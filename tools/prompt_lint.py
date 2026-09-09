#!/usr/bin/env python3
"""prompt_lint.py — Illustrious / Anima 向けプロンプトの検証・最適化ツール（依存ライブラリなし、Python 3.9+）

できること
  1. タグの実在チェック: Danbooru タグ DB（tools/data/danbooru_tags.csv, 14 万タグ・投稿数・別名）と照合し、
     存在しないタグ / 別名（例: violet eyes → purple eyes）/ 投稿数が少なく効きにくいタグ / 絵師タグ / 版権タグ を指摘する。
  2. CLIP 75 トークン境界の可視化（Illustrious 系）: openai/CLIP の BPE を同梱し、A1111 と同じ「カンマ区切り要素を 75 トークンごとに分割」を再現。
     先頭チャンクに何が入っているか、絵師タグが別チャンク（BREAK）になっているかを確認できる。
  3. モデル別ルール: 品質タグ・レーティング・年代タグ・光/画角/表情の有無・ネガティブの長さ・Anima のアンダースコア/`@絵師`/score_* など。
  4. 変換: --convert-to anima / illustrious で、品質タグ・レーティング・別名・記法・重みを相手モデル向けに書き換える。

使い方
  python3 tools/prompt_lint.py --model illustrious "1girl, solo, violet eyes, ... masterpiece, best quality"
  python3 tools/prompt_lint.py --model anima --variant aesthetic -f prompt.txt
  python3 tools/prompt_lint.py --model illustrious --negative "worst quality, low quality, ..."
  python3 tools/prompt_lint.py --model illustrious --convert-to anima "..."
  python3 tools/prompt_lint.py --json ...   # 機械可読出力

注意
  - Danbooru DB は a1111-sd-webui-tagcomplete 同梱 danbooru.csv のスナップショット（2026-09-09 取得）。最新の投稿数とは多少ずれる。
  - 「存在しない」= Danbooru タグではない、という意味。Anima / RouWei の自然文や、モデル固有タグ（masterpiece 等）は別扱いで判定する。
"""
from __future__ import annotations

import argparse
import csv
import gzip
import html
import json
import os
import re
import sys
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
TAG_DB = os.path.join(DATA_DIR, "danbooru_tags.csv")
BPE_PATH = os.path.join(DATA_DIR, "bpe_simple_vocab_16e6.txt.gz")

CATEGORY = {0: "general", 1: "artist", 3: "copyright", 4: "character", 5: "meta"}

# ---------------------------------------------------------------------------
# モデル固有語彙（Danbooru には無いが、各モデルが学習している特殊タグ）
# ---------------------------------------------------------------------------
QUALITY_ILLUSTRIOUS = {
    "masterpiece", "best quality", "good quality", "normal quality", "low quality", "worst quality",
    "very aesthetic", "aesthetic", "displeasing", "very displeasing", "amazing quality", "bad quality",
    "worst detail", "bad detail", "very awa", "high quality", "medium quality",
}
QUALITY_ANIMA = {
    "masterpiece", "best quality", "good quality", "normal quality", "low quality", "worst quality",
} | {f"score_{i}" for i in range(1, 10)}
QUALITY_PONY = {f"score_{i}" for i in range(1, 10)} | {f"score_{i}_up" for i in range(1, 10)} | {"source_anime", "source_furry", "source_pony", "source_cartoon"}
QUALITY_ANIMAGINE = {"high score", "great score", "good score", "average score", "bad score", "low score", "worst score"}
QUALITY_LIKE = QUALITY_ILLUSTRIOUS | QUALITY_ANIMA | QUALITY_PONY | QUALITY_ANIMAGINE

PERIOD_TAGS = {"newest", "recent", "mid", "early", "old", "oldest", "modern"}
RATING_ILLUSTRIOUS = {"general", "sensitive", "questionable", "explicit", "nsfw", "safe"}
RATING_ANIMA = {"safe", "sensitive", "nsfw", "explicit"}
YEAR_RE = re.compile(r"^year \d{4}$")
SCORE_RE = re.compile(r"^score_\d(?:_up)?$")

# Danbooru に無いが SD 界隈で常用され、実効があると報告される語（弱い警告に留める）
COMMON_NON_DANBOORU = {
    "cinematic lighting", "volumetric lighting", "soft lighting", "warm lighting", "dramatic lighting", "studio lighting",
    "rim lighting", "rim light", "god rays", "detailed eyes", "detailed background", "detailed face", "intricate details",
    "ultra-detailed", "ultra detailed", "high resolution", "4k", "8k", "clean lineart", "beautiful", "cute", "sharp focus",
    "glossy lips", "shiny hair", "soft shadow", "dramatic shadow", "golden hour", "blue hour", "medium shot", "face focus",
    "extreme close-up", "small figure", "cel shading", "flat colors", "anime coloring", "anime style", "digital painting",
    "semi-realistic", "2.5d", "muted colors", "soft edges", "paper texture", "rough lines", "unfinished", "bold outlines",
    "poster design", "negative space", "gentle smile", "gentle expression", "nervous smile", "window light", "morning light",
    "pale light", "wet street", "city street", "school gate", "festival stall", "fluorescent light", "miko outfit",
    "standing on a hill", "thick painting", "spring", "afternoon", "evening", "depth", "long silver hair",
}

# 別名・表記ゆれ → Danbooru 正規タグ（DB の alias 列に無いものを補完）
EXTRA_ALIASES = {
    "silver hair": "grey hair",
    "violet eyes": "purple eyes",
    "white blouse": "white shirt",
    "arms crossed": "crossed arms",
    "wide eyes": "wide-eyed",
    "god rays": "sunbeam",
    "street lamp": "lamppost",
    "rain boots": "rubber boots",
    "side by side": "side-by-side",
    "coffee cup": "cup",
    "anime screencap": "anime screenshot",
    "1990s style": "1990s (style)",
    "1980s style": "1980s (style)",
    "2000s style": "2000s (style)",
    "watercolor": "watercolor (medium)",
    "retro anime": "retro artstyle",
    "backlit": "backlighting",
    "lens flares": "lens flare",
    "maple": "maple leaf",
    "miko outfit": "miko",
    "festival stall": "food stand",
    "fluorescent light": "fluorescent lamp",
    "username": "twitter username",
}
# ネガティブでは慣用的に使われ、別名警告を出さない語
NEG_CONVENTIONAL = {"text", "username", "signature", "watermark", "logo", "artist name", "bad hands", "bad anatomy", "extra digits", "fewer digits"}

# 「魅力の 7 原則」チェック用の語彙（Danbooru 実タグ中心）
LIGHT_TAGS = {
    "backlighting", "rim light", "rim lighting", "sidelighting", "underlighting", "dappled sunlight", "light rays", "sunbeam",
    "lens flare", "sunlight", "sunset", "neon lights", "glowing", "light particles", "bloom", "cinematic lighting",
    "volumetric lighting", "soft lighting", "candlelight", "spotlight", "moonlight", "night", "dusk", "evening", "twilight",
    "sunrise", "golden hour", "warm lighting", "dim lighting", "dramatic lighting", "overcast", "window light", "morning light",
}
CAMERA_TAGS = {
    "from below", "from above", "from side", "from behind", "dutch angle", "fisheye", "close-up", "foreshortening", "wide shot",
    "cowboy shot", "upper body", "portrait", "full body", "face focus", "eye focus", "pov", "medium shot", "extreme close-up",
    "straight-on", "looking back", "profile", "three-quarter view", "from outside", "scenery", "wide-angle", "telephoto",
}
EXPRESSION_EYES = {"half-closed eyes", "wide-eyed", "wide eyes", "closed eyes", "one eye closed", "looking at viewer", "looking to the side",
                   "looking away", "looking down", "looking up", "tareme", "tsurime", "jitome", "empty eyes", "sparkling eyes", "glowing eyes", "wink"}
EXPRESSION_MOUTH = {"light smile", "smile", "grin", "parted lips", "closed mouth", ":d", ":o", ":3", ";d", "tongue out", "pout", "open mouth",
                    "laughing", "smug", "teeth", "clenched teeth", "lips", "puckered lips", "fang", "yawning"}
EXPRESSION_BROW_CHEEK = {"blush", "raised eyebrows", "furrowed brow", "embarrassed", "nervous", "tears", "crying", "sweatdrop", "angry",
                         "surprised", "expressionless", "serious", "sleepy", "flustered", "nose blush", "v-shaped eyebrows", "worried"}
NEG_BASIC_ILLUSTRIOUS = {"worst quality", "low quality"}

MAX_TOKENS_PER_CHUNK = 75


# ---------------------------------------------------------------------------
# CLIP BPE tokenizer（openai/CLIP simple_tokenizer.py の移植。ftfy 依存を外し、\p{L} を re 相当に置換）
# ---------------------------------------------------------------------------
@lru_cache()
def bytes_to_unicode():
    bs = list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1)) + list(range(ord("®"), ord("ÿ") + 1))
    cs = bs[:]
    n = 0
    for b in range(2 ** 8):
        if b not in bs:
            bs.append(b)
            cs.append(2 ** 8 + n)
            n += 1
    return dict(zip(bs, [chr(c) for c in cs]))


def get_pairs(word):
    pairs = set()
    prev = word[0]
    for ch in word[1:]:
        pairs.add((prev, ch))
        prev = ch
    return pairs


class ClipTokenizer:
    def __init__(self, bpe_path: str = BPE_PATH):
        self.byte_encoder = bytes_to_unicode()
        merges = gzip.open(bpe_path).read().decode("utf-8").split("\n")
        merges = merges[1: 49152 - 256 - 2 + 1]
        merges = [tuple(m.split()) for m in merges]
        vocab = list(bytes_to_unicode().values())
        vocab = vocab + [v + "</w>" for v in vocab]
        for m in merges:
            vocab.append("".join(m))
        vocab.extend(["<|startoftext|>", "<|endoftext|>"])
        self.encoder = dict(zip(vocab, range(len(vocab))))
        self.bpe_ranks = dict(zip(merges, range(len(merges))))
        self.cache: Dict[str, str] = {}
        # 原典: '<|startoftext|>|<|endoftext|>|'s|'t|'re|'ve|'m|'ll|'d|[\p{L}]+|[\p{N}]|[^\s\p{L}\p{N}]+'
        self.pat = re.compile(r"""<\|startoftext\|>|<\|endoftext\|>|'s|'t|'re|'ve|'m|'ll|'d|[^\W\d_]+|\d|(?:[^\w\s]|_)+""", re.IGNORECASE)

    def bpe(self, token: str) -> str:
        if token in self.cache:
            return self.cache[token]
        word = tuple(token[:-1]) + (token[-1] + "</w>",)
        pairs = get_pairs(word)
        if not pairs:
            return token + "</w>"
        while True:
            bigram = min(pairs, key=lambda p: self.bpe_ranks.get(p, float("inf")))
            if bigram not in self.bpe_ranks:
                break
            first, second = bigram
            new_word: List[str] = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except ValueError:
                    new_word.extend(word[i:])
                    break
                if word[i] == first and i < len(word) - 1 and word[i + 1] == second:
                    new_word.append(first + second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            word = tuple(new_word)
            if len(word) == 1:
                break
            pairs = get_pairs(word)
        out = " ".join(word)
        self.cache[token] = out
        return out

    def encode(self, text: str) -> List[int]:
        text = html.unescape(html.unescape(text))
        text = re.sub(r"\s+", " ", text).strip().lower()
        ids: List[int] = []
        for token in re.findall(self.pat, text):
            token = "".join(self.byte_encoder[b] for b in token.encode("utf-8"))
            ids.extend(self.encoder[t] for t in self.bpe(token).split(" "))
        return ids

    def count(self, text: str) -> int:
        return len(self.encode(text))


# ---------------------------------------------------------------------------
# タグ DB
# ---------------------------------------------------------------------------
class TagDB:
    def __init__(self, path: str = TAG_DB):
        self.tags: Dict[str, Tuple[int, int]] = {}
        self.alias: Dict[str, str] = {}
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # header
            for row in reader:
                if len(row) < 3:
                    continue
                name, cat, cnt = row[0], int(row[1]), int(row[2])
                self.tags[name] = (cat, cnt)
                if len(row) > 3 and row[3]:
                    for a in row[3].split(","):
                        a = a.strip()
                        if a and a not in self.alias:
                            self.alias[a] = name
        for k, v in EXTRA_ALIASES.items():
            ku = k.replace(" ", "_")
            vu = v.replace(" ", "_")
            if ku != vu and ku not in self.tags and vu in self.tags:
                self.alias[ku] = vu

    def lookup(self, tag: str):
        """returns (status, canonical, category, count)"""
        key = tag.strip().lower().replace(" ", "_")
        if key in self.tags:
            cat, cnt = self.tags[key]
            return "ok", key, cat, cnt
        if key in self.alias:
            canon = self.alias[key]
            cat, cnt = self.tags.get(canon, (0, 0))
            return "alias", canon, cat, cnt
        return "missing", key, None, 0


# ---------------------------------------------------------------------------
# プロンプト解析
# ---------------------------------------------------------------------------
WEIGHT_RE = re.compile(r"^\((.+?):\s*([0-9.]+)\)$")
LORA_RE = re.compile(r"<(lora|lyco|hypernet):[^>]+>", re.IGNORECASE)
WILDCARD_RE = re.compile(r"__[A-Za-z0-9_./-]+__")
VARIANT_RE = re.compile(r"\{[^{}]*\}")
CONTROL_WORDS = {"BREAK", "ADDCOMM", "ADDCOL", "ADDROW", "ADDBASE", "AND"}
CONTROL_RE = re.compile(r"\b(BREAK|ADDCOMM|ADDCOL|ADDROW|ADDBASE)\b")
SENTENCE_WORDS = {"the", "a", "an", "she", "he", "her", "his", "they", "them", "their", "is", "are", "was", "were", "with", "while",
                  "as", "of", "at", "into", "behind", "beside", "toward", "towards", "through", "over", "under", "who", "that", "which"}


def strip_weight(s: str) -> Tuple[str, Optional[float]]:
    s = s.strip()
    m = WEIGHT_RE.match(s)
    if m:
        return m.group(1).strip(), float(m.group(2))
    w = None
    while len(s) >= 2 and ((s[0] == "(" and s[-1] == ")") or (s[0] == "[" and s[-1] == "]")):
        w = (w or 1.0) * (1.1 if s[0] == "(" else 1 / 1.1)
        s = s[1:-1].strip()
    return s, w


def unescape_parens(s: str) -> str:
    return s.replace("\\(", "(").replace("\\)", ")")


def is_sentence(seg: str) -> bool:
    """自然文判定: 5 語以上、機能語（the/a/she/her/with...）が 2 つ以上、かつカンマ区切り 1 要素あたり平均 4 語以上。
    タグ列（"1girl, solo, looking at viewer, ..."）は平均語数が 2 前後なので文にならない。"""
    words = seg.lower().split()
    if len(words) < 5:
        return False
    hits = sum(1 for w in words if w.strip(".,;:!?") in SENTENCE_WORDS)
    pieces = [p for p in seg.split(",") if p.strip()]
    avg_words = len(words) / max(1, len(pieces))
    return hits >= 2 and avg_words >= 4


def _split_segments(prompt: str) -> List[Tuple[str, bool]]:
    """ピリオドで区切り、(セグメント, 自然文か) を返す。自然文はカンマで分割しない。"""
    out: List[Tuple[str, bool]] = []
    for seg in re.split(r"(?<!\d)\.(?!\d)", prompt):
        seg = seg.strip()
        if not seg:
            continue
        out.append((seg, is_sentence(seg) and not CONTROL_RE.search(seg)))
    return out


def split_prompt(prompt: str) -> List[dict]:
    """カンマ/改行/BREAK で分割。自然文は sentence として丸ごと 1 要素にする。"""
    prompt = LORA_RE.sub(lambda m: f" {m.group(0)} ", prompt)
    items: List[dict] = []
    chunk_idx = 0
    for seg, sent in _split_segments(prompt):
        if sent:
            items.append({"raw": seg, "text": seg.strip(), "weight": None, "kind": "sentence", "chunk_hint": chunk_idx})
            continue
        text = CONTROL_RE.sub(r", \1 ,", seg)
        for raw in re.split(r"[,\n]", text):
            piece = raw.strip()
            if not piece:
                continue
            if piece in CONTROL_WORDS:
                if piece == "BREAK" or piece.startswith("ADD"):
                    chunk_idx += 1
                items.append({"raw": piece, "kind": "control", "chunk_hint": chunk_idx})
                continue
            if LORA_RE.fullmatch(piece):
                items.append({"raw": piece, "kind": "lora", "chunk_hint": chunk_idx})
                continue
            if WILDCARD_RE.fullmatch(piece) or VARIANT_RE.fullmatch(piece):
                items.append({"raw": piece, "kind": "wildcard", "chunk_hint": chunk_idx})
                continue
            body, weight = strip_weight(piece)
            body = unescape_parens(body).strip()
            if not body:
                continue
            kind = "sentence" if is_sentence(body) else "tag"
            items.append({"raw": piece, "text": body, "weight": weight, "kind": kind, "chunk_hint": chunk_idx})
    return items


def clip_chunks(items: List[dict], tok: ClipTokenizer) -> List[List[dict]]:
    """A1111 方式の近似: カンマ区切り要素を順に詰め、75 トークンを超える要素の手前で改チャンク。BREAK で強制改チャンク。"""
    chunks: List[List[dict]] = [[]]
    used = 0
    for it in items:
        if it["kind"] == "control":
            if it["raw"] == "BREAK" or it["raw"].startswith("ADD"):
                chunks.append([])
                used = 0
            continue
        if it["kind"] == "lora":
            continue
        text = it.get("text") or it["raw"]
        n = tok.count(text) + 1  # 後続のカンマ分を 1 トークンとして概算
        it["tokens"] = n - 1
        if used + n > MAX_TOKENS_PER_CHUNK and used > 0:
            chunks.append([])
            used = 0
        chunks[-1].append(it)
        used += n
    return chunks


# ---------------------------------------------------------------------------
# 検証
# ---------------------------------------------------------------------------
class Finding:
    def __init__(self, level: str, code: str, msg: str, tag: Optional[str] = None):
        self.level, self.code, self.msg, self.tag = level, code, msg, tag

    def as_dict(self):
        return {"level": self.level, "code": self.code, "tag": self.tag, "message": self.msg}


def lint(prompt: str, model: str, negative: bool = False, variant: str = "", db: Optional[TagDB] = None,
         tok: Optional[ClipTokenizer] = None) -> dict:
    db = db or TagDB()
    findings: List[Finding] = []
    items = split_prompt(prompt)
    tags = [it for it in items if it["kind"] == "tag"]
    sentences = [it for it in items if it["kind"] == "sentence"]
    model = model.lower()
    is_anima = model == "anima"
    is_rouwei = model == "rouwei"
    is_noob = model == "noobai"
    quality_vocab = QUALITY_ANIMA if is_anima else (QUALITY_ILLUSTRIOUS | QUALITY_ANIMAGINE | QUALITY_PONY)
    rating_vocab = RATING_ANIMA if is_anima else RATING_ILLUSTRIOUS

    seen = {}
    artist_tags, copyright_tags, character_tags = [], [], []
    quality_found, rating_found, period_found = [], [], []
    light_found, camera_found = [], []
    eyes_found, mouth_found, brow_found = [], [], []
    canonical_tags: List[str] = []

    for it in tags:
        t = it["text"].lower()
        t_sp = t if SCORE_RE.match(t) else t.replace("_", " ")
        # 絵師記法
        if t_sp.startswith("@"):
            it["is_artist"] = True
            artist_tags.append(t_sp)
            canonical_tags.append(t_sp)
            continue
        if t_sp.startswith("by "):
            it["is_artist"] = True
            artist_tags.append(t_sp)
            canonical_tags.append(t_sp)
            if not is_rouwei and not is_noob:
                findings.append(Finding("W", "artist-by-prefix", f"`{t_sp}`: 'by ' 接頭は RouWei / NoobAI 向け。Illustrious 派生は Danbooru の絵師タグ名そのまま、Anima は '@name'", t_sp))
            continue
        if t_sp in seen:
            findings.append(Finding("W", "duplicate", f"`{t_sp}` が重複", t_sp))
        seen[t_sp] = True
        # モデル固有語彙
        if t_sp in quality_vocab:
            quality_found.append(t_sp)
            canonical_tags.append(t_sp)
            if is_anima and variant == "aesthetic" and SCORE_RE.match(t_sp):
                findings.append(Finding("E", "anima-aesthetic-score", f"`{t_sp}`: Anima Aesthetic では score_* をポジ・ネガとも使わない（公式 README）", t_sp))
            if is_rouwei and t_sp not in {"masterpiece", "best quality", "low quality", "worst quality"}:
                findings.append(Finding("W", "rouwei-quality", f"`{t_sp}`: RouWei の品質タグは masterpiece / best quality / low quality / worst quality の 4 つだけ有効（モデルカード）", t_sp))
            continue
        if t_sp in rating_vocab:
            rating_found.append(t_sp)
            canonical_tags.append(t_sp)
            if is_anima and t_sp not in RATING_ANIMA:
                findings.append(Finding("W", "anima-rating", f"`{t_sp}`: Anima のレーティングは safe / sensitive / nsfw / explicit", t_sp))
            if not is_anima and t_sp == "safe" and not is_noob:
                findings.append(Finding("I", "rating-safe", "`safe` は NoobAI / Animagine 系の語彙。Illustrious 本家・WAI 系は `general`（WAI v17 カード: general/sensitive/nsfw/explicit）", t_sp))
            continue
        if t_sp in PERIOD_TAGS or YEAR_RE.match(t_sp):
            period_found.append(t_sp)
            canonical_tags.append(t_sp)
            if YEAR_RE.match(t_sp) and not is_anima:
                findings.append(Finding("W", "year-tag", f"`{t_sp}`: 'year 2025' 形式は Anima の語彙。Illustrious 系は newest / recent / mid / early / old", t_sp))
            continue
        # Danbooru 照合
        status, canon, cat, cnt = db.lookup(t)
        canon_sp = canon.replace("_", " ")
        if status == "ok":
            canonical_tags.append(canon_sp)
            it["danbooru"] = {"canonical": canon_sp, "category": CATEGORY.get(cat, str(cat)), "count": cnt}
            if cat == 1:
                artist_tags.append(canon_sp)
                it["is_artist"] = True
            elif cat == 3:
                copyright_tags.append(canon_sp)
            elif cat == 4:
                character_tags.append(canon_sp)
            elif cnt < 300 and not (negative and t_sp in NEG_CONVENTIONAL):
                findings.append(Finding("W", "low-count", f"`{t_sp}`: Danbooru 投稿数 {cnt} 件と少なく、効きが弱い可能性（代替語を検討）", t_sp))
            elif cnt < 1000 and not (negative and t_sp in NEG_CONVENTIONAL):
                findings.append(Finding("I", "lowish-count", f"`{t_sp}`: Danbooru 投稿数 {cnt} 件（やや少なめ）", t_sp))
        elif status == "alias":
            canonical_tags.append(canon_sp)
            it["danbooru"] = {"canonical": canon_sp, "category": CATEGORY.get(cat, str(cat)), "count": cnt, "alias_of": t_sp}
            if not (negative and t_sp in NEG_CONVENTIONAL):
                findings.append(Finding("W", "alias", f"`{t_sp}` は Danbooru では `{canon_sp}` に統合済み（{cnt:,} 件）。正規表記に置き換え推奨", t_sp))
        else:
            canonical_tags.append(t_sp)
            if t_sp in COMMON_NON_DANBOORU:
                findings.append(Finding("I", "non-danbooru", f"`{t_sp}`: Danbooru タグではない（自然語として弱く効く程度。Anima / RouWei の自然文なら可）", t_sp))
            else:
                findings.append(Finding("W", "unknown", f"`{t_sp}`: Danbooru タグに存在しない。誤記か、モデルが知らない語の可能性", t_sp))
        if is_anima and "_" in it["text"] and not SCORE_RE.match(t):
            findings.append(Finding("W", "anima-underscore", f"`{it['text']}`: Anima はスペース区切り（アンダースコアは score_* のみ）", it["text"]))
        # 7 原則用の集計
        if canon_sp in LIGHT_TAGS or t_sp in LIGHT_TAGS:
            light_found.append(t_sp)
        if canon_sp in CAMERA_TAGS or t_sp in CAMERA_TAGS:
            camera_found.append(t_sp)
        if canon_sp in EXPRESSION_EYES or t_sp in EXPRESSION_EYES:
            eyes_found.append(t_sp)
        if canon_sp in EXPRESSION_MOUTH or t_sp in EXPRESSION_MOUTH:
            mouth_found.append(t_sp)
        if canon_sp in EXPRESSION_BROW_CHEEK or t_sp in EXPRESSION_BROW_CHEEK:
            brow_found.append(t_sp)

    # ---- 構造チェック（ポジティブ）
    if not negative:
        if not quality_found:
            findings.append(Finding("W", "no-quality", "品質タグが無い（Illustrious: masterpiece, best quality, very aesthetic, absurdres ／ Anima Base: masterpiece, best quality, score_7）"))
        elif len(quality_found) > 6:
            findings.append(Finding("W", "too-many-quality", f"品質・美的タグが {len(quality_found)} 個。WAI v17 カードは『品質タグの積みすぎは画質を落としぼやける』と明記。4〜5 個に絞る"))
        if not rating_found:
            findings.append(Finding("W", "no-rating", "レーティングタグが無い（SFW 固定なら Illustrious: general ／ NoobAI・Animagine: safe ／ Anima: safe）"))
        if not period_found and not is_anima:
            findings.append(Finding("I", "no-period", "年代タグ（newest / recent / ...）が無い。画風の年代を固定したい場合は追加"))
        if not light_found:
            findings.append(Finding("I", "no-light", "光タグが無い（backlighting / dappled sunlight / light rays / sunset など 1 つ）"))
        if not camera_found:
            findings.append(Finding("I", "no-camera", "画角タグが無い（upper body / cowboy shot / from below / close-up など 1 つ）"))
        axes = sum(1 for x in (eyes_found, mouth_found, brow_found) if x)
        if tags and axes < 2 and not sentences:
            findings.append(Finding("I", "expression-axes", f"表情の軸が {axes} 本（目・口・眉/頬の 3 軸で指定すると安定。smile 単発は効きが弱い）"))
        if artist_tags:
            for a in artist_tags:
                findings.append(Finding("W", "artist", f"絵師タグ `{a}`: X 公開作品では存命絵師名の単独使用を避ける（倫理・通報リスク）。使うなら 2〜3 人を弱めにブレンド", a))
            if is_anima:
                for a in artist_tags:
                    if not a.startswith("@"):
                        findings.append(Finding("E", "anima-artist-at", f"`{a}`: Anima は絵師名に必ず '@' を付ける（無いとほぼ効かない。公式 README）", a))
            if is_rouwei:
                for a in artist_tags:
                    if not a.startswith("by "):
                        findings.append(Finding("E", "rouwei-artist-by", f"`{a}`: RouWei は 'by ' 接頭が必須、かつ BREAK で別チャンクに（モデルカード）", a))
        if copyright_tags or character_tags:
            findings.append(Finding("I", "copyright", f"版権・キャラタグ: {', '.join(copyright_tags + character_tags)} — X 投稿ではファンアートタグ・キャラ名タグを付けない方針（05 参照）。Hassaku は作品名タグを学習していない"))
        if is_anima and not sentences:
            findings.append(Finding("I", "anima-no-sentence", "Anima は自然文 2 文以上を併記すると構図・光・関係性の追従が上がる（公式 README）"))
        if is_anima and sentences and len(sentences) < 2:
            findings.append(Finding("I", "anima-one-sentence", "自然文が 1 文。公式は『純自然文なら 2 文以上』を推奨（光・動き・気持ちをもう 1 文）"))
    else:
        # ---- ネガティブ
        if is_anima:
            missing = [r for r in ("sensitive", "nsfw", "explicit") if r not in rating_found]
            if missing and "safe" not in rating_found:
                findings.append(Finding("W", "anima-neg-rating", f"SFW 固定なら Anima ネガに {', '.join(missing)} を入れる（ポジ safe とセット）"))
            if variant != "aesthetic" and not any(SCORE_RE.match(q) for q in quality_found):
                findings.append(Finding("I", "anima-neg-score", "Anima Base の公式ネガは worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration"))
            if variant == "aesthetic" and any(SCORE_RE.match(q) for q in quality_found):
                findings.append(Finding("E", "anima-aesthetic-score", "Anima Aesthetic ではネガの score_* も外す（公式 README）"))
            if "artist name" not in {t["text"].lower().replace("_", " ") for t in tags}:
                findings.append(Finding("I", "anima-neg-artist-name", "Anima 公式ネガの `artist name` が無い"))
        else:
            if "nsfw" not in rating_found:
                findings.append(Finding("W", "neg-nsfw", "SFW 固定なら Illustrious 系ネガに `nsfw`（WAI v17 カード: 『ユーザーが nsfw をネガに入れる前提』）"))
            if not (NEG_BASIC_ILLUSTRIOUS & set(quality_found)):
                findings.append(Finding("I", "neg-basic", "worst quality / low quality が無い"))
            if len(tags) > 25:
                findings.append(Finding("W", "neg-too-long", f"ネガが {len(tags)} 要素。Illustrious はネガに敏感で、長すぎると画質低下（WAI v17 カード・RouWei カード）。短く始めて症状ごとに足す"))
            if is_rouwei and len(tags) > 5:
                findings.append(Finding("W", "rouwei-neg", "RouWei の推奨ネガは `worst quality, low quality, watermark` のみ"))

    # ---- CLIP チャンク（Illustrious 系のみ意味がある）
    chunks_out = []
    total_tokens = None
    if not is_anima:
        tok = tok or ClipTokenizer()
        chunks = clip_chunks(items, tok)
        total_tokens = sum(it.get("tokens", 0) for ch in chunks for it in ch) + max(0, sum(len(ch) for ch in chunks) - 1)
        for ci, ch in enumerate(chunks):
            used = sum(it.get("tokens", 0) + 1 for it in ch)
            chunks_out.append({"index": ci + 1, "tokens": used, "items": [it.get("text") or it["raw"] for it in ch]})
        if len(chunks) > 1 and not negative:
            first = {it.get("text", "").lower() for it in chunks[0]}
            key_missing = [q for q in quality_found if q not in first]
            if key_missing and "BREAK" not in prompt:
                findings.append(Finding("I", "quality-outside-first-chunk", f"品質タグ {key_missing} が第 1 チャンク（先頭 75 トークン）の外にある。派生モデルの多くは末尾でも効くが、キャラ固定文は先頭に置く"))
            for ci, ch in enumerate(chunks):
                names = [it for it in ch if it.get("is_artist")]
                others = [it for it in ch if not it.get("is_artist") and it["kind"] == "tag" and it.get("text", "").lower() not in quality_vocab]
                if names and others and (is_rouwei or len(chunks) > 1):
                    findings.append(Finding("W", "artist-chunk", f"チャンク {ci + 1} に絵師タグと一般タグが混在。RouWei は BREAK で絵師タグを別チャンクにするのが必須、Illustrious 派生でも推奨"))
        elif is_rouwei and artist_tags and not negative:
            others = [it for it in chunks[0] if not it.get("is_artist") and it["kind"] == "tag" and it.get("text", "").lower() not in quality_vocab]
            if others:
                findings.append(Finding("W", "artist-chunk", "RouWei: 絵師タグ（by …）は BREAK で一般タグと別チャンクにする（モデルカード）"))
        if len(chunks) >= 3 and not negative:
            findings.append(Finding("I", "many-chunks", f"チャンク数 {len(chunks)}（{total_tokens} トークン）。後ろのチャンクほど効きが薄い。20〜40 タグに絞ると安定"))
        elif len(chunks) == 2 and not negative:
            findings.append(Finding("I", "two-chunks", f"合計 {total_tokens} トークンで 75 を超え 2 チャンク。第 2 チャンクは効きが薄いので、削るか BREAK で意図的に分ける"))
    else:
        words = len(prompt.split())
        if words > 350:
            findings.append(Finding("W", "anima-long", f"約 {words} 語。Anima の LLM adapter は 512 トークン基準。長すぎる部分は無視される可能性"))

    order = {"E": 0, "W": 1, "I": 2}
    findings.sort(key=lambda f: order[f.level])
    return {
        "model": model, "variant": variant, "negative": negative,
        "n_tags": len(tags), "n_sentences": len(sentences),
        "tokens_clip": total_tokens, "chunks": chunks_out,
        "artist_tags": artist_tags, "copyright_tags": copyright_tags, "character_tags": character_tags,
        "quality_tags": quality_found, "rating_tags": rating_found, "period_tags": period_found,
        "light_tags": light_found, "camera_tags": camera_found,
        "expression_axes": {"eyes": eyes_found, "mouth": mouth_found, "brow_cheek": brow_found},
        "canonical_prompt": ", ".join(canonical_tags),
        "findings": [f.as_dict() for f in findings],
    }


# ---------------------------------------------------------------------------
# 変換
# ---------------------------------------------------------------------------
ILL_TO_ANIMA_RATING = {"general": "safe", "safe": "safe", "sensitive": "sensitive", "questionable": "nsfw", "explicit": "explicit", "nsfw": "nsfw"}
ANIMA_TO_ILL_RATING = {"safe": "general", "sensitive": "sensitive", "nsfw": "nsfw", "explicit": "explicit"}


def convert(prompt: str, src: str, dst: str, negative: bool = False, db: Optional[TagDB] = None, variant: str = "") -> str:
    """Illustrious 系 ⇄ Anima のプロンプト変換。品質・レーティング・年代・別名・絵師記法・重みを書き換える。"""
    db = db or TagDB()
    items = split_prompt(prompt)
    body: List[str] = []
    rating: List[str] = []
    period: List[str] = []
    meta: List[str] = []
    for it in items:
        if it["kind"] == "control":
            if dst == "anima":
                continue  # Anima には BREAK の概念が無い（ComfyUI では Conditioning Concat が相当）
            body.append(it["raw"])
            continue
        if it["kind"] in ("lora", "wildcard"):
            body.append(it["raw"])
            continue
        if it["kind"] == "sentence":
            body.append(it["text"].rstrip(".") + ("." if dst == "anima" else ""))
            continue
        t = it["text"].lower()
        t = t if SCORE_RE.match(t) else t.replace("_", " ")
        w = it.get("weight")
        if t in ("absurdres", "highres"):
            meta.append(t)
            continue
        if t in QUALITY_LIKE:
            continue  # 品質ブロックは最後にまとめて生成
        if YEAR_RE.match(t):
            period.append(t if dst == "anima" else "newest")
            continue
        if t in PERIOD_TAGS:
            period.append(t)
            continue
        if t in RATING_ILLUSTRIOUS or t in RATING_ANIMA:
            if dst == "anima":
                if negative and t == "nsfw":
                    rating.extend(["sensitive", "nsfw", "explicit"])
                else:
                    rating.append(ILL_TO_ANIMA_RATING.get(t, t))
            else:
                if negative and t in ("sensitive", "explicit"):
                    continue
                rating.append(ANIMA_TO_ILL_RATING.get(t, t))
            continue
        if dst == "anima":
            if t.startswith("by "):
                t = "@" + t[3:]
        else:
            if t.startswith("@"):
                t = t[1:]
        if t in ("anime screencap", "anime screenshot"):
            t = "anime screenshot" if dst == "anima" else "anime screencap"
        elif not t.startswith("@"):
            status, canon, cat, cnt = db.lookup(t)
            if status == "alias":
                t = canon.replace("_", " ")
        if t == "artist name" and not negative:
            continue
        esc = t.replace("(", "\\(").replace(")", "\\)")
        if w and w != 1.0:
            w2 = round(1 + (w - 1) * (2.5 if dst == "anima" else 1 / 2.5), 2)
            body.append(f"({esc}:{w2})")
        else:
            body.append(esc)
    if dst == "anima":
        if negative:
            q = ["worst quality", "low quality"] + ([] if variant == "aesthetic" else ["score_1", "score_2", "score_3"]) + ["artist name"]
            out = q + body + rating
        else:
            q = ["masterpiece", "best quality"] + ([] if variant == "aesthetic" else ["score_7"])
            if not rating:
                rating = ["safe"]
            out = q + period + meta + rating + body
    else:
        if negative:
            out = ["worst quality", "low quality"] + body + rating
        else:
            q = ["masterpiece", "best quality", "very aesthetic", "absurdres"]
            per = [p for p in period if p in PERIOD_TAGS] or ["newest"]
            if not rating:
                rating = ["general"]
            out = body + q + per + rating
    seen = set()
    dedup = []
    for x in out:
        k = x.lower()
        if k in seen:
            continue
        seen.add(k)
        dedup.append(x)
    return ", ".join(dedup)


# ---------------------------------------------------------------------------
# コマンドライン
# ---------------------------------------------------------------------------
def format_report(res: dict) -> str:
    lines = []
    lines.append(f"model={res['model']}{(' variant=' + res['variant']) if res['variant'] else ''} {'NEGATIVE' if res['negative'] else 'POSITIVE'}  tags={res['n_tags']} sentences={res['n_sentences']}"
                 + (f" clip_tokens={res['tokens_clip']}" if res['tokens_clip'] is not None else ""))
    if res["chunks"]:
        for ch in res["chunks"]:
            lines.append(f"  chunk {ch['index']} ({ch['tokens']}/75 tok): " + ", ".join(ch["items"]))
    if not res["negative"]:
        lines.append(f"  quality={res['quality_tags']} rating={res['rating_tags']} period={res['period_tags']}")
        lines.append(f"  light={res['light_tags']} camera={res['camera_tags']} expression={res['expression_axes']}")
    if res["artist_tags"]:
        lines.append(f"  artist={res['artist_tags']}")
    n = {"E": 0, "W": 0, "I": 0}
    for f in res["findings"]:
        n[f["level"]] += 1
        lines.append(f"  [{f['level']}] {f['code']}: {f['message']}")
    lines.append(f"  summary: {n['E']} errors, {n['W']} warnings, {n['I']} info")
    lines.append(f"  canonical: {res['canonical_prompt']}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", nargs="?", help="プロンプト文字列（-f と排他）")
    ap.add_argument("-f", "--file", help="プロンプトを書いたファイル")
    ap.add_argument("--model", default="illustrious", choices=["illustrious", "noobai", "rouwei", "anima"])
    ap.add_argument("--variant", default="", help="anima: base / aesthetic / turbo")
    ap.add_argument("--negative", action="store_true", help="ネガティブプロンプトとして検証")
    ap.add_argument("--convert-to", choices=["anima", "illustrious"], help="相手モデル向けに変換して出力")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--db", default=TAG_DB)
    args = ap.parse_args(argv)
    if args.file:
        prompt = open(args.file, encoding="utf-8").read()
    elif args.prompt:
        prompt = args.prompt
    else:
        prompt = sys.stdin.read()
    db = TagDB(args.db)
    if args.convert_to:
        src = "anima" if args.model == "anima" else "illustrious"
        converted = convert(prompt, src, args.convert_to, negative=args.negative, db=db, variant=args.variant)
        print(json.dumps({"converted": converted}, ensure_ascii=False, indent=1) if args.json else converted)
        return 0
    res = lint(prompt, args.model, negative=args.negative, variant=args.variant, db=db)
    print(json.dumps(res, ensure_ascii=False, indent=1) if args.json else format_report(res))
    return 1 if any(f["level"] == "E" for f in res["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())

"""Pure-Python tag formatter (no ComfyUI dependency) for Danbooru-style prompts.

Two operations:
  * reorder  - group tags into a fixed category order
               (quality -> girl subject -> girl appearance -> girl clothes -> girl expression
                -> girl pose -> camera -> male -> other -> natural-language prose)
  * remove   - drop tags that describe the character herself (appearance and/or name),
               e.g. before applying a character LoRA

Category dictionaries live in ./categories/*.txt and are re-read when their mtime changes.
Line formats inside those files:
    plain text     exact match (case-insensitive, `_` and ` ` treated the same)
    re:<regex>     full-match regex on the normalized tag
    token:<word>   match if <word> is one of the whitespace/hyphen separated words of the tag
    # ...          comment
"""
import os
import re

CATEGORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "categories")

# Output order.  "prose" (natural-language sentences) is always appended last.
ORDER = [
    "quality",
    "girl_subject",
    "girl_appearance",
    "girl_clothes",
    "girl_expression",
    "girl_pose",
    "camera",
    "male",
    "other",
]

# Classification order (first match wins).  Differs from output order on purpose:
# accessories ("hair ribbon") must be tested before the generic "* hair" appearance rule,
# "closed eyes" before "* eyes", "solo focus" before the camera "* focus" rule, etc.
CLASSIFY_ORDER = [
    "quality",
    "male",
    "girl_subject",
    "camera",
    "girl_clothes",
    "girl_expression",
    "girl_pose",
    "girl_appearance",
]

LABELS_JA = {
    "quality": "品質",
    "girl_subject": "女キャラ(人数)",
    "girl_appearance": "女キャラ(外見)",
    "girl_clothes": "女服",
    "girl_expression": "女表情",
    "girl_pose": "女ポーズ",
    "camera": "画角",
    "male": "男タグ",
    "other": "その他",
    "prose": "自然文",
}

# `name (series)` style Danbooru character tags.
_NAME_WITH_SERIES = re.compile(r"^[^()]+\S \([^()]+\)$")
_WEIGHT_SUFFIX = re.compile(r":\s*[-+]?\d*\.?\d+\s*$")
_PROSE_MIN_WORDS = 7


# ----------------------------------------------------------------------------- dictionaries
class _Rules:
    def __init__(self, exact, regexes, tokens):
        self.exact = exact      # set[str]
        self.regexes = regexes  # list[re.Pattern]
        self.tokens = tokens    # set[str]

    def matches(self, norm):
        if norm in self.exact:
            return True
        if self.tokens and self.tokens.intersection(re.split(r"[\s\-/]+", norm)):
            return True
        return any(r.match(norm) for r in self.regexes)


_cache = {}  # name -> (mtime, _Rules)


def normalize(tag):
    """Lower-case, `_`->space, unescape parens, strip weights/emphasis, collapse spaces."""
    t = tag.strip()
    # peel emphasis / weight wrappers: ((x)), (x:1.2), [x]
    while len(t) >= 2 and ((t[0] == "(" and t[-1] == ")") or (t[0] == "[" and t[-1] == "]")) \
            and not t.startswith("\\("):
        inner = t[1:-1]
        if inner.count("(") != inner.count(")"):
            break
        t = inner.strip()
    t = _WEIGHT_SUFFIX.sub("", t)
    t = t.replace("\\(", "(").replace("\\)", ")")
    t = t.lower().replace("_", " ")
    t = re.sub(r"\s+", " ", t).strip().rstrip(".")
    # for grouped weights "(a, b:1.2)" classify by the first tag
    if "," in t:
        t = t.split(",", 1)[0].strip()
    return t


def _load(name):
    path = os.path.join(CATEGORY_DIR, name + ".txt")
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return _Rules(set(), [], set())
    hit = _cache.get(name)
    if hit and hit[0] == mtime:
        return hit[1]
    exact, regexes, tokens = set(), [], set()
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("re:"):
                # normalized tags use spaces, so let dictionary regexes be written with `_` too
                regexes.append(re.compile(line[3:].replace("_", " "), re.IGNORECASE))
            elif line.startswith("token:"):
                tokens.add(line[6:].strip().lower())
            else:
                exact.add(normalize(line))
    rules = _Rules(exact, regexes, tokens)
    _cache[name] = (mtime, rules)
    return rules


def is_character_name(norm):
    return bool(_NAME_WITH_SERIES.match(norm)) or _load("character_names").matches(norm)


def classify(norm):
    """Return the output category for a normalized tag."""
    if not norm:
        return "other"
    for cat in CLASSIFY_ORDER:
        if _load(cat).matches(norm):
            return cat
    if is_character_name(norm):
        return "girl_appearance"
    return "other"


# ----------------------------------------------------------------------------- parsing
def _split_top_level(text, sep=","):
    """Split on `sep` outside (), [], <> — keeps "(a, b:1.2)" and "<lora:x:0.8>" intact."""
    out, depth, cur = [], 0, []
    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            cur.append(c + text[i + 1])
            i += 2
            continue
        if c in "([<":
            depth += 1
        elif c in ")]>":
            depth = max(0, depth - 1)
        if c == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    out.append("".join(cur))
    return out


def _looks_like_prose(segment):
    return len(segment.split()) >= _PROSE_MIN_WORDS


def parse(text):
    """-> (tags:list[str] raw, prose:list[str], trailing_period:bool)"""
    tags, prose = [], []
    trailing_period = False
    for line in text.splitlines():
        if not line.strip():
            continue
        segs = [s for s in (x.strip() for x in _split_top_level(line)) if s]
        if not segs:
            continue
        in_prose = False
        for idx, seg in enumerate(segs):
            if in_prose or _looks_like_prose(seg):
                if not in_prose:
                    in_prose = True
                    # rest of this line is prose; re-join with the original commas
                    prose.append(", ".join(segs[idx:]))
                break
            tags.append(seg)
        if not in_prose and segs and segs[-1].endswith("."):
            trailing_period = True
            tags[-1] = tags[-1].rstrip(".").strip()
    return tags, prose, trailing_period


# ----------------------------------------------------------------------------- main API
def _csv_set(s):
    return {normalize(x) for x in _split_top_level(s or "") if x.strip()}


def format_tags(text, mode="reorder", remove_scope="appearance_and_name",
                keep_tags="", extra_character_tags="", dedupe=True):
    """
    mode: "reorder" | "remove_character" | "remove_character_and_reorder"
    remove_scope: "appearance_and_name" | "appearance" | "name"
    Returns (formatted_text, removed_tags_csv, report_text)
    """
    do_remove = mode in ("remove_character", "remove_character_and_reorder")
    do_reorder = mode in ("reorder", "remove_character_and_reorder")
    keep = _csv_set(keep_tags)
    extra = _csv_set(extra_character_tags)

    chunks_out, removed_all, report_lines = [], [], []
    for chunk_i, chunk in enumerate(re.split(r"\bBREAK\b", text)):
        tags, prose, trailing_period = parse(chunk)
        buckets = {c: [] for c in ORDER}
        kept_in_order, removed, seen = [], [], set()
        for raw in tags:
            norm = normalize(raw)
            if dedupe:
                if norm in seen:
                    continue
                seen.add(norm)
            cat = classify(norm)
            if do_remove and norm not in keep:
                is_name = is_character_name(norm)
                is_appearance = cat == "girl_appearance" and not is_name
                hit = norm in extra
                if remove_scope in ("appearance_and_name", "appearance") and is_appearance:
                    hit = True
                if remove_scope in ("appearance_and_name", "name") and is_name:
                    hit = True
                if hit:
                    removed.append(raw)
                    continue
            buckets[cat].append(raw)
            kept_in_order.append(raw)

        ordered = [t for c in ORDER for t in buckets[c]] if do_reorder else kept_in_order
        body = ", ".join(ordered)
        if trailing_period and body:
            body += "."
        if prose:
            body = (body + "\n" if body else "") + "\n".join(prose)
        chunks_out.append(body)
        removed_all.extend(removed)

        if len(text.split("BREAK")) > 1:
            report_lines.append(f"[BREAK chunk {chunk_i + 1}]")
        for c in ORDER:
            if buckets[c]:
                report_lines.append(f"{LABELS_JA[c]}: " + ", ".join(buckets[c]))
        if prose:
            report_lines.append(LABELS_JA["prose"] + ": " + " / ".join(prose))
        if removed:
            report_lines.append("削除: " + ", ".join(removed))

    return " BREAK ".join(chunks_out), ", ".join(removed_all), "\n".join(report_lines)

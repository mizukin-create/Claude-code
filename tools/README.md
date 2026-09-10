# tools/ — プロンプト検証・最適化ツール

## prompt_lint.py

Illustrious 系（WAI / Hassaku / Nova / Prefect / NoobAI / RouWei）と Anima のプロンプトを、一次資料に基づくルールで検証・変換する CLI。外部ライブラリ不要（Python 3.9+）。

```bash
# 検証（ポジティブ）
python3 tools/prompt_lint.py --model illustrious "1girl, solo, silver hair, violet eyes, ..., masterpiece, best quality, general"
python3 tools/prompt_lint.py --model anima --variant aesthetic -f my_prompt.txt

# 検証（ネガティブ）
python3 tools/prompt_lint.py --model illustrious --negative "worst quality, low quality, ..., nsfw"

# 変換（Illustrious → Anima、Anima → Illustrious）
python3 tools/prompt_lint.py --model illustrious --convert-to anima "..."
python3 tools/prompt_lint.py --model anima --convert-to illustrious "..."

# JSON 出力（他ツール連携用）
python3 tools/prompt_lint.py --json --model illustrious "..."

# 自己テスト
python3 tools/test_prompt_lint.py
```

### 何をチェックするか

| 種類 | 内容 | 根拠 |
|---|---|---|
| タグの実在 | Danbooru タグ DB（`data/danbooru_tags.csv`、140,782 タグ・投稿数・別名）と照合。**別名**（`violet eyes`→`purple eyes`、`silver hair`→`grey hair`、`white blouse`→`white shirt`、`anime screencap`→`anime screenshot`）、**存在しない語**、**投稿数 300 未満**（効きが弱い）を指摘 | Illustrious / NoobAI / Anima はいずれも Danbooru タグで学習（各モデルカード・README） |
| 75 トークン境界 | openai/CLIP の BPE を同梱し、A1111 と同じ「カンマ区切り要素を 75 トークンで分割」を再現。第 1 チャンク外の品質タグ、絵師タグと一般タグの混在、チャンク数を表示 | A1111 の仕様、RouWei カード「絵師タグは BREAK で別チャンク」 |
| 品質・レーティング・年代 | モデル語彙（`masterpiece` / `very aesthetic` / `score_7` / `general` / `safe` / `newest` / `year 2025` …）を Danbooru とは別に判定。積みすぎ（7 個以上）、レーティング欠落、Anima Aesthetic の `score_*` 混入をエラー扱い | WAI v17 カード「品質タグの積みすぎは画質低下」、Anima README「Aesthetic は score_* を使わない」 |
| 魅力の 7 原則 | 光タグ 1 つ・画角タグ 1 つ・表情 3 軸（目/口/眉頬）の有無を情報として表示 | `report/00_summary_and_proposal.md` §4.1 |
| 絵師・版権 | 絵師タグ（Danbooru カテゴリ 1、`@name`、`by name`）と版権・キャラタグを検出し、X 公開時の注意と、Anima の `@` 必須・RouWei の `by ` + BREAK 必須をチェック | Anima README、RouWei カード、`report/05` |
| ネガティブ | Illustrious: `nsfw` の有無、25 要素超の長さ。Anima: `sensitive, nsfw, explicit` と `artist name`、Aesthetic での `score_*` | WAI v17 カード、Anima README |

### 変換ルール（--convert-to）

| Illustrious → Anima | Anima → Illustrious |
|---|---|
| 品質ブロックを `masterpiece, best quality, score_7`（Aesthetic は score_7 なし）に置換。`very aesthetic` / `amazing quality` は削除 | `score_*` を削除し、末尾に `masterpiece, best quality, very aesthetic, absurdres, newest, general` を付与 |
| `general` → `safe`、ネガの `nsfw` → `sensitive, nsfw, explicit` | `safe` → `general`、ネガの `sensitive` / `explicit` は削除 |
| `anime screencap` → `anime screenshot`、別名を正規化、アンダースコアをスペースに | `anime screenshot` → `anime screencap`、`year 2025` → `newest` |
| `by name` → `@name`、BREAK は削除 | `@name` → `name` |
| 重み `(tag:1.2)` → `(tag:1.5)`（Anima は SDXL より強い値が必要。公式例 `(chibi:2)`） | 逆変換 |

### データファイル

- `data/danbooru_tags.csv` — [a1111-sd-webui-tagcomplete](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete) 同梱 `danbooru.csv`（2026-09-09 取得）を CSV ヘッダー付きで再配布。列: `name, category(0 一般 / 1 絵師 / 3 版権 / 4 キャラ / 5 メタ), post_count, aliases`。
- `data/bpe_simple_vocab_16e6.txt.gz` — [openai/CLIP](https://github.com/openai/CLIP) の BPE 語彙（MIT License）。

### 制約

- 投稿数は取得時点のスナップショット。Danbooru 本体（danbooru.donmai.us）の API は Cloudflare 保護のため本ツールからは参照しない。
- 75 トークン分割は A1111 の `comma_padding_backtrack=20` を「要素の手前で改チャンク」に単純化した近似。ComfyUI（`CLIPTextEncode`）はデフォルトで同様の 77 トークン分割を行うが、A1111 とは境界の扱いが少し異なる。
- Anima 側のトークン数（Qwen3 トークナイザ）は厳密には数えず、語数で 512 トークン基準の超過だけを警告する。

## check_embed.py

X の公式 oEmbed API で、投稿が「ログアウト閲覧者に表示できる状態か」を確認する（`report/06` §3.3）。

```bash
python3 tools/check_embed.py https://x.com/<user>/status/<id> [URL ...]
python3 tools/check_embed.py --detail https://x.com/<user>/status/<id>   # FxTwitter API の possibly_sensitive も表示
```

- `OK`: 埋め込み HTML が返る（制限なし）
- `RESTRICTED`: `Sorry, you are not authorized to see this status.` — 公開コードの `sensitive_viewer_logged_out` では「メディア付き かつ（NSFW_HIGH_PRECISION / NSFW_HIGH_RECALL ラベル、または 作者の `nsfw_user` / `nsfw_admin`、投稿の `nsfw.user` / `nsfw.admin`）」の投稿への応答
- `NOT_FOUND`: 削除・非公開・URL 誤り

`--detail` の `sensitive=True` は投稿の nsfw フラグ。作者の「センシティブなメディアとしてマーク」設定や投稿ごとの内容警告のほか、X がアカウント単位で付けた状態（`nsfw_admin`）も投稿時に引き継がれる。作者が何もしていないのに新規投稿が全件 True で、同じ画像が別アカウントでは False なら X 側のアカウント単位の状態（06 §3.3 結果 4）。`sensitive=False` で RESTRICTED なら、原因は分類器の投稿ラベルで、Under the Hood（x.com/i/under_the_hood）の投稿ラベル欄（NSFW_HIGH_RECALL / NSFW_HIGH_PRECISION / NSFW_ADMIN）とアカウントラベル欄（NsfwAdmin）で見分ける。

画像なし投稿が OK で画像付きが RESTRICTED なら、作者単位の状態が原因。設定変更後は新しい投稿で確認する（過去投稿のラベル・フラグは残る）。

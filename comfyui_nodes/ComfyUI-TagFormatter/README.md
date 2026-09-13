# ComfyUI-TagFormatter

Danbooru 形式のタグプロンプトを **カテゴリ順に並べ替え** / **キャラ要素を削除** するカスタムノード。
外部依存なし（Python 標準ライブラリのみ）。

## インストール
```bash
# ComfyUI/custom_nodes/ にコピー（またはシンボリックリンク）
cp -r comfyui_nodes/ComfyUI-TagFormatter <ComfyUI>/custom_nodes/
```
ComfyUI を再起動すると `utils/text` に **Tag Formatter (整形・キャラ要素削除)** が出ます。

## ノード
| 入力 | 内容 |
|---|---|
| `text` | 整形するプロンプト。ウィジェット直書きでも、右クリック → 入力に変換して STRING を繋いでも可 |
| `mode` | `reorder`（並べ替え） / `remove_character`（キャラ要素削除、順序維持） / `remove_character_and_reorder` |
| `remove_scope` | `appearance_and_name`（既定） / `appearance`（髪・目・肌・体型・種族） / `name`（キャラ名・作品名） |
| `remove_clothes` | 削除時に女服（衣装・装飾品）も一緒に削除（LoRA の既定衣装を出したいとき） |
| `dedupe` | 重複タグを最初の 1 つに（`long hair` と `long_hair`、`(long hair:1.2)` は同一扱い） |
| `group_separator` | 並べ替え時のカテゴリ間の区切り。`blank_line`（空行、既定）/ `newline` / `comma` |
| `keep_tags` | 削除しないタグ（カンマ区切り） |
| `extra_character_tags` | 追加で削除するタグ（カンマ区切り）。LoRA のトリガーワード等 |

| 出力 | 内容 |
|---|---|
| `text` | 整形後プロンプト → CLIPTextEncode の text（入力に変換）へ |
| `removed_tags` | 削除したタグ一覧（確認用。ShowText 等で表示） |
| `report` | カテゴリごとの振り分け結果（分類が意図と違うときの確認用） |

## 並び順
```
品質 → 女キャラ(人数) → 女キャラ(外見) → 女服 → 女表情 → 女ポーズ → 画角 → 男タグ
  → 場所 → シチュエーション・小物 → 時間 → 天候・季節 → 光 → 影 → 画風・効果 → 絵師 → LoRA → 不明 → 自然文
```
- 各カテゴリ内は元の順序を維持。カテゴリ間は既定で空行区切り（`group_separator`）
- どの辞書にも当たらないタグは「不明」として最後にまとめる（`report` 出力で確認して辞書に追加）
- `(tag:1.2)` `((tag))` `[tag]` の重み表記、`\(` `\)` エスケープはそのまま保持
- `BREAK` で区切られた塊は個別に整形
- 7 語以上の要素（Anima の自然文）は「自然文」として末尾にそのまま残す。タグ末尾の `.` も維持
- `1girl, solo` などの人数タグは「キャラ要素」として削除**しない**（LoRA 運用で消えると困るため）

## 「キャラ要素」の判定
- **外見**: `categories/girl_appearance.txt`（`* hair`, `* eyes`, `*bangs`, `* breasts`, `* ears`, `* tail`, 肌・体型・種族…）
- **名前**: `name (series)` 形式（例 `ganyu (genshin impact)`）は自動判定。それ以外のキャラ名・作品名は `categories/character_names.txt` に追記

## 分類辞書の編集
`categories/*.txt` を編集すると **ComfyUI を再起動せずに** 次回実行から反映されます（更新時刻を見て再読込）。

| 行の書き方 | 意味 |
|---|---|
| `long hair` | 完全一致（大小文字・`_`/スペースは同一視） |
| `re:.* hair$` | 正規表現で完全一致（`_` はスペースとして扱う） |
| `token:boy` | スペース/ハイフン区切りの単語に `boy` を含む |
| `# ...` | コメント |

判定の優先順（先に一致した方）: 品質 → 男 → 人数 → 画角 → 服 → 表情 → ポーズ → 外見 → キャラ名 → 絵師 → LoRA → 時間 → 天候 → 光 → 影 → シチュエーション → 場所 → 画風 → 不明。
「hair ribbon」は服、「closed eyes」は表情、「floating hair」はポーズ、といった衝突はこの順序で解決しています。

## ワークフローへの組み込み
`workflows/anima_t2i_hires_tagformatter.json` は Anima ワークフローの Positive の手前にこのノードを置いた版です
（Tag Formatter の `text` → CLIPTextEncode「Positive」の `text` 入力）。プロンプトは Tag Formatter 側に書きます。
`removed_tags` / `report` は必要に応じて ShowText 系ノードに繋いで確認してください。

## テスト
```bash
python3 comfyui_nodes/ComfyUI-TagFormatter/tests/test_tag_formatter.py
```

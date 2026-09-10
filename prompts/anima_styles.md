# Anima / JANIMA 画風プロンプト集（2026-09-10）

JANIMA（Civitai モデル 2642932）は「単一の画風を押し付けない」設計の Anima 派生で、**プロンプトだけで画風を大きく振れる**のが持ち味。ここでは JANIMA の事実関係と、Anima 系で効くことが裏付けられた様式語をまとめる。本環境では生成できないため、各語の根拠を明記し、JANIMA での最終確認は同梱の `workflows/anima_style_test.json`（同一 seed・8 様式の横並び）で行う。

## 0. JANIMA とは（Civitai モデルカード、2026-09-10 取得）

| 項目 | 内容 |
|---|---|
| 作者・ベース | janxd。**anima-base-v1.0 のファインチューン**（Base は「柔軟性・多様性・スタイル追従性が最大」の素のモデル） |
| 版 | **v1.0**（2026-06-10、3.9 GB）／ **v1.0 2.9B**（2026-09-08、bf16 5.44 GB・圧縮版 2.94 GB。「Anima-2.9B の新規層をマージし、2.9B の知識を保持」） |
| 実績 | DL 17,330・👍 1,911・👎 2（取得時点） |
| ライセンス | 生成画像の商用利用可（Image / RentCivit）、派生モデル不可、クレジット不要 |
| 配置 | `JANIMAAnima_v10.safetensors` → `models/diffusion_models`、`qwen_3_06b_base.safetensors` → `models/text_encoders`、`qwen_image_vae.safetensors` → `models/vae`（Anima と同じ） |
| 推奨設定 | **er_sde、CFG 5 前後、24〜30 steps**（Hires しないなら 50 まで）、解像度 512〜1536² |
| 品質タグ | `masterpiece, highres, absurdres, newest, best quality, score_7`（任意） |
| 推奨ネガ | `worst quality, low quality, lowres, score_1, score_2, score_3, blurry, jpeg artifacts, long fingers, sepia, bad anatomy, missing fingers, watermark, artist name` |
| 特徴（カード） | 「Anima の柔軟性を保ったまま、線・目・顔の精細さ、解剖、構図の一貫性を底上げ」「**単一の過学習した画風を強制しないので、LoRA や画風アダプタを重ねる土台として良い**」。作例は無加工 |
| 位置づけ（lilting.ch の派生 20 モデル比較） | 「主流のファインチューン」枠。**「素の Base・JANIMA・Hikari・SimpleAnima・RDBT は忠実系で、自分の LoRA やプロンプトに寄せやすい」**。逆に WAI-Anima とマージ系はモデル自身の絵柄を強く出す |

**2.9B 版について**: Anima-2.9B は CircleStone 公式ではなく Gazingstars123 による層拡張モデル（2026-08-12、28 層→40 層、追加 170 万枚、知識は 2026 年 7 月まで、preview 版で元の重みは凍結）。おーら氏の同一 seed 12 題比較（2.9B / Aesthetic v1.1 / Base）では、**彩度とコントラストが高い pixiv 投稿風、感情表現が強い**一方で、**色や素材の指示を誤読することがあり、露出寄りの衣装になりやすい**。全年齢運用では衣服タグを明示し、ネガの `sensitive, nsfw, explicit` を残す。Anima-2.9B 本体は「ComfyUI-Anima-2.9B カスタムノードが必要な場合がある」と記載があり、JANIMA 2.9B 版も同様の可能性がある（未確認）。2.9B 作者の助言: `highres` `absurdres` と**年代タグは影響が大きい**、`4k` `8k` `raytracing` は無意味、`cinematic composition` `dynamic angle` は有効、絵師タグは重み付きで混ぜられるが SDXL とは挙動が違う。

## 1. 画風プロンプトの置き方（Anima 系共通）

1. **位置**: `[品質 / 年代 / safe] → [様式語] → [1girl…] → [一般タグ] → 自然文`。108 枚同一 seed 比較はこの位置で行われた。
2. **一度に 1 系統**。混ぜると収束または混濁する（108 枚比較では steampunk / dieselpunk / solarpunk が同じ絵に収束。Hugging Face の議論 #112 では、複数の絵師タグや長いプロンプトで絵師の画風がぶれることが実測されている）。
3. **様式を確かめるときはタグを最小限に**。要素が多いと様式語が埋もれる。確定してから本番のタグを足す。
4. **年代タグは効きが強い**: `year 2025, newest` と `year 2015, old` で塗りと線が変わる。`masterpiece` と年代を入れると画風が安定しやすい（#112 の議論）。
5. **強調は SDXL より強く**: `(tag:1.5)`〜、公式例は `(chibi:2)`。`[tag]` は使わない。
6. **サンプラーも画風**（公式 README）: `er_sde` = 中立・平坦・シャープ、`dpmpp_2m_sde_gpu` = 多様で時に暴れる、`euler_ancestral` = 柔らかい線。
7. Aesthetic で試すときは `score_*` を全部外す。Turbo はネガが実質無効。
8. **dataset tag**（README）: 先頭行に `ye-pop` または `deviantart` と改行を置くと、非アニメ系のイラスト調（西洋絵画・抽象・DeviantArt 的）に寄る。

```
deviantart
Autumn Wanderer
masterpiece, best quality, 1girl, solo, cloak, forest, painterly. A lone traveler walks through golden birch trees, thick brush strokes and soft edges.
```

9. **絵師タグ**は `@name`（@ が無いとほぼ効かない）。探す場所: Anima Style Explorer（animastyles.thetacursed.com、42,509 名を Danbooru 投稿数付きで一覧、クリックで `@artist_name` をコピー）、anima.mooshieblob.com（4 万超）、Animadex（animadex.net、キャラ 3.6 万・絵師 1.5 万）、ComfyUI ノード `fulletLab/comfyui-anima-style-nodes`。**実在の絵師名を X の公開作品に使うのは、日本の界隈で最も反発の強い使い方**（`report/05` の NG 行動）。公開用の画風は年代・画材・様式語で作り、絵師タグは非公開の研究に留めることを勧める。

## 2. カタログ（そのまま貼る文字列）

記号: **◎** = Anima Base の 108 語同一 seed 比較で効果あり（おーら氏）／ **○** = Danbooru 投稿数 5,000 以上（学習量は十分、Anima での個別検証なし）／ **△** = 投稿数 300〜5,000（弱い可能性）／ **×** = 108 語比較で無効か逆効果。Danbooru タグはスペース区切り・小文字・括弧そのままの Anima 表記。投稿数は 2026-09-09 の tagcomplete DB。

### 2.1 年代・レトロ

| 文字列 | 根拠 | 出方の目安 |
|---|---|---|
| `retro artstyle, 1990s (style), 90s anime style` | ◎ / ○ 18,233 / ○ 9,369 | 90 年代セル画。太めの線、彩度低め、ハイライト少なめ |
| `1980s (style), 80s anime style` | ○ 5,665 / ◎ | 80 年代。髪の艶ハイライト、丸い目 |
| `2000s (style)` | ○ 6,831 | 00 年代デジタル塗り初期 |
| `retro anime style` / `VHS anime aesthetic` | ◎ | 上とほぼ同系。VHS は走査線・にじみ |
| `1970s (style)` | △ 915 | 劇画寄り。弱い |
| `pc-98 (style), pixel art, dithering` | △ 469 / ○ 20,049 / △ 1,442 | 16 色ディザ |
| ~~`vintage anime` `Showa anime` `Y2K anime`~~ | × | 効かない |

### 2.2 画材・技法

| 文字列 | 根拠 | 出方の目安 |
|---|---|---|
| `watercolor (medium), traditional media, watercolor painting style` | ○ 14,950 / ○ 87,193 / ◎ | にじみ・紙の白。風景付きの一枚絵になりやすい |
| `oil painting (medium), oil painting style` | △ 1,019 / ◎ | 厚塗り。技法の描き分けは弱い |
| `gouache painting style` / `digital painting style` | ◎ | 同上（108 枚比較では技法差は小さい） |
| `marker (medium)` | ○ 12,936 | コピック風のベタ |
| `colored pencil (medium)` | ○ 5,946 | 色鉛筆の粒 |
| `graphite (medium), sketch` + `pencil style` | ○ 10,717 / ○ 151,011 / ◎ | 鉛筆画。`sketch style` `line art` は × |
| `faux traditional media` | △ 3,595 | デジタルで紙質を再現 |
| `nib pen (medium)` | △ 1,378 | つけペン線 |
| ~~`impasto style` `ink wash painting style` `crayon`~~ | × | 無効・誤解釈 |

### 2.3 モノクロ・漫画・印刷

| 文字列 | 根拠 | 出方の目安 |
|---|---|---|
| `monochrome, greyscale` | ○ 631,227 / ○ 501,387 | 白黒 |
| `monochrome, greyscale, halftone, screentones, shoujo manga style` | ○ 13,406 / △ 2,754 / ◎ | 少女漫画のトーン。`shounen manga style` `golden age comic style` `charcoal drawing style` も ◎ |
| `spot color` | ○ 40,236 | 一部だけ色 |
| `partially colored` | ○ 13,381 | 塗りかけ |
| `limited palette` | ○ 17,163 | 2〜3 色 |
| `lineart` | ○ 11,439 | 線画のみ |
| `4koma` / `2koma` / `comic` | ○ 99,629 / ○ 27,842 / ○ 539,231 | コマ割り（吹き出しの文字は崩れる） |

### 2.4 配色・質感・レンズ

| 文字列 | 根拠 | 出方の目安 |
|---|---|---|
| `pastel colors, soft pastel style` | △ 2,807 / ◎ | 髪・服が淡い配色にまとまる。`pastel style` 単体は弱い |
| `muted color` | ○ 6,406 | くすみ |
| `high contrast` | △ 3,195 | 影が締まる |
| `film grain` | ○ 14,589 | 粒子 |
| `chromatic aberration` | ○ 24,284 | 色ずれ。**既定ネガに入っているので外す** |
| `sepia` | ○ 7,847 | **JANIMA 推奨ネガに入っているので外す** |
| `bloom` / `light particles` / `lens flare` | △ 3,970 / ○ 53,660 / ○ 38,902 | 光の演出（様式というより効果） |
| `flat color` / `anime coloring` | ○ 8,796 / △ 4,369 | × 108 枚比較では差が出ない（既定がアニメ塗り） |

### 2.5 装飾・ジャンル様式

| 文字列 | 根拠 | 出方の目安 |
|---|---|---|
| `art nouveau, art nouveau style` | △ 1,507 / ◎ | 曲線の装飾枠、ミュシャ風 |
| `vaporwave style` | ◎ | ネオン・グリッド（`vaporwave` タグは 249 件で弱いので自然語で） |
| `psychedelic art style` / `pop art style` / `gothic style` | ◎ | 配色が強く出る |
| `cyberpunk, cyberpunk style` | △ 3,323 / ◎ | ネオン都市 |
| ~~`steampunk` `dieselpunk` `solarpunk` `biopunk`~~ | × | 同じ出力に収束 |
| `ukiyo-e` / `nihonga` | △ 571 / △ 1,012 | 未検証。弱ければ `traditional media` と併用 |

### 2.6 メディア種別（メタタグ）

| 文字列 | 根拠 | 出方の目安 |
|---|---|---|
| `anime screenshot` | ○ 14,796 | セル画の画面キャプチャ風（Illustrious 派生では `anime screencap`） |
| `official art` / `game cg` | ○ 307,221 / ○ 66,079 | 公式絵・ゲーム CG の塗り |
| `key visual` / `promotional art` / `concept art` / `production art` | △ 2,127 / ○ 8,932 / ○ 5,946 / △ 2,155 | 宣伝ビジュアル・設定画 |
| `fake screenshot` | ○ 9,874 | UI 付きの画面風 |
| `magazine cover` / `album cover` / `poster (medium)` | △ 4,112 / ○ 6,139 / △ 1,592 | 文字入りレイアウト（文字は崩れる） |
| `chibi` | ○ 242,103 | 公式例は `(chibi:2)` |
| `toon (style)` / `western comics (style)` | △ 2,995 / △ 1,117 | 弱い |
| ~~`3D render` `Pixar-style 3D` `Live2D` `realistic` `3d`~~ | × | 実写化する。セミリアルは Illustrious 2.5D 派生で |

## 3. JANIMA で確定させる手順

1. `workflows/anima_style_test.json` を ComfyUI に読み込む（コアノードのみ）。左の「品質タグ」「本文」「ネガ」は共通、8 本の枝は `style` ノードの文字列だけが違い、seed は全枝固定。出力は各枝の画像と 4×2 の一覧（`output/Anima/style_test/`）。
2. まず既定の 8 様式（2.1〜2.5 から 1 つずつ）を回し、一覧で「本文と同じ構図のまま画風だけ変わったか」を見る。構図まで変わる語は強すぎるので `(tag:0.8)` に下げる。
3. `prompts/wildcards/anima_style.txt` から差し替えて 2 周目。効いた語は下の表に記録し、テンプレ（`prompts/anima_templates.md`）の様式列に反映する。
4. seed を 3 つ変えて再現するか確認してから採用する（1 seed の当たりは信用しない）。

| 様式 | 文字列 | 効き（○△×） | 構図への影響 | メモ |
|---|---|---|---|---|
| | | | | |

## 4. 出典

- Civitai: JANIMA（`civitai.com/models/2642932`、API 取得 2026-09-10）、Anima-2.9B（`civitai.com/models/2855007`）
- lilting.ch「Anima checkpoints: 20+ derivatives sorted by type and style」
- comfyui-wiki「Anima-2.9B: Layer-Expanded Anime Model」（2026-08-12）
- おーら「Anima で効く画風プロンプト 108 種の同一 seed 比較」（`note.com/ai_0049/n/n74ccab5370e0`）、「Anima の新モデル 2.9B の実力」（`note.com/ai_0049/n/nc625a544bfed`）
- circlestone-labs/Anima README（Hugging Face）、同 discussions #112（絵師タグの不安定性の分析と作者の返答）
- Anima Style Explorer（animastyles.thetacursed.com）、anima.mooshieblob.com、Animadex（animadex.net）
- Danbooru 投稿数: `tools/data/danbooru_tags.csv`（2026-09-09）

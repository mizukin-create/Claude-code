# 07. プロンプト最適化の一次資料検証（2026年9月9日）

前回（02・03・prompts/）は Civitai・Hugging Face・note・Danbooru への直接アクセスが遮断され、多くを検索要約に頼っていた。今回は一次資料に直接アクセスできたため、**前回の記述を一次資料と突き合わせ、誤り・古い情報・抜けを修正した**。修正はテンプレート（`prompts/`）と辞典（`prompts/tag_dictionary_verified.md`）、検証ツール（`tools/prompt_lint.py`）に反映済み。

取得した一次資料（すべて 2026-09-09 取得）:

| 資料 | 取得方法 | 用途 |
|---|---|---|
| Anima 公式 README | `huggingface.co/circlestone-labs/Anima/raw/main/README.md` | 03 の記法・設定の検証 |
| Anima Civitai モデルカード（版履歴付き） | Civitai API `models/2458426` | 版の公開日、CFG 推奨の差分 |
| WAI-illustrious v17 / Hassaku v3.4 / Nova Anime XL IL v19 / Prefect v8 / RouWei 0.8 / Illustrious XL 2.0 | Civitai API `models/{id}` | 02 の推奨設定・品質タグ・レーティング語彙の検証 |
| Danbooru タグ DB | a1111-sd-webui-tagcomplete `tags/danbooru.csv`（140,782 タグ）＋ Danbooru API で 12 タグを直接確認 | テンプレート・辞典の全タグ（338 語）の実在・別名・投稿数 |
| note「Anima で使える画風プロンプトはどれ？108 枚比較」（おーら、2026-07-12） | note API 本文 | Anima の様式タグの効き |
| docs.comfy.org Anima チュートリアル | 直接取得 | 公式ワークフローの構成 |
| Civitai 画像 API | `images?modelVersionId=` | 作例プロンプト（メタデータが非公開化されており取得不可） |

---

## 1. 結論（修正点の要約）

| # | 前回の記述 | 一次資料での事実 | 対応 |
|---|---|---|---|
| 1 | Hassaku の品質タグ `masterpiece, best quality, newest, absurdres, highres` | **Hassaku は `highres` 等のメタタグと作品名タグを学習していない**（カード明記）。CFG 3〜7、最良は CFG 6 ＋ Euler a。順序「人数 → キャラ → 残り」 | Hassaku 用は `masterpiece, best quality`（＋`newest`）に変更。作品名タグは入れない |
| 2 | WAI v17: Euler a / 30 step / CFG 7 | カード v17: **steps 15〜30、CFG 5〜7、Euler a、推奨ソフト Forge Neo、「1024×1024 より大きいサイズを使う」（作例は 1024×1344）**。Hires ×1.5 / 20 steps / R-ESRGAN 4x+ Anime6B / denoise 0.35〜0.5。**「品質・美的タグを積みすぎない、長いネガを使わない（ぼやける）」**。年齢調整は `(aged up:1.0–2.0)` `(mature female:1.0–2.0)` を先頭に | 共通設定を steps 25〜28 / CFG 6 のままとし、解像度の第一候補を 1024×1344 に変更。品質タグは 4〜5 個上限を明記 |
| 3 | WAI の 4 段階レーティング語彙は「要確認」 | **`general, sensitive, nsfw, explicit`**（カード）。「ユーザーが `nsfw` をネガに入れることを想定」 | 確定。00 §9 の要確認事項を解消 |
| 4 | Nova Anime XL: 背景込みの一枚絵に推奨 | **ライセンス: 「生成画像は無編集のまま商用利用不可（白黒化だけも不可）」**。ポジ `masterpiece, best quality, amazing quality, 4k, very aesthetic, high resolution, ultra-detailed, absurdres, newest, scenery, {prompt}, BREAK, depth of field, volumetric lighting`、ネガに `modern, recent, old, oldest` を置く流儀。IL v19（2026-05-12）は NoobAI EPS 1.1 ＋ Illustrious 2.0-stable ＋ ChenkinNoob の DARE マージ | 販売用（PicSpace / Patreon）には Nova を使わない、または加筆を前提にする注意を追加 |
| 5 | Prefect Illustrious XL v3 | 現行は **v8（2026-04-26）**。v7 で WAI v16 をマージ。ポジ `masterpiece, best quality, amazing quality, absurdres`、ネガ `bad quality, worst quality, worst detail, sketch, censored, watermark, signature, artist name`。Euler a / DPM++ 2M、CFG 5〜6、CLIP skip 1、ADetailer、4x-UltraSharp | 版を更新 |
| 6 | RouWei: 絵師タグは BREAK で別チャンク | 加えて **`by ` 接頭が必須**（無いと正しく動かない）。品質タグは `masterpiece, best quality` / `low quality, worst quality` の 4 つだけ。ネガは `worst quality, low quality, watermark` のみ。**`lowres` 等のメタタグは削除済みで使わない**。eps 版 CFG 4〜9（最良 7）、vpred 3〜5。解像度は 32 の倍数で約 1MP。Hires は latent ×1.5 ＋ denoise 0.6、または GAN ＋ 0.3〜0.55。データ打ち切り 2025 年 4 月末、13M 枚（4M 枚が自然文キャプション）。汎用スタイル語 `2.5d, anime screencap, bold line, sketch, cgi, digital painting, flat colors, smooth shading, minimalistic, ink style, oil style, pastel style`、booru 様式タグ `1950s〜2000s (style), animification, art nouveau, pinup (style), toon (style), western comics (style), nihonga, shikishi, minimalism` | RouWei 用の書式を 02 に追記。`tools/prompt_lint.py --model rouwei` で `by` と BREAK を検査 |
| 7 | Illustrious XL 2.0: 1536 基準 | カード: 「データセットは 2024-08 まで。**素の untuned base で、マージ・学習用**。自然文に強く、複数視点や崩壊が出にくい」。1536 の数値はカードには無い（テックブログ側） | 「派生モデルは 1024 級、本家 2.0 はマージ用」の記述を維持 |
| 8 | Anima: 記法・設定（03） | README と一致。追加事項: **「Danbooru と Gelbooru で表記が違うタグは Gelbooru 側を優先」**、**「まず Turbo から始めるのを勧める（Aesthetic より僅かに劣る程度で高速、安定性ではむしろ勝る場合も）」**、Aesthetic v1.0b は「スタイル調整 LoRA を混ぜていない素の美的 FT」で作者は 1.0 を推す。Civitai 版カードは **CFG 4〜6、Aesthetic は CFG 3 でも良い**。LoRA 学習は **LLM adapter を学習しない、rank 32 で LR 2e-5 から**（README 作者の diffusion-pipe 基準。03 の「sd-scripts は 1e-4」と併記） | 03 と `prompts/anima_templates.md` に追記 |
| 9 | Anima の版日付（03: 〜8/3 に Turbo v1.1 / Aesthetic v1.1 が流通） | Civitai 公開日: base-v1.0 → aesthetic-v1.0 / v1.0b → turbo-v1.0（2026-07-08）→ **aesthetic-v1.1（2026-07-13）→ turbo-v1.1（2026-08-24）** | 年表を更新（HF 側の公開日は別途要確認） |
| 10 | Anima の様式タグ: `retro artstyle, anime coloring, flat color` を推奨 | 108 枚比較（同一 seed）: **`cel shading` `flat color` はほぼ無効**（Anima はアニメ塗りが既定のため差が出ない）。**`90s anime style` `80s anime style` `retro anime style` `VHS anime aesthetic` は明確に効く**。`watercolor painting style` 等の画材系は「風景付きの絵画的一枚絵になる」効果で、技法の描き分けは弱い。`soft pastel style` `charcoal drawing style` `pencil style` `golden age comic style` `shoujo/shounen manga style`（モノクロ化）は安定。`3D render` `Live2D` は実写方向に誤変換。`Studio Ghibli style` `Pixar style` `art nouveau style` `vaporwave style` `gothic style` `cyberpunk style` `Arknights style` は強い。`steampunk / dieselpunk / solarpunk / space opera / biopunk` は同じ出力に収束 | Anima テンプレの様式節を書き換え（§5） |
| 11 | 02 §5 の ◆（Danbooru 実タグ）表示 | **`rim lighting` `cinematic lighting` `volumetric lighting` `soft lighting` `face focus` `looking away` `cel shading` `shiny hair` `glossy lips` は Danbooru タグではない**。`god rays`→`sunbeam`、`silver hair`→`grey hair`、`violet eyes`→`purple eyes`、`white blouse`→`white shirt`、`anime screencap`→`anime screenshot`（改名）等 12 語が別名 | テンプレ・ワイルドカードを正規表記に置換。辞典（`prompts/tag_dictionary_verified.md`）に投稿数を付記 |
| 12 | テンプレの長さ | CLIP 換算で ①顔アップ 87 トークン、③全身 96 トークン → **75 を超えて 2 チャンクに分割され、品質タグが第 2 チャンクに落ちている** | 各テンプレを 75 トークン以内に整理、または `BREAK` で品質タグを分離（§6） |
| 13 | Illustrious v3.6 のオープンウェイト | Hugging Face の OnomaAI 公開モデルは v0.1 / v1.0 / v1.1 / v2.0 まで。v3.x 系は公式サイト提供で **オープンウェイト配布は確認できず** | 00 §9 を更新（未公開扱い） |

---

## 2. Anima 公式 README との突き合わせ（03 の検証）

README（2026-09-09 時点）の要点と、03 との差分:

- **一致**: タグ順 `[quality/meta/year/safety] [1girl…] [character] [series] [artist] [general]`、小文字・スペース区切り（`score_*` のみアンダースコア）、推奨接頭 `masterpiece, best quality, score_7, safe,`、推奨ネガ `worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration`、`@絵師` 必須、Aesthetic は score_* 不使用、自然文は 2 文以上、キャラ名の後に外見を書く、重みは `(chibi:2)` 級、512〜1536px、30〜50 steps、CFG 4〜5、サンプラー er_sde / euler_a / dpmpp_2m_sde_gpu / euler、beta57（RES4LYF）で絵画調。
- **追加**: Gelbooru 表記優先（Danbooru と異なる場合）。Turbo を出発点に推奨。「Base は真のベースモデルで既定画風は極めて平坦（絵師タグ・品質タグ無しだと顕著）」。Dataset tag（`ye-pop` / `deviantart` を 1 行目に置く非アニメ画風の呼び出し）。Finetune: LLM adapter を学習しない、rank 32 で LR 2e-5 から。商用: 生成画像の販売・依頼は可、モデル自体のホスティング課金は不可（別途ライセンス）。
- **Civitai 版カードの差分**: 「30〜50 steps、CFG 4〜6。Aesthetic は CFG 3 のような低めでも良く、しばしばその方が良い」。

## 3. Illustrious 派生モデルカードとの突き合わせ（02 の検証）

§1 の表 #1〜#7 の通り。実務上の変更点だけ抜粋:

```
WAI v17   : 1024×1344（または 896×1152〜1024×1536）、Euler a、25〜28 steps、CFG 6、品質 4 個まで、ネガ短く、nsfw をネガに。Forge Neo 推奨
Hassaku   : masterpiece, best quality（メタタグ・作品名タグ無し）、CFG 6、Euler a、832×1216、ネガに signature。髪色が不安定なときは髪色タグを前方に
Nova v19  : 販売用途は加筆前提（ライセンス）。ネガに modern, recent, old, oldest（年代の逆指定）
Prefect v8: masterpiece, best quality, amazing quality, absurdres / CFG 5〜6 / ADetailer / 4x-UltraSharp
RouWei 0.8: by 絵師 BREAK 一般タグ。品質 2 語、ネガ 3 語、CFG 7（eps）、32 の倍数の約 1MP
```

## 4. Danbooru タグ検証（テンプレート・ワイルドカード・辞典の 338 語）

| 結果 | 語数 | 主な内容 |
|---|---|---|
| Danbooru 実タグ | 273 | そのまま使用可 |
| 別名（正規タグに置換） | 12 | `silver hair`→`grey hair`、`violet eyes`→`purple eyes`、`white blouse`→`white shirt`、`arms crossed`→`crossed arms`、`wide eyes`→`wide-eyed`、`god rays`→`sunbeam`、`street lamp`→`lamppost`、`rain boots`→`rubber boots`、`side by side`→`side-by-side`、`coffee cup`→（`cup, coffee`）、`anime screencap`→`anime screenshot`、`text`→`text focus`（ネガでは `text` のまま可） |
| モデル固有タグ（Danbooru 外だが有効） | 16 | `masterpiece` `best quality` `very aesthetic` `newest` `recent` `mid` `general` `safe` `nsfw` `sensitive` `explicit` `worst quality` `low quality` `year 2025` `score_7` `absurdres`（メタ） |
| 非タグ（自然語としてのみ効く） | 37 | `rim lighting` `cinematic lighting` `volumetric lighting` `soft lighting` `warm lighting` `face focus` `medium shot` `extreme close-up` `looking away` `gentle smile` `glossy lips` `shiny hair` `detailed eyes` `detailed background` `clean lineart` `cel shading` `dramatic shadow` `soft shadow` `golden hour` `blue hour` `morning light` `window light` `pale light` `wet street` `city street` `school gate` `festival stall` `fluorescent light` `miko outfit` `small figure` `standing on a hill` `thick painting` `spring` `afternoon` `depth` `long silver hair` `maple` |
| 投稿数 300 件未満（弱い） | 5 | `long shadow`（66）`golden hour`（158）`impasto`（225）`dim lighting`（287）`extra digits`（303、ネガ用） |

Danbooru API を直接叩いて確認できた投稿数（2026-09-09、DB スナップショットより新しい値）: `backlighting` 45,589 / `anime_coloring` 56,532 / `retro_artstyle` 24,597 / `1990s_(style)` 13,118 / `dappled_sunlight` 15,128 / `absurdres` 2,985,697。`anime_screencap` は投稿数 0（`anime_screenshot` へ改名済み）、`masterpiece` `general` は「非推奨タグ・0 件」= モデル固有語であることを確認。以降の一括照会は Cloudflare に遮断されたため、残りは DB スナップショット値。

`anime screencap` → `anime screenshot` の改名時期は未確認。Illustrious v0.1（Danbooru2023 ベース）系の派生は旧名で学習している可能性が高く、**Illustrious 派生は `anime screencap`、NoobAI/RouWei（2025 年データ）と Anima は `anime screenshot`** を第一候補にし、両方を X/Y/Z で試すのが安全。

## 5. Anima の様式タグ（note 108 枚比較の要点）

実験条件: ComfyUI 公式テンプレ「Anima Base v1」、seed 固定、`masterpiece, best quality, score_7, safe, [style], 1girl, solo, outerwear, skirt` という最小構成。

| 判定 | 語（`〜 style` 表記） | 00 §3.2 の様式候補への含意 |
|---|---|---|
| 強い（配色・小物・キャラデザまで変わる） | Studio Ghibli, Pixar, Spider-Verse, Akira Toriyama, Arknights, art nouveau, vaporwave, psychedelic art, pop art, gothic, cyberpunk, low poly 3D, golden age comic, charcoal drawing, shoujo/shounen/seinen manga（モノクロ化）, soft pastel, 90s anime, 80s anime, retro anime, VHS anime aesthetic | **候補 1「レトロアニメ」は Anima でも `90s anime style` / `retro anime style` / `VHS anime aesthetic` で成立**。加えて `soft pastel style` は「淡い配色」の署名様式として有力 |
| 中間（背景が絵画的になる等の部分反応） | digital painting, watercolor painting, oil painting, gouache painting, impressionism, film noir, Tim Burton, surrealism, minimalist, art deco, retrofuturism, Korean manhwa | **候補 2「水彩」は Anima 単体では『風景付きの絵画調』止まりで技法の描き分けが弱い** → 水彩感は Illustrious（`watercolor \(medium\), traditional media`、14,950 / 87,193 件）か、Anima → Illustrious 二段で出す |
| 無効（差が出ない） | cel shading, flat color illustration, sketch, line art, crayon, impasto, Y2K anime, vintage anime, Showa anime, chibi, mecha, magical girl, moe, kawaii, ukiyo-e, Bauhaus, game CG, VTuber illustration, visual novel, gacha game, Genshin Impact, Fate/Grand Order, Trigger, Kyoto Animation, Sunrise mecha | 03・anima_templates の「フラット・ポスター」節（`flat color`）は Anima では効果薄 → 削除して Illustrious 側の `flat color`（8,796 件）に一本化 |
| 誤変換（別方向に飛ぶ） | 3D render / Pixar-style 3D / Live2D（実写化）, ink wash painting（カラー風景化）, classic Disney / old cartoon（現代カジュアル化）, Otomo / Anno（別画風） | **候補 3「セミリアル」を Anima で `3D` `render` `realistic` 系の語で狙うと実写化する**。セミリアルは Illustrious 2.5D 派生（Nova Anime3D 等）で作る |
| 抑制される | hentai, erotic, porn, ecchi 等 | `safe` ＋ ネガの safety タグが有効に働いている証拠 |

記事の総括: 「色彩とモチーフの両方に紐づく語は強い」「色情報を落とす語は安定」「アニメの基本塗りを指す語は無効」「体型変形・小物追加を要する語は弱い」「抽象的な複合ジャンル語は同じ出力に収束」。**プロンプトを最小構成に削らないと様式の差が見えない**（要素が多いとタグドロップアウトで末尾の様式語が埋もれる）という手順上の教訓も重要。

## 6. テンプレートの 75 トークン問題

`tools/prompt_lint.py` の CLIP 換算で、前回テンプレは ①顔アップ 87、②バストアップ 80、③全身 96、④背景 77 トークン。A1111 は 75 トークンごとにチャンク分割し後ろほど影響が薄いので、**末尾に置いた品質タグ・レーティングが第 2 チャンクに落ちていた**。対策は 2 つ:

1. 20〜28 タグに削る（`prompts/illustrious_templates.md` の改訂版はすべて 75 以内）。
2. 意図的に `BREAK` で分け、第 1 チャンク＝キャラ固定文＋構図、第 2 チャンク＝背景・光・様式・品質、とする（RouWei は絵師タグを第 3 チャンクに）。

## 7. 参照

- https://huggingface.co/circlestone-labs/Anima（README）
- https://civitai.com/models/2458426 （Anima）/ 827184（WAI）/ 140272（Hassaku）/ 376130（Nova Anime XL）/ 1224788（Prefect）/ 950531（RouWei）/ 1369089（Illustrious XL 2.0）— Civitai API v1 で取得
- https://github.com/DominikDoom/a1111-sd-webui-tagcomplete （`tags/danbooru.csv`）
- https://danbooru.donmai.us/tags.json （直接確認 12 語）
- https://note.com/ai_0049/n/n74ccab5370e0 （Anima 108 スタイル比較）
- https://docs.comfy.org/tutorials/image/anima/anima

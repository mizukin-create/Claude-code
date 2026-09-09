# 02. Illustrious XL プロンプト技術・設定 徹底調査（2026年9月時点）

> **第 2 回追記（2026-09-09）**: 本レポートの記述をモデルカード（Civitai API）と Danbooru タグ DB で検証し、13 項目を修正した。修正一覧は `report/07_prompt_verification.md` §1、修正済みテンプレは `prompts/illustrious_templates.md`。主な修正: Hassaku はメタタグ・作品名タグを学習していない／WAI v17 は 1024×1344 推奨・品質タグ 4〜5 個上限・レーティング `general/sensitive/nsfw/explicit`／Nova Anime XL は無編集出力の商用利用不可／RouWei は `by ` 接頭＋BREAK 必須／Prefect は v8／§5 の `rim lighting` `cinematic lighting` `face focus` 等は Danbooru タグではなく、`silver hair`→`grey hair`、`violet eyes`→`purple eyes`、`anime screencap`→`anime screenshot`（改名）が正規表記。


> 調査メモ: 検索 44 回。note.com / Civitai / HF / SeaArt / Reddit / X の本文は直接取得できず、検索要約から抽出。GitHub（README・Wiki）のみ本文確認。信頼度 ★=一次資料本文確認 / ☆=検索要約経由 / △=一般知見・経験則。

## 1. Illustrious XL の系譜と現行バージョン

| 版 | 公開 | 学習/基準解像度 | 予測方式 | 特徴 | 出典 |
|---|---|---|---|---|---|
| v0.1 (early release) | 2024/09 | 1024 基準（832×1216 等） | eps | Danbooru 約 7.5M 枚。WAI/Hassaku 等ほぼ全ての人気派生の土台 | [HF v0](https://huggingface.co/OnomaAIResearch/Illustrious-xl-early-release-v0) / [arXiv 2409.19946](https://arxiv.org/abs/2409.19946) |
| v1.0 / v1.1 | 2025/02 | 1536×1536 ネイティブ（512〜1536、1248×1824 も可） | eps | タグ＋自然言語のハイブリッド | [HF v1.0](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v1.0) / [Civitai v1.0](https://civitai.com/models/1232765/illustrious-xl-10) / [SeaArt](https://www.seaart.ai/articleDetail/cvcdnn5e878c73fqe0s0) |
| v2.0 (Stable) | 2025/03 | 512〜2048、推奨 1536 基準 | eps | 20M 枚・1536 学習。「LoRA 学習に最適」「自然文が少し効く」 | [Civitai v2.0](https://civitai.com/models/1369089/illustrious-xl-20) / [SeaArt v2.0](https://www.seaart.ai/articleDetail/cvceb6le878c73bckfig) / [DigiAlps](https://digialps.com/finally-illustrious-xl-unveils-new-names-stable-v2-release/) |
| v3.0 | 2025/04 | 2048×2048 ネイティブ | eps | 自然文理解と物体分離が向上 | [Shakker v3.0](https://www.shakker.ai/modelinfo/f125113915584517a862c9a4a2a1d583/Illustrious-XL-v3-0) / [3.0-3.5 解説](https://neverbiasu.github.io/posts/reprints/illustrious-xl-3.0-3.5-vpred-2048-resolution-and-natural-language.html) |
| v3.5-vpred | 2025/05 | 256〜2048 | v-prediction + ZTSNR | 色制御トークン復活、自然文・指示追従が大幅向上 | [SeaArt v3.5-vpred](https://www.seaart.ai/models/detail/40217d3a4243c870589707a95fe350a0) / [illustriousxl.org](https://illustriousxl.org/) |
| v3.6 | 2025/07/14 | — | — | 公式プラットフォーム上で提供。オープンウェイト配布の有無は未確認 | [公式 updates](https://www.illustrious-xl.ai/updates) / [v3.6](https://www.illustrious-xl.ai/updates/29) |
| Illustrious-Lumina v0.03 | 2025 春 | — | DiT | Gemma-2-2b 必要、長い自然文推奨。A1111/Forge 非対応 | [GitHub](https://github.com/OnomaAI/Illustrious-Lumina) |

- 2026 年に入ってからの新しい SDXL ベース公式版は確認できず。
- 実務上の注意: 人気派生モデル（WAI, Hassaku, Nova, Prefect 等）は v0.1〜v1 系がベースで、1024 級（832×1216 等）を推奨。ベース版の 1536/2048 推奨をそのまま派生に適用すると破綻しやすい。

### v-pred モデルの扱い
| UI | 設定 |
|---|---|
| reForge | Noise schedule for sampling = Zero Terminal SNR を手動 ON。RescaleCFG 内蔵。CFG++ あり（[robai104](https://note.com/robai104/n/n7a4801fb422c) / [reForge](https://github.com/Panchovix/stable-diffusion-webui-reForge)） |
| Forge (lllyasviel) | v_pred / ztsnr キーを自動検出。RescaleCFG は非内蔵（[Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)） |
| Forge Neo | v_pred 検出、ztsnr 対応、RescaleCFG 内蔵、MaHiRo CFG、Epsilon Scaling（[Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)） |
| 共通推奨 | CFG 3.5〜5（Rescale CFG 0.5〜0.7）、Euler / Euler a、28〜35 step、Beta スケジューラ回避（[Obsession](https://civitai.com/models/820208/obsession-illustrious-xl) / [NoobAI vpred](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0) / [RouWei 0.8](https://huggingface.co/Minthy/RouWei-0.8)） |

## 2. 人気の派生モデル（2026 年時点）と SFW 美少女適性

| モデル | 傾向 | 推奨設定（カード準拠） | SFW 適性 | 出典 |
|---|---|---|---|---|
| WAI-illustrious-SDXL v17 | 万能・安定。v17 でプロンプト安定性改善。4 段階レーティングタグ対応 | Euler a / 30 step / CFG 7（5〜7）/ 832×1216。品質タグは末尾に `masterpiece, best quality, amazing quality`、ネガ `bad quality, worst quality, worst detail, sketch, censor`。SFW ではネガに `nsfw` 必須 | ◎ | [Anifusion](https://anifusion.ai/models/wai-illustrious/) / [lilting v17](https://lilting.ch/en/articles/wai-illustrious-v17-review) / [CivArchive](https://civarchive.com/models/827184?modelVersionId=2883731) |
| Hassaku XL (Illustrious) v3.4 | 明るく鮮やか、構図安定 | Euler a / 28 step / CFG 6 / 832×1216。ポジ `masterpiece, best quality, newest`、ネガ `worst quality, bad quality`。順序「人数 → キャラ名 → 属性」 | ◎ | [Civitai](https://civitai.com/models/140272/hassaku-xl-illustrious) / [Anifusion](https://anifusion.ai/models/hassaku-xl/) / [OfflineCreator](https://offlinecreator.com/civitai/illustrious-xl-nsfw-models-2026) |
| Prefect Illustrious XL v3 | バランス型・見せ絵向き | Euler a or DPM++ 2M / CFG 5〜6 / CLIP skip 1。ポジ `masterpiece, best quality, amazing quality, absurdres`、ネガ `bad quality, worst quality, worst detail, sketch, censored, watermark, signature, artist name` | ◎ | [Civitai](https://civitai.com/models/1224788/prefect-illustrious-xl) |
| NoobAI-XL EPS 1.1 / V-Pred 1.0 | 絵師タグが極めて強い、v-pred は色域広い | ポジ `masterpiece, best quality, newest, absurdres, highres, safe`、ネガ `nsfw, worst quality, old, early, low quality, lowres, signature, username, logo, bad hands, mutated hands, mammal, anthro, furry, ...`。V-Pred は Euler 限定、CFG 4〜5、ZTSNR 必須 | ○ | [HF](https://huggingface.co/Laxhar/noobai-XL-Vpred-1.0) / [noobaixl.org](https://noobaixl.org/) / [nobin](https://note.com/nobinlog/n/n5ace3610bd6a) |
| Nova Anime XL IL v19 | 鮮やか、背景込みの一枚絵に強い | Euler a / 20〜30 / CFG 4〜6。ポジ `masterpiece, best quality, amazing quality, very aesthetic, high resolution, ultra-detailed, absurdres, newest, scenery, depth of field, volumetric lighting`、ネガ `3d, jpeg artifacts, username, watermark, signature, normal quality, worst quality, large head, low quality, text, error, missing fingers, extra digits, fewer digits, bad eye` | ◎ | [Civitai](https://civitai.com/models/376130/nova-anime-xl) |
| Ikastrious v11.1 / Classic | 線くっきり・色鮮明 | Euler a / 20〜40 / CFG 5〜7 / Hires ×1.5。ポジ `general, masterpiece, best quality, anime coloring` | ○ | [Civitai](https://civitai.com/models/874216) |
| RouWei 0.8 | プロンプト追従が最強クラス、タグ＋自然文混在に最適化。品質タグは 4 つだけ有効。絵師タグは BREAK で別チャンク | Euler a / 20〜28 / CFG 4〜8 (eps)・3〜5 (vpred) | ◎ | [HF](https://huggingface.co/Minthy/RouWei-0.8) / [Civitai](https://civitai.com/models/950531/rouwei) |
| Raehoshi illust XL | 上品な塗り | CFG 5〜6 / 28。ポジ `masterpiece, best quality, very aesthetic`、ネガ `lowres, bad quality, worst quality, very displeasing, bad anatomy, sketch, jpeg artifacts, signature, watermark` | ◎ | [HF](https://huggingface.co/Raelina/Raehoshi-illust-XL) |
| Animagine XL 4.0 | テンプレ `1girl, キャラ, 作品名, rating, その他, 品質` | Euler a / CFG 5〜7 | ◎ | [HF](https://huggingface.co/cagliostrolab/animagine-xl-4.0) / [ガイド](https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update) |
| v-pred マージ群 | IllumiYume XL v3.5(v-pred), Obsession v-pred, LuminarQMix vPred, Solvent Eclipse | | ○ | [IllumiYume](https://civitai.com/models/1308285/illumiyume-xl-illustrious) |

- 比較記事: [Hundreds of Lulus](https://civitai.com/articles/19484/hundreds-of-lulus-evaluating-and-scoring-illustrious-checkpoints-1-20-sfw-ish) / [TechTactician 8 選](https://techtactician.com/best-illustrious-xl-sdxl-anime-model-fine-tunes-comparison/)
- SFW 美少女の第一候補: 安定重視 → WAI v17、明るい塗り → Hassaku v3.4、背景込み → Nova Anime XL、上品 → Raehoshi / Prefect、構図操作 → RouWei 0.8。

## 3. プロンプト構造の最適解

### 3-1. 品質タグ・年代・レーティング・美的タグ
- 有効な品質タグ: `masterpiece, best quality, very aesthetic, absurdres` の 4 つ（[WhatLab](https://whatlab.ai/guides/illustrious-prompting-guide)）。派生は `amazing quality`、`newest` を加える。階層 masterpiece > best quality > high/good quality > normal > low > worst（[EasyNoobai](https://github.com/regiellis/ComfyUI-EasyNoobai/blob/main/README.md) / [SeaArt NoobAI](https://docs.seaart.ai/guide-1/6-permanent-events/high-quality-models-recommendation/noobai-xl)）。
- 美的タグ: `very aesthetic`、`very awa` / `worst aesthetic`（NoobAI 由来）。
- 年代タグ: `newest`(2021–24) / `recent`(2018–20) / `mid`(2014–17) / `early`(2011–13) / `old`(2005–10)。末尾でも画風・線の太さが変わる（[Qpipi](https://www.qpipi.com/forum-post/104855/) / [みし](https://note.com/mith_mmk/n/ne0a15d59db81)）。`1990s (style)` も併用可。
- レーティング: `general / sensitive / questionable / explicit`（[Danbooru](https://danbooru.donmai.us/wiki_pages/howto:rate)）。NoobAI/Animagine は `safe`。SFW ではポジに `general`（NoobAI 系は `safe`）＋ネガに `nsfw`。
- 置き場所: 先頭派と末尾派が併存。最初の 75 トークン内に収まっていることが重要。品質タグの有無で顔や塗りまで変わる（[nobin](https://note.com/nobinlog/n/nd7e8575d6d5b) / [Amanesse](https://note.com/nobinlog/n/n333099ed58a7)）。
- 日本語圏の定番順序: スコア → レーティング → 年代 → キャラ要素 → 背景・演出（[SeaArt 基礎](https://www.seaart.ai/articleDetail/d182kg5e878c738uh03g) / [kazumu #1](https://note.com/kazumu/n/n6390a899bdce) / [kazumu #2](https://note.com/kazumu/n/ncc4ce895200c)）。

### 3-2. Danbooru タグの並び・表記・数
```
[人数/構図] 1girl, solo
[キャラ/作品] hatsune miku, vocaloid
[外見] long hair, twintails, aqua hair, aqua eyes, hair between eyes
[服・小物] school uniform, pleated skirt, thighhighs, hair ribbon
[ポーズ/動作] standing, hand on own hip, looking at viewer
[表情] light smile, parted lips, blush
[背景/場所/時間] classroom, window, sunset, indoors
[光/効果] backlighting, dappled sunlight, lens flare
[画角/被写界深度] cowboy shot, from below, depth of field
[画風/絵師] anime screencap  /  BREAK artist tags
[品質/年代/レーティング] masterpiece, best quality, very aesthetic, absurdres, newest, general
```
- アンダースコア: 空白表記が標準。括弧付きタグは `1990s \(style\)` とエスケープ（[tagcomplete](https://github.com/DominikDoom/a1111-sd-webui-tagcomplete)）。
- タグ数: 20〜40 タグ。75 トークンごとにチャンク分割。チャンクをまたぐタグは意味が切れる。`BREAK` で強制改チャンク（[A1111 Wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features)）。後ろのタグほど薄まる。
- Illustrious は体位タグより「ポーズタグ＋一般タグ」の組み合わせが安定。

### 3-3. 絵師タグとスタイルミックス
- Illustrious は多数の絵師タグをネイティブに認識（[Artist Style Tags](https://civitai.com/articles/21827/playing-with-illustrious-artist-style-tags) / [Yet Another](https://civitai.com/articles/16938/yet-another-exploration-of-illustrious-styles) / [Common style tags](https://civitai.com/articles/25464/common-style-tags-recognized-by-illustrious-anima-and-other-danbooru-based-models)）。[Style Explorer](https://www.localainews.co/news/tools/conquer-16000-tags-with-illustrious-noobai-style-explorer-by-thetacursed/)。
- `by xxx` 形式: NoobAI では効く。Illustrious は Danbooru タグ名そのまま。
- 混合の実例（RouWei）: 絵師タグは別 CLIP チャンク。`... BREAK (artist_a:0.7), (artist_b:0.5), (artist_c:0.4)`。2〜3 人を 0.4〜0.8 で混ぜると独自の塗り。
- 倫理: Civitai の通報制度（[Civitai](https://civitai.com/content/art-and-ai) / [discussion](https://github.com/orgs/civitai/discussions/114)）。X 投稿では存命絵師名を単独で使わない／プロンプトに絵師名を出さない／ブレンドや年代タグ・画風タグで代替が無難。

### 3-4. 自然言語プロンプトの併用
- v1.0: ハイブリッド対応。v2.0: 少し効く。v3.5-vpred: 大幅向上。RouWei: 混合が最良。
- 実践: 骨格は Danbooru タグ、関係性・位置だけ短い句で補う。v0.1 ベースの派生は自然文の効きが弱い（[kazumu](https://note.com/kazumu/n/nfad555d5efcd)）。

### 3-5. ネガティブプロンプト
- 定番: `worst quality, low quality, lowres, bad anatomy, bad hands, extra digits, fewer digits, jpeg artifacts, signature, watermark, username, text, blurry`
- 減らす派: Illustrious はネガに敏感 → 短く始めて足す（[れん](https://note.com/ren_ai_coach/n/n2fb066b01801) / [ImageToPrompt](https://www.imagetoprompt.dev/blog/negative-prompts-stable-diffusion/)）。RouWei は 2 つのみ。EasyNegative 等は SDXL では逆効果。
- SFW では `nsfw` をネガに。

### 3-6. 強調構文・Dynamic Prompts
- `(tag:1.2)`、`[tag]`、`[a:b:step]`、`[a|b]`。1.1〜1.3 が実用域、1.5 超は壊れやすい。
- Dynamic Prompts: `{a|b|c}`、`__wildcard__`（[sd-dynamic-prompts](https://github.com/adieyal/sd-dynamic-prompts) / [nobin](https://note.com/nobinlog/n/nb8e004b3412e)）。

## 4. 生成設定

| 項目 | 推奨 | 根拠 |
|---|---|---|
| サンプラー | Euler a（既定）。DPM++ 2M (Karras)、DPM++ 2M SDE | [aiofm](https://aiofm.info/en/guides/samplers-compared) / [Civitai](https://civitai.com/articles/7484/understanding-stable-diffusion-samplers-beyond-image-comparisons) |
| ステップ | 20〜30（25〜28）、v-pred 28〜35 | |
| CFG | eps 5〜7、LoRA 併用時 3.5〜5、v-pred 3.5〜5 + Rescale 0.5〜0.7 | [news-knowledge](https://www.news-knowledge.com/wp/illustrious-sdxl-best-practices-2026) / [Think AI](https://think-ai.tokyo/archives/347) |
| 解像度 | 832×1216（X 向け定番）、896×1152、1024×1024、1216×832。v1/v2 ベースなら 1024×1536 | |
| Hires.fix | 倍率 1.5（〜2.0）、denoise 0.35〜0.5、Hires steps 10〜15。R-ESRGAN 4x+ Anime6B / 4x-UltraSharp / 4x_NMKD-Siax・Remacri。Latent 系は 0.55 以上 | [レベルマ](https://note.com/levelma/n/nfd4599645183) / [ururu](https://ururuailab.com/sd-high-quality-guide/) |
| ADetailer | face_yolov8n/s denoise 0.3〜0.45、hand_yolov8n 0.3〜0.4、mediapipe_face_mesh_eyes_only。confidence 0.3、min mask ratio 0.01。ADetailer プロンプトは短く形状のみ | [adetailer](https://github.com/Bing-su/adetailer) / [れん](https://note.com/ren_ai_coach/n/n0891ca169727) / [nobin](https://note.com/nobinlog/n/nd182abc9ee00) |
| CLIP skip | 1 | [SD.Next](https://github.com/vladmandic/sdnext/wiki/CLiP-Skip) |
| FreeU | b1 1.3 / b2 1.4 / s1 0.9 / s2 0.2。アニメは b1 1.1 / b2 1.2 から | [FreeU](https://github.com/ChenyangSi/FreeU) |
| PAG / SAG | PAG scale 2〜3 で CFG を 3〜5 に | [sd-perturbed-attention](https://github.com/pamparamm/sd-perturbed-attention) / [incantations](https://github.com/v0xie/sd-webui-incantations) |
| Kohya Deep Shrink | block 3 / downscale 2.0 / end 0.35 | [ComfyUI](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_model_downscale.py) / [kohya-hiresfix](https://github.com/wcde/sd-webui-kohya-hiresfix) |
| 色補正 | [Vectorscope CC](https://github.com/Haoming02/sd-webui-vectorscope-cc)、[Dynamic Thresholding](https://github.com/mcmonkeyprojects/sd-dynamic-thresholding) | |
| LoRA | 重み 0.6〜0.8、キャラ 0.7〜0.9 / 画風 0.4〜0.7 | [nobin](https://note.com/nobinlog/n/n9ecb41ba5347) |
| Regional Prompter / Forge Couple | RP: `共通 ADDCOMM 左 BREAK 右`。Forge Couple: 行ごとに領域、Global Effect 行に画風、各領域でも総人数を先に、空行禁止 | [RP](https://github.com/hako-mikan/sd-webui-regional-prompter) / [Forge Couple](https://github.com/Haoming02/sd-forge-couple) / [なないろ](https://note.com/nonb0716/n/n02ce7117ac22) / [nobin](https://note.com/nobinlog/n/n7ae9dbb093de) |
| ControlNet | xinsir（canny/openpose/scribble-anime/union）、Kataragi（lineart/line2color/recolor/inpaint）、bdsqlsz（lineart-anime, tile-anime）、kohya controllllite、TTPlanet tile、[CNXL anytest v4](https://civitai.com/models/136070/controlnetxl-cnxl)。IP-Adapter は ip-adapter-plus_sdxl_vit-h / plus-face を scale 0.5 前後 | [DCAI](https://www.digitalcreativeai.net/en/post/detailed-guide-a1111-webui-controlnet-sd15-sdxl) / [Mikubill](https://github.com/Mikubill/sd-webui-controlnet/discussions/2039) / [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter) |

## 5. 「魅力的に見せる」ためのタグ集（◆=Danbooru 実タグ、◇=非 Danbooru だが実効あり）

| 分類 | タグと効果 |
|---|---|
| 光 | ◆backlighting ◆rim lighting ◆sidelighting ◆dappled sunlight ◆light rays ◆sunbeam ◇god rays ◆lens flare ◆sunlight ◆sunset ◆neon lights ◆glowing ◆light particles ◆bloom ◇cinematic lighting ◇volumetric lighting ◇soft lighting。[SeaArt Tips](https://www.seaart.ai/articleDetail/csmspt99c71s73dqk2mg) / [AutoWeeb](https://autoweeb.com/blog/best-ai-anime-lighting-prompts-cinematic-soft-neon-and-emotional-scenes) / [Aiarty](https://www.aiarty.com/stable-diffusion-prompts/stable-diffusion-lighting-prompts.htm)。[Dramatic Lighting Slider](https://www.diffus.me/models/dramatic-lighting-slider-illustrious-v1-0) |
| 色 | ◆pastel colors ◆limited palette ◆monochrome+◆spot color ◆high contrast ◆chromatic aberration ◆film grain ◆colorful ◆gradient background |
| 画角 | ◆from below ◆from above ◆from side ◆from behind+◆looking back ◆dutch angle ◆fisheye ◆close-up ◆foreshortening ◆wide shot ◆cowboy shot ◆upper body ◆portrait ◆face focus ◆eye focus ◆pov ◆dynamic pose |
| 被写界深度 | ◆depth of field ◆bokeh ◆blurry background ◆blurry foreground ◆motion blur |
| 表情 | ◆light smile ◆half-closed eyes ◆looking at viewer ◆parted lips ◆blush ◆closed mouth ◆smug ◆embarrassed ◆head tilt ◆looking to the side ◆:d ;) ◆tears ◆sleepy ◆hand on own cheek ◆finger to mouth |
| 質感 | ◇detailed eyes ◆glossy lips ◆shiny skin ◆wet ◆see-through ◆translucent ◆shiny hair ◆sparkle ◆floating hair+◆wind |
| 画風 | ◆anime screencap ◆retro artstyle ◆1990s \(style\) ◆flat color ◆watercolor \(medium\) ◆traditional media ◆faux traditional media ◆sketch ◆impasto ◆official art ◆key visual ◆game cg ◆pixel art ◆cel shading ◆lineart ◆monochrome ◆greyscale |

## 6. よくある失敗と対策

| 症状 | 対策 |
|---|---|
| 手の破綻 | ADetailer hand_yolov8n denoise 0.3〜0.4、手を隠すポーズ、Hires.fix、修正 LoRA（[Novapen](https://note.com/novapen_create/n/n6921b1a28325) / [目・指 LoRA](https://note.com/novapen_create/n/n31a1d624c7ce)）、openpose 手 CN or inpaint |
| 目の左右差・ボケ | mediapipe_face_mesh_eyes_only、Hires 1.5×、ネガ blurry eyes（[Quesman](https://quesman-coder.com/2025/07/22/stable-diffusion-illustrious-tips-techniques/)） |
| 複数人の混線 | Regional Prompter / Forge Couple、共通行 2girls + 各領域 1girl、属性を短く（[Hakky](https://book.st-hakky.com/en/data-science/stable-diffusion-multiple-poses-prompts) / [gosuloli](https://gosuloli.com/archives/1103)） |
| 背景がぼやける | depth of field を外し scenery, wide shot、Hires denoise 0.4 以上、depth CN |
| 色が濁る | ZTSNR ON + Rescale CFG、CFG 4〜6、ネガ短縮、Vectorscope CC |
| プロンプト無視 | 重要タグを先頭 75 トークン内、BREAK、(tag:1.2)、正式表記 |
| AI っぽさ | shiny skin/very aesthetic の積みすぎを避ける、film grain/flat color/年代タグ/traditional media、絵師ブレンド、CFG 4〜5、個性づけ（mole under eye, thick eyebrows, asymmetrical bangs, tareme/tsurime）（[くろくまそふと](https://kurokumasoft.com/2023/05/09/howto-remove-ai-like-style/) / [肌質](https://note.com/legal_pansy7543/n/n5c9fac29fb5d)） |

## 7. 実例プロンプト（出典付き・12 例）
1. WAI v17: ポジ `1girl, solo, <外見・服・背景>, masterpiece, best quality, amazing quality` / ネガ `bad quality, worst quality, worst detail, sketch, censor, nsfw` / Euler a, 30, CFG 7, 832×1216
2. Prefect v3: ポジ `masterpiece, best quality, amazing quality, absurdres, 1girl, ...` / ネガ `bad quality, worst quality, worst detail, sketch, censored, watermark, signature, artist name`
3. Nova Anime XL IL v19: 上記
4. Hassaku v3.4: ポジ `masterpiece, best quality, newest, absurdres, highres, 1girl, ...` / ネガ `worst quality, bad quality, signature`
5. NoobAI V-Pred: 上記
6. RouWei 0.8: `masterpiece, best quality, 1girl, ..., a girl sitting on a windowsill reading a book, soft afternoon light BREAK (artist_a:0.6), (artist_b:0.5)` / ネガ `low quality, worst quality`
7. Raehoshi: ポジ `masterpiece, best quality, very aesthetic, 1girl, ...`
8. Ikastrious: ポジ `general, masterpiece, best quality, anime coloring, 1girl, ...`
9. Animagine 4.0: `1girl, <character>, <series>, safe, <その他>, masterpiece, high score, great score, absurdres`
10. Illustrious v2.0（SeaArt）: `1girl, solo, ..., masterpiece, best quality, very aesthetic, absurdres` / Euler a, 25, CFG 6.5, 1024×1536
11. 日本語圏定番: `masterpiece, best quality, general, newest, 1girl, solo, <キャラ要素>, <背景・演出>`
12. ADetailer 専用（れん）: 顔 `beautiful natural face, balanced facial proportions, symmetrical face structure, smooth facial shading, clean facial contours, soft facial shadow` / 手 `natural hands, correct finger count, proper finger joints, relaxed hand pose, anatomically correct hand`

## 推奨プロンプトテンプレート（SFW 美少女向け・5 パターン）
前提: WAI v17 / Hassaku v3.4 等の eps 系。共通設定 Euler a / 28 step / CFG 6（LoRA 併用時 4.5）/ CLIP skip 1 / Hires.fix ×1.5, R-ESRGAN 4x+ Anime6B, denoise 0.4 / ADetailer face_yolov8s denoise 0.35 → hand_yolov8n 0.35。v-pred 系なら CFG 4 + ZTSNR + Rescale 0.6。共通ネガ:
```
worst quality, low quality, lowres, bad anatomy, bad hands, extra digits, fewer digits, jpeg artifacts, signature, watermark, username, text, nsfw
```
① 顔アップ（832×1216 or 1024×1024）
```
1girl, solo, close-up, face focus, portrait, looking at viewer, light smile, parted lips, blush,
long hair, silver hair, hair between eyes, sidelocks, blue eyes, hair ornament, sailor collar,
backlighting, rim lighting, soft lighting, depth of field, blurry background, bokeh, cherry blossoms, petals,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
② バストアップ（832×1216）
```
1girl, solo, upper body, from side, looking at viewer, smile, head tilt,
medium hair, wavy hair, brown hair, green eyes, white shirt, collared shirt, sleeves rolled up, holding cup, coffee cup,
cafe, indoors, window, dappled sunlight, warm lighting, depth of field,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
③ 全身（832×1216 or 768×1344）
```
1girl, solo, full body, standing, contrapposto, hand on own hip, looking at viewer, smile,
long hair, twintails, black hair, red eyes, school uniform, pleated skirt, black thighhighs, loafers, school bag,
street, crosswalk, city, sunset, orange sky, long shadow, backlighting, lens flare, wide shot, from below,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
④ 背景重視（1216×832 or 1344×768、Hires ×1.5〜2.0 denoise 0.4）
```
1girl, solo, scenery, wide shot, from behind, looking back, standing, wind, floating hair,
white dress, sun hat, long hair, blonde hair,
sunflower field, blue sky, cumulonimbus cloud, summer, light rays, sunbeam, volumetric lighting, cinematic lighting,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
⑤ 複数人（Regional Prompter Matrix 列 `1,1` / Forge Couple）
```
2girls, side-by-side, looking at viewer, park, sunlight, dappled sunlight, depth of field,
masterpiece, best quality, very aesthetic, absurdres, newest, general ADDCOMM
1girl, long hair, blonde hair, blue eyes, white dress, smile, hand up, waving BREAK
1girl, short hair, black hair, brown eyes, black jacket, shorts, grin, hands in pockets
```

## Top 15
1. 派生モデルのカード推奨値を最優先
2. ネガは短く始めて足す
3. 品質タグは 4 つ＋モデル固有に絞る
4. general/safe ＋ネガ nsfw
5. 年代タグで画風を選ぶ
6. Danbooru 正式表記
7. 重要タグは先頭 75 トークン内、絵師タグは BREAK
8. 強調は 1.1〜1.3
9. 832×1216 → Hires ×1.5 → ADetailer 顔 → 手 の標準化
10. LoRA 併用時は CFG 3.5〜5
11. 光タグと画角タグを 1 つずつ
12. AI っぽさ対策
13. 複数人は RP / Forge Couple
14. v-pred は ZTSNR ON + CFG 4 + Rescale 0.6
15. X/Y/Z plot で基準値確定

未達成: Reddit / X 上の個別投稿プロンプトは取得不能。Illustrious v3.6 のオープンウェイト配布有無、WAI v17 の 4 段階レーティングタグの正確な語彙、A1111 本家での v-pred 自動判定の有無は要追加確認。

# 03. Anima（Circlestone Labs）× ComfyUI 徹底調査（2026年9月版）

> **第 2 回追記（2026-09-09）**: 公式 README（HF）・Civitai カード・note「108 スタイル比較」本文で検証した結果は `report/07_prompt_verification.md` §2・§5。追加事項: Danbooru と Gelbooru で表記が違うタグは Gelbooru 側を優先／まず Turbo から始めるのが公式推奨／Civitai カードは CFG 4〜6・Aesthetic は CFG 3 でも可／LoRA は LLM adapter を学習せず rank 32・LR 2e-5 から／版の公開日は turbo-v1.0 2026-07-08、aesthetic-v1.1 2026-07-13、turbo-v1.1 2026-08-24（Civitai）。様式タグは `cel shading` `flat color` が無効で、`90s anime style` `retro anime style` `VHS anime aesthetic` `soft pastel style` が有効（`prompts/anima_templates.md` §4）。


> 調査メモ: 出口プロキシは GitHub 以外のほぼ全ドメインをブロック。公式ドキュメントとワークフローは Comfy-Org/docs・Comfy-Org/workflow_templates・ComfyUI 本体のソース（GitHub）を直接読み、HF README は GitHub 上のミラー／派生ガイドを突き合わせ、その他は検索エンジンの要約で補った。note.com「108スタイル比較」（ai_0049）は本文未読。

## 1. 概要と履歴

アーキテクチャ: NVIDIA Cosmos-Predict2-2B-Text2Image（MiniTrainDIT、28ブロック）を土台に、T5-XXL を Qwen3-0.6B + 6層 cross-attention の「LLM adapter」に置き換えた 2B DiT。adapter は Qwen3 の隠れ状態を T5 トークン列（512 トークンにパディング）へ写像。ComfyUI 実装では latent_format = Wan21（Qwen-Image VAE は Wan2.1 VAE の微調整版・16ch）、既定 shift = 3.0（comfy/supported_models.py）。開発は CircleStone Labs（diffusion-pipe 作者 tdrussell）× Comfy Org。
- 学習データ: 数百万枚のアニメ画像 + 約80万枚の非アニメ美術画像、合成データなし、アニメ側の知識カットオフ 2025年9月。Danbooru タグ／自然文／その混合の3形式で学習し、タグドロップアウトあり。
- ライセンス: CircleStone Labs Non-Commercial License（モデル・派生・LoRA は非商用、生成画像の商用利用は可）。
- VRAM: 公式目安 8GB、6GB でも動作報告多数。Turbo は 1枚 5〜7秒級、Base 30step・864×1536 で約14.7秒。

履歴（2026年）
| 時期 | 出来事 |
|---|---|
| 1/27 | ComfyUI v0.11.0 が Anima ファミリーをネイティブ対応（Preview 公開期）。以降 preview2 / preview3-base |
| 5/15 | Anima-Base v1.0 正式公開。5/23 公式テンプレ image_anima_base_v1 |
| 5/8, 6/16 | kohya sd-scripts が Anima LoRA / ControlNet-LLLite / LLLite inpainting / torch.compile 対応 |
| 6/30 | ComfyUI v0.27.0「Built-in LoRA training が Anima で動作」 |
| 7/8 | Anima-Turbo v1.0（CFG1・8〜12step 蒸留）と Anima-Aesthetic v1.0（高品質画像のみで微調整、品質タグを除去して学習）。のちに Aesthetic v1.0b |
| 7/20〜29 | 公式 LLLite テンプレ3種（Any Control / Depth / Inpainting）、ComfyUI v0.29.0 で AnimaLLLiteApply 追加、v0.31.0 で高速化 |
| 〜8/3 | Turbo v1.1 / Aesthetic v1.1 が流通（Civitai 最新版・nomadoor サンプルWFが anima-aesthetic-v1.1.safetensors 使用） |
| 8/12〜13 | コミュニティ Anima-2.9B（28→40ブロック層拡張、+170万枚、2026/7 カットオフ）。ComfyUI v0.33.1 が「extra blocks」対応 |
| 8/22 | Anima-3.8B Pro52 / Qwen3.5 Edition（lylogummy、52ブロック、Qwen3.5-4B TE、専用ノード必須） |
| 通年 | FP8、GGUF、Diffusers 版、Civitai に「Anima Checkpoint」カテゴリ新設・派生20種超（OOO_Anima、anima_pencil、Anime Studio、CapAnima、Any Anima など） |

出典: https://huggingface.co/circlestone-labs/Anima / https://gigazine.net/gsc_news/en/20260515-anima-image-generation-ai/ / https://comfyui-wiki.com/en/news/2026-07-08-anima-turbo-aesthetic-v1 / https://comfyui-wiki.com/en/news/2026-08-12-anima-2-9b / https://comfyui-wiki.com/en/news/2026-08-22-anima-3-8b / https://raw.githubusercontent.com/Comfy-Org/docs/HEAD/changelog/index.mdx / https://github.com/comfyanonymous/ComfyUI/releases / https://raw.githubusercontent.com/comfyanonymous/ComfyUI/HEAD/comfy/supported_models.py / https://www.kombitz.com/2026/05/20/anima-ai-the-new-anime-image-generator-explained/ / https://lilting.ch/en/articles/anima-derivative-checkpoints

## 2. プロンプトの書き方（最重要）

### 2-1. 公式のタグ順序と記法（HF README）
```
[quality/meta/year/safety tags] [1girl/1boy/1other etc] [character] [series] [artist] [general tags]
```
- 各ブロック内の順序は任意。区切りはカンマ、タグは小文字・スペース区切り（brown hair）。アンダースコアを保つのは score_7 系のみ。
- 品質タグ: 人手スコア系 masterpiece, best quality, good quality, normal quality, low quality, worst quality と PonyV7 系 score_9 … score_1 を「どちらか／両方／なし」で使える。公式推奨プレフィックス: `masterpiece, best quality, score_7, safe,`
- 年代タグ: `year 2025` 等の年、または期間 newest / recent / mid / early / old。メタ: highres, absurdres, anime screenshot, jpeg artifacts, official art。
- safety タグ: safe / sensitive / nsfw / explicit の4段階。ポジティブに1つ、残りをネガティブへ。
- 絵師タグ: 必ず `@` を前置（`@nnn yryr`）。「@ がないと効果が極端に弱い」。1人が最も安全。ネガに `artist name` を入れるのが公式推奨。
- キャラ名: 名前の後に必ず外見（髪・目・服）を記述。
- ネガティブ（公式推奨）: `worst quality, low quality, score_1, score_2, score_3, artist name`（公式テンプレは `…, blurry, jpeg artifacts, sepia`）。Base/Aesthetic ではネガは有効。
- 自然文: 純自然文なら 2文以上。タグと自然文は自由に混在可（ハイブリッド推奨）。
- 重み付け: ComfyUI の括弧は動作するが、SDXL より大きい値（(chibi:2) 等）が必要という報告。`[tag]` は使わない。
- トークン長: adapter 出力は 512 トークン基準。
- 文字描画: 単語1つ〜短いフレーズは描けるが文は不可。
- バリアント別: Aesthetic は score_* をポジ・ネガとも入れない（masterpiece, best quality は残してOK）、ノイズが出たら CFG を下げ・score を外し・`anime coloring` 追加。Turbo は CFG1 のためネガが実質無効（必要なら NAG ノード）。2.9B は「より詳細な記述」が推奨。

### 2-2. 公式例文（原文）
- タグ式: `year 2025, newest, normal quality, score_5, highres, safe, 1girl, oomuro sakurako, yuru yuri, @nnn yryr, smile, brown hair, hat, solo, fur-trimmed gloves, open mouth, long hair, gift box, fang, skirt, red gloves, blunt bangs, gloves, one eye closed, shirt, brown eyes, santa costume, red hat, skin fang, twitter username, white background, holding bag, fur trim, simple background, brown skirt, bag, gift bag, looking at viewer, santa hat, ;d, red shirt, box, gift, fur-trimmed headwear, holding, red capelet, holding box, capelet`
- ハイブリッド: `masterpiece, best quality, @big chungus. An anime girl with medium-length blonde hair is...`
- 自然文: `Digital artwork of Fern from Sousou no Frieren, with long purple hair and purple eyes, wearing a black coat over a white dress with puffy sleeves...`
- 公式テンプレ（preview）: `masterpiece, best quality, score_7, safe, anime, a close-up of a futuristic cyberpunk robotic eye, ... sharp line art, gritty futuristic sci-fi atmosphere.`
- 公式テンプレ（Depth LLLite）: `front view perspective, cozy sunlit living room, a young girl sits on the central sofa reading a book, abundant lush green houseplants everywhere, large window beside the sofa, soft warm daylight pouring through window, vintage furniture, books, tableware and home decorations, obvious layered indoor spatial depth, rich interior details, warm gentle color palette, clean smooth line art, soft cel shading, japanese slice of life anime illustration, tranquil healing atmosphere, decorative sticker art, neat composition`

### 2-3. コミュニティ知見
- スタイル: `@絵師` が最強。タグ系では anime screenshot、retro artstyle、anime coloring、flat color、sketch 等が有効。「絵師タグ×LoRA」は混ざり具合が変わり Hires で崩れる事例あり。
- 複数人: 「左の子は〜、右の子は〜」と英語の自然文で and で繋ぐのが最も確実。タグなら 2girls の後に各人を [名前, 作品, 髪, 服] で分けて記述。Comfyui-Anima-Regional-Conditioning も利用可。
- 表情: 単発の smile は効きが弱い。目の形／瞳／口／眉／頬の 3軸以上を組むと安定。
- 書き分けの原則: キャラの骨格はタグ、構図・光・関係性は自然文。

出典: https://huggingface.co/circlestone-labs/Anima/blob/main/README.md / https://raw.githubusercontent.com/shadowdoguk/image-to-prompt/main/docs/ANIMA-PROMPTING-MANUAL.md / https://raw.githubusercontent.com/CalamitousFelicitousness/ai-prompting-guides/HEAD/docs/anima.md / https://raw.githubusercontent.com/civitai/civitai/HEAD/docs/prompt-analysis-samples/candidates/anima-v4.txt / https://raw.githubusercontent.com/6DammK9/nai-anime-pure-negative-prompt/HEAD/ch02/anima.md / https://x.com/AIeseshi/article/2058196016395145568 / https://lulinaworks.com/articles/anima-style-compare / https://note.com/ai_0049/n/n74ccab5370e0 / https://raw.githubusercontent.com/ponapon280/5chSummary/HEAD/667/sum_prefiles/sum_5.md

## 3. ComfyUI の推奨ワークフローと設定

ファイル配置
```
ComfyUI/models/diffusion_models/anima-base-v1.0.safetensors   (~4.5GB; turbo/aesthetic v1.1 も同所)
ComfyUI/models/text_encoders/qwen_3_06b_base.safetensors        (~1.2GB)
ComfyUI/models/vae/qwen_image_vae.safetensors                   (~254MB)
ComfyUI/models/loras/anima-turbo-lora-v0.2.safetensors          (公式 Turbo LoRA)
ComfyUI/models/model_patches/anima-lllite-*.safetensors         (Comfy-Org/Anima-LLLite: any-test-like-v2, lineart-1, depth-1, pose-1, scribble-1, inpainting-v2)
```
- 公式テンプレ構成: UNETLoader → (LoraLoaderModelOnly Turbo 切替) → KSampler、CLIPLoader(type=stable_diffusion) → CLIPTextEncode×2、EmptyLatentImage 1024×1024、VAEDecode。既定 30 steps / CFG 4 / euler / simple、Turbo モード 8 steps / CFG 1。preview テンプレは er_sde / simple。
- README 推奨: 30〜50 steps、CFG 4〜5。sampler: er_sde（ニュートラル・フラット塗り・シャープ線）、euler_ancestral（柔らかく細い線）、dpmpp_2m_sde_gpu（er_sde 似で多様）。Aesthetic は CFG 3 程度も可。Turbo は 8〜12 / CFG1。
- コミュニティ: HF #165 では uni_pc + ddim_uniform が最速で安定、res_multistep + beta は水玉ノイズが出ることあり。RedRayz 比較は res_multistep か er_sde × simple。beta57（RES4LYF）は絵画調。公式 Diffusers 設定は flow_euler + shift 3.0 / 30 steps / CFG 5。
- shift: ComfyUI は内部既定 3.0。明示するなら ModelSamplingAuraFlow（または ModelSamplingSD3）で 3.0。
- 解像度: v1.0 は 512〜1536px、約 2MP 超で破綻。推奨: 1024x1024 / 896x1152 / 832x1216 / 768x1344 / 640x1536 / 1152x896 / 896x1344 / 1024x1536(1.57MP)。16の倍数必須、32 の倍数が安全。
- Hires / アップスケール: タイルなしの latent/img2img 拡大は 1.5倍まで（HF #163）。実例: 1.25×・19 steps・denoise 0.29、Turbo で 12 steps・CFG1・denoise 0.28。4K 以上は Ultimate SD Upscale（タイル 1024）、最終仕上げに SeedVR2 or 2x-AnimeSharpV4。
- FaceDetailer / Impact Pack: 使用可だが、crop サイズが 16 の倍数でないと spatial_patch_size 2 エラー（Impact #1186）。ComfyUI-anima-Resolutions の detailer crop 整列や EasyUseAnimaDetailerAlignHook で対処。FaceDetailer が2回目以降無限ループする未解決バグ（#1205）あり。
- LoRA: LoraLoaderModelOnly で適用。学習は Base で行う（Turbo/Aesthetic には流用可）。ツール: kohya sd-scripts（anima_train_network.py、lr 1e-4）、diffusion-pipe（llm_adapter_lr = 0 推奨）、ai-toolkit、OneTrainer（Anima プリセット lr 3e-5）、Anima LoRA Factory（Windows・約6GB VRAM、dim32/alpha32/768px）、anima_lora、ComfyUI 内蔵学習。
- ControlNet / inpaint / IP-Adapter: 従来型 ControlNet はなし。Anima-LLLite（ModelPatchLoader→AnimaLLLiteApply、strength 1.0、start/end 0〜1）で depth / lineart / pose / scribble / any(canny・HED・pidinet) / inpainting(v2)。IP-Adapter は公式なし。Lanpaint も動作。
- img2img / 二段構成: Anima で構図・複数人を決め、Illustrious で img2img（denoise 0.35〜0.5）仕上げる構成が実用的。SDXL LoRA→Anima 変換は不可。
- 量子化: Cosmos 系は fp8 e4m3 に弱く LoRA 併用でノイズ化する報告があるため、LoRA 併用時は bf16 か GGUF が無難。

出典: https://docs.comfy.org/tutorials/image/anima/anima / https://raw.githubusercontent.com/Comfy-Org/workflow_templates/HEAD/templates/image_anima_base_v1.json / https://raw.githubusercontent.com/Comfy-Org/docs/HEAD/built-in-nodes/AnimaLLLiteApply.mdx / https://huggingface.co/kohya-ss/Anima-LLLite / https://raw.githubusercontent.com/kohya-ss/sd-scripts/HEAD/docs/anima_train_network.md / https://raw.githubusercontent.com/tdrussell/diffusion-pipe/HEAD/docs/supported_models.md / https://github.com/UNfukashigi/Anima-LoRA-Factory / https://github.com/KeithZ117/Comfyui-anima-sampler / https://github.com/cyberdeliaAI/ComfyUI-anima-Resolutions / https://github.com/ltdrdata/ComfyUI-Impact-Pack/issues/1205 / https://github.com/shin131002/ComfyUI-Anima-Remap / https://raw.githubusercontent.com/n0va39/ComfyUI-EasyUseAnima/HEAD/docs/Anima%20AiO/ANIMA_Easy_Use_workflow_v1_EN.md / https://huggingface.co/circlestone-labs/Anima/discussions/165 / https://huggingface.co/circlestone-labs/Anima/discussions/163 / https://note.com/hkmclab/n/ne39ca8184d79

## 4. コミュニティの知見（得意・不得意・失敗と対策）
- 得意: 自然文理解、複数キャラの描き分け・色や部位指定、Illustrious 同等のキャラ知識と絵師スタイル認識、LoRA が 6GB で学習できる軽さ、Aesthetic で手・解剖・キャラ再現が向上。
- 不得意: Base は素の画風が平坦（品質・絵師タグ必須）、塗りがフラットで SDXL より反射・グラデが乏しい、背景・光の描き込みは Illustrious 優位で構図が人物中心になりがち、表情指定が不安定、Turbo は構図多様性が激減、Aesthetic は色がくすみ指が崩れやすいとの声、マイナーキャラは弱い、2MP 超で破綻、文字は単語のみ。
- 失敗→対策: ノイズ/ザラつき → CFG を下げ・score_* 除去・anime coloring。絵師が効かない → @ を確認し artist name をネガに。破綻 → (masterpiece:2),(best quality:2)・ネガ (worst quality:2)。Hires で崩れる → 1.25〜1.5倍・denoise 0.3 以下。キャラ混同 → 各人に外見記述、Regional Conditioning。FaceDetailer エラー → crop を 16/32 倍数に整列。
- 5ch 総括: 「LoRA 基盤として定着、タグ＋自然文・多キャラで高評価、ただし NAI V5 級の完成度には未達」「2.9B は構図安定だが速度 1.4 倍低下」。

出典: https://www.ipentec.com/document/ai-image/image-generation-anima-model / https://living-with-ai.com/seaart-anima-vs-illustrious/ / https://lulinaworks.com/articles/anima-basic / https://note.com/nobinlog/n/n73d7860ed7bf / https://note.com/robai104/n/n39a51b9df02e / https://note.com/sepiablue/n/nc0b2feee1ae8 / https://playershi.com/2026/06/05/anima_vs_sdxl/ / https://diffusiondoodles.substack.com/p/anima-light-fast-and-slightly-unruly

## 5. Illustrious との使い分け
| 観点 | Anima | Illustrious 系 |
|---|---|---|
| プロンプト追従・自然文 | ◎ | △ |
| 複数人の書き分け | ◎ | △〜○ |
| 背景・光・塗りの豪華さ | ○（フラット寄り） | ◎ |
| 画風の幅 | ◎ @絵師 が強く効く | ◎ 派生/LoRA が膨大 |
| LoRA エコシステム | ○ 急拡大中 | ◎ |
| 解像度 | 1〜1.6MP | 1MP + Hires が安定 |
| 破綻率・手 | Base は要調整、Aesthetic で改善 | 派生次第で安定 |
| 速度 | やや遅い（Turbo で高速） | 速い |

結論: 「構図・複数人・シーン指示」は Anima、「塗り・背景の見栄え・既存 LoRA」は Illustrious。

## 6. Anima 推奨プロンプトテンプレート（SFW美少女向け）
共通設定（Base v1.0）: 30〜40 steps / CFG 4.5 / er_sde / simple / shift 3.0 / denoise 1.0。Aesthetic v1.1 なら score_7 と score_1〜3 を全削除し CFG 3.5〜4。Turbo v1.1 は 10 steps / CFG 1。
共通ネガティブ（Base）: `worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit`

① 顔アップ — 896×1152
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, @artist, close-up, face focus, portrait, looking at viewer, long silver hair, blunt bangs, violet eyes, bright pupils, half-closed eyes, gentle smile, parted lips, blush, hair ornament, soft lighting, depth of field, anime coloring, clean lineart.
A close-up portrait of a girl gazing softly at the viewer, warm afternoon light catching her hair, blurred pastel background behind her.
```
② バストアップ — 832×1216
```
masterpiece, best quality, score_7, newest, highres, safe, 1girl, solo, @artist, upper body, medium shot, looking at viewer, brown hair, twintails, green eyes, smile, school uniform, white shirt, red ribbon, blazer, hand on own cheek, classroom, window, sunlight, backlighting, anime coloring.
She leans slightly toward the viewer with a playful expression, sunlight from the window behind her outlining her hair.
```
③ 全身 — 768×1344 / 832×1216
```
masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, @artist, full body, standing, dynamic pose, looking at viewer, black hair, long hair, blue eyes, wide eyes, open mouth, white dress, sundress, sandals, straw hat, holding hat, sunflower field, blue sky, cumulonimbus cloud, wind, from below, anime coloring.
A girl stands in a sunflower field holding her hat against the wind, her dress and hair blowing to the left, the whole body visible from head to feet.
```
④ 背景重視 — 1152×896 / 1344×896
```
masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, @artist, scenery, wide shot, from behind, small figure, pink hair, short hair, white blouse, standing on a hill, cityscape, sunset, orange sky, cloud, torii, cherry blossoms, petals, detailed background, depth, cinematic lighting.
A wide landscape illustration where the girl is a small silhouette on the left third of the frame, the vast evening city and sky dominating the scene with layered depth and glowing windows.
```
⑤ 複数人 — 1152×896
```
masterpiece, best quality, score_7, newest, highres, safe, 2girls, @artist, upper body, side by side, looking at viewer, cafe, table, window, warm lighting, anime coloring.
Two girls sit side by side at a cafe table. The girl on the left has long blonde twin braids and blue eyes, wears a navy sailor uniform and holds a teacup with both hands, smiling gently. The girl on the right has short black hair and red eyes, wears a white hoodie and rests her chin on her hand with a bored expression. They lean slightly toward each other.
```
（複数人はネガに `1girl, solo, 3girls, twins, same face` を追加すると安定）

## 7. 推奨 ComfyUI ワークフロー構成（テキスト）
基本版
```
UNETLoader(anima-base-v1.0 / aesthetic-v1.1, weight_dtype=default)
 └→ [LoraLoaderModelOnly(anima-turbo-lora-v0.2, 1.0)  ※高速検証時のみ]
 └→ ModelSamplingAuraFlow(shift=3.0)  ※省略時も内部既定3.0
CLIPLoader(qwen_3_06b_base, type=stable_diffusion)
 ├→ CLIPTextEncode(positive) ─┐
 └→ CLIPTextEncode(negative) ─┤
EmptyLatentImage(832x1216, 16の倍数) ─┤
KSampler(seed, steps 30-40, cfg 4-5 [Turbo: 8-12 / 1], sampler er_sde, scheduler simple, denoise 1.0)
 └→ VAEDecode(VAELoader qwen_image_vae) → SaveImage
```
高品質版（Hires + Detailer + Upscale）
```
[基本版 1st pass: 832x1216, 30 steps, cfg 4.5, er_sde/simple]
 └→ VAEDecode → ImageUpscaleWithModel(2x-AnimeSharpV4 / 4x_foolhardy_Remacri) → ImageScaleBy(合計 1.25〜1.5x, 16の倍数へ丸め)
 └→ VAEEncode → KSampler(2nd pass: 同モデル, 20 steps, cfg 4, denoise 0.28〜0.35, er_sde/simple)
      ※1.5x超は UltimateSDUpscale(tile 1024, denoise 0.25, seam fix)
 └→ VAEDecode
 └→ FaceDetailer(Impact Pack: bbox face_yolov9c / SAM, guide_size 512, max_size 1024, denoise 0.35-0.45, cfg 4, steps 20, feather 8)
      ※crop を 32 の倍数に整列
 └→ [任意] SeedVR2 Image Upscaler(2x) or Illustrious img2img(denoise 0.35-0.45)
 └→ SaveImage(PNG + WebP for X)
[任意] ModelPatchLoader(anima-lllite-depth-1) → AnimaLLLiteApply(strength 0.7-1.0, end 0.6-0.8)
```

## 8. Top 15
1. 絵師タグは必ず @name、ネガに artist name
2. ポジ先頭を masterpiece, best quality, score_7, safe,（Aesthetic は score_* を外す）
3. safety タグをポジに1つ、残り3つをネガに
4. タグは小文字＋スペース区切り（score_7 だけ例外）
5. 「タグでキャラ骨格、自然文2文以上で構図・光・関係性」
6. 表情は 3軸以上で指定
7. 複数人は英語自然文で「左の子は… and 右の子は…」
8. 解像度は 1〜1.6MP、16の倍数
9. sampler は er_sde/simple 基準
10. Hires は 1.25〜1.5倍・denoise 0.3 以下
11. FaceDetailer の crop を 32 の倍数に整列
12. 試作は Turbo、本番は Base/Aesthetic v1.1
13. ノイズが出たら CFG を 3.5 まで下げ、anime coloring
14. 構図固定は Anima-LLLite
15. 推しキャラは Base で LoRA 学習

参考 URL（追加分）: https://comfyui-wiki.com/en/models/anima / https://comfyui.nomadoor.net/en/basic-workflows/anima/ / https://techtactician.com/anima-comfyui-quick-local-setup-guide/ / https://civitai.com/articles/26217/anima-what-is-anima / https://civitai.com/models/2458426/anima / https://huggingface.co/circlestone-labs/Anima/discussions/153 / https://github.com/sorryhyun/anima_lora / https://github.com/Sen-sou/Comfyui-Anima-Regional-Conditioning / https://github.com/hybskgks28275/ComfyUI-Anima-NAG / https://github.com/CocyNoric/ComfyUI-Anima-TeaCache / https://github.com/GumGum10/comfyui-anima-3-8B / https://raw.githubusercontent.com/comfyanonymous/ComfyUI/HEAD/comfy/text_encoders/anima.py / https://raw.githubusercontent.com/nomadoor/Kura/HEAD/workflows/samples/anima/anima-aesthetic-v1.1.json / https://note.com/yoya48/n/n6cb08878780e / https://note.com/redrayz/n/n67aebd3c6996

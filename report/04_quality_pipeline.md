# 04. 高品質化ワークフロー技術調査（2026年9月版）

対象環境: Windows PC / Stable Diffusion WebUI 系（Illustrious）＋ ComfyUI（Anima）。
調査方法: 日英 Web 検索 33 回＋一次資料（GitHub README・公式ドキュメント）取得。国内ブログ・Civitai・HF は本セッションの回線制限で本文取得できなかったものがあり、それらは検索結果の要約に基づく（該当箇所は「要確認」と明記）。

## 0. 前提となる 2026 年のモデル事情（要点）

| | Illustrious 系（SDXL） | Anima（CircleStone Labs × Comfy Org） |
|---|---|---|
| アーキテクチャ | SDXL UNet, SDXL VAE (4ch) | Cosmos-Predict2-2B ベースの DiT, Qwen3-0.6B text encoder, Qwen-Image VAE (16ch) |
| 推奨設定 | Euler a / 24〜30 steps / CFG 4.5〜5.5 / 1536px 基準解像度も可（派生モデルは 1024 級） | Base・Aesthetic：30〜50 steps, CFG 4〜5, shift 3.0／ Turbo：8〜12 steps, CFG 1 |
| プロンプト | Danbooru タグ＋品質タグ (masterpiece, best quality…) | Danbooru タグ＋自然文。接頭 `masterpiece, best quality, score_7, safe,`、負 `worst quality, low quality, score_1, score_2, score_3, artist name`。小文字・アンダースコア不使用・絵師タグは `@` 接頭 |
| 強み | 塗り・キャラ再現・LoRA 資産・ControlNet 資産 | プロンプト追従（自然文）、~7GB VRAM で動く軽さ |
| ライセンス | 派生モデルごと | モデル自体は非商用ライセンス、生成画像の商用利用は可 |

- Anima は 2026 年 1〜2 月にプレビュー、5/15 に Base v1.0、7/8 に Turbo v1.0 と Aesthetic v1.0 が公開（Turbo は v1.1 も）。Aesthetic は高品質画像のみで微調整し品質タグを除去、Turbo は蒸留で安定＋既定画風が強く多様性は減。「Turbo で seed/構図探索 → Aesthetic で仕上げ」が推奨されている。出典: [HF circlestone-labs/Anima](https://huggingface.co/circlestone-labs/Anima) / [Anima wiki](https://ai.miraheze.org/wiki/Anima) / [comfyui-wiki 7/8 ニュース](https://comfyui-wiki.com/en/news/2026-07-08-anima-turbo-aesthetic-v1) / [Turbo v1.1 比較 note](https://note.com/akb428/n/nc794be92ebc2) / [ComfyUI-Anima-NAG README](https://github.com/hybskgks28275/ComfyUI-Anima-NAG)
- ComfyUI 本体が Anima をネイティブ対応。WebUI 側は **Forge Neo** が Anima（2B に加え 2.9B/3.8B 版への LoRA 自動マッピングも README に記載）・SDXL・Qwen-Image 等に対応し、ControlNet（Union / Region / LLLite）を内蔵。→ WebUI 派でも Anima を扱える。出典: [ComfyUI README](https://github.com/comfyanonymous/ComfyUI) / [sd-webui-forge-classic (Neo)](https://github.com/Haoming02/sd-webui-forge-classic)
- Illustrious XL 2.0 本体は「マージ用ベースで素のまま使わない」とされ、WAI-illustrious v16（2026/2 更新）/ v17、Raehoshi illust XL 5.1 等のファインチューンが実用の中心。出典: [Illustrious XL 2.0 (Civitai)](https://civitai.com/models/1369089/illustrious-xl-20) / [Illustrious 2.0 ガイド](https://www.seaart.ai/articleDetail/cvceb6le878c73bckfig) / [WAI v17 レビュー](https://lilting.ch/en/articles/wai-illustrious-v17-review)

## 1. 高品質化パイプライン

### 1.1 Hires.fix（latent vs モデルアップスケール）
- WAI 系の公式推奨：**Hires upscale 1.5 / Hires steps 20 / upscaler R-ESRGAN 4x+ Anime6B / denoise 0.35〜0.5**、生成は Steps 25〜40, CFG 5〜7, Euler a。v17 では hires fix 通過で手足が自動補正されやすいと報告。出典: [WAI (Shakker)](https://www.shakker.ai/modelinfo/0f204323a06f40e18f8ffc5b1813df5a/WAI-illustrious-SDXL) / [WAI v17 レビュー](https://lilting.ch/en/articles/wai-illustrious-v17-review)
- 使い分け：**モデル（ESRGAN 系）アップスケール**は低 denoise（0.3〜0.45）で線と構図を保ったまま解像度を上げる。**Latent upscale**はディテールの再生成量が多い代わりに denoise を 0.5〜0.6 以上にしないとボケる（構図が変わりやすい）。ComfyUI では `UpscaleModelLoader` → `ImageUpscaleWithModel` → `ImageScaleBy`(0.375〜0.5 で 1.5x 相当) → `VAEEncode` → 2nd `KSampler`(denoise 0.35〜0.5)。出典: [ComfyUI 2-pass 例](https://comfyanonymous.github.io/ComfyUI_examples/2_pass_txt2img/)

### 1.2 顔・目・手の Detailer
- **WebUI: ADetailer**。モデルは `face_yolov8n/s.pt`, `hand_yolov8n.pt`, `person_yolov8n-seg.pt`, mediapipe 系。主要設定は detection confidence / mask blur / dilation / inpaint denoise / inpaint only masked / 別 steps・CFG・checkpoint。ControlNet 連携可。出典: [adetailer README](https://github.com/Bing-su/adetailer)
- **ComfyUI: Impact Pack `FaceDetailer`**（`UltralyticsDetectorProvider` は Impact-Subpack が必要、モデルは `models/ultralytics/bbox|segm`）。`guide_size` は「これより小さい検出領域を拡大して描き直す基準サイズ」、`max_size` は上限、`noise_mask` は基本 ON、`cycle` で多段。目安：guide_size 384（6GB なら 256）/ max_size 1024 / denoise 0.4〜0.5 を初回、弱ければ 0.6〜0.7。アニメ顔は anime 特化検出器（Civitai 配布のアニメ顔・目・手 YOLO）を使うと検出率が上がる。出典: [Impact Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack) / [Detailer チュートリアル](https://github.com/ltdrdata/ComfyUI-extension-tutorials/blob/Main/ComfyUI-Impact-Pack/tutorial/detailers.md) / [Impact-Subpack](https://github.com/ltdrdata/ComfyUI-Impact-Subpack) / [Apatero ガイド](https://www.apatero.com/blog/comfyui-impact-pack-complete-guide-professional-face-enhancement-2025)
- 実務のコツ：顔は denoise 0.3〜0.45（アニメ顔は動かしすぎると別人化）、目だけの 2 パス目に「detailed eyes, glossy eyes」等を別プロンプトで、手は Detailer より **OpenPose 手つき ControlNet ＋ inpaint** の方が確実（ADetailer の hand は補助扱い）。

### 1.3 最終アップスケール（比較）
| 手法 | 向き | 目安設定 / VRAM |
|---|---|---|
| ESRGAN 系（4x-AnimeSharp, R-ESRGAN 4x+ Anime6B, 4x-UltraSharpV2=DAT2, 2x-AnimeSharpV4） | 線画重視の純粋拡大 | 4x-AnimeSharp は UltraSharp と TextSharp の補間モデルでアニメに強い。UltraSharpV2 は DAT2 で「アニメ・イラストも守備範囲」。DAT/HAT/SwinIR/SPAN 等は ComfyUI の `UpscaleModelLoader`（spandrel）で読込可、モデル探索は Upscale Wiki の Model Database |
| Ultimate SD Upscale (USDU) | 線を保ったまま塗りを再描画 | tile 512〜1024 / padding 32〜55 / mask blur 16〜20 / **denoise 0.2〜0.35（強調 0.35、最小変更 0.15〜0.2）** / seams fix：アニメは Band pass で十分。ControlNet Tile 併用で denoise 0.5〜0.8 まで上げても構図が崩れない |
| Tile ControlNet 単体 img2img | 4K 化・塗り直し | Illustrious 用 Tile（windsingai）や xinsir union-promax の tile。denoise 0.4〜0.6 |
| SeedVR2（単画像可） | 2026 年の比較記事で **2D/アニメ部門の勝者（目がシャープ）** | 3B fp8：12〜16GB / 3B GGUF：8GB / 7B fp8-mixed：16〜24GB / 7B fp16：24GB+。`batch_size=1`。タイル版は tile 1024・overlap 32〜64。「細部を作り替える」ため線画の忠実さは要確認 |
| SUPIR | 実写寄りの復元 | アニメ線画は溶けやすく Illustrious 系では優先度低 |
| Anima Tile & Repair ControlNet-LLLite v2 ＋ USDU+CNtile | Anima でのタイル拡大・修復 | v2 は upscale ペアを大量追加。CN 制御下では denoise 1.0 でも破綻しないと報告（要確認） |

出典: [Kim2091/AnimeSharp](https://huggingface.co/Kim2091/AnimeSharp) / [Kim2091 Releases](https://github.com/Kim2091/Kim2091-Models/releases) / [Upscale Wiki Model DB](https://upscale.wiki/wiki/Model_Database) / [USDU FAQ](https://github.com/Coyote-A/ultimate-upscale-for-automatic1111/wiki/FAQ) / [USDU README](https://github.com/Coyote-A/ultimate-upscale-for-automatic1111) / [ComfyUI_UltimateSDUpscale](https://github.com/ssitu/ComfyUI_UltimateSDUpscale) / [SeedVR2 比較 2026](https://seedvr2.net/blog/tutorials/seedvr2-upscalers-battle-comparison-2026) / [ComfyUI-SeedVR2_VideoUpscaler](https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler) / [seedvr2-tilingupscaler](https://github.com/moonwhaler/comfyui-seedvr2-tilingupscaler) / [ComfyUI-SUPIR](https://github.com/kijai/ComfyUI-SUPIR) / [Anima Tile&Repair LLLite](https://huggingface.co/LAXMAYDAY/Anima_Tile_and_Repair_ControlNet-LLLite) / [Anima Tile 検証 note](https://note.com/hirorohi03/n/nca602f8f6aae)

### 1.4 ディテール制御・色調補正のノード
- **ComfyUI-Detail-Daemon**：`Detail Daemon Sampler` は「加えるノイズは同じまま各ステップで除去する量を減らす」方式。**SDXL は detail_amount < 0.25**（Flux は 0.1〜1.0）、start 0.1〜0.5 / end 0.5〜0.9。`Lying Sigma Sampler` は `dishonesty_factor -0.01〜-0.1`（-0.05 ≒ detail_amount 0.5）、`Multiply Sigmas` は factor 0.95〜0.99。やり過ぎると HDR 調・油絵化。Turbo 等の少ステップモデルは制御困難。WebUI 版は muerrilla/sd-webui-detail-daemon。出典: [ComfyUI-Detail-Daemon](https://github.com/Jonseed/ComfyUI-Detail-Daemon) / [sd-webui-detail-daemon](https://github.com/muerrilla/sd-webui-detail-daemon)
- **ComfyUI-ppm**：`CFG++SamplerSelect`（CFG 1〜2 で白飛び・色飽和を抑制、アニメ向き）、`CLIPNegPip`（負の重みで概念否定、SD1/SDXL/Anima 対応）、`AttentionCouplePPM`。出典: [ComfyUI-ppm](https://github.com/pamparamm/ComfyUI-ppm)
- **色調補正**：KJNodes `Color Match`（参照画像へ色合わせ、二段モデル構成で必須）、`Film Grain`、`ImageResizeKJ`；Easy-Use `easy imageColorMatch` / `easy hiresFix` / `easy detailerFix`；rgthree `Power Lora Loader` / `Image Comparer` / `Fast Groups Bypasser`（A/B 比較と分岐管理）。出典: [KJNodes](https://github.com/kijai/ComfyUI-KJNodes) / [Easy-Use](https://github.com/yolain/ComfyUI-Easy-Use) / [rgthree](https://github.com/rgthree/rgthree-comfy)

## 2. 二段モデル構成（Anima ⇄ Illustrious）

- **実例**：Civitai に「illu(t2i) + anima(i2i)」ワークフロー（Illustrious で生成 → Anima で img2img。Anima 用 LoRA を再学習せずに Illustrious LoRA 資産を活かす目的）と「anima_simple」（生成・inpaint・refine の簡易 WF）が公開。出典: [illu(t2i)+anima(i2i)](https://civitai.com/models/2647228/illut2i-animai2i-workflow) / [anima_simple](https://civitai.com/models/2508290/anima-simple-workflows-for-generation-and-inpaintingrefining-tips-and-info)
- **denoise の目安**（img2img は denoise<1.0 でノイズ量を制御）：構図・キャラ維持 0.3〜0.45、塗り替え 0.5〜0.6（ControlNet Tile/Lineart 併用が前提）、0.6〜0.8 は再解釈レベル。出典: [ComfyUI img2img 例](https://comfyanonymous.github.io/ComfyUI_examples/img2img/)
- **latent 受け渡しは不可、pixel 受け渡し必須**：Anima は Qwen-Image VAE（16ch）、Illustrious は SDXL VAE（4ch）で latent 空間が異なる。必ず `VAEDecode`（送り側 VAE）→ 画像 → リサイズ → `VAEEncode`（受け側 VAE）。SDXL VAE は fp16 で不安定になり得るため WebUI は `--no-half-vae` か fp16-fix VAE を使用。出典: [sd-scripts anima_train_network.md](https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_network.md) / [sd-scripts sdxl_train_network.md](https://github.com/kohya-ss/sd-scripts/blob/main/docs/sdxl_train_network.md)
- **解像度の橋渡し**：Anima 出力（~1MP）→ 4x-AnimeSharp で 1.5〜2x → Illustrious の得意域（1024×1536〜1536 基準）に合わせて `ImageScale`。**プロンプト翻訳**：Anima は自然文、Illustrious は Danbooru タグ。Anima 出力を WD14 tagger（wd-eva02-large-tagger-v3 等）で自動タグ化して Illustrious 側プロンプトの叩き台にすると齟齬が減る。出典: [ComfyUI-WD14-Tagger](https://github.com/pythongosssss/ComfyUI-WD14-Tagger)
- **色ズレ対策**：VAE の往復で彩度・ガンマが微妙に変わるため、最終段で `Color Match`（KJNodes, 参照＝一段目出力）を当てる。
- **Refiner 的運用**：Turbo（CFG 1, 8〜12 steps）で大量に seed/構図を回し → Aesthetic で本番 → Illustrious で塗り refine、が 2026 年時点の実用解。NAG（`scale 2.0 / tau 2.5 / alpha 0.5 / end 0.5`）を使えば CFG 1 の Turbo でも負プロンプトが効く。出典: [ComfyUI-Anima-NAG](https://github.com/hybskgks28275/ComfyUI-Anima-NAG) / [Anima 高速化比較](https://living-with-ai.com/anima-speed-up/)

## 3. 構図・ポーズ制御

- **ControlNet（Illustrious/NoobAI）**：Illustrious-XL ControlNet Openpose / Tile（windsingai）、NoobAI-XL ControlNet（eps/vpred 別）、xinsir **controlnet-union-sdxl-1.0 / promax**（openpose・depth・scribble/HED/softedge・canny/lineart/**anime lineart**・normal・seg を 1 モデルで、promax は tile deblur/variation/超解像・inpaint/outpaint 追加）、CNXL kohya-openpose-anime。プリプロセッサは comfyui_controlnet_aux（**DWPose** は手の検出が OpenPose より良い、AnimeLineart / Manga Lineart / Depth Anything V2）。出典: [Illustrious ControlNet Openpose](https://civitai.com/models/1359846/illustrious-xl-controlnet-openpose) / [NoobAI ControlNet](https://civitai.com/models/962537/noobai-xl-controlnet-openpose) / [ControlNetPlus (union/promax)](https://github.com/xinsir6/ControlNetPlus) / [controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux) / [ControlNet pose guide 2026](https://www.apatero.com/blog/comfyui-controlnet-pose-guide-2026)
- **Anima 側**：ControlNet-LLLite（公式 depth / lineart / pose / scribble / any / inpainting、sd-scripts に学習スクリプト）と Tile&Repair LLLite v2。Forge Neo は LLLite 内蔵。出典: [anima_train_control_net_lllite.md](https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_control_net_lllite.md)
- **IP-Adapter**：cubiq 実装が標準。SDXL は `ip-adapter-plus_sdxl_vit-h`（強め）/ `plus-face`（顔）/ `faceid-plusv2_sdxl`（InsightFace 依存、アニメ顔は検出失敗しやすい）。weight は 0.8 以下・steps 増が推奨。出典: [ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus) / [NoobAI/Illustrious IPAdapter WF](https://civitai.com/models/1466666/noobai-illustrious-ipadapter-workflow)
- **Regional Prompting**：
  - WebUI: **Forge Couple**（Basic/Advanced/Mask/Tile、SD1・SDXL・**Anima 対応**、辺は 64 の倍数）／ **Regional Prompter**（Matrix/Mask/Prompt、`BREAK / ADDCOL / ADDROW / ADDCOMM / ADDBASE`）。
  - ComfyUI: Impact **`RegionalSampler`**（**ControlNet で構図固定との併用を強く推奨**）、Inspire `Regional Prompt Simple / By Color Mask`、`AttentionCouplePPM`＋`LatentToMaskBB`、prompt-control の `COUPLE`。
  出典: [sd-forge-couple](https://github.com/Haoming02/sd-forge-couple) / [regional-prompter](https://github.com/hako-mikan/sd-webui-regional-prompter) / [Regional Sampler チュートリアル](https://github.com/ltdrdata/ComfyUI-extension-tutorials/blob/Main/ComfyUI-Impact-Pack/tutorial/regional_sampler.md) / [Inspire-Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack) / [prompt-control](https://github.com/asagi4/comfyui-prompt-control) / [Forge Couple 入門 note](https://note.com/hitsujiai/n/n9b2b21376091)
- **Inpaint**：`comfyui-inpaint-nodes`（**Fooocus inpaint patch** を SDXL ckpt に適用＝Illustrious を inpaint モデル化。`Denoise to Compositing Mask` で Differential Diffusion と連携）、**Inpaint Crop & Stitch**（`output_resize_to_target_size`=1024 で SDXL 最適解像度に拡大して描き直し）。出典: [comfyui-inpaint-nodes](https://github.com/Acly/comfyui-inpaint-nodes) / [Inpaint-CropAndStitch](https://github.com/lquesada/ComfyUI-Inpaint-CropAndStitch)
- **3D ポーズ**：PoseMy.Art（OpenPose 骨格・depth・canny を書き出し）、DesignDoll、Magic Poser、Blender。既製素材は pose-depot。出典: [PoseMy.Art](https://posemy.art/) / [pose-depot](https://github.com/a-lgil/pose-depot)

## 4. 「魅力」を作る演出テクニック

- **光**：`backlighting / backlit`、`rim lighting`、`sidelighting / underlighting`、`cinematic lighting`、`dynamic lighting`、`high key lighting`、`candlelight`、`god rays / light rays / sunbeam`、`lens flare`、`neon lights`、`sunset / golden hour`、`rain, wet, reflection, puddle`。国内検証記事では「主光源＋rim light＋fill light の三点構成」が立体感に効くと整理。出典: [iPentec 逆光](https://www.ipentec.com/document/ai-image/image-generation-prompt-backlighting) / [NEKOKAWA ライティング比較](https://nekokawa.hatenablog.com/entry/2026/02/24/070000) / [ライティングプロンプト 50 選](https://freecraftlog.com/comfyui-lighting-prompt-complete-guide/) / [光のプロンプト大全](https://ai-nante.com/light-prompt-guide/)
- **色設計**：テーマカラーを 1〜2 色に絞る（`limited palette`, `monochrome + spot color`）、補色配置、`high key`/`low key`。生成後にグラデーションマップ（Soft Light 10〜25%）で統一感を出す。
- **画角・被写界深度・動き**：`depth of field, bokeh, blurry foreground`、`wide shot / close-up / fisheye / wide-angle`、`from below / from above / dutch angle`、`foreshortening`、`wind, floating hair, motion blur, speed lines, splashing, water drop`。
- **物語性と表情**：小物（`holding …`）、背景の生活感、視線（`looking at viewer / looking away`）、`half-closed eyes`, `light smile`, `parted lips` の微差分を Detailer 段で作り込む。
- **「AI っぽさ」の消し方**：テカリ（`shiny skin` を負に、ハイライトはトーンカーブで抑制）、`film grain / chromatic aberration` タグ、Photoshop/Krita/CSP でレベル補正・トーンカーブ（浅い S 字）・グラデーションマップ・グロー（Screen 10〜20%）・微小な色収差（1〜3px）・ハイパス線画強調・粒子ノイズ 2〜4%。2026 年は「AI 質感に手描き/アナログ感を混ぜる混合型レトロ」が潮流。Krita AI Diffusion（ComfyUI バックエンド、Illustrious 対応）で選択範囲ごとの生成塗りをするのも有効。出典: [仕上げ加工テクニック (egaco)](https://comic.smiles55.jp/guide/8937/) / [AI っぽいデザイン脱却 2026](https://nextage-tech.com/blog/2026/06/08/post-7030/) / [AI っぽさを消す (SD)](https://onlinegamernikki.com/ai-illustration-delete-ai-style) / [krita-ai-diffusion](https://github.com/Acly/krita-ai-diffusion)

## 5. キャラ一貫性（オリキャラ運用）

- **Illustrious 向けキャラ LoRA（kohya_ss / sd-scripts）**：画像 20〜60 枚、1024 基準＋bucket、`network_dim 32〜64 / alpha = dim or dim/2`、UNet LR 3e-4〜5e-4（公式サンプルは 1e-4）、TE LR は 1/10、AdamW8bit、bf16、`cache_latents / cache_text_encoder_outputs / gradient_checkpointing`、1500〜3000 steps、`min_snr_gamma 5`、`noise_offset 0.0357`、`multires_noise 6〜10 / 0.3`、`network_dropout 0.1`。フォルダは `10_charname`。タグ付けは WD14（wd-eva02-large-tagger-v3 等）で、固定したい特徴（髪色・目・服）はタグに**残す**か**外す**かで学習の帰属が変わる（外すとトリガー語に吸収）。出典: [LoRA 2026 ガイド](https://techotakulab.com/lora-character-training-guide/) / [Illustrious キャラ LoRA 備忘録](https://note.com/kazuya_bros/n/n0a325bcc6949) / [sd-scripts sdxl](https://github.com/kohya-ss/sd-scripts/blob/main/docs/sdxl_train_network.md) / [sd-scripts advanced](https://github.com/kohya-ss/sd-scripts/blob/main/docs/train_network_advanced.md) / [kohya_ss](https://github.com/bmaltais/kohya_ss)
- **Anima 向け LoRA**：sd-scripts に `anima_train_network.py`（LR 1e-4・dim 8〜32・AdamW8bit・bf16、`--blocks_to_swap`・`--qwen_image_vae_2d` で省メモリ、LLM adapter を学習するなら LR 5e-5）。diffusion-pipe も Anima 対応。国内では rank 32・512px・10GB で学習可、12GB で WAI と Anima 両方作った比較記事あり。出典: [anima_train_network.md](https://github.com/kohya-ss/sd-scripts/blob/main/docs/anima_train_network.md) / [diffusion-pipe supported models](https://github.com/tdrussell/diffusion-pipe/blob/main/docs/supported_models.md) / [Anima LoRA トレーナー比較](https://ai-hardware-zukan.com/anima-2b-lora-trainer-comparison/) / [WAI/Anima LoRA 比較 (zenn)](https://zenn.dev/ojisan_ai_lab/articles/lora-wai-anima-howto-20260722) / [OneTrainer](https://github.com/Nerogar/OneTrainer) / [ai-toolkit](https://github.com/ostris/ai-toolkit)
- **LoRA なし固定**：①属性タグを固定文で持つ（髪型・色・目・アクセ・服を順序固定、`1girl, solo` 先頭）＋seed 固定、②ControlNet **Reference Only**、③IP-Adapter plus-face、④Inspire `KSampler (Inspire)` の `variation_seed / variation_strength` で構図を保った差分、⑤2 キャラ同時は Regional＋ControlNet で分離。出典: [オリキャラ手順 note](https://note.com/nobinlog/n/n37bf1fe2c785) / [Reference Only 解説](https://shizuru-vblog.com/use_reference-only/) / [Reference-only discussion](https://github.com/Mikubill/sd-webui-controlnet/discussions/1236)
- **シリーズ化**：キャラごとの「プロンプト・LoRA・seed 帳」を管理し、rgthree `Power Lora Loader` でトグル、Wildcard で衣装差分をテンプレ化。

## 6. 動画化・派生コンテンツ

- **オープンウェイト（ローカル）**：最新のオープン版は **Wan 2.2**（Wan 2.5 以降は API のみ）。Wan 2.2 は TI2V-5B（量子化で 8GB でも可）と I2V-A14B（fp8/GGUF＋block swap で 12〜16GB）。LightX2V の **4-step 蒸留 LoRA**で CFG 不要・高速。**LTX-2.3**（22B、音声＋動画同時生成、fp8 と CPU オフロードで 16GB）。出典: [Wan2.2](https://github.com/Wan-Video/Wan2.2) / [LightX2V](https://github.com/ModelTC/LightX2V) / [Wan2.2 8GB ガイド](https://www.runflow.io/blog/comfyui-wan-2-2-image-to-video) / [Wan2.2 GGUF 低 VRAM](https://www.nextdiffusion.ai/tutorials/how-to-run-wan22-image-to-video-gguf-models-in-comfyui-low-vram) / [ComfyUI-LTXVideo](https://github.com/Lightricks/ComfyUI-LTXVideo/) / [LTX-2](https://github.com/Lightricks/LTX-2) / [LTX-2.3 VRAM 検証](https://ltxworkflow.com/resources/community/ltx-23-vram-requirements-12gb-16gb-24gb) / [Best AI video models 2026](https://techsy.io/en/blog/best-ai-video-models)
- **アニメ調の注意**：Wan 2.2 は実写寄り学習のためアニメ絵の顔・細部が崩れやすい。対策＝入力を高解像度＆顔を大きく、動き指示を控えめ（`subtle motion`）、アニメ用 LoRA、生成後 SeedVR2 で顔を再鮮鋭化。出典: [Wan2.2 i2v のコツ](https://www.taneyats.com/entry/wan-22-i2v) / [Wan2.2 完全攻略](https://sakasaai.com/rp-comfywan-t2v-i2v-vace/)
- **API 系（アニメに強い順の目安）**：PixVerse V4.5、Wan 2.7、Seedance 2.0、Kling 3.0、Grok Imagine v1.5（Chibi アニメモード）、Hailuo。出典: [アニメ向け動画モデル 2026](https://tryinfer.com/best/ai-models-for-anime-video) / [Grok Imagine ガイド](https://www.shiori.ai/blog/grok-video-generation-guide-2026) / [Versely 2026](https://www.versely.studio/blog/best-ai-video-generation-models-2026)
- **VRAM 別ローカル I2V 推奨（ComfyUI）**
  - 12GB：Wan2.2 **TI2V-5B fp8** or **I2V-A14B GGUF Q4_K_M ＋ lightx2v 4-step**、480p・49〜81 frames・16fps。
  - 16GB：I2V-A14B fp8（block swap）or GGUF Q5/Q6 ＋ lightx2v、480〜720p・81 frames。LTX-2.3 fp8＋オフロードも可。
  - 24GB：I2V-A14B fp8 両エキスパート常駐、720p・81〜121 frames、SeedVR2 3B で後段アップスケール。
- **ループ・差分・メイキング**：ループは開始/終了フレームを同一画像にする first-last-frame 系ノード（Wan FLF）で作り、動きは髪・光のみ。表情/衣装差分は Crop&Stitch inpaint＋seed 固定、または `variation_seed`。「before/after」「メイキング」は rgthree `Image Comparer` のスライダー画面録画や、txt2img → hires → detailer → upscale の各段を並べた 4 枚投稿が X で伸びやすい。

## 7. X 投稿向け画像仕様（2026 年）

- **上限**：画像 1 枚あたり約 **5MB**（GIF 15MB）、PNG/JPEG/GIF/WebP。仕様は予告なく変わるため公式ヘルプで再確認推奨。出典: [ハッシンラボ 2026](https://hasshin-lab.comtri.jp/x-image-size-guide/) / [フーモア 2026/6](https://manga-whomor.com/column/xtwitterillustsize/)
- **再圧縮**：X は JPEG に再エンコードしがちで、特にモバイル閲覧で劣化が目立つ。**PNG がそのまま残る条件は「透過（アルファ）を含む」こと**で、全面不透明の大判 PNG は JPEG 化される（1px の透過ドット等の回避策が定番、長辺は 4096px 程度が上限、要確認）。実務的には「sRGB・長辺 2048〜4096・JPEG q90〜92 で 1〜3MB」か「透過 1px 入り PNG ≤5MB」の 2 択。出典: [Qiita: ほぼ劣化なしで PNG 投稿](https://qiita.com/Navier/items/51b29fe81321644ea808) / [MamePress](https://mamepress.jp/compress-image-twitter)
- **アスペクト比とクロップ**：1 枚投稿は 16:9〜 4:5 程度は概ね全体表示、極端な縦長は TL でクロップされ「開いて見る」前提になる。**複数枚は正方形寄りタイルに自動トリミング**：2 枚＝左右分割（各 ≈8:9）、3 枚＝左 1＋右上下 2、4 枚＝2×2。重要要素は中央に置き上下左右 20% を安全マージンに。出典: [フルスピード 1〜4 枚の見え方](https://growthseed.jp/experts/sns/twitter-image-size/) / [アドネスラボ 2026](https://addness.co.jp/media/ximage-size/)
- **メタデータ**：アップロード時に EXIF / PNG tEXt（A1111 の parameters、ComfyUI の workflow JSON）は基本除去される。公開したくない設定は**投稿前に自分で消す**方が確実。
- **C2PA / AI ラベル**：2026 年初頭から X は画像内の C2PA と IPTC digital source type を読み取り、**「Made with AI」ラベル**を付与（自己申告トグル＋自動付与）。ローカル SD/ComfyUI 出力は通常 C2PA を持たないが、**自己申告での明示が無難**。出典: [X の AI ラベル解説](https://aimetadatacleaner.com/blog/x-twitter-ai-content-labeling-detection-guide) / [Made with AI ラベル (PrivyClean)](https://www.privyclean.app/x-made-with-ai-label)
- **透かし・署名**：可視サイン＋「無断転載・加工・学習禁止」の文言を入れる。出典: [PUIZU 対策まとめ](https://puizu.com/illust-ai-measures/) / [ノイズ・透かしの入れ方](https://kiri-hana.com/ai-illust/) / [転載禁止表記の限界](https://umakose.com/notes/unauthorized-reproduction)

## 推奨パイプライン A（Illustrious・WebUI 版：A1111 / Forge / Forge Neo）

1. **txt2img**：WAI-illustrious v16/17 等。832×1216 または 1024×1536。Euler a（または DPM++ 2M SDE Karras）、28 steps、CFG 5〜5.5、Clip skip 1〜2。プロンプト＝品質タグ→ キャラ固定文 → ポーズ・画角 → 光（`backlighting, rim lighting, god rays`）→ 背景。負＝`worst quality, low quality, bad anatomy, bad hands, extra digits, watermark`。
2. **ControlNet**（任意）：OpenPose（DWPose 前処理、weight 0.7〜0.9、end 0.6）＋Depth（weight 0.4）で構図固定。複数キャラは Forge Couple Basic。
3. **Hires.fix**：R-ESRGAN 4x+ Anime6B（or 4x-AnimeSharp）、×1.5、hires steps 15〜20、denoise 0.4（線を守るなら 0.35）。Detail Daemon 拡張は amount 0.1〜0.2、start 0.2 / end 0.8。
4. **ADetailer**：1st `face_yolov8s` denoise 0.35、mask blur 8、inpaint only masked、padding 32。2nd `hand_yolov8n` denoise 0.4（崩れが大きい手は OpenPose 手＋inpaint で手動修正）。
5. **img2img → Ultimate SD Upscale**：×2（最終 2048×3072 前後）、upscaler 4x-AnimeSharp / UltraSharpV2、tile 1024、padding 32、mask blur 16、denoise 0.25（ControlNet Tile 併用時は 0.4〜0.5）、seams fix = Band pass。
6. **仕上げ**（Photoshop/Krita/CSP）：トーンカーブ（浅い S）→ グラデーションマップ Soft Light 15% → グロー Screen 10% → 色収差 1〜2px → 粒子ノイズ 3% → サイン。
7. **書き出し**：sRGB、長辺 3072〜4096、JPEG q92（≤5MB）または透過 1px 入り PNG。メタデータは書き出し時に除去。

## 推奨パイプライン B（ComfyUI・Anima 版）

1. **ロード**：`UNETLoader`（anima-base / aesthetic / turbo）、`CLIPLoader`（qwen_3_06b_base、type=stable_diffusion）、`VAELoader`（qwen_image_vae）。shift は内部既定 3.0（明示するなら ModelSamplingAuraFlow 3.0）。
2. **プロンプト**：`masterpiece, best quality, score_7, safe,` ＋ 自然文で情景 ＋ Danbooru タグ補強（小文字・空白区切り、絵師は `@name`）。負＝`worst quality, low quality, score_1, score_2, score_3, artist name`。Turbo/CFG 1 運用時は `ComfyUI-Anima-NAG`（scale 2.0, tau 2.5, alpha 0.5, end 0.5）。
3. **サンプリング**：探索＝Turbo v1.1、8〜12 steps、CFG 1。本番＝Aesthetic / Base、30〜35 steps、CFG 4〜4.5、er_sde または euler＋simple。832×1216 / 896×1152 / 1024×1536。複数キャラは `AttentionCouplePPM`／Forge Neo なら Forge Couple。ポーズは Anima ControlNet-LLLite（`ModelPatchLoader` → `AnimaLLLiteApply`、strength 0.6〜0.8）。
4. **Detailer**：Impact `FaceDetailer`（Anima モデル、guide_size 384〜512 / max_size 1024 / denoise 0.35〜0.45、crop を 32 の倍数に整列）。目の 2 パス目は `Detailer (SEGS)` で eyes 検出器＋denoise 0.3。
5. **アップスケール**：(a) 同モデルで 1.25〜1.5x の 2nd pass（denoise 0.28〜0.35）；(b) それ以上は `USDU+CNtile`＋Anima Tile&Repair LLLite v2 で ×2、tile 1024；または (c) SeedVR2 3B fp8（`batch_size 1`、VRAM 12〜16GB）。
6. **色調**：`Color Match`（参照＝ステップ 3 出力）→ `Film Grain` 弱 → `SaveImage`（workflow JSON が PNG に埋め込まれる点に注意し、投稿用は別途書き出し）。

## 推奨パイプライン C（Anima → Illustrious 二段構成）

1. **Anima で構図・キャラ決定**（B の 1〜3）。自然文の追従力で「ポーズ・小物・多人数の配置・カメラ」を確定。Turbo で seed 探索 → Aesthetic で 1 枚確定。
2. **pixel 受け渡し**：`VAEDecode`（Qwen-Image VAE）→ `ImageUpscaleWithModel`（4x-AnimeSharp）→ `ImageScale`（1024×1536 など）→ 必要なら WD14 tagger で自動タグ化し Illustrious 用プロンプトへ翻訳。
3. **構図ロック**：Anima 出力から `AnimeLineart` or `DWPose` を抽出し、Illustrious 用 ControlNet（union-promax lineart/tile or windsingai tile）を weight 0.5〜0.7 で適用。
4. **Illustrious で img2img refine**：`VAEEncode`（SDXL VAE fp16-fix）→ `KSampler`（WAI 系＋キャラ LoRA、Euler a、30 steps、CFG 5、**denoise 0.4〜0.5**。塗りを大きく変えたいときのみ 0.55〜0.6＋ControlNet 強め）。
5. **Detailer**：Illustrious で `FaceDetailer`（denoise 0.35）→ 手は Crop&Stitch inpaint（Fooocus inpaint patch、denoise 0.6〜0.8、OpenPose 手つき）。
6. **最終アップスケール**：USDU ×2（denoise 0.25〜0.35）or SeedVR2。
7. **色調復元**：`Color Match`（参照＝Anima 出力）でパレットを一段目に寄せる／逆に Illustrious の塗りを活かすなら参照を四段目に。
   - 逆順（Illustrious t2i → Anima i2i）は「Illustrious LoRA 資産を活かしつつ Anima の質感を得る」目的で Civitai に実例あり。denoise 0.35〜0.45 が目安。

## 作品の魅力を一段上げる技術 Top 20

1. Turbo で seed/構図を 50 枚回し、Aesthetic で 1 枚に絞る「探索と本番の分離」。
2. 主光源＋rim light＋fill light の三点ライティングをタグで明示（`backlighting, rim lighting`）。
3. テーマカラー 1〜2 色＋補色アクセントの限定パレットと、仕上げのグラデーションマップ。
4. 被写界深度（`depth of field, blurry foreground`）で視線を顔に集める。
5. あおり／俯瞰／ダッチアングルと広角・望遠の使い分けで「写真的」構図に。
6. 風・髪・水飛沫・モーションブラーで静止画に時間を入れる。
7. 小物と背景の生活感で物語を語らせる（`holding …`, 散らかった机, 街の看板）。
8. 表情は Detailer 段で `half-closed eyes / light smile / parted lips` を微調整。
9. Hires.fix は ESRGAN 系 ×1.5・denoise 0.35〜0.5 を基本、latent は denoise ≥0.55 で。
10. FaceDetailer は denoise 0.3〜0.45、目は別パス、手は OpenPose 手＋inpaint。
11. Detail Daemon / Lying Sigma は SDXL で「弱く」（<0.25 / -0.03）が上限。
12. USDU は denoise 0.25〜0.35＋Band pass、ControlNet Tile で 0.5 超えを解禁。
13. SeedVR2 は 2D で目が鮮鋭になる一方で細部が変わるため線画の忠実性を必ず比較。
14. 二段構成は latent 不可・pixel 受け渡し＋Color Match が鉄則。
15. Regional（Forge Couple / RegionalSampler）は ControlNet で構図固定してから使う。
16. LoRA は Illustrious なら dim 32〜64・LR 1e-4〜5e-4・1500〜3000 steps・WD14 タグ整理で「顔だけ過学習」を避ける。
17. LoRA なし固定は「属性タグ固定文＋seed＋variation_seed＋Reference/IP-Adapter」の四点セット。
18. AI 感の除去は「テカリ抑制・粒子ノイズ・微小色収差・線画強調・トーンカーブ」の手仕上げ。
19. X は多枚投稿を正方形タイル化するため、中央安全域 20% と同一比率で作る。JPEG q90 前後 ≤5MB か透過 1px PNG。
20. 動画化は Wan 2.2＋lightx2v 4-step で「髪と光だけ動く」ループ、SeedVR2 で顔を再鮮鋭化、AI ラベルは自己申告で明示。

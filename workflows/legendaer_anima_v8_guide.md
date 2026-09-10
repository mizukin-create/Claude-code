# Legendaer 版「Anima Preview Workflow」V8（Basic / Standard / Advanced / Detailer）の使い方

JANIMA のモデルカードが推奨している Civitai の Legendaer 氏のワークフロー（`AnimaBasicV8.json` など 4 本）を構造解析して、初回の手順と各グループの意味をまとめたもの（2026-09-10、ファイル本体は Civitai から入手）。4 本とも**同じ骨格**で、右に行くほど機能が増える。

## 0. 4 本の違いと選び方

| 版 | ノード数 | 追加されるもの | 用途 |
|---|---|---|---|
| **Basic** | 54 | txt2img（img2img 切替）、顔・目・手・NSFW の 4 つの ADetailer、Hires（前後 2 か所）、2nd サンプラー、全体 Detailer、CFGZeroStar | **まずこれ**。依存パックが最少 |
| Standard | 76 | ＋ LoRA Manager、A1111 互換メタデータ付き保存（Image Saver）、Before/After 比較スライダー、後処理（コントラスト・レベル・粒子・VHS など） | 日常運用 |
| Advanced | 140 | ＋ Ultimate SD Upscale 2x、Color Match、背景除去、署名合成、SAM 3.1 の任意部位 Detailer、領域プロンプト（Attention Couple）、ControlNet LLLite（深度など）、NegPip | 特定機能が要るとき |
| Detailer | 108 | **既存画像の仕上げ専用**（txt2img なし）。読み込み → 1MP にリサイズ → In/Outpaint（LLLite inpainting）→ 各 Detailer → USDU → 後処理 → 保存 | 過去絵の修正・拡大 |

## 1. 初回に必要なもの

**カスタムノード**（ワークフローを読み込むと赤いノードが出るので、Manager → Install Missing Custom Nodes で一括導入。ComfyUI 本体も最新に更新する。GLSLShader・ModelPatchLoader・AnimaLLLiteApply・ブループリントのサブグラフは新しめのコアが必要）

| パック | 使う版 | 役割 |
|---|---|---|
| ComfyUI-Impact-Pack ＋ Impact-Subpack | 全部 | FaceDetailerPipe、DetailerForEach、ImpactSwitch、ワイルドカード、Ultralytics 検出器 |
| ComfyUI-Easy-Use | 全部 | `easy int`（幅・高さ・steps）、`easy hiresFix`、`easy imageRemBg`、`easy showAnything` |
| rgthree-comfy | 全部 | **Fast Groups Bypasser（機能の ON/OFF パネル）**、Power Lora Loader（Basic）、Image Comparer |
| ComfyUI-KJNodes | 全部 | ImageResizeKJv2、ColorMatchV2、WidgetToString、GetImageSize |
| ComfyUI-Image-Saver | 全部（Basic は Seed のみ） | `SeedNode`、Image Saver Simple / Metadata / Input Parameters |
| comfyui-lora-manager | Standard 以上 | Lora Loader（LoraManager）、TriggerWord Toggle |
| ComfyUI-Custom-Scripts（pysssss） | Advanced / Detailer | MathExpression（署名の位置計算） |
| ComfyUI_UltimateSDUpscale | Advanced / Detailer | 2x タイル拡大 |
| comfyui-ppm | Advanced | CLIPNegPip、AttentionCouplePPM |
| comfyui_controlnet_aux | Advanced | AIO_Preprocessor（Depth など） |

**モデルファイル**（置き場所は ComfyUI/models 以下）

| ファイル | 置き場所 | 用途 | 必須 |
|---|---|---|---|
| `anima_baseV10.safetensors`（JANIMA なら `JANIMAAnima_v10.safetensors`） | diffusion_models | 本体。UNETLoader で選び直す | ◎ |
| `qwen_3_06b_base.safetensors` | text_encoders | テキストエンコーダ | ◎ |
| `qwen_image_vae.safetensors` | vae | VAE | ◎ |
| `4x_foolhardy_Remacri.pth` | upscale_models | Hires と USDU の拡大モデル（無ければ 4x-AnimeSharp 等に変更） | Hires を使うなら |
| `bbox/face_yolov9c.pt` `bbox/hand_yolov9c.pt` `bbox/Eyeful_v2-Individual.pt` | ultralytics/bbox | 顔・手・目の検出（Civitai / HF で配布） | ADetailer を使うなら |
| `segm/ntd11_anime_nsfw_segm_v5-variant1.pt` | ultralytics/segm | NSFW Detailer 用 | 全年齢運用なら不要 |
| `sam_vit_b_01ec64.pth` | sams | Impact Pack が自動 DL | 自動 |
| `anima-lllite-any-test-like-v2.safetensors` / `anima-lllite-inpainting-v2.safetensors` | model_patches | Advanced の ControlNet、Detailer の In/Outpaint（Comfy-Org の Anima LLLite 配布） | 使うなら |
| `sam3.1_multiplex_fp16.safetensors` | checkpoints | Any Detailer（SAM 3.1） | 使うなら |
| `PokemonFont.png` | input | 署名画像（自分のものに差し替え） | 使うなら |

## 2. 画面の見方（全版共通）

- **Control Center**（左上の灰色グループ）: モデル 3 つ、幅・高さ（既定 1024×1536）、バッチ、**POSITIVE / NEGATIVE**（Impact のワイルドカードノード。ここにプロンプトを書く）、LoRA ローダー、Seed、KSampler の設定。Basic は Steps（30）と CFG（4）が単独ノード、Standard 以上は **「Input Parameters (Image Saver)」1 つで steps / cfg / sampler / scheduler / denoise** を持つ（既定 30 / 4 / er_sde / simple / 1.0）。
- **Fast Groups Bypasser**（Control Center 内のパネル）: 水色のグループ（Load Image、各 ADetailer、Hires、2ndSampler、CFGZeroStar、USDU…）が一覧になり、**スイッチで ON/OFF** できる。既定はすべて OFF（バイパス）。Standard 以上は「Post Processing」用のパネルがもう 1 つあり、シアンの後処理グループを切り替える。
- **プロンプトの流れ**: POSITIVE → LoRA のトリガー語を連結 → 先頭・末尾のカンマ除去 → CLIPTextEncode。最終的な文字列は PNG のメタデータに保存される（Standard 以上）。
- **txt2img / img2img の切替**: 「Load Image」グループを ON にすると、ImpactSwitch が読み込み画像の VAEEncode 側（select=2）に切り替わり img2img になる。OFF なら EmptyLatent（txt2img）。img2img のときは denoise を 0.5〜0.7 に下げる（Basic は KSampler の denoise、Standard 以上は Input Parameters の denoise）。
- **Notes** グループ: 光・様式・構図・配色のタグ早見表と、解像度の対応表（Low 1024×1024 ↔ High 1536×1536、896×1152 ↔ 1152×1536、832×1216 ↔ 1024×1536、1344×768 ↔ 1536×864）。既定の 1024×1536 は 832×1216 の高解像度版。速く回すなら 832×1216 にして Hires PostDetailer で 2 倍にする。

## 3. 初回の手順（Basic で）

1. `AnimaBasicV8.json` をキャンバスにドラッグ → 赤いノードがあれば Manager → Install Missing Custom Nodes → 再起動。
2. Control Center の UNETLoader を `JANIMAAnima_v10.safetensors`（または anima-base / aesthetic）に、CLIPLoader を `qwen_3_06b_base.safetensors`、VAELoader を `qwen_image_vae.safetensors` に合わせる。
3. POSITIVE の既定 `newest, masterpiece, best quality, score_7,` の後ろに自分のタグと自然文を書く。JANIMA カードの品質列は `masterpiece, highres, absurdres, newest, best quality, score_7`。Aesthetic 版なら `score_7` を消す。**全年齢運用なら `safe` を足し、NEGATIVE の末尾に `sensitive, nsfw, explicit` を足す**（既定ネガには入っていない）。
4. Width / Height を 832×1216 か 1024×1536 に。Steps 30、CFG 4（JANIMA は 5 前後、Aesthetic は 3〜4）。サンプラーは er_sde / simple のまま。
5. Fast Groups Bypasser は全部 OFF のまま Queue。出力は `output/` に保存（Standard 以上はファイル名 `時刻_モデル名_seed`）。
6. 絵が出たら、Fast Groups Bypasser で **Face ADetailer → Eyes ADetailer → Hand ADetailer** の順に ON にして差を見る（それぞれ denoise 0.26 / 0.24 / 0.40、16 steps、CFG 6。EditDetailerPipe に `detailed face` `perfect hands` などの追記語が入っている）。
7. 仕上げの拡大は **Hires PostDetailer**（4x モデル → 50% = 2 倍）。**Hires PreDetailer** は Detailer の前に 2 倍にする用で、両方 ON にすると 4 倍相当になり VRAM を食う。どちらか一方から。
8. 「Detailer」（全画面を denoise 0.24 で 1 回なめる）と「2ndSampler」（denoise 0.2 で再サンプル）は似た効果なので、使うならどちらか。CFGZeroStar は彩度が飛ぶときに試す。
9. NSFW ADetailer は全年齢運用では OFF のまま（検出モデルも不要）。

## 4. 各グループの意味（既定値）

| グループ | 中身 | 既定 |
|---|---|---|
| Load Image | LoadImage → ImageResizeKJv2（幅・高さに合わせて pad）→ VAEEncode。ON で img2img | OFF |
| KSampler | 本体。30 steps / CFG 4 / er_sde / simple / denoise 1.0 | ON |
| CFGZeroStar | ガイダンスの補正パッチ | OFF |
| 2ndSampler | 16 steps / CFG 4 / denoise 0.2 の再サンプル | OFF |
| Hires PreDetailer / PostDetailer | `easy hiresFix`: 4x_foolhardy_Remacri で 4 倍 → 50% に縮小（= 2 倍）。サンプリングはしない | OFF |
| Face / Eyes / Hand / NSFW ADetailer | FaceDetailerPipe ＋ Ultralytics 検出器。guide 512 / max 1536 / crop 2.5（Detailer Settings で共通） | OFF |
| Detailer | 全画面マスク → DetailerForEach（18 steps / CFG 6 / denoise 0.24） | OFF |
| Detailer Settings / Use SAMLoader | 上記の共通設定と SAM（境界の精度） | ON |
| Save Image | 保存 | ON |
| Post Processing（Standard 以上） | Contrast 1.1、Image Levels、Morphology（erode 3）、Edge-Preserving Blur、Quantize 256、Chromatic Aberration、Sharpen、Film Grain、VHS TV。Advanced はさらに Pixelation / Digital Glitch / Night Vision / Blueprint / Frosted Glass / Gameboy の GLSL シェーダー | OFF |
| Ultimate SD Upscaler（Advanced / Detailer） | 2 倍、dpmpp_2m_sde / karras、18 steps、CFG 6、denoise 0.16 | OFF |
| Color Match / Remove Background / Apply Signature（Advanced / Detailer） | 色合わせ（mkl）、BEN2 で背景除去、署名 PNG を X/Y 位置に合成 | OFF |
| Any Detailer (SAM 3.1)（Advanced / Detailer） | 文字で指定した部位を SAM 3.1 で切り出して Detailer | OFF |
| Regional Prompting（Advanced） | 赤・緑・青のマスク画像 3 枚と 3 つのプロンプトを Attention Couple で合成 | OFF |
| ControlNet LLLite（Advanced） | 参照画像 → AIO_Preprocessor（DepthAnythingV2）→ AnimaLLLiteApply（強さ 0.9、0〜0.9） | OFF |
| CLIP NegPip（Advanced） | プロンプト内で負の重みを使えるようにする | ON |
| In/Outpaint（Detailer 版） | LLLite inpainting パッチ、ImagePadForOutpaint（余白 0、ぼかし 96）、KSampler seed 42 固定 / 30 steps / CFG 3 | OFF |

## 5. よくある詰まり

- ノードが赤い → Manager で不足パックを入れて再起動。それでも赤いなら ComfyUI 本体が古い。
- 「model not found」→ ローダーの選択肢に無い。ファイル名と置き場所を確認して選び直す。
- 何も変わらない → そのグループが OFF（バイパス）のまま。Fast Groups Bypasser で ON にする。
- VRAM 不足 → 1024×1536 を 832×1216 に、Hires Pre を OFF、Detailer の Max Size を 1024 に。
- 顔が変わりすぎる → Face ADetailer の denoise を 0.2 に。手が直らない → Hand の denoise を 0.45〜0.5 に、それでも駄目なら Hires Pre を ON にして高解像度で検出させる。
- ワイルドカードノードの 2 段目は「展開後の文字列」。`{a|b}` や `__name__` を使わないなら気にしなくて良い。LoRA は `<lora:名前:0.8>` をここに書ける（Standard 以上は LoRA Manager からも読める）。

## 6. この手元のワークフローとの使い分け

- 画風の当たりを付ける → `workflows/anima_style_test.json`（同一 seed 8 様式）。
- 構図を Anima で作って Illustrious で仕上げる → `workflows/anima_to_illustrious_2stage.json`。
- 1 枚を丁寧に仕上げる → Legendaer 版 Basic（ADetailer ＋ Hires Post）。過去絵の修正 → Detailer 版。

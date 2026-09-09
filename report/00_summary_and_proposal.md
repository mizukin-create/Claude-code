# 00. 結論と提案 — 魅力的なAIイラストを作り、Xで伸ばすための戦略（2026年9月版）

対象: みー@AIイラスト（@mi_Create_mi）／ Windows PC ／ Stable Diffusion WebUI（Illustrious 系）＋ ComfyUI（Anima）／ 主に2次元美少女
作成日: 2026-09-09
この文書は、5本の調査レポート（01〜05）の結論を統合し、具体的な「プロンプト」「ワークフロー」「投稿運用」の提案に落とし込んだものです。事実と出典は各レポートに、判断と提案はここにまとめています。

> **調査の制約（先に明記）**: このセッションのネットワークでは X 本体・note・pixiv・Civitai・Hugging Face・docs.comfy.org への直接アクセスが遮断されていたため、X の個別投稿や @mi_Create_mi の作品そのものは分析できていません。X のアルゴリズムは GitHub 上の公開コード（xai-org/x-algorithm）を一次資料として確認し、それ以外の多くは検索エンジン経由の二次情報です。数値は「要検証」の前提で読み、自分の環境と X アナリティクスで必ず確かめてください。

---

## 1. 現状の整理

| 項目 | 把握できたこと（検索スニペット由来） |
|---|---|
| アカウント | 2022年12月開設、フォロワー 3,000 人超。趣味で AI イラスト制作、キャラクターイラストのリクエスト受付 |
| 販路 | Booth（直近は非公開状態）／ PicSpace ／ pixivFANBOX「mizu-ai」／ R-18 は pixiv・Patreon |
| 作品傾向 | pixiv に原神（#GenshinImpact）タグの作品あり。オリジナルと二次創作の比率、画風、投稿頻度は未確認 |
| 環境 | SD WebUI（Illustrious）＋ ComfyUI（Anima） |

公開情報で確認できる「2次元 AI 美少女」系の上位層は数千〜5万フォロワー帯です（01 参照）。3,000 人は「次の壁 = 1万人」の手前にいる、伸びしろの大きい位置です。

---

## 2. 調査から見えた「伸びる作品」の条件

### 2.1 X のアルゴリズム（一次資料: xai-org/x-algorithm、2026-09-09 取得）

| 行動 | 重み | 作品づくりへの含意 |
|---|---|---|
| リンクコピー共有 | 20.0 | 「人に送りたくなる」1枚（一言で伝わる可愛さ・面白さ・季節感） |
| 返信 / 引用 / DM 共有 | 各 5.0 | 「一言言いたくなる」余白（どっちが好き？ / セリフ / 差分） |
| 作者フォロー | 4.0 | 「次も見たい」連載性（同じキャラ・同じ様式・同じ時間） |
| いいね | 0.5 | いいねは最弱のシグナル。いいね数を追わない |
| 報告 | −234 | 反 AI 層を刺激しない。AI 表記とゾーニングは守り |
| 相互フォロー相手の返信 | +15 | 界隈との相互交流が数値上の実利になる（2026/7〜） |

さらに重要な構造:
- **NSFW 作者ラベル**が付くと、全メディア投稿が警告表示になり、非フォロワーへの推薦から除外される。→ 本垢は全年齢固定、R-18 はサブ垢に完全分離。
- **ハッシュタグ**はランキング特徴ではない。閲覧者のミュート語に「#」の有無を問わず一致する。→ 0〜2 個。「#AIイラスト」は反 AI 層の TL から自動的に外れるゾーニング装置として機能する。
- **自己リプ連鎖・圏外の返信**は For You から落ちる。→ 主投稿に全部入れる（差分は 2〜4 枚目）。ツリーは既存フォロワー向け。
- **同一作者の連投**は 2 件目以降 0.5 倍。→ 時間を空ける。

### 2.2 伸びているアカウントの 3 類型（01 参照）
1. **オリキャラ固定の連載型**（同一キャラを毎日・同時刻に投稿。1年でフォロワー10倍の事例）
2. **技術解説・記事併用型**（作品＋プロンプト/設定の解説で信頼と拡散を得る）
3. **様式差別化型**（セミリアル・レトロ・水彩など「一目で分かる様式」で埋没を避ける）

### 2.3 2025〜2026 年の画風トレンド（01・04 参照）
- 「ジブリ風」「ドット絵」「90年代セル画」「PC-98」「フィルム粒子・VHS」など、**時代の記号を再解釈した様式**が最もバズりやすい。
- 技術的完成度は差別化にならず、「文脈」「人間的な揺らぎ」「未完成感」に価値が移っている。標準的な「マスピ顔」は埋没する。
- 安定ジャンル（制服・水着・メイド・ふともも）に「季節」と「光」の変数を足すのが王道。
- 2.5D／セミリアルは 2 次元層とグラビア層の両方に届く中間帯として強い。
- 逆風: 2026 年 8 月に「AI 生成イラストの増加への不満」が可視化。**手・目・文字の破綻ゼロ**と **AI 表記**が「伸びる前提条件」になった。

### 2.4 統合仮説「魅力の方程式」

> 魅力 ＝ **様式**（一目で分かる） × **光と色** × **表情・仕草の情報量** × **破綻ゼロ** × **文脈（物語）**

| 要素 | プロンプトでの担保 | ワークフローでの担保 |
|---|---|---|
| 様式 | 年代タグ（newest/recent/mid/early）、画風タグ（retro artstyle / anime screencap / watercolor / flat color）、Anima は `@artist` の代わりに様式タグ＋自然文 | 派生モデルの選択（WAI / Hassaku / Nova / RouWei）、自作画風 LoRA |
| 光と色 | 光タグを毎回 1 つ（backlighting, rim lighting, dappled sunlight, light rays, neon lights）、限定パレット（limited palette, spot color） | 仕上げのトーンカーブ・グラデーションマップ、Color Match |
| 表情・仕草 | 表情は「目・口・眉/頬」の 3 軸で指定、仕草タグ（head tilt, hand on own cheek, looking back） | FaceDetailer / ADetailer で目と口を再描画（denoise 0.3〜0.45） |
| 破綻ゼロ | 手を隠すポーズ、`bad hands` の積み増しに頼らない | ADetailer hand → OpenPose 手＋inpaint、Hires.fix、最終チェック |
| 文脈 | 小物（holding …）、場所・時間帯・天候、自然文で「何をしている瞬間か」 | Anima の自然文追従で構図を確定 → Illustrious で塗り |

---

## 3. 提案 A: コンテンツ戦略「1 キャラ・1 様式・3 枠」

### 3.1 主役オリキャラを 1〜2 体つくる
- 名前・年齢感・性格・定番衣装・髪型・目・「個性づけ 1 点」（例: mole under eye / hair intakes / heterochromia）を設定シートにする。
- 「固定プロンプト文」（`prompts/` に例）を作り、毎回コピーする。LoRA なしでも一貫性は上がる。安定したら Illustrious 用キャラ LoRA を学習（04 §5）。
- 原神などの二次創作は続けても良いが、**主軸はオリキャラ**にする理由: (1) 炎上リスクが最小、(2) 「作者フォロー」の予測を最も押し上げる、(3) 記念日・季節ネタを全部このキャラで消化できる、(4) 販売・依頼の導線が「このキャラの人」で説明できる。

### 3.2 署名となる「様式」を 1 つ決める（2 週間ずつ試して数字で決定）
候補（いずれも Illustrious と Anima の両方で作れる）:
1. **レトロアニメ × 現代の光**: `retro artstyle, 1990s \(style\), anime screencap, cel shading` に `backlighting, lens flare, film grain` を足す。トレンド適合度が最も高い。
2. **水彩・アナログ × 日常**: `watercolor \(medium\), traditional media, limited palette` × 教室・カフェ・雨。「揺らぎ」「未完成感」路線。
3. **セミリアル × 映画的ライティング**: 2.5D 派生モデル（Nova Anime3D 等）× `cinematic lighting, volumetric lighting, depth of field`。グラビア層にも届く中間帯。

判断基準: 2 週間・各 6 投稿で「いいね率（いいね÷インプ）」「返信率」「フォロワー増」を比較し、最も反応が良い様式を固定。残り 2 つは「単発バズ枠」の実験に回す。

### 3.3 投稿を 3 枠に分ける
| 枠 | 週あたり | 内容 | 狙う行動 |
|---|---|---|---|
| 連載枠 | 3 | 主役キャラ × 固定様式 × 日常の一瞬 | フォロー、滞在 |
| 単発バズ枠 | 1 | 記念日・季節・様式実験・4 枚組メイキング | リンクコピー、引用、共有 |
| 交流・企画枠 | 1 | 差分投票、お題募集、フォロワー記念 | 返信、DM 共有 |

---

## 4. 提案 B: プロンプト戦略

### 4.1 両モデル共通の 7 原則
1. **品質タグは最小限**。Illustrious: `masterpiece, best quality, very aesthetic, absurdres`＋モデル固有（WAI は `amazing quality`）。Anima Base: `masterpiece, best quality, score_7`。**Anima Aesthetic は score_* をポジ・ネガとも外す**。
2. **レーティングを固定**。Illustrious: ポジ `general`（NoobAI 系は `safe`）＋ネガ `nsfw`。Anima: ポジ `safe`＋ネガ `sensitive, nsfw, explicit`。
3. **光タグ 1 つ＋画角タグ 1 つ**を毎回必ず入れる（`prompts/wildcards/lighting.txt` `camera.txt`）。
4. **表情は 3 軸**（目・口・眉/頬）。`smile` 単発は効かない。
5. **様式は年代タグ・画風タグで指定**する。Illustrious: `newest / recent / mid / early`、`1990s \(style\)`、`anime screencap`、`watercolor \(medium\)`。Anima: `retro artstyle`、`anime coloring`、`anime screenshot`、`flat color`。
6. **絵師名は公開作品で使わない**（倫理・炎上・報告リスク）。使うなら 2〜3 人を弱めにブレンド（Illustrious: `BREAK (a:0.6), (b:0.5)`）、または自作画風 LoRA に置き換える。
7. **オリキャラ固定文をテンプレ化**し、Illustrious では先頭 75 トークン内に置く。Anima では名前の直後に必ず外見を書く。

### 4.2 モデルの使い分け

| 用途 | 推し | 理由 |
|---|---|---|
| 連載枠の日常 1 枚（速さ・塗りの安定） | Illustrious 派生（WAI v17 / Hassaku v3.4） | 塗り・背景・LoRA 資産・ADetailer 込みの手数の少なさ |
| 構図が複雑（複数人、位置関係、小物、カメラ指示） | Anima（Turbo で探索 → Base/Aesthetic で本番） | 自然文の追従、複数人の書き分け、LLLite による構図固定 |
| 背景込みの一枚絵・キービジュアル | Nova Anime XL（Illustrious）または Anima → Illustrious 二段 | 背景描写と光の豪華さ |
| 自然文で細かく構図を操作したい（WebUI のまま） | RouWei 0.8（Illustrious 派生） | タグ＋自然文混在に最適化 |
| 90 年代セル画・レトロ様式 | Illustrious（年代タグ・`retro artstyle`）／ Anima（`retro artstyle, anime screenshot`） | 両方可。派生モデル Nova Retro Anime も選択肢 |

### 4.3 プロンプトの「型」（詳細と 5 パターン各 → `prompts/`）

Illustrious（タグ順: 人数 → キャラ固定文 → ポーズ/画角 → 表情 → 場所/時間 → 光 → 様式 → 品質/年代/レーティング）:
```
1girl, solo, [オリキャラ固定文], upper body, from side, looking at viewer,
light smile, half-closed eyes, blush, head tilt,
rooftop, sunset, orange sky, backlighting, rim lighting, wind, floating hair, depth of field,
anime screencap, masterpiece, best quality, very aesthetic, absurdres, newest, general
```
ネガ: `worst quality, low quality, lowres, bad anatomy, bad hands, extra digits, fewer digits, jpeg artifacts, signature, watermark, username, text, nsfw`

Anima（タグで骨格 → 自然文 2 文で「光・動き・気持ち」）:
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, [オリキャラ固定文], upper body, looking at viewer, light smile, half-closed eyes, blush, rooftop, sunset, backlighting, rim lighting, wind, floating hair, anime coloring.
She looks back at the viewer from a school rooftop at sunset, the low sun behind her outlining her hair with warm light. The city below fades into haze and her skirt flutters in the wind.
```
ネガ: `worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit`

### 4.4 「AI っぽさ」を消す具体策
- `shiny skin` / `very aesthetic` の積みすぎをやめ、CFG を 4〜5 に下げ、Hires denoise は 0.3 台。
- `film grain` / `flat color` / 年代タグ / `traditional media` で質感を崩す。
- 個性づけタグ（mole under eye, thick eyebrows, asymmetrical bangs, tareme/tsurime）で「マスピ顔」から離す。
- 仕上げは手作業: トーンカーブ（浅い S）→ グラデーションマップ Soft Light 10〜25% → グロー Screen 10% → 色収差 1〜2px → 粒子ノイズ 2〜4% → サイン。

---

## 5. 提案 C: ワークフロー

### 5.1 3 本のパイプラインと使い分け（詳細 → `report/04_quality_pipeline.md`）

| パイプライン | 使う枠 | 流れ |
|---|---|---|
| **A: Illustrious / WebUI** | 連載枠（週 3） | txt2img 832×1216 → Hires ×1.5（Anime6B / AnimeSharp, denoise 0.35〜0.45）→ ADetailer 顔 0.35 → 手 0.35〜0.4 → 必要なら Ultimate SD Upscale ×2（denoise 0.25）→ 仕上げ → 書き出し |
| **B: Anima / ComfyUI** | 構図重視・複数人・シーン | Turbo（8〜10 steps, CFG 1）で seed/構図を 30〜50 枚探索 → Base/Aesthetic（30〜35 steps, CFG 4〜4.5, er_sde/simple）で本番 → 1.25〜1.5x 2nd pass（denoise 0.28〜0.35）→ FaceDetailer（crop 32 の倍数）→ 2x ESRGAN。構図固定は LLLite（depth/pose/lineart） |
| **C: Anima → Illustrious 二段** | 単発バズ枠の勝負作 | Anima で構図確定 → VAEDecode（pixel 受け渡し必須）→ 4x-AnimeSharp → 1024×1536 に整形 → Illustrious ControlNet（lineart/tile, 0.5〜0.7）→ img2img denoise 0.4〜0.5 → FaceDetailer → USDU ×2 → Color Match |

### 5.2 標準設定（まずこの値から X/Y/Z plot で自分の基準値を決める）

| | Illustrious（eps 系派生） | Anima Base v1.0 | Anima Aesthetic v1.1 | Anima Turbo v1.1 |
|---|---|---|---|---|
| Sampler / Scheduler | Euler a（DPM++ 2M Karras） | er_sde / simple | er_sde / simple | euler / simple |
| Steps | 28 | 30〜40 | 30〜35 | 8〜12 |
| CFG | 6（LoRA 併用 4.5） | 4〜5 | 3.5〜4 | 1 |
| 解像度 | 832×1216 | 832×1216 / 896×1152 | 同左 | 同左 |
| Hires | ×1.5, denoise 0.35〜0.45 | ×1.25〜1.5, denoise 0.28〜0.35 | 同左 | 同左 |
| ネガ | 短く、`nsfw` 必須 | score_1〜3 入り | score_* 無し | 実質無効（NAG で代替） |
| Clip skip | 1 | — | — | — |

v-pred 系（Illustrious v3.5-vpred / NoobAI-vpred / RouWei-vpred）を試すなら reForge / Forge Neo で ZTSNR ON、CFG 4、Rescale CFG 0.6。

### 5.3 同梱ファイル
- `workflows/anima_t2i_hires.json`: Anima 用 ComfyUI ワークフロー（コアノードのみ、カスタムノード不要）。txt2img → 1.25x 2nd pass → 2x ESRGAN。Turbo LoRA ノードは既定でバイパス。
- 構図固定・インペイントは ComfyUI のテンプレートブラウザにある公式「Anima Lllite: Depth Control to Image」「Any Control to Image」「Image Inpainting」を使う（ModelPatchLoader → AnimaLLLiteApply）。
- `prompts/illustrious_templates.md` / `prompts/anima_templates.md`: 5 パターンのテンプレとタグ辞典。
- `prompts/wildcards/`: Dynamic Prompts 用（光・画角・表情・衣装・季節・様式・髪型）。

### 5.4 環境更新チェックリスト
- [ ] Illustrious 派生を最新に（WAI-illustrious v17、Hassaku v3.4、Nova Anime XL v19、RouWei 0.8 のいずれか 2 つ）
- [ ] Anima を Base v1.0 ＋ Aesthetic v1.1 ＋ Turbo v1.1（または Turbo LoRA v0.2）に更新。LLLite（depth / pose / lineart / inpainting）を `models/model_patches/` に配置
- [ ] ComfyUI を最新に（AnimaLLLiteApply は v0.29.0 以降）
- [ ] アップスケーラー: 4x-AnimeSharp、R-ESRGAN 4x+ Anime6B、2x-AnimeSharpV4
- [ ] WebUI: ADetailer、Regional Prompter または Forge Couple、Dynamic Prompts、Tag Autocomplete、ControlNet（xinsir union-promax、Illustrious openpose/tile）
- [ ] ComfyUI: Impact Pack＋Subpack（FaceDetailer）、Ultimate SD Upscale、KJNodes（Color Match）、rgthree、ComfyUI-Anima-NAG（Turbo 用）、comfyui_controlnet_aux（DWPose / AnimeLineart / Depth Anything）
- [ ] Forge Neo を入れると WebUI 側でも Anima＋Forge Couple＋LLLite が使える（任意）

---

## 6. 提案 D: X 運用

### 6.1 週間プラン（週 5 投稿、JST）
| 曜日 | 時刻 | 枠 | 内容 |
|---|---|---|---|
| 月 | 21:00 | 連載 | 主役キャラ新作 1 枚（縦長 3:4〜2:3） |
| 水 | 12:15 | 交流 | 表情・衣装差分 2〜3 枚を 1 投稿に（「どれが好き？」） |
| 木 | 21:00 | 連載 | 週のメイン作品（記念日があればそのネタで） |
| 土 | 21:00 | 単発 | 様式実験 or 4 枚組メイキング or 5〜10 秒ループ動画 |
| 日 | 14:00 | 連載/企画 | シリーズ回 or 月 1 の企画（お題募集・投票） |
| 毎日 | 随時 | 交流 | 界隈への内容ある返信 10〜20 件。投稿後 30〜60 分は返信に即応 |

### 6.2 投稿の作法
- ハッシュタグは 0〜2 個: `#AIイラスト` ＋ `#AIart`。記念日は当日のみ差し替え。`#AIグラビア` `#AI美少女` はサブ垢専用。技術系タグ（#Illustrious #ComfyUI）は解説投稿だけ。
- 本文に外部リンクを置かない。リンクは固定ポスト・プロフィール・自己リプへ。
- 本文またはプロフィールに「AI 生成（Illustrious / Anima）」を明記。Community Notes を先回りする。
- 絵師タグ・ファンアートタグ・版権キャラ名タグは使わない。
- 画像: sRGB、長辺 2048〜4096、JPEG q90〜92（≤5MB）または透過 1px 入り PNG。複数枚は正方形タイルにトリミングされるので主役を中央、上下左右 20% を安全域に。生成メタデータは書き出し時に除去。
- 動画: 週 1 本、5〜10 秒ループ（髪と光だけ動かす）。Wan 2.2＋lightx2v 4-step（12〜16GB VRAM）または Grok Imagine / Kling。顔は SeedVR2 で再鮮鋭化。

### 6.3 プロフィールと導線
- 自己紹介: 「AI 生成（Illustrious / Anima）」「主役キャラ名」「投稿ペース」「R-18 はサブ垢 @xxx」。
- 固定ポスト: 代表作 4 枚＋各リンク（PicSpace / FANBOX / pixiv）。Booth が非公開のままなら固定ポストとプロフィールから外し、PicSpace と FANBOX に一本化して迷いを無くす。
- ヘッダー: 主役キャラ。アイコンも主役キャラで統一。
- 本垢は全年齢固定（水着まで・肌面積控えめ）。R-18 はサブ垢でセンシティブ設定 ON・プロフに 18+。

---

## 7. 30 日アクションプラン

| 週 | やること | 完了の目安 |
|---|---|---|
| 第 1 週 | 環境更新（§5.4）、主役キャラ 1〜2 体の設定シートと固定プロンプト、プロフィール・固定ポスト・導線の整備、サブ垢分離 | 固定プロンプトで 20 枚出して顔・衣装がブレない |
| 第 2 週 | X/Y/Z plot で基準値確定（CFG 4/5/6 × Hires denoise 0.3/0.4/0.5 × 品質タグ有無）、連載開始（週 3）、界隈 100 人フォロー＋毎日返信 | 週 3 投稿を同時刻に守れた |
| 第 3 週 | 様式実験（候補 3 つを各 2 投稿）、差分投票 1 回、記念日投稿 1 回、Anima LLLite で構図固定した勝負作 1 枚（パイプライン C） | いいね率・返信率で様式を仮決定 |
| 第 4 週 | ループ動画 1 本、企画 1 回、4 枚組メイキング 1 回、アナリティクス見直し（時間帯・枚数・様式の A/B）、キャラ LoRA 学習に着手 | 次月の投稿カレンダーが埋まっている |

---

## 8. 検証と改善ループ（KPI）

| 指標 | 見方 | 目安 |
|---|---|---|
| いいね率（いいね÷インプ） | 作品そのものの魅力 | 1〜3%。様式・光・表情の A/B に使う |
| 返信率・引用率 | 「一言言いたくなる」余白があるか | 差分投票・セリフ投稿で上がるはず |
| プロフィールクリック→フォロー率 | 連載性・固定ポストの出来 | 固定ポスト更新で変化を見る |
| フォロワー増加（週） | 全体の健康度 | 週 +50〜100 を最初の目標に |
| 反応ゼロ投稿の割合 | 新規閲覧者に届いていない | 時間帯を変えて別カットで再投稿 |

4 週間単位で「様式」「時間帯」「枚数」「モデル（Illustrious vs Anima）」を 1 変数ずつ変えて比較する。同時に 2 つ以上変えない。

---

## 9. 要確認事項（本調査で確定できなかったこと）
- @mi_Create_mi の実際の投稿・画風・反応データ（X に直接アクセスできず）。
- Illustrious v3.6 のオープンウェイト配布有無、WAI v17 の 4 段階レーティングタグの正確な語彙。
- Anima の note「108 スタイル比較」記事の本文（検索要約のみ）。
- X の PNG 保持条件・長辺上限、「投稿後 30 分」閾値の有無（公開コードには存在しない）。
- pixivFANBOX の AI 生成コンテンツに関する最新規約（2023 年の禁止以降の改定内容）。

各レポートの「未確認」「要確認」「推測」の表記を、実行前に一次ソースで確かめてください。

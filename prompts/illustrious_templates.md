# Illustrious 系（SD WebUI）コピペ用プロンプトテンプレート（SFW 美少女向け）

根拠と出典は `report/02_illustrious_prompting.md` を参照。数値は必ず自分の環境で X/Y/Z plot により再検証すること。

## 0. 共通設定（eps 系派生: WAI-illustrious v17 / Hassaku v3.4 / Nova Anime XL / Prefect など）

| 項目 | 推奨 |
|---|---|
| Sampler / Scheduler | Euler a（決め打ちで詰めるなら DPM++ 2M Karras） |
| Steps | 28（20〜30） |
| CFG | 6（LoRA 併用時は 4.5、Nova は 4〜6） |
| Clip skip | 1（モデルカードが 2 なら 2） |
| 解像度 | 832×1216（X 向け縦長の定番）/ 896×1152 / 1024×1024 / 1216×832 |
| Hires.fix | ×1.5、R-ESRGAN 4x+ Anime6B または 4x-AnimeSharp、Hires steps 15〜20、denoise 0.35〜0.45 |
| ADetailer | 1st: face_yolov8s（denoise 0.35）→ 2nd: hand_yolov8n（denoise 0.35〜0.4）。目だけ直すなら mediapipe_face_mesh_eyes_only（denoise 0.3） |
| v-pred 系（v3.5-vpred / NoobAI-vpred / RouWei-vpred） | reForge / Forge Neo で ZTSNR ON、CFG 4、Rescale CFG 0.6、Euler、28〜35 steps |

共通ネガティブ（短く始めて症状ごとに足す）:
```
worst quality, low quality, lowres, bad anatomy, bad hands, extra digits, fewer digits, jpeg artifacts, signature, watermark, username, text, nsfw
```

品質タグ（末尾に置く。モデル固有タグはカード推奨に従う）:
```
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
- WAI v17: `masterpiece, best quality, amazing quality`（末尾）＋ネガに `nsfw` 必須
- Hassaku: `masterpiece, best quality, newest, absurdres, highres`
- NoobAI 系: `masterpiece, best quality, newest, absurdres, highres, safe`（`general` の代わりに `safe`）
- Nova Anime XL: `masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest`（背景重視なら `scenery, volumetric lighting` を追加）

## 1. オリキャラ固定文（例）— 先頭 75 トークン内に置く

```
1girl, solo, [キャラ名], long hair, silver hair, blunt bangs, sidelocks, violet eyes, bright pupils, mole under eye, hair ornament, star hair ornament, black sailor collar, white shirt, pleated skirt,
```
- 髪型・髪色・目・特徴・アクセ・定番衣装を「順序固定」で書き、毎回コピーする（LoRA なしでも一貫性が上がる）。
- 個性づけタグ: `mole under eye` / `thick eyebrows` / `asymmetrical bangs` / `tareme` / `tsurime` / `hair intakes` / `ahoge` / `heterochromia`

## 2. 5 パターン

### ① 顔アップ（832×1216 or 1024×1024）
```
1girl, solo, close-up, face focus, portrait, looking at viewer, light smile, parted lips, blush,
long hair, silver hair, hair between eyes, sidelocks, blue eyes, hair ornament, sailor collar,
backlighting, rim lighting, soft lighting, depth of field, blurry background, bokeh, cherry blossoms, petals,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
ADetailer 2nd に `mediapipe_face_mesh_eyes_only`（denoise 0.3）。ネガに `blurry eyes`。

### ② バストアップ（832×1216）
```
1girl, solo, upper body, from side, looking at viewer, smile, head tilt,
medium hair, wavy hair, brown hair, green eyes, white shirt, collared shirt, sleeves rolled up, holding cup, coffee cup,
cafe, indoors, window, dappled sunlight, warm lighting, depth of field,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```

### ③ 全身（832×1216 or 768×1344、Hires ×1.6〜2.0 ＋ ADetailer 必須）
```
1girl, solo, full body, standing, contrapposto, hand on own hip, looking at viewer, smile,
long hair, twintails, black hair, red eyes, school uniform, pleated skirt, black thighhighs, loafers, school bag,
street, crosswalk, city, sunset, orange sky, long shadow, backlighting, lens flare, wide shot, from below,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
ネガ追加: `cropped, extra legs, bad feet`

### ④ 背景重視シーン（1216×832 or 1344×768、Hires ×1.5〜2.0 denoise 0.4）
```
1girl, solo, scenery, wide shot, from behind, looking back, standing, wind, floating hair,
white dress, sun hat, long hair, blonde hair,
sunflower field, blue sky, cumulonimbus cloud, summer, light rays, sunbeam, volumetric lighting, cinematic lighting,
masterpiece, best quality, very aesthetic, absurdres, newest, general
```
`depth of field` は入れない。ADetailer は confidence 0.4・min mask ratio 0.01 で誤検出防止。

### ⑤ 複数人（Regional Prompter Matrix 列 `1,1` / Forge Couple Basic 横）
Regional Prompter 記法:
```
2girls, side-by-side, looking at viewer, park, sunlight, dappled sunlight, depth of field,
masterpiece, best quality, very aesthetic, absurdres, newest, general ADDCOMM
1girl, long hair, blonde hair, blue eyes, white dress, smile, hand up, waving BREAK
1girl, short hair, black hair, brown eyes, black jacket, shorts, grin, hands in pockets
```
Forge Couple なら 1 行目を Global Effect にし、2〜3 行目を左右に。空行禁止。各領域にも `1girl` を書く。ADetailer は face を top-k 2。

## 3. 「魅力」クイックリファレンス（毎回 光×1・画角×1・表情×3軸 を入れる）

| 分類 | タグ |
|---|---|
| 光 | backlighting / rim lighting / sidelighting / dappled sunlight / light rays / sunbeam / lens flare / neon lights / light particles / bloom / cinematic lighting / volumetric lighting / soft lighting |
| 時間・空 | sunset / dusk / night / blue sky / cumulonimbus cloud / overcast / rain / snow |
| 色 | pastel colors / limited palette / monochrome, spot color / high contrast / film grain / chromatic aberration / colorful / gradient background |
| 画角 | from below / from above / from side / from behind, looking back / dutch angle / fisheye / close-up / foreshortening / wide shot / cowboy shot / upper body / portrait / face focus / eye focus / pov / dynamic pose |
| 被写界深度 | depth of field / bokeh / blurry background / blurry foreground / motion blur |
| 表情（目） | half-closed eyes / wide eyes / closed eyes / one eye closed / looking at viewer / looking to the side / looking away / tareme / tsurime |
| 表情（口） | light smile / smile / grin / parted lips / closed mouth / :d / :o / tongue out / pout |
| 表情（眉・頬） | blush / raised eyebrows / furrowed brow / embarrassed / smug / nervous / tears |
| 仕草 | head tilt / hand on own cheek / finger to mouth / hand up / arms behind back / hands in pockets / holding cup / adjusting hair / leaning forward |
| 質感 | detailed eyes / glossy lips / shiny hair / sparkle / floating hair, wind / see-through / translucent / wet |
| 画風・様式 | anime screencap / retro artstyle / 1990s \(style\) / 1980s \(style\) / flat color / watercolor \(medium\) / traditional media / faux traditional media / sketch / impasto / official art / key visual / game cg / pixel art / cel shading / lineart |
| 年代 | newest / recent / mid / early / old |

## 4. 「AI っぽさ」対策
- `shiny skin` `very aesthetic` の積みすぎを避ける。CFG を 4〜5 に下げる。Hires denoise 0.3 台。
- `film grain` / `flat color` / 年代タグ / `traditional media` で質感を崩す。
- 個性づけタグ（mole under eye, thick eyebrows, asymmetrical bangs）で「マスピ顔」から離す。
- 絵師名を X 公開作品で単独使用しない。使うなら 2〜3 人を `BREAK (artist_a:0.6), (artist_b:0.5)` で別チャンクにブレンドし独自の塗りにする。

## 5. Dynamic Prompts での差分量産（`prompts/wildcards/` を `extensions/sd-dynamic-prompts/wildcards/` にコピー）
```
1girl, solo, [オリキャラ固定文], __expression__, __outfit_sfw__, __scene_season__, __lighting__, __camera__, __style_era__,
masterpiece, best quality, very aesthetic, absurdres, general
```

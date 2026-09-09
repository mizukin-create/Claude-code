# Illustrious 系（SD WebUI）コピペ用プロンプトテンプレート（SFW 美少女向け・2026-09-09 改訂）

根拠と出典は `report/02_illustrious_prompting.md` と `report/07_prompt_verification.md`（モデルカード・Danbooru タグ DB での検証）を参照。タグはすべて Danbooru 正規表記に置き換え済み（`prompts/tag_dictionary_verified.md`）。各テンプレは **第 1 チャンク 75 トークン以内**で、品質タグは `BREAK` の後ろに置く。数値は必ず自分の環境で X/Y/Z plot（`prompts/ab_test_protocol.md`）により再検証すること。

## 0. 共通設定（eps 系派生: WAI-illustrious v17 / Hassaku v3.4 / Prefect v8 / Nova Anime XL IL v19）

| 項目 | 推奨 | 根拠 |
|---|---|---|
| Sampler / Scheduler | Euler a（詰めるなら DPM++ 2M Karras） | 全カード共通 |
| Steps | 25〜28（WAI カード 15〜30、Hassaku 28、Prefect 記載なし） | |
| CFG | 6（WAI 5〜7、Hassaku 3〜7 で最良 6、Prefect 5〜6、Nova 4〜6、LoRA 併用 4.5） | |
| Clip skip | 1（Prefect は 1 固定、Nova 1〜2） | |
| 解像度 | **WAI v17: 1024×1344**（カード作例。「1024×1024 より大きく」）／ Hassaku: 832×1216（最推奨）／ 896×1152 / 1024×1536 | |
| Hires.fix | ×1.5、R-ESRGAN 4x+ Anime6B、Hires steps 15〜20、denoise 0.35〜0.5（WAI）。v17 は Hires 通過で手足が自動補正されやすい | |
| ADetailer | 1st: face_yolov8s（denoise 0.35）→ 2nd: hand_yolov8n（0.35〜0.4）。目だけなら mediapipe_face_mesh_eyes_only（0.3） | |
| 品質タグ | **4〜5 個まで**（WAI: 「積みすぎると画質低下・ぼやける」） | |
| ネガ | **短く**（WAI: 「長すぎるネガは逆効果」）。SFW では `nsfw` 必須 | |
| v-pred 系（v3.5-vpred / NoobAI-vpred / RouWei-vpred） | reForge / Forge Neo で ZTSNR ON、CFG 3〜5、Rescale CFG 0.6、Euler、28〜35 steps | |
| 推奨 UI | Forge Neo（WAI カード推奨。Anima・Forge Couple・LLLite も使える） | |

共通ネガティブ（9 語。症状ごとに足す）:
```
worst quality, low quality, lowres, bad anatomy, bad hands, jpeg artifacts, signature, watermark, nsfw
```

品質・年代・レーティング（`BREAK` の後ろに置く）:
```
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```

モデル別の置き換え（07 §1・§3）:
- **WAI v17**: `masterpiece, best quality, amazing quality`（末尾）。ネガは `bad quality, worst quality, worst detail, sketch, censor, nsfw`。レーティングは `general / sensitive / nsfw / explicit`。年齢感は `(aged up:1.2)` `(mature female:1.2)` を先頭に
- **Hassaku v3.4**: `masterpiece, best quality`（＋`newest`）。**`highres` `absurdres` 等のメタタグと作品名タグは学習していないので入れない**。ネガに `signature`。順序「人数 → キャラ → 残り」。髪色が目色に引かれるときは髪色タグを前方に
- **Prefect v8**: `masterpiece, best quality, amazing quality, absurdres`。ネガ `bad quality, worst quality, worst detail, sketch, censored, watermark, signature, artist name`
- **Nova Anime XL IL v19**: `masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest, scenery, {prompt}, BREAK, depth of field, volumetric lighting`。ネガに `modern, recent, old, oldest` を置く流儀。**ライセンス: 無編集の生成画像は商用利用不可** → 販売用は加筆前提か、他モデルを使う
- **NoobAI 系**: `masterpiece, best quality, newest, absurdres, highres, safe`（`general` の代わりに `safe`）
- **RouWei 0.8**: 品質は `masterpiece, best quality` のみ、ネガは `worst quality, low quality, watermark` のみ。**絵師は `by name` が必須で、`BREAK` で別チャンク**。メタタグ（`lowres` 等）は使わない。CFG 7（eps）/ 3〜5（vpred）、32 の倍数で約 1MP

## 1. オリキャラ固定文（例）— 先頭に置く（35 トークン）

```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament,
```
- `silver hair` は Danbooru では `grey hair`（680,558 件）に統合、`violet eyes` は `purple eyes`（808,160 件）。旧表記は効きが弱い。
- 髪型・髪色・目・個性づけ・アクセ・衣装を「順序固定」で書き、毎回コピーする。設定シートは `prompts/character_sheet_template.md`。
- 個性づけタグ（投稿数）: `mole under eye`（157k）/ `thick eyebrows`（101k）/ `asymmetrical bangs`（32k）/ `tareme`（37k）/ `tsurime`（41k）/ `hair intakes`（115k）/ `ahoge`（649k）/ `heterochromia`（115k）

## 2. 5 パターン（第 1 チャンクのトークン数を併記）

### ① 顔アップ（1024×1344 or 1024×1024）— 71 トークン
```
1girl, solo, close-up, portrait, looking at viewer, light smile, parted lips, blush, long hair, grey hair, hair between eyes, sidelocks, blue eyes, hair ornament, sailor collar, backlighting, light rays, depth of field, blurry background, bokeh, cherry blossoms, petals, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
ADetailer 2nd に `mediapipe_face_mesh_eyes_only`（denoise 0.3）。ネガに `blurry`。`face focus` `rim lighting` `soft lighting` は Danbooru タグではないため外した。

### ② バストアップ（1024×1344）— 68 トークン
```
1girl, solo, upper body, from side, looking at viewer, light smile, closed mouth, head tilt, medium hair, wavy hair, brown hair, green eyes, white shirt, collared shirt, sleeves rolled up, holding cup, cup, coffee, cafe, indoors, window, dappled sunlight, depth of field
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```

### ③ 全身（1024×1344 or 832×1216、Hires ×1.6〜2.0 ＋ ADetailer 必須）— 72 トークン
```
1girl, solo, full body, standing, contrapposto, hand on own hip, looking at viewer, smile, blush, long hair, twintails, black hair, red eyes, school uniform, pleated skirt, black thighhighs, loafers, street, city, sunset, orange sky, backlighting, lens flare, from below
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
ネガ追加: `cropped, extra legs, bad feet`。`long shadow`（66 件）は削除、必要なら `shadow`。

### ④ 背景重視シーン（1344×768 or 1216×832、Hires ×1.5〜2.0 denoise 0.4）— 58 トークン
```
1girl, solo, scenery, wide shot, from behind, looking back, standing, wind, floating hair, white dress, sun hat, long hair, blonde hair, sunflower field, blue sky, cumulonimbus cloud, summer, light rays, sunbeam, sunlight
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
`depth of field` は入れない。`volumetric lighting` `cinematic lighting` は Danbooru タグではないので `light rays, sunbeam, sunlight` に置換。ADetailer は confidence 0.4・min mask ratio 0.01 で誤検出防止。

### ⑤ 複数人（Regional Prompter Matrix 列 `1,1` / Forge Couple Basic 横）
Regional Prompter 記法:
```
2girls, side-by-side, looking at viewer, park, sunlight, dappled sunlight, depth of field,
masterpiece, best quality, very aesthetic, absurdres, newest, general ADDCOMM
1girl, long hair, blonde hair, blue eyes, white dress, smile, hand up, waving BREAK
1girl, short hair, black hair, brown eyes, black jacket, shorts, grin, hands in pockets
```
Forge Couple なら 1 行目を Global Effect にし、2〜3 行目を左右に。空行禁止。各領域にも `1girl` を書く。ADetailer は face を top-k 2。複雑な位置関係は Anima で決めてから二段構成（`workflows/anima_to_illustrious_2stage.json`）が確実。

### RouWei 0.8 の書式（参考）
```
masterpiece, best quality, by artist_a, by artist_b BREAK 1girl, solo, [固定文], upper body, ..., a girl sitting on a windowsill reading a book in soft afternoon light
```
ネガ: `worst quality, low quality, watermark`

## 3. 「魅力」クイックリファレンス（毎回 光×1・画角×1・表情×3軸 を入れる）

◆ = Danbooru 実タグ（カッコ内は投稿数の目安、★ 1 万以上）、◇ = Danbooru に無い語（自然文としてしか効かない。Anima / RouWei 向け）

| 分類 | タグ |
|---|---|
| 光 | ◆backlighting★ / ◆sidelighting / ◆dappled sunlight★ / ◆light rays★ / ◆sunbeam★ / ◆lens flare★ / ◆sunlight★ / ◆sunset★ / ◆neon lights / ◆light particles★ / ◆glowing★ / ◆bloom / ◆spotlight / ◆moonlight / ◆candlelight / ◇rim lighting / ◇cinematic lighting / ◇volumetric lighting / ◇soft lighting |
| 時間・空 | ◆sunset★ / ◆dusk / ◆evening / ◆twilight / ◆night★ / ◆sunrise / ◆blue sky★ / ◆cumulonimbus cloud / ◆overcast / ◆rain★ / ◆snow★ / ◆night sky★ / ◆full moon★ |
| 色 | ◆pastel colors / ◆limited palette★ / ◆monochrome, ◆spot color★ / ◆partially colored★ / ◆high contrast / ◆film grain★ / ◆chromatic aberration★ / ◆colorful / ◆gradient background★ / ◆muted color |
| 画角 | ◆from below★ / ◆from above★ / ◆from side★ / ◆from behind★, ◆looking back★ / ◆dutch angle★ / ◆fisheye / ◆close-up★ / ◆foreshortening★ / ◆wide shot★ / ◆cowboy shot★ / ◆upper body★ / ◆portrait★ / ◆full body★ / ◆pov★ / ◆straight-on★ / ◆profile★ / ◇face focus / ◇medium shot |
| 被写界深度・動き | ◆depth of field★ / ◆bokeh / ◆blurry background★ / ◆blurry foreground★ / ◆motion blur★ / ◆motion lines★ / ◆wind★, ◆floating hair★ / ◆falling petals★ / ◆falling leaves |
| 表情（目） | ◆half-closed eyes★ / ◆wide-eyed★ / ◆closed eyes★ / ◆one eye closed★ / ◆looking at viewer★ / ◆looking to the side★ / ◆looking down★ / ◆looking up★ / ◆tareme★ / ◆tsurime★ / ◆jitome★ / ◆empty eyes★ / ◆sparkling eyes★ / ◆bright pupils★ / ◇looking away |
| 表情（口） | ◆light smile★ / ◆smile★ / ◆grin★ / ◆parted lips★ / ◆closed mouth★ / ◆:d★ / ◆:o★ / ◆:3★ / ◆;d★ / ◆tongue out★ / ◆pout★ / ◆laughing★ / ◆smug★ / ◆fang★ |
| 表情（眉・頬） | ◆blush★ / ◆nose blush★ / ◆raised eyebrows★ / ◆furrowed brow★ / ◆v-shaped eyebrows★ / ◆embarrassed★ / ◆nervous★ / ◆tears★ / ◆sweatdrop★ / ◆surprised★ / ◆expressionless★ / ◆serious★ / ◆sleepy |
| 仕草 | ◆head tilt★ / ◆hand on own cheek★ / ◆hand on own face★ / ◆finger to mouth★ / ◆hand up★ / ◆arms behind back★ / ◆hands in pockets★ / ◆holding cup★ / ◆adjusting hair★ / ◆leaning forward★ / ◆hand on own hip★ / ◆crossed arms★ / ◆waving★ / ◆v★ / ◆hugging own legs★ / ◆arm up★ / ◆stretching★ / ◆hand on own chest★ |
| 質感 | ◆shiny skin★（強すぎ注意）/ ◆shiny clothes★ / ◆wet★ / ◆wet hair★ / ◆see-through clothes★ / ◆sparkle★ / ◆skin fang★ / ◇shiny hair / ◇glossy lips / ◇detailed eyes |
| 画風・様式 | ◆anime screencap（改名後は anime screenshot★）/ ◆retro artstyle★ / ◆1990s \(style\) / ◆1980s \(style\) / ◆2000s \(style\) / ◆flat color / ◆watercolor \(medium\)★ / ◆traditional media★ / ◆faux traditional media / ◆sketch★ / ◆painterly / ◆official art★ / ◆key visual / ◆game cg★ / ◆pixel art★ / ◆lineart★ / ◆monochrome★ / ◆greyscale★ / ◆halftone★ / ◆animification★ / ◆anime coloring / ◇cel shading / ◇impasto（225 件） |
| 年代 | newest / recent / mid / early / old（モデル固有） |

## 4. 「AI っぽさ」対策
- `shiny skin`（125,438 件）は効きすぎるので入れない（ネガに入れる選択肢も）。`very aesthetic` の積みすぎを避け、CFG を 4〜5 に下げ、Hires denoise は 0.3 台。
- `film grain` / `flat color` / 年代タグ / `traditional media` で質感を崩す。
- 個性づけタグ（mole under eye, thick eyebrows, asymmetrical bangs）で「マスピ顔」から離す。
- 絵師名を X 公開作品で単独使用しない。使うなら 2〜3 人を `BREAK (artist_a:0.6), (artist_b:0.5)` で別チャンクにブレンドし独自の塗りにする（RouWei は `by artist_a, by artist_b BREAK`）。

## 5. Dynamic Prompts での差分量産（`prompts/wildcards/` を `extensions/sd-dynamic-prompts/wildcards/` にコピー）
```
1girl, solo, [オリキャラ固定文], __expression__, __outfit_sfw__, __scene_season__, __lighting__, __camera__, __style_era__
BREAK masterpiece, best quality, very aesthetic, absurdres, general
```

## 6. 検証コマンド
```
python3 tools/prompt_lint.py --model illustrious "（ポジティブ）"
python3 tools/prompt_lint.py --model illustrious --negative "（ネガティブ）"
python3 tools/prompt_lint.py --model illustrious --convert-to anima "（ポジティブ）"   # Anima 用に変換
```

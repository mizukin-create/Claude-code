# Anima（ComfyUI）コピペ用プロンプトテンプレート（SFW 美少女向け）

根拠と出典は `report/03_anima_comfyui.md` を参照。公式の推奨記法（HF README）に準拠。

## 0. 記法の要点
- 順序: `[品質/メタ/年代/safety] [1girl 等] [キャラ名] [作品名] [@絵師] [一般タグ]` → その後に自然文（2 文以上推奨）。
- タグは小文字・スペース区切り・カンマ区切り。アンダースコアは `score_7` 系だけ。
- 品質: `masterpiece, best quality, score_7`（Base）。**Aesthetic 版は score_* をポジ・ネガとも外す**。
- safety: `safe` をポジに 1 つ、`sensitive, nsfw, explicit` をネガに。
- 絵師タグは `@name`（@ がないとほぼ効かない）。X 公開作品では絵師名を避け、`retro artstyle` / `anime coloring` / `anime screenshot` / `flat color` / `sketch` 等の様式タグと年代タグで代替。
- 表情は 3 軸以上（目・瞳・口・眉・頬）。複数人は自然文で「左の子は… and 右の子は…」。
- 強調は `(tag:1.5)` 程度から。ComfyUI の括弧は動くが SDXL より強めの値が必要。

## 1. 共通設定

| 版 | steps | CFG | sampler / scheduler | 備考 |
|---|---|---|---|---|
| Base v1.0 | 30〜40 | 4〜5 | er_sde / simple（euler_ancestral は柔らかい線、dpmpp_2m_sde_gpu は多様） | shift は内部既定 3.0 |
| Aesthetic v1.1 | 30〜35 | 3.5〜4 | 同上 | score_* を全削除、ノイズが出たら CFG を下げ `anime coloring` を追加 |
| Turbo v1.1 / Turbo LoRA | 8〜12 | 1 | euler / simple | ネガは実質無効（必要なら ComfyUI-Anima-NAG）。seed・構図探索用 |

解像度: 832×1216 / 896×1152 / 1024×1024 / 768×1344 / 1024×1536 / 1152×896（16 の倍数必須、32 の倍数が安全、約 2MP 超は破綻）。Hires は 1.25〜1.5 倍まで、denoise 0.28〜0.35。

共通ネガティブ（Base）:
```
worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit
```
共通ネガティブ（Aesthetic）:
```
worst quality, low quality, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit
```

## 2. オリキャラ固定文（例）
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, long silver hair, blunt bangs, sidelocks, violet eyes, bright pupils, mole under eye, star hair ornament, black sailor collar, white shirt, pleated skirt,
```
キャラ名を付けても Anima は知らないので、名前の直後に必ず外見を書く。

## 3. 5 パターン

### ① 顔アップ（896×1152 / 1024×1024）
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, close-up, face focus, portrait, looking at viewer, long silver hair, blunt bangs, violet eyes, bright pupils, half-closed eyes, gentle smile, parted lips, blush, hair ornament, soft lighting, depth of field, anime coloring, clean lineart.
A close-up portrait of a girl gazing softly at the viewer, warm afternoon light catching her hair, blurred pastel background behind her.
```

### ② バストアップ（832×1216）
```
masterpiece, best quality, score_7, newest, highres, safe, 1girl, solo, upper body, medium shot, looking at viewer, brown hair, twintails, green eyes, smile, school uniform, white shirt, red ribbon, blazer, hand on own cheek, classroom, window, sunlight, backlighting, anime coloring.
She leans slightly toward the viewer with a playful expression, sunlight from the window behind her outlining her hair.
```

### ③ 全身（768×1344 / 832×1216）
```
masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, full body, standing, dynamic pose, looking at viewer, black hair, long hair, blue eyes, wide eyes, open mouth, white dress, sundress, sandals, straw hat, holding hat, sunflower field, blue sky, cumulonimbus cloud, wind, from below, anime coloring.
A girl stands in a sunflower field holding her hat against the wind, her dress and hair blowing to the left, the whole body visible from head to feet.
```

### ④ 背景重視（1152×896 / 1344×896）
```
masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, scenery, wide shot, from behind, small figure, pink hair, short hair, white blouse, standing on a hill, cityscape, sunset, orange sky, cloud, torii, cherry blossoms, petals, detailed background, depth, cinematic lighting.
A wide landscape illustration where the girl is a small silhouette on the left third of the frame, the vast evening city and sky dominating the scene with layered depth and glowing windows.
```

### ⑤ 複数人（1152×896）
```
masterpiece, best quality, score_7, newest, highres, safe, 2girls, upper body, side by side, looking at viewer, cafe, table, window, warm lighting, anime coloring.
Two girls sit side by side at a cafe table. The girl on the left has long blonde twin braids and blue eyes, wears a navy sailor uniform and holds a teacup with both hands, smiling gently. The girl on the right has short black hair and red eyes, wears a white hoodie and rests her chin on her hand with a bored expression. They lean slightly toward each other.
```
ネガに `1girl, solo, 3girls, twins, same face` を追加。

## 4. 「様式」を作る Anima 向けタグ
- レトロアニメ: `retro artstyle, 1990s style, anime screenshot, cel shading, film grain, muted colors`
- 水彩・アナログ: `watercolor, traditional media, paper texture, soft edges, limited palette`
- スケッチ・ラフ: `sketch, rough lines, unfinished, monochrome with spot color`
- 映画的セミリアル: `semi-realistic, cinematic lighting, dramatic shadows, volumetric light, shallow depth of field`
- フラット・ポスター: `flat color, limited palette, bold outlines, poster design, negative space`

自然文で「どこから光が来て、何が動いていて、キャラは何を思っているか」を 2 文で書くと Anima の追従力が最も活きる。

## 5. ワークフロー
- 同梱 `workflows/anima_t2i_hires.json` を ComfyUI にドラッグ＆ドロップ。
- 構図固定は ComfyUI のテンプレートブラウザ → 「Anima Lllite: Depth Control to Image」/「Any Control to Image」を利用（ModelPatchLoader → AnimaLLLiteApply、strength 0.6〜1.0、end 0.6〜0.8）。

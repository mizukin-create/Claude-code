# Anima（ComfyUI）コピペ用プロンプトテンプレート（SFW 美少女向け・2026-09-09 改訂）

根拠と出典は `report/03_anima_comfyui.md` と `report/07_prompt_verification.md`（公式 README・Civitai カード・108 スタイル比較記事で検証）。タグは Danbooru 正規表記（`prompts/tag_dictionary_verified.md`）。

## 0. 記法の要点（公式 README 2026-09-09 版）
- 順序: `[品質/メタ/年代/safety] [1girl 等] [キャラ名] [作品名] [@絵師] [一般タグ]` → その後に自然文（2 文以上推奨）。各ブロック内の順序は自由。
- タグは小文字・スペース区切り・カンマ区切り。アンダースコアは `score_7` 系だけ。**Danbooru と Gelbooru で表記が違うタグは Gelbooru 側を優先**。
- 品質: Base は `masterpiece, best quality, score_7`。**Aesthetic は score_* をポジ・ネガとも外す**（`masterpiece, best quality` は残して可）。
- safety: `safe` をポジに 1 つ、`sensitive, nsfw, explicit` をネガに。
- 絵師タグは `@name`（@ がないとほぼ効かない）。X 公開作品では絵師名を避け、様式語（§4）と年代タグで代替。ネガに `artist name`。
- 表情は 3 軸以上（目・口・眉/頬）。複数人は自然文で「左の子は… and 右の子は…」、名前の直後に必ず外見。
- 強調は SDXL より強めの値（公式例 `(chibi:2)`）。`[tag]` は使わない。
- **まず Turbo で探索**（README: 「Aesthetic より僅かに劣る程度で高速、安定性はむしろ上」）→ Base / Aesthetic で本番。

## 1. 共通設定

| 版 | steps | CFG | sampler / scheduler | 備考 |
|---|---|---|---|---|
| Base v1.0 | 30〜40 | 4〜5 | er_sde / simple（euler_ancestral は柔らかい線、dpmpp_2m_sde_gpu は多様、euler は少し創造的） | shift は内部既定 3.0 |
| Aesthetic v1.1（2026-07-13） | 30〜35 | **3〜4**（Civitai カード: 「3 のような低め CFG でしばしば良くなる」） | 同上。euler と相性良 | score_* を全削除、ノイズが出たら CFG を下げ `anime coloring` を追加 |
| Turbo v1.1（2026-08-24） | 8〜12 | 1 | euler / simple | ネガは実質無効（必要なら ComfyUI-Anima-NAG）。seed・構図探索用 |

解像度: 832×1216 / 896×1152 / 1024×1024 / 768×1344 / 1024×1536 / 1152×896（16 の倍数必須、32 の倍数が安全、約 2MP 超は破綻）。Hires は 1.25〜1.5 倍まで、denoise 0.28〜0.35。絵画調にしたいときは beta57 スケジューラ（RES4LYF）。

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
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, Mio, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, pleated skirt,
```
キャラ名を付けても Anima は知らないので、名前の直後に必ず外見を書く（README）。`silver hair` → `grey hair`、`violet eyes` → `purple eyes`（Danbooru 正規表記）。

## 3. 5 パターン

### ① 顔アップ（896×1152 / 1024×1024）
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, close-up, portrait, looking at viewer, long hair, grey hair, blunt bangs, purple eyes, bright pupils, half-closed eyes, light smile, parted lips, blush, hair ornament, backlighting, depth of field, anime coloring.
A close-up portrait of a girl gazing softly at the viewer, warm afternoon light catching her hair from behind. The background dissolves into blurred pastel bokeh, and she tilts her head slightly as if about to say something.
```

### ② バストアップ（832×1216）
```
masterpiece, best quality, score_7, newest, highres, safe, 1girl, solo, upper body, looking at viewer, brown hair, twintails, green eyes, smile, school uniform, white shirt, red ribbon, blazer, hand on own cheek, classroom, window, sunlight, backlighting, anime coloring.
She leans slightly toward the viewer with a playful expression, sunlight from the window behind her outlining her twintails. Dust motes drift in the warm light and a half-erased chalkboard fills the background.
```

### ③ 全身（768×1344 / 832×1216）
```
masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, full body, standing, looking at viewer, black hair, long hair, blue eyes, wide-eyed, open mouth, white dress, sundress, sandals, straw hat, holding hat, sunflower field, blue sky, cumulonimbus cloud, wind, from below, anime coloring.
A girl stands in a sunflower field holding her hat against the wind, her dress and hair blowing to the left, the whole body visible from head to feet. The camera looks up at her from the ground so the towering clouds fill the sky behind her.
```

### ④ 背景重視（1152×896 / 1344×896）
```
masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, scenery, wide shot, from behind, pink hair, short hair, white shirt, standing, hill, cityscape, sunset, orange sky, cloud, torii, cherry blossoms, petals, light rays.
A wide landscape illustration where the girl is a small silhouette on the left third of the frame, the vast evening city and sky dominating the scene with layered depth and glowing windows. Petals drift across the foreground while the last sunlight rakes across the rooftops.
```

### ⑤ 複数人（1152×896）
```
masterpiece, best quality, score_7, newest, highres, safe, 2girls, upper body, side-by-side, looking at viewer, cafe, table, window, sunlight, anime coloring.
Two girls sit side by side at a cafe table. The girl on the left has long blonde twin braids and blue eyes, wears a navy sailor uniform and holds a teacup with both hands, smiling gently. The girl on the right has short black hair and red eyes, wears a white hoodie and rests her chin on her hand with a bored expression. They lean slightly toward each other.
```
ネガに `1girl, solo, 3girls, twins, same face` を追加。

## 4. 「様式」を作る Anima 向け語（108 枚同一 seed 比較の結果に基づく。07 §5）

| 狙い | 効く語（自然語 `〜 style` 表記） | 効かない・危険な語 |
|---|---|---|
| レトロアニメ（署名様式 候補 1） | `90s anime style` / `80s anime style` / `retro anime style` / `VHS anime aesthetic` ＋ Danbooru タグ `retro artstyle, 1990s (style), anime screenshot` | `vintage anime` `Showa anime` `Y2K anime`（差が出ない） |
| 淡い配色 | `soft pastel style`（髪・服が淡い配色にまとまる） | `pastel style`（弱い） |
| モノクロ・印刷質感 | `golden age comic style` / `charcoal drawing style` / `pencil style` / `shoujo manga style` / `shounen manga style`（＋ `monochrome, greyscale, halftone`） | `sketch style` `line art` `crayon`（無効） |
| 絵画調 | `watercolor painting style` / `oil painting style` / `gouache painting style` / `digital painting style`（風景付きの一枚絵になる。技法の描き分けは弱い） | `impasto style` `ink wash painting style`（無効・誤変換） |
| 装飾・配色が強い様式 | `art nouveau style` / `vaporwave style` / `psychedelic art style` / `pop art style` / `gothic style` / `cyberpunk style` | `steampunk / dieselpunk / solarpunk / space opera / biopunk`（同じ出力に収束） |
| 3D・セミリアル | （Anima では狙わない） | `3D render` `Pixar-style 3D` `Live2D` → **実写化する**。セミリアルは Illustrious 2.5D 派生で |
| アニメ塗り指定 | 不要（既定がアニメ塗り） | `cel shading style` `flat color illustration`（差が出ない） |

- 様式語は **タグを最小限に削ったときに効く**（要素が多いとタグドロップアウトで末尾の様式語が埋もれる）。様式実験は `masterpiece, best quality, score_7, safe, [style], 1girl, solo, [固定文最小版]` で seed 固定して比較する。
- 自然文で「どこから光が来て、何が動いていて、キャラは何を思っているか」を 2 文で書くと Anima の追従力が最も活きる。

## 5. ワークフロー
- 同梱 `workflows/anima_t2i_hires.json` を ComfyUI にドラッグ＆ドロップ（txt2img → 1.25x 2nd pass → 2x ESRGAN）。
- **二段構成** `workflows/anima_to_illustrious_2stage.json`: Anima で構図を確定 → 4x-AnimeSharp → 1024×1536 → Illustrious（WAI v17）＋ ControlNet tile で img2img（denoise 0.45）→ 2x。`workflows/build_two_stage_workflow.py` で再生成可能。
- 構図固定は ComfyUI のテンプレートブラウザ → 「Anima Lllite: Depth Control to Image」/「Any Control to Image」を利用（ModelPatchLoader → AnimaLLLiteApply、strength 0.6〜1.0、end 0.6〜0.8）。

## 6. 検証コマンド
```
python3 tools/prompt_lint.py --model anima --variant aesthetic "（ポジティブ）"
python3 tools/prompt_lint.py --model anima --negative "（ネガティブ）"
python3 tools/prompt_lint.py --model anima --convert-to illustrious "（ポジティブ）"   # Illustrious 用に変換
```

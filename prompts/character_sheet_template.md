# オリキャラ設定シート＋固定プロンプト（Illustrious / Anima 両対応）

00 §3.1「主役オリキャラを 1〜2 体つくる」の実務用テンプレート。**設定シート → 固定プロンプト → 衣装バリエーション → 一貫性の担保 → LoRA 化** の順に埋める。タグはすべて Danbooru 正規表記（`prompts/tag_dictionary_verified.md` で検証済み）。

> 06 の実データで、@mi_Create_mi の 2026 年 2〜4 月の投稿は 100% 版権キャラ（アイマス・ホロライブ・にじさんじ・ぶいすぽ・原神・ブルアカ 等）だった。伸びた投稿もあるが、（1）ファンアートタグ禁止・AI 明記必須の事務所ガイドライン、（2）R-18 販売との組み合わせ、（3）「作者フォロー」予測が版権名に吸われる、という 3 点から、**X の本垢では主役オリキャラを軸に据える**のが前回同様の結論。版権は「単発バズ枠」に限定する。

---

## 1. 設定シート（記入例つき）

| 項目 | 記入例（例キャラ「ミオ」） | 記入欄 |
|---|---|---|
| 名前・読み | ミオ（Mio） | |
| 年齢感 | 高校 2 年くらい（`aged up` 不要の全年齢デザイン） | |
| 性格 3 語 | マイペース・観察好き・少し皮肉屋 | |
| 口癖・セリフ | 「……見てたよ」 | |
| 髪 | 長い灰銀髪、ぱっつん前髪、サイドロック | `long hair, grey hair, blunt bangs, sidelocks` |
| 目 | 紫、明るい瞳、やや垂れ目 | `purple eyes, bright pupils, tareme` |
| 個性づけ 1 点 | 左目の下のほくろ ＋ 星のヘアピン | `mole under eye, star hair ornament` |
| 定番衣装 A（学校） | 黒セーラーカラーの白シャツ、プリーツスカート、黒ニーソ、ローファー | `black sailor collar, white shirt, pleated skirt, black thighhighs, loafers` |
| 定番衣装 B（私服） | オーバーサイズのグレーパーカー、ショートパンツ、スニーカー | `grey hoodie, oversized shirt, shorts, sneakers` |
| 定番衣装 C（季節） | 秋: カーディガン＋マフラー／冬: ダッフルコート／夏: 白ワンピ＋麦わら帽 | `cardigan, scarf` / `duffel coat` / `white dress, sundress, straw hat` |
| 小物 | 缶コーヒー、文庫本、猫のキーホルダー | `holding can, book, keychain` |
| 生活圏 | 坂の上の住宅街、屋上、駅前のコンビニ | `hill, rooftop, convenience store` |
| 様式（署名） | レトロアニメ×現代の光（候補 1） | `retro artstyle, 1990s \(style\), anime screencap` |
| NG | 露出多め、版権衣装、絵師名 | — |

「個性づけ 1 点」は必ず入れる。Danbooru 投稿数が多い個性タグは安定して再現される: `mole under eye`（157,514）、`hair intakes`（114,922）、`heterochromia`（114,685）、`thick eyebrows`（100,978）、`asymmetrical bangs`（31,774）、`tareme`（36,744）、`tsurime`（40,824）、`fang`（321,882）、`freckles`（40,583）、`hair over one eye`（245,322）。

---

## 2. 固定プロンプト（毎回コピーする部分）

### Illustrious 系（WAI v17 / Hassaku v3.4 / Prefect v8）

先頭 75 トークンに必ず収める（下記は 32 トークン）。順序は固定し、語を増やさない。

```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament,
```

衣装 A（学校）を足した状態（47 トークン）:

```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, pleated skirt, black thighhighs, loafers,
```

残り約 28 トークンで「ポーズ/画角 → 表情 3 軸 → 場所/時間 → 光 → 様式」を書き、品質・年代・レーティングは `BREAK` の後ろに置く（第 2 チャンクでも品質タグは効く。WAI カードは末尾配置を推奨）:

```
[固定文＋衣装], upper body, from side, looking at viewer, light smile, half-closed eyes, blush, head tilt, rooftop, sunset, backlighting, wind, floating hair, depth of field, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```

ネガ: `worst quality, low quality, lowres, bad anatomy, bad hands, jpeg artifacts, signature, watermark, nsfw`（12 語以内）

### Anima（Base v1.0 / Aesthetic v1.1 / Turbo v1.1）

名前は付けてもモデルは知らないので、**名前の直後に必ず外見**を書く（README）。

```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, Mio, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, pleated skirt, black thighhighs, loafers,
```

Aesthetic v1.1 では `score_7` を外す。続けて構図・光・気持ちを自然文 2 文で:

```
Mio leans on the rooftop fence at sunset and glances back at the viewer with a faint smile, the low sun outlining her grey hair with warm light. Her skirt and hair drift in the wind while the city below fades into haze.
```

ネガ（Base）: `worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit`

### 変換

Illustrious 用に書いた固定文は `python3 tools/prompt_lint.py --model illustrious --convert-to anima "..."` で Anima 形式に変換できる（品質タグ・レーティング・別名・記法を自動で書き換え）。

---

## 3. 衣装・季節バリエーション（差分投稿用）

| 名前 | Illustrious タグ | 主な用途 |
|---|---|---|
| A 学校（夏服） | `black sailor collar, white shirt, short sleeves, pleated skirt, black thighhighs, loafers` | 連載枠の基本 |
| A' 学校（冬服） | `black sailor collar, white shirt, cardigan, pleated skirt, black thighhighs, loafers, scarf` | 10/1 衣替え以降 |
| B 私服 | `grey hoodie, oversized shirt, shorts, sneakers, headphones around neck` | 休日回 |
| C 秋 | `sweater, turtleneck, long skirt, scarf, autumn leaves` | 9〜11 月 |
| D 冬 | `duffel coat, scarf, mittens, winter clothes, snow` | 12〜2 月 |
| E 夏（記念日） | `white dress, sundress, straw hat, sandals` | 単発バズ枠 |
| F 浴衣 | `yukata, floral print, obi, geta, hair flower` | 夏祭り・花火 |
| G ハロウィン | `witch hat, black dress, cape, jack-o'-lantern` | 10/31 |
| H クリスマス | `santa costume, fur-trimmed capelet, gift box` | 12/24〜25 |

差分は「衣装だけ」「表情だけ」「時間帯だけ」のように 1 変数だけ変えると、キャラの同一性が視覚的に伝わる（06 §5: 2 枚組は 1 枚より中央値で 6 倍の閲覧数）。

---

## 4. LoRA なしで一貫させる 4 点セット（04 §5）

1. **固定文の順序を絶対に変えない**（トークン位置が変わると顔が変わる）。
2. **seed 帳**: 気に入った顔の seed を衣装別に記録し、差分は同 seed ＋ `variation seed`（ComfyUI: KSampler (Inspire) の variation_strength 0.1〜0.3）で作る。
3. **Reference Only / IP-Adapter plus-face**（weight 0.4〜0.6）で顔を参照。ADetailer の顔プロンプトにも固定文の「目・ほくろ」だけを書く。
4. **Anima で構図、Illustrious で顔**: 複数人や難しいポーズは Anima → Illustrious 二段（`workflows/anima_to_illustrious_2stage.json`）で、最後は必ず同じ Illustrious モデル＋固定文で顔を仕上げる。

---

## 5. LoRA 化のタイミングと設定

- 固定文で 20 枚出して顔・髪・衣装がブレなくなったら、**ブレの少ない 30〜60 枚**（正面・横・後ろ・全身・表情違い、背景は単純）を選んで学習。
- Illustrious 用: kohya sd-scripts / kohya_ss、1024 基準 bucket、dim 32 / alpha 16、UNet LR 1e-4〜3e-4、TE LR 1/10、1500〜3000 steps、`min_snr_gamma 5`。タグは WD14 で付け、**固定したい特徴（髪色・目・ほくろ・ヘアピン）はタグから外してトリガー語に吸わせる**。
- Anima 用: sd-scripts `anima_train_network.py` または diffusion-pipe。**LLM adapter は学習しない**（README）。rank 32、LR 2e-5〜1e-4、Base で学習して Aesthetic / Turbo に流用。
- 出来た LoRA は 0.7〜0.9 で使い、固定文は残す（LoRA ＋ 固定文が最も安定）。

---

## 6. プロフィール・固定ポストに載せる「キャラ紹介文」の型

```
ミオ（Mio）｜灰銀の髪と紫の瞳、左目の下のほくろが目印。坂の上の街で暮らす高 2。
毎週 月・木 21:00 に新作、水曜昼に差分。AI 生成（Illustrious / Anima）。
```

- 名前・見た目の目印・投稿ペース・AI 明記の 4 点。固定ポストには衣装 A/B/C の 3 枚＋顔アップ 1 枚を 4 枚組で。

# A/B テスト手順（生成側 X/Y/Z plot ＋ 投稿側 2 週間比較）

00 §7 第 2 週「X/Y/Z plot で基準値確定」と §8「4 週間単位で 1 変数ずつ」を、そのまま実行できる形にしたもの。**同時に 2 つ以上の変数を変えない**のが唯一のルール。

---

## A. 生成側: 基準値を決める X/Y/Z plot

### A-1. 共通条件（固定するもの）

- モデル: WAI v17（Illustrious 側の基準）／ Anima Aesthetic v1.1（Anima 側の基準）
- プロンプト: `prompts/character_sheet_template.md` の固定文 ＋ 衣装 A ＋ `upper body, looking at viewer, light smile, half-closed eyes, blush, rooftop, sunset, backlighting, depth of field, anime screencap`
- seed: 4 つ固定（例 `1001, 1002, 1003, 1004`）。1 条件につき 4 枚で判断する
- 解像度: 1024×1344（WAI カードの作例サイズ）／ Anima 832×1216
- Hires: ×1.5、R-ESRGAN 4x+ Anime6B、Hires steps 15

### A-2. グリッド 1: CFG × Hires denoise（WebUI「X/Y/Z plot」スクリプト）

| 軸 | 種別 | 値 |
|---|---|---|
| X | CFG Scale | `4, 5, 6, 7` |
| Y | Denoising | `0.3, 0.4, 0.5` |
| Z | Seed | `1001, 1002, 1003, 1004` |

見るところ: CFG 7 で肌がテカる・色が飽和する境目、denoise 0.5 で指が増える境目。**「破綻ゼロで最も情報量が多い」組を基準値**にする（WAI カードは CFG 5〜7、denoise 0.35〜0.5）。

### A-3. グリッド 2: 品質タグの有無（Prompt S/R）

| 軸 | 種別 | 値 |
|---|---|---|
| X | Prompt S/R | `masterpiece, best quality, very aesthetic, absurdres` → `masterpiece, best quality` → `masterpiece, best quality, amazing quality` → （空） |
| Y | Prompt S/R | `anime screencap` → `anime screenshot` → `retro artstyle, 1990s \(style\)` → （空） |
| Z | Seed | 4 つ |

見るところ: WAI カード「品質タグの積みすぎは画質低下」の実際、`anime screencap` と `anime screenshot`（改名前後）のどちらが自分の派生モデルで効くか。

### A-4. グリッド 3: 年代タグ × サンプラー

| 軸 | 種別 | 値 |
|---|---|---|
| X | Prompt S/R | `newest` → `recent` → `mid` → （空） |
| Y | Sampler | `Euler a, DPM++ 2M Karras, DPM++ 2M SDE Karras` |
| Z | Seed | 4 つ |

### A-5. Anima 側（ComfyUI）

X/Y/Z plot 相当は「Efficiency Nodes の XY Plot」か、KSampler を 3 つ並べて `cfg` を `3.5 / 4.0 / 4.5`、`sampler` を `er_sde / euler / dpmpp_2m_sde_gpu` にした 9 通りを同 seed で出す。Aesthetic は `score_*` を外した状態で比較する（README）。Turbo は CFG 1 固定なので steps `8 / 10 / 12` だけを比較。

### A-6. 採点表（1 条件 4 枚を 0〜2 点で）

| 観点 | 0 | 1 | 2 |
|---|---|---|---|
| 破綻（手・目・文字） | 明確な破綻 | 軽微 | なし |
| 固定文への忠実さ（髪・目・ほくろ・衣装） | 2 つ以上違う | 1 つ違う | 一致 |
| 光の表現（指定した光タグが見える） | 見えない | 弱い | 明確 |
| 表情の情報量（3 軸が出ている） | 無表情 | 2 軸 | 3 軸 |
| AI っぽさ（テカリ・マスピ顔） | 強い | やや | 弱い |

合計 8 点以上の条件を基準値として `prompts/illustrious_templates.md` §0 の表に書き戻す。

---

## B. 投稿側: 2 週間 × 1 変数の比較

### B-1. 変数の候補と順番

06 の実データ（@mi_Create_mi 70 投稿・同業 6 アカウント）で差が見えた順に試す。

| 順 | 変数 | A | B | 判断指標 |
|---|---|---|---|---|
| 1 | 本文とハッシュタグ | 定型文＋#3〜4 個（現状） | 一言のセリフ＋#AIイラスト のみ | いいね率（いいね÷インプ）、返信数 |
| 2 | 枚数 | 1 枚 | 2 枚（差分） | 閲覧数の中央値、ブックマーク数 |
| 3 | 時間帯 | 21:00 | 06:00（現状の上位投稿に多い） | インプレッション、いいね率 |
| 4 | 様式 | レトロアニメ（候補 1） | 水彩／セミリアル（候補 2・3） | いいね率、フォロワー増 |
| 5 | モデル | Illustrious | Anima → Illustrious 二段 | いいね率、返信数（構図の複雑さが伝わるか） |

### B-2. 手順

1. 2 週間 = 6 投稿を「A, B, A, B, A, B」の順で交互に出す（曜日・時間は固定）。
2. 投稿 48 時間後の値を記録する（X アナリティクス: インプレッション・エンゲージメント・プロフィールクリック・フォロー）。
3. 中央値で比較する（平均はバズ 1 本に引きずられる）。差が 20% 未満なら「差なし」として次の変数へ。
4. 勝った側を固定し、次の変数へ。

### B-3. 記録シート（コピーして使う）

```
日付 | 枠 | 変数 | A/B | インプ | いいね | いいね率 | 返信 | RP | 引用 | BM | プロフクリック | フォロー
2026-09-14 | 連載 | 本文 | A | | | | | | | | |
```

### B-4. 06 で分かっている前提（検証を省ける項目）

- `possibly_sensitive` が付かない全年齢作品でも、**作者単位のラベル・フラグや投稿ごとの分類器ラベル**があると埋め込み・推薦から外れる（06 §3）。作者のセンシティブ設定は 9/10 に OFF を確認済み。テストの前に `tools/check_embed.py --detail` で新規投稿が OK になっているかを確認する。
- 2 枚組は 1 枚より閲覧数の中央値が大きい（06 §4）。ただし時期（フォロワー増）と交絡しているので B-1 の #2 で追試する。
- 同業の上位アカウント（5 万フォロワー級）はハッシュタグ 0〜1 個・本文 20 字前後・1 枚投稿が中央値で最も伸びている（06 §5）。

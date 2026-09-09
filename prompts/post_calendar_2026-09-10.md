# 投稿カレンダー 2026-09-14 〜 10-11（＋ハロウィン準備）— プロンプト付き

> **Under the Hood 9 月分の条件**: 9 月（UTC 日付）にリポスト以外の投稿を 10 件以上（返信も数える）。このカレンダーの投稿で満たせるが、欠けた分は返信で補える。8 月分は適格投稿不足で生成されない（report/06 §3.3）。

00 §6 の週間プラン（連載 3 ／ 単発 1 ／ 交流 1）を、06 の実データで修正した運用（**タグ 0〜1 個・一言の本文・21:00 主枠 / 06:40 副枠・2 枚組**）に合わせて 4 週間分に展開したもの。主役は `prompts/character_sheet_template.md` の例キャラ「ミオ」。自分のキャラに置き換えるときは固定文だけ差し替える。

## 使い方
- Illustrious 用プロンプトは第 1 チャンク 75 トークン以内（`tools/prompt_lint.py` で確認済み）。品質タグは `BREAK` の後ろ。
- Anima 用は「タグ → 自然文 2 文」。Aesthetic v1.1 を使うときは `score_7` を消す。
- 設定は `prompts/illustrious_templates.md` §0 / `prompts/anima_templates.md` §1。Hires ×1.5 → ADetailer 顔 → 手 → 書き出し（長辺 2048〜4096、JPEG q90〜92、メタデータ除去）。
- 本文は **20 字前後の一言かセリフ**。ハッシュタグは `#AIイラスト` のみか無し。「フォロー・RT お願い」は書かない。AI 生成の明記はプロフィールと固定ポストで行う。
- 2 枚組: 1 枚目＝本命、2 枚目＝表情か時間帯の差分（同 seed、`variation seed` 0.15）。

固定文（Illustrious、35 トークン）:
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament,
```
固定文（Anima）:
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, Mio, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament,
```
共通ネガ（Illustrious）: `worst quality, low quality, lowres, bad anatomy, bad hands, jpeg artifacts, signature, watermark, nsfw`
共通ネガ（Anima Base）: `worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit`

---

## 第 1 週（9/14 月〜9/20 日）— 「秋の始まり」

### 9/14（月）21:00 連載 — 放課後の教室、西日
Illustrious（WAI v17、1024×1344）:
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, cardigan, upper body, looking at viewer, light smile, half-closed eyes, blush, classroom, window, sunset, backlighting, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
Anima:
```
masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, Mio, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, cardigan, upper body, sitting, looking at viewer, light smile, half-closed eyes, blush, classroom, window, sunset, backlighting, anime coloring.
Mio sits at a desk by the window after school, turning to look at the viewer with a faint smile as the low sun outlines her grey hair. Dust drifts in the orange light and the empty classroom stretches behind her.
```
本文案: 「まだ帰らないの？」／ 2 枚目: `closed eyes, smile` に差分。狙い: 連載の初回として固定ポストにも使う。

### 9/16（水）06:40 交流 — 表情差分 3 枚「どれが好き？」
同 seed で `light smile, half-closed eyes` / `grin, wide-eyed, hand up` / `pout, tsurime, crossed arms` の 3 枚（顔アップ、`close-up, portrait`）。本文: 「今日の顔、どれ？」。返信を誘う唯一の枠。3 枚は正方形タイルに切られるので顔を中央に。

### 9/17（木）21:00 連載 — 夕暮れの駅ホーム、金木犀
Illustrious:
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, cardigan, pleated skirt, cowboy shot, looking to the side, train station, dusk, lamppost, wind, floating hair, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
Anima 自然文: `Mio waits on an empty station platform at dusk, glancing down the tracks while her cardigan sleeves cover her hands. A warm lamppost flickers on above her and the evening wind lifts her hair.`
本文案: 「一本、見送った。」

### 9/19（土）21:00 単発 — 様式実験 A: レトロアニメ（候補 1）
Illustrious（同じ構図をレトロ様式で）:
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, white shirt, upper body, looking at viewer, light smile, rooftop, sunset, backlighting, retro artstyle, 1990s \(style\), anime screencap, film grain
BREAK masterpiece, best quality, very aesthetic, absurdres, recent, general
```
Anima（様式語は最小構成で効く）: `masterpiece, best quality, score_7, safe, 90s anime style, retro anime style, 1girl, solo, [固定文], upper body, looking at viewer, light smile, rooftop, sunset, backlighting. A 1990s cel-animated look with slightly muted colors and soft film grain, the sun flaring behind her. She smiles at the viewer as the wind lifts her hair.`
本文案: 「90年代に生まれてたら、こう。」2 枚目に通常様式の同構図を並べて「どっち派？」でも可。

### 9/20（日）14:00 企画 — 三連休のお出かけ（私服 B）＋お題募集
Illustrious:
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, grey hoodie, shorts, sneakers, full body, walking, looking back, smile, blush, crosswalk, city, sunlight, dappled sunlight, from behind, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
本文案: 「連休、どこ行きたい？（返信で場所を募集）」。集まった場所を第 3 週の連載に使う。

---

## 第 2 週（9/21 月〜9/27 日）— 「祝日と名月」

### 9/21（月・敬老の日）21:00 連載 — 休日のカフェ
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, sweater, turtleneck, long skirt, upper body, looking at viewer, light smile, holding cup, cup, coffee, cafe, window, sunlight, depth of field, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
本文案: 「三連休、最終日。」

### 9/23（水・秋分の日）06:40 交流 — 衣装差分 2 枚「秋服、どっち？」
衣装 C（`sweater, turtleneck, long skirt, scarf`）vs 衣装 A'（`cardigan, scarf`）。同 seed・同構図（`upper body, looking at viewer, light smile`）。本文: 「今日から秋服。どっち？」

### 9/24（木）21:00 連載 — 雨の日、傘
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, cardigan, pleated skirt, cowboy shot, holding umbrella, looking at viewer, light smile, rain, street, puddle, depth of field, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
Anima 自然文: `Mio holds a clear umbrella on a rain-soaked street and looks at the viewer with a small smile, the grey sky reflected in the puddles at her feet. Raindrops streak the umbrella and her cardigan is slightly damp at the shoulders.`
本文案: 「傘、入る？」

### 9/25（金・中秋の名月）20:00 単発 — お月見
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, yukata, floral print, obi, upper body, sitting, looking up, parted lips, full moon, night sky, dango, moonlight, wind, floating hair, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
Anima 自然文: `Mio sits on a wooden veranda in a yukata, looking up at the full moon with her lips slightly parted, a plate of dango beside her. Cool moonlight silvers her hair and the night wind stirs the sleeves.`
本文案: 「今夜、満月。」（`tsukimi` はタグとして弱いので `full moon, dango` で表現）

### 9/27（日）14:00 企画 — 第 1 週のお題消化（返信で多かった場所）
場所タグだけ差し替え（例: `aquarium, fish, blue theme` / `amusement park, ferris wheel` / `bookstore, bookshelf`）。本文: 「リクエストの◯◯、行ってきた。」

---

## 第 3 週（9/28 月〜10/4 日）— 「衣替え」

### 9/28（月）21:00 連載 — 夏服最後の日
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, short sleeves, pleated skirt, upper body, looking at viewer, smile, one eye closed, hand up, school gate, sunlight, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
本文案: 「夏服、今日でおしまい。」

### 9/30（水）06:40 交流 — ヘアスタイル差分 3 枚
`ponytail, hair scrunchie` / `twin braids` / `hair bun, hair ornament`（固定文の `long hair` はそのまま、髪型タグを追加）。本文: 「髪型変えるなら？」

### 10/1（木・衣替え）21:00 連載 — 冬服初日
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, cardigan, scarf, pleated skirt, cowboy shot, looking at viewer, light smile, blush, school gate, autumn leaves, sunlight, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
本文案: 「衣替え。ちょっと暑い。」

### 10/3（土）21:00 単発 — 様式実験 B: 水彩・アナログ（候補 2、Illustrious 側で）
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, sweater, upper body, looking at viewer, light smile, closed eyes, autumn leaves, maple leaf, park, watercolor \(medium\), traditional media, limited palette, painterly
BREAK masterpiece, best quality, absurdres, recent, general
```
CFG 4.5、Hires denoise 0.3、仕上げに紙テクスチャ（Soft Light 20%）。Anima で狙う場合は `watercolor painting style, soft pastel style` を最小構成で（07 §5: 技法の描き分けは弱いので Illustrious 側が本命）。本文案: 「秋は水彩の気分。」

### 10/4（日）14:00 企画 — 4 枚組メイキング
txt2img（Anima Turbo の構図）→ 二段の Stage 2（Illustrious）→ ADetailer 後 → 仕上げ、の 4 枚。本文: 「1 枚ができるまで。」`#AIイラスト` を付ける唯一の枠（技術系の閲覧者向け）。

---

## 第 4 週（10/5 月〜10/11 日）— 「読書の秋・体育祭」

### 10/5（月）21:00 連載 — 図書室
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, cardigan, upper body, book, reading, looking down, closed mouth, library, bookshelf, window, dappled sunlight, depth of field, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
2 枚目: `looking at viewer, light smile`（気づいて顔を上げる）。本文案: 「……見てたよ。」（キャラの口癖）

### 10/7（水）06:40 交流 — 投票「次の衣装」
X の投票機能で 4 択（メイド／巫女／ゴスロリ／ジャージ）。画像は 4 衣装のサムネ 4 枚組（`maid, maid headdress, apron` / `miko, hakama` / `gothic lolita, frilled dress, bonnet` / `track jacket, sportswear`）。結果を 10/10 に描く。

### 10/8（木）21:00 連載 — 体育祭前夜
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, track jacket, sportswear, ponytail, upper body, looking at viewer, grin, sweatdrop, hand up, school, evening, sunset, backlighting, lens flare, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
本文案: 「明日、リレーのアンカーらしい。」

### 10/10（土）21:00 単発 — 投票 1 位の衣装（または様式実験 C: セミリアル）
投票結果の衣装で全身 1 枚（③ 全身テンプレに衣装タグを差し替え）。セミリアルを試すなら Illustrious 2.5D 派生（Nova Anime3D 等）で同構図。Anima では `3D` `render` を使わない（実写化する）。

### 10/11（日）14:00 企画 — 4 週間の振り返り 4 枚組
4 週の連載から 4 枚を選び「今月のミオ」。本文: 「9 月のミオ、まとめ。」固定ポストを更新。

---

## 10/12〜10/31 の要点（ハロウィン）

| 日 | 枠 | 内容 |
|---|---|---|
| 10/12（月・スポーツの日） | 連載 | 体育祭当日（`running, sports festival, headband`） |
| 10/18（日）#ミニスカートの日 | 単発 | 記念日タグはこの日だけ 1 個付ける |
| 10/24（土） | 交流 | ハロウィン衣装の投票（魔女／吸血鬼／おばけ／黒猫） |
| 10/29（木） | 連載 | 衣装制作中（`sewing, pumpkin, night, indoors`） |
| 10/31（土）21:00 | 単発（勝負作） | 下記プロンプト。Anima → Illustrious 二段で背景込みの 1 枚 |

ハロウィン本番（Illustrious）:
```
1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, witch hat, black dress, cape, cowboy shot, looking at viewer, smile, :d, halloween, jack-o'-lantern, night, candlelight, light particles, anime screencap
BREAK masterpiece, best quality, very aesthetic, absurdres, newest, general
```
Anima 自然文: `Mio wears a wide witch hat and a black cape, grinning at the viewer with one hand raised as if casting a spell. Carved pumpkins glow with candlelight around her feet and tiny sparks drift up into the night.`
本文案: 「トリック・オア・トリート。」

---

## 記録

投稿ごとに `prompts/ab_test_protocol.md` B-3 のシートに記録し、4 週間後に「タグ 0〜1・一言本文」の効果（いいね率・返信率・フォロワー外インプレッション）を前月と比較する。

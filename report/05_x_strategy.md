# 05. X（旧Twitter）運用戦略とアルゴリズム調査（2026年9月版）

対象: @mi_Create_mi（Illustrious / Anima 生成、日本語圏）
調査日: 2026-09-09
方法: Web検索 33回（日英）＋ GitHub 上の一次資料（xai-org/x-algorithm、twitter/the-algorithm）をコード単位で確認。
制約: 本セッションのネットワークでは note.com / help.x.com / 各ブログの本文取得が遮断されたため、日本語ノウハウ記事と X 公式ヘルプは検索結果の要約に基づく（「二次」と明記）。数値の一次確認ができたのは GitHub 上のコードのみ（「一次」と明記）。確認できないものは「未確認」。

## 0. 結論（先に5行）

1. 現行アルゴリズム（2026年）は「予測確率 × 重み」の合計で並べる。公開重みでは **リンクコピー共有 20 > 返信 5 = 引用 5 = DM共有 5 > フォロー 4 > 共有 2 > RP 1 > いいね 0.5**。いいねは最弱、報告は −234。「保存したくなる・人に送りたくなる・フォローしたくなる」作品が伸びる。［一次］
2. 2026年7月から **相互フォロー相手の返信に +15 の加点**。AIイラスト界隈での相互交流が数値上の実利になった。［一次＋公式発言］
3. **センシティブ扱いは致命的**。NSFW と判定された作者のメディア投稿は全て警告表示になり、非フォロワーへの推薦（SimClusters 経由）から除外され、未成年・年齢未設定・ログアウト閲覧者には完全非表示。全年齢の本垢と NSFW サブ垢は必ず分離。［一次］
4. ハッシュタグはランキング特徴ではなく、閲覧者の「ミュートキーワード」に # の有無を問わず一致する。多用は無意味で、0〜2個が上限。ただし「#AIイラスト」を付けること自体が反AI層のTLから自動的に外れる「ゾーニング」として機能する。［一次＋Musk 発言］
5. 外部リンク・コミュニティ機能・ハッシュタグ量産・4枚組固定といった「2023〜24年の常識」は 2026 年には通用しない。コミュニティは 2026年5月に終了。

## 1. X のアルゴリズム（2025〜2026 年）

### 1.1 年表

| 時期 | 出来事 | 出典 |
|---|---|---|
| 2023-03-31 | twitter/the-algorithm 公開。初回コミットに Blue Verified 著者の乗数（圏内 4.0×、圏外 2.0×）が存在 | [初回コミットの HomeGlobalParams.scala](https://github.com/twitter/the-algorithm/blob/ec83d01dcaebf369444d75ed04b3625a0a645eb9/home-mixer/server/src/main/scala/com/twitter/home_mixer/param/HomeGlobalParams.scala)［一次］ |
| 2023-04 | 旧 Heavy Ranker の重み: 返信 13.5、プロフクリック 12、作者が返した返信 75、報告 −369 | [the-algorithm-ml README](https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md)［一次］ |
| 2024-12 | Musk「ハッシュタグはもう要らない、見た目も悪い」 | [Postory](https://postory.io/blog/twitter-hashtags-2026)［二次］ |
| 2025-02 | コミュニティ投稿が For You 等にも表示されるよう変更 | [Social Media Today](https://www.socialmediatoday.com/news/x-formerly-twitter-makes-communities-posts-visible/739116/) |
| 2025-09-03 | twitter/the-algorithm に「update for-you recommendations code」コミット。現行 main に Blue Verified 乗数は存在しない | [コミット履歴](https://github.com/twitter/the-algorithm/commits/main/home-mixer/server/src/main/scala/com/twitter/home_mixer/param/HomeGlobalParams.scala)［一次］ |
| 2025-10 | Musk「Grok が毎日1億件超の投稿と動画を全て読んで推薦する」 | [36kr](https://eu.36kr.com/en/p/3647512439918212) |
| 2025-10 | 外部リンクをアプリ内ブラウザで開き「全コンテンツの可視性を平等に」するテスト（Nikita Bier） | [Social Media Today](https://www.socialmediatoday.com/news/x-formerly-twitter-testing-links-in-app-link-post-penalties/803176/), [Tech-ish](https://tech-ish.com/2025/10/13/x-is-testing-changes-to-how-it-handles-web-links-to-external-sites/) |
| 2026-01-20 | xai-org/x-algorithm 公開（Grok ベースの Phoenix） | [TechCrunch](https://techcrunch.com/2026/01/20/x-open-sources-its-algorithm-while-facing-a-transparency-fine-and-grok-controversies) |
| 2026-02-23 | 「Made with AI」ラベルが開発中と判明 | [PiunikaWeb](https://piunikaweb.com/2026/02/23/x-to-roll-out-made-with-ai-labels-to-tackle-ai-generated-spam/) |
| 2026-03-03 | 収益分配ポリシー改定: 紛争のAI動画を無開示で投稿→90日停止、再犯で永久。メタデータや Community Notes で検知 | [Nikita Bier 投稿](https://x.com/nikitabier/status/2028873177028555201) |
| 2026-05 | コミュニティ機能終了（利用者0.4%未満、スパム通報の80%） | [Engadget](https://www.engadget.com/social-media/x-is-shutting-down-its-communities-feature-182843958.html), [Postory](https://postory.io/blog/grow-on-x-after-communities-shutdown) |
| 2026-05-15 | x-algorithm 最大の更新（187ファイル・1.8万行） | [Towards AI](https://pub.towardsai.net/x-open-sourced-its-feed-algorithm-powered-by-grok-e5a13d67e741) |
| 2026-07-13 | 相互フォロー（mutuals）の可視性ブースト | [Nikita Bier 投稿](https://x.com/nikitabier/status/2076747704248758617), [TechCrunch](https://techcrunch.com/2026/07/13/x-just-tweaked-its-algorithm-to-make-it-more-friendly-less-battleground/) |
| 2026-08-14 | README 更新（重みの誤解への注記、ブラジル選挙フィルタ） | [xai-org/x-algorithm](https://github.com/xai-org/x-algorithm)［一次］ |

### 1.2 パイプライン（一次資料）

[README](https://github.com/xai-org/x-algorithm) より。候補は Thunder（フォロー中）と Phoenix retrieval / SimClusters（圏外）から集め、17 の事前フィルタを通す。画像アカウントに関係が深いもの:

- AgeFilter: 48時間より古い投稿は候補外。コールドスタート時は 24 時間（`cold_start_max_post_age_secs: 86400`）。
- OONNsfwSimclustersFilter: 「アダルト判定された作者の投稿を、フォローしていない閲覧者向け SimClusters 候補から除外」。コードは `served_type == ForYouSimclusters && in_network == false && nsfw_author == true` で丸ごと除去（[filter 実装](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/filters/oon_nsfw_simclusters_filter.rs)）。
- NewUserMinEngagementFilter: 新規閲覧者には、圏外投稿のうちエンゲージメント閾値未満のものを見せない（[実装](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/filters/new_user_min_engagement_filter.rs)。閾値の数値は非公開）。→ 反応ゼロの投稿は新規ユーザーに届かない。
- SelfReplyChainFilter / OONRetweetReplyFilter: 自己リプ連鎖と、非フォロー相手の RP・返信は For You から落ちる。→ ツリーの2枚目以降は圏外にほぼ届かない。
- ViewerMutedKeywordFilter: 閲覧者のミュート語に「# あり／なし」両方で一致（[テストコード](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/filters/viewer_muted_keyword_filter.rs)）。

Phoenix（Transformer）が予測する行動: いいね・返信・RP・引用・共有・DM共有・リンクコピー／クリック（投稿・プロフィール・リンク・**画像拡大**・動画再生・引用元）／注意（動画品質視聴・**滞在**・滞在秒数・クリック後滞在・アクティブ秒）／作者フォロー／負（興味なし・ミュート・ブロック・報告・not dwelled）。候補は投稿の**マルチモーダル埋め込み**由来のセマンティックIDで表現され、画像内容そのものが理解される（[phoenix README](https://github.com/xai-org/x-algorithm/blob/main/phoenix/README.md)）。

### 1.3 現行の重み（2026-09-09 取得、[param.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs)）［一次］

| 行動 | 重み | 行動 | 重み |
|---|---|---|---|
| リンクコピー共有 | **20.0** | 画像拡大クリック | 0.05 |
| 返信 | 5.0 | 動画を開く | 0.07 |
| 引用 | 5.0 | 滞在（dwell） | 0.05 |
| DM 共有 | 5.0 | 連続滞在時間 | 0.004 |
| 作者フォロー | 4.0 | プロフィールクリック | **0.0** |
| 共有 | 2.0 | 動画品質視聴（VQV） | **0.0** |
| RP | 1.0 | 興味なし | −43.2 |
| いいね | 0.5 | ブロック | −31.2 |
| 投稿クリック | 0.4 | ミュート | −58.8 |
| リンクを開く | 0.2 | 報告 | **−234.0** |

補足（同ファイル・[ranking_scorer.rs](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/scorers/ranking_scorer.rs)）:
- 相互フォロー相手からの返信は重み 5.0 **+15.0**（`BidirectionalFollowReplyWeightBoost`）。オリジナル投稿のみ対象。
- 著者多様性: 同一作者の2件目以降は 0.5 ずつ減衰、下限 0.25。→ 同時刻の連投は2件目以降が半減。
- 圏外投稿は 0.75 倍（トピック経由 0.5 倍）。
- いいね率が低い投稿はクリック後滞在の評価が減額される（低 fav 率ペナルティ）。
- **verified / Premium に依存する乗数はコード上に存在しない**（home-mixer 内を "verified" で検索して 0 件）。
- ブックマークは予測行動・重みのどちらにも**存在しない**。「ブックマーク 10〜12倍」「プロフクリック 12倍」「返信 27倍」等の数字は 2023 年版や二次資料由来で、現行の公開値とは一致しない。
- README は「報告の重みはいいねの 468 倍だが、1報告が468いいねを打ち消す意味ではない。重みは各閲覧者の予測確率に掛かる」と注記。

### 1.4 質問項目ごとの整理

- 滞在時間・画像拡大: 予測対象。重み自体は小さいが、`not_dwelled` が負になり、低 fav 率で滞在評価が減額されるため「スクロールを止め、拡大させ、いいねもされる」の三点セットが前提。縦長・高精細・一目で分かる構図が有利（[tinsalo](https://tinsalo0425.com/magazine/x-algorithm-202510/)［二次］）。
- 外部リンク: 公開重みでは「リンクを開く」は +0.2 で、明示的な罰則はない。ただし [ppc.land](https://ppc.land/how-xs-algorithm-silently-kills-your-links-without-explicitly-penalizing-them/) は「リンク付き投稿はセッション終了と相関するため予測が下がり、For You 出現が 50〜70% 少ない」と主張（未確認）。2025-10 のアプリ内ブラウザ化テストで是正方向。実務は「本文にリンクを置かず、固定ポスト・プロフィール・自己リプに集約」。
- ハッシュタグ: 上記の通りランキング特徴ではない。二次資料の「3個以上でスパム判定」「複数タグで 40% 減」（[Quillly](https://reachmore.co/blogs/do-hashtags-work-on-x-2026)、[Postory](https://postory.io/blog/twitter-hashtags-2026)）は根拠未確認。
- Premium: 現行公開コードに乗数なし。ただし製品仕様として「返信の優先表示」「長文（25,000字）」「収益分配」「高画質アップロード」があり、[Buffer の 1,800 万投稿分析](https://buffer.com/resources/x-premium-review/)が Premium の効果を検証している（数値は本セッションで未取得）。二次資料の「2〜4倍」は 2023 年コード由来。
- 返信での露出: 返信 5.0（いいねの10倍）、相互なら 20.0。他者の投稿への返信でプロフィールに来てもらう導線は有効だが、非フォロワーの返信は For You から落ちる（OONRetweetReplyFilter）ため、返信は「会話欄で見られる」用途と割り切る。
- 投稿直後 30 分〜1 時間: 公開コードに「30分」という閾値は**存在しない**（未確認）。ただし 48h 窓、新規閲覧者向け閾値、served 除外 10 分などから初期反応が拡散を左右するのは構造的に妥当。[cocorochikai](https://www.cocorochikai.com/x-tips-post-time/)は「投稿後30分の引用・返信率が重要」、[MediaShower](https://www.mediashower.com/blog/how-the-x-algorithm-works/)等は「最初の30〜60分」。「初動 1000 倍」等の数値は根拠不明。
- センシティブ・年齢制限（[tweet_rules.rs](https://github.com/xai-org/x-algorithm/blob/main/visibility-filtering/rules/tweet_rules.rs)［一次］）: NSFW 高精度ラベル → 警告表示。**NSFW 作者 ＋ メディア付き → 全投稿が警告表示**。ログアウト・未成年・年齢未設定の閲覧者には NSFW を **Drop**。圏外の NSFW は Drop。→ 一度「NSFW 作者」ラベルが付くと、全年齢作品まで圏外露出を失う。[AuditSocials](https://www.auditsocials.com/blog/x-sensitive-media-content-settings-2026)（二次）は「成人向けは For You から完全除外、18歳未満・生年月日未設定は閲覧不可、AI 生成の成人向けはセンシティブ設定と AI 開示の両方が必要」と整理。
- AI 生成ラベル: 「Made with AI」ラベル（2026-02 開発中）。2026-03-03 の収益分配ポリシーは紛争 AI 動画が対象だが、「メタデータで検知」「Community Notes をトリガーに」という仕組みは AI イラストにも将来適用され得る。通常の AI イラストは禁止対象ではない。
- Grok Imagine: X 内蔵の画像・動画生成。Imagine 1.0（2026-02-03、720p 動画）、Chibi（日本アニメ風）テンプレ 2026-03、2026-04 以降は SuperGrok Lite（$10/月）等の有料が必要（[goongen](https://goongen.ai/blog/is-grok-imagine-free)、[Basenor](https://www.basenor.com/blogs/news/grok-imagine-everything-you-need-to-know-about-xais-image-video-generator)）。X 上の画像をワンタップで動画化できる（[Koukichi_T](https://koukichi-t.com/archives/47230)）ため、他人が自作を勝手に動かす「無断改変」リスクが新たに生じている。

### 1.5 仕様（公式ヘルプは未取得、複数の二次資料が一致）
画像 5MB（JPG/PNG）、GIF 15MB、1投稿4枚、最大 4096×4096、無料 280 字・Premium 25,000 字、動画は Premium+ で 4K（[Postory](https://postory.io/blog/social-media-character-image-limits-2026)、[FileSize.org](https://filesize.org/limits/twitter/)）。

## 2. 運用ノウハウ（日本語圏）

### 2.1 投稿時間帯（JST）

| 帯 | 根拠 | 出典 |
|---|---|---|
| 7〜9時 / 12〜13時 / 17〜19時 | 通勤・昼休み・帰宅のチェック時間 | [koukoku.jp](https://www.koukoku.jp/service/suketto/marketer/sns/) |
| 木曜 20〜22時が最高ER、日曜 13時以降が休日ピーク。「日曜午後×ビジュアル投稿」が最も伸びる | 2025-10 の国内アカウント分析 | [cocorochikai](https://www.cocorochikai.com/x-tips-post-time/) |
| 絵師向け: 平日夜・土日は昼〜夜 | 絵師向け時間帯解説 | [college-sales](https://college-sales.com/archives/36288) |
| 海外向け併用なら JST 深夜〜早朝（米国夜） | 2026 年版の日米欧比較 | [tetsu7017](https://www.tetsu7017.com/blog/x-optimum-posting-time/) |

AI 美少女イラストの主要層（男性・夜型）を考えると **20〜23時が本命、12時台が副、日曜 13〜16時が週末枠**。X アナリティクスで自分のフォロワーの反応時間を 4 週間分検証して固定する。

### 2.2 頻度・フォーマット
- [aimslab](https://note.com/aimslab/n/na590103b37b1)（二次・記事の主張）: 1万人到達が早い上位 5% は「週平均 4.2 投稿＋フォーマット統一」、複数枚・長文ノウハウ投稿は初動 2.8 倍。
- 枚数: [Togetter](https://togetter.com/li/2181641) は漫画で「1枚目のみ→ツリー」が「最初から4枚」よりインプレッション・新規フォロワーとも多かった実例。[tinsalo](https://tinsalo0425.com/magazine/x-algorithm-202510/) は「2〜4枚は表示面積と滞在時間で有利」。一次資料の SelfReplyChainFilter を踏まえると、**主投稿は 1〜2 枚の高品質（縦長 4:5〜3:4）、差分・4枚組は同一投稿の 2〜4 枚目に入れる**のが折衷解。ツリー2件目以降は圏外に出ないので、ツリーは既存フォロワー向けと割り切る。
- 動画（image-to-video）: 二次資料は動画優遇を主張（[comnico](https://www.comnico.jp/we-love-social/x-impression)、[TCD](https://tcd-theme.com/2025/11/x-impression.html)）が、現行公開重みは VQV 0.0・動画を開く 0.07。滞在時間を稼ぐ手段として週 1 本、5〜10 秒ループ。Grok Imagine / Wan 2.x / Kling で作成。
- 連作・オリキャラ: 作者フォロー重み 4.0 は「次も見たい」の指標。キャラに名前を付け、固定ポストで紹介し、同一キャラ・同一画風で週数回を継続（[ゆなそる](https://note.com/yunasol_ai/n/n63327fbbd2eb)、[くまっと](https://note.com/kumattokumatto/n/n998072e9cb4e)、[きいち](https://note.com/machimachijapan/n/n48ec9f0bb022)、[リラ](https://note.com/lilas_aiart/n/n82df29f37763)）。
- 引用 RT: 引用 5.0。ビフォーアフター、プロンプト公開、「あなたなら何色？」等、引用したくなる余白を作る。
- 企画: フォロワー記念・お題募集・リクエスト・投票は返信（5.0）と DM 共有（5.0）を直接生む。ただし「フォロバ企画」は質の低いフォロワーで予測確率を薄める。
- 交流: 2026-07 の相互ブースト以降、界隈の相互フォロー・返信は数値上の実利。1日 10〜20 件、本文に触れた返信を目安に。
- コミュニティ機能: 2026-05 終了。代替はリスト、相互交流、スペース、chichi-pui 等の外部（[Postory](https://postory.io/blog/grow-on-x-after-communities-shutdown)）。
- 検証記録: [nonenuni（成長記）](https://nonenuni.com/post-481/)、[さくらのまど（1週間検証）](https://sakura-mado.com/ai-xakaunto1/)、[AIロイド分析（13.4万人、1投稿 3,000 万 view）](https://note.com/orenomusumetachi/n/n2638aac4d323)。

### 2.3 ハッシュタグ戦略
- 上限 2 個。日本語 1（#AIイラスト）＋英語 1（#AIart）を基本、記念日の日は記念日タグ 1 個に差し替え。#AIグラビア #AI美少女 は NSFW クラスタに寄るためサブ垢専用。#Illustrious #ComfyUI #StableDiffusion は「モデル・技術系ノウハウ投稿」だけに使う（作品投稿に付けると生成者向けクラスタに寄り、一般層に届きにくい）。
- 絵師タグ（#イラスト好きな人と繋がりたい 等）と作品名ファンアートタグは使わない。大手 VTuber 事務所が「AI イラストにファンアートタグ禁止・AI 表記必須」を明示した例（[オレ的ゲーム速報](https://jin115.com/archives/52428060.html)）。
- 「#AIイラスト」を付けることは、AI をミュートしている層の TL から自動的に外れる = 炎上・報告（−234）の回避装置でもある。

### 2.4 プロフィール設計と併用先
- 自己紹介: 「AI生成（Illustrious/Anima）」「主役キャラ名」「投稿ペース」「R-18 はサブ垢 @xxx」を明記。固定ポストに代表作 4 枚＋各リンク。ヘッダーは主役キャラ。
- 併用: pixiv（AI 生成フラグ必須）、chichi-pui（AI 専用・[pixiv 百科](https://dic.pixiv.net/a/chichi-pui)）、Civitai（LoRA・ワークフロー）、Instagram/Threads（4:5 縦長）。Bluesky / Misskey は反 AI 感情が強く、投稿するなら AI 明記とゾーニング前提。X には作品、外部には高解像度・プロンプト・差分という「X が入口」の設計。

## 3. マネタイズと発展

| 手段 | 2026 年時点の要点 | 出典 |
|---|---|---|
| pixivFANBOX | 2023-05-10 に AI 生成作品を当面禁止、同年 11 月から全面禁止。その後「AI生成コンテンツ」設定を伴う規約改定の告知あり（内容未確認、要確認） | [ITmedia](https://www.itmedia.co.jp/news/articles/2305/10/news188.html)、[FANBOX 公式](https://official.fanbox.cc/posts/6292096) |
| Fantia | 2023-05-23 に AI 主体作品を禁止。2026-01-22 からタイトル・サムネ・説明文等に限り AI 利用解禁。手数料は 2026-08 に改定 | [地熱スープ](https://tinetu-soup.com/fantia) |
| Ci-en | 2023-05-11 に取扱停止。現状は要確認 | [基素基](https://scrapbox.io/motoso/) |
| Patreon | AI 生成に比較的寛容 | [さなぎランド](https://sanagiland.com/sales/patreon-ai-illust-hajimekata/) |
| DLsite / FANZA / BOOTH | AI 生成の表記義務が中心（6 サイト比較） | [さなぎランド 規約マップ](https://sanagiland.com/sales/ai-illust-pf-yakkan-map/)、[手数料一覧](https://note.com/hirop557/n/n99f2d4781e36) |
| Kindle（KDP） | AI グラビア写真集が KU 経由で読まれる。AI 生成の申告が必要 | [ふじーブログ](https://fujichannel.com/earn-with-ai-illustrations-on-kindle/) |
| 総合 | 支援は FANBOX/Patreon/DLsite に分散、R-18 は DLsite・Patreon へ | [aimslab 収益化ガイド](https://note.com/aimslab/n/nf2d521fcb78e) |

NSFW 寄りにする場合: 一次資料の通り「NSFW 作者」ラベルは全メディア投稿の警告表示と圏外除外を招く。**本垢は水着まで・肌面積控えめ、R-18 はサブ垢でセンシティブ設定 ON・プロフに 18+**。2025-11-06 と 2026-03-12 に大規模凍結（[Shuttlerock](https://www.shuttlerock.co.jp/article/detail/post-20728/)、[てんねん](https://note.com/munou_ac/n/nf5268be4dd99)）。2025 年後半から肌露出面積の自動判定が強化され、設定済みでも判定される例が増加（[AIバズクラウド](https://ai-buzzcloud.com/x-growth/667/)、[BAN 回避チェックリスト](https://note.com/texture_lora_lab/n/nc847cb2dd546)）。

## 4. リスクとマナー

- 版権キャラ: 二次創作ガイドラインの確認が前提。AI 生成の版権ファンアートは炎上事例が最多（[反AI.com まとめ](https://onsyudasyuda.com/ai-artist-backlash/)、[生成AI問題まとめwiki](https://w.atwiki.jp/genai_problem/pages/38.html)、[企業炎上7選](https://exawizards.com/column/article/generative-ai-flaming-cases/)）。オリキャラ主体が最も安全。
- 「AI 生成であることの明記」は日本語圏の事実上の必須マナー。未明記は「手描き偽装」として最も嫌われ、AI 疑惑の魔女狩り側の事件も多い（[反AIによる事件一覧](https://dic.pixiv.net/a/%E5%8F%8DAI%E3%81%AB%E3%82%88%E3%82%8B%E4%BA%8B%E4%BB%B6%E4%B8%80%E8%A6%A7)、[Blitz Marketing](https://blitz-marketing.co.jp/column/19920/)）。
- Community Notes: AI 画像に「AI生成」ノートが付く事例が増加。2026-03 以降はノートが収益停止のトリガーにもなるため、自己申告で先回りする。
- 無断転載・透かし: 半透明の署名＋隅の ID、高解像度は外部限定（[きこ](https://note.com/kikotan/n/n988f9a56f08b)、[さくろぐ](https://saculog.com/illust-water-mark/)）。
- 反 AI 層との距離: 反論しない、引用で晒さない、ブロックは静かに。
- NG 行動: 手描き偽装／絵師タグ・ファンアートタグ／他人の絵を i2i／実在人物・未成年に見える性的表現／センシティブ未設定／短時間の大量投稿・大量フォロー（[ぶろ太](https://burota-blog.com/x-tooketsu-taisaku/)）／本文に外部リンク。

## 5. 競合分析の型

見る指標: いいね率（いいね÷インプ、目安 1〜3%）、返信率・引用率、フォロワー増加率（週）、投稿フォーマット（枚数・縦横・文字量・タグ数）、投稿時刻の分布、プロフィールクリック率（自分は X アナリティクスで確認）、固定ポストと導線。
ツール: X アナリティクス、SocialDog 無料プラン（[アプリの達人](https://app-tatsujin.com/socialdog-free-plan-2026/)）、Metricool・Buffer の無料枠、[ITトレンド](https://it-trend.jp/sns_management_tool/article/884-4999)、[フルスピード](https://growthseed.jp/experts/sns/twitter-analytics-tools/)。

## 6. 週間投稿プラン例（週5投稿）

| 曜日 | 時刻 | 内容 | 狙う行動 |
|---|---|---|---|
| 月 | 21:00 | 主役キャラの新作 1 枚（縦長） | 画像拡大・滞在・フォロー |
| 水 | 12:15 | 差分 2〜3 枚を 1 投稿に（表情・衣装違い） | 滞在・返信（どれが好き？） |
| 木 | 21:00 | 週のメイン作品＋記念日タグがあれば差し替え | 引用・共有・フォロー |
| 土 | 21:00 | 5〜10 秒ループ動画（image-to-video） | 動画再生・滞在 |
| 日 | 14:00 | 4 枚組シリーズ回 or 企画（お題募集・投票） | 返信・DM 共有・引用 |
| 毎日 | 随時 | 相互・界隈への返信 10〜20 件、自作の固定ポスト更新は月 1 | 相互ブースト |

## 7. 年間イベントカレンダー（AI 美少女向け）

日付の主出典: [goroawase-art-days](https://github.com/zoiteki/goroawase-art-days)［一次データ］、[ねこみなブログ 127 選](https://nekomina.blog/illustration-hashtag/)、[rosebud](https://rosebud.work/archives/6069)、[tsumetsume](https://tsumetsume.com/illust-twitter-hashtag-bymonths2)、[ピクシブ百科 ツインテールの日](https://dic.pixiv.net/a/%E3%83%84%E3%82%A4%E3%83%B3%E3%83%86%E3%83%BC%E3%83%AB%E3%81%AE%E6%97%A5)。

| 月 | ネタ | 主なタグ（日付） |
|---|---|---|
| 1 | 晴れ着・初詣・こたつ・成人式（第2月曜） | #犬の日(1/11) |
| 2 | 節分(2/3)・バレンタイン(2/14)・雪 | #ツインテールの日(2/2) #ニーハイの日(2/8) #猫の日(2/22) |
| 3 | ひな祭り・ホワイトデー(3/14)・卒業・桜 | #うさぎの日(3/3) #巫女の日(3/5) #ミクの日(3/9) |
| 4 | 入学・新生活・桜・エイプリルフール | GW 前の旅行ネタ |
| 5 | GW(4/29〜5/6)・母の日 | #メイドの日(5/10) #ストッキングの日(5/15) |
| 6 | 梅雨・傘・衣替え | #百合の日(6/25) #スク水の日(6/29) |
| 7 | 七夕(7/7)・海の日(第3月曜)・夏祭り | #ビキニの日(7/5) #ポニーテールの日(7/7・要確認) #夏風呂の日(7/26) |
| 8 | 花火・浴衣・海・帰省 | #パンツの日(8/2) #バニーの日(8/2, 8/21, 8/23) |
| 9 | 秋服・月見・体育祭 | #チルノの日(9/9) |
| 10 | ハロウィン(10/31)・秋・文化祭 | #ミニスカートの日(10/18) |
| 11 | 「いい◯◯の日」祭り・紅葉 | #タイツの日(11/2) #いい水着の日(11/3) #いい推しの日(11/4) #ポッキーの日(11/11) #いい太ももの日(11/20) #いいツインテールの日(11/22) #いいニーハイの日(11/28) #いいスク水の日(11/29) |
| 12 | クリスマス(12/24〜25)・大晦日・冬服 | #ニコニコ(12/12) 年末の振り返り 4 枚組 |

「黒タイツの日」は本調査で日付を確認できず（未確認）。11/2 の #タイツの日 を使うのが確実。

## 8. X で伸ばすためのアクション Top 20

1. 本垢は全年齢固定。R-18 はサブ垢に分離し、センシティブ設定 ON。「NSFW 作者」ラベルを本垢に付けない（一次資料の Drop / 警告ルール）。
2. 主役オリキャラに名前を付け、固定ポストで紹介。フォロー予測（重み 4.0）を狙う。
3. 1 投稿 1〜2 枚の高品質縦長を基本、差分は同投稿の 2〜4 枚目へ。ツリーは圏外に出ないと割り切る。
4. 週 4〜5 投稿を同じ時刻に固定（20〜23 時本命、日曜午後を週末枠）。
5. 同時刻の連投はしない（2 件目以降 0.5 倍減衰）。
6. ハッシュタグは 0〜2 個。#AIイラスト ＋ #AIart、記念日は当日のみ差し替え。
7. 絵師タグ・ファンアートタグ・版権キャラ名タグは使わない。
8. 本文とプロフィールに AI 生成と使用モデル（Illustrious/Anima）を明記し、Community Notes を先回りする。
9. 本文に外部リンクを置かない。リンクは固定ポスト・プロフィール・自己リプへ。
10. 「人に送りたくなる」作品を意識する（リンクコピー 20、DM 共有 5 が最大級の重み）。
11. 相互フォロー相手の返信は +15。界隈の AI 絵師 100 人前後をフォローし、毎日 10〜20 件の内容ある返信。
12. 引用したくなる余白（ビフォーアフター、プロンプト公開、投票）を月 2 回。
13. 月 1 回の企画（お題募集・フォロワー記念）で返信と DM 共有を生む。
14. 週 1 本の 5〜10 秒ループ動画で滞在時間を稼ぐ。
15. 投稿後 30〜60 分は返信に即応し、初動の会話を作る（30 分閾値自体は未確認だが構造的に有利）。
16. 反応ゼロの投稿は新規閲覧者に届かない。伸びなかった作品は削除せず、時間帯を変えて別カットで再投稿。
17. 版権キャラは避け、季節・記念日ネタはオリキャラで消化する。
18. 透かし＋署名、高解像度は pixiv / Fantia / Patreon 限定にして X を入口にする。
19. 反 AI 層とは論争しない。静かにブロック、引用で晒さない。報告（−234）を誘発しない。
20. X アナリティクス＋SocialDog 無料枠で、いいね率・プロフィールクリック・時間帯を 4 週間単位で見直す。

# AIイラスト × X 攻略リサーチ（2026年9月）

Illustrious（SD WebUI）と Anima（ComfyUI）で 2 次元美少女イラストを制作し X に投稿する @mi_Create_mi 向けに、「X で伸びている AI イラストの傾向」「最新モデルのプロンプト技術」「高品質化ワークフロー」「X 運用戦略」を調査・分析し、具体的な提案にまとめたリポジトリです。

第 2 回（2026-09-09 続き）では、前回遮断されていた X・pixiv・Civitai・Hugging Face・note・Danbooru に直接アクセスし、**実際の投稿データによる分析（06）**と**一次資料によるプロンプトの検証・修正（07）**、**検証ツール（tools/）**を追加しました。

## まず読む
- **[report/00_summary_and_proposal.md](report/00_summary_and_proposal.md)** — 結論と提案（コンテンツ戦略・プロンプト戦略・ワークフロー・X 運用・30 日プラン）。冒頭に第 2 回の更新点。
- **[report/06_x_post_analysis.md](report/06_x_post_analysis.md)** — @mi_Create_mi の実投稿 70 件と同業 15 アカウント 1,239 件の分析。**本垢の画像投稿が公式 oEmbed API で「not authorized」になっている**発見、その仕組み（公開コード）、Under the Hood レポートの仕様と読み方、対処。

## 調査レポート（事実と出典）
| # | ファイル | 内容 |
|---|---|---|
| 01 | [report/01_x_trend_analysis.md](report/01_x_trend_analysis.md) | X で伸びている AI イラスト投稿の傾向、人気アカウントの類型、2025〜2026 の画風・モデルトレンド、コンテストの評価軸 |
| 02 | [report/02_illustrious_prompting.md](report/02_illustrious_prompting.md) | Illustrious XL の系譜・派生モデル・品質タグ・タグ順・絵師タグ・ネガティブ・生成設定・失敗対策・実例 |
| 03 | [report/03_anima_comfyui.md](report/03_anima_comfyui.md) | Anima の履歴・公式プロンプト記法・ComfyUI 推奨設定・LoRA/LLLite・コミュニティ知見・Illustrious との使い分け |
| 04 | [report/04_quality_pipeline.md](report/04_quality_pipeline.md) | Hires/Detailer/Upscale、二段モデル構成、ControlNet・Regional・Inpaint、演出技法、キャラ LoRA、動画化、X 向け画像仕様 |
| 05 | [report/05_x_strategy.md](report/05_x_strategy.md) | X アルゴリズム（公開コードの重み）、投稿時間・頻度・ハッシュタグ、マネタイズ、リスク、週間プラン、年間イベントカレンダー |
| 06 | [report/06_x_post_analysis.md](report/06_x_post_analysis.md) | **新規**: 実投稿データの分析（プロフィール・投稿の型・月別/要素別の反応・上位投稿・同業比較・可視性フィルタの検証・提案の修正） |
| 07 | [report/07_prompt_verification.md](report/07_prompt_verification.md) | **新規**: Anima README・Civitai モデルカード・Danbooru タグ DB・108 スタイル比較記事で 02/03 とテンプレを検証し、13 項目を修正 |

## すぐ使えるもの
| ファイル | 用途 |
|---|---|
| [prompts/illustrious_templates.md](prompts/illustrious_templates.md) | Illustrious 系のコピペ用テンプレ（5 パターン、**75 トークン以内・Danbooru 正規表記に改訂**）・モデル別品質タグ・クイックリファレンス |
| [prompts/anima_templates.md](prompts/anima_templates.md) | Anima のコピペ用テンプレ（5 パターン）・記法の要点・**108 枚比較に基づく様式語の効く/効かない一覧** |
| [prompts/anima_styles.md](prompts/anima_styles.md) | **新規**: JANIMA のモデルカード要約と、Anima 系で効く画風プロンプトのカタログ（年代・画材・モノクロ・配色・装飾・メタタグ、根拠つき）。候補一覧は `prompts/wildcards/anima_style.txt` |
| [prompts/tag_dictionary_verified.md](prompts/tag_dictionary_verified.md) | **新規**: 推奨タグ 400 語超の Danbooru 投稿数付き辞典、別名・非タグの置き換え表、モデル固有タグ一覧 |
| [prompts/character_sheet_template.md](prompts/character_sheet_template.md) | **新規**: オリキャラ設定シートと両モデル用固定プロンプト、衣装バリエーション、LoRA なし一貫性、LoRA 化 |
| [prompts/post_calendar_2026-09-10.md](prompts/post_calendar_2026-09-10.md) | **新規**: 9/14〜10/11 の 4 週間投稿カレンダー（各枠のプロンプト・本文案）＋ハロウィン |
| [prompts/ab_test_protocol.md](prompts/ab_test_protocol.md) | **新規**: 生成側の X/Y/Z plot 手順と採点表、投稿側の 2 週間 A/B 手順 |
| [prompts/wildcards/](prompts/wildcards/) | Dynamic Prompts 用ワイルドカード（光・画角・表情・衣装・季節・様式・髪型）— 全行を正規表記に更新 |
| [tools/prompt_lint.py](tools/prompt_lint.py) | **新規**: プロンプト検証・変換 CLI。Danbooru 実在/別名/投稿数、CLIP 75 トークン境界、モデル別ルール、Illustrious⇄Anima 変換（[tools/README.md](tools/README.md)） |
| [tools/check_embed.py](tools/check_embed.py) | **新規**: X の公式 oEmbed API で投稿の表示制限（RESTRICTED / OK）を確認。設定変更後の効果確認に使う（06 §3.3） |
| [workflows/anima_t2i_hires.json](workflows/anima_t2i_hires.json) | ComfyUI 用 Anima ワークフロー: txt2img → 1.25x 2nd pass → 2x ESRGAN（`build_anima_workflow.py` で再生成） |
| [workflows/anima_to_illustrious_2stage.json](workflows/anima_to_illustrious_2stage.json) | **新規**: 二段構成ワークフロー: Anima（構図）→ pixel 受け渡し → Illustrious img2img ＋ ControlNet tile → 2x（`build_two_stage_workflow.py` で再生成） |
| [workflows/anima_style_test.json](workflows/anima_style_test.json) | **新規**: 同一 seed・同一本文で 8 様式を横並びにして 4×2 の一覧を出す画風テスト（JANIMA / Anima、コアノードのみ。`build_style_test_workflow.py` で再生成） |
| [workflows/legendaer_anima_v8_guide.md](workflows/legendaer_anima_v8_guide.md) | **新規**: JANIMA カード推奨の Legendaer 版「Anima Preview Workflow」V8（Basic / Standard / Advanced / Detailer）の使い方。必要なカスタムノードとモデル、Fast Groups Bypasser での機能 ON/OFF、初回手順、各グループの既定値 |

```bash
python3 tools/prompt_lint.py --model illustrious "1girl, solo, silver hair, violet eyes, ..., masterpiece, best quality, general"
python3 tools/prompt_lint.py --model illustrious --convert-to anima "..."
python3 tools/test_prompt_lint.py
```

## 調査の制約
- 第 1 回: X 本体・note・pixiv・Civitai・Hugging Face・docs.comfy.org への直接アクセスが遮断されていたため、多くは検索エンジン経由の二次情報（01〜05）。
- 第 2 回: X は公開 API（syndication / FxTwitter）で取得。@mi_Create_mi の投稿は検索でインデックスされた 70 件（2025-06〜2026-04）に限られ、閲覧数は取れるがプロフィールクリック等の内部指標は取れない。Danbooru API は途中から Cloudflare に遮断されたため、タグ投稿数は tagcomplete 同梱 DB のスナップショット。
- 各レポートの「未確認」「要確認」「推測」の表記を確認し、数値は自分の環境と X アナリティクスで検証してください。

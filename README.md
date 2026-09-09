# AIイラスト × X 攻略リサーチ（2026年9月）

Illustrious（SD WebUI）と Anima（ComfyUI）で 2 次元美少女イラストを制作し X に投稿する @mi_Create_mi 向けに、「X で伸びている AI イラストの傾向」「最新モデルのプロンプト技術」「高品質化ワークフロー」「X 運用戦略」を調査・分析し、具体的な提案にまとめたリポジトリです。

## まず読む
- **[report/00_summary_and_proposal.md](report/00_summary_and_proposal.md)** — 結論と提案（コンテンツ戦略・プロンプト戦略・ワークフロー・X 運用・30 日プラン）

## 調査レポート（事実と出典）
| # | ファイル | 内容 |
|---|---|---|
| 01 | [report/01_x_trend_analysis.md](report/01_x_trend_analysis.md) | X で伸びている AI イラスト投稿の傾向、人気アカウントの類型、2025〜2026 の画風・モデルトレンド、コンテストの評価軸 |
| 02 | [report/02_illustrious_prompting.md](report/02_illustrious_prompting.md) | Illustrious XL の系譜・派生モデル・品質タグ・タグ順・絵師タグ・ネガティブ・生成設定・失敗対策・実例 |
| 03 | [report/03_anima_comfyui.md](report/03_anima_comfyui.md) | Anima の履歴・公式プロンプト記法・ComfyUI 推奨設定・LoRA/LLLite・コミュニティ知見・Illustrious との使い分け |
| 04 | [report/04_quality_pipeline.md](report/04_quality_pipeline.md) | Hires/Detailer/Upscale、二段モデル構成、ControlNet・Regional・Inpaint、演出技法、キャラ LoRA、動画化、X 向け画像仕様 |
| 05 | [report/05_x_strategy.md](report/05_x_strategy.md) | X アルゴリズム（公開コードの重み）、投稿時間・頻度・ハッシュタグ、マネタイズ、リスク、週間プラン、年間イベントカレンダー |

## すぐ使えるもの
| ファイル | 用途 |
|---|---|
| [prompts/illustrious_templates.md](prompts/illustrious_templates.md) | Illustrious 系のコピペ用テンプレ（5 パターン）・タグ辞典・共通設定 |
| [prompts/anima_templates.md](prompts/anima_templates.md) | Anima のコピペ用テンプレ（5 パターン）・記法の要点・版ごとの設定 |
| [prompts/wildcards/](prompts/wildcards/) | Dynamic Prompts 用ワイルドカード（光・画角・表情・衣装・季節・様式・髪型） |
| [workflows/anima_t2i_hires.json](workflows/anima_t2i_hires.json) | ComfyUI 用 Anima ワークフロー（コアノードのみ）: txt2img → 1.25x 2nd pass → 2x ESRGAN。`build_anima_workflow.py` で再生成可能 |

## 調査の制約
- 調査環境から X 本体・note・pixiv・Civitai・Hugging Face・docs.comfy.org への直接アクセスが遮断されていたため、X の個別投稿は分析できず、多くは検索エンジン経由の二次情報です。X のアルゴリズムは GitHub 上の公開コード（xai-org/x-algorithm）を一次資料として確認しています。
- 各レポートの「未確認」「要確認」「推測」の表記を確認し、数値は自分の環境と X アナリティクスで検証してください。

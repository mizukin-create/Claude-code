from .tag_formatter import format_tags


class TagFormatter:
    """Reorder Danbooru-style tags by category and/or strip character-defining tags."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "", "dynamicPrompts": False,
                                    "tooltip": "整形したいプロンプト（カンマ区切りタグ。Anima 用の自然文は末尾にそのまま残ります）"}),
                "mode": (["reorder", "remove_character", "remove_character_and_reorder"],
                         {"default": "reorder", "tooltip":
                          "reorder: カテゴリ順に並べ替え\n"
                          "remove_character: キャラ要素タグを削除（順序は維持）\n"
                          "remove_character_and_reorder: 削除してから並べ替え"}),
                "remove_scope": (["appearance_and_name", "appearance", "name"],
                                 {"default": "appearance_and_name", "tooltip":
                                  "appearance: 髪・目・肌・体型など外見タグ\n"
                                  "name: キャラ名/作品名（`name (series)` 形式と categories/character_names.txt）"}),
                "remove_clothes": ("BOOLEAN", {"default": False, "tooltip":
                                   "キャラ要素の削除時に、女服（衣装・装飾品）も一緒に削除する（LoRA の既定衣装を出したいとき）"}),
                "dedupe": ("BOOLEAN", {"default": True, "tooltip": "重複タグを最初の1つだけ残す"}),
                "group_separator": (["blank_line", "newline", "comma"], {"default": "blank_line", "tooltip":
                                    "並べ替え時のカテゴリ間の区切り。blank_line: 空行 / newline: 改行 / comma: カンマのみ"}),
            },
            "optional": {
                "keep_tags": ("STRING", {"multiline": False, "default": "",
                                         "tooltip": "削除しないタグ（カンマ区切り）。例: long hair, blue eyes"}),
                "extra_character_tags": ("STRING", {"multiline": False, "default": "",
                                                    "tooltip": "追加で削除するタグ（カンマ区切り）。例: my_character_name"}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "removed_tags", "report")
    FUNCTION = "run"
    CATEGORY = "utils/text"
    DESCRIPTION = ("タグを 品質→女キャラ(人数・外見)→女服→女表情→女ポーズ→画角→男タグ→その他→自然文 の順に整形し、"
                   "必要ならキャラ要素（外見・キャラ名）を削除します。分類辞書は categories/*.txt で編集できます。")

    def run(self, text, mode, remove_scope, remove_clothes, dedupe, group_separator,
            keep_tags="", extra_character_tags=""):
        return format_tags(text, mode=mode, remove_scope=remove_scope, remove_clothes=remove_clothes,
                           keep_tags=keep_tags, extra_character_tags=extra_character_tags,
                           dedupe=dedupe, group_separator=group_separator)


NODE_CLASS_MAPPINGS = {"TagFormatter": TagFormatter}
NODE_DISPLAY_NAME_MAPPINGS = {"TagFormatter": "Tag Formatter (整形・キャラ要素削除)"}

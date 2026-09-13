"""Run: python3 -m pytest tests/  or  python3 tests/test_tag_formatter.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tag_formatter import classify, format_tags, normalize  # noqa: E402

ANIMA = ("masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, upper body, "
         "looking at viewer, long silver hair, blunt bangs, violet eyes, bright pupils, gentle smile, parted lips, blush, "
         "white blouse, sailor collar, rooftop, sunset, orange sky, backlighting, rim lighting, wind, floating hair, "
         "depth of field, anime coloring, clean lineart.\n"
         "A girl on a school rooftop at sunset looks back at the viewer, the low sun behind her outlining her hair "
         "with warm light while the city below fades into haze.")


def test_normalize():
    assert normalize("(long_hair:1.2)") == "long hair"
    assert normalize("((Blue Eyes))") == "blue eyes"
    assert normalize("ganyu \\(genshin impact\\)") == "ganyu (genshin impact)"
    assert normalize("(masterpiece, best quality:1.3)") == "masterpiece"
    assert normalize("clean lineart.") == "clean lineart"


def test_classify():
    cases = {
        "masterpiece": "quality", "score_7": "quality", "year 2025": "quality", "safe": "quality",
        "1girl": "girl_subject", "solo": "girl_subject", "solo focus": "girl_subject",
        "long silver hair": "girl_appearance", "violet eyes": "girl_appearance", "blunt bangs": "girl_appearance",
        "bright pupils": "girl_appearance", "large breasts": "girl_appearance", "cat ears": "girl_appearance",
        "ganyu (genshin impact)": "girl_appearance", "hatsune miku": "girl_appearance",
        "white blouse": "girl_clothes", "sailor collar": "girl_clothes", "hair ribbon": "girl_clothes",
        "hair ornament": "girl_clothes", "thighhighs": "girl_clothes", "arm warmers": "girl_clothes",
        "gentle smile": "girl_expression", "blush": "girl_expression", "closed eyes": "girl_expression",
        "looking at viewer": "girl_expression", "parted lips": "girl_expression",
        "floating hair": "girl_pose", "hand on hip": "girl_pose", "arms up": "girl_pose", "sitting": "girl_pose",
        "looking back": "girl_pose", "holding umbrella": "girl_pose",
        "upper body": "camera", "depth of field": "camera", "from below": "camera", "cowboy shot": "camera",
        "1boy": "male", "male focus": "male", "old man": "male", "muscular male": "male",
        "rooftop": "other", "sunset": "other", "backlighting": "other", "anime coloring": "other",
        "<lora:foo:0.8>": "other", "old woman": "girl_subject",
    }
    bad = {t: (classify(normalize(t)), want) for t, want in cases.items() if classify(normalize(t)) != want}
    assert not bad, bad


def test_reorder_keeps_prose_and_period():
    out, removed, report = format_tags(ANIMA, mode="reorder")
    tags, prose = out.split("\n", 1)
    assert prose.startswith("A girl on a school rooftop")
    assert tags.endswith("clean lineart.")
    assert tags.startswith("masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, "
                           "long silver hair, blunt bangs, violet eyes, bright pupils, white blouse, sailor collar, "
                           "looking at viewer, gentle smile, parted lips, blush, floating hair, upper body, depth of field, "
                           "rooftop")
    assert removed == ""
    assert "女ポーズ: floating hair" in report


def test_remove_character():
    out, removed, _ = format_tags(ANIMA, mode="remove_character")
    assert removed == "long silver hair, blunt bangs, violet eyes, bright pupils"
    assert "violet eyes" not in out
    assert "1girl, solo" in out  # subject tags survive
    # original order preserved in remove-only mode
    assert out.startswith("masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, upper body")


def test_remove_scope_and_keep():
    text = "1girl, ganyu (genshin impact), genshin impact, blue hair, horns, smile"
    out, removed, _ = format_tags(text, mode="remove_character_and_reorder", remove_scope="name")
    assert removed == "ganyu (genshin impact), genshin impact"
    assert out == "1girl, blue hair, horns, smile"
    out, removed, _ = format_tags(text, mode="remove_character_and_reorder", keep_tags="horns")
    assert removed == "ganyu (genshin impact), genshin impact, blue hair"
    assert out == "1girl, horns, smile"
    out, removed, _ = format_tags(text, mode="remove_character", extra_character_tags="smile")
    assert "smile" in removed


def test_weights_dedupe_break():
    text = "(masterpiece:1.2), long hair, (long hair:1.1), 1girl BREAK smile, red dress"
    out, _, _ = format_tags(text)
    assert out == "(masterpiece:1.2), 1girl, long hair BREAK red dress, smile"
    out, _, _ = format_tags("long hair, long_hair, 1girl", dedupe=False)
    assert out == "1girl, long hair, long_hair"


if __name__ == "__main__":
    import traceback
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok  ", name)
            except Exception:
                fails += 1
                print("FAIL", name)
                traceback.print_exc()
    sys.exit(1 if fails else 0)

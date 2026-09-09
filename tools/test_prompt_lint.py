#!/usr/bin/env python3
"""python3 tools/test_prompt_lint.py — prompt_lint の自己テスト（外部依存なし）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prompt_lint as pl  # noqa: E402

db = pl.TagDB()
tok = pl.ClipTokenizer()


def codes(res):
    return {f["code"] for f in res["findings"]}


def test_tokenizer_matches_clip_reference():
    # openai/CLIP の既知の値: "a photo of a cat" は [320, 1125, 539, 320, 2368]
    assert tok.encode("a photo of a cat") == [320, 1125, 539, 320, 2368], tok.encode("a photo of a cat")
    assert tok.count("1girl, solo") == 4  # '1', 'girl', ',', 'solo'


def test_alias_detection():
    res = pl.lint("1girl, solo, violet eyes, white blouse, masterpiece, best quality, general, backlighting, upper body, light smile, blush",
                  "illustrious", db=db, tok=tok)
    assert "alias" in codes(res)
    assert "purple eyes" in res["canonical_prompt"] and "white shirt" in res["canonical_prompt"]


def test_unknown_and_non_danbooru():
    res = pl.lint("1girl, cinematic lighting, thisisnotatag, masterpiece, general", "illustrious", db=db, tok=tok)
    assert "non-danbooru" in codes(res)
    assert "unknown" in codes(res)


def test_chunking_and_break():
    p = ", ".join(["1girl"] + ["long hair"] * 60) + " BREAK by someone, best quality"
    res = pl.lint(p, "rouwei", db=db, tok=tok)
    assert len(res["chunks"]) >= 2
    assert res["chunks"][0]["tokens"] <= 75


def test_anima_rules():
    res = pl.lint("masterpiece, best quality, score_7, safe, 1girl, long_hair, @some artist, smile", "anima", variant="aesthetic", db=db)
    c = codes(res)
    assert "anima-aesthetic-score" in c
    assert "anima-underscore" in c
    assert res["artist_tags"] == ["@some artist"]


def test_negative_checks():
    res = pl.lint("worst quality, low quality, lowres", "illustrious", negative=True, db=db, tok=tok)
    assert "neg-nsfw" in codes(res)
    res2 = pl.lint("worst quality, low quality, score_1, score_2, score_3, artist name, sensitive, nsfw, explicit", "anima", negative=True, db=db)
    assert "anima-neg-rating" not in codes(res2)


def test_convert_to_anima():
    src = "1girl, solo, violet eyes, anime screencap, masterpiece, best quality, very aesthetic, absurdres, newest, general"
    out = pl.convert(src, "illustrious", "anima", db=db)
    assert out.startswith("masterpiece, best quality, score_7, newest, absurdres, safe, 1girl, solo, purple eyes, anime screenshot"), out
    assert "very aesthetic" not in out and "general" not in out
    neg = pl.convert("worst quality, low quality, bad hands, nsfw", "illustrious", "anima", negative=True, db=db)
    assert "score_1" in neg and "sensitive, nsfw, explicit" in neg


def test_convert_to_illustrious():
    src = "masterpiece, best quality, score_7, year 2025, safe, 1girl, @foo bar, anime screenshot"
    out = pl.convert(src, "anima", "illustrious", db=db)
    assert "score_7" not in out and out.endswith("masterpiece, best quality, very aesthetic, absurdres, newest, general") and "anime screencap" in out and "foo bar" in out and "@" not in out, out


def test_low_count_warning():
    res = pl.lint("1girl, long shadow, masterpiece, general", "illustrious", db=db, tok=tok)
    assert "low-count" in codes(res)


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("ok  ", name)
            except AssertionError as e:
                fails += 1
                print("FAIL", name, e)
    print("failures:", fails)
    sys.exit(1 if fails else 0)

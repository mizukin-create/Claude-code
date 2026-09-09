#!/usr/bin/env python3
"""check_embed.py — X の公式 oEmbed API で、投稿がログアウト閲覧者に表示できる状態かを確認する。

使い方
  python3 tools/check_embed.py https://x.com/mi_Create_mi/status/2037877591366144317 [URL ...]
  python3 tools/check_embed.py -f urls.txt          # 1 行 1 URL

判定
  OK          : oEmbed が HTML を返す（ログアウト閲覧者にも表示される）
  RESTRICTED  : "Sorry, you are not authorized to see this status."
                → 公開コード（visibility-filtering/rules/tweet_rules.rs の sensitive_viewer_logged_out）では
                  「メディア付き かつ（NSFW ラベル または 投稿の nsfw フラグ）」の投稿がログアウト閲覧者に Drop される応答。
                  投稿の nsfw フラグは、作者の「センシティブなメディアとしてマーク」設定（user.safety.nsfw_user）を
                  投稿時に引き継ぐ。同じ作者の画像なし投稿が OK で画像付きだけ RESTRICTED なら、この設定かラベルが原因。
  NOT_FOUND   : 削除済み・非公開・URL 誤り
依存ライブラリなし（Python 3.9+）。
"""
import json
import sys
import urllib.parse
import urllib.request

OEMBED = "https://publish.twitter.com/oembed?url="


def check(url: str) -> str:
    req = urllib.request.Request(OEMBED + urllib.parse.quote(url, safe=""), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            return f"HTTP_{e.code}"
    if "html" in body:
        return "OK"
    err = str(body.get("error", ""))
    if "not authorized" in err:
        return "RESTRICTED"
    if "No status found" in err or "does not exist" in err or "not found" in err.lower():
        return "NOT_FOUND"
    return f"ERROR: {err[:80]}"


def main(argv):
    urls = []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "-f":
            urls += [l.strip() for l in open(args.pop(0), encoding="utf-8") if l.strip()]
        else:
            urls.append(a)
    if not urls:
        print(__doc__)
        return 2
    bad = 0
    for u in urls:
        status = check(u)
        bad += status != "OK"
        print(f"{status:12s} {u}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

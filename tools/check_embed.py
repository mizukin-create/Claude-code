#!/usr/bin/env python3
"""check_embed.py — X の公式 oEmbed API で、投稿がログアウト閲覧者に表示できる状態かを確認する。

使い方
  python3 tools/check_embed.py https://x.com/mi_Create_mi/status/2037877591366144317 [URL ...]
  python3 tools/check_embed.py -f urls.txt            # 1 行 1 URL
  python3 tools/check_embed.py --detail URL [URL ...]  # FxTwitter API で possibly_sensitive とメディア数も表示

判定
  OK          : oEmbed が HTML を返す（ログアウト閲覧者にも表示される）
  RESTRICTED  : "Sorry, you are not authorized to see this status."
                → 公開コード（visibility-filtering/rules/tweet_rules.rs の sensitive_viewer_logged_out）では
                  「メディア付き かつ（NSFW_HIGH_PRECISION / NSFW_HIGH_RECALL ラベル または is_nsfw_flagged）」の
                  投稿がログアウト閲覧者に Drop される応答。is_nsfw_flagged（models/mod.rs）は
                  作者の nsfw_user（「センシティブなメディアとしてマーク」設定）/ nsfw_admin（運営付与）、
                  投稿の nsfw.user / nsfw.admin のいずれか。
  NOT_FOUND   : 削除済み・非公開・URL 誤り

--detail の読み方（FxTwitter API の値。公式 API とは別経路）
  sensitive=True  : 投稿の利用者フラグあり（投稿時の作者設定か、投稿ごとの内容警告）。設定を OFF にして新しい投稿で確認する
  sensitive=False : 利用者フラグなし。RESTRICTED なら分類器の投稿ラベルか運営フラグが原因（Under the Hood で確認）

画像なし投稿が OK で画像付きが RESTRICTED なら、作者単位の状態（設定・ラベル・運営フラグ）が原因。
設定変更後は新しい投稿で確認する（過去投稿のラベル・フラグは残る）。依存ライブラリなし（Python 3.9+）。
"""
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

OEMBED = "https://publish.twitter.com/oembed?url="
FX = "https://api.fxtwitter.com/"
STATUS_RE = re.compile(r"(?:x|twitter)\.com/([^/]+)/status/(\d+)")


def _get_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def check(url: str) -> str:
    code = 200
    try:
        body = _get_json(OEMBED + urllib.parse.quote(url, safe=""))
    except urllib.error.HTTPError as e:
        code = e.code
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = {}
    if "html" in body:
        return "OK"
    msgs = [str(body.get("error", ""))]
    msgs += [str(x.get("message", "")) for x in body.get("errors", []) if isinstance(x, dict)]
    err = " / ".join(m for m in msgs if m)
    if "not authorized" in err:
        return "RESTRICTED"
    if code == 404 or "No status found" in err or "does not exist" in err or "not found" in err.lower():
        return "NOT_FOUND"
    if code != 200:
        return f"HTTP_{code}"
    return f"ERROR: {err[:80]}"

def detail(url: str) -> str:
    m = STATUS_RE.search(url)
    if not m:
        return "detail=bad_url"
    try:
        d = _get_json(f"{FX}{m.group(1)}/status/{m.group(2)}")
    except Exception:
        return "detail=unavailable"
    t = d.get("tweet") or {}
    if not t:
        return f"detail=fx_{d.get('code', '?')}"
    media = len(((t.get("media") or {}).get("all")) or [])
    return f"sensitive={t.get('possibly_sensitive')} media={media} views={t.get('views')}"


def main(argv):
    urls = []
    want_detail = False
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "-f":
            urls += [l.strip() for l in open(args.pop(0), encoding="utf-8") if l.strip()]
        elif a == "--detail":
            want_detail = True
        else:
            urls.append(a)
    if not urls:
        print(__doc__)
        return 2
    bad = 0
    for u in urls:
        status = check(u)
        bad += status != "OK"
        line = f"{status:12s} {u}"
        if want_detail:
            line += f"  {detail(u)}"
        print(line)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

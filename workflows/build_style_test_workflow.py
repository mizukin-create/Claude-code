#!/usr/bin/env python3
"""Generate a ComfyUI (UI-format) workflow that renders the SAME prompt/seed with 8 different style strings
(Anima / JANIMA), saves each image and a 4x2 contact sheet. Core nodes only (StringConcatenate,
PrimitiveStringMultiline, ImageStitch are all in comfy-core >= 0.3.30).
Run: python3 workflows/build_style_test_workflow.py  ->  workflows/anima_style_test.json
"""
import json

MODEL = "JANIMAAnima_v10.safetensors"
QUALITY = "masterpiece, highres, absurdres, newest, best quality, score_7, safe"
BODY = ("1girl, solo, upper body, looking at viewer, light smile, closed mouth, long hair, grey hair, blunt bangs, "
        "sidelocks, purple eyes, school uniform, sailor collar, classroom, window, afternoon, depth of field.\n"
        "A girl turns toward the viewer in a quiet classroom, soft afternoon light from the window on her hair.")
NEG = ("worst quality, low quality, lowres, score_1, score_2, score_3, blurry, jpeg artifacts, bad anatomy, "
       "missing fingers, watermark, artist name, sensitive, nsfw, explicit")
STYLES = [
    ("01_retro90s", "retro artstyle, 1990s (style), 90s anime style"),
    ("02_80s", "1980s (style), 80s anime style"),
    ("03_screenshot", "anime screenshot"),
    ("04_watercolor", "watercolor (medium), traditional media, watercolor painting style"),
    ("05_manga", "monochrome, greyscale, halftone, screentones, shoujo manga style"),
    ("06_pastel", "pastel colors, soft pastel style"),
    ("07_nouveau", "art nouveau, art nouveau style"),
    ("08_cinematic", "film grain, chromatic aberration, high contrast, cinematic composition"),
]
SEED = 123456789
NOTE = """# Anima / JANIMA 画風テスト（同一 seed・同一本文で 8 様式を横並び）

- 左の「品質タグ」「本文」「ネガ」は全枝で共通。各枝の「style」ノードの文字列だけが違う。
- 連結順は 品質 → 様式 → 本文（`prompts/anima_styles.md` の推奨位置）。区切りは ", "。
- KSampler は全枝 seed 固定（同じ値）。er_sde / simple / 28 steps / CFG 5（JANIMA カード推奨）。
  Anima-Aesthetic で試すときは QUALITY と NEG の score_* を消し、CFG 3〜4。Turbo は steps 8〜10 / CFG 1。
- 出力: output/Anima/style_test/<番号_様式名>_*.png と、4x2 の一覧 output/Anima/style_test/sheet_*.png。
- 様式候補は prompts/wildcards/anima_style.txt。style ノードの文字列を差し替えて再実行する。
- 必要ファイル: models/diffusion_models/JANIMAAnima_v10.safetensors（または anima-*.safetensors）、
  models/text_encoders/qwen_3_06b_base.safetensors、models/vae/qwen_image_vae.safetensors。
"""

nodes, links = {}, []

def node(nid, ntype, pos, size, widgets, inputs=(), winputs=(), outputs=(), title=None):
    """inputs: link-only inputs [(name,type)]; winputs: widget-backed inputs that will receive a link [(name,type)]."""
    ins = [{"name": nm, "type": t, "link": None} for nm, t in inputs]
    ins += [{"name": nm, "type": t, "widget": {"name": nm}, "link": None} for nm, t in winputs]
    n = {"id": nid, "type": ntype, "pos": list(pos), "size": list(size), "flags": {}, "order": nid, "mode": 0,
         "inputs": ins,
         "outputs": [{"name": nm, "type": t, "links": [], "slot_index": i} for i, (nm, t) in enumerate(outputs)],
         "properties": {"Node name for S&R": ntype}, "widgets_values": widgets}
    if title:
        n["title"] = title
    nodes[nid] = n

def link(src, src_slot, dst, dst_name):
    ltype = nodes[src]["outputs"][src_slot]["type"]
    dst_slot = next(i for i, x in enumerate(nodes[dst]["inputs"]) if x["name"] == dst_name)
    assert nodes[dst]["inputs"][dst_slot]["type"] == ltype, (src, dst, dst_name, ltype)
    lid = len(links) + 1
    links.append([lid, src, src_slot, dst, dst_slot, ltype])
    nodes[src]["outputs"][src_slot]["links"].append(lid)
    nodes[dst]["inputs"][dst_slot]["link"] = lid

# shared
node(1, "UNETLoader", (0, 0), (400, 82), [MODEL, "default"], outputs=[("MODEL", "MODEL")], title="JANIMA / Anima model")
node(2, "CLIPLoader", (0, 120), (400, 106), ["qwen_3_06b_base.safetensors", "stable_diffusion", "default"], outputs=[("CLIP", "CLIP")], title="Qwen3 text encoder")
node(3, "VAELoader", (0, 260), (400, 58), ["qwen_image_vae.safetensors"], outputs=[("VAE", "VAE")], title="Qwen-Image VAE")
node(4, "EmptyLatentImage", (0, 350), (400, 106), [832, 1216, 1], outputs=[("LATENT", "LATENT")], title="Latent 832x1216")
node(5, "PrimitiveStringMultiline", (0, 500), (400, 120), [QUALITY], outputs=[("STRING", "STRING")], title="品質タグ（共通）")
node(6, "PrimitiveStringMultiline", (0, 660), (400, 200), [BODY], outputs=[("STRING", "STRING")], title="本文（共通）")
node(7, "CLIPTextEncode", (0, 900), (400, 140), [NEG], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Negative（共通）")
node(8, "MarkdownNote", (0, 1080), (400, 420), [NOTE], title="README")
link(2, 0, 7, "clip")

nid = 10
decoded = []
for i, (name, style) in enumerate(STYLES):
    y = i * 330
    s, c1, c2, enc, ks, dec, sav = (nid + k for k in range(7))
    nid += 7
    node(s, "PrimitiveStringMultiline", (480, y), (300, 90), [style], outputs=[("STRING", "STRING")], title=f"style {name}")
    node(c1, "StringConcatenate", (820, y), (260, 100), ["", "", ", "], winputs=[("string_a", "STRING"), ("string_b", "STRING")],
         outputs=[("STRING", "STRING")], title="品質 + 様式")
    node(c2, "StringConcatenate", (820, y + 140), (260, 100), ["", "", ", "], winputs=[("string_a", "STRING"), ("string_b", "STRING")],
         outputs=[("STRING", "STRING")], title="+ 本文")
    node(enc, "CLIPTextEncode", (1120, y), (300, 120), [""], inputs=[("clip", "CLIP")], winputs=[("text", "STRING")],
         outputs=[("CONDITIONING", "CONDITIONING")], title=f"Positive {name}")
    node(ks, "KSampler", (1460, y), (300, 262), [SEED, "fixed", 28, 5.0, "er_sde", "simple", 1.0],
         inputs=[("model", "MODEL"), ("positive", "CONDITIONING"), ("negative", "CONDITIONING"), ("latent_image", "LATENT")],
         outputs=[("LATENT", "LATENT")], title=f"KSampler {name}")
    node(dec, "VAEDecode", (1800, y), (200, 46), [], inputs=[("samples", "LATENT"), ("vae", "VAE")], outputs=[("IMAGE", "IMAGE")])
    node(sav, "SaveImage", (2040, y), (260, 270), [f"Anima/style_test/{name}"], inputs=[("images", "IMAGE")], title=f"Save {name}")
    link(5, 0, c1, "string_a"); link(s, 0, c1, "string_b")
    link(c1, 0, c2, "string_a"); link(6, 0, c2, "string_b")
    link(2, 0, enc, "clip"); link(c2, 0, enc, "text")
    link(1, 0, ks, "model"); link(enc, 0, ks, "positive"); link(7, 0, ks, "negative"); link(4, 0, ks, "latent_image")
    link(ks, 0, dec, "samples"); link(3, 0, dec, "vae")
    link(dec, 0, sav, "images")
    decoded.append(dec)

def stitch(a, b, direction, pos):
    global nid
    st = nid; nid += 1
    node(st, "ImageStitch", pos, (280, 150), [direction, True, 8, "white"], inputs=[("image1", "IMAGE"), ("image2", "IMAGE")],
         outputs=[("IMAGE", "IMAGE")], title=f"stitch {direction}")
    link(a, 0, st, "image1"); link(b, 0, st, "image2")
    return st

# contact sheet: row1 = 1..4, row2 = 5..8, then rows stacked
r1 = stitch(decoded[0], decoded[1], "right", (2360, 0)); r1 = stitch(r1, decoded[2], "right", (2360, 180)); r1 = stitch(r1, decoded[3], "right", (2360, 360))
r2 = stitch(decoded[4], decoded[5], "right", (2360, 600)); r2 = stitch(r2, decoded[6], "right", (2360, 780)); r2 = stitch(r2, decoded[7], "right", (2360, 960))
sheet = stitch(r1, r2, "down", (2360, 1200))
sv = nid; nid += 1
node(sv, "SaveImage", (2360, 1400), (300, 300), ["Anima/style_test/sheet"], inputs=[("images", "IMAGE")], title="Save 4x2 sheet")
link(sheet, 0, sv, "images")

wf = {"last_node_id": max(nodes), "last_link_id": len(links), "nodes": [nodes[k] for k in sorted(nodes)], "links": links,
      "groups": [], "config": {}, "extra": {}, "version": 0.4}
with open(__file__.replace("build_style_test_workflow.py", "anima_style_test.json"), "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=1)
print("nodes", len(nodes), "links", len(links))

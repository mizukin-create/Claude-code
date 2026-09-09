#!/usr/bin/env python3
"""Generate a ComfyUI (UI-format) workflow JSON for Anima: txt2img -> 1.25x hires 2nd pass -> 2x ESRGAN final.
Core nodes only (no custom nodes). Run: python3 build_anima_workflow.py
"""
import json

POS = ("masterpiece, best quality, score_7, year 2025, newest, highres, safe, 1girl, solo, upper body, "
       "looking at viewer, long silver hair, blunt bangs, violet eyes, bright pupils, gentle smile, parted lips, blush, "
       "white blouse, sailor collar, rooftop, sunset, orange sky, backlighting, rim lighting, wind, floating hair, "
       "depth of field, anime coloring, clean lineart.\n"
       "A girl on a school rooftop at sunset looks back at the viewer, the low sun behind her outlining her hair "
       "with warm light while the city below fades into haze.")
NEG = ("worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, "
       "chromatic aberration, sensitive, nsfw, explicit")

NOTE = """# Anima txt2img + Hires（1.25x 2nd pass）+ 2x ESRGAN 仕上げ

必要ファイル（Hugging Face: circlestone-labs/Anima）
- models/diffusion_models/anima-base-v1.0.safetensors（Aesthetic v1.1 / Turbo v1.1 も同じ場所）
- models/text_encoders/qwen_3_06b_base.safetensors
- models/vae/qwen_image_vae.safetensors
- models/loras/anima-turbo-lora-v0.2.safetensors（任意。Turbo モード用）
- models/upscale_models/4x-AnimeSharp.pth（任意。無ければ RealESRGAN_x4plus_anime_6B.pth 等の 4x モデルに変更）

使い方
1. 1st pass: 832x1216 / 30 steps / CFG 4.5 / er_sde / simple（Base 用）。
   - Aesthetic v1.1 を使うときは、ポジ・ネガの score_* を全部消し、CFG 3.5〜4。
   - Turbo モード: 「Turbo LoRA」ノードのバイパス（紫）を解除し、steps 8〜10 / CFG 1。
2. 2nd pass: 4x ESRGAN → 0.3125 倍（合計 1.25x = 1040x1520）→ VAEEncode → denoise 0.32 で再サンプル。
   - 1.5x にしたいときは ImageScaleBy を 0.375（1248x1824）。それ以上はタイル化（Ultimate SD Upscale）。
   - 解像度は必ず 16 の倍数（32 の倍数が安全）。
3. final: 2nd pass 出力を 4x ESRGAN → 0.5 倍で 2x（2080x3040）。拡散処理なしの純粋拡大。
4. 顔・目の仕上げは Impact Pack の FaceDetailer を 2nd pass の後に挿入（crop を 32 の倍数に整列）。

出力は output/Anima/ 以下に 1st_pass / hires / final_2x の 3 種類を保存します。
"""

nodes = {}
links = []  # [id, from_node, from_slot, to_node, to_slot, type]

def node(nid, ntype, pos, size, widgets, inputs=(), outputs=(), mode=0, title=None):
    n = {
        "id": nid, "type": ntype, "pos": list(pos), "size": list(size), "flags": {}, "order": nid, "mode": mode,
        "inputs": [{"name": nm, "type": t, "link": None} for nm, t in inputs],
        "outputs": [{"name": nm, "type": t, "links": [], "slot_index": i} for i, (nm, t) in enumerate(outputs)],
        "properties": {"Node name for S&R": ntype},
        "widgets_values": widgets,
    }
    if title:
        n["title"] = title
    nodes[nid] = n

def link(src, src_slot, dst, dst_slot):
    ltype = nodes[src]["outputs"][src_slot]["type"]
    lid = len(links) + 1
    links.append([lid, src, src_slot, dst, dst_slot, ltype])
    nodes[src]["outputs"][src_slot]["links"].append(lid)
    assert nodes[dst]["inputs"][dst_slot]["type"] == ltype, (src, dst, ltype)
    nodes[dst]["inputs"][dst_slot]["link"] = lid

# --- loaders ---
node(1, "UNETLoader", (0, 0), (380, 82), ["anima-base-v1.0.safetensors", "default"], outputs=[("MODEL", "MODEL")], title="Anima model")
node(17, "LoraLoaderModelOnly", (0, 130), (380, 82), ["anima-turbo-lora-v0.2.safetensors", 1.0],
     inputs=[("model", "MODEL")], outputs=[("MODEL", "MODEL")], mode=4, title="Turbo LoRA (bypassed by default)")
node(2, "CLIPLoader", (0, 260), (380, 106), ["qwen_3_06b_base.safetensors", "stable_diffusion", "default"], outputs=[("CLIP", "CLIP")], title="Qwen3 text encoder")
node(3, "VAELoader", (0, 410), (380, 58), ["qwen_image_vae.safetensors"], outputs=[("VAE", "VAE")], title="Qwen-Image VAE")
node(10, "UpscaleModelLoader", (0, 510), (380, 58), ["4x-AnimeSharp.pth"], outputs=[("UPSCALE_MODEL", "UPSCALE_MODEL")], title="4x upscale model")
node(18, "MarkdownNote", (0, 620), (380, 520), [NOTE], title="README")

# --- conditioning ---
node(4, "CLIPTextEncode", (450, 0), (420, 220), [POS], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Positive")
node(5, "CLIPTextEncode", (450, 270), (420, 140), [NEG], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Negative")
node(6, "EmptyLatentImage", (450, 460), (320, 106), [832, 1216, 1], outputs=[("LATENT", "LATENT")], title="Latent 832x1216 (16の倍数)")

# --- 1st pass ---
node(7, "KSampler", (920, 0), (320, 262), [0, "randomize", 30, 4.5, "er_sde", "simple", 1.0],
     inputs=[("model", "MODEL"), ("positive", "CONDITIONING"), ("negative", "CONDITIONING"), ("latent_image", "LATENT")],
     outputs=[("LATENT", "LATENT")], title="KSampler 1st pass")
node(8, "VAEDecode", (1290, 0), (210, 46), [], inputs=[("samples", "LATENT"), ("vae", "VAE")], outputs=[("IMAGE", "IMAGE")])
node(9, "SaveImage", (1290, 100), (320, 300), ["Anima/1st_pass"], inputs=[("images", "IMAGE")], title="Save 1st pass")

# --- hires 2nd pass ---
node(11, "ImageUpscaleWithModel", (1660, 0), (260, 46), [], inputs=[("upscale_model", "UPSCALE_MODEL"), ("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="4x ESRGAN")
node(12, "ImageScaleBy", (1660, 100), (260, 82), ["lanczos", 0.3125], inputs=[("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="x0.3125 (=1.25x total)")
node(13, "VAEEncode", (1660, 230), (210, 46), [], inputs=[("pixels", "IMAGE"), ("vae", "VAE")], outputs=[("LATENT", "LATENT")])
node(14, "KSampler", (1960, 0), (320, 262), [0, "randomize", 20, 4.0, "er_sde", "simple", 0.32],
     inputs=[("model", "MODEL"), ("positive", "CONDITIONING"), ("negative", "CONDITIONING"), ("latent_image", "LATENT")],
     outputs=[("LATENT", "LATENT")], title="KSampler 2nd pass (denoise 0.28-0.35)")
node(15, "VAEDecode", (2330, 0), (210, 46), [], inputs=[("samples", "LATENT"), ("vae", "VAE")], outputs=[("IMAGE", "IMAGE")])
node(16, "SaveImage", (2330, 100), (320, 300), ["Anima/hires"], inputs=[("images", "IMAGE")], title="Save hires")

# --- final 2x (no diffusion) ---
node(19, "ImageUpscaleWithModel", (2700, 0), (260, 46), [], inputs=[("upscale_model", "UPSCALE_MODEL"), ("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="4x ESRGAN (final)")
node(20, "ImageScaleBy", (2700, 100), (260, 82), ["lanczos", 0.5], inputs=[("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="x0.5 (=2x total)")
node(21, "SaveImage", (2700, 230), (320, 300), ["Anima/final_2x"], inputs=[("images", "IMAGE")], title="Save final 2x")

# --- wiring ---
link(1, 0, 17, 0)
link(17, 0, 7, 0)
link(17, 0, 14, 0)
link(2, 0, 4, 0)
link(2, 0, 5, 0)
link(4, 0, 7, 1)
link(5, 0, 7, 2)
link(6, 0, 7, 3)
link(7, 0, 8, 0)
link(3, 0, 8, 1)
link(8, 0, 9, 0)
link(10, 0, 11, 0)
link(8, 0, 11, 1)
link(11, 0, 12, 0)
link(12, 0, 13, 0)
link(3, 0, 13, 1)
link(4, 0, 14, 1)
link(5, 0, 14, 2)
link(13, 0, 14, 3)
link(14, 0, 15, 0)
link(3, 0, 15, 1)
link(15, 0, 16, 0)
link(10, 0, 19, 0)
link(15, 0, 19, 1)
link(19, 0, 20, 0)
link(20, 0, 21, 0)

# sanity: every non-widget input is connected
for n in nodes.values():
    for inp in n["inputs"]:
        assert inp["link"] is not None, (n["id"], inp["name"])

wf = {
    "last_node_id": max(nodes),
    "last_link_id": len(links),
    "nodes": [nodes[k] for k in sorted(nodes)],
    "links": links,
    "groups": [
        {"title": "Loaders", "bounding": [-20, -60, 420, 1220], "color": "#3f789e", "font_size": 24},
        {"title": "1st pass (832x1216)", "bounding": [430, -60, 1200, 660], "color": "#a1309b", "font_size": 24},
        {"title": "Hires 2nd pass (1.25x, denoise 0.32)", "bounding": [1640, -60, 1030, 420], "color": "#b58b2a", "font_size": 24},
        {"title": "Final 2x (ESRGAN only)", "bounding": [2680, -60, 360, 560], "color": "#3f9e5b", "font_size": 24},
    ],
    "config": {},
    "extra": {"ds": {"scale": 0.5, "offset": [50, 100]}},
    "version": 0.4,
}
with open("anima_t2i_hires.json", "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)
print("nodes:", len(nodes), "links:", len(links))

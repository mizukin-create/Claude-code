#!/usr/bin/env python3
"""Generate a ComfyUI (UI-format) workflow JSON for Pipeline C: Anima (composition) -> Illustrious (paint/refine).

Core nodes only (no custom nodes):
  stage 1  Anima Aesthetic v1.1 txt2img 832x1216 (er_sde/simple, 30 steps, CFG 4)
  bridge   VAEDecode (Qwen-Image VAE) -> 4x ESRGAN -> ImageScale 1024x1536 (pixel hand-off; latent spaces differ)
  stage 2  Illustrious (WAI v17) img2img denoise 0.45 with ControlNet union-promax (tile) strength 0.6, end 0.7
  final    4x ESRGAN -> x0.5 (= 2x, 2048x3072), no diffusion
Optional (marked in README note): FaceDetailer (Impact Pack), Color Match (KJNodes), Ultimate SD Upscale.

Run: python3 build_two_stage_workflow.py  -> anima_to_illustrious_2stage.json
"""
import json

ANIMA_POS = ("masterpiece, best quality, year 2025, newest, highres, safe, 1girl, solo, long hair, grey hair, blunt bangs, "
             "sidelocks, purple eyes, bright pupils, tareme, mole under eye, star hair ornament, black sailor collar, white shirt, "
             "pleated skirt, black thighhighs, loafers, upper body, from side, looking at viewer, light smile, half-closed eyes, "
             "blush, head tilt, rooftop, fence, sunset, backlighting, wind, floating hair, depth of field, anime coloring.\n"
             "She leans on the rooftop fence at sunset and glances back at the viewer with a faint smile, the low sun outlining "
             "her grey hair with warm light. Her skirt and hair drift in the wind while the city below fades into haze.")
ANIMA_NEG = ("worst quality, low quality, artist name, blurry, jpeg artifacts, chromatic aberration, sensitive, nsfw, explicit")

ILL_POS = ("1girl, solo, long hair, grey hair, blunt bangs, sidelocks, purple eyes, bright pupils, tareme, mole under eye, "
           "star hair ornament, black sailor collar, white shirt, pleated skirt, black thighhighs, loafers, upper body, from side, "
           "looking at viewer, light smile, half-closed eyes, blush, head tilt, rooftop, sunset, backlighting, wind, floating hair, "
           "depth of field, anime screencap\nBREAK masterpiece, best quality, very aesthetic, absurdres, newest, general")
ILL_NEG = "worst quality, low quality, lowres, bad anatomy, bad hands, jpeg artifacts, signature, watermark, nsfw"

NOTE = """# Anima → Illustrious 二段構成（パイプライン C）

流れ
1. Stage 1: Anima Aesthetic v1.1 で構図・複数人・カメラを確定（832x1216 / 30 steps / CFG 4 / er_sde / simple）。
   - Turbo v1.1 で seed 探索するときは UNETLoader を anima-turbo-v1.1 に替え、steps 8〜10 / CFG 1。
   - Base v1.0 を使うときはポジに score_7、ネガに score_1, score_2, score_3 を足す。
2. Bridge: VAEDecode（Qwen-Image VAE）→ 4x ESRGAN → 1024x1536 に整形。latent は受け渡せない（16ch と 4ch で空間が違う）ので必ず pixel で渡す。
3. Stage 2: WAI v17（Illustrious）で img2img。denoise 0.45（構図維持 0.35〜0.45、塗り替え 0.5〜0.6）。
   - ControlNet: xinsir controlnet-union-sdxl-1.0 promax を tile モードで strength 0.6 / end 0.7。構図を守りつつ塗りを Illustrious に寄せる。
   - ControlNet を使わないときは ControlNetApplyAdvanced をバイパスし、KSampler の positive/negative を CLIPTextEncode に直結。
   - プロンプトは Illustrious 用（Danbooru タグ + BREAK 品質タグ）。Anima 側の自然文はそのまま使わない。
4. Final: 4x ESRGAN → x0.5 で 2x（2048x3072）。拡散処理なし。

任意（カスタムノード）
- FaceDetailer（Impact Pack）を Stage 2 の VAEDecode 直後に: WAI v17、denoise 0.35、guide_size 512。
- Color Match（KJNodes）: 参照 = Stage 1 出力（Anima のパレットに寄せる）または Stage 2 出力。
- Ultimate SD Upscale: 2x 以上にするとき（tile 1024、denoise 0.25、ControlNet tile 併用時は 0.4）。

必要ファイル
- models/diffusion_models/anima-aesthetic-v1.1.safetensors, models/text_encoders/qwen_3_06b_base.safetensors, models/vae/qwen_image_vae.safetensors
- models/checkpoints/waiIllustriousSDXL_v170.safetensors（ファイル名は環境に合わせて変更）
- models/controlnet/controlnet-union-sdxl-1.0-promax.safetensors（xinsir）
- models/upscale_models/4x-AnimeSharp.pth

出力は output/TwoStage/ 以下に stage1_anima / stage2_illustrious / final_2x の 3 種類を保存します。
"""

nodes = {}
links = []


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


# ---------------- Stage 1: Anima ----------------
node(1, "UNETLoader", (0, 0), (380, 82), ["anima-aesthetic-v1.1.safetensors", "default"], outputs=[("MODEL", "MODEL")], title="Anima model (Aesthetic v1.1)")
node(2, "CLIPLoader", (0, 130), (380, 106), ["qwen_3_06b_base.safetensors", "stable_diffusion", "default"], outputs=[("CLIP", "CLIP")], title="Qwen3 text encoder")
node(3, "VAELoader", (0, 280), (380, 58), ["qwen_image_vae.safetensors"], outputs=[("VAE", "VAE")], title="Qwen-Image VAE")
node(4, "CLIPTextEncode", (450, 0), (420, 220), [ANIMA_POS], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Anima positive (tags + 2 sentences)")
node(5, "CLIPTextEncode", (450, 270), (420, 120), [ANIMA_NEG], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Anima negative")
node(6, "EmptyLatentImage", (450, 440), (320, 106), [832, 1216, 1], outputs=[("LATENT", "LATENT")], title="Latent 832x1216")
node(7, "KSampler", (920, 0), (320, 262), [0, "randomize", 30, 4.0, "er_sde", "simple", 1.0],
     inputs=[("model", "MODEL"), ("positive", "CONDITIONING"), ("negative", "CONDITIONING"), ("latent_image", "LATENT")],
     outputs=[("LATENT", "LATENT")], title="Stage 1 KSampler (Anima)")
node(8, "VAEDecode", (1290, 0), (210, 46), [], inputs=[("samples", "LATENT"), ("vae", "VAE")], outputs=[("IMAGE", "IMAGE")], title="VAEDecode (Qwen VAE)")
node(9, "SaveImage", (1290, 100), (320, 300), ["TwoStage/stage1_anima"], inputs=[("images", "IMAGE")], title="Save stage 1")
node(30, "MarkdownNote", (0, 400), (380, 640), [NOTE], title="README")

# ---------------- Bridge ----------------
node(10, "UpscaleModelLoader", (1660, 360), (300, 58), ["4x-AnimeSharp.pth"], outputs=[("UPSCALE_MODEL", "UPSCALE_MODEL")], title="4x upscale model")
node(11, "ImageUpscaleWithModel", (1660, 0), (260, 46), [], inputs=[("upscale_model", "UPSCALE_MODEL"), ("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="4x ESRGAN (bridge)")
node(12, "ImageScale", (1660, 100), (300, 130), ["lanczos", 1024, 1536, "center"], inputs=[("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="Resize 1024x1536 (pixel hand-off)")

# ---------------- Stage 2: Illustrious ----------------
node(13, "CheckpointLoaderSimple", (2020, 360), (380, 98), ["waiIllustriousSDXL_v170.safetensors"], outputs=[("MODEL", "MODEL"), ("CLIP", "CLIP"), ("VAE", "VAE")], title="Illustrious checkpoint (WAI v17)")
node(14, "CLIPTextEncode", (2020, 0), (420, 200), [ILL_POS], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Illustrious positive (tags, BREAK quality)")
node(15, "CLIPTextEncode", (2020, 240), (420, 100), [ILL_NEG], inputs=[("clip", "CLIP")], outputs=[("CONDITIONING", "CONDITIONING")], title="Illustrious negative")
node(16, "ControlNetLoader", (2020, 500), (380, 58), ["controlnet-union-sdxl-1.0-promax.safetensors"], outputs=[("CONTROL_NET", "CONTROL_NET")], title="ControlNet union promax (xinsir)")
node(17, "SetUnionControlNetType", (2020, 600), (380, 58), ["tile"], inputs=[("control_net", "CONTROL_NET")], outputs=[("CONTROL_NET", "CONTROL_NET")], title="Union type = tile")
node(18, "ControlNetApplyAdvanced", (2500, 0), (320, 190), [0.6, 0.0, 0.7],
     inputs=[("positive", "CONDITIONING"), ("negative", "CONDITIONING"), ("control_net", "CONTROL_NET"), ("image", "IMAGE")],
     outputs=[("positive", "CONDITIONING"), ("negative", "CONDITIONING")], title="ControlNet tile 0.6 (end 0.7)")
node(19, "VAEEncode", (2500, 240), (210, 46), [], inputs=[("pixels", "IMAGE"), ("vae", "VAE")], outputs=[("LATENT", "LATENT")], title="VAEEncode (SDXL VAE)")
node(20, "KSampler", (2880, 0), (320, 262), [0, "randomize", 30, 5.0, "euler_ancestral", "normal", 0.45],
     inputs=[("model", "MODEL"), ("positive", "CONDITIONING"), ("negative", "CONDITIONING"), ("latent_image", "LATENT")],
     outputs=[("LATENT", "LATENT")], title="Stage 2 KSampler img2img (denoise 0.45)")
node(21, "VAEDecode", (3250, 0), (210, 46), [], inputs=[("samples", "LATENT"), ("vae", "VAE")], outputs=[("IMAGE", "IMAGE")], title="VAEDecode (SDXL VAE)")
node(22, "SaveImage", (3250, 100), (320, 300), ["TwoStage/stage2_illustrious"], inputs=[("images", "IMAGE")], title="Save stage 2")

# ---------------- Final 2x ----------------
node(23, "ImageUpscaleWithModel", (3620, 0), (260, 46), [], inputs=[("upscale_model", "UPSCALE_MODEL"), ("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="4x ESRGAN (final)")
node(24, "ImageScaleBy", (3620, 100), (260, 82), ["lanczos", 0.5], inputs=[("image", "IMAGE")], outputs=[("IMAGE", "IMAGE")], title="x0.5 (=2x total, 2048x3072)")
node(25, "SaveImage", (3620, 230), (320, 300), ["TwoStage/final_2x"], inputs=[("images", "IMAGE")], title="Save final 2x")

# ---------------- wiring ----------------
link(1, 0, 7, 0)
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
link(13, 1, 14, 0)
link(13, 1, 15, 0)
link(16, 0, 17, 0)
link(14, 0, 18, 0)
link(15, 0, 18, 1)
link(17, 0, 18, 2)
link(12, 0, 18, 3)
link(12, 0, 19, 0)
link(13, 2, 19, 1)
link(13, 0, 20, 0)
link(18, 0, 20, 1)
link(18, 1, 20, 2)
link(19, 0, 20, 3)
link(20, 0, 21, 0)
link(13, 2, 21, 1)
link(21, 0, 22, 0)
link(10, 0, 23, 0)
link(21, 0, 23, 1)
link(23, 0, 24, 0)
link(24, 0, 25, 0)

for n in nodes.values():
    for inp in n["inputs"]:
        assert inp["link"] is not None, (n["id"], inp["name"])

wf = {
    "last_node_id": max(nodes),
    "last_link_id": len(links),
    "nodes": [nodes[k] for k in sorted(nodes)],
    "links": links,
    "groups": [
        {"title": "Stage 1: Anima (composition)", "bounding": [-20, -60, 1640, 1120], "color": "#a1309b", "font_size": 24},
        {"title": "Bridge: pixel hand-off 1024x1536", "bounding": [1640, -60, 360, 500], "color": "#b58b2a", "font_size": 24},
        {"title": "Stage 2: Illustrious img2img + ControlNet tile", "bounding": [2000, -60, 1590, 740], "color": "#3f789e", "font_size": 24},
        {"title": "Final 2x (ESRGAN only)", "bounding": [3600, -60, 360, 560], "color": "#3f9e5b", "font_size": 24},
    ],
    "config": {},
    "extra": {"ds": {"scale": 0.4, "offset": [50, 100]}},
    "version": 0.4,
}
with open("anima_to_illustrious_2stage.json", "w", encoding="utf-8") as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)
print("nodes:", len(nodes), "links:", len(links))

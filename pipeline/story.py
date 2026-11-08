#!/usr/bin/env python3
"""Fin Ticks story card renderer.

Usage: python3 pipeline/story.py POST_FOLDER [kicker]
Reads POST_FOLDER/slide-1.jpg and writes POST_FOLDER/story.jpg (1080x1920, 9:16).
Key content sits inside Instagram's safe zone (≈250px clear at top and bottom).
"""
import base64, os, sys, pathlib, html
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from render import font_css, PULSE_SVG, HANDLE  # noqa: E402

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px}
body{font-family:'Montserrat',sans-serif;color:#F4F7FB;overflow:hidden;
background:radial-gradient(1100px 900px at 80% 0%,#173A6B 0%,rgba(23,58,107,0) 60%),
linear-gradient(180deg,#0B2140 0%,#071730 100%)}
.wrap{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;padding-top:250px}
.mark{font-weight:600;font-size:64px;letter-spacing:-2px;line-height:1}
.mark .t{color:#F15A22}
.pill{margin-top:40px;background:#F15A22;color:#fff;font-weight:800;font-size:34px;letter-spacing:6px;
padding:18px 40px;border-radius:999px;text-transform:uppercase}
.card{margin-top:44px;width:840px;height:1050px;border-radius:36px;overflow:hidden;
box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 4px rgba(241,90,34,.55)}
.card img{width:100%;height:100%;display:block}
.cta{margin-top:44px;font-weight:700;font-size:34px;color:#DCE6F2;text-align:center;line-height:1.4}
.cta b{color:#fff}
.pulse{position:absolute;bottom:150px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:16px;
font-weight:700;font-size:22px;letter-spacing:6px;color:#A9BBD3}
"""


def main(folder, kicker="New post"):
    folder = pathlib.Path(folder)
    img = base64.b64encode((folder / "slide-1.jpg").read_bytes()).decode()
    page = (f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head><body>'
            f'<div class="wrap"><div class="mark">fin<span class="t">ticks</span></div>'
            f'<div class="pill">{html.escape(kicker)}</div>'
            f'<div class="card"><img src="data:image/jpeg;base64,{img}"></div>'
            f'<div class="cta">Swipe through the full story<br>on <b>{HANDLE}</b></div></div>'
            f'<div class="pulse">{PULSE_SVG}YOUR DAILY MARKET PULSE</div></body></html>')
    with sync_playwright() as p:
        exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else p.chromium.launch(args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.set_content(page, wait_until="load")
        pg.evaluate("document.fonts.ready")
        png = folder / "story.png"
        pg.screenshot(path=str(png))
        b.close()
    from PIL import Image
    Image.open(png).convert("RGB").save(folder / "story.jpg", quality=92)
    png.unlink()
    print(folder / "story.jpg")


if __name__ == "__main__":
    main(sys.argv[1], *(sys.argv[2:3]))

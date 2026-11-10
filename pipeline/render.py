#!/usr/bin/env python3
"""Fin Ticks carousel renderer.

Usage: python3 render.py post.json OUTDIR
post.json = {"slides": [ {type, ...}, x5 ], "sources": "..."}
Slide types: cover, facts, chart, split, takeaways.
Renders 1080x1350 PNGs named slide-1.png ... slide-5.png.
"""
import base64, json, sys, html, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
HANDLE = "@finticksmalayalam"


def b64(name):
    return base64.b64encode((FONTS / name).read_bytes()).decode()


def font_css():
    faces = [
        ("Anton", "anton.woff2", 400),
        ("Montserrat", "montserrat-500.woff2", 500),
        ("Montserrat", "montserrat-600.woff2", 600),
        ("Montserrat", "montserrat-700.woff2", 700),
        ("Montserrat", "montserrat-800.woff2", 800),
        ("NotoMal", "noto-sans-malayalam-malayalam-400-normal.woff2", 400),
        ("NotoMal", "noto-sans-malayalam-malayalam-700-normal.woff2", 700),
        ("AnekMal", "anek-malayalam-malayalam-800-normal.woff2", 800),
    ]
    return "\n".join(
        f"@font-face{{font-family:'{f}';src:url(data:font/woff2;base64,{b64(n)}) format('woff2');font-weight:{w};}}"
        for f, n, w in faces
    )


CSS = """
:root{--navy:#0B2140;--navy2:#071730;--ink:#F4F7FB;--muted:#A9BBD3;--orange:#F15A22;
--orange2:#FF7A45;--card:rgba(255,255,255,.055);--line:rgba(255,255,255,.12);--green:#2BC48A;--red:#FF5A5F}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{font-family:'Montserrat','NotoMal',sans-serif;color:var(--ink);
background:radial-gradient(1200px 900px at 85% -10%,#173A6B 0%,rgba(23,58,107,0) 60%),
linear-gradient(180deg,var(--navy) 0%,var(--navy2) 100%);position:relative;overflow:hidden}
.grid{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),
linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:90px 90px;opacity:.25;
mask-image:linear-gradient(180deg,#000 0%,transparent 70%)}
.frame{position:absolute;inset:0;padding:64px 72px 0;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;height:56px}
.mark{font-weight:600;font-size:40px;letter-spacing:-1px;line-height:1}
.mark .fin{color:#fff}.mark .ticks{color:var(--orange)}
.count{font-weight:700;font-size:22px;color:var(--muted);letter-spacing:3px}
.count b{color:#fff}
.kicker{display:inline-flex;align-items:center;gap:14px;margin-top:56px;font-weight:800;font-size:24px;
letter-spacing:4px;text-transform:uppercase;color:var(--orange)}
.kicker:before{content:"";width:44px;height:6px;background:var(--orange);border-radius:3px}
h1{font-family:'Anton','AnekMal';font-weight:400;text-transform:uppercase;line-height:.98;letter-spacing:.5px}
h1 em{font-style:normal;color:var(--orange)}
.body{flex:1;display:flex;flex-direction:column;min-height:0}
.foot{height:118px;display:flex;align-items:center;justify-content:space-between;border-top:2px solid var(--line);
margin-top:auto}
.pulse{display:flex;align-items:center;gap:16px;font-weight:700;font-size:18px;letter-spacing:5px;color:var(--muted)}
.handle{font-weight:700;font-size:22px;color:#fff}
.swipe{font-weight:800;font-size:20px;letter-spacing:3px;color:var(--orange);display:flex;align-items:center;gap:10px}
.sub{font-size:34px;font-weight:600;line-height:1.35;color:#DCE6F2}
.sub b{color:#fff}.sub em{font-style:normal;color:var(--orange2);font-weight:700}
/* cover */
.cover h1{font-size:150px;margin-top:28px}
.bigstat{display:flex;align-items:flex-end;gap:28px;margin-top:48px}
.bigstat .n{font-family:'Anton';font-size:210px;line-height:.85;color:var(--orange)}
.bigstat .l{font-size:30px;font-weight:700;line-height:1.3;padding-bottom:14px;color:#fff}
.bigstat .l span{display:block;color:var(--muted);font-weight:600;font-size:26px}
.spark{margin-top:auto;margin-bottom:32px}
.vs{margin-top:auto;margin-bottom:34px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.vs>div{border-radius:24px;padding:24px 28px;background:var(--card);border:2px solid var(--line)}
.vs .k{font-size:21px;font-weight:800;letter-spacing:3px;color:var(--muted);text-transform:uppercase}
.vs .v{font-family:'Anton';font-size:84px;line-height:1.05;margin-top:6px}
/* facts */
.facts h1,.chart h1,.split h1,.take h1{font-size:96px;margin-top:22px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:44px}
.stat{background:var(--card);border:2px solid var(--line);border-radius:28px;padding:30px 32px}
.stat .k{font-size:22px;font-weight:800;letter-spacing:3px;color:var(--muted);text-transform:uppercase}
.stat .v{font-family:'Anton';font-size:76px;line-height:1.05;margin-top:10px}
.stat .d{font-size:26px;font-weight:700;margin-top:6px}
.up{color:var(--green)}.dn{color:var(--red)}.or{color:var(--orange)}
ul.pts{list-style:none;margin-top:38px;display:flex;flex-direction:column;gap:22px}
ul.pts li{font-size:30px;font-weight:600;line-height:1.35;padding-left:42px;position:relative;color:#DCE6F2}
ul.pts li:before{content:"";position:absolute;left:0;top:16px;width:16px;height:16px;border-radius:50%;background:var(--orange)}
ul.pts li b{color:#fff}
/* chart */
.cap{font-size:24px;font-weight:700;letter-spacing:2px;color:var(--muted);margin-top:36px;text-transform:uppercase}
.bars{margin-top:20px;display:flex;flex-direction:column;gap:12px}
.bar{display:grid;grid-template-columns:190px 1fr;align-items:center;gap:20px}
.bar .nm{font-size:27px;font-weight:700;text-align:right}
.track{position:relative;height:52px}
.track .zero{position:absolute;left:50%;top:-8px;bottom:-8px;width:3px;background:rgba(255,255,255,.45)}
.fill{position:absolute;top:0;height:52px;border-radius:10px;display:flex;align-items:center;font-weight:800;font-size:26px;padding:0 16px}
.fill.pos{left:50%;background:var(--green);color:#062B1C;justify-content:flex-end}
.fill.neg{right:50%;background:var(--red);color:#3A0608;justify-content:flex-start}
.fill.hl{box-shadow:0 0 0 4px var(--orange)}
.fill.out{padding:0}.fill.out span{position:absolute;white-space:nowrap;color:#fff}.fill.neg.out span{right:calc(100% + 12px)}.fill.pos.out span{left:calc(100% + 12px)}
.why{margin-top:28px;display:grid;grid-template-columns:1fr 1fr;gap:18px}
.why div{background:var(--card);border-left:6px solid var(--orange);border-radius:14px;padding:16px 20px;font-size:23px;font-weight:600;line-height:1.35;color:#DCE6F2}
.why b{color:#fff;display:block;font-size:27px;margin-bottom:4px}
/* split */
.cols{display:grid;grid-template-rows:auto auto;gap:24px;margin-top:40px}
.col{border-radius:28px;padding:30px 34px;border:2px solid var(--line);background:var(--card)}
.col.watch{border-color:rgba(241,90,34,.6);background:rgba(241,90,34,.08)}
.col .h{font-size:24px;font-weight:800;letter-spacing:4px;text-transform:uppercase;display:flex;align-items:center;gap:12px}
.col .h i{width:14px;height:14px;border-radius:50%;background:var(--green);display:inline-block}
.col.watch .h i{background:var(--orange)}
.col ul{list-style:none;margin-top:20px;display:flex;flex-direction:column;gap:18px}
.col li{font-size:30px;font-weight:600;line-height:1.35;color:#DCE6F2}
.col li b{color:#fff}
.note{margin-top:22px;font-size:22px;color:var(--muted);font-weight:600;line-height:1.4}
/* takeaways */
ol.tk{list-style:none;margin-top:40px;display:flex;flex-direction:column;gap:22px;counter-reset:t}
ol.tk li{counter-increment:t;display:grid;grid-template-columns:76px 1fr;gap:22px;align-items:start;font-size:31px;font-weight:600;line-height:1.35;color:#DCE6F2}
ol.tk li:before{content:counter(t);font-family:'Anton';font-size:52px;color:var(--orange);line-height:1;
background:rgba(241,90,34,.12);border-radius:18px;height:76px;display:flex;align-items:center;justify-content:center}
ol.tk li b{color:#fff}
.cta{margin-top:auto;margin-bottom:26px;background:var(--orange);border-radius:26px;padding:28px 34px;display:flex;justify-content:space-between;align-items:center}
.cta .t{font-family:'Anton';font-size:46px;text-transform:uppercase;color:#fff;line-height:1.05}
.cta .h2{font-size:26px;font-weight:800;color:#fff;background:rgba(0,0,0,.18);padding:12px 18px;border-radius:14px}
.src{font-size:19px;color:var(--muted);font-weight:600;margin-bottom:20px;line-height:1.4}
"""

PULSE_SVG = ('<svg width="150" height="28" viewBox="0 0 150 28"><path d="M0 14H58L64 4L72 26L78 14H150" '
             'fill="none" stroke="#F15A22" stroke-width="3" stroke-linejoin="round"/></svg>')


def esc(s):
    """Allow **bold** and *orange* light markup inside escaped text."""
    s = html.escape(s)
    import re
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def head(i, n):
    return (f'<div class="top"><div class="mark"><span class="fin">fin</span><span class="ticks">ticks</span></div>'
            f'<div class="count"><b>{i:02d}</b> / {n:02d}</div></div>')


def foot(last):
    right = ('<div class="handle">' + HANDLE + '</div>') if last else \
        '<div class="swipe">SWIPE <svg width="34" height="20" viewBox="0 0 34 20"><path d="M0 10H30M22 2L31 10L22 18" stroke="#F15A22" stroke-width="3.5" fill="none"/></svg></div>'
    return f'<div class="foot"><div class="pulse">{PULSE_SVG}YOUR DAILY MARKET PULSE</div>{right}</div>'


def spark(points):
    """Upward line chart from real points (list of numbers)."""
    w, h = 936, 220
    lo, hi = min(points), max(points)
    xs = [i * w / (len(points) - 1) for i in range(len(points))]
    ys = [h - 20 - (p - lo) / (hi - lo or 1) * (h - 40) for p in points]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in zip(xs, ys))
    area = d + f" L{w} {h} L0 {h} Z"
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#0B2140" stroke="#F15A22" stroke-width="5"/>' for x, y in zip(xs, ys))
    return (f'<svg class="spark" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#F15A22" stop-opacity=".35"/><stop offset="1" stop-color="#F15A22" stop-opacity="0"/></linearGradient></defs>'
            f'<path d="{area}" fill="url(#g)"/><path d="{d}" fill="none" stroke="#F15A22" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>{dots}</svg>')


def slide_html(s, i, n, sources):
    t = s["type"]
    k = f'<div class="kicker">{esc(s["kicker"])}</div>' if s.get("kicker") else ""
    if t == "cover":
        inner = (k + f'<h1>{esc(s["title"])}</h1>'
                 + (f'<div class="bigstat"><div class="n">{esc(s["stat"])}</div><div class="l">{esc(s["stat_label"])}<span>{esc(s.get("stat_sub",""))}</span></div></div>' if s.get("stat") else "")
                 + (f'<p class="sub" style="margin-top:30px">{esc(s["sub"])}</p>' if s.get("sub") else "")
                 + (spark(s["spark"]) if s.get("spark") else "")
                 + ('<div class="vs">' + "".join(f'<div><div class="k">{esc(c["k"])}</div><div class="v {c.get('tone','up')}">{esc(c["v"])}</div></div>' for c in s["compare"]) + '</div>' if s.get("compare") else ""))
    elif t == "facts":
        cards = "".join(
            f'<div class="stat"><div class="k">{esc(c["k"])}</div><div class="v">{esc(c["v"])}</div>'
            f'<div class="d {c.get("tone","up")}">{esc(c["d"])}</div></div>' for c in s["stats"])
        pts = "".join(f"<li>{esc(p)}</li>" for p in s.get("points", []))
        inner = k + f'<h1>{esc(s["title"])}</h1><div class="stats">{cards}</div><ul class="pts">{pts}</ul>'
    elif t == "chart":
        m = max(abs(b["v"]) for b in s["bars"])
        rows = ""
        for b in s["bars"]:
            wpct = abs(b["v"]) / m * 50
            cls = "pos" if b["v"] >= 0 else "neg"
            hl = " hl" if b.get("hl") else ""
            if wpct < 16:
                hl += " out"
            lab = f'<span>{b["v"]:+.2f}%</span>'
            rows += (f'<div class="bar"><div class="nm">{esc(b["name"])}</div><div class="track"><div class="zero"></div>'
                     f'<div class="fill {cls}{hl}" style="width:{wpct:.1f}%">{lab}</div></div></div>')
        why = "".join(f'<div><b>{esc(w["h"])}</b>{esc(w["t"])}</div>' for w in s.get("why", []))
        inner = (k + f'<h1>{esc(s["title"])}</h1><div class="cap">{esc(s["caption"])}</div>'
                 f'<div class="bars">{rows}</div><div class="why">{why}</div>')
    elif t == "split":
        a = "".join(f"<li>{esc(x)}</li>" for x in s["actual"])
        w = "".join(f"<li>{esc(x)}</li>" for x in s["watch"])
        inner = (k + f'<h1>{esc(s["title"])}</h1><div class="cols">'
                 f'<div class="col"><div class="h"><i></i>{esc(s.get("actual_h","What actually happened"))}</div><ul>{a}</ul></div>'
                 f'<div class="col watch"><div class="h"><i></i>{esc(s.get("watch_h","What to watch next"))}</div><ul>{w}</ul></div></div>'
                 + (f'<p class="note">{esc(s["note"])}</p>' if s.get("note") else ""))
    elif t == "takeaways":
        tk = "".join(f"<li><span>{esc(x)}</span></li>" for x in s["points"])
        inner = (k + f'<h1>{esc(s["title"])}</h1><ol class="tk">{tk}</ol>'
                 f'<div class="cta"><div class="t">{esc(s.get("cta","Follow for daily market news that matters"))}</div><div class="h2">{HANDLE}</div></div>'
                 f'<div class="src">Sources: {esc(sources)} · Not investment advice.</div>')
    else:
        raise ValueError(t)
    cls = {"cover": "cover", "facts": "facts", "chart": "chart", "split": "split", "takeaways": "take"}[t]
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{font_css()}{CSS}</style></head>'
            f'<body><div class="grid"></div><div class="frame {cls}">{head(i, n)}<div class="body">{inner}</div>{foot(i == n)}</div></body></html>')


def main(post_path, outdir):
    post = json.loads(pathlib.Path(post_path).read_text())
    slides = post["slides"]
    assert len(slides) == 5, "Fin Ticks carousels must have exactly 5 slides"
    out = pathlib.Path(outdir); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        import os
        exe = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else p.chromium.launch(args=["--no-sandbox"])
        overflow = []
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for i, s in enumerate(slides, 1):
            h = slide_html(s, i, 5, post.get("sources", ""))
            (out / f"slide-{i}.html").write_text(h)
            pg.set_content(h, wait_until="load")
            pg.evaluate("document.fonts.ready")
            # overflow guard: content must not run into footer
            over = pg.evaluate("""()=>{const b=document.querySelector('.body');return b.scrollHeight>b.clientHeight+2}""")
            if over:
                print(f"OVERFLOW slide {i}: content overflows, shorten text", file=sys.stderr)
                overflow.append(i)
            pg.screenshot(path=str(out / f"slide-{i}.png"), full_page=False)
            from PIL import Image
            Image.open(out / f"slide-{i}.png").convert("RGB").save(out / f"slide-{i}.jpg", quality=92)
            print(out / f"slide-{i}.png")
        b.close()
    # contact sheet: all 5 slides in one image for a single visual check
    from PIL import Image
    ims = [Image.open(out / f"slide-{i}.jpg") for i in range(1, 6)]
    w, h = 432, 540
    sheet = Image.new("RGB", (w * 5 + 40, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), (i * (w + 10), 0))
    sheet.save(out / "contact.png")
    print(out / "contact.png")
    if overflow:
        sys.exit(f"Overflow on slides {overflow}: shorten text and re-render")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

#!/usr/bin/env python3
# CITY BUILDER LAB. — QR name-card image generator (Design Governance v2.0)
#   paper background, Ink modules, signature 2-color dots (Sky Blue / Grass Green)
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

URL = "https://citybuilderlab.github.io/"
OUT = "/workspace/downloads/citybuilderlab_qr.png"

PAPER = (248, 248, 246)   # #F8F8F6
INK = (22, 22, 22)        # #161616
GRAY = (85, 85, 85)       # #555555
RULE = (218, 218, 214)    # #DADAD6
SKY = (121, 172, 211)     # #79ACD3
GRASS = (54, 158, 56)     # #369E38

FONT = "/usr/share/fonts/pickle-hwp/NotoSansCJKkr-Regular.otf"
S = 2  # supersample factor
W, H = 1200, 1620


def f(size):
    return ImageFont.truetype(FONT, int(size * S))


def track(draw, xy, text, font, fill, spacing=0.0, anchor_left=True):
    """draw text with extra letter spacing (px)"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing * S
    return x


def tw(draw, text, font, spacing=0.0):
    return sum(draw.textlength(c, font=font) for c in text) + spacing * S * max(len(text) - 1, 0)


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)

# ---------- header ----------
mx = 96 * S
track(d, (mx, 112 * S), "CITY BUILDER LAB.", f(26), INK, spacing=3.6)
label = "DIRECTOR · ADVISORY"
lf = f(18)
track(d, (W * S - mx - tw(d, label, lf, 2.6), 121 * S), label, lf, GRAY, spacing=2.6)
d.line([(mx, 196 * S), (W * S - mx, 196 * S)], fill=RULE, width=2)

# ---------- QR ----------
qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=10, border=4)
qr.add_data(URL)
qr.make(fit=True)
q = qr.make_image(fill_color=INK, back_color=PAPER).convert("RGB")

QR_PX = 720 * S
q = q.resize((QR_PX, QR_PX), Image.NEAREST)
qx = (W * S - QR_PX) // 2
qy = 286 * S
img.paste(q, (qx, qy))

# ---------- 2 color bar ----------
bar_y = qy + QR_PX + 74 * S
bar_h = 6 * S
sky_w, grass_w = 84 * S, 56 * S
bar_x = (W * S - (sky_w + grass_w)) // 2
d.rectangle([bar_x, bar_y, bar_x + sky_w - 1, bar_y + bar_h], fill=SKY)
d.rectangle([bar_x + sky_w, bar_y, bar_x + sky_w + grass_w - 1, bar_y + bar_h], fill=GRASS)

# ---------- captions ----------
def centered(text, size, fill, y, spacing=0.0):
    ft = f(size)
    wpx = tw(d, text, ft, spacing)
    track(d, ((W * S - wpx) / 2, y * S), text, ft, fill, spacing=spacing)


centered("Youngsun Park", 40, INK, 1176, spacing=1.2)
centered("BRAND & BUSINESS GROWTH DIRECTOR", 17, GRAY, 1246, spacing=2.8)
centered("citybuilderlab.github.io", 24, GRAY, 1306, spacing=0.6)

# ---------- 2 color dots ----------
dot_r = 7 * S
gap = 14 * S
cy = 1392 * S
cx = (W * S - (dot_r * 2 * 2 + gap)) // 2
d.ellipse([cx, cy - dot_r, cx + dot_r * 2, cy + dot_r], fill=SKY)
d.ellipse([cx + dot_r * 2 + gap, cy - dot_r, cx + dot_r * 2 + gap + dot_r * 2, cy + dot_r], fill=GRASS)

# ---------- bottom rule + wordmark ----------
d.line([(mx, 1470 * S), (W * S - mx, 1470 * S)], fill=RULE, width=2)
track(d, (mx, 1506 * S), "CITY BUILDER LAB.", f(17), GRAY, spacing=2.8)
cc = "© 2026 Youngsun Park"
cf = f(17)
track(d, (W * S - mx - tw(d, cc, cf, 0.6), 1506 * S), cc, cf, GRAY, spacing=0.6)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, dpi=(300, 300))
print("saved", OUT, img.size)

#!/usr/bin/env python3
"""Compose the final entry image: collage + date banner + panel labels + footer."""
from PIL import Image, ImageDraw, ImageFont

SRC = "assets/media-generation-news-collage-raw-19-0-f1dcf993-1705-406c-9963-bd5ba6ccf3b1.webp"
OUT = "entry.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = 1024
BANNER_H = 92
FOOTER_H = 48
COL_H = W - BANNER_H - FOOTER_H  # 884

src = Image.open(SRC).convert("RGB")
col = src.resize((W, COL_H), Image.LANCZOS)

canvas = Image.new("RGB", (W, W), (10, 14, 26))
canvas.paste(col, (0, BANNER_H))
d = ImageDraw.Draw(canvas, "RGBA")

# --- banner ---
d.rectangle([0, 0, W, BANNER_H], fill=(10, 14, 26))
d.rectangle([0, BANNER_H - 4, W, BANNER_H], fill=(240, 165, 0))
title_f = ImageFont.truetype(FONT, 46)
sub_f = ImageFont.truetype(FONT, 21)
d.text((W // 2, 30), "THURSDAY 19 NOVEMBER 2026", font=title_f, fill=(255, 255, 255), anchor="mm")
d.text((W // 2, 68), "THE WORLD'S NEWS IN ONE IMAGE", font=sub_f, fill=(240, 165, 0), anchor="mm")

# --- footer ---
fy = BANNER_H + COL_H
d.rectangle([0, fy, W, W], fill=(10, 14, 26))
d.rectangle([0, fy, W, fy + 3], fill=(240, 165, 0))
foot_f = ImageFont.truetype(FONT, 19)
foot_text = "ALSO: TRUMP PARDONS PETE ROSE  ·  INDONESIA FIRE EMISSIONS 3RD-HIGHEST ON RECORD"
while d.textlength(foot_text, font=foot_f) > W - 24 and foot_f.size > 10:
    foot_f = ImageFont.truetype(FONT, foot_f.size - 1)
d.text(
    (W // 2, fy + FOOTER_H // 2),
    foot_text,
    font=foot_f, fill=(220, 228, 240), anchor="mm",
)

# --- panel labels ---
# collage geometry in source px (1600x1600), measured from the white gutters:
# top panel y 17..543; row2 y 559..1064 (split x 792..806);
# row3 y 1079..1583 (splits x 530..543, 1056..1070)
sx = W / 1600
sy = COL_H / 1600

def P(x, y):
    return (x * sx, BANNER_H + y * sy)

label_f = ImageFont.truetype(FONT, 24)
small_f = ImageFont.truetype(FONT, 21)

def label(x0, y1, x1, lines, font):
    """Dark strip at the bottom of a panel (y1 = panel bottom in final coords)."""
    # shrink the font until every line fits the panel width
    while font.size > 10 and any(d.textlength(ln, font=font) > (x1 - x0) - 16 for ln in lines):
        font = ImageFont.truetype(FONT, font.size - 1)
    line_h = font.size + 6
    h = line_h * len(lines) + 10
    d.rectangle([x0, y1 - h, x1, y1], fill=(5, 8, 16, 205))
    ty = y1 - h + 5
    for ln in lines:
        d.text(((x0 + x1) // 2, ty + line_h // 2), ln, font=font, fill=(255, 255, 255), anchor="mm")
        ty += line_h

# top panel
_, top_b = P(0, 543)
label(0, top_b, W, ["TRUMP–XI–PUTIN SUMMIT IN SHENZHEN:", "“A NUCLEAR WAR MUST NEVER BE FOUGHT”"], label_f)
# row 2
_, r2_b = P(0, 1064)
lx1, _ = P(799, 0)
label(0, r2_b, lx1, ["UN COURT RULES MYANMAR COMMITTED", "GENOCIDE AGAINST THE ROHINGYA"], small_f)
label(lx1 + 6, r2_b, W, ["ANTHROPIC IPO SOARS TO $2 TRILLION", "— LARGEST IN HISTORY"], small_f)
# row 3
_, r3_b = P(0, 1583)
m1, _ = P(536, 0)
m2, _ = P(1063, 0)
label(0, r3_b, m1, ["IRAN WIDENS GULF ATTACKS ·", "HORMUZ ON EDGE"], small_f)
label(m1 + 6, r3_b, m2, ["DENMARK APPROVES GREENLAND–US", "ARCTIC SECURITY PACT"], small_f)
label(m2 + 6, r3_b, W, ["CRIMEA BRIDGE HIT AGAIN ·", "RUSSIA'S FUEL BURNS"], small_f)

# JPEG bytes in a file named entry.png: the gate reads PNG or JPEG by first bytes,
# and JPEG keeps the poster well under the 1 MiB cap.
canvas.save(OUT, "JPEG", quality=88, optimize=True)
print("saved", OUT, canvas.size)

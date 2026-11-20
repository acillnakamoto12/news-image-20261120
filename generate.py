#!/usr/bin/env python3
"""Draw a one-day world-news front page (1024x1024 PNG) from news.json.

Usage: python3 news-image-generator.py <news.json> <out.png>
Deterministic: no network, no randomness, no timestamps in the PNG.
Layout is flow-based: every block's height is measured from its wrapped
lines, so text can never overlap a divider or the next story.
"""
import json
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 96, 108)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star_points(cx, cy, r_out, r_in, n=10):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon(d, kind, box, color):
    color = tuple(color)
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=16, fill=color)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w, h = x1 - x0, y1 - y0
    white = (255, 255, 255)
    if kind == "burst":
        d.polygon(star_points(cx, cy, w * 0.36, w * 0.16, 10), fill=white)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=color)
    elif kind == "bridge":
        d.arc([x0 + w * 0.16, y0 + h * 0.30, x1 - w * 0.16, y0 + h * 0.95],
              180, 360, fill=white, width=9)
        d.line([x0 + w * 0.14, y0 + h * 0.68, x1 - w * 0.14, y0 + h * 0.68],
               fill=white, width=9)
        for fx in (0.28, 0.5, 0.72):
            d.line([x0 + w * fx, y0 + h * 0.42, x0 + w * fx, y0 + h * 0.68],
                   fill=white, width=6)
    elif kind == "summit":
        for fx in (0.28, 0.5, 0.72):
            d.ellipse([x0 + w * fx - 13, y0 + h * 0.28 - 13,
                       x0 + w * fx + 13, y0 + h * 0.28 + 13], fill=white)
            d.pieslice([x0 + w * fx - 20, y0 + h * 0.52 - 6,
                        x0 + w * fx + 20, y0 + h * 0.52 + 34],
                       180, 360, fill=white)
    elif kind == "virus":
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=white)
        for i in range(8):
            a = math.pi * i / 4
            d.line([cx + 24 * math.cos(a), cy + 24 * math.sin(a),
                    cx + 34 * math.cos(a), cy + 34 * math.sin(a)],
                   fill=white, width=6)
    elif kind == "chart":
        base = y0 + h * 0.78
        for i, bh in enumerate((0.28, 0.48, 0.68)):
            bx = x0 + w * (0.22 + i * 0.24)
            d.rectangle([bx, base - h * bh, bx + w * 0.14, base], fill=white)
    elif kind == "tent":
        d.polygon([(cx, y0 + h * 0.24), (x0 + w * 0.18, y0 + h * 0.76),
                   (x1 - w * 0.18, y0 + h * 0.76)], fill=white)
        d.polygon([(cx, y0 + h * 0.52), (cx - 12, y0 + h * 0.76),
                   (cx + 12, y0 + h * 0.76)], fill=color)
    elif kind == "plane":
        d.polygon([(x0 + w * 0.20, y0 + h * 0.62), (x0 + w * 0.82, y0 + h * 0.28),
                   (x0 + w * 0.66, y0 + h * 0.58), (x0 + w * 0.78, y0 + h * 0.72),
                   (x0 + w * 0.60, y0 + h * 0.66), (x0 + w * 0.38, y0 + h * 0.78)],
                  fill=white)
    elif kind == "senate":
        d.rectangle([x0 + w * 0.20, y0 + h * 0.26, x1 - w * 0.20, y0 + h * 0.36],
                    fill=white)
        for fx in (0.28, 0.5, 0.72):
            d.rectangle([x0 + w * fx - 7, y0 + h * 0.40, x0 + w * fx + 7,
                         y0 + h * 0.70], fill=white)
        d.rectangle([x0 + w * 0.16, y0 + h * 0.72, x1 - w * 0.16, y0 + h * 0.80],
                    fill=white)


def draw(data, out_path):
    for s in data["stories"]:
        s["color"] = tuple(s["color"])
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34
    y = 26

    # ---- masthead ----
    d.text((mx, y), data["kicker"], font=font(FONT_B, 20), fill=RED)
    y += 28
    d.text((mx, y), data["title"], font=font(FONT_S, 54), fill=INK)
    y += 66
    d.text((mx, y), data["date_line"], font=font(FONT_B, 32), fill=RED)
    y += 46
    d.rectangle([mx, y, W - mx, y + 5], fill=INK)
    y += 11
    d.rectangle([mx, y, W - mx, y + 2], fill=INK)
    y += 16

    stories = data["stories"]
    lead, rest = stories[0], stories[1:]

    # ---- lead story (flow-measured) ----
    tx = mx + 172
    tw = W - mx - tx
    f_tag, f_lh, f_ls = font(FONT_B, 20), font(FONT_B, 40), font(FONT_R, 23)
    hl = wrap(d, lead["headline"], f_lh, tw)[:2]
    sl = wrap(d, lead["summary"], f_ls, tw)[:2]
    content_h = 26 + len(hl) * 46 + len(sl) * 29
    block_h = max(148, content_h)
    iy = y + (block_h - 148) // 2
    icon(d, lead["icon"], (mx, iy, mx + 148, iy + 148), lead["color"])
    cy = y
    d.text((tx, cy), lead["tag"], font=f_tag, fill=lead["color"])
    cy += 26
    for line in hl:
        d.text((tx, cy), line, font=f_lh, fill=INK)
        cy += 46
    for line in sl:
        d.text((tx, cy), line, font=f_ls, fill=(40, 48, 66))
        cy += 29
    y += block_h + 10
    d.line([mx, y, W - mx, y], fill=(200, 196, 186), width=2)
    y += 10

    # ---- remaining stories (flow-measured) ----
    f_tag2, f_h, f_s = font(FONT_B, 19), font(FONT_B, 30), font(FONT_R, 22)
    for i, s in enumerate(rest):
        tx = mx + 102
        tw = W - mx - tx
        hl = wrap(d, s["headline"], f_h, tw)[:2]
        max_sum = 2 if len(hl) == 1 else 1
        sl = wrap(d, s["summary"], f_s, tw)[:max_sum]
        content_h = 25 + len(hl) * 35 + len(sl) * 27
        block_h = max(84, content_h)
        iy = y + (block_h - 84) // 2
        icon(d, s["icon"], (mx, iy, mx + 84, iy + 84), s["color"])
        cy = y
        d.text((tx, cy), s["tag"], font=f_tag2, fill=s["color"])
        cy += 25
        for line in hl:
            d.text((tx, cy), line, font=f_h, fill=INK)
            cy += 35
        for line in sl:
            d.text((tx, cy), line, font=f_s, fill=(40, 48, 66))
            cy += 27
        y += block_h
        if i < len(rest) - 1:
            y += 4
            d.line([mx, y, W - mx, y], fill=(214, 210, 200), width=1)
            y += 6

    # ---- footer (shrunk to fit if needed) ----
    f_f = font(FONT_R, 18)
    while d.textlength(data["footer"], font=f_f) > W - 2 * mx and f_f.size > 12:
        f_f = font(FONT_R, f_f.size - 1)
    d.text((mx, H - 30), data["footer"], font=f_f, fill=GREY)
    print("content ends at y=%d (canvas %d)" % (y, H))
    assert y <= H - 40, "layout overflow: content ends at %d" % y

    img.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    news_path, out_path = sys.argv[1], sys.argv[2]
    with open(news_path) as f:
        data = json.load(f)
    draw(data, out_path)
    print("wrote", out_path)


if __name__ == "__main__":
    main()

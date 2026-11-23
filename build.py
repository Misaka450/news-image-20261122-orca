#!/usr/bin/env python3
# build.py -- "The World Daily" front-page plate, Sunday 22 November 2026.
# Orca's entry for make.fun news-image-20261122.
#
# Design (by Orca, drawn by hand in code):
#   a real broadsheet front page, not a dashboard.
#   - paper stock, ink rules, no boxes-with-badges anywhere
#   - 4 lead stories carried by code-drawn spot illustrations
#   - a red sports-style scoreboard for the day's hard numbers
#   - a solid region band whose segment widths encode story counts
#   - unequal editorial columns with kicker lines, then wire dispatches
#   - a DATE CHECK bar naming what was left out, and why
# Deterministic: fixed seed, no network, Pillow only.

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

from data import STORIES, DATE_CHECK, STATUS_LABEL

W = H = 1024
M = 22
INNER = W - 2 * M

PAPER = (243, 238, 226)
PAPER_DK = (231, 225, 209)
WHITE = (250, 247, 240)
INK = (27, 24, 21)
INK_SOFT = (82, 75, 66)
RED = (166, 33, 41)
RED_DK = (124, 22, 29)
ORANGE = (212, 108, 38)
SMOKE = (150, 145, 136)
SEA = (58, 84, 102)

REGION_COLOR = {
    "EUROPE": (43, 93, 138),
    "NORTH AMERICA": (138, 43, 43),
    "LATIN AMERICA": (61, 122, 74),
    "MIDDLE EAST": (176, 122, 42),
    "SOUTH & EAST ASIA": (106, 74, 138),
    "AFRICA": (138, 90, 43),
    "OCEANIA & POLAR": (42, 122, 138),
}
REGION_SHORT = {
    "EUROPE": "EUROPE",
    "NORTH AMERICA": "N. AMERICA",
    "LATIN AMERICA": "LATAM",
    "MIDDLE EAST": "MID. EAST",
    "SOUTH & EAST ASIA": "S. & E. ASIA",
    "AFRICA": "AFRICA",
    "OCEANIA & POLAR": "OCEANIA",
}

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def serif(name, size):
    return ImageFont.truetype(FD + name, size)


f_mast = serif("DejaVuSerif-Bold.ttf", 15)
f_mast_i = serif("DejaVuSerif-Italic.ttf", 12)
f_date = serif("DejaVuSerif-Bold.ttf", 46)
f_score = ImageFont.truetype(FL + "LiberationMono-Bold.ttf", 17)
f_band = ImageFont.truetype(FL + "LiberationMono-Bold.ttf", 12)
f_kick = serif("DejaVuSerifCondensed-Bold.ttf", 11)
f_head = serif("DejaVuSerifCondensed-Bold.ttf", 21)
f_head_s = serif("DejaVuSerifCondensed-Bold.ttf", 13)
f_sub = serif("DejaVuSerifCondensed.ttf", 13)
f_sub_s = serif("DejaVuSerifCondensed.ttf", 11)
f_cred = serif("DejaVuSerifCondensed-Italic.ttf", 10)
f_disp = serif("DejaVuSerifCondensed.ttf", 12)
f_dc = ImageFont.truetype(FL + "LiberationMono-Bold.ttf", 11)
f_foot = serif("DejaVuSerifCondensed-Italic.ttf", 10)


def blend(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(d, text, font, width):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def wrap_max(d, text, font, width, maxn):
    lines = wrap(d, text, font, width)
    if len(lines) <= maxn:
        return lines
    keep = lines[:maxn]
    last = keep[-1]
    while last and d.textlength(last + "...", font=font) > width:
        last = last[:-1]
    keep[-1] = last.rstrip() + "..."
    return keep


# ---------------------------------------------------------------- glyphs
# Every glyph is built from primitives at half-size s around (cx, cy).
# Abstract on purpose: no faces, no real buildings, nothing to get wrong.

def g_flame(d, cx, by, s, col=RED, inner=ORANGE):
    d.polygon([(cx, by - 2.2 * s), (cx + .75 * s, by - .9 * s),
               (cx + .5 * s, by), (cx, by - .4 * s),
               (cx - .5 * s, by), (cx - .75 * s, by - .9 * s)], fill=col)
    d.polygon([(cx, by - 1.3 * s), (cx + .4 * s, by - .5 * s),
               (cx + .25 * s, by), (cx, by - .25 * s),
               (cx - .25 * s, by), (cx - .4 * s, by - .5 * s)], fill=inner)


def g_drone(d, cx, cy, s, col):
    lw = max(2, int(s * .22))
    d.line([cx - s, cy - s * .55, cx + s, cy + s * .55], fill=col, width=lw)
    d.line([cx - s, cy + s * .55, cx + s, cy - s * .55], fill=col, width=lw)
    for dx, dy in ((-1, -.55), (1, .55), (-1, .55), (1, -.55)):
        ex, ey = cx + dx * s, cy + dy * s
        d.ellipse([ex - s * .34, ey - s * .16, ex + s * .34, ey + s * .16],
                  outline=col, width=2)
    d.rectangle([cx - s * .3, cy - s * .18, cx + s * .3, cy + s * .18], fill=col)


def g_ship(d, cx, cy, s, col):
    d.polygon([(cx - s, cy), (cx + s, cy), (cx + .8 * s, cy + .5 * s),
               (cx - .85 * s, cy + .5 * s)], fill=col)
    d.rectangle([cx - .3 * s, cy - .42 * s, cx + .2 * s, cy], fill=col)
    d.rectangle([cx - .12 * s, cy - .8 * s, cx + .02 * s, cy - .42 * s], fill=col)
    d.line([cx - .05 * s, cy - .8 * s, cx + .45 * s, cy - .45 * s],
           fill=col, width=2)


def g_house(d, cx, cy, s, col):
    d.rectangle([cx - .8 * s, cy - .2 * s, cx + .8 * s, cy + .9 * s], fill=col)
    d.polygon([(cx - .95 * s, cy - .2 * s), (cx, cy - .95 * s),
               (cx + .95 * s, cy - .2 * s)], fill=col)


def g_ballot(d, cx, cy, s, col):
    d.rectangle([cx - .8 * s, cy - .35 * s, cx + .8 * s, cy + .85 * s],
                outline=col, width=max(2, int(s * .18)))
    d.rectangle([cx - .45 * s, cy - .38 * s, cx + .45 * s, cy - .22 * s], fill=col)
    d.polygon([(cx - .12 * s, cy - 1.0 * s), (cx + .3 * s, cy - 1.0 * s),
               (cx + .2 * s, cy - .3 * s), (cx - .02 * s, cy - .3 * s)], fill=col)


def g_dome(d, cx, cy, s, col):
    d.pieslice([cx - s, cy - s, cx + s, cy + .9 * s], 180, 360, fill=col)
    d.rectangle([cx - 1.1 * s, cy - .08 * s, cx + 1.1 * s, cy + .08 * s], fill=col)
    for i in range(5):
        px = cx - .9 * s + i * .45 * s
        d.rectangle([px - .07 * s, cy + .08 * s, px + .07 * s, cy + .8 * s],
                    fill=col)


def g_star(d, cx, cy, s, col, points=5):
    pts = []
    for i in range(points * 2):
        r = s if i % 2 == 0 else s * .45
        a = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=col)


def g_explosion(d, cx, cy, s, col):
    pts = []
    for i in range(16):
        r = s if i % 2 == 0 else s * .4
        a = i * math.pi / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=col)


def g_bolt(d, cx, cy, s, col):
    d.polygon([(cx + .25 * s, cy - s), (cx - .55 * s, cy + .15 * s),
               (cx - .05 * s, cy + .15 * s), (cx - .25 * s, cy + s),
               (cx + .55 * s, cy - .15 * s), (cx + .05 * s, cy - .15 * s)],
              fill=col)


def g_waves(d, cx, cy, s, col):
    for row in range(3):
        yy = cy - s * .6 + row * s * .6
        for k in range(3):
            x0 = cx - s + k * s * .8
            d.arc([x0, yy - s * .28, x0 + s * .8, yy + s * .28],
                  180, 360, fill=col, width=2)


def g_heart(d, cx, cy, s, col):
    d.ellipse([cx - .85 * s, cy - .75 * s, cx, cy + .1 * s], fill=col)
    d.ellipse([cx, cy - .75 * s, cx + .85 * s, cy + .1 * s], fill=col)
    d.polygon([(cx - .78 * s, cy - .2 * s), (cx + .78 * s, cy - .2 * s),
               (cx, cy + .9 * s)], fill=col)


def g_scales(d, cx, cy, s, col):
    d.line([cx, cy - s, cx, cy + .7 * s], fill=col, width=max(2, int(s * .16)))
    d.line([cx - .9 * s, cy - .6 * s, cx + .9 * s, cy - .6 * s],
           fill=col, width=max(2, int(s * .16)))
    for side in (-1, 1):
        px = cx + side * .9 * s
        d.line([px, cy - .6 * s, px - .3 * s, cy + .05 * s], fill=col, width=2)
        d.line([px, cy - .6 * s, px + .3 * s, cy + .05 * s], fill=col, width=2)
        d.arc([px - .32 * s, cy - .1 * s, px + .32 * s, cy + .5 * s],
              0, 180, fill=col, width=2)
    d.line([cx - .5 * s, cy + .85 * s, cx + .5 * s, cy + .85 * s],
           fill=col, width=max(2, int(s * .16)))


def g_plane(d, cx, cy, s, col):
    d.polygon([(cx - s, cy + .15 * s), (cx + s, cy - .35 * s),
               (cx + .75 * s, cy + .05 * s), (cx - .7 * s, cy + .45 * s)],
              fill=col)
    d.polygon([(cx - .2 * s, cy + .1 * s), (cx + .15 * s, cy + .85 * s),
               (cx + .45 * s, cy + .8 * s), (cx + .25 * s, cy)], fill=col)


def g_key(d, cx, cy, s, col):
    d.ellipse([cx - s, cy - .7 * s, cx - .1 * s, cy + .2 * s],
              outline=col, width=max(2, int(s * .18)))
    d.line([cx - .1 * s, cy - .25 * s, cx + .9 * s, cy + .75 * s],
           fill=col, width=max(2, int(s * .18)))
    d.line([cx + .55 * s, cy + .42 * s, cx + .85 * s, cy + .2 * s],
           fill=col, width=2)
    d.line([cx + .75 * s, cy + .6 * s, cx + 1.05 * s, cy + .38 * s],
           fill=col, width=2)


def g_candle(d, cx, cy, s, col):
    d.rectangle([cx - .3 * s, cy - .1 * s, cx + .3 * s, cy + .9 * s], fill=col)
    g_flame(d, cx, cy - .15 * s, .5 * s, col=col, inner=col)


def g_flask(d, cx, cy, s, col):
    d.polygon([(cx - .7 * s, cy + .8 * s), (cx + .7 * s, cy + .8 * s),
               (cx + .2 * s, cy - .3 * s), (cx - .2 * s, cy - .3 * s)],
              outline=col, width=max(2, int(s * .16)))
    d.line([cx - .2 * s, cy - .3 * s, cx - .2 * s, cy - .8 * s],
           fill=col, width=max(2, int(s * .16)))
    d.line([cx + .2 * s, cy - .3 * s, cx + .2 * s, cy - .8 * s],
           fill=col, width=max(2, int(s * .16)))


def g_truck(d, cx, cy, s, col):
    d.rectangle([cx - s, cy - .5 * s, cx + .25 * s, cy + .35 * s],
                outline=col, width=max(2, int(s * .16)))
    d.rectangle([cx + .25 * s, cy - .15 * s, cx + .95 * s, cy + .35 * s],
                outline=col, width=max(2, int(s * .16)))
    for wx in (-.6, .6):
        d.ellipse([cx + wx * s - .18 * s, cy + .3 * s,
                   cx + wx * s + .18 * s, cy + .66 * s], fill=col)


def g_snow(d, cx, cy, s, col):
    for i in range(3):
        a = i * math.pi / 3
        dx, dy = math.cos(a) * s, math.sin(a) * s
        d.line([cx - dx, cy - dy, cx + dx, cy + dy], fill=col, width=2)


def g_flag(d, cx, cy, s, col):
    d.line([cx - .5 * s, cy - s, cx - .5 * s, cy + s],
           fill=col, width=max(2, int(s * .16)))
    d.polygon([(cx - .5 * s, cy - s), (cx + .8 * s, cy - .65 * s),
               (cx - .5 * s, cy - .3 * s)], fill=col)


def g_eye(d, cx, cy, s, col):
    d.arc([cx - s, cy - .6 * s, cx + s, cy + .6 * s], 200, 340,
          fill=col, width=max(2, int(s * .16)))
    d.arc([cx - s, cy - .6 * s, cx + s, cy + .6 * s], 20, 160,
          fill=col, width=max(2, int(s * .16)))
    d.ellipse([cx - .22 * s, cy - .22 * s, cx + .22 * s, cy + .22 * s], fill=col)


def g_phone(d, cx, cy, s, col):
    d.rectangle([cx - .45 * s, cy - s, cx + .45 * s, cy + s],
                outline=col, width=max(2, int(s * .16)))
    d.line([cx - .2 * s, cy + .7 * s, cx + .2 * s, cy + .7 * s], fill=col, width=2)


def g_crash(d, cx, cy, s, col):
    d.line([cx - s, cy - .8 * s, cx - .2 * s, cy - .1 * s],
           fill=col, width=max(2, int(s * .2)))
    d.line([cx - .2 * s, cy - .1 * s, cx - .55 * s, cy + .3 * s],
           fill=col, width=max(2, int(s * .2)))
    d.line([cx - .55 * s, cy + .3 * s, cx + .3 * s, cy + .55 * s],
           fill=col, width=max(2, int(s * .2)))
    d.line([cx + .3 * s, cy + .55 * s, cx + .9 * s, cy - .1 * s],
           fill=col, width=max(2, int(s * .2)))


def g_money(d, cx, cy, s, col):
    d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=col,
              width=max(2, int(s * .16)))
    fnt = serif("DejaVuSerif-Bold.ttf", int(s * 1.3))
    d.text((cx, cy), "$", font=fnt, fill=col, anchor="mm")


def g_bridge(d, cx, cy, s, col):
    d.arc([cx - s, cy - .9 * s, cx + s, cy + .9 * s], 180, 360,
          fill=col, width=max(2, int(s * .16)))
    for px in (-.6, .6):
        d.line([cx + px * s, cy - .55 * s, cx + px * s, cy + .6 * s],
               fill=col, width=max(2, int(s * .16)))
    d.line([cx - s, cy + .6 * s, cx + s, cy + .6 * s],
           fill=col, width=max(2, int(s * .16)))


def g_block(d, cx, cy, s, col):
    d.rectangle([cx - .7 * s, cy - .7 * s, cx + .7 * s, cy + .7 * s],
                outline=col, width=max(2, int(s * .16)))
    d.line([cx - .7 * s, cy - .7 * s, cx + .7 * s, cy + .7 * s], fill=col, width=2)
    d.line([cx - .7 * s, cy + .7 * s, cx + .7 * s, cy - .7 * s], fill=col, width=2)


def g_dot(d, cx, cy, s, col):
    d.polygon([(cx, cy - s * .8), (cx + s * .8, cy), (cx, cy + s * .8),
               (cx - s * .8, cy)], fill=col)


GLYPHS = {
    "drone": g_drone, "ship": g_ship, "tanker": g_ship, "house": g_house,
    "ballot": g_ballot, "dome": g_dome, "star": g_star, "alert": g_explosion,
    "explosion": g_explosion, "power": g_bolt, "water": g_waves,
    "heart": g_heart, "court": g_scales, "plane": g_plane, "key": g_key,
    "memory": g_candle, "flask": g_flask, "truck": g_truck, "snow": g_snow,
    "flag": g_flag, "eyes": g_eye, "phone": g_phone, "crash": g_crash,
    "money": g_money, "bridge": g_bridge, "block": g_block,
}


def draw_glyph(d, glyph, cx, cy, s, col):
    GLYPHS.get(glyph, g_dot)(d, cx, cy, s, col)


# ---------------------------------------------------------------- scenes
# The four lead illustrations. Duotone: region tint over paper, ink figures.

def scene_frame(d, x, y, w, h, col):
    d.rectangle([x, y, x + w, y + h], fill=blend(col, PAPER, .84))
    ground = y + int(h * .76)
    d.rectangle([x, ground, x + w, y + h], fill=blend(col, PAPER, .62))
    d.line([x, ground, x + w, ground], fill=blend(col, INK, .35), width=2)
    return ground


def scene_cop(d, x, y, w, h, col):
    """COP31 collapses: a cracked globe above an empty table."""
    ground = scene_frame(d, x, y, w, h, col)
    cx, cy, r = x + w // 2, y + int(h * .34), int(min(w, h) * .26)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=2)
    d.arc([cx - r, cy - r * .55, cx + r, cy + r * .55], 0, 360, fill=INK, width=2)
    crack = [(cx - r * .15, cy - r), (cx + r * .18, cy - r * .35),
             (cx - r * .1, cy + r * .05), (cx + r * .3, cy + r * .45),
             (cx + r * .08, cy + r)]
    d.line(crack, fill=RED, width=4)
    # table and empty chairs
    tw = int(w * .66)
    d.rectangle([cx - tw // 2, ground - 8, cx + tw // 2, ground], fill=INK)
    for i in (-1, 0, 1):
        bx = cx + i * int(tw * .38)
        d.rectangle([bx - 9, ground - 30, bx + 9, ground - 8], outline=INK, width=3)
    # scattered paper
    d.polygon([(cx - tw // 2 + 12, ground - 12), (cx - tw // 2 + 34, ground - 16),
               (cx - tw // 2 + 30, ground - 6)], fill=PAPER)


def scene_ship_fire(d, x, y, w, h, col):
    """The corvette Merkury burning off Benghazi."""
    ground = scene_frame(d, x, y, w, h, col)
    for i in range(4):
        yy = ground + 6 + i * 7
        for k in range(int(w // 26)):
            d.arc([x + 8 + k * 26, yy - 6, x + 8 + k * 26 + 22, yy + 6],
                  180, 360, fill=SEA, width=2)
    sw = int(w * .62)
    sx, sy = x + (w - sw) // 2, ground - int(h * .1)
    g_ship(d, sx + sw // 2, sy, sw // 2, INK)
    g_flame(d, sx + int(sw * .38), sy - 6, int(h * .09))
    g_flame(d, sx + int(sw * .6), sy - 2, int(h * .07))
    for i, (ox, oy, r) in enumerate(((0, -46, 12), (10, -66, 16), (-8, -90, 20))):
        d.ellipse([sx + sw // 2 + ox - r, sy + oy - r,
                   sx + sw // 2 + ox + r, sy + oy + r], outline=SMOKE, width=3)


def scene_drone_block(d, x, y, w, h, col):
    """Drone strike on a residential block at Dymer."""
    scene_frame(d, x, y, w, h, col)
    bw, bh = int(w * .44), int(h * .62)
    bx, by = x + int(w * .1), y + int(h * .14)
    d.rectangle([bx, by, bx + bw, by + bh], fill=INK)
    for r in range(int(bh // 18)):
        for c in range(int(bw // 18)):
            wx, wy = bx + 5 + c * 18, by + 5 + r * 18
            d.rectangle([wx, wy, wx + 8, wy + 10], fill=PAPER)
    cxp, cyp = bx + int(bw * .68), by + int(bh * .42)
    jag = [(cxp - 16, cyp - 24), (cxp + 2, cyp - 14), (cxp + 18, cyp - 22),
           (cxp + 12, cyp), (cxp + 20, cyp + 14), (cxp, cyp + 10),
           (cxp - 14, cyp + 20), (cxp - 8, cyp)]
    d.polygon(jag, fill=PAPER)
    g_flame(d, cxp, cyp + 14, 12)
    dcx, dcy = x + int(w * .72), y + int(h * .2)
    g_drone(d, dcx, dcy, 15, INK)
    d.arc([dcx - 40, dcy - 14, dcx - 8, dcy + 30], 280, 40, fill=INK_SOFT, width=2)
    d.arc([dcx - 54, dcy - 22, dcx - 8, dcy + 40], 280, 40, fill=INK_SOFT, width=2)


def scene_ballot(d, x, y, w, h, col):
    """The House changes hands: dome over a ballot box."""
    ground = scene_frame(d, x, y, w, h, col)
    cx = x + w // 2
    g_dome(d, cx, y + int(h * .4), int(w * .4), blend(col, INK, .5))
    bw = int(w * .34)
    g_ballot(d, cx, ground - int(h * .16), bw // 2, INK)
    g_star(d, x + int(w * .18), y + int(h * .2), 9, RED)
    g_star(d, x + int(w * .82), y + int(h * .16), 7, RED)


SCENES = [scene_cop, scene_ship_fire, scene_drone_block, scene_ballot]


# ---------------------------------------------------------------- page

def paper_texture(d):
    rnd = random.Random(20261122)
    for _ in range(5200):
        px, py = rnd.randrange(W), rnd.randrange(H)
        delta = rnd.choice((-7, -5, 5, 6))
        base = d.im.getpixel((px, py)) if hasattr(d, "im") else None
    # cheaper: draw 1px dots via point list
    pts_dark, pts_light = [], []
    for _ in range(2600):
        pts_dark.append((rnd.randrange(W), rnd.randrange(H)))
        pts_light.append((rnd.randrange(W), rnd.randrange(H)))
    d.point(pts_dark, fill=PAPER_DK)
    d.point(pts_light, fill=(250, 246, 236))


def masthead(d):
    d.rectangle([M, 22, W - M, 25], fill=INK)
    d.text((M, 32), "THE WORLD DAILY", font=f_mast, fill=INK)
    t = "one day on earth, drawn by hand"
    d.text((W - M - d.textlength(t, font=f_mast_i), 34), t,
           font=f_mast_i, fill=INK_SOFT)
    date = "Sunday 22 November 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 48), date, font=f_date, fill=INK)
    d.rectangle([M, 104, W - M, 106], fill=INK)
    d.line([M, 109, W - M, 109], fill=INK, width=1)


def scoreboard(d):
    y0, y1 = 118, 148
    d.rectangle([M, y0, W - M, y1], fill=RED)
    d.rectangle([M, y1 - 3, W - M, y1], fill=RED_DK)
    n = len(STORIES)
    txt = (f"186 DRONES  |  0 DEAL AT COP31  |  74,742 GAZA TOLL  |  "
           f"$12.1BN WFP ASK  |  {n} STORIES / 7 REGIONS")
    tw = d.textlength(txt, font=f_score)
    d.text(((W - tw) / 2, y0 + 7), txt, font=f_score, fill=WHITE)


def region_band(d):
    y0, y1 = 156, 174
    counts = {}
    order = []
    for st in STORIES:
        counts[st.region] = counts.get(st.region, 0) + 1
        if st.region not in order:
            order.append(st.region)
    total = sum(counts.values())
    x = M
    for i, reg in enumerate(order):
        seg = int(INNER * counts[reg] / total)
        if i == len(order) - 1:
            seg = W - M - x
        col = REGION_COLOR[reg]
        d.rectangle([x, y0, x + seg, y1], fill=col)
        label = f"{REGION_SHORT[reg]} {counts[reg]}"
        if d.textlength(label, font=f_band) + 10 <= seg:
            d.text((x + 6, y0 + 3), label, font=f_band, fill=WHITE)
        x += seg


def lead_cards(d, top):
    leads = STORIES[:4]
    widths = [296, 238, 226, 192]
    gap = (INNER - sum(widths)) / 3
    x = M
    scene_h = 168
    for st, wcol, scene in zip(leads, widths, SCENES):
        region, place, kicker, head = st.region, st.place, st.kicker, st.headline
        counters, status, credits = st.detail, st.status, st.source
        col = REGION_COLOR[region]
        scene(d, x, top, wcol, scene_h, col)
        yy = top + scene_h + 8
        d.rectangle([x, yy + 2, x + 8, yy + 10], fill=col)
        kick = f"{REGION_SHORT[region]} · {place.upper()} · {kicker} · {STATUS_LABEL[status]}"
        while d.textlength(kick, font=f_kick) > wcol - 13:
            kick = kick[:-1]
        kick = kick.rstrip(" ·") + "…"
        d.text((x + 13, yy), kick, font=f_kick, fill=col)
        yy += 17
        for ln in wrap_max(d, head, f_head, wcol, 3):
            d.text((x, yy), ln, font=f_head, fill=INK)
            yy += 23
        yy += 3
        for ln in wrap_max(d, counters, f_sub, wcol, 2):
            d.text((x, yy), ln, font=f_sub, fill=INK_SOFT)
            yy += 15
        d.text((x, yy + 1), credits, font=f_cred, fill=INK_SOFT)
        x += wcol + gap
    return top + scene_h + 8 + 17 + 3 * 23 + 3 + 2 * 15 + 14


def column_item(d, x, w, y, st):
    region, place, kicker = st.region, st.place, st.kicker
    glyph, head, status, counters = st.glyph, st.headline, st.status, st.detail
    col = REGION_COLOR[region]
    draw_glyph(d, glyph, x + 11, y + 15, 10, col)
    tx = x + 27
    kick = f"{REGION_SHORT[region]} · {place.upper()} · {kicker} · {STATUS_LABEL[status]}"
    while d.textlength(kick, font=f_kick) > w - 27:
        kick = kick[:-1]
    kick = kick.rstrip(" ·") + "…"
    d.text((tx, y), kick, font=f_kick, fill=col)
    yy = y + 13
    for ln in wrap_max(d, head, f_head_s, w - 27, 2):
        d.text((tx, yy), ln, font=f_head_s, fill=INK)
        yy += 14
    c0 = counters.split("·")[0].strip()
    d.text((tx, yy), c0, font=f_sub_s, fill=INK_SOFT)
    return y + 13 + 28 + 12 + 5


def columns(d, y0):
    blocks = [
        ("MIDDLE EAST", [5, 8, 23, 24, 25, 26]),
        ("EUROPE", [9, 10, 11, 12, 13, 14]),
        ("SOUTH & EAST ASIA", [7, 32, 33, 34, 35, 36]),
        ("LATIN AMERICA", [4, 19, 20]),
        ("AFRICA", [6, 39, 40]),
    ]
    widths = [266, 244, 234, 200]
    gap = (INNER - sum(widths)) / 3
    # assign blocks to columns: ME / EU / SEA / LA+AF
    col_blocks = [blocks[0:1], blocks[1:2], blocks[2:3], blocks[3:5]]
    x = M
    bottom = y0
    for wcol, bl in zip(widths, col_blocks):
        y = y0
        for reg, idxs in bl:
            col = REGION_COLOR[reg]
            d.rectangle([x, y, x + wcol, y + 14], fill=col)
            d.text((x + 5, y + 2), reg, font=f_kick, fill=WHITE)
            y += 19
            for i in idxs:
                y = column_item(d, x, wcol, y, STORIES[i])
                y += 4
        x += wcol + gap
        bottom = max(bottom, y)
    return bottom


def dispatches(d, y0):
    pool = [15, 16, 17, 18, 21, 22, 27, 28, 29, 30, 31, 37, 38, 41, 42, 43, 44, 45]
    d.line([M, y0, W - M, y0], fill=INK, width=1)
    d.text((M, y0 + 4), "DISPATCHES", font=f_kick, fill=INK)
    y0 += 18
    cols, rows = 3, 6
    cw = (INNER - 2 * 16) / cols
    for k, i in enumerate(pool):
        cx = M + (k // rows) * (cw + 16)
        cy = y0 + (k % rows) * 16
        st = STORIES[i]
        region, glyph, head, status, counters = st.region, st.glyph, st.headline, st.status, st.detail
        col = REGION_COLOR[region]
        d.rectangle([cx, cy + 3, cx + 6, cy + 9], fill=col)
        c0 = counters.split("·")[0].strip()
        txt = f"{head} -- {c0}"
        while txt and d.textlength(txt, font=f_disp) > cw - 14:
            txt = txt[:-1]
        d.text((cx + 11, cy), txt.rstrip() + ("..." if len(txt) < len(head) + 4 else ""),
               font=f_disp, fill=INK)
    return y0 + rows * 16 + 6


def date_check(d, y0):
    y1 = y0 + 34
    d.rectangle([M, y0, W - M, y1], fill=INK)
    items = "  |  ".join(f"{dt} {txt}" for dt, txt, _rg, verdict in DATE_CHECK)
    line = "DATE CHECK -- NOT OF THIS DAY:  " + items
    if d.textlength(line, font=f_dc) > INNER - 16:
        while d.textlength(line + "...", font=f_dc) > INNER - 16:
            line = line[:-1]
        line += "..."
    d.text((M + 8, y0 + 6), line, font=f_dc, fill=WHITE)
    d.text((M + 8, y0 + 19),
           "every story above was first reported on 22 Nov 2026; earlier "
           "developments were cut, however large.",
           font=f_foot, fill=blend(WHITE, INK, .25))


def footer(d):
    d.line([M, H - 16, W - M, H - 16], fill=INK_SOFT, width=1)
    d.text((M, H - 13), "THE WORLD DAILY - set in code, drawn by hand",
           font=f_foot, fill=INK_SOFT)
    t = "page 1 of 1"
    d.text((W - M - d.textlength(t, font=f_foot), H - 13), t,
           font=f_foot, fill=INK_SOFT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    paper_texture(d)
    masthead(d)
    scoreboard(d)
    region_band(d)
    y = lead_cards(d, 184)
    d.rectangle([M, y + 4, W - M, y + 6], fill=INK)
    y = columns(d, y + 14)
    y = dispatches(d, y + 8)
    date_check(d, max(y + 4, H - 58))
    footer(d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    prev = img.resize((300, 300), Image.LANCZOS)
    prev.save(os.path.join(os.path.dirname(out), "preview-300.png"), optimize=True)
    print("entry.png:", os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

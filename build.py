from __future__ import annotations

import hashlib
import math
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from data import DATE_CHECK, STORIES, STATUS_LABEL


W = H = 1024
SCALE = 3
OUT = Path(__file__).with_name("preview.png")

PAPER = (243, 241, 231)
INK = (35, 32, 29)
MUTED = (103, 96, 87)
RED = (166, 31, 40)
BLUE = (52, 100, 143)
GOLD = (179, 126, 39)
GREEN = (62, 125, 76)
PURPLE = (110, 74, 138)
TEAL = (47, 125, 137)
REGION_COLORS = {
    "EUROPE": BLUE,
    "MIDDLE EAST": GOLD,
    "LATIN AMERICA": GREEN,
    "NORTH AMERICA": (144, 48, 53),
    "SOUTH & EAST ASIA": PURPLE,
    "AFRICA": (153, 96, 42),
    "OCEANIA & POLAR": TEAL,
}


def font(size: int, bold: bool = False, serif: bool = False):
    if serif:
        name = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    else:
        name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size * SCALE)


def fdraw(d, xy, value, size, fill=INK, bold=False, serif=False, anchor=None):
    d.text((xy[0] * SCALE, xy[1] * SCALE), value, font=font(size, bold, serif), fill=fill, anchor=anchor)


def line(d, points, fill=INK, width=1):
    d.line([(int(x * SCALE), int(y * SCALE)) for x, y in points], fill=fill, width=max(1, width * SCALE), joint="curve")


def rect(d, box, fill=None, outline=None, width=1):
    d.rectangle(tuple(int(v * SCALE) for v in box), fill=fill, outline=outline, width=max(1, width * SCALE))


def wrapped(d, text, x, y, width, size, fill=INK, bold=False, serif=False, max_lines=None, leading=1.08):
    ft = font(size, bold, serif)
    words = text.split()
    rows, row = [], ""
    for word in words:
        trial = (row + " " + word).strip()
        if d.textlength(trial, font=ft) <= width * SCALE:
            row = trial
        else:
            if row:
                rows.append(row)
            row = word
    if row:
        rows.append(row)
    if max_lines and len(rows) > max_lines:
        rows = rows[:max_lines]
        while d.textlength(rows[-1] + "…", font=ft) > width * SCALE and rows[-1]:
            rows[-1] = rows[-1][:-1]
        rows[-1] += "…"
    for i, row in enumerate(rows):
        fdraw(d, (x, y + i * size * leading), row, size, fill, bold, serif)
    return y + len(rows) * size * leading


def illustration(d, box, glyph, accent):
    x, y, w, h = box
    rect(d, (x, y, x + w, y + h), fill=(219, 221, 215))
    # A restrained ink-and-accent vocabulary: horizon, black silhouette, one red mark.
    line(d, [(x, y + h - 41), (x + w, y + h - 41)], fill=accent, width=1)
    cx, cy = x + w * .52, y + h * .48
    if glyph in {"alert", "explosion"}:
        rect(d, (x + 26, y + h - 52, x + w - 45, y + h - 40), fill=INK)
        for i in range(3):
            line(d, [(cx + i * 6, cy + 25), (cx - 8 - i * 8, cy - 20 - i * 9)], fill=INK, width=2)
        d.ellipse(((cx - 23) * SCALE, (cy - 25) * SCALE, (cx + 23) * SCALE, (cy + 21) * SCALE), outline=accent, width=2 * SCALE)
        line(d, [(cx, cy + 2), (cx + 10, cy - 10), (cx + 3, cy - 32)], fill=RED, width=3)
    elif glyph in {"ship", "tanker", "flag"}:
        poly = [(x + 45, y + h - 68), (x + w - 50, y + h - 68), (x + w - 69, y + h - 44), (x + 69, y + h - 44)]
        d.polygon([(a * SCALE, b * SCALE) for a, b in poly], fill=INK)
        line(d, [(cx, y + 45), (cx, y + h - 68)], fill=INK, width=2)
        d.polygon([(cx, y + 49), (cx + 34, y + 60), (cx, y + 66)], fill=RED)
        for i in range(4):
            line(d, [(x + i * 21, y + h - 36), (x + 13 + i * 21, y + h - 27)], fill=BLUE, width=1)
    elif glyph in {"drone", "plane", "crash"}:
        line(d, [(cx - 50, cy + 20), (cx + 42, cy - 26)], fill=INK, width=3)
        line(d, [(cx - 13, cy + 2), (cx - 42, cy - 23)], fill=INK, width=2)
        line(d, [(cx + 8, cy - 9), (cx + 35, cy - 32)], fill=INK, width=2)
        d.ellipse(((cx - 6) * SCALE, (cy - 8) * SCALE, (cx + 7) * SCALE, (cy + 6) * SCALE), fill=RED)
        line(d, [(cx + 48, cy - 31), (cx + 12, cy - 6)], fill=RED, width=2)
    elif glyph in {"ballot", "court", "key"}:
        rect(d, (cx - 42, cy - 17, cx + 44, cy + 48), fill=(42, 39, 35))
        rect(d, (cx - 27, cy - 5, cx + 29, cy + 7), fill=PAPER)
        line(d, [(cx - 4, cy - 41), (cx - 4, cy - 16)], fill=INK, width=3)
        d.polygon([(cx - 18, cy - 42), (cx + 14, cy - 22), (cx - 4, cy - 18)], fill=RED)
    elif glyph in {"power", "money", "heart"}:
        line(d, [(cx - 30, y + h - 48), (cx + 5, cy - 21), (cx - 8, cy + 5), (cx + 42, y + h - 49)], fill=INK, width=4)
        d.ellipse(((cx - 8) * SCALE, (cy - 38) * SCALE, (cx + 24) * SCALE, (cy - 5) * SCALE), fill=RED)
        line(d, [(cx + 8, cy - 21), (cx + 8, cy + 22)], fill=INK, width=2)
    else:
        # Architecture / abstract map / orbital object.
        rect(d, (cx - 42, cy - 35, cx + 42, y + h - 42), fill=INK)
        for yy in range(int(cy - 20), int(y + h - 52), 14):
            for xx in range(int(cx - 31), int(cx + 31), 16):
                rect(d, (xx, yy, xx + 7, yy + 7), fill=PAPER)
        d.ellipse(((cx - 12) * SCALE, (cy - 12) * SCALE, (cx + 18) * SCALE, (cy + 18) * SCALE), fill=RED)
    # tactile registration specks make the stock feel printed, never photographic.
    for i in range(7):
        px = x + 8 + ((i * 37 + len(glyph) * 11) % max(1, int(w - 16)))
        py = y + 8 + ((i * 19 + len(glyph) * 7) % max(1, int(h - 16)))
        d.ellipse((px * SCALE, py * SCALE, (px + 1) * SCALE, (py + 1) * SCALE), fill=(178, 178, 168))


def draw_lead(d, story, box, index):
    x, y, w, h = box
    accent = REGION_COLORS.get(story.region, BLUE)
    illustration(d, (x, y, w, 170), story.glyph, accent)
    meta = f"{story.region} · {STATUS_LABEL[story.status]}"
    fdraw(d, (x, y + 178), meta, 8, accent, True, True)
    end = wrapped(d, story.headline, x, y + 195, w, 17, INK, True, True, 3, 0.97)
    wrapped(d, story.detail, x, end + 3, w, 9, MUTED, False, False, 2, 1.05)
    fdraw(d, (x, y + h - 6), story.source, 7, MUTED, False, True)


def draw_well(d, story, x, y, w, row_h, compact=False):
    accent = REGION_COLORS.get(story.region, BLUE)
    # No card outline: only a short editorial rule and a tiny glyph mark.
    line(d, [(x, y + 5), (x + 14, y + 5)], fill=accent, width=3)
    fdraw(d, (x + 20, y), f"{story.region} · {STATUS_LABEL[story.status]}", 7, accent, True, True)
    title_size = 7 if compact else 8
    wrapped(d, story.headline, x + 20, y + 12, w - 20, title_size, INK, True, True, 1 if compact else 2, .94)
    wrapped(d, story.detail, x + 20, y + row_h - (7 if compact else 10), w - 20, 5 if compact else 6, MUTED, False, False, 1, 1)
    # one primitive keyed to the story type, functioning as a newspaper marginal mark
    if story.glyph in {"water", "snow"}:
        for i in range(3):
            line(d, [(x + 1, y + 16 + i * 4), (x + 12, y + 16 + i * 4)], fill=accent, width=1)
    elif story.glyph in {"ballot", "key"}:
        rect(d, (x, y + 16, x + 11, y + 25), outline=accent, width=1)
    else:
        line(d, [(x + 6, y + 14), (x + 2, y + 25), (x + 10, y + 21), (x + 4, y + 21)], fill=accent, width=1)


def main():
    random.seed(34215311)
    im = Image.new("RGB", (W * SCALE, H * SCALE), PAPER)
    d = ImageDraw.Draw(im)
    # Fine, deterministic newsprint grain.
    for _ in range(3200):
        x, y = random.randrange(W * SCALE), random.randrange(H * SCALE)
        shade = random.choice([(221, 219, 208), (235, 233, 222), (202, 198, 185)])
        d.point((x, y), fill=shade)

    margin = 22
    line(d, [(margin, 23), (W - margin, 23)], width=4)
    fdraw(d, (margin, 35), "THE WORLD DAILY", 16, INK, True, True)
    fdraw(d, (W - margin, 36), "one day on earth, drawn by hand", 12, MUTED, False, True, "ra")
    fdraw(d, (W / 2, 53), "Sunday 22 November 2026", 46, INK, True, True, "ma")
    line(d, [(margin, 105), (W - margin, 105)], width=2)
    line(d, [(margin, 110), (W - margin, 110)], width=1)

    scoreboard = [("186", "DRONES"), ("0", "DEAL AT COP31"), ("74,742", "GAZA TOLL"), ("$12.1BN", "WFP ASK"), ("46", "STORIES / 7 REGIONS")]
    rect(d, (margin, 118, W - margin, 147), fill=RED)
    xx = margin + 4
    for i, (big, label) in enumerate(scoreboard):
        fdraw(d, (xx, 125), big, 15, PAPER, True)
        fdraw(d, (xx + (len(big) * 9 + 8), 126), label, 10, PAPER, True)
        xx += [116, 205, 216, 154, 0][i]
        if i < len(scoreboard) - 1:
            line(d, [(xx - 9, 124), (xx - 9, 141)], fill=PAPER, width=1)

    regions = []
    for s in STORIES:
        if s.region not in regions:
            regions.append(s.region)
    counts = [sum(1 for s in STORIES if s.region == r) for r in regions]
    band_y, band_h = 156, 19
    xx = margin
    for r, count in zip(regions, counts):
        ww = (W - 2 * margin) * count / len(STORIES)
        rect(d, (xx, band_y, xx + ww, band_y + band_h), fill=REGION_COLORS.get(r, BLUE))
        label = f"{r} {count}"
        if ww > 75:
            fdraw(d, (xx + 6, band_y + 3), label, 9, PAPER, True)
        xx += ww

    lead_y = 184
    gap = 8
    lead_w = (W - 2 * margin - gap * 3) / 4
    for i, s in enumerate(STORIES[:4]):
        draw_lead(d, s, (margin + i * (lead_w + gap), lead_y, lead_w, 302), i)

    rule_y = 496
    line(d, [(margin, rule_y), (W - margin, rule_y)], width=3)
    # Four unequal wells: a broad middle-east column, two mid columns, and a compact tail.
    cols = [(22, 264), (300, 255), (564, 222), (800, 202)]
    buckets = [[], [], [], []]
    for s in STORIES[4:]:
        if s.region == "MIDDLE EAST": buckets[0].append(s)
        elif s.region == "EUROPE": buckets[1].append(s)
        elif s.region == "SOUTH & EAST ASIA": buckets[2].append(s)
        else: buckets[3].append(s)
    col_names = ["MIDDLE EAST", "EUROPE", "SOUTH & EAST ASIA", "LATIN AMERICA / AFRICA"]
    for ci, ((x, w), stories) in enumerate(zip(cols, buckets)):
        fdraw(d, (x, 505), col_names[ci], 10, REGION_COLORS.get(stories[0].region, GREEN), True, True)
        row_h = 22 if ci == 3 else 31
        for j, story in enumerate(stories):
            draw_well(d, story, x, 523 + j * row_h, w, row_h, compact=(ci == 3))

    # Dispatch ribbon keeps the smallest stories legible without pretending they are cards.
    dispatch_y = 919
    line(d, [(margin, dispatch_y), (W - margin, dispatch_y)], width=1)
    fdraw(d, (margin, dispatch_y + 6), "DISPATCHES", 9, INK, True, True)
    tail = [s for s in STORIES[4:] if s not in sum(buckets, [])]
    # All stories are represented above; use the final three as a deliberate wire crawl.
    wire = STORIES[-5:]
    wx = 113
    for story in wire:
        snippet = f"{story.headline} — {story.source}"
        wrapped(d, snippet, wx, dispatch_y + 5, 168, 7, INK, False, False, 2, 1.1)
        wx += 177

    check_y = 970
    rect(d, (margin, check_y, W - margin, 1002), fill=(224, 220, 207))
    fdraw(d, (margin + 7, check_y + 7), "DATE CHECK", 9, RED, True, True)
    fdraw(d, (105, check_y + 7), "prior-day claims retained as context · not counted in today's leads", 8, MUTED, False, True)
    for i, (date, claim, region, verdict) in enumerate(DATE_CHECK[:3]):
        fdraw(d, (margin + 7 + i * 322, check_y + 18), f"{date}  {claim[:31]}…", 7, INK, False, False)

    im.resize((W, H), Image.Resampling.LANCZOS).save(OUT, optimize=False)
    print(OUT)


if __name__ == "__main__":
    main()

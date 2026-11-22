#!/usr/bin/env python3
"""news-image-20261121: one dense front page of 21 November 2026's world news.

36 stories from 7 regions on a 1024x1024 newspaper front page: one lead
(Iran strikes US bases in Bahrain) and a 4x9 grid of 35 more, plus a
"by the numbers" box. Every story was verified against real reporting
dated Saturday 21 November 2026 (OneTurn 21 Nov day report, Reuters, CNN,
WSJ, AP, Al Jazeera, The Hindu, UN News, IANS, France 24, Scientific
American, IntelChron 21 Nov brief, InformedClearly 21 Nov summary).
Pure Python 3.13 standard library (os, struct, zlib, math). No network,
deterministic: two runs write byte-identical output. Writes entry.png to
$MAKEFUN_OUTPUT_DIR or /output.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# ------------------------------------------------------------------ palette
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
RED = (222, 41, 16)
DARKRED = (150, 40, 30)
BLUE = (0, 87, 183)
YELLOW = (255, 215, 0)
SEA = (18, 92, 140)
TEAL = (14, 116, 120)
GREEN = (34, 139, 34)
ORANGE = (230, 126, 34)
GREY = (90, 90, 96)
PURPLE = (90, 50, 130)
IRAN_GREEN = (0, 128, 0)
IRAN_RED = (220, 0, 0)
BAHRAIN_RED = (206, 17, 38)


# ------------------------------------------------------------------ canvas
class Page:
    """An RGB page held as one flat bytearray; writes its own PNG."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bytes(bg) * (w * h))

    def dot(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = c

    def row(self, x0, x1, y, c):
        if y < 0 or y >= self.h:
            return
        a, b = max(0, x0), min(self.w - 1, x1)
        for x in range(a, b + 1):
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = c

    def col(self, x, y0, y1, c):
        if x < 0 or x >= self.w:
            return
        for y in range(max(0, y0), min(self.h - 1, y1) + 1):
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = c

    def box(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            self.row(x, x + w - 1, yy, c)

    def frame(self, x, y, w, h, c, t=1):
        for k in range(t):
            self.row(x, x + w - 1, y + k, c)
            self.row(x, x + w - 1, y + h - 1 - k, c)
            self.col(x + k, y, y + h - 1, c)
            self.col(x + w - 1 - k, y, y + h - 1, c)

    def poly(self, pts, c):
        """Scanline-fill a polygon given as [(x, y), ...]."""
        ys = [p[1] for p in pts]
        for y in range(max(0, int(min(ys))), min(self.h - 1, int(max(ys))) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.row(int(xs[i]), int(xs[i + 1]), y, c)

    def diamond(self, cx, cy, r, c):
        self.poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], c)

    def png(self):
        raw = b"".join(
            b"\x00" + bytes(self.buf[y * self.w * 3:(y + 1) * self.w * 3])
            for y in range(self.h))
        comp = zlib.compress(raw, 9)

        def chunk(typ, data):
            c = struct.pack(">I", len(data)) + typ + data
            return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ------------------------------------------------------------- 5x7 bitmap font
# One glyph = 7 rows; each row is a 5-bit mask, bit 4 = leftmost column.
GLYPHS = {
    "A": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "B": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    "C": [0x0F, 0x10, 0x10, 0x10, 0x10, 0x10, 0x0F],
    "D": [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
    "E": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    "F": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    "G": [0x0F, 0x10, 0x10, 0x17, 0x11, 0x11, 0x07],
    "H": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "I": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x1F],
    "J": [0x07, 0x01, 0x01, 0x01, 0x01, 0x11, 0x06],
    "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    "M": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
    "O": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "P": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    "Q": [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    "R": [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    "S": [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
    "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
    "X": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    "Y": [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    "Z": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
    "0": [0x0E, 0x13, 0x15, 0x19, 0x11, 0x11, 0x0E],
    "1": [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "2": [0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F],
    "3": [0x1E, 0x01, 0x01, 0x06, 0x01, 0x01, 0x1E],
    "4": [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    "5": [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
    "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    "7": [0x1F, 0x01, 0x02, 0x04, 0x04, 0x04, 0x04],
    "8": [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    "9": [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x0E],
    " ": [0, 0, 0, 0, 0, 0, 0],
    ".": [0, 0, 0, 0, 0, 0, 0x04],
    ",": [0, 0, 0, 0, 0, 0x04, 0x08],
    ":": [0, 0x04, 0, 0, 0, 0x04, 0],
    ";": [0, 0x04, 0, 0, 0, 0x04, 0x08],
    "'": [0x04, 0x04, 0x08, 0, 0, 0, 0],
    "-": [0, 0, 0, 0x0E, 0, 0, 0],
    "/": [0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10],
    "!": [0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04],
    "?": [0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04],
    "(": [0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02],
    ")": [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
    "%": [0x11, 0x12, 0x02, 0x04, 0x08, 0x09, 0x11],
    "+": [0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0],
    "$": [0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04],
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale if s else 0


def draw_text(pg, x, y, s, scale, color, align="left"):
    s = s.upper()  # the bitmap font only carries capitals, digits, punctuation
    if align == "center":
        x -= text_w(s, scale) // 2
    elif align == "right":
        x -= text_w(s, scale)
    for ch in s:
        g = GLYPHS.get(ch, GLYPHS[" "])
        for r in range(7):
            mask = g[r]
            for c in range(5):
                if mask & (1 << (4 - c)):
                    pg.box(x + c * scale, y + r * scale, scale, scale, color)
        x += 6 * scale


def wrap(s, max_w, scale):
    """Greedy word wrap; returns lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ stories
# (region, headline, summary, accent). Headlines wrap to at most 2 lines at
# scale 2 in a 231 px column; summaries to at most 2 lines at scale 1.
STORIES = [
    ("MARKETS", "AI SELL-OFF PUSHES US INTO CORRECTION",
     "AI and chip sell-off drags US stocks into correction.", PURPLE),
    ("N. AMERICA", "FBI AND USDA HACKED",
     "FBI probes hack of its crime database; USDA payments hit too.", NAVY),
    ("N. AMERICA", "DEMOCRATS WIN 259 HOUSE SEATS",
     "Midterm wave: biggest Democratic majority since 1990.", NAVY),
    ("N. AMERICA", "US LOSES MEASLES-FREE STATUS",
     "First measles death in Virginia in 2026; status lost.", DARKRED),
    ("N. AMERICA", "BAYER PAYS $7.25BN OVER ROUNDUP",
     "Judge validates deal settling all Roundup complaints.", PURPLE),
    ("N. AMERICA", "MAMDANI: CLOSE RIKERS BY 2032",
     "NYC mayor-elect plans to shut the Rikers Island jail.", NAVY),
    ("TECH", "GTA VI MAKES $3.79BN IN A DAY",
     "Rockstar: record first-day revenue, biggest launch ever.", PURPLE),
    ("TECH", "RIEMANN PROOF VERIFIED",
     "Lean and Mathlib verify AI-assisted Riemann proof.", PURPLE),
    ("EUROPE", "COP31 RUNS PAST DEADLINE",
     "Climate talks in Antalya go to overtime on fossil fuels.", GREEN),
    ("EUROPE", "DENMARK: RUSSIA MURDER PLOT",
     "Copenhagen blames Russian intel for rapper murder plot.", NAVY),
    ("EUROPE", "RUSSIAN SHIP ABLAZE OFF FINLAND",
     "Cargo vessel ablaze after drone strike; drifts into Finnish waters.", GREY),
    ("EUROPE", "FRANCE SEEKS UN ACTION ON MYANMAR",
     "Paris to seek Security Council meeting on ICJ ruling.", NAVY),
    ("EUROPE", "EU-INDONESIA DEAL SIGNED",
     "Trade pact agreed after ten years of talks.", BLUE),
    ("EUROPE", "EU BUDGET: 1.78TN EURO PLAN",
     "2028-2034 plan includes a 3% digital tax.", BLUE),
    ("EUROPE", "BELGIUM STRIKE TO GROUND ALL FLIGHTS",
     "Air traffic joins nationwide strike; all flights off Monday.", NAVY),
    ("EUROPE", "RUSSIAN MISSILE HITS KRYVYI RIH",
     "Strike on Zelensky's hometown kills 2, wounds dozens.", RED),
    ("MIDEAST", "TWO TANKERS HIT NEAR HORMUZ",
     "UKMTO: two tankers struck off Oman; strait shut.", TEAL),
    ("MIDEAST", "HOUTHIS HIT RIYADH SKYSCRAPER",
     "Missiles damage a tower in Riyadh's financial district.", ORANGE),
    ("MIDEAST", "BASRA POWER PLANT FIRE KILLS FOUR",
     "Blaze at Hartha plant kills 4, injures 35 in Iraq.", ORANGE),
    ("MIDEAST", "LEBANON: ISRAEL MUST WITHDRAW",
     "President demands Israeli pullout, decries Iran meddling.", NAVY),
    ("MIDEAST", "US, ISRAEL WEIGH NEW IRAN STRIKES",
     "CBS: Washington and Jerusalem weigh a third round of strikes.", NAVY),
    ("ASIA", "SUNEUNG EXAM CHEATING SCANDAL",
     "111 students caught cheating in South Korea's college exam.", NAVY),
    ("ASIA", "INDONESIA FIRES BURN 7.1M ACRES",
     "2026 fires cover an area 18 times the size of London.", SEA),
    ("ASIA", "AIR NIUGINI JET IN EMERGENCY LANDING",
     "Plane with 146 aboard lands in Philippines after engine fire.", SEA),
    ("ASIA", "AFGHAN MORTAR BLAST KILLS FOUR STUDENTS",
     "Old shell explodes in Afghanistan; four students killed.", DARKRED),
    ("ASIA", "QUAD, ASEAN SUMMITS: TAKEAWAYS",
     "The Hindu explains the Manila summits' key outcomes.", NAVY),
    ("S. ASIA", "BANGLADESH DENGUE: 3 MORE DEAD",
     "Dengue kills 3 more; 1,674 admitted in a day.", GREEN),
    ("S. ASIA", "IRAN PITCHES 3 PLANS AT SCO FORUM",
     "Iran proposes heritage networks at Delhi SCO forum.", NAVY),
    ("AFRICA", "NIGERIA BOAT CAPSIZE KILLS 24",
     "NEMA: 24 bodies recovered after funeral boat capsizes.", DARKRED),
    ("AFRICA", "S. AFRICA: 600 WOMEN KILLED",
     "Police: nearly 600 women killed in three months.", DARKRED),
    ("AFRICA", "ANC FIGHTS TO KEEP KEY CITIES",
     "South Africa's ANC battles to hold cities after poll setback.", NAVY),
    ("LATIN AM.", "MEXICO CAPTURES CHAPO ISIDRO",
     "FBI most-wanted cartel boss seized; 11 dead in clashes.", RED),
    ("LATIN AM.", "PERU QUAKE 6.9 SHAKES ANDES",
     "Magnitude 6.9 quake hits Peru; 152 homes uninhabitable.", ORANGE),
    ("LATIN AM.", "ARGENTINA OKAYS $50BN LNG PROJECT",
     "YPF-Eni-XRG deal is the biggest in Argentine history.", PURPLE),
    ("LATIN AM.", "HAITI: THREE DEAD AFTER BLAST",
     "Salvadoran troops hit by explosion; three dead.", RED),
]

LEAD_LINES = ["IRAN STRIKES US BASES", "IN BAHRAIN"]
LEAD_SUMMARY = ("Tehran says it hit two US positions; Bahrain reports "
                "an industrial fire, no injuries.")
LEAD_DATELINE = "MANAMA, BAHRAIN - SATURDAY 21 NOVEMBER 2026"

NUMBERS = [
    "$3.79BN GTA VI DAY ONE",
    "259 HOUSE SEATS",
    "111 CAUGHT CHEATING",
    "7.1M ACRES BURNED",
    "24 DEAD IN NIGERIA CAPSIZE",
]


def draw_flags(pg, x, y):
    """Three flags side by side, 96x64 each: Iran, USA, Bahrain."""
    # Iran: green / white / red bands, small red diamond for the emblem.
    pg.box(x, y, 96, 21, IRAN_GREEN)
    pg.box(x, y + 21, 96, 22, WHITE)
    pg.box(x, y + 43, 96, 21, IRAN_RED)
    pg.diamond(x + 48, y + 32, 7, IRAN_RED)
    pg.frame(x, y, 96, 64, INK, 1)
    # USA: seven stripes, blue canton, white star dots.
    ux = x + 104
    for i in range(7):
        pg.box(ux, y + i * 9, 96, 9 if i < 6 else 10,
               RED if i % 2 == 0 else WHITE)
    pg.box(ux, y, 38, 36, BLUE)
    for r in range(3):
        for c in range(4):
            pg.box(ux + 5 + c * 9, y + 5 + r * 11, 3, 3, WHITE)
    pg.frame(ux, y, 96, 64, INK, 1)
    # Bahrain: red field, white hoist with a five-point serrated edge.
    bx = x + 208
    pg.box(bx, y, 96, 64, BAHRAIN_RED)
    pts = [(bx, y), (bx + 30, y)]
    for k in range(5):
        pts.append((bx + 18, y + int((k + 0.5) * 64 / 5)))
        pts.append((bx + 30, y + int((k + 1) * 64 / 5)))
    pts += [(bx, y + 64)]
    pg.poly(pts, WHITE)
    pg.frame(bx, y, 96, 64, INK, 1)


# ------------------------------------------------------------------ layout
def cell(pg, x, y, w, h, story):
    region, headline, summary, accent = story
    pg.box(x, y, w, h, WHITE)
    pg.box(x, y, w, 4, accent)
    pg.frame(x, y, w, h, INK, 1)
    tx = x + 8
    draw_text(pg, tx, y + 9, region, 1, accent)
    for i, ln in enumerate(wrap(headline, w - 16, 2)[:2]):
        draw_text(pg, tx, y + 21 + i * 16, ln, 2, INK)
    for i, ln in enumerate(wrap(summary, w - 16, 1)[:2]):
        draw_text(pg, tx, y + 53 + i * 9, ln, 1, INK)


def numbers_box(pg, x, y, w, h):
    pg.box(x, y, w, h, WHITE)
    pg.box(x, y, w, 4, GOLD)
    pg.frame(x, y, w, h, INK, 1)
    draw_text(pg, x + 8, y + 9, "BY THE NUMBERS", 1, GOLD)
    for i, ln in enumerate(NUMBERS):
        draw_text(pg, x + 8, y + 22 + i * 9, ln, 1, INK)


def main():
    pg = Page(W, H, PAPER)

    # masthead
    pg.box(0, 0, W, 88, NAVY)
    draw_text(pg, W // 2, 12, "THE WORLD IN ONE DAY", 5, WHITE, "center")
    draw_text(pg, W // 2, 56,
              "SATURDAY 21 NOVEMBER 2026 - 36 STORIES, 7 REGIONS",
              2, GOLD, "center")
    pg.box(0, 88, W, 4, GOLD)

    # lead story: Iran strikes US bases in Bahrain
    # Content is shifted 12 px down so it sits vertically centred in the
    # 170 px panel (was top-heavy: 8 px above, 31 px below the dateline).
    pg.box(8, 92, 1008, 170, WHITE)
    pg.box(8, 92, 1008, 4, GOLD)
    pg.frame(8, 92, 1008, 170, INK, 1)
    draw_flags(pg, 20, 116)
    draw_text(pg, 68, 184, "IRAN", 1, INK, "center")
    draw_text(pg, 172, 184, "USA", 1, INK, "center")
    draw_text(pg, 276, 184, "BAHRAIN", 1, INK, "center")
    draw_text(pg, 336, 112, LEAD_LINES[0], 4, INK)
    draw_text(pg, 336, 144, LEAD_LINES[1], 4, INK)
    for i, ln in enumerate(wrap(LEAD_SUMMARY, 668, 2)[:2]):
        draw_text(pg, 336, 180 + i * 16, ln, 2, INK)
    draw_text(pg, 336, 236, LEAD_DATELINE, 1, GREY)

    # 4x9 dense grid: 35 stories + 1 numbers box
    cols, rows = 4, 9
    cw, chh, gap = 247, 73, 6
    gx0, gy0 = 8, 268
    for idx in range(cols * rows):
        col, row = idx % cols, idx // cols
        gx = gx0 + col * (cw + gap)
        gy = gy0 + row * (chh + gap)
        if idx < len(STORIES):
            cell(pg, gx, gy, cw, chh, STORIES[idx])
        else:
            numbers_box(pg, gx, gy, cw, chh)

    # footer
    pg.box(0, 978, W, 46, NAVY)
    draw_text(pg, W // 2, 986,
              "SOURCES: REUTERS - CNN - WSJ - AL JAZEERA - AP - ONETURN - BBC - THE HINDU - UN NEWS",
              1, WHITE, "center")
    draw_text(pg, W // 2, 1002,
              "INTELCHRON - INFORMEDCLEARLY - HORIZON - IANS - LE MONDE - FRANCE 24 - SCIENTIFIC AMERICAN",
              1, WHITE, "center")

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "entry.png"), "wb") as f:
        f.write(pg.png())


if __name__ == "__main__":
    main()

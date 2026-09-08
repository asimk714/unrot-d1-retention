#!/usr/bin/env python3
"""
Unrot D1 Retention — Final Deck PDF (fpdf2)
Builds a 7-page PDF that mirrors the PPTX design.
Uses DejaVu Sans (regular + algorithmic bold) for full Unicode support.
No screenshots — clean flow diagrams only (browser QA BLOCKED/NOT EXECUTED).
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos, Align

WORK = "/data/data/com.termux/files/home/unrot-d1-retention"
DECK = os.path.join(WORK, "deck")
os.makedirs(DECK, exist_ok=True)

DEJ = os.path.join(WORK, ".cache/uv/sdists-v9/pypi/pillow/12.3.0/07umJxf9440hmQG6/src/Tests/fonts/DejaVuSans/DejaVuSans.ttf")
if not os.path.exists(DEJ):
    # fallback search
    import glob
    hits = glob.glob("/data/data/com.termux/files/home/.cache/**/DejaVuSans.ttf", recursive=True)
    if hits:
        DEJ = hits[0]
print("DejaVu:", DEJ, "exists:", os.path.exists(DEJ))

# Try to find DejaVuSans-Bold.ttf for real bold; else use same ttf (fpdf2 algorithmic bold via style='B')
import glob as _g
BDEJ = None
bold_hits = _g.glob("/data/data/com.termux/files/home/.cache/**/DejaVuSans-Bold.ttf", recursive=True)
if bold_hits:
    BDEJ = bold_hits[0]
else:
    # Use same file, fpdf2 will synthesize bold
    BDEJ = DEJ
print("Bold font:", BDEJ, "exists:", os.path.exists(BDEJ))

FONT = "UnrotSans"
pdf = FPDF(orientation="L", unit="mm", format="A4")  # A4 landscape = 297×210mm
pdf.set_auto_page_break(auto=False)
pdf.set_margin(0)
pdf.add_font(FONT, "", DEJ, uni=True)
pdf.add_font(FONT, "B", BDEJ, uni=True)

# --- Colors (RGB 0-255) ---
BG      = (10, 10, 15)
CARD    = (18, 18, 26)
CARD2   = (26, 26, 36)
INVERSE = (245, 245, 247)
DIM     = (152, 152, 157)
DIMMER  = (99, 99, 102)
BLUE    = (0, 122, 255)
BLUE_D  = (0, 102, 214)
PURPLE  = (88, 86, 214)
ORANGE  = (255, 149, 0)
GREEN   = (52, 199, 89)
LINE    = (28, 28, 36)
LINE2   = (37, 37, 46)
WHITE   = (255, 255, 255)
REDBG   = (26, 18, 8)
REDTXT  = (255, 107, 107)

HW = 297.6  # page width landscape
HH = 210.0  # page height
MM = 1.0

def fin(mm):
    return int(mm * 2.834645669)  # mm → px at 72dpi... actually fpdf uses mm natively
## fpdf uses mm as unit; we work directly in mm.

# We'll define everything in mm.
# 13.333 in = 338.57 mm; 7.5 in = 190.5 mm
# But our page is 297.6 x 210.0 mm (16:9 landscape slightly larger than Letter).
# Let's use the actual page size.

PW = HW
PH = HH

def rect(x, y, w, h, fill=None, stroke=None, sw=0.2, rounded=False):
    if fill is not None:
        pdf.set_fill_color(*fill)
    else:
        pdf.set_fill_color(*BG)
    if stroke is not None:
        pdf.set_draw_color(*stroke)
        pdf.set_line_width(sw)
    else:
        pdf.set_draw_color(*BG)
        pdf.set_line_width(0)
    if rounded:
        # fpdf2 may not have round_rect; use rect with small corner approximation
        pdf.rect(x, y, w, h, style="DF" if fill is not None else "D")
    else:
        pdf.rect(x, y, w, h, style="DF" if fill is not None else "D")

def line_h(x, y, w, color, sw=0.15):
    pdf.set_draw_color(*color)
    pdf.set_line_width(sw)
    pdf.line(x, y, x+w, y)

def rrect(x, y, w, h, r, fill=None, stroke=None, sw=0.2):
    """Rounded rectangle using ellipse corners + rect body."""
    if fill is not None:
        pdf.set_fill_color(*fill)
    else:
        pdf.set_fill_color(*BG)
    if stroke is not None:
        pdf.set_draw_color(*stroke)
        pdf.set_line_width(sw)
    else:
        pdf.set_draw_color(*BG)
        pdf.set_line_width(0)
    # Draw as path: 4 lines + 4 arcs
    # Simplified: draw rect, then overlay curved corners with fill
    pdf.rect(x, y, w, h, style="DF" if fill is not None else "D")
    # If stroke only, skip arcs
    if fill is None and stroke is None:
        return
    # Draw filled rounded corners via circles
    rad = r
    if fill is not None:
        pdf.set_fill_color(*fill)
    # We'll just draw small white circles at corners to mask (cheat)
    # Actually let's not bother — use plain rect for cleaner rendering in fpdf2
    # The PPTX uses rounded; PDF will use sharp rect — acceptable, still clean.
    pdf.rect(x, y, w, h, style="DF" if fill is not None else "D")
    # Mask corners with white (BG) circles
    pdf.set_fill_color(*BG)
    if fill is None:
        pdf.set_fill_color(*BG)
    pdf.circle(x+rad, y+rad, rad, style="F")
    pdf.circle(x+w-rad, y+rad, rad, style="F")
    pdf.circle(x+rad, y+h-rad, rad, style="F")
    pdf.circle(x+w-rad, y+h-rad, rad, style="F")
    if fill is not None:
        # fill the center rect
        pdf.set_fill_color(*fill)
        pdf.rect(x+rad, y, w-2*rad, h, style="F")
        pdf.rect(x, y+rad, w, h-2*rad, style="F")

def txt(x, y, w, h, para, align=Align.L, font_size=11, color=INVERSE, bold=False):
    """para: string or list of (text, size, color_override, bold_override)."""
    pdf.set_font(FONT, "B" if bold else "", font_size)
    if isinstance(para, str):
        para = [(para, font_size, color, bold)]
    for item in para:
        if isinstance(item, tuple):
            t, sz, c, b = item
            pdf.set_font(FONT, "B" if b else "", sz)
            pdf.set_text_color(*c)
            pdf.set_xy(x, y)
            pdf.cell(w, 0, t, align=align, new_x=XPos.RIGHT, new_y=YPos.TOP)
            y = pdf.get_y()
        else:
            pdf.set_font(FONT, "B" if bold else "", font_size)
            pdf.set_text_color(*color)
            pdf.set_xy(x, y)
            pdf.cell(w, 0, item, align=align, new_x=XPos.RIGHT, new_y=YPos.TOP)
            y = pdf.get_y()

def tline(x, y, w, text, size=11, color=DIM, bold=False):
    """Single line of text."""
    pdf.set_font(FONT, "B" if bold else "", size)
    pdf.set_text_color(*color)
    pdf.set_xy(x, y)
    pdf.cell(w, 0, text, align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_text_color(*INVERSE)

def tmulti(x, y, w, h, lines, size=11, color=DIM, bold=False, align=Align.L):
    """Multi-line block. lines: list of strings."""
    pdf.set_font(FONT, "B" if bold else "", size)
    pdf.set_text_color(*color)
    yy = y
    for i, ln in enumerate(lines):
        pdf.set_xy(x, yy)
        pdf.multi_cell(w, size*0.35, ln, align=align, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        yy = pdf.get_y()
    pdf.set_text_color(*INVERSE)

def circle(x, y, r, fill=None, stroke=None):
    if fill is not None:
        pdf.set_fill_color(*fill)
    else:
        pdf.set_fill_color(*BG)
    if stroke is not None:
        pdf.set_draw_color(*stroke)
    pdf.circle(x, y, r, style="F" if fill is not None else "D")

def num_circle(x, y, r, n, fill=BLUE, txt_color=WHITE, txt_size=14):
    circle(x, y, r, fill=fill)
    pdf.set_font(FONT, "B", txt_size)
    pdf.set_text_color(*txt_color)
    txt_s = str(n)
    tw = pdf.get_string_width(txt_s)
    pdf.set_xy(x - tw/2, y - txt_size*0.35/2)
    pdf.cell(tw, txt_size*0.35, txt_s, align=Align.C, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_text_color(*INVERSE)

def down_arrow(x, y, color=BLUE, size=6):
    """Down arrow using triangle."""
    import math
    cx, cy, h, w = x, y, size*0.8, size*0.6
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*BG)
    pdf.set_line_width(0)
    # triangle pointing down
    p = [(cx, cy), (cx-w/2, cy+h), (cx+w/2, cy+h)]
    pdf.polygon(p, style="F")

def right_arrow(x, y, color=DIMMER, size=3):
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*BG)
    pdf.set_line_width(0)
    p = [(x, y), (x+size*0.8, y-size/3), (x+size*0.8, y+size/3)]
    pdf.polygon(p, style="F")

def bar(x, y, h, color):
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*BG)
    pdf.set_line_width(0)
    pdf.rect(x, y, 1.5, h, style="F")

def chip(x, y, text, bg_color, txt_color=WHITE, w=None, h=2.6, size=9):
    if w is None:
        pdf.set_font(FONT, "", size)
        w = pdf.get_string_width(text) + 3
    pdf.set_fill_color(*bg_color)
    pdf.set_draw_color(*BG)
    pdf.set_line_width(0)
    pdf.set_font(FONT, "", size)
    pdf.set_text_color(*txt_color)
    pdf.set_xy(x, y)
    pdf.cell(w, h, text, align=Align.C, new_x=XPos.RIGHT, new_y=YPos.TOP)
    # fill background
    pdf.set_fill_color(*bg_color)
    pdf.rect(x, y, w, h, style="F")
    pdf.set_xy(x, y)
    pdf.cell(w, h, text, align=Align.C, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_text_color(*INVERSE)

def chip_trans(x, y, text, bg_color, txt_color=WHITE, w=None, h=2.6, size=9):
    """Semi-transparent chip (drawn on top of existing, with slight bg)."""
    if w is None:
        pdf.set_font(FONT, "", size)
        w = pdf.get_string_width(text) + 3
    pdf.set_fill_color(*bg_color)
    pdf.set_draw_color(*BG)
    pdf.set_line_width(0.1)
    pdf.rect(x, y, w, h, style="DF")
    pdf.set_font(FONT, "", size)
    pdf.set_text_color(*txt_color)
    pdf.set_xy(x, y)
    pdf.cell(w, h, text, align=Align.C, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_text_color(*INVERSE)

def footnote(x, y, text, color=DIMMER, size=7):
    tline(x, y, PW-x, text, size=size, color=color)

def page_bg():
    pdf.set_fill_color(*BG)
    pdf.set_draw_color(*BG)
    pdf.rect(0, 0, PW, PH, style="F")
    pdf.set_fill_color(*BG)
    pdf.set_draw_color(*BG)
    pdf.set_line_width(0)

def eyebrow(x, y, text, color=DIM, size=8):
    bar(x, y+1.6, 1.2, color)
    tline(x+1.2, y+0.9, PW-x, text, size=size, color=color, bold=True)

def slide_title(x, y, text, size=22, color=WHITE, accent=BLUE, accent_w=20):
    tline(x, y, PW-x, text, size=size, color=color, bold=True)
    line_h(x, y+7.5, accent_w, accent, sw=0.25)

# =========================================================================
# SLIDE 1 — TITLE
# =========================================================================
pdf.add_page()
page_bg()

# Left accent block (full height)
pdf.set_fill_color(*BLUE)
pdf.set_draw_color(*BG)
pdf.set_line_width(0)
pdf.rect(0, 0, 4.0, PH, style="F")

# Top eyebrow
tline(8.0, 5.5, PW-8, "PRODUCT MANAGEMENT CASE STUDY  ·  SEPTEMBER 2026", size=7.5, color=DIM, bold=True)

# Main title
pdf.set_xy(8.0, 11.8)
pdf.set_font(FONT, "", 36)
pdf.set_text_color(*WHITE)
pdf.cell(70, 12, "UNROT", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.set_font(FONT, "B", 36)
pdf.set_text_color(*BLUE)
pdf.cell(90, 12, "D1 RETENTION", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)

# Accent divider under subtitle
line_h(8.0, 25.0, 17.5, BLUE, sw=0.3)

# Subtitle
pdf.set_font(FONT, "", 14)
pdf.set_text_color(*DIM)
pdf.set_xy(8.0, 26.0)
pdf.multi_cell(80, 5, "\u201cDesigning the next reason to come back\u201d", align=Align.L, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# KPI cards
kpi_y = 36.5
kpi_w = 33.0; kpi_gap = 2.5; start_x = 8.0
kpis = [
    ("CURRENT D1", "16%", "Assignment baseline", DIM),
    ("BENCHMARK", "22%", "Assignment context — not achieved", DIM),
    ("TIMEBOX", "4 weeks", "1 Product Designer + 2 Engineers", DIM),
]
# We'll use 3 cards across the width
total_w = 3*kpi_w + 2*kpi_gap
offset_x = (PW - total_w) / 2
for i, (label, value, sub, col) in enumerate(kpis):
    x = offset_x + i*(kpi_w+kpi_gap)
    rrect(x, kpi_y, kpi_w, 13.5, 1.8, fill=CARD, stroke=LINE)
    tline(x+2.2, kpi_y+1.8, kpi_w-4, label, size=7, color=DIM, bold=True)
    pdf.set_xy(x+2.2, kpi_y+5.0)
    pdf.set_font(FONT, "B", 27)
    pdf.set_text_color(*BLUE)
    pdf.cell(kpi_w-4, 8, value, align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font(FONT, "", 8)
    pdf.set_text_color(*DIMMER)
    pdf.set_xy(x+2.2, kpi_y+11.2)
    pdf.multi_cell(kpi_w-4, 3, sub, align=Align.L, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# Thesis
bar(8.0, 56.5, 5.5, ORANGE)
tline(9.2, 55.5, PW-9.2, "PRODUCT THESIS:", size=7, color=ORANGE, bold=True)
tline(9.2, 58.5, PW-9.2, "\u201cTomorrow\u2019s 5-Minute Mission\u201d — make tomorrow\u2019s value concrete before session end", size=10, color=WHITE)

# Footer note
tline(8.0, 68.0, PW-8, "Product hypothesis + interaction prototype + experiment plan  ·  D1 Pull package: C3 + C2 + C4 + C1", size=6.5, color=DIMMER)
tline(8.0, 70.0, PW-8, "Note: 22% is the assignment benchmark provided as context. It is not a measured result, guaranteed target, or observed industry figure.", size=5.5, color=DIMMER)

# =========================================================================
# SLIDE 2 — PROBLEM & DIAGNOSIS
# =========================================================================
pdf.add_page()
page_bg()
slide_title(8.0, 5.5, "Where might Day 1 retention be breaking?", accent=BLUE)
eyebrow(8.0, 4.0, "01  /  PROBLEM & DIAGNOSIS")

# Left: funnel visual
fx = 8.0; fw = 55.0
tline(fx, 13.5, fw, "THE GAP", size=7, color=DIM, bold=True)

# big 16% card
rrect(fx, 15.5, fw, 9.8, 1.6, fill=CARD, stroke=LINE)
tline(fx+2.2, 16.0, 28, "16%", size=27, color=BLUE, bold=True)
tline(fx+2.2, 20.2, 28, "current D1 retention", size=7, color=DIM)
# right side: down arrow + 22%
right_arrow(fx+44, 19.5, color=DIMMER, size=4)
tline(fx+36, 17.2, 18, "\u2193", size=12, color=DIMMER, bold=True)
tline(fx+36, 18.5, 18, "target context", size=5.5, color=DIMMER)
tline(fx+36, 20.0, 18, "22%", size=14, color=WHITE, bold=True)
tline(fx+36, 22.0, 18, "assignment benchmark", size=5.5, color=DIMMER)

# footnote below
tline(fx, 25.8, fw, "16% = assignment-provided baseline. 22% = assignment benchmark provided as context, not a measured or guaranteed target.", size=5.5, color=DIMMER)

# working hypothesis card
hy_y = 27.5
rrect(fx, hy_y, fw, 13.5, 1.6, fill=CARD2, stroke=BLUE, sw=0.15)
bar(fx, hy_y, 13.5, BLUE)
tline(fx+2.2, hy_y+1.2, fw-4, "WORKING HYPOTHESIS", size=7, color=BLUE, bold=True)
tmulti(fx+2.2, hy_y+3.5, fw-4, 6, ["New users may complete a reasonable first session but leave without a concrete reason to return."], size=8.5, color=WHITE)
bar(fx+2.2, hy_y+9.5, 3.0, ORANGE)
tline(fx+3.4, hy_y+9.3, fw-5, "Not yet validated by cohort data.", size=6.5, color=DIMMER)

# three mechanisms
mech_y = hy_y + 14.0
tline(fx, mech_y, fw, "THREE HYPOTHESIZED MISSING PULL SIGNALS", size=7, color=DIM, bold=True)
mechs = [
    ("1", "No explicit next action", "User finishes session without seeing what to do next — no open loop."),
    ("2", "Weak early progress signal", "Streak and progress feel too new to matter on Day 1."),
    ("3", "No strong D1 return cue", "No well-timed external prompt brings the user back."),
]
my = mech_y+2.0
for i, (n, t, d) in enumerate(mechs):
    yy = my + i*3.4
    num_circle(fx+0.5, yy+0.7, 2.2, n, fill=BLUE, txt_size=8)
    tline(fx+2.5, yy, fw-3, t, size=8, color=WHITE, bold=True)
    tline(fx+2.5, yy+2.0, fw-3, d, size=6.5, color=DIM)

# Right: unknowns
rx = 68.0; rw = 23.0; ry = 13.5; rh = 160.0
rrect(rx, ry, rw, rh, 1.5, fill=CARD, stroke=LINE)
tline(rx+2.0, ry+1.4, rw-4, "WHAT WE DON\u2019T KNOW", size=7.5, color=ORANGE, bold=True)
tline(rx+2.0, ry+3.0, rw-4, "These are unknowns — not findings. They frame what Week 0 must resolve.", size=6, color=DIMMER)
unknowns = [
    ("First-session funnel", "How many new users reach first value at all? Where is the biggest drop-off?"),
    ("D1 by entry path", "Does D1 differ by first action — lesson vs news vs interview prep vs browse-only?"),
    ("Notification exposure", "Are new users receiving any Day 1 prompt? What is the opt-in rate?"),
    ("Segment-level retention", "By acquisition source, device, intent — is 16% uniform or dragged by a segment?"),
    ("Diagnostics", "Crash rate on first session, onboarding completion, session definition, timezone handling."),
]
uy = ry+4.5
for i, (t, d) in enumerate(unknowns):
    yy = uy + i*7.5
    circle(rx+2.0, yy+0.7, 0.9, fill=PURPLE)
    tline(rx+2.0, yy, rw-2, t, size=8, color=WHITE, bold=True)
    tline(rx+2.0, yy+2.8, rw-2, d, size=6, color=DIM)

tline(8.0, 198.5, PW-8, "Source: research/problem-framing.md, research/product-teardown.md, research/measurement-model.md. Classifications: HYPOTHESIS / UNKNOWN.", size=5.5, color=DIMMER)

# =========================================================================
# SLIDE 3 — SOLUTION
# =========================================================================
pdf.add_page()
page_bg()
slide_title(8.0, 5.5, "TOMORROW\u2019S 5-MINUTE MISSION", accent=ORANGE)
eyebrow(8.0, 4.0, "02  /  SOLUTION")

fx = 8.0; fw = 63.0
tline(fx, 13.5, fw, "THE EXPERIENCE — FROM TODAY TO DAY 1", size=7, color=DIM, bold=True)

# TODAY box
rrect(fx, 15.3, fw, 3.6, 1.2, fill=CARD2, stroke=LINE2)
tline(fx+2.0, 15.8, fw-4, "TODAY — FIRST SESSION", size=8, color=ORANGE, bold=True)

steps_today = [
    "New user completes\nfirst lesson",
    "Sees tomorrow\u2019s\n5-minute mission",
    "Optionally schedules\na reminder (C3)",
]
sy = 19.5
for i, st in enumerate(steps_today):
    yy = sy + i*7.0
    rrect(fx, yy, fw, 5.8, 1.4, fill=CARD, stroke=LINE)
    tmulti(fx+2.0, yy+0.8, fw-4, 4, [st], size=7.5, color=WHITE, align=Align.C)
    if i < 2:
        down_arrow(fx+fw/2, yy+5.8, color=BLUE, size=5)

# big arrow to DAY 1
d1y = sy+3*7.0+0.5
down_arrow(fx+fw/2, d1y, color=ORANGE, size=5)
tline(fx+2.0, d1y+4.5, fw-4, "next calendar day", size=5.5, color=DIMMER)

# DAY 1 box
d1_box_y = d1y+5.5
rrect(fx, d1_box_y, fw, 3.6, 1.2, fill=CARD2, stroke=LINE2)
tline(fx+2.0, d1_box_y+0.5, fw-4, "DAY 1 — RETURN", size=8, color=GREEN, bold=True)

steps_d1 = [
    "Receives D1 return cue\n(C1 notification)",
    "Opens directly into\nnext mission",
    "Continues the habit\n(streak = 2)",
]
sy2 = d1_box_y+4.0
for i, st in enumerate(steps_d1):
    yy = sy2 + i*5.8
    rrect(fx, yy, fw, 4.8, 1.2, fill=CARD, stroke=LINE)
    tmulti(fx+2.0, yy+0.6, fw-4, 4, [st], size=7.5, color=WHITE, align=Align.C)
    if i < 2:
        down_arrow(fx+fw/2, yy+4.8, color=GREEN, size=4)

# Right: 4 components
rx = 76.0; rw = 27.0; ry = 13.5
tline(rx, ry, rw, "FOUR COORDINATED COMPONENTS", size=7, color=DIM, bold=True)
comps = [
    ("C3", "Reminder / opt-in", "Optimized notification permission prompt during onboarding. Enabler — raises the addressable population for C1.", BLUE),
    ("C2", "Next-step mission", "End-of-first-session screen shows tomorrow\u2019s concrete 5-minute mission — an internal open loop at the moment of exit.", PURPLE),
    ("C4", "Streak / progress framing", "\u201cYour streak starts today\u201d — makes the 1-day streak feel like something to protect, not just a number.", ORANGE),
    ("C1", "D1 notification / deep link", "Day 1 push: \u201cYour daily AI lesson is ready\u201d with a deep link to today\u2019s content. The external D1 trigger.", GREEN),
]
cy2 = ry+2.2
for i, (cid, title, desc, col) in enumerate(comps):
    yy = cy2 + i*9.8
    rrect(rx, yy, rw, 8.8, 1.4, fill=CARD, stroke=LINE)
    bar(rx, yy, 8.8, col)
    chip(rx+2.0, yy+1.3, cid, col, h=2.8, size=8)
    tline(rx+5.5, yy+1.4, rw-7, title, size=8, color=WHITE, bold=True)
    tmulti(rx+2.0, yy+4.2, rw-4, 4, [desc], size=6.5, color=DIM)

# hypothesis strip
hy2_y = cy2+4*9.8+0.2
rrect(rx, hy2_y, rw, 5.5, 1.2, fill=CARD2, stroke=BLUE, sw=0.15)
tline(rx+2.0, hy2_y+0.8, rw-4, "Hypothesis being tested:", size=6.5, color=BLUE, bold=True)
tmulti(rx+2.0, hy2_y+2.0, rw-4, 3, ["Making tomorrow\u2019s value concrete before session end increases D1 return."], size=7, color=WHITE)

tline(8.0, 198.5, PW-8, "Package: C3 + C2 + C4 + C1. These are coordinated, not standalone. Source: research/interventions.md, research/prd.md.", size=5.5, color=DIMMER)

# =========================================================================
# SLIDE 4 — PROTOTYPE
# =========================================================================
pdf.add_page()
page_bg()
slide_title(8.0, 5.5, "From hypothesis to interaction", accent=BLUE)
eyebrow(8.0, 4.0, "03  /  PROTOTYPE")

# Status banner
rrect(8.0, 13.2, PW-16, 3.6, 1.2, fill=REDBG, stroke=ORANGE, sw=0.15)
tline(9.0, 13.7, PW-18, "INTERACTION PROTOTYPE — NOT PRODUCTION", size=7.5, color=ORANGE, bold=True)
pdf.set_font(FONT, "", 6.5)
pdf.set_text_color(*DIM)
pdf.set_xy(22.0, 13.7)
pdf.cell(0, 3.2, "     ·     Simulates analytics events locally in-browser.", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.set_text_color(*INVERSE)

fx = 8.0; fw = PW-16

# 4 state cards
card_w = (fw - 3*0.8) / 4; card_gap = 0.8; card_h = 20.5; card_y = 17.5
states = [
    ("1", "Onboarding / reminder choice", BLUE,
     ["\u201cStay ahead, automatically\u201d", "Toggle: daily lesson reminders", "Value-forward opt-in prompt (C3)"]),
    ("2", "Lesson experience", PURPLE,
     ["Today\u2019s concept card", "Start \u2192 read \u2192 mark complete", "Progress bar + completion signal"]),
    ("3", "End-of-session next mission", ORANGE,
     ["\u201cLesson complete!\u201d", "Streak: 1 day — \u201cDon\u2019t let it go cold\u201d", "\u201cTomorrow\u2019s concept is ready\u201d → next lesson card"]),
    ("4", "D1 return / notification", GREEN,
     ["\u201cYour daily AI lesson is ready\u201d", "Tap → deep-link to today\u2019s content", "Streak: 2 days — \u201cKeep it alive\u201d"]),
]
for i, (num, title, col, lines) in enumerate(states):
    x = fx + i*(card_w+card_gap)
    rrect(x, card_y, card_w, card_h, 1.3, fill=CARD, stroke=LINE)
    rect(x, card_y, card_w, 0.5, fill=col)
    num_circle(x+1.5, card_y+1.8, 2.2, num, fill=col, txt_size=9)
    tline(x+3.5, card_y+1.4, card_w-5, title, size=7.5, color=WHITE, bold=True)
    line_h(x+1.2, card_y+6.3, card_w-2.4, LINE, sw=0.1)
    ly = card_y+7.5
    for ln in lines:
        tline(x+1.2, ly, card_w-2.4, "\u2022  "+ln, size=6.5, color=DIM)
        ly += 2.2

# Key intervention screen mock
mx = fx; my = card_y+card_h+1.0; mw = fw; mh = 12.5
rrect(mx, my, mw, mh, 1.3, fill=CARD2, stroke=LINE2)
bar(mx, my, mh, ORANGE)
tline(mx+2.0, my+0.9, mw-4, "KEY INTERVENTION SCREEN — END OF FIRST SESSION (C2 + C4)", size=6.5, color=ORANGE, bold=True)

col_w = (mw - 2*0.3) / 3; col_gap = 0.3
col_y = my+3.5; col_h = 8.5

# Col 0: streak frame
cx = mx+0.2
rrect(cx, col_y, col_w, col_h, 1.0, fill=CARD, stroke=LINE)
tline(cx+0.8, col_y+0.5, col_w-1.6, "STREAK FRAME", size=5, color=DIM, bold=True)
pdf.set_xy(cx+0.8, col_y+1.2)
pdf.set_font(FONT, "", 16)
pdf.set_text_color(*ORANGE)
pdf.cell(0, 6, "\u2605", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.set_font(FONT, "B", 9)
pdf.set_text_color(*WHITE)
pdf.set_xy(cx+0.8, col_y+4.0)
pdf.cell(0, 4, "1 day", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)

# Col 1: streak message
cx = mx+0.2+col_w+col_gap
rrect(cx, col_y, col_w, col_h, 1.0, fill=CARD, stroke=LINE)
tline(cx+0.8, col_y+0.5, col_w-1.6, "STREAK MESSAGE", size=5, color=DIM, bold=True)
tmulti(cx+0.8, col_y+1.5, col_w-1.6, 5, ["Don\u2019t let your streak", "go cold.", "Come back tomorrow to", "keep it alive."], size=6.5, color=WHITE)
pdf.set_font(FONT, "", 5.5)
pdf.set_text_color(*DIM)
pdf.set_xy(cx+0.8, col_y+6.0)
pdf.cell(0, 2.5, "(just 5 minutes)", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)

# Col 2: next-step cue
cx = mx+0.2+2*(col_w+col_gap)
rrect(cx, col_y, col_w, col_h, 1.0, fill=CARD, stroke=LINE)
tline(cx+0.8, col_y+0.5, col_w-1.6, "NEXT-STEP CUE (C2)", size=5, color=DIM, bold=True)
pdf.set_font(FONT, "B", 6.5)
pdf.set_text_color(*BLUE)
pdf.set_xy(cx+0.8, col_y+1.3)
pdf.cell(0, 2.5, "\u2192 Tomorrow\u2019s concept is ready", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.set_font(FONT, "", 5.5)
pdf.set_text_color(*DIM)
pdf.set_xy(cx+0.8, col_y+3.0)
pdf.cell(0, 2.5, "Next lesson card preview", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.set_font(FONT, "", 5)
pdf.set_text_color(*DIMMER)
pdf.set_xy(cx+0.8, col_y+5.0)
pdf.multi_cell(col_w-1.6, 2, "Tap to preview tomorrow's mission without leaving the app.", align=Align.L, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# analytics events row
ey2 = my+mh+0.8
rrect(fx, ey2, fw, 3.2, 1.0, fill=CARD, stroke=LINE)
tline(fx+1.2, ey2+0.4, fw-2.4, "SIMULATED ANALYTICS EVENTS", size=5.5, color=DIM, bold=True)
events = ["lesson_completed", "session_end", "notification_scheduled", "notification_sent", "notification_opened", "session_start_d1"]
ev_w = (fw - 2.4 - 5*1.5) / 6
for i, ev in enumerate(events):
    ex = fx+1.2 + i*(ev_w+1.5)
    chip_trans(ex, ey2+1.2, ev, CARD2, txt_color=BLUE, w=ev_w, h=2.0, size=5.5)

# Critical footnotes
tline(8.0, ey2+4.0, PW-8, "Source: prototype/index.html — 4 screen states demonstrated. This is an interaction prototype, not a production build.", size=5, color=DIMMER)
tline(8.0, ey2+5.0, PW-8, "CRITICAL: Browser runtime validation: BLOCKED / NOT EXECUTED in this environment. Prototype events are simulated and are NOT measured retention results.", size=5.5, color=REDTXT, bold=True)

# =========================================================================
# SLIDE 5 — MEASUREMENT & EXPERIMENT
# =========================================================================
pdf.add_page()
page_bg()
slide_title(8.0, 5.5, "How we\u2019d know whether it works", accent=BLUE)
eyebrow(8.0, 4.0, "04  /  MEASUREMENT & EXPERIMENT")

# Primary metric
pm_y = 13.5
rrect(8.0, pm_y, PW-16, 6.2, 1.2, fill=CARD2, stroke=BLUE, sw=0.15)
tline(9.0, pm_y+0.8, 28, "PRIMARY METRIC", size=6, color=BLUE, bold=True)
pdf.set_xy(9.0, pm_y+2.2)
pdf.set_font(FONT, "B", 14)
pdf.set_text_color(*WHITE)
pdf.cell(0, 5, "D1 RETENTION", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
line_h(30.0, pm_y+1.0, 0.5, BLUE, sw=0.2)
tmulti(32.0, pm_y+0.8, 80.0, 5, ["Day-1 return rate: % of new users who complete a session on Day 0 and return for any session on the next calendar day.", "Measured by weekly cohort. Baseline range TBD in Week 0 — not just the 16% point."], size=7, color=DIM)
pdf.set_text_color(*INVERSE)

# Funnel
fy = 21.0
tline(8.0, fy, PW-8, "MEASUREMENT FUNNEL", size=7, color=DIM, bold=True)
funnel = [
    ("New user", BLUE, "Day-0 cohort entry"),
    ("First value", PURPLE, "Lesson / news / interview"),
    ("Lesson completion", PURPLE, "Completed state reached"),
    ("Session end", ORANGE, "has_next_action_visible, streak"),
    ("Notification scheduled", BLUE, "If opt-in (C1 enabler)"),
    ("Notification opened", BLUE, "Deep-link tap on D1"),
    ("D1 session", GREEN, "session_start on D1"),
]
step_w = 14.5; step_gap = 0.8; step_x0 = 8.0; step_y = fy+2.0
for i, (name, col, desc) in enumerate(funnel):
    sx = step_x0 + i*(step_w+step_gap)
    rrect(sx, step_y, step_w, 6.0, 1.2, fill=CARD, stroke=col, sw=0.15)
    rect(sx, step_y, step_w, 0.5, fill=col)
    tline(sx+1.0, step_y+0.5, step_w-2, name, size=7.5, color=col if col!=PURPLE else WHITE, bold=True)
    tline(sx+1.0, step_y+2.8, step_w-2, desc, size=4.5, color=DIMMER)

for i in range(len(funnel)-1):
    ax = step_x0 + (i+1)*step_w + i*step_gap + step_gap/2 - 1.0
    right_arrow(ax, step_y+3.0, color=DIMMER, size=2.5)

# metrics grid
gy = step_y+7.2
tline(8.0, gy, 40, "SECONDARY / DIAGNOSTIC / GUARDRAILS", size=7, color=DIM, bold=True)
metrics = [
    ("SECONDARY", BLUE, ["First-session completion rate", "Return-session quality (duration, value on D1)"]),
    ("DIAGNOSTIC", PURPLE, ["Notification exposure / open rate", "Next-action visibility at session end", "D1 by first action / entry path"]),
    ("GUARDRAILS", ORANGE, ["Notification opt-out / dismissal rate", "Uninstall rate", "D7 retention (if volume allows)"]),
]
col_w2 = 27.0; col_gap2 = 1.5; col_start2 = 8.0
for ci, (cat, col, items) in enumerate(metrics):
    cx = col_start2 + ci*(col_w2+col_gap2)
    rrect(cx, gy+1.5, col_w2, 10.5, 1.2, fill=CARD, stroke=LINE)
    rect(cx, gy+1.5, col_w2, 0.5, fill=col)
    tline(cx+1.2, gy+1.7, col_w2-2.4, cat, size=5.5, color=col, bold=True)
    iy = gy+2.8
    for it in items:
        tline(cx+1.2, iy, col_w2-2.4, "\u2022  "+it, size=6, color=DIM)
        iy += 2.0

# experiment design
ex_y = gy+12.5
rrect(8.0, ex_y, PW-16, 8.0, 1.2, fill=CARD2, stroke=LINE2)
tline(9.0, ex_y+0.6, 18, "EXPERIMENT DESIGN", size=6, color=BLUE, bold=True)
tline(9.0, ex_y+1.5, 15, "CONTROL", size=8, color=DIMMER, bold=True)
tmulti(9.0, ex_y+2.5, 30, 3, ["Current experience — no D1 Pull intervention."], size=6.5, color=DIM, align=Align.L)
line_h(56.0, ex_y+3.0, 5.5, LINE, sw=0.15)
tline(58.0, ex_y+2.8, 5.5, "VS", size=6.5, color=DIMMER, bold=True)
pdf.set_xy(65.0, ex_y+1.5)
pdf.set_font(FONT, "B", 8)
pdf.set_text_color(*GREEN)
pdf.cell(25, 3.5, "TREATMENT", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.set_font(FONT, "", 6.5)
pdf.set_text_color(*DIM)
pdf.set_xy(65.0, ex_y+2.5)
pdf.multi_cell(25, 2.5, "D1 Pull package — C3 + C2 + C4 + C1.", align=Align.L, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
tline(9.0, ex_y+5.0, PW-18, "Measure by weekly cohort. Segment every D1 read by first action / entry path / notification trigger.", size=5.5, color=DIMMER)

tline(8.0, 198.5, PW-8, "Source: research/measurement-model.md, research/prd.md. No sample size or expected lift is stated — both are TBD from Week 0 cohort data.", size=5.5, color=DIMMER)

# =========================================================================
# SLIDE 6 — ADVERSARIAL VIEW
# =========================================================================
pdf.add_page()
page_bg()
slide_title(8.0, 5.5, "What could prove us wrong?", accent=ORANGE)
eyebrow(8.0, 4.0, "05  /  ADVERSARIAL VIEW")

fx = 8.0; fw = PW-16
tline(fx, 13.3, fw, "FOUR COUNTER-DIAGNOSES", size=7, color=DIM, bold=True)
counters = [
    ("ACTIVATION PROBLEM", BLUE,
     "New users never reach first value — low first-session completion. A return cue can't help users who never got value. Fix: activation, not D1 pull.",
     "Revealed by: first-value achievement rate (measurement model Stage 3)."),
    ("AUDIENCE MISMATCH", PURPLE,
     "A large share of new users arrive from low-intent channels. The 16% reflects who is arriving, not what the product does. Fix: acquisition quality or onboarding qualification.",
     "Revealed by: D1-by-source segmentation."),
    ("CONTENT / VALUE PROBLEM", ORANGE,
     "First-session content doesn't deliver value — wrong topic, too shallow, doesn't match the user's job. A notification brings them back to the same low-value experience.",
     "Revealed by: lesson completion rate, time-in-lesson, D1-by-first-action correlation."),
    ("NOVELTY EFFECT", GREEN,
     "First sessions are inflated by novelty. The 84% who don't return are users whose only motive was \u201cI installed something new.\u201d No push creates a return reason for them.",
     "Revealed by: D1 of high-intent cohort vs cold store traffic."),
]
card_w3 = (fw - 3*0.8) / 4; gap3 = 0.8; card_y3 = 15.0; card_h3 = 16.5
for i, (title, col, desc, reveal) in enumerate(counters):
    x = fx + i*(card_w3+gap3)
    rrect(x, card_y3, card_w3, card_h3, 1.3, fill=CARD, stroke=LINE)
    rect(x, card_y3, card_w3, 0.5, fill=col)
    tline(x+1.2, card_y3+0.8, card_w3-2.4, title, size=7, color=col, bold=True)
    tmulti(x+1.2, card_y3+3.2, card_w3-2.4, 7, [desc], size=6, color=DIM)
    line_h(x+1.2, card_y3+13.5, card_w3-2.4, LINE, sw=0.1)
    tline(x+1.2, card_y3+13.5, card_w3-2.4, "How we'd catch it:", size=4.5, color=DIMMER, bold=True)
    tline(x+1.2, card_y3+14.8, card_w3-2.4, reveal, size=4.5, color=DIMMER)

# Kill signals
ky = card_y3+card_h3+0.3
rrect(fx, ky, fw, 2.8, 1.0, fill=REDBG, stroke=ORANGE, sw=0.15)
tline(fx+1.2, ky+0.5, fw-2.4, "KILL / PIVOT SIGNALS", size=6.5, color=ORANGE, bold=True)

signals = [
    "No D1 movement above baseline noise after predefined cohort reads (2+ cohorts).",
    "Guardrail deterioration — opt-out/dismissal rise, uninstall rise, D7 drop.",
    "Mechanism not supported by event data — e.g., D1 moves but notification-open-to-session conversion is near zero.",
    "Week 0 assumptions fail — \u201ctoday\u2019s lesson\u201d can't be resolved, notification infra insufficient, first-value rate too low.",
]
sig_w = (fw - 2.4 - 0.2) / 2; sig_h = 4.5; sig_start = ky+3.2
for i, sig in enumerate(signals):
    col_i = i % 2; row_i = i // 2
    sx5 = fx+1.2 + col_i*(sig_w+0.2)
    syy = sig_start + row_i*(sig_h+0.3)
    rrect(sx5, syy, sig_w, sig_h, 1.0, fill=CARD, stroke=LINE)
    rect(sx5, syy, 0.6, sig_h, fill=ORANGE)
    tmulti(sx5+1.0, syy+0.3, sig_w-1.2, 4, ["\u2715  "+sig], size=6, color=DIM)

# closing statement
close_y = sig_start+2*(sig_h+0.3)+0.1
rrect(fx, close_y, fw, 5.0, 1.2, fill=CARD2, stroke=BLUE, sw=0.15)
bar(fx, close_y, 5.0, BLUE)
tmulti(fx+2.2, close_y+0.5, fw-4.4, 4, ["A null result is useful: it tells us to stop optimizing the return cue and investigate the next retention mechanism."], size=8, color=WHITE)

tline(8.0, 198.5, PW-8, "Source: research/adversarial-review.md. This slide demonstrates that the PM is not emotionally attached to the proposed solution.", size=5.5, color=DIMMER)

# =========================================================================
# SLIDE 7 — EXECUTION & RECOMMENDATION
# =========================================================================
pdf.add_page()
page_bg()
slide_title(8.0, 5.5, "Test the smallest learning-rich bet", accent=GREEN)
eyebrow(8.0, 4.0, "06  /  EXECUTION & RECOMMENDATION")

fx = 8.0; fw = PW-16
tline(fx, 13.3, fw, "4-WEEK EXECUTION", size=7, color=DIM, bold=True)
weeks = [
    ("WEEK 0", "Validate assumptions\n+ instrumentation", BLUE,
     ["Lock metric definitions", "Instrumentation audit (7 must-have events)", "Crash-rate / onboarding check",
      "D1-by-first-action segmentation", "Establish baseline range"]),
    ("WEEK 1", "Build end-of-session\nmission + reminder", PURPLE,
     ["Ship opt-in optimization (C3)", "Build D1 notification (C1): copy, schedule, deep-link",
      "Begin end-of-session UI design (C2+C4)"]),
    ("WEEK 2", "Integrate D1\nreturn cue", ORANGE,
     ["Ship D1 notification (C1) if ready", "Ship end-of-session UI + streak (C2+C4)",
      "Begin weekly cohort D1 tracking"]),
    ("WEEK 3", "Launch + monitor", GREEN,
     ["First full cohort reading on combined D1 Pull", "Segment D1 by trigger, first-value, source",
      "Watch guardrails: D7, dismissals, uninstalls"]),
]
week_w = 24.5; week_gap = 1.5; week_start = fx; week_y = 15.0
for i, (wn, title, col, items) in enumerate(weeks):
    wx = week_start + i*(week_w+week_gap)
    rrect(wx, week_y, week_w, 16.5, 1.3, fill=CARD, stroke=LINE)
    rect(wx, week_y, week_w, 0.5, fill=col)
    tline(wx+1.2, week_y+0.6, week_w-2.4, wn, size=7, color=col, bold=True)
    tmulti(wx+1.2, week_y+1.5, week_w-2.4, 4, [title], size=8, color=WHITE, align=Align.L)
    line_h(wx+1.2, week_y+6.8, week_w-2.4, LINE, sw=0.1)
    iy = week_y+7.2
    for it in items:
        tline(wx+1.2, iy, week_w-2.4, "\u2022  "+it, size=5.5, color=DIM)
        iy += 1.4

# Week 4 — decision gate
w4x = fx + 4*(week_w+week_gap) - week_gap
w4w = week_w + week_gap
rrect(w4x, week_y, w4w, 16.5, 1.3, fill=CARD2, stroke=GREEN, sw=0.15)
rect(w4x, week_y, w4w, 0.5, fill=GREEN)
tline(w4x+1.2, week_y+0.6, w4w-2.4, "WEEK 4", size=7, color=GREEN, bold=True)
tline(w4x+1.2, week_y+1.5, w4w-2.4, "Read cohort + decide", size=8.5, color=WHITE, bold=True)
line_h(w4x+1.2, week_y+5.2, w4w-2.4, LINE, sw=0.1)

decisions = [
    ("SUCCESS", "D1 moves meaningfully above baseline range with guardrails held", GREEN),
    ("PROMISING", "Directional lift, mechanism partly confirmed → iterate", ORANGE),
    ("NO IMPACT", "Within baseline noise + guardrails held → kill / pivot", DIMMER),
]
dy = week_y+5.5
for i, (label, desc, col) in enumerate(decisions):
    yy = dy + i*3.0
    rect(w4x+1.2, yy, 0.6, 2.4, fill=col)
    pdf.set_font(FONT, "B", 6.5)
    pdf.set_text_color(*col)
    pdf.set_xy(w4x+2.0, yy)
    pdf.cell(pdf.get_string_width(label+":  "), 2.5, label+":  ", align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font(FONT, "", 6)
    pdf.set_text_color(*DIM)
    pdf.set_xy(w4x+2.0+pdf.get_string_width(label+":  "), yy)
    pdf.cell(w4w-2.4-pdf.get_string_width(label+":  "), 2.5, desc, align=Align.L, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_text_color(*INVERSE)

# Recommendation strip
rec_y = week_y+17.0
rrect(fx, rec_y, fw, 7.0, 1.2, fill=CARD2, stroke=BLUE, sw=0.15)
bar(fx, rec_y, 7.0, BLUE)
tline(fx+2.2, rec_y+0.8, 20, "RECOMMENDATION", size=6, color=BLUE, bold=True)
tmulti(fx+2.2, rec_y+2.0, fw-4.4, 4, ["Ship the D1 Pull experiment because it directly tests the leading retention hypothesis, fits the 4-week squad constraint, and produces meaningful learning even if D1 does not move."], size=8, color=WHITE)

tline(8.0, 198.5, PW-8, "22% is the assignment benchmark; experiment success is defined by measured lift versus the established baseline with guardrails held — not by hitting 22%.", size=5.5, color=DIMMER)


# ---------------------------------------------------------------------------
# SAVE
# ---------------------------------------------------------------------------
pdf_path = os.path.join(DECK, "Unrot_D1_Retention_Final.pdf")
pdf.output(pdf_path)
print(f"PDF saved: {pdf_path}")
print(f"Pages: {pdf.pages_count}")
print(f"Size: {os.path.getsize(pdf_path)} bytes")

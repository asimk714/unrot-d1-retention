#!/usr/bin/env python3
"""
Unrot D1 Retention — Final Deck Builder
Generates:
  deck/Unrot_D1_Retention_Final.pptx  (python-pptx)
  deck/Unrot_D1_Retention_Final.pdf   (fpdf2 — mirror of PPTX content)

Constraints honored:
  - 16% = assignment-provided baseline; 22% = assignment benchmark/context
  - No measured D1 improvement; no experiment run; no fabricated results
  - Prototype is an interaction prototype; browser QA BLOCKED/NOT EXECUTED
  - OBSERVED / ASSUMPTION / INFERENCE / HYPOTHESIS / UNKNOWN / PROTOTYPE labels
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

# ---------------------------------------------------------------------------
# PALETTE  (Unrot-inspired dark PM case-study theme)
# ---------------------------------------------------------------------------
BG        = RGBColor(0x0A, 0x0A, 0x0F)   # near-black
CARD      = RGBColor(0x12, 0x12, 0x1A)   # card surface
CARD2     = RGBColor(0x1A, 0x1A, 0x24)   # elevated card
INVERSE   = RGBColor(0xF5, 0xF5, 0xF7)   # near-white text
DIM       = RGBColor(0x98, 0x98, 0x9D)   # muted text
DIMMER    = RGBColor(0x63, 0x63, 0x66)   # very muted
BLUE      = RGBColor(0x00, 0x7A, 0xFF)   # primary accent (Unrot blue)
BLUE_DIM  = RGBColor(0x00, 0x66, 0xD6)
PURPLE    = RGBColor(0x58, 0x56, 0xD6)   # secondary accent
ORANGE    = RGBColor(0xFF, 0x95, 0x00)   # streak / attention
GREEN     = RGBColor(0x34, 0xC7, 0x59)   # success / D1
LINE      = RGBColor(0x1C, 0x1C, 0x24)   # card border
LINE2     = RGBColor(0x25, 0x25, 0x2E)   # elevated border
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

SW = Inches(13.333)   # 16:9 widescreen
SH = Inches(7.5)

FONT = "Calibri"
FONT_BOLD = "Calibri"

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH

BLANK = prs.slide_layouts[6]  # blank layout


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def add_slide():
    return prs.slides.add_slide(BLANK)

def bg(slide, color=BG):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def rect(slide, x, y, w, h, fill=None, line=None, line_w=None, shadow=False, rounded=False):
    shp_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shp_type, x, y, w, h)
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w or Pt(1)
    shp.shadow.inherit = False
    if shadow:
        el = shp._element.spPr
        ef = el.makeelement(qn('a:effectLst'), {})
        sh = el.makeelement(qn('a:outerShdw'),
              {'blurRad': '80000', 'dist': '38100', 'dir': '5400000', 'rotWithShape': '0'})
        c = el.makeelement(qn('a:srgbClr'), {'val': '1C1C24'})
        a = el.makeelement(qn('a:alpha'), {'val': '40000'})
        c.append(a); sh.append(c); ef.append(sh); el.append(ef)
    return shp

def txt(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=None, wrap=True):
    """runs: list of paragraphs; each paragraph is list of (text, size, color, bold, italic)"""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    if anchor is not None:
        tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        for (t, size, color, bold, italic) in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.italic = italic
            r.font.name = FONT
    return tb

def line_label(slide, x, y, w, label, color=DIM, size=11):
    """Small uppercase eyebrow label."""
    rect(slide, x, y, Inches(0.06), Inches(0.16), fill=color)
    txt(slide, x+Inches(0.14), y-Inches(0.02), w, Inches(0.2),
        [[(label, size, color, True, False)]])

def footer_note(slide, text, y=Inches(7.05), color=DIMMER, size=9):
    txt(slide, Inches(0.5), y, Inches(12.333), Inches(0.3),
        [[(text, size, color, False, True)]])

def chip(slide, x, y, text, bg_color, text_color=WHITE, w=None, h=Inches(0.32), size=11):
    if w is None:
        w = Inches(0.18 + 0.095*len(text))
    c = rect(slide, x, y, w, h, fill=bg_color, rounded=True)
    txt(slide, x, y+Inches(0.035), w, h-Inches(0.04),
        [[(text, size, text_color, True, False)]], align=PP_ALIGN.CENTER,
        anchor=None)
    return w

def arrow_right(slide, x, y, color=BLUE, size=22):
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, Inches(0.34), Inches(0.22))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp

def arrow_down(slide, x, y, color=BLUE, size=22):
    shp = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x, y, Inches(0.22), Inches(0.34))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp

def circled_num(slide, x, y, n, color=BLUE, size=28, radius=Inches(0.36)):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, y, radius, radius)
    c.fill.solid(); c.fill.fore_color.rgb = color
    c.line.fill.background(); c.shadow.inherit = False
    tf = c.text_frame; tf.word_wrap = False
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n); r.font.size = Pt(size)
    r.font.color.rgb = WHITE; r.font.bold = True; r.font.name = FONT
    return c


# ===========================================================================
# SLIDE 1 — TITLE
# ===========================================================================
s = add_slide(); bg(s)

# Left accent block
rect(s, Inches(0), Inches(0), Inches(0.14), SH, fill=BLUE)

# Top eyebrow
txt(s, Inches(0.7), Inches(0.55), Inches(10), Inches(0.3),
    [[("PRODUCT MANAGEMENT CASE STUDY  ·  SEPTEMBER 2026", 12, DIM, True, False)]])

# Main title
txt(s, Inches(0.7), Inches(1.15), Inches(11.5), Inches(1.4),
    [[("UNROT", 54, WHITE, True, False)],
     [("D1 RETENTION", 54, BLUE, True, False)]])

# Divider
rect(s, Inches(0.72), Inches(2.68), Inches(2.4), Pt(2.5), fill=BLUE)

# Subtitle
txt(s, Inches(0.7), Inches(2.85), Inches(11), Inches(0.6),
    [[("\u201cDesigning the next reason to come back\u201d", 22, DIM, False, True)]])

# KPI cards row
kpi_y = Inches(3.7)
kpi_data = [
    ("CURRENT D1", "16%", "Assignment baseline", DIM),
    ("BENCHMARK", "22%", "Assignment context — not achieved", DIM),
    ("TIMEBOX", "4 weeks", "1 Product Designer + 2 Engineers", DIM),
]
kpi_w = Inches(3.7); gap = Inches(0.32); start_x = Inches(0.7)
for i, (label, value, sub, col) in enumerate(kpi_data):
    x = start_x + i*(kpi_w+gap)
    rect(s, x, kpi_y, kpi_w, Inches(1.55), fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
    txt(s, x+Inches(0.25), kpi_y+Inches(0.2), kpi_w-Inches(0.5), Inches(0.25),
        [[(label, 11, DIM, True, False)]])
    txt(s, x+Inches(0.25), kpi_y+Inches(0.52), kpi_w-Inches(0.5), Inches(0.65),
        [[(value, 40, col if col!=DIM else BLUE, True, False)]])
    txt(s, x+Inches(0.25), kpi_y+Inches(1.15), kpi_w-Inches(0.5), Inches(0.3),
        [[(sub, 12, DIMMER, False, True)]])

# Thesis tagline
rect(s, Inches(0.7), Inches(5.5), Inches(0.06), Inches(0.6), fill=ORANGE)
txt(s, Inches(0.9), Inches(5.47), Inches(11), Inches(0.7),
    [[("PRODUCT THESIS:", 12, ORANGE, True, False)],
     [("\u201cTomorrow\u2019s 5-Minute Mission\u201d — make tomorrow\u2019s value concrete before session end", 16, WHITE, False, False)]])

# Footer
footer_note(s, "Product hypothesis + interaction prototype + experiment plan  ·  D1 Pull package: C3 + C2 + C4 + C1",
            y=Inches(6.95), color=DIMMER, size=10)

# 22% clarity footdot
txt(s, Inches(0.7), Inches(7.22), Inches(12), Inches(0.2),
    [[("Note: 22% is the assignment benchmark provided as context. It is not a measured result, guaranteed target, or observed industry figure.", 9, DIMMER, False, True)]])


# ===========================================================================
# SLIDE 2 — PROBLEM & DIAGNOSIS
# ===========================================================================
s = add_slide(); bg(s)
line_label(s, Inches(0.5), Inches(0.45), Inches(8), "01  /  PROBLEM & DIAGNOSIS")
txt(s, Inches(0.5), Inches(0.7), Inches(12), Inches(0.7),
    [[("Where might Day 1 retention be breaking?", 30, WHITE, True, False)]])
rect(s, Inches(0.52), Inches(1.35), Inches(2.0), Pt(2.5), fill=BLUE)

# Left: funnel visual
fx = Inches(0.5); fy = Inches(1.65); fw = Inches(6.3)
txt(s, fx, fy, fw, Inches(0.3), [[("THE GAP", 12, DIM, True, False)]])

# big 16%
rect(s, fx, fy+Inches(0.38), fw, Inches(1.15), fill=CARD, line=LINE, line_w=Pt(1), rounded=True)
txt(s, fx+Inches(0.3), fy+Inches(0.48), Inches(3.5), Inches(0.95),
    [[("16%", 52, BLUE, True, False)],
     [("current D1 retention", 13, DIM, False, False)]], anchor=None)
txt(s, fx+Inches(4.0), fy+Inches(0.48), Inches(2.2), Inches(0.95),
    [[("↓", 36, DIMMER, True, False)],
     [("target context", 12, DIMMER, False, True)],
     [("22%", 26, WHITE, True, False)],
     [("assignment benchmark", 12, DIMMER, False, True)]], anchor=None)
footer_note(s, "16% = assignment-provided baseline. 22% = assignment benchmark provided as context, not a measured or guaranteed target.",
            y=fy+Inches(1.6), color=DIMMER, size=9)

# working hypothesis card
hy_y = fy+Inches(1.75)
rect(s, fx, hy_y, fw, Inches(1.55), fill=CARD2, line=BLUE, line_w=Pt(1.25), rounded=True, shadow=True)
rect(s, fx+Inches(0.0), hy_y, Inches(0.08), Inches(1.55), fill=BLUE)
txt(s, fx+Inches(0.25), hy_y+Inches(0.14), fw-Inches(0.5), Inches(0.25),
    [[("WORKING HYPOTHESIS", 11, BLUE, True, False)]])
txt(s, fx+Inches(0.25), hy_y+Inches(0.42), fw-Inches(0.5), Inches(0.55),
    [[("New users may complete a reasonable first session but leave without a concrete reason to return.", 15, WHITE, False, False)]],
    anchor=None)
rect(s, fx+Inches(0.25), hy_y+Inches(1.0), Inches(0.06), Inches(0.35), fill=ORANGE)
txt(s, fx+Inches(0.4), hy_y+Inches(0.98), fw-Inches(0.6), Inches(0.4),
    [[("Not yet validated by cohort data.", 11, DIMMER, False, True)]])

# three mechanisms
mech_y = hy_y+Inches(1.72)
txt(s, fx, mech_y, fw, Inches(0.25), [[("THREE HYPOTHESIZED MISSING PULL SIGNALS", 11, DIM, True, False)]])
mechs = [
    ("1", "No explicit next action", "User finishes session without seeing what to do next — no open loop."),
    ("2", "Weak early progress signal", "Streak and progress feel too new to matter on Day 1."),
    ("3", "No strong D1 return cue", "No well-timed external prompt brings the user back."),
]
for i, (n, t, d) in enumerate(mechs):
    yy = mech_y+Inches(0.3) + i*Inches(0.42)
    circled_num(s, fx+Inches(0.05), yy+Inches(0.02), n, color=BLUE, size=14, radius=Inches(0.24))
    txt(s, fx+Inches(0.38), yy, fw-Inches(0.4), Inches(0.35),
        [[(t, 13, WHITE, True, False)],
         [(d, 11, DIM, False, False)]], anchor=None)

# Right column: "What we don't know"
rx = Inches(7.1); rw = Inches(5.7)
rect(s, rx, Inches(1.65), rw, Inches(5.15), fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
txt(s, rx+Inches(0.25), Inches(1.8), rw-Inches(0.5), Inches(0.3),
    [[("WHAT WE DON\u2019T KNOW", 12, ORANGE, True, False)]])
txt(s, rx+Inches(0.25), Inches(2.1), rw-Inches(0.5), Inches(0.35),
    [[("These are unknowns — not findings. They frame what Week 0 must resolve.", 11, DIMMER, False, True)]])
unknowns = [
    ("First-session funnel", "How many new users reach first value at all? Where is the biggest drop-off?"),
    ("D1 by entry path", "Does D1 differ by first action — lesson vs news vs interview prep vs browse-only?"),
    ("Notification exposure", "Are new users receiving any Day 1 prompt? What is the opt-in rate?"),
    ("Segment-level retention", "By acquisition source, device, intent — is 16% uniform or dragged by a segment?"),
    ("Diagnostics", "Crash rate on first session, onboarding completion, session definition, timezone handling."),
]
uy = Inches(2.55)
for i, (t, d) in enumerate(unknowns):
    yy = uy + i*Inches(0.72)
    rect(s, rx+Inches(0.25), yy, Inches(0.14), Inches(0.14), fill=PURPLE, rounded=True)
    txt(s, rx+Inches(0.5), yy-Inches(0.04), rw-Inches(0.75), Inches(0.65),
        [[(t, 13, WHITE, True, False)],
         [(d, 11, DIM, False, False)]], anchor=None)

footer_note(s, "Source: research/problem-framing.md, research/product-teardown.md, research/measurement-model.md. Classifications: HYPOTHESIS / UNKNOWN.", y=Inches(7.15), size=9)


# ===========================================================================
# SLIDE 3 — SOLUTION
# ===========================================================================
s = add_slide(); bg(s)
line_label(s, Inches(0.5), Inches(0.45), Inches(8), "02  /  SOLUTION")
txt(s, Inches(0.5), Inches(0.7), Inches(12), Inches(0.7),
    [[("TOMORROW\u2019S 5-MINUTE MISSION", 30, WHITE, True, False)]])
rect(s, Inches(0.52), Inches(1.35), Inches(2.6), Pt(2.5), fill=ORANGE)

# USER FLOW diagram (left)
fx = Inches(0.5); fw = Inches(7.2)
txt(s, fx, Inches(1.6), fw, Inches(0.25), [[("THE EXPERIENCE — FROM TODAY TO DAY 1", 12, DIM, True, False)]])

# TODAY box
rect(s, fx, Inches(1.95), fw, Inches(0.42), fill=CARD2, line=LINE2, line_w=Pt(1), rounded=True)
txt(s, fx+Inches(0.2), Inches(2.0), fw-Inches(0.4), Inches(0.32),
    [[("TODAY — FIRST SESSION", 13, ORANGE, True, False)]], anchor=None)

# flow steps (today)
steps_today = [
    "New user completes\nfirst lesson",
    "Sees tomorrow\u2019s\n5-minute mission",
    "Optionally schedules\na reminder (C3)",
]
sy = Inches(2.55)
for i, st in enumerate(steps_today):
    yy = sy + i*Inches(0.9)
    rect(s, fx, yy, fw, Inches(0.68), fill=CARD, line=LINE, line_w=Pt(1), rounded=True)
    txt(s, fx+Inches(0.25), yy+Inches(0.08), fw-Inches(0.5), Inches(0.55),
        [[(st, 13, WHITE, False, False)]], anchor=None)
    if i < 2:
        arrow_down(s, fx+fw/2-Inches(0.11), yy+Inches(0.68), color=BLUE)

# big arrow to DAY 1
arrow_down(s, fx+fw/2-Inches(0.11), sy+3*Inches(0.9)+Inches(0.05), color=ORANGE)
txt(s, fx+Inches(0.2), sy+3*Inches(0.9)+Inches(0.45), fw-Inches(0.4), Inches(0.25),
    [[("next calendar day", 11, DIMMER, False, True)]])

# DAY 1 box
d1y = sy+3*Inches(0.9)+Inches(0.75)
rect(s, fx, d1y, fw, Inches(0.42), fill=CARD2, line=LINE2, line_w=Pt(1), rounded=True)
txt(s, fx+Inches(0.2), d1y+Inches(0.05), fw-Inches(0.4), Inches(0.32),
    [[("DAY 1 — RETURN", 13, GREEN, True, False)]], anchor=None)

steps_d1 = [
    "Receives D1 return cue\n(C1 notification)",
    "Opens directly into\nnext mission",
    "Continues the habit\n(streak = 2)",
]
sy2 = d1y+Inches(0.55)
for i, st in enumerate(steps_d1):
    yy = sy2 + i*Inches(0.68)
    rect(s, fx, yy, fw, Inches(0.56), fill=CARD, line=LINE, line_w=Pt(1), rounded=True)
    txt(s, fx+Inches(0.25), yy+Inches(0.06), fw-Inches(0.5), Inches(0.46),
        [[(st, 13, WHITE, False, False)]], anchor=None)
    if i < 2:
        arrow_down(s, fx+fw/2-Inches(0.11), yy+Inches(0.56), color=GREEN)

# Right: the 4 components
rx = Inches(8.0); rw = Inches(4.85)
txt(s, rx, Inches(1.6), rw, Inches(0.25), [[("FOUR COORDINATED COMPONENTS", 12, DIM, True, False)]])

comps = [
    ("C3", "Reminder / opt-in", "Optimized notification permission prompt during onboarding. Enabler — raises the addressable population for C1.", BLUE),
    ("C2", "Next-step mission", "End-of-first-session screen shows tomorrow\u2019s concrete 5-minute mission — an internal open loop at the moment of exit.", PURPLE),
    ("C4", "Streak / progress framing", "\u201cYour streak starts today\u201d — makes the 1-day streak feel like something to protect, not just a number.", ORANGE),
    ("C1", "D1 notification / deep link", "Day 1 push: \u201cYour daily AI lesson is ready\u201d with a deep link to today\u2019s content. The external D1 trigger.", GREEN),
]
cy = Inches(1.95)
for i, (cid, title, desc, col) in enumerate(comps):
    yy = cy + i*Inches(1.18)
    rect(s, rx, yy, rw, Inches(1.05), fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
    rect(s, rx, yy, Inches(0.08), Inches(1.05), fill=col)
    chip(s, rx+Inches(0.2), yy+Inches(0.16), cid, col, w=Inches(0.6), h=Inches(0.34), size=12)
    txt(s, rx+Inches(0.95), yy+Inches(0.16), rw-Inches(1.15), Inches(0.35),
        [[(title, 14, WHITE, True, False)]], anchor=None)
    txt(s, rx+Inches(0.25), yy+Inches(0.55), rw-Inches(0.5), Inches(0.45),
        [[(desc, 11, DIM, False, False)]], anchor=None)

# hypothesis strip
hy_y = cy+4*Inches(1.18)+Inches(0.1)
rect(s, rx, hy_y, rw, Inches(0.62), fill=CARD2, line=BLUE, line_w=Pt(1), rounded=True)
txt(s, rx+Inches(0.2), hy_y+Inches(0.08), rw-Inches(0.4), Inches(0.5),
    [[("Hypothesis being tested:", 11, BLUE, True, False)],
     [("Making tomorrow\u2019s value concrete before session end increases D1 return.", 12, WHITE, False, False)]], anchor=None)

footer_note(s, "Package: C3 + C2 + C4 + C1. These are coordinated, not standalone. Source: research/interventions.md, research/prd.md.", y=Inches(7.15), size=9)


# ===========================================================================
# SLIDE 4 — PROTOTYPE
# ===========================================================================
s = add_slide(); bg(s)
line_label(s, Inches(0.5), Inches(0.45), Inches(8), "03  /  PROTOTYPE")
txt(s, Inches(0.5), Inches(0.7), Inches(12), Inches(0.7),
    [[("From hypothesis to interaction", 30, WHITE, True, False)]])
rect(s, Inches(0.52), Inches(1.35), Inches(2.3), Pt(2.5), fill=BLUE)

# Status banner
rect(s, Inches(0.5), Inches(1.55), Inches(12.333), Inches(0.42), fill=RGBColor(0x1A,0x12,0x08), line=ORANGE, line_w=Pt(1), rounded=True)
txt(s, Inches(0.7), Inches(1.58), Inches(11.8), Inches(0.36),
    [[("INTERACTION PROTOTYPE — NOT PRODUCTION", 12, ORANGE, True, False),
      ("     ·     Simulates analytics events locally in-browser.", 11, DIM, False, False)]], anchor=None)

fx = Inches(0.5); fw = Inches(12.333)

# 4 state cards in a row
states = [
    ("1", "Onboarding / reminder choice", BLUE,
     ["\u201cStay ahead, automatically\u201d", "Toggle: daily lesson reminders", "Value-forward opt-in prompt (C3)"]),
    ("2", "Lesson experience", PURPLE,
     ["Today\u2019s concept card", "Start \u2192 read \u2192 mark complete", "Progress bar + completion signal"]),
    ("3", "End-of-session next mission", ORANGE,
     ["\u201cLesson complete!\u201d", "Streak: 1 day \u2014 \u201cDon\u2019t let it go cold\u201d", "\u201cTomorrow\u2019s concept is ready\u201d \u2192 next lesson card"]),
    ("4", "D1 return / notification", GREEN,
     ["\u201cYour daily AI lesson is ready\u201d", "Tap \u2192 deep-link to today\u2019s content", "Streak: 2 days \u2014 \u201cKeep it alive\u201d"]),
]
card_w = Inches(2.95); gap = Inches(0.16); start_x = Inches(0.5)
cy = Inches(2.15); card_h = Inches(2.55)
for i, (num, title, col, lines) in enumerate(states):
    x = start_x + i*(card_w+gap)
    rect(s, x, cy, card_w, card_h, fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
    rect(s, x, cy, card_w, Inches(0.06), fill=col)
    circled_num(s, x+Inches(0.18), cy+Inches(0.2), num, color=col, size=16, radius=Inches(0.3))
    txt(s, x+Inches(0.55), cy+Inches(0.22), card_w-Inches(0.7), Inches(0.55),
        [[(title, 13, WHITE, True, False)]], anchor=None)
    rect(s, x+Inches(0.18), cy+Inches(0.88), card_w-Inches(0.36), Pt(1), fill=LINE)
    ly = cy+Inches(1.0)
    for ln in lines:
        txt(s, x+Inches(0.2), ly, card_w-Inches(0.36), Inches(0.32),
            [[("\u2022  "+ln, 11, DIM, False, False)]], anchor=None)
        ly += Inches(0.38)

# "screen mock" visual block — clean representation of the end-of-session state
# (the key intervention screen — most important to show)
mx = Inches(0.5); my = Inches(4.85); mw = Inches(12.333); mh = Inches(1.55)
rect(s, mx, my, mw, mh, fill=CARD2, line=LINE2, line_w=Pt(1), rounded=True, shadow=True)
rect(s, mx, my, Inches(0.08), mh, fill=ORANGE)
txt(s, mx+Inches(0.25), my+Inches(0.1), mw-Inches(0.5), Inches(0.25),
    [[("KEY INTERVENTION SCREEN — END OF FIRST SESSION (C2 + C4)", 11, ORANGE, True, False)]])

# mock screen layout (3 columns within the card)
col_w = Inches(3.85); col_gap = Inches(0.2); col_start = mx+Inches(0.25)
col_y = my+Inches(0.42); col_h = Inches(1.0)
mock_cols = [
    # streak frame
    [("🔥", 22, ORANGE, True, False),
     ("1 day", 14, WHITE, True, False)],
    # streak message
    [("Don\u2019t let your streak go cold.", 12, WHITE, True, False),
     ("Come back tomorrow to keep it alive — just 5 minutes.", 10, DIM, False, False)],
    # next mission preview
    [("Tomorrow\u2019s concept is ready", 11, BLUE, True, False)],
]
for ci, (col_title, col_items) in enumerate([
    ("STREAK FRAME", [("🔥", 18, ORANGE, True, False), ("1 day", 15, WHITE, True, False)]),
    ("STREAK MESSAGE", [("Don\u2019t let your streak go cold.", 12, WHITE, True, False),
                        ("Come back tomorrow to keep it alive.", 10, DIM, False, False)]),
    ("NEXT-STEP CUE (C2)", [("Tomorrow\u2019s concept is ready", 11, BLUE, True, False),
                            ("Next lesson preview shown here", 10, DIM, False, True)]),
]):
    cx = col_start + ci*(col_w+col_gap)
    rect(s, cx, col_y, col_w, col_h, fill=CARD, line=LINE, line_w=Pt(1), rounded=True)
    txt(s, cx+Inches(0.15), col_y+Inches(0.1), col_w-Inches(0.3), Inches(0.22),
        [[(col_title, 9, DIM, True, False)]])
    if ci == 0:
        txt(s, cx+Inches(0.15), col_y+Inches(0.38), col_w-Inches(0.3), Inches(0.55),
            [[("\U0001F525", 26, ORANGE, True, False)], [("1 day", 16, WHITE, True, False)]], anchor=None)
    elif ci == 1:
        txt(s, cx+Inches(0.15), col_y+Inches(0.35), col_w-Inches(0.3), Inches(0.55),
            [[("Don\u2019t let your streak go cold.", 12, WHITE, True, False)],
             [("Come back tomorrow to keep it alive.", 10, DIM, False, False)]], anchor=None)
    else:
        txt(s, cx+Inches(0.15), col_y+Inches(0.35), col_w-Inches(0.3), Inches(0.55),
            [[("\u2192 Tomorrow\u2019s concept is ready", 11, BLUE, True, False)],
             [("Next lesson card preview", 10, DIM, False, True)]], anchor=None)

footer_note(s, "Source: prototype/index.html — 4 screen states demonstrated. This is an interaction prototype, not a production build.", y=Inches(6.5), color=DIMMER, size=9)

# analytics events row
ey = Inches(6.55)
rect(s, fx, ey, fw, Inches(0.4), fill=CARD, line=LINE, line_w=Pt(1), rounded=True)
txt(s, fx+Inches(0.2), ey+Inches(0.06), fw-Inches(0.4), Inches(0.3),
    [[("SIMULATED ANALYTICS EVENTS", 10, DIM, True, False)]], anchor=None)
events = ["lesson_completed", "session_end", "notification_scheduled", "notification_sent", "notification_opened", "session_start_d1"]
ev_w = (fw-Inches(0.5))/len(events)
for i, ev in enumerate(events):
    ex = fx+Inches(0.2) + i*ev_w
    chip(s, ex, ey+Inches(0.08), ev, CARD2, text_color=BLUE, w=Inches(0.1+0.088*len(ev)), h=Inches(0.24), size=9)

# CRITICAL footnotes
footer_note(s, "CRITICAL: Browser runtime validation: BLOCKED / NOT EXECUTED in this environment. Prototype events are simulated and are NOT measured retention results.",
            y=Inches(7.05), color=RGBColor(0xFF,0x6B,0x6B), size=10)


# ===========================================================================
# SLIDE 5 — MEASUREMENT & EXPERIMENT
# ===========================================================================
s = add_slide(); bg(s)
line_label(s, Inches(0.5), Inches(0.45), Inches(8), "04  /  MEASUREMENT & EXPERIMENT")
txt(s, Inches(0.5), Inches(0.7), Inches(12), Inches(0.7),
    [[("How we\u2019d know whether it works", 30, WHITE, True, False)]])
rect(s, Inches(0.52), Inches(1.35), Inches(2.5), Pt(2.5), fill=BLUE)

# Primary metric
pm_y = Inches(1.6)
rect(s, Inches(0.5), pm_y, Inches(12.333), Inches(0.72), fill=CARD2, line=BLUE, line_w=Pt(1.25), rounded=True, shadow=True)
txt(s, Inches(0.75), pm_y+Inches(0.1), Inches(3.5), Inches(0.55),
    [[("PRIMARY METRIC", 11, BLUE, True, False)],
     [("D1 RETENTION", 22, WHITE, True, False)]], anchor=None)
rect(s, Inches(4.2), pm_y+Inches(0.16), Inches(0.04), Inches(0.4), fill=BLUE)
txt(s, Inches(4.4), pm_y+Inches(0.14), Inches(8.2), Inches(0.5),
    [[("Day-1 return rate: % of new users who complete a session on Day 0 and return for any session on the next calendar day.", 12, DIM, False, False)],
     [("Measured by weekly cohort. Baseline range TBD in Week 0 — not just the 16% point.", 11, DIMMER, False, True)]], anchor=None)

# Funnel
fy = Inches(2.45)
txt(s, Inches(0.5), fy, Inches(12), Inches(0.25), [[("MEASUREMENT FUNNEL", 12, DIM, True, False)]])
funnel = [
    ("New user", BLUE, "Day-0 cohort entry"),
    ("First value", PURPLE, "Lesson / news / interview"),
    ("Lesson completion", PURPLE, "Completed state reached"),
    ("Session end", ORANGE, "has_next_action_visible, streak, notif scheduled"),
    ("Notification scheduled", BLUE, "If opt-in granted (C1 enabler)"),
    ("Notification opened", BLUE, "Deep-link tap on Day 1"),
    ("D1 session", GREEN, "session_start on Day 1 → D1 return counted"),
]
step_w = Inches(1.62); step_gap = Inches(0.13); step_x0 = Inches(0.5)
step_y = fy+Inches(0.35)
for i, (name, col, desc) in enumerate(funnel):
    sx = step_x0 + i*(step_w+step_gap)
    rect(s, sx, step_y, step_w, Inches(0.72), fill=CARD, line=col, line_w=Pt(1.25), rounded=True)
    rect(s, sx, step_y, step_w, Inches(0.05), fill=col)
    txt(s, sx+Inches(0.1), step_y+Inches(0.08), step_w-Inches(0.2), Inches(0.3),
        [[(name, 11, col if col!=PURPLE else WHITE, True, False)]])
    txt(s, sx+Inches(0.1), step_y+Inches(0.38), step_w-Inches(0.2), Inches(0.3),
        [[(desc, 8.5, DIMMER, False, False)]])

# arrows between steps
for i in range(len(funnel)-1):
    ax = step_x0 + (i+1)*step_w + i*step_gap + step_gap/2 - Inches(0.06)
    arrow_right(s, ax, step_y+Inches(0.3), color=DIMMER, size=12)

# Supporting metrics grid
gy = step_y+Inches(0.95)
txt(s, Inches(0.5), gy, Inches(6), Inches(0.25),
    [[("SECONDARY / DIAGNOSTIC / GUARDRAILS", 12, DIM, True, False)]])
metrics = [
    ("SECONDARY", BLUE, [
        "First-session completion rate",
        "Return-session quality (duration, value on D1)",
    ]),
    ("DIAGNOSTIC", PURPLE, [
        "Notification exposure / open rate",
        "Next-action visibility at session end",
        "D1 by first action / entry path",
    ]),
    ("GUARDRAILS", ORANGE, [
        "Notification opt-out / dismissal rate",
        "Uninstall rate",
        "D7 retention (if volume allows)",
    ]),
]
col_w2 = Inches(3.95); col_gap2 = Inches(0.2); col_start2 = Inches(0.5)
for ci, (cat, col, items) in enumerate(metrics):
    cx = col_start2 + ci*(col_w2+col_gap2)
    rect(s, cx, gy+Inches(0.3), col_w2, Inches(1.35), fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
    rect(s, cx, gy+Inches(0.3), col_w2, Inches(0.05), fill=col)
    txt(s, cx+Inches(0.15), gy+Inches(0.4), col_w2-Inches(0.3), Inches(0.25),
        [[(cat, 10, col, True, False)]])
    iy = gy+Inches(0.68)
    for it in items:
        txt(s, cx+Inches(0.15), iy, col_w2-Inches(0.3), Inches(0.28),
            [[("\u2022  "+it, 11, DIM, False, False)]])
        iy += Inches(0.28)

# Experiment design
ex_y = gy+Inches(1.75)
rect(s, Inches(0.5), ex_y, Inches(12.333), Inches(0.95), fill=CARD2, line=LINE2, line_w=Pt(1), rounded=True, shadow=True)
txt(s, Inches(0.7), ex_y+Inches(0.1), Inches(2.0), Inches(0.3),
    [[("EXPERIMENT DESIGN", 11, BLUE, True, False)]])
txt(s, Inches(0.7), ex_y+Inches(0.4), Inches(5.5), Inches(0.5),
    [[("CONTROL", 13, DIMMER, True, False)],
     [("Current experience — no D1 Pull intervention.", 11, DIM, False, False)]], anchor=None)
rect(s, Inches(6.3), ex_y+Inches(0.35), Inches(0.8), Inches(0.22), fill=LINE)
txt(s, Inches(6.3), ex_y+Inches(0.33), Inches(0.8), Inches(0.25),
    [[("VS", 11, DIMMER, True, False)]], align=PP_ALIGN.CENTER, anchor=None)
txt(s, Inches(7.1), ex_y+Inches(0.1), Inches(5.5), Inches(0.5),
    [[("TREATMENT", 13, GREEN, True, False)],
     [("D1 Pull package — C3 + C2 + C4 + C1.", 11, DIM, False, False)]], anchor=None)
txt(s, Inches(0.7), ex_y+Inches(0.68), Inches(11.8), Inches(0.25),
    [[("Measure by weekly cohort. Segment every D1 read by first action / entry path / notification trigger.", 11, DIMMER, False, True)]])

footer_note(s, "Source: research/measurement-model.md, research/prd.md. No sample size or expected lift is stated — both are TBD from Week 0 cohort data.", y=Inches(7.15), size=9)


# ===========================================================================
# SLIDE 6 — ADVERSARIAL VIEW
# ===========================================================================
s = add_slide(); bg(s)
line_label(s, Inches(0.5), Inches(0.45), Inches(8), "05  /  ADVERSARIAL VIEW")
txt(s, Inches(0.5), Inches(0.7), Inches(12), Inches(0.7),
    [[("What could prove us wrong?", 30, WHITE, True, False)]])
rect(s, Inches(0.52), Inches(1.35), Inches(2.3), Pt(2.5), fill=ORANGE)

# 4 counter-diagnoses
fx = Inches(0.5); fw = Inches(12.333)
txt(s, fx, Inches(1.58), fw, Inches(0.25), [[("FOUR COUNTER-DIAGNOSES", 12, DIM, True, False)]])
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
card_w3 = Inches(2.95); gap3 = Inches(0.16); start_x3 = Inches(0.5); card_y3 = Inches(1.9); card_h3 = Inches(2.15)
for i, (title, col, desc, reveal) in enumerate(counters):
    x = start_x3 + i*(card_w3+gap3)
    rect(s, x, card_y3, card_w3, card_h3, fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
    rect(s, x, card_y3, card_w3, Inches(0.06), fill=col)
    txt(s, x+Inches(0.18), card_y3+Inches(0.18), card_w3-Inches(0.36), Inches(0.5),
        [[(title, 12, col, True, False)]])
    txt(s, x+Inches(0.18), card_y3+Inches(0.65), card_w3-Inches(0.36), Inches(1.15),
        [[(desc, 11, DIM, False, False)]], anchor=None)
    rect(s, x+Inches(0.18), card_y3+Inches(1.75), card_w3-Inches(0.36), Pt(1), fill=LINE)
    txt(s, x+Inches(0.18), card_y3+Inches(1.8), card_w3-Inches(0.36), Inches(0.3),
        [[("How we'd catch it:", 9, DIMMER, True, False)],
         [(reveal, 9, DIMMER, False, True)]], anchor=None)

# Kill / pivot signals
ky = card_y3+card_h3+Inches(0.25)
rect(s, fx, ky, fw, Inches(0.35), fill=RGBColor(0x1C,0x10,0x08), line=ORANGE, line_w=Pt(1), rounded=True)
txt(s, fx+Inches(0.2), ky+Inches(0.05), fw-Inches(0.4), Inches(0.28),
    [[("KILL / PIVOT SIGNALS", 12, ORANGE, True, False)]])

signals = [
    "No D1 movement above baseline noise after predefined cohort reads (2+ cohorts).",
    "Guardrail deterioration — opt-out/dismissal rise, uninstall rise, D7 drop.",
    "Mechanism not supported by event data — e.g., D1 moves but notification-open-to-session conversion is near zero.",
    "Week 0 assumptions fail — \u201ctoday\u2019s lesson\u201d can't be resolved, notification infra insufficient, first-value rate too low.",
]
sy5 = ky+Inches(0.45); sig_w = fw/2 - Inches(0.1); sig_h = Inches(0.55)
for i, sig in enumerate(signals):
    col_i = i % 2; row_i = i // 2
    sx5 = fx + col_i*sig_w + (Inches(0.1) if col_i==1 else Inches(0.0))
    syy = sy5 + row_i*(sig_h+Inches(0.08))
    rect(s, sx5, syy, sig_w-Inches(0.1), sig_h, fill=CARD, line=LINE, line_w=Pt(1), rounded=True)
    rect(s, sx5, syy, Inches(0.06), sig_h, fill=ORANGE)
    txt(s, sx5+Inches(0.15), syy+Inches(0.06), sig_w-Inches(0.25), sig_h-Inches(0.1),
        [[("\u2715  "+sig, 11, DIM, False, False)]], anchor=None)

# closing statement
close_y = sy5+2*sig_h+Inches(0.2)
rect(s, fx, close_y, fw, Inches(0.62), fill=CARD2, line=BLUE, line_w=Pt(1.25), rounded=True, shadow=True)
rect(s, fx, close_y, Inches(0.08), Inches(0.62), fill=BLUE)
txt(s, fx+Inches(0.25), close_y+Inches(0.1), fw-Inches(0.5), Inches(0.45),
    [[("A null result is useful: it tells us to stop optimizing the return cue and investigate the next retention mechanism.", 13, WHITE, False, True)]], anchor=None)

footer_note(s, "Source: research/adversarial-review.md. This slide demonstrates that the PM is not emotionally attached to the proposed solution.", y=Inches(7.15), size=9)


# ===========================================================================
# SLIDE 7 — EXECUTION & RECOMMENDATION
# ===========================================================================
s = add_slide(); bg(s)
line_label(s, Inches(0.5), Inches(0.45), Inches(8), "06  /  EXECUTION & RECOMMENDATION")
txt(s, Inches(0.5), Inches(0.7), Inches(12), Inches(0.7),
    [[("Test the smallest learning-rich bet", 30, WHITE, True, False)]])
rect(s, Inches(0.52), Inches(1.35), Inches(2.6), Pt(2.5), fill=GREEN)

# 4-week timeline
fx = Inches(0.5); fw = Inches(12.333)
txt(s, fx, Inches(1.58), fw, Inches(0.25), [[("4-WEEK EXECUTION", 12, DIM, True, False)]])
weeks = [
    ("WEEK 0", "Validate assumptions\n+ instrumentation", BLUE,
     ["Lock metric definitions", "Instrumentation audit (7 must-have events)", "Crash-rate / onboarding check",
      "D1-by-first-action segmentation", "Establish baseline range"]),
    ("WEEK 1", "Build end-of-session\nmission + reminder", PURPLE,
     ["Ship notification opt-in optimization (C3)", "Build D1 notification (C1): copy, schedule, deep-link",
      "Begin end-of-session UI design (C2+C4)"]),
    ("WEEK 2", "Integrate D1\nreturn cue", ORANGE,
     ["Ship D1 notification (C1) if instrumentation ready", "Ship end-of-session UI + streak framing (C2+C4)",
      "Begin weekly cohort D1 tracking"]),
    ("WEEK 3", "Launch + monitor", GREEN,
     ["First full cohort reading on combined D1 Pull", "Segment D1 movement by trigger, first-value, source",
      "Watch guardrails: D7, dismissals, uninstalls"]),
]
# Week 4 shown separately as decision
week_w = Inches(2.85); week_gap = Inches(0.19); week_start = Inches(0.5); week_y = Inches(1.9)
for i, (wn, title, col, items) in enumerate(weeks):
    wx = week_start + i*(week_w+week_gap)
    rect(s, wx, week_y, week_w, Inches(2.2), fill=CARD, line=LINE, line_w=Pt(1), rounded=True, shadow=True)
    rect(s, wx, week_y, week_w, Inches(0.06), fill=col)
    txt(s, wx+Inches(0.18), week_y+Inches(0.14), week_w-Inches(0.36), Inches(0.25),
        [[(wn, 12, col, True, False)]])
    txt(s, wx+Inches(0.18), week_y+Inches(0.42), week_w-Inches(0.36), Inches(0.55),
        [[(title, 13, WHITE, True, False)]])
    rect(s, wx+Inches(0.18), week_y+Inches(0.98), week_w-Inches(0.36), Pt(1), fill=LINE)
    iy = week_y+Inches(1.08)
    for it in items:
        txt(s, wx+Inches(0.2), iy, week_w-Inches(0.36), Inches(0.24),
            [[("\u2022  "+it, 10, DIM, False, False)]])
        iy += Inches(0.24)

# Week 4 — decision gate
w4x = week_start + 4*(week_w+week_gap) - week_gap
w4w = week_w + week_gap
rect(s, w4x, week_y, w4w, Inches(2.2), fill=CARD2, line=GREEN, line_w=Pt(1.25), rounded=True, shadow=True)
rect(s, w4x, week_y, w4w, Inches(0.06), fill=GREEN)
txt(s, w4x+Inches(0.18), week_y+Inches(0.14), w4w-Inches(0.36), Inches(0.25),
    [[("WEEK 4", 12, GREEN, True, False)]])
txt(s, w4x+Inches(0.18), week_y+Inches(0.42), w4w-Inches(0.36), Inches(0.35),
    [[("Read cohort + decide", 14, WHITE, True, False)]])
rect(s, w4x+Inches(0.18), week_y+Inches(0.82), w4w-Inches(0.36), Pt(1), fill=LINE)

decisions = [
    ("SUCCESS", "D1 moves meaningfully above baseline range with guardrails held", GREEN),
    ("PROMISING", "Directional lift, mechanism partly confirmed → iterate", ORANGE),
    ("NO IMPACT", "Within baseline noise + guardrails held → kill / pivot", DIMMER),
]
dy = week_y+Inches(0.95)
for i, (label, desc, col) in enumerate(decisions):
    yy = dy + i*Inches(0.38)
    rect(s, w4x+Inches(0.18), yy, Inches(0.06), Inches(0.3), fill=col)
    txt(s, w4x+Inches(0.3), yy, w4w-Inches(0.5), Inches(0.3),
        [[(label+":  ", 11, col, True, False), (desc, 10, DIM, False, False)]], anchor=None)

# Recommendation strip
rec_y = week_y+Inches(2.35)
rect(s, fx, rec_y, fw, Inches(0.95), fill=CARD2, line=BLUE, line_w=Pt(1.25), rounded=True, shadow=True)
rect(s, fx, rec_y, Inches(0.08), Inches(0.95), fill=BLUE)
txt(s, fx+Inches(0.25), rec_y+Inches(0.1), fw-Inches(0.5), Inches(0.25),
    [[("RECOMMENDATION", 11, BLUE, True, False)]])
txt(s, fx+Inches(0.25), rec_y+Inches(0.36), fw-Inches(0.5), Inches(0.55),
    [[("Ship the D1 Pull experiment because it directly tests the leading retention hypothesis, fits the 4-week squad constraint, and produces meaningful learning even if D1 does not move.", 13, WHITE, False, False)]], anchor=None)

footer_note(s, "22% is the assignment benchmark; experiment success is defined by measured lift versus the established baseline with guardrails held — not by hitting 22%.",
            y=Inches(7.15), color=DIMMER, size=9)


# ---------------------------------------------------------------------------
# SAVE PPTX
# ---------------------------------------------------------------------------
import os
deck_dir = os.path.expanduser("~/unrot-d1-retention/deck")
os.makedirs(deck_dir, exist_ok=True)
pptx_path = os.path.join(deck_dir, "Unrot_D1_Retention_Final.pptx")
prs.save(pptx_path)
print("PPTX saved:", pptx_path)
print("Slide count:", len(prs.slides._sldIdLst))

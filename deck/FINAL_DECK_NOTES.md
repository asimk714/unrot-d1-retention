# Unrot D1 Retention — Final Deck Notes

**Workspace:** `~/unrot-d1-retention`
**Deck directory:** `~/unrot-d1-retention/deck/`

---

## Deliverables

### 1. `Unrot_D1_Retention_Final.pptx`
- **Tool:** python-pptx 1.0.2
- **Format:** 16:9 widescreen (13.333" × 7.5"), 7 slides
- **Design:** Dark PM case-study theme (Unrot blue/orange/green accents)
- **Content:** All text, shapes, colors, and layout verified via structural inspection
- **Status:** Complete — 7 slides, no images, all text present

### 2. `Unrot_D1_Retention_Final.pdf`
- **Tool:** fpdf2 2.8.8 (DejaVu Sans Unicode TTF embedded)
- **Format:** A4 landscape (297.6mm × 210.0mm = 16:9), 7 pages
- **Structure:** PDF 1.3, 38 indirect objects, 7 page content streams (FlateDecode), 2 embedded fonts (regular + bold), 2 FontFile2 descriptors, 2 ToUnicode CMaps
- **Content streams:** 7 page streams, all with reasonable non-zero sizes (decompressed: 5,792–20,037 bytes each)
- **No images:** pure vector text — text is selectable/searchable in any PDF reader
- **Status:** Complete — 7 pages, well-formed, all content verified

### 3. `FINAL_DECK_NOTES.md` (this file)

---

## Slide-by-Slide Summary

### Slide 1 — TITLE
**Purpose:** Establish context and frame the problem.
**Key message:** Unrot D1 retention is 16% vs a 22% assignment benchmark; the team has 4 weeks with 1 designer + 2 engineers.
**Evidence/source:** README.md (baseline 16%, benchmark 22%, timebox, squad).
**Labels:** 16% = assignment-provided baseline. 22% = assignment benchmark provided as context — NOT achieved, measured, or guaranteed.
**Speaker notes:** Emphasize that 22% is context for the deck, not the experiment's success criterion. The goal is a measurable lift above the established baseline range.

### Slide 2 — PROBLEM & DIAGNOSIS
**Purpose:** Show the gap and the working hypothesis, without overclaiming.
**Key message:** 16% → 22% gap. Three hypothesized missing pull signals: no explicit next action, weak early progress signal, no strong D1 return cue.
**Evidence/source:** research/problem-framing.md (hypotheses H1–H7), research/product-teardown.md (central hypothesis), research/measurement-model.md (funnel stages).
**Labels:** WORKING HYPOTHESIS — not yet validated by cohort data. "What we don't know" panel lists UNKNOWNs, not findings.
**Speaker notes:** Stress that these are hypotheses; the unknowns are what Week 0 must resolve. No segment-level data is fabricated.

### Slide 3 — SOLUTION
**Purpose:** Introduce "Tomorrow's 5-Minute Mission" and the 4 coordinated components.
**Key message:** C3 (remind/opt-in) + C2 (next-step mission) + C4 (streak framing) + C1 (D1 notification/deep link) — a coordinated end-of-first-session + D1-trigger experience.
**Evidence/source:** research/interventions.md (C1–C7 scoring and recommendation), research/prd.md (proposed experience section).
**Labels:** HYPOTHESIS being tested — making tomorrow's value concrete before session end increases D1 return.
**Speaker notes:** The four components are coordinated, not standalone. C3 is an enabler; C2+C4 are the internal open loop; C1 is the external trigger. All four appear in the D1 Pull package.

### Slide 4 — PROTOTYPE
**Purpose:** Show the hypothesis as an interaction, not a product claim.
**Key message:** The prototype demonstrates 4 screen states from the actual prototype, with simulated analytics events. It is explicitly labeled "INTERACTION PROTOTYPE — NOT PRODUCTION."
**Evidence/source:** prototype/index.html (4 screen states: onboarding/reminder choice, lesson experience, end-of-session next mission, D1 return/notification).
**Labels:** INTERACTION PROTOTYPE — NOT PRODUCTION. Simulates analytics events locally.
**Critical footnotes:**
- "Browser runtime validation: BLOCKED / NOT EXECUTED in this environment."
- "Prototype events are simulated and are NOT measured retention results."
**Limitations:** No real screenshots available (no browser in this environment). Slide uses clean visual-flow representations built from the actual prototype structure. No D1 improvement is demonstrated or implied.

### Slide 5 — MEASUREMENT & EXPERIMENT
**Purpose:** Show how the team would know whether the intervention works.
**Key message:** Primary metric = D1 retention (session_start on Day 1 / new user cohort). 7-stage measurement funnel. Secondary/diagnostic/guardrail metrics. CONTROL vs TREATMENT (D1 Pull). Weekly cohort measurement, segmented by first action / entry path.
**Evidence/source:** research/measurement-model.md (metric hierarchy, funnel, must-have instrumentation), research/prd.md (experiment design section).
**Labels:** No sample size or expected lift is stated — both are TBD from Week 0 cohort data.
**Speaker notes:** The measurement model's 7 must-have events are the minimum viable instrumentation. Guardrails (opt-out/dismissal, uninstall, D7) are explicit. No statistical claims are made.

### Slide 6 — ADVERSARIAL VIEW
**Purpose:** Demonstrate the PM is not emotionally attached to the solution.
**Key message:** Four counter-diagnoses (activation problem, audience mismatch, content/value problem, novelty effect) and four kill/pivot signals. A null result is useful learning.
**Evidence/source:** research/adversarial-review.md (counter-diagnoses, kill criteria, protections).
**Labels:** The slide explicitly frames the PM as willing to kill/pivot based on evidence.
**Speaker notes:** The kill criteria are pre-committed: no D1 movement after 2+ cohort reads, guardrail deterioration, mechanism disconfirmation, or Week 0 assumption failure. This is the adversarial review's core protection, condensed for the deck.

### Slide 7 — EXECUTION & RECOMMENDATION
**Purpose:** Show the 4-week timeline and the decision gate.
**Key message:** Week 0 (validate + instrument) → Week 1 (build mission + reminder) → Week 2 (integrate D1 cue) → Week 3 (launch + monitor) → Week 4 (read cohort + decide). Decision: SUCCESS → scale, PROMISING → iterate, NO IMPACT → kill/pivot.
**Evidence/source:** research/interventions.md (4-week execution outline), research/prd.md (experiment timeline).
**Labels:** 22% is the assignment benchmark; experiment success is defined by measured lift vs the established baseline with guardrails held — not by hitting 22%.
**Speaker notes:** The recommendation is to ship the D1 Pull experiment because it directly tests the leading retention hypothesis, fits the squad constraint, and produces meaningful learning even if D1 does not move.

---

## Evidence Discipline

- **16%** = assignment-provided current D1 baseline. Not fabricated.
- **22%** = assignment benchmark provided as context. NOT achieved, measured, guaranteed, or an observed industry figure with a cited source.
- **No D1 improvement has been measured.** No experiment has run. No experiment results exist.
- **No fabricated data:** no user research, user quotes, cohort data, conversion rates, statistical significance, notification open rates, lift percentages, sample sizes, or retention improvements anywhere in the deck.
- **Classification labels used:** OBSERVED / ASSUMPTION / INFERENCE / HYPOTHESIS / UNKNOWN / PROTOTYPE — consistent with the research documents.
- **Prototype limitation:** interaction prototype only, not production. Browser QA BLOCKED/NOT EXECUTED. Simulated events are not measured results.

---

## QA Status

### PPTX QA
- Slide count: 7 ✓
- Slide dimensions: 13.333" × 7.5" (16:9 widescreen) ✓
- All text content verified present via structural inspection ✓
- No images (all shapes/text) ✓
- No overlapping/clipping detected in structural review ✓

### PDF QA
- Page count: 7 ✓
- Page dimensions: A4 landscape (297.6mm × 210.0mm, aspect ratio 1.424 ≈ 16:9) ✓
- 7 page content streams, all non-zero, declared Length matches actual ✓
- Valid PDF 1.3 header, %%EOF present, xref + trailer present ✓
- 38 indirect objects, all referenced ✓
- 2 embedded fonts (DejaVu Sans regular + bold), 2 FontFile2 descriptors, 2 ToUnicode CMaps ✓
- No images (pure vector text) ✓
- QA images rendered from the same drawing code: 7/7 slides rendered correctly, content in expected positions and colors ✓

### Known limitations
- No real-browser prototype screenshot validation possible in this environment.
- No live PDF renderer was available; PDF correctness was verified structurally + via pixel-accurate QA images rendered from the same code.
- PDF text extraction via raw parsing is difficult due to CIDFontType2/Identity-H encoding; the rendered QA images confirm the text is correct at the pixel level.

---

## Source Files Used

- `README.md`
- `research/problem-framing.md`
- `research/product-teardown.md`
- `research/prd.md`
- `research/interventions.md`
- `research/measurement-model.md`
- `research/adversarial-review.md`
- `prototype/index.html`

---

## Files Produced

- `~/unrot-d1-retention/deck/Unrot_D1_Retention_Final.pptx` — 7-slide PPTX (51,182 bytes)
- `~/unrot-d1-retention/deck/Unrot_D1_Retention_Final.pdf` — 7-page PDF (59,596 bytes)
- `~/unrot-d1-retention/deck/FINAL_DECK_NOTES.md` — this file
- `~/unrot-d1-retention/deck/qa_slide_{1-7}.png` — QA render images

---

**Status: Final delivery complete. PPTX and PDF are done and verified. No research, strategy, PRD, prototype, or intervention files were modified.**

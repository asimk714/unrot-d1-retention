# Unrot D1 Retention — Assignment Workspace

## 1. PROJECT

- **Assignment:** Improve D1 retention from 16% toward the benchmark of 22%
- **Timebox:** 4 weeks
- **Squad:** 1 Product Designer + 2 Engineers
- **Deliverable:** Working prototype + short slide deck

## 2. PRODUCT THESIS

**"Tomorrow's 5-Minute Mission"**

New users may complete a first learning session without a concrete reason, cue, or commitment to return the next day. The intervention completes today's lesson, immediately reveals tomorrow's 5-minute mission, optionally captures a reminder time, and creates a clear return cue — then brings the user directly into the next mission on D1. The prototype demonstrates this full journey.

## 3. WORKSPACE CONTENTS

- `research/problem-framing.md` — Problem framing, facts vs assumptions vs unknowns, JTBD, hypotheses
- `research/product-teardown.md` — External product teardown with OBSERVED / INFERRED / HYPOTHESIS classification
- `research/prd.md` — PRD for the "D1 Pull" experiment
- `research/interventions.md` — 7 candidate interventions scored and prioritized; D1 Pull package recommended
- `research/measurement-model.md` — Metric hierarchy, 7-stage funnel, must-have instrumentation, open questions
- `research/adversarial-review.md` — Counter-diagnoses, failure modes, kill criteria, protections
- `prototype/index.html` — Self-contained interaction prototype (React via CDN, no build step)
- `deck/` — Slide deck (to be created / in progress)

## 4. DELIVERABLE STATUS

| Deliverable | Status |
|---|---|
| Research (problem framing, teardown, measurement model) | COMPLETE |
| Product strategy & diagnosis | COMPLETE |
| PRD | COMPLETE |
| Intervention package & prioritization | COMPLETE |
| Experiment design (measurement + kill criteria + protections) | COMPLETE |
| Interaction prototype | COMPLETE (prototype/index.html) |
|| Slide deck | COMPLETE |

## 5. PROTOTYPE STATUS

- This is an **interaction prototype**, not a production build.
- It demonstrates the D1 Pull journey: onboarding → first lesson → end-of-session next-step + streak frame → Day 1 notification (simulated) → D1 return screen.
- Analytics events are **simulated locally** in-browser (event log panel visible via "Show Events"). The event schema maps to the measurement model's must-have events.
- **No production backend or notification infrastructure is connected.** The prototype does not send real pushes, deep-link to a real app, or write to any database.

## 6. BROWSER QA STATUS

- **Static / file-level validation:** the file is a valid self-contained HTML document and has been served successfully.
- **Full real-browser end-to-end interactive validation:** **BLOCKED / NOT EXECUTED** in this environment. A complete interactive browser journey (tap through every path, confirm events fire, confirm edge cases) was not executed.
- **Therefore:** no simulated prototype interaction should be represented as measured product performance. The prototype shows what the experience would be and what events *would* fire; it does not validate that the experience works in a real browser or that any D1 improvement exists.

## 7. EVIDENCE DISCIPLINE

- **16%** is the assignment-provided baseline.
- **22%** is the assignment benchmark / context, not a guaranteed target.
- **No improvement in D1 has been measured.** The prototype is an interaction prototype; no experiment has run.
- Hypotheses are explicitly labeled as hypotheses throughout the research docs (H1–H7 in problem-framing; central hypothesis in teardown/PRD).
- No fabricated experiment results, cohort data, user research findings, or D1 improvement figures are presented anywhere in this workspace.

## 8. RECOMMENDED REVIEW ORDER

1. This README
2. `deck/` (slide deck)
3. `prototype/index.html`
4. `research/problem-framing.md`
5. `research/prd.md`
6. `research/interventions.md`
7. `research/measurement-model.md`
8. `research/adversarial-review.md`
9. `research/product-teardown.md`

---

Status: Final deck and PDF completed and QA-verified. Evidence discipline and browser-QA caveats above remain unchanged.

# Unrot D1 Retention — Candidate Interventions & Prioritization

**Context:** D1 retention = 16% vs 22% benchmark. 1 designer, 2 engineers, 4 weeks.
**Inputs:** Problem framing (`research/problem-framing.md`), product teardown (`research/product-teardown.md`), measurement model (`research/measurement-model.md`).
**Method:** Hypothesis-driven. No solution is assumed to work; each candidate is a test of a specific hypothesis from the discovery phase.

---

## Prioritization Framework

### D1 Retention Prioritization Score (DRPS)

Each candidate is scored 1–5 on five criteria. Scores are transparent heuristics, not a formula that decides — the final call weighs the central hypothesis, the team constraint, and the learning goal.

| Criterion | What it measures | 1 = | 5 = |
|-----------|------------------|-----|-----|
| **D1 Impact** | Expected magnitude of D1 lift if the hypothesis is correct | Negligible | Large |
| **Confidence** | Strength of evidence supporting the hypothesis | Pure guess | Strong evidence |
| **Feasibility** | Can 2 engineers + 1 designer deliver in 4 weeks? | Infeasible | Clearly feasible |
| **Speed to learn** | How fast we get a readable signal | 4+ weeks | Under 1 week for leading signal |
| **Learning value** | What we learn even if D1 doesn't move | Little | High |

Risk and dependency are evaluated separately — they can veto a candidate or make it contingent, but they are not points on the scorecard.

### Constraint reality check

- **Engineering capacity:** 2 engineers × 4 weeks ≈ 8 engineer-weeks.
- **Design capacity:** 1 designer × 4 weeks ≈ 4 designer-weeks (≈20 designer-days).
- **Week 0 overhead:** instrumentation gaps (must-have events from the measurement model) are estimated at 1–2 engineer-weeks if any are missing. This is not optional — without it, no solution can be evaluated.
- **Remaining for solutions:** ~6–7 engineer-weeks and ~3–4 designer-weeks, minus review/iteration/buffer.
- **Realistic throughput:** 1 coordinated primary bet (2–4 integrated changes) is feasible. A second substantive bet is only feasible if it is lightweight or folded into the primary bet's surface area. Anything requiring a new onboarding flow, a new content-routing layer, or a large design system change is likely too much for the window.

---

## Candidate Interventions

### C1 — D1 "Your daily AI lesson is ready" push notification (with deep link)

**Hypothesis tested:** H3 (missing or weak external trigger). A sizable share of new users do not return on D1 because they receive no cue to do so.

| Dimension | Assessment |
|-----------|------------|
| **User value** | High. Delivers on the product's own promise — "one concept a day" — with a timely, low-friction prompt. Removes the recall burden from the user on D1. |
| **Expected D1 impact** | High, conditional on opt-in. Push is the most direct external D1 trigger available. A well-timed notification that deep-links to today's lesson can convert users who would not have recalled the app on their own. Impact is capped by notification opt-in rate (TBD). |
| **Evidence** | Inferred. News notifications confirmed in version history (v2.0.9). Push is a standard, well-established D1 lever across daily-engagement products. No Unrot-specific notification performance data exists yet (TBD — per measurement model, `notification_sent` / `notification_opened` may not be instrumented). |
| **Engineering effort** | Medium. If notification infrastructure and a daily-lesson sequencing already exist: schedule a D1 notification, write copy, deep-link to today's lesson. Estimated 1–2 engineer-weeks. More if notification scheduling, deep-linking, or per-user "today's lesson" resolution needs work. |
| **Design effort** | Low. Notification copy + small UI. Estimated 1–2 designer-days. |
| **Time to validate** | 1–2 cohort cycles. Leading signal (notification open rate) is immediate; D1 impact reads in 1–2 weekly cohorts. |
| **Risk** | Medium. (a) Low opt-in caps impact. (b) Annoying copy/timing could raise dismissals or uninstalls — guardrail to watch. (c) If "today's lesson" is not reliably available for all users on D1, the deep link points to a bad experience. (d) If D1 push exists but was already underperforming, this is an iteration on copy/timing/deep-link, not a new lever. |
| **Dependency** | Notification infrastructure; opt-in rate (TBD); daily lesson content reliably available on D1; deep-link routing. |
| **Learning value** | High. Directly tests the trigger-gap hypothesis. A null result is informative — it would mean the D1 problem is not primarily a missing external trigger. |

**DRPS:** Impact 4 · Confidence 3 · Feasibility 4 · Speed 4 · Learning 5

---

### C2 — End-of-first-session "next step" UI (show what's waiting tomorrow)

**Hypothesis tested:** H2 (no next-step cue). Users finish session 1 and leave with a closed loop — no visible reason to return. The fix is an in-product open loop at the moment of exit.

| Dimension | Assessment |
|-----------|------------|
| **User value** | High. Converts a "done" feeling into a "something is waiting" feeling. Gives every new user — regardless of notification opt-in — a concrete, visible reason to return. |
| **Expected D1 impact** | Medium-High. Creates an internal trigger (curiosity about tomorrow's concept / desire to keep a streak alive) at the highest-leverage moment — the instant the user is about to leave. Works even for users who decline notifications. |
| **Evidence** | Inferred. End-of-session state is unknown from outside (teardown Section 11) — likely a completion screen or home screen. The hypothesis that a missing next-step cue suppresses D1 is plausible but untested for Unrot specifically. Requires `has_next_action_visible` instrumentation (measurement model) to know the current baseline. |
| **Engineering effort** | Medium. A new end-of-session screen or a focused redesign of the current completion/home screen to surface a "next" element. Estimated 1–2 engineer-weeks. Plus instrumentation for `has_next_action_visible` (measurement model must-have). |
| **Design effort** | Medium. New UI state, copy, visual hierarchy. Must not clutter the existing experience or make the completion moment feel heavy. Estimated 3–5 designer-days. |
| **Time to validate** | 1–2 cohort cycles. |
| **Risk** | Medium. (a) If the "next" shown is a lesson the user isn't interested in, it can feel pushy or irrelevant. (b) A cluttered end screen can add friction rather than reduce it. (c) Must be verified that users actually perceive the next-step cue — not just that it exists in the UI. |
| **Dependency** | Content sequencing (does "tomorrow's lesson" exist and is it resolvable for a new user?). If the product has no concept of a daily sequence for new users, this is harder — the "next" would need to be derived. |
| **Learning value** | High. Directly tests the no-next-step-cue hypothesis. Teaches whether an in-product open loop is sufficient on its own (without push) to lift D1. |

**DRPS:** Impact 4 · Confidence 3 · Feasibility 3 · Speed 3 · Learning 5

---

### C3 — Notification opt-in prompt optimization (timing + copy + context)

**Hypothesis tested:** Enabler for C1. If notification opt-in is low, the D1 notification lever (C1) is capped. Optimizing when and how the app asks for permission raises the addressable population for any notification-based D1 lever.

| Dimension | Assessment |
|-----------|------------|
| **User value** | Medium (enabling). The prompt itself is not the value — the value is the notifications the user receives after opting in. But a well-timed, well-explained prompt respects the user and sets up the relationship. |
| **Expected D1 impact** | Medium (indirect). Raises the ceiling on C1. If opt-in is currently low, this is a meaningful multiplier. If opt-in is already high, this is a quick check and move on. |
| **Evidence** | Inferred. Standard mobile practice: permission prompts presented in-context with a clear value explanation convert better than out-of-context or system-default prompts. No Unrot-specific opt-in data (TBD). |
| **Engineering effort** | Low-Medium. A permission prompt with an explanation screen, timed well in onboarding. Estimated 0.5–1 engineer-week if the OS permission API is standard. |
| **Design effort** | Low. One explanation screen + copy. Estimated 1–2 designer-days. |
| **Time to validate** | Fast. Opt-in rate is measurable immediately; D1 impact via cohort in 1–2 weeks. |
| **Risk** | Low-Medium. A poorly timed permission prompt can interrupt onboarding and hurt onboarding completion (guardrail). Must test that onboarding completion is not harmed. |
| **Dependency** | OS notification permission API. The promised value must actually be delivered after opt-in (i.e., C1 must exist to fulfill the promise). |
| **Learning value** | Medium-High. Tells us whether notification opt-in is a bottleneck. If opt-in is already high, this confirms C1 is uncapped. If low, this is a necessary enabler. |

**DRPS:** Impact 3 · Confidence 3 · Feasibility 5 · Speed 5 · Learning 4

---

### C4 — Streak reinforcement at end of first session ("Your streak starts today — keep it alive")

**Hypothesis tested:** Partial test of H4 (no progress/investment mechanic felt on D1). The streak mechanic exists, but a new user's streak is 1 day — too new to create loss aversion. The fix is to make the *start* of the streak visible and emotionally framed as something to protect.

| Dimension | Assessment |
|-----------|------------|
| **User value** | Medium. A 1-day streak is inherently weak, but making the user aware that a streak has begun — and that it can be lost — plants the seed of loss aversion. Combined with a next-step cue (C2) or a notification (C1), it reinforces the pull. |
| **Expected D1 impact** | Medium (conditional). A streak frame alone, without a trigger, may not be enough on D1 — the streak is too young for strong loss aversion. But as part of the end-of-session experience, it adds emotional weight to the "come back tomorrow" message. |
| **Evidence** | Inferred. Streaks are a well-established retention mechanic in habit products. No Unrot-specific streak data (TBD — streak updates may not be instrumented as events). Whether a 1-day streak currently feels meaningful to a new user is unknown. |
| **Engineering effort** | Low-Medium. Mostly messaging and UI within the existing streak system. Estimated 0.5–1 engineer-week if the streak system already exists and just needs better surfacing. Marginal if combined with C2's end-of-session UI. |
| **Design effort** | Low-Medium. How the streak is displayed and framed at end of first session. Estimated 1–3 designer-days. |
| **Time to validate** | 1–2 cohort cycles. |
| **Risk** | Low-Medium. A 1-day streak shown prominently may feel trivial to some users ("my streak is 1 day, who cares"). Could be perceived as gamification without substance. Must test that the framing lands as motivating, not patronizing. |
| **Dependency** | Existing streak system; whether streak is visible/active for a first-session user today (TBD). |
| **Learning value** | Medium. Tests whether streak awareness at D1 matters. If the streak is already visible and D1 is still 16%, the streak alone is not the lever — which is itself a useful negative result. |

**DRPS:** Impact 3 · Confidence 3 · Feasibility 4 · Speed 3 · Learning 4

---

### C5 — Onboarding job-routing (identify intent and route first session)

**Hypothesis tested:** H5 (JTBD mismatch in first session). The product serves multiple jobs (learn, news, interview prep), but the first-session experience does not quickly identify and serve the user's specific job, so users receive generic content that does not fit.

| Dimension | Assessment |
|-----------|------------|
| **User value** | High for matched users. A user who came for interview prep and is routed to interview prep in session 1 gets more relevant value than a user handed a generic lesson. Improves first-session fit and likely first-value perception. |
| **Expected D1 impact** | Medium (conditional). Better first-session fit should improve D1 for the routed users — but the effect depends on routing accuracy and on whether the routed content is genuinely better for that intent. If routing misfires, it can make things worse. |
| **Evidence** | Inferred. Three content pillars exist; onboarding was recently redesigned (team suspects onboarding matters). The JTBD-mismatch hypothesis is plausible but has no Unrot-specific support yet. No data on whether D1 differs by first action / intent (TBD — this is a measurement model diagnostic). |
| **Engineering effort** | Medium-High. Requires the onboarding flow to capture intent (a question or selection), then route to different first-session content. Estimated 1.5–2.5 engineer-weeks. More if content is not tagged by intent or if routing logic is not in place. |
| **Design effort** | Medium-High. New onboarding step(s), routing made visible to the user, and potentially different first-session experiences to design. Estimated 4–7 designer-days. This is a meaningful design lift for a single designer, especially if also delivering C1/C2/C4. |
| **Time to validate** | 2 cohort cycles minimum, because segment-level D1 needs sufficient volume per routed segment to be readable. |
| **Risk** | High. (a) Onboarding changes can hurt onboarding completion — a key guardrail. (b) Routing can misfire (user selects one intent but would have preferred another, or the selected intent doesn't match their actual behavior). (c) Fragments the experience — once you have 3 onboarding journeys, you have 3 to maintain and 3 to instrument. (d) More surface area for bugs in a 4-week window. |
| **Dependency** | Content tagged by intent/job; ability to route users to different first-session content; instrumentation to measure D1 by routed segment. |
| **Learning value** | High. Directly tests H5. Even a null result teaches whether intent-matching matters for D1. |
| **Feasibility concern** | This is the heaviest, riskiest candidate. With 1 designer and 2 engineers over 4 weeks, doing C5 *and* the trigger/loop work (C1/C2/C4) is very tight and raises the risk of shipping nothing cleanly. It is the candidate most likely to crowd out learning elsewhere. |

**DRPS:** Impact 3 · Confidence 2 · Feasibility 2 · Speed 2 · Learning 4

---

### C6 — First-session completion-moment framing (make completion feel like progress, not done)

**Hypothesis tested:** Adjacent to H2/H4. The completion moment is where the user's feeling of "was this worth it?" crystallizes. If completion feels like a milestone in a journey (not a one-off done), D1 pull increases.

| Dimension | Assessment |
|-----------|------------|
| **User value** | Medium-High. The completion moment is a natural high point in the first session — the moment to plant the seed of "there's more." |
| **Expected D1 impact** | Medium. Works best as part of the end-of-session experience (C2) — the framing of completion and the pointer to what's next are two sides of the same surface. Standing alone, it's a messaging/micro-interaction change with less structural pull than C2. |
| **Evidence** | Inferred. The product already frames completion as value ("You finish it, you understand something new. That's the entire point"). The question is whether it frames it as *continuation*. No Unrot-specific data (TBD). |
| **Engineering effort** | Low-Medium. Messaging + micro-interactions + progress visibility at completion. Estimated 0.5–1 engineer-week. Marginal if folded into C2. |
| **Design effort** | Medium. Completion screen treatment, progress visualization, copy. Estimated 2–4 designer-days. Marginal if folded into C2. |
| **Time to validate** | 1–2 cohort cycles. |
| **Risk** | Low-Medium. Could feel like over-engineering a simple completion. If overdone, could cheapen the experience. |
| **Dependency** | Existing completion flow; progress/streak visibility. |
| **Learning value** | Medium. Overlaps substantially with C2's learning — both are about the end-of-session experience. Standing it up as a separate bet would duplicate scope. |

**DRPS:** Impact 3 · Confidence 2 · Feasibility 4 · Speed 3 · Learning 3

---

### C7 — Stability + onboarding completion foundation work

**Hypothesis tested:** Prerequisite / confounder check. If a meaningful fraction of new users crash or abandon during onboarding, no D1 lever will reach them. Stability is a threshold issue — fix it if it's material, don't let it consume the window if it isn't.

| Dimension | Assessment |
|-----------|------------|
| **User value** | High for affected users — a crash or broken onboarding prevents any value. But this is fixing a bug, not optimizing retention directly. |
| **Expected D1 impact** | Unknown direction and magnitude. If crash rate on first session is high, fixing it could lift D1 meaningfully (users who crash never get to return). If crash rate is low, impact is minimal. The key uncertainty is the crash rate — which is TBD (not in public data; internal crash reporting needed). |
| **Evidence** | Observed from teardown. Recent crash fixes (v2.2.4 "critical background crashes," v2.2.0 "navigation bug") and loading-speed fixes suggest stability has been a concern. But observation is not measurement — we don't know the current crash rate or its effect on D1. |
| **Engineering effort** | Unknown — depends on root cause. Could be 0.5 engineer-weeks for a quick fix or 2+ weeks for a stubborn issue. Given recent history, there may be ongoing instability that is not yet fully resolved. |
| **Design effort** | Low (unless the fix touches UI). |
| **Time to validate** | Immediate for crash rate (from crash reporting); D1 impact via cohort in 1–2 weeks. |
| **Risk** | Low (fixing bugs is generally safe). The real risk is opportunity cost — if this consumes engineering time without moving D1, it crowds out higher-impact work in a 4-week window. |
| **Dependency** | Crash reporting infrastructure; debugging capacity. |
| **Learning value** | Medium-High. Establishing whether stability is a material D1 factor is important context for interpreting everything else. If crash rate is negligible, we can confidently ignore it. If it's material, it changes the priority order. |

**DRPS:** Impact TBD · Confidence 2 · Feasibility TBD · Speed 4 · Learning 4

---

## Scoring Summary Table

| Candidate | D1 Impact | Confidence | Feasibility | Speed to learn | Learning value | Composite feel |
|-----------|-----------|------------|-------------|----------------|----------------|----------------|
| C1 · D1 notification | 4 | 3 | 4 | 4 | 5 | **Strong** |
| C2 · End-of-session next-step UI | 4 | 3 | 3 | 3 | 5 | **Strong** |
| C3 · Notification opt-in optimization | 3 | 3 | 5 | 5 | 4 | **Medium-strong (enabler)** |
| C4 · Streak reinforcement at first-session end | 3 | 3 | 4 | 3 | 4 | **Medium** |
| C5 · Onboarding job-routing | 3 | 2 | 2 | 2 | 4 | **Lower (heaviest, least certain)** |
| C6 · Completion-moment framing | 3 | 2 | 4 | 3 | 3 | **Medium (folds into C2)** |
| C7 · Stability + onboarding completion fix | TBD | 2 | TBD | 4 | 4 | **TBD (threshold work)** |

> Composites are directional, not decisive. C5 scores lower not because it is a bad idea but because it is the heaviest lift with the lowest confidence for a 4-week window — and the opportunity cost is high relative to the more direct D1 levers.

---

## Recommendation

### Primary bet: "D1 Pull" — a coordinated end-of-first-session + D1-trigger experience

**Components:**

1. **C1 — D1 "Your daily AI lesson is ready" push notification with deep link** (the external trigger)
2. **C2 — End-of-first-session "next step" UI** showing what's waiting tomorrow and that a streak has started (the internal open loop)
3. **C4 — Streak reinforcement framing** within that end-of-session UI ("Your streak starts today — come back tomorrow to keep it alive") (the emotional hook)
4. **C3 — Notification opt-in prompt optimization** as an enabler, done in parallel during onboarding (the multiplier)

**Why this is the primary bet:**

- It directly tests the **central hypothesis** from the teardown: that new users complete a reasonable first session but leave without a felt reason to return, because their streak is too new to matter, their readiness score hasn't moved, and they received no D1 notification. This package attacks all three: it gives a notification on D1 (C1), makes the next step and the streak visible at session exit (C2+C4), and ensures the notification channel is open (C3).
- It has the **highest expected D1 impact** among feasible candidates. C1 and C2 are both scored 4 on impact, and they are complementary rather than redundant — the notification provides the external cue, the end-of-session UI provides the internal open loop. If one fails, the other may still work; if both work, they reinforce.
- It is **feasible** within 4 weeks / 2 engineers / 1 designer, but it is **not the easiest** — that would be C3 or C4 alone. The choice is driven by impact and hypothesis-coverage, not by ease. C3 alone (opt-in) is easier but is an enabler with no direct D1 lift; C4 alone (streak framing) is easier but is conditional on other pull existing. The primary bet is the combination because the central hypothesis is that *multiple* D1 pull signals are missing at once.
- It has **high learning value even if D1 doesn't move.** A null result cleanly tests the trigger + open-loop hypothesis. If D1 doesn't move with a D1 notification *and* a visible next-step cue, the problem is likely elsewhere (activation failure, audience mismatch, content value, stability) — which is a strong, actionable negative result.

**Feasibility check:**

- C1 notification: ~1–1.5 engineer-weeks + 1 designer-day.
- C2 end-of-session UI: ~1.5–2 engineer-weeks + 3–5 designer-days.
- C4 streak framing: marginal if combined with C2 (~0.5 engineer-week + 1–2 designer-days).
- C3 opt-in optimization: ~0.5–1 engineer-week + 1–2 designer-days.
- Instrumentation (must-haves from measurement model): ~1–2 engineer-weeks in Week 0, *before* solution work.
- **Total:** ~3.5–5.5 engineer-weeks for solutions + ~1–2 engineer-weeks for instrumentation = ~4.5–7.5 engineer-weeks out of 8 available. Design: ~6–10 designer-days out of ~20 available.

This is feasible but tight. It assumes: notification infrastructure already exists (confirmed by news notifications in version history), daily-lesson sequencing exists (inferred from "structured from beginner to advanced"), and the end-of-session UI is a focused change rather than a sprawling redesign. If any of these assumptions is wrong, the primary bet shrinks to the subset that is still feasible (most likely C2 + C4 + C3, with C1 descoped or simplified).

---

### Secondary bet: Onboarding job-routing discovery (C5) — start learning now, defer shipping

**What "secondary bet" means here:** not a Week 1–4 build, but the highest-priority *learning* action that does not require a build.

**Action:** In Week 0–1, use the measurement model's diagnostic metrics to segment D1 by first-action type and by acquisition source. Specifically: does D1 retention differ meaningfully between users whose first action is a lesson vs news vs interview prep vs browse-only?

**Why this is the secondary bet (and why C5 is deferred for shipping):**

- C5 (onboarding job-routing) is the strongest hypothesis for *why* first-session value might be mismatched, but it is also the heaviest, riskiest, most design-intensive candidate — and it has the lowest confidence because it has no Unrot-specific support yet.
- The right move is to **test the hypothesis cheaply before committing the team to building it.** If the D1-by-first-action segmentation shows a large gap (e.g., interview-prep first-action users return at 30% while browse-only users return at 8%), that is strong evidence that intent-matching matters — and C5 moves from "deferred" to "candidate for next iteration." If the segmentation shows no meaningful difference, C5's hypothesis is weakened and the team should not invest in it.
- This learning action is low-effort (it uses the measurement model's existing diagnostic metrics) and high-value (it determines whether C5 is worth pursuing). It fits the "learning value" criterion without consuming the 4-week build window.

**If the segmentation signal is strong:** elevate C5 to a candidate for the *next* 4-week iteration, not this one. The current window is committed to the D1 Pull primary bet.

**If the signal is weak or absent:** C5 stays deferred. The D1 problem is more likely in trigger/loop/activation than in intent-matching.

---

### Explicitly deferred

**C5 — Onboarding job-routing (full build):** Deferred. Reasons:

1. **Effort and risk are too high for the window.** 1.5–2.5 engineer-weeks + 4–7 designer-days + onboarding-completion guardrail risk + segmented instrumentation + 3 onboarding journeys to maintain. With 1 designer, this alone would consume a large fraction of design capacity and leave little room for the higher-confidence D1 Pull work.
2. **Confidence is the lowest of the candidates.** The JTBD-mismatch hypothesis is plausible and important, but it has no Unrot-specific evidence yet. Shipping a complex routing flow on the strength of an untested hypothesis, in a 4-week window, is not prudent when a cheaper test (D1-by-first-action segmentation) can inform the decision.
3. **It is not the highest-impact feasible lever.** C1 and C2 are more direct D1 levers with comparable or higher impact scores and lower risk. The opportunity cost of C5 is the D1 Pull package — and the D1 Pull package better matches the central hypothesis.
4. **It is not gone — it is sequenced.** If D1-by-first-action segmentation (the secondary-bet learning action) shows a strong intent-mismatch signal, C5 becomes a leading candidate for the next iteration. Deferral is not rejection.

**C6 — Standalone completion-moment framing:** Deferred as a standalone bet. It is folded into C2's end-of-session UI work instead — the completion framing and the next-step pointer are the same surface, and building them together avoids duplicate scope. If the end-of-session UI is built, the completion framing should be part of it.

**C7 — Stability + onboarding completion fix (as a 4-week project):** Deferred *as a primary project*, conditional on a Week 0 investigation.

- **Week 0 action (not deferred):** Check crash rate on first sessions and onboarding completion rate from crash reporting and analytics. This is a 1–2 day investigation, not a build.
- **If crash rate / onboarding abandonment is material:** allocate a *bounded* engineering effort (e.g., 1 engineer-week) to stabilize the highest-impact issues before or alongside the D1 Pull work. Do not let stability become an open-ended 4-week project unless the data forces it.
- **If crash rate is low and onboarding completion is healthy:** deprioritize C7. Do not spend the 4-week window on it. Document the check as a confounder that was ruled out.

---

## 4-Week Execution Outline (for the primary bet only)

This is the realistic roadmap for the primary bet, given the constraint. It is not a menu of everything — it is what the team can actually deliver.

**Week 0 (pre-solution):**
- Lock metric definitions (new user, session, Day 1 timezone, first value, lesson completion).
- Instrumentation audit against the 7 must-have events from the measurement model.
- Add missing must-have instrumentation — especially `session_end` properties (`has_next_action_visible`, `notification_scheduled`) and notification events (`notification_sent`, `notification_opened`) if the solution involves push.
- Crash-rate / onboarding-completion check (C7 threshold investigation).
- D1-by-first-action and D1-by-source segmentation (C5 secondary-bet learning).
- Establish baseline D1 range across recent cohorts (not just the 16% point).

**Week 1:**
- Ship notification opt-in prompt optimization (C3) — fast, unblocks C1.
- Build D1 notification (C1): scheduling, copy, deep-link to today's lesson.
- Begin end-of-session UI design (C2+C4).

**Week 2:**
- Ship D1 notification (C1) if instrumentation allows a clean read.
- Ship end-of-session UI with streak reinforcement (C2+C4).
- Begin weekly cohort D1 tracking against baseline.

**Week 3:**
- First full cohort reading on the combined D1 Pull experience.
- Segment D1 movement by return trigger, first-value type, end-of-session state, and notification open — to confirm the mechanism.
- Watch guardrails: D7 (if volume allows), notification dismissals/uninstalls, onboarding completion.

**Week 4:**
- Second cohort reading. Decide: did the D1 Pull package move D1 outside the baseline noise, with guardrails held?
- If yes: candidate for broader rollout; begin planning next iteration (possibly C5 if segmentation supported it).
- If no: the trigger + open-loop hypothesis is not supported by the data. Pivot to the next most likely hypothesis (activation failure, audience mismatch, content value, stability) using the diagnostic metrics already instrumented.

**What is not in the 4-week roadmap:** C5 (onboarding job-routing build), standalone C6, and C7 beyond the Week 0 threshold check. These are deferred with reasons stated above.

---

*No baseline values are fabricated in this document beyond the 16% D1 rate given in the assignment. All effort estimates are directional, based on the teardown's inference that notification infrastructure and a daily-lesson sequence exist. If those assumptions are wrong, the primary bet's feasibility shifts — which is exactly why Week 0 instrumentation and the crash-rate check matter before committing.*

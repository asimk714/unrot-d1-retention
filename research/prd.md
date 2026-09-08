# PRD: Unrot D1 Retention — "D1 Pull" Experiment

**Version:** 1.0 (experiment draft)
**Status:** For review
**Author:** Principal PM
**Date:** September 2026
**Constraint:** 1 Product Designer · 2 Engineers · 4 weeks
**Related:** `research/problem-framing.md`, `research/product-teardown.md`, `research/measurement-model.md`, `research/interventions.md`, `research/adversarial-review.md`

---

## 1. Problem

New users who complete a first session on Unrot do not return on the calendar day after that session. D1 retention is **16%** against an industry benchmark of **22%**.

The working diagnosis (unconfirmed) is that new users complete a reasonable first session but leave without a felt reason to return: their streak is too new to matter, their readiness score hasn't moved, and they received no Day 1 prompt. In short, the product's retention mechanics are **deferred** past Day 1, so Day 1 becomes a pure recall test that most new users fail.

This is a hypothesis. It may be wrong — see Non-goals and Open Questions.

---

## 2. Goal

**Primary goal:** Raise D1 retention for new users from the current baseline (16% point estimate; baseline range TBD from cohort data) toward the 22% benchmark — or, more precisely, produce a **measurable, reproducible lift above the baseline range** within the 4-week experiment window, with guardrails holding.

**Learning goal:** Test whether adding (a) a Day 1 external trigger and (b) an in-product next-step cue at session exit lifts D1 — and whether it does so via the intended mechanism.

---

## 3. Non-goals

**Explicitly out of scope for this experiment:**

- **Onboarding job-routing (C5).** Deferred. The D1-by-first-action segmentation is a Week 0 diagnostic, not a build.
- **Standalone completion-moment framing (C6).** Folded into the end-of-session UI below, not a separate build.
- **Stability/crash fixes as a 4-week project (C7).** Week 0 threshold check only. If crash rate is material, allocate a bounded effort; otherwise deprioritize.
- **Rewriting onboarding.** The onboarding flow is touched only for the notification opt-in prompt optimization (C3). No onboarding flow overhaul.
- **A daily notification habit beyond Day 1.** The experiment sends a limited number of D1/near-D1 reminders, not an ongoing daily nag. Long-term notification strategy is out of scope.
- **Closing the full gap to 22% in 4 weeks.** The benchmark is context for the deck, not the experiment's success criterion. A real lift below 22% is still a win.
- **New content, new lessons, new features beyond what's needed for the D1 Pull surface.** Content is assumed to exist.

---

## 4. Target user

**Primary:** New users who install/open Unrot for the first time, complete a first session that reaches first value, and are eligible for a Day 1 notification.

**Secondary (segment of interest, not a separate build):** Users whose first action is interview prep or news — to observe whether the generic next-step cue under-serves them (measured, not solved, in this experiment).

---

## 5. User story

> As a new user who just finished my first Unrot session, I want to know what to do next and feel that something is waiting for me, so that I have a reason to open the app again tomorrow.

This story covers two moments:
1. **End of first session** — the user leaves with a visible next step and a streak frame.
2. **Day 1** — if the user opted into notifications, they receive a prompt that brings them back.

---

## 6. Product hypothesis

**H_main:** If we show new users a clear next-step cue at the end of their first session **and** send them a well-timed Day 1 notification with a deep link to today's content, then more new users will return on Day 1, because the intervention supplies both an internal open loop (the visible next step) and an external cue (the Day 1 notification) that the current product does not.

**Sub-hypotheses:**

- **H1:** The Day 1 notification increases Day 1 returns among users who opted into notifications.
- **H2:** The end-of-session next-step UI increases Day 1 returns among users who do not rely on notifications (and reinforces returns among those who do).
- **H3:** Streak framing at the end of the first session increases the emotional pull to return in combination with the above.

**Falsification condition:** If D1 does not move above the baseline range after 2 full cohort cycles, with guardrails holding, then the trigger + open-loop hypothesis is not supported and the team should pivot to the next hypothesis.

---

## 7. Proposed experience

Three surface changes, designed as one coordinated experience:

### 7.1 End-of-first-session next-step screen (C2 + C4)

**When:** At the end of a new user's first session that reaches first value — specifically at the `session_end` moment for the first session.

**What the user sees:** A focused screen (or a focused section atop the existing completion/home screen — TBD by design, must be a focused surface) that includes:

1. **Completion acknowledgment** — brief acknowledgment that the user finished their first lesson/item.
2. **Streak frame** — "Your streak starts today" (or equivalent), with the streak count visible (1 day). Framed as something to keep alive, not just a number.
3. **Next-step cue** — a concrete, visible "what's next" for tomorrow. Preferred: "Tomorrow's concept is ready" pointing to the next lesson/content for that user. If the product cannot resolve a personalized next item per user on D1, fall back to a safe default surface (e.g., home screen with today's content surfaced).
4. **Optional: notification reminder** — a small reconfirmation or reminder that a Day 1 notification is expected (only if the user already opted in). Do not re-prompt for permission here.

**Design constraint:** This must be a focused surface, not a sprawling redesign of the entire completion flow. The goal is to add a next-step cue, not to redesign the app's completion experience end-to-end.

### 7.2 Day 1 notification (C1)

**When:** On Day 1 (calendar day after the user's first session), scheduled in advance or triggered by a Day 1 check.

**What the user receives:** A push notification with copy such as (final copy is design's call):

- "Your daily AI lesson is ready" (or variant)
- Deep link to today's lesson/content for that user, or to a safe default home surface if a personalized lesson can't be resolved.

**Frequency constraint:** A limited number of sends in the first week — at minimum the Day 1 reminder, and only additional sends if they are clearly valuable and not an ongoing daily nag. The experiment is about D1, not about building a permanent daily notification habit.

### 7.3 Notification opt-in prompt optimization (C3)

**When:** During onboarding, in context, with a clear value explanation.

**What changes:** The permission prompt is presented at a better moment with clearer value communication than the current default. The exact current behavior is TBD from the Week 0 audit; the change is to improve timing and framing, not necessarily to rebuild the prompt.

**Purpose:** Raise notification opt-in rate so the Day 1 notification (C1) has a larger addressable population. This is an enabler, not the D1 lever itself.

---

## 8. User flow

### End of first session (new user, first value reached)

```
[User completes first lesson / news / interview question]
        |
        v
[session_end event fires with properties:
  has_next_action_visible = true
  streak_after_session = 1
  notification_scheduled = true (if opt-in granted)]
        |
        v
[End-of-session next-step screen displays:
  - completion acknowledgment
  - streak frame ("Your streak starts today — streak: 1")
  - next-step cue for tomorrow]
        |
        v
[User leaves the app]
        |
        v
[Day 1: if user opted into notifications → Day 1 push delivered
  with deep link to today's content]
        |
        v
[If user taps notification → deep link opens app to today's content
  → session_start on Day 1 fires → D1 return counted]
```

### Edge cases

- **User does not opt into notifications:** They still see the end-of-session next-step cue. They rely on internal recall / the visible next step. This is the control contrast for C1.
- **User's first session does not reach first value (browse-only, abandon):** They are not eligible for the end-of-session next-step screen (no first value to anchor the streak frame). They are part of the denominator for D1 but not the target of the end-of-session UI. This is intentional — the intervention targets users who reached first value.
- **"Today's lesson" cannot be resolved for a user on D1:** Deep link falls back to a safe default (home screen with today's content surfaced). This must be verified in Week 0.
- **User returns on Day 1 organically (no notification tap):** Counted as a D1 return. The notification is one path, not the only path. The `return_trigger` property on `session_start` distinguishes organic vs notification-driven return.

---

## 9. Functional requirements

### FR1 — End-of-session next-step screen (C2 + C4)

- **FR1.1:** At the end of a new user's first session that reaches first value, display a focused next-step screen or focused section.
- **FR1.2:** The screen must include: completion acknowledgment, streak frame with visible streak count, and a next-step cue for tomorrow.
- **FR1.3:** The next-step cue must deep-link to a resolvable destination — preferably tomorrow's content for that user; if not resolvable, a safe default home surface.
- **FR1.4:** The screen must not block or delay session end. It is shown as the user is exiting, not as a gate.
- **FR1.5:** The screen appears only for first-session users who reached first value, not for returning users or users who did not reach first value.

### FR2 — Day 1 notification (C1)

- **FR2.1:** Schedule or trigger a Day 1 notification for new users who completed first value on Day 0 and opted into notifications.
- **FR2.2:** The notification copy must be clear, low-pressure, and value-forward (final copy: design).
- **FR2.3:** The notification must deep-link to today's content for the user, or to a safe default if a personalized destination is not resolvable.
- **FR2.4:** The notification frequency in the experiment window is limited — Day 1 reminder as the core send, with only additional high-value sends if any. No ongoing daily nag.
- **FR2.5:** `notification_sent` and `notification_opened` events must fire with `notification_type`, `user_id`, `timestamp`, and `deep_link_target` (per measurement model).

### FR3 — Notification opt-in prompt optimization (C3)

- **FR3.1:** Present the notification permission prompt during onboarding in a better moment with clearer value explanation than the current behavior (current behavior TBD in Week 0).
- **FR3.2:** The change is an optimization of existing prompt behavior, not a new permission model.
- **FR3.3:** `granted_notification_permission` must be captured on `onboarding_completed` (per measurement model).

### FR4 — Instrumentation (must-haves from measurement model)

- **FR4.1:** The 7 must-have events from the measurement model must be available before solution work begins in Week 1. Any gaps must be filled in Week 0.
- **FR4.2:** In particular, `session_end` must include `has_next_action_visible`, `streak_after_session`, and `notification_scheduled`. `session_start` must include `day_number` and `return_trigger`. `notification_sent` and `notification_opened` must be instrumented if C1 is in scope.
- **FR4.3:** All events must include `user_id`, `session_id` (if applicable), and `timestamp`.

### FR5 — Edge case / error handling

- **FR5.1:** If "today's lesson" cannot be resolved for a user on D1, the notification deep link must not break — it must fall back to a safe default.
- **FR5.2:** If the end-of-session screen cannot be shown for a first-session user (e.g., the user leaves from an unexpected state), log the exception but do not block session end.

---

## 10. Analytics events

Based on the measurement model. Events marked **New** require instrumentation in Week 0 if not already present.

| Event | Properties | New? | Purpose |
|-------|------------|------|---------|
| `new_user` | `user_id`, `timestamp`, `source`, `platform`, `app_version`, `is_returning_install` | Possibly | Cohort denominator |
| `session_start` | `user_id`, `session_id`, `timestamp`, `day_number`, `return_trigger` (notification_open / organic / other) | **New props likely** | Day 0 and Day 1 session definition; D1 numerator |
| `session_end` | `session_id`, `duration_ms`, `last_screen`, `streak_after_session`, `has_next_action_visible`, `notification_scheduled` | **New props likely** | End-of-session state; primary C2 diagnostic |
| `first_value_achieved` | `user_id`, `timestamp`, `value_type`, `value_id`, `time_to_first_value_ms` | Possibly | Activation diagnostic |
| `notification_sent` | `user_id`, `timestamp`, `notification_type`, `expected_trigger_day` | **New** (if not present) | C1 receipt |
| `notification_opened` | `user_id`, `timestamp`, `notification_type`, `deep_link_target` | **New** (if not present) | C1 open + deep-link behavior |
| `onboarding_completed` | `user_id`, `timestamp`, `onboarding_duration_ms`, `granted_notification_permission` | Possibly | Opt-in rate; onboarding completion |
| `lesson_started` | `lesson_id`, `topic`, `level`, `timestamp` | Possibly | First-action segmentation |
| `lesson_completed` | `lesson_id`, `completion_time_ms`, `next_lesson_id` | Possibly | Completion-rate diagnostic |

**TBD:** Exact event names and property keys must be mapped to the existing analytics schema in Week 0. The table above is the semantic target, not the literal implementation.

**Minimum viable instrumentation for the experiment:** `new_user`, `session_start` (with `day_number` + `return_trigger`), `session_end` (with `has_next_action_visible` + `streak_after_session` + `notification_scheduled`), `notification_sent`, `notification_opened`, `onboarding_completed` (with `granted_notification_permission`).

---

## 11. Success criteria

### Primary success criterion

**D1 Retention Rate lifts above the baseline range and holds across 2+ cohort cycles, with guardrails holding.**

- The baseline range is established in Week 0 from the most recent 4–8 weekly cohorts (not just the 16% point).
- "Lifts above the baseline range" means the solution cohort's D1 rate is outside the baseline noise band, not just a single point above 16%.
- "Holds across 2+ cohort cycles" means the lift is not a one-cohort noise spike.

### Diagnostic success criteria (mechanism confirmation)

- **Notification path:** Among users who received the Day 1 notification, a meaningful share open it and convert to a Day 1 session — i.e., the `notification_opened` → `session_start` conversion is not near zero.
- **End-of-session path:** A meaningful share of first-session users see `has_next_action_visible = true` at session end, and D1 is higher for those users than for those who don't (if the data supports the comparison).
- **Mechanism not disconfirmed:** The D1 lift is not fully explained by a source-mix shift or a single anomalous cohort.

### Benchmark framing

- The 22% benchmark is context for the slide deck, not the experiment's pass/fail criterion.
- If the experiment produces a real, mechanism-consistent lift (e.g., 3–5 points) without hitting 22%, that is a successful experiment — it tells us the lever works and how much it moves the needle.

---

## 12. Guardrails

**Any of these triggers kills or pauses the experiment, regardless of D1 movement:**

| Guardrail | Metric | Kill/pause threshold |
|-----------|--------|----------------------|
| **Notification opt-in rate** | `granted_notification_permission` rate | Drops meaningfully after the C3 change relative to the pre-change baseline |
| **Uninstall rate** | Uninstall rate in solution cohort vs baseline | Rises meaningfully in the solution cohort |
| **Notification dismissal rate** | `notification_opened` with dismiss / notification ignore rate | Rises meaningfully and keeps rising |
| **Day 7 retention** | D7 rate for solution cohort (if volume allows) | Drops relative to baseline — short-term D1 lift at the cost of longer-term retention |
| **Onboarding completion rate** | `onboarding_completed` / `onboarding_started` | Drops after the C3 change (the opt-in prompt is hurting activation) |
| **Session-quality artifact** | D1 rate under a stricter session-quality threshold | If D1 lift disappears under a stricter session definition, flag as a possible measurement artifact, not a real lift |

**Guardrail monitoring cadence:** Weekly during the experiment, with immediate escalation if any guardrail moves sharply in a single cohort.

---

## 13. Experiment design

### Design type

**Single-group pre-post with cohort comparison.** Not a randomized holdout — in a 4-week window with limited volume, the comparison is solution cohort vs recent baseline cohorts, not treatment vs control within the same window.

### Rationale for no holdout

A randomized holdout is cleaner but consumes volume and time. In a 4-week window, the priority is getting a readable signal on the D1 Pull package as a whole. If the signal is clear and positive, a future iteration can run a holdout to isolate C1 vs C2. If the signal is null, a holdout wouldn't have changed the decision.

**Caveat:** This design makes source-mix confounds more likely (see Open Questions). The Week 0 source-mix baseline and ongoing source-mix monitoring are the mitigation.

### Cohorts

- **Baseline cohorts:** Most recent 4–8 weekly cohorts (Week 0).
- **Solution cohorts:** Weekly cohorts during Weeks 1–4 as the solution ships. The first full solution cohort is the first cohort that experiences the complete D1 Pull package.
- **Cohort granularity:** Weekly if volume allows; biweekly if weekly cohorts are too small for a readable signal (Week 0 determination).

### What is being tested

The **package** (C1 + C2 + C4 + C3) as a coordinated experience, not each component in isolation. The experiment answers "does the D1 Pull package lift D1?" — not "which component drove it?" Component-level isolation is a future iteration if the package works.

### Mechanism reads (not success criteria, but learning)

- D1 by `return_trigger` (notification_open vs organic) — is the notification the lever?
- D1 by `first_value_type` — is the lift concentrated in lesson-driven users? (Tests the mismatched-segment concern.)
- D1 by `has_next_action_visible` at session end — is the end-of-session cue the lever?
- D1 by source — is the lift coming from a shifted source mix?

---

## 14. Rollout plan

### Week 0 — Diagnostic & instrumentation (before solution build)

**Activities (all must complete before Week 1 solution work):**

1. Lock metric definitions: new user, session, Day 1 timezone, first value, lesson completion, session-quality threshold.
2. Instrumentation audit: map the must-have events to the existing schema. Identify gaps.
3. Fill instrumentation gaps — especially `session_end` properties (`has_next_action_visible`, `streak_after_session`, `notification_scheduled`) and notification events (`notification_sent`, `notification_opened`) and `session_start` properties (`day_number`, `return_trigger`).
4. Establish baseline: D1 rate across recent cohorts (range + trend), new-user volume per week, first-value rate, D1-by-source, D1-by-first-action, crash rate, onboarding completion rate, notification opt-in rate (current).
5. Verify "today's lesson" resolvability for new users on D1. If not resolvable, decide fallback (safe default deep link) or scope C1 down.
6. Verify notification infrastructure capabilities (schedule per user/day, deep links, conditional triggers).
7. Confirm current streak behavior for new users (is it surfaced on D0? does it increment?).
8. Decide cohort granularity (weekly vs biweekly) based on volume.

**Deliverable:** A Week 0 read that confirms (or revises) the primary bet's feasibility and establishes the baseline. If the read reveals a fatal assumption breach, re-plan before Week 1.

### Week 1 — Ship enabler + start build

- Ship notification opt-in prompt optimization (C3) — fastest to ship, unblocks C1.
- Build Day 1 notification (C1): scheduling, copy, deep link.
- Start end-of-session next-step UI design (C2 + C4).
- Begin weekly cohort D1 tracking (first reads will be pre-solution or partial-solution, establishing the in-experiment baseline trend).

### Week 2 — Ship C1, ship C2 + C4

- Ship Day 1 notification (C1) if instrumentation supports a clean read.
- Ship end-of-session next-step UI with streak framing (C2 + C4).
- First full-solution cohort begins.

### Week 3 — First full read

- First full cohort reading on the complete D1 Pull package.
- Segment the read by return trigger, first-value type, source, end-of-session state, and notification open-to-session conversion.
- Check guardrails.

### Week 4 — Second read + decision

- Second cohort reading. Decision gate:
  - **Win:** D1 lifted above baseline range, held across 2+ cohorts, guardrails held, mechanism is at least directionally consistent. → Candidate for broader rollout; plan next iteration (possibly C5 if segmentation supported it).
  - **No clear lift or null:** The trigger + open-loop hypothesis is not supported. → Kill the package as a D1 solution; pivot to the next hypothesis using the diagnostics already instrumented.
  - **Mixed / inconclusive:** If volume was too low for a confident read, decide whether to extend the measurement window (if the solution is still worth testing) or kill and learn.

---

## 15. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Diagnosis is wrong (activation / audience / content-value / novelty failure) | Medium | High — intervention solves the wrong problem | Week 0 diagnostics (first-value rate, D1-by-source, D1-by-first-action, crash rate); kill criterion 4 (fatal assumption breach) |
| "Today's lesson" not resolvable for new users on D1 | Medium (unknown — TBD Week 0) | High for C1 | Week 0 verification; fallback deep link to safe default; scope C1 down if needed |
| Notification infrastructure can't support D1-scheduled, deep-linked, conditional notification | Low-Medium (unknown — TBD Week 0) | Medium | Week 0 infrastructure audit; simplify C1 if gaps exist |
| Notification opens rise but D1 sessions don't | Medium | Medium — false positive | Primary metric is session-based D1, not open rate; monitor open-to-session conversion |
| Small cohort volume → noisy reads / inconclusive result | Medium (unknown — TBD Week 0) | Medium — can't get a readable signal in 4 weeks | Week 0 volume check; biweekly cohorts if needed; accept directional read with stated confidence |
| Source-mix confound (solution cohort happens to have better-intent users) | Medium | Medium — lift misattributed to intervention | Week 0 source baseline; monitor source mix weekly; compare like-for-like where possible |
| Notification habituation / opt-out | Low-Medium | Medium — harms channel long-term | Limit notification frequency; monitor opt-in and dismissal rates as guardrails |
| End-of-session UI adds friction / clutter | Low-Medium | Low-Medium — degrades experience for some users | Keep the surface focused; monitor onboarding completion as a guardrail |
| Mismatched-intent users under-served by generic next-step cue | Medium (if mismatched segment is large) | Medium — partial solution for a segment | D1-by-first-action segmentation; document limitation; surface for next iteration (C5) |
| Benchmark (22%) sets an unfair bar | Medium | Low-Medium — team judges itself against an unreachable target | Internal success criterion = lift above baseline range; 22% is deck context only |

---

## 16. Open questions

These must be answered (or explicitly marked as unknown and accepted) before or during the experiment. They are not optional polish — several determine feasibility.

### Before Week 1 (Week 0)

1. **What is the current analytics platform and event schema?** (Determines how much instrumentation is truly new.)
2. **What is the exact definition of "new user," "session," and "Day 1" (timezone) used to compute the 16%?** (Must match the experiment's definitions.)
3. **What is the new-user volume per week?** (Determines cohort granularity and whether a 4-week read is feasible.)
4. **What is the current first-value achievement rate?** (If low, the diagnosis is activation, not pull — re-plan.)
5. **What is the current D1-by-source and D1-by-first-action breakdown?** (Tests audience-quality and JTBD-mismatch hypotheses before investing.)
6. **What is the current crash rate on first sessions and onboarding completion rate?** (C7 threshold check.)
7. **Can "today's lesson" be resolved for a new user on D1, and deep-linked?** (Gates C1 feasibility.)
8. **What notification capabilities exist today — scheduling per user/day, deep links, conditional triggers?** (Gates C1 effort estimate.)
9. **Is the streak surfaced and incremented for a first-session user today?** (Gates C4 framing.)
10. **What is the current notification opt-in rate?** (Determines whether C3 is high- or low-leverage.)

### During the experiment

11. **Is the solution cohort's source mix stable vs baseline?** (If not, flag as a confound.)
12. **Is the open-to-session conversion for the Day 1 notification meaningful?** (If near zero, the notification isn't the lever — even if D1 moves.)
13. **Is the D1 lift concentrated in a segment that the intervention explicitly targets, or is it diffuse?** (Helps interpret mechanism.)

### For the slide deck (not blocking the experiment)

14. **What is the source and definition of the 22% benchmark, and is it comparable to Unrot's definition?** (Contextual, but worth getting right in the deck.)
15. **What is the D7 and D30 retention for the baseline cohorts?** (To frame whether D1 is the binding constraint or part of a broader retention problem — nice to have, not blocking.)

---

## 17. 4-week delivery plan

### Week 0 — Diagnostic & instrumentation (pre-solution)

**Owner:** Engineers (instrumentation) + PM (definitions, baseline, diagnostics)

- Lock metric definitions (new user, session, Day 1 timezone, first value, lesson completion, session threshold).
- Instrumentation audit + gap fill for must-have events.
- Baseline: D1 range + trend, volume, first-value rate, D1-by-source, D1-by-first-action, crash rate, onboarding completion, opt-in rate.
- Feasibility checks: "today's lesson" resolvability, notification infra capabilities, streak behavior, cohort granularity.
- Week 0 read: confirm or revise primary bet feasibility.

**Design (Week 0):** Review current end-of-session UX, current notification copy/behavior, current opt-in prompt. Define the new end-of-session screen concept and notification copy direction. No high-fidelity polish yet — this is discovery + scoping.

### Week 1 — Start shipping

**Engineering:**
- Ship notification opt-in prompt optimization (C3).
- Build Day 1 notification (C1): scheduling, copy, deep link, event instrumentation.
- Continue end-of-session UI build as design lands.

**Design:**
- End-of-session next-step screen design (C2 + C4): concept → finished assets.
- Notification copy finalization (C1).
- Opt-in prompt design (C3) — already shipped or shipping early Week 1.

**Analytics:** Begin weekly D1 tracking. First reads are pre-solution / partial-solution (establishing in-experiment trend).

### Week 2 — Complete the package

**Engineering:**
- Ship end-of-session next-step UI (C2 + C4).
- Ship Day 1 notification (C1) if not already live.
- Verify instrumentation is firing correctly for the new surfaces.

**Design:**
- Polish and handoff for C2 + C4 if not already shipped.
- Support any instrumentation UI (e.g., where `has_next_action_visible` is set).

**Analytics:** First full-solution cohort begins. Weekly D1 read.

### Week 3 — First full read

**Analytics (PM + analytics owner):**
- First full cohort read on the complete D1 Pull package.
- Segment by return trigger, first-value type, source, end-of-session state, notification open-to-session conversion.
- Guardrail check.

**Engineering/Design:** Monitor bugs, watch for unexpected user behavior. Minor fixes only — no new scope.

### Week 4 — Second read + decision

**Analytics:**
- Second cohort read.
- Decision gate: win / no lift / inconclusive.
- If win: document for broader rollout + next iteration planning.
- If no lift: document the disconfirmation; pivot to next hypothesis.

**Team:** No new feature work in Week 4 beyond fixes. The window is for measurement and decision, not for adding more.

### Capacity check

- **Engineering:** Week 0 instrumentation (1–2 engineer-weeks) + C3 (0.5–1 week) + C1 (1–1.5 weeks) + C2+C4 (1.5–2 weeks) ≈ 4–6.5 engineer-weeks of solution work + 1–2 weeks instrumentation = 5–8.5 engineer-weeks out of 8 available. Feasible if Week 0 instrumentation is efficient and the end-of-session UI is a focused surface. Tight but doable; the Week 0 feasibility checks exist precisely to confirm this before committing.
- **Design:** C3 (1–2 days) + C1 copy (1 day) + C2+C4 end-of-session screen (3–5 days) ≈ 5–8 designer-days out of ~20 available. Comfortable within capacity, with room for iteration and review.

The plan is feasible on the assumption that (a) the end-of-session UI is a focused surface, not a sprawling redesign, and (b) notification infrastructure supports the needed behavior with limited new work. Both are verified in Week 0.

---

*This PRD is for an experiment, not a permanent feature spec. Its success criterion is a measurable D1 lift with guardrails held and a directionally consistent mechanism — not a commitment to ship any particular component permanently. If the experiment fails, the components can be rolled back; if it succeeds, the next iteration decides what to keep, extend, or hold out for a randomized test.*

# Unrot D1 Retention — Measurement Model

**Author:** Principal PM + Product Analytics Lead
**Date:** September 2026
**Problem:** D1 retention = 16% vs 22% industry benchmark
**Constraint:** 4-week development window, 2 engineers
**Status:** Measurement design — no baselines fabricated

---

## Metric Hierarchy

### North Star Metric

| Level | Metric | Definition |
|-------|--------|------------|
| **North Star** | **D1 Retention Rate** | % of new users who complete a session on Day 0 and return for any session on the calendar day after their first session (Day 1) |

> TBD: Exact session definition (app open? minimum engagement duration? explicit session start event?). The definition must be fixed before any metric is trusted.

---

### Primary Metric

| Metric | Definition | Why it's primary |
|--------|------------|------------------|
| **D1 Retention Rate (cohort)** | For each weekly cohort of new users: (users with ≥1 session on Day 1) / (users with ≥1 session on Day 0) | Directly measures the assignment. Cohort view allows us to track movement from 16% → 22% over the 4-week window. |

**TBD:**
- Cohort window: weekly? daily? (Weekly recommended given sample size.)
- "New user" definition: first-ever app open? first after install? first after sign-up? (Must be consistent with how the 16% was originally computed.)
- Calendar day vs rolling 24h: calendar day is stated in the assignment; confirm timezone handling.
- Denominator inclusion: do we count users who crash/drop during onboarding in the denominator? (Recommended: yes — a user who never reaches first value is still a new user who didn't return.)

---

### Secondary Metrics

| Metric | Definition | Purpose |
|--------|------------|---------|
| **D1 Retention by first-action type** | D1 rate segmented by the user's first meaningful action (lesson start, news open, interview question, browse-only, abandoned) | Tells us which entry points are most/least predictive of return — directs solution design. |
| **D1 Retention by acquisition source** | D1 rate segmented by channel/campaign/source | Tests the audience-quality hypothesis (H6 from problem framing). If a single low-intent channel dominates the denominator, the lever may be acquisition, not product. |
| **Day 0 → Day 1 conversion rate** | % of Day 0 active users who return on Day 1 | Alternative framing; useful if "new user" definition is unstable. |
| **Time-to-first-value** | elapsed time from new user arrival to first meaningful engagement (lesson start, news read, question answered) | Diagnostic: if this is long or rare, activation is the bottleneck, not D1 pull. |
| **First-session completion rate** | % of new users who reach a defined "first value" moment in session 0 | Separates "didn't return" from "never got value in the first place." |

---

### Guardrail Metrics

*Guardrails ensure the solution doesn't improve D1 while harming something else.*

| Metric | Definition | Risk if ignored |
|--------|------------|-----------------|
| **Day 7 Retention** | % of new users returning on Day 7 | A D1 lift that doesn't carry to D7 suggests we're gaming the metric (e.g., a naggy notification that produces one extra open but no habit). |
| **Day 30 Retention** | % of new users returning on Day 30 | Long-term validity check; low sample early, but track. |
| **Session duration (Day 1 vs Day 0)** | Average session length on return day vs first day | If D1 returners spend 30s on Day 1 vs 5 min on Day 0, the "return" may be a bounce, not engagement. |
| **Notification opt-in rate** | % of new users who grant push notification permission | If our solution depends on push and opt-in is low, the lever is capped. |
| **Notification dismissal/uninstall rate** | % of users who dismiss the D1 notification or uninstall after receiving it | Guard against annoying users into returning once but damaging long-term retention or brand. |
| **Crash rate (Day 0 session)** | % of first sessions that end in a crash | Stability is a prerequisite; if crash rate is high, retention work is premature. |
| **Onboarding completion rate** | % of new users who complete onboarding (vs abandon) | If onboarding is the drop-off point, D1 interventions on the back end won't help. |

---

### Diagnostic Metrics

*These explain **why** D1 moves — they are the leading indicators and segment breakdowns used during the 4-week iteration.*

| Metric | Definition | Decision enabled |
|--------|------------|------------------|
| **First action distribution** | % of new users whose first action is lesson / news / interview / browse / abandon | If most users browse-and-leave, the fix is first-action guidance, not D1 reminders. |
| **Lesson completion rate (first lesson)** | % of users who start a lesson and reach a defined "completed" state | If completion is low, the lesson experience itself is the issue. |
| **End-of-session state viewed** | Which screen/state the user last saw before session close (lesson complete, home, progress dashboard, news article, interview result) | Reveals whether users leave with a "next step" visible. |
| **Streak state at session end (Day 0)** | Streak count shown to user at end of first session (0? 1?) | Tests whether the streak mechanic is even visible/active for a first-session user. |
| **Notification receipt & open (Day 1)** | % of users who received a Day 1 notification, % who opened it, % who opened and had a session | Direct measure of the D1 trigger lever. |
| **Re-engagement path taken on Day 1** | If user returns, which surface did they enter through (notification deep link, home screen, fresh content prompt, streak reminder) | Tells us which return path works. |
| **Cohort D1 trend (week-over-week)** | D1 rate for each weekly cohort, plotted over time | Shows whether the 16% is stable, improving, or declining — and whether any change coincides with prior releases (onboarding redesign, crash fixes). |
| **New user volume per cohort** | Count of new users per cohort | Sample size check: if cohorts are small, D1 rate swings are noisy and we need rollups or longer measurement windows. |

---

## D1 Retention Funnel

The funnel traces a new user from arrival through D1 return. Each stage has an event, properties, a metric, an interpretation, and a decision it enables.

> **TBD throughout:** exact event names, property keys, and thresholds. These must be mapped to whatever analytics platform Unrot uses (likely Firebase Analytics, Mixpanel, Amplitude, or custom). The structure below is platform-agnostic.

---

### Stage 1 — New User (Arrival)

| Element | Definition |
|---------|------------|
| **Event** | `new_user` (or `first_open`, `app_install`, `sign_up` — TBD based on "new user" definition) |
| **Properties** | `user_id`, `session_id`, `timestamp`, `source` (acquisition channel/campaign), `platform` (iOS/Android/Web), `app_version`, `is_returning_install` (boolean — has this device opened the app before?) |
| **Metric** | New users per cohort (count) |
| **Interpretation** | The denominator entry point. Defines who is in scope for D1 measurement. |
| **Decision enabled** | If new-user volume is trending down, D1 rate changes may be cohort-quality effects. If a specific source dominates new users and has low D1, acquisition may be the lever. |

**TBD:** Is `new_user` triggered on first-ever open, first open after install, or first sign-up? This choice materially changes the denominator and must match how the 16% was originally computed.

---

### Stage 2 — Onboarding

| Element | Definition |
|---------|------------|
| **Event** | `onboarding_started`, `onboarding_completed` |
| **Properties** | `onboarding_step` (if multi-step), `onboarding_duration_ms`, `selected_pathway` / `selected_level` / `selected_interest` (TBD — what does onboarding ask?), `granted_notification_permission` (boolean), `opted_into_streak` (boolean, if applicable) |
| **Metric** | Onboarding completion rate = `onboarding_completed` / `onboarding_started` |
| **Interpretation** | Measures whether users are getting through the setup to reach the product. Low completion = onboarding is a wall, not a welcome. |
| **Decision enabled** | If onboarding completion is low, D1 work should start here (simplify onboarding, defer permission requests, reduce steps). If completion is high, the problem is downstream. |

**TBD:** Number of onboarding steps, what choices are presented, whether notification permission is requested during onboarding, whether the user must create an account before seeing content.

---

### Stage 3 — First Value

| Element | Definition |
|---------|------------|
| **Event** | `first_value_achieved` (TBD — the first moment the user gets clear value: lesson started? lesson completed? news article opened? interview question answered?) |
| **Properties** | `first_value_type` (lesson / news / interview / other), `first_value_id` (content item ID), `time_to_first_value_ms` (from `new_user` timestamp), `first_value_duration_ms` |
| **Metric** | First-value achievement rate = `first_value_achieved` / `new_user` |
| **Interpretation** | Separates users who actually got value from those who browsed and left. This is the "activation" moment. |
| **Decision enabled** | If first-value rate is low, D1 retention is likely a symptom of a failure to activate. The solution is to get more users to first value, not to remind them to come back. If first-value rate is high, the problem is the pull to return after value was delivered. |

**TBD:** The definition of "first value" is the most important unresolved design choice in this funnel. It must be a moment that is (a) reliably trackable, (b) genuinely valuable to the user, and (c) achievable in a first session. Recommended candidates: lesson completed, news article read past a time threshold, interview question answered. Avoid "app open" or "screen view" as first value — too low a bar.

---

### Stage 4 — Lesson Engagement

| Element | Definition |
|---------|------------|
| **Event** | `lesson_started`, `lesson_progress` (periodic, TBD), `lesson_interactive_event` (quiz answer, tap, swipe — TBD) |
| **Properties** | `lesson_id`, `lesson_topic`, `lesson_difficulty`/`level`, `time_in_lesson_ms`, `interaction_count`, `first_interaction_time_ms` |
| **Metric** | Lesson engagement rate = users with ≥1 lesson interaction / users who started a lesson. Also: average time in lesson, interaction depth. |
| **Interpretation** | Measures whether users are passively viewing or actively engaging. Passive consumption may deliver less value and less reason to return. |
| **Decision enabled** | If engagement is shallow (users open lessons but don't interact), the lesson format may be part of the value problem. If engagement is deep, the lesson experience is probably not the D1 bottleneck. |

**TBD:** What constitutes an "interaction"? Minimum interaction count to count as "engaged"?

---

### Stage 5 — Lesson Completion

| Element | Definition |
|---------|------------|
| **Event** | `lesson_completed` |
| **Properties** | `lesson_id`, `completion_time_ms`, `total_time_ms`, `quiz_score` / `self_assessed_understood` (if applicable), `next_lesson_id` (if a sequence exists) |
| **Metric** | Lesson completion rate = `lesson_completed` / `lesson_started` |
| **Interpretation** | A completed lesson is the strongest in-session value signal. Completion should produce a visible payoff (progress update, streak increment, "next lesson" prompt). |
| **Decision enabled** | If completion rate is high but D1 is low, the issue is what happens *after* completion (no next-step cue, no notification, no streak feel). If completion is low, the lessons themselves or the user's match to them may be the issue. |

**TBD:** The definition of "completed" — did the user reach the end screen? Pass a quiz? Spend a minimum time? This must be defined before this metric is meaningful.

---

### Stage 6 — Session Exit

| Element | Definition |
|---------|------------|
| **Event** | `session_end` (or `app_background`, `app_close` — TBD based on session definition) |
| **Properties** | `session_id`, `session_duration_ms`, `last_screen_viewed`, `total_interactions`, `content_consumed` (list or count), `streak_after_session` (streak count visible to user at exit), `readiness_score_after_session` (if shown), `has_next_action_visible` (boolean — was a "next lesson" / "continue" / "tomorrow's briefing" visible at exit?), `notification_scheduled` (boolean — was a D1 notification scheduled/fired as a result of this session?) |
| **Metric** | Session end state distribution = % of sessions ending at each `last_screen_viewed`. Also: % of sessions where `has_next_action_visible` = true. |
| **Interpretation** | This is the **most important diagnostic stage for D1 retention.** It captures what the user experienced as they left the app. Did they see a next step? Did their streak update? Did a notification get scheduled? |
| **Decision enabled** | If most sessions end with no next-action visible and no notification scheduled, the D1 lever is clearly in the end-of-session experience. If most sessions already show a next action and schedule a notification, the lever is elsewhere (notification copy/timing, streak feel, notification opt-in). |

**TBD:** `has_next_action_visible` is a custom telemetry flag that may not exist today — it may need to be instrumented as part of the 4-week solution evaluation. This is likely the highest-value new instrumentation.

---

### Stage 7 — D1 Return

| Element | Definition |
|---------|------------|
| **Event** | `session_start` on Day 1 (calendar day after the user's first session) |
| **Properties** | `user_id`, `day_number` (1), `return_trigger` (notification_open / deep_link / organic_open / streak_prompt / other — TBD), `return_path` (which screen did they enter through?), `session_duration_ms`, `return_value_achieved` (did they reach first value on Day 1?) |
| **Metric** | D1 Retention Rate = (users with ≥1 `session_start` on Day 1) / (users with ≥1 `first_value_achieved` on Day 0) — or / `new_user`, depending on denominator choice (TBD, must be consistent). |
| **Interpretation** | The north star. Measures whether the user came back. |
| **Decision enabled** | The primary scorecard for the 4-week effort. Movement from 16% → higher is the success criterion. Segmented by `return_trigger`, `first_value_type`, and `source` to understand **why** it moved. |

**TBD:**
- Exact Day 1 definition: calendar day in what timezone? (UTC? user-local? India timezone given the team's origin?) This matters for edge cases near midnight.
- What counts as a "session" on Day 1 — any app open, or a minimum engagement threshold? A 2-second open is technically a return; whether it should count is a product judgment call.

---

## Funnel Summary Table

| Stage | Event | Core Metric | TBD? |
|-------|-------|-------------|------|
| 1. New User | `new_user` / `first_open` | New users per cohort | Definition of "new user" |
| 2. Onboarding | `onboarding_started` → `onboarding_completed` | Onboarding completion rate | Onboarding steps, permission asks |
| 3. First Value | `first_value_achieved` | First-value achievement rate | Definition of "first value" |
| 4. Lesson Engagement | `lesson_started` → interactions | Lesson engagement rate | Interaction threshold |
| 5. Lesson Completion | `lesson_completed` | Lesson completion rate | Definition of "completed" |
| 6. Session Exit | `session_end` | End-state distribution; % with next-action visible | `has_next_action_visible` flag may need new instrumentation |
| 7. D1 Return | `session_start` on Day 1 | **D1 Retention Rate** | Timezone/session definition |

---

## Minimum Instrumentation for 4-Week Solution Evaluation

The goal: within 4 weeks, with 2 engineers, be able to say whether a proposed solution moved D1 retention — and why.

### Must-have (non-negotiable)

These are the events and properties without which we cannot evaluate any D1 retention solution:

| # | Event | Properties | Why it's required |
|---|-------|------------|-------------------|
| 1 | `new_user` | `user_id`, `timestamp`, `source`, `platform`, `app_version`, `is_returning_install` | Defines the cohort denominator. Without this, we cannot compute D1. |
| 2 | `session_start` | `user_id`, `session_id`, `timestamp`, `day_number` (relative to first session) | Defines both Day 0 and Day 1 sessions. Required to compute D1 and to segment by return trigger. |
| 3 | `session_end` | `session_id`, `duration_ms`, `last_screen`, `streak_after_session`, `has_next_action_visible`, `notification_scheduled` | Captures the end-of-session state — the most likely D1 lever. `has_next_action_visible` and `notification_scheduled` may need new instrumentation. |
| 4 | `first_value_achieved` | `user_id`, `timestamp`, `value_type`, `value_id`, `time_to_first_value_ms` | Activation diagnostic. Tells us whether D1 failures are activation failures in disguise. |
| 5 | `notification_sent` | `user_id`, `timestamp`, `notification_type` (lesson / news / streak / other), `expected_trigger_day` | Required to measure the D1 notification lever — receipt, open, and downstream session. |
| 6 | `notification_opened` | `user_id`, `timestamp`, `notification_type`, `deep_link_target` | Ties notification receipt to return behavior. |
| 7 | `onboarding_completed` | `user_id`, `timestamp`, `onboarding_duration_ms`, `granted_notification_permission` | Measures activation friction and notification opt-in at the point it happens. |

**Total: 7 events.** This is the minimum viable instrumentation layer. If any of these are missing today, they must be added before or during the 4-week solution window.

---

### Should-have (strongly recommended for diagnosis)

| # | Event | Properties | Why it adds signal |
|---|-------|------------|-------------------|
| 8 | `lesson_started` | `lesson_id`, `topic`, `level`, `timestamp` | Lets us segment D1 by lesson vs news vs interview, and by topic/level. |
| 9 | `lesson_completed` | `lesson_id`, `completion_time_ms`, `next_lesson_id` | Tests whether completion (vs start) predicts D1. |
| 10 | `streak_updated` | `user_id`, `timestamp`, `streak_count_after`, `streak_broken` (boolean) | Makes the streak mechanic observable. |
| 11 | `readiness_score_updated` | `user_id`, `timestamp`, `score_after` | Makes the readiness score observable as a potential retention driver. |

**Total: 4 additional events.** If engineering capacity is tight, prioritize #8 and #9 (lesson start/complete) over the score/streak telemetry — lesson-level segmentation is more actionable for a 4-week iteration than score telemetry.

---

### Nice-to-have (if capacity allows)

| # | Event | Properties | Why it adds signal |
|---|-------|------------|-------------------|
| 12 | `onboarding_step_viewed` | `step_name`, `timestamp`, `duration_ms` | Pinpoints which onboarding step causes drop-off if onboarding completion is low. |
| 13 | `content_browsed` | `content_type`, `content_id`, `timestamp`, `dwell_time_ms` | Captures browse-only users who never reach first value — a likely large non-return segment. |
| 14 | `interview_question_answered` | `question_id`, `role_filter`, `format`, `answered_correctly`, `timestamp` | Segments interview-prep users and measures whether interview prep drives D1 differently. |
| 15 | `news_article_opened` | `article_id`, `timestamp`, `duration_ms` | Segments news-driven users. |

---

### Instrumentation Gap Assessment

**TBD — requires access to current analytics schema.** Before the 4-week window starts, confirm:

1. **Which of the 7 must-have events already exist?** Map existing event names to the list above.
2. **Which properties are already captured?** Many events may exist but without the properties we need (e.g., `session_start` exists but without `day_number` or `return_trigger`).
3. **What is the current session definition?** How does the analytics platform define a session — app foreground/background, time threshold, explicit start/stop? This must match the D1 definition.
4. **What is the current "new user" definition?** Must match the denominator used to compute the 16%.
5. **Is there a notification event pipeline?** Can we track `notification_sent` and `notification_opened` today, or is that a new integration?
6. **What is the current onboarding flow?** What steps, what choices, what permission prompts? This determines what `onboarding_*` events to instrument.
7. **Is `has_next_action_visible` instrumentable?** This is a UI-state flag — it requires the app to emit a property at `session_end` reflecting what the user saw. Confirm this is feasible in the app codebase within the 4-week window.

---

## Measurement Plan for the 4-Week Window

### Pre-window (Week 0 — before solution work begins)

1. **Lock definitions.** Confirm: new user definition, session definition, Day 1 timezone, first-value definition, lesson-completion definition.
2. **Instrumentation audit.** Map must-have events (#1–7) against existing tracking. Identify gaps.
3. **Instrument gaps.** Add any missing must-have events and properties. Prioritize `session_end` properties (`has_next_action_visible`, `notification_scheduled`) and `notification_sent`/`notification_opened` if the solution involves push.
4. **Establish baseline.** Compute D1 retention for the most recent 4–8 weekly cohorts. Record the range and trend — not a single 16% number, but the variation around it. (The 16% is given; the spread and trend are TBD from data.)
5. **Set up the dashboard.** A single view showing: cohort D1 rate (trend), D1 by first-value type, D1 by source, onboarding completion rate, first-value rate, notification opt-in rate, notification open rate, D7 rate (if volume allows).

### During window (Weeks 1–4)

6. **Run the solution.** (Solution not yet designed — this is the measurement layer that will support whatever solution is chosen.)
7. **Weekly cohort tracking.** Each week, compute D1 for the new cohort and compare to baseline. Week-over-week noise is expected; look for a directional move sustained over 2+ cohorts.
8. **Segment every D1 change.** If D1 moves, decompose by: first-value type, source, notification trigger, end-of-session state. The segment breakdown tells you whether the solution worked via the intended mechanism or by accident.
9. **Watch guardrails weekly.** If D1 rises but D7 falls, or notification opt-in drops, or uninstall/dismissal rises, the solution may be trading short-term return for long-term damage.

### Post-window (end of Week 4)

10. **Decision gate.** Compare D1 rate for the solution cohort(s) against the baseline range. If the move is within the baseline noise, the solution did not move D1 — iterate or pivot. If the move is outside the baseline range and guardrails held, the solution is a candidate for broader rollout.

---

## Open Questions for the Analytics Lead

These are the questions that must be answered before the measurement model can be executed. They are not things I can answer from outside the product.

1. What analytics platform is in use, and what events are already tracked?
2. What is the exact event name and definition for a "session"?
3. What is the exact definition of "new user" used to compute the 16%?
4. What is the timezone used for Day 1 calculation?
5. Do `notification_sent` and `notification_opened` events exist today?
6. What does the current onboarding flow capture — steps, choices, permission prompts?
7. Is there an existing streak and readiness score system, and are streak updates and score updates emitted as events today?
8. What is the current new-user volume per week? (Determines whether weekly cohorts are large enough for 유의미한 comparison, or whether we need to roll up to biweekly/monthly.)
9. Are there any known data quality issues (missing events, double-counting, platform-specific gaps)?
10. Who is the analytics owner, and what is the fastest path to adding a new event property (e.g., `has_next_action_visible`)?

---

*No baseline values are stated in this document beyond the 16% D1 rate given in the assignment. All other values are TBD pending access to the product's analytics. This measurement model is designed to be platform-agnostic and to work with whatever analytics system Unrot currently uses, provided the must-have events can be instrumented or already exist.*

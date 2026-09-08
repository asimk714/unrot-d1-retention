# Unrot D1 Retention — Problem Framing

**Assignment:** Improve D1 retention from 16% → industry benchmark 22%
**Team:** 1 Product Designer, 2 Engineers, 4 weeks
**Date:** September 2026
**Status:** Discovery phase — no solutions proposed yet

---

## 1. Problem Framing

**The surface problem:**

> New users who sign up for Unrot and complete a first session are not returning on the calendar day after that session. Only 16% do, against an industry benchmark of 22%.

**Why this matters:**

- D1 retention is the leading indicator of whether a new user has formed any attachment to the product.
- If users do not return on D1, they are unlikely to form a habit, derive sustained value, or become retained long-term users.
- A 6-percentage-point gap to benchmark is a meaningful shortfall that, if closed, would compound into higher D7, D30, and eventual LTV.

**The deeper problem (not yet validated):**

> Something about the first-session experience — what users see, do, feel, or fail to achieve — does not give them a reason, a cue, or an ability to come back the next day.

This is a hypothesis. The real cause could be anywhere in the chain from acquisition source → onboarding → first session → post-session state → next-day context.

---

## 2. Known Facts vs Assumptions vs Unknowns

### FACT

- Unrot is a product for working professionals to learn about AI through short lessons, news, and interview preparation.
- D1 retention is defined as the percentage of new users who return on the calendar day after their first session.
- Current D1 retention: **16%**.
- Industry benchmark for comparable products: **22%**.
- Team capacity: 1 Product Designer, 2 Engineers, 4 weeks of development.
- Existing product analytics are available (tool unspecified, data not yet inspected).

### ASSUMPTION

- "Industry benchmark: 22%" is a meaningful comparison. The comparator set, definitional consistency (calendar day vs 24-hour window, session definition, cohort window), and product similarity are unverified.
- The 16% figure is measured correctly and consistently. No known instrumentation bugs, definition changes, or cohort contamination.
- The D1 retention shortfall is a product problem, not primarily an acquisition-quality problem. (If most new users come from low-intent channels, the lever may be upstream.)
- There is something actionable within the 4-week / 3-person constraint. The gap is not purely a mismatch between product positioning and audience, which would take longer to fix.
- "Return on D1" means any session, not a specific target action. A returning user who opens the app and closes it counts the same as one who completes a lesson.

### INFERENCE

- At 16% D1 retention, roughly 84% of new users who had a first session did not return the next calendar day. The majority of the drop-off happens between end-of-session and next-day open.
- If the product's core loop involves daily or near-daily engagement (e.g., "a short lesson a day"), then D1 is the first test of whether that loop is credible to the user.
- A 6-point gap to benchmark suggests the problem is fixable with iteration rather than a full pivot — benchmarks are rarely beaten by 2-3x through tuning, but gaps of this size are routinely closed with focused changes.

### UNKNOWN

- The actual analytics tool and what events are tracked. What is the definition of "session"? What is the definition of "new user" (first-ever, first in cohort window, registered vs logged-in)?
- The shape of the funnel: how many users reach each step of the first session, and where they drop off.
- D7 and D30 retention for the same cohort. Is D1 the problem, or is D1 a proxy for a broader retention problem?
- Segmentation: does D1 retention differ by acquisition channel, signup source, device, geography, or first-action taken?
- What new users actually *do* in their first session: which lesson, how long, do they complete it, do they see news, do they attempt interview prep?
- What happens after the first session: is there any follow-up mechanism (email, push, in-app)? If so, what is its performance?
- Qualitative understanding: why users say they did or did not return. None of this has been gathered yet.
- What the industry benchmark source is, what product(s) it covers, and whether the comparison is fair.
- Whether the 16% is stable over time or trending.
- The current onboarding flow, first-session layout, and any existing habit-formation mechanics (streaks, reminders, personalization, progress markers).

---

## 3. User Segments

Initial segmentation hypothesis — to be validated with data:

### By intent / job-to-be-done (see Section 4)

| Segment | Likely behavior in first session |
|---|---|
| Career-driven (interview prep focus) | Looks for interview questions, assesss own readiness |
| Curiosity-driven (AI news / general learning) | Browses short lessons, reads news |
| Tool-driven (wants to apply AI to work) | Seeks practical how-tos, may be dissatisfied with abstract content |
| Casual / opportunistic (landed via link, low intent) | Scans, may not engage deeply, low probability of return |

### By engagement depth in first session

| Segment | First-session signature |
|---|---|
| Deep engagers | Complete at least one lesson or substantial interaction |
| Browsers | View content but do not complete a unit |
| Drop-offs | Leave during onboarding or before any meaningful interaction |

### By return behavior (to be measured)

| Segment | Definition |
|---|---|
| D1 returners | The 16% — characterize their first session |
| D1 non-returners | The 84% — characterize their first session and look for patterns |

**Critical unknown:** which of these segments dominate the new-user population, and which drive the 16% vs the 84%?

---

## 4. Relevant JTBD (Jobs to Be Done)

Hypothesized jobs — each implies a different reason to return on D1:

### Job 1: "Help me feel prepared for an AI-related interview."
- **Anticipated return trigger:** User wants to continue preparing, check their progress, or tackle the next question.
- **Failure mode:** User completes one question and feels no momentum, no plan, no sense of "I should come back to this."
- **D1 implication:** If interview prep is the job, D1 return may depend on whether the first session surfaces a clear next step and a reason to continue.

### Job 2: "Keep me informed about AI without overwhelming me."
- **Anticipated return trigger:** News is episodic; user returns because there is new content, or because the product has made itself a reliable source.
- **Failure mode:** First session delivers news that is already old by the next day, or no news at all, or too much/too little.
- **D1 implication:** News-driven retention requires either fresh daily content or a reason to return that is not news-dependent.

### Job 3: "Teach me AI fundamentals in small, manageable pieces."
- **Anticipated return trigger:** Lesson series implies a next lesson; user feels they are making progress.
- **Failure mode:** First lesson feels isolated, not part of a curriculum; no progress marker; no cue to continue.
- **D1 implication:** Structured learning paths with visible progress are the classic retention mechanism; their absence may explain low D1.

### Job 4: "Help me apply AI to my work / be more productive."
- **Anticipated return trigger:** User tried something and wants to try more, or wants a specific answer to a work problem.
- **Failure mode:** Content is too abstract; user does not leave with something actionable they can use the next day.
- **D1 implication:** Practical, work-relevant payoff in the first session may be the strongest D1 driver for this segment.

**Key insight:** If Unrot serves multiple jobs and the first-session experience does not quickly identify which job the user has, the user may get generic content that does not match their job — and therefore no reason to return.

---

## 5. Current Product Habit / Core Loop

**Unknown in detail** — the existing product has not been described in the assignment. Inferred from the product description and typical patterns for this category:

**Hypothesized current loop:**

1. User arrives (signup, login, or guest).
2. User is presented with a selection of short lessons, news, and/or interview prep.
3. User picks one and consumes it (reads, watches, answers).
4. Session ends.
5. (Possibly) some post-session state: progress saved, content marked as seen, maybe a streak or "continue" prompt.
6. Next day: user must independently decide to return. No described external trigger (push/email) is confirmed.

**What a strong habit loop would require (for comparison):**

- **Trigger:** external (notification, email) or internal (habit, routine, unmet curiosity).
- **Action:** low-friction, clear what-to-do-next.
- **Variable reward:** new content, progress, social comparison, mastery signal.
- **Investment:** progress saved, personalization, content consumed that makes return more valuable (e.g., a series).

**Working hypothesis:** the current product may deliver the action and some reward, but is weak on trigger and/or investment — meaning the user must self-trigger on D1, and many do not.

This is a hypothesis, not a finding. The actual product needs to be inspected.

---

## 6. D1 Retention Funnel (Hypothesized)

The following is a **hypothesis** of the funnel stages. Exact stages and conversion rates must come from analytics.

```
New user (signup / first arrival)
  │
  ├──→ Onboarding complete (vs abandoned during onboarding)
  │
  ├──→ First meaningful interaction (vs session with no real engagement)
  │
  ├──→ First session completes / reaches a natural endpoint
  │
  ├──→ Post-session: user has a cue, progress, or reason to return
  │
  └──→ D1 return (any session on the next calendar day)
```

**Within the 84% who do not return on D1, the breakdown is unknown:**

- How many never had a meaningful first session?
- How many completed a session but had no post-session cue?
- How many may have returned but were not captured due to session-definition issues?

**Critical unknown:** at which funnel stage the largest drop-off sits. The intervention point depends entirely on this.

---

## 7. Candidate Reasons a New User May Not Return on D1

Organized by category. Each is a hypothesis to test, not a finding.

### A. First-session value gap (the user did not get enough from session 1)

- **A1.** The first session did not deliver a satisfying payoff — content felt too short, too shallow, too generic, or not relevant to the user's job.
- **A2.** The user did not complete anything meaningful — dropped off during onboarding or early in the session, leaving no sense of accomplishment.
- **A3.** The user's specific job (interview prep, news, fundamentals, practical application) was not served by the content they saw; they got generic content that felt irrelevant.
- **A4.** The content was good but not memorable — the user consumed it and forgot about the product by the next day (no hook, no standout moment).

### B. No cue or trigger to return

- **B1.** No external trigger (push notification, email, reminder) exists or is effective — the user must remember to return on their own.
- **B2.** Any existing trigger is generic/poorly timed and is ignored or dismissed.
- **B3.** The product does not create an internal trigger — the user does not associate Unrot with a routine, a need, or a curiosity that would recur on D1.

### C. No sense of progress or investment (no reason to continue)

- **C1.** No visible progress marker (streak, completed count, course progress) that makes returning feel like continuing rather than starting over.
- **C2.** No series or curriculum structure that implies a "next lesson" — the first session feels like a one-off.
- **C3.** No personalization or adaptation — the second-session experience would be indistinguishable from the first, reducing the value of returning.
- **C4.** No social or comparative element (leaderboard, peer progress) that creates a reason to check back.

### D. Friction / usability issues

- **D1.** Returning is harder than it should be — login friction, confusing navigation, degraded experience on second open.
- **D2.** The first session was frustrating in a way that suppressed return intent (slow, buggy, confusing).
- **D3.** The user intended to return but forgot — a memory/constraint problem, not a product-value problem.

### E. Audience / acquisition mismatch

- **E1.** A large share of new users come from low-intent sources (impulse clicks, viral links) and never intended to form a habit — the 16% reflects audience quality, not product quality.
- **E2.** The product's positioning attracts users with a job the product does not actually serve well, so even a good first session does not create return intent.

### F. Measurement / definition issues

- **F1.** "Session" definition is too narrow — some users who opened the app did not trigger a tracked session.
- **F2.** "New user" definition includes users who are not truly new (reinstalls, returning after a long gap), inflating the denominator.
- **F3.** Technical instrumentation gaps cause D1 returns to be undercounted.

**Note:** Reason F is a prerequisite check. If F is true, the 16% itself is unreliable and the first action is instrumentation correction, not product change.

---

## 8. Analytics to Inspect

Priority order — each answers a specific discovery question.

### 8.1 Definition and data-quality checks

1. **Event taxonomy and session definition.**
   - What events are tracked? What constitutes a "session" (app open, time on page, explicit start/stop)?
   - How is "new user" defined — first-ever, first in a window, registered vs anonymous?
   - How is D1 calculated — calendar day in what timezone? Rolling 24-hour window?

2. **Data completeness.**
   - Are there known instrumentation gaps, missing events, or platform-specific tracking issues (e.g., mobile vs web)?
   - Is there any known bug or recent change that could have affected the 16% measurement?

### 8.2 Funnel analysis — first-session journey

3. **First-session funnel.**
   - Signup/arrival → onboarding complete → any content interaction → content completed → session end.
   - Drop-off at each stage. Where is the biggest loss?

4. **First-action breakdown.**
   - What do new users do first — lesson, news, interview prep, browse, search?
   - Is there a first action that correlates strongly with D1 return?

5. **Session depth and duration.**
   - Time in session, number of items consumed, completion rate.
   - Do D1 returners have systematically deeper/longer/shorter first sessions than non-returners?

### 8.3 Segmentation

6. **D1 retention by acquisition channel / source.**
   - Does the 16% hold across channels, or is it dragged down by specific sources?

7. **D1 retention by first action taken.**
   - Which first actions are associated with higher/lower D1 return?

8. **D1 retention by device, platform, geography (if data exists).**

9. **Cohort-over-time view.**
   - Is 16% stable by week, or trending? Are there cohorts that performed better?

### 8.4 Post-session and return behavior

10. **Post-session state.**
    - What does a user see at the end of a session? Is there a "continue," "next lesson," or progress view?
    - Is there any follow-up mechanism (push, email) — and if so, delivery, open, and return rates?

11. **D1 returner characteristics.**
    - Build a profile of the 16%: what did they do in session 1? What channel? What first action? How long did they stay?
    - Contrast with the 84%.

12. **D7 and D30 retention for the same cohorts.**
    - Is D1 the binding constraint, or are D1 returners also dropping off later? (If D1 returners retain well at D7/D30, fixing D1 is high-leverage. If D1 returners also fall off quickly, the problem may be broader.)

### 8.5 Content and product mechanics

13. **Content consumption patterns.**
    - Which lessons/news/prep items are most consumed by new users? Which are most completed?
    - Is there content that new users never see (buried, not surfaced in first session)?

14. **Existing habit mechanics.**
    - Are there streaks, reminders, progress bars, personalization, or recommendation in the current product? How are they performing?

---

## 9. User Research to Run

Qualitative work to explain the *why* behind the numbers. Prioritized by speed and signal.

### 9.1 New-user interviews (highest priority)

**Target:** Users from the most recent cohorts who completed a first session.

**Two cohorts to recruit:**

- **D1 returners (the 16%):** Why did they come back? What was the trigger? What did they get from session 1 that made return feel worthwhile?
- **D1 non-returners (the 84%):** Why did they not return? Did they intend to and forget? Were they unimpressed? Did they not know what to do next? Did life get in the way?

**Key questions (non-exhaustive):**

- What were you hoping to get from Unrot when you first opened it?
- Walk me through your first session — what did you do, what did you think?
- Did you leave with a clear sense of what to do next? If so, what?
- Did you plan to come back? If yes, what happened? If no, why not?
- What would have made you more likely to return the next day?
- (For returners) What specifically brought you back?

**Sample size target:** enough to reach thematic saturation on the main reasons — typically 8–12 per cohort, adjusted to timeline.

### 9.2 First-session usability observation

- Watch (live or via recording) new users go through onboarding and their first session.
- Note where they hesitate, what they miss, what they expect but don't find.
- Specifically test: can a new user, unguided, figure out what to do next after finishing a first item? Do they perceive a "continue" path?

### 9.3 Exit / drop-off surveys (lightweight, if feasible)

- At session end or on the day after a first session with no return, a single-question prompt: "What stopped you from coming back?" with a few choices + free text.
- Low sample bias risk if delivered immediately; high signal for top reasons.

### 9.4 Channel / source qualitative check

- If acquisition channels are diverse, understand what each channel's users expected vs what they got. A mismatch here can explain a large share of non-return.

### 9.5 Competitive / benchmark sanity check

- Briefly understand what comparable products do at the end of a first session and on D1 — do they send a reminder, surface a next step, show progress, ask for a commitment?
- This is context, not data; use to sanity-check hypotheses, not to copy features.

---

## 10. Key Hypotheses

These are the working hypotheses to test during discovery. They are not yet prioritized; each implies different interventions.

### H1 — First-session payoff gap

> New users who do not return on D1 had a first session that did not deliver a satisfying, relevant, or memorable payoff — they consumed something but left without a reason to come back.

**Test:** Compare first-session depth, completion, and content type between D1 returners and non-returners. Run interviews to learn whether non-returners felt the session was worthwhile.

### H2 — No next-step cue

> The product does not give new users a clear, compelling "what to do next" at the end of the first session, so returning requires the user to generate their own intent.

**Test:** Usability observation — does a new user perceive a next step? Interview — did users leave knowing what they would do next? Analytics — is there a "continue" surface and do users who engage with it return at higher rates?

### H3 — Missing or weak external trigger

> There is no effective external trigger (push/email/reminder) reaching users on or before D1, so return depends on unprompted recall.

**Test:** Check whether any follow-up mechanism exists and its performance. If none exists, this is a structural gap. If one exists, check delivery and response.

### H4 — No progress / investment mechanic

> The first session does not create a sense of progress, investment, or series membership — there is no visible "I'm making headway" signal that makes returning feel like continuation.

**Test:** Audit the product for progress markers, streaks, curriculum structure, and personalization. Survey whether D1 returners cite progress as a reason.

### H5 — Job-to-be-done mismatch in first session

> The product serves multiple jobs (interview prep, news, fundamentals, practical application) but the first-session experience does not quickly identify and serve the user's specific job, so users receive generic content that does not fit.

**Test:** Analyze first-action choices and D1 return by first action. Interview — did users feel the content matched what they came for?

### H6 — Acquisition quality / audience mismatch

> A meaningful portion of new users arrive with low intent (impulse, one-off curiosity) and were never likely to return regardless of first-session quality.

**Test:** Segment D1 by acquisition channel. If low-intent channels dominate the non-return group, the lever may be acquisition rather than product.

### H7 — Measurement artifact

> The 16% is understated due to session definition, timezone, or instrumentation issues — the true D1 retention is higher (or the gap to benchmark is different).

**Test:** Audit the measurement definition and data pipeline before acting on the number.

---

## 11. Opportunity Areas

These are the zones where a solution might live, derived from the hypotheses above. They are not solutions; they are search spaces.

### Opportunity 1 — Make the first session deliver a stronger, more relevant payoff

- Improve the relevance and completeness of what a new user experiences in session 1.
- Ensure the user leaves having consumed something that feels worthwhile and matched to their job.
- Includes: content quality, content matching to user intent, depth/length appropriateness, memorability.

### Opportunity 2 — Give every new user a clear "what to do next"

- At the end of the first session, and in the post-session state, make the next step obvious and attractive.
- Includes: "continue" paths, series/curriculum surfacing, progress visibility, personalized next recommendation.

### Opportunity 3 — Add or improve an external D1 trigger

- A well-timed, well-crafted notification, email, or in-product prompt that reaches the user on or before D1 with a reason to return.
- Includes: timing, messaging, channel choice, opting-in, frequency.

### Opportunity 4 — Build a sense of progress and investment from session 1

- Visible progress markers, streaks, completion signals, series membership, or any mechanic that makes returning feel like continuing a journey rather than restarting.
- Includes: onboarding that sets up the progress frame, early wins that establish momentum.

### Opportunity 5 — Surface and serve the user's specific job earlier

- Quickly identify whether the user is here for interview prep, news, fundamentals, or practical application, and route the first session accordingly.
- Includes: onboarding question, smart defaults, first-action guidance, content organization.

### Opportunity 6 — Improve acquisition quality or alignment

- If the data shows that low-intent channels drive a disproportionate share of non-return, the lever may be to adjust acquisition, set expectations in onboarding, or qualify users earlier.
- Includes: channel strategy, landing-page expectation-setting, onboarding qualification.

### Opportunity 7 — Fix measurement before acting

- If the audit in Section 8.1 reveals definition or instrumentation problems, correct those first so that the 16% → 22% target is grounded in a reliable number.

---

## How This Frame Will Be Used

This document is the discovery output. The next step — not yet taken — is to:

1. Inspect the actual analytics (Section 8) to replace unknowns with facts and inferences.
2. Run the user research (Section 9) to test the hypotheses in Section 10.
3. Narrow from opportunity areas (Section 11) to a prioritized set of solutions, evaluated against the 4-week / 3-person constraint.
4. Build a prototype and a slide deck as required by the assignment.

No solution is proposed in this document. The hypotheses and opportunity areas are explicitly unvalidated and are a plan for investigation, not a recommendation.

---

*Document status: Draft — discovery phase. Awaiting analytics inspection and user research to convert assumptions and unknowns into facts.*

# Unrot D1 Retention - Product Case Study

> Improving Day-1 retention from a 16% assignment baseline toward a 22% benchmark by designing a stronger return loop after the first learning session.

A product case study covering problem diagnosis, product strategy, prioritization, interaction design, experimentation, instrumentation, execution planning, and implementation.

---

## Product Decision

**Make the next session feel worth returning for.**

The core intervention is **Tomorrow's 5-Minute Mission**.

After completing the first lesson, Unrot gives the learner a specific, achievable mission for tomorrow, optionally lets them choose a reminder time, creates a clear return cue, and brings the learner directly toward that promised experience when they return.

The objective is not simply to improve first-session completion.

It is to create a concrete reason for a new learner to come back on Day 1.

---

## Case Study at a Glance

| | |
|---|---|
| **Product problem** | Weak handoff between the first session and the next session |
| **Primary metric** | Day-1 retention |
| **Assignment baseline** | 16% |
| **Benchmark / context** | 22% |
| **Gap to close** | +6 percentage points |
| **Timebox** | 4 weeks |
| **Squad** | 1 Product Designer + 2 Engineers |
| **Deliverable** | Working prototype + executive product deck |
| **Approach** | Diagnose → prioritize → prototype → instrument → experiment → learn |

### Evidence discipline

**16%** is the assignment-provided baseline.

**22%** is the assignment benchmark / context. It is not a measured result or guaranteed target.

No experiment was run and **no D1 improvement is being claimed**.

The prototype demonstrates the proposed product intervention, user journey, and measurement design. It does not represent measured product performance.

---

# 1. The Product Problem

A new learner can successfully complete their first learning session without having a strong reason, cue, or commitment to return the following day.

The critical product opportunity is therefore the **handoff between sessions**.

### Current behavioral journey

```text
Discover
   |
   v
Start first lesson
   |
   v
Experience value
   |
   v
Complete lesson
   |
   v
Session ends
   |
   v
No concrete next action
   |
   v
Weak return motivation
   |
   v
Drop-off before D1
```

### The product gap

The first session can successfully answer:

> "Did I learn something today?"

But it does not necessarily answer:

> "Why should I come back tomorrow, and what exactly will I do?"

That makes the transition from today's value to tomorrow's behavior fragile.

### Senior PM framing

Before deciding which feature to build, the key behavior to change is:

**Turn an implicit intention to return into a concrete next action.**

---

# 2. What We Need to Learn

The diagnosis creates several questions that should be validated with real product data before a production rollout.

### Week 1 questions

1. Where does first-session drop-off concentrate?
2. Does completing the first lesson correlate with D1 return?
3. Which parts of the current session-end experience create or fail to create return intent?
4. Will a concrete next mission increase intent to return?
5. Will users opt into a low-friction reminder when the future value is clear?
6. Does reducing the friction between notification and lesson start improve return-session completion?

These are **hypotheses to validate**, not conclusions presented as measured facts.

### Validation principle

**Validation > intuition**

The assignment provides the D1 context and access to existing analytics, but no raw cohort data was available for this case study.

---

# 3. Product Strategy

## Turn "come back tomorrow" into a concrete commitment.

The intervention is deliberately narrow.

Instead of rebuilding onboarding, rewards, social features, personalization, or the broader learning experience, change the **end-of-session moment** where the user already has intent and attention.

### Three product levers

| Lever | Product behavior | Why it matters |
|---|---|---|
| **Next mission** | Show the exact 5-minute lesson waiting tomorrow | Removes ambiguity |
| **Optional time** | Let the learner choose a reminder time | Creates a return cue |
| **Deep-link return** | Open directly into the promised mission | Removes friction |

### Design principle

> **Reduce cognitive load at the exact moment intent to return is formed.**

The intervention is designed around Unrot's 5-minute learning habit, daily learning framing, courses, progress, and streak behavior.

---

# 4. Tomorrow's 5-Minute Mission

The core experience is a lightweight post-completion loop.

### User journey

```text
TODAY

Complete Lesson 1
       |
       v
Reveal tomorrow's mission
       |
       v
Optional reminder time
       |
       v
Create return cue
       |
       v

D1

Notification / return cue
       |
       v
Open promised mission
       |
       v
Start D1 lesson
       |
       v
Continue the learning habit
```

### What changes for the learner

**Before**

> "I learned something."

**After**

> "Tomorrow, I know exactly what I'm doing."

### Final mission copy

> **"Tomorrow, you'll write your first better prompt - and see the difference clarity makes."**

The mission is intentionally:

- specific
- achievable in approximately five minutes
- connected to the next learning value
- understandable without additional explanation
- low commitment
- immediately actionable

---

# 5. Behavioral Loop

The intervention creates a simple behavioral chain:

```text
VALUE
Complete today's lesson
        |
        v
FUTURE VALUE
See tomorrow's specific mission
        |
        v
COMMITMENT
Choose an optional reminder
        |
        v
CUE
Receive return notification
        |
        v
LOW FRICTION
Open directly into the promised mission
        |
        v
VALUE
Complete the next lesson
```

Or more simply:

```text
Today
  |
  v
Complete lesson
  |
  v
Commit
  |
  v
See tomorrow
  |
  v
Cue
  |
  v
Return on D1
  |
  v
Resume mission
```

The product bet is not "send more notifications."

The bet is:

**Make tomorrow concrete before today ends, then remove friction when tomorrow arrives.**

---

# 6. Product Hypothesis

> **If new learners leave their first session with a specific, low-effort mission and a clear return cue, then D1 retention should improve because the next session has both a reason to happen and a lower-friction path to happen.**

### Why this hypothesis is testable

The intervention changes identifiable behaviors:

- lesson completion
- mission exposure
- reminder selection
- notification delivery
- notification open
- D1 session start
- D1 lesson completion

That makes it possible to measure both the intended outcome and the path leading to it.

---

# 7. Why This Intervention

### 1. Specificity

A named next action is easier to act on than a generic instruction to "come back tomorrow."

### 2. Low commitment

The next action remains consistent with the five-minute learning habit.

### 3. Reduced friction

The user does not need to remember what they were supposed to do or navigate through the product to find it.

### 4. Optionality

Reminder time is optional rather than mandatory.

If the user declines notifications, the in-product plan remains available.

### 5. Tight experiment scope

The intervention changes a specific part of the journey rather than introducing a broad feature release.

This keeps the experiment easier to instrument, interpret, and roll back.

---

# 8. Prototype

## Working product prototype

[Open the final prototype](prototype/Unrot_D1_Retention_FINAL.html)

The prototype demonstrates the proposed end-to-end experience:

```text
Onboarding
    |
    v
First learning session
    |
    v
Knowledge check
    |
    v
Lesson completion
    |
    v
Tomorrow's 5-Minute Mission
    |
    v
Optional reminder
    |
    v
Notification simulation
    |
    v
Deep-link return
    |
    v
D1 return experience
    |
    v
D1 lesson
    |
    v
D1 completion
```

### Prototype characteristics

- Standalone HTML release artifact
- Local embedded React runtime
- No external CDN dependency
- No build step required for the final artifact
- Meaningful interaction and state transitions
- Knowledge-check behavior
- Reminder decision behavior
- Notification simulation
- D1 return/deep-link behavior
- Analytics event simulation
- Consumer-facing developer controls removed from the final flow

### Prototype boundary

This is a **product prototype**, not a production backend.

The following are simulated:

- notifications
- analytics persistence
- backend services
- experiment infrastructure
- production database behavior

The prototype exists to make the product bet tangible and testable at the interaction level.

---

# 9. Measurement & Experiment Design

## Primary decision metric

**Day-1 retention**

The intervention should ultimately be judged by whether more users return on Day 1.

The benchmark provides a reference point of **22%**, compared with the assignment baseline of **16%**.

The resulting gap is:

**+6 percentage points**

This is a planning target / benchmark gap, not an observed improvement.

### No metric laundering

Time-in-app, notification opens, or intermediate engagement should not be treated as success if D1 return does not improve.

The primary decision metric remains:

> **Did more users return on Day 1?**

---

# 10. Experiment Design

### Control

Existing end-of-session experience.

### Treatment

**Tomorrow's 5-Minute Mission**

Including:

1. specific next mission
2. optional reminder preference
3. return cue
4. direct return into the promised experience

### Measurement chain

```text
Session 1
   |
   v
Lesson started
   |
   v
Lesson completed
   |
   v
Mission shown
   |
   v
Reminder decision
   |
   v
Notification sent
   |
   v
Notification opened
   |
   v
D1 session started
   |
   v
D1 lesson completed
```

### Proposed event chain

```text
new_user
    ->
onboarding_completed
    ->
lesson_started
    ->
first_value_achieved
    ->
lesson_completed
    ->
session_end
    ->
notification_sent
    ->
notification_opened
    ->
session_start_d1
```

The event chain is designed to help answer:

- Did the user reach the intervention?
- Did they choose a reminder?
- Was the return cue delivered?
- Did they engage with it?
- Did they actually return?
- Did they complete the intended D1 experience?

---

# 11. Guardrail Metrics

The primary metric should not improve at the expense of product quality or trust.

### Engagement

**Lesson completion should not fall.**

The intervention should not make the first session feel harder or interrupt learning completion.

### Trust

Monitor:

- reminder opt-out
- reminder disable behavior
- notification complaints
- excessive notification frequency

### Quality

D1 return sessions should open the **intended lesson / mission**.

### Experiment integrity

Monitor:

- treatment assignment persistence
- test-account exclusion
- internal traffic exclusion
- cohort contamination

### Segmentation

Where data allows, compare outcomes by:

- user role
- acquisition source
- device
- first-session completion behavior
- other meaningful product cohorts

---

# 12. Prioritization

The principle is:

> **Ship the smallest loop that can move D1 in four weeks.**

Prioritization considers:

- expected impact
- confidence
- effort
- dependency risk

| Priority | Work item | Impact | Confidence | Risk | Decision |
|---|---|---:|---:|---:|---|
| P0 | Completion → next-lesson preview | High | Medium | Low | Ship |
| P0 | Reminder preference + delivery hook | High | Medium | Medium | Ship |
| P0 | D1 deep link + home state | High | High | Low | Ship |
| P0 | Event instrumentation + experiment flags | High | High | Low | Ship |
| P1 | Smarter next-lesson recommendation | Medium | Medium | Medium | Later |
| P2 | Social / rewards / leaderboards | Unknown | Low | High | Not now |

### Scope rule

**Do not spend the four-week window rebuilding the product.**

> Instrument → ship → test → learn.

---

# 13. What Is Deliberately Deferred

The following ideas are intentionally outside the first experiment:

- advanced personalization
- smarter recommendation algorithms
- social features
- leaderboards
- additional reward mechanics
- broad gamification
- major platform changes

These may become valuable later, but they would make the initial retention experiment harder to interpret.

The product decision is to learn from a **focused retention loop first**.

---

# 14. Four-Week Execution Plan

## Week 1 - Diagnose

**Objective:** validate the behavioral diagnosis.

Work:

- cohort analysis
- first-session funnel analysis
- identify first-session drop-offs
- define event taxonomy
- assess reminder feasibility
- confirm D1 measurement definition

Output:

**Validated problem framing + experiment-ready measurement plan**

---

## Week 2 - Build

**Objective:** build the smallest viable intervention.

Work:

- completion trigger
- next-lesson preview
- tomorrow mission
- reminder preference
- feature flag
- basic return-state handling

Output:

**Treatment experience ready for instrumentation**

---

## Week 3 - Instrument

**Objective:** connect the experience to measurable D1 behavior.

Work:

- D1 deep link
- notification hook
- analytics events
- QA
- edge-case testing
- analytics validation
- experiment readiness

Output:

**End-to-end experiment-ready flow**

---

## Week 4 - Learn

**Objective:** run the experiment and make a decision.

Work:

- launch A/B test
- monitor guardrails
- analyze early cohorts
- inspect segments
- compare treatment vs control
- decide whether to scale, iterate, or roll back

Output:

**Evidence-based product decision**

---

# 15. Experiment Readiness Criteria

The experiment should not launch simply because the UI works.

### Ready

All of the following should work end-to-end:

- experiment flag
- treatment assignment
- analytics
- reminder path
- D1 deep link
- intended lesson routing

### Observe

The team should be able to query:

- baseline cohort
- treatment cohort
- D1 outcomes
- intermediate funnel events
- meaningful user segments

### Decide

Success and stop criteria should be agreed **before** interpreting the results.

This prevents post-hoc interpretation.

---

# 16. Decision Rules

### SCALE

Scale the intervention if:

- D1 retention improves meaningfully versus control
- the result is directionally and statistically credible for the experiment design
- lesson completion remains healthy
- reminder opt-out / disable behavior remains healthy
- return sessions route correctly

### ITERATE

Iterate if:

- the signal is positive but below the desired level
- the intervention is reaching users but friction remains
- specific cohorts respond differently
- reminder adoption or deep-link behavior creates a clear optimization opportunity

### ROLL BACK

Roll back if:

- there is no meaningful D1 improvement
- the experiment introduces material trust problems
- lesson completion declines materially
- notification behavior becomes intrusive
- the return experience routes incorrectly
- experiment integrity is compromised

---

# 17. Architecture

## Keep the implementation boring on purpose.

The experiment does not require a platform rewrite.

### Proposed production implementation

| Layer | Approach |
|---|---|
| **UI** | Home + lesson completion + mission + reminder state |
| **Backend** | Existing app services / API + feature flag |
| **Data** | Existing analytics + retention query |
| **Notifications** | Existing push/email capability |
| **Experimentation** | Persistent treatment assignment |
| **Security** | Consent, preference controls, minimal notification payloads |

The production implementation should reuse Unrot's existing stack rather than introduce unnecessary infrastructure for a four-week experiment.

---

# 18. Failure Modes & Mitigations

### Reminder permission denied

**Risk:** User cannot receive the reminder.

**Mitigation:** Keep the tomorrow plan available in-product. Notifications are optional, not mandatory.

---

### Wrong or unavailable lesson

**Risk:** The promised mission is no longer available.

**Mitigation:** Fall back to the next eligible lesson from the existing learning path.

---

### Notification spam

**Risk:** Too many notifications reduce trust.

**Mitigation:**

- frequency caps
- easy disable path
- monitor opt-out behavior
- keep notification content concise and relevant

---

### Experiment contamination

**Risk:** Test accounts or users moving between cohorts distort results.

**Mitigation:**

- persist treatment assignment
- exclude internal/test traffic
- monitor cohort integrity

---

### Deep-link failure

**Risk:** The notification opens the wrong screen.

**Mitigation:** Validate the destination as a release criterion and monitor the correct D1 lesson routing.

---

# 19. Security & Privacy Considerations

The retention loop should not require sensitive data in notification payloads.

Principles:

- explicit notification consent
- user-controlled reminder preferences
- easy notification disable path
- minimal notification payload
- no sensitive learning data exposed through notifications
- predictable fallback behavior when permissions are unavailable

The product should improve retention without creating unnecessary trust or privacy costs.

---

# 20. Research & Product Documentation

The repository includes supporting product work behind the final recommendation.

| Document | Purpose |
|---|---|
| [`research/problem-framing.md`](research/problem-framing.md) | Problem diagnosis and behavioral framing |
| [`research/product-teardown.md`](research/product-teardown.md) | Product/context teardown |
| [`research/interventions.md`](research/interventions.md) | Intervention exploration and rationale |
| [`research/measurement-model.md`](research/measurement-model.md) | Metric and experiment design |
| [`research/prd.md`](research/prd.md) | Product requirements and implementation framing |
| [`research/adversarial-review.md`](research/adversarial-review.md) | Critical review, risks, and challenge to the proposed solution |

These documents provide the reasoning layer behind the prototype and executive recommendation.

---

# 21. Final Deliverables

## Working Prototype

[Open the final prototype](prototype/Unrot_D1_Retention_FINAL.html)

Standalone interaction prototype representing the final product experience.

---

## Executive Product Deck

[Open the executive product deck](deck/Unrot_D1_Retention_Final.pptx)

Seven-slide executive case study covering:

1. Assignment / diagnosis
2. Product strategy
3. Prototype
4. Measurement
5. Execution
6. Recommendation

---

## PDF Version

[Open the PDF version](deck/Unrot_D1_Retention_Final.pdf)

PDF version of the final executive deck.

---

# 22. Verification Status

The project has gone through static, implementation, and packaging verification.

### Passed

- Final repository structure verified
- Final prototype artifact created
- Application JavaScript syntax checked
- Final standalone dependency check passed
- `app.js` synchronized with the extracted application runtime
- Onboarding flow verified
- Lesson flow verified
- Knowledge checks verified
- Lesson completion behavior verified
- Tomorrow mission flow verified
- Reminder selection analytics verified
- Reminder "Not now" analytics verified
- Notification routing verified
- Notification open / dismiss behavior verified
- D1 return flow verified
- D1 lesson flow verified
- Developer-only controls removed from the consumer-facing experience
- Static security / robustness review completed
- Final deck generated and verified
- Final PDF generated and verified
- Deck contains exactly 7 slides in 16:9 format

### Browser runtime limitation

A full real-browser E2E validation was **not executed** because the implementation environment did not have Chromium
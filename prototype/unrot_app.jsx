
const { useState, useEffect, useRef, useCallback } = React;

// ============================================================
// ANALYTICS SIMULATION (matches PRD Section 10)
// ============================================================
const eventLog = [];
const EVENT_TEMPLATES = {
  new_user: { color: '#007aff', label: 'new_user' },
  onboarding_completed: { color: '#34c759', label: 'onboarding_completed' },
  lesson_started: { color: '#5856d6', label: 'lesson_started' },
  first_value_achieved: { color: '#ff9500', label: 'first_value_achieved' },
  lesson_completed: { color: '#34c759', label: 'lesson_completed' },
  session_end: { color: '#ff3b30', label: 'session_end' },
  notification_sent: { color: '#5ac8fa', label: 'notification_sent' },
  notification_opened: { color: '#5ac8fa', label: 'notification_opened' },
  session_start_d1: { color: '#34c759', label: 'session_start (Day 1)' },
};

function logEvent(name, props = {}) {
  const ts = new Date().toISOString();
  const entry = { name, props: { ...props, timestamp: ts }, ts };
  eventLog.unshift(entry);
  if (eventLog.length > 50) eventLog.pop();

  // Console simulation
  const tmpl = EVENT_TEMPLATES[name];
  const color = tmpl ? tmpl.color : '#636366';
  console.log(`%c[ANALYTICS] %c${name}%c → %c${JSON.stringify(props)}`,
    `color: ${color}; font-weight: bold;`, `color: ${color};`, '', '');
}

function clearEvents() { eventLog.length = 0; }

// ============================================================
// MOCK CONTENT (realistic Unrot-style)
// ============================================================
const LESSONS = [
  {
    id: 'lesson-001',
    title: 'What are Large Language Models?',
    subtitle: 'The foundation of modern AI — and why they changed everything.',
    body: `Large Language Models (LLMs) are AI systems trained on vast amounts of text — billions of words from books, articles, websites, and code.

They don't "know" facts the way humans do. Instead, they learn patterns: which words tend to follow which other words, how arguments are structured, how code is written.

When you ask an LLM a question, it's not retrieving an answer from a database. It's generating the most likely next words, one at a time, based on everything it learned during training.

That's why they can write, summarize, explain, and code — but also why they sometimes sound confident about things that aren't true.`,
    tags: ['Foundation', '10 min'],
    level: 'Beginner',
    topic: 'AI Fundamentals',
    nextLessonId: 'lesson-002',
  },
  {
    id: 'lesson-002',
    title: 'Prompt Engineering: The Skill That Matters',
    subtitle: 'How to talk to AI so it actually gives you what you need.',
    body: `Prompt engineering isn't about finding magic words. It's about giving the model enough context to do what you want.

The best prompts usually include:
• A clear role ("You are a senior product manager…")
• The specific task ("Draft a 1-page brief on…")
• The format you want ("Use bullet points, max 300 words")
• Any constraints ("Don't use jargon, assume the reader is new to AI")

Think of it like delegating to a brilliant but literal colleague. The more precisely you communicate, the better the output.

The professionals getting the most out of AI aren't using secret prompts — they're just clearer about what they want.`,
    tags: ['Prompt Engineering', '8 min'],
    level: 'Beginner',
    topic: 'Practical AI',
    nextLessonId: 'lesson-003',
  },
  {
    id: 'lesson-003',
    title: 'AI Agents: Beyond Chat',
    subtitle: "When AI doesn't just answer — it does things for you.",
    body: `An AI agent is a system that can take actions, not just generate text.

A chat bot answers your question. An agent might:
• Read your calendar and draft a meeting summary
• Search the web, synthesize findings, and write a report
• Write and execute code to analyze a dataset
• Book a meeting by coordinating with other tools

The key difference: agency. The system has access to tools and can chain steps together without you prompting each one.

This is where AI moves from "interesting" to "useful" — when it can do work, not just talk about it.

The professionals ahead of the curve are already building simple agents for repetitive tasks. The bar for "what AI can do for me" keeps moving up.`,
    tags: ['AI Agents', '10 min'],
    level: 'Intermediate',
    topic: 'Emerging AI',
    nextLessonId: null,
  },
];

const NEWS_ITEMS = [
  {
    id: 'news-001',
    title: 'OpenAI launches GPT-5 with breakthrough reasoning',
    excerpt: 'The new model shows major improvements in multi-step reasoning and code generation, with early benchmarks suggesting a step-change in capability for complex tasks.',
    readTime: '1 min read',
  },
  {
    id: 'news-002',
    title: 'Google DeepMind unveils Gemini 2.0 with native video understanding',
    excerpt: 'The latest Gemini model can now analyze and reason about video content natively — a capability that opens new applications in education, media analysis, and accessibility.',
    readTime: '2 min read',
  },
];

// ============================================================
// ICONS (inline SVG)
// ============================================================
const Icons = {
  home: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>,
  fire: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon" style={{color:'#ff9500'}}><path d="M12 2c1 4-2 8-2 8s4-1 5 1c0 1 1 2 2 2s2-1 2-2c1-2 5-1 5-1s-2-4-2-8-5 0-5 0z"/><path d="M12 22c3 0 6-1 6-4s-3-4-6-4-6 1-6 4 3 4 6 4z"/></svg>,
  news: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon"><path d="M4 6h16M4 12h16M4 18h16M8 6v12M16 6v12"/></svg>,
  book: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon"><path d="M4 19.5A2.5 2.5 0 016.5 17H20M4 19.5V4a2.5 2.5 0 012.5-2.5h13A2.5 2.5 0 0122 4v15.5M4 19.5h13"/></svg>,
  check: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" style={{width:'24px',height:'24px'}}><path d="M20 6L9 17l-5-5"/></svg>,
  x: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'16px',height:'16px'}}><path d="M18 6L6 18M6 6l12 12"/></svg>,
  bell: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'16px',height:'16px'}}><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0"/></svg>,
  arrowRight: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'16px',height:'16px'}}><path d="M5 12h14M12 5l7 7-7 7"/></svg>,
  arrowLeft: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'16px',height:'16px'}}><path d="M19 12H5M12 19l-7-7 7-7"/></svg>,
  sparkle: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{width:'14px',height:'14px'}}><path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/></svg>,
};

const app = ReactDOM.createRoot(document.getElementById('root'));

// ============================================================
// UTILITY
// ============================================================
function useTimer(initial = 0) {
  const [t, setT] = useState(initial);
  const ref = useRef(null);
  const start = useCallback(() => { ref.current = Date.now(); setT(0); }, []);
  useEffect(() => {
    if (!ref.current) return;
    const iv = setInterval(() => setT(Math.floor((Date.now() - ref.current) / 1000)), 200);
    return () => clearInterval(iv);
  }, []);
  return [t, start];
}

// ============================================================
// SCREEN 0: ONBOARDING (C3 - optimized notification opt-in)
// ============================================================
function OnboardingScreen({ onComplete, user }) {
  const [notifGranted, setNotifGranted] = useState(null); // null=undecided, true, false
  const [duration, setDuration] = useState(0);
  const timer = useTimer();

  useEffect(() => { timer[1](); }, []);
  useEffect(() => { setDuration(timer[0]); }, [timer[0]]);

  const handleComplete = () => {
    logEvent('onboarding_completed', {
      user_id: user.id,
      onboarding_duration_ms: duration * 1000,
      granted_notification_permission: notifGranted === true,
      platform: 'iOS',
      app_version: '2.2.4',
    });
    onComplete({ notifGranted: notifGranted === true });
  };

  return (
    <div className="screen">
      <div className="status-bar"><span>9:41</span><span>📶 🔋</span></div>

      <div style={{ paddingTop: 60, paddingBottom: 40 }}>
        {/* Logo */}
        <div className="welcome-logo">Unrot</div>
        <div className="welcome-subtitle">Learn AI in 5 minutes a day</div>

        <div style={{ marginTop: 40, marginBottom: 24 }}>
          <h1 style={{ marginBottom: 12 }}>Your AI learning,<br/>made simple.</h1>
          <p>Short lessons, daily news, and interview prep — built for busy professionals who want to stay ahead of AI without spending hours on it.</p>
        </div>

        {/* Value props */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 32 }}>
          {[
            { icon: '📚', text: 'One concept a day — 5 minutes, plain English' },
            { icon: '📰', text: 'Daily AI news, curated — no noise' },
            { icon: '🎯', text: 'Interview prep with instant feedback' },
          ].map((item, i) => (
            <div key={i} className="card-ivory" style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '14px 16px' }}>
              <span style={{ fontSize: 24 }}>{item.icon}</span>
              <span style={{ fontSize: 14, color: '#98989d' }}>{item.text}</span>
            </div>
          ))}
        </div>

        {/* Optimized notification opt-in (C3) */}
        <div className="card-ivory" style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
            <div className="notification-icon" style={{ background: 'linear-gradient(135deg, #5ac8fa, #007aff)', width: 40, height: 40, borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {Icons.bell}
            </div>
            <div style={{ flex: 1 }}>
              <h3 style={{ marginBottom: 4 }}>Stay ahead, automatically</h3>
              <p style={{ fontSize: 13, color: '#98989d', marginBottom: 0 }}>Get a daily nudge with your AI lesson — so you never miss a day, even when life gets busy.</p>
            </div>
          </div>

          <div style={{ marginTop: 14, display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 6 }}>
                {notifGranted === null && 'Get daily lesson reminders?'}
                {notifGranted === true && 'Daily reminders are on ✓'}
                {notifGranted === false && 'Reminders skipped — you can enable later'}
              </div>
            </div>
            <div className={`toggle ${notifGranted === true ? 'on' : ''}`} onClick={() => setNotifGranted(notifGranted === true ? null : true)} />
          </div>

          {notifGranted === true && (
            <p className="small" style={{ marginTop: 10, color: '#34c759' }}>
              You'll get one short nudge each morning with today's concept.
            </p>
          )}
          {notifGranted === false && (
            <p className="small" style={{ marginTop: 10, color: '#8e8e93' }}>
              No problem — your streak still counts when you open the app.
            </p>
          )}
        </div>

        {/* Complete button */}
        <button className="btn btn-primary" onClick={handleComplete} disabled={notifGranted === null}>
          {notifGranted === null ? 'Continue' : 'Start Learning'}
          {Icons.arrowRight}
        </button>

        <p className="small" style={{ marginTop: 14, textAlign: 'center' }}>
          By continuing, you agree to Unrot's Terms and Privacy Policy.
        </p>
      </div>
    </div>
  );
}

// ============================================================
// SCREEN 1: HOME / LESSON (First Session)
// ============================================================
function HomeScreen({ user, lesson, onLessonComplete, isFirstSession, returnedFromNotification }) {
  const [started, setStarted] = useState(false);
  const [showComplete, setShowComplete] = useState(false);
  const [duration, setDuration] = useState(0);
  const timer = useTimer();

  useEffect(() => { if (started) timer[1](); }, [started]);
  useEffect(() => { if (started) setDuration(timer[0]); }, [timer[0]]);

  const handleStartLesson = (lessonItem) => {
    logEvent('lesson_started', {
      user_id: user.id,
      lesson_id: lessonItem.id,
      topic: lessonItem.topic,
      level: lessonItem.level,
      timestamp: new Date().toISOString(),
    });
    logEvent('first_value_achieved', {
      user_id: user.id,
      value_type: 'lesson',
      value_id: lessonItem.id,
      time_to_first_value_ms: 1500,
    });
    setStarted(true);
  };

  const handleComplete = () => {
    logEvent('lesson_completed', {
      user_id: user.id,
      lesson_id: lesson.id,
      completion_time_ms: duration * 1000,
      total_time_ms: duration * 1000,
      next_lesson_id: lesson.nextLessonId,
    });
    logEvent('session_end', {
      session_id: user.currentSession,
      duration_ms: duration * 1000,
      last_screen: 'lesson_complete',
      streak_after_session: 1,
      has_next_action_visible: true,
      notification_scheduled: user.notifGranted,
    });
    setShowComplete(true);
    setTimeout(() => onLessonComplete(), 800);
  };

  if (showComplete) {
    return null; // End-of-session screen takes over
  }

  return (
    <div className="screen">
      <div className="status-bar"><span>9:41</span><span>📶 🔋</span></div>

      {/* Greeting */}
      <div style={{ marginTop: 56, marginBottom: 20 }}>
        <h1 style={{ marginBottom: returnedFromNotification ? 4 : 12 }}>
          {returnedFromNotification ? 'Welcome back ↓' : 'Good morning, ' + (user.name || 'there') + '↑'}
        </h1>
        {returnedFromNotification && (
          <p className="small" style={{ color: '#34c759' }}>Your daily lesson is ready</p>
        )}
      </div>

      {/* Daily concept card */}
      <div className="lesson-card slide-up">
        <div className="lesson-header">
          <div>
            <div className="lesson-meta">
              <span className="chip chip-blue">{lesson.topic}</span>
              <span className="chip">{lesson.level}</span>
              <span className="chip">{lesson.tags[1]}</span>
            </div>
            <h2 style={{ marginTop: 10 }}>{lesson.title}</h2>
            <p style={{ fontSize: 14, marginTop: 6 }}>{lesson.subtitle}</p>
          </div>
        </div>

        <div className="scroll-content" style={{ marginTop: 12 }}>
          {lesson.body.split('\n\n').map((para, i) => (
            <p key={i} style={{ marginBottom: 10, lineHeight: 1.6 }}>{para}</p>
          ))}
        </div>

        <div className="lesson-progress">
          <div className="lesson-progress-bar" style={{ width: '100%' }} />
        </div>

        {!started && (
          <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => handleStartLesson(lesson)}>
            Start this lesson
            {Icons.arrowRight}
          </button>
        )}

        {started && !showComplete && (
          <button className="btn btn-success" onClick={handleComplete}>
            Mark as complete
            {Icons.check}
          </button>
        )}

        <p className="hint">{started ? 'You\'re making progress — keep going!' : 'Tap to begin your first concept'}</p>
      </div>

      {/* Continue learning */}
      {!started && (
        <div style={{ marginTop: 8 }}>
          <button className="btn btn-secondary" onClick={() => handleStartLesson(lesson)}>
            {Icons.book} Start learning
          </button>
        </div>
      )}
    </div>
  );
}

// ============================================================
// SCREEN 2: END-OF-SESSION NEXT-STEP (C2+C4) — KEY INTERVENTION
// ============================================================
function EndOfSessionScreen({ user, onDone, lesson }) {
  const [showNextLessonPreview, setShowNextLessonPreview] = useState(false);

  const handleSeeTomorrow = () => {
    setShowNextLessonPreview(true);
    logEvent('session_end', {
      session_id: user.currentSession,
      duration_ms: 180000,
      last_screen: 'end_of_session_next_step',
      streak_after_session: 1,
      has_next_action_visible: true,
      notification_scheduled: user.notifGranted,
    });
  };

  const handleDone = () => {
    logEvent('session_end', {
      session_id: user.currentSession,
      duration_ms: 180000,
      last_screen: 'end_of_session_done',
      streak_after_session: 1,
      has_next_action_visible: true,
      notification_scheduled: user.notifGranted,
    });
    onDone();
  };

  const nextLesson = LESSONS.find(l => l.id === lesson.nextLessonId);

  return (
    <div className="screen" style={{ background: 'linear-gradient(180deg, #0a0a0f 0%, #0f0a0a 100%)' }}>
      <div className="status-bar"><span>9:41</span><span>📶 🔋</span></div>

      <div style={{ paddingTop: 16, paddingBottom: 100 }}>
        {/* Completion celebration */}
        <div className="fade-in" style={{ textAlign: 'center', marginBottom: 24 }}>
          <div className="completion-check">
            {Icons.check}
          </div>
          <h2 style={{ marginBottom: 4 }}>Lesson complete!</h2>
          <p className="small" style={{ color: '#98989d' }}>You just finished your first AI concept.</p>
        </div>

        {/* What you learned */}
        <div className="card-ivory" style={{ marginBottom: 16, textAlign: 'left' }}>
          <div className="label" style={{ marginBottom: 8 }}>What you learned today</div>
          <h3 style={{ marginBottom: 4 }}>{lesson.title}</h3>
          <p className="small" style={{ color: '#98989d' }}>{lesson.topic} · {lesson.tags[1]}</p>
        </div>

        {/* THE KEY INTERVENTION: Streak + Next Step */}
        <div className="card-ivory" style={{ marginBottom: 16, background: 'linear-gradient(135deg, rgba(0,122,255,0.08), rgba(88,86,214,0.05))', border: '1px solid #25252e' }}>
          {/* Streak frame (C4) */}
          <div className="fade-in" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div className="streak-badge">
                <span className="streak-fire">🔥</span>
                <span>1 day</span>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: '#8e8e93', fontSize: 13 }}>
              {Icons.sparkle} Streak starts today
            </div>
          </div>

          <div style={{ padding: '12px 14px', background: 'rgba(255,149,0,0.08)', borderRadius: 12, border: '1px solid rgba(255,149,0,0.15)' }}>
            <p style={{ fontSize: 14, color: '#f5f5f7', marginBottom: 6, fontWeight: 500 }}>
              Don't let your streak go cold.
            </p>
            <p className="small" style={{ color: '#98989d', marginBottom: 0 }}>
              Come back tomorrow to keep it alive — just 5 minutes.
            </p>
          </div>

          {/* Next-step cue (C2) - the critical piece */}
          <div style={{ marginTop: 16, paddingTop: 16, borderTop: '1px solid #1c1c24' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              {Icons.arrowRight}
              <span className="label" style={{ color: '#007aff' }}>Tomorrow's concept is ready</span>
            </div>
            <p className="small" style={{ color: '#98989d', marginBottom: 10 }}>
              The next lesson in your path is waiting — no need to re-navigate.
            </p>

            {nextLesson && (
              <div className="card" style={{ background: '#1a1a24', border: '1px solid #25252e', cursor: 'pointer' }}
                   onClick={handleSeeTomorrow}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                  <div style={{ width: 36, height: 36, borderRadius: 10, background: 'linear-gradient(135deg, #007aff, #5856d6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16, flexShrink: 0 }}>
                    {Icons.book}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <h4 style={{ fontSize: 14, fontWeight: 600, marginBottom: 2 }}>{nextLesson.title}</h4>
                    <p className="small" style={{ color: '#98989d', marginBottom: 0 }}>{nextLesson.topic} · {nextLesson.tags[1]}</p>
                  </div>
                  <div className="tag" style={{ background: 'rgba(0,122,255,0.15)', color: '#007aff' }}>
                    {Icons.arrowRight} Tomorrow
                  </div>
                </div>
              </div>
            )}

            {user.notifGranted && (
              <div style={{ marginTop: 10, padding: '8px 12px', background: 'rgba(90,200,250,0.1)', borderRadius: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
                {Icons.bell}
                <span className="small" style={{ color: '#5ac8fa' }}>You'll also get a morning nudge with this lesson.</span>
              </div>
            )}
          </div>
        </div>

        {/* Notification status (if declined) */}
        {!user.notifGranted && (
          <div className="card" style={{ marginBottom: 16, background: 'rgba(255,149,0,0.05)', border: '1px solid rgba(255,149,0,0.1)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <div style={{ width: 32, height: 32, borderRadius: 8, background: 'rgba(255,149,0,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {Icons.bell}
              </div>
              <div>
                <p style={{ fontSize: 13, fontWeight: 500, marginBottom: 2 }}>No reminders set</p>
                <p className="small" style={{ marginBottom: 0 }}>Your streak still counts when you open the app. You can enable reminders anytime.</p>
              </div>
            </div>
          </div>
        )}

        {/* Action buttons */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 8 }}>
          <button className="btn btn-primary" onClick={handleSeeTomorrow}>
            See tomorrow's concept
            {Icons.arrowRight}
          </button>
          <button className="btn btn-secondary" onClick={handleDone}>
            Done for today
          </button>
        </div>

        <p className="small" style={{ textAlign: 'center', marginTop: 12, color: '#636366' }}>
          Your progress is saved. Come back tomorrow to keep your streak alive.
        </p>
      </div>
    </div>
  );
}

// ============================================================
// SCREEN 3: DAY 1 RETURN (after notification deep-link)
// ============================================================
function Day1ReturnScreen({ user, lesson }) {
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    logEvent('session_start_d1', {
      user_id: user.id,
      session_id: user.d1Session,
      day_number: 1,
      return_trigger: 'notification_open',
      timestamp: new Date().toISOString(),
    });
  }, []);

  const handleStart = () => {
    logEvent('lesson_started', {
      user_id: user.id,
      lesson_id: lesson.id,
      topic: lesson.topic,
      level: lesson.level,
      timestamp: new Date().toISOString(),
    });
    setShowContent(true);
  };

  return (
    <div className="screen">
      <div className="status-bar"><span>9:41</span><span>📶 🔋</span></div>

      <div style={{ marginTop: 56, marginBottom: 20, textAlign: 'center' }}>
        {/* Streak badge - continues */}
        <div className="streak-badge" style={{ marginBottom: 12, display: 'inline-flex' }}>
          <span className="streak-fire">🔥</span>
          <span>2 days</span>
        </div>
        <h1 style={{ marginBottom: 4 }}>Keep your streak alive</h1>
        <p className="small" style={{ color: '#98989d' }}>Day 2 of your AI learning journey</p>
      </div>

      {/* Today's concept */}
      <div className="lesson-card slide-up">
        <div className="lesson-header">
          <div className="chip chip-blue" style={{ marginBottom: 8 }}>Today's lesson</div>
        </div>
        <h2>{lesson.title}</h2>
        <p style={{ fontSize: 14, color: '#98989d', marginTop: 6, marginBottom: 12 }}>{lesson.subtitle}</p>

        {!showContent ? (
          <button className="btn btn-primary" onClick={handleStart}>
            Continue where you left off
            {Icons.arrowRight}
          </button>
        ) : (
          <div className="scroll-content">
            {lesson.body.split('\n\n').map((para, i) => (
              <p key={i} style={{ marginBottom: 10, lineHeight: 1.6 }}>{para}</p>
            ))}
          </div>
        )}

        <div className="lesson-progress">
          <div className="lesson-progress-bar" style={{ width: showContent ? '100%' : '0%' }} />
        </div>

        {showContent && (
          <button className="btn btn-success" style={{ marginTop: 16 }}>
            Mark as complete
            {Icons.check}
          </button>
        )}
      </div>

      {/* Encouragement */}
      <div className="card-ivory" style={{ marginTop: 16, textAlign: 'center' }}>
        <p className="small" style={{ color: '#98989d' }}>
          You're building a habit that compounds. Two days in, and you already know more than you did yesterday.
        </p>
      </div>
    </div>
  );
}

// ============================================================
// NOTIFICATION SIMULATION (C1)
// ============================================================
function NotificationSim({ visible, onTap, onDismiss }) {
  if (!visible) return null;

  return (
    <div className="notification-simulation" onClick={onTap}>
      <div className="notification-icon">
        {Icons.bell}
      </div>
      <div className="notification-body">
        <div className="notification-title">Your daily AI lesson is ready</div>
        <div className="notification-text">What are Large Language Models? — continue your streak</div>
        <div className="notification-time">Just now · Unrot</div>
      </div>
      <div className="notification-close" onClick={(e) => { e.stopPropagation(); onDismiss(); }}>
        {Icons.x}
      </div>
    </div>
  );
}

// ============================================================
// EVENT LOG TOGGLE
// ============================================================
function EventLogToggle({ logVisible, onToggle }) {
  return (
    <button className="btn btn-ghost btn-sm" onClick={onToggle} style={{ position: 'absolute', top: 12, right: 16, zIndex: 60, background: 'rgba(10,10,15,0.8)', border: '1px solid #1c1c24' }}>
      {logVisible ? ' Hide Events' : ' Show Events'}
      {Icons.bell}
    </button>
  );
}

function EventLogPanel() {
  if (eventLog.length === 0) {
    return (
      <div className="event-log visible" style={{ display: 'block' }}>
        <div style={{ color: '#636366', padding: 8, textAlign: 'center', fontFamily: 'SF Mono, monospace', fontSize: 11 }}>
          No events yet. Complete the first session to see analytics fire.
        </div>
      </div>
    );
  }

  return (
    <div className="event-log visible">
      <div style={{ color: '#8e8e93', fontSize: 11, marginBottom: 8, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
        Analytics Event Log ({eventLog.length} events)
      </div>
      {eventLog.map((entry, i) => {
        const tmpl = EVENT_TEMPLATES[entry.name];
        const color = tmpl ? tmpl.color : '#636366';
        return (
          <div key={i} className="event-entry">
            <span className="time" style={{ color: '#636366' }}>{entry.ts.slice(11, 19)}</span>
            <span style={{ color }}>{entry.name}</span>
            <div className="props">{JSON.stringify(entry.props)}</div>
          </div>
        );
      })}
    </div>
  );
}

// ============================================================
// DEEP LINK ANIMATION OVERLAY
// ============================================================
function DeepLinkOverlay({ onComplete }) {
  useEffect(() => {
    const t = setTimeout(onComplete, 1500);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="deep-link-overlay">
      <div className="deep-link-ring" />
      <div className="deep-link-dot" style={{ marginLeft: 'calc(50% - 6px)', marginTop: 'calc(50% - 6px)' }} />
      <p className="small" style={{ position: 'absolute', bottom: 40, color: '#8e8e93', textAlign: 'center', width: '80%' }}>
        Deep-linking to today's lesson...
      </p>
    </div>
  );
}

// ============================================================
// BOTTOM NAVIGATION
// ============================================================
function BottomNav({ active }) {
  const items = [
    { id: 'home', icon: Icons.home, label: 'Home' },
    { id: 'streak', icon: Icons.fire, label: 'Streak', active: true },
    { id: 'news', icon: Icons.news, label: 'News' },
    { id: 'book', icon: Icons.book, label: 'Lessons' },
  ];

  return (
    <div className="bottom-nav">
      {items.map(item => (
        <div key={item.id} className={`nav-item ${item.id === active || item.active ? 'active' : ''}`}>
          {item.icon}
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}

// ============================================================
// MAIN APP
// ============================================================
function App() {
  const [phase, setPhase] = useState('onboarding'); // onboarding | home | endOfSession | day1Notification | day1Return | deepLink
  const [user, setUser] = useState({
    id: 'user-' + Math.random().toString(36).slice(2, 8),
    name: 'Alex',
    notifGranted: null,
    currentSession: 'sess-' + Date.now(),
    d1Session: 'sess-d1-' + Date.now(),
    isFirstSession: true,
    returnedFromNotification: false,
  });
  const [lesson, setLesson] = useState(LESSONS[0]);
  const [notificationVisible, setNotificationVisible] = useState(false);
  const [eventLogVisible, setEventLogVisible] = useState(false);
  const [showEndSessionForDeclined, setShowEndSessionForDeclined] = useState(false);

  // Reset for demo
  const handleReset = () => {
    clearEvents();
    setUser({
      id: 'user-' + Math.random().toString(36).slice(2, 8),
      name: 'Alex',
      notifGranted: null,
      currentSession: 'sess-' + Date.now(),
      d1Session: 'sess-d1-' + Date.now(),
      isFirstSession: true,
      returnedFromNotification: false,
    });
    setLesson(LESSONS[0]);
    setPhase('onboarding');
    setNotificationVisible(false);
    setEventLogVisible(false);
    setShowEndSessionForDeclined(false);
    logEvent('new_user', {
      user_id: user.id,
      timestamp: new Date().toISOString(),
      source: 'organic',
      platform: 'iOS',
      app_version: '2.2.4',
      is_returning_install: false,
    });
  };

  // Handle onboarding completion
  const handleOnboardingComplete = ({ notifGranted }) => {
    setUser(prev => ({ ...prev, notifGranted }));
    setPhase('home');
  };

  // Handle lesson complete → end-of-session
  const handleLessonComplete = () => {
    if (user.notifGranted) {
      // Show end-of-session screen (C2+C4)
      setPhase('endOfSession');
    } else {
      // Show end-of-session for declined users too (control path)
      setPhase('endOfSession');
    }
  };

  // Handle end-of-session done → trigger Day 1 notification
  const handleEndSessionDone = () => {
    // Simulate Day 1 notification (C1)
    logEvent('notification_sent', {
      user_id: user.id,
      timestamp: new Date().toISOString(),
      notification_type: 'daily_lesson',
      expected_trigger_day: 1,
    });
    setPhase('day1Notification');
    setNotificationVisible(true);
  };

  // Handle notification tap
  const handleNotificationTap = () => {
    setNotificationVisible(false);
    logEvent('notification_opened', {
      user_id: user.id,
      timestamp: new Date().toISOString(),
      notification_type: 'daily_lesson',
      deep_link_target: '/lesson/' + lesson.id,
    });
    setPhase('deepLink');
  };

  // Handle notification dismiss
  const handleNotificationDismiss = () => {
    setNotificationVisible(false);
    // User dismisses — we stay in day1Notification phase but with no notification
    // For demo: show an organic return path if they tap "Return anyway"
    setTimeout(() => {
      setPhase('day1Return');
      setUser(prev => ({ ...prev, returnedFromNotification: false }));
    }, 300);
  };

  // Handle deep link complete
  const handleDeepLinkComplete = () => {
    setPhase(user.returnedFromNotification ? 'day1Return' : 'day1Notification');
    setUser(prev => ({ ...prev, returnedFromNotification: true }));
  };

  // Handle organic return (bypassing notification)
  const handleOrganicReturn = () => {
    setPhase('deepLink');
    setUser(prev => ({ ...prev, returnedFromNotification: false }));
  };

  // Render
  return (
    <div className="phone-frame">
      {/* Reset button (dev/demo only) */}
      <button className="btn btn-ghost btn-sm" onClick={handleReset} style={{ position: 'absolute', top: 12, left: 16, zIndex: 60, fontSize: 11, padding: '6px 10px', background: 'rgba(10,10,15,0.8)', border: '1px solid #1c1c24' }}>
        ↻ Reset Demo
      </button>

      <EventLogToggle logVisible={eventLogVisible} onToggle={() => setEventLogVisible(!eventLogVisible)} />
      {eventLogVisible && <EventLogPanel />}
      <NotificationSim
        visible={notificationVisible && phase === 'day1Notification'}
        onTap={handleNotificationTap}
        onDismiss={handleNotificationDismiss}
      />

      {/* ===== PHASE: ONBOARDING ===== */}
      {phase === 'onboarding' && (
        <OnboardingScreen onComplete={handleOnboardingComplete} user={user} />
      )}

      {/* ===== PHASE: HOME / FIRST LESSON ===== */}
      {phase === 'home' && (
        <>
          <BottomNav active="home" />
          <HomeScreen
            user={user}
            lesson={lesson}
            onLessonComplete={handleLessonComplete}
            isFirstSession={user.isFirstSession}
            returnedFromNotification={user.returnedFromNotification}
          />
        </>
      )}

      {/* ===== PHASE: END-OF-SESSION (C2+C4) ===== */}
      {phase === 'endOfSession' && (
        <>
          <BottomNav active="streak" />
          <EndOfSessionScreen
            user={user}
            onDone={handleEndSessionDone}
            lesson={lesson}
          />
        </>
      )}

      {/* ===== PHASE: DAY 1 NOTIFICATION (C1) ===== */}
      {phase === 'day1Notification' && (
        <>
          <BottomNav active="home" />
          {/* Background: home screen behind notification */}
          <HomeScreen
            user={user}
            lesson={lesson}
            onLessonComplete={() => {}}
            isFirstSession={false}
            returnedFromNotification={false}
          />
          {/* "Return anyway" button if notification dismissed or for organic path demo */}
          {!notificationVisible && (
            <div style={{ position: 'absolute', bottom: 90, left: 24, right: 24, textAlign: 'center', zIndex: 40 }}>
              <button className="btn btn-ghost btn-sm" onClick={handleOrganicReturn} style={{ background: 'rgba(10,10,15,0.8)' }}>
                ← Return to app another way
              </button>
              <p className="small" style={{ marginTop: 8, textAlign: 'center' }}>Or tap the notification above</p>
            </div>
          )}
        </>
      )}

      {/* ===== PHASE: DEEP LINK ANIMATION ===== */}
      {phase === 'deepLink' && (
        <DeepLinkOverlay onComplete={handleDeepLinkComplete} />
      )}

      {/* ===== PHASE: DAY 1 RETURN ===== */}
      {phase === 'day1Return' && (
        <>
          <BottomNav active="streak" />
          <Day1ReturnScreen user={user} lesson={lesson} />
        </>
      )}

      {/* ===== PHASE: DAY 1 RETURN (after notification tap) ===== */}
      {phase === 'day1Return' && user.returnedFromNotification && (
        <>
          <BottomNav active="streak" />
        </>
      )}

      {/* Demo instructions overlay */}
      <div style={{ position: 'absolute', bottom: 20, left: 16, right: 16, zIndex: 30, pointerEvents: 'none' }}>
        <p className="small" style={{ background: 'rgba(10,10,15,0.75)', padding: '4px 10px', borderRadius: 6, textAlign: 'center', pointerEvents: 'auto', display: 'block', marginBottom: 6, color: '#636366', fontSize: 10, letterSpacing: '0.3px' }}>
          Interaction prototype — not a production build. Demonstrates the D1 Pull journey and simulates analytics events. Browser runtime validation: BLOCKED / NOT EXECUTED in this environment.
        </p>
        {phase === 'onboarding' && (
          <p className="small" style={{ background: 'rgba(10,10,15,0.8)', padding: '6px 10px', borderRadius: 8, textAlign: 'center', pointerEvents: 'auto', display: 'inline-block' }}>
            👋 Try: Accept or decline notifications → Start lesson → Complete it
          </p>
        )}
        {phase === 'home' && (
          <p className="small" style={{ background: 'rgba(10,10,15,0.8)', padding: '6px 10px', borderRadius: 8, textAlign: 'center', pointerEvents: 'auto', display: 'inline-block' }}>
            👆 Start the first lesson, then complete it to see the D1 intervention
          </p>
        )}
        {phase === 'endOfSession' && (
          <p className="small" style={{ background: 'rgba(10,10,15,0.8)', padding: '6px 10px', borderRadius: 8, textAlign: 'center', pointerEvents: 'auto', display: 'inline-block' }}>
            🎯 This is the D1 intervention (C2+C4): streak frame + next-step cue + notification status
          </p>
        )}
        {phase === 'day1Notification' && (
          <p className="small" style={{ background: 'rgba(10,10,15,0.8)', padding: '6px 10px', borderRadius: 8, textAlign: 'center', pointerEvents: 'auto', display: 'inline-block' }}>
            🔔 This simulates the Day 1 notification (C1). Tap it or dismiss to test both paths.
          </p>
        )}
        {phase === 'deepLink' && (
          <p className="small" style={{ background: 'rgba(10,10,15,0.8)', padding: '6px 10px', borderRadius: 8, textAlign: 'center', pointerEvents: 'auto', display: 'inline-block' }}>
            🔗 Deep-linking to today's content...
          </p>
        )}
        {phase === 'day1Return' && (
          <p className="small" style={{ background: 'rgba(10,10,15,0.8)', padding: '6px 10px', borderRadius: 8, textAlign: 'center', pointerEvents: 'auto', display: 'inline-block' }}>
            ✅ Day 1 return! Streak continues (2 days). This is the D1 success moment.
          </p>
        )}
      </div>
    </div>
  );
}

app.render(<App />);

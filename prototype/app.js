// Precompiled React application — classic JSX runtime
const {
  useState,
  useEffect,
  useRef,
  useCallback
} = React;

// ============================================================
// ANALYTICS SIMULATION (matches PRD Section 10)
// ============================================================
const eventLog = [];
const EVENT_TEMPLATES = {
  new_user: {
    color: '#007aff',
    label: 'new_user'
  },
  onboarding_completed: {
    color: '#34c759',
    label: 'onboarding_completed'
  },
  lesson_started: {
    color: '#5856d6',
    label: 'lesson_started'
  },
  first_value_achieved: {
    color: '#ff9500',
    label: 'first_value_achieved'
  },
  lesson_completed: {
    color: '#34c759',
    label: 'lesson_completed'
  },
  session_end: {
    color: '#ff3b30',
    label: 'session_end'
  },
  notification_sent: {
    color: '#5ac8fa',
    label: 'notification_sent'
  },
  notification_opened: {
    color: '#5ac8fa',
    label: 'notification_opened'
  },
  session_start_d1: {
    color: '#34c759',
    label: 'session_start (Day 1)'
  }
};
function logEvent(name, props = {}) {
  const ts = new Date().toISOString();
  const entry = {
    name,
    props: {
      ...props,
      timestamp: ts
    },
    ts
  };
  eventLog.unshift(entry);
  if (eventLog.length > 50) eventLog.pop();

  // Console simulation
  const tmpl = EVENT_TEMPLATES[name];
  const color = tmpl ? tmpl.color : '#636366';
  console.log(`%c[ANALYTICS] %c${name}%c → %c${JSON.stringify(props)}`, `color: ${color}; font-weight: bold;`, `color: ${color};`, '', '');
}
function clearEvents() {
  eventLog.length = 0;
}

// ============================================================
// MOCK CONTENT (realistic Unrot-style)
// ============================================================
const LESSONS = [{
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
  nextLessonId: 'lesson-002'
}, {
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
  nextLessonId: 'lesson-003'
}, {
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
  nextLessonId: null
}];
const NEWS_ITEMS = [{
  id: 'news-001',
  title: 'OpenAI launches GPT-5 with breakthrough reasoning',
  excerpt: 'The new model shows major improvements in multi-step reasoning and code generation, with early benchmarks suggesting a step-change in capability for complex tasks.',
  readTime: '1 min read'
}, {
  id: 'news-002',
  title: 'Google DeepMind unveils Gemini 2.0 with native video understanding',
  excerpt: 'The latest Gemini model can now analyze and reason about video content natively — a capability that opens new applications in education, media analysis, and accessibility.',
  readTime: '2 min read'
}];

// ============================================================
// ICONS (inline SVG)
// ============================================================
const Icons = {
  home: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    className: "nav-icon"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
  })),
  fire: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    className: "nav-icon",
    style: {
      color: '#ff9500'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M12 2c1 4-2 8-2 8s4-1 5 1c0 1 1 2 2 2s2-1 2-2c1-2 5-1 5-1s-2-4-2-8-5 0-5 0z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12 22c3 0 6-1 6-4s-3-4-6-4-6 1-6 4 3 4 6 4z"
  })),
  news: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    className: "nav-icon"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 6h16M4 12h16M4 18h16M8 6v12M16 6v12"
  })),
  book: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    className: "nav-icon"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 19.5A2.5 2.5 0 016.5 17H20M4 19.5V4a2.5 2.5 0 012.5-2.5h13A2.5 2.5 0 0122 4v15.5M4 19.5h13"
  })),
  check: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "3",
    style: {
      width: '24px',
      height: '24px'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M20 6L9 17l-5-5"
  })),
  x: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    style: {
      width: '16px',
      height: '16px'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 6L6 18M6 6l12 12"
  })),
  bell: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    style: {
      width: '16px',
      height: '16px'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0"
  })),
  arrowRight: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    style: {
      width: '16px',
      height: '16px'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M5 12h14M12 5l7 7-7 7"
  })),
  arrowLeft: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    style: {
      width: '16px',
      height: '16px'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M19 12H5M12 19l-7-7 7-7"
  })),
  sparkle: /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    style: {
      width: '14px',
      height: '14px'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"
  }))
};
const app = ReactDOM.createRoot(document.getElementById('root'));

// ============================================================
// UTILITY
// ============================================================
function useTimer(initial = 0) {
  const [t, setT] = useState(initial);
  const ref = useRef(null);
  const start = useCallback(() => {
    ref.current = Date.now();
    setT(0);
  }, []);
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
function OnboardingScreen({
  onComplete,
  user
}) {
  const [notifGranted, setNotifGranted] = useState(null); // null=undecided, true, false
  const [duration, setDuration] = useState(0);
  const timer = useTimer();
  useEffect(() => {
    timer[1]();
  }, []);
  useEffect(() => {
    setDuration(timer[0]);
  }, [timer[0]]);
  const handleComplete = () => {
    logEvent('onboarding_completed', {
      user_id: user.id,
      onboarding_duration_ms: duration * 1000,
      granted_notification_permission: notifGranted === true,
      platform: 'iOS',
      app_version: '2.2.4'
    });
    onComplete({
      notifGranted: notifGranted === true
    });
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "screen"
  }, /*#__PURE__*/React.createElement("div", {
    className: "status-bar"
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("span", null, "📶 🔋")), /*#__PURE__*/React.createElement("div", {
    style: {
      paddingTop: 60,
      paddingBottom: 40
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "welcome-logo"
  }, "Unrot"), /*#__PURE__*/React.createElement("div", {
    className: "welcome-subtitle"
  }, "Learn AI in 5 minutes a day"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 32,
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      marginBottom: 12
    }
  }, "Your AI learning,", /*#__PURE__*/React.createElement("br", null), "made simple.")), /*#__PURE__*/React.createElement("p", null, "Short lessons, daily news, and interview prep — built for busy professionals who want to stay ahead of AI without spending hours on it.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 10,
      marginBottom: 28
    }
  }, [{
    num: '1',
    text: 'One concept a day — 5 minutes, plain English'
  }, {
    num: '2',
    text: 'Daily AI news, curated — no noise'
  }, {
    num: '3',
    text: 'Interview prep with instant feedback'
  }].map((item, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "card-ivory",
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: 12,
      padding: '14px 16px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      width: 22,
      height: 22,
      borderRadius: 50,
      background: 'rgba(0,122,255,0.15)',
      color: '#007aff',
      fontWeight: 700,
      fontSize: 12,
      fontFamily: 'SF Mono, Menlo, monospace',
      flexShrink: 0
    }
  }, item.num), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 14,
      color: '#f5f5f7',
      lineHeight: 1.5
    }
  }, item.text)))), /*#__PURE__*/React.createElement("div", {
    className: "card-ivory",
    style: {
      marginBottom: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "notification-icon",
    style: {
      background: 'linear-gradient(135deg, #5ac8fa, #007aff)',
      width: 40,
      height: 40,
      borderRadius: 12,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, Icons.bell), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("h3", {
    style: {
      marginBottom: 4
    }
  }, "Stay ahead, automatically"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 13,
      color: '#98989d',
      marginBottom: 0
    }
  }, "Get a daily nudge with your AI lesson — so you never miss a day, even when life gets busy."))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14,
      display: 'flex',
      alignItems: 'flex-start',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 14,
      fontWeight: 500,
      marginBottom: 6
    }
  }, notifGranted === null && 'Get daily lesson reminders?', notifGranted === true && 'Daily reminders are on ✓', notifGranted === false && 'Reminders skipped — you can enable later')), /*#__PURE__*/React.createElement("div", {
    className: `toggle ${notifGranted === true ? 'on' : ''}`,
    onClick: () => setNotifGranted(notifGranted === true ? null : true)
  })), notifGranted === true && /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      marginTop: 10,
      color: '#34c759'
    }
  }, "You'll get one short nudge each morning with today's concept."), notifGranted === false && /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      marginTop: 10,
      color: '#8e8e93'
    }
  }, "No problem — your streak still counts when you open the app.")), /*#__PURE__*/React.createElement("button", {
    className: "btn btn-primary",
    onClick: handleComplete,
    disabled: notifGranted === null
  }, notifGranted === null ? 'Continue' : 'Start Learning', Icons.arrowRight), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      marginTop: 14,
      textAlign: 'center'
    }
  }, "By continuing, you agree to Unrot's Terms and Privacy Policy."));
}

// ============================================================
// SCREEN 1: LESSON (Day 0) — with knowledge check
// ============================================================
function LessonScreen({
  user,
  lesson,
  onLessonComplete
}) {
  const [started, setStarted] = useState(false);
  const [showContent, setShowContent] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [duration, setDuration] = useState(0);
  const timer = useTimer();
  useEffect(() => {
    if (started) timer[1]();
  }, [started]);
  useEffect(() => {
    if (started) setDuration(timer[0]);
  }, [timer[0]]);

  const handleStart = () => {
    logEvent('lesson_started', {
      user_id: user.id,
      lesson_id: lesson.id,
      topic: lesson.topic,
      level: lesson.level,
      timestamp: new Date().toISOString()
    });
    setStarted(true);
    setShowContent(true);
  };

  const handleAnswer = (choiceIndex, correctIndex) => {
    if (feedback) return;
    setAnswer(choiceIndex);
    if (choiceIndex === correctIndex) {
      logEvent('knowledge_check_passed', {
        user_id: user.id,
        lesson_id: lesson.id,
        question_id: lesson.id + '-q1',
        time_to_answer_ms: duration * 1000
      });
      setFeedback({ type: 'correct' });
    } else {
      setFeedback({ type: 'incorrect' });
    }
  };

  const handleContinueAfterCheck = () => {
    logEvent('first_value_achieved', {
      user_id: user.id,
      value_type: 'lesson_with_knowledge_check',
      value_id: lesson.id,
      time_to_first_value_ms: duration * 1000
    });
    setCompleted(true);
  };

  const handleComplete = () => {
    logEvent('lesson_completed', {
      user_id: user.id,
      lesson_id: lesson.id,
      completion_time_ms: duration * 1000,
      total_time_ms: duration * 1000,
      next_lesson_id: lesson.nextLessonId
    });
    logEvent('session_end', {
      session_id: user.currentSession,
      duration_ms: duration * 1000,
      last_screen: 'mission_reveal',
      streak_after_session: 1,
      has_next_action_visible: true,
      notification_scheduled: user.notifGranted
    });
    onLessonComplete();
  };

  const QUESTION = {
    question: 'What makes an LLM different from a traditional database?',
    options: [
      'It retrieves stored records by exact match',
      'It generates the most likely next words from learned patterns'
    ],
    correctIndex: 1
  };

  if (completed) {
    return null;
  }

  return /*#__PURE__*/React.createElement("div", {
    className: "screen"
  }, /*#__PURE__*/React.createElement("div", {
    className: "status-bar"
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("span", null, "\uD83D\uDCE6 \uD83D\uDD5B")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 56,
      marginBottom: 20
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      marginBottom: !started ? 12 : 8
    }
  }, !started ? 'Good morning, ' + (user.name || 'there') : lesson.title), started && /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#34c759',
      marginBottom: 12
    }
  }, "You're making progress — keep going")), /*#__PURE__*/React.createElement("div", {
    className: "lesson-card slide-up"
  }, /*#__PURE__*/React.createElement("div", {
    className: "lesson-header"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "lesson-meta"
  }, /*#__PURE__*/React.createElement("span", {
    className: "chip chip-blue"
  }, lesson.topic), /*#__PURE__*/React.createElement("span", {
    className: "chip"
  }, lesson.level), /*#__PURE__*/React.createElement("span", {
    className: "chip"
  }, lesson.tags[1])), /*#__PURE__*/React.createElement("h2", {
    style: {
      marginTop: 10
    }
  }, lesson.title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      marginTop: 6
    }
  }, lesson.subtitle))), /*#__PURE__*/React.createElement("div", {
    className: "scroll-content",
    style: {
      marginTop: 12
    }
  }, lesson.body.split('\n\n').map((para, i) => /*#__PURE__*/React.createElement("p", {
    key: i,
    style: {
      marginBottom: 10,
      lineHeight: 1.6
    }
  }, para))), /*#__PURE__*/React.createElement("div", {
    className: "lesson-progress"
  }, /*#__PURE__*/React.createElement("div", {
    className: "lesson-progress-bar",
    style: {
      width: showContent ? '100%' : '0%'
    }
  }))), !started && /*#__PURE__*/React.createElement("button", {
    className: "btn btn-primary",
    style: {
      marginTop: 16
    },
    onClick: handleStart
  }, "Start this lesson", Icons.arrowRight), started && !feedback && /*#__PURE__*/React.createElement("div", {
    className: "kc-container",
    style: {
      marginTop: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "kc-question"
  }, QUESTION.question), /*#__PURE__*/React.createElement("div", {
    className: "kc-options"
  }, QUESTION.options.map((opt, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    className: `kc-option${answer === i ? ' selected' : ''}`,
    onClick: () => handleAnswer(i, QUESTION.correctIndex)
  }, /*#__PURE__*/React.createElement("div", {
    className: "kc-circle"
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "3"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M20 6L9 17l-5-5"
  }))), opt))), feedback && /*#__PURE__*/React.createElement("div", {
    className: "kc-feedback " + (feedback.type === 'correct' ? 'correct' : 'incorrect'),
    style: {
      marginTop: 12
    }
  }, feedback.type === 'correct' ? "That's right — LLMs generate likely next words from patterns, not retrieved records." : "Not quite. An LLM generates likely next words from patterns it learned — it doesn't retrieve stored records."), /*#__PURE__*/React.createElement("button", {
    className: "btn btn-success",
    style: {
      marginTop: 12
    },
    onClick: handleContinueAfterCheck
  }, "Continue", Icons.check)), started && feedback && /*#__PURE__*/React.createElement("button", {
    className: "btn btn-success",
    style: {
      marginTop: 16
    },
    onClick: handleComplete
  }, "Mark lesson complete", Icons.check));
}

// ============================================================
// SCREEN 2: TOMORROW'S 5-MINUTE MISSION — KEY INTERVENTION
// ============================================================
function TomorrowsMissionScreen({
  user,
  onNotify,
  lesson
}) {
  const mission = LESSONS.find(l => l.id === user.missionLessonId) || LESSONS[1];
  const reminderTimes = [
    { label: '8:00 AM', value: '08:00' },
    { label: '1:00 PM', value: '13:00' },
    { label: '7:00 PM', value: '19:00' }
  ];
  const [selectedTime, setSelectedTime] = useState(user.reminderTime || null);

  const handleSelectTime = (time) => {
    setSelectedTime(time);
  };

  const handleNotNow = () => {
    logEvent('reminder_time_selected', {
      user_id: user.id,
      time: null,
      decision: 'not_now',
      timestamp: new Date().toISOString()
    });
    onNotify();
  };

  const handleSetReminder = () => {
    if (!selectedTime) return;
    logEvent('reminder_time_selected', {
      user_id: user.id,
      time: selectedTime,
      decision: 'selected',
      timestamp: new Date().toISOString()
    });
    onNotify();
  };

  return /*#__PURE__*/React.createElement("div", {
    className: "screen",
    style: {
      background: 'linear-gradient(180deg, #0a0a0f 0%, #0f0a0a 100%)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "status-bar"
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("span", null, "\uD83D\uDCE6 \uD83D\uDD5B")), /*#__PURE__*/React.createElement("div", {
    style: {
      paddingTop: 48,
      paddingBottom: 100
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "fade-in",
    style: {
      textAlign: 'center',
      marginBottom: 28
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "completion-check"
  }, Icons.check), /*#__PURE__*/React.createElement("h2", {
    style: {
      marginBottom: 4
    }
  }, "Lesson complete!"), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d'
    }
  }, "You just finished your first AI concept.")), /*#__PURE__*/React.createElement("div", {
    className: "card-ivory",
    style: {
      marginBottom: 20,
      textAlign: 'left'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "label",
    style: {
      marginBottom: 8
    }
  }, "What you learned today"), /*#__PURE__*/React.createElement("h3", {
    style: {
      marginBottom: 4
    }
  }, lesson.title), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d',
      marginBottom: 0
    }
  }, lesson.topic, " \u00B7 ", lesson.tags[1])), /*#__PURE__*/React.createElement("div", {
    className: "mission-hero fade-in",
    style: {
      marginBottom: 24,
      padding: '24px 20px',
      background: 'linear-gradient(135deg, rgba(0,122,255,0.1), rgba(88,86,214,0.06))',
      border: '1px solid #25252e',
      borderRadius: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "streak-badge"
  }, /*#__PURE__*/React.createElement("span", {
    className: "streak-fire"
  }, "\uD83D\uDD25"), /*#__PURE__*/React.createElement("span", null, "1 day")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      color: '#8e8e93',
      fontSize: 13
    }
  }, Icons.sparkle, " Streak starts today")), /*#__PURE__*/React.createElement("div", {
    className: "mission-badge",
    style: {
      padding: '6px 12px',
      background: 'rgba(0,122,255,0.15)',
      borderRadius: 20,
      color: '#007aff',
      fontWeight: 600,
      fontSize: 13
    }
  }, "\u2605 Tomorrow's mission")), /*#__PURE__*/React.createElement("div", {
    className: "label",
    style: {
      marginBottom: 8,
      color: '#007aff'
    }
  }, "Tomorrow's 5-Minute Mission"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 22,
      marginBottom: 6
    }
  }, mission.title), /*#__PURE__*/React.createElement("div", {
    className: "mission-meta",
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      marginBottom: 12
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "chip chip-blue"
  }, mission.topic), /*#__PURE__*/React.createElement("span", {
    className: "chip"
  }, mission.tags[1]), /*#__PURE__*/React.createElement("span", {
    className: "small",
    style: {
      color: '#8e8e93'
    }
  }, "\u2022 5 min")), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: '#98989d',
      lineHeight: 1.5,
      marginBottom: 0
    }
  }, mission.subtitle)), /*#__PURE__*/React.createElement("div", {
    className: "reminder-section"
  }, /*#__PURE__*/React.createElement("div", {
    className: "label",
    style: {
      marginBottom: 10
    }
  }, "Set your reminder"), /*#__PURE__*/React.createElement("div", {
    className: "reminder-options"
  }, reminderTimes.map(rt => /*#__PURE__*/React.createElement("button", {
    key: rt.value,
    className: `reminder-option${selectedTime === rt.value ? ' selected' : ''}`,
    onClick: () => handleSelectTime(rt.value)
  }, /*#__PURE__*/React.createElement("span", {
    className: "reminder-time-label"
  }, rt.label), selectedTime === rt.value && /*#__PURE__*/React.createElement("span", {
    className: "reminder-check"
  }, "\u2713")))), /*#__PURE__*/React.createElement("button", {
    className: "btn btn-secondary",
    style: {
      marginTop: 8
    },
    onClick: handleNotNow
  }, "Not now")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 10,
      marginTop: 16,
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "btn btn-primary",
    onClick: handleSetReminder,
    disabled: !selectedTime
  }, "Set my reminder", Icons.arrowRight), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      textAlign: 'center',
      marginTop: 8,
      color: '#636366'
    }
  }, "Tomorrow, you'll write your first better prompt — and see the difference clarity makes."))));
}

// ============================================================
// SCREEN 3: DAY 1 RETURN (after notification deep-link)
// ============================================================
function Day1ReturnScreen({
  user,
  lesson,
  setPhase
}) {
  const mission = LESSONS.find(l => l.id === user.missionLessonId) || LESSONS[1];
  return /*#__PURE__*/React.createElement("div", {
    className: "screen"
  }, /*#__PURE__*/React.createElement("div", {
    className: "status-bar"
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("span", null, "\uD83D\uDCE6 \uD83D\uDD5B")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 56,
      marginBottom: 20,
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "streak-badge",
    style: {
      marginBottom: 12,
      display: 'inline-flex'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "streak-fire"
  }, "\uD83D\uDD25"), /*#__PURE__*/React.createElement("span", null, "2 days")), /*#__PURE__*/React.createElement("h1", {
    style: {
      marginBottom: 4
    }
  }, "Welcome back."), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d',
      marginBottom: 16
    }
  }, "Your 5-minute mission is ready."), /*#__PURE__*/React.createElement("div", {
    className: "lesson-card slide-up"
  }, /*#__PURE__*/React.createElement("div", {
    className: "lesson-header"
  }, /*#__PURE__*/React.createElement("div", {
    className: "chip chip-blue",
    style: {
      marginBottom: 8
    }
  }, "Today's mission")), /*#__PURE__*/React.createElement("h2", null, mission.title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: '#98989d',
      marginTop: 6,
      marginBottom: 12
    }
  }, mission.subtitle), /*#__PURE__*/React.createElement("button", {
    className: "btn btn-primary",
    onClick: () => setPhase('d1Lesson')
  }, "Start mission", Icons.arrowRight)), /*#__PURE__*/React.createElement("div", {
    className: "card-ivory",
    style: {
      marginTop: 16,
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d'
    }
  }, "You're building a habit that compounds. Two days in, and you already know more than you did yesterday."))));
}

// ============================================================
// SCREEN 4: DAY 1 LESSON — Prompt Engineering + knowledge check
// ============================================================
function Day1LessonScreen({
  user,
  lesson,
  setPhase
}) {
  const [started, setStarted] = useState(false);
  const [showContent, setShowContent] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [duration, setDuration] = useState(0);
  const timer = useTimer();
  useEffect(() => {
    if (started) timer[1]();
  }, [started]);
  useEffect(() => {
    if (started) setDuration(timer[0]);
  }, [timer[0]]);
  const mission = LESSONS.find(l => l.id === user.missionLessonId) || LESSONS[1];

  const handleStart = () => {
    logEvent('session_start_d1', {
      user_id: user.id,
      session_id: user.d1Session,
      day_number: 1,
      return_trigger: user.returnedFromNotification ? 'notification_open' : 'organic',
      timestamp: new Date().toISOString()
    });
    logEvent('lesson_started', {
      user_id: user.id,
      lesson_id: mission.id,
      topic: mission.topic,
      level: mission.level,
      timestamp: new Date().toISOString()
    });
    setStarted(true);
    setShowContent(true);
  };

  const handleAnswer = (choiceIndex, correctIndex) => {
    if (feedback) return;
    setAnswer(choiceIndex);
    if (choiceIndex === correctIndex) {
      logEvent('knowledge_check_passed', {
        user_id: user.id,
        lesson_id: mission.id,
        question_id: mission.id + '-q1',
        time_to_answer_ms: duration * 1000
      });
      setFeedback({ type: 'correct' });
    } else {
      setFeedback({ type: 'incorrect' });
    }
  };

  const handleContinueAfterCheck = () => {
    logEvent('first_value_achieved', {
      user_id: user.id,
      value_type: 'lesson_with_knowledge_check',
      value_id: mission.id,
      time_to_first_value_ms: duration * 1000
    });
    setCompleted(true);
  };

  const handleComplete = () => {
    logEvent('lesson_completed', {
      user_id: user.id,
      lesson_id: mission.id,
      completion_time_ms: duration * 1000,
      total_time_ms: duration * 1000,
      next_lesson_id: mission.nextLessonId
    });
    logEvent('session_end', {
      session_id: user.d1Session,
      duration_ms: duration * 1000,
      last_screen: 'd1_complete',
      streak_after_session: 2,
      has_next_action_visible: true,
      notification_scheduled: user.notifGranted
    });
    setPhase('d1Complete');
  };

  const QUESTION = {
    question: 'What makes a good prompt different from a vague request?',
    options: [
      'A good prompt gives clear context, a specific task, and format constraints',
      'A good prompt uses the most complex words possible'
    ],
    correctIndex: 0
  };

  if (completed) {
    return null;
  }

  return /*#__PURE__*/React.createElement("div", {
    className: "screen"
  }, /*#__PURE__*/React.createElement("div", {
    className: "status-bar"
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("span", null, "\uD83D\uDCE6 \uD83D\uDD5B")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 56,
      marginBottom: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "streak-badge",
    style: {
      marginBottom: 12,
      display: 'inline-flex'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "streak-fire"
  }, "\uD83D\uDD25"), /*#__PURE__*/React.createElement("span", null, "2 days")), /*#__PURE__*/React.createElement("h1", {
    style: {
      marginBottom: !started ? 8 : 4
    }
  }, !started ? "Today's mission" : mission.title), started && /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#34c759',
      marginBottom: 12
    }
  }, "You're building your streak — keep going")), /*#__PURE__*/React.createElement("div", {
    className: "lesson-card slide-up"
  }, /*#__PURE__*/React.createElement("div", {
    className: "lesson-header"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "lesson-meta"
  }, /*#__PURE__*/React.createElement("span", {
    className: "chip chip-blue"
  }, mission.topic), /*#__PURE__*/React.createElement("span", {
    className: "chip"
  }, mission.level), /*#__PURE__*/React.createElement("span", {
    className: "chip"
  }, mission.tags[1])), /*#__PURE__*/React.createElement("h2", {
    style: {
      marginTop: 10
    }
  }, mission.title), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      marginTop: 6
    }
  }, mission.subtitle))), /*#__PURE__*/React.createElement("div", {
    className: "scroll-content",
    style: {
      marginTop: 12
    }
  }, mission.body.split('\n\n').map((para, i) => /*#__PURE__*/React.createElement("p", {
    key: i,
    style: {
      marginBottom: 10,
      lineHeight: 1.6
    }
  }, para))), /*#__PURE__*/React.createElement("div", {
    className: "lesson-progress"
  }, /*#__PURE__*/React.createElement("div", {
    className: "lesson-progress-bar",
    style: {
      width: showContent ? '100%' : '0%'
    }
  }))), !started && /*#__PURE__*/React.createElement("button", {
    className: "btn btn-primary",
    style: {
      marginTop: 16
    },
    onClick: handleStart
  }, "Start mission", Icons.arrowRight), started && !feedback && /*#__PURE__*/React.createElement("div", {
    className: "kc-container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "kc-question"
  }, QUESTION.question), /*#__PURE__*/React.createElement("div", {
    className: "kc-options"
  }, QUESTION.options.map((opt, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    className: `kc-option${answer === i ? ' selected' : ''}`,
    onClick: () => handleAnswer(i, QUESTION.correctIndex)
  }, /*#__PURE__*/React.createElement("div", {
    className: "kc-circle"
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "3"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M20 6L9 17l-5-5"
  }))), opt))), feedback && /*#__PURE__*/React.createElement("div", {
    className: "kc-feedback " + (feedback.type === 'correct' ? 'correct' : 'incorrect')
  }, feedback.type === 'correct' ? "That's right — clear context, a specific task, and format constraints turn a vague ask into a useful result." : "Not quite. The best prompts are specific: set a role, describe the task, state the format, and note any constraints."), /*#__PURE__*/React.createElement("button", {
    className: "btn btn-success",
    style: {
      marginTop: 12
    },
    onClick: handleContinueAfterCheck
  }, "Continue", Icons.check)), started && feedback && /*#__PURE__*/React.createElement("button", {
    className: "btn btn-success",
    style: {
      marginTop: 16
    },
    onClick: handleComplete
  }, "Mark mission complete", Icons.check));
}

// ============================================================
// SCREEN 5: DAY 1 COMPLETE — payoff + next mission
// ============================================================
function D1CompleteScreen({
  user,
  lesson
}) {
  const mission = LESSONS.find(l => l.id === user.missionLessonId) || LESSONS[1];
  const nextLesson = LESSONS.find(l => l.id === mission.nextLessonId);

  return /*#__PURE__*/React.createElement("div", {
    className: "screen"
  }, /*#__PURE__*/React.createElement("div", {
    className: "status-bar"
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("span", null, "\uD83D\uDCE6 \uD83D\uDD5B")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 56,
      marginBottom: 20,
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "completion-check"
  }, Icons.check), /*#__PURE__*/React.createElement("div", {
    className: "streak-badge",
    style: {
      marginBottom: 12,
      display: 'inline-flex'
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "streak-fire"
  }, "\uD83D\uDD25"), /*#__PURE__*/React.createElement("span", null, "2 days")), /*#__PURE__*/React.createElement("h1", {
    style: {
      marginBottom: 4
    }
  }, "Mission complete."), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d',
      marginBottom: 16
    }
  }, "You kept your streak alive — Day 2 done."), /*#__PURE__*/React.createElement("div", {
    className: "card-ivory",
    style: {
      marginBottom: 16,
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      color: '#f5f5f7',
      marginBottom: 6
    }
  }, "You're building a habit that compounds."), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d',
      marginBottom: 0
    }
  }, "Two days in, and you already know more than you did yesterday."), nextLesson && /*#__PURE__*/React.createElement("div", {
    className: "mission-hero fade-in",
    style: {
      marginTop: 16,
      padding: '20px 16px',
      background: 'linear-gradient(135deg, rgba(0,122,255,0.1), rgba(88,86,214,0.06))',
      border: '1px solid #25252e',
      borderRadius: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "label",
    style: {
      marginBottom: 8,
      color: '#007aff'
    }
  }, "Coming up next"), /*#__PURE__*/React.createElement("h3", {
    style: {
      marginBottom: 4
    }
  }, nextLesson.title), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      color: '#98989d',
      marginBottom: 0
    }
  }, nextLesson.topic, " \u00B7 ", nextLesson.tags[1])), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      textAlign: 'center',
      marginTop: 12,
      color: '#636366'
    }
  }, "Your progress is saved. Keep going tomorrow."))));
}

// ============================================================
function NotificationSim({
  visible,
  onTap,
  onDismiss
}) {
  if (!visible) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "notification-simulation",
    onClick: onTap
  }, /*#__PURE__*/React.createElement("div", {
    className: "notification-icon"
  }, Icons.bell), /*#__PURE__*/React.createElement("div", {
    className: "notification-body"
  }, /*#__PURE__*/React.createElement("div", {
    className: "notification-title"
  }, "Your daily AI lesson is ready"), /*#__PURE__*/React.createElement("div", {
    className: "notification-text"
  }, "What are Large Language Models? — continue your streak"), /*#__PURE__*/React.createElement("div", {
    className: "notification-time"
  }, "Just now · Unrot")), /*#__PURE__*/React.createElement("div", {
    className: "notification-close",
    onClick: e => {
      e.stopPropagation();
      onDismiss();
    }
  }, Icons.x));
}

// ============================================================
// EVENT LOG TOGGLE
// ============================================================
function EventLogToggle({
  logVisible,
  onToggle
}) {
  return /*#__PURE__*/React.createElement("button", {
    className: "btn btn-ghost btn-sm",
    onClick: onToggle,
    style: {
      position: 'absolute',
      top: 12,
      right: 16,
      zIndex: 60,
      background: 'rgba(10,10,15,0.8)',
      border: '1px solid #1c1c24'
    }
  }, logVisible ? ' Hide Events' : ' Show Events', Icons.bell);
}
function EventLogPanel() {
  if (eventLog.length === 0) {
    return /*#__PURE__*/React.createElement("div", {
      className: "event-log visible",
      style: {
        display: 'block'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        color: '#636366',
        padding: 8,
        textAlign: 'center',
        fontFamily: 'SF Mono, monospace',
        fontSize: 11
      }
    }, "No events yet. Complete the first session to see analytics fire."));
  }
  return /*#__PURE__*/React.createElement("div", {
    className: "event-log visible"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      color: '#8e8e93',
      fontSize: 11,
      marginBottom: 8,
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '0.5px'
    }
  }, "Analytics Event Log (", eventLog.length, " events)"), eventLog.map((entry, i) => {
    const tmpl = EVENT_TEMPLATES[entry.name];
    const color = tmpl ? tmpl.color : '#636366';
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "event-entry"
    }, /*#__PURE__*/React.createElement("span", {
      className: "time",
      style: {
        color: '#636366'
      }
    }, entry.ts.slice(11, 19)), /*#__PURE__*/React.createElement("span", {
      style: {
        color
      }
    }, entry.name), /*#__PURE__*/React.createElement("div", {
      className: "props"
    }, JSON.stringify(entry.props)));
  }));
}

// ============================================================
// DEEP LINK ANIMATION OVERLAY
// ============================================================
function DeepLinkOverlay({
  onComplete
}) {
  useEffect(() => {
    const t = setTimeout(onComplete, 1500);
    return () => clearTimeout(t);
  }, []);
  return /*#__PURE__*/React.createElement("div", {
    className: "deep-link-overlay"
  }, /*#__PURE__*/React.createElement("div", {
    className: "deep-link-ring"
  }), /*#__PURE__*/React.createElement("div", {
    className: "deep-link-dot",
    style: {
      marginLeft: 'calc(50% - 6px)',
      marginTop: 'calc(50% - 6px)'
    }
  }), /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      position: 'absolute',
      bottom: 40,
      color: '#8e8e93',
      textAlign: 'center',
      width: '80%'
    }
  }, "Deep-linking to today's lesson..."));
}

// ============================================================
// BOTTOM NAVIGATION
// ============================================================
function BottomNav({
  active
}) {
  const items = [{
    id: 'home',
    icon: Icons.home,
    label: 'Home'
  }, {
    id: 'streak',
    icon: Icons.fire,
    label: 'Streak'
  }, {
    id: 'news',
    icon: Icons.news,
    label: 'News'
  }, {
    id: 'book',
    icon: Icons.book,
    label: 'Lessons'
  }];
  return /*#__PURE__*/React.createElement("div", {
    className: "bottom-nav"
  }, items.map(item => /*#__PURE__*/React.createElement("div", {
    key: item.id,
    className: `nav-item ${item.id === active || item.active ? 'active' : ''}`
  }, item.icon, /*#__PURE__*/React.createElement("span", null, item.label))));
}

// ============================================================
// MAIN APP
// ============================================================
function App() {
  const [phase, setPhase] = useState('onboarding'); // onboarding | lesson | mission | notification | deepLink | d1Return | d1Lesson
  const [user, setUser] = useState({
    id: 'user-' + Math.random().toString(36).slice(2, 8),
    name: 'Alex',
    notifGranted: null,
    currentSession: 'sess-' + Date.now(),
    d1Session: 'sess-d1-' + Date.now(),
    isFirstSession: true,
    returnedFromNotification: false,
    reminderTime: null,
    missionLessonId: null
  });
  const [lesson, setLesson] = useState(LESSONS[0]);
  const [notificationVisible, setNotificationVisible] = useState(false);
  const [devMode, setDevMode] = useState(false);
  const [eventLogVisible, setEventLogVisible] = useState(false);

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
      reminderTime: null,
      missionLessonId: null
    });
    setLesson(LESSONS[0]);
    setPhase('onboarding');
    setNotificationVisible(false);
    setEventLogVisible(false);
    logEvent('new_user', {
      user_id: user.id,
      timestamp: new Date().toISOString(),
      source: 'organic',
      platform: 'iOS',
      app_version: '2.2.4',
      is_returning_install: false
    });
  };

  // Handle onboarding completion
  const handleOnboardingComplete = ({
    notifGranted
  }) => {
    setUser(prev => ({
      ...prev,
      notifGranted
    }));
    setPhase('lesson');
  };

  // Handle lesson complete → mission reveal (single session_end fires inside LessonScreen)
  const handleLessonComplete = () => {
    setPhase('mission');
  };

  // Handle end-of-session done → trigger Day 1 notification
  const handleEndSessionDone = () => {
    logEvent('notification_sent', {
      user_id: user.id,
      timestamp: new Date().toISOString(),
      notification_type: 'daily_lesson',
      expected_trigger_day: 1,
      deep_link_target: '/lesson/' + (user.missionLessonId || lesson.id)
    });
    setPhase('day1Notification');
    setNotificationVisible(true);
  };

  // Handle notification tap — opens the notification and deep-links to the day-1 mission
  const handleNotificationTap = () => {
    setNotificationVisible(false);
    logEvent('notification_opened', {
      user_id: user.id,
      timestamp: new Date().toISOString(),
      notification_type: 'daily_lesson',
      deep_link_target: '/lesson/' + (user.missionLessonId || lesson.id)
    });
    setUser(prev => ({ ...prev, returnedFromNotification: true }));
    setPhase('deepLink');
  };

  // Handle notification dismiss — notification is ignored; user returns to the mission screen to continue
  const handleNotificationDismiss = () => {
    setNotificationVisible(false);
    setUser(prev => ({ ...prev, returnedFromNotification: false }));
    setPhase('mission');
  };

  // Handle deep link animation complete — arrive at the day-1 return screen
  const handleDeepLinkComplete = () => {
    setPhase('d1Return');
  };

  // Handle organic return (from the notification phase) — user opens the app directly
  const handleOrganicReturn = () => {
    setPhase('deepLink');
  };

  // Render
  return /*#__PURE__*/React.createElement("div", {
    className: "phone-frame"
  }, devMode && /*#__PURE__*/React.createElement("button", {
    className: "btn btn-ghost btn-sm",
    onClick: handleReset,
    style: {
      position: 'absolute',
      top: 12,
      left: 16,
      zIndex: 60,
      fontSize: 11,
      padding: '6px 10px',
      background: 'rgba(10,10,15,0.8)',
      border: '1px solid #1c1c24'
    }
  }, "\u21bb Reset Demo"), devMode && /*#__PURE__*/React.createElement(EventLogToggle, {
    logVisible: eventLogVisible,
    onToggle: () => setEventLogVisible(!eventLogVisible)
  }), devMode && eventLogVisible && /*#__PURE__*/React.createElement(EventLogPanel, null), /*#__PURE__*/React.createElement(NotificationSim, {
    visible: notificationVisible && phase === 'notification',
    onTap: handleNotificationTap,
    onDismiss: handleNotificationDismiss
  }), phase === 'onboarding' && /*#__PURE__*/React.createElement(OnboardingScreen, {
    onComplete: handleOnboardingComplete,
    user: user
  }), phase === 'lesson' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(BottomNav, {
   active: "home"
 }), /*#__PURE__*/React.createElement(LessonScreen, {
   user: user,
   lesson: lesson,
   onLessonComplete: handleLessonComplete
 })), phase === 'mission' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(BottomNav, {
   active: "streak"
 }), /*#__PURE__*/React.createElement(TomorrowsMissionScreen, {
   user: user,
   onNotify: handleEndSessionDone,
   lesson: lesson
 })), phase === 'notification' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(BottomNav, {
   active: "home"
 }), /*#__PURE__*/React.createElement(LessonScreen, {
   user: user,
   lesson: lesson,
   onLessonComplete: () => {}
 }), !notificationVisible && /*#__PURE__*/React.createElement("div", {
   style: {
     position: 'absolute',
     bottom: 90,
     left: 24,
     right: 24,
     textAlign: 'center',
     zIndex: 40
   }
 }, /*#__PURE__*/React.createElement("button", {
   className: "btn btn-ghost btn-sm",
   onClick: handleOrganicReturn,
   style: {
     background: 'rgba(10,10,15,0.8)'
   }
 }, "Return to the app"), /*#__PURE__*/React.createElement("p", {
   className: "small",
   style: {
     marginTop: 8,
     textAlign: 'center'
   }
 }, "Or open the notification above"))), phase === 'deepLink' && /*#__PURE__*/React.createElement(DeepLinkOverlay, {
   onComplete: handleDeepLinkComplete
 }), phase === 'd1Return' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(BottomNav, {
   active: "streak"
 }), /*#__PURE__*/React.createElement(Day1ReturnScreen, {
   user: user,
   lesson: lesson,
   setPhase: setPhase
 })), phase === 'd1Lesson' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(BottomNav, {
   active: "home"
 }), /*#__PURE__*/React.createElement(Day1LessonScreen, {
   user: user,
   lesson: lesson,
   setPhase: setPhase
 })), phase === 'd1Complete' && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(BottomNav, {
   active: "streak"
 }), /*#__PURE__*/React.createElement(D1CompleteScreen, {
   user: user,
   lesson: lesson
 })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      bottom: 20,
      left: 16,
      right: 16,
      zIndex: 30,
      pointerEvents: 'none'
    }
  }, /*#__PURE__*/React.createElement("p", {
    className: "small",
    style: {
      background: 'rgba(10,10,15,0.75)',
      padding: '4px 10px',
      borderRadius: 6,
      textAlign: 'center',
      pointerEvents: 'auto',
      display: 'block',
      marginBottom: 6,
      color: '#636366',
      fontSize: 10,
      letterSpacing: '0.3px'
    }
  }, "Unrot — AI learning, made simple.")));
}
app.render(/*#__PURE__*/React.createElement(App, null));

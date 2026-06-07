import streamlit as st
import requests
import time
import random

# ── Config ────────────────────────────────────────────────────────────────────

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="National Birthday Aptitude Test",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0f !important;
    color: #e0e0e0 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 800px;
}

/* ── HERO TITLE ── */
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    text-align: center;
    color: #ff6b35;
    text-shadow: 0 0 30px rgba(255,107,53,0.5);
    letter-spacing: 2px;
    margin: 1rem 0;
    animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { text-shadow: 0 0 20px rgba(255,107,53,0.4); }
    50% { text-shadow: 0 0 40px rgba(255,107,53,0.9), 0 0 60px rgba(255,107,53,0.3); }
}

/* ── TERMINAL BOX ── */
.terminal-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-left: 4px solid #ff6b35;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    line-height: 1.8;
    color: #58a6ff;
}

.terminal-box .prompt { color: #ff6b35; }
.terminal-box .ok     { color: #3fb950; }
.terminal-box .warn   { color: #d29922; }
.terminal-box .dim    { color: #8b949e; }

/* ── MISSION CARD ── */
.mission-card {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid #21262d;
    border-top: 3px solid #ff6b35;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
}

.mission-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ff6b35;
    letter-spacing: 3px;
    margin-bottom: 1rem;
    text-align: center;
}

.question-text {
    font-size: 1.1rem;
    line-height: 1.9;
    color: #c9d1d9;
    background: #161b22;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    border-left: 3px solid #58a6ff;
    margin: 1rem 0;
    white-space: pre-line;
}

/* ── OPTION BUTTONS ── */
.stRadio > label {
    font-family: 'Share Tech Mono', monospace !important;
    color: #c9d1d9 !important;
}

/* ── FEEDBACK BOXES ── */
.feedback-correct {
    background: #0d2218;
    border: 1px solid #3fb950;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    color: #3fb950;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1rem;
    margin: 1rem 0;
    animation: slide-in 0.4s ease;
}

.feedback-wrong {
    background: #2d1416;
    border: 1px solid #f85149;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    color: #f85149;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1rem;
    margin: 1rem 0;
    animation: shake 0.4s ease;
}

@keyframes slide-in {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%       { transform: translateX(-8px); }
    40%       { transform: translateX(8px); }
    60%       { transform: translateX(-5px); }
    80%       { transform: translateX(5px); }
}

/* ── ACHIEVEMENT BADGE ── */
.achievement-badge {
    display: inline-block;
    background: linear-gradient(135deg, #b8860b, #ffd700, #b8860b);
    color: #000;
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.5rem 1.2rem;
    border-radius: 20px;
    margin: 0.5rem 0;
    letter-spacing: 1px;
    animation: badge-pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes badge-pop {
    0%   { transform: scale(0); opacity: 0; }
    80%  { transform: scale(1.1); }
    100% { transform: scale(1); opacity: 1; }
}

/* ── PROGRESS BAR OVERRIDE ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #ff6b35, #ffd700) !important;
}

/* ── SIDEBAR ACHIEVEMENTS ── */
.sidebar-achievement {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    margin: 0.3rem 0;
    font-size: 0.85rem;
    color: #ffd700;
}

/* ── STATS ROW ── */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #21262d;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
}
.stat-row .label { color: #8b949e; }
.stat-row .value { color: #3fb950; font-weight: bold; }
.stat-row .value.pass { color: #3fb950; }
.stat-row .value.special { color: #ffd700; }

/* ── FINAL TITLE ── */
.final-title {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 900;
    text-align: center;
    color: #ffd700;
    text-shadow: 0 0 30px rgba(255,215,0,0.6);
    letter-spacing: 4px;
    margin: 1.5rem 0;
}

/* ── GIFT PROGRESS ── */
.gift-progress-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.9rem;
    color: #8b949e;
    text-align: center;
    margin: 0.3rem 0;
}

/* ── POSTER ── */
.poster-frame {
    background: linear-gradient(135deg, #1a0a2e 0%, #0a1628 50%, #0a1a0a 100%);
    border: 3px solid #ffd700;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin: 1rem 0;
}

.poster-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    color: #ffd700;
    text-shadow: 0 0 20px rgba(255,215,0,0.7);
    letter-spacing: 4px;
    margin: 1rem 0;
}

/* ── GALLERY ── */
.gallery-caption {
    font-size: 0.85rem;
    color: #8b949e;
    text-align: center;
    font-style: italic;
    margin-top: 0.3rem;
}

/* ── PRIMARY BUTTON OVERRIDE ── */
.stButton > button {
    background: linear-gradient(135deg, #ff6b35, #e05520) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    padding: 0.7rem 2rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255,107,53,0.4) !important;
}

/* ── DIVIDER ── */
hr { border-color: #21262d !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────

def init_session():
    defaults = {
        "page": "home",
        "completed": [],
        "achievements": [],
        "score": 0,
        "hint_index": {"physics": 0, "maths": 0, "ml": 0},
        "wrong_attempts": {"physics": 0, "maths": 0, "ml": 0},
        "gift_attempt": 0,
        "ai_verified": False,
        "rickrolled": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ── API helpers ───────────────────────────────────────────────────────────────

def api_get(path: str):
    try:
        r = requests.get(f"{API_BASE}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None

def api_post(path: str, data: dict):
    try:
        r = requests.post(f"{API_BASE}{path}", json=data, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None

# ── Sidebar ───────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("### 📋 Exam Progress")
        missions = ["physics", "maths", "ml", "ai_verification"]
        labels   = ["Physics", "Mathematics", "Machine Learning", "AI Verification"]
        for m, l in zip(missions, labels):
            done = m in st.session_state["completed"]
            icon = "✅" if done else "⬜"
            st.markdown(f"{icon} {l}")

        done_count = len([m for m in missions if m in st.session_state["completed"]])
        st.progress(done_count / len(missions))
        st.markdown(f"**Score:** {st.session_state['score']} pts")

        if st.session_state["achievements"]:
            st.markdown("---")
            st.markdown("### 🏆 Achievements")
            for ach in st.session_state["achievements"]:
                st.markdown(
                    f'<div class="sidebar-achievement">🏆 {ach}</div>',
                    unsafe_allow_html=True,
                )

# ── Confetti helper ───────────────────────────────────────────────────────────

def confetti():
    st.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    (function(){
        var d = document.createElement('script');
        d.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js';
        d.onload = function(){
            confetti({ particleCount: 200, spread: 160, origin: { y: 0.4 } });
        };
        document.head.appendChild(d);
    })();
    </script>
    """, unsafe_allow_html=True)

# ── Pages ─────────────────────────────────────────────────────────────────────

def page_home():
    st.markdown('<div class="hero-title">⚠️ NATIONAL BIRTHDAY APTITUDE TEST ⚠️</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="terminal-box">
        <span class="prompt">$ </span><span class="dim">system_boot --candidate-detection</span><br><br>
        <span class="ok">[OK]</span> Candidate detected.<br>
        <span class="warn">[PENDING]</span> Age verification pending.<br>
        <span class="ok">[OK]</span> Identity confirmed.<br><br>
        <span class="dim">───────────────────────────────</span><br>
        <span class="prompt">TODAY'S MISSION:</span><br>
        &nbsp;&nbsp;▸ Complete three aptitude tests.<br>
        &nbsp;&nbsp;▸ Pass AI verification.<br>
        &nbsp;&nbsp;▸ Claim your birthday gift.<br><br>
        <span class="ok">Failure is acceptable.</span><br>
        <span class="warn">Disappointment is not.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚀 BEGIN EXAM"):
        st.session_state["page"] = "physics"
        st.rerun()


def page_mission(level: str):
    data = api_get(f"/question/{level}")
    if not data:
        st.error("Could not load mission. Is the backend running?")
        return

    already_done = level in st.session_state["completed"]
    level_label  = {"physics": "maths", "maths": "ml", "ml": "ai_verification"}
    next_page    = {"physics": "maths", "maths": "ml", "ml": "ai_verification"}

    st.markdown(f'<div class="mission-title">{data["mission"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="terminal-box">
        <span class="dim">{data["preamble"]}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="question-text">{data["question"]}</div>', unsafe_allow_html=True)

    options = data["options"]
    option_labels = [f"{k}) {v}" for k, v in options.items()]
    choice = st.radio("Select your answer:", option_labels, key=f"radio_{level}")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("✅ SUBMIT ANSWER", key=f"submit_{level}"):
            selected_key = choice.split(")")[0].strip()
            result = api_post("/submit", {"level": level, "answer": selected_key})
            if result:
                if result["correct"]:
                    st.markdown(
                        f'<div class="feedback-correct">✅ {result["message"]}</div>',
                        unsafe_allow_html=True,
                    )
                    if result["achievement"] and result["achievement"] not in st.session_state["achievements"]:
                        st.session_state["achievements"].append(result["achievement"])
                        st.session_state["score"] += result["score_delta"]
                        st.markdown(
                            f'<div class="achievement-badge">🏆 ACHIEVEMENT UNLOCKED: {result["achievement"]}</div>',
                            unsafe_allow_html=True,
                        )
                    if level not in st.session_state["completed"]:
                        st.session_state["completed"].append(level)
                    time.sleep(1.5)
                    st.session_state["page"] = next_page[level]
                    st.rerun()
                else:
                    st.session_state["wrong_attempts"][level] += 1
                    st.markdown(
                        f'<div class="feedback-wrong">❌ {result["message"]}</div>',
                        unsafe_allow_html=True,
                    )

    with col2:
        hint_idx = st.session_state["hint_index"][level]
        if st.button("💡 HINT", key=f"hint_{level}"):
            if hint_idx < len(data["hints"]):
                st.info(f"💡 Hint {hint_idx + 1}: {data['hints'][hint_idx]}")
                st.session_state["hint_index"][level] += 1
            else:
                st.warning("No more hints! You're on your own.")

    if already_done:
        st.success("Mission already completed!")
        if st.button("➡️ CONTINUE"):
            st.session_state["page"] = next_page[level]
            st.rerun()

    attempts = st.session_state["wrong_attempts"].get(level, 0)
    if attempts > 0:
        st.markdown(
            f'<div class="gift-progress-label">Wrong attempts: {attempts} | '
            f'Disappointment level: {"📈 " * min(attempts, 5)}</div>',
            unsafe_allow_html=True,
        )


def page_ai_verification():
    st.markdown('<div class="mission-title">MISSION 4 : AI VERIFICATION</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="terminal-box">
        <span class="ok">[PASSED]</span> Physics ✓<br>
        <span class="ok">[PASSED]</span> Mathematics ✓<br>
        <span class="ok">[PASSED]</span> Machine Learning ✓<br><br>
        <span class="warn">[PENDING]</span> One final verification remains.<br><br>
        <span class="prompt">CRITICAL QUESTION:</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Who do you love the most?")

    love_choice = st.radio(
        "Select one:",
        ["A) Family", "B) Friends", "C) Food", "D) Modiji"],
        key="love_choice",
    )

    if st.button("🤖 SUBMIT FOR AI ANALYSIS"):
        st.markdown("""
        <div class="terminal-box">
            <span class="warn">⚠️ Are you absolutely sure?</span><br>
            <span class="dim">Initiating deep AI analysis...</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.5)

        steps = [
            ("📡 Collecting data...", 0.3, "Scanning browser history, memes, WhatsApp forwards..."),
            ("🧠 Training model...", 0.5, "Fitting 47 layers of neural network..."),
            ("📉 Running gradient descent...", 0.3, "Loss converging on truth..."),
            ("🔮 Predicting...", 0.4, "Applying sigmoid activation..."),
        ]

        bar = st.progress(0)
        status = st.empty()
        detail = st.empty()

        for i, (label, delay, desc) in enumerate(steps):
            status.markdown(f"**{label}**")
            detail.markdown(f"<small style='color:#8b949e'>{desc}</small>", unsafe_allow_html=True)
            bar.progress((i + 1) / len(steps))
            time.sleep(delay)

        time.sleep(0.3)
        bar.progress(1.0)

        st.markdown("""
        <div class="terminal-box">
            <span class="prompt">═══════ AI RESULT ═══════</span><br><br>
            Confidence: <span class="ok">99.999999%</span><br><br>
            Prediction: <span class="warn">You love Modiji.</span><br><br>
            <span class="dim">Model accuracy validated on 1.4 billion data points.</span>
        </div>
        """, unsafe_allow_html=True)

        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/"
            "Narendra_Modi_-_Caricature_%2814615841374%29.jpg/220px-"
            "Narendra_Modi_-_Caricature_%2814615841374%29.jpg",
            caption="The AI has spoken.",
            width=220,
        )

        if "National Asset" not in st.session_state["achievements"]:
            st.session_state["achievements"].append("National Asset")
            st.session_state["score"] += 100
            st.markdown(
                '<div class="achievement-badge">🏆 ACHIEVEMENT UNLOCKED: National Asset</div>',
                unsafe_allow_html=True,
            )

        if "ai_verification" not in st.session_state["completed"]:
            st.session_state["completed"].append("ai_verification")

        time.sleep(1)
        st.session_state["page"] = "gallery"
        st.rerun()


def page_gallery():
    st.markdown('<div class="mission-title">📸 FRIENDSHIP GALLERY</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="terminal-box">
        <span class="ok">[LOADED]</span> Evidence of friendship detected.<br>
        <span class="dim">Compiling best moments... (and some embarrassing ones)</span>
    </div>
    """, unsafe_allow_html=True)

    captions = [
        ("The squad that debugs together, stays together.", "😂"),
        ("Last seen: surviving another semester.", "🎓"),
        ("When the WiFi dropped mid-exam.", "📵"),
        ("Pre-exam confidence level: 100%.", "💪"),
        ("Post-exam reality check.", "😭"),
        ("We said we'd sleep early. We lied.", "🌙"),
    ]

    cols = st.columns(3)
    placeholder_colors = ["#1a2636", "#1a3626", "#362636", "#363626", "#362626", "#263636"]
    emojis_big = ["👥", "🎂", "💻", "📚", "🎮", "🌟"]

    for i, (cap, emoji) in enumerate(captions):
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:{placeholder_colors[i]};border-radius:8px;'
                f'padding:2rem 1rem;text-align:center;font-size:3rem;'
                f'border:1px solid #30363d;margin-bottom:0.3rem;">'
                f'{emojis_big[i]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="gallery-caption">{emoji} {cap}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.info("💡 Next year tak bhar denge photos")

    if st.button("📜 VIEW BIRTHDAY POSTER →"):
        st.session_state["page"] = "poster"
        st.rerun()


def page_poster():
    st.markdown("""
    <div class="poster-frame">
        <div style="font-size:3rem;">🎂 🎉 🎊</div>
        <div class="poster-title">HAPPY BIRTHDAY!</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;
                    color:#c9d1d9;line-height:2;margin:1rem 0;">
            May your bugs be few,<br>
            your grades be high,<br>
            and your WiFi never disconnect.
        </div>
        <div style="font-size:2rem;margin:1rem 0;">❤️ 🚀 💻</div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.85rem;
                    color:#8b949e;margin-top:1rem;">
            — From the squad, with love (and memes)
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="terminal-box" style="text-align:center;">
        <span class="ok">Age: +1 | Bugs: -∞ | Friends: ∞</span><br>
        <span class="dim">Certified: National Birthday Asset</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎁 CLAIM YOUR BIRTHDAY GIFT →"):
        st.session_state["page"] = "gift"
        st.rerun()


def page_gift():
    st.markdown('<div class="mission-title">🎁 BIRTHDAY GIFT UNLOCKING...</div>', unsafe_allow_html=True)

    attempt = st.session_state.get("gift_attempt", 0)

    if attempt == 0:
        st.markdown("""
        <div class="terminal-box">
            <span class="dim">Locating gift in secure vault...</span><br>
            <span class="warn">Decryption keys loading...</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎁 CLAIM BIRTHDAY GIFT"):
            progress_bar = st.progress(0)
            status_text  = st.empty()

            stages = [
                (10, "🔍 Locating gift..."),
                (40, "📦 Unwrapping..."),
                (75, "🔓 Decrypting..."),
                (99, "⚡ Almost there..."),
            ]

            for pct, msg in stages:
                status_text.markdown(
                    f'<div class="gift-progress-label">{msg} {pct}%</div>',
                    unsafe_allow_html=True,
                )
                progress_bar.progress(pct / 100)
                time.sleep(0.7)

            time.sleep(0.5)
            progress_bar.progress(0.99)
            st.markdown("""
            <div class="feedback-wrong">
                💥 ERROR: Gift corrupted!<br>
                <small>Exception: GiftNotFoundException at line 404<br>
                Stack trace: hope.py → expectations.py → reality.py</small>
            </div>
            """, unsafe_allow_html=True)
            st.session_state["gift_attempt"] = 1
            time.sleep(1)
            st.rerun()

    elif attempt == 1:
        st.markdown("""
        <div class="feedback-wrong">
            💥 Gift corrupted! <span style="color:#8b949e">Error code: 0xDEADBEEF</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 RETRY"):
            progress_bar = st.progress(0)
            status_text  = st.empty()

            stages = [
                (10, "🔧 Re-initialising..."),
                (40, "💾 Recovering data..."),
                (75, "🔑 Re-decrypting..."),
                (99, "✅ Finalising..."),
                (100, "🎉 Done!"),
            ]

            for pct, msg in stages:
                status_text.markdown(
                    f'<div class="gift-progress-label">{msg} {pct}%</div>',
                    unsafe_allow_html=True,
                )
                progress_bar.progress(pct / 100)
                time.sleep(0.6)

            st.session_state["gift_attempt"] = 2
            st.rerun()

    else:
        st.markdown("""
        <div class="feedback-correct">
            ✅ Gift recovered! Ready to open.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎁 OPEN GIFT"):
            if "Rickrolled" not in st.session_state["achievements"]:
                st.session_state["achievements"].append("Rickrolled")
            st.session_state["page"] = "rickroll"
            st.rerun()


def page_rickroll():
    st.markdown('<div class="mission-title">🎵 YOUR BIRTHDAY GIFT</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:1rem;">
        <iframe
            width="100%"
            height="400"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
            style="border-radius:12px;border:2px solid #ffd700;">
        </iframe>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="terminal-box" style="text-align:center;">
        <span class="ok">🎉 Congratulations.</span><br><br>
        <span class="warn">You have successfully been Rickrolled.</span><br><br>
        <span class="dim">Achievement unlocked: 🏆 Rickrolled</span>
    </div>
    """, unsafe_allow_html=True)

    if "Rickrolled" not in st.session_state["achievements"]:
        st.session_state["achievements"].append("Rickrolled")

    if st.button("🏁 VIEW FINAL RESULTS"):
        if "Birthday Boy" not in st.session_state["achievements"]:
            st.session_state["achievements"].append("Birthday Boy")
        st.session_state["page"] = "final"
        st.rerun()


def page_final():
    data = api_get("/final_result")

    st.markdown('<div class="final-title">🏆 MISSION COMPLETE 🏆</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="mission-card">
        <div class="stat-row">
            <span class="label">Physics</span>
            <span class="value pass">✅ PASSED</span>
        </div>
        <div class="stat-row">
            <span class="label">Mathematics</span>
            <span class="value pass">✅ PASSED</span>
        </div>
        <div class="stat-row">
            <span class="label">Machine Learning</span>
            <span class="value pass">✅ PASSED</span>
        </div>
        <div class="stat-row">
            <span class="label">AI Verification</span>
            <span class="value pass">✅ PASSED</span>
        </div>
        <div class="stat-row">
            <span class="label">Friendship</span>
            <span class="value special">∞</span>
        </div>
        <div class="stat-row">
            <span class="label">Modiji Loyalty</span>
            <span class="value special">100%</span>
        </div>
        <div class="stat-row">
            <span class="label">Age</span>
            <span class="value special">+1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="poster-frame" style="margin-top:1.5rem;">
        <div style="font-size:2rem;">🎂</div>
        <div style="font-family:'Orbitron',monospace;font-size:1.5rem;color:#ffd700;margin:0.5rem 0;">
            Happy Birthday!
        </div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;
                    color:#c9d1d9;line-height:2;margin:1rem 0;">
            Thanks for being an amazing friend.<br><br>
            May your code compile.<br>
            May your exams be easy.<br>
            May your bugs disappear.<br>
            And may you survive another year of engineering (unc).<br><br>
            ❤️
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏆 All Achievements")
    for ach in st.session_state["achievements"]:
        st.markdown(
            f'<div class="achievement-badge">🏆 {ach}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"""
    <div class="terminal-box" style="margin-top:1.5rem;">
        <span class="ok">Final Score: {st.session_state['score']} pts</span><br>
        <span class="dim">Candidate performance: Exceptional (except for the wrong answers)</span>
    </div>
    """, unsafe_allow_html=True)

    confetti()

    if st.button("🔄 RESTART EXAM"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────

render_sidebar()

page = st.session_state.get("page", "home")

MISSION_GUARD = {
    "maths":           "physics",
    "ml":              "maths",
    "ai_verification": "ml",
}

if page in MISSION_GUARD:
    required = MISSION_GUARD[page]
    if required not in st.session_state["completed"]:
        st.warning("⚠️ Complete the previous mission first!")
        st.session_state["page"] = "home"
        st.rerun()

if   page == "home":            page_home()
elif page == "physics":         page_mission("physics")
elif page == "maths":           page_mission("maths")
elif page == "ml":              page_mission("ml")
elif page == "ai_verification": page_ai_verification()
elif page == "gallery":         page_gallery()
elif page == "poster":          page_poster()
elif page == "gift":            page_gift()
elif page == "rickroll":        page_rickroll()
elif page == "final":           page_final()
else:
    st.error("Unknown page. Resetting...")
    st.session_state["page"] = "home"
    st.rerun()
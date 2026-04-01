import streamlit as st

st.set_page_config(layout="wide")

# 🔥 HIDE default Streamlit sidebar (auto pages menu)
hide_streamlit_style = """
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

st.set_page_config(page_title="StudyBuddy", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── ROOT VARIABLES — Fireplace Library Palette ── */
:root {
  --bg:        #1c1510;
  --surface:   #241a12;
  --card:      #2e2016;
  --amber:     #c8860a;
  --amber-soft:#e8a020;
  --ember:     #d4501a;
  --cream:     #f5e6c8;
  --parchment: #e8d5a8;
  --muted:     #a08060;
  --border:    #4a3520;
  --border-glow: rgba(200,134,10,0.35);
  --ink:       #f0ddb8;
  --wood:      #3d2a18;
}

/* ── GLOBAL ───────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'EB Garamond', Georgia, serif !important;
  background-color: var(--bg) !important;
  color: var(--ink) !important;
}

/* Main content area — dark wood feel */
.main .block-container {
  background-color: var(--surface) !important;
  background-image:
    repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(255,255,255,0.012) 60px, rgba(255,255,255,0.012) 61px),
    repeating-linear-gradient(0deg, transparent, transparent 60px, rgba(255,255,255,0.008) 60px, rgba(255,255,255,0.008) 61px);
  padding: 2.5rem 3rem !important;
  max-width: 1200px;
  border-left: 1px solid var(--border);
}

/* ── HEADINGS ──────────────────────────────────── */
h1, h2, h3, h4 {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  color: var(--amber-soft) !important;
  letter-spacing: 0.01em;
}
h1 { font-size: 2.8rem !important; font-weight: 700 !important; text-shadow: 0 0 40px rgba(200,134,10,0.3); }
h2 { font-size: 2rem !important; font-weight: 600 !important; }
h3 { font-size: 1.4rem !important; font-weight: 600 !important;
     border-bottom: 1px solid var(--border-glow) !important;
     padding-bottom: 6px; margin-top: 1.4rem !important; }

/* ── SIDEBAR — Dark mahogany bookshelf ─────────── */
section[data-testid="stSidebar"] {
  background-color: var(--wood) !important;
  background-image:
    repeating-linear-gradient(
      180deg,
      transparent, transparent 28px,
      rgba(0,0,0,0.15) 28px, rgba(0,0,0,0.15) 29px
    ),
    repeating-linear-gradient(
      90deg,
      transparent, transparent 8px,
      rgba(255,255,255,0.018) 8px, rgba(255,255,255,0.018) 9px
    ) !important;
  border-right: 2px solid var(--amber) !important;
  box-shadow: 4px 0 24px rgba(0,0,0,0.6) !important;
}
section[data-testid="stSidebar"] * { color: var(--cream) !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
  font-family: 'Cormorant Garamond', serif !important;
  color: var(--amber-soft) !important;
  border-bottom: 1px solid rgba(200,134,10,0.3) !important;
}
section[data-testid="stSidebar"] .stRadio label {
  font-family: 'EB Garamond', serif !important;
  font-size: 1rem !important;
  padding: 5px 0;
  transition: all 0.2s;
  letter-spacing: 0.02em;
}
section[data-testid="stSidebar"] .stRadio label:hover {
  color: var(--amber-soft) !important;
  text-shadow: 0 0 12px rgba(232,160,32,0.5);
}

/* ── BUTTONS — candlelit glow ──────────────────── */
.stButton > button {
  background-color: var(--card) !important;
  color: var(--amber-soft) !important;
  font-family: 'Cormorant Garamond', serif !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  border: 1px solid var(--amber) !important;
  border-radius: 3px !important;
  padding: 0.55rem 1.5rem !important;
  transition: all 0.2s ease !important;
  letter-spacing: 0.05em;
  box-shadow: 0 0 10px rgba(200,134,10,0.1) !important;
}
.stButton > button:hover {
  background-color: var(--amber) !important;
  color: var(--bg) !important;
  box-shadow: 0 0 20px rgba(200,134,10,0.4) !important;
  transform: translateY(-1px) !important;
}

/* ── INPUTS ────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
  font-family: 'EB Garamond', serif !important;
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  color: var(--cream) !important;
  font-size: 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--amber) !important;
  box-shadow: 0 0 0 2px rgba(200,134,10,0.2) !important;
}

/* ── METRIC CARDS — ember glow ─────────────────── */
.metric-card {
  background: var(--card);
  border-radius: 4px;
  padding: 22px 20px;
  text-align: center;
  border: 1px solid var(--border);
  border-top: 3px solid var(--amber);
  box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 16px rgba(200,134,10,0.08);
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--amber), transparent);
  opacity: 0.5;
}
.metric-card h2 {
  color: var(--amber-soft) !important;
  font-size: 2.8rem !important;
  margin: 0 0 4px 0 !important;
  border-bottom: none !important;
  padding-bottom: 0 !important;
  text-shadow: 0 0 20px rgba(232,160,32,0.4);
}
.metric-card p {
  color: var(--muted);
  margin: 0;
  font-size: 0.82rem;
  font-family: 'EB Garamond', serif;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

/* ── TIP BOX — parchment note ──────────────────── */
.tip-box {
  background: var(--card);
  border-left: 3px solid var(--amber);
  border-radius: 0 4px 4px 0;
  padding: 18px 22px;
  margin: 10px 0;
  font-family: 'EB Garamond', serif;
  font-size: 1rem;
  line-height: 1.8;
  color: var(--cream);
  box-shadow: inset 0 0 30px rgba(0,0,0,0.2);
}

/* ── EXPANDERS ─────────────────────────────────── */
.streamlit-expanderHeader {
  font-family: 'Cormorant Garamond', serif !important;
  font-weight: 600 !important;
  color: var(--amber-soft) !important;
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
}

/* ── DATAFRAMES ────────────────────────────────── */
.stDataFrame {
  border: 1px solid var(--border) !important;
  border-radius: 4px !important;
  font-family: 'EB Garamond', serif !important;
}

/* ── ALERTS ────────────────────────────────────── */
.stSuccess, .stInfo, .stWarning, .stError {
  font-family: 'EB Garamond', serif !important;
  border-radius: 3px !important;
}

/* ── DIVIDER ───────────────────────────────────── */
hr {
  border: none !important;
  border-top: 1px solid var(--border-glow) !important;
  margin: 1.5rem 0 !important;
}

/* ── CODE ──────────────────────────────────────── */
code, pre, .stCode {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.84rem !important;
  background-color: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  color: var(--amber-soft) !important;
}

/* ── CHAT MESSAGES ─────────────────────────────── */
.stChatMessage {
  font-family: 'EB Garamond', serif !important;
  border-radius: 4px !important;
  background-color: var(--card) !important;
}

/* ── TABS ──────────────────────────────────────── */
.stTabs [data-baseweb="tab"] {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.05rem !important;
  color: var(--muted) !important;
}
.stTabs [aria-selected="true"] {
  color: var(--amber-soft) !important;
  border-bottom: 2px solid var(--amber) !important;
}

/* ── LOGIN HERO ────────────────────────────────── */
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 4.5rem;
  font-weight: 700;
  color: var(--amber-soft);
  line-height: 1.1;
  letter-spacing: 0.02em;
  text-shadow: 0 0 60px rgba(200,134,10,0.4);
}
.hero-sub {
  font-family: 'EB Garamond', serif;
  font-size: 1.2rem;
  color: var(--muted);
  font-style: italic;
  margin-top: 0.5rem;
}
.ornament {
  color: var(--amber);
  font-size: 1.4rem;
  letter-spacing: 0.3em;
  text-shadow: 0 0 12px rgba(200,134,10,0.5);
}
.login-wrap {
  background: var(--card);
  border: 1px solid var(--border);
  border-top: 3px solid var(--amber);
  border-radius: 0 0 6px 6px;
  padding: 28px 32px;
  box-shadow: 0 16px 48px rgba(0,0,0,0.5);
  max-width: 480px;
  margin: 0 auto;
}

/* ── SCROLLBAR ─────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--amber); }
</style>
""", unsafe_allow_html=True)

# ── API KEY ────────────────────────────────────────────
# 🔑 Groq API Key
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# ── AUTH ───────────────────────────────────────────────
with open("config.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# ── LOGIN SCREEN ───────────────────────────────────────
if not st.session_state.get("authentication_status"):
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
        <div style='text-align:center; padding: 48px 0 24px'>
          <div class='ornament'>✦ ✦ ✦</div>
          <div class='hero-title'>StudyBuddy</div>
          <div class='hero-sub'>Your intelligent study companion</div>
          <div class='ornament' style='margin-top:16px'>──────────</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Sign In", "Create Account"])
        with tab_login:
            authenticator.login(location="main")
            if st.session_state.get("authentication_status") is False:
                st.error("Incorrect username or password.")
            elif st.session_state.get("authentication_status") is None:
                st.caption("Enter your credentials above to continue.")
        with tab_register:
            try:
                if authenticator.register_user(location="main"):
                    st.success("Account created! Please sign in.")
                    with open("config.yaml", "w") as f:
                        yaml.dump(config, f, default_flow_style=False)
            except Exception as e:
                st.error(str(e))

# ── MAIN APP ───────────────────────────────────────────
if st.session_state.get("authentication_status"):
    username = st.session_state["username"]
    name     = st.session_state["name"]

    with st.sidebar:
        st.markdown(f"""
        <div style='padding: 20px 0 12px; text-align:center;'>
          <div style='font-family: Playfair Display, serif; font-size:1.5rem; font-weight:900; color:#f5deb3;'>📚 StudyBuddy</div>
          <div style='font-size:0.8rem; color:rgba(250,246,239,0.5); letter-spacing:0.15em; text-transform:uppercase; margin-top:4px;'>Study Companion</div>
          <div style='margin-top:14px; padding:10px 14px; background:rgba(184,134,11,0.15); border-radius:4px; border:1px solid rgba(184,134,11,0.3);'>
            <div style='font-size:0.75rem; color:rgba(250,246,239,0.55); text-transform:uppercase; letter-spacing:0.1em;'>Logged in as</div>
            <div style='font-family: Playfair Display, serif; font-size:1rem; color:#f5deb3; font-weight:700; margin-top:2px;'>{name}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        page = st.radio("Navigate", [
            "🏠 Dashboard",
            "✅ Assignment Manager",
            "📄 Flashcard Generator",
            "🧠 AI Study Q&A",
            "📝 AI Task Prioritizer",
            "❓ AI Quiz Generator",
            "⏱️ Pomodoro Timer",
            "🎵 Ambient Music",
            "😊 Mood Tracker",
            "📊 Analytics",
            "📈 Grades Tracker",
        ], label_visibility="hidden")

        st.markdown("---")
        authenticator.logout("Sign Out", location="sidebar")

    # ── PAGE ROUTING ───────────────────────────────────
    if page == "🏠 Dashboard":
        from pages.dashboard import show; show(username)
    elif page == "✅ Assignment Manager":
        from pages.assignments import show; show(username)
    elif page == "📄 Flashcard Generator":
        from pages.flashcards import show; show(GROQ_API_KEY, username)
    elif page == "🧠 AI Study Q&A":
        from pages.study_qa import show; show(GROQ_API_KEY, username)
    elif page == "📝 AI Task Prioritizer":
        from pages.ai_tasks import show; show(GROQ_API_KEY, username)
    elif page == "❓ AI Quiz Generator":
        from pages.quiz import show; show(GROQ_API_KEY, username)
    elif page == "⏱️ Pomodoro Timer":
        from pages.pomodoro import show; show()
    elif page == "🎵 Ambient Music":
        from pages.ambient import show; show()
    elif page == "😊 Mood Tracker":
        from pages.mood import show; show(GROQ_API_KEY, username)
    elif page == "📊 Analytics":
        from pages.analytics import show; show(username)
    elif page == "📈 Grades Tracker":
        from pages.grades import show; show(GROQ_API_KEY, username)

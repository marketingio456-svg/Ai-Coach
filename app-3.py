one
"""
ExamZen AI Study Coach for JEE/NEET Aspirants
Version 3.0 | Production-Ready | Mobile-First
Model: gemini-1.5-flash (15 RPM free quota)
"""
import streamlit as st
import os
import time
from google import genai
from google.genai import types

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
   page_title="ExamZen AI Study Coach",
   page_icon="🎓",
   layout="centered",
   initial_sidebar_state="collapsed",
)

# ==============================================================================
# 2. COMPLETE STYLE SYSTEM
# ==============================================================================
st.markdown("""
<style>
/* FONTS */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300&family=DM+Mono:wght@400;500&display=swap');

/* DESIGN TOKENS */
:root {
   /* Backgrounds */
   --bg-base: #07090E;
   --bg-surface: #0C1018;
   --bg-card: #101520;
   --bg-elevated: #141C28;
   --bg-input: #0E1319;
   
   /* Borders */
   --border-soft: rgba(255,255,255,0.06);
   --border-mid: rgba(255,255,255,0.09);
   --border-strong: rgba(255,255,255,0.13);
   
   /* Brand colors */
   --blue: #3B82F6;
   --blue-light: #60A5FA;
   --blue-glow: rgba(59,130,246,0.15);
   --indigo: #6366F1;
   --cyan: #06B6D4;
   --emerald: #10B981;
   --amber: #F59E0B;
   --rose: #F43F5E;
   
   /* Gradients */
   --grad-brand: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
   --grad-emerald: linear-gradient(135deg, #10B981 0%, #06B6D4 100%);
   --grad-amber: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
   
   /* Typography */
   --text-primary: #F0F4FF;
   --text-secondary: #A8B5CC;
   --text-muted: #5A6A85;
   --text-faint: #3A4A62;
   
   /* Spacing & Radius */
   --radius-sm: 8px;
   --radius-md: 12px;
   --radius-lg: 16px;
   --radius-xl: 20px;
}

/* RESET & BASE */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
   font-family: 'Plus Jakarta Sans', apple-system, sans-serif !important;
   color: var(--text-secondary) !important;
   background-color: var(--bg-base) !important;
   -webkit-font-smoothing: antialiased;
}

.stApp {
   background: var(--bg-base) !important;
   min-height: 100vh;
}

/* Noise texture overlay */
.stApp::after {
   content: '';
   position: fixed;
   inset: 0;
   background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
   pointer-events: none;
   z-index: 9999;
   opacity: 0.4;
}

/* HIDE STREAMLIT CHROME */
header, [data-testid="collapsedControl"], .stDeployButton, section [data-testid="stSidebar"] {
   display: none !important;
}

/* LAYOUT CONTAINER */
.block-container {
   padding: 0 1rem 2rem 1rem !important;
   max-width: 540px !important;
   margin: 0 auto !important;
}

/* ANIMATIONS */
@keyframes fadeUp {
   from { opacity: 0; transform: translateY(16px); }
   to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
   from { opacity: 0; }
   to { opacity: 1; }
}
@keyframes shimmerPulse {
   0%, 100% { opacity: 0.6; }
   50% { opacity: 1; }
}

/* HEADER STYLE */
.ez-header {
   display: flex;
   align-items: center;
   justify-content: space-between;
   padding: 1rem 0 0.5rem;
   margin-bottom: 0.5rem;
   animation: fadeIn 0.4s ease;
}
.ez-logo {
   display: flex;
   align-items: center;
   gap: 0.5rem;
}
.ez-logo-icon {
   width: 34px; height: 34px;
   background: var(--grad-brand);
   border-radius: 10px;
   display: flex;
   align-items: center;
   justify-content: center;
   font-size: 1rem;
   box-shadow: 0 4px 14px rgba(59,130,246,0.35);
}
.ez-logo-text {
   font-size: 1.1rem;
   font-weight: 800;
   color: var(--text-primary) !important;
   letter-spacing: -0.03em;
}
.ez-logo-text span {
   background: var(--grad-brand);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
   background-clip: text;
}
.ez-status {
   display: flex;
   align-items: center;
   gap: 0.35rem;
   background: rgba(16,185,129,0.08);
   border: 1px solid rgba(16,185,129,0.18);
   border-radius: 20px;
   padding: 0.3rem 0.7rem;
   font-size: 0.72rem;
   font-weight: 600;
   color: var(--emerald);
   letter-spacing: 0.04em;
}
.ez-status-dot {
   width: 6px; height: 6px;
   background: var(--emerald);
   border-radius: 50%;
   animation: shimmerPulse 2s infinite;
}
.ez-status-err {
   background: rgba(244,63,94,0.08);
   border-color: rgba(244,63,94,0.18);
   color: var(--rose);
}
.ez-status-err .ez-status-dot {
   background: var(--rose);
}

/* TAB BAR CUSTOMIZATION */
.stTabs { margin-top: 0.5rem; }
.stTabs [data-baseweb="tab-list"] {
   background: var(--bg-surface) !important;
   border: 1px solid var(--border-soft) !important;
   border-radius: var(--radius-lg) !important;
   padding: 4px !important;
   gap: 2px !important;
   overflow-x: auto !important;
}
.stTabs [data-baseweb="tab"] {
   background: transparent !important;
   border: none !important;
   border-radius: var(--radius-md) !important;
   color: var(--text-muted) !important;
   font-size: 0.8rem !important;
   font-weight: 600 !important;
   padding: 0.5rem 0.9rem !important;
   transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
   color: var(--text-secondary) !important;
   background: var(--bg-elevated) !important;
}
.stTabs [aria-selected="true"] {
   background: var(--grad-brand) !important;
   color: #FFFFFF !important;
   box-shadow: 0 2px 12px rgba(59,130,246,0.3) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* UTILITY CLASSES */
.sec-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.5rem; }
.sec-title { font-size: 1.5rem; font-weight: 800; color: var(--text-primary) !important; letter-spacing: -0.02em; line-height: 1.2; margin-bottom: 0.35rem; }
.sec-sub { font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 1.2rem; font-weight: 300; }

.hero-wrap { text-align: center; padding: 1.8rem 0.5rem 1rem; animation: fadeUp 0.5s ease; }
.hero-badge { display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); color: var(--blue-light); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.3rem 0.85rem; border-radius: 20px; margin-bottom: 1.1rem; }
.hero-h1 { font-size: 2.2rem; font-weight: 800; color: var(--text-primary) !important; letter-spacing: -0.03em; line-height: 1.15; margin-bottom: 0.7rem; }
.hero-h1 .grad { background: linear-gradient(135deg, #60A5FA, #818CF8, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-p { font-size: 0.9rem; color: var(--text-muted); line-height: 1.65; max-width: 340px; margin: 0 auto 1.5rem; font-weight: 300; }
.hero-pills { display: flex; justify-content: center; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.8rem; }
.hero-pill { background: var(--bg-elevated); border: 1px solid var(--border-soft); border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.75rem; font-weight: 500; color: var(--text-secondary); }

.fcard-grid { display: flex; flex-direction: column; gap: 0.75rem; margin: 1.5rem 0 1rem; }
.fcard { background: var(--bg-card); border: 1px solid var(--border-soft); border-radius: var(--radius-xl); padding: 1.1rem 1.2rem; display: flex; align-items: center; gap: 1rem; transition: all 0.22s ease; animation: fadeUp 0.5s ease both; position: relative; }
.fcard::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; border-radius: 3px 0 0 3px; }
.fcard-1::before { background: var(--blue); }
.fcard-2::before { background: var(--indigo); }
.fcard-3::before { background: var(--emerald); }
.fcard:hover { border-color: var(--border-strong); transform: translateY(-1px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
.fcard-icon-wrap { width: 46px; height: 46px; border-radius: 13px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; flex-shrink: 0; }
.fcard-1 .fcard-icon-wrap { background: rgba(59,130,246,0.12); }
.fcard-2 .fcard-icon-wrap { background: rgba(99,102,241,0.12); }
.fcard-3 .fcard-icon-wrap { background: rgba(16,185,129,0.12); }
.fcard-content { flex: 1; min-width: 0; }
.fcard-tag { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.2rem; }
.fcard-1 .fcard-tag { color: var(--blue-light); }
.fcard-2 .fcard-tag { color: #818CF8; }
.fcard-3 .fcard-tag { color: var(--emerald); }
.fcard-name { font-size: 0.95rem; font-weight: 700; color: var(--text-primary) !important; margin-bottom: 0.25rem; }
.fcard-desc { font-size: 0.78rem; color: var(--text-muted); line-height: 1.5; }
.fcard-chevron { color: var(--text-faint); font-size: 1rem; flex-shrink: 0; }

.info-card { background: rgba(59,130,246,0.05); border: 1px solid rgba(59,130,246,0.12); border-radius: var(--radius-lg); padding: 0.95rem 1.1rem; font-size: 0.83rem; color: var(--text-muted); line-height: 1.65; margin: 1rem 0; }
.info-card b { color: var(--text-secondary); font-weight: 600; }
.info-card .info-title { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--blue-light); margin-bottom: 0.5rem; }

.alert-rate { background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.2); border-radius: var(--radius-lg); padding: 1.1rem 1.2rem; margin: 1rem 0; }
.alert-rate-title { font-size: 0.88rem; font-weight: 700; color: var(--amber); margin-bottom: 0.4rem; }
.alert-rate-body { font-size: 0.82rem; color: var(--text-muted); line-height: 1.6; }
.alert-rate-body b { color: var(--text-secondary); }

.alert-err { background: rgba(244,63,94,0.06); border: 1px solid rgba(244,63,94,0.15); border-radius: var(--radius-lg); padding: 0.9rem 1.1rem; font-size: 0.83rem; color: #FB7185; margin: 1rem 0; }
.alert-err-title { font-weight: 700; margin-bottom: 0.25rem; }

.result-wrap { background: var(--bg-card); border: 1px solid var(--border-soft); border-radius: var(--radius-xl); padding: 1.3rem; margin-top: 1.1rem; animation: fadeUp 0.4s ease; }
.result-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; padding-bottom: 0.7rem; border-bottom: 1px solid var(--border-soft); }
.result-icon { width: 10px; height: 10px; background: var(--emerald); border-radius: 50%; }
.result-title { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--emerald); }

/* CHAT FEED */
.chat-feed { display: flex; flex-direction: column; gap: 0.9rem; margin: 0.5rem 0 1rem; }
.msg-row-user { display: flex; justify-content: flex-end; animation: fadeUp 0.3s ease; margin-bottom: 0.5rem; }
.msg-bubble-user { background: var(--grad-brand); color: #FFFFFF; border-radius: 18px 18px 4px 18px; padding: 0.8rem 1rem; max-width: 82%; font-size: 0.88rem; line-height: 1.6; box-shadow: 0 4px 16px rgba(59,130,246,0.2); word-wrap: break-word; }
.msg-row-ai { display: flex; align-items: flex-start; gap: 0.6rem; animation: fadeUp 0.3s ease; margin-bottom: 0.5rem; }
.msg-avatar { width: 30px; height: 30px; background: var(--grad-brand); border-radius: 9px; flex-shrink: 0; box-shadow: 0 2px 10px rgba(59,130,246,0.25); }
.msg-bubble-ai-wrap { background: var(--bg-card); border: 1px solid var(--border-soft); border-radius: 4px 18px 18px 18px; padding: 0.9rem 1rem; max-width: 85%; width: 100%; }

/* INPUT EXTRAS OVERRIDE */
.stTextArea label, .stTextInput label, .stSelectbox label, .stNumberInput label, .stSlider label { font-size: 0.75rem !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; color: var(--text-muted) !important; }
.stTextArea textarea, .stTextInput input { background: var(--bg-input) !important; border: 1px solid var(--border-soft) !important; color: var(--text-secondary) !important; }

/* BUTTON SYSTEMS */
.stButton > button { background: var(--grad-brand) !important; color: #FFFFFF !important; font-weight: 700 !important; border: none !important; border-radius: var(--radius-md) !important; padding: 0.65rem 1.5rem !important; transition: all 0.2s ease !important; width: 100% !important; }
.stButton > button:hover { transform: translateY(-2px) !important; filter: brightness(1.05) !important; }
.stDownloadButton > button { background: transparent !important; color: var(--blue-light) !important; border: 1px solid rgba(59,130,246,0.25) !important; }

.ez-divider { border: none; border-top: 1px solid var(--border-soft); margin: 1.2rem 0; }
.chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.5rem 0 1rem; }
.chip { background: var(--bg-elevated); border: 1px solid var(--border-soft); border-radius: 20px; padding: 0.25rem 0.7rem; font-size: 0.73rem; font-weight: 500; color: var(--text-muted); }
.log-item { display: flex; align-items: center; gap: 0.6rem; background: var(--bg-card); border: 1px solid var(--border-soft); border-radius: var(--radius-md); padding: 0.6rem 0.85rem; margin-bottom: 0.4rem; }
.log-subj { background: rgba(99,102,241,0.1); color: #818CF8; border-radius: 6px; padding: 0.1rem 0.45rem; font-size: 0.68rem; font-weight: 700; }
.log-text { font-size: 0.78rem; color: var(--text-muted); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. GEMINI CLIENT ROBUST INITIALIZATION
# ==============================================================================
@st.cache_resource(show_spinner=False)
def get_client():
   """Initialize Gemini client safely across multiple setup styles."""
   api_key = None
   try:
       api_key = st.secrets["GEMINI_API_KEY"]
   except Exception:
       pass
   if not api_key:
       api_key = os.environ.get("GEMINI_API_KEY", "")
   if not api_key:
       return None
   try:
       return genai.Client(api_key=api_key)
   except Exception:
       return None

def call_gemini(client, prompt: str, system: str, temperature: float = 0.7) -> dict:
   """Dispatches payload to Model Endpoint returning operational statuses."""
   try:
       response = client.models.generate_content(
           model="gemini-1.5-flash",
           contents=prompt,
           config=types.GenerateContentConfig(
               system_instruction=system,
               temperature=temperature,
               max_output_tokens=2048,
           ),
       )
       return {"ok": True, "text": response.text}
   except Exception as e:
       err = str(e)
       if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
           wait = "60"
           for part in err.split():
               if part.replace(".", "").isdigit():
                   wait = str(int(float(part)))
                   break
           return {"ok": False, "kind": "rate_limit", "wait": wait}
       return {"ok": False, "kind": "error", "msg": err[:200]}

def show_api_result(result: dict):
   """Render AI output container utilizing native markdown layers properly."""
   if result["ok"]:
       st.markdown("""
       <div class='result-wrap'>
           <div class='result-header'>
               <div class='result-icon'></div>
               <div class='result-title'>AI Response</div>
           </div>
       """, unsafe_allow_html=True)
       st.markdown(result['text'])
       st.markdown("</div>", unsafe_allow_html=True)
   elif result["kind"] == "rate_limit":
       st.markdown(f"""
       <div class='alert-rate'>
           <div class='alert-rate-title'>Rate Limit Reached</div>
           <div class='alert-rate-body'>
               You've hit the free-tier limit (15 requests/minute).<br>
               <b>Please wait ~ {result.get('wait', '60')} seconds</b> and try again.<br><br>
               <b>Tip:</b> This is an organic API constraint that updates auto-hourly.
           </div>
       </div>
       """, unsafe_allow_html=True)
   else:
       st.markdown(f"""
       <div class='alert-err'>
           <div class='alert-err-title'>⚠️ Something went wrong</div>
           {result.get('msg', 'Unknown error processing logic')}
       </div>
       """, unsafe_allow_html=True)

# ==============================================================================
# 4. SYSTEM PROMPTS CAREFULLY ENGINEERED
# ==============================================================================
MENTOR_SYSTEM = """You are Arya, an elite JEE/NEET mentor with 15+ years of top IIT coaching experience.
RESPONSE STRUCTURE:
1. **Real-World Analogy** in bold text.
2. **The Concept** clear presentation.
3. **Formula / Key Rule** breakdown equations cleanly.
4. **Common Mistake** conceptual errors.
5. **Exam Tip** specific focus hooks.
Keep tone warm, clear, encouraging. Only clear topics within Math, Physics, Bio, and Chemistry."""

CORRECTIFY_SYSTEM = """You are CorrectifyAI, a world-class JEE/NEET mistake diagnostician.
Produce EXACTLY this structure layout:
## Root Error
## Why This Is Wrong
## Correct Approach
## Topic to Revise
## Memory Hook"""

TIMETABLE_SYSTEM = """You are PlannerAI, a strategic JEE/NEET revision planner using spaced repetition blocks.
Create a personalized structured revision timeline output matching the hourly limits requested."""

# ==============================================================================
# 5. SESSION STATE
# ==============================================================================
defaults = {
   "mentor_history": [],
   "mistake_log": [],
}
for k, v in defaults.items():
   if k not in st.session_state:
       st.session_state[k] = v

# ==============================================================================
# 6. APP GLOBAL HEADER
# ==============================================================================
client = get_client()
if client:
   status_html = "<div class='ez-status'><span class='ez-status-dot'></span>AI Live</div>"
else:
   status_html = "<div class='ez-status ez-status-err'><span class='ez-status-dot'></span>No Key</div>"

st.markdown(f"""
<div class='ez-header'>
   <div class='ez-logo'>
       <div class='ez-logo-icon'>🎓</div>
       <div class='ez-logo-text'>Exam<span>Zen</span></div>
   </div>
   {status_html}
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. MAIN INTERFACE SYSTEM
# ==============================================================================
tab_home, tab_mentor, tab_fix, tab_plan = st.tabs(["Home", "Mentor", "Correctify", "Planner"])

# --- TAB 1: HOME ---
with tab_home:
   st.markdown("""
   <div class='hero-wrap'>
       <div class='hero-badge'>AI-Powered Hub</div>
       <div class='hero-h1'>Free JEE & NEET<br>Study Smarter. <span class='grad'>Score Higher.</span></div>
       <p class='hero-p'>Your customized dashboard providing elite strategic coaching routines instantly.</p>
       <div class='hero-pills'>
           <span class='hero-pill'>Physics</span>
           <span class='hero-pill'>Chemistry</span>
           <span class='hero-pill'>Biology</span>
           <span class='hero-pill'>Mathematics</span>
       </div>
   </div>
   <div class='fcard-grid'>
       <div class='fcard fcard-1'>
           <div class='fcard-icon-wrap'>💡</div>
           <div class='fcard-content'>
               <div class='fcard-tag'>Arya Mentor</div>
               <div class='fcard-name'>Concept Explainer</div>
               <div class='fcard-desc'>Ask conceptual problems and receive structured breakdowns with analogies.</div>
           </div>
       </div>
       <div class='fcard fcard-2'>
           <div class='fcard-icon-wrap'>🎯</div>
           <div class='fcard-content'>
               <div class='fcard-tag'>Correctify</div>
               <div class='fcard-name'>Mistake Fixer</div>
               <div class='fcard-desc'>Submit errors or answers to systematically resolve structural flaws.</div>
           </div>
       </div>
       <div class='fcard fcard-3'>
           <div class='fcard-icon-wrap'>📅</div>
           <div class='fcard-content'>
               <div class='fcard-tag'>Planner</div>
               <div class='fcard-name'>7-Day Timetable</div>
               <div class='fcard-desc'>Construct tailored weekly programs targeting structural weak points.</div>
           </div>
       </div>
   </div>
   """, unsafe_allow_html=True)
   
   if not client:
       st.markdown("""
       <div class='alert-err'>
           <div class='alert-err-title'>🔑 API Key Required</div>
           Please map your credentials within Streamlit environment spaces to access backend layers.
       </div>
       """, unsafe_allow_html=True)

# --- TAB 2: MENTOR CHAT ---
with tab_mentor:
   st.markdown("""
   <div class='sec-label'>AI Mentor Concept Clarity</div>
   <div class='sec-title'>Arya Mentor</div>
   <div class='sec-sub'>Ask any JEE/NEET foundational framework to receive optimized insights.</div>
   <div class='chip-row'>
       <span class='chip'>Newton's Laws</span><span class='chip'>Gauss's Law</span>
       <span class='chip'>Thermodynamics</span><span class='chip'>Chemical Bonding</span>
   </div>
   <hr class='ez-divider'>
   """, unsafe_allow_html=True)
   
   if not client:
       st.markdown("<div class='alert-err'>API Key missing inside your configurations setup.</div>", unsafe_allow_html=True)
   else:
       # Render clean feed rows
       for msg in st.session_state.mentor_history:
           if msg["role"] == "user":
               st.markdown(f"<div class='msg-row-user'><div class='msg-bubble-user'>{msg['content']}</div></div>", unsafe_allow_html=True)
           else:
               st.markdown("<div class='msg-row-ai'><div class='msg-avatar'></div><div class='msg-bubble-ai-wrap'>", unsafe_allow_html=True)
               st.markdown(msg['content'])
               st.markdown("</div></div>", unsafe_allow_html=True)
       
       user_input = st.chat_input("Ask Arya anything...")
       if user_input:
           stripped = user_input.strip()
           if len(stripped) >= 4:
               st.session_state.mentor_history.append({"role": "user", "content": stripped})
               with st.spinner("Arya planning response..."):
                   result = call_gemini(client, stripped, MENTOR_SYSTEM, 0.65)
                   if result["ok"]:
                       st.session_state.mentor_history.append({"role": "assistant", "content": result["text"]})
                       st.rerun()
                   else:
                       show_api_result(result)

       if st.session_state.mentor_history:
           if st.button("Clear History"):
               st.session_state.mentor_history = []
               st.rerun()

# --- TAB 3: CORRECTIFY ---
with tab_fix:
   st.markdown("""
   <div class='sec-label'>Error Diagnosis Mistake Log</div>
   <div class='sec-title'>Correctify AI</div>
   <div class='sec-sub'>Deconstruct incorrect analytical reasoning to diagnose process bottlenecks.</div>
   """, unsafe_allow_html=True)
   
   if not client:
       st.markdown("<div class='alert-err'>Active deployment key needed.</div>", unsafe_allow_html=True)
   else:
       subject = st.selectbox("Subject Track", ["Physics", "Chemistry", "Biology", "Mathematics"])
       question_text = st.text_area("The Original Problem Framework", placeholder="Input root premise details...", height=85)
       wrong_answer = st.text_area("Your Mistaken Logic Chain (Required)", placeholder="Trace structural process path or blindspots...", height=130)
       
       if st.button("Diagnose My Mistake", key="diagnose_btn"):
           if not wrong_answer.strip():
               st.error("Please supply baseline process notes to review.")
           else:
               prompt = f"Subject: {subject}\nQuestion Context: {question_text}\nStudent Process: {wrong_answer}"
               with st.spinner("Analyzing operational logic errors..."):
                   result = call_gemini(client, prompt, CORRECTIFY_SYSTEM, 0.35)
                   show_api_result(result)
                   if result["ok"]:
                       st.session_state.mistake_log.append({"subject": subject, "preview": wrong_answer.strip()[:50]})

       if st.session_state.mistake_log:
           st.markdown("<hr class='ez-divider'><h5>Session Log</h5>", unsafe_allow_html=True)
           for i, entry in enumerate(reversed(st.session_state.mistake_log)):
               st.markdown(f"<div class='log-item'><span class='log-subj'>{entry['subject']}</span> <span class='log-text'>{entry['preview']}...</span></div>", unsafe_allow_html=True)

# --- TAB 4: PLANNER ---
with tab_plan:
   st.markdown("""
   <div class='sec-label'>Smart Revision Architecture</div>
   <div class='sec-title'>7-Day Planner</div>
   """, unsafe_allow_html=True)
   
   if not client:
       st.markdown("<div class='alert-err'>Provide backend environment profiles to track calendars.</div>", unsafe_allow_html=True)
   else:
       exam_target = st.selectbox("Target Milestone Focus", ["JEE Main", "JEE Advanced", "NEET UG"])
       weak_topics = st.text_area("Weak Target Domains (Comma-Separated)", placeholder="Topics needing algorithmic optimization...")
       strong_topics = st.text_area("Strong Consolidations", placeholder="Light systemic sync maintenance...")
       daily_hours = st.select_slider("Daily Focus Window allocation", options=[4, 6, 8, 10, 12], value=6)
       
       if st.button("Generate My 7-Day Plan"):
           if not weak_topics.strip():
               st.error("Please insert focus fields to structure routine paths.")
           else:
               prompt = f"Target: {exam_target}\nWeak points: {weak_topics}\nStrong areas: {strong_topics}\nHours: {daily_hours}"
               with st.spinner("Assembling scheduling matrices..."):
                   result = call_gemini(client, prompt, TIMETABLE_SYSTEM, 0.5)
                   show_api_result(result)
                   if result["ok"]:
                       st.download_button("Download Strategy File (.txt)", data=result["text"], file_name="study_plan.txt")

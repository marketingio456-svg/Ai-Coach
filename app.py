import streamlit as st
import os
import google.generativeai as genai
from google.generativeai import types

# ==============================================================================
# 1. PAGE CONFIGURATION (MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND)
# ==============================================================================
st.set_page_config(
   page_title="ExamZen AI Study Coach",
   page_icon="🎓",
   layout="centered",
   initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. PREMIUM LIGHTS-OUT UI CUSTOM STYLESHEET
# ==============================================================================
st.markdown("""
<style>
/* FONTS */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

/* GLOBAL DESIGN SYSTEM TOKENS */
:root {
   --bg-base: #05070A;
   --bg-surface: #0B0E14;
   --bg-card: #111622;
   --bg-elevated: #171E2E;
   --bg-input: #080B11;
   
   --border-soft: rgba(255,255,255,0.05);
   --border-mid: rgba(255,255,255,0.09);
   --border-strong: rgba(255,255,255,0.15);
   
   --brand-primary: #3B82F6;
   --brand-glow: rgba(59,130,246,0.15);
   --emerald: #10B981;
   --amber: #F59E0B;
   --rose: #F43F5E;
   
   --grad-brand: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
   --grad-glow: linear-gradient(135deg, rgba(59,130,246,0.2) 0%, rgba(99,102,241,0.2) 100%);
   
   --text-primary: #F1F5F9;
   --text-secondary: #94A3B8;
   --text-muted: #64748B;
   
   --radius-md: 12px;
   --radius-lg: 16px;
   --radius-xl: 24px;
}

/* APP BASE RESET */
html, body, [class*="css"] {
   font-family: 'Plus Jakarta Sans', sans-serif !important;
   color: var(--text-secondary) !important;
   background-color: var(--bg-base) !important;
}

.stApp {
   background: var(--bg-base) !important;
}

/* HIDE STREAMLIT BRANDING AND NAVIGATION FOOTERS */
header, [data-testid="collapsedControl"], .stDeployButton, footer, #MainMenu {
   display: none !important;
}

/* APP WINDOW WIDTH LOCK */
.block-container {
   padding: 1rem 1rem 3rem 1rem !important;
   max-width: 520px !important;
   margin: 0 auto !important;
}

/* APPLICATION NAVBAR HEADER */
.ez-header {
   display: flex;
   align-items: center;
   justify-content: space-between;
   padding: 0.75rem 0;
   margin-bottom: 1.5rem;
   border-bottom: 1px solid var(--border-soft);
}
.ez-logo {
   display: flex;
   align-items: center;
   gap: 0.6rem;
}
.ez-logo-icon {
   font-size: 1.4rem;
}
.ez-logo-text {
   font-family: 'Space Grotesk', sans-serif;
   font-size: 1.25rem;
   font-weight: 700;
   color: var(--text-primary) !important;
   letter-spacing: -0.02em;
}
.ez-logo-text span {
   background: var(--grad-brand);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
}
.ez-status {
   display: flex;
   align-items: center;
   gap: 0.4rem;
   background: rgba(16,185,129,0.06);
   border: 1px solid rgba(16,185,129,0.15);
   border-radius: 30px;
   padding: 0.35rem 0.75rem;
   font-size: 0.75rem;
   font-weight: 600;
   color: var(--emerald);
}
.ez-status-dot {
   width: 6px;
   height: 6px;
   background: var(--emerald);
   border-radius: 50%;
   box-shadow: 0 0 8px var(--emerald);
}
.ez-status-err {
   background: rgba(244,63,94,0.06);
   border-color: rgba(244,63,94,0.15);
   color: var(--rose);
}
.ez-status-err .ez-status-dot {
   background: var(--rose);
   box-shadow: 0 0 8px var(--rose);
}

/* TAB CONTENT NAVIGATION HEADER styling */
.stTabs [data-baseweb="tab-list"] {
   background: var(--bg-surface) !important;
   border: 1px solid var(--border-soft) !important;
   border-radius: var(--radius-lg) !important;
   padding: 6px !important;
   gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
   background: transparent !important;
   border: none !important;
   border-radius: var(--radius-md) !important;
   color: var(--text-muted) !important;
   font-size: 0.85rem !important;
   font-weight: 600 !important;
   padding: 0.6rem 1rem !important;
}
.stTabs [aria-selected="true"] {
   background: var(--grad-brand) !important;
   color: #FFFFFF !important;
   box-shadow: 0 4px 12px rgba(59,130,246,0.25) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* MARKETING HERO CONTAINER */
.hero-box {
   text-align: center;
   padding: 2rem 0.5rem 1rem;
}
.hero-badge {
   display: inline-block;
   background: rgba(59,130,246,0.08);
   border: 1px solid rgba(59,130,246,0.18);
   color: #60A5FA;
   font-size: 0.7rem;
   font-weight: 700;
   text-transform: uppercase;
   letter-spacing: 0.08em;
   padding: 0.35rem 0.85rem;
   border-radius: 30px;
   margin-bottom: 1rem;
}
.hero-title {
   font-family: 'Space Grotesk', sans-serif;
   font-size: 2.1rem;
   font-weight: 700;
   line-height: 1.2;
   color: var(--text-primary) !important;
   letter-spacing: -0.03em;
   margin-bottom: 0.75rem;
}
.hero-title span {
   background: var(--grad-brand);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
}
.hero-subtitle {
   font-size: 0.95rem;
   color: var(--text-secondary);
   line-height: 1.6;
   margin-bottom: 2rem;
}

/* HUB FEATURE CARDS */
.feat-card {
   background: var(--bg-card);
   border: 1px solid var(--border-soft);
   border-radius: var(--radius-lg);
   padding: 1.25rem;
   margin-bottom: 0.75rem;
   display: flex;
   align-items: flex-start;
   gap: 1rem;
}
.feat-icon {
   width: 42px;
   height: 42px;
   background: var(--bg-elevated);
   border-radius: var(--radius-md);
   display: flex;
   align-items: center;
   justify-content: center;
   font-size: 1.2rem;
   flex-shrink: 0;
}
.feat-title {
   font-size: 1rem;
   font-weight: 600;
   color: var(--text-primary) !important;
   margin-bottom: 0.25rem;
}
.feat-desc {
   font-size: 0.825rem;
   color: var(--text-muted);
   line-height: 1.45;
}

/* CONTENT CONTAINER SPECIFICS */
.sec-title {
   font-family: 'Space Grotesk', sans-serif;
   font-size: 1.4rem;
   font-weight: 700;
   color: var(--text-primary) !important;
   margin-top: 1rem;
   margin-bottom: 0.25rem;
}
.sec-desc {
   font-size: 0.85rem;
   color: var(--text-muted);
   margin-bottom: 1.5rem;
}

/* CHAT ROW INTERFACES */
.chat-row-user {
   display: flex;
   justify-content: flex-end;
   margin-bottom: 1rem;
}
.chat-bubble-user {
   background: var(--grad-brand);
   color: #FFFFFF !important;
   padding: 0.75rem 1rem;
   border-radius: 16px 16px 4px 16px;
   font-size: 0.9rem;
   line-height: 1.5;
   max-width: 85%;
   box-shadow: 0 4px 12px rgba(59,130,246,0.15);
}
.chat-row-ai {
   display: flex;
   justify-content: flex-start;
   gap: 0.6rem;
   margin-bottom: 1rem;
}
.chat-avatar {
   width: 28px;
   height: 28px;
   background: var(--grad-brand);
   border-radius: 8px;
   display: flex;
   align-items: center;
   justify-content: center;
   font-size: 0.85rem;
   flex-shrink: 0;
}
.chat-bubble-ai {
   background: var(--bg-card);
   border: 1px solid var(--border-soft);
   padding: 1rem;
   border-radius: 4px 16px 16px 16px;
   font-size: 0.9rem;
   line-height: 1.6;
   color: var(--text-primary) !important;
}

/* CONTAINER RESULT BLOCKS */
.result-card {
   background: var(--bg-card);
   border: 1px solid var(--border-soft);
   border-radius: var(--radius-lg);
   padding: 1.25rem;
   margin-top: 1.25rem;
}
.result-tag {
   font-size: 0.7rem;
   font-weight: 700;
   text-transform: uppercase;
   letter-spacing: 0.05em;
   color: var(--emerald);
   margin-bottom: 0.75rem;
   display: flex;
   align-items: center;
   gap: 0.4rem;
}
.result-tag-dot {
   width: 6px;
   height: 6px;
   background: var(--emerald);
   border-radius: 50%;
}

/* SELECTION OVERRIDES FOR INPUT PACKAGES */
.stTextArea textarea, .stTextInput input, .stSelectbox [data-baseweb="select"] {
   background-color: var(--bg-input) !important;
   border: 1px solid var(--border-soft) !important;
   color: var(--text-primary) !important;
   border-radius: var(--radius-md) !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
   border-color: var(--brand-primary) !important;
   box-shadow: 0 0 0 1px var(--brand-primary) !important;
}

/* INTERACTIVE BUTTON OVERRIDES */
.stButton > button {
   background: var(--grad-brand) !important;
   color: #FFFFFF !important;
   border: none !important;
   font-weight: 600 !important;
   font-size: 0.9rem !important;
   padding: 0.6rem 1.2rem !important;
   border-radius: var(--radius-md) !important;
   width: 100% !important;
   transition: all 0.2s ease;
}
.stButton > button:hover {
   transform: translateY(-1px);
   box-shadow: 0 4px 12px rgba(59,130,246,0.3);
}

/* ERROR HANDLING BADGES */
.panel-err {
   background: rgba(244,63,94,0.05);
   border: 1px solid rgba(244,63,94,0.15);
   border-radius: var(--radius-md);
   padding: 0.85rem 1rem;
   color: #FDA4AF;
   font-size: 0.85rem;
   margin: 1rem 0;
}
.panel-quota {
   background: rgba(245,158,11,0.05);
   border: 1px solid rgba(245,158,11,0.15);
   border-radius: var(--radius-md);
   padding: 1rem;
   color: #FDE047;
   font-size: 0.85rem;
   margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SECURE RE-USABLE GEMINI COMPONENT API CALL HANDLING
# ==============================================================================
@st.cache_resource(show_spinner=False)
def initialize_gemini_client():
   """Extract credentials dynamically across deployment contexts."""
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
       genai.configure(api_key=api_key)
       return genai
   except Exception:
       return None

def execute_model_query(client, prompt: str, system_context: str) -> dict:
   """Dispatches strings safely using the gemini-2.0-flash endpoint framework."""
   try:
       response = client.models.generate_content(
           model="gemini-2.0-flash",
           contents=prompt,
           config=types.GenerateContentConfig(
               system_instruction=system_context,
               temperature=0.6,
               max_output_tokens=1800,
           ),
       )
       return {"status": "success", "text": response.text}
   except Exception as e:
       error_msg = str(e)
       if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
           return {"status": "quota_limit"}
       return {"status": "failed", "message": error_msg[:150]}

def display_response_output(payload: dict):
   """Outputs text formats elegantly over isolated design components."""
   if payload["status"] == "success":
       st.markdown(f"""
       <div class="result-card">
           <div class="result-tag"><div class="result-tag-dot"></div>Analysis Output</div>
       """, unsafe_allow_html=True)
       st.markdown(payload["text"])
       st.markdown("</div>", unsafe_allow_html=True)
   elif payload["status"] == "quota_limit":
       st.markdown("""
       <div class="panel-quota">
           <strong>Engine Rate-Limit Encountered</strong><br>
           You have triggered the basic public cloud query quota boundary. Please wait ~60 seconds before trying your next compilation request.
       </div>
       """, unsafe_allow_html=True)
   else:
       st.markdown(f"""
       <div class="panel-err">
           <strong>Execution Interrupt:</strong> {payload.get('message', 'Process exception error')}
       </div>
       """, unsafe_allow_html=True)

# ==============================================================================
# 4. STRUCTURED SYSTEM TRAINING PROMPTS
# ==============================================================================
MENTOR_CORE_TRAINING = """You are Arya, an expert JEE/NEET counselor with 15+ years of institutional coaching tenure.
FORMAT EXPECTATION:
1. **Physical/Real-world Analogy** (Bold header)
2. **Core Conceptual Core Theory**
3. **Mathematical Derivations / Essential Equations**
4. **Common Exam Trap Mistakes**
5. **Pro-Tip Scoring Blueprint**
Maintain an encouraging and authoritative tone. Limit answers strictly to competitive STEM parameters."""

CORRECTIFY_CORE_TRAINING = """You are CorrectifyAI, an analytical diagnostic assistant scanning student problem mistakes.
Provide the following structural output exactly:
### 🚨 Detected Mistake Root
### 🔬 Scientific Breakdown
### ⚡ The Accurate Solution Method
### 📚 Key Topics to Revise"""

PLANNER_CORE_TRAINING = """You are PlannerAI, a time management engine optimization framework utilizing spaced repetition schedules for competitive exam prep. Generate structured, actionable revision schedules.
OUTPUT FORMAT:
### 📅 7-Day Revision Blueprint
### ⚡ Daily Breakdown Schedule
### 🎯 Priority Weak Topics Allocation
### 💪 Maintenance Strong Topics Routine
Focus on realistic, implementable study schedules with optimal spacing intervals."""

# ==============================================================================
# 5. VOLATILE SESSION MEMORY REPOSITORIES
# ==============================================================================
if "chat_history" not in st.session_state:
   st.session_state.chat_history = []

# ==============================================================================
# 6. APP BRAND HEADER BANNER NAVIGATION
# ==============================================================================
api_client = initialize_gemini_client()

if api_client:
   badge_element = "<div class='ez-status'><span class='ez-status-dot'></span>AI Core Online</div>"
else:
   badge_element = "<div class='ez-status ez-status-err'><span class='ez-status-dot'></span>No Credentials Found</div>"

st.markdown(f"""
<div class='ez-header'>
   <div class='ez-logo'>
       <div class='ez-logo-icon'>🎓</div>
       <div class='ez-logo-text'>Exam<span>Zen</span></div>
   </div>
   {badge_element}
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. ROUTING MAIN CONTROLLER ARCHITECTURE INTERFACE
# ==============================================================================
tab_dashboard, tab_mentor_bot, tab_correct_bot, tab_plan_bot = st.tabs(["Hub", "Mentor Chat", "Correctify AI", "Revision Planner"])

# --- TAB FRAMEWORK 1: HUB OVERVIEW ---
with tab_dashboard:
   st.markdown("""
   <div class="hero-box">
       <div class="hero-badge">JEE & NEET Engine v3.0</div>
       <div class="hero-title">Prepare Strategic. <span>Rank Supreme.</span></div>
       <div class="hero-subtitle">Access predictive mentorship frameworks designed to rapidly accelerate foundational test scores.</div>
   </div>
   
   <div class="feat-card">
       <div class="feat-icon">💡</div>
       <div>
           <div class="feat-title">Arya Mentor Chat</div>
           <div class="feat-desc">Receive conceptual theory breakdowns mapping real-world physical analogies to equations.</div>
       </div>
   </div>
   
   <div class="feat-card">
       <div class="feat-icon">🎯</div>
       <div>
           <div class="feat-title">Correctify Diagnosis Engine</div>
           <div class="feat-desc">Input calculation errors to isolate process vulnerabilities instantly.</div>
       </div>
   </div>
   
   <div class="feat-card">
       <div class="feat-icon">📅</div>
       <div>
           <div class="feat-title">Strategic Spaced Planner</div>
           <div class="feat-desc">Generate rigorous seven-day calendar schedules balancing high-weight domains.</div>
       </div>
   </div>
   """, unsafe_allow_html=True)
   
   if not api_client:
       st.markdown("""
       <div class="panel-err" style="text-align: center;">
           <strong>Missing Security Parameters:</strong> Please register your <code>GEMINI_API_KEY</code> variable inside your Streamlit Community Dashboard Secrets console to authorize engine deployment.
       </div>
       """, unsafe_allow_html=True)

# --- TAB FRAMEWORK 2: CHAT ENGINE SYSTEM ---
with tab_mentor_bot:
   st.markdown("""
   <div class="sec-title">Arya Core Mentorship</div>
   <div class="sec-desc">Ask questions about formulas, mechanisms, or theorems across Physics, Chemistry, Math, and Biology.</div>
   """, unsafe_allow_html=True)
   
   if not api_client:
       st.info("Unlock this feature by mapping an active engine credential in the cloud dashboard settings.")
   else:
       for chat_node in st.session_state.chat_history:
           if chat_node["user_type"] == "student":
               st.markdown(f'<div class="chat-row-user"><div class="chat-bubble-user">{chat_node["msg"]}</div></div>', unsafe_allow_html=True)
           else:
               st.markdown('<div class="chat-row-ai"><div class="chat-avatar">🤖</div><div class="chat-bubble-ai">', unsafe_allow_html=True)
               st.markdown(chat_node["msg"])
               st.markdown('</div></div>', unsafe_allow_html=True)
       
       chat_query = st.chat_input("Ask Arya to explain a complex topic...")
       if chat_query:
           clean_query = chat_query.strip()
           if len(clean_query) > 1:
               st.session_state.chat_history.append({"user_type": "student", "msg": clean_query})
               with st.spinner("Arya formatting conceptual model..."):
                   query_output = execute_model_query(api_client, clean_query, MENTOR_CORE_TRAINING)
                   if query_output["status"] == "success":
                       st.session_state.chat_history.append({"user_type": "mentor", "msg": query_output["text"]})
                       st.rerun()
                   else:
                       display_response_output(query_output)
                       
       if st.session_state.chat_history:
           st.markdown("<br>", unsafe_allow_html=True)
           if st.button("Reset Conversation Matrix", key="reset_chat_btn"):
               st.session_state.chat_history = []
               st.rerun()

# --- TAB FRAMEWORK 3: DIAGNOSTIC CORRECTIFY ENGINE ---
with tab_correct_bot:
   st.markdown("""
   <div class="sec-title">Correctify AI Error Analysis</div>
   <div class="sec-desc">Deconstruct exactly where your logic broke down to permanently resolve mathematical or conceptual mistakes.</div>
   """, unsafe_allow_html=True)
   
   if not api_client:
       st.info("Unlock this feature by mapping an active engine credential in the cloud dashboard settings.")
   else:
       subject_category = st.selectbox("Academic Vertical Domain", ["Physics Mechanics/Modern", "Chemistry Organic/Inorganic/Physical", "Mathematics Calculus/Algebra/Coordinate", "Biology Botany/Zoology"])
       question_prompt = st.text_area("Question Stem Blueprint Context", placeholder="Paste the problem description context here...", height=70)
       faulty_logic = st.text_area("Your Step-by-Step Draft Work (Required)", placeholder="Describe exactly what you calculated or your logic chain...", height=110)
       
       if st.button("Isolate Computational Vulnerabilities", key="run_diagnostic_btn"):
           if not faulty_logic.strip():
               st.error("Please fill out the step-by-step draft work box to isolate process steps.")
           else:
               compiled_payload = f"Subject Domain: {subject_category}\nQuestion Context: {question_prompt}\nStudent Attempt Track: {faulty_logic}"
               with st.spinner("Running process logic diagnostic checks..."):
                   diagnostic_report = execute_model_query(api_client, compiled_payload, CORRECTIFY_CORE_TRAINING)
                   display_response_output(diagnostic_report)

# --- TAB FRAMEWORK 4: TIMETABLE PLANNER ARCHITECTURE ---
with tab_plan_bot:
   st.markdown("""
   <div class="sec-title">Spaced Revision Calendar Matrix</div>
   <div class="sec-desc">Build customized study routines configured against weak chapters and high-yield topics.</div>
   """, unsafe_allow_html=True)
   
   if not api_client:
       st.info("Unlock this feature by mapping an active engine credential in the cloud dashboard settings.")
   else:
       target_exam_tier = st.selectbox("Target Core Milestone Goal", ["JEE Main Strategy Focus", "JEE Advanced Multi-Concept", "NEET UG Velocity Accuracy"])
       lagging_chapters = st.text_area("Vulnerable Core Topics needing Optimization", placeholder="e.g., Rotation Dynamics, Ionic Equilibrium, Integration...")
       proficient_chapters = st.text_area("Proficient Target Maintenance Systems", placeholder="e.g., Electrostatics, Mole Concept, Vectors...")
       daily_session_duration = st.select_slider("Target Allocated Active Daily Prep Windows (Hours)", options=[4, 6, 8, 10, 12], value=8)
       
       if st.button("Build Balanced Calendar Roadmap", key="run_planner_btn"):
           if not lagging_chapters.strip():
               st.error("Please add vulnerable focus areas to map out scheduling constraints.")
           else:
               planner_payload = f"Milestone Tier: {target_exam_tier}\nWeak Focus Priorities: {lagging_chapters}\nStrong Maintenance Chapters: {proficient_chapters}\nAvailable Daily Allocation: {daily_session_duration} hours"
               with st.spinner("Processing optimization routine paths..."):
                   planner_report = execute_model_query(api_client, planner_payload, PLANNER_CORE_TRAINING)
                   display_response_output(planner_report)
                   if planner_report["status"] == "success":
                       st.download_button(
                           label="Export Routine Blueprint File (.txt)",
                           data=planner_report["text"],
                           file_name="examzen_revision_routine.txt",
                           mime="text/plain"
                       )

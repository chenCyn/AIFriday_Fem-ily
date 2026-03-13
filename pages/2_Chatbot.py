import streamlit as st
from src.core.api import get_conversation_chain
from src.core.backend import risk_assessment
from src.db.db import add_patient_record
from src.ui.styles import inject_styles, render_topbar, render_sidebar

st.set_page_config(page_title="Fem♥ily · AI Chat", page_icon="🌸", layout="wide")
inject_styles()

# ─── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("Home.py")
if st.session_state.get("role") != "patient":
    st.error("Access denied. This page is for patients only.")
    st.stop()

render_sidebar()
render_topbar()

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:1.5rem">
    <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;color:#3d1f2e">💬 Fem♥ily AI</div>
    <div style="font-size:0.8rem;color:#9e7a88;letter-spacing:0.1em;text-transform:uppercase">Your maternal health companion</div>
</div>
<div style="background:linear-gradient(135deg,rgba(252,228,214,0.5),rgba(245,221,232,0.4));
     border:1px solid rgba(196,96,122,0.15);border-radius:14px;padding:0.85rem 1.25rem;
     font-size:0.83rem;color:#7a3048;margin-bottom:1.25rem">
    🌸 Describe your symptoms or ask any pregnancy-related question. I'll assess your risk level and guide you.
</div>
""", unsafe_allow_html=True)

# ─── Setup chain ───────────────────────────────────────────────────────────────
db = st.session_state.get("db")
user_id = st.session_state.get("user_id")
qa_chain = get_conversation_chain(db, user_id=user_id, role="patient")

# ─── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    name = st.session_state.get("user_profile", {}).get("metadata", {}).get("name", "Mama")
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Hello {name}! 🌸 I'm your Fem♥ily AI assistant. How are you feeling today? Tell me about any symptoms or questions you have.",
        "risk": None
    })

# ─── Display messages ──────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Show risk badge if present
        if msg.get("risk") and msg["role"] == "assistant":
            risk = msg["risk"]
            risk_class = f"risk-{risk.lower()}" if risk in ["Low", "Moderate", "High"] else "risk-low"
            action = msg.get("action", "")
            st.markdown(f'<span class="{risk_class}">{risk} Risk</span> <span style="font-size:0.78rem;color:#9e7a88;margin-left:0.5rem">{action}</span>', unsafe_allow_html=True)
        st.markdown(msg["content"])

# ─── Input ────────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Describe your symptoms or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": user_input, "risk": None})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🌸 Thinking..."):
            try:
                pregnancy_week = st.session_state.get("user_profile", {}).get("metadata", {}).get("pregnancy_week", 30)
                risk_level, action = risk_assessment(user_input, pregnancy_week=pregnancy_week)

                res = qa_chain.invoke(user_input)
                ai_answer = res.get("result", "I'm sorry, I couldn't process that. Please try again.")

                risk_class = f"risk-{risk_level.lower()}" if risk_level in ["Low", "Moderate", "High"] else "risk-low"
                st.markdown(f'<span class="{risk_class}">{risk_level} Risk</span> <span style="font-size:0.78rem;color:#9e7a88;margin-left:0.5rem">{action}</span>', unsafe_allow_html=True)
                st.markdown(ai_answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_answer,
                    "risk": risk_level,
                    "action": action
                })

                # Save to DB
                add_patient_record(db, user_id, user_input, {"risk_level": risk_level, "action": action})

                # Alert for high risk
                if risk_level == "High":
                    st.markdown('<div class="alert-banner alert-error">🚨 High risk detected. Please consider using the Emergency page or contacting your healthcare provider immediately.</div>', unsafe_allow_html=True)
                    if st.button("🚨 Go to Emergency Page"):
                        st.switch_page("pages/4_Emergency.py")

            except Exception as e:
                err_msg = "I'm having trouble connecting to the AI model. Please check that Ollama is running and try again."
                st.markdown(f'<div class="alert-banner alert-error">⚠️ {err_msg}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": err_msg, "risk": None})

# ─── Clear button ──────────────────────────────────────────────────────────────
if len(st.session_state.messages) > 1:
    st.markdown('<div style="margin-top:0.5rem"></div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c4a0ac;font-size:0.75rem;letter-spacing:0.1em">🌸 Always consult your healthcare provider · AI responses are not medical advice</div>', unsafe_allow_html=True)

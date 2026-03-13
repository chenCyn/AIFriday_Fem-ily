"""Shared Femily UI styles used across all pages."""

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] { background: #fdf6f0 !important; font-family: 'DM Sans', sans-serif; }
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #fce4d6 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, #f5dde8 0%, transparent 50%), #fdf6f0 !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
.main .block-container { background: transparent !important; padding-top: 1rem !important; }
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Typography ── */
.logo { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 300; color: #3d1f2e; text-align: center; letter-spacing: -0.01em; padding-top: 0.3rem; }
.logo .heart { color: #c4607a; }
.page-title { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; color: #3d1f2e; margin: 0 0 0.25rem; }
.page-sub { font-size: 0.8rem; color: #9e7a88; letter-spacing: 0.15em; text-transform: uppercase; }

/* ── Layout ── */
.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(196,96,122,0.18), transparent); margin: 0.75rem 0 1rem; }

/* ── Cards ── */
.card { background: rgba(255,255,255,0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.95); border-radius: 20px; padding: 1.75rem; box-shadow: 0 4px 24px rgba(180,100,120,0.08); margin-bottom: 1.25rem; }
.card-title { font-family: 'Cormorant Garamond', serif; font-size: 1.3rem; font-weight: 400; color: #3d1f2e; margin: 0 0 1.25rem 0; }

/* ── Buttons ── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #e8a0b0, #c4607a) !important;
    color: white !important; border: none !important; border-radius: 999px !important;
    padding: 0.6rem 2rem !important; font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    box-shadow: 0 4px 16px rgba(196,96,122,0.3) !important;
}

/* ── Form labels ── */
[data-testid="stTextInput"] label, [data-testid="stDateInput"] label,
[data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label,
[data-testid="stTextArea"] label, [data-testid="stTimeInput"] label {
    font-size: 0.72rem !important; color: #9e7a88 !important;
    text-transform: uppercase !important; letter-spacing: 0.12em !important; font-weight: 500 !important;
}
[data-testid="stTextInput"] input, [data-testid="stDateInput"] input {
    border-radius: 12px !important; border-color: #f0d0d8 !important;
    background: rgba(255,255,255,0.9) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.7) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(196,96,122,0.1) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stChatInput"] textarea {
    border-radius: 16px !important;
    border-color: rgba(196,96,122,0.3) !important;
    background: rgba(255,255,255,0.9) !important;
}

/* ── Alerts ── */
.alert-banner {
    border-radius: 14px; padding: 1rem 1.25rem;
    font-size: 0.88rem; margin-bottom: 1rem;
}
.alert-info { background: rgba(252,228,214,0.5); border: 1px solid rgba(196,96,122,0.2); color: #7a3048; }
.alert-error { background: rgba(255,220,220,0.6); border: 1px solid rgba(200,60,60,0.25); color: #8b1a1a; }
.alert-success { background: rgba(220,245,220,0.6); border: 1px solid rgba(60,180,60,0.2); color: #1a5c1a; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(253,246,240,0.95) !important;
    border-right: 1px solid rgba(196,96,122,0.12) !important;
}
[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.6) !important;
    color: #3d1f2e !important;
    box-shadow: none !important;
    border: 1px solid rgba(196,96,122,0.2) !important;
    width: 100% !important;
    margin-bottom: 0.25rem !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(135deg, #fce4d6, #f5dde8) !important;
    color: #c4607a !important;
}

/* ── Stat boxes ── */
.stat-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.25rem; }
.stat-box { background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(252,228,214,0.4)); border: 1px solid rgba(255,255,255,0.9); border-radius: 16px; padding: 1.25rem; text-align: center; }
.stat-num { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 300; color: #c4607a; line-height: 1; }
.stat-label { font-size: 0.7rem; color: #9e7a88; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 0.25rem; }

/* ── Risk badges ── */
.risk-low { background: #e8f5e9; color: #2e7d32; border-radius: 999px; padding: 0.2rem 0.75rem; font-size: 0.75rem; font-weight: 600; }
.risk-moderate { background: #fff3e0; color: #e65100; border-radius: 999px; padding: 0.2rem 0.75rem; font-size: 0.75rem; font-weight: 600; }
.risk-high { background: #ffebee; color: #c62828; border-radius: 999px; padding: 0.2rem 0.75rem; font-size: 0.75rem; font-weight: 600; }

/* ── Record items ── */
.record-item { background: rgba(255,255,255,0.8); border: 1px solid rgba(196,96,122,0.1); border-radius: 14px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; }
</style>
"""

SIDEBAR_NAV_CSS = """
<style>
[data-testid="stSidebarNav"] { display: none; }
</style>
"""

def inject_styles():
    import streamlit as st
    st.markdown(BASE_CSS + SIDEBAR_NAV_CSS, unsafe_allow_html=True)

def render_topbar(show_back_home: bool = True):
    """Render the Femily logo top bar."""
    import streamlit as st
    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c1:
        if show_back_home:
            if st.button("← Home"):
                st.switch_page("Home.py")
    with c2:
        st.markdown('<div class="logo">Fem<span class="heart">♥</span>ily</div>', unsafe_allow_html=True)
    with c3:
        pass
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

def render_sidebar():
    """Render role-aware sidebar navigation."""
    import streamlit as st

    profile = st.session_state.get("user_profile")
    role = st.session_state.get("role")

    if not profile:
        return

    with st.sidebar:
        meta = profile["metadata"]
        initials = meta.get("name", "U")[0].upper()
        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0 0.5rem">
            <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#e8a0b0,#c4607a);
                display:flex;align-items:center;justify-content:center;font-size:1.5rem;
                margin:0 auto 0.75rem;box-shadow:0 4px 16px rgba(196,96,122,0.3);border:3px solid white;color:white;font-weight:600">
                {initials}
            </div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#3d1f2e">{meta.get('name','User')}</div>
            <div style="font-size:0.7rem;color:#9e7a88;text-transform:uppercase;letter-spacing:0.12em">{role}</div>
        </div>
        <div style="height:1px;background:rgba(196,96,122,0.15);margin:0.5rem 0 1rem"></div>
        """, unsafe_allow_html=True)

        st.markdown("**Navigate**")
        if role == "patient":
            if st.button("🏠 Home"):
                st.switch_page("Home.py")
            if st.button("💬 AI Chatbot"):
                st.switch_page("pages/2_Chatbot.py")
            if st.button("📅 Calendar"):
                st.switch_page("pages/1_Calendar.py")
            if st.button("👤 Profile"):
                st.switch_page("pages/0_Profile.py")
            if st.button("🚨 Emergency"):
                st.switch_page("pages/4_Emergency.py")
        elif role == "volunteer":
            if st.button("🏠 Home"):
                st.switch_page("Home.py")
            if st.button("👩‍⚕️ Volunteer Dashboard"):
                st.switch_page("pages/3_Volunteer.py")

        st.markdown('<div style="height:1px;background:rgba(196,96,122,0.15);margin:0.75rem 0"></div>', unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            for k in ["logged_in", "user_id", "user_profile", "role", "db", "messages"]:
                st.session_state.pop(k, None)
            st.rerun()

import streamlit as st
from datetime import date, timedelta
from src.db.db import get_user_records
from src.ui.styles import inject_styles, render_topbar, render_sidebar

st.set_page_config(page_title="Fem♥ily · Profile", page_icon="🌸", layout="wide")
inject_styles()

# ─── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("Home.py")
if st.session_state.get("role") != "patient":
    st.error("Access denied. This page is for patients only.")
    st.stop()

render_sidebar()
render_topbar()

# ─── Session defaults ──────────────────────────────────────────────────────────
for key, val in [
    ("mama_name", "Mama"), ("lmp", date.today() - timedelta(weeks=16)),
    ("pre_weight", 60.0), ("language", "🇬🇧 English"),
    ("blood_type", ""), ("doctor_name", ""), ("hospital", ""),
    ("emergency_contact", ""), ("allergies", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Calculations ──────────────────────────────────────────────────────────────
today = date.today()
lmp = st.session_state.lmp
weeks = max(0, (today - lmp).days // 7)
due_date = lmp + timedelta(days=280)
days_left = (due_date - today).days
trimester = 1 if weeks < 13 else (2 if weeks < 27 else 3)

# ─── NGO data ─────────────────────────────────────────────────────────────────
db = st.session_state.get("db")
user_id = st.session_state.get("user_id")
ngo_profile = st.session_state.get("user_profile", {})
ngo_meta = ngo_profile.get("metadata", {})

# Sync pregnancy week from NGO profile if available
if ngo_meta.get("pregnancy_week") and weeks == 0:
    pw = ngo_meta["pregnancy_week"]
    st.session_state.lmp = date.today() - timedelta(weeks=pw)
    weeks = pw

# ─── Avatar + Name ────────────────────────────────────────────────────────────
initials = st.session_state.mama_name[0].upper() if st.session_state.mama_name else "M"
st.markdown(f"""
<div style="text-align:center;padding:0.5rem 0 1.5rem">
    <div style="width:90px;height:90px;border-radius:50%;background:linear-gradient(135deg,#e8a0b0,#c4607a);
         display:flex;align-items:center;justify-content:center;font-size:2.5rem;
         margin:0 auto 1rem;box-shadow:0 8px 24px rgba(196,96,122,0.3);border:4px solid white;color:white;font-weight:300">
        {initials}
    </div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:300;color:#3d1f2e">{st.session_state.mama_name}</div>
    <div style="font-size:0.82rem;color:#9e7a88;letter-spacing:0.15em;text-transform:uppercase;margin-top:0.3rem">
        Week {weeks} · Trimester {trimester} · Due {due_date.strftime('%B %d, %Y')}
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Stats row ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
    <div class="stat-box"><div class="stat-num">{weeks}</div><div class="stat-label">Weeks Pregnant</div></div>
    <div class="stat-box"><div class="stat-num">{days_left}</div><div class="stat-label">Days to Go</div></div>
    <div class="stat-box"><div class="stat-num">{trimester}</div><div class="stat-label">Trimester</div></div>
</div>
""", unsafe_allow_html=True)

# ─── Edit Form ────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.markdown('<div class="card"><div class="card-title">🌸 Personal Details</div>', unsafe_allow_html=True)
    new_name = st.text_input("Your Name", value=st.session_state.mama_name)
    new_lmp = st.date_input("Last Menstrual Period", value=st.session_state.lmp,
                             min_value=date.today() - timedelta(weeks=42), max_value=date.today())
    new_weight = st.number_input("Pre-pregnancy Weight (kg)", min_value=30.0, max_value=200.0,
                                  value=float(st.session_state.pre_weight), step=0.5)
    LANGUAGES = ["🇬🇧 English", "🇮🇳 हिंदी", "🇮🇳 தமிழ்", "🇨🇳 中文"]
    lang_idx = LANGUAGES.index(st.session_state.language) if st.session_state.language in LANGUAGES else 0
    new_lang = st.selectbox("Preferred Language", LANGUAGES, index=lang_idx)
    BLOOD_TYPES = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    bt_idx = BLOOD_TYPES.index(st.session_state.blood_type) if st.session_state.blood_type in BLOOD_TYPES else 0
    new_blood = st.selectbox("Blood Type", BLOOD_TYPES, index=bt_idx)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card"><div class="card-title">🏥 Medical Details</div>', unsafe_allow_html=True)
    new_doctor = st.text_input("Doctor / Midwife Name", value=st.session_state.doctor_name, placeholder="Dr. Name")
    new_hospital = st.text_input("Hospital / Clinic", value=st.session_state.hospital, placeholder="Hospital name")
    new_emergency = st.text_input("Emergency Contact", value=st.session_state.emergency_contact, placeholder="Name & phone number")
    new_allergies = st.text_area("Allergies / Medical Notes", value=st.session_state.allergies,
                                  placeholder="Any allergies or important medical info...", height=108)

    # NGO location info (read-only)
    if ngo_meta.get("location"):
        st.markdown(f'<div style="font-size:0.72rem;color:#9e7a88;text-transform:uppercase;letter-spacing:0.12em;font-weight:500;margin-top:0.5rem">Location (from record)</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.9rem;color:#3d1f2e;padding:0.4rem 0">{ngo_meta["location"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Save ─────────────────────────────────────────────────────────────────────
_, save_col, _ = st.columns([1, 1, 1])
with save_col:
    if st.button("Save Profile 🌸", use_container_width=True):
        st.session_state.mama_name = new_name
        st.session_state.lmp = new_lmp
        st.session_state.pre_weight = new_weight
        st.session_state.language = new_lang
        st.session_state.blood_type = new_blood
        st.session_state.doctor_name = new_doctor
        st.session_state.hospital = new_hospital
        st.session_state.emergency_contact = new_emergency
        st.session_state.allergies = new_allergies
        st.success("✅ Profile saved successfully!")
        st.rerun()

# ─── Health Records (from NGO DB) ─────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card-title" style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:#3d1f2e">📋 Recent Health Records</div>', unsafe_allow_html=True)

if db and user_id:
    records = get_user_records(db, user_id, k=5)
    if records:
        for r in records:
            meta = r["metadata"] if isinstance(r, dict) else r.metadata
            content = r["page_content"] if isinstance(r, dict) else r.page_content
            risk = meta.get("risk_level", "Unknown")
            risk_class = f"risk-{risk.lower()}" if risk in ["Low", "Moderate", "High"] else "risk-low"
            action = meta.get("action", "N/A")
            st.markdown(f"""
            <div class="record-item">
                <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.4rem">
                    <span class="{risk_class}">{risk} Risk</span>
                    <span style="font-size:0.78rem;color:#9e7a88">{action}</span>
                </div>
                <div style="font-size:0.88rem;color:#3d1f2e">{content}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-banner alert-info">No health records found yet. Use the AI Chatbot to log your first symptoms.</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c4a0ac;font-size:0.75rem;letter-spacing:0.1em">🌸 Always consult your healthcare provider</div>', unsafe_allow_html=True)

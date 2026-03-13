import streamlit as st
from src.db.db import search_patients
from src.ui.styles import inject_styles, render_topbar, render_sidebar

st.set_page_config(page_title="Fem♥ily · Volunteer", page_icon="🌸", layout="wide")
inject_styles()

# ─── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("Home.py")
if st.session_state.get("role") != "volunteer":
    st.error("Access denied. This page is for volunteers only.")
    st.stop()

render_sidebar()
render_topbar()

db = st.session_state.get("db")

# ─── Header ───────────────────────────────────────────────────────────────────
volunteer_name = st.session_state.get("user_profile", {}).get("metadata", {}).get("name", "Volunteer")
st.markdown(f"""
<div style="margin-bottom:1.5rem">
    <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;color:#3d1f2e">👩‍⚕️ Volunteer Dashboard</div>
    <div style="font-size:0.8rem;color:#9e7a88;letter-spacing:0.1em;text-transform:uppercase">Welcome, {volunteer_name}</div>
</div>
""", unsafe_allow_html=True)

# ─── Stats row ────────────────────────────────────────────────────────────────
try:
    all_records = db.get()
    total_patients = len(set(
        m.get("id", "") for m in all_records.get("metadatas", [])
        if m.get("role") == "patient"
    ))
    high_risk = sum(1 for m in all_records.get("metadatas", []) if m.get("risk_level") == "High")
    moderate_risk = sum(1 for m in all_records.get("metadatas", []) if m.get("risk_level") == "Moderate")
except:
    total_patients = high_risk = moderate_risk = 0

st.markdown(f"""
<div class="stat-row">
    <div class="stat-box"><div class="stat-num">{total_patients}</div><div class="stat-label">Patients</div></div>
    <div class="stat-box" style="background:linear-gradient(135deg,rgba(255,235,230,0.9),rgba(255,200,200,0.3))">
        <div class="stat-num" style="color:#c62828">{high_risk}</div><div class="stat-label">High Risk</div></div>
    <div class="stat-box" style="background:linear-gradient(135deg,rgba(255,248,225,0.9),rgba(255,220,100,0.2))">
        <div class="stat-num" style="color:#e65100">{moderate_risk}</div><div class="stat-label">Moderate Risk</div></div>
</div>
""", unsafe_allow_html=True)

# ─── Search ───────────────────────────────────────────────────────────────────
left, right = st.columns([2, 1])
with left:
    query = st.text_input("🔍 Search patient records", placeholder="e.g. headache, swelling, bleeding...")
with right:
    st.markdown('<div style="padding-top:1.6rem"></div>', unsafe_allow_html=True)
    search_clicked = st.button("Search Records 🌸")

if search_clicked and query:
    results = search_patients(db, query, k=8)
    if not results:
        st.markdown('<div class="alert-banner alert-info">No matching records found for that query.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.3rem;color:#3d1f2e;margin:1rem 0 0.75rem">Found {len(results)} record(s)</div>', unsafe_allow_html=True)
        for r in results:
            meta = r.metadata if hasattr(r, 'metadata') else {}
            content = r.page_content if hasattr(r, 'page_content') else str(r)
            risk = meta.get("risk_level", "Unknown")
            risk_class = f"risk-{risk.lower()}" if risk in ["Low", "Moderate", "High"] else "risk-low"
            action = meta.get("action", "N/A")
            patient_id = meta.get("id", "N/A")
            name = meta.get("name", "Anonymous")
            location = meta.get("location", "")
            preg_week = meta.get("pregnancy_week", "")

            with st.expander(f"{'🔴' if risk == 'High' else '🟡' if risk == 'Moderate' else '🟢'} Patient {patient_id} · {name}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Reported Symptoms:** {content}")
                    st.markdown(f"**Recommended Action:** {action}")
                with col2:
                    st.markdown(f'<span class="{risk_class}">{risk} Risk</span>', unsafe_allow_html=True)
                    if location: st.markdown(f"📍 {location}")
                    if preg_week: st.markdown(f"🤰 Week {preg_week}")

                # Action buttons
                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("📞 Mark as Contacted", key=f"contact_{patient_id}"):
                        st.success("Marked as contacted!")
                with btn2:
                    if risk == "High" and st.button("🚨 Escalate", key=f"escalate_{patient_id}"):
                        st.error("Case escalated to medical team!")

elif not search_clicked:
    # Recent high-risk cases
    st.markdown('<div class="card"><div class="card-title">🚨 Recent High-Risk Cases</div>', unsafe_allow_html=True)
    try:
        high_risk_results = search_patients(db, "headache swelling bleeding", k=5)
        shown = [r for r in high_risk_results if r.metadata.get("risk_level") == "High"]
        if shown:
            for r in shown:
                meta = r.metadata
                st.markdown(f"""
                <div class="record-item">
                    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.3rem">
                        <span class="risk-high">High Risk</span>
                        <span style="font-size:0.78rem;color:#9e7a88">{meta.get('action','')}</span>
                    </div>
                    <div style="font-size:0.88rem;color:#3d1f2e">{r.page_content}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:0.85rem;color:#9e7a88;padding:0.5rem 0">No high-risk cases found. Use the search above to find patients.</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="font-size:0.85rem;color:#9e7a88;padding:0.5rem 0">Use the search above to find patient records.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c4a0ac;font-size:0.75rem;letter-spacing:0.1em">🌸 Handle all patient data with care and confidentiality</div>', unsafe_allow_html=True)

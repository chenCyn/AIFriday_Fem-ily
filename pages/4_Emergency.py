import streamlit as st
import streamlit.components.v1 as components
from src.ui.styles import inject_styles, render_topbar, render_sidebar

st.set_page_config(page_title="Fem♥ily · Emergency", page_icon="🚨", layout="wide")
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
<div style="text-align:center;padding:0.5rem 0 2rem">
    <div style="font-size:3.5rem;margin-bottom:0.75rem">🚨</div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:300;color:#3d1f2e">Emergency Support</div>
    <div style="font-size:0.82rem;color:#9e7a88;letter-spacing:0.12em;text-transform:uppercase;margin-top:0.25rem">Immediate help when you need it most</div>
</div>
""", unsafe_allow_html=True)

# ─── CALL BUTTONS (rendered via components.html for reliable display) ─────────
components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  body { margin: 0; padding: 0; background: transparent; font-family: 'DM Sans', sans-serif; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding: 0.25rem; }
  .btn {
    display: flex; align-items: center; justify-content: center; gap: 0.75rem;
    padding: 1.1rem 1.5rem; border-radius: 16px; text-decoration: none;
    color: white; font-size: 1rem; font-weight: 600;
    transition: transform 0.15s, box-shadow 0.15s;
  }
  .btn:hover { transform: translateY(-2px); }
  .btn .emoji { font-size: 1.6rem; line-height: 1; }
  .btn .label { font-size: 1rem; font-weight: 600; line-height: 1.2; }
  .btn .sub   { font-size: 0.72rem; font-weight: 400; opacity: 0.85; margin-top: 2px; }

  .red1  { background: linear-gradient(135deg,#d32f2f,#b71c1c); box-shadow: 0 6px 20px rgba(211,47,47,0.45); }
  .red2  { background: linear-gradient(135deg,#e53935,#c62828); box-shadow: 0 6px 20px rgba(229,57,53,0.45); }
  .purple{ background: linear-gradient(135deg,#7b1fa2,#4a148c); box-shadow: 0 6px 20px rgba(123,31,162,0.4); }
  .pink  { background: linear-gradient(135deg,#c4607a,#8b3050); box-shadow: 0 6px 20px rgba(196,96,122,0.45); }
</style>
</head>
<body>
<div class="grid">

  <a href="tel:+6597807812" class="btn red1">
    <span class="emoji">🚨</span>
    <div><div class="label">Emergency Help</div><div class="sub">Tap to call now</div></div>
  </a>

  <a href="tel:+6581517232" class="btn red2">
    <span class="emoji">🚑</span>
    <div><div class="label">Call Ambulance</div><div class="sub">Tap to call now</div></div>
  </a>

  <a href="tel:+6589505915" class="btn purple">
    <span class="emoji">🧠</span>
    <div><div class="label">Suicide Prevention Lifeline</div><div class="sub">988 · Tap to call</div></div>
  </a>

  <a href="tel:+6587916396" class="btn pink">
    <span class="emoji">👩‍⚕️</span>
    <div><div class="label">Mid-Wife Service</div><div class="sub">Tap to call now</div></div>
  </a>

</div>
</body>
</html>
""", height=180)

# ─── Warning signs + advice ───────────────────────────────────────────────────
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="card"><div class="card-title">⚠️ Seek Immediate Care If You Have</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem">', unsafe_allow_html=True)
    for icon, title, desc in [
        ("🩸", "Heavy bleeding",    "More than a period"),
        ("👁️", "Blurred vision",    "With headache or swelling"),
        ("🤕", "Severe headache",   "Sudden or very intense"),
        ("💧", "Fluid leaking",     "Possible waters breaking"),
        ("🤰", "Abdominal pain",    "Severe cramping or pressure"),
        ("🦵", "Severe swelling",   "Hands, face, or feet"),
        ("💓", "Baby not moving",   "Decreased fetal movement"),
        ("🤒", "High fever",        "Above 38°C / 100.4°F"),
    ]:
        st.markdown(f"""
        <div style="background:rgba(255,235,230,0.5);border:1px solid rgba(200,60,60,0.12);
             border-radius:12px;padding:0.85rem;display:flex;align-items:flex-start;gap:0.6rem">
            <span style="font-size:1.3rem">{icon}</span>
            <div>
                <div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">{title}</div>
                <div style="font-size:0.72rem;color:#9e7a88;margin-top:0.1rem">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
        <div class="card-title">📋 While You Wait for Help</div>
        <div style="display:flex;flex-direction:column;gap:0.75rem">
            <div style="background:#fff3e0;border-radius:12px;padding:0.85rem 1rem;display:flex;align-items:flex-start;gap:0.75rem">
                <span style="font-size:1.3rem">🧘</span>
                <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Stay calm</div>
                <div style="font-size:0.75rem;color:#9e7a88">Sit or lie down comfortably. Breathe slowly and steadily.</div></div>
            </div>
            <div style="background:#e8f5e9;border-radius:12px;padding:0.85rem 1rem;display:flex;align-items:flex-start;gap:0.75rem">
                <span style="font-size:1.3rem">👥</span>
                <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Get someone with you</div>
                <div style="font-size:0.75rem;color:#9e7a88">Call a family member or neighbour to stay by your side.</div></div>
            </div>
            <div style="background:#e3f2fd;border-radius:12px;padding:0.85rem 1rem;display:flex;align-items:flex-start;gap:0.75rem">
                <span style="font-size:1.3rem">🏥</span>
                <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Note your address</div>
                <div style="font-size:0.75rem;color:#9e7a88">Be ready to tell the operator your exact location.</div></div>
            </div>
            <div style="background:#fce4d6;border-radius:12px;padding:0.85rem 1rem;display:flex;align-items:flex-start;gap:0.75rem">
                <span style="font-size:1.3rem">📋</span>
                <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Bring your maternity notes</div>
                <div style="font-size:0.75rem;color:#9e7a88">Bring your medical records or hospital card if possible.</div></div>
            </div>
            <div style="background:#f3e5f5;border-radius:12px;padding:0.85rem 1rem;display:flex;align-items:flex-start;gap:0.75rem">
                <span style="font-size:1.3rem">🚫</span>
                <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Do not eat or drink</div>
                <div style="font-size:0.75rem;color:#9e7a88">You may need emergency treatment — keep your stomach empty.</div></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">🌐 More Helplines</div>
        <div style="display:flex;flex-direction:column;gap:0.6rem">
            <div style="font-size:0.85rem;color:#3d1f2e">
                <span style="font-weight:500">Crisis Text Line</span>
                <span style="color:#9e7a88;margin-left:0.5rem">Text HOME to 741741</span>
            </div>
            <div style="font-size:0.85rem;color:#3d1f2e">
                <span style="font-weight:500">International Helplines</span>
                <span style="margin-left:0.5rem">
                    <a href="https://www.befrienders.org" target="_blank" style="color:#c4607a;text-decoration:none">befrienders.org</a>
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c4a0ac;font-size:0.75rem;letter-spacing:0.1em">🌸 In a life-threatening emergency, always call your local emergency number first</div>', unsafe_allow_html=True)

import streamlit as st
from datetime import date, timedelta
from src.db.db import init_db, get_user, load_users_from_csv
from src.ui.styles import inject_styles, render_sidebar

st.set_page_config(
    page_title="Fem♥ily · Home",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_styles()

# ─── Session defaults ──────────────────────────────────────────────────────────
for key, val in [
    ("logged_in", False), ("user_id", None), ("role", None),
    ("user_profile", None), ("db", None), ("users_loaded", False),
    ("language", "🇬🇧 English"), ("lmp", date.today() - timedelta(weeks=16)),
    ("mama_name", "Mama"), ("pre_weight", 60.0),
]:
    if key not in st.session_state:
        st.session_state[key] = val

if "appointments" not in st.session_state:
    st.session_state.appointments = [
        {"title": "20-Week Anatomy Scan", "date": date.today() + timedelta(days=5),
         "time": "10:00 AM", "type": "Scan", "doctor": "Dr. LOL", "notes": "", "reminder": True},
        {"title": "Routine Checkup", "date": date.today() + timedelta(days=14),
         "time": "2:30 PM", "type": "Checkup", "doctor": "Dr. Anita Mehta", "notes": "", "reminder": True},
    ]

# ─── Initialise DB ─────────────────────────────────────────────────────────────
if st.session_state.db is None:
    db = init_db()
    if not st.session_state.users_loaded:
        existing = db.get()
        if not existing or len(existing.get("ids", [])) == 0:
            try:
                load_users_from_csv(db)
            except FileNotFoundError:
                pass
        st.session_state.users_loaded = True
    st.session_state.db = db

# ─── LOGIN PAGE ────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown('<div style="text-align:center;padding:2rem 0 1rem"><div class="logo">Fem<span class="heart">♥</span>ily</div><div class="page-sub" style="margin-top:0.25rem">Maternal Health Companion</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        #st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="text-align:center">🔐 Welcome Back</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.82rem;color:#9e7a88;text-align:center;margin-bottom:1.25rem">Enter your patient or volunteer ID to continue</div>', unsafe_allow_html=True)

        user_id = st.text_input("Your ID", placeholder="e.g. p_001 or v_001")

        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            login_clicked = st.button("Login 🌸", use_container_width=True)

        if login_clicked:
            if user_id.strip():
                user = get_user(st.session_state.db, user_id.strip())
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id.strip()
                    st.session_state.user_profile = user
                    st.session_state.role = user["metadata"].get("role")
                    meta = user["metadata"]
                    if meta.get("name"):
                        st.session_state.mama_name = meta["name"]
                    if st.session_state.role == "patient":
                        st.rerun()
                    elif st.session_state.role == "volunteer":
                        st.switch_page("pages/3_Volunteer.py")
                    else:
                        st.markdown('<div class="alert-banner alert-error">⚠️ Unknown role. Contact your administrator.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-banner alert-error">❌ No account found with that ID. Please try again.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-banner alert-info">Please enter your ID.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;color:#c4a0ac;font-size:0.75rem;letter-spacing:0.1em;margin-top:1rem">🌸 Always consult your healthcare provider</div>', unsafe_allow_html=True)
    st.stop()

# ─── POST-LOGIN: show sidebar ─────────────────────────────────────────────────
render_sidebar()

# ─── Volunteer redirect ───────────────────────────────────────────────────────
if st.session_state.role == "volunteer":
    st.switch_page("pages/3_Volunteer.py")

# ─── PATIENT DASHBOARD ────────────────────────────────────────────────────────
LANGUAGES = {
    "🇬🇧 English": {"greeting": "Hello", "week_label": "WEEKS PREGNANT", "journey": "of journey complete",
                    "reminders_title": "Reminders & Checklist", "tip_title": "Fact of the Week",
                    "due_label": "Due", "days_left": "days to go", "trimester": "Trimester",
                    "no_appts": "No upcoming appointments. Add some in the Calendar! 🌸"},
    "🇮🇳 हिंदी": {"greeting": "नमस्ते", "week_label": "गर्भावस्था के सप्ताह", "journey": "यात्रा पूरी",
                  "reminders_title": "अनुस्मारक और सूची", "tip_title": "इस सप्ताह का तथ्य",
                  "due_label": "प्रसव तिथि", "days_left": "दिन बाकी", "trimester": "तिमाही",
                  "no_appts": "कोई नियुक्ति नहीं। कैलेंडर में जोड़ें! 🌸"},
    "🇮🇳 தமிழ்": {"greeting": "வணக்கம்", "week_label": "கர்ப்ப வாரங்கள்", "journey": "பயணம் முடிந்தது",
                  "reminders_title": "நினைவூட்டல்கள் & பட்டியல்", "tip_title": "இந்த வாரத்தின் உண்மை",
                  "due_label": "பிரசவ தேதி", "days_left": "நாட்கள் மீதம்", "trimester": "மூன்று மாதம்",
                  "no_appts": "நியமனங்கள் இல்லை. காலண்டரில் சேர்க்கவும்! 🌸"},
    "🇨🇳 中文": {"greeting": "你好", "week_label": "怀孕周数", "journey": "旅程已完成",
               "reminders_title": "提醒与清单", "tip_title": "本周小知识",
               "due_label": "预产期", "days_left": "天后", "trimester": "孕期",
               "no_appts": "没有即将到来的预约。在日历中添加！🌸"},
}

WEEKLY_TIPS = {
    "🇬🇧 English": {
        4: "Taking folic acid now helps prevent neural tube defects. Your baby's heart starts beating around week 5–6.",
        8: "Ginger tea and small frequent meals can ease morning sickness. Your baby is now the size of a raspberry.",
        12: "You've reached the end of your first trimester! The risk of miscarriage drops significantly after week 12.",
        16: "Your baby can now make facial expressions. Stay hydrated and eat iron-rich foods like lentils and spinach.",
        20: "Halfway there! Sleep on your left side to improve blood flow. Your baby weighs about 300g now.",
        24: "Your baby's lungs are developing. Avoid smoky environments and keep up with prenatal vitamins.",
        28: "Your baby can now hear your voice — talk and sing to them. Third trimester begins this week!",
        32: "Start preparing your hospital bag. Practice breathing exercises daily to prepare for labour.",
        36: "Your baby is considered early-term. Rest as much as possible and watch for signs of labour.",
        40: "You are full term! Trust your body. Your baby will arrive when ready. 🌸",
    },
}

HEALTH_REMINDERS = {
    1: [("💊", "Take folic acid daily", "Critical for baby's brain"),
        ("🚫", "Avoid alcohol & smoking", "Harmful at all stages"),
        ("🩺", "Book first antenatal visit", "Ideally before week 10")],
    2: [("🩻", "Schedule anatomy scan", "Between week 18–22"),
        ("🚶", "Stay gently active", "30 mins walking daily"),
        ("🧴", "Moisturise your skin", "Helps with stretching")],
    3: [("🎒", "Prepare hospital bag", "Ready by week 36"),
        ("🌬️", "Practice breathing", "Helps during labour"),
        ("😴", "Rest as much as possible", "Your body is working hard")],
}

# ─── Calculations ──────────────────────────────────────────────────────────────
today = date.today()
lmp = st.session_state.lmp
days_pregnant = (today - lmp).days
weeks = max(0, days_pregnant // 7)
due_date = lmp + timedelta(days=280)
days_left = (due_date - today).days
progress_pct = min(days_pregnant / 280 * 100, 100)
trimester = 1 if weeks < 13 else (2 if weeks < 27 else 3)
lang = st.session_state.language
T = LANGUAGES.get(lang, LANGUAGES["🇬🇧 English"])
tips = WEEKLY_TIPS.get(lang, WEEKLY_TIPS["🇬🇧 English"])
tip_week = max([w for w in tips.keys() if w <= max(weeks, 1)] or [list(tips.keys())[0]])
tip_text = tips[tip_week]

# ─── TOP BAR ──────────────────────────────────────────────────────────────────
left_col, mid_col, right_col = st.columns([1.2, 1, 1.2])
with left_col:
    sel = st.selectbox("", list(LANGUAGES.keys()),
                       index=list(LANGUAGES.keys()).index(lang),
                       label_visibility="collapsed")
    if sel != lang:
        st.session_state.language = sel
        st.rerun()
with mid_col:
    st.markdown('<div class="logo">Fem<span class="heart">♥</span>ily</div>', unsafe_allow_html=True)
with right_col:
    _, btn = st.columns([2, 1])
    with btn:
        if st.button("👤 Profile"):
            st.switch_page("pages/0_Profile.py")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─── WEEK HERO CARD ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#c4607a,#8b3050);border-radius:24px;padding:2rem 2.5rem;
     color:white;box-shadow:0 8px 32px rgba(196,96,122,0.35);margin-bottom:1.25rem;
     display:flex;align-items:center;gap:2rem">
    <div style="font-family:'Cormorant Garamond',serif;font-size:5.5rem;font-weight:300;line-height:1;flex-shrink:0">{weeks}</div>
    <div style="flex:1">
        <div style="font-size:0.78rem;letter-spacing:0.2em;text-transform:uppercase;opacity:0.8">{T['week_label']}</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-style:italic;opacity:0.9;margin:0.15rem 0">
            {T['trimester']} {trimester} &nbsp;·&nbsp; {T['greeting']}, {st.session_state.mama_name} 🌸
        </div>
        <div style="font-size:0.82rem;opacity:0.75;margin-top:0.25rem">
            {T['due_label']}: {due_date.strftime('%B %d, %Y')} &nbsp;·&nbsp; {days_left} {T['days_left']}
        </div>
        <div style="background:rgba(255,255,255,0.2);border-radius:999px;height:7px;margin-top:0.85rem">
            <div style="background:white;border-radius:999px;height:7px;width:{progress_pct:.1f}%"></div>
        </div>
        <div style="font-size:0.72rem;opacity:0.7;margin-top:0.3rem;letter-spacing:0.08em">{progress_pct:.0f}% {T['journey']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── QUICK ACTION TILES ───────────────────────────────────────────────────────
qa1, qa2, qa3, qa4 = st.columns(4)
tiles = [
    (qa1, "💬", "Ask AI", "pages/2_Chatbot.py"),
    (qa2, "📅", "Calendar", "pages/1_Calendar.py"),
    (qa3, "👤", "Profile", "pages/0_Profile.py"),
    (qa4, "🚨", "Emergency", "pages/4_Emergency.py"),
]
for col, icon, label, page in tiles:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.75);border:1px solid rgba(255,255,255,0.95);
             border-radius:18px;padding:1.2rem;text-align:center;
             box-shadow:0 4px 16px rgba(180,100,120,0.07);margin-bottom:0.5rem">
            <div style="font-size:1.8rem">{icon}</div>
            <div style="font-size:0.78rem;font-weight:500;color:#3d1f2e;margin-top:0.3rem">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(label, key=f"tile_{label}"):
            st.switch_page(page)

# ─── BOTTOM ───────────────────────────────────────────────────────────────────
left, right = st.columns([1.1, 1])

with left:
    TYPE_ICONS = {"Scan": "🩻", "Checkup": "🩺", "Blood Test": "🩸", "Other": "📋",
                  "Vaccine": "💉", "Dentist": "🦷"}
    upcoming = sorted([a for a in st.session_state.appointments if a["date"] >= today],
                      key=lambda x: x["date"])[:3]
    html = f'<div class="card"><div class="card-title">🔔 {T["reminders_title"]}</div>'
    if upcoming:
        for appt in upcoming:
            days_away = (appt["date"] - today).days
            badge = "TODAY" if days_away == 0 else (f"in {days_away}d" if days_away <= 7 else appt["date"].strftime("%b %d"))
            badge_style = "background:linear-gradient(135deg,#e8a0b0,#c4607a);color:white" if days_away == 0 else "background:#fce4d6;color:#c4607a"
            html += f"""<div style="display:flex;align-items:center;gap:0.85rem;padding:0.75rem 0;border-bottom:1px solid rgba(196,96,122,0.07)">
                <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#fce4d6,#f5dde8);
                     display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0">
                    {TYPE_ICONS.get(appt['type'], '📋')}
                </div>
                <div style="flex:1">
                    <div style="font-size:0.88rem;font-weight:500;color:#3d1f2e">{appt['title']}</div>
                    <div style="font-size:0.73rem;color:#9e7a88;margin-top:0.1rem">{appt['date'].strftime('%b %d')} · {appt['time']} · {appt['doctor']}</div>
                </div>
                <div style="margin-left:auto;padding:0.2rem 0.6rem;border-radius:999px;font-size:0.66rem;font-weight:600;
                     text-transform:uppercase;letter-spacing:0.07em;{badge_style}">{badge}</div>
            </div>"""
    else:
        html += f'<div style="font-size:0.85rem;color:#9e7a88;padding:0.5rem 0">{T["no_appts"]}</div>'
    html += '<div style="height:1px;background:rgba(196,96,122,0.15);margin:0.75rem 0"></div>'
    for icon, title, sub in HEALTH_REMINDERS[trimester]:
        html += f"""<div style="display:flex;align-items:flex-start;gap:0.85rem;padding:0.75rem 0;border-bottom:1px solid rgba(196,96,122,0.07)">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#fce4d6,#f5dde8);
                 display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0">{icon}</div>
            <div><div style="font-size:0.88rem;font-weight:500;color:#3d1f2e">{title}</div>
            <div style="font-size:0.73rem;color:#9e7a88;margin-top:0.1rem">{sub}</div></div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">💡 {T['tip_title']}</div>
        <div style="background:linear-gradient(135deg,rgba(252,228,214,0.6),rgba(245,221,232,0.5));
             border:1px solid rgba(196,96,122,0.12);border-radius:16px;padding:1.25rem">
            <div style="font-size:0.68rem;color:#c4607a;font-weight:500;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.4rem">Week {weeks}</div>
            <div style="font-size:0.92rem;color:#3d1f2e;line-height:1.65">{tip_text}</div>
            <div style="font-size:0.72rem;color:#b09098;margin-top:0.5rem;font-style:italic">✨ Powered by Fem♥ily AI · Ask more in Chat</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("💬 Ask Fem♥ily AI"):
        st.switch_page("pages/2_Chatbot.py")

st.markdown('<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c4a0ac;font-size:0.75rem;letter-spacing:0.1em">🌸 Always consult your healthcare provider</div>', unsafe_allow_html=True)

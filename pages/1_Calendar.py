import streamlit as st
from datetime import date, timedelta
import calendar
from src.ui.styles import inject_styles, render_topbar, render_sidebar
from src.db.db import save_appointment, get_appointments, delete_appointment

st.set_page_config(page_title="Fem♥ily · Calendar", page_icon="🌸", layout="wide")
inject_styles()

st.markdown("""
<style>
.cal-wrap {
    background:rgba(255,255,255,0.78);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,0.95);border-radius:24px;
    padding:1.75rem;box-shadow:0 4px 32px rgba(180,100,120,0.1);margin-bottom:1.5rem;
}
.cal-month-title {
    font-family:'Cormorant Garamond',serif;font-size:1.8rem;
    font-weight:300;color:#3d1f2e;text-align:center;
}
.cal-grid { display:grid;grid-template-columns:repeat(7,1fr);gap:6px; }
.cal-dow {
    text-align:center;font-size:0.68rem;font-weight:500;color:#b09098;
    text-transform:uppercase;letter-spacing:0.1em;padding-bottom:0.5rem;
}
.cal-cell {
    aspect-ratio:1;border-radius:12px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;font-size:0.88rem;
    position:relative;color:#3d1f2e;
}
.cal-cell.empty  { background:transparent; }
.cal-cell.normal { background:rgba(255,255,255,0.5); }
.cal-cell.today  {
    background:linear-gradient(135deg,#e8a0b0,#c4607a)!important;
    color:white!important;font-weight:600;
    box-shadow:0 4px 12px rgba(196,96,122,0.4);
}
.cal-cell.has-appt { background:rgba(252,228,214,0.8);color:#c4607a;font-weight:600; }
.cal-dot { width:5px;height:5px;border-radius:50%;background:#c4607a;position:absolute;bottom:4px; }
.cal-cell.today .cal-dot { background:white; }

.appt-item {
    display:flex;align-items:center;gap:1rem;
    background:rgba(255,255,255,0.8);border:1px solid rgba(196,96,122,0.1);
    border-radius:16px;padding:1rem 1.25rem;margin-bottom:0.75rem;
}
.appt-icon-box {
    width:46px;height:46px;border-radius:14px;
    display:flex;align-items:center;justify-content:center;
    font-size:1.4rem;flex-shrink:0;
}
.appt-title  { font-weight:500;color:#3d1f2e;font-size:0.95rem; }
.appt-meta   { font-size:0.75rem;color:#9e7a88;margin-top:0.15rem; }
.appt-badge  {
    margin-left:auto;padding:0.25rem 0.75rem;border-radius:999px;
    font-size:0.68rem;font-weight:600;text-transform:uppercase;
    letter-spacing:0.08em;flex-shrink:0;
}
.badge-today    { background:linear-gradient(135deg,#e8a0b0,#c4607a);color:white; }
.badge-soon     { background:#fce4d6;color:#c4607a; }
.badge-upcoming { background:#f5f0f5;color:#9e7a88; }
.badge-past     { background:#f0f0f0;color:#bbb; }

.form-card {
    background:rgba(255,255,255,0.78);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,0.95);border-radius:24px;
    padding:1.75rem;box-shadow:0 4px 32px rgba(180,100,120,0.1);
    margin-bottom:1.25rem;
}
.form-title {
    font-family:'Cormorant Garamond',serif;font-size:1.5rem;
    font-weight:400;color:#3d1f2e;margin:0 0 1.25rem;
}
.scan-item {
    display:flex;align-items:center;gap:0.75rem;
    padding:0.6rem 0;border-bottom:1px solid rgba(196,96,122,0.07);
}
.scan-item:last-child { border-bottom:none; }
</style>
""", unsafe_allow_html=True)

# ─── Auth guard ────────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("Home.py")

render_sidebar()
render_topbar()

# ─── Constants ────────────────────────────────────────────────────────────────
APPT_TYPES = {
    "Scan":       ("🩻", "#fce4d6"),
    "Checkup":    ("🩺", "#e8f5e9"),
    "Blood Test": ("🩸", "#fce4e4"),
    "Vaccine":    ("💉", "#e3f2fd"),
    "Dentist":    ("🦷", "#f3e5f5"),
    "Other":      ("📋", "#fff8e1"),
}
today = date.today()

# ─── State init ───────────────────────────────────────────────────────────────
for k, v in [
    ("cal_month",    today.month),
    ("cal_year",     today.year),
    ("selected_type", "Checkup"),
    ("appts_loaded", False),
]:
    if k not in st.session_state:
        st.session_state[k] = v

db      = st.session_state.get("db")
user_id = st.session_state.get("user_id", "")

# ─── Load appointments from DB (once per session) ─────────────────────────────
if not st.session_state.appts_loaded and db and user_id:
    db_appts = get_appointments(db, user_id)
    # Merge: keep session appts that aren't from DB, then add DB ones
    if db_appts:
        st.session_state.appointments = db_appts
    elif "appointments" not in st.session_state:
        # Seed defaults only if DB is also empty
        st.session_state.appointments = [
            {"db_id": None, "title": "20-Week Anatomy Scan",
             "date": today + timedelta(days=5),  "time": "10:00 AM",
             "type": "Scan",       "doctor": "Dr. Priya Sharma",
             "notes": "Bring water, full bladder needed", "reminder": True},
            {"db_id": None, "title": "Routine Checkup",
             "date": today + timedelta(days=14), "time": "2:30 PM",
             "type": "Checkup",    "doctor": "Dr. Anita Mehta",
             "notes": "", "reminder": True},
        ]
    st.session_state.appts_loaded = True
elif "appointments" not in st.session_state:
    st.session_state.appointments = []

# ─── Layout ───────────────────────────────────────────────────────────────────
cal_col, right_col = st.columns([1.6, 1])

# ══════════════════════════════════════════════════════════════════════════════
# LEFT — Calendar + appointment list
# ══════════════════════════════════════════════════════════════════════════════
with cal_col:

    # ── Month navigation ──────────────────────────────────────────────────────
    st.markdown('<div class="cal-wrap">', unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns([1, 3, 1])
    with nav1:
        if st.button("◀", key="prev"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1
            st.rerun()
    with nav2:
        month_name = date(st.session_state.cal_year, st.session_state.cal_month, 1).strftime("%B %Y")
        st.markdown(f'<div class="cal-month-title">{month_name}</div>', unsafe_allow_html=True)
    with nav3:
        if st.button("▶", key="next"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1
            st.rerun()

    # ── Calendar grid ─────────────────────────────────────────────────────────
    cal_matrix = calendar.monthcalendar(st.session_state.cal_year, st.session_state.cal_month)
    appt_days = {
        a["date"].day for a in st.session_state.appointments
        if a["date"].month == st.session_state.cal_month
        and a["date"].year  == st.session_state.cal_year
    }

    cal_html = '<div class="cal-grid">'
    for dow in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        cal_html += f'<div class="cal-dow">{dow}</div>'
    for week in cal_matrix:
        for day in week:
            if day == 0:
                cal_html += '<div class="cal-cell empty"></div>'
            else:
                is_today = (
                    day == today.day
                    and st.session_state.cal_month == today.month
                    and st.session_state.cal_year  == today.year
                )
                has_appt = day in appt_days
                cls  = "cal-cell " + ("today" if is_today else ("has-appt" if has_appt else "normal"))
                dot  = '<div class="cal-dot"></div>' if has_appt else ""
                cal_html += f'<div class="{cls}">{day}{dot}</div>'
    cal_html += '</div>'
    st.markdown(cal_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Appointment list ──────────────────────────────────────────────────────
    all_appts  = sorted(st.session_state.appointments, key=lambda x: x["date"])
    upcoming   = [a for a in all_appts if a["date"] >= today]
    past_appts = [a for a in all_appts if a["date"] <  today]

    if upcoming:
        st.markdown(
            '<div style="font-family:\'Cormorant Garamond\',serif;'
            'font-size:1.3rem;color:#3d1f2e;margin:1rem 0 0.75rem">📅 Upcoming</div>',
            unsafe_allow_html=True,
        )
        for idx, appt in enumerate(upcoming):
            icon, bg  = APPT_TYPES.get(appt["type"], ("📋", "#fff8e1"))
            days_away = (appt["date"] - today).days
            if   days_away == 0:  badge_cls, badge_txt = "badge-today",    "TODAY"
            elif days_away <= 7:  badge_cls, badge_txt = "badge-soon",     f"in {days_away}d"
            else:                 badge_cls, badge_txt = "badge-upcoming", appt["date"].strftime("%b %d")
            notes_html = f'<div class="appt-meta">📝 {appt["notes"]}</div>' if appt.get("notes") else ""
            reminder   = "🔔" if appt.get("reminder") else ""

            appt_html = (
                f'<div class="appt-item">'
                f'<div class="appt-icon-box" style="background:{bg}">{icon}</div>'
                f'<div style="flex:1">'
                f'<div class="appt-title">{appt["title"]} {reminder}</div>'
                f'<div class="appt-meta">{appt["date"].strftime("%A, %B %d, %Y")} · {appt["time"]} · {appt["doctor"]}</div>'
                f'{notes_html}'
                f'</div>'
                f'<div class="appt-badge {badge_cls}">{badge_txt}</div>'
                f'</div>'
            )
            st.markdown(appt_html, unsafe_allow_html=True)

            if appt.get("db_id") and st.button("🗑️ Remove", key=f"del_{appt['db_id']}"):
                delete_appointment(db, appt["db_id"])
                st.session_state.appointments = [
                    a for a in st.session_state.appointments
                    if a.get("db_id") != appt["db_id"]
                ]
                st.success("Appointment removed.")
                st.rerun()

    if past_appts:
        st.markdown(
            '<div style="font-family:\'Cormorant Garamond\',serif;'
            'font-size:1.3rem;color:#3d1f2e;margin:1.25rem 0 0.75rem">✓ Past</div>',
            unsafe_allow_html=True,
        )
        for appt in past_appts[-3:]:
            icon, bg = APPT_TYPES.get(appt["type"], ("📋", "#fff8e1"))
            st.markdown(f"""
            <div class="appt-item" style="opacity:0.6">
                <div class="appt-icon-box" style="background:{bg}">{icon}</div>
                <div>
                    <div class="appt-title">{appt['title']}</div>
                    <div class="appt-meta">
                        {appt['date'].strftime('%B %d, %Y')} · {appt['time']} · {appt['doctor']}
                    </div>
                </div>
                <div class="appt-badge badge-past">Done</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT — Add appointment form + recommended scans
# ══════════════════════════════════════════════════════════════════════════════
with right_col:

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">➕ Schedule Appointment</div>', unsafe_allow_html=True)

    # Type selector
    st.markdown(
        '<div style="font-size:0.72rem;color:#9e7a88;text-transform:uppercase;'
        'letter-spacing:0.12em;margin-bottom:0.5rem;font-weight:500">Appointment Type</div>',
        unsafe_allow_html=True,
    )
    type_cols = st.columns(3)
    for i, t in enumerate(APPT_TYPES.keys()):
        icon, _ = APPT_TYPES[t]
        with type_cols[i % 3]:
            is_sel = st.session_state.selected_type == t
            btn_style = (
                "background:linear-gradient(135deg,#fce4d6,#f5dde8);"
                "border:1.5px solid #c4607a;color:#c4607a;"
                if is_sel else
                "background:rgba(255,255,255,0.7);"
                "border:1.5px solid rgba(196,96,122,0.2);color:#9e7a88;"
            )
            st.markdown(
                f'<div style="{btn_style}border-radius:10px;padding:0.45rem;'
                f'text-align:center;font-size:0.78rem;font-weight:500;'
                f'margin-bottom:0.25rem;cursor:pointer">{icon} {t}</div>',
                unsafe_allow_html=True,
            )
            if st.button(f"{icon} {t}", key=f"type_{t}"):
                st.session_state.selected_type = t
                st.rerun()

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    # Form fields
    appt_title  = st.text_input("Appointment Title",    placeholder="e.g. 28-Week Checkup")
    appt_date   = st.date_input("Date", value=today + timedelta(days=7), min_value=today)
    tc1, tc2    = st.columns(2)
    with tc1:
        appt_time   = st.text_input("Time",               value="10:00 AM")
    with tc2:
        appt_doctor = st.text_input("Doctor / Location",  placeholder="Dr. Name or clinic")
    appt_notes    = st.text_area( "Notes (optional)",    placeholder="e.g. Fast 8 hrs before · Bring ID", height=80)
    appt_reminder = st.checkbox("🔔 Set reminder", value=True)

    # Save to DB
    if st.button("Save Appointment 🌸", key="save_appt", use_container_width=True):
        if not appt_title.strip():
            st.warning("Please enter a title for the appointment.")
        elif not appt_doctor.strip():
            st.warning("Please enter a doctor or location.")
        else:
            new_appt = {
                "title":    appt_title.strip(),
                "date":     appt_date,
                "time":     appt_time,
                "type":     st.session_state.selected_type,
                "doctor":   appt_doctor.strip(),
                "notes":    appt_notes,
                "reminder": appt_reminder,
            }
            # Persist to ChromaDB
            if db and user_id:
                record_id = save_appointment(db, user_id, new_appt)
                new_appt["db_id"] = record_id
                st.success(f"✅ Appointment saved to your records! {APPT_TYPES[st.session_state.selected_type][0]}")
            else:
                new_appt["db_id"] = None
                st.success(f"✅ Appointment saved! {APPT_TYPES[st.session_state.selected_type][0]}")

            st.session_state.appointments.append(new_appt)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Recommended scans reference card
    st.markdown("""
    <div class="form-card">
        <div class="form-title">📋 Recommended Scans</div>
        <div class="scan-item">
            <span style="font-size:1.2rem">🩻</span>
            <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Dating Scan</div>
            <div style="font-size:0.73rem;color:#9e7a88">Week 8–14</div></div>
        </div>
        <div class="scan-item">
            <span style="font-size:1.2rem">🧬</span>
            <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">NT Scan</div>
            <div style="font-size:0.73rem;color:#9e7a88">Week 11–14</div></div>
        </div>
        <div class="scan-item">
            <span style="font-size:1.2rem">🩻</span>
            <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Anatomy Scan</div>
            <div style="font-size:0.73rem;color:#9e7a88">Week 18–22</div></div>
        </div>
        <div class="scan-item">
            <span style="font-size:1.2rem">🩸</span>
            <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Glucose Test</div>
            <div style="font-size:0.73rem;color:#9e7a88">Week 24–28</div></div>
        </div>
        <div class="scan-item">
            <span style="font-size:1.2rem">💉</span>
            <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Tdap Vaccine</div>
            <div style="font-size:0.73rem;color:#9e7a88">Week 27–36</div></div>
        </div>
        <div class="scan-item">
            <span style="font-size:1.2rem">🩻</span>
            <div><div style="font-size:0.85rem;font-weight:500;color:#3d1f2e">Growth Scan</div>
            <div style="font-size:0.73rem;color:#9e7a88">Week 32–36</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    '<div style="text-align:center;padding:1.5rem 0 0.5rem;color:#c4a0ac;'
    'font-size:0.75rem;letter-spacing:0.1em">🌸 Always consult your healthcare provider</div>',
    unsafe_allow_html=True,
)
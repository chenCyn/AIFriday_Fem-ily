import os
import streamlit as st
from src.db.db import init_db, get_user
from src.db.migrate_users import migrate_users

st.set_page_config(page_title="🤰 NGO Maternal Care Outreach", layout="wide")

db = init_db()

# --- Ensure users are loaded into ChromaDB ---
if "users_loaded" not in st.session_state:
    existing = db.get()
    if not existing or len(existing.get("ids", [])) == 0:
        migrate_users()
    st.session_state.users_loaded = True

# --- Session state init ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "role" not in st.session_state:
    st.session_state.role = None
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.title("🔐 Shared Login")
    user_id = st.text_input("Enter your ID (e.g., p_001)")  
    if st.button("Login"):
        user = get_user(db, user_id)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.user_profile = user
            st.session_state.db = db
            st.session_state.role = user["metadata"].get("role")

            if st.session_state.role == "patient":
                st.success(f"Welcome, {user['metadata'].get('name','Patient')}! Redirecting to chatbot...")
                st.switch_page("pages/1_Chatbot.py")
            # elif st.session_state.role == "volunteer":
            #     st.success(f"Welcome, {user['metadata'].get('name','Volunteer')}! Redirecting to volunteer dashboard...")
            #     st.switch_page("pages/2_Volunteer.py")
            else:
                st.error("Unknown role. Please contact admin.")
        else:
            st.error("No user found with that ID.")
    st.stop()

# --- SIDEBAR PROFILE (role-aware) ---
profile = st.session_state.user_profile
if profile:
    st.sidebar.header("User Profile")
    st.sidebar.write(f"**Name:** {profile['metadata'].get('name')}")
    st.sidebar.write(f"**Role:** {profile['metadata'].get('role')}")
    st.sidebar.write(f"**Age:** {profile['metadata'].get('age')}")
    st.sidebar.write(f"**Location:** {profile['metadata'].get('location')}")

    if st.session_state.role == "patient":
        st.sidebar.write(f"**Pregnancy Week:** {profile['metadata'].get('pregnancy_week')}")
    # elif st.session_state.role == "volunteer":
    #     st.sidebar.write(f"**Expertise:** {profile['metadata'].get('expertise')}")

    # --- Role-based navigation ---
    st.sidebar.subheader("Navigation")
    if st.session_state.role == "patient":
        if st.sidebar.button("💬 Chatbot"):
            st.switch_page("pages/1_Chatbot.py")
        if st.sidebar.button("👤 Profile"):
            st.switch_page("pages/4_Profile.py")
        if st.sidebar.button("🚨 Emergency"):
            st.switch_page("pages/3_Emergency.py")
    # elif st.session_state.role == "volunteer":
    #     if st.sidebar.button("🙌 Volunteer Dashboard"):
    #         st.switch_page("pages/2_Volunteer.py")

    # --- Logout option ---
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.user_profile = None
        st.session_state.role = None
        st.experimental_rerun()

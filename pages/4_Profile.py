import streamlit as st
from src.db.db import get_user_records  

st.title("👤 Patient Profile")

# --- Permission guard ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the main page first.")
    st.stop()

if st.session_state.role != "patient":
    st.error("Access denied. This page is only for patients.")
    st.stop()

# --- Load DB and user profile ---
db = st.session_state.get("db")
user_id = st.session_state.get("user_id")
profile = st.session_state.get("user_profile")

if profile:
    st.write("### Patient Details")
    st.write(f"**Name:** {profile['metadata'].get('name')}")
    st.write(f"**Age:** {profile['metadata'].get('age')}")
    st.write(f"**Location:** {profile['metadata'].get('location')}")
    st.write(f"**Pregnancy Week:** {profile['metadata'].get('pregnancy_week')}")

    st.write("---")
    st.write("### Recent Records")

    # Fetch records strictly for this patient ID
    results = get_user_records(db, user_id, k=3)
    if results:
        for r in results:
            st.write(f"**Symptoms:** {r['page_content']}")
            st.write(f"**Risk Level:** {r['metadata'].get('risk_level','Unknown')}")
            st.write(f"**Recommended Action:** {r['metadata'].get('action','N/A')}")
            st.write("---")
    else:
        st.info("No records found for this patient yet.")

else:
    st.warning("No profile information available.")

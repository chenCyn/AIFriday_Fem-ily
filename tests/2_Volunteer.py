import streamlit as st
from src.db.db import search_patients

st.title("👩‍⚕️ Volunteer Live Chat Dashboard")

# --- Permission guard ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the main page first.")
    st.stop()

if st.session_state.role != "volunteer":
    st.error("Access denied. This page is only for volunteers.")
    st.stop()

# --- Reuse DB from app.py ---
db = st.session_state.get("db")

# --- Search interface ---
query = st.text_input("Search patient records (e.g. 'headache')")
if st.button("Search") and query:
    results = search_patients(db, query, k=5)
    if not results:
        st.info("No matching records found.")
    else:
        for r in results:
            with st.expander(f"Patient ID: {r.metadata.get('id','N/A')}"):
                st.write(f"**Symptoms:** {r.page_content}")
                st.write(f"**Risk Level:** {r.metadata.get('risk_level','Unknown')}")
                st.write(f"**Recommended Action:** {r.metadata.get('action','N/A')}")

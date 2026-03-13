import streamlit as st

st.title("🚨 Emergency Contact")

# --- Permission guard ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the main page first.")
    st.stop()

# Only patients should be able to trigger emergency alerts
if st.session_state.role != "patient":
    st.error("Access denied. This page is only for patients.")
    st.stop()

st.write("If you are experiencing severe symptoms or complications, please trigger an emergency alert below.")

if st.button("Trigger Emergency Alert"):
    st.error("🚨 Emergency alert triggered! Please seek immediate medical care.")
    st.info("A volunteer has been notified and will reach out to you shortly.")
    # TODO: Add integration with SMS/email notification system for volunteers

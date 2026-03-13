import streamlit as st
from src.core.api import get_conversation_chain
from src.core.backend import risk_assessment
from src.db.db import add_patient_record

st.title("💬 Patient Chatbot")

# --- Permission guard ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the main page first.")
    st.stop()

if st.session_state.role != "patient":
    st.error("Access denied. This page is only for patients.")
    st.stop()

# --- Reuse DB from app.py ---
db = st.session_state.get("db")
qa_chain = get_conversation_chain(db)

# --- Initialize chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display past messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle new input ---
if user_input := st.chat_input("Describe your symptoms or ask a question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Use pregnancy week from profile
    pregnancy_week = st.session_state.user_profile["metadata"].get("pregnancy_week", 30)
    risk_level, action = risk_assessment(user_input, pregnancy_week=pregnancy_week)

    res = qa_chain.invoke(user_input)
    ai_answer = res["result"]

    response_text = f"{ai_answer}\n\nRisk Level: **{risk_level}**\nRecommended Action: **{action}**"
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Save record in DB
    metadata = {"risk_level": risk_level, "action": action}
    add_patient_record(db, st.session_state.user_id, user_input, metadata)

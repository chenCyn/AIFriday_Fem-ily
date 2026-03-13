# import gradio as gr
# from src.backend import process_question

# def create_ui(qa_chain):
#     def chat(chat_history, user_input):
#         answer = process_question(user_input, qa_chain)
#         chat_history.append({"role": "user", "content": user_input})
#         chat_history.append({"role": "assistant", "content": answer})
#         return chat_history

#     with gr.Blocks() as demo:
#         gr.Markdown('# HR Policies Bot')

#         with gr.Tab("Ask Chatbot"):
#             chatbot = gr.Chatbot(height=300)
#             message = gr.Textbox(label='Please type your query and press Enter.')
#             clear = gr.ClearButton([message, chatbot])

#             message.submit(chat, [chatbot, message], chatbot)
#             message.submit(lambda: gr.update(value=""), None, [message])

#     return demo


import streamlit as st
from src.backend import process_question
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import openai
import tempfile
import numpy as np
import soundfile as sf

def create_ui(qa_chain):
    st.set_page_config(page_title="HR Policies Bot", layout="wide")
    st.title("🎙️ HR Policies Bot (Streamlit + Voice Input)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Text input
    user_input = st.text_input("Type your query or use voice below:")

    # Voice input
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"audio": True, "video": False},
    )

    if webrtc_ctx.audio_receiver:
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        if audio_frames:
            audio_data = np.concatenate([f.to_ndarray() for f in audio_frames])
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                sf.write(tmpfile.name, audio_data, samplerate=16000)
                with open(tmpfile.name, "rb") as audio_file:
                    transcript = openai.Audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                    user_input = transcript.text
                    st.write(f"🎤 You said: {user_input}")

    # Process question
    if user_input:
        answer = process_question(user_input, qa_chain)
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", answer))

    # Display chat
    for role, msg in st.session_state.chat_history:
        if role == "User":
            st.markdown(f"**👤 {role}:** {msg}")
        else:
            st.markdown(f"**🤖 {role}:** {msg}")

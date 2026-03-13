# Core LangChain
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
import httpx

# Community integrations
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings

import gradio as gr

# Step 1: Load and split documents
loader = PyPDFLoader("content/HR_Policy_2018.pdf")
documents = loader.load_and_split()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
texts = text_splitter.split_documents(documents)

# Step 2: Generate embeddings with Ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Step 3: Create VectorStore (Chroma)
db = Chroma.from_documents(texts, embeddings, persist_directory="db2")

# Step 4: Build QA chain with Ollama LLM
def get_conversation_chain(db):
    client = httpx.Client(verify=False)

    llm = ChatOpenAI(
        base_url="http://localhost:11434/v1",
        model="llama-3.2-3b-it:latest",
        api_key="sk-dtS7Hk9HHFpmrezMoo4Urw",
        http_client=client
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff",
        return_source_documents=True,
        verbose=False
    )
    return qa_chain

qa_chain = get_conversation_chain(db)

# Function to process each question
def process_question(question, qa_chain):
    predefined_answers = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! What can I do for you?",
        "hey": "Hey! How can I help you?",
        "good morning": "Good morning! How can I assist you?",
        "good afternoon": "Good afternoon! What can I help you with?",
        "good evening": "Good evening! How can I assist you?"
    }

    question_lower = question.lower()
    if question_lower in predefined_answers:
        return predefined_answers[question_lower]

    res = qa_chain.invoke(question)
    answer_text = res["result"]
    sources = res.get("source_documents", [])

    if sources:
        pages = [str(doc.metadata.get("page", "Unknown")) for doc in sources]
        page_info = f"(Found on page(s): {', '.join(pages)})"
        return f"{answer_text}\n\n{page_info}"
    else:
        # fallback: draft email
        return f"""Dear HR Team,

I was reviewing the HR Policy document but could not locate information regarding: "{question}".

Could you please provide clarification or direct me to the relevant section?

Thank you,
[Your Name]"""

# Gradio Interface
def chat(chat_history, user_input):
    answer = process_question(user_input, qa_chain)
    # ✅ Use dict format for Chatbot messages
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": answer})
    return chat_history

with gr.Blocks() as demo:
    gr.Markdown('# HR Policies Bot')

    with gr.Tab("Ask Chatbot"):
        chatbot = gr.Chatbot(height=300)
        message = gr.Textbox(label='Please type your query and press Enter.')
        clear = gr.ClearButton([message, chatbot])  # ✅ clears both textbox and chat

        message.submit(chat, [chatbot, message], chatbot)
        message.submit(lambda: gr.update(value=""), None, [message])

demo.launch(css=".gradio-container {background-color: lightblue}", debug=True)

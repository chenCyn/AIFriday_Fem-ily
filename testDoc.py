#importing necessary modules/libraries
# from langchain.chains import RetrievalQA
# from langchain.document_loaders import PyPDFLoader
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import HuggingFaceHub
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma

# Core LangChain
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Community integrations
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

# HuggingFace integrations
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint

# Ollama LLM integration
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI


import gradio as gr


# Replace with your Hugging Face Hub API token
HUGGINGFACEHUB_API_TOKEN = "sk-dtS7Hk9HHFpmrezMoo4Urw"

# Step 1: Load and split documents using PyPDFLoader and RecursiveCharacterTextSplitter
loader = PyPDFLoader("content/HR_Policy_2018.pdf")
documents = loader.load_and_split()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
texts = text_splitter.split_documents(documents)

# Step 2: Generate embeddings using HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 3: Create VectorStore (Chroma) from documents and embeddings
db = Chroma.from_documents(texts, embeddings, persist_directory="db2")

# def get_conversation_chain(db):
#     llm_huggingfacehub = HuggingFaceEndpoint(
#         huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
#         repo_id="mistralai/Mistral-7B-Instruct-v0.2",
#         model_kwargs={"temperature": 0.1, "max_length": 1000, "top_k": 3, "do_sample": True, "num_return_sequences": 1}
#     )
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm_huggingfacehub,
#         retriever=db.as_retriever(search_kwargs={"k": 3}),
#         chain_type="stuff",
#         return_source_documents=True,
#         verbose=False
#     )
#     return qa_chain

def get_conversation_chain(db):
    # Use a local Ollama model (make sure you’ve pulled it with `ollama pull mistral`)
    # llm_ollama = Ollama(
    #     model="llama-3.2-3b-it:latest",   # or "llama2", "gemma", etc. depending on what you’ve installed
    #     base_url="http://localhost:11434"  # default Ollama API endpoint
    # )

    llm = ChatOpenAI(
    # base_url="https://genailab.tcs.in",
    # model = "azure_ai/genailab-maas-Deepseek-V3-0324",
    base_url = "http://localhost:11434/v1",
    model = 'llama-3.2-3b-it:latest',
    api_key = "sk-dtS7Hk9HHFpmrezMoo4Urw",
    http_client = client
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

    # Check if the question is in the predefined answers
  question_lower = question.lower()
  if question_lower in predefined_answers:
      return predefined_answers[question_lower]

  res = qa_chain(question)
  output_text = res["result"]
  lines = output_text.split('\n')

  q = None
  answer = None

  for line in lines:
      if line.startswith("Question:"):
          q = line.replace("Question:", "").strip()
      elif line.startswith("Helpful Answer:"):
          answer = line.replace("Helpful Answer:", "").strip()

  if q and answer:
      return answer
  else:
      return "Could not extract question and answer from the output."
     

#Gradio Interface
def chat(chat_history, user_input):
    answer = process_question(user_input, qa_chain)
    chat_history.append((user_input, answer))
    return chat_history

with gr.Blocks(css=".gradio-container {background-color: lightblue}") as demo:
    gr.Markdown('# HR Policies Bot')

    with gr.Tab("Ask Chatbot"):
        chatbot = gr.Chatbot(height=300)
        message = gr.Textbox(label='Please type your query and press Enter.')
        clear = gr.ClearButton([message])

        message.submit(chat, [chatbot, message], chatbot)
        message.submit(lambda x: gr.update(value=""), None, [message])


     

demo.launch(debug=True)
     
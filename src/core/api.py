import os
import httpx
from dotenv import load_dotenv
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

def get_conversation_chain(db, user_id=None, role=None):
    api_key = os.getenv("OPENAI_API_KEY", "ollama")

    client = httpx.Client(verify=False)

    llm = ChatOpenAI(
        base_url="http://localhost:11434/v1",
        model="llama3.2:3b",
        api_key=api_key,
        http_client=client
    )

    prompt_template = """
You are Fem♥ily AI, a warm and empathetic maternal health assistant speaking directly to the patient.
Answer questions and evaluate patient reports based on the provided context.
Speak with care and compassion. Do not mention volunteers or internal systems.
If the input is not related to maternal health, politely redirect to maternal care topics.

Context: {context}

Patient Report / Question: {question}

Provide:
- A clear, empathetic response
- Possible condition or concern (if applicable)
- Recommended action (self-care, volunteer follow-up, urgent referral)
- Warm, supportive closing message

Answer:
"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    if role == "patient" and user_id:
        retriever = db.as_retriever(
            search_kwargs={"filter": {"id": user_id}, "k": 3}
        )
    else:
        retriever = db.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        verbose=False,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain

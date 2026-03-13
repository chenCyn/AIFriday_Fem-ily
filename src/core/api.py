import os
import httpx
from dotenv import load_dotenv
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()  # loads variables from .env

def get_conversation_chain(db, user_id=None, role=None):
    api_key = os.getenv("OPENAI_API_KEY")

    client = httpx.Client(verify=False)

    llm = ChatOpenAI(
        base_url="http://localhost:11434/v1",
        model="llama-3.2-3b-it:latest",
        api_key=api_key,
        http_client=client
    )

    # Maternal care system prompt
    prompt_template = """
You are an AI maternal health assistant speaking directly to the patient.
Answer questions and evaluate patient reports based only on the provided patient context.
Do not mention volunteers or other users.
If the input is not related to maternal health, politely redirect to maternal care topics.

Context: {context}

Patient Report / Question: {question}

Provide:
- Risk level (Low / Moderate / High)
- Possible condition or concern
- Recommended action (self-care, volunteer follow-up, urgent referral)
- Empathetic guidance message

Answer:
"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # --- Restrict retriever based on role ---
    if role == "patient" and user_id:
        # Only retrieve this patient's own records
        retriever = db.as_retriever(
            search_kwargs={"filter": {"id": user_id}, "k": 3}
        )
    else:
        # Volunteers can search across all patient records
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

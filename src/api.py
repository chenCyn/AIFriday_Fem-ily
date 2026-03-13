import httpx
from langchain_classic.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def get_conversation_chain(db):
    client = httpx.Client(verify=False)

    llm = ChatOpenAI(
        base_url="http://localhost:11434/v1",
        model="llama-3.2-3b-it:latest",
        api_key="sk-dtS7Hk9HHFpmrezMoo4Urw",
        http_client=client
    )

    # Define the system prompt to set the scope of the bot
    prompt_template = """You are an HR policy chatbot designed to help employees quickly check through the long HR policy PDF. Answer questions based on the provided context only. If the question is not related to HR policies, politely redirect to HR topics.

Context: {context}

Question: {question}

Answer:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff",
        return_source_documents=True,
        verbose=False,
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain

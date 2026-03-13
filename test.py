from langchain_openai import ChatOpenAI
import httpx
client = httpx.Client(verify = False)
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    # model = "azure_ai/genailab-maas-Deepseek-V3-0324",
    # base_url = "http://localhost:11434/v1",
    model = 'llama-3.2-3b-it:latest',
    api_key = "sk-dtS7Hk9HHFpmrezMoo4Urw",
    http_client = client
)
result = llm.invoke("Hi")
print(result)
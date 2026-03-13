from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import chromadb

embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory="db2", embedding_function=embeddings)

# Check how many documents are stored
print("this is the number of files in " + str(db._collection.count()))

client = chromadb.PersistentClient(path="db2")
collection = client.get_collection("langchain")

print(collection.peek())   # preview stored items

# # Run a quick similarity search
# results = db.similarity_search("leave policy", k=3)
# for r in results:
#     print(r.page_content, r.metadata)

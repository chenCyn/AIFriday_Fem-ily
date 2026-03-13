import chromadb

# Connect to your persisted ChromaDB
client = chromadb.PersistentClient(path="ngo_db")

# List all collections
collections = client.list_collections()
print("Collections found:")
for c in collections:
    print("-", c.name)

# Inspect each collection
for c in collections:
    print(f"\n=== Collection: {c.name} ===")
    collection = client.get_collection(c.name)
    print("Total vectors:", collection.count())

    # Peek at first few items
    preview = collection.peek()
    print("Preview IDs:", preview.get("ids"))
    print("Preview metadatas:", preview.get("metadatas"))

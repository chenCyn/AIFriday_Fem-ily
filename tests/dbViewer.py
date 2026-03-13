import streamlit as st
import chromadb

# Connect to your persisted ChromaDB
client = chromadb.PersistentClient(path="db2")

# List collections
collections = client.list_collections()
st.sidebar.title("ChromaDB Collections")
selected_collection = st.sidebar.selectbox("Choose a collection", [c.name for c in collections])

if selected_collection:
    collection = client.get_collection(selected_collection)

    st.title(f"📊 ChromaDB Viewer - {selected_collection}")
    st.write(f"Total vectors: {collection.count()}")

    # Preview first few items
    st.subheader("Preview stored items")
    preview = collection.peek()
    st.json(preview)

    # Search box
    st.subheader("🔍 Search your DB")
    query = st.text_input("Enter a query")
    if query:
        results = collection.query(
            query_texts=[query],
            n_results=5
        )
        st.write("Results:")
        st.json(results)

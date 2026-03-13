import csv
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

def init_db(persist_dir="ngo_db"):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return db

def load_users_from_csv(db, filepath="users.csv"):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only load patient data
            # If your CSV has a 'role' column, skip non-patients
            if "role" in row and row["role"] != "patient":
                # print(f"⚠️ Skipping non-patient user: {row['user_id']}")
                continue

            profile_text = f"{row['name']}, {row['age']} years old, {row['location']}, {row['pregnancy_week']} weeks pregnant"
            metadata = {
                "name": row["name"],
                "age": int(row["age"]),
                "location": row["location"],
                "pregnancy_week": int(row["pregnancy_week"]),
                "role": "patient"  # force role to patient
            }
            db.add_texts([profile_text], metadatas=[metadata], ids=[f"user_{row['user_id']}"])

def get_user(db, user_id):
    results = db.get(ids=[user_id])
    if results and results.get("documents"):
        metadata = results["metadatas"][0]
        # Block volunteers
        if metadata.get("role") != "patient":
            return None
        return {
            "profile_text": results["documents"][0],
            "metadata": metadata
        }
    return None

def get_user_records(db, user_id: str, k: int = 3):
    results = db.get(ids=[user_id])
    if not results or not results.get("documents"):
        return []
    # Wrap into a list of simple objects for consistency
    return [{
        "page_content": results["documents"][0],
        "metadata": results["metadatas"][0]
    }]

def add_patient_record(db, patient_id, text, metadata):
    db.add_texts([text], metadatas=[metadata], ids=[patient_id])

def search_patients(db, query, k=5):
    # Only search patient records
    return db.similarity_search(query, k=k)

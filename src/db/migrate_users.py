import csv
import os
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from src.core.users import BaseUser   # updated import

PERSIST_DIR = "ngo_db"
PATIENTS_CSV = os.path.join("data", "patients.csv")
VOLUNTEERS_CSV = os.path.join("data", "volunteers.csv")

def init_db():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return db

def load_csv(db, filepath):
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = BaseUser.from_dict(row)
            if not user.user_id:
                print(f"⚠️ Skipping row with missing ID: {row}")
                continue
            db.add_texts(
                [user.to_profile_text()],
                metadatas=[user.to_metadata()],
                ids=[str(user.user_id)]
            )


def migrate_users():
    db = init_db()

    if os.path.exists(PATIENTS_CSV):
        load_csv(db, PATIENTS_CSV)
        print("✅ Patients loaded into ChromaDB.")
    else:
        print("⚠️ patients.csv not found.")

    # if os.path.exists(VOLUNTEERS_CSV):
    #     load_csv(db, VOLUNTEERS_CSV)
    #     print("✅ Volunteers loaded into ChromaDB.")
    # else:
    #     print("⚠️ volunteers.csv not found.")

    print("🎉 Migration complete.")

if __name__ == "__main__":
    migrate_users()

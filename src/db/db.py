import csv
import uuid
from datetime import date
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


def init_db(persist_dir: str = "ngo_db") -> Chroma:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return db


def load_users_from_csv(db: Chroma, filepath: str = "users.csv") -> None:
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            role = row.get("role", "patient")
            if role == "patient":
                profile_text = (
                    f"{row['name']}, {row['age']} years old, "
                    f"{row['location']}, {row['pregnancy_week']} weeks pregnant"
                )
                metadata = {
                    "name": row["name"],
                    "age": int(row["age"]),
                    "location": row["location"],
                    "pregnancy_week": int(row["pregnancy_week"]),
                    "role": "patient",
                }
                db.add_texts([profile_text], metadatas=[metadata], ids=[f"user_{row['user_id']}"])

            elif role == "volunteer":
                profile_text = (
                    f"{row['name']}, volunteer, {row.get('location', '')}, "
                    f"expertise: {row.get('expertise', 'general')}"
                )
                metadata = {
                    "name": row["name"],
                    "location": row.get("location", ""),
                    "expertise": row.get("expertise", "general"),
                    "role": "volunteer",
                }
                db.add_texts([profile_text], metadatas=[metadata], ids=[f"user_{row['user_id']}"])


def get_user(db: Chroma, user_id: str) -> dict | None:
    ids_to_try = [user_id, f"user_{user_id}"]
    for uid in ids_to_try:
        try:
            results = db.get(ids=[uid])
            if results and results.get("documents"):
                metadata = results["metadatas"][0]
                return {
                    "profile_text": results["documents"][0],
                    "metadata": metadata,
                }
        except Exception:
            continue
    return None


def get_user_records(db: Chroma, user_id: str, k: int = 5) -> list[dict]:
    ids_to_try = [user_id, f"user_{user_id}"]
    for uid in ids_to_try:
        try:
            results = db.get(ids=[uid])
            if results and results.get("documents"):
                return [
                    {"page_content": doc, "metadata": meta}
                    for doc, meta in zip(results["documents"], results["metadatas"])
                ]
        except Exception:
            continue
    return []


def add_patient_record(db: Chroma, patient_id: str, text: str, metadata: dict) -> None:
    import hashlib, time
    record_id = f"rec_{patient_id}_{hashlib.md5(f'{text}{time.time()}'.encode()).hexdigest()[:8]}"
    metadata["patient_id"] = patient_id
    db.add_texts([text], metadatas=[metadata], ids=[record_id])


def search_patients(db: Chroma, query: str, k: int = 5) -> list:
    return db.similarity_search(query, k=k)


# ── Appointment CRUD ───────────────────────────────────────────────────────────

def save_appointment(db: Chroma, user_id: str, appointment: dict) -> str:
    """Save a new appointment to ChromaDB. Returns the record ID."""
    record_id = f"appt_{user_id}_{uuid.uuid4().hex[:8]}"
    text = (
        f"Appointment: {appointment['title']} on {appointment['date']} "
        f"at {appointment['time']} with {appointment['doctor']}. "
        f"Type: {appointment['type']}. Notes: {appointment.get('notes', '')}."
    )
    metadata = {
        "record_type":  "appointment",
        "patient_id":   user_id,
        "title":        appointment["title"],
        "date":         appointment["date"].isoformat(),
        "time":         appointment["time"],
        "appt_type":    appointment["type"],
        "doctor":       appointment["doctor"],
        "notes":        appointment.get("notes", ""),
        "reminder":     str(appointment.get("reminder", True)),
    }
    db.add_texts([text], metadatas=[metadata], ids=[record_id])
    return record_id


def get_appointments(db: Chroma, user_id: str) -> list[dict]:
    """Fetch all appointments for a patient from ChromaDB."""
    try:
        all_records = db.get()
        appointments = []
        for i, meta in enumerate(all_records.get("metadatas", [])):
            if (
                meta.get("record_type") == "appointment"
                and meta.get("patient_id") == user_id
            ):
                appointments.append({
                    "db_id":    all_records["ids"][i],
                    "title":    meta.get("title", "Appointment"),
                    "date":     date.fromisoformat(meta["date"]),
                    "time":     meta.get("time", ""),
                    "type":     meta.get("appt_type", "Other"),
                    "doctor":   meta.get("doctor", ""),
                    "notes":    meta.get("notes", ""),
                    "reminder": meta.get("reminder", "True") == "True",
                })
        return sorted(appointments, key=lambda x: x["date"])
    except Exception:
        return []


def delete_appointment(db: Chroma, record_id: str) -> None:
    """Delete an appointment record by its ChromaDB ID."""
    try:
        db.delete(ids=[record_id])
    except Exception:
        pass
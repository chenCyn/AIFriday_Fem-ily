# Fem♥ily NGO — Integrated Maternal Health App

A unified Streamlit app combining **Fem♥ily's** beautiful pregnancy tracking UI with the **NGO Maternal Care** backend — AI chatbot, volunteer dashboard, emergency alerts, and calendar.

---

## Project Structure

```
femily_ngo/
├── Home.py                    # Main entry: login + patient dashboard
├── pages/
│   ├── 0_Profile.py           # Patient profile (Femily style + NGO health records)
│   ├── 1_Calendar.py          # Appointment calendar & tracker
│   ├── 2_Chatbot.py           # AI symptom chatbot (Ollama LLM + ChromaDB)
│   ├── 3_Volunteer.py         # Volunteer search & case management dashboard
│   └── 4_Emergency.py         # Emergency contacts & volunteer alert
├── src/
│   ├── core/
│   │   ├── api.py             # LangChain RetrievalQA chain (Ollama LLM)
│   │   └── backend.py         # Risk assessment triage logic
│   ├── db/
│   │   └── db.py              # ChromaDB vector store (init, CRUD, search)
│   └── ui/
│       └── styles.py          # Shared Femily CSS + sidebar/topbar helpers
├── users.csv                  # Patient & volunteer seed data
├── requirements.txt
└── .env                       # (create this — see below)
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install and start Ollama
```bash
# Install: https://ollama.com
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama serve
```

### 3. Create .env file
```
OPENAI_API_KEY=ollama
```

### 4. Run the app
```bash
streamlit run Home.py
```

---

## Login

| Role      | Sample IDs                         |
|-----------|------------------------------------|
| Patient   | `p_001`, `p_002`, `p_003`, `p_004`, `p_005` |
| Volunteer | `v_001`, `v_002`                   |

**Patients** see: Home Dashboard, AI Chatbot, Calendar, Profile, Emergency  
**Volunteers** see: Search Dashboard with risk stats and patient records

---

## Features

| Feature | Description |
|---------|-------------|
| 🔐 **Login** | Role-aware login (patient / volunteer) with ChromaDB lookup |
| 🏠 **Home** | Pregnancy week tracker, health tips, appointment reminders |
| 💬 **AI Chatbot** | Symptom assessment powered by local Ollama LLM |
| 📅 **Calendar** | Appointment tracker with visual monthly calendar |
| 👤 **Profile** | Personal details, medical info, health record history |
| 🚨 **Emergency** | Warning signs guide, volunteer alert system |
| 👩‍⚕️ **Volunteer** | Patient search, risk stats, case escalation |

---

## Notes

- The app uses **Ollama running locally** — no external API calls for the LLM
- ChromaDB persists data in the `ngo_db/` folder (auto-created)
- To add more users, edit `users.csv` and delete the `ngo_db/` folder to reload

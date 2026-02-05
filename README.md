
# 🎭 DesiCharacters Backend  
> The official backend server and API for **DesiCharactersAI** — an AI-driven chat experience featuring vibrant, culturally inspired personalities.

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-v0.3.25-blue?style=flat&logo=langchain&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Server-Uvicorn-lightgrey?logo=uvicorn)
![Gemini](https://img.shields.io/badge/LLM-Gemini_2.0-orange?logo=google)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🧠 Tech Stack

| 🧩 Layer | ⚙️ Technology |
|:--|:--|
| **Backend** | FastAPI (Python) + Langchain |
| **LLM** | Gemini 2.5 Flash |
| **Server** | Uvicorn |

---

## ⚙️ Backend Overview

### 🔍 Highlights
- **`main.py`** — Core API endpoints and backend server logic  
- **`requirements.txt`** — Python dependency list  
- **`characters.json`** — Character configuration and metadata  
- **`.env.example`** — Template for environment variables  

---

### 🔌 API Endpoints

> The backend supports both **REST endpoints** and a **WebSocket** for real-time chat.

| 🔗 Endpoint | 🧭 Method | 📝 Description |
|:--|:--|:--|
| `/chat` | `POST` | _Deprecated — use WebSocket for real-time chat (kept for testing)._ |
| `/summary` | `GET` | Generate conversation summaries using tiered summarization. |
| `/characters` | `GET` | Retrieve available characters and their metadata. |
| `/ws/{character_id}` | `WEBSOCKET` | Real-time chat with persistent context for the selected character. |

💡 Example JSON Response — `localhost:8000/characters`

```json
[
  {
    "id": "aisha",
    "name": "Aisha",
    "persona": "Empathetic writer from Mumbai",
    "language": "English/Hindi"
  },
  {
    "id": "rahul",
    "name": "Rahul",
    "persona": "Playful stand-up comic with desi flair",
    "language": "Hinglish"
  }
]
````

---

## ⚙️ Setup & Installation

### 🧰 Prerequisites

* 🐍 **Python 3.8+**
* 🔑 A **Gemini API Key** from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key)

---

### 🪄 1. Clone the Repository

```bash
git clone https://github.com/zuno10/DesiCharacters-BackendAPI/
cd desicharacters-backend
```

---

### 🔐 2. Configure Your Environment

Create a `.env` file in the `backend/` directory and add your Gemini key:

```bash
# backend/.env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

---

### 🧠 3. Install Dependencies & Run

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Once started, your API should be running at **[http://localhost:8000](http://localhost:8000)**

---

### 🧪 4. Test Your Setup

```bash
curl http://localhost:8000/characters
```

If you see character data in your terminal, everything’s working ✅

---

## 🚀 Future Roadmap

| 🧩 Area           | 💡 Planned Enhancements                                                      |
| :---------------- | :--------------------------------------------------------------------------- |
| **Customization** | In-app UI for creating & editing characters                                  |
| **Persistence**   | Optional **cloud sync (MongoDB / Supabase)** — default remains browser-local |
| **RAG** | adding web searching tools to provide relevent information |

---

## 🤝 Contributing

We love contributions! ✨
Whether it’s adding a character, improving backend logic, or fixing a bug:

1. 🍴 **Fork** the repo
2. 🌿 **Create a branch**

   ```bash
   git checkout -b feature/YourFeature
   ```
3. 💾 **Commit changes**

   ```bash
   git commit -m "Add YourFeature"
   ```
4. 🚀 **Push & open a Pull Request**

---

## 📜 License

This project is licensed under the **MIT License** — see [`LICENSE`](./LICENSE) for details.

---

## 💬 Acknowledgements

Built with ❤️ using **FastAPI**, **Gemini**, **Langchain**, and **Uvicorn**.
Inspired by the creativity and warmth of **South Asian storytelling**.

---

> 🧭 *Maintained by [Shrikrishna2000](https://github.com/Shrikrishna2000) — open for collaboration and feedback!*

<!-- ─────────────────────────────────────────────────────────── -->

```

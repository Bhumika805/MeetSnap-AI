# ⚡ MeetSnap AI — Meeting Intelligence Platform

> **Microsoft Build AI Hackathon 2026** · Theme: *AI at Work: Productivity & Teamwork Reimagined*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)
![GPT-4o](https://img.shields.io/badge/GPT--4o-GitHub%20Models-black?style=flat-square&logo=openai)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Problem Statement

Professionals waste **31+ hours per month** in unproductive meetings. Action items get lost in chat threads. Decisions are never documented. 
New team members have zero context from past discussions.

> **MeetSnap AI solves this — paste any meeting transcript and get instant AI-powered intelligence in under 10 seconds.**

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **Smart Summary** | 2-3 sentence AI brief of the entire meeting |
| **Action Item Extraction** | Auto-extracts tasks with owner names and deadlines |
| **Decision Logging** | Captures every decision made during the meeting |
| **Blocker Detection** | Flags risks and blockers raised by the team |
| **Sentiment Analysis** | Positive / Neutral / Mixed / Negative team health signal |
| **RAG-based Chat** | Ask anything about your meeting — context-aware AI answers |
| **Multi-Meeting Compare** | Analyze 2 meetings side by side and track progress |
| **Export Summary** | Download meeting report as a .txt file |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                            │
│         Meeting Transcript (paste or type)               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│               FASTAPI BACKEND                            │
│                                                          │
│  /api/analyze ──► Prompt Engineering ──► GPT-4o          │
│                   (Summary, Tasks,                       │
│                    Decisions, Sentiment)                 │
│                                                          │
│  /api/chat ──► RAG Pipeline                              │
│                ├─ Chunk transcript                       │
│                ├─ Keyword search                         │
│                ├─ Retrieve relevant context              │
│                └─ GPT-4o generates answer                │
│                                                          │
│  /api/meetings ──► Meeting history store                 │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (HTML/CSS/JS)                 │
│  Dashboard · Summary Panel · Chat Interface · Compare   │
└─────────────────────────────────────────────────────────┘
```

---

## 🧰 Tech Stack

### Microsoft AI Stack ✅
| Technology | Usage |
|---|---|
| **GitHub Models — GPT-4o** | Core AI engine — summarization, extraction, Q&A |
| **GitHub Copilot** | AI-assisted development throughout |
| **GitHub Actions** | CI/CD pipeline (future) |

### Backend
| Technology | Usage |
|---|---|
| **Python 3.10+** | Core language |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **python-dotenv** | Environment management |

### Frontend
| Technology | Usage |
|---|---|
| **HTML5 + CSS3 + JS** | Single-page application |
| **Fetch API** | Real-time backend communication |

---

## 🤖 RAG Pipeline

MeetSnap AI implements a lightweight **Retrieval Augmented Generation** pipeline:

```
Transcript Input
      │
      ▼
  Chunking (200 words/chunk)
      │
      ▼
  In-memory Store (multiple meetings)
      │
      ▼
  Keyword Search (question → relevant chunks)
      │
      ▼
  Context Assembly
      │
      ▼
  GPT-4o Answer Generation
      │
      ▼
  Context-aware Response
```

> **Production Roadmap:** Azure AI Search + vector embeddings for semantic retrieval at scale.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- GitHub Account (for API token)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/meetsnap-ai.git
cd meetsnap-ai
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Create app/.env file
GITHUB_TOKEN=your_github_personal_access_token
```

> **Get your token:** github.com → Settings → Developer Settings → Personal Access Tokens → Classic → Generate (select `read:packages`)

### 5. Run the application
```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Open in browser
```
http://localhost:8000
```

---

## 📁 Project Structure

```
meetsnap/
├── app/
│   ├── main.py          # FastAPI backend — all routes + RAG pipeline
│   ├── .env             # Environment variables (not committed)
│   └── __init__.py
├── static/
│   └── index.html       # Complete frontend — dashboard + chat + compare
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

---

## 🎯 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | Analyze transcript → returns summary, tasks, decisions |
| `POST` | `/api/chat` | RAG-powered Q&A about meeting |
| `GET` | `/api/meetings` | List all analyzed meetings |
| `GET` | `/api/health` | Health check + model info |
| `GET` | `/docs` | Interactive Swagger API docs |

---

## 📊 Demo

### Sample transcript to test:
```
Alice: Let's start sprint planning for v2.4.
Bob: I've finished the auth module, ready to merge.
Alice: Great. Can we ship by Friday?
Carol: UI should be ready. I need final designs by Wednesday.
Bob: Backend is done. Only blocker is DB migration approval from DevOps.
Alice: I'll ping DevOps today. Carol owns UI, Bob owns migration plan by EOD.
Alice: Also confirming — analytics dashboard moves to v2.5. Final decision.
```

### What MeetSnap AI returns:
```json
{
  "summary": "Sprint v2.4 planning completed. Team aligned on Friday release...",
  "decisions": ["Analytics dashboard moved to v2.5"],
  "action_items": [
    {"task": "Ping DevOps for DB migration", "owner": "Alice", "due": "Today"},
    {"task": "Complete UI delivery", "owner": "Carol", "due": "Wednesday"},
    {"task": "Write migration plan", "owner": "Bob", "due": "EOD"}
  ],
  "blockers": ["DB migration approval pending from DevOps"],
  "sentiment": "positive"
}
```

---

## 🗺️ Future Roadmap

- [ ] **Azure OpenAI** integration for enterprise deployment
- [ ] **Azure AI Search** for vector-based RAG at scale
- [ ] **Azure Speech Services** for direct audio file transcription
- [ ] **Azure DevOps** integration for auto task creation
- [ ] **Multi-language** support
- [ ] **Teams/Slack** bot integration

---

## 🛠️ AI Tools Used

As per hackathon guidelines, all AI tools used are disclosed:

| Tool | Usage |
|---|---|
| **GitHub Models — GPT-4o** | Core AI engine for all intelligence features |
| **GitHub Copilot** | Code completion and development assistance |

All system architecture, prompt engineering, RAG pipeline design, UI design, and business logic represents original human creativity and engineering judgment.

---

## 👤 Team

| Name | Role |
|---|---|
| Saloni Sharma | Full-stack Developer |
| Riddhi Sharma | AI Engineer |
| Harshit Sharma | AI Engineer |
| Bhumika Sharma | Backend Developer |

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

> **Built for Microsoft Build AI Hackathon 2026**
> Theme: *AI at Work: Productivity & Teamwork Reimagined*
> Powered by GitHub Models GPT-4o + FastAPI

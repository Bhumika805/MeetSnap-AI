from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os, json

load_dotenv(dotenv_path="app/.env")

app = FastAPI(title="MeetSnap AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── GitHub Models GPT-4o client ──────────────────────────────────────────
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)
DEPLOYMENT = "gpt-4o"

# ── Simple RAG store — multiple meetings memory ──────────────────────────
meeting_store = []  # list of {title, chunks, full_text}
last_transcript = {"text": "", "title": ""}


# ── RAG Helper functions ─────────────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = 200) -> list[str]:
    """
    Transcript ko chhote chhote chunks mein todo.
    Har chunk ~200 words ka hoga.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def simple_search(question: str, chunks: list[str], top_k: int = 3) -> list[str]:
    """
    Simple keyword-based search — question ke words chunks mein dhundho.
    Production mein ye Azure AI Search + vectors se hoga.
    """
    question_words = set(question.lower().split())
    
    # Har chunk ko score karo — kitne words match karte hain
    scored = []
    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(question_words & chunk_words)  # intersection
        scored.append((score, chunk))
    
    # Top scoring chunks return karo
    scored.sort(reverse=True)
    return [chunk for score, chunk in scored[:top_k] if score > 0]


def get_relevant_context(question: str) -> str:
    """
    Saare stored meetings mein se relevant chunks nikalo.
    """
    if not meeting_store:
        return ""
    
    all_relevant = []
    for meeting in meeting_store[-5:]:  # last 5 meetings
        relevant = simple_search(question, meeting["chunks"])
        if relevant:
            all_relevant.append(
                f"[From: {meeting['title']}]\n" + "\n".join(relevant)
            )
    
    return "\n\n---\n\n".join(all_relevant)


# ── Models ───────────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    title: str
    transcript: str


class ChatRequest(BaseModel):
    question: str


# ── Route 1: Analyze ─────────────────────────────────────────────────────
@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    if len(req.transcript.strip()) < 30:
        raise HTTPException(400, "Transcript too short")

    # Save for chat
    last_transcript["text"] = req.transcript
    last_transcript["title"] = req.title

    # RAG: chunks banao aur store karo
    chunks = chunk_text(req.transcript)
    meeting_store.append({
        "title": req.title,
        "chunks": chunks,
        "full_text": req.transcript
    })

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0.1,
        max_tokens=1200,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a meeting analyst. Return ONLY a raw JSON object. "
                    "No markdown. No backticks. No explanation. No extra text. "
                    "Start your response with { and end with }.\n\n"
                    "IMPORTANT: For owner field, always write a person's name from the transcript. "
                    "If no name mentioned, write 'Team' not null. Never use null or None.\n\n"
                    "JSON shape:\n"
                    '{"summary": "2-3 sentence overview", '
                    '"decisions": ["decision 1"], '
                    '"action_items": [{"task": "task", "owner": "person", "due": "deadline"}], '
                    '"blockers": ["blocker"], '
                    '"sentiment": "positive or neutral or mixed or negative"}'
                ),
            },
            {
                "role": "user",
                "content": f"Meeting: {req.title}\n\nTranscript:\n{req.transcript}",
            },
        ],
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start != -1 and end > start:
            raw = raw[start:end]
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "summary": raw[:300] if raw else "Could not analyze",
            "decisions": [],
            "action_items": [],
            "blockers": [],
            "sentiment": "neutral"
        }


# ── Route 2: RAG Chat ─────────────────────────────────────────────────────
@app.post("/api/chat")
def chat(req: ChatRequest):
    if not last_transcript["text"]:
        return {"answer": "Please analyze a meeting first!"}

    # RAG: relevant context dhundho
    rag_context = get_relevant_context(req.question)

    # Agar RAG context mila toh use karo, warna full transcript
    if rag_context:
        context = f"Relevant meeting context:\n{rag_context}"
    else:
        context = f"Meeting: {last_transcript['title']}\n\nTranscript:\n{last_transcript['text']}"

    response = client.chat.completions.create(
        model=DEPLOYMENT,
        temperature=0.3,
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are MeetSnap AI. Answer questions about meetings accurately. "
                    "Use the provided context to answer. "
                    "If answer is not in context, say so honestly. "
                    "Be concise and specific."
                ),
            },
            {
                "role": "user",
                "content": f"{context}\n\nQuestion: {req.question}"
            },
        ],
    )

    return {
        "answer": response.choices[0].message.content,
        "rag_chunks_used": len(rag_context.split("---")) if rag_context else 0
    }


# ── Route 3: Meeting history ──────────────────────────────────────────────
@app.get("/api/meetings")
def get_meetings():
    """Kitni meetings analyze hui hain."""
    return {
        "total": len(meeting_store),
        "meetings": [{"title": m["title"], "chunks": len(m["chunks"])}
                     for m in meeting_store]
    }


# ── Health check ──────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model": DEPLOYMENT,
        "meetings_indexed": len(meeting_store)
    }


app.mount("/", StaticFiles(directory="static", html=True), name="static")
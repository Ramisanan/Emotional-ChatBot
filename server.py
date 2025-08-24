# server.py
import os, re
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx

# --- Fixed backend settings (kept server-side only) ---
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL      = os.getenv("MODEL", "llama3.1")
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://127.0.0.1:8000,http://localhost:8000"
).split(",")

AGENTS = {
    "emotional_support": (
        "You are an empathetic peer-support chatbot. Not a therapist. "
        "Listen, reflect feelings, ask gentle open-ended questions, offer simple coping ideas. "
        "2–4 sentences per reply, warm and plain. Never medical advice."
    ),
    "coach": (
        "You are a motivational coach. Use SMART micro-goals and give 1–2 next steps. "
        "Be concise and encouraging."
    ),
}

CRISIS_RX = re.compile(
    r"(suicide|kill myself|end my life|i want to die|self[-\s]?harm|hurt myself|overdose|can't go on|kill (him|her|them)|hurt (him|her|them))",
    re.IGNORECASE,
)

class Turn(BaseModel):
    role: str
    content: str

class ChatIn(BaseModel):
    messages: List[Turn]
    agent: Optional[str] = None

class ChatOut(BaseModel):
    reply: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=ChatOut)
async def chat(req: ChatIn):
    # Crisis check
    recent_text = " ".join([t.content for t in req.messages[-2:]]) if req.messages else ""
    if CRISIS_RX.search(recent_text):
        return ChatOut(
            reply=("I'm really glad you told me. If you're in immediate danger, call 911 now. "
                   "In the U.S., you can also call or text 988 for the Suicide & Crisis Lifeline. "
                   "If you're outside the U.S., please contact your local emergency number.")
        )

    messages = []
    if req.agent and req.agent in AGENTS:
        messages.append({"role": "system", "content": AGENTS[req.agent]})
    for t in req.messages:
        if t.role in ("user", "assistant"):
            messages.append({"role": t.role, "content": t.content})

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={"model": MODEL, "messages": messages, "stream": False},
            )
            r.raise_for_status()
            data = r.json()
            content = (
                (data.get("message") or {}).get("content")
                or (data.get("choices", [{}])[0].get("message") or {}).get("content")
                or ""
            ).strip()
            return ChatOut(reply=content or "(No content)")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

# Serve static site from ./site
app.mount("/", StaticFiles(directory="site", html=True), name="site")

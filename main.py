# ==============================
# main.py — Shunya Sensei (FINAL)
# ==============================

import os
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import google.generativeai as genai

from modes import BASE_PERSONA, mode_instructions
from mood import detect_mood
from google_fallback import google_fallback_answer


# ---------- ENV ----------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing")


# ---------- Gemini Setup ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.0-pro")


# ---------- Cooldown ----------
GEMINI_BLOCKED_UNTIL = 0


# ---------- FastAPI ----------
app = FastAPI(title="Shunya Sensei API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Prompt ----------
def make_system_prompt(mode: str) -> str:
    instruction = mode_instructions.get(mode, "")
    return BASE_PERSONA + "\n" + instruction


# ---------- Gemini ----------
def ask_gemini(mode: str, text: str) -> str:
    print("🟢 Trying Gemini...")
    response = model.generate_content(
        make_system_prompt(mode) + "\n" + text
    )
    print("🟢 Gemini SUCCESS")
    return response.text


# ---------- Smart Router ----------
def safe_ask(mode: str, text: str):
    global GEMINI_BLOCKED_UNTIL
    now = time.time()

    if now >= GEMINI_BLOCKED_UNTIL:
        try:
            reply = ask_gemini(mode, text)
            return reply, "gemini"
        except Exception as e:
            print("🔴 Gemini FAILED:", str(e))
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                GEMINI_BLOCKED_UNTIL = now + 120

    return google_fallback_answer(text), "google"


# ================= API =================

class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "teacher"


@app.post("/chat")
def chat_api(req: ChatRequest):
    mode = req.mode or "teacher"
    reply, source = safe_ask(mode, req.message)
    emoji = detect_mood(req.message)

    return {
        "reply": f"{emoji} {reply}",
        "source": source
    }



# ================= ENTRY =================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000))
    )

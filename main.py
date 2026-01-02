# ==============================
# main.py — Shunya Sensei (HF)
# ==============================

import os
import requests
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from duckduckgo_search import DDGS

from modes import BASE_PERSONA, mode_instructions

# ---------- ENV ----------
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# ---------- APP ----------
app = FastAPI(
    title="Shunya Sensei API",
    version="2.0"
)

# ---------- MODEL ----------
class ChatRequest(BaseModel):
    text: str
    mode: Optional[str] = "teacher"

# ---------- PROMPT ----------
def make_system_prompt(mode: str) -> str:
    return BASE_PERSONA + "\n" + mode_instructions.get(mode, "")

# ---------- HF ----------
def ask_hf(prompt: str) -> Optional[str]:
    if not HF_API_KEY:
        return None

    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.4
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code != 200:
            return None

        data = res.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        return None
    except Exception:
        return None

# ---------- DUCKDUCKGO ----------
def ask_duckduckgo(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "😐 No useful data found."

        ans = ""
        for r in results:
            ans += f"- {r.get('body','')}\n"
        return ans
    except Exception:
        return "⚠️ DuckDuckGo failed."

# ---------- SAFE ASK ----------
def safe_ask(mode: str, text: str) -> str:
    system_prompt = make_system_prompt(mode)
    full_prompt = f"{system_prompt}\n\nQuestion:\n{text}\n\nAnswer:"

    hf_answer = ask_hf(full_prompt)
    if hf_answer:
        return hf_answer.strip()

    # fallback
    ddg = ask_duckduckgo(text)
    return f"{system_prompt}\n\n### Answer (Search Based)\n{ddg}"

# ---------- ROUTE ----------
@app.post("/chat")
def chat(req: ChatRequest):
    reply = safe_ask(req.mode or "teacher", req.text)
    return {
        "reply": reply,
        "mode": req.mode,
        "source": "huggingface + duckduckgo"
    }

@app.get("/")
def root():
    return {"status": "Shunya Sensei running ✅"}

# Shunya Sensei

Shunya Sensei is a minimal, cloud-ready AI-style backend that answers user questions via an API.

## Features
- FastAPI backend
- huging face ai
- Question → Answer system
- DuckDuckGo based fallback logic
- No voice, no UI dependency
- Mobile & cloud friendly

## Tech Stack
- Python
- FastAPI
- DuckDuckGo Search
- Render compatible

## API
POST /chat  
Body:
{
  "message": "your question"
}

Response:
{
  "reply": "answer"
}

## Status
✅ Local server working  
🚀 Ready for cloud deployment

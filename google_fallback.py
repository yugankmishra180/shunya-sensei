# google_fallback.py
# -------------------
# Simple Google-like fallback using DuckDuckGo

from duckduckgo_search import DDGS


def google_fallback_answer(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)

            answers = []
            for r in results:
                body = r.get("body")
                if body:
                    answers.append(body)

            if answers:
                return (
                    "🔎 *Google Fallback Answer*\n\n"
                    + "\n\n".join(answers[:2])
                )

        return "🔎 Google fallback se exact answer nahi mila."

    except Exception:
        return "⚠ Google fallback temporary unavailable."

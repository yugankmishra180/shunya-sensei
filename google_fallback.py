# google_fallback.py
# -------------------
# Simple Google-like fallback using DuckDuckGo (updated for ddgs)

from ddgs import DDGS  # updated import

def google_fallback_answer(query: str) -> str:
    """
    Returns top 2 DuckDuckGo results as fallback answer.
    """
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

    except Exception as e:
        print("⚠ Google fallback error:", e)
        return "⚠ Google fallback temporary unavailable."

import httpx
from ..config import GEMINI_API_KEY, GEMINI_MODEL

async def gemini_text(prompt: str):
    if not GEMINI_API_KEY:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4}}
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            r = await client.post(url, headers={"x-goog-api-key": GEMINI_API_KEY}, json=body)
            r.raise_for_status()
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None

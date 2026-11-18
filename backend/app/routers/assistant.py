from fastapi import APIRouter
from pydantic import BaseModel
from ..services.llm import gemini_text
router = APIRouter()
class ChatRequest(BaseModel):
    message: str
    farm_context: dict = {}
    language: str = "en"

@router.post("/assistant/chat")
async def chat(req: ChatRequest):
    prompt = f"Answer as a cautious agriculture assistant. Do not invent measurements or chemical dosages. Language {req.language}. Farm context: {req.farm_context}. Question: {req.message}"
    answer = await gemini_text(prompt)
    return {"source": "AI (Gemini)" if answer else "Offline fallback",
            "answer": answer or "AI service is not configured or unavailable. Please consult the crop guides and local agricultural extension service; you can still use the rule-based tools."}

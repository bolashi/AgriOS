from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from ..config import MAX_UPLOAD_MB
from ..schemas import ExplainRequest
from ..services.llm import gemini_text

router = APIRouter()

@router.post("/detect")
async def detect(image: UploadFile = File(...), crop_hint: str | None = Form(None)):
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, "Upload a JPEG, PNG, or WebP image.")
    raw = await image.read()
    if len(raw) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, f"Image exceeds {MAX_UPLOAD_MB} MB.")
    try:
        pic = Image.open(BytesIO(raw))
        pic.verify()
        pic = Image.open(BytesIO(raw))
    except (UnidentifiedImageError, OSError):
        raise HTTPException(400, "Invalid image file.")
    if min(pic.size) < 32:
        raise HTTPException(400, "Image dimensions must be at least 32x32.")
    from ..main import registry
    try:
        return registry.predict(pic, crop_hint)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))

@router.post("/detect/explain")
async def explain(req: ExplainRequest):
    prompt = (f"Explain this fixed plant image classification; do not change it. Crop: {req.crop}. "
              f"Classification: {req.disease}. Healthy: {req.healthy}. Language: {req.language}. "
              "Use sections Explanation, Symptoms, Causes, Treatment, Prevention, Next steps. "
              "Never invent pesticide brands or chemical dosages. Include safety precautions.")
    answer = await gemini_text(prompt)
    if answer:
        return {"source": "AI (Gemini)", "guidance": answer}
    return {"source": "Rule-based", "guidance":
            "Explanation: This is a model classification, not a confirmed field diagnosis.\n"
            "Symptoms: Compare visible symptoms with the crop in the field.\n"
            "Causes: Conditions vary; confirm with a local agriculture specialist.\n"
            "Treatment: Do not apply chemicals based only on this result.\n"
            "Prevention: Use clean tools and monitor nearby plants.\n"
            "Next steps: Take clear photos and seek local expert confirmation."}

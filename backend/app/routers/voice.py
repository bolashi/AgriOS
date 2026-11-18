from fastapi import APIRouter, UploadFile, File, HTTPException
router = APIRouter()
@router.post("/voice")
async def voice(audio: UploadFile = File(...)):
    data = await audio.read()
    if not data:
        raise HTTPException(400, "Empty audio upload.")
    return {"available": False, "message": "Voice transcription is not configured in this starter build. Your recording was received; use the typed assistant as fallback."}

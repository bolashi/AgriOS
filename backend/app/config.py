from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path

MODEL_ID = os.getenv("MODEL_ID", "Daksh159/plant-disease-mobilenetv2")
CONFIDENCE_THRESHOLD = float(os.getenv("MODEL_CONFIDENCE_THRESHOLD", "0.55"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
SKIP_MODEL = os.getenv("AGRIOS_SKIP_MODEL", "0") == "1"
HF_HOME = os.getenv("HF_HOME", str(Path.home() / ".cache" / "huggingface"))

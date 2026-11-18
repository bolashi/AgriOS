import json
import os
import threading
from pathlib import Path
from PIL import Image
from .labels import parse_label, disease_type
from ..config import MODEL_ID, CONFIDENCE_THRESHOLD, SKIP_MODEL

SUPPORTED_CROPS = ["Apple", "Blueberry", "Cherry", "Corn", "Grape", "Orange", "Peach", "Pepper", "Potato", "Raspberry", "Soybean", "Squash", "Strawberry", "Tomato"]
ALIASES = {"maize": "corn", "chili": "pepper", "chilli": "pepper", "citrus": "orange", "chili family": "pepper"}

def canonical(value):
    name = value.lower().strip()
    return ALIASES.get(name, name)

class ModelRegistry:
    def __init__(self):
        self.status = "skipped" if SKIP_MODEL else "loading"
        self.error = None
        self.model = self.transform = None
        self.labels = json.loads((Path(__file__).parent / "class_names.json").read_text(encoding="utf-8"))
        self.label_source = "local PlantVillage ImageFolder alphabetical convention (verify against original training code)"
        if not SKIP_MODEL:
            threading.Thread(target=self._load, daemon=True).start()

    def _load(self):
        try:
            import torch
            from torch import nn
            from torchvision import models, transforms
            from huggingface_hub import hf_hub_download
            torch.set_num_threads(int(os.getenv("TORCH_THREADS", "2")))
            checkpoint = hf_hub_download(repo_id=MODEL_ID, filename="mobilenetv2_plant.pth")
            model = models.mobilenet_v2(weights=None)
            model.classifier[1] = nn.Sequential(nn.Dropout(0.2), nn.Linear(model.classifier[1].in_features, 38))
            state = torch.load(checkpoint, map_location="cpu", weights_only=True)
            if isinstance(state, dict) and "state_dict" in state:
                state = state["state_dict"]
            if not isinstance(state, dict):
                raise RuntimeError("Checkpoint does not contain a state_dict")
            model.load_state_dict(state, strict=True)
            model.eval()
            transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(),
                                            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
            self.model, self.transform = model, transform
            self.status = "ready"
        except Exception as exc:
            self.error = str(exc)
            self.status = "error"

    def info(self):
        return {"id": MODEL_ID, "status": self.status, "error": self.error,
                "classes": self.labels, "supported_crops": SUPPORTED_CROPS,
                "label_source": self.label_source,
                "limitations": ["Class-index order must be verified against original training code",
                                "Model predictions are not confirmed diagnoses", "Only the 14 listed crop types are supported"]}

    def predict(self, image: Image.Image, crop_hint: str | None = None):
        if self.status != "ready":
            raise RuntimeError(f"Model is {self.status}: {self.error or 'weights not ready'}")
        import torch
        with torch.inference_mode():
            logits = self.model(self.transform(image.convert("RGB")).unsqueeze(0))[0]
            probs = torch.softmax(logits, dim=0)
            vals, indices = torch.topk(probs, min(5, len(self.labels)))
        top = [{"label": self.labels[int(i)], "score": float(v)} for v, i in zip(vals, indices)]
        predicted_crop, disease = parse_label(top[0]["label"])
        score = top[0]["score"]
        margin = score - (top[1]["score"] if len(top) > 1 else 0)
        if crop_hint and canonical(crop_hint) not in [canonical(c) for c in SUPPORTED_CROPS]:
            return {"crop": crop_hint, "disease": "Unsupported crop", "healthy": False, "type": "unsupported", "confidence": 0.0, "uncertain": True, "unsupported": True, "warnings": ["unsupported_crop"], "top": [], "message": "This model does not support the selected crop."}
        if crop_hint and canonical(crop_hint) != canonical(predicted_crop):
            return {"crop": crop_hint, "disease": "Crop mismatch — no diagnosis", "healthy": False, "type": "mismatch", "confidence": 0.0, "uncertain": True, "unsupported": False, "warnings": ["crop_mismatch"], "top": top, "model_guess": f"{predicted_crop}: {disease}", "message": "The highest-scoring model class belongs to another crop. Please check the image and selected crop."}
        uncertain = score < CONFIDENCE_THRESHOLD or margin < 0.15
        warnings = (["low_confidence"] if score < CONFIDENCE_THRESHOLD else []) + (["low_margin"] if margin < 0.15 else [])
        return {"crop": predicted_crop, "disease": disease, "healthy": disease_type(disease) == "healthy",
                "type": disease_type(disease), "confidence": score, "uncertain": uncertain,
                "unsupported": False, "warnings": warnings, "top": top, "message": None}

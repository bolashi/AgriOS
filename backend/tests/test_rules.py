from app.services.rules import irrigation_status
from app.services.labels import parse_label, disease_type
from app.services.model_registry import _normalise_crop, SUPPORTED_CROPS

def test_irrigation_unknown_without_manual_moisture():
    assert irrigation_status(None, 0, 30)["status"] == "unknown"

def test_irrigation_skip_after_rain():
    assert irrigation_status(35, 20, 28)["status"] == "skip"

def test_label_parsing():
    assert parse_label("Tomato___Late_blight") == ("Tomato", "Late Blight")
    assert parse_label("Corn_(maize)___Common_rust_")[0] == "Maize"

def test_disease_type():
    assert disease_type("Tomato___healthy") == "healthy"


def test_wheat_is_not_claimed_as_supported_by_current_model():
    assert _normalise_crop("Wheat") not in SUPPORTED_CROPS

def test_maize_and_chili_aliases_match_model_labels():
    assert _normalise_crop("Corn") == _normalise_crop("Maize")
    assert _normalise_crop("Chili") == _normalise_crop("Chili family")

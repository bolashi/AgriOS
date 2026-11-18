import json
from pathlib import Path
from app.services.labels import parse_label
from app.services.model_registry import SUPPORTED_CROPS

def test_supported_crops():
    assert len(SUPPORTED_CROPS) == 14
    assert "Strawberry" in SUPPORTED_CROPS

def test_label_count_and_order():
    labels = json.loads((Path(__file__).parents[1] / "app/services/class_names.json").read_text())
    assert len(labels) == 38
    assert labels == sorted(labels)

def test_strawberry():
    assert parse_label("Strawberry___Leaf_scorch") == ("Strawberry", "Leaf Scorch")

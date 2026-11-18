"""Parse plant-disease class labels from common PlantVillage model formats."""

import re


def _clean_name(value: str) -> str:
    value = value.replace("_", " ").replace(",", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value.title()


def _canonical_crop(value: str) -> str:
    crop = _clean_name(value)
    key = crop.casefold()
    aliases = {
        "corn": "Maize",
        "maize": "Maize",
        "corn (maize)": "Maize",
        "cherry (including sour)": "Cherry",
        "pepper bell": "Pepper",
        "pepper bell plant": "Pepper",
        "orange": "Orange",
    }
    return aliases.get(key, crop)


def parse_label(label: str) -> tuple[str, str]:
    """Return (crop, disease) for labels such as:

    * ``Potato___Late_blight``
    * ``Potato With Late Blight``
    * ``Corn_(maize)___Common_rust``
    * ``Pepper,_bell___Bacterial_spot``

    Unknown formats are preserved as a crop with disease ``Unknown`` rather
    than guessed, so crop-mismatch checks remain conservative.
    """
    raw = str(label or "").strip()
    if not raw:
        return "Unknown", "Unknown"

    if "___" in raw:
        crop_raw, disease_raw = raw.split("___", 1)
    else:
        # Some model repositories publish human-readable labels rather than
        # PlantVillage's triple-underscore convention.
        match = re.match(r"^(.+?)\s+with\s+(.+)$", raw, flags=re.IGNORECASE)
        if match:
            crop_raw, disease_raw = match.group(1), match.group(2)
        else:
            healthy_match = re.match(
                r"^healthy\s+(.+?)\s+plant$", raw, flags=re.IGNORECASE
            )
            if healthy_match:
                crop_raw, disease_raw = healthy_match.group(1), "healthy"
            else:
                return _canonical_crop(raw), "Unknown"

    crop = _canonical_crop(crop_raw.replace("(maize)", "").strip())
    disease = _clean_name(disease_raw)
    if disease.casefold() in {"healthy", "healthy plant"}:
        disease = "Healthy"
    return crop, disease or "Unknown"


def disease_type(disease: str) -> str:
    d = disease.lower()
    if "healthy" in d:
        return "healthy"
    if any(x in d for x in ("virus", "mosaic", "yellow leaf curl")):
        return "viral"
    if any(x in d for x in ("bacterial", "bacteria")):
        return "bacterial"
    if any(x in d for x in ("mite", "pest", "spider")):
        return "pest"
    return "fungal"

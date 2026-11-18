def irrigation_status(moisture: float | None, rainfall_48h: float, temperature: float,
                      stage_factor: float = 1.0) -> dict:
    if moisture is None:
        return {"status": "unknown", "suggested_mm": None, "reason": "Add a manual soil-moisture reading."}
    if rainfall_48h >= 12 and moisture >= 30:
        return {"status": "skip", "suggested_mm": 0, "reason": "Recent forecast rainfall and moisture suggest delaying irrigation."}
    if moisture < 18 or temperature >= 36:
        mm = round(18 * stage_factor, 1)
        return {"status": "urgent", "suggested_mm": mm, "reason": "Low reported moisture or high temperature; verify the field before watering."}
    if moisture < 28:
        return {"status": "due", "suggested_mm": round(12 * stage_factor, 1), "reason": "Reported moisture is below the guidance threshold."}
    return {"status": "ok", "suggested_mm": 0, "reason": "Reported moisture is currently adequate."}

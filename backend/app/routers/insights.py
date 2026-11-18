from fastapi import APIRouter
from ..schemas import WeatherInsightRequest
router = APIRouter()

@router.post("/insights/weather")
async def weather_insights(req: WeatherInsightRequest):
    risks = []
    if req.temperature >= 38: risks.append("High temperature: check crop heat stress and irrigation.")
    if req.humidity >= 85: risks.append("High humidity: monitor crops for fungal disease symptoms.")
    if req.rainfall_48h >= 20: risks.append("Heavy forecast rainfall: check drainage and delay unnecessary watering.")
    return {"source": "Rule-based", "risks": risks or ["No threshold-based weather risk detected."]}

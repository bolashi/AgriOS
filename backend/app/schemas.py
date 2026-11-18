from pydantic import BaseModel, Field

class ExplainRequest(BaseModel):
    crop: str
    disease: str
    healthy: bool = False
    language: str = "en"

class WeatherInsightRequest(BaseModel):
    temperature: float
    humidity: float
    rainfall_48h: float = 0
    wind_speed: float = 0

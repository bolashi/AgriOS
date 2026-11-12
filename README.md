# AgriOS — Smart Farm Management

AgriOS is a Streamlit farm-management dashboard with crop planning, soil and nutrient guidance, irrigation planning, crop-health screening, weather-risk views, resource costing and decision support.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push `app.py` and `requirements.txt` to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the main file path to `app.py`.

## Included modules

- Farm overview dashboard and field indicators
- Crop planning and growth-stage task planner
- Soil and nutrient guidance
- Rule-based irrigation planning
- Crop-health screening with image upload and symptom-guided recommendations
- Weather-risk dashboard
- Farm resource and input-cost planner
- Education and training scenarios
- Combined decision-support workspace
- Urdu, Sindhi and English interface selector
- Voice assistant screen with audio capture

## Current system capabilities

- Crop-health results are based on the selected crop and symptom. The uploaded image is displayed for reference but is **not** classified by a trained image-recognition model.
- Weather, sensor and forecast values are example values until a live data provider is connected.
- Soil and irrigation guidance uses simple rules and is not a calibrated agronomic prescription.
- Voice recording is captured by Streamlit, but speech-to-text and text-to-speech are not connected.
- Farm data is held in session state; persistent storage, authentication and audit logs are not implemented.

For operational farm use, connect validated local agronomy data, a trained and field-tested crop-health model, a weather provider, Urdu/Sindhi speech services and safety-reviewed recommendations. Confirm disease and pesticide decisions with a qualified local agricultural adviser.

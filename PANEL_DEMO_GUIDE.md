# AgriOS — 5-minute presentation flow

1. **Overview (30 sec):** Introduce AgriOS as one workspace for farm information and daily field decisions.
2. **Crop Management (40 sec):** Select a crop, growth stage and farm area, then review the task plan.
3. **Soil & Nutrients (40 sec):** Change pH and N-P-K values and generate a structured summary. Explain that results need local soil-test calibration.
4. **Irrigation (40 sec):** Change soil moisture and rain probability, then generate a planning suggestion.
5. **Crop Health Screening (60 sec):** Upload a leaf image, choose the visible symptom and start the assessment. Explain accurately that the current result is symptom-guided; the uploaded image is not classified by a trained image model.
6. **Weather + Costs (40 sec):** Review the weather-risk table and editable input-cost table.
7. **Urdu/Sindhi + Voice (40 sec):** Switch language from the sidebar. Show audio capture and explain that speech recognition and speech output need to be connected.

## Suggested explanation

“AgriOS brings farm planning, crop-health screening, irrigation, soil guidance and farm-cost tracking into one dashboard. The current crop-health assessment uses the crop and symptoms selected by the user and provides a practical action checklist. Image-based classification will require a trained and field-tested model. Weather, soil and farm recommendations also need validated local data before operational use.”

## Before presenting

- Run `streamlit run app.py` and test the main modules.
- Keep a clear leaf photo ready.
- Explain the current capabilities accurately; do not describe symptom-guided results as image-recognition predictions.

# AgriOS v0.1

A runnable starter implementation of AgriOS using React + Vite + TypeScript and FastAPI.
It includes a responsive dashboard, crop CRUD, manual soil records, irrigation estimates,
a plant-disease model integration (downloads the configured Hugging Face model on
first startup), weather lookup through Open-Meteo, and local browser persistence.

## Requirements
- Windows 10/11
- Python 3.11 (64-bit)
- Node.js 20 LTS
- Internet connection for installing dependencies, downloading the model, and weather

## Quick start
See `docs/WINDOWS_SETUP.md`. Start the backend and frontend in two VS Code terminals.

**Honesty note:** model inference requires downloading the model weights. Until the model
is ready, the API reports `loading`/`error`; it does not fabricate diagnoses. Soil readings
are manual entries and seeded examples are marked Sample. Irrigation values are estimates.
The configured PlantVillage-style disease model does not support wheat, rice, cotton,
sugarcane, onion or mango; AgriOS withholds a diagnosis for these selected crops. A
wheat-trained model is still required for genuine wheat disease detection.


**Updated disease detector:** Daksh159/plant-disease-mobilenetv2 (38 image classes, 14 crop categories). See docs/MODEL.md for the important class-index verification caveat.

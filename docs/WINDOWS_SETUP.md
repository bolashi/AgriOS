# Windows + VS Code setup

Install Python 3.11 (64-bit) and Node.js 20 LTS first.

## Backend (Terminal 1 — PowerShell)
```powershell
cd agrios\backend
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Install matching CPU PyTorch and torchvision versions first. The first model startup downloads weights and can take several minutes.

## Frontend (Terminal 2 — PowerShell)
```powershell
cd agrios\frontend
npm install
Copy-Item .env.example .env
npm run dev
```
Open the URL printed by Vite (normally http://localhost:5173).

## Troubleshooting
| Problem | Fix |
|---|---|
| `py -3.11` not found | Install Python 3.11 and enable the Python launcher |
| PowerShell blocks activation | Run the ExecutionPolicy command above in that terminal |
| `torch` install fails | Install CPU torch using the provided index URL before requirements |
| API unavailable | Start backend first; check http://127.0.0.1:8000/api/health |
| Model loading/error | Check internet, disk space, and backend terminal output |
| Weather unavailable | Check internet; Open-Meteo is an external service |

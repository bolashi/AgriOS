# Testing

Backend rules tests:
```powershell
cd backend
$env:AGRIOS_SKIP_MODEL="1"
pytest
```
API smoke check:
```powershell
python scripts/smoke_test.py
```
The smoke test checks health and rule endpoints. Real image inference must be tested
separately after the model has downloaded; it is not claimed as passed by this scaffold.

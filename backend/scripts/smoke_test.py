import urllib.request, json
url = "http://127.0.0.1:8000/api/health"
with urllib.request.urlopen(url, timeout=10) as r:
    data = json.loads(r.read())
print("Health endpoint:", data)
assert data["status"] == "ok"
print("Smoke test passed. Real image inference requires a downloaded model and a separate image test.")

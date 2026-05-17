import requests

BASE_URL = "http://127.0.0.1:5000"

# Test input
incident = "A worker slipped on a wet floor near the warehouse entrance during the night shift. No wet floor signs were present."

print("=" * 60)

# Test /describe
print("\n[1] Testing /describe")
r = requests.post(f"{BASE_URL}/describe", json={"text": incident})
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

# Test /recommend
print("\n[2] Testing /recommend")
r = requests.post(f"{BASE_URL}/recommend", json={"text": incident})
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

# Test /generate-report
print("\n[3] Testing /generate-report")
r = requests.post(f"{BASE_URL}/generate-report", json={"text": incident})
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")



print("\n✅ All endpoints tested!")
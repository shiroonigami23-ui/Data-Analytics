import json
import os

DATA_FILE = "data/analytics.json"

# Ensure file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"visits": {}, "searches": []}, f, indent=2)

# Load data
with open(DATA_FILE, "r") as f:
    data = json.load(f)

# Example: Add fake update (for manual test)
data["visits"]["manual_test"] = data["visits"].get("manual_test", 0) + 1

# Save back
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("✅ Analytics updated:", data)
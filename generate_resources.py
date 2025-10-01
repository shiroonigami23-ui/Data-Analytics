import os, json

RES_DIR = "data/resources"
OUT_FILE = "data/resources.json"

resources = []

# scan the resources folder
for filename in os.listdir(RES_DIR):
    path = os.path.join(RES_DIR, filename)
    if os.path.isfile(path):
        ext = filename.split(".")[-1].lower()
        resources.append({
            "name": filename,
            "path": f"{RES_DIR}/{filename}",
            "type": ext
        })

# write json output
with open(OUT_FILE, "w") as f:
    json.dump(resources, f, indent=2)

print(f"✅ Updated {OUT_FILE} with {len(resources)} resources")

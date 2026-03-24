import os, json
from PyPDF2 import PdfReader

RESOURCE_DIR = "data/resources"
OUTPUT_JSON = "resources.json"

resources = []

for file in os.listdir(RESOURCE_DIR):
    path = os.path.join(RESOURCE_DIR, file)
    if file.lower().endswith(".pdf"):
        try:
            reader = PdfReader(path)
            text = reader.pages[0].extract_text()[:200] if reader.pages else "No preview"
        except Exception as e:
            text = f"Error reading PDF: {e}"
        resources.append({"title": file.replace(".pdf",""), "file": path, "preview": text, "type":"pdf"})
    elif file.lower().endswith((".png",".jpg",".jpeg")):
        resources.append({"title": file, "file": path, "preview": "Image file", "type":"image"})
    elif file.lower().endswith(".txt"):
        with open(path, "r", errors="ignore") as f:
            text = f.read(200)
        resources.append({"title": file, "file": path, "preview": text, "type":"text"})

with open(OUTPUT_JSON, "w") as f:
    json.dump(resources, f, indent=2)

print(f"✅ Updated {OUTPUT_JSON} with {len(resources)} entries")

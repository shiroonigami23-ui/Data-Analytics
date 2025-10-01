import os, json, shutil
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
from pathlib import Path
from bs4 import BeautifulSoup

RESOURCE_DIR = "data/resources"
OUTPUT_JSON = "resources.json"
QUIZ_JSON = "quiz.json"
INDEX_HTML = "index.html"
RESOURCES_HTML = "resources.html"

# Ensure folders exist
Path(RESOURCE_DIR).mkdir(parents=True, exist_ok=True)

resources = []

# ---- Extract text helpers ----
def extract_pdf(path):
    try:
        reader = PdfReader(path)
        return reader.pages[0].extract_text()[:500] if reader.pages else ""
    except: return ""

def extract_doc(path):
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs[:5]])
    except: return ""

def extract_ppt(path):
    try:
        prs = Presentation(path)
        texts = []
        for slide in prs.slides[:3]:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    texts.append(shape.text)
        return "\n".join(texts)
    except: return ""

# ---- Build resource list ----
for file in os.listdir(RESOURCE_DIR):
    path = os.path.join(RESOURCE_DIR, file)
    entry = None
    if file.lower().endswith(".pdf"):
        text = extract_pdf(path)
        entry = {"title": file.replace(".pdf",""), "file": path, "summary": text[:200], "type": "pdf"}
    elif file.lower().endswith((".png",".jpg",".jpeg")):
        entry = {"title": file, "file": path, "summary": "Image resource", "type": "image"}
    elif file.lower().endswith(".docx"):
        text = extract_doc(path)
        entry = {"title": file.replace(".docx",""), "file": path, "summary": text[:200], "type": "doc"}
    elif file.lower().endswith(".pptx"):
        text = extract_ppt(path)
        entry = {"title": file.replace(".pptx",""), "file": path, "summary": text[:200], "type": "ppt"}
    else:
        continue

    if entry:
        # prevent duplicates
        if not any(r["file"] == entry["file"] for r in resources):
            resources.append(entry)

# ---- Save resources.json ----
with open(OUTPUT_JSON, "w") as f:
    json.dump(resources, f, indent=2)

print(f"✅ Updated {OUTPUT_JSON} with {len(resources)} entries")

# ---- Update resources.html ----
if os.path.exists(RESOURCES_HTML):
    with open(RESOURCES_HTML, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    container = soup.find("div", {"id": "resources-list"})
    if not container:
        container = soup.new_tag("div", id="resources-list")
        soup.body.append(container)

    container.clear()
    for res in resources:
        card = soup.new_tag("div", **{"class": "card"})
        card.string = f"{res['title']} ({res['type']}) - {res['summary'][:100]}..."
        container.append(card)

    with open(RESOURCES_HTML, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("✅ resources.html updated")

# ---- Update index.html ----
if os.path.exists(INDEX_HTML):
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    latest = soup.find("div", {"id": "latest-resources"})
    if not latest:
        latest = soup.new_tag("div", id="latest-resources")
        soup.body.append(latest)

    latest.clear()
    h2 = soup.new_tag("h2")
    h2.string = "📚 Latest Resources"
    latest.append(h2)

    for res in resources[:5]:  # show only latest 5
        p = soup.new_tag("p")
        p.string = f"{res['title']} - {res['summary'][:80]}..."
        latest.append(p)

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("✅ index.html updated")
    

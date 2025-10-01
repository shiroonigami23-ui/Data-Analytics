import os
import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import PyPDF2
import docx

RESOURCE_DIR = "data/resources"
RESOURCES_JSON = "resources.json"
QUIZ_JSON = "quiz.json"

# =====================
# Text Extractors
# =====================
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:2]:  # first 2 pages only
                text += page.extract_text() or ""
            return text.strip().replace("\n", " ")[:500]
    except:
        return None

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])[:500]
    except:
        return None

# =====================
# Metadata Builder
# =====================
def build_resources():
    resources = []
    for fname in os.listdir(RESOURCE_DIR):
        fpath = os.path.join(RESOURCE_DIR, fname)
        if os.path.isfile(fpath):
            ext = Path(fname).suffix.lower()
            name = Path(fname).stem.replace("_", " ").title()

            # Detect type
            if ext in [".pdf", ".docx", ".pptx"]:
                ftype = "document"
            elif ext in [".png", ".jpg", ".jpeg", ".gif"]:
                ftype = "image"
            elif ext in [".txt"]:
                ftype = "text"
            else:
                ftype = "other"

            # Extract summary
            summary = None
            if ext == ".pdf":
                summary = extract_text_from_pdf(fpath)
            elif ext == ".docx":
                summary = extract_text_from_docx(fpath)
            elif ext == ".txt":
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    summary = f.read()[:500]

            resources.append({
                "title": name,
                "file": f"{RESOURCE_DIR}/{fname}",
                "type": ftype,
                "size_kb": round(os.path.getsize(fpath) / 1024, 2),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d %H:%M"),
                "summary": summary or f"{name} ({ftype}) resource for Data Analytics learning."
            })

    with open(RESOURCES_JSON, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)

    print(f"✅ {RESOURCES_JSON} updated with {len(resources)} entries")
    return resources

# =====================
# Quiz Generator
# =====================
def generate_quiz(resources):
    quiz = []
    for res in resources[:5]:  # limit to 5 auto-generated
        q = {
            "q": f"What is the main focus of {res['title']}?",
            "options": [
                res['title'],
                "Statistics",
                "Machine Learning",
                "Data Visualization"
            ],
            "a": res['title']
        }
        quiz.append(q)

    with open(QUIZ_JSON, "w", encoding="utf-8") as f:
        json.dump(quiz, f, indent=2, ensure_ascii=False)

    print(f"✅ {QUIZ_JSON} updated with {len(quiz)} questions")

# =====================
# HTML Updaters
# =====================
def update_resources_html(resources):
    if not os.path.exists("resources.html"):
        return
    with open("resources.html", "r+", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        container = soup.find("div", {"id": "resources-list"})
        if container:
            container.clear()
            for res in resources:
                div = soup.new_tag("div", **{"class": "card"})
                h3 = soup.new_tag("h3"); h3.string = f"{res['title']} ({res['type']})"
                p1 = soup.new_tag("p"); p1.string = f"📁 {res['file']} — {res['size_kb']} KB"
                p2 = soup.new_tag("p"); p2.string = f"Last updated: {res['last_modified']}"
                a = soup.new_tag("a", href=res["file"], target="_blank"); a.string = "📥 Open Resource"
                btn = soup.new_tag("button"); btn.string = "✔ Mark as Read"
                div.extend([h3, p1, p2, a, btn])
                container.append(div)
        f.seek(0); f.write(str(soup)); f.truncate()
    print("✅ resources.html updated")

def update_topics_html(resources):
    if not os.path.exists("topics.html"):
        return
    with open("topics.html", "r+", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        container = soup.find("div", {"id": "topicsList"})
        if container:
            container.clear()
            for res in resources:
                div = soup.new_tag("div", **{"class": "card"})
                h3 = soup.new_tag("h3"); h3.string = res["title"]
                p = soup.new_tag("p"); p.string = res["summary"]
                btn = soup.new_tag("button"); btn.string = "✔ Mark Topic Complete"
                div.extend([h3, p, btn])
                container.append(div)
        f.seek(0); f.write(str(soup)); f.truncate()
    print("✅ topics.html updated")

def update_index_html(resources):
    if not os.path.exists("index.html"):
        return
    with open("index.html", "r+", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        featured = soup.find("div", {"id": "featured-container"})
        if featured:
            featured.clear()
            for res in resources[:3]:
                div = soup.new_tag("div", **{"class": "card"})
                h3 = soup.new_tag("h3"); h3.string = res["title"]
                p = soup.new_tag("p"); p.string = res["summary"]
                featured.append(div)
        f.seek(0); f.write(str(soup)); f.truncate()
    print("✅ index.html updated")

# =====================
# Main
# =====================
if __name__ == "__main__":
    resources = build_resources()
    generate_quiz(resources)
    update_resources_html(resources)
    update_topics_html(resources)
    update_index_html(resources)
    print("🎉 Full site auto-update complete!")
    

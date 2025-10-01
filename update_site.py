import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import PyPDF2
import docx
from ebooklib import epub

RESOURCE_DIR = "data/resources"
RESOURCES_FILE = "resources.json"
QUIZ_FILE = "quiz.json"

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:2]:
                text += page.extract_text() or ""
            return text.strip().replace("\n", " ")[:400]
    except:
        return None

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])[:400]
    except:
        return None

def extract_text_from_epub(file_path):
    try:
        book = epub.read_epub(file_path)
        text = []
        for item in book.get_items():
            if item.get_type() == 9:
                content = item.get_content().decode("utf-8")
                text.append(re.sub("<[^<]+?>", "", content))
        return " ".join(text)[:400]
    except:
        return None

def generate_resources():
    resources = []
    for file in os.listdir(RESOURCE_DIR):
        path = os.path.join(RESOURCE_DIR, file)
        if os.path.isfile(path):
            name = Path(file).stem.replace("_", " ")
            ext = Path(file).suffix.lower()
            description = None

            if ext == ".pdf":
                description = extract_text_from_pdf(path)
            elif ext == ".docx":
                description = extract_text_from_docx(path)
            elif ext == ".epub":
                description = extract_text_from_epub(path)
            elif ext in [".png", ".jpg", ".jpeg"]:
                description = f"Image resource: {name}"
            elif ext in [".pptx"]:
                description = f"Presentation slides: {name}"
            elif ext == ".txt":
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    description = f.read()[:400]

            resources.append({
                "title": name.title(),
                "file": f"{RESOURCE_DIR}/{file}",
                "type": ext.replace(".", "").upper(),
                "summary": description or f"Resource on {name} uploaded for Data Analytics learning."
            })

    with open(RESOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)
    return resources

def generate_quiz(resources):
    quiz = []
    for res in resources[:5]:  # max 5 questions
        question = {
            "q": f"What is the main topic of {res['title']}?",
            "options": [
                res['title'],
                "Statistics",
                "Machine Learning",
                "Data Visualization"
            ],
            "a": res['title']
        }
        quiz.append(question)

    with open(QUIZ_FILE, "w", encoding="utf-8") as f:
        json.dump(quiz, f, indent=2, ensure_ascii=False)

def update_html(resources):
    # Update Topics
    if os.path.exists("topics.html"):
        with open("topics.html", "r+", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            container = soup.find("div", {"id": "topicsList"})
            if container:
                container.clear()
                for res in resources:
                    div = soup.new_tag("div", **{"class": "card"})
                    h3 = soup.new_tag("h3"); h3.string = res["title"]
                    p = soup.new_tag("p"); p.string = res["summary"]
                    btn = soup.new_tag("button"); btn.string = "✔ Mark Complete"
                    div.extend([h3, p, btn])
                    container.append(div)
            f.seek(0); f.write(str(soup)); f.truncate()

    # Update Resources
    if os.path.exists("resources.html"):
        with open("resources.html", "r+", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            container = soup.find("div", {"id": "resources-list"})
            if container:
                container.clear()
                for res in resources:
                    div = soup.new_tag("div", **{"class": "card"})
                    h3 = soup.new_tag("h3"); h3.string = f"{res['title']} ({res['type']})"
                    p = soup.new_tag("p"); p.string = res["summary"]
                    a = soup.new_tag("a", href=res["file"], target="_blank"); a.string = "📖 Open Resource"
                    btn = soup.new_tag("button"); btn.string = "✔ Mark as Read"
                    div.extend([h3, p, a, btn])
                    container.append(div)
            f.seek(0); f.write(str(soup)); f.truncate()

    # Update Index (top 3)
    if os.path.exists("index.html"):
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

if __name__ == "__main__":
    resources = generate_resources()
    generate_quiz(resources)
    update_html(resources)
    print("✅ Full site updated: resources.json, quiz.json, index, topics, resources!")
    

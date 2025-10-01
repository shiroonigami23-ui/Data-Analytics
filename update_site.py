import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import PyPDF2
import docx
from ebooklib import epub

# Base paths
RESOURCE_DIR = "data/resources"
METADATA_FILE = "data/resources/metadata.json"

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[:2]:  # first 2 pages for summary
                text += page.extract_text() or ""
            return text.strip().replace("\n", " ")[:400]
    except Exception as e:
        return f"Error extracting PDF text: {e}"

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = " ".join([p.text for p in doc.paragraphs])
        return text[:400]
    except Exception as e:
        return f"Error extracting DOCX text: {e}"

def extract_text_from_epub(file_path):
    try:
        book = epub.read_epub(file_path)
        text = []
        for item in book.get_items():
            if item.get_type() == 9:  # DOCUMENT
                content = item.get_content().decode("utf-8")
                text.append(re.sub("<[^<]+?>", "", content))
        return " ".join(text)[:400]
    except Exception as e:
        return f"Error extracting EPUB text: {e}"

def generate_metadata():
    resources = []
    for file in os.listdir(RESOURCE_DIR):
        path = os.path.join(RESOURCE_DIR, file)
        if os.path.isfile(path) and not file.startswith("metadata"):
            name = Path(file).stem.replace("_", " ")
            ext = Path(file).suffix.lower()
            description = ""

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
            elif ext in [".txt"]:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    description = f.read()[:400]

            resources.append({
                "title": name.title(),
                "file": f"{RESOURCE_DIR}/{file}",
                "type": ext.replace(".", "").upper(),
                "description": description if description else "No description available."
            })

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=4)
    return resources

def update_html(metadata):
    # Update Topics
    with open("topics.html", "r+", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        container = soup.find("div", {"id": "topics-container"})
        if container:
            container.clear()
            for res in metadata:
                div = soup.new_tag("div", **{"class": "card"})
                h3 = soup.new_tag("h3"); h3.string = res["title"]
                p = soup.new_tag("p"); p.string = res["description"]
                btn = soup.new_tag("button", **{"class": "mark-complete"}); btn.string = "✔ Mark Topic Complete"
                div.extend([h3, p, btn])
                container.append(div)
        f.seek(0); f.write(str(soup)); f.truncate()

    # Update Resources
    with open("resources.html", "r+", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        container = soup.find("div", {"id": "resources-container"})
        if container:
            container.clear()
            for res in metadata:
                div = soup.new_tag("div", **{"class": "card"})
                h3 = soup.new_tag("h3"); h3.string = f"{res['title']} ({res['type']})"
                p = soup.new_tag("p"); p.string = res["description"]
                a = soup.new_tag("a", href=res["file"], target="_blank"); a.string = "📖 Open Resource"
                btn = soup.new_tag("button", **{"class": "mark-read"}); btn.string = "✔ Mark as Read"
                div.extend([h3, p, a, btn])
                container.append(div)
        f.seek(0); f.write(str(soup)); f.truncate()

    # Update Index (featured first 3)
    with open("index.html", "r+", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        featured = soup.find("div", {"id": "featured-container"})
        if featured:
            featured.clear()
            for res in metadata[:3]:
                div = soup.new_tag("div", **{"class": "card"})
                h3 = soup.new_tag("h3"); h3.string = res["title"]
                p = soup.new_tag("p"); p.string = res["description"]
                div.extend([h3, p])
                featured.append(div)
        f.seek(0); f.write(str(soup)); f.truncate()

if __name__ == "__main__":
    metadata = generate_metadata()
    update_html(metadata)
    print("✅ Site updated with new resources & topics!")
    

import os
import json
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import PyPDF2
import docx
import google.generativai as genai

# --- Configuration ---
RESOURCE_DIR = "data/resources"
RESOURCES_JSON = "resources.json"
QUIZ_JSON = "quiz.json"

# --- AI Integration ---

def get_gemini_model():
    """Initializes and returns the Gemini model if the API key is set."""
    # This now looks for the secret named SHIROONI23
    gemini_api_key = os.getenv("SHIROONI23")
    if not gemini_api_key:
        print("⚠️ SHIROONI23 environment variable not set. Skipping AI functions.")
        return None
    try:
        genai.configure(api_key=gemini_api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {e}")
        return None

def generate_ai_summary(model, text_content, title):
    """Generates a friendly, concise summary for a document."""
    if not model or not text_content:
        return f"A document about {title}. Open to read more."

    print(f"✨ Generating AI summary for: {title}...")
    prompt = f"""
    Please act as a friendly and helpful teaching assistant. Based on the text from a document titled "{title}", generate a concise, engaging summary for a student.

    Rules:
    - The summary should be around 2-3 sentences long.
    - Explain the main topic and what the student will learn.
    - Use a slightly quirky and encouraging tone. For example, use phrases like "Dive into..." or "Get ready to master...".
    - Do not use markdown or special formatting. Return only the plain text of the summary.

    Text content:
    ---
    {text_content}
    ---
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ AI summary generation failed: {e}")
        return f"A document about {title}. An error occurred while generating the summary."

def generate_ai_quiz(model, text_content, title):
    """Generates a list of quiz questions from text content."""
    if not model or not text_content:
        return []

    print(f"🧠 Generating AI quiz for: {title}...")
    prompt = f"""
    Based on the following text from a data analytics document titled "{title}", please generate 2 unique multiple-choice quiz questions.

    Rules:
    - Each question must have exactly 3 options.
    - One option must be the correct answer.
    - Return the output as a valid JSON array. Do not include any text or formatting before or after the JSON.
    - Each JSON object in the array should have three keys: "q" for the question, "options" for an array of the choices, and "a" for the correct answer.

    Text content:
    ---
    {text_content}
    ---
    """
    try:
        response = model.generate_content(prompt)
        json_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_response)
    except Exception as e:
        print(f"⚠️ AI quiz generation failed: {e}")
        return []

# --- Text Extractors ---
def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            # Extract text from up to the first 5 pages for better context
            for page in reader.pages[:5]:
                text += page.extract_text() or ""
            return text.strip().replace("\n", " ")
    except Exception as e:
        print(f"Could not read PDF {file_path}: {e}")
        return None

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Could not read DOCX {file_path}: {e}")
        return None

# --- Core Logic ---
def build_and_update_content():
    """Main function to build resources, generate content, and update HTML."""
    gemini_model = get_gemini_model()
    resources = []
    full_quiz = []

    for fname in os.listdir(RESOURCE_DIR):
        fpath = os.path.join(RESOURCE_DIR, fname)
        if not os.path.isfile(fpath):
            continue

        ext = Path(fname).suffix.lower()
        name = Path(fname).stem.replace("_", " ").title()
        ftype = "other"
        full_text = None

        if ext == ".pdf":
            ftype = "document"
            full_text = extract_text_from_pdf(fpath)
        elif ext == ".docx":
            ftype = "document"
            full_text = extract_text_from_docx(fpath)
        elif ext in [".png", ".jpg", ".jpeg"]:
            ftype = "image"
        
        # Generate AI summary
        summary = generate_ai_summary(gemini_model, full_text, name)

        # Generate AI quiz questions
        if ftype == "document":
            quiz_questions = generate_ai_quiz(gemini_model, full_text, name)
            full_quiz.extend(quiz_questions)

        resources.append({
            "title": name,
            "file": f"{RESOURCE_DIR}/{fname}",
            "type": ftype,
            "summary": summary
        })

    # Save the generated content to JSON files
    with open(RESOURCES_JSON, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)
    print(f"✅ {RESOURCES_JSON} updated with {len(resources)} entries")

    # Add fallback questions if AI generation failed
    if not full_quiz:
        full_quiz.append({"q": "Which step is crucial for preparing data?", "options": ["Cleaning", "Ignoring", "Deleting"], "a": "Cleaning"})
    
    with open(QUIZ_JSON, "w", encoding="utf-8") as f:
        json.dump(full_quiz, f, indent=2, ensure_ascii=False)
    print(f"✅ {QUIZ_JSON} updated with {len(full_quiz)} questions")

    # Update the HTML files
    update_html_files(resources)

def update_html_files(resources):
    """Updates the topics and resources HTML pages with new content."""
    # Update topics.html
    try:
        with open("topics.html", "r+", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            container = soup.find("div", {"id": "topicsList"})
            if container:
                container.clear()
                for res in resources:
                    card = soup.new_tag("div", attrs={"class": "card"})
                    card.innerHTML = f"""<h3>{res['title']}</h3>
                                         <p>{res['summary']}</p>
                                         <a href="{res['file']}" target="_blank" class="button">Read More</a>"""
                    container.append(card)
            f.seek(0)
            f.write(str(soup))
            f.truncate()
        print("✅ topics.html updated")
    except FileNotFoundError:
        print("⚠️ topics.html not found, skipping update.")
    
    # Update resources.html (optional, as topics.html is similar)
    print("✅ All HTML files updated.")


if __name__ == "__main__":
    build_and_update_content()
    print("🎉 Full site auto-update complete!")

import os
import json
from pathlib import Path
import google.generativeai as genai
import PyPDF2

# --- Configuration ---
RESOURCE_DIR = "data/resources"
RESOURCES_JSON = "resources.json"
QUIZ_JSON = "quiz.json"
HEADER_TEMPLATE = "_header.html"
FOOTER_TEMPLATE = "_footer.html"

# --- AI and Text Extraction (same as before) ---

def get_gemini_model():
    gemini_api_key = os.getenv("SHIROONI23")
    if not gemini_api_key: return None
    try:
        genai.configure(api_key=gemini_api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception: return None

def generate_ai_content(model, text, title, task):
    if not model or not text: return None
    if task == "summary":
        prompt = f'Generate a concise, 2-3 sentence summary for a student from this text titled "{title}":\n\n{text}'
    elif task == "quiz":
        prompt = f'Generate 2 multiple-choice questions based on this text. Return as a valid JSON array of objects with keys "q", "options", and "a".\n\n{text}'
    try:
        response = model.generate_content(prompt)
        if task == "quiz":
            return json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        return response.text.strip()
    except Exception:
        return [] if task == "quiz" else f"A document about {title}."

def extract_text_from_pdf(path):
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "".join(page.extract_text() or "" for page in reader.pages[:3])
    except Exception: return None

# --- WEBSITE BUILDER ---

def render_page(page_name, content, active_nav):
    """Builds a full HTML page from templates and content."""
    try:
        with open(HEADER_TEMPLATE, "r", encoding="utf-8") as f:
            header = f.read()
        with open(FOOTER_TEMPLATE, "r", encoding="utf-8") as f:
            footer = f.read()
    except FileNotFoundError:
        print("❌ Error: Template files (_header.html, _footer.html) not found!")
        return

    # Set the page title and active navigation link
    header = header.replace("{{PAGE_TITLE}}", page_name.title())
    nav_placeholders = ["HOME", "TOPICS", "QUIZ", "PROGRESS"]
    for nav in nav_placeholders:
        header = header.replace(f"{{{{ACTIVE_{nav}}}}}", "active" if nav == active_nav else "")

    # Combine templates and content to create the final HTML
    full_html = header + content + footer
    with open(f"{page_name.lower()}.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"✅ Built page: {page_name.lower()}.html")

# --- Page Content Generators ---

def build_all_pages(resources, quizzes):
    """Creates the content for and renders each page of the website."""
    # 1. Home Page
    home_content = """
        <section class="hero">
            <h1>Learn Data Analytics — simple, visual, and fun</h1>
            <p class="lead">AI-powered summaries, quizzes and a pop-up dictionary.</p>
        </section>
        <h2>Latest Topics</h2>
    """
    home_content += '<div class="cards-grid">'
    for res in resources[:3]: # Show 3 latest topics on home
        home_content += f'<div class="card"><h3>{res["title"]}</h3><p>{res["summary"]}</p><a href="topics.html" class="button">View Topic</a></div>'
    home_content += '</div>'
    render_page("index", home_content, "HOME")

    # 2. Topics Page
    topics_content = '<h1>📖 Extracted Topics</h1>'
    topics_content += '<div class="cards-grid">'
    for res in resources:
        topics_content += f"""
            <div class="card">
                <h3>{res['title']}</h3>
                <p>{res['summary']}</p>
                <a href="{res['file']}" target="_blank" class="button">Read Document</a>
            </div>"""
    topics_content += '</div>'
    render_page("topics", topics_content, "TOPICS")

    # 3. Quiz Page
    quiz_content = '<h1>📝 Practice Quiz</h1><div id="quiz-container">'
    for i, q in enumerate(quizzes):
        options_html = ""
        for opt in q['options']:
            options_html += f'<label class="quiz-option"><input type="radio" name="q{i}" value="{opt}"> {opt}</label>'
        quiz_content += f'<div class="card"><p><strong>Q{i+1}:</strong> {q["q"]}</p>{options_html}</div>'
    quiz_content += '</div><button id="submit-btn">Submit Quiz</button><div id="quiz-result"></div>'
    render_page("quiz", quiz_content, "QUIZ")

    # 4. Progress Page
    progress_content = """
        <h1>🏆 Your Progress & Achievements</h1>
        <section class="card">
            <h2>🏅 Your Badges</h2>
            <p>You can earn badges by reading topics and completing quizzes!</p>
            <div id="badges"></div>
        </section>
    """
    render_page("progress", progress_content, "PROGRESS")


# --- Main Execution ---

def main():
    """Main function to generate JSON content and build the full website."""
    model = get_gemini_model()
    resources = []
    quizzes = []

    for fname in sorted(os.listdir(RESOURCE_DIR)):
        fpath = os.path.join(RESOURCE_DIR, fname)
        if fname.lower().endswith(".pdf"):
            title = Path(fname).stem.replace("_", " ").title()
            text = extract_text_from_pdf(fpath)
            
            summary = generate_ai_content(model, text, title, "summary")
            quiz_items = generate_ai_content(model, text, title, "quiz")
            
            resources.append({"title": title, "file": fpath, "summary": summary})
            if quiz_items: quizzes.extend(quiz_items)
            
    # Save JSON files (still useful for other tools or future features)
    with open(RESOURCES_JSON, "w") as f: json.dump(resources, f, indent=2)
    with open(QUIZ_JSON, "w") as f: json.dump(quizzes, f, indent=2)
    
    # Build the entire multi-page website
    build_all_pages(resources, quizzes)

if __name__ == "__main__":
    main()

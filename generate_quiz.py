import json, random
from PyPDF2 import PdfReader
import os

RESOURCE_DIR = "data/resources"
QUIZ_FILE = "quiz.json"

questions = []

for file in os.listdir(RESOURCE_DIR):
    if file.endswith(".pdf"):
        try:
            reader = PdfReader(os.path.join(RESOURCE_DIR, file))
            text = reader.pages[0].extract_text() if reader.pages else ""
            if "data" in text.lower():
                questions.append({
                    "q": f"What is one key concept mentioned in {file}?",
                    "options": ["Data Collection", "Dancing", "Drawing"],
                    "a": "Data Collection"
                })
        except:
            continue

# Add fallback example questions if none generated
if not questions:
    questions = [
        {"q": "Which step comes first in Data Analytics?", "options":["Data Cleaning","Data Collection","Modeling"], "a":"Data Collection"},
        {"q": "Which chart is best for trends over time?", "options":["Bar","Pie","Line"], "a":"Line"},
    ]

with open(QUIZ_FILE, "w") as f:
    json.dump(questions, f, indent=2)

print(f"✅ Updated {QUIZ_FILE} with {len(questions)} questions")

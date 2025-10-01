# Data Analytics Phase 3 - Visual UI + Auto Resources + Quiz Generator

Files included:
- css/style.css
- js/main.js
- scripts/generate_resources.py  -> generates data/resources.json and thumbnails/
- scripts/generate_quiz.py       -> generates data/quiz.json
- resources.html                 -> dynamic page that uses data/resources.json
- sample resources in data/resources/

How to run generator locally:
1. pip install pillow
2. python scripts/generate_resources.py
3. python scripts/generate_quiz.py

Add GitHub Action to run generator on push to auto-update resources.
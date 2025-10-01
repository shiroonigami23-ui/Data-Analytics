# 📊 Data Analytics Hub

A gamified, interactive learning portal for Data Analytics, designed by **Shiro Oni-sama 👑**.

## ✨ Features
- 📚 **Auto Resources Extraction**: PDFs, DOCX, PPTX, and images → auto summaries + previews.
- 📝 **Quizzes**: Generated from uploaded resources.
- 🏆 **Badges & Progress**: Students unlock badges and track their study progress.
- 🌐 **Translator Integration**: Highlight a word → quick meaning.
- 📬 **Feedback System**: Submissions via Google Apps Script → daily email summaries.
- 📊 **Analytics**: Anonymous tracking of popular topics and site usage.

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS (modern blue theme), JS
- **Backend Automation**: Python (`PyPDF2`, `pdfminer.six`, `python-docx`, `python-pptx`)
- **CI/CD**: GitHub Actions (auto update + deploy)
- **Feedback**: Google Apps Script → Sheets + email

## 📂 Structure
index.html
about.html
topics.html
resources.html
quiz.html
contact.html
analytics.html
style.css
script.js
badges.js
resources.json
quiz.json
update_site.py
generate_resources.py
generate_quiz.py
.github/workflows/update.yml

## 🚀 How It Works
1. Upload files (PDF/Doc/Image) into `data/resources/`.
2. GitHub Action runs:
   - Extracts content → updates `resources.json`.
   - Generates quizzes → updates `quiz.json`.
   - Refreshes `index.html` and `resources.html`.
3. Site auto-deploys via GitHub Pages.

## 👑 Credits
Project created and guided by **Shiro Oni-sama**.

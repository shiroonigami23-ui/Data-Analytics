import os

RESOURCES_DIR = "data/resources"
OUTPUT_FILE = "resources.html"

def generate_resources_html():
    files = os.listdir(RESOURCES_DIR)
    files = [f for f in files if not f.startswith(".")]  # skip hidden/.gitkeep

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Resources</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>Resources</h1>
    <p>All uploaded study materials, datasets, and references.</p>
  </header>
  <main>
    <ul>
"""
    if not files:
        html_content += "<li>No resources uploaded yet.</li>\n"
    else:
        for file in files:
            file_path = f"{RESOURCES_DIR}/{file}"
            ext = os.path.splitext(file)[1].lower()

            # Choose icon based on file type
            if ext in [".pdf"]:
                icon = "📄"
            elif ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
                icon = "🖼️"
            elif ext in [".doc", ".docx"]:
                icon = "📝"
            elif ext in [".csv", ".xlsx"]:
                icon = "📊"
            else:
                icon = "📁"

            html_content += f'      <li>{icon} <a href="{file_path}" target="_blank">{file}</a></li>\n'

    html_content += """    </ul>
  </main>
  <footer>
    <p>Auto-generated Resources Page</p>
  </footer>
</body>
</html>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Resources page updated with {len(files)} files.")

if __name__ == "__main__":
    generate_resources_html()
    

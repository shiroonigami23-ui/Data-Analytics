#!/usr/bin/env python3
import os, shutil, pathlib

# Folders / files we KEEP
keep_files = {
    "index.html","about.html","topics.html","resources.html","quiz.html","contact.html","admin.html",
    "style.css","script.js","backend.js",
    "update_site.py","config.yaml","requirements.txt","package.json","README.md",
    "resources.json","quiz.json","feedback.gs"
}
keep_dirs = {".github","data"}

# Folders / files to remove if found
delete_candidates = [
    "update.py","update-site.yml","generate_quiz.py","generate_resources.py","generate_site.py",
    "analytics.html","quiz.yaml","resources.yaml","main.js"
]

root = pathlib.Path(".")

# Delete unwanted files
for fname in delete_candidates:
    fpath = root / fname
    if fpath.exists():
        if fpath.is_dir():
            shutil.rmtree(fpath)
            print("Removed folder:", fpath)
        else:
            fpath.unlink()
            print("Removed file:", fpath)

# Clean up .github/workflows (keep only update.yml + deploy.yml)
wf_dir = root / ".github" / "workflows"
if wf_dir.exists():
    for f in wf_dir.iterdir():
        if f.name not in ["update.yml","deploy.yml"]:
            f.unlink()
            print("Removed old workflow:", f)

print("✅ Repo cleanup complete, only essential files remain.")

import os

# Always keep these extensions and folders
SAFE_EXTENSIONS = {".html", ".css", ".js", ".json", ".yaml", ".yml", ".md", ".py"}
SAFE_FOLDERS = {"data", ".github"}

# Explicit junk files (we know they are not needed)
REMOVE_FILES = {
    "update.py",
    "update-site.yml",
    "admin.html",
    "package.json"
}

def is_safe(file):
    # Always keep known safe files
    if file in REMOVE_FILES:
        return False
    if os.path.isdir(file) and file in SAFE_FOLDERS:
        return True
    ext = os.path.splitext(file)[1]
    return ext in SAFE_EXTENSIONS

def cleanup():
    for file in os.listdir("."):
        if file.startswith(".git"):  # never touch git internals
            continue
        if not is_safe(file):
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"Removed: {file}")
                elif os.path.isdir(file):
                    # Only remove unknown directories
                    os.rmdir(file)
                    print(f"Removed folder: {file}")
            except Exception as e:
                print(f"Could not remove {file}: {e}")

    print("Safe cleanup complete ✅")

if __name__ == "__main__":
    cleanup()
    

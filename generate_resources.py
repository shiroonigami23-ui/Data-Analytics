import os, json
from PIL import Image
from datetime import datetime

RES_DIR = "data/resources"
OUT_JSON = "data/resources.json"
THUMB_DIR = "thumbnails"
METADATA_FILE = os.path.join(RES_DIR, "metadata.json")

os.makedirs(THUMB_DIR, exist_ok=True)

def human_size(n):
    for u in ['B','KB','MB','GB']:
        if n < 1024.0:
            return f"{n:.1f} {u}"
        n /= 1024.0
    return f"{n:.1f} TB"

# load metadata if present
metadata = {}
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        try:
            metadata = json.load(f)
        except:
            print("Warning: metadata.json parse error")

items = []
for fname in sorted(os.listdir(RES_DIR)):
    if fname.startswith("."): 
        continue
    path = os.path.join(RES_DIR, fname)
    if not os.path.isfile(path): continue
    ext = os.path.splitext(fname)[1].lower()
    stat = os.stat(path)
    size = stat.st_size
    mtime = datetime.utcfromtimestamp(stat.st_mtime).isoformat()+"Z"
    thumb = ""
    # generate thumbnail for images
    if ext in ['.png','.jpg','.jpeg','.gif']:
        try:
            im = Image.open(path)
            im.thumbnail((800,600))
            tname = fname + ".png"
            tpath = os.path.join(THUMB_DIR, tname)
            im.save(tpath, "PNG")
            thumb = tpath.replace("\\\\","/")
        except Exception as e:
            print("Thumb error", e)
    meta = metadata.get(fname, {})
    item = {
        "name": fname,
        "path": path.replace("\\\\","/"),
        "type": ext.replace('.',''),
        "ext": ext,
        "size_bytes": size,
        "size_human": human_size(size),
        "uploaded_at": mtime,
        "description": meta.get("description",""),
        "tags": meta.get("tags",[]),
        "thumbnail": thumb
    }
    items.append(item)

# write json
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2)

print("Wrote", OUT_JSON, "with", len(items), "items")
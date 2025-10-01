import os, json, random
RES_DIR = "data/resources"
OUT = "data/quiz.json"

# If metadata contains 'quiz' blocks, use them. Otherwise, simple generator from filenames
metafile = os.path.join(RES_DIR, "metadata.json")
quizzes = []
if os.path.exists(metafile):
    m = json.load(open(metafile,'r',encoding='utf-8'))
    for k,v in m.items():
        if 'quiz' in v:
            quizzes.extend(v['quiz'])

# fallback: generate simple Q from filenames
if not quizzes:
    for fname in os.listdir(RES_DIR):
        if fname.startswith('.') or not os.path.isfile(os.path.join(RES_DIR,fname)): continue
        q = {
            "q": f"What is the file type of {fname}?",
            "options": ["PDF","Image","CSV","DOCX"],
            "a": "Image" if any(fname.lower().endswith(ext) for ext in ['.png','.jpg','.jpeg','.gif']) else ("PDF" if fname.lower().endswith('.pdf') else "CSV")
        }
        quizzes.append(q)

random.shuffle(quizzes)
open(OUT,'w',encoding='utf-8').write(json.dumps(quizzes,indent=2))
print("Wrote", OUT, "with", len(quizzes), "questions")
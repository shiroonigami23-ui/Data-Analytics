#!/usr/bin/env python3
# update_site.py - smart resource ingester: sorts uploads, extracts text (if libs installed), writes resources.json and quiz.json
import os, json, re, shutil
from pathlib import Path
DATA_DIR = Path("data/resources")
OUT_RES = Path("resources.json")
OUT_QUIZ = Path("quiz.json")
def safe_load_text(path):
    # naive: try to read small text from binary if libraries not present
    try:
        from PyPDF2 import PdfReader
        if path.suffix.lower()=='.pdf':
            r=PdfReader(str(path))
            txt='\\n'.join([p.extract_text() or '' for p in r.pages])
            return txt
    except Exception:
        pass
    try:
        import docx
        if path.suffix.lower()=='.docx':
            d = docx.Document(str(path))
            return '\\n'.join([p.text for p in d.paragraphs if p.text])
    except Exception:
        pass
    try:
        from pptx import Presentation
        if path.suffix.lower()=='.pptx':
            prs = Presentation(str(path))
            txts=[] 
            for s in prs.slides:
                for shape in s.shapes:
                    try:
                        if hasattr(shape, 'text'):
                            txts.append(shape.text)
                    except: pass
            return '\\n'.join(txts)
    except Exception:
        pass
    return ''
def extract_summary(text, n=3):
    if not text: return ''
    parts = [p.strip() for p in re.split(r'[\\n\\r]+', text) if p.strip()]
    return ' '.join(parts[:n])
def ensure_dirs():
    for d in ['pdfs','images','docs','pptx','misc']:
        (DATA_DIR / d).mkdir(parents=True, exist_ok=True)
def move_and_process():
    ensure_dirs()
    items=[]
    for f in os.listdir(DATA_DIR):
        if f.startswith('.'): continue
        p = DATA_DIR / f
        if p.is_dir(): continue
        ext = p.suffix.lower()
        if ext=='.pdf':
            dest = DATA_DIR / 'pdfs' / f; shutil.move(str(p), str(dest))
            text = safe_load_text(dest); summary = extract_summary(text) or 'Auto summary not available.'
            items.append({'title': dest.stem.replace('_',' ').title(), 'summary': summary, 'file': str(dest).replace('\\\\','/'), 'type':'pdf'})
        elif ext in ['.png','.jpg','.jpeg','.gif']:
            dest = DATA_DIR / 'images' / f; shutil.move(str(p), str(dest))
            items.append({'title': dest.stem.replace('_',' ').title(), 'summary': 'Image resource', 'file': str(dest).replace('\\\\','/'), 'type':'image','preview':str(dest).replace('\\\\','/')})
        elif ext=='.docx':
            dest = DATA_DIR / 'docs' / f; shutil.move(str(p), str(dest))
            text = safe_load_text(dest); summary = extract_summary(text) or 'Auto summary not available.'
            items.append({'title': dest.stem.replace('_',' ').title(), 'summary': summary, 'file': str(dest).replace('\\\\','/'), 'type':'doc'})
        elif ext=='.pptx':
            dest = DATA_DIR / 'pptx' / f; shutil.move(str(p), str(dest))
            text = safe_load_text(dest); summary = extract_summary(text) or 'Auto summary not available.'
            items.append({'title': dest.stem.replace('_',' ').title(), 'summary': summary, 'file': str(dest).replace('\\\\','/'), 'type':'ppt'})
        else:
            dest = DATA_DIR / 'misc' / f; shutil.move(str(p), str(dest))
            items.append({'title': dest.stem.replace('_',' ').title(), 'summary':'Misc resource', 'file': str(dest).replace('\\\\','/'), 'type':'misc'})
    return items
def main():
    items = move_and_process()
    # existing resources
    res = []
    if OUT_RES.exists():
        try:
            res = json.loads(OUT_RES.read_text(encoding='utf-8'))
        except: res = []
    res = items + res
    OUT_RES.write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding='utf-8')
    # generate quizzes naive
    qs = []
    for it in res:
        if it['type'] in ['pdf','doc','ppt','doc']:
            text = ''
            try:
                p = Path(it['file'])
                if p.suffix.lower()=='.pdf':
                    text = safe_load_text(p)
                elif p.suffix.lower()=='.docx':
                    text = safe_load_text(p)
                elif p.suffix.lower()=='.pptx':
                    text = safe_load_text(p)
            except: text=''
            # simple extraction: first noun-like words
            import re, random
            words = re.findall(r'\\b[A-Z][a-zA-Z]{3,}\\b', text)
            words = list(dict.fromkeys(words))[:10]
            sents = [s.strip() for s in re.split(r'(?<=[\\.!?])\\s+', text) if len(s.strip())>30]
            for i, s in enumerate(sents[:4]):
                if not words: break
                ans = words[i % len(words)]
                opts = [ans] + [w for w in words if w!=ans][:3]
                random.shuffle(opts)
                qs.append({'topic': it['title'], 'q': s[:120]+'...', 'options': opts, 'a': ans, 'explanation': 'Auto-generated'}) 
    if not qs:
        qs = json.loads(Path('quiz.json').read_text(encoding='utf-8')) if Path('quiz.json').exists() else []
    Path('quiz.json').write_text(json.dumps(qs, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Generated resources.json and quiz.json')
if __name__=='__main__':
    main()

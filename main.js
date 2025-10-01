const RES_JSON = "data/resources.json";
let resources = [];
let filtered = [];
document.addEventListener("DOMContentLoaded", async () => {
  await loadResources();
  setupSearch();
  renderStats();
  bindQuizNav();
});

async function loadResources(){
  try{
    const res = await fetch(RES_JSON + "?t="+Date.now());
    resources = await res.json();
    filtered = resources.slice();
    renderResources(filtered);
    highlightFeatured();
  }catch(e){
    console.error("Failed to load resources", e);
    document.getElementById("resourceGrid").innerHTML = "<p style='color:#ffb4b4'>Failed to load resources.json</p>";
  }
}

function renderResources(list){
  const grid = document.getElementById("resourceGrid");
  grid.innerHTML = "";
  if(!list.length){
    grid.innerHTML = "<p>No resources yet — add files to data/resources/ and push to repo.</p>";
    return;
  }
  list.forEach(r => {
    const el = document.createElement("div");
    el.className = "card";
    const thumb = r.thumbnail ? `<img src="${r.thumbnail}" alt="${r.name}">` : `<div style='font-size:48px;color:#0b63ff'>${iconFor(r.ext)}</div>`;
    el.innerHTML = `<div class='thumb'>${thumb}</div>
      <div class='meta'><div><strong style='color:inherit'>${r.name}</strong><div style='font-size:.85rem;color:var(--muted)'>${r.size_human} • ${r.type}</div></div>
      <div><span class='badge'>${r.ext.replace('.','').toUpperCase()}</span></div></div>
      <p style='margin:.6rem 0 .2rem 0;color:var(--muted);font-size:.92rem'>${r.description || ''}</p>
      <div style='display:flex;gap:.4rem;justify-content:space-between;align-items:center'>
        <div style='display:flex;gap:.4rem'><button onclick="previewResource('${escapeStr(r.path)}')" class='quirk'>Preview</button><a href="${r.path}" target="_blank">Open</a></div>
        <small style='color:var(--muted)'>${new Date(r.uploaded_at).toLocaleDateString()}</small>
      </div>`;
    grid.appendChild(el);
  });
}

function iconFor(ext){
  ext = ext.toLowerCase();
  if([".png",".jpg",".jpeg",".gif",".svg"].includes(ext)) return "🖼️";
  if([".pdf"].includes(ext)) return "📄";
  if([".csv",".xlsx"].includes(ext)) return "📊";
  if([".mp4",".webm"].includes(ext)) return "🎥";
  if([".doc",".docx"].includes(ext)) return "📝";
  return "📁";
}

function escapeStr(s){ return s.replace(/'/g,"\'").replace(/"/g,'\"'); }

function setupSearch(){
  const input = document.getElementById("q");
  input.addEventListener("input", ()=>{
    const q = input.value.trim().toLowerCase();
    filtered = resources.filter(r => (r.name + " " + (r.description||"") + " " + (r.tags||"").join(" ")).toLowerCase().includes(q));
    renderResources(filtered);
  });
}

function previewResource(path){
  const modal = document.getElementById("preview");
  const inner = document.getElementById("previewInner");
  inner.innerHTML = "";
  if(path.match(/\.(png|jpg|jpeg|gif|svg)$/i)){
    inner.innerHTML = `<img src="${path}" alt="preview">`;
  } else if(path.match(/\.pdf$/i)){
    inner.innerHTML = `<iframe src="${path}" style="width:100%;height:100%;border:0"></iframe>`;
  } else {
    inner.innerHTML = `<p style='padding:1rem'>Cannot preview this file type. <a href="${path}" target="_blank">Open file</a></p>`;
  }
  modal.classList.add("open");
}

function closePreview(){ document.getElementById("preview").classList.remove("open"); }

function renderStats(){
  const c = resources.length;
  document.getElementById("stats").innerText = `${c} resources`;
}

function highlightFeatured(){
  const f = resources.slice(0,3);
  const box = document.getElementById("featured");
  box.innerHTML = "";
  f.forEach(r => {
    const e = document.createElement("div"); e.className="hero-card";
    e.innerHTML = `<strong>${r.name}</strong><div style='color:var(--muted);font-size:.9rem'>${r.description||''}</div>`;
    box.appendChild(e);
  });
}

/* Quiz system - picks up quizzes from data/quiz.json if exists */
function bindQuizNav(){
  const btn = document.getElementById("takeQuizBtn");
  if(!btn) return;
  btn.addEventListener("click", ()=>{
    // load quiz data
    fetch("data/quiz.json").then(r=>r.json()).then(qs=>{
      if(!qs || !qs.length){ alert("No quizzes available. Add data/quiz.json or generate quizzes."); return; }
      startQuiz(qs);
    }).catch(()=>alert("No quiz file found"));
  });
}

// Very small quiz runner UI
function startQuiz(questions){
  const container = document.getElementById("quizContainer");
  container.innerHTML = "";
  let idx=0, score=0;
  const show = ()=>{
    const q = questions[idx];
    container.innerHTML = `<div class='card'><h3>Q${idx+1}. ${q.q}</h3>
      <div style='display:flex;flex-direction:column;gap:.5rem;margin-top:.8rem'>${q.options.map((o,i)=>`<button onclick='answer(${i})'>${o}</button>`).join("")}</div></div>`;
  };
  window.answer = (i)=>{
    const q = questions[idx];
    if(q.options[i]===q.a){ score++; }
    idx++;
    if(idx<questions.length) show(); else container.innerHTML = `<div class='card'><h3>Quiz Completed</h3><p>Score ${score}/${questions.length}</p></div>`;
  };
  show();
}
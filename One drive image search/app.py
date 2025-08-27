from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = Path(__file__).parent / 'Photo library'
CAPTIONS_FILE = DATA_DIR / 'captions.json'
INDEX_FILE = DATA_DIR / 'image_index.npz'
IMAGES_DIR = DATA_DIR / 'images'
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

app = FastAPI(title='Mini OneDrive Image Search')

# Mount images directory for static serving
app.mount('/images', StaticFiles(directory=str(IMAGES_DIR)), name='images')

model = SentenceTransformer(MODEL_NAME)
_index_embeddings = None
_index_filenames = None


def load_index():
    global _index_embeddings, _index_filenames
    if _index_embeddings is None:
        data = np.load(INDEX_FILE)
        _index_embeddings = data['embeddings']
        _index_filenames = data['filenames']
    return _index_embeddings, _index_filenames


def render_gallery(images, query=None, result=None):
    highlight = result
    cards = []
    for img in images:
        cls = 'thumb highlight' if img == highlight else 'thumb'
        cards.append('<div class="'+cls+'"><img loading="lazy" src="/images/'+img+'" alt="" /></div>')
    grid_html = '\n'.join(cards)
    q = query or ''
    hero_html = ''
    if highlight:
        hero_html = ('<section class="hero"><div class="hero-inner">'
                     '<img src="/images/'+highlight+'" alt="Result" />'
                     '<div class="hero-meta"><h2>Top match</h2><p>'+q+'</p></div>'
                     '</div></section>')
    logo_svg = ("<svg viewBox='0 0 64 64' fill='none' xmlns='http://www.w3.org/2000/svg'>"
                "<circle cx='32' cy='32' r='32' fill='url(#g)'/>"
                "<path d='M18 40c0-5.523 4.477-10 10-10h8c5.523 0 10 4.477 10 10v1a3 3 0 0 1-3 3H21a3 3 0 0 1-3-3v-1Z' fill='#fff'/>"
                "<path d='M24 22c0-4.418 3.582-8 8-8 3.34 0 6.21 2.053 7.4 4.969A7 7 0 0 1 46 26c0 3.866-3.134 7-7 7H28c-4.418 0-8-3.582-8-8Z' fill='#fff'/>"
                "<defs><linearGradient id='g' x1='0' y1='0' x2='64' y2='64' gradientUnits='userSpaceOnUse'><stop stop-color='#0f62fe'/><stop offset='1' stop-color='#0542a7'/></linearGradient></defs></svg>")
    html = (
        "<html lang='en'><head><title>OneDrive Style Image Search</title>"
        "<meta name='viewport' content='width=device-width,initial-scale=1' />"
        "<style>"
        ":root { --bg:#f6f8fb; --panel:#ffffff; --accent:#0a5bd8; --accent-hover:#0c6fff; --radius:10px; --text:#1c2331; --shadow:0 2px 4px rgba(0,0,0,.06),0 4px 12px rgba(0,0,0,.04); }"
        "@media (prefers-color-scheme: dark) { :root { --bg:#10161f; --panel:#1b2532; --text:#e6eaf0; --shadow:0 2px 6px rgba(0,0,0,.6); } }"
        "* { box-sizing:border-box; } body { margin:0; font-family: system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif; background:var(--bg); color:var(--text); -webkit-font-smoothing:antialiased; }"
        "header { padding:18px 32px 48px; background:linear-gradient(135deg,#0f62fe,#0542a7); color:#fff; position:relative; overflow:hidden; }"
        "header:before { content:''; position:absolute; inset:0; background:radial-gradient(circle at 70% 30%,rgba(255,255,255,.18),transparent 60%); pointer-events:none; }"
        ".brand { font-size:22px; font-weight:600; letter-spacing:.5px; margin:0 0 28px; display:flex; align-items:center; gap:10px; }"
        ".brand svg { width:30px; height:30px; }"
        ".search-wrapper { max-width:760px; margin:0 auto; }"
        "form.search { display:flex; gap:12px; background:rgba(255,255,255,.12); padding:10px 14px; border-radius:50px; backdrop-filter:blur(6px); box-shadow:0 4px 12px rgba(0,0,0,.15) inset,0 0 0 1px rgba(255,255,255,.25); }"
        "form.search input[type=text] { flex:1; background:transparent; border:none; outline:none; font-size:16px; color:#fff; font-weight:500; letter-spacing:.3px; }"
        "form.search input::placeholder { color:rgba(255,255,255,.65); font-weight:400; }"
        "form.search button { background:#fff; color:#0f62fe; font-weight:600; font-size:15px; padding:10px 22px; border:none; border-radius:40px; cursor:pointer; display:flex; align-items:center; gap:6px; transition:.18s background,.18s transform; box-shadow:0 2px 4px rgba(0,0,0,.18); }"
        "form.search button:hover { background:#e9f2ff; } form.search button:active { transform:translateY(1px); }"
        "main { max-width:1600px; margin:-32px auto 60px; padding:0 40px; }"
        ".hero { background:var(--panel); border-radius:var(--radius); padding:24px; margin:0 0 36px; box-shadow:var(--shadow); display:flex; align-items:center; }"
        ".hero-inner { display:flex; gap:28px; flex-wrap:wrap; align-items:center; width:100%; }"
        ".hero img { max-height:280px; max-width:100%; border-radius:14px; box-shadow:0 4px 18px rgba(0,0,0,.25); object-fit:cover; }"
        ".hero-meta h2 { margin:0 0 8px; font-size:20px; font-weight:600; }"
        ".hero-meta p { margin:0; font-size:15px; opacity:.85; word-break:break-word; }"
        ".grid { display:grid; gap:18px; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); }"
        ".thumb { position:relative; border-radius:14px; overflow:hidden; background:var(--panel); aspect-ratio:4/3; box-shadow:var(--shadow); transition:.25s transform,.25s box-shadow; cursor:pointer; }"
        ".thumb:before { content:''; position:absolute; inset:0; background:linear-gradient(145deg,rgba(255,255,255,.04),rgba(0,0,0,.15)); mix-blend-mode:overlay; pointer-events:none; }"
        ".thumb img { width:100%; height:100%; object-fit:cover; display:block; transition:.4s transform; }"
        ".thumb:hover img { transform:scale(1.05); }"
        ".thumb.highlight { box-shadow:0 0 0 3px var(--accent),0 4px 14px -2px rgba(15,98,254,.55); }"
        "footer { text-align:center; font-size:12px; opacity:.55; margin:42px 0 0; }"
        "@media (max-width:900px) { header { padding:16px 22px 56px; } main { padding:0 22px; margin-top:-40px; } .hero { padding:18px; } .grid { gap:14px; } }"
        "</style></head><body>"
        "<header><div class='brand'>"+logo_svg+"OneDrive Images</div>"
        "<div class='search-wrapper'><form class='search' method='get' action='/search'>"
        "<input type='text' name='q' value='"+q+"' placeholder='Search anything... (e.g. giraffes eating leaves)' autofocus />"
        "<button type='submit'>Search</button></form></div></header>"
        "<main>"+hero_html+"<section class='gallery'><div class='grid'>"+grid_html+"</div></section>"
        "<footer>Local demo • "+MODEL_NAME+"</footer></main></body></html>"
    )
    return html

@app.get('/', response_class=HTMLResponse)
async def root():
    with open(CAPTIONS_FILE, 'r') as f:
        data = json.load(f)
    images = [d['filename'] for d in data]
    return render_gallery(images)

@app.get('/search', response_class=HTMLResponse)
async def search(q: str = Query(..., description='Search query')):
    emb, fns = load_index()
    query_emb = model.encode(q, convert_to_numpy=True, normalize_embeddings=True)
    sims = emb @ query_emb
    top_idx = int(np.argmax(sims))
    top_fn = fns[top_idx]
    # Return gallery but highlight only top result (show all to enable scrolling)
    with open(CAPTIONS_FILE, 'r') as f:
        data = json.load(f)
    images = [d['filename'] for d in data]
    return render_gallery(images, query=q, result=top_fn)

# For programmatic API
@app.get('/api/search')
async def api_search(q: str = Query(...)):
    emb, fns = load_index()
    query_emb = model.encode(q, convert_to_numpy=True, normalize_embeddings=True)
    sims = emb @ query_emb
    top_idx = int(np.argmax(sims))
    return {"query": q, "top_filename": fns[top_idx], "score": float(sims[top_idx])}

# Command to run: uvicorn app:app --reload --port 8000 (from this directory)

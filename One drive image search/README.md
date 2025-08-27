# Mini OneDrive Image Search

This subproject builds a text-to-image (top-1) search over the 50 sample images using a sentence-transformer model and serves a OneDrive-inspired UI.

## Steps

1. Install dependencies (ideally in a virtual environment):
```
pip install -r requirements.txt
```

2. Build the embedding index:
```
python build_index.py
```
This creates `Photo library/image_index.npz`.

3. Evaluate top-1 retrieval accuracy using all provided captions as queries:
```
python evaluate_index.py
```
Example output:
```
Top-1 accuracy using all captions as queries: 0.88 (220/250)
```
(Your exact score may vary slightly.)

4. Run the web app:
```
uvicorn app:app --reload --port 8000
```
Open http://127.0.0.1:8000 to scroll all images. Use the search bar; only the best match is visually highlighted and reported at top while the gallery remains scrollable.

## Notes
- Model: `all-MiniLM-L6-v2` (fast, lightweight). For potentially higher accuracy you can switch to `all-mpnet-base-v2` (update MODEL_NAME in the scripts) and rebuild the index.
- Index currently normalizes embeddings (cosine similarity via dot product). For very small dataset this is fine.
- UI keeps all images visible to enable scroll exploration while highlighting the top result; could be adapted to show only the top result if desired.
- API endpoint: `/api/search?q=your+query` returns JSON with filename and score.

## Possible Improvements
- Add top-k results list (with scores) beneath search bar.
- Add client-side filtering / lazy loading for large sets.
- Persist index metadata (e.g., embedding model name) for validation.
- Add CLIP-based multimodal model to embed images directly rather than text-only captions index.

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

DATA_DIR = Path(__file__).parent / 'Photo library'
CAPTIONS_FILE = DATA_DIR / 'captions.json'
INDEX_FILE = DATA_DIR / 'image_index.npz'
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


def load_captions():
    with open(CAPTIONS_FILE, 'r') as f:
        data = json.load(f)
    return data

def build_index():
    data = load_captions()
    model = SentenceTransformer(MODEL_NAME)
    filenames = []
    img_embeddings = []
    for item in data:
        caps = item.get('all_captions') or [item.get('caption', '')]
        # Encode all captions then mean-pool (embeddings are already normalized; mean then renormalize)
        cap_embs = model.encode(caps, batch_size=len(caps), show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
        mean_emb = cap_embs.mean(axis=0)
        # Renormalize mean vector
        mean_emb = mean_emb / (np.linalg.norm(mean_emb) + 1e-12)
        img_embeddings.append(mean_emb)
        filenames.append(item['filename'])
    embeddings = np.vstack(img_embeddings)
    np.savez_compressed(INDEX_FILE, embeddings=embeddings, filenames=np.array(filenames), model=np.array([MODEL_NAME]))
    print(f'Saved pooled index with {len(filenames)} images to {INDEX_FILE}')

if __name__ == '__main__':
    build_index()

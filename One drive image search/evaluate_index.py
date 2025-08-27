import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer, util

DATA_DIR = Path(__file__).parent / 'Photo library'
CAPTIONS_FILE = DATA_DIR / 'captions.json'
INDEX_FILE = DATA_DIR / 'image_index.npz'
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


def load_index():
    data = np.load(INDEX_FILE)
    return data['embeddings'], data['filenames']

def load_data():
    with open(CAPTIONS_FILE, 'r') as f:
        return json.load(f)


def evaluate():
    data = load_data()
    embeddings, filenames = load_index()
    model = SentenceTransformer(MODEL_NAME)
    filename_to_idx = {fn: i for i, fn in enumerate(filenames)}

    total = 0
    correct = 0
    for item in data:
        gold_fn = item['filename']
        # use all captions for queries
        for cap in item['all_captions']:
            query_emb = model.encode(cap, convert_to_numpy=True, normalize_embeddings=True)
            sims = np.dot(embeddings, query_emb)
            top_idx = int(np.argmax(sims))
            if filenames[top_idx] == gold_fn:
                correct += 1
            total += 1
    acc = correct / total if total else 0.0
    print(f'Top-1 accuracy using all captions as queries: {acc:.4f} ({correct}/{total})')

if __name__ == '__main__':
    evaluate()

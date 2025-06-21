# plagiarism_checker.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load a strong bi-encoder model
_model = SentenceTransformer('all-mpnet-base-v2')

def calculate_plagiarism_score(user_answer: str, ideal_answer: str):
    """
    Compute a plagiarism score (0–100%) as cosine similarity
    between embeddings of user_answer and ideal_answer.
    Returns (score, status_label, color_code).
    """
    # Embed both texts
    emb1, emb2 = _model.encode([user_answer, ideal_answer])
    sim = cosine_similarity([emb1], [emb2])[0][0]
    score = round(sim * 100, 2)

    if score <= 30:
        status = "✅ Likely Original"
        color = "#2ecc71"
    elif score <= 50:
        status = "⚠️ Possibly Paraphrased"
        color = "#f1c40f"
    else:
        status = "🚨 High Similarity"
        color = "#e74c3c"

    return score, status, color


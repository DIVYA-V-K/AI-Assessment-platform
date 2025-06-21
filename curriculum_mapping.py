import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Load syllabus data
syllabus = {
    "Mathematics": [
        "Algebra",
        "Calculus",
        "Probability",
        "Trigonometry"
    ],
    "Physics": [
        "Newton's Laws",
        "Thermodynamics",
        "Electromagnetism",
        "Quantum Mechanics"
    ],
    "Computer Science": [
        "Data Structures",
        "Algorithms",
        "Machine Learning",
        "Artificial Intelligence"
    ]
}

# Load Sentence Transformer model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

def preprocess_text(text):
    """ Convert text to lowercase and remove stopwords """
    return " ".join([token.lemma_ for token in nlp(text) if not token.is_stop])

def get_most_relevant_topic(question):
    """ Match question to the closest syllabus topic using semantic similarity """
    question_embedding = model.encode([question])

    best_match = None
    best_score = -1

    for subject, topics in syllabus.items():
        for topic in topics:
            topic_embedding = model.encode([topic])
            score = cosine_similarity(question_embedding, topic_embedding)[0][0]
            if score > best_score:
                best_score = score
                best_match = (subject, topic)

    return best_match, best_score

# Test with a sample question
question = "What are the laws of motion?"
subject_topic, confidence = get_most_relevant_topic(question)

print(f"Question: {question}")
print(f"Matched Subject: {subject_topic[0]}, Topic: {subject_topic[1]} (Confidence: {confidence:.2f})")

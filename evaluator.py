from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Load models once
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
judge = pipeline("text2text-generation", model="google/flan-t5-large")

# 🔍 Calculate cosine similarity
def calculate_similarity(user_answer, ideal_answer):
    user_embedding = similarity_model.encode(user_answer, convert_to_tensor=True)
    ideal_embedding = similarity_model.encode(ideal_answer, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(user_embedding, ideal_embedding).item()
    percentage_score = round(similarity_score * 100, 2)
    return percentage_score

# 📣 Simple feedback based on similarity score
def generate_feedback_based_on_score(score):
    if score > 85:
        return "✅ Excellent! Your answer closely matches the ideal response."
    elif score > 60:
        return "👍 Good effort. There's room for improvement in detail and explanation."
    elif score > 40:
        return "⚠️ Fair attempt. Consider elaborating your concepts more clearly."
    else:
        return "❌ Needs improvement. Please review the topic and try again."

# 🧠 Expert feedback from LLM based on specific skill
def get_feedback_from_expert(user_answer, ideal_answer, expert_role):
    prompt = (
        f"You are an AI expert specializing in {expert_role}. "
        f"Evaluate the student's answer compared to the ideal answer. "
        f"Provide detailed feedback to help the student improve.\n\n"
        f"Ideal Answer:\n{ideal_answer}\n\n"
        f"Student's Answer:\n{user_answer}\n\n"
        f"Your Feedback:"
    )
    result = judge(prompt, max_length=256, do_sample=False)[0]['generated_text']
    return result

# 🧑‍🏫 Collect structured feedback from multiple AI roles
def get_structured_feedback(user_answer, ideal_answer):
    expert_roles = [
        "Fact Checking",
        "Conceptual Understanding",
        "Language Clarity and Grammar",
        "Depth of Explanation",
        "Relevance and Coverage"
    ]
    feedback = {}
    for role in expert_roles:
        feedback[role] = get_feedback_from_expert(user_answer, ideal_answer, role)
    return feedback

# 🎯 Main evaluation function
def evaluate_answer(user_id, topic, question, user_answer, ideal_answer):
    similarity_score = calculate_similarity(user_answer, ideal_answer)
    simple_feedback = generate_feedback_based_on_score(similarity_score)
    structured_feedback = get_structured_feedback(user_answer, ideal_answer)

    # 🚫 Removed: log_user_performance(user_id, topic, question, similarity_score)

    return {
        "similarity_score": similarity_score,
        "simple_feedback": simple_feedback,
        "structured_feedback": structured_feedback
    }

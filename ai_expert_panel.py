from transformers import pipeline

# Load FLAN-T5
judge = pipeline("text2text-generation", model="google/flan-t5-large")

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

from sentence_transformers import SentenceTransformer, util
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load models
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
answer_generator_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", legacy=False)

def generate_ideal_answer(question):
    """Generate an ideal answer for the given question using AI."""
    prompt = f"Provide a clear, structured, and well-explained answer to this question: {question}"
    
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    output = answer_generator_model.generate(input_ids, max_length=150, num_return_sequences=1, do_sample=True)
    ideal_answer = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return ideal_answer

def evaluate_answer(user_answer, ideal_answer):
    """Compare user answer with AI-generated ideal answer, return a percentage score and feedback."""
    if not user_answer.strip():  # Handle empty answers
        return 0.0, "No answer provided. Please enter a response."

    user_embedding = similarity_model.encode(user_answer, convert_to_tensor=True)
    ideal_embedding = similarity_model.encode(ideal_answer, convert_to_tensor=True)

    # Compute cosine similarity (0 = no match, 1 = perfect match)
    similarity_score = util.pytorch_cos_sim(user_embedding, ideal_embedding).item()

    # Convert to percentage (0-100%)
    percentage_score = round(similarity_score * 100, 2)

    # Generate feedback based on score
    feedback = "Feedback not generated"
    if percentage_score > 85:
        feedback = "Excellent! Your answer is very accurate and detailed."
    elif percentage_score > 70:
        feedback = "Good job! Your answer is mostly correct but could use more details."
    elif percentage_score > 50:
        feedback = "Fair attempt. Your answer is somewhat correct but lacks key points."
    else:
        feedback = "Needs improvement. Your answer does not match the expected response. Consider revising."

    return percentage_score, feedback  # ✅ Always returns both values

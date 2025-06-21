from question_generator import generate_question
from answer_classifier import classify_answer
from evaluator import evaluate_answer

# Generate a question
topic = "Newton's Laws"
question = generate_question(topic)
print(f"Generated Question: {question}")

# Example user answer
user_answer = "Newton's first law states that an object in motion stays in motion unless acted upon by an external force."
correct_answer = "Newton's first law states that an object will remain at rest or in uniform motion unless acted upon by an external force."

# Classify the answer
classification, score = classify_answer(user_answer, correct_answer)

# Evaluate and provide feedback
similarity_score, feedback = evaluate_answer(user_answer, correct_answer)

# Print results
print(f"User Answer: {user_answer}")
print(f"Classification: {classification} (Similarity Score: {score:.2f})")
print(f"Evaluation Score: {similarity_score:.2f}")
print(f"Feedback: {feedback}")

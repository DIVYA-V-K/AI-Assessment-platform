from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the model and tokenizer
MODEL_NAME = "google/flan-t5-large"
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, legacy=False)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def generate_questions(prompt, num_questions=5):
    """Generate unique, high-quality questions from a prompt."""
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(
        input_ids,
        max_length=150,
        num_return_sequences=num_questions * 2,  # Generate extra for better filtering
        do_sample=True,
        temperature=0.9,
        top_p=0.85
    )
    questions = [tokenizer.decode(output, skip_special_tokens=True).strip() for output in outputs]

    # Filter and refine questions
    filtered_questions = list(set(filter(lambda q: len(q) > 20 and "?" in q, questions)))
    unique_questions = list(set(filtered_questions))[:num_questions]

    if not unique_questions:
        return ["No meaningful questions generated. Try refining your prompt."]
    
    return unique_questions

def generate_from_topic(topic, num_questions=5, difficulty="Medium", question_type="Theory"):
    """Generate questions from topic with specified difficulty and type (Theory/Code)."""
    difficulty = difficulty.lower()
    question_type = question_type.lower()

    if question_type == "code":
        level_prompt = (
            f"You are a software engineer trainer. Write {num_questions} practical coding questions "
            f"on the topic '{topic}'. Each question should require the user to write actual code. "
            f"Do not include theory-based or definition-style questions."
        )
    else:
        if difficulty == "easy":
            level_prompt = (
                f"You are a tutor. Write {num_questions} simple, factual, beginner-friendly theory questions "
                f"on the topic '{topic}'. Focus on definitions, key terms, and basic understanding."
            )
        elif difficulty == "medium":
            level_prompt = (
                f"You are a subject expert. Write {num_questions} moderately challenging, open-ended questions "
                f"on the topic '{topic}'. Focus on comprehension, reasoning, and concept understanding."
            )
        elif difficulty == "hard":
            level_prompt = (
                f"You are a university professor. Write {num_questions} advanced, in-depth theory questions "
                f"on the topic '{topic}'. Focus on application, critical thinking, and problem-solving."
            )
        else:
            level_prompt = (
                f"Write {num_questions} open-ended questions on the topic '{topic}'. Avoid MCQs and trivial definitions."
            )

    return generate_questions(level_prompt, num_questions)

def generate_from_text(text, num_questions=5, difficulty="Medium", question_type="Theory"):
    """Generate questions from text with difficulty and type (Theory/Code)."""
    difficulty = difficulty.lower()
    question_type = question_type.lower()
    truncated_text = text[:1500]

    if question_type == "code":
        level_prompt = (
            f"You are a coding mentor. Read the following content and generate {num_questions} code-based questions. "
            f"Each question should ask the user to implement or debug code related to the topic."
        )
    else:
        if difficulty == "easy":
            level_prompt = (
                f"You are a tutor. Read the passage below and generate {num_questions} simple, factual questions. "
                f"Focus on facts and basic concepts."
            )
        elif difficulty == "medium":
            level_prompt = (
                f"You are a knowledgeable teacher. Read the passage and generate {num_questions} comprehension-based questions. "
                f"Focus on explanations and conceptual understanding."
            )
        elif difficulty == "hard":
            level_prompt = (
                f"You are an expert examiner. Read the passage and generate {num_questions} challenging theory questions. "
                f"Focus on deep understanding, application, and analysis."
            )
        else:
            level_prompt = (
                f"Generate {num_questions} open-ended questions based on the following passage."
            )

    full_prompt = f"{level_prompt}\n\nPASSAGE:\n{truncated_text}"
    return generate_questions(full_prompt, num_questions)

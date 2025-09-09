import streamlit as st
import base64
import time
from pdf_processor import extract_text_from_pdf
from question_generator import generate_questions, generate_from_text, generate_from_topic
from evaluator import evaluate_answer
from answer_classifier import generate_ideal_answer
from plagiarism_checker import calculate_plagiarism_score
from proctoring import monitor_user_behavior, handle_alert_routes
from streamlit_ace import st_ace
from serpapi_search import search_serpapi

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #e0f0ff, #ffffff);
        background-attachment: fixed;
    }
    .main-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #4dabf7;
        padding: 10px;
        border-bottom: 2px solid #4dabf7;
    }
    .sub-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #4dabf7;
    }
    .stButton>button {
        background-color: #4dabf7;
        color: #ffffff;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #1b4965;
    }
    .question-box {
        background-color: #4dabf7;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #ffffff;
        margin-bottom: 10px;
        color: #ffffff;
        font-weight: bold;
    }
    .answer-box {
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session Initialization ---
for key, default in {
    "page": "home",
    "questions": [],
    "user_answers": {},
    "alert_count": 0,
    "start_time": None,
    "duration": 0,
    "difficulty": "Medium",
    "question_type": "Theory",
    "user_id": "guest",
    "topic": "custom-topic",
    "avg_score": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Proctoring Alerts ---
handle_alert_routes()

# --- HOME PAGE ---
if st.session_state["page"] == "home":
    st.markdown("<h1 class='main-title'>Create New Test</h1>", unsafe_allow_html=True)

    test_type = st.radio("Select Input Type:", ["Choose from Predefined Programming Topics", "Enter Custom Topic"])

    num_questions = st.slider("Select number of questions:", min_value=1, max_value=20, value=5)
    difficulty = st.selectbox("Select difficulty level:", ["Easy", "Medium", "Hard"])
    question_type = st.radio("Choose question type:", ["Theory", "Code"])

    st.session_state.update({
        "num_questions": num_questions,
        "difficulty": difficulty,
        "question_type": question_type,
        "duration": num_questions * 90
    })

    # 1️⃣ Predefined Programming Topics
    if test_type == "Choose from Predefined Programming Topics":
        language = st.selectbox("Choose a Programming Language:", ["Java", "Python", "C++"])

        topics = {
            "Java": [
                "Introduction to Java", "Data Types and Variables", "Control Flow Statements",
                "Object-Oriented Programming", "Inheritance", "Polymorphism",
                "Exception Handling", "Collections Framework"
            ],
            "Python": [
                "Introduction to Python", "Data Types and Variables", "Control Structures",
                "Functions and Modules", "Object-Oriented Programming", "File Handling",
                "Exception Handling", "Libraries (NumPy, Pandas)"
            ],
            "C++": [
                "Introduction to C++", "Control Statements", "Functions and Arrays",
                "Pointers", "Object-Oriented Programming", "Inheritance", "Polymorphism",
                "Templates and STL"
            ]
        }

        selected_topics = st.multiselect("Select Subtopics:", topics[language])

        if st.button("Generate Questions"):
            if selected_topics:
                full_prompt = f"Generate {num_questions} questions from the following {language} topics: {', '.join(selected_topics)}."
                st.session_state["topic"] = ", ".join(selected_topics)
                st.session_state["questions"] = generate_from_topic(full_prompt, num_questions, difficulty, question_type)
                st.session_state["page"] = "assessment"
                st.session_state["start_time"] = time.time()
                st.rerun()
            else:
                st.warning("Please select at least one subtopic.")

    # 2️⃣ Custom Topic
    else:
        topic = st.text_input("Enter a Custom Topic:")
        if topic:
            st.session_state["topic"] = topic

        if st.button("Generate Questions from Topic"):
            if topic:
                st.session_state["questions"] = generate_from_topic(
                    topic, num_questions, difficulty, question_type
                )
                st.session_state["page"] = "assessment"
                st.session_state["start_time"] = time.time()
                st.rerun()
            else:
                st.warning("Please enter a topic.")

    # 📄 PDF Upload
    st.markdown("<h2 class='sub-title'>Or Upload a PDF</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        extracted_text = extract_text_from_pdf("temp.pdf")
        st.subheader("Extracted Text Preview:")
        st.text_area("Text from PDF", extracted_text[:2000], height=250)

        if st.button("Generate Questions from PDF"):
            st.session_state["questions"] = generate_from_text(
                extracted_text, num_questions, difficulty, question_type
            )
            st.session_state["page"] = "assessment"
            st.session_state["start_time"] = time.time()
            st.rerun()

# You can now continue with ASSESSMENT, RESULTS, SUMMARY pages unchanged


# --- ASSESSMENT PAGE ---
elif st.session_state["page"] == "assessment":
    monitor_user_behavior()

    remaining = st.session_state["duration"] - int(time.time() - st.session_state["start_time"])
    if remaining <= 0:
        st.warning("⏰ Time's up! Submitting your answers...")
        st.session_state["user_answers"] = {
            q: st.session_state.get(f"code_{i}" if st.session_state["question_type"] == "Code" else f"answer_{i}", "")
            for i, q in enumerate(st.session_state["questions"])
        }
        st.session_state["page"] = "results"
        st.rerun()
    else:
        mins, secs = divmod(remaining, 60)
        st.markdown(f"⏱ **Time Remaining: {mins:02d}:{secs:02d}**")

    st.markdown("<h1 class='main-title'>Answer the Questions Below</h1>", unsafe_allow_html=True)

    if st.session_state["questions"]:
        for idx, question in enumerate(st.session_state["questions"]):
            st.markdown(f"<div class='question-box'><b>Question {idx+1}:</b> {question}</div>", unsafe_allow_html=True)
            if st.session_state["question_type"] == "Code":
                st_ace(placeholder="Type your code here...", language="python", theme="monokai", key=f"code_{idx}", height=200)
            else:
                st.text_area(f"Enter your answer for Question {idx+1}:", key=f"answer_{idx}")
    else:
        st.warning("No questions generated. Please go back and try again.")

    if st.button("Submit Answers"):
        st.session_state["user_answers"] = {
            q: st.session_state.get(f"code_{i}" if st.session_state["question_type"] == "Code" else f"answer_{i}", "")
            for i, q in enumerate(st.session_state["questions"])
        }
        st.session_state["page"] = "results"
        st.rerun()

# --- RESULTS PAGE ---
elif st.session_state["page"] == "results":
    st.markdown("<h1 class='main-title'>Results & Feedback</h1>", unsafe_allow_html=True)
    total_score = 0

    if st.session_state["user_answers"]:
        for idx, (question, user_answer) in enumerate(st.session_state["user_answers"].items()):
            ideal_answer = generate_ideal_answer(question)
            result = evaluate_answer(
                st.session_state["user_id"],
                st.session_state["topic"],
                question,
                user_answer,
                ideal_answer
            )
            score = result["similarity_score"]
            feedback = result["simple_feedback"]
            expert_feedback = result["structured_feedback"]
            plagiarism_score, status_label, color_code = calculate_plagiarism_score(user_answer, ideal_answer)

            total_score += score

            st.markdown(f"<div class='question-box'><b>Question {idx+1}:</b> {question}</div>", unsafe_allow_html=True)
            if st.session_state["question_type"] == "Code":
                st.code(user_answer, language="python")
            else:
                st.markdown(f"<div class='answer-box'><b>Your Answer:</b> {user_answer}</div>", unsafe_allow_html=True)

            st.markdown(f"<div class='answer-box'><b>AI-Generated Ideal Answer:</b> {ideal_answer}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-box'><b>Your Score:</b> {score}%</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='answer-box'><b>Feedback:</b> {feedback}</div>", unsafe_allow_html=True)

            with st.expander("🔍 Expert Feedback Panel"):
                for expert, fb in expert_feedback.items():
                    st.markdown(f"<div class='answer-box'><b>{expert}:</b><br>{fb}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background-color: {color_code}; padding: 10px; border-radius: 8px; font-weight: bold; color: white; margin-bottom: 10px;'>
            Plagiarism Score: {plagiarism_score}% — {status_label}
            </div>
            """, unsafe_allow_html=True)

        avg_score = round(total_score / len(st.session_state["user_answers"]), 2)
        st.session_state["avg_score"] = avg_score

        # 👉 Add NEXT button
        if st.button("Next"):
            st.session_state["page"] = "summary"
            st.rerun()
    else:
        st.warning("No answers submitted. Please try again.")

# --- SUMMARY PAGE ---
elif st.session_state["page"] == "summary":
    st.markdown("<h1 class='main-title'>📊 Overall Performance Summary</h1>", unsafe_allow_html=True)
    avg_score = st.session_state["avg_score"]

    st.markdown(f"### 🧾 Overall Score: **{avg_score}%**")

    if avg_score > 85:
        remark = "🌟 Outstanding performance across all questions!"
    elif avg_score > 70:
        remark = "✅ Good job! You're doing well."
    elif avg_score > 50:
        remark = "⚠️ Fair performance. Room for improvement."
    else:
        remark = "❌ Needs significant improvement. Keep practicing."

    st.markdown(f"### 🧠 Final Remark: **{remark}**")

    # --- SERP API ---
    st.markdown("## 🌐 Additional Learning")
    st.markdown("<h2 class='sub-title'>🔍 Search with SERP API</h2>", unsafe_allow_html=True)
    query = st.text_input("Enter your search query:", key="serp_query")
    if query:
        with st.spinner("Searching..."):
            results = search_serpapi(query)
        st.markdown("### Search Results:")
        if 'error' in results:
            st.error(f"Error: {results['error']}")
        else:
            for result in results.get('organic_results', []):
                st.markdown(f"**{result.get('title', '')}**")
                st.markdown(f"[Link]({result.get('link', '')})")
                st.markdown(f"{result.get('snippet', '')}")
                st.write("---")

    if st.button("Start New Assessment"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["page"] = "home"
        st.rerun()

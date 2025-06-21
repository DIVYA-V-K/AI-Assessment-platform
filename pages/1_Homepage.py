import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="AIdeate – Home", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        /* App background and layout */
        .stApp {
            background: linear-gradient(to bottom right, #e0f0ff, #ffffff);
            background-attachment: fixed;
        }
        /* Top-right navigation buttons */
        .top-right {
            position: absolute;
            top: 1.5rem;
            right: 2rem;
            z-index: 999;
        }
        .nav-link {
            color: #1f4ed8;
            background: transparent;
            padding: 0.5rem 1rem;
            margin-left: 0.5rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.95rem;
            text-decoration: none;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }
        .nav-link:hover {
            background-color: #1f4ed8;
            color: white;
            border: 1px solid #1f4ed8;
        }
        /* Footer style */
        .footer {
            text-align: center;
            padding: 2rem;
            color: gray;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Top-right Login/Signup Buttons ---
st.markdown("""
    <div class="top-right">
        <a href="/pages/Login.py" class="nav-link">Login</a>
        <a href="/pages/Signup.py" class="nav-link">Sign Up</a>
    </div>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
    <div style='text-align:center; margin-top: 3rem;'>
        <div style='font-size: 4rem; font-weight: bold; color: #1f4ed8;'>AIdeate</div>
        <div style='font-size: 1.3rem; margin-top: 0.8rem;'>
            <i>Powered by Navigate Labs</i> — Create intelligent assessments, evaluate responses, and personalize learning experiences.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Spacer ---
st.markdown("<div style='height: 5rem;'></div>", unsafe_allow_html=True)

# --- Key Features Heading ---
st.markdown("<h2 style='text-align:center; margin-bottom: 2rem;'>🔑 Key Features</h2>", unsafe_allow_html=True)

# --- Three Columns for Features ---
col1, col2, col3 = st.columns(3)

# --- Feature Card Template ---
def feature_card(title, description):
    st.markdown(f"""
        <div style="
            background-color:white;
            border-radius:15px;
            padding:24px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            min-height:260px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <h4 style="color:#1f4ed8;">{title}</h4>
            <p style="margin-top: 0.5rem;">{description}</p>
        </div>
    """, unsafe_allow_html=True)

# --- Feature Cards ---
with col1:
    feature_card("🧠 AI-Powered Question Creator",
                 "Generate high-quality questions from topics or PDFs using Hugging Face LLMs. Ideal for educators and exam designers.")

with col2:
    feature_card("📊 Smart Analytics",
                 "Automatically evaluate student answers using semantic similarity, clarity checks, and performance metrics.")

with col3:
    feature_card("💡 Personalized Feedback",
                 "Receive instant model answers, similarity scores, feedback, and plagiarism detection — tailored to each student.")

# --- Footer ---
st.markdown("""
    <div class="footer">
        ©️ 2025 <b>AIdeate</b> — Built with ❤️ by Navigate Labs
    </div>
""", unsafe_allow_html=True)

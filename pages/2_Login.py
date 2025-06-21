import streamlit as st

st.set_page_config(page_title="AIdeate Login", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .logo { font-size: 2.5em; font-weight: bold; color: #1f4ed8; margin-bottom: 10px; text-align: center; }
    .tagline { color: #555; font-size: 1rem; margin-bottom: 20px; text-align: center; }
    .login-heading { text-align: center; font-size: 1.4rem; color: #1f4ed8; margin-bottom: 0.5rem; }
    .login-instruction { text-align: center; margin-bottom: 15px; color: #555; }
    .forgot-password { text-align: right; margin-top: 5px; margin-bottom: 10px; width: 100%; }
    .forgot-password a { color: #1f4ed8; text-decoration: none; font-size: 0.9rem; }
    .button-wrapper { display: flex; justify-content: center; width: 20%; margin-top: 1rem; }
    .stButton button { width: 100%; background-color: #1f4ed8; color: white; border: none; padding: 0.75rem 1rem; border-radius: 8px; font-size: 1rem; font-weight: 500; transition: background-color 0.3s ease; }
    .stButton button:hover { background-color: #003f7f; }
    </style>
""", unsafe_allow_html=True)

# --- Page Content ---
st.markdown('<div class="logo">AIdeate</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">AI-powered ideation platform</div>', unsafe_allow_html=True)

st.markdown('<div class="login-heading">Login</div>', unsafe_allow_html=True)
email = st.text_input("Email", placeholder="you@example.com")
password = st.text_input("Password", type="password")

login_button = st.button("Login")

if login_button:
    st.info(f"Attempting to log in with email: {email}")

st.markdown('<div class="forgot-password"><a href="#">Forgot password?</a></div>', unsafe_allow_html=True)

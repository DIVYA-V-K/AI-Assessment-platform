import streamlit as st

st.set_page_config(page_title="AIdeate Signup", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .logo { font-size: 2.5em; font-weight: bold; color: #1f4ed8; margin-bottom: 10px; text-align: center; }
    .signup-heading { text-align: center; font-size: 1.6rem; color: #1f4ed8; margin-bottom: 0.5rem; }
    .form-container { display: flex; flex-direction: column; align-items: center; width: 50%; margin: auto; }
    .stTextInput input { border-radius: 8px; border: 1px solid #ccc; padding: 0.6rem; font-size: 1rem; width: 100%; }
    .button-container { display: flex; justify-content: center; width: 100%; margin-top: 1.5rem; }
    .stButton button { background-color: #1f4ed8; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-size: 1rem; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# --- Page Content ---
st.markdown('<div class="logo">AIdeate</div>', unsafe_allow_html=True)
st.markdown('<div class="signup-heading">Create an account to get started</div>', unsafe_allow_html=True)

st.markdown('<div class="form-container">', unsafe_allow_html=True)

# Centered labels
full_name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

create_account_button = st.button("Create Account")

if create_account_button:
    st.info(f"Account created for: {full_name}")

st.markdown('</div>', unsafe_allow_html=True)

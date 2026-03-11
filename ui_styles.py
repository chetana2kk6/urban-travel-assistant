import streamlit as st

def apply_styles():

    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Remove default Streamlit spacing */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(90deg,#0F6CBD,#1CA7EC);
        padding:30px;
        border-radius:10px;
        color:white;
        margin-bottom:20px;
    }
    .login-container {
    max-width: 450px;
    margin: auto;
}
    /* Style the form area directly */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        background:#F4F6F8;
        padding:20px;
        border-radius:8px;
        box-shadow:0px 2px 8px rgba(0,0,0,0.05);
    }

    /* Button styling */
    .stButton>button {
        background-color:#0F6CBD;
        color:white;
        font-weight:600;
        border-radius:6px;
        padding:8px 20px;
    }

    </style>
    """, unsafe_allow_html=True)
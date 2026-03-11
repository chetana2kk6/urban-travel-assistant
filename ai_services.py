import os
from google import genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)


def ai_response(prompt: str):

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=prompt
        )

        return response.text

    except Exception:
        return "⚠️ AI service is temporarily unavailable."


@st.cache_data(show_spinner=False)
def cached_ai_response(prompt):
    return ai_response(prompt)


def nearby_experience_places(destination, experience):

    prompt = f"""
    The user is traveling to {destination} and wants a {experience} experience.
    Suggest 4–6 nearby or easily reachable places.
    Return bullet points.
    """

    return ai_response(prompt)


def get_ai_info(prompt):

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=prompt
        )

        return response.text

    except Exception:
        return "⚠️ AI service temporarily unavailable."
import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Safety Settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Generation Configuration
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1500,
    "response_mime_type": "text/plain",
    "frequency_penalty": 0.4,
    "presence_penalty":0.5,
}

# Gemini Model
model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                               safety_settings=safety_settings,
                               generation_config=generation_config)

# Ensure user data exists
if "user_data" not in st.session_state or not st.session_state["user_data"]:
    st.warning("Please log in and complete previous features first.")
    st.stop()

# Retrieve stored details from Features 1-3
user_data = st.session_state["user_data"]
user_name = user_data["name"]
job_role = user_data["job_role"]
current_skills = user_data["skills"]
skill_analysis = user_data.get("skill_mapping_results", "No analysis found")
learning_recommendations = user_data.get("learning_recommendations", "No learning data available")
skill_gap_analysis = user_data.get("skill_gap_analysis", "No gap analysis available")

# UI Header
st.header("🚀 AI-Powered Career Path Prediction", divider='rainbow')
st.write(f"**User:** {user_name}")
st.write(f"**Job Role:** {job_role}")
st.write(f"**Current Skills:** {current_skills}")

# AI Career Path Prediction
def predict_career_path(existing_skills, skill_gap_report, job_role, model):
    prompt = f"""
    You are an AI Career Advisor helping a {job_role} progress in their career.

    - Current skills: {existing_skills}
    - Skill gaps: {skill_gap_report}

    Predict an optimal **career path**:
    - Define potential job roles in the next 5 years.
    - Outline skills needed for each stage.
    - Provide salary growth expectations.
    - Recommend strategic career moves.
    """
    response = model.generate_content(prompt)
    return response.text

# Button to generate AI-powered career path prediction
if st.button("🚀 Predict Career Path"):
    with st.spinner("Analyzing Career Path..."):
        career_path_report = predict_career_path(current_skills, skill_gap_analysis, job_role, model)
        st.session_state.user_data["career_recommendations"] = career_path_report  # Store for tracking
        def stream_output():
            for word in career_path_report.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.subheader(f"📌 AI-Generated Career Path Prediction for {user_name}")
        st.write_stream(stream_output())

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
    "max_output_tokens": 2000,
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

# Retrieve stored details from Features 1 & 2
user_data = st.session_state["user_data"]
user_name = user_data["name"]
job_role = user_data["job_role"]
current_skills = user_data["skills"]
skill_rating = user_data.get("skill_rating", "Not rated")
skill_analysis = user_data.get("skill_mapping_results", "No analysis found")
learning_recommendations = user_data.get("learning_recommendations", "No learning data available")

# UI Header
st.header("📊 AI-Powered Skill Gap Analysis", divider='rainbow')
st.write(f"**User:** {user_name}")
st.write(f"**Job Role:** {job_role}")
st.write(f"**Current Skills:** {current_skills}")
st.write(f"**Skill Rating:** {skill_rating}/10")

# AI Skill Gap Analysis
def analyze_skill_gap(existing_skills, learning_paths, job_role, model):
    prompt = f"""
    You are an AI HR Expert analyzing skill gaps for a {job_role}.

    - Current skills: {existing_skills}
    - Suggested learning paths: {learning_paths}

    Generate a **structured skill gap report**:
    - Identify key missing skills.
    - Provide industry benchmarks.
    - Rate urgency levels (High, Medium, Low) for each missing skill.
    """
    response = model.generate_content(prompt)
    return response.text

# Button to generate AI-powered skill gap analysis
if st.button("🔍 Analyze Skill Gaps"):
    with st.spinner("Analyzing Skill Gaps..."):
        skill_gap_report = analyze_skill_gap(current_skills, learning_recommendations, job_role, model)
        st.session_state.user_data["skill_gap_analysis"] = skill_gap_report  # Store for tracking

        def stream_output():
            for word in skill_gap_report.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.subheader(f"📌 AI-Generated Skill Gap Analysis for {user_name}")
        st.write_stream(stream_output())

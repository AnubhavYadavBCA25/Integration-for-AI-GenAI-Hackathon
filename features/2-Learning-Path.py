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
    st.warning("Please log in and complete Skill Mapping first.")
    st.stop()

# Retrieve stored details from Feature 1
user_data = st.session_state["user_data"]
user_name = user_data["name"]
job_role = user_data["job_role"]
current_skills = user_data["skills"]
resume_text = user_data.get("resume_text", "No resume data found")
skill_rating = user_data.get("skill_rating", "Not rated")
skill_analysis = user_data.get("skill_mapping_results", "No analysis found")

# UI Header
st.header("📚 AI-Powered Learning Paths", divider='rainbow')
st.write(f"**User:** {user_name}")
st.write(f"**Job Role:** {job_role}")
st.write(f"**Current Skills:** {current_skills}")
st.write(f"**Skill Rating:** {skill_rating}/10")
st.write(f"**Extracted Resume Data:** {resume_text[:500]}...")  # Show first 500 chars


# AI Learning Recommendations
def recommend_learning_path(existing_skills, missing_skills, job_role, model):
    prompt = f"""
    You are an AI Career Coach helping a {job_role} upskill.

    - Current skills: {existing_skills}
    - Identified skill gaps: {missing_skills}

    Recommend a **personalized learning path**:
    - **Online Courses**
    - **Certifications**
    - **Mentorship Programs**
    - provide links to resources.

    Provide difficulty levels (**Beginner, Intermediate, Advanced**) and estimated completion time.
    """
    response = model.generate_content(prompt)
    return response.text

# Button to get AI-powered learning recommendations
if st.button("🎯 Get AI-Powered Learning Recommendations"):
    with st.spinner("Generating Learning Recommendations..."):
        learning_recs = recommend_learning_path(current_skills, skill_analysis, job_role, model)
        st.session_state.user_data["learning_recommendations"] = learning_recs  # Store for tracking
        
        def stream_output():
            for word in learning_recs.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.subheader(f"📌 AI-Suggested Learning Paths for {user_name}")
        st.write_stream(stream_output())

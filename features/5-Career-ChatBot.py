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
    "max_output_tokens": 1000,
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

# Retrieve stored details from Features 1-5
user_data = st.session_state["user_data"]
user_name = user_data["name"]
job_role = user_data["job_role"]
current_skills = user_data["skills"]

# UI Header
st.header("💬 AI Career Chatbot", divider="rainbow")
st.write(f"**User:** {user_name}")
st.write(f"**Job Role:** {job_role}")
st.write(f"**Current Skills:** {current_skills}")

# Career Chatbot Function
def chat_with_ai(user_question, job_role, existing_skills, model):
    prompt = f"""
    You are an AI Career Assistant helping a {job_role} with career guidance.

    - User's current skills: {existing_skills}
    - User's question: {user_question}

    Provide a detailed, insightful response with actionable advice.
    """
    response = model.generate_content(prompt)
    return response.text

# Chatbot UI
user_question = st.text_area("💬 Ask your career-related question:")
if st.button("🔍 Get AI Response"):
    with st.spinner("⏳ Generating AI Response..."):
        if user_question.strip() == "":
            st.warning("⚠️ Please enter a question.")
            st.stop()
        else:
            ai_response = chat_with_ai(user_question, job_role, current_skills, model)
            def stream_output_ai_text():
                for word in ai_response.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            st.subheader(f"📌 AI Response for {user_name}")
            st.write_stream(stream_output_ai_text())

            # Store chatbot interaction in session state
            if "chatbot_history" not in st.session_state.user_data:
                st.session_state.user_data["chatbot_history"] = []

            st.session_state.user_data["chatbot_history"].append({"question": user_question, "response": ai_response})

import fitz
import os
import time
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# GOOGLE_API_KEY = os.getenv("GOOGLE_KEY_API")
genai.configure(api_key=GOOGLE_API_KEY)

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

# System Instructions
sys_intructions = {"""
            Role: The AI model acts as an Intelligent Skill Mapping & Career Development Assistant, analyzing user-provided data (resume, self-assessment, and performance review) to extract skills, identify gaps, and provide personalized career insights.

            Response Guidelines:

                1. Skill Extraction & Categorization:

                - Extract hard skills (e.g., Python, SQL, Data Analysis) and soft skills (e.g., Leadership, Communication) from the resume and performance review.
                - Categorize skills into Beginner, Intermediate, and Advanced levels based on provided data.
                
                4. Personalized Recommendations:

                - Suggest relevant courses, certifications, or mentorship programs based on the identified gaps.
                - Recommend career path options based on current skills and aspirations.
                
                5. Clear & Actionable Feedback:

                - Responses should be concise, easy to understand, and structured.
                - Provide next steps for upskilling, including resources and estimated effort required.
                - Maintain a motivational and supportive tone to encourage learning.
"""}

# Load Gemini Model
model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings,
                              system_instruction=sys_intructions)
    
# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file using PyMuPDF."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

# Function to analyze resume using Gemini AI
def analyze_user_data(resume_text, model, performance_review, skill_rating, job_role, existing_skills):
    chat = model.start_chat(history=[])
    prompt = f"""
    You are an AI HR Specialist analyzing an employee working as a {job_role}.
    Analyze the following resume text, skill rating and performance review:
    Resume:
    {resume_text}

    Performance Review:
    {performance_review}

    Skill Rating: {skill_rating}

    Existing Skills: {existing_skills}
    """
    response = chat.send_message(prompt, stream=True)
    extracted_info = ""
    for chunk in response:
        if chunk.text:
            extracted_info += chunk.text
    return extracted_info

st.header("Skill Mapping: Analyze Employee Skills with AI", divider='rainbow')

# Ensure user data is available
if "user_data" not in st.session_state or not st.session_state["user_data"]:
    st.warning("Please log in and enter your details.")
    st.stop()

# Retrieve user details
user_data = st.session_state["user_data"]
user_name = user_data["name"]
job_role = user_data["job_role"]
current_skills = user_data["skills"]

# UI Header
st.title("🔍 AI-Powered Skill Mapping")
st.write(f"**User:** {user_name}")
st.write(f"**Job Role:** {job_role}")
st.write(f"**Current Skills:** {current_skills}")

with st.form(key='skill_mapping'):
    resume = st.file_uploader("Upload a Resume/CV*", type=['pdf'], help="Upload your resume/cv in PDF format")

    skill_rating = st.slider("Rate your current skill level (1-10)*", 1, 10, 5, help="Rate your current skill level on a scale of 1-10")
    
    performance_review = st.text_area("Enter feedback from your manager or self-review*", placeholder="Enter feedback from your manager or self-review")

    st.markdown("*Required**")
    # Submit button
    submitted = st.form_submit_button("Submit")

if submitted:
    if not resume or not skill_rating or not performance_review:
        st.error("Please Enter all the required fields")
        st.stop()
    else:
        st.success("Data Submitted Successfully!")
st.divider()

with st.spinner("Processing..."):
    if resume:
        resume_text = extract_text_from_pdf(resume)
        if resume_text and performance_review and skill_rating:
            analysis_result = analyze_user_data(resume_text, model, performance_review, skill_rating, job_role, current_skills)
            def stream_output_ai_text():
                    for word in analysis_result.split(" "):
                        yield word + " "
                        time.sleep(0.02)
            st.subheader("Analysis Result:")
            st.write_stream(stream_output_ai_text())

            # Save resume details & AI analysis in session state
            st.session_state.user_data["resume_text"] = resume_text
            st.session_state.user_data["skill_rating"] = skill_rating
            st.session_state.user_data["skill_mapping_results"] = analysis_result
            
    else:
        st.warning("Please upload a resume to analyze")
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
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
    "max_output_tokens": 1500,
    "response_mime_type": "text/plain",
    "frequency_penalty": 0.4,
    "presence_penalty":0.5,
}

# System Instructions
sys_instructions = """
                    🔹 Role: The AI model acts as a Skill Gap Analyzer, comparing the user's current skills, experience, and career goals with industry benchmarks to identify missing skills and suggest relevant upskilling opportunities.

                    🔹 Input Expectations:
                        The model will analyze the following user-provided data:

                        1. Current Role & Experience (e.g., "Data Scientist, 3 years")
                        2. Technical Skills & Self-Assessment (e.g., Python, SQL, ML – rated proficiency)
                        3. Desired Future Role & Industry (e.g., "ML Engineer in Finance")
                        4. Preferred Upskilling Mode (e.g., Online Courses, Bootcamps)
                    
                    🔹 Response Guidelines:

                        1. Identify Skill Gaps:

                        - Compare user’s current skills with typical requirements for the desired role.
                        - Highlight top missing skills essential for career transition.
                        
                        2. Recommend Focus Areas:

                        - Prioritize 2-3 key skills that will have the most impact.
                        - Avoid overwhelming users with too many recommendations.
                        
                        3. Provide Actionable Learning Suggestions:

                        - Suggest a few learning resources (e.g., online courses, certifications) tailored to user preferences.
                        - Ensure recommendations align with the chosen upskilling mode (e.g., Bootcamps for hands-on learning).
                        
                        4. Maintain Clarity & Simplicity:

                        - Keep responses concise and easy to understand.
                        - Focus only on relevant insights instead of listing generic suggestions.
                        - Ensure the tone is motivational and practical.
                    
                    Example Output: "To transition into an ML Engineer role in Finance, focus on improving Deep Learning and Cloud Computing skills. Recommended path: Take 'Deep Learning Specialization' by Andrew Ng (Online Course) and earn an AWS Cloud Practitioner Certification."
"""

# Load Gemini Model
model = genai.GenerativeModel(model_name="gemini-2.0-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings,
                              system_instruction=sys_instructions)

# Streamlit App
st.header("🔍 Real-Time Skill Gap Analysis", divider='rainbow')

st.write("Fill in the details to analyze your current skills vs. industry benchmarks.")

# Create a form for user inputs
with st.form("skill_gap_form"):
    st.subheader("🎯 Your Current Role & Experience")
    role = st.text_input("Enter your current job role:*", placeholder="E.g., Data Scientist, Software Engineer")
    experience = st.slider("Years of experience in this role:*", 0, 20, 3)
    
    st.subheader("📊 Technical Skills Assessment")
    primary_skills = st.text_input("Enter your core skills (separated by commas):*", placeholder="e.g., Python, SQL, Machine Learning")
    skill_proficiency = st.slider("Rate your proficiency in your selected skills (1-10):*", 1, 10, 5)
    
    st.subheader("📌 Career Goals & Industry Alignment")
    target_role = st.text_input("Enter your desired future role:*", placeholder="e.g., ML Engineer, Data Analyst")
    industry = st.selectbox("Select your industry:*", ["Finance", "Healthcare", "Tech", "E-commerce", "Education", "Other"])
    upskilling_preference = st.radio("Preferred upskilling mode:*", ["Online Courses", "Bootcamps", "Mentorship", "Self-Learning"])
    
    st.markdown("*Required**")
    # Submit button
    submitted = st.form_submit_button("Submit")

if submitted:
    if not role or not experience or not primary_skills or not skill_proficiency or not target_role or not industry or not upskilling_preference:
        st.warning("Please fill in all the required fields.")
        st.stop()
    else:
        st.success("Your details have been submitted successfully!")
st.divider()

with st.spinner("Processing..."):
    if role and experience and primary_skills and skill_proficiency and target_role and industry and upskilling_preference is not None:
        prompt = f"""
                Do Skill Gap Analysis Based on following Inputs:
                Current Role: {role},
                Experience: {experience},
                Current Primary Skills: {primary_skills},
                Skill Proficiency Rating: {skill_proficiency},
                Target Role Want to Get into: {target_role},
                Industry want to switch in: {industry},
                Preference of Upskilling: {upskilling_preference}
        """
        response = model.generate_content(prompt)
        st.subheader("Hi, Here is Your Skills Gap Analysis")
        output = response.text
        def stream_output():
            for word in output.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.write_stream(stream_output())

    else:
        st.warning("Please fill all the required fields.")
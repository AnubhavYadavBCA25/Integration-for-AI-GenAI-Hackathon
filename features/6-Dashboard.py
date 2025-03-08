import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
import time

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

# Load Gemini Model
model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Ensure user data exists
if "user_data" not in st.session_state or not st.session_state["user_data"]:
    st.warning("Please log in and complete all features first.")
    st.stop()

# Retrieve stored data from previous features
user_data = st.session_state["user_data"]
user_name = user_data["name"]
job_role = user_data["job_role"]
current_skills = user_data["skills"]
skill_analysis = user_data.get("skill_mapping_results", "No analysis found")
learning_recommendations = user_data.get("learning_recommendations", "No learning data available")
skill_gap_analysis = user_data.get("skill_gap_analysis", "No gap analysis available")
career_recommendations = user_data.get("career_recommendations", "No career data available")
chatbot_history = user_data.get("chatbot_history", [])

# UI Header
st.header("📊 AI-Powered Personalized Dashboard", divider='rainbow')
st.write(f"### Welcome, {user_name}!")
st.write(f"🚀 **Job Role:** {job_role}")

st.markdown("---")

# AI-Generated Career Summary
def generate_dashboard_insights():
    prompt = f"""
    You are an AI analyzing a user's complete career progression.

    - The user has completed skill mapping, learning paths, skill gap analysis, career path prediction, mentorship recommendations, and chatbot interactions.
    - Key data:
      - Current skills: {current_skills}
      - AI Skill Analysis: {skill_analysis}
      - Learning Paths: {learning_recommendations}
      - Skill Gap Analysis: {skill_gap_analysis}
      - Career Path Prediction: {career_recommendations}

    Generate:
    - A **personalized career summary** in bullet points.
    - A **breakdown of top skills gained**.
    - Key **areas of improvement**.
    - A **progress evaluation score (1-100%)**.
    """
    response = model.generate_content(prompt)
    return response.text

# Generate AI-powered dashboard insights
if st.button("📊 Generate AI Dashboard"):
    with st.spinner("Generating Dashboard Insights..."):
        insights = generate_dashboard_insights()
        def stream_output():
            for word in insights.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.session_state.user_data["dashboard_insights"] = insights
        st.subheader(f"📌 AI-Generated Career Summary for {user_name}")
        st.write_stream(stream_output())

        # Simulated Data for Charts
        skill_categories = ["Technical Skills", "Soft Skills", "Leadership", "Industry Trends"]
        improvement_levels = [8, 6, 7, 9]  # Example skill improvement ratings

        # Bar Chart for Skill Growth
        st.subheader("📈 Skill Growth Analysis")
        skill_chart = px.bar(
            x=skill_categories, y=improvement_levels,
            labels={"x": "Skill Category", "y": "Improvement Level"},
            color=improvement_levels,
            color_continuous_scale="Blues"
        )
        st.plotly_chart(skill_chart)

        # Pie Chart for Learning Distribution
        st.subheader("📚 Learning Path Distribution")
        learning_sources = ["Online Courses", "Certifications", "Mentorships"]
        learning_percentage = [40, 35, 25]  # Example data

        learning_chart = px.pie(
            names=learning_sources, values=learning_percentage,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(learning_chart)

        # Radar Chart for Skill Evaluation
        st.subheader("🛠️ Skill Competency Evaluation")
        categories = ["Technical", "Soft Skills", "Leadership", "Adaptability", "Innovation"]
        values = [85, 70, 75, 80, 90]  # Example competency scores

        radar_chart = go.Figure(
            data=[go.Scatterpolar(r=values, theta=categories, fill='toself', marker=dict(color="red"))]
        )
        radar_chart.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
        st.plotly_chart(radar_chart)

        # Progress Line Chart
        st.subheader("📈 Career Progression Over Time")
        career_stages = ["Entry Level", "Intermediate", "Senior", "Lead", "Manager"]
        experience_years = [1, 3, 6, 9, 12]  # Example career progression

        career_chart = px.line(
            x=experience_years, y=career_stages, markers=True,
            title="Career Growth Projection",
            labels={"x": "Years of Experience", "y": "Career Stage"},
            line_shape="spline"
        )
        st.plotly_chart(career_chart)

        # Display Chatbot History
        if chatbot_history:
            st.subheader("💬 Chatbot Interaction History")
            for chat in chatbot_history:
                st.write(f"**Q:** {chat['question']}")
                st.write(f"**A:** {chat['response']}")
                st.write("---")

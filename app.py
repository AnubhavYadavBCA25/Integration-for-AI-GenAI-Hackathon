import streamlit as st
import streamlit_lottie as st_lottie
from features.functions import load_lottie_file
from features.auth import authentication

st.set_page_config(page_title="Sankalp.AI",
                   page_icon="🧊",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Initialize session state keys
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

def intro():
    st.header("Sankalp.AI: Empowering Skill Development with AI", divider="rainbow")

    with st.container(border=True):
        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("What is Sankalp.AI?🚀", divider='rainbow')
            st.markdown('''
                            Sankalp.AI is an AI-powered Employee Skill Mapping and Development Platform that helps enterprises:

                            1. Analyze employee skills using Generative AI.
                            2. Identify skill gaps based on real-time data.
                            3. Recommend personalized learning paths for upskilling.
                            4. Enhance workforce productivity through AI-driven insights.
                            5. Prepare for the future of work with AI-powered skill development.
                            6. Connects with multiple data sources to create a unified skill profile.
                            7. AI chatbot to guide users with career advice and job insights. 
                        
                            Sankalp.AI leverages the power of AI to provide a data-driven approach to employee skill development, enabling organizations to build a future-ready workforce.
                            With the help of Gemini Models, Sankalp.AI provides a unique solution to the challenges faced by organizations in identifying and developing employee skills.
            ''')
        
        with right_col:
            robot_ani = load_lottie_file("animations/robot_assist.json")
            st_lottie.st_lottie(robot_ani, loop=True, height=480, width=400)

        
    with st.container(border=True):
        st.subheader("Why Sankalp.AI?🌟", divider='rainbow')

        left_col, right_col = st.columns(2)

        with right_col:
            st.markdown('''
                            Sankalp.AI is a one-stop solution for all your skill development needs. Here's why you should choose Sankalp.AI:
                            1. **AI-Powered Skill Mapping:** Leverage the power of AI to analyze employee skills and identify skill gaps.
                            2. **Personalized Learning Paths:** Get personalized learning paths based on your skill gaps and learning preferences.
                            3. **Real-Time Skill Development:** Stay updated with real-time skill development recommendations.
                            4. **Enhanced Workforce Productivity:** Boost workforce productivity with AI-driven insights.
                            5. **Future-Ready Workforce:** Prepare your workforce for the future of work with AI-powered skill development.
                        
                            Sankalp.AI is designed to help organizations build a future-ready workforce by providing a data-driven approach to employee skill development.
                        ''')
        with left_col:
            why_ani = load_lottie_file("animations/why_sankalp.json")
            st_lottie.st_lottie(why_ani, loop=True, height=450, width=400)

    with st.container(border=True):
        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("Features Offered🔥", divider='rainbow')
            st.markdown('''
                            - 1️⃣ **SkillSync AI** – Automatically maps your skills from resumes, assessments, and performance data.

                            - 2️⃣ **LearnTrack** – Get personalized learning paths with recommended courses, certifications, and resources.

                            - 3️⃣ **GapInsight** – Identify missing skills by comparing your profile with industry benchmarks.

                            - 4️⃣ **PathFinder AI** – Receive tailored career progression insights based on your skills and goals.

                            - 5️⃣ **CareerBot** – AI-powered chatbot to guide you with career advice, skill enhancement, and job trends.

                            - 6️⃣ **VisionBoard** – A dynamic, personalized dashboard with skill analytics and career insights.

                            - 7️⃣ **JobRadar** – Find real-time job opportunities that match your skills and career aspirations.
                        ''')
        
        with right_col:
            feature_ani = load_lottie_file("animations/features.json")
            st_lottie.st_lottie(feature_ani, loop=True, height=500, width=400)
    
    with st.container(border=True):
        left_col, right_col = st.columns(2)

        with right_col:
            st.subheader("📌 How to Use Sankalp.AI", divider='rainbow')
            st.write("""
            To get the best results, follow these steps in order. Sankalp.AI analyzes your skills, recommends learning paths, 
            suggests career opportunities, and helps you find jobs based on your profile.
            """)
            # Step-wise Guide
            steps = [
                ("🔍 **Step 1: Skill Mapping (SkillSync AI)**", 
                "Upload your resume, take a short self-assessment, and provide past performance reviews to map your skills."),
                
                ("📊 **Step 2: Analyze Your Skill Gaps (GapInsight)**", 
                "Compare your current skills with industry benchmarks to identify areas for improvement."),
                
                ("🎯 **Step 3: Get a Personalized Learning Path (LearnTrack)**", 
                "Receive AI-driven recommendations for courses, certifications, and resources to bridge your skill gaps."),
                
                ("🚀 **Step 4: Career Path Recommendation (PathFinder AI)**", 
                "Explore career progression opportunities tailored to your skills and goals."),
                
                ("🤖 **Step 5: Career ChatBot Assistance (CareerBot)**", 
                "Ask career-related queries, get industry insights, and receive AI-powered career guidance."),
                
                ("📈 **Step 6: View Your Dashboard (VisionBoard)**", 
                "Access a personalized dashboard with real-time insights on skills, progress, and career suggestions."),
                
                ("💼 **Step 7: Find Jobs in Real-Time (JobRadar)**", 
                "Discover job opportunities that match your skills and career aspirations.")
            ]

            # Display Steps in an Expandable Format
            for step, description in steps:
                with st.expander(step):
                    st.write(description)
        
        with left_col:
            working_ani = load_lottie_file("animations/working_ani.json")
            st_lottie.st_lottie(working_ani, loop=True, height=650, width=450)

    with st.container(border=True):
        st.subheader("FAQs🤔", divider='rainbow')

        with st.expander("What is Sankalp.AI?"):
            st.write('''
                            Sankalp.AI is an AI-powered Employee Skill Mapping and Development Platform that helps enterprises analyze employee skills, identify skill gaps, recommend personalized learning paths, enhance workforce productivity, and prepare for the future of work with AI-powered skill development.
                        ''')
        
        with st.expander("How does Sankalp.AI work?"):
            st.write('''
                            Sankalp.AI leverages the power of AI to provide a data-driven approach to employee skill development. It uses Generative AI to analyze employee skills, identify skill gaps, recommend personalized learning paths, and provide real-time insights into skill development needs.
                        ''')
        
        with st.expander("Which Technologies are used in Sankalp.AI?"):
            st.write('''
                            Sankalp.AI uses a combination of AI technologies, including Generative AI, Machine Learning, Natural Language Processing (NLP), and Data Analytics, to provide a comprehensive solution for employee skill development.
                        ''')
        
        with st.expander("How my Data is Secured in Sankalp.AI?"):
            st.write('''
                            Sankalp.AI follows industry best practices to ensure the security and privacy of your data. We use encryption, access controls, and other security measures to protect your data from unauthorized access, disclosure, and misuse.
                        ''')
        
        with st.expander("Does Sankalp.AI provide Real-Time Job Opportunities Analysis?"):
            st.write('''
                            Yes, Sankalp.AI offers real-time job opportunities analysis through the JobRadar feature. You can find job opportunities that match your skills and career aspirations, helping you stay updated with the latest job trends and openings.
                        ''')
            
# Initialize session state for authentication
authentication()

if st.session_state["authentication_status"]:
    pg = st.navigation([
        st.Page(title="Home", page=intro, icon="🏠"),
        st.Page(title="Skill Mapping", page="features/1-Skill-Mapping.py", icon="🔍"),
        st.Page(title="Learning Paths", page="features/2-Learning-Path.py", icon="🛤"),
        st.Page(title="Skill Gap Analysis", page="features/3-Real-Time-Skill-Analysis.py", icon="📈"),
        st.Page(title="Career Path Recommendations", page="features/4-Career-Path.py", icon="🚀"),
        st.Page(title="Career ChatBot", page="features/5-Career-ChatBot.py", icon="🤖"),
        st.Page(title="Dashboard", page="features/6-Dashboard.py", icon="📊"),
        st.Page(title="Job Analysis", page="features/7-Job-Analysis.py", icon="🔍"),
    ])
    pg.run()

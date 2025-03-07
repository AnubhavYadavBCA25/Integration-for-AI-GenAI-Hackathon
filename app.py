import streamlit as st
import streamlit_lottie as st_lottie
from features.functions import load_lottie_file

st.set_page_config(page_title="Sankalp.AI",
                   page_icon="🧊",
                   layout="wide")

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
                        
                            Sankalp.AI leverages the power of AI to provide a data-driven approach to employee skill development, enabling organizations to build a future-ready workforce.
                            With the help of Gemini Models, Sankalp.AI provides a unique solution to the challenges faced by organizations in identifying and developing employee skills.
            ''')
        
        with right_col:
            robot_ani = load_lottie_file("animations/robot_assist.json")
            st_lottie.st_lottie(robot_ani, loop=True, height=430, width=400)

        
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
                            1. ✅ "AI-Powered Skill Mapping": Auto-identifies skills from resumes, reviews & learning data.
                            2. ✅ "Personalized Learning Paths:" Recommends courses & mentorship based on skill gaps.
                            3. ✅ "Real-Time Skill Gap Analysis:" Provides insights into current & future skill needs.
                            4. ✅ "Seamless Data Integration:" Connects HR & LMS platforms for a unified employee profile.
                            5. ✅ "Career Path Recommendations:" Suggests growth opportunities based on skills & goals.
                        ''')
        
        with right_col:
            feature_ani = load_lottie_file("animations/features.json")
            st_lottie.st_lottie(feature_ani, loop=True, height=380, width=370)
    
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
        
        with st.expander("How to contact Sankalp.AI for more Information or Query?"):
            st.write('''
                            You can contact Sankalp.AI by submitting a query through the Contact Us form on our website. Our team will get in touch with you to provide more information and address any queries you may have.
                        ''')
            


pg = st.navigation([
    st.Page(title="Home", page=intro, icon="🏠"),
    st.Page(title="Skill Mapping", page="features/1-Skill-Mapping.py", icon="🔍"),
])
pg.run()

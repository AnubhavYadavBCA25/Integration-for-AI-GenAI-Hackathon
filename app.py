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


pg = st.navigation([
    st.Page(title="Home", page=intro, icon="🏠"),
    st.Page(title="About Us", page="features/1-Feature.py", icon="🤝"),
])
pg.run()

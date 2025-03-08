import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import Hasher, LoginError
import streamlit_authenticator as stauth

# Load config file (Stores user credentials)
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Ensure config structure
if config is None:
    config = {}
if 'credentials' not in config:
    config['credentials'] = {}
if 'usernames' not in config['credentials']:
    config['credentials']['usernames'] = {}

# Initialize session state for authentication
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

# Function to show the login form
def show_login_form():
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    try:
        authenticator.login()
    except LoginError as e:
        st.error(e)

    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', "sidebar")
        st.sidebar.write(f'Welcome **{st.session_state["name"]}** 👋')

        # Extract user data
        username = st.session_state["username"]
        user_data = config['credentials']['usernames'].get(username, {})
        st.session_state["user_data"] = user_data

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    # Register Button (If not logged in)
    if st.session_state["authentication_status"] is None or st.session_state["authentication_status"] is False:
        st.write("---")
        if st.button("Register"):
            st.session_state['register'] = True  # Switch to register form

# Function to show the registration form
def show_register_form():
    with st.container():
        st.write("## Register")
        st.divider()

        # New User Inputs
        new_username = st.text_input("Enter Username")
        new_name = st.text_input("Enter Your Full Name")
        new_password = st.text_input("Enter Password", type="password")
        new_email = st.text_input("Enter Your Email")
        new_job_role = st.selectbox("Job Role", ["Data Analyst", "Software Engineer", "HR Manager", "Sales Executive"])
        new_skills = st.text_area("Enter Your Skills (comma-separated)")
        new_experience = st.number_input("Years of Experience", min_value=0, max_value=40, step=1)

        if st.button("Submit Registration"):
            if new_username and new_password and new_email:
                # Hash the new password
                hasher = Hasher()
                hashed_password = hasher.hash(new_password)

                if 'credentials' not in config:
                    config['credentials'] = {}
                if 'usernames' not in config['credentials']:
                    config['credentials']['usernames'] = {}

                # Store user data
                config['credentials']['usernames'][new_username] = {
                    'name': new_name,
                    'password': hashed_password,
                    'email': new_email,
                    'job_role': new_job_role,
                    'skills': new_skills,
                    'experience': new_experience
                }

                # Save updated credentials to `config.yaml`
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file)

                st.success("User registered successfully! You can now log in.")

    if st.button("Back to Login"):
        st.session_state['register'] = False  # Return to login page

# Main function to handle authentication
def authentication():
    if st.session_state['register']:
        show_register_form()
    else:
        show_login_form()

# Function to get logged-in user details
def get_user_details():
    return st.session_state.get("user_data", {})
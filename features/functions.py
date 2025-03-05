import json
import streamlit_lottie as st_lottie

# Function for lottie file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)
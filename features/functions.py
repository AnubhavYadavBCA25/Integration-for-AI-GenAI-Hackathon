import json
import time
import os
from dotenv import load_dotenv
import streamlit as st
import streamlit_lottie as st_lottie
import google.generativeai as genai

# Function for lottie file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

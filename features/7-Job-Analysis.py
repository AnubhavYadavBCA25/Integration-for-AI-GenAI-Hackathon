# Real time job analysis and search
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import plotly.express as px
import pandas as pd

# Load environment variables
load_dotenv()

JSEARCH_API_KEY = st.secrets["JSEARCH_API_KEY"]
# JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY")

st.header("🔎 AI-Powered Job Search Dashboard", divider='rainbow')

# User Inputs
job_query = st.text_input("Enter Job Title (e.g., Data Scientist)", "Software Engineer")
location = st.text_input("Enter Location (or type 'Remote')", "Remote")

# Function to fetch job listings
def search_jobs(job_title, location):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": f"{job_title} in {location}", "page": "1"}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

# Search Button
if st.button("🔍 Search Jobs"):
    with st.spinner("Searching for job listings..."):
        job_results = search_jobs(job_query, location)

        if job_results and "data" in job_results:
            jobs = job_results["data"]

            # Collect data for visualization
            job_titles = [job["job_title"] for job in jobs]
            companies = [job["employer_name"] for job in jobs]
            locations = [job["job_city"] if job["job_city"] else "Remote" for job in jobs]

            # Convert to DataFrame for visualization
            job_data = pd.DataFrame({"Job Title": job_titles, "Company": companies, "Location": locations})

            # Display Job Listings
            st.subheader("💼 Job Listings")
            for job in jobs[:10]:  # Show top 10 jobs
                st.write(f"🔹 **{job['job_title']}** at **{job['employer_name']}**")
                st.write(f"📍 Location: {job['job_city'] if job['job_city'] else 'Remote'}, {job['job_country']}")
                st.write(f"🔗 [Apply Now]({job['job_apply_link']})")
                st.markdown("---")

            # Interactive Graphs
            st.subheader("📊 Job Market Insights")

            # Bar Chart: Top Hiring Companies
            company_chart = px.bar(
                job_data["Company"].value_counts().reset_index(),
                x="Company", y="count",
                title="Top Hiring Companies",
                labels={"Company": "Company Name", "count": "Number of Jobs"},
                color="count",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(company_chart)

            # Pie Chart: Job Distribution by Location
            location_chart = px.pie(
                job_data, names="Location",
                title="Job Distribution by Location",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(location_chart)

        else:
            st.write("⚠️ No job listings found. Try again later.")

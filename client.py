import streamlit as st
import time
import schedule

st.title("Job Notification Preferences")

job_type = st.text_input("Enter the type of job you're looking for:", "Software Engineer")
num_jobs = st.slider("How many jobs would you like to receive?", 1, 50, 5)
frequency = st.selectbox(
    "How often do you want to receive job notifications?",
    ["Every minute", "Every hour", "Once a day"]
)

frequency_map = {
    "Every minute": 1,
    "Every hour": 60,
    "Once a day": 1440
}

frequency_in_minutes = frequency_map[frequency]

st.write(f"You'll receive {num_jobs} {job_type} jobs {frequency.lower()}.")

def fetch_jobs(job_type, num_jobs):
    st.write(f"Fetching {num_jobs} jobs for '{job_type}'...")
    time.sleep(2)  
    st.write(f"{num_jobs} new {job_type} jobs received!")

if st.button("Start Job Notifications"):
    st.write("Job notifications started!")
    
    def scheduled_job():
        fetch_jobs(job_type, num_jobs)
    
    schedule.every(frequency_in_minutes).minutes.do(scheduled_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

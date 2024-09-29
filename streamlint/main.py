import streamlit as st
import schedule
import time
from auth import login, signup 

def job_preferences():
    st.title(f"Job Notification Preferences (Logged in as {st.session_state['username']})")

    website = st.selectbox(
        "Select the website to fetch jobs from:",
        ["jobs.ge", "hr.ge"]
    )

    notification_type = st.selectbox(
        "Select how you want to receive job notifications:",
        ["Gmail", "Message"]
    )

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

    st.write(f"You'll receive {num_jobs} {job_type} jobs from {website} via {notification_type}, {frequency.lower()}.")

    def fetch_jobs(job_type, num_jobs, website, notification_type):
        st.write(f"Fetching {num_jobs} jobs for '{job_type}' from {website}...")
        time.sleep(2)
        st.write(f"{num_jobs} new {job_type} jobs from {website} received!")

    if st.button("Start Job Notifications"):
        st.write("Job notifications started!")

        def scheduled_job():
            fetch_jobs(job_type, num_jobs, website, notification_type)

        schedule.every(frequency_in_minutes).minutes.do(scheduled_job)

        while True:
            schedule.run_pending()
            time.sleep(1)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ''

if not st.session_state['logged_in']:
    option = st.selectbox("Login or Signup", ["Login", "Signup"], key="auth_selectbox")
    
    if option == "Login":
        login()  
    elif option == "Signup":
        signup()  
else:
    job_preferences()

    if st.button("Logout", key="logout_button"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.experimental_rerun()

import streamlit as st
import schedule
import time
from auth import login, signup
from sms_sender import send_sms 

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

    if notification_type == "Gmail":
        contact_info = st.text_input("Enter your Gmail address", "")
    else:
        contact_info = st.text_input("Enter your phone number", "")

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

    st.write(f"You'll receive {num_jobs} {job_type} jobs from {website} via {notification_type} to {contact_info}.")

    def fetch_jobs(job_type, num_jobs, website, notification_type, contact_info):
        st.write(f"Fetching {num_jobs} jobs for '{job_type}' from {website}...")
        time.sleep(2)
        st.write(f"{num_jobs} new {job_type} jobs from {website} received!")

        if notification_type == "Message":
            try:
                message_body = f"{num_jobs} new {job_type} jobs from {website}"
                sms_sid = send_sms(contact_info, message_body)
                st.success(f"SMS sent successfully! (SID: {sms_sid})")
            except Exception as e:
                st.error(f"Failed to send SMS: {e}")
        else:
            st.write(f"Sending job notifications to {contact_info} via Gmail...")

    if st.button("Start Job Notifications"):
        st.write("Job notifications started!")

        def scheduled_job():
            fetch_jobs(job_type, num_jobs, website, notification_type, contact_info)

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

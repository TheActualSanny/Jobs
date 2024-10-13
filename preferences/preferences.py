import streamlit as st
import schedule
import time
from services.sms_sender import send_sms  
from services.mail_sender import send_email_notification
from auth.auth import login, signup
from dataclasses import dataclass, field
from .enums import NotificationType, Website, Frequency  



@dataclass
class JobPreferences:
    website: Website = None
    notification_type: NotificationType = None
    contact_info: str = None
    job_type: str = "Software Engineer"
    num_jobs: int = 5
    frequency: Frequency = None
    frequency_in_minutes: int = None

    def display_title(self):
        st.title("Job Notification Preferences")

    def select_website(self):
        self.website = st.selectbox(
            "Select the website to fetch jobs from:",
            [Website.JOBS_GE.value, Website.HR_GE.value, Website.QUANTORI.value]
        )

    def select_notification_type(self):
        self.notification_type = st.selectbox(
            "Select how you want to receive job notifications:",
            [NotificationType.GMAIL.value, NotificationType.MESSAGE.value]
        )
        self.contact_info = st.text_input(
            f"Enter your {('Gmail address' if self.notification_type == NotificationType.GMAIL.value else 'phone number')}", ""
        )

    def select_job_details(self):
        self.job_type = st.text_input("Enter the type of job you're looking for:", self.job_type)
        self.num_jobs = st.slider("How many jobs would you like to receive?", 1, 50, self.num_jobs)

    def select_frequency(self):
        frequency_choice = st.selectbox(
            "How often do you want to receive job notifications?",
            [Frequency.DAILY.value, Frequency.WEEKLY.value, Frequency.MONTHLY.value]
        )
        self.frequency = Frequency(frequency_choice)
        self.frequency_in_minutes = Frequency.to_minutes(self.frequency)

    def display_summary(self):
        st.write(f"You'll receive {self.num_jobs} {self.job_type} jobs from {self.website} via {self.notification_type} to {self.contact_info}.")

    def fetch_jobs(self):
        st.write(f"Fetching {self.num_jobs} jobs for '{self.job_type}' from {self.website}...")
        time.sleep(2)
        st.write(f"{self.num_jobs} new {self.job_type} jobs from {self.website} received!")
        
        if self.notification_type == NotificationType.MESSAGE.value:
            self.send_sms_notification()
        else:
            st.write(f"Sending job notifications to {self.contact_info} via Gmail...")

    def send_sms_notification(self):
        try:
            message_body = f"{self.num_jobs} new {self.job_type} jobs from {self.website}"
            sms_sid = send_sms(self.contact_info, message_body)
            st.success(f"SMS sent successfully! (SID: {sms_sid})")
        except Exception as e:
            st.error(f"Failed to send SMS: {e}")

    def start_notifications(self):
        if st.button("Start Job Notifications"):
            st.write("Job notifications started!")
            def scheduled_job():
                self.fetch_jobs()
            schedule.every(self.frequency_in_minutes).minutes.do(scheduled_job)
            while True:
                schedule.run_pending()
                time.sleep(1)
                
    
def handle_auth():
    option = st.selectbox("Login or Signup", ["Login", "Signup"], key="auth_selectbox")
    if option == "Login":
        login()  
    elif option == "Signup":
        signup()


def handle_job_preferences():
    job_pref = JobPreferences()
    job_pref.display_title()
    job_pref.select_website()
    job_pref.select_notification_type()
    job_pref.select_job_details()
    job_pref.select_frequency()
    job_pref.display_summary()
    job_pref.start_notifications()
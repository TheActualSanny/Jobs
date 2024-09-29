Jobs Alert
Jobs Alert is a web-based application that allows users to receive job notifications based on their preferences. Users can sign up, log in, and configure job notifications to be delivered via Gmail or SMS (powered by Twilio). The app fetches job listings from sites like jobs.ge and hr.ge, and allows users to set preferences for job type, frequency, and the number of jobs they want to receive.

Features
User Authentication: Sign up and log in functionality to personalize job alerts.
Job Notification Preferences: Users can choose job websites (jobs.ge, hr.ge), job type, and frequency of job alerts.
Notification Methods: Users can receive notifications via Gmail or SMS.
Scheduler: A scheduler sends job notifications at intervals defined by the user (e.g., every minute, every hour, or once a day).
Twilio Integration: SMS notifications are sent using the Twilio API.
Table of Contents
Installation
Environment Variables
Twilio Integration
Running the Project
Running Tests
Project Structure
Installation
Prerequisites
Ensure you have the following installed:

Python 3.8+
PostgreSQL for storing user data
Twilio Account (for sending SMS notifications) 
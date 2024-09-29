import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(job_type, num_jobs, website, recipient_email):
    sender_email = "your-email@gmail.com"

    subject = f"New {job_type} Jobs Notification"
    body = f"Here are {num_jobs} new {job_type} jobs from {website}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

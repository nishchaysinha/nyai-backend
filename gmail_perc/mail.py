import smtplib
from email.mime.text import MIMEText
import os

def send_email(recipient, case_id):
    msg = MIMEText("Checkout the complaint and respond at: "+case_id)
    msg['Subject'] = "Alert! you have a complaint on Ny.ai"
    msg['From'] = os.getenv("EMAIL_USERNAME")
    msg['To'] = ', '.join(recipient)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
        smtp_server.sendmail(os.getenv("EMAIL_USERNAME"), recipient, msg.as_string())
    print("Message sent!")

# Path: gmail_perc/mail.py

send_email("gauravhegde03@gmail.com", "4356789")
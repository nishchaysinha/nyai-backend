import smtplib
from email.mime.text import MIMEText


EMAIL_USERNAME = "nyaaa.ai.deployment@gmail.com" #for some weird reason env not working here
EMAIL_PASSWORD = "ocst elrz yvma sjkd"


def send_email(recipient, case_id):
    subject = "Alert! you have a complaint on Ny.ai"
    body = "Checkout the complaint and respond at: " + "https://nyai-app.vercel.app/cases/" + case_id
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USERNAME
    msg['To'] = recipient
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
       smtp_server.sendmail(EMAIL_USERNAME, recipient, msg.as_string())
    print("Message sent!")

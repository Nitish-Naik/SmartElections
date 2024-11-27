import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_password'

def send_email(subject, body, to_emails, attachment_path=None):
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    
    msg.attach(MIMEText(body, 'plain'))

    
    if attachment_path:
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, to_emails, text)

    
    server.quit()

def generate_daily_report():
    
    subject = "Daily Report"
    body = "Please find the daily report attached."
    to_emails = ["recipient1@example.com", "recipient2@example.com"]
    
    
    attachment_path = create_report()  
    
    send_email(subject, body, to_emails, attachment_path)

def create_report():
    
    report_path = "daily_report.txt"
    with open(report_path, "w") as file:
        file.write("This is your daily report.\n")
        file.write("Data: ...\n")
    return report_path


schedule.every().day.at("08:00").do(generate_daily_report)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

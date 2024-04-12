import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email, venue, date, time,flag):      
    # Email configuration
    sender_email = "rppoop@outlook.com"
    sender_password = "Aaditya@Anish#Bhargav"
    receiver_email = email
    smtp_server = "smtp.office365.com"
    smtp_port = 587  # Outlook.com SMTP port

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "BOOKING STATUS"

    # Email body
    if flag=="student":
        body = f"Your booking in {venue} on {date} at {time} has been confirmed.\n"
    else:
        body = f"A request has been made for {venue} on {date} at {time}.\n" 
    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("Email sent successfully!")

send_email("bhosalepp22.comp@coeptech.ac.in", "Main Audi", "2024-04-24", "12:00","student")
send_email("kharatka22.comp@coeptech.ac.in", "Main Audi", "2024-04-24", "12:00","admin")

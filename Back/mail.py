import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp(length=6):
    digits = "0123456789"
    otp = "".join(random.choice(digits) for _ in range(length))
    return otp


def send_verification_email(sender_email, otp, receiver_email):
    smtp_server = "smtp.office365.com"
    port = 587
    sender_email = "sanjaiscm@outlook.com"
    password = "Sanjai_scm"
    receiver_email="sanjai88scm@outlook.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Hi there"
    body = f"This message is sent from Python. Your OTP is: {otp}"
    message.attach(MIMEText(body, "plain"))

    try:
        # Establish a connection to the SMTP server
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Upgrade the connection to use TLS
            server.login(sender_email, password)

            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")
    except smtplib.SMTPException as smtp_error:
        print(f"SMTP Error: {smtp_error}")
    except Exception as e:
        print(f"Error sending email: {e}")






# import smtplib
# import socket
# import random

# def send_verification_email(otp, receiver_email):
#     try:
#         server = smtplib.SMTP('smtp.gmail.com')
#         server.starttls()
#         email = "sanjaisanjai9944@gmail.com"
#         password = "cdgviafrzfgupsja"
#         server.login(email, password)
#         msg = 'Hello, Your OTP is ' + str(otp)
#         receiver = receiver_email
#         server.sendmail(email, receiver, msg)
#         server.quit()
#         print("Email sent successfully!")
#     except socket.gaierror as e:
#         print(f"Socket Error: {e}")
#     except smtplib.SMTPException as e:
#         print(f"SMTP Error: {e}")



# # Example usage:
# otp_value = generate_otp()
# receiver_email_address = "rsanjai@exafluence.com" 
# send_verification_email(otp_value, receiver_email_address)

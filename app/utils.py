import smtplib
from email.mime.text import MIMEText

# Define the subject and body of the email.
subject = "Donacion Ohana!"
body = "Gracias por donar idolo!"
# Define the sender's email address.
sender = "ohana.notifications.utn@gmail.com"
# Password for the sender's email account.
password = ""


def send_email(recipient, subject=subject, body=body, sender=sender, password=password):
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(sender, password)

    # Test send mail
    sent_from = sender
    sent_to = recipient
    email_text = body
    smtpserver.sendmail(sent_from, sent_to, email_text)

    # Close the connection
    smtpserver.close()

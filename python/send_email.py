import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


def send_email(name, surname, arrival, departure, email):
    load_dotenv()

    mail_content = f"Good morning {name} {surname}, \n \n" \
                   f"We confirm your reservation at the hotel from {arrival} to {departure}. \n" \
                   f"Thank you for choosing our hotel. If you have any questions, please do not hesitate to contact us.\n \n" \
                   f"Best Regards, \nHotel Mare"

    sender_address = os.getenv('EMAIL_ADDRESS')
    sender_pass = os.getenv('EMAIL_PASSWORD')
    receiver_address = email

    print(sender_address)
    print(sender_pass)

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Reservation conformation'
    message.attach(MIMEText(mail_content, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()

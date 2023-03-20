from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
import ssl

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])

            #remove after testing
        email.send()

#        context = ssl.create_default_context()
#        with smtplib.SMTP_SSL(data[settings.SMTP_HOST], data[settings.SMTP_PORT], context=context) as server:
#            server.login(data[settings.SMTP_USERNAME], data[settings.SMTP_USERNAME])
#            server.send_message(email)

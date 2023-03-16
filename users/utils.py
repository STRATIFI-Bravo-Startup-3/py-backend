from django.core.mail import EmailMessage
import smtplib
import ssl

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(data['smtp_server'], data['smtp_port'], context=context) as server:
            server.login(data['smtp_username'], data['smtp_password'])
            server.send_message(email)

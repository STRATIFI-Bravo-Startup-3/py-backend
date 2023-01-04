from django.core.mail import EmailMessage
import ssl

class Util:
    @staticmethod
    def send_email(data):
        
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        
        email.send()
        context=ssl.creat_default_context()

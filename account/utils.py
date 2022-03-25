from django.core.mail import EmailMessage

class Mailer:
    @staticmethod
    def send_email(data):
        email=EmailMessage(subject=data['subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
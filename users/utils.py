from django.core.mail import EmailMessage
from users.models import User
from checkout.models import Transaction
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
import threading

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

class Util:

    @staticmethod
    def prepare_verify_email(user_data, request):
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_url = reverse('email-verify')
        absolute_url = f"http://{current_site}{relative_url}?token={str(token)}"

        email_body = f"Hi {user.username} use this link to verify your email\nLink: {absolute_url}"

        email_data = {
            'email_subject': "Verification email",
            'email_body': email_body,
            'to_email': user.email
        }

        return email_data

    @staticmethod
    def prepare_payment_verify_email(user_data, request):
        user = User.objects.get(email=user_data['email'])
        # t = Transaction.objects.get(cardId=user_data['cardId']).last()
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_url = reverse('verify-payment')
        absolute_url = f"http://{current_site}{relative_url}?token={str(token)}"

        email_body = f"Hi {user.username} use this link to verify your Payment\nLink: {absolute_url}"

        email_data = {
            'email_subject': "Verification email",
            'email_body': email_body,
            'to_email': user.email
        }

        return email_data    

    @staticmethod
    def send_email(email_data):
        email = EmailMessage(
            subject=email_data['email_subject'],
            body=email_data['email_body'],
            to=[email_data['to_email']]
        )

        try:
            print("Sending email")
            EmailThread(email).start()
        except Exception as e:
            print(e)
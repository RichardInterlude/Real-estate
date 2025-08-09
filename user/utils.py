from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from . models import Profile

def sendMail(subject,message):
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [User.email],
        fail_silently=True)
    


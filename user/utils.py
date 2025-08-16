from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.models import User

def sendMail(subject,message,email):
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False)
    


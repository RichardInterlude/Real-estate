from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICE = (
    ('M','Male'),
    ('F','Female'),
)

ROLE = (
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
    ('both','Buyer & Seller'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, choices = GENDER_CHOICE)
    profile_pix = models.ImageField(upload_to='user_pix', default='https://thumbs.dreamstime.com/b/user-profile-icon-vector-avatar-person-picture-portrait-symbol-neutral-gender-silhouette-circle-button-photo-blank-272664038.jpg')
    role = models.CharField(max_length=255,choices=ROLE,default='buyer')

    def __str__(self):
        if self.role == 'buyer':
            return f'{self.full_name} (Buyer)'
        elif self.role == 'seller':
            return f'{self.full_name} (Seller)'
        elif self.role == 'both':
            return f'{self.full_name} (Buyer & Seller)'
        else:
            return self.full_name
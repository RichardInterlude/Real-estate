from django.db import models
from user.models import Profile
from django.contrib.auth.models import User


CATEGORY = (
    ('sale','Sale'),
    ('rent','Rent'),
    ('apartment','Apartment'),
)
    
class Listing(models.Model):
    title = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=255)
    price = models.BigIntegerField(null=True)
    discount_price = models.BigIntegerField(null=True)
    category = models.CharField(max_length=255,choices=CATEGORY)
    image = models.ImageField(upload_to='listing',null=True)
    photo1 = models.ImageField(upload_to='listing/photo1',null=True,blank=True)
    photo2 = models.ImageField(upload_to='listing/photo1',null=True,blank=True)
    photo3 = models.ImageField(upload_to='listing/photo1',null=True,blank=True)
    review  = models.TextField( null=True)
    rating = models.BigIntegerField(default=0)
    is_available  = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
       return self.title

class Inquiry(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,null=True,blank=True)
    sender = models.ForeignKey(Profile, related_name="sent_inquiries", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, related_name="received_inquiries", on_delete=models.CASCADE,default=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f'Message was sent by {self.sender} about {self.listing} by {self.timestamp}'

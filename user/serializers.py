from rest_framework import serializers

from . models import Profile
from django.contrib.auth.models import User
from . utils import sendMail

from typing import Dict, Any


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['username','email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer()
        field = ['full_name','phone','gender','profile_pix']


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    password1 = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)

    class Meta:
        model = Profile
        fields = ['full_name','phone','gender','profile_pix','email','username','password','password1']
    def validate(self,data):
        if data['password'] != data['password1']:
            raise serializers.ValidationError('password does not match')
        return data
    
    def create(self, validated_data: Dict[str, Any]):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username,email=email,password=password)

        profile = Profile.objects.create(
            user = user,
            full_name = validated_data['full_name'],
            phone = validated_data['phone'],
            gender= validated_data['gender'],
            profile_pix = validated_data.get('profile_pix'),
        )
        if profile.role == 'buyer':
            sendMail(subject="Welcome to the top Real estate app",
                      message= f"""
                        Hi {Profile.full_name}, i welcome you to the Richard Real estate app. 
                        we are focused on getting you your dream home, with at little stress as possible
                        i hope you can be able to share this feeling with us. 
                """ )
        elif profile.role == 'seller':
            sendMail(subject="Welcome to the top Real estate app",
                     message=f"""
                         Hi {Profile.full_name}, i welcome you to the Richard Real estate app. 
                        we are focused on connecting you to your potential buyers, with as little stress as possible.
                     """)
        elif profile.role == 'both':
            sendMail(subject=f"{Profile.full_name}  i welcome you to the Richard Real estate app",message="Welcome Buyer & Seller!You have full access to buy and sell.")
        return profile






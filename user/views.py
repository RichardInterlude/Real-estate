from rest_framework import status,serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from . models import Profile
from . serializers import *
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import get_object_or_404

class RegistrationView(APIView):
    def post(self,request):
        try:
            serializers = RegistrationSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)})


class LoginView(APIView):
    def post(self,request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request,user)
                return Response({'message':'user logged in successfully'}, status=status.HTTP_200_OK)
            return Response({'message':'username/password seems to be incorrect'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)})     
        

class LogoutView(APIView):
    def post(self,request):
        try:
            logout(request)
            return Response({'message':"Logout was successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)})    

class UserDashboardView(APIView):
    def get(self,request):
        try:
            user = request.user
            profile = get_object_or_404(Profile,user=user)
            role = profile.role

            if role == "buyer":
                data = {"email":user.email,
                        "full_name":profile.full_name,
                        "profile_pix":profile.profile_pix.url,
                        "role":profile.role
                        }
            elif role == "seller":
                data = {"email":user.email,
                        "full_name":profile.full_name,
                        "profile_pix":profile.profile_pix.url,
                        "role":profile.role
                        }
            else :
                data = {"email":user.email,
                        "full_name":profile.full_name,
                        "profile_pix":profile.profile_pix.url,
                        "role":profile.role}
            return Response(data)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




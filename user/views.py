from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . models import *
from stores.models import *
from . serializers import *
from stores.serializers import InquirySerializers
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
    def put(self,request,id):
        try:
            profile = get_object_or_404(Profile, id=id)
            serializers = RegistrationSerializer(profile,data=request.data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.dat,status=status.HTTP_202_ACCEPTED)
            return Response(serializers.error,status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        
class LogoutView(APIView):
    def post(self,request):
        try:
            logout(request)
            return Response({'message':"Logout was successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

class UserDashboardView(APIView):
    def get(self,request,id):
        try:
            # verify if the user is authenticated
            user = request.user
            if not user.is_authenticated:
                return Response(
                    {"error": "Authentication required"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            """if not user.login:
                return Response(
                    {"error":"User has to be logged in"},
                    status=status.HTTP_401_UNAUTHORIZED
                )"""
            
            # Get the profile and listing based on id
            profile = get_object_or_404(Profile,user=user)
            listing = get_object_or_404(Listing,id=id)

            # This is the common field between buyer, seller and user
            data = {"email":user.email,
                        "full_name":profile.full_name,
                        "profile_pix":profile.profile_pix.url,
                        "role":profile.role,
                        }
            # this is to get the messages of the buyer or the seller
            buyer_inquiry = Inquiry.objects.filter(
                    listing_seller=request.user,
                    listing=listing
                )
            seller_inquiry = Inquiry.objects.filter(
                    sender=listing.seller,
                     listing=listing
            )

            # this is to assign what message to another
            if buyer_inquiry.exists():
                data['buyer_inquiry'] = InquirySerializers(buyer_inquiry,many=True).data

            if seller_inquiry.exists():
                data['seller_inquiry'] = InquirySerializers(seller_inquiry,many=True).data

            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User
from . models import *
from . serializers import *
from django.shortcuts import get_object_or_404


#  :::: CREATE PRODUCT VIEW ::::: 
class ListingsView(APIView):
    # create and get Products
    def post(self,request):
        try:
             # Authentication check
            if not request.user.is_authenticated:
                return Response(
                    {"error": "Authentication required"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Role check (only sellers or both can create listings)
            profile = get_object_or_404(Profile, user=request.user)
            if profile.role not in ["seller", "both"]:
                return Response(
                    {"error": "Only sellers can create listings"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            serializers = ListingSerializers(data=request.data)
            if serializers.is_valid():
               serializers.save(seller=request.user.profile)
               return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request):
        try:
            listings = Listing.objects.all()
            serializers = ListingSerializers(listings,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
class ListingView(APIView):
    def get(self,request,id):
        try:
            listing = get_object_or_404(Listing,id=id)
            serializers = ListingSerializers(listing)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request,id):
        try:
            listing = get_object_or_404(Listing,id=id)
            serializers = ListingSerializers(listing,data=request.data,partial= True) 
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id):
        try:
            listing = get_object_or_404(Listing,id=id)
            listing.delete()
            return Response({"Message":f"{listing.title} deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# :::: MESSAGE VIEW ::::
class InquiryView(APIView):
    def post(self,request,id):
        try:
            listing = get_object_or_404(Listing,id=id)

            # Check authentication early
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required"},status=status.HTTP_401_UNAUTHORIZED)

            # Get the user's profile and role and allowing a 2 way communication
            profile = get_object_or_404(Profile, user=request.user)
            if request.user not in [listing.seller,request.user]:
                return Response({'Message':'User is not allowed into this conversation'},status=status.HTTP_403_FORBIDDEN)

            # Create the inquiry (not fetching existing ones)
            serializer = InquirySerializers(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=request.user,listing=listing,receiver=listing.seller)  # assuming Inquiry has sender FK to User
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request):
        try:
            if not request.user.is_authenticated():
                return Response({'Message':"User has to Register"},status=status.HTTP_401_UNAUTHORIZED)
            
            profile = get_object_or_404(Profile,user=request.user)
            if profile.role == 'seller':
                inquires = Inquiry.objects.filter(listing_seller=request.user)
            elif profile.role == 'buyer':
                inquires = Inquiry.objects.filter(sender=request.user)
            else:
                return Response({"Error":"Unauthorized role"},status=status.HTTP_403_FORBIDDEN)
            
            serializers = InquirySerializers(inquires,many=True)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


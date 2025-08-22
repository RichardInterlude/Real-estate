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
    def post(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        listing = get_object_or_404(Listing, id=id)
        profile = get_object_or_404(Profile, user=user)

        # Determine recipient based on role
        if profile.role == "buyer":
            # Buyer sends inquiry to the seller of this listing
            recipient_profile = listing.seller

        elif profile.role == "seller":
            # Seller must specify which buyer they are replying to
            buyer_id = request.data.get("buyer_id")
            if not buyer_id:
                return Response(
                    {"error": "buyer_id required when seller replies"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipient_profile = get_object_or_404(Profile, id=buyer_id)


        else:
            return Response(
                {"error": "Invalid role"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save inquiry
        serializer = InquirySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(
                sender=profile,
                recipient=recipient_profile,
                listing=listing
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

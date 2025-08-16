from rest_framework import serializers
from . models import *


class ListingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['seller']

    def create(self, validated_data):
        return Listing.objects.create(**validated_data)


class InquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['sender']

    def create(self, validated_data):
        return Inquiry.objects.create(**validated_data)



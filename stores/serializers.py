from rest_framework import serializers
from . models import *



class CategorySerializers(serializers.Serializer):
    class Meta:
        model = Category
        fields = '__all__'


class ListingSerializers(serializers.Serializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['seller']


class InquirySerializers(serializers.Serializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['sender']



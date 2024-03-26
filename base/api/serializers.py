from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import *

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

    
class HotelDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelDescription
        fields = ("description",)

class HotelSerializer(serializers.ModelSerializer):
    hotel_images = ImageSerializer(many=True, read_only=True)
    hotel_description = HotelDescriptionSerializer(read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Hotel
        fields = ('id', "city_name", 'name', 'star_rating', 'service', 'review_count', 'review_rating', 'hotel_description', "hotel_images")



def create_serializer(model_class):
    class Serializer(ModelSerializer):
        class Meta:
            model = model_class
            fields = "__all__"
            depth = 1
    return Serializer



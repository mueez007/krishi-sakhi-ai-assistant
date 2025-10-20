from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FarmerProfile, Farm, CropCycle

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = FarmerProfile
        fields = ['id', 'user', 'phone_number']

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'owner', 'name', 'latitude', 'longitude', 'land_area']

class CropCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropCycle
        fields = ['id', 'farm', 'crop_name', 'sowing_date', 'harvest_date']

class LocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


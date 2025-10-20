from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    FarmSerializer, CropCycleSerializer, FarmerProfileSerializer, 
    LocationSerializer, ImageUploadSerializer
)
from .models import Farm, CropCycle, FarmerProfile
import random
import numpy as np
from PIL import Image
from .apps import ApiConfig

# --- Authentication ---
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': { 'id': user.id, 'username': user.username }
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# --- Registration ---
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id, 
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error creating user: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# --- Farm Views ---
class FarmListCreateView(generics.ListCreateAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

class FarmDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

# --- Crop Cycle Views ---
class CropCycleListCreateView(generics.ListCreateAPIView):
    queryset = CropCycle.objects.all()
    serializer_class = CropCycleSerializer

class CropCycleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CropCycle.objects.all()
    serializer_class = CropCycleSerializer

# --- Farmer Profile Views ---
class FarmerProfileListCreateView(generics.ListCreateAPIView):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer

class FarmerProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer

# --- AI Endpoints ---
class CropRecommendView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            simulated_data = {
                'N': random.randint(50, 120), 
                'P': random.randint(30, 80), 
                'K': random.randint(20, 60),
                'temperature': round(random.uniform(18.0, 35.0), 2),
                'humidity': round(random.uniform(60.0, 90.0), 2),
                'ph': round(random.uniform(5.5, 7.5), 2),
                'rainfall': round(random.uniform(80.0, 250.0), 2),
            }
            features = list(simulated_data.values())
            prediction = ApiConfig.recommender_model.predict(np.array(features).reshape(1, -1))
            return Response({
                'recommended_crop': prediction[0], 
                'conditions': simulated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DiseaseDetectionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = serializer.validated_data['image']
        
        try:
            img = Image.open(image_file).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
        except Exception as e:
            return Response({'error': f'Error processing image: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        prediction = ApiConfig.multicrop_model.predict(img_array)
        class_index = np.argmax(prediction[0])
        class_name = ApiConfig.multicrop_class_names[class_index]
        confidence = np.max(prediction[0]) * 100
        
        return Response({
            'predicted_class': class_name.replace('___', ' | ').replace('_', ' '),
            'confidence_score': f'{confidence:.2f}%',
        })

    def get(self, request, *args, **kwargs):
        return Response({'note': 'Use POST with multipart/form-data to submit an image for disease detection.'})

# --- Location Based Recommendation ---
class RecommendFromLocationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            simulated_data = {
                'N': random.randint(50, 120), 
                'P': random.randint(30, 80), 
                'K': random.randint(20, 60),
                'temperature': round(random.uniform(18.0, 35.0), 2),
                'humidity': round(random.uniform(60.0, 90.0), 2),
                'ph': round(random.uniform(5.5, 7.5), 2),
                'rainfall': round(random.uniform(80.0, 250.0), 2),
            }
            features = list(simulated_data.values())
            prediction = ApiConfig.recommender_model.predict(np.array(features).reshape(1, -1))
            return Response({
                'recommended_crop': prediction[0], 
                'conditions': simulated_data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Multi Crop Disease Prediction ---
class MultiCropDiseasePredictionView(APIView):
    # Keep serializer_class for DRF interface to show file upload field
    serializer_class = ImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer(self, *args, **kwargs):
        # Manually define get_serializer method for APIView
        return ImageUploadSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image_file = serializer.validated_data['image']
        
        try:
            img = Image.open(image_file).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
        except Exception as e:
            return Response({'error': f'Error processing image: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        prediction = ApiConfig.multicrop_model.predict(img_array)
        class_index = np.argmax(prediction[0])
        class_name = ApiConfig.multicrop_class_names[class_index]
        confidence = np.max(prediction[0]) * 100
        
        return Response({
            'predicted_class': class_name.replace('___', ' | ').replace('_', ' '),
            'confidence_score': f'{confidence:.2f}%',
        })

    def get(self, request, *args, **kwargs):
        return Response({'note': 'Use POST with multipart/form-data to submit an image for multi-crop disease prediction.'})
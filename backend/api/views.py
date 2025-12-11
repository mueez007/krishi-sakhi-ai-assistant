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
import requests
import os
import json

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
            prediction = ApiConfig.get_recommender_model().predict(np.array(features).reshape(1, -1))
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

        multicrop_model, multicrop_class_names = ApiConfig.get_multicrop_model()
        prediction = multicrop_model.predict(img_array)
        class_index = np.argmax(prediction[0])
        class_name = multicrop_class_names[class_index]
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
            prediction = ApiConfig.get_recommender_model().predict(np.array(features).reshape(1, -1))
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

        multicrop_model, multicrop_class_names = ApiConfig.get_multicrop_model()
        prediction = multicrop_model.predict(img_array)
        class_index = np.argmax(prediction[0])
        class_name = multicrop_class_names[class_index]
        confidence = np.max(prediction[0]) * 100
        
        return Response({
            'predicted_class': class_name.replace('___', ' | ').replace('_', ' '),
            'confidence_score': f'{confidence:.2f}%',
        })

    def get(self, request, *args, **kwargs):
        return Response({'note': 'Use POST with multipart/form-data to submit an image for multi-crop disease prediction.'})

# --- AI Assistant Endpoint ---
class AIAssistantView(APIView):
    def post(self, request, *args, **kwargs):
        print("\n" + "="*60)
        print("AI ASSISTANT - REQUEST RECEIVED")
        print("="*60)
        
        # Log all request details
        print(f"1. Request Method: {request.method}")
        print(f"2. Content-Type: {request.content_type}")
        print(f"3. Request data type: {type(request.data)}")
        print(f"4. Request data: {request.data}")
        
        # Extract message from request.data
        user_message = None
        
        # Check if request.data is a dictionary
        if isinstance(request.data, dict):
            # Try all possible parameter names
            param_names = ['message', 'question', 'query', 'text', 'input', 'prompt', 'content']
            for param in param_names:
                value = request.data.get(param)
                if value:
                    user_message = str(value).strip()
                    print(f"✓ Found in request.data['{param}']: {user_message[:50]}...")
                    break
        else:
            # If not a dict, try to convert to string
            user_message = str(request.data).strip()
            print(f"✓ Using request.data as string: {user_message[:50]}...")
        
        # If still no message, return error
        if not user_message:
            print("✗ ERROR: No message could be extracted!")
            return Response({
                'error': 'No message provided. Please send a JSON object like: {"message": "your question here"}',
                'received': {
                    'content_type': request.content_type,
                    'data_type': str(type(request.data)),
                    'data_preview': str(request.data)[:100]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"\n✓ Message to process: {user_message[:100]}...")
        
        # Now call Gemini API
        try:
            # Get API key
            api_key = 'AIzaSyDV0EJkSckGiCeB0ZdRvTE9yaN9cNwMKOE'
            
            # Use the available models from your test
            # These models are confirmed to exist with your API key
            model_names = [
                "gemini-2.5-flash",  # From your available models list
                "gemini-2.0-flash",  # From your available models list
                "gemini-pro-latest",  # From your available models list
                "gemini-flash-latest",  # From your available models list
                "gemini-2.0-flash-001",  # From your available models list
            ]
            
            system_instruction = """You are 'Krishi Sakhi,' an expert AI agronomist from the University of Agricultural Sciences, Bangalore. 
            Your knowledge is strictly limited to agriculture, farming, horticulture, and related government schemes. 
            You specialize in the crops, soil types, and climate of Karnataka, India. 
            Your language must be simple, direct, and easy for a farmer to understand. 
            If a user asks a question outside of this agricultural domain, politely refuse to answer."""
            
            payload = {
                'contents': [{'parts': [{'text': user_message}]}],
                'systemInstruction': {'parts': [{'text': system_instruction}]},
            }
            
            # Try each model until one works
            for model_name in model_names:
                api_url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}'
                print(f"\nTrying model: {model_name}")
                print(f"API URL: {api_url}")
                
                try:
                    response = requests.post(api_url, json=payload, timeout=10)
                    print(f"Status Code: {response.status_code}")
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        if 'candidates' in response_data and len(response_data['candidates']) > 0:
                            gemini_response = response_data['candidates'][0]['content']['parts'][0]['text']
                            print(f"✓ Success with model {model_name}! Response: {gemini_response[:100]}...")
                            print("="*60 + "\n")
                            return Response({'response': gemini_response})
                        else:
                            print(f"✓ Model responded but no candidates in response")
                    
                    # Log the error if not 200
                    print(f"✗ Model {model_name} returned {response.status_code}: {response.text[:150]}")
                    
                except requests.exceptions.RequestException as e:
                    print(f"✗ Network error with model {model_name}: {str(e)[:100]}")
                    continue
            
            # If no model worked, check if it's a quota issue
            print("✗ All models failed. Checking for quota issues...")
            
            # Try to get more details about quota
            quota_test_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}'
            quota_response = requests.post(quota_test_url, json=payload, timeout=5)
            
            if quota_response.status_code == 429:
                return Response({
                    'error': 'API quota exceeded',
                    'details': 'You have used up your free Gemini API quota. Please check your Google Cloud Console billing.',
                    'solution': '1. Go to Google Cloud Console 2. Enable billing 3. Check quota limits 4. Or get a new API key'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'All Gemini models failed',
                    'available_models': model_names,
                    'last_error': f'Status {quota_response.status_code}: {quota_response.text[:200]}'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                'error': f'Server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.urls import path
from .views import (
    LoginView,
    FarmListCreateView,
    RecommendFromLocationView,
    MultiCropDiseasePredictionView,
    AIAssistantView,
    register_user  # Add this import
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', register_user, name='register'),  # Add this line
    path('farms/', FarmListCreateView.as_view(), name='farm-list-create'),
    path('recommend-from-location/', RecommendFromLocationView.as_view(), name='recommend-from-location'),
    path('predict-disease-v2/', MultiCropDiseasePredictionView.as_view(), name='predict-disease-v2'),
    path('assistant/', AIAssistantView.as_view(), name='ai-assistant'),
]
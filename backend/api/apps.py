from django.apps import AppConfig
import pickle
import os
from django.conf import settings
from tensorflow.keras.models import load_model

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # Load Crop Recommender
    RECOMMENDER_PATH = os.path.join(settings.BASE_DIR, 'ml_models/crop_recommender_v2.pkl')
    with open(RECOMMENDER_PATH, 'rb') as f:
        recommender_model = pickle.load(f)
    print("V2.0 Crop Recommender model loaded successfully.")

    # Load Multi-Crop Doctor
    MULTICROP_MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models/multicrop_doctor_v2.h5')
    MULTICROP_CLASSES_PATH = os.path.join(settings.BASE_DIR, 'ml_models/multicrop_class_names_v2.pkl')
    
    multicrop_model = load_model(MULTICROP_MODEL_PATH)
    with open(MULTICROP_CLASSES_PATH, 'rb') as f:
        multicrop_class_names = pickle.load(f)
    print("V2.0 Multi-Crop Doctor model and class names loaded successfully.")


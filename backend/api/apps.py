from django.apps import AppConfig
import pickle
import os
from django.conf import settings

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # Models loaded lazily to avoid TensorFlow import issues at startup
    recommender_model = None
    multicrop_model = None
    multicrop_class_names = None

    @classmethod
    def get_recommender_model(cls):
        if cls.recommender_model is None:
            RECOMMENDER_PATH = os.path.join(settings.BASE_DIR, 'ml_models/crop_recommender_v2.pkl')
            with open(RECOMMENDER_PATH, 'rb') as f:
                cls.recommender_model = pickle.load(f)
            print("V2.0 Crop Recommender model loaded successfully.")
        return cls.recommender_model

    @classmethod
    def get_multicrop_model(cls):
        if cls.multicrop_model is None:
            from tensorflow.keras.models import load_model
            MULTICROP_MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models/multicrop_doctor_v2.h5')
            MULTICROP_CLASSES_PATH = os.path.join(settings.BASE_DIR, 'ml_models/multicrop_class_names_v2.pkl')
            
            cls.multicrop_model = load_model(MULTICROP_MODEL_PATH)
            with open(MULTICROP_CLASSES_PATH, 'rb') as f:
                cls.multicrop_class_names = pickle.load(f)
            print("V2.0 Multi-Crop Doctor model and class names loaded successfully.")
        return cls.multicrop_model, cls.multicrop_class_names

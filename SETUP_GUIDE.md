# Krishi Sakhi V2.0 - Complete Setup & Deployment Guide

## ✅ Project Status: READY TO USE

All components are now fully configured and ready for development/deployment.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- macOS (or Linux/Windows with minor adjustments)

### 1. Backend Setup (Django)

```bash
cd backend
. venv/bin/activate
pip install -r requirements.txt
```

**Start Backend Server:**
```bash
python manage.py runserver
```
Backend runs at: `http://127.0.0.1:8000/`

**Admin Panel:** `http://127.0.0.1:8000/admin/`
- Username: `admin`
- Password: `admin@123`

### 2. Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173/`

---

## 📋 Project Structure

```
Krishi_Sakhi_V2/
├── backend/
│   ├── venv/                          # Python virtual environment (Python 3.11)
│   ├── db.sqlite3                     # SQLite database
│   ├── requirements.txt               # Python dependencies
│   ├── manage.py                      # Django management
│   ├── krishi_sakhi/                  # Main Django project settings
│   │   ├── settings.py               # Django configuration
│   │   ├── urls.py                   # URL routing
│   │   └── wsgi.py                   # WSGI config
│   ├── api/                           # REST API app
│   │   ├── models.py                 # Database models
│   │   ├── views.py                  # API endpoints
│   │   ├── urls.py                   # API routes
│   │   ├── serializers.py            # DRF serializers
│   │   └── migrations/               # Database migrations
│   ├── ml_models/                     # ML training scripts
│   │   ├── train_crop_recommender_v2.py
│   │   └── train_multicrop_doctor_v2.py
│   └── data/                          # Dataset
│       ├── Crop_recommendation.csv
│       └── PlantVillage_V2/           # Plant disease images
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── src/
    │   ├── App.jsx                   # Main React component
    │   ├── App.css                   # Styling
    │   ├── main.jsx                  # React entry point
    │   ├── services/
    │   │   └── api.js                # API client configuration
    │   └── assets/
    └── public/
```

---

## 🔌 API Endpoints

### Authentication
- **POST** `/api/login/` - User login
  ```json
  { "username": "admin", "password": "admin@123" }
  ```
- **POST** `/api/register/` - User registration
  ```json
  { "username": "user", "password": "pass", "email": "user@example.com" }
  ```

### AI Features
- **POST** `/api/assistant/` - AI Assistant (Krishi Sakhi)
  ```json
  { "message": "What crops grow well in Karnataka?" }
  ```
- **POST** `/api/predict-disease-v2/` - Disease Detection
  ```multipart
  Form: image (file upload, jpeg/png)
  ```
- **POST** `/api/recommend-from-location/` - Crop Recommendation
  ```json
  { "latitude": 15.3173, "longitude": 75.7139 }
  ```

### Farm Management
- **GET/POST** `/api/farms/` - List/Create farms
- **GET/POST** `/api/recommend-from-location/` - Location-based recommendations

---

## 🤖 ML Models

### 1. Crop Recommender (V2.0)
- **Location:** `backend/ml_models/crop_recommender_v2.pkl`
- **Type:** Random Forest Classifier
- **Dataset:** 2,200 records
- **Features:** N, P, K, temperature, humidity, pH, rainfall
- **Output:** Recommended crop name

### 2. Multi-Crop Doctor (V2.0)
- **Location:** `backend/ml_models/multicrop_doctor_v2.h5`
- **Type:** MobileNetV2 CNN (Transfer Learning)
- **Classes:** 17 disease/health states (Corn, Potato, Tomato)
- **Accuracy:** 87.78% validation
- **Input:** 224x224 RGB leaf image
- **Output:** Disease classification + confidence score

#### Supported Diseases:
- **Corn:** Cercospora leaf spot, Common rust, Northern Leaf Blight, Healthy
- **Potato:** Early blight, Late blight, Healthy
- **Tomato:** Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites, Target Spot, Mosaic virus, Yellow Leaf Curl Virus, Healthy

---

## 🔐 Security Features

✅ CORS enabled for frontend-backend communication
✅ JWT token-based authentication (djangorestframework-simplejwt)
✅ Environment-based secrets (API keys can be stored in `.env`)
✅ SQLite database with migrations
✅ Password hashing with Django's built-in tools

---

## 📊 Database Models

### User (Django Built-in)
- id, username, email, password, is_staff, is_active, etc.

### Farm
- id, owner, farm_name, location, size_hectares, soil_type

### CropCycle
- id, farm, crop_name, start_date, end_date, status

### FarmerProfile
- id, user, district, language_preference, farm_size

---

## 🔄 Retraining ML Models

If you have new data, retrain the models:

### Crop Recommender:
```bash
cd backend
. venv/bin/activate
python ml_models/train_crop_recommender_v2.py
```

### Multi-Crop Doctor:
```bash
cd backend
. venv/bin/activate
python ml_models/train_multicrop_doctor_v2.py  # Takes 20-30 minutes
```

---

## 🛠️ Development Commands

### Backend

```bash
# Run migrations
python manage.py migrate

# Create superuser (interactive)
python manage.py createsuperuser

# Run tests
python manage.py test

# Django shell
python manage.py shell

# Generate API schema
python manage.py generateschema

# Collect static files (for production)
python manage.py collectstatic
```

### Frontend

```bash
# Development server with hot reload
npm run dev

# Build for production
npm build

# Preview production build
npm preview

# Lint code
npm run lint
```

---

## 📦 Key Dependencies

### Backend (Python)
- Django 4.2.13 - Web framework
- Django REST Framework 3.15.1 - REST API
- django-cors-headers 4.3.1 - CORS support
- TensorFlow 2.16.1 - ML models
- scikit-learn 1.4.2 - RandomForest
- Pillow 10.3.0 - Image processing
- pandas 2.2.2 - Data analysis

### Frontend (Node.js)
- React 19.1.1 - UI framework
- Vite 7.2.6 - Build tool
- Tailwind CSS 4.1.14 - Styling
- Axios 1.12.2 - HTTP client
- React Leaflet 5.0.0 - Map component

---

## 🚢 Deployment

### Production Backend (using Gunicorn)

```bash
pip install gunicorn
gunicorn krishi_sakhi.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Production Frontend (static build)

```bash
npm run build
# Serves optimized build from 'dist/' folder
```

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "krishi_sakhi.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## 📱 Features Implemented

✅ **Crop Recommender (Magic Map)** - AI-powered crop suggestions based on location
✅ **Multi-Crop Doctor** - Disease detection from leaf images
✅ **AI Assistant (Krishi Sakhi)** - Conversational AI for farming advice (Gemini-powered)
✅ **User Authentication** - Login/Registration
✅ **Farm Management** - Store farm details
✅ **Responsive UI** - Tailwind CSS styling
✅ **Map Integration** - Leaflet.js for interactive maps
✅ **Dark Theme** - Modern UI with green accent colors

---

## 🐛 Troubleshooting

### Issue: "Port 8000 already in use"
```bash
lsof -i :8000
kill -9 <PID>
```

### Issue: "ModuleNotFoundError" in Python
```bash
. venv/bin/activate
pip install -r requirements.txt
```

### Issue: Frontend can't connect to backend
- Ensure Django is running on `http://127.0.0.1:8000/`
- Check CORS settings in `backend/krishi_sakhi/settings.py`
- Verify API URL in `frontend/src/services/api.js`

### Issue: ML models not loading
- Check if `.pkl` and `.h5` files exist in `backend/ml_models/`
- Run training scripts if files are missing

---

## 📝 Notes for Future Development

1. **Database:** Currently using SQLite. For production, consider PostgreSQL
2. **Authentication:** Currently basic JWT. Add refresh token rotation for security
3. **Image Upload:** Implement S3/cloud storage for production
4. **API Rate Limiting:** Add rate limiting to prevent abuse
5. **Logging:** Set up proper logging for debugging
6. **Testing:** Add comprehensive unit and integration tests
7. **CI/CD:** Set up GitHub Actions for automated testing/deployment

---

## 📞 Support Resources

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- React Docs: https://react.dev/
- Vite Docs: https://vitejs.dev/
- TensorFlow Docs: https://www.tensorflow.org/

---

**Last Updated:** December 4, 2025
**Version:** 2.0
**Status:** ✅ Ready for Development/Deployment

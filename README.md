Krishi Sakhi V2.0 - The AI-Powered Digital Farming Companion

Krishi Sakhi V2.0 is a full-stack, AI-powered web application designed to be a digital companion for Indian farmers. It tackles the challenges of fragmented information and the lack of access to personalized, data-driven agricultural advice by integrating multiple AI models into a single, user-friendly platform.

This project was developed as a comprehensive solution for a college mini-project, inspired by multiple high-priority problem statements from the Smart India Hackathon (SIH).

✨ Key Features

This application combines three distinct AI-powered services into one cohesive user experience:

📍 "Magic Map" Crop Recommender:

An interactive map interface allows users to click on any location in Karnataka.

The backend receives the GPS coordinates and simulates fetching real-time soil and weather data for that exact spot.

A pre-trained Random Forest machine learning model analyzes these conditions to provide an instant, data-driven recommendation for the most suitable crop to plant.

🩺 "Multi-Crop Doctor":

A powerful computer vision tool for on-the-spot disease diagnosis.

Users can upload an image of a leaf from a Tomato, Potato, or Maize (Corn) plant.

The image is analyzed by a custom-trained Convolutional Neural Network (CNN) built with TensorFlow/Keras.

The model identifies one of 17 possible conditions (diseases or healthy) and returns a diagnosis with a confidence score.

🤖 Expert AI Assistant:

A specialized chatbot, powered by the Google Gemini API, designed to be an expert on farming in Karnataka.

It is guided by a strict system prompt to ensure it only answers questions related to agriculture, horticulture, local crops, and government schemes.

It politely refuses to answer off-topic questions, making it a focused and reliable tool for farmers.

🔒 Secure Authentication:

A complete user registration and login system to provide a secure and personalized experience for each farmer.

🛠️ Technology Stack

This project is built with a modern, professional full-stack architecture.

Category

Technology

Backend

Python, Django, Django REST Framework, Simple JWT

Frontend

React.js (with Vite), Tailwind CSS, Axios

AI / ML

TensorFlow/Keras, Scikit-learn, Pandas, NumPy

Mapping

React Leaflet, OpenStreetMap

LLM API

Google Gemini API

Database

SQLite (for development)

🚀 Getting Started

To run this project on your local machine, you will need two separate terminals.

Backend Setup

Navigate to the backend directory:

cd backend


Activate the virtual environment:

source venv/bin/activate


Start the Django server:

python3 manage.py runserver


The backend will be running at http://127.0.0.1:8000/.

Frontend Setup

Navigate to the frontend directory in a new terminal:

cd frontend


Start the Vite development server:

npm run dev


The frontend will be accessible at http://localhost:5173/.

🧠 AI Models

This project utilizes two custom-trained models located in the backend/ml_models directory.

Crop Recommender (crop_recommender_v2.pkl): A Random Forest Classifier trained on the Kaggle "Crop Recommendation Dataset" containing 2200 records of soil and climate data.

Multi-Crop Doctor (multicrop_doctor_v2.h5): A Convolutional Neural Network (using MobileNetV2 for transfer learning) trained on a curated subset of the PlantVillage dataset. It was trained on over 24,000 images across 17 classes for Tomato, Potato, and Maize.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.



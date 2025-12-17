import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

print("--- Krishi Sakhi V2.0: Crop Recommender Training ---")

# 1. Load the Full Dataset
data_path = 'data/Crop_recommendation.csv'
print(f"Loading dataset from: {data_path}")
try:
    df = pd.read_csv(data_path)
    print(f"Dataset loaded successfully with {len(df)} records.")
except FileNotFoundError:
    print(f"ERROR: The file was not found at {data_path}")
    print("Please ensure you have downloaded 'Crop_recommendation.csv' and placed it in the 'data' folder.")
    exit()

# 2. Prepare Data for Training
# X contains all the input features (N, P, K, etc.)
# y contains the target label (the name of the crop)
X = df.drop('label', axis=1)
y = df['label']
print("Data prepared for training.")

# 3. Initialize and Train the V2.0 Model
# We use the RandomForestClassifier, which is excellent for this task.
# We train on the ENTIRE dataset to make the final model as smart as possible.
model = RandomForestClassifier(n_estimators=150, random_state=42, n_jobs=-1)

print("Training the V2.0 Random Forest model on the full dataset...")
print("This may take a minute...")
model.fit(X, y)
print("Model training completed successfully.")

# 4. Save the V2.0 "AI Brain"
# The trained model is saved to a file, ready for our Django app to use.
model_filename = 'ml_models/crop_recommender_v2.pkl'
with open(model_filename, 'wb') as file:
    pickle.dump(model, file)

print(f"V2.0 Model saved successfully as: {model_filename}")
print("--------------------------------------------------")

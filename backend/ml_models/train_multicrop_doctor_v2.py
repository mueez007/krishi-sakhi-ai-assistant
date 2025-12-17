import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import os
import pickle

print("--- Krishi Sakhi V2.0: Multi-Crop Doctor Training ---")

# --- 1. SETUP ---
data_dir = 'data/PlantVillage_V2.'
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32 # A good default for larger datasets

print(f"Loading images from: {data_dir}")

# --- 2. DATA PREPARATION & AUGMENTATION ---
# Create an ImageDataGenerator to load and augment our images.
# Augmentation creates more variety in our training data, making the model more robust.
datagen = ImageDataGenerator(
    rescale=1./255,          # Normalize pixel values
    validation_split=0.2,    # Use 20% of images for validation
    rotation_range=40,       # Randomly rotate images
    width_shift_range=0.2,   # Randomly shift images horizontally
    height_shift_range=0.2,  # Randomly shift images vertically
    shear_range=0.2,         # Apply shear transformations
    zoom_range=0.2,          # Randomly zoom in on images
    horizontal_flip=True,    # Randomly flip images horizontally
    fill_mode='nearest'
)

# Create a generator for training data from the directory
train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

# Create a generator for validation data
validation_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

print(f"Found {train_generator.samples} images for training.")
print(f"Found {validation_generator.samples} images for validation.")

# Get the class names (our disease labels) which will be saved
class_names = list(train_generator.class_indices.keys())
num_classes = len(class_names)
print(f"Found {num_classes} classes (diseases): {class_names}")

# --- 3. MODEL BUILDING (TRANSFER LEARNING) ---
# Load MobileNetV2 pre-trained on ImageNet, without its top classification layer
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))

# Freeze the layers of the base model so they are not retrained
base_model.trainable = False

# Add our custom layers on top of the base model
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x) # Add a dropout layer to prevent overfitting
x = Dense(128, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x) # Final layer for our specific diseases

# Create the final model
model = Model(inputs=base_model.input, outputs=predictions)
print("V2.0 AI Model built successfully.")

# --- 4. MODEL TRAINING ---
# Compile the model with an optimizer, loss function, and metrics
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("Training the V2.0 Multi-Crop Doctor model...")
print("!!! THIS WILL TAKE A SIGNIFICANT AMOUNT OF TIME (15-30 minutes or more) !!!")

# Train the model
model.fit(
    train_generator,
    epochs=5, # 5 epochs is a good starting point for this large dataset
    validation_data=validation_generator
)
print("Model training completed successfully.")

# --- 5. SAVE THE TRAINED V2.0 MODEL ---
model_filename = 'ml_models/multicrop_doctor_v2.h5'
model.save(model_filename)

# Save the class names so our app knows what the model can predict
class_filename = 'ml_models/multicrop_class_names_v2.pkl'
with open(class_filename, 'wb') as f:
    pickle.dump(class_names, f)

print(f"V2.0 Model saved successfully as: {model_filename}")
print(f"Class names saved as: {class_filename}")
print("--------------------------------------------------")

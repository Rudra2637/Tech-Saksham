
import cv2
import os
import numpy as np
import tensorflow as tf
import pandas as pd
from datetime import datetime
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Parametersimport cv2
import os
import numpy as np
import tensorflow as tf
import pandas as pd
from datetime import datetime
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Dataset path
DATASET_DIR = 'dataset/'

# Function to preprocess images
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (100, 100))  # Resize for CNN input
    image = image / 255.0  # Normalize
    return image

# Load dataset
def load_dataset():
    images, labels = [], []
    label_map = {}
    for idx, person in enumerate(os.listdir(DATASET_DIR)):
        label_map[idx] = person
        person_path = os.path.join(DATASET_DIR, person)
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            images.append(preprocess_image(img_path))
            labels.append(idx)
    return np.array(images).reshape(-1, 100, 100, 1), np.array(labels), label_map

# Load data and split
X, y, label_map = load_dataset()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CNN Model
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(len(label_map), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Train the model
model = create_model()
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save model
model.save('face_recognition_model.h5')

# Load trained model
model = tf.keras.models.load_model('face_recognition_model.h5')

# Function to recognize face
def recognize_face(face):
    face = cv2.resize(face, (100, 100))
    face = face / 255.0
    face = face.reshape(1, 100, 100, 1)
    prediction = model.predict(face)
    label_index = np.argmax(prediction)
    return label_map.get(label_index, 'Unknown')

# Attendance marking
def mark_attendance(name):
    filename = 'attendance.csv'
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=['Name', 'Time'])
        df.to_csv(filename, index=False)
    df = pd.read_csv(filename)
    if name not in df['Name'].values:
        new_entry = pd.DataFrame({'Name': [name], 'Time': [timestamp]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f'Attendance marked for {name}')
    else:
        print(f'{name} already marked')

# Real-time face detection
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        name = recognize_face(face)
        mark_attendance(name)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow('Face Attendance', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

IMG_SIZE = (224, 224)  # MobileNetV2 default input size
BATCH_SIZE = 16
EPOCHS = 15  # Adjust based on your dataset size

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Define dataset directory
DATASET_DIR = 'dataset/'

# Load images from dataset in color
images = []
labels = []
label_map = {}
for idx, person in enumerate(os.listdir(DATASET_DIR)):
    label_map[idx] = person
    person_path = os.path.join(DATASET_DIR, person)
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        image = cv2.imread(img_path)  # Read in BGR format
        if image is None:
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
        image = cv2.resize(image, IMG_SIZE)
        images.append(image)
        labels.append(idx)

images = np.array(images)
labels = np.array(labels)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Data augmentation for training (helps with limited images)
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow(X_train, y_train, batch_size=BATCH_SIZE)
test_generator = test_datagen.flow(X_test, y_test, batch_size=BATCH_SIZE)

# Create the model using MobileNetV2 for transfer learning
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
base_model.trainable = False  # Freeze the base model

# Add a custom head for face recognition
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(len(label_map), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_generator, validation_data=test_generator, epochs=EPOCHS)

# Save the trained model
model.save('face_recognition_model.h5')

# Reload the trained model (optional, for clarity)
model = tf.keras.models.load_model('face_recognition_model.h5')

def recognize_face(face_gray):
    """
    Convert the detected grayscale face to a 3-channel image,
    resize it to the required input size, normalize, and predict.
    """
    face_color = cv2.cvtColor(face_gray, cv2.COLOR_GRAY2RGB)
    face_color = cv2.resize(face_color, IMG_SIZE)
    face_color = face_color / 255.0
    face_color = np.expand_dims(face_color, axis=0)
    prediction = model.predict(face_color)
    label_index = np.argmax(prediction)
    return label_map.get(label_index, "Unknown")

def mark_attendance(name):
    """
    Mark attendance by recording the name and current timestamp
    in an 'attendance.csv' file.
    """
    filename = 'attendance.csv'
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=['Name', 'Time'])
        df.to_csv(filename, index=False)
    df = pd.read_csv(filename)
    if name not in df['Name'].values:
        new_entry = pd.DataFrame({'Name': [name], 'Time': [timestamp]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f'Attendance marked for {name}')
    else:
        print(f'{name} already marked')

# Real-time face detection using webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        name = recognize_face(face_roi)
        mark_attendance(name)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow('Face Attendance', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

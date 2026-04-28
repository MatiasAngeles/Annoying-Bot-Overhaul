import tensorflow as tf
import numpy as np
from PIL import Image
import io

# Cambia la ruta a la carpeta donde descargaste el modelo
MODEL_PATH = "./tm_model/keras_model.h5"
LABELS_PATH = "./tm_model/labels.txt"

# Carga el modelo y las etiquetas
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    labels = [line.strip() for line in f.readlines()]

def predict_image(image_bytes):
    # Carga la imagen desde bytes
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))  # Tamaño estándar de Teachable Machine
    img_array = np.asarray(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    # Predicción
    predictions = model.predict(img_array)
    idx = np.argmax(predictions[0])
    label = labels[idx]
    prob = float(predictions[0][idx])
    return label, prob

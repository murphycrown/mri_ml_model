from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model("mri_model.keras")

IMG_SIZE = 224

@app.route("/")
def home():
    return "MRI Model API is running"

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["file"]
    img = Image.open(file).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)[0][0]

    result = "Tumor" if prediction > 0.5 else "No Tumor"

    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

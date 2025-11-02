from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import sqlite3
import sys  # <-- for Python version check

app = Flask(__name__)

# Load the trained model
model = load_model("emotion_detector.h5")

# Define emotion labels
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    if 'username' not in request.form:
        return 'No username provided', 400

    file = request.files['file']
    username = request.form['username']

    if file.filename == '':
        return 'No selected file', 400

    filepath = os.path.join('static', file.filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(48, 48), color_mode='grayscale')
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)
    predicted_emotion = emotions[np.argmax(prediction)]

    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS predictions (username TEXT, image_name TEXT, emotion TEXT)')
    c.execute('INSERT INTO predictions (username, image_name, emotion) VALUES (?, ?, ?)',
              (username, file.filename, predicted_emotion))
    conn.commit()
    conn.close()

    return render_template('index.html', emotion=predicted_emotion, image_path=filepath, username=username)

# TEMPORARY route to check Python version
@app.route('/check')
def check():
    return f"Python version on server: {sys.version}"

if __name__ == '__main__':
    app.run(debug=True)

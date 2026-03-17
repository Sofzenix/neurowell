import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from voice_text_emotion.text import analyze_text_emotion
from voice_text_emotion.speech import analyze_speech_emotion
import base64
import cv2
import numpy as np
from gen_ai_chatbot.chatbot import NeuroWellAI   # ✅ ADDED

app = Flask(__name__)
CORS(app)

bot = NeuroWellAI()   # ✅ ADDED
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Home route
@app.route("/")
def home():
    return " API is running "
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    result = bot.chat(user_input)

    # ✅ SAVE MOOD DATA TO ANALYTICS SERVER
    try:
        requests.post("http://127.0.0.1:5001/api/analytics/log_mood", json={
            "user_id": "1",
            "emotion": result["emotion"],
            "intensity": 5  # default intensity, could be inferred
        })
    except Exception as e:
        print(f"Failed to save mood to analytics: {e}")

    return jsonify(result)

# Text emotion analysis
@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text")

    result = analyze_text_emotion(text)
    return jsonify(result)


# Speech emotion analysis
@app.route("/analyze_speech", methods=["POST"])
def analyze_speech():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    save_path = "temp_audio.wav"

    audio_file.save(save_path)

    result = analyze_speech_emotion(save_path)

    if os.path.exists(save_path):
        os.remove(save_path)

    return jsonify(result)

# Face emotion analysis
@app.route("/analyze_face", methods=["POST"])
def analyze_face():
    data = request.get_json()
    image_data = data.get("image")
    if not image_data:
        return jsonify({"error": "No image provided"}), 400
        
    try:
        # Decode base64 image
        encoded_data = image_data.split(',')[1] if ',' in image_data else image_data
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(60, 60))

        if len(faces) == 0:
            return jsonify({"emotion": "No face detected"})

        for (x, y, w, h) in faces:
            # Simple heuristic emotion logic
            if w > 220:
                emotion = "Happy"
            elif h > 220:
                emotion = "Surprise"
            elif w < 120:
                emotion = "Sad"
            else:
                emotion = "Neutral"
            
            return jsonify({"emotion": emotion})
            
        return jsonify({"emotion": "Face logic incomplete"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
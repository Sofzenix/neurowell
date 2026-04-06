import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from voice_text_emotion.text import analyze_text_emotion
from voice_text_emotion.speech import analyze_speech_emotion
import base64
import cv2
import numpy as np
import sqlite3
from datetime import datetime
from gen_ai_chatbot.chatbot import NeuroWellAI

app = Flask(__name__)
CORS(app)

from analytics.dashboard import dashboard_bp
app.register_blueprint(dashboard_bp)

bot = NeuroWellAI()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Absolute path to shared DB
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "neurowell.db")

def log_mood_direct(emotion, intensity, source="chat"):
    """Save mood directly to SQLite — no HTTP call needed"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO moods (user_id, emotion, intensity, timestamp, source) VALUES (?,?,?,?,?)",
            ("1", emotion.lower(), int(intensity), datetime.now().isoformat(), source)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB log error: {e}")

# Home route
@app.route("/")
def home():
    return "API is running"

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    result = bot.chat(user_input)
    log_mood_direct(result["emotion"], 5, "chat")
    return jsonify(result)

# Text emotion analysis
@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text")

    result = analyze_text_emotion(text)
    conf = float(result.get("confidence", "0.5")) * 100 if "confidence" in result else 80
    log_mood_direct(result["emotion"], int(conf), "text")
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
    conf = float(result.get("confidence", "0.5")) * 100 if "confidence" in result else 80
    log_mood_direct(result["emotion"], int(conf), "voice")

    if os.path.exists(save_path):
        os.remove(save_path)
    return jsonify(result)

try:
    from deepface import DeepFace
    HAS_DEEPFACE = True
except ImportError:
    HAS_DEEPFACE = False

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

        if frame is None:
            return jsonify({"emotion": "Camera Error"})

        if not HAS_DEEPFACE:
            return jsonify({"emotion": "Still installing Video Analyzer module..."})

        # Use DeepFace for robust emotion detection
        try:
            # We set enforce_detection=False to avoid exceptions if face is not clear
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(result, list):
                result = result[0]
            emotion = result.get('dominant_emotion', 'neutral').capitalize()
            
            log_mood_direct(emotion.lower(), 85, "face")
            return jsonify({"emotion": emotion})
            
        except Exception as e:
            return jsonify({"emotion": "No emotion detected", "details": str(e)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
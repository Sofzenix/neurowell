import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from analytics.mood_tracker import save_mood
from flask import Flask, request, jsonify
from flask_cors import CORS
from voice_text_emotion.text import analyze_text_emotion
from voice_text_emotion.speech import analyze_speech_emotion
from gen_ai_chatbot.chatbot import NeuroWellAI   # ✅ ADDED

app = Flask(__name__)
CORS(app)

bot = NeuroWellAI()   # ✅ ADDED

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

    # ✅ SAVE MOOD DATA
    save_mood(
        result["emotion"],
        user_input,
        result["observation"]
    )

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


# ✅ NEW CHATBOT ROUTE
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    result = bot.chat(user_input)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
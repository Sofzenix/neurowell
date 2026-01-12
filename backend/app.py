from flask_cors import CORS
from flask import Flask, request, jsonify
from voice_text_emotion.text import analyze_text_emotion
from voice_text_emotion.speech import analyze_speech_emotion
import os

app = Flask(__name__)
CORS(app)
@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text")
    result = analyze_text_emotion(text)
    return jsonify(result)

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

if __name__ == "__main__":
    app.run(debug=True)

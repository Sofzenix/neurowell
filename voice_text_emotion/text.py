from transformers import pipeline

# Load emotion analysis model (Hugging Face)
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def analyze_text_emotion(text):
    """
    Analyze emotion from input text.
    Returns emotion label, sentiment, and confidence score.
    """

    if not text or text.strip() == "":
        return {
            "error": "Empty text input"
        }

    results = emotion_classifier(text)[0]

    # Find emotion with highest confidence
    top_emotion = max(results, key=lambda x: x["score"])

    emotion = top_emotion["label"]
    confidence = round(top_emotion["score"], 2)

    # Simple sentiment mapping
    if emotion in ["joy", "love"]:
        sentiment = "positive"
    elif emotion in ["anger", "sadness", "fear"]:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "input_text": text,
        "emotion": emotion,
        "sentiment": sentiment,
        "confidence": confidence
    }

# Local testing
if __name__ == "__main__":
    sample_text = "I feel anxious and stressed today"
    print(analyze_text_emotion(sample_text))

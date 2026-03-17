# ================================
# NeuroWell AI Chatbot
# GenAI Emotional Intelligence Bot
# ================================

from datetime import datetime


class NeuroWellAI:

    def __init__(self):
        self.disclaimer = (
            "\n\n⚠️ Disclaimer: This chatbot provides emotional support only "
            "and does NOT offer medical or psychological diagnosis."
        )
    def detect_emotion(self, user_input):
        user_input = user_input.lower()

        if any(word in user_input for word in ["stress", "tension", "pressure", "overwhelmed"]):
            return "stress"

        elif any(word in user_input for word in ["sad", "lonely", "depressed", "unhappy"]):
            return "sadness"

        elif any(word in user_input for word in ["anxious", "anxiety", "fear", "nervous"]):
            return "anxiety"

        else:
            return "general"

    def generate_response(self, emotion):

        if emotion == "stress":
            return (
                "I’m really sorry that you’re feeling stressed. 💙\n"
                "It’s completely okay to feel this way sometimes.\n\n"
                "🧘 Coping Strategy:\n"
                "- Take slow, deep breaths (inhale 4 sec, hold 4 sec, exhale 6 sec)\n"
                "- Step away from the stressor for a short break\n"
                "- Try writing down what’s worrying you"
                + self.disclaimer
            )

        elif emotion == "sadness":
            return (
                "It sounds like you’re feeling low, and I want you to know that your feelings matter. 🤍\n\n"
                "🌱 Gentle Suggestions:\n"
                "- Talk to someone you trust\n"
                "- Do a small activity you enjoy\n"
                "- Be kind to yourself today"
                + self.disclaimer
            )

        elif emotion == "anxiety":
            return (
                "I hear that you’re feeling anxious. You’re not alone. 🌸\n\n"
                "🫁 Grounding Exercise:\n"
                "- Name 5 things you can see\n"
                "- 4 things you can touch\n"
                "- 3 things you can hear\n"
                "- 2 things you can smell\n"
                "- 1 thing you can taste"
                + self.disclaimer
            )

        else:
            return (
                "Thank you for sharing how you feel. 🤍\n"
                "I’m here to listen and support you.\n\n"
                "You can talk to me about what’s on your mind."
                + self.disclaimer
            )
    def chat(self, user_input):

        emotion = self.detect_emotion(user_input)
        if "suicide" in user_input.lower() or "kill myself" in user_input.lower():
            return {
                "emotion": "critical",
                "response": "I'm really sorry you're feeling this way. You are not alone. Please consider talking to someone you trust or a mental health professional." + self.disclaimer,
                "observation": "User shows signs of severe emotional distress",
                "timestamp": str(datetime.now())
            }

        response = self.generate_response(emotion)
        observation_map = {
            "stress": "User is experiencing stress or pressure",
            "sadness": "User shows signs of sadness",
            "anxiety": "User is feeling anxious or nervous",
            "general": "User emotional state is neutral or unclear"
        }

        observation = observation_map.get(emotion, "General emotional state")

        return {
            "emotion": emotion,
            "response": response,
            "observation": observation,
            "timestamp": str(datetime.now())
        }
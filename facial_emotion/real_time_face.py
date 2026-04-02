import cv2
import os
import random

# Load Haar cascade safely
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

if not os.path.exists(cascade_path):
    print("❌ Haar cascade file not found")
    exit()

face_cascade = cv2.CascadeClassifier(cascade_path)

# Emotion labels
emotions = ["Happy", "Sad", "Angry", "Surprise", "Fear", "Disgust", "Neutral"]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not accessible")
    exit()

print("✅ Camera started. Press Q to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(60, 60)
    )
    try:
        from deepface import DeepFace
        for (x, y, w, h) in faces:
            face_roi_color = frame[y:y+h, x:x+w]
            try:
                # We enforce_detection=False to avoid crashes on bad frames
                result = DeepFace.analyze(face_roi_color, actions=['emotion'], enforce_detection=False)
                if isinstance(result, list):
                    result = result[0]
                emotion = result.get('dominant_emotion', 'Neutral').capitalize()
            except:
                emotion = "Neutral"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"Emotion: {emotion}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )
    except ImportError:
        cv2.putText(frame, "Waiting for DeepFace installation...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow("Live Facial Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

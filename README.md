# Module Name:Backend

## 👤 Owner
Name:Rammohan yerragola

## 🎯 Module Purpose
Briefly explain what this module does and which local business problem it solves.

## 🧩 Features
- Feature 1
- Feature 2
- Feature 3

## 🔧 Tech Stack
- Frontend:
- Backend:
- Database:
- APIs / Libraries:

## 🔄 Workflow / Logic
Step-by-step explanation of how your module works.

## 🔗 Integration Points
- Which modules interact with this one?
- APIs or data shared

## ▶️ How to Run This Module in VS Code

### 1️⃣ Prerequisites
- VS Code installed  
- Node.js / Python (mention required version)
- Git installed
_______________________________________________________________________________________________________________________________________________________________________________________________________________________
# Module NamemFacial Emotion
## 👤 Owner
Name:Sairupesh Nyani

## 🎯 Module Purpose
Briefly explain what this module does and which local business problem it solves.

## 🧩 Features
- Feature 1
- Feature 2
- Feature 3

## 🔧 Tech Stack
- Frontend:
- Backend:
- Database:
- APIs / Libraries:

## 🔄 Workflow / Logic
Step-by-step explanation of how your module works.

## 🔗 Integration Points
- Which modules interact with this one?
- APIs or data shared

## ▶️ How to Run This Module in VS Code

### 1️⃣ Prerequisites
- VS Code installed  
- Node.js / Python (mention required version)
- Git installed
_______________________________________________________________________________________________________________________________________________________________________________________________________________________

# Module Name : Voice and Text emotion analysis

## 👤 Owner
Name: Divyashree

## 🎯 Module Purpose
The Voice and Text Emotion Analysis module is responsible for detecting a user’s emotional state through text input and speech input.
It solves the problem of understanding user emotions in real time by converting speech to text, analyzing linguistic patterns using NLP models, and classifying emotions such as joy, anger, sadness, fear, etc.
This module enables NeuroWell to provide emotionally aware insights and support instead of generic responses.

## 🧩 Features
- Text-based emotion detection using NLP
- Speech-to-text conversion using audio processing
- Emotion classification with confidence score
- Sentiment categorization (positive / negative / neutral)
- Real-time frontend integration via REST APIs

## 🔧 Tech Stack
- Frontend: HTML, CSS, JavaScript (Fetch API for backend communication)
- Backend: Python, Flask, Flask-CORS
- Database: Not directly used in this module (emotion results can be stored by analytics module)
- APIs / Libraries: Hugging Face Transformers, PyTorch (Torch), SpeechRecognition, Pydub, Web Speech API (for browser-based voice input)

## 🔄 Workflow / Logic
Text Emotion Flow
1. User enters text in the Analyzer section.
2. Frontend sends a POST request to /analyze_text API.
3. Flask backend receives the text.
4. Hugging Face pre-trained emotion model processes the text.
5. Model returns emotion probabilities.
6. Highest-confidence emotion is selected.
7. Sentiment (positive/negative/neutral) is derived.
8. JSON response is sent back to frontend.
9. Emotion, sentiment, and confidence are displayed to the user.

Speech Emotion Flow
1. User uploads or records speech input.
2. Backend receives audio file via /analyze_speech.
3. SpeechRecognition converts audio to text.
4. Converted text is passed to text emotion analyzer.
5. Emotion and sentiment are predicted.
6. Results are returned as JSON.
7. Frontend displays transcribed text + emotion result.

## 🔗 Integration Points
## Interacts With:
- Frontend Analyzer UI
- Backend Flask app (app.py)
- Analytics module (for storing mood history)
- GenAI Chatbot module (for emotionally aware responses)

## APIs Provided:
- POST /analyze_text
- POST /analyze_speech

## Data Shared:
- Emotion label
- Sentiment
- Confidence score
- Transcribed text (for speech)

## ▶️ How to Run This Module in VS Code

### 1️⃣ Prerequisites
- VS Code installed
- Python 3.10 or above
- Git installed

### 2️⃣ Clone the Repository
git clone https://github.com/Sofzenix/neurowell.git and 
cd neurowell

### 3️⃣ Create Virtual Environment
python -m venv venv

Activate:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

### 4️⃣ Install Dependencies
pip install -r backend/requirements.txt

### 5️⃣ Run Backend Server
python -m backend.app

Server will run at:
http://127.0.0.1:5000

### 6️⃣ Open Frontend
Open:
frontend/dashboard.html
Go to:
Analyzer → Text or Voice
_______________________________________________________________________________________________________________________________________________________________________________________________________________________

# Module Name:Gen ai chatboat

## 👤 Owner
Name:Maounika

## 🎯 Module Purpose
Briefly explain what this module does and which local business problem it solves.

## 🧩 Features
- Feature 1
- Feature 2
- Feature 3

## 🔧 Tech Stack
- Frontend:
- Backend:
- Database:
- APIs / Libraries:

## 🔄 Workflow / Logic
Step-by-step explanation of how your module works.

## 🔗 Integration Points
- Which modules interact with this one?
- APIs or data shared

## ▶️ How to Run This Module in VS Code

### 1️⃣ Prerequisites
- VS Code installed  
- Node.js / Python (mention required version)
- Git installed
_______________________________________________________________________________________________________________________________________________________________________________________________________________________

# ModuleNames: Analytical Dashboard

## 👤 Owner
Name:Manjinath chinta

## 🎯 Module Purpose
Briefly explain what this module does and which local business problem it solves.

## 🧩 Features
- Feature 1
- Feature 2
- Feature 3

## 🔧 Tech Stack
- Frontend:
- Backend:
- Database:
- APIs / Libraries:

## 🔄 Workflow / Logic
Step-by-step explanation of how your module works.

## 🔗 Integration Points
- Which modules interact with this one?
- APIs or data shared

## ▶️ How to Run This Module in VS Code

### 1️⃣ Prerequisites
- VS Code installed  
- Node.js / Python (mention required version)
- Git installed
_______________________________________________________________________________________________________________________________________________________________________________________________________________________

# Module Name:Frontend

## 👤 Owner
Name:Arib

## 🎯 Module Purpose
Briefly explain what this module does and which local business problem it solves.

## 🧩 Features
- Feature 1
- Feature 2
- Feature 3

## 🔧 Tech Stack
- Frontend:
- Backend:
- Database:
- APIs / Libraries:

## 🔄 Workflow / Logic
Step-by-step explanation of how your module works.

## 🔗 Integration Points
- Which modules interact with this one?
- APIs or data shared

## ▶️ How to Run This Module in VS Code

### 1️⃣ Prerequisites
- VS Code installed  
- Node.js / Python (mention required version)
- Git installed
_______________________________________________________________________________________________________________________________________________________________________________________________________________________

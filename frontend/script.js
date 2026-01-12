// LOGIN
function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;
  if (user && pass) window.location.href="dashboard.html";
  else alert("Enter valid credentials!");
}

// CREATE PROFILE
function createProfile() {
  const name = document.getElementById("newName").value;
  const email = document.getElementById("newEmail").value;
  if(name && email) {
    alert(`Profile created for ${name}!`);
    window.location.href="index.html";
  } else alert("Fill all fields!");
}

// LOGOUT
function logout() { window.location.href="index.html"; }

// SIDEBAR
function toggleSidebar() { document.getElementById("sidebar").classList.toggle("collapsed"); }

// PAGE SWITCH
function showPage(id) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

async function sendMessage() {
    const input = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");
    const userMsg = input.value.trim();

    if (userMsg === "") return;

    // Show user message
    chatBox.innerHTML += `
        <div class="message user">${userMsg}</div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;
    input.value = "";

    // Thinking
    chatBox.innerHTML += `
        <div class="message bot" id="thinking">Thinking... ⏳</div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // CALL FLASK BACKEND
        const res = await fetch("http://127.0.0.1:5000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMsg })
        });

        const data = await res.json();

        // Remove thinking
        document.getElementById("thinking")?.remove();

        // Show reply
        chatBox.innerHTML += `
            <div class="message bot">${data.reply}</div>
        `;
    } catch (err) {
        console.error(err);
        document.getElementById("thinking")?.remove();
        chatBox.innerHTML += `
            <div class="message bot error">❌ Server error</div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}




// DASHBOARD CHARTS
const radarCtx=document.getElementById("emotionRadar");
if(radarCtx) new Chart(radarCtx,{type:"radar",data:{labels:["Happiness","Sadness","Anger","Calmness","Anxiety"],datasets:[{label:"Mood %",data:[82,40,25,70,35],backgroundColor:"rgba(44,182,125,0.3)",borderColor:"#2cb67d",borderWidth:2}]}});
const barCtx=document.getElementById("moodBar");
if(barCtx) new Chart(barCtx,{type:"bar",data:{labels:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],datasets:[{label:"Mood %",data:[70,75,60,82,68,80,77],backgroundColor:"#2cb67d"}]},options:{scales:{y:{beginAtZero:true,max:100}}}});
const pieCtx=document.getElementById("moodPie");
if(pieCtx) new Chart(pieCtx,{type:"pie",data:{labels:["Happy","Calm","Sad","Angry","Anxious"],datasets:[{data:[40,25,15,10,10],backgroundColor:["#2cb67d","#7f5af0","#f65a5a","#f5a623","#23a26f"]}]}});

// ANALYZER
// -----------------------
// ANALYZER FUNCTIONS
// -----------------------

// 1️⃣ Camera Emotion Analysis
function startCamera() { 
    const video = document.getElementById("videoFeed");
    
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
        })
        .catch(() => alert("Camera not accessible"));

    document.getElementById("analyze-result").innerText = "Analyzing face emotions...";
}

// 2️⃣ Voice-to-Text + Emotion Analysis
let recognition;  // Global speech recognition

function startVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Your browser does not support Speech Recognition.");
        return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();
    document.getElementById("analyze-result").innerText = "Listening... Please speak.";

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById("analyze-result").innerHTML = `You said: <b>${transcript}</b>`;
        analyzeEmotionFromText(transcript); // Use existing text emotion logic
    };

    recognition.onerror = (event) => {
        document.getElementById("analyze-result").innerText = `Error: ${event.error}`;
    };

    recognition.onend = () => {
        console.log("Speech recognition ended");
    };
}

// 3️⃣ Text Emotion Analysis (Backend Connected)
async function analyzeText() {
    const textArea = document.getElementById("textInput");
    const resultDiv = document.getElementById("analyze-result");

    // First click → show textarea
    if (textArea.style.display === "none") {
        textArea.style.display = "block";
        textArea.focus();
        resultDiv.innerHTML = "Enter text and click Text again to analyze.";
        return;
    }

    const text = textArea.value.trim();

    if (!text) {
        alert("Please enter some text");
        return;
    }

    resultDiv.innerHTML = "Analyzing emotion... ⏳";

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze_text", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        resultDiv.innerHTML = `
            <p><b>Emotion:</b> ${data.emotion}</p>
            <p><b>Sentiment:</b> ${data.sentiment}</p>
            <p><b>Confidence:</b> ${data.confidence}</p>
        `;
    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = "❌ Error connecting to backend";
    }
}



// 4️⃣ Optional: Analyze Text/Voice input for emotion
function analyzeEmotionFromText(text) {
    const emotions = ["Happy 😊","Sad 😢","Angry 😡","Calm 😌","Anxious 😟"];
    const detected = emotions[Math.floor(Math.random() * emotions.length)];
    document.getElementById("analyze-result").innerHTML += `<br>Detected Emotion: <b>${detected}</b>`;
}

// REPORT
function generateReport() {
  document.getElementById("report-output").innerHTML=`
    <h3>Neurowell Emotional Summary</h3>
    <p>Average Mood Score: <b>82%</b></p>
    <p>Dominant Emotion: <b>Happiness 😊</b></p>
    <p>Suggested Improvement: <b>Mindfulness & Sleep Schedule</b></p>`;
}
 
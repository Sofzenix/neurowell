// LOGIN
function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;
  
  if (user === "admin" && pass === "admin") {
      localStorage.setItem("isLoggedIn", "true");
      window.location.href = "dashboard.html";
  } else {
      alert("Invalid credentials! Try using admin / admin");
  }
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
function logout() { 
    localStorage.removeItem("isLoggedIn");
    window.location.href = "index.html"; 
}

// SIDEBAR
function toggleSidebar() { document.getElementById("sidebar").classList.toggle("collapsed"); }

// PAGE SWITCH
function showPage(id) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  if (id === "dashboard") {
      loadDashboard();
  }
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
        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMsg })
        });

        const data = await res.json();

        // Remove thinking
        document.getElementById("thinking")?.remove();

        // Show reply
        chatBox.innerHTML += `
            <div class="message bot">${data.response || data.reply || "I didn't quite get that."}</div>
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
let radarChart, barChart, pieChart;

async function loadDashboard() {
    try {
        const radarRes = await fetch("http://127.0.0.1:5000/api/analytics/charts/radar?user_id=1");
        const radarData = await radarRes.json();
        const radarCtx=document.getElementById("emotionRadar");
        if(radarCtx && radarData.success) {
            if (radarChart) radarChart.destroy();
            radarChart = new Chart(radarCtx,{
                type:"radar",
                data:{
                    labels:radarData.chart.labels,
                    datasets:[{
                        label:"Mood Count",
                        data:radarData.chart.data,
                        backgroundColor:"rgba(255, 159, 67, 0.4)",
                        borderColor:"#FF9F43",
                        pointBackgroundColor: "#FF4C60",
                        borderWidth:2
                    }]
                },
                options: {
                    scales: { r: { ticks: { color: "#fff", backdropColor: "transparent" }, grid: { color: "rgba(255,255,255,0.2)" }, pointLabels: { color: "#fff", font: { size: 14 } } } },
                    plugins: { legend: { labels: { color: "#fff" } } }
                }
            });
        }

        const barRes = await fetch("http://127.0.0.1:5000/api/analytics/charts/bar?user_id=1");
        const barData = await barRes.json();
        const barCtx=document.getElementById("moodBar");
        if(barCtx && barData.success) {
            if (barChart) barChart.destroy();
            barChart = new Chart(barCtx,{
                type:"bar",
                data:{
                    labels:barData.chart.labels,
                    datasets:[{
                        label:"Intensity",
                        data:barData.chart.data,
                        backgroundColor:["#FF4C60", "#FF9F43", "#F7D046", "#00E2C2", "#2cb67d", "#7B61FF", "#00D2FF"]
                    }]
                },
                options:{
                    scales:{
                        y:{ beginAtZero:true, max:10, ticks: { color: "#fff" }, grid: { color: "rgba(255,255,255,0.1)" } },
                        x:{ ticks: { color: "#fff" }, grid: { color: "rgba(255,255,255,0.1)" } }
                    },
                    plugins: { legend: { labels: { color: "#fff" } } }
                }
            });
        }

        const pieRes = await fetch("http://127.0.0.1:5000/api/analytics/charts/pie?user_id=1");
        const pieData = await pieRes.json();
        const pieCtx=document.getElementById("moodPie");
        if(pieCtx && pieData.success) {
            if (pieChart) pieChart.destroy();
            pieChart = new Chart(pieCtx,{
                type:"pie",
                data:{
                    labels:pieData.chart.map(d=>d.emotion),
                    datasets:[{
                        data:pieData.chart.map(d=>d.count),
                        backgroundColor:["#FF4C60", "#FF9F43", "#F7D046", "#00E2C2", "#7B61FF"],
                        borderWidth: 0
                    }]
                },
                options: {
                    plugins: { legend: { labels: { color: "#fff" } } }
                }
            });
        }

        const progRes = await fetch("http://127.0.0.1:5000/api/analytics/progress?user_id=1");
        const progData = await progRes.json();
        if (progData.success) {
            const containers = document.querySelectorAll("#dashboard .floating-card");
            if (containers.length >= 4) {
                const container = containers[3];
                let html = '<h2>💚 Mood Progress</h2>';
                const colorMap = {"happy": "#FF9F43", "calm": "#00E2C2", "anxious": "#FF4C60", "sad": "#7B61FF", "stress": "#F7D046", "neutral": "#2cb67d"};
                for (const [emotion, info] of Object.entries(progData.progress)) {
                    const barColor = colorMap[emotion] || "#00D2FF";
                    html += `
                    <div class="progress-bar">
                      <span style="font-weight: bold; margin-bottom: 8px;">${info.label}</span>
                      <div class="progress"><div class="fill" style="width:${info.width}%; background-color: ${barColor};"></div></div>
                    </div>`;
                }
                container.innerHTML = html;
            }
        }
    } catch (e) {
        console.error("Dashboard load error", e);
    }
}

// ANALYZER
// -----------------------
// ANALYZER FUNCTIONS
// -----------------------

// 1️⃣ Camera Emotion Analysis
let faceInterval;

function startCamera() { 
    const video = document.getElementById("videoFeed");
    const resultDiv = document.getElementById("analyze-result");
    
    // Create an invisible canvas for capturing frames
    let canvas = document.getElementById("captureCanvas");
    if (!canvas) {
        canvas = document.createElement("canvas");
        canvas.id = "captureCanvas";
        canvas.style.display = "none";
        document.body.appendChild(canvas);
    }
    const ctx = canvas.getContext("2d");

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            resultDiv.innerText = "Analyzing face emotions...";
            
            // Set up interval to capture frames every 1 second
            if (faceInterval) clearInterval(faceInterval);
            faceInterval = setInterval(async () => {
                if (!video.videoWidth) return;
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL("image/jpeg", 0.5);
                
                try {
                    const res = await fetch("http://127.0.0.1:5000/analyze_face", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ image: imageData })
                    });
                    const data = await res.json();
                    if (data.emotion) {
                        resultDiv.innerHTML = `Face detected emotion: <b>${data.emotion}</b>`;
                    }
                } catch (e) {
                    console.error("Face API Error:", e);
                }
            }, 1000);
        })
        .catch(() => alert("Camera not accessible"));
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
async function analyzeEmotionFromText(text) {
    const resultDiv = document.getElementById("analyze-result");
    resultDiv.innerHTML += `<br>Analyzing text for emotion... ⏳`;

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze_text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        
        if (data.emotion) {
             resultDiv.innerHTML += `<br>Detected Emotion: <b>${data.emotion} (Confidence: ${data.confidence})</b>`;
        } else {
             resultDiv.innerHTML += `<br>Detected Emotion: <b>Error reading emotion</b>`;
        }
    } catch (error) {
        console.error(error);
        resultDiv.innerHTML += "<br>❌ Error connecting to text backend";
    }
}

// REPORT
async function generateReport() {
    document.getElementById("report-output").innerHTML = "Generating report...";
    try {
        const res = await fetch("http://127.0.0.1:5000/api/analytics/report/generate?user_id=1");
        const data = await res.json();
        if (data.success) {
            const element = document.createElement("div");
            element.innerHTML = data.html;
            const opt = {
                margin:       0.5,
                filename:     'mood_report.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2 },
                jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' },
                pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
            };
            html2pdf().set(opt).from(element).save();
            document.getElementById("report-output").innerHTML = `<p>Report downloaded successfully as PDF!</p>`;
        } else {
            document.getElementById("report-output").innerHTML = `<p>Error generating report: ${data.error}</p>`;
        }
    } catch (e) {
        document.getElementById("report-output").innerHTML = `<p>Error connecting to analytics API.</p>`;
    }
}
 
document.addEventListener("DOMContentLoaded", function() {
    var sendBtn = document.getElementById("send-btn");
    var chatInput = document.getElementById("chat-input");

    if (sendBtn) {
        sendBtn.onclick = function() { sendMessage(); return false; };
    }

    if (chatInput) {
        chatInput.onkeydown = function(e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        };
    }
});
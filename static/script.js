const synth = window.speechSynthesis;
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";

let apiKey = "";

function saveApiKey() {
  const keyInput = document.getElementById("apiKeyInput");
  const keyStatus = document.getElementById("keyStatus");
  const micButton = document.getElementById("micButton");
  
  apiKey = keyInput.value.trim();
  
  if (apiKey) {
    keyStatus.textContent = "API Key saved successfully!";
    keyStatus.className = "key-status success";
    micButton.disabled = false;
    micButton.style.backgroundColor = "#007bff";
    micButton.style.cursor = "pointer";
  } else {
    keyStatus.textContent = "Please enter a valid API key";
    keyStatus.className = "key-status error";
    micButton.disabled = true;
  }
}

function startListening() {
  if (!apiKey) {
    alert("Please enter your OpenAI API key first!");
    return;
  }

  recognition.start();

  recognition.onresult = async (event) => {
    const question = event.results[0][0].transcript;
    appendMessage("user", question);

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question, apiKey})
      });

      const data = await res.json();
      
      if (data.error) {
        appendMessage("bot", `Error: ${data.error}`);
      } else {
        appendMessage("bot", data.answer);
      }
    } catch (error) {
      appendMessage("bot", "Sorry, there was an error processing your request.");
    }
  };
}

function appendMessage(role, text) {
  const chatBox = document.getElementById("chatBox");
  const message = document.createElement("div");
  message.className = `message ${role}`;
  message.innerHTML = `<span class="${role}">${role === "user" ? "You" : "Bot"}:</span> ${text}`;
  chatBox.appendChild(message);
  chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to bottom
}

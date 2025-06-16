const synth = window.speechSynthesis;
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";

function startListening() {
  recognition.start();

  recognition.onresult = async (event) => {
    const question = event.results[0][0].transcript;
    appendMessage("user", question);

    const res = await fetch("/ask", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question})
    });

    const data = await res.json();
    appendMessage("bot", data.answer);
    synth.speak(new SpeechSynthesisUtterance(data.answer));
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

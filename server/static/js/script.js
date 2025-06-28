function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chat-box");

  // Display user message
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.textContent = message;
  chatBox.appendChild(userMsg);
  chatBox.scrollTop = chatBox.scrollHeight;

  input.value = "";

  fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: message,
      character: character.toLowerCase()
    })
  })
  .then(res => res.json())
  .then(data => {
    // Add a 2-second delay before displaying the bot's response
    setTimeout(() => {
      const botMsg = document.createElement("div");
      botMsg.className = "message bot";
      botMsg.textContent = data.response;
      chatBox.appendChild(botMsg);
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 2000); // 2000 ms = 2 seconds
  })
  .catch(err => {
    const errMsg = document.createElement("div");
    errMsg.className = "message bot";
    errMsg.textContent = "Error fetching divine wisdom.";
    chatBox.appendChild(errMsg);
  });
}

// ➕ Add this part to enable Enter key to send message
document.getElementById("user-input").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevents newline
    sendMessage();
  }
});

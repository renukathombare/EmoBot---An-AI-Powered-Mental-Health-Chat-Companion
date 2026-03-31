const chat = document.getElementById("chat-box");
const input = document.getElementById("input");
const picker = document.getElementById("picker");
const emojiBtn = document.getElementById("emoji");

// Load chat history
window.onload = () => {
    chat.innerHTML = localStorage.getItem("chat") || "";
};

// Save chat
function save() {
    localStorage.setItem("chat", chat.innerHTML);
}

// Add message
function add(text, type) {
    let div = document.createElement("div");
    div.className = "msg " + type;
    div.innerText = text;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    save();
}

// Send message
function send() {
    let msg = input.value.trim();
    if (!msg) return;

    add("You: " + msg, "user");

    fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: msg }),
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        add("EmoBot: " + data.reply, "bot");
    });

    input.value = "";
}

// Enter key
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") send();
});

// Emoji toggle
emojiBtn.onclick = () => {
    picker.style.display = picker.style.display === "none" ? "block" : "none";
};

// Insert emoji
picker.addEventListener("emoji-click", e => {
    input.value += e.detail.unicode;
});
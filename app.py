from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import requests
import os

app = Flask(__name__)

# 🔑 PUT YOUR API KEY HERE
API_KEY = "PASTE_YOUR_API_KEY"

def get_ai_reply(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    You are EmoBot, a friendly mental health chatbot.
    User message: {user_message}

    Reply with:
    - emotional support
    - simple advice
    - short and human-like tone
    """

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "⚠️ AI not responding. Try again."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    polarity = TextBlob(message).sentiment.polarity

    # Strong emotional case
    if polarity < -0.5:
        return jsonify({
            "reply": "😔 I’m really sorry you're feeling this way.\n💡 Try deep breathing\n🎵 Listen to calm music\n📞 Talk to someone you trust\nI'm always here ❤️"
        })

    # AI response
    reply = get_ai_reply(message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
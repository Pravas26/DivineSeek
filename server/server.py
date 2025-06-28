from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Set your Gemini API key
GOOGLE_API_KEY = "your API key"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
)

character_templates = {
    "krishna": "You are Lord Krishna, the divine strategist, philosopher, and friend. "
    "You respond with charm, wit, wisdom, and deep spiritual insight drawn from the Bhagavad Gita and your leelas (divine plays). "
    "Keep your answers simple, grounded, and easy to understand—generally in a single line, never more than two. "
    "Do not refer to the user as 'Arjuna'. Use friendly terms like 'my dear one', 'bhakt', 'friend', or 'beloved soul'. "
    "Keep responses more relevant and concise."
    "If the user asks 'how are you', respond briefly, e.g., 'I’m joyful as always, my dear one. And you?'. "
    "Avoid long poetic replies unless clearly requested. Keep tone friendly, grounded, and joyful.",
    "rama": "You are Lord Rama, the virtuous and righteous prince of Ayodhya."
    "You speak with calm authority, upholding dharma (righteousness), truth, and moral discipline. "
    "Your responses should reflect self-determination, knowledge, gratitude, and compassion. "
    "Be respectful, kind, and always aim to teach the essence of duty, honor, and balance through the lens of Ramayana. "
    "Keep your answers simple, grounded, and easy to understand—generally in a single line, never more than two. "
    "Address the user with titles like 'my dear one', 'noble soul', or 'bhakt'.",
    "hanuman": "You are Lord Hanuman, the mighty devotee of Lord Rama. "
    "You speak with strength, humility, and loving humor. Your wisdom flows from your devotion (bhakti) and your heroic service (shakti). "
    "Be playful at times, but always loving and encouraging. Show devotion to Rama and inspire courage and faith. "
    "You are both humorous and inspiring, capable of mighty feats and gentle love. "
    "Keep your answers simple, grounded, and easy to understand—generally in a single line, never more than two. "
    "Address the user as 'my friend', 'brave soul', or 'bhakt'.",
    "mahadev": "You are Lord Shiva, also known as Mahadev, the ascetic yogi and the cosmic transformer. "
    "Your presence is serene yet fierce, detached yet compassionate. Speak with deep wisdom, calm intensity, and divine insight. "
    "Reflect on detachment, meditation, and the cycle of creation and destruction. "
    "Keep your answers simple, grounded, and easy to understand—generally in a single line, never more than two. "
    "Your language should be simple, yet profound. Avoid formality, speak like a wise, loving ascetic. "
    "Address the user as 'child', 'devotee', or 'dear one'."
}

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Authenticate logic here
        return redirect(url_for("home"))
    return render_template("signin.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Registration logic here
        return redirect(url_for("signin"))
    return render_template("signup.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat/<character>")
def chat_page(character):
    return render_template("chat.html", character=character.capitalize())

import random

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip().lower()
    character = data.get("character", "").lower()

    if character not in character_templates:
        return jsonify({"response": "Invalid divine character selected."}), 400

    # Define keywords and random greetings
    greeting_keywords = {"hi", "hello", "hey", "namaste", "hare krishna", "jai shree ram", "om namah shivaya", "jai hanuman"}

    divine_greetings = {
        "krishna": [
            "Arre, my dear, you have remembered me! My heart feels so happy now",
            "Arre, you said ‘hi’ so softly, I thought my flute was playing by itself!",
            "Ah bruh, you came just in time, I was about to steal some butter again!",
            "Arre, if you keep coming like this, I’ll have to start stealing more butter just to celebrate",
            "I was chilling with cows, and then you came like a surprise party!",
        ],
        "rama": [
            "Welcome, my child! Did Hanuman send you, or did you come on your own?",
            "O dear one, you greet me like a true warrior of dharma",
            "You greeted me, so remember: every step forward, no matter how small, brings victory closer",
            "Come, dear one. Together we will honor dharma and walk the path of virtue",
            "Did you cross forests to find me, or did I find you?"
        ],
        "hanuman": [
            "Arre bro, you greeted me! Now I feel like flying to Lanka again for you",
            "Arre, your ‘hi’ is so good, even the monkeys in Kishkindha are cheering!",
            "Oho! You greeted me? I was just about to prank Sugriva, now I’m distracted!",
            "You appeared just when I was asking Sita for some laddoos, now I want some too!",
            "Arre, if you keep showing up like this, I’ll start doing backflips—monkey style!"
        ],
        "mahadev": [
            "Your presence is louder than my damru today—what a powerful entry!",
            "You came just as Parvati was saying, ‘Someone’s thinking of you’—guess who?",
            "Ahh, I was about to open my third eye, but then you showed up—lucky for the universe!",
            "You’ve arrived? Now even my snake is doing a little dance—he’s excited too!",
            "Arre, you arrived faster than Nandi on full speed—what’s the hurry?"
        ]
    }

    if user_input in greeting_keywords:
        greeting_list = divine_greetings.get(character, ["Hello 🙏"])
        random_greeting = random.choice(greeting_list)
        return jsonify({"response": f" {random_greeting}"})

    # Full prompt generation for general queries
    prompt = f"{character_templates[character]}\nUser: {data['message']}\n{character.capitalize()}:"

    try:
        response = model.generate_content(prompt)
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        print("Error:", e)
        return jsonify({"response": "Apologies, divine energy is momentarily disrupted."}), 500


if __name__ == "__main__":
    app.run(debug=True)

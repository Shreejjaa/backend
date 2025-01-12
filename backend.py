from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Predefined responses for emotions
emotion_responses = {
    "happy": [
        "You seem happy! What's the good news?",
        "Glad to see you're happy! Tell me more!",
        "Happiness looks great on you. What made your day?"
    ],
    "sad": [
        "I'm sorry you're feeling sad. Want to talk about it?",
        "It's okay to feel down sometimes. I'm here to listen.",
        "What happened? Talking might help."
    ],
    "neutral": [
        "How's your day going?",
        "Anything interesting happening today?",
        "What would you like to talk about?"
    ],
    "angry": [
        "Take a deep breath. I'm here if you want to talk.",
        "It's okay to vent. What's bothering you?",
        "I'm sorry you're upset. How can I help?"
    ],
    "surprised": [
        "Wow, you seem surprised! Tell me what's on your mind.",
        "Surprises are fun! What's going on?",
        "Something unexpected happened? I'm curious!"
    ]
}

# Intent-based responses
intent_responses = {
    "greeting": ["Hello! How can I assist you?", "Hi there! What's on your mind?"],
    "farewell": ["Goodbye! Take care.", "See you later!"],
    "thanks": ["You're welcome!", "Happy to help!"],
    "advice": ["Life has its ups and downs. Stay strong.", "Believe in yourself. You can do it!"],
    "unknown": ["That's interesting! Tell me more.", "I see. Can you elaborate?"]
}

def detect_intent(user_message):
    """
    Analyze user input to determine intent.
    """
    doc = nlp(user_message.lower())

    # Simple keyword matching for intents
    if any(token.text in ["hi", "hello", "hey"] for token in doc):
        return "greeting"
    elif any(token.text in ["bye", "goodbye", "see you"] for token in doc):
        return "farewell"
    elif any(token.text in ["thanks", "thank you"] for token in doc):
        return "thanks"
    elif any(token.text in ["advice", "help", "suggest"] for token in doc):
        return "advice"
    else:
        return "unknown"

# Chatbot route
@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        # Get data from request
        data = request.json
        emotion = data.get('emotion', 'neutral')
        user_message = data.get('message', '').lower()

        # Select response based on emotion
        response = random.choice(emotion_responses.get(emotion, emotion_responses["neutral"]))

        # Handle user message with intent detection
        if user_message:
            intent = detect_intent(user_message)
            response = random.choice(intent_responses.get(intent, intent_responses["unknown"]))

        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Oops! Something went wrong. Please try again."}), 500

# Run the app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

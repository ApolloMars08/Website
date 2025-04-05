from flask import Flask, request, render_template_string
from openai import OpenAI
import os

Code = Flask(__name__)

# Grok API-Client mit deinem Schlüssel
client = OpenAI(
    api_key="xai-JFDe0guvhLP8YkCg75V76cqXZK3GEY8mngOYOWFFpiR37y38QEEAApJtzYE6JM5LGdk6BG9EF5QZs2Dw",  # Deinen xAI API-Schlüssel hier einfügen
    base_url="https://api.x.ai/v1"
)

# Liste für den Chatverlauf
chat_history = []

# HTML mit Chatverlauf
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Grok Chat</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chat-container { max-width: 600px; margin: auto; }
        .chat-box { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
        .message { margin: 5px 0; padding: 5px; }
        .user { background-color: #e0f7fa; text-align: right; }
        .grok { background-color: #f1f1f1; text-align: left; }
        textarea { width: 100%; height: 100px; margin-bottom: 10px; }
        button { padding: 5px 10px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>Chat mit Grok</h1>
        <div class="chat-box">
            {% for sender, message in chat_history %}
                <div class="message {{ 'user' if sender == 'Du' else 'grok' }}">
                    <strong>{{ sender }}:</strong> {{ message }}
                </div>
            {% endfor %}
        </div>
        <form method="POST">
            <textarea name="prompt" placeholder="Schreib deinen Prompt hier..."></textarea>
            <button type="submit">Senden</button>
        </form>
    </div>
</body>
</html>
"""

@Code.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        prompt = request.form["prompt"]
        # Füge die Nutzernachricht zum Verlauf hinzu
        chat_history.append(("Du", prompt))
        try:
            # API-Aufruf an Grok
            completion = client.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": prompt}]
            )
            grok_response = completion.choices[0].message.content
            # Füge Groks Antwort zum Verlauf hinzu
            chat_history.append(("Grok", grok_response))
        except Exception as e:
            chat_history.append(("Grok", f"Fehler: {str(e)}"))
    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Nimmt den Port vom Server oder 5000 lokal
    Code.run(host="0.0.0.0", port=port, debug=True)
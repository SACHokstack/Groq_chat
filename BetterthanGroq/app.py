from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Set up Groq client with the API key directly in the code
api_key = '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'
client = Groq(api_key=api_key)

# Initialize system prompt and chat history
system_prompt = {
    "role": "system",
    "content": "You are a helpful assistant. You reply with very short answers."
}
chat_history = [system_prompt]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json.get('message')

    chat_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=100,
        temperature=1.2
    )

    assistant_message = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_message})

    return jsonify({"reply": assistant_message})

if __name__ == '__main__':
    app.run(debug=True)

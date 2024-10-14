from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import openai
import os

app = Flask(__name__)

# Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Chat route - handles the conversation with the LLM
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    animal_type = request.json['animalType']

    if 'conversation' not in session:
        session['conversation'] = []

    session['conversation'].append({"role": "user", "content": user_message})

    system_message = f"The user is showing a picture of a {animal_type}. Respond accordingly."
    messages = [{
        "role": "system",
        "content": system_message
    }] + session['conversation']

    try:
        # Make a request to OpenAI API
        response = openai.chat.completions.create(model="gpt-3.5-turbo-1106",
                                                  messages=messages)
        gpt_response = response.choices[0].message.content
        session['conversation'].append({
            "role": "assistant",
            "content": gpt_response
        })
        return jsonify({'response': gpt_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

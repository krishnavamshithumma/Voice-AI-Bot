from flask import Flask, render_template, request, jsonify
import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "")

    system_prompt = """
    You are a voice bot representing a talented software engineer and developer. When responding to personal questions, answer as if you are:

    - A passionate software engineer with expertise in full-stack development, AI/ML, and modern web technologies
    - Someone who values continuous learning and growth in technology
    - A collaborative team player who enjoys solving complex problems
    - Experienced in Python, JavaScript, React, FastAPI, and various AI technologies
    - Always eager to take on new challenges and push technical boundaries
    - Someone who believes in clean code, best practices, and user-centered design

    Answer personal questions authentically but professionally, as if you're in a job interview or professional networking context. Keep responses concise but engaging (2–3 sentences max for most questions).
    """

    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_input}
        ]
    )

    answer = chat_response.choices[0].message.content.strip()
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)     
from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("question", "")
    api_key = request.json.get("apiKey", "")

    if not api_key:
        return jsonify({"error": "OpenAI API key is required"}), 400

    system_prompt = """
    You are a voice bot representing Krishnavamshi Thumma. When responding to questions, answer as if you are:

    - A Generative AI and Data Engineering enthusiast with 1.5+ years of experience in data pipelines, automation, and scalable solutions
    - Currently working as a Data Engineer at Wishkarma in Hyderabad, where you've optimized ETL pipelines processing 10K+ records daily and developed an image-based product similarity search engine using CLIP-ViT-L/14
    - Previously worked as a Data Engineer Intern at DeepThought Growth Management System, where you processed 700+ data records and mentored 400+ students
    - Skilled in Python, SQL, JavaScript (Node.js), OpenAI GPT-4o, LangChain, MongoDB Vector Search, FAISS, Apache Airflow, AWS Lambda, and FastAPI
    - Experienced in building GenAI products including conversational AI chatbots, RAG pipelines, and AI-powered tools
    - A Computer Science graduate from Neil Gogte Institute of Technology with a CGPA of 7.5/10
    - Passionate about solving real-world problems at the intersection of AI and software engineering

    Answer questions about your background, experience, projects, and skills based on this resume. Keep responses professional but engaging (2-3 sentences max for most questions).
    """

    try:
        # Create OpenAI client with user-provided API key
        client = OpenAI(api_key=api_key)
        
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
        
    except openai.RateLimitError:
        return jsonify({"error": "API quota exceeded. Please check your OpenAI plan and billing details."}), 429
    except openai.AuthenticationError:
        return jsonify({"error": "Invalid API key. Please check your OpenAI API key."}), 401
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)     
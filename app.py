import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    roadmap = None
    goal = None

    if request.method == "POST":
        goal = request.form.get("goal")
        roadmap = generate_roadmap(goal)

    return render_template("index.html", roadmap=roadmap, goal=goal)


def generate_roadmap(goal: str):
    """
    Generates a detailed roadmap using the Gemini API.
    """
    try:
        prompt = f"""
        You are an expert career mentor. Generate a step-by-step professional learning roadmap for becoming an expert in "{goal}".
        The roadmap should be organized by phases (beginner → intermediate → advanced) and contain actionable, measurable goals.
        Return a clean, human-readable markdown-style response, also be precise and give me a medium sized response(on a scale of 1-5 i want the length to be 2.5).
        """

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()

        html_text = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        return html_text
    except Exception as e:
        return f"⚠️ Error generating roadmap: {e}"


@app.route("/api/roadmap", methods=["POST"])
def api_generate():
    data = request.get_json()
    goal = data.get("goal")
    roadmap = generate_roadmap(goal)
    return jsonify({"goal": goal, "roadmap": roadmap})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
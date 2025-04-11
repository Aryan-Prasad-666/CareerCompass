from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import json
import re
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


@app.route('/generate-roadmap', methods=['POST'])
def generate_roadmap():
    data = request.get_json()
    name = data.get('name', 'User')
    career_goal = data.get('careerGoal', '')
    current_skills = data.get('currentSkills', '')
    experience = data.get('experience', 'beginner')
    interests = data.get('interests', '')

    prompt = f"""
    Generate a detailed career roadmap for {name}, who wants to become a {career_goal}.
    Current skills: {current_skills or 'none listed'}.
    Experience level: {experience}.
    Interests: {interests or 'none listed'}.
    Provide a step-by-step plan with:
    - 3-5 milestones with specific titles, timeframes (e.g., '0-6 months'), and detailed descriptions.
    - For each milestone, list 3-5 specific skills to learn (tailored to the career goal and current skills).
    - Include 2-4 actionable resources (e.g., websites, courses, books) with names and URLs if possible.
    - Make the roadmap practical, motivational, and detailed, with clear progression from {experience} level to achieving {career_goal}.
    Return the response in valid JSON format with this structure:
    [
      {{
        "milestone": "title",
        "timeframe": "duration",
        "description": "detailed text",
        "skills": ["skill1", "skill2", ...],
        "resources": [{{"name": "resource name", "url": "resource url"}}, ...]
      }},
      ...
    ]
    Ensure the output is strictly valid JSON, enclosed in square brackets, with no extra text, markdown, or comments outside the JSON structure.
    """

    try:
        response = model.generate_content(prompt)
        raw_response = response.text
        print("Raw Gemini Response:", raw_response)  # Debug output to terminal

        json_match = re.search(r'\[.*\]', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            raise ValueError("No valid JSON array found in response")

        try:
            roadmap = json.loads(json_str)
        except json.JSONDecodeError as e:
            json_str = json_str.replace("'", '"').strip()
            roadmap = json.loads(json_str)

        if not isinstance(roadmap, list):
            raise ValueError("Response is not a JSON array")
        for item in roadmap:
            if not all(key in item for key in ["milestone", "timeframe", "description", "skills", "resources"]):
                raise ValueError("Invalid roadmap item structure")

        return jsonify(roadmap)

    except Exception as e:
        print("Error:", str(e))  # Log error to terminal
        mock_roadmap = [
            {
                "milestone": f"Start Your {career_goal} Journey",
                "timeframe": "0-6 months",
                "description": f"Begin your path to becoming a {career_goal} with foundational skills.",
                "skills": ["Skill 1", "Skill 2", "Skill 3"],
                "resources": [
                    {"name": "Example Course", "url": "https://example.com"},
                    {"name": "Tutorial Site", "url": "https://tutorial.com"}
                ]
            },
            {
                "milestone": "Build Practical Experience",
                "timeframe": "6-12 months",
                "description": f"Apply your skills to real-world {career_goal} projects.",
                "skills": ["Project Skill 1", "Project Skill 2"],
                "resources": [
                    {"name": "GitHub", "url": "https://github.com"},
                    {"name": "Docs", "url": "https://docs.example.com"}
                ]
            }
        ]
        return jsonify(mock_roadmap), 200
    
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    prompt = f"""
    You are a personal career guidance mentor. Respond to the user query: "{query}" with short, concise, and practical advice in bullet points. 
    - Keep each point brief (1-2 sentences max).
    - Focus on actionable steps, key skills, or resources relevant to career development.
    - Use a friendly, encouraging tone.
    - Return the response as plain text with bullet points (e.g., - Point 1\n- Point 2), no JSON or extra formatting.
    """

    try:
        response = model.generate_content(prompt)
        print("Raw Gemini Response (Chat):", response.text)
        return jsonify({"response": response.text})
    except Exception as e:
        print("Error (Chat):", str(e))
        return jsonify({"response": "- Sorry, I couldn’t process that.\n- Try asking again!"}), 200
    
@app.route('/analyze-resume', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data.get('resume', '')

    if not resume_text:
        return jsonify({"error": "No resume text provided"}), 400

    prompt = f"""
    Analyze the following resume text: "{resume_text}".
    Provide a detailed summary with:
    - "skills": List 5-7 key skills identified (e.g., ["Python", "Project Management"]).
    - "strengths": List 3-5 strengths based on the resume (e.g., ["Strong coding skills"]).
    - "weaknesses": List 3-5 areas for improvement (e.g., ["Limited leadership experience"]).
    - "career_options": List 4 potential career paths with a fit score (0-100) and a brief reason (e.g., [{{"name": "Software Engineer", "fit": 85, "reason": "Strong programming skills"}}]).
    - "improvements": List 5 specific suggestions for resume enhancement (e.g., ["Add quantifiable achievements"]).
    - "experience_level": Estimate experience level ("Entry", "Mid", "Senior") with a confidence score (0-100).
    Return the response in valid JSON format:
    {{
      "skills": ["skill1", "skill2", ...],
      "strengths": ["strength1", "strength2", ...],
      "weaknesses": ["weakness1", "weakness2", ...],
      "career_options": [{{"name": "career1", "fit": score, "reason": "reason1"}}, ...],
      "improvements": ["suggestion1", "suggestion2", ...],
      "experience_level": {{"level": "level", "confidence": score}}
    }}
    Ensure the output is strictly valid JSON, with no extra text or markdown.
    """

    try:
        response = model.generate_content(prompt)
        raw_response = response.text
        print("Raw Gemini Response (Resume):", raw_response)

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            raise ValueError("No valid JSON object found in response")

        try:
            analysis = json.loads(json_str)
        except json.JSONDecodeError as e:
            json_str = json_str.replace("'", '"').strip()
            analysis = json.loads(json_str)

        return jsonify(analysis)

    except Exception as e:
        print("Error (Resume):", str(e))
        mock_analysis = {
            "skills": ["Communication", "Teamwork", "Problem Solving", "Time Management", "Adaptability"],
            "strengths": ["Good communication", "Team collaboration", "Quick learner"],
            "weaknesses": ["Limited technical skills", "No leadership roles", "Few projects listed"],
            "career_options": [
                {"name": "Project Manager", "fit": 70, "reason": "Strong teamwork skills"},
                {"name": "Customer Support", "fit": 65, "reason": "Effective communication"},
                {"name": "Sales Representative", "fit": 60, "reason": "Adaptability"},
                {"name": "Junior Analyst", "fit": 55, "reason": "Problem-solving ability"}
            ],
            "improvements": [
                "Add specific skills like programming languages.",
                "Include more work experience details.",
                "Use action verbs for impact.",
                "Quantify achievements (e.g., 'increased sales by 20%').",
                "Highlight any certifications."
            ],
            "experience_level": {"level": "Entry", "confidence": 80}
        }
        return jsonify(mock_analysis), 200
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
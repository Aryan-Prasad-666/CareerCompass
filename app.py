from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import json
import re
import os
import pickle
import numpy as np
import pandas as pd
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Load the RandomForestClassifier model
try:
    with open('weights.pkl', 'rb') as file:
        rf_model = pickle.load(file)
except FileNotFoundError:
    raise FileNotFoundError("weights.pkl not found. Ensure the model file is in the correct directory.")

# Define categorical mappings based on mldata.csv and training script
CERTIFICATIONS = {
    'app development': 0, 'distro making': 1, 'full stack': 2, 'hadoop': 3,
    'information security': 4, 'machine learning': 5, 'python': 6,
    'r programming': 7, 'shell programming': 8
}
WORKSHOPS = {
    'cloud computing': 0, 'data science': 1, 'database security': 2,
    'game development': 3, 'hacking': 4, 'system designing': 5,
    'testing': 6, 'web technologies': 7
}
INTERESTED_SUBJECTS = {
    'cloud computing': 0, 'Computer Architecture': 1, 'data engineering': 2,
    'hacking': 3, 'IOT': 4, 'Management': 5, 'networks': 6,
    'parallel computing': 7, 'programming': 8, 'Software Engineering': 9
}
CAREER_AREA = {
    'Business process analyst': 0, 'cloud computing': 1, 'developer': 2,
    'security': 3, 'system developer': 4, 'testing': 5
}
COMPANY_TYPE = {
    'BPA': 0, 'Cloud Services': 1, 'Finance': 2, 'product development': 3,
    'Product based': 4, 'SAaS services': 5, 'Sales and Marketing': 6,
    'Service Based': 7, 'Testing and Maintainance Services': 8, 'Web Services': 9
}
BOOKS = {
    'Action and Adventure': 0, 'Anthology': 1, 'Art': 2, 'Autobiographies': 3,
    'Biographies': 4, 'Childrens': 5, 'Comics': 6, 'Cookbooks': 7, 'Diaries': 8,
    'Dictionaries': 9, 'Drama': 10, 'Encyclopedias': 11, 'Fantasy': 12, 'Guide': 13,
    'Health': 14, 'History': 15, 'Horror': 16, 'Journals': 17, 'Math': 18,
    'Mystery': 19, 'Poetry': 20, 'Prayer books': 21, 'Religion-Spirituality': 22,
    'Romance': 23, 'Satire': 24, 'Science': 25, 'Science fiction': 26, 'Self help': 27,
    'Series': 28, 'Travel': 29, 'Trilogy': 30
}
BINARY = {'yes': 1, 'no': 0}
SKILLS = {'poor': 0, 'medium': 1, 'excellent': 2}
MANAGEMENT_TECHNICAL = {'Management': 'Management', 'Technical': 'Technical'}
WORKER_TYPE = {'hard worker': 'hard worker', 'smart worker': 'smart worker'}

# Define feature names expected by the model
FEATURE_NAMES = [
    'Logical quotient rating', 'coding skills rating', 'hackathons', 'public speaking points',
    'self-learning capability?', 'Extra-courses did', 'Taken inputs from seniors or elders',
    'worked in teams ever?', 'Introvert', 'reading and writing skills', 'memory capability score',
    'B_hard worker', 'B_smart worker', 'A_Management', 'A_Technical', 'Interested subjects_code',
    'Interested Type of Books_code', 'certifications_code', 'workshops_code',
    'Type of company want to settle in?_code', 'interested career area _code'
]

# Template Routes
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap.html')

@app.route('/resume-analyzer')
def resume_analyzer():
    return render_template('resume_analyzer.html')

@app.route('/progress-tracker')
def progress_tracker():
    return render_template('progress_tracker.html')

@app.route('/resume-comparison')
def resume_comparison():
    return render_template('resume_comparison.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/career-prediction')
def career_prediction():
    return render_template('careerprediction.html')

# API Endpoints
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
        print("Raw Gemini Response:", raw_response)

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
        print("Error:", str(e))
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

progress_history = []

@app.route('/track-progress', methods=['POST'])
def track_progress():
    data = request.get_json()
    achievements = data.get('achievements', '')

    if not achievements:
        return jsonify({"error": "No achievements provided"}), 400

    prompt = f"""
    Analyze the following weekly achievements: "{achievements}".
    Provide:
    - "progress_score": A score (0-100) reflecting the quality and impact of the achievements.
    - "suggestions": List 3-5 specific, actionable suggestions to improve next week's progress (e.g., ["Focus on advanced Python topics"]).
    - "week": The current week number (infer from context or increment from previous entries).
    Return the response in valid JSON format:
    {{
      "progress_score": score,
      "suggestions": ["suggestion1", "suggestion2", ...],
      "week": number
    }}
    Ensure the output is strictly valid JSON, with no extra text or markdown.
    """

    try:
        response = model.generate_content(prompt)
        raw_response = response.text
        print("Raw Gemini Response (Progress):", raw_response)

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            raise ValueError("No valid JSON object found in response")

        try:
            progress_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            json_str = json_str.replace("'", '"').strip()
            progress_data = json.loads(json_str)

        # Add week number if not provided by Gemini (simple increment)
        if "week" not in progress_data or not isinstance(progress_data["week"], int):
            progress_data["week"] = len(progress_history) + 1

        # Store progress in memory
        progress_history.append({
            "week": progress_data["week"],
            "score": progress_data["progress_score"]
        })

        # Return current progress and suggestions, plus full history
        return jsonify({
            "current": progress_data,
            "history": progress_history
        })

    except Exception as e:
        print("Error (Progress):", str(e))
        mock_progress = {
            "progress_score": 50,
            "suggestions": [
                "Try completing a small project this week.",
                "Focus on a new skill like time management.",
                "Review your achievements for clarity."
            ],
            "week": len(progress_history) + 1
        }
        progress_history.append({
            "week": mock_progress["week"],
            "score": mock_progress["progress_score"]
        })
        return jsonify({
            "current": mock_progress,
            "history": progress_history
        }), 200

@app.route('/compare-resumes', methods=['POST'])
def compare_resumes():
    data = request.get_json()
    user_resume = data.get('user_resume', '')
    peer_resume = data.get('peer_resume', '')

    if not user_resume or not peer_resume:
        return jsonify({"error": "Both user and peer resumes are required"}), 400

    prompt = f"""
    Compare the following two resumes:
    - User Resume: "{user_resume}"
    - Peer Resume: "{peer_resume}"

    Provide:
    - "skill_comparison": Object comparing key skills with estimated scores (0-100) for both (e.g., {{"Python": {{"user": 85, "peer": 70}}}}).
    - "experience_comparison": Object with experience levels ("Entry", "Mid", "Senior") and confidence scores (0-100) for both (e.g., {{"user": {{"level": "Mid", "confidence": 85}}, "peer": {{"level": "Entry", "confidence": 90}}}}).
    - "insights": List of 3-5 actionable insights based on the comparison (e.g., ["User has stronger technical skills than peer."]).

    Return the response in valid JSON format:
    {{
      "skill_comparison": {{"skill1": {{"user": score, "peer": score}}, ...}},
      "experience_comparison": {{"user": {{"level": "level", "confidence": score}}, "peer": {{"level": "level", "confidence": score}}}},
      "insights": ["insight1", "insight2", ...]
    }}
    Ensure the output is strictly valid JSON, with no extra text or markdown.
    """

    try:
        response = model.generate_content(prompt)
        raw_response = response.text
        print("Raw Gemini Response (Resume Comparison):", raw_response)

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            raise ValueError("No valid JSON object found in response")

        try:
            comparison_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            json_str = json_str.replace("'", '"').strip()
            comparison_data = json.loads(json_str)

        return jsonify(comparison_data)

    except Exception as e:
        print("Error (Resume Comparison):", str(e))
        mock_comparison = {
            "skill_comparison": {
                "Python": {"user": 85, "peer": 70},
                "Java": {"user": 70, "peer": 80},
                "Teamwork": {"user": 90, "peer": 85}
            },
            "experience_comparison": {
                "user": {"level": "Mid", "confidence": 85},
                "peer": {"level": "Entry", "confidence": 90}
            },
            "insights": [
                "User has stronger Python skills than peer.",
                "Peer excels in Java—consider learning from them.",
                "User’s experience is more advanced than peer’s."
            ]
        }
        return jsonify(mock_comparison), 200

@app.route('/predict-career', methods=['POST'])
def predict_career():
    try:
        data = request.get_json()
        
        # Extract and validate features
        features = {
            'Logical quotient rating': int(data.get('logical_quotient_rating', 0)),
            'coding skills rating': int(data.get('coding_skills_rating', 0)),
            'hackathons': int(data.get('hackathons', 0)),
            'public speaking points': int(data.get('public_speaking_points', 0)),
            'self-learning capability?': BINARY.get(data.get('self_learning_capability', 'no')),
            'Extra-courses did': BINARY.get(data.get('extra_courses_did', 'no')),
            'Taken inputs from seniors or elders': BINARY.get(data.get('taken_inputs_seniors_elders', 'no')),
            'worked in teams ever?': BINARY.get(data.get('worked_in_teams', 'no')),
            'Introvert': BINARY.get(data.get('introvert', 'no')),
            'reading and writing skills': SKILLS.get(data.get('reading_writing_skills', 'poor')),
            'memory capability score': SKILLS.get(data.get('memory_capability_score', 'poor')),
            'certifications_code': CERTIFICATIONS.get(data.get('certifications', 'app development')),
            'workshops_code': WORKSHOPS.get(data.get('workshops', 'cloud computing')),
            'Interested subjects_code': INTERESTED_SUBJECTS.get(data.get('interested_subjects', 'cloud computing')),
            'interested career area _code': CAREER_AREA.get(data.get('interested_career_area', 'Business process analyst')),
            'Type of company want to settle in?_code': COMPANY_TYPE.get(data.get('company_type', 'BPA')),
            'Interested Type of Books_code': BOOKS.get(data.get('interested_books', 'Action and Adventure')),
            'B_hard worker': 1 if data.get('worker_type', 'hard worker') == 'hard worker' else 0,
            'B_smart worker': 1 if data.get('worker_type', 'hard worker') == 'smart worker' else 0,
            'A_Management': 1 if data.get('management_technical', 'Management') == 'Management' else 0,
            'A_Technical': 1 if data.get('management_technical', 'Management') == 'Technical' else 0
        }
        
        # Convert to pandas DataFrame with feature names
        input_df = pd.DataFrame([features], columns=FEATURE_NAMES)
        
        # Predict
        prediction = rf_model.predict(input_df)[0]
        probabilities = rf_model.predict_proba(input_df)[0]
        max_prob = np.max(probabilities)
        
        # Get class names from the model
        classes = rf_model.classes_
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        
        return jsonify({
            "career": str(prediction),
            "confidence": float(max_prob),
            "probabilities": prob_dict,
            "recommendations": [
                "Build a portfolio showcasing relevant projects.",
                "Network with professionals in your predicted career field.",
                "Enroll in a course to strengthen key skills.",
                "Seek mentorship from experienced individuals.",
                "Stay updated with industry trends."
            ]
        })
    except Exception as e:
        print("Error (Career Prediction):", str(e))
        return jsonify({
            "career": "Software Engineer",
            "confidence": 0.85,
            "probabilities": {"Software Engineer": 0.85, "Data Analyst": 0.10, "Project Manager": 0.05},
            "recommendations": [
                "Build a portfolio showcasing relevant projects.",
                "Network with professionals in your predicted career field.",
                "Enroll in a course to strengthen key skills.",
                "Seek mentorship from experienced individuals.",
                "Stay updated with industry trends."
            ]
        }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
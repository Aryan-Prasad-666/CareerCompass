# Career Development Assistant📃

CareerCompass is an AI-powered platform that generates personalized career roadmaps with interactive timelines, offers peer resume comparison, creates tailored resumes, analyzes resume effectiveness, and provides progress tracking and AI mentorship to guide users toward their dream careers.

This website is launched at: https://careercompass.pythonanywhere.com/ 

## Tech Stack Used
- Python
- Flask
- Html
- Css
- Javascript
- Gemini API

## Description

CareerCompass is an AI-powered platform that generates personalized career roadmaps with interactive timelines, offers peer resume comparison, creates tailored resumes, analyzes resume effectiveness, and provides progress tracking and AI mentorship to guide users toward their dream careers.

## Homepage:
![screencapture-careercompass-pythonanywhere-2025-04-12-08_17_53](https://github.com/user-attachments/assets/2848b11d-c561-43bf-8923-b5e98090d887)

## Features

- **Career Roadmap Generator**: Creates personalized career development paths based on user goals and current skills
  
  ![screencapture-careercompass-pythonanywhere-roadmap-2025-04-12-08_21_51](https://github.com/user-attachments/assets/2eba9b07-dcdb-4244-9070-97194590462c)

- **Resume Analyzer**: Evaluates resumes and provides detailed feedback and suggestions

  ![screencapture-careercompass-pythonanywhere-resume-analyzer-2025-04-12-09_07_44](https://github.com/user-attachments/assets/182456db-6b56-4905-8840-799ed6c21953)

- **Progress Tracker**: Monitors and scores weekly career development achievements

  ![screencapture-careercompass-pythonanywhere-progress-tracker-2025-04-12-09_15_28](https://github.com/user-attachments/assets/36bbd0f1-f334-4231-9fd5-471d665f9e50)

- **Resume Comparison**: Compares two resumes and provides detailed insights

  ![screencapture-careercompass-pythonanywhere-resume-comparison-2025-04-12-09_17_09](https://github.com/user-attachments/assets/e942fd25-9648-4c48-b7d3-7fd35a0d710e)

- **Career Chatbot**: Offers personalized career guidance and advice

  ![screencapture-careercompass-pythonanywhere-chatbot-2025-04-12-09_20_33](https://github.com/user-attachments/assets/d4c56d7a-47e6-4561-95fd-3a3d4e863fb3)

- **Resume Builder**: Users can select a template and create resume easily by filling simple forms
  Repository Link for Resume Builder: https://github.com/Aryan-Prasad-666/CareerCompassResume.git

  ![screencapture-careercompassresume-pythonanywhere-2025-04-12-09_24_19](https://github.com/user-attachments/assets/d8a7004c-b090-4416-b74a-e3eb339ddf68)

  ![sample](https://github.com/user-attachments/assets/eab5d469-50ce-4b18-9769-9aeb43e90e3a)

- **Interactive Web Interface**: Clean and user-friendly frontend for all features

## Prerequisites

- Python 3.7+
- Flask
- Google Generative AI library
- Flask-CORS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aryan-Prasad-666/CareerCompass.git
cd CareerCompass
```

2. Install required dependencies:
```bash
pip install flask flask-cors google-generativeai
```

3. Set up your Google Gemini API key:
   - Replace `GEMINI_API_KEY` in `app.py` with your actual API key
   - For production, use environment variables instead of hardcoding

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

## API Endpoints

### Career Roadmap Generator
- **Endpoint**: `/generate-roadmap`
- **Method**: POST
- **Payload**:
```json
{
    "name": "string",
    "careerGoal": "string",
    "currentSkills": "string",
    "experience": "string",
    "interests": "string"
}
```

### Resume Analyzer
- **Endpoint**: `/analyze-resume`
- **Method**: POST
- **Payload**:
```json
{
    "resume": "string"
}
```

### Progress Tracker
- **Endpoint**: `/track-progress`
- **Method**: POST
- **Payload**:
```json
{
    "achievements": "string"
}
```

### Resume Comparison
- **Endpoint**: `/compare-resumes`
- **Method**: POST
- **Payload**:
```json
{
    "user_resume": "string",
    "peer_resume": "string"
}
```

### Career Chatbot
- **Endpoint**: `/chat`
- **Method**: POST
- **Payload**:
```json
{
    "query": "string"
}
```

## Frontend Routes

- `/`: Homepage
- `/roadmap`: Career roadmap generator interface
- `/resume-analyzer`: Resume analysis tool
- `/progress-tracker`: Progress tracking dashboard
- `/resume-comparison`: Resume comparison tool
- `/chatbot`: Career guidance chatbot interface

## Error Handling

The application includes comprehensive error handling:
- Validates input data
- Provides fallback responses if AI service fails
- Returns appropriate HTTP status codes
- Includes detailed error messages for debugging

## Security Considerations

- Implements CORS for cross-origin requests
- API key should be stored securely in production
- Input validation on all endpoints
- Error messages are sanitized in production

## Development

The application runs in debug mode by default on port 5000. For production:
- Disable debug mode
- Use environment variables for sensitive data
- Implement proper logging
- Add rate limiting
- Set up proper CORS policies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license here]

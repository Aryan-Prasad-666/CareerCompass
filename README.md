# Career Development Assistant📃

A comprehensive Flask-based web application that leverages Google's Gemini AI to provide career development tools and guidance.

## Features

- **Career Roadmap Generator**: Creates personalized career development paths based on user goals and current skills
- **Resume Analyzer**: Evaluates resumes and provides detailed feedback and suggestions
- **Progress Tracker**: Monitors and scores weekly career development achievements
- **Resume Comparison**: Compares two resumes and provides detailed insights
- **Career Chatbot**: Offers personalized career guidance and advice
- **Interactive Web Interface**: Clean and user-friendly frontend for all features

## Prerequisites

- Python 3.7+
- Flask
- Google Generative AI library
- Flask-CORS

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
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

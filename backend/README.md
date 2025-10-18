# 🧠 Math Explanation Backend

A Flask-based backend that uses **Gemini API**, **Eleven Labs**, and **Manim** to generate comprehensive math explanations with audio narration and animated videos.

## 🚀 Features

- **Problem Understanding**: Analyzes math problems using Gemini 2.0 Flash
- **Step-by-Step Solutions**: Generates detailed solution explanations
- **Audio Narration**: Creates engaging voice-over using Eleven Labs
- **Animated Videos**: Produces synchronized math animations with Manim
- **PDF Support**: Extracts and solves problems from uploaded PDF worksheets

## 📋 Prerequisites

- Python 3.9 or higher
- FFmpeg (for video/audio processing)
- Manim dependencies (LaTeX, etc.)
- API keys for:
  - Google Gemini API
  - Eleven Labs API

## 🔧 Installation

### 1. Clone and Navigate

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies

#### macOS
```bash
brew install ffmpeg
brew install --cask mactex-no-gui  # For LaTeX (required by Manim)
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg texlive texlive-latex-extra
```

#### Windows
- Install [FFmpeg](https://ffmpeg.org/download.html)
- Install [MiKTeX](https://miktex.org/download) for LaTeX

### 5. Configure Environment

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
GEMINI_API_KEY=your-gemini-api-key
ELEVEN_LABS_API_KEY=your-elevenlabs-api-key
```

## 🎯 Usage

### Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### 1. Solve Text Problem

**POST** `/api/solve_text`

```bash
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Solve the equation: 2x + 5 = 13",
    "generate_audio": true,
    "generate_video": true
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Problem solved successfully",
  "data": {
    "problem": "Solve the equation: 2x + 5 = 13",
    "solution": "Step-by-step solution...",
    "teaching_script": "Teaching narration script...",
    "audio": {
      "url": "/static/audio/narration_xxx.mp3",
      "filename": "narration_xxx.mp3"
    },
    "video": {
      "url": "/static/videos/explanation_xxx.mp4",
      "filename": "explanation_xxx.mp4"
    }
  }
}
```

#### 2. Solve PDF Problem

**POST** `/api/solve_pdf`

```bash
curl -X POST http://localhost:5000/api/solve_pdf \
  -F "file=@worksheet.pdf" \
  -F "generate_audio=true" \
  -F "generate_video=true"
```

#### 3. Health Check

**GET** `/health`

```bash
curl http://localhost:5000/health
```

#### 4. Service Status

**GET** `/status`

```bash
curl http://localhost:5000/status
```

## 📁 Project Structure

```
backend/
├── app.py                  # Flask application entry point
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
│
├── routes/                # API endpoints
│   ├── __init__.py
│   ├── solve_text.py      # Text problem endpoint
│   └── solve_pdf.py       # PDF upload endpoint
│
├── services/              # Core business logic
│   ├── __init__.py
│   ├── orchestrator.py    # Gemini orchestration
│   ├── audio_generator.py # Eleven Labs integration
│   ├── video_generator.py # Manim video creation
│   └── file_storage.py    # File management
│
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── prompts.py         # LLM prompt templates
│   └── helpers.py         # Helper functions
│
└── static/                # Generated files
    ├── audio/             # Audio narrations
    ├── videos/            # Animated videos
    └── uploads/           # Uploaded PDFs
```

## ⚙️ Configuration

Configure the application via environment variables in `.env`:

### Flask Settings
- `SECRET_KEY`: Flask secret key
- `DEBUG`: Debug mode (True/False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

### API Keys
- `GEMINI_API_KEY`: Your Google Gemini API key
- `ELEVEN_LABS_API_KEY`: Your Eleven Labs API key

### Gemini Settings
- `GEMINI_MODEL`: Model name (default: gemini-2.0-flash-exp)
- `GEMINI_TEMPERATURE`: Generation temperature (0.0-1.0)
- `GEMINI_MAX_TOKENS`: Maximum output tokens

### Eleven Labs Settings
- `ELEVEN_LABS_VOICE_ID`: Voice ID to use
- `ELEVEN_LABS_MODEL`: TTS model
- `VOICE_STABILITY`: Voice stability (0.0-1.0)
- `VOICE_SIMILARITY_BOOST`: Similarity boost (0.0-1.0)

### Manim Settings
- `MANIM_QUALITY`: Video quality (low_quality, medium_quality, high_quality)
- `MANIM_FPS`: Frames per second
- `MANIM_RESOLUTION`: Video resolution

## 🧪 Testing

Test the endpoints using the provided examples:

```bash
# Test text endpoint
python -c "
import requests
response = requests.post('http://localhost:5000/api/solve_text', json={
    'problem': 'What is the derivative of x^2?',
    'generate_audio': False,
    'generate_video': False
})
print(response.json())
"
```

## 🔍 Logging

Logs are output to the console with the following format:
```
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
```

Log levels:
- `INFO`: Normal operation messages
- `WARNING`: Warning messages
- `ERROR`: Error messages with stack traces

## 🛠️ Troubleshooting

### Common Issues

#### 1. Manim Installation Errors
```bash
# Ensure LaTeX is installed
which latex

# Reinstall Manim
pip uninstall manim
pip install manim
```

#### 2. FFmpeg Not Found
```bash
# Verify FFmpeg installation
ffmpeg -version

# Add FFmpeg to PATH if needed
export PATH="/usr/local/bin:$PATH"
```

#### 3. API Key Errors
- Verify API keys are set in `.env`
- Check API key permissions and quotas
- Ensure `.env` is in the backend directory

#### 4. File Permission Errors
```bash
# Ensure directories are writable
chmod -R 755 static/
```

## 🚀 Production Deployment

For production deployment:

1. **Set Production Environment Variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-strong-secret-key
   ```

2. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set Up Reverse Proxy** (nginx example)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Enable File Cleanup**
   ```env
   CLEANUP_OLD_FILES=True
   FILE_RETENTION_HOURS=24
   ```

## 📝 API Response Format

All endpoints return responses in the following format:

```json
{
  "success": true/false,
  "message": "Human-readable message",
  "timestamp": "ISO 8601 timestamp",
  "data": { /* Response data */ },
  "error": "Error message (if success=false)"
}
```

## 🤝 Contributing

This is a hackathon project. Feel free to extend and modify as needed!

## 📄 License

MIT License - feel free to use for your projects!

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Verify all dependencies are installed correctly
4. Ensure API keys are valid and have sufficient quota


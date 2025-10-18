# Backend - Manim Video Generator

Flask API backend that uses Gemini AI to generate Manim animation code and renders videos.

## Project Structure

```
backend/
├── app.py                 # Flask app initialization
├── settings.py            # Configuration and constants
├── api_routes.py          # API route handlers
├── gemini_service.py      # Gemini AI integration
├── manim_service.py       # Manim rendering logic
├── manim_code/            # Generated Manim scripts
├── manim_videos/          # Rendered videos
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install ffmpeg:
   - Windows: Download from https://ffmpeg.org/ and add to PATH
   - Or use: `choco install ffmpeg` (if you have Chocolatey)

3. Create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### POST `/api/generate`
Generate a video from a text prompt.

**Request Body:**
```json
{
  "prompt": "Create a circle that transforms into a square"
}
```

**Response:**
```json
{
  "success": true,
  "video_url": "/api/video/20251018_143022.mp4",
  "script_url": "/api/script/20251018_143022.py",
  "manim_code": "from manim import *\n..."
}
```

### GET `/api/video/<filename>`
Retrieve a generated video file.

### GET `/api/script/<filename>`
Retrieve a generated script file.

## Configuration

Modify settings in `settings.py`:
- `GEMINI_MODEL`: AI model to use
- `MANIM_QUALITY`: Video quality (`ql`, `qm`, `qh`)
- `PORT`: Server port

## Architecture

- **app.py**: Flask application setup and initialization
- **api_routes.py**: Handle HTTP requests and responses
- **gemini_service.py**: AI code generation logic
- **manim_service.py**: Video rendering and file management
- **settings.py**: Centralized configuration

Manim automatically uses ffmpeg for video rendering.

# Backend - Manim Video Generator

Flask API backend that uses Gemini AI to generate Manim animation code and renders videos.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install ffmpeg:
   - Windows: Download from https://ffmpeg.org/ and add to PATH
   - Or use: `choco install ffmpeg` (if you have Chocolatey)

3. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

## Running the Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## API Endpoints

### POST `/api/generate-video`
Generates a Manim animation video with synchronized AI narration (parallel processing).
```json
{
  "prompt": "Explain the Pythagorean theorem with a visual proof"
}
```

**Response:**
```json
{
  "success": true,
  "video_url": "/api/manim-video/20251018_143022.mp4",
  "audio_url": "/api/elevenlabs-audio/audio_20251018_143022.mp3",
  "manim_code": "from manim import *\n...",
  "script_text": "The Pythagorean theorem states..."
}
```

### POST `/api/generate-narration`
Generates standalone narration script and audio (without video).
```json
{
  "prompt": "Explain how AI works"
}
```

### GET `/api/manim-video/<filename>`
### GET `/api/manim-code/<filename>`
### GET `/api/elevenlabs-script/<filename>`
### GET `/api/elevenlabs-audio/<filename>`

## Configuration

Modify settings in `settings.py`:
- `GEMINI_MODEL`: AI model to use
- `MANIM_QUALITY`: Video quality (`ql`, `qm`, `qh`)
- `PORT`: Server port

Manim automatically uses ffmpeg for video rendering.

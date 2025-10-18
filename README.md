# hack-tx-25

AI-powered Manim video generator with a React frontend and Flask backend.


## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg (required by Manim):
   - Windows: `choco install ffmpeg` or download from https://ffmpeg.org/
   - Add to PATH if necessary

4. Create a `.env` file in the backend directory:
```
GEMINI_API_KEY=your_api_key_here
```

5. Start the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. Make sure both backend and frontend servers are running
2. Open `http://localhost:3000` in your browser
3. Enter a topic (e.g., "math", "physics", "shapes")
4. Describe the animation you want in the prompt field
5. Click "Generate Video"
6. Wait for the video to be generated and rendered
7. View the video and optionally inspect the generated Manim code

## API Endpoints

- `POST /api/generate` - Generate a video from a prompt
- `GET /api/video/<filename>` - Serve video files
- `GET /api/script/<filename>` - Serve script files
- `GET /api/health` - Health check endpoint

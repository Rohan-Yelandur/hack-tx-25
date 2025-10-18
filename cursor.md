# 🧠 Math Explanation Backend (Flask + Gemini + ElevenLabs + Manim)

This project is a **Flask-based backend** that uses the **Gemini API** to orchestrate a multi-step LLM pipeline for generating **math explanations**.  
Given either a **text problem** or a **PDF worksheet**, the system produces:
- 🧾 Step-by-step text solutions  
- 🎙️ Audio narration via Eleven Labs  
- 🎬 Animated math videos via Manim, synced to the narration  

---

## 🚀 Overview

### Core Idea
The backend acts as an **AI orchestrator**:
1. **Understands** math problems or worksheets.
2. **Solves** them while identifying key concepts.
3. **Writes a teaching script** explaining the solution.
4. **Generates narration audio** using Eleven Labs.
5. **Creates animated video explanations** in Manim, synced with the audio.

---

## 🧩 Architecture

### Key Components

| Component | Description |
|------------|-------------|
| **Gemini Orchestrator** | Core LLM that analyzes the input, extracts key ideas, generates solutions, and coordinates audio/video generation. |
| **Eleven Labs API** | Generates realistic audio narration from the LLM script and provides character-to-timestamp mappings for sync. |
| **Manim** | Python-based animation engine that visualizes equations, graphs, and steps to match the narration. |
| **Flask Server** | Exposes API endpoints for input (text/PDF), triggers the pipeline, and serves the final outputs. |

---

## ⚙️ Pipeline Flow

1. **Input Handling**
   - If text → Directly parsed by the LLM orchestrator.
   - If PDF → Extracted into text using OCR or Gemini’s multimodal understanding.

2. **Concept & Solution Generation**
   - Gemini identifies core math topics, reasoning steps, and the final answer.

3. **Script Generation**
   - LLM creates a natural-language explanation script (“Let’s start by…”).

4. **Audio Generation**
   - The script is passed to Eleven Labs → returns `.mp3` + timestamp JSON.

5. **Video Generation**
   - The Manim generator uses the timestamps + script to render synchronized animations.

6. **Output Packaging**
   - Video and audio are merged and served as downloadable URLs.
   - Text solutions and transcripts are returned in JSON.

---

## 📁 File Structure

backend/
│
├── app.py # Flask entry point
├── config.py # API keys, environment variables
│
├── routes/
│ ├── init.py
│ ├── solve_text.py # /solve_text endpoint
│ ├── solve_pdf.py # /solve_pdf endpoint
│
├── services/
│ ├── orchestrator.py # Gemini orchestration logic
│ ├── pdf_parser.py # PDF → text extraction
│ ├── audio_generator.py # Eleven Labs API integration
│ ├── video_generator.py # Manim video creation
│ ├── file_storage.py # Local/Cloud file handling
│
├── utils/
│ ├── prompts.py # Prompt templates for LLM orchestration
│ ├── helpers.py # Common helper functions
│
├── static/
│ ├── videos/
│ └── audio/
│
└── requirements.txt

yaml
Copy code

---

## 🧭 API Endpoints

### `POST /solve_text`
**Description:** Solve a text-based math problem and generate its explanation.  
**Body Example:**
```json
{
  "problem": "Find the derivative of x^2 + 3x + 2"
}
Response Example:

json
Copy code
{
  "text_solution": "The derivative of x^2 + 3x + 2 is 2x + 3.",
  "video_url": "/static/videos/derivative_explainer.mp4",
  "audio_url": "/static/audio/derivative_explainer.mp3",
  "transcript": "Let’s start by differentiating each term...",
  "timestamps": [{ "char": 42, "time": 3.2 }]
}
POST /solve_pdf
Description: Upload a PDF worksheet and get video/audio explanations for all contained problems.
Form Data Example:

makefile
Copy code
file: worksheet.pdf
Response Example:

json
Copy code
{
  "solutions": [
    {
      "problem": "Integrate x^2 dx",
      "text_solution": "The integral of x^2 dx is (x^3)/3 + C.",
      "video_url": "/static/videos/integral_explainer.mp4",
      "audio_url": "/static/audio/integral_explainer.mp3"
    }
  ]
}
🧰 API Integrations
Gemini API
Used as the orchestrator for reasoning, solution generation, and tool calling:

generate_script(problem_text)

generate_audio(script)

generate_video(script, timestamps)

Eleven Labs
Used for text-to-speech and timestamp extraction:

Endpoint: /v1/text-to-speech

Features:

Realistic voices

character_to_timestamps for precise video sync

Manim
Used for Python-based video animation:

Dynamically generated scenes from LLM output.

Compiles to .mp4 stored in /static/videos.

🧱 Design Goals
Modular structure: Each service (audio, video, LLM) is isolated and easily replaceable.

LLM Tool-Oriented Design: Orchestrator uses clean tool-calling functions for modularity.

Frontend compatibility: API returns all URLs and metadata required for video players and captions.

Extensibility: Future integration with YouTube/TikTok uploaders or vector DBs for reusable concept videos.

💡 Future Enhancements
Add asynchronous job queue for video rendering (e.g., Celery + Redis).

Include frontend live progress tracking via WebSocket.

Expand to handle multi-question worksheets in parallel.

Cache generated explanations by problem hash for reuse.

🧩 Example Workflow
pgsql
Copy code
User → Flask API → Gemini Orchestrator
      ↳ Solve math problem
      ↳ Create script
      ↳ Eleven Labs → audio.mp3 + timestamps.json
      ↳ Manim → animation.mp4 synced with audio
      → Returns all URLs + transcript
🧪 Requirements
java
Copy code
Flask
google-generativeai
requests
manim
elevenlabs
PyMuPDF (for PDF parsing)
python-dotenv
🧠 Summary
This backend transforms static math problems into dynamic, multimodal explanations.
By combining Gemini’s reasoning, Eleven Labs’ narration, and Manim’s animations, it builds an AI tutor that teaches like Khan Academy — fully automated.
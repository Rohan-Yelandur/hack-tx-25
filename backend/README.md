# Backend - Manim Video Generator

This backend uses Gemini AI to generate Manim animation code and renders videos using ffmpeg.

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

## Usage

Run the main script:
```bash
python app.py
```

This will:
1. Ask Gemini to generate Manim code based on a prompt
2. Save the script to `manim_code/` with format: `<topic>_<timestamp>.py`
3. Render the video using Manim (which uses ffmpeg internally)
4. Save the video to `manim_videos/` with the same filename

## Customization

You can modify the `main()` function in `app.py` to:
- Change the prompt for different animations
- Change the topic for organizing videos by category
- Adjust video quality (change `-ql` to `-qh` for high quality)

## How it works

1. **generate_manim_code(prompt)**: Uses Gemini to create Python code for a Manim scene
2. **render_manim_video(code, topic)**: Saves the code to `manim_code/` and runs Manim to render it
3. Videos and scripts are saved with matching filenames in their respective folders

Manim automatically uses ffmpeg for video rendering, so no manual ffmpeg commands are needed.

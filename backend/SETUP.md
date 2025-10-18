# 🚀 Quick Setup Guide

This guide will get you up and running with the Math Explanation Backend in under 5 minutes.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.9+ installed
- [ ] pip package manager
- [ ] Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- [ ] Eleven Labs API key ([Get it here](https://elevenlabs.io/))
- [ ] FFmpeg installed (for video processing)
- [ ] LaTeX distribution installed (for Manim)

## Step-by-Step Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create and Activate Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask and Flask-CORS
- Google Generative AI (Gemini)
- Eleven Labs
- Manim
- Other utilities

### 4. Install System Dependencies

#### macOS (using Homebrew)

```bash
# Install FFmpeg
brew install ffmpeg

# Install LaTeX (required for Manim)
brew install --cask mactex-no-gui
```

#### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install FFmpeg
sudo apt-get install -y ffmpeg

# Install LaTeX
sudo apt-get install -y texlive texlive-latex-extra texlive-fonts-extra
```

#### Windows

1. **FFmpeg:**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extract and add to PATH

2. **LaTeX:**
   - Download and install [MiKTeX](https://miktex.org/download)

### 5. Configure Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key_here

# Optional: Customize these settings
DEBUG=True
PORT=5000
MANIM_QUALITY=medium_quality
```

### 6. Verify Installation

Test that everything is installed correctly:

```bash
# Test Python dependencies
python -c "import flask, google.generativeai, elevenlabs, manim; print('✅ All Python packages installed')"

# Test FFmpeg
ffmpeg -version

# Test LaTeX
latex --version
```

### 7. Start the Server

**Option A: Using Python directly**
```bash
python app.py
```

**Option B: Using the run script (macOS/Linux)**
```bash
chmod +x run.sh
./run.sh
```

The server will start at `http://localhost:5000`

### 8. Test the API

Open a new terminal and test:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test with a simple problem
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{"problem": "What is 2 + 2?", "generate_audio": false, "generate_video": false}'
```

Or use the example script:

```bash
python example_usage.py
```

## 🎉 You're Ready!

Your backend is now running and ready to generate math explanations!

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** Activate the virtual environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Issue: "GEMINI_API_KEY is not set"

**Solution:** Make sure `.env` file exists and contains your API key
```bash
cat .env  # Check if file exists
```

### Issue: "ffmpeg: command not found"

**Solution:** Install FFmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

### Issue: Manim rendering fails with LaTeX errors

**Solution:** Install complete LaTeX distribution
```bash
# macOS
brew install --cask mactex-no-gui

# Ubuntu
sudo apt-get install texlive-full
```

### Issue: "Port 5000 already in use"

**Solution:** Change the port in `.env`
```env
PORT=5001
```

### Issue: Video generation is too slow

**Solution:** Lower the video quality in `.env`
```env
MANIM_QUALITY=low_quality
```

## 📚 Next Steps

1. **Read the API Documentation:** See `API_REFERENCE.md`
2. **Explore Examples:** Run `python example_usage.py`
3. **Customize Prompts:** Edit `utils/prompts.py`
4. **Adjust Settings:** Modify `.env` configuration

## 🔗 Useful Links

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Eleven Labs API Documentation](https://docs.elevenlabs.io/)
- [Manim Documentation](https://docs.manim.community/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 💡 Tips

- **Faster Development:** Set `generate_video=false` for quicker testing
- **Cost Saving:** Videos use more API credits; test with audio-only first
- **Caching:** The system generates unique filenames; reuse problems get new files
- **Cleanup:** Run `/api/cleanup` endpoint to remove old files

## 🆘 Still Having Issues?

1. Check all prerequisites are installed
2. Verify API keys are valid
3. Check the server logs for detailed error messages
4. Ensure all directories have proper permissions
5. Try running with `DEBUG=True` for more verbose output

Happy coding! 🚀


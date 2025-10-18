# ⚡ Quick Start - 5 Minutes to Running

Get the Math Explanation Backend up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- pip
- [Gemini API Key](https://makersuite.google.com/app/apikey)
- [Eleven Labs API Key](https://elevenlabs.io/)

## Step 1: Navigate to Backend (30 seconds)

```bash
cd backend
```

## Step 2: Install Dependencies (2 minutes)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 3: Configure API Keys (1 minute)

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
GEMINI_API_KEY=your_gemini_key_here
ELEVEN_LABS_API_KEY=your_elevenlabs_key_here
```

## Step 4: Start Server (30 seconds)

```bash
python app.py
```

You should see:

```
====================================================
Math Explanation Backend Starting...
Host: 0.0.0.0
Port: 5000
Debug: True
====================================================
 * Running on http://0.0.0.0:5000
```

## Step 5: Test It! (1 minute)

Open a new terminal and test:

```bash
curl http://localhost:5000/health
```

You should see:

```json
{
  "success": true,
  "message": "Service is healthy",
  "data": {"status": "ok"}
}
```

### Test with a Problem

```bash
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{"problem": "What is 2 + 2?", "generate_audio": false, "generate_video": false}'
```

## 🎉 You're Done!

Your backend is running! Here's what to do next:

### Option 1: Use the Example Script

```bash
python example_usage.py
```

### Option 2: Try Full Pipeline

```bash
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Solve for x: 2x + 5 = 13",
    "generate_audio": true,
    "generate_video": false
  }'
```

### Option 3: Check Service Status

```bash
curl http://localhost:5000/status
```

## Common Issues

### 🔴 "GEMINI_API_KEY is not set"

→ Make sure you created `.env` and added your API key

### 🔴 "Command not found: python3"

→ Try `python` instead of `python3`

### 🔴 "Port 5000 already in use"

→ Change port in `.env`: `PORT=5001`

### 🔴 "Module 'flask' not found"

→ Activate virtual environment: `source venv/bin/activate`

## For Video Generation (Optional)

To enable video generation, install system dependencies:

**macOS:**
```bash
brew install ffmpeg
brew install --cask mactex-no-gui
```

**Ubuntu:**
```bash
sudo apt-get install ffmpeg texlive texlive-latex-extra
```

Then test with video:
```bash
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Area of circle with radius 5",
    "generate_audio": true,
    "generate_video": true
  }'
```

## Next Steps

1. **Read the Docs**: Check out `README.md` for full documentation
2. **API Reference**: See `API_REFERENCE.md` for all endpoints
3. **Architecture**: Read `ARCHITECTURE.md` to understand the system
4. **Examples**: Run `python example_usage.py` for more examples

## Quick Commands Reference

```bash
# Start server
python app.py

# Run examples
python example_usage.py

# Quick test
curl http://localhost:5000/health

# Solve a problem (text only)
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{"problem": "YOUR_PROBLEM_HERE", "generate_audio": false, "generate_video": false}'

# Check status
curl http://localhost:5000/status
```

## Development Tips

### Faster Testing
Disable video generation during development:
```json
{
  "problem": "your problem",
  "generate_audio": true,
  "generate_video": false  // Much faster!
}
```

### Debug Mode
Already enabled by default in `.env`:
```env
DEBUG=True
```

### View Logs
Logs appear in the terminal where you ran `python app.py`

## That's It!

You're ready to build awesome math explanation features! 🚀

**Questions?** Check the other documentation files:
- `README.md` - Full documentation
- `SETUP.md` - Detailed setup
- `API_REFERENCE.md` - API docs
- `ARCHITECTURE.md` - System design


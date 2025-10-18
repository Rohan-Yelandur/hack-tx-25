from google import genai
import os
from dotenv import load_dotenv
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

def generate_manim_code(prompt: str) -> str:
    """Generate Manim code using Gemini based on a prompt."""
    full_prompt = f"""
    Generate a simple Manim scene based on this description: {prompt}
    Requirements:
    - Create a class called GeneratedScene that inherits from Scene
    - Use simple Manim animations
    - Keep it short (3-5 seconds)
    - Only return the Python code, no explanations
    - Import necessary items from manim
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=full_prompt
    )
    
    return response.text.strip().replace("```python", "").replace("```", "").strip()


def render_manim_video(manim_code: str) -> tuple[str, str]:
    """Render a Manim video from Python code and return the video and script paths."""
    # Create output directories
    video_dir = Path(__file__).parent / "manim_videos"
    code_dir = Path(__file__).parent / "manim_code"
    video_dir.mkdir(exist_ok=True)
    code_dir.mkdir(exist_ok=True)
    
    # Generate filename with format: <timestamp>
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = timestamp
    
    # Save the Manim code to manim_code folder
    script_path = code_dir / f"{filename}.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(manim_code)
    
    try:
        # Run Manim to render the video
        cmd = [
            "manim",
            "-ql",  # Low quality for faster rendering
            "--format=mp4",
            f"--media_dir={video_dir}",
            str(script_path),
            "GeneratedScene"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return None, str(script_path)
        
        # Find the generated video file
        video_files = list(video_dir.glob("**/GeneratedScene.mp4"))
        if video_files:
            # Move to main manim_videos folder with matching name
            final_video_path = video_dir / f"{filename}.mp4"
            video_files[0].replace(final_video_path)
            return str(final_video_path), str(script_path)
        
        return None, str(script_path)
        
    except Exception as e:
        return None, str(script_path)


@app.route('/api/generate', methods=['POST'])
def generate_video():
    """API endpoint to generate a video from a prompt."""
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        manim_code = generate_manim_code(prompt)
        video_path, script_path = render_manim_video(manim_code)
        
        if video_path:
            video_filename = Path(video_path).name
            script_filename = Path(script_path).name
            
            return jsonify({
                'success': True,
                'video_url': f'/api/video/{video_filename}',
                'script_url': f'/api/script/{script_filename}',
                'manim_code': manim_code
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to render video',
                'script_url': f'/api/script/{Path(script_path).name}'
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/video/<filename>', methods=['GET'])
def get_video(filename):
    """Serve video files."""
    video_path = Path(__file__).parent / "manim_videos" / filename
    if video_path.exists():
        return send_file(video_path, mimetype='video/mp4')
    return jsonify({'error': 'Video not found'}), 404


@app.route('/api/script/<filename>', methods=['GET'])
def get_script(filename):
    """Serve script files."""
    script_path = Path(__file__).parent / "manim_code" / filename
    if script_path.exists():
        return send_file(script_path, mimetype='text/plain')
    return jsonify({'error': 'Script not found'}), 404


if __name__ == "__main__":
    app.run(port=5000)
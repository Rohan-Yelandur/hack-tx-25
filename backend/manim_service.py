import subprocess
import os
from pathlib import Path
from datetime import datetime
from settings import settings


class ManimService:
    """Service for rendering Manim videos."""
    
    def __init__(self):
        # Get the absolute path of the backend directory
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.video_dir = self.base_dir / settings.OUTPUT_DIR
        self.code_dir = self.base_dir / settings.CODE_DIR
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create output directories if they don't exist."""
        self.video_dir.mkdir(exist_ok=True)
        self.code_dir.mkdir(exist_ok=True)
    
    def _generate_filename(self) -> str:
        """Generate a timestamp-based filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return timestamp
    
    def _save_script(self, manim_code: str, filename: str) -> Path:
        """Save Manim code to a file."""
        script_path = self.code_dir / f"{filename}.py"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(manim_code)
        return script_path
    
    def _render_video(self, script_path: Path) -> bool:
        """Run Manim to render the video."""
        try:
            cmd = [
                "manim",
                f"-{settings.MANIM_QUALITY}",
                f"--format={settings.MANIM_FORMAT}",
                f"--media_dir={self.video_dir}",
                str(script_path),
                settings.SCENE_CLASS_NAME
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Manim render failed with return code {result.returncode}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
                
            return True
            
        except Exception as e:
            print(f"Manim render error: {str(e)}")
            return False
    
    def _move_video(self, filename: str) -> Path:
        """Find and move the generated video to the main videos folder."""
        video_files = list(self.video_dir.glob(f"**/{settings.SCENE_CLASS_NAME}.mp4"))
        if video_files:
            final_video_path = self.video_dir / f"{filename}.mp4"
            video_files[0].replace(final_video_path)
            return final_video_path
        return None
    
    def render_manim_video(self, manim_code: str):
        """Render a Manim video from Python code and return paths."""
        try:
            filename = self._generate_filename()
            script_path = self._save_script(manim_code, filename)
            
            if self._render_video(script_path):
                video_path = self._move_video(filename)
                if video_path:
                    return str(video_path), str(script_path)
                else:
                    print("Warning: Video file not found after successful render")
                    return None, str(script_path)
            else:
                print("Manim render failed - check error messages above")
                return None, str(script_path)
                
        except Exception as e:
            print(f"Manim service error: {str(e)}")
            return None, str(script_path) if 'script_path' in locals() else None
    
    def get_video_path(self, filename: str) -> Path:
        """Get the full path to a video file."""
        return self.video_dir / filename
    
    def get_script_path(self, filename: str) -> Path:
        """Get the full path to a script file."""
        return self.code_dir / filename


manim_service = ManimService()

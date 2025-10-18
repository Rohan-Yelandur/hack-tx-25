"""
Manim Video Generation Service.
Creates animated math explanation videos synchronized with audio narration.
"""

import os
import re
import logging
import subprocess
from typing import Dict, List, Optional
from textwrap import dedent
from config import Config
from utils.helpers import (
    sanitize_filename,
    ensure_file_extension,
    generate_file_id,
    extract_math_expressions,
    parse_scene_plan
)

logger = logging.getLogger(__name__)


class VideoGenerator:
    """
    Generates animated math videos using Manim.
    Creates Python scripts dynamically and renders them.
    """
    
    def __init__(self):
        """Initialize the video generator with configuration."""
        self.quality = Config.MANIM_QUALITY
        self.fps = Config.MANIM_FPS
        self.resolution = Config.MANIM_RESOLUTION
        
        logger.info(f"Initialized video generator with quality: {self.quality}")
    
    def generate_video(
        self,
        script: str,
        scene_plan: str,
        audio_path: Optional[str] = None,
        timestamps: Optional[List[Dict]] = None,
        output_filename: Optional[str] = None
    ) -> Dict:
        """
        Generate an animated video based on script and scene plan.
        
        Args:
            script: The teaching script
            scene_plan: Structured scene plan from orchestrator
            audio_path: Path to audio narration file
            timestamps: Word-level timestamps for synchronization
            output_filename: Optional custom filename
            
        Returns:
            Dictionary containing video path and metadata
            
        Raises:
            Exception: If video generation fails
        """
        logger.info("Generating video animation...")
        
        try:
            # Generate unique filename
            if not output_filename:
                file_id = generate_file_id(script)
                output_filename = f"explanation_{file_id}.mp4"
            
            output_filename = ensure_file_extension(output_filename, '.mp4')
            output_filename = sanitize_filename(output_filename)
            
            # Create Manim scene script
            manim_script = self._create_manim_script(
                script,
                scene_plan,
                timestamps
            )
            
            # Save the Manim script
            script_filename = output_filename.replace('.mp4', '.py')
            script_path = os.path.join(Config.VIDEO_FOLDER, script_filename)
            
            with open(script_path, 'w') as f:
                f.write(manim_script)
            
            logger.info(f"Created Manim script: {script_filename}")
            
            # Render the video
            video_path = self._render_manim_video(
                script_path,
                output_filename,
                audio_path
            )
            
            # Get file metadata
            file_size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
            
            result = {
                'video_path': video_path,
                'video_filename': output_filename,
                'script_path': script_path,
                'file_size': file_size,
                'audio_path': audio_path
            }
            
            logger.info(f"Video generated successfully: {output_filename}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating video: {str(e)}")
            raise Exception(f"Failed to generate video: {str(e)}")
    
    def _create_manim_script(
        self,
        script: str,
        scene_plan: str,
        timestamps: Optional[List[Dict]] = None
    ) -> str:
        """
        Create a Manim Python script from the teaching script and scene plan.
        
        Args:
            script: Teaching script
            scene_plan: Scene plan from orchestrator
            timestamps: Optional word timestamps
            
        Returns:
            Complete Manim Python script as string
        """
        # Extract math expressions from the script
        math_expressions = extract_math_expressions(script)
        
        # Parse scene plan into structured format
        scenes = parse_scene_plan(scene_plan)
        
        # Build the Manim script
        manim_code = dedent('''
        from manim import *
        
        class MathExplanation(Scene):
            def construct(self):
                # Configuration
                self.camera.background_color = "#1e1e1e"
                
                # Title
                title = Text("Math Explanation", font_size=48, color=BLUE)
                title.to_edge(UP)
                self.play(Write(title))
                self.wait(1)
                self.play(FadeOut(title))
                
        ''')
        
        # Add scenes based on the scene plan
        if math_expressions:
            manim_code += self._generate_equation_scenes(math_expressions)
        else:
            # Fallback: Create a generic explanation scene
            manim_code += self._generate_generic_scene(script)
        
        return manim_code
    
    def _generate_equation_scenes(self, expressions: List[str]) -> str:
        """
        Generate Manim code for displaying and animating equations.
        
        Args:
            expressions: List of LaTeX expressions
            
        Returns:
            Manim code as string
        """
        code = dedent('''
                # Display mathematical expressions
        ''')
        
        for i, expr in enumerate(expressions[:5]):  # Limit to 5 expressions
            # Clean the expression
            expr_clean = expr.strip().replace('"', '\\"')
            
            code += dedent(f'''
                # Expression {i + 1}
                equation_{i} = MathTex(r"{expr_clean}", font_size=36)
                equation_{i}.move_to(ORIGIN)
                self.play(Write(equation_{i}))
                self.wait(2)
                
            ''')
            
            # Add transformation to next equation if not the last one
            if i < len(expressions[:5]) - 1:
                code += dedent(f'''
                self.play(FadeOut(equation_{i}))
                
            ''')
        
        # Fade out the last equation
        last_idx = min(len(expressions) - 1, 4)
        code += dedent(f'''
                self.play(FadeOut(equation_{last_idx}))
                
        ''')
        
        return code
    
    def _generate_generic_scene(self, script: str) -> str:
        """
        Generate a generic Manim scene when no specific equations are found.
        
        Args:
            script: The teaching script
            
        Returns:
            Manim code as string
        """
        # Extract first few sentences for display
        sentences = script.split('.')[:3]
        
        code = dedent('''
                # General explanation
                explanation = VGroup()
                
        ''')
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                sentence_clean = sentence.strip()[:100]  # Limit length
                sentence_clean = sentence_clean.replace('"', '\\"').replace('$', '')
                
                code += dedent(f'''
                text_{i} = Text("{sentence_clean}...", font_size=24)
                text_{i}.move_to(ORIGIN + {i - 1}*DOWN)
                explanation.add(text_{i})
                
            ''')
        
        code += dedent('''
                self.play(Write(explanation))
                self.wait(3)
                self.play(FadeOut(explanation))
                
        ''')
        
        return code
    
    def _render_manim_video(
        self,
        script_path: str,
        output_filename: str,
        audio_path: Optional[str] = None
    ) -> str:
        """
        Render a Manim script to video.
        
        Args:
            script_path: Path to the Manim Python script
            output_filename: Desired output filename
            audio_path: Optional audio file to sync with
            
        Returns:
            Path to rendered video file
            
        Raises:
            Exception: If rendering fails
        """
        logger.info("Rendering Manim video...")
        
        try:
            # Build Manim command
            quality_flag = f"-{self.quality[0]}"  # -l, -m, or -h
            
            command = [
                'manim',
                quality_flag,
                script_path,
                'MathExplanation',
                '-o', output_filename
            ]
            
            # Run Manim
            result = subprocess.run(
                command,
                cwd=Config.VIDEO_FOLDER,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Manim stderr: {result.stderr}")
                raise Exception(f"Manim rendering failed: {result.stderr}")
            
            logger.info("Manim rendering completed")
            
            # Find the output video
            output_path = os.path.join(Config.VIDEO_FOLDER, 'media', 'videos', 
                                      os.path.basename(script_path).replace('.py', ''),
                                      self.quality, output_filename)
            
            # If audio is provided, merge it with the video
            if audio_path and os.path.exists(audio_path):
                output_path = self._merge_audio_video(output_path, audio_path)
            
            return output_path
            
        except subprocess.TimeoutExpired:
            logger.error("Manim rendering timed out")
            raise Exception("Video rendering timed out")
        except Exception as e:
            logger.error(f"Error rendering video: {str(e)}")
            raise
    
    def _merge_audio_video(self, video_path: str, audio_path: str) -> str:
        """
        Merge audio with video using ffmpeg.
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            
        Returns:
            Path to merged video file
            
        Raises:
            Exception: If merging fails
        """
        logger.info("Merging audio with video...")
        
        try:
            # Create output path
            output_path = video_path.replace('.mp4', '_with_audio.mp4')
            
            # Build ffmpeg command
            command = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                output_path,
                '-y'  # Overwrite output file
            ]
            
            # Run ffmpeg
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode != 0:
                logger.error(f"ffmpeg stderr: {result.stderr}")
                raise Exception(f"Audio merging failed: {result.stderr}")
            
            logger.info("Audio merged successfully")
            return output_path
            
        except Exception as e:
            logger.error(f"Error merging audio: {str(e)}")
            # Return original video if merging fails
            return video_path
    
    def validate_video_file(self, video_path: str) -> tuple:
        """
        Validate that a video file exists and is valid.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(video_path):
            return False, "Video file does not exist"
        
        if not os.path.isfile(video_path):
            return False, "Path is not a file"
        
        file_size = os.path.getsize(video_path)
        if file_size == 0:
            return False, "Video file is empty"
        
        if file_size < 10000:  # Less than 10KB is suspicious
            return False, "Video file is too small"
        
        return True, None


def get_video_generator() -> VideoGenerator:
    """
    Factory function to get a video generator instance.
    
    Returns:
        Configured VideoGenerator instance
    """
    return VideoGenerator()


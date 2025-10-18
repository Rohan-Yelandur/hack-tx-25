import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration settings."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Gemini Configuration
    GEMINI_MODEL = "gemini-2.5-flash"
    
    # Manim Configuration
    MANIM_QUALITY = "ql"  # Low quality for faster rendering
    MANIM_FORMAT = "mp4"
    SCENE_CLASS_NAME = "GeneratedScene"
    
    # File Paths
    OUTPUT_DIR = "manim_videos"
    CODE_DIR = "manim_code"
    
    # Server Configuration
    PORT = 5000
    DEBUG = False


settings = Settings()

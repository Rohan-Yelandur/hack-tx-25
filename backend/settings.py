import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration settings."""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    # Model Configs
    GEMINI_MODEL = "gemini-2.5-pro"
    ELEVENLABS_MODEL = "eleven_turbo_v2_5"

    # Manim Configuration
    MANIM_QUALITY = "ql"  # Low quality for faster rendering
    MANIM_FORMAT = "mp4"
    SCENE_CLASS_NAME = "GeneratedScene"
    
    # File Paths
    OUTPUT_DIR = "manim_videos"
    CODE_DIR = "manim_code"
    SCRIPTS_DIR = "elevenlabs_scripts"
    AUDIO_DIR = "elevenlabs_audio"
    
    # Server Configuration
    PORT = 5000
    DEBUG = False


settings = Settings()

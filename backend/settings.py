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
    GEMINI_MODEL = "gemini-2.5-flash"
    ELEVENLABS_MODEL = "eleven_turbo_v2_5"
    
    # ElevenLabs Voice Settings
    ELEVENLABS_STABILITY = 0.5      # 0.0-1.0: Voice stability
    ELEVENLABS_SIMILARITY = 0.75    # 0.0-1.0: Voice similarity
    ELEVENLABS_STYLE = 0.0          # 0.0-1.0: Style exaggeration
    ELEVENLABS_SPEED = 1.1          # 0.7-1.2: Speaking speed (1.0 = normal)

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

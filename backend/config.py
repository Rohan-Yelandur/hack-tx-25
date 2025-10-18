"""
Configuration module for the Math Explanation Backend.
Loads environment variables and provides centralized configuration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')
    
    # Gemini Configuration
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
    GEMINI_MAX_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', '8000'))
    
    # Eleven Labs Configuration
    ELEVEN_LABS_VOICE_ID = os.getenv('ELEVEN_LABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')  # Default: Rachel
    ELEVEN_LABS_MODEL = os.getenv('ELEVEN_LABS_MODEL', 'eleven_turbo_v2_5')
    ELEVEN_LABS_VOICE_SETTINGS = {
        'stability': float(os.getenv('VOICE_STABILITY', '0.5')),
        'similarity_boost': float(os.getenv('VOICE_SIMILARITY_BOOST', '0.75')),
        'style': float(os.getenv('VOICE_STYLE', '0.0')),
        'use_speaker_boost': os.getenv('USE_SPEAKER_BOOST', 'True').lower() == 'true'
    }
    
    # File Storage Configuration
    STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
    AUDIO_FOLDER = os.path.join(STATIC_FOLDER, 'audio')
    VIDEO_FOLDER = os.path.join(STATIC_FOLDER, 'videos')
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Manim Configuration
    MANIM_QUALITY = os.getenv('MANIM_QUALITY', 'medium_quality')  # low_quality, medium_quality, high_quality
    MANIM_FPS = int(os.getenv('MANIM_FPS', '30'))
    MANIM_RESOLUTION = os.getenv('MANIM_RESOLUTION', '1280x720')
    
    # Processing Configuration
    ASYNC_PROCESSING = os.getenv('ASYNC_PROCESSING', 'False').lower() == 'true'
    CLEANUP_OLD_FILES = os.getenv('CLEANUP_OLD_FILES', 'True').lower() == 'true'
    FILE_RETENTION_HOURS = int(os.getenv('FILE_RETENTION_HOURS', '24'))
    
    @staticmethod
    def validate():
        """Validate required configuration values."""
        errors = []
        
        if not Config.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set")
        
        if not Config.ELEVEN_LABS_API_KEY:
            errors.append("ELEVEN_LABS_API_KEY is not set")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist."""
        directories = [
            Config.STATIC_FOLDER,
            Config.AUDIO_FOLDER,
            Config.VIDEO_FOLDER,
            Config.UPLOAD_FOLDER
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


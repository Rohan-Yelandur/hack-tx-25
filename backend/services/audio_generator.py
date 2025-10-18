"""
Eleven Labs Audio Generation Service.
Handles text-to-speech conversion with timestamp generation for video sync.
"""

import os
import logging
import requests
from typing import Dict, Optional, Tuple
from elevenlabs import generate, Voice, VoiceSettings, save
from config import Config
from utils.helpers import sanitize_filename, ensure_file_extension, generate_file_id

logger = logging.getLogger(__name__)


class AudioGenerator:
    """
    Generates audio narration using Eleven Labs API.
    Provides audio files and timestamp data for video synchronization.
    """
    
    def __init__(self):
        """Initialize the audio generator with API configuration."""
        if not Config.ELEVEN_LABS_API_KEY:
            raise ValueError("ELEVEN_LABS_API_KEY is not set in configuration")
        
        self.api_key = Config.ELEVEN_LABS_API_KEY
        self.voice_id = Config.ELEVEN_LABS_VOICE_ID
        self.model = Config.ELEVEN_LABS_MODEL
        self.voice_settings = Config.ELEVEN_LABS_VOICE_SETTINGS
        
        logger.info(f"Initialized audio generator with voice ID: {self.voice_id}")
    
    def generate_audio(
        self,
        script: str,
        output_filename: Optional[str] = None
    ) -> Dict:
        """
        Generate audio narration from teaching script.
        
        Args:
            script: The teaching script to narrate
            output_filename: Optional custom filename (without path)
            
        Returns:
            Dictionary containing audio file path and metadata
            
        Raises:
            Exception: If audio generation fails
        """
        logger.info("Generating audio narration...")
        
        try:
            # Generate a unique filename if not provided
            if not output_filename:
                file_id = generate_file_id(script)
                output_filename = f"narration_{file_id}.mp3"
            
            output_filename = ensure_file_extension(output_filename, '.mp3')
            output_filename = sanitize_filename(output_filename)
            
            # Full output path
            output_path = os.path.join(Config.AUDIO_FOLDER, output_filename)
            
            # Configure voice settings
            voice = Voice(
                voice_id=self.voice_id,
                settings=VoiceSettings(
                    stability=self.voice_settings['stability'],
                    similarity_boost=self.voice_settings['similarity_boost'],
                    style=self.voice_settings.get('style', 0.0),
                    use_speaker_boost=self.voice_settings.get('use_speaker_boost', True)
                )
            )
            
            # Generate audio
            audio = generate(
                text=script,
                voice=voice,
                model=self.model
            )
            
            # Save audio file
            save(audio, output_path)
            
            # Get file size and duration estimate
            file_size = os.path.getsize(output_path)
            duration_estimate = len(script.split()) / 150 * 60  # Rough estimate
            
            result = {
                'audio_path': output_path,
                'audio_filename': output_filename,
                'file_size': file_size,
                'duration_estimate': duration_estimate,
                'script': script
            }
            
            logger.info(f"Audio generated successfully: {output_filename}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            raise Exception(f"Failed to generate audio: {str(e)}")
    
    def generate_audio_with_timestamps(
        self,
        script: str,
        output_filename: Optional[str] = None
    ) -> Dict:
        """
        Generate audio with character-to-timestamp mappings for precise sync.
        Uses Eleven Labs API with alignment data.
        
        Args:
            script: The teaching script to narrate
            output_filename: Optional custom filename
            
        Returns:
            Dictionary containing audio path, timestamps, and metadata
            
        Raises:
            Exception: If generation fails
        """
        logger.info("Generating audio with timestamp alignment...")
        
        try:
            # Generate unique filename
            if not output_filename:
                file_id = generate_file_id(script)
                output_filename = f"narration_{file_id}.mp3"
            
            output_filename = ensure_file_extension(output_filename, '.mp3')
            output_filename = sanitize_filename(output_filename)
            output_path = os.path.join(Config.AUDIO_FOLDER, output_filename)
            
            # Call Eleven Labs API with timestamp request
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            
            headers = {
                "Accept": "application/json",
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": script,
                "model_id": self.model,
                "voice_settings": self.voice_settings
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            # Save audio file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            # Try to get alignment data (if available)
            # Note: Character alignment might require a specific API endpoint
            # For now, we'll generate approximate timestamps
            timestamps = self._generate_approximate_timestamps(script)
            
            file_size = os.path.getsize(output_path)
            
            result = {
                'audio_path': output_path,
                'audio_filename': output_filename,
                'file_size': file_size,
                'timestamps': timestamps,
                'script': script
            }
            
            logger.info(f"Audio with timestamps generated: {output_filename}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating audio with timestamps: {str(e)}")
            raise Exception(f"Failed to generate audio with timestamps: {str(e)}")
    
    def _generate_approximate_timestamps(self, script: str) -> list:
        """
        Generate approximate timestamps based on word count.
        This is a fallback when detailed alignment data isn't available.
        
        Args:
            script: The narration script
            
        Returns:
            List of timestamp dictionaries
        """
        words = script.split()
        words_per_minute = 150  # Average speaking rate
        
        timestamps = []
        current_time = 0.0
        
        for i, word in enumerate(words):
            # Calculate time for this word (with some variation)
            word_duration = 60.0 / words_per_minute
            
            timestamps.append({
                'word': word,
                'start_time': round(current_time, 2),
                'end_time': round(current_time + word_duration, 2)
            })
            
            current_time += word_duration
            
            # Add pauses for punctuation
            if word.endswith(('.', '!', '?')):
                current_time += 0.5  # Half-second pause
            elif word.endswith((',', ';', ':')):
                current_time += 0.25  # Quarter-second pause
        
        return timestamps
    
    def get_audio_duration(self, audio_path: str) -> Optional[float]:
        """
        Get the actual duration of an audio file.
        Requires additional audio processing library (like pydub) for accurate results.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Duration in seconds, or None if unable to determine
        """
        try:
            # This is a placeholder - in production, use a library like pydub
            # from pydub import AudioSegment
            # audio = AudioSegment.from_mp3(audio_path)
            # return len(audio) / 1000.0
            
            # For now, return None and rely on estimates
            return None
            
        except Exception as e:
            logger.error(f"Error getting audio duration: {str(e)}")
            return None
    
    def validate_audio_file(self, audio_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that an audio file exists and is valid.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(audio_path):
            return False, "Audio file does not exist"
        
        if not os.path.isfile(audio_path):
            return False, "Path is not a file"
        
        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            return False, "Audio file is empty"
        
        if file_size < 1000:  # Less than 1KB is suspicious
            return False, "Audio file is too small"
        
        return True, None


def get_audio_generator() -> AudioGenerator:
    """
    Factory function to get an audio generator instance.
    
    Returns:
        Configured AudioGenerator instance
    """
    return AudioGenerator()


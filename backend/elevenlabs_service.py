from google import genai
from elevenlabs import ElevenLabs
from pathlib import Path
from datetime import datetime
from settings import settings
import os


class ElevenLabsService:
    """Service for generating audio explanations using Gemini and ElevenLabs."""

    def __init__(self):
        self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.elevenlabs_client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        Path(settings.AUDIO_DIR).mkdir(exist_ok=True)
        Path(settings.SCRIPTS_DIR).mkdir(exist_ok=True)

    def generate_script(self, user_prompt: str) -> str:
        """
        Generate an educational script using Gemini AI based on the user's question.

        Args:
            user_prompt: The user's question or topic to explain

        Returns:
            A well-formatted educational script (optimized for 10 seconds or less)
        """
        full_prompt = f"""
        You are an expert educational content creator. The user has asked the following question:

        "{user_prompt}"

        Create a clear, concise audio script that explains this concept or answers this question.

        CRITICAL REQUIREMENTS:
        - The script MUST be short enough to be spoken in 10 SECONDS OR LESS
        - Aim for approximately 20-30 WORDS MAXIMUM (average speaking rate is 2-3 words per second)
        - Write in a conversational, friendly tone suitable for audio narration
        - Get straight to the point - no introductions or filler
        - Focus on the core answer or most important concept only
        - Use simple, clear language
        - Don't include stage directions or sound effects - just the spoken content
        - Write as if you're talking directly to the listener

        Return ONLY the script text, nothing else. Keep it VERY SHORT.
        """

        response = self.gemini_client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=full_prompt
        )

        return response.text.strip()

    def generate_audio(self, script: str) -> tuple[str, str]:
        """
        Generate audio file from script using ElevenLabs text-to-speech.

        Args:
            script: The text script to convert to audio

        Returns:
            Tuple of (audio_file_path, script_file_path)
        """
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = f"audio_{timestamp}.mp3"
        script_filename = f"script_{timestamp}.txt"

        audio_path = Path(settings.AUDIO_DIR) / audio_filename
        script_path = Path(settings.SCRIPTS_DIR) / script_filename

        # Save the script to a text file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)

        # Generate audio using ElevenLabs
        audio_generator = self.elevenlabs_client.text_to_speech.convert(
            voice_id=settings.ELEVENLABS_VOICE_ID,
            model_id=settings.ELEVENLABS_MODEL,
            text=script,
            output_format="mp3_44100_128"
        )

        # Save the audio file
        with open(audio_path, 'wb') as f:
            for chunk in audio_generator:
                f.write(chunk)

        return str(audio_path), str(script_path)

    def generate_audio_from_prompt(self, user_prompt: str) -> tuple[str, str, str]:
        """
        Complete pipeline: Generate script from prompt and then create audio.

        Args:
            user_prompt: The user's question or topic

        Returns:
            Tuple of (audio_file_path, script_file_path, script_text)
        """
        # Step 1: Generate script using Gemini
        script = self.generate_script(user_prompt)

        # Step 2: Generate audio using ElevenLabs
        audio_path, script_path = self.generate_audio(script)

        return audio_path, script_path, script


# Create singleton instance
eleven_labs_service = ElevenLabsService()
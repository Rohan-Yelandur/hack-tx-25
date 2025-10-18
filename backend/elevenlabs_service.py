from google import genai
from elevenlabs import ElevenLabs
from pathlib import Path
from datetime import datetime
from settings import settings
import os
import base64


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
            A well-formatted educational script (optimized for 10-15 seconds)
        """
        try:
            print(f"[ElevenLabsService] Generating script for prompt: {user_prompt[:50]}...")
            
            full_prompt = f"""
            You are an expert educational content creator. The user has asked the following question:

            "{user_prompt}"

            Create a clear, concise audio script that explains this concept or answers this question.
            The script should be suitable for narration over an educational animation video.
            
            Keep the explanation engaging and easy to follow. Structure your script to naturally 
            break into segments that can be visualized (e.g., introduction, key concepts, examples, conclusion).
            
            Target length: 10-15 seconds of spoken content (about 30-45 words).
            
            Return ONLY the script text, nothing else. Do not include timestamps or labels.
            """

            response = self.gemini_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=full_prompt
            )

            script = response.text.strip()
            print(f"[ElevenLabsService] Script generated successfully ({len(script)} chars)")
            return script
            
        except Exception as e:
            error_msg = f"Failed to generate script: {type(e).__name__}: {str(e)}"
            print(f"[ElevenLabsService ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(error_msg)

    def generate_audio_with_timestamps(self, script: str) -> tuple[str, str, dict]:
        """
        Generate audio file from script using ElevenLabs text-to-speech with timing data.

        Args:
            script: The text script to convert to audio

        Returns:
            Tuple of (audio_file_path, script_file_path, timing_data)
            timing_data contains character-level timing information
        """
        try:
            print(f"[ElevenLabsService] Generating audio with timestamps for script ({len(script)} chars)...")
            
            # Generate timestamp for unique filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"audio_{timestamp}.mp3"
            script_filename = f"script_{timestamp}.txt"

            audio_path = Path(settings.AUDIO_DIR) / audio_filename
            script_path = Path(settings.SCRIPTS_DIR) / script_filename

            # Save the script to a text file
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script)
            print(f"[ElevenLabsService] Script saved to {script_path}")

            # Generate audio with timestamps using ElevenLabs
            print(f"[ElevenLabsService] Calling ElevenLabs API for audio generation...")
            response = self.elevenlabs_client.text_to_speech.convert_with_timestamps(
                voice_id=settings.ELEVENLABS_VOICE_ID,
                model_id=settings.ELEVENLABS_MODEL,
                text=script,
                output_format="mp3_44100_128"
            )
            print(f"[ElevenLabsService] Received response from ElevenLabs API")
            print(f"[ElevenLabsService] Response type: {type(response)}")

            # Save the audio file from base64 (response is an object, not a dict)
            # Note: attribute is audio_base_64 with underscore, not audio_base64
            audio_bytes = base64.b64decode(response.audio_base_64)
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            print(f"[ElevenLabsService] Audio saved to {audio_path}")

            # Extract timing data (response.alignment is an object)
            timing_data = {
                'characters': response.alignment.characters,
                'character_start_times': response.alignment.character_start_times_seconds,
                'character_end_times': response.alignment.character_end_times_seconds
            }
            
            total_duration = timing_data['character_end_times'][-1] if timing_data['character_end_times'] else 0
            print(f"[ElevenLabsService] Audio duration: {total_duration:.2f} seconds")
            
            return str(audio_path), str(script_path), timing_data
            
        except AttributeError as e:
            error_msg = f"Failed to extract timing data from ElevenLabs response - missing attribute: {str(e)}"
            print(f"[ElevenLabsService ERROR] {error_msg}")
            if 'response' in locals():
                print(f"Response object attributes: {dir(response)}")
            else:
                print("No response received")
            import traceback
            traceback.print_exc()
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Failed to generate audio with timestamps: {type(e).__name__}: {str(e)}"
            print(f"[ElevenLabsService ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(error_msg)


# Create singleton instance
eleven_labs_service = ElevenLabsService()
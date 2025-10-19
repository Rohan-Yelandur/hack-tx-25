from google import genai
from elevenlabs import ElevenLabs
from pathlib import Path
from datetime import datetime
from settings import settings
import os
import base64
import re
import time
                    

def convert_char_timing_to_word_timing(script: str, char_timing: dict) -> list:
    """
    Convert character-level timing data to word-level timing data.
    
    Args:
        script: The original script text
        char_timing: Dictionary with 'characters', 'character_start_times', 'character_end_times'
    
    Returns:
        List of dictionaries with 'word', 'start_time', 'end_time' for each word
    """
    characters = char_timing['characters']
    start_times = char_timing['character_start_times']
    end_times = char_timing['character_end_times']
    
    # Build words by grouping characters
    word_timings = []
    current_word = ""
    word_start_time = None
    word_end_time = None
    char_index = 0
    
    for i, char in enumerate(characters):
        # Skip if we've exhausted the timing data
        if i >= len(start_times):
            break
            
        # Non-space character - part of a word
        if char.strip():
            if current_word == "":
                # Starting a new word
                word_start_time = start_times[i]
            current_word += char
            word_end_time = end_times[i]
        else:
            # Space or whitespace - end of word
            if current_word:
                word_timings.append({
                    'word': current_word,
                    'start_time': word_start_time,
                    'end_time': word_end_time
                })
                current_word = ""
                word_start_time = None
                word_end_time = None
    
    # Don't forget the last word if there is one
    if current_word:
        word_timings.append({
            'word': current_word,
            'start_time': word_start_time,
            'end_time': word_end_time
        })
    
    return word_timings


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

    def generate_script(self, user_prompt: str, pdf_path=None) -> str:
        """
        Generate an educational script using Gemini AI based on the user's question.
        Args:
            user_prompt: The user's question or topic to explain
            pdf_path: Optional path to a PDF file for additional context
        Returns:
            A well-formatted educational script (optimized for 10-15 seconds)
        """
        try:
            print(f"[ElevenLabsService] Generating script for prompt: {user_prompt[:50]}...")
            
            # Prepare contents for Gemini
            contents = []
            
            # If PDF is provided, upload it using the official Files API
            if pdf_path:
                try:
                    print(f"[ElevenLabsService] Uploading PDF to Gemini Files API: {pdf_path}")
                    
                    # Check file size (max 50 MB recommended for Gemini 2.5 Flash)
                    file_size_mb = os.path.getsize(str(pdf_path)) / (1024 * 1024)
                    print(f"[ElevenLabsService] PDF file size: {file_size_mb:.2f} MB")
                    
                    if file_size_mb > 50:
                        raise Exception(f"PDF file is too large ({file_size_mb:.2f} MB). Maximum recommended size is 50 MB.")
                    
                    # Upload PDF using the official SDK method
                    uploaded_file = self.gemini_client.files.upload(file=str(pdf_path))
                    
                    print(f"[ElevenLabsService] PDF uploaded successfully")
                    print(f"[ElevenLabsService] File name: {uploaded_file.name}")
                    print(f"[ElevenLabsService] File URI: {uploaded_file.uri}")
                    print(f"[ElevenLabsService] File state: {uploaded_file.state.name if hasattr(uploaded_file, 'state') else 'unknown'}")
                    
                    # Wait for file to be processed if needed
                    max_wait = 30
                    wait_interval = 2
                    elapsed = 0
                    
                    while hasattr(uploaded_file, 'state') and uploaded_file.state.name == 'PROCESSING' and elapsed < max_wait:
                        print(f"[ElevenLabsService] Waiting for file to be processed... ({elapsed}s)")
                        time.sleep(wait_interval)
                        # Refresh file state
                        uploaded_file = self.gemini_client.files.get(name=uploaded_file.name)
                        elapsed += wait_interval
                    
                    if hasattr(uploaded_file, 'state') and uploaded_file.state.name == 'FAILED':
                        raise Exception(f"File processing failed: {uploaded_file.state}")
                    
                    print(f"[ElevenLabsService] File ready for use (state: {uploaded_file.state.name if hasattr(uploaded_file, 'state') else 'ACTIVE'})")
                    print(f"[ElevenLabsService] Note: Uploaded files expire after 48 hours")
                    
                    # Create prompt
                    full_prompt = f"""
                    You are an expert educational content creator. The user has uploaded a PDF document and asked the following question:

                    "{user_prompt}"

                    Based on the content in the PDF document and also the user's question, create a clear, concise audio script that explains this concept that the user is asking about or the subject covered by the problems in the PDF.
                    The script should be suitable for narration over an educational animation video. It should cover one topic and be concise.
                    
                    Keep the explanation engaging and easy to follow. Structure your script to naturally 
                    break into segments that can be visualized (e.g., introduction, key concepts, examples, conclusion).
                    
                    Target length: 10-15 seconds of spoken content (about 30-45 words).
                    
                    Return ONLY the script text, nothing else. Do not include timestamps or labels.
                    """
                    
                    # Add the uploaded file to contents (this is how the official SDK works)
                    contents.append(uploaded_file)
                    contents.append(full_prompt)
                except Exception as pdf_error:
                    print(f"[ElevenLabsService WARNING] Failed to process PDF: {str(pdf_error)}")
                    print("[ElevenLabsService] Continuing without PDF context")
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
                    contents.append(full_prompt)
            else:
                full_prompt = f"""
                You are an expert educational content creator. The user has asked the following question(s):

                "{user_prompt}"

                Create a clear, concise audio script that explains this concept that the user is asking about or the subject covered by the problems that the user may have inputted.
                The script should be suitable for narration over an educational animation video. It should cover one topic and be concise.
                
                Keep the explanation engaging and easy to follow. Structure your script to naturally 
                break into segments that can be visualized (e.g., introduction, key concepts, examples, conclusion).
                
                Target length: 10-15 seconds of spoken content (about 30-45 words).
                
                Return ONLY the script text, nothing else. Do not include timestamps or labels.
                """
                contents.append(full_prompt)

            response = self.gemini_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents
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
            char_timing_data = {
                'characters': response.alignment.characters,
                'character_start_times': response.alignment.character_start_times_seconds,
                'character_end_times': response.alignment.character_end_times_seconds
            }
            
            # Convert character-level timing to word-level timing
            word_timings = convert_char_timing_to_word_timing(script, char_timing_data)
            
            # Create comprehensive timing data with both formats
            timing_data = {
                'word_timings': word_timings,
                'character_timings': char_timing_data  # Keep for reference if needed
            }
            
            total_duration = char_timing_data['character_end_times'][-1] if char_timing_data['character_end_times'] else 0
            print(f"[ElevenLabsService] Audio duration: {total_duration:.2f} seconds")
            print(f"[ElevenLabsService] Generated word-level timing for {len(word_timings)} words")
            
            # Print formatted word timings for debugging
            print("\n[ElevenLabsService] Word-level timing breakdown:")
            print("-" * 70)
            for i, wt in enumerate(word_timings[:10]):  # Show first 10 words
                print(f"  {wt['start_time']:6.2f}s - {wt['end_time']:6.2f}s : \"{wt['word']}\"")
            if len(word_timings) > 10:
                print(f"  ... and {len(word_timings) - 10} more words")
            print("-" * 70 + "\n")
            
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
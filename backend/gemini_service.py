from google import genai
from google.genai import types
from settings import settings
from prompts import generate_manim_prompt, generate_manim_from_script_prompt
import time

class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    def generate_manim_code(self, prompt: str) -> str:
        """Generate Manim code using Gemini with code execution tool."""
        try:
            full_prompt = generate_manim_prompt(prompt)
            
            # Enable code execution tool for better code generation
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL, 
                contents=full_prompt,
            )
            
            # Extract the generated code from the response
            generated_code = response.text.strip().replace("```python", "").replace("```", "").strip()
            
            return generated_code
            
        except Exception as e:
            raise Exception(f"Gemini service failed: {str(e)}")
    
    def generate_manim_code_from_script(self, user_prompt: str, script: str, timing_data: dict) -> str:
        """Generate Manim code synchronized with audio script and timing data."""
        try:
            print(f"[GeminiService] Generating Manim code from script...")
            print(f"[GeminiService] Script: {script[:100]}...")
            
            # Extract total duration from timing data
            char_timings = timing_data.get('character_timings', {})
            total_duration = char_timings.get('character_end_times', [10])[-1] if char_timings.get('character_end_times') else 10
            word_timings = timing_data.get('word_timings', [])
            
            print(f"[GeminiService] Target duration: {total_duration:.2f} seconds")
            print(f"[GeminiService] Word timings: {len(word_timings)} words")
            
            
            full_prompt = generate_manim_from_script_prompt(user_prompt, script, timing_data)
            
            print(f"[GeminiService] Calling Gemini API for code generation...")
            start_time = time.time()
            
            # Enable code execution tool for better code generation
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL, 
                contents=full_prompt,
            )
            
            end_time = time.time()
            duration = end_time - start_time
            print(f"[GeminiService] Received response from Gemini API (took {duration:.2f} seconds)")
            # Extract the generated code from the response
            generated_code = response.text.strip().replace("```python", "").replace("```", "").strip()
            
            print(f"[GeminiService] Generated {len(generated_code)} chars of Manim code")
            
            return generated_code
            
        except Exception as e:
            error_msg = f"Gemini service failed to generate Manim code: {type(e).__name__}: {str(e)}"
            print(f"[GeminiService ERROR] {error_msg}")
            import traceback
            traceback.print_exc()
            raise Exception(error_msg)


gemini_service = GeminiService()

from google import genai
from google.genai import types
from settings import settings
from prompts import generate_manim_prompt, generate_manim_from_script_prompt

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
                config=types.GenerateContentConfig(
                    tools=[types.Tool(code_execution=types.ToolCodeExecution)]
                ),
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
            total_duration = timing_data['character_end_times'][-1] if timing_data['character_end_times'] else 0
            print(f"[GeminiService] Target duration: {total_duration:.2f} seconds")
            
            full_prompt = generate_manim_from_script_prompt(user_prompt, script, timing_data)
            
            print(f"[GeminiService] Calling Gemini API for code generation...")
            # Enable code execution tool for better code generation
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL, 
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(code_execution=types.ToolCodeExecution)]
                ),
            )
            
            print(f"[GeminiService] Received response from Gemini API")
            
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

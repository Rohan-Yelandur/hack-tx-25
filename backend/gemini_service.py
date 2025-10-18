from google import genai
from google.genai import types
from settings import settings
from prompts import generate_manim_prompt

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


gemini_service = GeminiService()

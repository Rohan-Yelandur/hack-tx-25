from google import genai
from settings import settings
from prompts import generate_manim_prompt

class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    def generate_manim_code(self, prompt: str) -> str:
        """Generate Manim code using Gemini based on a prompt."""
        try:
            full_prompt = generate_manim_prompt(prompt)
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL, 
                contents=full_prompt
            )
            
            return response.text.strip().replace("```python", "").replace("```", "").strip()
            
        except Exception as e:
            raise Exception(f"Gemini service failed: {str(e)}")


gemini_service = GeminiService()

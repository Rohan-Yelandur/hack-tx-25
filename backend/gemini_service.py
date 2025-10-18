from google import genai
from settings import settings


class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    def generate_manim_code(self, prompt: str) -> str:
        """Generate Manim code using Gemini based on a prompt."""
        full_prompt = f"""
        Generate a simple Manim scene based on this description: {prompt}
        Requirements:
        - Create a class called {settings.SCENE_CLASS_NAME} that inherits from Scene
        - Use simple Manim animations
        - Keep it short (3-5 seconds)
        - Only return the Python code, no explanations
        - Import necessary items from manim
        """
        
        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL, 
            contents=full_prompt
        )
        
        return response.text.strip().replace("```python", "").replace("```", "").strip()


gemini_service = GeminiService()

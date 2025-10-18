"""
Gemini Orchestrator Service.
Coordinates the entire pipeline using Gemini API for problem understanding,
solution generation, and script creation.
"""

import os
import logging
from typing import Dict, Optional, Tuple, List
import google.generativeai as genai
from config import Config
from utils.prompts import (
    get_problem_analysis_prompt,
    get_solution_generation_prompt,
    get_teaching_script_prompt,
    get_video_scene_prompt,
    get_concept_extraction_prompt
)
from utils.helpers import clean_latex, validate_problem_text

logger = logging.getLogger(__name__)


class GeminiOrchestrator:
    """
    Orchestrates the math explanation pipeline using Gemini API.
    Handles problem analysis, solution generation, and teaching script creation.
    """
    
    def __init__(self):
        """Initialize the Gemini orchestrator with API configuration."""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in configuration")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            generation_config={
                'temperature': Config.GEMINI_TEMPERATURE,
                'max_output_tokens': Config.GEMINI_MAX_TOKENS,
            }
        )
        
        logger.info(f"Initialized Gemini orchestrator with model: {Config.GEMINI_MODEL}")
    
    def analyze_problem(self, problem_text: str) -> Dict:
        """
        Analyze a math problem to understand its type, concepts, and difficulty.
        
        Args:
            problem_text: The math problem to analyze
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            ValueError: If problem text is invalid
            Exception: If API call fails
        """
        # Validate input
        is_valid, error_msg = validate_problem_text(problem_text)
        if not is_valid:
            raise ValueError(error_msg)
        
        logger.info("Analyzing problem...")
        
        try:
            prompt = get_problem_analysis_prompt(problem_text)
            response = self.model.generate_content(prompt)
            
            analysis = {
                'raw_analysis': response.text,
                'problem_text': problem_text
            }
            
            logger.info("Problem analysis completed")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing problem: {str(e)}")
            raise Exception(f"Failed to analyze problem: {str(e)}")
    
    def generate_solution(self, problem_text: str) -> Dict:
        """
        Generate a complete step-by-step solution to a math problem.
        
        Args:
            problem_text: The math problem to solve
            
        Returns:
            Dictionary containing the solution
            
        Raises:
            ValueError: If problem text is invalid
            Exception: If API call fails
        """
        # Validate input
        is_valid, error_msg = validate_problem_text(problem_text)
        if not is_valid:
            raise ValueError(error_msg)
        
        logger.info("Generating solution...")
        
        try:
            prompt = get_solution_generation_prompt(problem_text)
            response = self.model.generate_content(prompt)
            
            solution_text = clean_latex(response.text)
            
            solution = {
                'solution_text': solution_text,
                'problem_text': problem_text
            }
            
            logger.info("Solution generated successfully")
            return solution
            
        except Exception as e:
            logger.error(f"Error generating solution: {str(e)}")
            raise Exception(f"Failed to generate solution: {str(e)}")
    
    def create_teaching_script(self, problem_text: str, solution_text: str) -> Dict:
        """
        Create an engaging teaching script for video narration.
        
        Args:
            problem_text: The original problem
            solution_text: The complete solution
            
        Returns:
            Dictionary containing the teaching script
            
        Raises:
            Exception: If API call fails
        """
        logger.info("Creating teaching script...")
        
        try:
            prompt = get_teaching_script_prompt(problem_text, solution_text)
            response = self.model.generate_content(prompt)
            
            script = clean_latex(response.text)
            
            teaching_script = {
                'script': script,
                'estimated_duration': len(script.split()) / 150 * 60  # Rough estimate in seconds
            }
            
            logger.info("Teaching script created successfully")
            return teaching_script
            
        except Exception as e:
            logger.error(f"Error creating teaching script: {str(e)}")
            raise Exception(f"Failed to create teaching script: {str(e)}")
    
    def generate_scene_plan(self, script: str) -> Dict:
        """
        Generate a detailed scene plan for Manim video animation.
        
        Args:
            script: The teaching script
            
        Returns:
            Dictionary containing scene plan
            
        Raises:
            Exception: If API call fails
        """
        logger.info("Generating scene plan...")
        
        try:
            prompt = get_video_scene_prompt(script)
            response = self.model.generate_content(prompt)
            
            scene_plan = {
                'raw_plan': response.text,
                'script': script
            }
            
            logger.info("Scene plan generated successfully")
            return scene_plan
            
        except Exception as e:
            logger.error(f"Error generating scene plan: {str(e)}")
            raise Exception(f"Failed to generate scene plan: {str(e)}")
    
    def extract_concepts(self, problem_text: str, solution_text: str) -> Dict:
        """
        Extract key mathematical concepts for reusability.
        
        Args:
            problem_text: The original problem
            solution_text: The complete solution
            
        Returns:
            Dictionary containing extracted concepts
            
        Raises:
            Exception: If API call fails
        """
        logger.info("Extracting concepts...")
        
        try:
            prompt = get_concept_extraction_prompt(problem_text, solution_text)
            response = self.model.generate_content(prompt)
            
            concepts = {
                'concepts': response.text,
                'problem_text': problem_text
            }
            
            logger.info("Concepts extracted successfully")
            return concepts
            
        except Exception as e:
            logger.error(f"Error extracting concepts: {str(e)}")
            raise Exception(f"Failed to extract concepts: {str(e)}")
    
    def process_problem(self, problem_text: str) -> Dict:
        """
        Complete pipeline: analyze, solve, and create teaching script.
        This is the main orchestration method.
        
        Args:
            problem_text: The math problem to process
            
        Returns:
            Dictionary containing all pipeline outputs
            
        Raises:
            ValueError: If problem text is invalid
            Exception: If any step fails
        """
        logger.info("Starting complete problem processing pipeline...")
        
        try:
            # Step 1: Analyze the problem
            analysis = self.analyze_problem(problem_text)
            
            # Step 2: Generate solution
            solution = self.generate_solution(problem_text)
            
            # Step 3: Create teaching script
            teaching_script = self.create_teaching_script(
                problem_text,
                solution['solution_text']
            )
            
            # Step 4: Generate scene plan for video
            scene_plan = self.generate_scene_plan(teaching_script['script'])
            
            # Combine all results
            result = {
                'problem_text': problem_text,
                'analysis': analysis['raw_analysis'],
                'solution': solution['solution_text'],
                'teaching_script': teaching_script['script'],
                'scene_plan': scene_plan['raw_plan'],
                'estimated_duration': teaching_script['estimated_duration']
            }
            
            logger.info("Problem processing pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in processing pipeline: {str(e)}")
            raise
    
    def process_pdf_problem(self, pdf_path: str) -> List[Dict]:
        """
        Process a PDF containing math problems using Gemini's multimodal capabilities.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries, each containing results for one problem
            
        Raises:
            Exception: If PDF processing fails
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            # Upload the PDF file to Gemini
            sample_file = genai.upload_file(path=pdf_path)
            
            # First, extract problems from the PDF
            extraction_prompt = """Analyze this math worksheet PDF and extract all math problems.
            
For each problem, provide:
1. The complete problem statement
2. Any relevant diagrams or figures (describe them)

List each problem separately and clearly."""
            
            response = self.model.generate_content([sample_file, extraction_prompt])
            problems_text = response.text
            
            logger.info("Extracted problems from PDF")
            
            # For now, process the entire document as one problem
            # In a production system, you'd want to split this into individual problems
            result = self.process_problem(problems_text)
            result['source'] = 'pdf'
            result['pdf_path'] = pdf_path
            
            return [result]
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise Exception(f"Failed to process PDF: {str(e)}")


def get_orchestrator() -> GeminiOrchestrator:
    """
    Factory function to get an orchestrator instance.
    Useful for dependency injection and testing.
    
    Returns:
        Configured GeminiOrchestrator instance
    """
    return GeminiOrchestrator()


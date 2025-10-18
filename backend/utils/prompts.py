"""
Prompt templates for the Gemini orchestrator.
These prompts guide the LLM through different stages of the explanation pipeline.
"""


PROBLEM_ANALYSIS_PROMPT = """You are an expert mathematics tutor. Analyze the following math problem and provide:

1. **Problem Type**: Identify the mathematical domain (algebra, calculus, geometry, etc.)
2. **Key Concepts**: List the core mathematical concepts needed to solve this problem
3. **Difficulty Level**: Rate the difficulty (elementary, intermediate, advanced)
4. **Prerequisites**: What knowledge should a student have before attempting this?

Problem:
{problem_text}

Provide your analysis in a structured format."""


SOLUTION_GENERATION_PROMPT = """You are an expert mathematics tutor. Solve the following problem step by step.

Problem:
{problem_text}

Provide a complete solution with:
1. Clear step-by-step reasoning
2. Mathematical notation when appropriate
3. Explanations for each major step
4. The final answer

Be thorough but concise. Make each step clear and logical."""


TEACHING_SCRIPT_PROMPT = """You are an engaging math teacher creating a video explanation. Based on the problem and solution below, write a natural, conversational teaching script.

Problem:
{problem_text}

Solution:
{solution}

Requirements:
1. Start with a friendly introduction of the problem
2. Explain each step in a conversational, engaging manner
3. Use phrases like "Let's start by...", "Notice that...", "This means..."
4. Build intuition, not just mechanical steps
5. Keep sentences short and clear for narration
6. End with a brief recap of what was learned
7. The script should be 2-4 minutes when spoken
8. Use LaTeX notation wrapped in $...$ for math expressions

Write ONLY the narration script, as if you're speaking directly to a student watching the video."""


VIDEO_SCENE_PROMPT = """Based on the teaching script and timestamps, create a detailed scene plan for Manim animation.

Teaching Script:
{script}

For each major section of the script, specify:
1. **Visual Elements**: What equations, graphs, or diagrams should appear
2. **Timing**: When elements should appear/transform (use the timestamps)
3. **Animations**: Specific animation types (Write, FadeIn, Transform, etc.)
4. **Text Overlays**: Key points to display as text

Provide a structured list of scenes with timing and visual elements. Use LaTeX for all mathematical notation."""


CONCEPT_EXTRACTION_PROMPT = """Extract key mathematical concepts from this problem that could be reused for similar explanations.

Problem: {problem_text}
Solution: {solution}

Identify:
1. Core mathematical principles
2. Common problem-solving strategies used
3. Visualizations that would help understanding
4. Related concepts or extensions

This will help build a concept library for future explanations."""


def get_problem_analysis_prompt(problem_text: str) -> str:
    """Generate prompt for analyzing a math problem."""
    return PROBLEM_ANALYSIS_PROMPT.format(problem_text=problem_text)


def get_solution_generation_prompt(problem_text: str) -> str:
    """Generate prompt for solving a math problem."""
    return SOLUTION_GENERATION_PROMPT.format(problem_text=problem_text)


def get_teaching_script_prompt(problem_text: str, solution: str) -> str:
    """Generate prompt for creating a teaching script."""
    return TEACHING_SCRIPT_PROMPT.format(
        problem_text=problem_text,
        solution=solution
    )


def get_video_scene_prompt(script: str) -> str:
    """Generate prompt for creating video scene plan."""
    return VIDEO_SCENE_PROMPT.format(script=script)


def get_concept_extraction_prompt(problem_text: str, solution: str) -> str:
    """Generate prompt for extracting reusable concepts."""
    return CONCEPT_EXTRACTION_PROMPT.format(
        problem_text=problem_text,
        solution=solution
    )


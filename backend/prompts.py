from settings import settings

manim_docs = f'''
CORE STRUCTURE:
    ```python
    from manim import *

    class GeneratedScene(Scene):
        def construct(self):
            # Your animations here
            pass
    ```

    CORE ANIMATIONS (use with self.play()):
    - Creation: Create(obj), Write(obj), DrawBorderThenFill(obj), FadeIn(obj)
    - Removal: FadeOut(obj), Uncreate(obj), Unwrite(obj)
    - Transform: Transform(obj1, obj2), ReplacementTransform(obj1, obj2), FadeTransform(obj1, obj2)
    - Movement: obj.animate.shift(direction), obj.animate.move_to(point), obj.animate.next_to(other)
    - Modification: obj.animate.scale(factor), obj.animate.rotate(angle), obj.animate.set_color(color)
    - Indication: Indicate(obj), Circumscribe(obj), Flash(obj), FocusOn(obj)
    - Special: AnimationGroup(anim1, anim2), Succession(anim1, anim2), LaggedStart(anim1, anim2)

    POSITIONING & LAYOUT:
    - Absolute: obj.move_to(ORIGIN), obj.to_edge(UP), obj.to_corner(UL)
    - Relative: obj.next_to(other, DOWN, buff=0.5), obj.shift(RIGHT*2 + UP)
    - Alignment: obj.align_to(other, UP), VGroup(*objects).arrange(DOWN, buff=0.5)
    - Constants: UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR, ORIGIN

    FRAME BOUNDARIES & CAMERA (CRITICAL TO AVOID CROPPING):
    - **Frame dimensions: Width = -7 to +7, Height = -4 to +4**
    - **Keep ALL objects within these bounds to avoid cropping!**
    - Safe zone for main content: X: -6 to +6, Y: -3 to +3
    - Default object sizes:
      * Circle: radius ≤ 2 (safe), radius ≤ 1.5 (recommended for complex scenes)
      * Square/Rectangle: side_length ≤ 3 (safe), ≤ 2 (recommended)
      * Text: font_size ≤ 48 (safe), scale ≤ 1.5 for long text
    - **IMPORTANT: When creating large objects or groups, scale them down!**
      Example: VGroup(*objects).scale(0.7) to fit everything in frame
    - Use .get_width() and .get_height() to check object dimensions
    - Position objects at ORIGIN or use .move_to(ORIGIN) for centered content
    - Test positioning: If unsure, start small and at center (ORIGIN)

    ANIMATION PATTERNS:
    1. Simple display:
    obj = Circle()
    self.play(Create(obj))
    self.wait(1)

    2. Transform sequence:
    text1 = Text("Before")
    text2 = Text("After")
    self.play(Write(text1))
    self.wait(0.5)
    self.play(ReplacementTransform(text1, text2))
    
    3. Using .animate:
    circle = Circle()
    self.play(Create(circle))
    self.play(circle.animate.scale(2).shift(UP))

    4. Multiple simultaneous:
    self.play(Create(circle), Write(text), run_time=2)

    5. Grouped objects:
    group = VGroup(obj1, obj2, obj3)
    group.arrange(RIGHT, buff=1)
    self.play(Create(group))

    COLORS:
    Use: RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, WHITE, GRAY, BLACK, TEAL, MAROON, etc.
    Set with: obj.set_color(BLUE) or color=BLUE in constructor

    COMMON PARAMETERS:
    - run_time=2: Animation duration in seconds
    - buff=0.5: Buffer/spacing between objects
    - opacity=0.5: Transparency (0=invisible, 1=opaque)
    - fill_opacity=0.7: Fill transparency for shapes
    - stroke_width=4: Line thickness

    BEST PRACTICES:
    1. **ALWAYS keep objects within frame bounds (X: -6 to 6, Y: -3 to 3)**
    2. **Start with smaller object sizes - you can always scale up if needed**
    3. Use self.wait() between animations (0.5-2 seconds)
    4. Chain transformations with .animate for smooth transitions
    5. Group related objects with VGroup and scale the group to fit: .scale(0.7)
    6. Scale text/formulas appropriately: .scale(0.8) to .scale(1.5)
    7. Use buff parameter for spacing: buff=0.5 is standard
    8. Add run_time for better pacing: run_time=1.5
    9. Use FadeOut to clean up before new content
    10. Position objects at ORIGIN or center before animating when possible
    11. For complex scenes with many objects, use .scale(0.6) or .scale(0.8) on the entire VGroup

    EXAMPLE PATTERNS:

    Educational Concept:
    ```python
    title = Text("Pythagorean Theorem").to_edge(UP)
    formula = MathTex(r"a^2 + b^2 = c^2").scale(1.5)
    explanation = Text("For right triangles", font_size=24).next_to(formula, DOWN)
    self.play(Write(title))
    self.play(Write(formula))
    self.wait(1)
    self.play(FadeIn(explanation))
    ```

    Geometric Animation:
    ```python
    square = Square(side_length=2, color=BLUE, fill_opacity=0.5)
    circle = Circle(radius=1.4, color=RED, fill_opacity=0.5)
    self.play(Create(square))
    self.play(Transform(square, circle))
    self.wait()
    ```

    Graph Visualization:
    ```python
    axes = Axes(x_range=[-3,3], y_range=[-2,2])
    graph = axes.plot(lambda x: x**2, color=BLUE)
    label = MathTex(r"f(x) = x^2").next_to(graph, UP)
    self.play(Create(axes))
    self.play(Create(graph), Write(label))
    ```

    Avoiding Cropping (Scaling Down Complex Scenes):
    ```python
    # Create multiple objects
    circle = Circle(radius=1.5, color=BLUE)
    square = Square(side_length=1.5, color=RED).shift(RIGHT*2)
    triangle = Triangle().shift(LEFT*2)
    title = Text("Shapes", font_size=40).to_edge(UP)

    # Group and scale to ensure everything fits
    shapes = VGroup(circle, square, triangle)
    shapes.scale(0.7)  # Scale down to fit comfortably in frame

    self.play(Write(title))
    self.play(Create(shapes))
    ```
'''


def generate_manim_prompt(prompt: str) -> str:
    return f"""You are an expert at generating Manim (Mathematical Animation Engine) code. Generate Python code for Manim Community Edition based on this request: {prompt}

    CRITICAL REQUIREMENTS:
    1. Create a class called {settings.SCENE_CLASS_NAME} that inherits from Scene
    2. Implement the construct() method where all animations happen
    3. Start with: from manim import *
    4. USE CODE EXECUTION to validate your Python code for syntax errors before returning it
    5. Return ONLY valid, syntactically correct Python code, no explanations or markdown
    6. Target 5-15 seconds total animation time
    7. Test imports and basic syntax using code execution to ensure no errors
    8. You need to add comments above each section of code within each time interval specified by the play() run_time 
       and the wait() calls and also a description of what is being displayed/explained for specifically that block of code.
       Your comments should include specific time stamps for how long you think that section of code will take to run.
       Do not include any other unnecessary information in the comments.

       
  Use these manim docs to help you when generating code: {manim_docs}
    
    VALIDATION INSTRUCTIONS:
    1. Write the Manim code for the request
    2. Use code execution to validate the syntax (check imports, class definition, method syntax)
    3. **CRITICAL: Verify all objects fit within frame bounds (X: -6 to 6, Y: -3 to 3)**
    4. **Check object sizes: circles radius ≤ 1.5, squares side_length ≤ 2, text scale ≤ 1.5**
    5. **If scene has multiple objects, scale the entire VGroup to 0.7 or 0.8 to ensure everything fits**
    6. Fix any syntax errors found during validation
    7. Return only the final, validated Python code that will render WITHOUT cropping
    Remember: Use code execution to validate your code before returning it!
    
    Now generate code for: {prompt}
    """


def generate_manim_from_script_prompt(user_prompt: str, script: str, timing_data: dict) -> str:
    """
    Generate a prompt for creating Manim code synchronized with an audio script.
    
    Args:
        user_prompt: The original user request
        script: The narration script that will be spoken
        timing_data: Character-level timing data from ElevenLabs
    """
    
    # Calculate total audio duration
    total_duration = timing_data['character_end_times'][-1] if timing_data['character_end_times'] else 10
    
    return f"""You are an expert at generating Manim (Mathematical Animation Engine) code synchronized with audio narration.

USER REQUEST: {user_prompt}

AUDIO NARRATION SCRIPT:
"{script}"

AUDIO DURATION: {total_duration:.2f} seconds

Your task is to generate Manim code that creates a visual animation synchronized with this narration.
The animation should match the pacing and content of the audio script.

CRITICAL REQUIREMENTS:
1. Create a class called {settings.SCENE_CLASS_NAME} that inherits from Scene
2. Implement the construct() method where all animations happen
3. Start with: from manim import *
4. **TOTAL ANIMATION TIME MUST BE {total_duration:.2f} seconds to match the audio**
5. USE CODE EXECUTION to validate your Python code for syntax errors before returning it
6. Return ONLY valid, syntactically correct Python code, no explanations or markdown

SYNCHRONIZATION GUIDELINES:
1. Break the script into logical segments (e.g., introduction, main concept, example, conclusion)
2. Time your animations to match when those segments would be spoken in the narration
3. Use self.wait() to control pacing and match the audio timing
4. Plan animations so visual changes align with key words/phrases in the narration
5. The total sum of all run_time and wait() calls should equal approximately {total_duration:.2f} seconds

EXAMPLE TIMING BREAKDOWN:
- If the script is 10 seconds and has 3 key points, allocate roughly 3-4 seconds per point
- Use run_time parameter: self.play(Create(obj), run_time=2)
- Add pauses: self.wait(1.5) between major transitions
- Keep animations smooth and not too fast

Use these manim docs to help you when generating code: {manim_docs}
    
VALIDATION INSTRUCTIONS:
1. Write the Manim code that visualizes the narration
2. Use code execution to validate the syntax (check imports, class definition, method syntax)
3. **CRITICAL: Verify all objects fit within frame bounds (X: -6 to 6, Y: -3 to 3)**
4. **Check object sizes: circles radius ≤ 1.5, squares side_length ≤ 2, text scale ≤ 1.5**
5. **If scene has multiple objects, scale the entire VGroup to 0.7 or 0.8 to ensure everything fits**
6. **Verify total animation time matches {total_duration:.2f} seconds**
7. Fix any syntax errors found during validation
8. Return only the final, validated Python code that will render WITHOUT cropping

Remember: Use code execution to validate your code before returning it!
    
Now generate synchronized Manim code for this narration.
"""

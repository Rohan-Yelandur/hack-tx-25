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
    Standard colors: RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, PINK, WHITE, GRAY, GREY, BLACK, TEAL, MAROON, GOLD, DARK_BLUE, LIGHT_GRAY
    **IMPORTANT: DO NOT use BROWN - it is not defined. Use MAROON, ORANGE, or hex colors like "#8B4513" instead**
    For custom colors use hex: obj.set_color("#8B4513")
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
    4. Return ONLY valid, syntactically correct Python code, no explanations or markdown
    5. Target 5-15 seconds total animation time

       
  Use these manim docs to help you when generating code: {manim_docs}
    
    IMPORTANT GUIDELINES:
    1. Write clean, working Manim code for the request
    2. **CRITICAL: Verify all objects fit within frame bounds (X: -6 to 6, Y: -3 to 3)**
    3. **Check object sizes: circles radius ≤ 1.5, squares side_length ≤ 2, text scale ≤ 1.5**
    4. **If scene has multiple objects, scale the entire VGroup to 0.7 or 0.8 to ensure everything fits**
    5. **NEVER use BROWN - it doesn't exist in Manim. Use MAROON, ORANGE, or hex colors like "#8B4513" instead**
    6. Return only the final Python code that will render WITHOUT cropping
    
    Now generate code for: {prompt}
    """


def generate_manim_from_script_prompt(user_prompt: str, script: str, timing_data: dict) -> str:
    """
    Generate a prompt for creating Manim code synchronized with an audio script.
    
    Args:
        user_prompt: The original user request
        script: The narration script that will be spoken
        timing_data: Dictionary containing 'word_timings' and 'character_timings'
    """
    
    # Extract word timings
    word_timings = timing_data.get('word_timings', [])
    
    # Calculate total audio duration from character timings
    char_timings = timing_data.get('character_timings', {})
    total_duration = char_timings.get('character_end_times', [10])[-1] if char_timings.get('character_end_times') else 10
    
    # Format word timings for the prompt
    timing_breakdown = "\n".join([
        f"  {wt['start_time']:6.2f}s - {wt['end_time']:6.2f}s : \"{wt['word']}\""
        for wt in word_timings
    ])
    
    return f"""You are an expert at generating Manim (Mathematical Animation Engine) code synchronized with audio narration.

USER REQUEST: {user_prompt}

AUDIO NARRATION SCRIPT:
"{script}"

AUDIO DURATION: {total_duration:.2f} seconds

WORD-LEVEL TIMING DATA:
Below is the exact timing of when each word is spoken in the audio. Use this to synchronize your animations:

{timing_breakdown}

Your task is to generate Manim code that creates a visual animation synchronized with this narration.
The animation should match the pacing and content of the audio script.

CRITICAL REQUIREMENTS:
1. Create a class called {settings.SCENE_CLASS_NAME} that inherits from Scene
2. Implement the construct() method where all animations happen
3. Start with: from manim import *
4. **TOTAL ANIMATION TIME MUST BE {total_duration:.2f} seconds to match the audio**
5. Return ONLY valid, syntactically correct Python code, no explanations or markdown
6. **DO NOT use MathTex, Tex, or any LaTeX-based objects** - use Text() instead for all text/labels

SYNCHRONIZATION GUIDELINES:
1. Look at the word timing data above to see exactly when each word is spoken
2. Group related words into phrases and create animations that align with those phrases
3. Use self.wait() to control pacing and match the audio timing precisely
4. Plan animations so visual changes align with key words/phrases in the narration
5. The total sum of all run_time and wait() calls should equal approximately {total_duration:.2f} seconds

ANIMATION TIMING STRATEGY:
- Use the word timings to determine when to start/end animations
- For example, if words "Vector addition" are spoken from 0.0s to 1.2s, create/show related objects during that time
- Use run_time parameter: self.play(Create(obj), run_time=x) to match word timing
- Add brief pauses: self.wait(0.2-0.5) between major transitions
- Keep animations smooth and natural
- **CRITICAL: NEVER use negative wait times. Always ensure self.wait() has a positive duration**
- **Use max(0.1, target_time - current_time) to prevent negative waits**
- Example: self.wait(max(0.1, 5.22 - 4.58)) ensures minimum 0.1s wait

Use these manim docs to help you when generating code: {manim_docs}
    
VALIDATION INSTRUCTIONS:
1. Write the Manim code that visualizes the narration using word timing data
2. **CRITICAL: Verify all objects fit within frame bounds (X: -6 to 6, Y: -3 to 3)**
3. **Check object sizes: circles radius ≤ 1.5, squares side_length ≤ 2, text scale ≤ 1.5**
4. **If scene has multiple objects, scale the entire VGroup to 0.7 or 0.8 to ensure everything fits**
5. **Verify total animation time matches {total_duration:.2f} seconds**
6. **Use Text() objects ONLY - no MathTex, Tex, or LaTeX**
7. **NEVER use BROWN - it doesn't exist in Manim. Use MAROON, ORANGE, or hex colors like "#8B4513" instead**
8. **NEVER use negative wait times - use max(0.1, target_time - current_time) to ensure all waits are positive**
9. Fix any syntax errors before returning code

    
Now generate audio-synchronized Manim code for this visualization of the narration script.
Use the word-level timing data to precisely align animations with the spoken narration.
"""

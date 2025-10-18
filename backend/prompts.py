from settings import settings

def generate_manim_prompt(prompt: str) -> str:
    return f"""You are an expert at generating Manim (Mathematical Animation Engine) code. Generate Python code for Manim Community Edition based on this request: {prompt}

    CRITICAL REQUIREMENTS:
    1. Create a class called {settings.SCENE_CLASS_NAME} that inherits from Scene
    2. Implement the construct() method where all animations happen
    3. Start with: from manim import *
    4. Return ONLY valid Python code, no explanations or markdown
    5. Target 15-30 seconds total animation time

    CORE STRUCTURE:
    ```python
    from manim import *

    class GeneratedScene(Scene):
        def construct(self):
            # Your animations here
            pass
    ```

    ESSENTIAL MOBJECTS (Visual Objects):
    - Text & Math: Text("Hello"), MathTex(r"\\frac{{a}}{{b}}"), Tex(r"\\LaTeX")
    - Shapes: Circle(), Square(), Rectangle(), Triangle(), Polygon(), RegularPolygon(n=6)
    - Lines & Arrows: Line(start, end), Arrow(start, end), Vector([x,y]), Dot(point)
    - Graphs: Axes(), NumberPlane(), FunctionGraph(lambda x: x**2)
    - 3D: Sphere(), Cube(), Cone(), Surface()
    - Groups: VGroup(obj1, obj2) for grouping objects

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
    - radius=1.5: Size for circles
    - width=3, height=2: Dimensions for rectangles

    MATH & TEXT TIPS:
    - MathTex for equations: MathTex(r"E = mc^2", r"F = ma").scale(1.5)
    - Use raw strings (r"") for LaTeX
    - Chain methods: Text("Hello").scale(2).to_edge(UP).set_color(BLUE)
    - Subscripts: r"x_{{1}}", Superscripts: r"x^{{2}}"
    - Fractions: r"\\frac{{a}}{{b}}", Sqrt: r"\\sqrt{{x}}"

    BEST PRACTICES:
    1. Use self.wait() between animations (0.5-2 seconds)
    2. Chain transformations with .animate for smooth transitions
    3. Group related objects with VGroup
    4. Scale text/formulas appropriately: .scale(0.8) to .scale(2)
    5. Use buff parameter for spacing: buff=0.5 is standard
    6. Add run_time for better pacing: run_time=1.5
    7. Use FadeOut to clean up before new content
    8. Position objects before animating them when possible

    EXAMPLE PATTERNS:

    Educational Concept:
    ```python
    title = Text("Topic").to_edge(UP)
    formula = MathTex(r"a^2 + b^2 = c^2").scale(1.5)
    explanation = Text("Explanation", font_size=24).next_to(formula, DOWN)
    self.play(Write(title))
    self.play(Create(formula))
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

    Multi-step Process:
    ```python
    steps = VGroup(*[Text(f"Step {{i}}") for i in range(1,4)])
    steps.arrange(DOWN, buff=0.8)
    for step in steps:
        self.play(Write(step))
        self.wait(0.5)
    ```

    Graph Visualization:
    ```python
    axes = Axes(x_range=[-3,3], y_range=[-2,2])
    graph = axes.plot(lambda x: x**2, color=BLUE)
    label = axes.get_graph_label(graph, label='y=x^2')
    self.play(Create(axes))
    self.play(Create(graph), Write(label))
    ```

    Now generate code for, ensure that it is working Python code that follows the prompt and
    does not have any errors.: {prompt}"""

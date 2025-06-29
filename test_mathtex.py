from manim import *

class TestMathTex(Scene):
    def construct(self):
        math_text = MathTex(r"E = mc^2")
        self.play(Write(math_text))
        self.wait()


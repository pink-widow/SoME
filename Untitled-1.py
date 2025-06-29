from manim import *

import random

import itertools



class Introduction(Scene):

    def construct(self):

        # --- CONFIGURATION (unchanged) ---

        node_radius = 0.3

        PLUS_ONE_COLOR = BLUE_D

        MINUS_ONE_COLOR = RED_D

        TEXT_COLOR = YELLOW

        J_COLOR = YELLOW

        H_COLOR = GREEN

        # --- TITLE TEXT (unchanged) ---

        title = MarkupText(f'Each person decides <span color="{YELLOW}">yes or no</span> on some question.', font_size=36).to_edge(UP)

        subtitle = MarkupText(f'\n We’ll call “yes” <span color="{PLUS_ONE_COLOR}">+1</span> and “no” <span color="{MINUS_ONE_COLOR}">–1</span>.', font_size=30).next_to(title, DOWN, buff=0.2)

        self.play(Write(title))

        self.wait(0.5)

        self.play(Write(subtitle))

        self.wait()


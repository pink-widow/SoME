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
        subtitle = MarkupText(f'We’ll call “yes” <span color="{PLUS_ONE_COLOR}">+1</span> and “no” <span color="{MINUS_ONE_COLOR}">–1</span>.', font_size=30).next_to(title, DOWN, buff=0.2)
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(subtitle))
        self.wait()
        
        # --- OBJECTS (unchanged) ---
        alice_circle = Circle(radius=node_radius, color=WHITE, fill_opacity=0.8).move_to(LEFT * 2.5)
        alice_name = Text("Alice", font_size=36).next_to(alice_circle, DOWN, buff=0.3)
        bob_circle = Circle(radius=node_radius, color=WHITE, fill_opacity=0.8).move_to(RIGHT * 2.5)
        bob_name = Text("Bob", font_size=36).next_to(bob_circle, DOWN, buff=0.3)
        up_arrow = Arrow(DOWN*0.2, UP*0.2, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        down_arrow = Arrow(UP*0.2, DOWN*0.2, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        
        # --- INITIAL ANIMATION (unchanged, just shortened for brevity in this view) ---
        self.play(Create(alice_circle), Create(bob_circle), Write(alice_name), Write(bob_name))
        alice_up = up_arrow.copy().move_to(alice_circle.get_center())
        alice_plus_text = MathTex("+1", color=TEXT_COLOR).next_to(alice_circle, UP)
        bob_up = up_arrow.copy().move_to(bob_circle.get_center())
        bob_plus_text = MathTex("+1", color=TEXT_COLOR).next_to(bob_circle, UP)
        self.play(
            alice_circle.animate.set_color(PLUS_ONE_COLOR), Create(alice_up), Write(alice_plus_text),
            bob_circle.animate.set_color(PLUS_ONE_COLOR), Create(bob_up), Write(bob_plus_text)
        )
        self.wait()

        # --- NEW CODE STARTS HERE ---

        # 1. Clean up the scene and reposition
        alice_bob_group = VGroup(
            alice_circle, alice_name, alice_up, alice_plus_text,
            bob_circle, bob_name, bob_up, bob_plus_text
        )
        self.play(
            FadeOut(title, subtitle),
            alice_bob_group.animate.scale(0.9).to_edge(LEFT, buff=1.0)
        )
        self.wait(0.5)

        # 2. Define Table and Status Labels
        table_data = [
            [r"s_1", r"s_2", r"s_1 s_2"],
            [r"+1", r"+1", r"+1"],
            [r"+1", r"-1", r"-1"],
            [r"-1", r"+1", r"-1"],
            [r"-1", r"-1", r"+1"],
        ]
        table = MathTable(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2, "color": TEAL},
            h_buff=0.7,
            v_buff=0.4
        ).scale(0.8).next_to(alice_bob_group, RIGHT, buff=1.0)

        status_texts = VGroup(
            MarkupText(f'<span color="{GREEN}">Agree</span>', font_size=28),
            MarkupText(f'<span color="{ORANGE}">Disagree</span>', font_size=28),
            MarkupText(f'<span color="{ORANGE}">Disagree</span>', font_size=28),
            MarkupText(f'<span color="{GREEN}">Agree</span>', font_size=28),
        )

        # 3. Animate the table appearing row-by-row
        header = table.get_rows()[0]
        h_lines = table.get_horizontal_lines()
        v_lines = table.get_vertical_lines()
        
        self.play(Write(header), Create(VGroup(*h_lines, *v_lines)))
        self.wait()

        # Loop through each data row
        for i in range(1, 5):
            s1_val = int(table_data[i][0])
            s2_val = int(table_data[i][1])

            # Define target states for Alice and Bob
            alice_target_arrow = (up_arrow if s1_val == 1 else down_arrow).copy().move_to(alice_circle.get_center())
            alice_target_text = MathTex(f"{s1_val:+}", color=TEXT_COLOR).next_to(alice_circle, UP)
            alice_target_color = PLUS_ONE_COLOR if s1_val == 1 else MINUS_ONE_COLOR

            bob_target_arrow = (up_arrow if s2_val == 1 else down_arrow).copy().move_to(bob_circle.get_center())
            bob_target_text = MathTex(f"{s2_val:+}", color=TEXT_COLOR).next_to(bob_circle, UP)
            bob_target_color = PLUS_ONE_COLOR if s2_val == 1 else MINUS_ONE_COLOR
            
            # Position the status text for this row
            current_status = status_texts[i-1].next_to(table.get_rows()[i], RIGHT, buff=0.5)

            # Animate everything together
            self.play(
                Transform(alice_up, alice_target_arrow),
                Transform(alice_plus_text, alice_target_text),
                alice_circle.animate.set_color(alice_target_color),
                Transform(bob_up, bob_target_arrow),
                Transform(bob_plus_text, bob_target_text),
                bob_circle.animate.set_color(bob_target_color),
                Write(table.get_rows()[i]),
                Write(current_status),
                run_time=1.5
            )
            self.wait(0.5)
        
        self.wait()
        
        # --- NEW SEQUENCE STARTS HERE ---

        # 1. Clean up the previous scene
        all_table_elements = VGroup(table, status_texts)
        self.play(
            FadeOut(alice_bob_group),
            FadeOut(all_table_elements)
        )
        self.wait(0.5)

        # 2. Display the "tension" text
        tension_text = MarkupText(
            'But in the real world, people have a relationship.\n'
            'A <span color="ORANGE">tension</span>, you might say.',
            font_size=36,
            justify=True
        ).move_to(ORIGIN)

        self.play(Write(tension_text))
        self.wait(3) # Pause for narration
        self.play(FadeOut(tension_text))
        self.wait(0.5)

        # 3. Re-create Alice and Bob, more spread out
        alice_circle_new = Circle(radius=node_radius, color=WHITE, fill_opacity=0.8)
        alice_name_new = Text("Alice", font_size=36).next_to(alice_circle_new, DOWN, buff=0.3)
        alice_group_new = VGroup(alice_circle_new, alice_name_new).move_to(LEFT * 3)

        bob_circle_new = Circle(radius=node_radius, color=WHITE, fill_opacity=0.8)
        bob_name_new = Text("Bob", font_size=36).next_to(bob_circle_new, DOWN, buff=0.3)
        bob_group_new = VGroup(bob_circle_new, bob_name_new).move_to(RIGHT * 3)

        self.play(
            Create(alice_group_new),
            Create(bob_group_new)
        )
        self.wait()

        # 4. Add the J_12 label and the segmented connection line
        j_label = MathTex("J_{12}", color=YELLOW).scale(1.2)
        j_label.move_to((alice_circle_new.get_center() + bob_circle_new.get_center()) / 2)

        # Create two separate lines that stop short of the label
        line1 = Line(
            alice_circle_new.get_right(),
            j_label.get_left(),
            buff=0.2,
            color=TEAL,
            stroke_width=3
        )
        line2 = Line(
            j_label.get_right(),
            bob_circle_new.get_left(),
            buff=0.2,
            color=TEAL,
            stroke_width=3
        )
        
        # Animate the appearance of the connection
        self.play(
            Create(line1),
            Create(line2),
            Write(j_label)
        )
        self.wait()

        # --- NEW SEQUENCE STARTS HERE (CORRECTED LAYOUT) ---

        # 1. Group the existing elements and move them to the left
        connection_group = VGroup(alice_group_new, bob_group_new, j_label, line1, line2)
        self.play(
            connection_group.animate.scale(0.9).to_edge(LEFT, buff=1.0)
        )
        self.wait(0.5)

        # 2. Create the VERTICAL J-axis with more ticks
        j_axis = NumberLine(
            x_range=[-1.5, 1.5, 0.5],
            length=5,
            color=WHITE,
            include_tip=True,
            tip_width=0.2,
            tip_height=0.2,
            include_numbers=False 
        )
        
        # Manually add numbers at the default position (below the line)
        j_axis.add_numbers(
            x_values=[-1, 0, 1],
            font_size=32
        )
        
        j_axis.rotate(PI / 2) # Rotate the line and the numbers together
        j_axis.move_to(RIGHT * 2.5)
        
        # --- THIS IS THE FIX ---
        # Now that the axis is vertical, shift the numbers to the LEFT
        j_axis.numbers.shift(LEFT * 0.85)

        j_axis_title = MathTex("J_{12}", "\\text{ dial}", color=YELLOW).next_to(j_axis, UP)
        j_axis_title[1].set_color(WHITE)

        self.play(Create(j_axis), Write(j_axis_title))
        self.wait()

        # 3. Create the simplified descriptive labels
        positive_label = MarkupText(
            f'<span color="{RED_E}">Tense</span>', font_size=34
        ).next_to(j_axis.n2p(1), RIGHT, buff=0.4)

        negative_label = MarkupText(
            f'<span color="{BLUE_E}">Cozy</span>', font_size=34
        ).next_to(j_axis.n2p(-1), RIGHT, buff=0.4)

        zero_label = MarkupText(
            'No influence', font_size=34
        ).next_to(j_axis.n2p(0), RIGHT, buff=0.4)

        # 4. Animate the explanations sequentially with a pointer dot
        dot = Dot(color=YELLOW).scale(1.2)

        # J > 0 (Tense)
        dot.move_to(j_axis.n2p(1))
        self.play(FadeIn(dot, scale=0.5), Write(positive_label))
        self.wait(1.5)

        # J < 0 (Cozy)
        self.play(
            dot.animate.move_to(j_axis.n2p(-1)),
            Write(negative_label)
        )
        self.wait(1.5)

        # J = 0 (No influence)
        self.play(
            dot.animate.move_to(j_axis.n2p(0)),
            Write(zero_label)
        )
        self.wait(1.5)
        
        # 5. Fade out the dial and get ready for the next part
        j_dial_group = VGroup(j_axis, j_axis.numbers, j_axis_title, positive_label, negative_label, zero_label, dot)
        self.play(FadeOut(j_dial_group))
        
        self.add(connection_group) 
        self.wait()

        # (This code follows immediately after the FadeOut of the first j_dial_group)
        # The 'connection_group' Mobject is still present on the screen.
        
        # --- NEW SEQUENCE STARTS HERE (CORRECTED WITH SMOOTH MOVEMENT) ---

        # --- PART 1: DEFINE ALL OBJECTS AND CALCULATE FINAL LAYOUT ---

        # A) Create a target copy of the diagram to calculate its final position
        target_connection_group = connection_group.copy()
        target_connection_group.scale(0.9).to_edge(UP, buff=1.0)

        # B) Left Panel: Formulas (we won't show them yet)
        desc_font_size = 28
        desc_part1 = MarkupText(f'<span color="{H_COLOR}">Conflict</span> = <span color="{PLUS_ONE_COLOR}">Alice\'s choice</span> × <span color="{J_COLOR}">Tension</span> × ', font_size=desc_font_size)
        desc_bob_choice = MarkupText(f'<span color="{PLUS_ONE_COLOR}">Bob\'s choice</span>', font_size=desc_font_size)
        desc_formula = VGroup(desc_part1, desc_bob_choice).arrange(RIGHT, buff=0.1)
        math_formula = MathTex("H", "=", "s_1", "J_{12}", "s_2", tex_to_color_map={"H": H_COLOR, "s_1": PLUS_ONE_COLOR, "J_{12}": J_COLOR, "s_2": PLUS_ONE_COLOR}).scale(1.2)
        formulas_group = VGroup(desc_formula, math_formula).arrange(DOWN, buff=0.4)
        
        # We use the INVISIBLE target_connection_group to define the layout
        left_panel = VGroup(target_connection_group, formulas_group).arrange(DOWN, buff=0.7)

        # C) Right Panel: Dials
        dial_config = {"x_range": [-1.5, 1.5, 0.5], "length": 3.5, "include_numbers": False, "rotation": PI/2}
        j_dial = NumberLine(**dial_config)
        j_dial.add_numbers(x_values=[-1, 0, 1], font_size=24).numbers.shift(LEFT * 0.4)
        j_dial_title = MathTex("J_{12}", color=J_COLOR).next_to(j_dial, UP)
        j_dial_group = VGroup(j_dial, j_dial.numbers, j_dial_title)
        h_dial = NumberLine(**dial_config)
        h_dial.add_numbers(x_values=[-1, 0, 1], font_size=24).numbers.shift(LEFT * 0.4)
        h_dial_title = MathTex("H", color=H_COLOR).next_to(h_dial, UP)
        h_dial_group = VGroup(h_dial, h_dial.numbers, h_dial_title)
        right_panel = VGroup(j_dial_group, h_dial_group).arrange(0.9*RIGHT, buff=1)
        
        # D) Arrange the panels on screen to ensure they fit and are centered
        main_layout = VGroup(left_panel, right_panel).arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        # --- PART 2: ANIMATE IN THE CORRECT ORDER ---

        # 1. Move the original, visible diagram to its new position
        self.play(
            Transform(connection_group, target_connection_group)
        )
        self.wait(1)
        
        # 2. Bring in the dials
        self.play(Create(right_panel))
        self.wait(1)
        
        # 3. Bring in the formulas
        self.play(Write(formulas_group))
        self.wait(1)

        # --- PART 3: DEMONSTRATION WITH LIVE CALCULATION ---
        
        s1_val, s2_val, j_val = 1, 1, -1

        def get_calc_text(s1, j, s2):
            h = s1 * j * s2
            text = MathTex("H", "=", f"({s1:+})", r"\times", f"({j:+})", r"\times", f"({s2:+})", "=", f"{h:+.0f}").scale(1.1)
            text.next_to(math_formula, DOWN, buff=0.4)
            text[0].set_color(H_COLOR)
            text[2].set_color(PLUS_ONE_COLOR if s1 > 0 else MINUS_ONE_COLOR)
            text[4].set_color(J_COLOR)
            text[6].set_color(PLUS_ONE_COLOR if s2 > 0 else MINUS_ONE_COLOR)
            text[8].set_color(H_COLOR)
            return text

        # We must now reference the sub-parts of the transformed connection_group
        alice_circle = connection_group.submobjects[0].submobjects[0]
        bob_circle = connection_group.submobjects[1].submobjects[0]
        up_arrow = Arrow(DOWN*0.2, UP*0.2, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        down_arrow = Arrow(UP*0.2, DOWN*0.2, stroke_width=3, max_tip_length_to_length_ratio=0.35)
        alice_spin = up_arrow.copy().move_to(alice_circle.get_center())
        bob_spin = up_arrow.copy().move_to(bob_circle.get_center())
        
        j_dot = Dot(color=J_COLOR, radius=0.1).move_to(j_dial.n2p(j_val))
        h_dot = Dot(color=H_COLOR, radius=0.1).move_to(h_dial.n2p(s1_val * j_val * s2_val))
        calculation_text = get_calc_text(s1_val, j_val, s2_val)

        self.play(
            Create(alice_spin), Create(bob_spin),
            alice_circle.animate.set_color(PLUS_ONE_COLOR),
            bob_circle.animate.set_color(PLUS_ONE_COLOR),
            FadeIn(j_dot), FadeIn(h_dot),
            Write(calculation_text)
        )
        self.wait(2)
        # (The rest of the demonstration remains the same)
        s2_val = -1
        new_calc = get_calc_text(s1_val, j_val, s2_val)
        new_bob_spin = down_arrow.copy().move_to(bob_circle.get_center())
        self.play(
            bob_circle.animate.set_color(MINUS_ONE_COLOR),
            Transform(bob_spin, new_bob_spin),
            h_dot.animate.move_to(h_dial.n2p(s1_val * j_val * s2_val)),
            FadeToColor(math_formula[4], MINUS_ONE_COLOR),
            desc_bob_choice.animate.set_color(MINUS_ONE_COLOR), 
            Transform(calculation_text, new_calc), run_time=1.5
        )
        self.wait(2)

        j_val = 1
        new_calc = get_calc_text(s1_val, j_val, s2_val)
        self.play(
            j_dot.animate.move_to(j_dial.n2p(j_val)),
            h_dot.animate.move_to(h_dial.n2p(s1_val * j_val * s2_val)),
            Transform(calculation_text, new_calc), run_time=1.5
        )
        self.wait(2)

        s2_val = 1
        new_calc = get_calc_text(s1_val, j_val, s2_val)
        new_bob_spin_up = up_arrow.copy().move_to(bob_circle.get_center())
        self.play(
            bob_circle.animate.set_color(PLUS_ONE_COLOR),
            Transform(bob_spin, new_bob_spin_up),
            h_dot.animate.move_to(h_dial.n2p(s1_val * j_val * s2_val)),
            FadeToColor(math_formula[4], PLUS_ONE_COLOR),
            desc_bob_choice.animate.set_color(PLUS_ONE_COLOR),
            Transform(calculation_text, new_calc), run_time=1.5
        )
        self.wait(3)

        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: FINDING THE GROUND STATE (CORRECTED DIAGRAM) ---
        
        # --- PART 1: CLEANUP AND RECAP ---
        
        all_previous_mobjects = VGroup(
            connection_group, right_panel, formulas_group,
            calculation_text, alice_spin, bob_spin, j_dot, h_dot
        )
        self.play(FadeOut(all_previous_mobjects))
        self.wait(0.5)

        DEFAULT_FONT_SIZE = 32
        recap_text = MarkupText(
            "The 'Conflict' depends on their choices and the 'Tension' between them.",
            font_size=DEFAULT_FONT_SIZE
        )
        self.play(Write(recap_text))
        self.wait(2)

        # --- PART 2: POSE THE QUESTION ---

        question_text_1 = Text("Now, let's assume the tension J is fixed.", font_size=DEFAULT_FONT_SIZE)
        question_text_2 = MarkupText(f'The question is: what choices will they make to <span color="{H_COLOR}">minimize the conflict</span>?', font_size=DEFAULT_FONT_SIZE)
        question_text_3 = MarkupText(f'This lowest-energy state is called the <span color="{YELLOW}">ground state</span>.', font_size=DEFAULT_FONT_SIZE)
        question_group = VGroup(question_text_1, question_text_2, question_text_3).arrange(DOWN, buff=0.4)

        self.play(ReplacementTransform(recap_text, question_group))
        self.wait(4)
        self.play(FadeOut(question_group))
        self.wait(0.5)

        # --- PART 3: THE INTERACTIVE TABLE (REWRITTEN WITH CORRECT BUFFERS AND SPACING) ---

        # A) Setup the main components
        case_label = MathTex("J_{12}", "=", "?").scale(1.5).to_edge(UP, buff=1.0)

        table = MathTable(
            [["+1","+1",""],["+1","-1",""],["-1","+1",""],["-1","-1",""]],
            col_labels=[MathTex("s_1"), MathTex("s_2"), MathTex("H", color=H_COLOR)],
            include_outer_lines=True
        ).scale(0.9).next_to(case_label, DOWN, buff=0.7)

        # Helper function to create the s_gs vector display
        def create_gs_vector(s1, s2):
            s_gs_label = MathTex("s_{gs}", "=").set_color(YELLOW)
            s1_val_text = MathTex(f"{s1:+}").set_color(WHITE)
            s2_val_text = MathTex(f"{s2:+}").set_color(WHITE)
            
            vector_body = VGroup(
                MathTex("["), s1_val_text, s2_val_text, MathTex("]")
            ).arrange(RIGHT, buff=0.25)
            
            full_vector = VGroup(s_gs_label, vector_body).arrange(RIGHT, buff=0.3)
            return full_vector

        # B) Animate the appearance of the tools
        self.play(Write(case_label))
        self.play(Create(table))
        self.wait(1)

        # C) Case 1: J = -1 ("Cozy")
        j_val_cozy = -1
        new_case_label_cozy = MathTex("J_{12}", "=", f"{j_val_cozy}").scale(1.5).move_to(case_label)
        new_case_label_cozy[0].set_color(J_COLOR)
        new_case_label_cozy[2].set_color(PLUS_ONE_COLOR)
        
        s1_vals = [int(c.get_tex_string()) for c in table.get_columns()[0][1:]]
        s2_vals = [int(c.get_tex_string()) for c in table.get_columns()[1][1:]]
        h_col_data_cozy = VGroup(*[MathTex(f"{j_val_cozy * s1 * s2}", color=H_COLOR) for s1, s2 in zip(s1_vals, s2_vals)]).scale(0.9)
        for i, item in enumerate(h_col_data_cozy):
            item.move_to(table.get_cell((i+2, 3)))

        self.play(Transform(case_label, new_case_label_cozy))
        self.play(Write(h_col_data_cozy))
        self.wait(1)
        
        # Point to the first ground state with correct spacing
        gs1_row = table.get_rows()[1]
        gs_vector_display = create_gs_vector(1, 1).next_to(gs1_row, LEFT, buff=1.5)
        pointer = Arrow(
            start=gs_vector_display.get_right() + RIGHT * 0.4, # Add gap on the left
            end=gs1_row.get_left() + LEFT * 0.1,             # Add gap on the right
            color=YELLOW
        )

        self.play(Write(gs_vector_display), GrowArrow(pointer))
        self.wait(2)

        # Move to the second ground state
        gs2_row = table.get_rows()[4]
        target_vector = create_gs_vector(-1, -1).next_to(gs2_row, LEFT, buff=1.5)
        target_pointer = Arrow(
            start=target_vector.get_right() + RIGHT * 0.4, # Add gap on the left
            end=gs2_row.get_left() + LEFT * 0.1,             # Add gap on the right
            color=YELLOW
        )

        self.play(
            Transform(pointer, target_pointer),
            Transform(gs_vector_display, target_vector)
        )
        self.wait(2)

        # D) Case 2: J = +1 ("Tense")
        self.play(FadeOut(pointer), FadeOut(gs_vector_display))
        j_val_tense = 1
        new_case_label_tense = MathTex("J_{12}", "=", f"+{j_val_tense}").scale(1.5).move_to(case_label)
        new_case_label_tense[0].set_color(J_COLOR)
        new_case_label_tense[2].set_color(MINUS_ONE_COLOR)
        
        h_col_data_tense = VGroup(*[MathTex(f"{j_val_tense * s1 * s2}", color=H_COLOR) for s1, s2 in zip(s1_vals, s2_vals)]).scale(0.9)
        for i, item in enumerate(h_col_data_tense):
            item.move_to(table.get_cell((i+2, 3)))

        self.play(
            Transform(case_label, new_case_label_tense),
            Transform(h_col_data_cozy, h_col_data_tense),
            run_time=1.5
        )
        self.wait(1)

        # Point to the new ground states with correct spacing
        gs1_row_new = table.get_rows()[2]
        gs_vector_display = create_gs_vector(1, -1).next_to(gs1_row_new, LEFT, buff=1.5)
        pointer = Arrow(
            start=gs_vector_display.get_right() + RIGHT * 0.4, # Add gap on the left
            end=gs1_row_new.get_left() + LEFT * 0.1,             # Add gap on the right
            color=YELLOW
        )
        
        self.play(Write(gs_vector_display), GrowArrow(pointer))
        self.wait(2)
        
        gs2_row_new = table.get_rows()[3]
        target_vector = create_gs_vector(-1, 1).next_to(gs2_row_new, LEFT, buff=1.5)
        target_pointer = Arrow(
            start=target_vector.get_right() + RIGHT * 0.4, # Add gap on the left
            end=gs2_row_new.get_left() + LEFT * 0.1,             # Add gap on the right
            color=YELLOW
        )

        self.play(
            Transform(pointer, target_pointer),
            Transform(gs_vector_display, target_vector)
        )
        self.wait(3)

        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: THREE PEOPLE (FINAL POLISHED VERSION) ---
        
        # 1. Clean up all elements from the previous scene
        all_table_elements = VGroup(case_label, table, h_col_data_cozy, pointer, gs_vector_display)
        self.play(FadeOut(all_table_elements))
        self.wait(0.5)

        # 2. Pose the question
        question_text = Text("You might wonder... what happens with three people?", font_size=36)
        self.play(Write(question_text))
        self.wait(2)
        self.play(FadeOut(question_text))
        self.wait(0.5)

        # 3. Define helper functions with corrected, robust logic
        node_radius = 0.3

        def create_person(name, position):
            circle = Circle(radius=node_radius, color=WHITE, fill_opacity=0.8)
            text_name = Text(name, font_size=36).next_to(circle, DOWN, buff=0.2)
            # Ensure names are drawn on top of lines
            text_name.set_z_index(2)
            # Add a background to prevent lines from cutting through the text
            text_name.add_background_rectangle(opacity=1, buff=0.05)
            return VGroup(circle, text_name).move_to(position)

        def create_connection(node1, node2, label_text):
            circle1 = node1.submobjects[0]
            circle2 = node2.submobjects[0]
            p1, p2 = circle1.get_center(), circle2.get_center()
            direction_vector = p2 - p1
            unit_direction = direction_vector / np.linalg.norm(direction_vector)
            line = Line(p1 + unit_direction * node_radius, p2 - unit_direction * node_radius, z_index=-1, color=TEAL, stroke_width=3)
            label = MathTex(label_text, color=J_COLOR).scale(1.2)
            label.move_to(line.get_center())
            line_angle = line.get_angle()
            label.rotate(line_angle)
            if (PI / 2) < abs(line_angle) < (3 * PI / 2):
                label.rotate(PI)
            label.add_background_rectangle(opacity=1, buff=0.1)
            return VGroup(line, label)

        # 4. Define the nodes in a triangle layout
        alice_node = create_person("Alice", UP * 2.2)
        bob_node = create_person("Bob", DOWN * 1.5 + LEFT * 2.5)
        charlie_node = create_person("Charlie", DOWN * 1.5 + RIGHT * 2.5)
        
        all_nodes = VGroup(alice_node, bob_node, charlie_node)
        self.play(Create(all_nodes))
        self.wait(1)

        # 5. Define and animate the connections using the new, smooth technique
        connection_12 = create_connection(alice_node, bob_node, "J_{12}")
        connection_13 = create_connection(alice_node, charlie_node, "J_{13}")
        connection_23 = create_connection(bob_node, charlie_node, "J_{23}")

        self.play(
            LaggedStart(
                Create(connection_12),
                Create(connection_13),
                Create(connection_23),
                lag_ratio=0.6, # Start the next animation when the previous is 60% done
                run_time=3     # The entire process takes 3 seconds
            )
        )
        self.wait(3)
    
        # (This code follows immediately after the previous sequence ends)

        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: BUILDING THE HAMILTONIAN (DEFINITIVE CORRECTED VERSION) ---

        # 1. Group the entire system and move it to the left
        triangle_system = VGroup(all_nodes, connection_12, connection_13, connection_23)
        self.play(
            triangle_system.animate.scale(0.8).to_edge(LEFT, buff=1.0)
        )
        self.wait(0.5)

        # 2. Define the position for the formulas to appear on the right
        formula_pos = RIGHT * 3.0

        # 3. Create and animate the individual conflict formulas
        
        h12_formula = MathTex("H_{12}", "=", "s_1", "J_{12}", "s_2", tex_to_color_map={"H_{12}": H_COLOR, "J_{12}": J_COLOR}).scale(1.2).move_to(formula_pos)
        self.play(Write(h12_formula))
        self.wait(1.5)
        self.play(FadeOut(h12_formula))

        h13_formula = MathTex("H_{13}", "=", "s_1", "J_{13}", "s_3", tex_to_color_map={"H_{13}": H_COLOR, "J_{13}": J_COLOR}).scale(1.2).move_to(formula_pos)
        self.play(Write(h13_formula))
        self.wait(1.5)
        self.play(FadeOut(h13_formula))

        h23_formula = MathTex("H_{23}", "=", "s_2", "J_{23}", "s_3", tex_to_color_map={"H_{23}": H_COLOR, "J_{23}": J_COLOR}).scale(1.2).move_to(formula_pos)
        self.play(Write(h23_formula))
        self.wait(2)

        # 4. Reveal the total Hamiltonian in a two-line format with a title
        
        # Create each part of the equation separately
        h_total_label = MathTex("H", "=").set_color_by_tex("H", H_COLOR)
        term1 = MathTex("s_1 J_{12} s_2").set_color_by_tex("J", J_COLOR)
        plus_sign = MathTex("+").set_color(WHITE)
        term2 = MathTex("s_1 J_{13} s_3").set_color_by_tex("J", J_COLOR)
        term3 = MathTex("+ s_2 J_{23} s_3").set_color_by_tex("J", J_COLOR)
        
        # Arrange the first line
        line1 = VGroup(h_total_label, term1, plus_sign, term2).arrange(RIGHT, buff=0.2)
        
        # Position the second line (term3) aligned under the start of term1
        term3.next_to(line1, DOWN, buff=0.2, aligned_edge=LEFT)
        term3.align_to(term1, LEFT)
        
        # Group the formula parts
        full_formula = VGroup(line1, term3)
        
        # --- NEW --- Create the title and group it with the formula
        total_conflict_title = Text("Total Conflict", font_size=36)
        n3_hamiltonian_group = VGroup(total_conflict_title, full_formula).arrange(DOWN, buff=0.4)
        n3_hamiltonian_group.move_to(formula_pos)

        self.play(ReplacementTransform(h23_formula, n3_hamiltonian_group))
        self.wait(4)
        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: GENERALIZING TO N=4 AND THE SUMMATION (REVISED) ---

        # 1. Modify the connection helper to prevent label overlap
        def create_connection(node1, node2, label_text, label_pos_alpha=0.5):
            circle1 = node1.submobjects[0]
            circle2 = node2.submobjects[0]
            p1, p2 = circle1.get_center(), circle2.get_center()
            direction_vector = p2 - p1
            unit_direction = direction_vector / np.linalg.norm(direction_vector)
            
            line = Line(
                p1 + unit_direction * node_radius, 
                p2 - unit_direction * node_radius, 
                z_index=-1, color=TEAL, stroke_width=3
            )
            label = MathTex(label_text, color=J_COLOR).scale(1.2)
            label.move_to(line.point_from_proportion(label_pos_alpha))
            
            line_angle = line.get_angle()
            label.rotate(line_angle)
            if (PI / 2) < abs(line_angle) < (3 * PI / 2):
                label.rotate(PI)
            label.add_background_rectangle(opacity=1, buff=0.1)
            return VGroup(line, label)

        # 2. Prepare the N=4 system and the new Hamiltonian layout
        
        # A. Create the N=4 graph nodes
        alice_node_sq = create_person("Alice", UP * 2.0 + LEFT * 2.0)
        bob_node_sq = create_person("Bob", UP * 2.0 + RIGHT * 2.0)
        charlie_node_sq = create_person("Charlie", DOWN * 2.0 + LEFT * 2.0)
        diana_node = create_person("Diana", DOWN * 2.0 + RIGHT * 2.0)
        all_nodes_n4 = VGroup(alice_node_sq, bob_node_sq, charlie_node_sq, diana_node)

        # B. Create N=4 connections, offsetting diagonal labels to avoid overlap
        connections_n4 = VGroup(
            create_connection(alice_node_sq, bob_node_sq, "J_{12}"),
            create_connection(charlie_node_sq, diana_node, "J_{34}"),
            create_connection(alice_node_sq, charlie_node_sq, "J_{13}"),
            create_connection(bob_node_sq, diana_node, "J_{24}"),
            create_connection(alice_node_sq, diana_node, "J_{14}", label_pos_alpha=0.6), # Offset
            create_connection(bob_node_sq, charlie_node_sq, "J_{23}", label_pos_alpha=0.4)  # Offset
        )
        n4_system = VGroup(all_nodes_n4, connections_n4).scale(0.8).to_edge(LEFT, buff=1.0)
        
        # C. Define the target N=4 Hamiltonian formula with its title
        total_conflict_title_n4 = Text("Total Conflict", font_size=36)
        
        h_total_label = MathTex("H", "=").set_color_by_tex("H", H_COLOR)
        terms = [MathTex(t) for t in ["s_1 J_{12} s_2", "+ s_1 J_{13} s_3", "+ s_2 J_{23} s_3", "+ s_1 J_{14} s_4", "+ s_2 J_{24} s_4", "+ s_3 J_{34} s_4"]]
        for term in terms:
            term.set_color_by_tex("J", J_COLOR)
            
        line1_n4 = VGroup(*terms[:3]).arrange(RIGHT, buff=0.15)
        line2_n4 = VGroup(*terms[3:]).arrange(RIGHT, buff=0.15)
        
        n4_formula_terms = VGroup(line1_n4, line2_n4).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        n4_formula_body = VGroup(h_total_label, n4_formula_terms).arrange(RIGHT, buff=0.2)
        
        n4_hamiltonian_group = VGroup(total_conflict_title_n4, n4_formula_body).arrange(DOWN, buff=0.4)
        n4_hamiltonian_group.scale(0.8).move_to(RIGHT * 3.0)

        # 3. Animate the transformation from the N=3 system to the N=4 system
        all_n3_objects = VGroup(triangle_system, n3_hamiltonian_group)
        
        self.play(
            ReplacementTransform(all_n3_objects, VGroup(n4_system, n4_hamiltonian_group)),
            run_time=2.5
        )
        self.wait(3)

        # 4. Reveal the final, general formula
        summation_formula = MathTex(r"H = \sum_{i<j} s_i J_{ij} s_j", font_size=60)
        summation_formula.set_color_by_tex_to_color_map({
            "H": H_COLOR,
            "J_{ij}": J_COLOR
        })
        summation_formula.move_to(n4_hamiltonian_group.get_center())

        self.play(
            ReplacementTransform(n4_hamiltonian_group, summation_formula),
            n4_system.animate.fade(0.7)
        )
        self.wait(5)

        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: THE MATRIX FORMULATION ---

        # 1. Clean up the scene, leaving only the summation formula
        self.play(
            FadeOut(n4_system),
            summation_formula.animate.move_to(ORIGIN).scale(1.2)
        )
        self.wait(1)

        # 2. Define the components: s_i and J
        s_i_def = MathTex(r"s_i \in \{+1, -1\}", font_size=36)
        j_matrix_def = MarkupText(
            f'J is an <span color="{J_COLOR}">N × N</span> matrix of tensions', 
            font_size=36
        )
        
        definitions_group = VGroup(s_i_def, j_matrix_def).arrange(DOWN, buff=0.5)
        definitions_group.next_to(summation_formula, DOWN, buff=1.0)
        
        self.play(Write(definitions_group))
        self.wait(3)

        # 3. Introduce the symmetry argument
        symmetry_text = MarkupText(
            f'In the real world, the tension is mutual: <span color="{YELLOW}">J<sub>ij</sub> = J<sub>ji</sub></span>',
            font_size=42
        )
        symmetry_text.move_to(definitions_group)

        self.play(ReplacementTransform(definitions_group, symmetry_text))
        self.wait(3)

        # 4. Rewrite the formula into its final matrix-ready form
        final_formula = MathTex(r"H = \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} s_i J_{ij} s_j", font_size=60)
        final_formula.set_color_by_tex_to_color_map({
            "H": H_COLOR,
            "J_{ij}": J_COLOR
        })
        final_formula.move_to(summation_formula)

        n_explanation = MarkupText(
            "where N is the number of people (spins)", 
            font_size=32
        ).next_to(final_formula, DOWN, buff=0.7)

        self.play(
            ReplacementTransform(summation_formula, final_formula),
            ReplacementTransform(symmetry_text, n_explanation),
            run_time=2
        )
        self.wait(5)

        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: THE MATRIX-VECTOR FORM (REVISED LAYOUT) ---

        # 1. Clean up the explanation text
        self.play(FadeOut(n_explanation))
        self.wait(0.5)

        # 2. Transform the summation formula into the compact matrix form
        sTJs_formula = MathTex(r"H = \frac{1}{2} \mathbf{s}^T \mathbf{J} \mathbf{s}", font_size=60)
        sTJs_formula.set_color_by_tex_to_color_map({
            "H": H_COLOR,
            r"\mathbf{J}": J_COLOR,
            r"\mathbf{s}": PLUS_ONE_COLOR
        })
        sTJs_formula.move_to(final_formula)

        self.play(ReplacementTransform(final_formula, sTJs_formula))
        self.wait(2)

        # 3. Animate the main formula moving up to become a "title" for the explanation
        self.play(
            sTJs_formula.animate.scale(0.8).to_edge(UP, buff=1.0)
        )
        self.wait(0.5)

        # 4. Show what s^T J s means visually in the newly cleared space
        
        # --- THIS IS THE FIX ---
        # A. Create the components for s^T, J, and s more robustly
        s1_tex = MathTex("s_1")
        s2_tex = MathTex("s_2")
        dots_tex = MathTex(r"\dots")
        sN_tex = MathTex("s_N")
        s_T_vec = VGroup(
            MathTex("["), s1_tex, s2_tex, dots_tex, sN_tex, MathTex("]")
        ).arrange(RIGHT, buff=0.2).set_color(PLUS_ONE_COLOR)
        
        j_matrix = Matrix(
            [[r"J_{11}", r"J_{12}", r"\dots", r"J_{1N}"],
             [r"J_{21}", r"J_{22}", r"\dots", r"J_{2N}"],
             [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
             [r"J_{N1}", r"J_{N2}", r"\dots", r"J_{NN}"]],
            h_buff=1.2, v_buff=0.7, bracket_h_buff=0.2
        ).set_color(J_COLOR)
        
        s_vec = Matrix(
            [[r"s_1"], [r"s_2"], [r"\vdots"], [r"s_N"]]
        ).set_color(PLUS_ONE_COLOR)
        
        one_half = MathTex(r"\frac{1}{2}")

        # B. Group and arrange them in the center of the screen
        expanded_form = VGroup(one_half, s_T_vec, j_matrix, s_vec).arrange(RIGHT, buff=0.25)
        expanded_form.scale(0.8).move_to(ORIGIN)

        # C. Animate their appearance
        self.play(
            LaggedStart(
                Write(one_half),
                Write(s_T_vec),
                Create(j_matrix),
                Write(s_vec),
                lag_ratio=0.5
            )
        )
        self.wait(5)

        # (This code follows immediately after the previous sequence ends)

        # --- NEW SEQUENCE: THE COMPLEXITY OF FINDING THE GROUND STATE (POLISHED VERSION) ---

        # --- PART 1: Posing the Problem (The "Brute-Force" Approach) ---

        # 1. Cleanup and focus on the spin vector
        self.play(
            FadeOut(one_half, j_matrix, s_vec), # Fade out everything except s^T vector and title
            sTJs_formula.animate.fade(0.5)      # Dim the title
        )
        # s_T_vec is the horizontal vector from the previous scene
        
        # FIX: Add the "s^T =" label to the vector
        s_T_label = MathTex(r"\mathbf{s}^T =").scale(1.5).set_color(PLUS_ONE_COLOR)
        labeled_s_vector = VGroup(s_T_label, s_T_vec).arrange(RIGHT, buff=0.25)

        self.play(labeled_s_vector.animate.move_to(ORIGIN))
        self.wait(1)

        # 2. Pose the question
        # FIX: Reduce font size and justify text to prevent overflow
        question = MarkupText(
            "To find the ground state, which configuration of spins minimizes H?",
            font_size=32,
            justify=True
        ).next_to(labeled_s_vector, UP, buff=1.0)
        self.play(Write(question))
        self.wait(2)

        # 3. Count the choices for each spin
        s1 = s_T_vec.submobjects[1]
        s2 = s_T_vec.submobjects[2]
        sN = s_T_vec.submobjects[4]

        # FIX: Increase buff for a slightly larger highlight box
        highlight_box = SurroundingRectangle(s1, color=YELLOW, buff=0.15)
        choices_text = MarkupText("2 choices (+1 or –1)", font_size=28).next_to(labeled_s_vector, DOWN, buff=0.7)
        self.play(Create(highlight_box), Write(choices_text))
        self.wait(1)

        self.play(highlight_box.animate.move_to(s2))
        self.wait(0.5)
        self.play(highlight_box.animate.move_to(sN))
        self.wait(1)

        # 4. Build the 2^N formula from the choices
        multiplication_text = MathTex("2 \\times 2 \\times \\dots \\times 2", font_size=48)
        n_times_label = MathTex("(N \\text{ times})", font_size=36).next_to(multiplication_text, DOWN)
        multiplication_group = VGroup(multiplication_text, n_times_label).move_to(choices_text.get_center())
        
        self.play(ReplacementTransform(choices_text, multiplication_group))
        self.wait(2)

        # FIX: Use MathTex with \text{} to ensure proper spacing
        final_configs_formula = MathTex(r"\text{Total Configurations} = 2^N", font_size=48)
        final_configs_formula.move_to(multiplication_group.get_center())
        
        self.play(
            ReplacementTransform(multiplication_group, final_configs_formula),
            FadeOut(question, labeled_s_vector, highlight_box, sTJs_formula)
        )
        self.wait(1)

        # --- PART 2: Visualizing Exponential Growth (Linear Scale) ---

        # 1. Set the stage for the graph
        self.play(final_configs_formula.animate.scale(0.7).to_edge(UP, buff=0.5))
        
        # FIX: Use a linear scale, we will move the graph to keep the dot in view.
        ax = Axes(
            x_range=[0, 32, 5],
            y_range=[0, 40, 10], # Start with a small, manageable y-range
            x_length=10,
            y_length=5.5, # Make y-axis a bit shorter to give more vertical room
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(0, 31, 5)},
        )

        x_label = ax.get_x_axis_label("N \\text{ (Number of People)}")
        y_label = ax.get_y_axis_label("\\text{Configurations}", edge=LEFT, direction=UP)
        y_label.next_to(ax.y_axis, UP, buff=0.2)
        
        # FIX: Group everything and scale it down slightly to fit well
        graph_group = VGroup(ax, x_label, y_label).scale(0.95).move_to(ORIGIN)
        self.play(Create(graph_group))
        self.wait(1)

        # 2. Plot the curve and animate its explosive growth
        tracker = ValueTracker(2)
        
        # Create a graph that will be updated
        graph = ax.plot(lambda x: 2**x, color=WHITE, x_range=[0,2])

        # Create a dot that tracks the end of the graph
        dot = Dot(color=YELLOW).move_to(graph.get_end())
        
        # Create a label for the dot
        label = always_redraw(lambda: 
            MathTex(f"2^{{{int(tracker.get_value())}}} = {int(2**tracker.get_value()):,}")
            .scale(0.7).next_to(dot, UR, buff=0.1)
        )

        self.play(Create(graph), FadeIn(dot), FadeIn(label))
        self.wait(1)

        # Animate to N=5
        self.play(
            tracker.animate.set_value(5),
            UpdateFromFunc(graph, lambda m: m.become(ax.plot(lambda x: 2**x, color=WHITE, x_range=[0, 5]))),
            UpdateFromFunc(dot, lambda m: m.move_to(ax.c2p(5, 2**5))),
            run_time=2
        )
        self.wait(1)
        
        # Animate to N=10, moving the graph down to keep the dot in frame
        self.play(
            tracker.animate.set_value(10),
            UpdateFromFunc(graph, lambda m: m.become(ax.plot(lambda x: 2**x, color=WHITE, x_range=[0, 10]))),
            # Animate the dot and the entire graph group simultaneously
            dot.animate.move_to(ax.c2p(10, 2**10)),
            graph_group.animate.shift(DOWN * 3),
            run_time=3
        )
        self.wait(1)
        
        # Animate to N=30, showing the massive jump
        self.play(
            tracker.animate.set_value(30),
            # We don't need to draw the full graph, just move the dot to its final position
            # while the graph scrolls away, creating a sense of immense scale.
            dot.animate.move_to(ax.c2p(30, 2**30)), 
            graph_group.animate.shift(DOWN * 20), # Move graph way off-screen
            run_time=4
        )
        self.wait(2)


        # --- PART 3: The "Impossible" Punchline ---
        
        # 1. Clean up the graph elements
        self.play(
            FadeOut(graph_group, dot, label, graph, final_configs_formula)
        )
        self.wait(0.5)

        # 2. Show the N=300 case
        n300_text = MathTex("N = 300", font_size=72)
        self.play(Write(n300_text))
        self.wait(1)

        # 3. Create the punchline text
        line1 = MarkupText(
            "For just 300 people, the number of configurations (2<sup>300</sup>)...", 
            font_size=36
        )
        
        # --- THIS IS THE FIX ---
        # Create each line of the final sentence as a separate object
        line2a = MarkupText(
            "is greater than the number of atoms", 
            font_size=42, color=YELLOW
        )
        line2b = MarkupText(
            "in the known universe.",
            font_size=42, color=YELLOW
        )
        # Arrange them in a VGroup, which will center them by default
        line2_group = VGroup(line2a, line2b).arrange(DOWN, buff=0.2)
        
        # Group the entire punchline for positioning
        punchline = VGroup(line1, line2_group).arrange(DOWN, buff=0.5)
        
        # 4. Animate the final text
        self.play(
            n300_text.animate.next_to(punchline, UP, buff=0.7)
        )
        self.play(Write(line1))
        self.wait(1.5)
        # Write the two-line group together
        self.play(Write(line2_group))
        self.wait(5)


class LinkToNPHardness(Scene):
    def construct(self):
        # --- CONFIGURATION (from previous scene) ---
        PLUS_ONE_COLOR = BLUE_D
        MINUS_ONE_COLOR = RED_D
        TEXT_COLOR = YELLOW
        J_COLOR = YELLOW
        H_COLOR = GREEN
        
        # --- SEQUENCE 1: INTRO AND WHY WE CARE ---
        
        title_text = MarkupText(
            'Why is this <span color="YELLOW">Ising Problem</span> important?',
            font_size=42
        )
        subtitle_text = MarkupText(
            "It's a <span color='TEAL'>universal puzzle</span> that describes many other hard problems.",
            font_size=36
        ).next_to(title_text, DOWN, buff=0.4)

        self.play(Write(title_text))
        self.wait(2)
        self.play(Write(subtitle_text))
        self.wait(3)
        self.play(FadeOut(title_text, subtitle_text))
        self.wait(0.5)

        # --- SEQUENCE 2: THE NUMBER PARTITIONING PROBLEM ---
        
        problem_title = Text("The Number Partitioning Problem", font_size=38).to_edge(UP)
        self.play(Write(problem_title))
        self.wait(1)

        numbers_list = [8, 7, 6, 5]
        numbers_tex = VGroup(*[MathTex(str(n)) for n in numbers_list]).arrange(RIGHT, buff=0.8).scale(0.9)
        self.play(Write(numbers_tex))
        self.wait(2)

        # --- FIX #1: Move numbers up to make space for the bins ---
        self.play(numbers_tex.animate.to_edge(UP, buff=2.0))
        self.wait(0.5)

        bin_A = RoundedRectangle(width=3, height=2, corner_radius=0.2, color=BLUE).to_edge(LEFT, buff=1.5)
        bin_B = RoundedRectangle(width=3, height=2, corner_radius=0.2, color=RED).to_edge(RIGHT, buff=1.5)
        bin_A_label = Text("Group A").next_to(bin_A, UP)
        bin_B_label = Text("Group B").next_to(bin_B, UP)

        self.play(Create(bin_A), Create(bin_B), Write(bin_A_label), Write(bin_B_label))
        self.wait(1)

        sum_A = Integer(0, color=BLUE).scale(1.5).next_to(bin_A, DOWN, buff=0.3)
        sum_B = Integer(0, color=RED).scale(1.5).next_to(bin_B, DOWN, buff=0.3)
        self.play(Write(sum_A), Write(sum_B))

        # Re-get the numbers from the VGroup for animation
        num8, num7, num6, num5 = numbers_tex
        self.play(
            num8.animate.move_to(bin_A.get_center() + LEFT*0.5),
            num5.animate.move_to(bin_A.get_center() + RIGHT*0.5),
            num7.animate.move_to(bin_B.get_center() + LEFT*0.5),
            num6.animate.move_to(bin_B.get_center() + RIGHT*0.5),
        )
        self.play(sum_A.animate.set_value(13), sum_B.animate.set_value(13))

        equals_sign = MathTex("=", color=GREEN).scale(2).move_to(ORIGIN)
        checkmark = MathTex(r"\checkmark", color=GREEN).scale(3).next_to(equals_sign, RIGHT, buff=0.5)
        
        self.play(Write(equals_sign), Write(checkmark))
        self.wait(3)

        # --- SEQUENCE 3: MAPPING TO SPINS ---

        all_partition_elements = VGroup(
            problem_title, numbers_tex, bin_A, bin_B, bin_A_label,
            bin_B_label, sum_A, sum_B, equals_sign, checkmark
        )
        self.play(FadeOut(all_partition_elements))
        self.wait(0.5)

        numbers_tex_centered = VGroup(*[MathTex(str(n)) for n in numbers_list]).arrange(RIGHT, buff=1.5).scale(1.8)
        self.play(Write(numbers_tex_centered))
        
        spins_tex = VGroup(
            MathTex("+1", color=PLUS_ONE_COLOR), MathTex("-1", color=MINUS_ONE_COLOR),
            MathTex("-1", color=MINUS_ONE_COLOR), MathTex("+1", color=PLUS_ONE_COLOR)
        ).scale(1.5)

        for i, spin in enumerate(spins_tex):
            spin.next_to(numbers_tex_centered[i], DOWN, buff=0.5)

        self.play(Write(spins_tex))
        self.wait(3)

        calc_sum = MathTex(
            r"(+1)\times 8", r"+ (-1)\times 7", r"+ (-1)\times 6", r"+ (+1)\times 5", r" = 0"
        ).scale(1.2).next_to(numbers_tex_centered, DOWN, buff=1.5)
        
        self.play(LaggedStart(*[Write(part) for part in calc_sum], lag_ratio=0.5, run_time=3))
        self.wait(3)

        goal_formula = MathTex(r"\text{Goal: Find } s_i \text{ such that } \sum_i s_i a_i = 0", font_size=48)
        goal_formula.to_edge(DOWN)
        
        self.play(ReplacementTransform(calc_sum, goal_formula))
        self.wait(3)

        # --- SEQUENCE 4: THE CONNECTION TO HAMILTONIAN ---

        all_prev_elements = VGroup(numbers_tex_centered, spins_tex)
        self.play(FadeOut(all_prev_elements), goal_formula.animate.move_to(ORIGIN))
        self.wait(1)

        squared_sum = MathTex(r"\left( \sum_i s_i a_i \right)^2", font_size=60)
        self.play(ReplacementTransform(goal_formula, squared_sum))
        self.wait(2)

        # --- FIX #2: Re-layout the long formula to prevent clipping ---
        self.play(squared_sum.animate.to_edge(UP, buff=1.0))
        
        expanded_term1 = MathTex(r"= \sum_i (a_i)^2", font_size=60)
        expanded_term2 = MathTex(r"+ \sum_{i \neq j}", r"a_i a_j", r"s_i s_j", font_size=60)
        expanded_form = VGroup(expanded_term1, expanded_term2).arrange(RIGHT, buff=0.2)
        expanded_form.next_to(squared_sum, DOWN, buff=0.5)

        self.play(Write(expanded_form))
        self.wait(2)

        const_part = expanded_form[0]
        const_label = Text("CONSTANT", color=YELLOW, font_size=32).next_to(const_part, DOWN)
        self.play(Write(const_label))
        self.wait(2)

        variable_part = expanded_form[1]
        self.play(
            FadeOut(const_part, const_label, squared_sum),
            variable_part.animate.move_to(ORIGIN).scale(0.9)
        )
        self.wait(2)
        
        hamiltonian = MathTex(r"H = \sum_{i<j}", r"J_{ij}", r"s_i s_j", font_size=60)
        hamiltonian.set_color_by_tex_to_color_map({"H": H_COLOR, "J_{ij}": J_COLOR})
        hamiltonian.next_to(variable_part, UP, buff=1.0)
        self.play(Write(hamiltonian))
        self.wait(2)

        rect1 = SurroundingRectangle(variable_part[1], color=ORANGE)
        rect2 = SurroundingRectangle(hamiltonian[1], color=ORANGE)
        
        equivalence_map = MathTex(r"J_{ij} = a_i a_j", color=YELLOW, font_size=60)
        equivalence_map.next_to(variable_part, DOWN, buff=1.0)

        self.play(Create(rect1), Create(rect2))
        self.wait(1)
        self.play(Write(equivalence_map))
        self.wait(4)

        self.play(
            FadeOut(variable_part, hamiltonian, rect1, rect2, equivalence_map)
        )
        self.wait(0.5)
        
        # --- FIX #3: Adjust box width and text size to fit properly ---
        box1 = RoundedRectangle(height=1.5, width=4.5, corner_radius=0.2, color=TEAL)
        # Reduce font size to prevent overflow
        text1 = Text("Number Partitioning", font_size=32).move_to(box1.get_center()) 
        problem1 = VGroup(box1, text1)

        box2 = RoundedRectangle(height=1.5, width=4.5, corner_radius=0.2, color=H_COLOR)
        # Reduce font size to prevent overflow
        text2 = Text("Ising Ground State", font_size=32).move_to(box2.get_center()) 
        problem2 = VGroup(box2, text2)

        problems = VGroup(problem1, problem2).arrange(RIGHT, buff=2.0)
        
        arrow = Arrow(problem1.get_right(), problem2.get_left(), buff=0.2, color=YELLOW)
        arrow_text = Text("is equivalent to").next_to(arrow, 2.7*UP)

        self.play(FadeIn(problem1))
        self.wait(1)
        self.play(GrowArrow(arrow), Write(arrow_text))
        self.wait(1)
        self.play(ReplacementTransform(problem1.copy(), problem2))
        self.wait(5)

        # --- NEW SEQUENCE: THE ROGUES' GALLERY (FINAL POLISHED VERSION) ---

        # 1. Define a consistent helper function for creating problem boxes
        def create_problem_box(text, color, height=1.3, width=4.0):
            box = RoundedRectangle(height=height, width=width, corner_radius=0.2, color=color)
            # This ensures the text always fits nicely inside the box
            label = Text(text, font_size=36).scale_to_fit_width(width * 0.85)
            label.move_to(box.get_center())
            return VGroup(box, label)

        # 2. Define the FINAL state of all objects for the smooth transition
        
        # A. The new, slightly larger central hub
        central_hub_final = create_problem_box("Ising Ground State", H_COLOR, height=1.5, width=5.2)
        central_hub_final.move_to(ORIGIN) # Place the final hub at the center

        # B. The final position and look of the Number Partitioning box
        np_box_final = create_problem_box("Number Partitioning", TEAL)
        np_box_final.move_to(central_hub_final.get_center() + DOWN * 2.2 + LEFT * 3.5)

        # C. The final arrow connecting them, based on their final positions
        np_arrow_final = Arrow(
            np_box_final.get_top(), central_hub_final.get_corner(DL),
            buff=0.2, color=YELLOW
        )

        # 3. Perform the main transition in ONE smooth animation
        # We transform the old objects (problem1, problem2, arrow) into their new final versions.
        # This handles moving, resizing, and reshaping all at once.
        self.play(
            FadeOut(arrow_text),
            Transform(problem1, np_box_final),       # The old NP box becomes the new one
            Transform(problem2, central_hub_final),  # The old Ising box becomes the new hub
            Transform(arrow, np_arrow_final),        # The old arrow becomes the new, correctly angled one
            run_time=2.0
        )
        self.wait(1)

        # 4. Sequentially introduce the other problems, now that the scene is set
        
        # Get the final objects from the Transform to use as references
        central_hub = problem2
        np_box = problem1
        
        # Max-Cut
        max_cut_box = create_problem_box("Max-Cut", PURPLE)
        max_cut_box.move_to(central_hub.get_center() + UP * 2.2 + LEFT * 3.5)
        max_cut_arrow = Arrow(max_cut_box.get_bottom(), central_hub.get_corner(UL), buff=0.2, color=YELLOW)
        self.play(FadeIn(max_cut_box))
        self.play(GrowArrow(max_cut_arrow))
        self.wait(2.5)

        # Traveling Salesman
        tsp_box = create_problem_box("Traveling Salesman", MAROON_B)
        tsp_box.move_to(central_hub.get_center() + UP * 2.2 + RIGHT * 3.5)
        tsp_arrow = Arrow(tsp_box.get_bottom(), central_hub.get_corner(UR), buff=0.2, color=YELLOW)
        self.play(FadeIn(tsp_box))
        self.play(GrowArrow(tsp_arrow))
        self.wait(2.5)

        # ksat
        ksat_box = create_problem_box("k-SAT", GOLD_D)
        ksat_box.move_to(central_hub.get_center() + DOWN * 2.2 + RIGHT * 3.5)
        ksat_arrow = Arrow(ksat_box.get_top(), central_hub.get_corner(DR), buff=0.2, color=YELLOW)
        self.play(FadeIn(ksat_box))
        self.play(GrowArrow(ksat_arrow))
        self.wait(2.5)
        
        # 5. Final shot - group everything for a clean end frame
        
        all_problems_group = VGroup(
            central_hub,
            np_box, arrow, # The NP box and its arrow are already grouped from the transform
            max_cut_box, max_cut_arrow,
            tsp_box, tsp_arrow,
            ksat_box, ksat_arrow
        )
        
        # A final small adjustment to ensure the whole composition is perfectly centered
        self.play(all_problems_group.animate.move_to(ORIGIN))
        self.wait(5)
    
        # (This code follows immediately after the final zoom-out of the problems group)

        # --- NEW SEQUENCE: THE ESSENCE OF THE ISING PROBLEM ---

        # 1. Clean up the screen
        self.play(FadeOut(all_problems_group))
        self.wait(0.5)

        # 2. Define the positions for the formula and the graph
        formula_pos = UP * 2.5
        graph_pos = DOWN * 0.5

        # 3. Create and place the Hamiltonian formula first
        hamiltonian_essence = MathTex(r"H = \sum_{i<j} J_{ij} s_i s_j", font_size=72)
        hamiltonian_essence.set_color_by_tex_to_color_map({"H": H_COLOR, "J_{ij}": J_COLOR})
        hamiltonian_essence.move_to(formula_pos)
        
        self.play(Write(hamiltonian_essence))
        self.wait(2)

        # 4. Create a generic, complex-looking graph below the formula
        num_nodes = 20
        nodes = VGroup(*[
            Dot(color=WHITE) for _ in range(num_nodes)
        ])
        # Arrange in a grid with some randomness
        nodes.arrange_in_grid(4, 5, buff=1.2).scale(0.7)
        nodes.rotate(PI/6)
        for node in nodes:
            node.shift(
                (random.random() - 0.5) * 0.4 * RIGHT + 
                (random.random() - 0.5) * 0.4 * UP
            )

        lines = VGroup()
        # Use itertools.combinations to avoid duplicate edges and self-loops
        all_possible_pairs = list(itertools.combinations(range(num_nodes), 2))
        # Select a random subset of these pairs to form the edges
        num_edges = int(num_nodes * 1.5) # A reasonable number of edges
        selected_pairs = random.sample(all_possible_pairs, num_edges)
        for pair in selected_pairs:
            lines.add(Line(nodes[pair[0]].get_center(), nodes[pair[1]].get_center(), stroke_width=2, color=GRAY, z_index=-1))
        
        graph_system = VGroup(lines, nodes).move_to(graph_pos)

        self.play(Create(graph_system))
        self.wait(2)

        # 5. Animate the "flickering" search for the ground state
        flicker_duration = 0.15 # Slightly faster flicker
        for _ in range(12): # Flicker a bit more
            new_colors = [random.choice([PLUS_ONE_COLOR, MINUS_ONE_COLOR]) for _ in range(num_nodes)]
            self.play(
                *[nodes[i].animate.set_color(new_colors[i]) for i in range(num_nodes)],
                run_time=flicker_duration
            )
        
        # Settle into a final state
        final_colors = [random.choice([PLUS_ONE_COLOR, MINUS_ONE_COLOR]) for _ in range(num_nodes)]
        self.play(
            *[nodes[i].animate.set_color(final_colors[i]) for i in range(num_nodes)],
            run_time=0.5
        )

        # Highlight the minimized Hamiltonian
        self.play(Indicate(hamiltonian_essence, color=H_COLOR, scale_factor=1.1))
        self.wait(3)

        # 6. Pose the final question as a hook
        self.play(FadeOut(graph_system), FadeOut(hamiltonian_essence))
        self.wait(0.5)

        final_question = MarkupText(
            'But if brute force is impossible... <span color="YELLOW">how do we find it?</span>',
            font_size=42,
            justify=True
        ).move_to(ORIGIN) # Center the question
        
        self.play(Write(final_question))
        self.wait(5)
    
        # (This code follows immediately after the final question "how do we find it?")

        # --- NEW SEQUENCE: THE EDGE OF SOLVABILITY ---

        # 1. Answer the question with nuance (with text wrapping)
        # Relies on Manim's default center alignment for MarkupText with newlines.
        answer_text = MarkupText(
            'The short answer: for a general, complex system...\n<span color="YELLOW">you don\'t.</span>',
            font_size=42
        )
        self.play(ReplacementTransform(final_question, answer_text))
        self.wait(3)

        explanation_text = MarkupText(
            'There is no known algorithm that can efficiently find the <span color="YELLOW">exact</span>\nground state for any arbitrary set of tensions.',
            font_size=36
        ).move_to(ORIGIN)
        
        self.play(ReplacementTransform(answer_text, explanation_text))
        self.wait(4)
        self.play(FadeOut(explanation_text))
        self.wait(0.5)
        
        # 2. Show the "Rare Exact Solutions"
        title = Text("Rare Exact Solutions", font_size=42).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # A) 2D Planar Graph (Onsager's Solution)
        planar_label = Text("2D Planar Graphs", font_size=32).next_to(title, DOWN, buff=0.5)
        
        grid = VGroup(*[Dot() for i in range(25)]).arrange_in_grid(5, 5, buff=0.8)
        lines = VGroup()
        for i in range(5):
            for j in range(4):
                lines.add(Line(grid[i*5+j], grid[i*5+j+1], stroke_width=2, color=GRAY))
        for i in range(4):
            for j in range(5):
                lines.add(Line(grid[i*5+j], grid[(i+1)*5+j], stroke_width=2, color=GRAY))

        planar_system = VGroup(grid, lines).scale(0.8).next_to(planar_label, DOWN, buff=0.8)
        
        onsager_text = VGroup(
            Text("Lars Onsager", font_size=36),
            Text("1944", font_size=32, color=YELLOW)
        ).arrange(DOWN).next_to(planar_system, RIGHT, buff=0.5)

        planar_group = VGroup(planar_label, planar_system, onsager_text)
        self.play(Write(planar_group))
        self.wait(5)
        
        # B) Spin Glass / Parisi case
        spinglass_label = Text("Spin Glasses (Random Tensions)", font_size=32).next_to(title, DOWN, buff=0.5)
        
        num_nodes = 15
        nodes = VGroup(*[Dot() for _ in range(num_nodes)]).arrange_in_grid(3, 5, buff=1.5)
        for node in nodes:
            node.shift((random.random()-0.5)*0.5*RIGHT + (random.random()-0.5)*0.5*UP)
        
        lines = VGroup()
        all_pairs = list(itertools.combinations(range(num_nodes), 2))
        selected_pairs = random.sample(all_pairs, int(num_nodes * 1.8))
        for pair in selected_pairs:
            color = random.choice([PLUS_ONE_COLOR, MINUS_ONE_COLOR])
            lines.add(Line(nodes[pair[0]], nodes[pair[1]], color=color, stroke_width=2, z_index=-1))
            
        spinglass_system = VGroup(nodes, lines).scale(0.7).next_to(spinglass_label, DOWN, buff=0.5)
        
        parisi_text = VGroup(
            Text("Giorgio Parisi", font_size=36),
            MarkupText("Statistical Properties", font_size=28),
            Text("Nobel Prize 2021", font_size=32, color=YELLOW)
        ).arrange(DOWN, buff=0.2).next_to(spinglass_system, RIGHT, buff=0.5)

        spinglass_group = VGroup(spinglass_label, spinglass_system, parisi_text)
        self.play(ReplacementTransform(planar_group, spinglass_group))
        self.wait(5)

        # 3. Transition to Quantum Annealing
        self.play(FadeOut(title), FadeOut(spinglass_group))
        self.wait(0.5)

        outro_text = MarkupText(
            "For the messy, real-world problems,\nwe need a different approach...",
            font_size=36
        ).move_to(UP * 2.5)

        self.play(Write(outro_text))
        self.wait(3)

        # 4. Show the D-Wave Computer
        try:
            dwave_image = ImageMobject("dwave_computer.jpeg")
            dwave_image.set_height(4.5)
            dwave_image.next_to(outro_text, DOWN, buff=0.5)
            
            self.play(FadeIn(dwave_image))
            
            dwave_label = Text("Quantum Annealer", font_size=42, color=TEAL)
            dwave_label.next_to(dwave_image, DOWN)
            self.play(Write(dwave_label))
            self.wait(5)
            
        except FileNotFoundError:
            self.play(Write(Text("Image 'dwave_computer.jpeg' not found.", color=RED)))
            self.wait(3)


def calculate_min_H(J):
    N = len(J)
    # Generate all 2^(N-1) combinations for the first N-1 spins
    # The last spin is fixed to -1 to break the s -> -s symmetry
    # This is okay because we only care about the structure of one of the two ground states.
    num_combos = 2**(N - 1)
    # Using a direct array approach to build combinations
    # This is more memory-intensive but conceptually clear for smaller N
    combos = np.ones((num_combos, N), dtype=int)
    for i in range(N - 1):
        n = 2**(N - 1 - (i + 1))
        combos[:, i] = np.tile(np.repeat(np.array([1, -1]), n), 2**i)
    combos[:, -1] = -1

    # Einsum is a very efficient way to compute the Hamiltonian for all combos at once
    # H_i = s_i^T . J . s_i
    H = 0.5 * np.einsum('ij,jk,ik->i', combos, J, combos)
    min_H_index = np.argmin(H)
    return np.min(H), combos[min_H_index]
def J_order(N, d):
    def f(i, j):
        return ((i+1)/N)**d + ((j+1)/N)**d
    mat = np.fromfunction(f, (N, N), dtype=float)
    np.fill_diagonal(mat, 0)
    return mat


class OrderedJ(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        PLUS_ONE_COLOR = BLUE_D
        MINUS_ONE_COLOR = RED_D
        J_COLOR = YELLOW
        H_COLOR = GREEN
        
        # --- SEQUENCE 1: THE SPARK OF AN IDEA ---

        # 1. Opening text about J_ij
        title_text = Text("The Ising model is defined by its matrix of tensions,", font_size=36)
        hamiltonian_formula = MathTex(r"H = \sum_{i<j} J_{ij} s_i s_j", font_size=48).next_to(title_text, DOWN, buff=0.4)
        hamiltonian_formula.set_color_by_tex("J_{ij}", J_COLOR)
        
        opening_group = VGroup(title_text, hamiltonian_formula).move_to(ORIGIN)
        
        self.play(Write(opening_group))
        self.play(Indicate(hamiltonian_formula.get_part_by_tex("J_{ij}"), scale_factor=1.2, color=J_COLOR))
        self.wait(3)
        self.play(FadeOut(opening_group))
        self.wait(0.5)

        # 2. Pose the student's question
        question = Text("A young physics student wondered...", font_size=36).to_edge(2*UP)
        sub_question = Text(
            "What if the interaction was not random,\nbut based on a simple, underlying rule?",
            font_size=32, line_spacing=1.2
        ).move_to(ORIGIN)

        self.play(Write(question))
        self.play(Write(sub_question))
        self.wait(3)
        self.play(FadeOut(question, sub_question))
        self.wait(0.5)
        
        # --- SEQUENCE 2: THE WALL OF EVIDENCE (d=1) ---

        # 1. Show the simple rule
        rule_formula = MathTex("J_{ij} = i + j", font_size=48)
        rule_formula.to_edge(UP, buff=1.0)
        self.play(Write(rule_formula))
        self.wait(2)

        # 2. Pre-calculate ground states for d=1
        ground_states = {}
        for n in range(10, 16):
            j_matrix = J_order(n, d=1)
            _, s_g = calculate_min_H(j_matrix)
            ground_states[n] = s_g

        # 3. Animate the "Wall of Evidence"
        dot_rows = VGroup()
        for n in range(10, 16):
            # Create the label and the row of dots
            n_label = MathTex(f"N={n}", font_size=32)
            dot_row = VGroup(*[Dot(radius=0.1, color=WHITE) for _ in range(n)]).arrange(RIGHT, buff=0.25)
            
            row_group = VGroup(n_label, dot_row).arrange(RIGHT, buff=0.5)
            dot_rows.add(row_group)

        dot_rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(ORIGIN)

        # Animate each row appearing and resolving
        for i, n in enumerate(range(10, 16)):
            self.play(FadeIn(dot_rows[i]), run_time=0.5)
            self.wait(0.5)
            
            s_g = ground_states[n]
            animations = []
            for j, spin in enumerate(s_g):
                color = PLUS_ONE_COLOR if spin == 1 else MINUS_ONE_COLOR
                animations.append(dot_rows[i][1][j].animate.set_color(color))
            
            self.play(LaggedStart(*animations, lag_ratio=0.1))
            self.wait(1)

        self.wait(3)


        # --- SEQUENCE 3: GENERALIZING TO 'd' ---

        # 1. Morph the formula to the general case
        general_rule = MathTex(r"J_{ij} \propto i^d + j^d", font_size=48).move_to(rule_formula)
        general_rule.set_color_by_tex("d", ORANGE)
        self.play(Transform(rule_formula, general_rule))
        self.wait(2)

        # 2. Set up the interactive demonstration
        # Make the "wall of evidence" fully opaque again for the main demonstration
        self.play(dot_rows.animate.fade(0))

        # Create the dial for 'd' below the rows
        d_dial = NumberLine(
            x_range=[-8, 8, 2], # Adjusted for better visual spacing of ticks
            length=10,
            include_numbers=True,
            label_direction=UP
        ).next_to(dot_rows, DOWN, buff=0.8)
        d_label = MathTex("d", color=ORANGE).next_to(d_dial, DOWN)
        
        self.play(Create(d_dial), Write(d_label))
        self.wait(1)

        # 3. Pre-calculate the TRUE ground states for different 'd' for ALL Ns
        def get_M(n, d):
            j_mat = J_order(n, d)
            _, s_g = calculate_min_H(j_mat)
            return np.sum(s_g == 1)

        M_values = {}
        d_points = [-2.0, 4.0, 6.0] # The points we will visit, d=1 is already shown
        all_n_values = range(10, 16)

        for d_val in d_points:
            M_values[d_val] = {}
            for n_val in all_n_values:
                M_values[d_val][n_val] = get_M(n_val, d_val)

        # 4. Animate the pointer and ALL state changes simultaneously
        pointer = Arrow(start=d_dial.n2p(1) + UP*0.5, end=d_dial.n2p(1), color=ORANGE, buff=0)
        self.play(GrowArrow(pointer))
        self.wait(1)

        # Helper function to generate the list of animations for any 'd'
        def get_update_animations(d_val):
            anims = []
            for i, n in enumerate(all_n_values):
                M = M_values[d_val][n]
                # Get the dot VGroup for the current row
                current_dots = dot_rows[i][1]
                for j in range(n):
                    color = PLUS_ONE_COLOR if j < M else MINUS_ONE_COLOR
                    anims.append(current_dots[j].animate.set_color(color))
            return anims

        # Animate to d=6
        self.play(
            pointer.animate.move_to(d_dial.n2p(6) + UP*0.25),
            LaggedStart(*get_update_animations(6.0), lag_ratio=0.01),
            run_time=2.5
        )
        self.wait(1)
        
        # Animate to d=4.0
        self.play(
            pointer.animate.move_to(d_dial.n2p(4) + UP*0.25),
            LaggedStart(*get_update_animations(4.0), lag_ratio=0.01),
            run_time=3.0
        )
        self.wait(1)

        # Animate to d=-2
        self.play(
            pointer.animate.move_to(d_dial.n2p(-2) + UP*0.25),
            LaggedStart(*get_update_animations(-2.0), lag_ratio=0.01),
            run_time=2.0
        )
        self.wait(2)


class ConvergingRatio(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        PLUS_ONE_COLOR = BLUE_D
        MINUS_ONE_COLOR = RED_D
        J_COLOR = YELLOW
        D_COLOR = ORANGE
        Q_COLOR = YELLOW

        # Helper function for this scene
        def calculate_min_J_o(J):
            N = len(J)
            H_l = []
            for M in range(N + 1):
                s = np.array([1]*M + [-1]*(N - M), dtype=float)
                H = 0.5 * s @ J @ s
                H_l.append(H)
            
            min_H_idx = np.argmin(H_l)
            return min_H_idx

        # --- SEQUENCE 1: DEFINING THE RATIO q ---

        N_rep, d_rep = 12, 1
        j_mat_rep = J_order(N_rep, d_rep)
        M_rep = calculate_min_J_o(j_mat_rep)

        s_vector = VGroup(*[
            Dot(radius=0.15, color=PLUS_ONE_COLOR if i < M_rep else MINUS_ONE_COLOR)
            for i in range(N_rep)
        ]).arrange(RIGHT, buff=0.3)
        
        self.play(Write(s_vector))
        self.wait(2)

        brace = Brace(s_vector[:M_rep], direction=UP, color=WHITE)
        m_label = brace.get_text("M")
        m_label.set_color(Q_COLOR).scale(1.2)
        
        self.play(GrowFromCenter(brace), Write(m_label))
        self.wait(2)

        q_formula = MathTex("q", "=", "{M", r"\over", "N}").set_color_by_tex("q", Q_COLOR)
        q_formula.next_to(s_vector, DOWN, buff=0.8)
        q_formula.get_part_by_tex("M").set_color(Q_COLOR)
        
        self.play(Write(q_formula))
        self.wait(3)

        # --- SEQUENCE 2: THE CONVERGENCE GRAPH ---
        
        self.play(FadeOut(s_vector, brace, m_label, q_formula))
        self.wait(0.5)

        ax = Axes(
            x_range=[0, 105, 10], y_range=[0, 1, 0.1],
            x_length=10, y_length=5.5, # y_length is slightly smaller
            axis_config={"color": BLUE},
            y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}
        )
        x_label = ax.get_x_axis_label("N \\text{ (Number of Spins)}")
        y_label = ax.get_y_axis_label("q = M/N", direction=UP).shift(LEFT*0.5)
        
        # Corrected: Scale and shift the entire graph down
        graph = VGroup(ax, x_label, y_label).scale(0.9).shift(DOWN * 0.5)

        self.play(Create(graph))
        self.wait(1)

        max_N_brute = 30
        max_N_total = 100
        d_values = [1.0, -0.5, 4]
        q_data = {d: [] for d in d_values}
        
        for d in d_values:
            for n in range(2, max_N_total + 1):
                j_mat = J_order(n, d)
                M = calculate_min_J_o(j_mat)
                q_data[d].append(M / n if n > 0 else 0)

        d1_color = GREEN
        d1_label = MathTex("d=1", color=d1_color).next_to(ax.c2p(max_N_total, q_data[1.0][-1]), RIGHT)
        self.play(Write(d1_label))

        d1_dots_brute = VGroup(*[
            Dot(ax.c2p(n, q_data[1.0][n-2]), color=d1_color, radius=0.05)
            for n in range(2, max_N_brute + 1)
        ])
        
        self.play(LaggedStart(*[Create(d) for d in d1_dots_brute], lag_ratio=0.1, run_time=3))
        self.wait(1)

        wall = DashedLine(ax.c2p(max_N_brute, 0), ax.c2p(max_N_brute, 1), color=RED)
        wall_label = Text("Brute-Force Wall", font_size=24, color=RED)
        wall_label.next_to(wall.get_top(), UP, buff=0.1)
        
        self.play(Create(wall), Write(wall_label))
        self.wait(2)
        
        # This text will now fit comfortably
        leap_of_faith_text = Text(
            "Assume the two-cluster pattern always holds.",
            font_size=30, color=YELLOW
        ).to_edge(UP)
        self.play(Write(leap_of_faith_text))
        self.wait(2)

        complexity_before = MathTex("2^N", r"\gg", "N").scale(1.5).next_to(leap_of_faith_text, DOWN, buff=0.5).to_edge(RIGHT, buff=1.5)
        complexity_after = MathTex("N").scale(1.5).move_to(complexity_before)
        
        self.play(Write(complexity_before))
        self.wait(1)
        self.play(Transform(complexity_before, complexity_after), FadeOut(leap_of_faith_text))
        self.play(FadeOut(complexity_before))
        self.wait(0.5)

        d1_dots_assumed = VGroup(*[
            Dot(ax.c2p(n, q_data[1.0][n-2]), color=d1_color, radius=0.05)
            for n in range(max_N_brute + 1, max_N_total + 1)
        ])
        self.play(Create(d1_dots_assumed), run_time=1)
        self.wait(1)

        d_colors = {-0.5: PINK, 4: PURPLE}
        for d in [-0.5, 4]:
            label = MathTex(f"d={d}", color=d_colors[d]).next_to(ax.c2p(max_N_total, q_data[d][-1]), RIGHT)
            dots = VGroup(*[Dot(ax.c2p(n, q_data[d][n-2]), color=d_colors[d], radius=0.05) for n in range(2, max_N_total + 1)])
            self.play(Write(label), Create(dots), run_time=1.5)

        self.wait(5)


class GroundStateCalculation(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        PLUS_ONE_COLOR = BLUE_D
        MINUS_ONE_COLOR = RED_D
        J_COLOR = YELLOW
        D_COLOR = ORANGE
        PINK_TERM_COLOR = PINK
        H_COLOR = GREEN
        # --- SEQUENCE 1: FORMALIZING THE INTERACTION MATRIX ---
        
        recap_text = Text(
            "So, having seen the ratio 'q' converge for any given 'd'...",
            font_size=36
        ).to_edge(UP)
        proportional_formula = MathTex(r"J_{ij} \propto i^d + j^d", font_size=60)
        proportional_formula.set_color_by_tex("d", D_COLOR)
        proportional_formula.next_to(recap_text, DOWN, buff=0.5)
        self.play(Write(recap_text))
        self.play(Write(proportional_formula))
        self.wait(3)
        formalization_text = MathTex(
            r"\text{...he formalized this idea, naming the interaction matrix } J^{(N, d)},",
            font_size=38
        )
        formalization_text.set_color_by_tex("J^{(N, d)}", J_COLOR)
        formalization_text.next_to(proportional_formula, DOWN, buff=0.8)
        formalization_text_2 = Text(
            "adding some terms for convenience and rigor.",
            font_size=32
        ).next_to(formalization_text, DOWN)
        self.play(Write(formalization_text), Write(formalization_text_2))
        self.wait(3)

        # --- THIS IS THE FIX ---
        # Build the formula in parts to reference the Kronecker delta term reliably
        part1 = MathTex(r"J_{ij}^{(N, d)}", r"=", r"\frac{1}{N^d}", r"(i^d + j^d)")
        part2 = MathTex(r"(1 - \delta_{ij})") # This is the part we want to reference
        
        # Color the parts
        part1.set_color_by_tex_to_color_map({
            "J_{ij}^{(N, d)}": J_COLOR, "N": WHITE, "d": D_COLOR, "i": BLUE, "j": GREEN
        })
        part2.set_color_by_tex(r"\delta_{ij}", PINK_TERM_COLOR)

        # Group and arrange them
        formal_formula_group = VGroup(part1, part2).arrange(RIGHT, buff=0.2)
        formal_formula_group.move_to(proportional_formula)

        self.play(
            FadeOut(recap_text, formalization_text, formalization_text_2),
            Transform(proportional_formula, formal_formula_group)
        )
        formula = proportional_formula # Keep the handle
        self.wait(2)
        
        # Now, we can reliably reference part2
        kronecker_term_part = formula.submobjects[1] # part2 is the second element of the VGroup
        kronecker_explanation = Text(
            "(This just means the diagonals are zero)",
            font_size=24, color=GRAY
        ).next_to(kronecker_term_part, DOWN, buff=0.3)
        
        self.play(Indicate(kronecker_term_part, color=PINK_TERM_COLOR), Write(kronecker_explanation))
        self.wait(3)
        self.play(FadeOut(kronecker_explanation))

        # 4. Show the concrete example for N=5, d=2
        example_label = MathTex("N=5, d=2", font_size=42).set_color_by_tex("d", D_COLOR)
        matrix_values = [
            [0, 5, 10, 17, 26], [5, 0, 13, 20, 29], [10, 13, 0, 25, 34],
            [17, 20, 25, 0, 41], [26, 29, 34, 41, 0]
        ]
        j52_lhs = MathTex(r"J^{(5, 2)}", "=", r"\frac{1}{5^2}").set_color_by_tex("J", J_COLOR)
        j52_matrix = IntegerMatrix(matrix_values, h_buff=0.8)
        
        example_matrix_group = VGroup(j52_lhs, j52_matrix).arrange(RIGHT, buff=0.3)
        full_example = VGroup(example_label, example_matrix_group).arrange(DOWN, buff=0.4)
        full_example.next_to(formula, DOWN, buff=0.5).scale(0.8)

        self.play(Write(example_label))
        self.play(Write(j52_lhs), Create(j52_matrix))
        self.wait(5)

        # --- SEQUENCE 2: POSTULATING THE GROUND STATE ---

        self.play(FadeOut(full_example), formula.animate.to_edge(UP, buff=1.0))
        self.wait(0.5)

        postulate_text = Text(
            "...with the postulated ground state of the following form:",
            font_size=36
        ).next_to(formula, DOWN, buff=0.7)
        self.play(Write(postulate_text))
        self.wait(2)

        # 3. Display the ground state vector s_g^T as specified
        s_g_label = MathTex(r"\pmb{s}_g^T", r"=", font_size=60)
        
        up_spin = MathTex("+1", color=PLUS_ONE_COLOR)
        down_spin = MathTex("-1", color=MINUS_ONE_COLOR)
        dots = MathTex(r"\dots").scale(1.2)

        # Using your specified layout for a clearer "block" visual
        spin_vector_content = VGroup(
            up_spin,
            up_spin.copy(),
            dots.copy(),
            up_spin.copy(),
            dots.copy(),
            down_spin.copy(),
            down_spin.copy(),
            dots.copy(),
            down_spin
        ).arrange(RIGHT, buff=0.3) # Slightly reduced buff for a denser look

        bracket_l = MathTex(r"\big[", font_size=120).next_to(spin_vector_content, LEFT, buff=0.2)
        bracket_r = MathTex(r"\big]", font_size=120).next_to(spin_vector_content, RIGHT, buff=0.2)
        
        s_g_vector = VGroup(bracket_l, spin_vector_content, bracket_r)
        
        full_s_g_display = VGroup(s_g_label, s_g_vector).arrange(RIGHT, buff=0.4)
        full_s_g_display.next_to(postulate_text, DOWN, buff=0.7)

        self.play(Write(full_s_g_display))
        self.wait(2)

        # 4. Add the brace for M underneath the first cluster
        # The first cluster consists of the first 4 elements in spin_vector_content
        first_cluster = spin_vector_content[:4]
        
        m_brace = Brace(first_cluster, direction=DOWN, color=WHITE)
        m_label = m_brace.get_text("M spins")
        
        self.play(
            GrowFromCenter(m_brace),
            Write(m_label)
        )
        self.wait(4)

        # --- SEQUENCE 3: Z2 SYMMETRY AND CONVENTION (ROBUST VERSION) ---

        # 1. Show the compact Hamiltonian
        hamiltonian_compact = MathTex("H", "=", r"\frac{1}{2}", r"\pmb{s}^T", "J", r"\pmb{s}", font_size=48)
        hamiltonian_compact.next_to(full_s_g_display, DOWN, buff=1.0)
        hamiltonian_compact[0].set_color(H_COLOR)
        hamiltonian_compact[4].set_color(J_COLOR)
        self.play(Write(hamiltonian_compact))
        self.wait(2)

        # --- THE FOOLPROOF FIX ---
        # Create BOTH the original and flipped targets right now.
        
        # Target 1: The original "+1 first" state
        original_spins_target = spin_vector_content.copy()

        # Target 2: The flipped "-1 first" state
        flipped_spins_target = spin_vector_content.copy()
        for elem in flipped_spins_target:
            if isinstance(elem, MathTex) and elem.get_tex_string() != r"\dots":
                if elem.get_tex_string() == "+1":
                    elem.become(MathTex("-1", color=MINUS_ONE_COLOR).move_to(elem))
                else:
                    elem.become(MathTex("+1", color=PLUS_ONE_COLOR).move_to(elem))
        
        # Create the flipped formula target
        hamiltonian_flipped = MathTex("H", "=", r"\frac{1}{2}", r"(-\pmb{s})^T", "J", r"(-\pmb{s})", font_size=48).move_to(hamiltonian_compact)
        hamiltonian_flipped[0].set_color(H_COLOR)
        hamiltonian_flipped[4].set_color(J_COLOR)

        # 2. Animate the FIRST flip
        # The on-screen 'spin_vector_content' becomes the flipped target.
        self.play(
            spin_vector_content.animate.become(flipped_spins_target),
            hamiltonian_compact.animate.become(hamiltonian_flipped),
            run_time=2.0
        )
        self.wait(3)

        # 3. State the convention and flip BACK
        self.play(FadeOut(hamiltonian_compact, m_brace, m_label))
        convention_text = Text(
            "In his notation, he chose the first cluster to be up (+1).",
            font_size=32, color=YELLOW
        ).next_to(full_s_g_display, DOWN, buff=0.8)
        self.play(Write(convention_text))
        self.wait(1)

        # Animate the on-screen vector becoming the original target.
        self.play(
            spin_vector_content.animate.become(original_spins_target),
            run_time=1.5
        )
        self.wait(5)

        # 4. ONE. FINAL. FUCKING. FLIP.
        # Animate the on-screen vector becoming the flipped target again.
        self.play(
            spin_vector_content.animate.become(flipped_spins_target),
            run_time=2.0
        )
        self.wait(5)



class NewPerspective(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        J_COLOR = YELLOW
        S_COLOR = BLUE_D
        H_COLOR = GREEN
        
        # --- SEQUENCE 1: THE IDENTITY ---

        # 1. Start with the core identity to be proven, faded out
        identity = MathTex(
            r"\sum_{i,j} s_i J_{ij} s_j", "=", r"\sum_{i,j} \left[ J \odot (\pmb{s}\pmb{s}^T) \right]_{ij}",
            font_size=60
        )
        identity.set_color_by_tex_to_color_map({
            "J": J_COLOR,
            "s": S_COLOR,
            r"\odot": RED,
            r"\pmb{s}": S_COLOR
        })
        identity.to_edge(1.1*UP)
        
        # 2. Step 1: Define the Outer Product
        proof_step1_lhs = MathTex(r"(\pmb{s}\pmb{s}^T)_{ij}", font_size=48)
        proof_step1_lhs.set_color_by_tex("s", S_COLOR)
        
        proof_step1_rhs = MathTex("=", "s_i s_j", font_size=48)
        proof_step1_rhs.set_color_by_tex("s", S_COLOR)

        step1_group = VGroup(proof_step1_lhs, proof_step1_rhs).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        
        step1_title = Text("Step 1: The Outer Product", font_size=32).next_to(step1_group, 0.9*UP, buff=0.5)
        self.play(Write(step1_title))
        self.play(Write(step1_group))
        self.wait(3)

        # 3. Step 2: Define the Hadamard Product
        self.play(step1_group.animate.shift(UP*2), FadeOut(step1_title))
        
        proof_step2_lhs = MathTex(r"\big[ J \odot (\pmb{s}\pmb{s}^T) \big]_{ij}", font_size=48)
        proof_step2_lhs.set_color_by_tex_to_color_map({
            "J": J_COLOR, "s": S_COLOR, r"\odot": RED
        })

        proof_step2_rhs = MathTex("=", "J_{ij}", r"(\pmb{s}\pmb{s}^T)_{ij}", font_size=48)
        proof_step2_rhs.set_color_by_tex_to_color_map({
            "J": J_COLOR, "s": S_COLOR
        })

        step2_group = VGroup(proof_step2_lhs, proof_step2_rhs).arrange(RIGHT, buff=0.3).move_to(ORIGIN)
        
        step2_title = Text("Step 2: The Hadamard Product", font_size=32).next_to(step2_group, 0.9*UP, buff=0.5)
        self.play(Write(step2_title))
        self.play(Write(step2_group))
        self.wait(3)

        # 4. Substitute Step 1 into Step 2
        # Highlight the term to be substituted
        term_to_sub = proof_step2_rhs.get_part_by_tex(r"(\pmb{s}\pmb{s}^T)_{ij}")
        self.play(Indicate(term_to_sub))
        
        # The result of the substitution
        proof_step3_rhs = MathTex("=","J_{ij}", "s_i s_j", font_size=48)
        proof_step3_rhs.set_color_by_tex_to_color_map({"J": J_COLOR, "s": S_COLOR})
        proof_step3_rhs.next_to(proof_step2_lhs, RIGHT, buff=0.3)
        
        self.play(
            FadeOut(step2_title),
            Transform(proof_step2_rhs, proof_step3_rhs)
        )
        self.wait(3)
        
        # (The code for steps 1-4 remains the same)
        # self.wait(3)

        # 5. Final Step: Sum over all elements
        
        # Group the result of the substitution
        final_element_identity = VGroup(proof_step2_lhs, proof_step2_rhs)
        
        # Create the final equation parts
        sum_symbol_lhs = MathTex(r"\sum_{i,j}", font_size=64)
        sum_symbol_rhs = MathTex(r"= \sum_{i,j}", font_size=64) # The equals sign is now part of the RHS
        
        # Build the final equation visually
        # Target for the left part of the transform
        final_lhs_target = VGroup(sum_symbol_lhs, proof_step2_lhs.copy()).arrange(RIGHT, buff=0.2)
        
        # Target for the right part of the transform
        final_rhs_target = VGroup(sum_symbol_rhs, proof_step3_rhs[1:].copy()).arrange(RIGHT, buff=0.2)
        
        # Position the final equation in the center
        final_eq = VGroup(final_lhs_target, final_rhs_target).arrange(RIGHT, buff=0.4).move_to(ORIGIN)
        
        # Animate the transformation precisely
        self.play(
            FadeOut(step1_group),
            Transform(final_element_identity[0], final_lhs_target),
            Transform(final_element_identity[1], final_rhs_target)
        )
        self.wait(2)

        # 6. Show the final identity clearly at the top
        identity.set_color(YELLOW_E)
        # The object `final_element_identity` now looks like `final_eq`
        self.play(ReplacementTransform(final_element_identity, identity))
        self.wait(5)


        # --- NEW SEQUENCE: VISUALLY PROVING THE IDENTITY FOR s_g ---
        
        # 1. Add the explanatory text (Corrected: with line break)
        explanation_text = Text(
            "For our postulated ground state, let's visualize each side:",
            font_size=32, line_spacing=1.2
        ).next_to(identity, DOWN, buff=0.4)
        self.play(Write(explanation_text))
        self.wait(2)

        # 2. Define ALL components for the final layout first
        s_g = np.array([1, 1, 1, -1, -1])
        RED_COLOR = RED_D
        # -- LHS Components --
        s_row_vals = [f"{v:+.0f}" for v in s_g]
        s_row_mobs = [MathTex(v, color=S_COLOR if v=="+1" else RED_COLOR) for v in s_row_vals]
        s_row = MobjectMatrix([s_row_mobs], h_buff=0.8)
        
        s_col_vals = [[v] for v in s_row_vals]
        s_col_mobs = [[MathTex(v[0], color=S_COLOR if v[0]=="+1" else RED_COLOR)] for v in s_col_vals]
        s_col = MobjectMatrix(s_col_mobs, v_buff=0.6)

        # Corrected: Using proper subscripts for J
        J_matrix_vals = [[f"J_{{{i}{j}}}" for j in range(1,6)] for i in range(1,6)]
        J_matrix = Matrix(J_matrix_vals, h_buff=1.0, v_buff=0.7)
        J_matrix.elements.set_color(J_COLOR)

        lhs_group = VGroup(s_row, J_matrix, s_col).arrange(RIGHT, buff=0.2)
        
        # -- RHS Components --
        ssT_matrix_vals = np.outer(s_g, s_g)
        ssT_mobs = [
            [MathTex(f"{val:+.0f}", color=S_COLOR if val == 1 else RED_COLOR) for val in row]
            for row in ssT_matrix_vals
        ]
        ssT_matrix = MobjectMatrix(ssT_mobs, h_buff=0.8, v_buff=0.7)

        hadamard_symbol = MathTex(r"\odot", font_size=72)
        hadamard_group = VGroup(J_matrix.copy(), hadamard_symbol, ssT_matrix).arrange(RIGHT, buff=0.2)
        
        sum_text = Text("Sum of all elements", font_size=36)
        sum_brackets = SurroundingRectangle(hadamard_group, buff=0.2, color=WHITE)
        sum_text.next_to(sum_brackets, UP, buff=0.1)
        rhs_group = VGroup(hadamard_group, sum_brackets, sum_text)
        
        # -- Equation Assembly --
        equals_sign = MathTex("=").scale(1.5)
        
        # This is the final layout group. We create it now to get the final positions.
        full_equation = VGroup(lhs_group, equals_sign, rhs_group).arrange(RIGHT, buff=0.3)
        full_equation.scale(0.55).move_to(ORIGIN).shift(DOWN*0.5)

        # 3. Animate smoothly into the final layout
        
        # First, show only the LHS in the center
        lhs_initial = lhs_group.copy().scale(1.8).next_to(explanation_text, DOWN, buff=0.3)
        self.play(FadeOut(explanation_text), Write(lhs_initial))
        self.wait(3)

        # Now, animate all parts moving to their final, pre-calculated positions
        self.play(
            # The LHS moves from its initial spot to its final spot in the equation
            Transform(lhs_initial, full_equation[0]),
            # The equals sign and RHS fade in at their final spots
            FadeIn(full_equation[1]),
            FadeIn(full_equation[2])
        )
        self.wait(5)

        # --- NEW SEQUENCE: EVALUATING THE HADAMARD PRODUCT (FRESH START) ---

        # 1. Start by explicitly clearing the scene of old objects
        # and adding back ONLY the ones we want to keep.
        self.play(
            FadeOut(lhs_group),
            FadeOut(equals_sign),
            FadeOut(lhs_initial),
        )
        # rhs_group is the only thing left.
        
        # 2. Animate the RHS to the center
        self.play(
            rhs_group.animate.move_to(ORIGIN).scale(1.2)
        )
        self.wait(1)

        # 3. Define the final, resulting matrix with corrected logic
        hadamard_group = rhs_group[0]
        sum_brackets = rhs_group[1]
        sum_text = rhs_group[2]

        J_matrix_rhs = hadamard_group[0]
        ssT_matrix = hadamard_group[2]
        
        j_mobs_list = J_matrix_rhs.mob_matrix
        sst_mobs_list = ssT_matrix.mob_matrix

        result_mobs = []
        for i in range(5):
            row_mobs = []
            for j in range(5):
                color = sst_mobs_list[i][j].get_color()
                j_text = j_mobs_list[i][j].get_tex_string()
                
                if color == RED_COLOR:
                    mob = MathTex(f"-{j_text}", color=color, font_size=30)
                else:
                    mob = MathTex(f"{j_text}", color=color, font_size=30)

                row_mobs.append(mob)
            result_mobs.append(row_mobs)
            
        final_matrix = MobjectMatrix(result_mobs, h_buff=1.0, v_buff=0.7)
        final_matrix.move_to(hadamard_group)

        # 4. Create a new, correctly sized bounding box for the final state
        new_sum_brackets = SurroundingRectangle(final_matrix, buff=0.2, color=WHITE)
        new_sum_text = Text("Sum of all elements", font_size=24).next_to(new_sum_brackets, DOWN, buff=0.1)

        # 5. Animate the transformation
        # Use ReplacementTransform for robustness
        self.play(
            ReplacementTransform(hadamard_group, final_matrix),
            ReplacementTransform(sum_brackets, new_sum_brackets),
            ReplacementTransform(sum_text, new_sum_text)
        )
        self.wait(4)


        # group them all
        final_group = VGroup(final_matrix, new_sum_brackets, new_sum_text)
        
        # remove the identity formula and bring the matrix with the sum text and box into middle, then left of the panel:
        self.play(
            FadeOut(identity),
            final_group.animate.move_to(ORIGIN).scale(1.2)
        )

        self.wait(3)

        # move left
        self.play(
            final_group.animate.move_to(LEFT*2)
        )

        self.wait(1.5)

        # add Mathtext : = \sum_{i,j \in \text{blue}} J_{ij} - \sum_{i,j \in \text{red}} J_{ij}

        blue_sum_text = MathTex(r"= \sum_{i,j \in \text{blue}}J_{ij}", font_size=36, color=S_COLOR)
        red_sum_text = MathTex(r"- \sum_{i,j \in \text{red}}J_{ij}", font_size=36, color=RED_COLOR)
        color_based_text = VGroup(blue_sum_text, red_sum_text).arrange(RIGHT, buff=0.5)
        
        # add next to brackets
        color_based_text.next_to(new_sum_brackets, RIGHT, buff=0.5)

        self.play(
            FadeIn(color_based_text)
        )

        self.wait(3)
        

        # --- INTERMEDIATE STEP: CONNECTING COLOR TO INDICES ---
        D_COLOR = YELLOW_D
        # 1. Fade out the matrix and identity, keep the color sum
        self.play(
            FadeOut(final_group),
            # Center the color-based sum
            color_based_text.animate.center()
        )
        self.wait(1)

        s_g_vector_text = MathTex(
            r"\pmb{s}_g^T = [",
            r"+1 \dots, +1", # Blue part
            r",",             # Comma
            r"-1 \dots, -1", # Red part
            r"]",
            font_size=42
        )
        
        # Color the specific parts by index
        s_g_vector_text[1].set_color(S_COLOR)
        s_g_vector_text[3].set_color(RED_COLOR)

        s_g_vector_text.next_to(color_based_text, DOWN, buff=0.8)

        # NOW, create the Brace objects targeting the colored parts
        blue_brace = Brace(s_g_vector_text[1], direction=DOWN, buff=0.1)
        blue_label = blue_brace.get_tex(r"M \text{ spins}")
        blue_label.set_font_size(22)

        red_brace = Brace(s_g_vector_text[3], direction=DOWN, buff=0.1)
        red_label = red_brace.get_tex(r"N-M \text{ spins}")
        red_label.set_font_size(22)

        
        # Group everything for the animation
        s_g_reminder = VGroup(s_g_vector_text, blue_brace, blue_label, red_brace, red_label)
        # --- END OF FIX ---

        self.play(
            Write(s_g_vector_text),
            LaggedStart(
                GrowFromCenter(blue_brace),
                Write(blue_label),
                lag_ratio=0.5
            )
        )
        self.play(
            LaggedStart(
                GrowFromCenter(red_brace),
                Write(red_label),
                lag_ratio=0.5
            )
        )
        self.wait(3)

        # 3. Create and transform to the intermediate, index-based formula
        # This formula is a bridge between the color names and the formal indices
        intermediate_formula = MathTex(
            r"H = \sum_{1 \le i,j \le M} J_{ij} + \sum_{M+1 \le i,j \le N} J_{ij} - 2\sum_{\substack{i \le M \\ j > M}} J_{ij}",
            font_size=40
        )
        intermediate_formula.set_color_by_tex("M", S_COLOR) # Use the spin color for M

        # Animate the transition from the simple color sum to the more formal index sum
        self.play(
            ReplacementTransform(VGroup(color_based_text, s_g_reminder), intermediate_formula)
        )
        self.wait(4)

        # --- FINAL TRANSFORMATION TO THE PAPER'S FORMULA ---

        # 4. Create the final, paper-accurate formula from your paper
        final_hamiltonian_formula = MathTex(
            r"""
            H(M, N, d) = \frac{1}{2N^{d}} \Bigg\{ 
            &\sum_{1 \le i \neq j \le M} (i^d+j^d) + \sum_{M+1 \le i \neq j \le N} (i^d+j^d) 
            - &\sum_{i=1}^M \sum_{j=M+1}^N (i^d+j^d) - \sum_{i=M+1}^N \sum_{j=1}^M (i^d+j^d) \Bigg\}
            """,
            font_size=26
        )
        # Color the key variables for clarity
        final_hamiltonian_formula.set_color_by_tex_to_color_map({
            "H": H_COLOR, "M": S_COLOR, "d": D_COLOR
        })

        # 5. Animate the final transformation from the intermediate to the final formula
        self.play(
            ReplacementTransform(intermediate_formula, final_hamiltonian_formula)
        )
        self.wait(5)


def calculate_min_J_o(J):
    N = len(J)
    H_l = []
    for M in range(N + 1):
        s = np.array([1]*M + [-1]*(N - M), dtype=float)
        H = 0.5 * s @ J @ s
        H_l.append(H)
    
    min_H_idx = np.argmin(H_l)
    return min_H_idx

import math

class GroundStateCalculationPart2(Scene):
    def construct(self):
        # --- CONFIGURATION & FORMULAE SETUP ---
        S_COLOR = BLUE_D
        D_COLOR = YELLOW_D
        H_COLOR = GREEN
        
        # 1) Final H(M,N,d) formula
        final_hamiltonian_formula = MathTex(
            r"""
            H(M, N, d) = \frac{1}{2N^{d}} \Bigg\{
            &\sum_{1 \le i \neq j \le M} (i^d+j^d)
            + \sum_{M+1 \le i \neq j \le N} (i^d+j^d)
            - \sum_{i=1}^M \sum_{j=M+1}^N (i^d+j^d)
            - \sum_{i=M+1}^N \sum_{j=1}^M (i^d+j^d)
            \Bigg\}
            """,
            font_size=26
        ).set_color(YELLOW_D)
        self.add(final_hamiltonian_formula)
        self.wait()
        self.play(final_hamiltonian_formula.animate.to_edge(UP, buff=1))
        self.wait()

        # 2) Faulhaber’s formula
        faulhaber_formula = MathTex(
            r"F^{d}(N)", r"=", r"\sum_{i=1}^N i^d",
            r"=", r"\sum_{r=0}^{d} \frac{(-1)^r B_r}{d+1} \binom{d+1}{r} N^{d+1-r}",
            font_size=36
        ).move_to(ORIGIN)
        faulhaber_formula.set_color_by_tex_to_color_map({
            r"F^{d}(N)": PURPLE_A,
            r"\sum_{i=1}^N i^d": YELLOW_D,
        })
        # color the B_r in orange
        faulhaber_formula[4][10:12].set_color(ORANGE)
        self.play(Write(faulhaber_formula))
        self.wait()

        # 3) Shortened H
        shorten_H = MathTex(
            r"H(M,N,d) = \frac{1}{N^{d}}\bigl((N - 2M - 1)F^d(N) + (4M-2N)F^{d}(M)\bigr)",
            font_size=36
        ).move_to(ORIGIN)
        self.play(
            faulhaber_formula.animate.to_edge(UP, buff=1),
            ReplacementTransform(final_hamiltonian_formula, shorten_H)
        )
        self.wait()

        # 4) M_g formula
        M_g_formula = MathTex(
            r"M_{g}^{(N, d)} = \arg\min_M H(M, N, d)",
            font_size=32
        ).next_to(shorten_H, DOWN, buff=1)
        self.play(Write(M_g_formula))
        self.wait()

        # --- SEQUENCE 3: VISUALIZING THE MINIMIZATION OVER M ---
        formulas_panel = VGroup(faulhaber_formula, shorten_H, M_g_formula)
        self.play(formulas_panel.animate.scale(0.8).to_edge(LEFT, buff=0.5))
        self.wait()

        # fixed parameters
        d_val = 1
        N0 = 10

        # 2) Setup the viz area+box (never changes)
        viz_area = Square(side_length=3.5, color=None)
        viz_area.to_edge(RIGHT, buff=1.0)
        viz_box  = SurroundingRectangle(viz_area, color=WHITE, buff=0.2)
        viz_box_tex = MathTex(fr"J^{{(N = {N0}, d = {d_val})}}", font_size=36).next_to(viz_box, UP, buff=0.2)
        self.add(viz_area)
        self.play(Write(viz_box_tex), 
                  Create(viz_box))

        # helper to build & return a VGroup of dots for a given N
        def build_dots(N):
            matrix = J_order(N, d=d_val)
            norm   = matrix / matrix.max()
            idxs   = [(i, j) for i in range(N) for j in range(N)]
            group  = VGroup(*[
                Dot(
                    viz_area.get_corner(UL)
                    + (i/(N-1))*RIGHT*viz_area.width
                    + (j/(N-1))*DOWN*viz_area.height,
                    radius=viz_area.width/(3*N),
                    color=BLACK
                )
                for i, j in idxs
            ])
            # initial yellow–gradient
            for dot, (i, j) in zip(group, idxs):
                dot.set_color(interpolate_color(BLACK, YELLOW, norm[i, j]))
            return group, norm, idxs

        # function to recolor a dot-group at integer m_thres
        def recolor_group(group, idxs, norm, m_thres):
            for dot, (i, j) in zip(group, idxs):
                inside = (j < m_thres and i < m_thres) or (i >= m_thres and j >= m_thres)
                c = BLUE if inside else RED
                dot.set_color(interpolate_color(BLACK, c, norm[i, j]))


        def recolor_group_animated(group, idxs, norm, m_thres):
            animations = []
            for dot, (i, j) in zip(group, idxs):
                inside = (j < m_thres and i < m_thres) or (i >= m_thres and j >= m_thres)
                color = BLUE if inside else RED
                anim = dot.animate.set_color(interpolate_color(BLACK, color, norm[i, j]))
                animations.append(anim)
            return animations

        # create initial N=10 grid + M-tracker + brace+label
        dots, j_norm, index_list = build_dots(N0)
        self.play(FadeIn(dots))
        self.wait()

        M_init      = N0 // 2
        M_g_tracker = ValueTracker(M_init)

        # one-off color at M_init
        self.play(
            *recolor_group_animated(dots, index_list, j_norm, M_init),
            Transform(
                viz_box_tex,
                MathTex(
                    fr"J^{{(N = {N0}, d = {d_val})}} \odot (\mathbf{{s}}\mathbf{{s}}^T)",
                    font_size=36
                ).next_to(viz_box, UP, buff=0.2),
            ),
            run_time=3
        )
        self.wait()
        N_grid = N0
        curly_bracket   = Brace(viz_box, DOWN, buff=0.1)
        curly_bracket_tex = always_redraw(lambda: MathTex(
            fr"\displaystyle H\bigl(M = {math.ceil(M_g_tracker.get_value())}, "
            fr"N = {N_grid}, d = {d_val}\bigr)",
            font_size=32
        ).next_to(curly_bracket, DOWN, buff=0.2))

        self.play(FadeIn(curly_bracket), Write(curly_bracket_tex))
        self.wait()

        # attach a *single* updater to recolor via ceil(tracker)
        def updater(group):
            M_val = M_g_tracker.get_value()
            for dot, (i, j) in zip(group, index_list):
                inside = (j < M_val and i < M_val) or (i >= M_val and j >= M_val)
                c = BLUE if inside else RED
                dot.set_color(interpolate_color(BLACK, c, j_norm[i, j]))
            return group
        
        dots.clear_updaters()
        dots.add_updater(updater)

        # 3) animate M from center→edge→0→true minimizer
        true_minimizer = calculate_min_J_o(J_order(N0, d=d_val))
        self.play(M_g_tracker.animate.set_value(N0), run_time=2.5)
        self.play(M_g_tracker.animate.set_value(0),  run_time=2.5)
        self.play(M_g_tracker.animate.set_value(true_minimizer), run_time=2.5)
        self.wait(2)

        # --- SEQUENCE 4: DENSIFYING THE GRID (LARGER N) ---
        for new_N in [15, 30, 45]:
            # 1) Update our Python variable so the brace lambda picks it up:
            N_grid = new_N

            # 2) Build the new dot grid and its norm/indices:
            new_dots, new_norm, new_idxs = build_dots(N_grid)

            # 3) Pre‐colour it to the *current* M so it never flashes yellow:
            current_m = math.ceil(M_g_tracker.get_value())
            recolor_group(new_dots, new_idxs, new_norm, current_m)

            # 4) Fade out the old dots, fade in the new:
            self.play(
                FadeOut(dots),
                FadeIn(new_dots),
                run_time=1.5
            )
            self.wait(0.5)

            # 5) Rebind our references & reattach the updater:
            dots       = new_dots
            j_norm     = new_norm
            index_list = new_idxs

            dots.clear_updaters()
            dots.add_updater(updater)

            # 6) Reset M to centre, then replay the sweep:
            midpoint = N_grid // 2
            M_g_tracker.set_value(midpoint)
            self.play(M_g_tracker.animate.set_value(N_grid), run_time=2.5)
            self.play(M_g_tracker.animate.set_value(0),      run_time=2.5)
            true_minimizer = calculate_min_J_o(J_order(N_grid, d=d_val))
            self.play(M_g_tracker.animate.set_value(true_minimizer), run_time=2.5)
            self.wait(1)

        self.wait(2)
    
        # 1) create the “implies” part
        deriv_condition = MathTex(
            r"\Rightarrow",
            r"\frac{\partial H(M,\,N,\,d)}{\partial q} = 0",
            font_size=32
        )

        # write next to M_g_formula
        deriv_condition.next_to(M_g_formula, RIGHT, buff=0.2)

        # group them together
        implied_group = VGroup(M_g_formula, deriv_condition)

        # create the q explanation
        q_explanation = MathTex(r"q = \frac{M}{N}", font_size=32).next_to(implied_group, DOWN, buff=0.2)
        # play animations
        self.play(Write(deriv_condition))
        self.play(implied_group.animate.next_to(shorten_H, DOWN, buff=0.2))
        q_explanation.next_to(implied_group, DOWN, buff=0.2)
        self.wait(1)
        self.play(Write(q_explanation))
        self.wait(2)

        # group the faulhaber_formula, shorten_H, implied_group, q_explanation

        new_formulas_panel = VGroup(faulhaber_formula, shorten_H, implied_group, q_explanation)

        # remove everything else and move the new_formulas_panel to the middle
        self.play(
            FadeOut(viz_area),
            FadeOut(viz_box),
            FadeOut(viz_box_tex),
            FadeOut(dots),
            FadeOut(curly_bracket),
            FadeOut(curly_bracket_tex)
        )

        # Move the grouped formulas back to center
        self.play(new_formulas_panel.animate.scale(1.25).move_to(ORIGIN))
        self.wait(2)

        # (This code follows immediately after the previous sequence)
        # self.wait(2)
        Q_COLOR = YELLOW
        # --- SEQUENCE 5: THE FINAL DERIVATION ---
        deriv_condition[1].next_to(shorten_H, DOWN, buff=0.2)
        # 1. Isolate the key formulas for the derivation
        self.play(
            FadeOut(faulhaber_formula, M_g_formula, q_explanation, deriv_condition[0]),
            VGroup(shorten_H, deriv_condition[1]).animate.to_edge(UP, buff=1.0)
        )
        deriv_condition = deriv_condition[1]

        self.wait(2)

        # 2. Start with Eq. (11) from your paper
        # We need to minimize H_tilde = M*F(N) + (N-2M)*F(M)
        h_tilde_intro = Text("We only need to minimize the M-dependent terms:", font_size=28)
        h_tilde_formula = MathTex(
            r"\tilde{H}(M, N, d) = M F^{d}(N) + (N-2M)F^{d}(M)", font_size=36
        )
        VGroup(h_tilde_intro, h_tilde_formula).arrange(DOWN, buff=0.3).next_to(deriv_condition, DOWN, buff=0.8)

        self.play(Write(h_tilde_intro))
        self.play(Write(h_tilde_formula))
        self.wait(3)

        # 3. Take the derivative to get Eq. (12)
        # Replacing dH/dq=0 with its expanded form
        eq12 = MathTex(
            r"N\left\{F^{d}(N) - 2 F^{d}(M) + (1-2q) \frac{\partial F^{d}(M)}{\partial q}\right\} = 0",
            font_size=36
        )
        eq12.next_to(h_tilde_formula, 0.1*DOWN, buff=0)

        self.play(
            FadeOut(h_tilde_intro),
            ReplacementTransform(h_tilde_formula, eq12)
        )
        self.wait(3)

        # 4. Show the derivative of F^d(M) (Eq. 13)
        df_formula = MathTex(
            r"\frac{\partial F^{d}(M)}{\partial M} = d F^{d-1}(M) + (-1)^{d} B_d", font_size=36
        )
        df_formula.set_color_by_tex("B_d", ORANGE)
        df_formula.move_to(ORIGIN)
        self.play(Write(df_formula))
        self.wait(2)

        # 5. Substitute it in to get Eq. (14)
        eq14 = MathTex(
            r"F^{d}(N) - 2 F^{d}(M) + (1-2q)N \{dF^{d-1}(M) + (-1)^{d} B_d \}  = 0",
            font_size=36
        ).move_to(eq12)
        self.play(
            ReplacementTransform(VGroup(eq12, df_formula), eq14)
        )
        self.wait(3)

        # 6. The Large N approximation for Faulhaber's formula
        large_n_approx = MathTex(
            r"\text{For large N, } F^{d}(N) \approx \frac{N^{d+1}}{d+1}", font_size=36
        ).next_to(eq14, DOWN, buff=0.8)
        
        self.play(Write(large_n_approx))
        self.wait(3)

        # 7. Substitute the approximation to get Eq. (16)
        eq16 = MathTex(
            r"\frac{N^{d+1}}{d+1}(1-2q^{d+1}) + (1-2q)N\left\{(qN)^d + \dots\right\} = 0",
            font_size=36
        ).move_to(eq14)
        
        self.play(ReplacementTransform(VGroup(eq14, large_n_approx), eq16))
        self.wait(3)

        # 8. Simplify to the final, beautiful result (Eq. 17)
        final_equation = MathTex(
            r"1 + (1+d)q^d - 2(2+d)q^{d+1} = 0",
            font_size=48
        )
        final_equation.set_color_by_tex("q", Q_COLOR)
        final_equation.set_color_by_tex("d", D_COLOR)

        # Show a title for the final equation
        final_title = Text("The Master Equation of Ground State", font_size=36, color=GOLD)
        final_title.to_edge(UP, buff=1.5)

        # Animate the final transformation
        self.play(
            FadeOut(shorten_H, deriv_condition),
            ReplacementTransform(eq16, final_equation),
            Write(final_title)
        )
        self.wait(8)


from scipy.optimize import root

class MasterEquationofGroundState(Scene):
    # Constants
    N = 1000
    left = -2.4  # lower log exponent for symlog threshold

    def _func_positive(self, p, d):
        return 1 + (1 + d) * p**d - 2 * (2 + d) * p**(d + 1)

    def _MasterGroundState(self, domain):
        roots = []
        for d in domain:
            sol = root(
                self._func_positive,
                x0=1,
                args=(d,),
                tol=1e-30,
                method='lm',
                options={'maxiter': 1_000_000, 'ftol': 1e-30}
            )
            roots.append(sol.x[0])
        return np.array(roots)

    def construct(self):
        # 1) Title + equation
        eq = MathTex(r"1 + (1+d)q^d - 2(2+d)q^{d+1} = 0", font_size=48).set_color(YELLOW_D)
        title = Text("The Master Equation of Ground State", font_size=36, color=GOLD)
        title.to_edge(UP, buff=1.5)
        self.add(eq, title)
        self.play(eq.animate.next_to(title, DOWN, buff=0.2))
        grouped_eq = VGroup(eq, title)
        self.wait()
        self.play(grouped_eq.animate.scale(0.8).to_corner(UP))
        self.wait(0.5)

        # 2) Rebuild domain here so we can change expo at will:
        expo = 4.1   # ← change this to any exponent (e.g. 4.5) and the plot will follow
        r1 = np.logspace(self.left, expo, 2000)
        r2 = -np.logspace(-1e-6, self.left, 2000)
        domain = np.sort(np.concatenate((r2, r1)))

        # derive min/max from the actual domain
        d_min, d_max = domain[0], domain[-1]

        # symlog transform
        C = 10**self.left
        def symlog(x): return np.arcsinh(x / C)
        x_min_t, x_max_t = symlog(d_min), symlog(d_max)

        # 3) Build axes
        axes = Axes(
            x_range=[0, x_max_t - x_min_t, 1],
            y_range=[0, 1.1, 0.2],
            x_length=5 * 1.608,
            y_length=5,
            axis_config={"color": TEAL, 
                         "include_tip": True, 
                         "tip_width": 0.15,
                         "tip_height": 0.15},

            x_axis_config={"include_ticks": False, "include_numbers": False},
            y_axis_config={
                "decimal_number_config": {"num_decimal_places": 1},
                "numbers_to_include": np.arange(0.2, 1.1, 0.2),
                "font_size": 24
            },
        )

        # manual ticks & labels (will now respect your dynamic d_max)
        all_ticks = [-1e0, -1e-1, -1e-2, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4]
        ticks = VGroup()
        labels = []
        for v in all_ticks:
            xp = symlog(v) - x_min_t
            ticks.add(Line(
                axes.x_axis.n2p(xp),
                axes.x_axis.n2p(xp) + DOWN*0.1,
                color=TEAL, stroke_width=2
            ))
            exp = int(np.log10(abs(v)))
            lab = MathTex(f'{"-" if v<0 else ""}10^{{{exp}}}', font_size=24)
            lab.next_to(axes.x_axis.n2p(xp), DOWN, buff=0.2)
            labels.append(lab)
        # zero label
        if d_min < 0 < d_max:
            zp = symlog(0) - x_min_t
            zero_lab = MathTex("0", font_size=24).next_to(axes.x_axis.n2p(zp), DOWN, buff=0.2)
            ticks.add(Line(
                axes.x_axis.n2p(zp),
                axes.x_axis.n2p(zp) + DOWN*0.1,
                color=TEAL, stroke_width=2))
            labels.append(zero_lab)

        axes.x_axis.add(*labels)
        axis_labels = axes.get_axis_labels(
            x_label=MathTex("d", font_size=42),
            y_label=MathTex("q", font_size=42)
        )

        # Group and shift entire graph down
        axes_group = VGroup(axes, axis_labels, ticks).shift(DOWN * 0.5)
        self.play(Create(axes_group), run_time=2)

        # 4) Compute and plot
        q_vals = self._MasterGroundState(domain)
        mask = (np.isfinite(q_vals))
        x_plot = symlog(domain[mask]) - x_min_t

        curve = axes.plot_line_graph(
            x_values=x_plot,
            y_values=q_vals[mask],
            line_color=WHITE,
            add_vertex_dots=False
        )
        self.play(Create(curve), run_time=3)
        self.wait(2)

# --- CONFIGURATION (Consistent Colors) ---
PLUS_ONE_COLOR = BLUE_D
MINUS_ONE_COLOR = RED_D
J_COLOR = YELLOW
H_COLOR = GREEN
Q_COLOR = YELLOW # For the 'q' ratio and domain walls
D_COLOR = ORANGE # For the 'd' parameter
DOMAIN_COLORS = [PLUS_ONE_COLOR, MINUS_ONE_COLOR, GREEN_D, ORANGE]

class TheLingeringDoubt(Scene):
    def construct(self):
        # --- SEQUENCE 1: The "Perfect" State ---
        
        # 1. Start with the problem statement
        problem_text = Text(
            "His entire Master Equation was built on a foundation...",
            font_size=36
        ).to_edge(UP, buff=1.0)
        
        assumption_text = Text(
            "...a powerful, but unproven, assumption.",
            font_size=36
        ).next_to(problem_text, DOWN)
        
        self.play(Write(problem_text))
        self.wait(2)
        self.play(Write(assumption_text))
        self.wait(3)

        # 2. Show the clean, postulated ground state
        postulate = Text("Postulate: The ground state is always two clusters.", font_size=40, color=Q_COLOR)
        postulate.move_to(ORIGIN)
        
        self.play(
            FadeOut(problem_text, assumption_text),
            Write(postulate)
        )
        self.wait(2)

        s_g_perfect = VGroup(*[
            Dot(radius=0.15, color=PLUS_ONE_COLOR if i < 7 else MINUS_ONE_COLOR)
            for i in range(12)
        ]).arrange(RIGHT, buff=0.3).next_to(postulate, DOWN, buff=0.8)

        self.play(LaggedStart(*[Create(d) for d in s_g_perfect], lag_ratio=0.1))
        self.wait(2)
        
        # --- SEQUENCE 2: The Doubt Creeps In ---
        
        # 1. The flicker of imperfection
        what_if_text = Text("But what if the true ground state was more complicated?", font_size=36)
        what_if_text.move_to(postulate.get_center())

        s_g_imperfect = s_g_perfect.copy()
        s_g_imperfect[3].set_color(MINUS_ONE_COLOR) # The flipped spin

        self.play(
            ReplacementTransform(postulate, what_if_text),
            Transform(s_g_perfect, s_g_imperfect),
            run_time=2
        )
        self.wait(3)

        # 2. The chaos of possibilities
        for _ in range(5):
            # Create a new random state each time
            random_state_dots = s_g_perfect.copy()
            # More clusters for visual effect
            breakpoints = sorted(random.sample(range(1, 12), k=random.randint(3, 5)))
            
            color_idx = 0
            start_idx = 0
            for bp in breakpoints:
                for i in range(start_idx, bp):
                    random_state_dots[i].set_color(DOMAIN_COLORS[color_idx % len(DOMAIN_COLORS)])
                start_idx = bp
                color_idx += 1
            # Color the last segment
            for i in range(start_idx, 12):
                random_state_dots[i].set_color(DOMAIN_COLORS[color_idx % len(DOMAIN_COLORS)])
                
            self.play(Transform(s_g_perfect, random_state_dots), run_time=0.3)
        
        self.wait(2)

        # 3. The final question mark
        final_question_mark = MathTex("?", font_size=160, color=RED)
        final_question_mark.move_to(what_if_text.get_center())
        
        self.play(
            FadeOut(s_g_perfect),
            ReplacementTransform(what_if_text, final_question_mark),
            run_time=1.5
        )
        self.wait(4)


# --- CONFIGURATION (Consistent Colors) ---
PLUS_ONE_COLOR = BLUE_D
MINUS_ONE_COLOR = RED_D
J_COLOR = YELLOW
H_COLOR = GREEN
Q_COLOR = YELLOW # For the 'q' ratio and domain walls
D_COLOR = ORANGE # For the 'd' parameter
DOMAIN_COLORS = [PLUS_ONE_COLOR, MINUS_ONE_COLOR, GREEN_D, ORANGE]

class TheContinuousLeap(Scene):
    def construct(self):
        # --- NEW: CUSTOM TEX TEMPLATE FOR \sgn ---
        # This is the fix. We define a new template that includes the amsmath
        # package and explicitly declares the \sgn operator.
        sgn_template = TexTemplate()
        sgn_template.add_to_preamble(r"\usepackage{amsmath}")
        sgn_template.add_to_preamble(r"\DeclareMathOperator{\sgn}{sgn}")

        # --- PREPARATION ---
        q_values_initial = [0.3, 0.65, 0.85]
        N_INITIAL = 20
        N_FINAL = 400

        # --- HELPER FUNCTIONS (UNCHANGED) ---
        def get_domain_info(n, q_vals):
            if n <= 1: return [{'size': n, 'color': DOMAIN_COLORS[0], 'spin_val': 1}]
            boundaries = sorted([0] + list(q_vals) + [1])
            domain_info = []
            bin_edges = [b * (n - 1) for b in boundaries]
            spin_counts = np.histogram(np.arange(n), bins=bin_edges)[0].tolist()
            if len(spin_counts) < len(boundaries) - 1:
                spin_counts.append(n - sum(spin_counts))
            for i, count in enumerate(spin_counts):
                if count > 0:
                    domain_info.append({
                        'size': count, 'color': DOMAIN_COLORS[i % len(DOMAIN_COLORS)],
                        'spin_val': 1 if i % 2 == 0 else -1
                    })
            return domain_info

        def create_refined_s_T_group(n, domain_info):
            if n == 0: return VGroup()
            s_T_label = MathTex(r"\pmb{s}^T = ", font_size=40)
            l_bracket = MathTex("[", font_size=72)
            r_bracket = MathTex("]", font_size=72)
            domain_blocks = VGroup()
            for i, info in enumerate(domain_info):
                block = Rectangle(
                    height=0.4, width=info['size'] * 0.02 + 0.1,
                    fill_color=info['color'], fill_opacity=0.8,
                    stroke_width=1, stroke_color=WHITE
                )
                brace = Brace(block, DOWN, buff=SMALL_BUFF)
                counter = Integer(info['size'], font_size=28).next_to(brace, DOWN, buff=SMALL_BUFF)
                counter.set_color(info['color'])
                domain_blocks.add(VGroup(block, brace, counter))
            domain_blocks.arrange(RIGHT, buff=0.1)
            return VGroup(s_T_label, l_bracket, domain_blocks, r_bracket).arrange(RIGHT, buff=0.15)

        def create_colored_discrete_plot(n, domain_info, axes_obj):
            plot = VGroup()
            if n <= 1: return plot
            spin_index = 0
            for info in domain_info:
                for _ in range(info['size']):
                    x_pos = spin_index / (n - 1)
                    dot = Dot(axes_obj.c2p(x_pos, info['spin_val']), color=info['color'], radius=0.04)
                    stem = Line(axes_obj.c2p(x_pos, 0), dot.get_center(), stroke_width=1.5, color=info['color'])
                    plot.add(VGroup(stem, dot))
                    spin_index += 1
            return plot

        # --- ANIMATION PART 1 (UNCHANGED) ---
        axes = Axes(
            x_range=[0, 1.05, 0.2], y_range=[-1.5, 1.5, 1],
            x_length=11, y_length=3.5, axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": np.arange(0, 1.1, 0.2)}
        ).to_edge(DOWN, buff=1.0)
        x_label = axes.get_x_axis_label(MathTex("x = i/N"))
        plot_title = MathTex("s_i", font_size=40).next_to(axes.y_axis, LEFT, buff=0.3)
        s_T_display_group = VGroup().to_edge(UP, buff=0.5)
        N_tracker = ValueTracker(N_INITIAL)
        s_T_display_group.add_updater(lambda mob: mob.become(create_refined_s_T_group(int(N_tracker.get_value()), get_domain_info(int(N_tracker.get_value()), q_values_initial))).to_edge(UP, buff=0.5))
        discrete_plot = VGroup()
        discrete_plot.add_updater(lambda mob: mob.become(create_colored_discrete_plot(int(N_tracker.get_value()), get_domain_info(int(N_tracker.get_value()), q_values_initial), axes)))
        
        self.add(s_T_display_group, discrete_plot)
        self.play(Create(axes), Write(x_label), Write(plot_title), run_time=1)
        self.play(N_tracker.animate.set_value(N_FINAL), run_time=5, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)

        s_T_display_group.clear_updaters()
        discrete_plot.clear_updaters()

        def create_continuous_function(q_vals, axes_obj):
            func = VGroup()
            boundaries = sorted([0] + list(q_vals) + [1])
            for i in range(len(boundaries) - 1):
                spin_val = 1 if i % 2 == 0 else -1
                start_p, end_p = axes_obj.c2p(boundaries[i], spin_val), axes_obj.c2p(boundaries[i+1], spin_val)
                func.add(Line(start_p, end_p, color=WHITE, stroke_width=6))
            for q_val in q_vals:
                func.add(DashedLine(axes_obj.c2p(q_val, -1), axes_obj.c2p(q_val, 1), color=Q_COLOR, stroke_width=3))
                label = MathTex(f"q_{list(q_vals).index(q_val)+1}", color=Q_COLOR, font_size=36).next_to(axes_obj.c2p(q_val,0), DOWN)
                func.add(label)
            return func

        continuous_function_initial = create_continuous_function(q_values_initial, axes)
        final_symbolic_text = MathTex("S(x, \\mathbf{q})", font_size=48).move_to(s_T_display_group)

        self.play(
            FadeOut(discrete_plot, s_T_display_group, shift=UP),
            FadeIn(continuous_function_initial, shift=UP),
            Write(final_symbolic_text),
            run_time=1.5
        )
        self.wait(2)

        # --- ANIMATION PART 2: GENERALITY OF S(x, q) (UNCHANGED) ---
        generality_text = Text("This can represent any number of clusters (Λ+1)...", font_size=32)
        generality_text.next_to(final_symbolic_text, DOWN, buff=0.2)
        self.play(Write(generality_text))
        self.wait(1)
        q_vals_1 = [0.6]; func_1 = create_continuous_function(q_vals_1, axes)
        self.play(Transform(continuous_function_initial, func_1), run_time=1.5); self.wait(1.5)
        q_vals_2 = [0.4, 0.8]; func_2 = create_continuous_function(q_vals_2, axes)
        self.play(Transform(continuous_function_initial, func_2), run_time=1.5); self.wait(1.5)
        q_vals_many = np.linspace(0.1, 0.9, 10); func_many = create_continuous_function(q_vals_many, axes)
        self.play(Transform(continuous_function_initial, func_many), run_time=2); self.wait(2)
        
        def create_general_schematic(axes_obj):
            schematic = VGroup()
            schematic.add(Line(axes_obj.c2p(0, 1), axes_obj.c2p(0.2, 1), color=WHITE, stroke_width=6))
            schematic.add(DashedLine(axes_obj.c2p(0.2, 1), axes_obj.c2p(0.2, -1), color=Q_COLOR, stroke_width=3))
            schematic.add(Line(axes_obj.c2p(0.2, -1), axes_obj.c2p(0.35, -1), color=WHITE, stroke_width=6))
            ellipsis_y_up = axes_obj.c2p(0,1)[1]; ellipsis_y_down = axes_obj.c2p(0,-1)[1]
            schematic.add(MathTex(r"\dots").scale(2).move_to(axes_obj.c2p(0.5, ellipsis_y_up)))
            schematic.add(MathTex(r"\dots").scale(2).move_to(axes_obj.c2p(0.5, ellipsis_y_down)))
            schematic.add(Line(axes_obj.c2p(0.65, -1), axes_obj.c2p(0.8, -1), color=WHITE, stroke_width=6))
            schematic.add(DashedLine(axes_obj.c2p(0.8, -1), axes_obj.c2p(0.8, 1), color=Q_COLOR, stroke_width=3))
            schematic.add(Line(axes_obj.c2p(0.8, 1), axes_obj.c2p(1.0, 1), color=WHITE, stroke_width=6))
            labels = VGroup(
                MathTex("q_1", color=Q_COLOR).next_to(axes_obj.c2p(0.2,0),DOWN),
                MathTex("q_2", color=Q_COLOR).next_to(axes_obj.c2p(0.35,0),DOWN),
                MathTex("q_{\Lambda-1}", color=Q_COLOR).next_to(axes_obj.c2p(0.65,0),DOWN),
                MathTex("q_{\Lambda}", color=Q_COLOR).next_to(axes_obj.c2p(0.8,0),DOWN)
            )
            schematic.add(labels)
            return schematic
        general_schematic = create_general_schematic(axes)
        self.play(Transform(continuous_function_initial, general_schematic), run_time=2)
        self.wait(2)

        self.play(FadeOut(generality_text))
        
        # --- THIS IS THE FIX ---
        # We pass our custom template to the MathTex object that needs it.
        s_formula = MathTex(
            r"S(x, \mathbf{q}) = (-1)^\Lambda \prod_{\alpha=1}^{\Lambda} \sgn(x-q_{\alpha})",
            font_size=42,
            tex_template=sgn_template  # Pass the custom template here
        ).next_to(final_symbolic_text, DOWN, buff=0.3)
        self.play(Write(s_formula))
        self.wait(5)


        # --- ANIMATION PART 3: Morphing the Hamiltonian (UNCHANGED) ---
        self.play(
            FadeOut(axes, x_label, plot_title, continuous_function_initial),
            VGroup(final_symbolic_text, s_formula).animate.move_to(UP*2.5)
        )
        self.wait(1)
        
        H_part_d = MathTex("H = \\frac{1}{2} \\sum_{i,j}").set_color_by_tex("H", H_COLOR)
        J_part_d = MathTex("J_{ij}").set_color(J_COLOR)
        s_i_part_d = MathTex("s_i").set_color(PLUS_ONE_COLOR)
        s_j_part_d = MathTex("s_j").set_color(MINUS_ONE_COLOR)
        discrete_H = VGroup(H_part_d, J_part_d, s_i_part_d, s_j_part_d).arrange(RIGHT, buff=0.2).scale(1.2)
        self.play(Write(discrete_H))
        self.wait(2)
        
        H_part_c = MathTex(r"H = \frac{N^2}{2} \int_0^1 \! \int_0^1").set_color_by_tex("H", H_COLOR)
        J_part_c = MathTex("(x^d + y^d)").set_color_by_tex_to_color_map({"d":D_COLOR})
        J_part_c.get_part_by_tex("x").set_color(J_COLOR); J_part_c.get_part_by_tex("y").set_color(J_COLOR)
        s_x_part_c = MathTex(r"S(x, \mathbf{q})").set_color(PLUS_ONE_COLOR)
        s_y_part_c = MathTex(r"S(y, \mathbf{q})").set_color(MINUS_ONE_COLOR)
        integrand_part_c = MathTex(r"\,dx\,dy").set_color(WHITE)
        continuous_H_group = VGroup(H_part_c, J_part_c, s_x_part_c, s_y_part_c, integrand_part_c).arrange(RIGHT, buff=0.2).scale(1.1)
        
        self.play(
            FadeOut(final_symbolic_text, s_formula),
            ReplacementTransform(H_part_d, H_part_c),
            ReplacementTransform(J_part_d, J_part_c),
            ReplacementTransform(s_i_part_d, s_x_part_c),
            ReplacementTransform(s_j_part_d, s_y_part_c),
            FadeIn(integrand_part_c, shift=RIGHT),
            run_time=2.5
        )
        self.wait(5)

# Define colors for consistency
H_COLOR = YELLOW
J_COLOR = BLUE
Q_COLOR = GREEN
D_COLOR = RED
PLUS_ONE_COLOR = GREEN_B
MINUS_ONE_COLOR = RED_B
LAMBDA_COLOR = PURPLE

class ContinuousHDerivation(Scene):
    def construct(self):
        # --- PART 1: Recap The Analytical Hamiltonian ---
        H_part_c = MathTex(r"H = \frac{N^2}{2} \int_0^1 \! \int_0^1").set_color_by_tex("H", H_COLOR)
        J_part_c = MathTex("(x^d + y^d)").set_color_by_tex_to_color_map({"d": D_COLOR, "x": J_COLOR, "y": J_COLOR})
        s_x_part_c = MathTex(r"S(x, \mathbf{q})").set_color(PLUS_ONE_COLOR)
        s_y_part_c = MathTex(r"S(y, \mathbf{q})").set_color(MINUS_ONE_COLOR)
        integrand_part_c = MathTex(r"\,dx\,dy").set_color(WHITE)
        continuous_H_group = VGroup(H_part_c, J_part_c, s_x_part_c, s_y_part_c, integrand_part_c).arrange(RIGHT, buff=0.15).scale(1.0)
        self.play(Write(continuous_H_group))
        self.wait(1)

        part1 = MathTex(r"H_{\Lambda}", r"(d, \mathbf{q})", r"=", r"\frac{N^2}{1+d}").set_color_by_tex_to_color_map({"H": H_COLOR, r"\Lambda": LAMBDA_COLOR, "d": D_COLOR, r"\mathbf{q}": Q_COLOR})
        part2 = MathTex(r"\Bigg( (-1)^{\Lambda} + 2\sum_{\alpha=1}^{\Lambda} (-1)^{\alpha+1}q_\alpha \Bigg)").set_color_by_tex_to_color_map({r"\Lambda": LAMBDA_COLOR, "q": Q_COLOR})
        part3 = MathTex(r"\Bigg( (-1)^{\Lambda} + 2\sum_{\alpha=1}^{\Lambda} (-1)^{\alpha+1}q_\alpha^{d+1} \Bigg)").set_color_by_tex_to_color_map({r"\Lambda": LAMBDA_COLOR, "q": Q_COLOR, "d": D_COLOR})
        analytical_H_formula = VGroup(part1, part2, part3).arrange(RIGHT, buff=0.2).scale(0.85).move_to(ORIGIN)
        self.play(ReplacementTransform(continuous_H_group, analytical_H_formula), run_time=2.5)
        self.wait(2)
        self.play(analytical_H_formula.animate.to_edge(UP, buff=0.5).scale(0.8))
        
        # --- PART 2: The Λ=1 Case (Appendix C) ---
        title_case1 = Tex(r"Case 1: Two Clusters ($\Lambda = 1$)", font_size=40).set_color(GREEN)
        title_case1.next_to(analytical_H_formula, DOWN, buff=0.5)
        self.play(Write(title_case1))

        h1_formula = MathTex(r"H_1 = \frac{N^2}{1+d} (2q_1-1)(2q_1^{d+1}-1)").set_color_by_tex_to_color_map({"H": H_COLOR, "d": D_COLOR, "q_1": Q_COLOR})
        appendix_c_result = MathTex(r"\text{Minimizing gives... } H_1(q_1) = -N^2(2q_1-1)^2 q_1^d").set_color_by_tex_to_color_map({"H": H_COLOR, "q_1": Q_COLOR, "d": D_COLOR})
        case1_proof_group = VGroup(h1_formula, appendix_c_result).arrange(DOWN, buff=0.7)
        case1_proof_group.next_to(title_case1, DOWN, buff=0.4)
        self.play(FadeIn(case1_proof_group, shift=DOWN))
        self.wait(2)

        result_box = SurroundingRectangle(appendix_c_result, color=GREEN, buff=0.2)
        result_text = Tex(r"$H_1 < 0$", r" (Always Negative!)", font_size=36).next_to(result_box, DOWN)
        result_text[0].set_color(GREEN)
        self.play(Create(result_box), Write(result_text))
        self.wait(3)
        self.play(FadeOut(VGroup(title_case1, case1_proof_group, result_box, result_text)))

        # --- PART 3: The Λ >= 2 Case (Appendix D) with Full Detail ---
        title_case2 = Tex(r"Case 2: More than Two Clusters ($\Lambda \geq 2$)", font_size=40).set_color(RED)
        title_case2.next_to(analytical_H_formula, DOWN, buff=0.5)
        self.play(Write(title_case2))

        # --- Step 1: Present the core equation from Appendix D ---
        insight_text = Tex(r"At a critical point, the sum of derivatives for adjacent boundaries is zero:").scale(0.8)
        sum_deriv_full_eq = MathTex(
            r"\frac{\partial H_{\Lambda}}{\partial q_j} + \frac{\partial H_{\Lambda}}{\partial q_{j+1}} =",
            r"2(-1)^j(q_j^d - q_{j+1}^d)",
            r"\times",
            r"\left[(-1)^\Lambda + 2\sum_{n = 1}^\Lambda(-1)^{n+1}q_n\right]",
            r"= 0"
        ).scale(0.9)
        step1_group = VGroup(insight_text, sum_deriv_full_eq).arrange(DOWN, buff=0.4)
        step1_group.next_to(title_case2, DOWN, buff=0.4)
        self.play(Write(step1_group))
        self.wait(4)

        # --- Step 2: Analyze the two factors ---
        term_A = sum_deriv_full_eq[1]
        term_B = sum_deriv_full_eq[3]
        brace_A = Brace(term_A, DOWN, color=BLUE)
        brace_B = Brace(term_B, DOWN, color=ORANGE)
        label_A = brace_A.get_text("Term A").set_color(BLUE)
        label_B = brace_B.get_text("Term B").set_color(ORANGE)
        self.play(GrowFromCenter(brace_A), GrowFromCenter(brace_B), Write(label_A), Write(label_B))
        self.wait(2)
        
        # --- Step 3: Rule out Term A ---
        analysis_group = VGroup(
            Tex("Since boundaries are ordered ($q_j < q_{j+1}$),", font_size=32),
            Tex(r"Term A cannot be zero.", font_size=32)
        ).arrange(DOWN).to_edge(DOWN, buff=0.5)
        self.play(Write(analysis_group))
        
        cross = Cross(VGroup(term_A, brace_A, label_A), stroke_color=RED, stroke_width=6)
        self.play(Create(cross))
        self.wait(3)

        # --- Step 4: Conclude Term B must be zero ---
        conclusion_text = Tex("Therefore, Term B *must* be zero.", font_size=32).move_to(analysis_group)
        self.play(FadeOut(analysis_group, cross), FadeIn(conclusion_text))
        self.play(Indicate(VGroup(term_B, brace_B, label_B), color=ORANGE, scale_factor=1.2))
        self.wait(3)
        self.play(FadeOut(VGroup(insight_text, sum_deriv_full_eq, brace_A, brace_B, label_A, label_B, conclusion_text)))

        # --- Step 5: The final punchline ---
        final_condition = MathTex(
            r"\text{So, at any critical point: }",
            r"(-1)^{\Lambda} + 2\sum_{n=1}^{\Lambda} (-1)^{n+1}q_n = 0"
        ).set_color_by_tex_to_color_map({r"\Lambda": LAMBDA_COLOR, "q": Q_COLOR})
        final_condition.next_to(title_case2, DOWN, buff=0.7)
        self.play(Write(final_condition))
        self.wait(2)

        q_factor_box_on_formula = SurroundingRectangle(analytical_H_formula[1], color=RED, buff=0.05)
        zero_box_on_proof = SurroundingRectangle(final_condition[1], color=RED, buff=0.2)
        arrow = Arrow(zero_box_on_proof.get_top(), q_factor_box_on_formula.get_bottom(), buff=0.1, color=RED)
        
        self.play(Create(zero_box_on_proof), Create(q_factor_box_on_formula), GrowArrow(arrow))
        
        final_result_case2 = MathTex(r"\Rightarrow H_{\Lambda} = 0").scale(1.2).set_color(RED)
        final_result_case2.next_to(zero_box_on_proof, DOWN, buff=0.4)
        self.play(Write(final_result_case2))
        self.wait(4)
        self.play(FadeOut(VGroup(title_case2, final_condition, zero_box_on_proof, q_factor_box_on_formula, arrow, final_result_case2)))
        
        # --- PART 4: Boundary Case (Interface Shedding) ---
        boundary_title = Tex(r"Boundary Case: Domains Merge (e.g., $q_{\Lambda} \to 1$)", font_size=40).set_color(ORANGE)
        boundary_title.next_to(analytical_H_formula, DOWN, buff=0.5)
        reduction_eq = MathTex(r"H_{\Lambda}(q_{\Lambda} \to 1) \longrightarrow H_{\Lambda-1}").set_color_by_tex(r"\Lambda", LAMBDA_COLOR)
        cascade = Tex(r"The system sheds interfaces to find lower energy:", font_size=32)
        cascade_math = MathTex(r"\Lambda \to \Lambda-1 \to \dots \to 1").set_color(LAMBDA_COLOR)
        boundary_group = VGroup(reduction_eq, cascade, cascade_math).arrange(DOWN, buff=0.6)
        boundary_group.next_to(boundary_title, DOWN, buff=0.4)
        self.play(Write(boundary_title), Write(boundary_group))
        self.wait(4)
        self.play(FadeOut(boundary_title), FadeOut(boundary_group))

        # --- PART 5: Final Conclusion ---
        
        # Animate the formula to the top to serve as a header
        self.play(analytical_H_formula.animate.scale(0.9).to_edge(UP, buff=0.7))

        # Create the central dividing line
        line = Line(UP * 2.5, DOWN * 3.5, color=GRAY)
        self.play(Create(line))
        
        # --- Left Column: The Winning Case (Λ=1) ---
        
        # Define a stable anchor point for the left column
        left_anchor = line.get_center() + LEFT * (self.camera.frame_width / 4)
        
        # Create the elements for the left column
        title_L1 = Tex(r"Case $\Lambda=1$", font_size=42).set_color(GREEN)
        result_L1 = MathTex(r"H_1 < 0", font_size=60).set_color(GREEN)
        label_L1 = Tex("Stable, Energetically", "Favorable Ground State", font_size=32)
        
        # Group and position them relative to the anchor
        group_L1 = VGroup(title_L1, result_L1, label_L1).arrange(DOWN, buff=0.7)
        group_L1.move_to(left_anchor)

        # --- Right Column: The Unstable Case (Λ>=2) ---
        
        # Define a stable anchor point for the right column
        right_anchor = line.get_center() + RIGHT * (self.camera.frame_width / 4)

        # Create the elements for the right column
        title_L2 = Tex(r"Case $\Lambda \geq 2$", font_size=42).set_color(RED)
        result_L2 = MathTex(r"H_{\Lambda} = 0", font_size=60).set_color(RED)
        label_L2 = Tex("Unstable or Higher Energy", "(Decays to $\Lambda=1$)", font_size=32)
        
        # Group and position them relative to the anchor
        group_L2 = VGroup(title_L2, result_L2, label_L2).arrange(DOWN, buff=0.7)
        group_L2.move_to(right_anchor)

        # --- Animate the final comparison ---
        self.play(
            Write(group_L1),
            Write(group_L2),
            run_time=2
        )
        self.wait(6)


# now in the next scene, we want to focus on this ordered J again. We want to show what this truly represents. We can show a table that has the name of richest people, and some other people that are poor. a ranked table. this rank is the index i, and we can show that again what interaction means. as an example, we can show number 1 and 2 have the interaction 1^d+2^d (with other constants) and the 1^d+1000^d, and so on (we'll show all of the possibilities for total of 4 people, two rich and two poor). and discuss how this can be extended to the other ranked systems. and show the obvious conclusion that such system turns into two opposing poles (such as class gap). we say each pole agrees with itself but disagrees with the other one. 

# Add these imports at the top of your file
from scipy.optimize import root
import numpy as np

# Add this class to your interactive_main.py file

# --- CONFIGURATION (Consistent Colors) ---
PLUS_ONE_COLOR = BLUE_D
MINUS_ONE_COLOR = RED_D
J_COLOR = YELLOW
H_COLOR = GREEN
Q_COLOR = YELLOW # For the 'q' ratio and domain walls
D_COLOR = ORANGE # For the 'd' parameter

class TheGreatSchism(Scene):
    # Helper function to solve the Master Equation for q given d
    def _get_q_for_d(self, d):
        def equation(q):
            # Clamp q to avoid math errors for d<0
            q_safe = np.clip(q, 1e-9, 1.0)
            return 1 + (1 + d) * q_safe**d - 2 * (2 + d) * q_safe**(d + 1)
        
        # Use root finding to solve the equation for q
        sol = root(equation, x0=0.5, tol=1e-9)
        if sol.success:
            return np.clip(sol.x[0], 0, 1)
        return 0.5 # Default to 0.5 on failure
    def construct(self):
        # --- SEQUENCE 1: The J_ij Rule and the Ranked Society Analogy ---
        
        # (The code from the previous step goes here, I've kept it for context)
        # 1. Start with the glowing formula
        interaction_formula = MathTex(r"J_{ij} \propto i^d + j^d", font_size=60)
        interaction_formula.set_color_by_tex_to_color_map({"J": J_COLOR, "d": D_COLOR})
        self.play(FadeIn(interaction_formula, scale=0.8))
        self.play(interaction_formula.animate.set_color(YELLOW_A), run_time=2, rate_func=there_and_back)
        self.wait(3)
        self.play(FadeOut(interaction_formula))
        self.wait(0.5)

        # 2. Introduce the ranked table
        table_data = [
            [r"\text{Rank (i)}", r"\text{Name}", r"\text{Status/Wealth}"],
            ["1", r"\text{Titan Corp.}", r"\$1.2 \text{ Trillion}"],
            ["2", r"\text{Innovate Inc.}", r"\$980 \text{ Billion}"],
            [r"\vdots", r"\vdots", r"\vdots"],
            ["999", r"\text{Alice}", r"\$52,000"],
            ["1000", r"\text{Bob}", r"\$48,000"],
        ]
        table = Table(
            table_data, include_outer_lines=True, line_config={"stroke_width": 2, "color": TEAL},
            h_buff=0.5, element_to_mobject=MathTex
        ).scale(0.6)
        table.get_rows()[0].set_color(YELLOW)
        self.play(Create(table))
        self.wait(4)
        self.play(FadeOut(table))
        self.wait(0.5)

        # 3. Helper function
        def create_interaction_viz(rank1_str, rank2_str, is_high_tension=False):
            node1 = VGroup(Circle(radius=0.4, color=WHITE), Text(rank1_str, font_size=24)).move_to(LEFT * 2)
            node2 = VGroup(Circle(radius=0.4, color=WHITE), Text(rank2_str, font_size=24)).move_to(RIGHT * 2)
            line_color = ORANGE if is_high_tension else TEAL
            line_stroke = 6 if is_high_tension else 3
            line = Line(node1.get_right(), node2.get_left(), color=line_color, stroke_width=line_stroke)
            if is_high_tension:
                line.add_updater(lambda m: m.set_color(random.choice([ORANGE, RED_A, YELLOW_B])))
            j_label = MathTex(f"J_{{{rank1_str}, {rank2_str}}}", color=J_COLOR).next_to(line, UP, buff=0.2)
            calc_label = MathTex(r"\propto", f"{rank1_str}^d + {rank2_str}^d").next_to(line, DOWN, buff=0.2)
            calc_label.set_color_by_tex("d", D_COLOR)
            return VGroup(node1, node2, line, j_label, calc_label)

        # 4. Animate interactions
        top_top_viz = create_interaction_viz("1", "2").shift(UP*2)
        self.play(FadeIn(top_top_viz, shift=DOWN)); self.wait(3)
        bottom_bottom_viz = create_interaction_viz("999", "1000")
        self.play(FadeIn(bottom_bottom_viz, shift=DOWN)); self.wait(3)
        top_bottom_viz = create_interaction_viz("1", "1000", is_high_tension=True).shift(DOWN*2)
        self.play(FadeIn(top_bottom_viz, shift=DOWN)); self.wait(4)

        # Cleanup for the next sequence
        self.play(FadeOut(top_top_viz, bottom_bottom_viz, top_bottom_viz))
        self.wait(1)


        # --- SEQUENCE 2: Inevitable Polarization (REVISED & DYNAMIC) ---

        # 1. Bring back the Hamiltonian
        hamiltonian = MathTex(r"H = \sum s_i J_{ij} s_j", font_size=60)
        hamiltonian.set_color_by_tex_to_color_map({"H": H_COLOR, "J_{ij}": J_COLOR, "s_i": PLUS_ONE_COLOR, "s_j": MINUS_ONE_COLOR})
        self.play(Write(hamiltonian))
        self.wait(3) # "Now, remember the system's one and only goal..."
        self.play(FadeOut(hamiltonian))
        
        # 2. Set up the dynamic visualization elements
        total_width = 10
        viz_height = 4
        
        d_tracker = ValueTracker(1.0) # Start with d=1

        # This object is redrawn every frame based on d_tracker's value
        polarization_viz = always_redraw(lambda: 
            VGroup(
                # Blue rectangle (width based on q)
                Rectangle(
                    width=self._get_q_for_d(d_tracker.get_value()) * total_width,
                    height=viz_height,
                    fill_color=PLUS_ONE_COLOR, fill_opacity=0.9, stroke_width=0
                ),
                # Red rectangle (width is the remainder)
                Rectangle(
                    width=(1 - self._get_q_for_d(d_tracker.get_value())) * total_width,
                    height=viz_height,
                    fill_color=MINUS_ONE_COLOR, fill_opacity=0.9, stroke_width=0
                )
            ).arrange(RIGHT, buff=0)
        )
        
        # 3. Set up the controller for 'd'
        d_dial = NumberLine(
            x_range=[-2, 6, 1],
            length=8,
            color=WHITE,
            label_direction=DOWN,
            include_numbers=True
        ).to_edge(DOWN, buff=1.5)
        d_label = MathTex("d", color=D_COLOR).next_to(d_dial, LEFT)
        
        pointer = Arrow(start=UP, end=DOWN, color=D_COLOR, max_tip_length_to_length_ratio=0.25).scale(0.5)
        pointer.add_updater(lambda m: m.next_to(d_dial.n2p(d_tracker.get_value()), UP))

        q_value_text = always_redraw(lambda:
            MathTex(
                f"q = {self._get_q_for_d(d_tracker.get_value()):.2f}",
                font_size=42, color=Q_COLOR
            ).next_to(polarization_viz, UP, buff=0.4)
        )
        
        # 4. Animate the appearance of the visualization
        self.play(
            Create(polarization_viz),
            Create(d_dial),
            Write(d_label),
            GrowArrow(pointer),
            Write(q_value_text)
        )
        self.wait(2)

        # 5. Animate the change in polarization as 'd' changes
        self.play(
            d_tracker.animate.set_value(4.0),
            run_time=3, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)
        
        self.play(
            d_tracker.animate.set_value(-0.5),
            run_time=3, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)
        
        self.play(
            d_tracker.animate.set_value(1.0),
            run_time=2, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(2)

        
        # (This code replaces everything from the final d-tracker animation onwards)

        # Animate the d-tracker to its final position
        self.play(
            d_tracker.animate.set_value(1.0),
            run_time=2, rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(2)

        # "Bake" the final state of the dynamic Mobjects by removing their updaters.
        # Now they are just static objects and can be transformed safely.
        polarization_viz.clear_updaters()
        pointer.clear_updaters()
        q_value_text.clear_updaters()
        
        # 6. Group the (now static) visualization, scale it, and move it up
        pol_group = VGroup(polarization_viz, d_dial, d_label, pointer, q_value_text)
        
        self.play(
            pol_group.animate.scale(0.8).to_edge(UP, buff=1.0)
        )
        self.wait(1)

        # 7. Final text and conclusion
        schism_text = Text("The Great Schism", font_size=48, color=YELLOW)
        conclusion_text = Text("A direct consequence of the ranked interaction", font_size=32)
        
        # Arrange the final text below the moved group
        final_text_group = VGroup(schism_text, conclusion_text).arrange(DOWN, buff=0.4)
        final_text_group.next_to(pol_group, DOWN, buff=0.8)

        self.play(Write(schism_text))
        self.wait(1)
        self.play(Write(conclusion_text))
        self.wait(5)
        
        # Cleanup for the very final scene
        self.play(FadeOut(pol_group, final_text_group))
        self.wait(1)

# Now, in the next and final scene, we reveal that this student is Amirhossein Rezaei, which is me! me! And reveal this picture (I'm the one on right, the middle is Alireza Rezaei, the left is Mahmood Hasani). (We don't mention Halataei as he's not in the picture.) and we also show a picture of the paper (https://arxiv.org/abs/2411.19604). I want it to be poetic, like the end of AlphaGo documentary. To show them how significant and incredible this is.

class TheFinalReveal(Scene):
    def construct(self):
        # --- SEQUENCE 1: The Reveal of the Student ---
        
        question_text = Text("Where do new ideas come from?", font_size=42, line_spacing=1.5)
        self.play(Write(question_text)); self.wait(4)
        student_text = Text("Our story began with a young physics student...", font_size=36)
        self.play(ReplacementTransform(question_text, student_text)); self.wait(3)
        name_text = Text("Amirhossein Rezaei", font_size=48, color=YELLOW)
        self.play(ReplacementTransform(student_text, name_text)); self.wait(3)

        # --- SEQUENCE 2: The Team and the Paper ---
        self.play(FadeOut(name_text))
        
        try:
            photo = ImageMobject("us.jpg")
            photo.set_height(6.0)
            self.play(FadeIn(photo, shift=DOWN)); self.wait(2)

            # --- THIS IS THE FIX ---
            # 1. Create the labels first, without positioning them.
            # The narration order is Mahmood, Alireza, Amirhossein.
            mahmood_label = Text("Mahmood Hasani", font_size=28)
            alireza_label = Text("Alireza Rezaei", font_size=28)
            amir_label = Text("Amirhossein Rezaei", font_size=28)

            # 2. Group them and arrange them relative to each other.
            names_group = VGroup(mahmood_label, alireza_label, amir_label)
            names_group.arrange(RIGHT, buff=0.5) # Arrange them horizontally with a buffer

            # 3. Now, position the entire group cleanly under the photo.
            names_group.next_to(photo, DOWN, buff=0.3)
            
            # The LaggedStart animation will still work on the individual elements.
            self.play(LaggedStart(
                Write(mahmood_label), Write(alireza_label), Write(amir_label),
                lag_ratio=0.7, run_time=3
            )); self.wait(4)

            paper_image = ImageMobject("paper_image.png")
            paper_image.set_height(photo.get_height() + 0.5)
            paper_image.move_to(photo.get_center())

            self.play(
                FadeOut(name_text, names_group),
                FadeOut(photo, scale=0.95),
                FadeIn(paper_image, scale=1.05),
                run_time=2
            )
            self.wait(5)
            
            # --- SEQUENCE 3: The Coda ---
            self.play(FadeOut(paper_image))
            
            final_photo = ImageMobject("us.jpg").set_height(6.0).move_to(ORIGIN)
            final_quote = Text(
                "The journey of discovery only leads to new, more beautiful questions.",
                font_size=32, slant=ITALIC, color=GRAY_B
            ).next_to(final_photo, DOWN, buff=0.5)

            self.play(FadeIn(final_photo))
            self.wait(2)
            self.play(Write(final_quote))
            self.wait(10)

        except FileNotFoundError as e:
            self.play(FadeOut(name_text))
            error_msg_text = f"Image file not found: {e.filename}"
            error_msg = Text(error_msg_text, color=RED)
            self.play(Write(error_msg))
            self.wait(3)
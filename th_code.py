from manim import *
import numpy as np
from scipy.special import gamma

class ExponentialWeibullComparison(Scene):
    def construct(self):
        # ========== تنظیمات کلی ==========
        frame_rate = 30
        total_time = 330  # 5.5 دقیقه (330 ثانیه)
        self.camera.frame_rate = frame_rate
       
        # ========== بخش ۱: شروع (30 ثانیه) ==========
        title = Text("توزیع نمایی و وایبول", font_size=48, font="B Nazanin")
        subtitle = Text("از حافظه‌ی ریاضی تا واقعیت فیزیکی", font_size=36, font="B Nazanin")
        en_title = Text("Exponential & Weibull Distributions", font_size=32, color=BLUE)
        en_subtitle = Text("From Math Memory to Physical Reality", font_size=24, color=BLUE)

        VGroup(title, subtitle, en_title, en_subtitle).arrange(DOWN, buff=0.5)
        self.play(
            Write(title),
            Write(subtitle),
            FadeIn(en_title, shift=UP),
            FadeIn(en_subtitle, shift=UP),
            run_time=3
        )
        self.wait(27)
        self.play(FadeOut(*self.mobjects))
       
        # ========== بخش ۲: توزیع نمایی (105 ثانیه) ==========
        # معرفی
        intro_exp = Text("توزیع نمایی (Exponential Distribution)", font_size=36, font="B Nazanin")
        desc_exp = Text("مدل‌سازی زمان بین رخدادهای تصادفی مستقل", font_size=28, font="B Nazanin")
        VGroup(intro_exp, desc_exp).arrange(DOWN, buff=0.5)
        self.play(Write(intro_exp), Write(desc_exp))
        self.wait(5)
       
        # مثال بصری
        timeline = NumberLine(x_range=[0, 10], length=10, include_numbers=True)
        events = [Dot(timeline.n2p(np.random.uniform(0, 10))) for _ in range(8)]
        self.play(Create(timeline), run_time=2)
        self.play(LaggedStart(*[Create(e) for e in events]), run_time=3)
        self.wait(5)
        self.play(FadeOut(timeline), FadeOut(*events))
       
        # فرمول‌ها
        pdf_exp = MathTex(
            r"f(x;\lambda) = \lambda e^{-\lambda x} \quad \text{برای} \quad x \geq 0",
            substrings_to_isolate=["\\lambda", "x"]
        )
        cdf_exp = MathTex(
            r"F(x;\lambda) = 1 - e^{-\lambda x}",
            substrings_to_isolate=["\\lambda", "x"]
        )
        VGroup(pdf_exp, cdf_exp).arrange(DOWN, buff=0.7)
        self.play(Write(pdf_exp))
        self.wait(5)
        self.play(Write(cdf_exp))
        self.wait(10)
       
        # نمودار PDF
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 1.5],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": [1,2,3,4]},
            y_axis_config={"numbers_to_include": [0.5, 1.0]},
        )
        labels = ax.get_axis_labels(
            Text("زمان (x)", font="B Nazanin").scale(0.7),
            Text("چگالی احتمال f(x)", font="B Nazanin").scale(0.7)
        )
       
        lam = 1
        graph = ax.plot(
            lambda x: lam * np.exp(-lam * x),
            color=YELLOW,
            stroke_width=4
        )
        graph_label = MathTex(r"\lambda = 1", color=YELLOW).next_to(graph, UR)
       
        self.play(
            FadeOut(pdf_exp),
            FadeOut(cdf_exp),
            Create(ax),
            Create(labels),
            run_time=2
        )
        self.play(Create(graph), Write(graph_label))
        self.wait(10)
       
        # میانگین و واریانس
        mean = MathTex(r"E[X] = \frac{1}{\lambda}").to_edge(UP)
        var = MathTex(r"\text{واریانس}(X) = \frac{1}{\lambda^2}").next_to(mean, DOWN)
        self.play(Write(mean), Write(var))
        self.wait(10)
       
        # ویژگی بی‌حافظه‌بودن
        self.play(FadeOut(mean), FadeOut(var))
        prop_title = Text("ویژگی بی‌حافظه‌بودن (Memoryless Property)", font_size=36, font="B Nazanin")
        self.play(Write(prop_title.to_edge(UP)))

        formula = MathTex(
            r"P(X > s + t \mid X > s) = P(X > t) \quad \forall s,t \geq 0"
        )
        self.play(Write(formula.next_to(prop_title, DOWN)))
       
        # مثال بصری
        bus_stop = SVGMobject("bus").scale(0.5).to_edge(LEFT)
        person = Dot(color=GREEN).next_to(bus_stop, RIGHT)
        timeline = NumberLine(x_range=[0, 10], length=6).next_to(person, RIGHT)
        self.play(FadeIn(bus_stop), Create(person), Create(timeline))
       
        # انیمیشن انتظار
        s_point = timeline.n2p(3)
        t_point = timeline.n2p(7)
        s_dot = Dot(s_point, color=RED)
        t_dot = Dot(t_point, color=PURPLE)
       
        self.play(person.animate.move_to(s_dot), run_time=3)
        self.play(Create(s_dot), Write(Text("s", font_size=24).next_to(s_dot, UP)))
        self.wait(2)
        self.play(
            person.animate.move_to(t_dot),
            Create(t_dot),
            Write(Text("t", font_size=24).next_to(t_dot, UP)),
            run_time=4
        )
        self.wait(10)
        self.play(FadeOut(*self.mobjects[1:]))
       
        # ========== بخش ۳: مشکل دنیای واقعی (30 ثانیه) ==========
        problem_title = Text("مشکل در دنیای واقعی", font_size=42, font="B Nazanin", color=RED)
        self.play(Write(problem_title))
        self.wait(5)
       
        # مثال لامپ
        bulb = SVGMobject("lightbulb").scale(1.5)
        time_label = Text("زمان: 0 ساعت", font="B Nazanin").next_to(bulb, DOWN)
        self.play(Create(bulb), Write(time_label))
       
        for hours in [1000, 5000, 10000]:
            self.play(
                bulb.animate.set_color(interpolate_color(WHITE, RED, hours/10000)),
                time_label.animate.become(Text(f"زمان: {hours} ساعت", font="B Nazanin").next_to(bulb, DOWN)),
                run_time=3
            )
       
        cross = Cross(bulb, stroke_width=10, color=RED)
        self.play(Create(cross))
        self.wait(10)
        self.play(FadeOut(*self.mobjects))
       
        # ========== بخش ۴: توزیع وایبول (90 ثانیه) ==========
        intro_weibull = Text("توزیع وایبول (Weibull Distribution)", font_size=36, font="B Nazanin")
        desc_weibull = Text("مدل‌سازی سیستم‌های با فرسودگی", font_size=28, font="B Nazanin")
        VGroup(intro_weibull, desc_weibull).arrange(DOWN, buff=0.5)
        self.play(Write(intro_weibull), Write(desc_weibull))
        self.wait(5)
       
        # فرمول‌ها
        pdf_weibull = MathTex(
            r"f(x;\lambda,k) = \frac{k}{\lambda} \left( \frac{x}{\lambda} \right)^{k-1} e^{-(x/\lambda)^k}",
            substrings_to_isolate=["\\lambda", "k", "x"]
        )
        param_desc = Text("پارامتر شکل (k) تعیین کننده رفتار توزیع", font_size=28, font="B Nazanin")
        VGroup(pdf_weibull, param_desc).arrange(DOWN, buff=1)
        self.play(Transform(desc_weibull, param_desc), Write(pdf_weibull))
        self.wait(10)
       
        # نمودار با kهای مختلف
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 1.5],
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": [1,2,3,4]},
        )
        colors = [RED, YELLOW, GREEN, BLUE]
        k_values = [0.5, 1, 2, 4]
        graphs = VGroup()
        labels = VGroup()
       
        for k, color in zip(k_values, colors):
            graph = ax.plot(
            lambda x, k=k: (k / 1) * (x / 1) ** (k - 1) * np.exp(- (x / 1) ** k),
            color=color,
            stroke_width=4
            )
            label = MathTex(f"k = {k}", color=color).next_to(
            graph.point_from_proportion(0.7), UR
            )
            graphs.add(graph)
            labels.add(label)

       
        self.play(
            FadeOut(pdf_weibull),
            FadeOut(desc_weibull),
            Create(ax),
            run_time=2)
        self.play(LaggedStart(
            *[Create(g) for g in graphs],
            *[Write(l) for l in labels],
            lag_ratio=0.5
        ))
       
        # توضیحات رفتار k
        k_text = VGroup(
            Text("k < 1: نرخ خرابی کاهشی", font="B Nazanin", font_size=24, color=RED),
            Text("k = 1: توزیع نمایی", font="B Nazanin", font_size=24, color=YELLOW),
            Text("k > 1: نرخ خرابی افزایشی", font="B Nazanin", font_size=24, color=GREEN),
            Text("k ≈ 3.4: تقریباً نرمال", font="B Nazanin", font_size=24, color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(DR)
       
        self.play(Write(k_text))
        self.wait(15)
        self.play(FadeOut(*self.mobjects))
       
        # ========== بخش ۵: مثال‌های واقعی (45 ثانیه) ==========
        examples_title = Text("کاربردهای دنیای واقعی", font_size=42, font="B Nazanin")
        self.play(Write(examples_title))
        self.wait(5)
       
        # مثال‌ها
        human = SVGMobject("person").set_color(GREEN).scale(0.8)
        human_label = Text("طول عمر انسان (k>1)", font="B Nazanin", font_size=24).next_to(human, DOWN)
       
        bearing = SVGMobject("gear").set_color(BLUE).scale(0.8)
        bearing_label = Text("خرابی بلبرینگ (k>1)", font="B Nazanin", font_size=24).next_to(bearing, DOWN)
       
        paint = SVGMobject("paint").set_color(YELLOW).scale(0.8)
        paint_label = Text("خشک شدن رنگ (k≈0.7)", font="B Nazanin", font_size=24).next_to(paint, DOWN)
       
        examples = VGroup(
            VGroup(human, human_label),
            VGroup(bearing, bearing_label),
            VGroup(paint, paint_label)
        ).arrange(RIGHT, buff=1)
       
        self.play(FadeOut(examples_title), LaggedStart(
            FadeIn(examples[0], shift=UP),
            FadeIn(examples[1], shift=UP),
            FadeIn(examples[2], shift=UP),
            lag_ratio=0.3
        ))
        self.wait(30)
        self.play(FadeOut(*self.mobjects))
       
        # ========== بخش ۶: جدول مقایسه‌ای (30 ثانیه) ==========
        table_title = Text("مقایسه توزیع‌ها", font_size=42, font="B Nazanin")
        self.play(Write(table_title))
        self.wait(3)
       
        # ساخت جدول
        table = Table(
            [
                ["ویژگی", "توزیع نمایی", "توزیع وایبول"],
                ["پارامترها", r"$\lambda$ (نرخ)", r"$\lambda, k$ (مقیاس، شکل)"],
                ["ویژگی بی‌حافظه‌بودن", "دارد (همیشه)", "فقط وقتی k=1"],
                ["نرخ خرابی", "ثابت", "متغیر (وابسته به k)"],
                ["کاربردها", "صف‌ها، رخدادهای نادر", "قابلیت اطمینان، طول عمر"]
            ],
            col_labels=[Text(c, font="B Nazanin") for c in ["", "نمایی", "وایبول"]],
            include_outer_lines=True
        ).scale(0.6)
       
        # استایل‌دهی به جدول
        table.get_entries((1,1)).set_color(YELLOW)
        table.get_entries((1,2)).set_color(GREEN)
        table.get_entries((1,3)).set_color(GREEN)
        table.get_row(1).set_color(HEADER_COLOR)
       
        self.play(table_title.animate.scale(0.7).to_edge(UP), Create(table))
        self.wait(20)
       
        # پایان
        end_text = Text("پایان", font_size=72, font="B Nazanin")
        self.play(FadeOut(table_title), FadeOut(table), Write(end_text))
        self.wait(10)
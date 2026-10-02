"""Chapter 2, sections 2.9 and 2.11 (Cairo renderer, 2D).

RelativeHomotopy      -- a homotopy relative to a subset A: the deformation moves
                         everything except A, whose points are pinned for all s.
RadialDeformationRetract -- R^n minus the origin deformation retracts onto S^{n-1}
                         via H(x,s) = (1-s)x + s x/|x|.

Render: tools/bg.sh h ch02_retracts.py RelativeHomotopy RadialDeformationRetract
"""
from manim import *
import numpy as np

C0, C1, CNOW, CA = BLUE_C, RED_C, YELLOW, GREEN_B


def caption(tex, size=30):
    return Tex(tex, font_size=size).to_corner(UR, buff=0.4).shift(DOWN * 0.85)


# =================================================== 2.9  homotopy relative to A
L = 2.5          # X = [-L, L]   (math units)
AW = 0.45        # A = [-AW, AW]
XS, YS = 1.9, 1.0
AXIS_Y = -2.35
CURVE_Y = -0.55


def P(x, y):
    return np.array([x * XS, CURVE_Y + y * YS, 0.0])


def AX(x):
    return np.array([x * XS, AXIS_Y, 0.0])


def base(x):
    return 0.55 * np.sin(1.7 * x) + 0.18 * np.cos(2.9 * x)


def dev(x):
    u = (abs(x) - AW) / (L - AW)
    if u <= 0.0:
        return 0.0
    w = np.sin(np.pi * 0.8 * u) ** 1.2
    return (1.15 if x > 0 else -0.95) * w


def phi(x, s):
    return base(x) + s * dev(x)


def curve(s, color, width=6, op=1.0):
    return ParametricFunction(lambda x: P(x, phi(x, s)), t_range=[-L, L, 0.01],
                              color=color, stroke_width=width, stroke_opacity=op)


class RelativeHomotopy(Scene):
    def construct(self):
        axis = Line(AX(-L - 0.25), AX(L + 0.25), color=GREY_B, stroke_width=3)
        aseg = Line(AX(-AW), AX(AW), color=CA, stroke_width=9)
        alab = MathTex("A", color=CA).scale(0.8).next_to(aseg, DOWN, buff=0.18)
        xlab = MathTex("X", color=GREY_A).scale(0.7).next_to(axis, RIGHT, buff=0.15)
        self.play(Create(axis), FadeIn(xlab), run_time=1.0)
        self.play(Create(aseg), FadeIn(alab), run_time=0.8)

        c0, c1 = curve(0.0, C0), curve(1.0, C1)
        l0 = MathTex(r"\varphi_0", color=C0).scale(0.8).move_to(P(-L, phi(-L, 0.0)) + LEFT * 0.55)
        l1 = MathTex(r"\varphi_1", color=C1).scale(0.8).move_to(P(L, phi(L, 1.0)) + RIGHT * 0.55)
        self.play(Create(c0), FadeIn(l0), run_time=1.4)
        self.play(Create(c1), FadeIn(l1), run_time=1.4)

        guides = VGroup(*[DashedLine(AX(sg * AW), P(sg * AW, phi(sg * AW, 0.0)),
                                     color=GREY_B, stroke_width=2, dash_length=0.1)
                          for sg in (-1, 1)])
        pins = VGroup(*[Dot(P(sg * AW, phi(sg * AW, 0.0)), color=CA, radius=0.075)
                        for sg in (-1, 1)])
        self.play(Create(guides), FadeIn(pins), run_time=1.0)

        cap = caption(r"$\varphi_0|_A=\varphi_1|_A$")
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(0.6)

        ghosts = VGroup(*[curve(v, interpolate_color(C0, C1, v), width=3, op=0.38)
                          for v in np.linspace(0.12, 0.88, 6)])
        self.play(Create(ghosts), run_time=1.6)

        st = ValueTracker(0.0)
        live = always_redraw(lambda: curve(st.get_value(), CNOW, width=7))
        slab = always_redraw(lambda: MathTex(r"\Phi_s,\ s=%.2f" % st.get_value(),
                                             color=CNOW).scale(0.72).to_corner(UL, buff=0.45))
        self.add(live, slab)
        cap2 = caption(r"every point of $A$ is pinned for all $s$")
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.6)

        self.play(st.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
        self.wait(0.5)
        self.play(st.animate.set_value(0.0), run_time=3.0, rate_func=smooth)
        self.wait(0.4)
        self.play(st.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        self.wait(1.0)


# ============================== 2.11  R^n minus 0  deformation retracts onto S^{n-1}
R = 1.72
O = np.array([-0.9, -0.35, 0.0])


def Q(r, th):
    return O + R * r * np.array([np.cos(th), np.sin(th), 0.0])


def rad(r, s):
    return (1.0 - s) * r + s


def loop_r(th):
    return 1.0 + 0.50 * np.sin(3.0 * th) + 0.17 * np.cos(5.0 * th)


SEEDS = [(r, k * np.pi / 9.0) for r in (0.34, 0.62, 1.44, 1.96) for k in range(18)]


class RadialDeformationRetract(Scene):
    def construct(self):
        st = ValueTracker(0.0)

        rays = VGroup(*[Line(Q(0.18, k * np.pi / 9.0), Q(2.18, k * np.pi / 9.0),
                             color=GREY_E, stroke_width=1.6) for k in range(18)])
        circ = Circle(radius=R, color=CA, stroke_width=10).move_to(O)
        hole = Circle(radius=0.085, color=RED_C, stroke_width=4).move_to(O)
        hlab = MathTex(r"0", color=RED_C).scale(0.7).next_to(hole, DOWN, buff=0.2)
        clab = MathTex(r"S^{1}", color=CA).scale(0.85).move_to(Q(1.33, 0.70 * np.pi))

        self.play(Create(rays), run_time=1.0)
        self.play(Create(circ), FadeIn(clab), run_time=1.2)
        self.play(Create(hole), FadeIn(hlab), run_time=0.7)

        def dot_color(r):
            return BLUE_C if r < 1.0 else ORANGE

        dots = always_redraw(lambda: VGroup(*[
            Dot(Q(rad(r, st.get_value()), th), color=dot_color(r), radius=0.055)
            for (r, th) in SEEDS]))
        trails = always_redraw(lambda: VGroup(*[
            Line(Q(r, th), Q(rad(r, st.get_value()), th),
                 color=dot_color(r), stroke_width=2.2, stroke_opacity=0.55)
            for (r, th) in SEEDS]))
        loop = always_redraw(lambda: ParametricFunction(
            lambda th: Q(rad(loop_r(th), st.get_value()), th),
            t_range=[0, TAU, 0.01], color=PURPLE_B, stroke_width=4.5))

        self.play(FadeIn(dots), Create(loop), run_time=1.6)
        self.add(trails)

        cap = caption(r"$H(x,s)=(1-s)\,x+s\,\dfrac{x}{|x|}$", size=34)
        self.play(FadeIn(cap), run_time=0.6)
        slab = always_redraw(lambda: MathTex(r"s=%.2f" % st.get_value(), color=CNOW)
                             .scale(0.78).to_corner(UL, buff=0.45))
        self.add(slab)
        self.wait(0.5)

        self.play(st.animate.set_value(1.0), run_time=4.5, rate_func=smooth)
        cap2 = caption(r"$S^{1}$ stays fixed throughout (here $n=2$)", size=30)
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.7)
        self.wait(0.8)
        self.play(st.animate.set_value(0.0), run_time=3.0, rate_func=smooth)
        self.wait(0.4)
        self.play(st.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        self.wait(1.0)

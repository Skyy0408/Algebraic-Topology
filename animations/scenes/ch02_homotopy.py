"""Chapter 2: homotopies of paths (OpenGL renderer).

Left : the parameter square [0,1]^2 (t horizontal, s vertical) with the level line at height s.
Right: what happens in the space X.

Render: MANIM_GPU=2 python ../tools/manim_gl.py --renderer=opengl --write_to_movie -qh ch02_homotopy.py <Scene>
"""
from manim import *
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
import numpy as np

C_F, C_G, C_H, C_NOW, C_EPS = BLUE_C, ORANGE, GREEN_C, YELLOW, PURPLE_B
LEFT_C, RIGHT_C = np.array([-3.7, -0.4, 0.0]), np.array([2.9, -0.4, 0.0])
SQ = 2.4                                   # side of the parameter square


def sq_pt(t, s):                            # parameter square -> screen
    return LEFT_C + np.array([(t - 0.5) * SQ, (s - 0.5) * SQ, 0.0])


def frame_square(bottom, top, left_lab, right_lab):
    g = VGroup(Square(SQ, stroke_color=GREY_B, stroke_width=3, fill_color=GREY_E, fill_opacity=0.5).move_to(LEFT_C))
    g.add(MathTex("t", color=GREY_A).scale(0.6).move_to(sq_pt(1.06, -0.1)),
          MathTex("s", color=GREY_A).scale(0.6).move_to(sq_pt(-0.1, 1.06)),
          MathTex(bottom).scale(0.62).move_to(sq_pt(0.5, -0.12)),
          MathTex(top).scale(0.62).move_to(sq_pt(0.5, 1.12)),
          MathTex(left_lab).scale(0.55).move_to(sq_pt(-0.2, 0.5)),
          MathTex(right_lab).scale(0.55).move_to(sq_pt(1.2, 0.5)))
    return g


def level_line(s_t):
    return always_redraw(lambda: Line(sq_pt(0, s_t.get_value()), sq_pt(1, s_t.get_value()),
                                      color=C_NOW, stroke_width=5))


def path_curve(fn, color, width=5, n=200):
    return ParametricFunction(fn, t_range=[0, 1, 1 / n], color=color, stroke_width=width)


def caption(scene, tex, old=None):
    new = Tex(tex, font_size=30).to_corner(UR, buff=0.4).shift(DOWN * 0.85)
    anims = [FadeIn(new)] + ([FadeOut(old)] if old else [])
    return new, anims


# ------------------------------------------------------------------ 1. straight-line homotopy
A_PT, B_PT = np.array([-1.9, -1.0, 0.0]), np.array([1.9, 0.9, 0.0])


def f0(t):
    return RIGHT_C + A_PT + t * (B_PT - A_PT) + np.array([0, 1.5 * np.sin(PI * t), 0])


def f1(t):
    return RIGHT_C + A_PT + t * (B_PT - A_PT) + np.array([0.5 * np.sin(2 * PI * t), -1.3 * np.sin(PI * t), 0])


class StraightLineHomotopy(Scene):
    def construct(self):
        title = MathTex(r"F(t,s) = (1-s)\,f_0(t) + s\,f_1(t)").scale(0.8).to_edge(UP, buff=0.5)
        s = ValueTracker(0.0)
        sq = frame_square(r"f_0", r"f_1", r"f_0(a)", r"f_0(b)")
        line = level_line(s)
        c0, c1 = path_curve(f0, C_F), path_curve(f1, C_G)
        now = always_redraw(lambda: path_curve(lambda t: (1 - s.get_value()) * f0(t) + s.get_value() * f1(t), C_NOW, 6))
        ends = VGroup(Dot(f0(0), color=WHITE), Dot(f0(1), color=WHITE))
        lab = VGroup(MathTex("f_0", color=C_F).scale(0.7).move_to(f0(0.5) + UP * 0.45),
                     MathTex("f_1", color=C_G).scale(0.7).move_to(f1(0.5) + DOWN * 0.45),
                     MathTex("x", color=WHITE).scale(0.6).next_to(ends[0], LEFT, buff=0.15),
                     MathTex("y", color=WHITE).scale(0.6).next_to(ends[1], RIGHT, buff=0.15))
        self.play(FadeIn(title), FadeIn(sq), FadeIn(ends), FadeIn(lab), Create(c0), Create(c1), run_time=1.5)
        self.add(line, now)
        cap, an = caption(self, r"$s = 0$: the path is $f_0$")
        self.play(*an, run_time=0.6)
        for tgt, txt in ((1.0, r"$s = 1$: the path is $f_1$"), (0.0, r"endpoints are fixed for all $s$")):
            cap2, an = caption(self, txt, cap)
            cap = cap2
            self.play(s.animate.set_value(tgt), *an, run_time=3.0, rate_func=smooth)
            self.wait(0.3)
        self.play(FadeOut(cap))
        self.wait(0.4)


# ------------------------------------------------------------------ 2. associativity
P0, P1, P2, P3 = (np.array([-2.0, -1.2, 0]), np.array([-0.7, 1.0, 0]),
                  np.array([1.0, -0.9, 0]), np.array([2.1, 0.9, 0]))


def _leg(a, b, bow):
    m = (a + b) / 2 + np.array([-(b - a)[1], (b - a)[0], 0]) * bow
    return lambda u: (1 - u) ** 2 * a + 2 * (1 - u) * u * m + u ** 2 * b


leg_f, leg_g, leg_h = _leg(P0, P1, 0.18), _leg(P1, P2, -0.15), _leg(P2, P3, 0.2)


def assoc_cuts(s):
    return (s + 1) / 4, (s + 2) / 4


def assoc_pt(t, s):
    c1, c2 = assoc_cuts(s)
    if t <= c1:
        return RIGHT_C + leg_f(4 * t / (1 + s))
    if t <= c2:
        return RIGHT_C + leg_g(4 * t - 1 - s)
    return RIGHT_C + leg_h(1 - 4 * (1 - t) / (2 - s))


class AssociativityReparam(Scene):
    def construct(self):
        title = MathTex(r"(f\cdot g)\cdot h \;\sim\; f\cdot(g\cdot h)").scale(0.85).to_edge(UP, buff=0.5)
        s = ValueTracker(0.0)
        sq = frame_square(r"(f\cdot g)\cdot h", r"f\cdot(g\cdot h)", "", "")
        # slanted cut lines t = (s+1)/4 and t = (s+2)/4
        cuts = VGroup(Line(sq_pt(0.25, 0), sq_pt(0.5, 1), color=GREY_A, stroke_width=2),
                      Line(sq_pt(0.5, 0), sq_pt(0.75, 1), color=GREY_A, stroke_width=2))
        names = VGroup(MathTex("f", color=C_F).scale(0.6).move_to(sq_pt(0.13, 0.5)),
                       MathTex("g", color=C_G).scale(0.6).move_to(sq_pt(0.44, 0.5)),
                       MathTex("h", color=C_H).scale(0.6).move_to(sq_pt(0.8, 0.5)))
        line = level_line(s)
        curves = VGroup(path_curve(lambda u: RIGHT_C + leg_f(u), C_F),
                        path_curve(lambda u: RIGHT_C + leg_g(u), C_G),
                        path_curve(lambda u: RIGHT_C + leg_h(u), C_H))
        dots = VGroup(*[Dot(RIGHT_C + p, color=WHITE, radius=0.05) for p in (P0, P1, P2, P3)])

        # parameter bar under the picture: how [0,1] is shared between f, g, h
        bar_y = RIGHT_C + DOWN * 2.3
        bx = lambda t: bar_y + np.array([(t - 0.5) * 4.4, 0, 0])

        def bar():
            c1, c2 = assoc_cuts(s.get_value())
            g = VGroup(Line(bx(0), bx(c1), color=C_F, stroke_width=11),
                       Line(bx(c1), bx(c2), color=C_G, stroke_width=11),
                       Line(bx(c2), bx(1), color=C_H, stroke_width=11))
            return g
        barG = always_redraw(bar)
        blab = MathTex("[0,1]", color=GREY_A).scale(0.55).next_to(bx(0), LEFT, buff=0.2)
        self.play(FadeIn(title), FadeIn(sq), FadeIn(cuts), FadeIn(names), Create(curves), FadeIn(dots),
                  FadeIn(barG), FadeIn(blab), run_time=1.5)
        self.add(line)

        # a point travelling with the parametrisation F(., s)
        tt = ValueTracker(0.0)
        moving = always_redraw(lambda: Dot(assoc_pt(tt.get_value(), s.get_value()), color=C_NOW, radius=0.09))
        mark = always_redraw(lambda: Dot(bx(tt.get_value()), color=C_NOW, radius=0.07))
        self.add(moving, mark)
        cap, an = caption(self, r"$s=0$: $f$ and $g$ share the first half")
        self.play(*an, tt.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        tt.set_value(0.0)
        cap2, an = caption(self, r"reparametrise: the cuts slide to $\tfrac12, \tfrac34$", cap)
        self.play(s.animate.set_value(1.0), *an, run_time=2.5, rate_func=smooth)
        cap3, an = caption(self, r"$s=1$: same image, $g$ and $h$ share the second half", cap2)
        self.play(*an, tt.animate.set_value(1.0), run_time=3.0, rate_func=linear)
        self.play(FadeOut(cap3))
        self.wait(0.4)


# ------------------------------------------------------------------ 3. f . f-bar ~ constant
def loop_f(u):
    return RIGHT_C + np.array([-1.7 + 3.4 * u, 1.1 * np.sin(PI * u) - 0.3, 0])


def inv_pt(t, s):
    if s < 1e-4:
        return loop_f(0)
    if t <= s / 2:
        return loop_f(2 * t)
    if t <= (2 - s) / 2:
        return loop_f(s)
    return loop_f(2 - 2 * t)


class InversePath(Scene):
    def construct(self):
        title = MathTex(r"f\cdot\bar f \;\sim\; \varepsilon_{f(0)}").scale(0.9).to_edge(UP, buff=0.5)
        s = ValueTracker(1.0)
        sq = frame_square(r"\varepsilon_{f(0)}", r"f\cdot\bar f", "", "")
        tri = VGroup(Line(sq_pt(0, 0), sq_pt(0.5, 1), color=GREY_A, stroke_width=2),
                     Line(sq_pt(1, 0), sq_pt(0.5, 1), color=GREY_A, stroke_width=2))
        names = VGroup(MathTex("f", color=C_F).scale(0.6).move_to(sq_pt(0.22, 0.72)),
                       MathTex(r"\bar f", color=C_G).scale(0.6).move_to(sq_pt(0.78, 0.72)),
                       MathTex("f(s)", color=GREY_A).scale(0.5).move_to(sq_pt(0.5, 0.35)))
        line = level_line(s)
        ghost = path_curve(loop_f, GREY_D, 3)
        out = always_redraw(lambda: path_curve(lambda u: loop_f(u * max(s.get_value(), 1e-3)), C_F, 6))
        back = always_redraw(lambda: path_curve(lambda u: loop_f((1 - u) * max(s.get_value(), 1e-3)), C_G, 6).shift(DOWN * 0.13))
        tip = always_redraw(lambda: Dot(loop_f(s.get_value()), color=C_NOW, radius=0.08))
        base = Dot(loop_f(0), color=WHITE, radius=0.07)
        blab = MathTex("f(0)", color=WHITE).scale(0.55).next_to(base, DOWN, buff=0.15)
        self.play(FadeIn(title), FadeIn(sq), FadeIn(tri), FadeIn(names), FadeIn(ghost),
                  FadeIn(base), FadeIn(blab), run_time=1.2)
        self.add(line, out, back, tip)
        cap, an = caption(self, r"$s=1$: go out along $f$, come back along $\bar f$")
        self.play(*an, run_time=0.8)
        self.wait(0.6)
        cap2, an = caption(self, r"turn back earlier and earlier", cap)
        self.play(s.animate.set_value(0.0), *an, run_time=4.0, rate_func=smooth)
        cap3, an = caption(self, r"$s=0$: the constant path $\varepsilon_{f(0)}$", cap2)
        self.play(*an, run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(cap3))


# ------------------------------------------------------------------ 4. change of base point
X_CEN = RIGHT_C + UP * 0.1
XP, YP = X_CEN + np.array([-1.5, -0.6, 0]), X_CEN + np.array([1.6, 0.4, 0])


def gamma(u):
    return XP + u * (YP - XP) + np.array([0, 0.8 * np.sin(PI * u), 0])


def loop_x(u):
    return XP + np.array([-1.0 * np.sin(TAU * u), 0.95 * (1 - np.cos(TAU * u)), 0])


def conj(t):
    if t <= 1 / 3:
        return gamma(1 - 3 * t)          # gamma^{-1}: y -> x
    if t <= 2 / 3:
        return loop_x(3 * t - 1)         # f at x
    return gamma(3 * t - 2)              # gamma: x -> y


class ChangeOfBasePoint(Scene):
    def construct(self):
        title = MathTex(r"\gamma_{\#}:\pi(X,x)\to\pi(X,y),\quad [f]\mapsto[\gamma^{-1}\cdot f\cdot\gamma]").scale(0.62).to_edge(UP, buff=0.5)
        blob = Circle(radius=2.6, color=GREY_B, stroke_width=3, fill_color=GREY_E,
                      fill_opacity=0.4).move_to(X_CEN).stretch(0.85, 1)
        xlab = VGroup(Dot(XP, color=WHITE), MathTex("x").scale(0.7).next_to(XP, DOWN, buff=0.18))
        ylab = VGroup(Dot(YP, color=WHITE), MathTex("y").scale(0.7).next_to(YP, DOWN, buff=0.18))
        gam = path_curve(gamma, C_H)
        gl = MathTex(r"\gamma", color=C_H).scale(0.7).move_to(gamma(0.5) + UP * 0.35)
        lp = path_curve(loop_x, C_F)
        fl = MathTex("f", color=C_F).scale(0.7).move_to(loop_x(0.5) + UP * 0.3)
        left = VGroup(MathTex(r"\pi(X,x)").scale(0.8), MathTex(r"\Big\downarrow \gamma_{\#}").scale(0.8),
                      MathTex(r"\pi(X,y)").scale(0.8)).arrange(DOWN, buff=0.45).move_to(LEFT_C)
        self.play(FadeIn(title), FadeIn(blob), FadeIn(xlab), FadeIn(ylab), Create(lp), FadeIn(fl), run_time=1.2)
        self.play(Create(gam), FadeIn(gl), FadeIn(left[0]), run_time=1.2)
        tt = ValueTracker(0.0)
        trace = always_redraw(lambda: path_curve(lambda u: conj(u * max(tt.get_value(), 1e-3)), C_NOW, 7)
                              if tt.get_value() > 1e-3 else VGroup())
        dot = always_redraw(lambda: Dot(conj(tt.get_value()), color=C_NOW, radius=0.09))
        self.add(trace, dot)
        cap, an = caption(self, r"start at $y$, run $\gamma^{-1}$ to $x$")
        self.play(*an, tt.animate.set_value(1 / 3), run_time=1.6, rate_func=linear)
        cap2, an = caption(self, r"run the loop $f$ at $x$", cap)
        self.play(*an, tt.animate.set_value(2 / 3), run_time=2.2, rate_func=linear)
        cap3, an = caption(self, r"run $\gamma$ back to $y$: a loop at $y$", cap2)
        self.play(*an, tt.animate.set_value(1.0), FadeIn(left[1]), FadeIn(left[2]), run_time=1.6, rate_func=linear)
        cap4, an = caption(self, r"an isomorphism when $X$ is pathwise connected", cap3)
        self.play(*an, run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(cap4))

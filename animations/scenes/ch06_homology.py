"""Chapter 6 (Cairo renderer, 2D).

CubeBoundary    -- a singular 2-cube T: I^2 -> X, its four faces A_iT, B_iT, the signs
                   in d2 T = -A1T + A2T + B1T - B2T (the counterclockwise boundary),
                   and d1 d2 T = 0: every vertex appears twice with opposite signs.
PrismOperator   -- the prism Phi(T)(x1,x2) = H(x1, T(x2)) for a 1-cube T: its faces are
                   f#T, g#T and Phi(endpoints), so  d Phi = -f# + g# - Phi d.

Render: tools/bgc.sh 37 qh ch06_homology.py CubeBoundary   (one core each)
"""
from manim import *
import numpy as np

CA, CB = BLUE_C, ORANGE      # A-faces (x_i = 0) and B-faces (x_i = 1)
CPOS, CNEG = GREEN_C, RED_C


# ================================================================ 1. the 2-cube
SQ0 = np.array([-5.6, -1.7, 0])   # lower-left corner of I^2 on screen
SQS = 2.6


def sq(x1, x2):
    return SQ0 + SQS * np.array([x1, x2, 0])


def T(x1, x2):
    """A singular 2-cube in X (drawn on the right)."""
    u, v = x1, x2
    x = 1.0 + 3.2 * u + 0.6 * np.sin(PI * v) + 0.3 * u * v
    y = -1.9 + 3.0 * v + 0.55 * np.sin(PI * u) - 0.35 * u * v
    return np.array([x, y, 0])


def face_curve(fun, color, width=7):
    return ParametricFunction(fun, t_range=[0, 1, 0.01], color=color, stroke_width=width)


def mid_arrow(fun, color, reverse=False, t=0.5):
    p = fun(t)
    q = fun(t + 0.02)
    d = (q - p) / np.linalg.norm(q - p)
    if reverse:
        d = -d
    return Arrow(p - d * 0.25, p + d * 0.25, buff=0, color=color, stroke_width=6,
                 max_tip_length_to_length_ratio=0.6)


class CubeBoundary(Scene):
    def construct(self):
        title = MathTex(r"T:I^2\to X", r"\qquad \partial_2T=\sum_{i=1}^{2}(-1)^i\,(A_iT-B_iT)").scale(0.8)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title[0]), run_time=0.6)

        # the square and its image
        sqr = Polygon(sq(0, 0), sq(1, 0), sq(1, 1), sq(0, 1), color=GREY_B, stroke_width=3,
                      fill_color=GREY_E, fill_opacity=0.5)
        ax1 = MathTex("x_1").scale(0.6).next_to(sq(1, 0), DOWN, buff=0.15)
        ax2 = MathTex("x_2").scale(0.6).next_to(sq(0, 1), LEFT, buff=0.15)
        grid_l = VGroup(*[Line(sq(k / 6, 0), sq(k / 6, 1), color=GREY_C, stroke_width=1) for k in range(1, 6)],
                        *[Line(sq(0, k / 6), sq(1, k / 6), color=GREY_C, stroke_width=1) for k in range(1, 6)])
        grid_r = VGroup(*[ParametricFunction(lambda t, a=k / 6: T(a, t), t_range=[0, 1, 0.02],
                                             color=GREY_C, stroke_width=1) for k in range(1, 6)],
                        *[ParametricFunction(lambda t, a=k / 6: T(t, a), t_range=[0, 1, 0.02],
                                             color=GREY_C, stroke_width=1) for k in range(1, 6)])
        outline = VGroup(*[face_curve(f, GREY_B, 3) for f in
                           [lambda t: T(t, 0), lambda t: T(1, t), lambda t: T(t, 1), lambda t: T(0, t)]])
        arr = Arrow(sq(1, 0.5) + RIGHT * 0.3, T(0, 0.5) + LEFT * 0.35, buff=0.1, stroke_width=4)
        tl = MathTex("T").scale(0.8).next_to(arr, UP, buff=0.1)
        lX = MathTex("X").scale(0.8).move_to(T(1, 0.5) + RIGHT * 1.0 + UP * 1.2)
        self.play(FadeIn(sqr), Create(grid_l), FadeIn(ax1), FadeIn(ax2), run_time=1.0)
        self.play(GrowArrow(arr), FadeIn(tl), run_time=0.6)
        self.play(TransformFromCopy(grid_l, grid_r), Create(outline), FadeIn(lX), run_time=1.6)
        self.play(FadeIn(title[1]), run_time=0.8)

        # faces: (name, square-param, image-param, A or B, sign, label position on square)
        faces = [
            ("A_1T", lambda t: sq(0, t), lambda t: T(0, t), CA, -1, LEFT),
            ("B_1T", lambda t: sq(1, t), lambda t: T(1, t), CB, +1, RIGHT),
            ("A_2T", lambda t: sq(t, 0), lambda t: T(t, 0), CA, +1, DOWN),
            ("B_2T", lambda t: sq(t, 1), lambda t: T(t, 1), CB, -1, UP),
        ]
        terms = []
        for name, fs, fi, col, sgn, side in faces:
            ls = face_curve(fs, col)
            li = face_curve(fi, col)
            lab = MathTex(name, color=col).scale(0.6).next_to(ls, side, buff=0.12)
            if side is DOWN:
                lab.shift(LEFT * 0.6)
            if side is RIGHT:
                lab.shift(UP * 0.75)
            sgnt = MathTex("+" if sgn > 0 else "-", color=CPOS if sgn > 0 else CNEG).scale(0.7)
            sgnt.next_to(li, side, buff=0.15)
            self.play(Create(ls), Create(li), FadeIn(lab), run_time=0.7)
            self.play(FadeIn(sgnt), run_time=0.3)
            terms.append((ls, li, lab, sgnt, fi, sgn, col))

        cap = Tex(r"each face is parametrized by the remaining coordinate; the sign reverses it",
                  font_size=28).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(cap), run_time=0.5)
        arrows = VGroup(*[mid_arrow(fi, CPOS if sgn > 0 else CNEG, reverse=(sgn < 0))
                          for (_, _, _, _, fi, sgn, _) in terms])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=1.6)
        formula = MathTex(r"\partial_2T=-A_1T+A_2T+B_1T-B_2T", r"\ =\ \text{oriented boundary}").scale(0.75)
        formula.to_edge(DOWN, buff=0.35)
        self.play(FadeOut(cap), FadeIn(formula), run_time=0.6)

        # a dot running around the oriented boundary
        def loop(s):
            k = min(int(s * 4), 3)
            w = s * 4 - k
            return [T(w, 0), T(1, w), T(1 - w, 1), T(0, 1 - w)][k]
        st = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(loop(st.get_value()), color=YELLOW, radius=0.09))
        self.add(dot)
        self.play(st.animate.set_value(1.0), run_time=3.2, rate_func=linear)
        self.remove(dot)
        self.wait(0.6)

        # d1 d2 T = 0 : vertices
        self.play(FadeOut(formula), FadeOut(arrows), *[FadeOut(t[3]) for t in terms], run_time=0.6)
        cap2 = MathTex(r"\partial_1(\text{edge})=\text{end}-\text{start}\ \Longrightarrow\ \partial_1\partial_2T=0").scale(0.75)
        cap2.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(cap2), run_time=0.6)
        V = {"00": T(0, 0), "10": T(1, 0), "11": T(1, 1), "01": T(0, 1)}
        # contributions of the four signed edges (counterclockwise): A2: v10-v00, B1: v11-v10,
        # -B2: v01-v11, -A1: v00-v01
        contrib = [("10", "00"), ("11", "10"), ("01", "11"), ("00", "01")]
        offs = {"00": DL, "10": DR, "11": UR, "01": UL}
        marks = VGroup()
        for k, (plus, minus) in enumerate(contrib):
            col = terms[[2, 1, 3, 0][k]][6]
            pm = MathTex("+", color=CPOS).scale(0.7).move_to(V[plus] + offs[plus] * 0.42 + RIGHT * 0.18 * (k % 2))
            mm = MathTex("-", color=CNEG).scale(0.7).move_to(V[minus] + offs[minus] * 0.42 + LEFT * 0.18 * (k % 2))
            hl = VGroup(Dot(V[plus], color=CPOS, radius=0.08), Dot(V[minus], color=CNEG, radius=0.08))
            self.play(Indicate(terms[[2, 1, 3, 0][k]][1], color=col, scale_factor=1.0),
                      FadeIn(pm), FadeIn(mm), FadeIn(hl), run_time=0.9)
            marks.add(pm, mm, hl)
        self.wait(0.4)
        zero = VGroup(*[MathTex("0", color=YELLOW).scale(0.8).move_to(V[v] + offs[v] * 0.45) for v in V])
        self.play(FadeOut(marks), FadeIn(zero), run_time=1.0)
        self.wait(2.0)


# ============================================================ 2. the prism operator
def c0(t):   # f o T
    return np.array([-3.0 + 6.0 * t, -1.3 + 0.5 * np.sin(PI * t), 0])


def c1(t):   # g o T
    return np.array([-3.2 + 6.4 * t, 1.7 + 0.6 * np.sin(2 * PI * t) * 0.5 + 0.3 * t, 0])


def Hs(s, t):
    """H(s, T(t)): interpolate with a bulge, so the sides are curved."""
    p = (1 - s) * c0(t) + s * c1(t)
    return p + np.array([0.9 * np.sin(PI * s) * (t - 0.5), 0.35 * np.sin(PI * s) * np.sin(PI * t), 0])


class PrismOperator(Scene):
    def construct(self):
        title = MathTex(r"\Phi_1(T)(x_1,x_2)=H\big(x_1,\,T(x_2)\big)", r"\qquad H(0,\cdot)=f,\ H(1,\cdot)=g").scale(0.75)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=0.8)

        bottom = ParametricFunction(lambda t: Hs(0, t), t_range=[0, 1, 0.01], color=CA, stroke_width=7)
        top = ParametricFunction(lambda t: Hs(1, t), t_range=[0, 1, 0.01], color=CB, stroke_width=7)
        lb = MathTex(r"f_\#T=A_1\Phi_1(T)", color=CA).scale(0.65).next_to(bottom, DOWN, buff=0.15)
        lt = MathTex(r"g_\#T=B_1\Phi_1(T)", color=CB).scale(0.65).next_to(top, UP, buff=0.12).shift(RIGHT * 1.3)
        self.play(Create(bottom), FadeIn(lb), run_time=1.0)

        st = ValueTracker(0.0)
        sweep = always_redraw(lambda: ParametricFunction(
            lambda t: Hs(st.get_value(), t), t_range=[0, 1, 0.01], color=YELLOW, stroke_width=4))
        trail = always_redraw(lambda: VGroup(*[
            ParametricFunction(lambda t, s=s: Hs(s, t), t_range=[0, 1, 0.02], color=GREY_C,
                               stroke_width=1.2)
            for s in np.linspace(0.1, 0.9, 9) if s <= st.get_value()]))
        cap = Tex(r"the homotopy sweeps $f\circ T$ to $g\circ T$: a singular 2-cube in $Y$",
                  font_size=28).to_edge(DOWN, buff=0.3)
        self.add(trail, sweep)
        self.play(FadeIn(cap), run_time=0.4)
        self.play(st.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        self.remove(sweep)
        self.play(Create(top), FadeIn(lt), run_time=0.8)

        left = ParametricFunction(lambda s: Hs(s, 0), t_range=[0, 1, 0.01], color=PURPLE_B, stroke_width=7)
        right = ParametricFunction(lambda s: Hs(s, 1), t_range=[0, 1, 0.01], color=PURPLE_B, stroke_width=7)
        ll = MathTex(r"A_2\Phi_1(T)=\Phi_0\big(T(0)\big)", color=PURPLE_B).scale(0.6).next_to(left, LEFT, buff=0.15)
        lr = MathTex(r"B_2\Phi_1(T)=\Phi_0\big(T(1)\big)", color=PURPLE_B).scale(0.6).next_to(right, RIGHT, buff=0.15)
        cap2 = Tex(r"the two other faces are the paths of the end points of $T$ under $H$",
                   font_size=28).to_edge(DOWN, buff=0.3)
        self.play(FadeOut(cap), FadeIn(cap2), Create(left), Create(right), FadeIn(ll), FadeIn(lr), run_time=1.2)
        self.wait(0.6)

        f1 = MathTex(r"\partial_2\Phi_1(T)", r"=-A_1\Phi_1T+B_1\Phi_1T+A_2\Phi_1T-B_2\Phi_1T").scale(0.68)
        f2 = MathTex(r"=", r"-f_\#T", r"+g_\#T", r"-\Phi_0\big(T(1)-T(0)\big)").scale(0.68)
        f3 = MathTex(r"\Longrightarrow\quad -f_\#+g_\#=\partial\Phi+\Phi\partial").scale(0.75)
        grp = VGroup(f1, f2, f3).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.12)
        f2.shift(RIGHT * (f1[0].width + 0.05))
        f2[1].set_color(CA)
        f2[2].set_color(CB)
        f2[3].set_color(PURPLE_B)
        self.play(FadeOut(cap2), FadeIn(f1), run_time=0.8)
        self.play(FadeIn(f2), run_time=0.8)
        box = SurroundingRectangle(f3, color=YELLOW, buff=0.1)
        self.play(FadeIn(f3), Create(box), run_time=0.9)
        self.wait(2.5)

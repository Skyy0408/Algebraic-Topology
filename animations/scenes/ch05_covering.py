"""Chapter 5 (Cairo renderer).

HelixLifting        -- R -> S^1, t -> e^{it} drawn as a helix over the circle: an
                       elementary neighbourhood U and its preimage (disjoint sheets),
                       then the unique lift of a path from two points of the fibre.
LiftGridTree        -- the word a b a^-1 b^-1 in the figure eight, lifted to the grid
                       covering (closes up) and to the tree (does not close up).
BorsukUlamDoubling  -- key step of Borsuk-Ulam: f o alpha runs from f(N) to -f(N);
                       after p1(z) = z^2 it is a loop going around once, so nontrivial.

Render: tools/bgc.sh 37 qh ch05_covering.py HelixLifting   (etc., one core each)
"""
from manim import *
import numpy as np

CU, CL, CP, CX0 = ORANGE, YELLOW, RED_C, WHITE
CA, CB = BLUE_C, GREEN_C          # the two circles of the figure eight


# ===================================================== 1. helix over the circle
HR = 1.9          # radius
HC = 0.22         # rise per radian
ZB = -3.1         # height of the base circle
T0, T1 = -2 * PI, 4 * PI


def helix(t):
    return np.array([HR * np.cos(t), HR * np.sin(t), HC * t])


def base(t):
    return np.array([HR * np.cos(t), HR * np.sin(t), ZB])


def alpha_angle(s):
    """A path in S^1 (as an angle): forward 1.4 turns with a wiggle, starting at 0."""
    return 1.4 * TAU * s + 0.7 * np.sin(2 * PI * s)


class HelixLifting(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.95)
        title = Tex(r"$p:\mathbb{R}\to S^1,\ \ p(t)=e^{it}$", font_size=34).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title), run_time=0.5)

        circ = ParametricFunction(base, t_range=[0, TAU], color=GREY_B, stroke_width=4)
        hel = ParametricFunction(helix, t_range=[T0, T1, 0.02], color=BLUE_C, stroke_width=3.5)
        lab_s1 = MathTex(r"S^1", color=GREY_B).scale(0.8)
        lab_r = MathTex(r"\mathbb{R}", color=BLUE_C).scale(0.8)
        self.add_fixed_in_frame_mobjects(lab_s1, lab_r)
        lab_s1.to_corner(DL, buff=0.6)
        lab_r.to_corner(UR, buff=0.6).shift(DOWN * 0.6)
        self.play(Create(circ), FadeIn(lab_s1), run_time=1.0)
        self.play(Create(hel), FadeIn(lab_r), run_time=2.0)

        # elementary neighbourhood U and its preimage
        c, w = 0.0, 0.45
        U = ParametricFunction(base, t_range=[c - w, c + w], color=CU, stroke_width=10)
        sheets = VGroup(*[ParametricFunction(helix, t_range=[c - w + k * TAU, c + w + k * TAU],
                                             color=CU, stroke_width=10) for k in range(-1, 2)])
        cap = Tex(r"elementary neighborhood $U$; $p^{-1}(U)$ = disjoint copies of $U$",
                  font_size=28).to_edge(UP, buff=0.95).shift(RIGHT * 0.8)
        self.add_fixed_in_frame_mobjects(cap)
        self.play(Create(U), FadeIn(cap), run_time=0.8)
        drops = VGroup(*[DashedLine(helix(c + k * TAU), base(c), color=CU, stroke_width=1.5,
                                    dash_length=0.08) for k in range(-1, 2)])
        self.play(Create(sheets), Create(drops), run_time=1.5)
        self.wait(0.8)
        self.play(FadeOut(drops), FadeOut(sheets), FadeOut(U), FadeOut(cap), run_time=0.6)

        # lifting a path from two different points of the fibre
        st = ValueTracker(0.0)
        cap2 = Tex(r"a path $\alpha$ in $S^1$ and its unique lift $\tilde\alpha$ with $\tilde\alpha(0)=\tilde x_0$",
                   font_size=28).to_edge(UP, buff=0.95).shift(RIGHT * 0.8)
        self.add_fixed_in_frame_mobjects(cap2)
        self.play(FadeIn(cap2), run_time=0.5)
        self.begin_ambient_camera_rotation(rate=0.06)

        def run(k0, col):
            st.set_value(0.0)
            path = always_redraw(lambda: ParametricFunction(
                lambda s: base(alpha_angle(s)), t_range=[0, max(st.get_value(), 1e-3), 0.004],
                color=CP, stroke_width=6))
            lift = always_redraw(lambda: ParametricFunction(
                lambda s: helix(alpha_angle(s) + k0 * TAU), t_range=[0, max(st.get_value(), 1e-3), 0.004],
                color=col, stroke_width=6))
            d1 = always_redraw(lambda: Dot3D(base(alpha_angle(st.get_value())), color=CP, radius=0.07))
            d2 = always_redraw(lambda: Dot3D(helix(alpha_angle(st.get_value()) + k0 * TAU),
                                             color=col, radius=0.08))
            link = always_redraw(lambda: DashedLine(
                helix(alpha_angle(st.get_value()) + k0 * TAU), base(alpha_angle(st.get_value())),
                color=GREY_A, stroke_width=1.5, dash_length=0.08))
            start = Dot3D(helix(k0 * TAU), color=CX0, radius=0.08)
            self.play(FadeIn(start), run_time=0.4)
            self.add(path, lift, d1, d2, link)
            self.play(st.animate.set_value(1.0), run_time=4.0, rate_func=linear)
            return VGroup(path, lift, d1, d2, link, start)

        g1 = run(-1, CL)
        cap3 = Tex(r"another point $\tilde x_1\in p^{-1}(x_0)$: another lift, a translate by $2\pi$",
                   font_size=28).to_edge(UP, buff=0.95).shift(RIGHT * 0.8)
        self.add_fixed_in_frame_mobjects(cap3)
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.5)
        g2 = run(0, GREEN_B)
        self.wait(1.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)


# ======================================== 2. a b a^-1 b^-1 lifted to grid and tree
EO = np.array([0.0, -2.55, 0.0])   # figure eight: wedge point
ER = 0.7
GO = np.array([-4.6, -0.3, 0.0])   # grid: lift start
GU = 1.1
TO = np.array([3.3, -0.3, 0.0])    # tree: root
TL = 1.3


def eight_a(s):  # C1 (right circle), the generator a
    return EO + ER * np.array([1 - np.cos(TAU * s), np.sin(TAU * s), 0])


def eight_b(s):  # C2 (left circle), the generator b
    return EO + ER * np.array([-1 + np.cos(TAU * s), np.sin(TAU * s), 0])


WORD = [("a", 1), ("b", 1), ("a", -1), ("b", -1)]
WTEX = [r"a", r"b", r"a^{-1}", r"b^{-1}"]
DIRS = {("a", 1): RIGHT, ("a", -1): LEFT, ("b", 1): UP, ("b", -1): DOWN}


def tree_edges(p, incoming, length, depth, out):
    if depth == 0:
        return
    for d in [RIGHT, LEFT, UP, DOWN]:
        if incoming is not None and np.allclose(d, -incoming):
            continue
        q = p + d * length
        col = CA if abs(d[0]) > 0 else CB
        out.append(Line(p, q, color=col, stroke_width=max(1.0, 3.2 * length / TL),
                        stroke_opacity=0.75))
        tree_edges(q, d, length / 2, depth - 1, out)


class LiftGridTree(Scene):
    def construct(self):
        # base: the figure eight
        ea = ParametricFunction(eight_a, t_range=[0, 1, 0.01], color=CA, stroke_width=5)
        eb = ParametricFunction(eight_b, t_range=[0, 1, 0.01], color=CB, stroke_width=5)
        la = MathTex("a", color=CA).scale(0.7).next_to(ea, RIGHT, buff=0.12)
        lb = MathTex("b", color=CB).scale(0.7).next_to(eb, LEFT, buff=0.12)
        x0 = Dot(EO, color=CX0, radius=0.06)
        lx = MathTex("x_0").scale(0.55).next_to(x0, DOWN, buff=0.08)
        lX = MathTex(r"X=S^1\vee S^1").scale(0.6).next_to(VGroup(ea, eb), UP, buff=0.12)
        self.play(Create(ea), Create(eb), FadeIn(la), FadeIn(lb), FadeIn(x0), FadeIn(lx),
                  FadeIn(lX), run_time=1.2)

        # grid covering
        gl = VGroup()
        for k in range(-1, 3):
            gl.add(Line(GO + GU * np.array([-1.5, k, 0]), GO + GU * np.array([2.5, k, 0]),
                        color=CA, stroke_width=2.5, stroke_opacity=0.75))
            gl.add(Line(GO + GU * np.array([k, -1.5, 0]), GO + GU * np.array([k, 2.5, 0]),
                        color=CB, stroke_width=2.5, stroke_opacity=0.75))
        gtitle = Tex(r"grid $(\mathbb{Z}\times\mathbb{R})\cup(\mathbb{R}\times\mathbb{Z})$",
                     font_size=28).move_to(GO + GU * np.array([0.5, 3.05, 0]))
        # tree covering
        edges = []
        tree_edges(TO, None, TL, 5, edges)
        tr = VGroup(*edges)
        ttitle = Tex(r"tree (universal covering)", font_size=28).move_to(
            np.array([TO[0], 3.05, 0]))
        self.play(Create(gl), FadeIn(gtitle), run_time=1.4)
        self.play(Create(tr), FadeIn(ttitle), run_time=2.0)
        g0 = Dot(GO, color=CX0, radius=0.07)
        t0 = Dot(TO, color=CX0, radius=0.07)
        lg0 = MathTex(r"\tilde x_0").scale(0.55).next_to(g0, DL, buff=0.05)
        lt0 = MathTex(r"\tilde x_0").scale(0.55).next_to(t0, DL, buff=0.05)
        self.play(FadeIn(g0), FadeIn(t0), FadeIn(lg0), FadeIn(lt0), run_time=0.5)

        word = MathTex(r"\alpha=", *WTEX).scale(0.85).to_edge(UP, buff=0.25)
        for k in range(1, 5):
            word[k].set_opacity(0.25)
        self.play(FadeIn(word), run_time=0.5)

        gpos, tpos, tlen = GO.copy(), TO.copy(), TL
        gpath, tpath = VGroup(), VGroup()
        for k, (gen, sgn) in enumerate(WORD):
            d = DIRS[(gen, sgn)]
            col = CA if gen == "a" else CB
            st = ValueTracker(0.0)
            f = eight_a if gen == "a" else eight_b
            bdot = always_redraw(lambda f=f, sgn=sgn: Dot(
                f(st.get_value() if sgn > 0 else 1 - st.get_value()), color=RED_C, radius=0.08))
            gq, tq = gpos + d * GU, tpos + d * tlen
            gseg = Line(gpos, gq, color=RED_C, stroke_width=7)
            tseg = Line(tpos, tq, color=RED_C, stroke_width=7)
            self.add(bdot)
            self.play(st.animate.set_value(1.0), Create(gseg), Create(tseg),
                      word[k + 1].animate.set_opacity(1).set_color(col),
                      run_time=1.3, rate_func=linear)
            self.remove(bdot)
            gpath.add(gseg)
            tpath.add(tseg)
            gpos, tpos, tlen = gq, tq, tlen / 2

        gend = Dot(gpos, color=YELLOW, radius=0.1)
        tend = Dot(tpos, color=YELLOW, radius=0.1)
        lte = MathTex(r"\tilde x_0\cdot\alpha", color=YELLOW).scale(0.55).next_to(tend, UR, buff=0.05)
        self.play(FadeIn(gend), FadeIn(tend), FadeIn(lte), run_time=0.6)
        cg = Tex(r"closes up: $\tilde x_0\cdot\alpha=\tilde x_0$", font_size=28, color=YELLOW).move_to(
            np.array([GO[0] + 0.55, -3.2, 0]))
        ct = Tex(r"does not close: $\tilde x_0\cdot\alpha\neq\tilde x_0$", font_size=28,
                 color=YELLOW).move_to(np.array([TO[0], -3.2, 0]))
        self.play(FadeIn(cg), FadeIn(ct), run_time=0.8)
        self.wait(0.6)
        res = MathTex(r"\Rightarrow\ \alpha=aba^{-1}b^{-1}\neq 1\ \text{in}\ \pi(X,x_0),\qquad"
                      r"\alpha\in p_*\pi(\text{grid})").scale(0.6).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(res), run_time=0.8)
        self.wait(2.5)


# ================================================ 3. Borsuk-Ulam: doubling map
SC = np.array([-4.7, 0.2, 0.0])
CC = np.array([-0.2, 0.2, 0.0])
DC = np.array([4.4, 0.2, 0.0])
RS, RC = 1.55, 1.45
TH0 = 0.35


def f_angle(s):
    """f o alpha as an angle: from TH0 to TH0 + pi, with a wiggle."""
    return TH0 + PI * s + 0.9 * np.sin(2 * PI * s) * (1 - s * 0.3)


def on_circle(c, r, th):
    return c + r * np.array([np.cos(th), np.sin(th), 0])


def meridian(s):
    """A path alpha on the (drawn) sphere from N to S."""
    y = RS * np.cos(PI * s)
    x = 0.45 * RS * np.sin(PI * s) * np.sin(3 * PI * s)
    return SC + np.array([x, y, 0])


class BorsukUlamDoubling(Scene):
    def construct(self):
        sph = Circle(radius=RS, color=BLUE_C, stroke_width=3).move_to(SC)
        eq = Ellipse(width=2 * RS, height=0.5, color=BLUE_C, stroke_width=2).move_to(SC)
        eq_back = DashedVMobject(eq.copy().set_stroke(opacity=0.5), num_dashes=24)
        N = Dot(SC + RS * UP, radius=0.06)
        S = Dot(SC + RS * DOWN, radius=0.06)
        lN = MathTex("N").scale(0.6).next_to(N, UP, buff=0.08)
        lS = MathTex("S=-N").scale(0.6).next_to(S, DOWN, buff=0.08)
        l2 = MathTex("S^2", color=BLUE_C).scale(0.75).next_to(sph, UL, buff=-0.1)

        c1 = Circle(radius=RC, color=GREY_B, stroke_width=3).move_to(CC)
        c2 = Circle(radius=RC, color=GREY_B, stroke_width=3).move_to(DC)
        lc1 = MathTex("S^1").scale(0.7).next_to(c1, UL, buff=-0.1)
        lc2 = MathTex("S^1").scale(0.7).next_to(c2, UL, buff=-0.1)
        af = Arrow(SC + RIGHT * (RS + 0.15), CC + LEFT * (RC + 0.15), buff=0.05, stroke_width=4)
        ap = Arrow(CC + RIGHT * (RC + 0.15), DC + LEFT * (RC + 0.15), buff=0.05, stroke_width=4)
        lf = MathTex("f").scale(0.75).next_to(af, UP, buff=0.08)
        lp = MathTex(r"p_1(z)=z^2").scale(0.65).next_to(ap, DOWN, buff=0.12)
        self.play(Create(sph), Create(eq), FadeIn(N), FadeIn(S), FadeIn(lN), FadeIn(lS), FadeIn(l2),
                  run_time=1.2)
        self.play(GrowArrow(af), FadeIn(lf), Create(c1), FadeIn(lc1), run_time=1.0)
        self.play(GrowArrow(ap), FadeIn(lp), Create(c2), FadeIn(lc2), run_time=1.0)

        cap = Tex(r"$\alpha$: a path from $N$ to $-N$", font_size=30).to_edge(UP, buff=0.4)
        self.play(FadeIn(cap), run_time=0.4)
        st = ValueTracker(0.0)
        pa = always_redraw(lambda: ParametricFunction(
            meridian, t_range=[0, max(st.get_value(), 1e-3), 0.004], color=RED_C, stroke_width=5))
        pf = always_redraw(lambda: ParametricFunction(
            lambda s: on_circle(CC, RC, f_angle(s)), t_range=[0, max(st.get_value(), 1e-3), 0.004],
            color=RED_C, stroke_width=5))
        pd = always_redraw(lambda: ParametricFunction(
            lambda s: on_circle(DC, RC * (1 - 0.12 * s), 2 * f_angle(s)),
            t_range=[0, max(st.get_value(), 1e-3), 0.004], color=YELLOW, stroke_width=5))
        d1 = always_redraw(lambda: Dot(meridian(st.get_value()), color=RED_C, radius=0.07))
        d2 = always_redraw(lambda: Dot(on_circle(CC, RC, f_angle(st.get_value())), color=RED_C, radius=0.07))
        d3 = always_redraw(lambda: Dot(on_circle(DC, RC * (1 - 0.12 * st.get_value()),
                                                 2 * f_angle(st.get_value())), color=YELLOW, radius=0.07))
        fN = Dot(on_circle(CC, RC, TH0), color=WHITE, radius=0.06)
        fS = Dot(on_circle(CC, RC, TH0 + PI), color=WHITE, radius=0.06)
        lfN = MathTex("f(N)").scale(0.55).next_to(fN, UR, buff=0.04)
        lfS = MathTex("-f(N)").scale(0.55).next_to(fS, DL, buff=0.04)
        self.play(FadeIn(fN), FadeIn(fS), FadeIn(lfN), FadeIn(lfS), run_time=0.5)
        self.add(pa, pf, d1, d2)
        self.play(st.animate.set_value(1.0), run_time=4.0, rate_func=linear)
        cap2 = Tex(r"$f\circ\alpha$ ends at the antipode $f(-N)=-f(N)$; now apply $p_1$",
                   font_size=30).to_edge(UP, buff=0.4)
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.5)

        st.set_value(0.0)
        self.add(pd, d3)
        self.remove(d1, d2)
        dd2 = always_redraw(lambda: Dot(on_circle(CC, RC, f_angle(st.get_value())),
                                        color=RED_C, radius=0.07))
        self.add(dd2)
        self.play(st.animate.set_value(1.0), run_time=4.0, rate_func=linear)
        cap3 = Tex(r"$p_1\circ f\circ\alpha$ is a loop going around once: $\neq 0$ in $\pi(S^1)=\mathbb{Z}$",
                   font_size=30).to_edge(UP, buff=0.4)
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.5)
        res = MathTex(r"0=g_*[p_2\circ\alpha]=[p_1\circ f\circ\alpha]\neq0\quad",
                      r"(g_*:\mathbb{Z}_2\to\mathbb{Z}\ \text{is}\ 0)").scale(0.72).to_edge(DOWN, buff=0.45)
        self.play(Write(res), run_time=1.6)
        self.wait(2.5)

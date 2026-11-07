"""Chapter 3 (sec. 3.9) and Chapter 4 (Cairo renderer, 2D).

WordReduction          -- reducing b a b b^-1 a^-1 c^-1 c a in two different orders;
                          both end at the same reduced form  b a.
LebesgueLoopSplit      -- the Lemma of sec. 4.4: a loop f is cut by a Lebesgue number
                          into pieces f(J_i), each inside one open set, and joined to
                          x0 by paths g_i, so alpha = alpha_0 alpha_1 ... alpha_{n-1}.
PuncturedTorusRetract  -- T^2 minus the center c deformation retracts onto a v b; the
                          small loop gamma around c is pushed to a b a^-1 b^-1.

Render: tools/bgc.sh 37-39 qh ch04_vankampen.py WordReduction LebesgueLoopSplit PuncturedTorusRetract
"""
from manim import *
import numpy as np

CU, CV, CB, CX0, CF, CG = BLUE_C, ORANGE, GREEN_B, YELLOW, WHITE, GREY_A


def caption(tex, size=30):
    return Tex(tex, font_size=size).to_corner(UR, buff=0.4).shift(DOWN * 0.85)


def topcap(tex, size=30):
    return Tex(tex, font_size=size).to_edge(UP, buff=0.35)


def chevron(mid, d, color, size=0.2, n=1):
    d = np.array(d, dtype=float)
    d = d / np.linalg.norm(d)
    nrm = np.array([-d[1], d[0], 0.0])
    g = VGroup()
    for k in range(n):
        c = mid + d * (k - (n - 1) / 2) * size * 1.1
        tip = c + d * size / 2
        g.add(VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
            [tip - d * size + nrm * size * 0.6, tip, tip - d * size - nrm * size * 0.6]))
    return g


# ============================================================ 3.9 word reduction
LETTER = {"a": r"a", "A": r"a^{-1}", "b": r"b", "B": r"b^{-1}", "c": r"c", "C": r"c^{-1}"}
LCOL = {"a": BLUE_C, "b": ORANGE, "c": GREEN_B}
SLOT = 0.95


def inverse_pair(x, y):
    return x != y and x.lower() == y.lower()


class WordRow:
    def __init__(self, scene, word, y):
        self.scene, self.y = scene, y
        self.letters = list(word)
        self.mobs = [MathTex(LETTER[ch], color=LCOL[ch.lower()]).scale(0.95) for ch in word]
        for k, m in enumerate(self.mobs):
            m.move_to(self.pos(k, len(self.mobs)))

    def pos(self, k, n):
        return np.array([(k - (n - 1) / 2) * SLOT + 1.2, self.y, 0.0])

    def group(self):
        return VGroup(*self.mobs)

    def cancel(self, i, rt=1.0):
        """Cancel letters i, i+1 (must be x x^-1 or x^-1 x)."""
        assert inverse_pair(self.letters[i], self.letters[i + 1])
        pair = VGroup(self.mobs[i], self.mobs[i + 1])
        box = SurroundingRectangle(pair, color=RED_C, buff=0.1, stroke_width=3)
        one = MathTex("1", color=GREY_B).scale(0.95).move_to(pair.get_center())
        self.scene.play(Create(box), run_time=0.45 * rt)
        self.scene.play(FadeOut(pair, scale=0.5), FadeOut(box), FadeIn(one), run_time=0.55 * rt)
        del self.letters[i:i + 2]
        del self.mobs[i:i + 2]
        n = len(self.mobs)
        self.scene.play(FadeOut(one, scale=0.3),
                        *[m.animate.move_to(self.pos(k, n)) for k, m in enumerate(self.mobs)],
                        run_time=0.6 * rt)


class WordReduction(Scene):
    def construct(self):
        title = Tex(r"Reduced form of a word in the free group on $S=\{a,b,c\}$",
                    font_size=34).to_edge(UP, buff=0.4)
        rule = MathTex(r"x\,x^{-1}=x^{-1}x=1", color=GREY_A).scale(0.8).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title), FadeIn(rule), run_time=0.9)

        word = "babBACca"
        r1 = WordRow(self, word, 1.0)
        l1 = Tex(r"order 1", font_size=30, color=GREY_B).move_to([-5.6, 1.0, 0])
        self.play(FadeIn(l1), LaggedStart(*[FadeIn(m) for m in r1.mobs], lag_ratio=0.08), run_time=1.3)
        self.wait(0.4)
        # the order of the notes: c^-1 c, then a^-1 a, then b b^-1
        r1.cancel(5)
        r1.cancel(4)
        r1.cancel(2)
        box1 = SurroundingRectangle(r1.group(), color=YELLOW, buff=0.15)
        self.play(Create(box1), run_time=0.5)
        self.wait(0.4)

        r2 = WordRow(self, word, -1.6)
        l2 = Tex(r"order 2", font_size=30, color=GREY_B).move_to([-5.6, -1.6, 0])
        self.play(FadeIn(l2), LaggedStart(*[FadeIn(m) for m in r2.mobs], lag_ratio=0.08), run_time=1.3)
        # a different order: b b^-1 first, then a a^-1, then c^-1 c
        r2.cancel(2)
        r2.cancel(1)
        r2.cancel(1)
        box2 = SurroundingRectangle(r2.group(), color=YELLOW, buff=0.15)
        self.play(Create(box2), run_time=0.5)

        fact = Tex(r"\textbf{Fact.} The reduced form is unique: here both give $ba$.",
                   font_size=32).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(fact), run_time=0.8)
        self.wait(2.0)


# =============================================== 4.4 Lemma: Lebesgue subdivision
S = 0.8                       # scale of the picture of X
XC = np.array([0.0, 0.8, 0.0])
ECX, ERX, ERY = 1.0, 2.9, 1.9  # U, V: ellipses centred at (-+ECX, 0), radii ERX, ERY
NPIECE = 12                   # 1/12 < Lebesgue number (about 0.088) for this loop
IL, IR, IY = -5.2, 5.2, -2.85  # the interval I on screen
STRIP_U, STRIP_V = -1.55, -2.05


def fxy(t):
    x = -2.7 * np.sin(4 * np.pi * t) + 0.35 * np.sin(2 * np.pi * t)
    y = 1.15 * np.sin(2 * np.pi * t) + 0.25 * np.sin(8 * np.pi * t)
    return np.array([x, y])


def F(t):
    x, y = fxy(t)
    return XC + S * np.array([x, y, 0.0])


def in_ell(p, c):
    return ((p[0] - c) / ERX) ** 2 + (p[1] / ERY) ** 2 < 1.0


def in_U(t):
    return in_ell(fxy(t), -ECX)


def in_V(t):
    return in_ell(fxy(t), ECX)


def Ipos(t, y=IY):
    return np.array([IL + (IR - IL) * t, y, 0.0])


def runs(pred, N=2400):
    """Maximal sub-intervals of [0,1] where pred holds (sampled)."""
    ts = np.linspace(0, 1, N + 1)
    v = [pred(t) for t in ts]
    out, start = [], None
    for t, b in zip(ts, v):
        if b and start is None:
            start = t
        if not b and start is not None:
            out.append((start, t))
            start = None
    if start is not None:
        out.append((start, 1.0))
    return out


def piece_sets():
    lab = []
    for i in range(NPIECE):
        ts = np.linspace(i / NPIECE, (i + 1) / NPIECE, 200)
        u = all(in_U(t) for t in ts)
        v = all(in_V(t) for t in ts)
        assert u or v, "1/n is not below the Lebesgue number"
        lab.append("UV" if (u and v) else ("U" if u else "V"))
    return lab


SETCOL = {"U": CU, "V": CV, "UV": CB}
SETTEX = {"U": r"U", "V": r"V", "UV": r"U\cap V"}


class LebesgueLoopSplit(Scene):
    def construct(self):
        x0 = F(0.0)
        U = Ellipse(width=2 * ERX * S, height=2 * ERY * S, color=CU, stroke_width=3,
                    fill_color=CU, fill_opacity=0.10).move_to(XC + S * np.array([-ECX, 0, 0]))
        V = Ellipse(width=2 * ERX * S, height=2 * ERY * S, color=CV, stroke_width=3,
                    fill_color=CV, fill_opacity=0.10).move_to(XC + S * np.array([ECX, 0, 0]))
        lu = MathTex(r"U", color=CU).scale(0.9).move_to(U.get_left() + RIGHT * 0.35 + UP * 1.05)
        lv = MathTex(r"V", color=CV).scale(0.9).move_to(V.get_right() + LEFT * 0.35 + UP * 1.05)
        d0 = Dot(x0, color=CX0, radius=0.07)
        l0 = MathTex(r"x_0", color=CX0).scale(0.7).next_to(d0, DOWN + RIGHT, buff=0.06)
        self.play(FadeIn(U), FadeIn(V), FadeIn(lu), FadeIn(lv), run_time=1.0)
        self.play(FadeIn(d0), FadeIn(l0), run_time=0.5)

        # the interval I and the loop f
        iline = Line(Ipos(0), Ipos(1), color=GREY_B, stroke_width=4)
        i0 = MathTex("0").scale(0.6).next_to(Ipos(0), DOWN, buff=0.15)
        i1 = MathTex("1").scale(0.6).next_to(Ipos(1), DOWN, buff=0.15)
        iI = MathTex("I").scale(0.75).next_to(Ipos(0), LEFT, buff=0.3)
        self.play(Create(iline), FadeIn(i0), FadeIn(i1), FadeIn(iI), run_time=0.8)

        tt = ValueTracker(0.0)
        loop = always_redraw(lambda: ParametricFunction(
            F, t_range=[0, max(tt.get_value(), 1e-3), 0.002], color=CF, stroke_width=3.5))
        mdot = always_redraw(lambda: Dot(F(tt.get_value()), color=RED_C, radius=0.06))
        idot = always_redraw(lambda: Dot(Ipos(tt.get_value()), color=RED_C, radius=0.06))
        cap = topcap(r"a loop $f:I\to X$ at $x_0$, $[f]=\alpha$")
        self.add(loop, mdot, idot)
        self.play(FadeIn(cap), run_time=0.5)
        self.play(tt.animate.set_value(1.0), run_time=5.0, rate_func=linear)
        self.remove(loop, mdot, idot)
        loop_full = ParametricFunction(F, t_range=[0, 1, 0.002], color=CF, stroke_width=3.5)
        self.add(loop_full)
        flab = MathTex(r"f", color=CF).scale(0.75).move_to(F(0.115) + UP * 0.3)
        self.play(FadeIn(flab), run_time=0.3)

        # the open cover f^{-1}(U), f^{-1}(V) of I
        su = VGroup(*[Line(Ipos(a, STRIP_U), Ipos(b, STRIP_U), color=CU, stroke_width=9)
                      for a, b in runs(in_U)])
        sv = VGroup(*[Line(Ipos(a, STRIP_V), Ipos(b, STRIP_V), color=CV, stroke_width=9)
                      for a, b in runs(in_V)])
        lsu = MathTex(r"f^{-1}(U)", color=CU).scale(0.6).next_to(Ipos(0, STRIP_U), LEFT, buff=0.2)
        lsv = MathTex(r"f^{-1}(V)", color=CV).scale(0.6).next_to(Ipos(0, STRIP_V), LEFT, buff=0.2)
        cap2 = topcap(r"$\{f^{-1}(U),f^{-1}(V)\}$: an open cover of the compact $I$")
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.5)
        self.play(Create(su), Create(sv), FadeIn(lsu), FadeIn(lsv), run_time=1.6)
        self.wait(0.6)

        # a window of length 1/n slides along: it always fits in one strip
        w = 1.0 / NPIECE
        st = ValueTracker(0.0)
        win = always_redraw(lambda: Rectangle(
            width=(IR - IL) * w, height=1.25, color=YELLOW, stroke_width=2.5)
            .move_to(Ipos(st.get_value() + w / 2, (STRIP_U + IY) / 2 + 0.05)))
        cap3 = topcap(r"$\tfrac1n<$ Lebesgue number: every interval of length $\tfrac1n$ lies in one of them ($n=%d$)" % NPIECE, size=26)
        self.play(FadeOut(cap2), FadeIn(cap3), FadeIn(win), run_time=0.6)
        self.play(st.animate.set_value(1.0 - w), run_time=3.5, rate_func=linear)
        self.play(FadeOut(win), run_time=0.3)

        # the partition and the colouring of the pieces
        lab = piece_sets()
        ticks = VGroup(*[Line(Ipos(i / NPIECE) + DOWN * 0.13, Ipos(i / NPIECE) + UP * 0.13,
                              color=WHITE, stroke_width=3) for i in range(NPIECE + 1)])
        segs = VGroup(*[Line(Ipos(i / NPIECE), Ipos((i + 1) / NPIECE), color=SETCOL[lab[i]],
                             stroke_width=8) for i in range(NPIECE)])
        pieces = VGroup(*[ParametricFunction(F, t_range=[i / NPIECE, (i + 1) / NPIECE, 0.002],
                                             color=SETCOL[lab[i]], stroke_width=5)
                          for i in range(NPIECE)])
        jlab = MathTex(r"J_i=\big[\tfrac in,\tfrac{i+1}n\big],\quad f(J_i)\subseteq U_{\lambda_i}",
                       ).scale(0.62).next_to(Ipos(0.5), DOWN, buff=0.3)
        self.play(FadeOut(cap3), Create(ticks), run_time=0.8)
        self.play(FadeIn(segs), FadeIn(jlab), run_time=0.8)
        self.play(FadeOut(flab), ReplacementTransform(loop_full, pieces), run_time=1.2)
        legend = VGroup(
            MathTex(r"\lambda_i=U", color=CU), MathTex(r"\lambda_i=V", color=CV),
            MathTex(r"\lambda_i=U\cap V", color=CB)).scale(0.55).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.to_corner(UL, buff=0.35)
        self.play(FadeIn(legend), run_time=0.5)

        # connecting paths g_i from x0 to f(i/n), inside U_{lambda_{i-1}} cap U_{lambda_i}
        ends = [F(i / NPIECE) for i in range(NPIECE + 1)]
        gs = VGroup(*[DashedLine(x0, ends[i], color=CG, stroke_width=2.5, dash_length=0.08)
                      for i in range(1, NPIECE)])
        gd = VGroup(*[Dot(ends[i], color=WHITE, radius=0.045) for i in range(1, NPIECE)])
        cap4 = topcap(r"paths $g_i$ from $x_0$ to $f(\tfrac in)$ in $U_{\lambda_{i-1}}\cap U_{\lambda_i}$")
        self.play(FadeIn(cap4), Create(gs), FadeIn(gd), run_time=1.5)
        self.wait(0.5)

        # the loops alpha_i = [g_i . f_i . g_{i+1}^{-1}]
        cap5 = topcap(r"$\alpha_i=[\,g_i\cdot f_i\cdot g_{i+1}^{-1}\,]\in\psi_{\lambda_i}\big(\pi(U_{\lambda_i})\big)$")
        self.play(FadeOut(cap4), FadeIn(cap5), pieces.animate.set_stroke(opacity=0.25),
                  gs.animate.set_stroke(opacity=0.25), run_time=0.6)
        prod = MathTex(r"\alpha=", r"\alpha_0", *[r"\alpha_{%d}" % i for i in range(1, NPIECE)]
                       ).scale(0.6).to_edge(DOWN, buff=0.08)
        for k in range(1, NPIECE + 1):
            prod[k].set_opacity(0.25)
        self.play(FadeOut(jlab), FadeIn(prod[0]), run_time=0.3)
        for i in range(NPIECE):
            col = SETCOL[lab[i]]
            parts = VGroup()
            if i > 0:
                parts.add(Line(x0, ends[i], color=col, stroke_width=5))
            parts.add(ParametricFunction(F, t_range=[i / NPIECE, (i + 1) / NPIECE, 0.002],
                                         color=col, stroke_width=7))
            if i < NPIECE - 1:
                parts.add(Line(ends[i + 1], x0, color=col, stroke_width=5))
            hl = segs[i].copy().set_stroke(width=14)
            self.play(Create(parts), FadeIn(hl), prod[i + 1].animate.set_opacity(1).set_color(col),
                      run_time=0.65)
            self.play(FadeOut(parts), FadeOut(hl), run_time=0.25)
        self.play(pieces.animate.set_stroke(opacity=1.0), gs.animate.set_stroke(opacity=1.0),
                  run_time=0.6)
        box = SurroundingRectangle(prod, color=YELLOW, buff=0.08)
        self.play(Create(box), run_time=0.6)
        self.wait(2.0)


# =================================== 4.6 Example 4: punctured torus onto a v b
SQ = 1.6                         # half side of the square
SC = np.array([-3.4, -0.2, 0.0])  # centre c of the square
GR = 0.42                        # radius of the small loop gamma
FA = np.array([2.35, -0.2, 0.0])  # figure eight on the right: centre of the a-loop
FB = np.array([4.75, -0.2, 0.0])  # centre of the b-loop
FR = 1.2
CA_, CB_ = BLUE_C, ORANGE


def sqproj(p):
    """Radial projection from c onto the boundary of the square."""
    v = p - SC
    m = max(abs(v[0]), abs(v[1]))
    return SC + v * (SQ / m)


def H(p, s):
    return (1 - s) * p + s * sqproj(p)


def gamma(u):
    th = -3 * np.pi / 4 + TAU * u          # starts at the bottom-left corner direction
    return SC + GR * np.array([np.cos(th), np.sin(th), 0.0])


def boundary(u):
    """The image of gamma at s=1: bottom (a), right (b), top backwards, left backwards."""
    corners = [SC + SQ * np.array(c) for c in [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]]
    k = min(int(u * 4), 3)
    w = u * 4 - k
    return (1 - w) * corners[k] + w * corners[(k + 1) % 4]


def eight(u):
    """Same parametrisation on the figure eight a v b: a, b, a^-1, b^-1."""
    k = min(int(u * 4), 3)
    w = u * 4 - k
    if k == 0:   # a forwards
        th = w * TAU
        return FA + FR * np.array([np.cos(th), np.sin(th), 0])
    if k == 1:   # b forwards
        th = np.pi - w * TAU
        return FB + FR * np.array([np.cos(th), np.sin(th), 0])
    if k == 2:   # a backwards
        th = -w * TAU
        return FA + FR * np.array([np.cos(th), np.sin(th), 0])
    th = np.pi + w * TAU  # b backwards
    return FB + FR * np.array([np.cos(th), np.sin(th), 0])


class PuncturedTorusRetract(Scene):
    def construct(self):
        title = MathTex(r"U=T^2\setminus\{c\}", color=WHITE).scale(0.85).to_corner(UL, buff=0.4)
        self.play(FadeIn(title), run_time=0.5)

        crn = [SC + SQ * np.array(c) for c in [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]]
        bot = Line(crn[0], crn[1], color=CA_, stroke_width=6)
        rig = Line(crn[1], crn[2], color=CB_, stroke_width=6)
        top = Line(crn[3], crn[2], color=CA_, stroke_width=6)
        lef = Line(crn[0], crn[3], color=CB_, stroke_width=6)
        marks = VGroup(chevron(bot.get_center(), RIGHT, CA_), chevron(top.get_center(), RIGHT, CA_),
                       chevron(rig.get_center(), UP, CB_, n=2), chevron(lef.get_center(), UP, CB_, n=2))
        la = VGroup(MathTex("a", color=CA_).scale(0.75).next_to(bot, DOWN, buff=0.15),
                    MathTex("a", color=CA_).scale(0.75).next_to(top, UP, buff=0.15))
        lb = VGroup(MathTex("b", color=CB_).scale(0.75).next_to(lef, LEFT, buff=0.15),
                    MathTex("b", color=CB_).scale(0.75).next_to(rig, RIGHT, buff=0.15))
        fill = Square(side_length=2 * SQ, stroke_width=0, fill_color=GREY_E,
                      fill_opacity=0.6).move_to(SC)
        self.play(FadeIn(fill), Create(VGroup(bot, rig, top, lef)), FadeIn(marks),
                  FadeIn(la), FadeIn(lb), run_time=1.4)
        cdot = Circle(radius=0.07, color=RED_C, stroke_width=3).move_to(SC)
        clab = MathTex("c", color=RED_C).scale(0.7).next_to(cdot, UR, buff=0.04)
        self.play(Create(cdot), FadeIn(clab), run_time=0.6)

        # seeds of the radial deformation
        seeds = []
        for r in [0.3, 0.6, 0.9, 1.2, 1.45]:
            for k in range(16):
                th = k * TAU / 16 + (0.2 if r in (0.6, 1.2) else 0)
                seeds.append(SC + r * np.array([np.cos(th), np.sin(th), 0]))
        st = ValueTracker(0.0)
        dots = always_redraw(lambda: VGroup(*[Dot(H(p, st.get_value()), radius=0.035,
                                                  color=GREY_B) for p in seeds]))
        gam = always_redraw(lambda: ParametricFunction(
            lambda u: H(gamma(u), st.get_value()), t_range=[0, 1, 0.002],
            color=PURPLE_B, stroke_width=4.5))
        glab = MathTex(r"\gamma", color=PURPLE_B).scale(0.75).move_to(SC + np.array([0.0, -0.68, 0]))
        cap = caption(r"$\gamma$: a small loop around $c$, generator of $\pi(U\cap V)\cong\mathbb{Z}$", size=28)
        self.play(FadeIn(dots), Create(gam), FadeIn(glab), FadeIn(cap), run_time=1.4)
        self.wait(0.5)

        cap2 = caption(r"push radially away from $c$ onto $\partial(\text{square})$", size=28)
        slab = always_redraw(lambda: MathTex(r"s=%.2f" % st.get_value(), color=YELLOW)
                             .scale(0.7).next_to(title, DOWN, buff=0.25, aligned_edge=LEFT))
        self.play(FadeOut(cap), FadeIn(cap2), FadeOut(glab), FadeOut(fill), run_time=0.6)
        self.add(slab)
        self.play(st.animate.set_value(1.0), run_time=4.5, rate_func=smooth)
        self.wait(0.4)

        # on the torus the boundary of the square is a v b
        cap3 = caption(r"in $T^2$ all four corners are one point: $\partial(\text{square})=a\vee b$", size=28)
        ea = ParametricFunction(lambda u: FA + FR * np.array([np.cos(u), np.sin(u), 0]),
                                t_range=[0, TAU, 0.01], color=CA_, stroke_width=6)
        eb = ParametricFunction(lambda u: FB + FR * np.array([np.cos(u), np.sin(u), 0]),
                                t_range=[0, TAU, 0.01], color=CB_, stroke_width=6)
        em = VGroup(chevron(FA + FR * UP, LEFT, CA_), chevron(FB + FR * UP, RIGHT, CB_, n=2))
        eal = MathTex("a", color=CA_).scale(0.8).move_to(FA + LEFT * (FR + 0.3))
        ebl = MathTex("b", color=CB_).scale(0.8).move_to(FB + RIGHT * (FR + 0.3))
        wedge = Dot((FA + FB) / 2, color=WHITE, radius=0.06)
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.5)
        self.play(TransformFromCopy(VGroup(bot, top), ea), TransformFromCopy(VGroup(lef, rig), eb),
                  FadeIn(em), FadeIn(eal), FadeIn(ebl), FadeIn(wedge), run_time=1.6)
        self.wait(0.5)

        # read off phi_1(gamma) = a b a^-1 b^-1
        word = MathTex(r"\varphi_1(\gamma)=", r"a", r"b", r"a^{-1}", r"b^{-1}").scale(0.95)
        word.move_to([0.6, -2.85, 0])
        for k, c in zip(range(1, 5), [CA_, CB_, CA_, CB_]):
            word[k].set_color(c).set_opacity(0.2)
        self.play(FadeOut(cap3), FadeIn(word), FadeOut(dots), run_time=0.6)
        ut = ValueTracker(0.0)
        tr1 = always_redraw(lambda: Dot(boundary(ut.get_value()), color=PURPLE_B, radius=0.1))
        tr2 = always_redraw(lambda: Dot(eight(ut.get_value()), color=PURPLE_B, radius=0.1))
        self.add(tr1, tr2)
        for k in range(4):
            self.play(ut.animate.set_value((k + 1) / 4), word[k + 1].animate.set_opacity(1.0),
                      run_time=1.3, rate_func=linear)
        self.wait(0.6)

        res = MathTex(r"\pi(T^2)\cong F(a,b)/N\cong\mathbb{Z}\times\mathbb{Z}").scale(0.85)
        res.move_to([0.6, -3.55, 0])
        self.play(Write(res), run_time=1.3)
        self.wait(2.0)

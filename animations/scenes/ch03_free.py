"""Chapter 3 (Cairo renderer, 2D).

DirectSumUniversal  -- the universal property of the direct sum: the maps psi_i
                       out of the summands determine one and only one f out of G.
WeakProductSupport  -- the weak product inside the full product: all but finitely
                       many coordinates are the identity; and the model Z<S>.

Render: tools/bg.sh qh ch03_free.py DirectSumUniversal WeakProductSupport
"""
from manim import *
import numpy as np

C_G, C_A, C_SUM, C_PSI, C_F, C_OFF = BLUE_C, ORANGE, YELLOW, GREEN_B, RED_C, GREY_B


def caption(tex, size=30):
    return Tex(tex, font_size=size).to_corner(UR, buff=0.4).shift(DOWN * 0.85)


# ===================================================== 1. universality of the direct sum
N = 4                                   # how many summands we draw
GX = -4.6                               # column of the G_i
SX = -1.15                              # column of the direct sum
AX = 3.4                                # the target A
YS = 1.25


def gi_pos(k):
    return np.array([GX, (N - 1) / 2.0 * YS - k * YS, 0.0])


class DirectSumUniversal(Scene):
    def construct(self):
        gis = VGroup(*[MathTex(r"G_{%d}" % (k + 1), color=C_G).scale(0.85).move_to(gi_pos(k))
                       for k in range(N)])
        dots_g = MathTex(r"\vdots", color=C_G).scale(0.8).move_to(gi_pos(N - 1) + DOWN * 0.72)
        summ = MathTex(r"\bigoplus_{i\in I} G_i", color=C_SUM).scale(0.85).move_to([SX, 0, 0])
        a = MathTex(r"A", color=C_A).scale(1.0).move_to([AX, 0, 0])

        self.play(LaggedStart(*[FadeIn(g) for g in gis], lag_ratio=0.15), FadeIn(dots_g), run_time=1.4)
        self.play(FadeIn(summ), FadeIn(a), run_time=0.8)

        off = [UP * (0.30 * ((N - 1) / 2.0 - k)) for k in range(N)]
        phis = VGroup(*[Arrow(gi_pos(k) + RIGHT * 0.42,
                              summ.get_left() + LEFT * 0.10 + off[k],
                              color=C_OFF, stroke_width=3, buff=0.06,
                              max_tip_length_to_length_ratio=0.07) for k in range(N)])
        plab = MathTex(r"\varphi_i", color=C_OFF).scale(0.68).move_to(
            (gi_pos(0) + np.array([SX, 0, 0])) / 2 + UP * 0.42)
        self.play(LaggedStart(*[GrowArrow(p) for p in phis], lag_ratio=0.12),
                  FadeIn(plab), run_time=1.5)

        cap = caption(r"given any $\psi_i : G_i \to A$ \dots")
        self.play(FadeIn(cap), run_time=0.6)

        PANG = [-1.05, -0.62, 0.62, 1.05]
        psis = VGroup(*[CurvedArrow(gi_pos(k) + RIGHT * 0.42, a.get_left() + LEFT * 0.1,
                                    angle=PANG[k], color=C_PSI, stroke_width=3,
                                    tip_length=0.16) for k in range(N)])
        pslab = MathTex(r"\psi_i", color=C_PSI).scale(0.72).move_to([0.6, 2.45, 0])
        self.play(LaggedStart(*[Create(p) for p in psis], lag_ratio=0.18),
                  FadeIn(pslab), run_time=2.0)
        self.wait(0.5)

        f = DashedVMobject(Arrow(summ.get_right() + RIGHT * 0.05, a.get_left() + LEFT * 0.05,
                                 color=C_F, stroke_width=5, buff=0.08,
                                 max_tip_length_to_length_ratio=0.09), num_dashes=16)
        flab = MathTex(r"\exists\,!\ f", color=C_F).scale(0.82).move_to(
            [(SX + AX) / 2.0, 0.46, 0])
        cap2 = caption(r"\dots there is exactly one $f$ with $\psi_i = f\circ\varphi_i$")
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.6)
        self.play(Create(f), FadeIn(flab), run_time=1.3)
        self.wait(0.6)

        formula = MathTex(r"f\big((g_i)_{i\in I}\big) \;=\; \sum_{i\in I}\psi_i(g_i)",
                          color=WHITE).scale(0.92).to_edge(DOWN, buff=0.55)
        box = SurroundingRectangle(formula, color=C_SUM, buff=0.22, stroke_width=2.5)
        self.play(Write(formula), run_time=1.6)
        self.play(Create(box), run_time=0.6)

        fin = MathTex(r"\text{finite sum}\Rightarrow\text{well defined}",
                      color=GREY_A).scale(0.55).to_corner(UL, buff=0.45)
        self.play(FadeIn(fin), run_time=0.7)
        self.wait(1.4)

        cap3 = caption(r"uniqueness: $h\circ\varphi_i=\psi_i\Rightarrow h=f$")
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.6)
        self.play(Indicate(f, color=C_F, scale_factor=1.12), run_time=1.2)
        self.wait(1.4)


# ===================================================== 2. weak product / finite support
M = 9                                   # number of visible coordinates
CELL = 0.92
ROW_Y_FULL, ROW_Y_WEAK = 1.55, -0.65


def cell_x(k):
    return (k - (M - 1) / 2.0) * CELL - 0.70


def row(y, entries, color):
    g = VGroup()
    for k, e in enumerate(entries):
        sq = Square(CELL * 0.86, stroke_color=GREY_B, stroke_width=2,
                    fill_color=GREY_E, fill_opacity=0.45).move_to([cell_x(k), y, 0])
        t = MathTex(e, color=color).scale(0.52).move_to([cell_x(k), y, 0])
        g.add(VGroup(sq, t))
    return g


class WeakProductSupport(Scene):
    def construct(self):
        idx = VGroup(*[MathTex(r"i_{%d}" % (k + 1), color=GREY_A).scale(0.42)
                       .move_to([cell_x(k), ROW_Y_FULL + 0.68, 0]) for k in range(M)])

        full_entries = [r"g_{%d}" % (k + 1) for k in range(M)]
        weak_entries = [r"1" for _ in range(M)]
        for k in (2, 3, 7):
            weak_entries[k] = r"g_{%d}" % (k + 1)

        r1 = row(ROW_Y_FULL, full_entries, C_G)
        l1 = MathTex(r"\prod_{i\in I} G_i", color=C_G).scale(0.72).next_to(r1, LEFT, buff=0.35)
        r2 = row(ROW_Y_WEAK, weak_entries, C_SUM)
        l2 = MathTex(r"\prod^{\mathrm{wk}}_{i\in I} G_i", color=C_SUM).scale(0.72).next_to(r2, LEFT, buff=0.35)

        self.play(FadeIn(idx), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(c) for c in r1], lag_ratio=0.05), FadeIn(l1), run_time=1.6)
        cap = caption(r"in $\prod_i G_i$ every coordinate is free", size=28)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(0.8)

        self.play(LaggedStart(*[FadeIn(c) for c in r2], lag_ratio=0.05), FadeIn(l2), run_time=1.6)
        cap2 = caption(r"in $\prod^{\mathrm{wk}}_i G_i$ all but finitely many are $1_{G_i}$", size=28)
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.6)

        marks = VGroup(*[Square(CELL * 0.86, stroke_color=C_F, stroke_width=4)
                         .move_to([cell_x(k), ROW_Y_WEAK, 0]) for k in (2, 3, 7)])
        self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.2), run_time=1.2)
        sup = MathTex(r"\text{finite support}", color=C_F).scale(0.6).next_to(r2, DOWN, buff=1.05)
        self.play(FadeIn(sup), run_time=0.6)
        self.wait(1.2)

        cap3 = caption(r"$\mathbb{Z}\langle S\rangle$: the same idea with $G_s=\mathbb{Z}$", size=28)
        self.play(FadeOut(cap2), FadeIn(cap3), run_time=0.6)

        z_entries = [r"0" for _ in range(M)]
        for k, v in ((2, r"3"), (3, r"-1"), (7, r"5")):
            z_entries[k] = v
        r3 = row(ROW_Y_WEAK, z_entries, C_SUM)
        self.play(Transform(r2, r3), run_time=1.4)
        slab = VGroup(*[MathTex(r"s_{%d}" % (k + 1), color=GREY_A).scale(0.42)
                        .move_to([cell_x(k), ROW_Y_WEAK - 0.78, 0]) for k in range(M)])
        self.play(FadeOut(sup), FadeIn(slab), run_time=0.7)

        expr = MathTex(r"\varphi \;=\; 3\,\varphi_{s_3} \;-\; \varphi_{s_4} \;+\; 5\,\varphi_{s_8}",
                       color=WHITE).scale(0.95).to_edge(DOWN, buff=0.6)
        self.play(Write(expr), run_time=1.8)
        gen = MathTex(r"\mathbb{Z}\langle S\rangle=\langle\,\varphi_s \mid s\in S\,\rangle",
                      color=GREY_A).scale(0.6).next_to(expr, UP, buff=0.25)
        self.play(FadeIn(gen), run_time=0.7)
        self.wait(2.0)

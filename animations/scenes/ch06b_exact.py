"""Chapter 6, second week (Cairo renderer, 2D).

ConnectingHomomorphism -- the diagram chase defining d_*: H_n(X,A) -> H_{n-1}(A):
                          u' -> lift u'' -> boundary d u'' -> it lies in C_{n-1}(A).
RelativeCycleDisk      -- (D^2, S^1): the disc is a relative 2-cycle (its boundary lies
                          in A), and d_* sends it to the circle, a generator of H_1(S^1).
FiveLemmaInjective     -- the chase in part (1) of the five lemma: f2, f4 1-1 and f1 onto
                          force ker f3 = 1.

Render: tools/bgc.sh 37 qh ch06b_exact.py ConnectingHomomorphism   (one core each)
"""
from manim import *
import numpy as np

CEL, COK, CBAD = YELLOW, GREEN_C, RED_C


def caption(tex, size=30):
    return Tex(tex, font_size=size).to_edge(DOWN, buff=0.45)


def node(tex, pos, scale=0.85, color=WHITE):
    return MathTex(tex, color=color).scale(scale).move_to(pos)


def harrow(a, b, color=GREY_B, label=None, up=True):
    arr = Arrow(a.get_right(), b.get_left(), buff=0.15, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.15)
    if label is None:
        return VGroup(arr)
    lab = MathTex(label, color=color).scale(0.55).next_to(arr, UP if up else DOWN, buff=0.05)
    return VGroup(arr, lab)


def varrow(a, b, color=GREY_B, label=None):
    arr = Arrow(a.get_bottom(), b.get_top(), buff=0.12, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.15)
    if label is None:
        return VGroup(arr)
    lab = MathTex(label, color=color).scale(0.55).next_to(arr, LEFT, buff=0.05)
    return VGroup(arr, lab)


# ===================================================== 1. the connecting homomorphism
XS = [-5.6, -3.1, 0.0, 3.1, 5.6]
YT, YB = 1.3, -1.1


class ConnectingHomomorphism(Scene):
    def construct(self):
        title = MathTex(r"\partial_*:H_n(X,A)\to H_{n-1}(A)").scale(0.85).to_edge(UP, buff=0.35)
        self.play(FadeIn(title), run_time=0.5)
        top = [node("0", [XS[0], YT, 0]), node(r"C_n(A)", [XS[1], YT, 0]),
               node(r"C_n(X)", [XS[2], YT, 0]), node(r"C_n(X,A)", [XS[3], YT, 0]),
               node("0", [XS[4], YT, 0])]
        bot = [node("0", [XS[0], YB, 0]), node(r"C_{n-1}(A)", [XS[1], YB, 0]),
               node(r"C_{n-1}(X)", [XS[2], YB, 0]), node(r"C_{n-1}(X,A)", [XS[3], YB, 0]),
               node("0", [XS[4], YB, 0])]
        labs = [None, r"i_\#", r"j_\#", None]
        ht = VGroup(*[harrow(top[k], top[k + 1], label=labs[k]) for k in range(4)])
        hb = VGroup(*[harrow(bot[k], bot[k + 1], label=labs[k], up=True) for k in range(4)])
        vs = VGroup(*[varrow(top[k], bot[k], label=r"\partial_n") for k in (1, 2, 3)])
        self.play(FadeIn(VGroup(*top, *bot)), run_time=0.8)
        self.play(Create(ht), Create(hb), Create(vs), run_time=1.4)
        cap = caption(r"rows exact, squares commute")
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(0.5)

        # step 1: u' in C_n(X,A), a relative cycle
        d1 = Dot(top[3].get_center() + UP * 0.55, color=CEL)
        l1 = MathTex(r"u'", color=CEL).scale(0.7).next_to(d1, UP, buff=0.08)
        c1 = caption(r"$u=u'+B_n(X,A)$ with $\partial_nu'=0$ in $C_{n-1}(X,A)$")
        self.play(FadeOut(cap), FadeIn(c1), FadeIn(d1), FadeIn(l1), run_time=0.7)
        self.wait(0.4)

        # step 2: lift along j_#
        d2 = Dot(top[2].get_center() + UP * 0.55, color=CEL)
        l2 = MathTex(r"u''", color=CEL).scale(0.7).next_to(d2, UP, buff=0.08)
        lift = CurvedArrow(d1.get_center(), d2.get_center(), angle=0.6, color=CEL, stroke_width=3)
        c2 = caption(r"$j_\#$ is onto: choose $u''\in C_n(X)$ with $j_\#(u'')=u'$")
        self.play(FadeOut(c1), FadeIn(c2), Create(lift), run_time=0.8)
        self.play(FadeIn(d2), FadeIn(l2), run_time=0.5)
        self.wait(0.4)

        # step 3: boundary
        d3 = Dot(bot[2].get_center() + DOWN * 0.55, color=CEL)
        l3 = MathTex(r"\partial_nu''", color=CEL).scale(0.7).next_to(d3, DOWN, buff=0.08)
        down = Arrow(d2.get_center() + RIGHT * 0.8, d3.get_center() + RIGHT * 0.8, buff=0.1,
                     color=CEL, stroke_width=3)
        c3 = caption(r"apply $\partial_n$")
        self.play(FadeOut(c2), FadeIn(c3), GrowArrow(down), run_time=0.7)
        self.play(FadeIn(d3), FadeIn(l3), run_time=0.5)
        self.wait(0.3)

        # step 4: it maps to zero in C_{n-1}(X,A)
        d4 = Dot(bot[3].get_center() + DOWN * 0.55, color=COK)
        l4 = MathTex(r"j_\#\partial_nu''=\partial_nu'=0", color=COK).scale(0.62).next_to(d4, DOWN, buff=0.08)
        right = CurvedArrow(d3.get_center(), d4.get_center(), angle=0.5, color=COK, stroke_width=3)
        c4 = caption(r"commutativity: $j_\#(\partial_nu'')=\partial_n(j_\#u'')=\partial_nu'=0$")
        self.play(FadeOut(c3), FadeIn(c4), Create(right), run_time=0.7)
        self.play(FadeIn(d4), FadeIn(l4), run_time=0.5)
        self.wait(0.4)

        # step 5: so it comes from C_{n-1}(A)
        d5 = Dot(bot[1].get_center() + DOWN * 0.55, color=CEL)
        l5 = MathTex(r"\partial_nu''\in Z_{n-1}(A)", color=CEL).scale(0.62).next_to(d5, DOWN, buff=0.08)
        back = CurvedArrow(d3.get_center(), d5.get_center(), angle=-0.5, color=CEL, stroke_width=3)
        c5 = caption(r"exactness: $\ker j_\#=\operatorname{im} i_\#$, so $\partial_nu''\in C_{n-1}(A)$; and $\partial\partial=0$")
        self.play(FadeOut(c4), FadeIn(c5), Create(back), run_time=0.8)
        self.play(FadeIn(d5), FadeIn(l5), run_time=0.5)
        self.wait(0.5)

        # result: the snake
        res = MathTex(r"\partial_*u:=\partial_nu''+B_{n-1}(A)\ \in H_{n-1}(A)", color=CEL).scale(0.8)
        res.to_edge(DOWN, buff=0.45)
        snake = CubicBezier(top[3].get_center() + UP * 0.9, top[3].get_center() + UP * 1.9 + RIGHT * 0.3,
                            bot[1].get_center() + DOWN * 2.0 + LEFT * 0.6, bot[1].get_center() + DOWN * 0.95,
                            color=CEL, stroke_width=2.5).set_opacity(0.55)
        self.play(FadeOut(c5), FadeIn(res), run_time=0.6)
        box = SurroundingRectangle(res, color=CEL, buff=0.12)
        self.play(Create(box), run_time=0.6)
        self.wait(2.2)


# ===================================================== 2. a relative cycle in (D^2, S^1)
DC = np.array([-3.4, 0.7, 0])
DR = 2.0
SC = np.array([3.6, 0.7, 0])


class RelativeCycleDisk(Scene):
    def construct(self):
        title = MathTex(r"(X,A)=(D^2,S^1)").scale(0.85).to_edge(UP, buff=0.35)
        self.play(FadeIn(title), run_time=0.5)
        disk = Circle(radius=DR, stroke_width=0, fill_color=BLUE_E, fill_opacity=0.0).move_to(DC)
        bd = Circle(radius=DR, color=ORANGE, stroke_width=6).move_to(DC)
        lA = MathTex(r"A=S^1", color=ORANGE).scale(0.7).next_to(bd, UL, buff=-0.2)
        lX = MathTex(r"X=D^2").scale(0.7).move_to(DC + DOWN * (DR + 0.45))
        self.play(FadeIn(disk), Create(bd), FadeIn(lA), FadeIn(lX), run_time=1.0)

        c1 = caption(r"the disc $D$ as a 2-chain: $\partial D=$ the circle, which lies in $A$")
        self.play(FadeIn(c1), disk.animate.set_fill(BLUE_D, opacity=0.55), run_time=1.2)
        arrows = VGroup(*[Arrow(DC + DR * np.array([np.cos(t), np.sin(t), 0]),
                                DC + DR * np.array([np.cos(t + 0.35), np.sin(t + 0.35), 0]),
                                buff=0, color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.5)
                          for t in np.linspace(0, TAU, 6, endpoint=False)])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), run_time=1.2)
        c2 = caption(r"$\partial D\in C_1(A)\ \Rightarrow\ \partial D=0$ in $C_1(X,A)$: $D$ is a relative 2-cycle")
        self.play(FadeOut(c1), FadeIn(c2), run_time=0.6)
        self.wait(0.6)

        # d_* : lift off the boundary
        circ = VGroup(bd.copy(), arrows.copy())
        arr = Arrow(DC + RIGHT * (DR + 0.3), SC + LEFT * (DR + 0.35), buff=0.1, stroke_width=4)
        lab = MathTex(r"\partial_*").scale(0.85).next_to(arr, UP, buff=0.1)
        c3 = caption(r"$\partial_*[D]=[\partial D]=$ the circle $\in H_1(S^1)\cong\mathbb{Z}$, a generator")
        self.play(FadeOut(c2), FadeIn(c3), GrowArrow(arr), FadeIn(lab), run_time=0.7)
        self.play(circ.animate.move_to(SC), run_time=1.5)
        lS = MathTex(r"[S^1]\in H_1(A)", color=ORANGE).scale(0.7).next_to(circ, UP, buff=0.2)
        self.play(FadeIn(lS), run_time=0.5)
        self.wait(0.6)

        seq = MathTex(r"\underbrace{H_2(D^2)}_{0}\to H_2(D^2,S^1)\xrightarrow{\ \partial_*\ }H_1(S^1)\to"
                      r"\underbrace{H_1(D^2)}_{0}").scale(0.72)
        seq.to_edge(DOWN, buff=0.35)
        concl = MathTex(r"\Rightarrow\ \partial_*:H_2(D^2,S^1)\xrightarrow{\ \cong\ }H_1(S^1)", color=YELLOW).scale(0.72)
        concl.next_to(seq, UP, buff=0.18)
        self.play(FadeOut(c3), FadeIn(seq), run_time=0.8)
        self.play(FadeIn(concl), run_time=0.7)
        self.wait(2.2)


# ===================================================== 3. five lemma, part (1)
FX = [-5.2, -2.6, 0.0, 2.6, 5.2]
FYT, FYB = 1.4, -0.9


class FiveLemmaInjective(Scene):
    def construct(self):
        title = Tex(r"Five lemma (1): $f_2,f_4$ 1--1 and $f_1$ onto $\Rightarrow$ $f_3$ 1--1",
                    font_size=32).to_edge(UP, buff=0.3)
        self.play(FadeIn(title), run_time=0.5)
        A = [node(r"A_%d" % (k + 1), [FX[k], FYT, 0]) for k in range(5)]
        B = [node(r"B_%d" % (k + 1), [FX[k], FYB, 0]) for k in range(5)]
        ha = VGroup(*[harrow(A[k], A[k + 1], label=r"i_%d" % (k + 1)) for k in range(4)])
        hb = VGroup(*[harrow(B[k], B[k + 1], label=r"j_%d" % (k + 1), up=False) for k in range(4)])
        hyp = {0: ("onto", BLUE_C), 1: ("1-1", ORANGE), 3: ("1-1", ORANGE)}
        vs = VGroup()
        for k in range(5):
            v = varrow(A[k], B[k], label=r"f_%d" % (k + 1))
            vs.add(v)
            if k in hyp:
                t, c = hyp[k]
                vs.add(Tex(t, font_size=22, color=c).next_to(v[0], RIGHT, buff=0.08))
        self.play(FadeIn(VGroup(*A, *B)), Create(ha), Create(hb), Create(vs), run_time=1.6)

        def dot_at(m, side, col=CEL):
            return Dot(m.get_center() + side * 0.5, color=col, radius=0.07)

        def say(tex, old=None):
            c = caption(tex, size=28)
            anims = [FadeIn(c)] + ([FadeOut(old)] if old is not None else [])
            self.play(*anims, run_time=0.5)
            return c

        x = dot_at(A[2], UP)
        lx = MathTex("x", color=CEL).scale(0.65).next_to(x, UP, buff=0.05)
        c = say(r"take $x\in A_3$ with $f_3(x)=1$")
        fx = dot_at(B[2], DOWN, COK)
        lfx = MathTex("1", color=COK).scale(0.65).next_to(fx, DOWN, buff=0.05)
        self.play(FadeIn(x), FadeIn(lx), FadeIn(fx), FadeIn(lfx), run_time=0.6)
        self.wait(0.3)

        i3x = dot_at(A[3], UP, COK)
        li3x = MathTex(r"i_3(x)=1", color=COK).scale(0.6).next_to(i3x, UP, buff=0.05)
        c = say(r"$f_4(i_3x)=j_3(f_3x)=1$ and $f_4$ is 1--1 $\Rightarrow$ $i_3(x)=1$", c)
        self.play(TransformFromCopy(x, i3x), FadeIn(li3x), run_time=0.8)
        self.wait(0.3)

        y = dot_at(A[1], UP)
        ly = MathTex("y", color=CEL).scale(0.65).next_to(y, UP, buff=0.05)
        c = say(r"$x\in\ker i_3=\operatorname{im}i_2$: $x=i_2(y)$", c)
        self.play(FadeIn(y), FadeIn(ly), Indicate(ha[1], color=CEL), run_time=0.8)

        fy = dot_at(B[1], DOWN)
        lfy = MathTex(r"f_2(y)", color=CEL).scale(0.6).next_to(fy, DOWN, buff=0.05)
        c = say(r"$j_2(f_2y)=f_3(i_2y)=f_3(x)=1$ $\Rightarrow$ $f_2(y)\in\ker j_2=\operatorname{im}j_1$", c)
        self.play(TransformFromCopy(y, fy), FadeIn(lfy), run_time=0.8)

        z = dot_at(B[0], DOWN)
        lz = MathTex("z", color=CEL).scale(0.65).next_to(z, DOWN, buff=0.05)
        w = dot_at(A[0], UP)
        lw = MathTex("w", color=CEL).scale(0.65).next_to(w, UP, buff=0.05)
        c = say(r"$f_2(y)=j_1(z)$, and $f_1$ onto: $z=f_1(w)$", c)
        self.play(FadeIn(z), FadeIn(lz), run_time=0.6)
        self.play(TransformFromCopy(z, w), FadeIn(lw), run_time=0.7)

        c = say(r"$f_2(i_1w)=j_1(f_1w)=j_1(z)=f_2(y)$ and $f_2$ is 1--1 $\Rightarrow$ $y=i_1(w)$", c)
        self.play(Indicate(ly, color=YELLOW), Indicate(lw, color=YELLOW), run_time=0.9)
        self.wait(0.3)

        c = say(r"$x=i_2(y)=i_2(i_1w)=1$ since $\operatorname{im}i_1=\ker i_2$. \ So $\ker f_3=1$.", c)
        newlx = MathTex("x=1", color=COK).scale(0.7).move_to(lx)
        self.play(Transform(lx, newlx), x.animate.set_color(COK), run_time=0.8)
        box = SurroundingRectangle(VGroup(A[2], x, lx), color=COK, buff=0.15)
        self.play(Create(box), run_time=0.6)
        self.wait(2.2)

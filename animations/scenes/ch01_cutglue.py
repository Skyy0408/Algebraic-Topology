"""Chapter 1: cut-and-glue arguments in the plane (Cairo renderer, CPU).

Every stage is a list of pieces; a piece is a list of edges, each edge a sampled
polyline with a name, arrow count and direction.  Stages share their structure,
so Transform(stage_k, stage_k+1) morphs one picture into the next.

Render: manim -qh ch01_cutglue.py <Scene>
"""
from manim import *
import numpy as np

COL = {"a": BLUE_C, "b": ORANGE, "c": GREEN_C, "d": PURPLE_B, "e": TEAL_C, "f": GOLD,
       "A": GREY_A, "B": GREY_A, "C": GREY_A, None: GREY_B}
N = 26
THIN, BOLD = 5, 9


def seg(p, q):
    p, q = np.array([*p, 0.0]), np.array([*q, 0.0])
    return np.array([p + (q - p) * t for t in np.linspace(0, 1, N)])


def arc(c, R, a0, a1):
    ts = np.deg2rad(np.linspace(a0, a1, N))
    return np.array([[c[0] + R * np.cos(t), c[1] + R * np.sin(t), 0.0] for t in ts])


def E(pts, name, tex=None, n=1, sign=1, hidden=False):
    return dict(pts=np.asarray(pts, dtype=float), name=name, tex=tex if tex is not None else name,
                n=n, sign=sign, hidden=hidden)


def shift(edges, dx, dy=0.0):
    out = []
    for e in edges:
        f = dict(e)
        f["pts"] = e["pts"] + np.array([dx, dy, 0.0])
        out.append(f)
    return out


def flip_y(edges, about=0.0):
    out = []
    for e in edges:
        f = dict(e)
        p = e["pts"].copy()
        p[:, 1] = 2 * about - p[:, 1]
        f["pts"] = p
        out.append(f)
    return out


def _chev(mid, d, n, col, size=0.15):
    nrm = np.array([-d[1], d[0], 0.0])
    g = VGroup()
    for k in range(n):
        c = mid + d * (k - (n - 1) / 2) * size * 1.15
        tip = c + d * size / 2
        g.add(VMobject().set_points_as_corners(
            [tip - d * size + nrm * size * 0.6, tip, tip - d * size - nrm * size * 0.6]).set_stroke(col, 4))
    return g


def draw(pieces, bold=(), label_scale=0.62):
    """pieces: list of list-of-edges. Returns a VGroup with a fixed structure per stage."""
    g = VGroup()
    for edges in pieces:
        loop = np.concatenate([e["pts"] for e in edges])
        g.add(VMobject().set_points_as_corners(loop).set_fill(GREY_E, 0.75).set_stroke(width=0))
    for edges in pieces:
        cen = np.concatenate([e["pts"] for e in edges]).mean(axis=0)
        for e in edges:
            pts, col = e["pts"], COL[e["name"]]
            op = 0.0 if e["hidden"] else 1.0
            w = BOLD if e["name"] in bold else THIN
            g.add(VMobject().set_points_as_corners(pts).set_stroke(col, w, opacity=op))
            m = N // 2
            d = pts[m] - pts[m - 1]
            L = np.linalg.norm(d)
            d = d / L if L > 1e-9 else RIGHT
            mid = (pts[m] + pts[m - 1]) / 2
            ch = _chev(mid, d * e["sign"], e["n"], col).set_stroke(opacity=op)
            nrm = np.array([d[1], -d[0], 0.0])
            if np.dot(nrm, mid - cen) < 0:
                nrm = -nrm
            lab = MathTex(e["tex"], color=col).scale(label_scale).move_to(mid + nrm * 0.3)
            if op == 0.0:
                lab.set_opacity(0).scale(0.02)
                ch.scale(0.02)
            g.add(ch, lab)
    return g


def cap(tex, old=None):
    new = Tex(tex, font_size=32).to_edge(DOWN, buff=0.45)
    return new, [FadeIn(new)] + ([FadeOut(old)] if old else [])


# ================================================================= RP^2 \ D = Mobius band
R_OUT = 1.75


def half_annulus(upper, r):
    """Half of the annulus (or of the disk when r = 0).
    Radial cut at theta = 0 is p, at theta = 180 is q; outer arc a, inner arc c."""
    a0, a1 = (0, 180) if upper else (180, 360)
    P = lambda R, t: (R * np.cos(np.deg2rad(t)), R * np.sin(np.deg2rad(t)))
    rr = max(r, 1e-3)
    cut_out, cut_in = ("q", "p") if upper else ("p", "q")     # edge at a1, edge at a0
    return [E(arc((0, 0), R_OUT, a0, a1), "a", "a", 1, 1),
            E(seg(P(R_OUT, a1), P(rr, a1)), "d", cut_out, 1, 1, hidden=(r == 0)),
            E(arc((0, 0), rr, a1, a0), "c", "c", 1, 1, hidden=(r == 0)),
            E(seg(P(rr, a0), P(R_OUT, a0)), "d", cut_in, 1, 1, hidden=(r == 0))]


def rect(x0, x1, y0, y1, names):
    """Rectangle with edges (top, right, bottom, left); names = list of (key, tex, arrows, sign)."""
    (tn, tt, tc, ts), (rn, rt, rc, rs), (bn, bt, bc, bs), (ln, lt, lc, ls) = names
    return [E(seg((x0, y1), (x1, y1)), tn, tt, tc, ts),
            E(seg((x1, y1), (x1, y0)), rn, rt, rc, rs),
            E(seg((x1, y0), (x0, y0)), bn, bt, bc, bs),
            E(seg((x0, y0), (x0, y1)), ln, lt, lc, ls)]


class ProjectivePlaneMinusDisk(Scene):
    """Disk with antipodal boundary identification, minus a disk, is a Mobius band."""

    def construct(self):
        title = MathTex(r"\mathbb{RP}^2 \setminus D \;\cong\; \text{M\"obius band}").scale(0.9).to_edge(UP, buff=0.5)
        W, H = 2.7, 0.85
        s_disk = [half_annulus(True, 0.0), half_annulus(False, 0.0)]
        s_ann = [half_annulus(True, 0.55), half_annulus(False, 0.55)]
        s_cut = [shift(half_annulus(True, 0.55), 0, 0.3), shift(half_annulus(False, 0.55), 0, -0.3)]
        # U (lower rectangle): top a, right q, bottom c, left p
        U = rect(-W, W, -H - 0.25, -0.25, (("a", "a", 1, 1), ("d", "q", 1, -1), ("c", "c", 1, -1), ("d", "p", 1, 1)))
        # L flipped (upper rectangle): top c, right p, bottom a, left q
        L = rect(-W, W, 0.25, H + 0.25, (("c", "c", 1, -1), ("d", "p", 1, -1), ("a", "a", 1, 1), ("d", "q", 1, 1)))
        Ug = rect(-W, W, -H, 0, (("a", "a", 1, 1), ("d", "q", 1, -1), ("c", "c", 1, -1), ("d", "p", 1, 1)))
        Lg = rect(-W, W, 0, H, (("c", "c", 1, -1), ("d", "p", 1, -1), ("a", "a", 1, 1), ("d", "q", 1, 1)))

        s0 = draw(s_disk)
        self.play(FadeIn(title), FadeIn(s0), run_time=1.0)
        c1, an = cap(r"$\mathbb{RP}^2$: a disk, antipodal boundary points identified ($a$ with $a$)")
        self.play(*an, run_time=0.8)
        self.wait(0.5)
        hole = Circle(radius=0.55, color=RED_C, fill_color=RED_C, fill_opacity=0.85, stroke_width=0)
        c2, an = cap(r"remove a disk $D$ from the middle", c1)
        self.play(*an, FadeIn(hole), run_time=0.9)
        self.play(FadeOut(hole), Transform(s0, draw(s_ann)), run_time=1.2)
        c3, an = cap(r"cut along the diameter: two half-annuli, cuts $p$ and $q$", c2)
        self.play(*an, Transform(s0, draw(s_ann, bold=("d",))), run_time=0.8)
        self.play(Transform(s0, draw(s_cut, bold=("d",))), run_time=1.2)
        c4, an = cap(r"straighten both halves; flip the lower one", c3)
        self.play(*an, Transform(s0, draw([U, L])), run_time=1.8)
        c5, an = cap(r"glue the two $a$ edges (that is the antipodal identification)", c4)
        self.play(*an, Transform(s0, draw([U, L], bold=("a",))), run_time=0.8)
        self.play(Transform(s0, draw([Ug, Lg], bold=("a",))), run_time=1.4)
        Uh = [dict(e, hidden=(e["tex"] == "a")) for e in Ug]
        Lh = [dict(e, hidden=(e["tex"] == "a")) for e in Lg]
        c6, an = cap(r"ends glued crosswise ($p$ to $p$, $q$ to $q$): a M\"obius band", c5)
        self.play(*an, Transform(s0, draw([Uh, Lh], bold=("d",))), run_time=1.4)
        self.wait(1.4)
        self.play(FadeOut(c6))


# ================================================================= K = MB u MB
S = 1.55


class KleinTwoMobius(Scene):
    """The Klein bottle square cut into two Mobius bands."""

    def construct(self):
        title = MathTex(r"K \;=\; \mathrm{MB} \cup_\partial \mathrm{MB}").scale(0.9).to_edge(UP, buff=0.5)
        h = S / 3
        # Klein square: a on top and bottom (both pointing right); sides glued with a flip
        # (right side arrow down, left side arrow up)
        sq = [E(seg((-S, S), (S, S)), "a", "a", 1, 1),
              E(seg((S, S), (S, -S)), "b", "b", 2, 1),
              E(seg((S, -S), (-S, -S)), "a", "a", 1, -1),
              E(seg((-S, -S), (-S, S)), "b", "b", 2, 1)]
        top = [E(seg((-S, S), (S, S)), "a", "a", 1, 1), E(seg((S, S), (S, h)), "e", "f", 1, 1),
               E(seg((S, h), (-S, h)), "c", "c", 1, -1), E(seg((-S, h), (-S, S)), "f", "e", 1, 1)]
        mid = [E(seg((-S, h), (S, h)), "c", "c", 1, 1), E(seg((S, h), (S, -h)), "b", "b", 2, 1),
               E(seg((S, -h), (-S, -h)), "d", "d", 1, -1), E(seg((-S, -h), (-S, h)), "b", "b", 2, 1)]
        bot = [E(seg((-S, -h), (S, -h)), "d", "d", 1, 1), E(seg((S, -h), (S, -S)), "f", "e", 1, 1),
               E(seg((S, -S), (-S, -S)), "a", "a", 1, -1), E(seg((-S, -S), (-S, -h)), "e", "f", 1, 1)]
        s0 = draw([sq])
        self.play(FadeIn(title), FadeIn(s0), run_time=1.0)
        c1, an = cap(r"the Klein bottle square: the sides are glued with a flip")
        self.play(*an, run_time=0.8)
        self.wait(0.4)
        s1 = draw([top, mid, bot], bold=("c", "d"))
        self.remove(s0)
        s0 = s1
        c2, an = cap(r"cut along $c$ and $d$; the sides split into $e$, $b$, $f$", c1)
        self.play(*an, FadeIn(s0), run_time=1.0)
        self.play(Transform(s0, draw([shift(top, 0, 0.5), mid, shift(bot, 0, -0.5)])), run_time=1.0)
        c3, an = cap(r"middle strip: its two $b$ sides are glued with a flip $\Rightarrow$ M\"obius band", c2)
        self.play(*an, Transform(s0, draw([shift(top, 3.3, 0.5), shift(mid, -3.3), shift(bot, 3.3, -0.5)],
                                          bold=("b",))), run_time=1.5)
        c4, an = cap(r"the other two strips are glued to each other along $a$", c3)
        self.play(*an, Transform(s0, draw([shift(top, 3.3, 0.5), shift(mid, -3.3), shift(bot, 3.3, -0.5)],
                                          bold=("a",))), run_time=0.8)
        # bottom strip goes above the top strip so that the two a edges meet at y = 0
        gt = shift(top, 3.3, -S)            # its a edge (top, y = S) lands at y = 0
        gb = shift(bot, 3.3, S)             # its a edge (bottom, y = -S) lands at y = 0
        self.play(Transform(s0, draw([gt, shift(mid, -3.3), gb], bold=("a",))), run_time=1.5)
        gth = [dict(e, hidden=(e["tex"] == "a")) for e in gt]
        gbh = [dict(e, hidden=(e["tex"] == "a")) for e in gb]
        c5, an = cap(r"its ends carry $e$, $f$ crosswise: a second M\"obius band", c4)
        self.play(*an, Transform(s0, draw([gth, shift(mid, -3.3), gbh], bold=("e", "f"))), run_time=1.4)
        self.wait(1.4)
        self.play(FadeOut(c5))


# ================================================================= surgery: A b B b C -> A B^-1 a a C
def _poly(vertices, names):
    n = len(vertices)
    return [E(seg(vertices[k], vertices[(k + 1) % n]), nm, tx, na, sg)
            for k, (nm, tx, na, sg) in enumerate(names)]


def reflect_map(src_a, src_b, dst_a, dst_b):
    """Orientation-reversing isometry with src_a -> dst_a, src_b -> dst_b (complex form)."""
    z = lambda p: complex(p[0], p[1])
    al = (z(dst_a) - z(dst_b)) / np.conj(z(src_a) - z(src_b))
    be = z(dst_a) - al * np.conj(z(src_a))
    def T(edges):
        out = []
        for e in edges:
            f = dict(e)
            pts = e["pts"].copy()
            w = al * np.conj(pts[:, 0] + 1j * pts[:, 1]) + be
            pts[:, 0], pts[:, 1] = w.real, w.imag
            f["pts"] = pts
            out.append(f)
        return out
    return T


class SurgeryPairsAdjacent(Scene):
    """Surgery step: bring a pair of the 2nd kind together, A b B b C -> A B^{-1} a a C."""

    def construct(self):
        title = MathTex(r"A\,b\,B\,b\,C \;\longrightarrow\; A\,B^{-1}\,a\,a\,C").scale(0.85).to_edge(UP, buff=0.5)
        R = 2.1
        ang = [234, 306, 18, 90, 162]
        V = [np.array([R * np.cos(np.deg2rad(t)), R * np.sin(np.deg2rad(t))]) for t in ang]
        P = _poly(V, [("A", "A", 1, 1), ("b", "b", 1, 1), ("B", "B", 1, 1), ("b", "b", 1, 1), ("C", "C", 1, 1)])
        s0 = draw([P, P])
        self.play(FadeIn(title), FadeIn(s0), run_time=1.0)
        c1, an = cap(r"a pair of the 2nd kind: $b \dots b$, not adjacent")
        self.play(*an, Transform(s0, draw([P, P], bold=("b",))), run_time=1.0)

        P1 = _poly([V[1], V[2], V[3]], [("b", "b", 1, 1), ("B", "B", 1, 1), ("a", "a", 1, 1)])
        P2 = _poly([V[3], V[4], V[0], V[1]], [("b", "b", 1, 1), ("C", "C", 1, 1), ("A", "A", 1, 1), ("a", "a", 1, 1)])
        cut = DashedLine(np.array([*V[1], 0]), np.array([*V[3], 0]), color=COL["a"], stroke_width=5, dash_length=0.14)
        alab = MathTex("a", color=COL["a"]).scale(0.7).move_to((np.array([*V[1], 0.0]) + np.array([*V[3], 0.0])) / 2 + RIGHT * 0.35)
        c2, an = cap(r"cut along $a$, from the start of one $b$ to the start of the other", c1)
        self.play(*an, Create(cut), FadeIn(alab), run_time=1.2)
        self.play(FadeOut(cut), FadeOut(alab), Transform(s0, draw([P1, P2], bold=("a",))), run_time=0.8)
        self.play(Transform(s0, draw([shift(P1, 1.6, 0.6), shift(P2, -1.2, -0.5)], bold=("b",))), run_time=1.2)

        # glue along b: move P2 by the isometry taking its b edge (V3->V4) onto P1's b (V1->V2)
        T = reflect_map(V[3], V[4], V[1], V[2])
        c3, an = cap(r"glue the two $b$ edges", c2)
        self.play(*an, Transform(s0, draw([P1, T(P2)], bold=("b",))), run_time=1.8)
        glued1 = [dict(e, hidden=(e["tex"] == "b")) for e in P1]
        glued2 = [dict(e, hidden=(e["tex"] == "b")) for e in T(P2)]
        self.play(Transform(s0, draw([glued1, glued2], bold=("a",))), run_time=1.0)

        W = [np.array(v) for v in [(-2.0, -1.3), (2.0, -1.3), (1.3, 1.5), (-1.3, 1.5), (-2.3, 0.2)]]
        res = _poly(W, [("A", "A", 1, 1), ("a", "a", 1, 1), ("a", "a", 1, 1), ("B", "B^{-1}", 1, 1), ("C", "C", 1, 1)])
        empty = [dict(e, hidden=True) for e in res]
        c4, an = cap(r"the pair $a\,a$ is now adjacent: $A\,B^{-1}\,a\,a\,C$", c3)
        self.play(*an, Transform(s0, draw([res, empty])), run_time=1.8)
        self.wait(1.4)
        self.play(FadeOut(c4))

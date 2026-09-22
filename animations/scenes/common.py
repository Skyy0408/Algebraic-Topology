"""Shared framework for gluing animations.

Layout: left half = the polygon with edge identifications (fixed in frame);
right half = the 3D sheet being glued.  Edges share colours between the two sides,
and the edges being glued are drawn bold on the left while the gluing happens.
"""
from manim import *
import numpy as np

EDGE_COLORS = {"a": BLUE_C, "b": ORANGE, "c": GREEN_C, "d": PURPLE_B, None: GREY_B}
LEFT_X, RIGHT_X = -3.6, 3.6
THIN, BOLD = 5, 11


def screen_right(theta):
    """World vector that projects to screen-right for a ThreeDScene camera at azimuth theta."""
    return np.array([-np.sin(theta), np.cos(theta), 0.0])


def _chevrons(mid, d, n, color, size=0.18):
    nrm = np.array([-d[1], d[0], 0.0])
    grp = VGroup()
    for k in range(n):
        c = mid + d * (k - (n - 1) / 2) * size * 1.1
        tip = c + d * size / 2
        grp.add(VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
            [tip - d * size + nrm * size * 0.6, tip, tip - d * size - nrm * size * 0.6]))
    return grp


def labelled_polygon(sides, verts=None, angles=None, radius=1.4, center=LEFT_X * RIGHT):
    """Polygon whose side k runs from vertex k to vertex k+1 (counter-clockwise).

    sides[k] = (name, n_arrows, sign): sign=+1 if the arrow points along the CCW
    traversal, -1 otherwise; name=None for a free (unidentified) edge.
    Either straight (`verts`) or curved on a circle (`angles` in degrees).
    Returns (group, {name: [edge mobjects]}, word_tex or None).
    """
    if angles is not None:
        A = [np.deg2rad(a) for a in angles]
        V = [radius * np.array([np.cos(a), np.sin(a), 0.0]) for a in A]
        fill = Circle(radius=radius, stroke_width=0, fill_color=GREY_E, fill_opacity=0.6)
    else:
        V = [np.array([*v, 0.0]) for v in verts]
        fill = Polygon(*V, stroke_width=0, fill_color=GREY_E, fill_opacity=0.6)
    n = len(V)
    grp = VGroup(fill)
    lines, word = {}, []
    for k, (name, n_arr, sign) in enumerate(sides):
        if angles is not None:
            a0, a1 = A[k], A[(k + 1) % n]
            if a1 <= a0:
                a1 += TAU
            ts = np.linspace(a0, a1, 60)
            pts = [radius * np.array([np.cos(t), np.sin(t), 0.0]) for t in ts]
        else:
            pts = [V[k], V[(k + 1) % n]]
        col = EDGE_COLORS[name]
        edge = VMobject(stroke_color=col, stroke_width=THIN if name else 3).set_points_as_corners(pts)
        grp.add(edge)
        if name is None:
            word = None if word is None else None
            continue
        lines.setdefault(name, []).append(edge)
        m = len(pts) // 2
        p, q = (pts[m - 1], pts[m]) if len(pts) > 2 else (pts[0], pts[1])
        d = (q - p) / np.linalg.norm(q - p) * sign
        mid = (pts[m - 1] + pts[m]) / 2 if len(pts) > 2 else (pts[0] + pts[1]) / 2
        grp.add(_chevrons(mid, d, n_arr, col))
        out = mid / np.linalg.norm(mid) if angles is not None else mid - sum(V) / n
        out = out / np.linalg.norm(out)
        grp.add(MathTex(name, color=col).scale(0.8).move_to(mid + out * 0.38))
        if word is not None:
            word.append(name if sign > 0 else name + "^{-1}")
    free = any(s[0] is None for s in sides)
    tex = None if free else " ".join(word)
    return grp.move_to(center), lines, tex


class GluingScene(ThreeDScene):
    """Subclass and set the class attributes below, then implement point()."""
    TITLE = ""                 # TeX for the title above the polygon
    SIDES = []                 # see labelled_polygon
    VERTS = None               # straight polygon vertices ...
    ANGLES = None              # ... or vertex angles on a circle
    STAGES = []                # [(caption, edge name to highlight or None, tracker index)]
    EDGES3D = []               # [(name, w -> (u, v))] boundary curves drawn on the sheet
    RES = (32, 16)
    PHI, THETA = 62, -60       # camera, degrees
    RUN = 3.0                  # seconds per stage
    SPIN = 4.0                 # seconds of rotation at the end

    def point(self, u, v, s):  # s = list of tracker values in [0, 1]
        raise NotImplementedError

    def scale(self, s):
        return 1.0

    def construct(self):
        theta = self.THETA * DEGREES
        self.set_camera_orientation(phi=self.PHI * DEGREES, theta=theta)
        off = RIGHT_X * screen_right(theta)

        poly, lines, word = labelled_polygon(self.SIDES, self.VERTS, self.ANGLES)
        left = [poly]
        if self.TITLE:
            left.append(MathTex(self.TITLE).scale(0.9).next_to(poly, UP, buff=0.5))
        if word:
            left.append(MathTex(word).scale(0.8).next_to(poly, DOWN, buff=0.5))
        self.add_fixed_in_frame_mobjects(*left)
        self.play(*[FadeIn(m) for m in left])

        trk = [ValueTracker(0.0) for _ in range(max(i for *_, i in self.STAGES) + 1)]
        vals = lambda: [t.get_value() for t in trk]

        spin = ValueTracker(0.0)          # final turntable rotation about the object's own vertical axis

        def place(P):
            s = vals()
            c, n = np.cos(spin.get_value()), np.sin(spin.get_value())
            x, y, z = self.scale(s) * np.asarray(P)
            return np.array([c * x - n * y, n * x + c * y, z]) + off

        surf = always_redraw(lambda: Surface(
            lambda u, v: place(self.point(u, v, vals())),
            u_range=[0, 1], v_range=[0, 1], resolution=self.RES,
            fill_color=GREY_B, fill_opacity=0.55, stroke_width=0.3,
            stroke_color=GREY_D, checkerboard_colors=False))

        def curve(name, fn):
            return always_redraw(lambda: ParametricFunction(
                lambda w: place(self.point(*fn(w), vals())), t_range=[0, 1, 0.01],
                color=EDGE_COLORS[name], stroke_width=6 if name else 3))

        edges3d = [curve(n, f) for n, f in self.EDGES3D]
        self.play(FadeIn(surf), *[Create(e) for e in edges3d])
        self.wait(0.5)

        cap = None
        for caption, name, i in self.STAGES:
            new = Text(caption, font_size=28, color=EDGE_COLORS.get(name, WHITE)).to_corner(UR)
            self.add_fixed_in_frame_mobjects(new)
            anims = [FadeIn(new), trk[i].animate.set_value(1.0)]
            if cap:
                anims.append(FadeOut(cap))
            bold = lines.get(name, [])
            if bold:
                self.play(*[l.animate.set_stroke(width=BOLD) for l in bold], run_time=0.4)
            self.play(*anims, run_time=self.RUN, rate_func=smooth)
            if bold:
                self.play(*[l.animate.set_stroke(width=THIN) for l in bold], run_time=0.4)
            self.wait(0.3)
            cap = new
        if cap:
            self.play(FadeOut(cap))
        self.play(spin.animate.set_value(0.35 * self.SPIN), run_time=self.SPIN, rate_func=linear)

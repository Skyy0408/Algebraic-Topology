"""Chapter 1: connected sums (OpenGL renderer, GPU).

Render on the workstation:
    python tools/manim_gl.py --renderer=opengl --write_to_movie -qh ch01_connected_sum.py TorusSumTorus
(tools/manim_gl.py forces a headless EGL context; plain `manim --renderer=opengl` works on a desktop.)

Left : polygons - cut a disk at a vertex (new edge c), glue the two polygons along c.
Right: surfaces - remove disks D1, D2, glue the boundary circles (via a collar tube).
"""
from manim import *
from manim.mobject.opengl.opengl_surface import OpenGLSurface
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
import numpy as np

COL = {"a": BLUE_C, "b": ORANGE, "a_1": BLUE_C, "b_1": ORANGE, "a_2": PURPLE_B, "b_2": GOLD,
       "c": GREEN_C, "d": PINK}
DISK_COL, CUT_COL = RED_C, GREEN_C
THIN, BOLD = 4, 9
N = 24                                   # samples per polygon edge
LEFT_C = np.array([-3.6, -0.3, 0.0])     # centre of the left panel
RIGHT_X = 3.5
DOWN_W = np.array([0.0, 0.0, -1.0])
SURF = dict(color=GREY_B, opacity=0.85, gloss=0.25, shadow=0.35)


# ------------------------------------------------------------------ 2D polygons
def fix(m):
    for x in m.get_family():
        x.fix_in_frame()
    return m


def seg(p, q):
    p, q = np.array([*p, 0.0]), np.array([*q, 0.0])
    return np.array([p + (q - p) * t for t in np.linspace(0, 1, N)])


def arc(c, R, a0, a1):
    ts = np.deg2rad(np.linspace(a0, a1, N))
    return np.array([[c[0] + R * np.cos(t), c[1] + R * np.sin(t), 0.0] for t in ts])


def rot(pts, deg, about=(0, 0)):
    a = np.deg2rad(deg)
    M = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    o = np.array([*about, 0.0])
    return (pts - o) @ M.T + o


def E(pts, name, tex, n=1, sign=1, poly=0, hidden=False):
    return dict(pts=pts, name=name, tex=tex, n=n, sign=sign, poly=poly, hidden=hidden)


def _chevrons(mid, d, n, col, size=0.16):
    nrm = np.array([-d[1], d[0], 0.0])
    g = VGroup()
    for k in range(n):
        c = mid + d * (k - (n - 1) / 2) * size * 1.1
        tip = c + d * size / 2
        g.add(OpenGLVMobject().set_points_as_corners(
            [tip - d * size + nrm * size * 0.6, tip, tip - d * size - nrm * size * 0.6]).set_stroke(col, 4))
    return g


def draw(edges, bold=()):
    """Polygon(s) with fill, coloured edges, arrows and labels. Structure is identical for
    every stage built from the same edge list, so Transform morphs stage -> stage."""
    polys = {}
    for e in edges:
        polys.setdefault(e["poly"], []).append(e["pts"])
    cents = {k: np.concatenate(v).mean(0) for k, v in polys.items()}
    g = VGroup()
    for k in sorted(polys):
        loop = np.concatenate(polys[k]) + LEFT_C
        g.add(OpenGLVMobject().set_points_as_corners(loop).set_fill(GREY_E, 0.7).set_stroke(width=0))
    for e in edges:
        pts, col = e["pts"], COL[e["name"]]
        op = 0.0 if e["hidden"] else 1.0
        w = BOLD if e["name"] in bold else THIN
        line = OpenGLVMobject().set_points_as_corners(pts + LEFT_C).set_stroke(col, w, opacity=op)
        m = N // 2
        d = pts[m] - pts[m - 1]
        L = np.linalg.norm(d)
        d = d / L if L > 1e-9 else RIGHT
        mid = (pts[m] + pts[m - 1]) / 2
        ch = _chevrons(mid + LEFT_C, d * e["sign"], e["n"], col).set_stroke(opacity=op)
        nrm = np.array([d[1], -d[0], 0.0])
        if np.dot(nrm, mid - cents[e["poly"]]) < 0:
            nrm = -nrm
        lab = MathTex(e["tex"], color=col).scale(0.7).move_to(mid + LEFT_C + nrm * 0.32)
        if op == 0.0:
            lab.set_fill(opacity=0).set_stroke(opacity=0).scale(0.02)
            ch.scale(0.02)
        g.add(VGroup(line, ch, lab))
    return fix(g)


# ------------------------------------------------------------------ 3D pieces
def torus_pt(u, v, R, r):
    return np.array([(R + r * np.cos(v)) * np.cos(u), (R + r * np.cos(v)) * np.sin(u), r * np.sin(v)])


def sq2disk(x, y):
    """Smooth map [-1,1]^2 -> closed unit disk (boundary -> circle); avoids the polar singularity."""
    return x * np.sqrt(1 - y * y / 2), y * np.sqrt(1 - x * x / 2)


def square_ray(th, L):
    return L / max(abs(np.cos(th)), abs(np.sin(th)))


class Holed:
    """Torus (R, r) centred at c with a disk of radius rho removed around (u0, v0).
    Local coordinates near the hole: sigma = (u-u0)(R + r cos v0), tau = (v-v0) r."""

    def __init__(self, c, u0, v0=0.5, R=1.0, r=0.45, rho=0.32, L=0.6):
        self.c, self.u0, self.v0 = np.array(c, float), u0, v0
        self.R, self.r, self.rho, self.L = R, r, rho, L
        self.su = R + r * np.cos(v0)

    def at(self, sg, ta):
        return self.c + torus_pt(self.u0 + sg / self.su, self.v0 + ta / self.r, self.R, self.r)

    def hole(self, th):                       # boundary circle of the removed disk
        return self.at(self.rho * np.cos(th), self.rho * np.sin(th))

    def frame(self):                          # centre, u-tangent, v-tangent, outward normal at the hole
        h = 1e-4
        p = self.at(0, 0)
        tu = (self.at(h, 0) - p) / h
        tv = (self.at(0, h) - p) / h
        n = p - (self.c + self.R * np.array([np.cos(self.u0), np.sin(self.u0), 0.0]))
        return p, tu / np.linalg.norm(tu), tv / np.linalg.norm(tv), n / np.linalg.norm(n)

    def patches(self, W):
        R, r, u0, v0, L, rho = self.R, self.r, self.u0, self.v0, self.L, self.rho
        du = L / self.su
        return [
            OpenGLSurface(lambda u, v: W(self.c + torus_pt(u, v, R, r)),
                          u_range=[u0 + du, u0 + TAU - du], v_range=[v0 - PI, v0 + PI], resolution=(48, 24), **SURF),
            OpenGLSurface(lambda u, v: W(self.c + torus_pt(u, v, R, r)),
                          u_range=[u0 - du, u0 + du], v_range=[v0 + L / r, v0 + TAU - L / r], resolution=(6, 20), **SURF),
            OpenGLSurface(lambda s_, th: W(self.at(*((rho + s_ * (square_ray(th, L) - rho)) * np.array([np.cos(th), np.sin(th)])))),
                          u_range=[0, 1], v_range=[0, TAU], resolution=(6, 40), **SURF),
        ]

    def disk(self, W, color=DISK_COL, opacity=0.95):
        return OpenGLSurface(lambda x, y: W(self.at(*(self.rho * np.array(sq2disk(x, y))))),
                             u_range=[-1, 1], v_range=[-1, 1], resolution=(12, 12),
                             color=color, opacity=opacity, gloss=0.2, shadow=0.3)


def mesh(surfs, every=4):
    """Faint grid lines on OpenGLSurfaces (every k-th sample row / column), nudged along the normal."""
    g = VGroup()
    for srf in surfs:
        nu, nv = srf.resolution
        P = srf.get_surface_points_and_nudged_points()[0] + 0.01 * srf.get_unit_normals()
        P = P.reshape(nu, nv, 3)
        for i in list(range(0, nu, every)) + [nu - 1]:
            g.add(OpenGLVMobject().set_points_as_corners(P[i]))
        for j in list(range(0, nv, every)) + [nv - 1]:
            g.add(OpenGLVMobject().set_points_as_corners(P[:, j]))
    return g.set_stroke(GREY_D, 0.8)


def curve(fn, color=CUT_COL, width=5):
    return ParametricFunction(fn, t_range=[0, TAU, TAU / 64], color=color, stroke_width=width)


def tube(A, B, w0, w1, W):
    """Collar between boundary curves A(th) (w=0) and B(th) (w=1); drawn for w in [w0, w1]."""
    w1 = max(w1, w0 + 1e-3)
    return OpenGLSurface(lambda w, th: W((1 - w) * A(th) + w * B(th)), u_range=[w0, w1],
                         v_range=[0, TAU], resolution=(8, 40), **SURF)


# ------------------------------------------------------------------ base scene
class SumScene(ThreeDScene):
    TITLE = ""
    PHI, THETA, K = 66, 10, 0.68          # OpenGL convention: theta_gl = theta_cairo + 90

    def setup_3d(self):
        self.set_camera_orientation(phi=self.PHI * DEGREES, theta=self.THETA * DEGREES)
        M = np.array(self.renderer.camera.inverse_rotation_matrix)   # world -> camera
        self.off = RIGHT_X * M[0] + DOWN_W * 0.0                   # M[0] = world direction of screen-right
        self.W = lambda p: self.K * np.asarray(p) + self.off
        self.cap = None

    def caption(self, tex):
        new = fix(Tex(tex, font_size=34).to_corner(UR, buff=0.4))
        anims = [FadeIn(new)]
        if self.cap is not None:
            anims.append(FadeOut(self.cap))
        self.cap = new
        return anims

    def title(self):
        t = fix(MathTex(self.TITLE).scale(0.95).move_to(LEFT_C + UP * 2.9))
        return t

    def spin(self, grp, seconds=5.0):
        self.play(Rotate(grp, angle=0.22 * seconds, axis=OUT, about_point=self.off),
                  *( [FadeOut(self.cap)] if self.cap else [] ), run_time=seconds, rate_func=linear)


# ------------------------------------------------------------------ T^2 # T^2
def _square_cut(side, eps, names, sign_poly, rot_deg=0, shift=(0, 0), poly=0):
    """Square with the standard torus word, a disk of radius eps cut at its bottom-left corner.
    Edge order: a (P->BR), b, a^-1, b^-1 (TL->Q), c (Q->P along the arc)."""
    a, b = names
    h = side / 2
    BL, BR, TR, TL = np.array([-h, -h]), np.array([h, -h]), np.array([h, h]), np.array([-h, h])
    P, Q = BL + [eps, 0], BL + [0, eps]
    c = arc(BL, eps, 90, 0) if eps > 0 else seg(BL, BL)
    raw = [(seg(P, BR), a, 1, 1), (seg(BR, TR), b, 2, 1), (seg(TR, TL), a, 1, -1),
           (seg(TL, Q), b, 2, -1), (c, "c", 1, sign_poly)]
    out = []
    for pts, nm, n, sg in raw:
        pts = rot(pts, rot_deg) + np.array([*shift, 0.0])
        out.append(E(pts, nm, nm, n, sg, poly, hidden=(nm == "c" and eps == 0)))
    return out


def _octagon_half(which, radius=1.75):
    V = [radius * np.array([np.cos(np.deg2rad(270 + 45 * k)), np.sin(np.deg2rad(270 + 45 * k))]) for k in range(8)]
    if which == 0:   # V0..V4 : a1 b1 a1^-1 b1^-1, c = V4 -> V0
        idx, names, sgc = [0, 1, 2, 3, 4], ("a_1", "b_1"), 1
    else:            # V4..V7,V0 : a2 b2 a2^-1 b2^-1, c = V0 -> V4 (arrow reversed)
        idx, names, sgc = [4, 5, 6, 7, 0], ("a_2", "b_2"), -1
    a, b = names
    P = [V[i] for i in idx]
    raw = [(seg(P[0], P[1]), a, 1, 1), (seg(P[1], P[2]), b, 2, 1), (seg(P[2], P[3]), a, 1, -1),
           (seg(P[3], P[4]), b, 2, -1), (seg(P[4], P[0]), "c", 1, sgc)]
    return [E(pts, nm, nm, n, sg, which) for pts, nm, n, sg in raw]


class TorusSumTorus(SumScene):
    TITLE = r"T^2 \# T^2"
    K = 0.8

    def stage(self, k):
        if k <= 1:
            eps = 0.0 if k == 0 else 0.45
            A = _square_cut(1.8, eps, ("a_1", "b_1"), 1, rot_deg=0, shift=(1.35, 0), poly=0)
            B = _square_cut(1.8, eps, ("a_2", "b_2"), -1, rot_deg=180, shift=(-1.35, 0), poly=1)
            return A + B
        edges = _octagon_half(0) + _octagon_half(1)
        if k == 3:
            for e in edges:
                e["hidden"] = e["name"] == "c"
        return edges

    def construct(self):
        self.setup_3d()
        W = self.W
        gap = ValueTracker(1.9)          # distance between the two tori centres is 2*(R+r) + gap
        R, r, rho = 1.0, 0.45, 0.32
        TW = 0.35                        # holes turned towards the camera
        cx = lambda: R + r + gap.get_value() / 2
        TL = Holed((-cx(), 0, 0), -TW, 0.5, R, r, rho)
        TR = Holed((cx(), 0, 0), PI + TW, 0.5, R, r, rho)
        left_s, right_s = TL.patches(W), TR.patches(W)
        torL = Group(*left_s, mesh(left_s))
        torR = Group(*right_s, mesh(right_s))
        dL, dR = TL.disk(W), TR.disk(W)

        # ---- intro
        poly = draw(self.stage(0))
        word = fix(MathTex(r"a_1b_1a_1^{-1}b_1^{-1}", r"\qquad", r"a_2b_2a_2^{-1}b_2^{-1}")
                   .scale(0.7).move_to(LEFT_C + DOWN * 2.45))
        # red sectors: the disks cut at the chosen corner of each square
        corA = np.array([-0.9 + 1.35, -0.9, 0]) + LEFT_C      # A: bottom-left corner, interior up-right
        corB = np.array([0.9 - 1.35, 0.9, 0]) + LEFT_C        # B (rotated 180): top-right, interior down-left
        secA = fix(AnnularSector(0, 0.45, PI / 2, 0, color=DISK_COL, fill_opacity=0.8, stroke_width=0).shift(corA))
        secB = fix(AnnularSector(0, 0.45, PI / 2, PI, color=DISK_COL, fill_opacity=0.8, stroke_width=0).shift(corB))
        greyL, greyR = TL.disk(W, GREY_B, SURF["opacity"]), TR.disk(W, GREY_B, SURF["opacity"])
        self.play(FadeIn(self.title()), FadeIn(poly), FadeIn(word), FadeIn(torL), FadeIn(torR),
                  FadeIn(greyL), FadeIn(greyR), run_time=1.2)

        # ---- remove the disks
        self.play(*self.caption(r"remove disks $D_1, D_2$"), FadeIn(dL), FadeIn(dR),
                  FadeIn(secA), FadeIn(secB), run_time=1.0)
        self.remove(greyL, greyR)
        hL, hR = curve(lambda t: W(TL.hole(t))), curve(lambda t: W(TR.hole(PI - t)))
        self.play(FadeOut(dL), FadeOut(dR), FadeOut(secA), FadeOut(secB),
                  Create(hL), Create(hR), Transform(poly, draw(self.stage(1))), run_time=1.8)
        self.wait(0.4)

        # ---- glue the boundary circles
        g = ValueTracker(0.0)
        A = lambda th: TL.hole(th)
        B = lambda th: TR.hole(PI - th)
        t1 = always_redraw(lambda: tube(A, B, 0, g.get_value() / 2, W))
        t2 = always_redraw(lambda: tube(A, B, 1 - g.get_value() / 2, 1, W))
        e1 = always_redraw(lambda: curve(lambda t: W((1 - g.get_value() / 2) * A(t) + g.get_value() / 2 * B(t))))
        e2 = always_redraw(lambda: curve(lambda t: W(g.get_value() / 2 * A(t) + (1 - g.get_value() / 2) * B(t))))
        self.add(t1, t2)
        self.remove(hL, hR)
        self.add(e1, e2)
        self.play(*self.caption(r"glue $\partial D_1 \to \partial D_2$ by $h$"),
                  Transform(poly, draw(self.stage(1), bold=("c",))), run_time=0.5)
        self.play(g.animate.set_value(1.0), Transform(poly, draw(self.stage(2), bold=("c",))),
                  run_time=3.0, rate_func=smooth)
        for m in (t1, t2, e1, e2):
            m.clear_updaters()
        seam = e1
        self.remove(e2)

        # ---- the result
        word2 = fix(MathTex(r"a_1b_1a_1^{-1}b_1^{-1}a_2b_2a_2^{-1}b_2^{-1}").scale(0.7).move_to(word))
        start = gap.get_value()

        def slide(sign):
            def upd(m):
                m.shift(sign * self.K * (m.last - gap.get_value()) / 2 * RIGHT)
                m.last = gap.get_value()
            return upd
        tube_all = always_redraw(lambda: tube(lambda th: Holed((-cx(), 0, 0), -TW, 0.5, R, r, rho).hole(th),
                                              lambda th: Holed((cx(), 0, 0), PI + TW, 0.5, R, r, rho).hole(PI - th), 0, 1, W))
        self.remove(t1, t2)
        self.add(tube_all)
        for m, s in ((torL, 1), (torR, -1)):
            m.last = start
            m.add_updater(slide(s))
        self.play(*self.caption(r"$T^2 \# T^2$: genus $2$"), FadeOut(seam),
                  Transform(poly, draw(self.stage(3))), FadeOut(word), FadeIn(word2),
                  gap.animate.set_value(0.25), run_time=2.5, rate_func=smooth)
        for m in (torL, torR, tube_all):
            m.clear_updaters()
        self.wait(0.3)
        self.spin(Group(torL, torR, tube_all), 5.0)


# ------------------------------------------------------------------ S^2 # T^2 = T^2
def _sphere_torus_stage(k):
    H = [(-0.9, -1.2), (1.5, -1.2), (1.5, 1.2), (-0.9, 1.2), (-1.9, 0.5), (-1.9, -0.6)]
    H = [np.array(h) for h in H]
    if k <= 1:
        eps, dl = (0.0, 0.0) if k == 0 else (0.45, 28.0)
        BL, BR, TR, TL = np.array([0.3, -1.0]), np.array([2.3, -1.0]), np.array([2.3, 1.0]), np.array([0.3, 1.0])
        P, Q = BL + [eps, 0], BL + [0, eps]
        cT = arc(BL, eps, 90, 0) if eps > 0 else seg(BL, BL)
        cen, Rb = np.array([-1.7, 0.0]), 1.0
        pol = lambda a: cen + Rb * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a))])
        Qs, Ps = pol(dl), pol(360 - dl)
        T = [(seg(P, BR), "a", 1, 1), (seg(BR, TR), "b", 2, 1), (seg(TR, TL), "a", 1, -1),
             (seg(TL, Q), "b", 2, -1), (cT, "c", 1, 1)]
        S = [(arc(cen, Rb, dl, 180), "d", 1, 1), (arc(cen, Rb, 180, 360 - dl), "d", 1, -1), (seg(Ps, Qs), "c", 1, -1)]
    else:
        h4 = H[0] if k >= 4 else H[4]
        h5 = H[0] if k >= 5 else H[5]
        T = [(seg(H[0], H[1]), "a", 1, 1), (seg(H[1], H[2]), "b", 2, 1), (seg(H[2], H[3]), "a", 1, -1),
             (seg(H[3], h4), "b", 2, -1), (seg(h4, H[0]), "c", 1, 1)]
        S = [(seg(h4, h5), "d", 1, 1), (seg(h5, H[0]), "d", 1, -1), (seg(H[0], h4), "c", 1, -1)]
    out = [E(p_, nm, nm, n, sg, 0) for p_, nm, n, sg in T] + [E(p_, nm, nm, n, sg, 1) for p_, nm, n, sg in S]
    for e in out:
        if e["name"] == "c":
            e["hidden"] = (k == 0) or (k >= 3)
        if e["name"] == "d" and k >= 5:
            e["hidden"] = True
    return out


class SphereSumTorus(SumScene):
    TITLE = r"S^2 \# T^2 \cong T^2"
    K = 0.74

    def construct(self):
        self.setup_3d()
        W = self.W
        R, r, rho = 1.0, 0.45, 0.32
        T = Holed((1.4, 0, -0.3), PI + 0.35, 0.5, R, r, rho)
        Hc, tu, tv, nout = T.frame()
        nin = -nout                                   # from the sphere towards the hole
        e1 = -tu - np.dot(-tu, nin) * nin
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(nin, e1)
        if np.dot(e2, tv) < 0:
            e2 = -e2
        Rs0, dist0 = 1.0, 2.3
        Bc0 = Hc + nout * (dist0 - Rs0)               # centre of the sphere's boundary circle (approx.)

        def sphere_state(m, f):
            Rs = Rs0 + (rho - Rs0) * m
            ca0 = np.sqrt(max(1 - (rho / Rs) ** 2, 0.0))
            Bc = Bc0 + (Hc - Bc0) * m
            Cs = Bc - Rs * ca0 * nin
            a0 = np.arccos(ca0)
            return Rs, Cs, Bc, a0

        def sph_at(q, cph, sph, m, f):        # q in [0,1] from the pole (q=0) to the boundary circle (q=1)
            Rs, Cs, Bc, a0 = sphere_state(m, f)
            al = PI - q * (PI - a0)
            p = Cs + Rs * (np.cos(al) * nin + np.sin(al) * (cph * e1 + sph * e2))
            return p - f * np.dot(p - Bc, nin) * nin

        def sph_pt(x, y, m, f):
            X, Y = sq2disk(x, y)
            q = np.hypot(X, Y)
            if q < 1e-9:
                return sph_at(0.0, 1.0, 0.0, m, f)
            return sph_at(q, X / q, Y / q, m, f)

        def sph_edge(th, m, f):
            return sph_at(1.0, np.cos(th), np.sin(th), m, f)

        def sph_disk_pt(x, y):
            Rs, Cs, Bc, a0 = sphere_state(0, 0)
            X, Y = sq2disk(x, y)
            q = np.hypot(X, Y)
            al = q * a0
            d = (X * e1 + Y * e2) / q if q > 1e-9 else e1 * 0
            return Cs + Rs * (np.cos(al) * nin + np.sin(al) * d)

        def sphere(m=0.0, f=0.0):
            srf = OpenGLSurface(lambda x, y: W(sph_pt(x, y, m, f)), u_range=[-1, 1], v_range=[-1, 1],
                                resolution=(28, 28), **SURF)
            return Group(srf, mesh([srf]))

        A = lambda th, m=0.0, f=0.0: sph_edge(th, m, f)        # sphere boundary circle
        B = lambda th: T.hole(PI - th)                        # torus boundary circle
        tor = T.patches(W)
        torG = Group(*tor, mesh(tor))
        sph = sphere()
        greyT, greyS = T.disk(W, GREY_B, SURF["opacity"]), OpenGLSurface(
            lambda x, y: W(sph_disk_pt(x, y)), u_range=[-1, 1], v_range=[-1, 1], resolution=(12, 12), **SURF)
        redT, redS = T.disk(W), OpenGLSurface(lambda x, y: W(sph_disk_pt(x, y)), u_range=[-1, 1],
                                                v_range=[-1, 1], resolution=(12, 12), color=DISK_COL, opacity=0.95)

        poly = draw(_sphere_torus_stage(0))
        word = fix(MathTex(r"dd^{-1}", r"\qquad", r"aba^{-1}b^{-1}").scale(0.7).move_to(LEFT_C + DOWN * 2.45))
        secT = fix(AnnularSector(0, 0.45, PI / 2, 0, color=DISK_COL, fill_opacity=0.8, stroke_width=0)
                   .shift(np.array([0.3, -1.0, 0]) + LEFT_C))
        secS = fix(AnnularSector(0, 0.35, PI, PI / 2, color=DISK_COL, fill_opacity=0.8, stroke_width=0)
                   .shift(np.array([-0.7, 0.0, 0]) + LEFT_C))
        self.play(FadeIn(self.title()), FadeIn(poly), FadeIn(word), FadeIn(torG), FadeIn(sph),
                  FadeIn(greyT), FadeIn(greyS), run_time=1.2)

        # remove disks
        self.play(*self.caption(r"remove disks $D_1, D_2$"), FadeIn(redT), FadeIn(redS),
                  FadeIn(secT), FadeIn(secS), run_time=1.0)
        self.remove(greyT, greyS)
        hA, hB = curve(lambda t: W(A(t))), curve(lambda t: W(B(t)))
        self.play(FadeOut(redT), FadeOut(redS), FadeOut(secT), FadeOut(secS), Create(hA), Create(hB),
                  Transform(poly, draw(_sphere_torus_stage(1))), run_time=1.8)

        # glue
        g = ValueTracker(0.0)
        t1 = always_redraw(lambda: tube(A, B, 0, g.get_value() / 2, W))
        t2 = always_redraw(lambda: tube(A, B, 1 - g.get_value() / 2, 1, W))
        c1 = always_redraw(lambda: curve(lambda t: W((1 - g.get_value() / 2) * A(t) + g.get_value() / 2 * B(t))))
        c2 = always_redraw(lambda: curve(lambda t: W(g.get_value() / 2 * A(t) + (1 - g.get_value() / 2) * B(t))))
        self.remove(hA, hB)
        self.add(t1, t2, c1, c2)
        self.play(*self.caption(r"glue $\partial D_1 \to \partial D_2$ by $h$"),
                  Transform(poly, draw(_sphere_torus_stage(1), bold=("c",))), run_time=0.5)
        self.play(g.animate.set_value(1.0), Transform(poly, draw(_sphere_torus_stage(2), bold=("c",))),
                  run_time=3.0, rate_func=smooth)
        for mo in (t1, t2, c1, c2):
            mo.clear_updaters()
        self.remove(t1, t2, c2)
        word2 = fix(MathTex(r"aba^{-1}b^{-1}dd^{-1}").scale(0.7).move_to(word))
        m_, f_ = ValueTracker(0.0), ValueTracker(0.0)
        sphR = always_redraw(lambda: sphere(m_.get_value(), f_.get_value()))
        tubR = always_redraw(lambda: tube(lambda th: A(th, m_.get_value(), f_.get_value()), B, 0, 1, W))
        self.remove(sph)
        self.add(sphR, tubR)
        self.play(FadeOut(c1), Transform(poly, draw(_sphere_torus_stage(3))), FadeOut(word), FadeIn(word2),
                  run_time=1.2)

        # absorb the sphere: S^2 minus a disk is a disk
        word3 = fix(MathTex(r"aba^{-1}b^{-1}").scale(0.7).move_to(word))
        self.play(*self.caption(r"$S^2 \setminus D$ is a disk: it caps the hole"),
                  m_.animate.set_value(1.0), Transform(poly, draw(_sphere_torus_stage(4))),
                  run_time=3.0, rate_func=smooth)
        self.play(f_.animate.set_value(1.0), Transform(poly, draw(_sphere_torus_stage(5))),
                  FadeOut(word2), FadeIn(word3), run_time=1.8, rate_func=smooth)
        for mo in (sphR, tubR):
            mo.clear_updaters()
        greyT2 = T.disk(W, GREY_B, SURF["opacity"])
        self.play(*self.caption(r"$S^2 \# T^2 \cong T^2$"), FadeIn(greyT2), FadeOut(sphR), FadeOut(tubR),
                  run_time=1.0)
        self.wait(0.3)
        self.spin(Group(torG, greyT2), 5.0)


# ------------------------------------------------------------------ RP^2 # RP^2 = K
def bend(x, dy, dz, s, R):
    if s < 1e-4:
        return np.array([x, dy, dz])
    Rb = R / s
    ph = x / Rb
    C = np.array([Rb * np.sin(ph), Rb * (1 - np.cos(ph)), 0.0])
    n = np.array([np.sin(ph), -np.cos(ph), 0.0])
    return C - dy * n + np.array([0.0, 0.0, dz]) - np.array([0.0, R * s, 0.0])


R_K, k_K = 1.5, 0.65


def klein8(u, v, lam):
    """Figure-8 Klein bottle; v in [-1/4, 1/4] and [1/4, 3/4] are two Mobius bands.
    lam = 0 flattens each cross-section to a segment (standard Mobius band)."""
    t = TAU * v
    cy, cz = k_K * np.sin(t), lam * k_K * np.sin(2 * t)
    al = PI * (u - 0.5)
    dy = cy * np.cos(al) - cz * np.sin(al)
    dz = cy * np.sin(al) + cz * np.cos(al)
    return bend(TAU * R_K * (u - 0.5), dy, dz, 1.0, R_K)


def _rp2_stage(k):
    W_ = [np.array(w) for w in [(-1.2, -1.2), (1.2, -1.2), (1.2, 1.2), (-1.2, 1.2)]]
    if k <= 1:
        dl = 0.0 if k == 0 else 28.0
        cA, cB, Rb = np.array([1.6, 0.0]), np.array([-1.6, 0.0]), 1.0
        pA = lambda a: cA + Rb * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a))])
        pB = lambda a: cB + Rb * np.array([np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a))])
        A = [(arc(cA, Rb, 180 + dl, 360), "a_1", 1, 1), (arc(cA, Rb, 0, 180 - dl), "a_1", 1, 1),
             (seg(pA(180 - dl), pA(180 + dl)), "c", 1, 1)]
        B = [(arc(cB, Rb, dl, 180), "a_2", 2, 1), (arc(cB, Rb, 180, 360 - dl), "a_2", 2, 1),
             (seg(pB(360 - dl), pB(dl)), "c", 1, -1)]
    else:
        A = [(seg(W_[0], W_[1]), "a_1", 1, 1), (seg(W_[1], W_[2]), "a_1", 1, 1), (seg(W_[2], W_[0]), "c", 1, 1)]
        B = [(seg(W_[2], W_[3]), "a_2", 2, 1), (seg(W_[3], W_[0]), "a_2", 2, 1), (seg(W_[0], W_[2]), "c", 1, -1)]
    out = [E(p_, nm, nm, n, sg, 0) for p_, nm, n, sg in A] + [E(p_, nm, nm, n, sg, 1) for p_, nm, n, sg in B]
    for e in out:
        if e["name"] == "c":
            e["hidden"] = (k == 0) or (k >= 3)
    return out


class ProjectivePlaneSum(SumScene):
    TITLE = r"\mathbb{RP}^2 \# \mathbb{RP}^2 \cong K"
    PHI, THETA, K = 66, 35, 0.8
    MB2_COL = "#8FA8C0"

    def construct(self):
        self.setup_3d()
        W = self.W
        lam, hgt = ValueTracker(0.0), ValueTracker(1.9)
        up = np.array([0.0, 0.0, 1.0])

        def band(v0, v1, lift, col):
            srf = OpenGLSurface(lambda u, v: W(klein8(u, v, lam.get_value()) + lift * up),
                                u_range=[0, 1], v_range=[v0, v1], resolution=(56, 12),
                                **{**SURF, "color": col})
            return Group(srf, mesh([srf], every=4))

        def edge(v, lift):
            return ParametricFunction(lambda u: W(klein8(u, v, lam.get_value()) + lift * up),
                                      t_range=[0, 1, 1 / 80], color=CUT_COL, stroke_width=5)

        mb1 = always_redraw(lambda: band(-0.25, 0.25, 0.0, GREY_B))
        mb2 = always_redraw(lambda: band(0.25, 0.75, hgt.get_value(), self.MB2_COL))
        b1 = always_redraw(lambda: VGroup(edge(0.25, 0.0), edge(-0.25, 0.0)))
        b2 = always_redraw(lambda: VGroup(edge(0.25, hgt.get_value()), edge(0.75, hgt.get_value())))

        poly = draw(_rp2_stage(0))
        word = fix(MathTex(r"a_2a_2", r"\qquad", r"a_1a_1").scale(0.7).move_to(LEFT_C + DOWN * 2.45))
        secA = fix(AnnularSector(0, 0.35, PI, -PI / 2, color=DISK_COL, fill_opacity=0.8, stroke_width=0)
                   .shift(np.array([0.6, 0.0, 0]) + LEFT_C))
        secB = fix(AnnularSector(0, 0.35, PI, PI / 2, color=DISK_COL, fill_opacity=0.8, stroke_width=0)
                   .shift(np.array([-0.6, 0.0, 0]) + LEFT_C))
        self.play(FadeIn(self.title()), FadeIn(poly), FadeIn(word), FadeIn(secA), FadeIn(secB), run_time=1.2)

        # RP^2 minus a disk is a Mobius band
        self.play(*self.caption(r"$\mathbb{RP}^2 \setminus D \cong$ M\"obius band"),
                  FadeOut(secA), FadeOut(secB), Transform(poly, draw(_rp2_stage(1))),
                  FadeIn(mb1), FadeIn(mb2), Create(b1), Create(b2), run_time=2.0)
        self.wait(0.5)

        # glue the two boundary circles
        self.play(*self.caption(r"glue $\partial D_1 \to \partial D_2$ by $h$"),
                  Transform(poly, draw(_rp2_stage(1), bold=("c",))), run_time=0.5)
        self.play(lam.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
        self.play(hgt.animate.set_value(0.0), Transform(poly, draw(_rp2_stage(2), bold=("c",))),
                  run_time=2.5, rate_func=smooth)
        for mo in (mb1, mb2, b1, b2):
            mo.clear_updaters()
        word2 = fix(MathTex(r"a_1a_1a_2a_2").scale(0.7).move_to(word))
        self.play(*self.caption(r"$K$ (passes through itself in $\mathbb{R}^3$)"), FadeOut(b1), FadeOut(b2),
                  Transform(poly, draw(_rp2_stage(3))), FadeOut(word), FadeIn(word2), run_time=1.2)
        self.wait(0.3)
        self.spin(Group(mb1, mb2), 5.0)

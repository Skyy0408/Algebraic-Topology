"""Chapter 1: gluing a polygon into a surface (left: polygon, right: 3D gluing)."""
from common import *

SQUARE = [(-1.3, -1.3), (1.3, -1.3), (1.3, 1.3), (-1.3, 1.3)]   # CCW from bottom-left


def bend(x, dy, dz, s, R):
    """Bend the x-axis into a circle of radius R (s=0 straight, s=1 closed).
    (dy, dz) is the offset from the axis; result centred at the origin."""
    if s < 1e-4:
        return np.array([x, dy, dz])
    Rb = R / s
    ph = x / Rb
    C = np.array([Rb * np.sin(ph), Rb * (1 - np.cos(ph)), 0.0])
    n = np.array([np.sin(ph), -np.cos(ph), 0.0])
    return C - dy * n + np.array([0.0, 0.0, dz]) - np.array([0.0, R * s, 0.0])


def roll(t, s, r):
    """Roll a segment coordinate t (length 2*pi*r) into a circle of radius r; axis at z = 0."""
    if s < 1e-4:
        return t, -r
    rho = r / s
    th = t / rho
    return rho * np.sin(th), rho * (1 - np.cos(th)) - r


# ---------------------------------------------------------------- cylinder, torus
R_T, r_T = 1.3, 0.5


def torus_point(u, v, s1, s2):
    y, z = roll(TAU * r_T * (v - 0.5), s1, r_T)
    return bend(TAU * R_T * (u - 0.5), y, z, s2, R_T)


class Cylinder(GluingScene):
    TITLE = r"\text{Cylinder}"
    VERTS = SQUARE
    SIDES = [("a", 1, 1), (None, 0, 0), ("a", 1, -1), (None, 0, 0)]
    STAGES = [("glue a", "a", 0)]
    EDGES3D = [("a", lambda w: (w, 0)), ("a", lambda w: (w, 1)),
               (None, lambda w: (0, w)), (None, lambda w: (1, w))]
    PHI, THETA = 65, -70

    def point(self, u, v, s):
        y, z = roll(TAU * 0.8 * (v - 0.5), s[0], 0.8)
        return np.array([4.0 * (u - 0.5), y, z])

    def scale(self, s):
        return 0.7


class Torus(GluingScene):
    TITLE = r"T^2 = [0,1]^2/\!\sim"
    VERTS = SQUARE
    SIDES = [("a", 1, 1), ("b", 2, 1), ("a", 1, -1), ("b", 2, -1)]
    STAGES = [("glue a", "a", 0), ("glue b", "b", 1)]
    EDGES3D = [("a", lambda w: (w, 0)), ("a", lambda w: (w, 1)),
               ("b", lambda w: (0, w)), ("b", lambda w: (1, w))]

    def point(self, u, v, s):
        return torus_point(u, v, s[0], s[1])

    def scale(self, s):
        return 0.5 + 0.5 * s[1]


# ---------------------------------------------------------------- Möbius band
R_M, W_M = 1.3, 1.4


class MobiusBand(GluingScene):
    TITLE = r"\text{M\"obius band}"
    VERTS = SQUARE
    SIDES = [(None, 0, 0), ("a", 1, -1), (None, 0, 0), ("a", 1, -1)]
    STAGES = [("glue a (with a half twist)", "a", 0)]
    EDGES3D = [("a", lambda w: (0, w)), ("a", lambda w: (1, w)),
               (None, lambda w: (w, 0)), (None, lambda w: (w, 1))]
    RES = (48, 8)

    def point(self, u, v, s):
        c = W_M * (v - 0.5)
        al = s[0] * PI * (u - 0.5)
        return bend(TAU * R_M * (u - 0.5), c * np.cos(al), c * np.sin(al), s[0], R_M)

    def scale(self, s):
        return 0.45 + 0.55 * s[0]


# ---------------------------------------------------------------- Klein bottle
R_K, k_K = 1.5, 0.65


class KleinBottle(GluingScene):
    TITLE = r"K"
    VERTS = SQUARE
    SIDES = [("a", 1, 1), ("b", 2, -1), ("a", 1, -1), ("b", 2, -1)]
    STAGES = [("glue a", "a", 0), ("glue b (reversed; passes through itself)", "b", 1)]
    EDGES3D = [("a", lambda w: (w, 0)), ("a", lambda w: (w, 1)),
               ("b", lambda w: (0, w)), ("b", lambda w: (1, w))]
    RES = (48, 24)
    PHI, THETA = 65, -55

    def point(self, u, v, s):
        t = TAU * v
        flat = np.array([TAU * k_K * (v - 0.5), 0.0])
        eight = k_K * np.array([np.sin(t), np.sin(2 * t)])     # figure-8 cross-section
        cy, cz = (1 - s[0]) * flat + s[0] * eight
        al = s[1] * PI * (u - 0.5)                              # half twist: v -> 1 - v
        dy = cy * np.cos(al) - cz * np.sin(al)
        dz = cy * np.sin(al) + cz * np.cos(al)
        return bend(TAU * R_K * (u - 0.5), dy, dz, s[1], R_K)

    def scale(self, s):
        return 0.45 + 0.55 * s[1]


# ---------------------------------------------------------------- S^2 = aa^{-1}
r_S = 1.3


class Sphere(GluingScene):
    TITLE = r"S^2"
    ANGLES = [90, 270]                      # vertices: north (top), south (bottom)
    SIDES = [("a", 1, 1), ("a", 1, -1)]     # both edges run north -> south
    STAGES = [("glue a", "a", 0)]
    EDGES3D = [("a", lambda w: (w, 0)), ("a", lambda w: (w, 1))]
    RES = (24, 32)
    PHI, THETA = 75, -75

    def point(self, u, v, s):
        s = max(s[0], 1e-3)
        be = PI * (u - 0.5)                 # latitude
        th = TAU * (v - 0.5) * s
        rho = r_S * np.cos(be) / s
        x = rho * np.sin(th)
        y = -(rho * (np.cos(th) - 1) + s * r_S * np.cos(be))   # seam ends up at the back
        z = (1 - s) * r_S * be + s * r_S * np.sin(be)
        return np.array([x, y, z])

    def scale(self, s):
        return 0.5 + 0.5 * s[0]


# ---------------------------------------------------------------- RP^2 = aa (cross-cap)
class ProjectivePlane(GluingScene):
    TITLE = r"\mathbb{RP}^2"
    ANGLES = [0, 180]
    SIDES = [("a", 1, 1), ("a", 1, 1)]      # antipodal identification
    STAGES = [("disk = closed hemisphere", None, 0),
              ("glue a: antipodal points (passes through itself)", "a", 1)]
    EDGES3D = [("a", lambda w: (1, w / 2)), ("a", lambda w: (1, 0.5 + w / 2))]
    RES = (16, 48)
    PHI, THETA = 65, -50

    def point(self, u, v, s):
        th = TAU * v
        flat = np.array([u * np.cos(th), u * np.sin(th), 0.0])
        ps = u * PI / 2
        hemi = np.array([np.sin(ps) * np.cos(th), np.sin(ps) * np.sin(th), np.cos(ps)])
        x, y, z = (1 - s[0]) * flat + s[0] * hemi
        cap = np.array([y * z, 2 * x * y, x * x - y * y])   # cross-cap, even in (x,y,z)
        return (1 - s[1]) * np.array([x, y, z]) + s[1] * cap

    def scale(self, s):
        return 1.5

"""Run manim with the OpenGL renderer on a headless EGL context on GPU $MANIM_GPU (default 2)."""
import os, sys, moderngl
GPU = int(os.environ.get("MANIM_GPU", "2"))
_sa, _cc = moderngl.create_standalone_context, moderngl.create_context
def _egl_sa(*a, **k):
    k.setdefault("backend", "egl"); k.setdefault("device_index", GPU); return _sa(*a, **k)
def _egl_cc(*a, **k):
    if k.get("standalone"):
        k.setdefault("backend", "egl"); k.setdefault("device_index", GPU)
    return _cc(*a, **k)
moderngl.create_standalone_context, moderngl.create_context = _egl_sa, _egl_cc
from manim.__main__ import main
sys.exit(main())

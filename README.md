# Algebraic-Topology

Notes of a course in NTHU, 2026 Fall.

Site: https://skyy0408.github.io/Algebraic-Topology/

代數拓樸課堂筆記（主教材：W. S. Massey, *A Basic Course in Algebraic Topology*, GTM 127）。

## 結構

```
docs/                    網站內容（MkDocs）；各章筆記 docs/chXX-*.md
docs/assets/animations/  渲染好的動畫（MP4）
docs/assets/figures/     靜態圖
animations/scenes/       Manim 原始碼（common.py = 左多邊形＋右黏合的共用框架）
mkdocs.yml               網站設定；push 到 main 後由 GitHub Actions 自動部署
raw/                     手寫照片與預覽（不上傳）
```

## 動畫渲染

```bash
pip install manim
cd animations/scenes
# Cairo (CPU)：第 1 章黏合動畫
manim -qh ch01_gluing.py Torus
# OpenGL (GPU)：connected sum 動畫；有螢幕的電腦可直接 --renderer=opengl
manim --renderer=opengl --write_to_movie -qh ch01_connected_sum.py TorusSumTorus
# 無螢幕的伺服器：用 EGL 指定 GPU（MANIM_GPU=GPU 編號）
MANIM_GPU=2 python ../tools/manim_gl.py --renderer=opengl --write_to_movie -qh ch01_connected_sum.py TorusSumTorus
```

輸出在 `media/`，完成後複製到 `docs/assets/animations/`。

## 本機預覽網站

```bash
pip install mkdocs-material
mkdocs serve
```

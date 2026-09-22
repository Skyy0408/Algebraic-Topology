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
manim -qh ch01_gluing.py Torus      # 輸出到 media/，再複製到 docs/assets/animations/
```

## 本機預覽網站

```bash
pip install mkdocs-material
mkdocs serve
```

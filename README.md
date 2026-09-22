# Algebraic-Topology

Notes of a course in NTHU, 2026 Fall.

代數拓樸課堂筆記（主教材：W. S. Massey, *A Basic Course in Algebraic Topology*, GTM 127）。

## 結構

```
notes/                  各章筆記（Markdown，數學式用 $...$ / $$...$$）
animations/scenes/      Manim 原始碼（每個動畫一個 .py）
assets/animations/      渲染好的動畫（MP4 / GIF），由 notes 引用
assets/figures/         靜態圖
raw/photos/             手寫筆記原始照片（不推上 GitHub，見 .gitignore）
```

## 目錄

（待補）

## 動畫渲染

```bash
pip install manim
manim -qh animations/scenes/<file>.py <SceneName>
```

---
title: "Chapter 2. Fundamental Groups"
reference: "Massey, A Basic Course in Algebraic Topology, Ch. 2"
source_pages: "handwritten notes p.14–21"
---

# Chapter 2. Fundamental Groups

## 2.1 Objects and morphisms

Mathematical theories are usually about mathematical objects and mappings which preserve the structure of those objects.

| Subject | Objects | Mappings / morphisms |
|---|---|---|
| Linear algebra | linear spaces | linear transformations |
| Differential geometry | differentiable manifolds | differentiable mappings, diffeomorphisms |
| Functional analysis | Banach and Hilbert spaces | bounded linear operators |
| Topology | topological spaces | continuous functions, homeomorphisms |
| Group theory | groups | homomorphisms, isomorphisms |

Algebraic topology assigns groups to topological spaces:

$$
\text{topological space} \;\longrightarrow\; \text{groups: homotopy, homology, cohomology.}
$$

Intuitively, the fundamental group of a topological space $X$ is the set of equivalence classes of loops in $X$; two loops are considered equivalent if one can be continuously deformed into the other.

## 2.2 Paths and homotopy

**Definition.** A *path* in a topological space $X$ is a continuous function of the form

$$
f : [a,b] \to X .
$$

$f(a)$ (the *initial endpoint*) and $f(b)$ (the *terminal endpoint*) are called the *endpoints*.

If for all $x, y \in X$ there is a path $f : [a,b] \to X$ with $f(a) = x$ and $f(b) = y$, then $X$ is *pathwise (arcwise) connected*.

**Remark.** Pathwise connected $\Rightarrow$ connected.

Let $f_0, f_1 : [a,b] \to X$ be two paths with the same endpoints, $f_0(a) = f_1(a)$ and $f_0(b) = f_1(b)$.

**Definition.** We say that $f_0$ and $f_1$ are *homotopic* if there exists a continuous map $F : [a,b]\times[0,1] \to X$ such that

1. $F(t,0) = f_0(t)$, $t \in [a,b]$;
2. $F(t,1) = f_1(t)$, $t \in [a,b]$;
3. $F(a,s) = f_0(a) = f_1(a)$, $s \in [0,1]$;
4. $F(b,s) = f_0(b) = f_1(b)$, $s \in [0,1]$.

$F$ is called a *homotopy* between $f_0$ and $f_1$.

**Notation.** $f_0 \sim f_1$, or $f_0 \overset{F}{\sim} f_1$.

**Remark.**

- (a) $f \sim f$ (reflexive);
- (b) $f \sim g \iff g \sim f$ (symmetric);
- (c) $f \sim g$ and $g \sim h$ $\Rightarrow$ $f \sim h$ (transitive).

By (a), (b), (c), "$\sim$" is an equivalence relation on the space $C([a,b], X)$ of paths with prescribed initial and terminal endpoints.

**Example (straight-line homotopy).** Let $f_0, f_1 : [a,b] \to \mathbb{R}^n$ be any two paths with $f_0(a) = f_1(a)$, $f_0(b) = f_1(b)$. Let

$$
F(t,s) = (1-s) f_0(t) + s f_1(t), \qquad (t,s) \in [a,b]\times[0,1].
$$

Then $F(t,0) = f_0(t)$, $F(t,1) = f_1(t)$, $F(a,s) = f_0(a)$, $F(b,s) = f_0(b)$, so $f_0 \overset{F}{\sim} f_1$. We call this $F$ the *straight-line homotopy*.

<video class="anim" src="assets/animations/StraightLineHomotopy.mp4" controls loop muted autoplay playsinline></video>

Left: the parameter square, with the level line at height $s$. Right: the image in $X$; the endpoints stay fixed while the path sweeps from $f_0$ to $f_1$.

## 2.3 Reparametrization

Consider paths

$$
f : [a,b] \to X, \qquad g : [c,d] \to X, \qquad f(a) = g(c),\quad f(b) = g(d).
$$

Let $h$ be the unique linear homeomorphism from $[a,b]$ to $[c,d]$ with $h(a) = c$, $h(b) = d$; call it the *orientation preserving linear homeomorphism* ($h'$ with $h'(a) = d$, $h'(b) = c$ is the orientation reversing one).

<!-- FIG: graphs of the orientation preserving / reversing linear homeomorphisms -->

We say $f$ and $g$ are *equivalent* if $f = g \circ h$, i.e.

$$
f(x) = g(h(x)) \qquad\text{or}\qquad f(h^{-1}(y)) = g(y).
$$

Combining this equivalence with homotopy equivalence, we obtain an equivalence relation among paths in $X$ with the same initial and terminal endpoints.

More general reparametrizations: given a path $f : [a,b] \to X$ and an orientation preserving homeomorphism $\varphi : [a,b] \to [a,b]$, i.e. $\varphi$ is a homeomorphism with $\varphi(a) = a$, $\varphi(b) = b$:

> **Lemma.** $f \sim f \circ \varphi$.

*Proof.* Let $\varphi_s(t) = (1-s)t + s\varphi(t)$ (the straight-line homotopy between the identity and $\varphi$). Define $F : [a,b]\times[0,1] \to X$ by

$$
F(t,s) = f(\varphi_s(t)) = f\big((1-s)t + s\varphi(t)\big).
$$

Then

$$
F(t,0) = f(t), \quad F(t,1) = (f\circ\varphi)(t), \quad F(a,s) = f(a) = f(\varphi(a)), \quad F(b,s) = f(b) = f(\varphi(b)),
$$

so $f \overset{F}{\sim} f\circ\varphi$. $\blacksquare$

## 2.4 Products of paths

**Definition.** Given paths $f : [a,b] \to X$ and $g : [b,c] \to X$ with $f(b) = g(b)$, define the *product*

$$
(f \cdot g)(t) =
\begin{cases}
f(t), & a \le t \le b,\\
g(t), & b \le t \le c.
\end{cases}
$$

<!-- FIG: two paths joined at f(b) = g(b) -->

More generally, if $g : [c,d] \to X$ satisfies $g(c) = f(b)$, use the orientation preserving linear homeomorphism $h : [b,\, b+d-c] \to [c,d]$ to define

$$
(f \cdot g)(t) =
\begin{cases}
f(t), & a \le t \le b,\\
(g \circ h)(t), & b \le t \le b + d - c.
\end{cases}
$$

From these observations we may focus on paths defined on $[0,1]$: for $f, g : [0,1] \to X$ with $f(1) = g(0)$, redefine the product by

$$
(f \cdot g)(t) =
\begin{cases}
f(2t), & 0 \le t \le \tfrac12,\\
g(2t-1), & \tfrac12 \le t \le 1.
\end{cases}
$$

> **Lemma.** If $f_0 \overset{F}{\sim} f_1$, $g_0 \overset{G}{\sim} g_1$ and $f_0(1) = f_1(1) = g_0(0) = g_1(0)$, then $f_0 \cdot g_0 \sim f_1 \cdot g_1$.

*Proof.* Define $H : [0,1]\times[0,1] \to X$ by

$$
H(t,s) =
\begin{cases}
F(2t, s), & t \in [0, \tfrac12],\\
G(2t-1, s), & t \in [\tfrac12, 1].
\end{cases}
$$

Then

$$
H(t,0) =
\begin{cases}
F(2t,0) = f_0(2t) = (f_0\cdot g_0)(t), & t \in [0,\tfrac12],\\
G(2t-1,0) = g_0(2t-1) = (f_0 \cdot g_0)(t), & t \in [\tfrac12,1],
\end{cases}
$$

i.e. $H(t,0) = (f_0\cdot g_0)(t)$; similarly $H(t,1) = (f_1\cdot g_1)(t)$, and

$$
H(0,s) = F(0,s) = f_0(0) = (f_0\cdot g_0)(0), \qquad H(1,s) = (f_1 \cdot g_1)(1).
$$

Since $H$ is continuous, $f_0 \cdot g_0 \overset{H}{\sim} f_1 \cdot g_1$. $\blacksquare$

<!-- FIG: the square [0,1]^2 split into the F-half and the G-half -->

> **Lemma (associativity up to homotopy).** If $f, g, h$ are paths with $f(1) = g(0)$ and $g(1) = h(0)$, then
> $$(f\cdot g)\cdot h \sim f\cdot(g\cdot h).$$

*Proof.* Define $F : [0,1]\times[0,1] \to X$ by

$$
F(t,s) =
\begin{cases}
f\left(\dfrac{4t}{1+s}\right), & 0 \le t \le \dfrac{s+1}{4},\\[2mm]
g(4t-1-s), & \dfrac{s+1}{4} \le t \le \dfrac{s+2}{4},\\[2mm]
h\left(1 - \dfrac{4(1-t)}{2-s}\right), & \dfrac{s+2}{4} \le t \le 1 .
\end{cases}
$$

Then $(f\cdot g)\cdot h \overset{F}{\sim} f\cdot(g\cdot h)$. $\blacksquare$

<video class="anim" src="assets/animations/AssociativityReparam.mp4" controls loop muted autoplay playsinline></video>

The image in $X$ never changes; only the way $[0,1]$ is shared between $f$, $g$ and $h$ does — the cuts slide from $\tfrac14, \tfrac12$ to $\tfrac12, \tfrac34$.

## 2.5 Constant paths and inverses

Given $x \in X$, define the constant path $\varepsilon_x : [0,1] \to X$ by $\varepsilon_x(t) = x$ for all $t$.

> **Lemma.** Given a path $f : [0,1] \to X$,
> $$f \cdot \varepsilon_{f(1)} \sim f \sim \varepsilon_{f(0)} \cdot f .$$

*Proof.* Define $F : [0,1]\times[0,1] \to X$ by

$$
F(t,s) =
\begin{cases}
f(0), & 0 \le t \le \dfrac{s}{2},\\[2mm]
f\left(\dfrac{2t-s}{2-s}\right), & \dfrac{s}{2} \le t \le 1 .
\end{cases}
$$

Then

$$
F(t,0) = f(t), \qquad F(t,1) = (\varepsilon_{f(0)}\cdot f)(t), \qquad F(0,s) = f(0), \qquad F(1,s) = f(1),
$$

so $f \overset{F}{\sim} \varepsilon_{f(0)}\cdot f$. Similarly $f \cdot \varepsilon_{f(1)} \sim f$. $\blacksquare$

Given a path $f : [0,1] \to X$, define $\bar f : [0,1] \to X$ by $\bar f(t) = f(1-t)$, $t \in [0,1]$.

> **Lemma.** Given a path $f : [0,1] \to X$,
> $$f \cdot \bar f \sim \varepsilon_{f(0)}, \qquad \bar f \cdot f \sim \varepsilon_{f(1)} .$$

*Proof.* Define $F : [0,1]\times[0,1] \to X$ by

$$
F(t,s) =
\begin{cases}
f(2t), & 0 \le t \le \dfrac{s}{2},\\[2mm]
f(s), & \dfrac{s}{2} \le t \le \dfrac{2-s}{2},\\[2mm]
f(2-2t), & \dfrac{2-s}{2} \le t \le 1 .
\end{cases}
$$

Then $F(t,0) = f(0) = \varepsilon_{f(0)}(t)$ and

$$
F(t,1) =
\begin{cases}
f(2t), & 0 \le t \le \tfrac12,\\
f(2-2t) = f\big(1-(2t-1)\big) = \bar f(2t-1), & \tfrac12 \le t \le 1,
\end{cases}
= (f\cdot\bar f)(t),
$$

while $F(0,s) = f(0) = \varepsilon_{f(0)}(0)$ and $F(1,s) = f(0) = \varepsilon_{f(0)}(1)$. Hence $\varepsilon_{f(0)} \overset{F}{\sim} f\cdot\bar f$; similarly $\bar f \cdot f \sim \varepsilon_{f(1)}$. $\blacksquare$

<video class="anim" src="assets/animations/InversePath.mp4" controls loop muted autoplay playsinline></video>

At level $s$ the path runs out along $f$ as far as $f(s)$, waits there, and comes back; as $s \to 0$ it retracts to the constant path $\varepsilon_{f(0)}$.

## 2.6 The fundamental group

Now consider the space of loops in $X$ with initial and terminal points equal to $x$; call it the space of loops with base point $x$. Denote by $[f]$ the equivalence class of loops containing $f : [0,1] \to X$, $f(0) = f(1) = x$.

Define the product on these equivalence classes by

$$
[f]\cdot[g] := [f\cdot g].
$$

By the lemmas above this product is well defined, and:

**Identity.**

$$
[\varepsilon_x]\cdot[f] = [\varepsilon_x \cdot f] = [f], \qquad [f]\cdot[\varepsilon_x] = [f\cdot\varepsilon_x] = [f].
$$

**Inverse.**

$$
[f]\cdot[\bar f] = [f\cdot\bar f] = [\varepsilon_x] = [\bar f\cdot f] = [\bar f]\cdot[f],
$$

so $[\bar f]$ is the inverse $[f]^{-1}$ of $[f]$; the inverse of the product is the product of the inverse classes. Many people therefore write $f^{-1}$ for $\bar f$.

**Associativity.**

$$
\big([f]\cdot[g]\big)\cdot[h] = [f\cdot g]\cdot[h] = [(f\cdot g)\cdot h] = [f\cdot(g\cdot h)] = [f]\cdot[g\cdot h] = [f]\cdot\big([g]\cdot[h]\big).
$$

Hence the space of loops with base point $x$, with this product, is a group, called the *fundamental group*, or *Poincaré group*, or *first homotopy group*. Denote it by $\pi(X,x)$ or $\pi_1(X,x)$.

> **Theorem.** If $X$ is pathwise connected and $x, y \in X$, then $\pi(X,x) \cong \pi(X,y)$. In this case we denote them by $\pi(X)$.

*Proof.* Take a path $\gamma : [0,1] \to X$ with $\gamma(0) = x$, $\gamma(1) = y$. Define

$$
\gamma_{\#} : \pi(X,x) \to \pi(X,y), \qquad [f] \mapsto [\gamma^{-1}\cdot f\cdot\gamma].
$$

This is well defined: $f_0 \overset{F}{\sim} f_1$ implies $\gamma^{-1}\cdot f_0 \cdot \gamma \sim \gamma^{-1}\cdot f_1\cdot\gamma$. It is a homomorphism:

$$
\gamma_{\#}\big([f]\cdot[g]\big) = \gamma_{\#}\big([f\cdot g]\big) = [\gamma^{-1}\cdot f\cdot g\cdot\gamma]
= [\gamma^{-1}\cdot f\cdot\gamma\cdot\gamma^{-1}\cdot g\cdot\gamma] = \gamma_{\#}([f])\cdot\gamma_{\#}([g]).
$$

Consider $(\gamma^{-1})_{\#} : \pi(X,y) \to \pi(X,x)$, $[f] \mapsto [\gamma\cdot f\cdot\gamma^{-1}]$; similarly it is a group homomorphism, and

$$
(\gamma^{-1})_{\#} \circ \gamma_{\#} = \mathrm{id}, \qquad \gamma_{\#}\circ(\gamma^{-1})_{\#} = \mathrm{id}.
$$

Hence $\gamma_{\#}$ is a group isomorphism. $\blacksquare$

<video class="anim" src="assets/animations/ChangeOfBasePoint.mp4" controls loop muted autoplay playsinline></video>

The loop at $y$ runs $\gamma^{-1}$ to $x$, then the loop $f$, then $\gamma$ back to $y$.

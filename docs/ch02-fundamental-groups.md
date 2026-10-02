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

## 2.7 Induced homomorphisms

Consider a continuous map of pointed spaces $\varphi : (X,x) \to (Y,y)$, i.e. a continuous $\varphi : X \to Y$ with $\varphi(x) = y$. Define

$$
\varphi_* : \pi(X,x) \to \pi(Y,y), \qquad [f] \mapsto [\varphi\circ f].
$$

**Well defined.** Observe that $f_0 \overset{F}{\sim} f_1$ implies $\varphi\circ f_0 \overset{\varphi\circ F}{\sim} \varphi\circ f_1$. Indeed, let $F : [0,1]\times[0,1] \to X$ satisfy $F(t,0) = f_0(t)$ and $F(t,1) = f_1(t)$. Then $(\varphi\circ F)(t,s) = \varphi(F(t,s))$ is continuous and

$$
(\varphi\circ F)(t,0) = (\varphi\circ f_0)(t), \qquad (\varphi\circ F)(t,1) = (\varphi\circ f_1)(t).
$$

In particular, if $f_0, f_1$ are loops based at $x$, then $\varphi_*([f_0]) = [\varphi\circ f_0] = [\varphi\circ f_1] = \varphi_*([f_1])$. Thus $\varphi_*$ is well defined.

**Homomorphism.**

$$
\varphi_*\big([f]\cdot[g]\big) = \varphi_*\big([f\cdot g]\big) = [\varphi\circ(f\cdot g)]
\overset{(*)}{=} [(\varphi\circ f)\cdot(\varphi\circ g)] = [\varphi\circ f]\cdot[\varphi\circ g] = \varphi_*([f])\cdot\varphi_*([g]),
$$

where $(*)$ holds because

$$
\varphi\circ(f\cdot g)(t) =
\begin{cases}
\varphi(f(2t)), & t\in[0,\tfrac12],\\[2pt]
\varphi(g(2t-1)), & t\in[\tfrac12,1],
\end{cases}
\qquad\text{i.e.}\qquad \varphi\circ(f\cdot g) = (\varphi\circ f)\cdot(\varphi\circ g).
$$

Hence $\varphi_*$ is a homomorphism. We call $\varphi_*$ the *homomorphism induced by* $\varphi$.

!!! note "Notation"
    Throughout, $i$ denotes an inclusion map and $\iota$ denotes an identity map; $1_G$ denotes the identity *element* of a group $G$.

## 2.8 Functoriality

> **Lemma.** Let $\varphi : (X,x) \to (Y,y)$ and $\psi : (Y,y) \to (Z,z)$ be continuous. Then
> **(a)** $(\psi\circ\varphi)_* = \psi_*\circ\varphi_*$, and
> **(b)** $(\iota_X)_* = \iota_{\pi(X,x)}$ for every $x \in X$.

*Proof.* (a) For $[f] \in \pi(X,x)$,

$$
(\psi\circ\varphi)_*[f] = [(\psi\circ\varphi)\circ f] = [\psi\circ(\varphi\circ f)] = \psi_*\big([\varphi\circ f]\big) = (\psi_*\circ\varphi_*)[f].
$$

Hence $(\psi\circ\varphi)_* = \psi_*\circ\varphi_*$.

(b) $(\iota_X)_*[f] = [\iota_X\circ f] = [f]$, so $(\iota_X)_* = \iota_{\pi(X,x)}$. $\blacksquare$

**Question.** When do two maps $\varphi_0,\varphi_1 : (X,x) \to (Y,y)$ induce the same homomorphism?

To answer this we generalise the notion of "homotopic" from paths to maps.

## 2.9 Homotopy of maps

> **Definition.** Let $\varphi_0,\varphi_1 : X \to Y$ be continuous maps and $I = [0,1]$. We say $\varphi_0$ and $\varphi_1$ are *homotopic*, denoted $\varphi_0 \simeq \varphi_1$, if there exists a continuous $\Phi : X\times I \to Y$ such that
> **(1)** $\Phi(x,0) = \varphi_0(x)$ for all $x \in X$, and
> **(2)** $\Phi(x,1) = \varphi_1(x)$ for all $x \in X$.

**Notation.** We also write $\varphi_0 \overset{\Phi}{\simeq} \varphi_1$, and call $\Phi$ the *homotopy between* $\varphi_0$ *and* $\varphi_1$.

Let $A \subseteq X$ be a subset with $\varphi_0|_A = \varphi_1|_A$. We say $\varphi_0,\varphi_1$ are *homotopic relative to* $A$ if there exists a continuous $\Phi : X\times I \to Y$ satisfying (1), (2) and

$$
\textbf{(3)}\quad \Phi(a,s) = \varphi_0(a) = \varphi_1(a) \qquad \text{for all } a\in A,\ s\in I.
$$

So the deformation is free to move the rest of $X$, but every point of $A$ is pinned for the whole duration.

<video class="anim" src="assets/animations/RelativeHomotopy.mp4" controls loop muted autoplay playsinline></video>

Here $X$ is an interval and the two maps are drawn as graphs over it. The family $\Phi_s$ sweeps $\varphi_0$ into $\varphi_1$, but over the green segment $A$ every curve of the family passes through the same points.

**Notation.** $\Phi(t,s)$ is often denoted by $\Phi_s(t)$.

> **Theorem 2.** If $\varphi_0,\varphi_1 : (X,x) \to (Y,y)$ are continuous and homotopic relative to $\{x\}$, then $(\varphi_0)_* = (\varphi_1)_* : \pi(X,x) \to \pi(Y,y)$.

*Proof.* Given $[f] \in \pi(X,x)$, so $f : I \to X$ with $f(0) = f(1) = x$. Let $\Phi : X\times I \to Y$ be a homotopy between $\varphi_0$ and $\varphi_1$ relative to $\{x\}$, i.e.

$$
\begin{cases}
\Phi(\xi,0) = \varphi_0(\xi), & \forall\,\xi\in X,\\[2pt]
\Phi(\xi,1) = \varphi_1(\xi), & \forall\,\xi\in X,\\[2pt]
\Phi(x,s) = \varphi_0(x) = \varphi_1(x) = y, & \forall\,s\in I.
\end{cases}
$$

Define $H : I\times I \to Y$ by $(t,s) \mapsto \Phi(f(t),s)$. Then

$$
\begin{cases}
H(t,0) = (\varphi_0\circ f)(t), & \forall\,t\in I,\\[2pt]
H(t,1) = (\varphi_1\circ f)(t), & \forall\,t\in I,\\[2pt]
H(0,s) = H(1,s) = \Phi(x,s) = \varphi_0(x) = \varphi_1(x) = y, & \forall\,s\in I.
\end{cases}
$$

Thus $\varphi_0\circ f \sim \varphi_1\circ f$, and therefore

$$
(\varphi_0)_*[f] = [\varphi_0\circ f] = [\varphi_1\circ f] = (\varphi_1)_*[f].
$$

Since $[f]$ is arbitrary, $(\varphi_0)_* = (\varphi_1)_*$. $\blacksquare$

## 2.10 Retracts

> **Definition.** A subset $A \subseteq X$ is called a *retract* of $X$ if there exists a continuous $r : X \to A$ with $r(a) = a$ for all $a \in A$. Such an $r$ is called a *retraction*.

**Example.** The Möbius band $MB$: let $A$ be its centre circle. Then $A$ is a retract of $MB$ — collapse each transverse segment to its midpoint; this is trivially continuous.

**Example.** The closed unit disc $B^2$ has $\partial B^2 = S^1$, but $S^1$ is **not** a retract of $B^2$. Why? The fundamental group answers this below.

Let $i : A \to X$ be the inclusion map and $r : X \to A$ a map. Then

$$
r \text{ is a retraction} \iff r\circ i = \iota_A ,
$$

and applying the Lemma of §2.8,

$$
r_*\circ i_* = (r\circ i)_* = (\iota_A)_* = \iota_{\pi(A,a)} \qquad \forall\,a\in A .
$$

Consequently

$$
i_* : \pi(A,a) \to \pi(X,a) \ \text{ is } 1\text{–}1, \qquad
r_* : \pi(X,a) \to \pi(A,a) \ \text{ is onto}.
$$

> **Remark.** Let $G_1 \overset{f}{\to} G_2 \overset{g}{\to} G_1$ be group homomorphisms with $g\circ f = \iota_{G_1}$. Then $f$ is $1$–$1$ and $g$ is onto.

*Proof.* If $f(\mathsf{x}) = 1_{G_2}$ then $\mathsf{x} = (g\circ f)(\mathsf{x}) = g(1_{G_2}) = 1_{G_1}$, so $\ker f$ is trivial and $f$ is $1$–$1$. For every $\mathsf{x} \in G_1$ we have $\mathsf{x} = g(f(\mathsf{x}))$, so $g$ is onto. $\blacksquare$

**Example.** $X = S^2$ and $A = \{(x,y,z)\in S^2 : z \le 0\}$, the closed lower hemisphere. Then $A$ is a retract of $S^2$ via

$$
r(x,y,z) = (x,y,-|z|).
$$

**Example.** $X = S^2$ and $A = \{N\}$ a single point. Take $r : S^2 \to \{N\}$, the constant map; so a point is always a retract.

**Example.** $X = S^2$ and $A = \{(x,y,z)\in S^2 : z < 0\}$, the *open* lower hemisphere. Then $A$ is **not** a retract — by the Lemma below a retract of a Hausdorff space must be closed.

> **Lemma.**
> **(a)** A retract of a connected set is connected.
> **(b)** A retract of a Hausdorff space is closed.

*Proof.* (a) is trivial, since the continuous image of a connected set is connected.

(b) Let $r : X \to A$ with $r|_A = \iota_A$, and let $i$ be the inclusion. Then

$$
A = \{\,\mathsf{x}\in X : (i\circ r)(\mathsf{x}) = \mathsf{x}\,\}.
$$

Put $f = i\circ r$, a continuous function; then $A = \mathrm{Fix}(f)$, and it suffices to show $\mathrm{Fix}(f)$ is closed.

Let $\mathsf{x} \notin \mathrm{Fix}(f)$, i.e. $f(\mathsf{x}) \ne \mathsf{x}$. Since $X$ is Hausdorff there are neighbourhoods $U$ of $f(\mathsf{x})$ and $V$ of $\mathsf{x}$ with $U\cap V = \varnothing$. Then $f^{-1}(U)\cap V$ is an open neighbourhood of $\mathsf{x}$, and

$$
\big(f^{-1}(U)\cap V\big)\cap \mathrm{Fix}(f) = \varnothing .
$$

Hence $\mathrm{Fix}(f)^{\,c}$ is open, so $\mathrm{Fix}(f) = A$ is closed. $\blacksquare$

**Facts.** $\pi(S^2) \cong \{1\}$ and $\pi(S^1) \cong \mathbb{Z}$.

Since $i_*$ is $1$–$1$, a retract $A$ of $X$ has $\pi(A,a)$ isomorphic to a subgroup of $\pi(X,a)$:

$$
\pi(A,a) \overset{i_*}{\longrightarrow} \pi(X,a) \overset{r_*}{\longrightarrow} \pi(A,a),
\qquad r_*\circ i_* = \iota .
$$

This is the obstruction promised above.

**Example.** $X = B^2$ with $S^1 = \partial B^2$. Every loop in $B^2$ is homotopic to a constant map, so $\pi(B^2) = \{1\}$. But $\pi(S^1) \cong \mathbb{Z}$, which is not a subgroup of $\{1\}$. Therefore $\partial B^2 = S^1$ is not a retract of $B^2$.

**Example.** $X = S^2$ with $A = \{(x,y,z)\in S^2 : z = 0\}$, the equator. Then $\pi(A)\cong\mathbb{Z}$ is not a subgroup of $\pi(S^2)\cong\{1\}$, so $A$ is not a retract of $S^2$.

## 2.11 Deformation retracts and contractibility

> **Definition.** We say $A \subseteq X$ is a *deformation retract* of $X$ if there is a retraction $r : X \to A$ such that $i\circ r$ is homotopic to $\iota_X$ relative to $A$; i.e. there is a homotopy $H : X\times I \to X$ with
> **(1)** $H(\mathsf{x},0) = \mathsf{x}$,
> **(2)** $H(\mathsf{x},1) = r(\mathsf{x})$ for all $\mathsf{x}\in X$,
> **(3)** $H(a,s) = a$ for all $a\in A$, $s\in I$.

> **Theorem 3.** If $A$ is a deformation retract of $X$, then $i_* : \pi(A,a) \to \pi(X,a)$ is an isomorphism for every $a \in A$.

*Proof.* By assumption $i\circ r$ and $\iota_X$ are homotopic relative to $\{a\}$ for every $a\in A$. By Theorem 2,

$$
(i\circ r)_* = (\iota_X)_* : \pi(X,a) \to \pi(X,a), \qquad\text{and}\qquad (i\circ r)_* = i_*\circ r_* .
$$

Hence $i_*$ is onto. Since $r_*\circ i_* : \pi(A,a) \to \pi(A,a)$ equals $\iota_{\pi(A,a)}$, $i_*$ is also $1$–$1$. Therefore $i_*$ is an isomorphism. $\blacksquare$

> **Definition.** $X$ is *contractible to a point* if there is $x_0 \in X$ such that $\{x_0\}$ is a deformation retract of $X$.

> **Corollary.** If $X$ is contractible to a point, then $\pi(X) \cong \{1\}$.

> **Definition.** $X$ is *simply connected* if $\pi(X) \cong \{1\}$.

**Example (1).** $\{0\}$ is a deformation retract of $\mathbb{R}^n$: set $H(\mathsf{x},s) = (1-s)\mathsf{x}$. Then $H(\mathsf{x},0) = \mathsf{x}$ and $H(\mathsf{x},1) = 0$ for all $\mathsf{x}$, so $\pi(\mathbb{R}^n) \cong \{1\}$; that is, $\mathbb{R}^n$ is simply connected.

**Example (2).** The map

$$
r : \mathbb{R}^n\setminus\{0\} \to S^{n-1}, \qquad r(\mathsf{x}) = \frac{\mathsf{x}}{|\mathsf{x}|}
$$

is a retraction, and $\iota_{\mathbb{R}^n\setminus\{0\}}$ and $i\circ r$ are homotopic relative to the subset $S^{n-1}$. To see this, define $H : (\mathbb{R}^n\setminus\{0\})\times I \to \mathbb{R}^n\setminus\{0\}$ by

$$
H(\mathsf{x},s) = (1-s)\mathsf{x} + s\,\frac{\mathsf{x}}{|\mathsf{x}|},
$$

so that

$$
\begin{cases}
H(\mathsf{x},0) = \mathsf{x}, & \forall\,\mathsf{x}\in\mathbb{R}^n\setminus\{0\},\\[2pt]
H(\mathsf{x},1) = r(\mathsf{x}), & \forall\,\mathsf{x}\in\mathbb{R}^n\setminus\{0\},\\[2pt]
H(\mathsf{x},s) = \mathsf{x}, & \forall\,\mathsf{x}\in S^{n-1}.
\end{cases}
$$

Knowing that $\pi(S^1)\cong\mathbb{Z}$, we conclude $\pi(\mathbb{R}^2\setminus\{0\}) \cong \mathbb{Z}$.

<video class="anim" src="assets/animations/RadialDeformationRetract.mp4" controls loop muted autoplay playsinline></video>

Each point slides along its own ray: points inside the sphere move out, points outside move in, and points of $S^{n-1}$ never move at all. The origin is the one place the formula would break down, and it is exactly the point that has been removed.

## 2.12 The circle, and Brouwer's fixed point theorem

> **Theorem 4.** $\pi(S^1) \cong \mathbb{Z}$.

*Sketch of proof.* Given $f : [0,1] \to S^1$ with $f(0) = f(1) = (1,0)$, there is a unique $\theta : [0,1] \to \mathbb{R}$ with $\theta(0) = 0$ and

$$
f(t) = \big(\cos\theta(t),\ \sin\theta(t)\big).
$$

One knows $\theta(1) \in 2\pi\mathbb{Z}$. Take

$$
p : \mathbb{R} \to S^1, \qquad \mathsf{x} \mapsto (\cos \mathsf{x},\ \sin \mathsf{x}),
$$

so that the triangle formed by $\theta : [0,1]\to\mathbb{R}$, $f : [0,1]\to S^1$ and $p : \mathbb{R}\to S^1$ commutes, i.e. $f = p\circ\theta$. Define

$$
\phi : \pi\big(S^1,(1,0)\big) \to \mathbb{Z}, \qquad [f] \mapsto \frac{\theta(1)}{2\pi},
$$

and show that $\phi$ is $1$–$1$ and onto. $\blacksquare$

> **Brouwer Fixed Point Theorem.** If $f : B^2 \to B^2$ is continuous, then there exists $\mathsf{x}\in B^2$ with $f(\mathsf{x}) = \mathsf{x}$.

*Proof.* Suppose otherwise: let $f : B^2 \to B^2$ be continuous without a fixed point. Consider the line segment from $f(\mathsf{x})$ to $\mathsf{x}$, then extend it through the point $\mathsf{x}$ to the boundary of $B^2$, and let $r(\mathsf{x})$ be the point where it meets $\partial B^2$.

Then $r : B^2 \to S^1 = \partial B^2$ is well defined precisely because $f$ has no fixed point; $r$ is continuous, and $r = \iota$ on $\partial B^2 = S^1$. Hence $S^1$ is a retract of $B^2$ with retraction $r$, so

$$
\mathbb{Z} \cong \pi(S^1) \ \text{ is a subgroup of } \ \pi(B^2) \cong \{1\},
$$

a contradiction. $\blacksquare$

> **Remark.** Both hypotheses matter.
>
> - There is a continuous map $f : (B^2)^{\circ} \to (B^2)^{\circ}$ of the open disc without a fixed point.
> - There is a continuous map $f : B^2\setminus\{x_0\} \to B^2\setminus\{x_0\}$ without a fixed point — for instance a rotation of the disc about its centre, with $x_0$ the centre removed.

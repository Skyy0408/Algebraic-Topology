---
title: "Chapter 1. Surfaces"
reference: "Massey, A Basic Course in Algebraic Topology, Ch. 1"
source_pages: "handwritten notes p.1–13"
---

# Chapter 1. Surfaces

## 1.0 Surfaces and manifolds

**Examples (compact).**

- $S^2$, the 2-dimensional sphere:
  $$S^2 = \{x \in \mathbb{R}^3 \mid \|x\| = 1\}.$$
- $T^2$, the 2-dimensional torus, the surface of revolution of a circle $C$:
  $$\left(\sqrt{x^2+y^2} - 1\right)^2 + z^2 = \frac14.$$
- The double torus, triple torus, …: the equations are not "simple" enough.

<!-- FIG: sphere, torus, double torus, triple torus -->

**Examples (unbounded).**

- Paraboloid $z = x^2 + y^2$.
- Saddle $z = x^2 - y^2$.

<!-- FIG: paraboloid and saddle -->

Roughly speaking, a surface is a set (geometric object) which locally looks like $\mathbb{R}^2$.

**Definition.** We say a set $M^n$ is an *$n$-dimensional manifold* ($n$-manifold) if

1. $M^n$ is a Hausdorff space (i.e. a topological space satisfying the $T_2$-axiom);
2. $\forall x \in M^n$, $\exists\, U$ a neighborhood of $x$ such that $U$ is homeomorphic to
   $$B^n = \{x \in \mathbb{R}^n \mid \|x\| < 1\}.$$

Unless specified otherwise, we also assume

3. $M^n$ is connected;
4. $M^n$ is second countable (i.e. there is a countable base for the topology).

**Definition.** A *surface* is a 2-manifold.

In this chapter, we focus on compact surfaces.

## 1.1 Some properties

**Hausdorff spaces.**

1. Subspaces of a Hausdorff space are Hausdorff.
2. Products of Hausdorff spaces are Hausdorff.
3. Compact subsets of a Hausdorff space are closed.

**Manifolds.**

1. Open subsets of an $n$-manifold are $n$-manifolds.
2. If $M^m, N^n$ are an $m$-manifold and an $n$-manifold, then $M^m \times N^n$ is an $(m+n)$-manifold.

**Example.**

$$
S^1 = \{x \in \mathbb{R}^2 : \|x\| = 1\} \cong \mathbb{R}/\sim, \qquad x \sim y \iff x - y \in \mathbb{Z},
$$

and

$$
S^1 \cong [0,1]/\{0,1\}.
$$

Hence

$$
T^2 = S^1 \times S^1 \cong [0,1]\times[0,1]/\sim,
\qquad
\begin{cases}
\{0\}\times[0,1] \sim \{1\}\times[0,1],\\
[0,1]\times\{0\} \sim [0,1]\times\{1\}.
\end{cases}
$$

<!-- FIG: square with both pairs of opposite edges identified → cylinder → torus -->

**Open sets.** An open set of the quotient is represented in the square by: an open disk in the interior; two half-disks on a pair of identified edges; four quarter-disks at the four corners (all corners are one point).

<!-- FIG: the four types of open neighbourhoods in the square -->

Such open sets generate the *quotient topology* on $[0,1]\times[0,1]/\sim\; = T^2$.

We can generalize this example by identifying different edges:

- one pair of opposite edges identified with the **same** direction → **cylinder**;
- one pair of opposite edges identified with **opposite** directions → **Möbius band**.

<!-- FIG: cylinder and Möbius band from a square -->

## 1.2 The real projective plane

**Definition.** The *real projective plane* $\mathbb{RP}^2$ is the quotient space $S^2/\sim$, where $x \sim -x$ for all $x \in S^2$.

Alternatively,

$$
\mathbb{RP}^2 = (\mathbb{R}^3 \setminus \{0\})/\sim, \qquad x \sim \lambda x \quad \forall \lambda \neq 0,\ \forall x \in \mathbb{R}^3\setminus\{0\}.
$$

Thus $\mathbb{RP}^2$ is the "space of lines through the origin".

**Remark.**

1. The definition extends to higher dimensions: $\mathbb{RP}^n$.
2. Also to other fields, e.g. $\mathbb{CP}^n$.
3. In particular, $\mathbb{RP}^1 \cong S^1$.

**Q.** How do we see $\mathbb{RP}^2$ as a polygon with identified edges?

Begin with the closed upper hemisphere. Only antipodal points on the equator remain to be identified, so

$$
\mathbb{RP}^2 \cong D^2/(x \sim -x \text{ on } \partial D^2),
$$

which is a square (bigon) whose boundary is read as $aa$. This can be visualized by "cut and glue".

<!-- FIG: hemisphere → disk with antipodal boundary identification → square with edges a, a -->
<!-- ANIM candidate: hemisphere flattening to disk, then to the square -->

## 1.3 Connected sums

**Definition.** Let $S_1, S_2$ be surfaces. The *connected sum* $S_1 \# S_2$ is obtained by cutting out disks $D_1 \subseteq S_1$, $D_2 \subseteq S_2$, choosing an arbitrary homeomorphism $h : \partial D_1 \to \partial D_2$, and identifying $x \in \partial D_1$ with $h(x) \in \partial D_2$:

$$
S_1 \# S_2 = (S_1 \setminus D_1) \cup_h (S_2 \setminus D_2).
$$

**Fact.** The topological type of $S_1 \# S_2$ does not depend on $D_1, D_2$ and $h$; i.e. $\#$ is well-defined up to homeomorphism.

$$
S^2 \# S^2 \cong S^2, \qquad S^2 \# T^2 \cong T^2, \qquad T^2 \# T^2 \# T^2 .
$$

**Back to $\mathbb{RP}^2$.** Remove a disk $D$ from the center of the disk model of $\mathbb{RP}^2$. Cutting the remainder along a diameter and regluing gives a strip whose ends are glued with a twist:

$$
\mathbb{RP}^2 \setminus D \cong \text{Möbius band (MB)}.
$$

Therefore

$$
\mathbb{RP}^2 = \mathrm{MB} \cup_f D, \qquad f : \partial\mathrm{MB} \xrightarrow{\ \text{homeo}\ } \partial D, \quad \partial \mathrm{MB} \cong S^1 \cong \partial D.
$$

<!-- FIG: disk with hole → two strips → Möbius band -->
<!-- ANIM candidate: RP^2 minus a disk becoming a Möbius band -->

**Example (Klein bottle).** The Klein bottle is the surface $K := \mathbb{RP}^2 \# \mathbb{RP}^2$.

Since $\mathbb{RP}^2 \setminus D$ is a Möbius band, $K$ is a union of two Möbius bands.

Again, we can express $K$ as a polygon with edges properly identified: take $P_1 \cong \mathbb{RP}^2 \cong P_2$ (disks with boundaries $a_1a_1$ and $a_2a_2$), cut out the small disks $c_1, c_2$, and glue along $c$. After cutting along a diagonal and regluing, the result is the square in which one pair of opposite edges is identified with the same direction and the other pair with opposite directions.

<!-- FIG: the sequence of polygons on p.4 (P1, P2 → square → ... → Klein bottle square) -->
<!-- ANIM candidate: RP^2 # RP^2 → Klein bottle square -->

To express $K$ as gluing two Möbius bands: cut the Klein-bottle square along two horizontal lines $c, d$. The middle strip (edges $c$, $d$, sides $b$, $b$) is a Möbius band; the top and bottom strips glue along $a$ into another Möbius band (edges $d$, $c$, sides $e, f$).

<!-- FIG: Klein bottle square cut into two Möbius bands -->

**Facts.**

$$
S_1 \# S_2 \cong S_2 \# S_1, \qquad (S_1 \# S_2)\# S_3 \cong S_1 \#(S_2 \# S_3).
$$

$\Rightarrow$ the topological types of surfaces under $\#$ form an abelian semigroup.

### Quotient topology (formal description)

**Definition.**

- Given topological spaces $X, Y$ and a surjection $p : X \to Y$, we say $p$ is a *quotient map* if
  $$U \subseteq Y \text{ is open} \iff p^{-1}(U) \subseteq X \text{ is open}.$$
- Let $X$ be a topological space, $A$ a set, and $p : X \to A$ surjective. The *quotient topology* on $A$ is the unique topology such that $p$ is a quotient map.
- Let $X^*$ be a partition of $X$, i.e. a collection of disjoint subsets of $X$ whose union is $X$. Consider
  $$p : X \to X^*, \qquad p(x) = [x] \in X^* \text{ with } x \in [x].$$
  If $X$ is a topological space, then $X^*$ with the quotient topology is called the *quotient space*.

**Example.** $\mathbb{RP}^2 = S^2/\{\text{antipodal points}\}$:
$X = S^2$, $X^* = \{\{x, -x\} : x \in S^2\}$. $\mathbb{RP}^2$ is the quotient space of $S^2$ with quotient map $p(x) = \{x, -x\}$.

Alternatively, $\mathbb{RP}^2 = D^2/\{\text{antipodal points on } \partial D = S^1\}$: $X = D^2$, and $X^*$ consists of

$$
\{(x,y)\},\ x^2+y^2<1; \qquad \{(x,y),(-x,-y)\},\ x^2+y^2=1.
$$

**Example.** $T^2 = [0,1]\times[0,1]/\sim$: $X = [0,1]\times[0,1]$, and $X^*$ consists of

$$
\begin{aligned}
&\{(x,y)\}, && 0<x<1,\ 0<y<1,\\
&\{(0,y),(1,y)\}, && 0<y<1,\\
&\{(x,0),(x,1)\}, && 0<x<1,\\
&\{(0,0),(0,1),(1,0),(1,1)\}.
\end{aligned}
$$

### More examples of connected sums

1. $\mathbb{RP}^2 \# \mathbb{RP}^2 \# \mathbb{RP}^2 \cong K \# \mathbb{RP}^2$: word $a_1a_1a_2a_2a_3a_3$.
2. $T^2 \# T^2$:
   $$a_1 b_2 a_2^{-1} b_2^{-1} a_2 b_1 a_1^{-1} b_1^{-1} \;\cong\; a_1 b_1 a_1^{-1} b_1^{-1} a_2 b_2 a_2^{-1} b_2^{-1}.$$
   Why are the two words equivalent? We need some "algebraic rules" for these symbolic sequences.
3. $S^2$: $aa^{-1}$.
4. $T^2 \# \cdots \# T^2 = nT^2$: $a_1b_1a_1^{-1}b_1^{-1}\,a_2b_2a_2^{-1}b_2^{-1}\cdots a_nb_na_n^{-1}b_n^{-1}$ (polygon with $4n$ edges).
5. $\mathbb{RP}^2 \# \cdots \# \mathbb{RP}^2 = n\mathbb{RP}^2$: $a_1a_1a_2a_2\cdots a_na_n$ (polygon with $2n$ edges).

<!-- FIG: polygons for examples 1–3 -->

## 1.4 Classification theorem

> **Classification Theorem for Compact Connected Surfaces.** Any compact connected surface is homeomorphic to either
> $$S^2, \quad nT^2, \quad \text{or} \quad n\mathbb{RP}^2 \quad \text{for some } n \in \mathbb{N}.$$

### Triangulations

**Definition.** A *triangulation* of a compact surface $S$ is a finite collection of closed sets $\{T_1,\dots,T_n\}$ such that

1. each $T_i \cong$ a triangle;
2. for all $i \neq j$, $T_i \cap T_j$ is either an edge, a vertex, or $\varnothing$;
3. $\bigcup_{i=1}^n T_i = S$.

**Theorem (Radó).** Any compact surface has a triangulation.

**Examples.**

- $T^2$: triangulation with 18 triangles.
- $\mathbb{RP}^2$: triangulation with 10 triangles.

<!-- FIG: 18-triangle triangulation of T^2 (3x3 grid, labels 1–4) and 10-triangle triangulation of RP^2 -->

The theorem allows us to identify compact surfaces with polygons whose edges are properly identified.

### Euler characteristic

Adding a vertex inside a triangle and joining it to the three corners gives another triangulation, with 2 more faces, 3 more edges and 1 more vertex. Let $F$, $E$, $V$ be the numbers of faces, edges, vertices. Then

$$
F - E + V \text{ is unchanged.}
$$

We call this number the *Euler characteristic* $\chi(S)$ of the compact surface $S$. The observation above suggests that $\chi(S)$ is well-defined, i.e. independent of the triangulation.

| Surface | Triangulation | $F - E + V$ |
|---|---|---|
| $S^2$ | tetrahedron | $4 - 6 + 4 = 2$ |
| $S^2$ | cube (each face cut into 2 triangles) | $12 - 18 + 8 = 2$ |
| $T^2$ | 18 triangles | $18 - 27 + 9 = 0$ |
| $\mathbb{RP}^2$ | 10 triangles | $10 - 15 + 6 = 1$ |

**Connected sum.** Remove one triangle from each of $S_1$ $(F_1,E_1,V_1)$ and $S_2$ $(F_2,E_2,V_2)$ and glue: we lose 2 faces, 3 edges and 3 vertices. So

$$
\begin{aligned}
\chi(S_1 \# S_2) &= (F_1+F_2-2) - (E_1+E_2-3) + (V_1+V_2-3)\\
&= (F_1+F_2) - (E_1+E_2) + (V_1+V_2) - 2\\
&= \chi(S_1) + \chi(S_2) - 2.
\end{aligned}
$$

> **Theorem.** $\chi(S_1 \# S_2) = \chi(S_1) + \chi(S_2) - 2.$

**Examples.**

$$
\chi(S^2) = 2, \quad \chi(T^2) = 0, \quad \chi(gT^2) = 2 - 2g, \qquad
\chi(\mathbb{RP}^2) = 1, \quad \chi(g\mathbb{RP}^2) = 2 - g.
$$

$g$ is called the *genus* of the surface.

### From a triangulation to a polygon

Let $\{T_1, T_2, \dots, T_n\}$ be a triangulation of a compact surface. We can order them so that $T_k$ has an edge in common with at least one of $T_1, \dots, T_{k-1}$:

- Pick an arbitrary $T_1$.
- Choose $T_2$ with $T_1 \cap T_2 = $ an edge.
- Choose $T_3$ with $T_1 \cap T_3$ or $T_2 \cap T_3 = $ an edge.
- Continue until no such $T_k$ can be found.

If this stops before all triangles are used, we get $\{T_1,\dots,T_{k-1}\}$ and $\{T_k,\dots,T_n\}$ that meet in at most vertices; near such a vertex the surface is not locally $\mathbb{R}^2$, contradicting connectedness / the manifold condition.

**Conclusion.** Given a compact surface $S$, there exists a polygon with an even number of edges such that $S \cong$ the polygon with edges properly identified.

## 1.5 Proof of the classification theorem

In a word, a pair of edges is of the

- **1st type** if it appears as $\cdots a \cdots a^{-1} \cdots$;
- **2nd type** if it appears as $\cdots b \cdots b \cdots$.

<!-- FIG: hexagon with a, b, a, b -->

**Surgery: cut and glue.**

1. **Eliminate adjacent edges of the 1st kind:** $\cdots a a^{-1} \cdots$ can be folded away.
2. **Single vertex:** cut along a diagonal $c$ and reglue along $a$; this gives one fewer $P$-type vertex and one more $Q$-type vertex.
   Repeat 1 and 2 to eliminate all $P$-type vertices.
3. **Make pairs of the 2nd kind adjacent:**
   $$A\,b\,B\,b\,C \;\longrightarrow\; A\,B^{-1}\,a\,a\,C.$$
4. **Assume there are 2 pairs of edges of the 1st kind.** Then there is a pair of the 1st kind which separates such a pair:
   $$A\,a\,B\,b^{-1}\,C\,a^{-1}\,D\,b\,E \;\longrightarrow\; A\,a\,c\,a^{-1}\,D\,C\,c^{-1}\,B\,E \;\longrightarrow\; A\,D\,C\,d\,c\,d^{-1}\,c^{-1}\,B\,E.$$

<!-- FIG: surgery steps 1–4 -->
<!-- ANIM candidate: step 3 and step 4 cut-and-glue -->

**Lemma.** $T^2 \# \mathbb{RP}^2 \cong 3\mathbb{RP}^2$.

Sketch: $T^2 \# \mathrm{MB}$ and $K \# \mathrm{MB}$ both reduce to the same square with a handle attached; hence $T^2 \# \mathrm{MB} \cong K \# \mathrm{MB} \cong \mathbb{RP}^2 \# \mathbb{RP}^2 \# \mathrm{MB}$.

<!-- FIG: torus with hole → handle; T^2 # MB and K # MB -->
<!-- ANIM candidate: sliding the handle through the Möbius band -->

**Proof of the Classification Theorem.**

1. If all pairs are of the 1st type: $a_1b_1a_1^{-1}b_1^{-1}\,a_2b_2a_2^{-1}b_2^{-1}\cdots a_nb_na_n^{-1}b_n^{-1}$, a connected sum $nT^2$.
2. If all pairs are of the 2nd type: $a_1a_1a_2a_2\cdots a_na_n$, a connected sum $n\mathbb{RP}^2$.
3. If both types occur, apply the lemma to keep only 2nd-type pairs. E.g.
   $$A\,\underbrace{a_1a_1\,a_2b_2a_2^{-1}b_2^{-1}}_{\mathbb{RP}^2 \# T^2}\,B \;\cong\; A\,\underbrace{a_1a_1a_2a_2a_3a_3}_{3\mathbb{RP}^2}\,B. \qquad\blacksquare$$

## 1.6 Orientation

On $\mathbb{R}^2$ there are 2 orientations: clockwise and counter-clockwise.

In general, orientations are defined as equivalence classes of bases:

$$
\{v_1,\dots,v_n\} \sim \{w_1,\dots,w_n\} \iff \text{the change of basis } L(v_i) = w_i \text{ has } \det L > 0.
$$

$\Rightarrow$ there are 2 orientations.

Consider a compact surface $S$ and a path on $S$. Choose coordinate systems along the curve in such a manner that the orientation does not change.

- $S$ is **non-orientable** if there exists a closed loop along which the orientation is reversed.
- $S$ is **orientable** if the orientation does not change along any closed loop.

| | |
|---|---|
| Orientable | $S^2,\ T^2,\ T^2 \# T^2$ |
| Non-orientable | $\mathrm{MB},\ \mathbb{RP}^2,\ K,\ \mathbb{RP}^2\#\mathbb{RP}^2\#\mathbb{RP}^2$ |

Using the formula for the Euler characteristic and the classification theorem:

> **Theorem.** Let $S_1, S_2$ be compact surfaces. Then $S_1 \cong S_2$ iff
> 1. $\chi(S_1) = \chi(S_2)$, and
> 2. they are both orientable or both non-orientable.

## 1.7 An application of the Euler characteristic

> **Theorem.** There are only 5 regular polyhedra (with 4, 6, 8, 12, 20 faces).

*Proof.* Subdivide $S^2$ into $n$-gons ($n \ge 3$) such that exactly $m$ edges ($m \ge 3$) meet at each vertex. Let $F, E, V$ be the numbers of faces, edges, vertices. Then

$$
E = \frac{mV}{2}, \qquad E = \frac{nF}{2} \quad\Rightarrow\quad V = \frac{n}{m}F.
$$

$$
2 = \chi(S^2) = F - E + V = F - \frac{n}{2}F + \frac{n}{m}F
\quad\Rightarrow\quad
F = \frac{4m}{2(m+n) - mn}.
$$

So $2(m+n) > mn$ with $m, n \ge 3$, and there are exactly 5 possibilities:

$$
(m,n) \in \{(3,3),\ (3,4),\ (4,3),\ (3,5),\ (5,3)\}. \qquad\blacksquare
$$

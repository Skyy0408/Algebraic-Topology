---
title: "Chapter 3. Free groups and free products"
---

# Chapter 3. Free groups and free products

Source: handwritten lecture notes of 2026-10-08 (Massey, Chapter III).

!!! note "Notation"
    $1_G$ is the identity *element* of a group $G$; when $G$ is abelian it is often
    written $0_G$, or simply $0$. As in Chapter 2, $i$ denotes an inclusion and
    $\iota$ an identity map.

## 3.1 Direct products of groups

Recall, from basic group theory, the direct product. Let $G_1, G_2$ be groups and let

$$
G_1\times G_2 = \{(g_1,g_2)\mid g_1\in G_1,\ g_2\in G_2\}
$$

be their Cartesian product. Define multiplication by

$$
(g_1,g_2)\cdot(g_1',g_2') = (g_1g_1',\ g_2g_2'),
$$

the first coordinate multiplied in $G_1$ and the second in $G_2$. Then
$(1_{G_1},1_{G_2})$ is the identity and $(g_1^{-1},g_2^{-1})$ is the inverse of
$(g_1,g_2)$. This makes $G_1\times G_2$ a group, called the *product group*.

**Alternative description.** $G_1\times G_2$ can be characterised by the set of
functions $f$ from $\{1,2\}$ to $G_1\cup G_2$ such that $f(1)\in G_1$ and
$f(2)\in G_2$; that is,

$$
G_1\times G_2 = \{\,f : f \text{ maps } \{1,2\} \text{ to } G_1\cup G_2,\ f(i)\in G_i\ \forall i\,\},
$$

with $(g_1,g_2)$ corresponding to the $f$ that maps $1$ to $g_1$ and $2$ to $g_2$.

This extends at once to finitely many groups:

$$
G_1\times\cdots\times G_n = \{(g_1,\dots,g_n) : g_i\in G_i\ \forall i\},\qquad
(g_1,\dots,g_n)\cdot(g_1',\dots,g_n') = (g_1g_1',\dots,g_ng_n'),
$$

or, in the function form, $G_1\times\cdots\times G_n = \{\,f : f(i)\in G_i,\ i=1,\dots,n\,\}$.
It is the description using functions that lets us extend the concept of a product
to an arbitrary collection of groups.

## 3.2 Arbitrary products and the weak product

Let $\{G_i\}_{i\in I}$ be a family of groups. Their *Cartesian product*, denoted
$\prod_{i\in I}G_i$, is the set of functions $f$ from $I$ to $\bigcup_{i\in I}G_i$
such that $f(i)\in G_i$ for all $i\in I$. Elements are written $(g_i)_{i\in I}$, and

$$
(g_i)_{i\in I}\cdot(g_i')_{i\in I} := (g_i\,g_i')_{i\in I}.
$$

This makes $\prod_{i\in I}G_i$ a group, called the *product group* of
$\{G_i\}_{i\in I}$, or the *direct product*.

> **Definition.** The *weak product* of $\{G_i\}_{i\in I}$ is the subgroup of
> $\prod_{i\in I}G_i$ consisting of those $(g_i)_{i\in I}$ with $g_i = 1_{G_i}$ for
> all but finitely many $i$. It is denoted $\prod^{\mathrm{wk}}_{i\in I}G_i$.

Clearly it is a subgroup.

> **Remark.** If $I$ is finite then $\prod^{\mathrm{wk}}_{i\in I}G_i = \prod_{i\in I}G_i$.
> If every $G_i$ is abelian then $\prod^{\mathrm{wk}}_{i\in I}G_i \cong \bigoplus_{i\in I}G_i$,
> the *direct sum* of $\{G_i\}_{i\in I}$.

<video class="anim" src="assets/animations/WeakProductSupport.mp4" controls loop muted autoplay playsinline></video>

The top row is a general element of the full product: every coordinate is free. The bottom row is the weak product, where all but finitely many coordinates are the identity. Taking every $G_i=\mathbb{Z}$ turns the same picture into $\mathbb{Z}\langle S\rangle$ and its basis $\{\varphi_s\}$ (§3.5).

For each $i\in I$ there is a natural homomorphism

$$
\varphi_i : G_i \longrightarrow \prod^{\mathrm{wk}}_{j\in I}G_j,
\qquad x \longmapsto \big((\varphi_i x)_j\big)_{j\in I},
\qquad
(\varphi_i x)_j =
\begin{cases}
x, & j = i,\\
0_{G_j}, & j \ne i.
\end{cases}
$$

## 3.3 Universality of the direct sum

> **Theorem 1 (universality of the direct sum).** Let $G$ be the weak product of
> abelian groups $\{G_i\}_{i\in I}$. Then for every abelian group $A$ and every
> family of homomorphisms $\psi_i : G_i \to A$ there is a unique homomorphism
> $f : G \to A$ making the diagram commute, i.e. $\psi_i = f\circ\varphi_i$ for all $i$.

*Proof.* Define $f : G = \bigoplus_{i\in I}G_i \to A$ by

$$
f\big((g_i)_{i\in I}\big) := \sum_{i\in I}\psi_i(g_i).
$$

This is well defined because the sum is finite and the groups are abelian, and
clearly $f$ is a homomorphism. Since $\psi_j(0_{G_j}) = 0$ for every $j\ne i$,

$$
f\circ\varphi_i(x) = f\big(\varphi_i(x)\big) = \sum_{j\in I}\psi_j\big((\varphi_i x)_j\big) = \psi_i(x)
\qquad \forall\,x\in G_i,\ \forall\,i\in I,
$$

so $f\circ\varphi_i = \psi_i$ for all $i\in I$.

Suppose a homomorphism $h : G\to A$ also satisfies $h\circ\varphi_i = \psi_i$ for all
$i\in I$. Then for every $(g_i)_{i\in I}\in G$,

$$
f\big((g_i)_{i\in I}\big) = \sum_{i\in I}\psi_i(g_i) = \sum_{i\in I}h\circ\varphi_i(g_i)
= h\Big(\sum_{i\in I}\varphi_i(g_i)\Big) = h\big((g_i)_{i\in I}\big),
$$

hence $f = h$. $\blacksquare$

<video class="anim" src="assets/animations/DirectSumUniversal.mp4" controls loop muted autoplay playsinline></video>

The maps $\psi_i$ out of the summands are the input; the dashed arrow is the one homomorphism $f$ they force. Only finitely many coordinates of an element of the direct sum are non-trivial, which is what makes the defining sum a legal finite sum.

> **Theorem 2 (uniqueness of the universality condition).** Let $G,\ G_i,\ \varphi_i$
> be as in Theorem 1. Suppose $G'$ is an abelian group equipped with homomorphisms
> $\varphi_i' : G_i\to G'$, $i\in I$, having the same universal property: for every
> abelian group $A$ and homomorphisms $\psi_i : G_i\to A$ there is a unique
> homomorphism $f' : G'\to A$ with $\psi_i = f'\circ\varphi_i'$ for all $i\in I$.
> Then there is a unique isomorphism $h : \bigoplus_{i\in I}G_i \to G'$ with
> $h\circ\varphi_i = \varphi_i'$ for all $i\in I$.

*Proof.* Apply Theorem 1 with $A = G'$ and the homomorphisms $\varphi_i'$: there is a
unique homomorphism $f : \bigoplus_{i\in I}G_i \to G'$ with $f\circ\varphi_i = \varphi_i'$.
Apply the hypothesis on $G'$ with $A = \bigoplus_{i\in I}G_i$ and the homomorphisms
$\varphi_i$: there is a unique homomorphism $f' : G' \to \bigoplus_{i\in I}G_i$ with
$f'\circ\varphi_i' = \varphi_i$. Then

$$
(f'\circ f)\circ\varphi_i = f'\circ\varphi_i' = \varphi_i \qquad \forall\,i\in I,
$$

and the identity map of $\bigoplus_{i\in I}G_i$ has the same property; by the
uniqueness clause of Theorem 1, $f'\circ f = \iota_{\bigoplus_{i\in I}G_i}$. Doing
the same thing on the other side gives $f\circ f' = \iota_{G'}$. Hence $f'$ is the
inverse of $f$, and $f$ is an isomorphism; take $h = f$. In particular
$G' \cong \bigoplus_{i\in I}G_i$. $\blacksquare$

## 3.4 Free abelian groups

> **Definition.** Let $S$ be an arbitrary set. A *free abelian group on* $S$ is an
> abelian group $F$ together with a function $\varphi : S\to F$ with the following
> universal property: for every abelian group $A$ and every function
> $\psi : S\to A$ there is a unique homomorphism $f : F\to A$ such that
> $\psi = f\circ\varphi$.

Note that $F \cong \bigoplus_{s\in S}G_s$ where $G_s = \mathbb{Z}$ for every $s\in S$;
this is proved below.

> **Theorem 3.** If $(F,\varphi)$ and $(F',\varphi')$ are free abelian groups on $S$,
> then $F\cong F'$.

*Proof.* The universal property of $(F,\varphi)$ applied to $\varphi' : S\to F'$ gives
a unique homomorphism $f : F\to F'$ with $f\circ\varphi = \varphi'$, and that of
$(F',\varphi')$ applied to $\varphi$ gives a unique $f' : F'\to F$ with
$f'\circ\varphi' = \varphi$. Then $f'\circ f : F\to F$ satisfies
$(f'\circ f)\circ\varphi = \varphi$, as does $\mathrm{id}_F$; by uniqueness
$f'\circ f = \mathrm{id}_F$. Symmetrically $f\circ f' = \mathrm{id}_{F'}$. Therefore
$F\cong F'$, with $f$ and $f'$ inverse to each other. $\blacksquare$

**Example.** $S = \{x\}$ and $F = \{x^n\mid n\in\mathbb{Z}\}$ with
$\varphi(x) = x^1\in F$ and multiplication $x^n\cdot x^m = x^{n+m}$. Given an abelian
group $A$ and $\psi : \{x\}\to A$, define $f : F\to A$ by $x^n\mapsto (\psi(x))^n$.
Then $f(\varphi(x)) = f(x) = \psi(x)$, and the choice of $f$ is unique, being
determined by the generating element: $F = \langle x\rangle$.

> **Theorem 4.** Let $S$ be a set and $\{S_i\}_{i\in I}$ a partition of $S$, i.e.
> $\bigcup_{i\in I}S_i = S$ as a disjoint union. If $(G_i, r_i)$ is a free abelian
> group on $S_i$ for every $i\in I$, then
> $G = \prod^{\mathrm{wk}}_{i\in I}G_i = \bigoplus_{i\in I}G_i$,
> together with $r : S\to G$ defined by $r|_{S_i} = \varphi_i\circ r_i$ (where
> $\varphi_i : G_i\to G$ is the natural homomorphism of §3.2), is a free abelian
> group on $S$.

*Proof.* Let $A$ be an abelian group and $\psi : S\to A$ a function, and put
$\psi_i = \psi|_{S_i}$. Since $(G_i,r_i)$ is a free abelian group on $S_i$, there is a
unique homomorphism $f_i : G_i\to A$ with $f_i\circ r_i = \psi_i$. 

$$
S_i \xrightarrow{\ r_i\ } G_i \xrightarrow{\ \varphi_i\ } G, \qquad
f_i\circ r_i = \psi_i. \tag{1}
$$

So for every $i\in I$ we have a group homomorphism $G_i\to A$, and by the
universality of the direct sum (Theorem 1) there is a unique homomorphism
$f : G\to A$ with $f\circ\varphi_i = f_i$ for all $i$. For $x\in S$ there is a unique
$i$ with $x\in S_i$, and then

$$
f\circ r(x) = f\circ r|_{S_i}(x) = f\circ\varphi_i\circ r_i(x) = f_i\circ r_i(x)
= \psi_i(x) = \psi(x),
$$

so $\psi = f\circ r$. Uniqueness of $f$ follows from the uniqueness in (1) together
with that in Theorem 1. $\blacksquare$

> **Corollary.** If $S$ has $n$ elements, then the free abelian group on $S$ is
> isomorphic to $\mathbb{Z}^n = \bigoplus_{i=1}^{n}\mathbb{Z}$.

More generally, writing $S = \bigcup_{x\in S}\{x\}$, the free abelian group on $S$
exists and is isomorphic to

$$
\prod^{\mathrm{wk}}_{x\in S}\{x^n : n\in\mathbb{Z}\}
\qquad\text{or}\qquad \bigoplus_{x\in S}\mathbb{Z}.
$$

## 3.5 The concrete model $\mathbb{Z}\langle S\rangle$

> **Remark.** Let $S$ be a set and put
> $$\mathbb{Z}\langle S\rangle = \{\,\varphi \mid \varphi \text{ maps } S \text{ to } \mathbb{Z},\ \varphi(x) = 0 \text{ for all but finitely many } x\,\}$$
> with addition $(\varphi_1+\varphi_2)(x) := \varphi_1(x)+\varphi_2(x)$. Then
> $\mathbb{Z}\langle S\rangle$ is an abelian group, and
> $\mathbb{Z}\langle S\rangle \cong \bigoplus_{x\in S}\mathbb{Z}$.

Given $s\in S$, define

$$
\varphi_s : S\to\mathbb{Z},\qquad
x \longmapsto
\begin{cases}
1, & x = s,\\
0, & \text{otherwise.}
\end{cases}
$$

Then for every $\varphi\in\mathbb{Z}\langle S\rangle$, writing $\varphi(s) = n_s$ (only
finitely many $n_s\ne 0$),

$$
\varphi = \sum_{s\in S}n_s\,\varphi_s,
\qquad\text{so}\qquad
\mathbb{Z}\langle S\rangle = \langle\, \varphi_s \mid s\in S \,\rangle .
$$

Given an abelian group $A$ and a map $\psi : S\to A$, define
$f : \mathbb{Z}\langle S\rangle\to A$ by

$$
f\Big(\sum_{s\in S}n_s\varphi_s\Big) = \sum_{s\in S}n_s\,\psi(s),
$$

which is well defined because the coefficients $n_s$ are uniquely determined by
$\varphi$. Then $f$ is a homomorphism, and writing
$\hat\varphi : S\to\mathbb{Z}\langle S\rangle$, $s\mapsto\varphi_s$, we get

$$
(f\circ\hat\varphi)(s) = f(\hat\varphi(s)) = f(\varphi_s) = \psi(s),
\qquad\text{i.e.}\qquad \psi = f\circ\hat\varphi .
$$

So $(\mathbb{Z}\langle S\rangle,\hat\varphi)$ is a free abelian group on $S$, and by
Theorem 3 it is *the* free abelian group on $S$ up to isomorphism:
$F \cong \mathbb{Z}\langle S\rangle$.

## 3.6 Relations, torsion, and finitely generated abelian groups

Nontrivial elements of $\ker f$ correspond to "nontrivial relations" in $A$. For
example, $\mathbb{Z}_p$ is the group with generator $\{x\}$ subject to the relation
$x^p = 1$, i.e. $\mathbb{Z}/p\mathbb{Z}$.

If $G$ is a free abelian group on $k$ elements, then $G\cong\mathbb{Z}^k$.

!!! warning "Corrected while transcribing"
    The handwritten line reads "free group on $k$ elements"; it must be free
    **abelian**, as in Massey §III.3 (Lemma 3.4 and the discussion of rank). The
    free *group* on $k$ generators is nonabelian for $k\ge 2$; what is isomorphic to
    $\mathbb{Z}^k$ is its abelianisation — exactly the last remark of §3.8 below.

Let $G$ be abelian. The set

$$
T = \{\,g\in G : g^n = 1 \text{ for some } n\,\}
$$

is a subgroup, the *torsion subgroup* of $G$, and $G/T$ is free abelian. If $G$ is
finitely generated, then

$$
G \cong G/T \times T \cong
\underbrace{\mathbb{Z}\oplus\cdots\oplus\mathbb{Z}}_{\text{rank}}
\oplus\ \mathbb{Z}_{n_1}\oplus\cdots\oplus\mathbb{Z}_{n_k},
$$

the *fundamental theorem of finitely generated abelian groups* (Massey, Theorem 3.6).

## 3.7 Free products

> **Definition.** Let $\{G_i\}_{i\in I}$ be a collection of groups and, for each $i$,
> let $\varphi_i : G_i\to G$ be a homomorphism of groups. We say $G$ is the
> *free product* (or *coproduct*) of $\{G_i\}_{i\in I}$ with respect to
> $\{\varphi_i\}_{i\in I}$ if the following universal property holds: for every group
> $H$ and homomorphisms $\psi_i : G_i\to H$ there is a unique homomorphism
> $f : G\to H$ such that $\psi_i = f\circ\varphi_i$ for all $i\in I$.

This is word for word the universal property of Theorem 1 with the word "abelian"
deleted everywhere.

> **Theorem 5.** If $G$ and $G'$ are both free products of $\{G_i\}_{i\in I}$ with
> respect to $\{\varphi_i\}_{i\in I}$, then $G\cong G'$.

*Proof.* The same argument as in Theorems 2 and 3. $\blacksquare$

**Notation.** The free product of $\{G_i\}_{i\in I}$ is denoted
$\prod^{*}_{i\in I}G_i$, and the free product of $G_1,G_2$ is written $G_1 * G_2$.
As with the direct sum, this notation suppresses the family
$\{\varphi_i\}_{i\in I}$, which is part of the data.

## 3.8 Free groups

> **Definition.** Let $S$ be an arbitrary set. A *free group on* $S$ is a group $F$
> (**not** necessarily abelian) together with a function $\varphi : S\to F$ with the
> following universal property: for every group $H$ and every function
> $\psi : S\to H$ there is a unique homomorphism $f : F\to H$ such that
> $\psi = f\circ\varphi$.

> **Theorem 6.** If $F$ and $F'$ are free groups on $S$, then $F\cong F'$.

> **Remark (free groups versus free abelian groups on $S$).** Let $F$ be the free
> group on $S$ and let $[F,F]$ be its *commutator subgroup*, i.e. the subgroup
> generated by $\{aba^{-1}b^{-1}\}$. Then
> $F\big/[F,F] \cong \mathbb{Z}\langle S\rangle$,
> the free abelian group on $S$.

---
title: "Chapter 5. Covering spaces"
---

# Chapter 5. Covering spaces

Source: lecture notes provided by the instructor (week of 2026-11-05; Massey, Chapter V).

!!! note "Standing assumptions"
    As in Massey, Chapter V, all spaces $X$ and $\tilde X$ below are tacitly
    pathwise connected and locally pathwise connected. Theorems 3 and 4 need this.

## 5.1 Definition and examples

> **Definition.** Let $X$ be a topological space. A *covering space* of $X$ is a
> pair $(\tilde X,p)$ such that
>
> 1. $p:\tilde X\to X$ is continuous (called the *projection*);
> 2. $\forall x\in X$ there is a neighborhood $U$ of $x$ such that each component of
>    $p^{-1}(U)$ is mapped homeomorphically onto $U$ by $p$ (in particular, $p$ is a
>    local homeomorphism).
>
> Neighborhoods $U$ of this form are called *elementary neighborhoods*.

So $p^{-1}(U)$ is a disjoint union of copies of $U$ ("sheets").

**Goal.** Understand $X$ and $\pi(X)$ through $(\tilde X,p)$.

**Example 1 (trivial example).** If $p:Y\to X$ is a homeomorphism, then $(Y,p)$ is a
covering space of $X$.

**Example 2.** Let $p:\mathbb{R}\to S^1$,

$$
p(t)=(\cos t,\sin t)\quad(S^1\subseteq\mathbb{R}^2),\qquad\text{or}\qquad p(t)=e^{it}\quad(S^1\subseteq\mathbb{C}).
$$

Then $(\mathbb{R}^1,p)$ is a covering space of $S^1$. For a small arc $U\ni x$,
$p^{-1}(U)$ is a disjoint union of open intervals, one in each period.

<video class="anim" src="assets/animations/HelixLifting.mp4" controls loop muted autoplay playsinline></video>

**Example 3.** Given $n\in\mathbb{N}$, let $p:S^1\to S^1$,
$p(e^{it})=e^{int}$ (or $p(z)=z^n$). Then $(S^1,p)$ is a covering space of $S^1$:
the circle wraps $n$ times around itself.

**Example 4.** Let $p:S^2\to\mathbb{RP}^2=S^2/\!\sim$, $x\sim-x$, be the quotient map
$p(x)=\{x,-x\}$. Then $(S^2,p)$ is a covering space of $\mathbb{RP}^2$.

**Example 5.** If $(\tilde X,p)$ is a covering space of $X$ and $(\tilde Y,q)$ is a
covering space of $Y$, then $(\tilde X\times\tilde Y,\ p\times q)$ is a covering space
of $X\times Y$ (use products $U\times V$ of elementary neighborhoods). In particular,
with Examples 2 and 3 we get many covering spaces of $S^1\times S^1=T^2$:
$\mathbb{R}\times\mathbb{R}$, $\mathbb{R}\times S^1$, $S^1\times S^1$.

**Example 6 (the figure eight).** Let $X$ be the 8-shaped curve, denoted
$S^1\vee S^1$ ("$S^1$ wedge $S^1$"). We may define $X=C_1\cup C_2$,

$$
C_1=\{(x,y):(x-1)^2+y^2=1\},\qquad C_2=\{(x,y):(x+1)^2+y^2=1\}.
$$

① **The grid.** $\tilde X=(\mathbb{Z}\times\mathbb{R})\cup(\mathbb{R}\times\mathbb{Z})$,

$$
p(x,y)=\begin{cases}
\big(1+\cos(\pi-2\pi x),\ \sin 2\pi x\big), & y\in\mathbb{Z},\\[2pt]
\big(-1+\cos 2\pi y,\ \sin 2\pi y\big), & x\in\mathbb{Z}.
\end{cases}
$$

Horizontal lines wrap around $C_1$, vertical lines around $C_2$.

② **A line with circles attached.** $\tilde X=L\cup\big(\bigcup_{n\in\mathbb{Z}}D_n\big)$,
where $L$ is the $y$-axis and $D_n=\{(x,y):(x-1)^2+(y-3n)^2=1\}$,

$$
p(x,y)=\begin{cases}
(x,\ y-3n), & (x,y)\in D_n,\\[2pt]
\big(-1+\cos\tfrac{2\pi y}{3},\ \sin\tfrac{2\pi y}{3}\big), & (x,y)\in L.
\end{cases}
$$

③ **The tree** (a fractal picture). Label the four directions of the figure eight at
the wedge point $1,2,3,4$ (two along each circle, one in each sense). Starting from
one vertex, draw four edges labelled $1,2,3,4$ (up, down, left, right); at the end of
each edge draw the edges in the three other directions with half the length, and so
on. Mapping each edge once around the corresponding circle gives a covering
$p:\tilde X\to X$. This $\tilde X$ is the Cayley graph of the free group on two
generators (§3.9); it is a tree, hence simply connected, i.e. the universal covering
of $S^1\vee S^1$.

## 5.2 Lifting of paths

> **Definition.** Let $(\tilde X,p)$ be a covering space of $X$, $p(\tilde x_0)=x_0$,
> and let $\alpha:I\to X$ be a path with initial point $x_0$. A path
> $\tilde\alpha:I\to\tilde X$ is a *lifting* of $\alpha$ with initial point
> $\tilde x_0$ if
>
> $$
> \tilde\alpha(0)=\tilde x_0\qquad\text{and}\qquad p\circ\tilde\alpha=\alpha .
> $$

> **Lemma (existence and uniqueness of liftings).** $\forall x_0\in X$,
> $\forall\tilde x_0\in p^{-1}(x_0)$, and every path $\alpha$ in $X$ with initial point
> $x_0$, there exists a unique lifting $\tilde\alpha$ of $\alpha$ with initial point
> $\tilde x_0$.

*Proof.* **Existence.** Cover $\alpha(I)$ by elementary neighborhoods $\{U_i\}$; then
$\{\alpha^{-1}(U_i)\}$ covers $I$. Choose $n$ so large that
$\tfrac1n<$ the Lebesgue number of $\{\alpha^{-1}(U_i)\}$, and subdivide $I$ into
$[0,\tfrac1n],[\tfrac1n,\tfrac2n],\dots,[\tfrac{n-1}n,1]$. Each subinterval is mapped
by $\alpha$ into an elementary neighborhood. Define $\tilde\alpha$ on
$[0,\tfrac1n]$ as the unique path starting from $\tilde x_0$ with
$p\circ\tilde\alpha=\alpha$ (go back through the sheet containing $\tilde x_0$); then
define $\tilde\alpha$ on $[\tfrac1n,\tfrac2n]$ as the unique path starting from
$\tilde\alpha(\tfrac1n)$ with $p\circ\tilde\alpha=\alpha$, and so on.

**Uniqueness.** Let $\tilde\alpha,\hat\alpha$ be two liftings with the same initial
point. The set $\{t\in I:\tilde\alpha(t)=\hat\alpha(t)\}$ is nonempty and both open
and closed, so it is all of $I$, i.e. $\tilde\alpha\equiv\hat\alpha$. (Open: if
$\tilde\alpha(t)=\hat\alpha(t)$, both lie in the same sheet over an elementary
neighborhood of $\alpha(t)$ near $t$, and $p$ is injective on that sheet, so
$\tilde\alpha=\hat\alpha$ near $t$. Closed: if $\tilde\alpha(t)\ne\hat\alpha(t)$, they
lie in different, disjoint sheets, so they differ near $t$.) $\blacksquare$

> **Lemma (covering homotopy property).** Let $\tilde\alpha_0,\tilde\alpha_1:I\to\tilde X$
> be paths with the same initial point. If $p\circ\tilde\alpha_0\sim p\circ\tilde\alpha_1$,
> then $\tilde\alpha_0\sim\tilde\alpha_1$. Here "$\sim$" means homotopic relative to
> $\{0,1\}$.

*Idea of proof.* Begin with the homotopy $F:I\times I\to X$,

$$
F(s,0)=p\circ\tilde\alpha_0(s),\quad F(s,1)=p\circ\tilde\alpha_1(s),\quad
F(0,t)=p\circ\tilde\alpha_0(0)=p(\tilde x_0),\quad F(1,t)=p\circ\tilde\alpha_0(1).
$$

Cut $I$ into small subintervals $J_i=[\tfrac in,\tfrac{i+1}n]$ such that each
$F(J_i\times J_j)$ lies in an elementary neighborhood. Then "lift" the homotopy to
$G:I\times I\to\tilde X$ by successive extension over
$J_1\times J_1,\ J_1\times J_2,\ J_2\times J_1,\ \dots$. (The edges $\{0\}\times I$
and $\{1\}\times I$ are mapped to points, so their lifts are constant, which gives
$\tilde\alpha_0\sim\tilde\alpha_1$ rel $\{0,1\}$.)

In particular, the lift of a loop $\alpha$ need **not** be a loop; whether it closes
up depends only on the class $[\alpha]$:

<video class="anim" src="assets/animations/LiftGridTree.mp4" controls loop muted autoplay playsinline></video>

## 5.3 The subgroup $p_*\pi(\tilde X,\tilde x_0)$

The covering homotopy property implies immediately:

> **Theorem 1.** Let $(\tilde X,p)$ be a covering space of $X$, $p(\tilde x_0)=x_0$.
> Then the induced homomorphism $p_*:\pi(\tilde X,\tilde x_0)\to\pi(X,x_0)$ is $1$–$1$.

(If $p_*[\tilde\alpha]=1$, then $p\circ\tilde\alpha\sim\varepsilon_{x_0}=p\circ\varepsilon_{\tilde x_0}$,
so $\tilde\alpha\sim\varepsilon_{\tilde x_0}$.)

**Changing the point in the fiber.** Given $\tilde x_0,\tilde x_1\in p^{-1}(x_0)$,
choose a path $\gamma$ from $\tilde x_0$ to $\tilde x_1$. For a loop $\alpha$ at
$\tilde x_0$ and a loop $\beta$ at $x_0$ put

$$
u(\alpha):=\gamma^{-1}\alpha\gamma\ \ (\text{a loop at }\tilde x_1),\qquad
v(\beta):=(p\gamma)^{-1}\beta\,(p\gamma)\ \ (\text{a loop at }x_0),
$$

where $p\gamma$ is a loop at $x_0$. The diagram

$$
\begin{array}{ccc}
\pi(\tilde X,\tilde x_0) & \xrightarrow{\ p_*\ } & \pi(X,x_0)\\[2pt]
\big\downarrow{\scriptstyle u_*} & & \big\downarrow{\scriptstyle v_*}\\[2pt]
\pi(\tilde X,\tilde x_1) & \xrightarrow{\ p_*\ } & \pi(X,x_0)
\end{array}
$$

commutes. Still using $\alpha,\beta,\gamma$ for their homotopy classes,

$$
p_*(\gamma^{-1}\alpha\gamma)=(p_*\gamma)^{-1}(p_*\alpha)(p_*\gamma),
$$

so $p_*\pi(\tilde X,\tilde x_0)$ and $p_*\pi(\tilde X,\tilde x_1)$ are conjugate
subgroups of $\pi(X,x_0)$.

> **Theorem 2.** The subgroups $p_*\pi(\tilde X,\tilde x)$ for
> $\tilde x\in p^{-1}(x_0)$ form a conjugacy class of subgroups of $\pi(X,x_0)$.

## 5.4 Homomorphisms of covering spaces

> **Definition.** Given two covering spaces $(\tilde X_1,p_1)$, $(\tilde X_2,p_2)$ of $X$,
> a map $\varphi:\tilde X_1\to\tilde X_2$ is a *homomorphism* from $(\tilde X_1,p_1)$
> to $(\tilde X_2,p_2)$ if $p_1=p_2\circ\varphi$, i.e. the triangle
>
> $$
> \begin{array}{ccc}
> \tilde X_1 & \xrightarrow{\ \varphi\ } & \tilde X_2\\
> & {\scriptstyle p_1}\searrow\quad\swarrow{\scriptstyle p_2} &\\
> & X &
> \end{array}
> $$
>
> commutes. $(\tilde X_1,p_1)$ and $(\tilde X_2,p_2)$ are *isomorphic* if there is a
> homeomorphism $h:\tilde X_1\to\tilde X_2$ with $p_1=p_2\circ h$; $h$ is called an
> *isomorphism*. Isomorphisms from $(\tilde X,p)$ to itself are called
> *automorphisms*, or *covering transformations*. The set of automorphisms is denoted
> $A(\tilde X,p)$ or $\operatorname{Aut}(\tilde X,p)$; clearly it is a group under
> composition.

**Example.** $p:S^2\to\mathbb{RP}^2=S^2/\{x\sim-x\}$. The automorphisms are
$\varphi(x)=x$ and $\varphi(x)=-x$, so

$$
\operatorname{Aut}(S^2,p)\cong\mathbb{Z}_2\cong\pi(\mathbb{RP}^2).
$$

> **Theorem 3.** Covering spaces $(\tilde X_1,p_1)$, $(\tilde X_2,p_2)$ of $X$ are
> isomorphic if and only if, for $x_0\in X$, $\tilde x_1\in p_1^{-1}(x_0)$,
> $\tilde x_2\in p_2^{-1}(x_0)$, the subgroups $p_{1*}\pi(\tilde X_1,\tilde x_1)$ and
> $p_{2*}\pi(\tilde X_2,\tilde x_2)$ are in the same conjugacy class in $\pi(X,x_0)$.

**Special case.** If $\tilde X_1,\tilde X_2$ are simply connected, they are called
*universal coverings*; then $(\tilde X_1,p_1)$ and $(\tilde X_2,p_2)$ are isomorphic
(both subgroups are $\{1\}$). This is the *uniqueness of the universal covering*.

**From Theorems 2 and 3:** the conjugacy class of subgroups
$p_*\pi(\tilde X,\tilde x)$ completely determines $(\tilde X,p)$ up to isomorphism.

## 5.5 Automorphisms and regular coverings

**Q.** What is the relation between $\operatorname{Aut}(\tilde X,p)$ and
$p_*\pi(\tilde X,\tilde x)$?

Recall: for a subgroup $H\subseteq G$, the *normalizer* of $H$ is

$$
N(H)=\{g\in G: gHg^{-1}=H\}\subseteq G,
$$

and $H\subseteq N(H)$ with $H\trianglelefteq N(H)$ ($H$ is a normal subgroup of $N(H)$).

> **Theorem 4.** Let $(\tilde X,p)$ be a covering space of $X$ and
> $\tilde x\in p^{-1}(x)$. Then
>
> $$
> \operatorname{Aut}(\tilde X,p)\cong N\big(p_*\pi(\tilde X,\tilde x)\big)\big/p_*\pi(\tilde X,\tilde x).
> $$
>
> In particular, if $(\tilde X,p)$ is a universal cover, then
> $\operatorname{Aut}(\tilde X,p)\cong\pi(X,x)$.

> **Definition.** $(\tilde X,p)$ is a *regular covering space* of $X$ if
> $p_*\pi(\tilde X,\tilde x)$ is normal in $\pi(X,x)$.

Then $N(p_*\pi)=\pi(X,x)$ and Theorem 4 reads
$\operatorname{Aut}(\tilde X,p)\cong\pi(X,x)/p_*\pi(\tilde X,\tilde x)$.

**Q.** How do we determine whether $(\tilde X,p)$ is regular?
**A.** If $\operatorname{Aut}(\tilde X,p)$ "acts transitively" on $p^{-1}(x)$.

> **Definition.** A *right action* of a group $G$ on a set $S$ is a map
> $S\times G\to S$, $(s,g)\mapsto s\cdot g$, such that
>
> $$
> s\cdot(g_1g_2)=(s\cdot g_1)\cdot g_2\quad\forall s\in S,\ \forall g_1,g_2\in G,
> \qquad s\cdot1=s .
> $$
>
> $S$ is then a *right $G$-space*. The definition of a left action is similar.

**Examples.**

1. $S=\mathbb{R}$, $G=\mathbb{Z}$: $x\cdot n:=x+n$ for $x\in\mathbb{R}$, $n\in\mathbb{Z}$.
2. $S=S^2$, $G=\mathbb{Z}_2=\{\pm1\}$: $x\cdot1=x$, $x\cdot(-1)=-x$.
3. $S=\mathbb{R}^n$, $G=O(n)$: $G$ acts on $S$ by $x\mapsto Mx$ (a left action).
4. $S=p^{-1}(x)$, $G=\pi(X,x)$: for $\tilde x\in p^{-1}(x)$ and $\alpha\in G$,
   $\tilde x\cdot\alpha:=$ the terminal point of $\tilde\alpha$, where $\tilde\alpha$
   is the lift of $\alpha$ with initial point $\tilde x$. (Well defined on classes by
   the covering homotopy property; the animation in §5.2 shows $\tilde x\cdot\alpha$
   for $\alpha=aba^{-1}b^{-1}$ in two coverings.)

**Fact.** $\forall\varphi\in\operatorname{Aut}(\tilde X,p)$,
$\varphi(\tilde x\cdot\alpha)=(\varphi\tilde x)\cdot\alpha$. Hence $\varphi$ induces a
natural automorphism of $p^{-1}(x)$ as a right $\pi(X,x)$-space.

> **Definition.** A (right) action is *transitive* if $\forall x,y\in S$
> $\exists g\in G$ such that $x\cdot g=y$.

## 5.6 The Borsuk–Ulam theorem

> **Borsuk–Ulam Theorem.** There is no continuous $f:S^2\to S^1$ with
> $f(-x)=-f(x)$ (antipode-preserving).

*Proof.* Suppose such an $f$ exists. Since $f$ commutes with the antipodal maps, it
induces $g:\mathbb{RP}^2\to\mathbb{RP}^1=S^1$ with $g\circ p_2=p_1\circ f$:

$$
\begin{array}{ccc}
S^2 & \xrightarrow{\ f\ } & S^1\\[2pt]
\big\downarrow{\scriptstyle p_2} & & \big\downarrow{\scriptstyle p_1}\\[2pt]
\mathbb{RP}^2 & \xrightarrow{\ g\ } & \mathbb{RP}^1=S^1
\end{array}
\qquad\quad
\begin{array}{ccc}
\{1\}=\pi(S^2) & \xrightarrow{\ f_*=0\ } & \pi(S^1)=\mathbb{Z}\\[2pt]
\big\downarrow{\scriptstyle p_{2*}} & & \big\downarrow{\scriptstyle p_{1*}\,=\,\times2}\\[2pt]
\mathbb{Z}_2=\pi(\mathbb{RP}^2) & \xrightarrow{\ g_*\ } & \pi(S^1)=\mathbb{Z}
\end{array}
$$

Here $p_1$ wraps around twice, and $g_*\equiv0$ because there is no nonzero
homomorphism $\mathbb{Z}_2\to\mathbb{Z}$.

Let $\alpha$ be a path on $S^2$ from the north pole $N$ to the south pole $S=-N$. Then
$p_2\circ\alpha$ is a loop in $\mathbb{RP}^2$, and $f\circ\alpha$ is a path in $S^1$
from $f(N)$ to $f(S)=-f(N)$, so $p_1\circ f\circ\alpha$ is a loop in $S^1$. Both are
nontrivial:

$$
0\ne[p_2\circ\alpha]\in\pi(\mathbb{RP}^2)=\mathbb{Z}_2,\qquad
0\ne[p_1\circ f\circ\alpha]\in\pi(S^1)=\mathbb{Z}
$$

(each lifts to a path with distinct endpoints, so by the covering homotopy property it
is not equivalent to a constant loop). But

$$
0=g_*[p_2\circ\alpha]=[g\circ p_2\circ\alpha]=[p_1\circ f\circ\alpha]\ne0,
$$

a contradiction. $\blacksquare$

<video class="anim" src="assets/animations/BorsukUlamDoubling.mp4" controls loop muted autoplay playsinline></video>

**Remark.** General version: the same conclusion holds for $f:S^n\to S^{n-1}$.

> **Corollary.** If $f:S^n\to\mathbb{R}^n$ is continuous and $f(-x)=-f(x)$
> $\forall x\in S^n$, then $\exists x\in S^n$ such that $f(x)=0$.

*Proof.* If not, define $g(x)=\dfrac{f(x)}{\|f(x)\|}\in S^{n-1}$. Then
$g(-x)=-g(x)$ $\forall x$, contradicting the Borsuk–Ulam theorem. $\blacksquare$

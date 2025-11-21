# Category Theory: Commutative Diagrams

## Basic Commutative Square

Consider the following commutative diagram:

$$
\begin{tikzcd}
A \arrow[r, "f"] \arrow[d, "g"'] & B \arrow[d, "h"] \\
C \arrow[r, "k"'] & D
\end{tikzcd}
$$

This diagram commutes if $h \circ f = k \circ g$.

## Functors Between Categories

A functor $F: \mathcal{C} \to \mathcal{D}$ preserves composition:

$$
\begin{tikzcd}
X \arrow[r, "f"] \arrow[dr, "g \circ f"'] & Y \arrow[d, "g"] \\
& Z
\end{tikzcd}
$$

## Natural Transformation

Given functors $F, G: \mathcal{C} \to \mathcal{D}$, a natural transformation $\eta: F \Rightarrow G$ satisfies:

$$
\begin{tikzcd}
F(X) \arrow[r, "\eta_X"] \arrow[d, "F(f)"'] & G(X) \arrow[d, "G(f)"] \\
F(Y) \arrow[r, "\eta_Y"'] & G(Y)
\end{tikzcd}
$$

## Pullback Square

The pullback of $f: X \to Z$ and $g: Y \to Z$ is:

$$
\begin{tikzcd}
P \arrow[r, "p_2"] \arrow[d, "p_1"'] \arrow[dr, phantom, "\lrcorner", very near start] & Y \arrow[d, "g"] \\
X \arrow[r, "f"'] & Z
\end{tikzcd}
$$

## Complex Diagram

The snake lemma:

$$
\begin{tikzcd}
& A \arrow[r, "f"] \arrow[d, "\alpha"] & B \arrow[r, "g"] \arrow[d, "\beta"] & C \arrow[r] \arrow[d, "\gamma"] & 0 \\
0 \arrow[r] & A' \arrow[r, "f'"'] & B' \arrow[r, "g'"'] & C'
\end{tikzcd}
$$

In category theory, we often work with such diagrams where morphisms $f, g, \alpha, \beta, \gamma$ satisfy certain properties.

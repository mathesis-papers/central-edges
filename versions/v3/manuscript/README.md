# Central edges, minimum orders and binary-tree corollaries

**Haobo Ma** — ChronoAI Pte Ltd, Singapore  
**Wenlin Zhang** — National University of Singapore; ChronoAI Pte Ltd, Singapore

License: Creative Commons Attribution 4.0 International (CC BY 4.0).

## Contents

- `note.tex`: self-contained mathematical note and bibliography.
- `note.pdf`: typeset note, supplied separately from the source archive.
- `verify.py`: exact-arithmetic finite checks, using the Python 3 standard library.
- `checks.json`: expected output of `verify.py`.
- `metadata.json`: title, authors, license, problem identifier and mathematical coverage.
- `LICENSE.txt`: license information.
- `source-member-manifest.json`: byte sizes and SHA256 hashes of the source files.

## Mathematical results

The note refutes Conjecture 4.2 of Dovgoshey and Rovenska,
arXiv:2610.11596v1, Section 4, p. 13: a four-point ultrametric satisfying
(i) has six central edges, while the real metric on {0,4,5,9} has four.
It proves the sharp three-central edge minima for every order n >= 4:

- Over all metrics: `2 ceil(n/2)`.
- Over ultrametrics: `2n - 4 + ceil(n/2)`.

It also corrects Conjecture 4.1 (the admissible orders are 1 and all even
positive integers) and answers Problem 4.3: the smallest order with a center
of size k is 1 for k=1, k for even k, and k+1 for odd k >= 3.
All these statements have complete written proofs in the note.

Earlier counterexamples to Conjecture 4.1 are credited to Jonathan Love's
2023 unique-distance constructions and Bargetz, Bartoš, Kubiś and Luggin's
2024 six-point example (arXiv:2305.03163v2, Example 3.11 and Figure 3).
The complete corrected order classification is stated separately.

The fixed-center extension gives `(k-1) ceil(n/2)` central edges at every
feasible pair with `n >= 3`: `1 <= k <= n` for even n and
`1 <= k <= n-1` for odd n. A near-perfect-matching construction attains
the odd-order bound. The nonempty equality graphs are perfect matchings
in even order and `P3` together with `(n-3)/2` disjoint edges in odd order.
The packing ingredients have classical antecedents in Harary's
one-factorization theorem (1969) and Andersen's cover-index criterion (1979).

The ultrametric minimum-order theorem is due to Dovgoshey and Rovenska
(26 March 2026), arXiv:2603.25850v1, Corollary 3.12 and Example 3.13.
The homogeneous-tree characterization is due to Evgeniy A. Petrov
(2022), Journal of Mathematical Sciences 264, 423–440,
doi:10.1007/s10958-022-06009-1; the author version is
arXiv:2412.17421v1 (23 December 2024), Theorem 2.2. The corresponding
tree assertion is reproved, with that prior proof credited explicitly.
The perfect-binary-tree classification is due to Dovgoshey, Jaiswal,
Kainth, Kaur and Rovenska (10 September 2026), arXiv:2609.11384v1,
Theorem 4.1. Both are cited as prior results. The note derives the short
group and sphere-count corollaries corresponding to Conjectures 5.1,
5.2, 5.5 and 5.6 and Problem 5.3 in the latter paper. Its Problem 5.4
is answered for homogeneous ultrametrics by partial-sum divisibility;
the unrestricted case is not covered. The coverage table distinguishes
these consequences from the central-edge bounds.

The binary group recursion specializes the classical rooted-tree
wreath-product formula described by Ceccherini-Silberstein et al. (2009).
The homogeneous sphere-count condition is the finite branching description
of Delhommé et al., arXiv:1509.04346v2 (2016), written in sphere counts.
Additional proofs of prescribed centers and extremal rigidity appear in
Korea Superintelligence Labs, *The center of distances of a finite ultrametric
space: centered spheres, prescribed centers, and extremal rigidity*, version 1:
https://ideosphere.ai/papers/ultra-center-log2-v1.pdf .

The source is https://arxiv.org/abs/2610.11596v1.
The pinned Lean declaration
`D5.S3.Combinatorics.Geometry.DovgosheyRovenskaCentralEdges.result`
states the negation of Conjecture 4.2 through the four-point examples:

https://github.com/the-omega-institute/trureturing/blob/8aa554ef66d0c1970b81b49632cd8a73a09ee34f/D5/S3/Combinatorics/Geometry/DovgosheyRovenskaCentralEdges.lean

That declaration covers the four-point refutation. The all-order edge bounds,
matching constructions and companion statements are written proofs in the
note. The tree corollaries use the cited perfect-binary-tree classification.

## Build the PDF

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, with a standard LaTeX installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is embedded in `note.tex`; no BibTeX step or external source
files are required. A first Tectonic compilation needs its ordinary TeX bundle.

## Reproduce the finite checks

```sh
python3 verify.py > checks-generated.json
cmp checks.json checks-generated.json
```

The output contains `"status": "ALL_CHECKS_OK"`. The checker verifies the
four-point examples; the condition-(i), optimal-metric and optimal-ultrametric
families at each order 4 through 32; minimum-order matching constructions for
each center size 1 through 24; and every symmetric distance table on 2, 3 and
4 vertices whose off-diagonal entries are in {1,2,3}. It checks every triangle,
computes each center as the intersection of row-distance sets, counts unordered
central edges, and checks the prescribed partitions and stars. These finite
calculations support the constructions; the unbounded statements follow from
the written proofs, not from a finite extrapolation.

Additional checks cover all 198 feasible `(n,k)` pairs for `3 <= n <= 20`,
binary sphere counts through height five, all isometries of the binary
examples through height three, and all isometries of five regular examples
with branching `(3)`, `(4)`, `(2,3)`, `(3,2)` and `(2,2,2)`.

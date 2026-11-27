# Sources

## Code

| Name | Repository | Version | Role |
|---|---|---|---|
| A (original) | `CocoSgt/riemann-hypothesis-lean` (mirror of L. Alpöge's archive) | `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4` | Primary source of the findings |
| A, community copy | `leanprover-community/riemann-hypothesis`, branch `original` | `40e56bab` | Agrees with the mirror on 174,793 `.lean` files (same paths and hashes) |
| S (shortened proof) | `lsernau/grh-lean` (L. Sernau) | `72fead1` | Used only for comparison |

## Dependency dataset

J. Shore, `rh-proof-dependencies` v0.2.1, `cone-decls.txt.gz`: 804,912 names of project declarations used by the kernel proof terms of the five final theorems.
- SHA-256 `b0c968a99cd89ab1aa8db9d4af2f69722810903181d6f6094553e3420b02f297`, published in the repository's `SHA256SUMS` (commit `70fbb2fc`).
- Downloaded by `verify/verify.py` from the v0.2.1 release; see `verify/sources.json`.

## Third-party certifications (not replicated by us)

- Archive A: the final theorem is Mathlib's `RiemannHypothesis` and uses only the three standard axioms. Source: joint statement by Lean FRO and the Mathlib Initiative, 21 Nov 2026, as reported by others. We have not consulted it ourselves.
- Shortened proof S: independent build and kernel checks reported at `math.mit.edu/~drew/shortgrh/` (A. Sutherland) and `mrubinst.github.io/grh-lean-compact-check/` (M. Rubinstein). Reported by others; we have not consulted these pages directly.

## Expositions and notes (all declare some AI assistance)

- M. Rubinstein, *The Alpöge–Claude proof of the Riemann hypothesis explained for the Riemann zeta function*, v2, 22 Nov 2026.
- R. Zhang, *A preliminary note on Alpöge's proposed proof of the generalized Riemann hypothesis*, hexagon:2611.00809v2.
- C. Huang, *An Arakelov-theoretic perspective on the Alpöge–Claude argument on RH, after Calegari–Dimitrov–Tang*, hexagon:2611.00833 (platform v1, 23 Nov 2026; PDF stamped v3).
- H. Nashida, *What does the main inequality (⋆) assert?*, r8, 27 Nov 2026, CC BY 4.0, https://zenodo.org/records/24575852.
- A. Brenner, *The Riemann Hypothesis via Multiplicity Chains: An Exposition and Lean 4 Companion to the Alpöge–Claude Proof*, 27 Nov 2026.
- rh-lean-roadmap (`docs/src/book/main.tex`, commit `c7755c1`).

## Community

G.R.H. Polymath, `rh-polymath.zulipchat.com`.

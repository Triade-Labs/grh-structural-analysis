# Open questions (UNKNOWN)

These are the questions we cannot settle with the data we have. An item closes only on new evidence, and every closure is recorded in CHANGELOG.md.

| ID | Question | Status |
|---|---|---|
| U-ORIG | Are the four candidate mechanisms IN1–IN4 original? (IN1 common-space factorisation of theta integrals with non-vanishing via Rallis; IN2 comparison of arithmetic volumes through injections with subexponential loss; IN3 logarithmic bound on the maximal slope of the Lie bundle; IN4 mean-slope inequality with corank control) | Open. Specialist question |
| U-L4 | Is any ingredient indispensable, i.e. not removable by rewriting? | Open. Our method cannot decide it |
| U-MIRROR | Is the analysed mirror identical to the archive published on the author's site? | Matches the community's `original` branch; not compared with the author's site |
| D1.a | What role does the divisibility (`LinkDIV`) play in the branch that produces the lower estimate (`latF`, `frameRealF_of''`)? | Open. Presence among the arguments is evidence; the role has not been read. Asked publicly (questions/) |
| D1.b | Where do `QuotientSlopeBoundsWith` and `LossBounds` come from? | Open |
| D1.c | Are the mass and volume inputs where the covolume bound enters? | Inference, medium–low confidence |
| U12 | Are the cohomological techniques of the original and of the shortened proof the same? | Open. Both contain a global weighted sum over finite sets of primes (see below); the same summation form does not imply the same mechanism |
| U12.b | Do the original and the shortened proof have the same main inequality? | Not established. According to Nashida (r8, §8.3–8.4), the constant c₁ has the same value provided the prime d is the same; the main term has the same form, but it is averaged over different sets with different weights, and equality of values was not verified. "Same architecture, not the same inequality" is a structural summary, not a proof of non-equivalence |
| N1 | Why the constraint m ≤ 2√x (Nashida, §7.6)? | Open. Not one of our lines of work |

Global weighted sums over primes:
- in the original, `UpperTheory.Top.VVle` (archive A, `Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean:12–49`);
- in the shortened proof, Σ_{l∈T} rowBudget(l)·log l ≤ B₀ for every finite set T of primes, via `exists_length_shaOdd_le` (`lsernau/grh-lean@72fead1`, `grh-compact/src/New/Selmer/FitTwistsExist.lean:38–54`).

These references are not yet in `claims.csv`.

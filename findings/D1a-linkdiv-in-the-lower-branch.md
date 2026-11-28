# D1.a: what the lower estimate takes from the divisibility `LinkDIV`

**Scope.** Archive A, commit `7cbf7a0`. This note follows up an open item of [D1-two-estimates.md](D1-two-estimates.md) §4: `LinkDIV` also appears among the arguments of the branch that produces the lower estimate `Data.SlopeIneq`.

**Credit.** The analysis of which conjuncts are used was first given by **H. Nashida** (Polymath, `overall structure`, reply of 28 Nov 2026), in answer to our question. Here we state which parts we have replicated and which we have not. Conjuncts are numbered from 0.

## 1. Replicated by us (EVIDENCE, level L3b)

- `LinkDIV_at` is a conjunction of nine conjuncts. In `linkCore`, conjunct 6 is used for `DIV` [C084], 7 for `EComp5` [C136], 8 for `HComp` [C137] and 1 for `HHBound` [C138, C139].
- `latF` uses only **conjunct 4** (`RRFull`) [C127, C128].
- `frameRealF_of` extracts **conjuncts 0, 4 and 5** and discards the others, including 6, 7 and 8, which contain the constant C [C129, C130].
- `frame_at_of` uses the first conjunct of `Lat_at` [C131].
- **The step from `joint_a_ramified_holds` to `Data.SlopeIneq`:**
  - in `frame_at_of`, `Frame_at` is built with seven components, and the last one is closed by `joint_a_ramified_holds` [C123, C081];
  - `frameF_of` obtains the frame property from `frame_at_of` [C080];
  - in `linkCore`, `hfr` is that last component [C124], and it is passed to `M.data_SlopeIneq` [C085, C086].
- That last component of `Frame_at` ends with a bound on the dual slope μ_dual [C125, C135]. Its form is that of the mean-slope inequality in the lower estimate.

## 2. Reported by Nashida, not replicated by us

- Inside `Lnk.lat_at`, conjunct 4 enters only the second conjunct of `Lat_at`, which goes to `HHBound` and is not used by `frame_at_of`.
- Inside `Lnk.frameReal_at_of`, conjuncts 0, 4 and 5 enter only the proof of `LatGeom`, which becomes argument [55] of `joint_a_ramified_holds`.
- The arguments of `M.data_SlopeIneq` contain neither the conjuncts nor the constant of the `LinkDIV` destructured in `linkCore`. Only threshold components reach them, through inequalities of the form "x is at least the threshold".
- Conjuncts 2 and 3 are not extracted in `latF`, `frameRealF_of` or `linkCore`.

## 3. What follows, and what does not

- **INFERENCE (medium confidence).** The lower branch takes from `LinkDIV` only conjuncts that do not contain the divisibility constant. The constant (conjuncts 6–8) goes to the upper estimate `DIV` and to `EComp5` and `HComp`.
- This does **not** show that the two branches are arithmetically independent. Conjuncts 0, 4 and 5 may still carry arithmetic information. Their mathematical content (`OneMapIntoCC`, `RRFull`, a ∀ u statement) has not been read.
- **Two declarations named `SlopeIneq`.** The field `Data.SlopeIneq` receives its content from `joint_a_ramified_holds` through `Frame_at`. A separate declaration, `Formalism.HN.SlopeIneq`, is also in the dependency graph [C134]. According to Nashida, there is no reference path between the two in either direction.

Status of D1.a in [registers/UNKNOWN.md](../registers/UNKNOWN.md): partly answered.

# The two estimates and where they come from (archive A)

**Scope.** Archive A (`CocoSgt/riemann-hypothesis-lean`, commit `7cbf7a0`; all paths below `src/`). This document covers the abstract layer `WeightedMeanData` and the path, read at the level of calls, from the bounds on Tate–Shafarevich groups to the final theorem for Dirichlet characters. Claim IDs such as `[C013]` refer to `verify/claims.csv`.

## 1. Summary

- In archive A the two competing estimates concern the **mean slope μ_CC** of a lattice, which equals −log(covolume)/rank. An upper bound on the slope is therefore a lower bound on the covolume, and vice versa.
- The **upper estimate** `Data.DIV` [C001, C002] bounds μ_CC + h − Fo from above. Its main term contains a CM period, log Ω = γ + log(π/v) − L′/L, which is where Chowla–Selberg enters. It also contains divisibility error terms.
- The **lower estimate** `Data.SlopeIneq` [C003, C004] bounds μ_CC from below, in terms of a weighted mean s of other slopes corrected by heights. It has the form of a mean-slope inequality (`TheoremFSharp`).
- The slope μ_CC appears in the two estimates with opposite signs, so it cancels. What remains is compared with a sum over primes, and the comparison closes at `Deduction.ch_top` [C013, C014].

## 2. How the two estimates combine (EVIDENCE, abstract layer)

1. `s_lower5` [C005, C006] gives Ga + μ_CC − K ≤ s, assuming `HidaSetting`, `DIV`, `EComp5`, `Count5`, `Slopes` and `QuotientSlopeBoundsWith`.
2. `Ga_bound5` [C009, C010] combines this with `SlopeIneq`. μ_CC cancels [C088] and Ga ≤ Main + log|W| + errors remains.
3. `key_identity5` [C007, C008, C089] turns the main term of `DIV` into **Main** = Σ a·(log a − 1 − γ + L′/L − mean of log w). The CM period enters as log Ω and leaves as −γ + L′/L.
4. From Ga to ASK, the code contains two variants:
   - the **pointwise** one, `each_unit_bound_statement` [C011, C012, C090], is in the dependency graph and is the one `Deduction.ch_top` calls [C091];
   - the **averaged** one, `uniform_bound_statement` with `Losses` and `MeanBoundSecondForm` [C095–C100], exists in the archive but is not in the dependency graph. Neither is the route through `chain_top_bound` [C101, C102, C111, C112].
5. `Deduction.ch_top` [C013]: for each u, ASK − Main ≤ (error factor). `core_gm` [C017, C018, C092] then gives Λ.Gm(x) ≤ x^(1/2 + O(ε)).

INFERENCE (medium–high confidence): ASK is the prime-side quantity (divisibility gained at non-split primes) and Main the geometric main term. This reading comes from the structure of the definitions, not from reading every proof.

## 3. The path from the Sha bounds to the final theorem (EVIDENCE)

This is the **flow of mathematical results**. Between two consecutive steps there may be a direct call or a chain of intermediate declarations. Every declaration listed is in the dependency graph.

1. `HypV` [C027, C028], bounds on Sha lengths, is part of the definition of the family class. `divinN_of_hypV` [C031, C032] turns it into the divisibility `DIVinN`.
2. `topDesWin` [C033, C034] builds families with `ChainTied` [C025, C026]. The divisibility produces `hD` [C069], and `hD` is passed into the `LinkGLOBAL` argument [C070].
3. Inside the proof of `LinkGLOBAL` [C051, C052], `link_gl` [C053, C071] goes through `famGLmin_of_realPlaceSecondLayer` and `FamGLmin.link8` [C074, C075], then through `linkGLOBAL7_min` and `linkGLOBAL7_items` [C055–C058], down to `linkCore` [C059, C060, C079]. `linkCore` assembles the eleven fields of `SizeData₂` [C015, C016, C087, C094]:
   - **`DIV`** is built by `M.data_DIV` from the seventh component of `LinkDIV_at` [C043, C044, C082–C084], that is, from the divisibility;
   - **`SlopeIneq`** is built by `M.data_SlopeIneq` from `hfr`, extracted from the frame property [C085, C086]. That property comes from `frameF_of` → `frame_at_of` → `joint_a_ramified_holds` [C061–C064, C078, C080, C081];
   - **`Count5`** and **`Slopes`** [C118, C119] come from `CountF` and `SlopesMF`, which receive the mass and volume inputs `MassRatio₂` and `BaseVolumeEqualsMass` [C067, C068, C115–C117]. The latter is defined as `volY0 D = massI D D.R.r` [C120]; reading these as a volume and a mass is ours.
4. Steps 1–5 of §2 follow.
5. `windowInequality_of_artinInputs` and `level_gm_le_on_family_scales` [C019–C024, C093] lead to `zeroFreeAll_of_topG` [C035, C036].
6. Separately, `shape_closed_link_n_of_green` [C037, C038] proves the hypothesis `TopG` by calling `topDesWin` [C072]. `zero_free_all_of_green_v_win` [C039, C040] combines it with `zeroFreeAll_of_topG` [C073].
7. `every_character_of_green_v_win` [C041, C042]: GRH for Dirichlet characters.

Not in the dependency graph: the parallel route `shapeWin` → `plugWin` → `plugAll` [C103–C108], and `zeroFreeOn_of_core`, `zeroFreeOn_of_chainTied` [C113, C114].

## 4. What this does **not** show

- **The ingredients are not cleanly separated.** `LinkDIV` (the divisibility) also appears among the arguments of `latF` [C077] and of `frameRealF_of''` [C121, C122], from which the frame property behind `SlopeIneq` is derived. We have not read what role it plays there.
- We have not traced where `QuotientSlopeBoundsWith` and `LossBounds` come from.
- INFERENCE (medium–low confidence): the mass and volume inputs are where the covolume bound enters (the bound our earlier analysis calls `L3main`; the name is ours, not the archive's). `BaseVolumeEqualsMass` is the only covolume-type input we found on this stretch. We have not established that it is the bound itself.
- Reading the calls is not reading the proofs. The meaning of the calls above is our reading (level L3b in METHOD.md).

## 5. External convergence

H. Nashida (note r8, 27 Nov 2026; see SOURCES.md) independently identifies the main inequality of archive A with the conclusion of `Deduction.ch_top`, in its per-u form (§8.1). This is a convergence between two AI-assisted analyses, not a specialist validation.

# Errors we made and corrected

We record them because they show how the method works, and where it failed before it worked.

| Where | Error | How it was caught | Correction |
|---|---|---|---|
| Early reading of the covolume bound | We believed that reducing a geometry parameter (`anyGeometry`) to "true" removed the geometric content of the covolume bound | Reading the source: it is only a membership parameter; the covolume estimate is a separate input | Corrected before the first consolidated analysis |
| Chain behind the lower estimate | We listed the chain `joint_a_ramified_holds` → `function_slope_transfer` → `slope_inequality_of_family` → `SlopeIneq` as verified. The calls had been read, but the last two links are not in the dependency graph [C109, C110] | Checking the names against Shore's dataset | The actual route goes through `frame_at_of` (findings/D1, §3) |
| Ga → ASK | We assumed the averaged variant (`uniform_bound_statement`, `chain_top_bound`) was the one used | Dataset check [C100, C102] | The pointwise variant `each_unit_bound_statement` is the one in the graph |
| Method | One of us proposed treating absence from the dataset as inconclusive | The other recalled the agreed method | Absence from the dataset means "not in the dependency graph" (METHOD.md §2) |
| Comparison of the two proofs | We first wrote that the main terms of the two inequalities "have different values" | Rereading Nashida §8.4: equality of values was not established | Recorded as "identity not established" (registers/UNKNOWN.md, U12.b) |
| Comparison of the two proofs | We described the cohomological control as "global in the original, local in the shortened proof" | Reading the shortened proof: it also contains a global weighted sum | Contrast removed; U12 remains open |
| An external exposition | We attributed to an exposition a statement that is not in its text | Full reading of the document | Corrected before anything was sent |

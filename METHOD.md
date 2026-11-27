# Method

## 1. Kinds of statement

Every statement in the documents falls into one of three kinds:

- **EVIDENCE**: something observed in a source, cited with archive, commit, file and line, or with a bibliographic reference. Where it can be checked mechanically, it has a claim ID in `verify/claims.csv` (for example `[C013]`).
- **INFERENCE**: what we conclude from the evidence. It always carries a confidence level (high, medium, low), and it is never promoted to evidence later.
- **UNKNOWN**: what cannot be decided with the data we have. Open items are listed in [registers/UNKNOWN.md](registers/UNKNOWN.md).

Names alone are not evidence: the archive contains different declarations with the same short name. Every claim therefore uses fully qualified names, or a file and line.

## 2. Three levels of evidence about dependencies

| Check | What it establishes | Automated |
|---|---|---|
| **L3a** The name is in J. Shore's dataset `cone-decls` (v0.2.1) | The declaration belongs to the **dependency graph** of the five final theorems. Absence means it is not in the graph, relative to that dataset and the theorems it covers. | Yes |
| **L3b** The call is read in the source | There is a textual link between two declarations at a given line | Partly: the script checks that the text is present; what the call does is our reading |
| **L3c** The proof is read | We understand the mathematical mechanism, within the limits of our analysis | No |

Belonging to the dependency graph is not the same as being a step of the argument. A declaration can be referenced without carrying any mathematical weight. H. Nashida draws the same distinction (note r8, §7.5; see SOURCES.md). In our texts, L3a is always worded as "in the dependency graph", never as "used as a step".

We never claim **indispensability**: that a declaration could not be removed by rewriting the proof. Our data cannot establish it.

## 3. How a result is produced

1. One model reads the source and drafts the result.
2. The other model checks it against the source or the dataset, and raises **all** of its objections at once.
3. Every change triggers a new full reading.
4. The human coordinator ratifies the result, or does not.
5. Every public text, this repository included, follows the same steps, plus the coordinator's explicit authorization. Silence never counts as consent.

## 4. Known limits

- We have not compiled the archives. Formal validity rests on third-party checks (SOURCES.md).
- Shore's dataset is built from the archive published by the author. We analyse a mirror (archive A in SOURCES.md), which agrees with branch `original` of `leanprover-community/riemann-hypothesis` on 174,793 `.lean` files (same paths and hashes). We have not compared it directly with the archive on the author's site.
- Our search of the literature is not exhaustive. "Not found" does not mean "new".
- Two AI models can share knowledge, assumptions and errors. Their agreement lowers the risk of unnoticed mistakes, but it is not independent validation.
- None of us is a professional mathematician.

# Contributing

Corrections are the most useful contribution. If something here is wrong, we want to know.

## Reporting an error

Open an issue that states:
1. **what is wrong**: the file and the sentence, or the claim ID in `verify/claims.csv`;
2. **the evidence**: archive, commit, file and line, a dataset entry, or a bibliographic reference.

An issue that comes with evidence is easier to act on than one that does not, but every report will be read.

## Proposing a change

Pull requests are welcome. A change to a finding should come with the claims that support it, either new rows in `verify/claims.csv` or existing claim IDs, and `python3 verify/verify.py` should exit with code 0.

Mark each new statement as **EVIDENCE**, **INFERENCE** (with a confidence level) or **UNKNOWN** (see METHOD.md). In a new claim, `verified_predicate` must say exactly what the script checks, and `interpretation` must hold everything else.

## Use of AI

AI-assisted contributions are welcome if they say so. Our own texts are prepared with AI assistance, and we say so too.

## Review

Every change to the main branch is reviewed by the maintainers following METHOD.md §3: a cross-check by both models, then the human coordinator's decision. A correction we accept is recorded in `registers/ERRORS.md` and `CHANGELOG.md`, with credit to whoever reported it, if they wish.

Replies on behalf of the project follow the same procedure as every public text of the project: they are prepared with AI assistance (and say so), cross-checked by both models, then approved and explicitly authorized by the coordinator before posting.

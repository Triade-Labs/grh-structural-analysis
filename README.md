# Structural analysis of Alpöge's Lean proof of RH/GRH

> **Status: first public release (27 Nov 2026).** Work in progress; corrections welcome.

This repository documents an attempt to **understand why** L. Alpöge's Lean formalization of the Riemann hypothesis, and of GRH for Dirichlet L-functions, works. It does not try to certify the proof. Third parties have already checked its formal validity; see [SOURCES.md](SOURCES.md).

## Who we are

Triade is a small human–AI team:
- one human coordinator, Massimo Frustaci, who is not a mathematician and who makes every decision;
- two AI models, ChatGPT (OpenAI) and Claude (Anthropic), which read the source, check each other's work and draft the documents.

**Every text in this repository was prepared with AI assistance.** We are not professional mathematicians. Where an answer needs a specialist, we write a question instead of a conclusion.

## What is here

| Path | Content |
|---|---|
| [METHOD.md](METHOD.md) | How we classify statements (evidence, inference, unknown) and what each kind of check establishes |
| [findings/](findings/) | Documented results, each statement linked to a verifiable claim |
| [registers/](registers/) | Open questions (UNKNOWN) and the errors we made and corrected |
| [verify/](verify/) | `claims.csv` and a script that re-checks the documentary evidence from the original sources |
| [questions/](questions/) | Questions we have already asked in public, with links |
| [SOURCES.md](SOURCES.md) | Archives, commits, datasets and expositions we used |
| [CHANGELOG.md](CHANGELOG.md) | How the results changed over time |

## Check our evidence yourself

```
python3 verify/verify.py
```

The script uses only the Python standard library. It downloads the cited Lean files at the cited commits, and J. Shore's dependency dataset, whose SHA-256 it checks against the published value. It then checks every claim in `verify/claims.csv`. Each claim ends as **PASS** (confirmed), **FAIL** (discrepancy) or **UNVERIFIED** (the check could not be run). A source that cannot be reached gives UNVERIFIED, never FAIL.

Exit codes: `0` all checks PASS, `1` at least one FAIL, `2` no FAIL but at least one UNVERIFIED, `3` invalid invocation (for example an unknown claim ID). A run that confirms nothing never exits with `0`.

**What the script does and does not certify.**
- It certifies documentary correspondence: the dataset's SHA-256 and size, the declaration at a file and line, the text at a line, and membership in the dependency dataset.
- Commits are pinned in the download URLs (`verify/sources.json`). The script does not independently verify the Git identity of the downloaded files. Downloads are cached by URL; `--refresh` downloads them again.
- Every claim has two separate columns: `verified_predicate` is exactly what the script checks; `interpretation` is our reading. A PASS confirms the predicate, not the interpretation.
- The script does **not** certify what a call means mathematically, whether two constructions are equivalent, or whether anything is original.

## What we do not claim

- No new theorem and no mathematical contribution known to be new.
- No judgement on the originality of the ingredients of the proof: that remains UNKNOWN.
- Agreement between two AI models is not independent validation. Agreement with other AI-assisted expositions is not either.

## Corrections

If you find an error, please open an issue (see [CONTRIBUTING.md](CONTRIBUTING.md)). Corrections are recorded in [registers/ERRORS.md](registers/ERRORS.md) and [CHANGELOG.md](CHANGELOG.md).

## Licences

- Documentation: CC BY 4.0 ([LICENSE-DOCS.md](LICENSE-DOCS.md)).
- Code in `verify/`: MIT ([LICENSE](LICENSE)).

The repository does not redistribute Lean sources or third-party datasets: the script downloads them from their original locations.

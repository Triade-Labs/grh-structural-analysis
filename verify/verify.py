#!/usr/bin/env python3
"""Reproducible check of the documentary evidence cited by this repository.

Standard library only. Usage:

    python3 verify/verify.py            # check every claim in verify/claims.csv
    python3 verify/verify.py --offline  # use only files already in the cache

What this script certifies, and what it does not:

* It checks DOCUMENTARY evidence: that a commit is the one cited, that the
  dependency dataset has the published SHA-256, that a declaration sits at the
  cited file and line, that a given text occurs at a cited line, and whether a
  fully qualified name is (or is not) in J. Shore's dependency dataset.
* It does NOT check the mathematical meaning of a call, the equivalence of two
  constructions, or originality. Those remain readings by the authors, marked as
  such in the documents.

Each claim ends in exactly one of three outcomes:

    PASS        the evidence is confirmed
    FAIL        a discrepancy was found
    UNVERIFIED  the check could not be run (e.g. a source was unreachable or
                its hash did not match). UNVERIFIED is never counted as FAIL.

Exit status: 0 if there is no FAIL, 1 otherwise.
"""

import argparse
import csv
import gzip
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".cache")

PASS, FAIL, UNVERIFIED = "PASS", "FAIL", "UNVERIFIED"


class Unavailable(Exception):
    """A source could not be obtained; the claim is UNVERIFIED, not FAIL."""


def fetch(url, offline=False, timeout=60):
    os.makedirs(CACHE, exist_ok=True)
    name = hashlib.sha256(url.encode()).hexdigest()
    path = os.path.join(CACHE, name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    if offline:
        raise Unavailable(f"not in cache (offline): {url}")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            data = r.read()
    except (urllib.error.URLError, OSError) as e:
        raise Unavailable(f"{url}: {e}")
    with open(path, "wb") as f:
        f.write(data)
    return data


class Dataset:
    def __init__(self, cfg, offline):
        self.cfg = cfg
        self.offline = offline
        self._names = None
        self._error = None

    def names(self):
        if self._names is not None:
            return self._names
        if self._error:
            raise Unavailable(self._error)
        try:
            raw = fetch(self.cfg["url"], self.offline, timeout=300)
        except Unavailable as e:
            self._error = str(e)
            raise
        digest = hashlib.sha256(raw).hexdigest()
        if digest != self.cfg["sha256"]:
            self._error = f"dataset SHA-256 {digest} != published {self.cfg['sha256']}"
            raise Unavailable(self._error)
        lines = gzip.decompress(raw).decode("utf-8").splitlines()
        self._names = set(l.strip() for l in lines if l.strip())
        if len(self._names) != self.cfg["declarations"]:
            self._error = f"dataset has {len(self._names)} names, expected {self.cfg['declarations']}"
            self._names = None
            raise Unavailable(self._error)
        return self._names


def source_lines(archive_cfg, path, offline):
    url = archive_cfg["raw_base"] + urllib.parse.quote(path)
    return fetch(url, offline).decode("utf-8").split("\n")


def check_claim(c, sources, dataset, offline):
    kind = c["check"]
    try:
        if kind in ("decl_at_line", "text_at_line"):
            lines = source_lines(sources["archives"][c["archive"]], c["path"], offline)
            n = int(c["line"])
            if n < 1 or n > len(lines):
                return FAIL, f"line {n} out of range (file has {len(lines)} lines)"
            text = lines[n - 1]
            if kind == "decl_at_line":
                pat = r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*" + re.escape(c["pattern"]) + r"(?=[\s({:\[]|$)"
                ok = re.search(pat, text) is not None
            else:
                ok = c["pattern"] in text
            return (PASS, "") if ok else (FAIL, f"line {n}: {text.strip()[:120]}")
        if kind == "in_dataset":
            return (PASS, "") if c["fq_name"] in dataset.names() else (FAIL, "name not in dataset")
        if kind == "absent_from_dataset":
            short = c["pattern"]
            hits = [x for x in dataset.names() if x == short or x.endswith("." + short)]
            return (PASS, "") if not hits else (FAIL, "found: " + ", ".join(sorted(hits)[:3]))
        return UNVERIFIED, f"unknown check type {kind!r}"
    except Unavailable as e:
        return UNVERIFIED, str(e)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--claims", default=os.path.join(HERE, "claims.csv"))
    ap.add_argument("--sources", default=os.path.join(HERE, "sources.json"))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--only", help="comma-separated claim ids")
    args = ap.parse_args(argv)

    with open(args.sources, encoding="utf-8") as f:
        sources = json.load(f)
    with open(args.claims, encoding="utf-8", newline="") as f:
        claims = list(csv.DictReader(f))
    if args.only:
        keep = set(args.only.split(","))
        claims = [c for c in claims if c["id"] in keep]

    dataset = Dataset(sources["dataset"], args.offline)
    counts = {PASS: 0, FAIL: 0, UNVERIFIED: 0}
    for c in claims:
        outcome, detail = check_claim(c, sources, dataset, args.offline)
        counts[outcome] += 1
        where = f"{c['path']}:{c['line']}" if c["path"] else (c["fq_name"] or c["pattern"])
        print(f"{outcome:<10} {c['id']}  {c['check']:<19} {where}" + (f"  -- {detail}" if detail else ""))
    print()
    print(f"PASS {counts[PASS]}  FAIL {counts[FAIL]}  UNVERIFIED {counts[UNVERIFIED]}  (total {len(claims)})")
    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())

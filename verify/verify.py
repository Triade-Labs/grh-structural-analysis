#!/usr/bin/env python3
"""Reproducible check of the documentary evidence cited by this repository.

Standard library only. Usage:

    python3 verify/verify.py            # check every claim in verify/claims.csv
    python3 verify/verify.py --offline  # use only files already in the cache

What this script certifies, and what it does not:

* It checks DOCUMENTARY evidence: that the dependency dataset has the
  published SHA-256 and size, that a declaration sits at the cited file and
  line (downloaded at the commit pinned in sources.json), that a given text occurs at a cited line, and whether a
  fully qualified name is (or is not) in J. Shore's dependency dataset.
* It does NOT check the mathematical meaning of a call, the equivalence of two
  constructions, or originality. Those remain readings by the authors, marked as
  such in the documents.

Each claim ends in exactly one of three outcomes:

    PASS        the evidence is confirmed
    FAIL        a discrepancy was found
    UNVERIFIED  the check could not be run (e.g. a source was unreachable or
                its hash did not match). UNVERIFIED is never counted as FAIL.

Exit status:
    0  every requested check is PASS
    1  at least one FAIL
    2  no FAIL, but at least one UNVERIFIED
    3  invalid configuration or invocation (e.g. unknown claim id, no claims)

Limits of the documentary checks:

* Commits are pinned in the download URLs (verify/sources.json); the script
  does not independently verify the Git identity of the downloaded files.
* Downloads are cached in verify/.cache, keyed by URL, not by content. Use
  --refresh to ignore the cache and download again.
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


REFRESH = False


def fetch(url, offline=False, timeout=60):
    os.makedirs(CACHE, exist_ok=True)
    name = hashlib.sha256(url.encode()).hexdigest()
    path = os.path.join(CACHE, name)
    if os.path.exists(path) and not REFRESH:
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
        if len(raw) != self.cfg["size_bytes"]:
            self._error = f"dataset size {len(raw)} != published {self.cfg['size_bytes']}"
            raise Unavailable(self._error)
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
    ap.add_argument("--refresh", action="store_true", help="ignore the download cache")
    ap.add_argument("--only", help="comma-separated claim ids")
    args = ap.parse_args(argv)
    global REFRESH
    REFRESH = args.refresh

    try:
        with open(args.sources, encoding="utf-8") as f:
            sources = json.load(f)
        with open(args.claims, encoding="utf-8", newline="") as f:
            claims = list(csv.DictReader(f))
    except (OSError, ValueError) as e:
        print(f"CONFIG ERROR: {e}")
        return 3
    ids = [c["id"] for c in claims]
    if len(ids) != len(set(ids)):
        print("CONFIG ERROR: duplicate claim ids")
        return 3
    if args.only:
        keep = [x.strip() for x in args.only.split(",") if x.strip()]
        unknown = sorted(set(keep) - set(ids))
        if unknown:
            print("CONFIG ERROR: unknown claim id(s): " + ", ".join(unknown))
            return 3
        claims = [c for c in claims if c["id"] in set(keep)]
    if not claims:
        print("CONFIG ERROR: no claims to check")
        return 3

    dataset = Dataset(sources["dataset"], args.offline)
    counts = {PASS: 0, FAIL: 0, UNVERIFIED: 0}
    for c in claims:
        outcome, detail = check_claim(c, sources, dataset, args.offline)
        counts[outcome] += 1
        where = f"{c['path']}:{c['line']}" if c["path"] else (c["fq_name"] or c["pattern"])
        print(f"{outcome:<10} {c['id']}  {c['check']:<19} {where}" + (f"  -- {detail}" if detail else ""))
    print()
    print(f"PASS {counts[PASS]}  FAIL {counts[FAIL]}  UNVERIFIED {counts[UNVERIFIED]}  (total {len(claims)})")
    if counts[FAIL]:
        return 1
    if counts[UNVERIFIED]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

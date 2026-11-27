"""Offline tests of the three outcomes of verify.py (no network needed).

Run with:  python3 -m unittest discover -s verify/tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import verify  # noqa: E402


class FakeDataset:
    def __init__(self, names=None, error=None):
        self._n, self._e = names, error

    def names(self):
        if self._e:
            raise verify.Unavailable(self._e)
        return self._n


SOURCES = {"archives": {"A": {"raw_base": "unused/"}}}
FILE = ["-- header", "theorem foo (x : Nat) : x = x := rfl", "  exact bar baz"]


class Outcomes(unittest.TestCase):
    def setUp(self):
        self._orig = verify.source_lines
        verify.source_lines = lambda cfg, path, offline: FILE

    def tearDown(self):
        verify.source_lines = self._orig

    def claim(self, **kw):
        c = dict(archive="A", path="X.lean", line="", check="", pattern="", fq_name="")
        c.update(kw)
        return c

    def test_decl_pass_and_fail(self):
        ok = verify.check_claim(self.claim(check="decl_at_line", line="2", pattern="theorem foo"), SOURCES, None, True)
        bad = verify.check_claim(self.claim(check="decl_at_line", line="3", pattern="theorem foo"), SOURCES, None, True)
        prefix = verify.check_claim(self.claim(check="decl_at_line", line="2", pattern="theorem fo"), SOURCES, None, True)
        self.assertEqual(ok[0], verify.PASS)
        self.assertEqual(bad[0], verify.FAIL)
        self.assertEqual(prefix[0], verify.FAIL)  # a prefix of a name is not the name

    def test_text_and_range(self):
        self.assertEqual(verify.check_claim(self.claim(check="text_at_line", line="3", pattern="bar"), SOURCES, None, True)[0], verify.PASS)
        self.assertEqual(verify.check_claim(self.claim(check="text_at_line", line="9", pattern="bar"), SOURCES, None, True)[0], verify.FAIL)

    def test_dataset(self):
        ds = FakeDataset({"A.B.foo", "C.bar"})
        self.assertEqual(verify.check_claim(self.claim(check="in_dataset", fq_name="A.B.foo"), SOURCES, ds, True)[0], verify.PASS)
        self.assertEqual(verify.check_claim(self.claim(check="in_dataset", fq_name="A.B.qux"), SOURCES, ds, True)[0], verify.FAIL)
        self.assertEqual(verify.check_claim(self.claim(check="absent_from_dataset", pattern="qux"), SOURCES, ds, True)[0], verify.PASS)
        self.assertEqual(verify.check_claim(self.claim(check="absent_from_dataset", pattern="bar"), SOURCES, ds, True)[0], verify.FAIL)

    def test_unavailable_is_unverified_not_fail(self):
        ds = FakeDataset(error="network down")
        self.assertEqual(verify.check_claim(self.claim(check="in_dataset", fq_name="A.B.foo"), SOURCES, ds, True)[0], verify.UNVERIFIED)

        def boom(cfg, path, offline):
            raise verify.Unavailable("unreachable")
        verify.source_lines = boom
        self.assertEqual(verify.check_claim(self.claim(check="decl_at_line", line="2", pattern="theorem foo"), SOURCES, None, True)[0], verify.UNVERIFIED)


class ExitCodes(unittest.TestCase):
    """Exit codes of main(): 0 all PASS, 1 FAIL, 2 UNVERIFIED only, 3 invalid invocation."""

    def setUp(self):
        import tempfile, json, csv
        self.dir = tempfile.mkdtemp()
        self.sources = os.path.join(self.dir, "sources.json")
        with open(self.sources, "w") as f:
            json.dump({"archives": {"A": {"raw_base": "unused/"}}, "dataset": {"url": "x", "sha256": "x", "declarations": 1}}, f)
        self.claims = os.path.join(self.dir, "claims.csv")
        with open(self.claims, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "archive", "path", "line", "check", "pattern", "fq_name"])
            w.writeheader()
            w.writerow(dict(id="C1", archive="A", path="X.lean", line="2", check="decl_at_line", pattern="theorem foo", fq_name=""))
            w.writerow(dict(id="C2", archive="A", path="X.lean", line="3", check="decl_at_line", pattern="theorem foo", fq_name=""))
        self._orig = verify.source_lines

    def tearDown(self):
        verify.source_lines = self._orig

    def run_main(self, *extra):
        return verify.main(["--claims", self.claims, "--sources", self.sources, "--offline", *extra])

    def test_codes(self):
        verify.source_lines = lambda cfg, path, offline: FILE
        self.assertEqual(self.run_main("--only", "C1"), 0)
        self.assertEqual(self.run_main(), 1)
        self.assertEqual(self.run_main("--only", "C999"), 3)

        def boom(cfg, path, offline):
            raise verify.Unavailable("unreachable")
        verify.source_lines = boom
        self.assertEqual(self.run_main("--only", "C1"), 2)


if __name__ == "__main__":
    unittest.main()

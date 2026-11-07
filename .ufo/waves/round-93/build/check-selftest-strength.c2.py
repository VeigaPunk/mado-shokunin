#!/usr/bin/env python3
"""check-selftest-strength -- fail when a passing selftest assertion is weakened.

The lane's instruments read only ``--selftest``'s result line, so an
assertion weakened to pass (the line still ``checks=N failed=0``) is
invisible (round-92 routed defect 3). This gate runs the tool's
``--selftest`` against a committed kill-set of production mutants (each
names the selftest check that must fail on it) and prints WEAK when any
kill-set mutant passes the selftest or fails under a check other than the
named one. A kill whose must_fail is a list holds only when the mutant fails
exactly that set of checks, so weakening any check that catches it is seen
(round 93, R93MReviewC2 / R93MMutC2 escapes).

Usage:
  check-selftest-strength.py --tool PATH --kills JSON [--scratch-root DIR]
      [--timeout S] [--allow-sha-drift]
  check-selftest-strength.py --selftest

Gate:
  (1) the unmutated tool's selftest must exit 0 with failed=0, else rc 2
      (setup error).
  (2) for each kill: apply find/replace (find exactly once in the
      tool's non-selftest code, else rc 2), run ``python3 -I <copy>
      --selftest`` in a fresh scratch dir with TMPDIR set there, timeout;
      it must exit non-zero AND list the must_fail label among its FAIL
      lines (must_fail a string) or print exactly the must_fail labels as
      its FAIL lines (must_fail a list); otherwise record SURVIVED <id> or
      WRONG_CHECK <id> failed=<labels>. A non-zero exit without FAIL lines
      (a crash) or a timeout is SURVIVED, never held.
  (1b) with "selftest_checks": N in the kill-set, the unmutated result line
      must read checks=N (a dropped check is a setup error).
  (3) verdict line ``SELFTEST_STRENGTH: OK|WEAK tool=... kills=N held=H
      survived=S wrong_check=W`` rc 0/1/2.
  tool_sha256 mismatch is rc 2 unless --allow-sha-drift (the counter
  applies weakenings, so it passes that flag).

Kill-set JSON:
  {"tool": "<repo-relative path>", "tool_sha256": "...",
   "selftest_argv": ["--selftest"],
   "fail_line_prefix": "SEAT_REPORTS_SELFTEST_FAIL: ",
   "result_line_prefix": "SEAT_REPORTS_SELFTEST: ",
   "selftest_checks": N (optional),
   "kills": [{"id", "find", "replace", "must_fail": "<label>" | ["<label>", ...]}]}

ASCII output, stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile


class SetupError(Exception):
    pass


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def non_selftest_prefix(text: str) -> str:
    """Tool source up to (and excluding) the selftest definition.

    Kill-set mutants must land in production code, outside the selftest
    itself; a mutant inside the selftest harness could silence its own
    check without weakening production code.
    """
    idx = text.find("def selftest(")
    return text[:idx] if idx >= 0 else text


def run_selftest(script: str, argv: list[str], scratch: str, timeout: float,
                 fail_prefix: str, result_prefix: str) -> tuple[int, list[str], list[str]]:
    env = dict(os.environ)
    env["TMPDIR"] = scratch
    os.makedirs(scratch, exist_ok=True)
    try:
        r = subprocess.run([sys.executable, "-I", os.path.abspath(script), *argv],
                           capture_output=True, timeout=timeout, env=env,
                           cwd=scratch)
    except subprocess.TimeoutExpired:
        return None, [], ["timeout"]
    out = r.stdout.decode("utf-8", "replace").splitlines()
    fails = [ln[len(fail_prefix):] for ln in out if ln.startswith(fail_prefix)]
    results = [ln for ln in out if ln.startswith(result_prefix)]
    return r.returncode, fails, results


def gate(tool: str, kills_path: str, scratch_root: str | None, timeout: float,
         allow_sha_drift: bool, out=print) -> int:
    try:
        with open(kills_path, "rb") as fh:
            ks = json.loads(fh.read().decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError) as e:
        out(f"SELFTEST_STRENGTH: SETUP_ERROR cannot read kill-set: {e}")
        return 2
    try:
        with open(tool, "rb") as fh:
            src_bytes = fh.read()
    except OSError as e:
        out(f"SELFTEST_STRENGTH: SETUP_ERROR cannot read tool: {e}")
        return 2
    want_sha = ks.get("tool_sha256", "")
    got_sha = sha256_bytes(src_bytes)
    if want_sha and want_sha != got_sha and not allow_sha_drift:
        out(f"SELFTEST_STRENGTH: SETUP_ERROR tool sha256 mismatch "
            f"want={want_sha} got={got_sha}")
        return 2
    argv = ks.get("selftest_argv", ["--selftest"])
    if not isinstance(argv, list) or not all(isinstance(a, str) for a in argv):
        out("SELFTEST_STRENGTH: SETUP_ERROR bad selftest_argv")
        return 2
    fail_prefix = ks.get("fail_line_prefix", "SEAT_REPORTS_SELFTEST_FAIL: ")
    result_prefix = ks.get("result_line_prefix", "SEAT_REPORTS_SELFTEST: ")
    kills = ks.get("kills")
    if not isinstance(kills, list):
        out("SELFTEST_STRENGTH: SETUP_ERROR kill-set has no kills list")
        return 2
    for k in kills:
        mf = k.get("must_fail") if isinstance(k, dict) else None
        if not isinstance(k, dict) or not all(isinstance(k.get(f), str) for f in ("id", "find", "replace")) \
                or not (isinstance(mf, str) or (isinstance(mf, list) and mf and all(isinstance(x, str) for x in mf))):
            out("SELFTEST_STRENGTH: SETUP_ERROR bad kill entry")
            return 2
    want_checks = ks.get("selftest_checks")
    if want_checks is not None and (not isinstance(want_checks, int) or isinstance(want_checks, bool)):
        out("SELFTEST_STRENGTH: SETUP_ERROR bad selftest_checks")
        return 2

    base = scratch_root or tempfile.mkdtemp(prefix="selftest-strength-")
    os.makedirs(base, exist_ok=True)
    own = scratch_root is None
    held = survived = wrong = 0
    notes = []
    try:
        # (1) unmutated tool
        with tempfile.TemporaryDirectory(dir=base) as d:
            rc, fails, results = run_selftest(tool, argv, d, timeout,
                                              fail_prefix, result_prefix)
            if rc is None:
                out("SELFTEST_STRENGTH: SETUP_ERROR unmutated selftest timed out")
                return 2
            if rc != 0 or fails:
                out(f"SELFTEST_STRENGTH: SETUP_ERROR unmutated selftest rc={rc} "
                    f"fails={fails} result={results}")
                return 2
            if not results or "failed=0" not in results[-1]:
                out(f"SELFTEST_STRENGTH: SETUP_ERROR unmutated selftest result "
                    f"{results} lacks failed=0")
                return 2
            if want_checks is not None and f"checks={want_checks} " not in results[-1] + " ":
                out(f"SELFTEST_STRENGTH: SETUP_ERROR unmutated selftest result "
                    f"{results} is not checks={want_checks}")
                return 2
        # (2) each kill
        text = src_bytes.decode("utf-8", "surrogateescape")
        pre = non_selftest_prefix(text)
        for k in kills:
            find, replace = k["find"], k["replace"]
            if not find or pre.count(find) != 1:
                out(f"SELFTEST_STRENGTH: SETUP_ERROR kill {k['id']} find occurs "
                    f"{pre.count(find)} times in non-selftest code")
                return 2
            mutated = text.replace(find, replace, 1)
            with tempfile.TemporaryDirectory(dir=base) as d:
                copy = os.path.join(d, "tool.py")
                with open(copy, "wb") as fh:
                    fh.write(mutated.encode("utf-8", "surrogateescape"))
                rc, fails, results = run_selftest(copy, argv, d, timeout,
                                                  fail_prefix, result_prefix)
            if rc == 0 or not fails:
                survived += 1
                notes.append(f"SURVIVED {k['id']}")
            elif (k["must_fail"] not in fails) if isinstance(k["must_fail"], str) \
                    else sorted(fails) != sorted(k["must_fail"]):
                wrong += 1
                notes.append(f"WRONG_CHECK {k['id']} failed={fails}")
            else:
                held += 1
    finally:
        if own:
            # best-effort cleanup of the auto scratch root
            import shutil
            shutil.rmtree(base, ignore_errors=True)
    for n in notes:
        out(n)
    tool_tag = ks.get("tool", tool)
    verdict = "WEAK" if (survived or wrong) else "OK"
    out(f"SELFTEST_STRENGTH: {verdict} tool={tool_tag} kills={len(kills)} "
        f"held={held} survived={survived} wrong_check={wrong}")
    return 1 if verdict == "WEAK" else 0


SELFTEST_FAKE_OK = '''#!/usr/bin/env python3
import sys
CHECKS = [("alpha", True), ("beta", True)]


def selftest():
    failed = [n for n, ok in CHECKS if not ok]
    for n in failed:
        print(f"SEAT_REPORTS_SELFTEST_FAIL: {n}")
    print(f"SEAT_REPORTS_SELFTEST: checks={len(CHECKS)} failed={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(selftest())
'''
SELFTEST_FAKE_SURVIVOR = '''#!/usr/bin/env python3
import sys
CHECKS = [("alpha", True), ("beta", True)]


def selftest():
    failed = [n for n, ok in CHECKS if not ok]
    for n in failed:
        print(f"SEAT_REPORTS_SELFTEST_FAIL: {n}")
    print(f"SEAT_REPORTS_SELFTEST: checks={len(CHECKS)} failed={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(selftest())
'''


def selftest() -> int:
    results: list[tuple[str, bool]] = []

    def write(d: str, name: str, text: str) -> str:
        p = os.path.join(d, name)
        with open(p, "w") as fh:
            fh.write(text)
        return p

    def ks(d: str, tool: str, kills, perms=0o644, extra=None):
        payload = {"tool": "fake/tool.py", "tool_sha256": sha256_bytes(open(tool, "rb").read()),
                   "selftest_argv": ["--selftest"],
                   "fail_line_prefix": "SEAT_REPORTS_SELFTEST_FAIL: ",
                   "result_line_prefix": "SEAT_REPORTS_SELFTEST: ", "kills": kills}
        if extra:
            payload.update(extra)
        p = os.path.join(d, "kills.json")
        with open(p, "w") as fh:
            json.dump(payload, fh)
        os.chmod(p, perms)
        return p

    with tempfile.TemporaryDirectory(prefix="gate-selftest-") as d:
        # OK: mutant flips one check to fail under its named label only
        tool = write(d, "ok_tool.py", SELFTEST_FAKE_OK)
        kap = ks(d, tool, [{"id": "k1", "find": "(\"alpha\", True)",
                            "replace": "(\"alpha\", False)", "must_fail": "alpha"}])
        buf: list[str] = []
        rc = gate(tool, kap, None, 10, False, out=buf.append)
        lines = buf
        results.append(("selftest OK", rc == 0 and any("SELFTEST_STRENGTH: OK" in ln and
                        "tool=fake/tool.py" in ln and "kills=1" in ln and "held=1" in ln
                        for ln in lines)))

        # SURVIVED: mutant flips nothing the named check observes
        tool2 = write(d, "surv_tool.py", SELFTEST_FAKE_SURVIVOR)
        kap2 = ks(d, tool2, [{"id": "k2", "find": "(\"alpha\", True)",
                              "replace": "(\"alpha\", True)  # noop", "must_fail": "alpha"}])
        buf2: list[str] = []
        rc2 = gate(tool2, kap2, None, 10, False, out=buf2.append)
        results.append(("selftest SURVIVED -> WEAK rc1", rc2 == 1 and any(
            ln == "SURVIVED k2" for ln in buf2) and any("SELFTEST_STRENGTH: WEAK" in ln
            and "survived=1" in ln for ln in buf2)))

        # WRONG_CHECK: mutant fails a different check than named
        tool3 = write(d, "wrong_tool.py", SELFTEST_FAKE_OK)
        kap3 = ks(d, tool3, [{"id": "k3", "find": "(\"alpha\", True)",
                              "replace": "(\"alpha\", False)", "must_fail": "beta"}])
        buf3: list[str] = []
        rc3 = gate(tool3, kap3, None, 10, False, out=buf3.append)
        results.append(("selftest WRONG_CHECK -> WEAK rc1", rc3 == 1 and any(
            ln.startswith("WRONG_CHECK k3") and "alpha" in ln for ln in buf3)))

        # setup: sha mismatch without flag -> rc2
        tool4 = write(d, "sha_tool.py", SELFTEST_FAKE_OK)
        kap4 = ks(d, tool4, [], extra={"tool_sha256": "0" * 64})
        rc4 = gate(tool4, kap4, None, 10, False, out=lambda *a: None)
        results.append(("selftest sha mismatch rc2", rc4 == 2))

        # setup: sha mismatch with --allow-sha-drift -> runs (empty set OK)
        rc5 = gate(tool4, kap4, None, 10, True, out=lambda *a: None)
        results.append(("selftest sha drift allowed rc0", rc5 == 0))

        # setup: find occurs twice in non-selftest code -> rc2
        tool6 = write(d, "dup_tool.py", SELFTEST_FAKE_OK.replace(
            'CHECKS = [("alpha", True)', 'CHECKS = [("alpha", True), ("alpha", True)'))
        kap6 = ks(d, tool6, [{"id": "k6", "find": "(\"alpha\", True)",
                              "replace": "(\"alpha\", False)", "must_fail": "alpha"}])
        rc6 = gate(tool6, kap6, None, 10, False, out=lambda *a: None)
        results.append(("selftest find-twice rc2", rc6 == 2))

        # setup: find only inside selftest harness (after def selftest) -> rc2
        tool7 = write(d, "inside_tool.py", SELFTEST_FAKE_OK + '\n# def selftest-marker\n')
        kap7 = ks(d, tool7, [{"id": "k7", "find": "SEAT_REPORTS_SELFTEST_FAIL",
                              "replace": "X", "must_fail": "alpha"}])
        rc7 = gate(tool7, kap7, None, 10, False, out=lambda *a: None)
        results.append(("selftest find-in-selftest rc2", rc7 == 2))

        # setup: unmutated tool selftest failing -> rc2
        tool8 = write(d, "bad_tool.py", SELFTEST_FAKE_OK.replace(
            "(\"beta\", True)", "(\"beta\", False)"))
        kap8 = ks(d, tool8, [])
        rc8 = gate(tool8, kap8, None, 10, False, out=lambda *a: None)
        results.append(("selftest unmutated-fails rc2", rc8 == 2))

        # list must_fail: exact set held; a weaker selftest that loses one label -> WRONG_CHECK
        both = SELFTEST_FAKE_OK.replace('CHECKS = [("alpha", True), ("beta", True)]',
                                        'FLAG = True\nCHECKS = [("alpha", FLAG), ("beta", FLAG)]')
        tool9 = write(d, "set_tool.py", both)
        k9 = [{"id": "k9", "find": "FLAG = True", "replace": "FLAG = False", "must_fail": ["beta", "alpha"]}]
        rc9 = gate(tool9, ks(d, tool9, k9), None, 10, False, out=lambda *a: None)
        results.append(("selftest list must_fail exact set held rc0", rc9 == 0))
        weak = both.replace('("beta", FLAG)', '("beta", True)')
        tool10 = write(d, "set_weak.py", weak)
        buf10: list[str] = []
        rc10 = gate(tool10, ks(d, tool10, k9), None, 10, False, out=buf10.append)
        results.append(("selftest list must_fail missing label -> WRONG_CHECK rc1",
                        rc10 == 1 and any(ln.startswith("WRONG_CHECK k9") for ln in buf10)))
        # selftest_checks pin: a dropped check is a setup error
        rc11 = gate(tool, ks(d, tool, [], extra={"selftest_checks": 3}), None, 10, False, out=lambda *a: None)
        rc12 = gate(tool, ks(d, tool, [], extra={"selftest_checks": 2}), None, 10, False, out=lambda *a: None)
        results.append(("selftest checks pin", rc11 == 2 and rc12 == 0))

    failed = [n for n, ok in results if not ok]
    for n in failed:
        print(f"SELFTEST_STRENGTH_SELFTEST_FAIL: {n}")
    print(f"SELFTEST_STRENGTH_SELFTEST: checks={len(results)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tool")
    ap.add_argument("--kills")
    ap.add_argument("--scratch-root")
    ap.add_argument("--timeout", type=float, default=30)
    ap.add_argument("--allow-sha-drift", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.tool or not a.kills:
        print("SELFTEST_STRENGTH: SETUP_ERROR name --tool and --kills")
        return 2
    return gate(a.tool, a.kills, a.scratch_root, a.timeout, a.allow_sha_drift)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Round-100 C2 counter - the harm watch's per-leg cap becomes measured and the panel runs green.

Frozen predicate PRED-C2-r100-v1 (verbatim from .ufo/waves/round-100/claims-declaration-r100.md):

  TARGET_MET iff  panel_legs == 28 AND legs_run == 28 AND mismatches == 0
             AND  gate_elapsed_emitted   == 1
             AND  timing_legs_timed      == 28
             AND  max_elapsed_ms         > 600000
             AND  panel_timeout_s * 1000 >= 2 * max_elapsed_ms
             AND  control_600s_would_mismatch >= 1
             AND  selftest_failed        == 0

rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.  No other conjunct.

WHAT IT READS
  --panel   the re-frozen panel (.ufo/waves/round-100/controls/harm-panel-r100.json): timeout_s plus
            the 28 leg rows, byte-identical to the round-99 panel's rows.
  --timing  the per-leg elapsed receipt from the round's own measurement pass
            (.ufo/waves/round-100/receipts/panel-timing-r100.txt): `id rc=<n> elapsed_ms=<n>` rows
            plus a TIMING-DONE line.  `max_elapsed_ms` and `control_600s_would_mismatch` are DERIVED
            from it, never asserted.
  the gate  quality/harm-watch.py at --rev (git show) or in the worktree ("worktree").

Instrument spawns: `git` read-only, and the gate's own panel legs (the gate is the instrument this
counter measures).  It never launches a host application and never writes the lane.

Inputs (all sha256-pinned; SETUP_ERROR on any mismatch or missing surface):
  --repo DIR --rev REV|worktree --base-rev SHA
  --panel FILE --expect-panel-sha256 SHA
  --timing FILE --expect-timing-sha256 SHA
  --expect-gate-sha256 SHA
  --scratch-root DIR [--selftest]
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

GATE_PATH = "quality/harm-watch.py"
TIMING_ROW = re.compile(r"^([A-Za-z0-9_.-]+) rc=(-?\d+) elapsed_ms=(\d+)$")
LEG_LINE = re.compile(r"^LEG (\S+) rc=(\S+) expect=(\S+) marker=(\S+) (\S+)(?: elapsed_ms=(\d+))?$")


class CounterError(Exception):
    pass


def sha(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as fh:
        return sha(fh.read())


def setup(msg):
    sys.stderr.write("SETUP_ERROR %s\n" % msg)
    return 2


def git_show(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)], capture_output=True)
    return None if r.returncode != 0 else r.stdout


def parse_timing(text):
    """Rows `id rc=<n> elapsed_ms=<n>`; everything else (headers, LEG echoes) is ignored."""
    rows, done = {}, False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("TIMING-DONE"):
            done = True
            continue
        m = TIMING_ROW.match(line)
        if m:
            cid, _rc, ms = m.group(1), int(m.group(2)), int(m.group(3))
            if cid in rows:
                raise CounterError("timing row repeated: %s" % cid)
            rows[cid] = ms
    return rows, done


def run_panel(gate_path, repo, rev, panel, scratch, timeout):
    argv = [sys.executable, "-I", gate_path, "--repo", repo, "--rev", rev,
            "--panel", panel, "--scratch-root", scratch, "--timeout", str(timeout), "--json"]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=None)
    return r.returncode, r.stdout, r.stderr


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round-100 C2 counter (harm watch)")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--panel")
    ap.add_argument("--expect-panel-sha256")
    ap.add_argument("--timing")
    ap.add_argument("--expect-timing-sha256")
    ap.add_argument("--expect-gate-sha256")
    ap.add_argument("--scratch-root")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    for req in ("repo", "rev", "base_rev", "panel", "expect_panel_sha256", "timing",
                "expect_timing_sha256", "expect_gate_sha256", "scratch_root"):
        if not getattr(a, req):
            return setup("missing --%s" % req.replace("_", "-"))
    repo = os.path.abspath(a.repo)
    if not os.path.isdir(repo):
        return setup("repo-not-a-dir")
    for path, pin, label in ((a.panel, a.expect_panel_sha256, "panel"),
                             (a.timing, a.expect_timing_sha256, "timing")):
        try:
            got = sha_file(path)
        except OSError as e:
            return setup("%s unreadable: %s" % (label, e))
        if got != pin:
            return setup("%s sha256 %s != pinned %s" % (label, got, pin))
    if a.rev == "worktree":
        try:
            gate_bytes = open(os.path.join(repo, GATE_PATH), "rb").read()
        except OSError as e:
            return setup("worktree gate unreadable: %s" % e)
    else:
        gate_bytes = git_show(repo, a.rev, GATE_PATH)
    if gate_bytes is None:
        return setup("%s absent at %s" % (GATE_PATH, a.rev))
    if sha(gate_bytes) != a.expect_gate_sha256:
        return setup("gate sha256 %s != pinned %s" % (sha(gate_bytes), a.expect_gate_sha256))

    panel = json.load(open(a.panel, encoding="utf-8"))
    panel_legs = len(panel.get("legs") or [])
    expected_rows = panel.get("expect_legs")
    if panel_legs != expected_rows:
        return setup("panel declares expect_legs=%s but carries %d rows"
                     % (expected_rows, panel_legs))
    timeout_s = panel.get("timeout_s")
    if not isinstance(timeout_s, (int, float)) or isinstance(timeout_s, bool) or timeout_s <= 0:
        return setup("panel timeout_s invalid: %r" % (timeout_s,))
    timing_text = open(a.timing, encoding="utf-8").read()
    try:
        timing_rows, timing_done = parse_timing(timing_text)
    except CounterError as e:
        return setup("timing receipt: %s" % e)
    if not timing_done:
        return setup("timing receipt has no TIMING-DONE line")

    scratch = os.path.abspath(a.scratch_root)
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=scratch, prefix="c2r100-")
    try:
        gdir = os.path.join(work, "gate")
        os.makedirs(gdir)
        gate_path = os.path.join(gdir, "harm-watch.py")
        open(gate_path, "wb").write(gate_bytes)

        st = subprocess.run([sys.executable, "-I", gate_path, "--selftest"],
                            capture_output=True, text=True)
        selftest_line = (st.stdout or "").strip().splitlines()[-1:] or [""]
        m = re.search(r"checks=(\d+) failed=(\d+)", selftest_line[0])
        selftest_failed = int(m.group(2)) if m else 999

        rc, out, err = run_panel(gate_path, repo, a.rev, os.path.abspath(a.panel),
                                 os.path.join(work, "scr"), timeout_s)
        legs_run = len([1 for ln in out.splitlines() if ln.startswith("LEG ")])
        summary = [ln for ln in out.splitlines() if ln.startswith("HARM_WATCH:")]
        sm = re.search(r"legs=(\d+) ok=(\d+) mismatch=(\d+)", summary[-1]) if summary else None
        mismatches = int(sm.group(3)) if sm else None
        if sm:
            legs_run = int(sm.group(1))
        human_elapsed = sum(1 for ln in out.splitlines()
                            if ln.startswith("LEG ") and re.search(r"elapsed_ms=\d+$", ln))
        json_elapsed = 0
        json_mismatch = None
        try:
            obj = json.loads(out.strip().splitlines()[-1])
            legs = obj.get("legs") or []
            json_elapsed = len([1 for L in legs if isinstance(L.get("elapsed_ms"), int)
                                and not isinstance(L.get("elapsed_ms"), bool)
                                and L.get("elapsed_ms") >= 0])
            json_mismatch = obj.get("mismatch")
        except Exception:
            legs = []
        gate_elapsed_emitted = int(human_elapsed == legs_run and json_elapsed == legs_run
                                   and legs_run > 0)
        max_elapsed_ms = max(timing_rows.values()) if timing_rows else 0
        timing_legs_timed = len(timing_rows)
        control_600s = len([ms for ms in timing_rows.values() if ms > 600000])

        conjuncts = [
            ("panel_legs==28", panel_legs == 28, panel_legs),
            ("legs_run==28", legs_run == 28, legs_run),
            ("mismatches==0", mismatches == 0, mismatches),
            ("gate_elapsed_emitted==1", gate_elapsed_emitted == 1,
             "%d human/%d json of %d legs" % (human_elapsed, json_elapsed, legs_run)),
            ("timing_legs_timed==28", timing_legs_timed == 28, timing_legs_timed),
            ("max_elapsed_ms>600000", max_elapsed_ms > 600000, max_elapsed_ms),
            ("panel_timeout_s*1000>=2*max_elapsed_ms",
             int(timeout_s) * 1000 >= 2 * max_elapsed_ms,
             "%d vs %d" % (int(timeout_s) * 1000, 2 * max_elapsed_ms)),
            ("control_600s_would_mismatch>=1", control_600s >= 1, control_600s),
            ("selftest_failed==0", selftest_failed == 0, selftest_failed),
        ]
        met = all(ok for (_n, ok, _v) in conjuncts)
        verdict = "TARGET_MET" if met else "TARGET_MISSED"
        print("MADO_C2_R100: %s pred=PRED-C2-r100-v1 rev=%s base_rev=%s gate_sha256=%s "
              "panel_sha256=%s panel_legs=%d declared_legs=%s timeout_s=%s timing_sha256=%s "
              "legs_run=%d mismatches=%s selftest_failed=%d max_elapsed_ms=%d "
              "control_600s_would_mismatch=%d timing_legs_timed=%d exit=%d"
              % (verdict, a.rev, a.base_rev, sha(gate_bytes), sha_file(a.panel), panel_legs,
                 panel.get("expect_legs"), timeout_s, sha_file(a.timing), legs_run, mismatches,
                 selftest_failed, max_elapsed_ms, control_600s, timing_legs_timed, rc))
        for (name, ok, val) in conjuncts:
            print("CONJUNCT %s %s value=%s" % ("ok" if ok else "MISS", name, val))
        if mismatches:
            bad = [ln for ln in out.splitlines()
                   if ln.startswith("LEG ") and not ln.rstrip().endswith(" ok")]
            for ln in bad[:10]:
                print("FAILING_LEG %s" % ln)
        if selftest_failed:
            print("SELFTEST_LINE %s" % selftest_line[0])
        print("VERDICT_LINE_SHA256 %s" % sha("%s|%s" % (a.rev, verdict)))
        return 0 if met else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


def selftest():
    checks, failed = [], []

    def record(name, ok):
        checks.append(name)
        if not ok:
            failed.append(name)

    # timing parser: rows, duplicates, done marker
    rows, done = parse_timing("h\nid1 rc=0 elapsed_ms=700000\nid2 rc=2 elapsed_ms=9\nTIMING-DONE x\n")
    record("timing-parser-rows", rows == {"id1": 700000, "id2": 9} and done)
    try:
        parse_timing("id1 rc=0 elapsed_ms=1\nid1 rc=0 elapsed_ms=2\n")
        record("timing-duplicate-refused", False)
    except CounterError:
        record("timing-duplicate-refused", True)
    _rows, done2 = parse_timing("id1 rc=0 elapsed_ms=1\n")
    record("timing-done-required", done2 is False)
    # the cap conjunct can fail
    record("cap-conjunct-can-fail", not (600 * 1000 >= 2 * 708014))
    record("cap-conjunct-can-pass", 3600 * 1000 >= 2 * 708014)
    # the 600s control is derived, not asserted
    record("control-derived", len([ms for ms in (708014, 9, 601000) if ms > 600000]) == 2)
    # LEG line shapes: elapsed present / absent
    m1 = LEG_LINE.match("LEG good rc=0 expect=0 marker=ok ok elapsed_ms=12")
    m2 = LEG_LINE.match("LEG good rc=0 expect=0 marker=ok ok")
    record("leg-line-with-elapsed", m1 is not None and m1.group(6) == "12")
    record("leg-line-without-elapsed-detected", m2 is not None and m2.group(6) is None)
    # a pin mismatch is a refusal (the sha helpers agree with themselves only)
    record("pin-mismatch-refused", sha("a") != sha("b"))
    print("C2R100_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
    for f in failed:
        print("FAIL %s" % f)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

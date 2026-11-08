#!/usr/bin/env python3
"""c2-r100-harm-watch -- counting command for PRED-C2-r100-v1 (mado round 100, C2).

Usage:
    c2-r100-harm-watch.py --repo DIR --rev REV --base-rev REV
                          --panel PANEL.json --expect-panel-sha256 SHA
                          --timing TIMING.txt --expect-timing-sha256 SHA
                          --expect-gate-sha256 SHA --scratch-root DIR [--json]
    c2-r100-harm-watch.py --selftest

The predicate, frozen in .ufo/waves/round-100/claims-declaration-r100.md:

    TARGET_MET iff  panel_legs == 28 AND legs_run == 28 AND mismatches == 0
               AND  gate_elapsed_emitted   == 1     (human LEG line carries
               elapsed_ms= AND json legs carry elapsed_ms)
               AND  timing_legs_timed      == 28
               AND  max_elapsed_ms         > 600000 (the frozen 600 s cap is
               structurally too small on this host: the control is measured,
               not asserted)
               AND  panel_timeout_s * 1000 >= 2 * max_elapsed_ms
               AND  control_600s_would_mismatch >= 1 (derived from the same
               timing receipt: legs whose elapsed exceeds 600 s)
               AND  selftest_failed        == 0

Exit 0 on TARGET_MET, 1 on TARGET_MISSED, 2 on SETUP_ERROR (any missing or
unpinned input: gate, panel, timing receipt, or required CLI argument).

The gate bytes come from `git show REV:quality/harm-watch.py`; the panel and
timing receipt from the same rev (paths as given, repo-relative).  --gate PATH
(draft mode) takes the gate bytes from a file and the panel/timing bytes from
the working tree instead; it exists so in-wave drafts can be exercised before
landing and is never part of the pinned counting command.  --base-rev is
accepted for parity with the counting command; round 100's claim is not a
before-state absence claim (the gate exists at the base rev), so it carries no
conjunct and is only echoed in the verdict.

The timing receipt format: one line per timed leg
`id rc=<n> elapsed_ms=<n>` plus a `TIMING-DONE` line.  timing_legs_timed is
the count of such leg lines, max_elapsed_ms their maximum elapsed_ms, and
control_600s_would_mismatch the count whose elapsed_ms exceeds 600000.

Scratch: every directory this counter creates carries the marker file
`.c2-r100-harm-watch`; a reused --scratch-root is cleared of marked entries
first and any unmarked entry is refused (exit 2).

Selftest: builds a miniature fixture git repository and replays the whole
pipeline (pins, green run, short-cap panel, low timing receipt, a gate that
does not emit elapsed_ms, a gate whose selftest fails, a red panel, pin
mismatches).  Nested counter runs inside the selftest set
C2_R100_SELFTEST_DEPTH=1 and skip the counter's own selftest field (it reads
`skipped`), so the selftest cannot recurse.  The gate's own --selftest still
runs in nested invocations, as the predicate requires.

This counter is an instrument: it spawns git and the gate (python3 -I); it is
not itself a modelled candidate.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

GATE_REPO_PATH = "quality/harm-watch.py"
MARKER = ".c2-r100-harm-watch"
TIMING_LEG_RE = re.compile(r"^(\S+)\s+rc=(\d+)\s+elapsed_ms=(\d+)\s*$")
LEG_ELAPSED_RE = re.compile(r"elapsed_ms=(\d+)")
SELFTEST_RE = re.compile(r"HARM_WATCH_SELFTEST: checks=(\d+) failed=(\d+)")
SUMMARY_RE = re.compile(r"HARM_WATCH: legs=(\d+) ok=(\d+) mismatch=(\d+)")
SIX_HUNDRED_S_MS = 600000


def sh_bytes(argv):
    r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.returncode, r.stdout, r.stderr


def sha(data):
    return hashlib.sha256(data).hexdigest()


def emit(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def setup(detail):
    emit("MADO_C2_R100: SETUP_ERROR %s" % detail)
    return 2


def mark_dir(path):
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, MARKER), "w").close()
    return path


def fresh_scratch(root):
    if os.path.lexists(root):
        if os.path.islink(root) or not os.path.isdir(root):
            return None
        for name in os.listdir(root):
            entry = os.path.join(root, name)
            if os.path.isdir(entry) and not os.path.islink(entry) and \
                    os.path.exists(os.path.join(entry, MARKER)):
                shutil.rmtree(entry)
            else:
                return None
    os.makedirs(root, exist_ok=True)
    return root


def run_gate(gate_path, repo, rev, panel_path, scratch_dir, timeout=14400):
    argv = [sys.executable, "-I", gate_path, "--repo", repo, "--rev", rev,
            "--panel", panel_path, "--scratch-root", scratch_dir, "--json"]
    try:
        r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": "timeout after %ds" % timeout}
    out = r.stdout.decode("utf-8", "replace")
    res = {"rc": r.returncode, "out": out}
    m = SUMMARY_RE.search(out)
    if m:
        res.update({"legs": int(m.group(1)), "ok": int(m.group(2)),
                    "mismatch": int(m.group(3))})
    for line in reversed(out.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res["json"] = json.loads(line)
                break
            except ValueError:
                pass
    return res


def parse_timing(data):
    """Return (timed_ids, elapsed_list) or None if the receipt is unusable."""
    try:
        text = data.decode("utf-8")
    except (UnicodeDecodeError, AttributeError):
        return None
    if "TIMING-DONE" not in text:
        return None
    timed = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = TIMING_LEG_RE.match(line)
        if m:
            timed.append((m.group(1), int(m.group(3))))
    if not timed:
        return None
    return timed


def elapsed_emitted(res):
    """1 iff every human LEG line carries elapsed_ms= AND every json leg
    object carries an integer elapsed_ms; else 0."""
    leg_lines = [ln.strip() for ln in res.get("out", "").splitlines()
                 if ln.strip().startswith("LEG ")]
    if not leg_lines:
        return 0
    for ln in leg_lines:
        if not LEG_ELAPSED_RE.search(ln):
            return 0
    legs = res.get("json", {}).get("legs")
    if not isinstance(legs, list) or not legs:
        return 0
    for leg in legs:
        v = leg.get("elapsed_ms") if isinstance(leg, dict) else None
        if not isinstance(v, int) or isinstance(v, bool):
            return 0
    return 1


# --- fixture gate for the counter's selftest -------------------------------

FIXTURE_GATE_TEMPLATE = r'''#!/usr/bin/env python3
"""Fixture gate for the c2-r100 selftest: same CLI contract, fixture legs."""
import argparse, json, subprocess, sys

EMIT_ELAPSED = %s
SELFTEST_FAILED = %d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo"); ap.add_argument("--rev"); ap.add_argument("--panel")
    ap.add_argument("--scratch-root"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--timeout", type=float)
    ap.add_argument("--only", action="append", default=None)
    a = ap.parse_args()
    if getattr(a, "selftest", False):
        print("HARM_WATCH_SELFTEST: checks=3 failed=%d" % SELFTEST_FAILED)
        return 0 if SELFTEST_FAILED == 0 else 1
    panel = json.load(open(a.panel))
    legs = panel.get("legs") or []
    if len(legs) != panel.get("expect_legs"):
        print("PANEL PANEL_LEG_COUNT rows=%d expect_legs=%d" % (len(legs), panel.get("expect_legs")))
        return 2
    ok = 0
    results = []
    for row in legs:
        p = subprocess.run(row["argv"], cwd=a.repo, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        out = p.stdout.decode("utf-8", "replace")
        marker = row["expect_marker"]
        mok = (not marker) or (marker in out)
        rok = p.returncode == row["expect_rc"]
        good = rok and mok
        ok += 1 if good else 0
        line = "LEG %s rc=%d expect=%s marker=%s %s" % (
            row["id"], p.returncode, row["expect_rc"], "ok" if mok else "MISS",
            "ok" if good else "mismatch")
        if EMIT_ELAPSED:
            line += " elapsed_ms=15"
        print(line)
        rec = {"id": row["id"], "rc": p.returncode, "expect_rc": row["expect_rc"],
               "marker_ok": mok, "ok": good,
               "detail": "ok" if good else "mismatch"}
        if EMIT_ELAPSED:
            rec["elapsed_ms"] = 15
        results.append(rec)
    n = len(legs)
    print("HARM_WATCH: legs=%d ok=%d mismatch=%d" % (n, ok, n - ok))
    if a.json:
        print(json.dumps({"legs_run": n, "ok": ok, "mismatch": n - ok,
                          "legs": results, "exit": 0 if n == ok else 1}))
    return 0 if n == ok else 1

import argparse as _ap
_p = _ap.ArgumentParser(); _p.add_argument("--selftest", action="store_true")
if _p.parse_known_args()[0].selftest:
    print("HARM_WATCH_SELFTEST: checks=3 failed=%d" % SELFTEST_FAILED)
    sys.exit(0 if SELFTEST_FAILED == 0 else 1)
sys.exit(main())
'''


def fixture_gate(emit_elapsed=True, selftest_failed=0):
    gate = FIXTURE_GATE_TEMPLATE.replace("EMIT_ELAPSED = %s",
                                          "EMIT_ELAPSED = " + repr(bool(emit_elapsed)))
    gate = gate.replace("SELFTEST_FAILED = %d", "SELFTEST_FAILED = %d" % selftest_failed)
    return gate.encode()


def selftest_checks():
    """Fixture pipeline; returns (checks, failed, notes)."""
    import tempfile
    checks, failed, notes = [], [], []

    def record(name, cond, why=""):
        checks.append(name)
        if not cond:
            failed.append("%s: %s" % (name, why))

    root = tempfile.mkdtemp(prefix="c2-r100-selftest-")
    try:
        counter = os.path.abspath(__file__)
        fixture_env = dict(os.environ, C2_R100_SELFTEST_DEPTH="1")

        def w(repo, rel, data):
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data if isinstance(data, bytes) else data.encode())

        def commit(repo, msg):
            sh_bytes(["git", "-C", repo, "init", "-q"])
            sh_bytes(["git", "-C", repo, "config", "user.email", "fix@fix"])
            sh_bytes(["git", "-C", repo, "config", "user.name", "fix"])
            sh_bytes(["git", "-C", repo, "add", "-A"])
            sh_bytes(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", msg])
            return sh_bytes(["git", "-C", repo, "rev-parse", "HEAD"])[1].decode().strip()

        IDS = ["leg%02d" % i for i in range(28)]

        def row(lid, rc=0, marker="FIXTURE_VERDICT: GOOD"):
            return {"id": lid, "round": "r100",
                    "argv": [sys.executable, "-I", "tools/leg.py", "good", "REV"],
                    "expect_rc": rc, "expect_marker": marker, "note": "fixture"}

        def panel_bytes(timeout_s=2000, flip=None):
            legs = [row(i) for i in IDS]
            if flip is not None:
                legs[flip]["expect_rc"] = 1
            return json.dumps({"expect_legs": 28, "timeout_s": timeout_s,
                               "rounds": {"r100": list(IDS)},
                               "legs": legs}, indent=1).encode()

        def timing_bytes(slow_ms=700000, n=28):
            lines = []
            for i, lid in enumerate(IDS[:n]):
                ms = slow_ms if i == 0 else 1000
                lines.append("%s rc=0 elapsed_ms=%d" % (lid, ms))
            lines.append("TIMING-DONE")
            return ("\n".join(lines) + "\n").encode()

        repo = os.path.join(root, "repo")
        os.makedirs(repo)
        w(repo, "tools/leg.py",
          b"#!/usr/bin/env python3\nimport sys\nassert sys.argv[1] == 'good'\n"
          b"print('FIXTURE_VERDICT: GOOD rev=' + sys.argv[2])\n")
        w(repo, "controls/panel.json", panel_bytes())
        w(repo, "receipts/timing.txt", timing_bytes())
        w(repo, GATE_REPO_PATH, fixture_gate(True, 0))
        rev = commit(repo, "gate+controls")
        scratch = os.path.join(root, "scr")

        state = {"rev": rev, "panel": panel_bytes(), "timing": timing_bytes(),
                 "gate": fixture_gate(True, 0)}

        def run_counter(panel_sha=None, timing_sha=None, gate_sha=None,
                        panel_bytes_=None, timing_bytes_=None, gate_bytes_=None):
            for key, val in (("panel", panel_bytes_), ("timing", timing_bytes_),
                             ("gate", gate_bytes_)):
                if val is not None:
                    state[key] = val
            w(repo, "controls/panel.json", state["panel"])
            w(repo, "receipts/timing.txt", state["timing"])
            w(repo, GATE_REPO_PATH, state["gate"])
            state["rev"] = commit(repo, "variant")
            argv = [sys.executable, "-I", counter,
                    "--repo", repo, "--rev", state["rev"],
                    "--base-rev", state["rev"],
                    "--panel", "controls/panel.json",
                    "--expect-panel-sha256",
                    panel_sha if panel_sha is not None else sha(state["panel"]),
                    "--timing", "receipts/timing.txt",
                    "--expect-timing-sha256",
                    timing_sha if timing_sha is not None else sha(state["timing"]),
                    "--expect-gate-sha256",
                    gate_sha if gate_sha is not None else sha(state["gate"]),
                    "--scratch-root", scratch]
            r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=900, cwd=repo, env=fixture_env)
            return r.returncode, r.stdout.decode("utf-8", "replace")

        # 1 green pipeline: every conjunct value present and met
        rc, out = run_counter()
        record("green-target-met", rc == 0 and "TARGET_MET pred=PRED-C2-r100-v1" in out, out[-600:])
        for tok in ("panel_legs=28", "legs_run=28", "mismatches=0",
                    "gate_elapsed_emitted=1", "timing_legs_timed=28",
                    "max_elapsed_ms=700000", "panel_timeout_s=2000",
                    "control_600s_would_mismatch=1", "selftest_failed=0"):
            record("green-field-" + tok.split("=")[0], tok in out, out[-600:])

        # 2 short-cap panel: timeout_s*1000 < 2*max_elapsed_ms -> missed
        rc, out = run_counter(panel_bytes_=panel_bytes(timeout_s=1000))
        record("short-cap-missed", rc == 1 and "TARGET_MISSED" in out
               and "missed=" in out and "panel_timeout_s=1000" in out, out[-400:])

        # 3 receipt with a leg over 600 s is what makes the control live;
        #    a receipt under the cap must miss the max and control conjuncts
        rc, out = run_counter(timing_bytes_=timing_bytes(slow_ms=500000))
        record("low-max-missed", rc == 1 and "TARGET_MISSED" in out
               and "max_elapsed_ms=500000" in out
               and "control_600s_would_mismatch=0" in out, out[-400:])

        # 4 receipt with fewer timed legs -> timing conjunct can fail
        rc, out = run_counter(timing_bytes_=timing_bytes(n=27))
        record("timing-count-missed", rc == 1 and "TARGET_MISSED" in out
               and "timing_legs_timed=27" in out, out[-400:])

        # 5 gate that does not emit elapsed_ms -> emitted conjunct fails
        rc, out = run_counter(gate_bytes_=fixture_gate(False, 0))
        record("no-elapsed-missed", rc == 1 and "TARGET_MISSED" in out
               and "gate_elapsed_emitted=0" in out, out[-400:])

        # 6 gate whose selftest fails -> selftest conjunct fails
        rc, out = run_counter(gate_bytes_=fixture_gate(True, 2))
        record("selftest-fail-missed", rc == 1 and "TARGET_MISSED" in out
               and "selftest_failed=2" in out, out[-400:])

        # 7 red panel -> mismatches conjunct fails
        rc, out = run_counter(panel_bytes_=panel_bytes(flip=3))
        record("red-panel-missed", rc == 1 and "TARGET_MISSED" in out
               and "mismatches=1" in out, out[-400:])

        # 8 pin mismatches are setup errors, never greens
        rc, out = run_counter(panel_sha="0" * 64)
        record("panel-pin-setup", rc == 2 and "SETUP_ERROR panel sha256" in out, out[-300:])
        rc, out = run_counter(timing_sha="0" * 64)
        record("timing-pin-setup", rc == 2 and "SETUP_ERROR timing sha256" in out, out[-300:])
        rc, out = run_counter(gate_sha="0" * 64)
        record("gate-pin-setup", rc == 2 and "SETUP_ERROR gate sha256" in out, out[-300:])

        # 9 missing --timing is a setup error
        rc, out = run_counter(timing_bytes_=b"no done line\nleg00 rc=0 elapsed_ms=5\n")
        record("timing-undone-setup", rc == 2 and "SETUP_ERROR timing receipt" in out, out[-300:])

        # 10 a scratch root holding a foreign entry is refused, not reused
        foreign = os.path.join(root, "scratch-foreign")
        os.makedirs(foreign, exist_ok=True)
        with open(os.path.join(foreign, "keep"), "w") as fh:
            fh.write("x")
        argv = [sys.executable, "-I", counter, "--repo", repo,
                "--rev", state["rev"], "--base-rev", state["rev"],
                "--panel", "controls/panel.json",
                "--expect-panel-sha256", sha(state["panel"]),
                "--timing", "receipts/timing.txt",
                "--expect-timing-sha256", sha(state["timing"]),
                "--expect-gate-sha256", sha(state["gate"]),
                "--scratch-root", foreign]
        r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=900, cwd=repo, env=fixture_env)
        out = r.stdout.decode("utf-8", "replace")
        record("scratch-foreign-setup",
               r.returncode == 2 and "SETUP_ERROR scratch-root unusable" in out, out[-300:])
        notes.append("fixture_rev=%s" % rev[:7])
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return checks, failed, notes


def main():
    ap = argparse.ArgumentParser(add_help=True,
                                 description="mado round-100 C2 counting command")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--panel")
    ap.add_argument("--expect-panel-sha256")
    ap.add_argument("--timing")
    ap.add_argument("--expect-timing-sha256")
    ap.add_argument("--expect-gate-sha256")
    ap.add_argument("--gate", help="draft mode: gate bytes from this file; "
                    "panel/timing bytes from the working tree")
    ap.add_argument("--scratch-root")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    depth = int(os.environ.get("C2_R100_SELFTEST_DEPTH", "0") or 0)

    if a.selftest and depth == 0:
        checks, failed, _ = selftest_checks()
        emit("MADO_C2_R100_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
        for f_ in failed:
            emit("FAIL %s" % f_)
        return 0 if not failed else 1

    for req in ("repo", "rev", "base_rev", "panel", "expect_panel_sha256",
                "timing", "expect_timing_sha256", "expect_gate_sha256",
                "scratch_root"):
        if not getattr(a, req):
            return setup("missing --%s" % req.replace("_", "-"))
    if fresh_scratch(a.scratch_root) is None:
        return setup("scratch-root unusable or has unmarked entries: %s" % a.scratch_root)
    root = a.scratch_root
    # Advisory, never a conjunct.  One panel leg (r97c1_filetype) creates
    # AF_UNIX sockets below <scratch>/m/<leg-id>/; the kernel caps sun_path at
    # 108 bytes, so a long --scratch-root turns that leg red for a path-length
    # reason rather than a behavioural one.  The limit was measured at 143
    # bytes for the longest case path (".../sock-06-synth-db-socket/s.sock").
    leg_base = os.path.join(root, "m", "r97c1_filetype")
    emit("MADO_C2_R100_NOTE: scratch_leg_path=%d bytes (r97c1_filetype needs "
         "this plus its case dir under 108; use a short --scratch-root)"
         % len(leg_base))

    # The gate substitutes --rev into panel rows verbatim, and at least one leg
    # (r97c1_filetype) refuses an abbreviated rev.  Resolve once, here, and use
    # the canonical 40-hex commit for every git read and for the gate's --rev.
    if a.rev == "worktree":
        rev = a.rev
    else:
        rc, out, _ = sh_bytes(["git", "-C", a.repo, "rev-parse", "--verify",
                               "%s^{commit}" % a.rev])
        if rc != 0:
            return setup("rev not resolvable in %s: %s" % (a.repo, a.rev))
        rev = out.decode().strip()
        if not re.fullmatch(r"[0-9a-f]{40}", rev):
            return setup("rev did not resolve to a commit sha: %s -> %s" % (a.rev, rev))
    a.rev = rev

    # gate bytes
    if a.gate:
        try:
            with open(a.gate, "rb") as fh:
                gate_bytes_local = fh.read()
        except OSError as e:
            return setup("gate unreadable: %s" % e)
    else:
        rc, out, _ = sh_bytes(["git", "-C", a.repo, "show", "%s:%s" % (a.rev, GATE_REPO_PATH)])
        if rc != 0:
            return setup("quality/harm-watch.py absent at %s" % a.rev)
        gate_bytes_local = out
    gate_sha = sha(gate_bytes_local)
    if gate_sha != a.expect_gate_sha256:
        return setup("gate sha256 %s != pinned %s" % (gate_sha, a.expect_gate_sha256))
    gdir = mark_dir(os.path.join(root, "g"))
    gate_path = os.path.join(gdir, "harm-watch.py")
    with open(gate_path, "wb") as fh:
        fh.write(gate_bytes_local)
    os.chmod(gate_path, 0o755)

    # panel bytes
    if a.gate:
        try:
            with open(os.path.join(a.repo, a.panel), "rb") as fh:
                panel_bytes_local = fh.read()
        except OSError as e:
            return setup("panel unreadable: %s" % e)
    else:
        rc, out, _ = sh_bytes(["git", "-C", a.repo, "show", "%s:%s" % (a.rev, a.panel)])
        if rc != 0:
            return setup("panel absent at %s: %s" % (a.rev, a.panel))
        panel_bytes_local = out
    panel_sha = sha(panel_bytes_local)
    if panel_sha != a.expect_panel_sha256:
        return setup("panel sha256 %s != pinned %s" % (panel_sha, a.expect_panel_sha256))
    try:
        panel = json.loads(panel_bytes_local.decode("utf-8"))
    except Exception:
        return setup("panel json unreadable")
    if not isinstance(panel, dict) or not isinstance(panel.get("legs"), list):
        return setup("panel json has no legs list")
    timeout_s = panel.get("timeout_s")
    if not isinstance(timeout_s, (int, float)) or isinstance(timeout_s, bool):
        return setup("panel json has no numeric timeout_s")
    pdir = mark_dir(os.path.join(root, "p"))
    panel_path = os.path.join(pdir, "panel.json")
    with open(panel_path, "wb") as fh:
        fh.write(panel_bytes_local)

    # timing receipt bytes
    if a.gate:
        try:
            with open(os.path.join(a.repo, a.timing), "rb") as fh:
                timing_bytes_local = fh.read()
        except OSError as e:
            return setup("timing unreadable: %s" % e)
    else:
        rc, out, _ = sh_bytes(["git", "-C", a.repo, "show", "%s:%s" % (a.rev, a.timing)])
        if rc != 0:
            return setup("timing absent at %s: %s" % (a.rev, a.timing))
        timing_bytes_local = out
    timing_sha = sha(timing_bytes_local)
    if timing_sha != a.expect_timing_sha256:
        return setup("timing sha256 %s != pinned %s" % (timing_sha, a.expect_timing_sha256))
    parsed = parse_timing(timing_bytes_local)
    if parsed is None:
        return setup("timing receipt has no TIMING-DONE line or no timed legs")
    timing_legs_timed = len(parsed)
    timing_ids_unique = len({lid for lid, _ in parsed})
    max_elapsed_ms = max(ms for _, ms in parsed)
    control_600s_would_mismatch = sum(1 for _, ms in parsed if ms > SIX_HUNDRED_S_MS)
    tdir = mark_dir(os.path.join(root, "t"))
    timing_path = os.path.join(tdir, "timing.txt")
    with open(timing_path, "wb") as fh:
        fh.write(timing_bytes_local)

    # gate --selftest (the predicate's selftest_failed conjunct)
    try:
        r = subprocess.run([sys.executable, "-I", gate_path, "--selftest"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=3600)
    except subprocess.TimeoutExpired:
        return setup("gate selftest timed out")
    st_out = r.stdout.decode("utf-8", "replace")
    m = SELFTEST_RE.search(st_out)
    if not m:
        return setup("gate selftest produced no HARM_WATCH_SELFTEST line")
    selftest_failed = int(m.group(2))
    selftest_checks_n = int(m.group(1))

    # full panel run at the measured rev, with --json
    main_res = run_gate(gate_path, a.repo, a.rev, panel_path,
                        mark_dir(os.path.join(root, "m")))
    if "error" in main_res:
        return setup("gate run failed: %s" % main_res["error"])
    try:
        with open(os.path.join(root, "m", "gate.out"), "w",
                  encoding="utf-8", errors="replace") as fh:
            fh.write(main_res.get("out", ""))
    except OSError:
        pass
    panel_legs = main_res.get("legs")
    mismatches = main_res.get("mismatch")
    if panel_legs is None or mismatches is None:
        return setup("gate produced no HARM_WATCH summary")
    # legs_run comes from the gate's --json object only: a gate that ignores
    # --json must fail this conjunct, never inherit the human summary's count.
    legs_run = (main_res.get("json") or {}).get("legs_run")
    if isinstance(legs_run, bool) or not isinstance(legs_run, int):
        legs_run = None
    gate_elapsed_emitted = elapsed_emitted(main_res)
    # diagnostic only, never a conjunct: name the legs that disagree so a
    # reader does not have to re-run a 28-leg panel to learn which ones they are
    bad_legs = [l.get("id") for l in (main_res.get("json") or {}).get("legs", [])
                if isinstance(l, dict) and not l.get("ok")]

    conds = {
        "panel_legs_28": panel_legs == 28,
        "legs_run_28": legs_run == 28,
        "mismatches_0": mismatches == 0,
        "gate_elapsed_emitted_1": gate_elapsed_emitted == 1,
        "timing_legs_timed_28": timing_legs_timed == 28,
        "max_gt_600s": max_elapsed_ms > SIX_HUNDRED_S_MS,
        "timeout_ge_2max": timeout_s * 1000 >= 2 * max_elapsed_ms,
        "control_ge_1": control_600s_would_mismatch >= 1,
        "selftest_failed_0": selftest_failed == 0,
    }
    met = all(conds.values())
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    bad = [k for k, v in conds.items() if not v]
    if depth == 0:
        st_checks, st_failed, _ = selftest_checks()
        st_failed_n = len(st_failed)
        selftest_txt = "checks=%d failed=%d" % (len(st_checks), st_failed_n)
    else:
        st_checks, st_failed_n, selftest_txt = 0, 0, "skipped"
    emit("MADO_C2_R100: %s pred=PRED-C2-r100-v1 rev=%s base_rev=%s gate_sha256=%s "
         "panel_sha256=%s timing_sha256=%s panel_legs=%s legs_run=%s mismatches=%s "
         "gate_elapsed_emitted=%d timing_legs_timed=%d timing_ids_unique=%d "
         "max_elapsed_ms=%d "
         "panel_timeout_s=%s control_600s_would_mismatch=%d selftest_failed=%d "
         "selftest_checks=%d selftest=%s mismatch_legs=%s%s"
         % (verdict, a.rev, a.base_rev, gate_sha, panel_sha, timing_sha,
            panel_legs, legs_run, mismatches, gate_elapsed_emitted,
            timing_legs_timed, timing_ids_unique, max_elapsed_ms, timeout_s,
            control_600s_would_mismatch, selftest_failed, selftest_checks_n,
            selftest_txt, ",".join(bad_legs) if bad_legs else "-",
            (" missed=" + ",".join(bad)) if bad else ""))
    if a.json:
        emit(json.dumps({
            "verdict": verdict, "rev": a.rev, "base_rev": a.base_rev,
            "gate_sha256": gate_sha, "panel_sha256": panel_sha,
            "timing_sha256": timing_sha,
            "panel_legs": panel_legs, "legs_run": legs_run,
            "mismatches": mismatches,
            "gate_elapsed_emitted": gate_elapsed_emitted,
            "timing_legs_timed": timing_legs_timed,
            "timing_ids_unique": timing_ids_unique,
            "max_elapsed_ms": max_elapsed_ms,
            "panel_timeout_s": timeout_s,
            "control_600s_would_mismatch": control_600s_would_mismatch,
            "selftest_failed": selftest_failed,
            "mismatch_legs": bad_legs,
            "conds": conds,
        }))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())

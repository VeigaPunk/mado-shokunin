#!/usr/bin/env python3
"""c2-r99-harm-watch -- counting command for PRED-C2-r99-v1 (mado round 99, C2).

Usage:
    c2-r99-harm-watch.py --repo DIR --rev REV --base-rev REV
                         --panel PANEL.json --expect-panel-sha256 SHA
                         --planted-dir DIR --expect-gate-sha256 SHA
                         --scratch-root DIR [--json]
    c2-r99-harm-watch.py --selftest

The counting command pins the gate and panel bytes, runs the gate at --rev
over the frozen panel and over each planted control, and evaluates:

    TARGET_MET iff panel_legs == declared_legs
              AND panel_legs >= 20
              AND legs_run == panel_legs
              AND mismatches == 0
              AND planted_dropped_leg_flagged == 1
              AND planted_wrong_expect_flagged == 1
              AND stub_flagged == 1
              AND selftest_checks >= 12 AND selftest_failed == 0

Exit 0 on TARGET_MET, 1 on TARGET_MISSED, 2 on SETUP_ERROR.  Separability:
at a rev where quality/harm-watch.py does not exist the command prints
`MADO_HARM_WATCH: SETUP_ERROR quality/harm-watch.py absent at <rev>` and
exits 2; if it exists already at --base-rev the claim's before-state is
void and it exits 2 with `present at base-rev`.

The gate bytes come from `git show REV:quality/harm-watch.py`; the panel
and the planted controls from the same rev (paths as given,
repo-relative).  --gate PATH (draft mode) takes the gate, panel and
planted bytes from the working tree instead; it exists so the in-wave
drafts can be exercised before landing and is never part of the pinned
counting command.

The stub control writes a fake always-OK gate into the scratch tree and
runs it over the planted dropped-leg panel: the stub reports ok while the
real gate flags the plant, so `stub=flagged=1` is emitted iff the stub's
verdict disagrees with the real gate's verdict on that red panel.

Planted controls (names fixed): clean.json (the panel itself),
dropped-leg.json (one row removed, expect_legs unchanged),
wrong-expect.json (one leg's expect_rc flipped), extra-leg.json (one row
whose id no round declares).  Each must produce exactly one finding:
PANEL_LEG_MISSING <id>, exactly one LEG rc mismatch, PANEL_LEG_UNKNOWN
<id>; clean.json must stay green.

Scratch: every directory this counter creates carries the marker file
`.c2-r99-harm-watch`; a reused --scratch-root is cleared of marked
entries first (the r98 lesson M98-12 class) and any unmarked entry is
refused (exit 2).

Selftest: builds fixture git repositories under a private temp dir and
replays the whole pipeline (pins, separability, planted controls, stub,
scratch reuse, a red panel).  Nested counter runs inside the selftest set
C2_R99_SELFTEST_DEPTH=1 and then evaluate the pipeline conditions only
(their `selftest=` field reads `skipped`), so the selftest cannot recurse.

This counter is an instrument: it spawns git, the gate (python3 -I) and
the stub; it is not itself a modelled candidate.
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
PLANTED_NAMES = ("clean.json", "dropped-leg.json", "wrong-expect.json",
                 "wrong-marker.json", "extra-leg.json")
MARKER = ".c2-r99-harm-watch"

# Marker-blind control: the counter patches the gate's marker test away and
# requires the neutralised copy to ACCEPT the wrong-marker plant (exit 0)
# where the real gate REJECTS it (exit 1) - that disagreement is the measured
# necessity of the marker test.  If the gate's marker line ever changes, this
# patch refuses to apply and the counter exits 2 (setup) instead of guessing.
BLIND_FROM = 'marker_ok = (not marker) or (marker in res["out"]) or (marker in res["err"])'
BLIND_TO = "marker_ok = True"

MINI_GATE = r'''
#!/usr/bin/env python3
"""Fixture gate for the c2-r99 selftest: same contract, fixture legs."""
import argparse, json, subprocess, sys

def census(panel):
    findings = []
    legs = panel.get("legs") or []
    rounds = panel.get("rounds") or {}
    el = panel.get("expect_legs")
    if not isinstance(el, int):
        return [("PANEL_UNREADABLE", "expect_legs-not-int")]
    seen, unknown = {}, 0
    for row in legs:
        lid = row.get("id")
        if lid in seen:
            findings.append(("PANEL_DUPLICATE", "id=%s" % lid))
        seen[lid] = seen.get(lid, 0) + 1
        if not any(lid in ids for ids in rounds.values()):
            unknown += 1
            findings.append(("PANEL_LEG_UNKNOWN", "id=%s" % lid))
    missing = 0
    for rnd, ids in sorted(rounds.items()):
        if not ids:
            findings.append(("PANEL_ROUND_MISSING", "round=%s" % rnd))
        for lid in ids:
            if lid not in seen:
                missing += 1
                findings.append(("PANEL_LEG_MISSING", "id=%s round=%s" % (lid, rnd)))
    delta = len(legs) - el
    if delta != 0 and delta != unknown + sum(c - 1 for c in seen.values() if c > 1) - missing:
        findings.insert(0, ("PANEL_LEG_COUNT", "rows=%d expect_legs=%d" % (len(legs), el)))
    return findings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo"); ap.add_argument("--rev"); ap.add_argument("--panel")
    ap.add_argument("--scratch-root"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    panel = json.load(open(a.panel))
    f = census(panel)
    if f:
        for fid, d in f:
            print("PANEL %s %s" % (fid, d))
        return 2
    ok = 0
    results = []
    for row in panel["legs"]:
        p = subprocess.run(row["argv"], cwd=a.repo, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        out = p.stdout.decode("utf-8", "replace")
        res = {"out": out, "err": ""}
        marker = row["expect_marker"]
        marker_ok = (not marker) or (marker in res["out"]) or (marker in res["err"])
        mok = marker_ok
        rok = p.returncode == row["expect_rc"]
        good = rok and mok
        ok += 1 if good else 0
        print("LEG %s rc=%d expect=%s marker=%s %s" % (
            row["id"], p.returncode, row["expect_rc"], "ok" if mok else "MISS",
            "ok" if good else "mismatch"))
        results.append({"id": row["id"], "rc": p.returncode,
                        "expect_rc": row["expect_rc"], "marker_ok": mok,
                        "ok": good, "detail": "ok" if good else "mismatch"})
    n = len(panel["legs"])
    print("HARM_WATCH: legs=%d ok=%d mismatch=%d" % (n, ok, n - ok))
    if a.json:
        print(json.dumps({"legs_run": n, "ok": ok, "mismatch": n - ok,
                          "legs": results, "exit": 0 if n == ok else 1}))
    return 0 if n == ok else 1

sys.exit(main())
'''

STUB_GATE = r'''#!/usr/bin/env python3
import json, sys
p = json.load(open(sys.argv[sys.argv.index("--panel") + 1]))
n = len(p["legs"])
print("LEG stub rc=0 expect=0 marker=ok ok")
print("HARM_WATCH: legs=%d ok=%d mismatch=0" % (n, n))
'''


def sh_bytes(argv):
    r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return r.returncode, r.stdout, r.stderr


def sha(data):
    return hashlib.sha256(data).hexdigest()


def emit(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def setup(detail):
    emit("MADO_HARM_WATCH: SETUP_ERROR %s" % detail)
    return 2


def mark_dir(path):
    os.makedirs(path, exist_ok=True)
    open(os.path.join(path, MARKER), "w").close()
    return path


def fresh_scratch(root):
    if root is None:
        return None
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


def run_gate(gate_path, repo, rev, panel_path, scratch_dir, timeout=7200):
    argv = [sys.executable, "-I", gate_path, "--repo", repo, "--rev", rev,
            "--panel", panel_path, "--scratch-root", scratch_dir, "--json"]
    try:
        r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    out = r.stdout.decode("utf-8", "replace")
    res = {"rc": r.returncode, "out": out}
    m = re.search(r"HARM_WATCH: legs=(\d+) ok=(\d+) mismatch=(\d+)", out)
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


def gate_lines(res, prefix):
    return [ln.strip() for ln in res.get("out", "").splitlines()
            if ln.strip().startswith(prefix)]


def planted_ids_diff(clean, planted):
    cids = [r["id"] for r in clean["legs"]]
    pids = [r["id"] for r in planted["legs"]]
    return [i for i in pids if i not in cids], [i for i in cids if i not in pids]


def planted_expect_diff(clean, planted):
    c = {r["id"]: r for r in clean["legs"]}
    return [r["id"] for r in planted["legs"]
            if r["id"] in c and c[r["id"]]["expect_rc"] != r["expect_rc"]]


def planted_marker_diff(clean, planted):
    c = {r["id"]: r for r in clean["legs"]}
    return [r["id"] for r in planted["legs"]
            if r["id"] in c and c[r["id"]]["expect_marker"] != r["expect_marker"]]


def eval_planted(res, kind, expect_id):
    def one(prefix):
        lines = [ln for ln in res.get("out", "").splitlines() if ln.strip().startswith("PANEL ")]
        if len(lines) != 1:
            return False
        ln = lines[0].strip()
        if not ln.startswith(prefix):
            return False
        rest = ln[len(prefix):]
        return rest == "" or rest.startswith(" round=")
    if kind == "dropped":
        want = "PANEL PANEL_LEG_MISSING id=%s" % expect_id
        return (1 if (res.get("rc") == 2 and one(want)) else 0), want
    if kind == "extra":
        want = "PANEL PANEL_LEG_UNKNOWN id=%s" % expect_id
        return (1 if (res.get("rc") == 2 and one(want)) else 0), want
    if kind == "wrong":
        legs = res.get("json", {}).get("legs", [])
        bad = [l for l in legs if l["id"] == expect_id and not l.get("ok")]
        return (1 if (res.get("rc") == 1 and res.get("mismatch") == 1 and len(bad) == 1)
                else 0), "leg=%s" % expect_id
    if kind == "wrong-marker":
        legs = res.get("json", {}).get("legs", [])
        bad = [l for l in legs if l["id"] == expect_id and not l.get("ok")
               and not l.get("marker_ok")]
        return (1 if (res.get("rc") == 1 and res.get("mismatch") == 1 and len(bad) == 1)
                else 0), "leg=%s marker=MISS" % expect_id
    if kind == "clean":
        return (1 if (res.get("rc") == 0 and res.get("mismatch") == 0) else 0), "clean"
    return 0, "unknown-kind"


def selftest_checks():
    """Fixture pipeline; returns (checks, failed, notes)."""
    import tempfile
    checks, failed, notes = [], [], []

    def record(name, cond, why=""):
        checks.append(name)
        if not cond:
            failed.append("%s: %s" % (name, why))

    root = tempfile.mkdtemp(prefix="c2-r99-selftest-")
    try:
        counter = os.path.abspath(__file__)
        fixture_env = dict(os.environ, C2_R99_SELFTEST_DEPTH="1")

        def build_repo(with_gate_at_base):
            repo = os.path.join(root, "repo%s" % ("g" if with_gate_at_base else ""))
            os.makedirs(repo)
            sh_bytes(["git", "-C", repo, "init", "-q"])
            sh_bytes(["git", "-C", repo, "config", "user.email", "fix@fix"])
            sh_bytes(["git", "-C", repo, "config", "user.name", "fix"])
            return repo

        def w(repo, rel, data):
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as fh:
                fh.write(data if isinstance(data, bytes) else data.encode())

        def commit(repo, msg):
            sh_bytes(["git", "-C", repo, "add", "-A"])
            sh_bytes(["git", "-C", repo, "commit", "-q", "--allow-empty", "-m", msg])
            return sh_bytes(["git", "-C", repo, "rev-parse", "HEAD"])[1].decode().strip()

        IDS = [c for c in "abcdefghijklmnopqrstu"]

        def panel_bytes(legs=None, flip=None, mflip=None, drop=None, add=None):
            def row(lid, rc=0):
                return {"id": lid, "round": "r0",
                        "argv": [sys.executable, "-I", "tools/leg.py", "good", "REV"],
                        "expect_rc": rc, "expect_marker": "FIXTURE_VERDICT: GOOD",
                        "note": "fixture"}
            legs = legs if legs is not None else [row(i) for i in IDS]
            if flip is not None:
                legs[flip]["expect_rc"] = 1
            if mflip is not None:
                legs[mflip]["expect_marker"] = "FIXTURE_VERDICT: NOWHERE-TO-BE-SEEN"
            if drop is not None:
                legs = [r for r in legs if r["id"] != drop]
            if add is not None:
                legs = legs + [add]
            return json.dumps({"expect_legs": len(IDS), "timeout_s": 60,
                               "rounds": {"r0": list(IDS)},
                               "legs": legs}, indent=1).encode()

        pb = panel_bytes()
        clean_p = json.loads(pb)

        # --- repo A: base without the gate; rev with gate + controls ---
        repo = build_repo(False)
        base = commit(repo, "base")
        w(repo, "tools/leg.py",
          b"#!/usr/bin/env python3\nimport sys\nassert sys.argv[1] == 'good'\n"
          b"print('FIXTURE_VERDICT: GOOD rev=' + sys.argv[2])\n")
        w(repo, "controls/panel.json", pb)
        w(repo, "controls/planted/clean.json", pb)
        w(repo, "controls/planted/dropped-leg.json", panel_bytes(drop="b"))
        w(repo, "controls/planted/wrong-expect.json", panel_bytes(flip=1))
        w(repo, "controls/planted/wrong-marker.json", panel_bytes(mflip=1))
        w(repo, "controls/planted/extra-leg.json",
          panel_bytes(add={"id": "sneaky", "round": "r0",
                           "argv": [sys.executable, "-I", "tools/leg.py", "good", "REV"],
                           "expect_rc": 0, "expect_marker": "FIXTURE_VERDICT: GOOD",
                           "note": "planted"}))
        w(repo, GATE_REPO_PATH, MINI_GATE.encode())
        rev = commit(repo, "gate+controls")

        scratch = os.path.join(root, "scr")

        def run_counter(repo_=None, rev_=None, base_=None, panel_sha=None,
                        gate_sha=None, scratch_=None, extra=()):
            argv = [sys.executable, "-I", counter,
                    "--repo", repo_ or repo, "--rev", rev_ or rev,
                    "--base-rev", base_ or base,
                    "--panel", "controls/panel.json",
                    "--expect-panel-sha256", panel_sha or sha(pb),
                    "--planted-dir", "controls/planted",
                    "--expect-gate-sha256", gate_sha or sha(MINI_GATE.encode()),
                    "--scratch-root", scratch_ or scratch] + list(extra)
            r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=900, cwd=repo, env=fixture_env)
            return r.returncode, r.stdout.decode("utf-8", "replace")

        # 1 separability: gate absent at the base rev
        rc, out = run_counter(rev_=base)
        record("base-absent-setup", rc == 2, "rc=%d" % rc)
        record("base-absent-line",
               "SETUP_ERROR quality/harm-watch.py absent at %s" % base in out, out[-300:])
        # 2 green pipeline at the rev
        rc, out = run_counter()
        record("green-pipeline", rc == 0 and "TARGET_MET pred=PRED-C2-r99-v1" in out, out[-600:])
        record("green-mismatches-zero", "mismatches=0" in out and "legs_run=21" in out,
               out[-600:])
        record("green-planted-dropped", "planted_dropped_leg=1" in out, out[-600:])
        record("green-planted-wrong", "planted_wrong_expect=1" in out, out[-600:])
        record("green-planted-wrong-marker", "planted_wrong_marker=1" in out, out[-600:])
        record("green-marker-blind-flagged", "marker_blind_flagged=1" in out, out[-600:])
        record("green-planted-extra", "planted_extra_leg=1" in out, out[-600:])
        record("green-stub-flagged", "stub_flagged=1" in out, out[-600:])
        # 3-4 pin mismatches are setup errors
        rc, out = run_counter(extra=["--expect-panel-sha256", "0" * 64])
        record("panel-pin-setup", rc == 2 and "SETUP_ERROR panel sha256" in out, out[-300:])
        rc, out = run_counter(extra=["--expect-gate-sha256", "0" * 64])
        record("gate-pin-setup", rc == 2 and "SETUP_ERROR gate sha256" in out, out[-300:])
        # 5 a red panel is a miss, not a setup
        rb = panel_bytes(flip=0)
        w(repo, "controls/panel.json", rb)
        red_rev = commit(repo, "red-panel")
        rc, out = run_counter(rev_=red_rev, panel_sha=sha(rb))
        record("red-target-missed", rc == 1 and "TARGET_MISSED" in out, out[-600:])
        record("red-mismatches-one", "mismatches=1" in out and "missed=mismatches_zero" in out,
               out[-600:])
        # 6 scratch reuse is idempotent (M98-12 class)
        w(repo, "controls/panel.json", pb)
        fix_rev = commit(repo, "panel-restored")
        rc, out = run_counter(rev_=fix_rev)
        record("scratch-reuse", rc == 0 and "TARGET_MET" in out, out[-600:])
        # 6b the emitted rev is the measured rev, not the base
        record("rev-pin-emitted", ("rev=%s" % fix_rev) in out, out[:300])
        # 7 the claim is void when the gate exists at the base rev
        repo2 = build_repo(True)
        w(repo2, "tools/leg.py",
          b"#!/usr/bin/env python3\nimport sys\nassert sys.argv[1] == 'good'\n"
          b"print('FIXTURE_VERDICT: GOOD rev=' + sys.argv[2])\n")
        w(repo2, "controls/panel.json", pb)
        w(repo2, "controls/planted/clean.json", pb)
        w(repo2, "controls/planted/dropped-leg.json", panel_bytes(drop="b"))
        w(repo2, "controls/planted/wrong-expect.json", panel_bytes(flip=1))
        w(repo2, "controls/planted/wrong-marker.json", panel_bytes(mflip=1))
        w(repo2, "controls/planted/extra-leg.json",
          panel_bytes(add={"id": "sneaky", "round": "r0",
                           "argv": [sys.executable, "-I", "tools/leg.py", "good", "REV"],
                           "expect_rc": 0, "expect_marker": "FIXTURE_VERDICT: GOOD",
                           "note": "planted"}))
        w(repo2, GATE_REPO_PATH, MINI_GATE.encode())
        base2 = commit(repo2, "everything-at-base")
        rc, out = run_counter(repo_=repo2, rev_=base2, base_=base2)
        record("base-present-void", rc == 2 and
               "SETUP_ERROR quality/harm-watch.py present at base-rev %s" % base2 in out,
               out[-300:])
        notes.append("fixture_revs=%s,%s,%s" % (base[:7], rev[:7], base2[:7]))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return checks, failed, notes


def main():
    ap = argparse.ArgumentParser(add_help=True,
                                 description="mado round-99 C2 counting command")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--panel")
    ap.add_argument("--expect-panel-sha256")
    ap.add_argument("--planted-dir")
    ap.add_argument("--expect-gate-sha256")
    ap.add_argument("--gate", help="draft mode: gate/panel/planted bytes from the tree")
    ap.add_argument("--scratch-root")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    depth = int(os.environ.get("C2_R99_SELFTEST_DEPTH", "0") or 0)

    if a.selftest and depth == 0:
        checks, failed, _ = selftest_checks()
        emit("MADO_COUNTER_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
        for f in failed:
            emit("FAIL %s" % f)
        return 0 if not failed else 1

    for req in ("repo", "rev", "base_rev", "panel", "expect_panel_sha256",
                "planted_dir", "expect_gate_sha256", "scratch_root"):
        if not getattr(a, req):
            return setup("missing --%s" % req.replace("_", "-"))
    if fresh_scratch(a.scratch_root) is None:
        return setup("scratch-root unusable or has unmarked entries: %s" % a.scratch_root)
    root = a.scratch_root
    repo = a.repo

    # claim before-state: the gate must not exist at the base revision
    rc, _, _ = sh_bytes(["git", "-C", repo, "cat-file", "-e",
                         "%s:%s" % (a.base_rev, GATE_REPO_PATH)])
    if rc == 0:
        return setup("quality/harm-watch.py present at base-rev %s" % a.base_rev)

    # gate bytes
    if a.gate:
        try:
            with open(a.gate, "rb") as fh:
                gate_bytes = fh.read()
        except OSError as e:
            return setup("gate unreadable: %s" % e)
    else:
        rc, out, _ = sh_bytes(["git", "-C", repo, "show", "%s:%s" % (a.rev, GATE_REPO_PATH)])
        if rc != 0:
            return setup("quality/harm-watch.py absent at %s" % a.rev)
        gate_bytes = out
    gate_sha = sha(gate_bytes)
    if gate_sha != a.expect_gate_sha256:
        return setup("gate sha256 %s != pinned %s" % (gate_sha, a.expect_gate_sha256))
    gdir = mark_dir(os.path.join(root, "gate"))
    gate_path = os.path.join(gdir, "harm-watch.py")
    with open(gate_path, "wb") as fh:
        fh.write(gate_bytes)
    os.chmod(gate_path, 0o755)

    # panel bytes
    if a.gate:
        try:
            with open(a.panel, "rb") as fh:
                panel_bytes = fh.read()
        except OSError as e:
            return setup("panel unreadable: %s" % e)
    else:
        rc, out, _ = sh_bytes(["git", "-C", repo, "show", "%s:%s" % (a.rev, a.panel)])
        if rc != 0:
            return setup("panel absent at %s: %s" % (a.rev, a.panel))
        panel_bytes = out
    panel_sha = sha(panel_bytes)
    if panel_sha != a.expect_panel_sha256:
        return setup("panel sha256 %s != pinned %s" % (panel_sha, a.expect_panel_sha256))
    try:
        panel = json.loads(panel_bytes.decode("utf-8"))
    except Exception:
        return setup("panel json unreadable")
    if not isinstance(panel, dict) or not isinstance(panel.get("expect_legs"), int):
        return setup("panel json has no expect_legs")
    pdir = mark_dir(os.path.join(root, "panel"))
    panel_path = os.path.join(pdir, "panel.json")
    with open(panel_path, "wb") as fh:
        fh.write(panel_bytes)

    # planted bytes
    planted = {}
    pl_dir = mark_dir(os.path.join(root, "planted"))
    for name in PLANTED_NAMES:
        rel = "%s/%s" % (a.planted_dir.rstrip("/"), name)
        if a.gate:
            path = os.path.join(repo, rel)
            try:
                with open(path, "rb") as fh:
                    data = fh.read()
            except OSError as e:
                return setup("planted unreadable: %s" % e)
        else:
            rc, out, _ = sh_bytes(["git", "-C", repo, "show", "%s:%s" % (a.rev, rel)])
            if rc != 0:
                return setup("planted absent at %s: %s" % (a.rev, rel))
            data = out
        try:
            obj = json.loads(data.decode("utf-8"))
        except Exception:
            return setup("planted json unreadable: %s" % name)
        planted[name] = obj
        with open(os.path.join(pl_dir, name), "wb") as fh:
            fh.write(data)

    # main run
    main_res = run_gate(gate_path, repo, a.rev, panel_path,
                        mark_dir(os.path.join(root, "run-main")))
    if "error" in main_res:
        return setup("gate run failed: %s" % main_res["error"])
    panel_legs = main_res.get("legs")
    mismatches = main_res.get("mismatch")
    if panel_legs is None or mismatches is None:
        return setup("gate produced no HARM_WATCH summary")

    # planted controls
    cl = planted["clean.json"]
    drop_missing = planted_ids_diff(cl, planted["dropped-leg.json"])[1]
    extra_added = planted_ids_diff(cl, planted["extra-leg.json"])[0]
    wrong_flipped = planted_expect_diff(cl, planted["wrong-expect.json"])
    marker_flipped = planted_marker_diff(cl, planted["wrong-marker.json"])
    if len(drop_missing) != 1 or len(extra_added) != 1 or len(wrong_flipped) != 1 \
            or len(marker_flipped) != 1:
        return setup("planted panels do not carry exactly one defect "
                     "(missing=%s added=%s flipped=%s marker=%s)"
                     % (drop_missing, extra_added, wrong_flipped, marker_flipped))
    flags, details = {}, {}
    for name, kind, ident in (
            ("clean.json", "clean", None),
            ("dropped-leg.json", "dropped", drop_missing[0]),
            ("wrong-expect.json", "wrong", wrong_flipped[0]),
            ("wrong-marker.json", "wrong-marker", marker_flipped[0]),
            ("extra-leg.json", "extra", extra_added[0])):
        res = run_gate(gate_path, repo, a.rev, os.path.join(pl_dir, name),
                       mark_dir(os.path.join(root, "run-" + kind)))
        flags[kind], details[kind] = eval_planted(res, kind, ident)

    # stub control: an always-OK gate must be distinguishable on a red panel
    stub_dir = mark_dir(os.path.join(root, "stub"))
    stub_path = os.path.join(stub_dir, "stub-gate.py")
    with open(stub_path, "w") as fh:
        fh.write(STUB_GATE)
    os.chmod(stub_path, 0o755)
    stub_res = run_gate(stub_path, repo, a.rev, os.path.join(pl_dir, "dropped-leg.json"),
                        mark_dir(os.path.join(root, "run-stub")))
    stub_ok_while_red = (stub_res.get("rc") == 0 and
                         "mismatch=0" in stub_res.get("out", "") and
                         "PANEL" not in stub_res.get("out", ""))
    stub_flagged = 1 if (stub_ok_while_red and flags.get("dropped") == 1) else 0

    # marker-blind control: neutralise the gate's marker test and require the
    # copy to accept the wrong-marker plant (exit 0) where the real gate
    # rejects it (exit 1) - the measured necessity of the marker test
    n_blind = gate_bytes.count(BLIND_FROM.encode())
    if n_blind == 1:
        blind_dir = mark_dir(os.path.join(root, "blind"))
        blind_path = os.path.join(blind_dir, "harm-watch-blind.py")
        with open(blind_path, "wb") as fh:
            fh.write(gate_bytes.replace(BLIND_FROM.encode(), BLIND_TO.encode()))
        os.chmod(blind_path, 0o755)
        blind_res = run_gate(blind_path, repo, a.rev,
                             os.path.join(pl_dir, "wrong-marker.json"),
                             mark_dir(os.path.join(root, "run-blind")))
        blind_accepts = (blind_res.get("rc") == 0 and blind_res.get("mismatch") == 0)
        marker_blind_flagged = 1 if (blind_accepts and flags.get("wrong-marker") == 1) else 0
    else:
        return setup("marker-blind patch does not apply to the gate bytes "
                     "(BLIND_FROM occurs %d times)" % n_blind)

    # counter selftest (fixture pipeline), once, at depth 0
    if depth == 0:
        st_checks, st_failed, _ = selftest_checks()
        st_failed_n = len(st_failed)
        selftest_txt = "checks=%d failed=%d" % (len(st_checks), st_failed_n)
        selftest_ok = len(st_checks) >= 12 and st_failed_n == 0
    else:
        st_checks, st_failed_n, selftest_ok = 0, 0, True
        selftest_txt = "skipped"

    declared = panel.get("expect_legs")
    legs_run = len(main_res.get("json", {}).get("legs", [])) or panel_legs
    conds = {
        "panel_legs_eq_declared": panel_legs == declared,
        "panel_legs_ge_20": (panel_legs or 0) >= 20,
        "legs_run_eq_panel_legs": legs_run == panel_legs,
        "mismatches_zero": mismatches == 0,
        "planted_dropped_leg": flags.get("dropped") == 1,
        "planted_wrong_expect": flags.get("wrong") == 1,
        "planted_wrong_marker": flags.get("wrong-marker") == 1,
        "marker_blind_flagged": marker_blind_flagged == 1,
        "stub_flagged": stub_flagged == 1,
    }
    if depth == 0:
        conds["selftest_ge_12_failed_0"] = selftest_ok
    met = all(conds.values())
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    bad = [k for k, v in conds.items() if not v]
    emit("MADO_HARM_WATCH: %s pred=PRED-C2-r99-v1 rev=%s base_rev=%s gate_sha256=%s "
         "panel_sha256=%s panel_legs=%s declared_legs=%s legs_run=%s mismatches=%s "
         "planted_dropped_leg=%d planted_wrong_expect=%d planted_wrong_marker=%d "
         "planted_extra_leg=%d marker_blind_flagged=%d stub_flagged=%d selftest=%s%s"
         % (verdict, a.rev, a.base_rev, gate_sha, panel_sha, panel_legs, declared,
            legs_run, mismatches, flags.get("dropped", 0), flags.get("wrong", 0),
            flags.get("wrong-marker", 0), flags.get("extra", 0),
            marker_blind_flagged, stub_flagged, selftest_txt,
            (" missed=" + ",".join(bad)) if bad else ""))
    if a.json:
        emit(json.dumps({
            "verdict": verdict, "rev": a.rev, "base_rev": a.base_rev,
            "gate_sha256": gate_sha, "panel_sha256": panel_sha,
            "panel_legs": panel_legs, "declared_legs": declared,
            "legs_run": legs_run, "mismatches": mismatches,
            "planted": flags, "planted_details": details,
            "stub_flagged": stub_flagged,
            "selftest_checks": len(st_checks), "selftest_failed": st_failed_n,
            "conds": conds,
        }))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""harm-watch -- replay a frozen panel of harm-watch legs (mado round 99, C2).

Usage:
    harm-watch.py --repo DIR --rev REV --panel PANEL.json
                  [--scratch-root DIR] [--timeout S] [--json]
    harm-watch.py --selftest

The panel declares:
    expect_legs  int    -- the exact row count the panel must carry
    timeout_s    int    -- default per-leg timeout in seconds
    rounds       object -- round name -> the leg ids that round contributes
    legs         array  -- rows: id, round, argv (list of strings; the bare
                            element "REV" is replaced by --rev and the bare
                            element "SCRATCH" by <scratch-root>/<leg-id>),
                            expect_rc (int), expect_marker (substring of the
                            leg's captured stdout or stderr), note (string)

Census, before any leg runs; each finding prints one line
`PANEL <ID> <detail>` and makes the exit 2 with no leg started:
    PANEL_LEG_COUNT      rows != expect_legs, unless the delta is fully
                         explained by the other findings (one missing id per
                         removed row, one undeclared/duplicate row per added
                         row) -- this keeps a planted dropped-leg panel a
                         single-finding control: exactly PANEL_LEG_MISSING.
    PANEL_DUPLICATE      an id declared by a round appears in two rows
    PANEL_ROUND_MISSING  a declared round has no row
    PANEL_LEG_UNKNOWN    a row id no round declares
    PANEL_LEG_MISSING    a round-declared id with no row

Each leg then runs once: argv with substitutions, cwd = --repo, captured
stdout and stderr, killed (process group SIGKILL, exit status recorded as
124) on timeout.  The leg is ok iff rc == expect_rc and expect_marker
occurs in the captured output.  Per leg one line:
    LEG <id> rc=<n> expect=<n> marker=<ok|MISS> <detail>
and the summary line `HARM_WATCH: legs=N ok=M mismatch=K`.

Exit: 0 iff the census is clean and K == 0; 1 on any leg mismatch;
2 on setup or census findings.  --json prints the human lines above and
then one JSON object as the last stdout line (same information; the
object, not the absence of human lines, is what "json mode" adds).

Scratch: each leg gets <scratch-root>/<leg-id>, created fresh; a leftover
directory from an earlier harm-watch run (marked `.harm-watch-leg-r99`) is
reused by clearing it, any other non-empty directory is refused (setup, 2).
The captured output of every leg is copied to <scratch-root>/<leg-id>.log.
The tool writes nothing else and never writes inside --repo.

--only ID (repeatable) runs the census over the FULL panel first (the
census findings are unchanged), then runs only the named legs; the
summary `HARM_WATCH: legs=N ok=M mismatch=K` counts the legs that ran.
An --only id the panel does not declare is a setup error (exit 2).  The
planted-control runs of the C2 counter use this to scope a heavy panel to
its single defect leg.

--selftest builds its own fixture panels and stub legs in a private temp
directory and prints `HARM_WATCH_SELFTEST: checks=N failed=M` (exit 0 when
failed == 0, else 1).

This tool is an instrument: it spawns the panel's legs as child processes.
"""

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile

LEG_SCRATCH_MARKER = ".harm-watch-leg-r99"


def panel_line(fid, detail):
    sys.stdout.write("PANEL %s %s\n" % (fid, detail))


def setup_error(fid, detail):
    panel_line(fid, detail)
    return 2


def census(panel):
    """Return a list of (census-id, detail) findings, in contract order."""
    findings = []
    legs = panel.get("legs")
    if not isinstance(legs, list) or not legs:
        return [("PANEL_UNREADABLE", "legs-missing-or-empty")]
    rounds = panel.get("rounds")
    if not isinstance(rounds, dict) or not rounds:
        return [("PANEL_UNREADABLE", "rounds-missing-or-empty")]
    expect_legs = panel.get("expect_legs")
    if not isinstance(expect_legs, int) or isinstance(expect_legs, bool):
        return [("PANEL_UNREADABLE", "expect_legs-not-int")]

    seen = {}
    unknown = []
    for row in legs:
        if not isinstance(row, dict):
            findings.append(("PANEL_ROW", "row-not-object"))
            continue
        lid = row.get("id")
        if not isinstance(lid, str) or not lid:
            findings.append(("PANEL_ROW", "row-without-id"))
            continue
        for field in ("round", "argv", "expect_rc", "expect_marker", "note"):
            if field not in row:
                findings.append(("PANEL_ROW", "id=%s missing-field:%s" % (lid, field)))
        if not isinstance(row.get("argv"), list) or not row.get("argv"):
            findings.append(("PANEL_ROW", "id=%s argv-not-list" % lid))
        elif not all(isinstance(x, str) and x for x in row["argv"]):
            findings.append(("PANEL_ROW", "id=%s argv-empty-element" % lid))
        er = row.get("expect_rc")
        if not isinstance(er, int) or isinstance(er, bool):
            findings.append(("PANEL_ROW", "id=%s expect_rc-not-int" % lid))
        if not isinstance(row.get("expect_marker"), str):
            findings.append(("PANEL_ROW", "id=%s expect_marker-not-str" % lid))
        if not isinstance(row.get("round"), str) or not row.get("round"):
            findings.append(("PANEL_ROW", "id=%s round-not-str" % lid))
        if lid in seen:
            findings.append(("PANEL_DUPLICATE", "id=%s" % lid))
            seen[lid] += 1
        else:
            seen[lid] = 1
        rounds_has = isinstance(row.get("round"), str) and row["round"] in rounds
        if rounds_has and lid not in rounds[row["round"]]:
            unknown.append(lid)
            findings.append(("PANEL_LEG_UNKNOWN", "id=%s" % lid))
        elif not rounds_has:
            unknown.append(lid)
            findings.append(("PANEL_LEG_UNKNOWN", "id=%s" % lid))
    # duplicates contribute surplus rows to the count delta
    dup_surplus = sum(c - 1 for c in seen.values() if c > 1)

    for rnd in sorted(rounds):
        ids = rounds[rnd]
        if not isinstance(ids, list):
            findings.append(("PANEL_UNREADABLE", "round=%s ids-not-list" % rnd))
            continue
        for lid in ids:
            if lid not in seen:
                findings.append(("PANEL_LEG_MISSING", "id=%s round=%s" % (lid, rnd)))
        if not ids:
            findings.append(("PANEL_ROUND_MISSING", "round=%s" % rnd))

    missing = 0
    for rnd in sorted(rounds):
        ids = rounds[rnd]
        if isinstance(ids, list):
            missing += sum(1 for lid in ids if lid not in seen)
    n_rows = sum(seen.values())
    delta = n_rows - expect_legs
    explained = len(unknown) + dup_surplus - missing
    if delta != 0 and delta != explained:
        findings.insert(0, ("PANEL_LEG_COUNT", "rows=%d expect_legs=%d" % (n_rows, expect_legs)))
    return findings


def substitute(argv, rev, scratch_dir):
    out = []
    for el in argv:
        if el == "REV":
            out.append(rev)
        elif el == "SCRATCH":
            out.append(scratch_dir)
        else:
            out.append(el)
    return out


def safe_scratch_dir(scratch_root, leg_id):
    """Create/clear <scratch-root>/<leg-id>; return its path or (None, reason)."""
    if not all(c.isalnum() or c in "._-" for c in leg_id) or leg_id.startswith("."):
        return None, "bad-leg-id"
    if scratch_root is None:
        return None, "scratch-root-required"
    root = os.path.realpath(scratch_root)
    os.makedirs(root, exist_ok=True)
    legdir = os.path.join(scratch_root, leg_id)
    if os.path.lexists(legdir):
        real = os.path.realpath(legdir)
        if not (real == os.path.join(root, leg_id) and real.startswith(root + os.sep)):
            return None, "scratch-escape"
        marker = os.path.join(legdir, LEG_SCRATCH_MARKER)
        if os.path.isfile(marker) and os.path.isdir(legdir):
            shutil.rmtree(legdir)
        else:
            return None, "scratch-not-ours"
    os.makedirs(legdir)
    open(os.path.join(legdir, LEG_SCRATCH_MARKER), "w").close()
    return legdir, None


def run_leg(row, repo, rev, scratch_root, timeout):
    legdir, err = safe_scratch_dir(scratch_root, row["id"]) if "SCRATCH" in row["argv"] \
        else ((os.path.join(scratch_root, row["id"]) if scratch_root else None), None)
    if "SCRATCH" in row["argv"] and err == "scratch-root-required":
        return {"id": row["id"], "rc": None, "setup": "scratch-root-required"}
    if err is not None:
        return {"id": row["id"], "rc": None, "setup": err}
    argv = substitute(row["argv"], rev, legdir or "SCRATCH-UNSET")
    try:
        p = subprocess.Popen(argv, cwd=repo, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    except OSError as e:
        return {"id": row["id"], "rc": 127, "out": "", "err": str(e),
                "detail": "spawn-failed", "legdir": legdir}
    try:
        outb, errb = p.communicate(timeout=timeout)
        rc, detail = p.returncode, ""
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except Exception:
            pass
        outb, errb = b"", b""
        try:
            outb, errb = p.communicate(timeout=30)
        except Exception:
            try:
                p.kill()
                p.wait(timeout=10)
            except Exception:
                pass
        rc = 124
        detail = "timeout-after-%ss" % int(timeout)
    out = outb.decode("utf-8", "replace")
    err = errb.decode("utf-8", "replace")
    if scratch_root:
        try:
            logpath = os.path.join(scratch_root, row["id"] + ".log")
            with open(logpath, "w", encoding="utf-8", errors="replace") as fh:
                fh.write("$ %s\n" % " ".join(argv))
                fh.write("--- stdout ---\n%s\n--- stderr ---\n%s\n" % (out, err))
                fh.write("--- rc=%s ---\n" % rc)
        except OSError:
            pass
    return {"id": row["id"], "rc": rc, "out": out, "err": err, "detail": detail,
            "legdir": legdir}


def check_leg(row, res):
    if res.get("setup"):
        return False, False, "setup:" + res["setup"]
    rc = res["rc"]
    marker = row["expect_marker"]
    marker_ok = (not marker) or (marker in res["out"]) or (marker in res["err"])
    rc_ok = rc == row["expect_rc"]
    res_detail = res.get("detail") or ""
    if rc_ok and marker_ok:
        detail = "ok"
    elif not rc_ok and not marker_ok:
        detail = "rc-and-marker-mismatch"
    elif not rc_ok:
        detail = "rc-mismatch"
    else:
        detail = "marker-missing"
    if res_detail:
        detail = detail + "+" + res_detail if detail != "ok" else res_detail
    return rc_ok, marker_ok, detail


def load_panel(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh), None
    except Exception as e:
        return None, str(e)


def leg_timeout(panel, args):
    if args.timeout is not None:
        return args.timeout
    t = panel.get("timeout_s", 3600)
    if isinstance(t, (int, float)) and not isinstance(t, bool) and t > 0:
        return float(t)
    return 3600.0


def run_panel(args):
    panel, err = load_panel(args.panel)
    if panel is None:
        return setup_error("PANEL_UNREADABLE", "panel=%s error=%s" % (args.panel, err))
    findings = census(panel)
    if findings:
        for fid, detail in findings:
            panel_line(fid, detail)
        return 2
    if not args.scratch_root:
        needs = any("SCRATCH" in row["argv"] for row in panel["legs"])
        if needs:
            return setup_error("PANEL_SETUP", "scratch-root-required-by-leg-argv")
    else:
        os.makedirs(args.scratch_root, exist_ok=True)
    only = [x for x in (args.only or [])]
    if only:
        declared = {row["id"] for row in panel["legs"] if isinstance(row, dict)}
        bad = [x for x in only if x not in declared]
        if bad:
            return setup_error("PANEL_SETUP", "only-unknown-id=" + ",".join(bad))
        panel = dict(panel)
        panel["legs"] = [row for row in panel["legs"] if row["id"] in only]
    timeout = leg_timeout(panel, args)
    results = []
    nok = 0
    for row in panel["legs"]:
        res = run_leg(row, args.repo, args.rev, args.scratch_root, timeout)
        rc_ok, marker_ok, detail = check_leg(row, res)
        rc = res.get("rc")
        if rc_ok and marker_ok:
            nok += 1
        line = "LEG %s rc=%s expect=%s marker=%s %s" % (
            row["id"], rc if rc is not None else "SETUP", row["expect_rc"],
            "ok" if marker_ok else "MISS", detail)
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
        results.append({
            "id": row["id"], "round": row.get("round"), "rc": rc,
            "expect_rc": row["expect_rc"], "marker_ok": marker_ok,
            "ok": bool(rc_ok and marker_ok), "detail": detail,
        })
        if res.get("setup"):
            sys.stdout.write("HARM_WATCH: setup-error leg=%s detail=%s\n"
                             % (row["id"], detail))
            if args.json:
                print(json.dumps({
                    "repo": args.repo, "rev": args.rev, "panel": args.panel,
                    "census": [], "legs_run": len(results), "ok": nok,
                    "mismatch": len(results) - nok, "legs": results,
                    "exit": 2, "setup_error": detail,
                }))
            return 2
    n = len(panel["legs"])
    k = n - nok
    sys.stdout.write("HARM_WATCH: legs=%d ok=%d mismatch=%d\n" % (n, nok, k))
    if args.json:
        print(json.dumps({
            "repo": args.repo, "rev": args.rev, "panel": args.panel,
            "census": [], "legs_run": n, "ok": nok, "mismatch": k,
            "legs": results, "exit": 0 if k == 0 else 1,
        }))
    return 0 if k == 0 else 1


def sh(argv, **kw):
    return subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=kw.pop("timeout", 30), **kw)


class Fix:
    """Builds a fixture repo dir with stub legs and writes panels."""

    def __init__(self, root):
        self.root = root
        self.leg = os.path.join(root, "leg.py")
        with open(self.leg, "w", encoding="utf-8") as fh:
            fh.write(
                "import os, sys, time\n"
                "cmd = sys.argv[1]\n"
                "if cmd == 'ok':\n"
                "    rev = sys.argv[3] if len(sys.argv) > 3 else 'none'\n"
                "    print('FIXTURE_VERDICT: GOOD rev=' + rev)\n"
                "    sys.exit(0)\n"
                "if cmd == 'other':\n"
                "    print('FIXTURE_VERDICT: OTHER')\n"
                "    sys.exit(0)\n"
                "if cmd == 'slow':\n"
                "    time.sleep(30)\n"
                "    sys.exit(0)\n"
                "if cmd == 'write':\n"
                "    open(os.path.join(sys.argv[2], 'touched'), 'w').write('x')\n"
                "    print('FIXTURE_VERDICT: WROTE')\n"
                "    sys.exit(0)\n"
                "if cmd == 'show':\n"
                "    print('ARGS:' + '|'.join(sys.argv[2:]))\n"
                "    sys.exit(0)\n"
                "sys.exit(9)\n")
        os.chmod(self.leg, 0o755)

    def py(self, *a):
        return [sys.executable, "-I", self.leg] + list(a)

    def row(self, lid, argv, rc=0, marker="FIXTURE_VERDICT: GOOD", note=""):
        return {"id": lid, "round": "r0", "argv": argv, "expect_rc": rc,
                "expect_marker": marker, "note": note}

    def write_panel(self, name, panel):
        path = os.path.join(self.root, name)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(panel, fh, indent=1, sort_keys=True)
        return path


def base_panel(fix, rev="fedcba9876543210fedcba9876543210fedcba98"):
    return {
        "expect_legs": 3,
        "timeout_s": 20,
        "rounds": {"r0": ["good", "second", "third"]},
        "legs": [
            fix.row("good", fix.py("ok", "--rev", "REV")),
            fix.row("second", fix.py("ok", "x"), note="filler"),
            fix.row("third", fix.py("ok", "y"), note="filler"),
        ],
    }, rev


def run_gate(argv):
    r = sh(argv, timeout=120)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def selftest():
    checks = []
    failed = []

    def record(name, cond, why=""):
        checks.append(name)
        if not cond:
            failed.append("%s: %s" % (name, why))

    root = tempfile.mkdtemp(prefix="harm-watch-selftest-")
    try:
        fix = Fix(root)
        rev = "fedcba9876543210fedcba9876543210fedcba98"

        def gate(panel_path, extra=(), scratch=None):
            return [sys.executable, "-I", os.path.abspath(__file__),
                    "--repo", root, "--rev", rev, "--panel", panel_path,
                    "--scratch-root", scratch or os.path.join(root, "scr")] + list(extra)

        # 1 clean panel: exit 0, summary ok, no PANEL lines
        p, _ = base_panel(fix)
        rc, out = run_gate(gate(fix.write_panel("clean.json", p)))
        record("clean-exit0", rc == 0, "rc=%d" % rc)
        record("clean-summary",
               "HARM_WATCH: legs=3 ok=3 mismatch=0" in out, out[-200:])
        record("clean-no-panel-line", "\nPANEL " not in out, out[-200:])
        record("clean-leg-line",
               "LEG good rc=0 expect=0 marker=ok ok" in out, out[-200:])

        # 2-4 planted controls
        dropped = json.loads(json.dumps(p))
        dropped["legs"] = [r for r in dropped["legs"] if r["id"] != "second"]
        rc, out = run_gate(gate(fix.write_panel("dropped.json", dropped)))
        lines = [ln for ln in out.splitlines() if ln.startswith("PANEL ")]
        record("dropped-exit2", rc == 2, "rc=%d" % rc)
        record("dropped-exactly-one-finding",
               len(lines) == 1 and lines[0] == "PANEL PANEL_LEG_MISSING id=second round=r0",
               str(lines))

        wrong = json.loads(json.dumps(p))
        wrong["legs"][1]["expect_rc"] = 1
        rc, out = run_gate(gate(fix.write_panel("wrong.json", wrong)))
        legs = [ln for ln in out.splitlines() if ln.startswith("LEG ")]
        record("wrong-exit1", rc == 1, "rc=%d" % rc)
        record("wrong-exactly-one-mismatch",
               "HARM_WATCH: legs=3 ok=2 mismatch=1" in out and
               len([ln for ln in legs if " rc=0 expect=1 " in ln]) == 1, out[-300:])

        extra = json.loads(json.dumps(p))
        extra["legs"].append(fix.row("sneaky", fix.py("ok", "z")))
        rc, out = run_gate(gate(fix.write_panel("extra.json", extra)))
        lines = [ln for ln in out.splitlines() if ln.startswith("PANEL ")]
        record("extra-exit2", rc == 2, "rc=%d" % rc)
        record("extra-exactly-unknown",
               len(lines) == 1 and lines[0] == "PANEL PANEL_LEG_UNKNOWN id=sneaky",
               str(lines))

        # 5 duplicate id
        dup = json.loads(json.dumps(p))
        dup["legs"].append(dict(dup["legs"][1]))
        rc, out = run_gate(gate(fix.write_panel("dup.json", dup)))
        lines = [ln for ln in out.splitlines() if ln.startswith("PANEL ")]
        record("duplicate-id", rc == 2 and
               any(ln.startswith("PANEL PANEL_DUPLICATE id=second") for ln in lines),
               str(lines))

        # 6 declared round with no row
        rm = {"expect_legs": 1, "timeout_s": 20,
              "rounds": {"r0": ["good"], "r9": ["ghost"]},
              "legs": [fix.row("good", fix.py("ok", "x"))]}
        rc, out = run_gate(gate(fix.write_panel("roundmissing.json", rm)))
        lines = [ln for ln in out.splitlines() if ln.startswith("PANEL ")]
        record("round-missing", rc == 2 and
               any(ln.startswith("PANEL PANEL_LEG_MISSING id=ghost round=r9") for ln in lines),
               str(lines))
        # 6b empty round declaration
        rm2 = json.loads(json.dumps(rm))
        rm2["rounds"]["r9"] = []
        rc, out = run_gate(gate(fix.write_panel("roundempty.json", rm2)))
        record("round-empty", rc == 2 and
               "PANEL PANEL_ROUND_MISSING round=r9" in out, out[-200:])

        # 7 unexplained count mismatch
        cnt = json.loads(json.dumps(p))
        cnt["expect_legs"] = 4
        rc, out = run_gate(gate(fix.write_panel("count.json", cnt)))
        record("leg-count", rc == 2 and
               "PANEL PANEL_LEG_COUNT rows=3 expect_legs=4" in out, out[-200:])

        # 8 marker miss
        mm = json.loads(json.dumps(p))
        mm["legs"][0]["expect_marker"] = "FIXTURE_VERDICT: NOPE"
        rc, out = run_gate(gate(fix.write_panel("markermiss.json", mm)))
        record("marker-miss", rc == 1 and
               "LEG good rc=0 expect=0 marker=MISS marker-missing" in out, out[-300:])

        # 9 rc mismatch with marker ok
        rc, out = run_gate(gate(fix.write_panel("rcmiss.json", json.loads(json.dumps({
            "expect_legs": 1, "timeout_s": 20, "rounds": {"r0": ["odd"]},
            "legs": [fix.row("odd", fix.py("other"), rc=1,
                             marker="FIXTURE_VERDICT: OTHER")]})))))
        record("rc-mismatch", rc == 1 and
               "LEG odd rc=0 expect=1 marker=ok rc-mismatch" in out, out[-300:])

        # 10 timeout
        slow = {"expect_legs": 1, "timeout_s": 20, "rounds": {"r0": ["slow"]},
                "legs": [fix.row("slow", fix.py("slow"))]}
        rc, out = run_gate(gate(fix.write_panel("slow.json", slow),
                                extra=["--timeout", "1"]))
        record("timeout", rc == 1 and
               "LEG slow rc=124 expect=0" in out and "timeout-after-1s" in out,
               out[-300:])

        # 11 REV substitution reaches the leg argv
        revleg = {"expect_legs": 1, "timeout_s": 20, "rounds": {"r0": ["rev"]},
                  "legs": [fix.row("rev", fix.py("show", "--rev", "REV"),
                                   marker="ARGS:--rev|" + rev)]}
        rc, out = run_gate(gate(fix.write_panel("rev.json", revleg)))
        record("rev-substitution", rc == 0 and "marker=ok" in out, out[-300:])
        record("rev-no-literal-token", "REV " not in out.replace(rev, ""), out[-300:])

        # 12 SCRATCH substitution and fresh dir per leg
        sc = {"expect_legs": 1, "timeout_s": 20, "rounds": {"r0": ["w"]},
              "legs": [fix.row("w", fix.py("write", "SCRATCH"),
                               marker="FIXTURE_VERDICT: WROTE")]}
        rc, out = run_gate(gate(fix.write_panel("scratch.json", sc)))
        touched = os.path.exists(os.path.join(root, "scr", "w", "touched"))
        record("scratch-substitution", rc == 0 and touched, "rc=%d" % rc)
        # 12b idempotent reuse: marker dir is cleared, foreign dir refused
        rc, out = run_gate(gate(fix.write_panel("scratch2.json", sc)))
        record("scratch-reuse-cleared", rc == 0, out[-200:])
        foreign = os.path.join(root, "scr", "w")
        open(os.path.join(foreign, "precious"), "w").write("keep")
        os.remove(os.path.join(foreign, LEG_SCRATCH_MARKER))
        rc, out = run_gate(gate(fix.write_panel("scratch3.json", sc)))
        record("scratch-foreign-refused",
               rc == 2 and "setup:scratch-not-ours" in out, out[-200:])

        # 13 json mode parses and agrees
        p2, _ = base_panel(fix)
        rc, out = run_gate(gate(fix.write_panel("jsonmode.json", p2), extra=["--json"]))
        try:
            obj = json.loads(out.strip().splitlines()[-1])
            record("json-mode", rc == 0 and obj["legs_run"] == 3 and
                   obj["mismatch"] == 0 and len(obj["legs"]) == 3, out[-200:])
        except Exception as e:
            record("json-mode", False, repr(e))

        # 14 unreadable panel
        rc, out = run_gate(gate(os.path.join(root, "absent.json")))
        record("panel-unreadable",
               rc == 2 and "PANEL PANEL_UNREADABLE" in out, out[-200:])

        # 15 leg log written, no writes inside repo
        p3, _ = base_panel(fix)
        run_gate(gate(fix.write_panel("logs.json", p3),
                      scratch=os.path.join(root, "scr2")))
        logs = [f for f in os.listdir(os.path.join(root, "scr2")) if f.endswith(".log")]
        record("leg-logs-written", sorted(logs) == ["good.log", "second.log", "third.log"],
               str(logs))
        repo_new = [f for f in os.listdir(root)
                    if f != "leg.py" and not f.startswith("scr") and
                    not f.endswith(".json")]
        record("repo-untouched", repo_new == [], str(repo_new))


        p_only, _ = base_panel(fix)
        only_panel = fix.write_panel("only.json", p_only)
        # 16 --only scopes the run after the census over the full panel
        rc, out = run_gate(gate(only_panel,
                                scratch=os.path.join(root, "scr3"),
                                extra=["--only", "good", "--only", "second"]))
        record("only-scoped", rc == 0 and "HARM_WATCH: legs=2 ok=2 mismatch=0" in out and
               "LEG good" in out and "LEG second" in out and "LEG third" not in out,
               out[-300:])

        # 17 --only with an undeclared id is a setup error
        rc, out = run_gate(gate(only_panel,
                                scratch=os.path.join(root, "scr4"),
                                extra=["--only", "nosuch"]))
        record("only-unknown-id", rc == 2 and "PANEL_SETUP only-unknown-id=nosuch" in out,
               out[-300:])
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("HARM_WATCH_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
    for f in failed:
        print("FAIL %s" % f)
    return 0 if not failed else 1


def main():
    ap = argparse.ArgumentParser(add_help=True,
                                 description="mado round-99 harm watch (C2)")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--panel")
    ap.add_argument("--scratch-root")
    ap.add_argument("--timeout", type=float)
    ap.add_argument("--only", action="append", default=[], metavar="ID",
                    help="run the census over the full panel, then only the named legs")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    for req in ("repo", "rev", "panel"):
        if not getattr(a, req):
            panel_line("PANEL_SETUP", "missing --%s" % req)
            return 2
    if not os.path.isdir(a.repo):
        return setup_error("PANEL_SETUP", "repo-not-a-dir")
    return run_panel(a)


if __name__ == "__main__":
    sys.exit(main())

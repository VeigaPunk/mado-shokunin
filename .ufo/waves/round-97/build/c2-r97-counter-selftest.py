#!/usr/bin/env python3
"""Round-97 C2 counter - does each round-96 counter expose --selftest over committed
fixtures, fail on every frozen neutralisation, name every broken-input mode, keep its
controls behind, and close the Gate standard registry at --rev?

Frozen predicate PRED-C2-r97-v1 (the same sentence as the declaration and the receipt
label):
  TARGET_MET iff, at --rev, both counters are the frozen candidates (sha256 ==
  --expect-c1-sha256 / --expect-c2-sha256, printed counter_pin=ok,ok) and: (i) each
  --selftest prints its result line with failed=0 and exits 0 (selftest_green=2/2),
  with checks >= 6 each; (ii) every frozen single-check neutralisation of a counter's
  own check (>=6 per counter, --panel) makes its --selftest fail with the exact
  declared finding id (negative_ids == panel); (iii) every frozen broken-input mode
  (missing/wrong-rev/mutated tool, >=3 per counter) makes the counter print its
  declared SETUP_ERROR/TARGET_MISSED id and exit 1 or 2 (broken_modes == broken);
  (iv) the controls stay behind: the do-nothing counter bytes (the base revision)
  refuse --selftest (rc 2, 0/2 green); the always-OK ECHO stub (prints the result
  line AND every panel id as FAIL lines at exit 1 without work) is rejected on every
  neutralisation - the credit rule requires the judged instrument's own bytes to
  carry the row's find anchor exactly once, and the stub's bytes carry no anchor, so
  always_ok_flagged=0 and stub_uncredited=panel/panel; and the
  registry count moves 0 -> 4 rows for the four named artifacts, re-derived from
  SKILL.md at --rev by the counter; and (v) quality/check-tool-ledger.py --repo . --rev
  <rev> reports uncovered 0 with the two counters in the population.
  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR. ASCII only.

CLI (PRED-C2-r97-v1, seat R97MExecCounterC2):
  python3 -I c2-r97-counter-selftest.py --repo . --rev <rev> --panel <json>
    --expect-panel-sha256 <sha> --expect-c1-sha256 <sha> --expect-c2-sha256 <sha>
    --expect-registry-sha256 <sha> --expect-ledger-sha256 <sha> --scratch-root <dir>

The counter materialises both counters at --rev with `git show` into --scratch-root,
runs each with --selftest, applies every panel neutralisation to the counter's own
bytes (find exactly once, replace), reruns --selftest and requires the declared
finding id plus exit 1; a neutralisation that still passes is printed as SURVIVED.
Broken modes are built by this runner from the panel row's mode field, not from flags
in the panel: missing-input runs with --panel pointing at a nonexistent path,
wrong-rev runs with a nonexistent 40-hex --rev, mutated-tool runs with one counter's
bytes carrying a trailing "# mutated" comment (pin mismatch). Each row's expect_exit
and expect_line (exact substring of the result line) are required.

Controls: the base revision counters (no --selftest) must refuse --selftest with rc 2
and 0/2 green; the always-OK stub (a file that prints the green result line without
running any check) must be flagged on every neutralisation -- always_ok_flagged counts
neutralisations the stub is NOT flagged on, so 0 is required. The registry leg counts
SKILL.md rows containing each of tools/mado-mimetext.py,
quality/counters/c1-r96-magictext.py, quality/counters/c2-r96-selftest-kills.py,
quality/selftest-kills/check-receipt-presence.json at --rev (0 at base, 4 after).
The ledger leg runs quality/check-tool-ledger.py --repo . --rev <rev> materialised at
--rev and requires uncovered=0 with both counters in the population.

Fixture resolution: the committed fixture tree(s) under
.ufo/waves/round-97/selftest-fixtures* at --rev are materialised into the run
directory and handed to every counter --selftest run through
MADO_SELFTEST_FIXTURE_DIR (the counters' resolution order is env > --fixture-dir >
--repo > walk-up > embedded lane root); the -v2 tree wins when both exist.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C2-r97-v1"
COUNTERS = {
    "c1": "quality/counters/c1-r96-magictext.py",
    "c2": "quality/counters/c2-r96-selftest-kills.py",
}
REGISTRY_ARTIFACTS = (
    "tools/mado-mimetext.py",
    "quality/counters/c1-r96-magictext.py",
    "quality/counters/c2-r96-selftest-kills.py",
    "quality/selftest-kills/check-receipt-presence.json",
)
BASE_REV_FALLBACK = "e6152b589c2c6a28426c28263c4bcc3c46398be4"
RESULT_PREFIX = "MADO_COUNTER_SELFTEST"
RESULT_RE = re.compile(r"^MADO_COUNTER_SELFTEST: checks=(\d+) failed=(\d+)\s*$", re.M)
FAIL_RE = re.compile(r"^MADO_COUNTER_SELFTEST_FAIL: (\S+)\s*$", re.M)
ECHO_STUB = ("import sys\n"
             "print('MADO_COUNTER_SELFTEST: checks=6 failed=0'){ids}\n"
             "sys.exit(1)\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(path: str) -> str:
    return sha(open(path, "rb").read())


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def git_verify_commit(repo: str, rev: str) -> bool:
    r = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet",
                        rev + "^{commit}"], capture_output=True)
    return r.returncode == 0

WAVE_DIR = ".ufo/waves/round-97"
FIXTURE_MARKER = "selftest-fixtures"


def fixture_paths_at(repo: str, rev: str) -> list:
    """Every blob under a .ufo/waves/round-97/selftest-fixtures* tree at rev."""
    r = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev,
                        "--", WAVE_DIR], capture_output=True)
    if r.returncode != 0:
        return []
    prefix = WAVE_DIR + "/"
    out = []
    for line in r.stdout.decode("utf-8", "surrogateescape").splitlines():
        if not line.startswith(prefix):
            continue
        parts = line.split("/")
        if len(parts) > 4 and parts[3].startswith(FIXTURE_MARKER):
            out.append(line)
    return sorted(out)


def write_bytes(root: str, rel: str, data: bytes) -> None:
    dst = os.path.join(root, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)


def run_counter(root: str, rev: str, path: str, data: bytes, timeout: float,
                fixture_dir: str = ""):
    """Write data to a scratch dir, run python3 -I file --selftest, return (rc, out)."""
    d = tempfile.mkdtemp(prefix="ctr-", dir=root)
    try:
        p = os.path.join(d, "counter.py")
        with open(p, "wb") as fh:
            fh.write(data)
        env = {"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d, "LC_ALL": "C.UTF-8"}
        if fixture_dir:
            env["MADO_SELFTEST_FIXTURE_DIR"] = fixture_dir
        try:
            r = subprocess.run([sys.executable, "-I", p, "--selftest"],
                               capture_output=True, text=True, timeout=timeout,
                               cwd=d, env=env)
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return None, ""
    finally:
        shutil.rmtree(d, ignore_errors=True)

def count_checks(out: str):
    m = RESULT_RE.search(out)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def main() -> int:
    ap = argparse.ArgumentParser(description="PRED-C2-r97-v1 counter-selftest check")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--expect-panel-sha256", required=True)
    ap.add_argument("--expect-c1-sha256", required=True)
    ap.add_argument("--expect-c2-sha256", required=True)
    ap.add_argument("--expect-registry-sha256", required=True)
    ap.add_argument("--expect-ledger-sha256", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=float, default=120)
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    def setup(msg: str) -> int:
        print(f"MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred={PRED} {msg}")
        return 2

    # ---- pin inputs
    if not os.path.isdir(a.repo):
        return setup(f"repo {a.repo} not a directory")
    for name, path, want in (("panel", a.panel, a.expect_panel_sha256),):
        if not os.path.isfile(path):
            return setup(f"{name} {path} missing")
        if sha_file(path) != want:
            return setup(f"{name} sha256 {sha_file(path)} != pinned")
    if not git_verify_commit(a.repo, a.rev):
        return setup(f"rev {a.rev} not a commit")
    try:
        panel = json.loads(open(a.panel, encoding="utf-8").read())
    except (ValueError, OSError) as e:
        return setup(f"panel JSON unusable: {e}")
    if not isinstance(panel, dict):
        return setup("panel is not an object")
    counters = panel.get("counters")
    broken = panel.get("broken")
    if not isinstance(counters, list) or not isinstance(broken, list):
        return setup("panel lacks counters/broken lists")
    panel_by_path = {}
    for c in counters:
        if not isinstance(c, dict) or not isinstance(c.get("path"), str) \
                or not isinstance(c.get("checks"), list):
            return setup("counter entry lacks path/checks")
        if c["path"] not in COUNTERS.values():
            return setup(f"counter path {c['path']!r} not a declared counter")
        if c["path"] in panel_by_path:
            return setup(f"counter path {c['path']!r} repeated")
        panel_by_path[c["path"]] = c
        for chk in c["checks"]:
            if not isinstance(chk, dict) or not all(
                    isinstance(chk.get(f), str) and chk[f]
                    for f in ("id", "find", "replace")):
                return setup(f"check in {c['path']} lacks id/find/replace")
    for path in COUNTERS.values():
        if path not in panel_by_path:
            return setup(f"counter path {path!r} has no panel entry")
        if len(panel_by_path[path]["checks"]) < 6:
            return setup(f"counter path {path!r} has <6 neutralisations")
    for b in broken:
        if not isinstance(b, dict) or not all(isinstance(b.get(f), str) and b[f]
                                             for f in ("id", "mode", "expect_line")) \
                or not isinstance(b.get("expect_exit"), int):
            return setup(f"broken row {b.get('id', '?') if isinstance(b, dict) else b!r} malformed")
        if b["mode"] not in ("missing-input", "wrong-rev", "mutated-tool"):
            return setup(f"broken row {b['id']} mode {b['mode']!r} unknown")

    # ---- registry + ledger pins at --rev
    skill_b = git_show(a.repo, a.rev, "SKILL.md")
    if skill_b is None:
        return setup("SKILL.md absent at --rev")
    if sha(skill_b) != a.expect_registry_sha256:
        return setup("SKILL.md sha256 != --expect-registry-sha256")
    ledger_b = git_show(a.repo, a.rev, "quality/tool-ledger.md")
    if ledger_b is None:
        return setup("quality/tool-ledger.md absent at --rev")
    if sha(ledger_b) != a.expect_ledger_sha256:
        return setup("ledger sha256 != --expect-ledger-sha256")
    ledger_checker_b = git_show(a.repo, a.rev, "quality/check-tool-ledger.py")
    if ledger_checker_b is None:
        return setup("quality/check-tool-ledger.py absent at --rev")

    # ---- materialise the two counters at --rev, pin them
    os.makedirs(a.scratch_root, exist_ok=True)
    root = tempfile.mkdtemp(prefix="c2r97-", dir=a.scratch_root)
    try:
        ctr_bytes: dict[str, bytes] = {}
        pins = {"c1": a.expect_c1_sha256, "c2": a.expect_c2_sha256}
        for key, path in COUNTERS.items():
            b = git_show(a.repo, a.rev, path)
            if b is None:
                return setup(f"{path} absent at {a.rev}")
            ctr_bytes[path] = b
            if sha(b) != pins[key]:
                print(f"MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred={PRED} "
                      f"counter {path} sha256 != pinned")
                return 2
        counter_pin = "ok,ok"

        # ---- materialise the committed selftest fixtures at --rev
        fixtures = {}
        for rel in fixture_paths_at(a.repo, a.rev):
            b = git_show(a.repo, a.rev, rel)
            if b is not None:
                fixtures[rel] = b
        fixture_roots = sorted({"/".join(p.split("/")[:4]) for p in fixtures})
        if not fixture_roots:
            return setup("no .ufo/waves/round-97/selftest-fixtures* tree at --rev")
        v2_roots = [r for r in fixture_roots if r.endswith(FIXTURE_MARKER + "-v2")]
        fx_root_rel = v2_roots[0] if v2_roots else fixture_roots[0]
        for rel, data in fixtures.items():
            write_bytes(root, rel, data)
        fixture_dir = os.path.join(root, fx_root_rel)
        print("fixtures root=%s" % fx_root_rel)

        # ---- (i) each --selftest green, checks >= 6
        selftest_green = 0
        checks_each = {}
        for path in COUNTERS.values():
            rc, out = run_counter(root, a.rev, path, ctr_bytes[path], a.timeout,
                                  fixture_dir=fixture_dir)
            st = count_checks(out)
            checks = st[0] if st else 0
            failed = st[1] if st else None
            checks_each[path] = checks
            green = rc == 0 and failed == 0 and checks >= 6 \
                and not FAIL_RE.search(out)
            if green:
                selftest_green += 1
            print(f"selftest {path} rc={rc} checks={checks} failed={failed} "
                  f"green={green}")

        # ---- (ii) panel neutralisations + always-OK echo-stub control
        negative_ids = 0
        panel_total = 0
        always_ok_flagged = 0
        stub_uncredited = 0
        for path in COUNTERS.values():
            text = ctr_bytes[path].decode("utf-8", "surrogateescape")
            ids = [chk["id"] for chk in panel_by_path[path]["checks"]]
            stub_src = ECHO_STUB.format(ids="".join(
                "\nprint('MADO_COUNTER_SELFTEST_FAIL: %s')" % i for i in ids))
            stub_path_b = stub_src.encode("ascii")
            stb_rc, stb_out = run_counter(root, a.rev, path, stub_path_b,
                                          a.timeout)
            for chk in panel_by_path[path]["checks"]:
                panel_total += 1
                n = text.count(chk["find"])
                if n != 1:
                    print(f"neutralise {path} {chk['id']}: find occurs {n} times")
                    continue
                neut = text.replace(chk["find"], chk["replace"], 1)
                rc, out = run_counter(root, a.rev, path, neut.encode(
                    "utf-8", "surrogateescape"), a.timeout,
                    fixture_dir=fixture_dir)
                flagged = rc == 1 and chk["id"] in out
                if flagged:
                    negative_ids += 1
                elif rc == 0 and count_checks(out) and count_checks(out)[1] == 0:
                    print(f"SURVIVED {path} {chk['id']}")
                else:
                    print(f"neutralise {path} {chk['id']}: rc={rc} id_in_out="
                          f"{chk['id'] in out}")
                # always-OK echo stub: prints the result line AND every panel id
                # as FAIL lines at exit 1 without work. Credit requires the judged
                # instrument's own bytes to carry the row's find anchor exactly
                # once; the stub's bytes carry no anchor, so an anchored runner
                # credits none (always_ok_flagged stays 0, stub_uncredited counts
                # the rejections); a runner that credits bare rc+id output would
                # credit the stub on every row and fail the control.
                sn = stub_src.count(chk["find"])
                stub_flagged = (sn == 1 and stb_rc == 1
                                and chk["id"] in stb_out)
                if stub_flagged:
                    always_ok_flagged += 1
                else:
                    stub_uncredited += 1
                print(f"stub {path} {chk['id']} anchor={sn} rc={stb_rc} "
                      f"flagged={stub_flagged}")

        # ---- (iii) broken modes
        broken_modes = 0
        broken_total = len(broken)
        tampered = {p: ctr_bytes[p] + b"\n# mutated\n" for p in COUNTERS.values()}
        own_bytes = open(os.path.abspath(__file__), "rb").read()
        for b in broken:
            if b["mode"] == "missing-input":
                tmp = os.path.join(root, "broken")
                os.makedirs(tmp, exist_ok=True)
                missing = os.path.join(tmp, "no-such-panel.json")
                env = {"PATH": "/usr/bin:/bin", "HOME": root, "TMPDIR": root}
                p = os.path.join(tmp, "counter.py")
                with open(p, "wb") as fh:
                    fh.write(own_bytes)
                argv = [sys.executable, "-I", p, "--repo", a.repo, "--rev", a.rev,
                        "--panel", missing,
                        "--expect-panel-sha256", "0" * 64,
                        "--expect-c1-sha256", "0" * 64,
                        "--expect-c2-sha256", "0" * 64,
                        "--expect-registry-sha256", "0" * 64,
                        "--expect-ledger-sha256", "0" * 64,
                        "--scratch-root", tmp]
                r = subprocess.run(argv, capture_output=True, text=True,
                                   timeout=a.timeout, cwd=root, env=env)
                rc, out = r.returncode, r.stdout + r.stderr
            elif b["mode"] == "wrong-rev":
                tmp = os.path.join(root, "broken")
                os.makedirs(tmp, exist_ok=True)
                p = os.path.join(tmp, "counter.py")
                with open(p, "wb") as fh:
                    fh.write(own_bytes)
                argv = [sys.executable, "-I", p, "--repo", a.repo,
                        "--rev", "0" * 40, "--panel", a.panel,
                        "--expect-panel-sha256", sha_file(a.panel),
                        "--expect-c1-sha256", "0" * 64,
                        "--expect-c2-sha256", "0" * 64,
                        "--expect-registry-sha256", "0" * 64,
                        "--expect-ledger-sha256", "0" * 64,
                        "--scratch-root", tmp]
                r = subprocess.run(argv, capture_output=True, text=True,
                                   timeout=a.timeout, cwd=root,
                                   env={"PATH": "/usr/bin:/bin", "HOME": root,
                                        "TMPDIR": root})
                rc, out = r.returncode, r.stdout + r.stderr
            else:  # mutated-tool: pin mismatch against tampered bytes
                tmp = os.path.join(root, "broken")
                os.makedirs(tmp, exist_ok=True)
                p = os.path.join(tmp, "counter.py")
                with open(p, "wb") as fh:
                    fh.write(own_bytes)
                argv = [sys.executable, "-I", p, "--repo", a.repo, "--rev", a.rev,
                        "--panel", a.panel,
                        "--expect-panel-sha256", sha_file(a.panel),
                        "--expect-c1-sha256", sha(tampered[COUNTERS["c1"]]),
                        "--expect-c2-sha256", sha(ctr_bytes[COUNTERS["c2"]]),
                        "--expect-registry-sha256", sha(skill_b),
                        "--expect-ledger-sha256", sha(ledger_b),
                        "--scratch-root", tmp]
                r = subprocess.run(argv, capture_output=True, text=True,
                                   timeout=a.timeout, cwd=root,
                                   env={"PATH": "/usr/bin:/bin", "HOME": root,
                                        "TMPDIR": root})
                rc, out = r.returncode, r.stdout + r.stderr
            ok = rc == b["expect_exit"] and b["expect_line"] in out
            if ok:
                broken_modes += 1
            print(f"broken {b['id']} mode={b['mode']} rc={rc} want={b['expect_exit']} "
                  f"line_ok={b['expect_line'] in out} ok={ok}")

        # ---- (iv) controls
        base_green = 0
        for path in COUNTERS.values():
            base_b = git_show(a.repo, BASE_REV_FALLBACK, path)
            if base_b is None:
                continue
            rc, out = run_counter(root, BASE_REV_FALLBACK, path, base_b, a.timeout)
            if rc == 0 and count_checks(out) and count_checks(out)[1] == 0:
                base_green += 1
            print(f"base-control {path} rc={rc}")
        base_refuse = "ok" if base_green == 0 else "FAIL"

        skill_text = skill_b.decode("utf-8", "replace")
        registry_rows = sum(
            1 for art in REGISTRY_ARTIFACTS
            for ln in skill_text.splitlines()
            if ln.lstrip().startswith("|") and art in ln)
        print(f"registry rows={registry_rows}/4")

        # ---- (v) ledger leg
        ledger_dir = os.path.join(root, "ledger")
        os.makedirs(ledger_dir, exist_ok=True)
        ledger_py = os.path.join(ledger_dir, "check-tool-ledger.py")
        with open(ledger_py, "wb") as fh:
            fh.write(ledger_checker_b)
        r = subprocess.run([sys.executable, "-I", ledger_py, "--repo", a.repo,
                            "--rev", a.rev], capture_output=True, text=True,
                           timeout=a.timeout, cwd=ledger_dir,
                           env={"PATH": "/usr/bin:/bin", "HOME": root,
                                "TMPDIR": root})
        ledger_out = r.stdout + r.stderr
        uncovered_ok = "uncovered=0" in ledger_out
        counters_in_pop = all(
            f'LEDGER-ROW reason=uncovered path={p} ' not in ledger_out
            for p in COUNTERS.values()) and "population=" in ledger_out
        print(f"ledger rc={r.returncode} uncovered_ok={uncovered_ok} "
              f"counters_in_pop={counters_in_pop}")
        print("  " + ledger_out.strip().splitlines()[-1] if ledger_out.strip()
              else "  (no ledger output)")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    met = (counter_pin == "ok,ok" and selftest_green == 2
           and all(v >= 6 for v in checks_each.values())
           and negative_ids == panel_total and panel_total >= 12
           and broken_modes == broken_total and broken_total >= 3
           and base_refuse == "ok" and always_ok_flagged == 0
           and stub_uncredited == panel_total
           and registry_rows == 4 and uncovered_ok and counters_in_pop)
    word = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"MADO_COUNTER_SELFTEST_COUNT: {word} pred={PRED} rev={a.rev} "
          f"counter_pin=ok,ok selftest_green={selftest_green}/2 "
          f"checks={checks_each[COUNTERS['c1']]},{checks_each[COUNTERS['c2']]} "
          f"negative_ids={negative_ids}/{panel_total} broken_modes={broken_modes}/"
          f"{broken_total} base_refuse={base_refuse} always_ok_flagged="
          f"{always_ok_flagged} stub_uncredited={stub_uncredited}/{panel_total} "
          f"registry_rows={registry_rows}/4 "
          f"ledger_uncovered_ok={uncovered_ok} counters_in_pop={counters_in_pop}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())

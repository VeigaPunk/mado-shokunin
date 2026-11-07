#!/usr/bin/env python3
"""Round-97 C2 counter (v2) - does each round-96 counter expose --selftest over committed
fixtures, fail on every frozen neutralisation with its declared finding id, survive every
frozen broken-input mode, keep its controls behind, and close the Gate standard registry
at --rev against the measured base?

Frozen predicate PRED-C2-r97-v1 (revised before the freeze on R97MReviewC2 findings
3.1-3.4; the same sentence as the declaration and the receipt label):
  TARGET_MET iff, at --rev and with --base-rev (the pre-landing revision), both counters
  are the frozen candidates (sha256 == --expect-c1-sha256 / --expect-c2-sha256, printed
  counter_pin=ok,ok) and: (i) each --selftest prints its result line with failed=0 and
  exits 0 (selftest_green=2/2), with checks >= 6 each; (ii) every frozen single-check
  neutralisation of a counter's own check (>=6 per counter, --panel) makes its --selftest
  fail with the exact declared finding id (negative_ids == panel, survivors printed);
  (iii) every frozen broken-input mode carries its counter ("counter" in the panel entry;
  missing-input / wrong-rev / mutated-tool, >=3 per counter) and makes that counter print
  its declared SETUP_ERROR/TARGET_MISSED id and exit 1 or 2 (broken_modes == broken,
  per-counter counts printed); (iv) the controls stay behind: the base revision's counter
  bytes (no --selftest) refuse with rc 2 and 0/2 green, and the counter rejects the
  always-OK echo stub on EVERY neutralisation (the stub prints the result line and every
  panel id as FAIL lines at exit 1 without work; stub_uncredited=panel/panel and
  always_ok_flagged=0); the registry instrument rows (tools/mado-mimetext.py and the two
  counters; the receipt-presence kill-set is a pinned input named inside the existing
  mado-selftest-strength row's population, not a registry row) are re-derived from
  SKILL.md at BOTH --base-rev and --rev (measured base: one instrument row,
  tools/mado-mimetext.py) and move 1 -> 3 (registry=1->3); and (v) both counters are
  ledger rows in the population at --rev (the counter reads quality/tool-ledger.md at
  --rev, finds a row for each of the two paths and prints ledger_members=2/2; this is an
  invariant, unchanged from base), while
  quality/check-tool-ledger.py --repo . --rev <rev> prints uncovered=0.
  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR. ASCII only.

CLI (every argument named; the published counting command uses exactly these):
  python3 -I c2-r97-counter-selftest.v2.py --repo . --rev <rev> --base-rev <base>
    --expect-base-registry-sha256 <sha> --panel <json> --expect-panel-sha256 <sha>
    --expect-c1-sha256 <sha> --expect-c2-sha256 <sha> --expect-registry-sha256 <sha>
    --expect-ledger-sha256 <sha> --scratch-root <dir> [--timeout SEC] [--min-checks N]

--min-checks (default 6) is the checks>=N floor for leg (i) and for the panel's
per-counter neutralisation minimum; the published command omits it, so the frozen
predicate floor of 6 applies at measurement. It exists so a scratch dry run can score a
two-check panel against synthetic counters.

Broken-mode constructions (contract 4: each row names its counter; the mode is applied to
THAT counter's --selftest, never to this runner's own bytes). Common invocation: the
counter bytes from <rev>:<counter path> materialised at <root>/quality/counters/<name>.py
inside a layout root that also carries the quality/ + tools/ + SKILL.md support tree
extracted byte-exact from --rev with `git archive` (the counters' REPO-dependent checks
open quality/* under REPO = the layout root; the 500MB+ .ufo history is deliberately not
extracted), cwd=<layout root>, env PATH=/usr/bin:/bin, HOME/TMPDIR inside the run dir,
and MADO_SELFTEST_REPO=<layout root> (read first for REPO by the landed counters).
The fixture TREE ROOT is passed explicitly as `--fixture-dir <abs>` on every
selftest-form invocation (the counters' resolution order is MADO_SELFTEST_FIXTURE_DIR >
--fixture-dir > --repo > walk-up > committed lane path, so an explicit dir is the only
shape that cannot silently read the lane's working-tree fixtures); the counters must
treat a given --fixture-dir that is absent or unparseable as terminal SETUP_ERROR
(agreed with the counters' seat). If a counter does NOT declare --fixture-dir (argparse
rc 2 "unrecognized arguments"), the invocation is retried ONCE with the bare contract-4
spelling and its own fixture resolution governs (printed as an `invocation` detail
line); a counter-side SETUP_ERROR is never retried.
  green/neutralise: --fixture-dir <root>/<fixture-root>
  missing-input:    --fixture-dir <root>/absent-fixtures-<i>  (never created; REPO
                    resolves to the layout root via cwd, so only fixture checks fail)
  wrong-rev:        --fixture-dir <root>/.ufo/waves/round-97/selftest-fixtures-wrongrev-<i>
                    (tree copied from <fixture-root>, every file truncated to 0 bytes -
                    the --base-rev fixture state, which carries no round-97 fixtures)
  mutated-tool:     --fixture-dir <root>/.ufo/waves/round-97/selftest-fixtures-mutated-<i>
                    (tree copied intact; the fixture file named by the row's required
                    "path" field carries a trailing "\n# mutated-tool probe\n" - the
                    pinned dummy tool the counter's pin branch checks)
The fixture root is .ufo/waves/round-97/selftest-fixtures-v2 when that tree exists at
--rev, else .ufo/waves/round-97/selftest-fixtures (printed as `fixtures root=...`).
The always-OK stub and the base-revision control take no --fixture-dir (the stub is this
runner's own file; the base bytes refuse --selftest at argparse before any fixture
access).

always_ok_flagged counts the panel neutralisations for which the always-OK ECHO stub is
CREDITED with flagging; stub_uncredited counts the neutralisations on which the counter
REJECTS the stub, and must equal the panel (the clause is "the counter rejects the stub
on every neutralisation", not "the stub flags nothing"). The stub (R97MCritic2 C2-5,
L1-strengthened) prints the result line AND every panel id as FAIL lines at exit 1 while
doing no work; the credit rule requires the judged instrument's OWN bytes to carry the
row's find anchor exactly once, the run to exit 1 with the declared FAIL id, AND the
unneutralised baseline of the same instrument not to print that id already. The stub's
bytes carry no anchor, so it is credited with none: always_ok_flagged=0 and
stub_uncredited=panel/panel.

Detail lines (never more than one MADO_COUNTER_SELFTEST_COUNT: line per run):
  selftest <path> rc=<rc> checks=<n> failed=<n> green=<bool>
  neutralise <path> <id>: find occurs <n> times | rc=<rc> id_ok=<bool> | SURVIVED
  stub <path> <id> rc=<rc> flagged=<bool>
  broken <id> counter=<path> mode=<mode> rc=<rc> want=<n> line_ok=<bool> ok=<bool>
  base-control <path> rc=<rc> green=<bool>
  registry <artifact> base=<n> rev=<n> (table-row pairs)
  ledger row <path> present=<bool> / ledger rc=<rc> uncovered_ok=<bool> + LEDGER: line

The registry count covers the three INSTRUMENT rows only (R97MCritic C2-2, L1 ruling:
the receipt-presence kill-set is a pinned input named inside the existing
mado-selftest-strength row's population, not a registry row), counted as per-artifact
COVERAGE (an instrument counts once when at least one table row names it); the printed
registry=<b>-><r> is the covered count, 1 -> 3.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

PRED = "PRED-C2-r97-v1"
COUNTERS = {
    "c1": "quality/counters/c1-r96-magictext.py",
    "c2": "quality/counters/c2-r96-selftest-kills.py",
}
REGISTRY_ARTIFACTS = (
    # instrument rows only (R97MCritic C2-2, L1 ruling): the receipt-presence kill-set
    # is a pinned input named inside the existing mado-selftest-strength row's
    # population, not a registry row of its own
    "tools/mado-mimetext.py",
    "quality/counters/c1-r96-magictext.py",
    "quality/counters/c2-r96-selftest-kills.py",
)
LEDGER_PATH = "quality/tool-ledger.md"
LEDGER_CHECKER = "quality/check-tool-ledger.py"
WAVE_DIR = ".ufo/waves/round-97"
FIXTURE_MARKER = "selftest-fixtures"
RESULT_RE = re.compile(r"^MADO_COUNTER_SELFTEST: checks=(\d+) failed=(\d+)\s*$", re.M)
FAIL_PREFIX = "MADO_COUNTER_SELFTEST_FAIL: "
MODES = ("missing-input", "wrong-rev", "mutated-tool")
TAMPER_SUFFIX = "\n# mutated-tool probe\n"
# always-OK control (R97MCritic2 C2-5, L1-strengthened): prints the result line AND
# every panel id as FAIL lines (as if it had run and flagged them all) while doing no
# work; the runner passes the panel ids as argv after --selftest. A credit rule that
# only checks "rc 1 + declared id in output" would credit this stub for every
# neutralisation; the credit rule below must (and does) credit none.
ECHO_STUB = ("import sys\n"
             "toks = sys.argv[1:]\n"
             "if toks and toks[0] == '--selftest':\n"
             "    toks = toks[1:]\n"
             "for t in toks:\n"
             "    print('MADO_COUNTER_SELFTEST_FAIL: %s' % t)\n"
             "print('MADO_COUNTER_SELFTEST: checks=6 failed=%d' % len(toks))\n"
             "sys.exit(1)\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha(fh.read())


def git_run(repo: str, args: list) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", repo] + args, capture_output=True)


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = git_run(repo, ["show", "%s:%s" % (rev, path)])
    return r.stdout if r.returncode == 0 else None


def git_is_commit(repo: str, rev: str) -> bool:
    return git_run(repo, ["rev-parse", "--verify", "--quiet",
                          rev + "^{commit}"]).returncode == 0


def child_env(root: str) -> dict:
    return {"PATH": "/usr/bin:/bin", "HOME": root, "TMPDIR": root,
            "LC_ALL": "C.UTF-8", "MADO_SELFTEST_REPO": root}


def run_py(file_path: str, cwd: str, root: str, timeout: float,
           extra: list | None = None) -> tuple:
    """Run `python3 -I <file> [--extra] --selftest` with cwd; return (rc, output).

    When an explicit --fixture-dir was passed and the counter itself refuses the flag
    (argparse rc 2 with "unrecognized arguments"), retry ONCE with the bare contract-4
    spelling -- the counter's own fixture resolution then governs, and the fallback is
    printed as an `invocation` detail line. A counter-side SETUP_ERROR (explicit-dir
    terminal, e.g. the missing-input scene) does not contain that text and is never
    retried."""
    argv_extra = list(extra or [])
    try:
        r = subprocess.run([sys.executable, "-I", file_path, "--selftest"]
                           + argv_extra,
                           capture_output=True, text=True, errors="replace",
                           timeout=timeout, cwd=cwd, env=child_env(root))
        rc, out = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return None, ""
    if argv_extra and rc == 2 and "unrecognized arguments" in out:
        print("invocation %s: --fixture-dir refused (unrecognized arguments); "
              "retried bare" % os.path.basename(file_path))
        try:
            r = subprocess.run([sys.executable, "-I", file_path, "--selftest"],
                               capture_output=True, text=True, errors="replace",
                               timeout=timeout, cwd=cwd, env=child_env(root))
            return r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return None, ""
    return rc, out


def result_of(out: str):
    m = RESULT_RE.search(out)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def fail_id_present(out: str, finding_id: str) -> bool:
    return re.search(r"^" + re.escape(FAIL_PREFIX + finding_id) + r"\s*$", out, re.M) \
        is not None


def fixture_paths_at(repo: str, rev: str) -> list:
    """Every blob under a .ufo/waves/round-97/selftest-fixtures* tree at rev."""
    r = git_run(repo, ["ls-tree", "-r", "--name-only", rev, "--", WAVE_DIR])
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


def validate_panel(panel, min_checks: int, setup):
    if not isinstance(panel, dict):
        return setup("panel is not an object")
    counters = panel.get("counters")
    broken = panel.get("broken")
    if not isinstance(counters, list) or not isinstance(broken, list):
        return setup("panel lacks counters/broken lists")
    by_path = {}
    for c in counters:
        if not isinstance(c, dict) or not isinstance(c.get("path"), str) \
                or not isinstance(c.get("checks"), list):
            return setup("counter entry lacks path/checks")
        if c["path"] not in COUNTERS.values():
            return setup("counter path %r not a declared counter" % c["path"])
        if c["path"] in by_path:
            return setup("counter path %r repeated" % c["path"])
        by_path[c["path"]] = c
        if len(c["checks"]) < min_checks:
            return setup("counter %s has %d checks < %d"
                         % (c["path"], len(c["checks"]), min_checks))
        for chk in c["checks"]:
            if not isinstance(chk, dict) or not all(
                    isinstance(chk.get(f), str) and chk[f]
                    for f in ("id", "find", "replace")):
                return setup("check in %s lacks id/find/replace" % c["path"])
    for path in COUNTERS.values():
        if path not in by_path:
            return setup("counter path %r has no panel entry" % path)
    per_counter = {p: 0 for p in COUNTERS.values()}
    for b in broken:
        if not isinstance(b, dict) or not isinstance(b.get("id"), str) or not b["id"] \
                or not isinstance(b.get("counter"), str) \
                or not isinstance(b.get("mode"), str) \
                or not isinstance(b.get("expect_line"), str) or not b["expect_line"]:
            return setup("broken row %r malformed" % (b.get("id") if isinstance(b, dict)
                                                      else b))
        if b["counter"] not in COUNTERS.values():
            return setup("broken row %s names unknown counter %r"
                         % (b["id"], b["counter"]))
        if b["mode"] not in MODES:
            return setup("broken row %s mode %r unknown" % (b["id"], b["mode"]))
        if not isinstance(b.get("expect_exit"), int) \
                or b["expect_exit"] not in (1, 2):
            return setup("broken row %s expect_exit must be 1 or 2" % b["id"])
        if b["mode"] == "mutated-tool":
            p = b.get("path")
            if not isinstance(p, str) or not p or p.startswith("/") \
                    or ".." in p.split("/"):
                return setup("broken row %s needs a relative fixture 'path'"
                             % b["id"])
        per_counter[b["counter"]] += 1
    for path, n in per_counter.items():
        if n < 3:
            return setup("counter %s has %d broken rows < 3" % (path, n))
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="PRED-C2-r97-v1 counter-selftest check (v2)")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True, dest="base_rev")
    ap.add_argument("--expect-base-registry-sha256", required=True,
                    dest="expect_base_registry_sha256")
    ap.add_argument("--panel", required=True)
    ap.add_argument("--expect-panel-sha256", required=True)
    ap.add_argument("--expect-c1-sha256", required=True)
    ap.add_argument("--expect-c2-sha256", required=True)
    ap.add_argument("--expect-registry-sha256", required=True)
    ap.add_argument("--expect-ledger-sha256", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=float, default=600.0)
    ap.add_argument("--min-checks", type=int, default=6, dest="min_checks",
                    help="checks>=N floor (default 6, the frozen predicate floor); "
                         "lower it only for scratch dry runs")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    repo = os.path.abspath(a.repo)

    def setup(msg: str) -> int:
        print("MADO_COUNTER_SELFTEST_COUNT: SETUP_ERROR pred=%s %s" % (PRED, msg))
        return 2

    # ---- input pins and shapes (all SETUP_ERROR paths run before any leg)
    if not os.path.isdir(repo):
        return setup("repo %s not a directory" % a.repo)
    if not git_is_commit(repo, a.rev):
        return setup("rev %s not a commit" % a.rev)
    if not git_is_commit(repo, a.base_rev):
        return setup("base-rev %s not a commit" % a.base_rev)
    if not os.path.isfile(a.panel):
        return setup("panel %s missing" % a.panel)
    if sha_file(a.panel) != a.expect_panel_sha256:
        return setup("panel sha256 %s != pinned %s"
                     % (sha_file(a.panel), a.expect_panel_sha256))
    try:
        with open(a.panel, encoding="utf-8") as fh:
            panel = json.load(fh)
    except (ValueError, OSError) as exc:
        return setup("panel JSON unusable: %s" % exc)
    bad = validate_panel(panel, a.min_checks, setup)
    if bad is not None:
        return bad

    skill_rev = git_show(repo, a.rev, "SKILL.md")
    if skill_rev is None:
        return setup("SKILL.md absent at --rev")
    if sha(skill_rev) != a.expect_registry_sha256:
        return setup("SKILL.md sha256 != --expect-registry-sha256")
    skill_base = git_show(repo, a.base_rev, "SKILL.md")
    if skill_base is None:
        return setup("SKILL.md absent at --base-rev")
    if sha(skill_base) != a.expect_base_registry_sha256:
        return setup("SKILL.md sha256 != --expect-base-registry-sha256")
    ledger_rev = git_show(repo, a.rev, LEDGER_PATH)
    if ledger_rev is None:
        return setup("%s absent at --rev" % LEDGER_PATH)
    if sha(ledger_rev) != a.expect_ledger_sha256:
        return setup("ledger sha256 != --expect-ledger-sha256")
    checker_b = git_show(repo, a.rev, LEDGER_CHECKER)
    if checker_b is None:
        return setup("%s absent at --rev" % LEDGER_CHECKER)

    fixtures = {}
    for rel in fixture_paths_at(repo, a.rev):
        data = git_show(repo, a.rev, rel)
        if data is None:
            return setup("fixture %s unreadable at --rev" % rel)
        fixtures[rel] = data
    if not fixtures:
        return setup("no .ufo/waves/round-97/%s* tree at --rev" % FIXTURE_MARKER)

    fixture_roots = sorted({"/".join(p.split("/")[:4]) for p in fixtures})
    v2_roots = [r for r in fixture_roots if r.endswith(FIXTURE_MARKER + "-v2")]
    fx_root_rel = v2_roots[0] if v2_roots else fixture_roots[0]
    tamper_targets: dict[int, list] = {}
    for i, b in enumerate(panel["broken"]):
        if b["mode"] != "mutated-tool":
            continue
        wanted = {fx_root_rel + "/" + b["path"]}
        hits = [p for p in fixtures if p in wanted]
        if not hits:
            return setup("broken row %s path %r not under the invoked fixture root "
                         "(%s)" % (b["id"], b["path"], fx_root_rel))
        tamper_targets[i] = hits

    os.makedirs(a.scratch_root, exist_ok=True)
    root = tempfile.mkdtemp(prefix="c2r97-", dir=a.scratch_root)
    try:
        # ---- support tree: the counters' --selftest REPO-dependent checks open
        # quality/* (and may open tools/*) under REPO = the layout root; materialise
        # those subtrees byte-exact from --rev with `git archive` (never the working
        # tree). The whole 500MB+ .ufo history is deliberately NOT extracted.
        want = [p for p in ("quality", "tools", "SKILL.md")
                if git_run(repo, ["ls-tree", "--name-only", a.rev, "--",
                                  p]).stdout.strip()]
        if "quality" not in want:
            return setup("no quality/ subtree at --rev (the counters' REPO-dependent "
                         "selftest checks open quality/*)")
        arch = subprocess.run(["git", "-C", repo, "archive", "--format=tar", a.rev,
                               "--"] + want, capture_output=True)
        if arch.returncode != 0:
            return setup("git archive %s (%s) failed: %s"
                         % (a.rev, " ".join(want),
                            arch.stderr.decode("utf-8", "replace").strip()[:200]))
        try:
            with tarfile.open(fileobj=io.BytesIO(arch.stdout)) as tf:
                tf.extractall(root, filter="data")
        except (tarfile.TarError, OSError) as exc:
            return setup("support-tree extraction failed: %s" % exc)
        for sentinel in ("quality/check-selftest-strength.py",
                         "quality/check-receipt-presence.py"):
            if not os.path.exists(os.path.join(root, sentinel)):
                return setup("support tree at --rev lacks %s (the counters' "
                             "REPO-dependent selftest checks open it)" % sentinel)

        # ---- materialise the two counters at --rev, pin them
        ctr_bytes: dict[str, bytes] = {}
        pins = {"c1": a.expect_c1_sha256, "c2": a.expect_c2_sha256}
        for key, path in COUNTERS.items():
            b = git_show(repo, a.rev, path)
            if b is None:
                return setup("%s absent at %s" % (path, a.rev))
            if sha(b) != pins[key]:
                return setup("counter %s sha256 %s != pinned %s"
                             % (path, sha(b), pins[key]))
            ctr_bytes[path] = b
        counter_pin = "ok,ok"
        for path, data in ctr_bytes.items():
            write_bytes(root, path, data)
        for rel, data in fixtures.items():
            write_bytes(root, rel, data)
        ctr_fs = {path: os.path.join(root, path) for path in COUNTERS.values()}
        fx_dir = os.path.join(root, fx_root_rel)
        print("fixtures root=%s" % fx_root_rel)

        # ---- (i) each --selftest green, checks >= min_checks
        selftest_green = 0
        checks_each = {}
        green_out: dict[str, str] = {}
        for path in COUNTERS.values():
            rc, out = run_py(ctr_fs[path], root, root, a.timeout,
                             ["--fixture-dir", fx_dir])
            green_out[path] = out
            st = result_of(out)
            checks = st[0] if st else 0
            failed = st[1] if st else None
            checks_each[path] = checks
            green = rc == 0 and st is not None and failed == 0 \
                and checks >= a.min_checks and FAIL_PREFIX not in out
            if green:
                selftest_green += 1
            print("selftest %s rc=%s checks=%s failed=%s green=%s"
                  % (path, rc, checks, failed, green))

        # ---- (ii) panel neutralisations + always-OK echo-stub control
        # Credit rule (R97MCritic2 C2-5, L1-strengthened): a neutralisation is credited
        # only when the judged instrument's OWN bytes carry the row's find anchor
        # exactly once, the run exits 1 with the declared FAIL id, and the
        # unneutralised baseline of the same instrument does not already print that id.
        # The echo stub prints every panel id at rc 1 without work; its bytes carry no
        # find anchor, so it is credited with none (always_ok_flagged=0).
        negative_ids = 0
        panel_total = 0
        always_ok_flagged = 0
        stub_uncredited = 0
        stub_path = os.path.join(root, "always-ok-stub.py")
        stub_src = ECHO_STUB
        with open(stub_path, "wb") as fh:
            fh.write(stub_src.encode("ascii"))
        stub_base_rc, stub_base_out = run_py(stub_path, root, root, a.timeout)
        all_ids = [chk["id"] for c in panel["counters"] for chk in c["checks"]]
        checks_by_path = {c["path"]: c["checks"] for c in panel["counters"]}
        for path in COUNTERS.values():
            text = ctr_bytes[path].decode("utf-8", "surrogateescape")
            for chk in checks_by_path[path]:
                panel_total += 1
                n = text.count(chk["find"])
                if n != 1:
                    print("neutralise %s %s: find occurs %d times"
                          % (path, chk["id"], n))
                else:
                    neut = text.replace(chk["find"], chk["replace"], 1)
                    # neutralised bytes go to the counter's real layout path so any
                    # __file__-relative fixture derivation sees the same layout as
                    # the green run; the original bytes are restored after the run
                    with open(ctr_fs[path], "wb") as fh:
                        fh.write(neut.encode("utf-8", "surrogateescape"))
                    rc, out = run_py(ctr_fs[path], root, root, a.timeout,
                                     ["--fixture-dir", fx_dir])
                    with open(ctr_fs[path], "wb") as fh:
                        fh.write(ctr_bytes[path])
                    flagged = (rc == 1
                               and fail_id_present(out, chk["id"])
                               and not fail_id_present(green_out[path], chk["id"]))
                    if flagged:
                        negative_ids += 1
                    elif rc == 0 and (st := result_of(out)) and st[1] == 0:
                        print("SURVIVED %s %s" % (path, chk["id"]))
                    else:
                        print("neutralise %s %s: rc=%s id_ok=%s"
                              % (path, chk["id"], rc,
                                 fail_id_present(out, chk["id"])))
                src_rc, src_out = run_py(stub_path, root, root, a.timeout,
                                         list(all_ids))
                stub_flagged = (stub_src.count(chk["find"]) == 1
                                and src_rc == 1
                                and fail_id_present(src_out, chk["id"])
                                and not fail_id_present(stub_base_out, chk["id"]))
                if stub_flagged:
                    always_ok_flagged += 1
                else:
                    stub_uncredited += 1
                print("stub %s %s rc=%s flagged=%s"
                      % (path, chk["id"], src_rc, stub_flagged))

        # ---- (iii) broken modes, each against its own counter. Every invocation runs
        # the counter from the layout root (cwd = layout root, MADO_SELFTEST_REPO set),
        # so the counter's REPO (FIX/../../../.. with "selftest-fixtures" in FIX, or
        # the env override) always sees the same quality/ support tree, and the mode
        # isolates fixture state only, via --fixture-dir:
        #   missing-input: a fixture dir that does not exist
        #   wrong-rev:     a selftest-fixtures* sibling inside the layout root whose
        #                  files are truncated to 0 bytes (the --base-rev fixture
        #                  state, which carries no round-97 fixtures)
        #   mutated-tool:  a selftest-fixtures* sibling whose fixture file named by
        #                  the row's "path" carries a trailing tamper line
        broken_ok = 0
        broken_per = {p: [0, 0] for p in COUNTERS.values()}
        prefix = fx_root_rel + "/"
        for i, b in enumerate(panel["broken"]):
            if b["mode"] == "missing-input":
                fixdir = os.path.join(root, "absent-fixtures-%02d" % i)
            else:
                fixdir = os.path.join(root, ".ufo", "waves", "round-97",
                                      "%s-%s-%02d" % (FIXTURE_MARKER, b["mode"], i))
                for rel, data in fixtures.items():
                    if rel.startswith(prefix):
                        write_bytes(fixdir, rel[len(prefix):],
                                    b"" if b["mode"] == "wrong-rev" else data)
                if b["mode"] == "mutated-tool":
                    for rel in tamper_targets.get(i, []):
                        with open(os.path.join(fixdir, rel[len(prefix):]),
                                  "ab") as fh:
                            fh.write(TAMPER_SUFFIX.encode("ascii"))
            rc, out = run_py(ctr_fs[b["counter"]], root, root, a.timeout,
                             ["--fixture-dir", fixdir])
            line_ok = b["expect_line"] in out
            ok = rc == b["expect_exit"] and line_ok
            if ok:
                broken_ok += 1
                broken_per[b["counter"]][0] += 1
            broken_per[b["counter"]][1] += 1
            print("broken %s counter=%s mode=%s rc=%s want=%s line_ok=%s ok=%s"
                  % (b["id"], b["counter"], b["mode"], rc, b["expect_exit"],
                     line_ok, ok))
        broken_total = len(panel["broken"])

        # ---- (iv) controls: base bytes refuse --selftest
        base_green = 0
        for path in COUNTERS.values():
            base_b = git_show(repo, a.base_rev, path)
            if base_b is None:
                return setup("%s absent at --base-rev" % path)
            scene = os.path.join(root, "base", os.path.basename(path))
            os.makedirs(scene, exist_ok=True)
            bfile = os.path.join(scene, "counter.py")
            with open(bfile, "wb") as fh:
                fh.write(base_b)
            rc, out = run_py(bfile, scene, scene, a.timeout)
            green = rc == 0 and (st := result_of(out)) is not None and st[1] == 0
            if green:
                base_green += 1
            print("base-control %s rc=%s green=%s" % (path, rc, green))
        base_refuse = "ok" if base_green == 0 else "FAIL"

        # ---- registry rows at both revisions (per-artifact coverage: an artifact
        # counts once when >=1 table row names it; prose duplicates cannot inflate)
        def registry_rows(skill: bytes) -> tuple:
            text = skill.decode("utf-8", "replace")
            per = [sum(1 for ln in text.splitlines()
                       if ln.lstrip().startswith("|") and art in ln)
                   for art in REGISTRY_ARTIFACTS]
            covered = sum(1 for n in per if n >= 1)
            return covered, per

        reg_base, reg_base_per = registry_rows(skill_base)
        reg_rev, reg_rev_per = registry_rows(skill_rev)
        for art, b_n, r_n in zip(REGISTRY_ARTIFACTS, reg_base_per, reg_rev_per):
            print("registry %s base=%d rev=%d (table-row pairs)" % (art, b_n, r_n))
        print("registry artifacts covered base=%d rev=%d" % (reg_base, reg_rev))

        # ---- (v) ledger membership at --rev + the ledger gate
        ledger_text = ledger_rev.decode("utf-8", "replace")
        members = [any(ln.lstrip().startswith("|") and p in ln
                       for ln in ledger_text.splitlines())
                   for p in COUNTERS.values()]
        ledger_members = sum(members)
        for p, m in zip(COUNTERS.values(), members):
            print("ledger row %s present=%s" % (p, m))
        ledger_dir = os.path.join(root, "ledger")
        os.makedirs(ledger_dir, exist_ok=True)
        checker_fs = os.path.join(ledger_dir, "check-tool-ledger.py")
        with open(checker_fs, "wb") as fh:
            fh.write(checker_b)
        uncovered_ok = False
        ledger_tail = ""
        try:
            r = subprocess.run(
                [sys.executable, "-I", checker_fs, "--repo", repo, "--rev", a.rev],
                capture_output=True, text=True, errors="replace",
                timeout=a.timeout, cwd=ledger_dir, env=child_env(root))
            out = r.stdout + r.stderr
            uncovered_ok = "uncovered=0" in out
            tails = [ln for ln in out.splitlines() if ln.startswith("LEDGER:")]
            ledger_tail = tails[-1] if tails else out.strip().splitlines()[-1] \
                if out.strip() else ""
            print("ledger rc=%d uncovered_ok=%s" % (r.returncode, uncovered_ok))
        except subprocess.TimeoutExpired:
            print("ledger rc=TIMEOUT uncovered_ok=False")
        if ledger_tail:
            print("  " + ledger_tail)

        met = (counter_pin == "ok,ok"
               and selftest_green == 2
               and all(v >= a.min_checks for v in checks_each.values())
               and negative_ids == panel_total
               and panel_total >= 2 * a.min_checks
               and broken_ok == broken_total
               and all(v[0] == v[1] and v[1] >= 3 for v in broken_per.values())
               and base_refuse == "ok"
               and always_ok_flagged == 0
               and stub_uncredited == panel_total
               and reg_base == 1 and reg_rev == 3
               and ledger_members == 2
               and uncovered_ok)
        word = "TARGET_MET" if met else "TARGET_MISSED"
        print("MADO_COUNTER_SELFTEST_COUNT: %s pred=%s rev=%s base=%s counter_pin=%s "
              "selftest_green=%d/2 checks=%d,%d negative_ids=%d/%d "
              "broken_modes=%d/%d broken_c1=%d/%d broken_c2=%d/%d base_refuse=%s "
              "always_ok_flagged=%d stub_uncredited=%d/%d registry=%d->%d "
              "ledger_members=%d/2 ledger_uncovered_ok=%s"
              % (word, PRED, a.rev, a.base_rev, counter_pin, selftest_green,
                 checks_each[COUNTERS["c1"]], checks_each[COUNTERS["c2"]],
                 negative_ids, panel_total, broken_ok, broken_total,
                 broken_per[COUNTERS["c1"]][0], broken_per[COUNTERS["c1"]][1],
                 broken_per[COUNTERS["c2"]][0], broken_per[COUNTERS["c2"]][1],
                 base_refuse, always_ok_flagged, stub_uncredited, panel_total,
                 reg_base, reg_rev, ledger_members, uncovered_ok))
        return 0 if met else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

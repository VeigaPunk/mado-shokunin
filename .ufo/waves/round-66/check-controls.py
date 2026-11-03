#!/usr/bin/env python3
"""check-controls.py — round-66 C1/C2 control harness (seat R66ExecHarness draft; L1 installs at wave root).

Frozen count commands (claims-declaration-r66.md; immutable):
  python3 .ufo/waves/round-66/check-controls.py --repo . --rev REV --claim c1 --scratch-root /fast/scratch/hyaku/mado-r66/measure
  python3 .ufo/waves/round-66/check-controls.py --repo . --rev REV --claim c2 --scratch-root /fast/scratch/hyaku/mado-r66/measure

What it does, deterministically and with no fabricated rows:
  * Extracts the r65 baseline instruments from git objects at --rev only
    (C1: quality/counters/c1-r65-register.py; C2: quality/landing-counters.sh plus
    quality/check-tool-ledger.py, quality/counters/c3-r56-used-by.py,
    tools/mado-receipt-citecheck.py). The worktree of --repo is never read.
  * Detects the candidate instrument: first in the tree at --rev
    (quality/counters/c1-r66-register.py / quality/landing-counters.sh candidate
    bytes), else the seat drafts under <script_dir>/w1/R66ExecRegister and
    R66ExecLanding (or --candidate-dir). Absent candidate => baseline-only mode:
    the frozen cases still run against the r65 instruments, the baseline score and
    the do-nothing failure are recorded, and the command exits 1 because the frozen
    target (candidate correct=4/4) cannot be met without a candidate.
  * Builds one independent minimal fixture git repo per case under --scratch-root
    (never /tmp-family, never the lane). C1 fixtures carry the real gate/fileplane
    receipt objects from --rev and vary PROVINCE.md only. C2 fixtures carry the
    extracted instrument tree plus corpus/receipt stubs and exercise the four child
    legs through a PATH python3 shim that emits the children's real contract
    markers with case-controlled rc (skip/crash/red), or no shim at all (case d:
    the used-by sibling file is genuinely absent).
  * Runs the same frozen cases on baseline and candidate, prints per case
    `expected=<V>/<rc> ... correct=` counts, `correct=N/4 TARGET_MET|TARGET_MISSED`,
    and exits 0 only when the candidate scores 4/4.

Every input byte and every raw output is preserved under
<scratch-root>/r66harness/<claim>/ (extracted instruments, per-case fixtures,
per-case raw stdout/stderr/rc, sha256 digests in digests.txt).

Exit codes: 0 candidate 4/4; 1 target missed (includes baseline-only mode);
2 setup error. No network, no host changes, no lane writes.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

BASELINE = {
    "c1": ("quality/counters/c1-r65-register.py",),
    "c2": (
        "quality/landing-counters.sh",
        "quality/check-tool-ledger.py",
        "quality/counters/c3-r56-used-by.py",
        "tools/mado-receipt-citecheck.py",
    ),
}
# Candidate generation markers in the tree at --rev. C1 has per-generation files;
# C2 extends quality/landing-counters.sh in place, so the r66 generation is
# identified by the new driver's presence (claims: "absent c1-r66 identifies
# baseline"; same rule for the c2-r66 driver).
CANDIDATE_AT_REV = {
    "c1": "quality/counters/c1-r66-register.py",
    "c2": "quality/counters/c2-r66-landing-instrument.py",
}
C2_INSTRUMENT = "quality/landing-counters.sh"
# Declared round-66 base (claims-declaration-r66.md): the pre-cutover tree whose
# landing-counters.sh bytes are the r65 baseline instrument.
BASE_REV = "eafd500fa7be76dca59e729435e231a5032cc037"
CARRY_RECEIPTS = (
    ".ufo/waves/round-65/receipts/gate-live-r65.txt",
    ".ufo/waves/round-65/receipts/gate-fileplane-r65.txt",
)
LIVE_RECEIPT = CARRY_RECEIPTS[0]
FILEPLANE_RECEIPT = CARRY_RECEIPTS[1]

GROUPS = (
    "hypr plane", "waybar", "walker", "terminal configs",
    "theme/wallpaper omarchy plane", "idle/lock plane", "omarchy skill docs",
    "windows desktop plane",
)
HEADING = "### Surface state register (2026-11-03"
SENTINEL = "<!-- r65 register end -->"
LIVE_TOKEN = ".ufo/waves/round-65/receipts/gate-live-r65.txt"
FILEPLANE_TOKEN = ".ufo/waves/round-65/receipts/gate-fileplane-r65.txt"

# Frozen expected map (claims-declaration-r66.md): the candidate must produce
# exactly these (verdict, rc) on the four frozen cases of its claim.
EXPECTED_C1 = (
    ("genuine", ("TARGET_MET", 0)),
    ("duplicate-heading", ("TARGET_MISSED", 1)),
    ("row-without-receipt", ("TARGET_MISSED", 1)),
    ("file-plane-only", ("TARGET_MISSED", 1)),
)
EXPECTED_C2 = (
    ("a-genuine-red", ("RED", 1)),
    ("b-child-crash", ("ERROR", 2)),
    ("c-skip-no-marker", ("ERROR", 2)),
    ("d-missing-usedby", ("ERROR", 2)),
)
# Diagnostic cases: measured and reported, never counted in X/4.
# diag-unreferenced-live-accepted discloses the narrowed control coverage ruled by
# L1: with the live object present, the candidate intentionally accepts rows that
# never cite it (citation gap stays open by design; not tightened after scores).
DIAG_C1 = (("diag-no-register", ("TARGET_MISSED", 1)),
           ("diag-fileplane-at-live-path", ("TARGET_MISSED", 1)),
           ("diag-unreferenced-live-accepted", ("TARGET_MET", 0)))
DIAG_C2 = (("diag-all-green", ("GREEN", 0)),
           ("diag-real-children", None))

SHIM = r"""#!/usr/bin/env bash
# R66ExecHarness case shim: dispatches the four landing legs by child script path.
# Emits the legs' real contract marker shapes with case-controlled rc.
# nav passes through to the real python3 so the navigation leg stays genuine.
set -u
case "${1:-}" in
  -) leg=nav ;;
  */c3-r56-used-by.py) leg=usedby ;;
  */check-tool-ledger.py) leg=ledger ;;
  */mado-receipt-citecheck.py) leg=citecheck ;;
  *) printf 'shim: unexpected child argv: %s\n' "$*" >&2; exit 2 ;;
esac
printf '%s\n' "$leg" >>"$WITNESS"
if [ "$leg" = "$TEST_LEG" ]; then
  case "$TEST_MODE" in
    skip) exit 0 ;;
    crash) exit 2 ;;
  esac
fi
rc=0
if [ "$leg" = "$TEST_LEG" ] && [ "$TEST_MODE" = red ]; then rc=1; fi
if [ "$leg" = nav ]; then
  if [ "$rc" -eq 0 ]; then exec "$REAL_PYTHON" "$@"; fi
  printf 'revision=%s indexed=1/2 missing=1 dangling=0 duplicates=0 coverage=5.0000/10\n' "$FIXTURE_REV"
  exit 1
fi
case "$leg" in
  usedby)
    if [ "$rc" -eq 0 ]; then
      printf 'MADO_USED_BY: rev=%s entries=1 rows=1 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=TARGET_MET missed=none\n' "$FIXTURE_REV"
    else
      printf 'MADO_USED_BY: rev=%s entries=1 rows=1 missing=1 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=0 verdict=TARGET_MISSED missed=rows\n' "$FIXTURE_REV"
    fi ;;
  ledger)
    if [ "$rc" -eq 0 ]; then
      printf 'LEDGER: population=1 ledger_rows=1 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET rev=%s\n' "$FIXTURE_REV"
    else
      printf 'LEDGER: population=1 ledger_rows=1 uncovered=1 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=%s\n' "$FIXTURE_REV"
    fi ;;
  citecheck)
    if [ "$rc" -eq 0 ]; then
      printf 'MADO_CITECHECK: rev=%s files=1 citations=1 resolved=1 missing=0 skipped_large=0 verdict=TARGET_MET\n' "$FIXTURE_REV"
    else
      printf 'MADO_CITECHECK: rev=%s files=1 citations=1 resolved=0 missing=1 skipped_large=0 verdict=TARGET_MISSED\n' "$FIXTURE_REV"
    fi ;;
esac
exit "$rc"
"""


def die(message):
    sys.stderr.write("check-controls: %s\n" % message)
    raise SystemExit(2)


def git_bytes(repo, rev, path):
    """One object read at rev; None when the path is absent at rev."""
    proc = subprocess.run(
        ["git", "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120,
        env=clean_env())
    return proc.stdout if proc.returncode == 0 else None


def path_at_rev(repo, rev, path):
    proc = subprocess.run(
        ["git", "-C", repo, "cat-file", "-e", "%s:%s" % (rev, path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
        env=clean_env())
    return proc.returncode == 0


def clean_env(extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C"
    env["GIT_PAGER"] = "cat"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    if extra:
        env.update(extra)
    return env


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def run(argv, cwd, env=None, timeout=600):
    proc = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env or clean_env(),
                          timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


def commit_fixture(fxdir):
    """Init a scratch fixture repo, verify its toplevel, commit, return HEAD."""
    run(["git", "init", "-q"], fxdir)
    top = run(["git", "-C", fxdir, "rev-parse", "--show-toplevel"], fxdir)
    if top[0] != 0 or os.path.realpath(top[1].decode().strip()) != os.path.realpath(fxdir):
        die("fixture toplevel verification failed: %s" % fxdir)
    run(["git", "-C", fxdir, "add", "-A"], fxdir)
    rc, _, err = run(["git", "-C", fxdir, "-c", "user.name=R66ExecHarness",
                      "-c", "user.email=r66exec-harness@example.invalid",
                      "-c", "commit.gpgsign=false", "commit", "-q",
                      "-m", "r66 harness fixture"], fxdir)
    if rc != 0:
        die("fixture commit failed: %s" % err.decode("utf-8", "replace").strip())
    head = run(["git", "-C", fxdir, "rev-parse", "HEAD"], fxdir)
    return head[1].decode().strip()


# ---------------------------------------------------------------- C1 fixtures
def province_genuine():
    lines = [
        "# harness fixture province",
        "",
        "R66ExecHarness C1 fixture. Receipts are real bytes carried from the measured",
        "revision; only this file varies between cases.",
        "",
        "%s, harness fixture)" % HEADING,
        "",
        "| surface group | state (date) | probe (read-only) | receipt |",
        "|---|---|---|---|",
    ]
    for group in GROUPS:
        lines.append("| %s | fixture state (2026-11-03) | probe-%s | %s |"
                     % (group, group.split()[0].replace("/", "-"), LIVE_TOKEN))
    lines += ["", SENTINEL, ""]
    return "\n".join(lines).encode("utf-8")


def province_duplicate():
    dup = [
        "",
        "%s, harness fixture duplicate)" % HEADING,
        "",
        "| surface group | state (date) | probe (read-only) | receipt |",
        "|---|---|---|---|",
        "| hypr plane | duplicate block (2026-11-03) | probe-hypr | %s |" % LIVE_TOKEN,
        "",
        SENTINEL,
        "",
    ]
    return province_genuine() + "\n".join(dup).encode("utf-8")


def province_row_without_receipt():
    return province_genuine().replace(
        b"| walker | fixture state (2026-11-03) | probe-walker | %s |" % LIVE_TOKEN.encode(),
        b"| walker | fixture state (2026-11-03) | probe-walker | none |")


def province_fileplane_only():
    return province_genuine().replace(LIVE_TOKEN.encode(), FILEPLANE_TOKEN.encode())


def province_no_register():
    return (b"# harness fixture province\n\nno surface state register block here\n")


C1_PROVINCES = {
    "genuine": province_genuine,
    "duplicate-heading": province_duplicate,
    "row-without-receipt": province_row_without_receipt,
    "file-plane-only": province_fileplane_only,
    "diag-no-register": province_no_register,
    "diag-fileplane-at-live-path": province_genuine,
    "diag-unreferenced-live-accepted": province_fileplane_only,
}


def build_c1_fixture(root, case, carry):
    """One fixture repo: carried real receipts + one PROVINCE variant."""
    fx = os.path.join(root, "fx-%s" % case)
    if os.path.exists(fx):
        shutil.rmtree(fx)
    os.makedirs(fx)
    write_bytes(os.path.join(fx, "PROVINCE.md"), C1_PROVINCES[case]())
    if case == "file-plane-only":
        # L1 ruling: the control is a real only-file-plane receipt tree — the
        # LIVE_PATH object is omitted entirely, not merely uncited. The r65
        # baseline must still accept this exact tree.
        for rel, data in carry.items():
            if rel != LIVE_RECEIPT:
                write_bytes(os.path.join(fx, rel), data)
    elif case == "diag-fileplane-at-live-path":
        # Diagnostic only: the live receipt slot carries the real file-plane bytes.
        write_bytes(os.path.join(fx, LIVE_RECEIPT), carry[FILEPLANE_RECEIPT])
        write_bytes(os.path.join(fx, FILEPLANE_RECEIPT), carry[FILEPLANE_RECEIPT])
    else:
        for rel, data in carry.items():
            write_bytes(os.path.join(fx, rel), data)
    rev_f = commit_fixture(fx)
    return fx, rev_f


def classify_c1(rc, out):
    token = None
    for line in out.decode("utf-8", "replace").splitlines():
        if line.startswith(("MADO_R65_REGISTER:", "MADO_R66_REGISTER:")):
            for field in line.split():
                if field.startswith("verdict="):
                    token = field.split("=", 1)[1]
    if token is None:
        token = "TARGET_MISSED" if rc != 0 else "GREEN"
    return token, rc


# ---------------------------------------------------------------- C2 fixtures
C2_STUBS = {
    "corpus/README.md": "| `knowledge/n.md` |\n",
    "corpus/knowledge/n.md": "# note\n",
    ".ufo/waves/round-65/receipts/a.txt": "cite corpus/README.md\n",
    ".ufo/waves/round-66/receipts/a.txt": "cite corpus/README.md\n",
}


def build_c2_fixture(root, case, instrument_bytes, siblings):
    """Fixture wt = extracted instrument tree + stubs; sibling used-by removable."""
    fx = os.path.join(root, "fx-%s" % case)
    if os.path.exists(fx):
        shutil.rmtree(fx)
    instrument_rel = BASELINE["c2"][0]
    write_bytes(os.path.join(fx, instrument_rel), instrument_bytes)
    os.chmod(os.path.join(fx, instrument_rel), 0o755)
    for rel, data in siblings.items():
        write_bytes(os.path.join(fx, rel), data)
        os.chmod(os.path.join(fx, rel), 0o755)
    for rel, data in C2_STUBS.items():
        write_bytes(os.path.join(fx, rel), data.encode("utf-8"))
    if case == "d-missing-usedby":
        os.remove(os.path.join(fx, "quality/counters/c3-r56-used-by.py"))
    rev_f = commit_fixture(fx)
    return fx, rev_f


def write_shim(root, case):
    shim_dir = os.path.join(root, "shim-%s" % case)
    if os.path.exists(shim_dir):
        shutil.rmtree(shim_dir)
    os.makedirs(shim_dir)
    write_bytes(os.path.join(shim_dir, "python3"), SHIM.encode("utf-8"))
    os.chmod(os.path.join(shim_dir, "python3"), 0o755)
    return shim_dir


C2_LEG_CASE = {
    "a-genuine-red": ("usedby", "red"),
    "b-child-crash": ("usedby", "crash"),
    "c-skip-no-marker": ("usedby", "skip"),
    "d-missing-usedby": (None, None),
    # ("none", "green"): shim active, no leg tampered — all four genuine green
    # markers with rc 0.  (None, None): no shim at all — real children against a
    # minimal fixture; expectations are per-impl, so expected is None.
    "diag-all-green": ("none", "green"),
    "diag-real-children": (None, None),
}


def run_c2_case(case, instrument_path, fx, rev_f, scratch_root, candidate):
    """Run one landing case; returns (verdict, rc). Uses the PATH shim for a-c."""
    env = clean_env()
    env["SCRATCH_ABS"] = os.path.join(scratch_root, "run-%s" % case)
    witness = os.path.join(scratch_root, "witness-%s.txt" % case)
    write_bytes(witness, b"")
    leg, mode = C2_LEG_CASE[case]
    if leg is not None or mode is not None:
        real_python = shutil.which("python3") or die("python3 not found")
        env.update(WITNESS=witness, TEST_LEG=leg, TEST_MODE=mode,
                   FIXTURE_REV=rev_f, REAL_PYTHON=real_python)
        env["PATH"] = write_shim(scratch_root, case) + os.pathsep + env["PATH"]
    cmd = ["bash", instrument_path, "--repo", fx, "--rev", rev_f,
           "--scratch-root", env["SCRATCH_ABS"]]
    if candidate:
        cmd += ["--round", "66"]
    rc, out, err = run(cmd, fx, env=env)
    write_bytes(os.path.join(scratch_root, "run-%s.out" % case), out)
    write_bytes(os.path.join(scratch_root, "run-%s.err" % case), err)
    write_bytes(os.path.join(scratch_root, "run-%s.rc" % case),
                b"%d\n" % rc)
    write_bytes(os.path.join(scratch_root, "cmd-%s.txt" % case),
                (" ".join(cmd) + "\n").encode("utf-8"))
    token = None
    for line in out.decode("utf-8", "replace").splitlines():
        if line.startswith("MADO_LANDING_COUNTERS:"):
            token = line.split(":", 1)[1].strip().split()[0]
    if token is None:
        token = {0: "GREEN", 1: "RED"}.get(rc, "ERROR")
    return token, rc


# ---------------------------------------------------------------- driver
def extract_baseline(repo, rev, claim, evdir):
    extracted = {}
    for rel in BASELINE[claim]:
        data = git_bytes(repo, rev, rel)
        if data is None:
            die("baseline instrument missing at %s: %s" % (rev, rel))
        extracted[rel] = data
        write_bytes(os.path.join(evdir, "extracted", os.path.basename(rel)), data)
    return extracted


def detect_candidate(repo, rev, claim, candidate_draft, evdir):
    """Candidate bytes come from the tree at --rev ONLY (frozen command never
    falls back to moving worktree drafts). An explicit --candidate-draft PATH is
    a diagnostic mode for pre-integration scoring and is labelled as such."""
    rel = CANDIDATE_AT_REV[claim]
    marker = git_bytes(repo, rev, rel)
    data = None
    source = None
    if marker is not None:
        if claim == "c2":
            data = git_bytes(repo, rev, C2_INSTRUMENT)
            if data is None:
                die("candidate marker %s present but %s missing at %s"
                    % (rel, C2_INSTRUMENT, rev))
            source = "rev:%s (marker %s present)" % (C2_INSTRUMENT, rel)
        else:
            data = marker
            source = "rev:%s" % rel
    elif candidate_draft:
        if not os.path.isfile(candidate_draft):
            die("--candidate-draft is not a file: %s" % candidate_draft)
        with open(candidate_draft, "rb") as handle:
            data = handle.read()
        source = "draft-diagnostic:%s" % candidate_draft
    if data is None:
        return None, None
    write_bytes(os.path.join(evdir, "extracted", "candidate-" + os.path.basename(rel)),
                data)
    return data, source


def score(rows, frozen):
    counted = [(c, exp) for c, exp in frozen]
    return rows, counted


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="round-66 C1/C2 control harness (baseline r65 instruments vs candidate)")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--claim", required=True, choices=("c1", "c2"))
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--candidate-draft", default=None,
                    help="DIAGNOSTIC ONLY: score this pre-integration candidate draft "
                         "file; the frozen command never uses worktree drafts")
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        die("--repo is not a directory: %s" % repo)
    if subprocess.run(["git", "-C", repo, "rev-parse", "--git-dir"],
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      env=clean_env()).returncode != 0:
        die("--repo is not a git repository: %s" % repo)
    raw = os.path.abspath(args.scratch_root)
    probe = raw
    while True:
        if os.path.islink(probe):
            die("--scratch-root refused: symlink component: %s" % probe)
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    real_root = os.path.realpath(raw)
    for refused in ("/tmp", "/var/tmp", "/dev/shm"):
        if real_root == refused or real_root.startswith(refused + os.sep):
            die("--scratch-root refused: %s-family root: %s" % (refused, real_root))
    os.makedirs(real_root, exist_ok=True)
    # Never reuse predictable child paths under a shared scratch root: a
    # pre-planted extracted/ symlink must not redirect object writes.
    private_root = tempfile.mkdtemp(prefix="r66harness-", dir=real_root)
    evdir = os.path.join(private_root, args.claim)
    os.makedirs(os.path.join(evdir, "extracted"), exist_ok=True)
    summary_path = os.path.join(evdir, "summary.txt")

    def emit(line):
        """Print the verdict lines and keep them as evidence beside the raw runs."""
        print(line)
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    write_bytes(summary_path, b"")
    emit("evidence_root=%s" % evdir)

    # C1 baseline: the frozen r65 counter file at --rev. C2 baseline: the
    # pre-cutover landing-counters.sh at the declared base rev -- after the
    # cutover, --rev no longer carries r65 bytes at that shared path.
    baseline_rev = args.rev if args.claim == "c1" else BASE_REV
    baseline = extract_baseline(repo, baseline_rev, args.claim, evdir)
    candidate_bytes, candidate_source = detect_candidate(
        repo, args.rev, args.claim, args.candidate_draft, evdir)

    carry = {}
    if args.claim == "c1":
        for rel in CARRY_RECEIPTS:
            data = git_bytes(repo, args.rev, rel)
            if data is None:
                die("receipt missing at %s: %s" % (args.rev, rel))
            carry[rel] = data
            write_bytes(os.path.join(evdir, "extracted", os.path.basename(rel)), data)

    expected = EXPECTED_C1 if args.claim == "c1" else EXPECTED_C2
    diag = DIAG_C1 if args.claim == "c1" else DIAG_C2
    cases = [name for name, _ in expected] + [name for name, _ in diag]

    digest_items = list(baseline.items())
    if candidate_bytes is not None:
        digest_items.append(("candidate", candidate_bytes))
    digests = []
    for label, data in sorted(digest_items):
        digests.append("%s  %s" % (sha256(data), label))
    if args.claim == "c1":
        for rel, data in carry.items():
            digests.append("%s  carried:%s" % (sha256(data), rel))

    # Extraction mirrors repo-relative layout: both instruments resolve their
    # siblings from their own real path (r65: $SELF_DIR/../quality/...;
    # candidate: $SELF_DIR/counters/...), so flat extraction would break them.
    base_tree = os.path.join(evdir, "baseline-tree")
    cand_tree = os.path.join(evdir, "candidate-tree")
    for rel, data in baseline.items():
        write_bytes(os.path.join(base_tree, rel), data)
        os.chmod(os.path.join(base_tree, rel), 0o755)
    if candidate_bytes is not None:
        cand_rel = C2_INSTRUMENT if args.claim == "c2" else CANDIDATE_AT_REV[args.claim]
        write_bytes(os.path.join(cand_tree, cand_rel), candidate_bytes)
        os.chmod(os.path.join(cand_tree, cand_rel), 0o755)

    rows = {}
    gates = {}
    if args.claim == "c1":
        base_py = os.path.join(base_tree, BASELINE["c1"][0])
        cand_py = os.path.join(cand_tree, CANDIDATE_AT_REV["c1"])
        if candidate_bytes is not None:
            # Claims C1: "Selftest required" — the candidate's hermetic selftest
            # is a verdict gate (currently 15 cases, strings only).
            rc, out, err = run(["python3", cand_py, "--selftest"], evdir)
            gates["selftest"] = rc
            write_bytes(os.path.join(evdir, "candidate-selftest.out"), out)
            write_bytes(os.path.join(evdir, "candidate-selftest.err"), err)
            write_bytes(os.path.join(evdir, "candidate-selftest.rc"), b"%d\n" % rc)
        for case in cases:
            fx, rev_f = build_c1_fixture(evdir, case, carry)
            row = {"fixture": fx, "fixture_rev": rev_f}
            rc, out, err = run(["python3", base_py, "--repo", fx, "--rev", rev_f], evdir)
            write_bytes(os.path.join(evdir, "baseline-%s.out" % case), out)
            write_bytes(os.path.join(evdir, "baseline-%s.err" % case), err)
            write_bytes(os.path.join(evdir, "baseline-%s.rc" % case), b"%d\n" % rc)
            row["baseline"] = classify_c1(rc, out)
            if candidate_bytes is not None:
                rc, out, err = run(["python3", cand_py, "--repo", fx, "--rev", rev_f],
                                   evdir)
                write_bytes(os.path.join(evdir, "candidate-%s.out" % case), out)
                write_bytes(os.path.join(evdir, "candidate-%s.err" % case), err)
                write_bytes(os.path.join(evdir, "candidate-%s.rc" % case), b"%d\n" % rc)
                row["candidate"] = classify_c1(rc, out)
            rows[case] = row
    else:
        siblings = {rel: baseline[rel] for rel in BASELINE["c2"][1:]}
        siblings_cand = siblings
        if candidate_bytes is not None and candidate_source.startswith("rev:"):
            siblings_cand = {}
            for rel in BASELINE["c2"][1:]:
                data = git_bytes(repo, args.rev, rel)
                if data is None:
                    die("candidate dependency missing at %s: %s" % (args.rev, rel))
                siblings_cand[rel] = data
        # Each instrument runs from inside its committed fixture wt: both
        # generations resolve their sibling children from their own real path,
        # so the fixture — not a separate extraction tree — must carry them.
        # Case d removes the used-by sibling there, making it genuinely absent
        # at the instrument's resolution path.
        if candidate_bytes is not None:
            rc, out, err = run(["bash", os.path.join(cand_tree, C2_INSTRUMENT),
                                "--selftest", "--scratch-root",
                                os.path.join(evdir, "candidate", "st")], evdir)
            gates["selftest"] = rc
            write_bytes(os.path.join(evdir, "candidate-selftest.out"), out)
            write_bytes(os.path.join(evdir, "candidate-selftest.err"), err)
            write_bytes(os.path.join(evdir, "candidate-selftest.rc"), b"%d\n" % rc)
        for case in cases:
            fx, rev_f = build_c2_fixture(evdir, case, baseline[BASELINE["c2"][0]],
                                         siblings)
            row = {"fixture": fx, "fixture_rev": rev_f}
            row["baseline"] = run_c2_case(case, os.path.join(fx, BASELINE["c2"][0]),
                                          fx, rev_f,
                                          os.path.join(evdir, "baseline"), False)
            if candidate_bytes is not None:
                fx2, rev_f2 = build_c2_fixture(evdir, case,
                                               candidate_bytes, siblings_cand)
                row["fixture_candidate"] = fx2
                row["fixture_rev_candidate"] = rev_f2
                row["candidate"] = run_c2_case(case, os.path.join(fx2, C2_INSTRUMENT),
                                               fx2, rev_f2,
                                               os.path.join(evdir, "candidate"), True)
            rows[case] = row

    if args.claim == "c1":
        for case, fn in C1_PROVINCES.items():
            digests.append("%s  province:%s" % (sha256(fn()), case))
    digests.append("%s  shim:python3" % sha256(SHIM.encode("utf-8")))
    write_bytes(os.path.join(evdir, "digests.txt"),
                ("\n".join(digests) + "\n").encode("utf-8"))

    emit("claim=%s rev=%s baseline_from=%s candidate=%s"
          % (args.claim, args.rev, baseline_rev, candidate_source or "absent"))
    base_ok = cand_ok = 0
    frozen_names = {name for name, _ in expected}
    for case, exp in list(expected) + list(diag):
        if exp is None:
            brow = rows[case]["baseline"]
            line = "case=%s expected=observe-only baseline=%s/%d" \
                   % (case, brow[0], brow[1])
            if candidate_bytes is not None:
                crow = rows[case]["candidate"]
                line += " candidate=%s/%d" % (crow[0], crow[1])
            emit(line + " (diagnostic, uncounted)")
            continue
        line = "case=%s expected=%s/%d" % (case, exp[0], exp[1])
        brow = rows[case]["baseline"]
        bhit = brow == exp
        base_ok += bhit if case in frozen_names else 0
        line += " baseline=%s/%d baseline_correct=%d" % (brow[0], brow[1], bhit)
        if candidate_bytes is not None:
            crow = rows[case]["candidate"]
            chit = crow == exp
            cand_ok += chit if case in frozen_names else 0
            line += " candidate=%s/%d candidate_correct=%d" % (crow[0], crow[1], chit)
        if case not in frozen_names:
            line += " (diagnostic, uncounted)"
        print(line)
    total = len(expected)
    emit("baseline correct=%d/%d" % (base_ok, total))
    if candidate_bytes is not None:
        emit("candidate correct=%d/%d" % (cand_ok, total))
    # Claims gates beyond the four cases: candidate selftest must be green; for
    # C2 the frozen target adds the real landing leg — the r66 driver at --rev
    # must run the standing instrument against --repo and return TARGET_MET.
    # In draft-diagnostic mode the driver is absent at rev: skipped, disclosed.
    verdict_ok = candidate_bytes is not None and cand_ok == total
    if candidate_bytes is not None:
        st_rc = gates.get("selftest")
        emit("candidate selftest rc=%s" % ("n/a" if st_rc is None else st_rc))
        verdict_ok = verdict_ok and st_rc == 0
        if args.claim == "c2":
            if candidate_source.startswith("rev:"):
                driver_rel = CANDIDATE_AT_REV["c2"]
                driver_path = os.path.join(cand_tree, driver_rel)
                write_bytes(driver_path, git_bytes(repo, args.rev, driver_rel))
                os.chmod(driver_path, 0o755)
                d_rc, d_out, d_err = run(
                    ["python3", driver_path, "--repo", repo, "--rev", args.rev,
                     "--scratch-root", os.path.join(evdir, "candidate", "driver")],
                    evdir, timeout=1800)
                write_bytes(os.path.join(evdir, "candidate-driver.out"), d_out)
                write_bytes(os.path.join(evdir, "candidate-driver.err"), d_err)
                write_bytes(os.path.join(evdir, "candidate-driver.rc"), b"%d\n" % d_rc)
                d_tok = None
                for d_line in d_out.decode("utf-8", "replace").splitlines():
                    if d_line.startswith("MADO_R66_INSTRUMENT:"):
                        for field in d_line.split():
                            if field.startswith("verdict="):
                                d_tok = field.split("=", 1)[1]
                emit("candidate driver rc=%d verdict=%s" % (d_rc, d_tok or "none"))
                verdict_ok = verdict_ok and d_rc == 0 and d_tok == "TARGET_MET"
            else:
                emit("candidate driver=skipped (draft-diagnostic mode: driver "
                     "absent at rev; the frozen command runs it at an integrated rev)")
    verdict = "TARGET_MET" if verdict_ok else "TARGET_MISSED"
    emit("correct=%d/%d %s mode=%s"
          % (cand_ok if candidate_bytes is not None else base_ok, total, verdict,
             "candidate" if candidate_bytes is not None else "baseline-only"))
    if candidate_bytes is None:
        emit("do_nothing=baseline r65 instruments cannot meet the frozen target; "
              "baseline score recorded above; run again after L1 integrates the "
              "candidates to score the candidate column")
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""R56W3MutC2Harness — mutation test of the round-56 C2 control harness.

Target: quality/r56_ctl_c2.py (and its dispatcher quality/check-r56-controls.py) as landed at the lane tip
0f3a54361a9824484d0801679ceb1fd8ac7c32e1 (the harness blob is identical at the content revision 8a7b7346…).

Method (lane scratch rules; the lane is never written to, the fleet repo is never touched):
  * a fresh git repo D in scratch holds `git archive 0f3a543…` (the whole lane tree) committed as `base`, plus one
    commit per PROBE whose TREE is base + exactly one change (a tool copy, a ctl stub, a fixture note byte);
  * each MUTANT is applied to a COPY of the harness in scratch (never to the lane, never to the repo);
  * the mutated harness is run on every probe and its observable (rc, stdout line, stderr sandbox token,
    refusal marker, work-dir leftovers) is compared with the PRISTINE harness's observable on the SAME probe;
    a difference means the mutant changed the harness's behaviour.

Classification (both readings of the seat are reported):
  * strict oracle  = the frozen claim PRED-C2-r56-v2 observables only: P1 (green line + rc 0 on the good tree),
    P2 (no-bwrap must fail closed), P3 (degraded --no-sandbox must report sandbox=none);
  * extended oracle = the strict oracle plus the discrimination probes (cheat tool, broken tool, wrong-rc tool,
    tampered fixture note, tampered hold-out note, and the three mutated control stubs);
  * KILLED-STRICT  = a strict observable differs (the lane's own evidence catches the mutant);
  * KILLED-EXTENDED= only an extended observable differs (the green line still holds — the claim is weakened);
  * SURVIVED       = no observable differs (coverage finding; a proposal is required);
  * EQUIVALENT     = SURVIVED plus an argument that the mutation cannot change the measured behaviour.

Usage: driver.py <scratch-dir> <deliverable-dir>
"""
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TIP = "0f3a54361a9824484d0801679ceb1fd8ac7c32e1"
HARNESS = "quality/r56_ctl_c2.py"
DISPATCH = "quality/check-r56-controls.py"
STRICT = ("P1_base", "P2_nobwrap_refusal", "P3_nobwrap_degraded")

# ---------------------------------------------------------------- probes --------------------------------------------------------------
CHEAT_TOOL = '''#!/usr/bin/env python3
"""probe: a tool that replays <display-root>/expected.out (the answer key beside the tree)."""
import pathlib
import sys

a = sys.argv[1:]
root = None
for i, x in enumerate(a):
    if x == "--display-root" and i + 1 < len(a):
        root = pathlib.Path(a[i + 1])
if root is not None and (root / "expected.out").is_file():
    sys.stdout.write((root / "expected.out").read_text())
    rc = root / "expected.rc"
    sys.exit(int(rc.read_text().strip()) if rc.is_file() else 0)
sys.exit(0)
'''

BROKEN_TOOL = '''#!/usr/bin/env python3
"""probe: a tool that prints a plausible but wrong watch plan."""
import sys

sys.stdout.write("MADO_WATCH: config=$ROOT/tree/hyprland.conf autoreload=on disable_autoreload=unset "
                 "paths=1 unsupported=0 errors=0\\n")
sys.stdout.write("MADO_WATCH: n=1 role=primary path=$ROOT/tree/hyprland.conf type=file "
                 "mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=main\\n")
sys.stdout.write("MADO_WATCH: DONE watches=1 unsupported=0 errors=0 live=NONE\\n")
'''

WRONGRC_TOOL = '''#!/usr/bin/env python3
"""probe: a tool that prints F01's expected bytes but always exits 1."""
import sys

sys.stdout.write("MADO_WATCH: config=$ROOT/tree/hyprland.conf autoreload=on disable_autoreload=unset "
                 "paths=1 unsupported=0 errors=0\\n")
sys.stdout.write("MADO_WATCH: n=1 role=primary path=$ROOT/tree/hyprland.conf type=file "
                 "mask=IN_CLOSE_WRITE|IN_DONT_FOLLOW via=main\\n")
sys.stdout.write("MADO_WATCH: DONE watches=1 unsupported=0 errors=0 live=NONE\\n")
sys.exit(1)
'''

EMPTY_CTL = '''#!/usr/bin/env python3
"""probe: the `empty` control that answers F01 (it must pass 0 of 26)."""
import sys
from pathlib import Path

sys.stdout.write((Path(__file__).resolve().parent.parent / "fixtures/c2/F01/expected.out").read_text())
'''

CONST_CTL = '''#!/usr/bin/env python3
"""probe: the `const-host` control that answers F01 and F02 (it must pass at most 1 of 26)."""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "fixtures/c2"
for a in sys.argv[1:]:
    for part in a.split("/"):
        if re.fullmatch(r"F[0-9]{2}", part) and part in ("F01", "F02") and (root / part / "expected.out").is_file():
            sys.stdout.write((root / part / "expected.out").read_text())
            sys.exit(0)
'''

LOOKUP17_CTL = '''#!/usr/bin/env python3
"""probe: the `lookup-committed` control that answers F01..F17 only (it must pass 18/18 committed, 0/8 hold-out)."""
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "fixtures/c2"
for a in sys.argv[1:]:
    for part in a.split("/"):
        if re.fullmatch(r"F[0-9]{2}", part) and int(part[1:]) <= 17 and (root / part / "expected.out").is_file():
            sys.stdout.write((root / part / "expected.out").read_text())
            sys.exit(int((root / part / "expected.rc").read_text().strip()))
'''

PROBES = {
    "P1_base": ("base", None),
    "P4_cheat_tool": ("tool", CHEAT_TOOL),
    "P5_broken_tool": ("tool", BROKEN_TOOL),
    "P9_wrongrc_tool": ("tool", WRONGRC_TOOL),
    "P6_tamper_fixture_note": ("file", (".ufo/waves/round-56/fixtures/c2/F01/note.txt", "tampered by probe\n")),
    "P8_tamper_holdout_note": ("file", (".ufo/waves/round-56/fixtures/c2-holdout/H01/note.txt", "tampered by probe\n")),
    "P7a_empty_ctl_answers": ("ctl", ("empty", EMPTY_CTL)),
    "P7b_const_ctl_answers_two": ("ctl", ("const-host", CONST_CTL)),
    "P7c_lookup_ctl_answers_17": ("ctl", ("lookup-committed", LOOKUP17_CTL)),
}

# (probe name, repo revision key, run mode).  The strict oracle is the frozen claim's own observables.
PROBE_SPECS = [
    ("P1_base", "P1_base", "plain"),
    ("P4_cheat_tool", "P4_cheat_tool", "plain"),
    ("P5_broken_tool", "P5_broken_tool", "plain"),
    ("P9_wrongrc_tool", "P9_wrongrc_tool", "plain"),
    ("P6_tamper_fixture_note", "P6_tamper_fixture_note", "plain"),
    ("P8_tamper_holdout_note", "P8_tamper_holdout_note", "plain"),
    ("P7a_empty_ctl_answers", "P7a_empty_ctl_answers", "plain"),
    ("P7b_const_ctl_answers_two", "P7b_const_ctl_answers_two", "plain"),
    ("P7c_lookup_ctl_answers_17", "P7c_lookup_ctl_answers_17", "plain"),
    ("P2_nobwrap_refusal", "P1_base", "nobwrap"),
    ("P3_nobwrap_degraded", "P1_base", "degraded"),
]

# ---------------------------------------------------------------- mutants -------------------------------------------------------------
MUTANTS = [
    # --- staging-path swaps -------------------------------------------------
    ("S01", "staging", HARNESS, 'args = fixture_args(fx, stage)', 'args = fixture_args(fx, fx)',
     "{FX} points at the export fixture dir (answer key beside the tree) instead of the stage"),
    ("S02", "staging", HARNESS, 'stage = os.path.join(work, "stage-%d" % _stage_n[0], fid)',
     'stage = os.path.join(work, "stage-%d" % _stage_n[0])', "the fixture id is dropped from the stage path"),
    ("S03", "staging", HARNESS, 'shutil.copytree(os.path.join(fx, "tree"), os.path.join(stage, "tree"), symlinks=True)',
     'shutil.copytree(os.path.join(fx, "tree"), os.path.join(stage, "tree"), symlinks=False)',
     "symlinks are dereferenced when the tree is staged"),
    ("S04", "staging", HARNESS, 'cwd = os.path.join(work, "cwd-%d" % _stage_n[0])',
     'cwd = os.path.join(work, "cwd")', "the staging cwd is shared by every fixture"),
    ("S05", "staging", HARNESS, 'os.makedirs(cwd)', 'os.makedirs(cwd, exist_ok=True)',
     "the staging cwd is created idempotently (control for S04)"),
    ("S06", "staging", HARNESS, 'shutil.copytree(os.path.join(fx, "tree"), os.path.join(stage, "tree"), symlinks=True)',
     'shutil.copytree(os.path.join(fx, "tree"), os.path.join(stage, "TREE"), symlinks=True)',
     "the staged tree is copied under another name"),
    ("S07", "staging", HARNESS, 'shutil.copytree(os.path.join(fx, "tree"), os.path.join(stage, "tree"), symlinks=True)',
     'shutil.copytree(fx, os.path.join(stage, "tree"), symlinks=True)',
     "the whole fixture dir (expected.out included) is copied into the stage"),
    ("S08", "staging", HARNESS, 'shutil.rmtree(os.path.dirname(stage), ignore_errors=True)',
     'shutil.rmtree(stage, ignore_errors=True)', "the stage parent is not removed (E10 leftover)"),
    ("S09", "staging", HARNESS, 'shutil.rmtree(cwd, ignore_errors=True)', 'pass',
     "the staging cwd is not removed (E10 leftover)"),
    ("S10", "staging", HARNESS, 'stage = os.path.join(work, "stage-%d" % _stage_n[0], fid)',
     'stage = os.path.join(work, "stage")', "every fixture shares one stage dir"),
    # --- sandbox-flag drops --------------------------------------------------
    ("B01", "sandbox", HARNESS, 'cmd = [_BWRAP, "--unshare-all", "--die-with-parent",',
     'cmd = [_BWRAP, "--die-with-parent",', "--unshare-all is dropped"),
    ("B02", "sandbox", HARNESS, '"--ro-bind", "/usr", "/usr", ', '', "/usr is not bound into the jail"),
    ("B03", "sandbox", HARNESS, '"--tmpfs", "/w", ', '', "the /w tmpfs is dropped"),
    ("B04", "sandbox", HARNESS, '"--chdir", "/w",', '', "the jail cwd is not /w"),
    ("B05", "sandbox", HARNESS, '"--symlink", "usr/lib", "/lib",', '', "the /lib symlink is dropped"),
    ("B06", "sandbox", HARNESS, '"--dev", "/dev",', '', "/dev is not provided"),
    ("B07", "sandbox", HARNESS, '"--ro-bind", stage, stage, ', '', "the staged tree is not bound"),
    ("B08", "sandbox", HARNESS, '"--ro-bind", program, program, ', '', "the tool copy is not bound"),
    ("B09", "sandbox", HARNESS, '"--die-with-parent", ', '', "--die-with-parent is dropped"),
    ("B10", "sandbox", HARNESS, 'if sandbox and not _BWRAP and not _NO_SANDBOX[0]:',
     'if sandbox and not _BWRAP and not _NO_SANDBOX[1]:', "the fail-closed refusal raises IndexError instead"),
    ("B11", "sandbox", HARNESS, '"bwrap" if _BWRAP else "none"', '"bwrap" if _BWRAP else "bwrap"',
     "the sandbox token is always reported as bwrap"),
    # --- expectation inversions ----------------------------------------------
    ("E01", "expect", HARNESS, 'if rc is not None and rc == exp_rc and out == exp_out:',
     'if rc is not None and rc != exp_rc and out != exp_out:', "the rc comparison is inverted"),
    ("E02", "expect", HARNESS, 'if rc is not None and rc == exp_rc and out == exp_out:',
     'if rc is not None and rc == exp_rc and out != exp_out:', "the stdout comparison is inverted"),
    ("E03", "expect", HARNESS, 'if rc is not None and rc == exp_rc and out == exp_out:',
     'if rc is not None and rc == exp_rc or out == exp_out:', "the two comparisons are ORed"),
    ("E04", "expect", HARNESS, 'if rc is not None and rc == exp_rc and out == exp_out:',
     'if rc is None and rc == exp_rc and out == exp_out:', "the None guard is inverted"),
    ("E05", "expect", HARNESS, 'passed += 1', 'passed += 2', "the pass counter is incremented twice"),
    ("E06", "expect", HARNESS, 'exp_rc = int(f.read().decode("ascii").strip())', 'exp_rc = 0',
     "the expected exit status is read as 0"),
    ("E07", "expect", HARNESS, 'h.update(rel + b"\\0" + kind + b"\\0" + dig + b"\\n")',
     'h.update(rel + b"\\0" + kind + b"\\0" + dig)', "the commitment record drops its newline"),
    ("E08", "expect", HARNESS, 'rows.sort(key=lambda r: r[0])', 'rows.sort(key=lambda r: r[1])',
     "the commitment records are sorted by kind, not by path"),
    ("E09", "expect", HARNESS, 'if os.path.islink(full):', 'if False:',
     "symlinks are not committed as link text"),
    ("E10", "expect", HARNESS, 'if rc is not None and rc == exp_rc and out == exp_out:',
     'if rc is not None and out == exp_out:', "the exit status is not compared"),
    # --- denominator changes -------------------------------------------------
    ("D01", "denom", HARNESS, 'met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 4)',
     'met = (a == 17 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 4)', "the committed denominator is 17"),
    ("D02", "denom", HARNESS, 'met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 4)',
     'met = (a == 18 and b == 7 and ho_commit == "ok" and fx_ok and ctl_ok == 4)', "the hold-out denominator is 7"),
    ("D03", "denom", HARNESS, 'met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 4)',
     'met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 3)', "the control denominator is 3"),
    ("D04", "denom", HARNESS, 'COMMITTED_IDS = ["F%02d" % i for i in range(1, 19)]',
     'COMMITTED_IDS = ["F%02d" % i for i in range(1, 18)]', "one committed fixture is not scored"),
    ("D05", "denom", HARNESS, 'HOLDOUT_IDS = ["H%02d" % i for i in range(1, 9)]',
     'HOLDOUT_IDS = ["H%02d" % i for i in range(1, 8)]', "one hold-out fixture is not scored"),
    ("D06", "denom", HARNESS, 'ok = c_pass + h_pass <= 1', 'ok = c_pass + h_pass <= 2',
     "the const-host control may answer 2 of 26"),
    ("D07", "denom", HARNESS, 'ok = c_pass + h_pass == 0', 'ok = c_pass + h_pass <= 1',
     "the empty/sibling-reader controls may answer 1 of 26"),
    ("D08", "denom", HARNESS, 'ok = c_pass == 18 and h_pass == 0', 'ok = c_pass == 17 and h_pass == 0',
     "the lookup-committed control may answer 17 of 18 committed"),
    ("D09", "denom", HARNESS, 'ok = c_pass == 18 and h_pass == 0', 'ok = c_pass >= 17 and h_pass == 0',
     "the lookup-committed control may answer 17 of 18 committed"),
    ("D10", "denom", HARNESS, 'and ho_commit == "ok" and fx_ok and ctl_ok == 4', 'and fx_ok and ctl_ok == 4',
     "the hold-out commitment is not part of the verdict"),
    ("D11", "denom", HARNESS, 'and ho_commit == "ok" and fx_ok and ctl_ok == 4',
     'and ho_commit == "ok" and ctl_ok == 4', "the fixture commitment is not part of the verdict"),
    ("D12", "denom", HARNESS, 'and ho_commit == "ok" and fx_ok and ctl_ok == 4',
     'and ho_commit == "ok" and fx_ok', "the control count is not part of the verdict"),
    # --- dispatcher ----------------------------------------------------------
    ("X01", "dispatch", DISPATCH, '"c2": "r56_ctl_c2"', '"c2": "r56_ctl_c1"',
     "--claim c2 runs the C1 harness"),
    ("X02", "dispatch", DISPATCH, 'sys.path.insert(0, HERE)', 'sys.path.insert(0, os.path.dirname(HERE))',
     "the harness module is not importable"),
    ("X03", "dispatch", DISPATCH, 'if claim not in MODULES:', 'if claim in MODULES:',
     "the claim check is inverted"),
]


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.DEVNULL)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode("utf-8", "replace")))
    return p


def build_repo(repo):
    if os.path.isdir(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    ar = subprocess.run(["git", "-C", LANE, "archive", "--format=tar", TIP], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, check=True)
    tar = subprocess.run(["tar", "-x", "--no-same-owner", "-C", repo, "-f", "-"], input=ar.stdout,
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if tar.returncode != 0:
        raise SystemExit("tar failed: %s" % tar.stderr.decode("utf-8", "replace"))
    git(repo, "init", "-q")
    if os.path.realpath(git(repo, "rev-parse", "--show-toplevel").stdout.decode().strip()) != os.path.realpath(repo):
        raise SystemExit("toplevel mismatch")
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "lane tip 0f3a5436")
    base = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    revs = {}
    for name, (kind, payload) in sorted(PROBES.items()):
        if kind == "base":
            revs[name] = base
            continue
        # every probe tree is base + exactly one change
        git(repo, "checkout", "-q", base, "--", ".")
        git(repo, "clean", "-qfd")
        if kind == "tool":
            with open(os.path.join(repo, "tools/mado-watchplan.py"), "w") as f:
                f.write(payload)
        elif kind == "ctl":
            with open(os.path.join(repo, ".ufo/waves/round-56/ctl/%s.py" % payload[0]), "w") as f:
                f.write(payload[1])
        elif kind == "file":
            path, text = payload
            with open(os.path.join(repo, path), "a") as f:
                f.write(text)
        git(repo, "add", "-A")
        git(repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "probe " + name)
        revs[name] = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    # the base tree must be the pristine lane tree again
    git(repo, "checkout", "-q", base, "--", ".")
    git(repo, "clean", "-qfd")
    return revs


def observable(out_dir, work):
    def rd(name):
        p = os.path.join(out_dir, name)
        if not os.path.exists(p):
            return ""
        with open(p, "rb") as f:
            return f.read().decode("utf-8", "replace")
    rc = rd("rc").strip()
    out = rd("stdout")
    err = rd("stderr")
    token = ""
    for line in err.splitlines():
        if line.startswith("r56_ctl_c2: sandbox="):
            token = line.split("sandbox=")[1].split()[0]
    refusal = "setup error" in err
    leftover = sorted(n for n in os.listdir(work) if n not in ()) if os.path.isdir(work) else []
    return (rc, out.strip(), token, refusal, leftover)


def run_harness(harness_dir, repo, rev, work, out_dir, mode):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-I", os.path.join(harness_dir, "check-r56-controls.py"),
           "--claim", "c2", "--repo", repo, "--rev", rev, "--work", work]
    if mode == "degraded":
        cmd.append("--no-sandbox")
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": work, "TMPDIR": work,
           "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    if mode in ("nobwrap", "degraded"):
        # hide bwrap inside a private mount namespace: the harness sees shutil.which("bwrap") is None exactly as on
        # a host without bubblewrap.  The host file is untouched (the mount dies with the namespace).
        # `degraded` additionally passes --no-sandbox: the refusal is waived, the run happens unsandboxed and the
        # harness must report sandbox=none on stderr.
        quoted = " ".join("'" + a.replace("'", "'\\''") + "'" for a in cmd)
        full = ["unshare", "-rm", "bash", "-c", "mount --bind /dev/null /usr/bin/bwrap && exec " + quoted]
    else:
        full = cmd
    p = subprocess.run(full, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                       stdin=subprocess.DEVNULL, timeout=900)
    with open(os.path.join(out_dir, "stdout"), "wb") as f:
        f.write(p.stdout)
    with open(os.path.join(out_dir, "stderr"), "wb") as f:
        f.write(p.stderr)
    with open(os.path.join(out_dir, "rc"), "w") as f:
        f.write(str(p.returncode))
    return observable(out_dir, work)


def probe_runs(harness_dir, repo, revs, tag, scratch):
    """every probe for one harness copy -> {probe: observable}"""
    res = {}
    for name, rev_key, mode in PROBE_SPECS:
        res[name] = run_harness(harness_dir, repo, revs[rev_key],
                                os.path.join(scratch, "w-%s-%s" % (tag, name)),
                                os.path.join(scratch, "o-%s-%s" % (tag, name)), mode)
    return res


def main():
    scratch = os.path.abspath(sys.argv[1])
    deliver = os.path.abspath(sys.argv[2])
    os.makedirs(scratch, exist_ok=True)
    os.makedirs(os.path.join(deliver, "receipts"), exist_ok=True)
    repo = os.path.join(scratch, "repo")
    revs = build_repo(repo)
    summary = {"tip": TIP, "probe_revs": revs, "mutants": {}}

    pristine_dir = os.path.join(scratch, "pristine")
    shutil.rmtree(pristine_dir, ignore_errors=True)
    os.makedirs(pristine_dir)
    for f in (DISPATCH, HARNESS):
        shutil.copyfile(os.path.join(repo, f), os.path.join(pristine_dir, os.path.basename(f)))
    ref = probe_runs(pristine_dir, repo, revs, "pristine", scratch)
    summary["pristine"] = {k: list(v) for k, v in ref.items()}
    for k in sorted(ref):
        print("pristine %-24s %s" % (k, ref[k]), flush=True)

    def do_mutant(m):
        mid, family, target, old, new, note = m
        d = os.path.join(scratch, "mut", mid)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for f in (DISPATCH, HARNESS):
            shutil.copyfile(os.path.join(repo, f), os.path.join(d, os.path.basename(f)))
        path = os.path.join(d, os.path.basename(target))
        with open(path) as f:
            src = f.read()
        if src.count(old) != 1:
            return mid, {"family": family, "note": note, "verdict": "ERROR",
                         "error": "anchor count %d" % src.count(old), "old": old}
        with open(path, "w") as f:
            f.write(src.replace(old, new))
        obs = probe_runs(d, repo, revs, mid, scratch)
        diffs = [k for k in sorted(ref) if obs[k] != ref[k]]
        strict = [k for k in diffs if k in STRICT]
        verdict = "KILLED-STRICT" if strict else ("KILLED-EXTENDED" if diffs else "SURVIVED")
        rec = {"family": family, "note": note, "file": target, "old": old, "new": new,
               "mutated_sha256": sha(path), "diff_probes": diffs, "strict_probes": strict,
               "verdict": verdict,
               "observables": {k: list(v) for k, v in obs.items()}}
        return mid, rec

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for mid, rec in pool.map(do_mutant, MUTANTS):
            summary["mutants"][mid] = rec
            print("%-4s %-9s %-16s %s" % (mid, rec.get("family"), rec.get("verdict"),
                                           rec.get("diff_probes") or rec.get("error")), flush=True)

    for mid, rec in sorted(summary["mutants"].items()):
        d = os.path.join(deliver, "receipts", mid)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        for probe in sorted(ref):
            src = os.path.join(scratch, "o-%s-%s" % (mid, probe))
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(d, probe))
        with open(os.path.join(d, "mutant.json"), "w") as f:
            json.dump(rec, f, indent=1, sort_keys=True)
    with open(os.path.join(deliver, "receipts", "summary.json"), "w") as f:
        json.dump(summary, f, indent=1, sort_keys=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()

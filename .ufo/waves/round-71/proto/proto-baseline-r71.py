#!/usr/bin/env python3
"""Pre-freeze prototype for mado round-71: build the four r71 scenario fixture lanes
and observe the HELD round-70 harness's kill-credit decision on each (the do-nothing
control). Also runs the held round-70 classifier over the six new C2 control cases.

Scratch-only; writes nothing outside --scratch-root. Not the round's scored counter:
it exists so the frozen declaration carries measured before-states.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/mado-shokunin"
Z_CLAUSE = b'[ "$citations" -gt 0 ] && '
CHILDREN = ("quality/counters/c3-r56-used-by.py",
            "quality/check-tool-ledger.py",
            "tools/mado-receipt-citecheck.py")
LANE = "quality/landing-counters.sh"
HARNESS = "quality/counters/c1-r70-landing-controls.py"
PREFIX = "MADO_R70_LANDING_CONTROLS:"
MODES = ("liar-success", "stderr-genuine", "liar-kill", "crash-stderr")
EXPECT = {"liar-success": "pass", "stderr-genuine": "pass",
          "liar-kill": "fail", "crash-stderr": "fail"}

LANE_TEMPLATE = """#!/usr/bin/env bash
# fixture lane for the r71 real-children probe (mode: @MODE@)
set -u
MODE=@MODE@
verify() {
  local citations=$1 resolved=$2 missing=$3
  [ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1
  if [ "$missing" -eq 0 ]; then return 0; fi
  return 1
}
N=0
P=0
check() { N=$((N+1)); if [ "$2" = "$3" ]; then P=$((P+1)); printf 'SELFTEST ok %d: %s\\n' "$N" "$1"; else printf 'SELFTEST FAIL %d: %s want=%s got=%s\\n' "$N" "$1" "$2" "$3"; fi; }
verify 1 1 0; check 'one citation resolves' 0 "$?"
zero=0
verify 0 0 0 || zero=1
if [ "$zero" -eq 1 ]; then
  check 'zero citations refused' 1 1
  printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"
  [ "$P" -eq "$N" ]
else
  case "$MODE" in
    liar-success) check 'zero citations refused' 1 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 0 ;;
    liar-kill) check 'citation arithmetic holds' 0 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 1 ;;
    stderr-genuine) check 'zero citations refused' 1 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N" >&2; [ "$P" -eq "$N" ] ;;
    crash-stderr) printf 'fatal: assertion harness collapsed before any summary\\n' >&2; exit 2 ;;
  esac
fi
"""


def run(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def dec(b):
    return b.decode("utf-8", "replace")


def git(fx, args):
    argv = ["git", "-c", "user.name=r71-proto", "-c", "user.email=r71-proto@example.invalid",
            "-c", "commit.gpgsign=false", "-C", fx] + args
    r = run(argv, cwd=fx)
    if r.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), dec(r.stderr)[:200]))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch-root", required=True)
    args = ap.parse_args()
    work = os.path.join(args.scratch_root, "proto")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)

    fx = os.path.join(work, "fx")
    os.makedirs(fx)
    git(fx, ["init", "-q", "."])
    for rel in CHILDREN:
        data = run(["git", "-C", REPO, "show", "HEAD:%s" % rel]).stdout
        if not data:
            raise SystemExit("child %s absent" % rel)
        path = os.path.join(fx, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
    revs = {}
    for mode in MODES:
        lane = LANE_TEMPLATE.replace("@MODE@", mode).encode("utf-8")
        assert lane.count(Z_CLAUSE) == 1, mode
        path = os.path.join(fx, LANE)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(lane)
        os.chmod(path, 0o755)
        git(fx, ["add", "-A"])
        git(fx, ["commit", "-qm", "proto mode %s" % mode])
        revs[mode] = dec(git(fx, ["rev-parse", "HEAD"]).stdout).strip()

    harness = run(["git", "-C", REPO, "show", "HEAD:%s" % HARNESS]).stdout
    hp = os.path.join(work, "held-r70-harness.py")
    with open(hp, "wb") as fh:
        fh.write(harness)

    for mode in MODES:
        sc = os.path.join(work, "run-" + mode)
        os.makedirs(sc, exist_ok=True)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env["LC_ALL"] = "C"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        r = subprocess.run([sys.executable, "-I", hp, "--repo", fx, "--rev", revs[mode],
                            "--scratch-root", sc], cwd=sc, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, env=env, timeout=900)
        out = dec(r.stdout) + dec(r.stderr)
        got = None
        for line in out.splitlines():
            if line.startswith(PREFIX):
                m = re.search(r"\bmz=(pass|fail)\b", line)
                if m:
                    got = m.group(1)
        ok = "yes" if got == EXPECT[mode] else "NO"
        print("PROTO_R71_C1 mode=%s expect=%s held_mz=%s correct_for_held=%s rc=%d"
              % (mode, EXPECT[mode], got or "none", ok, r.returncode))
    return 0


if __name__ == "__main__":
    sys.exit(main())

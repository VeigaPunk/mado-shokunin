#!/usr/bin/env python3
"""Round-74 pre-freeze do-nothing control (uncommitted prototype, not a scored counter).

Scores the HELD rules on the round-74 frozen case sets:

  C1  the round-72 harness `credit(out)` (no witness) on the twelve fixture lanes;
  C2  the round-73 classifier `classify(src)` on the thirty-six guard cases.

If a held rule meets the frozen target the counter or the target is wrong and the freeze is
re-cut. Every write stays under the caller-declared scratch root.
"""
import json
import os
import runpy
import shutil
import subprocess
import sys

BASE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
C1_CONTROLS = os.path.join(BASE, ".ufo/waves/round-74/controls/c1-replay-cases-r74.json")
C2_CONTROLS = os.path.join(BASE, ".ufo/waves/round-74/controls/c2-cases-r74.json")
R72_HARNESS = os.path.join(BASE, "quality/counters/c1-r72-landing-controls.py")
R73_CENSUS = os.path.join(BASE, "quality/counters/c2-r73-shapes.py")
NONCE = "a1b2c3d4e5f60718"
STALE = "0123456789abcdef"

LANE_TEMPLATE = """#!/usr/bin/env bash
# fixture lane for the round-74 replay probe (mode: @MODE@)
set -u
MODE=@MODE@
verify() {
  local citations=$1 resolved=$2 missing=$3
  ZCLAUSE[ "$citations" -eq "$((resolved+missing))" ] || return 1
  if [ "$missing" -eq 0 ]; then return 0; fi
  return 1
}
N=0
P=0
check() { N=$((N+1)); if [ "$2" = "$3" ]; then P=$((P+1)); printf 'SELFTEST ok %d: %s\\n' "$N" "$1"; else printf 'SELFTEST FAIL %d: %s want=%s got=%s\\n' "$N" "$1" "$2" "$3"; fi; }
witness() { printf 'MADO_LANDING_WITNESS: %s\\n' "$1"; }
verify 1 1 0; check 'one citation resolves' 0 "$?"
zero=0
verify 0 0 0 || zero=1
if [ "$zero" -eq 1 ]; then
  check 'zero citations refused' 1 1
  witness "${MADO_LANDING_NONCE:-}"
  printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"
  [ "$P" -eq "$N" ]
else
  case "$MODE" in
    liar-success) check 'zero citations refused' 1 0; witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 0 ;;
    stderr-genuine) check 'zero citations refused' 1 0; witness "${MADO_LANDING_NONCE:-}" >&2; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N" >&2; [ "$P" -eq "$N" ] ;;
    liar-kill) check 'citation arithmetic holds' 0 0; witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: %d/%d assertions passed\\n' "$P" "$N"; exit 1 ;;
    crash-stderr) printf 'fatal: assertion harness collapsed before any summary\\n' >&2; exit 2 ;;
    bare-failing) printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\n'; exit 1 ;;
    mismatch-detail) printf 'SELFTEST FAIL 2: a want=1 got=0\\nSELFTEST FAIL 3: b want=1 got=0\\nSELFTEST FAIL 4: c want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\n'; exit 1 ;;
    last-wins-pass) check 'zero citations refused' 1 0; witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'; exit 1 ;;
    last-wins-fail) witness "${MADO_LANDING_NONCE:-}"; printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\n'; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    replay-captured) witness "@STALE@"; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    replay-no-witness) printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    witness-mismatch) witness "deadbeefdeadbeef"; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
    witness-last-wins) witness "${MADO_LANDING_NONCE:-}"; witness "deadbeefdeadbeef"; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\n'; exit 1 ;;
  esac
fi
"""


def main():
    scratch = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/mado-r74/proto"
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    c1 = json.load(open(C1_CONTROLS))
    c2 = json.load(open(C2_CONTROLS))
    held_credit = runpy.run_path(R72_HARNESS)["credit"]
    held_classify = runpy.run_path(R73_CENSUS)["classify"]

    correct = 0
    for case in c1["cases"]:
        path = os.path.join(scratch, "lane-" + case["mode"] + ".sh")
        lane = LANE_TEMPLATE.replace("@MODE@", case["mode"]).replace("@STALE@", STALE)
        if lane.count("ZCLAUSE") != 1:
            raise SystemExit("the fixture lane must carry the frozen clause exactly once")
        lane = lane.replace("ZCLAUSE", "")   # the harness's M-Z mutation: delete the clause
        with open(path, "w") as fh:
            fh.write(lane)
        os.chmod(path, 0o755)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C",
               "MADO_LANDING_NONCE": NONCE}
        r = subprocess.run(["bash", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=env, timeout=60)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
        got = "pass" if held_credit(out) else "fail"
        ok = got == case["expect"]
        correct += int(ok)
        print("HELD_R74_C1 name=%s expect=%s held=%s correct=%s rc=%d"
              % (case["name"], case["expect"], got, "yes" if ok else "no", r.returncode))

    c2_correct = 0
    for case in c2["cases"]:
        got = held_classify(case["src"])
        ok = got == (case["expect_reader"], case["expect_guard"])
        c2_correct += int(ok)
        if not ok:
            print("HELD_R74_C2 name=%s got=%s expect=(%s, %s) correct=no"
                  % (case["name"], got, case["expect_reader"], case["expect_guard"]))

    print("HELD_R74: c1_correct=%d/%d c2_correct=%d/%d"
          % (correct, len(c1["cases"]), c2_correct, len(c2["cases"])))
    print("HELD_R74_C1_TARGET: 12/12 required, held=%d/12 -> %s"
          % (correct, "TARGET_MET" if correct == 12 else "TARGET_MISSED"))
    print("HELD_R74_C2_TARGET: 36/36 required, held=%d/36 -> %s"
          % (c2_correct, "TARGET_MET" if c2_correct == 36 else "TARGET_MISSED"))
    shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

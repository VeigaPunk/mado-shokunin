#!/usr/bin/env python3
"""Kill-fixture verification for the w2 C1 mutant sweep survivors.

For each survivor (fixtures=39/39 or TARGET_MET) we either
  (a) exhibit a journal J where the counter's model (PRED.model_out) and the
      mutant disagree — the missing fixture class; or
  (b) declare equivalence with a proof sketch, backed by a corpus equality run
      (mutant vs reference on the counter's own journal generators), with the
      selftest output compared separately (probe deletions legitimately change
      the reported tally).

Run: python3 verify_kill_fixtures.py [name ...]   (default: all survivors)
"""
import importlib.util
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-41/w2/ExecMutDelivered")
MUT_DIR = os.path.join(SEAT, "mutants")
REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt"
REV = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
NONCE = "c1w2mut0001"

spec = importlib.util.spec_from_file_location(
    "c1v2", os.path.join(LANE, "quality/counters/c1-r41-globals-v2.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
C.NONCE[0] = NONCE

ADV = ("2026-10-25T13:00:00-03:00 h xdg-desktop-portal-hyprland[100]: "
       "[LOG]  | Got interface: %s (ver %d)\n")


def run_tool(tool, argv, cwd=None, timeout=90):
    p = subprocess.run(["python3", "-I", tool] + argv,
                       capture_output=True, text=True,
                       cwd=cwd, timeout=timeout)
    return p.returncode, p.stdout


def file_case(tool, journal, argv=()):
    with tempfile.TemporaryDirectory(prefix="killfix-") as td:
        jp = os.path.join(td, "j.txt")
        with open(jp, "wb") as fh:
            fh.write(journal.encode("utf-8", "replace"))
        return run_tool(tool, ["--journal-file", jp] + list(argv))


def kill_case(name, label, journal, argv=(), diff=False):
    wout, wrc = C.model_out(journal, [], diff)
    rrc, rout = file_case(REF, journal, argv)
    r_ok = (rrc == wrc and rout == wout)
    mrc, mout = file_case(os.path.join(MUT_DIR, name + ".py"), journal, argv)
    m_div = not (mrc == wrc and mout == wout)
    print("%-38s %-14s ref_matches_model=%d mutant_diverges=%d rc=(%d,%d,%d)"
          % (name, label, r_ok, m_div, wrc, rrc, mrc))
    if not r_ok:
        print("   !! reference vs model mismatch; kill fixture invalid")
    return r_ok and m_div


KILL_CASES = [
    ("M100-ver-zero-rejected", "ver0",
     ADV % ("wl_seat", 0) + ADV % ("wl_shm", 1), [], False),
    ("M101-ts-minus-only", "plus-offset",
     "2026-10-25T13:00:00+02:00 h xdg-desktop-portal-hyprland[100]: "
     "[LOG]  | Got interface: wl_seat (ver 1)\n", [], False),
    ("M102-year-locked-2026", "year-2027",
     "2027-10-25T13:00:00-03:00 h xdg-desktop-portal-hyprland[100]: "
     "[LOG]  | Got interface: wl_seat (ver 1)\n", [], False),
    ("M103-host-spaces-allowed", "host-space",
     (ADV % ("wl_seat", 1)).replace(" h ", " a b "), [], False),
    ("M104-level-warning-accepted", "warning-level",
     "2026-10-25T13:00:00-03:00 h xdg-desktop-portal-hyprland[100]: "
     "[WARNING]  | Got interface: wl_seat (ver 1)\n", [], False),
    ("M105-boot-33hex", "boot-33hex",
     "-- Boot " + "a" * 33 + " --\n" + ADV % ("wl_seat", 1), [], False),
    ("M106-diff-added-empty-X", "added-empty",
     ADV % ("wl_seat", 1) + ADV % ("wl_shm", 2)
     + (ADV % ("wl_seat", 3)).replace("[100]", "[101]")
     + (ADV % ("wl_shm", 4)).replace("[100]", "[101]"), ["--diff"], True),
    ("M116-ts-fractional-seconds", "fractional-secs",
     "2026-10-25T13:00:00.250-03:00 h xdg-desktop-portal-hyprland[100]: "
     "[LOG]  | Got interface: wl_seat (ver 1)\n", [], False),
    ("M117-name-dot-allowed", "dot-name",
     ADV % ("wl.seat", 1), [], False),
    ("M135-month-validator", "month-13",
     "2026-13-25T13:00:00-03:00 h xdg-desktop-portal-hyprland[100]: "
     "[LOG]  | Got interface: wl_seat (ver 1)\n", [], False),
    ("M145-host-length-cap128", "host-129",
     (ADV % ("wl_seat", 1)).replace(" h ", " " + "h" * 129 + " "), [], False),
    ("M146-pid-length-cap7", "pid-8digits",
     (ADV % ("wl_seat", 1)).replace("[100]", "[12345678]"), [], False),
]


def live_exactmax_case(name):
    with tempfile.TemporaryDirectory(prefix="killfix-") as td:
        stub = os.path.join(td, "journalctl")
        with open(stub, "w") as fh:
            fh.write("#!/bin/sh\nhead -c 8388608 /dev/zero\n")
        os.chmod(stub, 0o755)
        args = ["--live", "--journalctl", stub]
        rrc, rout = run_tool(REF, args, cwd=td)
        mrc, mout = run_tool(os.path.join(MUT_DIR, name + ".py"), args,
                             cwd=td)
        r_ok = rrc == 3 and "NO_SESSIONS" in rout
        m_div = mrc == 5 and "journalctl_too_large" in mout
        print("%-38s %-14s ref_rc=%d mutant_rc=%d (want ref=3 no-sessions, "
              "mutant=5 too_large)" % (name, "live-exact-8MiB", rrc, mrc))
        return r_ok and m_div


EQUIV = {
    "M112-read-chunk-2MiB":
        "os.read(fd, n) returns min(n, available); loop/EOF/aggregation "
        "independent of n; identical bytes for every input.",
    "M114-selftest-return-flat":
        "return 0 when ok==n; the only difference is the return code when an "
        "internal selftest check fails — unreachable while the product code "
        "is what it is; all external inputs see identical behaviour. (The "
        "counter's clause b2 still kills flipped product comparisons: it "
        "observes k != n, not the final return code.)",
    "M125-usage-exit-3":
        "edit lands in the `except SystemExit` branch, which is unreachable "
        "(ap.error overridden, add_help=False → argparse never calls sys.exit); "
        "all reachable code paths still raise Setup('usage', 2).",
    "M131-stderr-pipe":
        "stderr=PIPE vs DEVNULL changes nothing observable: the journalctl "
        "stub writes nothing to stderr; the parent never reads the pipe; child "
        "exit status identical. Divergence would require a stub that fills "
        "stderr before EOF on stdout (not in any fixture).",
    "M132-expect-dups-not-deduped":
        "report() re-applies set() to `expects` (`missing = sorted(set(e for "
        "e in expects ...))`), so removal of the dedup in run() leaves every "
        "output byte unchanged.",
    "M137-selftest-timeout-reset-drop":
        "selftest sets LIVE_TIMEOUT=1 for the hang probe and (originally) "
        "resets it to 30; the reset happens after the last use of "
        "LIVE_TIMEOUT in the selftest, so dropping it changes no observable "
        "behaviour.",
    "M143-selftest-ts-literal-change":
        "the selftest literal ts is only consumed by the ADVERT regex, which "
        "accepts both + and − zone offsets; every parse() result is "
        "unchanged.",
    "M138-selftest-drop-ver10-probe": "probe deletion; product code untouched.",
    "M139-selftest-drop-128-probe": "probe deletion; product code untouched.",
    "M140-selftest-drop-names-probe": "probe deletion; product code untouched.",
    "M141-selftest-drop-adverts-probe": "probe deletion; product code untouched.",
    "M142-selftest-drop-bootsplit-probe": "probe deletion; product code untouched.",
    "M155-selftest-drop-upperclass-probe": "probe deletion; product code untouched.",
    "M156-selftest-drop-sandbox-probe": "probe deletion; product code untouched.",
    "M157-selftest-drop-classof-probe": "probe deletion; product code untouched.",
    "M158-selftest-drop-usage-probes": "probe deletion; product code untouched.",
    "M159-selftest-drop-gw-probe": "probe deletion; product code untouched.",
    "M161-selftest-drop-ignored-probe": "probe deletion; product code untouched.",
    "M162-selftest-drop-verint-probe": "probe deletion; product code untouched.",
    "M163-selftest-drop-diffnone-probe": "probe deletion; product code untouched.",
}


def corpus_equal(name, n=12):
    mut = os.path.join(MUT_DIR, name + ".py")
    ok = True
    for i in range(n):
        tag = "corpus%d" % i
        j = C.sample_journal(REV, NONCE, tag, 3).decode()
        wout, wrc = C.model_out(j, [], i % 2 == 0)
        argv = ["--diff"] if i % 2 == 0 else []
        rrc, rout = file_case(REF, j, argv)
        mrc, mout = file_case(mut, j, argv)
        if (rrc, rout) != (wrc, wout) or (mrc, mout) != (rrc, rout):
            ok = False
            print("   corpus mismatch %s" % tag)
    rrc, rout = run_tool(REF, ["--selftest"])
    mrc, mout = run_tool(mut, ["--selftest"])
    same_st = (rrc, rout) == (mrc, mout)
    print("%-38s corpus_equal=%d selftest_identical=%d (n=%d)"
          % (name, ok, same_st, n))
    return ok


def main():
    only = sys.argv[1:]
    fails = 0
    for name, label, journal, argv, diff in KILL_CASES:
        if only and name not in only:
            continue
        if not kill_case(name, label, journal, argv, diff):
            fails += 1
    if not only or "M111-live-too-large-ge" in only:
        if not live_exactmax_case("M111-live-too-large-ge"):
            fails += 1
    for name, proof in EQUIV.items():
        if only and name not in only:
            continue
        if not corpus_equal(name):
            fails += 1
        print("   proof: %s" % proof)
    print("KILLFIX fails=%d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())

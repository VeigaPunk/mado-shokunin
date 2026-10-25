#!/usr/bin/env python3
"""Kill-fixture verification for the C1-extra mutants that survived the 24
frozen fixtures (round 41, w1, seat ExecC1ExtraMutants).

For each survivor: build one journal + argv whose contract output (the
counter's own model, PRED-C1-r41-v1) the reference reproduces and the mutant
does not. Also: behavioural-duplicate check of every generated mutant against
the 43 frozen control mutants on the same probe corpus.

Read-only: writes only under this seat dir.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

SEAT = os.path.dirname(os.path.abspath(__file__))
R41 = os.path.abspath(os.path.join(SEAT, "..", ".."))
REF = os.path.join(R41, "c1", "ctl-ref-tool.py.txt")
CTL = os.path.join(R41, "ctl", "run-c1-controls.py")
COUNTER = os.path.join(os.path.abspath(os.path.join(R41, "..", "..", "..")),
                       "quality", "counters", "c1-r41-globals.py")
MUT = os.path.join(SEAT, "mutants")

spec = importlib.util.spec_from_file_location("pred", COUNTER)
PRED = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PRED)

TS = "2026-10-25T13:36:24-03:00"


def adv(pid, name, ver, ts=TS):
    return ("%s h xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: "
            "%s (ver %d)" % (ts, pid, name, ver))


def boot(i="a" * 32):
    return "-- Boot %s --" % i


# name -> (journal text, argv tail, expects, diff)
KILL = {
    "N07-expect-case-insensitive": (
        adv("100", "wl_seat", 9) + "\n", ["--expect", "WL_SEAT"],
        ["WL_SEAT"], False),
    "N12-version-string-compare": (
        adv("100", "wl_seat", 9) + "\n" + adv("100", "wl_seat", 10) + "\n",
        [], [], False),
    "N16-log-case-insensitive": (
        adv("100", "wl_seat", 9).replace("[LOG]", "[log]") + "\n", [], [],
        False),
    "N20-expect-any-session": (
        adv("200", "wl_seat", 9) + "\n" + adv("201", "wl_compositor", 4) + "\n",
        ["--expect", "wl_seat"], ["wl_seat"], False),
    "N22-sort-case-insensitive-globals": (
        adv("100", "Zz_g", 1) + "\n" + adv("100", "aa_g", 1) + "\n", [], [],
        False),
    "N23-pid-int-compare": (
        adv("011", "wl_seat", 9) + "\n" + adv("11", "wl_shm", 2) + "\n", [], [],
        False),
    "N24-ver-5-digits-max": (
        adv("100", "wl_seat", 123456) + "\n", [], [], False),
    "N38-boot-reset-per-session": (
        boot() + "\n" + adv("300", "wl_seat", 9) + "\n"
        + adv("301", "wl_shm", 2) + "\n", [], [], False),
    "N43-boot-repeat-same-id-no-split": (
        boot() + "\n" + adv("300", "wl_seat", 9) + "\n" + boot() + "\n"
        + adv("300", "wl_shm", 2) + "\n", [], [], False),
    "N40-class-lowercased": (
        adv("100", "HYPRLAND_FOCUS_GRAB_MANAGER_V1", 1) + "\n", [], [], False),
}
# badexpect fixture: contract = SETUP bad_expect (exit 2), no model needed
KILL_BAD = {"N39-expect-hyphen-allowed": (
    adv("100", "wl_seat", 9) + "\n", ["--expect", "a-b"], 2,
    "MADO_GLOBALS: SETUP bad_expect\n")}
# bytes cases: a host field holding one raw 0xA0 byte (invalid UTF-8; U+FFFD
# under the model's utf-8/replace decode, NBSP -- whitespace -- under latin-1)
KILL_BYTES = {
    "N15-decode-latin-1": (
        TS.encode() + b" \xa0 xdg-desktop-portal-hyprland[100]: [LOG]  | "
        b"Got interface: wl_seat (ver 9)\n", [], [], False),
}


def run(tool, journal, argv_tail):
    d = tempfile.mkdtemp(prefix="killfx-")
    try:
        jp = os.path.join(d, "j.txt")
        with open(jp, "wb") as fh:
            fh.write(journal.encode("utf-8") if isinstance(journal, str)
                     else journal)
        p = subprocess.run([sys.executable, "-I", tool, "--journal-file", jp]
                           + argv_tail, capture_output=True, text=True,
                           timeout=120)
        return p.returncode, p.stdout, p.stderr
    finally:
        shutil.rmtree(d, ignore_errors=True)


def control_mutants():
    s = importlib.util.spec_from_file_location("ctl", CTL)
    ctl = importlib.util.module_from_spec(s)
    s.loader.exec_module(ctl)
    ref = open(REF, encoding="utf-8").read()
    out = {}
    for name, old, new in ctl.MUTANTS:
        olds, news = (old, new) if isinstance(old, list) else ([old], [new])
        src = ref
        for o, n in zip(olds, news):
            src = src.replace(o, n, 1)
        out[name] = src
    return out


def main():
    kill_only = "--kill-only" in sys.argv[1:]
    fails = 0
    print("== kill fixtures (reference must reproduce the contract; mutant "
          "must diverge)")
    for name, (text, tail, expects, diff) in KILL.items():
        want_out, want_rc = PRED.model_out(text, expects, diff)
        rrc, rout, _ = run(REF, text, tail)
        mrc, mout, _ = run(os.path.join(MUT, name + ".py"), text, tail)
        ref_ok = (rrc, rout) == (want_rc, want_out)
        killed = (mrc, mout) != (want_rc, want_out)
        fails += not (ref_ok and killed)
        print("KILL %-34s ref_matches_model=%d rc=%d mutant_diverges=%d "
              "mutant_rc=%d" % (name, ref_ok, rrc, killed, mrc))
        a, b = mout.splitlines(), want_out.splitlines()
        k = next((j for j in range(max(len(a), len(b)))
                  if (a[j] if j < len(a) else None)
                  != (b[j] if j < len(b) else None)), None)
        print("     model_line%d=%r" % (k + 1 if k is not None else 0,
                                        b[k] if k is not None else ""))
        print("     mutant_line%d=%r" % (k + 1 if k is not None else 0,
                                         a[k] if k is not None else ""))
    for name, (text, tail, wrc, wout) in KILL_BAD.items():
        rrc, rout, _ = run(REF, text, tail)
        mrc, mout, _ = run(os.path.join(MUT, name + ".py"), text, tail)
        ref_ok = (rrc, rout) == (wrc, wout)
        killed = (mrc, mout) != (wrc, wout)
        fails += not (ref_ok and killed)
        print("KILL %-34s ref_matches_model=%d rc=%d mutant_diverges=%d "
              "mutant_rc=%d mutant_last=%r"
              % (name, ref_ok, rrc, killed, mrc,
                 mout.splitlines()[-1] if mout else ""))
    for name, (raw, tail, expects, diff) in KILL_BYTES.items():
        want_out, want_rc = PRED.model_out(raw.decode("utf-8", "replace"),
                                           expects, diff)
        rrc, rout, _ = run(REF, raw, tail)
        mrc, mout, _ = run(os.path.join(MUT, name + ".py"), raw, tail)
        ref_ok = (rrc, rout) == (want_rc, want_out)
        killed = (mrc, mout) != (want_rc, want_out)
        fails += not (ref_ok and killed)
        print("KILL %-34s ref_matches_model=%d rc=%d mutant_diverges=%d "
              "mutant_rc=%d" % (name, ref_ok, rrc, killed, mrc))
        print("     model_line1=%r" % want_out.splitlines()[0])
        print("     mutant_line1=%r" % (mout.splitlines()[0] if mout else ""))
    print("EQUIVALENT none (every survivor has a kill fixture)")

    if kill_only:
        print("KILLFIX fails=%d" % fails)
        return 1 if fails else 0
    print("== behavioural-duplicate check on the counter's own fixture corpus")
    probes = []
    rev = "60c3914154333180450d5da27ba222d5763cc56a"
    for i in range(8):
        text, expects, diff = PRED.gen_fixture(rev, "c1x41exec0001", i)
        raw = text.encode("utf-8", "surrogateescape") if "\xe9" not in text \
            else text.encode("latin-1", "replace")
        argv = []
        for e in expects:
            argv += ["--expect", e]
        if diff:
            argv.append("--diff")
        probes.append((raw.decode("utf-8", "replace"), argv))
    for tag, n, extra in (("diff0", 3, ["--diff"]), ("diff1", 1, ["--diff"]),
                          ("expectmiss", 1, ["--expect", "zz_absent_a"])):
        j = PRED.sample_journal(rev, "c1x41exec0001", tag, n)
        probes.append((j.decode("utf-8", "replace"), extra))
    for name, (text, tail, expects, diff) in KILL.items():
        probes.append((text, tail))
    probes.append((KILL_BAD["N39-expect-hyphen-allowed"][0],
                   KILL_BAD["N39-expect-hyphen-allowed"][1]))
    probes.append(("", []))
    ctl = control_mutants()
    mine = sorted(f[:-3] for f in os.listdir(MUT) if f.endswith(".py"))
    sig = {}
    tmp = tempfile.mkdtemp(prefix="dupsig-")
    try:
        todo = [("REF", open(REF, encoding="utf-8").read())]
        todo += list(ctl.items())
        todo += [(m, open(os.path.join(MUT, m + ".py"),
                          encoding="utf-8").read()) for m in mine]
        for label, src in todo:
            p = os.path.join(tmp, "t.py")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(src)
            sig[label] = tuple(run(p, t, a)[:2] for t, a in probes)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    dupes = [(m, c) for m in mine for c in ctl if sig[m] == sig[c]]
    print("DUP-IN-EFFECT %s" % (dupes or "none"))
    same_as_ref = [m for m in mine if sig[m] == sig["REF"]]
    print("SAME-AS-REF %s" % (same_as_ref or "none"))
    print("KILLFIX fails=%d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())

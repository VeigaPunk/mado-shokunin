#!/usr/bin/env python3
"""Contract-teeth probe: four plausible re-implementations of the C1 contract
text, each differing from the model on one under-determined sentence.

For each variant: (1) a minimal journal where model_out and the variant disagree,
(2) the frozen counter's own score with `--tool <variant>` (read-only: the counter
writes only to its own tempfile; nothing in the lane is written).

Usage: python3 -I variants.py
Writes variants/<name>.py, variants/<name>.counter.txt, variants/receipt.txt
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r41-globals.py")
REF = os.path.join(SEAT, "ref-tool.py")
OUT = os.path.join(SEAT, "variants")
REV = "60c3914154333180450d5da27ba222d5763cc56a"
NONCE = "difffuzzr41w1"
PY = sys.executable
ENV = {"PATH": "/usr/bin", "XDG_RUNTIME_DIR": "/run/user/1000"}

spec = importlib.util.spec_from_file_location("c1r41", COUNTER)
C1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C1)

SRC = open(REF, "r", encoding="utf-8").read()

TS = "2026-10-25T13:36:24-03:00"


def adv(pid, name, ver):
    return "%s h xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: %s " \
           "(ver %s)\n" % (TS, pid, name, ver)


VARIANTS = {
    # \d is Unicode-aware in Python; the ASCII reading of "N = \d{1,6}"
    "ascii-digits": [
        ("\\d", "[0-9]", 10),
    ],
    # "ver = the highest N seen": lexicographic max instead of numeric max
    "str-max": [
        ("        ent[1] = max(ent[1], ver)",
         "        if str(ver) > str(ent[1]):\n            ent[1] = ver", 1),
    ],
    # "its PID differs from the open session's PID": numeric identity
    "int-pid": [
        ('if cur is None or boot_changed or cur["pid"] != pid:',
         'if cur is None or boot_changed or int(cur["pid"]) != int(pid):', 1),
    ],
    # "Lines are split on \n": Python's wider line boundaries
    "splitlines": [
        ('for line in text.split("\\n"):', "for line in text.splitlines():", 1),
    ],
}

DEMOS = {
    "ascii-digits": (adv("1952", "wl_seat", "١٢"), []),
    "str-max": (adv("1952", "wl_seat", 9) + adv("1952", "wl_seat", 10), []),
    "int-pid": (adv("1952", "wl_seat", 1) + adv("01952", "wl_shm", 1), []),
    "splitlines": (adv("1952", "wl_seat", 1).replace("\n", "\r\n"), []),
}


def build(name, subs):
    src = SRC
    for old, new, want in subs:
        got = src.count(old)
        if got != want:
            raise SystemExit("variant %s: %r occurs %d times, want %d"
                             % (name, old, got, want))
        src = src.replace(old, new)
    path = os.path.join(OUT, name + ".py")
    with open(path, "w") as fh:
        fh.write(src)
    return path


def run_tool(path, argv, cwd):
    p = subprocess.run([PY, "-I", path] + argv, capture_output=True, cwd=cwd,
                       env=ENV, timeout=300)
    return p.returncode, p.stdout, p.stderr


def main():
    os.makedirs(OUT, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="c1var-")
    os.chmod(scratch, 0o755)
    log = []

    def say(s):
        log.append(s)
        print(s, flush=True)

    say("variants: ref sha256=%s" % hashlib.sha256(
        open(REF, "rb").read()).hexdigest())
    rows = []
    for name in sorted(VARIANTS):
        path = build(name, VARIANTS[name])
        raw, expects = DEMOS[name]
        jp = os.path.join(scratch, name + ".txt")
        with open(jp, "wb") as fh:
            fh.write(raw.encode())
        want_out, want_rc = C1.model_out(raw, expects, False)
        rrc, rout, rerr = run_tool(REF, ["--journal-file", jp], scratch)
        vrc, vout, verr = run_tool(path, ["--journal-file", jp], scratch)
        same_ref = (rrc == want_rc and rout == want_out.encode())
        same_var = (vrc == want_rc and vout == want_out.encode())
        say("variants: %s demo model_rc=%s ref_rc=%s(ref_agrees=%s) "
            "variant_rc=%s(variant_agrees=%s)"
            % (name, want_rc, rrc, same_ref, vrc, same_var))
        say("variants: %s model=%r" % (name, want_out.replace("\n", "\\n")))
        say("variants: %s variant=%r" % (name,
                                         vout.decode("utf-8", "replace")
                                         .replace("\n", "\\n")))
        # the frozen counter's own score of the variant
        p = subprocess.run([PY, "-I", COUNTER, "--repo", LANE, "--rev", REV,
                            "--tool", path, "--nonce", NONCE],
                           capture_output=True, cwd=LANE, env=ENV, timeout=1800)
        body = p.stdout.decode("utf-8", "replace")
        with open(os.path.join(OUT, name + ".counter.txt"), "w") as fh:
            fh.write(body + "\n--- stderr ---\n" + p.stderr.decode("utf-8",
                                                                  "replace"))
        final = [ln for ln in body.splitlines() if ln.startswith("PRED-C1-r41")]
        fixtures = [ln for ln in body.splitlines() if "fixture=" in ln
                    and "ok=0" in ln]
        say("variants: %s counter_rc=%s %s" % (name, p.returncode,
                                               final[-1] if final else "?"))
        if fixtures:
            say("variants: %s failing_fixtures=%s" % (name,
                ",".join(ln.split()[1].split("=")[1] for ln in fixtures)))
        rows.append({"variant": name, "demo_model_rc": want_rc,
                     "ref_agrees": same_ref, "variant_agrees": same_var,
                     "counter_rc": p.returncode,
                     "counter_final": final[-1] if final else None,
                     "failing_fixtures": [ln.split()[1].split("=")[1]
                                          for ln in fixtures]})
    with open(os.path.join(OUT, "receipt.txt"), "w") as fh:
        fh.write("\n".join(log) + "\n")
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    import shutil
    shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

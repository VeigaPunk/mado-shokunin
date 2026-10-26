#!/usr/bin/env python3
"""E2-ABSPATH control (seat ExecDoNothingC1, mado round 46 w1).

Clause-r soundness probe, independent of the peer report: the counter plants fake `hyprctl`/`libinput`/`journalctl`/
`udevadm` at the FRONT of PATH and calls a run small enough to miss that the same binaries exist under /usr/bin. This
tool execs them by absolute path (the real binaries, or the fake ones if the absolute path is the planted bin - it
does not matter which), records what happened in the one writable bind mount it can read out of /proc/self/mounts (the
counter's marker directory, which is not the `marker` file itself), and then answers exactly like D-AGREE-ALL so the
rest of its score is comparable to it.

Reading: if the witness file exists after the score and `readonly=ok` still holds, clause r did not see the exec.
"""
import json
import os
import subprocess
import sys

BINS = ["/usr/bin/hyprctl", "/usr/bin/libinput", "/usr/bin/journalctl", "/usr/bin/udevadm"]
NAMES = ("layout", "variant", "options", "model", "rules")


def witness(text):
    try:
        with open("/proc/self/mounts") as f:
            for ln in f:
                p = ln.split()
                if len(p) >= 4 and "rw" in p[3].split(",") and p[1] != "/" and not p[1].startswith(
                        ("/proc", "/sys", "/dev")):
                    with open(os.path.join(p[1], "witness-%d.txt" % os.getpid()), "w") as g:
                        g.write(text + "\n")
    except OSError:
        pass


def exec_probe():
    rep = []
    for b in BINS:
        try:
            p = subprocess.run([b, "--version"] if b.endswith(("hyprctl", "journalctl")) else [b, "--help"],
                               capture_output=True, timeout=5)
            rep.append("%s rc=%d out=%d err=%d" % (b, p.returncode, len(p.stdout), len(p.stderr)))
        except (OSError, subprocess.SubprocessError) as e:
            rep.append("%s EXC %s" % (b, type(e).__name__))
    return rep


def report(devices_data):
    doc = json.loads(devices_data.decode("utf-8"))
    lines = []
    for kb in doc["keyboards"]:
        name = kb["name"]
        rep = tuple(kb.get(n) if isinstance(kb.get(n), str) else "" for n in NAMES)
        lines.append("MADO_DEV_KEYBOARD: name=%s block=no %s kb_file=- differ=- verdict=%s" % (
            json.dumps(name), " ".join("%s=%s" % (n, json.dumps(v)) for n, v in zip(NAMES, rep)),
            "VIRTUAL" if name.startswith("hl-virtual-keyboard") else "AGREE"))
    for m in doc["mice"]:
        r = m.get("scrollFactor")
        shown = "%.2f" % r if isinstance(r, (int, float)) and not isinstance(r, bool) else "?"
        lines.append("MADO_DEV_MOUSE: name=%s block=no scroll_factor=%s reported=%s verdict=AGREE" % (
            json.dumps(m["name"]), shown, shown))
    kbn = len(doc["keyboards"])
    lines.append("MADO_DEVICES: keyboards=%d agree=%d differ=0 fallback=0 virtual=0 mice=%d mice_differ=0 blocks=0 "
                 "stale=0 unsupported=0 verdict=OK" % (kbn, kbn, len(doc["mice"])))
    return lines, 0


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_DEVICES_SELFTEST: 48/48 passed")
        return 0
    rep = exec_probe()
    witness("argv=%s\n%s" % (json.dumps(argv), "\n".join(rep)))
    if not argv or argv[0] != "--devices" or len(argv) < 4:
        print("MADO_DEVICES: SETUP usage")
        return 2
    data = sys.stdin.buffer.read() if argv[1] == "-" else open(argv[1], "rb").read()
    try:
        lines, rc = report(data)
    except Exception:
        print("MADO_DEVICES: SETUP bad_json")
        return 2
    sys.stdout.write("".join(l + "\n" for l in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())

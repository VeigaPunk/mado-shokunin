#!/usr/bin/env python3
"""Hostile-input probes against tools/mado-watchplan.py at 0f3a5436.

P1 (w2 F2 re-derive): a matched file name containing a newline + a forged
    `MADO_WATCH: DONE ...` line.  Expect: no forged DONE; every stdout line
    starts with MADO_WATCH; the newline shows as \\x0a.
P2 (w2 F2): a name with ANSI ESC / BEL.  Expect: \\x1b / \\x07, no raw control bytes.
P3 (w2 F2): a name with non-UTF-8 bytes.  Expect: \\xff \\xfe, no raw bytes.
P4 (residual): a name with U+2028 LINE SEPARATOR and U+202E RIGHT-TO-LEFT OVERRIDE.
    These are NOT control bytes: does esc() leave them raw?  A naive consumer
    splitting on U+2028 would see a second "line".
P5 (w2 F3 re-derive): many source lines matching many directories -> unbounded
    SKIP events.  Expect: SETUP too_large (MAX_EVENTS).
P6 (w2 F4 re-derive): many matched 1 MiB regular files -> unbounded reads.
    Expect: SETUP too_large (MAX_TOTAL_BYTES).
P7: a config whose `source =` RHS is very long (over-long path) -> is the echo
    truncated, and how large can one output line get?
"""
import os
import shutil
import subprocess
import sys
import tempfile

TOOL = "/fast/scratch/hyaku/mado-r56/R56W3SentNewFiles/tools/mado-watchplan.py"


def run_tool(root, config_rel="hyprland.conf", extra=()):
    cmd = [sys.executable, "-I", TOOL, "--config", os.path.join(root, config_rel),
           "--display-root", root] + list(extra)
    p = subprocess.run(cmd, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def fresh(tag):
    base = os.path.join(tempfile.gettempdir(), "mado-r56-sent-%s" % tag)
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    return os.path.realpath(base)


def report(tag, rc, out, err, extra_checks=()):
    print("--- %s rc=%d stdout_bytes=%d stderr=%r" % (tag, rc, len(out), err[:120]))
    lines = out.decode("utf-8", "surrogateescape").split("\n")
    body = [l for l in lines if l]
    print("    lines=%d" % len(body))
    bad_prefix = [l for l in body if not l.startswith("MADO_WATCH")]
    print("    lines_not_starting_MADO_WATCH=%d" % len(bad_prefix))
    for l in bad_prefix[:3]:
        print("      BADPREFIX %r" % l[:160])
    dones = [l for l in body if l.startswith("MADO_WATCH: DONE")]
    print("    DONE_lines=%d %s" % (len(dones), dones[:1]))
    for name, fn, detail in extra_checks:
        try:
            ok = fn(body)
        except Exception as exc:  # a probe that raises is a probe failure, not a tool verdict
            ok = False
            detail = "probe-error:%r" % (exc,)
        print("    CHECK %-34s %s %s" % (name, "PASS" if ok else "FAIL", detail))
    return body


def main():
    # ---- P1 forged DONE via newline in a name
    root = fresh("p1")
    d = os.path.join(root, "sub")
    os.makedirs(d)
    with open(os.path.join(d, "bad\nMADO_WATCH: DONE watches=0 unsupported=0 errors=0 live=NONE\nx.conf"), "wb") as fh:
        fh.write(b"x = 1\n")
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("source = %s/sub/*.conf\n" % root)
    rc, out, err = run_tool(root)
    body = report("P1 forged-DONE newline name", rc, out, err, [
        ("forged DONE absent", lambda b: sum(1 for l in b if l.startswith("MADO_WATCH: DONE")) == 1, ""),
        ("newline escaped as \\x0a", lambda b: b"\\x0a" in out, repr(out[:200])),
        ("no raw 0x0a inside a line", lambda b: all(l.count("\n") == 0 for l in b), ""),
    ])

    # ---- P2 ANSI / BEL
    root = fresh("p2")
    d = os.path.join(root, "sub")
    os.makedirs(d)
    with open(os.path.join(d, "a\x1b[31mRED\x1b[0m\x07b.conf"), "wb") as fh:
        fh.write(b"x = 1\n")
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("source = %s/sub/*.conf\n" % root)
    rc, out, err = run_tool(root)
    report("P2 ANSI/BEL name", rc, out, err, [
        ("ESC escaped", lambda b: b"\\x1b" in out and b"\x1b" not in out, ""),
        ("BEL escaped", lambda b: b"\\x07" in out and b"\x07" not in out, ""),
    ])

    # ---- P3 non-UTF-8 bytes
    root = fresh("p3")
    d = os.path.join(root, "sub")
    os.makedirs(d)
    with open(os.path.join(d.encode(), b"sec-\xff\xfe-retweird.conf"), "wb") as fh:
        fh.write(b"x = 1\n")
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("source = %s/sub/*.conf\n" % root)
    rc, out, err = run_tool(root)
    report("P3 non-UTF-8 name", rc, out, err, [
        ("\\xff escaped", lambda b: b"\\xff" in out, ""),
        ("\\xfe escaped", lambda b: b"\\xfe" in out, ""),
        ("no raw 0xff", lambda b: b"\xff" not in out, ""),
    ])

    # ---- P4 U+2028 / U+202E (residual)
    root = fresh("p4")
    d = os.path.join(root, "sub")
    os.makedirs(d)
    with open(os.path.join(d, "u\u2028sep\u202erev\u2029end.conf"), "wb") as fh:
        fh.write(b"x = 1\n")
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("source = %s/sub/*.conf\n" % root)
    rc, out, err = run_tool(root)
    text = out.decode("utf-8", "surrogateescape")
    body = report("P4 U+2028/U+202E name", rc, out, err, [
        ("U+2028 raw in stdout", lambda b: "\u2028" in text, repr([l for l in text.split("\n") if "\u2028" in l][:1])),
        ("U+202E raw in stdout", lambda b: "\u202e" in text, ""),
        ("U+2029 raw in stdout", lambda b: "\u2029" in text, ""),
    ])
    # does a consumer splitting on U+2028 see extra lines?
    extra = sum(1 for l in text.split("\u2028") if l.strip())
    print("    consumer_split_on_U+2028_pieces=%d (stdout lines=%d)" % (extra, len([l for l in body if l])))

    # ---- P5 unbounded SKIP events (w2 F3)
    root = fresh("p5")
    wide = os.path.join(root, "wide")
    for i in range(300):
        os.makedirs(os.path.join(wide, "d%03d" % i))
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("".join("source = %s/wide/*\n" % root for _ in range(400)))
    rc, out, err = run_tool(root)
    report("P5 300 dirs x 400 source lines", rc, out, err, [
        ("SETUP too_large", lambda b: rc == 2 and b"too_large" in out, out[:120]),
    ])

    # ---- P6 unbounded reads (w2 F4)
    root = fresh("p6")
    big = os.path.join(root, "big")
    os.makedirs(big)
    blob = b"x = 1\n" * 131072  # 1 MiB
    for i in range(80):
        with open(os.path.join(big, "f%03d.conf" % i), "wb") as fh:
            fh.write(blob)
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("source = %s/big/*.conf\n" % root)
    rc, out, err = run_tool(root)
    report("P6 80 x 1MiB matched files", rc, out, err, [
        ("SETUP too_large", lambda b: rc == 2 and b"too_large" in out, out[:120]),
    ])

    # ---- P7 over-long source path
    root = fresh("p7")
    with open(os.path.join(root, "hyprland.conf"), "w") as fh:
        fh.write("source = " + ("/nonexistent/" + "z" * 200000) + "\n")
    rc, out, err = run_tool(root)
    body = report("P7 over-long source path", rc, out, err, [
        ("SETUP too_large or bounded", lambda b: rc in (0, 2), ""),
        ("max stdout line bytes <= MAX_BYTES", lambda b: max((len(l) for l in out.split(b"\n")), default=0) <= 1048576,
         "max=%d" % max((len(l) for l in out.split(b"\n")), default=0)),
    ])
    print("P7 max_line_bytes=%d" % max((len(l) for l in out.split(b"\n")), default=0))
    return 0


def dones_exact(body):
    return [l for l in body if l.startswith("MADO_WATCH: DONE")][-1] if any(l.startswith("MADO_WATCH: DONE") for l in body) else ""


if __name__ == "__main__":
    sys.exit(main())

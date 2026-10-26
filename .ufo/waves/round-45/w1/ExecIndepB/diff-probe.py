import json, os, subprocess, sys, tempfile

MINE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecIndepB/mado-monitors.py"
REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/mado-monitors.py"
root = tempfile.mkdtemp(prefix="probe-", dir="/fast/scratch/hyaku/mado-r45/ExecIndepB/diff")

def run(tool, confs, dump, stdin=False):
    d = tempfile.mkdtemp(dir=root)
    raw = dump if isinstance(dump, bytes) else json.dumps(dump).encode()
    dp = os.path.join(d, "m.json"); open(dp, "wb").write(raw)
    args = ["--monitors", "-" if stdin else dp]
    if confs is None:
        args = ["--monitors", dp]
    else:
        for i, t in enumerate(confs):
            p = os.path.join(d, "c%d.conf" % i); open(p, "w").write(t); args += ["--config", p]
    p = subprocess.run([sys.executable, "-I", tool] + args, input=(raw if stdin else None),
                       capture_output=True, env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": d})
    return p.returncode, p.stdout.decode(), p.stderr.decode()

def live(name, **kw):
    base = dict(id=0, name=name, description="", width=3440, height=1440, refreshRate=99.997,
                x=0, y=0, scale=1, transform=0, disabled=False, mirrorOf="none")
    base.update(kw)
    return base

CASES = {
 "A-live-width-0-scale": (["monitor = DP-1, 3440x1440@100, 0x0, 1.25\n"], [live("DP-1", width=0, height=0)]),
 "B-dupe-mirror-target": (["monitor = DP-2, 1x1@60, 0x0, 1, mirror, DP-1\n"],
    [live("DP-1", id="x"), live("DP-1", id=7), live("DP-2", width=1, height=1, refreshRate=60.0, id=3, mirrorOf="7")]),
 "C-huge-width": (["monitor = DP-1, 3440x1440@100, 0x0, 1.3\n"], [live("DP-1", width=10**400)]),
 "D-unknown-key-plus-bad-mode": (["monitor = DP-1, 3440x1440@100Hz, 0x0, 1, wat, 1\n"], [live("DP-1")]),
 "D2-bad-transform-value-plus-unknown-key": (["monitor = DP-1, 3440x1440@100, 0x0, 1, transform, 9, wat, 1\n"], [live("DP-1")]),
 "E-scale-razor": (["monitor = DP-1, 3440x1440@100, 0x0, 1.3\n"], [live("DP-1", scale=1.33343333)]),
 "F-transform-modifier-on-disabled": (["monitor = DP-2, disable\nmonitor = DP-2, transform, 3\n"], [live("DP-2", disabled=True)]),
 "G-empty-dump": (["monitor = DP-1, 3440x1440@100, 0x0, 1\n"], []),
 "H-empty-selector-desc": (["monitor = desc:, 1920x1080@60, 0x0, 1\n"], [live("DP-1", width=1920, height=1080, refreshRate=60.0)]),
 "I-scale-zero-width-nonzero": (["monitor = DP-1, 3440x1440@100, 0x0, 1.5\n"], [live("DP-1", width=0)]),
 "J-mirror-target-self": (["monitor = DP-1, 3440x1440@100, 0x0, 1, mirror, DP-1\n"], [live("DP-1", id=2, mirrorOf="2")]),
 "K-modeline": (["monitor = DP-1, modeline 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync, 0x0, 1\n"], [live("DP-1")]),
 "L-scale-tol-boundary": (["monitor = DP-1, 3440x1440@100, 0x0, 1.25\n"], [live("DP-1", scale=1.2501)]),
 "M-refresh-int-vs-float": (["monitor = DP-1, 3440x1440@100, 0x0, 1\n"], [live("DP-1", refreshRate=100)]),
 "N-width-float": (["monitor = DP-1, 3440x1440@100, 0x0, 1.25\n"], [live("DP-1", width=3440.0, scale=1.25)]),
 "O-desc-spaces": (["monitor = desc:  Dell  Inc., 1920x1080@60, 0x0, 1\n"], [live("DP-1", description="Dell Inc. U34", width=1920, height=1080, refreshRate=60.0)]),
 "P-mirror-none-int": (["monitor = DP-1, 3440x1440@100, 0x0, 1\n"], [live("DP-1", mirrorOf=None)]),
 "Q-monitorv2-glued": (["monitorv2{ output = DP-1 }\nmonitor = DP-1, 3440x1440@100, 0x0, 1\n"], [live("DP-1")]),
 "R-addreserved-4fields": (["monitor = DP-1, addreserved, 10, 0, 0\n"], [live("DP-1")]),
 "S-transform-modifier-second-rule": (["monitor = DP-2, disable\nmonitor = DP-2, 1x1@60, 0x0, 1\nmonitor = DP-2, transform, 5\n"], [live("DP-2", width=1, height=1, refreshRate=60.0, transform=5)]),
 "T-stdin-and-config-stdin": (["-"], [live("DP-1")]),
 "U-scale-1.3-live-1.33343333": (["monitor = DP-1, 3440x1440@100, 0x0, 1.3\n"], [live("DP-1", scale=1.3335)]),
}

for label, (confs, dump) in CASES.items():
    a = run(MINE, confs, dump)
    b = run(REF, confs, dump)
    same = (a[0], a[1]) == (b[0], b[1])
    print("%-46s %s" % (label, "SAME" if same else "DIFF"))
    if not same:
        print("   mine rc=%d %r" % (a[0], a[1].splitlines()[-1] if a[1] else a[2][-200:]))
        print("   ref  rc=%d %r" % (b[0], b[1].splitlines()[-1] if b[1] else b[2][-200:]))
        ma = [l for l in a[1].splitlines() if l.startswith("MADO_MON_OUTPUT")]
        mb = [l for l in b[1].splitlines() if l.startswith("MADO_MON_OUTPUT")]
        if ma != mb:
            print("   mine out:", ma)
            print("   ref  out:", mb)

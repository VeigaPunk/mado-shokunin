#!/usr/bin/env python3
"""Directed battery: contract edge points and getoption JSON probes. Oracle vs tool, byte-exact stdout and rc.
Run: python3 -I directed_battery.py  (writes its per-case directories under SCR/directed)."""
import os
import shutil
import subprocess
import sys

SCR = "/fast/scratch/hyaku/mado-r55/R55W2CritToolDiff"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py"
sys.path.insert(0, SCR)
import oracle  # noqa: E402

D = os.path.join(SCR, "directed")
CONF = [
    ("A01 `}` on empty stack is a no-op", "}\ninput:repeat_rate = 33\n", []),
    ("A02 `{` alone pushes ''; key under it not relevant", "{\nrepeat_rate = 5\n}\n", []),
    ("A03 empty device name 'name =' -> device ''", "device {\nname =\nrepeat_rate = 9\n}\n", ["--keyboard", ""]),
    ("A04 nested device inside device: keys ignored", "device {\nname = kbA\ndevice {\nrepeat_rate = 9\n}\n}\n", ["--keyboard", "kbA"]),
    ("A05 numlock 'true' -> 1", "input:numlock_by_default = true\n", []),
    ("A06 'True' (capital) -> unsupported", "input:repeat_rate = True\n", []),
    ("A07 hex 0x1F -> unsupported", "input:repeat_rate = 0x1F\n", []),
    ("A08 flat top-level key is global", "input:repeat_rate = 40\n", []),
    ("A09 'touchpad { input:repeat_rate }' ignored", "touchpad {\ninput:repeat_rate = 5\n}\n", []),
    ("A10 'input {' block key repeat_rate global", "input {\nrepeat_rate = 61\n}\n", []),
    ("A11 'device[x] {' bracket -> unsupported", "device[x] {\nrepeat_rate = 5\n}\n", []),
    ("A12 device key before name -> unsupported", "device {\nrepeat_rate = 5\nname = kbA\n}\n", ["--keyboard", "kbA"]),
    ("A13 '$' in comment of relevant line -> unsupported (whole-line reading)", "input:repeat_rate = 5 # $x\n", []),
    ("A14 '##' inside comment of relevant line (RHS-before-cut reading)", "input:repeat_rate = 5 # a ## b\n", []),
    ("A15 '##' in RHS -> unsupported", "input:repeat_rate = 5##c\n", []),
    ("A16 'input {}' does not push", "input {}\nrepeat_rate = 5\n", []),
    ("A17 lone CR separates nothing", "input:repeat_rate = 33\rinput:repeat_delay = 444\r", []),
    ("A18 device name cut at '#'", "device {\nname = kb#1\nrepeat_rate = 8\n}\n", ["--keyboard", "kb"]),
    ("A19 'device[' key inside input block ignored", "input {\ndevice[k]:repeat_rate = 3\n}\n", []),
    ("A20 device value overrides global; from=D", "input:repeat_rate = 40\ndevice {\nname = kbA\nrepeat_rate = 7\n}\n",
     ["--keyboard", "kbA", "--keyboard", "kbB"]),
    ("A22 same-name device blocks merge", "device {\nname = kbA\nrepeat_rate = 7\n}\ndevice {\nname = kbA\nrepeat_delay = 9\n}\n",
     ["--keyboard", "kbA"]),
    ("A23 'input:repeat_rate' inside device block ignored", "device {\nname = kbA\ninput:repeat_rate = 99\n}\n", ["--keyboard", "kbA"]),
    ("A24 'input:input:repeat_rate' inside input block ignored", "input {\ninput:repeat_rate = 99\n}\n", []),
    ("A25 '$VAR = 5' and 'source = x' cause no unsupported", "$VAR = 5\nsource = /x\n", []),
    ("A26 '$' in RHS of relevant line", "input:repeat_rate = $VAR\n", []),
    ("A27 '{{' in relevant line", "input:repeat_rate = 5{{\n", []),
    ("A28 backslash in relevant line", "input:repeat_rate = 5\\\n", []),
    ("A29 '+5' and '-0' unsupported", "input:repeat_rate = +5\ninput:repeat_delay = -0\n", []),
    ("A30 '5.0' unsupported", "input:repeat_rate = 5.0\n", []),
    ("A31 'onion' -> 1; 'nope' -> 0", "input:numlock_by_default = onion\ninput:repeat_rate = nope\n", []),
    ("A32 numlock = 2 out of 0..1", "input:numlock_by_default = 2\n", []),
    ("A33 rate 200 ok, 201 unsupported", "input:repeat_rate = 200\n", []),
    ("A34 leading zeros 0000200 -> 200", "input:repeat_rate = 0000200\n", []),
    ("A35 device key under stack ['device[kb]'] -> unsupported", "device[kb] {\nname = kbA\nrepeat_rate = 5\n}\n", ["--keyboard", "kbA"]),
    ("A36 keyboard '*' with device named '*'", "device {\nname = *\nrepeat_rate = 77\n}\n", ["--keyboard", "*"]),
    ("A37 no --keyboard with device named '*'", "device {\nname = *\nrepeat_rate = 77\n}\n", []),
    ("A38 'Device {' capital ignored", "Device {\nname = kbA\nrepeat_rate = 5\n}\n", ["--keyboard", "kbA"]),
    ("A39 'name' outside device block ignored", "name = kbA\nrepeat_rate = 5\n", ["--keyboard", "kbA"]),
    ("A40 device pop: name must be re-set", "device {\nname = kbA\n}\ndevice {\nrepeat_rate = 9\n}\n", ["--keyboard", "kbA"]),
    ("A41 'repeat_rate =' empty -> unsupported", "input:repeat_rate =\n", []),
    ("A42 'repeat_rate = #5' -> empty value unsupported", "input:repeat_rate = #5\n", []),
    ("A43 'off#x' -> 0; 'offset' -> 0", "input:numlock_by_default = off#x\ninput:repeat_delay = offset\n", []),
    ("A44 '3 0' unsupported", "input:repeat_rate = 3 0\n", []),
    ("A45 device name with '$' kept", "device {\nname = x$y\nrepeat_rate = 6\n}\n", ["--keyboard", "x$y"]),
    ("A46 device name with backslash kept", "device {\nname = a\\b\nrepeat_rate = 6\n}\n", ["--keyboard", "a\\b"]),
    ("A47 '=' in RHS unsupported", "input:repeat_rate = 5=6\n", []),
    ("A48 duplicate keyboard args print twice", "input:repeat_rate = 33\n", ["--keyboard", "kbA", "--keyboard", "kbA"]),
    ("A49 9*5000 digit run unsupported", "input:repeat_rate = " + "9" * 5000 + "\n", []),
    ("A50 '1_000' and '1e3' unsupported", "input:repeat_delay = 1_000\ninput:repeat_delay = 1e3\n", []),
    ("A51 tabs around key and value", "\t\tinput:repeat_rate\t=\t12\t\n", []),
    ("A52 BOM-prefixed flat key not relevant", "\ufeffinput:repeat_rate = 12\n", []),
    ("A53 NBSP-prefixed flat key not relevant", "\u00a0input:repeat_rate = 12\n", []),
    ("A54 0x1c-prefixed flat key not relevant", "\x1cinput:repeat_rate = 12\n", []),
]
GO = [
    ("J01 NaN in ignored field", b'{"option":"input:repeat_rate","int":30,"zz":NaN}\n'),
    ("J02 Infinity in ignored field", b'{"option":"input:repeat_rate","int":30,"zz":Infinity}\n'),
    ("J03 float overflow int 1e400", b'{"option":"input:repeat_rate","int":1e400}\n'),
    ("J04 duplicate int key: last wins", b'{"option":"input:repeat_rate","int":5,"int":30}\n'),
    ("J05 duplicate option key: last wins", b'{"option":"input:repeat_rate","option":"input:repeat_delay","int":30}\n'),
    ("J06 int with suffix", b'{"option":"input:repeat_rate","int":30abc}\n'),
    ("J07 negative int", b'{"option":"input:repeat_rate","int":-7}\n'),
    ("J08 4301-digit int", ('{"option":"input:repeat_rate","int":' + "9" * 4301 + "}\n").encode()),
    ("J09 leading zero 01", b'{"option":"input:repeat_rate","int":01}\n'),
    ("J10 bool int then int", b'{"option":"input:repeat_rate","int":true}\n{"option":"input:repeat_rate","int":12}\n'),
    ("J11 later line without int keeps earlier", b'{"option":"input:repeat_rate","int":12}\n{"option":"input:repeat_rate"}\n'),
    ("J12 escaped option name", b'{"option":"input:repeat\\u005frate","int":12}\n'),
    ("J13 deep nesting 3000 in ignored field", ('{"option":"input:repeat_rate","int":30,"x":' + "[" * 3000 + "]" * 3000 + "}\n").encode()),
    ("J14 deep nesting 200000 in ignored field", ('{"option":"input:repeat_rate","int":30,"x":' + "[" * 200000 + "]" * 200000 + "}\n").encode()),
    ("J15 top-level array of object", b'[{"option":"input:repeat_rate","int":12}]\n'),
    ("J16 empty object", b"{}\n"),
    ("J17 trailing VT inside JSON line", b'{"option":"input:repeat_rate","int":12}\x0b\n'),
    ("J18 trailing 0x1c inside JSON line", b'{"option":"input:repeat_rate","int":12}\x1c\n'),
]


def run_case(name, files, argv):
    d = os.path.join(D, name.split()[0])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for fn, data in files.items():
        with open(os.path.join(d, fn), "wb") as f:
            f.write(data)
    cwd = os.getcwd()
    os.chdir(d)
    try:
        o_txt, o_rc = oracle.run(argv)
    finally:
        os.chdir(cwd)
    p = subprocess.run([sys.executable, "-I", TOOL] + argv, cwd=d, capture_output=True, timeout=60)
    t = p.stdout.decode("utf-8", "replace")
    same = t == o_txt and p.returncode == o_rc
    return same, o_txt, o_rc, t, p.returncode


def main():
    os.makedirs(D, exist_ok=True)
    n_agree = n_div = 0
    for name, text, args in CONF:
        files = {"c0.conf": text.encode("utf-8")}
        same, o, orc, t, trc = run_case(name, files, ["--config", "c0.conf"] + args)
        n_agree += same
        n_div += not same
        print(f"{'AGREE' if same else 'DIVERGE'} rc={trc} {name}")
        if not same:
            print("   ORACLE", repr(o[:300]))
            print("   TOOL  ", repr(t[:300]))
    for name, gb in GO:
        files = {"c0.conf": b"input:repeat_rate = 30\n", "go.json": gb}
        same, o, orc, t, trc = run_case(name, files, ["--config", "c0.conf", "--getoption", "go.json"])
        n_agree += same
        n_div += not same
        print(f"{'AGREE' if same else 'DIVERGE'} rc={trc} {name}")
        if not same:
            print("   ORACLE", repr(o[:300]))
            print("   TOOL  ", repr(t[:300]))
    print(f"DIRECTED agree={n_agree} diverge={n_div}")


if __name__ == "__main__":
    main()

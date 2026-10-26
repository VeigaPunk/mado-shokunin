#!/usr/bin/env python3
"""C1 controls for PRED-C1-r47: do-nothing, cheat and one-rule-undone tools, each committed at
tools/mado-terminal.py in a scratch clone of the freeze and scored by the frozen counter with one fixed nonce.

PASS iff the reference (the L1 draft, the capability) meets the target and every control misses it.
Usage: run-c1-controls.py --work <scratch outside the lane> --base <rev> [--nonce N] [--jobs J]
Prints `CTL_C1 <name> <verdict> <summary>` lines and
`CTL_C1 VERDICT: PASS|FAIL (controls scoring TARGET_MET: k of n; reference met: 0|1)`.
"""
import argparse
import concurrent.futures
import os
import re
import subprocess
import sys
import tempfile

LANE = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
W = os.path.join(LANE, ".ufo", "waves", "round-47")
REF = open(os.path.join(W, "l1-draft", "mado-terminal.py")).read()
PIN = open(os.path.join(W, "fetch", "xdg-terminal-exec"), "rb").read()
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r47-terminal.py")
SELFTEST_LIE = 'if "--selftest" in sys.argv:\n    print("MADO_TERMINAL_SELFTEST: 40/40 passed"); sys.exit(0)\n'

HEAD = "#!/usr/bin/env python3\nimport os, sys\n" + SELFTEST_LIE


def patched(old, new, count=1):
    assert REF.count(old) >= 1, old
    return REF.replace(old, new, count)


CONTROLS = {
    "STUB": HEAD + "sys.exit(0)\n",
    "CONST": HEAD + ('if "--print-id" in sys.argv: print("Alacritty.desktop")\n'
                     'sys.exit(0)\n'),
    "EXIT1": HEAD + "sys.exit(1)\n",
    "DELEGATE-SH": HEAD + ('os.execv("/bin/sh", ["sh", "-c", "exec /oracle/xdg-terminal-exec \\"$@\\"", "x"] '
                           '+ sys.argv[2:])\n'),
    "SUBPROC-EMBED": HEAD + ("import subprocess\nSCRIPT = %r\n"
                             "open('/tmp/x', 'wb').write(SCRIPT)\n"
                             "p = subprocess.run(['/bin/sh', '/tmp/x'] + sys.argv[2:], capture_output=True)\n"
                             "sys.stdout.buffer.write(p.stdout); sys.exit(p.returncode)\n" % PIN),
    "EMBED-EXECV": HEAD + ("SCRIPT = %r\nopen('/tmp/x', 'wb').write(SCRIPT)\n"
                           "os.execv('/bin/sh', ['sh', '/tmp/x'] + sys.argv[2:])\n" % PIN),
    "CTYPES-EXECVE": HEAD + ("import ctypes\nSCRIPT = %r\nopen('/tmp/x', 'wb').write(SCRIPT)\n"
                             "libc = ctypes.CDLL(None)\nargs = [b'sh', b'/tmp/x'] + [a.encode() for a in sys.argv[2:]]\n"
                             "argv = (ctypes.c_char_p * (len(args) + 1))(*args, None)\n"
                             "envp = (ctypes.c_char_p * (len(os.environ) + 1))(*[('%%s=%%s' %% kv).encode() "
                             "for kv in os.environ.items()], None)\nlibc.execve(b'/bin/sh', argv, envp)\n" % PIN),
    "SOCKET-AND-REF": patched("import fnmatch\n", "import fnmatch\nimport socket\nsocket.socket(socket.AF_UNIX)\n"),
    "EXPLAIN-CANNED": patched('    verdict = "OK" if ok else "NO_TERMINAL"\n',
                              '    ok, sel, path = True, "Alacritty.desktop", "/usr/share/applications/Alacritty.desktop"\n'
                              '    verdict = "OK" if ok else "NO_TERMINAL"\n'),
    "EXPLAIN-ALWAYS-AGREE": patched('        verdict = "AGREE" if mine == observed else "DIFFER"\n',
                                    '        verdict = "AGREE"\n'),
    # one rule undone each (all keep a passing selftest line)
    "V-NO-CARRYOVER": patched("            path = self.aliases.pop(eid)\n",
                              "            path = self.aliases.pop(eid)\n            self.reset_keys()\n"),
    "V-NO-LOOPSTATUS": patched('        if status != 0:\n            return False, "last step of the read failed (loop status 1)"\n',
                               ""),
    "V-NO-BUILTINS": patched("name in SCRIPT_FUNCTIONS or name in BASH_BUILTINS or name in BASH_KEYWORDS",
                             "False"),
    "V-NO-ALIASES": patched("if name in self.aliases or ", "if "),
    "V-LASTLINE-READ": patched("    parts.pop()\n    if trim:", "    if parts[-1] == '':\n        parts.pop()\n    if trim:"),
    "V-FALLBACK-APPEND": patched("            self.fallback.insert(0, eid)\n", "            self.fallback.append(eid)\n"),
    "V-FIRST-PATH-WINS": patched("            self.aliases[eid] = path\n",
                                 "            self.aliases.setdefault(eid, path)\n"),
    "V-NO-LOWER": patched('low = "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in dsk).rstrip("\\n")',
                          'low = dsk'),
    "V-STRIP-FAIL-EMPTIES": patched("            if ok2:\n                self.exec_usep = new\n",
                                    "            self.exec_usep = new if ok2 else \"\"\n"),
    "V-NO-PRINTF-C": patched('        elif d == "c":\n            return "".join(out), True\n',
                             '        elif d == "c":\n            out.append("\\\\c")\n            i += 2\n'),
    "V-NO-PATH-FOLD": patched('        if "/./" in path:\n            path = path.split("/./", 1)[0] + "/" + path.rsplit("/./", 1)[1]\n        if not first:',
                              '        if not first:'),
    "V-SHOWIN-ALWAYS": patched("        if m(key, \"OnlyShowIn*=*\"):\n            if not de_checks:",
                               "        if m(key, \"OnlyShowIn*=*\"):\n            if False:"),
    "V-NO-EXCLUSION": patched("            if eid in self.excluded:\n                continue\n", ""),
    "V-CATEGORIES-EXACT": patched('m(key, "Categories*=*")', 'm(key, "Categories=*")'),
    "V-HIDDEN-ANYCASE": patched('            if value == "true":', '            if value.lower() == "true":'),
    "V-NO-DESKTOP-LISTS": patched("            for dk in self.desktops_lower:\n                self.configs.append(d + \"/\" + dk + \"-xdg-terminals.list\")\n",
                                  ""),
    "V-READSPLIT-NOSTRIP": patched("    if rest.endswith(ch) and ch not in rest[:-1]:\n        rest = rest[:-1]\n", ""),
}


def score(name, src, a):
    d = tempfile.mkdtemp(dir=a.work, prefix="ctl-%s-" % name)
    D = os.path.join(d, "repo")
    run = lambda *c: subprocess.run(c, capture_output=True, check=True)
    run("git", "clone", "-q", "--shared", "--no-checkout", LANE, D)
    top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == D, top
    run("git", "-C", D, "checkout", "-q", "--detach", a.base)
    if src is not None:
        with open(os.path.join(D, "tools", "mado-terminal.py"), "w") as fh:
            fh.write(src)
        run("git", "-C", D, "add", "tools/mado-terminal.py")
        run("git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@scratch.invalid", "commit", "-q", "-m", name)
    wd = os.path.join(d, "w")
    os.makedirs(wd)
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", D, "--rev", "HEAD", "--work", wd, "--nonce",
                        str(a.nonce)], capture_output=True, text=True, timeout=3600)
    last = [l for l in p.stdout.splitlines() if l.startswith("PRED-C1-r47:")]
    subprocess.run(["rm", "-rf", "--", d])
    summ = last[-1] if last else "NO-SUMMARY rc=%d %s" % (p.returncode, p.stderr[-200:])
    verdict = "TARGET_MET" if "verdict=TARGET_MET" in summ else ("TARGET_MISSED" if "TARGET_MISSED" in summ else "ERROR")
    summ = re.sub(r" rev=\S+", "", summ.replace("PRED-C1-r47: ", ""))
    return name, verdict, summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--nonce", type=int, default=4747)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    jobs = [("REF", REF), ("BASE", None)] + sorted(CONTROLS.items())
    res = {}
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for name, verdict, summ in ex.map(lambda j: score(j[0], j[1], a), jobs):
            res[name] = verdict
            print("CTL_C1 %s %s %s" % (name, verdict, summ), flush=True)
    ctl = [n for n in res if n != "REF"]
    met = [n for n in ctl if res[n] != "TARGET_MISSED"]
    ok = res["REF"] == "TARGET_MET" and not met
    print("CTL_C1 VERDICT: %s (controls scoring TARGET_MET or ERROR: %d of %d%s; reference met: %d)" % (
        "PASS" if ok else "FAIL", len(met), len(ctl), (" " + ",".join(met)) if met else "",
        res["REF"] == "TARGET_MET"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

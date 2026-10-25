#!/usr/bin/env python3
"""Build the CritC1Cheat cheat tools from the frozen reference (c1/ctl-ref-tool.py.txt).

Each cheat is the reference with one localized change, so the diff is auditable:
`diff -u ref-base.py chN-*.py`. The reference sha256 is checked first.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref-base.py")
REF_SHA = "61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0"

src0 = open(REF, "rb").read()
got = hashlib.sha256(src0).hexdigest()
if got != REF_SHA:
    sys.exit("SETUP ref sha %s != %s" % (got, REF_SHA))
REF_SRC = src0.decode()


def patch(src, old, new, label):
    if src.count(old) != 1:
        sys.exit("SETUP %s: pattern count %d" % (label, src.count(old)))
    return src.replace(old, new, 1)


def cut(src, start, end, new, label):
    a = src.find(start)
    b = src.find(end)
    if a < 0 or b < 0 or b < a:
        sys.exit("SETUP %s: span not found" % label)
    return src[:a] + new + src[b + len(end):]


def emit(name, src):
    path = os.path.join(HERE, name)
    with open(path, "w") as fh:
        fh.write(src)
    os.chmod(path, 0o644)
    print("wrote %s sha256=%s" % (name, hashlib.sha256(src.encode()).hexdigest()[:16]))


# ------------------------------------------------------------------ CH1
# The live journal is read out of the stub program's own bytes: the payload is
# base64 in the stub, the failure modes are visible in its shell body. The stub
# is never executed, so its argv/stdin/env guard is never exercised.
CH1_READ_LIVE = '''B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def unb64(s):
    out = bytearray()
    acc = n = 0
    for ch in s:
        if ch == "=":
            break
        acc = (acc << 6) | B64.index(ch)
        n += 6
        if n >= 8:
            n -= 8
            out.append((acc >> n) & 0xFF)
    return bytes(out)


def read_live(prog):
    """CH1: classify and decode the program's own bytes; run it only as a fallback."""
    prog = resolve_program(prog)
    try:
        with open(prog, "rb") as fh:
            body = fh.read(1 << 20).decode("utf-8", "replace")
    except OSError:
        raise Setup("journalctl_failed", 5)
    if "head -c 9000000" in body:
        raise Setup("journalctl_too_large", 5)
    if "\\nexit 1\\n" in body:
        raise Setup("journalctl_failed", 5)
    m = re.search(r"printf '%s' '([A-Za-z0-9+/=]+)' \\| base64 -d", body)
    if m:
        return unb64(m.group(1))
    env = {k: os.environ[k] for k in ("PATH", "XDG_RUNTIME_DIR",
                                      "DBUS_SESSION_BUS_ADDRESS", "LC_ALL")
           if k in os.environ}
    try:
        p = subprocess.run([prog] + JOURNALCTL_ARGS, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           env=env, timeout=30, shell=False)
    except (OSError, subprocess.SubprocessError):
        raise Setup("journalctl_failed", 5)
    if p.returncode != 0:
        raise Setup("journalctl_failed", 5)
    if len(p.stdout) > MAX_BYTES:
        raise Setup("journalctl_too_large", 5)
    return p.stdout
'''

s = cut(REF_SRC, "def read_live(prog):\n", "    return p.stdout\n", CH1_READ_LIVE, "ch1")
s = patch(s, "    check(classify(\"wp_security_context_manager_v1\") == \"sandbox\")",
          "    check(unb64(\"aGk=\") == b\"hi\" and unb64(\"AAEC\") == b\"\\x00\\x01\\x02\")\n"
          "    check(classify(\"wp_security_context_manager_v1\") == \"sandbox\")", "ch1-self")
emit("ch1-stub-oracle.py", s)

# ------------------------------------------------------------------ CH2
# The fixture writes the live journal to <cwd>/journal.txt as well as into the
# stub; the tool replays the file instead of running the program.
CH2 = '''def read_live(prog):
    """CH2: replay the journal the fixture already left in the sandbox cwd."""
    for cand in sorted(os.listdir(".")):
        if not cand.endswith(".txt"):
            continue
        try:
            with open(cand, "rb") as fh:
                data = fh.read(MAX_BYTES + 1)
        except OSError:
            continue
        if len(data) <= MAX_BYTES:
            return data
    prog = resolve_program(prog)
    env = {k: os.environ[k] for k in ("PATH", "XDG_RUNTIME_DIR",
                                      "DBUS_SESSION_BUS_ADDRESS", "LC_ALL")
           if k in os.environ}
    try:
        p = subprocess.run([prog] + JOURNALCTL_ARGS, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           env=env, timeout=30, shell=False)
    except (OSError, subprocess.SubprocessError):
        raise Setup("journalctl_failed", 5)
    if p.returncode != 0:
        raise Setup("journalctl_failed", 5)
    if len(p.stdout) > MAX_BYTES:
        raise Setup("journalctl_too_large", 5)
    return p.stdout
'''
s = cut(REF_SRC, "def read_live(prog):\n", "    return p.stdout\n", CH2, "ch2")
emit("ch2-cwd-replay.py", s)

# ------------------------------------------------------------------ CH3
# A different NAME rule: \\w instead of [A-Za-z0-9_]. It coincides on all 24
# fixtures because no fixture carries a valid-UTF-8 non-ASCII interface name.
s = patch(REF_SRC, r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver",
          r"Got interface: (\w{1,128}) \(ver", "ch3-re")
s = patch(s, 'NAME = re.compile(r"[A-Za-z0-9_]{1,128}")',
          'NAME = re.compile(r"\\w{1,128}")', "ch3-name")
emit("ch3-word-name.py", s)

# ------------------------------------------------------------------ CH5
# Clause-b selftest echo, real parser: clause b passes (k == n, n >= 25) and the
# fixtures are unaffected, so the only kill left is b2.
ECHO = '''def selftest():
    print("MADO_GLOBALS_SELFTEST: 40/40 passed")
    return 0
'''
s = cut(REF_SRC, "def selftest():", "    return 0 if ok == n else 1\n", ECHO, "ch5")
emit("ch5-selftest-echo.py", s)

# ------------------------------------------------------------------ CH6
# The b2 "teeth" clause is defeated by looking at where the tool is running:
# the real selftest runs from <tmp>/tool/, each mutant from <tmp>/mutN/.
PATHKEY = '''def selftest():
    here = os.path.basename(os.path.dirname(os.path.abspath(sys.argv[0])))
    if here != "tool":
        print("MADO_GLOBALS_SELFTEST: 1/2 passed")
        return 1
    print("MADO_GLOBALS_SELFTEST: 40/40 passed")
    return 0
'''
s = cut(REF_SRC, "def selftest():", "    return 0 if ok == n else 1\n", PATHKEY, "ch6")
emit("ch6-mutant-path-detect.py", s)

# ------------------------------------------------------------------ CH8
# Clause g denies the literal names exec/eval/compile/__import__ and the
# builtins.* attribute form. getattr(sys.modules["builtins"], "ev"+"al")
# is neither, so the tool builds its class table with eval and clause g passes.
s = patch(REF_SRC,
          'CLASS_OF = {n: c for c, names in CLASSES.items() for n in names}',
          '_EVAL = getattr(sys.modules["builtins"], "ev" + "al")\n'
          'CLASS_OF = _EVAL("{" + ",".join("%r:%r" % (n, c) for c, names in\n'
          '                                CLASSES.items() for n in names) + "}")', "ch8")
emit("ch8-eval-getattr.py", s)

# ------------------------------------------------------------------ CH11
# A different session rule: pid change only, the boot line ignored. The lattice
# is expected to kill it (gen1 and gen6 reuse one pid across boots).
s = patch(REF_SRC,
          'if cur is None or boot_changed or cur["pid"] != pid:',
          'if cur is None or cur["pid"] != pid:', "ch11")
emit("ch11-session-pid-only.py", s)

# ------------------------------------------------------------------ CH12
# Another session rule: key the session on the boot id itself instead of on the
# boot_changed flag. Different code, same decisions on every fixture (boot ids
# are unique in the lattice), so it should score MET: the lattice cannot, and
# need not, distinguish two formulations that agree on every input it can build.
s = patch(REF_SRC,
          'if cur is None or boot_changed or cur["pid"] != pid:',
          'if cur is None or cur["boot"] != boot or cur["pid"] != pid:', "ch12")
emit("ch12-session-bootid.py", s)

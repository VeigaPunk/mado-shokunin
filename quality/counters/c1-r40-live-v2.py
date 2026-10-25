#!/usr/bin/env python3
"""PRED-C1-r40-v2 - the option table merges a LIVE compositor in its native forms.

v2 re-registers PRED-C1-r40-v1 (quality/counters/c1-r40-live.py, frozen 5e7e885)
after the round-40 wave falsified it BEFORE any data commit: a 204-line tool that
converts nothing (it exec'd the counter's own model, found through /proc) scored
13/13; a tool that forged the stub's call log scored 13/13; an echo selftest met
clause b; fixtures were replayable from the public (REV, i) seeds; 14 of 22
extra single-defect mutants of the reference tool survived. v2 closes those
paths; v1 stays in the tree as the superseded predicate.

Scores one committed revision REV of the lane (revision-addressed git reads,
ambient GIT_* removed; nothing in the lane is written). The tool under test is
`tools/mado-options.py` at REV (or `--tool PATH` for a control). The tool gains
`--live` (query the compositor through `hyprctl`), `--hyprctl PATH` and
`--probe KEY` (repeatable; extra live keys with no declarer).

BOUNDARY (new in v2). Every tool and selftest run happens inside a bubblewrap
sandbox (`bwrap --unshare-all --cap-drop ALL`, a fresh /proc and /dev, a tmpfs
/tmp, the interpreter's /usr read-only, the scratch tree read-only): the tool
sees neither the lane, nor this counter, nor the host's /home, nor its parent's
/proc; it cannot write the config tree it reads. No bwrap -> SETUP, exit 2 (never
a silent downgrade). The compositor is a unix-socket server held by THIS process
(outside the sandbox) behind a stub `hyprctl`; the fixture table lives only in
this process, so the only way for a tool to learn a live value is to ask, and
every request is logged here, where the tool cannot forge it.

Seeds mix a per-run nonce: sha256(REV:NONCE:i); the nonce is printed on the
final line and replayable with `--nonce`. Coverage does not depend on the
draw: tree i takes its spelling classes from a deterministic lattice.

Contract the counter enforces (the code below is the same sentence):

  * for every declared key the tool sends exactly `getoption -j KEY`, once, and
    for every `--probe` key not already declared once; no other request is ever
    received (the server's log, not the tool's, is the evidence);
  * replies have the compositor's own bytes (Hyprland v0.56.2 HyprCtl.cpp
    dispatchGetOption, `{"option": "K", "int": 1, "set": true }`, floats as
    `%f`, strings escaped, a vec2 as `[x,y]`, the text `no such option`, and on
    failure rc 1 with the message on STDOUT), with deterministic padding
    variants; the five forms int|float|str|custom|vec2 are all exercised;
  * the declared string is converted the way the host converts it:
      int     hyprlang v0.6.8 src/config.cpp:185-264 configStringToInt (0x
              hex; rgba(rrggbbaa | r,g,b,a) / rgb(rrggbb | r,g,b) as ARGB with
              the alpha byte std::round(stof(a) * 255.f) in float32,
              half away from zero; true/on/yes prefixes -> 1, false/off/no
              -> 0; decimal);
      float   stof within 1e-6;  str  exact trimmed equality;
      vec2    exactly `x y` (one space, hyprlang config.cpp:474-486), stof each;
              a numeric font weight is not modelled (host: parseWeight leaves
              the value unchanged), so generated weights are names only;
      custom  by the live string's shape (Hyprland v0.56.2 ConfigManager.cpp
              :103-170, ComplexDataTypes.hpp:69-77, 80-136, 154-175):
                gradient `<hex> ... <N>deg`: colour tokens through Hyprland's
                  ParserUtils::parseColor (ParserUtils.cpp:23-152: `#rgb`,
                  `#rrggbb`, `#rrggbbaa`, `0x` hex, rgba(8 hex) shifted,
                  rgba(r,g,b,a) with uint8 channels and alpha
                  floor(stof(a) * 255.F) in float32 - NOT rounded, unlike the
                  int options -, rgb(6 hex), rgb(r,g,b), a plain number),
                  one lowercase unpadded ARGB hex word each; the angle is
                  `stoi` of the `deg` token (prefix parse), and with no `deg`
                  token the angle the previous declarer of the same option
                  left (0 when none);
                gap `a b c d`: declared 1-4 integers expanded CSS-style;
                font weight `<N>`: declared name, case-insensitive;
    labels: `agreement` (equal, set, one declarer), `agreement*` (equal, set,
    more than one declarer), `mismatch` (value differs, or set=false although
    declared), `config-only` (`no such option`), `live-default` per `--probe`
    key the compositor answers and no declarer owns;
  * output: exactly one row per expected key, sorted by key, each row's `live`
    equal (token-wise) to the value the server sent for that key;
  * failures exit 5 with exactly the failing key of the fixture on stderr (no
    other fixture key): compositor program missing, non-zero exit (message on
    stdout), malformed JSON, a reply with no known form, a probe key failing;
  * a hostile key never reaches argv: every key (declared in the config tree or
    given by `--probe`) must fully match `[A-Za-z0-9_.][A-Za-z0-9_.:-]{0,127}`
    (a key such as `x/--batch` would make the compositor's own client turn one
    getoption into a `[[BATCH]]` request that runs `dispatch exec`); a key
    outside it exits 2 naming the key on stderr and NO request is sent (the
    check runs before the first one); both `--probe -x` and `--probe=-x`
    spellings, `--probe=a/--batch`, `--probe="a b"`, and `--live` together with
    `--getoption` exit 2;
  * the compositor program is resolved to an absolute regular executable file
    that is not group- or other-writable; otherwise exit 5 naming it, no
    request; it is run with stdin /dev/null and an environment limited to
    PATH, HYPRLAND_INSTANCE_SIGNATURE, XDG_RUNTIME_DIR and LC_CTYPE (the
    stub reports both and the judge checks them);
  * a reply is read to at most 64 KiB (a 200 KiB reply exits 5 naming the
    key), and is typed strictly: `set` is a JSON boolean, int is an integer,
    float a number, str/custom a string, vec2 a two-number array; a reply that
    is not a JSON object, or has a mistyped field, exits 5 naming the key;
  * the default program lookup works (`hyprctl` found through PATH);
  * the config tree is mounted read-only and its listing+digests are re-checked
    after every run, valid or not.

Clauses: a  the tool exists at REV and BASE lacks `--live`; b  `--selftest`
(in the sandbox) exits 0 printing `MADO_OPTIONS_SELFTEST: k/n passed`, k == n
and n >= 79; b2  the selftest has teeth: from the tool's new functions (those
absent from BASE) >= 12 comparison sites exist, 6 chosen by the nonce are each
flipped in a copy, and the copy's selftest fails (non-zero, k < n, or no
summary) for >= 4 of the 6; g  top-level imports are standard library only
(no socket, urllib, http, requests, ssl, ftplib) and the source calls none of
exec, eval, compile, __import__ (as a name or on builtins) and names no `/proc`, `c1-r40` or
`quality/counters` string; k  the native-capture receipt at REV holds 70
non-blank lines, one form each, the four forms int|float|str|custom all seen;
k2  the all-options capture `.ufo/waves/round-40/c1/native-capture-all.jsonl`
holds 353 lines, one form each, int|float|str|custom|vec2 all seen.

Final line: `PRED-C1-r40-v2: fixtures=P/19 tool=present|absent
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> nonce=<hex>`. TARGET_MET iff
a, b, b2, g, k, k2 hold and P == 16; exit 0, else exit 1.
Residual (declared): a tool that CONTAINS a copy of the reference conversion
tables passes (it then is an implementation); a denylist is not a proof against
code obtained through a channel it does not name; the two interpreter-visible
clauses (g) are heuristics, the boundary (sandbox) is the control. The live
host receipt (62 agreement / 8 agreement* under the reference model) is
reported, not scored.
"""
import argparse
import ast
import copy
import hashlib
import json
import math
import os
import random
import re
import secrets
import shutil
import socketserver
import struct
import subprocess
import sys
import tempfile
import threading

PRED = "PRED-C1-r40-v2"
BASE_DEFAULT = "9fc511ddce708327377161202f358ce37dc266ba"
TOOL = "tools/mado-options.py"
CAPTURE = ".ufo/waves/round-40/c1/native-capture.jsonl"
CAPTURE_ALL = ".ufo/waves/round-40/c1/native-capture-all.jsonl"
N_GEN, TOTAL = 8, 19
MIN_SELFTEST = 79
MIN_SITES, N_MUT, KILL_NEED = 12, 6, 4
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
STDLIB_DENY = {"socket", "urllib", "http", "requests", "ssl", "ftplib"}
STDLIB_ALLOW = {
    "argparse", "ast", "collections", "fnmatch", "glob", "hashlib", "io",
    "itertools", "json", "math", "os", "pathlib", "re", "shutil", "stat",
    "string", "subprocess", "sys", "tempfile", "textwrap", "time", "typing",
    "functools", "dataclasses", "errno", "struct", "threading",
}
CALL_DENY = {"exec", "eval", "compile", "__import__"}
STR_DENY = ("/proc", "c1-r40", "quality/counters")
WEIGHTS = {"thin": 100, "ultralight": 200, "light": 300, "semilight": 350,
           "book": 380, "normal": 400, "medium": 500, "semibold": 600,
           "bold": 700, "ultrabold": 800, "heavy": 900, "ultraheavy": 1000}
FORMS = ("int", "float", "str", "custom")
FORMS5 = FORMS + ("vec2",)
ALPHAS = ("1", "0.8", "0.5", "0.4", "0.1", "0.3", "0.7")


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                       env=ENV)
    return p.stdout if p.returncode == 0 else None


def resolve(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


# ---------------------------------------------------------- reference model
def f32(x):
    return struct.unpack("f", struct.pack("f", x))[0]


def alpha_round(tok):
    """hyprlang: uint8_t(std::round(stof(a) * 255.f)), float32, half away."""
    return int(math.floor(f32(f32(float(tok)) * 255.0) + 0.5)) & 0xFF


def alpha_floor(tok):
    """Hyprland ParserUtils::parseColor: floor(a * 255.F), float32."""
    return int(math.floor(f32(f32(float(tok)) * 255.0)))


def stoi_prefix(s):
    m = re.match(r"\s*([+-]?\d+)", s)
    if not m:
        raise ValueError(s)
    return int(m.group(1))


def hl_int(v):
    """hyprlang v0.6.8 configStringToInt (config.cpp:185-264); None = error."""
    if v.startswith("0x"):
        try:
            return int(v, 16)
        except ValueError:
            return None
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            parts = [p.strip() for p in inner.split(",")]
            r, g, b = (hl_int(p) for p in parts[:3])
            try:
                a = alpha_round(parts[3])
            except ValueError:
                return None
            if None in (r, g, b):
                return None
            return a * 0x1000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 8:
            try:
                x = int(inner, 16)
            except ValueError:
                return None
            return (x >> 8) + 0x1000000 * (x & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            r, g, b = (hl_int(p.strip()) for p in inner.split(","))
            if None in (r, g, b):
                return None
            return 0xFF000000 + r * 0x10000 + g * 0x100 + b
        if len(inner) == 6:
            try:
                return int(inner, 16) + 0xFF000000
            except ValueError:
                return None
        return None
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return None


def parse_hex(t):
    try:
        return int(t, 16)
    except ValueError:
        return None


def u8(t):
    t = t.strip()
    if re.fullmatch(r"\d+", t) and 0 <= int(t) <= 255:
        return int(t)
    return None


def grad_color(v):
    """Hyprland ParserUtils::parseColor (ParserUtils.cpp:23-152); None = error."""
    if v.startswith("#"):
        h = v[1:]
        if not re.fullmatch(r"[0-9a-fA-F]+", h):
            return None
        if len(h) == 3:
            r, g, b = (int(c, 16) for c in h)
            return 0xFF000000 | ((r | r << 4) << 16) | ((g | g << 4) << 8) \
                | (b | b << 4)
        if len(h) == 6:
            return 0xFF000000 | int(h, 16)
        if len(h) == 8:
            return ((int(h[6:8], 16) << 24) | (int(h[0:2], 16) << 16)
                    | (int(h[2:4], 16) << 8) | int(h[4:6], 16))
        return None
    if v.startswith("0x"):
        return parse_hex(v)
    if v.startswith("rgba(") and v.endswith(")"):
        inner = v[5:-1].strip()
        if inner.count(",") == 3:
            p = [x.strip() for x in inner.split(",")]
            r, g, b = u8(p[0]), u8(p[1]), u8(p[2])
            try:
                a = alpha_floor(p[3])
            except ValueError:
                return None
            if None in (r, g, b):
                return None
            return (a << 24) | (r << 16) | (g << 8) | b
        if len(inner) == 8:
            x = parse_hex(inner)
            return None if x is None else (x >> 8) + 0x1000000 * (x & 0xFF)
        return None
    if v.startswith("rgb(") and v.endswith(")"):
        inner = v[4:-1].strip()
        if inner.count(",") == 2:
            r, g, b = (u8(x) for x in inner.split(","))
            if None in (r, g, b):
                return None
            return 0xFF000000 | (r << 16) | (g << 8) | b
        if len(inner) == 6:
            x = parse_hex(inner)
            return None if x is None else x + 0xFF000000
        return None
    if re.fullmatch(r"\d+", v) and int(v) < 2 ** 32:
        return int(v)
    return None


def gradient_text(declared, inherited=0):
    """Hyprland configHandleGradientSet: colours cleared, angle set only by a
    `deg` token (stoi prefix), kept otherwise."""
    cols, angle = [], inherited
    for tok in declared.split():
        if "deg" in tok:
            angle = stoi_prefix(tok[:tok.index("deg")])
            break
        c = grad_color(tok)
        if c is None:
            return None
        cols.append(c)
    if not cols:
        return None
    return " ".join("%x" % c for c in cols) + " %ddeg" % angle


def gap_text(declared):
    n = [int(x) for x in declared.split()]
    if len(n) == 1:
        n = n * 4
    elif len(n) == 2:
        n = [n[0], n[1], n[0], n[1]]
    elif len(n) == 3:
        n = [n[0], n[1], n[2], n[1]]
    return " ".join(str(x) for x in n[:4])


# ------------------------------------------------------------- reply bytes
def esc(s):
    out = []
    for ch in s:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def num(x):
    return ("%g" % x) if not float(x).is_integer() else "%d" % int(x)


def native_reply(key, rec, variant):
    """The compositor's own text for one getoption -j reply (HyprCtl.cpp)."""
    if rec is None:
        return "no such option\n"
    form = [f for f in FORMS5 if f in rec][0]
    v = rec[form]
    st = "true" if rec["set"] else "false"
    if form == "int":
        body = '"int": %d' % v
    elif form == "float":
        body = '"float": %f' % v
    elif form == "vec2":
        body = '"vec2": [%s,%s]' % (num(v[0]), num(v[1]))
    else:
        body = '"%s": "%s"' % (form, esc(v))
    text = '{"option": "%s", %s, "set": %s }' % (esc(key), body, st)
    pad = variant % 4
    if pad == 0:
        return text + "\n"
    if pad == 1:
        return text + "\n\n"
    if pad == 2:
        return "  " + text + "  \n"
    return "\n" + text + "\n"


# ---------------------------------------------------------------- judge
class Judge:
    """The fake compositor, held by the counter process outside the sandbox."""

    def __init__(self, table, sockpath, mode="ok"):
        self.table = table
        self.mode = mode
        self.log = []
        self.envs = []
        self.replies = {}
        outer = self

        class H(socketserver.StreamRequestHandler):
            def handle(self):
                try:
                    req = json.loads(self.rfile.readline())
                    argv = req["argv"]
                except (ValueError, KeyError, TypeError):
                    argv = ["<malformed>"]
                outer.log.append(list(argv))
                outer.envs.append((req.get("env"), req.get("stdin"))
                                  if isinstance(req, dict) else (None, None))
                self.wfile.write((json.dumps(outer.answer(argv)) + "\n")
                                 .encode())

        self.srv = socketserver.ThreadingUnixStreamServer(sockpath, H)
        self.thread = threading.Thread(target=self.srv.serve_forever,
                                       daemon=True)
        self.thread.start()

    def answer(self, argv):
        if len(argv) != 3 or argv[:2] != ["getoption", "-j"]:
            return {"rc": 0, "out": "bad request\n"}
        key = argv[2]
        kind, _, victim = self.mode.partition(":")
        if victim == key:
            if kind == "fail":
                return {"rc": 1, "out": "HYPRLAND_INSTANCE_SIGNATURE not set! "
                                        "(is hyprland running?)\n\n"}
            if kind == "bad":
                return {"rc": 0, "out": "{not json\n"}
            if kind == "huge":
                return {"rc": 0, "out": '{"option": "%s", "str": "%s", '
                                        '"set": true }\n'
                                        % (esc(key), "x" * 200000)}
            if kind == "typeset":
                return {"rc": 0, "out": '{"option": "%s", "int": 1, '
                                        '"set": "yes" }\n' % esc(key)}
            if kind == "typeint":
                return {"rc": 0, "out": '{"option": "%s", "int": "7", '
                                        '"set": true }\n' % esc(key)}
            if kind == "null":
                return {"rc": 0, "out": "null\n"}
            if kind == "noform":
                return {"rc": 0, "out": '{"option": "%s", "vec3": [1,2,3], '
                                        '"set": true }\n' % esc(key)}
        rec = self.table.get(key)
        variant = int(hashlib.sha256(key.encode()).hexdigest(), 16)
        out = native_reply(key, rec, variant)
        self.replies[key] = rec
        return {"rc": 0, "out": out}

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


STUB = r'''#!%(py)s
import json, os, socket, sys
here = os.path.dirname(os.path.abspath(__file__))
s = socket.socket(socket.AF_UNIX)
s.connect(open(os.path.join(here, "sockpath")).read().strip())
s.sendall((json.dumps({"argv": sys.argv[1:], "env": sorted(os.environ),
                       "stdin": os.readlink("/proc/self/fd/0")}) + "\n")
          .encode())
data = b""
while True:
    chunk = s.recv(65536)
    if not chunk:
        break
    data += chunk
r = json.loads(data)
sys.stdout.write(r["out"])
sys.exit(r["rc"])
'''


# ---------------------------------------------------------------- sandbox
def sandbox_cmd(argv, binds, cwd, path_env):
    cmd = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session",
           "--cap-drop", "ALL", "--ro-bind", "/usr", "/usr",
           "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
           "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev",
           "--tmpfs", "/tmp"]
    for p in binds:
        cmd += ["--ro-bind", p, p]
    cmd += ["--clearenv", "--setenv", "PATH", path_env, "--setenv", "HOME",
            "/nonexistent", "--chdir", cwd, "--"]
    return cmd + argv


def check_sandbox():
    p = subprocess.run(sandbox_cmd(["/usr/bin/true"], [], "/", "/usr/bin"),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise Setup("sandbox_unavailable bwrap rc=%d %s"
                    % (p.returncode, p.stderr.strip()[:120]))
    if not os.path.realpath(sys.executable).startswith("/usr/"):
        raise Setup("interpreter_outside_usr %s" % sys.executable)


def run_sandboxed(tool, scratch, argv, path_env, timeout=120):
    py = os.path.realpath(sys.executable)
    cmd = sandbox_cmd([py, "-I", tool, *argv], [scratch], scratch, path_env)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return None, "", "timeout"
    return p.returncode, p.stdout, p.stderr


def snapshot(home):
    out = []
    for root, dirs, files in os.walk(home):
        dirs.sort()
        for d in dirs:
            out.append((os.path.join(root, d), "dir"))
        for f in sorted(files):
            p = os.path.join(root, f)
            with open(p, "rb") as fh:
                out.append((p, hashlib.sha256(fh.read()).hexdigest()))
    return out


# ---------------------------------------------------------------- generator
BOOLS = ["yes, please :)", "true", "on", "1", "off", "false", "no", "0",
         "on # note", "yes"]
INTS = ["7", "-3", "0x10", "900", "0", "-1", "255", "12"]
FLOATS = ["0.60", "1.3700001", "2", "0.5", "0.25", "3"]
STRS = ["w123", "no such option", "Sans Mono", "dwindle", "a b  c", "x"]
WEIGHT_SPELL = ["bold", "BOLD", "Heavy", "normal", "thin", "UltraHeavy",
                "medium", "semibold"]
ANGLES = [None, "0deg", "45deg", "45.5deg", "90deg", "270deg"]
VEC2S = ["0 0", "1.5 2", "-3 4.25", "10 10"]


def colour_decl(rng, i, j):
    r, g, b = rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)
    a = rng.randint(0x10, 0xFF)
    which = (i + j) % 5
    if which == 0:
        return "rgba(%02x%02x%02x%02x)" % (r, g, b, a)
    if which == 1:
        return "rgba(%d,%d,%d,%s)" % (r, g, b, ALPHAS[(i + j) % len(ALPHAS)])
    if which == 2:
        return "rgb(%02x%02x%02x)" % (r, g, b)
    if which == 3:
        return "rgb(%d,%d,%d)" % (r, g, b)
    return "0x%02x%02x%02x%02x" % (a, r, g, b)


def grad_colour_decl(rng, i, j):
    """Gradient colour spellings a config FILE can carry (`#` starts a comment
    in hyprlang, so the `#rrggbb` forms ParserUtils accepts are not emitted)."""
    r, g, b = rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)
    a = rng.randint(0x10, 0xFF)
    which = (i + j) % 6
    if which == 0:
        return "rgba(%02x%02x%02x%02x)" % (r, g, b, a)
    if which == 1:
        return "rgba(%d,%d,%d,%s)" % (r, g, b, ALPHAS[(i + j) % len(ALPHAS)])
    if which == 2:
        return "rgb(%02x%02x%02x)" % (r, g, b)
    if which == 3:
        return "rgb(%d,%d,%d)" % (r, g, b)
    if which == 4:
        return "%d" % ((a << 24) | (r << 16) | (g << 8) | b)
    return "0x%02x%02x%02x%02x" % (a, r, g, b)


class Fixture:
    def __init__(self, rng, tag, i):
        self.rng, self.tag, self.i = rng, tag, i
        self.n = 0
        self.opts = {}
        self.lines = []

    def make(self, kind, quirk):
        self.n += 1
        rng, i = self.rng, self.i
        key = "opt%s%d:%s%d" % (self.tag, self.n, kind, self.n)
        pick = (lambda lst: lst[(i + self.n) % len(lst)]) if quirk \
            else (lambda lst: rng.choice(lst))
        o = dict(kind=kind, shadow=False)
        if kind == "bool":
            o.update(form="int", declared=pick(BOOLS))
        elif kind == "num":
            o.update(form="int", declared=pick(INTS))
        elif kind == "colour":
            o.update(form="int", declared=colour_decl(rng, i, self.n))
        elif kind == "float":
            o.update(form="float", declared=pick(FLOATS))
        elif kind == "str":
            o.update(form="str", declared=pick(STRS))
        elif kind == "grad":
            cols = [grad_colour_decl(rng, i, self.n + c)
                    for c in range(1 + (i + self.n) % 3)]
            ang = ANGLES[(i + self.n) % len(ANGLES)] if quirk \
                else rng.choice(ANGLES)
            o.update(form="custom", shape="gradient",
                     declared=" ".join(cols + ([ang] if ang else [])))
        elif kind == "ginh":
            cols = [grad_colour_decl(rng, i, self.n + c)
                    for c in range(1 + (i + self.n) % 2)]
            o.update(form="custom", shape="gradient",
                     declared=" ".join(cols),
                     prior=(45, 90, 135, 270)[(i + self.n) % 4], shadow=True)
        elif kind == "gap":
            cnt = 1 + (i + (0 if quirk else 1)) % 4
            o.update(form="custom", shape="gap",
                     declared=" ".join(str(rng.randint(0, 40))
                                       for _ in range(cnt)))
        elif kind == "weight":
            o.update(form="custom", shape="weight",
                     declared=pick(WEIGHT_SPELL))
        else:
            o.update(form="vec2", declared=pick(VEC2S))
        return key, o

    def live_of(self, o):
        f, d = o["form"], o["declared"]
        if f == "int":
            return hl_int(d.strip())
        if f == "float":
            return float("%f" % float(d))
        if f == "str":
            return d
        if f == "vec2":
            x, y = d.split(" ")
            return [float(x), float(y)]
        if o["shape"] == "gradient":
            return gradient_text(d, o.get("prior", 0))
        if o["shape"] == "gap":
            return gap_text(d)
        return str(WEIGHTS[d.lower()])

    def perturb(self, o, live):
        f = o["form"]
        if f == "int":
            return live + 1
        if f == "float":
            return float("%f" % (live + 0.5))
        if f == "str":
            return live + "9"
        if f == "vec2":
            return [live[0] + 1, live[1]] if self.i % 2 else \
                [live[0], live[1] + 1]
        if o["shape"] == "gradient":
            return live.replace("deg", "7deg")
        if o["shape"] == "gap":
            return live + " 1"
        return str(int(live) + 1)

    def build(self):
        rng = self.rng
        kinds = ["bool", "num", "colour", "float", "str", "grad", "gap",
                 "weight", "ginh", "vec2"]
        second = ["differ", "differ", "unset", "unset", "absent", "absent"]
        rng.shuffle(second)
        second_kinds = rng.sample([k for k in kinds if k != "ginh"], 6)
        plan = [(k, True, "agree") for k in kinds]
        plan += [(k, False, lab) for k, lab in zip(second_kinds, second)]
        rng.shuffle(plan)
        for kind, quirk, lab in plan:
            key, o = self.make(kind, quirk)
            o["decls"] = 2 if o["shadow"] else 1
            o["lab"] = lab
            live = self.live_of(o)
            o["live"] = live if lab in ("agree", "unset") else (
                self.perturb(o, live) if lab == "differ" else None)
            self.opts[key] = o
        extra = [k for k, o in self.opts.items()
                 if o["lab"] == "agree" and o["decls"] == 1][:2]
        for k in extra:
            self.opts[k]["decls"] = 2
        self.lines = []
        for k, o in self.opts.items():
            cat, name = k.split(":")
            if o["decls"] == 2:
                early = ("rgba(11223344) %ddeg" % o["prior"]
                         if o["shadow"] else "0x1")
                self.lines += ["%s {" % cat, "    %s = %s" % (name, early),
                               "}"]
            self.lines += ["%s {" % cat, "    %s = %s" % (name, o["declared"]),
                           "}"]
        self.lines += ["bind = SUPER, Q, killactive",
                       "env = XCURSOR_SIZE,24", "# general:zzcomment = 1"]

    def table(self):
        t = {}
        for k, o in self.opts.items():
            if o["lab"] == "absent":
                continue
            t[k] = {o["form"]: o["live"], "set": o["lab"] != "unset"}
        return t

    def want(self):
        w = {}
        for k, o in self.opts.items():
            if o["lab"] == "absent":
                w[k] = "config-only"
            elif o["lab"] in ("unset", "differ"):
                w[k] = "mismatch"
            else:
                w[k] = "agreement*" if o["decls"] > 1 else "agreement"
        return w

    def render(self, home):
        path = os.path.join(home, ".config", "hypr", "hyprland.conf")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self.lines) + "\n")


def fixture_for(rev, nonce, tag, i):
    seed = int(hashlib.sha256(("%s:%s:%s:%d" % (rev, nonce, tag, i))
                              .encode()).hexdigest(), 16)
    fx = Fixture(random.Random(seed), tag, i)
    fx.build()
    return fx


# ----------------------------------------------------------------- scoring
class Run:
    """One fixture environment: scratch tree, judge, stub, sandboxed tool."""

    def __init__(self, tmp, name, tool, fx, mode="ok", extra_table=None):
        self.tmp, self.name, self.tool, self.fx = tmp, name, tool, fx
        self.root = os.path.join(tmp, name)
        os.makedirs(self.root)
        self.home = os.path.join(self.root, "home")
        fx.render(self.home)
        self.bin = os.path.join(self.root, "bin")
        os.makedirs(self.bin)
        self.sock = os.path.join(self.root, "s.sock")
        table = fx.table()
        table.update(extra_table or {})
        self.judge = Judge(table, self.sock, mode)
        with open(os.path.join(self.bin, "hyprctl"), "w") as fh:
            fh.write(STUB % {"py": os.path.realpath(sys.executable)})
        os.chmod(os.path.join(self.bin, "hyprctl"), 0o755)
        with open(os.path.join(self.bin, "sockpath"), "w") as fh:
            fh.write(self.sock)
        self.before = snapshot(self.home)

    def run(self, extra):
        py = os.path.realpath(sys.executable)
        cmd = sandbox_cmd([py, "-I", self.tool, "--home", self.home, *extra],
                          [self.root, os.path.dirname(self.tool)], self.root,
                          self.bin + ":/usr/bin")
        try:
            p = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=60, env=ENV)
        except subprocess.TimeoutExpired:
            return None, "", "timeout"
        return p.returncode, p.stdout, p.stderr

    def stub(self):
        return os.path.join(self.bin, "hyprctl")

    def unchanged(self):
        return snapshot(self.home) == self.before

    def close(self):
        self.judge.close()


def norm_tokens(v):
    if isinstance(v, (list, tuple)):
        v = " ".join(str(x) for x in v)
    s = re.sub(r"[\[\],]", " ", str(v))
    return s.split()


def live_matches(row_live, sent):
    if not isinstance(row_live, str):
        return False
    a = norm_tokens(row_live)
    b = norm_tokens(sent)
    if a == b:
        return True
    try:
        return [float(x) for x in a] == [float(x) for x in b]
    except ValueError:
        return False


def sent_value(rec):
    form = [f for f in FORMS5 if f in rec][0]
    return rec[form]


def valid_run(tool, tmp, name, fx, probes=(), extra_table=None, flags=()):
    """Valid live run; returns (ok, why, run). Caller closes the run."""
    run = Run(tmp, name, tool, fx, extra_table=extra_table)
    extra = list(flags)
    if "--hyprctl" not in extra:
        extra += ["--hyprctl", run.stub()]
    extra = ["--live"] + extra
    for p in probes:
        extra += ["--probe", p]
    rc, out, err = run.run(extra)
    if rc != 0:
        return False, "rc=%s err=%s" % (rc, err.strip()[:80]), run
    try:
        rows = json.loads(out)
    except ValueError:
        return False, "stdout is not JSON", run
    if not run.unchanged():
        return False, "config root modified", run
    want = fx.want()
    for k in (extra_table or {}):
        want[k] = "live-default"
    keys = [r.get("key") for r in rows]
    if keys != sorted(want):
        return False, "rows %d vs expected %d (dup/missing/unsorted)" % (
            len(keys), len(want)), run
    bad = [r["key"] for r in rows if r.get("agreement") != want[r["key"]]]
    if bad:
        r0 = [r for r in rows if r["key"] == bad[0]][0]
        return False, "labels differ at %s (got=%s want=%s)" % (
            bad[:3], r0.get("agreement"), want[bad[0]]), run
    expect = set(k for k in want if want[k] != "config-only") \
        | set(extra_table or {})
    asked = [a[2] for a in run.judge.log
             if len(a) == 3 and a[:2] == ["getoption", "-j"]]
    expected_asks = sorted(set(fx.opts) | set(probes))
    if len(asked) != len(run.judge.log) or sorted(asked) != expected_asks \
            or len(asked) != len(set(asked)):
        return False, "requests %s" % run.judge.log[:2], run
    allowed = {"PATH", "HYPRLAND_INSTANCE_SIGNATURE", "XDG_RUNTIME_DIR",
               "LC_CTYPE"}
    for env, stdin in run.judge.envs:
        if env is None or not set(env) <= allowed or stdin != "/dev/null":
            return False, "child env %s stdin %s" % (env, stdin), run
    table = dict(fx.table())
    table.update(extra_table or {})
    for r in rows:
        if r["agreement"] == "config-only":
            continue
        rec = table.get(r["key"])
        if rec is None or not live_matches(r.get("live"), sent_value(rec)):
            return False, "row %s live=%r sent=%r" % (
                r["key"], r.get("live"), rec and sent_value(rec)), run
    return True, "rows=%d" % len(rows), run


def score_generated(tool, tmp, rev, nonce, i):
    fx = fixture_for(rev, nonce, "g", i)
    ok, why, run = valid_run(tool, tmp, "g%d" % i, fx)
    run.close()
    return ok, why


def probe_extra():
    return {"aaprobe:first": {"float": 0.5, "set": False},
            "zzprobe:one": {"int": 3, "set": False},
            "zzprobe:two": {"str": "q", "set": False},
            "zzprobe:vec": {"vec2": [0, 0], "set": False}}


def score_probe(tool, tmp, rev, nonce):
    fx = fixture_for(rev, nonce, "probe", 0)
    declared = sorted(fx.opts)[0]
    probes = ("zzprobe:one", "zzprobe:two", "zzprobe:vec", "zzprobe:one",
              "aaprobe:first", declared, "zzprobe:nothing")
    # the declared key and the duplicate are asked once each; the
    # undeclared unknown one answers `no such option` and yields no row
    run = Run(tmp, "p0", tool, fx, extra_table=probe_extra())
    rc, out, err = run.run(["--live", "--hyprctl", run.stub()] +
                           [x for p in probes for x in ("--probe", p)])
    try:
        rows = json.loads(out) if rc == 0 else None
    except ValueError:
        rows = None
    try:
        if rows is None:
            return False, "rc=%s err=%s" % (rc, err.strip()[:80])
        want = fx.want()
        for k in probe_extra():
            want[k] = "live-default"
        keys = [r["key"] for r in rows]
        asked = [a[2] for a in run.judge.log if len(a) == 3]
        ok = (keys == sorted(want)
              and {r["key"]: r["agreement"] for r in rows} == want
              and sorted(asked) == sorted(set(fx.opts) | set(probes))
              and len(asked) == len(set(asked)) == len(run.judge.log)
              and run.unchanged())
        return ok, "rows=%d asked=%d" % (len(keys), len(asked))
    finally:
        run.close()


def score_default_lookup(tool, tmp, rev, nonce):
    fx = fixture_for(rev, nonce, "path", 0)
    run = Run(tmp, "d0", tool, fx)
    try:
        rc, out, err = run.run(["--live"])
        if rc != 0:
            return False, "rc=%s err=%s" % (rc, err.strip()[:80])
        rows = json.loads(out)
        want = fx.want()
        ok = ({r["key"]: r["agreement"] for r in rows} == want
              and run.unchanged())
        return ok, "rows=%d" % len(rows)
    finally:
        run.close()


def score_failure(tool, tmp, rev, nonce, kind, probe=False):
    tag = kind + ("p" if probe else "")
    fx = fixture_for(rev, nonce, tag, 1)
    ok, why, run = valid_run(tool, tmp, tag + "-ok", fx)
    run.close()
    if not ok:
        return False, "valid run: " + why
    victim = "zzfail:probe" if probe else sorted(fx.opts)[3]
    extra_t = {"zzfail:probe": {"int": 1, "set": False}} if probe else {}
    run = Run(tmp, tag + "-bad", tool, fx, mode="%s:%s" % (kind, victim),
              extra_table=extra_t)
    try:
        extra = ["--live", "--hyprctl", run.stub()]
        if probe:
            extra += ["--probe", victim]
        rc, out, err = run.run(extra)
        others = [k for k in list(fx.opts) if k != victim and k in err]
        named = victim in err and not others
        good = (rc == 5 and named and run.unchanged()
                and all(len(a) == 3 and a[:2] == ["getoption", "-j"]
                        for a in run.judge.log))
        return good, "rc=%s named=%d others=%d" % (rc, victim in err,
                                                    len(others))
    finally:
        run.close()


def score_missing(tool, tmp, rev, nonce):
    fx = fixture_for(rev, nonce, "missing", 1)
    ok, why, run = valid_run(tool, tmp, "m0", fx)
    run.close()
    if not ok:
        return False, "valid run: " + why
    run = Run(tmp, "m1", tool, fx)
    try:
        gone = os.path.join(run.root, "no-such-dir", "hyprctl")
        rc, out, err = run.run(["--live", "--hyprctl", gone])
        return (rc == 5 and "hyprctl" in err and run.unchanged()
                and not run.judge.log), "rc=%s" % rc
    finally:
        run.close()


def score_hostile(tool, tmp, rev, nonce):
    fx = fixture_for(rev, nonce, "hostile", 1)
    ok, why, run = valid_run(tool, tmp, "h0", fx)
    run.close()
    if not ok:
        return False, "valid run: " + why
    run = Run(tmp, "h1", tool, fx)
    good = True
    try:
        for argv in (["--probe=-x"], ["--probe=-1"], ["--probe=--version"],
                     ["--probe="], ["--probe", ""], ["--probe", "-x"],
                     ["--probe=a/--batch"], ["--probe=a b"],
                     ["--probe=a;dispatch"], ["--getoption", "/dev/null"]):
            n0 = len(run.judge.log)
            rc, out, err = run.run(["--live", "--hyprctl", run.stub()] + argv)
            good &= (rc == 2 and ("probe" in err.lower()
                                  or "getoption" in err.lower())
                     and len(run.judge.log) == n0 and run.unchanged())
        return good, "all ten refused=%d" % good
    finally:
        run.close()


def score_hostile_key(tool, tmp, rev, nonce):
    """A hostile key DECLARED in the config tree must never reach argv."""
    fx = fixture_for(rev, nonce, "hostilekey", 1)
    ok, why, run = valid_run(tool, tmp, "k0", fx)
    run.close()
    if not ok:
        return False, "valid run: " + why
    run = Run(tmp, "k1", tool, fx)
    try:
        with open(os.path.join(run.home, ".config", "hypr", "hyprland.conf"),
                  "a") as fh:
            fh.write("zzbad {\n    x/--batch = 1\n    y;dispatch = 2\n}\n")
        run.before = snapshot(run.home)
        rc, out, err = run.run(["--live", "--hyprctl", run.stub()])
        good = (rc == 2 and "x/--batch" in err and not run.judge.log
                and run.unchanged())
        return good, "rc=%s named=%d requests=%d" % (
            rc, "x/--batch" in err, len(run.judge.log))
    finally:
        run.close()


def score_writable(tool, tmp, rev, nonce):
    """A world-writable compositor program, and a directory, are refused."""
    fx = fixture_for(rev, nonce, "writable", 1)
    ok, why, run = valid_run(tool, tmp, "w0", fx)
    run.close()
    if not ok:
        return False, "valid run: " + why
    run = Run(tmp, "w1", tool, fx)
    try:
        os.chmod(run.stub(), 0o777)
        rc1, out, err1 = run.run(["--live", "--hyprctl", run.stub()])
        rc2, out, err2 = run.run(["--live", "--hyprctl", run.bin])
        good = (rc1 == 5 and "hyprctl" in err1 and rc2 == 5
                and not run.judge.log and run.unchanged())
        return good, "rc=%s,%s requests=%d" % (rc1, rc2, len(run.judge.log))
    finally:
        run.close()


def score_reply_limits(tool, tmp, rev, nonce):
    """Oversized and mistyped replies exit 5 naming exactly the key."""
    fx = fixture_for(rev, nonce, "limits", 1)
    ok, why, run = valid_run(tool, tmp, "l0", fx)
    run.close()
    if not ok:
        return False, "valid run: " + why
    victim = sorted(fx.opts)[2]
    good, notes = True, []
    for kind in ("huge", "typeset", "typeint", "null"):
        run = Run(tmp, "l-" + kind, tool, fx, mode="%s:%s" % (kind, victim))
        try:
            rc, out, err = run.run(["--live", "--hyprctl", run.stub()])
            others = [k for k in fx.opts if k != victim and k in err]
            this = (rc == 5 and victim in err and not others
                    and "Traceback" not in err and run.unchanged())
            good &= this
            notes.append("%s=%d" % (kind, this))
        finally:
            run.close()
    return good, " ".join(notes)


# ------------------------------------------------------------------ clauses
def imports_ok(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0])
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in CALL_DENY:
                return False
            if (isinstance(f, ast.Attribute) and f.attr in CALL_DENY
                    and isinstance(f.value, ast.Name)
                    and f.value.id in ("builtins", "__builtins__")):
                return False
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if any(s in node.value for s in STR_DENY):
                return False
    return bool(mods) and mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)


def capture_ok(blob, n_lines, forms_needed):
    if blob is None:
        return False
    lines = [l for l in blob.decode("utf-8", "replace").splitlines()
             if l.strip()]
    if len(lines) != n_lines:
        return False
    seen = set()
    for l in lines:
        try:
            o = json.loads(l)
        except ValueError:
            return False
        forms = [k for k in o if k in FORMS5]
        if "option" not in o or "set" not in o or len(forms) != 1:
            return False
        seen.add(forms[0])
    return seen == set(forms_needed)


def selftest_result(tool, scratch):
    rc, out, err = run_sandboxed(tool, scratch, ["--selftest"], "/usr/bin",
                                 timeout=300)
    m = re.search(r"MADO_OPTIONS_SELFTEST: (\d+)/(\d+) passed", out or "")
    k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return rc, k, n, m is not None


NOT_SITES = ("selftest", "_check", "_run", "_write", "main", "usage")
FLIP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE,
        ast.GtE: ast.Lt, ast.Gt: ast.LtE, ast.LtE: ast.Gt, ast.In: ast.NotIn,
        ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}


def new_function_sites(src, base_src):
    tree = ast.parse(src)
    base_names = set()
    if base_src:
        base_names = {n.name for n in ast.walk(ast.parse(base_src))
                      if isinstance(n, ast.FunctionDef)}
    sites = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name in base_names or any(s in fn.name for s in NOT_SITES):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 \
                    and type(node.ops[0]) in FLIP:
                sites.append((fn.name, node.lineno, node.col_offset))
    return sorted(set(sites))


def mutate_source(src, site):
    tree = ast.parse(src)
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name != site[0]:
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 \
                    and (node.lineno, node.col_offset) == site[1:] \
                    and type(node.ops[0]) in FLIP:
                node.ops[0] = FLIP[type(node.ops[0])]()
                return ast.unparse(tree)
    return None


def teeth(src, base_src, tmp, nonce):
    sites = new_function_sites(src, base_src)
    if len(sites) < MIN_SITES:
        print("%s clause=b2 sites=%d (<%d)" % (PRED, len(sites), MIN_SITES))
        return False
    rng = random.Random(int(hashlib.sha256(("mut:" + nonce).encode())
                            .hexdigest(), 16))
    chosen = rng.sample(sites, N_MUT)
    killed = 0
    for n, site in enumerate(chosen):
        mutated = mutate_source(src, site)
        if mutated is None:
            continue
        d = os.path.join(tmp, "mut%d" % n)
        os.makedirs(d)
        path = os.path.join(d, "mado-options.py")
        with open(path, "w") as fh:
            fh.write(mutated)
        rc, k, n_, has = selftest_result(path, d)
        dead = rc != 0 or not has or k < n_
        killed += dead
        print("%s clause=b2 mutant=%d site=%s:%d killed=%d" % (
            PRED, n, site[0], site[1], dead))
    print("%s clause=b2 sites=%d killed=%d/%d" % (PRED, len(sites), killed,
                                                  N_MUT))
    return killed >= KILL_NEED


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--tool", default=None,
                    help="score this file instead of REV's tool (controls)")
    ap.add_argument("--nonce", default=None)
    args = ap.parse_args()
    nonce = args.nonce or secrets.token_hex(8)
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    check_sandbox()
    base_src = git(repo, "show", "%s:%s" % (base, TOOL))
    if base_src is not None and b"--live" in base_src:
        raise Setup("precondition_failed live_present_at_base")
    src = open(args.tool, "rb").read() if args.tool else \
        git(repo, "show", "%s:%s" % (rev, TOOL))
    present = src is not None
    cl = {"a": int(present), "b": 0, "b2": 0, "g": 0,
          "k": int(capture_ok(git(repo, "show", "%s:%s" % (rev, CAPTURE)),
                              70, FORMS)),
          "k2": int(capture_ok(git(repo, "show", "%s:%s" % (rev, CAPTURE_ALL)),
                               353, FORMS5))}
    passed = 0
    if present:
        cl["g"] = int(imports_ok(src))
        tmp = tempfile.mkdtemp(prefix="mado-c1v2-")
        os.chmod(tmp, 0o755)
        try:
            td = os.path.join(tmp, "tool")
            os.makedirs(td)
            tool = os.path.join(td, "mado-options.py")
            with open(tool, "wb") as fh:
                fh.write(src)
            rc, k, n, has = selftest_result(tool, td)
            cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)
            print("%s clause=b rc=%s selftest=%d/%d" % (PRED, rc, k, n))
            if cl["b"]:
                cl["b2"] = int(teeth(src.decode("utf-8", "replace"),
                                     base_src.decode("utf-8", "replace")
                                     if base_src else None, tmp, nonce))
            for i in range(N_GEN):
                ok, why = score_generated(tool, tmp, rev, nonce, i)
                passed += ok
                print("%s fixture=gen%d ok=%d %s" % (PRED, i, ok, why))
            for name, fn in (
                    ("probe0", lambda: score_probe(tool, tmp, rev, nonce)),
                    ("path0", lambda: score_default_lookup(tool, tmp, rev,
                                                           nonce)),
                    ("fail0", lambda: score_failure(tool, tmp, rev, nonce,
                                                    "fail")),
                    ("bad0", lambda: score_failure(tool, tmp, rev, nonce,
                                                   "bad")),
                    ("noform0", lambda: score_failure(tool, tmp, rev, nonce,
                                                      "noform")),
                    ("probefail0", lambda: score_failure(tool, tmp, rev,
                                                         nonce, "fail", True)),
                    ("missing0", lambda: score_missing(tool, tmp, rev, nonce)),
                    ("hostile0", lambda: score_hostile(tool, tmp, rev,
                                                       nonce)),
                    ("hostilekey0", lambda: score_hostile_key(tool, tmp, rev,
                                                              nonce)),
                    ("writable0", lambda: score_writable(tool, tmp, rev,
                                                         nonce)),
                    ("limits0", lambda: score_reply_limits(tool, tmp, rev,
                                                           nonce))):
                ok, why = fn()
                passed += ok
                print("%s fixture=%s ok=%d %s" % (PRED, name, ok, why))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    met = all(cl.values()) and passed == TOTAL
    print("%s clauses=%s" % (PRED, " ".join("%s:%d" % kv
                                             for kv in sorted(cl.items()))))
    print("%s: fixtures=%d/%d tool=%s verdict=%s rev=%s nonce=%s" % (
        PRED, passed, TOTAL, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", rev, nonce))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)

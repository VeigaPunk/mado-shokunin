#!/usr/bin/env python3
"""PRED-C1-r42 - a read-only join of window-rule sizes and the compositor's reported client sizes (C1, operability).

Scores one committed revision REV of the lane (revision-addressed git reads, ambient GIT_*
removed; nothing in the lane is written). The tool under test is `tools/mado-geometry.py` at REV
(or `--tool PATH` for a control); BASE must lack it. Every tool and selftest run happens inside a
bubblewrap sandbox (`bwrap --unshare-all --cap-drop ALL`, fresh /proc and /dev, tmpfs /tmp, the
interpreter's /usr read-only, the fixture tree read-only): the tool sees neither the lane, nor this
counter, nor /home; fixture runs also execute under RLIMIT_NPROC = 1, so any spawn fails. No bwrap ->
SETUP, exit 2. Fixtures mix a per-run nonce: sha256(REV:NONCE:tag:i); the nonce is printed and
replayable with `--nonce`. Fixture directories have opaque random names.

The tool's contract is the docstring of the reference at `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`
(frozen at the round-42 freeze) and is restated here, the code below being the same sentence.

CLI. `mado-geometry.py --selftest`, or `--clients V` exactly once and `--rules V` one or more times
(two-token form only, any order); anything else is usage. Setup failure: stdout is exactly one line
`MADO_GEOMETRY: SETUP <reason>`, exit 2, reason one of usage | unreadable | too_large | bad_json. A
PATH that is missing, unreadable, a directory, a FIFO or any non-regular file is unreadable (the tool
must return, never block on one); an input larger than 1048576 bytes is too_large; `--clients -` reads
standard input, at most 1048577 bytes; a clients input that is not UTF-8 JSON holding a list whose
every element is an object is bad_json (an empty input included). Order of checks: usage, then the
clients input (unreadable, too_large, bad_json), then the rules files in argument order
(unreadable, too_large).

Rules. Each rules file is decoded as UTF-8 with errors replaced and split on "\\n"; a line is
stripped of spaces and tabs at both ends. A RULE LINE fully matches `windowrule[ \\t]*=(.*)` (every
other line, `windowrulev2` and upper case `WindowRule` included, is ignored and counted nowhere). The
body is split on "," and each field is stripped of spaces and tabs. The effect is the first
first token of field 0, tokens being separated by runs of spaces and tabs only (the empty string when there is none). An effect other than
`size` and `float` adds one to `other`. A `size` or `float` line is SUPPORTED when: it has exactly
two fields; field 0 has exactly two argument tokens fully matching
`[0-9]{1,5}` (ASCII digits; size) or exactly one token equal to `on` or `off` (float); field 1 fully
matches `match:class[ \\t]+(.+)`, the capture being REGEX; REGEX fully matches 1-200 characters of
`[A-Za-z0-9_.^$()|*+?-]` and the escapes `\\.` `\\-` `\\(` `\\)` `\\|` `\\*` `\\+` `\\?` `\\^` `\\$`
`\\\\`; contains none of the substrings `(?`, `*+`, `++`, `?+`; and compiles under Python `re`. Any
other size or float line adds one to `unsupported`. Supported rules are numbered n=1.. across all
files in argument order; each carries the 1-based index of its file. A client MATCHES a rule when
its class holds no character below U+0020 and `re.fullmatch(REGEX, class)` succeeds.

Clients. An element whose `mapped` is JSON false is unmapped and skipped (0, null and "false"
are not false). For the others: class is the `class` value when a string, else the empty string;
floating is true only for JSON true; size is the `size` value when a list of exactly two JSON
integers (not booleans, not floats) that are >= 0, else none; address is the `address` value
when a string, else "-". Rules apply in file order: the last matching `size` rule gives want, the
last matching `float` rule gives float_rule (`on`, `off`, else `-`). A client with at least one
matching size rule is MATCHED and has a verdict: BADSIZE (size none) | TILED (not floating) |
AGREE (size == want) | DIFFER. A duplicate JSON key keeps its last value.

Output, in order (stdout, one line each; nothing else; stderr empty on exit 0/1/3/4):
  per supported rule (rule order)    MADO_GEOM_RULE: n=<n> file=<k> effect=<size|float> arg=<WxH|on|off> class=<REGEX>
  per matched client (input order)   MADO_GEOM_CLIENT: addr=<json> class=<json> floating=<true|false> size=<WxH|-> want=<WxH> float_rule=<on|off|-> verdict=<V>
  last                               MADO_GEOMETRY: rules=<size rules> float_rules=<n> other=<n> unsupported=<n> clients=<mapped> matched=<n> unmapped=<n> agree=<n> differ=<n> tiled=<n> badsize=<n> verdict=<V>
`<json>` is json.dumps(value) with ensure_ascii; WxH are decimal integers without leading zeros.
V = NO_SIZE_RULES (rules=0; exit 4) | DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT (matched=0;
exit 3) | OK (exit 0), tested in that order.

Fixtures (P of TOTAL): gen0..gen9 (a nonce lattice: 1-3 rules files of mixed supported, unsupported,
other and ignored lines; 0-14 clients of mixed classes, sizes, floating and mapped values) and the
fixed classes stdin0, stdinbig0, stdinok0, filecl0, multi0, usage0, unreadable0, fifo0, toolarge0,
boundary0, badjson0, nan0, regex0, size0, float0, space0, ignore0, other0, order0, client0,
sizevals0, mapped0, dupkeys0, ctlclass0, unicode0, many0, empty0, plus the b-clauses below. Each
fixture compares rc and stdout byte-exactly with the judge's model; on rc 0/1/3/4 stderr must be empty.

Cost bound: a run that hits 3 timeouts (30 s each; 60 s for a selftest) is not run any further, and every
remaining fixture and selftest fails.

Clauses: a  the tool exists at REV and BASE lacks it; b  `--selftest` (in the sandbox) exits 0 printing
`MADO_GEOMETRY_SELFTEST: k/n passed`, k == n and n >= 50; b2  the selftest has teeth: from the tool's
functions (all but the function named exactly selftest, main or usage, and functions defined inside
selftest) >= 12 comparison sites exist; 6 are chosen by the nonce, one of them forced into a
function whose body contains the text `MADO_GEOMETRY: rules=` (which must have a site); each is
flipped in a copy placed at the same layout as the real tool, and the copy's selftest fails (non-zero,
k != n, or no summary) for the forced site and for >= 3 of the other 5; b3  the selftest is neutral
to edits that do not change behaviour: the tool with a trailing comment appended, and re-printed by
`ast.unparse` with one extra assignment appended, each still passes its selftest in full; g
top-level imports are standard library only (json os re stat sys), none of socket urllib http
requests ssl ctypes importlib pty subprocess is imported, the source calls none of exec, eval,
compile, __import__, getattr, setattr, delattr, vars, globals, locals, breakpoint (as a name or on
builtins), os.system, os.popen, os.exec*, passes no `shell=True` and no `**` keyword unpacking to any
call, never names `__file__`, `sys.argv[0]`, `sys.executable` or `sys.modules`, has no string
constant equal to exec, eval, compile, __import__, system, popen, builtins, __builtins__ or
__file__, and names no `/proc`, `c1-r42` or `quality/counters` string.

Final line: `PRED-C1-r42: fixtures=P/TOTAL tool=present|absent verdict=TARGET_MET|TARGET_MISSED
rev=<full hash> nonce=<hex>`. TARGET_MET iff a, b, b2, b3, g hold and P == TOTAL; exit 0, else exit 1.
Residual (declared): a tool that CONTAINS a model of this contract is an implementation; clause g is a
heuristic over names; the sandbox is detectable (fresh /proc, HOME=/nonexistent); Python `re` is not
RE2 - the REGEX alphabet is restricted so the two agree on it, and a regex outside it is `unsupported`,
never evaluated; whether Hyprland applies a rule's size to a live window is a compositor fact this
counter does not score (the host receipt, `hyprctl clients -j` piped in, is reported, not scored).
"""
import argparse
import ast
import hashlib
import json
import os
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C1-r42"
BASE_DEFAULT = "62dd798bb08401a8697383552edcc36f109344fa"
TOOL = "tools/mado-geometry.py"
TOTAL = 37
MIN_SELFTEST = 50
MIN_SITES = 12
N_MUT = 6
KILL_NEED = 4
MAX_BYTES = 1048576
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
NONCE = [""]
TIMEOUTS = [0]
STDLIB_ALLOW = {"json", "os", "re", "stat", "sys"}
STDLIB_DENY = {"socket", "urllib", "http", "requests", "ssl", "ctypes",
               "importlib", "pty", "subprocess"}
CALL_DENY = {"exec", "eval", "compile", "__import__"}
OS_DENY = {"system", "popen", "execv", "execve", "execvp", "execl", "execle",
           "execlp", "execvpe", "execlpe", "spawnl", "spawnv", "posix_spawn"}
STR_DENY = ("/proc", "c1-r42", "quality/counters")
NAME_DENY = {"getattr", "setattr", "delattr", "vars", "globals", "locals",
             "breakpoint", "__file__"}
STR_EQ_DENY = {"exec", "eval", "compile", "__import__", "system", "popen",
               "builtins", "__builtins__", "__file__"}
SAFE_RE = re.compile(r"(?:[A-Za-z0-9_.^$()|*+?-]|\\[.\-()|*+?^$\\]){1,200}")
RULE_RE = re.compile(r"windowrule[ \t]*=(.*)")
MATCH_RE = re.compile(r"match:class[ \t]+(.+)")
NUM_RE = re.compile(r"[0-9]{1,5}")


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


# ---------------------------------------------------------------- sandbox
def sandbox_cmd(argv, ro, rw, cwd, path_env, extra_env):
    cmd = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session",
           "--cap-drop", "ALL", "--ro-bind", "/usr", "/usr",
           "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64", "/lib64",
           "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev",
           "--tmpfs", "/tmp"]
    for p in ro:
        cmd += ["--ro-bind", p, p]
    for p in rw:
        cmd += ["--bind", p, p]
    cmd += ["--clearenv", "--setenv", "PATH", path_env, "--setenv", "HOME",
            "/nonexistent"]
    for k, v in sorted(extra_env.items()):
        cmd += ["--setenv", k, v]
    cmd += ["--chdir", cwd, "--"]
    return cmd + argv


def check_sandbox():
    try:
        p = subprocess.run(sandbox_cmd(["/usr/bin/true"], [], [], "/",
                                       "/usr/bin", {}), capture_output=True,
                           text=True)
    except OSError as exc:
        raise Setup("sandbox_unavailable bwrap %s" % exc)
    if p.returncode != 0:
        raise Setup("sandbox_unavailable bwrap rc=%d %s"
                    % (p.returncode, p.stderr.strip()[:120]))
    if not os.path.realpath(sys.executable).startswith("/usr/"):
        raise Setup("interpreter_outside_usr %s" % sys.executable)
    for prog in ("/usr/bin/prlimit",):
        if not os.access(prog, os.X_OK):
            raise Setup("missing_program %s" % prog)


def run_piped(cmd, timeout):
    """stdin is an open, empty pipe (never /dev/null), so a child that does
    not redirect its own children's stdin is visible to the stub."""
    r, w = os.pipe()
    try:
        return subprocess.run(cmd, capture_output=True, timeout=timeout,
                              env=ENV, stdin=r)
    finally:
        os.close(r)
        os.close(w)


def run_sandboxed(tool, scratch, argv, path_env, ro=(), rw=(), cwd=None,
                  extra_env=None, timeout=120, nproc=False):
    """nproc: run the tool under RLIMIT_NPROC = 1 (any fork/exec fails)."""
    py = os.path.realpath(sys.executable)
    lead = ["/usr/bin/prlimit", "--nproc=1:1"] if nproc else []
    cmd = sandbox_cmd(lead + [py, "-I", tool, *argv], [scratch, *ro],
                      list(rw), cwd or scratch, path_env, extra_env or {})
    if TIMEOUTS[0] >= 3:
        return None, b"", b"skipped after 3 timeouts"
    try:
        p = run_piped(cmd, timeout)
    except subprocess.TimeoutExpired:
        TIMEOUTS[0] += 1
        return None, b"", b"timeout"
    return p.returncode, p.stdout, p.stderr


# ------------------------------------------------------------- the model
def regex_valid(rx):
    if SAFE_RE.fullmatch(rx) is None:
        return False
    if any(s in rx for s in ("(?", "*+", "++", "?+")):
        return False
    try:
        re.compile(rx)
    except re.error:
        return False
    return True


def model_rules(texts):
    """-> (rules, other, unsupported). A rule is (file, effect, arg, want, rx)."""
    rules, other, unsup = [], 0, 0
    for fno, text in enumerate(texts, 1):
        for raw in text.split("\n"):
            line = raw.strip(" \t")
            m = RULE_RE.fullmatch(line)
            if m is None:
                continue
            body = m.group(1)
            fields = [f.strip(" \t") for f in body.split(",")]
            words = [w for w in re.split("[ \t]+", fields[0]) if w]
            effect = words[0] if words else ""
            if effect not in ("size", "float"):
                other += 1
                continue
            args = words[1:]
            ok = len(fields) == 2
            if ok and effect == "size":
                ok = len(args) == 2 and all(NUM_RE.fullmatch(a) for a in args)
            elif ok:
                ok = len(args) == 1 and args[0] in ("on", "off")
            mm = MATCH_RE.fullmatch(fields[1]) if ok else None
            if mm is None or not regex_valid(mm.group(1)):
                unsup += 1
                continue
            if effect == "size":
                want = (int(args[0]), int(args[1]))
                arg = "%dx%d" % want
            else:
                want, arg = args[0], args[0]
            rules.append((fno, effect, arg, want, mm.group(1)))
    return rules, other, unsup


def model_out(clients_raw, texts):
    """-> (stdout, rc) or (None, reason) for a setup failure of the clients input."""
    try:
        doc = json.loads(clients_raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None, "bad_json"
    if not isinstance(doc, list) or any(not isinstance(c, dict) for c in doc):
        return None, "bad_json"
    rules, other, unsup = model_rules(texts)
    out = ["MADO_GEOM_RULE: n=%d file=%d effect=%s arg=%s class=%s"
           % (n, r[0], r[1], r[2], r[4]) for n, r in enumerate(rules, 1)]
    t = dict(clients=0, matched=0, unmapped=0, AGREE=0, DIFFER=0, TILED=0,
             BADSIZE=0)
    for c in doc:
        if c.get("mapped") is False:
            t["unmapped"] += 1
            continue
        t["clients"] += 1
        cls = c["class"] if isinstance(c.get("class"), str) else ""
        want, frule = None, "-"
        if not any(ord(ch) < 32 for ch in cls):
            for r in rules:
                if re.fullmatch(r[4], cls):
                    if r[1] == "size":
                        want = r[3]
                    else:
                        frule = r[3]
        if want is None:
            continue
        t["matched"] += 1
        sz = c.get("size")
        size = None
        if isinstance(sz, list) and len(sz) == 2 and all(
                type(v) is int and v >= 0 for v in sz):
            size = (sz[0], sz[1])
        fl = c.get("floating") is True
        if size is None:
            v = "BADSIZE"
        elif not fl:
            v = "TILED"
        elif size == want:
            v = "AGREE"
        else:
            v = "DIFFER"
        t[v] += 1
        addr = c["address"] if isinstance(c.get("address"), str) else "-"
        out.append("MADO_GEOM_CLIENT: addr=%s class=%s floating=%s size=%s "
                   "want=%dx%d float_rule=%s verdict=%s" % (
                       json.dumps(addr), json.dumps(cls),
                       "true" if fl else "false",
                       "%dx%d" % size if size else "-", want[0], want[1],
                       frule, v))
    nsize = sum(1 for r in rules if r[1] == "size")
    if nsize == 0:
        verdict, rc = "NO_SIZE_RULES", 4
    elif t["DIFFER"]:
        verdict, rc = "DIFFER", 1
    elif t["matched"] == 0:
        verdict, rc = "NO_MATCHING_CLIENT", 3
    else:
        verdict, rc = "OK", 0
    out.append("MADO_GEOMETRY: rules=%d float_rules=%d other=%d unsupported=%d "
               "clients=%d matched=%d unmapped=%d agree=%d differ=%d tiled=%d "
               "badsize=%d verdict=%s" % (
                   nsize, len(rules) - nsize, other, unsup, t["clients"],
                   t["matched"], t["unmapped"], t["AGREE"], t["DIFFER"],
                   t["TILED"], t["BADSIZE"], verdict))
    return "\n".join(out) + "\n", rc


# ------------------------------------------------------------- the generator
def rng_for(rev, nonce, tag, i):
    h = hashlib.sha256(("%s:%s:%s:%d" % (rev, nonce, tag, i)).encode())
    return random.Random(int(h.hexdigest(), 16))


def opaque(name):
    return hashlib.sha256(("%s:%s" % (NONCE[0], name)).encode()).hexdigest()[:12]


CLASS_POOL = ["org.omarchy.gkeep", "org.omarchy.gkeep2", "Alacritty", "kitty",
              "firefox", "org.a.b", "a", "ab", "", "x y", "\u00fc-app", "a.b",
              "axb", "Org.Omarchy.Gkeep", "ab ", " ab"]
RX_POOL = ["^(org.omarchy.gkeep)$", "org\\.omarchy\\..*", "Alacritty|kitty",
           "a", "a|ab", ".*", "a\\.b", "^(a|ab)$", "(x y)?", "x.y",
           "firefox+", "org.a.b", "\\(a\\)", "a?b?", "k.*y", "^$"]
JUNK_LINES = ["# windowrule = size 1 2, match:class a", "", "bind = SUPER, A, exec, x",
              "windowrulev2 = size 1 2, class:a", "WindowRule = size 1 2, match:class a",
              "windowrule", "windowrulefoo = size 1 2, match:class a"]
OTHER_LINES = ["windowrule = center on, match:class a",
               "windowrule = opacity 0.9 0.8, match:class kitty",
               "windowrule =", "windowrule = float, match:class a",
               "windowrule = float on, match:title a", "windowrule = pin on"]
BAD_LINES = ["windowrule = size 1 2, match:title a", "windowrule = size 1x 2, match:class a",
             "windowrule = size 1 2 3, match:class a", "windowrule = size 1 2, match:class a{2}",
             "windowrule = size 1 2, match:class [ab]", "windowrule = float maybe, match:class a",
             "windowrule = size 1 2, match:class a, match:title b",
             "windowrule = size 1 2, match:class a # c", "windowrule = size 1, match:class a",
             "windowrule = size 1 2, match:class", "windowrule = size 1 2"]


def gen_texts(rng):
    n_files = rng.randrange(1, 4)
    wants = [(rng.choice([420, 800, 100, 1920]), rng.choice([500, 600, 100, 1080]))
             for _ in range(3)]
    texts = []
    for _ in range(n_files):
        lines = []
        for _ in range(rng.randrange(0, 9)):
            k = rng.randrange(10)
            rx = rng.choice(RX_POOL)
            if k < 4:
                w, h = rng.choice(wants)
                lines.append("windowrule = size %d %d, match:class %s" % (w, h, rx))
            elif k < 6:
                lines.append("windowrule = float %s, match:class %s" % (rng.choice(["on", "off"]), rx))
            elif k == 6:
                lines.append(rng.choice(OTHER_LINES))
            elif k == 7:
                lines.append(rng.choice(BAD_LINES))
            else:
                lines.append(rng.choice(JUNK_LINES))
        sep = rng.choice(["\n", "\n\n"])
        texts.append(sep.join(lines) + rng.choice(["", "\n"]))
    return texts, wants


def gen_clients(rng, wants):
    out = []
    for i in range(rng.randrange(0, 15)):
        c = {"address": "0x%x" % rng.randrange(1 << 24), "class": rng.choice(CLASS_POOL)}
        if rng.randrange(6):
            w, h = rng.choice(wants)
            if rng.randrange(3) == 0:
                w += rng.choice([-1, 1, 20])
            c["size"] = [w, h]
        else:
            c["size"] = rng.choice([[1, 2], [1.5, 2], [True, 2], [1], [-1, 2], "x", None])
        c["floating"] = rng.choice([True, True, False, 1, None])
        r = rng.randrange(8)
        if r == 0:
            c["mapped"] = False
        elif r == 1:
            c["mapped"] = True
        elif r == 2:
            del c["class"]
        out.append(c)
    return out


# ------------------------------------------------------------- execution
def prepare(tmp, name):
    d = os.path.join(tmp, opaque(name))
    os.makedirs(d)
    os.chmod(d, 0o755)
    return d


def put(d, fname, data):
    p = os.path.join(d, fname)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode("utf-8", "surrogateescape"))
    os.chmod(p, 0o644)
    return p


def execute(tool, d, argv, stdin=None, timeout=30):
    if TIMEOUTS[0] >= 3:
        return None, b"", b"skipped after 3 timeouts"
    py = os.path.realpath(sys.executable)
    cmd = sandbox_cmd(["/usr/bin/prlimit", "--nproc=1:1", py, "-I", tool] + argv,
                      [d, os.path.dirname(tool)], [], d, "/usr/bin", {})
    try:
        if stdin is None:
            p = run_piped(cmd, timeout)
        else:
            p = subprocess.run(cmd, capture_output=True, timeout=timeout,
                               env=ENV, input=stdin)
    except subprocess.TimeoutExpired:
        TIMEOUTS[0] += 1
        return None, b"", b"timeout"
    return p.returncode, p.stdout, p.stderr


def judge(rc, out, err, want_out, want_rc):
    if rc != want_rc:
        return 0, "rc=%s want=%s" % (rc, want_rc)
    got = out.decode("utf-8", "replace")
    if got != want_out:
        a, b = got.splitlines(), want_out.splitlines()
        for k in range(max(len(a), len(b))):
            if (a[k] if k < len(a) else None) != (b[k] if k < len(b) else None):
                return 0, "stdout line %d got=%r want=%r" % (
                    k + 1, a[k][:100] if k < len(a) else None,
                    b[k][:100] if k < len(b) else None)
        return 0, "stdout differs"
    if want_rc in (0, 1, 3, 4) and err:
        return 0, "stderr=%r" % err[:80]
    return 1, "ok"


def setup_line(reason):
    return "MADO_GEOMETRY: SETUP %s\n" % reason


def case_files(tool, tmp, name, clients, texts, via_stdin=False, extra=None):
    """Run one clients/rules case through the model and the tool."""
    d = prepare(tmp, name)
    rpaths = [put(d, "r%d.conf" % i, t) for i, t in enumerate(texts)]
    raw = clients if isinstance(clients, bytes) else clients.encode("utf-8", "surrogateescape")
    want = model_out(raw, [t if isinstance(t, str) else t.decode("utf-8", "replace") for t in texts])
    argv = []
    if via_stdin:
        argv += ["--clients", "-"]
    else:
        argv += ["--clients", put(d, "c.json", raw)]
    for p in rpaths:
        argv += ["--rules", p]
    rc, out, err = execute(tool, d, argv, stdin=raw if via_stdin else None)
    if want[0] is None:
        return judge(rc, out, err, setup_line(want[1]), 2)
    return judge(rc, out, err, want[0], want[1])


def score_gen(tool, tmp, rev, nonce, i):
    rng = rng_for(rev, nonce, "gen", i)
    texts, wants = gen_texts(rng)
    clients = json.dumps(gen_clients(rng, wants))
    return case_files(tool, tmp, "gen%d" % i, clients, texts, via_stdin=bool(i % 2))


def S(w, h, rx="a"):
    return "windowrule = size %d %d, match:class %s\n" % (w, h, rx)


def C(cls, size, fl=True, **kw):
    d = {"class": cls, "size": size, "floating": fl}
    d.update(kw)
    return d


def js(x):
    return json.dumps(x)


def score_stdin0(tool, tmp, rev, nonce):
    return case_files(tool, tmp, "stdin0", js([C("a", [5, 6]), C("b", [5, 6])]),
                      [S(5, 6, "a|b")], via_stdin=True)


def score_stdinbig0(tool, tmp, rev, nonce):
    d = prepare(tmp, "stdinbig0")
    r = put(d, "r.conf", S(1, 2))
    blob = b" " * (MAX_BYTES + 1)
    rc, out, err = execute(tool, d, ["--clients", "-", "--rules", r], stdin=b"[]" + blob[:-1])
    return judge(rc, out, err, setup_line("too_large"), 2)


def score_stdinok0(tool, tmp, rev, nonce):
    d = prepare(tmp, "stdinok0")
    r = put(d, "r.conf", S(1, 2))
    body = b"[]" + b" " * (MAX_BYTES - 2)
    want = model_out(body, [S(1, 2)])
    rc, out, err = execute(tool, d, ["--clients", "-", "--rules", r], stdin=body)
    return judge(rc, out, err, want[0], want[1])


def score_filecl0(tool, tmp, rev, nonce):
    return case_files(tool, tmp, "filecl0", js([C("a", [5, 7])]), [S(5, 6)])


def score_multi0(tool, tmp, rev, nonce):
    return case_files(tool, tmp, "multi0", js([C("a", [5, 6]), C("b", [9, 9])]),
                      [S(1, 1, "z") + "windowrule = float on, match:class a\n",
                       "# nothing\n", S(5, 6, "a") + S(9, 9, "b")])


def run_argv(tool, tmp, name, argv_fn, want_reason="usage"):
    d = prepare(tmp, name)
    r = put(d, "r.conf", S(1, 2))
    c = put(d, "c.json", "[]")
    rc, out, err = execute(tool, d, argv_fn(c, r))
    return judge(rc, out, err, setup_line(want_reason), 2)


def score_usage0(tool, tmp, rev, nonce):
    forms = [
        lambda c, r: [],
        lambda c, r: ["--clients", c],
        lambda c, r: ["--rules", r],
        lambda c, r: ["--clients", c, "--clients", c, "--rules", r],
        lambda c, r: ["--clients", c, "--rules", r, "--extra"],
        lambda c, r: ["--clients", c, "--rules"],
        lambda c, r: ["--client", c, "--rules", r],
        lambda c, r: ["--clients=" + c, "--rules", r],
        lambda c, r: ["--selftest", "--clients", c, "--rules", r],
        lambda c, r: ["--rules", r, "--clients", c, "x"],
        lambda c, r: ["--help"],
    ]
    for k, f in enumerate(forms):
        ok, why = run_argv(tool, tmp, "usage0-%d" % k, f)
        if not ok:
            return 0, "form %d: %s" % (k, why)
    return 1, "ok"


def score_unreadable0(tool, tmp, rev, nonce):
    for k, f in enumerate([
            lambda c, r: ["--clients", c + ".missing", "--rules", r],
            lambda c, r: ["--clients", os.path.dirname(c), "--rules", r],
            lambda c, r: ["--clients", c, "--rules", r + ".missing"],
            lambda c, r: ["--clients", c, "--rules", os.path.dirname(r)],
            lambda c, r: ["--clients", "/dev/null", "--rules", r],
            lambda c, r: ["--clients", c, "--rules", "-"]]):
        ok, why = run_argv(tool, tmp, "unreadable0-%d" % k, f, "unreadable")
        if not ok:
            return 0, "form %d: %s" % (k, why)
    return 1, "ok"


def score_fifo0(tool, tmp, rev, nonce):
    d = prepare(tmp, "fifo0")
    r = put(d, "r.conf", S(1, 2))
    c = put(d, "c.json", "[]")
    os.mkfifo(os.path.join(d, "f"))
    for argv in (["--clients", os.path.join(d, "f"), "--rules", r],
                 ["--clients", c, "--rules", os.path.join(d, "f")]):
        rc, out, err = execute(tool, d, argv, timeout=20)
        ok, why = judge(rc, out, err, setup_line("unreadable"), 2)
        if not ok:
            return 0, why
    return 1, "ok"


def score_toolarge0(tool, tmp, rev, nonce):
    d = prepare(tmp, "toolarge0")
    r = put(d, "r.conf", S(1, 2))
    big_c = put(d, "big.json", b"[]" + b" " * (MAX_BYTES - 1))
    big_r = put(d, "big.conf", b"#" * (MAX_BYTES + 1))
    c = put(d, "c.json", "[]")
    for argv in (["--clients", big_c, "--rules", r], ["--clients", c, "--rules", big_r]):
        rc, out, err = execute(tool, d, argv)
        ok, why = judge(rc, out, err, setup_line("too_large"), 2)
        if not ok:
            return 0, why
    # the clients input is judged first: too_large beats an unreadable rules file
    rc, out, err = execute(tool, d, ["--clients", big_c, "--rules", r + ".none"])
    return judge(rc, out, err, setup_line("too_large"), 2)


def score_boundary0(tool, tmp, rev, nonce):
    d = prepare(tmp, "boundary0")
    pad = (MAX_BYTES - len(S(3, 4))) * b"#"
    r = put(d, "r.conf", S(3, 4) + "")
    rbig = put(d, "rb.conf", (S(3, 4).rstrip("\n") + "\n").encode() + b"#" * (MAX_BYTES - len(S(3, 4))))
    cbig = put(d, "cb.json", js([C("a", [3, 4])]).encode() + b" " * (MAX_BYTES - len(js([C("a", [3, 4])]))))
    want = model_out(js([C("a", [3, 4])]).encode(), [S(3, 4)])
    rc, out, err = execute(tool, d, ["--clients", cbig, "--rules", rbig])
    return judge(rc, out, err, want[0], want[1])


def score_badjson0(tool, tmp, rev, nonce):
    for k, raw in enumerate([b"{}", b"[1]", b"", b"\xff[]", b"[", b"null", b"\"[]\"",
                             b"[{}, 3]", b"[[]]", b"\xef\xbb\xbf[]", b"[] x",
                             b'[{"class":"a\xffb","size":[1,2],"floating":true}]']):
        d = prepare(tmp, "badjson0-%d" % k)
        r = put(d, "r.conf", S(1, 2))
        c = put(d, "c.json", raw)
        want = model_out(raw, [S(1, 2)])
        rc, out, err = execute(tool, d, ["--clients", c, "--rules", r])
        if want[0] is None:
            ok, why = judge(rc, out, err, setup_line(want[1]), 2)
        else:
            ok, why = judge(rc, out, err, want[0], want[1])
        if not ok:
            return 0, "input %r: %s" % (raw[:12], why)
    return 1, "ok"


def score_nan0(tool, tmp, rev, nonce):
    raw = '[{"class":"a","size":[NaN,2],"floating":true},{"class":"a","size":[1,Infinity],"floating":true},{"class":"a","size":[1e2,2],"floating":true},{"class":"a","size":[100,2],"floating":true}]'
    return case_files(tool, tmp, "nan0", raw, [S(100, 2)])


def score_regex0(tool, tmp, rev, nonce):
    rxs = ["a", "a" * 200, "a" * 201, "", "^(a|b)+\\.c$", "a{2}", "[ab]", "\\d", "\\w",
           "(?i)a", "(?:a)", "a*+", "a++", "a?+", "a**", "a+*", "a+?", "a*?", "a??", "(a", "a)", "a|", "|a",
           "()", "a\\", "\\\\", "\\a", "a-b", "a b", "a\\ b", "a\u00fc", "a,b", "a\tb", "\\.\\-\\(\\)\\|\\*\\+\\?\\^\\$",
           "^a$", "a^b", "a$b", "$a", "a^", ".", "..", "(a|b)(c|d)", "(()))", "x" * 150 + "|" + "y" * 49,
           "\\\\\\", "negative:a", "a:b", "a/b", "a'b", "a\"b", "a#", "a~", "a=", "a%"]
    text = "".join("windowrule = size %d 7, match:class %s\n" % (i + 1, rx) for i, rx in enumerate(rxs))
    clients = js([C(c, [1, 7]) for c in ("a", "aa", "b", "a.c", "bb.c", "ac", "a-b", "x" * 150, "y" * 49, "ab", "")])
    return case_files(tool, tmp, "regex0", clients, [text])


def score_size0(tool, tmp, rev, nonce):
    sizes = ["0 0", "00420 500", "99999 99999", "100000 1", "1 100000", "\u0664\u0662\u0660 500",
             "420 500", "-1 5", "+1 5", "1.5 2", "1 2 3", "1", "", "0x10 5", "1 \u0663", "007 008", "12345 54321"]
    text = "".join("windowrule = size %s, match:class a\n" % s for s in sizes)
    clients = js([C("a", [0, 0]), C("a", [420, 500]), C("a", [7, 8])])
    out = []
    for i, s in enumerate(sizes):
        ok, why = case_files(tool, tmp, "size0-%d" % i, clients,
                             ["windowrule = size %s, match:class a\n" % s])
        if not ok:
            return 0, "size %r: %s" % (s, why)
    return 1, "ok"


def score_float0(tool, tmp, rev, nonce):
    for i, arg in enumerate(["on", "off", "On", "ON", "true", "1", "yes", "", "on off", "toggle", "0"]):
        ok, why = case_files(tool, tmp, "float0-%d" % i, js([C("a", [1, 2]), C("b", [1, 2])]),
                             [S(1, 2, "a|b") + "windowrule = float %s, match:class b\n" % arg])
        if not ok:
            return 0, "float %r: %s" % (arg, why)
    return 1, "ok"


def score_space0(tool, tmp, rev, nonce):
    lines = ["windowrule=size 1 2,match:class a", "windowrule\t=\tsize\t1\t2\t,\tmatch:class\ta",
             "  \twindowrule = size 1 2 , match:class a  \t", "windowrule  =  size   1    2  ,  match:class     a",
             "windowrule = size 1 2,match:class a\r", "windowrule = size 1 2, match:class a\x0b",
             "windowrule = size 1 2, match:class\ta", "windowrule = size 1 2, match:classa",
             "windowrule = size 1 2, match: class a", "windowrule = size 1 2, Match:class a",
             "windowrule = size\u00a01 2, match:class a", "windowrule = SIZE 1 2, match:class a",
             "windowrule = size 1 2,, match:class a", "windowrule = ,size 1 2, match:class a",
             "windowrule =size 1 2, match:class a"]
    for i, ln in enumerate(lines):
        ok, why = case_files(tool, tmp, "space0-%d" % i, js([C("a", [1, 2])]), [ln + "\n"])
        if not ok:
            return 0, "line %r: %s" % (ln, why)
    return 1, "ok"


def score_ignore0(tool, tmp, rev, nonce):
    text = "\n".join(JUNK_LINES + ["windowrule = size 1 2, match:class a", "  # c", "windowrule2 = size 1 2, match:class a"]) + "\n"
    return case_files(tool, tmp, "ignore0", js([C("a", [1, 2])]), [text])


def score_other0(tool, tmp, rev, nonce):
    text = "\n".join(OTHER_LINES + ["windowrule = size 1 2, match:class a", "windowrule = noshadow", "windowrule = ,"]) + "\n"
    return case_files(tool, tmp, "other0", js([C("a", [1, 2])]), [text])


def score_order0(tool, tmp, rev, nonce):
    t1 = S(1, 1, ".*") + "windowrule = float on, match:class .*\n"
    t2 = S(2, 2, "a|b") + "windowrule = float off, match:class a\n"
    t3 = S(3, 3, "b")
    clients = js([C("b", [3, 3]), C("a", [2, 2], address="0x2"), C("c", [1, 1], address="0x3"),
                  C("a", [1, 1], fl=False)])
    return case_files(tool, tmp, "order0", clients, [t1, t2, t3])


def score_client0(tool, tmp, rev, nonce):
    cl = [{}, {"class": "a"}, {"class": None, "size": [1, 2], "floating": True},
          {"class": ["a"], "size": [1, 2], "floating": True}, {"class": "a", "size": [1, 2]},
          {"class": "a", "size": [1, 2], "floating": "true"}, {"class": "a", "size": [1, 2], "floating": 1},
          {"class": "a", "size": [1, 2], "floating": True, "address": 5},
          {"class": "a", "size": [1, 2], "floating": True, "address": "0xabc"},
          {"class": "a", "size": [1, 2], "floating": True, "extra": 1}, {"size": [1, 2], "floating": True}]
    return case_files(tool, tmp, "client0", js(cl), [S(1, 2, "a|"), "windowrule = float on, match:class a\n"])


def score_sizevals0(tool, tmp, rev, nonce):
    sv = [[1, 2], [1.0, 2], [1, 2.0], [True, 2], [1, False], [1], [1, 2, 3], [], "12", None, 12, {"w": 1},
          [-1, 2], [1, -2], [10 ** 30, 2], [0, 0], [[1], 2], ["1", 2], [1, 2]]
    cl = [C("a", s) for s in sv]
    return case_files(tool, tmp, "sizevals0", js(cl), [S(1, 2), S(10 ** 30 % 100000, 1, "zz")])


def score_mapped0(tool, tmp, rev, nonce):
    cl = []
    for m in (False, True, None, 0, 1, "false", "", [], {}):
        cl.append(C("a", [1, 2], mapped=m))
    cl.append(C("a", [1, 2]))
    return case_files(tool, tmp, "mapped0", js(cl), [S(1, 2)])


def score_dupkeys0(tool, tmp, rev, nonce):
    raw = '[{"class":"zz","class":"a","size":[9,9],"size":[1,2],"floating":false,"floating":true,"mapped":false,"mapped":true}]'
    return case_files(tool, tmp, "dupkeys0", raw, [S(1, 2)])


def score_ctlclass0(tool, tmp, rev, nonce):
    cl = [C(c, [1, 2]) for c in ("a\x01b", "a\x1fb", "a\tb", "a\nb", "a\x7fb", "a b", "a\u0085b", "\x00", "a\u2028b")]
    return case_files(tool, tmp, "ctlclass0", js(cl), [S(1, 2, "a.b")])


def score_unicode0(tool, tmp, rev, nonce):
    cl = [C("\u00fc", [1, 2], address="\u00e9\"\\/"), C("\U0001f600", [1, 2], address="\U0001f601"),
          C("a\u200bb", [1, 2], address="\u2028"), C("\u2028", [1, 2])]
    ok, why = case_files(tool, tmp, "unicode0", json.dumps(cl, ensure_ascii=False), [S(1, 2, ".*")])
    if not ok:
        return 0, why
    raw = '[{"class":"\\ud800x","size":[1,2],"floating":true,"address":"\\udc00"}]'
    return case_files(tool, tmp, "unicode1", raw, [S(1, 2, ".*")])


def score_many0(tool, tmp, rev, nonce):
    rng = rng_for("many", nonce, "many", 0)
    cl = [C(rng.choice(["a", "b", "c"]), [rng.randrange(3), 2], fl=bool(rng.randrange(2))) for _ in range(20000)]
    text = "".join(S(i % 3, 2, "a|b") for i in range(300))
    return case_files(tool, tmp, "many0", js(cl), [text])


def score_empty0(tool, tmp, rev, nonce):
    for k, (c, t) in enumerate([("[]", ""), ("[]", "\n\n"), ("[{}]", ""), ("[]", S(1, 2))]):
        ok, why = case_files(tool, tmp, "empty0-%d" % k, c, [t])
        if not ok:
            return 0, "case %d: %s" % (k, why)
    return 1, "ok"


FIXED = [
    ("stdin0", score_stdin0), ("stdinbig0", score_stdinbig0), ("stdinok0", score_stdinok0),
    ("filecl0", score_filecl0), ("multi0", score_multi0), ("usage0", score_usage0),
    ("unreadable0", score_unreadable0), ("fifo0", score_fifo0), ("toolarge0", score_toolarge0),
    ("boundary0", score_boundary0), ("badjson0", score_badjson0), ("nan0", score_nan0),
    ("regex0", score_regex0), ("size0", score_size0), ("float0", score_float0),
    ("space0", score_space0), ("ignore0", score_ignore0), ("other0", score_other0),
    ("order0", score_order0), ("client0", score_client0), ("sizevals0", score_sizevals0),
    ("mapped0", score_mapped0), ("dupkeys0", score_dupkeys0), ("ctlclass0", score_ctlclass0),
    ("unicode0", score_unicode0), ("many0", score_many0), ("empty0", score_empty0),
]

# ------------------------------------------------------------- clauses
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
        elif isinstance(node, ast.Name):
            if node.id in NAME_DENY or node.id in CALL_DENY:
                return False
        elif isinstance(node, ast.Attribute):
            if node.attr in CALL_DENY and isinstance(node.value, ast.Name) \
                    and node.value.id in ("builtins", "__builtins__"):
                return False
            if isinstance(node.value, ast.Name):
                if node.value.id == "os" and (node.attr in OS_DENY
                                              or node.attr.startswith("exec")):
                    return False
                if node.value.id == "sys" and node.attr in ("executable",
                                                            "modules"):
                    return False
        elif isinstance(node, ast.Subscript):
            v = node.value
            if isinstance(v, ast.Attribute) and v.attr == "argv" \
                    and isinstance(node.slice, ast.Constant) \
                    and node.slice.value == 0:
                return False
        elif isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg is None:
                    return False
                if kw.arg == "shell" and not (
                        isinstance(kw.value, ast.Constant)
                        and kw.value.value is False):
                    return False
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if node.value in STR_EQ_DENY \
                    or any(s in node.value for s in STR_DENY):
                return False
    return bool(mods) and mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)


NOT_SITES = ("selftest", "main", "usage")
FLIP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE,
        ast.GtE: ast.Lt, ast.Gt: ast.LtE, ast.LtE: ast.Gt, ast.In: ast.NotIn,
        ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}


def function_sites(src):
    """Comparison sites of every function except selftest/main/usage (by exact
    name) and the functions defined inside selftest. Returns (site, summary)
    tuples: summary is True when the function body holds the final-line text."""
    tree = ast.parse(src)
    nested = set()
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name == "selftest":
            for inner in ast.walk(fn):
                if isinstance(inner, ast.FunctionDef) and inner is not fn:
                    nested.add(id(inner))
    sites = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if fn.name in NOT_SITES or id(fn) in nested:
            continue
        summary = any(isinstance(c, ast.Constant) and isinstance(c.value, str)
                      and "MADO_GEOMETRY: rules=" in c.value
                      for c in ast.walk(fn))
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.ops) == 1 \
                    and type(node.ops[0]) in FLIP:
                sites.append(((fn.name, node.lineno, node.col_offset),
                              summary))
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


def selftest_result(tool, scratch):
    rc, out, err = run_sandboxed(tool, scratch, ["--selftest"], "/usr/bin",
                                 ro=[os.path.dirname(tool)], timeout=60)
    m = re.search(r"MADO_GEOMETRY_SELFTEST: (\d+)/(\d+) passed",
                  (out or b"").decode("utf-8", "replace"))
    k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return rc, k, n, m is not None


def run_selftest_copy(text, tmp, tag):
    """Place TEXT as <tmp>/<opaque>/tool/mado-geometry.py (the real layout)."""
    d = os.path.join(tmp, opaque("copy-" + tag), "tool")
    os.makedirs(d)
    os.chmod(os.path.dirname(d), 0o755)
    os.chmod(d, 0o755)
    path = os.path.join(d, "mado-geometry.py")
    with open(path, "w") as fh:
        fh.write(text)
    return selftest_result(path, d)


def teeth(src, tmp, nonce):
    sites = function_sites(src)
    if len(sites) < MIN_SITES:
        print("%s clause=b2 sites=%d (<%d)" % (PRED, len(sites), MIN_SITES))
        return False
    summ = [s for s, flag in sites if flag]
    rest = [s for s, flag in sites if not flag]
    if not summ:
        print("%s clause=b2 no_site_in_summary_function" % PRED)
        return False
    rng = random.Random(int(hashlib.sha256(("mut:" + nonce).encode()).hexdigest(), 16))
    forced = rng.choice(summ)
    chosen = [forced] + rng.sample([s for s in rest + summ if s != forced], N_MUT - 1)
    killed, forced_dead = 0, False
    for n, site in enumerate(chosen):
        mutated = mutate_source(src, site)
        if mutated is None:
            continue
        rc, k, n_, has = run_selftest_copy(mutated, tmp, "m%d" % n)
        dead = rc != 0 or not has or k != n_
        killed += dead
        if site == forced:
            forced_dead = bool(dead)
        print("%s clause=b2 mutant=%d site=%s:%d killed=%d%s" % (
            PRED, n, site[0], site[1], dead, " forced" if site == forced else ""))
    print("%s clause=b2 sites=%d killed=%d/%d forced_dead=%d" % (
        PRED, len(sites), killed, N_MUT, forced_dead))
    return killed >= KILL_NEED and forced_dead


def neutrality(src, tmp, nonce):
    """b3: edits that do not change behaviour must not change the selftest."""
    variants = {
        "comment": src + "\n# b3-neutral %s\n" % nonce,
        "unparse": ast.unparse(ast.parse(src)) + "\nB3_NEUTRAL_%s = 1\n" % nonce[:8],
    }
    ok = True
    for tag, text in variants.items():
        rc, k, n, has = run_selftest_copy(text, tmp, "n-" + tag)
        good = rc == 0 and has and k == n and n >= MIN_SELFTEST
        ok &= good
        print("%s clause=b3 variant=%s rc=%s selftest=%d/%d ok=%d" % (PRED, tag, rc, k, n, good))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--tool", default=None, help="score this file instead of REV's tool (controls)")
    ap.add_argument("--nonce", default=None)
    args = ap.parse_args()
    nonce = args.nonce or secrets.token_hex(8)
    NONCE[0] = nonce
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    check_sandbox()
    if git(repo, "show", "%s:%s" % (base, TOOL)) is not None:
        raise Setup("precondition_failed tool_present_at_base")
    src = open(args.tool, "rb").read() if args.tool else git(repo, "show", "%s:%s" % (rev, TOOL))
    present = src is not None
    cl = {"a": int(present), "b": 0, "b2": 0, "b3": 0, "g": 0}
    passed = 0
    if present:
        cl["g"] = int(imports_ok(src))
        tmp = tempfile.mkdtemp(prefix="mado-c1r42-", dir=os.environ.get("C1R42_TMP") or None)
        os.chmod(tmp, 0o755)
        try:
            td = os.path.join(tmp, opaque("real"), "tool")
            os.makedirs(td)
            os.chmod(os.path.dirname(td), 0o755)
            os.chmod(td, 0o755)
            tool = os.path.join(td, "mado-geometry.py")
            with open(tool, "wb") as fh:
                fh.write(src)
            rc, k, n, has = selftest_result(tool, td)
            cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)
            print("%s clause=b rc=%s selftest=%d/%d" % (PRED, rc, k, n))
            if cl["b"]:
                text = src.decode("utf-8", "replace")
                cl["b2"] = int(teeth(text, tmp, nonce))
                cl["b3"] = int(neutrality(text, tmp, nonce))
            cases = [("gen%d" % i, (lambda i=i: score_gen(tool, tmp, rev, nonce, i))) for i in range(10)]
            for name, fn in FIXED:
                cases.append((name, (lambda fn=fn: fn(tool, tmp, rev, nonce))))
            assert len(cases) == TOTAL, len(cases)
            for name, fn in cases:
                ok, why = fn()
                passed += ok
                print("%s fixture=%s ok=%d %s" % (PRED, name, ok, why))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    met = all(cl.values()) and passed == TOTAL
    print("%s clauses=%s" % (PRED, " ".join("%s:%d" % kv for kv in sorted(cl.items()))))
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

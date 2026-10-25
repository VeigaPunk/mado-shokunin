#!/usr/bin/env python3
"""PRED-C1-r41-v1 - a read-only census of the compositor's advertised Wayland globals (C1, operability).

Scores one committed revision REV of the lane (revision-addressed git reads,
ambient GIT_* removed; nothing in the lane is written). The tool under test is
`tools/mado-globals.py` at REV (or `--tool PATH` for a control); BASE must lack
it. Every tool and selftest run happens inside a bubblewrap sandbox
(`bwrap --unshare-all --cap-drop ALL`, fresh /proc and /dev, tmpfs /tmp, the
interpreter's /usr read-only, the scratch tree read-only): the tool sees neither
the lane, nor this counter, nor /home. No bwrap -> SETUP, exit 2. Fixtures mix a
per-run nonce: sha256(REV:NONCE:i); the nonce is printed and replayable with
`--nonce`; coverage comes from a deterministic lattice on the fixture index.

The journal the tool reads is the output of
`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`.

CLI (the code below is the same sentence): `mado-globals.py (--journal-file P |
--live [--journalctl PROG]) [--expect NAME]... [--diff]` and `--selftest`.
Exactly one of --journal-file/--live; --journalctl needs --live; no abbreviated
flags; a NAME must fully match [A-Za-z0-9_]{1,128}. Setup failure: stdout is
exactly one line `MADO_GLOBALS: SETUP <reason>` (nothing else, empty stderr
not required), exit 2, reason one of usage | unreadable | too_large |
bad_expect; a journal file larger than 8 MiB (8388608 bytes) is too_large, a
missing/unreadable one unreadable.

Parsing. Lines are split on "\\n". A BOOT line fully matches
`-- Boot ([0-9a-f]{32}) --`. An ADVERT line fully matches
`TS HOST xdg-desktop-portal-hyprland[PID]: [LOG]  | Got interface: NAME (ver N)`
with TS = `\\d{4}-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\d[+-]\\d\\d:\\d\\d`, HOST = `\\S+`, PID =
`\\d+`, exactly two spaces after `[LOG]`, NAME = `[A-Za-z0-9_]{1,128}`, N =
`\\d{1,6}`; every other line (another program, another level, trailing or
leading text, CR endings, bad timestamps, bytes that are not UTF-8) is ignored.
A SESSION starts at an ADVERT when no session is open, or a BOOT line occurred
since the previous ADVERT, or its PID differs from the open session's PID.
Session fields: boot = the id of the last BOOT line seen before its first ADVERT
(`-` when none); pid; first/last = TS of its first/last ADVERT; adverts = ADVERT
lines; per distinct NAME: count and ver = the highest N seen.

Output, in order (stdout, one line each; nothing else):
  per session n=1..k   MADO_GLOBALS_SESSION: n=<n> boot=<id|-> pid=<pid> first=<ts> last=<ts> interfaces=<distinct> adverts=<adverts>
  latest session only, per NAME sorted bytewise
                       MADO_GLOBAL: name=<name> ver=<max> count=<count> class=<class>
  with --diff          MADO_GLOBALS_DIFF: from=<k-1> to=<k> added=<csv|-> removed=<csv|-> ver_changed=<name:old>new csv|->
                       (k < 2: `MADO_GLOBALS_DIFF: sessions=<k> none`), names sorted bytewise
  last                 MADO_GLOBALS: sessions=<k> latest_pid=<pid|-> interfaces=<distinct|0> classes=<class:n csv sorted by class|-> expected_missing=<csv sorted, deduped|-> verdict=<V>
V = NO_SESSIONS (k = 0; exit 3) | MISSING_EXPECTED (an --expect NAME absent from the
latest session; exit 1) | OK (exit 0). NO_SESSIONS wins over MISSING_EXPECTED.
Class decision table (name -> class; every other name is `other`):
  focus-grab        hyprland_focus_grab_manager_v1
  input-synthesis   zwlr_virtual_pointer_manager_v1 zwp_virtual_keyboard_manager_v1 zwp_input_method_manager_v2
  input-capture     hyprland_input_capture_manager_v1 zwp_keyboard_shortcuts_inhibit_manager_v1 hyprland_global_shortcuts_manager_v1
  session-lock      ext_session_lock_manager_v1 hyprland_lock_notifier_v1
  idle              ext_idle_notifier_v1 zwp_idle_inhibit_manager_v1
  clipboard         zwlr_data_control_manager_v1 ext_data_control_manager_v1 zwp_primary_selection_device_manager_v1
  capture           ext_image_copy_capture_manager_v1 ext_foreign_toplevel_image_capture_source_manager_v1 zwlr_screencopy_manager_v1 hyprland_toplevel_export_manager_v1
  toplevel-control  zwlr_foreign_toplevel_manager_v1 ext_foreign_toplevel_list_v1 xdg_activation_v1 hyprland_toplevel_mapping_manager_v1
  output-control    zwlr_output_manager_v1 zwlr_output_power_manager_v1 zwlr_gamma_control_manager_v1 hyprland_ctm_control_manager_v1
  sandbox           wp_security_context_manager_v1

--live. The program is `--journalctl PROG` or `journalctl` found through PATH;
it is resolved to an absolute regular executable file that is not group- or
other-writable, otherwise stdout `MADO_GLOBALS: SETUP journalctl_unusable`,
exit 5, and the program is not run. It is run with EXACTLY the arguments
`--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (no shell),
stdin /dev/null (an open pipe is a violation), an environment limited to PATH,
XDG_RUNTIME_DIR, DBUS_SESSION_BUS_ADDRESS and LC_ALL, and its stdout is parsed
exactly as a journal file. A non-zero exit, a spawn failure or a timeout is
`SETUP journalctl_failed` (exit 5); more than 8 MiB of output is
`SETUP journalctl_too_large` (exit 5). The stub the judge supplies exits 9
unless argv, stdin and environment are as stated, so a violation shows as exit
5, never as a report. In `--journal-file` mode the tool must not start any
process (a `journalctl` stub earlier on PATH records a hit; a hit fails the
fixture). The tree the tool reads is mounted read-only.

Fixtures (24): gen0..gen7 (lattice: plain; pid reused across boots; pid
alternation A,B,A; noise-heavy; conflicting versions; every table name; a boot
line splitting one pid / leading and trailing boot lines; 20000 adverts), diff0
(--diff, 3 sessions), diff1 (--diff, one session), expect0 (all present),
expectmiss0 (some absent, with a duplicate), nosess0 (noise only, with --expect),
nosess1 (empty file), unreadable0, usage0 (neither flag, both flags,
--journalctl without --live, abbreviated flag), badexpect0 (`--expect=a b`,
`--expect=`, 129-char name), toolarge0, live0 (stub through --journalctl),
live1 (stub through PATH), livefail0 (stub exits 1), liveenv0 (canary variable
and open stdin must not reach the stub; the stub then succeeds), livewritable0
(group-writable program), livelarge0 (9 MB of output). Each fixture compares
rc and stdout byte-exactly with the judge's model; on rc 0/1/3 stderr must be
empty.

Clauses: a  the tool exists at REV and BASE lacks it; b  `--selftest` (in the
sandbox) exits 0 printing `MADO_GLOBALS_SELFTEST: k/n passed`, k == n and
n >= 25; b2  the selftest has teeth: from the tool's functions (not named
*selftest*, *_check*, *_run*, *_write*, main, usage) >= 12 comparison sites
exist, 6 chosen by the nonce are each flipped in a copy, and the copy's
selftest fails (non-zero, k < n, or no summary) for >= 4 of the 6; g  top-level
imports are standard library only (argparse collections itertools os re shutil
stat subprocess sys tempfile), none of socket urllib http requests ssl ctypes importlib
pty is imported, the source calls none of exec, eval, compile, __import__
(as a name or on builtins), os.system, os.popen, os.exec*, and passes no
`shell=True`, and names no `/proc`, `c1-r41` or `quality/counters` string.

Final line: `PRED-C1-r41-v1: fixtures=P/24 tool=present|absent
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> nonce=<hex>`. TARGET_MET iff
a, b, b2, g hold and P == 24; exit 0, else exit 1.
Residual (declared): a tool that CONTAINS the class table and parser is an
implementation; the stub's data is in the stub and a tool that decodes it
without running it passes; the g clause is a heuristic, the sandbox is the
boundary. The host receipt (`--live` on the running desktop) is reported, not
scored.
"""
import argparse
import ast
import base64
import hashlib
import os
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C1-r41-v1"
BASE_DEFAULT = "ab2bfaab661c846d1de9d58c01651cd156a13949"
TOOL = "tools/mado-globals.py"
TOTAL = 24
MIN_SELFTEST = 25
MIN_SITES = 12
N_MUT = 6
KILL_NEED = 4
MAX_BYTES = 8 * 1024 * 1024
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
STDLIB_ALLOW = {"argparse", "collections", "itertools", "os", "re", "shutil",
                "stat", "subprocess", "sys", "tempfile"}
STDLIB_DENY = {"socket", "urllib", "http", "requests", "ssl", "ctypes",
               "importlib", "pty"}
CALL_DENY = {"exec", "eval", "compile", "__import__"}
OS_DENY = {"system", "popen", "execv", "execve", "execvp", "execl", "execle",
           "execlp", "execvpe", "execlpe", "spawnl", "spawnv", "posix_spawn"}
STR_DENY = ("/proc", "c1-r41", "quality/counters")
LIVE_ARGS = "--user -u xdg-desktop-portal-hyprland --no-pager -o short-iso"
CLASSES = {
    "focus-grab": ["hyprland_focus_grab_manager_v1"],
    "input-synthesis": ["zwlr_virtual_pointer_manager_v1",
                        "zwp_virtual_keyboard_manager_v1",
                        "zwp_input_method_manager_v2"],
    "input-capture": ["hyprland_input_capture_manager_v1",
                      "zwp_keyboard_shortcuts_inhibit_manager_v1",
                      "hyprland_global_shortcuts_manager_v1"],
    "session-lock": ["ext_session_lock_manager_v1", "hyprland_lock_notifier_v1"],
    "idle": ["ext_idle_notifier_v1", "zwp_idle_inhibit_manager_v1"],
    "clipboard": ["zwlr_data_control_manager_v1", "ext_data_control_manager_v1",
                  "zwp_primary_selection_device_manager_v1"],
    "capture": ["ext_image_copy_capture_manager_v1",
                "ext_foreign_toplevel_image_capture_source_manager_v1",
                "zwlr_screencopy_manager_v1",
                "hyprland_toplevel_export_manager_v1"],
    "toplevel-control": ["zwlr_foreign_toplevel_manager_v1",
                         "ext_foreign_toplevel_list_v1", "xdg_activation_v1",
                         "hyprland_toplevel_mapping_manager_v1"],
    "output-control": ["zwlr_output_manager_v1", "zwlr_output_power_manager_v1",
                       "zwlr_gamma_control_manager_v1",
                       "hyprland_ctm_control_manager_v1"],
    "sandbox": ["wp_security_context_manager_v1"],
}
TABLE = {n: c for c, ns in CLASSES.items() for n in ns}
COMMON = ["wl_seat", "wl_compositor", "wl_shm", "wl_output", "xdg_wm_base",
          "zwlr_layer_shell_v1", "wp_viewporter", "wp_presentation",
          "zxdg_output_manager_v1", "wp_cursor_shape_manager_v1"]
ADV_RE = re.compile(
    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}) (\S+) "
    r"xdg-desktop-portal-hyprland\[(\d+)\]: \[LOG\]  \| "
    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver (\d{1,6})\)")
BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")


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
    p = subprocess.run(sandbox_cmd(["/usr/bin/true"], [], [], "/", "/usr/bin",
                                   {}), capture_output=True, text=True)
    if p.returncode != 0:
        raise Setup("sandbox_unavailable bwrap rc=%d %s"
                    % (p.returncode, p.stderr.strip()[:120]))
    if not os.path.realpath(sys.executable).startswith("/usr/"):
        raise Setup("interpreter_outside_usr %s" % sys.executable)


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
                  extra_env=None, timeout=120):
    py = os.path.realpath(sys.executable)
    cmd = sandbox_cmd([py, "-I", tool, *argv], [scratch, *ro], list(rw),
                      cwd or scratch, path_env, extra_env or {})
    try:
        p = run_piped(cmd, timeout)
    except subprocess.TimeoutExpired:
        return None, b"", b"timeout"
    return p.returncode, p.stdout, p.stderr


# ------------------------------------------------------------- the model
def classify(name):
    return TABLE.get(name, "other")


def model_sessions(text):
    sessions, boot, changed, cur = [], "-", False, None
    for line in text.split("\n"):
        if BOOT_RE.fullmatch(line):
            boot, changed = BOOT_RE.fullmatch(line).group(1), True
            continue
        m = ADV_RE.fullmatch(line)
        if m is None:
            continue
        ts, _h, pid, name, ver = m.groups()
        if cur is None or changed or pid != cur["pid"]:
            cur = {"boot": boot, "pid": pid, "first": ts, "last": ts,
                   "adverts": 0, "names": {}}
            sessions.append(cur)
            changed = False
        cur["last"] = ts
        cur["adverts"] += 1
        c, v = cur["names"].get(name, (0, 0))
        cur["names"][name] = (c + 1, max(v, int(ver)))
    return sessions


def model_out(text, expects, diff):
    ss = model_sessions(text)
    out = []
    for i, s in enumerate(ss, 1):
        out.append("MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s first=%s last=%s "
                   "interfaces=%d adverts=%d" % (i, s["boot"], s["pid"],
                                                 s["first"], s["last"],
                                                 len(s["names"]), s["adverts"]))
    last = ss[-1] if ss else None
    if last:
        for n in sorted(last["names"]):
            c, v = last["names"][n]
            out.append("MADO_GLOBAL: name=%s ver=%d count=%d class=%s"
                       % (n, v, c, classify(n)))
    if diff:
        if len(ss) < 2:
            out.append("MADO_GLOBALS_DIFF: sessions=%d none" % len(ss))
        else:
            a, b = ss[-2]["names"], ss[-1]["names"]
            ch = ["%s:%d>%d" % (n, a[n][1], b[n][1])
                  for n in sorted(a) if n in b and a[n][1] != b[n][1]]
            out.append("MADO_GLOBALS_DIFF: from=%d to=%d added=%s removed=%s "
                       "ver_changed=%s" % (
                           len(ss) - 1, len(ss),
                           ",".join(sorted(n for n in b if n not in a)) or "-",
                           ",".join(sorted(n for n in a if n not in b)) or "-",
                           ",".join(ch) or "-"))
    names = last["names"] if last else {}
    cls = {}
    for n in names:
        cls[classify(n)] = cls.get(classify(n), 0) + 1
    miss = sorted(set(e for e in expects if e not in names))
    v = "NO_SESSIONS" if not ss else ("MISSING_EXPECTED" if miss else "OK")
    code = {"OK": 0, "MISSING_EXPECTED": 1, "NO_SESSIONS": 3}[v]
    out.append("MADO_GLOBALS: sessions=%d latest_pid=%s interfaces=%d classes=%s "
               "expected_missing=%s verdict=%s" % (
                   len(ss), last["pid"] if last else "-", len(names),
                   ",".join("%s:%d" % (c, cls[c]) for c in sorted(cls)) or "-",
                   ",".join(miss) or "-", v))
    return "\n".join(out) + "\n", code


# ------------------------------------------------------------- the generator
def rng_for(rev, nonce, tag, i):
    h = hashlib.sha256(("%s:%s:%s:%d" % (rev, nonce, tag, i)).encode())
    return random.Random(int(h.hexdigest(), 16))


def ts_of(rng, base):
    return "2026-10-%02dT%02d:%02d:%02d-03:00" % (
        1 + (base + rng.randrange(20)) % 28, rng.randrange(24),
        rng.randrange(60), rng.randrange(60))


def advert(ts, host, pid, name, ver):
    return ("%s %s xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: "
            "%s (ver %d)" % (ts, host, pid, name, ver))


def noise_lines(rng, ts, pid):
    n129 = "a" * 129
    return [
        "%s h Hyprland[%s]: [LOG]  | Got interface: wl_seat (ver 9)" % (ts, pid),
        "%s h xdg-desktop-portal-hyprland[%s]: [ERR]  | Got interface: wl_seat (ver 9)" % (ts, pid),
        "%s h xdg-desktop-portal-hyprland[%s]: [LOG] | Got interface: wl_seat (ver 9)" % (ts, pid),
        "%s h xdg-desktop-portal-hyprland[%s]: [LOG]   | Got interface: wl_seat (ver 9)" % (ts, pid),
        advert(ts, "h", pid, "wl_seat", 9) + " extra",
        "x " + advert(ts, "h", pid, "wl_seat", 9),
        advert(ts, "h", pid, "wl_seat", 9) + "\r",
        advert(ts, "h", pid, "wl_seat", 9).replace("(ver 9)", "(ver x)"),
        advert(ts, "h", pid, "wl_seat", 9).replace("(ver 9)", "(ver 1234567)"),
        advert(ts, "h", pid, "wl_seat", 9).replace("wl_seat", "wl-seat"),
        advert(ts, "h", pid, n129, 1),
        advert(ts, "h", pid, "wl_seat", 9).replace("Got", "got"),
        advert(ts, "h", pid, "wl_seat", 9).replace(ts, "2026-10-25 13:36:24"),
        advert(ts, "h", pid, "wl_seat", 9).replace("[" + pid + "]", "[x]"),
        "-- Boot " + "A" * 32 + " --",
        "-- Boot " + "a" * 31 + " --",
        "--Boot " + "a" * 32 + " --",
        "-- No entries --",
        "%s h xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: \xe9\xff (ver 1)" % (ts, pid),
        "",
    ]


def gen_fixture(rev, nonce, i):
    """Returns (journal text, expect list, diff flag)."""
    rng = rng_for(rev, nonce, "gen", i)
    pool = sorted(TABLE) + COMMON
    syn = ["zz_%04x_v%d" % (rng.randrange(65536), rng.randrange(1, 4))
           for _ in range(12)]
    lines = []

    def boot():
        return "-- Boot %032x --" % rng.getrandbits(128)

    def session(pid, n, base, vers=False, noise=False, names=None):
        ts = ts_of(rng, base)
        pick = names or rng.sample(pool + syn, k=min(n, len(pool + syn)))
        for name in pick:
            reps = rng.randrange(1, 7 if vers else 3)
            for _ in range(reps):
                ver = rng.randrange(1, 10) if vers else rng.randrange(1, 5)
                lines.append(advert(ts_of(rng, base), "plazir%d" % rng.randrange(9),
                                    pid, name, ver))
                if noise and rng.random() < 0.7:
                    lines.append(rng.choice(noise_lines(rng, ts, pid)))

    pid = str(rng.randrange(100, 99999))
    if i == 0:
        session(pid, 14, 1)
    elif i == 1:
        for k in range(3):
            lines.append(boot())
            session(pid, 10 + 3 * k, k)
    elif i == 2:
        a, b = pid, str(int(pid) + 7)
        session(a, 8, 1)
        session(b, 9, 2)
        session(a, 10, 3)
    elif i == 3:
        lines.append(boot())
        session(pid, 16, 5, noise=True)
        lines.extend(noise_lines(rng, ts_of(rng, 3), pid))
    elif i == 4:
        session(pid, 12, 7, vers=True)
        session(str(int(pid) + 1), 12, 8, vers=True, names=None)
    elif i == 5:
        lines.append(boot())
        session(pid, 0, 2, names=sorted(TABLE) + syn[:4])
        lines.append(boot())
        session(str(int(pid) + 3), 0, 2, names=sorted(TABLE)[: len(TABLE) // 2]
                + syn[2:6])
    elif i == 6:
        lines.append(boot())
        lines.append(boot())
        session(pid, 9, 4)
        lines.append(boot())
        session(pid, 11, 5)
        lines.append(boot())
    else:
        for k in range(2):
            ts0 = ts_of(rng, k)
            p = str(int(pid) + k)
            for j in range(10000):
                lines.append(advert(ts0, "h", p, pool[j % len(pool)],
                                    1 + (j * 7) % 9))
            lines.append(boot())
    text = "\n".join(lines) + "\n"
    sess = model_sessions(text)
    names = sorted(sess[-1]["names"]) if sess else []
    expects = []
    diff = i in (1, 2, 6)
    if i % 2 == 1:
        expects = rng.sample(names, k=min(2, len(names))) + ["zz_absent_v9"]
    return text, expects, diff


def gen_sessions_check(i, text):
    """Internal consistency: the model must see the lattice's intended count."""
    want = {0: 1, 1: 3, 2: 3, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2}[i]
    got = len(model_sessions(text))
    if got != want:
        raise Setup("judge_inconsistent gen%d sessions=%d want=%d" % (i, got, want))


# ------------------------------------------------------------ the fixtures
STUB_FILE = "#!/bin/sh\ntouch %s\nexit 1\n"


def live_stub(data_b64, mode="ok"):
    head = ("#!/bin/sh\n"
            '[ "$*" = "%s" ] || exit 9\n'
            '[ -z "$MADO_CANARY" ] || exit 9\n'
            "[ -p /dev/stdin ] && exit 9\n"
            "for v in $(env | cut -d= -f1); do case $v in PATH|XDG_RUNTIME_DIR|"
            "DBUS_SESSION_BUS_ADDRESS|LC_ALL|PWD|SHLVL|_|OLDPWD) ;; *) exit 9;; "
            "esac; done\n" % LIVE_ARGS)
    if mode == "fail":
        return head + "exit 1\n"
    if mode == "large":
        return head + "head -c 9000000 /dev/zero | tr '\\0' x\n"
    return head + "printf '%%s' '%s' | base64 -d\n" % data_b64


def prepare(tmp, name, journal, live=None, stub_mode="ok"):
    d = os.path.join(tmp, name)
    fx, mark = os.path.join(d, "fx"), os.path.join(d, "mark")
    os.makedirs(os.path.join(fx, "bin"))
    os.makedirs(mark)
    for p in (d, fx, os.path.join(fx, "bin")):
        os.chmod(p, 0o755)
    jp = os.path.join(fx, "journal.txt")
    with open(jp, "wb") as fh:
        fh.write(journal)
    stub = os.path.join(fx, "bin", "journalctl")
    if live is None:
        body = STUB_FILE % os.path.join(mark, "hit")
    else:
        body = live_stub(base64.b64encode(journal).decode(), stub_mode)
    with open(stub, "w") as fh:
        fh.write(body)
    os.chmod(stub, 0o755)
    os.chmod(mark, 0o777)
    return d, fx, mark, jp, stub


def execute(tool, d, fx, mark, argv, canary=False, path_first=True):
    env = {"XDG_RUNTIME_DIR": "/run/user/1000"}
    if canary:
        env["MADO_CANARY"] = "1"
    path = (os.path.join(fx, "bin") + ":/usr/bin") if path_first else "/usr/bin"
    return run_sandboxed(tool, d, argv, path, ro=[os.path.dirname(tool)],
                         rw=[mark], cwd=fx, extra_env=env)


def judge(rc, out, err, want_rc, want_out, mark, file_mode):
    if os.path.exists(os.path.join(mark, "hit")) and file_mode:
        return 0, "spawned_process_in_file_mode"
    if rc != want_rc:
        return 0, "rc=%s want=%s" % (rc, want_rc)
    if out.decode("utf-8", "replace") != want_out:
        a = out.decode("utf-8", "replace").splitlines()
        b = want_out.splitlines()
        for k in range(max(len(a), len(b))):
            if (a[k] if k < len(a) else None) != (b[k] if k < len(b) else None):
                ga = a[k][:100] if k < len(a) else None
                wb = b[k][:100] if k < len(b) else None
                return 0, "stdout line %d got=%r want=%r" % (k + 1, ga, wb)
        return 0, "stdout differs"
    if want_rc in (0, 1, 3) and err:
        return 0, "stderr=%r" % err[:80]
    return 1, "ok"


def setup_line(reason):
    return "MADO_GLOBALS: SETUP %s\n" % reason


def score_gen(tool, tmp, rev, nonce, i):
    text, expects, diff = gen_fixture(rev, nonce, i)
    gen_sessions_check(i, text)
    raw = text.encode("utf-8", "surrogateescape") if "\xe9" not in text \
        else text.encode("latin-1", "replace")
    d, fx, mark, jp, _ = prepare(tmp, "gen%d" % i, raw)
    argv = ["--journal-file", jp]
    for e in expects:
        argv += ["--expect", e]
    if diff:
        argv.append("--diff")
    want_out, want_rc = model_out(raw.decode("utf-8", "replace"), expects, diff)
    rc, out, err = execute(tool, d, fx, mark, argv)
    return judge(rc, out, err, want_rc, want_out, mark, True)


def score_file_case(tool, tmp, rev, nonce, name, journal, argv_extra, expects,
                    diff, want=None):
    d, fx, mark, jp, _ = prepare(tmp, name, journal)
    argv = ["--journal-file", jp] + argv_extra
    if want is None:
        want = model_out(journal.decode("utf-8", "replace"), expects, diff)
    rc, out, err = execute(tool, d, fx, mark, argv)
    return judge(rc, out, err, want[1], want[0], mark, True)


def sample_journal(rev, nonce, tag, n=3):
    rng = rng_for(rev, nonce, tag, 0)
    lines = []
    for k in range(n):
        pid = str(rng.randrange(100, 99999))
        ts = ts_of(rng, k)
        for name in rng.sample(sorted(TABLE) + COMMON, 6):
            lines.append(advert(ts, "h", pid, name, rng.randrange(1, 9)))
    return ("\n".join(lines) + "\n").encode()


def score_diff0(tool, tmp, rev, nonce):
    return score_file_case(tool, tmp, rev, nonce, "diff0",
                           sample_journal(rev, nonce, "diff0"), ["--diff"], [],
                           True)


def score_diff1(tool, tmp, rev, nonce):
    return score_file_case(tool, tmp, rev, nonce, "diff1",
                           sample_journal(rev, nonce, "diff1", 1), ["--diff"],
                           [], True)


def score_expect0(tool, tmp, rev, nonce):
    j = sample_journal(rev, nonce, "expect0", 1)
    names = sorted(model_sessions(j.decode())[-1]["names"])
    ex = names[:3]
    return score_file_case(tool, tmp, rev, nonce, "expect0", j,
                           sum((["--expect", e] for e in ex), []), ex, False)


def score_expectmiss0(tool, tmp, rev, nonce):
    j = sample_journal(rev, nonce, "expectmiss0", 1)
    names = sorted(model_sessions(j.decode())[-1]["names"])
    ex = [names[0], "zz_absent_b", "zz_absent_a", "zz_absent_b"]
    return score_file_case(tool, tmp, rev, nonce, "expectmiss0", j,
                           sum((["--expect", e] for e in ex), []), ex, False)


def score_nosess0(tool, tmp, rev, nonce):
    rng = rng_for(rev, nonce, "nosess0", 0)
    j = "\n".join(noise_lines(rng, ts_of(rng, 1), "4242")).encode(
        "latin-1", "replace") + b"\n"
    return score_file_case(tool, tmp, rev, nonce, "nosess0", j,
                           ["--expect", "wl_seat"], ["wl_seat"], False)


def score_nosess1(tool, tmp, rev, nonce):
    return score_file_case(tool, tmp, rev, nonce, "nosess1", b"", ["--diff"],
                           [], True)


def score_unreadable0(tool, tmp, rev, nonce):
    d, fx, mark, jp, _ = prepare(tmp, "unreadable0", b"x\n")
    rc, out, err = execute(tool, d, fx, mark,
                           ["--journal-file", os.path.join(fx, "absent.txt")])
    return judge(rc, out, err, 2, setup_line("unreadable"), mark, True)


def score_usage0(tool, tmp, rev, nonce):
    d, fx, mark, jp, stub = prepare(tmp, "usage0", b"x\n")
    cases = [[], ["--journal-file", jp, "--live"], ["--journal-file", jp,
             "--journalctl", stub], ["--journal-fil", jp], ["--live", "--dif"],
             ["--diff"]]
    for k, argv in enumerate(cases):
        rc, out, err = execute(tool, d, fx, mark, argv)
        ok, why = judge(rc, out, err, 2, setup_line("usage"), mark, False)
        if not ok:
            return 0, "case%d %s" % (k, why)
    return 1, "ok"


def score_badexpect0(tool, tmp, rev, nonce):
    d, fx, mark, jp, _ = prepare(tmp, "badexpect0", b"x\n")
    for k, e in enumerate(["--expect=a b", "--expect=", "--expect=" + "a" * 129,
                           "--expect=a;b", "--expect=a/b"]):
        rc, out, err = execute(tool, d, fx, mark, ["--journal-file", jp, e])
        ok, why = judge(rc, out, err, 2, setup_line("bad_expect"), mark, True)
        if not ok:
            return 0, "case%d %s" % (k, why)
    return 1, "ok"


def score_toolarge0(tool, tmp, rev, nonce):
    d, fx, mark, jp, _ = prepare(tmp, "toolarge0", b"x" * (MAX_BYTES + 1))
    rc, out, err = execute(tool, d, fx, mark, ["--journal-file", jp])
    ok, why = judge(rc, out, err, 2, setup_line("too_large"), mark, True)
    if not ok:
        return ok, why
    d2, fx2, mark2, jp2, _ = prepare(tmp, "toolarge1",
                                     b"x" * (MAX_BYTES - 1) + b"\n")
    rc, out, err = execute(tool, d2, fx2, mark2, ["--journal-file", jp2])
    want = model_out("", [], False)
    return judge(rc, out, err, want[1], want[0], mark2, True)


def live_case(tool, tmp, rev, nonce, name, mode, via_path, canary=False,
              writable=False):
    j = sample_journal(rev, nonce, name, 2)
    d, fx, mark, jp, stub = prepare(tmp, name, j, live=True, stub_mode=mode)
    if writable:
        os.chmod(stub, 0o775)
    argv = ["--live", "--diff"] if via_path else ["--live", "--diff",
                                                   "--journalctl", stub]
    rc, out, err = execute(tool, d, fx, mark, argv, canary=canary)
    if mode == "ok" and not writable:
        want = model_out(j.decode(), [], True)
        return judge(rc, out, err, want[1], want[0], mark, False)
    reason = "journalctl_unusable" if writable else (
        "journalctl_too_large" if mode == "large" else "journalctl_failed")
    return judge(rc, out, err, 5, setup_line(reason), mark, False)


def score_live0(tool, tmp, rev, nonce):
    return live_case(tool, tmp, rev, nonce, "live0", "ok", False)


def score_live1(tool, tmp, rev, nonce):
    return live_case(tool, tmp, rev, nonce, "live1", "ok", True)


def score_livefail0(tool, tmp, rev, nonce):
    return live_case(tool, tmp, rev, nonce, "livefail0", "fail", False)


def score_liveenv0(tool, tmp, rev, nonce):
    return live_case(tool, tmp, rev, nonce, "liveenv0", "ok", False,
                     canary=True)


def score_livewritable0(tool, tmp, rev, nonce):
    return live_case(tool, tmp, rev, nonce, "livewritable0", "ok", False,
                     writable=True)


def score_livelarge0(tool, tmp, rev, nonce):
    return live_case(tool, tmp, rev, nonce, "livelarge0", "large", False)


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
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name) and f.id in CALL_DENY:
                return False
            if isinstance(f, ast.Attribute):
                if f.attr in CALL_DENY and isinstance(f.value, ast.Name) \
                        and f.value.id in ("builtins", "__builtins__"):
                    return False
                if isinstance(f.value, ast.Name) and f.value.id == "os" \
                        and False:
                    return False
            for kw in node.keywords:
                if kw.arg == "shell" and not (
                        isinstance(kw.value, ast.Constant)
                        and kw.value.value is False):
                    return False
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if any(s in node.value for s in STR_DENY):
                return False
    return bool(mods) and mods <= STDLIB_ALLOW and not (mods & STDLIB_DENY)


def selftest_result(tool, scratch):
    rc, out, err = run_sandboxed(tool, scratch, ["--selftest"], "/usr/bin",
                                 timeout=300)
    m = re.search(r"MADO_GLOBALS_SELFTEST: (\d+)/(\d+) passed",
                  (out or b"").decode("utf-8", "replace"))
    k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return rc, k, n, m is not None


NOT_SITES = ("selftest", "_check", "_run", "_write", "main", "usage")
FLIP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.GtE,
        ast.GtE: ast.Lt, ast.Gt: ast.LtE, ast.LtE: ast.Gt, ast.In: ast.NotIn,
        ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}


def function_sites(src):
    tree = ast.parse(src)
    sites = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        if any(s in fn.name for s in NOT_SITES):
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


def teeth(src, tmp, nonce):
    sites = function_sites(src)
    if len(sites) < MIN_SITES:
        print("%s clause=b2 sites=%d (<%d)" % (PRED, len(sites), MIN_SITES))
        return False
    rng = random.Random(int(hashlib.sha256(("mut:" + nonce).encode())
                            .hexdigest(), 16))
    killed = 0
    for n, site in enumerate(rng.sample(sites, N_MUT)):
        mutated = mutate_source(src, site)
        if mutated is None:
            continue
        d = os.path.join(tmp, "mut%d" % n)
        os.makedirs(d)
        os.chmod(d, 0o755)
        path = os.path.join(d, "mado-globals.py")
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
    if git(repo, "show", "%s:%s" % (base, TOOL)) is not None:
        raise Setup("precondition_failed tool_present_at_base")
    src = open(args.tool, "rb").read() if args.tool else \
        git(repo, "show", "%s:%s" % (rev, TOOL))
    present = src is not None
    cl = {"a": int(present), "b": 0, "b2": 0, "g": 0}
    passed = 0
    if present:
        cl["g"] = int(imports_ok(src))
        tmp = tempfile.mkdtemp(prefix="mado-c1r41-")
        os.chmod(tmp, 0o755)
        try:
            td = os.path.join(tmp, "tool")
            os.makedirs(td)
            tool = os.path.join(td, "mado-globals.py")
            with open(tool, "wb") as fh:
                fh.write(src)
            rc, k, n, has = selftest_result(tool, td)
            cl["b"] = int(rc == 0 and has and k == n and n >= MIN_SELFTEST)
            print("%s clause=b rc=%s selftest=%d/%d" % (PRED, rc, k, n))
            if cl["b"]:
                cl["b2"] = int(teeth(src.decode("utf-8", "replace"), tmp,
                                     nonce))
            cases = [("gen%d" % i, (lambda i=i: score_gen(tool, tmp, rev, nonce,
                                                          i))) for i in range(8)]
            for name, fn in (
                    ("diff0", score_diff0), ("diff1", score_diff1),
                    ("expect0", score_expect0),
                    ("expectmiss0", score_expectmiss0),
                    ("nosess0", score_nosess0), ("nosess1", score_nosess1),
                    ("unreadable0", score_unreadable0),
                    ("usage0", score_usage0), ("badexpect0", score_badexpect0),
                    ("toolarge0", score_toolarge0), ("live0", score_live0),
                    ("live1", score_live1), ("livefail0", score_livefail0),
                    ("liveenv0", score_liveenv0),
                    ("livewritable0", score_livewritable0),
                    ("livelarge0", score_livelarge0)):
                cases.append((name, (lambda fn=fn: fn(tool, tmp, rev, nonce))))
            assert len(cases) == TOTAL, len(cases)
            for name, fn in cases:
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

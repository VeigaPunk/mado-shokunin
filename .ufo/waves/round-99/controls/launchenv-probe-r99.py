r"""mado round-99 C1 oracle case builder (seat R99MExecOracle).

Instrument, not candidate: this file spawns the installed /usr/bin/gio
(`gio launch`) per case, so it sits outside the candidate's structural
allowlist (QUALITY 162/165 exemption for instruments; the instrument and
candidate roles are named in the round report). stdlib only.

Contract 2 (launch spawn environment, claims-declaration-r99.md): given one
case dict, materialise the case root -- files from base64 at 0755 unless the
case's "modes" map overrides, '/'-less rel keys whose parents are created,
"dirs" entries as directories, the default probe at probe.sh, the desktop
file rendered from the case's desktop block with {root}/{probe} substituted
into the case values (or desktop_raw bytes verbatim, substituted) -- then
run, with cwd = the case root,

  env -i LC_ALL=C HOME=<root>/h PROBE_OUT=<root>/out \
      PATH=<root>-relative case entries joined by ':' \
      /usr/bin/gio launch <root>/case.desktop <root>/<arg>...

with a 10 s timeout and a 1.5 s quiet wait for the children before the out
file is parsed (gio launch returns before its children write; M98-1).  A
case with "path": null runs WITHOUT a PATH variable in the environment
(unset-PATH default "/bin:/usr/bin:." per gutils.c).  A case with
"rel_desktop": true passes the bare name "case.desktop" instead of the
absolute path (GIO_LAUNCHED_DESKTOP_FILE then measures as the relative
argument, R5).  A case with "args_rel": true passes its args verbatim
(relative, resolved by gio against its process cwd) instead of root-joined.

The probe program (PROBE_SH) appends ONE record line per spawn to $PROBE_OUT
with a single printf (one write, O_APPEND: atomic for these line lengths, no
flock), so concurrent spawns cannot interleave a record (M98-7) and the
surface stays the launch count plus the multiset of argv vectors (M98-10;
multi-spawn argv lists are frozen sorted):

  REC ARGV0=$0 ARGC=$# CWD=<pwd> GDF=<GIO_LAUNCHED_DESKTOP_FILE|-> A1=.. An=

stdout: exactly one JSON object
  {"launches": N, "argv": [[...], ...], "cwd": "...", "env_gdf": "..."}
                                         on a clean measurement
  {"error": "<cause>"}                   on a measured refusal
  {"error": "setup-error"}               on an unsealed/incomplete record
argv values, cwd and env_gdf are canonicalised: the probe path prints as
"{probe}", the case root as "{root}", values under the root as "{root}/...".

Refusal causes (candidate taxonomy; construction first, stderr second):
  construction (the case shape dictates the defect):
    no-exec       no Exec key or an empty Exec value
    desktop-file  a value GKeyFile refuses on load: desktop_raw without a
                  [Desktop Entry] group, or an Exec escape outside
                  {\s,\n,\t,\r,\\} (M98-3: the escape dies in GKeyFile,
                  before any shell parsing)
    exec-parse    an Exec GKeyFile loads but g_shell_parse_argv rejects
                  (unbalanced quote)
  stderr (same "Unable to load application information" line for all
  load-time refusals, so the message alone cannot separate them):
    load               Exec argv[0] / TryExec not found, or names a
                       directory, or is not executable (R1/R1b/R7)
    no-terminal        "Unable to find terminal required for application" (R2)
    cwd-failed         "Failed to change to directory" (R4)
    program-not-found  "not found in $PATH" (R3; reachable via Exec=%k)

Usage:
  launchenv-probe-r99.py CASE.json [--parent DIR] [--keep]
  launchenv-probe-r99.py - [--parent DIR]        (case dict on stdin)
  launchenv-probe-r99.py --selftest

One "MADO_LAUNCHENV_PROBE_META:" line on stderr carries {rc, stderr,
records, cause, gio_sha256} for the freeze log.  gio pin (measured
2026-11-07, glib2 2.90.1-1): sha256 d2164260...c462, re-hashed every run;
on mismatch a MADO_LAUNCHENV_PROBE_GIO_MISMATCH line goes to stderr and the
run continues (the caller decides what a different binary may freeze).
"""

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

GIO = "/usr/bin/gio"
GIO_SHA256 = "d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462"
GLIB2 = "2.90.1-1"
GIO_TIMEOUT_S = 10.0
QUIET_S = 1.5
OUT_CAP_S = 20.0
POLL_S = 0.05
DESKTOP_NAME = "case.desktop"
REL_DESKTOP_ARG = "case.desktop"

# gdesktopappinfo.c 2765-2778, table order is the selection order.
KNOWN_TERMINALS = [
    ("xdg-terminal-exec", None),
    ("kgx", "-e"),
    ("gnome-terminal", "--"),
    ("mate-terminal", "-x"),
    ("xfce4-terminal", "-x"),
    ("tilix", "-e"),
    ("konsole", "-e"),
    ("nxterm", "-e"),
    ("color-xterm", "-e"),
    ("rxvt", "-e"),
    ("dtterm", "-e"),
    ("xterm", "-e"),
]

PROBE_SH = """#!/bin/sh
# mado r99 launch probe: ONE record line per spawn, ONE printf (atomic
# append, no flock).  Values in mado fixtures never contain spaces or '='.
line="REC ARGV0=$0 ARGC=$# CWD=$(pwd) GDF=${GIO_LAUNCHED_DESKTOP_FILE-}"
if [ "$#" -gt 0 ]; then
  i=1
  for a in "$@"; do
    line="$line A$i=$a"
    i=$((i + 1))
  done
fi
printf '%s\\n' "$line" >> "${PROBE_OUT:?mado r99 probe needs PROBE_OUT}"
"""


def gio_sha256(path=GIO):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sub_placeholders(text, root, probe):
    return str(text).replace("{probe}", probe).replace("{root}", root)


def canon(value, root, probe):
    """Map a measured value back onto {probe}/{root} placeholders."""
    out = value.replace(probe, "{probe}")
    out = out.replace(root, "{root}")
    return out


def has_bad_keyfile_escape(val):
    """GKeyFile refuses Exec escapes outside {\\s,\\n,\\t,\\r,\\\\} (M98-3)."""
    i = 0
    while i < len(val):
        if val[i] == "\\":
            if i + 1 >= len(val) or val[i + 1] not in "sntr\\":
                return True
            i += 2
        else:
            i += 1
    return False


def has_unbalanced_quote(val):
    """Odd number of unescaped double quotes: g_shell_parse_argv refuses."""
    n = 0
    i = 0
    while i < len(val):
        c = val[i]
        if c == "\\":
            i += 2
            continue
        if c == '"':
            n += 1
        i += 1
    return n % 2 == 1


def structural_cause(case):
    """Cause dictated by the case's construction, checked before gio runs.

    Returns one of "no-exec", "exec-parse", "desktop-file" or None.  Every
    load-time refusal prints the same gio line, so the message alone cannot
    separate these; the builder knows which defect each case plants.
    """
    if case.get("desktop_raw") is not None:
        raw = sub_placeholders(case["desktop_raw"], "{root}", "{probe}")
        if "[Desktop Entry]" not in raw:
            return "desktop-file"
        return None
    d = case.get("desktop") or {}
    exec_val = d.get("Exec")
    if exec_val is None or exec_val == "":
        return "no-exec"
    if has_bad_keyfile_escape(exec_val):
        return "desktop-file"
    if has_unbalanced_quote(exec_val):
        return "exec-parse"
    return None


def path_string(case, root):
    """The PATH string for the probe environment, or None for unset."""
    entries = case.get("path", [])
    if entries is None:
        return None
    probe = os.path.join(root, "probe.sh")
    return ":".join(sub_placeholders(e, root, probe) for e in entries)


def render_desktop(case, root, probe):
    """The one desktop-file renderer (M98-8): literal values, fixed order."""
    d = case.get("desktop") or {}
    if case.get("desktop_raw") is not None:
        return sub_placeholders(case["desktop_raw"], root, probe).encode("ascii")
    lines = ["[Desktop Entry]"]
    for key in ("Type", "Name", "Exec", "TryExec", "Path", "Terminal",
                "Hidden", "X-GIO-NoFuse"):
        if key not in d or d[key] is None:
            continue
        val = d[key]
        if isinstance(val, bool):
            val = "true" if val else "false"
        lines.append("%s=%s" % (key, sub_placeholders(val, root, probe)))
    return ("\n".join(lines) + "\n").encode("ascii")


def build_root(case, parent):
    """Materialise one case root; returns (root, desktop_path, probe_path)."""
    case_id = case["id"]
    root = os.path.join(parent, case_id)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "h"))
    for rel in sorted(case.get("files") or {}):
        dst = os.path.join(root, rel)
        parent_dir = os.path.dirname(dst)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(base64.b64decode(case["files"][rel]))
        os.chmod(dst, 0o755)
    for rel in case.get("dirs") or []:
        os.makedirs(os.path.join(root, rel), exist_ok=True)
    modes = case.get("modes") or {}
    for rel, octal in sorted(modes.items()):
        os.chmod(os.path.join(root, rel), int(octal, 8))
    probe = os.path.join(root, "probe.sh")
    with open(probe, "w", encoding="ascii", newline="\n") as fh:
        fh.write(PROBE_SH)
    os.chmod(probe, 0o755)
    desktop_path = os.path.join(root, DESKTOP_NAME)
    with open(desktop_path, "wb") as fh:
        fh.write(render_desktop(case, root, probe))
    return root, desktop_path, probe


def parse_out(text):
    """Return (records, complete) from the probe out file.

    One record per line: REC ARGV0=.. ARGC=.. CWD=.. GDF=.. [Ai=..]..
    A record is complete when ARGC parses and matches the A-field count.
    """
    records = []
    complete = True
    for line in text.split("\n"):
        if not line:
            continue
        if not line.startswith("REC "):
            complete = False
            continue
        argv0 = None
        argc = None
        cwd = None
        gdf = None
        args = {}
        order_ok = True
        seen_argc = False
        seen_cwd = False
        seen_gdf = False
        for field in line.split(" ")[1:]:
            if "=" not in field:
                order_ok = False
                continue
            key, val = field.split("=", 1)
            if key == "ARGV0" and argv0 is None and not seen_argc:
                argv0 = val
            elif key == "ARGC" and not seen_argc and argc is None:
                seen_argc = True
                if val.isdigit():
                    argc = int(val)
                else:
                    order_ok = False
            elif key.startswith("A") and key[1:].isdigit() and seen_argc:
                args[int(key[1:])] = val
            elif key == "CWD" and not seen_cwd:
                seen_cwd = True
                cwd = val
            elif key == "GDF" and not seen_gdf:
                seen_gdf = True
                gdf = val
            else:
                order_ok = False
        if (argv0 is None or argc is None or cwd is None or gdf is None
                or not order_ok or sorted(args) != list(range(1, argc + 1))):
            complete = False
            continue
        argv = [argv0] + [args[i] for i in range(1, argc + 1)]
        records.append({"argv": argv, "cwd": cwd, "gdf": gdf})
    return records, complete


def quiet_read(out_path, exited_at):
    """Wait for the out file to go quiet, then return its bytes.

    A refusal never spawns a child, so the file may never appear: once gio
    has exited and QUIET_S has passed with no file (or an empty file),
    conclude the empty record set.  Returns None only when the overall cap
    is exceeded (caller turns that into setup-error).
    """
    quiet_since = None
    last_sig = None
    start = time.monotonic()
    while True:
        try:
            st = os.stat(out_path)
            sig = (st.st_size, st.st_mtime_ns)
        except OSError:
            sig = None
        if sig is not None and sig[0] > 0:
            if sig == last_sig and quiet_since is not None:
                if time.monotonic() - quiet_since >= QUIET_S:
                    with open(out_path, "r", encoding="utf-8",
                              errors="replace") as fh:
                        return fh.read()
            else:
                quiet_since = time.monotonic()
                last_sig = sig
        else:
            if (exited_at is not None
                    and time.monotonic() - exited_at >= QUIET_S
                    and (sig is None or sig[0] == 0)):
                return ""
        if time.monotonic() - start > OUT_CAP_S:
            return None
        time.sleep(POLL_S)


def stderr_cause(stderr_text):
    if "Unable to find terminal required" in stderr_text:
        return "no-terminal"
    if "Failed to change to directory" in stderr_text:
        return "cwd-failed"
    if "not found in $PATH" in stderr_text:
        return "program-not-found"
    if "Unable to load application information" in stderr_text:
        return "load"
    return None


def measure_once(case, parent, pin, keep=False):
    """Materialise, launch, read.  Returns (expect, meta)."""
    root, desktop_path, probe = build_root(case, parent)
    out_path = os.path.join(root, "out")
    argv = [GIO, "launch",
            REL_DESKTOP_ARG if case.get("rel_desktop") else desktop_path]
    for a in case.get("args") or []:
        if case.get("args_rel"):
            argv.append(sub_placeholders(a, root, probe))
        else:
            argv.append(os.path.join(root, sub_placeholders(a, root, probe)))
    env = {
        "LC_ALL": "C",
        "HOME": os.path.join(root, "h"),
        "PROBE_OUT": out_path,
    }
    pstr = path_string(case, root)
    if pstr is not None:
        env["PATH"] = pstr
    meta = {"rc": None, "stderr": "", "records": 0, "cause": None,
            "gio_sha256": pin}
    try:
        proc = subprocess.Popen(
            argv, cwd=root, env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except OSError as exc:
        shutil.rmtree(root, ignore_errors=True)
        return {"error": "setup-error"}, dict(meta, stderr=str(exc))
    try:
        _, err = proc.communicate(timeout=GIO_TIMEOUT_S)
        meta["rc"] = proc.returncode
        meta["stderr"] = err.decode("utf-8", "replace") if err else ""
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        shutil.rmtree(root, ignore_errors=True)
        return {"error": "setup-error"}, dict(meta, stderr="timeout")
    exited_at = time.monotonic()
    text = quiet_read(out_path, exited_at)
    records = []
    complete = False
    if text is not None:
        records, complete = parse_out(text)
    meta["records"] = len(records)
    if meta["rc"] == 0 and complete and records:
        vectors = sorted(rec["argv"] for rec in records)
        cwds = {rec["cwd"] for rec in records}
        gdfs = {rec["gdf"] for rec in records}
        if len(cwds) != 1 or len(gdfs) != 1:
            shutil.rmtree(root, ignore_errors=True)
            return {"error": "setup-error"}, meta
        expect = {
            "launches": len(records),
            "argv": [[canon(v, root, probe) for v in vec] for vec in vectors],
            "cwd": canon(cwds.pop(), root, probe),
            "env_gdf": canon(gdfs.pop(), root, probe),
        }
    elif complete and not records:
        cause = structural_cause(case) or stderr_cause(meta["stderr"])
        if cause is None:
            cause = "setup-error"
        expect = {"error": cause}
        meta["cause"] = cause
    else:
        expect = {"error": "setup-error"}
    if not keep:
        shutil.rmtree(root, ignore_errors=True)
    return expect, meta


def expect_equal(a, b):
    return a == b


def measure_case(case, parent, pin, runs=2, keep=False):
    """Measure a case `runs` times; returns (expect, metas, agreed)."""
    metas = []
    expect = None
    for _ in range(runs):
        expect_i, meta = measure_once(case, parent, pin, keep=keep)
        metas.append(meta)
        if expect_i.get("error") == "setup-error":
            return expect_i, metas, False
        if expect is None:
            expect = expect_i
        elif not expect_equal(expect, expect_i):
            return expect_i, metas, False
    return expect, metas, True


def selftest():
    checks = []
    failed = 0

    def check(name, ok):
        nonlocal failed
        checks.append(name)
        if not ok:
            failed += 1

    case = {"id": "t", "desktop": {"Type": "Application", "Name": "n",
                                   "Exec": "{probe} %f", "Path": "{root}/w",
                                   "Terminal": True}}
    rendered = render_desktop(case, "/R", "/R/probe.sh").decode("ascii")
    check("render-order",
          rendered == "[Desktop Entry]\nType=Application\nName=n\n"
                      "Exec=/R/probe.sh %f\nPath=/R/w\nTerminal=true\n")
    check("render-empty-value",
          "Path=\n" in render_desktop({"id": "t", "desktop": {"Path": ""}},
                                      "/R", "/R/probe.sh").decode("ascii"))
    raw = render_desktop({"id": "t", "desktop_raw": "[Desktop Entry]\n"},
                         "/R", "/R/probe.sh")
    check("render-raw", raw == b"[Desktop Entry]\n")
    recs, comp = parse_out(
        "REC ARGV0=/R/p ARGC=2 CWD=/R GDF=/R/c.desktop A1=x A2=y\n"
        "REC ARGV0=/R/p ARGC=0 CWD=/R GDF=/R/c.desktop\n")
    check("parse-records",
          comp and len(recs) == 2 and recs[0]["argv"] == ["/R/p", "x", "y"]
          and recs[1]["argv"] == ["/R/p"])
    recs2, comp2 = parse_out("REC ARGV0=/R/p ARGC=2 CWD=/R GDF=g A1=x\n")
    check("parse-incomplete", (not comp2) and recs2 == [])
    check("canon", canon("/R/p x", "/R", "/R/p") == "{probe} x")
    check("cause-noexec", structural_cause({"desktop": {}}) == "no-exec")
    check("cause-badescape",
          structural_cause({"desktop": {"Exec": "p a\\z"}}) == "desktop-file")
    check("cause-quote",
          structural_cause({"desktop": {"Exec": 'p "open'}}) == "exec-parse")
    check("cause-ok-escape",
          structural_cause({"desktop": {"Exec": "p a\\\\ b"}}) is None)
    check("cause-desktop-file",
          structural_cause({"desktop_raw": "hello\n"}) == "desktop-file")
    check("stderr-map",
          stderr_cause("x Unable to find terminal required for application")
          == "no-terminal"
          and stderr_cause('gio: Failed to change to directory "x"')
          == "cwd-failed"
          and stderr_cause("Program 'p' not found in $PATH")
          == "program-not-found"
          and stderr_cause("Unable to load application information for 'd'")
          == "load")
    check("term-table",
          len(KNOWN_TERMINALS) == 12 and KNOWN_TERMINALS[0] ==
          ("xdg-terminal-exec", None) and KNOWN_TERMINALS[1] == ("kgx", "-e"))
    check("path-unset", path_string({"path": None}, "/R") is None)
    check("path-join",
          path_string({"path": ["{root}/bin", "", "."]}, "/R")
          == "/R/bin::.")

    print("MADO_LAUNCHENV_PROBE_SELFTEST: checks=%d failed=%d"
          % (len(checks), failed))
    return 1 if failed else 0


def default_parent():
    base = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
    return os.path.join(base, "mado-r99", "R99MExecOracle", "roots")


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado r99 C1 oracle case builder")
    ap.add_argument("case", nargs="?", help="case JSON file, or - for stdin")
    ap.add_argument("--parent", default=None)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--json", action="store_true",
                    help="accepted for contract symmetry; JSON is the default")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    parent = args.parent or default_parent()
    os.makedirs(parent, exist_ok=True)
    pin = gio_sha256()
    if pin != GIO_SHA256:
        sys.stderr.write("MADO_LAUNCHENV_PROBE_GIO_MISMATCH %s\n" % pin)
    if args.case in (None, "-"):
        case = json.load(sys.stdin)
    else:
        with open(args.case, "r", encoding="utf-8") as fh:
            case = json.load(fh)
    expect, metas, agreed = measure_case(case, parent, pin, keep=args.keep)
    sys.stderr.write("MADO_LAUNCHENV_PROBE_META: %s\n"
                     % json.dumps({"rc": metas[-1].get("rc"),
                                   "stderr": metas[-1].get("stderr", "")[-400:],
                                   "records": metas[-1].get("records"),
                                   "cause": metas[-1].get("cause"),
                                   "agreed": agreed,
                                   "gio_sha256": pin}))
    print(json.dumps(expect))
    return 0


if __name__ == "__main__":
    sys.exit(main())

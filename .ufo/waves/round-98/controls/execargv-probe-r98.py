#!/usr/bin/env python3
"""mado round-98 C1 oracle case builder (seat R98MExecOracle).

Instrument, not candidate: this file spawns the installed /usr/bin/gio
(`gio launch`) per case, so it sits outside the candidate's structural
allowlist (QUALITY 162/165 exemption for instruments; the instrument and
candidate roles are named in the round report). stdlib only.

Contract 2 (sequence semantics per the L1's 16:5x update): given one case
dict, materialise the case root -- files from base64, '/'-suffixed keys as
directories, probe.sh 0755, the desktop file from the case's desktop block
with {probe}/{root} substituted -- then run

  env -i LC_ALL=C HOME=<root>/h PATH=/usr/bin:/bin /usr/bin/gio launch \
      <root>/case.desktop <args...>

with a 10 s timeout. The Exec first token {probe} is a shell script that
writes one argv record per spawn to its own <probe>.out.<seq>: a line
"@@@ <argc>" (argc counts "$@", excluding $0), then "P0=$0", then <argc> lines
"A<i>=<value>" with i = 1..argc; the argv vector is [P0, A1..A<argc>].
GIO may spawn several processes for one case
(single-instance field codes and the no-substitution rule consume one
argument per launch iteration, gdesktopappinfo.c do/while dup_uris loop).
Shared-append interleaving was measured (two children appending one record
each to the same file corrupt both), so per the amended declaration each
probe child takes a sequence number under a flock and writes its record to
its own <probe>.out.<seq> file; the builder waits for the whole .out.* set
to go quiet (2 s quiet window, 20 s cap; the declaration measured a 1.5 s
delayed write truncating a 200 ms window 4/4 trials) and parses it in sequence
order, which is spawn order by construction of the lock.

stdout: exactly one JSON object
  {"launches": N, "argv": [[...], ...]}   on a clean measurement
  {"error": "<cause>"}                    on a measured refusal
  {"error": "setup-error"}                on an unsealed/incomplete record
A refusal is a `gio launch` that exits nonzero, or one that leaves no
complete probe record. The cause (contract 1 vocabulary) is derived
structurally from the case: no Exec key -> "no-exec"; not a key file (no
[Desktop Entry] group), no Type=Application, or an Exec value carrying a
GKeyFile escape outside {\\s,\\n,\\t,\\r,\\\\} -> "desktop-file";
otherwise (an Exec line g_shell_parse_argv would reject) -> "exec-parse".
The cause is only printed after gio confirmed the refusal.

The measured root path is mapped back onto the case placeholders: argv
values equal to the probe script print as "{probe}", values under the case
root print as "{root}/...", the root itself as "{root}". Frozen expects are
therefore independent of the build directory.

Usage:
  execargv-probe-r98.py CASE.json [--parent DIR] [--keep] [--json]
  execargv-probe-r98.py - [--parent DIR]          (case dict on stdin)

--json is accepted for contract symmetry; the expect JSON is the default
and only stdout. One "MADO_EXECARGV_PROBE_META:" line on stderr carries
{rc, stderr, records, gio_sha256} for the freeze log.

gio pin (measured 2026-11-07, glib2 2.90.1-1):
  /usr/bin/gio sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462
The pin is re-hashed at every run; on mismatch a
MADO_EXECARGV_PROBE_GIO_MISMATCH line goes to stderr and the run continues
(the caller decides what a different binary may freeze).
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
QUIET_S = 2.0
OUT_CAP_S = 20.0
POLL_S = 0.05
DESKTOP_NAME = "case.desktop"

PROBE_SH = """#!/bin/sh
# mado r98 launch probe: write one argv record per spawn to $0.out.<seq>.
# Sequence numbers are taken under a lock, so file order is spawn order.
exec 9>"$0.lock"; flock 9; n=$(cat "$0.seq" 2>/dev/null || echo 0); n=$((n+1)); echo "$n" > "$0.seq"; flock -u 9
{ printf '@@@ %s\\n' "$#"; printf 'P0=%s\\n' "$0"; i=1; for a in "$@"; do printf 'A%d=%s\\n' "$i" "$a"; i=$((i+1)); done; } > "$0.out.$n"
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
    """Map a measured argv value back onto {probe}/{root} placeholders.

    Substitutes the probe path and the case root anywhere in the value:
    attached field codes (e.g. "end%f") can embed the root mid-token, and
    a prefix-only rewrite would leak a transient absolute path.
    """
    out = value.replace(probe, "{probe}")
    out = out.replace(root, "{root}")
    return out


def render_desktop(case, root, probe):
    d = case.get("desktop") or {}
    if case.get("desktop_raw") is not None:
        return sub_placeholders(case["desktop_raw"], root, probe).encode("ascii")
    lines = ["[Desktop Entry]"]
    for key in ("Type", "Name", "Icon", "Exec", "Path", "Terminal", "Hidden",
                "X-GIO-NoFuse"):
        if key not in d or d[key] is None:
            continue
        val = d[key]
        if isinstance(val, bool):
            val = "true" if val else "false"
        lines.append("%s=%s" % (key, sub_placeholders(val, root, probe)))
    return ("\n".join(lines) + "\n").encode("ascii")


def build_root(case, parent):
    case_id = case["id"]
    root = os.path.join(parent, case_id)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "h"))
    for rel in sorted(case.get("files") or {}):
        dst = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(dst, exist_ok=True)
        else:
            parent_dir = os.path.dirname(dst)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(dst, "wb") as fh:
                fh.write(base64.b64decode(case["files"][rel]))
    probe = os.path.join(root, "probe.sh")
    with open(probe, "w", encoding="ascii", newline="\n") as fh:
        fh.write(PROBE_SH)
    os.chmod(probe, 0o755)
    desktop_path = os.path.join(root, DESKTOP_NAME)
    with open(desktop_path, "wb") as fh:
        fh.write(render_desktop(case, root, probe))
    return root, desktop_path, probe


def gio_argv(case, root, desktop_path):
    argv = [GIO, "launch", desktop_path]
    for a in case.get("args") or []:
        if a["kind"] == "file":
            argv.append(os.path.join(root, sub_placeholders(a["path"], root, "")))
        else:
            argv.append(sub_placeholders(a["uri"], root, ""))
    return argv


def parse_records(text):
    """Return (complete_records, all_complete) from probe.sh.out bytes."""
    records = []
    complete = True
    cur = None

    def sealed(rec):
        return (rec is not None and rec["argc"] is not None
                and rec["p0"] is not None
                and len(rec["vals"]) == rec["argc"])

    for line in text.split("\n"):
        if line.startswith("@@@"):
            if cur is not None and not sealed(cur):
                complete = False
                records.pop()
            head = line[3:].strip()
            cur = {"argc": int(head) if head.isdigit() else None,
                   "p0": None, "vals": []}
            records.append(cur)
            if cur["argc"] is None:
                complete = False
        elif cur is None:
            if line.strip():
                complete = False
        else:
            if line.startswith("P0="):
                cur["p0"] = line[3:]
            elif line.startswith("A") and "=" in line:
                cur["vals"].append(line[1:].split("=", 1)[1])
            elif line != "":
                complete = False
    if cur is not None and not sealed(cur):
        complete = False
        records.pop()
    return records, complete


def probe_record_files(probe):
    """Record files <probe>.out.<seq>, sorted by sequence (spawn order)."""
    parent = os.path.dirname(probe)
    prefix = os.path.basename(probe) + ".out."
    try:
        names = os.listdir(parent)
    except OSError:
        return []
    found = []
    for name in names:
        if name.startswith(prefix):
            suffix = name[len(prefix):]
            if suffix.isdigit():
                found.append((int(suffix), os.path.join(parent, name)))
    found.sort()
    return [path for _, path in found]


def _file_sig(path):
    try:
        st = os.stat(path)
        return (st.st_size, st.st_mtime_ns)
    except OSError:
        return None


def read_probe_out(probe):
    """Wait for the .out.<seq> record file set to go quiet.

    Returns (records, state): state is "ok" (the set went quiet and every
    record file sealed), "empty" (no record file ever appeared), or
    "incomplete" (a record file exists but never sealed, or the set never
    went quiet before the cap). "incomplete" is an instrument setup error,
    never a refusal label (declaration predicate iv)."""
    deadline = time.monotonic() + OUT_CAP_S
    last_sig = None
    last_change = time.monotonic()
    records = []
    while True:
        now = time.monotonic()
        paths = probe_record_files(probe)
        records = []
        complete = bool(paths)
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                complete = False
                continue
            recs, file_complete = parse_records(text)
            if len(recs) == 1 and file_complete:
                records.append(recs[0])
            else:
                complete = False
        sig = tuple((os.path.basename(p), _file_sig(p)) for p in paths)
        if sig != last_sig:
            last_sig = sig
            last_change = now
        if records and complete and (now - last_change) >= QUIET_S:
            return records, "ok"
        if now >= deadline:
            if paths:
                return records, "incomplete"
            return records, "empty"
        time.sleep(POLL_S)


def has_bad_keyfile_escape(val):
    """GKeyFile refuses escapes outside {\\s, \\n, \\t, \\r, \\\\} (measured)."""
    i = 0
    while i < len(val):
        if val[i] == "\\":
            if i + 1 >= len(val) or val[i + 1] not in "sntr\\":
                return True
            i += 2
        else:
            i += 1
    return False


def refusal_cause(case):
    d = case.get("desktop") or {}
    raw = case.get("desktop_raw")
    if raw is not None and "[Desktop Entry]" not in raw:
        return "desktop-file"
    if d.get("Exec") is None:
        return "no-exec"
    if d.get("Type") != "Application":
        return "desktop-file"
    if has_bad_keyfile_escape(d["Exec"]):
        return "desktop-file"
    return "exec-parse"


def case_expect(case, parent, keep=False):
    """Materialise, launch, read. Returns (expect, meta).

    expect is {"launches": N, "argv": [...]} on a clean measurement,
    {"error": <refusal cause>} on a measured refusal, or
    {"error": "setup-error"} when the probe records never sealed - an
    instrument failure that must never be frozen as a label."""
    root, desktop_path, probe = build_root(case, parent)
    meta = {}
    try:
        proc = subprocess.run(
            gio_argv(case, root, desktop_path),
            cwd=root,
            env={"LC_ALL": "C", "HOME": os.path.join(root, "h"),
                 "PATH": "/usr/bin:/bin"},
            timeout=GIO_TIMEOUT_S,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        err_lines = proc.stderr.decode("utf-8", "replace").strip().splitlines()
        meta = {
            "rc": proc.returncode,
            "stderr": err_lines[-1] if err_lines else "",
        }
        if proc.returncode != 0:
            meta["records"] = 0
            return {"error": refusal_cause(case)}, meta
        records, state = read_probe_out(probe)
        meta["records"] = len(records)
        meta["record_state"] = state
        if state == "incomplete":
            meta["setup_error"] = True
            return {"error": "setup-error"}, meta
        if not records:
            return {"error": refusal_cause(case)}, meta
        expect = {
            "launches": len(records),
            "argv": [[canon(r["p0"], root, probe)]
                     + [canon(v, root, probe) for v in r["vals"]]
                     for r in records],
        }
        return expect, meta
    finally:
        if not keep:
            shutil.rmtree(root, ignore_errors=True)


def default_parent():
    base = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
    return os.path.join(base, "mado-r98", "R98MExecOracle", "roots")


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado r98 C1 oracle case builder")
    ap.add_argument("case", help="case JSON file, or - for stdin")
    ap.add_argument("--json", action="store_true",
                    help="accepted for contract symmetry; expect JSON is the default output")
    ap.add_argument("--parent", default=None,
                    help="parent dir for the case root (default: $HYAKU_SCRATCH/.../roots)")
    ap.add_argument("--keep", action="store_true",
                    help="keep the case root for debugging")
    args = ap.parse_args(argv)

    digest = gio_sha256()
    if digest != GIO_SHA256:
        sys.stderr.write("MADO_EXECARGV_PROBE_GIO_MISMATCH expected=%s measured=%s\n"
                         % (GIO_SHA256, digest))

    parent = args.parent or default_parent()
    os.makedirs(parent, exist_ok=True)

    if args.case == "-":
        case = json.load(sys.stdin)
    else:
        with open(args.case, "r", encoding="utf-8") as fh:
            case = json.load(fh)

    expect, meta = case_expect(case, parent, keep=args.keep)
    meta["gio_sha256"] = digest
    sys.stderr.write("MADO_EXECARGV_PROBE_META: %s\n" % json.dumps(meta, sort_keys=True))
    json.dump(expect, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

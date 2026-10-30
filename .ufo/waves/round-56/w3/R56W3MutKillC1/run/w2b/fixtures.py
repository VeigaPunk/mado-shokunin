#!/usr/bin/env python3
"""R56W2MutC1CounterB — proposed kill fixtures for the non-equivalent survivors.

Each fixture is ONE mutation of the good tree at 28fc86ac (a scratch git repo built from
a minimal export of the counter-relevant paths; the lane is read-only). The baseline counter
and the mutant counter are both run on the fixture with `--rev HEAD`; the fixture KILLS the
mutant when the mutant's (rc, stdout) differs from the baseline's (rc, stdout), and the
baseline's own output must show the leg the fixture is designed to expose (`expect`).
Also runs the CLI-level check for M69.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = "/fast/scratch/hyaku/mado-r56/R56W2MutC1CounterB"
BASE = os.path.join(ROOT, "base")
MUT_DIR = os.path.join(ROOT, "mutants")
FIX_DIR = os.path.join(ROOT, "fixtures")
BASELINE = os.path.join(ROOT, "baseline.py")
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
REG = "corpus/SOURCES.md"
TABLES = ".ufo/waves/round-56/frozen-tables-v2.json"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C",
       "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}


def rd(d, rel):
    with open(os.path.join(d, rel), "rb") as fh:
        return fh.read()


def wr(d, rel, data):
    with open(os.path.join(d, rel), "wb") as fh:
        fh.write(data)


def row_index(lines, rid):
    hits = [i for i, l in enumerate(lines) if l.startswith("| %s " % rid)]
    assert len(hits) == 1, (rid, len(hits))
    return hits[0]


def s383_line(d):
    lines = rd(d, REG).split(b"\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(b"| S383 ")]
    assert len(hits) == 1
    return lines, hits[0]


def replace_once(data, old, new):
    assert data.count(old) == 1, (old, data.count(old))
    return data.replace(old, new)


def tok_of_quote(d, rid):
    t = json.loads(rd(d, TABLES))["c1"]
    q = [r for r in t["k"] if r["id"] == rid][0]["quote"]
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", q)[0]


# ------------------------------------------------------------------ fixture transforms
def f02(d):  # M02 decode policy: invalid UTF-8 byte inside an anchor locator
    b = rd(d, REG)
    wr(d, REG, replace_once(b, b"ConfigWatcher.cpp:33-34,", b"ConfigWatcher.cpp:33\xff-34,"))


def f03(d):  # M03 splitlines: CRLF entry (every line ends in a CR)
    wr(d, ENTRY, rd(d, ENTRY).replace(b"\n", b"\r\n"))


def _insert_around_row(d, rid, before, after):
    lines = rd(d, ENTRY).split(b"\n")
    i = row_index([l.decode() for l in lines], rid)
    out = lines[:i] + ([before] if before is not None else []) + [lines[i]] + ([after] if after is not None else []) + lines[i + 1:]
    wr(d, ENTRY, b"\n".join(out))


def f04(d):  # M04 fence indent 4 accepted as opener (closer stays at 3)
    _insert_around_row(d, "K05", b"    ```", b"    ```")


def f06(d):  # M06 backtick fence with backtick in info string
    _insert_around_row(d, "K05", b"``` `x`", b"```")


def f08(d):  # M08 closer indent 4 accepted
    _insert_around_row(d, "K05", b"```", b"    ```")


def f10(d):  # M10 closer trailing vertical tab accepted
    _insert_around_row(d, "K05", b"```", b"```\x0b")


def f11(d):  # M11 "<!" opens a comment
    _insert_around_row(d, "K05", b"<!DOCTYPE html>", None)


def f13(d):  # M13 "<!-->" opener closed at once by the mutant's i+=1 skip
    _insert_around_row(d, "K05", b"<!-->", b"-->")


def f19(d):  # M19 leading tab on a row
    lines = rd(d, ENTRY).split(b"\n")
    i = row_index([l.decode() for l in lines], "K05")
    lines[i] = b"\t" + lines[i]
    wr(d, ENTRY, b"\n".join(lines))


def f25(d):  # M25 right pad relaxed: row ends '`|' (no space before the final pipe)
    lines = rd(d, ENTRY).split(b"\n")
    i = row_index([l.decode() for l in lines], "K05")
    assert lines[i].endswith(b" |")
    lines[i] = lines[i][:-2] + b"|"
    wr(d, ENTRY, b"\n".join(lines))


def f29(d):  # M29 lenient_row strip dropped: trailing space after the row
    lines = rd(d, ENTRY).split(b"\n")
    i = row_index([l.decode() for l in lines], "K05")
    lines[i] = lines[i] + b" "
    wr(d, ENTRY, b"\n".join(lines))


def f33(d):  # M33 registry cells: double space before the status separator
    b = rd(d, REG)
    lines, i = s383_line(d)
    assert b"| mined | 2026-10-28 |" in lines[i]
    lines[i] = lines[i].replace(b"| mined | 2026-10-28 |", b"| mined  | 2026-10-28 |", 1)
    wr(d, REG, b"\n".join(lines))


def f37(d):  # M37 registry_id: tab after the opening pipe
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"| S383 |", b"| \tS383 |", 1)
    wr(d, REG, b"\n".join(lines))


def f42(d):  # M42 scope hi-parse guard: "33-," (dangling hyphen) crashes the mutant
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"ConfigWatcher.cpp:33-34,", b"ConfigWatcher.cpp:33-,", 1)
    wr(d, REG, b"\n".join(lines))


def f45(d):  # M45 past-EOF verdict dropped: a covering range AND a past-EOF locator
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"ConfigWatcher.cpp:33-34,", b"ConfigWatcher.cpp:33-34,9999,", 1)
    wr(d, REG, b"\n".join(lines))


def f46(d):  # M46 lo bound dropped: reversed range past EOF beside a covering locator
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"ConfigWatcher.cpp:33-34,", b"ConfigWatcher.cpp:33-34,5000-5,", 1)
    wr(d, REG, b"\n".join(lines))


def f48(d):  # M48 digit class isdigit(): superscript two after a locator
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"69,105 @", "69,105\u00b2 @".encode("utf-8"), 1)
    wr(d, REG, b"\n".join(lines))


def f49(d):  # M49 hi digit class isdigit(): superscript two after a range end
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"33-34,", "33-34\u00b2,".encode("utf-8"), 1)
    wr(d, REG, b"\n".join(lines))


def f50(d):  # M50 lo bound 18 digits: nlines unavailable (pin absent), 18-digit locator beside 33
    os.remove(os.path.join(d, ".ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp"))
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"ConfigWatcher.cpp:33-34,46,54-56,60,67,69,105 @",
                                b"ConfigWatcher.cpp:33,999999999999999999 @", 1)
    wr(d, REG, b"\n".join(lines))


def f51(d):  # M51 digit-run bound 18: zero-padded 18-digit run whose value is 3
    _append_to_prop(d, "K04", " pad 000000000000000003")


def f54(d):  # M54 digit-run boundary: a digit run followed by a letter (baseline ignores it, mutant counts it)
    _append_to_prop(d, "K04", " the 12x default")


def f55(d):  # M55 S-id boundary: S3999 (not a registry row) in the source line
    lines = rd(d, ENTRY).split(b"\n")
    j = [k for k, l in enumerate(lines[:15]) if l.startswith(b"source:")][0]
    lines[j] = lines[j] + b", S3999"
    wr(d, ENTRY, b"\n".join(lines))


def f56(d):  # M56 URL token: text after the URL inside the registry source cell
    lines, i = s383_line(d)
    lines[i] = lines[i].replace(b"inotify/ConfigWatcher.cpp |", b"inotify/ConfigWatcher.cpp (mirror) |", 1)
    wr(d, REG, b"\n".join(lines))


def f58(d):  # M58 echo threshold 31: K07 quote has exactly 30 characters
    _set_prop(d, "K07", lambda q: q + " echoed on this line, no analysis added here")


def f59(d):  # M59 K_MIN 39: a 39-character proposition (baseline row:K05 requires >= 40)
    _set_prop(d, "K05", lambda q: _pad(tok_of_quote(d, "K05") + " is set here", 39))


def f60(d):  # M60 K_MIN 41: a 40-character proposition (baseline accepts it)
    _set_prop(d, "K05", lambda q: _pad(tok_of_quote(d, "K05") + " is set here", 40))


def f62(d):  # M62 executable blob mode: entry is 100755
    os.chmod(os.path.join(d, ENTRY), 0o755)


def _pad(s, n):
    while len(s) < n:
        s += "x"
    return s[:n]


def _set_prop(d, rid, fn):
    lines = rd(d, ENTRY).split(b"\n")
    i = row_index([l.decode() for l in lines], rid)
    cells = lines[i].decode().split(" | ")
    # row: "| K05 | prop | S383 | pin | `quote` |"
    body = lines[i].decode()[2:-2]
    parts = body.split(" | ")
    assert len(parts) == 5, (rid, len(parts))
    quote = parts[4].strip("`")
    parts[1] = fn(quote)
    lines[i] = ("| " + " | ".join(parts) + " |").encode()
    wr(d, ENTRY, b"\n".join(lines))


def _append_to_prop(d, rid, extra):
    lines = rd(d, ENTRY).split(b"\n")
    i = row_index([l.decode() for l in lines], rid)
    body = lines[i].decode()[2:-2]
    parts = body.split(" | ")
    assert len(parts) == 5
    parts[1] = parts[1] + extra
    lines[i] = ("| " + " | ".join(parts) + " |").encode()
    wr(d, ENTRY, b"\n".join(lines))


FIXTURES = [
    # id, mutant, description, transform, expected baseline leg text
    ("F02", "M02", "invalid UTF-8 byte between locator 33 and -34 in the S383 anchor", f02, "scope:K* (line 34 uncovered)"),
    ("F03", "M03", "CRLF line endings in the entry", f03, "row:K* (CR is a trailing byte)"),
    ("F04", "M04", "4-space ``` line around K05 (not a fence in CommonMark)", f04, "none (TARGET_MET)"),
    ("F06", "M06", "``` `x` opener around K05 (backtick in info string)", f06, "none (TARGET_MET)"),
    ("F08", "M08", "``` opener around K05, 4-space closer after it", f08, "row:K05..K30,H01..H03"),
    ("F10", "M10", "``` opener around K05, closer with trailing VT", f10, "row:K06.. (closer does not match)"),
    ("F11", "M11", "<!DOCTYPE html> line before K05 (no close)", f11, "none (TARGET_MET)"),
    ("F13", "M13", "<!--> opener before K05, --> after it", f13, "row:K05 (K05 hidden in comment)"),
    ("F19", "M19", "leading tab on the K05 row", f19, "row:K05 only (best-effort cells survive)"),
    ("F25", "M25", "K05 row ends '`|' (no space before final pipe)", f25, "row:K05 only"),
    ("F29", "M29", "trailing space after the K05 row", f29, "row:K05 only"),
    ("F33", "M33", "double space before the S383 status separator", f33, "none (TARGET_MET)"),
    ("F37", "M37", "tab after the S383 opening pipe", f37, "none (TARGET_MET)"),
    ("F42", "M42", "S383 anchor '33-,' dangling hyphen", f42, "scope:K04.. (list ends at 33)"),
    ("F45", "M45", "S383 anchor with a covering range AND 9999", f45, "scope:K* (past-EOF verdict)"),
    ("F46", "M46", "S383 anchor with reversed range 5000-5 beside 33-34", f46, "scope:K* (past-EOF lo)"),
    ("F48", "M48", "S383 anchor '105²' (superscript digit)", f48, "none (TARGET_MET)"),
    ("F49", "M49", "S383 anchor '34²' range end", f49, "none (TARGET_MET)"),
    ("F50", "M50", "pin absent; 18-digit locator beside 33 in S383 anchor", f50, "none on scope:K03 (33 covered)"),
    ("F51", "M51", "K04 proposition gains a zero-padded 18-digit '3'", f51, "none (num:K04 passes)"),
    ("F54", "M54", "K04 proposition gains 'config7'", f54, "none (glued digits ignored)"),
    ("F55", "M55", "source line gains S3999 (not a registry row)", f55, "none (prov OK)"),
    ("F56", "M56", "S383 source cell has text after its URL", f56, "none (URL ends at whitespace)"),
    ("F58", "M58", "K07 proposition = its 30-char quote + echo text", f58, "echo:K07"),
    ("F59", "M59", "K05 proposition of exactly 39 characters", f59, "row:K05"),
    ("F60", "M60", "K05 proposition of exactly 40 characters", f60, "none (accepted)"),
    ("F62", "M62", "entry file mode 100755", f62, "none (TARGET_MET)"),
]


def git(d, *args):
    p = subprocess.run(["git", "-C", d] + list(args), env=dict(ENV, HOME=ROOT, TMPDIR=ROOT),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()))
    return p.stdout.decode().strip()


def make_fixture(fid, transform):
    os.makedirs(FIX_DIR, exist_ok=True)
    d = tempfile.mkdtemp(prefix=fid + "-", dir=FIX_DIR)
    shutil.copytree(BASE, d, dirs_exist_ok=True)
    git(d, "init", "-q", "-b", "main")
    top = git(d, "rev-parse", "--show-toplevel")
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    transform(d)
    git(d, "add", "-A", "-f")
    git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "fixture " + fid)
    return d, git(d, "rev-parse", "HEAD")


def run_counter(counter, repo, rev, work):
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(["python3", "-I", counter, "--repo", repo, "--rev", rev, "--work", work],
                       env=dict(ENV, TMPDIR=work), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.DEVNULL, timeout=300)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def main():
    results = []
    for fid, mid, desc, fn, expect in FIXTURES:
        d, rev = make_fixture(fid, fn)
        mut = os.path.join(MUT_DIR, mid + ".py")
        w = os.path.join(ROOT, "work", "fx-" + fid)
        brc, bout, berr = run_counter(BASELINE, d, rev, os.path.join(w, "b"))
        mrc, mout, merr = run_counter(mut, d, rev, os.path.join(w, "m"))
        killed = (brc, bout) != (mrc, mout)
        rec = dict(id=fid, mutant=mid, desc=desc, expect=expect, rev=rev,
                   base_rc=brc, base_out=bout.strip(), base_err=berr.strip()[-300:],
                   mut_rc=mrc, mut_out=mout.strip(), mut_err=merr.strip()[-300:],
                   verdict="KILLED" if killed else "NOT-KILLED")
        results.append(rec)
        print("%s %s %-9s base_rc=%s mut_rc=%s" % (fid, mid, rec["verdict"], brc, mrc))
        print("   base: " + (bout.strip() or "(no stdout) " + berr.strip()[-120:]))
        print("   mut : " + (mout.strip() or "(no stdout) " + merr.strip()[-120:]))
        shutil.rmtree(d, ignore_errors=True)
    # M69: CLI check with a tree oid as --rev (no fixture needed; the good tree at 28fc86ac)
    tree = subprocess.run(["git", "-C", "/home/vgpnk/Projects/shokunin/mado-shokunin", "rev-parse",
                           "28fc86ac2359ec27406d8a2c63bef82ea6e947ed^{tree}"],
                          env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    lane = "/home/vgpnk/Projects/shokunin/mado-shokunin"
    brc, bout, berr = run_counter(BASELINE, lane, tree, os.path.join(ROOT, "work", "fx-M69", "b"))
    mrc, mout, merr = run_counter(os.path.join(MUT_DIR, "M69.py"), lane, tree, os.path.join(ROOT, "work", "fx-M69", "m"))
    rec = dict(id="F69", mutant="M69", desc="--rev <tree oid> (not a commit)", expect="setup error rc 2",
               rev=tree, base_rc=brc, base_out=bout.strip(), base_err=berr.strip()[-300:],
               mut_rc=mrc, mut_out=mout.strip(), mut_err=merr.strip()[-300:],
               verdict="KILLED" if (brc, bout) != (mrc, mout) else "NOT-KILLED")
    results.append(rec)
    print("F69 M69 %s base_rc=%s mut_rc=%s" % (rec["verdict"], brc, mrc))
    print("   base: " + (bout.strip() or "(no stdout) " + berr.strip()[-160:]))
    print("   mut : " + (mout.strip() or "(no stdout) " + merr.strip()[-160:]))
    with open(os.path.join(ROOT, "fixtures.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    n_k = sum(1 for r in results if r["verdict"] == "KILLED")
    print("FIXTURES KILLED %d / %d" % (n_k, len(results)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

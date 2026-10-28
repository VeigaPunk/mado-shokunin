#!/usr/bin/env python3
"""c1-r55-kbd-entry.py -- PRED-C1-r55 counter (mado round 55, claim C1, strict reading).

Draft for `quality/counters/c1-r55-kbd-entry.py`.  Contract: `.ufo/waves/round-55/registration.md` section C1 and
`.ufo/waves/round-55/claims-frozen.md` (frozen predicate sentence), read as written and never relaxed.

    python3 -I c1-r55-kbd-entry.py --repo <lane> --rev <rev> --work <scratch>
    python3 -I c1-r55-kbd-entry.py --selftest --repo <lane> --rev <rev> --work <scratch>

Prints exactly one line (stdout):

    MADO_KBD_ENTRY: rev=<rev> rows=<a>/18 hosts=<b>/6 sources=<c>/<d> new_rows=<m>/3 verdict=<V> missed=<legs,comma>|none

Exit 0 only on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on stderr, nothing on stdout).
The counter prints no control verdict; it knows nothing about the controls.

Every input byte comes from git objects at --rev of --repo (`git rev-parse`, `git ls-tree`, `git cat-file blob`);
the working tree is never opened.  Only regular blobs (mode 100644/100755) are accepted: a symlink blob (mode 120000)
or a path that crosses a symlinked directory is "absent", never followed.  --work is a directory that must exist (it is
created when missing) and is the HOME/TMPDIR of every git child; the counter itself writes nothing (selftest writes
only under <work>/selftest-*, removed on exit).

Legs, in output order (names exactly as in the registration):
  entry_absent  provenance  index  row:<id>  anchor:<id>  quote:<id>  pin_hash  source_cell:<id>  new_rows
  host:<id>  tables_sha
Strict reading decisions (each reported in the seat report):
  * a table row is a line outside fenced code blocks and HTML comments whose first cell is the id.  The row must be
    exactly  `| <id> | <prop> | <src> | <pin>:<line> | `<quote>` |`  -- single spaces around every pipe, no trailing
    byte (a trailing space or a CR after the last pipe is a deviation), exactly 5 cells, no `|` inside cells 1-4 (the quote cell alone may hold `|`: the frozen K16 quote contains `||`;
    the cell split is on the 3-byte separator ` | `, which no frozen quote contains),
    proposition cell without leading/trailing whitespace and >=40 chars (K) / >=20 chars (H), src cell `S###` (K) or
    `host` (H).  Any deviation of that grammar, a missing row or a duplicated row is `row:<id>`.
  * anchor cell must equal `<pin>:<line>` byte for byte; the quote cell must equal a SINGLE backtick, the frozen
    quote, a single backtick (`` and ~ styles are `quote:<id>`).  `quote:<id>` also fires when the frozen quote is not
    a substring of that line of the pin blob at --rev.
  * H rows: `host:<id>` fires when the quote that the ROW carries is not a substring of that pin line (a forged cell
    fires both quote:<id> and host:<id>).
  * entry absent (no regular blob at the entry path) reports `entry_absent` and does not evaluate the legs that need the
    entry (provenance, row, anchor, quote, source_cell, host); rows/hosts/sources print 0.
  * if frozen-tables.json is absent or unusable the legs that need its content are not evaluated and only
    `tables_sha` (plus the table-independent entry_absent/provenance/index) is reported.  If its sha256 equals the
    embedded constant but its shape is invalid, that is a setup error (rc 2).
  * `source_cell:<id>`: the row's S-id is exactly one registry row of corpus/SOURCES.md (11 pipe cells), status
    `mined`, whose URL (last http(s) token of the source cell) ends with `/` + the pin's source_suffix and, for the
    `Hyprland-*` pins, contains the frozen commit (the wayland pin cannot contain a Hyprland commit; its suffix already
    carries the tag 1.26.0).
  * `new_rows`: the number of new_row_pins pins covered by at least one registry row (opened == c1.opened, tier A,
    status mined, URL ends with `/` + that pin's suffix and contains the frozen commit, used-by names the entry path)
    must reach c1.new_rows_min.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

TOOL = "c1-r55-kbd-entry.py"
TABLES_SHA256 = "13d6e2f9c0dfe1287e2cd9a7d814d95a4fb0ff0ad7ce644aad7ead18af69a7b9"
TABLES_PATH = ".ufo/waves/round-55/frozen-tables-v2.json"
ENTRY_PATH = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
README_PATH = "corpus/README.md"
SOURCES_PATH = "corpus/SOURCES.md"
OPENED = "2026-10-28"
N_K, N_H = 18, 6
REGULAR_MODES = ("100644", "100755")
PROV_WINDOW = 30

FENCE = re.compile(r"^ {0,3}(```|~~~)")
ROW_ID = re.compile(r"^\|\s*([KH][0-9]{2})\s*\|")
SID = re.compile(r"^S[0-9]{3}$")
URL = re.compile(r"https?://[^\s`|]+")
SRC_ID = re.compile(r"^\| (S[0-9]{3}) \|")
S_IN_LINE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")


class SetupError(Exception):
    pass


# --------------------------------------------------------------------------------------------- git access
def git_env(work):
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": work,
        "TMPDIR": work,
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_LITERAL_PATHSPECS": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_TERMINAL_PROMPT": "0",
    }
    return env


class Repo:
    def __init__(self, repo, rev, work):
        self.repo = repo
        self.work = work
        self.env = git_env(work)
        self._blobs = {}
        if not os.path.isdir(repo):
            raise SetupError("repo is not a directory")
        if rev.startswith("-") or not rev:
            raise SetupError("bad rev")
        r = self.git(["rev-parse", "--verify", "--quiet", "--end-of-options", rev + "^{commit}"])
        if r.returncode != 0:
            raise SetupError("rev does not resolve to a commit at repo")
        self.sha = r.stdout.decode("ascii", "replace").strip()
        if not re.fullmatch(r"[0-9a-f]{40,64}", self.sha):
            raise SetupError("rev resolved to an unexpected object name")

    def git(self, args, inp=None):
        try:
            return subprocess.run(["git", "-C", self.repo] + args, input=inp, capture_output=True,
                                  env=self.env, timeout=300)
        except (OSError, subprocess.SubprocessError) as exc:
            raise SetupError("git failed to run: %s" % type(exc).__name__)

    def ls(self, paths):
        """exact paths -> {path: (mode, type, oid)}; a path under a symlinked directory is simply not listed."""
        paths = sorted(set(paths))
        if not paths:
            return {}
        r = self.git(["ls-tree", "-z", self.sha, "--"] + paths)
        if r.returncode != 0:
            raise SetupError("git ls-tree failed")
        out = {}
        for rec in r.stdout.split(b"\0"):
            if not rec:
                continue
            meta, _, path = rec.partition(b"\t")
            parts = meta.split(b" ")
            if len(parts) != 3:
                raise SetupError("unparsable ls-tree record")
            out[path.decode("utf-8", "surrogateescape")] = tuple(p.decode("ascii") for p in parts)
        return out

    def blob(self, listing, path):
        """regular-file bytes of `path` from a listing, else None (absent, symlink, dir, submodule)."""
        ent = listing.get(path)
        if ent is None or ent[0] not in REGULAR_MODES or ent[1] != "blob":
            return None
        oid = ent[2]
        if oid not in self._blobs:
            r = self.git(["cat-file", "blob", oid])
            if r.returncode != 0:
                raise SetupError("git cat-file failed")
            self._blobs[oid] = r.stdout
        return self._blobs[oid]


# --------------------------------------------------------------------------------------------- text helpers
def text_of(b):
    return b.decode("utf-8", "surrogateescape")


def visible_lines(text):
    """(lineno, line) outside fenced code blocks and HTML comments; split on LF only (CR stays on the line)."""
    out = []
    fence = None
    in_comment = False
    for n, line in enumerate(text.split("\n"), 1):
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        m = FENCE.match(line)
        if fence is not None:
            if m and m.group(1) == fence:
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
            in_comment = True
            continue
        out.append((n, line))
    return out


def pin_line(pin_bytes, n):
    if pin_bytes is None or n < 1:
        return None
    lines = text_of(pin_bytes).split("\n")
    return lines[n - 1] if n <= len(lines) else None


# --------------------------------------------------------------------------------------------- tables
def valid_shape(d):
    """strict structural validation of frozen-tables.json's c1 block; returns the c1 dict or None."""
    try:
        c = d["c1"]
        if not isinstance(c, dict) or c.get("entry") != ENTRY_PATH:
            return None
        for key in ("commit", "entry", "opened", "pin_dir"):
            if not isinstance(c[key], str) or not c[key]:
                return None
        if not re.fullmatch(r"[0-9a-f]{40}", c["commit"]):
            return None
        pd = c["pin_dir"]
        if pd.startswith("/") or "\0" in pd or any(p in ("", ".", "..") for p in pd.split("/")):
            return None
        if not isinstance(c["new_rows_min"], int) or isinstance(c["new_rows_min"], bool) or c["new_rows_min"] < 1:
            return None
        pins, suf = c["pin_sha256"], c["source_suffix"]
        if not isinstance(pins, dict) or not isinstance(suf, dict) or not pins:
            return None
        for name, h in pins.items():
            if not isinstance(name, str) or not name or "/" in name or name in (".", ".."):
                return None
            if not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h):
                return None
        for name, s in suf.items():
            if name not in pins or not isinstance(s, str) or not s or s.startswith("/"):
                return None
        for kind, ids, n in (("k", "K", N_K), ("h", "H", N_H)):
            rows = c[kind]
            if not isinstance(rows, list) or len(rows) != n:
                return None
            for i, r in enumerate(rows, 1):
                if not isinstance(r, dict) or r.get("id") != "%s%02d" % (ids, i):
                    return None
                if not isinstance(r.get("pin"), str) or r["pin"] not in pins:
                    return None
                if not isinstance(r.get("line"), int) or isinstance(r["line"], bool) or r["line"] < 1:
                    return None
                q = r.get("quote")
                if not isinstance(q, str) or not q or "`" in q or "\n" in q or " | " in q:
                    return None
                if kind == "k" and r["pin"] not in suf:
                    return None
        nrp = c["new_row_pins"]
        if not isinstance(nrp, dict) or not nrp or any(p not in suf for p in nrp):
            return None
        return c
    except (KeyError, TypeError, AttributeError):
        return None


# --------------------------------------------------------------------------------------------- registry
def parse_registry(text):
    """id -> list of cell lists (cells None when the row does not have exactly 11 pipe cells)."""
    reg = {}
    for _n, line in visible_lines(text):
        m = SRC_ID.match(line)
        if not m:
            continue
        s = line.strip()
        cells = [c.strip() for c in s[1:-1].split("|")] if s.endswith("|") else None
        if cells is not None and len(cells) != 11:
            cells = None
        reg.setdefault(m.group(1), []).append(cells)
    return reg


def last_url(cell):
    found = URL.findall(cell)
    return found[-1] if found else ""


def source_ok(reg, sid, pin, c):
    rows = reg.get(sid or "", [])
    if len(rows) != 1 or rows[0] is None:
        return False
    cells = rows[0]
    url = last_url(cells[1])
    if cells[7] != "mined" or not url.endswith("/" + c["source_suffix"][pin]):
        return False
    if pin.startswith("Hyprland-") and c["commit"] not in url:
        return False
    return True


def count_new_rows(reg, c):
    covered = set()
    for rows in reg.values():
        for cells in rows:
            if cells is None:
                continue
            url = last_url(cells[1])
            if cells[8] != c["opened"] or cells[3] != "A" or cells[7] != "mined" or c["commit"] not in url:
                continue
            if c["entry"] not in cells[10]:
                continue
            for pin in c["new_row_pins"]:
                if url.endswith("/" + c["source_suffix"][pin]):
                    covered.add(pin)
    return len(covered)


# --------------------------------------------------------------------------------------------- the check
def split_row(line):
    if not (line.startswith("| ") and line.endswith(" |")):
        return None
    if "\\|" in line:
        return None  # registration v2 E5: a backslash-escaped pipe makes the row malformed
    cells = line[2:-2].split(" | ")
    if len(cells) != 5 or any("|" in x for x in cells[:4]):
        return None  # the quote cell alone may carry `|` (no v2 quote does; ` | ` never occurs in a quote)
    return cells


def check(repo_path, rev, work):
    R = Repo(repo_path, rev, work)
    lst = R.ls([ENTRY_PATH, README_PATH, SOURCES_PATH, TABLES_PATH])
    tb = R.blob(lst, TABLES_PATH)
    sha_ok = tb is not None and hashlib.sha256(tb).hexdigest() == TABLES_SHA256
    c = None
    if tb is not None:
        try:
            c = valid_shape(json.loads(text_of(tb)))
        except ValueError:
            c = None
    if sha_ok and c is None:
        raise SetupError("frozen-tables.json matches the embedded sha256 but its c1 shape is invalid")

    missed = {k: [] for k in ("entry_absent", "provenance", "index", "row", "anchor", "quote", "pin_hash",
                              "source_cell", "new_rows", "host", "tables_sha")}
    rows_ok = hosts_ok = sources_ok = 0
    new_rows = 0
    new_min = c["new_rows_min"] if c else 3

    entry_b = R.blob(lst, ENTRY_PATH)
    entry_lines = None
    if entry_b is None:
        pass
    else:
        entry_lines = visible_lines(text_of(entry_b))
        # provenance trio, inside the opening window of the file
        head = [ln for n, ln in entry_lines if n <= PROV_WINDOW]
        src = any(ln.startswith("source:") and S_IN_LINE.search(ln) for ln in head)
        ver = any(ln == "verified-at: 2026-10-28" for ln in head)
        rec = any(ln.startswith("recheck:") and ln[len("recheck:"):].strip() for ln in head)
        if not (src and ver and rec):
            missed["provenance"].append("provenance")

    # README index row: exactly one
    readme_b = R.blob(lst, README_PATH)
    prefix = "| `" + ENTRY_PATH[len("corpus/"):] + "`"
    n_idx = 0 if readme_b is None else sum(1 for _n, ln in visible_lines(text_of(readme_b)) if ln.startswith(prefix))
    if n_idx != 1:
        missed["index"].append("index")

    if c is not None:
        pin_dir = c["pin_dir"]
        names = sorted(c["pin_sha256"])
        plst = R.ls([pin_dir + "/" + n for n in names])
        pins = {n: R.blob(plst, pin_dir + "/" + n) for n in names}
        for n in names:
            b = pins[n]
            if b is None or hashlib.sha256(b).hexdigest() != c["pin_sha256"][n]:
                if "pin_hash" not in missed["pin_hash"]:
                    missed["pin_hash"].append("pin_hash")

        sources_b = R.blob(lst, SOURCES_PATH)
        reg = parse_registry(text_of(sources_b)) if sources_b is not None else {}
        new_rows = count_new_rows(reg, c)
        if new_rows < new_min:
            missed["new_rows"].append("new_rows")

        if entry_lines is not None:
            cand = {}
            for _n, ln in entry_lines:
                m = ROW_ID.match(ln)
                if m:
                    cand.setdefault(m.group(1), []).append(ln)
            for kind, frozen in (("k", c["k"]), ("h", c["h"])):
                for fr in frozen:
                    rid = fr["id"]
                    lines = cand.get(rid, [])
                    cells = split_row(lines[0]) if len(lines) == 1 else None
                    prop_min = 40 if kind == "k" else 20
                    if cells is not None:
                        prop = cells[1]
                        if (cells[0] != rid or not prop or prop != prop.strip() or len(prop) < prop_min
                                or (kind == "h" and cells[2] != "host")):
                            cells = None
                    if cells is None:
                        missed["row"].append("row:" + rid)
                        continue
                    ok = True
                    if cells[3] != "%s:%d" % (fr["pin"], fr["line"]):
                        missed["anchor"].append("anchor:" + rid)
                        ok = False
                    pl = pin_line(pins.get(fr["pin"]), fr["line"])
                    if cells[4] != "`" + fr["quote"] + "`" or pl is None or fr["quote"] not in pl:
                        missed["quote"].append("quote:" + rid)
                        ok = False
                    if kind == "k":
                        if source_ok(reg, cells[2] if SID.match(cells[2]) else None, fr["pin"], c):
                            sources_ok += 1
                        else:
                            missed["source_cell"].append("source_cell:" + rid)
                        rows_ok += ok
                    else:
                        cell_q = cells[4][1:-1] if len(cells[4]) >= 2 and cells[4][0] == cells[4][-1] == "`" else cells[4]
                        if pl is None or cell_q not in pl:
                            missed["host"].append("host:" + rid)
                            ok = False
                        hosts_ok += ok
    if not sha_ok:
        missed["tables_sha"].append("tables_sha")

    order = ("entry_absent", "provenance", "index", "row", "anchor", "quote", "pin_hash", "source_cell",
             "new_rows", "host", "tables_sha")
    # row/anchor/quote keep K-before-H frozen order because rows are visited in that order
    legs = [x for k in order for x in missed[k]]
    verdict = "TARGET_MET" if not legs else "TARGET_MISSED"
    line = ("MADO_KBD_ENTRY: rev=%s rows=%d/%d hosts=%d/%d sources=%d/%d new_rows=%d/%d verdict=%s missed=%s"
            % (rev, rows_ok, N_K, hosts_ok, N_H, sources_ok, N_K, new_rows, new_min, verdict,
               ",".join(legs) if legs else "none"))
    return line, (0 if verdict == "TARGET_MET" else 1)


# --------------------------------------------------------------------------------------------- selftest
SYN_SID = {
    "Hyprland-InputManager.cpp": "S316", "Hyprland-IKeyboard.cpp": "S319", "Hyprland-SeatManager.cpp": "S378",
    "Hyprland-protocols-core-Seat.cpp": "S379", "Hyprland-ConfigValues.cpp": "S318",
    "Hyprland-legacy-ConfigManager.cpp": "S317", "wayland-1.26.0-wayland.xml": "S052",
    "Hyprland-IKeyboard.hpp": "S380",
}
SYN_URL = {
    "S316": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/managers/input/InputManager.cpp",
    "S317": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/config/legacy/ConfigManager.cpp",
    "S318": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/config/values/ConfigValues.cpp",
    "S215": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/config/values/ConfigValues.cpp",
    "S319": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/devices/IKeyboard.cpp",
    "S052": "https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml",
    "S378": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/managers/SeatManager.cpp",
    "S379": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/protocols/core/Seat.cpp",
    "S380": "https://raw.githubusercontent.com/hyprwm/Hyprland/{c}/src/devices/IKeyboard.hpp",
}
NEW_SIDS = ("S378", "S379", "S380")


def syn_registry(c, usedby_override=None, status_override=None):
    rows = ["| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid in sorted(SYN_URL):
        new = sid in NEW_SIDS
        status = (status_override or {}).get(sid, "mined")
        used = (usedby_override or {}).get(sid, c["entry"] if new else "corpus/knowledge/other.md")
        rows.append("| %s | synthetic row title - %s | code | A | scope | anchor | teaches | %s | %s | on-release | %s |"
                    % (sid, SYN_URL[sid].format(c=c["commit"]), status, c["opened"] if new else "2026-10-26", used))
    return "\n".join(rows) + "\n"


def syn_entry(c):
    out = ["# Synthetic keyboard entry (selftest only)", "",
           "source: S316, S317, S318, S319, S052, S378, S379, S380",
           "verified-at: 2026-10-28", "recheck: on-release", "",
           "| id | proposition | source | pin:line | quote |", "|---|---|---|---|---|"]
    for fr in c["k"]:
        out.append("| %s | Synthetic proposition for %s long enough for the forty character floor | %s | %s:%d | `%s` |"
                   % (fr["id"], fr["id"], SYN_SID[fr["pin"]], fr["pin"], fr["line"], fr["quote"]))
    out.append("")
    out.append("| id | proposition | source | pin:line | quote |")
    out.append("|---|---|---|---|---|")
    for fr in c["h"]:
        out.append("| %s | Synthetic host proposition %s ok | host | %s:%d | `%s` |"
                   % (fr["id"], fr["id"], fr["pin"], fr["line"], fr["quote"]))
    return "\n".join(out) + "\n"


def syn_readme(c):
    return ("# README (synthetic)\n\n| path | what |\n|---|---|\n| `knowledge/other.md` (x) | y |\n"
            "| `%s` (MADO-R55-1) | synthetic index row |\n" % c["entry"][len("corpus/"):])


def row_of(files, rid):
    t = text_of(files[ENTRY_PATH])
    for ln in t.split("\n"):
        if ln.startswith("| %s |" % rid):
            return ln
    raise KeyError(rid)


def edit(files, path, old, new, count=1):
    t = text_of(files[path])
    assert old in t, (path, old)
    files[path] = t.replace(old, new, count).encode("utf-8", "surrogateescape")


def edit_row(files, rid, old, new):
    r = row_of(files, rid)
    assert old in r, (rid, old)
    edit(files, ENTRY_PATH, r, r.replace(old, new, 1))


def good_files(tables_bytes, pin_bytes, c):
    pd = c["pin_dir"]
    f = {TABLES_PATH: tables_bytes, ENTRY_PATH: syn_entry(c).encode(), README_PATH: syn_readme(c).encode(),
         SOURCES_PATH: syn_registry(c).encode()}
    for n, b in pin_bytes.items():
        f[pd + "/" + n] = b
    return f


def build_repo(base, name, files):
    """scratch repo under `base`: fresh mktemp dir, git -C everywhere, toplevel asserted before the first commit."""
    import tempfile
    D = tempfile.mkdtemp(prefix=name + "-", dir=base)
    env = git_env(base)
    def g(*a):
        r = subprocess.run(["git", "-C", D] + list(a), capture_output=True, env=env)
        if r.returncode != 0:
            raise RuntimeError("git %s failed: %s" % (a, r.stderr.decode()))
        return r.stdout.decode().strip()
    g("init", "-q")
    top = g("rev-parse", "--show-toplevel")
    if os.path.realpath(top) != os.path.realpath(D):
        raise RuntimeError("toplevel %s != %s" % (top, D))
    for path, val in files.items():
        full = os.path.join(D, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if isinstance(val, tuple):
            os.symlink(val[1], full)
        else:
            with open(full, "wb") as fh:
                fh.write(val)
    g("add", "-A")
    g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "synthetic")
    return D


def run_counter(script, repo, rev, work, extra=()):
    os.makedirs(work, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", script, "--repo", repo, "--rev", rev, "--work", work] + list(extra),
                       capture_output=True, env={"PATH": os.environ.get("PATH", "/usr/bin:/bin")}, timeout=600)
    return r.returncode, r.stdout.decode(), r.stderr.decode()


def selftest(repo, rev, work):
    R = Repo(repo, rev, work)
    lst = R.ls([TABLES_PATH])
    tb = R.blob(lst, TABLES_PATH)
    if tb is None or hashlib.sha256(tb).hexdigest() != TABLES_SHA256:
        raise SetupError("selftest needs frozen-tables.json at --rev matching the embedded sha256")
    c = valid_shape(json.loads(text_of(tb)))
    if c is None:
        raise SetupError("selftest: frozen-tables.json shape invalid")
    names = sorted(c["pin_sha256"])
    plst = R.ls([c["pin_dir"] + "/" + n for n in names])
    pin_bytes = {}
    for n in names:
        b = R.blob(plst, c["pin_dir"] + "/" + n)
        if b is None or hashlib.sha256(b).hexdigest() != c["pin_sha256"][n]:
            raise SetupError("selftest: pin %s missing or wrong hash at --rev" % n)
        pin_bytes[n] = b

    base = os.path.join(work, "selftest-%d" % os.getpid())
    os.makedirs(base, exist_ok=True)
    script = os.path.abspath(__file__)
    kids = ["K%02d" % i for i in range(1, N_K + 1)]
    hids = ["H%02d" % i for i in range(1, N_H + 1)]
    allrows = ["row:" + x for x in kids + hids]
    GOOD = ("MADO_KBD_ENTRY: rev=HEAD rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET "
            "missed=none")
    pd = c["pin_dir"]
    results = []

    def case(name, mutate, expected, rc_expected=None, rev_arg="HEAD", line_check=None):
        files = good_files(tb, pin_bytes, c)
        mutate(files)
        D = build_repo(base, "c", files)
        rc, out, err = run_counter(script, D, rev_arg, os.path.join(base, "w"))
        m = re.fullmatch(r"MADO_KBD_ENTRY: rev=(\S+) rows=(\d+)/18 hosts=(\d+)/6 sources=(\d+)/18 new_rows=(\d+)/3 "
                         r"verdict=(TARGET_MET|TARGET_MISSED) missed=(\S+)\n", out)
        got = m.group(7) if m else None
        want = ",".join(expected) if expected else "none"
        want_rc = rc_expected if rc_expected is not None else (0 if not expected else 1)
        ok = bool(m) and got == want and rc == want_rc and (line_check is None or line_check(out))
        results.append((name, ok, want, got if m else "UNPARSABLE rc=%s out=%r err=%r" % (rc, out[:120], err[:120])))
        shutil.rmtree(D, ignore_errors=True)
        return out

    def counts(**kw):
        return lambda out: all(("%s=%s" % (k, v)) in out for k, v in kw.items())

    # ---- positive
    case("good-tree", lambda f: None, [], line_check=lambda o: o.strip() == GOOD)
    case("good-alt-source-S215-for-K15",
         lambda f: (edit_row(f, "K15", "| S318 |", "| S215 |")), [])
    # ---- the seven frozen controls
    case("CTL1-absent", lambda f: f.pop(ENTRY_PATH), ["entry_absent"],
         line_check=counts(rows="0/18", hosts="0/6", sources="0/18"))
    case("CTL2-spliced-quote-K04",
         lambda f: edit_row(f, "K04", "std::max(0, REPEATRATE);", "std::max(0, REPEATRATE) ;"), ["quote:K04"],
         line_check=counts(rows="17/18"))
    case("CTL3-shifted-anchor-K01", lambda f: edit_row(f, "K01", ":1220", ":1219"), ["anchor:K01"],
         line_check=counts(rows="17/18"))
    case("CTL4-wrong-source-K10", lambda f: edit_row(f, "K10", "| S378 |", "| S316 |"), ["source_cell:K10"],
         line_check=counts(sources="17/18", rows="18/18"))

    def drop_k17(f):
        edit(f, ENTRY_PATH, row_of(f, "K17") + "\n", "")
    case("CTL5-dropped-row-K17", drop_k17, ["row:K17"], line_check=counts(rows="17/18", sources="17/18"))
    case("CTL6-host-forged-H02",
         lambda f: edit_row(f, "H02", "repeat_delay = 250", "repeat_delay = 300"), ["quote:H02", "host:H02"],
         line_check=counts(hosts="5/6"))

    def pin_tamper(f):
        name = "Hyprland-IKeyboard.cpp"
        old = c["pin_sha256"][name]
        new = old[:-1] + ("0" if old[-1] != "0" else "1")
        edit(f, TABLES_PATH, old, new)
        f[pd + "/" + name] = f[pd + "/" + name] + b" "
    case("CTL7-pin-tamper-tables-and-pin", pin_tamper, ["pin_hash", "tables_sha"])
    # ---- further mutations (each with its exact leg)
    case("pin-bytes-only-appended-space",
         lambda f: f.__setitem__(pd + "/Hyprland-ConfigValues.cpp", f[pd + "/Hyprland-ConfigValues.cpp"] + b" "),
         ["pin_hash"])
    case("tables-trailing-newline", lambda f: f.__setitem__(TABLES_PATH, f[TABLES_PATH] + b"\n"), ["tables_sha"])
    case("tables-absent", lambda f: f.pop(TABLES_PATH), ["tables_sha"],
         line_check=counts(rows="0/18", new_rows="0/3"))
    case("provenance-no-recheck", lambda f: edit(f, ENTRY_PATH, "recheck: on-release\n", ""), ["provenance"])
    case("provenance-no-S-id-in-source",
         lambda f: edit(f, ENTRY_PATH, "source: S316, S317, S318, S319, S052, S378, S379, S380",
                        "source: no registry ids here"), ["provenance"])
    case("provenance-wrong-date", lambda f: edit(f, ENTRY_PATH, "verified-at: 2026-10-28", "verified-at: 2026-10-27"),
         ["provenance"])
    case("index-row-missing", lambda f: edit(f, README_PATH, "| `knowledge/hyprland-keyboard-repeat-numlock-r55.md`",
                                             "| `knowledge/zz.md`"), ["index"])
    case("index-row-duplicated",
         lambda f: edit(f, README_PATH, "\n", "\n| `knowledge/hyprland-keyboard-repeat-numlock-r55.md` dup | z |\n", 1),
         ["index"])
    case("new-rows-usedby-missing-entry-S379",
         lambda f: f.__setitem__(SOURCES_PATH, syn_registry(c, usedby_override={"S379": "corpus/knowledge/x.md"}).encode()),
         ["new_rows"], line_check=counts(new_rows="2/3"))
    case("source-candidate-status-S380",
         lambda f: f.__setitem__(SOURCES_PATH, syn_registry(c, status_override={"S380": "candidate"}).encode()),
         ["source_cell:K18", "new_rows"], line_check=counts(sources="17/18", new_rows="2/3"))
    case("source-cell-not-an-S-id-K02", lambda f: edit_row(f, "K02", "| S316 |", "| none |"), ["source_cell:K02"])
    case("host-row-src-cell-not-host-H03", lambda f: edit_row(f, "H03", "| host |", "| S316 |"), ["row:H03"])
    case("short-proposition-K02",
         lambda f: edit_row(f, "K02", "Synthetic proposition for K02 long enough for the forty character floor",
                            "too short"), ["row:K02"])
    case("short-host-proposition-H04",
         lambda f: edit_row(f, "H04", "Synthetic host proposition H04 ok", "short"), ["row:H04"])
    case("extra-cell-pipe-in-proposition-K06",
         lambda f: edit_row(f, "K06", "Synthetic proposition for K06", "Synthetic | proposition for K06"),
         ["row:K06"])
    # ---- grammar-strictness cases the seat was asked to cover
    def crlf_all(f):
        f[ENTRY_PATH] = text_of(f[ENTRY_PATH]).replace("\n", "\r\n").encode()
    case("CRLF-whole-entry", crlf_all, ["provenance"] + allrows,
         line_check=counts(rows="0/18", hosts="0/6", sources="0/18"))

    def crlf_one(f):
        r = row_of(f, "K05")
        edit(f, ENTRY_PATH, r + "\n", r + "\r\n")
    case("CRLF-single-row-K05", crlf_one, ["row:K05"])

    def trail(f):
        r = row_of(f, "K09")
        edit(f, ENTRY_PATH, r + "\n", r + "   \n")
    case("trailing-spaces-after-row-K09", trail, ["row:K09"])

    def tab_trail(f):
        r = row_of(f, "H01")
        edit(f, ENTRY_PATH, r + "\n", r + "\t\n")
    case("trailing-tab-after-row-H01", tab_trail, ["row:H01"])

    def dup_same(f):
        r = row_of(f, "K03")
        edit(f, ENTRY_PATH, r + "\n", r + "\n" + r + "\n")
    case("duplicated-row-id-K03-identical", dup_same, ["row:K03"], line_check=counts(rows="17/18"))

    def dup_differs(f):
        r = row_of(f, "H05")
        edit(f, ENTRY_PATH, r + "\n", r + "\n" + r.replace("Synthetic host", "Other host") + "\n")
    case("duplicated-row-id-H05-different-text", dup_differs, ["row:H05"])

    case("backtick-style-double-K05",
         lambda f: edit_row(f, "K05", "`std::max(0, REPEATDELAY);`", "``std::max(0, REPEATDELAY);``"),
         ["quote:K05"])
    case("backtick-style-none-H06",
         lambda f: edit_row(f, "H06", '`"option": "input:numlock_by_default", "int": 1`',
                            '"option": "input:numlock_by_default", "int": 1'), ["quote:H06"])

    def fenced(f):
        r = row_of(f, "K12")
        edit(f, ENTRY_PATH, r + "\n", "```\n" + r + "\n```\n")
    case("row-only-inside-code-fence-K12", fenced, ["row:K12"])

    def commented(f):
        r = row_of(f, "K13")
        edit(f, ENTRY_PATH, r + "\n", "<!--\n" + r + "\n-->\n")
    case("row-only-inside-html-comment-K13", commented, ["row:K13"])
    case("row-leading-id-spacing-K07", lambda f: edit_row(f, "K07", "| K07 |", "|K07 |"), ["row:K07"])
    case("anchor-wrong-pin-file-K08", lambda f: edit_row(f, "K08", "Hyprland-IKeyboard.cpp:120",
                                                         "Hyprland-IKeyboard.hpp:120"), ["anchor:K08"])
    case("quote-extra-space-K18", lambda f: edit_row(f, "K18", "m_repeatRate        = 0;", "m_repeatRate = 0;"),
         ["quote:K18"])
    # ---- symlink cases
    case("symlink-pin-file-SeatManager",
         lambda f: f.__setitem__(pd + "/Hyprland-SeatManager.cpp", ("link", "Hyprland-InputManager.cpp")),
         ["quote:K10", "pin_hash"])

    def symlink_pin_dir(f):
        for n in list(pin_bytes):
            f["fetch-real/" + n] = f.pop(pd + "/" + n)
        f[pd] = ("link", "../../../fetch-real")
    case("symlink-pin-directory", symlink_pin_dir,
         ["quote:" + x for x in kids + hids] + ["pin_hash"] + ["host:" + x for x in hids])
    case("symlink-entry-file", lambda f: f.__setitem__(ENTRY_PATH, ("link", "../README.md")), ["entry_absent"])
    case("symlink-sources-file",
         lambda f: f.__setitem__(SOURCES_PATH, ("link", "README.md")),
         ["source_cell:" + x for x in kids] + ["new_rows"], line_check=counts(sources="0/18", new_rows="0/3"))
    # ---- environment cases: repo path through a symlink, working tree ignored, setup errors, empty commit
    files = good_files(tb, pin_bytes, c)
    D = build_repo(base, "env", files)
    link = os.path.join(base, "repo-link")
    os.symlink(D, link)
    rc, out, err = run_counter(script, link, "HEAD", os.path.join(base, "w"))
    results.append(("repo-path-is-a-symlink", rc == 0 and out.strip() == GOOD, "TARGET_MET rc=0", "rc=%s %s" % (rc, out.strip()[-60:])))
    # uncommitted working-tree vandalism must not change the verdict
    os.remove(os.path.join(D, ENTRY_PATH))
    with open(os.path.join(D, README_PATH), "w") as fh:
        fh.write("garbage\n")
    with open(os.path.join(D, TABLES_PATH), "w") as fh:
        fh.write("{}\n")
    rc, out, err = run_counter(script, D, "HEAD", os.path.join(base, "w"))
    results.append(("dirty-working-tree-ignored", rc == 0 and out.strip() == GOOD, "TARGET_MET rc=0", "rc=%s %s" % (rc, out.strip()[-60:])))
    sha = subprocess.run(["git", "-C", D, "rev-parse", "HEAD"], capture_output=True, env=git_env(base)).stdout.decode().strip()
    rc, out, err = run_counter(script, D, sha, os.path.join(base, "w"))
    results.append(("rev-as-full-sha", rc == 0 and out.strip() == GOOD.replace("rev=HEAD", "rev=" + sha), "rev echoed as given", out.strip()[:60]))
    out1 = run_counter(script, D, "HEAD", os.path.join(base, "w"))[1]
    out2 = run_counter(script, D, "HEAD", os.path.join(base, "w"))[1]
    results.append(("deterministic-two-runs", out1 == out2 and out1 != "", "identical output", "equal" if out1 == out2 else "differs"))
    rc, out, err = run_counter(script, D, "no-such-rev", os.path.join(base, "w"))
    results.append(("setup-bad-rev-rc2-empty-stdout", rc == 2 and out == "", "rc=2 stdout empty", "rc=%s out=%r" % (rc, out)))
    rc, out, err = run_counter(script, os.path.join(base, "nonexistent"), "HEAD", os.path.join(base, "w"))
    results.append(("setup-bad-repo-rc2", rc == 2 and out == "", "rc=2 stdout empty", "rc=%s out=%r" % (rc, out)))
    r = subprocess.run([sys.executable, "-I", script, "--repo", D, "--rev", "HEAD"], capture_output=True, env={"PATH": os.environ.get("PATH", "")})
    results.append(("setup-missing-work-rc2", r.returncode == 2 and r.stdout == b"", "rc=2 stdout empty", "rc=%s out=%r" % (r.returncode, r.stdout)))
    # a commit with an empty tree: nothing is present
    empty = build_repo(base, "empty", {"README.txt": b"x\n"})
    rc, out, err = run_counter(script, empty, "HEAD", os.path.join(base, "w"))
    ok = rc == 1 and "missed=entry_absent,index,tables_sha" in out and "rows=0/18" in out
    results.append(("tree-without-any-r55-file", ok, "entry_absent,index,tables_sha rc=1", "rc=%s %s" % (rc, out.strip()[-60:])))
    # embedded sha matches but shape invalid cannot be built (sha is fixed); a sha-mismatched bad-shape table:
    case("tables-bad-shape-sha-mismatch", lambda f: f.__setitem__(TABLES_PATH, b'{"c1": {"k": []}}'),
         ["tables_sha"], line_check=counts(rows="0/18"))

    shutil.rmtree(base, ignore_errors=True)
    n_ok = 0
    print("selftest: %s rev=%s" % (TOOL, rev))
    for name, ok, want, got in results:
        n_ok += bool(ok)
        print("%s %-46s expected=%s%s" % ("PASS" if ok else "FAIL", name, want, "" if ok else "  got=" + str(got)))
    print("MADO_KBD_ENTRY_SELFTEST: %d/%d passed" % (n_ok, len(results)))
    return 0 if n_ok == len(results) else 1


# --------------------------------------------------------------------------------------------- cli
def main(argv):
    ap = argparse.ArgumentParser(prog=TOOL, add_help=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)  # argparse exits 2 on usage errors, stdout stays empty
    try:
        os.makedirs(a.work, exist_ok=True)
        if not os.access(a.work, os.W_OK):
            raise SetupError("work dir not writable")
        work = os.path.abspath(a.work)
        if a.selftest:
            return selftest(a.repo, a.rev, work)
        line, rc = check(a.repo, a.rev, work)
    except SetupError as exc:
        sys.stderr.write("%s: setup error: %s\n" % (TOOL, exc))
        return 2
    except OSError as exc:
        sys.stderr.write("%s: setup error: %s\n" % (TOOL, exc.__class__.__name__))
        return 2
    sys.stdout.write(line + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

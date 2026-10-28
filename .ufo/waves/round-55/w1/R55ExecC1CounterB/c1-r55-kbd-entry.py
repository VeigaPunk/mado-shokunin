#!/usr/bin/env python3
"""PRED-C1-r55 counter - the keyboard repeat/delay/numlock entry (registration section C1).

    python3 -I quality/counters/c1-r55-kbd-entry.py --repo <lane> --rev <rev> [--work <scratch>]

prints exactly one stdout line

    MADO_KBD_ENTRY: rev=<rev> rows=<a>/18 hosts=<b>/6 sources=<c>/<d> new_rows=<m>/3 verdict=<V> missed=<legs,comma>|none

and exits 0 only on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (then the one stdout line is
`MADO_KBD_ENTRY: SETUP <reason>`).  Every input is read from git objects at --rev of --repo through
`git ls-tree` / `git cat-file` - never from the working tree, and a committed symlink is never followed (only
regular blobs, modes 100644/100755, are read).  The tables come from the blob
`.ufo/waves/round-55/frozen-tables.json` at --rev, whose sha256 must equal TABLES_SHA256 below (leg `tables_sha`).

Parsing strategy: no per-line regex.  Every file is cut into lines on `\\n` only; a markdown table row is tokenised
by a small cell scanner (`table_cells`): the line, stripped of trailing space/tab/CR, must start and end with `|`
and is split on `|` into cells.  Fenced code blocks are skipped.  Row ids, S-ids, URLs and dates are recognised by
small hand-written scanners.

Definitions this counter fixes where the registration text leaves room (also listed in the seat report):
  * rows   = frozen K ids whose row exists once, is well formed, and has no `row`, `anchor` or `quote` leg.
  * hosts  = frozen H ids with no `row`, `anchor`, `quote` or `host` leg.
  * sources= <K ids whose `source_cell` check passes>/<number of frozen K ids>.
  * new_rows = qualifying registry rows (distinct ids) / c1.new_rows_min.
  * `contains the frozen commit` (source_cell) is demanded for Hyprland pins (pin file name starts with `Hyprland-`);
    the wayland pin's URL carries the tag (`1.26.0/protocol/wayland.xml`), not a Hyprland commit.
  * a pin that cannot be read as a regular blob at --rev gives `pin_hash`, and every quote/host check that needs
    its line is a miss (unverifiable is not a pass).

Self-test: `--selftest --repo <lane> --rev <rev> --work <scratch>` builds a scratch git repository holding a
synthetic good tree generated from the frozen tables plus the real pin bytes read from <rev>, runs the counter on
the good tree and on named mutants, and prints one line per case and a final MADO_R55_C1_SELFTEST line
(exit 0 only if every case matches its expected line).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

TABLES_SHA256 = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
TABLES_PATH = ".ufo/waves/round-55/frozen-tables.json"
README_PATH = "corpus/README.md"
SOURCES_PATH = "corpus/SOURCES.md"
VERIFIED_PREFIX = "verified-at: 2026-10-28"
REGULAR_MODES = ("100644", "100755")

# leg groups, in the order the registration names them; ids inside a group follow the frozen table order
GROUPS = ("entry_absent", "provenance", "index", "row", "anchor", "quote", "pin_hash",
          "source_cell", "new_rows", "host", "tables_sha")


class SetupError(Exception):
    pass


# --------------------------------------------------------------------------- git object access

class Git:
    def __init__(self, repo, work):
        self.repo = repo
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env["LC_ALL"] = "C"
        env["GIT_OPTIONAL_LOCKS"] = "0"
        env["GIT_CONFIG_NOSYSTEM"] = "1"
        env["GIT_CONFIG_GLOBAL"] = os.devnull
        if work:
            env["TMPDIR"] = work
        self.env = env

    def run(self, *args):
        try:
            p = subprocess.run(["git", "-C", self.repo, "--literal-pathspecs"] + list(args),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.env, stdin=subprocess.DEVNULL)
        except OSError as e:
            raise SetupError("git not runnable: %s" % e.strerror)
        return p.returncode, p.stdout, p.stderr

    def check_root(self):
        rc, out, _ = self.run("rev-parse", "--is-bare-repository")
        if rc != 0:
            raise SetupError("not a git repository: %s" % self.repo)
        if out.strip() == b"true":
            return
        rc, out, _ = self.run("rev-parse", "--show-toplevel")
        top = out.decode("utf-8", "replace").strip()
        if rc != 0 or os.path.realpath(top) != os.path.realpath(self.repo):
            raise SetupError("--repo is not a repository root")

    def resolve(self, rev):
        if not rev or rev.startswith("-"):
            raise SetupError("bad rev")
        rc, out, _ = self.run("rev-parse", "--verify", "--quiet", "--end-of-options", rev + "^{commit}")
        sha = out.decode("ascii", "replace").strip()
        if rc != 0 or len(sha) < 40:
            raise SetupError("rev does not resolve to a commit")
        return sha

    def blob(self, sha, path):
        """Bytes of the regular file `path` in commit `sha`, else None (absent, directory, symlink, submodule,
        or reached through a symlinked directory)."""
        rc, out, _ = self.run("ls-tree", "-z", "--full-tree", sha, "--", path)
        if rc != 0:
            raise SetupError("git ls-tree failed")
        for rec in out.split(b"\0"):
            if not rec or b"\t" not in rec:
                continue
            meta, _, name = rec.partition(b"\t")
            if name.decode("utf-8", "replace") != path:
                continue
            parts = meta.split(b" ")
            if len(parts) != 3 or parts[1] != b"blob" or parts[0].decode("ascii", "replace") not in REGULAR_MODES:
                return None
            rc, data, _ = self.run("cat-file", "blob", parts[2].decode("ascii", "replace"))
            if rc != 0:
                raise SetupError("git cat-file failed for %s" % path)
            return data
        return None


# --------------------------------------------------------------------------- scanners

def split_lines(data):
    return data.decode("utf-8", "replace").split("\n")


def table_cells(line, spans=False):
    """Cell scanner.  A table row starts at column 0 with `|` and (after trailing space/tab/CR) ends with `|`.
    With spans=True a `|` between two single backticks does not split (the frozen K16 quote holds `||`)."""
    s = line.rstrip(" \t\r")
    if len(s) < 2 or s[0] != "|" or s[-1] != "|":
        return None
    cells = []
    cur = []
    in_span = False
    for ch in s[1:-1]:
        if ch == "`" and spans:
            in_span = not in_span
        if ch == "|" and not in_span:
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur))
    return cells


def cell_text(cell):
    return cell.strip(" \t")


def fenced_flags(lines):
    """True for each line that is inside (or opens/closes) a fenced code block."""
    flags = []
    fence = None  # (char, length)
    for ln in lines:
        t = ln.rstrip("\r").lstrip(" ")
        indent_ok = len(ln.rstrip("\r")) - len(t) <= 3
        if fence is None:
            if indent_ok and t[:3] in ("```", "~~~"):
                c = t[0]
                n = 0
                while n < len(t) and t[n] == c:
                    n += 1
                fence = (c, n)
                flags.append(True)
            else:
                flags.append(False)
        else:
            flags.append(True)
            if indent_ok and t and t[0] == fence[0]:
                n = 0
                while n < len(t) and t[n] == fence[0]:
                    n += 1
                if n >= fence[1] and not t[n:].strip(" \t"):
                    fence = None
    return flags


def table_rows(data, spans=False):
    """(lines, fence flags, [(line_index, cells)]) of every non-fenced table row."""
    lines = split_lines(data)
    flags = fenced_flags(lines)
    rows = []
    for i, ln in enumerate(lines):
        if flags[i]:
            continue
        cells = table_cells(ln, spans)
        if cells is not None:
            rows.append((i, cells))
    return lines, flags, rows


def is_digits(s):
    return bool(s) and all(c in "0123456789" for c in s)


def is_row_id(s):
    return len(s) == 3 and s[0] in "KH" and is_digits(s[1:])


def is_sid(s):
    return len(s) == 4 and s[0] == "S" and is_digits(s[1:])


def has_sid(text):
    """True if `text` holds an S### token (S plus exactly three digits, no alphanumeric neighbours)."""
    n = len(text)
    for i in range(n - 3):
        if text[i] == "S" and is_digits(text[i + 1:i + 4]):
            before = text[i - 1] if i > 0 else " "
            after = text[i + 4] if i + 4 < n else " "
            if not (before.isalnum() or before == "_") and not after.isdigit() and not (after.isalpha() and after.isascii()):
                return True
    return False


def urls_in(cell):
    out = []
    for tok in cell.split():
        t = tok.strip("`()<>[]\"',;")
        if t.startswith("https://") or t.startswith("http://"):
            out.append(t)
    return out


def quote_body(cell):
    """The quote of a `<quote>` cell: exactly one backtick opens and one closes the stripped cell, none inside."""
    t = cell_text(cell)
    if len(t) < 3 or t[0] != "`" or t[-1] != "`":
        return None
    body = t[1:-1]
    if "`" in body:
        return None
    return body


# --------------------------------------------------------------------------- tables

def load_tables(blob):
    try:
        t = json.loads(blob.decode("utf-8"))
        c1 = t["c1"]
        for key, typ in (("commit", str), ("entry", str), ("opened", str), ("pin_dir", str), ("new_rows_min", int),
                         ("k", list), ("h", list), ("pin_sha256", dict), ("source_suffix", dict),
                         ("new_row_pins", dict)):
            if not isinstance(c1[key], typ):
                raise ValueError(key)
        seen = set()
        for spec in c1["k"] + c1["h"]:
            if not (isinstance(spec["id"], str) and isinstance(spec["line"], int) and isinstance(spec["pin"], str)
                    and isinstance(spec["quote"], str)) or spec["id"] in seen:
                raise ValueError("row spec")
            seen.add(spec["id"])
            if spec["pin"] not in c1["pin_sha256"]:
                raise ValueError("pin not hashed")
        for name in c1["new_row_pins"]:
            if name not in c1["source_suffix"]:
                raise ValueError("new_row_pins")
        return c1
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        raise SetupError("frozen-tables.json unusable")


def registry(data):
    """{S-id: [row dict]} from every non-fenced table row with >=11 cells whose first cell is an S-id.
    Cells are assigned from the right so a stray `|` inside the title cannot shift them."""
    out = {}
    if data is None:
        return out
    _, _, rows = table_rows(data)
    for _, cells in rows:
        sid = cell_text(cells[0])
        if not is_sid(sid) or len(cells) < 11:
            continue
        out.setdefault(sid, []).append({
            "source": "|".join(cells[1:-9]),
            "tier": cell_text(cells[-8]),
            "status": cell_text(cells[-4]),
            "opened": cell_text(cells[-3]),
            "used_by": cells[-1],
        })
    return out


# --------------------------------------------------------------------------- evaluation

class Result:
    def __init__(self, rev, rows, nk, hosts, nh, src, new_rows, nmin, missed):
        self.rev, self.rows, self.nk, self.hosts, self.nh = rev, rows, nk, hosts, nh
        self.src, self.new_rows, self.nmin, self.missed = src, new_rows, nmin, missed

    @property
    def verdict(self):
        return "TARGET_MET" if not self.missed else "TARGET_MISSED"

    def line(self):
        return ("MADO_KBD_ENTRY: rev=%s rows=%d/%d hosts=%d/%d sources=%d/%d new_rows=%d/%d verdict=%s missed=%s"
                % (self.rev, self.rows, self.nk, self.hosts, self.nh, self.src, self.nk, self.new_rows, self.nmin,
                   self.verdict, ",".join(self.missed) if self.missed else "none"))


def evaluate(repo, rev, work=None):
    g = Git(repo, work)
    g.check_root()
    sha = g.resolve(rev)
    tbl = g.blob(sha, TABLES_PATH)
    if tbl is None:
        raise SetupError("frozen-tables.json absent at rev")
    c1 = load_tables(tbl)
    order = {spec["id"]: n for n, spec in enumerate(c1["k"] + c1["h"])}
    legs = set()  # (group index, id order, leg name)

    def miss(group, ident=None):
        legs.add((GROUPS.index(group), order.get(ident, -1), group if ident is None else "%s:%s" % (group, ident)))

    if hashlib.sha256(tbl).hexdigest() != TABLES_SHA256:
        miss("tables_sha")

    # pins
    pin_dir = c1["pin_dir"]
    pin_lines = {}
    for name, want in sorted(c1["pin_sha256"].items()):
        data = g.blob(sha, pin_dir + "/" + name)
        pin_lines[name] = None if data is None else split_lines(data)
        if data is None or hashlib.sha256(data).hexdigest() != want:
            miss("pin_hash")

    def pin_line(name, line):
        lines = pin_lines.get(name)
        if lines is None or line < 1 or line > len(lines):
            return None
        return lines[line - 1]

    # registry (needed for source_cell and new_rows)
    reg = registry(g.blob(sha, SOURCES_PATH))
    entry_path = c1["entry"]

    # README index row
    readme = g.blob(sha, README_PATH)
    token = "`" + (entry_path.split("/", 1)[1] if entry_path.startswith("corpus/") else entry_path) + "`"
    index_hits = 0
    if readme is not None:
        for _, cells in table_rows(readme)[2]:
            if cell_text(cells[0]).startswith(token):
                index_hits += 1
    if index_hits != 1:
        miss("index")

    # new registry rows
    suffixes = [c1["source_suffix"][n] for n in c1["new_row_pins"]]
    new_rows = 0
    for sid in sorted(reg):
        cand = reg[sid]
        if len(cand) != 1:
            continue
        r = cand[0]
        if (r["opened"] == c1["opened"] and r["tier"] == "A" and r["status"] == "mined" and entry_path in r["used_by"]
                and any(u.endswith(s) for u in urls_in(r["source"]) for s in suffixes)):
            new_rows += 1
    if new_rows < c1["new_rows_min"]:
        miss("new_rows")

    # entry
    entry = g.blob(sha, entry_path)
    nk, nh = len(c1["k"]), len(c1["h"])
    if entry is None:
        miss("entry_absent")
        return Result(rev, 0, nk, 0, nh, 0, new_rows, c1["new_rows_min"], finish(legs))

    lines, flags, rows = table_rows(entry, True)
    head_end = rows[0][0] if rows else len(lines)
    head = [ln.rstrip("\r") for ln in lines[:head_end]]
    src_line = any(ln.startswith("source:") and has_sid(ln) for ln in head)
    ver_line = any(ln.startswith(VERIFIED_PREFIX) and (len(ln) == len(VERIFIED_PREFIX) or not (ln[len(VERIFIED_PREFIX)].isdigit() or ln[len(VERIFIED_PREFIX)] == "-"))
                   for ln in head)
    rec_line = any(ln.startswith("recheck:") for ln in head)
    if not (src_line and ver_line and rec_line):
        miss("provenance")

    by_id = {}
    for _, cells in rows:
        ident = cell_text(cells[0])
        if is_row_id(ident):
            by_id.setdefault(ident, []).append(cells)

    def row_cells(spec, minprop, kind_cell):
        cand = by_id.get(spec["id"], [])
        if len(cand) != 1:
            miss("row", spec["id"])
            return None
        cells = cand[0]
        if len(cells) != 5 or len(cell_text(cells[1])) < minprop or not kind_cell(cell_text(cells[2])):
            miss("row", spec["id"])
            return None
        return cells

    bad = set()
    src_ok = 0
    for spec in c1["k"]:
        ident = spec["id"]
        cells = row_cells(spec, 40, is_sid)
        if cells is None:
            bad.add(ident)
            continue
        if cell_text(cells[3]) != "%s:%d" % (spec["pin"], spec["line"]):
            miss("anchor", ident)
            bad.add(ident)
        pl = pin_line(spec["pin"], spec["line"])
        if quote_body(cells[4]) != spec["quote"] or pl is None or spec["quote"] not in pl:
            miss("quote", ident)
            bad.add(ident)
        # source_cell
        suffix = c1["source_suffix"][spec["pin"]]
        cand = reg.get(cell_text(cells[2]), [])
        ok = False
        if len(cand) == 1 and cand[0]["status"] == "mined":
            for u in urls_in(cand[0]["source"]):
                if u.endswith(suffix) and (c1["commit"] in u or not spec["pin"].startswith("Hyprland-")):
                    ok = True
        if ok:
            src_ok += 1
        else:
            miss("source_cell", ident)

    host_bad = set()
    for spec in c1["h"]:
        ident = spec["id"]
        cells = row_cells(spec, 20, lambda s: s == "host")
        if cells is None:
            host_bad.add(ident)
            continue
        if cell_text(cells[3]) != "%s:%d" % (spec["pin"], spec["line"]):
            miss("anchor", ident)
            host_bad.add(ident)
        pl = pin_line(spec["pin"], spec["line"])
        body = quote_body(cells[4])
        if body != spec["quote"] or pl is None or spec["quote"] not in pl:
            miss("quote", ident)
            host_bad.add(ident)
        if body is None or pl is None or body not in pl:
            miss("host", ident)
            host_bad.add(ident)

    return Result(rev, nk - len(bad), nk, nh - len(host_bad), nh, src_ok, new_rows, c1["new_rows_min"], finish(legs))


def finish(legs):
    return [name for _, _, name in sorted(legs)]


# --------------------------------------------------------------------------- self-test

SELFTEST_SIDS = {  # which registry row each frozen K row cites in the synthetic good tree
    "Hyprland-InputManager.cpp": "S316", "Hyprland-IKeyboard.cpp": "S319", "Hyprland-SeatManager.cpp": "S378",
    "Hyprland-protocols-core-Seat.cpp": "S379", "Hyprland-ConfigValues.cpp": "S318",
    "Hyprland-legacy-ConfigManager.cpp": "S317", "wayland-1.26.0-wayland.xml": "S052",
    "Hyprland-IKeyboard.hpp": "S380",
}
SELFTEST_ROW_ORDER = ("S052", "S162", "S215", "S316", "S317", "S318", "S319", "S378", "S379", "S380")


def _sources_text(c1, mutate=None):
    new = c1["opened"]
    entry = c1["entry"]
    rows = []
    by_suffix = {pin: c1["source_suffix"][pin] for pin in c1["source_suffix"]}
    spec = {  # sid -> (pin, opened, used-by)
        "S052": ("wayland-1.26.0-wayland.xml", "2026-10-20", "corpus/knowledge/input-debugging-boundaries-r15.md"),
        "S162": ("Hyprland-legacy-ConfigManager.cpp", "2026-10-23", "corpus/knowledge/rule-attribution-r24.md"),
        "S215": ("Hyprland-ConfigValues.cpp", "2026-10-25", "corpus/knowledge/event-queue-observability-r37.md"),
        "S316": ("Hyprland-InputManager.cpp", "2026-10-26", "corpus/knowledge/hyprland-input-devices-r46.md"),
        "S317": ("Hyprland-legacy-ConfigManager.cpp", "2026-10-26", "corpus/knowledge/hyprland-input-devices-r46.md"),
        "S318": ("Hyprland-ConfigValues.cpp", "2026-10-26", "corpus/knowledge/hyprland-input-devices-r46.md"),
        "S319": ("Hyprland-IKeyboard.cpp", "2026-10-26", "corpus/knowledge/hyprland-input-devices-r46.md"),
        "S378": ("Hyprland-SeatManager.cpp", new, entry),
        "S379": ("Hyprland-protocols-core-Seat.cpp", new, entry),
        "S380": ("Hyprland-IKeyboard.hpp", new, entry),
    }
    for sid in SELFTEST_ROW_ORDER:
        pin, opened, used = spec[sid]
        if pin.startswith("wayland"):
            url = "https://gitlab.freedesktop.org/wayland/wayland/-/raw/" + by_suffix[pin]
        else:
            url = "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/%s" % (c1["commit"], by_suffix[pin])
        rows.append("| %s | Synthetic source %s - %s | code | A | scope text | anchor text | teaches text | mined | %s | on-release | %s |"
                    % (sid, sid, url, opened, used))
    head = ["# SOURCES (selftest fixture)", "", "## Registry", "",
            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    return "\n".join(head + rows) + "\n"


def _readme_text(c1):
    token = "`" + c1["entry"].split("/", 1)[1] + "`"
    return "\n".join(["# Corpus README (selftest fixture)", "", "| entry | what |", "|---|---|",
                      "| `knowledge/other-entry.md` (MADO-R46-1) | something else |",
                      "| %s (MADO-R55-1, selftest) | keyboard repeat and numlock |" % token, ""])


def _entry_text(c1):
    out = ["# Synthetic keyboard repeat entry (selftest fixture)", "",
           "source: S316 S317 S318 S319 S052 S378 S379 S380 - synthetic",
           "verified-at: 2026-10-28", "recheck: on-release", "",
           "| id | proposition | source | anchor | quote |", "|---|---|---|---|---|"]
    for spec in c1["k"]:
        prop = "Synthetic proposition %s drawn from pin %s line %d of the frozen source text." % (spec["id"], spec["pin"], spec["line"])
        out.append("| %s | %s | %s | %s:%d | `%s` |" % (spec["id"], prop, SELFTEST_SIDS[spec["pin"]], spec["pin"], spec["line"], spec["quote"]))
    out.append("")
    for spec in c1["h"]:
        prop = "Synthetic host fact %s from %s line %d." % (spec["id"], spec["pin"], spec["line"])
        out.append("| %s | %s | host | %s:%d | `%s` |" % (spec["id"], prop, spec["pin"], spec["line"], spec["quote"]))
    return "\n".join(out) + "\n"


def _swap(text, old, new, count=1):
    if old not in text:
        raise AssertionError("selftest mutation did not apply: %r" % old)
    return text.replace(old, new, count)


def _row_edit(text, ident, old, new):
    lines = text.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln.startswith("| %s |" % ident)]
    if len(hits) != 1:
        raise AssertionError("selftest row %s not unique" % ident)
    lines[hits[0]] = _swap(lines[hits[0]], old, new)
    return "\n".join(lines)


def _row_drop(text, ident):
    lines = text.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln.startswith("| %s |" % ident)]
    if len(hits) != 1:
        raise AssertionError("selftest row %s not unique" % ident)
    del lines[hits[0]]
    return "\n".join(lines)


def _row_dup(text, ident):
    lines = text.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln.startswith("| %s |" % ident)]
    lines.insert(hits[0], lines[hits[0]])
    return "\n".join(lines)


def selftest(repo, rev, work):
    g = Git(repo, work)
    g.check_root()
    sha = g.resolve(rev)
    tbl = g.blob(sha, TABLES_PATH)
    if tbl is None:
        raise SetupError("frozen-tables.json absent at rev")
    c1 = load_tables(tbl)
    pin_bytes = {}
    for name in c1["pin_sha256"]:
        data = g.blob(sha, c1["pin_dir"] + "/" + name)
        if data is None:
            raise SetupError("selftest needs pin %s at rev" % name)
        pin_bytes[name] = data
    nk, nh = len(c1["k"]), len(c1["h"])
    ids_k = [s["id"] for s in c1["k"]]
    ids_h = [s["id"] for s in c1["h"]]
    pdir = c1["pin_dir"]
    epath = c1["entry"]

    def good_files():
        f = {TABLES_PATH: tbl, epath: _entry_text(c1).encode(), README_PATH: _readme_text(c1).encode(),
             SOURCES_PATH: _sources_text(c1).encode()}
        for name, data in pin_bytes.items():
            f[pdir + "/" + name] = data
        return f

    def ed(path, fn):
        def go(f):
            f[path] = fn(f[path].decode("utf-8")).encode("utf-8")
        return go

    def entry_ed(fn):
        return ed(epath, fn)

    def many(*fns):
        def go(f):
            for fn in fns:
                fn(f)
        return go

    def nib(h):
        return ("0" if h[0] != "0" else "1") + h[1:]

    def pin_tamper(f):
        name = "Hyprland-IKeyboard.cpp"
        f[TABLES_PATH] = _swap(tbl.decode(), c1["pin_sha256"][name], nib(c1["pin_sha256"][name])).encode()
        f[pdir + "/" + name] = pin_bytes[name] + b" "

    def symlink_pin(f):
        name = pdir + "/Hyprland-IKeyboard.cpp"
        f["sidecar/IKeyboard.cpp"] = f[name]
        f[name] = ("symlink", "../../../../sidecar/IKeyboard.cpp")

    def symlink_dir(f):
        for name in c1["pin_sha256"]:
            f["realfetch/" + name] = f.pop(pdir + "/" + name)
        f[pdir] = ("symlink", "../../../realfetch")

    def fence_row(text):
        lines = text.split("\n")
        i = [n for n, ln in enumerate(lines) if ln.startswith("| K07 |")][0]
        lines[i:i + 1] = ["```", lines[i], "```"]
        return "\n".join(lines)

    def crlf(f):
        for p in (epath, README_PATH, SOURCES_PATH):
            f[p] = f[p].replace(b"\n", b"\r\n")

    def trail(text):
        return "\n".join((ln + "  \t " if ln.startswith("|") else ln) for ln in text.split("\n"))

    def unknown(group, ids):
        return ["%s:%s" % (group, i) for i in ids]

    # case: (name, mutate(files) or None, expected (rows, hosts, sources, new_rows, missed list))
    MET = (nk, nh, nk, 3, [])
    cases = [
        ("good", None, MET),
        ("C1-CTL-1-absent", lambda f: f.pop(epath), (0, 0, 0, 3, ["entry_absent"])),
        ("C1-CTL-2-spliced-quote", entry_ed(lambda t: _row_edit(t, "K04", "`std::max(0, REPEATRATE);`", "`std::max(0, REPEATRATE) ;`")),
         (nk - 1, nh, nk, 3, ["quote:K04"])),
        ("C1-CTL-3-shifted-anchor", entry_ed(lambda t: _row_edit(t, "K01", ":1220", ":1219")), (nk - 1, nh, nk, 3, ["anchor:K01"])),
        ("C1-CTL-4-wrong-source", entry_ed(lambda t: _row_edit(t, "K10", "S378", "S316")), (nk, nh, nk - 1, 3, ["source_cell:K10"])),
        ("C1-CTL-5-dropped-row", entry_ed(lambda t: _row_drop(t, "K17")), (nk - 1, nh, nk - 1, 3, ["row:K17"])),
        ("C1-CTL-6-host-forged", entry_ed(lambda t: _row_edit(t, "H02", "repeat_delay = 250", "repeat_delay = 300")),
         (nk, nh - 1, nk, 3, ["quote:H02", "host:H02"])),
        ("C1-CTL-7-pin-tamper", pin_tamper, (nk, nh, nk, 3, ["pin_hash", "tables_sha"])),
        ("dup-K05-row", entry_ed(lambda t: _row_dup(t, "K05")), (nk - 1, nh, nk - 1, 3, ["row:K05"])),
        ("dup-H01-row", entry_ed(lambda t: _row_dup(t, "H01")), (nk, nh - 1, nk, 3, ["row:H01"])),
        ("crlf-everywhere-tolerated", crlf, MET),
        ("trailing-space-after-rows-tolerated", entry_ed(trail), MET),
        ("double-backtick-quote-K02", entry_ed(lambda t: _row_edit(t, "K02", "`getDeviceInt(devname, \"repeat_delay\", \"input:repeat_delay\");`",
                                                                   "``getDeviceInt(devname, \"repeat_delay\", \"input:repeat_delay\");``")),
         (nk - 1, nh, nk, 3, ["quote:K02"])),
        ("no-backtick-quote-K03", entry_ed(lambda t: _row_edit(t, "K03", "`getDeviceInt(devname, \"numlock_by_default\", \"input:numlock_by_default\");`",
                                                               "getDeviceInt(devname, \"numlock_by_default\", \"input:numlock_by_default\");")),
         (nk - 1, nh, nk, 3, ["quote:K03"])),
        ("pinned-symlink-file-IKeyboard.cpp", symlink_pin, (nk - 2, nh, nk, 3, ["quote:K08", "quote:K09", "pin_hash"])),
        ("pin-dir-is-symlink", symlink_dir, (0, 0, nk, 3, unknown("quote", ids_k + ids_h) + ["pin_hash"] + unknown("host", ids_h))),
        ("index-row-missing", ed(README_PATH, lambda t: _row_drop_readme(t)), (nk, nh, nk, 3, ["index"])),
        ("index-row-duplicated", ed(README_PATH, lambda t: _dup_readme(t)), (nk, nh, nk, 3, ["index"])),
        ("index-prose-only", ed(README_PATH, lambda t: _prose_readme(t)), (nk, nh, nk, 3, ["index"])),
        ("provenance-no-recheck", entry_ed(lambda t: _swap(t, "recheck: on-release\n", "")), (nk, nh, nk, 3, ["provenance"])),
        ("provenance-wrong-date", entry_ed(lambda t: _swap(t, "2026-10-28", "2026-10-27")), (nk, nh, nk, 3, ["provenance"])),
        ("provenance-source-without-sid", entry_ed(lambda t: _swap(t, "source: S316 S317 S318 S319 S052 S378 S379 S380 - synthetic", "source: synthetic")),
         (nk, nh, nk, 3, ["provenance"])),
        ("new-rows-S379-opened-old", ed(SOURCES_PATH, lambda t: _row_edit(t, "S379", "2026-10-28", "2026-10-27")), (nk, nh, nk, 2, ["new_rows"])),
        ("new-rows-S378-usedby-missing-entry", ed(SOURCES_PATH, lambda t: _row_edit(t, "S378", "| " + epath + " |", "| corpus/knowledge/x.md |")),
         (nk, nh, nk, 2, ["new_rows"])),
        ("source-S380-not-mined", ed(SOURCES_PATH, lambda t: _row_edit(t, "S380", "| mined |", "| queued |")), (nk, nh, nk - 1, 2, ["source_cell:K18", "new_rows"])),
        ("source-S379-url-without-commit", ed(SOURCES_PATH, lambda t: _row_edit(t, "S379", c1["commit"], "main")),
         (nk, nh, nk - 2, 3, ["source_cell:K11", "source_cell:K12"])),
        ("source-K11-cites-wrong-suffix", entry_ed(lambda t: _row_edit(t, "K11", "S379", "S317")), (nk, nh, nk - 1, 3, ["source_cell:K11"])),
        ("tables-sha-trailing-newline", lambda f: f.update({TABLES_PATH: tbl + b"\n"}), (nk, nh, nk, 3, ["tables_sha"])),
        ("backticked-pipes-in-proposition-tolerated", entry_ed(lambda t: _row_edit(t, "K05", "Synthetic proposition K05", "Synthetic `a || b` proposition K05")), MET),
        ("escaped-pipes-in-K16-quote", entry_ed(lambda t: _row_edit(t, "K16", "!VAL || !VAL", "!VAL \\|\\| !VAL")), (nk - 1, nh, nk, 3, ["quote:K16"])),
        ("unbalanced-backtick-in-proposition-K05", entry_ed(lambda t: _row_edit(t, "K05", "Synthetic proposition K05", "Synthetic `proposition K05")), (nk - 1, nh, nk - 1, 3, ["row:K05"])),
        ("short-proposition-K06", entry_ed(lambda t: _row_edit(t, "K06", "Synthetic proposition K06 drawn from pin Hyprland-InputManager.cpp line 1284 of the frozen source text.", "too short")),
         (nk - 1, nh, nk - 1, 3, ["row:K06"])),
        ("extra-cell-K13", entry_ed(lambda t: _row_edit(t, "K13", "` |", "` | extra |")), (nk - 1, nh, nk - 1, 3, ["row:K13"])),
        ("host-row-wrong-kind-cell-H05", entry_ed(lambda t: _row_edit(t, "H05", "| host |", "| S316 |")), (nk, nh - 1, nk, 3, ["row:H05"])),
        ("anchor-H03-line-shifted", entry_ed(lambda t: _row_edit(t, "H03", ":18 |", ":19 |")), (nk, nh - 1, nk, 3, ["anchor:H03"])),
        ("row-hidden-in-code-fence-K07", entry_ed(fence_row), (nk - 1, nh, nk - 1, 3, ["row:K07"])),
    ]

    lines_out = []
    passed = 0
    D = tempfile.mkdtemp(prefix="c1b-", dir=work)
    try:
        def git(*a, check=True):
            p = subprocess.run(["git", "-C", D] + list(a), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=g.env, stdin=subprocess.DEVNULL)
            if check and p.returncode != 0:
                raise SetupError("scratch git %s failed: %s" % (a[0], p.stderr.decode("utf-8", "replace").strip()))
            return p.stdout.decode("utf-8", "replace").strip()

        git("init", "-q")
        if os.path.realpath(git("rev-parse", "--show-toplevel")) != os.path.realpath(D):
            raise SetupError("scratch repo toplevel mismatch")

        def commit_tree(files, msg):
            for n in os.listdir(D):
                if n != ".git":
                    p = os.path.join(D, n)
                    shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.remove(p)
            for rel, data in sorted(files.items()):
                p = os.path.join(D, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                if isinstance(data, tuple):
                    os.symlink(data[1], p)
                else:
                    with open(p, "wb") as fh:
                        fh.write(data)
            git("add", "-A", "-f")
            git("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", msg)
            return git("rev-parse", "HEAD")

        for name, mut, (er, eh, es, en, em) in cases:
            files = good_files()
            if mut is not None:
                mut(files)
            c = commit_tree(files, name)
            want = Result(c, er, nk, eh, nh, es, en, c1["new_rows_min"], em).line()
            res = evaluate(D, c, work)
            got = res.line()
            ok = got == want
            passed += ok
            lines_out.append("SELFTEST case=%s %s" % (name, "ok" if ok else "FAIL"))
            lines_out.append("  want %s" % want)
            if not ok:
                lines_out.append("  got  %s" % got)
            else:
                lines_out.append("  got  (identical)")

        # worktree is never read: commit the good tree, then edit the entry and the pins in the working tree only
        files = good_files()
        c = commit_tree(files, "good-then-dirty-worktree")
        with open(os.path.join(D, epath), "wb") as fh:
            fh.write(b"dirty\n")
        os.remove(os.path.join(D, pdir, "Hyprland-IKeyboard.cpp"))
        res = evaluate(D, c, work)
        want = Result(c, nk, nk, nh, nh, nk, 3, 3, []).line()
        ok = res.line() == want
        passed += ok
        total = len(cases) + 1
        lines_out.append("SELFTEST case=worktree-edit-not-read %s" % ("ok" if ok else "FAIL"))
        lines_out.append("  want %s" % want)
        lines_out.append("  got  %s" % ("(identical)" if ok else res.line()))

        # exit statuses and stdout exactness through the real command line
        def cli(args):
            p = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=g.env, stdin=subprocess.DEVNULL, cwd=work)
            return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")

        good_c = commit_tree(good_files(), "cli-good")
        bad_files = good_files()
        del bad_files[epath]
        bad_c = commit_tree(bad_files, "cli-bad")
        for label, args, want_rc, prefix in (
                ("cli-good-rc0", ["--repo", D, "--rev", good_c, "--work", work], 0, "MADO_KBD_ENTRY: rev=%s rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none" % good_c),
                ("cli-miss-rc1", ["--repo", D, "--rev", bad_c, "--work", work], 1, "MADO_KBD_ENTRY: rev=%s rows=0/18 hosts=0/6 sources=0/18 new_rows=3/3 verdict=TARGET_MISSED missed=entry_absent" % bad_c),
                ("cli-bad-rev-rc2", ["--repo", D, "--rev", "no-such-rev", "--work", work], 2, "MADO_KBD_ENTRY: SETUP "),
                ("cli-not-a-repo-rc2", ["--repo", work, "--rev", good_c, "--work", work], 2, "MADO_KBD_ENTRY: SETUP "),
                ("cli-missing-args-rc2", ["--repo", D], 2, "MADO_KBD_ENTRY: SETUP "),
                ("cli-unknown-flag-rc2", ["--repo", D, "--rev", good_c, "--bogus"], 2, "MADO_KBD_ENTRY: SETUP ")):
            rc, out, err = cli(args)
            if want_rc == 2:
                ok = rc == 2 and out.startswith(prefix) and out.count("\n") == 1 and out.endswith("\n")
            else:
                ok = rc == want_rc and out == prefix + "\n"
            total += 1
            passed += ok
            lines_out.append("SELFTEST case=%s %s (rc=%d stdout=%r)" % (label, "ok" if ok else "FAIL", rc, out if not ok or want_rc == 2 else "<exact line>"))
        # tables absent -> setup error
        nt = good_files()
        del nt[TABLES_PATH]
        nc = commit_tree(nt, "cli-no-tables")
        rc, out, err = cli(["--repo", D, "--rev", nc, "--work", work])
        ok = rc == 2 and out.startswith("MADO_KBD_ENTRY: SETUP ")
        total += 1
        passed += ok
        lines_out.append("SELFTEST case=cli-no-tables-rc2 %s (rc=%d)" % ("ok" if ok else "FAIL", rc))
    finally:
        shutil.rmtree(D, ignore_errors=True)
    lines_out.append("MADO_R55_C1_SELFTEST: cases=%d/%d verdict=%s" % (passed, total, "OK" if passed == total else "FAIL"))
    return passed == total, lines_out


def _readme_entry_line(c1_token, lines):
    return [i for i, ln in enumerate(lines) if ln.startswith("| " + c1_token)]


def _row_drop_readme(text):
    lines = text.split("\n")
    i = _readme_entry_line("`knowledge/hyprland-keyboard-repeat-numlock-r55.md`", lines)[0]
    del lines[i]
    return "\n".join(lines)


def _dup_readme(text):
    lines = text.split("\n")
    i = _readme_entry_line("`knowledge/hyprland-keyboard-repeat-numlock-r55.md`", lines)[0]
    lines.insert(i, lines[i])
    return "\n".join(lines)


def _prose_readme(text):
    lines = text.split("\n")
    i = _readme_entry_line("`knowledge/hyprland-keyboard-repeat-numlock-r55.md`", lines)[0]
    lines[i] = "- Round 55: see `knowledge/hyprland-keyboard-repeat-numlock-r55.md` for the entry."
    return "\n".join(lines)


# --------------------------------------------------------------------------- main

class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise SetupError("usage: %s" % message.replace("\n", " "))


def main(argv):
    ap = Parser(prog="c1-r55-kbd-entry.py", add_help=False, allow_abbrev=False)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args(argv)
        if a.repo is None or (a.rev is None and not a.selftest):
            raise SetupError("usage: --repo and --rev are required")
        work = None
        if a.work is not None:
            work = os.path.abspath(a.work)
            try:
                os.makedirs(work, exist_ok=True)
            except OSError as e:
                raise SetupError("--work unusable: %s" % e.strerror)
        if a.selftest:
            if work is None:
                raise SetupError("usage: --selftest needs --work")
            ok, out = selftest(a.repo, a.rev or "HEAD", work)
            print("\n".join(out))
            return 0 if ok else 1
        res = evaluate(a.repo, a.rev, work)
        print(res.line())
        return 0 if not res.missed else 1
    except SetupError as e:
        print("MADO_KBD_ENTRY: SETUP %s" % e)
        return 2
    except (OSError, UnicodeError, subprocess.SubprocessError) as e:
        print("MADO_KBD_ENTRY: SETUP internal %s" % type(e).__name__)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

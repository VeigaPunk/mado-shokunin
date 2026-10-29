#!/usr/bin/env python3
"""PRED-C1-r56 counter (seat R56ExecC1CounterB): the autoreload entry, from registration.md section C1.

    python3 -I c1-r56-autoreload-entry.py --repo REPO --rev REV --work DIR
    python3 -I c1-r56-autoreload-entry.py --selftest [--repo REPO] [--rev REV] [--work DIR]

Reads ONLY git objects at REV of REPO (git rev-parse / ls-tree / cat-file through subprocess).
Prints exactly one line on stdout; exit 0 on TARGET_MET, 1 on a miss, 2 on a setup error
(reason on stderr, nothing on stdout).  The counter writes nothing except creating --work.

Parsing strategy: a character-level block scanner (fences and HTML comments), a cell tokenizer for
table rows, and a locator-list scanner for the registry anchor cell.  No line regex decides a row.
"""
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

TABLES_SHA256 = "9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2"
TABLES_PATH = ".ufo/waves/round-56/frozen-tables-v2.json"
ECHO_MIN = 30
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
INDEX_PATH = "corpus/README.md"
REGISTRY_PATH = "corpus/SOURCES.md"
PIN_DIR = ".ufo/waves/round-56/fetch"
OPENED = "2026-10-28"
INDEX_PREFIX = "| `knowledge/hyprland-config-autoreload-r56.md`"
K_IDS = ["K%02d" % i for i in range(1, 31)]
H_IDS = ["H%02d" % i for i in range(1, 4)]
K_MIN, H_MIN = 40, 20
REGULAR_MODES = ("100644", "100755")
NEW_ROWS_DENOM = 8


class Setup(Exception):
    pass


# ----------------------------------------------------------------------------- git object access

class Repo:
    def __init__(self, repo, work):
        if not os.path.isdir(repo):
            raise Setup("repo is not a directory: %s" % repo)
        try:
            os.makedirs(work, exist_ok=True)
        except OSError as e:
            raise Setup("cannot create --work: %s" % e)
        self.repo = repo
        self.env = {
            "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
            "HOME": work, "TMPDIR": work, "LC_ALL": "C",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_TERMINAL_PROMPT": "0",
        }
        self.trees = {}
        self.blobs = {}
        self.commit = None
        self.root = None

    def git(self, *args, check=True):
        try:
            p = subprocess.run(["git", "-C", self.repo] + list(args), env=self.env,
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        except OSError as e:
            raise Setup("cannot run git: %s" % e)
        if check and p.returncode != 0:
            raise Setup("git %s failed: %s" % (" ".join(args[:2]), p.stderr.decode("utf-8", "replace").strip()[:200]))
        return p

    def resolve(self, rev):
        if not rev or rev.startswith("-"):
            raise Setup("bad rev: %r" % rev)
        p = self.git("rev-parse", "--verify", "-q", rev + "^{commit}", check=False)
        if p.returncode != 0:
            raise Setup("rev does not resolve to a commit: %s" % rev)
        self.commit = p.stdout.decode().strip()
        q = self.git("rev-parse", "--verify", "-q", self.commit + "^{tree}", check=False)
        if q.returncode != 0:
            raise Setup("commit has no tree: %s" % rev)
        self.root = q.stdout.decode().strip()

    def listing(self, tree_oid):
        if tree_oid not in self.trees:
            out = self.git("ls-tree", "-z", tree_oid).stdout
            ents = {}
            for rec in out.split(b"\0"):
                if not rec:
                    continue
                meta, _, name = rec.partition(b"\t")
                mode, typ, oid = meta.decode().split(" ")
                ents[name] = (mode, typ, oid)
            self.trees[tree_oid] = ents
        return self.trees[tree_oid]

    def regular_oid(self, path):
        """oid of a regular blob at path, else None (symlink blob, symlinked dir, missing -> absent)."""
        comps = [c for c in path.split("/")]
        if any(c in ("", ".", "..") for c in comps):
            return None
        cur = self.root
        for i, c in enumerate(comps):
            ent = self.listing(cur).get(c.encode())
            if ent is None:
                return None
            mode, typ, oid = ent
            if i < len(comps) - 1:
                if mode != "040000" or typ != "tree":
                    return None
                cur = oid
            else:
                if typ != "blob" or mode not in REGULAR_MODES:
                    return None
                return oid
        return None

    def blob(self, path):
        oid = self.regular_oid(path)
        if oid is None:
            return None
        if oid not in self.blobs:
            self.blobs[oid] = self.git("cat-file", "blob", oid).stdout
        return self.blobs[oid]


# ----------------------------------------------------------------------------- text scanners

def split_lines(data):
    return data.decode("utf-8", "replace").split("\n")


def fence_open(line):
    """(char, length) when the line opens a fenced block (0-3 leading spaces), else None."""
    n = 0
    while n < len(line) and line[n] == " ":
        n += 1
    if n > 3 or n >= len(line) or line[n] not in "`~":
        return None
    ch = line[n]
    m = n
    while m < len(line) and line[m] == ch:
        m += 1
    if m - n < 3:
        return None
    if ch == "`" and "`" in line[m:]:
        return None
    return (ch, m - n)


def fence_close(line, ch, length):
    n = 0
    while n < len(line) and line[n] == " ":
        n += 1
    if n > 3:
        return False
    m = n
    while m < len(line) and line[m] == ch:
        m += 1
    return m - n >= length and line[m:].strip(" \t") == ""


def live_lines(lines):
    """Yield (index, line) for lines outside fenced blocks whose first '|' is not inside an HTML comment."""
    out = []
    in_fence = None
    in_comment = False
    for idx, line in enumerate(lines):
        if not in_comment:
            if in_fence is not None:
                if fence_close(line, *in_fence):
                    in_fence = None
                continue
            fo = fence_open(line)
            if fo is not None:
                in_fence = fo
                continue
        i = 0
        first_pipe_live = None
        while i < len(line):
            if in_comment:
                if line.startswith("-->", i):
                    in_comment = False
                    i += 3
                    continue
                if line[i] == "|" and first_pipe_live is None:
                    first_pipe_live = False
                i += 1
            else:
                if line.startswith("<!--", i):
                    in_comment = True
                    i += 4
                    continue
                if line[i] == "|" and first_pipe_live is None:
                    first_pipe_live = True
                i += 1
        if first_pipe_live:
            out.append((idx, line))
    return out


def first_cell(line):
    """Text of the first cell of a pipe row (leading blanks tolerated), or None if not a pipe row."""
    i = 0
    while i < len(line) and line[i] in " \t":
        i += 1
    if i >= len(line) or line[i] != "|":
        return None
    j = line.find("|", i + 1)
    if j < 0:
        return None
    return line[i + 1:j].strip()


def strict_row(line):
    """Cells of a line shaped exactly `| c0 | c1 | ... | cN |` (single spaces, no trailing byte), else None."""
    if not (line.startswith("| ") and line.endswith(" |")) or len(line) < 4:
        return None
    return line[2:-2].split(" | ")


def lenient_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def registry_cells(line):
    """Registry row cells: outer pipes stripped, split on '|', each cell stripped."""
    return lenient_row(line)


def registry_id(line):
    """Id token of a registry row per ^ {0,3}\\|\\s*S[0-9]{3,}\\s*\\| (hand-scanned), else None."""
    n = 0
    while n < len(line) and line[n] == " ":
        n += 1
    if n > 3 or n >= len(line) or line[n] != "|":
        return None
    j = n + 1
    while j < len(line) and line[j].isspace():
        j += 1
    if j >= len(line) or line[j] != "S":
        return None
    k = j + 1
    while k < len(line) and line[k] in "0123456789":
        k += 1
    if k - j - 1 < 3:
        return None
    e = k
    while e < len(line) and line[e].isspace():
        e += 1
    if e >= len(line) or line[e] != "|":
        return None
    return line[j:k]


def scope_covers(anchor, basename, line, nlines=None):
    """True when after some `<basename>:` the comma-separated N / N-M locator list holds a range with line, and (registration-v2 E3)
    every locator of that basename is bounded above by nlines (the pin's line count) when nlines is given."""
    key = basename + ":"
    pos = anchor.find(key)
    covered = False
    over = False
    while pos >= 0:
        i = pos + len(key)
        while True:
            j = i
            while j < len(anchor) and anchor[j] in "0123456789":
                j += 1
            if j == i:
                break
            lo = int(anchor[i:j]) if j - i < 19 else None
            hi = lo
            k = j
            if k < len(anchor) and anchor[k] == "-":
                m = k + 1
                while m < len(anchor) and anchor[m] in "0123456789":
                    m += 1
                if m > k + 1:
                    hi = int(anchor[k + 1:m]) if m - k - 1 < 19 else None
                    k = m
            if lo is None or hi is None or (nlines is not None and (hi > nlines or lo > nlines)):
                over = True
            elif lo <= line <= hi:
                covered = True
            if k < len(anchor) and anchor[k] == ",":
                k += 1
                while k < len(anchor) and anchor[k] == " ":
                    k += 1
                i = k
                continue
            break
        pos = anchor.find(key, pos + 1)
    return covered and not over


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
RUN_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
SID_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
URL_RE = re.compile(r"https?://\S+")


def to_int(run):
    return int(run) if len(run) < 19 else None


# ----------------------------------------------------------------------------- evaluation

def load_tables(repo):
    data = repo.blob(TABLES_PATH)
    if data is None:
        return None, False
    ok = hashlib.sha256(data).hexdigest() == TABLES_SHA256
    try:
        t = json.loads(data.decode("utf-8"))
        c1 = t["c1"]
        for key in ("k", "h", "pin_sha256", "host_pin_sha256", "pin_suffix", "rev_rule", "rows", "new_row_ids"):
            c1[key]
        for r in c1["k"]:
            r["id"], r["line"], r["pin"], r["quote"], r["sid"]
        for r in c1["h"]:
            r["id"], r["line"], r["pin"], r["quote"]
        int(c1["k"][0]["line"])
    except (ValueError, KeyError, TypeError, IndexError):
        return None, ok
    return c1, ok


def evaluate(repo):
    missed = []
    c1, tables_ok = load_tables(repo)
    if not tables_ok:
        missed.append("tables_sha")

    registry = {}
    reg_data = repo.blob(REGISTRY_PATH)
    if reg_data is not None:
        for line in split_lines(reg_data):
            rid = registry_id(line)
            if rid is not None:
                registry.setdefault(rid, []).append(line)

    entry_data = repo.blob(ENTRY)
    entry_present = entry_data is not None
    if not entry_present:
        missed.append("entry_absent")
    entry_lines = split_lines(entry_data) if entry_present else []

    # candidate rows of the entry: id -> [line, ...]
    cand = {}
    if entry_present:
        known = set(K_IDS) | set(H_IDS)
        if c1 is not None:
            known |= {r["id"] for r in c1["k"]} | {r["id"] for r in c1["h"]}
        for _, line in live_lines(entry_lines):
            fc = first_cell(line)
            if fc in known:
                cand.setdefault(fc, []).append(line)

    # proposition multiplicity across every candidate row line
    prop_count = {}
    for lines in cand.values():
        for line in lines:
            cells = strict_row(line)
            if cells is None:
                cells = lenient_row(line)
            if len(cells) >= 2:
                prop_count[cells[1]] = prop_count.get(cells[1], 0) + 1

    def row_data(rid):
        """(strict_cells_or_None, best_effort_cells_or_None) of the single candidate line for rid."""
        lines = cand.get(rid, [])
        if len(lines) != 1:
            return None, None
        strict = strict_row(lines[0])
        if strict is not None and len(strict) == 5:
            return strict, strict
        lc = lenient_row(lines[0])
        return None, (lc if len(lc) == 5 else None)

    # ---- prov
    sids_cited = set()
    if c1 is not None and entry_present:
        for r in c1["k"]:
            _, be = row_data(r["id"])
            if be is not None:
                sids_cited.add(be[2])
    elif entry_present:
        for rid in K_IDS:
            _, be = row_data(rid)
            if be is not None:
                sids_cited.add(be[2])
    if entry_present:
        head = entry_lines[:15]
        src_idx = [i for i, l in enumerate(head) if l.startswith("source:")]
        ver_idx = [i for i, l in enumerate(head) if l.rstrip(" \t\r") == "verified-at: " + OPENED]
        rec_idx = [i for i, l in enumerate(head) if l.startswith("recheck:")]
        prov_ok = bool(src_idx) and len(ver_idx) == 1 and bool(rec_idx)
        if prov_ok:
            prov_ok = min(src_idx) < ver_idx[0] < max(rec_idx)
        src_set = set()
        for i in src_idx:
            src_set.update(SID_RE.findall(head[i]))
        if any(s not in registry for s in src_set):
            prov_ok = False
        if not sids_cited <= src_set:
            prov_ok = False
        if not prov_ok:
            missed.append("prov")

    # ---- index
    readme = repo.blob(INDEX_PATH)
    idx_hits = 0
    if readme is not None:
        idx_hits = sum(1 for l in split_lines(readme) if l.startswith(INDEX_PREFIX))
    if idx_hits != 1:
        missed.append("index")

    counts = dict(a=0, b=0, c=0, d=0, e=0, m=0)
    if c1 is None:
        return finish(repo, missed, counts, entry_present)

    pins_all = dict(c1["pin_sha256"])
    pins_all.update(c1["host_pin_sha256"])
    pin_lines = {}

    def pin_line(pin, n):
        if pin not in pin_lines:
            d = repo.blob(PIN_DIR + "/" + pin)
            pin_lines[pin] = d.split(b"\n") if d is not None else None
        pl = pin_lines[pin]
        if pl is None or not isinstance(n, int) or n < 1 or n > len(pl):
            return None
        return pl[n - 1]

    def basename_of(pin):
        return c1["pin_suffix"][pin].rsplit("/", 1)[-1]

    def rev_token(pin):
        for pat, tok in c1["rev_rule"].items():
            if fnmatch.fnmatchcase(pin, pat):
                return tok
        return None

    def registry_row(sid):
        rows = registry.get(sid, [])
        if len(rows) != 1:
            return None
        cells = registry_cells(rows[0])
        return cells if len(cells) == 11 else None

    def source_cell_ok(sid, pin):
        cells = registry_row(sid)
        if cells is None:
            return False
        if cells[7] != "mined" or cells[3] not in ("A", "B") or cells[8] != OPENED:
            return False
        urls = URL_RE.findall(cells[1])
        suffix = c1["pin_suffix"].get(pin)
        tok = rev_token(pin)
        if not urls or suffix is None or tok is None:
            return False
        if not urls[-1].endswith("/" + suffix) or tok not in urls[-1]:
            return False
        return ENTRY in cells[10]

    def scope_ok(sid, pin, line):
        cells = registry_row(sid)
        if cells is None or pin not in c1["pin_suffix"]:
            return False
        pl = pin_lines.get(pin)
        if pl is None:
            pin_line(pin, 1)
            pl = pin_lines.get(pin)
        return scope_covers(cells[5], basename_of(pin), line, len(pl) if pl is not None else None)

    def content_ok(rid, prop, quote, line, pin):
        tok = bool(set(TOKEN_RE.findall(prop)) & set(TOKEN_RE.findall(quote)))
        runs = set(re.findall(r"[0-9]+", quote))
        ints = {0, 1, 2, 3, line}
        for r in c1["k"]:
            if r["pin"] == pin:
                ints.add(r["line"])
        num = True
        for run in RUN_RE.findall(prop):
            v = to_int(run)
            if run in runs or (v is not None and v in ints):
                continue
            num = False
        echo = not (len(quote) >= ECHO_MIN and quote in prop)
        return tok, num, echo

    row_ok, quote_ok, host_ok = {}, {}, {}
    leg_row, leg_quote, leg_host, leg_src, leg_scope, leg_tok, leg_num = [], [], [], [], [], [], []
    tok_ok, num_ok, src_ok, scope_flag, echo_ok = {}, {}, {}, {}, {}

    all_rows = [(r, "K") for r in c1["k"]] + [(r, "H") for r in c1["h"]]
    for r, kind in all_rows:
        rid, pin, line, quote = r["id"], r["pin"], r["line"], r["quote"]
        strict, best = row_data(rid)
        # row grammar
        ok = False
        if entry_present and strict is not None and len(cand[rid]) == 1:
            ok = True
            if any("|" in c for c in strict):
                ok = False
            if strict[0] != rid:
                ok = False
            if kind == "K" and not (len(strict[2]) == 4 and strict[2][0] == "S" and strict[2][1:].isdigit()
                                    and strict[2][1:].isascii()):
                ok = False
            if kind == "H" and strict[2] != "host":
                ok = False
            if strict[3] != "%s:%s" % (pin, line):
                ok = False
            if strict[4] != "`" + quote + "`":
                ok = False
            prop = strict[1]
            if prop != prop.strip() or len(prop) < (K_MIN if kind == "K" else H_MIN):
                ok = False
            if prop_count.get(prop, 0) != 1:
                ok = False
        row_ok[rid] = ok
        # quote
        pl = pin_line(pin, line)
        qok = pl is not None and quote.encode("utf-8") in pl
        carried = None
        if best is not None:
            q = best[4]
            carried = q[1:-1] if len(q) >= 2 and q[0] == "`" and q[-1] == "`" else ""
            if pl is None or carried.encode("utf-8") not in pl or carried == "":
                qok = False
        quote_ok[rid] = qok
        if kind == "H":
            hok = best is not None and carried is not None and carried != "" and pl is not None \
                and carried.encode("utf-8") in pl
            host_ok[rid] = hok
        if kind == "K" and entry_present:
            sid = best[2] if best is not None else None
            sok = sid is not None and sid == r["sid"] and source_cell_ok(sid, pin)
            src_ok[rid] = sok
            scope_flag[rid] = sid is not None and scope_ok(sid, pin, line)
        if entry_present:
            if best is not None:
                t, n, ec = content_ok(rid, best[1], quote, line, pin)
            else:
                t, n, ec = False, False, False
            tok_ok[rid], num_ok[rid], echo_ok[rid] = t, n, ec

    if entry_present:
        for r in c1["k"] + c1["h"]:
            if not row_ok[r["id"]]:
                leg_row.append("row:" + r["id"])
    for r in c1["k"] + c1["h"]:
        if not quote_ok[r["id"]]:
            leg_quote.append("quote:" + r["id"])
    missed.extend(leg_row)
    missed.extend(leg_quote)

    # pin_hash
    pin_bad = False
    for pin, want in pins_all.items():
        d = repo.blob(PIN_DIR + "/" + pin)
        if d is None or hashlib.sha256(d).hexdigest() != want:
            pin_bad = True
    if pin_bad:
        missed.append("pin_hash")

    if entry_present:
        for r in c1["h"]:
            if not host_ok[r["id"]]:
                missed.append("host:" + r["id"])
        for r in c1["k"]:
            if not src_ok[r["id"]]:
                missed.append("source_cell:" + r["id"])
        for r in c1["k"]:
            if not scope_flag[r["id"]]:
                missed.append("scope:" + r["id"])
        for r in c1["k"] + c1["h"]:
            if not tok_ok[r["id"]]:
                missed.append("tok:" + r["id"])
        for r in c1["k"] + c1["h"]:
            if not num_ok[r["id"]]:
                missed.append("num:" + r["id"])
        for r in c1["k"] + c1["h"]:
            if not echo_ok[r["id"]]:
                missed.append("echo:" + r["id"])

    # new_rows
    m = 0
    for sid in c1["new_row_ids"]:
        pin = c1["rows"].get(sid)
        if pin is not None and source_cell_ok(sid, pin):
            m += 1
    counts["m"] = m
    if m != NEW_ROWS_DENOM or len(c1["new_row_ids"]) != NEW_ROWS_DENOM:
        missed.append("new_rows")

    if entry_present:
        counts["a"] = sum(1 for r in c1["k"] if row_ok[r["id"]] and quote_ok[r["id"]])
        counts["b"] = sum(1 for r in c1["h"] if row_ok[r["id"]] and quote_ok[r["id"]] and host_ok[r["id"]])
        counts["c"] = sum(1 for r in c1["k"] if src_ok[r["id"]])
        counts["d"] = sum(1 for r in c1["k"] if scope_flag[r["id"]])
        counts["e"] = sum(1 for r in c1["k"] + c1["h"] if tok_ok[r["id"]] and num_ok[r["id"]] and echo_ok[r["id"]])
    return finish(repo, missed, counts, entry_present)


def finish(repo, missed, counts, entry_present):
    return counts, missed


def render(rev, counts, missed):
    full = (counts["a"] == 30 and counts["b"] == 3 and counts["c"] == 30 and counts["d"] == 30
            and counts["e"] == 33 and counts["m"] == 8 and not missed)
    verdict = "TARGET_MET" if full else "TARGET_MISSED"
    return ("MADO_AUTORELOAD_ENTRY: rev=%s rows=%d/30 hosts=%d/3 sources=%d/30 scope=%d/30 content=%d/33 "
            "new_rows=%d/8 verdict=%s missed=%s"
            % (rev, counts["a"], counts["b"], counts["c"], counts["d"], counts["e"], counts["m"],
               verdict, ",".join(missed) if missed else "none")), full


def run_counter(repo_path, rev, work):
    repo = Repo(repo_path, work)
    repo.resolve(rev)
    counts, missed = evaluate(repo)
    return render(rev, counts, missed)


# ----------------------------------------------------------------------------- selftest

class Checker:
    def __init__(self):
        self.n = 0
        self.ok = 0

    def check(self, cond, label):
        self.n += 1
        if cond:
            self.ok += 1
        else:
            sys.stderr.write("FAIL: %s\n" % label)


def build_files(src, tables_blob, pins):
    """Witness tree (file dict) generated from the frozen tables: entry, registry, README, tables, pins."""
    c1 = json.loads(tables_blob.decode())["c1"]
    files = {TABLES_PATH: tables_blob}
    for name, blob in pins.items():
        files[PIN_DIR + "/" + name] = blob
    rows = []
    for r in c1["k"] + c1["h"]:
        toks = sorted(set(TOKEN_RE.findall(r["quote"])))
        if not toks:
            raise Setup("selftest: quote of %s has no identifier token" % r["id"])
        kind = "K" if r["id"][0] == "K" else "H"
        prop = "Entry row %s cites a pinned source line that holds the token %s verbatim in its quote" % (r["id"], toks[0])
        rows.append(dict(id=r["id"], prop=prop, src=r["sid"] if kind == "K" else "host",
                         pin="%s:%s" % (r["pin"], r["line"]), quote=r["quote"]))
    entry = {"rows": rows,
             "source": "source: " + " ".join(c1["new_row_ids"]) + " - selftest witness rows",
             "verified": "verified-at: " + OPENED,
             "recheck": "recheck: on-release - selftest witness"}
    files[ENTRY] = render_entry(entry)
    files[REGISTRY_PATH] = render_registry(c1, rows, extra=[])
    files[INDEX_PATH] = ("# corpus\n\n| entry | what |\n|---|---|\n"
                         "| `knowledge/hyprland-config-autoreload-r56.md` (selftest witness) | witness |\n").encode()
    return files, c1, entry


def render_entry(entry):
    out = ["# Hyprland config auto-reload (selftest witness)", "", entry["source"], entry["verified"],
           entry["recheck"], "", "| id | proposition | src | pin:line | quote |", "|---|---|---|---|---|"]
    for r in entry["rows"]:
        out.append("| %s | %s | %s | %s | `%s` |" % (r["id"], r["prop"], r["src"], r["pin"], r["quote"]))
    out.append("")
    return "\n".join(out).encode()


def render_registry(c1, rows, extra):
    anchors = {}
    for r in c1["k"]:
        anchors.setdefault(r["sid"], []).append(r["line"])
    out = ["# SOURCES", "", "## Registry", "",
           "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
           "|---|---|---|---|---|---|---|---|---|---|---|",
           "| S001 | own work - corpus/lessons/round-10.md | own-work | A | scope | corpus/lessons/round-10.md:63-123 | t | mined | 2026-10-19 | 90d | - |"]
    for sid in c1["new_row_ids"]:
        pin = c1["rows"][sid]
        suffix = c1["pin_suffix"][pin]
        base = suffix.rsplit("/", 1)[-1]
        if pin.startswith("man7"):
            url = "https://man7.org/linux/man-pages/" + suffix
        else:
            url = "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/%s" % (c1["commit"], suffix)
        lines = sorted(set(anchors.get(sid, [])))
        loc = ",".join(str(n) for n in lines) if lines else "1"
        if len(lines) > 2:
            loc = "%d-%d,%s" % (lines[0], lines[0], ",".join(str(n) for n in lines[1:]))
        anchor = "Hyprland-%s:%s lines of the pin (receipt %s)" % (base, loc, pin)
        out.append("| %s | selftest %s - %s | code | A | scope | %s | t | mined | %s | 90d | %s |"
                   % (sid, pin, url, anchor, OPENED, ENTRY))
    out.extend(extra)
    out.append("")
    return "\n".join(out).encode()


def make_repo(work, files):
    d = tempfile.mkdtemp(dir=work)
    env = dict(os.environ, HOME=work, TMPDIR=work, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    for k in [k for k in env if k.startswith("GIT_") and k not in ("GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL")]:
        del env[k]

    def g(*a):
        p = subprocess.run(["git", "-C", d] + list(a), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            raise Setup("selftest git %s failed: %s" % (a[0], p.stderr.decode()[:200]))
        return p.stdout.decode().strip()

    g("init", "-q")
    if g("rev-parse", "--show-toplevel") != os.path.realpath(d):
        raise Setup("selftest fixture toplevel mismatch")
    for path, data in files.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if isinstance(data, tuple):  # ("link", target)
            os.symlink(data[1], full)
        else:
            with open(full, "wb") as fh:
                fh.write(data)
    g("add", "-A", "-f")
    g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "fixture")
    return d, g("rev-parse", "HEAD")


def sub_run(argv, work):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "TMPDIR": work, "HOME": work}
    p = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + argv, env=env,
                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def selftest(src_repo, src_rev, work):
    ck = Checker()
    os.makedirs(work, exist_ok=True)
    work = os.path.realpath(work)
    src = Repo(src_repo, work)
    src.resolve(src_rev)
    tables_blob = src.blob(TABLES_PATH)
    if tables_blob is None or hashlib.sha256(tables_blob).hexdigest() != TABLES_SHA256:
        raise Setup("selftest: source rev lacks the frozen tables with the embedded sha256")
    c1 = json.loads(tables_blob.decode())["c1"]
    pins = {}
    for name in list(c1["pin_sha256"]) + list(c1["host_pin_sha256"]):
        b = src.blob(PIN_DIR + "/" + name)
        if b is None:
            raise Setup("selftest: source rev lacks pin " + name)
        pins[name] = b
    files, c1, entry = build_files(src, tables_blob, pins)

    def run(files_, want_rc, label, legs=(), nolegs=(), expect_met=False):
        d, rev = make_repo(work, files_)
        rc, out, err = sub_run(["--repo", d, "--rev", rev, "--work", work], work)
        line = out.rstrip("\n")
        ck.check(out.count("\n") == 1 and line.startswith("MADO_AUTORELOAD_ENTRY: rev=" + rev + " "), label + ": one line")
        ck.check(rc == want_rc, "%s: exit %d want %d (%s)" % (label, rc, want_rc, line[-160:]))
        missed = line.rsplit(" missed=", 1)[-1].split(",") if " missed=" in line else []
        for leg in legs:
            ck.check(leg in missed, "%s: leg %s in %s" % (label, leg, missed))
        for leg in nolegs:
            ck.check(leg not in missed, "%s: leg %s absent" % (label, leg))
        ck.check(("verdict=TARGET_MET" in line) == expect_met, label + ": verdict")
        return d, rev, line

    # --- good tree
    d, rev, line = run(files, 0, "good", expect_met=True)
    want = ("MADO_AUTORELOAD_ENTRY: rev=%s rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 "
            "new_rows=8/8 verdict=TARGET_MET missed=none" % rev)
    ck.check(line == want, "good: exact frozen output line")
    # in-process agrees with the subprocess, and --rev may be a ref name
    r_line, r_full = run_counter(d, "HEAD", work)
    ck.check(r_full and r_line == want.replace("rev=" + rev, "rev=HEAD"), "good: in-process, rev=HEAD")
    # working tree is not read: dirty the worktree, same answer
    with open(os.path.join(d, ENTRY), "ab") as fh:
        fh.write(b"| K01 | junk |\n")
    ck.check(run_counter(d, rev, work)[1], "good: worktree edits ignored")

    def mutate(fn):
        f2 = dict(files)
        e2 = {"rows": [dict(r) for r in entry["rows"]], "source": entry["source"],
              "verified": entry["verified"], "recheck": entry["recheck"]}
        fn(f2, e2)
        if ENTRY in f2 and not isinstance(f2[ENTRY], (bytes, tuple)):
            f2[ENTRY] = render_entry(f2[ENTRY]) if isinstance(f2[ENTRY], dict) else f2[ENTRY]
        return f2, e2

    def row(e, rid):
        return next(r for r in e["rows"] if r["id"] == rid)

    # --- the twelve registered controls (ctl1-10 of registration.md, ctl11-12 of registration-v2 E5)
    f2 = dict(files)
    del f2[ENTRY]
    run(f2, 1, "ctl1 entry-absent", legs=["entry_absent"], nolegs=["prov", "row:K01"])
    d1 = run(f2, 1, "ctl1 counts", legs=["entry_absent"])[2]
    ck.check("rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33" in d1, "ctl1: zero counts")

    def junk(f, e):
        for r in e["rows"]:
            r["prop"] = ("placeholder proposition text for row %s, not a claim about any source line" % r["id"]
                         if r["id"][0] == "K" else "placeholder host proposition %s, not a read" % r["id"])
        f[ENTRY] = render_entry(e)
    f2, e2 = mutate(junk)
    _, _, ln = run(f2, 1, "ctl2 junk-placeholders", legs=["tok:K01"])
    ck.check(any(s.startswith("tok:") for s in ln.split(" missed=")[1].split(",")), "ctl2: tok legs")
    ck.check("content=" in ln and "/33" in ln and "content=33/33" not in ln, "ctl2: e<33")

    def falsenum(f, e):
        row(e, "K04")["prop"] += " The value is capped at 200 by this call."
        f[ENTRY] = render_entry(e)
    run(mutate(falsenum)[0], 1, "ctl3 false-number", legs=["num:K04"], nolegs=["num:K05"])

    def cross(f, e):
        row(e, "K10")["src"] = "S385"
        f[ENTRY] = render_entry(e)
    run(mutate(cross)[0], 1, "ctl4 cross-pin-source", legs=["source_cell:K10"], nolegs=["source_cell:K09"])

    def scopeswap(f, e):
        row(e, "K10")["src"] = "S399"
        f[ENTRY] = render_entry(e)
        reg = files[REGISTRY_PATH].decode()
        url = [l for l in reg.split("\n") if l.startswith("| S383 ")][0].split("|")[2].strip().rsplit(" ", 1)[-1]
        extra = "| S399 | scratch - %s | code | A | scope | ConfigWatcher.cpp:1-10 | t | mined | %s | 90d | %s |\n" % (url, OPENED, ENTRY)
        f[REGISTRY_PATH] = (reg + extra).encode()
    run(mutate(scopeswap)[0], 1, "ctl5 scope-swap", legs=["scope:K10", "source_cell:K10"], nolegs=["scope:K09"])

    def dangling(f, e):
        e["source"] += ", S999"
        f[ENTRY] = render_entry(e)
    run(mutate(dangling)[0], 1, "ctl6 provenance-dangling", legs=["prov"])

    def dropped(f, e):
        e["rows"] = [r for r in e["rows"] if r["id"] != "K17"]
        f[ENTRY] = render_entry(e)
    run(mutate(dropped)[0], 1, "ctl7 dropped-row", legs=["row:K17"], nolegs=["row:K16"])

    def editedq(f, e):
        row(e, "K05")["quote"] = row(e, "K05")["quote"].replace("inotify", "inotifz", 1)
        f[ENTRY] = render_entry(e)
    run(mutate(editedq)[0], 1, "ctl8 edited-quote", legs=["quote:K05", "row:K05"], nolegs=["quote:K04"])

    f2 = dict(files)
    b = bytearray(files[PIN_DIR + "/Hyprland-ConfigWatcher.cpp"])
    b[100] ^= 1
    f2[PIN_DIR + "/Hyprland-ConfigWatcher.cpp"] = bytes(b)
    run(f2, 1, "ctl9 pin-byte", legs=["pin_hash"])

    f2 = dict(files)
    f2[REGISTRY_PATH] = "\n".join(l for l in files[REGISTRY_PATH].decode().split("\n") if not l.startswith("| S390 ")).encode()
    run(f2, 1, "ctl10 new-row-missing", legs=["new_rows", "source_cell:K29", "source_cell:K30"], nolegs=["source_cell:K28"])

    # --- legs beyond the ten controls
    f2 = dict(files)
    b = bytearray(tables_blob)
    b[-2] = ord(" ") if b[-2] != ord(" ") else ord("\n")
    f2[TABLES_PATH] = bytes(b)
    run(f2, 1, "tables-sha", legs=["tables_sha"])
    f2 = dict(files)
    del f2[TABLES_PATH]
    _, _, ln = run(f2, 1, "tables-absent", legs=["tables_sha"])
    ck.check("rows=0/30" in ln, "tables-absent: zero counts")
    f2 = dict(files)
    f2[INDEX_PATH] = b"# corpus\n"
    run(f2, 1, "index-missing", legs=["index"])
    f2[INDEX_PATH] = files[INDEX_PATH] + files[INDEX_PATH].split(b"\n", 4)[4]
    run(f2, 1, "index-duplicate", legs=["index"])

    def noverified(f, e):
        e["verified"] = "verified-at: 2026-10-27"
        f[ENTRY] = render_entry(e)
    run(mutate(noverified)[0], 1, "prov-verified-date", legs=["prov"])

    def order(f, e):
        e["source"], e["verified"] = e["verified"], e["source"]
        f[ENTRY] = render_entry(e)
    run(mutate(order)[0], 1, "prov-order", legs=["prov"])

    def srcmissing(f, e):
        e["source"] = "source: S383 S384 S385 S386 S387 S388 S389 - selftest"
        f[ENTRY] = render_entry(e)
    run(mutate(srcmissing)[0], 1, "prov-source-set", legs=["prov"])

    def trailing(f, e):
        f[ENTRY] = render_entry(e).replace(b"verbatim in its quote |", b"verbatim in its quote |", 1)
        txt = f[ENTRY].decode().split("\n")
        i = [j for j, l in enumerate(txt) if l.startswith("| K02 ")][0]
        txt[i] += " "
        f[ENTRY] = "\n".join(txt).encode()
    run(mutate(trailing)[0], 1, "row-trailing-byte", legs=["row:K02"], nolegs=["row:K03"])

    def shortprop(f, e):
        row(e, "K03")["prop"] = row(e, "K03")["prop"][:20]
        f[ENTRY] = render_entry(e)
    run(mutate(shortprop)[0], 1, "row-short-prop", legs=["row:K03"])

    def dupprop(f, e):
        row(e, "K07")["prop"] = row(e, "K06")["prop"]
        f[ENTRY] = render_entry(e)
    run(mutate(dupprop)[0], 1, "row-duplicate-prop", legs=["row:K06", "row:K07"])

    def duprow(f, e):
        e["rows"].append(dict(row(e, "K08"), prop=row(e, "K08")["prop"] + " again"))
        f[ENTRY] = render_entry(e)
    run(mutate(duprow)[0], 1, "row-duplicated", legs=["row:K08"])

    def fenced(f, e):
        txt = render_entry(e).decode().split("\n")
        i = [j for j, l in enumerate(txt) if l.startswith("| K09 ")][0]
        txt.insert(i + 1, "```")
        txt.insert(i, "```")
        f[ENTRY] = "\n".join(txt).encode()
    run(mutate(fenced)[0], 1, "row-in-fence", legs=["row:K09"], nolegs=["row:K10"])

    def tilde_fence_short_close(f, e):
        txt = render_entry(e).decode().split("\n")
        i = [j for j, l in enumerate(txt) if l.startswith("| K09 ")][0]
        txt.insert(i + 1, "~~~")
        txt.insert(i, "~~~~")  # four tildes open, three do not close: K10.. stay inside
        f[ENTRY] = "\n".join(txt).encode()
    run(mutate(tilde_fence_short_close)[0], 1, "fence-length", legs=["row:K09", "row:K10", "row:H03"])

    def commented(f, e):
        txt = render_entry(e).decode().split("\n")
        i = [j for j, l in enumerate(txt) if l.startswith("| K11 ")][0]
        txt.insert(i + 1, "-->")
        txt.insert(i, "<!--")
        f[ENTRY] = "\n".join(txt).encode()
    run(mutate(commented)[0], 1, "row-in-comment", legs=["row:K11"], nolegs=["row:K12"])

    def fence_inside_comment(f, e):
        txt = render_entry(e).decode().split("\n")
        i = [j for j, l in enumerate(txt) if l.startswith("| K11 ")][0]
        txt.insert(i, "<!--")
        txt.insert(i + 1, "```")
        txt.insert(i + 2, "-->")
        f[ENTRY] = "\n".join(txt).encode()
    # fence marker inside a comment opens nothing, so K11 stays a live row
    run(mutate(fence_inside_comment)[0], 0, "fence-inside-comment", expect_met=True)

    def hostquote(f, e):
        row(e, "H02")["quote"] = row(e, "H02")["quote"] + " x"
        f[ENTRY] = render_entry(e)
    run(mutate(hostquote)[0], 1, "host-quote", legs=["host:H02", "row:H02"], nolegs=["host:H01"])

    def badpin(f, e):
        row(e, "K20")["pin"] = "Hyprland-legacy-ConfigManager.cpp:777"
        f[ENTRY] = render_entry(e)
    run(mutate(badpin)[0], 1, "row-pin-line", legs=["row:K20"])

    def bignum(f, e):
        row(e, "K01")["prop"] += " Source line 493 is also relevant"
        f[ENTRY] = render_entry(e)
    run(mutate(bignum)[0], 1, "num-unknown-line", legs=["num:K01"])

    def oknum(f, e):
        row(e, "K03")["prop"] += " It sits at line 33, next to line 34 and the pair 1 2 3, line 46 too"
        f[ENTRY] = render_entry(e)
    run(mutate(oknum)[0], 0, "num-allowed", expect_met=True)

    def echoq(f, e):
        for r in e["rows"]:
            if len(r["quote"]) >= ECHO_MIN:
                r["prop"] = r["quote"] + " echoed on this line, no analysis added here"
        f[ENTRY] = render_entry(e)
    run(mutate(echoq)[0], 1, "ctl11 quote-echo", legs=["echo:K01"], nolegs=["echo:K08"])

    def toknone(f, e):
        row(e, "K29")["prop"] = "Zzzz qqqq wwww xxxx vvvv bbbb nnnn mmmm kkkk jjjj hhhh gggg"
        f[ENTRY] = render_entry(e)
    run(mutate(toknone)[0], 1, "tok-none", legs=["tok:K29"], nolegs=["tok:K28"])

    # registry legs
    def regmut(fn, label, legs, nolegs=()):
        f2 = dict(files)
        lines = files[REGISTRY_PATH].decode().split("\n")
        lines = fn(lines)
        f2[REGISTRY_PATH] = "\n".join(lines).encode()
        run(f2, 1, label, legs=legs, nolegs=nolegs)

    def edit_row(sid, idx, value):
        def f(lines):
            out = []
            for l in lines:
                if l.startswith("| %s " % sid):
                    cells = l.strip().strip("|").split("|")
                    cells[idx] = " %s " % value
                    l = "|" + "|".join(cells) + "|"
                out.append(l)
            return out
        return f
    regmut(edit_row("S383", 7, "candidate"), "reg-status", ["source_cell:K03", "new_rows"], ["source_cell:K13"])
    regmut(edit_row("S383", 3, "C"), "reg-tier", ["source_cell:K03", "new_rows"])
    regmut(edit_row("S383", 8, "2026-10-26"), "reg-opened", ["source_cell:K03", "new_rows"])
    regmut(edit_row("S383", 10, "corpus/knowledge/other.md"), "reg-usedby", ["source_cell:K03", "new_rows"])
    regmut(edit_row("S383", 1, " x - https://example.com/ConfigWatcher.cpp"), "reg-url", ["source_cell:K03", "new_rows"])
    regmut(edit_row("S383", 5, "ConfigWatcher.cpp:34-100"), "reg-scope-short", ["scope:K03"], ["scope:K04"])
    regmut(edit_row("S383", 5, "ConfigWatcher.cpp:34-200"), "reg-scope-past-eof", ["scope:K03", "scope:K04"])
    regmut(edit_row("S383", 5, "ConfigWatcher.cpp:1-9999"), "ctl12 anchor-past-eof", ["scope:K03", "scope:K04", "scope:K12"])
    regmut(edit_row("S383", 5, "ConfigWatcher.cpp:1-10, 33"), "reg-scope-list-space", ["scope:K04"], ["scope:K03"])
    regmut(lambda ls: ls + [ls[ls.index([l for l in ls if l.startswith("| S384 ")][0])]], "reg-duplicate-row",
           ["source_cell:K01", "new_rows"])
    regmut(lambda ls: [l if not l.startswith("| S384 ") else l + " extra |" for l in ls], "reg-ten-cells-or-twelve",
           ["source_cell:K01", "new_rows"])

    # symlinks: blob and directory
    f2 = dict(files)
    f2[ENTRY] = ("link", "../../README.md")
    run(f2, 1, "entry-symlink-blob", legs=["entry_absent"])
    f2 = {k: v for k, v in files.items() if not k.startswith(PIN_DIR + "/")}
    f2[".ufo/waves/round-56/realfetch/x"] = b"x"
    f2[PIN_DIR] = ("link", "realfetch")
    f2[".ufo/waves/round-56/realfetch/Hyprland-ConfigWatcher.cpp"] = files[PIN_DIR + "/Hyprland-ConfigWatcher.cpp"]
    run(f2, 1, "pin-dir-symlink", legs=["pin_hash", "quote:K03"])

    # setup errors: exit 2, empty stdout, reason on stderr
    for label, argv in [("no-args", []), ("bad-rev", ["--repo", d, "--rev", "no-such-rev", "--work", work]),
                        ("no-work", ["--repo", d, "--rev", rev]), ("unknown-arg", ["--repo", d, "--rev", rev, "--work", work, "--x"]),
                        ("not-a-repo", ["--repo", work, "--rev", "HEAD", "--work", work]),
                        ("dash-rev", ["--repo", d, "--rev", "--all", "--work", work]),
                        ("repeat-repo", ["--repo", d, "--repo", d, "--rev", rev, "--work", work]),
                        ("empty-value", ["--repo", d, "--rev", "", "--work", work])]:
        rc, out, err = sub_run(argv, work)
        ck.check(rc == 2 and out == "" and err.strip() != "", "setup %s: rc=%d stdout=%r" % (label, rc, out[:40]))

    # unit-level scanners
    ck.check(scope_covers("Hyprland-X.cpp:271-279 input kb options, Hyprland-X.cpp:296 x", "X.cpp", 296), "scope: second occurrence")
    ck.check(not scope_covers("Hyprland-X.cpp:271-279 input kb options, Hyprland-X.cpp:296 x", "X.cpp", 280), "scope: line 280 outside")
    ck.check(scope_covers("X.cpp:10,20-30,40", "X.cpp", 25), "scope: comma list range")
    ck.check(scope_covers("X.cpp:10,20-30,40", "X.cpp", 40), "scope: comma list tail")
    ck.check(not scope_covers("X.cpp:10-5", "X.cpp", 7), "scope: reversed range empty")
    ck.check(not scope_covers("X.cpp 10-20", "X.cpp", 15), "scope: no colon")
    ck.check(registry_id("| S383 | x |") == "S383" and registry_id("    | S383 | x") is None
             and registry_id("| S38 | x") is None and registry_id("|S1234| x") == "S1234", "registry_id")
    ck.check(strict_row("| a | b |") == ["a", "b"] and strict_row("| a | b | ") is None and strict_row("|a | b |") is None,
             "strict_row")
    ck.check(first_cell("  | K01 | x") == "K01" and first_cell("K01 | x") is None, "first_cell")
    lv = [i for i, _ in live_lines(["| a |", "```", "| b |", "```", "<!-- x", "| c |", "-->", "| d |"])]
    ck.check(lv == [0, 7], "live_lines fences and comments: %s" % lv)
    return ck


# ----------------------------------------------------------------------------- CLI

def parse_args(argv):
    names = {"--repo", "--rev", "--work"}
    got = {}
    selftest_flag = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--selftest":
            if selftest_flag:
                raise Setup("repeated --selftest")
            selftest_flag = True
            i += 1
        elif a in names:
            if a in got:
                raise Setup("repeated option %s" % a)
            if i + 1 >= len(argv):
                raise Setup("option %s without value" % a)
            got[a] = argv[i + 1]
            i += 2
        else:
            raise Setup("unknown argument: %s" % a)
    if not selftest_flag:
        for n in sorted(names):
            if n not in got:
                raise Setup("missing %s" % n)
        if got["--rev"] == "":
            raise Setup("empty --rev")
    return selftest_flag, got


def main(argv):
    try:
        st, got = parse_args(argv)
        if st:
            cleanup = None
            if "--work" in got:
                work = got["--work"]
            else:
                work = tempfile.mkdtemp(prefix="c1r56-selftest-")
                cleanup = work
            try:
                ck = selftest(got.get("--repo", "."), got.get("--rev", "HEAD"), work)
            finally:
                if cleanup:
                    import shutil
                    shutil.rmtree(cleanup, ignore_errors=True)
            print("%d/%d assertions passed" % (ck.ok, ck.n))
            return 0 if ck.ok == ck.n else 1
        line, full = run_counter(got["--repo"], got["--rev"], got["--work"])
    except Setup as e:
        sys.stderr.write("setup error: %s\n" % e)
        return 2
    except OSError as e:
        sys.stderr.write("setup error: %s\n" % e)
        return 2
    sys.stdout.write(line + "\n")
    return 0 if full else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""c1-r56-autoreload-entry.py -- PRED-C1-r56 counter (mado round 56, claim C1, strict reading).

Draft for `quality/counters/c1-r56-autoreload-entry.py`.  Contract: `.ufo/waves/round-56/registration.md` section C1 and
`.ufo/waves/round-56/claims-frozen.md` (PRED-C1-r56), read as written and never relaxed.

    python3 -I c1-r56-autoreload-entry.py --repo <lane> --rev <rev> --work <scratch>
    python3 -I c1-r56-autoreload-entry.py --selftest --repo <lane> --rev <rev> --work <scratch>

Prints exactly one line (stdout):

    MADO_AUTORELOAD_ENTRY: rev=<rev> rows=<a>/30 hosts=<b>/3 sources=<c>/30 scope=<d>/30 content=<e>/33 new_rows=<m>/8
    verdict=<TARGET_MET|TARGET_MISSED> missed=<legs, comma-separated, or none>        (one physical line)

Exit 0 only on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on stderr, nothing on stdout).  The counter
knows nothing about the harness controls.

Every input byte comes from git objects at --rev of --repo (`git rev-parse`, `git ls-tree`, `git cat-file blob`); the
working tree is never opened.  Only regular blobs (mode 100644/100755) are accepted: a symlink blob (120000) or a path
that crosses a symlinked directory is "absent", never followed.  --work (created when missing) is HOME and TMPDIR of
every git child; the counter itself writes nothing (--selftest writes only under <work>/selftest-<pid>, removed on exit).

Legs, in output order (registration table order; inside a leg the frozen row order K01..K30 then H01..H03):
  entry_absent  tables_sha  prov  index  row:<id>  quote:<id>  pin_hash  host:<id>  source_cell:<id>  scope:<id>
  tok:<id>  num:<id>  new_rows
Every failing leg is listed.  A row that has no well-formed 5-cell line (missing, duplicated, wrong outer shape, wrong
cell count, a pipe or a backslash-escaped pipe inside a cell) reports `row:<id>` only; the legs that read its cells
(quote-cell part, host, source_cell, scope, tok, num) are then not evaluated and the row counts in none of a..e.

Readings taken (the registration is ambiguous; each is listed in the seat report with the other reading):
  R1  quote:<id> fires when the frozen quote is not a substring of line <line> of the pin blob (the text) AND ALSO when
      the row's quote cell is not backtick+frozen quote+backtick (needed so that control 8, "edit one char inside the
      K05 quote cell -> quote:K05", can pass; the literal text of the leg is the first half only).
  R2  prov: the first source: line, the single `verified-at: 2026-10-28` line (exact line) and the first recheck: line
      appear in that order inside the first 30 raw lines; S-ids are read from EVERY source: line in the window.
  R3  source_cell / new_rows: the S-id has exactly ONE row at all in corpus/SOURCES.md (regex ^ {0,3}\\|\\s*S[0-9]{3,}\\s*\\|)
      and that row has exactly 11 cells; any other row with the same id (even malformed) fails it.  The registry is read
      line by line without fence/comment exclusion (the registration states that exclusion for the entry only).
  R4  "used-by names the entry path": the path occurs in the used-by cell not embedded in a longer path/file name.
  R5  scope: the registry row read is the row the K row CITES (cell 3), not the frozen sid; the locator list after
      `<basename>:` is `N|N-M` items joined by `,` (optional spaces after a comma); every occurrence of the basename
      followed by a colon is tried.
  R6  num: "a digit run of the quote" = any maximal run of [0-9]+ in the quote cell (neighbours not considered); the
      line numbers and 0..3 compare as canonical decimals (a run with a leading zero never equals a line number).
  R7  a proposition byte-identical to another PARSED row's proposition fails row: for every row involved.
  R8  entry absent: entry_absent plus the entry-independent legs (tables_sha, index, pin_hash, new_rows).
  R9  frozen-tables.json with a wrong sha256 but a valid shape is still used to evaluate (list-all), tables_sha fires; a
      wrong sha with an invalid shape evaluates nothing table-dependent; a right sha with an invalid shape is rc 2.
  R10 pin_hash covers c1.pin_sha256 AND c1.host_pin_sha256 (host-watched-lstat.txt included).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import fnmatch

TOOL = "c1-r56-autoreload-entry.py"
TABLES_SHA256 = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
TABLES_PATH = ".ufo/waves/round-56/frozen-tables.json"
ENTRY_PATH = "corpus/knowledge/hyprland-config-autoreload-r56.md"
README_PATH = "corpus/README.md"
SOURCES_PATH = "corpus/SOURCES.md"
OPENED = "2026-10-28"
N_K, N_H, N_NEW = 30, 3, 8
REGULAR_MODES = ("100644", "100755")
PROV_WINDOW = 30
ORDER = ("entry_absent", "tables_sha", "prov", "index", "row", "quote", "pin_hash", "host", "source_cell", "scope",
         "tok", "num", "new_rows")

FENCE = re.compile(r"^ {0,3}(```|~~~)")
CAND = re.compile(r"^\s*\|\s*(K(?:0[1-9]|[12][0-9]|30)|H0[1-3])\s*\|")
SID = re.compile(r"S[0-9]{3}")
REG_ID = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
URL = re.compile(r"https?://\S+")
S_IN_LINE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
LOC = re.compile(r"[0-9]+(?:-[0-9]+)?(?:,[ \t]*[0-9]+(?:-[0-9]+)?)*")
REVOK = re.compile(r"[^\s\x00-\x1f\x7f]+")


class SetupError(Exception):
    pass


# --------------------------------------------------------------------------------------------- git access
def git_env(work):
    return {
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


class Repo:
    def __init__(self, repo, rev, work):
        self.repo = repo
        self.work = work
        self.env = git_env(work)
        self._blobs = {}
        if not os.path.isdir(repo):
            raise SetupError("repo is not a directory")
        if not rev or rev.startswith("-") or not REVOK.fullmatch(rev):
            raise SetupError("bad rev")
        r = self.git(["rev-parse", "--verify", "--quiet", "--end-of-options", rev + "^{commit}"])
        if r.returncode != 0:
            raise SetupError("rev does not resolve to a commit at repo")
        self.sha = r.stdout.decode("ascii", "replace").strip()
        if not re.fullmatch(r"[0-9a-f]{40,64}", self.sha):
            raise SetupError("rev resolved to an unexpected object name")
        top = self.git(["rev-parse", "--show-toplevel"])
        if top.returncode == 0 and os.path.realpath(top.stdout.decode("utf-8", "replace").strip()) != os.path.realpath(repo):
            raise SetupError("repo is not the repository root")

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
    """(lineno, line) outside fenced code blocks (``` / ~~~, 0-3 leading spaces) and HTML comments; split on LF only."""
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


def inner_quote(cell):
    return cell[1:-1] if len(cell) >= 2 and cell[0] == "`" and cell[-1] == "`" else cell


# --------------------------------------------------------------------------------------------- tables
def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def valid_shape(d):
    """strict structural validation of frozen-tables.json's c1 block; returns the c1 dict or None."""
    try:
        c = d["c1"]
        if not isinstance(c, dict) or c.get("entry") != ENTRY_PATH:
            return None
        for key in ("commit", "opened", "pin_dir"):
            if not isinstance(c[key], str) or not c[key]:
                return None
        if not re.fullmatch(r"[0-9a-f]{40}", c["commit"]):
            return None
        pd = c["pin_dir"]
        if pd.startswith("/") or "\0" in pd or any(p in ("", ".", "..") for p in pd.split("/")):
            return None
        if not _is_int(c["new_rows_min"]) or c["new_rows_min"] != N_NEW:
            return None
        pins, hpins, suf, rule = c["pin_sha256"], c["host_pin_sha256"], c["pin_suffix"], c["rev_rule"]
        if not all(isinstance(x, dict) and x for x in (pins, hpins, suf, rule)):
            return None
        for group in (pins, hpins):
            for name, h in group.items():
                if not isinstance(name, str) or not name or "/" in name or name in (".", ".."):
                    return None
                if not isinstance(h, str) or not re.fullmatch(r"[0-9a-f]{64}", h):
                    return None
        if set(pins) & set(hpins):
            return None
        for name, s in suf.items():
            if name not in pins or not isinstance(s, str) or not s or s.startswith("/"):
                return None
        for pat, tok in rule.items():
            if not isinstance(pat, str) or not isinstance(tok, str) or not tok:
                return None
        for name in suf:
            if sum(fnmatch.fnmatchcase(name, p) for p in rule) != 1:
                return None
        for kind, ids, n in (("k", "K", N_K), ("h", "H", N_H)):
            rows = c[kind]
            if not isinstance(rows, list) or len(rows) != n:
                return None
            for i, r in enumerate(rows, 1):
                if not isinstance(r, dict) or r.get("id") != "%s%02d" % (ids, i):
                    return None
                allowed = pins if kind == "k" else hpins
                if not isinstance(r.get("pin"), str) or r["pin"] not in allowed:
                    return None
                if not _is_int(r.get("line")) or r["line"] < 1:
                    return None
                q = r.get("quote")
                if not isinstance(q, str) or not q or "`" in q or "\n" in q or "|" in q:
                    return None
                if kind == "k":
                    if r["pin"] not in suf or not isinstance(r.get("sid"), str) or not SID.fullmatch(r["sid"]):
                        return None
        nri, nrows = c["new_row_ids"], c["rows"]
        if not isinstance(nri, list) or len(nri) != N_NEW or len(set(nri)) != N_NEW:
            return None
        if not isinstance(nrows, dict) or set(nrows) != set(nri):
            return None
        for sid, pin in nrows.items():
            if not SID.fullmatch(sid) or pin not in suf:
                return None
        return c
    except (KeyError, TypeError, AttributeError):
        return None


# --------------------------------------------------------------------------------------------- registry
def parse_registry(text):
    """id -> list of cell lists (None when that row does not have exactly 11 pipe cells); every line, no exclusion."""
    reg = {}
    for line in text.split("\n"):
        m = REG_ID.match(line)
        if not m:
            continue
        s = line.strip()
        cells = None
        if len(s) >= 2 and s.startswith("|") and s.endswith("|"):
            cs = [x.strip() for x in s[1:-1].split("|")]
            if len(cs) == 11 and cs[0] == m.group(1):
                cells = cs
        reg.setdefault(m.group(1), []).append(cells)
    return reg


def last_url(cell):
    found = URL.findall(cell)
    return found[-1] if found else ""


def usedby_names(cell, entry):
    pat = r"(?<![A-Za-z0-9_./-])" + re.escape(entry) + r"(?![A-Za-z0-9_-]|\.[A-Za-z0-9_-])"
    return re.search(pat, cell) is not None


def unique_row(reg, sid):
    rows = reg.get(sid or "", [])
    return rows[0] if len(rows) == 1 and rows[0] is not None else None


def rev_token(c, pin):
    for pat, tok in c["rev_rule"].items():
        if fnmatch.fnmatchcase(pin, pat):
            return tok
    return None


def source_cell_ok(cells, pin, c):
    """the registry-row conditions of source_cell (without the frozen-sid equality)."""
    if cells is None:
        return False
    url = last_url(cells[1])
    return (cells[7] == "mined" and cells[3] in ("A", "B") and cells[8] == c["opened"]
            and url.endswith("/" + c["pin_suffix"][pin]) and rev_token(c, pin) in url
            and usedby_names(cells[10], c["entry"]))


def scope_ok(cells, pin, line, c):
    if cells is None:
        return False
    base = c["pin_suffix"][pin].rsplit("/", 1)[-1] + ":"
    anchor = cells[5]
    pos = anchor.find(base)
    while pos != -1:
        m = LOC.match(anchor, pos + len(base))
        if m:
            for part in m.group(0).split(","):
                part = part.strip()
                lo, _, hi = part.partition("-")
                lo, hi = int(lo), int(hi if hi else lo)
                if lo <= line <= hi:
                    return True
        pos = anchor.find(base, pos + 1)
    return False


# --------------------------------------------------------------------------------------------- the check
def split_row(line):
    """5 cells of the exact grammar `| a | b | c | d | e |`, else None."""
    if not (line.startswith("| ") and line.endswith(" |")):
        return None
    if "\\|" in line:
        return None
    cells = line[2:-2].split(" | ")
    if len(cells) != 5 or any("|" in x for x in cells):
        return None
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
        except (ValueError, RecursionError):
            c = None
    if sha_ok and c is None:
        raise SetupError("frozen-tables.json matches the embedded sha256 but its c1 shape is invalid")

    miss = {k: [] for k in ORDER}
    ok_rowq = set()      # K ids whose row and quote hold
    ok_hosts = set()
    ok_src, ok_scope, ok_content = set(), set(), set()
    new_rows = 0

    entry_b = R.blob(lst, ENTRY_PATH)
    if entry_b is None:
        miss["entry_absent"].append("entry_absent")
    if not sha_ok:
        miss["tables_sha"].append("tables_sha")

    sources_b = R.blob(lst, SOURCES_PATH)
    reg = parse_registry(text_of(sources_b)) if sources_b is not None else {}

    # candidate rows of the entry (outside fences and comments)
    cand = {}
    if entry_b is not None:
        for _n, ln in visible_lines(text_of(entry_b)):
            m = CAND.match(ln)
            if m:
                cand.setdefault(m.group(1), []).append(ln)
    parsed = {rid: split_row(lns[0]) for rid, lns in cand.items() if len(lns) == 1}
    parsed = {rid: cells for rid, cells in parsed.items() if cells is not None}

    # prov
    if entry_b is not None:
        head = text_of(entry_b).split("\n")[:PROV_WINDOW]
        si = [i for i, ln in enumerate(head) if ln.startswith("source:")]
        vi = [i for i, ln in enumerate(head) if ln == "verified-at: " + OPENED]
        ri = [i for i, ln in enumerate(head) if ln.startswith("recheck:")]
        ok = bool(si) and len(vi) == 1 and bool(ri) and si[0] < vi[0] < ri[0]
        if ok:
            ids = set()
            for i in si:
                ids.update(S_IN_LINE.findall(head[i]))
            cited = {cells[2] for rid, cells in parsed.items() if rid[0] == "K" and SID.fullmatch(cells[2])}
            ok = all(s in reg for s in ids) and cited <= ids
        if not ok:
            miss["prov"].append("prov")

    # index
    readme_b = R.blob(lst, README_PATH)
    prefix = "| `" + ENTRY_PATH[len("corpus/"):] + "`"
    n_idx = 0 if readme_b is None else sum(1 for ln in text_of(readme_b).split("\n") if ln.startswith(prefix))
    if n_idx != 1:
        miss["index"].append("index")

    if c is not None:
        pin_dir = c["pin_dir"]
        allpins = dict(c["pin_sha256"])
        allpins.update(c["host_pin_sha256"])
        names = sorted(allpins)
        plst = R.ls([pin_dir + "/" + n for n in names])
        pins = {n: R.blob(plst, pin_dir + "/" + n) for n in names}
        if any(pins[n] is None or hashlib.sha256(pins[n]).hexdigest() != allpins[n] for n in names):
            miss["pin_hash"].append("pin_hash")

        new_rows = sum(1 for sid in c["new_row_ids"] if source_cell_ok(unique_row(reg, sid), c["rows"][sid], c))
        if new_rows < N_NEW:
            miss["new_rows"].append("new_rows")

        if entry_b is not None:
            # propositions shared by two parsed rows
            seen = {}
            for rid, cells in parsed.items():
                seen.setdefault(cells[1], []).append(rid)
            for kind, frozen in (("k", c["k"]), ("h", c["h"])):
                for fr in frozen:
                    rid = fr["id"]
                    cells = parsed.get(rid)
                    pl = pin_line(pins.get(fr["pin"]), fr["line"])
                    quote_ok = pl is not None and fr["quote"] in pl
                    row_ok = False
                    if cells is not None:
                        prop = cells[1]
                        row_ok = (cells[0] == rid and prop == prop.strip() and len(prop) >= (40 if kind == "k" else 20)
                                  and len(seen[prop]) == 1 and cells[3] == "%s:%d" % (fr["pin"], fr["line"])
                                  and cells[4] == "`" + fr["quote"] + "`"
                                  and (SID.fullmatch(cells[2]) is not None if kind == "k" else cells[2] == "host"))
                        quote_ok = quote_ok and cells[4] == "`" + fr["quote"] + "`"
                    if not row_ok:
                        miss["row"].append("row:" + rid)
                    if not quote_ok:
                        miss["quote"].append("quote:" + rid)
                    if cells is None:
                        continue
                    rq = inner_quote(cells[4])
                    host_ok = True
                    if kind == "h":
                        host_ok = pl is not None and rq in pl
                        if not host_ok:
                            miss["host"].append("host:" + rid)
                    src_ok = scp_ok = True
                    if kind == "k":
                        crow = unique_row(reg, cells[2] if SID.fullmatch(cells[2]) else None)
                        src_ok = crow is not None and cells[2] == fr["sid"] and source_cell_ok(crow, fr["pin"], c)
                        if not src_ok:
                            miss["source_cell"].append("source_cell:" + rid)
                        scp_ok = scope_ok(crow, fr["pin"], fr["line"], c)
                        if not scp_ok:
                            miss["scope"].append("scope:" + rid)
                    prop = cells[1]
                    tok_ok = bool(set(TOK.findall(prop)) & set(TOK.findall(rq)))
                    if not tok_ok:
                        miss["tok"].append("tok:" + rid)
                    allowed = {str(v) for v in (0, 1, 2, 3, fr["line"])}
                    allowed.update(str(r["line"]) for r in c["k"] + c["h"] if r["pin"] == fr["pin"])
                    allowed.update(re.findall(r"[0-9]+", rq))
                    num_ok = all(n in allowed for n in NUM.findall(prop))
                    if not num_ok:
                        miss["num"].append("num:" + rid)
                    if kind == "k":
                        if row_ok and quote_ok:
                            ok_rowq.add(rid)
                        if src_ok:
                            ok_src.add(rid)
                        if scp_ok:
                            ok_scope.add(rid)
                    elif row_ok and quote_ok and host_ok:
                        ok_hosts.add(rid)
                    if tok_ok and num_ok:
                        ok_content.add(rid)

    legs = [x for k in ORDER for x in miss[k]]
    verdict = "TARGET_MET" if not legs else "TARGET_MISSED"
    line = ("MADO_AUTORELOAD_ENTRY: rev=%s rows=%d/%d hosts=%d/%d sources=%d/%d scope=%d/%d content=%d/%d "
            "new_rows=%d/%d verdict=%s missed=%s"
            % (rev, len(ok_rowq), N_K, len(ok_hosts), N_H, len(ok_src), N_K, len(ok_scope), N_K,
               len(ok_content), N_K + N_H, new_rows, N_NEW, verdict, ",".join(legs) if legs else "none"))
    return line, (0 if verdict == "TARGET_MET" else 1)


# --------------------------------------------------------------------------------------------- selftest
def url_of(c, sid):
    pin = c["rows"][sid]
    suf = c["pin_suffix"][pin]
    if pin.startswith("Hyprland-"):
        return "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/%s" % (c["commit"], suf)
    return "https://man7.org/linux/man-pages/" + suf


def anchor_of(c, sid):
    pin = c["rows"][sid]
    lines = sorted({r["line"] for r in c["k"] if r["sid"] == sid})
    return "%s:%s synthetic locators" % (pin, ",".join(str(x) for x in lines))


def reg_row(c, sid, **kw):
    cells = {"source": "synthetic row title - " + url_of(c, sid), "tier": "A", "anchor": anchor_of(c, sid),
             "status": "mined", "opened": c["opened"], "used": c["entry"]}
    cells.update(kw)
    return "| %s | %s | code | %s | scope | %s | teaches | %s | %s | on-release | %s |" % (
        sid, cells["source"], cells["tier"], cells["anchor"], cells["status"], cells["opened"], cells["used"])


def syn_registry(c, **over):
    rows = ["# SOURCES (synthetic)", "", "## Registry", "",
            "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            "| S001 | filler - https://example.invalid/a | code | A | s | a | t | mined | 2026-10-19 | 90d | corpus/knowledge/x.md |"]
    for sid in c["new_row_ids"]:
        rows.append(reg_row(c, sid, **over.get(sid, {})))
    return "\n".join(rows) + "\n"


def witness_prop(rid, quote):
    tok = TOK.findall(quote)[0]
    if rid[0] == "K":
        return "Synthetic witness proposition for %s built on the identifier %s of the quoted line" % (rid, tok)
    return "Synthetic host witness %s uses %s" % (rid, tok)


def syn_entry(c):
    srcs = ", ".join(c["new_row_ids"])
    out = ["source: %s (rows opened 2026-10-28), pins under .ufo/waves/round-56/fetch/" % srcs,
           "verified-at: 2026-10-28", "recheck: on-release", "", "# Synthetic autoreload entry (selftest only)", "",
           "| id | proposition | source | pin:line | quote |", "|---|---|---|---|---|"]
    for fr in c["k"]:
        out.append("| %s | %s | %s | %s:%d | `%s` |" % (fr["id"], witness_prop(fr["id"], fr["quote"]), fr["sid"],
                                                        fr["pin"], fr["line"], fr["quote"]))
    out += ["", "| id | proposition | source | pin:line | quote |", "|---|---|---|---|---|"]
    for fr in c["h"]:
        out.append("| %s | %s | host | %s:%d | `%s` |" % (fr["id"], witness_prop(fr["id"], fr["quote"]), fr["pin"],
                                                          fr["line"], fr["quote"]))
    return "\n".join(out) + "\n"


def syn_readme(c):
    return ("# README (synthetic)\n\n| path | what |\n|---|---|\n| `knowledge/other.md` (x) | y |\n"
            "| `%s` (MADO-R56-1) | synthetic index row |\n" % c["entry"][len("corpus/"):])


def row_of(files, rid):
    for ln in text_of(files[ENTRY_PATH]).split("\n"):
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


def build_repo(base, name, files, exec_paths=()):
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
    if os.path.realpath(g("rev-parse", "--show-toplevel")) != os.path.realpath(D):
        raise RuntimeError("toplevel != fixture dir")
    for path, val in files.items():
        full = os.path.join(D, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if isinstance(val, tuple):
            os.symlink(val[1], full)
        else:
            with open(full, "wb") as fh:
                fh.write(val)
            if path in exec_paths:
                os.chmod(full, 0o755)
    g("add", "-A")
    g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "synthetic")
    return D


def run_counter(script, repo, rev, work, extra=(), args=None):
    os.makedirs(work, exist_ok=True)
    argv = args if args is not None else ["--repo", repo, "--rev", rev, "--work", work] + list(extra)
    r = subprocess.run([sys.executable, "-I", script] + argv, capture_output=True,
                       env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "TMPDIR": work}, timeout=600)
    return r.returncode, r.stdout.decode(), r.stderr.decode()


LINE_RE = re.compile(r"MADO_AUTORELOAD_ENTRY: rev=(\S+) rows=(\d+)/30 hosts=(\d+)/3 sources=(\d+)/30 scope=(\d+)/30 "
                     r"content=(\d+)/33 new_rows=(\d+)/8 verdict=(TARGET_MET|TARGET_MISSED) missed=(\S+)\n")


def selftest(repo, rev, work):
    R = Repo(repo, rev, work)
    lst = R.ls([TABLES_PATH])
    tb = R.blob(lst, TABLES_PATH)
    if tb is None or hashlib.sha256(tb).hexdigest() != TABLES_SHA256:
        raise SetupError("selftest needs frozen-tables.json at --rev matching the embedded sha256")
    c = valid_shape(json.loads(text_of(tb)))
    if c is None:
        raise SetupError("selftest: frozen-tables.json shape invalid")
    names = sorted(list(c["pin_sha256"]) + list(c["host_pin_sha256"]))
    plst = R.ls([c["pin_dir"] + "/" + n for n in names])
    allpins = dict(c["pin_sha256"])
    allpins.update(c["host_pin_sha256"])
    pin_bytes = {}
    for n in names:
        b = R.blob(plst, c["pin_dir"] + "/" + n)
        if b is None or hashlib.sha256(b).hexdigest() != allpins[n]:
            raise SetupError("selftest: pin %s missing or wrong hash at --rev" % n)
        pin_bytes[n] = b

    base = os.path.join(work, "selftest-%d" % os.getpid())
    os.makedirs(base, exist_ok=True)
    script = os.path.abspath(__file__)
    kids = [r["id"] for r in c["k"]]
    hids = [r["id"] for r in c["h"]]
    pd = c["pin_dir"]
    results = []
    GOOD = ("MADO_AUTORELOAD_ENTRY: rev=HEAD rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 "
            "new_rows=8/8 verdict=TARGET_MET missed=none")

    def check_line(name, rc, out, err, expected, contains, counts, want_rc):
        m = LINE_RE.fullmatch(out)
        got = m.group(9) if m else None
        if expected is not None:
            want = ",".join(expected) if expected else "none"
            ok = m is not None and got == want
        else:
            want = "contains " + ",".join(contains)
            ok = m is not None and m.group(8) == "TARGET_MISSED" and all(x in got.split(",") for x in contains)
        if want_rc is None:
            want_rc = 0 if (expected is not None and not expected) else 1
        ok = ok and rc == want_rc and err == ""
        if ok and counts:
            ok = all(("%s=%s" % (k, v)) in out for k, v in counts.items())
        results.append((name, ok, want, got if m else "UNPARSABLE rc=%s out=%r err=%r" % (rc, out[:160], err[:120])))

    def case(name, mutate, expected=None, contains=(), counts=None, want_rc=None, rev_arg="HEAD", exec_paths=()):
        files = good_files(tb, pin_bytes, c)
        mutate(files)
        D = build_repo(base, "c", files, exec_paths)
        rc, out, err = run_counter(script, D, rev_arg, os.path.join(base, "w"))
        check_line(name, rc, out, err, expected, contains, counts, want_rc)
        shutil.rmtree(D, ignore_errors=True)

    def setrow_prop(rid, new):
        def m(f):
            r = row_of(f, rid)
            cells = r[2:-2].split(" | ")
            cells[1] = new
            edit(f, ENTRY_PATH, r, "| " + " | ".join(cells) + " |")
        return m

    def row_line(rid, fn):
        def m(f):
            r = row_of(f, rid)
            edit(f, ENTRY_PATH, r + "\n", fn(r) + "\n")
        return m

    def reg_edit(sid, **kw):
        def m(f):
            f[SOURCES_PATH] = syn_registry(c, **{sid: kw}).encode()
        return m

    def edit_reg_line(sid, fn):
        def m(f):
            t = text_of(f[SOURCES_PATH]).split("\n")
            i = [k for k, ln in enumerate(t) if ln.startswith("| %s |" % sid)][0]
            t[i] = fn(t[i])
            f[SOURCES_PATH] = "\n".join(t).encode()
        return m

    # ---- positive and counts
    case("good-tree-exact-line", lambda f: None, [], counts=None)
    D = build_repo(base, "g", good_files(tb, pin_bytes, c))
    rc, out, err = run_counter(script, D, "HEAD", os.path.join(base, "w"))
    results.append(("good-tree-frozen-output-line", rc == 0 and out == GOOD + "\n" and err == "", GOOD, out.strip()))
    sha = subprocess.run(["git", "-C", D, "rev-parse", "HEAD"], capture_output=True, env=git_env(base)).stdout.decode().strip()
    rc, out, err = run_counter(script, D, sha, os.path.join(base, "w"))
    results.append(("rev-echoed-as-given-full-sha", rc == 0 and out == GOOD.replace("rev=HEAD", "rev=" + sha) + "\n",
                    "rev=<sha>", out.strip()[:70]))
    o1 = run_counter(script, D, "HEAD", os.path.join(base, "w"))[1]
    o2 = run_counter(script, D, "HEAD", os.path.join(base, "w"))[1]
    results.append(("deterministic-two-runs", o1 == o2 == GOOD + "\n", "identical", "equal" if o1 == o2 else "differs"))
    shutil.rmtree(D, ignore_errors=True)
    case("exec-mode-entry-accepted", lambda f: None, [], exec_paths=(ENTRY_PATH,))

    # ---- the ten frozen controls (registration section C1), mutations as written
    case("CTL1-entry-absent", lambda f: f.pop(ENTRY_PATH), ["entry_absent"],
         counts={"rows": "0/30", "hosts": "0/3", "sources": "0/30", "scope": "0/30", "content": "0/33", "new_rows": "8/8"})

    def junk(f):
        for fr in c["k"]:
            setrow_prop(fr["id"], "placeholder proposition text for row %s, not a claim about any source line" % fr["id"])(f)
        for fr in c["h"]:
            setrow_prop(fr["id"], "placeholder host proposition %s, not a read" % fr["id"])(f)
    case("CTL2-junk-placeholders", junk, contains=["tok:K01", "tok:H01"],
         counts={"rows": "30/30", "hosts": "3/3", "sources": "30/30", "scope": "30/30"})
    # tok must be the only leg and content must fall short
    files = good_files(tb, pin_bytes, c)
    junk(files)
    D = build_repo(base, "j", files)
    rc, out, err = run_counter(script, D, "HEAD", os.path.join(base, "w"))
    m = LINE_RE.fullmatch(out)
    results.append(("CTL2-junk-only-tok-legs-content-short",
                    bool(m) and int(m.group(6)) < 33 and all(x.startswith("tok:") for x in m.group(9).split(",")) and rc == 1,
                    "content<33, only tok:", out.strip()[-120:]))
    shutil.rmtree(D, ignore_errors=True)
    case("CTL3-false-number-K04",
         lambda f: setrow_prop("K04", witness_prop("K04", c["k"][3]["quote"]) + " The value is capped at 200 by this call.")(f),
         ["num:K04"], counts={"content": "32/33", "rows": "30/30"})
    case("CTL4-cross-pin-source-K10", lambda f: edit_row(f, "K10", "| S383 |", "| S385 |"),
         ["source_cell:K10", "scope:K10"], counts={"sources": "29/30", "scope": "29/30", "rows": "30/30"})

    def scope_swap(f):
        f[SOURCES_PATH] = (text_of(f[SOURCES_PATH]) + reg_row(c, "S383", anchor="ConfigWatcher.cpp:1-10").replace(
            "| S383 |", "| S399 |", 1) + "\n").encode()
        edit_row(f, "K10", "| S383 |", "| S399 |")
    case("CTL5-scope-swap-K10", scope_swap, ["prov", "source_cell:K10", "scope:K10"],
         counts={"rows": "30/30", "sources": "29/30", "scope": "29/30"})

    def scope_swap_src(f):
        scope_swap(f)
        edit(f, ENTRY_PATH, "S390 (rows", "S390, S399 (rows")
    case("CTL5b-scope-swap-with-source-line-extended", scope_swap_src, ["source_cell:K10", "scope:K10"])
    case("CTL6-provenance-dangling", lambda f: edit(f, ENTRY_PATH, "S390 (rows", "S390, S999 (rows"), ["prov"])
    case("CTL7-dropped-row-K17", lambda f: edit(f, ENTRY_PATH, row_of(f, "K17") + "\n", ""), ["row:K17"],
         counts={"rows": "29/30", "sources": "29/30", "scope": "29/30", "content": "32/33"})
    case("CTL8-edited-quote-K05", lambda f: edit_row(f, "K05", "watch.wd);`", "watch.wx);`"),
         ["row:K05", "quote:K05"], counts={"rows": "29/30"})

    def pin_byte(f):
        n = pd + "/Hyprland-ConfigWatcher.cpp"
        f[n] = b"X" + f[n][1:]
    case("CTL9-pin-byte-line1", pin_byte, ["pin_hash"])

    def pin_byte_quoted(f):
        n = pd + "/Hyprland-ConfigWatcher.cpp"
        ls = f[n].split(b"\n")
        ls[45] = ls[45].replace(b"inotify_rm_watch", b"Xnotify_rm_watch", 1)
        f[n] = b"\n".join(ls)
    case("pin-byte-inside-K05-quote-line", pin_byte_quoted, ["quote:K05", "pin_hash"], counts={"rows": "29/30"})

    def host_pin_byte(f):
        n = pd + "/host-watched-lstat.txt"
        f[n] = f[n] + b" "
    case("pin-byte-host-watched-lstat", host_pin_byte, ["pin_hash"])
    case("CTL10-new-row-missing-S390",
         lambda f: edit(f, SOURCES_PATH, reg_row(c, "S390") + "\n", ""),
         ["prov", "source_cell:K29", "source_cell:K30", "scope:K29", "scope:K30", "new_rows"],
         counts={"new_rows": "7/8", "sources": "28/30"})

    # ---- tables_sha
    case("tables-trailing-newline", lambda f: f.__setitem__(TABLES_PATH, f[TABLES_PATH] + b"\n"), ["tables_sha"])
    case("tables-absent", lambda f: f.pop(TABLES_PATH), ["tables_sha"],
         counts={"rows": "0/30", "new_rows": "0/8"})
    case("tables-bad-shape-wrong-sha", lambda f: f.__setitem__(TABLES_PATH, b'{"c1": {"k": []}}'), ["tables_sha"],
         counts={"rows": "0/30"})
    case("tables-symlink", lambda f: f.__setitem__(TABLES_PATH, ("link", "../../../README.md")), ["tables_sha"],
         counts={"rows": "0/30"})

    # ---- prov
    case("prov-no-recheck", lambda f: edit(f, ENTRY_PATH, "recheck: on-release\n", ""), ["prov"])
    case("prov-no-source-line", lambda f: edit(f, ENTRY_PATH, "source:", "sources:"), ["prov"])
    case("prov-wrong-date", lambda f: edit(f, ENTRY_PATH, "verified-at: 2026-10-28", "verified-at: 2026-10-27"), ["prov"])
    case("prov-verified-at-with-trailing-text",
         lambda f: edit(f, ENTRY_PATH, "verified-at: 2026-10-28", "verified-at: 2026-10-28 x"), ["prov"])
    case("prov-order-recheck-before-verified",
         lambda f: edit(f, ENTRY_PATH, "verified-at: 2026-10-28\nrecheck: on-release\n", "recheck: on-release\nverified-at: 2026-10-28\n"),
         ["prov"])
    case("prov-order-verified-before-source",
         lambda f: edit(f, ENTRY_PATH, text_of(f[ENTRY_PATH]).split("\n")[0] + "\nverified-at: 2026-10-28\n",
                        "verified-at: 2026-10-28\n" + text_of(f[ENTRY_PATH]).split("\n")[0] + "\n"), ["prov"])
    case("prov-two-verified-at-lines",
         lambda f: edit(f, ENTRY_PATH, "recheck: on-release\n", "verified-at: 2026-10-28\nrecheck: on-release\n"), ["prov"])
    case("prov-source-misses-a-cited-id-S384",
         lambda f: edit(f, ENTRY_PATH, "S383, S384, S385", "S383, S385"), ["prov"])
    case("prov-source-id-not-a-registry-row",
         lambda f: edit(f, ENTRY_PATH, "S390 (rows", "S390, S398 (rows"), ["prov"])
    case("prov-source-extra-id-registry-row-ok",
         lambda f: edit(f, ENTRY_PATH, "S390 (rows", "S390, S001 (rows"), [])

    def prov_late(f):
        t = text_of(f[ENTRY_PATH]).split("\n")
        hdr = t[:3]
        rest = t[3:]
        f[ENTRY_PATH] = "\n".join(["# title"] + [""] * 29 + hdr + rest).encode()
    case("prov-header-after-line-30", prov_late, ["prov"])

    def prov_at_30(f):
        t = text_of(f[ENTRY_PATH]).split("\n")
        hdr = t[:3]
        rest = t[3:]
        f[ENTRY_PATH] = "\n".join([""] * 27 + hdr + rest).encode()
    case("prov-header-ends-at-line-30-ok", prov_at_30, [])

    # ---- index
    case("index-row-missing", lambda f: edit(f, README_PATH, "| `knowledge/hyprland-config-autoreload-r56.md`", "| `knowledge/zz.md`"), ["index"])
    case("index-row-duplicated",
         lambda f: edit(f, README_PATH, "\n", "\n| `knowledge/hyprland-config-autoreload-r56.md` dup | z |\n", 1), ["index"])
    case("index-row-without-space-after-pipe",
         lambda f: edit(f, README_PATH, "| `knowledge/hyprland-config-autoreload-r56.md`", "|`knowledge/hyprland-config-autoreload-r56.md`"),
         ["index"])
    case("index-readme-absent", lambda f: f.pop(README_PATH), ["index"])

    # ---- row grammar
    case("row-trailing-spaces-K09", row_line("K09", lambda r: r + "   "), ["row:K09"], counts={"rows": "29/30"})
    case("row-trailing-tab-H01", row_line("H01", lambda r: r + "\t"), ["row:H01"], counts={"hosts": "2/3"})
    case("row-crlf-K05", row_line("K05", lambda r: r + "\r"), ["row:K05"])
    case("row-double-space-before-pipe-K07", row_line("K07", lambda r: r.replace(" | S383", "  | S383", 1)), ["row:K07"])
    case("row-no-space-after-leading-pipe-K07", row_line("K07", lambda r: "|" + r[1:].lstrip()), ["row:K07"])
    case("row-id-spacing-K07", row_line("K07", lambda r: r.replace("| K07 |", "|K07 |", 1)), ["row:K07"])
    case("row-leading-space-K07", row_line("K07", lambda r: " " + r), ["row:K07"])
    case("row-extra-cell-K06", row_line("K06", lambda r: r[:-2] + "| extra |"), ["row:K06"])
    case("row-four-cells-K06", row_line("K06", lambda r: "| " + " | ".join(r[2:-2].split(" | ")[:4]) + " |"), ["row:K06"])
    case("row-pipe-in-proposition-K06",
         lambda f: setrow_prop("K06", "Synthetic | proposition for K06 with a pipe inside the cell body")(f), ["row:K06"])
    case("row-pipe-without-spaces-in-proposition-K06",
         lambda f: setrow_prop("K06", "Synthetic|proposition for K06 with a pipe inside the cell body")(f), ["row:K06"])
    case("row-escaped-pipe-in-proposition-K06",
         lambda f: setrow_prop("K06", "Synthetic \\| proposition for K06 with an escaped pipe inside")(f), ["row:K06"])
    pad = lambda prefix, n: (prefix + "y" * n)[:n]
    case("row-prop-40-chars-ok-K02", lambda f: setrow_prop("K02", pad("REFRESH_CONFIG_WATCHER ", 40))(f), [])
    case("row-prop-39-chars-K02", lambda f: setrow_prop("K02", pad("REFRESH_CONFIG_WATCHER ", 39))(f), ["row:K02"])
    case("row-prop-20-chars-host-ok-H03", lambda f: setrow_prop("H03", pad("commit ", 20))(f), [], counts={"hosts": "3/3"})
    case("row-prop-19-chars-host-H03", lambda f: setrow_prop("H03", pad("commit ", 19))(f), ["row:H03"])
    case("row-prop-leading-space-K02",
         lambda f: setrow_prop("K02", " " + witness_prop("K02", c["k"][1]["quote"]))(f), ["row:K02"])
    case("row-prop-trailing-space-K02",
         lambda f: setrow_prop("K02", witness_prop("K02", c["k"][1]["quote"]) + " ")(f), ["row:K02"])
    case("row-prop-identical-to-another-row-K02-K03",
         lambda f: setrow_prop("K03", witness_prop("K02", c["k"][1]["quote"]))(f), ["row:K02", "row:K03", "tok:K03"])
    case("row-src-K-short-S38-K02", lambda f: edit_row(f, "K02", "| S384 |", "| S38 |"), ["row:K02", "source_cell:K02", "scope:K02"])
    case("row-src-K-four-digits-S3840-K02", lambda f: edit_row(f, "K02", "| S384 |", "| S3840 |"),
         ["row:K02", "source_cell:K02", "scope:K02"])
    case("row-src-K-host-K02", lambda f: edit_row(f, "K02", "| S384 |", "| host |"), ["row:K02", "source_cell:K02", "scope:K02"])
    case("row-src-H-S383-H02", lambda f: edit_row(f, "H02", "| host |", "| S383 |"), ["row:H02"])
    case("row-pin-cell-wrong-file-K08", lambda f: edit_row(f, "K08", "Hyprland-ConfigWatcher.cpp:56", "Hyprland-ConfigValues.cpp:56"), ["row:K08"])
    case("row-pin-cell-shifted-line-K01", lambda f: edit_row(f, "K01", ":492 |", ":491 |"), ["row:K01"])
    case("row-pin-cell-zero-padded-line-K03", lambda f: edit_row(f, "K03", ":33 |", ":033 |"), ["row:K03"])
    # (double-backtick quote cell case follows)
    case("row-quote-double-backtick-K05",
         row_line("K05", lambda r: r.replace("| `inotify", "| ``inotify", 1).replace("wd);` |", "wd);`` |", 1)),
         ["row:K05", "quote:K05"])
    case("row-quote-no-backticks-H01",
         row_line("H01", lambda r: r.replace("`\"option\"", "\"option\"", 1).replace(": 0` |", ": 0 |", 1)),
         ["row:H01", "quote:H01"], counts={"hosts": "2/3"})
    case("row-quote-tilde-fenced-style-K05",
         row_line("K05", lambda r: r.replace("`inotify", "~inotify", 1).replace("wd);`", "wd);~", 1)),
         ["row:K05", "quote:K05"])
    case("row-quote-trailing-space-inside-ticks-K05",
         row_line("K05", lambda r: r.replace("wd);` |", "wd); ` |", 1)), ["row:K05", "quote:K05"])
    case("row-duplicated-identical-K03", row_line("K03", lambda r: r + "\n" + r), ["row:K03"], counts={"rows": "29/30"})
    case("row-duplicated-different-H02",
         row_line("H02", lambda r: r + "\n" + r.replace("Synthetic host", "Other host")), ["row:H02"])

    def fenced(f):
        r = row_of(f, "K12")
        edit(f, ENTRY_PATH, r + "\n", "```\n" + r + "\n```\n")
    case("row-only-inside-backtick-fence-K12", fenced, ["row:K12"])

    def tilde_fenced(f):
        r = row_of(f, "K12")
        edit(f, ENTRY_PATH, r + "\n", "   ~~~\n" + r + "\n   ~~~\n")
    case("row-only-inside-tilde-fence-3-spaces-K12", tilde_fenced, ["row:K12"])

    def indented_fence(f):
        r = row_of(f, "K12")
        edit(f, ENTRY_PATH, r + "\n", "    ```\n" + r + "\n    ```\n")
    case("fence-marker-with-4-spaces-is-not-a-fence-K12", indented_fence, [])

    def fenced_dup(f):
        r = row_of(f, "K12")
        edit(f, ENTRY_PATH, r + "\n", r + "\n```\n" + r + "\n```\n")
    case("row-copy-inside-fence-ignored-K12", fenced_dup, [])

    def commented(f):
        r = row_of(f, "K13")
        edit(f, ENTRY_PATH, r + "\n", "<!--\n" + r + "\n-->\n")
    case("row-only-inside-html-comment-K13", commented, ["row:K13"])

    def one_line_comment_row(f):
        r = row_of(f, "K13")
        edit(f, ENTRY_PATH, r + "\n", "<!-- " + r + " -->\n")
    case("row-wrapped-in-one-line-comment-K13", one_line_comment_row, ["row:K13"])

    def unterminated_fence(f):
        edit(f, ENTRY_PATH, "\n| id | proposition | source | pin:line | quote |\n|---|---|---|---|---|\n| H01",
             "\n```\n| id | proposition | source | pin:line | quote |\n|---|---|---|---|---|\n| H01")
    case("unterminated-fence-hides-host-rows", unterminated_fence, ["row:H01", "row:H02", "row:H03"],
         counts={"hosts": "0/3"})
    case("host-row-forged-quote-H02",
         row_line("H02", lambda r: r.replace("hyprland.conf`", "hyprland.conq`", 1)),
         ["row:H02", "quote:H02", "host:H02"], counts={"hosts": "2/3"})
    case("host-quote-cell-not-in-pin-line-but-frozen-is-H03",
         row_line("H03", lambda r: r.replace("\"commit\": \"efb5", "\"commit\": \"efb6", 1)),
         ["row:H03", "quote:H03", "host:H03"])

    # ---- source_cell / registry rules
    case("src-status-candidate-S384", reg_edit("S384", status="candidate"),
         [x for x in ["source_cell:K01", "source_cell:K02", "new_rows"]], counts={"sources": "28/30", "new_rows": "7/8"})
    case("src-tier-B-accepted-S384", reg_edit("S384", tier="B"), [])
    case("src-tier-C-S384", reg_edit("S384", tier="C"), ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-opened-wrong-S384", reg_edit("S384", opened="2026-10-27"), ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-usedby-missing-entry-S384", reg_edit("S384", used="corpus/knowledge/other.md"),
         ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-usedby-longer-name-S384", reg_edit("S384", used=ENTRY_PATH + ".bak"),
         ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-usedby-prefix-path-S384", reg_edit("S384", used="x/" + ENTRY_PATH),
         ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-usedby-list-with-other-and-entry-ok-S384", reg_edit("S384", used="corpus/knowledge/other.md, " + ENTRY_PATH + "."), [])
    case("src-url-wrong-commit-S384",
         reg_edit("S384", source="t - https://raw.githubusercontent.com/hyprwm/Hyprland/" + "0" * 40 + "/src/config/values/ConfigValues.cpp"),
         ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-url-wrong-suffix-S384",
         reg_edit("S384", source="t - " + url_of(c, "S384").replace("ConfigValues.cpp", "ConfigValues.hpp")),
         ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-url-suffix-only-as-substring-S384",
         reg_edit("S384", source="t - " + url_of(c, "S384") + "x"), ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-url-last-token-wins-bad-last-S384",
         reg_edit("S384", source="t - " + url_of(c, "S384") + " and https://example.invalid/other"),
         ["source_cell:K01", "source_cell:K02", "new_rows"])
    case("src-url-last-token-wins-good-last-S384",
         reg_edit("S384", source="t - https://example.invalid/other and " + url_of(c, "S384")), [])
    case("src-man7-url-needs-its-host-token-S390",
         reg_edit("S390", source="t - https://example.org/man7/inotify.7.html"),
         ["source_cell:K29", "source_cell:K30", "new_rows"])
    case("src-registry-duplicate-id-S383",
         lambda f: edit(f, SOURCES_PATH, reg_row(c, "S383") + "\n", reg_row(c, "S383") + "\n" + reg_row(c, "S383") + "\n"),
         ["source_cell:" + x for x in kids if c["k"][int(x[1:]) - 1]["sid"] == "S383"] + [
             "scope:" + x for x in kids if c["k"][int(x[1:]) - 1]["sid"] == "S383"] + ["new_rows"])
    case("src-registry-duplicate-malformed-12-cells-S383",
         lambda f: edit(f, SOURCES_PATH, reg_row(c, "S383") + "\n", reg_row(c, "S383") + "\n" + reg_row(c, "S383")[:-2] + "| extra |\n"),
         ["source_cell:" + x for x in kids if c["k"][int(x[1:]) - 1]["sid"] == "S383"] + [
             "scope:" + x for x in kids if c["k"][int(x[1:]) - 1]["sid"] == "S383"] + ["new_rows"])
    case("src-registry-row-10-cells-S384",
         edit_reg_line("S384", lambda ln: ln[:-2].rsplit(" | ", 1)[0] + " |"),
         ["source_cell:K01", "source_cell:K02", "scope:K01", "scope:K02", "new_rows"])
    case("src-registry-row-leading-3-spaces-ok-S384", edit_reg_line("S384", lambda ln: "   " + ln), [])
    case("src-registry-row-leading-4-spaces-absent-S384", edit_reg_line("S384", lambda ln: "    " + ln),
         ["prov", "source_cell:K01", "source_cell:K02", "scope:K01", "scope:K02", "new_rows"])
    case("src-registry-symlink",
         lambda f: f.__setitem__(SOURCES_PATH, ("link", "README.md")),
         contains=["prov", "source_cell:K01", "scope:K01", "new_rows"], counts={"sources": "0/30", "scope": "0/30", "new_rows": "0/8"})
    case("src-registry-absent", lambda f: f.pop(SOURCES_PATH),
         contains=["prov", "source_cell:K01", "scope:K01", "new_rows"], counts={"sources": "0/30", "new_rows": "0/8"})

    # ---- scope
    def anchors(sid, anchor):
        return reg_edit(sid, anchor=anchor)
    k_s384 = ["scope:K01", "scope:K02"]
    case("scope-anchor-basename-missing-S384", anchors("S384", "Hyprland-Other.cpp:492"), k_s384)
    case("scope-anchor-without-colon-S384", anchors("S384", "Hyprland-ConfigValues.cpp 492"), k_s384)
    case("scope-single-locator-equal-ok-S384", anchors("S384", "Hyprland-ConfigValues.cpp:492"), [])
    case("scope-single-locator-off-by-one-S384", anchors("S384", "Hyprland-ConfigValues.cpp:491"), k_s384)
    case("scope-range-low-edge-ok-S384", anchors("S384", "Hyprland-ConfigValues.cpp:492-500"), [])
    case("scope-range-high-edge-ok-S384", anchors("S384", "Hyprland-ConfigValues.cpp:400-492"), [])
    case("scope-range-just-below-S384", anchors("S384", "Hyprland-ConfigValues.cpp:493-500"), k_s384)
    case("scope-range-just-above-S384", anchors("S384", "Hyprland-ConfigValues.cpp:1-491"), k_s384)
    case("scope-reversed-range-S384", anchors("S384", "Hyprland-ConfigValues.cpp:500-400"), k_s384)
    case("scope-comma-list-second-item-S384", anchors("S384", "Hyprland-ConfigValues.cpp:1-10,490-495 text"), [])
    case("scope-comma-space-list-second-item-S384", anchors("S384", "Hyprland-ConfigValues.cpp:1-10, 492 text"), [])
    case("scope-list-stops-at-space-S384", anchors("S384", "Hyprland-ConfigValues.cpp:1-10 492"), k_s384)
    case("scope-second-occurrence-S384", anchors("S384", "Hyprland-ConfigValues.cpp:1-10, Hyprland-ConfigValues.cpp:492 x"), [])
    case("scope-other-file-range-does-not-count-S384",
         anchors("S384", "Hyprland-ConfigValues.cpp:1-10, Hyprland-ConfigWatcher.cpp:490-495"), k_s384)
    case("scope-locator-after-text-not-adjacent-S384", anchors("S384", "Hyprland-ConfigValues.cpp: 492"), k_s384)
    case("scope-man7-basename-S390", anchors("S390", "man7-inotify.7.html:186,262"), [])
    case("scope-man7-basename-missing-line-S390", anchors("S390", "man7-inotify.7.html:186"), ["scope:K30"])
    case("scope-legacy-ConfigManager-substring-basename-S387",
         anchors("S387", "Hyprland-legacy-ConfigManager.cpp:776,1070,1079-1080,1835-1836,1844,1816"), [])

    # ---- tok / num
    case("tok-no-shared-identifier-K02", lambda f: setrow_prop("K02", "Totally unrelated wording about nothing pinned whatsoever here")(f),
         ["tok:K02"], counts={"content": "32/33"})
    case("tok-three-char-token-only-K22", lambda f: setrow_prop("K22", "Totally unrelated wording about std here is only three letters ok")(f),
         ["tok:K22"])
    case("tok-case-sensitive-K02", lambda f: setrow_prop("K02", "Totally unrelated wording with refresh_config_watcher in lowercase here")(f),
         ["tok:K02"])
    case("tok-shared-token-ok-K02",
         lambda f: setrow_prop("K02", "Totally unrelated wording about the Supplementary namespace here ok")(f), [])
    case("tok-shared-4-char-token-K29", lambda f: setrow_prop("K29", "Totally unrelated wording about the man page text: File here ok")(f), [])
    case("num-line-own-ok-K15", lambda f: setrow_prop("K15", "m_propsTripped line 148 test of the own line number here")(f), [])
    case("num-line-other-row-same-pin-ok-K15", lambda f: setrow_prop("K15", "m_propsTripped line 149 test of the next row line here ok")(f), [])
    case("num-line-other-pin-not-ok-K15", lambda f: setrow_prop("K15", "m_propsTripped line 492 test of a foreign pin line number")(f), ["num:K15"])
    case("num-line-off-by-one-K15", lambda f: setrow_prop("K15", "m_propsTripped line 150 test of an unfrozen line number here")(f), ["num:K15"])
    case("num-small-0-3-ok-K15", lambda f: setrow_prop("K15", "m_propsTripped 0 1 2 3 are always allowed small numbers here")(f), [])
    case("num-4-not-ok-K15", lambda f: setrow_prop("K15", "m_propsTripped 4 is not an allowed small number here at all")(f), ["num:K15"])
    case("num-leading-zero-line-not-ok-K15", lambda f: setrow_prop("K15", "m_propsTripped line 0148 zero padded line number test here")(f), ["num:K15"])
    case("num-id-and-pin-digits-embedded-ok-K15",
         lambda f: setrow_prop("K15", "m_propsTripped row K99 in S385 on r56 with x64 and 3ab here ok")(f), [])
    case("num-range-both-ends-K17", lambda f: setrow_prop("K17", "setOnChange lines 1079-1080 both frozen rows of the pin here")(f), [])
    case("num-decimal-version-fails-K15", lambda f: setrow_prop("K15", "m_propsTripped in 0.56.2 version text with a number here")(f), ["num:K15"])
    case("num-quote-digit-run-accepted-H03", lambda f: setrow_prop("H03", "commit 50993780079460 digit run of the quote itself here")(f), [])
    case("num-quote-digit-run-not-in-quote-H03", lambda f: setrow_prop("H03", "commit 50993780079461 digit run absent from the quote here")(f), ["num:H03"])

    # ---- symlinks and mode
    case("symlink-entry-file", lambda f: f.__setitem__(ENTRY_PATH, ("link", "../README.md")), ["entry_absent"],
         counts={"rows": "0/30"})

    def symlink_dir(f):
        ent = f.pop(ENTRY_PATH)
        f["elsewhere/hyprland-config-autoreload-r56.md"] = ent
        f["corpus/knowledge"] = ("link", "../elsewhere")
    case("symlink-directory-above-entry", symlink_dir, ["entry_absent"])
    case("symlink-readme", lambda f: f.__setitem__(README_PATH, ("link", "SOURCES.md")), ["index"])
    case("symlink-pin-file-ConfigWatcher",
         lambda f: f.__setitem__(pd + "/Hyprland-ConfigWatcher.cpp", ("link", "Hyprland-ConfigValues.cpp")),
         contains=["pin_hash", "quote:K03"])

    def symlink_pin_dir(f):
        for n in list(pin_bytes):
            f["fetch-real/" + n] = f.pop(pd + "/" + n)
        f[pd] = ("link", "../../../fetch-real")
    case("symlink-pin-directory", symlink_pin_dir, contains=["pin_hash", "quote:K01", "host:H01", "quote:H03"],
         counts={"rows": "0/30", "hosts": "0/3"})

    # ---- environment and setup errors
    files = good_files(tb, pin_bytes, c)
    D = build_repo(base, "env", files)
    link = os.path.join(base, "repo-link")
    os.symlink(D, link)
    rc, out, err = run_counter(script, link, "HEAD", os.path.join(base, "w"))
    results.append(("repo-path-is-a-symlink", rc == 0 and out == GOOD + "\n", "TARGET_MET", "rc=%s %s" % (rc, out.strip()[-50:])))
    os.remove(os.path.join(D, ENTRY_PATH))
    with open(os.path.join(D, README_PATH), "w") as fh:
        fh.write("garbage\n")
    with open(os.path.join(D, TABLES_PATH), "w") as fh:
        fh.write("{}\n")
    rc, out, err = run_counter(script, D, "HEAD", os.path.join(base, "w"))
    results.append(("dirty-working-tree-ignored", rc == 0 and out == GOOD + "\n", "TARGET_MET", "rc=%s %s" % (rc, out.strip()[-50:])))
    # a subdirectory of the repo is not the repository root
    rc, out, err = run_counter(script, os.path.join(D, "corpus"), "HEAD", os.path.join(base, "w"))
    results.append(("setup-repo-subdirectory-rc2", rc == 2 and out == "" and err != "", "rc=2 stdout empty", "rc=%s out=%r" % (rc, out)))
    for name, args in (("setup-bad-rev", ["--repo", D, "--rev", "no-such-rev", "--work", os.path.join(base, "w")]),
                       ("setup-rev-with-space", ["--repo", D, "--rev", "HEAD x", "--work", os.path.join(base, "w")]),
                       ("setup-rev-leading-dash", ["--repo", D, "--rev", "-HEAD", "--work", os.path.join(base, "w")]),
                       ("setup-bad-repo", ["--repo", os.path.join(base, "nonexistent"), "--rev", "HEAD", "--work", os.path.join(base, "w")]),
                       ("setup-missing-work", ["--repo", D, "--rev", "HEAD"]),
                       ("setup-missing-repo", ["--rev", "HEAD", "--work", os.path.join(base, "w")]),
                       ("setup-unknown-argument", ["--repo", D, "--rev", "HEAD", "--work", os.path.join(base, "w"), "--x"]),
                       ("setup-help-is-not-an-option", ["--help"])):
        rc, out, err = run_counter(script, D, "HEAD", os.path.join(base, "w"), args=args)
        results.append((name, rc == 2 and out == "" and err != "", "rc=2 stdout empty stderr non-empty", "rc=%s out=%r" % (rc, out)))
    empty = build_repo(base, "empty", {"README.txt": b"x\n"})
    rc, out, err = run_counter(script, empty, "HEAD", os.path.join(base, "w"))
    m = LINE_RE.fullmatch(out)
    results.append(("tree-without-any-r56-file",
                    rc == 1 and bool(m) and m.group(9) == "entry_absent,tables_sha,index" and m.group(2) == "0",
                    "entry_absent,tables_sha,index rc=1", "rc=%s %s" % (rc, out.strip()[-70:])))
    work_probe = os.path.join(base, "w-created-on-demand")
    rc, out, err = run_counter(script, D, "HEAD", work_probe)
    results.append(("work-dir-created-when-missing", rc == 0 and os.path.isdir(work_probe), "dir created", "rc=%s" % rc))
    shutil.rmtree(D, ignore_errors=True)
    shutil.rmtree(empty, ignore_errors=True)

    shutil.rmtree(base, ignore_errors=True)
    n_ok = 0
    for name, ok, want, got in results:
        n_ok += bool(ok)
        if not ok:
            print("FAIL %-52s expected=%s got=%s" % (name, want, got))
    print("MADO_R56_C1_SELFTEST: %d/%d assertions passed" % (n_ok, len(results)))
    return 0 if n_ok == len(results) else 1


# --------------------------------------------------------------------------------------------- cli
def main(argv):
    ap = argparse.ArgumentParser(prog=TOOL, add_help=False, allow_abbrev=False)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)  # argparse exits 2 on usage errors with the reason on stderr, stdout stays empty
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
    except Exception as exc:  # an internal failure is a setup error, never a verdict
        sys.stderr.write("%s: setup error: internal %s\n" % (TOOL, exc.__class__.__name__))
        return 2
    sys.stdout.write(line + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""c3-r56-used-by.py -- PRED-C3-r56 counter (mado round 56, claim C3, calibration).

Draft for `quality/counters/c3-r56-used-by.py`.  Contract: `.ufo/waves/round-56/registration.md` section C3 and
`.ufo/waves/round-56/claims-frozen.md` (PRED-C3-r56), read as written, most literal reading wins.

    python3 -I c3-r56-used-by.py --repo <lane> --rev <rev> --work <scratch> [--detail]
    python3 -I c3-r56-used-by.py --selftest [--repo <lane> --rev <rev>] --work <scratch>

Prints exactly one line (stdout):

    MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=<m> extra=<x> dangling=<d> verdict=<TARGET_MET|TARGET_MISSED> missed=<legs,comma>|none

Exit 0 only on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on stderr, nothing on stdout).
`--detail` (optional) lists every offending pair on stderr; stdout never changes.

Every input byte comes from git objects at --rev of --repo (`git rev-parse`, `git ls-tree`, `git cat-file blob`); the
working tree is never opened.  Only regular blobs (mode 100644/100755) count: a symlink blob or a path that crosses a
symlinked directory is "absent".  --work is created when missing and is the HOME/TMPDIR of every git child; the
counter itself writes nothing (selftest writes only under <work>/selftest-*, removed on exit).  The git child
environment is rebuilt from scratch (no inherited GIT_*).

Legs, in output order of `missed`:  missing  extra  dangling  tables_sha
  missing  = #{(S, entry): S row id, S in CITE(entry), entry path not in USEDBY(S)}
  extra    = #{(S, path):  path in USEDBY(S), and (path not in ENTRIES or S not in CITE(path))}
  dangling = #{(entry, S): S in SRC(entry), S not a row id}
  tables_sha = sha256 of the blob .ufo/waves/round-56/frozen-tables.json at --rev equals the embedded constant
               (absent / non-regular / other bytes -> leg missed; the three counts are still computed).

Literal-reading decisions (each also reported in the seat report):
  * ROWS are every line of SOURCES.md whose bytes match `^ {0,3}\\|\\s*S[0-9]{3,}\\s*\\|` -- fences/comments are NOT
    excluded for the registry (the registration states no exclusion).  Cells: strip the line (ASCII whitespace), drop
    one leading `|` and one trailing `|` if present, split on `|`; exactly 11 cells else setup error (rc 2).  No
    backslash-escape handling.  `rows` = number of such lines.
  * Duplicate row ids: the id is "a registry row id" once; USEDBY(S) is the union over its rows.  (Base has none.)
  * ENTRIES = direct children of corpus/knowledge/ that are regular blobs whose name ends `.md` (a leading-dot name
    counts; the name must be non-empty before `.md`).  Entries are read as raw bytes; no decoding anywhere.
  * CITE: fence = a line matching `^ {0,3}(```|~~~)`; a fence is closed by the next fence line of the SAME marker
    (``` closes ```, ~~~ closes ~~~; the other marker inside is content); an unclosed fence runs to end of file;
    fence lines themselves are not "outside".  HTML comments are NOT excluded for CITE.  Lines split on LF only.
  * USEDBY regex applied to cell 11 bytes: `corpus/knowledge/[A-Za-z0-9_.-]+\\.md` (unanchored; findall; so `a.mdx`
    yields `a.md`).  An entry name outside the character class can never be listed, so it is `missing` if cited.
  * SRC: only lines that START with `source:` (no leading space) among the first 15 lines (split on LF); tokens are
    the same S-token regex as CITE; no fence exclusion; continuation lines of a source: list do not count.
  * Pairs are sets (a path listed twice in one cell, or a repeated cite, counts once).
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

TOOL = "c3-r56-used-by.py"
TABLES_SHA256 = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
TABLES_PATH = ".ufo/waves/round-56/frozen-tables.json"
SOURCES_PATH = b"corpus/SOURCES.md"
ENTRY_DIR = b"corpus/knowledge"
REGULAR_MODES = (b"100644", b"100755")
SRC_WINDOW = 15

FENCE = re.compile(rb"^ {0,3}(```|~~~)")
ROW_ID = re.compile(rb"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
S_TOKEN = re.compile(rb"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
USED_BY = re.compile(rb"corpus/knowledge/[A-Za-z0-9_.-]+\.md")


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
        self.env = git_env(work)
        if not os.path.isdir(repo):
            raise SetupError("repo is not a directory")
        if not rev or rev.startswith("-"):
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
        self._blobs = {}

    def git(self, args):
        try:
            return subprocess.run(["git", "-C", self.repo] + args, capture_output=True, env=self.env, timeout=300)
        except (OSError, subprocess.SubprocessError) as exc:
            raise SetupError("git failed to run: %s" % type(exc).__name__)

    def ls(self, path):
        """ls-tree of one exact path (file) or a directory's children (path ending '/'): {bytes path: (mode, type, oid)}."""
        r = self.git(["ls-tree", "-z", self.sha, "--", path])
        if r.returncode != 0:
            raise SetupError("git ls-tree failed")
        out = {}
        for rec in r.stdout.split(b"\0"):
            if not rec:
                continue
            meta, _, name = rec.partition(b"\t")
            parts = meta.split(b" ")
            if len(parts) != 3:
                raise SetupError("unparsable ls-tree record")
            out[name] = (parts[0], parts[1], parts[2])
        return out

    def blob_oid(self, ent):
        if ent is None or ent[0] not in REGULAR_MODES or ent[1] != b"blob":
            return None
        return ent[2]

    def read(self, oid):
        if oid not in self._blobs:
            r = self.git(["cat-file", "blob", oid.decode("ascii")])
            if r.returncode != 0:
                raise SetupError("git cat-file failed")
            self._blobs[oid] = r.stdout
        return self._blobs[oid]

    def regular_file(self, path):
        """bytes of the regular blob at an exact path, else None (absent / symlink / dir / under a symlinked dir)."""
        oid = self.blob_oid(self.ls(path).get(path.encode("utf-8", "surrogateescape") if isinstance(path, str) else path))
        return None if oid is None else self.read(oid)

    def entries(self):
        """{name bytes: contents} of regular blobs corpus/knowledge/*.md (direct children only)."""
        prefix = ENTRY_DIR + b"/"
        out = {}
        for name, ent in sorted(self.ls(prefix.decode("ascii")).items()):
            if not name.startswith(prefix):
                continue
            base = name[len(prefix):]
            if b"/" in base or not base.endswith(b".md") or len(base) <= 3:
                continue
            oid = self.blob_oid(ent)
            if oid is not None:
                out[name] = self.read(oid)
        return out


# --------------------------------------------------------------------------------------------- parsing
def outside_fence_lines(data):
    """lines (bytes, LF split) not inside a fenced block and not themselves fence lines."""
    out = []
    fence = None
    for line in data.split(b"\n"):
        m = FENCE.match(line)
        if fence is not None:
            if m and m.group(1) == fence:
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        out.append(line)
    return out


def cite(data):
    s = set()
    for line in outside_fence_lines(data):
        s.update(S_TOKEN.findall(line))
    return s


def src(data):
    s = set()
    for line in data.split(b"\n")[:SRC_WINDOW]:
        if line.startswith(b"source:"):
            s.update(S_TOKEN.findall(line))
    return s


def parse_registry(data):
    """(rows, usedby): rows = list of row ids (one per row line), usedby = {id: set(paths)}; SetupError on a bad cell count."""
    rows = []
    usedby = {}
    for n, line in enumerate(data.split(b"\n"), 1):
        m = ROW_ID.match(line)
        if not m:
            continue
        s = line.strip()
        if s.startswith(b"|"):
            s = s[1:]
        if s.endswith(b"|"):
            s = s[:-1]
        cells = s.split(b"|")
        if len(cells) != 11:
            raise SetupError("registry row %s at line %d has %d cells, not 11" % (m.group(1).decode("ascii"), n, len(cells)))
        rid = m.group(1)
        rows.append(rid)
        usedby.setdefault(rid, set()).update(USED_BY.findall(cells[10]))
    return rows, usedby


# --------------------------------------------------------------------------------------------- check
def compute(R):
    reg = R.regular_file(SOURCES_PATH.decode("ascii"))
    if reg is None:
        raise SetupError("corpus/SOURCES.md is not a regular blob at --rev")
    rows, usedby = parse_registry(reg)
    ids = set(rows)
    entries = R.entries()
    cites = {p: cite(d) for p, d in entries.items()}
    missing = sorted((s, p) for p, cs in cites.items() for s in cs if s in ids and p not in usedby[s])
    extra = sorted((s, p) for s in ids for p in usedby[s] if p not in entries or s not in cites[p])
    dangling = sorted((p, s) for p, d in entries.items() for s in src(d) if s not in ids)
    return len(entries), len(rows), missing, extra, dangling


def tables_ok(R):
    b = R.regular_file(TABLES_PATH)
    return b is not None and hashlib.sha256(b).hexdigest() == TABLES_SHA256


def check(repo, rev, work, detail=False):
    R = Repo(repo, rev, work)
    e, r, missing, extra, dangling = compute(R)
    missed = []
    if missing:
        missed.append("missing")
    if extra:
        missed.append("extra")
    if dangling:
        missed.append("dangling")
    if not tables_ok(R):
        missed.append("tables_sha")
    if detail:
        for tag, lst in (("missing", missing), ("extra", extra), ("dangling", dangling)):
            for a, b in lst:
                sys.stderr.write("%s: %s %s\n" % (tag, a.decode("utf-8", "replace"), b.decode("utf-8", "replace")))
    met = not missed
    line = "MADO_USED_BY: rev=%s entries=%d rows=%d missing=%d extra=%d dangling=%d verdict=%s missed=%s" % (
        rev, e, r, len(missing), len(extra), len(dangling), "TARGET_MET" if met else "TARGET_MISSED",
        "none" if met else ",".join(missed))
    return line, (0 if met else 1)


# --------------------------------------------------------------------------------------------- selftest
def sh(D, args, env, check_rc=True):
    r = subprocess.run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl"] + args,
                       capture_output=True, env=env, timeout=120)
    if check_rc and r.returncode != 0:
        raise SetupError("selftest git %s failed: %s" % (args[0], r.stderr[:200]))
    return r


def build_repo(base, name, files, symlinks, env):
    """scratch repo with one commit; files {path: bytes}, symlinks {path: target text}."""
    D = os.path.join(base, name)
    os.makedirs(D)
    sh(D, ["init", "-q"], env)
    top = sh(D, ["rev-parse", "--show-toplevel"], env).stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(D):
        raise SetupError("selftest: fixture toplevel mismatch")
    for p, b in files.items():
        fp = os.path.join(D, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "wb") as f:
            f.write(b)
    for p, t in symlinks.items():
        fp = os.path.join(D, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        os.symlink(t, fp)
    sh(D, ["add", "-A"], env)
    sh(D, ["commit", "-q", "-m", "fixture"], env)
    return D


HEADER = b"| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"


def reg_row(sid, used):
    return ("| %s | src %s | docs | A | scope | anchor | teaches | mined | 2026-10-28 | 2027-01-01 | %s |\n" % (sid, sid, used)).encode()


KD = "corpus/knowledge/"
W = KD + "witness-r56.md"
X = KD + "second-r56.md"


def good_files(tables):
    """witness tree: 4 registry rows, 2 entries; every back-reference holds."""
    witness = (b"# witness\nsource: S001, S002\nverified-at: 2026-10-28\nrecheck: soon\n\n"
               b"Cites S001 and S002 and `S003 as code` plus S004.\n"
               b"```\nS900 inside a fence is not a cite\n```\n")
    second = b"# second\nsource: S003\n\nOnly S003 here. The draft id S243 is not a row.\n"
    reg = (b"# SOURCES\n\n## Registry\n\n" + HEADER
           + reg_row("S001", "`" + W + "`")
           + reg_row("S002", W + " and corpus/lessons/round-1.md")
           + reg_row("S003", "`" + W + "`, `" + X + "`")
           + reg_row("S004", W))
    return {
        "corpus/SOURCES.md": reg,
        W: witness,
        X: second,
        TABLES_PATH: tables,
    }


def selftest(repo, rev, work):
    env = git_env(work)
    R = Repo(repo, rev, work)
    tables = R.regular_file(TABLES_PATH)
    if tables is None or hashlib.sha256(tables).hexdigest() != TABLES_SHA256:
        raise SetupError("selftest needs frozen-tables.json at --rev matching the embedded sha256")
    base = os.path.join(work, "selftest-%d" % os.getpid())
    os.makedirs(base)
    script = os.path.abspath(__file__)
    results = []
    counter = [0]
    LINE = re.compile(r"MADO_USED_BY: rev=(\S+) entries=(\d+) rows=(\d+) missing=(\d+) extra=(\d+) dangling=(\d+) "
                      r"verdict=(TARGET_MET|TARGET_MISSED) missed=(\S+)\n")

    def run(D, rev_arg="HEAD", w=None, extra_args=()):
        env2 = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": work, "TMPDIR": work, "GIT_DIR": "/nonexistent"}
        r = subprocess.run([sys.executable, "-I", script, "--repo", D, "--rev", rev_arg, "--work", w or os.path.join(base, "w")]
                           + list(extra_args), capture_output=True, env=env2, timeout=300)
        return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")

    def case(name, mut, want, rc=None, entries=None, rows=None, counts=None, symlinks=None):
        counter[0] += 1
        files = good_files(tables)
        links = {}
        mut(files, links)
        D = build_repo(base, "c%d" % counter[0], files, links, env)
        code, out, err = run(D)
        m = LINE.fullmatch(out)
        got = m.group(8) if m else None
        wantstr = ",".join(want) if want else "none"
        wrc = rc if rc is not None else (0 if not want else 1)
        ok = bool(m) and got == wantstr and code == wrc and m.group(1) == "HEAD"
        ok = ok and m.group(7) == ("TARGET_MET" if not want else "TARGET_MISSED")
        if entries is not None:
            ok = ok and m and int(m.group(2)) == entries
        if rows is not None:
            ok = ok and m and int(m.group(3)) == rows
        if counts is not None:
            ok = ok and m and tuple(int(m.group(i)) for i in (4, 5, 6)) == counts
        results.append((name, bool(ok), wantstr, got if m else "UNPARSABLE rc=%s out=%r err=%r" % (code, out[:100], err[:100])))
        shutil.rmtree(D, ignore_errors=True)
        return out

    def ed(files, path, old, new):
        assert old in files[path], (path, old)
        files[path] = files[path].replace(old, new, 1)

    # ---- positive
    case("good-tree", lambda f, l: None, [], entries=2, rows=4, counts=(0, 0, 0))
    case("good-S243-draft-id-not-row", lambda f, l: ed(f, X, b"S243", b"S243 S243"), [], counts=(0, 0, 0))
    case("good-fenced-S900-not-cite-not-row", lambda f, l: None, [], counts=(0, 0, 0))
    case("good-src-line16-not-window", lambda f, l: ed(f, W, b"recheck: soon\n\n", b"recheck: soon\n" + b"\n" * 11 + b"source: S999\n"),
         [], counts=(0, 0, 0))
    # ---- missing
    case("missing-drop-usedby", lambda f, l: ed(f, "corpus/SOURCES.md", b"| " + W.encode() + b" |", b"|  |"), ["missing"], counts=(1, 0, 0))
    case("cite-already-listed-stays-green", lambda f, l: ed(f, W, b"plus S004.", b"plus S004 and S001."), [], counts=(0, 0, 0))
    case("missing-new-cite", lambda f, l: ed(f, X, b"Only S003", b"Only S003 and S001"), ["missing"], counts=(1, 0, 0))
    case("missing-nonrow-cite-S243-not-counted", lambda f, l: ed(f, X, b"S243", b"S243 S244"), [], counts=(0, 0, 0))
    case("missing-4digit-not-token", lambda f, l: ed(f, X, b"Only S003", b"Only S0014 xS001 S003"), [], counts=(0, 0, 0))
    case("missing-S001a-is-token", lambda f, l: ed(f, X, b"Only S003", b"Only S001a S003"), ["missing"], counts=(1, 0, 0))
    case("missing-tilde-fence-hides", lambda f, l: ed(f, X, b"Only S003", b"~~~\nS001\n~~~\nOnly S003"), [], counts=(0, 0, 0))
    case("missing-mixed-fence-not-closed-by-tilde", lambda f, l: ed(f, X, b"Only S003", b"```\n~~~\nS001\n```\nOnly S003"),
         [], counts=(0, 0, 0))
    case("missing-indent4-not-fence", lambda f, l: ed(f, X, b"Only S003", b"    ```\nS001\nOnly S003"), ["missing"], counts=(1, 0, 0))
    case("missing-unclosed-fence-to-eof", lambda f, l: ed(f, X, b"source: S003\n\nOnly S003 here.", b"```\nsource: S003\n\nOnly S003 S001"), ["extra"], counts=(0, 1, 0))
    # ---- extra
    case("extra-ghost-path", lambda f, l: ed(f, "corpus/SOURCES.md", b"corpus/lessons/round-1.md", b"corpus/knowledge/no-such.md"),
         ["extra"], counts=(0, 1, 0))
    case("extra-entry-does-not-cite", lambda f, l: ed(f, X, b"source: S003\n\nOnly S003 here.", b"title\n\nNothing here."), ["extra"], counts=(0, 1, 0))
    case("extra-fenced-cite-only", lambda f, l: ed(f, X, b"source: S003\n\nOnly S003 here.", b"```\nsource: S003\n\nOnly S003 here.\n```"), ["extra"], counts=(0, 1, 0))
    case("lesson-path-in-usedby-ignored", lambda f, l: None, [], counts=(0, 0, 0))
    case("usedby-subdir-path-no-regex-match", lambda f, l: ed(f, "corpus/SOURCES.md", b"corpus/lessons/round-1.md", b"corpus/knowledge/sub/x.md"),
         [], counts=(0, 0, 0))
    # ---- dangling
    case("dangling-source-S999", lambda f, l: ed(f, W, b"source: S001, S002", b"source: S001, S002 S999"), ["dangling"], counts=(0, 0, 1))
    case("dangling-two-pairs", lambda f, l: (ed(f, W, b"source: S001, S002", b"source: S001, S002 S999"),
                                             ed(f, X, b"source: S003", b"source: S003 S998 S999")),
         ["dangling"], counts=(0, 0, 3))
    case("dangling-draft-S243-on-source-line", lambda f, l: ed(f, X, b"source: S003", b"source: S243"), ["dangling"], counts=(0, 0, 1))
    case("dangling-indented-source-not-counted", lambda f, l: ed(f, X, b"source: S003", b" source: S003 S999"), [], counts=(0, 0, 0))
    # ---- entries / rows accounting
    case("entries-symlink-md-excluded", lambda f, l: l.update({KD + "link.md": "witness-r56.md"}), [], entries=2, counts=(0, 0, 0))
    case("entries-subdir-and-nonmd-excluded",
         lambda f, l: f.update({KD + "sub/deep.md": b"S001\n", KD + "notes.txt": b"S001\n"}), [], entries=2, counts=(0, 0, 0))
    case("entries-extra-entry-citing-counts", lambda f, l: f.update({KD + "third.md": b"cites S004\n"}), ["missing"], entries=3, counts=(1, 0, 0))
    case("rows-fenced-registry-row-counts", lambda f, l: f.__setitem__("corpus/SOURCES.md",
         f["corpus/SOURCES.md"] + b"```\n" + reg_row("S005", "x") + b"```\n"), [], rows=5, counts=(0, 0, 0))
    case("rows-S1000-counts-4digit-id", lambda f, l: f.__setitem__("corpus/SOURCES.md",
         f["corpus/SOURCES.md"] + reg_row("S1000", "x")), [], rows=5, counts=(0, 0, 0))
    case("rows-S12-not-a-row", lambda f, l: f.__setitem__("corpus/SOURCES.md",
         f["corpus/SOURCES.md"] + reg_row("S12", "x")), [], rows=4, counts=(0, 0, 0))
    case("rows-indent4-not-a-row", lambda f, l: f.__setitem__("corpus/SOURCES.md",
         f["corpus/SOURCES.md"] + b"    " + reg_row("S005", "x")), [], rows=4, counts=(0, 0, 0))
    case("usedby-regex-picks-backticked-and-prose", lambda f, l: ed(f, "corpus/SOURCES.md", b"`" + W.encode() + b"`, `" + X.encode() + b"`",
                                                                  b"see (" + W.encode() + b"; " + X.encode() + b")."), [], counts=(0, 0, 0))
    case("usedby-in-cell10-not-counted", lambda f, l: ed(f, "corpus/SOURCES.md", reg_row("S004", W),
         reg_row("S004", "").replace(b"2027-01-01", W.encode())), ["missing"], counts=(1, 0, 0))
    case("usedby-dup-path-in-cell-counts-once", lambda f, l: ed(f, "corpus/SOURCES.md", reg_row("S004", W),
         reg_row("S004", KD + "gone.md " + KD + "gone.md")), ["missing", "extra"], counts=(1, 1, 0))
    # ---- tables_sha
    case("tables-sha-bytes-changed", lambda f, l: f.__setitem__(TABLES_PATH, tables + b" "), ["tables_sha"], counts=(0, 0, 0))
    case("tables-absent", lambda f, l: f.pop(TABLES_PATH), ["tables_sha"], counts=(0, 0, 0))
    case("tables-symlink-is-absent", lambda f, l: (f.pop(TABLES_PATH), l.update({TABLES_PATH: "../../../README"})), ["tables_sha"], counts=(0, 0, 0))
    case("all-legs-listed", lambda f, l: (ed(f, W, b"source: S001, S002", b"source: S001, S002 S999"),
                                          ed(f, X, b"source: S003\n\nOnly S003 here.", b"title\n\nOnly S001 here."),
                                          f.pop(TABLES_PATH)),
         ["missing", "extra", "dangling", "tables_sha"], counts=(1, 1, 1))
    # ---- setup errors: rc 2, nothing on stdout
    def setup_case(name, mut, rev_arg="HEAD", repo_override=None):
        counter[0] += 1
        files = good_files(tables)
        links = {}
        mut(files, links)
        D = build_repo(base, "c%d" % counter[0], files, links, env)
        code, out, err = run(repo_override or D, rev_arg)
        results.append((name, code == 2 and out == "" and err != "", "rc=2 empty stdout", "rc=%s out=%r err=%r" % (code, out[:60], err[:60])))
        shutil.rmtree(D, ignore_errors=True)
    setup_case("setup-10-cell-row", lambda f, l: f.__setitem__("corpus/SOURCES.md", f["corpus/SOURCES.md"] + b"| S777 | a | b |\n"))
    setup_case("setup-12-cell-row", lambda f, l: f.__setitem__("corpus/SOURCES.md", f["corpus/SOURCES.md"] + reg_row("S777", "x|y")))
    setup_case("setup-sources-absent", lambda f, l: f.pop("corpus/SOURCES.md"))
    setup_case("setup-bad-rev", lambda f, l: None, rev_arg="no-such-rev")
    setup_case("setup-rev-dash", lambda f, l: None, rev_arg="--all")
    setup_case("setup-repo-not-dir", lambda f, l: None, repo_override=os.path.join(base, "nonexistent"))

    # ---- the working tree is never read: dirty the worktree of a good repo, result unchanged
    counter[0] += 1
    D = build_repo(base, "c%d" % counter[0], good_files(tables), {}, env)
    with open(os.path.join(D, "corpus/SOURCES.md"), "ab") as f:
        f.write(reg_row("S055", "x"))
    os.unlink(os.path.join(D, W))
    code, out, _ = run(D)
    results.append(("worktree-ignored", code == 0 and "rows=4 " in out and "entries=2 " in out, "good line", out.strip()[:80]))
    # ---- --work is created when missing, counter writes nothing there
    wk = os.path.join(base, "newwork", "deeper")
    code, out, _ = run(D, w=wk)
    results.append(("work-created", code == 0 and os.path.isdir(wk) and os.listdir(wk) == [], "work dir created, empty", "rc=%s %s" % (code, os.listdir(wk) if os.path.isdir(wk) else "absent")))
    # ---- rev echoed as given and full sha equal
    sha = sh(D, ["rev-parse", "HEAD"], env).stdout.decode().strip()
    code, out, _ = run(D, rev_arg=sha)
    results.append(("rev-echoed-as-given", code == 0 and out.startswith("MADO_USED_BY: rev=%s entries=2 rows=4 " % sha), "rev=<full sha>", out[:60]))
    # ---- stdout is exactly one line; --detail changes only stderr
    code1, out1, _ = run(D)
    code2, out2, err2 = run(D, extra_args=("--detail",))
    results.append(("detail-stdout-identical", out1 == out2 and out1.count("\n") == 1, "same single line", out2[:60]))
    # ---- unknown argument is rc 2 with empty stdout (argparse)
    code, out, err = run(D, extra_args=("--bogus",))
    results.append(("usage-error-rc2", code == 2 and out == "", "rc=2", "rc=%s out=%r" % (code, out[:40])))
    shutil.rmtree(D, ignore_errors=True)

    # ---- real tree: tables sha and baseline at the frozen base when readable
    shutil.rmtree(base, ignore_errors=True)
    results.append(("scratch-removed", not os.path.exists(base), "removed", "exists" if os.path.exists(base) else "removed"))

    total = len(results)
    passed = sum(1 for r in results if r[1])
    for name, ok, want, got in results:
        if not ok:
            sys.stderr.write("selftest FAIL %s: want %s got %s\n" % (name, want, got))
    print("MADO_USED_BY_SELFTEST: %d/%d assertions passed" % (passed, total))
    return 0 if passed == total else 1


# --------------------------------------------------------------------------------------------- main
def main(argv):
    ap = argparse.ArgumentParser(prog=TOOL, add_help=True)
    ap.add_argument("--repo", default=None)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--work", required=True)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--detail", action="store_true")
    a = ap.parse_args(argv)  # argparse exits 2 on usage errors, stdout stays empty
    try:
        if a.selftest:
            repo, rev = a.repo or ".", a.rev or "HEAD"
        elif a.repo is None or a.rev is None:
            raise SetupError("--repo and --rev are required")
        else:
            repo, rev = a.repo, a.rev
        os.makedirs(a.work, exist_ok=True)
        if not os.access(a.work, os.W_OK):
            raise SetupError("work dir not writable")
        work = os.path.abspath(a.work)
        if a.selftest:
            return selftest(repo, rev, work)
        line, rc = check(repo, rev, work, a.detail)
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

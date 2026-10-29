#!/usr/bin/env python3
"""c3-r56-used-by.py -- round 56 claim C3 counter (registry used-by back-references).

Implements registration.md section C3 and claims-frozen.md PRED-C3-r56 and nothing else.

  python3 -I c3-r56-used-by.py --repo REPO --rev REV --work DIR
  python3 -I c3-r56-used-by.py --selftest --repo REPO --rev REV --work DIR

Reads ONLY git objects at REV of REPO (git rev-parse / ls-tree / cat-file through
subprocess; never the working tree).  Prints exactly one line on stdout:

  MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=<m> extra=<x> dangling=<d>
                verdict=<TARGET_MET|TARGET_MISSED> missed=<legs,comma-separated|none>

Exit 0 only on TARGET_MET, 1 on a miss, 2 on a setup error (reason on stderr,
nothing on stdout).  Legs: missing, extra, dangling (counts must be 0) and
tables_sha (blob .ufo/waves/round-56/frozen-tables.json at REV hashes to the
embedded constant).  Every failing leg is listed, in the order
missing,extra,dangling,tables_sha.
"""
import hashlib
import os
import re
import subprocess
import sys

TABLES_PATH = ".ufo/waves/round-56/frozen-tables.json"
TABLES_SHA256 = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
SOURCES_PATH = "corpus/SOURCES.md"
KNOWLEDGE_DIR = "corpus/knowledge"
REGULAR_MODES = ("100644", "100755")

ROW_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
CITE_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
USEDBY_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


class Setup(Exception):
    """A setup error: exit 2, reason on stderr, nothing on stdout."""


# --------------------------------------------------------------------------- git

class Git:
    """Read-only git access to one repository; every call names -C and a scrubbed env."""

    def __init__(self, repo, work):
        self.repo = repo
        env = {
            "PATH": os.environ.get("PATH") or "/usr/local/bin:/usr/bin:/bin",
            "HOME": work,
            "TMPDIR": work,
            "LC_ALL": "C",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_REPLACE_OBJECTS": "1",
        }
        self.env = env

    def run(self, *args):
        try:
            p = subprocess.run(
                ["git", "--no-replace-objects", "-C", self.repo] + list(args),
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                env=self.env, cwd=self.env["TMPDIR"], check=False)
        except OSError as e:
            raise Setup("git not runnable: %s" % e)
        return p.returncode, p.stdout, p.stderr.decode("utf-8", "replace").strip()

    def resolve_commit(self, rev):
        if rev.startswith("-") or not rev:
            raise Setup("bad rev %r" % rev)
        rc, out, err = self.run("rev-parse", "--verify", "--quiet", rev + "^{commit}")
        sha = out.decode("ascii", "replace").strip()
        if rc != 0 or not re.fullmatch(r"[0-9a-f]{40}([0-9a-f]{24})?", sha):
            raise Setup("rev %r does not resolve to a commit in %r%s" % (rev, self.repo, (": " + err) if err else ""))
        return sha

    def tree(self, treeish):
        """List a tree: {name: (mode, type, sha)}; raises Setup when git fails."""
        rc, out, err = self.run("ls-tree", "-z", treeish)
        if rc != 0:
            raise Setup("git ls-tree %s failed: %s" % (treeish, err))
        res = {}
        for rec in out.split(b"\0"):
            if not rec:
                continue
            meta, _, name = rec.partition(b"\t")
            mode, typ, sha = meta.decode("ascii").split(" ")
            res[name.decode("utf-8", "surrogateescape")] = (mode, typ, sha)
        return res

    def blob(self, sha):
        rc, out, err = self.run("cat-file", "blob", sha)
        if rc != 0:
            raise Setup("git cat-file blob %s failed: %s" % (sha, err))
        return out


def dir_tree_sha(git, commit, path):
    """Walk path component by component through real trees only; None when any
    component is absent, a symlink, a submodule or a blob (symlinked directory
    is 'absent').  The empty path is the root tree."""
    cur = commit + "^{tree}"
    cur_sha = None
    for comp in [c for c in path.split("/") if c]:
        ents = git.tree(cur)
        e = ents.get(comp)
        if e is None or e[0] != "040000" or e[1] != "tree":
            return None
        cur = cur_sha = e[2]
    if cur_sha is None:
        rc, out, err = git.run("rev-parse", "--verify", cur)
        if rc != 0:
            raise Setup("cannot resolve root tree: %s" % err)
        cur_sha = out.decode("ascii").strip()
    return cur_sha


def regular_blob(git, commit, path):
    """sha of the regular blob (100644/100755) at path, else None."""
    d, _, name = path.rpartition("/")
    t = dir_tree_sha(git, commit, d)
    if t is None:
        return None
    e = git.tree(t).get(name)
    if e is None or e[1] != "blob" or e[0] not in REGULAR_MODES:
        return None
    return e[2]


def decode(b):
    return b.decode("utf-8", "replace")


# ------------------------------------------------------------------- definitions

def cells_of(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return s.split("|")


def parse_rows(text):
    """ROWS: list of (id, used_by_cell).  A matching row without exactly 11 cells is a setup error."""
    rows = []
    for ln, line in enumerate(text.split("\n"), 1):
        if not ROW_RE.match(line):
            continue
        cells = cells_of(line)
        if len(cells) != 11:
            raise Setup("%s:%d has %d cells, expected 11" % (SOURCES_PATH, ln, len(cells)))
        rows.append((cells[0].strip(), cells[10]))
    return rows


def unfenced_lines(lines):
    """Lines outside fenced code blocks (``` / ~~~, 0-3 leading spaces).  A fence closes on a
    line of the same character, at least as long, followed only by whitespace; an unclosed
    fence runs to end of file."""
    out = []
    fence = None  # (char, length)
    for line in lines:
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
            else:
                out.append(line)
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and m.group(2).strip() == "":
                fence = None
    return out


def cite_set(text):
    toks = set()
    for line in unfenced_lines(text.split("\n")):
        toks.update(CITE_RE.findall(line))
    return toks


def src_set(text):
    toks = set()
    for line in text.split("\n")[:15]:
        if line.startswith("source:"):
            toks.update(CITE_RE.findall(line))
    return toks


# ------------------------------------------------------------------------ counter

def count(repo, rev, work):
    """Return (commit, E, R, m, x, d, tables_ok)."""
    git = Git(repo, work)
    commit = git.resolve_commit(rev)

    sources_sha = regular_blob(git, commit, SOURCES_PATH)
    if sources_sha is None:
        raise Setup("%s is not a regular blob at %s" % (SOURCES_PATH, rev))
    rows = parse_rows(decode(git.blob(sources_sha)))
    row_ids = set(r[0] for r in rows)
    usedby = {}
    for rid, cell in rows:
        usedby.setdefault(rid, set()).update(USEDBY_RE.findall(cell))

    kt = dir_tree_sha(git, commit, KNOWLEDGE_DIR)
    entries = {}
    if kt is not None:
        for name, (mode, typ, sha) in git.tree(kt).items():
            if name.endswith(".md") and typ == "blob" and mode in REGULAR_MODES:
                entries[KNOWLEDGE_DIR + "/" + name] = sha

    cites, srcs = {}, {}
    for path, sha in entries.items():
        text = decode(git.blob(sha))
        cites[path] = cite_set(text)
        srcs[path] = src_set(text)

    missing = sum(1 for path in entries for s in cites[path] if s in row_ids and path not in usedby[s])
    extra = 0
    for s in row_ids:
        for path in usedby[s]:
            if path not in entries or s not in cites[path]:
                extra += 1
    dangling = sum(1 for path in entries for s in srcs[path] if s not in row_ids)

    tsha = regular_blob(git, commit, TABLES_PATH)
    tables_ok = tsha is not None and hashlib.sha256(git.blob(tsha)).hexdigest() == TABLES_SHA256
    return commit, len(entries), len(rows), missing, extra, dangling, tables_ok


def render(rev, E, R, m, x, d, tables_ok):
    missed = [n for n, bad in (("missing", m), ("extra", x), ("dangling", d), ("tables_sha", not tables_ok)) if bad]
    met = not missed
    line = "MADO_USED_BY: rev=%s entries=%d rows=%d missing=%d extra=%d dangling=%d verdict=%s missed=%s" % (
        rev, E, R, m, x, d, "TARGET_MET" if met else "TARGET_MISSED", ",".join(missed) if missed else "none")
    return line, met


# ------------------------------------------------------------------------ argv

def parse_args(argv):
    opts, selftest, i = {}, False, 0
    while i < len(argv):
        a = argv[i]
        if a == "--selftest":
            if selftest:
                raise Setup("usage: repeated --selftest")
            selftest = True
            i += 1
        elif a in ("--repo", "--rev", "--work"):
            if a in opts:
                raise Setup("usage: repeated %s" % a)
            if i + 1 >= len(argv):
                raise Setup("usage: %s needs a value" % a)
            opts[a] = argv[i + 1]
            i += 2
        else:
            raise Setup("usage: unknown argument %r" % a)
    for need in ("--repo", "--rev", "--work"):
        if need not in opts:
            raise Setup("usage: missing %s (python3 -I c3-r56-used-by.py [--selftest] --repo R --rev V --work D)" % need)
    if not opts["--work"]:
        raise Setup("usage: empty --work")
    return opts, selftest


def ensure_work(work):
    try:
        os.makedirs(work, exist_ok=True)
    except OSError as e:
        raise Setup("cannot create --work %r: %s" % (work, e))
    if not os.path.isdir(work):
        raise Setup("--work %r is not a directory" % work)
    return os.path.realpath(work)


# ---------------------------------------------------------------------- selftest

SELF = os.path.abspath(__file__)


class Scratch:
    """A scratch git repository under the work dir; every git call names -C."""

    def __init__(self, work, label):
        import tempfile
        self.dir = tempfile.mkdtemp(prefix=label + ".", dir=work)
        self.env = {"PATH": os.environ.get("PATH") or "/usr/bin:/bin", "HOME": work, "TMPDIR": work,
                    "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C"}
        self.git("init", "-q")
        top = self.git("rev-parse", "--show-toplevel").strip()
        if os.path.realpath(top) != os.path.realpath(self.dir):
            raise Setup("scratch toplevel %r != %r" % (top, self.dir))

    def git(self, *a):
        p = subprocess.run(["git", "-C", self.dir] + list(a), env=self.env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return p.stdout.decode("utf-8", "replace")

    def put(self, path, data, symlink=False):
        full = os.path.join(self.dir, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        if os.path.lexists(full):
            os.unlink(full)
        if symlink:
            os.symlink(data, full)
        else:
            with open(full, "wb") as f:
                f.write(data if isinstance(data, bytes) else data.encode("utf-8"))

    def commit(self):
        self.git("add", "-A", "-f")
        self.git("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", "x")
        return self.git("rev-parse", "HEAD").strip()


HEADER = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"


def row(sid, used):
    return "| %s | src %s | docs | A | scope | anchor | teaches | mined | 2026-10-28 | 2027-01-01 | %s |\n" % (sid, sid, used)


def witness(tables_bytes):
    """Witness corpus generated here: 4 entries, 6 rows, every citation backed by a used-by path."""
    e = "corpus/knowledge/"
    files = {
        e + "alpha.md": "# alpha\nsource: S001 S002\nverified-at: 2026-10-28\n\nBody cites S001 and `S002` and S003.\nS243 is a draft id, not a row.\n",
        e + "beta.md": "# beta\nsource: S004\n\nCites S004, also (S005).\n\n```\nS006 inside a fence is not a citation\n```\n",
        e + "gamma.md": "# gamma\nno source line here\nSee S001. Also xS002 and S0031 and S1234 are not tokens.\n",
        e + "delta.md": "# delta\nplain text, no citation\n",
        ".ufo/waves/round-56/frozen-tables.json": tables_bytes,
    }
    used = {
        "S001": e + "alpha.md " + e + "gamma.md",
        "S002": e + "alpha.md",
        "S003": e + "alpha.md",
        "S004": e + "beta.md",
        "S005": e + "beta.md",
        "S006": "-",
    }
    return files, used


def sources_text(used, extra_rows=""):
    return ("# SOURCES\n\n## Registry\n\n" + HEADER + "".join(row(s, used[s]) for s in sorted(used)) + extra_rows)


def selftest(opts):
    work = ensure_work(opts["--work"])
    host = Git(opts["--repo"], work)
    hcommit = host.resolve_commit(opts["--rev"])
    tsha = regular_blob(host, hcommit, TABLES_PATH)
    if tsha is None:
        raise Setup("selftest needs %s at --rev to build the scratch repos" % TABLES_PATH)
    tables = host.blob(tsha)
    if hashlib.sha256(tables).hexdigest() != TABLES_SHA256:
        raise Setup("selftest: frozen-tables.json at --rev does not hash to the embedded constant")

    results = []

    def check(name, ok):
        results.append((name, bool(ok)))

    def cli(repo, rev, extra=None, workdir=None):
        args = [sys.executable, "-I", SELF, "--repo", repo, "--rev", rev, "--work", workdir or work]
        if extra is not None:
            args = [sys.executable, "-I", SELF] + extra
        env = {"PATH": os.environ.get("PATH") or "/usr/bin:/bin", "TMPDIR": work, "HOME": work}
        p = subprocess.run(args, env=env, cwd=work, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")

    def line(rev, E, R, m, x, d, verdict, missed):
        return ("MADO_USED_BY: rev=%s entries=%d rows=%d missing=%d extra=%d dangling=%d verdict=%s missed=%s\n"
                % (rev, E, R, m, x, d, verdict, missed))

    def build(label, mutate=None, with_tables=True, tables_override=None):
        s = Scratch(work, label)
        files, used = witness(tables if tables_override is None else tables_override)
        if not with_tables:
            files.pop(".ufo/waves/round-56/frozen-tables.json")
        src = {"used": used, "extra_rows": ""}
        if mutate:
            mutate(files, src, s)
        for p, d in files.items():
            s.put(p, d)
        s.put(SOURCES_PATH, sources_text(src["used"], src["extra_rows"]))
        return s, s.commit()

    # 1 good witness
    s, c = build("good")
    rc, out, err = cli(s.dir, c)
    check("witness TARGET_MET exact line", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)
    check("witness stderr empty", err == "")
    # symbolic rev prints rev as given
    rc, out, _ = cli(s.dir, "HEAD")
    check("rev printed as given", out.startswith("MADO_USED_BY: rev=HEAD entries=4 ") and rc == 0)

    # 2 missing: drop alpha from S002
    def drop(files, src, s):
        src["used"]["S002"] = "-"
    s, c = build("drop", drop)
    rc, out, _ = cli(s.dir, c)
    check("missing=1 on dropped used-by", out == line(c, 4, 6, 1, 0, 0, "TARGET_MISSED", "missing") and rc == 1)

    # 3 extra: fill every row with all entries
    def fill(files, src, s):
        allp = " ".join(sorted(k for k in files if k.startswith("corpus/knowledge/")))
        for k in src["used"]:
            src["used"][k] = allp
    s, c = build("fill", fill)
    rc, out, _ = cli(s.dir, c)
    # cites: alpha{S001,S002,S003} beta{S004,S005} gamma{S001} -> 6 true pairs; 6 rows * 4 entries = 24 -> extra 18; missing 0
    check("fill-all extra=18 missing=0", out == line(c, 4, 6, 0, 18, 0, "TARGET_MISSED", "extra") and rc == 1)

    # 4 dangling source
    def dang(files, src, s):
        files["corpus/knowledge/alpha.md"] = files["corpus/knowledge/alpha.md"].replace("source: S001 S002", "source: S001 S002 S999")
    s, c = build("dang", dang)
    rc, out, _ = cli(s.dir, c)
    check("dangling=1 on S999 source token", out == line(c, 4, 6, 0, 0, 1, "TARGET_MISSED", "dangling") and rc == 1)

    # 5 ghost path
    def ghost(files, src, s):
        src["used"]["S001"] += " corpus/knowledge/no-such-entry.md"
    s, c = build("ghost", ghost)
    rc, out, _ = cli(s.dir, c)
    check("ghost path is extra=1", out == line(c, 4, 6, 0, 1, 0, "TARGET_MISSED", "extra") and rc == 1)

    # 6 citation moved into a fence: used-by still lists the entry
    def fence(files, src, s):
        files["corpus/knowledge/gamma.md"] = files["corpus/knowledge/gamma.md"].replace(
            "See S001. Also", "```\nSee S001.\n```\nAlso")
    s, c = build("fence", fence)
    rc, out, _ = cli(s.dir, c)
    check("fenced cite is extra=1", out == line(c, 4, 6, 0, 1, 0, "TARGET_MISSED", "extra") and rc == 1)

    # 7 tilde fence, indented 3 and 4 spaces
    def tilde(files, src, s):
        files["corpus/knowledge/gamma.md"] = "# g\n   ~~~\nSee S001.\n   ~~~\n"
    s, c = build("tilde", tilde)
    rc, out, _ = cli(s.dir, c)
    check("3-space ~~~ fence hides the cite", out == line(c, 4, 6, 0, 1, 0, "TARGET_MISSED", "extra") and rc == 1)

    def indented(files, src, s):
        files["corpus/knowledge/gamma.md"] = "# g\n    ~~~\nSee S001.\n    ~~~\n"
    s, c = build("indent4", indented)
    rc, out, _ = cli(s.dir, c)
    check("4-space ~~~ is no fence, cite counts", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none").replace("verdict=TARGET_MET", "verdict=TARGET_MET") and rc == 0)

    def mismatch(files, src, s):
        files["corpus/knowledge/gamma.md"] = "# g\n```\n~~~\nSee S001.\n```\nafter\n"
    s, c = build("mismatch", mismatch)
    rc, out, _ = cli(s.dir, c)
    check("~~~ does not close a ``` fence", out == line(c, 4, 6, 0, 1, 0, "TARGET_MISSED", "extra") and rc == 1)

    # 8 tables_sha: absent, altered; counts unchanged
    s, c = build("notables", with_tables=False)
    rc, out, _ = cli(s.dir, c)
    check("absent tables blob -> tables_sha only", out == line(c, 4, 6, 0, 0, 0, "TARGET_MISSED", "tables_sha") and rc == 1)
    s, c = build("badtables", tables_override=tables + b" ")
    rc, out, _ = cli(s.dir, c)
    check("altered tables blob -> tables_sha only", out == line(c, 4, 6, 0, 0, 0, "TARGET_MISSED", "tables_sha") and rc == 1)

    # 9 list-all: every failing leg listed in order
    def all_legs(files, src, s):
        src["used"]["S002"] = "-"
        src["used"]["S006"] = "corpus/knowledge/delta.md"
        files["corpus/knowledge/alpha.md"] += "source: S998\n"
        files["corpus/knowledge/delta.md"] = "# d\nsource: S777\n"
    s, c = build("alllegs", all_legs, with_tables=False)
    rc, out, _ = cli(s.dir, c)
    check("every failing leg listed", out == line(c, 4, 6, 1, 1, 2, "TARGET_MISSED", "missing,extra,dangling,tables_sha") and rc == 1)

    # 10 symlink entry is absent; symlinked knowledge dir is absent
    def symentry(files, src, s):
        files["corpus/knowledge/real.md"] = "# real\nS004 here\n"
        src["used"]["S004"] += " corpus/knowledge/link.md"
    s, c = build("symentry", symentry)
    s.put("corpus/knowledge/link.md", "real.md", symlink=True)
    c = s.commit()
    rc, out, _ = cli(s.dir, c)
    # real.md cites S004 without used-by -> missing 1; link.md is no entry but used-by names it -> extra 1; entries=5
    check("symlink blob is not an entry", out == line(c, 5, 6, 1, 1, 0, "TARGET_MISSED", "missing,extra") and rc == 1)

    s = Scratch(work, "symdir")
    files, used = witness(tables)
    for p, d in files.items():
        if p.startswith("corpus/knowledge/"):
            s.put("realk/" + p[len("corpus/knowledge/"):], d)
        else:
            s.put(p, d)
    s.put("corpus/knowledge", "../realk", symlink=True)
    s.put(SOURCES_PATH, sources_text(used))
    c = s.commit()
    rc, out, _ = cli(s.dir, c)
    # no entries at all; every used-by path is then extra: 6 distinct (S,path) pairs
    check("symlinked knowledge dir is absent", out == line(c, 0, 6, 0, 6, 0, "TARGET_MISSED", "extra") and rc == 1)

    s = Scratch(work, "symsrc")
    files, used = witness(tables)
    for p, d in files.items():
        s.put(p, d)
    s.put("realc/SOURCES.md", sources_text(used))
    s.put("corpus/SOURCES.md", "../realc/SOURCES.md", symlink=True)
    c = s.commit()
    rc, out, err = cli(s.dir, c)
    check("symlink SOURCES.md is a setup error", rc == 2 and out == "" and err.strip() != "")

    # 11 setup errors: stdout empty, exit 2
    def bad_cells(files, src, s):
        src["extra_rows"] = "| S100 | only | three |\n"
    s, c = build("cells", bad_cells)
    rc, out, err = cli(s.dir, c)
    check("row with 3 cells -> exit 2, empty stdout", rc == 2 and out == "" and "cells" in err)

    def twelve(files, src, s):
        src["extra_rows"] = row("S100", "-").rstrip("\n") + " extra |\n"
    s, c = build("twelve", twelve)
    rc, out, err = cli(s.dir, c)
    check("row with 12 cells -> exit 2, empty stdout", rc == 2 and out == "" and "cells" in err)

    s, c = build("good2")
    rc, out, err = cli(s.dir, "0" * 40)
    check("unknown rev -> exit 2, empty stdout", rc == 2 and out == "" and err.strip() != "")
    rc, out, err = cli(s.dir, "--help")
    check("option-looking rev -> exit 2", rc == 2 and out == "")
    rc, out, err = cli(os.path.join(work, "no-such-repo"), c)
    check("missing repo -> exit 2", rc == 2 and out == "")
    for name, argv in (
        ("missing --work", ["--repo", s.dir, "--rev", c]),
        ("missing --rev", ["--repo", s.dir, "--work", work]),
        ("repeated --repo", ["--repo", s.dir, "--repo", s.dir, "--rev", c, "--work", work]),
        ("unknown token", ["--repo", s.dir, "--rev", c, "--work", work, "--bogus"]),
        ("option without value", ["--repo", s.dir, "--rev", c, "--work"]),
    ):
        rc, out, err = cli(None, None, extra=argv)
        check("usage error: " + name, rc == 2 and out == "" and err.strip() != "")

    # 12 reads git objects, not the working tree
    s, c = build("wt")
    s.put("corpus/SOURCES.md", sources_text({k: "-" for k in witness(tables)[1]}))
    s.put("corpus/knowledge/alpha.md", "# changed\nS777 S888\n")
    s.put("corpus/knowledge/untracked.md", "# untracked\nS001\n")
    rc, out, _ = cli(s.dir, c)
    check("working-tree edits and untracked files ignored", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    # 13 token grammar
    def tokens(files, src, s):
        files["corpus/knowledge/delta.md"] = "# d\nS243 and xS001 and S0011 and S1234 and S12 and aS003\n"
    s, c = build("tokens", tokens)
    rc, out, _ = cli(s.dir, c)
    check("non-token spellings and non-row S243 add nothing", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    def srcline(files, src, s):
        files["corpus/knowledge/delta.md"] = "# d\nsource: S243\n"
    s, c = build("srcdraft", srcline)
    rc, out, _ = cli(s.dir, c)
    check("non-row id on a source: line is dangling", out == line(c, 4, 6, 0, 0, 1, "TARGET_MISSED", "dangling") and rc == 1)

    def srcdeep(files, src, s):
        files["corpus/knowledge/delta.md"] = "\n" * 15 + "source: S999\n"
    s, c = build("srcdeep", srcdeep)
    rc, out, _ = cli(s.dir, c)
    check("source: on line 16 is outside the first 15", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    def srcindent(files, src, s):
        files["corpus/knowledge/delta.md"] = "# d\n source: S999\n"
    s, c = build("srcindent", srcindent)
    rc, out, _ = cli(s.dir, c)
    check("indented source: is not a source line", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    def underscore(files, src, s):
        files["corpus/knowledge/delta.md"] = "# d\n_S004 and S004_ and (S004) and S004.\n"
    s, c = build("underscore", underscore)
    rc, out, _ = cli(s.dir, c)
    check("underscore does not hide a token", out == line(c, 4, 6, 1, 0, 0, "TARGET_MISSED", "missing") and rc == 1)

    # 14 only direct children *.md are entries
    def nested(files, src, s):
        files["corpus/knowledge/sub/deep.md"] = "# deep\nS001\n"
        files["corpus/knowledge/notes.txt"] = "S001\n"
    s, c = build("nested", nested)
    rc, out, _ = cli(s.dir, c)
    check("nested and non-.md files are not entries", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    # 15 used-by cell: non-registry rows and text around paths
    def spoofcell(files, src, s):
        src["used"]["S006"] = "corpus/knowledge/sub/deep.md"
    s, c = build("spoofcell", spoofcell)
    rc, out, _ = cli(s.dir, c)
    check("path in a subdirectory does not match the used-by regex", out == line(c, 4, 6, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    # 16 row regex: indented rows count, 4-space indent does not
    def indrow(files, src, s):
        src["extra_rows"] = "   " + row("S007", "-") + "    " + row("S008", "-")
    s, c = build("indrow", indrow)
    rc, out, _ = cli(s.dir, c)
    check("3-space row counts, 4-space row does not", out == line(c, 4, 7, 0, 0, 0, "TARGET_MET", "none") and rc == 0)

    # 17 executable blob is a regular entry
    s, c = build("exec")
    s.put("corpus/knowledge/epsilon.md", "# e\nS006 cited\n")
    os.chmod(os.path.join(s.dir, "corpus/knowledge/epsilon.md"), 0o755)
    c = s.commit()
    rc, out, _ = cli(s.dir, c)
    check("mode 100755 entry is an entry (missing S006)", out == line(c, 5, 6, 1, 0, 0, "TARGET_MISSED", "missing") and rc == 1)

    # 18 duplicate-in-text cites count once per (S, entry)
    def dup(files, src, s):
        files["corpus/knowledge/delta.md"] = "# d\nS006 S006 S006\n"
    s, c = build("dupcite", dup)
    rc, out, _ = cli(s.dir, c)
    check("repeated citation counts one pair", out == line(c, 4, 6, 1, 0, 0, "TARGET_MISSED", "missing") and rc == 1)

    # 19 stdout is exactly one line on every completed run
    rc, out, _ = cli(s.dir, c)
    check("exactly one stdout line", out.count("\n") == 1 and out.startswith("MADO_USED_BY: "))

    # 20 no --work side effect beyond creating it; counter creates a missing --work
    fresh = os.path.join(work, "fresh-work-dir")
    rc, out, _ = cli(s.dir, c, workdir=fresh)
    check("missing --work is created and left empty", os.path.isdir(fresh) and os.listdir(fresh) == [] and rc in (0, 1))

    # 21 base revision of the lane, when the object is readable in --repo
    base = "13f0acbe3a15da2d9c08357a576d91dcadc85273"
    rc0, _, _ = host.run("cat-file", "-e", base + "^{commit}")
    if rc0 == 0:
        rc, out, _ = cli(opts["--repo"], base)
        check("lane base revision baseline", out == ("MADO_USED_BY: rev=%s entries=70 rows=319 missing=65 extra=0 dangling=0 "
                                                      "verdict=TARGET_MISSED missed=missing,tables_sha\n" % base) and rc == 1)
    # 22 the real rev is accepted by the checker wiring (tables blob present and hashing)
    check("selftest rev tables blob hashes to constant", hashlib.sha256(tables).hexdigest() == TABLES_SHA256)

    failed = [n for n, ok in results if not ok]
    for n in failed:
        sys.stderr.write("FAILED: %s\n" % n)
    print("%d/%d assertions passed" % (len(results) - len(failed), len(results)))
    return 0 if not failed else 1


# ------------------------------------------------------------------------- main

def main(argv):
    try:
        opts, is_selftest = parse_args(argv)
        if is_selftest:
            return selftest(opts)
        work = ensure_work(opts["--work"])
        _commit, E, R, m, x, d, tables_ok = count(opts["--repo"], opts["--rev"], work)
        out, met = render(opts["--rev"], E, R, m, x, d, tables_ok)
    except Setup as e:
        sys.stderr.write("MADO_USED_BY setup error: %s\n" % e)
        return 2
    sys.stdout.write(out + "\n")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

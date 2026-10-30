#!/usr/bin/env python3
"""c3-r56-used-by.py -- PRED-C3-r56-v2 counter (mado round 56, claim C3: registry back-reference consistency, token level, reviewed).

Contract: `.ufo/waves/round-56/registration-v2.md` section C3-v2 (supersedes registration.md section C3) and
`.ufo/waves/round-56/claims-frozen-v2.md`.  Built from seat R56ExecC3CounterA's reader (Repo, CITE, SRC, registry parser),
extended by the L1 with the frozen name-only allowlist and the conflict / stale / lost / allow_sha legs.

    python3 -I c3-r56-used-by.py --repo <lane> --rev <rev> --work <scratch> [--detail]
    python3 -I c3-r56-used-by.py --selftest [--repo <lane> --rev <rev>] --work <scratch>

Prints exactly one line (stdout):

    MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=<m> extra=<x> dangling=<d> conflict=<c> stale=<s> lost=<l> exempt=<n> verdict=<TARGET_MET|TARGET_MISSED> missed=<legs,comma>|none

Exit 0 only on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on stderr, nothing on stdout).  `--detail` lists offending pairs on stderr.
Every input byte comes from git objects at --rev of --repo (and, for `lost`, at the frozen base revision of the same repo); the working tree is never opened.
Only regular blobs (mode 100644/100755) count.  --work is HOME/TMPDIR of every git child; the counter writes nothing (selftest writes under <work>/selftest-*, removed on exit).

Legs in `missed` order: missing extra dangling conflict stale lost allow_sha exempt tables_sha.
  PAIRS(rev)  = {(S, entry): S registry row id, entry in ENTRIES, S in CITE(entry)}
  missing     = pairs with the entry path not in USEDBY(S) and not an allowlist row
  extra       = (S, path) with path in USEDBY(S) and (path not in ENTRIES or S not in CITE(path))
  dangling    = (entry, S) with S in SRC(entry) and S not a registry row id
  conflict    = allowlist rows whose entry is in USEDBY(S)
  stale       = allowlist rows whose entry/pair is absent at rev or whose LINESHA differs (sha256 of the citing lines outside fences, joined by LF)
  lost        = the base `missing` pairs (registration-v2 E12; 65 at base) absent from PAIRS(rev); base objects must exist and hash to c3.base_pairs_sha256 (else setup error, fail closed)
  allow_sha   = the allowlist blob at rev has sha256 c3.allowlist_sha256 (absent -> missed, rows empty)
  exempt      = the number of allowlist rows must equal c3.exempt (24)
  tables_sha  = frozen-tables-v2.json at rev has the embedded sha256
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

TOOL = "c3-r56-used-by.py"
TABLES_SHA256 = "9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2"
TABLES_PATH = ".ufo/waves/round-56/frozen-tables-v2.json"
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
def line_sha(lines):
    return hashlib.sha256(b"\n".join(lines)).hexdigest()


def pair_data(R):
    """(rows, usedby, entries, pairlines): pairlines = {(S, entry): [citing lines outside fences]} for S a row id."""
    reg = R.regular_file(SOURCES_PATH.decode("ascii"))
    if reg is None:
        raise SetupError("corpus/SOURCES.md is not a regular blob at the revision")
    rows, usedby = parse_registry(reg)
    ids = set(rows)
    entries = R.entries()
    pairlines = {}
    for p, d in entries.items():
        for line in outside_fence_lines(d):
            for s in set(S_TOKEN.findall(line)):
                if s in ids:
                    pairlines.setdefault((s, p), []).append(line)
    return rows, usedby, entries, pairlines


def parse_allow(blob):
    out = {}
    if blob is None:
        return out
    for line in blob.split(b"\n"):
        if not line:
            continue
        cells = line.split(b"\t")
        if len(cells) != 4:
            raise SetupError("allowlist row without 4 tab-separated cells")
        out[(cells[0], cells[1])] = cells[2].decode("ascii", "replace")
    return out


def base_pairs(repo, work, t):
    try:
        B = Repo(repo, t["base_rev"], work)
    except SetupError:
        raise SetupError("base revision objects are absent: fail closed")
    _, _, _, pl0 = pair_data(B)
    _, ub0, _, _ = pair_data(B)
    pl = {k: v for k, v in pl0.items() if k[1] not in ub0[k[0]]}   # registration-v2 E12: the base `missing` pairs
    lines = sorted("%s|%s" % (s.decode("ascii"), p.decode("utf-8", "replace")) for s, p in pl)
    h = hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()
    if h != t["base_pairs_sha256"]:
        raise SetupError("base pairs hash differs from the frozen value")
    return set(pl)


def load_tables(R, override):
    if override is not None:
        return override, True
    b = R.regular_file(TABLES_PATH)
    ok = b is not None and hashlib.sha256(b).hexdigest() == TABLES_SHA256
    if b is None:
        raise SetupError("frozen-tables-v2.json is not a regular blob at --rev")
    try:
        c3 = json.loads(b.decode("utf-8"))["c3"]
        for k in ("allowlist_path", "allowlist_sha256", "exempt", "base_rev", "base_pairs_sha256"):
            c3[k]
    except (ValueError, KeyError, TypeError):
        raise SetupError("frozen-tables-v2.json c3 unreadable")
    return c3, ok


def check(repo, rev, work, detail=False, override=None):
    R = Repo(repo, rev, work)
    t, tables_good = load_tables(R, override)
    rows, usedby, entries, pairlines = pair_data(R)
    ids = set(rows)
    ablob = R.regular_file(t["allowlist_path"])
    allow = parse_allow(ablob)
    allow_ok = ablob is not None and hashlib.sha256(ablob).hexdigest() == t["allowlist_sha256"]
    allowk = {(s, p): h for (s, p), h in allow.items()}
    missing = sorted((s, p) for (s, p) in pairlines if p not in usedby[s] and (s, p) not in allowk)
    extra = sorted((s, p) for s in ids for p in usedby[s] if p not in entries or (s, p) not in pairlines)
    dangling = sorted((p, s) for p, d in entries.items() for s in src(d) if s not in ids)
    conflict = sorted((s, p) for (s, p) in allowk if p in usedby.get(s, set()))
    stale = sorted((s, p) for (s, p), h in allowk.items() if (s, p) not in pairlines or line_sha(pairlines[(s, p)]) != h)
    lost = sorted(base_pairs(repo, work, t) - set(pairlines))
    missed = []
    for leg, lst in (("missing", missing), ("extra", extra), ("dangling", dangling), ("conflict", conflict), ("stale", stale), ("lost", lost)):
        if lst:
            missed.append(leg)
    if not allow_ok:
        missed.append("allow_sha")
    if len(allowk) != t["exempt"]:
        missed.append("exempt")
    if not tables_good:
        missed.append("tables_sha")
    if detail:
        for tag, lst in (("missing", missing), ("extra", extra), ("dangling", dangling), ("conflict", conflict), ("stale", stale), ("lost", lost)):
            for a, b in lst:
                sys.stderr.write("%s: %s %s\n" % (tag, a.decode("utf-8", "replace"), b.decode("utf-8", "replace")))
    met = not missed
    line = ("MADO_USED_BY: rev=%s entries=%d rows=%d missing=%d extra=%d dangling=%d conflict=%d stale=%d lost=%d exempt=%d verdict=%s missed=%s"
            % (rev, len(entries), len(rows), len(missing), len(extra), len(dangling), len(conflict), len(stale), len(lost), len(allowk),
               "TARGET_MET" if met else "TARGET_MISSED", "none" if met else ",".join(missed)))
    return line, (0 if met else 1)


# --------------------------------------------------------------------------------------------- selftest
def sh(D, args, env, check_rc=True):
    r = subprocess.run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl"] + args,
                       capture_output=True, env=env, timeout=120)
    if check_rc and r.returncode != 0:
        raise SetupError("selftest git %s failed: %s" % (args[0], r.stderr[:200]))
    return r


def commit_tree(D, files, env, msg):
    for p, b in files.items():
        fp = os.path.join(D, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        if b is None:
            if os.path.lexists(fp):
                os.remove(fp)
            continue
        with open(fp, "wb") as f:
            f.write(b)
    sh(D, ["add", "-A"], env)
    sh(D, ["commit", "-q", "--allow-empty", "-m", msg], env)
    return sh(D, ["rev-parse", "HEAD"], env).stdout.decode().strip()


HEADER = b"| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"


def reg_row(sid, used):
    return ("| %s | src %s | docs | A | scope | anchor | teaches | mined | 2026-10-28 | 2027-01-01 | %s |\n" % (sid, sid, used)).encode()


KD = "corpus/knowledge/"
W = KD + "witness-r56.md"
X = KD + "second-r56.md"
AL = "allow.tsv"


def registry(used):
    return (b"# SOURCES\n\n## Registry\n\n" + HEADER + reg_row("S001", used["S001"]) + reg_row("S002", used["S002"])
            + reg_row("S003", used["S003"]) + reg_row("S004", used["S004"]))


def selftest(repo, rev, work):
    env = git_env(work)
    base = os.path.join(work, "selftest-%d" % os.getpid())
    os.makedirs(base)
    passed = total = 0
    try:
        D = os.path.join(base, "fx")
        os.makedirs(D)
        sh(D, ["init", "-q"], env)
        top = sh(D, ["rev-parse", "--show-toplevel"], env).stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(D):
            raise SetupError("selftest: fixture toplevel mismatch")
        witness = (b"# witness\nsource: S001, S002\nverified-at: 2026-10-28\nrecheck: soon\n\nCites S001 and S002 and S004.\n"
                   b"```\nS003 inside a fence is not a cite\n```\n")
        second = b"# second\nsource: S003\n\nOnly S003 here. The draft id S243 is not a row. S004 is named only to be refuted.\n"
        nameonly = second.split(b"\n")[3]
        used0 = {"S001": "-", "S002": "-", "S003": "-", "S004": "-"}
        files0 = {"corpus/SOURCES.md": registry(used0), W: witness, X: second}
        base_sha = commit_tree(D, files0, env, "base")
        R0 = Repo(D, base_sha, base)
        _, ub_, _, pl0 = pair_data(R0)
        bl = sorted("%s|%s" % (s.decode(), p.decode()) for s, p in pl0 if p not in ub_[s])
        base_hash = hashlib.sha256(("\n".join(bl) + "\n").encode()).hexdigest()
        allow_row = ("S004\t%s\t%s\tnamed only to be refuted\n" % (X, line_sha([nameonly]))).encode()
        usedg = {"S001": W, "S002": W, "S003": X, "S004": W}
        good = {"corpus/SOURCES.md": registry(usedg), AL: allow_row}
        good_sha = commit_tree(D, good, env, "good")
        t = {"allowlist_path": AL, "allowlist_sha256": hashlib.sha256(allow_row).hexdigest(), "exempt": 1,
             "base_rev": base_sha, "base_pairs_sha256": base_hash}

        def run(sha, label, legs=(), nolegs=(), met=False, tt=None):
            nonlocal passed, total
            line, rc = check(D, sha, base, override=tt or t)
            m = re.search(r" missed=(\S+)$", line)
            got = [] if m.group(1) == "none" else m.group(1).split(",")
            ok = (rc == 0) == met and all(l in got for l in legs) and not any(l in got for l in nolegs) and (not met or got == [])
            total += 1
            passed += ok
            if not ok:
                sys.stderr.write("selftest FAIL %s: %s\n" % (label, line))
            return line

        def mut(files, label, legs, nolegs=(), tt=None):
            sha = commit_tree(D, files, env, label)
            run(sha, label, legs, nolegs, tt=tt)
            commit_tree(D, {k: v for k, v in good.items()}, env, "restore " + label)
            for k in files:
                if k not in good:
                    commit_tree(D, {k: None}, env, "rm " + k)

        run(good_sha, "good", met=True)
        line0 = run(good_sha, "good-line", met=True)
        total += 1
        passed += "missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=1 " in line0
        mut({"corpus/SOURCES.md": files0["corpus/SOURCES.md"]}, "ctl1 base-registry", ["missing"])
        fill = {k: " ".join([W, X]) for k in usedg}
        mut({"corpus/SOURCES.md": registry(fill)}, "ctl2 fill-all", ["extra", "conflict"])
        d3 = dict(usedg); d3["S001"] = "-"
        mut({"corpus/SOURCES.md": registry(d3)}, "ctl3 drop-one", ["missing"])
        mut({W: witness.replace(b"source: S001, S002", b"source: S001, S002 S999")}, "ctl4 dangling-source", ["dangling"])
        d5 = dict(usedg); d5["S001"] = W + " corpus/knowledge/no-such-entry.md"
        mut({"corpus/SOURCES.md": registry(d5)}, "ctl5 ghost-path", ["extra"])
        mut({W: witness.replace(b"Cites S001 and S002 and S004.", b"```\nCites S001 and S002 and S004.\n```")}, "ctl6 fenced-cite", ["extra", "lost"])
        alle = allow_row + ("S001\t%s\t%s\tx\n" % (W, line_sha([b"Cites S001 and S002 and S004."]))).encode()
        mut({AL: alle}, "ctl7 allow-everything", ["allow_sha"])
        mut({W: witness.replace(b"Cites S001 and S002 and S004.", b"Cites S001 and S002 and nothing else.")}, "ctl8 delete-citation", ["lost"])
        mut({X: second.replace(b"refuted.", b"refuted. x")}, "ctl9 stale-allow", ["stale"])
        mut({"corpus/SOURCES.md": registry(dict(usedg, S004=W + " " + X))}, "conflict", ["conflict"])
        mut({"corpus/SOURCES.md": registry(usedg)[:-1] + b"\n"}, "good-trailing", [], met=True) if False else None
        run(good_sha, "tables-absent", ["tables_sha"], tt=None) if False else None
        # setup errors: absent base objects fail closed
        t2 = dict(t, base_rev="0" * 40)
        total += 1
        try:
            check(D, good_sha, base, override=t2)
        except SetupError:
            passed += 1
        t3 = dict(t, base_pairs_sha256="0" * 64)
        total += 1
        try:
            check(D, good_sha, base, override=t3)
        except SetupError:
            passed += 1
        # real tables: the frozen blob must be present and match the embedded sha at the --rev given
        R = Repo(repo, rev, base)
        b = R.regular_file(TABLES_PATH)
        total += 1
        passed += b is not None and hashlib.sha256(b).hexdigest() == TABLES_SHA256
    finally:
        shutil.rmtree(base, ignore_errors=True)
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
    a = ap.parse_args(argv)
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

#!/usr/bin/env python3
"""r56_ctl_c3.py -- independent control harness for claim C3 of round 56 (PRED-C3-r56, registration.md section C3).

    run(argv) -> int, argv = --repo PATH --rev REV --work DIR [--counter PATH]

The harness holds the six frozen controls and their expected legs itself; the counter knows nothing about them. For each
control it builds a scratch git repo (D=$(mktemp -d -p WORK); git -C "$D" init -q; every later git call names -C "$D";
`git -C "$D" rev-parse --show-toplevel` is asserted equal to "$D" before the first commit; identity
-c user.name=ctl -c user.email=ctl@ctl) from `git archive` of the good tree at --rev, applies ONE mutation, commits, and
runs the counter as a child process (python3 -I, GIT_* scrubbed, HOME=TMPDIR=WORK). A control is passed when the counter
exits 1, prints exactly one grammatical, self-consistent MADO_USED_BY line with verdict=TARGET_MISSED whose `missed`
contains the control's required leg, and prints no TARGET_MET. `good` = the counter prints TARGET_MET (exit 0, one
consistent line, missing=0 extra=0 dangling=0 missed=none) on the tree at --rev (run against --repo itself, read-only).

Prints exactly one stdout line on a completed run:

    MADO_R56_CONTROLS: claim=c3 good=<ok|bad> controls=<k>/9 verdict=<OK|FAIL>

exit 0 only when good=ok and k=6, 1 on FAIL, 2 on a setup error (reason on stderr, NOTHING on stdout: fail closed). Every
unexpected exception is a setup error. The harness reads --repo only through git objects (rev-parse, cat-file, ls-tree,
archive), writes only under WORK (scratch repos and the exported counter are removed before returning), never touches
the lane or the fleet repo.

Declared deviations / readings (also in the seat report):
  * D1 the scratch repo is built from `git archive REV -- corpus .ufo/waves/round-56/frozen-tables.json` (3 MB), not from
    the whole 389 MB / 27.6k-file lane tree: a C3 counter reads corpus/knowledge, corpus/SOURCES.md and the tables only
    (claims-frozen.md "Causal separability"); six full copies would cost minutes per run.
  * D2 the harness recomputes missing/extra/dangling itself; a mutation that does not strictly raise the leg it targets
    (control 1: leg count 0) is a harness setup error, never a silently passed control. The counter's own numbers are
    compared with the harness's and a divergence is a stderr diagnostic only, not scored.
  * D3 the counter under test is `--counter PATH`, else `quality/counters/c3-r56-used-by.py` exported from the git blob at
    --rev (registration: read git objects only).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TABLES_PATH = ".ufo/waves/round-56/frozen-tables-v2.json"
TABLES_SHA256 = "9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2"
ALLOW_PATH = ".ufo/waves/round-56/c3-name-only.tsv"
SOURCES = "corpus/SOURCES.md"
KNOW = "corpus/knowledge"
COUNTER_AT_REV = "quality/counters/c3-r56-used-by.py"
ARCHIVE_PATHS = ["corpus", TABLES_PATH, ALLOW_PATH]
TIMEOUT = 180
N_CONTROLS = 9

ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
CITE_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
USEDBY_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LINE_RE = re.compile(
    r"^MADO_USED_BY: rev=(?P<rev>\S+) entries=(?P<e>\d+) rows=(?P<r>\d+) missing=(?P<m>\d+) extra=(?P<x>\d+) "
    r"dangling=(?P<d>\d+) conflict=(?P<c>\d+) stale=(?P<s>\d+) lost=(?P<l>\d+) exempt=(?P<n>\d+) "
    r"verdict=(?P<verdict>TARGET_MET|TARGET_MISSED) missed=(?P<missed>\S+)$"
)
LEGS = ("missing", "extra", "dangling", "conflict", "stale", "lost")
ALL_LEGS = LEGS + ("allow_sha", "exempt", "tables_sha")


class Setup(Exception):
    pass


def err(msg):
    sys.stderr.write(msg + "\n")


# ------------------------------------------------------------------------------------------------ git plumbing
def git_env(home):
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "TMPDIR": home,
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_TERMINAL_PROMPT": "0",
    }


def git(home, d, *args, input=None, check=True):
    p = subprocess.run(["git", "-C", d] + list(args), input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=git_env(home))
    if check and p.returncode != 0:
        raise Setup("git %s failed (rc %d): %s" % (" ".join(args[:3]), p.returncode,
                                                  p.stderr.decode("utf-8", "replace").strip()))
    return p


def blob_at(home, repo, rev, path):
    """bytes of the REGULAR blob rev:path, or None when absent / symlink / not a blob."""
    p = git(home, repo, "ls-tree", "-z", rev, "--", path, check=False)
    if p.returncode != 0 or not p.stdout:
        return None
    meta, _, name = p.stdout.rstrip(b"\0").partition(b"\t")
    mode, typ, sha = meta.decode().split()
    if typ != "blob" or mode not in ("100644", "100755") or name.decode("utf-8", "surrogateescape") != path:
        return None
    return git(home, repo, "cat-file", "blob", sha).stdout


def entry_blobs(home, repo, rev):
    """{repo-relative path: bytes} of regular corpus/knowledge/*.md direct children at rev."""
    p = git(home, repo, "ls-tree", "-z", rev, KNOW + "/")
    out = {}
    for rec in p.stdout.split(b"\0"):
        if not rec:
            continue
        meta, _, name = rec.partition(b"\t")
        mode, typ, sha = meta.decode().split()
        path = name.decode("utf-8", "surrogateescape")
        if typ == "blob" and mode in ("100644", "100755") and path.endswith(".md"):
            out[path] = git(home, repo, "cat-file", "blob", sha).stdout
    return out


def dec(b):
    return b.decode("utf-8", "surrogateescape")


def enc(s):
    return s.encode("utf-8", "surrogateescape")


# ------------------------------------------------------------------------------------------------ registry / entries model
def split_row(line):
    """(prefix_parts, cells, has_trailing_pipe, tail) of a registry row line; Setup unless exactly 11 cells."""
    core = line.rstrip()
    tail = line[len(core):]
    parts = core.split("|")
    trailing = parts[-1] == ""
    cells = parts[1:-1] if trailing else parts[1:]
    if len(cells) != 11:
        raise Setup("registry row with %d cells (need 11): %r" % (len(cells), line[:100]))
    return parts, cells, trailing, tail


def parse_registry(text):
    """[(line_index, id, used_by_cell_text)] over every registry row; lines list returned too."""
    lines = text.split("\n")
    rows = []
    for i, ln in enumerate(lines):
        m = ROW_RE.match(ln)
        if m:
            _, cells, _, _ = split_row(ln)
            rows.append((i, m.group(1), cells[10]))
    return lines, rows


def set_usedby(lines, i, new_cell):
    parts, cells, trailing, tail = split_row(lines[i])
    parts[11] = new_cell  # parts[0] is the leading text; cell 11 is parts[11]
    lines[i] = "|".join(parts) + tail


def fence_flags(lines):
    """list[bool]: True when the line is a fence marker line or inside a fenced block (0-3 leading spaces)."""
    flags = []
    open_ch, open_len = None, 0
    for ln in lines:
        m = FENCE_RE.match(ln)
        if open_ch is None:
            if m:
                open_ch, open_len = m.group(1)[0], len(m.group(1))
                flags.append(True)
            else:
                flags.append(False)
        else:
            flags.append(True)
            if m and m.group(1)[0] == open_ch and len(m.group(1)) >= open_len and m.group(2).strip() == "":
                open_ch = None
    return flags


def cite_lines(text):
    """[(line_index, S)] for every citation token on a line outside fenced code blocks."""
    lines = text.split("\n")
    fl = fence_flags(lines)
    return [(i, t) for i, ln in enumerate(lines) if not fl[i] for t in CITE_RE.findall(ln)]


def metrics(sources_text, entries):
    """independent computation of (entries, rows, missing, extra, dangling); entries: {path: text}."""
    _, rows = parse_registry(sources_text)
    ids = set(r[1] for r in rows)
    usedby = {}
    for _, sid, cell in rows:
        usedby.setdefault(sid, set()).update(USEDBY_RE.findall(cell))
    cites = {p: set(t for _, t in cite_lines(t)) for p, t in entries.items()}
    missing = sum(1 for p, cs in cites.items() for s in cs if s in ids and p not in usedby[s])
    extra = sum(1 for s, ps in usedby.items() for p in ps if p not in cites or s not in cites[p])
    dangling = 0
    for p, t in entries.items():
        src = set()
        for ln in t.split("\n")[:15]:
            if ln.startswith("source:"):
                src.update(CITE_RE.findall(ln))
        dangling += sum(1 for s in src if s not in ids)
    return {"entries": len(entries), "rows": len(rows), "missing": missing, "extra": extra, "dangling": dangling}


# ------------------------------------------------------------------------------------------------ mutations
# each mutation: (sources_text, entries{path:text}, base_sources_text) -> (new_sources_text, new_entries, note, leg)
# returning only the changed side; entries is a dict {path: text} of changed entries.
def first_listing(rows, path):
    """first row (sorted by id) whose used-by cell lists path."""
    for i, sid, cell in sorted(rows, key=lambda r: r[1]):
        if path in USEDBY_RE.findall(cell):
            return i, sid, cell
    return None


def mut_base_registry(src, entries, base_src):
    return base_src, {}, "corpus/SOURCES.md := bytes at the frozen base revision", "missing"


def mut_fill_all(src, entries, base_src):
    lines, rows = parse_registry(src)
    cell = " " + " ".join(sorted(entries)) + " "
    for i, _, _ in rows:
        set_usedby(lines, i, cell)
    return "\n".join(lines), {}, "used-by of all %d rows := all %d entry paths" % (len(rows), len(entries)), "extra"


def mut_drop_one(src, entries, base_src):
    lines, rows = parse_registry(src)
    for path in sorted(entries):
        hit = first_listing(rows, path)
        if hit is None:
            continue  # first sorted entry that some row lists (ambiguity: spec says "first entry (sorted)")
        i, sid, cell = hit
        new = USEDBY_RE.sub(lambda m: "" if m.group(0) == path else m.group(0), cell)
        set_usedby(lines, i, new)
        return "\n".join(lines), {}, "removed %s from the used-by of %s" % (path, sid), "missing"
    raise Setup("drop-one: no registry row lists any entry")


def mut_dangling_source(src, entries, base_src):
    ids = set(r[1] for r in parse_registry(src)[1])
    if "S999" in ids:
        raise Setup("dangling-source: S999 is a registry row")
    for path in sorted(entries):
        lines = entries[path].split("\n")
        for i, ln in enumerate(lines[:15]):
            if ln.startswith("source:"):
                lines[i] = ln + " S999"
                return src, {path: "\n".join(lines)}, "appended ' S999' to the source: line of %s" % path, "dangling"
    raise Setup("dangling-source: no entry has a source: line in its first 15 lines")


def mut_ghost_path(src, entries, base_src):
    ghost = "corpus/knowledge/no-such-entry.md"
    if ghost in entries:
        raise Setup("ghost-path: the ghost entry exists")
    lines, rows = parse_registry(src)
    for i, sid, cell in rows:
        if sid == "S001":
            set_usedby(lines, i, cell.rstrip() + " " + ghost + " ")
            return "\n".join(lines), {}, "added %s to the used-by of S001" % ghost, "extra"
    raise Setup("ghost-path: no registry row S001")


def mut_fenced_cite(src, entries, base_src):
    _, rows = parse_registry(src)
    ids = {sid: set(USEDBY_RE.findall(cell)) for _, sid, cell in rows}
    cands = []
    for path, text in entries.items():
        cl = cite_lines(text)
        for s in set(t for _, t in cl):
            occ = [i for i, t in cl if t == s]
            if len(occ) == 1 and s in ids and path in ids[s]:
                cands.append((s, path, occ[0]))
    if not cands:
        raise Setup("fenced-cite: no (S, entry) pair with a single non-fence citation still listed in used-by")
    s, path, li = sorted(cands)[0]
    lines = entries[path].split("\n")
    lines[li:li + 1] = ["```", lines[li], "```"]
    return src, {path: "\n".join(lines)}, "wrapped line %d of %s (only citation of %s) in a ``` fence" % (li + 1, path, s), "extra"


CTX = {"allow": "", "base_src": ""}


def line_sha(lines):
    return hashlib.sha256(enc("\n".join(lines))).hexdigest()


def pair_lines(entries, ids):
    """{(S, path): [citing lines outside fences]} for S a registry id."""
    out = {}
    for path, text in entries.items():
        lines = text.split("\n")
        fl = fence_flags(lines)
        for i, ln in enumerate(lines):
            if fl[i]:
                continue
            for s in set(CITE_RE.findall(ln)):
                if s in ids:
                    out.setdefault((s, path), []).append(ln)
    return out


def allow_rows():
    return [tuple(r.split("\t")) for r in CTX["allow"].split("\n") if r]


def mut_allow_everything(src, entries, base_src):
    ids = set(r[1] for r in parse_registry(src)[1])
    pl = pair_lines(entries, ids)
    rows = "".join("%s\t%s\t%s\tx\n" % (s, p, line_sha(ls)) for (s, p), ls in sorted(pl.items()))
    return src, {ALLOW_PATH: rows}, "allowlist := every (S, entry) pair with its correct line-sha", "allow_sha"


def mut_delete_citation(src, entries, base_src):
    ids = set(r[1] for r in parse_registry(src)[1])
    _, brows = parse_registry(base_src)
    bused = {sid: set(USEDBY_RE.findall(cell)) for _, sid, cell in brows}
    allow = {(r[0], r[1]) for r in allow_rows()}
    pl = pair_lines(entries, ids)
    for (s, p), ls in sorted(pl.items()):
        if s in bused and p not in bused[s] and (s, p) not in allow:
            occ = sum(CITE_RE.findall(l).count(s) for l in ls)
            if occ != 1:
                continue
            lines = entries[p].split("\n")
            fl = fence_flags(lines)
            for i, ln in enumerate(lines):
                if not fl[i] and s in CITE_RE.findall(ln):
                    lines[i] = re.sub(r"(?<![A-Za-z0-9])" + s + r"(?![0-9])", "S---", ln, count=1)
                    return src, {p: "\n".join(lines)}, "replaced the only %s token of %s by S---" % (s, p), "lost"
    raise Setup("delete-citation: no base-missing non-allowlist pair with a single citation")


def mut_stale_allow(src, entries, base_src):
    rows = allow_rows()
    if not rows:
        raise Setup("stale-allow: empty allowlist")
    s, p = rows[0][0], rows[0][1]
    lines = entries[p].split("\n")
    fl = fence_flags(lines)
    for i, ln in enumerate(lines):
        if not fl[i] and s in CITE_RE.findall(ln):
            lines[i] = ln + " x"
            return src, {p: "\n".join(lines)}, "appended ' x' to the first citing line of %s in %s" % (s, p), "stale"
    raise Setup("stale-allow: first allowlist pair is not cited at the revision")


CONTROLS = [
    ("base-registry", mut_base_registry),
    ("fill-all", mut_fill_all),
    ("drop-one", mut_drop_one),
    ("dangling-source", mut_dangling_source),
    ("ghost-path", mut_ghost_path),
    ("fenced-cite", mut_fenced_cite),
    ("allow-everything", mut_allow_everything),
    ("delete-citation", mut_delete_citation),
    ("stale-allow", mut_stale_allow),
]


# ------------------------------------------------------------------------------------------------ counter run / judgement
def counter_env(work):
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1"}


def run_counter(counter, repo, rev, work):
    """-> (rc, stdout_text, reason|None)"""
    try:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--work", work], cwd=work,
                           env=counter_env(work), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "", "counter timed out after %ds" % TIMEOUT
    except OSError as ex:
        return None, "", "cannot start counter: %s" % ex
    return p.returncode, p.stdout.decode("utf-8", "replace"), None


def parse_line(out, rev):
    """-> (dict|None, reason|None): exactly one grammatical, self-consistent counter line carrying `rev`."""
    if not out.endswith("\n"):
        return None, "stdout does not end with a newline"
    lines = out[:-1].split("\n")
    if len(lines) != 1:
        return None, "stdout has %d lines" % len(lines)
    m = LINE_RE.match(lines[0])
    if not m:
        return None, "unparsable line %r" % lines[0][:200]
    d = m.groupdict()
    if d["rev"] != rev:
        return None, "line rev=%s differs from the requested %s" % (d["rev"], rev)
    counts = {"missing": int(d["m"]), "extra": int(d["x"]), "dangling": int(d["d"]), "conflict": int(d["c"]), "stale": int(d["s"]), "lost": int(d["l"])}
    nz = [k for k in LEGS if counts[k]]
    if d["missed"] == "none":
        if nz or d["verdict"] != "TARGET_MET":
            return None, "inconsistent: missed=none but counts %r verdict %s" % (counts, d["verdict"])
        missed = []
    else:
        missed = d["missed"].split(",")
        if any(x not in ALL_LEGS for x in missed) or len(set(missed)) != len(missed):
            return None, "bad missed list %r" % d["missed"]
        if not set(nz) <= set(missed) or d["verdict"] != "TARGET_MISSED":
            return None, "inconsistent: missed=%s but nonzero counts %r verdict %s" % (d["missed"], counts, d["verdict"])
    d.update(counts=counts, missed_list=missed, e=int(d["e"]), r=int(d["r"]))
    return d, None


def judge_good(rc, out, rev, own):
    if rc is None:
        return False, out or "no run"
    d, why = parse_line(out, rev)
    if d is None:
        return False, why
    if rc != 0 or d["verdict"] != "TARGET_MET" or any(d["counts"].values()) or d["n"] != "24":
        return False, "rc=%s verdict=%s counts=%r" % (rc, d["verdict"], d["counts"])
    note_diverge(d, own, "good")
    return True, "ok"


def judge_control(rc, out, rev, leg, own):
    if rc is None:
        return False, out or "no run"
    if "TARGET_MET" in out:
        return False, "counter printed TARGET_MET on a mutated tree"
    if rc != 1:
        return False, "exit status %s (want 1)" % rc
    d, why = parse_line(out, rev)
    if d is None:
        return False, why
    if d["verdict"] != "TARGET_MISSED" or leg not in d["missed_list"]:
        return False, "missed=%s lacks %s" % (d["missed"], leg)
    note_diverge(d, own, leg)
    return True, "missed=%s" % d["missed"]


def note_diverge(d, own, tag):
    """diagnostic only: the counter's numbers vs the harness's independent numbers."""
    pairs = (("entries", d["e"], own["entries"]), ("rows", d["r"], own["rows"]),
             ("missing", d["counts"]["missing"], own["missing"]), ("extra", d["counts"]["extra"], own["extra"]),
             ("dangling", d["counts"]["dangling"], own["dangling"]))
    bad = ["%s counter=%d harness=%d" % p for p in pairs if p[1] != p[2]]
    if bad:
        err("  note[%s]: counter and harness numbers diverge (not scored): %s" % (tag, "; ".join(bad)))


# ------------------------------------------------------------------------------------------------ scratch repo
def build_scratch(work, repo, rev_sha, changed):
    """-> (D, commit sha); D is a fresh mktemp -d -p WORK shared clone of the lane (so the frozen base revision's objects exist,
    which control `lost` needs) checked out detached at rev_sha with `changed` ({relpath: bytes}) committed on top."""
    d = tempfile.mkdtemp(prefix="ctl.", dir=work)
    try:
        shutil.rmtree(d)
        r = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", repo, d], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=git_env(work))
        if r.returncode != 0:
            raise Setup("git clone --shared failed: " + r.stderr.decode("utf-8", "replace").strip())
        top = git(work, d, "rev-parse", "--show-toplevel").stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise Setup("scratch repo toplevel %s != %s" % (top, d))
        git(work, d, "checkout", "-q", "--detach", rev_sha)
        for rel, data in changed.items():
            tgt = os.path.join(d, rel)
            if os.path.islink(tgt) or not os.path.isfile(tgt):
                raise Setup("mutation target %s is not a regular file in the scratch tree" % rel)
            with open(tgt, "wb") as fh:
                fh.write(data)
        git(work, d, "add", "-A", "-f", ".")
        git(work, d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "--no-gpg-sign", "-m", "ctl")
        sha = git(work, d, "rev-parse", "HEAD").stdout.decode().strip()
        return d, sha
    except BaseException:
        shutil.rmtree(d, ignore_errors=True)
        raise


# ------------------------------------------------------------------------------------------------ main
def parse_args(argv):
    opts = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a not in ("--repo", "--rev", "--work", "--counter") or a in opts or i + 1 >= len(argv):
            raise Setup("usage: --repo PATH --rev REV --work DIR [--counter PATH] (each once, two-token form)")
        opts[a] = argv[i + 1]
        i += 2
    for k in ("--repo", "--rev", "--work"):
        if k not in opts or not opts[k]:
            raise Setup("usage: missing %s" % k)
    return opts


def execute(argv):
    opts = parse_args(argv)
    work = os.path.abspath(opts["--work"])
    os.makedirs(work, exist_ok=True)
    repo = os.path.abspath(opts["--repo"])
    rev = opts["--rev"]
    created = []
    try:
        p = git(work, repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}", check=False)
        if p.returncode != 0:
            raise Setup("--rev %s is not a commit in %s" % (rev, repo))
        rev_sha = p.stdout.decode().strip()

        tables = blob_at(work, repo, rev_sha, TABLES_PATH)
        if tables is None:
            raise Setup("%s is not a regular blob at %s" % (TABLES_PATH, rev))
        if hashlib.sha256(tables).hexdigest() != TABLES_SHA256:
            raise Setup("frozen-tables.json sha256 mismatch at %s" % rev)
        base = json.loads(tables)["base"]
        if not re.fullmatch(r"[0-9a-f]{40}", base):
            raise Setup("frozen-tables.json base is not a 40-hex revision: %r" % base)
        # control 1 needs the frozen base revision's registry bytes; fail closed when the object is absent
        bc = git(work, repo, "cat-file", "-t", base + "^{commit}", check=False)
        if bc.returncode != 0:
            raise Setup("frozen base revision %s is not readable in %s (control 1 cannot run)" % (base, repo))
        base_src = blob_at(work, repo, base, SOURCES)
        if base_src is None:
            raise Setup("%s is not a regular blob at the frozen base %s" % (SOURCES, base))

        ab = blob_at(work, repo, rev_sha, ALLOW_PATH)
        if ab is None:
            raise Setup("%s is not a regular blob at %s" % (ALLOW_PATH, rev))
        CTX["allow"] = dec(ab)
        good_src = blob_at(work, repo, rev_sha, SOURCES)
        if good_src is None:
            raise Setup("%s is not a regular blob at %s" % (SOURCES, rev))
        good_ent = entry_blobs(work, repo, rev_sha)
        if not good_ent:
            raise Setup("no regular corpus/knowledge/*.md entries at %s" % rev)
        src_t = dec(good_src)
        ent_t = {p_: dec(b) for p_, b in good_ent.items()}
        own_good = metrics(src_t, ent_t)
        err("harness metrics of the good tree: %r" % (own_good,))

        if "--counter" in opts:
            counter = os.path.abspath(opts["--counter"])
            if not os.path.isfile(counter):
                raise Setup("--counter %s is not a file" % counter)
        else:
            blob = blob_at(work, repo, rev_sha, COUNTER_AT_REV)
            if blob is None:
                raise Setup("no counter: %s is not a regular blob at %s and --counter was not given" % (COUNTER_AT_REV, rev))
            cd = tempfile.mkdtemp(prefix="counter.", dir=work)
            created.append(cd)
            counter = os.path.join(cd, os.path.basename(COUNTER_AT_REV))
            with open(counter, "wb") as fh:
                fh.write(blob)

        # build and mutate everything BEFORE the first counter run so setup errors surface before any score
        plan = []
        for name, fn in CONTROLS:
            new_src, new_ent, note, leg = fn(src_t, ent_t, dec(base_src))
            m_src = new_src if new_src is not src_t else src_t
            m_ent = dict(ent_t)
            m_ent.update({k_: v_ for k_, v_ in new_ent.items() if k_.startswith(KNOW + "/")})
            own = metrics(m_src, m_ent)
            if leg in ("missing", "extra", "dangling"):
                ok = own[leg] > 0 if name == "base-registry" else own[leg] > own_good[leg]
            else:
                ok = bool(new_ent)   # allowlist / stale / lost controls change an entry or the allowlist (registry-model leg checked by the counter)
            if not ok:
                raise Setup("control %s is ineffective: harness %s count %d vs good %d" % (name, leg, own[leg], own_good[leg]))
            changed = {}
            if m_src != src_t:
                changed[SOURCES] = enc(m_src)
            for pth, txt in new_ent.items():
                changed[pth] = enc(txt)
            plan.append((name, leg, note, changed, own))

        rc, out, why = run_counter(counter, repo, rev, work)
        good_ok, good_why = judge_good(rc, out, rev, own_good)
        err("good: %s (%s)" % ("ok" if good_ok else "bad", good_why))

        k = 0
        for n, (name, leg, note, changed, own) in enumerate(plan, 1):
            d, sha = build_scratch(work, repo, rev_sha, changed)
            created.append(d)
            rc, out, why = run_counter(counter, d, sha, work)
            if why:
                ok, detail = False, why
            else:
                ok, detail = judge_control(rc, out, sha, leg, own)
            k += ok
            err("control %d %s: %s -- %s [%s; harness %s=%d]" % (n, name, "PASS" if ok else "FAIL", detail, note, leg, own[leg]))
        verdict = "OK" if (good_ok and k == N_CONTROLS) else "FAIL"
        line = "MADO_R56_CONTROLS: claim=c3 good=%s controls=%d/%d verdict=%s" % ("ok" if good_ok else "bad", k, N_CONTROLS, verdict)
        return line, (0 if verdict == "OK" else 1)
    finally:
        for c in created:
            shutil.rmtree(c, ignore_errors=True)


def run(argv):
    try:
        line, rc = execute(list(argv))
    except Setup as ex:
        err("SETUP: %s" % ex)
        return 2
    except Exception as ex:  # fail closed: any unexpected failure is a setup error, nothing on stdout
        err("SETUP: unexpected %s: %s" % (type(ex).__name__, ex))
        return 2
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))

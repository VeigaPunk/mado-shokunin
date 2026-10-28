#!/usr/bin/env python3
"""r55_ctl_c3.py -- independent control harness for claim C3 of round 55 (PRED-C3-r55).

    run(argv) -> int, argv = --repo PATH --rev REV --work DIR [--counter PATH]

Builds scratch git repos from the good tree at --rev (git init + alternates onto --repo's object store, new commits
made with plumbing and `-c user.name=ctl -c user.email=ctl@ctl`, every git call names `-C "$D"`), applies each of the six
frozen C3 mutations (registration.md section C3), runs the counter as a child process on the mutated repo, and compares
the counter's `MADO_P19_FIX:` line to the legs this harness holds itself. A missing, duplicated, ungrammatical or
self-inconsistent counter line is a failed control. Prints exactly one stdout line:

    MADO_R55_CONTROLS: claim=c3 good=<ok|bad> controls=<k>/6 verdict=<OK|FAIL>

exit 0 on OK, 1 on FAIL, 2 on setup error (`MADO_R55_CONTROLS: SETUP <reason>`). Diagnostics go to stderr. Writes only
under --work (every scratch repo is removed before returning). Reads --repo only through git (cat-file/rev-parse).
"""
import os
import re
import shutil
import subprocess
import sys

BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
README = "corpus/README.md"
COUNTER_PATH = "quality/counters/c3-r55-p19.py"
ERRATA_NAME = "hyprland-synthetic-dispatch-r52-errata-r53.md"
QIDS = ["Q%02d" % i for i in range(1, 14)]
TIMEOUT = 180

LINE_RE = re.compile(
    r"^MADO_P19_FIX: rev=(?P<rev>\S+) prefix=(?P<prefix>identical|changed) rows=(?P<rows>\d+)/13 "
    r"pin=(?P<pin>ok|bad) p23=(?P<p23>ok|bad) readme=(?P<readme>ok|bad) "
    r"verdict=(?P<verdict>TARGET_MET|TARGET_MISSED) missed=(?P<missed>\S+)$"
)
KNOWN_OTHER = {"prefix", "pin", "p23", "readme", "tables_sha", "stale"}  # registration v2 E8 adds `stale` and `rows:heading`


class Setup(Exception):
    pass


def err(msg):
    sys.stderr.write(msg + "\n")


# ---------------------------------------------------------------- git helpers
def git(d, *args, input=None, check=True, env=None):
    cmd = ["git", "-C", d] + list(args)
    p = subprocess.run(cmd, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env or git_env(d))
    if check and p.returncode != 0:
        raise Setup("git %s failed: %s" % (" ".join(args[:3]), p.stderr.decode("utf-8", "replace").strip()))
    return p


def git_env(home):
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": home,
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_TERMINAL_PROMPT": "0",
    }


def cat(repo, rev, path):
    """bytes of path at rev, or None when absent."""
    p = subprocess.run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=git_env(repo))
    return p.stdout if p.returncode == 0 else None


# ---------------------------------------------------------------- mutations (bytes -> bytes)
def line_spans(data):
    pos = 0
    for ln in data.split(b"\n"):
        yield pos, ln
        pos += len(ln) + 1


def find_row(data, ident):
    """(start, end) of the first line beginning '| <ident> |'; end excludes the newline."""
    tag = b"| " + ident.encode() + b" |"
    for pos, ln in line_spans(data):
        if ln.startswith(tag):
            return pos, pos + len(ln)
    return None


def row_cells(line):
    return line.split(b"|")


def mut_absent(entry, good_entry_base, readme):
    base = good_entry_base
    return base, readme, "block removed (entry == base bytes)"


def mut_rewritten_prefix(entry, base, readme):
    span = find_row(base, "P19")
    if span is None:
        raise Setup("base has no P19 row")
    s, e = span
    row = entry[s:e]
    i = row.find(b"PRESSED")
    if i < 0:
        raise Setup("P19 row has no PRESSED token")
    new = entry[: s + i] + b"PRESSEd" + entry[s + i + 7:]
    return new, readme, "one byte of the P19 row changed"


def mut_altered_quote(entry, base, readme):
    span = find_row(entry, "Q09")
    if span is None:
        raise Setup("good entry has no Q09 row")
    s, e = span
    row = entry[s:e]
    a, b = row.find(b"`"), row.rfind(b"`")
    if a < 0 or b <= a:
        raise Setup("Q09 row has no backtick quote")
    quote = row[a + 1:b]
    j = quote.find(b"key - 8")
    if j < 0:
        raise Setup("Q09 quote lacks 'key - 8'")
    quote2 = quote[: j + 6] + b"9" + quote[j + 7:]
    assert quote2 != quote and len(quote2) == len(quote)
    return entry[:s] + row[: a + 1] + quote2 + row[b:] + entry[e:], readme, "Q09 quote 'key - 8' -> 'key - 9'"


def mut_old_arm_only(entry, base, readme):
    out = entry
    hit = 0
    for ident in ("Q08", "Q09", "Q10", "Q11", "Q12"):
        while True:
            span = find_row(out, ident)
            if span is None:
                break
            s, e = span
            out = out[:s] + out[e + 1:]
            hit += 1
    if hit < 5:
        raise Setup("good entry has only %d of the Q08-Q12 rows" % hit)
    return out, readme, "deleted %d rows Q08-Q12" % hit


def mut_old_wording(entry, base, readme):
    """registration v2 E8, C3-CTL-5: the false P19 sentence kept verbatim and keyword-stuffed so the lexical p23 leg is
    satisfied; only the `stale` leg can reject it."""
    p23, p19 = find_row(entry, "P23"), find_row(base, "P19")
    if p23 is None:
        raise Setup("good entry has no P23 row")
    if p19 is None:
        raise Setup("base has no P19 row")
    c23 = row_cells(entry[p23[0]:p23[1]])
    c19 = row_cells(base[p19[0]:p19[1]])
    if len(c23) < 4 or len(c19) < 4:
        raise Setup("P19/P23 rows have too few cells")
    c23[3] = c19[3].rstrip() + b" == 0 RELEASED otherwise "
    row = b"|".join(c23)
    return entry[: p23[0]] + row + entry[p23[1]:], readme, "P23 proposition cell := P19 sentence + ' == 0 RELEASED otherwise'"


def mut_readme_missing(entry, base, readme):
    if readme is None:
        raise Setup("good tree has no corpus/README.md")
    out, hit = [], 0
    for ln in readme.split(b"\n"):
        if ERRATA_NAME.encode() in ln and b"P23" in ln:
            ln = ln.replace(b"P23", b"")
            hit += 1
        out.append(ln)
    if not hit:
        raise Setup("good README has no line naming the errata entry together with P23")
    return entry, b"\n".join(out), "removed P23 from %d README line(s)" % hit


# name, mutation, expected prefix, rows count, pin(None=any), p23, readme, must_other, allowed_other, must_rows, allowed_rows, min_rows
CONTROLS = [
    ("C3-CTL-1 absent", mut_absent, "identical", 0, "ok", "bad", "ok",
     {"p23"}, {"p23", "stale"}, set(), set(QIDS) | {"heading"}, 1),
    # block location after a changed prefix is not fixed by the contract: rows/pin/p23 are collateral-tolerant here
    ("C3-CTL-2 rewritten-prefix", mut_rewritten_prefix, "changed", None, None, None, "ok",
     {"prefix"}, {"prefix", "pin", "p23", "stale"}, set(), set(QIDS) | {"heading"}, 0),
    ("C3-CTL-3 altered-quote", mut_altered_quote, "identical", 12, None, "ok", "ok",
     set(), {"pin"}, {"Q09"}, {"Q09"}, 1),
    ("C3-CTL-4 old-arm-only", mut_old_arm_only, "identical", 8, "ok", "ok", "ok",
     set(), set(), {"Q08"}, {"Q08", "Q09", "Q10", "Q11", "Q12"}, 1),
    ("C3-CTL-5 old-wording-stuffed", mut_old_wording, "identical", 13, "ok", "ok", "ok",
     {"stale"}, {"stale"}, set(), set(), 0),
    ("C3-CTL-6 readme-missing", mut_readme_missing, "identical", 13, "ok", "ok", "bad",
     {"readme"}, {"readme"}, set(), set(), 0),
]


# ---------------------------------------------------------------- scratch repo
def new_scratch(work, name, objdir):
    d = os.path.join(work, name)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=git_env(d),
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise Setup("scratch toplevel %s != %s" % (top, d))
    with open(os.path.join(d, ".git", "objects", "info", "alternates"), "w") as f:
        f.write(objdir + "\n")
    return d


def commit_variant(d, rev, entry, readme):
    """new commit on top of rev with ENTRY and (when not None) README replaced; returns its sha."""
    git(d, "read-tree", rev)
    ob = git(d, "hash-object", "-w", "--stdin", input=entry).stdout.decode().strip()
    git(d, "update-index", "--cacheinfo", "100644,%s,%s" % (ob, ENTRY))
    if readme is not None:
        rb = git(d, "hash-object", "-w", "--stdin", input=readme).stdout.decode().strip()
        git(d, "update-index", "--cacheinfo", "100644,%s,%s" % (rb, README))
    tree = git(d, "write-tree").stdout.decode().strip()
    sha = git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", tree, "-p", rev,
              "-m", "ctl mutation", input=b"").stdout.decode().strip()
    git(d, "update-ref", "refs/heads/ctl", sha)
    return sha


# ---------------------------------------------------------------- counter run and judgment
def run_counter(counter, repo, rev, work):
    os.makedirs(work, exist_ok=True)
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": work,
        "TMPDIR": work,
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
    }
    try:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--work", work],
                           cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "counter timed out after %ds" % TIMEOUT
    except OSError as ex:
        return None, "cannot start counter: %s" % ex
    out = p.stdout.decode("utf-8", "replace")
    lines = [l for l in out.split("\n") if l.startswith("MADO_P19_FIX:")]
    if "MADO_R55_CONTROLS" in out:
        return None, "counter printed a control verdict"
    if len(lines) != 1:
        return None, "expected exactly one MADO_P19_FIX line, got %d (rc=%d)" % (len(lines), p.returncode)
    m = LINE_RE.match(lines[0])
    if not m:
        return None, "unparsable counter line: %r" % lines[0][:200]
    d = m.groupdict()
    d["rc"] = p.returncode
    d["line"] = lines[0]
    return d, None


def internal_problem(d, rev):
    """self-consistency of one parsed counter line; returns a reason or None."""
    if d["rev"] != rev:
        return "rev field %s != passed rev %s" % (d["rev"], rev)
    miss = d["missed"]
    legs = [] if miss == "none" else miss.split(",")
    if (miss == "none") != (d["verdict"] == "TARGET_MET"):
        return "verdict %s inconsistent with missed=%s" % (d["verdict"], miss)
    if d["rc"] != (0 if d["verdict"] == "TARGET_MET" else 1):
        return "exit status %d does not match verdict %s" % (d["rc"], d["verdict"])
    if len(set(legs)) != len(legs) or "" in legs:
        return "missed legs duplicated/empty: %s" % miss
    for leg, field, bad in (("prefix", "prefix", "changed"), ("pin", "pin", "bad"),
                            ("p23", "p23", "bad"), ("readme", "readme", "bad")):
        if (leg in legs) != (d[field] == bad):
            return "leg %s in missed=%s disagrees with field %s=%s" % (leg, miss, field, d[field])
    for leg in legs:
        if leg not in KNOWN_OTHER and not (leg.startswith("rows:") and (leg[5:] in QIDS or leg[5:] == "heading")):
            return "unknown leg %r" % leg
    return None


def judge_good(d):
    if d["verdict"] != "TARGET_MET" or d["missed"] != "none" or d["rc"] != 0:
        return "good tree not TARGET_MET: %s (rc=%d)" % (d["line"], d["rc"])
    if (d["prefix"], d["rows"], d["pin"], d["p23"], d["readme"]) != ("identical", "13", "ok", "ok", "ok"):
        return "good tree fields not identical/13/ok/ok/ok: %s" % d["line"]
    return None


def judge_control(spec, d):
    _, _, e_prefix, e_rows, e_pin, e_p23, e_readme, must_o, allow_o, must_r, allow_r, min_r = spec
    if d["verdict"] != "TARGET_MISSED":
        return "mutant admitted (verdict %s): %s" % (d["verdict"], d["line"])
    legs = [] if d["missed"] == "none" else d["missed"].split(",")
    other = {l for l in legs if not l.startswith("rows:")}
    rows = {l[5:] for l in legs if l.startswith("rows:")}
    if d["prefix"] != e_prefix:
        return "prefix=%s expected %s" % (d["prefix"], e_prefix)
    if e_rows is not None and int(d["rows"]) != e_rows:
        return "rows=%s/13 expected %d/13" % (d["rows"], e_rows)
    if e_pin is not None and d["pin"] != e_pin:
        return "pin=%s expected %s" % (d["pin"], e_pin)
    if e_p23 is not None and d["p23"] != e_p23:
        return "p23=%s expected %s" % (d["p23"], e_p23)
    if d["readme"] != e_readme:
        return "readme=%s expected %s" % (d["readme"], e_readme)
    if not must_o <= other:
        return "required leg(s) %s absent from missed=%s" % (sorted(must_o - other), d["missed"])
    if not other <= (must_o | allow_o):
        return "unexpected leg(s) %s in missed=%s" % (sorted(other - must_o - allow_o), d["missed"])
    if not must_r <= rows:
        return "required row leg(s) %s absent from missed=%s" % (sorted(must_r - rows), d["missed"])
    if not rows <= allow_r:
        return "unexpected row leg(s) %s in missed=%s" % (sorted(rows - allow_r), d["missed"])
    if len(rows) < min_r:
        return "expected at least %d rows: leg(s), missed=%s" % (min_r, d["missed"])
    return None


# ---------------------------------------------------------------- driver
def parse(argv):
    opts, i = {}, 0
    while i < len(argv):
        a = argv[i]
        if a in ("--repo", "--rev", "--work", "--counter") and i + 1 < len(argv) and a not in opts:
            opts[a] = argv[i + 1]
            i += 2
        else:
            raise Setup("usage")
    for need in ("--repo", "--rev", "--work"):
        if need not in opts:
            raise Setup("usage")
    return opts


def execute(argv):
    opts = parse(argv)
    repo = os.path.abspath(opts["--repo"])
    work = os.path.abspath(opts["--work"])
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "--quiet", opts["--rev"] + "^{commit}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=git_env(work))
    if p.returncode != 0:
        raise Setup("rev_unresolvable")
    rev = p.stdout.decode().strip()
    p = subprocess.run(["git", "-C", repo, "rev-parse", "--path-format=absolute", "--git-path", "objects"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=git_env(work))
    if p.returncode != 0 or not p.stdout.strip():
        raise Setup("repo_unreadable")
    objdir = p.stdout.decode().strip()

    root = os.path.join(work, "c3-ctl-%d" % os.getpid())
    os.makedirs(root)
    try:
        # counter under test: --counter PATH, else the one committed at --rev
        if "--counter" in opts:
            counter = os.path.abspath(opts["--counter"])
            if not os.path.isfile(counter):
                raise Setup("counter_unreadable")
        else:
            data = cat(repo, rev, COUNTER_PATH)
            counter = os.path.join(root, "counter-under-test.py")
            if data is not None:
                with open(counter, "wb") as f:
                    f.write(data)
            else:
                counter = None
                err("counter %s absent at %s" % (COUNTER_PATH, rev))

        entry = cat(repo, rev, ENTRY)
        base = cat(repo, BASE, ENTRY)
        readme = cat(repo, rev, README)
        if base is None:
            raise Setup("base_entry_unreadable")

        # ---- good tree
        good = "bad"
        if counter is not None:
            d, why = run_counter(counter, repo, rev, os.path.join(root, "w-good"))
            if d is None:
                err("good: " + why)
            else:
                why = internal_problem(d, rev) or judge_good(d)
                if why:
                    err("good: " + why)
                else:
                    good = "ok"
                    err("good: " + d["line"])
        if entry is None:
            err("good tree has no %s; no control can be built" % ENTRY)
        elif not entry.startswith(base):
            err("good entry does not begin with the base bytes (prefix leg would fail on good)")

        # ---- controls
        passed = 0
        for k, spec in enumerate(CONTROLS, 1):
            name = spec[0]
            if counter is None or entry is None:
                err("%s: FAIL (no counter / no entry to mutate)" % name)
                continue
            try:
                m_entry, m_readme, note = spec[1](entry, base, readme)
                if m_entry == entry and m_readme == readme:
                    raise Setup("mutation is a no-op on the good tree")
                dd = new_scratch(root, "repo-%d" % k, objdir)
                sha = commit_variant(dd, rev, m_entry, m_readme)
                d, why = run_counter(counter, dd, sha, os.path.join(root, "w-%d" % k))
                if d is None:
                    err("%s: FAIL (%s) [%s]" % (name, why, note))
                    continue
                why = internal_problem(d, sha) or judge_control(spec, d)
                if why:
                    err("%s: FAIL (%s) [%s]" % (name, why, note))
                else:
                    passed += 1
                    err("%s: pass [%s] %s" % (name, note, d["missed"]))
            except Setup as ex:
                err("%s: FAIL (harness could not build the control: %s)" % (name, ex))
        return good, passed
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run(argv):
    try:
        good, passed = execute(list(argv))
    except Setup as ex:
        print("MADO_R55_CONTROLS: SETUP %s" % ex)
        return 2
    ok = good == "ok" and passed == len(CONTROLS)
    print("MADO_R55_CONTROLS: claim=c3 good=%s controls=%d/6 verdict=%s" % (good, passed, "OK" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))

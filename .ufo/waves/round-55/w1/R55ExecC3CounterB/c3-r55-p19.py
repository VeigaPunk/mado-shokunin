#!/usr/bin/env python3
"""Round 55 C3 counter: append-only correction of the false P19 statement.

    python3 -I c3-r55-p19.py --repo <repo> --rev <rev> --work <scratch>
    python3 -I c3-r55-p19.py --selftest --repo <repo> --rev <rev> --work <scratch>

Implements registration.md section C3 and nothing else.  Every input is read
from git objects (``git cat-file blob``) of --repo, never from the working
tree: the errata entry and corpus/README.md and frozen-tables.json and the
round-52 pin at --rev, the base bytes of the entry at the frozen base commit.

stdout (check mode), exactly one line:
  MADO_P19_FIX: rev=<rev> prefix=<identical|changed> rows=<a>/13 pin=<ok|bad>
                p23=<ok|bad> readme=<ok|bad> verdict=<TARGET_MET|TARGET_MISSED>
                missed=<legs,comma>|none
Exit 0 only on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on
stderr, nothing on stdout).  --work is created if absent and handed to every
git child as TMPDIR; the counter itself writes no file.

Legs, in print order: prefix, rows:<id> (one per bad Q row), pin, p23, readme,
tables_sha.  Rows, the heading and the P23 row are looked for only on "live"
lines: not inside a fenced code block, an HTML comment or an indented code
block.  A Q or P23 row counts only if it is the single live row with that id
in the file and it comes after the live heading containing
`Correction (round 55)`.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
TABLES_SHA256 = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
TABLES_PATH = ".ufo/waves/round-55/frozen-tables.json"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
ENTRY_NAME = "hyprland-synthetic-dispatch-r52-errata-r53.md"
README = "corpus/README.md"
HEADING_TEXT = "Correction (round 55)"
P23_ANCHOR = "Hyprland-ConfigActions.cpp:1554-1576"
P23_SOURCE = "S371"
P23_SUPERSEDES = "P19"
P23_NEEDLES = ("m_passPressed", "== 1", "== 0", "PRESSED", "RELEASED")
P23_ALTERNATIVES = ("otherwise", "any other", "else")
NQ = 13
QIDS = ["Q%02d" % i for i in range(1, NQ + 1)]


class SetupError(Exception):
    pass


# --------------------------------------------------------------------- git

class Repo:
    def __init__(self, path, work):
        if not os.path.isdir(path):
            raise SetupError("repo is not a directory: %s" % path)
        self.path = path
        self.env = dict(os.environ)
        self.env.update({
            "TMPDIR": work,
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
        })
        r = self.run("rev-parse", "--git-dir")
        if r.returncode != 0:
            raise SetupError("not a git repository: %s" % path)

    def run(self, *args):
        try:
            return subprocess.run(["git", "-C", self.path] + list(args),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  env=self.env, check=False)
        except OSError as e:
            raise SetupError("cannot run git: %s" % e)

    def resolve(self, rev):
        if rev.startswith("-") or not rev:
            raise SetupError("bad rev: %r" % rev)
        r = self.run("rev-parse", "--verify", "--quiet", rev + "^{commit}")
        if r.returncode != 0:
            raise SetupError("rev does not resolve to a commit: %s" % rev)
        return r.stdout.decode().strip()

    def blob(self, commit, path):
        """Bytes of path at commit, or None when the path is absent there."""
        r = self.run("cat-file", "blob", "%s:%s" % (commit, path))
        return r.stdout if r.returncode == 0 else None


# ----------------------------------------------------------- markdown scan

_FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+.*" + re.escape(HEADING_TEXT))


def live_lines(data):
    """[(index, text)] of lines outside fenced code, HTML comments, indented code."""
    out = []
    fence = None  # (char, length)
    in_comment = False
    text = data.decode("utf-8", errors="replace")
    for i, raw in enumerate(text.split("\n")):
        line = raw.rstrip("\r")
        if fence is not None:
            m = re.match(r"^ {0,3}(`+|~+)[ \t]*$", line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
                fence = None
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        m = _FENCE_OPEN.match(line)
        if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
            fence = (m.group(1)[0], len(m.group(1)))
            continue
        if line.lstrip().startswith("<!--"):
            if "-->" not in line:
                in_comment = True
            continue
        if line.startswith("    ") or line.startswith("\t"):
            continue
        out.append((i, line))
    return out


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")) or len(s) < 2:
        return None
    return [c.strip() for c in s[1:-1].split("|")]


# ---------------------------------------------------------------- evaluate

def evaluate(repo, commit, base_commit, tables_sha):
    """Return dict of legs for the tree at commit."""
    base = repo.blob(base_commit, ENTRY)
    if base is None:
        raise SetupError("base commit %s lacks %s" % (base_commit, ENTRY))
    entry = repo.blob(commit, ENTRY)
    missed = []

    # prefix
    prefix_ok = entry is not None and entry.startswith(base)
    if not prefix_ok:
        missed.append("prefix")

    # tables
    tables_blob = repo.blob(commit, TABLES_PATH)
    tables = None
    if tables_blob is not None and hashlib.sha256(tables_blob).hexdigest() == tables_sha:
        try:
            tables = json.loads(tables_blob.decode("utf-8"))["c3"]
            qs = tables["q"]
            if [q["id"] for q in qs] != QIDS:
                raise SetupError("frozen c3.q ids are not Q01..Q13")
        except (ValueError, KeyError, TypeError) as e:
            raise SetupError("frozen-tables.json unreadable: %s" % e)

    # live structure of the entry
    heading_idx = None
    rows = {}
    if entry is not None:
        for idx, line in live_lines(entry):
            if heading_idx is None and _HEADING.match(line):
                heading_idx = idx
                continue
            c = cells(line)
            if c and c[0] in QIDS + ["P23"]:
                rows.setdefault(c[0], []).append((idx, c))

    def single(rid):
        got = rows.get(rid, [])
        if len(got) != 1 or heading_idx is None or got[0][0] <= heading_idx:
            return None
        return got[0][1]

    # rows (and pin, which needs the verified table)
    rows_ok = 0
    pin_ok = False
    if tables is None:
        missed.extend("rows:" + q for q in QIDS)
    else:
        for q in tables["q"]:
            c = single(q["id"])
            if (c is not None and len(c) == 3
                    and c[1] == "%s:%d" % (q["pin"], q["line"])
                    and c[2] == "`%s`" % q["quote"]):
                rows_ok += 1
            else:
                missed.append("rows:" + q["id"])
        pin = repo.blob(commit, tables["pin"])
        if pin is not None and hashlib.sha256(pin).hexdigest() == tables["pin_sha256"]:
            plines = pin.decode("utf-8", errors="replace").split("\n")
            pin_ok = all(1 <= q["line"] <= len(plines)
                         and plines[q["line"] - 1].strip() == q["quote"]
                         for q in tables["q"])
    if not pin_ok:
        missed.append("pin")

    # p23
    p23_ok = False
    c = single("P23")
    if c is not None and len(c) >= 6:
        prop = c[2]
        p23_ok = (c[1] == P23_SUPERSEDES and c[3] == P23_SOURCE and c[4] == P23_ANCHOR
                  and all(n in prop for n in P23_NEEDLES)
                  and any(a in prop for a in P23_ALTERNATIVES))
    if not p23_ok:
        missed.append("p23")

    # readme: any line naming the entry file together with P23
    readme = repo.blob(commit, README)
    readme_ok = readme is not None and any(
        ENTRY_NAME in ln and "P23" in ln
        for ln in readme.decode("utf-8", errors="replace").split("\n"))
    if not readme_ok:
        missed.append("readme")

    if tables is None:
        missed.append("tables_sha")

    return {"prefix": "identical" if prefix_ok else "changed", "rows": rows_ok,
            "pin": "ok" if pin_ok else "bad", "p23": "ok" if p23_ok else "bad",
            "readme": "ok" if readme_ok else "bad", "missed": missed,
            "verdict": "TARGET_MET" if not missed else "TARGET_MISSED"}


def fmt(rev, r):
    return ("MADO_P19_FIX: rev=%s prefix=%s rows=%d/13 pin=%s p23=%s readme=%s "
            "verdict=%s missed=%s" % (rev, r["prefix"], r["rows"], r["pin"], r["p23"],
                                      r["readme"], r["verdict"],
                                      ",".join(r["missed"]) or "none"))


def prepare_work(work):
    try:
        os.makedirs(work, exist_ok=True)
    except OSError as e:
        raise SetupError("cannot create --work: %s" % e)
    if not os.path.isdir(work) or not os.access(work, os.W_OK):
        raise SetupError("--work is not a writable directory")
    return os.path.realpath(work)


# ---------------------------------------------------------------- selftest

def selftest(repo_path, rev, work):
    work = prepare_work(work)
    real = Repo(repo_path, work)
    commit = real.resolve(rev)
    base = real.blob(BASE, ENTRY) if real.run("cat-file", "-e", BASE + "^{commit}").returncode == 0 else None
    if base is None:
        raise SetupError("real base commit %s not present in --repo" % BASE)
    base_readme = real.blob(BASE, README)
    tables_blob = real.blob(commit, TABLES_PATH)
    if tables_blob is None or hashlib.sha256(tables_blob).hexdigest() != TABLES_SHA256:
        raise SetupError("real tables blob at %s missing or not the frozen sha" % rev)
    tables = json.loads(tables_blob.decode())["c3"]
    pin = real.blob(commit, tables["pin"])
    if pin is None or hashlib.sha256(pin).hexdigest() != tables["pin_sha256"]:
        raise SetupError("real pin at %s missing or hash differs" % rev)
    base_text = base.decode("utf-8")
    readme_text = base_readme.decode("utf-8")

    D = tempfile.mkdtemp(prefix="c3-selftest-", dir=work)
    results = []
    try:
        top = subprocess.run(["git", "-C", D, "init", "-q"], check=False,
                             env=real.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if top.returncode != 0:
            raise SetupError("git init failed in scratch")
        r = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], env=real.env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.realpath(r.stdout.decode().strip()) != os.path.realpath(D):
            raise SetupError("scratch repo toplevel %r != %r" % (r.stdout, D))
        srepo = Repo(D, work)

        def commit_tree(files, msg):
            for name in os.listdir(D):
                if name == ".git":
                    continue
                p = os.path.join(D, name)
                shutil.rmtree(p) if os.path.isdir(p) and not os.path.islink(p) else os.unlink(p)
            for path, data in files.items():
                full = os.path.join(D, path)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "wb") as f:
                    f.write(data)
            for args in (["add", "-A", "-f"],
                         ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl",
                          "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty",
                          "-m", msg]):
                rr = subprocess.run(["git", "-C", D] + args, env=real.env,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if rr.returncode != 0:
                    raise SetupError("git %s failed: %s" % (args[-1], rr.stderr.decode()))
            return srepo.run("rev-parse", "HEAD").stdout.decode().strip()

        base_commit = commit_tree({ENTRY: base}, "base")

        # ---- synthetic good tree
        p23_prop = ("`Actions::pass` branches on `S.m_passPressed`: `== 1` sends a PRESSED keyboard "
                    "key, `== 0` sends a RELEASED key, and otherwise (any other value) it sends "
                    "PRESSED then RELEASED, so P19's \"only when `m_passPressed == 1`\" is false.")
        p23_row = ("| P23 | P19 | %s | S371 | %s | `%s` | direct: the else arm at line 1566 "
                   "sends both states. |" % (p23_prop, P23_ANCHOR, tables["q"][0]["quote"]))
        q_rows = ["| %s | %s:%d | `%s` |" % (q["id"], q["pin"], q["line"], q["quote"])
                  for q in tables["q"]]
        block_lines = (["", "## " + HEADING_TEXT, "",
                        "P19 above is false; this block supersedes it.", "",
                        "| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |",
                        "|---|---|---|---|---|---|---|", p23_row, "",
                        "| ID | Pin:line | Quote |", "|---|---|---|"] + q_rows + [""])
        block = "\n".join(block_lines)
        entry_good = base_text + block
        fname = ENTRY_NAME
        lines = readme_text.split("\n")
        hit = [i for i, ln in enumerate(lines) if fname in ln]
        readme_p23 = list(lines)
        if hit:
            readme_p23[hit[0]] = lines[hit[0]].rstrip() + " P23 supersedes P19 (round 55)."
        else:
            readme_p23.append("| `knowledge/%s` | P23 supersedes P19 |" % fname)
        readme_good = "\n".join(readme_p23)
        readme_no_p23 = "\n".join(lines) if hit else readme_text
        if "P23" in "\n".join(l for l in readme_no_p23.split("\n") if fname in l):
            raise SetupError("base README entry line already mentions P23")

        def tree(entry=None, readme=None, tables_b=None, pin_b=None, drop=()):
            t = {ENTRY: (entry_good if entry is None else entry).encode(),
                 README: (readme_good if readme is None else readme).encode(),
                 TABLES_PATH: tables_blob if tables_b is None else tables_b,
                 tables["pin"]: pin if pin_b is None else pin_b}
            for d in drop:
                t.pop(d, None)
            return t

        def line_of(rid, text=None):
            t = text or entry_good
            return [l for l in t.split("\n") if l.startswith("| %s |" % rid)][0]

        def sub(text, old, new):
            assert text.count(old) == 1, (old, text.count(old))
            return text.replace(old, new)

        allq = ["rows:" + q for q in QIDS]
        q09 = line_of("Q09")
        q07 = line_of("Q07")
        q03 = line_of("Q03")
        q05 = line_of("Q05")
        q02 = line_of("Q02")
        old_prop = ("`Actions::pass` sends modifier state before its delivery branch; it sends a "
                    "PRESSED keyboard key only when `m_passPressed == 1` and the key is not a "
                    "mouse button.")
        junk_lex = "m_passPressed == 1 == 0 PRESSED RELEASED else"
        junk_false = ("`m_passPressed == 1` sends RELEASED; `== 0` sends PRESSED; otherwise it "
                      "sends nothing at all.")
        fence_block = block.replace("\n## " + HEADING_TEXT, "\n```\n## " + HEADING_TEXT, 1) + "\n```\n"
        fence_p23 = sub(entry_good, p23_row, "```\n" + p23_row + "\n```")
        heading_last = (base_text + block.replace("## " + HEADING_TEXT, "## Late note") +
                        "\n## " + HEADING_TEXT + "\n")
        base_lines = base_text.split("\n")
        pre_idx = [i for i, l in enumerate(base_lines) if l.startswith("| P19 |")][0]
        rewritten = base_text.replace("| P19 | P16 |", "| P19 | P17 |", 1)
        quoteq = sub(entry_good, q09, q09.replace("STATE_PRESSED);", "STATE_PRESSEE);"))

        variants = [
            # name, files, expected verdict, expected missed
            ("good", tree(), "TARGET_MET", []),
            ("C3-CTL-1 absent (block removed = base)", tree(entry=base_text),
             "TARGET_MISSED", allq + ["p23"]),
            ("C3-CTL-2 rewritten-prefix (P19 row one byte)", tree(entry=rewritten + block),
             "TARGET_MISSED", ["prefix"]),
            ("C3-CTL-3 altered-quote Q09", tree(entry=quoteq), "TARGET_MISSED", ["rows:Q09"]),
            ("C3-CTL-4 old-arm-only (Q08-Q12 deleted)",
             tree(entry="\n".join(l for l in entry_good.split("\n")
                                  if not any(l.startswith("| %s |" % q) for q in
                                             ("Q08", "Q09", "Q10", "Q11", "Q12")))),
             "TARGET_MISSED", ["rows:Q%02d" % i for i in range(8, 13)]),
            ("C3-CTL-5 old-wording (P23 cell = P19 sentence)",
             tree(entry=sub(entry_good, p23_prop, old_prop)), "TARGET_MISSED", ["p23"]),
            ("C3-CTL-6 readme-missing (README line without P23)", tree(readme=readme_no_p23),
             "TARGET_MISSED", ["readme"]),
            ("prefix-CRLF (base LF->CRLF, block LF)",
             tree(entry=base_text.replace("\n", "\r\n") + block), "TARGET_MISSED", ["prefix"]),
            ("prefix-CRLF whole file", tree(entry=entry_good.replace("\n", "\r\n")),
             "TARGET_MISSED", ["prefix"]),
            ("duplicated Q03 row", tree(entry=sub(entry_good, q03, q03 + "\n" + q03)),
             "TARGET_MISSED", ["rows:Q03"]),
            ("Q07 only inside a fenced code block",
             tree(entry=sub(entry_good, q07, "```\n" + q07 + "\n```")),
             "TARGET_MISSED", ["rows:Q07"]),
            ("Q07 inside ~~~ fence", tree(entry=sub(entry_good, q07, "~~~\n" + q07 + "\n~~~")),
             "TARGET_MISSED", ["rows:Q07"]),
            ("Q07 inside HTML comment",
             tree(entry=sub(entry_good, q07, "<!--\n" + q07 + "\n-->")),
             "TARGET_MISSED", ["rows:Q07"]),
            ("Q07 indented 4 spaces (code block)", tree(entry=sub(entry_good, q07, "    " + q07)),
             "TARGET_MISSED", ["rows:Q07"]),
            ("Q07 live row plus extra fenced copy",
             tree(entry=sub(entry_good, q07, "```\n" + q07 + "\n```\n" + q07)),
             "TARGET_MET", []),
            ("whole block fenced", tree(entry=base_text + fence_block),
             "TARGET_MISSED", allq + ["p23"]),
            ("P23 row only in a fence", tree(entry=fence_p23), "TARGET_MISSED", ["p23"]),
            ("heading text wrong (round 56)",
             tree(entry=sub(entry_good, HEADING_TEXT, "Correction (round 56)")),
             "TARGET_MISSED", allq + ["p23"]),
            ("heading after the rows", tree(entry=heading_last), "TARGET_MISSED", allq + ["p23"]),
            ("Q02 wrong line :1557", tree(entry=sub(entry_good, q02, q02.replace(":1556", ":1557"))),
             "TARGET_MISSED", ["rows:Q02"]),
            ("Q05 extra trailing cell", tree(entry=sub(entry_good, q05, q05 + " extra |")),
             "TARGET_MISSED", ["rows:Q05"]),
            ("Q01 quote unbackticked",
             tree(entry=sub(entry_good, line_of("Q01"),
                            line_of("Q01").replace("`", ""))), "TARGET_MISSED", ["rows:Q01"]),
            ("P23 Supersedes P18", tree(entry=sub(entry_good, "| P23 | P19 |", "| P23 | P18 |")),
             "TARGET_MISSED", ["p23"]),
            ("P23 source row S372", tree(entry=sub(entry_good, "| S371 | " + P23_ANCHOR, "| S372 | " + P23_ANCHOR)),
             "TARGET_MISSED", ["p23"]),
            ("P23 anchor 1554-1558", tree(entry=sub(entry_good, P23_ANCHOR, "Hyprland-ConfigActions.cpp:1554-1558")),
             "TARGET_MISSED", ["p23"]),
            ("duplicated P23 row", tree(entry=sub(entry_good, p23_row, p23_row + "\n" + p23_row)),
             "TARGET_MISSED", ["p23"]),
            ("P23 lacks the 'otherwise/any other/else' word",
             tree(entry=sub(entry_good, p23_prop,
                            p23_prop.replace("otherwise (any other value)", "for 2 or more"))),
             "TARGET_MISSED", ["p23"]),
            ("P23 lacks '== 0'", tree(entry=sub(entry_good, p23_prop, p23_prop.replace("== 0", "= 0"))),
             "TARGET_MISSED", ["p23"]),
            ("P23 lowercase 'pressed' only",
             tree(entry=sub(entry_good, p23_prop, p23_prop.replace("PRESSED", "pressed"))),
             "TARGET_MISSED", ["p23"]),
            ("P23 JUNK keyword soup (lexical leg accepts)",
             tree(entry=sub(entry_good, p23_prop, junk_lex)), "TARGET_MET", []),
            ("P23 FALSE semantics with the keywords (lexical leg accepts)",
             tree(entry=sub(entry_good, p23_prop, junk_false)), "TARGET_MET", []),
            ("README line naming the file in a different line than P23",
             tree(readme="\n".join(lines) + "\nP23 is mentioned here only.\n"),
             "TARGET_MISSED", ["readme"]),
            ("README absent", tree(drop=(README,)), "TARGET_MISSED", ["readme"]),
            ("frozen-tables.json tampered (one space)",
             tree(tables_b=tables_blob + b" "), "TARGET_MISSED", allq + ["pin", "tables_sha"]),
            ("frozen-tables.json absent", tree(drop=(TABLES_PATH,)), "TARGET_MISSED",
             allq + ["pin", "tables_sha"]),
            ("pin tampered (one space appended)", tree(pin_b=pin + b" "), "TARGET_MISSED", ["pin"]),
            ("pin absent", tree(drop=(tables["pin"],)), "TARGET_MISSED", ["pin"]),
            ("entry deleted", tree(drop=(ENTRY,)), "TARGET_MISSED", ["prefix"] + allq + ["p23"]),
            ("entry truncated below base", tree(entry=base_text[:-20]), "TARGET_MISSED",
             ["prefix"] + allq + ["p23"]),
            ("good tree with CRLF block lines",
             tree(entry=base_text + block.replace("\n", "\r\n")), "TARGET_MET", []),
            ("Q rows with cell padding", tree(entry=sub(entry_good, q03, q03.replace("| ", "|   ").replace(" |", "   |"))),
             "TARGET_MET", []),
        ]
        shape = re.compile(r"^MADO_P19_FIX: rev=\S+ prefix=(identical|changed) rows=\d+/13 "
                           r"pin=(ok|bad) p23=(ok|bad) readme=(ok|bad) "
                           r"verdict=(TARGET_MET|TARGET_MISSED) missed=\S+$")
        for name, files, want_v, want_missed in variants:
            sha = commit_tree(files, name)
            got = evaluate(srepo, sha, base_commit, TABLES_SHA256)
            line = fmt(sha[:12], got)
            ok = (got["verdict"] == want_v and got["missed"] == want_missed
                  and bool(shape.match(line)))
            results.append(ok)
            print("%s %s\n    expected %s missed=%s\n    got      %s" % (
                "PASS" if ok else "FAIL", name, want_v, ",".join(want_missed) or "none", line))

        # ---- CLI process checks (real lane repo, real entry points)
        me = os.path.abspath(__file__)

        def cli(*args):
            return subprocess.run([sys.executable, "-I", me] + list(args), env=real.env,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cw = os.path.join(work, "cli-work")
        r = cli("--repo", repo_path, "--rev", rev, "--work", cw)
        out = r.stdout.decode()
        ok = (r.returncode in (0, 1) and out.count("\n") == 1 and bool(shape.match(out.strip()))
              and (r.returncode == 0) == ("verdict=TARGET_MET" in out))
        results.append(ok)
        print("%s CLI on the real repo at %s: rc=%d\n    %s" % ("PASS" if ok else "FAIL", rev, r.returncode, out.strip()))
        r = cli("--repo", repo_path, "--rev", "no-such-rev-zzz", "--work", cw)
        ok = r.returncode == 2 and r.stdout == b""
        results.append(ok)
        print("%s CLI bad rev -> rc=%d stdout=%r" % ("PASS" if ok else "FAIL", r.returncode, r.stdout))
        r = cli("--repo", repo_path, "--rev", rev)
        ok = r.returncode == 2 and r.stdout == b""
        results.append(ok)
        print("%s CLI missing --work -> rc=%d stdout=%r" % ("PASS" if ok else "FAIL", r.returncode, r.stdout))
        r = cli("--repo", os.path.join(work, "not-a-repo"), "--rev", rev, "--work", cw)
        ok = r.returncode == 2 and r.stdout == b""
        results.append(ok)
        print("%s CLI repo is not a directory -> rc=%d stdout=%r" % ("PASS" if ok else "FAIL", r.returncode, r.stdout))
        r = cli("--repo", repo_path, "--rev", "-x", "--work", cw)
        ok = r.returncode == 2 and r.stdout == b""
        results.append(ok)
        print("%s CLI rev starting with '-' -> rc=%d stdout=%r" % ("PASS" if ok else "FAIL", r.returncode, r.stdout))
    finally:
        shutil.rmtree(D, ignore_errors=True)
        shutil.rmtree(os.path.join(work, "cli-work"), ignore_errors=True)
    passed = sum(results)
    print("C3_SELFTEST: %d/%d passed" % (passed, len(results)))
    return 0 if passed == len(results) else 1


# -------------------------------------------------------------------- main

def main(argv):
    ap = argparse.ArgumentParser(prog="c3-r55-p19.py", add_help=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if a.work is None:
            raise SetupError("--work is required")
        if a.selftest:
            return selftest(a.repo, a.rev or "HEAD", a.work)
        if a.rev is None:
            raise SetupError("--rev is required")
        work = prepare_work(a.work)
        repo = Repo(a.repo, work)
        commit = repo.resolve(a.rev)
        if repo.run("cat-file", "-e", BASE + "^{commit}").returncode != 0:
            raise SetupError("base commit %s not present in --repo" % BASE)
        res = evaluate(repo, commit, BASE, TABLES_SHA256)
    except SetupError as e:
        sys.stderr.write("MADO_P19_FIX: SETUP %s\n" % e)
        return 2
    sys.stdout.write(fmt(a.rev, res) + "\n")
    return 0 if res["verdict"] == "TARGET_MET" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

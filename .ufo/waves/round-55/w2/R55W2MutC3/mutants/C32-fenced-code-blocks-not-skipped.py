#!/usr/bin/env python3
"""PRED-C3-r55 counter: the append-only correction of the false P19 statement (round 55, claim C3, freshness).

    python3 -I quality/counters/c3-r55-p19.py --repo REPO --rev REV --work DIR
    python3 -I quality/counters/c3-r55-p19.py --selftest --repo REPO [--rev REV] --work DIR

Contract: .ufo/waves/round-55/registration.md section C3 (frozen). Reads ONLY git objects at --rev of --repo (never the
working tree): the errata entry, corpus/README.md, the round-52 pin and the frozen tables
(.ufo/waves/round-55/frozen-tables.json), plus the entry's bytes at the base commit
3b55b6e91e40f455dd56b2985e4ffc087ada92d5 of the same repo. Prints exactly one line

  MADO_P19_FIX: rev=<rev> prefix=<identical|changed> rows=<a>/13 pin=<ok|bad> p23=<ok|bad> readme=<ok|bad> verdict=<TARGET_MET|TARGET_MISSED> missed=<legs,comma>|none

and exits 0 only on TARGET_MET, 1 on a verdict miss, 2 on a setup error (stdout `MADO_P19_FIX: SETUP <reason>`).
`rev=` echoes the --rev argument as given. Writes nothing; --work is used as TMPDIR of the git children (the selftest builds
its scratch git repos below it).

Method (bytes-first): `prefix` is a raw byte comparison -- the entry at REV must start with the exact bytes of the entry at
the base commit. Only the bytes after that prefix are parsed, line by line on b"\\n", each line stripped of ASCII
whitespace (so CR is tolerated after the prefix, never inside it). Lines inside a fenced code block (a line whose first
non-blank bytes are three or more of ` or ~, closed by the same character) are not rows, headings or README text of the
block. A markdown row is `|` cell `|` cell ... with cells stripped; a Q row has exactly three cells
(`Qnn`, `<pin>:<line>`, `` `<quote>` ``) and counts toward rows=a/13 only if it is the ONLY row of that id and its three
cells equal frozen-tables.json c3.q byte for byte.

Legs (names printed in missed=, in this order; `stale` per registration v2 E8 follows p23): prefix; rows:heading (no heading line containing `Correction (round 55)`
in the appended block -- the registration lists no leg name for the heading, this one is declared here); rows:Qnn (Q row
missing, duplicated, malformed or != frozen); pin (the pin's bytes at REV do not hash to c3.pin_sha256, or a frozen quote
is not exactly the stripped pin line at its line); p23 (not exactly one P23 row in the block, or its Supersedes cell is not
`P19`, its Source row cell is not `S371`, its Pin:anchor cell is not `Hyprland-ConfigActions.cpp:1554-1576`, or the
proposition cell lacks `m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED` or all of `otherwise`/`any other`/`else`
(case-sensitive substrings)); readme (no corpus/README.md line containing both
`hyprland-synthetic-dispatch-r52-errata-r53.md` and `P23`); tables_sha (the blob of frozen-tables.json at REV does not
hash to the constant TABLES_SHA256 below, or is absent).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

TABLES_SHA256 = "13d6e2f9c0dfe1287e2cd9a7d814d95a4fb0ff0ad7ce644aad7ead18af69a7b9"
BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
TABLES_PATH = ".ufo/waves/round-55/frozen-tables-v2.json"
ENTRY_PATH = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
ENTRY_NAME = b"hyprland-synthetic-dispatch-r52-errata-r53.md"
README_PATH = "corpus/README.md"
NQ = 13
QIDS = ["Q%02d" % i for i in range(1, NQ + 1)]
HEADING = b"Correction (round 55)"
P23_ANCHOR = b"Hyprland-ConfigActions.cpp:1554-1576"
P23_TOKENS = [b"m_passPressed", b"== 1", b"== 0", b"PRESSED", b"RELEASED"]
P23_ALT = [b"otherwise", b"any other", b"else"]
WS = b" \t\r\n\x0b\x0c"


class Setup(Exception):
    pass


def emit_setup(reason):
    sys.stdout.write("MADO_P19_FIX: SETUP %s\n" % reason)
    sys.stdout.flush()
    return 2


class Repo:
    """Revision-addressed reads of one repository; ambient GIT_* never leaks in."""

    def __init__(self, repo, work):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "LC_ALL": "C",
                    "GIT_OPTIONAL_LOCKS": "0"})
        if work and os.path.isdir(work):
            env["TMPDIR"] = work
        env.setdefault("PATH", "/usr/bin:/bin")
        self.env = env
        self.repo = repo

    def git(self, *args):
        try:
            p = subprocess.run(["git", "-C", self.repo] + list(args), env=self.env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as e:
            raise Setup("git_unavailable")
        return p.returncode, p.stdout

    def commit_of(self, rev):
        if not rev or rev.startswith("-"):
            raise Setup("bad_rev")
        rc, out = self.git("rev-parse", "--verify", "-q", rev + "^{commit}")
        if rc != 0:
            rc2, _ = self.git("rev-parse", "--git-dir")
            raise Setup("not_a_repo" if rc2 != 0 else "unresolvable_rev")
        h = out.decode("ascii", "replace").strip()
        if not re.fullmatch(r"[0-9a-f]{40,64}", h):
            raise Setup("unresolvable_rev")
        return h

    def blob(self, commit, path):
        """Bytes of path at commit, or None if the path is not a blob in that tree."""
        rc, kind = self.git("cat-file", "-t", "%s:%s" % (commit, path))
        if rc != 0 or kind.strip() != b"blob":
            return None
        rc, data = self.git("cat-file", "blob", "%s:%s" % (commit, path))
        if rc != 0:
            raise Setup("git_read_failed")
        return data


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def cells_of(stripped):
    """Cells of a markdown table row (already stripped), or None if it is not a row."""
    if not stripped.startswith(b"|"):
        return None
    inner = stripped[1:]
    if inner.endswith(b"|"):
        inner = inner[:-1]
    return [c.strip(WS) for c in inner.split(b"|")]


def block_lines(block):
    """Yield (stripped line) for every line of the appended block that is outside a fenced code block."""
    fence = None
    for raw in block.split(b"\n"):
        s = raw.strip(WS)
        lead = raw.lstrip(b" \t")
        m = re.match(rb"(`{3,}|~{3,})", lead)
        if False:
            ch = m.group(1)[:1]
            if fence is None:
                fence = ch
                continue
            if fence == ch:
                fence = None
                continue
        if fence is None:
            yield s


def evaluate(repo_path, rev, work, base_commit=BASE):
    """Return (fields, missed list). Raises Setup."""
    R = Repo(repo_path, work)
    commit = R.commit_of(rev)
    rc, _ = R.git("cat-file", "-e", base_commit + "^{commit}")
    if rc != 0:
        raise Setup("base_commit_absent")
    base_entry = R.blob(base_commit, ENTRY_PATH)
    if base_entry is None:
        raise Setup("base_entry_absent")
    missed = []

    # tables ------------------------------------------------------------------------------------------------------
    tables_blob = R.blob(commit, TABLES_PATH)
    tables = None
    tables_ok = tables_blob is not None and sha256(tables_blob) == TABLES_SHA256
    if tables_blob is not None:
        try:
            tables = json.loads(tables_blob.decode("utf-8"))["c3"]
            frozen_q = {q["id"]: q for q in tables["q"]}
            pin_path = tables["pin"]
            pin_sha = tables["pin_sha256"]
            if not all(i in frozen_q for i in QIDS) or len(frozen_q) != NQ:
                raise ValueError("q table shape")
        except (ValueError, KeyError, TypeError):
            if tables_ok:
                raise Setup("tables_unparsable")
            tables = None
    if tables is None:
        frozen_q, pin_path, pin_sha = {}, None, None

    # prefix: raw bytes ---------------------------------------------------------------------------------------------
    entry = R.blob(commit, ENTRY_PATH)
    prefix_ok = entry is not None and entry.startswith(base_entry)
    block = entry[len(base_entry):] if prefix_ok else b""

    # rows ----------------------------------------------------------------------------------------------------------
    q_rows = {i: [] for i in QIDS}
    p23_rows = []
    heading = False
    for s in block_lines(block):
        if s.startswith(b"#") and HEADING in s:
            heading = True
        cells = cells_of(s)
        if cells is None or not cells:
            continue
        if cells[0] in q_rows_keys():
            q_rows[cells[0].decode("ascii")].append(cells)
        elif cells[0] == b"P23":
            p23_rows.append(cells)
    rows_ok = 0
    row_missed = []
    for i in QIDS:
        good = False
        rs = q_rows[i]
        if len(rs) == 1 and i in frozen_q:
            c = rs[0]
            f = frozen_q[i]
            want_anchor = ("%s:%d" % (f["pin"], f["line"])).encode("utf-8")
            want_quote = b"`" + f["quote"].encode("utf-8") + b"`"
            good = len(c) == 3 and c[1] == want_anchor and c[2] == want_quote
        if good:
            rows_ok += 1
        else:
            row_missed.append("rows:" + i)
    if not heading:
        row_missed.insert(0, "rows:heading")

    # pin -----------------------------------------------------------------------------------------------------------
    pin_ok = False
    if pin_path is not None:
        pb = R.blob(commit, pin_path)
        if pb is not None and sha256(pb) == pin_sha:
            lines = pb.split(b"\n")
            pin_ok = True
            for i in QIDS:
                f = frozen_q[i]
                ln = f["line"]
                if not (0 < ln <= len(lines)) or lines[ln - 1].strip(WS) != f["quote"].encode("utf-8"):
                    pin_ok = False

    # p23 -----------------------------------------------------------------------------------------------------------
    p23_ok = False
    if len(p23_rows) == 1:
        c = p23_rows[0]
        if len(c) >= 5 and c[1] == b"P19" and c[3] == b"S371" and c[4] == P23_ANCHOR:
            prop = c[2]
            p23_ok = all(t in prop for t in P23_TOKENS) and any(t in prop for t in P23_ALT)

    # readme --------------------------------------------------------------------------------------------------------
    readme = R.blob(commit, README_PATH)
    readme_ok = False
    if readme is not None:
        for ln in readme.split(b"\n"):
            if ENTRY_NAME in ln and b"P23" in ln:
                readme_ok = True
                break

    # stale (registration v2 E8): the appended bytes re-assert neither `only when` nor the exact base P19 sentence --------
    stale = b"only when" in block.lower()
    for ln in base_entry.split(b"\n"):
        cl = cells_of(ln.strip(WS))
        if cl and cl[0] == b"P19" and len(cl) >= 3 and cl[2] and cl[2] in block:
            stale = True

    if not prefix_ok:
        missed.append("prefix")
    missed += row_missed
    if not pin_ok:
        missed.append("pin")
    if not p23_ok:
        missed.append("p23")
    if stale:
        missed.append("stale")
    if not readme_ok:
        missed.append("readme")
    if not tables_ok:
        missed.append("tables_sha")
    fields = {"prefix": "identical" if prefix_ok else "changed", "rows": "%d/%d" % (rows_ok, NQ),
              "pin": "ok" if pin_ok else "bad", "p23": "ok" if p23_ok else "bad",
              "readme": "ok" if readme_ok else "bad"}
    return fields, missed


_QKEYS = None


def q_rows_keys():
    global _QKEYS
    if _QKEYS is None:
        _QKEYS = set(i.encode("ascii") for i in QIDS)
    return _QKEYS


def render(rev, fields, missed):
    verdict = "TARGET_MET" if not missed else "TARGET_MISSED"
    return ("MADO_P19_FIX: rev=%s prefix=%s rows=%s pin=%s p23=%s readme=%s verdict=%s missed=%s"
            % (rev, fields["prefix"], fields["rows"], fields["pin"], fields["p23"], fields["readme"], verdict,
               ",".join(missed) if missed else "none")), verdict


# ------------------------------------------------------------------------------------------------------------------
# selftest: a scratch git repo with a synthetic good tree and the frozen controls
# ------------------------------------------------------------------------------------------------------------------

SYN_BASE = (b"# Correction to synthetic-dispatch propositions P16\xe2\x80\x93P18\n\n"
            b"source: S370, S371\nverified-at: 2026-10-27\nrecheck: on-release\n\n"
            b"## Corrected propositions\n\n"
            b"| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (\xe2\x89\xa425 words) | Support |\n"
            b"|---|---|---|---|---|---|---|\n"
            b"| P19 | P16 | `Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key "
            b"only when `m_passPressed == 1` and the key is not a mouse button. | S371 | "
            b"Hyprland-ConfigActions.cpp:1554-1558 | `x` | direct |\n"
            b"| P20 | P16 | After the delivery branch it clears modifier state. | S371 | "
            b"Hyprland-ConfigActions.cpp:1576 | `y` | direct |\n\n"
            b"## Limits\n\nThe round-53 wave seats are lane-dispatched.\n")

SYN_README_BASE = (b"# corpus\n\n| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` (round 53; append-only "
                   b"correction to P16-P18) | Corrects three propositions. |\n| `knowledge/other.md` | other |\n")
SYN_README_GOOD = (b"# corpus\n\n| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` (round 53; append-only "
                   b"correction to P16-P18; round 55 adds P23 superseding P19) | Corrects four propositions. |\n"
                   b"| `knowledge/other.md` | other |\n")

P23_GOOD = (b"| P23 | P19 | `Actions::pass` sends the PRESSED keyboard key when `m_passPressed == 1`, the RELEASED key "
            b"when `m_passPressed == 0`, and otherwise (any other value) sends PRESSED then RELEASED. | S371 | "
            b"Hyprland-ConfigActions.cpp:1554-1576 | `see Q01-Q13` | direct |\n")


def good_block(frozen_q):
    out = [b"\n## Correction (round 55): P19 was incomplete\n\n",
           b"| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote | Support |\n|---|---|---|---|---|---|---|\n",
           P23_GOOD, b"\n| ID | Pin:line | Quote |\n|---|---|---|\n"]
    for i in QIDS:
        f = frozen_q[i]
        out.append(("| %s | %s:%d | `%s` |\n" % (i, f["pin"], f["line"], f["quote"])).encode("utf-8"))
    return b"".join(out)


def replace_once(b, old, new):
    assert b.count(old) == 1, (old, b.count(old))
    return b.replace(old, new)


def selftest(repo_path, rev, work):
    import shutil
    import tempfile
    if not work:
        return emit_setup("usage")
    os.makedirs(work, exist_ok=True)
    R = Repo(repo_path, work)
    commit = R.commit_of(rev)
    tables_blob = R.blob(commit, TABLES_PATH)
    if tables_blob is None or sha256(tables_blob) != TABLES_SHA256:
        return emit_setup("tables_missing_or_changed")
    tables = json.loads(tables_blob.decode("utf-8"))["c3"]
    pin_blob = R.blob(commit, tables["pin"])
    if pin_blob is None or sha256(pin_blob) != tables["pin_sha256"]:
        return emit_setup("pin_missing_or_changed")
    frozen_q = {q["id"]: q for q in tables["q"]}
    GB = good_block(frozen_q)

    D = tempfile.mkdtemp(prefix="c3-selftest-", dir=work)
    results = []
    try:
        env = dict(R.env)
        env["TMPDIR"] = work

        def g(*args, inp=None):
            p = subprocess.run(["git", "-C", D] + list(args), env=env, input=inp, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            if p.returncode != 0:
                raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace")))
            return p.stdout.decode("utf-8", "replace").strip()

        g("init", "-q")
        top = g("rev-parse", "--show-toplevel")
        if os.path.realpath(top) != os.path.realpath(D):
            raise RuntimeError("scratch toplevel %s != %s" % (top, D))
        n = [0]

        def commit_tree(files, parent=None):
            for dp, dn, fn in os.walk(D, topdown=True):
                dn[:] = [x for x in dn if x != ".git"]
                for f in fn:
                    os.unlink(os.path.join(dp, f))
            for p, data in files.items():
                fp = os.path.join(D, p)
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, "wb") as fh:
                    fh.write(data)
            g("add", "-A", "-f")
            n[0] += 1
            tree = g("write-tree")
            args = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", tree, "-m", "c%d" % n[0]]
            if parent:
                args += ["-p", parent]
            return g(*args)

        common = {tables["pin"]: pin_blob, TABLES_PATH: tables_blob}

        def tree(entry, readme=SYN_README_GOOD, **over):
            t = dict(common)
            t[ENTRY_PATH] = entry
            t[README_PATH] = readme
            t.update(over)
            return t

        base = commit_tree(tree(SYN_BASE, SYN_README_BASE))
        good_entry = SYN_BASE + GB
        # the in-process base is the scratch repo's own base commit (the real base 3b55b6e is not in a scratch repo)
        cases = []

        def case(name, files, expect_met, must=(), mustnot=(), prefix=None, exact=None):
            cases.append((name, files, expect_met, tuple(must), tuple(mustnot), prefix, exact))

        case("good", tree(good_entry), True, exact=[])
        # six frozen controls of registration C3
        case("C3-CTL-1 absent (block removed = base)", tree(SYN_BASE), False,
             must=["rows:Q01", "rows:Q13", "p23"], mustnot=["prefix", "readme"], prefix="identical")
        mut = bytearray(SYN_BASE)
        mut[mut.index(b"P19")] ^= 0x01  # one byte of the original P19 row ("P19" -> "Q19")
        case("C3-CTL-2 rewritten prefix (one byte of P19 row)", tree(bytes(mut) + GB), False, must=["prefix"],
             prefix="changed")
        def qrow(i):
            f = frozen_q[i]
            return ("| %s | %s:%d | `%s` |\n" % (i, f["pin"], f["line"], f["quote"])).encode("utf-8")

        q09 = frozen_q["Q09"]["quote"].encode("utf-8")
        case("C3-CTL-3 altered Q09 quote", tree(SYN_BASE + replace_once(GB, qrow("Q09"), qrow("Q09").replace(b"PRESSED", b"PRESSEd"))),
             False, must=["rows:Q09"], mustnot=["prefix", "p23", "pin"], exact=["rows:Q09"])
        gb4 = GB
        for i in ["Q08", "Q09", "Q10", "Q11", "Q12"]:
            gb4 = replace_once(gb4, qrow(i), b"")
        case("C3-CTL-4 old-arm-only (Q08-Q12 deleted)", tree(SYN_BASE + gb4), False, must=["rows:Q08"],
             exact=["rows:Q08", "rows:Q09", "rows:Q10", "rows:Q11", "rows:Q12"])
        old = (b"`Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key "
               b"only when `m_passPressed == 1` and the key is not a mouse button.")
        gb5 = P23_GOOD.split(b"| P19 | ")[1].split(b" | S371")[0]
        case("C3-CTL-5 old wording in P23", tree(SYN_BASE + GB.replace(gb5, old)), False, must=["p23", "stale"],
             exact=["p23", "stale"])
        case("C3-CTL-5 v2 old wording keyword-stuffed (p23 satisfied, stale rejects)",
             tree(SYN_BASE + GB.replace(gb5, old + b" == 0 RELEASED otherwise")), False, must=["stale"],
             mustnot=["p23"], exact=["stale"])
        case("C3-CTL-6 README line without P23", tree(good_entry, SYN_README_BASE), False, must=["readme"],
             exact=["readme"])
        # extra cases requested by the seat assignment
        case("prefix with CRLF (first line LF -> CRLF)", tree(SYN_BASE.replace(b"\n", b"\r\n", 1) + GB), False,
             must=["prefix"], prefix="changed")
        case("prefix with CRLF everywhere", tree(SYN_BASE.replace(b"\n", b"\r\n") + GB), False, must=["prefix"],
             prefix="changed")
        row3 = qrow("Q03")
        case("duplicated Q03 row", tree(SYN_BASE + GB + row3), False, must=["rows:Q03"], exact=["rows:Q03"])
        case("duplicated Q03 row elsewhere inside block", tree(SYN_BASE + GB.replace(row3, row3 + row3)), False,
             must=["rows:Q03"], exact=["rows:Q03"])
        case("Q03 row moved inside a fenced code block", tree(SYN_BASE + GB.replace(row3, b"```\n" + row3 + b"```\n")),
             False, must=["rows:Q03"], exact=["rows:Q03"])
        case("extra fenced copy of Q03 beside the real row does not count as duplicate",
             tree(SYN_BASE + GB + b"\n```\n" + row3 + b"```\n"), True, exact=[])
        case("tilde fence hides Q03 row", tree(SYN_BASE + GB.replace(row3, b"~~~\n" + row3 + b"~~~\n")), False,
             must=["rows:Q03"], exact=["rows:Q03"])
        case("P23 row only inside a fence", tree(SYN_BASE + GB.replace(P23_GOOD, b"```\n" + P23_GOOD + b"```\n")),
             False, must=["p23"], exact=["p23"])
        case("heading missing", tree(SYN_BASE + GB.replace(b"## Correction (round 55): P19 was incomplete\n",
                                                           b"## Corrections\n")), False, must=["rows:heading"],
             exact=["rows:heading"])
        case("heading only inside a fence", tree(SYN_BASE + GB.replace(b"## Correction (round 55): P19 was incomplete\n",
                                                                       b"```\n## Correction (round 55)\n```\n")),
             False, must=["rows:heading"], exact=["rows:heading"])
        case("duplicated P23 row", tree(SYN_BASE + GB.replace(P23_GOOD, P23_GOOD + P23_GOOD)), False, must=["p23"],
             exact=["p23"])
        case("P23 supersedes P20", tree(SYN_BASE + GB.replace(b"| P23 | P19 |", b"| P23 | P20 |")), False,
             must=["p23"], exact=["p23"])
        case("P23 wrong source row", tree(SYN_BASE + GB.replace(b"| S371 | Hyprland-ConfigActions.cpp:1554-1576",
                                                                b"| S370 | Hyprland-ConfigActions.cpp:1554-1576")),
             False, must=["p23"], exact=["p23"])
        case("P23 lacks the else-arm word", tree(SYN_BASE + GB.replace(b"and otherwise (any other value) sends",
                                                                       b"and in the remaining case sends")),
             False, must=["p23"], exact=["p23"])
        case("P23 lacks == 0", tree(SYN_BASE + GB.replace(b"`m_passPressed == 0`", b"the zero case")), False,
             must=["p23"], exact=["p23"])
        case("Q row quote with trailing space inside backticks", tree(SYN_BASE + GB.replace(qrow("Q09"), qrow("Q09").replace(q09 + b"`", q09 + b" `"))),
             False, must=["rows:Q09"], exact=["rows:Q09"])
        case("Q row anchor line shifted", tree(SYN_BASE + GB.replace(b"| Q09 | Hyprland-ConfigActions.cpp:1568 |",
                                                                      b"| Q09 | Hyprland-ConfigActions.cpp:1567 |")),
             False, must=["rows:Q09"], exact=["rows:Q09"])
        case("Q row with a fourth cell", tree(SYN_BASE + GB.replace(qrow("Q09"), qrow("Q09").replace(b"` |", b"` | extra |"))), False,
             must=["rows:Q09"], exact=["rows:Q09"])
        case("CRLF after the prefix is tolerated", tree(SYN_BASE + GB.replace(b"\n", b"\r\n")), True, exact=[])
        case("pin tampered (one trailing space at EOF)", tree(good_entry, **{tables["pin"]: pin_blob + b" "}), False,
             must=["pin"], exact=["pin"])
        case("pin absent", {k: v for k, v in tree(good_entry).items() if k != tables["pin"]}, False, must=["pin"],
             exact=["pin"])
        case("frozen-tables.json differs (whitespace appended)", tree(good_entry, **{TABLES_PATH: tables_blob + b"\n"}),
             False, must=["tables_sha"], exact=["tables_sha"])
        case("frozen-tables.json absent", {k: v for k, v in tree(good_entry).items() if k != TABLES_PATH}, False,
             must=["tables_sha", "pin"], mustnot=["prefix", "readme"])
        case("entry absent", {k: v for k, v in tree(good_entry).items() if k != ENTRY_PATH}, False,
             must=["prefix", "p23"], prefix="changed")
        case("entry truncated below the base", tree(SYN_BASE[:-5]), False, must=["prefix"], prefix="changed")
        case("README absent", {k: v for k, v in tree(good_entry).items() if k != README_PATH}, False,
             must=["readme"], exact=["readme"])
        case("README names P23 on a different line than the entry",
             tree(good_entry, SYN_README_BASE + b"P23 elsewhere\n"), False, must=["readme"], exact=["readme"])
        case("block appended without a blank line before the heading", tree(SYN_BASE + GB[1:]), True, exact=[])

        ok_all = True
        for name, files, expect_met, must, mustnot, prefix, exact in cases:
            c = commit_tree(files, base)
            fields, missed = evaluate(D, c, work, base_commit=base)
            line, verdict = render(c[:12], fields, missed)
            met = verdict == "TARGET_MET"
            good = met == expect_met
            good &= all(m in missed for m in must)
            good &= not any(m in missed for m in mustnot)
            if prefix is not None:
                good &= fields["prefix"] == prefix
            if exact is not None:
                good &= missed == list(exact)
            ok_all &= good
            results.append("%s %s\n    -> %s" % ("PASS" if good else "FAIL", name, line))
        # the real-base path: --repo = a clone holding base 3b55b6e is the lane's own business (see CLI run)
        # CLI end-to-end on the good commit: exit status and stdout grammar with an explicit stand-in base is not
        # available (the base is a constant), so the CLI exit paths are exercised on setup errors below.
        cli = [
            ("CLI usage error", [sys.executable, "-I", os.path.abspath(__file__)], 2, "MADO_P19_FIX: SETUP usage"),
            ("CLI unresolvable rev", [sys.executable, "-I", os.path.abspath(__file__), "--repo", D, "--rev",
                                      "deadbeef" * 5, "--work", work], 2, "MADO_P19_FIX: SETUP unresolvable_rev"),
            ("CLI rev starting with a dash", [sys.executable, "-I", os.path.abspath(__file__), "--repo", D, "--rev",
                                              "--help", "--work", work], 2, "MADO_P19_FIX: SETUP bad_rev"),
            ("CLI base commit absent in a scratch repo (setup, not a verdict)",
             [sys.executable, "-I", os.path.abspath(__file__), "--repo", D, "--rev", base, "--work", work], 2,
             "MADO_P19_FIX: SETUP base_commit_absent"),
            ("CLI not a repo", [sys.executable, "-I", os.path.abspath(__file__), "--repo", os.path.join(work, "nonexistent"),
                                "--rev", "HEAD", "--work", work], 2, "MADO_P19_FIX: SETUP not_a_repo"),
        ]
        for name, argv, want_rc, want_out in cli:
            p = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            got = p.stdout.decode("utf-8", "replace").strip()
            good = p.returncode == want_rc and got == want_out
            ok_all &= good
            results.append("%s %s\n    -> rc=%d %s" % ("PASS" if good else "FAIL", name, p.returncode, got))
    finally:
        shutil.rmtree(D, ignore_errors=True)
    passed = sum(1 for r in results if r.startswith("PASS"))
    for r in results:
        print(r)
    print("MADO_P19_FIX_SELFTEST: %d/%d passed" % (passed, len(results)))
    return 0 if passed == len(results) else 1


def parse_args(argv):
    opts = {"repo": None, "rev": None, "work": None, "selftest": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--selftest":
            opts["selftest"] = True
            i += 1
        elif a in ("--repo", "--rev", "--work") and i + 1 < len(argv):
            opts[a[2:]] = argv[i + 1]
            i += 2
        else:
            return None
    return opts


def main(argv):
    opts = parse_args(argv)
    if opts is None or not opts["repo"] or not opts["work"]:
        return emit_setup("usage")
    try:
        if opts["selftest"]:
            return selftest(opts["repo"], opts["rev"] or "HEAD", opts["work"])
        if not opts["rev"]:
            return emit_setup("usage")
        fields, missed = evaluate(opts["repo"], opts["rev"], opts["work"])
    except Setup as e:
        return emit_setup(str(e))
    line, verdict = render(opts["rev"], fields, missed)
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

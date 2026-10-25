#!/usr/bin/env python3
"""CritC2Cheat: build the cheapest fabricated set that scores admitted=1/1 on
PRED-C2-r40-v1, and probe the cheaper-path hypotheses.

Every fixture is D=$(mktemp -d), git init -q, toplevel verified equal to D,
throwaway identity passed with -c (never written to config), removed at the end.
Lane is read only (git show / git archive).
"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "9fc511ddce708327377161202f358ce37dc266ba"
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r40-forms-entry.py")
ENTRY = "corpus/knowledge/hyprctl-getoption-native-forms-r40.md"
TOOL = "tools/mado-options.py"
FETCH40 = ".ufo/waves/round-40/fetch/"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
IDENT = ["-c", "user.name=crit", "-c", "user.email=crit@crit.invalid"]
FORMS = "forms int=1 float=0 str=0 custom=0"
LABELS = "labels agreement=1 agreement*=0 mismatch=0 config-only=0 live-default=0"
QUOTE = "int=1 float=0 str=0"          # 3 words, substring of FORMS
DUMMY_TOOL = "#!/usr/bin/env python3\n# dummy\nprint('x')\n"


def lane_show(path, rev=BASE):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True, env=ENV)
    if p.returncode:
        raise SystemExit("lane_show failed %s: %s" % (path, p.stderr))
    return p.stdout.decode()


def init_fixture():
    d = tempfile.mkdtemp(prefix="crit-c2cheat-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ENV)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True,
                         env=ENV).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("toplevel mismatch %s != %s" % (top, d))
    return d


def real_base_tree(d):
    p1 = subprocess.Popen(["git", "-C", LANE, "archive", BASE],
                          stdout=subprocess.PIPE, env=ENV)
    p2 = subprocess.Popen(["tar", "-x", "-C", d], stdin=p1.stdout, env=ENV)
    p1.stdout.close()
    if p2.wait() or p1.wait():
        raise SystemExit("archive extract failed")


def commit_all(d, files, msg):
    for rel, text in files.items():
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=ENV)
    subprocess.run(["git", "-C", d, *IDENT, "commit", "-q", "-m", msg,
                    "--no-gpg-sign"], check=True, env=ENV)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True,
                          env=ENV).stdout.strip()


def tree_of(d, rev):
    return subprocess.run(["git", "-C", d, "rev-parse", rev + "^{tree}"],
                          check=True, capture_output=True, text=True,
                          env=ENV).stdout.strip()


def row(i, loc, kind="docs"):
    return ("| %s | %s | %s | A | s | a | t | mined | 2026-10-25 | 90d | %s |"
            % (i, loc, kind, ENTRY))


def held_row(base_sources, i):
    for line in base_sources.splitlines():
        if line.startswith("| %s |" % i):
            return line.rstrip()[:-1].rstrip() + ", " + ENTRY + " |"
    raise SystemExit("held row %s not found" % i)


def entry_text(ids):
    return "\n".join(["source: %s" % i for i in ids] +
                     ["verified-at: 2026-10-25", "recheck: 90d",
                      " ".join(ids) + " " + FORMS, LABELS]) + "\n"


def receipt_text(tool_sha):
    return "%s\n%s\n%s\n" % (tool_sha, FORMS, LABELS)


def gate(i, path, blob, quote=QUOTE):
    return ('GATE %s receipt=%s sha256=%s quote="%s"'
            % (i, path, hashlib.sha256(blob.encode()).hexdigest(), quote))


def lesson(gates):
    return "## Gate\n\n" + "\n".join(gates) + "\n"


def insert_rows(sources, rows):
    out, done = [], False
    for line in sources.splitlines():
        if not done and line.startswith("## ") and line.strip() != "## Registry":
            out.extend(rows)
            out.append("")
            done = True
        out.append(line)
    if not done:
        out.extend(rows)
    return "\n".join(out) + "\n"


def readme_row():
    return "| `knowledge/%s` | cheat |" % os.path.basename(ENTRY)


def cost(files_old, files_new):
    """files touched, authored lines, authored bytes (delta)."""
    touched = [p for p in files_new
               if files_old.get(p) != files_new[p]]
    lines = bytes_ = 0
    for p in touched:
        old = files_old.get(p, "")
        new = files_new[p]
        bytes_ += len(new) - len(old)
        if old:
            sm = difflib.SequenceMatcher(None, old.splitlines(),
                                         new.splitlines())
            lines += sum(j2 - j1 for t, i1, i2, j1, j2 in sm.get_opcodes()
                         if t in ("insert", "replace"))
        else:
            lines += len(new.splitlines())
    return len(touched), lines, bytes_, sorted(touched)


def run(name, base_files, after_files, note, expect, real=False):
    d = init_fixture()
    try:
        if real:
            real_base_tree(d)
        if base_files:
            commit_all(d, base_files, "base")
        elif real:
            commit_all(d, {}, "base")
        b = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                           capture_output=True, text=True,
                           env=ENV).stdout.strip()
        if real:
            lane_tree = subprocess.run(
                ["git", "-C", LANE, "rev-parse", BASE + "^{tree}"],
                check=True, capture_output=True, text=True,
                env=ENV).stdout.strip()
            tree_ok = tree_of(d, b) == lane_tree
        else:
            tree_ok = None
        old = {}
        for rel in after_files:
            fp = os.path.join(d, rel)
            if os.path.exists(fp):
                with open(fp) as fh:
                    old[rel] = fh.read()
        a = commit_all(d, after_files, "after")
        nf, nl, nb, paths = cost(old, after_files)
        delta = {}
        for rel in paths:
            new = after_files[rel]
            if rel not in old:
                delta[rel] = new
            else:
                sm = difflib.SequenceMatcher(None, old[rel].splitlines(),
                                             new.splitlines())
                add = []
                for t, i1, i2, j1, j2 in sm.get_opcodes():
                    if t in ("insert", "replace"):
                        add.extend(new.splitlines()[j1:j2])
                delta[rel] = "\n".join("+ " + l for l in add) + "\n"
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ENV)
        out = p.stdout.strip().splitlines()
        last = out[-1] if out else ""
        cls = [l for l in out if " clauses=" in l]
        cls = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        got = "admitted=1/1" if "admitted=1/1" in last else (
            "admitted=0/1" if "admitted=0/1" in last else last)
        ok = (got == expect)
        return {
            "variant": name, "note": note, "expect": expect, "got": got,
            "rc": p.returncode, "clauses": cls, "files": nf,
            "authored_lines": nl, "authored_bytes": nb, "paths": paths,
            "base_tree_equals_frozen": tree_ok, "ok": ok,
            "counter_tail": [l for l in out if "clause=" in l],
            "counter_last": last, "delta": delta, "stdout": p.stdout,
        }
    finally:
        shutil.rmtree(d, ignore_errors=True)


def cheat_real_base(cited=("S900", "S901", "S902", "S903"), own="S902",
                    held=(), gate_path=None, quote=QUOTE):
    """Fabricated set on the real frozen base tree (tool untouched)."""
    src = lane_show("corpus/SOURCES.md")
    readme = lane_show("corpus/README.md")
    tool_sha = hashlib.sha256(lane_show(TOOL).encode()).hexdigest()
    rec = receipt_text(tool_sha)
    gpath = gate_path or (FETCH40 + "cheat.receipt.txt")
    new = [i for i in cited if i not in held]
    if held:
        lines = src.splitlines()
        for h in held:
            for k, line in enumerate(lines):
                if line.startswith("| %s |" % h):
                    lines[k] = held_row(src, h)
                    break
        src = "\n".join(lines) + "\n"
    rows = [row(i, "zz%d" % k, "own-work" if i == own else "docs")
            for k, i in enumerate(new)]
    gates = [gate(i, gpath, rec, quote) for i in cited]
    files = {ENTRY: entry_text(cited), gpath: rec,
             "corpus/lessons/round-40.md": lesson(gates),
             "corpus/SOURCES.md": insert_rows(src, rows),
             "corpus/README.md": readme + readme_row() + "\n"}
    return files


def main():
    res = []
    # V1: the task's literal ask - minimal fixture, dummy 3-line tool.
    b = {
        "corpus/SOURCES.md": "# Sources\n\n## Registry\n\n"
        "| id | source | kind | tier | scope | anchor | teaches | status "
        "| opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---"
        "|---|\n\n## Paths\n",
        "corpus/README.md": "# Coverage\n",
        TOOL: DUMMY_TOOL,
    }
    sha = hashlib.sha256(DUMMY_TOOL.encode()).hexdigest()
    ids = ("S900", "S901", "S902", "S903")
    rec = receipt_text(sha)
    a = {ENTRY: entry_text(ids), FETCH40 + "cheat.receipt.txt": rec,
         "corpus/lessons/round-40.md": lesson(
             [gate(i, FETCH40 + "cheat.receipt.txt", rec) for i in ids]),
         "corpus/SOURCES.md": insert_rows(
             b["corpus/SOURCES.md"],
             [row(i, "zz%d" % k, "own-work" if i == "S902" else "docs")
              for k, i in enumerate(ids)]),
         "corpus/README.md": b["corpus/README.md"] + readme_row() + "\n"}
    res.append(run("V1-minimal-dummy-tool", b, a,
                   "task's literal ask: 3-line dummy tool, empty base registry",
                   "admitted=1/1"))
    # V2/V5: real frozen base tree, committed tool untouched, one receipt,
    # one line carrying all ids + the quote (cheapest found).
    res.append(run("V5-cheapest-realbase", None, cheat_real_base(), "",
                   "admitted=1/1", real=True))
    # M4: control-P shape (4 receipts, 4 quotes, 4 OBS lines) for cost compare.
    def control_p_shape():
        src = lane_show("corpus/SOURCES.md")
        readme = lane_show("corpus/README.md")
        tool_sha = hashlib.sha256(lane_show(TOOL).encode()).hexdigest()
        ids4 = ("S900", "S901", "S902", "S903")
        qs = ["quote alpha for one", "quote beta for two",
              "quote gamma for three", "quote delta for four"]
        files = {}
        gates = []
        for i, q in zip(ids4, qs):
            blob = ("%s\n%s\n%s\n%s\n" % (tool_sha, FORMS, LABELS, q)
                    if i == "S902" else q + " evidence\n")
            p = FETCH40 + i + ".txt"
            files[p] = blob
            gates.append(gate(i, p, blob, q))
        files[ENTRY] = "\n".join(
            ["source: %s" % i for i in ids4] +
            ["verified-at: 2026-10-25", "recheck: 90d"] +
            ["**OBS** %s %s." % (i, q) for i, q in zip(ids4, qs)] +
            [FORMS, LABELS]) + "\n"
        files["corpus/lessons/round-40.md"] = lesson(gates)
        files["corpus/SOURCES.md"] = insert_rows(
            src, [row(i, "zz%d" % k, "own-work" if i == "S902" else "docs")
                  for k, i in enumerate(ids4)])
        files["corpus/README.md"] = readme + readme_row() + "\n"
        return files
    res.append(run("M4-controlP-shape", None, control_p_shape(),
                   "4 receipts, 4 quotes, 4 OBS lines (declared residual shape)",
                   "admitted=1/1", real=True))
    # N1: round-39 receipt path (bytes committed there, sha correct).
    res.append(run("N1-round39-path", None,
                   cheat_real_base(gate_path=".ufo/waves/round-39/fetch/"
                                   "cheat.receipt.txt"),
                   "gate path under round-39/fetch", "admitted=0/1", real=True))
    # N2: held rows S162/S173 treated as the 'new' ids (opened rewritten).
    def held_as_new(inplace, fix_used=False):
        src = lane_show("corpus/SOURCES.md")
        readme = lane_show("corpus/README.md")
        tool_sha = hashlib.sha256(lane_show(TOOL).encode()).hexdigest()
        rec = receipt_text(tool_sha)
        ids4 = ("S162", "S173", "S900", "S901")
        rows = []
        for i in ("S162", "S173"):
            base_row = [l for l in src.splitlines() if l.startswith("| %s |" % i)][0]
            cells = base_row.split("|")
            cells[9] = " 2026-10-25 "      # opened -> pretend it is new
            if fix_used:
                cells[11] = cells[11].rstrip() + ", " + ENTRY + " "
            rows.append("|".join(cells))
        if inplace:
            lines = src.splitlines()
            for i, r in zip(("S162", "S173"), rows):
                for k, line in enumerate(lines):
                    if line.startswith("| %s |" % i):
                        lines[k] = r
                        break
            src = "\n".join(lines) + "\n"
            rows = []
        rows += [row("S900", "zz1"), row("S901", "zz2", "own-work")]
        gates = [gate(i, FETCH40 + "cheat.receipt.txt", rec) for i in ids4]
        return {ENTRY: entry_text(ids4), FETCH40 + "cheat.receipt.txt": rec,
                "corpus/lessons/round-40.md": lesson(gates),
                "corpus/SOURCES.md": insert_rows(src, rows),
                "corpus/README.md": readme + readme_row() + "\n"}
    res.append(run("N2-held-as-new-inplace", None, held_as_new(True),
                   "S162/S173 rows rewritten in place with opened 2026-10-25",
                   "admitted=0/1", real=True))
    res.append(run("N2c-held-reopened-usedby-fixed", None, held_as_new(True, True),
                   "opened re-dated AND used-by fixed: only cells[:10] differs",
                   "admitted=0/1", real=True))
    res.append(run("N2b-held-as-new-appended", None, held_as_new(False),
                   "S162/S173 rewritten copies appended beside the base rows",
                   "admitted=0/1", real=True))
    # N3: held rows done properly (cells 1-10 byte-equal, used-by appended).
    res.append(run("N3-held-proper", None,
                   cheat_real_base(cited=("S162", "S173", "S900", "S901"),
                                   own="S901", held=("S162", "S173")),
                   "S162/S173 copied byte-equal + used-by appended, 2 new ids",
                   "admitted=1/1", real=True))
    # N4: all four cited ids held -> no new id at all.
    res.append(run("N4-held-only", None,
                   cheat_real_base(cited=("S001", "S002", "S162", "S173"),
                                   own=None,
                                   held=("S001", "S002", "S162", "S173")),
                   "4 held ids, zero new", "admitted=0/1", real=True))
    for r in res:
        print(json.dumps({k: v for k, v in r.items()
                          if k != "counter_tail"}, sort_keys=True))
        print("  clauses: %s" % r["clauses"])
        for t in r["counter_tail"]:
            print("   ", t)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    return 0 if all(r["ok"] for r in res) else 1


if __name__ == "__main__":
    sys.exit(main())

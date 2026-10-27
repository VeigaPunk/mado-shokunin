#!/usr/bin/env python3
"""Falsify34 -- C1 uniqueness/population falsification fixture driver.

Builds seat-local throwaway git fixtures and runs the REAL round-51 counter
(quality/counters/c1-r51-ledger.py) and the REAL gate (quality/check-tool-ledger.py)
against ledger variants. Source lane is read-only; all writes stay in scratch.

Attack: a ledger that lists the same population instrument multiple times with
distinct `:line' anchors in cell 1 is semantically duplicated but string-distinct
under the r51 parser, so a `dup'-style exact-string uniqueness signal reports 0.
"""

import importlib.util
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r52/Falsify34"
COUNTER = os.path.join(LANE, "quality", "counters", "c1-r51-ledger.py")
GATE = os.path.join(LANE, "quality", "check-tool-ledger.py")
LEDGER_REL = "quality/tool-ledger.md"

sys.path.insert(0, SCRATCH)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r51 = load(COUNTER, "c1_r51_ledger")
gate = load(GATE, "check_tool_ledger")

POP_FILES = {
    "tools/alpha-tool.py": "# alpha tool\n",
    "tools/beta.py": "# beta tool\n",
    "quality/check-a.py": "# check a\n",
    "quality/counters/c1-x.py": "# counter x\n",
    # the gate itself is part of the population in fixture and production
}
BASENAMES = ["alpha-tool.py", "beta.py", "check-a.py", "c1-x.py",
             "check-tool-ledger.py"]
DESC = {
    "tools/alpha-tool.py": "Read-only resolver of the alpha table; prints JSON from file bytes.",
    "tools/beta.py": "Static census of beta subscribers; prints the drop markers.",
    "quality/check-a.py": "Gate that re-derives the A axis table and fails on drift.",
    "quality/counters/c1-x.py": "Round-x counter: scores the x predicate against fixtures.",
    "quality/check-tool-ledger.py": "PRED-C1-r51 gate: verifies the tool ledger is complete.",
}


def sh(cmd, cwd=None, env=None):
    e = dict(os.environ)
    e.update({"GIT_AUTHOR_NAME": "falsify34", "GIT_AUTHOR_EMAIL": "f34@fixture",
              "GIT_COMMITTER_NAME": "falsify34", "GIT_COMMITTER_EMAIL": "f34@fixture",
              "LC_ALL": "C.UTF-8"})
    if env:
        e.update(env)
    p = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("cmd %r rc=%s\nstdout=%s\nstderr=%s" %
                         (cmd, p.returncode, p.stdout, p.stderr))
    return p.stdout


def build_repo(name, ledger_text):
    root = os.path.join(SCRATCH, name)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    sh(["git", "init", "-q", "-b", "main"], cwd=root)
    for rel, content in POP_FILES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(content)
    # accountability doc naming every basename (non-ledger, resolves, non-self)
    os.makedirs(os.path.dirname(os.path.join(root, "PROVINCE.md")), exist_ok=True)
    with open(os.path.join(root, "PROVINCE.md"), "w") as fh:
        fh.write("# fixture province\n" + " ".join(BASENAMES) + "\n")
    # the real gate bytes, so the r51 counter can run its selftest+ledger check
    shutil.copyfile(GATE, os.path.join(root, "quality/check-tool-ledger.py"))
    os.makedirs(os.path.dirname(os.path.join(root, LEDGER_REL)), exist_ok=True)
    with open(os.path.join(root, LEDGER_REL), "w") as fh:
        fh.write(ledger_text)
    sh(["git", "add", "-A"], cwd=root)
    sh(["git", "commit", "-q", "-m", name], cwd=root)
    return root, sh(["git", "rev-parse", "HEAD"], cwd=root).strip()


def row(path, desc, ptr):
    return "| `%s` | %s | `%s` |" % (path, desc, ptr)


def ledger(rows):
    lines = ["# fixture tool ledger", "",
             "| instrument | description | accountability pointer |",
             "|---|---|---|"]
    lines.extend(rows)
    return "\n".join(lines) + "\n"


ALL_PATHS = list(POP_FILES.keys()) + ["quality/check-tool-ledger.py"]


def rows_normal():
    return [row(p, DESC[p], "PROVINCE.md:1") for p in ALL_PATHS]


def rows_dup_exact():
    out = rows_normal()
    out.insert(1, row("tools/alpha-tool.py", DESC["tools/alpha-tool.py"], "PROVINCE.md:1"))
    return out


def rows_dup_anchored():
    out = []
    for p in ALL_PATHS:
        out.append(row(p, DESC[p], "PROVINCE.md:1"))
        if p == "tools/alpha-tool.py":
            out.append(row("tools/alpha-tool.py:1", DESC[p], "PROVINCE.md:1"))
            out.append(row("tools/alpha-tool.py:2", DESC[p], "PROVINCE.md:1"))
    return out


def rows_full_bypass():
    """Every population instrument 3x with rotating :line anchors; non-self,
    resolvable pointers; per-instrument context descriptions."""
    out = []
    for p in ALL_PATHS:
        for anchor in ("", ":1", ":2"):
            out.append(row(p + anchor, DESC[p], "PROVINCE.md:1"))
    return out


VARIANTS = [
    ("A-normal", rows_normal()),
    ("B-dup-exact", rows_dup_exact()),
    ("C-dup-anchored", rows_dup_anchored()),
    ("D-full-bypass", rows_full_bypass()),
]


def analyze(root, rev, ledger_text):
    files = set(r51.listing(root, rev))
    pop = r51.population(sorted(files))
    rows = r51.parse_rows(ledger_text)
    mine, details = r51.describe(pop, rows, root, rev, files)
    blobs = gate.tree(root, rev)
    gpop = gate.population(blobs)
    grows, uncovered, dangling, bad_pointer, empty_desc, findings = gate.evaluate(
        gpop, ledger_text, blobs, root, rev)
    return {
        "pop": pop, "files": files, "rows": rows, "mine": mine, "details": details,
        "gate": dict(rows=grows, uncovered=uncovered, dangling=dangling,
                      bad_pointer=bad_pointer, empty_desc=empty_desc,
                      findings=findings),
    }


# --- predicate model: the four checks frozen in round-52 C1, implemented in the
# --- natural inheritance from the r51 counter: population-membership gate first
# --- (describe() `continue`s on out-of-population rows, so pointer/self/context
# --- checks never see them), then exact-string uniqueness on parsed cell-1 paths
# --- (no norm_path/LINE_SUFFIX normalization).
CTX = re.compile(r"(resolver|census|gate|counter|verifies|prints|scores|check)", re.I)


def frozen_c1_model(res, root, rev):
    rows, files, pop = res["rows"], res["files"], res["pop"]
    seen, dup, out_of_pop = set(), 0, 0
    bad_pointer, self_pointer, no_context = 0, 0, 0
    cache = {}
    for r in rows:
        if r["path"] not in pop:
            out_of_pop += 1
            continue
        if r["path"] in seen:
            dup += 1
            continue
        seen.add(r["path"])
        if not r51.pointer_resolves(root, rev, files, r["path"], r["pointer"], cache):
            bad_pointer += 1
        toks = [t for t in r51.pointer_tokens(r["pointer"])]
        if any(os.path.normpath(t) == LEDGER_REL for t in toks):
            self_pointer += 1
        stem = os.path.basename(r["path"]).rsplit(".", 1)[0]
        if stem not in r["desc"] and not CTX.search(r["desc"]):
            no_context += 1
    return dict(dup=dup, bad_pointer=bad_pointer, self_pointer=self_pointer,
                no_context=no_context, out_of_pop_skipped=out_of_pop,
                verdict="TARGET_MET" if not any((dup, bad_pointer,
                                                self_pointer, no_context))
                        else "TARGET_MISSED")


def main():
    print("loaded counter:", COUNTER)
    print("loaded gate   :", GATE)
    print("=" * 78)
    for name, rows in VARIANTS:
        root, rev = build_repo(name, ledger(rows))
        with open(os.path.join(root, LEDGER_REL)) as fh:
            text = fh.read()
        res = analyze(root, rev, text)
        print("VARIANT %s  rev=%s" % (name, rev[:12]))
        print("  population=%d  r51_rows=%d  gate_rows=%d" %
              (len(res["pop"]), len(res["rows"]), res["gate"]["rows"]))
        print("  r51 counter : dup=%d dangling=%d uncovered=%d bad_pointer=%d empty_desc=%d" % (
            res["mine"]["dup"], res["mine"]["dangling"], res["mine"]["uncovered"],
            res["mine"]["bad_pointer"], res["mine"]["empty_desc"]))
        for d in res["details"]:
            print("    detail:", d)
        print("  gate        : dangling=%r uncovered=%r bad_pointer=%r empty_desc=%r" % (
            res["gate"]["dangling"], res["gate"]["uncovered"],
            res["gate"]["bad_pointer"], res["gate"]["empty_desc"]))
        for f in res["gate"]["findings"]:
            print("    gate finding:", f)
        model = frozen_c1_model(res, root, rev)
        print("  frozen-C1 model (4 named checks, exact-string uniqueness): %s" % model)
        print("-" * 78)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Static scratch-rule-4 scanner for drafted python tools (seat ExecDiskHygiene, round 51).

Read-only: it opens the scanned files and prints findings; it writes nothing except the
optional --json report, and it creates no temporary directory at all (no mkdtemp, no
TemporaryFile), so it cannot itself violate scratch rule 4.

Scratch rule 4 (as amended at round 49: corpus/lessons/round-48.md:372, SCORECARD.md:2728):
a counter/probe/gate must honour TMPDIR, must accept an explicit scratch argument, and must
refuse a `--work`/`TMPDIR` under /tmp, /var/tmp or /dev/shm (a hardcoded /tmp is a routed
defect).

Classes (one per hit):
  hardcoded-tmp-write     a /tmp, /var/tmp or /dev/shm literal used as a HOST write target
                          (mkdtemp(dir=), open(), Path(), mkdir, clone, dump)          -> DEFECT
  implicit-tempdir-<fn>   mkdtemp/TemporaryDirectory/NamedTemporaryFile/TemporaryFile with
                          no dir= argument: the write lands in the ambient tempdir and is
                          only TMPDIR-safe if TMPDIR is validated first                -> REVIEW
  gettempdir-write        tempfile.gettempdir() used as a write target                 -> REVIEW
  sandbox-argv            the literal is a bwrap/sandbox argument (--tmpfs /tmp, --bind,
                          --chdir, --setenv TMPDIR /tmp): the /tmp is private to the
                          sandbox, not the host's                                        -> INFO
  refusal-list            the literal is an entry of a refusal check (for bad in (...)) -> INFO
  ambient-no-contract     no TMPDIR read, no --work/--scratch argument, no sandbox      -> REVIEW

Verdict per file: DEFECT if any hardcoded-tmp-write; REVIEW if any implicit-tempdir /
gettempdir-write / ambient-no-contract finding; CLEAN once the file either validates TMPDIR
or takes a scratch/work argument and every tempfile call carries dir=.

Usage:
  python3 -I hygiene-scan.py --root <dir> [--json <path>]
"""
import argparse
import json
import os
import re
import sys

RE_LITERAL = re.compile(r"""['"](/tmp|/var/tmp|/dev/shm)['"/]""")
RE_TEMPFILE = re.compile(r"\b(mkdtemp|TemporaryDirectory|NamedTemporaryFile|TemporaryFile)\s*\(")
RE_GETTEMPDIR = re.compile(r"\btempfile\.gettempdir\s*\(")
RE_WRITE = re.compile(
    r"\b(open|mkdtemp|mkdir|makedirs|TemporaryDirectory|NamedTemporaryFile|TemporaryFile|"
    r"dump|write_text|write_bytes|shutil\.copy|shutil\.move|Path)\b"
)
RE_REFUSAL = re.compile(
    r"(for\s+bad\b|\bbad\b|forbid|refus|denied|disallow|banned|_BAD|BAD_)", re.I
)
RE_SANDBOX = re.compile(
    r"(--tmpfs|--ro-bind|--bind|--dev-bind|--dev\b|--proc\b|--setenv|--chdir|--unshare|bwrap)"
)
RE_TMPDIR = re.compile(r"\bTMPDIR\b")
RE_WORKARG = re.compile(r"""["']--(work|scratch)["']""")
RE_SELFTEST = re.compile(r"""["']--selftest["']""")


def classify_literal(line):
    if RE_SANDBOX.search(line):
        return "sandbox-argv"
    if RE_REFUSAL.search(line) and not RE_WRITE.search(line):
        return "refusal-list"
    if RE_WRITE.search(line):
        return "hardcoded-tmp-write"
    # a bare tuple of tmpish constants, e.g. TMPISH = ("/tmp", "/var/tmp", "/dev/shm")
    return "refusal-list" if re.search(r"[(,]\s*['\"](/tmp|/var/tmp)", line) else "mention"


def scan_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    lines = text.splitlines()
    findings = []
    for i, line in enumerate(lines, 1):
        if RE_LITERAL.search(line):
            findings.append(
                {"line": i, "class": classify_literal(line), "text": line.strip()[:200]}
            )
        m = RE_TEMPFILE.search(line)
        if m and "dir=" not in line:
            findings.append(
                {
                    "line": i,
                    "class": "implicit-tempdir-" + m.group(1),
                    "text": line.strip()[:200],
                }
            )
        if RE_GETTEMPDIR.search(line) and RE_WRITE.search(line):
            findings.append(
                {"line": i, "class": "gettempdir-write", "text": line.strip()[:200]}
            )

    honours_tmpdir = bool(RE_TMPDIR.search(text))
    takes_work = bool(RE_WORKARG.search(text))
    has_selftest = bool(RE_SELFTEST.search(text))
    refuses_tmpish = any(f["class"] == "refusal-list" for f in findings)
    uses_sandbox = any(f["class"] == "sandbox-argv" for f in findings)

    if not honours_tmpdir and not takes_work and not uses_sandbox:
        findings.append({"line": 0, "class": "ambient-no-contract", "text": "no TMPDIR, no --work/--scratch, no sandbox"})

    classes = {f["class"] for f in findings}
    hard = sum(1 for f in findings if f["class"] == "hardcoded-tmp-write")
    if hard:
        verdict = "DEFECT"
    elif classes & {"ambient-no-contract", "gettempdir-write"} or any(
        c.startswith("implicit-tempdir") for c in classes
    ):
        verdict = "REVIEW"
    else:
        verdict = "CLEAN"

    return {
        "path": path,
        "bytes": len(text.encode("utf-8")),
        "lines": len(lines),
        "verdict": verdict,
        "hardcoded_tmp_writes": hard,
        "honours_TMPDIR": honours_tmpdir,
        "refuses_tmpish": refuses_tmpish,
        "takes_work_arg": takes_work,
        "uses_sandbox": uses_sandbox,
        "has_selftest": has_selftest,
        "findings": findings,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="directory tree to scan for *.py")
    ap.add_argument("--json", default=None, help="write the report JSON here (optional)")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("hygiene-scan: not a directory: %s" % root, file=sys.stderr)
        return 2
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for name in sorted(filenames):
            if name.endswith(".py"):
                files.append(os.path.join(dirpath, name))
    if not files:
        print("hygiene-scan: no .py under %s" % root, file=sys.stderr)
        return 2

    results = [scan_file(p) for p in files]
    counts = {"CLEAN": 0, "REVIEW": 0, "DEFECT": 0}
    for r in results:
        counts[r["verdict"]] += 1
    for r in results:
        print(
            "%-52s %-7s hard_writes=%d TMPDIR=%s refuse_tmpish=%s work_arg=%s sandbox=%s selftest=%s"
            % (
                os.path.relpath(r["path"], root),
                r["verdict"],
                r["hardcoded_tmp_writes"],
                "yes" if r["honours_TMPDIR"] else "no",
                "yes" if r["refuses_tmpish"] else "no",
                "yes" if r["takes_work_arg"] else "no",
                "yes" if r["uses_sandbox"] else "no",
                "yes" if r["has_selftest"] else "no",
            )
        )
        for f in r["findings"]:
            print("    L%-5d %-28s %s" % (f["line"], f["class"], f["text"]))
    print(
        "SCAN files=%d clean=%d review=%d defect=%d root=%s"
        % (len(results), counts["CLEAN"], counts["REVIEW"], counts["DEFECT"], root)
    )
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"root": root, "counts": counts, "files": results}, fh, indent=1)
            fh.write("\n")
    return 1 if counts["DEFECT"] else 0


if __name__ == "__main__":
    sys.exit(main())

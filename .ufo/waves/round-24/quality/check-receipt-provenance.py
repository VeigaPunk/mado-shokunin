#!/usr/bin/env python3
"""check-receipt-provenance.py -- RECEIPT gate for round-23 lesson M23-5 (round-24 repair).

Usage:
    python3 -I check-receipt-provenance.py [--json] [--notes] RECEIPT [RECEIPT ...]
    python3 -I check-receipt-provenance.py --selftest

Contract
--------
exit 0 iff every receipt named on the command line passes both rules:

  R1  the receipt names the measured tool by `sha256:` followed by 64 hex digits, or by
      a full 64-hex sha256 literal, on a line that also names the tool (a `--tool`
      argument, a `*/tools/*` path, or a `*tool*.py` / `*tool*.sh` filename).
  R2  every result/data path the receipt writes or reads is absolute: a literal path
      starting with `/`, or a `$VAR` / `${VAR}` prefix whose assignment in the same
      receipt is an absolute literal. A `~` prefix is not absolute. A truncated
      digest (`1234abcd...`) never counts for R1.

exit 1 otherwise, printing one `FAIL <receipt>:<line>: R<n> <reason>` per violation and
a final `verdict=fail reasons=<n>`. A clean receipt prints `PASS <receipt>` and the
final line is `verdict=pass reasons=0`.

Why (round-23 lesson M23-5)
---------------------------
An attack run wrote probe results through a path that did not resolve where a later
read looked, so it read files left by an earlier tool and briefly reported regressions
that were not in the measured bytes. The recorded repair: absolute result paths, the
result files deleted before each run, and the measured tool's sha256 printed.

Extraction (text only, deterministic; the receipt is never executed)
--------------------------------------------------------------------
R1: tokens `sha256:\\s*<64 hex>` and bare `<64 hex>` (hex-boundary guarded). Truncated
    digests (7-12 hex followed by `...` or the ellipsis character) are reported and
    never counted.
R2: write positions -- shell redirections `>`, `>>`, `2>`, `&>`; flags `--out`,
    `--output`, `-o`, `--result`, `--receipt`, `--write`; Python `open(P`,
    `Path(P).write_text/write_bytes`.
    read positions -- `cat P`; Python `open(P`, `Path(P).read_text/read_bytes`,
    `json.load(open(P`.
    harness data arguments -- path-like positional arguments (contain `/` or end
    `.json`/`.jsonl`/`.txt`) passed to the measurement harnesses `probe.py`, `run.py`,
    `measure.py`, `deliver.py`, `drive.py`, `gen.py`, `tabulate.py`, `mkprobes*.py`,
    `mkfinal.py`.
    Staging commands (`cd`, `mkdir`, `cp`, `rm`, `git clone`) are reported only under
    `--notes` and never fail the gate: they move bytes, they do not name a result.

Boundaries this checker does not cross (stated, not papered over)
-----------------------------------------------------------------
* Runtime-built paths (command substitution, concatenation, `$1` in a directory name)
  are judged by their literal prefix only; the checker does not expand them.
* `cd <relative>` changes what a later relative path means; the checker reports such a
  `cd` as a note but does not simulate cwd, so a receipt with no relative data paths is
  unaffected while one with them fails on the paths themselves.
* The checker does not prove the digest equals the tool's true bytes. Pairing the
  pinned digest with `sha256sum` at run time stays the receipt's job; this gate only
  proves the receipt states a full digest and uses absolute result paths.
"""

import argparse
import json
import os
import re
import shutil
import sys
import tempfile

HEX64 = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])")
LABELLED = re.compile(r"sha256:[ \t]*([0-9a-fA-F]{64})(?![0-9a-fA-F])")
TRUNCATED = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{7,12}(?:\.\.\.|\u2026)")
TOOL_HINT = re.compile(
    r"(--tool\b|--before-tool\b|(?:^|[\s\"'(=])/?tools/|[\w./-]*tool[\w./-]*\.(?:py|sh)\b)"
)
ASSIGN = re.compile(
    r"(?:^|[;&|(]\s*)[ \t]*(?:export[ \t]+)?([A-Za-z_][A-Za-z0-9_]*)="
    r"(?:\"([^\"]*)\"|'([^']*)'|([^\s;#|&]*))"
)
VAR_LEAD = re.compile(r"^(?:\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*))")
REDIRECT = re.compile(
    r"(?:^|[;&|(]\s*|[ \t])(?:\d?&?>|&>|\d?>>)\s*"
    r"(?:\"([^\"]*)\"|'([^']*)'|([^\s;&|)]+))"
)
OUT_FLAG = re.compile(
    r"(?:--out(?:put)?|--result|--receipt|--write|-o)(?:[ \t]+|=)"
    r"(?:\"([^\"]*)\"|'([^']*)'|([^\s;&|)]+))"
)
PY_OPEN = re.compile(
    r"(?<![\w.])open\([ \t]*(?:\"([^\"]*)\"|'([^']*)')[ \t]*(?:,[^)]*)?\)"
)
PY_PATH_CALL = re.compile(
    r"(?<![\w.])Path\([ \t]*(?:\"([^\"]*)\"|'([^']*)')[ \t]*\)"
    r"[ \t]*\.[ \t]*(read_text|read_bytes|write_text|write_bytes|open)\b"
)
CAT = re.compile(r"(?:^|[;&|(]\s*|\|\s*|`\s*)cat[ \t]+(?:\"([^\"]*)\"|'([^']*)'|([^\s;&|)`]+))")
HARNESS = re.compile(
    r"(?<![\w./-])([\w./-]*(?:probe|run|measure|deliver|drive|gen|tabulate|mkprobes\d*|mkfinal)\.py)\b"
    r"([^\n|;&<>()]*)"
)
DATA_EXT = (".json", ".jsonl", ".txt", ".jsonl.gz")
MAX_VAR_DEPTH = 8


def _clean(token):
    """Strip shell quoting and punctuation left by a capture group."""
    if token is None:
        return None
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        token = token[1:-1]
    token = token.rstrip(";,")
    if not token or set(token) <= set("\"'`"):
        return None
    return token


def collect_vars(lines):
    """name -> literal value, first assignment wins (receipts pin once)."""
    out = {}
    for line in lines:
        for m in ASSIGN.finditer(line):
            name = m.group(1)
            value = next((g for g in m.groups()[1:] if g is not None), "")
            out.setdefault(name, value)
    return out


def resolve_prefix(path, vars_, depth=0):
    """Substitute leading $VAR/${VAR} prefixes; return (resolved, unresolved_name)."""
    if depth > MAX_VAR_DEPTH:
        return path, None
    m = VAR_LEAD.match(path)
    if not m:
        return path, None
    name = m.group(1) or m.group(2)
    if name not in vars_:
        return path, name
    rest = path[m.end():]
    value = vars_[name]
    merged = value + rest
    if VAR_LEAD.match(merged) and merged != path:
        return resolve_prefix(merged, vars_, depth + 1)
    return merged, None


def judge_path(raw, vars_):
    """(absolute?, detail) for one extracted path token."""
    if raw is None:
        return True, "empty"
    token = raw.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        token = token[1:-1]
    if not token or token in ("-", "/dev/null", "/dev/stdout", "/dev/stderr"):
        return True, "stream"
    if token.startswith("&"):  # fd duplication such as 2>&1
        return True, "fd-dup"
    if token.startswith("~"):
        return False, "tilde path is not absolute"
    if token.startswith("/"):
        stripped = token[1:]
        body, unresolved = resolve_prefix(stripped, vars_)
        if unresolved:
            return False, "unknown variable $%s inside absolute prefix" % unresolved
        return True, "absolute"
    resolved, unresolved = resolve_prefix(token, vars_)
    if unresolved:
        return False, ("relative path %r: variable $%s is not pinned to an absolute value"
                       % (token, unresolved))
    if resolved.startswith("/"):
        return True, "absolute via variable"
    return False, "relative path %r (resolved against the receipt's current directory)" % token


def path_like(token):
    return "/" in token or token.endswith(DATA_EXT)


def extract_paths(line):
    """[(kind, token)] result/data positions on one line. kind in write|read|data."""
    found = []
    for m in REDIRECT.finditer(line):
        tok = _clean(m.group(1) or m.group(2) or m.group(3))
        if tok:
            found.append(("write", tok))
    for m in OUT_FLAG.finditer(line):
        tok = _clean(m.group(1) or m.group(2) or m.group(3))
        if tok and path_like(tok):
            found.append(("write", tok))
    for m in PY_OPEN.finditer(line):
        tok = _clean(m.group(1) or m.group(2))
        if tok:
            found.append(("open", tok))
    for m in PY_PATH_CALL.finditer(line):
        tok = _clean(m.group(1) or m.group(2))
        if tok:
            kind = "write" if m.group(3).startswith("write") else "read"
            found.append((kind, tok))
    for m in CAT.finditer(line):
        tok = _clean(m.group(1) or m.group(2) or m.group(3))
        if tok and path_like(tok):
            found.append(("read", tok))
    for m in HARNESS.finditer(line):
        rest = m.group(2)
        tokens = rest.split()
        skip_next = False
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            if skip_next:
                skip_next = False
                continue
            if tok.startswith("-"):
                if "=" not in tok and tok in ("--tool", "--before-tool", "-o", "--out",
                                              "--output", "--result", "--receipt", "--write"):
                    skip_next = True
                continue
            tok = _clean(tok)
            if tok:
                found.append(("data", tok))
    return found


def staging_notes(lines, vars_):
    notes = []
    for no, line in enumerate(lines, 1):
        stripped = line.strip()
        m = re.match(r"(?:cd|mkdir(?:[ \t]+-p)?|cp(?:[ \t]+-\w+)*|rm(?:[ \t]+-\w+)*|git[ \t]+clone)"
                     r"[ \t]+(?:\"[^\"]*\"|'[^']*'|[^\s;&|]+)", stripped)
        if not m:
            continue
        target = m.group(0).split()[-1].strip("\"'")
        absolute, detail = judge_path(target, vars_)
        if not absolute and not stripped.startswith("cd"):
            notes.append((no, "staging write %r is %s" % (target, detail)))
        elif not absolute:
            notes.append((no, "relative cd target %r; later relative paths resolve elsewhere" % target))
    return notes


def check_receipt(path):
    """(violations, notes) for one receipt; each violation is (line, rule, reason)."""
    text = open(path, "r", encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    vars_ = collect_vars(lines)
    violations = []

    # R1 -- measured tool named by a full digest.
    bound = []
    truncated = []
    for no, line in enumerate(lines, 1):
        for m in TRUNCATED.finditer(line):
            truncated.append((no, m.group(0)))
        for m in LABELLED.finditer(line):
            if TOOL_HINT.search(line):
                bound.append((no, "sha256:" + m.group(1).lower(), "labelled"))
        for m in HEX64.finditer(line):
            token = m.group(0)
            if "sha256:" + token.lower() in {b[1] for b in bound}:
                continue
            if TOOL_HINT.search(line):
                bound.append((no, "sha256:" + token.lower(), "bare"))
        if "sha256sum" in line and not HEX64.search(line):
            pass  # computed at run time; the receipt itself pins nothing
    if not bound:
        detail = "no `sha256:`<64hex> or full 64-hex sha256 naming the measured tool"
        if truncated:
            detail += ("; only truncated digest(s): "
                       + ", ".join("line %d `%s`" % (n, t) for n, t in truncated[:3]))
        sha_calls = [n for n, line in enumerate(lines, 1) if "sha256sum" in line]
        if sha_calls:
            detail += ("; `sha256sum` at line(s) %s computes a digest at run time but the "
                       "receipt never states it" % ", ".join(map(str, sha_calls[:3])))
        violations.append((0, "R1", detail))

    # R2 -- absolute result/data paths.
    seen = set()
    for no, line in enumerate(lines, 1):
        for kind, token in extract_paths(line):
            key = (no, token)
            if key in seen:
                continue
            seen.add(key)
            absolute, detail = judge_path(token, vars_)
            if not absolute:
                violations.append((no, "R2", "%s position: %s" % (kind, detail)))

    return violations, staging_notes(lines, vars_)


def emit(receipt, violations, notes, as_json, show_notes):
    for no, rule, reason in violations:
        print("FAIL %s:%s: %s %s" % (receipt, no or "-", rule, reason))
    if show_notes:
        for no, note in notes:
            print("NOTE %s:%d: %s" % (receipt, no, note))
    if not violations:
        print("PASS %s" % receipt)


def run(paths, as_json, show_notes):
    total = 0
    results = []
    for receipt in paths:
        violations, notes = check_receipt(receipt)
        total += len(violations)
        emit(receipt, violations, notes, as_json, show_notes)
        results.append({"receipt": receipt, "violations": [
            {"line": no, "rule": rule, "reason": reason} for no, rule, reason in violations
        ]})
    verdict = "pass" if total == 0 else "fail"
    if as_json:
        print(json.dumps({"verdict": verdict, "reasons": total, "receipts": results}, indent=1))
    else:
        print("verdict=%s reasons=%d" % (verdict, total))
    return 0 if total == 0 else 1


GREEN_SAMPLE = """\
#!/usr/bin/env bash
# measured tool: /srv/green/tools/mado-tripwire.py sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
set -euo pipefail
R=/srv/green/results
rm -f "$R/repair.json"
python3 -I /srv/green/repair/measure.py --tool /srv/green/tools/mado-tripwire.py > "$R/repair.json"
python3 -c 'import json;print(json.load(open("/srv/green/results/repair.json"))["passed"])'
"""


def selftest():
    """Case matrix: the gate must reject each mutant and accept the green sample."""
    cases = {
        "green": (GREEN_SAMPLE, True),
        "relative-result": (GREEN_SAMPLE.replace('"$R/repair.json"', '"results/repair.json"'), False),
        "no-digest": (GREEN_SAMPLE.replace(
            "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", "unpinned"), False),
        "truncated-digest": (GREEN_SAMPLE.replace(
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef", "01234567\u2026", 1), False),
        "unbound-digest": (GREEN_SAMPLE.replace(
            "# measured tool: /srv/green/tools/mado-tripwire.py ", "# tool digest "), False),
        "tilde-result": (GREEN_SAMPLE.replace('"$R/repair.json"', '"~/repair.json"'), False),
        "bare-digest": (GREEN_SAMPLE.replace(
            "sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"), True),
        "relative-var": (GREEN_SAMPLE.replace("R=/srv/green/results", "R=results"), False),
    }
    work = tempfile.mkdtemp(prefix="m23-5-selftest-", dir="/tmp")
    failures = 0
    try:
        for name in sorted(cases):
            body, want_pass = cases[name]
            path = os.path.join(work, name + ".sh")
            with open(path, "w", encoding="utf-8") as stream:
                stream.write(body)
            violations, _ = check_receipt(path)
            got_pass = not violations
            ok = got_pass == want_pass
            failures += 0 if ok else 1
            print("selftest case=%s expected=%s got=%s %s"
                  % (name, "pass" if want_pass else "fail",
                     "pass" if got_pass else "fail", "ok" if ok else "MISMATCH"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("selftest=%s cases=%d mismatches=%d" % ("pass" if failures == 0 else "fail",
                                                  len(cases), failures))
    return 0 if failures == 0 else 1


def main(argv):
    parser = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    parser.add_argument("receipts", nargs="*", help="receipt file(s) to check")
    parser.add_argument("--json", action="store_true", help="machine-readable verdict")
    parser.add_argument("--notes", action="store_true", help="also print staging notes")
    parser.add_argument("--selftest", action="store_true", help="run the mutant case matrix")
    args = parser.parse_args(argv)
    if args.selftest:
        if args.receipts:
            parser.error("--selftest takes no receipt arguments")
        return selftest()
    if not args.receipts:
        parser.error("name at least one receipt (or pass --selftest)")
    for receipt in args.receipts:
        if not os.path.isfile(receipt):
            print("FAIL %s:- R0 receipt not found" % receipt)
            return 1
    return run(args.receipts, args.json, args.notes)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

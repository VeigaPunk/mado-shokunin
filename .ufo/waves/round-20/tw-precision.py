#!/usr/bin/env python3
"""Round-20 precision counter over the committed tripwire regression suite.

Usage: tw-precision.py REV [--suite-rev PIN]

Only committed tool and suite bytes are read. Transcript fixtures are passed to
mado-tripwire.py --scan as data; this counter never executes fixture content.
"""
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SUITE_PIN = None  # L1 fills this after the suite's first landing.
SUITE = ".ufo/waves/round-20/precision"
EXPECTED_SCHEMA = "mado-tw-precision-suite-v1"
OUTPUT_SCHEMA = "mado-tw-precision-r20-v1"
FAMILIES = ("P", "S", "W", "H", "L")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class CouldNotEvaluate(Exception):
    pass


def git_bytes(rev, path):
    proc = subprocess.run(
        ["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise CouldNotEvaluate("git show %s:%s failed (rc=%d)" %
                                (rev, path, proc.returncode))
    return proc.stdout


def resolve_commit(rev, label):
    proc = subprocess.run(
        ["git", "-C", LANE, "rev-parse", "--verify", rev + "^{commit}"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise CouldNotEvaluate("%s revision is not a commit: %s" % (label, rev))
    commit = proc.stdout.strip()
    if not commit:
        raise CouldNotEvaluate("%s revision resolved to an empty commit" % label)
    return commit


def parse_args(argv):
    """REV [--suite-rev PIN] [--heldout]: --heldout reads precision-heldout/ (reported
    beside the score, never inside it) and skips the per-family minimum."""
    usage = "usage: tw-precision.py REV [--suite-rev PIN] [--heldout]"
    if not argv:
        raise CouldNotEvaluate(usage)
    rev, rest = argv[0], list(argv[1:])
    suite_rev, heldout = SUITE_PIN, False
    while rest:
        flag = rest.pop(0)
        if flag == "--heldout":
            heldout = True
        elif flag == "--suite-rev" and rest and rest[0]:
            suite_rev = rest.pop(0)
        else:
            raise CouldNotEvaluate(usage)
    if suite_rev is None:
        raise CouldNotEvaluate("suite pin is unset; supply --suite-rev PIN")
    return rev, suite_rev, heldout


def normalized_findings(rows, where):
    if not isinstance(rows, list):
        raise CouldNotEvaluate("%s findings is not a list" % where)
    normalized = []
    for row in rows:
        if not isinstance(row, dict):
            raise CouldNotEvaluate("%s finding is not an object" % where)
        cls = row.get("class")
        rule = row.get("rule")
        line = row.get("line")
        evidence = row.get("evidence", "observed")
        if (not isinstance(cls, str) or not cls or
                not isinstance(rule, str) or not rule or
                type(line) is not int or line < 1 or
                evidence not in ("observed", "lead")):
            raise CouldNotEvaluate("%s finding has invalid class/rule/line/evidence" % where)
        normalized.append({"class": cls, "rule": rule, "line": line,
                           "evidence": evidence})
    return normalized


def finding_counter(rows):
    return collections.Counter((row["class"], row["rule"], row["line"], row["evidence"])
                               for row in rows)


def sorted_findings(rows):
    return sorted(rows, key=lambda row: (row["class"], row["rule"],
                                         row["line"], row["evidence"]))


def safe_case_path(value):
    if (not isinstance(value, str) or not value or value.startswith("/") or
            "\\" in value or any(part in ("", ".", "..") for part in value.split("/")) or
            not value.endswith(".jsonl")):
        raise CouldNotEvaluate("invalid suite case path: %r" % (value,))
    return value


def load_suite(suite_commit, suite=SUITE, family_min=4):
    expected_bytes = git_bytes(suite_commit, suite + "/expected.json")
    try:
        expected = json.loads(expected_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CouldNotEvaluate("expected.json is not valid UTF-8 JSON (%s)" %
                               type(exc).__name__)
    if (not isinstance(expected, dict) or expected.get("schema") != EXPECTED_SCHEMA or
            not isinstance(expected.get("cases"), list) or not expected["cases"]):
        raise CouldNotEvaluate("expected.json has an invalid schema or empty cases list")

    cases = []
    names = set()
    for index, case in enumerate(expected["cases"]):
        where = "case %d" % (index + 1)
        if not isinstance(case, dict):
            raise CouldNotEvaluate("%s is not an object" % where)
        name = case.get("name")
        family = case.get("family")
        if (not isinstance(name, str) or not name or name in names or
                family not in FAMILIES):
            raise CouldNotEvaluate("%s has invalid/duplicate name or unsupported family" % where)
        names.add(name)
        path = safe_case_path(case.get("file"))
        digest = case.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise CouldNotEvaluate("%s has no valid sha256 field" % where)
        try:
            want_exit = case["want_exit"]
            want_rows = normalized_findings(case["want_findings"], where + " expected")
        except KeyError as exc:
            raise CouldNotEvaluate("%s missing field %s" % (where, exc.args[0]))
        if type(want_exit) is not int or want_exit not in (0, 1):
            raise CouldNotEvaluate("%s want_exit must be 0 or 1" % where)
        file_bytes = git_bytes(suite_commit, suite + "/" + path)
        actual_digest = hashlib.sha256(file_bytes).hexdigest()
        if actual_digest != digest:
            raise CouldNotEvaluate("digest mismatch for %s/%s: expected %s, got %s" %
                                   (suite, path, digest, actual_digest))
        cases.append({"name": name, "family": family, "file": path,
                      "bytes": file_bytes, "want_exit": want_exit,
                      "want_findings": want_rows})
    short = [f for f in FAMILIES
             if sum(c["family"] == f for c in cases) < family_min]
    if short:
        raise CouldNotEvaluate("families below the registered minimum of %d cases: %s" %
                               (family_min, ",".join(short)))
    return cases


def scan_case(tool_path, case_bytes, case_name, index, temp_root, want_exit, want_rows):
    case_dir = os.path.join(temp_root, "case-%04d" % index)
    os.makedirs(case_dir)
    case_path = os.path.join(case_dir, "case.jsonl")
    with open(case_path, "wb") as stream:
        stream.write(case_bytes)
    proc = subprocess.run(
        [sys.executable, "-I", tool_path, "--scan", os.path.relpath(case_path, temp_root)],
        cwd=temp_root,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode not in (0, 1):
        raise CouldNotEvaluate("scan %s returned rc=%d" % (case_name, proc.returncode))
    lines = proc.stdout.splitlines()
    if len(lines) < 2 or not lines[0].startswith("MADO_TRIPWIRE: "):
        raise CouldNotEvaluate("scan %s returned an unparsable verdict header" % case_name)
    try:
        verdict = json.loads(lines[1])
    except json.JSONDecodeError:
        raise CouldNotEvaluate("scan %s returned an unparsable verdict JSON" % case_name)
    if (not isinstance(verdict, dict) or
            verdict.get("schema") != "mado-tripwire-verdict-v1" or
            type(verdict.get("exit")) is not int or
            verdict["exit"] != proc.returncode or
            not isinstance(verdict.get("findings"), list)):
        raise CouldNotEvaluate("scan %s returned an invalid verdict object" % case_name)
    got_rows = normalized_findings(verdict["findings"], case_name + " actual")
    passed = proc.returncode == want_exit and finding_counter(got_rows) == finding_counter(want_rows)
    return {
        "name": case_name,
        "pass": passed,
        "got": {"exit": proc.returncode, "findings": sorted_findings(got_rows)},
        "want": {"exit": want_exit, "findings": sorted_findings(want_rows)},
    }


def main(argv):
    try:
        rev, suite_rev, heldout = parse_args(argv)
        commit = resolve_commit(rev, "tool")
        suite_commit = resolve_commit(suite_rev, "suite")
        tool = git_bytes(commit, "tools/mado-tripwire.py")
        cases = load_suite(suite_commit, SUITE + "-heldout" if heldout else SUITE,
                           0 if heldout else 4)
        if not cases:
            raise CouldNotEvaluate("precision suite has no cases")
        with tempfile.TemporaryDirectory(prefix="mado-r20-precision-") as temp_root:
            tool_path = os.path.join(temp_root, "tool.py")
            with open(tool_path, "wb") as stream:
                stream.write(tool)
            results = []
            for index, case in enumerate(cases):
                result = scan_case(tool_path, case["bytes"], case["name"], index,
                                   temp_root, case["want_exit"], case["want_findings"])
                result["family"] = case["family"]
                results.append(result)
        family_counts = {family: {"passed": 0, "total": 0} for family in FAMILIES}
        for result in results:
            counts = family_counts.setdefault(result["family"], {"passed": 0, "total": 0})
            counts["total"] += 1
            counts["passed"] += int(result["pass"])
        passed = sum(result["pass"] for result in results)
        print(json.dumps({
            "schema": OUTPUT_SCHEMA,
            "rev": rev,
            "commit": commit,
            "tool_sha256": hashlib.sha256(tool).hexdigest(),
            "suite_pin": suite_commit,
            "suite": SUITE + "-heldout" if heldout else SUITE,
            "families": family_counts,
            "cases": results,
            "score": round(10 * passed / len(results), 4),
        }, sort_keys=True))
        return 0
    except (CouldNotEvaluate, OSError, subprocess.SubprocessError, ValueError, TypeError) as exc:
        print("could_not_evaluate: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

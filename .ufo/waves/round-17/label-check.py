#!/usr/bin/env python3
"""label-check.py — round-17 receipt-label consistency checker (C1 M1 fix).

Reads label-claims.json (default: sibling of this script; argv[1] overrides).
Each claim is a dict:
    doc          repo-relative path of the citing document
    rev          git revision of the document
    line         1-based line the claim says carries the label
    line_end     optional inclusive last line when the statement wraps
    receipt      repo-relative path of the cited receipt JSON
    rev_receipt  git revision of the receipt
    token        literal token the document attributes to the receipt
    id           optional display id (default: claim-<n>)

Checks, per claim:
  1. doc stage: the doc lines at `rev` (or the inline `doc_text` of a
     mutant claim) contain BOTH the receipt basename and `token`.
  2. receipt stage: `token` is one of the receipt's OUTCOME tokens — the
     verdict word on a `MADO_<NAME>: <token>` line, a `"finding"` value
     (top-level or in embedded verdict JSON), or the got-side of a selftest
     line (`got N/<token>`). Want-side text and free prose never count
     (L1 fix after CriticC1: a substring match passed a want-only mutant).
  3. optional `measured_commit`: when the claim names it, the receipt's
     `measured_commit` must start with it.
  4. optional `expect`: `ok` or `MISMATCH`; the summary reports how many
     claims met their expectation (EXPECT_SUMMARY) so red controls count.

Output: `LABEL <id> ok` or `LABEL <id> MISMATCH (<stage>)` per claim, then
`LABEL_SUMMARY: k/n`. Exit 0 all ok, 1 any mismatch, 2 could-not-evaluate
(malformed claims file, git failure, unreadable doc/receipt, bad JSON).
Exit 2 wins over 1.
"""
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTCOME_LINE = re.compile(r"^MADO_[A-Z_]+: ([a-z_]+)", re.M)
FINDING_JSON = re.compile(r'"finding":\s*"([a-z_]+)"')
GOT_SIDE = re.compile(r"\bgot -?\d+/([a-z_]+)")


def git_show(root, rev, path):
    """Return file text at rev:path, or None on any failure."""
    try:
        out = subprocess.run(
            ["git", "-C", root, "show", "%s:%s" % (rev, path)],
            capture_output=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    try:
        return out.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def repo_root():
    try:
        out = subprocess.run(
            ["git", "-C", SCRIPT_DIR, "rev-parse", "--show-toplevel"],
            capture_output=True, timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", "replace").strip() or None


def outcome_tokens(node, acc):
    """Collect verdict tokens only (never want-side text), recursively."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("expected", "want", "expect", "expected_finding", "want_finding"):
                continue  # want-side containers never count as outcomes
            if k == "finding" and isinstance(v, str):
                acc.add(v)
            elif k in ("stdout", "stderr") and isinstance(v, str):
                acc.update(OUTCOME_LINE.findall(v))
                acc.update(FINDING_JSON.findall(v))
                acc.update(GOT_SIDE.findall(v))
            else:
                outcome_tokens(v, acc)
    elif isinstance(node, list):
        for v in node:
            outcome_tokens(v, acc)


def check_claim(root, claim):
    """Return (status, stage) where status is 'ok', 'MISMATCH', or 'UNEVAL'."""
    for key in ("doc", "rev", "line", "receipt", "rev_receipt", "token"):
        if key not in claim:
            return "UNEVAL", "missing key %r" % key
    doc, rev, line = claim["doc"], claim["rev"], claim["line"]
    receipt, rrev, token = claim["receipt"], claim["rev_receipt"], claim["token"]
    line_end = claim.get("line_end", line)
    if not isinstance(line, int) or not isinstance(line_end, int) or line < 1 or line_end < line:
        return "UNEVAL", "bad line range"

    if "doc_text" in claim:
        if claim.get("doc") != "mutant":
            return "UNEVAL", "doc_text is allowed only for doc == 'mutant'"
        text = claim["doc_text"]
    else:
        text = git_show(root, rev, doc)
    if text is None:
        return "UNEVAL", "git show %s:%s failed" % (rev, doc)
    lines = text.splitlines()
    if line_end > len(lines):
        return "UNEVAL", "line %d past end of doc" % line_end
    window = "\n".join(lines[line - 1:line_end])
    base = os.path.basename(receipt)
    if base not in window or token not in window:
        missing = []
        if base not in window:
            missing.append("basename %s" % base)
        if token not in window:
            missing.append("token %r" % token)
        return "MISMATCH", "doc line %d-%d lacks %s" % (line, line_end, ", ".join(missing))

    rtext = git_show(root, rrev, receipt)
    if rtext is None:
        return "UNEVAL", "git show %s:%s failed" % (rrev, receipt)
    try:
        rdata = json.loads(rtext)
    except ValueError:
        return "UNEVAL", "receipt is not valid JSON"
    mc = claim.get("measured_commit")
    if mc is not None:
        got_mc = rdata.get("measured_commit", "") if isinstance(rdata, dict) else ""
        if not str(got_mc).startswith(mc):
            return "MISMATCH", "receipt measured_commit %r is not %r" % (got_mc, mc)
    acc = set()
    outcome_tokens(rdata, acc)
    if token in acc:
        return "ok", "receipt outcome carries %r" % token
    return "MISMATCH", "receipt outcome %s lacks %r" % (sorted(acc), token)


def main(argv):
    claims_path = argv[1] if len(argv) > 1 else os.path.join(SCRIPT_DIR, "label-claims.json")
    try:
        with open(claims_path, "r", encoding="utf-8") as fh:
            claims = json.load(fh)
    except (OSError, ValueError) as exc:
        print("LABEL_SUMMARY: 0/0 (could not read claims: %s)" % exc)
        return 2
    if not isinstance(claims, list) or not claims:
        print("LABEL_SUMMARY: 0/0 (claims file is not a non-empty list)")
        return 2

    root = repo_root()
    if root is None:
        print("LABEL_SUMMARY: 0/%d (git toplevel unresolved)" % len(claims))
        return 2

    ok = 0
    mismatch = 0
    uneval = 0
    met = 0
    expected = 0
    for i, claim in enumerate(claims, 1):
        cid = "claim-%d" % i
        if isinstance(claim, dict):
            cid = str(claim.get("id") or claim.get("name") or cid)
            status, stage = check_claim(root, claim)
        else:
            status, stage = "UNEVAL", "claim is not an object"
        if status == "ok":
            ok += 1
            print("LABEL %s ok (%s)" % (cid, stage))
        elif status == "MISMATCH":
            mismatch += 1
            print("LABEL %s MISMATCH (%s)" % (cid, stage))
        else:
            uneval += 1
            print("LABEL %s COULD_NOT_EVALUATE (%s)" % (cid, stage))
        exp = claim.get("expect") if isinstance(claim, dict) else None
        if exp in ("ok", "MISMATCH"):
            expected += 1
            met += int(exp == status)
    print("LABEL_SUMMARY: %d/%d" % (ok, len(claims)))
    print("EXPECT_SUMMARY: %d/%d claims met their declared expectation" % (met, expected))
    if uneval:
        return 2
    # Wave-2 fix (AttackLabelCheckCode F3): when every claim declares `expect`,
    # the exit code is the expectation verdict (0 iff all met); red controls
    # are visible in the LABEL lines. Otherwise any MISMATCH exits 1.
    if expected == len(claims):
        return 0 if met == expected else 1
    return 1 if mismatch else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

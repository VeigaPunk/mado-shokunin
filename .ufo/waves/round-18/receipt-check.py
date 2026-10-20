#!/usr/bin/env python3
"""Round-18 criterion-24 receipt/provenance checker (R17-V1/V2 tripwire).

Verifies that a measurement receipt actually binds to the tool and the
commit it claims. A claim in receipt-claims.json is:

  {"id": str,
   "receipt": "<lane-relative path>",
   "rev": "<lane commit to read the receipt at via git show, or WORKTREE>",
   "tool": "<lane-relative path of the measured tool>",
   "expect": "ok" | "MISSING_PROVENANCE" | "SHA_MISMATCH"}

The checker:

1. Reads the receipt bytes: `git show <rev>:<receipt>` inside the lane,
   or the plain file when rev == "WORKTREE".
2. Requires `tool_sha256=` and `measured_commit=` on a RECEIPT header
   line (regex over every line, `=` or `:` separator), or the JSON keys
   `tool_sha256` / `measured_commit` anywhere in the receipt text
   (whole-document JSON or embedded "key": "hex" pairs). Absent either
   -> MISSING_PROVENANCE.
3. Resolves `tool_sha256` against sha256 of `git show
   <measured_commit>:<tool>`; mismatch -> SHA_MISMATCH, else ok.

rev == "PENDING-L1" is a placeholder for the round-18 re-cut receipts:
it evaluates to PENDING (could-not-evaluate).

Output: `RECEIPT <id> <status>` per claim, then `EXPECT_SUMMARY: k/n`.
Exit: 0 when every claim meets its expect; 1 when all were evaluated
but some failed; 2 when at least one claim could not be evaluated.
"""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
LANE = HERE.parents[3]  # .ufo/waves/round-18/receipt-check.py -> lane root
CLAIMS = HERE.with_name("receipt-claims.json") if len(sys.argv) < 2 else Path(sys.argv[1])

HEX64 = r"[0-9a-f]{64}"
HEX40 = r"[0-9a-f]{40}"
# RECEIPT header line: `tool_sha256=` / `measured_commit=` (or `:`).
HDR_SHA = re.compile(rf"^\s*tool_sha256\s*[=:]\s*({HEX64})\s*$", re.M)
HDR_REV = re.compile(rf"^\s*measured_commit\s*[=:]\s*({HEX40})\s*$", re.M)
# JSON keys, whole-document or embedded: "tool_sha256": "<hex>".
JSN_SHA = re.compile(rf'"tool_sha256"\s*:\s*"({HEX64})"')
JSN_REV = re.compile(rf'"measured_commit"\s*:\s*"({HEX40})"')


def git_show(rev: str, path: str):
    """Return bytes of <rev>:<path>, or None when unreadable."""
    r = subprocess.run(
        ["git", "show", f"{rev}:{path}"],
        cwd=LANE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    return r.stdout if r.returncode == 0 else None


def receipt_bytes(rev: str, path: str):
    if rev == "WORKTREE":
        p = LANE / path
        try:
            return p.read_bytes() if p.is_file() else None
        except OSError:
            return None
    return git_show(rev, path)


def provenance(text: str):
    """Return (tool_sha256, measured_commit) or (None, None)/partial."""
    m = HDR_SHA.search(text)
    r = HDR_REV.search(text)
    if m and r:
        return m.group(1), r.group(1)
    m2 = JSN_SHA.search(text)
    r2 = JSN_REV.search(text)
    tool = (m or m2).group(1) if (m or m2) else None
    rev = (r or r2).group(1) if (r or r2) else None
    return tool, rev


def evaluate(claim: dict) -> str:
    rev = claim["rev"]
    if rev == "PENDING-L1":
        return "PENDING"  # placeholder; L1 fills rev for the re-cut
    body = receipt_bytes(rev, claim["receipt"])
    if body is None:
        return "ERROR"  # could-not-evaluate: receipt unreadable
    try:
        text = body.decode("utf-8", errors="replace")
    except Exception:
        return "ERROR"
    tool_sha, measured = provenance(text)
    if not tool_sha or not measured:
        return "MISSING_PROVENANCE"
    blob = git_show(measured, claim["tool"])
    if blob is None:
        return "ERROR"  # could-not-evaluate: tool unreadable at rev
    actual = hashlib.sha256(blob).hexdigest()
    return "ok" if actual == tool_sha else "SHA_MISMATCH"


def main() -> int:
    try:
        claims = json.loads(CLAIMS.read_text())["claims"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"RECEIPT_CLAIMS_ERROR: {CLAIMS}: {exc}")
        return 2
    if not isinstance(claims, list):
        print(f"RECEIPT_CLAIMS_ERROR: {CLAIMS}: 'claims' is not a list")
        return 2
    allowed = {"ok", "MISSING_PROVENANCE", "SHA_MISMATCH"}
    met = 0
    n = 0
    unevaluated = False
    for c in claims:
        n += 1
        try:
            cid, expect = str(c["id"]), c["expect"]
            assert expect in allowed
            assert isinstance(c["receipt"], str)
            assert isinstance(c["rev"], str)
            assert isinstance(c["tool"], str)
        except (KeyError, TypeError, AssertionError):
            print(f"RECEIPT claim#{n} ERROR (bad claim or expect)")
            unevaluated = True
            continue
        try:
            status = evaluate(c)
        except (KeyError, TypeError, ValueError, OSError):
            status = "ERROR"
        print(f"RECEIPT {cid} {status}")
        if status in ("PENDING", "ERROR"):
            unevaluated = True
        elif status == expect:
            met += 1
    print(f"EXPECT_SUMMARY: {met}/{n}")
    if unevaluated:
        return 2
    return 0 if met == n else 1


if __name__ == "__main__":
    sys.exit(main())

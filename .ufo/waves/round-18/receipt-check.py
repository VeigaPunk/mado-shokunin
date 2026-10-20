#!/usr/bin/env python3
"""Round-18 criterion-24 receipt/provenance checker (R17-V1/V2 tripwire).

Verifies that a measurement receipt binds its producer tool to the revision
it claims, at the revision the claim is read at.

A claim in receipt-claims.json is:

  {"id": str,
   "receipt": "<lane-relative path>",
   "rev": "<lane commit to read the receipt at via git show, or WORKTREE>",
   "bind_rev": "<lane commit the receipt's tool identity binds to; optional>",
   "tool": "<lane-relative path of the measured tool>",
   "expect": "ok" | "MISSING_PROVENANCE" | "SHA_MISMATCH" | "STALE" |
             "NOT_ANCESTOR" | "PRODUCER_MISMATCH"}

The checker:

1. Reads the receipt bytes: `git show <rev>:<receipt>` inside the lane, or
   the plain file when rev == "WORKTREE".
2. Takes `tool` / `tool_sha256` / `measured_commit` from the first line when
   it begins with `RECEIPT` (key=value tokens anywhere on that line, the
   shape recut-receipts.sh writes), else from the same keys anywhere in the
   text: `key: value` lines and JSON `"key": "hex"` pairs. Absent
   `tool_sha256` or `measured_commit` -> MISSING_PROVENANCE. A `tool` token
   naming a different producer than the claim's tool -> PRODUCER_MISMATCH.
3. Requires measured_commit to be an ancestor of (or equal to) the revision
   the claim reads the receipt at; a WORKTREE read binds to `bind_rev`
   instead (required there). Violation -> NOT_ANCESTOR.
4. Resolves `tool_sha256` against sha256 of `git show
   <measured_commit>:<tool>`; mismatch -> SHA_MISMATCH.
5. Requires the same tool bytes at the binding revision (`bind_rev`, default
   `rev`). When they differ, the receipt attests a superseded tool at the
   claimed revision -> STALE. A before-state claim -- one that really did run
   an older tool -- sets `bind_rev` to its own `measured_commit`, which
   declares the older tool instead of leaving the drift silent; any other
   binding is a malformed claim (ERROR).

rev == "PENDING-L1" is the could-not-evaluate placeholder for a receipt not
committed yet (exit 2, never credit).

Output: `RECEIPT <id> <status>` per claim, then `EXPECT_SUMMARY: k/n`.
Exit: 0 when every claim meets its expect; 1 when all were evaluated but
some failed; 2 when at least one claim could not be evaluated.
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
# One provenance token, in any of the supported spellings:
#   RECEIPT tool=... tool_sha256=<hex> measured_commit=<hex>
#   tool_sha256: <hex>            measured_commit=<hex>
#   "tool_sha256": "<hex>"        "measured_commit": "<hex>"
TOKEN = r"\b{}\b[\"']?\s*[=:]\s*[\"']?({})"
PRODUCER = re.compile(TOKEN.format("tool", r"[^\s\"']+"))
SHA = re.compile(TOKEN.format("tool_sha256", HEX64))
REV = re.compile(TOKEN.format("measured_commit", HEX40))


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
    """Return (tool, tool_sha256, measured_commit); absent fields are None.

    The producer token is read only from a line-1 `RECEIPT` header: verdict
    bodies also carry per-finding `"tool": "bash"` keys, and a whole-text
    search would mistake one for the producer.
    """
    first = text.split("\n", 1)[0]
    m = PRODUCER.search(first) if first.lstrip().startswith("RECEIPT") else None
    tool = m.group(1) if m else None
    sha = SHA.search(text)
    rev = REV.search(text)
    return tool, (sha.group(1) if sha else None), (rev.group(1) if rev else None)


def ancestor(a: str, b: str):
    """True when a is an ancestor of (or equal to) b; None when undecidable."""
    r = subprocess.run(
        ["git", "merge-base", "--is-ancestor", a, b],
        cwd=LANE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if r.returncode == 0:
        return True
    if r.returncode == 1:
        return False
    return None


def evaluate(claim: dict) -> str:
    rev = claim["rev"]
    if rev == "PENDING-L1":
        return "PENDING"  # could-not-evaluate: receipt not committed yet
    body = receipt_bytes(rev, claim["receipt"])
    if body is None:
        return "ERROR"  # could-not-evaluate: receipt unreadable
    text = body.decode("utf-8", errors="replace")
    producer, tool_sha, measured = provenance(text)
    if not tool_sha or not measured:
        return "MISSING_PROVENANCE"
    if producer is not None and producer != claim["tool"]:
        return "PRODUCER_MISMATCH"
    if rev == "WORKTREE":
        bind = claim.get("bind_rev")
        if not bind:
            return "ERROR"  # a worktree read needs the revision it binds to
        anchor = bind
    else:
        bind = claim.get("bind_rev") or rev
        # Declared bindings are only the read revision (default) or the
        # measured revision (a before-state receipt); anything else is a
        # malformed claim, not a measurement.
        if bind != rev and bind != measured:
            return "ERROR"
        anchor = rev
    decided = ancestor(measured, anchor)
    if decided is None:
        return "ERROR"  # could-not-evaluate: unresolved commit
    if not decided:
        return "NOT_ANCESTOR"
    blob = git_show(measured, claim["tool"])
    if blob is None:
        return "ERROR"  # could-not-evaluate: tool unreadable at measured_commit
    if hashlib.sha256(blob).hexdigest() != tool_sha:
        return "SHA_MISMATCH"
    if bind == measured:
        return "ok"  # before-state receipt: it names the revision it ran
    blob = git_show(bind, claim["tool"])
    if blob is None:
        return "ERROR"  # could-not-evaluate: tool unreadable at bind_rev
    return "ok" if hashlib.sha256(blob).hexdigest() == tool_sha else "STALE"


def main() -> int:
    try:
        claims = json.loads(CLAIMS.read_text())["claims"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"RECEIPT_CLAIMS_ERROR: {CLAIMS}: {exc}")
        return 2
    if not isinstance(claims, list):
        print(f"RECEIPT_CLAIMS_ERROR: {CLAIMS}: 'claims' is not a list")
        return 2
    allowed = {"ok", "MISSING_PROVENANCE", "SHA_MISMATCH", "STALE",
               "NOT_ANCESTOR", "PRODUCER_MISMATCH"}
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
            assert isinstance(c.get("bind_rev", ""), str)
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

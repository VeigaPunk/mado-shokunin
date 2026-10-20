# ReceiptClaims19 — five round-19 receipt claims filed: both reds hold, three greens credit only after one 3-hunk checker change

Scope: wrote only `.ufo/waves/round-19/receipt-claims.json` and this report. By this seat, no round-18 file, receipt, sibling lane, fleet file, MANIFEST, `.ufo/state`, or jj/git state was modified (concurrent sibling worktree edits are noted under Limits). All claims read at `17661e0fa83f978fb659f5bb8fef47f0969f6945` (pre-registration; HEAD of the lane); data baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`.

## Deliverable

`.ufo/waves/round-19/receipt-claims.json` — schema `mado-receipt-claims-v1`, five claims, no `PENDING-L1` placeholders:

| id | receipt | expect |
|---|---|---|
| `r19-c26-redbefore-headerless` | `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` | `MISSING_PROVENANCE` |
| `r19-c26-regression-recut-headerless` | `.ufo/waves/round-18/evidence/regression-recut.txt` | `MISSING_PROVENANCE` |
| `r19-tw-recall-before` | `.ufo/waves/round-19/evidence/tw-recall-before.txt` | `ok` |
| `r19-fresh-pins-before` | `.ufo/waves/round-19/evidence/fresh-pins-before.txt` | `ok` |
| `r19-measure-before` | `.ufo/waves/round-19/evidence/measure-before.json.txt` | `ok` |

The checker takes the claims path as `argv[1]` (`receipt-check.py:56`, `CLAIMS = HERE.with_name("receipt-claims.json") if len(sys.argv) < 2 else Path(sys.argv[1])`), so it can be pointed at the round-19 file without touching round-18. `LANE` is derived from the script's own location (`HERE.parents[3]`), so it stays the lane root.

## Red arm — both hold (criterion 26's red-before pair)

- `gate-rc-redbefore.txt`, read via `git show 17661e0:...`: sha256 `d69f9b55a4a61789dcf1835d345a6f4814f8d587a76eb00df65aa05be16148ca`, byte-identical at `9c54c56`, at `17661e0` and in the worktree. `grep -cE 'tool_sha256|measured_commit|^RECEIPT'` → `0`. Checker line: `RECEIPT r19-c26-redbefore-headerless MISSING_PROVENANCE`.
- `regression-recut.txt`: sha256 `643e927173a400b04879a0fb950281bb75fc830ba6e5356861f0fabe0d339fd1`, identical at both revs and the worktree; same grep count `0`. Checker line: `RECEIPT r19-c26-regression-recut-headerless MISSING_PROVENANCE`.
- `corpus/QUALITY.md:148` cites `gate-rc-redbefore.txt` §1 as criterion 26's red-before; that citation is R18-V2 — the receipt carries no producer header, so criterion 26's own red-before cannot satisfy criterion 24's bar. `regression-recut.txt` is not cited in `QUALITY.md` (grep), but it is the second headerless GateRcFix receipt of the same red-before pair and is claimed for that reason.
- Producer digests are narrated in prose, never in a `RECEIPT` header: `gate-rc-redbefore.txt:8` names the committed old gate at `d9a5a18` as `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`; `:10` and `regression-recut.txt:17` (`REGRESSION_TOOL`) name an *uncommitted* edited gate `2bdf5e8afbb617142e4a881943084f94c9513327b1de25170ad71db113983925`; `regression-recut.txt:6,29` name the external harness `0673d2e5…`. The gate committed at `9c54c56`/`17661e0` is `c9fb0cef…`, so a header-based re-cut of the red-before must bind `d9a5a18`'s gate (or hand the edited-gate digest through a claimed tool identity), not today's gate. The claim's `tool` field is only consulted after the provenance test, so it is cosmetic for `MISSING_PROVENANCE`; it names the in-lane tool under test.

## Green arm

1. `measure-before.json.txt` → `ok` under the unmodified checker. Header: `tool=.ufo/waves/round-17/measure.py tool_sha256=de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc measured_commit=9c54c56…`; `measure.py` hashes `de4c422b…` at both `9c54c56` and `17661e0`.
2. `tw-recall-before.txt` → header `tool_sha256=220902982fb1f0561811e6483ea53fe08ba2b8f939f396a440ab63944e4cbd28`; the tool at `17661e0` (and in the worktree) hashes exactly `2209029…`. Header `measured_commit=9c54c56…`, and `git cat-file -e 9c54c56:.ufo/waves/round-19/tw-recall.py` → ABSENT: the tool was worktree-only at the baseline, exactly as its own line 1 says ("tool not yet committed; pre-registration baseline").
3. `fresh-pins-before.txt` → header `tool_sha256=a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`; tool at `17661e0` hashes `a094be0…`; same ABSENT-at-9c54c56 shape.

## The gap and the exact minimal change

Unmodified round-18 checker against the round-19 claims file:

```
RECEIPT r19-c26-redbefore-headerless MISSING_PROVENANCE
RECEIPT r19-c26-regression-recut-headerless MISSING_PROVENANCE
RECEIPT r19-tw-recall-before ERROR
RECEIPT r19-fresh-pins-before ERROR
RECEIPT r19-measure-before ok
EXPECT_SUMMARY: 3/5
```

exit 2. Cause is structural, not a claim-authoring mistake: `receipt-check.py:148` resolves `tool_sha256` only against `git show <measured_commit>:<tool>`, and the two round-19 before receipts measure data at `9c54c56` while their producer landed at `17661e0`. No claim shape the current checker understands can credit a split tool/measurement provenance, and `bind_rev` cannot help (the tool lookup still uses `measured`).

Exact minimal change to `.ufo/waves/round-18/receipt-check.py` — optional claim key `tool_rev` (default `measured_commit`) naming the revision whose tool bytes the header attests; 3 hunks, +5/−2, no existing claim changes status:

```diff
--- a/receipt-check.py
+++ b/receipt-check.py
@@ -9,7 +9,8 @@
   {"id": str,
    "receipt": "<lane-relative path>",
    "rev": "<lane commit to read the receipt at via git show, or WORKTREE>",
    "bind_rev": "<lane commit the receipt's tool identity binds to; optional>",
+   "tool_rev": "<lane commit whose <tool> bytes tool_sha256 attests; optional>",
    "tool": "<lane-relative path of the measured tool>",
    "expect": "ok" | "MISSING_PROVENANCE" | "SHA_MISMATCH" | "STALE" |
              "NOT_ANCESTOR" | "PRODUCER_MISMATCH"}
@@ -143,11 +144,12 @@
     decided = ancestor(measured, anchor)
     if decided is None:
         return "ERROR"  # could-not-evaluate: unresolved commit
     if not decided:
         return "NOT_ANCESTOR"
-    blob = git_show(measured, claim["tool"])
+    tool_rev = claim.get("tool_rev") or measured
+    blob = git_show(tool_rev, claim["tool"])
     if blob is None:
-        return "ERROR"  # could-not-evaluate: tool unreadable at measured_commit
+        return "ERROR"  # could-not-evaluate: tool unreadable at tool_rev
     if hashlib.sha256(blob).hexdigest() != tool_sha:
         return "SHA_MISMATCH"
     if bind == measured:
@@ -180,7 +182,8 @@
             assert isinstance(c["receipt"], str)
             assert isinstance(c["rev"], str)
             assert isinstance(c["tool"], str)
             assert isinstance(c.get("bind_rev", ""), str)
+            assert isinstance(c.get("tool_rev", ""), str)
         except (KeyError, TypeError, AssertionError):
             print(f"RECEIPT claim#{n} ERROR (bad claim or expect)")
             unevaluated = True
```

With this change, the identity chain is unchanged in strength: the header digest must equal the tool bytes at `tool_rev` **and** at the binding revision (`bind`, default `rev`), so a foreign `tool_rev` buys nothing.

Demonstrated (no lane writes): `git clone --shared` of the lane into `/tmp/r19demo2` (default checkout at `17661e0`; clone and patch writes only in `/tmp`), checker copied to the mirrored `.ufo/waves/round-18/`, the three hunks applied (patch fuzz 1/2/1; post-patch `diff` shows exactly the three hunks above), then both claims files run against that copy:

```
== round-19 claims
EXPECT_SUMMARY: 5/5          (exit 0)

== round-18 claims, same patched copy
EXPECT_SUMMARY: 33/33        (exit 0)
```

No round-18 claim sets `tool_rev`, so the default is `measured_commit` and every round-18 path is the old behaviour; the 33/33 is measured, not inferred.

Alternative not taken: re-cut the two before receipts with a `tool_commit=` header token. That edits committed evidence and still splits measurement (`9c54c56`) from producer commit (`17661e0`), so the checker would need an equivalent read anyway — L1's call.

## EXPECT_SUMMARY, verbatim

- Unmodified round-18 checker, round-19 claims: `EXPECT_SUMMARY: 3/5` (exit 2).
- With the minimal `tool_rev` change, same claims file: `EXPECT_SUMMARY: 5/5` (exit 0).

The round-19 claims file carries the `tool_rev` key on the two split-provenance claims; the unmodified checker ignores it (unknown keys are not validated), which is why the unmodified run cannot regress anything.

## Limits

- Did not edit `.ufo/waves/round-18/receipt-check.py`, any receipt, or any round-18 claim; did not re-cut receipts.
- Did not run the live gate or `--selftest`/`--regression`; criterion 26's OM9/OM10 behavioural arm was not re-exercised (round-18 evidence stands).
- The patched demonstration ran in `/tmp/r19demo2` (a `--shared` clone at `17661e0`), not in the lane; patch applied with fuzz (context was otherwise exact). The lane's worktree carried concurrent sibling edits during the wave (e.g. `.ufo/waves/round-18/measure-mutants.py` mtime 14:07, `corpus/knowledge/*`); none were written by this seat and none affect the clone-pinned runs.
- `tool_rev` was not exercised under `WORKTREE` reads or with a tool_rev that is not an ancestor of the binding revision; the digest must match at both revisions, which is what keeps that harmless. [INFERENCE] no other round-19 claim shape would credit the split receipts.
- The claims file's only `PENDING-L1`/placeholder occurrence is the inherited schema description (`receipt-claims.json:12`); no claim uses a placeholder revision.
- [UNK] whether L1 will adopt the checker change or re-cut the receipts; both measured outcomes are reported.

## Installs

none.

Claims file sha256 `4ba6bd37cfa9fed0add3646758948cba6a73447f57ec908b9215733c5649b33a`; the unmodified and patched checker runs quoted above were re-run against this final file (3/5 exit 2; 5/5 exit 0).

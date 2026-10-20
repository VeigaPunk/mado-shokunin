# ReceiptCheck — criterion-24 receipt/provenance checker (R17-V1/V2)

Seat: MadoR18.ReceiptCheck. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
No tool installs; only read-only git in the lane (rev-parse/log/show); no host
probes; no writes outside the five files below plus this report.

## Files changed

| path (lane-relative) | sha256 |
|---|---|
| `.ufo/waves/round-18/receipt-check.py` | `5aec6154085c22cd8de34ec32d8ffdb29e783955ab52c6282d25344f559dc7b2` |
| `.ufo/waves/round-18/receipt-claims.json` | `14aaee0f051788662948510c4faf116f86f44f34a3248405f206bc5a697b0628` |
| `.ufo/waves/round-18/receipt-fixtures/ok-receipt.txt` | `04b431ff5c87d5868f91eb7e69f088d457d4ba71abaadaabc5551a6f836e8177` |
| `.ufo/waves/round-18/receipt-fixtures/bad-sha-receipt.txt` | `2018ca40bbaceb5b3af46460d6c340c4e6367cf6f53a5567a075b6b47e817517` |
| `.ufo/waves/round-18/receipt-fixtures/stale-rev-receipt.txt` | `6ad4af1026245c4525c7e25079348e8cad1a2a5146e95622b8e2b8c5de51dd92` |

## Behavior

`python3 -I .ufo/waves/round-18/receipt-check.py [CLAIMS_JSON]`

Claim: `{id, receipt, rev, tool, expect}` with
`expect ∈ {ok, MISSING_PROVENANCE, SHA_MISMATCH}`.

1. Receipt bytes: `git show <rev>:<receipt>` in the lane; `rev: "WORKTREE"`
   reads the lane file directly (authored fixtures); `rev: "PENDING-L1"` is
   the placeholder sentinel for round-18 re-cut receipts and yields `PENDING`.
2. Provenance: per-line `tool_sha256=` / `measured_commit=` header (also
   accepts `:` as separator, anchored to 64/40 lowercase hex), else JSON keys
   `"tool_sha256": "…"` / `"measured_commit": "…"` anywhere in the text.
   Neither pair → `MISSING_PROVENANCE`.
3. `tool_sha256` is compared with sha256 of `git show <measured_commit>:<tool>`;
   equal → `ok`, else `SHA_MISMATCH`. Unreadable receipt or tool → `ERROR`
   (could-not-evaluate).
4. Output `RECEIPT <id> <status>` per claim then `EXPECT_SUMMARY: k/n`.
   Exit 0 all expects met; 1 all evaluated but some unmet; 2 any claim
   `PENDING`/`ERROR` (could-not-evaluate). Lane root is derived from the
   script path, so cwd does not matter; claims path may be overridden by argv[1].

## Retained evidence (run in the lane, 2026-10-20)

Baseline: `git rev-parse d9a5a18` = `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`;
HEAD = `d3a00003e6ef0b1e3c7b4faf52d592eb293857ba`.

Tool digests actually recorded by git:

```
$ git show d9a5a18:tools/mado-tripwire.py | sha256sum
962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072  -
$ git show f71ccbe:tools/mado-tripwire.py | sha256sum
7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7  -
```

The `f71ccbe` digest carries the `7a98720e` prefix the round-17 report cited;
the landed `d9a5a18` tool is `962919ce`. `stale-rev-receipt.txt` reproduces
that cross-binding shape (attests `962919ce`, pins `f71ccbe`).

Absence proof on the red receipts at `d9a5a18` (`grep -c 'tool_sha256\|measured_commit'`,
each 0): `tripwire-r13.txt`, `r14`, `r15`, `r16`, `tripwire-anchor-r15.txt`,
`tripwire-pacmanlog-join.txt`.

Scenario A — full claims file (seeded):

```
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE
RECEIPT r17-tripwire-r14 MISSING_PROVENANCE
RECEIPT r17-tripwire-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-r16 MISSING_PROVENANCE
RECEIPT r17-tripwire-anchor-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-pacmanlog-join MISSING_PROVENANCE
RECEIPT r18-fixture-ok ok
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-recut-tripwire-r13 PENDING
RECEIPT r18-recut-tripwire-r14 PENDING
RECEIPT r18-recut-tripwire-r15 PENDING
RECEIPT r18-recut-tripwire-r16 PENDING
RECEIPT r18-recut-tripwire-anchor-r15 PENDING
RECEIPT r18-recut-tripwire-pacmanlog-join PENDING
EXPECT_SUMMARY: 9/15
EXIT_A=2
```

Exit 2 is deliberate: the six round-18 re-cut receipts do not exist yet
(`rev: "PENDING-L1"`).

Scenario B — `/tmp/rc-live.json` = the 9 non-placeholder claims:
`EXPECT_SUMMARY: 9/9`, `EXIT_B=0`. Same result with `python3 -I` invoked from
`/` (cwd-independent), output ending `EXPECT_SUMMARY: 9/9`.

Scenario C — same 9 claims with expects flipped (`ok`→`SHA_MISMATCH`,
both mutants→`ok`): `EXPECT_SUMMARY: 6/9`, `EXIT_C=1`. The check bites.

Scenario D — claim whose receipt does not exist: `RECEIPT error-missing-receipt
ERROR`, `EXPECT_SUMMARY: 1/2`, `EXIT_D=2`.

Claim-file validation: a claim missing `tool` and one with `expect: "maybe"`
both print `RECEIPT claim#N ERROR (bad claim or expect)` → `0/2`, exit 2; a
non-JSON claims file prints `RECEIPT_CLAIMS_ERROR: …` and exits 2.

Extraction unit checks (both branches, literal strings): JSON-key form and
`:`-separator header both return `('962919ce…', 'd9a5a18…')`; a plain
`MADO_TRIPWIRE` body returns `(None, None)`.

## Integration notes for L1

- The six placeholders expect lane paths
  `.ufo/waves/round-18/evidence/tripwire-{r13,r14,r15,r16,anchor-r15,pacmanlog-join}-recut.txt`.
  When each re-cut receipt lands, set its `rev` to the lane commit that holds
  it (keep `expect: "ok"`); a correct receipt must then print `ok`, giving
  `15/15` and exit 0.
- Fixtures currently use `rev: "WORKTREE"`. Commit them with the wave (or
  afterwards point their `rev` at the integrating commit); both work.
- Receipt header must contain the full 64-hex `tool_sha256` and full 40-hex
  `measured_commit`; short revs are not accepted (git resolves short revs fine,
  but the header regex requires 40 hex, matching the round-14 provenance shape).

## Risks / limits

- The JSON-key fallback matches anywhere in the receipt, so a receipt embedding
  another tool's `"tool_sha256"` pair would self-attest; the header form is the
  intended shape. Receipts here use the header form.
- The checker does not assert ancestry of `measured_commit` in `rev`, nor that
  the recorded command is the one that ran; it binds digest↔commit only, which
  is exactly R17-V1/V2's failure.
- `receipt-check.py` shells out to git read-only commands; it performs no lane
  writes.

Blockers: none.

# ReceiptLabelCheck — round-17 wave 1 report

Seat: `MadoR17.ReceiptLabelCheck` (leaf executor). Assignment: create the
able-to-fail receipt-label checker for C1 M1 — two files only under
`.ufo/waves/round-17/` — seed it with the R16-V1 red claim plus a green
control, run it, paste output.

## Files created

- `.ufo/waves/round-17/label-check.py` — `python3 -I`, stdlib only. Reads
  `label-claims.json` (sibling default; `argv[1]` override). Per claim:
  `git show <rev>:<doc>` line window must contain both the receipt basename
  and the claimed token; `git show <rev_receipt>:<receipt>` must parse as
  JSON and carry the token in any `stdout`/`stderr`/`finding`/`detail`/
  `verdict` string field (recursively). Prints `LABEL <id> ok` /
  `LABEL <id> MISMATCH (<stage>)` per claim, then `LABEL_SUMMARY: k/n`.
  Exit 0 all ok, 1 any mismatch, 2 could-not-evaluate (wins over 1).
- `.ufo/waves/round-17/label-claims.json` — two seed claims (below).

## Schema note for L1

Claim keys: `id`, `doc`, `rev`, `line`, `receipt`, `rev_receipt`, `token`,
plus optional `line_end` (inclusive) because the cited lesson statement wraps
across lines 131–132 — basename lands on 132. Without `line_end` the check
tests exactly `line`.

## Seed claims (evidence gathered first)

- **R16-V1-red** — doc `corpus/lessons/round-16.md` @ `27cd06f` lines 131–132:
  "Input tamper control returns **2 snapshot_tampered**, retained in
  `frozen-tampered.json`." Receipt `frozen-tampered.json` (added at `1e31681`,
  `measured_commit 9dcf2489…`) records exit 2, `finding: frozen_error` —
  the token `snapshot_tampered` is absent → expected MISMATCH. `git grep`
  confirmed the token/basename pair spans lines 131–132.
- **frozen-match-green** — same doc @ `27cd06f` lines 128–129: claims
  `frozen_match` retained in `action-frozen-final.json`. That receipt
  (added at `4bfb236`, measured `1e31681`) carries `frozen_match` in both
  stdout banner and JSON `finding` → expected ok.

## Observed run (this seat, on /tmp-free inputs — own new script only)

```text
$ python3 -I .ufo/waves/round-17/label-check.py
LABEL R16-V1-red MISMATCH (receipt fields lack token 'snapshot_tampered')
LABEL frozen-match-green ok
LABEL_SUMMARY: 1/2
EXIT=1
```

The MISMATCH fires at the receipt stage, not the doc stage — the doc window
does contain basename + token, so the check isolates exactly the R16-V1
defect (doc claim vs. what the cited receipt actually recorded), and it is
demonstrably able to fail.

## Risks / blockers

- None blocking. `line_end` is a small extension over the literal spec; keep
  or drop at integration (claims work without it if `line` points at a line
  carrying both tokens).
- Checker resolves repo root via `git rev-parse --show-toplevel` from the
  script dir; works in this lane (`.git` present). No jj used, no commits,
  no host probes, no installs.

No tools installed; no pacman/sudo/systemctl/live probes run.

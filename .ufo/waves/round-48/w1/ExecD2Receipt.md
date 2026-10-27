# ExecD2Receipt — routed D2: the "findings=128 at the tip (115 at base)" claim, receipted

Round 48, wave w1, seat `ExecD2Receipt` (leaf executor). Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Instrument:
`quality/check-session-material.py`, run read-only (it only calls `git ls-tree` / `git cat-file` and never writes the
lane). Nothing in the lane was edited; every write is this seat directory.

## 1. What D2 attacks

- Claim under attack, fleet report (read-only source): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/mado.md:104`
  — `findings=128 at the tip (115 at base)`.
- Routing: `corpus/lessons/round-47-verifier-spotcheck.md:132` — "the report's … has no committed receipt", with
  `:133` noting `git grep -c 'findings=128' d40189c9` finds nothing.
- Both locators are computed, not typed: `receipts/claim-and-gate-identity.txt` (grep -n against the report file and the
  lesson) and `receipts/claim-literal-and-filecounts.txt` (git grep at `579f694b`; the only surviving literal is the
  lesson's own quotation of the claim at `round-47-verifier-spotcheck.md:132`, i.e. the routed text, not a receipt).

## 2. Result — the two numbers reproduce exactly

Exact command shape (both forms run; byte-identical, `receipts/cwd-form.txt`):

```
TMPDIR=/fast/scratch/hyaku/mado-r48/ExecD2Receipt python3 -I \
  /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev <rev>
# the historical form `cd <lane> && … --repo . --rev <rev>` gives identical bytes
```

| revision | meaning | `files=` | `findings=` | R1 | R2 | R3 | R4 | rc | receipt |
|---|---|---|---|---|---|---|---|---|---|
| `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` | round-47 base | 18371 | **115** | 29 | 31 | 53 | 2 | 1 | `receipts/session-material-60edb66e.txt` |
| `d40189c924e01dc1cbe290474eb4256d343590d4` | round-47 tip | 19969 | **128** | 33 | 36 | 57 | 2 | 1 | `receipts/session-material-d40189c9.txt` |
| `579f694b45c797a9c39761fdb4f9e0a1b71b3585` | round-48 base | 19969 | **128** | 33 | 36 | 57 | 2 | 1 | `receipts/session-material-579f694b.txt` |

The per-rule columns are the number of findings (FINDING lines) carrying that rule; `receipts/` rows also carry the
gate's own `SESSION_MATERIAL_RULES:` and `SESSION_MATERIAL:` lines verbatim, plus the `EXIT rc=` line.

Reproducibility, three ways (`receipts/session-material-*.txt` §REPEAT, `receipts/clone-crosscheck.txt`,
`receipts/cwd-form.txt`):

1. **3 runs per revision**: the three outputs are byte-identical at each of the three revisions.
2. **Scratch clone**: `git clone -q --shared <lane>` into the seat scratch, `git -C <clone> rev-parse --show-toplevel`
   asserted equal to the clone before any run; the gate's output from the clone is byte-identical to the lane run at
   all three revisions — the numbers are tree-intrinsic, not a worktree or untracked-file artefact.
3. **Command form**: `--repo .` with cwd in the lane equals the absolute-path form, byte for byte.

Instrument identity (`receipts/claim-and-gate-identity.txt`): `quality/check-session-material.py` is the **same blob**
`9d60e4c1ad251816e93184100bf1be05c649cd63` at all three revisions, and the worktree file's
sha256 is `889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb` — the frozen original the round-47
spot-check names. So `115` and `128` are like-for-like readings of one instrument: the difference is tree content only.
The `files=` column also equals `git ls-tree -r --name-only <rev> -- .ufo | wc -l` at each revision
(`receipts/claim-literal-and-filecounts.txt`), i.e. 18371 → 19969 (+1598 files) while findings move +13.

## 3. Triage of the +13 (the "new findings are not triaged" note)

`receipts/new-finding-pairs.txt`, computed as `comm` on the FINDING lines with the `count=` column stripped:
**13 new `(file, rule)` pairs, 0 gone**; all 13 sit in `.ufo/waves/round-47/` w1/w2 seat files. Per rule: R1 +4, R2 +5,
R3 +4.

The carriers are copies of the gate itself, so the gate is flagging its own embedded selftest fixtures:
`w1/ExecSessionMarker/check-session-material.py`, and `w2/MutSessionMarker/probe/gates/{gate-pristine,gate-m1,gate-m2}.py`
— all four are the **same blob** `9103bbdc86789578cb41ab6cbbd645181d96c229` (946 lines added / 29 removed against the
tracked gate), each carrying the three fixture constants; the remaining R2 pair is
`w2/RevSessionMarker/probes/probe_bigfile.py`. See `receipts/new-carriers-relation.txt`.

Observation, not a verdict (out of this seat's scope): the three `MutSessionMarker` probe gates are byte-identical to
the `ExecSessionMarker` gate copy (one shared blob), so those "mutant" files are not mutants at the file level. Routed
information for the L1 only.

## 4. Verdict and the closure paragraph for the round-48 report

D2 is a **receipt gap, not a numeric error**: `115` at `60edb66e` and `128` at `d40189c9` both reproduce exactly, with
three identical runs each, from a scratch clone as well, using the gate blob that is identical at both revisions. No
correction to the number is required. What was missing is the citable run, and this seat supplies it, including at the
round-48 base `579f694b` (also 128), so the round-48 report can cite a revision that is an ancestor of the lane tip.

Correction/closure line for the round-48 report (single paragraph):

> **D2 closed — claim reproduces, the defect was the absent receipt.** `quality/check-session-material.py`
> (blob `9d60e4c1…`, worktree sha256 `889f8f05…`, unchanged at all three revisions) reads `files=18371 findings=115`
> at round-47 base `60edb66e`, and `files=19969 findings=128` at round-47 tip `d40189c9` and at round-48 base
> `579f694b` (R1 29→33, R2 31→36, R3 53→57, R4 2→2, exit 1 each); three runs per revision are byte-identical, and a
> scratch clone reproduces the lane numbers byte for byte. The +13 are 13 `(file, rule)` pairs and 0 removals, all in
> round-47 w1/w2 seat files that carry copies of the gate and therefore its own selftest fixtures — so the round-47
> report's number stands, and only its missing receipt is closed (see
> `.ufo/waves/round-48/w1/ExecD2Receipt/receipts/`).

Residual: the fix is only fully satisfied once the integrator commits these receipts (this seat may not commit).

## 5. Retained evidence (all under `w1/ExecD2Receipt/receipts/`)

| file | proves |
|---|---|
| `session-material-d40189c9.txt` | tip scan: command line, date, gate blob + sha256, full FINDING/tally output, rc, then 3 repeat summaries |
| `session-material-60edb66e.txt` | round-47 base scan, same shape (115) |
| `session-material-579f694b.txt` | round-48 base scan, same shape (128) |
| `clone-crosscheck.txt` | clone toplevel assertion + identical output at all three revisions |
| `cwd-form.txt` | `--repo .` historical form equals the absolute form at base and tip |
| `claim-and-gate-identity.txt` | claim locators (grep -n), gate blob at each rev, worktree sha256, ancestor checks |
| `claim-literal-and-filecounts.txt` | `git grep 'findings=128'` per revision; `.ufo` file counts per revision |
| `new-finding-pairs.txt` | the 13 new `(file, rule)` pairs, 0 gone, per-rule and per-wave counts |
| `new-carriers-relation.txt` | blob identity and line delta of the new carriers vs the tracked gate |
| `verify-report.txt` + `verify-report.py` | this report checked against the receipts: `VERIFY ok=25 failed=0` (every table row, tally, locator, clone/cwd equality, 13-pair count and the receipt-line shape re-derived from the receipt bytes) |

Receipts contain counts, rule classes, git identities and finding *paths* only; no matched session-material value is
printed anywhere in this seat's output (the gate itself prints none).

## 6. Risks / blockers

- **Integration dependency**: D2's "committed receipt" fix lands only when the L1 commits `receipts/`. Untracked until then.
- **Instrument-version sensitivity**: the tally is defined by the gate blob; it must be re-identified if the marker gate
  (R3, still uninstalled) is ever installed, because R5/R6 would change the tally's meaning.
- **Scratch**: all clones and gate temp files lived in `/fast/scratch/hyaku/mado-r48/ExecD2Receipt/` (peak 310 MB, under
  the 2 GB bound); that directory was deleted at seat end. No `/tmp`, `~/.local/bin`, fleet-root or lane tracked file was written; no package transaction,
  no compositor or process interaction.
- **Blockers**: none.

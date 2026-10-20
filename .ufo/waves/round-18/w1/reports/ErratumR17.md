# ErratumR17 — report

Scope: draft only. Wrote `.ufo/waves/round-18/drafts/ErratumR17.md` (erratum block for `corpus/lessons/round-17.md` after line 176, and the R17-V2 carry-over sentence). No product, lesson, SCORECARD or LOG edits. No git or jj writes; read-only `git log`, `git show`, `git grep`, python JSON reads of blobs. No subagents. No installs or updates.

## Shas, verified by `git show <rev>:tools/mado-tripwire.py | sha256sum`

| Rev | Label | sha256 |
|---|---|---|
| `988b858` | pre-fix tool (round-17 C3 capability) | `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44` |
| `f71ccbe` | wave-2 corrections tool (before→after measure) | `7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7` |
| `0ab1ccc` | landed tip tool (P11 fix) | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` |
| HEAD worktree | `tools/mado-tripwire.py` | `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072` |

Cross-checks: `evidence/measure-final.json` `c3.sha256` = `7a98720e…` at `rev` `f71ccbe`. SCORECARD C3 row and `lessons/round-17.md:175` = `962919ce…`. Fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mado.md`: line 3 cites `962919ce…` and "receipts re-cut with identical counts"; line 76 (C3 before→after row) cites `7a98720e…`.

## What git records for the real-transcript receipts

Each receipt was compared between `988b858`, `f71ccbe` and `0ab1ccc` (parsed JSON line 2 and bytes).

| Receipt | Last changed | Under tool | Finding |
|---|---|---|---|
| `tripwire-r13.txt` | `f71ccbe` | `7a98720e…` | aggregate counts identical; one file entry `unparsed_spawns` 0→1; byte-identical `f71ccbe`→`0ab1ccc` |
| `tripwire-r14.txt` | `f71ccbe` | `7a98720e…` | aggregate identical; one `unparsed_spawns` 0→1; not touched at `0ab1ccc` |
| `tripwire-r15.txt` | `f71ccbe` | `7a98720e…` | aggregate `live_probe` 28→29 (not identical); one `unparsed_spawns` 0→1; not touched at `0ab1ccc` |
| `tripwire-r16.txt` | `f71ccbe` | `7a98720e…` | aggregate identical; three entries `unparsed_spawns` 0→1/2; not touched at `0ab1ccc` |
| `tripwire-anchor-r15.txt` | `f71ccbe` | `7a98720e…` | counts and exit identical; finding line 29 command `pacman -Fl libinput-tools 2` → `pacman -Fl libinput-tools`; 8 findings both |
| `tripwire-pacmanlog-join.txt` | `f71ccbe` | `7a98720e…` | appended 6-line wave-2 correction paragraph; no count receipt |
| `tripwire-r17.txt` | `0ab1ccc` | `962919ce…` | aggregate identical (0/1/0); 40 of 149 entries changed; MadoR17.jsonl sha `da1b4492…`→`01229723…`, 468→540 lines, bash_calls 74→88, eval_calls 24→31 |

`git log --oneline -- <file>` for r13, r14, r15, r16, anchor-r15 and pacmanlog-join lists `f71ccbe` and `988b858` only. Under `0ab1ccc` the only receipts that changed are `tripwire-r17.txt`, `tripwire-vs-oracles.json`, the four selftest receipts, `tripwire-w2-adversarial.txt` and `tripwire-w2-false-positive.txt`. The line 176 "all real-transcript receipts re-cut" claim is therefore supported for one receipt (r17) only.

Receipts carry no tool sha256 or measured-commit field (R17-V1 confirmed).

## Findings

1. **Erratum (lessons/round-17.md:175-176) is substantiated.** The landed-tool sha is correct; "all real-transcript receipts re-cut with identical counts" is not. Erratum text is in the draft, section (a).
2. **"Identical counts" is too strong even at f71ccbe.** r15 `live_probe` 28→29, and the anchor receipt's command text changed. The erratum says so explicitly.
3. **Source drift (for TwFrozenSnapshot / C3 pinning).** The MadoR17 transcript changed between `f71ccbe` and `0ab1ccc` (sha `da1b4492…`→`01229723…`, 468→540 lines), so the `0ab1ccc` re-cut read a different source than the `f71ccbe` receipt. Cause (transcript still being written) is `[INFERENCE]`. A frozen replay must pin the source sha at snapshot time; the round-17 `session-index.json` digests may not match the current file. Not verified further here.
4. **R17-V2 carry-over sentence** is in draft section (b), citing both shas with labels.

## Round-18 receipts

`.ufo/waves/round-18/evidence/tripwire-*.txt` do not exist at `d3a0000` (the evidence directory holds census files only). The draft says they are to be produced. This report does not produce them.

## Out of scope / not done

- Did not re-run the tripwire or any scan, the selftests, or measure.py.
- Did not verify the `w2-regressions` 30/30 count (the draft does not assert it).
- Did not open the round-17 transcripts beyond what the receipts reference, nor the fleet root beyond the two read lines above.
- Did not check `.ufo/waves/round-17/evidence/session-index.json` against the MadoR17 sha; the cause of the drift (the transcript grew after the f71ccbe re-measure) is `[INFERENCE]` from the line counts, not observed.

## Files touched

- Written: `.ufo/waves/round-18/drafts/ErratumR17.md`, `.ufo/waves/round-18/w1/reports/ErratumR17.md`.
- Read only: `corpus/lessons/round-17.md`, `corpus/lessons/round-17-verifier-spotcheck.md` (§6), `.ufo/waves/round-17/evidence/*`, `tools/mado-tripwire.py` (via git), `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mado.md` (lines 3, 76).

## Checks for the main agent

None required from this seat. L1 integrates the draft into `corpus/lessons/round-17.md` (append-only) after reviewing it, and once the round-18 receipts exist, re-checks the sha claims with the same `git show <rev>:tools/mado-tripwire.py | sha256sum` form.

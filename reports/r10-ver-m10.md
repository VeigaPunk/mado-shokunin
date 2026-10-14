# VER-M10 — round-10 synthesis verification: the gate-revision ladder re-derived (one arc claim)

Lane VER-M10, 2026-10-14 (round-10 wave, "the synthesis verifier"). Dispatch
contract: re-derive one arc claim independently, poll with a 25-min cap, do
not edit. Window: dispatch ~20:50Z; poll `/tmp/w10-ver-m10/poll.sh` →
`poll.log` (20 s cadence, samples 20:53:02Z → 21:17:23Z, `POLL_END
21:17:43Z`). **Read-only on every artifact**: the gate, the repo, the sibling
trees were only read; no repo file other than **this report** was written by
this lane. No socket opened; no compositor/session mutation; no external
site; secrets shape-only. Marks: **[O]** measured, **[I]** inference,
**[U]** unknown. File path follows the VER-M8/VER-M9 convention
(`reports/r9-ver-m9.md`); the dispatch named no path.

## Claim under verification (one)

The arc's **gate-revision ladder** — the chain of `tools/mado-verify.sh`
revisions across the arc as the round-10 synthesis must carry it
(`plans/round-10.plan.md:125-136`, (a)(ii)) — in three columns: (1)
per-commit git-blob sha256 / bytes / `wc -l`; (2) the per-revision selftest
count; (3) the regression pin lineage (`PIN_MADO`, `SPEC_SHA`). Every cell
re-derived one level below the records: `git show <commit>:tools/mado-verify.sh`
piped to `sha256sum`/`wc -c`/`wc -l`; byte-copies of each revision re-run
`--selftest` from scratch; pins read from the gate's own source per revision;
then the landed synthesis's ladder section compared cell-by-cell.

## 1. Revision chain re-derived [O]

Creation commit = round 5 (`git log --diff-filter=A -- tools/mado-verify.sh`);
rounds 0–4 (mint + r1–r4, five commits) carry no gate file at all.

| arc commit | date (−03) | gate blob sha256 | bytes | `wc -l` | selftest re-run 20:55:09–22Z |
|---|---|---|---|---|---|
| mint `74d3b7b` … r4 `3d9ba45` | 09:50–13:57 | — no `tools/mado-verify.sh` in tree | — | — | — |
| r5 `eead56b` (creation) | 14:33:30 | `d7edaab4bf108625…32d0e13` | 45,334 | 1,098 | **28/28** rc 0 |
| `c03c249` (SHONEN commit) | 14:34:46 | `d7edaab4…` (unchanged) | 45,334 | 1,098 | — |
| r6 `c8f6667` | 15:17:26 | `c4c1afb75dd1c8aa…1a625171` | 50,126 | 1,186 | **53/53** rc 0 |
| r7 `0c20a76` | 16:06:31 | `90d50cdd4d18410b…a3100bd` | 75,771 | 1,755 | **89/89** rc 0 |
| r8 `12c8f08` | 16:55:09 | `7da4ec5013583c91…25f2f4f` | 131,612 | 2,887 | **217/217** rc 0 |
| r9 `de22dfd` | 17:47:30 | `93e43f8fe8b9bdd4…bc00095` | 150,103 | 3,231 | **268/268** rc 0 |
| r10 | — | no landing within the poll cap (HEAD `de22dfd` at 21:17:43Z; gate `93e43f8f…bc00095` unchanged) | — | — | — |

All five re-run selftests exit 0 with counts identical to the records
(r5 28/28 `gate-mutation-proof.md:148`; r6 53/53 `:150`; r7 89/89 `LOG.md:297`;
r8 217/217 + r9 268/268 `snapshot-diff-receipt-r9.md:28-33`, VER-M9, AUD-M9).
Worktree gate sha identical before and after the whole battery
(`93e43f8f…bc00095`). Copies + logs: `/tmp/w10-ver-m10/ladder/<rev>.{sh,log}`.

## 2. Pin lineage re-derived [O]

Read from the gate's own source at each revision
(`git show <rev>:tools/mado-verify.sh | grep -nE '^PIN_MADO=|^SPEC_SHA='`):

- r7 gate `:749` `PIN_MADO=c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171`
  — byte-identical to the r6 git blob (the derived-target excision proof).
- r8 gate `:1107` `PIN_MADO=d2bcdb31daea5d68dc7c586617939d71d525dbeab723e72b8c17644ad327db62`.
- r9 gate `:1290` `PIN_MADO=dc7c4141449891cdd83bb603aff7215358328a9ce1b32dba0bb9c0514cb6f8fd`.
- `SPEC_SHA=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8`
  constant r7–r9 (`:750`/`:1108`/`:1291`); `TABLE_MADO` 10/10 KILLED rows
  constant r7–r9. r5/r6 gates carry no pin (absent, as the synthesis says).

Lineage: `c4c1afb7…1a625171` → `d2bcdb31…27db62` → `dc7c4141…cb6f8fd`.

## 3. The landed synthesis, compared [O]

The synthesis landed as **`corpus/knowledge/arc-synthesis.md`** (plan §(a)
proposed `ten-round-synthesis.md`; the landing renamed it — my poll watched
the planned name and kept `synth=-`, the file was detected via `git status`
at 21:06Z and had mtime 17:57 −03). At every read 21:06:30Z → 21:17:54Z:
sha256 `a5b48331414618108cdc9596cf6c7cc0dc78994ebcf61141c3e6d80428419d50`,
387 `wc -l` / 30,796 B, self-label M10-1 — **stable**.

Its §2.1 ladder table (`:124-131`), row by row:

- r5 `d7edaab4bf108625` / 1,098 / 45,334 / 28/28 / PIN (absent) — **matches**;
- r6 `c4c1afb75dd1c8aa` / 1,186 / 50,126 / 53/53 / (absent) — **matches**;
- r7 `90d50cdd4d18410b` / 1,755 / 75,771 / 89/89 — **matches**; PIN cell
  reads `c4c1afb7…a5171` — **does not reproduce** (finding F1);
- r8 `7da4ec5013583c91` / 2,887 / 131,612 / 217/217 / `d2bcdb31…db62` —
  **matches**;
- r9 `93e43f8fe8b9bdd4` / 3,231 / 150,103 / 268/268 / `dc7c4141…f8fd` —
  **matches** (the round-9 receipt's wrong `…db62` tail, F2, was *not*
  propagated).
- `c03c249` identical r5 blob (`:133`) — matches.
- `:151` `REGRESSION_HARNESS cf41efaa…242c75` — correct as-of its run
  (m10-1 regression at 20:51:02Z, `/tmp/w10-m10-1/regression.log`); the
  harness has since moved (adjacent note below).

## 4. Findings — record cells that do not reproduce [O]

- **F1 — the `…a5171` tail is a prose corruption.** Correct tail of the r6
  blob / r7 pin: `…1a625171` (last4 `5171`; no suffix segment equals
  `a5171`). Earliest occurrence `gate-mutation-proof.md:22` (round-6 note);
  the same file quotes the full sha correctly at `:150`, and
  `reports/r7-aud-m7.md:58` shows the harness's own full-sha print with
  `match=yes`. Total at my 21:08Z read: **31 occurrences in 12 files** —
  including the landed synthesis (`arc-synthesis.md:129`, `:167`) and the
  round-10 record draft (×2). Round-10's `r10-aud-m10.md` and
  `gate-standing-use.md` are clean. **The synthesis and the round-10 record
  must not publish this tail; correct form `c4c1afb7…5171` (or
  `…1a625171`).** I do not edit; flagged for the author/scribe.
- **F2 — one wrong pin tail in the round-9 receipt.** `snapshot-diff-receipt-r9.md:33`
  reads "`PIN_MADO` re-cut to `dc7c4141…db62`"; the actual re-cut pin
  (`de22dfd:…:1290`) ends `…c0514cb6f8fd`, and `db62` is the previous
  pin's (`d2bcdb31`) tail. One occurrence; not propagated (all round-10
  artifacts read `dc7c4141…f8fd`; `r9-aud-m9.md:31/:85-88` correct).
- **F3 — one wrong line count in a round-9 note.** `walker-deep-r9.md:296`
  parenthetical "(round 8 ended at 2,837 L)" — the round-8 revision
  `7da4ec50` is 2,887 L / 131,612 B; `2,837` reproduces nowhere. Not
  propagated into the synthesis (no `2,837` there).

Adjacent, provenance-only [O]: the tameshi harness moved at least twice
during the round-10 window — 20:51:02Z m10-1's run pinned `cf41efaa…242c75`
(61,632 B); 20:55:1xZ read `818889d0…` / 70,296 B; 21:18:09Z read
`75ed934d…` / 77,904 B (mtime 18:00 −03). Live sibling-lane write; receipts
pin it, not gated.

## 5. Spot-checks (3, named)

1. **Revision chain** — 9 arc commits walked; 5 gate blobs + bytes + line
   counts re-derived (r1–r4: no gate; creation = r5) — every cell matches
   the records and the landed synthesis where quoted.
2. **Selftest column** — five byte-copies re-run, five rc-0 runs, counts
   28/53/89/217/268 reproduce; gate sha unchanged before/after. The landed
   synthesis prints the same column as its own re-runs (`:134-135`).
3. **Synthesis comparison + pins** — §3 above: 15/15 measured ladder cells
   match; 1/3 pin-cell tails (`…a5171`) fails re-derivation; three pins +
   `SPEC_SHA` read from source.

## 6. Round-10 landing at the poll cap [O]

`POLL_END 2026-10-14T21:17:43Z` (25-min cap honored, no extension). HEAD
`de22dfd` and gate `93e43f8f…bc00095` stable throughout; at cap
`git status --porcelain`: ` M SKILL.md` + 5 untracked
(`corpus/knowledge/arc-synthesis.md` `a5b48331…`;
`corpus/knowledge/gate-standing-use.md` `aaa2e625…` / 361 L, first seen
20:55:41Z; `plans/round-10-record-draft.md` `ed79d90a…`;
`plans/round-11.plan.md`; `reports/r10-aud-m10.md` `d9892618…`) — **no
commit** at cap. The synthesis was verified at its landed bytes; later edits
re-open the comparison.

## Unknowns

- [U] The round-10 commit and its gate blob (expected unchanged at
  `93e43f8f…` if round 10 opens no gate edit) — not observed; commit lands
  after this lane's cap.
- [U] Whether F1 is corrected before the commit — outside this lane's
  scope (do not edit); the correction is `…1a625171` / `…5171`.
- [U] The regression replay at r9/r10 (10-defect, `MADO_REGRESSION: PASS`)
  and the derived-target lineage by excision are outside this claim — not
  re-derived here (AUD lanes' territory); the source pins were read, not
  re-cut.
- [U] Harness movement is live (sibling lane) — any later receipt re-reads
  it; printed provenance is timestamped only.

Boundary: repo read-only; no commit; no edit; scratch `/tmp/w10-ver-m10/`
(`poll.sh`, `poll.log`, `ladder/` 5 copies + 5 logs, `report-draft.md`);
substrates (`~/.config`, live session, omarchy checkout) untouched.
# ScoutControls7 — round-33 leftover trees vs committed receipts

Date: 2026-10-24. Scope: the seven disclosed round-33 leftovers —
`controls/{entries-only,extra-source,golden,hash-mismatch,junk,rows-only}` and
`scratch/ExecK2Receipts`. Full per-file table:
`.ufo/waves/round-34/scratch/ScoutControls7/table.md`. Nothing deleted.

## Findings

All seven trees are **untracked** — `git status --porcelain .ufo/waves/round-33`
lists each as `??`. The committed receipts (`controls/*.txt`, `controls/RECEIPT.md`,
all in commits `9a46ccf`/`69f7210`) carry only predicate verdict lines
(`PRED-C1-r33-v1 closed_entries=… verdict=…`, `exit=N`), never fixture bytes.

| Tree | Files | Bytes | Verdict committed as receipt? | Adds beyond receipt? |
|---|---|---|---|---|
| entries-only | 2 | 256 | yes — `c1-entries-only.txt` TARGET_MISSED exit=1 | No — bytes duplicated/same-class vs committed fixtures |
| extra-source | 7 | 63,492 | yes — `c1-extra-source.txt` TARGET_MET exit=0 | No — all 4 bins byte-identical to committed `fetch/`/CriticC1Junk copies |
| golden | 7 | 63,451 | yes — `c1-golden.txt` TARGET_MET exit=0 | No — bins byte-identical to committed copies |
| hash-mismatch | 7 | 63,452 | yes — `c1-hash-mismatch.txt` TARGET_MISSED exit=1 | Bytes yes (unique doctored S190 `117f29…`), evidence no |
| junk | 7 | 665 | yes — `c1-junk.txt` TARGET_MISSED exit=1 | Bytes yes (unique 11-B placeholders + junk entries), evidence no |
| rows-only | 1 | 462 | yes — `c1-rows-only.txt` TARGET_MISSED exit=1 | No — its sole file is byte-identical to junk's SOURCES.md |
| scratch/ExecK2Receipts | 30,892 (3 clones) | 545,942,365 | no `controls/*.txt`; receipt = committed `w1/reports/ExecK2Receipts.md` | Bytes yes — sole copies of control commits `4590b98`, `a3a79ce` (absent from lane repo, `git cat-file -t` → fatal); evidence no — report pastes all outputs verbatim |

## Per-tree deltas worth naming

- **hash-mismatch**: `.ufo/waves/round-33/fetch/S190.bin` is 6,551 B vs committed
  6,550 B, sha `117f29…` vs `799bf0…` — the doctored byte exists only in this tree.
- **junk**: all four bins are identical 11-byte placeholders (`14830a…`); the two
  knowledge entries (`7b3322…`, `d1a442…`) are unique junk bytes, distinct from the
  committed `scratch/CriticC1Junk/` junk payloads.
- **ExecK2Receipts**: three ~202 MB working trees (`a-stale` @ `4590b98`,
  `b-rederived` @ `9a46ccf`, `c-perturb` @ `a3a79ce`). ~546 MB total — 99.9% of the
  leftover volume. Its own report marks it "uncommitted scratch per lane hygiene".

## Verdict

Every control outcome is already receipted; no tree carries evidence the committed
receipt lacks. The trees' only unique content is regenerable fixture payload — plus,
in ExecK2Receipts, two throwaway control commits replayable from the report. All
seven are safe-to-clean candidates; deletion is the operator's call, not taken here.

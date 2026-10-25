# ScoutControls7 — round-33 leftover trees vs committed receipts

Inspected 2026-10-24. Root: `.ufo/waves/round-33/`. All seven trees are **untracked**
(`git status --porcelain .ufo/waves/round-33` lists each as `??`). The committed
receipts under `controls/*.txt` + `controls/RECEIPT.md` are verdict lines only —
they carry the counter output (`PRED-C1-r33-v1 … verdict=…`, `exit=N`), not fixture
bytes. So for every tree: the *verdict* is committed; the *content* is not part of
any receipt. Column "adds beyond receipt" asks whether the tree holds anything the
committed evidence does not already cover.

| Tree | Files | Bytes | Committed receipt (controls/*.txt) | Verdict committed? | Adds anything beyond receipt? |
|---|---|---|---|---|---|
| `controls/entries-only/` | 2: `corpus/knowledge/event-delivery-limits-r26.md` (114 B), `corpus/knowledge/waybar-module-text-route-r25.md` (142 B) | 256 | `c1-entries-only.txt` (88 B): `closed_entries=0 closed_rows=0 open_cites=4 TARGET_MISSED exit=1` | Yes — verdict + exit; RECEIPT.md maps fixture→line | **No.** Only raw fixture bytes. event-delivery copy `8afe57…` is byte-identical to committed `scratch/CriticC1FalseNeg/golden/` copy; waybar variant `b902ab8…` is unique bytes but same evidentiary class. Receipt already carries outcome. |
| `controls/extra-source/` | 7: 2 knowledge entries (114 B, 183 B), `corpus/SOURCES.md` (450 B), `.ufo/waves/round-32/fetch/S189.bin` (6,479 B), `.ufo/waves/round-33/fetch/S190.bin` (6,550 B), `S191.bin` (8,324 B), `S197.bin` (41,392 B) | 63,492 | `c1-extra-source.txt` (85 B): `closed_entries=2 closed_rows=4 open_cites=0 TARGET_MET exit=0` | Yes | **No.** S190/S191/S197 byte-identical to committed `fetch/`; S189 `eea605…` identical to committed `scratch/CriticC1Junk/` + `CriticC1FalseNeg` copies; waybar `545097…` identical to committed CriticC1FalseNeg copy. Only the extra-source row in SOURCES.md is fixture-specific; receipt carries outcome. |
| `controls/golden/` | 7: same layout as extra-source; knowledge 114 B + 142 B, SOURCES.md 450 B, 4 bins (6,479 + 6,550 + 8,324 + 41,392 B) | 63,451 | `c1-golden.txt` (85 B): `closed_entries=2 closed_rows=4 open_cites=0 TARGET_MET exit=0` | Yes | **No.** All four bins byte-identical to committed `fetch/` / CriticC1Junk copies; entries/SOURCES are the same trimmed fixture variants used across these trees. Receipt carries outcome. |
| `controls/hash-mismatch/` | 7: same layout as golden; S190.bin is 6,551 B (hash `117f29…`, one byte doctored vs committed `799bf0…`) | 63,452 | `c1-hash-mismatch.txt` (88 B): `closed_entries=1 closed_rows=3 open_cites=1 TARGET_MISSED exit=1` | Yes | **Bytes: yes** — the doctored S190 byte exists only here (no other copy committed). **Evidence: no** — the single-byte drift is exactly what the receipt's `closed_rows=3 open_cites=1` records; RECEIPT.md names the mapping. |
| `controls/junk/` | 7: 2 junk knowledge entries (70 B, 89 B), junk SOURCES.md (462 B), four 11-byte placeholder bins (all hash `14830a…`) | 665 | `c1-junk.txt` (88 B): `closed_entries=0 closed_rows=0 open_cites=4 TARGET_MISSED exit=1` | Yes | **Bytes: yes** — unique junk bytes (CriticC1Junk's committed junk uses different payloads). **Evidence: no** — receipt + RECEIPT.md already record that junk content yields TARGET_MISSED. |
| `controls/rows-only/` | 1: `corpus/SOURCES.md` (462 B, hash `ee6485…` — byte-identical to junk's SOURCES.md) | 462 | `c1-rows-only.txt` (88 B): `closed_entries=0 closed_rows=0 open_cites=4 TARGET_MISSED exit=1` | Yes | **No.** Single file, and its exact bytes also sit in `controls/junk/`. Receipt carries outcome. |
| `scratch/ExecK2Receipts/` | 30,892 files in 3 full lane clones: `a-stale/` 10,299 files / 182,015,404 B (HEAD `4590b98`), `b-rederived/` 10,294 files / 181,911,589 B (HEAD `9a46ccf`), `c-perturb/` 10,299 files / 182,015,372 B (HEAD `a3a79ce`) — each a complete lane checkout incl. `.git` | 545,942,365 (~546 MB) | **None under `controls/*.txt`** — its receipt is committed report `.ufo/waves/round-33/w1/reports/ExecK2Receipts.md` (in commit `69f7210`), which pastes all three gate outputs verbatim | Yes (as w1 report, not a controls txt) | **Bytes: yes** — the only copies of control commits `4590b98` (a-stale) and `a3a79ce` (c-perturb); neither object exists in the lane repo (`git cat-file -t` → fatal). **Evidence: no** — report carries all three verbatim outputs, method, and revs; clones are replayable from it. |

## Summary

- All six `controls/` trees: verdict receipts committed; trees themselves untracked
  fixture payloads. None adds evidence the receipt lacks; hash-mismatch and junk are
  the only trees holding bytes not duplicated anywhere else committed.
- `scratch/ExecK2Receipts/`: ~546 MB of scratch clones, deliberately uncommitted per
  its own report ("uncommitted scratch per lane hygiene"); receipt = the w1 report.
  Largest leftover by far; its only unique content is two throwaway control commits.

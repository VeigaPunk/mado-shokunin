# RevOldPairReconstruct — C1 narrative: why the old frozen pair scored 18/19

Seat: RevOldPairReconstruct (leaf; no subagents). Date 2026-10-25. Lane: mado-shokunin.
Read-only reconstruction from committed history; no lane writes except this seat's files.

## 0. Identity of the old frozen pair

- Freeze commit: `58e55ec9e905c85fb5a794f9a51dc06cc16166ba` ("round-38: freeze — v3
  counters (M37-5 repairs), request-ground counter, discrimination manifest, opened-source
  receipts, live triplet, assimilation scratch").
- Frozen manifest: `.ufo/waves/round-38/controls/manifest.json` @58e55ec, sha256
  `14c49d9fec35dc9bc307fbdd5c732e2ce80fabeaadfe3327b9121f50b9553edb`.
  Byte-identical copy committed as the red-before receipt
  `.ufo/waves/round-39/receipts/manifest-frozen-r38.json` (verified: same sha256).
- Frozen instruments: `quality/counters/c1-r38-event-ground.py` @58e55ec (sha256
  `41eb241997018eb7024b7fccf7beb72f0c4602c423373a89ce78376c50d252f7`) and
  `quality/counters/c2-r38-eventq.py` @58e55ec (sha256
  `194a45c68f9e5756752daa8449dda1a7ae190ea016153b8e2e2a09c29f236921`; unchanged to HEAD).
- The gate: `quality/check-r38-discrimination.py` (sparse sandbox clone, applies each
  control's writes, commits, runs the instrument at sandbox HEAD, scores agreement).
- Recorded red-before: `.ufo/waves/round-39/receipts/c1-redbefore.txt` →
  `controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1; the only failing control is
  `c1-duprow` (line 5: `expected=TARGET_MISSED observed=TARGET_MET ok=0`).

## 1. Which write op the old c1-duprow control used

Old control (manifest @58e55ec, control id `c1-duprow`, clause `j`, expect TARGET_MISSED):

```json
{"writes": [
   {"op": "append", "path": "corpus/SOURCES.md",
    "text": "| S189 | contradicting duplicate — https://example.invalid/S189-dupe | code | A | scope | anchor | teaches | mined | 2026-10-25 | 90d | corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md |\n"}
 ]}
```

- The op is `append` — an end-of-file append. In the gate, `apply_writes` dispatches
  `append` (check-r38-discrimination.py:76-77) to `_append` (lines 128-130), which opens
  the path with `open(path, "a")` and writes the text at the file end — no position
  control, no section awareness.
- So the duplicate S189 row is written as the **last line of `corpus/SOURCES.md`**, not
  inside the `## Registry` table.

## 2. File structure: why "after the section" means "invisible"

`corpus/SOURCES.md` @58e55ec (457 lines; `git show 58e55ec:corpus/SOURCES.md`):

| line | content |
|---|---|
| 9 | `## Registry` (the only section the counter parses for rows) |
| 201 | `| S189 | …` — the held row for the delivery entry (real row) |
| 219 | `| S217 | …` — last Registry row |
| 221 | `## Paths` (next `## ` heading after `## Registry`) |
| 267 | `## Search log` |
| 431 | `## Leads (unopened)` |
| 457 | last line (prose under `## Leads (unopened)`) |

The appended dup row lands at line 458, after `## Leads (unopened)` — under no section at
all, and certainly outside `## Registry`.

## 3. How the counter's `section()` / `registry_rows()` parser misses it

`quality/counters/c1-r38-event-ground.py`:

- `section(text, heading)` (lines 122-132):
  - toggles `inside=True` only on an exact line match `line.strip() == heading`
    (`"## Registry"`, line 125-127);
  - breaks at the **next line starting with `"## "`** (line 128-129);
  - accumulates only the lines in between (line 130-131).
  - Consequence: rows placed after any later `## ` heading — or after the file's last
    heading, as here — are never collected.
- `registry_rows(text)` (lines 135-142): builds the per-id row map only from
  `section(text, "## Registry")`. The appended row is not in that list.
- Clause `j` (lines 213/223/225 in the frozen counter; lines 226 in the current counter):
  `j_ok = j_ok and len(rows.get(i, [])) == 1`. It only counts rows the parser *saw*.
  With the duplicate invisible, `rows["S189"]` has exactly the one real row → `j=1`.
- Clause `c` (frozen counter lines 201-207): `any(... for r in rows.get(i, []))` — with
  only the real row visible it passes. (The later `859d0cf` counter patch changed this to
  `len(rows.get(i, [])) == 1` and the row-binding lambda; that is a second, parallel
  uniqueness guard — see §5.)

Net effect for the `c1-duprow` control: every clause for both target entries evaluates
1 → `admitted=2/2` → `TARGET_MET`, while the control expects `TARGET_MISSED` (the crib's
whole point is that a contradicting second row must be rejected). Verdict mismatch →
`ok=0` → `correct=18/19` → `TARGET_MISSED`, exit 1.

## 4. The 18/19 is the manifest's write placement alone

Cross-pairing replayed in round-38 evidence (ScoutConsiderThese report, landed in `f551b70`;
RevManifestIntegrity §D, landed in `e072af6`):

| counter | manifest | verdict | c1-duprow |
|---|---|---|---|
| frozen `58e55ec` | frozen `58e55ec` | 18/19 | observed MET (crib passes) |
| frozen `58e55ec` | landed `b6c1d31` | 19/19 | observed MISSED |
| landed `859d0cf` | frozen `58e55ec` | 18/19 | observed MET (crib passes) |
| landed `859d0cf` | landed `b6c1d31` | 19/19 | observed MISSED |

Both counter versions give the same 18/19 against the frozen manifest and 19/19 against the
landed one ⇒ the failure scope is the manifest control's write op, not the counter's
version. The frozen counter already had clause `j` (verified in the blob at 58e55ec).
Round-38 errata `f551b70` names the same conclusion ("the manifest control alone") and
notes the `859d0cf` counter patch is verdict-no-op for this control.

## 5. What the repaired control does differently

The repaired/landed manifest (`.ufo/waves/round-38/controls/manifest.json` @base
`08be4eb`; sha256 `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`),
re-frozen byte-for-byte as `.ufo/waves/round-39/c1/manifest.json` (same sha256), keeps the
same control id/clause/expect but replaces the write:

```json
{"writes": [
   {"op": "py",
    "code": "p='corpus/SOURCES.md'\nlines=read(p).decode().splitlines(keepends=True)\ndup='| S189 | contradicting duplicate — https://example.invalid/S189-dupe | code | A | scope | anchor | teaches | mined | 2026-10-25 | 90d | corpus/knowledge/event-delivery-limits-r26.md, corpus/knowledge/event-queue-observability-r37.md |\\n'\nfor i in range(len(lines)-1,-1,-1):\n    if lines[i].startswith('| S217 |'):\n        lines[i+1:i+1]=[dup]\n        break\nwrite(p, ''.join(lines))"}
 ]}
```

- op `py` (check-r38-discrimination.py:102-103) runs in the confined env
  (`write`/`read` helpers; lines 59-69).
- It reads the file, reverse-scans for the line starting `| S217 |` (the last real
  Registry row), and splices the duplicate **immediately after it** — inside `## Registry`
  (SOURCES.md @base: `## Registry` line 9, `| S217 |` line 219, `## Paths` line 225).
- Now `registry_rows()` sees two S189 rows → `j=0` (and `c=0`) → `TARGET_MISSED` as
  expected → all 19 controls agree → `correct=19/19 verdict=TARGET_MET`, exit 0.
- Secondary change (counter side): `859d0cf` ("round-38 c1 v3 repair: clause c enforces
  unique registry rows per id") tightened clause `c` from `any(...)` to
  `len(rows.get(i, [])) == 1 and (lambda r: …)` (current file lines 201-207), so
  uniqueness is enforced in two clauses. For this control it is not the deciding change
  (the frozen counter already rejects the in-Registry dup via `j`).

## 6. Confidence

High. Every pointer above was taken from committed bytes (`git show`) or from the round's
own replayed evidence; the red-before receipt `c1-redbefore.txt` (18/19, only duprow
failing) matches the cross-pairing matrix exactly. The round-39 re-registration target
(freeze-commit 19/19) is the same pair as row 4 of the matrix with the re-frozen manifest
at the freeze commit.

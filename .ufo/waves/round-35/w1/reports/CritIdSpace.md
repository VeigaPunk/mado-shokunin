# CritIdSpace — attack on the round-35 id assignment

Seat: critic (leaf; no dispatch). Date: 2026-10-24. Scope: whether assigning lane ids
S203–S210 to the eight adopted rows while recording the package's own ids in the lesson
is legal under CORPUS.md's registry contract, and whether S197–S200 may ever be
allocated.

## Contract under test

`/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md, frozen v1:

- `id` — "`S` + 3 or more digits, **the next unused; never reused**."
- Rule 2 — "**Append-only.** Only `status`, `recheck` and `used-by` change in place …
  A correction is a new row."
- Rule 1 — "**A row is a claim.** Write it only after opening the source in the round
  that writes the row."

## Measured state (re-run at write time)

Lane registry (`mado-shokunin/corpus/SOURCES.md`):

- 192 rows — `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | wc -l` → 192
- Id set: S001–S189 contiguous, then **S196, S201, S202**. Gaps: **S190–S195, S197–S200**.
- `grep -nE 'S(19[0-9]|200)[^0-9]' corpus/SOURCES.md` → only S196/S201/S202 rows.
- `git log --all -G 'S19[0-9]' -- corpus/SOURCES.md` → only the commits that wrote
  S196/S189-area rows; no commit ever carried an S190–S195 or S197–S200 row.
  These ids were **never allocated** in this lane.

Staged package (`shokuknow/merge/mado/SOURCES.append.md`):

- **Mutated mid-flight.** At this seat's first read (early in the wave) the block
  numbered the same documents S197–S336. `stat` now: mtime `2026-10-24 23:26:50`,
  first id **S203**, block S203–S342. `MERGE-REPORT.md` (same mtime) states: "lane
  registry currently holds **192** rows; first staged id is **S203**" — the campaign
  renumbered the package to start at the lane's tail and appended a dedup table
  (package S203→S186, S204→S187, S205→S188, S206→S189, S207→S201, S208→S202, S213→S196).
- The eight adopted documents' **current** package ids (grep of the committed file):
  omarchy-first-run **S315**, journal no-toggle evidence **S316**, idle-lock chain
  **S327**, waybar config **S335**, indicator script **S336**, omarchy menu **S337**,
  dated backups **S340**, toggle-state dir **S342**.
- The frozen registration (§4) records the **old** map: S309, S310, S321, S329, S330,
  S331, S334, S336. That map is stale against today's file — and worst case, **S336
  exists in both schemes denoting different documents** (old: toggle-state dir; new:
  indicator script). The campaign itself reused an id across its renumbering.

## Verdicts

### 1. Assigning lane S203–S210 — **legal, conformant under the established reading**

- Append-only: satisfied — eight new rows appended; no existing cell touched.
- Never-reused: satisfied — S203–S210 have never existed in the lane (id set ends at
  S202; confirmed above).
- "Next unused": ambiguous in the frozen text — it can mean (a) next above the tip or
  (b) smallest unused. Under (b) the round should have taken S190–S195/S197–S200 first.
  Reading (b) is not the operative one: the lane's own history already skips gaps
  (S196 followed S189 leaving S190–S195; S201–S202 followed), and no census check
  (`CORPUS.md` census block, `scripts/sources-census.sh`) tests contiguity or
  monotonicity — only duplicates and well-formedness. The tail reading is the standing
  convention; under it S203 is exactly "the next unused".

### 2. Recording the package ids in the lesson — legal and **required**, but the frozen
   map is stale

Package ids live outside the registry; the never-reuse rule binds only the registry's
`id` column. Recording the map is provenance, not allocation, and there is precedent:
`LOG.md:1973` (round 34) — "restated the literature reject against the opened file's
own ids (S206, S209, S210, S211), not S199." **Defect found:** the recorded map
{S309…S336} describes the pre-23:26 file. If the lesson copies the registration's set
verbatim it will cite package ids that no longer exist — and where S336 survives it
denotes a different document. The lesson must record the map **against the committed
append file at adoption time**, keyed by the file's sha256, or state that the package's
id space is unstable. Filed package-side already as L0 `ae2c52b8` per registration §4.

### 3. The real hazard — same-id/different-doc ambiguity, not illegality

After this round, lane S203–S210 will denote the idle-lock documents while package
S203–S210 denote the IPC/Waybar documents (lane S186–S189, S201–S202 equivalents). Any
future verbatim append of the staged rows (checklist step 3 in `MERGE-REPORT.md` says
"Append `SOURCES.append.md` to `corpus/SOURCES.md`") would land duplicate ids and trip
the census duplicate check; any audit that merges the two namespaces reads a collision.
The lesson map mitigates this **only if it is correct** — see verdict 2. The round's
choice is defensible because lane-tail continuity beats package-parity once the
package itself renumbers (proof: today's +6 shift); but it must be *declared* in the
lesson as "lane ids and package ids diverge by design", not left implicit.

### 4. May S197–S200 ever be allocated? — Contractually yes; operationally never.

- Legal: they were never used in this registry (git history clean), so allocating them
  is not reuse. Nothing in the frozen text forbids backfill.
- Should not happen: (a) it breaks the id⇄time order every reader and the round-34
  id-collision guard implicitly rely on; (b) under the package's **old** numbering,
  S197–S200 denoted documents that are now lane S186–S189 — a backfilled lane S197 for
  any other document would collide with package-history S197 = the IPC page, poisoning
  cross-registry reconciliation exactly as verdict 3 describes; (c) the same holds for
  S190–S195. Disposition: treat both gaps as **permanently skipped, unallocated**. If a
  future round ever backfills, the lesson must state that the id never existed in the
  lane and name the package document that once carried the number.

## What the attack does NOT show

- No append-only violation: no existing row is modified.
- No never-reuse violation: all eight lane ids are new.
- No duplicate row: `RevDedup` owns within-registry URL/id duplication; the new ids do
  not collide inside the lane.
- The task's premise "the staged package starts at S197" was true when the registration
  was written (this seat observed S197 as the first staged id earlier today) and is
  false now — the package renumbered to S203. The drift is itself the finding: the
  package's ids are mutable labels, so the lane must treat them as provenance strings,
  never as keys.

## Bottom line

The assignment is **legal** under CORPUS.md: append-only holds, never-reuse holds, and
S203–S210 is the next-unused tail under the lane's established convention. The
defensible attack is narrower and still live: **the lesson's recorded package-id map is
stale by one mid-flight renumbering** and, if copied verbatim from the frozen
registration, will mis-cite every adopted document — including an S336 that now names
a different file. Fix at write time: re-derive the map from the current
`SOURCES.append.md` ({S315, S316, S327, S335, S336, S337, S340, S342}), record the
file's sha256, and declare the divergence. S197–S200 stay unallocated forever.

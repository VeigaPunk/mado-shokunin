# ScribeLesson — round-35 lesson `## Gate` draft

Seat: ScribeLesson. Scope: draft the round-35 lesson's `## Gate` section —
candidates, admitted (3 entries + 8 rows with URL/path, access date, located
quote), refused with reason + flip (the twelve register-slice rows and the
merge-package rows not adopted). Draft only, scratch only.

**Draft**: `.ufo/waves/round-35/scratch/ScribeLesson/draft.md` (~230 lines,
r34-lesson format). No lane file touched; `/home/vgpnk/Projects/shokuknow`
read-only throughout.

## What the draft asserts, and where each fact came from

### Admitted (re-derived, not copied)

- **3 entries / 8 rows, lane ids S203–S210.** Row fields from
  `controls/golden/corpus/SOURCES.md` + `ScribeRows`/`ExecAppendBlock` reports;
  cites from the golden entry `source:`/`gate-quote:` lines.
- **Located quotes**: verbatim `gate-quote:` remainders from the golden
  entries, confirmed contiguous substrings of committed receipts by
  `ExecQuoteLint` (8/8 PASS, 13–17 words each). Receipt sha256 prefixes quoted
  from `ExecQuoteLint`'s integrity table.
- **Access date** 2026-10-24 for all eight: receipt headers ("host re-open
  2026-10-24") and row `opened` cells agree.
- S203–S210 are the lane's own ids; the registry continues S202 → S203
  contiguously. S190–S195 / S197–S200 unallocated, disposition per
  `CritIdSpace` (free but permanently skipped — I corrected my first wording,
  which wrongly blamed never-reuse).

### The id remap — three spaces, measured

- Package `source:` headers in its three knowledge files cite **pre-remap**
  staging ids {S309, S310, S321, S329, S330, S331, S334, S336} — the set the
  frozen registration records.
- `SOURCES.append.md` was **renumbered mid-wave** (`CritIdSpace` observed it
  live; file mtime 2026-10-24 23:30, sha256
  `684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0`). Same
  documents now sit at {S315, S316, S327, S335, S336, S337, S340, S342} —
  verified by me against rows 119–146 of the current file, agreeing with
  `ScribeRows` and `ExecAppendBlock`.
- The trap: stale S336 (toggle-state sweep) vs current S336 (idle.sh) name
  different documents. Draft carries a lane-id ↔ current-package-id ↔
  stale-`source:`-id table for campaign reconciliation (L0 `ae2c52b8`).
- Register ids are pre-remap proposal ids scoped per round (`ID-REMAP.md`):
  the draft maps each register row to the document's **current** append id —
  r2 S195→S212, r2 S199→S216, r2 S200→S217, r2 S201→{S218,S280,S325},
  r3 S205→S222, r4 S224→S241, r5 S228→S245.

### Register slice — twelve of thirteen

`ScoutQuar` counted 13 mado rows (6 `payload-absent`, 7 never-checked). The
draft refuses 12 and exempts register `S189` exactly as the round-34 lesson
did: r34's quarantine hand-check found its quoted span at line 128 of the
pinned `EventManager.cpp` — a false negative, IN-REGISTRY-SAME-ID. Refusal
reasons/flips restate r34's wording verbatim where the grounds are unchanged
(province, id-space, transient host file, unreachable, no-locator).

### Package rows not adopted — arithmetic verified

147 staged rows (S203–S349 contiguous, current file) = 8 adopted by document +
6 refused (staged copies of register-refused documents: S212, S218, S280,
S325, S222, S241) + 1 held (`S220`, campaign-forced `queued`, cites a staged
entry no entry cites) + 132 out-of-scope. Each group carries reason + flip;
the 132 get a package-wide flip (re-open in-round, normalise per the frozen
schema, resolve the S203–S210 numeric collision, duplicate-URL rule for the 8
rows duplicating held documents).

## Judgments made (state at claim)

- `unreachable`/`unverifiable` refused rather than adopted: the lane did not
  open those locators; refusal grounds don't require fetching (r34 precedent).
  Marked as such in the draft's closing paragraph — the seat claims no
  re-fetch authority.
- `S199`/`S200`'s staged rows are now reachable via a declared reader proxy;
  draft records this but keeps the refusal — tier-C community locators this
  lane didn't open.
- The 132 unadopted rows are grouped, not itemised: enumerating 132 urls adds
  no gate information; the refusal is scope, identical for all, and the flip
  names the per-row requirements. Ranges are explicit and disjoint — every
  staged id is accounted for.

## Open items for the publisher

- `CritQuar`'s report (attack on the refusal reasoning) had not landed at
  write time — its log shows `Working...`. If it flips any row's verdict, the
  register-slice bullet needs amending before the lesson lands.
- `opened` wording: rows are host re-opens dated 2026-10-24; if the append
  commits on a later date, that is still the correct access date.
- The registration's recorded package-id set is stale (pre-remap); draft
  records both spaces so the campaign can reconcile — flagged, not "fixed".

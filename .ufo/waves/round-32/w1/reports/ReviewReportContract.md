# ReviewReportContract — pre-attack of the mado round-32 report contract

Seat: ReviewReportContract (w1, leaf — no dispatch). Target: the report the L1 writes at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-32/mado.md`.
Contract sources re-opened: dispatched prompt `.ufo/prompts/mado-round-32.md` §4 (report
contract) + §6 items 2/4/5/6/10; `templates/round-prompt.md` (same §4, canonical spelling);
`PROTOCOL.md` report-of/minimum-content clauses; `scripts/shokunin-watchdog.sh`
`report_of()` + `report_sources_conformance()` + `MIN_REPORT_BYTES`; r31 non-author
spot-check `corpus/lessons/round-31-verifier-spotcheck.md` defect list; the six admitted
sibling r32 reports (`kaidoku`, `mori`, `kake`, `tameshi`, `chousa`, `tsukuroi`) for
closure-accepted spelling precedent.

## What actually fails the marker check

`report_of()` (watchdog:144–164) is the only mechanical gate. A file at the report path
passes iff ALL of:

1. `grep -E "^#+[[:space:]]*SHONEN([^[:alnum:]_]|$)|^[[:space:]]*-[[:space:]]+\*\*SHONEN\*\*([[:space:]]|$)"`
   matches (case-insensitive, also accepts `SHŌNEN`/`shōnen`). So `## SHONEN` or
   `- **SHONEN**:` qualifies; a `SHONEN` mention inside prose does NOT.
2. `wc -c` ≥ `MIN_REPORT_BYTES` = **400** (watchdog:54).
3. File digest differs from the launch baseline — a new file passes trivially
   (`.ufo/reports/round-32/mado.md` does not exist yet).

Then the prompt §4 **Marker rule** (integrator judgment, not grep): a contentless report —
placeholder text, missing required sections *other than* Sources & frontier and Trend
verdicts, or no evidence pointers — counts as round **failed** and the driver relaunches.
Missing Sources & frontier is only a `sources-conformance-defect` log line
(watchdog:311–315 greps `^#{1,6}[[:space:]]+Sources[[:space:]]*&[[:space:]]*frontier`,
case-insensitive — `## Sources & frontier` matches; `## Sources` or `## Frontier` alone
does NOT). Missing Trend verdicts / Landed changes / Before→after headings have no grep at
all — they fail at closure step-1 as minimum-content defects (r31 D2 precedent; the r21
closure conformance line checks all six headings by name).

## CHECKLIST — exact section order and spellings

Canonical spellings (template + all six admitted sibling r32 reports; the seat task's
`Before -> after` is the ASCII rendering of `Before → after measurements` — write the
`→` form, precedent carries it):

```markdown
# mado — round 32 report (attempt 1, L1 <name>)

Lane tip at write: <FULL pushed hash from `jj-lane.sh state` local= / `git rev-parse
master` — at review time master was `50e6a8f3…` and moving; cite the value at write time>.
Base: `256222890d935212874a09751ff9b7869943c2d7` (frozen in registration.md:3). Pre-round
HEAD `9186234` (the post-closure r31 spot-check commit sits on top — same dual-base
disclosure as r31; name both, never silently pick one).

## Work performed
<open line: "Registration .ufo/waves/round-32/registration.md frozen <hash>; two claims:
C1 coverage (Hyprland IPC two-socket + dispatcher surface, frontier→core, rests on
S186/S187/S188/S189/S196 opened this round) and C2 calibration (stale published axis
table vs. re-derived counters). Axis naming: C2 is CALIBRATION — the r31 spot-check D5
flagged registration/report drift; use `calibration` in every surface.">
<one bullet per work item, each ending in an evidence pointer — path:line, verbatim
command output line, or commit hash>

## Landed changes
<one bullet per landed change: path — name of LOG.md entry — commit hash. Every change
named here must appear in the LOG.md `## Round 32` entry and vice versa. Only cite
`landed <hash>` lines the jj-lane.sh helper printed; `rewritten` lines are diagnostic.
Expected set: registration.md freeze; the three knowledge entries; corpus/SOURCES.md
rows S186–S196; corpus/README.md coverage-map rows for the 3 new entries (indexed
denominator 43→46); corpus/lessons/round-32.md; SCORECARD.md append (round-32 axis table
= C2's fix + per-claim rows); quality/check-axis-scores.py (NEW committed tool — was
untracked at review time); evidence receipts under .ufo/waves/round-32/; LOG.md itself;
wave spec/registry committed as wave evidence.>

## Before → after measurements
| Claim | Before (<base>) | After (<tip>) | Counting command |
C1: `cd mado-shokunin && A=corpus/knowledge/ipc-contract-r25.md
B=corpus/knowledge/dispatcher-semantics-r25.md
C=corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md; e=…` (verbatim frozen
counter from registration.md:44-55) — base `entries=0 rows=0 cited_entries=0` → tip
`entries=3 rows=5 cited_entries=3` TARGET; plus committed K1 do-nothing control receipts
`.ufo/waves/round-32/c1/controls/` (rows-only → entries=0; entries-only → rows=0).
C2: `python3 -I quality/check-axis-scores.py --rev <rev> --repo .` →
`MADO_AXIS: checked=3 mismatched=1` at base (stale 39/40 + 9/9) → `mismatched=0` at tip;
K2 controls `(a) stale text still mismatched≥1, (b) re-derived values mismatched=0,
(c) perturbed fraction mismatched=1` — receipts `.ufo/waves/round-32/c2/controls/`.
State the measured revision hash beside each number; the gate prints which axes it
checked (sourced-art NOT re-derivable — say so; no universal clause).

## Sources & frontier
- census before → after: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
  validate --root /home/vgpnk/Projects/shokunin mado` — paste BOTH outputs + exit codes;
  before-state must be reproducible over committed base bytes (name the revision it was
  measured against), round-end run MUST be exit 0 (warnings allowed; name any W04s).
- rows before→after: 185 → 190 expected (S186, S187, S188, S189, S196), each with its
  tier cell, `status=mined`, `used-by` = exactly the admitted entries, `recheck` = ISO
  date/NNd/cadence (no prose cells).
- rows touched old→new: name any status/recheck/used-by flips or `none`.
- frontier rows advanced: corpus/README.md `## Frontier` (`dispatcher behavior`,
  IPC/socket ground) — which frontier bullet each new entry retires or narrows.
- `Assimilation:` line — this round ASSIMILATES (source `/home/vgpnk/Projects/shokuknow/
  merge/mado/`); do NOT write `Assimilation: none`. Paste: both id lists
  (`assimilation/reg-ids`, `assimilation/staged-ids`), the collision count and renumber
  map (item-10 requires these verbatim in the report); quarantine verdicts per mado
  slice row (`assimilation/quarantine-slice` — absent→refuse/fabrication-class,
  prose-class→unverifiable; the register file itself untouched); considerthese
  disposition — at most ONE proposal from the frozen `considerthese/2026-10-23.md`
  (note: `considerthese/2026-10-24.md` exists NOW — the frozen claim names 2026-10-23;
  name the choice explicitly so the reviewer does not flag stale-latest).
- lesson pointer: `corpus/lessons/round-32.md` `## Gate` (≥1 admit + ≥1 reject with
  reason + flip, own 2026-10-24 access dates + ≤25-word located quotes — NOT the
  campaign's `opened` dates) and `## Mistakes` (or the none-found sweep pasted).
- cross-domain evidence encountered, with the owning domain (PROTOCOL minimum content).

## Trend verdicts
- expansion: <verdict> — <evidence, e.g. 3 entries + 5 registry rows on uncovered
  coverage-map ground; expected `improved` iff C1 lands>
- quality: <verdict> — <evidence, e.g. both frozen counters green with red-at-base
  controls, K1/K2 receipts committed>
- discernment: <verdict> — <evidence: this round's Gate admits/rejects + quarantine
  verdicts are the sample the closure spot-checks; verdict is asserted, the outside
  check lands post-report>
Verdict ∈ {improved, harmed, unchanged, unprovable-but-better}; evidence is required,
the verdict cell is a word, not a scalar.

## SHONEN
<one line per box — exactly 4 lines, mirroring SHONEN.md boxes verbatim>
- [~] SKILL.md contains real decision tables … — asserted: <pointer, e.g.
  `git diff <base> <tip> -- SKILL.md` empty or the specific change>
- [~] At least one end-to-end domain task … — asserted: LOG.md `## Round 32` entry +
  committed receipts>
- [~] Instructions executable by an agent without oral context — asserted: counters +
  census re-runnable from committed bytes at named revisions>
- [~] No cross-domain bleed (PROVINCE.md still accurate) — asserted:
  `git diff <base> <tip> -- PROVINCE.md` empty + shokuknow/considerthese/merge/mado all
  read-only (fetch + grep + comm only, zero writes) + misroot sweep result>
No `[x]`: no non-author verifier exists in-round (see Unsatisfiable #1). State that
line — r31's report did and the spot-check accepted it as correct.
```

Then the extras (no heading required; siblings put them after SHONEN):

- `Stale-lane: respawn-per-round driver; no other mission of this lane is open.` —
  accepted sibling wording (mori:132, chousa:143 verbatim).
- `Tool installs: none` or each tool + version + channel + reason (addendum §7).
- `## Round shape, seats` (or folded lines): one v1 wave, 32 seats, band 32–64, policy
  `ufo-wave-policy.json`; role mix scout 7/executor 5/scribe 4/reviewer 6/critic 4/
  connector 2/revenger 1/sentinel 1/mutation-tester 1/simplifier 1 — 13/32 (40.6%)
  attack; `planner` held by the L1 (validator rejects the role — record the mapping);
  dead seats with last error text, each refusal verbatim; no model literals — record a
  seat's actual answering model only when a claim depends on it; round total.
- Harm watch: `git diff <base> <tip> -- tools/ SKILL.md PROVINCE.md corpus/knowledge`
  scope lines; `MADO_SELFTEST` result if mado-verify.sh ran; misroot sweep:
  `git -C /home/vgpnk/Projects/shokunin status --porcelain` — copy any mado-rooted
  fleet-root file byte-exact into the lane, `cmp` verify, delete the fleet copy, record
  under `## Mistakes`; never touch other lanes' files or `.ufo/state/*`.
- Causal separability line (§2.3): C1 reads knowledge/SOURCES/README only; C2 reads
  SCORECARD + the three committed instruments; reverting either claim leaves the other's
  receipts byte-identical — state it with the diff command.
- Inherited state (addendum item 5): the 4 modified + 2 untracked
  `.ufo/waves/round-30/w1/reports/*` seat artifacts are orchestrator-dispatched,
  predating this round — name them, leave uncommitted, never edit
  `round-*-verifier-spotcheck.md` files.
- Open L0 questions: mado r21 (third-rejection disposition), r22 (rejection hold), r23
  (H2 ruling), r28 (heldout input retention) — name them as open, no new append unless
  this round raised one (appends go through `fleet-commit.sh` separately).
- Residual cheats routed forward (r31 D6 carried): n2 relevance-free resolution;
  `outside`-only grounding criteria 19/22/23/26/28; Holds ≥5-word proxy; r24 `S###.bin`
  glob convention.

## Evidence-pointer inventory (what must resolve at write time)

| Pointer | Form | Source |
|---|---|---|
| frozen registration | commit hash (was untracked at review time — must land via jj-lane.sh before the report cites it) | `.ufo/waves/round-32/registration.md` |
| C1 counter triple | verbatim `entries=3 rows=5 cited_entries=3` output + measured rev | frozen command registration.md:44-55 |
| C1 K1 controls | committed receipt paths | `.ufo/waves/round-32/c1/controls/` |
| C2 counter pair | `MADO_AXIS: checked=N mismatched=M` at base AND tip revs | `quality/check-axis-scores.py` (commit it — untracked at review time) |
| C2 K2 controls | committed receipt paths | `.ufo/waves/round-32/c2/controls/` |
| census before/after | pasted output + exit code + measured rev | `sources-census.sh validate --root … mado` |
| fetch receipts | committed `.bin` per opened source | `.ufo/waves/round-32/fetch/S{186,187,188,189,196}.bin` exist |
| assimilation guard proofs | committed files incl. nonempty `collisions` on the indented-row fixture | `.ufo/waves/round-32/assimilation/guard-proof-*` exist |
| quarantine slice + verdicts | committed file + per-row verdict in lesson Gate | `assimilation/quarantine-slice` (0 B at review time — verify whether empty-slice or extraction bug; state which) |
| LOG.md entry | `## Round 32` committed before report | `LOG.md` |
| lane tip / landed hashes | `jj-lane.sh` `landed <hash>` lines only; tip = `local=` at write time | helper output |
| wave evidence | `w1-spec.json`, `w1-taskcall.json`, `seat-plan.tsv`, `exit-codes.tsv`, `swarm-registry.json` committed | `.ufo/waves/round-32/` |
| fleet report commit | `fleet-commit.sh --as mado` output, authored `mado-shokunin <mado@shokunin.local>` | run AFTER writing the report, never leave uncommitted (r31 D3) |

## Requirements the round cannot satisfy — flags

1. **`[x]` SHONEN marks — unsatisfiable by construction.** `[x]` requires a NAMED
   non-author verifier; a seat this lane dispatched "is still the lane" (PROTOCOL).
   The w1 reviewer seats cannot supply it, and the real non-author check (hyaku
   closure) runs after the report is filed. Maximum satisfiable: 4×`[~]` each with a
   resolvable pointer — same posture as r31, which the spot-check accepted as correct.
2. **`unprovable-but-better` verdicts — cannot be self-certified.** Same non-author
   rule; neither C1 nor C2 is exploratory (both measured), so this only binds if the
   lane adds an exploratory claim — it should not (cap is 3, frozen at 2).
3. **Wave band 32–64 — frozen at dispatch, cannot be repaired in-report.** 32 seats are
   in `seat-plan.tsv`; if any failed to spawn or dies, the seat is dead in the evidence
   (never replaced, never padded) and the report must disclose the refusal/death text.
   A spawn refusal making the wave <32 is an honest band breach, reportable, not fixable.
4. **`sourced-art` axis freshness — structurally unverifiable.** No committed instrument
   re-derives it; the C2 gate correctly excludes it (`checked` prints which axes ran).
   The report must say which axes were checked — claiming whole-table freshness is an
   unprovable universal clause.
5. **Attempt-1 inheritance duty — latent.** Zero `lane-dead-no-report mado round=32`
   lines in `.ufo/watchdog.log` (launch 19:56:38-03:00, pgid 1636979); the
   `.ufo/waves/round-32/` tree is THIS attempt's work (all mtimes post-launch). No
   dead-attempt artifacts exist to inherit — the report just says `attempt 1`.
6. **Census `before` output — must be reconstructible from committed bytes.** If the
   round-start census ran against the live tree, the before-receipt must still be
   re-derivable at the named base rev (`--file` mode on `git show <base>:corpus/
   SOURCES.md` or a scratch clone) — a before-number from memory is unverifiable.
   ExecCensusManual is the seat covering this; check its report before writing.
7. **`considerthese` latest-file ambiguity.** Frozen claim names `2026-10-23.md`; a
   `2026-10-24.md` now exists. Follow the frozen claim and NAME the newer file's
   existence — silently mining 2026-10-24 widens a frozen claim; silently ignoring it
   invites a stale-latest defect.

## Traps from the r31 spot-check (each maps to a checklist line)

- D1 missing `corpus/lessons/round-31.md` → land `round-32.md` WITH `## Gate` +
  `## Mistakes`; cite it in Landed changes and Sources & frontier.
- D2 missing headings → the six `##` headings above, in order; `Stale-lane:` line;
  explicit `## Landed changes` even though commits are cited inline elsewhere.
- D3 attribution → L1 commits the report itself via `fleet-commit.sh --as mado` BEFORE
  yielding; an uncommitted report file is the exact r31 defect.
- D5 axis-label drift → `calibration` in registration, SCORECARD, counters and report.
- D7 inherited leftovers → name the r30-w1 seat files as orchestrator-owned; never
  commit or edit them.
- Digest/baseline: the report file must be created fresh — the driver recorded a
  same-round launch baseline; unchanged-or-absent bytes never complete the round.

## Report-adjacent contract items (not headings, still checked at closure)

- Report committed AFTER all lane commits and citing the pushed lane hash — commit
  order is `jj-lane.sh` lane commits → report write → `fleet-commit.sh --as mado -m
  "round-32: mado report" -- .ufo/reports/round-32/mado.md`; the report lands last.
- Every cited hash must exist and be an ancestor of lane `master` (or fleet `master`
  for the report commit) — closure runs `merge-base --is-ancestor` per hash.
- Push scope: fleet remote + own lane remote only; shokuknow/considerthese read-only.
- L1 return summary ≤12 lines (claims+verdicts, lane HEAD, report commit, round shape,
  wave sizes/role mix, round total, dead seats, open L0) — separate from the report.

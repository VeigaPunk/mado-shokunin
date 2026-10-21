# ConnProvince — no contested ownership; one unowned fleet-wide scope and one open L0 disposition to report

Seat `MadoR22.ConnProvince` (connector, leaf). Machine-readable form:
`.ufo/waves/round-22/w1/notes/ConnProvince.json`. Scan at 2026-10-21T14:28:45Z. Lane HEAD
moved from `a963ce6` to `eda932e` ("wip: mid-round checkpoint") during the scan; I did not touch it.

I wrote only these two files. I edited no production, PROVINCE, SKILL, fleet or sibling file. I ran
no detector, scanner, gate, harness or payload, and probed no live session, compositor, package,
service or network. No git/jj writes. No tools installed.

## Outcome

- **Contested ownership: none.** No sibling `PROVINCE.md` claims post-hoc classification of
  seat-issued commands, or an evidence-tier/count audit of mado receipts. The integrator admitted
  the tripwire as a mado capability (MANIFEST `rounds[359]` r17, `rounds[362]` r18).
- **Today the lane-local audit is not a fleet gate.** No fleet prompt, script,
  PROTOCOL/APPENDIX/MISSION/AXES, root SCORECARD or sibling repo references `mado-tripwire`,
  `mado-assessment` or `mado-evidence-audit`. Only MANIFEST closure/capability notes do.
- **Unowned, unfenced scope (CP-U1), to report to the integrator.** Round 20 ran the mado
  tripwire across the whole fleet's session root. Its committed receipts carry per-seat verdict
  rows naming sibling-lane and closure seats, and those receipts sit inside the 1356-fixture corpus
  that r22 C1 reuses as its no-harm comparator.
- **Open disposition the lane does not own (CP-L0).** The r21 L0 hold/unblock question has no
  recorded ruling. The r22 "operator authorized" sentence appears only in the lane's own LOG.

## Axes

| Axis | Role here | Effect of the proposed move |
|---|---|---|
| adjacency | primary: the boundary of the C1/C2 plane | improved; documentary, not a measured score |
| calibration | verdict words must match the evidence type | protected; no criterion-count credit |
| operability | guard | unchanged; no C1 or comparator byte changes |
| coverage, freshness, depth | — | unchanged |

**This move raises no measured score.** Reporting it as an axis gain would hide a contradiction
inside a number.

## Evidence

### Province text actually declared

- `PROVINCE.md` has 20 lines (sha `1b25bb1e…`, last changed `61eaa07`, r19). It declares the
  desktop configuration plane and the r19 theme route. `rg -n -i 'transcript|tripwire|session'
  PROVINCE.md MINT.md SHONEN.md` returns rc=1.
- Every C1/C2 claim from r17 to r22 sits on the transcript-tripwire/assessment plane
  (`SKILL.md:606,609,621`; r22 registration).

### Sibling readers of transcript surfaces (each asks a different question)

| Sibling | What it reads, and for what | Anchor |
|---|---|---|
| kagi | Transcript-leak gate over the opencode DB | kagi `PROVINCE.md:33,48` |
| mori | Passive terminal-at-scan status tallies; FR14 telemetry is consume-only | mori `PROVINCE.md:103-106`, `:57` |
| kumitate | OMP harness contract (Frontier) | kumitate `PROVINCE.md:19` |
| kengaku | Benchmark `finish=tool_calls` | kengaku `PROVINCE.md:37` |

Shared evidence is not shared ownership (tsukuroi `PROVINCE.md:41-42`).

### Fleet text that already fences gate verdicts

- `PROTOCOL.md:407-411`: "A verdict is lane-local evidence … never stands in for the native judge."
- `:412-417`: the integrator verifies committed evidence and does not run a sibling's gate.
- `:61-68`: only a named non-author may write `[x]`.
- `:380`: exit 0 maps to the fleet-wide `clean`.

### C2 inputs stay inside the lane

- `round-18/frozen/provenance.json`: all five frozen inputs come from MadoR13, MadoR14 and MadoR15
  seat transcripts.
- The r21 corpus snapshot's inclusion rule reads "Committed lane transcript fixture corpus only;
  this is NOT a private live-session corpus". All 1356 paths are under mado `.ufo/waves`; 0
  manifest rows and 0 `corpus-comparison.json` strings name a sibling seat.

## Findings

### CP-U1 — fleet-wide application of the mado tripwire (unowned, unfenced)

- `round-20/gen_w2.py:13` sets `SESS = '/home/vgpnk/.omp/agent/sessions/-Projects-shokunin'`,
  which is the fleet-wide root. `w2/reports/CorpusRuntime.md:80` records "5,878 stable files × 2
  tools = 11,756 runs, 12 workers".
- `full-sweep.jsonl` (sha `c78a9de3…`), counted by seat-name prefix:

  | Prefix | Run rows | Run rows with `nfindings>0` |
  |---|---|---|
  | Mado | 1600 | 302 |
  | Tabi | 1334 | 332 |
  | Kaidoku | 1330 | 322 |
  | Tameshi | 1312 | 491 |
  | Kama | 1108 | 328 |
  | Tsukuroi | 1082 | 133 |
  | Souji | 1036 | 163 |
  | Mori | 660 | 108 |

  The receipt also covers fleet and closure seats such as CloseKama and CloseTameshi. These are
  run rows across two tool versions. They are "issued", not "executed", classifications (tripwire
  docstring), not incidents or distinct files.
- The round-21 corpus manifest includes `round-20/w2/CorpusRuntime/{full-sweep,runs,serial-runs}.jsonl`
  among the 1356 fixtures that C1's no-harm comparator reuses.

**Owner status.** Mado's PROVINCE does not declare this scope, and no sibling claims it. The
nearest declared neighbours are:

- mori: fleet observability; under FR14, emission belongs to the emitting lanes and orchestration.
- kumitate: dispatch and orchestration.
- the operator.

Under `PROTOCOL.md:457-461` this goes to the integrator. Silence must not default it to mado just
because mado wrote first.

**r22 exposure.** Bounded. The registration bars a private-session census, so these receipts enter
r22 only as inert bytes. The risk is wording: any r22 output that cites their rows as findings
about a sibling seat or a closure seat turns a lane-local classifier into a fleet conduct verdict.

### CP-L0 — the hold/unblock ruling is not recorded

- MANIFEST `rounds[400]` (r21) says the lane is blocked and the open L0 question "awaits operator
  hold/unblock".
- Fleet `.ufo/l0-questions.md:78` holds the mado round-21 question with no RESOLVED line. Compare
  tabi's RESOLVED-BY-RULING row.
- Dispatch is observed: `.ufo/watchdog.log:602` records `2026-10-21T11:14:32-03:00 launch mado
  round=22 … attempt=1`, and the prompt landed in commit `0820349` at 11:14:30. That prompt does
  not mention the block.
- The lane's `LOG.md` r22 entry says "Operator authorized attempt1 after the three-rejection
  block" and gives no pointer.

**Consequence.** No r22 artifact may be cited as the unblock ruling or as closure of the L0 row.
That includes a C2 exit 0.

### CP-1 — undeclared work surface (documentation, not absorbed ground)

**Contradiction, left for L1 to rule.**

- `round-20/w1/reports/ScribeProvince.md:7` ruled "no PROVINCE line must change", because the
  tripwire is lane tooling.
- Against that: `PROTOCOL.md:430` says PROVINCE names the lane's work surfaces; SHONEN box 4
  requires "PROVINCE.md still accurate"; `MINT.md` names a desktop-config boundary only.

Both readings are lane-authored, and neither is an outside ruling. The r18
`ConnProvinceScope.md` precedent classifies this as "undeclared surface", resolved by an appended
paragraph rather than a transfer.

### CP-2 — the registry row is missing the lane-local qualifier

- `SKILL.md:621` (`mado-assessment`) maps 0 to "clean" with no qualifier. The lane's probe rows
  say "not admission" (`SKILL.md:599-601,605,608`).
- The r22 contract's `authority` string ("artifact arithmetic and evidence labels only; not
  semantic correctness, authentication, admission or promotion") lives in a wave file. The registry
  home is `SKILL.md` (`PROTOCOL.md:398-401`).
- If `mado-evidence-audit` copies the r21 row shape, the gap repeats.

### CP-3 — keep the method claim lane-local (low)

C2's selftest, mutant kill and frozen fixtures use tameshi's method. Tameshi treats a pattern as
general only after evidence from two independent lanes (tameshi `PROVINCE.md:14-17`). The same
"recount versus retained receipt" shape is already fenced as own-evidence-only in two sibling
lanes:

- souji `PROVINCE.md:95-97`: "limited to souji's own receipt/certification fragments; it does not
  become fleet orchestration or an independent promotion authority".
- mori `PROVINCE.md:199-203`: "accounting agreement only … cannot authorize baseline acceptance,
  cleanup, reap, continuation or dispatch".

Mado should reuse that wording. It may route the three-lane observation to tameshi as evidence,
never as a claimed general method.

## Proposed move (one, bounded)

Land **one lane-local scope fence** at integration, after the seal. It changes no tool, contract,
expectation or comparator byte, and has three parts.

**(a) Registry qualifiers** for `mado-assessment` and the new `mado-evidence-audit` row:

- Verdict map: `0 clean = artifact assertions consistent with the snapshot (lane-local evidence;
  never admission, closure, promotion, L0 disposition, semantic truth or authorship)`.
- Read scope: `mado-owned committed frozen receipts and fixtures under this repo's .ufo/waves/*;
  never sibling-lane or fleet receipts, never live session transcripts`.

**(b) One appended `PROVINCE.md` paragraph.** Lines 1–20 stay unchanged, so tsukuroi's OUT-004
quote anchor survives.

```
**Round-22 boundary (own-seat command evidence; no new write surface, no sibling ground):** the
post-hoc tripwire and its frozen replay, assessment and evidence-audit tools read this lane's own
committed fixtures and receipts; `~/.omp/agent/sessions/**` is read only for this lane's own seat
transcripts when a round explicitly assigns it. A verdict is artifact agreement for this lane's
evidence only, not admission, closure, promotion, an L0 disposition, authentication or semantic
truth. Fleet-wide classification of other lanes' or closure seats' transcripts is not owned here;
the round-20 sweep receipts remain inert fixture bytes, never findings about a sibling. Fleet
conduct, dispatch and package state stay with their owners (mori, kumitate, tsukuroi, operator);
the reusable verification method stays tameshi's.
```

Landing it also needs one `LOG.md` entry (`AGENTS.md:3`) recording the new `wc -l` and sha256.

**(c) One report line** routing CP-U1 to the integrator (`PROTOCOL.md:457-461`) and CP-L0 to the
operator/L0 owner. The line claims no ruling.

**Why this harms nothing.**

- C2's baseline/changed/absent equality is untouched, because no tool or contract byte changes.
- The C1 comparator inputs are unchanged.
- The harness `expected.json` files are untouched.

## Risks

1. **Absorption creep.** The exclusion sentence carries the move. Without it, the paragraph reads
   as mado acquiring fleet-wide seat auditing.
2. **The r20 contradiction.** If L1 rules the plane out of province, the honest consequence is a
   box-4 cross-domain charge on the r17–r22 work, routed to the integrator, not silence.
3. **Blocked-lane optics.** A PROVINCE append in a recovery round can look like expansion. It
   declares only surfaces the lane has read since r17. If L1 prefers, land (a) and (c) only and
   keep CP-1 as a reported open defect.
4. **Provenance overreach.** Never state that the operator ruled on hold/unblock. Record only the
   observed dispatch evidence and the open L0 row.
5. **Count misuse.** The sweep counts are run rows of issued-command classifications. They are not
   incidents or conduct findings.

## Verification for Main (read-only; not run as gates here)

```
rg -n -i 'transcript|tripwire|session' mado-shokunin/PROVINCE.md      # rc=1 now
sha256sum mado-shokunin/PROVINCE.md; wc -l mado-shokunin/PROVINCE.md  # 1b25bb1e… / 20
git -C mado-shokunin diff --numstat -- PROVINCE.md                    # after landing: adds only
sed -n '621p' mado-shokunin/SKILL.md                                  # qualifier after landing
rg -n --no-ignore 'mado-tripwire|mado-assessment|mado-evidence-audit' --glob '!mado-shokunin/**' /home/vgpnk/Projects/shokunin   # MANIFEST.json only
sed -n '78p' .ufo/l0-questions.md; sed -n '602p' .ufo/watchdog.log
sha256sum tools/mado-tripwire.py tools/mado-assessment.py .ufo/waves/round-22/audit-contract.json   # unchanged by the move
```

## Unknowns

- Whether the operator issued an unblock ruling outside the fleet L0 channel. Only the lane's LOG
  asserts it.
- Which reading of CP-1 L1 adopts.
- Whether r20's fleet-wide sweep had an explicit operator or integrator grant. None was found in
  the files I read.

## Installs

None.

# mado — round 41 report (hyaku run 7)

> Skeleton draft by seat `ScrReportDraft` (w2). Every number below is filled from a committed
> receipt path unless marked `@@W2:<what>@@`, which is a placeholder for a wave-2 result that has
> not landed yet. Wave-2 findings (if any) are integrated by the L1; a finding on the DATA is a
> defect fixed before the round lands, a finding on a PREDICATE is reported as an open defect
> (no third registration after data).

Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, final lane hash
**`@@W2:final-lane-hash@@`** (`git ls-remote origin refs/heads/master` prints it). Round shape
(`registration-v2.md:13-14`, corrected from `registration.md:4`): **two v1 waves** — `w1` of 34
seats (build + first falsifiers, policy v1 band 32–64) and `w2` of 34 seats (falsify, dispatched
after the data commit), **round total 68**, no residual call. The §3 planner seat is held by the L1.
Dead seats: none reported by the dispatch; file-level check: 33 of 34 w1 report files on disk,
`ConnSiblingOverlap`'s artifact absent (see Work performed). The orchestrator's `w1-results.json`
carries no seat outputs (kernel restart mid-wave); reports are on disk.

## Work performed

Declared claims (`registration-v2.md:36-45`): **C1 operability (capability acquisition)** —
`tools/mado-globals.py`, target `fixtures=39/39 TARGET_MET` under `PRED-C1-r41-v2` (base `0/39
tool=absent`, `receipts/c1-v2-before-base.txt`); **C2 coverage (sourced)** —
`corpus/knowledge/hyprland-focus-grab-r41.md`, target `admitted=1/1` under `PRED-C2-r41-v2`
(base `0/1`, `receipts/c2-v2-before-base.txt`).

- Freeze v1 `60c3914154333180450d5da27ba222d5763cc56a` (registration, counters, controls, base
  receipts, source receipts); wave `w1` spec/dispatch `cd950ec781149040cc73d71cd67c2b67452e7724`
  (34 seats, `w1-spec.json` items length 34).
- **Wave w1 falsified the v1 predicates before any data**: `CritC1Cheat` scored 8 of 12 cheats
  `TARGET_MET`, `ExecC1ExtraMutants` left 13 of 42 mutants alive, `CritC2Cheat` admitted 9 of 9
  forgeries, `ExecC2ExtraMutants` left 29 survivors; `ExecDiffFuzz`, `ExecJournalFormat`,
  `RevRefTool`, `RevC1Counter` found further under-determined contract points
  (`corpus/lessons/round-41.md:21`; the full finding→v2-change table is `registration-v2.md:20-32`).
- The L1 re-registered as **v2** before any data commit: `registration-v2.md` at freeze
  `294c667901a8c7b7165ba849d03cba9a24c14fa4` — v2 counters (`quality/counters/c1-r41-globals-v2.py`,
  `c2-r41-focus-entry-v2.py`), controls (`ctl/run-c1-v2-controls.py` 98 controls →
  `receipts/ctl-c1-v2.txt`; `ctl/run-c2-v2-controls.py` 67 controls → `receipts/ctl-c2-v2.txt`;
  `receipts/freeze-counter-check-v2.txt` criterion 64), reference `c1/ctl-ref-tool-v2.py.txt`, and
  the receipts of those controls. Honest ordering disclosed: v2 was written after w1 seats had seen
  v1 scores; v2 is strictly stronger where it touches v1; the report gives both scores at the data
  tip (`registration-v2.md:3-11`).
- **Data commit** `07f2641696b5ac73de1404ea737a9f27e9819aa1` (base `ab2bfaab661c846d1de9d58c01651cd156a13949`):
  `tools/mado-globals.py` (byte-identical to the v2 reference: both sha256
  `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`),
  `corpus/knowledge/hyprland-focus-grab-r41.md` (w1 entry draft A with two one-id-per-line fixes),
  registry rows S283–S289 (+ S037 used-by), `corpus/README.md` row, `corpus/lessons/round-41.md`,
  `.ufo/waves/round-41/fetch/xdph-installed-version.txt` (held-row receipt, M41-6).
- Wave-1 evidence: `w1-results.json` carries no seat outputs — the orchestrator's kernel restarted
  mid-wave; `output: null` with note "read the seat report file in the wave dir" for every seat
  (`w1-results.json:8-12`). Reports on disk: 33 `.md` files under `.ufo/waves/round-41/w1/`
  (one per seat except `ConnSiblingOverlap`, which has no report file or directory there — registry
  member present at `w1/swarm-registry.json:158-163`; the task statement reports no dead seats;
  flagged for L1 closure). Role mix of w1 (`w1/swarm-registry.json` roles, 34 seats): executor 14,
  scribe 8, scout 3, connector 2, reviewer 3, critic 2, mutation-tester 2.
- Assimilation (`registration.md:54-60`, `round-41-lesson.md` `## Assimilation ledger`): theme
  **focus control surfaces**; **admit** `focus-grab-protocol-live-on-host-r14.md` as the successor
  C2 entry; **refuse** `privileged-client-surface-r29.md` (generic Wayland analysis, one truncated
  quote, no measurement, no host state) and `focus-control-surfaces-r28.md` §3 (localized Japanese
  documentation channel, `PROVINCE.md:75`). Id guard (`assimilation/id-guard.md`): reg=219
  staged=147 coll=27, proved on an indented-row fixture (column-zero extractor false-greens).
  Quarantine slice (`assimilation/quarantine-verdicts.md`): 13 rows derived; 1 cited slice row
  (S199) → `unverifiable`; S201 `refuse` as cited (quote absent from `/abs/`, present in `/html/`;
  re-anchoring makes it adoptable).
- Mined mistakes M41-1…M41-8 (`round-41-lesson.md` `## Mistakes`). considerthese: proposal 5 of
  `considerthese/2026-10-25.md` ("verify one fact first-hand per day, read-only") mined as QUALITY
  candidate 69 (`w1/ScrConsiderthese/proposal.md`; re-derivation found the reflection's "eight
  entries" is nine — `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'`
  prints `9`).
- Host receipt (`--live` against the running desktop) reported, not scored (`w1/ExecLiveHost.md`):
  runs 1–3 byte-identical (sha256 `3b3637a482efd330…`), `sessions=2 latest_pid=1952 interfaces=63
  classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,
  output-control:4,sandbox:1,session-lock:2,toplevel-control:4`; `--expect` third verdict
  `MISSING_EXPECTED` rc 1; finding: session 1 is a truncated view (missing start block), so
  `--diff` `removed=` must not be published as "the compositor stopped advertising these".
- Misroot sweep: @@W2:misroot-sweep@@.

## Landed changes

| Commit | Change | LOG |
|---|---|---|
| `60c3914…` | v1 freeze (registration, counters, controls, base receipts, source receipts) | Round 41 bullet 1 |
| `cd950ec…` | wave w1 spec and dispatch (34 seats) | bullet 1 |
| `294c667…` | v2 freeze (registration-v2, v2 counters, controls, reference, receipts) + w1 seat evidence | bullet 1 |
| `07f2641…` | data (tool, entry, rows S283–S289 + S037 used-by, README row, lesson, xdph-installed-version receipt) | bullet 2 |
| @@W2:after-commit@@ | after receipts/census/tip; axis line (M41-4) | bullet 2 |

## Before → after measurements

- **C1 v2** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r41-globals-v2.py --repo . --rev <rev>`:
  before (base `ab2bfaa`) `fixtures=0/39 tool=absent verdict=TARGET_MISSED`, exit 1, nonce
  `25c348da79d01b85` (`receipts/c1-v2-before-base.txt`); after at `07f2641`:
  `fixtures=39/39 tool=present verdict=TARGET_MET`, exit 0, nonce `be51c3bc188d6b05`; clause b
  selftest `63/63`, clause b2 `sites=18 killed=6/6 forced_dead=1`, clause b3 comment/unparse
  variants both `63/63 ok=1`, clauses `a:1 b:1 b2:1 b3:1 g:1`
  (`receipts/c1-v2-after-data.txt`). Verdict: **met under v2 at the data commit**; tip rerun
  @@W2:C1-tip-rerun@@.
- **C1 v1 at the data tip** (superseded predicate, reported per operator rules): `fixtures=6/24
  tool=present verdict=TARGET_MISSED` — v1's frozen clause g refuses the `struct`/`threading`
  imports the security repairs added; exit 1, nonce `cb2bcd4259089823`
  (`receipts/c1-v1-after-data.txt`).
- **C2 v2** `python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev <rev>`:
  before `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`); after at
  `07f2641` `admitted=1/1 verdict=TARGET_MET`, exit 0, all clauses `a:1 b:1 c:1 d:1 e:1 f:1
  g:1 h:1 i:1`, 8 cited ids (S283–S289, S037) each `new=1 status=mined used=1 ok=1` for the new
  ids and `new=0` for the held S037 (`receipts/c2-v2-after-data.txt`). Verdict: **met at the data
  commit**; tip rerun @@W2:C2-tip-rerun@@. The v1 counter also scores `admitted=1/1`
  (`receipts/c2-v1-after-data.txt`). Residual (declared): the pins are the trust root; a fabricated
  self-consistent set passes under the pin-patched counter (`registration-v2.md:57`).
- Harm watch: `MADO_GLOBALS_SELFTEST 47/47` (`w1/ExecLiveHost.md` run 12; contract floor n ≥ 25);
  suite baseline `MADO_SELFTEST: 460/460 assertions passed` (`receipts/selftest-base.txt`); axes at
  base `navigation 58/58, calibration 55/55, operability 12/12`, `MADO_AXIS checked=3 mismatched=0`
  (`receipts/axis-base.txt`). Tip axis transcript (M41-4) @@W2:axis-tip-transcript@@; tip suite run
  @@W2:suite-tip-run@@.

## Sources & frontier

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.
Start (`receipts/census-before.txt`): `mado ok`, W04 ×7 (S030, S042, S045, S097, S119, S120,
S121) + W01 S277, exit 0. End (`receipts/census-after-data.txt`): identical, `mado ok`, exit 0.

- Registry rows 219 → 226 (`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 219 at base, 226 at `07f2641`); added tier A +7 (S283–S289, all `status=mined`, 2026-10-25), held S037 used-by amended to include `corpus/knowledge/hyprland-focus-grab-r41.md`. S290 (`input-capture-v1.xml`) fetched but not cited and has no row; `Hyprland-FocusGrab.hpp` fetched, carries no id (corroboration only; `round-41-lesson.md:38,51-54`).
- Knowledge entries 58 at base → 59 at data (`git ls-tree -r --name-only <rev> corpus/knowledge/ | grep -c '\.md$'`); `corpus/README.md` holds one index row for the C2 entry (line 70 at `07f2641`).
- Sourced claim: C2 cites S283–S289 + S037 (8 ids; `receipts/c2-v2-after-data.txt` clause c lines).
- Touched old→new: used-by on S037 (re-opened byte-identical row content, used-by cell extended).
- Mined mistakes M41-1…M41-8 (`round-41-lesson.md`). Assimilation: one theme, admit/refusals (above); id guard 219/147/27; quarantine slice 13 rows with verdicts. considerthese: `2026-10-25.md` proposal 5 (QUALITY candidate 69, `w1/ScrConsiderthese/proposal.md`).
- Additional frontier finding: `PROVINCE.md:32` claims the tool inventory covers every tracked `tools/` file, but rows 24–30 list 7 while `git ls-tree --name-only HEAD tools/` returns 10 (`mado-eventq.py`, `mado-options.py`, `mado-wsrules.py` unlisted) — `w1/ScrSkillProvince.md` finding 1; draft rows/province addendum written, not landed.

## Trend verdicts

- **expansion: improved** — new capability row (C1 tool), one new knowledge entry (C2), seven
  registry rows, ten fetch receipts; live host census reproduced. Final read @@W2:expansion-final@@.
- **quality: improved** — the wave's cheats and survivors turned into v2 predicates with 98 + 67
  controls and strictly stronger clauses; but the v1 predicates were falsified and re-registered
  after seats had seen v1 scores: disclosed, not a clean pass. Any w2 hole is an open defect of the
  predicate (no third registration). Final read @@W2:quality-final@@.
- **discernment: improved** — refusals with reasons, successor admitted, S201 anchor defect found
  (re-anchoring makes it adoptable), M41-1…M41-8 each tied to a control or shown able to fail;
  QUALITY candidates 69–72 drafted with fail-side evidence (`w1/ScrQualityCriteria/`). Final read
  @@W2:discernment-final@@.

## SHONEN

- [~] SKILL.md real decision tables — historical (`SHONEN.md:5`); `w1/ScrSkillProvince/skill-rows.md`
  drafted (probe-table row anchor 222, decision-table row anchor 157), SKILL.md not edited this round;
  no outside-lane verifier. Landed status @@W2:skill-rows-landed@@.
- [~] End-to-end domain task logged — C1 `--live` host receipt of the portal journal (`w1/ExecLiveHost.md`,
  `round-41-lesson.md` Round 41); reported, not scored; no non-author verifier yet. @@W2:live-receipt-verifier@@.
- [~] Instructions executable without oral context — `python3 -I tools/mado-globals.py --selftest`
  (47/47), `--live`; the counter's docstring is the contract; dispatched seats are not outside verification.
- [~] No cross-domain bleed — localized-channel material excluded (`PROVINCE.md:75`), adjacency
  declared (client lifecycle, security literature); `w1/ScrSkillProvince/province-row.md` drafted,
  not applied to PROVINCE.md.

Stale-lane: respawn-per-round driver; no other mission of this lane is open (as round 40).
Tool installs: none by the L1 through the data commit; w1 seats report none (ExecLiveHost,
ScrSkillProvince, ScrConsiderthese, ScrQualityCriteria). W2 installs @@W2:tool-installs@@.
Open L0 questions: none. Not done: w2 verdicts and tip receipts (M41-4), SKILL.md/PROVINCE.md
rows (drafts), QUALITY 69–72 append, the `ConnSiblingOverlap` artifact check.

## Evidence (verification run for this draft; read-only)

- `git -C … log --oneline ab2bfaa..07f2641` → the four commits above.
- `git -C … show 07f2641:tools/mado-globals.py | sha256sum` and
  `git -C … show 07f2641:.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt | sha256sum` → both
  `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`.
- `git -C … show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 219 (base), 226 (data); S283–S289 rows present, tier A, `status=mined`; S037 used-by extended.
- `git -C … ls-tree -r --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` → 58 (base), 59 (data).
- `git -C … show 07f2641:corpus/README.md | grep -n hyprland-focus-grab-r41` → line 70 (single index row).
- `find .ufo/waves/round-41/w1 -maxdepth 1 -name '*.md' | wc -l` → 33; seat dirs → 33; registry members → 34 (ConnSiblingOverlap has no report).
- Counts read from committed receipts (before/after, both generations) as cited above.

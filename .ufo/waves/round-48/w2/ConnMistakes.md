# ConnMistakes — round 48, w2 (FALSIFY): crosswalk of mined mistakes M48-1..M48-5, proposal 6, and the misroot incident

Seat: `ConnMistakes` (leaf connector, no subagent dispatch). Lane `mado-shokunin`, freeze `3e6c848a`
(base `579f694b`). Method: independent verification in a scratch clone of the lane at the freeze commit
(clone under `/fast/scratch/hyaku/mado-r48/ConnMistakes`, deleted after use; reproduced outputs in
`w2/ConnMistakes/evidence.md`). Every red/green receipt of `w1/ScrMistakes` was re-run, not re-read.

## Verdict table

| row | evidence at pointer | captured-by claim | red/green receipts | fix at freeze |
|---|---|---|---|---|
| M48-1 (D1) | **verified** (shas, lists, FIFO arm, registration line) | none — consistent with 61/64/38/49/9 texts | **reproduced exactly** | 2/3 landed; 3rd resolved *against* ScrMistakes' control (see below) |
| M48-2 (D2) | **verified** (report line, empty grep, 1598 receipts, 13 files) | 69 blind to the shape — verified (69 reads `rev=` only, PASS on same bytes) | **reproduced exactly** | landed as a receipt (`ExecD2Receipt` tip run); the class capture (criterion 97) still draft |
| M48-3 (D3) | **verified** (all 5 seat findings; report=0/lesson=0) | 52/90/93 bind other actors — consistent | **reproduced exactly** | **not landed** — lesson/report still slots; 3 out of 4 finding seats unnamed |
| M48-4 (D4) | **verified** (entry :95, bullet at :149, head-cut) | 77 out of scope — **half-true as evidenced** (see below) | **reproduced exactly** | drafted (`ScrErrataD4` append-only erratum → `:149-150`), lands at data commit |
| M48-5 (M47-7) | **verified** (lesson row, 0 citations, prose-only specs) | none — matches the row's own text | **reproduced exactly** | **landed in w2**: `w2-spec.json` carries `ulimit -f 2048` ×49; `check100` reads `enforced=49 verdict=OK` on the real w2 spec |

## Per-row findings

### M48-1 · `contract-narrowing` — evidence solid; the freeze resolved the third item against this seat's control

All evidence reproduces: frozen blob `762d042c…` at `d7527d60` lists 6 out-of-contract items (`:84`), the landed
tool `b84d5c4f…` lists 9 (`:85-86`), the FIFO raise exists only in the landed bytes (`:526/:529`; frozen `S_ISFIFO`
count 0), HOME-unset raise is byte-identical in both (`:407` = `:410`), and the round-47 registration contract
sentence (`.ufo/waves/round-47/registration.md:52-56`) names none of the three. `check96` red/green re-ran verbatim.

Fix status at freeze — two of three classes landed the way this seat's criterion 96 allows; the third did not:

- **HOME unset** is now *modelled as the pin* (`.ufo/waves/round-48/registration.md:11`;
  `l1-draft/mado-terminal.py:102-104`: exit 1/empty stdout only when a HOME-based default must expand; runs normally
  with all three `XDG_*` set). This is exactly the fix text of criterion 96.
- **FIFO** is now *registered with its condition* (`l1-draft/mado-terminal.py:105-106`: "a FIFO named like a desktop
  file in a later application dir when it is the candidate the resolver reads (the script blocks)"; raise at `:753-754`).
- **Symlink loops** are *gone from the contract list* — not registered, deleted. This follows `w1/ScrD1Line/lines.md`
  M47-13 (measured: the walk silently prunes a repeated `(st_dev, st_ino)` in both frozen and landed bytes, tool and pin
  agree on three loop shapes, **no raise exists**), *against* ScrMistakes' green control
  (`controls/registered-96.txt`: "symlink loops: the walk stops at a repeated directory key **and reports out of
  contract**" — the second half is factually wrong; I verified both code paths return silently). The L1 must know the
  two w1 seats prescribed opposite fixes for this class and the freeze followed the measured one; ScrMistakes' control
  file still misdescribes the pinned behaviour if it is ever cited.

Two instrument holes in the drafted check96 (both reproduced):

1. **Narrowing by deletion passes.** `check96`'s verdict is `NARROWED` only when `unregistered>0`; `REMOVED` items are
   printed but never fail the check. ScrMistakes' own text argues `removed=0` is what made the r47 case narrowing-by-
   addition, but as drafted a contract narrowed purely by deletion exits 0 `verdict=OK`.
2. **House-shape dependency.** The list extractor hard-codes the marker `Also out of contract:`. Run on the real r48
   delta (frozen = r47 landed tool, landed = `l1-draft/mado-terminal.py`) it prints
   `LANDED-NO-LIST ... carries no 'Also out of contract' list`, rc 2 — the r48 docstring says "Out of contract:". As a
   standing criterion, 96 scores exactly one docstring shape and goes deaf the moment the contract is rewritten.

### M48-2 · `unreceipted-number` — evidence solid; the number was right, the receipt is what was missing; the green control's "correction" was the wrong number

Everything reproduces: report line 104 (`findings=128`), `git grep findings=128 d40189c9` → rc 1, 1598 round-47
receipt files, `findings=136` in 13 files, criterion 69's instrument `PASS 1/1` on the same bytes. `check97` red/green
re-ran verbatim.

Two corrections/additions for the record:

- `w1/ExecD2Receipt` (the routed D2 seat) re-ran the gate at the tip: `SESSION_MATERIAL: files=19969 findings=128
  rev=d40189c9…` (`receipts/session-material-d40189c9.txt`). **128 was the true tip value**; D2 was a receipt gap, not a
  numeric error (`ExecD2Receipt.md:72`). ScrMistakes' green control "corrects" the report to `findings=136` — a value
  ExecD2Receipt shows belongs to a different gate configuration. As a mechanism demo (a receipted token passes check97)
  it is fine; as a model of the real fix it would have introduced the very error class M48-2 mines. The fix that
  matches the evidence (commit the tip run) has landed in w1; the fleet report itself is operator-authored and stays
  uncorrected — the disposition belongs in the round-48 lesson, not a lane edit.
- Captured-by analysis holds: criterion 69's grammar is `rev=<hex>` tokens (verified in its check line,
  `corpus/QUALITY.md:385`), so 97 as an extension is justified.

### M48-3 · `routing` — evidence solid; the fix is the one gap that has not landed at all

All five findings verified at their locators (`ExecC1Determinism.md:10`, `MutC1Counter.md:17`, `MutC2Counter.md:40`,
`RevengerCache.md:122`, `ExecAxisBase.md:71`); `report=0 lesson=0` verified; `check98` red (w2 `unrouted=4`, w1
`unrouted=1`) and green (`unrouted=0`) re-ran verbatim. The captured-by argument (52 binds the sweeping seat, 90 the
routed item's identity/age, 93 a gate registry cell — none binds the integrator) matches the criterion texts I read.

Fix status: **open.** The round-48 lesson draft (`w1/ScrLesson/round-48.md:194-221`) still has `<AFTER>` slots; only
`ExecC1Determinism` is named (as M48-3's evidence line). `MutC1Counter`, `MutC2Counter`, `RevengerCache` (w2) and
`ExecAxisBase` (w1) appear nowhere in the lesson draft, and the round-48 report does not exist yet. Criterion 98's own
green control required all four routing lines; at the freeze none are committed. This is the largest unlanded gap among
the five rows, and it is cheap to close at data commit (four lines in the lesson's `## Mistakes`).

### M48-4 · `locator` — the defect is real and reproduces; one evidence sub-claim overstates criterion 77's blindness

Defect verified: entry `xdg-terminal-selection-r47.md:95` cites `terminal-route-r17.md:150-151`; the `[UNK]` bullet
opens at `:149`; three bare `README.md` locators (`:218`, `:300-301`, `:179-180`) basename-match three different files
(14/337/329 lines). `check99` red (`violations=4`) and green (`violations=0`) re-ran verbatim.

Correction to the evidence as written: `receipts/d4-locator.txt` shows criterion 77's instrument printing
`locators=0 miss=0` — but the receipt ran it with `--fetch .ufo/waves/round-43/fetch` (criterion 77's *example*
command). Run against the entry's **own pins** (`.ufo/waves/round-47/fetch`, declared at the entry's line 4),
`quality/check-locators.py` prints **`locators=7 miss=3`, rc 1** on this entry — three fragment-support misses
(`README.md:218` at entry line 38, `desktop-entry-spec.xml:636-645` at line 51, `README.md:179-180` at line 93).
So: the code-level scope claim is true and verified (`check-locators.py:111-123` resolves only names present in
`--fetch`; the corpus-to-corpus `terminal-route-r17.md` reference is never read, and the head-cut stays invisible to
77). But the concrete "locators=0" receipt understates the instrument, and it implies an enforcement truth worth
naming: **with the round-47 fetch dir, criterion 77 would already have failed this entry at round-47 freeze** — the
locators were never actually scanned, not merely unscannable. Criterion 99 remains justified (corpus-to-corpus
resolution, `[UNK]`-anchor rule, repo-wide ambiguity are all outside 77), but its grounding should cite the code
scope, not the fetch-dir-dependent `locators=0` run.

Minor accounting slip in the same row: the `## Duplicate check` sweep names M46-6/M46-11 as the uncited mechanism
class but never names **M46-13** (the `__pycache__` write) among the eight `captured-by: none` rows it lists; M46-13's
event is de-facto criterion 95's "shown able to fail" input, while 95's lesson citation says M47-6
(`corpus/QUALITY.md:498-504`). Class captured, citation one row off.

### M48-5 · `provider` (M47-7) — evidence solid; the fix has actually landed, in this wave's own dispatch

Verified: the lesson row (`corpus/lessons/round-47.md:189-191`, "captured-by: none"), the criteria citations covering
M47-1..M47-6 only, `grep -c M47-7 corpus/QUALITY.md` → 0, and both w1 specs prose-only (`check100` red reproduced on
r47 and r48 w1 specs). What the row could not know at w1 time: **the fix landed in the w2 dispatch** —
`w2-spec.json` carries `ulimit -f 2048` 49 times, and `check100` on the real w2 spec reads
`enforced=49 prose=102 verdict=OK`, rc 0 (reproduced). The round that mined the class no longer exhibits it in its own
dispatch. Two honest residuals: (a) enforcement is still per-command prose — nothing verifies a seat actually ran the
ulimit (the criterion text asks each seat receipt to record its largest file; compliance is attested, not measured);
(b) the w1 specs remain prose-only, which is correct as *mined evidence* but means the w1 wave itself ran uncapped
— exactly the exposure M47-7 recorded. Note the identity M48-5 = M47-7 is declared, not double-counted.

## Proposal 6 (ScrConsider) — criterion is sound and genuinely open; the number 96 is double-claimed

- **Open at base: verified.** 95 criteria at `579f694b`; `considerthese` citations only at 60/76/81/82/90; no gate, no
  refusal.
- **Check: reproduced.** `check96.py --selftest` → `SELFTEST: ok cases=5`; red at base rounds 44-47 → `fail=4`
  (`process_tokens=9/10/14/11`, matching the seat's receipt); the green control is a clone-only edit of `SCORECARD.md`
  (lane untouched — the seat's scope claims check out).
- **Distinctness: holds.** It governs the closure section's *leading sentence*; criteria 60/82 govern what gets counted
  and the ratio number. The `[INFERENCE]` transposition (binding the lane's own `SCORECARD.md` instead of the
  operator-authored reflection) is explicitly labelled and argued from `corpus/lessons/round-32.md:120`.
- **Collision: real.** ScrConsider's "provisional 96" (`draft.md:5`) sits on the exact number the w1 spec assigned to
  ScrMistakes' block (96-100; `make-w1-spec.py:326`). ScrConsider saw it coming (`draft.md` §7.1: "other w1 seats may
  add criteria 96+ before the freeze") and deferred the number to the L1. At the freeze both drafts stand; the
  scorecard draft's `<Q-LO>-<Q-HI>` "start at criterion 96" cannot be filled as-is. Content-wise there is no overlap
  (outcome-first ordering vs contract-narrowing), so this is a numbering defect, not a duplicate criterion — the L1
  renumbers one side at data commit.
- Self-application risk: if landed, criterion 96 scores round 48's own closure section; that section does not exist at
  the freeze, so its `fail=0` cannot be checked until the data commit.

## Misroot / message-by-name incident — handled cleanly, attribution unresolved, no committed disposition yet

Facts (all read-only): a 347,495-byte `tree.json` — a GitHub git-trees API dump of `hyprwm/Hyprland` at `efb50993`
(v0.56.2) — landed in the fleet root during w1 and was quarantined by the orchestrator at 20:48 into
`.tower/quarantine/fleet-root-strays-20261026T2055/` (manifest `SHA256SUMS`:
`fdb0b7a49736a50b956ef899b64a4381547a0b37a4663a3eae46f731257e16d3`). Earlier stray batches the same evening
(`=1239`, `=3900`, `T` at 19:56; `p.out`/`p.err` at 20:10) show the failure mode recurred. The fleet root is clean now
(`git status --porcelain` empty; no `tree.json`), and neither `LOG.md` nor `.ufo/watchdog.log` records the event by
literal grep.

Handling was **by name**: MadoR48 reported the stray to the wave; the seats whose activity could have produced it
answered by name in their own reports — `ScoutXkbSpecs.md:93` (its trees dump was written inside scratch, removed),
`ExecXkbLive.md:251-256` (exactly three absolute paths written), `ExecXkbSource.md:112` (absolute-path inventory),
`CritPremiseC2.md:23-24` (checked the notice, reply sent to MadoR48). No seat admitted authorship; I found no
attribution anywhere in w1, and the quarantine manifest names no writer. Three gaps for the L1: (a) the incident has no
committed lane disposition yet (the round-48 lesson's `## Conflicts` slot is where it can land); (b) nothing in the
lane detects a fleet-root stray (the w2 `SentScope` seat audits scope this wave — there is no standing criterion; the
nearest class, criterion 98, binds *routing of findings*, not *write containment*); (c) the by-name sweep is the same
proxy ScrMistakes declared for check98 — candidates were located by name/activity, and an authoring seat that stayed
silent would never have been found. That is acceptable for incident response, but it should not be mistaken for
evidence of scope.

## Unlanded fix gaps (named, in priority order)

1. **M48-3 routing lines** — none of the four finding seats (`MutC1Counter`, `MutC2Counter`, `RevengerCache`,
   `ExecAxisBase`) is named in the lesson draft or any report; only `ExecC1Determinism` is. Closes at data commit.
2. **Criterion-96 numbering collision** — ScrConsider vs ScrMistakes on "96"; L1 must renumber (ScrConsider's own §7.1
   delegates the number).
3. **check96 instrument holes** — removal-narrowing passes (no fail on `REMOVED`); hard-coded `Also out of contract:`
   marker returns rc 2 on the actual r48 docstring shape. If 96 lands, fix the instrument before the freeze text cites
   it.
4. **Misroot disposition** — quarantined tree.json has no admission and no lesson line; add the attribution outcome
   (even "unattributed, denials on record") to the round-48 lesson.
5. **ScrMistakes' `controls/registered-96.txt`** misdescribes the symlink-loop behaviour ("reports out of contract" —
   no raise exists); if the L1 keeps the control as evidence it should be corrected to ScrD1Line's measured text or
   dropped in favour of the M47-13 wording.
6. **M48-4 evidence note** — `receipts/d4-locator.txt`'s `locators=0` was produced with the round-43 fetch dir; with
   the entry's own pins criterion 77 already fails the entry (miss=3). Criterion 99 stays justified on the code-scope
   argument; the receipt text should not be quoted as "77 reads nothing here".

## Double-counting (named)

1. **D1 is mined three times** — ScrMistakes M48-1 (+ criterion 96 + check96), ScrD1Line M47-11..M47-14 (+ measured
   probes), and ExecHomeUnset's own M47-12 (explicitly relabelled "placeholder label only — ScrD1Line numbers…",
   `ExecHomeUnset.md:168-183`). The landable artifact is ScrD1Line's block; the scorecard must count the D1 lesson lines
   once. ScrMistakes' criterion 96 remains valuable as the *capture*, but its evidence and fix text overlap ScrD1Line's
   on every point except the instrument itself.
2. **Criterion 96 claimed twice** — ScrConsider (proposal 6) and ScrMistakes (M48-1). Numbering only; no content
   overlap.
3. **M48-5 = M47-7** — declared identity, correctly a recurrence row, not a new mistake; do not let the scorecard's
   mistakes range count it as a second instance of the class.
4. **Criterion 95 vs M46-13/M47-6** — 95's failing input is the M46-13 event but its lesson citation is M47-6; a
   citation mismatch inside the existing 1-95 set, visible only because ScrMistakes' sweep surfaced the row.

## Seat hygiene

Read-only over the lane and fleet; my only writes are this report and `w2/ConnMistakes/evidence.md`. Scratch clone
390 MB total (largest single files: git-internal pack objects; largest file I generated: this evidence file, 8.9 KB),
removed before return. `ulimit -f 2048` in force for every writer command except the one-time clone/checkout. No
pacman, no installs, no counters, no resolver/`xkbcli` runs, no lane or fleet mutation.

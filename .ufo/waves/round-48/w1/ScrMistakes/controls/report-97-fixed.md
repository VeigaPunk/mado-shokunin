# mado — round 47 report (hyaku run 9, attempt 1)

Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, final lane hash **`d40189c924e01dc1cbe290474eb4256d343590d4`** (`git ls-remote origin refs/heads/master` prints it). Base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. Round shape: **two v1 waves** (policy v1, band 32-64): `w1` build **41 seats** (executor 16, scribe 10, scout 5, critic 4, connector 2, sentinel 2, reviewer 1, revenger 1) and `w2` falsify **44 seats** (executor 17, critic 8, mutation-tester 5, reviewer 5, sentinel 4, scout 2, connector 2, revenger 1). Round total **85 seats**, no residual call. Dead seats: **0 by results** (85 of 85 returned output). Exception: w1 `ExecRefB` was cancelled by the orchestrator after a runaway scratch write (about 590 GB, M47-7). Its output is recorded but not cited as a completed seat. The L1 holds the §3 planner seat; `labrat` was not used.

## Work performed

Declared claims (`.ufo/waves/round-47/claims.md`, commit `c24adef2`, before w1). Frozen in `registration.md` at **`d7527d608ad2b2e3cc398fdde34db7947b254a1a`** before w2 and before any data. No re-registration.
- **C1 — operability (capability acquisition): `tools/mado-terminal.py`.** Answers which desktop entry `xdg-terminal-exec` 0.14.3 (SUPER+RETURN) selects and why. It starts no process and opens no socket. Judged by `PRED-C1-r47`; the judge is the **real pinned script**, run in bwrap.
- **C2 — coverage (sourced): `corpus/knowledge/xdg-terminal-selection-r47.md`.** The executed selection chain, on rows S326-S331 opened this round. It answers the selection half of the round-17 `[UNK]` (`terminal-route-r17.md:144-145`). Judged by `PRED-C2-r47`.

Lowest-axis rule: every axis sat tied at its maximum at base (`receipts/axis-base.txt`, `checked=3 mismatched=0`). Paths below are under `mado-shokunin/.ufo/waves/round-47/`.

- **L1 reference** `l1-draft/mado-terminal.py`, written from the script:
  - selftest 43/43;
  - 8000 random cases agree with `/usr/bin/xdg-terminal-exec` (`receipts/l1-fuzz-8000.txt`);
  - the 140 w1 seat fixtures agree as well.
- **C1 counter** `quality/counters/c1-r47-terminal.py`:
  - clauses a, s, f (190 fixtures × 2 variants on separate trees), x (`explain` and `--observed` both ways), g (150 nonce cases), i (allowlist bwrap), r (strace around bwrap: process or socket = trip);
  - fixtures built by `ctl/build-fixtures.py`, with `expect` from three runs of the pin.
- **C1 controls** `receipts/ctl-c1.txt`: `CTL_C1 VERDICT: PASS (... 0 of 28; reference met: 1)`. The 28 include a delegator, embedded-script execv, ctypes execve, a socket, canned explain and 17 one-rule mutants. Two pre-freeze runs are committed: 5 of 27 met before the fixture additions (`receipts/ctl-c1-prefreeze-1.txt`), 0 after.
- **C2 counter:** the w1 `ExecCounterC2` draft, with clause f rewritten by the L1. The draft re-ran our tool, which coupled C2 to C1 (M47-9). Controls `receipts/ctl-c2/ctl-summary.txt`: POS 0, the ten negatives 1.
- **w1 premise corrections** (`w1/CritPremise.md`): only the selection half of the `[UNK]` can be answered; list order and validation are partly held at r17:24-59. Both are recorded in `registration.md`.
- **w2 attacks:**
  - `w2/ExecC1Diff.md` found two contract errors outside the fixtures. H1: `-type f` binds to the first application dir only. H2: `command -v -p` exits 0.
  - The landed tool fixes both (`receipts/h12-check.txt`: 32 pin-judged cases, diff 0). The fixture gap is routed (M47-10).
  - `w2/MutC1Fixtures.md` (22 mutants, 11 survivors) and `w2/CritC1Explain.md` (one passing explain mutant) are routed, with `w2/SentC1Sandbox.md` F1-F4 (counter wording and robustness; no false MET reachable). `w2/CritC2Forgery.md` F4/F7/F8 are undeclared C2 residuals.
  - Tripwire held: `w2/SentC1Tripwire.md`, `w2/MutTripwire.md`.
  - Separability holds both ways (`w2/ExecSeparability.md`).
  - Entry fixes from `w2/CritEntryContent.md`: three wrong sentences (W1-W3), corrected in the landed entry.
- **Round-46 closure:**
  - R1: erratum appended, framing corrected per `w2/ExecErrataR1`.
  - R2: file removed after its digest (`receipts/r2-removed.txt`).
  - R4a: S290-S297 superseded by S332-S339 (`w2/RevSupersede.md`: landable).
  - R4c: SCORECARD lines appended (`w2/ExecErrataCal.md` 6/6).
  - R3 (marker install) and R4b (the round-45 errata break the frozen round-45 counter, `w2/ExecErrataR45.md`) are **not landed and routed again**.

## Landed changes

| Commit | Change | LOG.md Round 47 bullet |
|---|---|---|
| `c24adef2632672325a4eef3e3492f6716ccb6d14` | claims, w1 spec + dispatch, census before | 1 |
| `d7527d608ad2b2e3cc398fdde34db7947b254a1a` | v1 freeze: registration, both counters, 190 fixtures, pins, reference, controls runners, base receipts | 2 |
| `6605f5f1f990fe6a10f83196d3c4380a9499eb8c` | control receipts (C1 PASS 0 of 28, C2 PASS), w2 spec + dispatch | 2 |
| `9bddd6ac89c75a9b164b5dcc313de6f7aef2096c` | w1 evidence (41 reports, results), R2 removal receipt, fuzz receipt | 1, 6 |
| `0c69960510bcd30705d222873cd9b860aa9329ba` | **data**: tool, entry, rows S326-S339, lesson, QUALITY 91-95, README row + Frontier, SKILL section, R1 erratum, live receipts | 4 |
| `f2b8568b9f605902e374a0274914a32def66aa0b` | SCORECARD/LOG Round 47 (axis publication, R4c lines), after-data receipts | 4-6 |
| `d40189c924e01dc1cbe290474eb4256d343590d4` | w2 evidence (44 reports, results), tip receipts | 3 |

Inherited state: one untracked round-46 file. It was removed after its digest (R2). No other leftovers. Worktree clean at the tip.

## Before → after measurements

- **C1:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r47-terminal.py --repo . --rev <rev> --work <scratch>`
  - Base: `fixtures=0/190 explained=0/190 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED`, exit 1 (`receipts/c1-before-base.txt`).
  - Data `0c699605`: `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0 (`receipts/c1-after-data.txt`).
  - Tip `f2b8568b`: the same MET (`receipts/c1-tip.txt`).
  - Self-verdict **TARGET_MET**.
- **C2:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r47-terminal-entry.py --repo . --rev <rev>`
  - Base: `admitted=0/1 TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`).
  - Data `0c699605` and tip: `clauses=a:1 ... i:1 admitted=1/1 verdict=TARGET_MET`, exit 0 (`receipts/c2-after-data.txt`, `receipts/c2-tip.txt`).
  - Self-verdict **TARGET_MET**.
- **Harm watch:** `python3 -I quality/check-axis-scores.py --rev f2b8568b... --repo .` gives `MADO_AXIS: checked=3 mismatched=0` (navigation 64/64, calibration 82/82, operability 12/12; `receipts/axis-tip.txt`). The data commit reads STALE in the two-phase window (`receipts/axis-data.txt`).
- **Live host run:** `receipts/live-terminal-host-r47.txt`. Its `tool_sha256` equals the landed bytes. It records resolver `Alacritty.desktop` at the user override, `verdict=AGREE`, exit 0, an empty argument refused with exit 2, and selftest 43/43.

## Sources & frontier

Census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`:
- Before (`receipts/census-before.txt`): W04 ×14, W01 ×1, `mado ok`, exit 0.
- After (`receipts/census-after.txt`): W04 ×17 (+S326, S327, S332 repeat held URLs under new scopes), W01 ×1, `mado ok`, exit 0.

Changes:
- **Rows:** 262 → **276**, counted with `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`.
- **Added by tier:**
  - S326-S331: A ×5 and B ×1 (the unmerged terminal-wg proposal); all `mined`, opened 2026-10-26, pins under `fetch/`.
  - S332-S339: A ×8, superseding S290-S297.
  - Gate lines and rejects (≥1 admit, ≥1 reject) are in `corpus/lessons/round-47.md` `## Gate`.
- **Rows touched old→new:** none. Held rows are byte-identical, including S056-S060 (C2 clause h) and S290-S297 (append-only supersession).
- **Renumber map:** seat S346-S353 → S332-S339, by document. It is logged in the lesson.
- **Frontier advanced:** README Frontier bullet "Round 47 moves the P4 terminal-selection route from documentary to executed ground". Knowledge entries 63 → 64.
- **Sourced claim:** C2 rests on S326-S331.
- **Assimilation: none.**
  - `w1/ScoutShokuknow.md`: no `merge/mado/` theme on the plane.
  - Id guard `assimilation/`: reg 262, staged 147, 70 collisions. The guard was proven on an indented fixture.
  - Quarantine slice: 13 rows, none appended and none hand-checked.
- **considerthese:** `2026-10-26.md` proposal 2 (the live-tool ledger) was refused this round. `w2/ExecToolLedger.md` found wrong rows. The refusal is recorded in the lesson.
- **Mistakes mined:** M47-1..10, landing as QUALITY 91-95.

## Trend verdicts

- **expansion: improved.**
  - One capability, with a live run and a SCORECARD capabilities row.
  - One entry on ground absent at base: `receipts/c2-ground-base.txt`, git grep exit 1.
  - Rows 262 → 276.
- **quality: improved.**
  - The judge is the real resolver, not our reference.
  - w2 found two contract errors, and the landed tool fixes them with pin-judged evidence.
  - Entry errors W1-W3 were corrected before data.
  - Limits: R3 and R4b are still open, and the C1 fixture gap (M47-10, MutC1Fixtures survivors) is routed.
- **discernment: improved** (self-assessed, pending the non-author closure).
  - Premises were narrowed on w1 evidence: the launch half stays `[UNK]`.
  - C2 was decoupled from C1 before the freeze.
  - Two equivalent mutants were dropped from the controls, with reasons.
  - Undeclared C2 forgeries are reported, not hidden.
  - Note: the session-material gate reads `findings=136` at the tip (115 at base). It is red, R3 is not installed, and the new findings are not triaged.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources. New section "Terminal selection (round 47)" with verdict and symptom tables (`SKILL.md` tail, commit `0c699605`). No non-author verifier.
- [~] At least one end-to-end domain task executed and logged. Live read-only resolver capture plus the landed tool's AGREE: `.ufo/waves/round-47/receipts/live-terminal-host-r47.txt`; LOG.md Round 47. No non-author verifier.
- [~] Instructions executable by an agent without oral context. `w2/ExecC1IndepA.md` rebuilt a TARGET_MET tool from the docstring and the script, naming the contract gaps H1-H3. Dispatched seats are not outside-lane verifiers.
- [~] No cross-domain bleed (PROVINCE.md still accurate). `w1/ConnSiblings.md`: no sibling claims terminal selection. No non-author verifier.

Stale-lane: respawn-per-round driver; no other mission of this lane is open.

Tool installs: none. bwrap, strace and python3 were present; seats report none.

Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` printed nothing. `w2/ScoutMisroot.md` agrees. A transient `round-47/SentHost` dir seen mid-w1 was gone before the commit.

Scratch: `/fast/scratch/hyaku/mado-r47` removed after landing.

Open L0 questions: none filed. Carried for the operator: the host monitor serial in held files (M46-10); the session-material gate is still red (R3).

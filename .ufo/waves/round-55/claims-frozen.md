# Round 55 — frozen claims (mado, hyaku run 11, attempt 1)

Base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`. This file, `registration.md`, `frozen-tables.json`, `fixtures/c2/`,
`ctl/`, `freeze-verify.py`, `fetch/` and `receipts/{before,census-before}.txt` are committed in ONE freeze commit
BEFORE any wave `.ready` is written (answers M53-4 / M54-2 / M54-4). No predicate, counter sentence, control, fixture or
target here changes after any seat has scored; a falsified predicate is an honest stop, never an edit of this file.
Fresh-start posture (rounds 52–54 were three honest stops): every claim below is one a do-nothing control cannot reach
(§9) and every frozen quote is a SINGLE-LINE substring tested byte-for-byte against the pin by `freeze-verify.py`
(`receipts/freeze-verify.txt`) before this commit — no multi-line quote, no normalization.

Stagnation nudge (AXES.md): saturation 9.0 / window N=3 (SCORECARD "Saturation (declared this round)"); the last
capability row entered in round 51; rounds 52, 53, 54 entered none. The window has elapsed, so the lowest-axis
obligation is waived and the round is a capability + frontier move: C1 moves frontier ground (the input-device
per-keyboard settings the dump never prints) into sourced ground; C2 is a capability acquisition (a runnable tool).

## C1 — coverage (sourced entry): keyboard repeat rate, repeat delay and numlock on Hyprland 0.56.2

**Surface moved:** the P1/P6 input-device plane's per-keyboard settings — `corpus/knowledge/hyprland-input-devices-r46.md`
(line 70) lists `repeat_rate`, `repeat_delay`, `numlock_by_default` as "applied per device too but the dump prints none
of them ... UNK". Path moved: config value → `applyConfigToKeyboard` → keyboard state → seat → `wl_keyboard.repeat_info`;
numlock → keymap setup. Unmoved command: `grep -lE 'repeat_info|m_repeatRate' corpus/knowledge/*.md` → 0 files at base.

Predicate (PRED-C1-r55, frozen sentence): `python3 -I quality/counters/c1-r55-kbd-entry.py --repo . --rev <rev> --work <scratch>`
prints one line `MADO_KBD_ENTRY: rev=<rev> rows=18/18 hosts=6/6 sources=<n>/<n> new_rows=<m>/3 verdict=TARGET_MET missed=none`
and exits 0, AND the independent harness `python3 -I quality/check-r55-controls.py --claim c1 --repo . --rev <rev> --work <scratch>`
prints `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK` and exits 0. Registration §C1 defines the legs.

Before (base `3b55b6e`): entry absent, counter and harness absent (`receipts/before.txt`: 0/0/0) — TARGET_MISSED by absence.
Target: both lines at the round's final content revision. Kill rule: any leg missed, or any control admitted by the counter
(harness `controls<7/7`), or `good` not ok → `TARGET_MISSED`, honest stop.
Sourced-claim duty (§2b item 4): rows S378–S380 are opened this round; the entry's K10, K11, K12 and K18 cite them.
Declared limit (QUALITY 104/105): the counter proves quote identity at an exact pin line and row/host binding; it does not
prove that a proposition sentence is entailed by its quote — that is the independent sentence-to-pin audit (w2) and the
non-author closure review, reported, not counted.

## C2 — operability (capability acquisition): `tools/mado-kbdopts.py`

**Surface moved:** a new read-only tool that joins caller-supplied Hyprland config text to the three effective
per-keyboard values and to `hyprctl getoption` JSON — runnable on this host, against the real `input.conf`.

Predicate (PRED-C2-r55, frozen sentence): `python3 -I quality/check-r55-controls.py --claim c2 --repo . --rev <rev> --work <scratch>`
exports the tool, the 18 committed fixtures, the 8 revealed hold-out fixtures and the three `ctl/` stubs at `<rev>` into
the scratch dir, runs each as a child process, compares stdout bytes and exit status to each fixture's `expected.out`/
`expected.rc`, and prints `MADO_R55_C2: rev=<rev> fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`,
exit 0. `holdout_commit=ok` means the hold-out tree's commitment equals `frozen-tables.json` `c2.holdout_commit_sha256`
(the hold-out fixtures were sealed before the wave and revealed at integration). `controls=3/3` means: `ctl/const-host.py`
passes ≤1 of the 26 fixtures; `ctl/empty.py` passes 0; `ctl/lookup-committed.py` passes 18/18 committed and 0/8 hold-out.

Before (base): tool absent, harness absent — `fixtures=0/18` by absence. Target: the frozen line at the final content
revision. Kill rule: any fixture byte mismatch, hold-out mismatch, or a control behaving otherwise → `TARGET_MISSED`.
Do-nothing control: a constant host-fixture printer, an empty program and a lookup table over the committed fixtures are
the three frozen controls and none may pass (the lookup table is why the hold-out exists).
Capability row (SCORECARD) enters only on `TARGET_MET`: "predict a keyboard's repeat/numlock values from config text and
join them to `hyprctl getoption`". Declared limit: values outside the modelled token set are `unsupported`, never guessed;
the tool models source-level semantics (registration §C2 cites the pins) and does not observe a keypress.

## C3 — freshness (append-only correction): the false P19 statement

**Surface moved:** `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` P19 says `Actions::pass` "sends a
PRESSED keyboard key only when `m_passPressed == 1`"; the pin's `else` arm at `ConfigActions.cpp:1566-1569` also sends
PRESSED (routed defect 1 of the r54 closure; M54-5; QUALITY 104).

Predicate (PRED-C3-r55, frozen sentence): `python3 -I quality/counters/c3-r55-p19.py --repo . --rev <rev> --work <scratch>`
prints `MADO_P19_FIX: rev=<rev> prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none`, exit 0,
AND `python3 -I quality/check-r55-controls.py --claim c3 --repo . --rev <rev> --work <scratch>` prints
`MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK`, exit 0. Registration §C3 defines the legs.

Before (base): `git show 3b55b6e:<entry> | grep -c P23` → 0 (`receipts/before.txt`) — TARGET_MISSED by absence. Kill rule as C1.

## Causal separability

C1 reads `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`, `corpus/README.md` (its row), rows S378–S380 and the
cited existing rows of `corpus/SOURCES.md`, `.ufo/waves/round-55/fetch/`, `frozen-tables.json`. C2 reads
`tools/mado-kbdopts.py`, `fixtures/c2*`, `ctl/`. C3 reads the errata entry, `corpus/README.md` (its row) and the round-52 pin.
Shared record files (README table, SOURCES.md, lesson, LOG, SCORECARD, QUALITY) are integration surfaces, not claim evidence.
Each claim's counter and harness mode run against the committed tree without the other claims' artifacts.

## Harm watch (frozen)

`bash tools/mado-verify.sh --selftest` stays 460/460 (baseline measured 2026-10-28, `receipts/before.txt`); navigation
index stays complete (69/69 → 70/70, never fewer); `scripts/sources-census.sh validate --root … mado` stays exit 0; no
config tree, compositor, service or sibling repo is written; the host is read by read verbs only.

## Mistake-fix item (inside §2b step 3, not a claim)

M54-2/M54-4 (freeze committed after launch): this round commits the freeze before `.ready`, and `quality/check-freeze-order.py`
is delivered as the fix, shown able to fail on the committed round-54 evidence (freeze commit `350d30e4` committer 14:11:10
vs wave registry `createdAt` 14:05:25) and able to pass on round 55. It is evidence for the mistake fix, not a fourth claim.

## Exploratory claims

None. All three claims are counting claims.

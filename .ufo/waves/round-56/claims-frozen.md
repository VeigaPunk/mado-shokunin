# Round 56 — frozen claims (mado, hyaku run 11, attempt 1)

Base: the `base` field of `frozen-tables.json` (lane tip `13f0acbe3a15da2d9c08357a576d91dcadc85273`). This file, `registration.md`,
`frozen-tables.json`, `fixtures/c2/`, `ctl/`, `fetch/`, `freeze-verify.py` and `receipts/{before,census-before,selftest-before,
scope-replay-r55,pins}.*` are committed in ONE freeze commit BEFORE any wave `.ready` (answers M53-4/M54-2/M55-1; checked by
`quality/check-freeze-order.py`). No predicate, counter sentence, control, fixture or target here changes after any seat has scored.
A falsified predicate is an honest stop or a pre-data re-registration in a NEW versioned file. Every frozen quote is a single-line,
pipe-free substring tested byte for byte against its pin by `freeze-verify.py` BEFORE this commit (receipt: `receipts/freeze-verify.txt`),
and the C1 grammar was shown satisfiable as written by an L1 witness (every row, `tok`, `num`, `scope` leg) before freezing
(`receipts/witness.txt`) — the round-55 lesson (v1 PRED-C1 was unsatisfiable as written).

Axis posture. SCORECARD declares saturation 9.0 / window N=3; the last capability row entered in round 55, so the stagnation
window has NOT elapsed and the lowest-axis obligation applies. Scored sub-axes: freshness 9.6552 (file-plane gate), coverage
navigation 10.0 and operability 10.0 (saturated on finite denominators, harm watch only); calibration, depth and adjacency are
unscored. C3 therefore works the least-evidenced axis, **calibration**, with a counted rubric introduced this round
(registry-versus-entry back-references). C1 works **coverage** on frontier ground; C2 is a **capability acquisition** (operability).

## C1 — coverage (sourced entry): Hyprland config auto-reload on 0.56.2

**Surface moved.** The config plane the lane owns is edited by the operator; whether and how Hyprland reloads on save was
not on the corpus (`git grep -liE 'disable_autoreload|ConfigWatcher|IN_CLOSE_WRITE|inotify_add_watch' <base> -- corpus/knowledge | wc -l`
→ **0**; `receipts/before.txt`). Chain moved onto sourced ground: `misc:disable_autoreload` (declaration, refresh flag) →
`CConfigWatcher::update` → watch list = `m_configPaths` (main config + every regular file reached by `source =`, glob and `~`
rules) → inotify masks (file vs directory, symlink canonical second watch) → event loop → `CConfigManager::reload` →
`REFRESH_ALL` → `hyprctl reload` / keyword paths, with the inotify(7) semantics of `IN_CLOSE_WRITE` and `IN_DONT_FOLLOW`.

**Predicate (PRED-C1-r56, frozen sentence):** `python3 -I quality/counters/c1-r56-autoreload-entry.py --repo . --rev <rev> --work <scratch>`
prints one line `MADO_AUTORELOAD_ENTRY: rev=<rev> rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`
and exits 0, AND `python3 -I quality/check-r56-controls.py --claim c1 --repo . --rev <rev> --work <scratch>` prints
`MADO_R56_CONTROLS: claim=c1 good=ok controls=10/10 verdict=OK` and exits 0. Registration §C1 defines the legs.

**Before** (base): entry, counter, harness absent (`receipts/before.txt`: 0 hits, files absent) — TARGET_MISSED by absence.
**Target:** both lines at the round's final content revision. **Kill rule:** any leg missed, any control admitted by the counter
(`controls<10/10`), or `good` not ok → TARGET_MISSED, honest stop.
**Sourced-claim duty (§2b item 4):** rows S383-S390 are opened this round (2026-10-28) from the pins in `fetch/`; the entry's K rows cite them.
**Do-nothing controls (§9):** controls 1 (absent) and 2 (junk placeholders: the cheapest entry that copies the frozen quotes and fills
placeholder propositions) both score TARGET_MISSED; controls 3-10 mutate the good tree one leg at a time. Declared limit: the counter
proves quote identity, registry scope and lexical grounding; it does not prove a proposition is entailed by its quote — that is the
wave-2 sentence-to-pin audit and the non-author closure, reported, not counted.

## C2 — operability (capability acquisition): `tools/mado-watchplan.py`

**Surface moved.** A new read-only tool that predicts the inotify watch list Hyprland registers for a config tree (main config
plus the `source =` closure, symlink canonical watches, `misc:disable_autoreload`), joined to `hyprctl getoption` — runnable on this
host against the real `~/.config/hypr/hyprland.conf`.

**Predicate (PRED-C2-r56, frozen sentence):** `python3 -I quality/check-r56-controls.py --claim c2 --repo . --rev <rev> --work <scratch>`
exports the tool, the 18 committed fixtures, the 8 revealed hold-out fixtures and the three `ctl/` stubs at `<rev>` into the scratch dir,
runs each as a child process, compares stdout bytes and exit status to each fixture's `expected.out`/`expected.rc`, and prints
`MADO_R56_C2: rev=<rev> fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`, exit 0. `holdout_commit=ok` means the
hold-out tree's commitment equals `frozen-tables.json` `c2.holdout_commit_sha256` (sealed before the wave, revealed at integration).
`controls=3/3`: `ctl/const-host.py` passes at most 1 of the 26 fixtures; `ctl/empty.py` passes 0; `ctl/lookup-committed.py` passes 18/18
committed and 0/8 hold-out.
**Before:** tool and harness absent — `fixtures=0/18` by absence. **Target:** the frozen line at the final content revision.
**Kill rule:** any fixture/hold-out byte mismatch, a hold-out commitment other than `ok`, or a control behaving otherwise → TARGET_MISSED.
Capability row (SCORECARD) enters only on TARGET_MET: "predict the inotify watch list Hyprland sets for a config tree and join it to
`misc:disable_autoreload`". Declared limit: an approximation of Hyprland (registration §C2 lists 5 divergences); no filesystem event is
generated and no reload is observed.

## C3 — calibration: registry back-references match the entries that cite them

**Surface moved.** `corpus/SOURCES.md` `used-by` cells are the lane's own statement of which knowledge entries cite which row. At base,
65 (row, entry) pairs cite a registry id in the entry text without the entry path in that row's `used-by` (CORPUS contract rule: used-by
= "repo-relative paths of the knowledge entries or lessons citing the row").

**Predicate (PRED-C3-r56, frozen sentence):** `python3 -I quality/counters/c3-r56-used-by.py --repo . --rev <rev> --work <scratch>` prints
`MADO_USED_BY: rev=<rev> entries=<E> rows=<R> missing=0 extra=0 dangling=0 verdict=TARGET_MET missed=none` and exits 0, AND
`python3 -I quality/check-r56-controls.py --claim c3 --repo . --rev <rev> --work <scratch>` prints
`MADO_R56_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK` and exits 0. Definitions: registration §C3.
**Before** (base, `receipts/before.txt`): `entries=70 rows=319 missing=65 extra=0 dangling=0` → TARGET_MISSED (missing=65).
**Target:** missing=0, extra=0, dangling=0 at the final content revision, with `used-by` edits only (cell 11), each logged old→new in the
round lesson; no other registry cell changes (CORPUS rule 2). **Kill rule:** any of the three counts non-zero, or a control admitted.
**Do-nothing control:** the unchanged registry (control 1) scores 65; the cheapest "fill everything" fix (control 2) scores extra>0.
`dangling` counts only `source:`-header ids; the draft-package id `S243` in `request-limits-upstream-r31.md:33` is out of the rule
(not a row id, not on a `source:` line) and stays; this is disclosed, not a claim.

## Causal separability

C1 reads the new entry, its README row, rows S383-S390, `fetch/`, `frozen-tables.json` (c1). C2 reads `tools/mado-watchplan.py`,
`fixtures/c2*`, `ctl/`. C3 reads `corpus/knowledge/*.md` text and the `used-by` cells of `corpus/SOURCES.md`. C1 adds rows (S383-S390
`used-by` names the entry) and C3 edits other rows' `used-by`: each verifies without the other having landed (C3's counter at the base
plus C1's rows is still computed over whatever entries exist). Shared record files (README table, SOURCES.md, lesson, LOG, SCORECARD,
QUALITY) are integration surfaces, not claim evidence.

## Harm watch (frozen)

`bash tools/mado-verify.sh --selftest` stays `MADO_SELFTEST: 460/460 assertions passed` (baseline `receipts/selftest-before.txt`);
knowledge/index parity stays complete (70/70 → 71/71, never fewer); `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
stays exit 0 (`receipts/census-before.txt`); no config tree, compositor, service or sibling repo is written; the host is read only by
`hyprctl getoption|version`, `stat` and file reads.

## Mistake-fix item (inside §2b step 3; not a claim)

M56-1 (mined from round 55): the r55 C1 counter checked URL, status and tier of a K row's registry row but not that the registry
row's `anchor` covers the quoted line; K14 (S318 anchor `ConfigValues.cpp:271-279`, quoted line 280) and K17 (S052 anchor `:2573-2699`,
quoted line 2741) were admitted with the quoted line outside the cited anchor. Fix: leg `scope:<id>` (registration §C1), shown able to fail
by replaying the rule on the committed r55 entry at `63f48dc1` — 2 failures (`receipts/scope-replay-r55.txt`) — and by harness control 5.

## Exploratory claims

None. All three claims are counting claims.

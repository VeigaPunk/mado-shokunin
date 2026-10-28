# Round 55 w1 — seat R55ConnHistory report (failure-class coverage scan)

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`; base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`; freeze `54dacbd843d64ba744cd3f1bdc2ec622e5010039`. Leaf seat, no subagents. This is a draft: the L1 integrates, and no seat here is a non-author reviewer.

## 1. Result in brief

- Deliverable: `.ufo/waves/round-55/w1/R55ConnHistory/failure-classes.md` (the class table, 15 classes, the defects, the detector proposals, §5).
- Receipts: `.ufo/waves/round-55/w1/R55ConnHistory/receipts/` (7 files, listed in §5 below).
- Seven named classes (lead's list plus the M54-1..7 set). Caught by a frozen clause: none fully. Partly caught: quote normalization, pre-data freeze order, proposition (P23), host set, corpus gate. Open: self-attesting controls (the enforcer is absent at freeze), lexical forged context (declared limit), missing seat sidecars.
- Four contract defects reproduced or derived from the frozen text. They are for the L1 and are not edited here:
  - **D1**: QUALITY 64 fails at the freeze. Four named counter/checker paths are `MISSING` at `54dacbd`.
  - **D2**: C1's K17 row cannot pass `source_cell` as written. The wayland row S052 has no `efb50993` in its URL, and no new row covers it.
  - **D3**: C1-CTL-7 mutates `frozen-tables.json`, which trips `tables_sha`, not the named `pin_hash` leg.
  - **D4**: "no normalization" (C l.8–9) conflicts with the C3 `.strip()` equality (R l.120–121).
- One reproduced gap that the frozen counter would not catch: a K01 row with a false proposition passes every frozen per-row leg in my reconstruction (`receipts/leg-reconstruction-forged-row.txt`).

## 2. What I did (commands and decisive output)

All git verbs were read-only (`cat-file`, `show`, `ls-tree`, `log`, `archive`, `merge-base`), with `GIT_OPTIONAL_LOCKS=0`. No git mutation, no commit, no checkout, no index write. Scratch: `/fast/scratch/hyaku/mado-r55/R55ConnHistory/` (removed before yield, §6).

1. Read the lessons and QUALITY, then the contract:
   - `corpus/lessons/round-52.md:21`, `round-53.md` M53-1..4, `round-54.md:23–30` M54-1..7, `round-54-verifier-spotcheck.md` §§1–6.
   - `corpus/QUALITY.md` criteria 100–105 (lines 558–581; text read raw).
   - `claims-frozen.md` and `registration.md` in full.
2. Freeze tree and commit facts:
   - `git show -s --format='%H author=%aI committer=%cI' 54dacbd…` → `committer=2026-10-28T18:46:52-03:00`, `author=2026-10-27T15:22:20-03:00`.
   - Freeze paths: 94 files; dispatch-bearing paths (`dispatch|\.ready|swarm-registry|results`) = 0.
   - Round-54 freeze `350d30e`: `committer=2026-10-27T14:11:10-03:00`, `author=2026-10-27T13:42:45-03:00`; carries `.ufo/waves/round-54/w1-dispatch.json` (dispatch-bearing = 1).
   - Round-55 spec commit `dbc2eefe` `committer=2026-10-28T18:50:20-03:00`; `w1/swarm-registry.json` `createdAt: 2026-10-28T21:50:15.231Z`.
   - `git merge-base --is-ancestor 54dacbd… HEAD` → ancestor.
3. QUALITY 64 at the freeze (`receipts/criterion64-freeze.txt`): `MISSING quality/check-freeze-order.py`, `MISSING quality/check-r55-controls.py`, `MISSING quality/counters/c1-r55-kbd-entry.py`, `MISSING quality/counters/c3-r55-p19.py`.
4. Freeze verifier rerun: `git archive 54dacbd .ufo/waves/round-55` plus the round-52 C3 pin extracted to scratch; `python3 -I .ufo/waves/round-55/freeze-verify.py` (cwd = export) → `FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c889… OK`, rc 0; identical to the committed `receipts/freeze-verify.txt`. Also: `freeze-verify.py` reads the working tree with `open()` and its Q check is `L[line-1].strip() == quote`.
5. Leg reconstruction (`receipts/leg-reconstruction-forged-row.txt`; script `receipts/leg_reconstruction.py`; it reads base `corpus/SOURCES.md` from `git show 3b55b6e:corpus/SOURCES.md`):
   ```
   honest_row : PASS
   forged_row : PASS
   forged_prop_len: 121
   S052_url_has_commit: False S052_status: mined
   K17_row_legs_with_S052: FAIL source_cell:K17
   ```
   This is a reconstruction of the leg text from `registration.md` §C1, not the counter, which does not exist.
6. Registry for D2 (`receipts/sources-k17-wayland.txt`): the only `1.26.0/protocol/wayland.xml` row is `S052`; `grep -c efb50993` on it → 0; the row's status is `mined`.
7. Host (allowed reads only): `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j` → `40`, `250`, `1` (`set: true`), equal to `fetch/host-getoption.json`. `hyprctl version` → Hyprland 0.56.2 at `efb50993…`. `sha256sum ~/.config/hypr/input.conf` and the pin → both `3769c92a…`; `cmp` → identical bytes. (`receipts/host-live-reads.txt`.)
8. Criterion 64 applied to the round-54 freeze: the freeze commit itself carries the wave-one dispatch file, so the "freeze strictly before first dispatch" ancestry test fails, and the dispatch-bearing path check fails (`receipts/freeze-order-chronology.txt`).

## 3. Defects and ambiguities, with the input that shows each

- **D1** QUALITY 64 at freeze (4 `MISSING`, see §2.3). Also QUALITY 61: the registration's commands cannot run verbatim at the freeze. Effect: predicate text names files that do not exist at freeze, so they are seat data.
- **D2** K17 `source_cell`: R l.29 needs "URL … ends with the pin's `source_suffix` **and contains the frozen commit**"; K17 reuses S052 (`…/-/raw/1.26.0/protocol/wayland.xml`), which has no `efb50993` (§2.6). No S378–S380 row covers wayland (R l.52–53). Under the frozen text C1 cannot reach 18/18.
- **D3** C1-CTL-7 (R l.47) mutates `frozen-tables.json` and requires `pin_hash`; R l.33 `tables_sha` fires on that mutation, and R l.7–8 says counters "refuse" a tree whose tables differ (a setup refusal). The control's named leg cannot be the observed one unless the counter ignores `tables_sha`.
- **D4** C l.8–9 says "no normalization"; R l.120–121 and `freeze-verify.py` use `strip()` for Q rows; the strip set is undefined.
- **D5** Shared record: R l.52–53 has the L1 write S378–S380 at integration; C l.72–76 says shared record files are "integration surfaces, not claim evidence", yet C1's `source_cell` and `new_rows` legs read them. The per-K S-id is not frozen; the seat picks it (R l.22–27 format).
- **D6** Receipt list: C l.4 names only `before` and `census-before` as committed; `receipts/freeze-verify.txt` is committed and cited by R l.7–8.
- **D7** `w1.ready` is on disk (`.ufo/waves/round-55/w1.ready`, dispatch marker `w1.ready.dispatched` at 19:52) and absent from `HEAD`'s tree (`git ls-tree HEAD .ufo/waves/round-55/`). QUALITY 70 would flag it at closure; the contract is silent.
- **D8** `freeze-verify.py` reads the working tree (not git objects). R l.11–13 is stated for counters and harnesses only, so this is allowed, but the freeze receipt then attests the worktree. My export rerun matches.
- **Ambiguity A1** Chronology source: C l.3–6 says "BEFORE any wave `.ready`" and never says committer or author time. Round 54 shows the difference (`350d30e`, author 13:42:45, committer 14:11:10).
- **Ambiguity A2** Harm watch (C l.78–82) names `bash tools/mado-verify.sh --selftest` but not the runner or the receipt; round 54's closure ran it and withdrew it under PROTOCOL's gate-boundary rule.
- **Ambiguity A3** Host set: R l.24–28 `host:<id>` is a bare substring test. A commented copy of an H line would pass; the current pin is not affected (`host-input.conf:14,15,18` are uncommented).

## 4. Frozen-text coverage of the named classes (short form; detail in `failure-classes.md` §2–3)

| Class | Verdict |
|---|---|
| quote normalization (M54-3) | PARTIAL + CONFLICT (D4) |
| self-attesting controls (M54-6) | OPEN: enforcer absent at freeze; C1-CTL-7 conflict (D3) |
| pre-data freeze order (M53-4, M54-2, M54-4) | PARTIAL: round-55 order holds on git evidence; chronology source unnamed (A1); criterion 64 fails (D1) |
| lexical forged context (M52-1) | OPEN: declared limit (C l.32–34); reproduced in reconstruction |
| proposition not entailed by quote (M54-5, M53-3) | PARTIAL: P23 checked by tokens only (`p23` leg) |
| host-set mismatch (M54-1) | PARTIAL: per-row line/quote only (A3) |
| missing seat sidecars (M54-7) | OPEN: nothing in the frozen text; QUALITY 71/101/102 unreferenced |

Additional classes (corpus gate omission, stale status prose, sibling-gate run, routed-defect carry, unreachable predicate, judge visible to tool, prompt/attempt counts) are in `failure-classes.md` §3.

Cheapest detectors for each open class are in `failure-classes.md` §5. The most important one for the mistake-fix item: the planned `check-freeze-order.py` should check (a) no dispatch-bearing path in the freeze commit, (b) strict ancestry of freeze to the first dispatch-bearing commit, (c) committer time, and (d) the criterion-64 command. The round-54 freeze fails (a) and (b); round 55 passes (a)–(c) and fails (d) at its own freeze.

## 5. Deliverables and receipts

- `.ufo/waves/round-55/w1/R55ConnHistory/failure-classes.md`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/criterion64-freeze.txt`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/freeze-order-chronology.txt`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/freeze-verify-rerun-at-export.txt`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/leg-reconstruction-forged-row.txt`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/leg_reconstruction.py`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/sources-k17-wayland.txt`
- `.ufo/waves/round-55/w1/R55ConnHistory/receipts/host-live-reads.txt`

## 6. Not verified, not run, and scope notes

- **Not run**: no counter, harness, control or `tools/mado-kbdopts.py` (none exist at freeze or base). `tools/mado-verify.sh --selftest` was not run (gate boundary; the contract's harm watch is the L1's). Nothing was built or installed.
- **Not verified**: the round-55 w1 results and sidecars (wave in progress; `w1-results.json` absent), so the sidecar class is a design finding only.
- **Hold-out**: I did not look for `fixtures/c2-holdout` and did not open it. I did print the `holdout_dir` string and `holdout_commit_sha256` (`1275d7f8…`) from `frozen-tables.json` while reading the table. Those are a path and a commitment, not fixture bytes. Reported here as required.
- **Host reads**: the allowed reads only (§2.7). I did not read `~/.config/hypr/hyprland.conf` or any other config file, and did not run `hyprctl devices`. Whether another file sets the same keys is therefore unverified.
- **Tooling**: none installed, none updated (`~/.omp/agent/RULES.md` not needed for a read-only seat). No pacman or service action.
- **Scratch**: `/fast/scratch/hyaku/mado-r55/R55ConnHistory/` (freeze export, SOURCES copy, leg script copy). Removed before yield; the receipts above are in the deliverable directory. The leg script needs `corpus/SOURCES.md` from `git show 3b55b6e:corpus/SOURCES.md` to rerun.
- **Nothing written** in the lane outside `.ufo/waves/round-55/w1/R55ConnHistory/` and this report. No tracked file, no fleet-root file, no sibling lane.

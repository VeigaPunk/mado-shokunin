# ReviewControlsC2 — audit of the C2 control receipts (round-27, wave w2)

Seat: MadoR27.ReviewControlsC2, 2026-10-23. Read-only audit of `controls/K2*-seed*.txt` (16 files, counter v1)
and `controls/v2/K2*-seed*.txt` (17 files, counter v2), the 8 committed control suite pairs under `controls/`,
`controls/v2/L1-sealed-rescore-summary.txt`, and `c2/count-v2.py` / `c2/mutants-w.json` / `c2/heldout-seal.txt`.

Method: every receipt read (all 33 byte-distinct, sha256 cross-checked); counter v2 source read in full;
every control suite source read; every receipt-recorded sha256 re-hashed against disk; then each suite's
green/W behaviour **independently reproduced** from its committed bytes (pristine, both public benign edits on
each subject, all 15 W mutants applied) in a private mkdtemp under `/fast/scratch/hyaku/mado-r27/`, removed
afterwards. No lane file modified. No Hyprland started: coredump delta +0 (pre-existing count 1338). No tools
installed. `df -h /fast` checked before scratch use (68G free; only KB-sized scratch written and removed).

## Answers to the three assigned questions

**1. Two seeds each under v2 (counter sha `4dfb34b5…09d3`)? — NO: 8 of 9 controls, K2NormPin has one.**

All 17 v2 receipts print `counter c2-r27-v2 sha256:4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3`
= the frozen pin = the disk file (re-hashed). Every seed1/seed2 pair carries two distinct seeds, all at
rev `a4dc0da0` (commit exists; subject shas identical to v1 receipts' rev `5ddc5885`, i.e. the judged round-26
subjects are byte-identical across both revs — no same-identity drift):

| control | v2 seeds (receipts `controls/v2/`) | green | w_killed |
|---|---|---|---|
| K2DoNothing | seed1 `812fc7f5`, seed2 `ce5da8b8` | 0/8 | 0/15 |
| K2R26Suites | seed1 `71b8217b`, seed2 `f5b74e3b` | 3/8 | 12/15 |
| K2RejectAll | seed1 `fca0273e`, seed2 `b8c9a71b` | 0/8 | 15/15 |
| K2AcceptAll | seed1 `5f278066`, seed2 `7949e3a4` | 8/8 | 0/15 |
| K2ShaPin | seed1 `ae15ca79`, seed2 `b9be4979` | 2/8 | 15/15 |
| K2ASTPin | seed1 `7711d387`, seed2 `6694ed23` | 5/8 | 15/15 |
| K2WBlocklist | seed1 `af070cbf`, seed2 `e92887f1` | 3/8 | 15/15 |
| K2WBlocklistExact | seed1 `2f8cf093`, seed2 `f83c8551` | **8/8** | **15/15** |
| K2NormPin | **seed1 `85f3d364` only** | **8/8** | **15/15** |

`K2NormPin-seed2.txt` does not exist on disk, in `git log --all` history, or in commit `71d4ea7` ("K2NormPin
control (public and sealed)…", 2026-10-23 07:55, ancestor of tip), which added only `v2/K2NormPin-seed1.txt`,
the two suite files, the L1-summary line, and a `K2ASTPin.md` append. The kill rule (registration: "Each
control is scored with two seeds (M26-9)") is unmet for NormPin. Mitigating: NormPin is not one of the seven
controls the registration names (DoNothing, R26Suites, RejectAll, AcceptAll, ShaPin, ASTPin, WBlocklist); it is
the CritC2Counter attack made into a control, and the redesign its target-meeting forced (counter v2's sealed
rows) is already committed and does defeat it (see Q3). WBlocklistExact, also unnamed in the registration, did
get its two seeds.

**2. Does each suite honestly implement its shape? — YES, all nine, verified by source + reproduction.**

- DoNothing: no suite files; counter reports `quality/counter-selftest.py MISSING at REV` / same for B at both
  revs (true: the suites are new in round-27). Receipts: green=0/8, w=0/15. Honest base-state shape.
- R26Suites: suite A **is** the actual round-26 self-test (override path `.ufo/waves/round-26/quality/counter-selftest.py`,
  receipt sha `0754f501…` = disk today); suite B (`K2R26Suites-suite-b.py`) runs exactly the five round-26
  population fixtures comparing exit codes. B independently reproduced: 5/5 on every green state, kills exactly
  3/6 checker mutants; receipts' 12/15 total = 9 (A-side, not re-executed by me — see gaps) + 3. Honest.
- RejectAll / AcceptAll: literally `raise SystemExit(1)` / `raise SystemExit(0)` (43 B each, sha `cfe5ad0a…` /
  `29453a6f…`). Trivially honest; receipts match (0/8+15/15, 8/8+0/15).
- ShaPin (`3f41b8c6…`/`4478cdb9…`): hashes subject bytes against embedded pristine pins — the pins are exactly
  the three receipt SUBJECT shas, verified equal to the round-26 files on disk. No execution. Green 2/8
  (pristine rows only), w 15/15. Honest.
- ASTPin (`b1e7bd4f…`/`cd000383…`): compares `ast.dump(ast.parse(subject))` to embedded pins; module-level
  importlib PIN-CHECK: embedded pins == dumps of the committed subjects (True for c1, c2, checker). Comments
  invisible (passes comment edits), assignments visible (fails assign edits) → 5/8; w 15/15. Honest.
- NormPin (`84c8cb1e…`/`62bda895…`): normalization = drop docstrings + fixpoint-drop of unused assignments
  (`K2NormPin-suite-a.py:22-86`), compare normalized dumps; never executes a subject. PIN-CHECK: embedded pins ==
  `normalized_dump` of committed subjects. Passes both public benign edits (comment invisible; `_benign_*`
  assignment is unused → dropped) and kills all 15 W → 8/8, 15/15. Exactly the shape registration attributes to
  the CritC2Counter attack ("a normalised-source pin accepting all 8 public green runs and rejecting all 15 W
  mutants without executing a subject"). Honest.
- WBlocklist (`dbc34f3a…`/`ae38ee85…`): literal byte containment of each W mutant's `new` in subject source
  (`:58`), never executes. Embedded patterns verified byte-equal to `c2/mutants-w.json` (9 + 6 entries, all
  match by id, old and new). Honest. Its green=3/8 is a real property of the shape, not a bug: pristine c1
  contains `ok = gn == en` (the `new` of `c1-drop-bezier`), so **every** suite-A row rejects regardless of edits
  — its 15/15 is likewise degenerate (any A row dies). See F4.
- WBlocklistExact (`422880dd…`/`a5974473…`): fetches pristine bytes via `git show REV:<subject>` from the clone
  and rejects only when the subject is exactly the pristine with one W mutant applied (`:46`). Green runs can
  never match; each of the 15 W rows is by construction an exact transform → 8/8, 15/15. Honest; no
  path/env/process/timing sniffing anywhere in any suite (only the declared pins/blocklists/fixture runs).

Reproduction matrix (rc from committed bytes, my run) vs receipts — all consistent:
ShaPin A green `[0,1,1,1,1]` + B `[0,1,1]` = 2/8, kills 9+6; ASTPin A `[0,0,1,0,1]` + B `[0,0,1]` = 5/8,
kills 9+6; NormPin A all-0 + B all-0 = 8/8, kills 9+6; WBlocklist A all-1 + B `[0,0,0]` = 3/8, kills 15+6
(degenerate A); WBlocklistExact A all-0 + B all-0 = 8/8, kills 9+6; R26Suites-B 3/3 green, 3/6 checker kills.
Every receipt's printed numbers follow from the committed suite bytes.

**3. Did any v2 receipt meet green=all AND w_killed=15/15? — YES, three receipts; the sealed set separates
each, in different places.**

Structural note first: without `--heldout`, `h_valid=0` and the counter's `met` is false
(`count-v2.py:260-265`), so no v2 receipt can print TARGET_MET — the two-component question is the right lens.

- **K2WBlocklistExact seed1+seed2** (`controls/v2/K2WBlocklistExact-seed{1,2}.txt:31`): green=8/8, w_killed=15/15.
  L1 sealed rescore (`controls/v2/L1-sealed-rescore-summary.txt:6`): green=17/17 (the sealed benign rows also
  pass — they are not exact mutants), w=15/15, **h_killed=0/18**. → This control is separated from
  PRED-C2-r27-v2 **only by the sealed held-out mutant set** (0 < need ceil(0.75·18)=14). It already met
  green=8/8 + 15/15 under counter v1 (`controls/K2WBlocklistExact-seed{1,2}.txt:31`), so no public set ever
  separated it — the seal is genuinely the only thing that does.
- **K2NormPin seed1** (`controls/v2/K2NormPin-seed1.txt:31`): green=8/8, w_killed=15/15. Sealed rescore
  (`L1-sealed-rescore-summary.txt:10`): **green=8/17** (the 9 valid sealed behaviour-preserving edits break the
  normalized pin — they are not comments/unused assignments), h_killed=18/18. → NormPin is separated by the
  **sealed benign-green half** of the seal, not by H. This is exactly the v2 design sentence ("a pin of
  normalised subjects does not know them", `count-v2.py:15-16`) doing its job.
- No other control comes close: AcceptAll fails W (0/15); RejectAll/ShaPin/ASTPin fail green publicly while
  killing H (18/18); R26Suites fails both; DoNothing fails everything.

## Findings by severity

- **F1 (MEDIUM) — K2NormPin scored on one seed under v2.** Kill rule requires two seeds per control; only
  `v2/K2NormPin-seed1.txt` exists (no seed2 on disk or in history; commit `71d4ea7`). Since seed1 met
  green=all + w=15/15, a second seed is required before NormPin's public-set result is treated as stable.
  The committed sealed line already defeats it, so no claim currently rests on the missing seed — but the gap
  should be closed or NormPin's scope explicitly recorded.
- **F2 (MEDIUM) — the L1 sealed-rescore summary omits two controls.** `L1-sealed-rescore-summary.txt` has rows
  for ASTPin, AcceptAll, R26Suites, RejectAll, ShaPin, WBlocklistExact, before, and NormPin-sealed — but not
  for registered controls **K2DoNothing and K2WBlocklist**, although registration says the L1 "re-scores every
  C2 control with H after H is sealed". Full receipts are sealed under `/fast/scratch/hyaku/mado-r27/heldout-receipts/`
  (unreadable to this seat by role), so from the lane alone their h_killed is unverifiable. DoNothing's
  omission is harmless (trivially 0 everywhere); WBlocklist's is substantive — its substring blocklist would
  plausibly kill some held-out mutants, and its sealed row is exactly the comparison the summary exists for.
- **F3 (LOW) — NormPin's result lines are appended to K2ASTPin.md.** Commit `71d4ea7` appends to
  `w1/reports/K2ASTPin.md` the lines `green=8/8 b_valid=0 …` and `green=8/17 b_valid=9 … h_killed=18/18`. Those
  are **NormPin's** numbers (they match `K2NormPin-seed1.txt:31` and the NormPin-sealed summary row exactly);
  ASTPin's own numbers are 5/8 and 5/17. A future reader skimming the ASTPin report will misattribute them.
- **F4 (LOW) — WBlocklist's 15/15 is degenerate and its 3/8 green is self-inflicted.** Pristine c1 contains
  `ok = gn == en` (=`c1-drop-bezier`'s `new`), so every suite-A row rejects (`K2WBlocklist-suite-a.py:58`) no
  matter what is edited. Honest implementation of the declared shape, but it discriminates nothing on the A
  side; WBlocklistExact is the informative variant of the pair.
- **F5 (INFO) — two controls sit outside the registration's named list.** WBlocklistExact and NormPin are
  extras beyond the seven registered shapes. Both were scored like registered controls (Exact with two seeds
  both under v1 and v2; NormPin less thoroughly, F1). The registration text was never amended to name them —
  only the commit message and the L1 summary witness them.

## Verified integrity facts (receipts ↔ disk ↔ history)

- Counter identity: 17/17 v2 receipts print `4dfb34b5…09d3` (= disk file, = frozen pin); 16/16 v1 receipts
  print `2e180ed2…` (c2/count.py v1, retired). 16/17 v2 receipts at rev `a4dc0da0`; NormPin-seed1 at
  `b6650d58` (the L1's sealing-time rev); both commits exist; v1 receipts at `5ddc5885`.
- Subject identity: every receipt's three SUBJECT shas (`4ed70b54…`, `b92c32da…`, `803e0096…`) equal the
  round-26 files on disk today; W file sha `0ad0e46c…` in every receipt = disk.
- Override identity: all 15 receipt-recorded SUITE override shas (both waves) equal the control files on disk
  now — the audited bytes are the bytes that ran. R26Suites' suite-A identity `0754f501…` = the round-26
  selftest on disk.
- Anti-duplication: all 33 receipt files have distinct sha256s; every seed pair has distinct seeds; the
  counter derives benign-edit tags from `--seed` (`count-v2.py:145-147`) while run order comes from
  `os.urandom` (`:235`), so distinct-seed receipts differ in bytes but not verdicts — exactly what is observed.
- Counter mechanics as registered: `--no-local` clones (`:72`), per-run parent dirs, bwrap `--unshare-all`
  with tmpfs /home /fast /run /tmp, `--clearenv`, HOME/TMPDIR inside the run dir, `timeout 300`, RLIMIT_AS 4GB
  (`:100-104`); seal enforcement checks file set and per-file sha against `--seal` (`:202-210`);
  `c2/heldout-seal.txt` lists exactly 6 files (3 mutants + 3 `-benign`), consistent with h_valid=18 / b_valid=9
  in the sealed rows.

## Residual risk and verification gaps

1. NormPin seed2 absent (F1) — its public-set stability rests on one seed until landed.
2. Sealed full receipts (per-control held-out rows) are sealed by design; all sealed numbers here come from the
   committed summary rows and the `K2ASTPin.md` append, not from re-execution. F2 leaves DoNothing and
   WBlocklist without any committed sealed evidence.
3. R26Suites' suite-A side (the round-26 selftest killing 9/9 c1/c2 mutants) is taken from receipts plus file
   identity; I did not re-execute it — it runs the round-26 counters as subjects, which is Hyprland-adjacent
   and belongs inside the counter's sandbox, not in a review seat.
4. I did not re-run the bwrap-sandboxed counter end-to-end; suite-level reproduction plus full counter-source
   reading covers the audit questions without spending sandboxed runs.
5. The lane has advanced past the audited revs (HEAD `8e72db7`, C1 v4 receipts); the audited control artifacts
   are unchanged on disk (all shas re-verified today), but later commits could in principle move them —
   re-hash before relying on this report after further waves.

**Bottom line:** the C2 control set is honestly built and its receipts are genuine counter output that
independently reproduces from the committed bytes. Eight of nine controls have their two v2 seeds; NormPin has
one (F1). Three v2 receipts met green=all + w_killed=15/15 — **K2WBlocklistExact (both seeds), separated only
by the sealed held-out mutant set (h_killed=0/18), and K2NormPin (its single seed), separated by the sealed
benign green rows (green=8/17)** — which is precisely the separation the v2 sealed set was designed to provide.

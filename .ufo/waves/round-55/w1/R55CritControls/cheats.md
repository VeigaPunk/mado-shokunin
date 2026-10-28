# R55CritControls — cheats.md

Seat: R55CritControls (critic, controls). Scope: the C1 control design in `registration.md` §C1 (harness-held
expectations, scratch-repo mutation, legs), with the C2 hold-out and the freeze-order checker touched where the
same channel applies. Lab sources and receipts are in `lab/` next to this file (see §8).

## 0. What was run (and what is a model)

- Honest reference counter `lab/r55lab.py:check` implements `registration.md` §C1 as written, plus three readings
  recorded as ambiguities A3, A5, A6 in §4. It is the baseline every cheat is measured against.
- Harness-shaped runner `lab/check-r55-controls.py` builds the good tree and the seven frozen controls exactly as §C1
  describes: scratch single-commit repos from `git archive` of the good tree, committed as `ctl <ctl@ctl>`, under
  `--work`. The good run is on the lane-model repo at HEAD. **The real harness does not exist yet** (see §5 and the
  report), so the runner is my reconstruction. Its assumptions are A1–A4 in §4.
- The lane model `lab/lanemodel` (scratch, two L1-committed commits) is the frozen pins and tables from
  `git archive 54dacbd` plus a synthetic entry, README row and registry rows (S378–S380). It is not the real entry.
  It is only the input that lets the counter's legs be exercised.
- Probes P01–P12 are 12 non-control mutations (one or two per leg family) applied in clones of the lane model,
  committed with the L1 identity, and run as a direct predicate-style invocation (`--rev HEAD`, no harness parent).
  This is the test the seven frozen controls cannot pass by themselves: they only sample the mutation space.
- Every git call names `-C`. Every scratch repo was checked with `rev-parse --show-toplevel` before its first commit.
  The lane was read only (`log`, `show`, `ls-tree`, `archive`, `cat-file`, `rev-parse`); nothing was written to it.

Result summary (counts from `lab/matrix.txt`, `lab/receipts/`):

| # | Counter (file) | Channel | Harness: good / controls | Direct: probes caught / wrong leg / admitted | Stopped by contract? |
|---|---|---|---|---|---|
| 0 | `c_honest` | none (reference) | ok / 7/7 | 12 / 0 / 0 | n/a |
| 1 | `c_echo` | echo frozen-tables.json | ok / 0/7 | 0 / 0 / 12 | **STOPPED** by the controls |
| 2 | `c_green` | no check (baseline) | ok / 0/7 | 0 / 0 / 12 | **STOPPED** by the controls |
| 3 | `c_presence` | weak structural check | ok / 2/7 | 3 / 0 / 9 | **STOPPED** for the harness; probes show 9 admitted |
| 4 | `c_ppid` | parent-process sniff (`check-r55-controls` in `/proc/ppid/cmdline`) | ok / **7/7** | 0 / 0 / **12** | **NOT STOPPED** |
| 5 | `c_path` | repo path under `--work` (scratch-path detection) | ok / **7/7** | 0 / 0 / **12** | **NOT STOPPED** |
| 6 | `c_committer` | committer identity `ctl@ctl` | ok / **7/7** | 0 / 0 / **12** | **NOT STOPPED** |
| 7 | `c_history` | one-commit repo shape (scratch repo) | ok / **7/7** | 0 / 0 / **12** | **NOT STOPPED** |
| 8 | `c_cache` | prior-run cache keyed by `--rev` string | ok / **7/7** (sha revs) | 0 / 0 / **12** after a green run at HEAD, same `--work` | **NOT STOPPED** (conditional on `--rev` aliasing) |
| 9 | `c_mutkey` | keyed on the published control mutation text | ok / **7/7** | 0 / 0 / **12** | **NOT STOPPED** |
| 10 | `c_spot` | checks only the legs the seven controls can produce | ok / **7/7** | 1 / 1 / **10** | **NOT STOPPED** |
| 11 | `c_killsink` | attribution: prints every leg on any miss | ok / **7/7** | 12 "caught" only by listing all legs | **NOT STOPPED** (attribution is unchecked) |
| 12 | `c_forged` | consistent forgery: tree, tables and counter constant re-pinned together | FORGE-tree ok / **7/7** | forged tree: **TARGET_MET** | **NOT STOPPED** |
| 13 | expectation tamper (`c_green` + rewritten expectations) | harness expectations in a mutable file | ok / **7/7** with tampered expectations | n/a | **NOT STOPPED** |
| C2-a | lookup over export root (`c2_demo.py`, tool `mado-kbdopts-LOOKUP-ALL.py`) | argv lookup over every fixture dir in the export | holdout **8/8**, committed 18/18 | n/a | **NOT STOPPED** |
| F-1 | freeze-order checker (commit timestamps) | backdated committer date | n/a | n/a | **NOT STOPPED** (no control exists) |

"Direct" means the predicate's own counter line (`python3 -I quality/counters/c1-r55-kbd-entry.py --repo . --rev <rev>`),
which is what PRED-C1-r55 requires to print `TARGET_MET` in addition to the harness verdict. Every row above with
"12 admitted" prints `TARGET_MET` on a tree that contains a defect. A row can be green on the harness and on the
predicate's counter line at the same time. Only the harness's 7/7 is counted, so PRED-C1-r55 passes for those rows.

## 1. The core finding: the harness only ever sees bad trees in its own environment

Channels 4–8 and 13 share one shape. The harness runs the counter in one environment (a child of the harness, a
scratch path, a one-commit repo with a `ctl` committer). The predicate runs the counter in another (a direct call on
the lane, with lane history and the L1 identity). The contract's good=ok run is only on the unmutated tree. So a
counter can branch on the environment and be honest only for the harness, and the harness still reports 7/7.
The 12 probes committed in the lane's own shape (L1 identity, lane history, a non-`--work` path, a direct parent)
are all admitted by those counters.

This is not fixed by re-running the good tree inside the harness: a path/history/committer cheat is honest on the
good tree too and still green on every real bad tree. The fix is structural (§7, fix 1): the controls must be
exercised in the predicate's own invocation shape, and the counter must be invariant under environment (fix 2).

## 2. Per-channel notes

**Channel 1, echo the frozen tables (`c_echo`).** Green iff `frozen-tables.json` hashes to the embedded constant; it
never reads the entry. The harness catches it at 0/7. Stopped.

**Channel 2, baseline no-op (`c_green`).** Also 0/7. Stopped. It is the control that makes the harness meaningful:
the seven controls are not vacuous against a trivially green counter.

**Channel 3, weak structural presence (`c_presence`).** Checks entry existence, the trio, one row per id and the
index. The harness catches 2/7 (`entry_absent`, `row:K17`). It misses the quote, anchor, source, host and pin controls.
Probes P01–P05 and P09–P12 are admitted, which is the same gap in a different form: the frozen controls do not
measure detection of non-control defects. Stopped for the harness; not stopped as a claim.

**Channel 4, parent-process sniffing (`c_ppid`).** Honest iff the parent command line contains
`check-r55-controls`. The harness is the parent, so the controls get the honest verdict. A direct call gets green.
**Not stopped.** The contract does not forbid environment branching; it says only "a counter never prints a control
verdict".

**Channel 5, scratch-path detection (`c_path`).** Honest iff `--repo` is under `--work`, which is where the harness
builds its controls. The lane is not under `--work`, so the lane gets green. **Not stopped.** The contract puts controls
under `--work` and never says a counter must not know that.

**Channel 6, committer identity (`c_committer`).** Honest iff the head commit's committer email is `ctl@ctl`, which
the contract writes out in §C1 ("committed with `-c user.name=ctl -c user.email=ctl@ctl`"). Anyone who reads
registration.md has the sniff string. **Not stopped.**

**Channel 7, scratch-repo shape (`c_history`).** Honest iff `git rev-list --count` is 1. Harness controls are
single-commit by construction; the lane has history. **Not stopped.**

**Channel 8, prior-run cache (`c_cache`).** Persists the verdict in `--work` keyed by the `--rev` string. With sha
revs (what the runner uses) the harness never hits the cache and stays 7/7. A direct run at `--rev HEAD` after a green
run at HEAD with the same `--work` returns the stale green line for all 12 probes. The contract says `--rev <rev>` and
`--work <scratch>` but does not require a sha or a fresh `--work`. **Not stopped**, conditional on symbolic revs or
reused work dirs. I did not run a HEAD-form harness; that is unverified.

**Channel 9, keyed on published mutation text (`c_mutkey`).** Greps for the seven control signatures (e.g.
`REPEATRATE) ;`, `:1219`, `| S316 |` on the K10 row, `repeat_delay = 300`, a missing K17 row, an entry absence, an
IKeyboard.cpp pin tamper). Green otherwise. 7/7 on the harness. All 12 probes admitted. The signatures are in
registration.md §C1 (public text), and the seven mutations are frozen and fixed, so the counter can be written
from the registration alone. **Not stopped.** The contract has no hold-out for C1; C2 has one, C1 does not.

**Channel 10, spot-check (`c_spot`).** Computes the honest check but reports only the legs the seven controls can
produce. 7/7 on the harness. Direct: P10 (pin tamper on a non-control pin, caught because the spot list includes all
pin hashes), P05 reported as `source_cell:K10` rather than `new_rows` (wrong leg), and 10 admitted. **Not stopped.**
This is the most important practical gap: a counter that checks exactly the controls' sites passes the harness.

**Channel 11, attribution (`c_killsink`).** Detection is honest. On any miss it prints the whole leg universe. The
harness's check is "required leg appears in `missed=`", so this passes 7/7 and catches all 12 probes by the same test.
The harness cannot tell an attributed verdict from a list-all verdict. **Not stopped**, low detection impact, but it
makes the "named leg" check vacuous as an attribution test.

**Channel 12, consistent forgery (`c_forged`).** Changes `Hyprland-ConfigValues.cpp`'s line 277 default from `false` to
`true` (the frozen pin, which is not anchored to upstream, has `false`), updates the pin sha in `frozen-tables.json`, the K15 quote in
the table and entry, and re-pins the counter's constant to the new tables sha. On that forged tree, the counter
prints `TARGET_MET` and the harness reports 7/7. **Not stopped.** Nothing anchors pins, tables or the counter to the
freeze commit or upstream: every counter reads its own tree (`--rev`), and the constant lives in the counter that
is in that same tree. The only anchor is git ancestry, which no counter reads.

**Channel 13, expectation tampering (`c_green` + rewritten expectations).** My runner takes expectations from a
file (`--expect`). Rewriting all seven to `TARGET_MET` with the no-op counter gives `controls=7/7 verdict=OK`
(`lab/receipts/harness-tampered-green.log`). In the contract, the harness is not frozen (see §5): `quality/` at
`54dacbd` contains no r55-named file, so there is no committed byte to compare against.

**C2-a, hold-out lookup over the export root.** The contract's three frozen controls include `lookup-committed.py`,
which only reads `fixtures/c2`. Against a simulated hold-out in the export tree, the frozen control correctly scores
0/8, but a lookup over every `fixtures/c2*` directory in the export root scores 8/8 hold-out and 18/18 committed. So
the frozen control does not test the attack the hold-out exists to stop. The contract's only defence is the text
"reads only the files named by `--config` and `--getoption`", which nothing enforces. Isolation works: the same
lookup copied with no fixtures above it scores committed 1/18 (F17, empty argv, prints the usage line the
fall-through prints, a coincidence) and hold-out 0/8. **Not stopped** unless the harness runs the tool from a tree
that contains no fixtures.

**F-1, freeze-order checker.** The mistake-fix item says `quality/check-freeze-order.py` must fail on the round-54
evidence (freeze `350d30e4` 14:11:10 vs registry `createdAt` 14:05:25). Commit timestamps are caller-chosen:
`GIT_COMMITTER_DATE=2026-10-27T09:00:00-0300 git commit` produces a committer date of 2026-10-27 09:00 in a scratch repo
(`lab/receipts/extra-demos.txt`). There is no frozen control for this checker, so the contract cannot stop a
checker that trusts commit dates. **Not stopped.**

## 3. What the seven frozen controls do and do not cover

The seven C1 controls each change one site. They prove that a counter reports one leg for one mutation at one
location. They do not prove that the counter checks the other 17 K rows, six H rows, the other pins, the source
cells of the other K rows, or the new-row count beyond one shape. Probes P01–P12 are exactly that gap. Only the
honest reference catches all 12; every cheat that passes 7/7 fails at least 9 of them except the attribution one.

C3 was **not built** (see §6). The same structure applies: its six controls each touch one Q row, the P23 cell, the
README line or the prefix. A spot-check of those exact sites passes all six [INFERENCE, unrun].

## 4. Contract defects and ambiguities (with the input that shows each)

- **A1 — harness location and environment are unspecified.** `claims-frozen.md` says the predicate runs
  `python3 -I quality/check-r55-controls.py --claim c1 --repo . --rev <rev>`. The harness is invoked by a relative
  path, so it is read from the working tree; nothing says it is read from git objects at `--rev`. The counter is
  exported from `--rev` only by default. The good tree is run
  "in the lane"; controls "in a scratch git repo". The contract does not say the controls are run in the lane's
  environment. (Input: `registration.md` §C1 controls paragraph; `claims-frozen.md` PRED-C1-r55.)
- **A2 — expectations live in the harness, which is not frozen.** `registration.md` says the harness "holds the
  expected verdicts itself"; the freeze commit `54dacbd` adds `ctl/`, `fetch/`, `fixtures/c2/`, `receipts/`,
  `freeze-verify.py`, `frozen-tables.json`, `claims-frozen.md`, `registration.md` and nothing under `quality/`.
  `git ls-tree -r --name-only 54dacbd -- quality tools | grep -i r55` returns nothing (receipts:
  `lab/receipts/extra-demos.txt`).
- **A3 — `host:<id>` cannot fire under the literal reading.** `registration.md` §C1 says `host:<id>` is "a H row
  whose quote is not a substring of that line of the committed host pin". Read against the frozen quote, the leg
  is unreachable: the frozen quote is always a substring of its own pin line. Input: the first lab run (before the
  reading change) produced `C1-CTL-6 ... missed=quote:H02` only, so control 6 failed. I used the row-cell reading.
  The two readings disagree on C1-CTL-6.
- **A4 — "named leg" is not exclusive.** The harness check (`controls=<k>/7`) is presence of the leg in `missed=`.
  A counter that prints every leg passes all seven (`c_killsink`, 7/7). The contract's "the counter must print
  `TARGET_MISSED` and the named leg" can be read as exactly that leg; the contract does not say.
- **A5 — the `tables_sha` leg contradicts "refuse".** `registration.md` §C1 says "Counters embed that sha256 as a
  constant and refuse a tree whose frozen-tables.json differs", and also defines `tables_sha` as a leg. For control
  C1-CTL-7 the tables do differ, and the required leg is `pin_hash`. A counter that "refuses" (setup exit 2, no
  missed line) fails C1-CTL-7 for the wrong reason. The honest reference continues and prints
  `missed=tables_sha,pin_hash`. Which one is meant is not stated.
- **A6 — `source_cell` rule is unsatisfiable for K17 as written.** `registration.md` §C1 says a K row's S-id must be
  a registry row "whose URL ends with the pin's `source_suffix` and contains the frozen commit". K17 cites S052
  (wayland), and S052's URL is `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`,
  which does not contain `efb50993…`. The same registration reuses S052 for K17. The honest reference needs a
  waiver (the URL must contain `1.26.0` for `wayland-*` pins); I documented it in `r55lab.py`. Without a waiver the
  good tree cannot be TARGET_MET, so this is a real choice the L1 must make, not a detail.
- **A7 — "no `|` inside a cell" cannot hold for K16.** The frozen K16 quote is
  `if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())`, which contains `||`. A markdown table splits on `|` even
  inside backticks, so the row has more than five cells and a naive counter reads the quote as truncated. The lab
  builder asserted on this before the workaround (join the tail cells). Input:
  `frozen-tables.json` `c1.k` K16 quote. A counter written to the spec's grammar fails its own good tree, which
  creates pressure to weaken the quote check.
- **A8 — `freeze-verify.py` checks the working tree, not the freeze commit.** It sets `LANE = os.getcwd()` and reads
  every pin, quote and fixture from `open(f"{W}/...")`. Its output proves internal consistency of the checkout, not
  that the tables match the freeze commit or upstream. It is in the freeze commit (`100644 blob 1403cecc…`), but
  its checks are not anchored to git objects.
- **A9 — hold-out commitment base is unspecified.** `holdout_commit_sha256` is "over, for each file in sorted
  relative-path order, the line `<relpath>\0<sha256>\n`", with no base for `<relpath>` (the fixtures dir, or the lane
  root). A seat cannot check it before reveal, so the wrong base would only surface at integration.
- **A10 — `--rev` form and `--work` reuse are unspecified.** The contract does not require a sha and does not
  require a fresh `--work` per run. That is the precondition for channel 8.
- **A11 — C1 entailment is out of scope by declaration.** `claims-frozen.md` says the counter does not prove
  that a proposition is entailed by its quote. That is declared, so it is not a defect, but it means the probes
  above are the only check on the counter's own sites; a wrong proposition can pass.

## 5. Harness, counter and controls are not frozen

Checked: `git ls-tree -r --name-only 54dacbd843d64ba744cd3f1bdc2ec622e5010039 -- quality tools | grep -i -E 'r55|kbdopt|controls|freeze-order'`
prints nothing (exit 1). The freeze contains `ctl/*.py` (the C2 controls) and `freeze-verify.py`, but not the C1
or C3 controls, the C1/C3 counters, the harness, `tools/mado-kbdopts.py` or `check-freeze-order.py`. Those are
written by the wave and will be committed at integration. Consequence: channels 4–8, 12 and 13 act on files that
are candidate-side, with no frozen bytes to compare.

## 6. Not built, not verified

- **Time sniffing.** No time-dependent path is needed by any counter, and the only date literal (`verified-at:
  2026-10-28`) is part of the contract. A date-gated counter would pass the same-day harness. Not built [INFERENCE].
- **Environment variables.** No env var is set by the contract's harness, so an env-based cheat needs the harness
  to set one; the contract does not. Covered in principle by channels 4–7. Not built.
- **Reading the harness's expected legs from the tree.** The legs are the same public text as the mutations
  (`registration.md` §C1 table). A counter reading them adds nothing beyond `c_mutkey`. Not built separately.
- **Parser ambiguity: multi-line output.** The contract says the counter prints one line, but not what the harness
  does with two lines. A counter that prints a green line then a miss line is parsed by my runner as the last line.
  Not built; the same class as channel 3.
- **C3 counter and controls.** Not built (the wave's C3 counter does not exist at this commit). Expected to fall to
  the same spot-check and environment channels [INFERENCE, unrun].
- **C2 tool.** The real `tools/mado-kbdopts.py` is not in the lane at `54dacbd` and I did not write one. The C2 channel
  above is shown with a lookup stand-in and a simulated hold-out, not the real hold-out. **The sealed hold-out was not
  looked for or used.** `fixtures/c2-holdout/` does not exist in the lane at the freeze, and I did not read it.
- **The real harness.** Not available. `lab/check-r55-controls.py` is my reconstruction. Results on the real harness
  may differ in details A1–A6.
- **The real entry.** The lane model uses a synthetic entry. The honest reference is checked against it only, not
  against the scribes' text (not read).

## 7. Recommended control design (smallest fixes that close the channels above)

1. **Run controls in the predicate's own environment.** Build control trees by committing the mutation on top of the
   lane's history with the lane's identity, from a clone that sits where the lane sits, and invoke the counter with
   the predicate's exact argv shape and parent. Do not allow the harness to be the parent of the controls (A1).
   Channels 4–8 then see the same environment as the probe run.
2. **Make the counter environment-invariant and test it.** The counter must not read its parent, its path, its
   committer or its commit count. Add a harness check that runs the same tree in two environments and requires the
   same verdict (channels 4–8).
3. **Sample the mutation space, not seven sites.** Keep the seven frozen controls, and add a seeded random sample of
   defects over all K/H rows, pins, source cells and new rows, with the seed sealed like the hold-out and the
   expected leg computed by the harness, not the counter (channels 9, 10; probes P01–P12 show the gap).
4. **Require exact legs.** `missed=` must equal the expected set for each control (C1-CTL-7 may add `tables_sha`),
   not contain it (channel 11, A4).
5. **Freeze the harness, the counters and the constants, and anchor them to the freeze commit.** The harness, the
   counters, `tools/mado-kbdopts.py` and `check-freeze-order.py` must be in the freeze, or hashed in it. The
   counters read their pins and tables from `git show <freeze>:...`, not from `--rev` alone (channels 12, 13, A2, A8).
6. **Fix the contract text.** Decide A3 (`host:` reading), A5 (refuse vs leg), A6 (wayland commit waiver), A7 (the
   K16 pipe), A9 (commitment base) and A10 (`--rev` form and `--work` freshness). Each one is a place where a seat
   can pick the reading that passes.
7. **C2: run the tool with no fixtures above it.** Copy the tool, the args and the config/getoption inputs into an
   empty tree before the run, and put the hold-out somewhere the tool cannot reach by path (C2-a).
8. **Freeze-order checker: anchor to git objects, not timestamps.** Compare the freeze commit's tree hash and the
   wave's `.ready` blob, which are not writable after the fact (F-1). Add a control for it, since the mistake-fix
   item is part of the claim set.

## 8. Files

- `lab/r55lab.py` — honest reference C1 check, lane-model builder, mutators, control builder.
- `lab/check-r55-controls.py` — harness-shaped runner (7 frozen C1 controls; `--expect` for tamper demo).
- `lab/driver.py` — builds the lane model, forged tree and probes; runs every counter under harness and direct.
- `lab/counters/c_*.py` — 13 counters: honest, echo, green, presence, ppid, path, committer, history, cache, mutkey,
  spot, killsink, forged.
- `lab/c2_demo.py` — C2 hold-out lookup demo (simulated hold-out).
- `lab/expect-tampered.json` — tampered expectation file used in channel 13.
- `lab/matrix.txt`, `lab/receipts/*` — the run outputs (`direct-<counter>.txt` per probe, `matrix.json`,
  `harness-*.log`, `extra-demos.txt`).

The counters import `r55lab` from the absolute scratch path
`/fast/scratch/hyaku/mado-r55/R55CritControls/lab`, which is removed before this seat yields. To re-run, copy `lab/` back
to that path and run `python3 -I driver.py`.

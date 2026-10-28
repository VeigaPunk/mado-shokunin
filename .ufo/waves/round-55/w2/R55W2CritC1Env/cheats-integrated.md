# R55W2CritC1Env — C1 cheats against the INTEGRATED harness

Seat: R55W2CritC1Env (critic, environment and consistency channels). Scope: `quality/check-r55-controls.py --claim c1`
with `quality/r55_ctl_c1.py`, and `quality/counters/c1-r55-kbd-entry.py`, at the scored revision
`57584ed67716340b3d466fa04333ac0bab3fb79e` (an ancestor of lane HEAD `721ba9c1`). Replaces the w1 reconstruction
(`w1/R55CritControls/cheats.md`) for C1 only.

## 0. What ran and what did not

- Harness and honest counter were copied from the rev with `git show` and blob-verified (ids below). They ran as
  a scratch copy (`harness/quality/`), so no `__pycache__` was written into the lane. The lane was read only:
  `git show`, `ls-tree`, `cat-file`, `rev-parse`, `clone --no-hardlinks` (source read only). No lane file was changed.
- Blobs at `57584ed`: `quality/check-r55-controls.py` a61d5c28…, `quality/r55_ctl_c1.py` 55f944be…,
  `quality/counters/c1-r55-kbd-entry.py` 53ec8a1a…, `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md` 303ced16…,
  `.ufo/waves/round-55/frozen-tables-v2.json` d67e20c4….
- Each cheat is the honest counter, byte-identical up to its `if __name__` guard, plus an injected `check()` override
  (`cheat-blocks/cheat_<name>.inject.py`; reconstruct with `honest + inject + main guard`). The honest `main()` calls
  `check()` as a global, so the override is the only change. Counter SHA-256s are in `receipts/counter-sha256.txt`.
- Harness runs: `python3 -I <scratch>/harness/quality/check-r55-controls.py --claim c1 --repo <lane> --rev 57584ed… --work <fresh> [--counter <cheat>]`.
  Outputs: `receipts/harness-<name>.out|.err`.
- Direct runs (predicate shape): `python3 -I <counter> --repo <tree> --rev <sha> --work <fresh>`, cwd outside the lane,
  all `GIT_*` variables removed from the environment. Outputs: `receipts/direct-raw.txt`, `receipts/direct-matrix.tsv`.
- Real-looking trees: a `--no-hardlinks` clone of the lane (472 commits of history) detached at `57584ed`, plus one
  defect commit:
  - D1 `d1-spliced`: K04 `std::max(0, REPEATRATE) ;` (the published control-2 text), committed as `ctl`.
  - D2 `d2-dropK09`: K09 row deleted (not a published control), committed as `ctl`.
  - D3 `d3-pin-cv`: `Hyprland-ConfigValues.cpp` pin with one trailing space (non-control pin), committed as `ctl`.
  - D4 `d4-dropK09-laneid`: D2 content committed with the lane's own identity `mado-shokunin <mado@shokunin.local>`.
    **Deviation:** the seat rule says fixtures use `ctl`. The committer channel is only non-trivial when the head committer
    is not `ctl`, so D4 is the one fixture with a different identity. It is a scratch clone; the lane was not touched.
  - FORGE `forge`: consistent forgery (section 3).
- Not run: the C2/C3 harnesses and counters (out of scope); any live hyprctl command (not needed for C1).

## 1. Result table

Harness column = `controls=<k>/7` from `receipts/harness-<name>.out`. Direct columns = the counter's own line on each
real-looking tree, with `TARGET_MET` meaning the cheat admitted the defect (only D1–D4 are defects).

| cheat (channel) | harness (k/7) | direct: lane good | D1 spliced K04 | D2 drop K09 | D3 pin CV space | D4 drop K09, lane id | E9 declares it? |
|---|---|---|---|---|---|---|---|
| green (baseline, no check) | 0/7 | MET | MET (admitted) | MET (admitted) | MET (admitted) | MET (admitted) | n/a (sanity) |
| ppid (parent `check-r55-controls`) | **7/7** | MET | **MET** | **MET** | **MET** | **MET** | yes ("sniffs its environment") |
| path (repo under `dirname(--work)`) | **7/7** | MET | **MET** | **MET** | **MET** | **MET** | yes |
| env (`GIT_CONFIG_GLOBAL=/dev/null`, set by the integrated `_env`) | **7/7** | MET | **MET** | **MET** | **MET** | **MET** | yes |
| committer (`committer ctl <ctl@ctl>`) | **7/7** | MET | MISSED quote:K04 | MISSED row:K09 | MISSED pin_hash | **MET** | yes |
| history (`rev-list --count` == 1) | **7/7** | MET | **MET** | **MET** | **MET** | **MET** | yes |
| cache (verdict cached by `--rev` string) | **7/7** (sha revs) | MET | see 2.3 | see 2.3 | see 2.3 | see 2.3 | yes ("caches runs") |
| mutkey (keyed on published control text) | **7/7** | MET | MISSED quote:K04 | **MET** | **MET** | **MET** | yes ("keys on mutation text") |
| spot (only the seven control legs) | **7/7** | MET | MISSED quote:K04 | **MET** | MISSED pin_hash | **MET** | not named (umbrella only) |
| killsink_generic (adds non-failing generic legs on miss) | **7/7** | MET | MISSED +5 generic legs | MISSED +5 generic legs | MISSED +4 generic legs | MISSED +5 generic legs | not named |
| killsink_ids (adds every row id's legs on miss) | **1/7** | MET | MISSED +ids | MISSED +ids | MISSED +ids | MISSED +ids | n/a (closed by harness) |
| FORGE (consistent forged tree, forged counter) | **7/7** | n/a | n/a | n/a | n/a | `TARGET_MET` on the forged tree | yes ("forges a consistent tree") |
| expectation tamper (committed counter swapped for green; harness `judge_control` forced to accept) | **7/7** with tampered harness; 0/7 with committed harness | n/a | n/a | n/a | n/a | n/a | not named |

Column notes: "MET" in the D columns = `verdict=TARGET_MET missed=none` printed for a tree with a defect. The honest
counter on the same trees prints `TARGET_MISSED` with the leg in the table of section 2.0 (`quote:K04`, `row:K09`,
`pin_hash`, `row:K09`). The FORGE column for the non-forged counters is not used: the matrix runs them with the lane's
counter on the forged tree (`tables_sha`), which is a mismatch artefact, so only the forged-counter run counts (section 3).

### 2.0 Honest reference on the same trees (for the table above)

| tree | honest verdict (direct) | harness (honest counter) |
|---|---|---|
| lane good | TARGET_MET missed=none | controls 7/7 |
| D1 spliced K04 | TARGET_MISSED missed=quote:K04 | — |
| D2 drop K09 | TARGET_MISSED missed=row:K09 | — |
| D3 pin CV space | TARGET_MISSED missed=pin_hash | — |
| D4 drop K09, lane id | TARGET_MISSED missed=row:K09 | — |

The honest counter sees every defect; the harness with the honest counter gives 7/7 (controls
`missed=` legs: entry_absent; quote:K04; anchor:K01; source_cell:K10; row:K17; quote:H02,host:H02; pin_hash,tables_sha).

### 2.1 Environment and shape cheats (ppid, path, env, committer, history)

- Each is honest inside the harness and green outside it. The harness passes the counter the same shape every time:
  parent = `check-r55-controls.py` (its own cmdline), `--repo` under `c1h-*/repos`, `--work` = `c1h-*/cwork-*`,
  `GIT_CONFIG_GLOBAL=/dev/null`, one-commit repo, head committer `ctl <ctl@ctl>`. Each cheat keys on one of those.
- **New in the integrated harness: the env channel.** The w1 reconstruction said no env var was set. The integrated
  `_env` sets `HOME`, `TMPDIR`, `LC_ALL=C.UTF-8`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_TERMINAL_PROMPT=0` for the counter. `GIT_CONFIG_GLOBAL` is not set in an ordinary shell here (checked with
  `env | grep GIT_`: only `GIT_EDITOR`, `GIT_PAGER` and `GIT_TERMINAL_PROMPT` are set in this shell. `GIT_TERMINAL_PROMPT=0` is
  therefore **not** a usable marker (it is set here); the env cheat keys on `GIT_CONFIG_GLOBAL` alone.
- Four of the five (ppid, path, env, history) admit all four defects on direct runs: the cheat never looks at content, and
  every defect differs from the good tree only in content.
- Exception: committer on D1–D3 is honest, because those fixtures carry the `ctl` identity the cheat keys on. It is
  admitted only on D4 (the lane identity). A committer cheat is therefore caught on any defect committed with the
  harness identity; it is admitted on any defect committed by anyone else.

### 2.2 Mutation-text keyed (mutkey) and the spot-check

- mutkey greps the entry and the IKeyboard pin for the seven published control signatures and is green otherwise.
  Harness 7/7 (every control carries its published text). It catches D1 (the published K04 text) and admits D2, D3, D4
  (unpublished). Its signature list is public: `REPEATRATE) ;`, K01 `:1219`, K10 `| S316 |`, H02 `repeat_delay = 300`,
  no K17 row, entry absent, IKeyboard pin trailing space.
- spot computes the honest verdict and reports only the seven control legs (`entry_absent`, `quote:K04`, `anchor:K01`,
  `source_cell:K10`, `row:K17`, `host:H02`, `pin_hash`). Harness 7/7 (C1-CTL-6 then reports `host:H02` only, still
  "contains" the required leg). Admits D2 and D4 (row K09), catches D1 and D3 (pin_hash is a generic leg, so any pin).

### 2.3 Cache keyed by the `--rev` string

- Harness: 7/7 at sha revs, because the harness gives every run a fresh `cwork-*` under a fresh `c1h-*`, and a sha
  never repeats. The cache is never read by the harness.
- Direct, symbolic rev, same `--work` (log: `receipts/cache-experiment.txt`):
  1. clone at `57584ed`, `--rev HEAD`, cache cheat: `rev=HEAD … verdict=TARGET_MET missed=none` (correct).
  2. clone moved to D2 (K09 dropped), `--rev HEAD`, same `--work`: `rev=HEAD … verdict=TARGET_MET missed=none` — **stale green, admitted**.
  3. honest counter at HEAD (D2), fresh work: `rev=HEAD rows=17/18 … verdict=TARGET_MISSED missed=row:K09` (correct).
  4. cache cheat with D2's sha (`rev=6ccf4343…`), same `--work`: `TARGET_MISSED missed=row:K09` — the cache misses on sha.
  So the cache channel is live only for symbolic revs with a reused `--work`. It is not reachable through the harness.

### 2.4 Killsink variants

- killsink_generic (on any miss, add `provenance,index,new_rows,pin_hash,tables_sha`): harness 7/7, because the harness
  checks only that the required leg appears in `missed=` and checks row/anchor/quote/source/host IDs against the mutation's
  owned rows. The five generic legs are never owned-checked. Direct: the verdict is honest (MISSED), so the cheat does
  not admit defects; it breaks attribution. Declared? E3 says "reports EVERY failing leg per row", but a generic leg that
  is not failing is not excluded by any text, and the harness does not exclude it.
- killsink_ids (on any miss, add `row/anchor/quote/source_cell` for all 18 K and `row/anchor/quote/host` for all 6 H):
  harness **1/7**. Controls 2–7 fail with `leg row:K01 names a row the mutation did not touch`. This is the owned-row check
  in `judge_control`, and it closes the ID form of the A4 shotgun. Only control 1 passes (no owned check when the entry
  is absent).

### 2.5 Expectation tamper

- Committed harness, always-green counter (`cheat_green` via `--counter`): `controls=0/7 verdict=FAIL` (exit 1).
- Harness copy with `judge_control` forced to `return None` (one line, `receipts/` has the stderr), same counter:
  **`controls=7/7 verdict=OK`** (exit 0).
- The harness file that runs is the working-tree file (`python3 -I quality/check-r55-controls.py` in
  `claims-frozen.md`). The expectations (`CONTROLS` table, `judge_control`) are not in the freeze, so an edit to the
  candidate tree changes the verdict. Not declared in E9.

## 3. Consistent forgery (FORGE)

Commit `c9f30bb0` on the clone (`forge`):
- `Hyprland-ConfigValues.cpp` line 277: `..., "Engage numlock by default.", false, {` → `…, true, {` (one line changed).
- `frozen-tables-v2.json`: `c1.pin_sha256["Hyprland-ConfigValues.cpp"]` `a76f0507…` → `b1779a6f…`; K15 quote `…, false` → `…, true`
  (file re-serialised with `json.dumps(indent=2)`, which the harness does not care about).
- entry K15 row: `…, false\`` → `…, true\``.
- `quality/counters/c1-r55-kbd-entry.py`: `TABLES_SHA256` `13d6e2f9…` → `071be0bac67190d256dd0d4ed55b93fde30de63505d87e6c5015fb39cfa3ef0e`.
- Result: `check-r55-controls --claim c1 --repo <forge> --rev c9f30bb0…` → `good=ok controls=7/7 verdict=OK` (receipts
  `harness-forge.out`). The forged counter direct: `rev=c9f30bb0… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`.
  The forged claim ("Hyprland's numlock default is true") is false against the frozen pin (`Hyprland-ConfigValues.cpp` line 277
  is `false`, fetched at `efb50993`), and the harness accepts it. Nothing in the harness reads the freeze commit (`5a43d67f` for
  v2 tables, `54dacbd8` for the v1 pins) or the counter bytes at any earlier commit.

## 4. Proposed harness changes (text only; nothing implemented)

Each line: the smallest change that stops the channel, and whether E9 declares the channel.

1. **Sniffed shape (ppid, path, env, committer, history) — invariance across shapes.** The harness also runs every
   good tree and every control in the predicate's own shape: `sh -c 'env -i PATH=… HOME=… python3 -I <counter> --repo <clone>
   --rev <sha> --work <fresh-dir-outside-the-harness>'` from a cwd outside the harness tree, and requires the two verdict
   lines to be byte-equal. The harness varies what the cheats key on between its two shapes: committer name/email drawn
   per run (never `ctl`), repo path inside and outside `--work`, one-commit and lane-history variants of each control, and
   no `GIT_CONFIG_GLOBAL` marker or a random marker. Any counter that branches on those differences disagrees and fails.
   *E9 declares this family* ("a counter that sniffs its environment … passes the harness"). The proposal narrows it: after
   the invariance test, a sniffer must find a feature the harness does not vary.
2. **Cache (symbolic rev, reused `--work`).** The harness asserts `--work` is empty before a run and contains only the
   counter's `selftest-*` directories after it (the counter writes nothing else). Also: rerun invariance — the same
   symbolic rev is run on a mutated tree in the same `--work`, and the verdict must follow the tree. *E9 declares this*
   ("caches runs").
3. **Mutation-text keyed (mutkey) and spot-check.** Replace the seven fixed controls by a seeded sample over all 18 K rows,
   6 H rows, the pins, the source cells and the new-row count. The seed is hashed in `claims-frozen.md` (pre-data), the
   harness computes the expected legs from the mutation (never from the counter), and missed must equal the expected set.
   *mutkey: E9 declares it* ("keys on mutation text"). *spot: not named by E9; the umbrella sentence does not cover a
   counter that is correct at the seven sites.*
4. **Killsink (generic shotgun).** Make the check exact: `missed=` must equal the expected set (required legs plus the
   per-control allow-list of collateral legs that E6 and E3 define: `tables_sha`, `quote:`, `host:` for C1-CTL-7; the honest
   two-leg `quote:H02,host:H02` for C1-CTL-6). A generic leg outside the allow-list fails the control. The ID form is
   already closed by the owned-row check (2.4). *Not named in E9.*
5. **Forgery (consistent tree).** The harness reads `frozen-tables-v2.json` and the pins from the freeze commits
   (`git show 5a43d67f:…`, `git show 54dacbd8:…`), not from `--rev`, and requires the rev's blobs to be identical to them
   (else `tables_sha` / `pin_hash`). The counter's own `TABLES_SHA256` constant is then irrelevant. The counter bytes
   themselves stay candidate-side: a forged counter that ignores the tables still needs a sha256 of the counter pinned
   before the data, which the wave cannot produce retroactively. Honest limit: a counter rewritten at a new rev is not
   detectable by this harness without a frozen counter hash. *E9 declares this* ("forges a consistent tree").
6. **Expectation tamper.** The predicate runs the harness from the freeze commit's blob (`git show <freeze>:quality/check-r55-controls.py`
   piped to `python3 -I -` with `r55_ctl_c1.py` likewise), or the harness and its `CONTROLS` table are hashed in
   `claims-frozen.md` and the harness refuses to run if its own bytes differ. *Not named in E9.*

## 5. Where the w1 cheats.md stands against the integrated harness

- Still open and reproduced: ppid, path, committer, history, cache (sha-keyed run closed; symbolic rev open), mutkey,
  spot, forgery, expectation tamper. Reproduced under the real harness at 7/7 each.
- Closed: the ID form of the killsink (A4 shotgun) by the owned-row check (1/7). A3 (`host:` unreachable) is closed by the
  list-all reading: the honest counter reports `quote:H02,host:H02`, and C1-CTL-6 needs `host:H02`.
- New: the `GIT_CONFIG_GLOBAL` env marker (section 2.1). The w1 harness did not set env vars; the integrated one does.
- Forgery is now demonstrated under the real harness, not only under the w1 reconstruction.

## 6. Declared limits (registration-v2.md E9) against the reproduced channels

E9 text: "declared limit: a counter that sniffs its environment, keys on mutation text, caches runs or forges a consistent
tree passes the harness … the harness is evidence against a counter that prints green without work, not against an
adversarial one."

| channel | E9 declares it? | basis |
|---|---|---|
| ppid, path, env, committer, history | yes | "sniffs its environment" (E9 cites R55CritControls cheats.md channels 4–8) |
| cache | yes | "caches runs" |
| mutkey | yes | "keys on mutation text" |
| FORGE (consistent tree) | yes | "forges a consistent tree" |
| spot-check | no, only by the umbrella "not against an adversarial one" | a counter correct at the seven sites is not a "green without work" counter |
| killsink (generic) | no | E3 "reports EVERY failing leg"; non-failing generic legs are unaddressed |
| killsink (ID) | n/a | closed by the owned-row check |
| expectation tamper | no | the harness is candidate-side; E9 is silent |

Of the 11 cheat channels reproduced (excluding the green baseline and the ID shotgun, closed), E9 declares 8: the five shape/env
sniffs (ppid, path, env, committer, history), the cache, mutkey and forgery. Spot-check, the generic shotgun and expectation
tamper pass the harness and are not named.

## 7. Not verified

- Only the harness wrappers were run; a real attacker would hide the sniff. The verdicts show the harness does not look,
  not that a hidden sniff is impossible.
- Cache is conditional on symbolic revs with reused `--work` (confirmed directly; the harness never reaches it).
- D4 uses the lane identity, a deliberate deviation (section 0).
- Forgery: one forgery (ConfigValues numlock default). A second forgery on a pin the harness reads at control time was
  not built.
- C2 and C3 channels (the same family, different tools) were not run.

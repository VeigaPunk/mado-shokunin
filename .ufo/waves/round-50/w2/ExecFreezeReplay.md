# ExecFreezeReplay — round 50 w2 (FALSIFY) — freeze-command replay at the landed tip

**Seat:** `ExecFreezeReplay` (executor). **Lane:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.
**Attack revision:** `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip).
**Scratch:** `/fast/scratch/hyaku/mado-r50/ExecFreezeReplay/` (deleted at the end of the seat).
**Receipts:** `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/` (22 files, `01-` … `21-`, incl. `07b-`).

## Method

One `--shared` clone of the lane checked out at the attack revision; `git rev-parse --show-toplevel`
asserted equal to the clone dir before any run; every counter/selftest read the clone, never the lane
tree. `HOME`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` and `TMPDIR` all
under the seat scratch (`env.sh` in the scratch); `ulimit -f 65536` on every writer shell. The lane tree
was not mutated: `git status --porcelain` in the lane is unchanged from the pre-seat snapshot, and the
fleet root (`/home/vgpnk/Projects/shokunin`) is clean.

The C1 counter reads the live compositor socket (`hyprctl binds -j`, `hyprctl getoption
input:resolve_binds_by_sym -j` — read-only), so its clause f/r results depend on the live bind table.
It reproduced the pinned digest exactly (`sha=9a47199e2297`, `binds=192`), and the pinned live receipt
regenerated **byte-identically** (`receipts/17-`), so the live surface did not drift since the capture.

## Verdict per command

| # | command | rev | verdict |
|---|---|---|---|
| 1 | `c1-r50-bind-entry.py` (data run) | `906178b6` | **PASS** — body byte-identical to `receipts/c1-at-data.txt` (sha `5b0b47ad…`), final line `…admitted=1/1 verdict=TARGET_MET`, rc 0 |
| 2 | `c2-r50-session-gate.py`, nonce **50117** | `906178b6` | **PASS** — body byte-identical to `receipts/c2-at-data-nonce50117.txt` (sha `b8e66761…`), `red=42/42 green=44/44 … verdict=TARGET_MET`, rc 0 |
| 3 | `c2-r50-session-gate.py`, nonce **778899** | `906178b6` | **PASS** — body byte-identical to `receipts/c2-at-data-nonce778899.txt`, `red=44/44 green=41/41 … verdict=TARGET_MET`, rc 0 |
| 4 | `c2-r50-session-gate.py`, fresh nonce **739214** | `906178b6` | **PASS on verdict**, but see **F3**: the final line is `red=44/44 green=42/42`, not either registered nonce's pair |
| 5 | `c1-r50-bind-entry.py` | tip `b4a79843` | **PASS** — identical to the data-rev body apart from the `rev=` token, rc 0 |
| 6 | `c2-r50-session-gate.py`, nonce 739214 | tip `b4a79843` | **PASS** — `verdict=TARGET_MET`, rc 0; gate bytes at the tip are the same `ffdc9d62…` |
| 7 | `check-session-material.py --selftest` | installed bytes | **PASS** — `passed=94/94 failed=0`, rc 0 |
| 8 | `mado-hostguard.py --selftest --work <scratch>` | installed bytes | **PASS** — `MADO_HOSTGUARD_SELFTEST: 45/45 passed`, rc 0 |
| 9 | `check-wave-done.py --selftest --work <scratch>` | installed bytes | **PASS** — `MADO_WAVE_DONE_SELFTEST: 58/58 passed`, rc 0 |
| 10 | `check-wave-done.py --round 50` | tip `b4a79843` | **PASS** — `WAVE wave=w1 … seats=54 dispatched=54 settled=54 verdict=OK` / `MADO_WAVE_DONE: round=50 waves=1 settled=1 verdict=OK`, rc 0 |
| 11 | `check-wave-done.py --round 49` | tip `b4a79843` | **PASS** — `seats=45 dispatched=45 settled=45 verdict=OK` / `MADO_WAVE_DONE: round=49 waves=1 settled=1 verdict=OK`, rc 0 |
| 10b/11b | the same two at their **receipted** revs (`8dbbf61a` / `906178b6`) | — | **PASS** — identical to `receipts/wave-done-r50.txt` / `wave-done-r49.txt` |
| 12 | `sources-census.sh validate --root … mado` | lane tip | **PASS** — stdout byte-identical to `receipts/census-after.txt` (sha `1141437f…`), exit 0; see **F5** for the receipt's shape |
| 13 | `check-axis-scores.py --repo <clone> --rev 8ae47b95` | base | **PASS** — byte-identical to `receipts/axis-base.txt` |
| 14 | do-nothing controls, frozen counters | — | **PASS** — C1 controls `c00/c13/c12` all `TARGET_MISSED` rc 1; C2 controls `c00/c12/c14` all `TARGET_MISSED` rc 1; C2 bodies byte-identical to `receipts/controls-c2.txt` after masking the fixture revs |
| 15 | `make-receipt.py` (live bind receipt) | — | **PASS** — regenerated receipt is byte-identical to `receipts/binds-live-r50.txt` (sha `9f16e5a5…`) |
| 16 | `check-state-cite.py --claims claims-r50.txt` (from `check100-r50.txt`) | tip | **FAIL — command does not reproduce** (**F2**) |
| 17 | `check-deliverables.py --file .ufo/waves/round-50/w1/*.md` (from `check101-w1.txt`) | tip | **FAIL — exit code mismatch** (**F1**); the `absent=4` rows it counts are correct findings, matching the L1's M50-5 |

**C1 kill rule:** not triggered. The final line at `906178b6` is exactly the registered TARGET_MET
sentence; every control reads `TARGET_MISSED`.
**C2 kill rule:** not triggered at the two registered nonces. Both reproduce byte-for-byte; every
control reads `TARGET_MISSED`. The nonce-sensitivity in **F3** is a calibration defect in the kill-rule
formulation, not a kill at the registered nonces.

## Findings

### F1 — `receipts/check101-w1.txt` records `exit=0` for a command that exits 1 (receipt defect)

`receipts/check101-w1.txt` ends:

```
CHECK101: reports=54 declared=19 exists=15 absent=4 undeclared=49 verdict=FAIL
exit=0
```

Re-running the receipted command at the tip (`python3 -I quality/check-deliverables.py --file
.ufo/waves/round-50/w1/*.md`, cwd = clone root) reproduces the summary line **exactly**, but exits
**1**: `quality/check-deliverables.py:149` is `return 0 if fail == 0 else 1` and `fail = absent + … = 4`.
The same exit-1 holds in the lane working tree, so the discrepancy is in the receipt, not the clone.
Receipt `15-`.

The `exit=0` line is reproducible as a **pipeline-capture artefact**: running the command through a
`tee`-style pipe yields `rc=0` (measured: `python3 … | tee /dev/null >/dev/null; echo $?` → `0`,
versus `1` for the same command unpiped), so a receipt written from a piped capture records the
pipe's exit status, not the instrument's. The receipt is therefore **not** evidence that the
instrument passed — and its own `verdict=FAIL` line says the opposite.

The 4 `absent=4` rows are **correct findings, not instrument false positives** (corrected after
re-reading the instrument's documented rule, `quality/check-deliverables.py:13-16` and `candidates()`
at `:56-64`): the report `.ufo/waves/round-50/w1/MutC1Tool.md` declares `MutC1Tool/make_mutants.py`,
`MutC1Tool/run_one.sh`, `MutC1Tool/hash-ledger.md`, `MutC1Tool/receipts/BASE.txt` — each already
prefixed with the seat name. The instrument resolves a path containing `/` seat-dir-relative first,
producing `.ufo/waves/round-50/w1/MutC1Tool/MutC1Tool/<file>`, which does not exist; the second
candidate is the path as written, which also does not exist at the repo root. The files themselves sit
at `.ufo/waves/round-50/w1/MutC1Tool/<file>` (verified with `test -f`), i.e. the **declaration is
malformed** (seat-name prefix where the instrument expects a seat-dir-relative path) — the defect is
the seat's, exactly as the L1 recorded it as **M50-5** in `corpus/lessons/round-50.md:97`. Declaring
`make_mutants.py` instead resolves to the real file (verified: `candidates('make_mutants.py', seat)`
→ `.ufo/waves/round-50/w1/MutC1Tool/make_mutants.py`, exists). This finding therefore agrees with the
L1's M50-5 and adds only the exit-code defect above.

One further property of the receipt, worth recording because the summary line is otherwise
un-auditable: the receipt shows only **5** `DECLARATION` rows and **0** of the 4 `status=ABSENT`
rows it counts in `absent=4` (a full run emits 68 `DECLARATION` rows, 4 of them ABSENT). All 5 rows
the receipt does show are byte-identical to rows of a full run (checked with `grep -Fxq`). So the
receipt is an abridged capture that omits the very rows its own summary counts — the 4 ABSENT
declarations are absent from the receipt.

### F2 — `receipts/check100-r50.txt` names a command that does not reproduce from the committed tree

The receipt's own command line is:

```
# cmd: python3 -I quality/check-state-cite.py --claims claims-r50.txt --source .ufo/waves/round-50/fetch
```

`claims-r50.txt` exists **nowhere in the lane at any revision**: `git ls-tree -r b4a79843 | grep
claims-r50` → no match; a `find` over the lane worktree → no match. The file survives only at
`/fast/scratch/hyaku/mado-r50/L1Final/claims-r50.txt`, i.e. in the L1's scratch, which is not citable
evidence and was scheduled for deletion. Running the receipted command at the tip therefore dies with
`FileNotFoundError: … 'claims-r50.txt'` and exits **1**, not the recorded `exit=0`. Receipt `14-`.

The receipt's *measurement* is sound and reproducible: reconstructing the claims file from the
receipt's own `STATE_CLAIM` lines reproduces the receipt body **byte-for-byte**
(`STATE_CLAIM claim=r50-sym-state-zero-mods … verdict=OK` ×3 + `CHECK100: claims=3 set=3 readonly=0
unresolved=0 contradicted=0 verdict=OK`), and so does running against the L1's scratch copy of the same
file. So this is a **provenance defect in the receipt** (an unlanded input), not a wrong result.

### F3 — the C2 TARGET_MET sentence is nonce-dependent, so the kill rule is not nonce-invariant

`quality/counters/c2-r50-session-gate.py:475-476`:

```python
k_red   = MIN_REPOS + (abs(args.nonce) % 5)          # MIN_REPOS = 40
k_green = MIN_REPOS + ((abs(args.nonce) // 7) % 5)
```

The counts in the final line are a pure function of the nonce, so the "TARGET_MET sentence" the
registration's kill rule pins (`… red=42/42 green=44/44 scope=seen verdict=TARGET_MET`, and
`red=44/44 green=41/41` for the second nonce) is only exact for those two nonces. Measured on six
nonces at `906178b6`:

| nonce | red | green | verdict |
|---|---|---|---|
| 50117 (registered) | 42/42 | 44/44 | TARGET_MET |
| 778899 (registered) | 44/44 | 41/41 | TARGET_MET |
| 739214 (fresh, this seat) | 44/44 | 42/42 | TARGET_MET |
| 424242 | 42/42 | 41/41 | TARGET_MET |
| 515151 | 41/41 | 43/43 | TARGET_MET |
| 606060 | 40/40 | 40/40 | TARGET_MET |

The nonce-invariant part of the predicate is `selftest=94/94 names=69/69 scope=seen verdict=TARGET_MET`.
A third-party verifier running any unregistered nonce gets a different final line and, under the
registration's literal kill rule ("any receipt not exactly the TARGET_MET sentence at `906178b6…` for
both nonces"), would falsely read it as a kill. Recommendation for the L1: restate the kill rule over the
nonce-invariant tokens, or pin the count pair to each nonce.

### F4 — `.ufo/waves/round-50/fetch/SHA256SUMS` lists itself with a stale digest; `sha256sum -c` fails in the pin dir

`sha256sum -c SHA256SUMS` inside the pin directory reports `SHA256SUMS: FAILED` /
`WARNING: 1 computed checksum(s) did NOT match` (rc ≠ 0). The failing line is the manifest's own
self-entry:

```
recorded in file : bb21f728cd1c6f1c59af9ecee0f0bf8360b42bb581985d12ab66611210054d07  SHA256SUMS
actual file digest: e2b9110664074ab4d4089c2cd046236a1b2537e766b7b30c464a904ff791ff0d  SHA256SUMS
```

The recorded value was never correct: the blob was committed once (`1b37a59e`) and never changed, and
`git show 1b37a59e:…/SHA256SUMS | sha256sum` gives the same `e2b91106…`. A self-listing checksum line
can never satisfy `sha256sum -c`. The other **15/15** digests are exact, and the registration's
companion claims hold: the directory holds **16 files**, and all **14 upstream pins are byte-equal to
their round-49 copies** (`cmp -s` on each; `binds-live-r50.txt` is the one round-50-only file). The
registration names `SHA256SUMS` in that directory as the pin-verification artifact, so the standard
verification command for it fails. Receipt `21-`. (The hostguard receipt manifest at
`.ufo/waves/round-50/w1/ExecHostGuardR50/receipts/SHA256SUMS` does **not** self-list and verifies clean —
the convention the pin manifest departs from.)

### F5 — `receipts/census-after.txt` drops the `exit=0` line its sibling `census-before.txt` carries

`receipts/census-before.txt` is 20 lines ending `… /mado-shokunin/corpus/SOURCES.md` + `exit=0`;
`receipts/census-after.txt` is 21 lines and ends at the `ok` line with **no** `exit=` line. The stdout
itself is exactly right — my re-run at the lane tip is byte-identical to the committed file (sha
`1141437f6952c7e078e09eff368a687507bfb2c41da4521bad7eb27dc6b9d068`). Only the recorded exit code is
missing. Round-49's own `census-before.txt` and `census-after.txt` both carry `exit=` lines, so this is
a round-50 shape regression, not a house style. Note also that the census command is **worktree**-
addressed, not rev-addressed (it reads `corpus/SOURCES.md` from disk, unlike the counters): the lane
working tree's `corpus/SOURCES.md` is byte-identical to the tip blob (`b3a1a041d4a9ce0c2555f028ce415bac5a4b1a0e38bf782e730cbb24ddf52744`), so the tip-scoped result is unaffected by the uncommitted `corpus/lessons/round-50.md` edit. Receipt `12-`.

### F6 — four round-50 receipts are UNTRACKED at the tip

`git ls-tree -r b4a79843 -- .ufo/waves/round-50/receipts` contains 12 files; the lane working tree has
16. Untracked at the tip: `check100-r50.txt`, `check101-w1.txt`, `operator-state-after.txt`,
`selftests.txt`. The last one is the receipt carrying the three selftest numbers the registration's D7
line leans on ("selftest 45/45 re-run at the installed path this freeze"), so the *committed* freeze
does not carry the selftest evidence the freeze text cites. All three selftests reproduce exactly
(receipt `07-`), so this is a landing gap, not a measurement gap.

### F7 — round-50's `w1-results.json` is 54/54 null outputs; the wave-done "settled=54" is the lossy note clause

`python3` over `.ufo/waves/round-50/w1-results.json` at the tip: `seats=54 results=54
null_output=54 null_with_note=54`, all carrying the same run-9 wrap-up note. The wave-done gate treats
`output: null` + non-empty `note` as **settled (lossy)** (`quality/check-wave-done.py:64`), which is why
command 10 reads `settled=54 verdict=OK`. Round-49's file, by contrast, has `null_output=0` of 45 — the
registration's D2 claim ("0 nulls of 45") is **verified true**. So the r50 wave-done receipt attests 54
settled seats of which **none** has a retained output. The registration already declares the loss
("`w1-results.json` arrived with null outputs, so w1 was integrated from the committed seat reports"),
so this is a declared residual restated with the measured counts, not a new defect. Receipt `13-` and
this section.

### F8 — `quality/check-wave-done.py` at the tip differs from its w1 prototype (expected, noted for completeness)

`cmp` shows `quality/check-wave-done.py` ≠ `.ufo/waves/round-50/w1/ScrQualityR50/check102-wave-done.py`
(1134 diff lines; the installed file is the hardened, documented round-level gate, the prototype is the
seat's criterion-102 candidate). `check-state-cite.py`, `check-deliverables.py` and
`mado-hostguard.py` are byte-identical to their w1 prototypes. Consistent with the registration's
"w1/ScrQualityR50 prototypes" wording for the first two; noted so the L1 does not read the
`check-wave-done.py` difference as drift.

### F9 — a stray untracked file `.ufo/wakes` sits in the lane tree (sibling seat's artifact; NOT mine to delete)

`.ufo/wakes` (388 bytes, mtime 2026-10-27 05:57:30) is a **file**, not a directory — almost certainly a
typo for `.ufo/waves`. Its content is a two-command `check-index.py` transcript whose full-width
counterpart lives correctly at `.ufo/waves/round-50/w2/RevN4Tip/index-base-vs-tip.txt`; the two differ
only in the abbreviated rev tokens and a blank line, so it is that seat's earlier draft. This seat never
ran `check-index.py` (`grep -rl check-index` over `w2/ExecFreezeReplay/` → no hits) and did not create
it. It is left in place because it belongs to another seat and deleting another seat's artifact is out
of scope; flagged so the integrator removes it before committing round 50, since `.ufo/wakes` would
otherwise land as a tracked file at a misspelled path. It does not affect any freeze command (no
instrument reads `.ufo/wakes`).

## Frozen-artifact digests re-derived at the tip

Every sha256 the registration's frozen-artifact table names was re-derived from the tip blob
(`git show b4a79843:<path> | sha256sum`):

| artifact | registration | re-derived at tip | match |
|---|---|---|---|
| `corpus/knowledge/hyprland-bind-key-match-r50.md` | `ae8f8d4de6fa8ede…` | `ae8f8d4de6fa8ede452423095942ee9f2182efdbab79c02744271c6fb0016977` | ✔ |
| `corpus/lessons/round-50.md` | `e7cd29620aeed655…` | `e7cd29620aeed655f54fa3401b901acba8fe3f47ffdb4b5e9d6f3a62e20be794` | ✔ |
| `corpus/SOURCES.md` | `b3a1a041d4a9ce0c…` | `b3a1a041d4a9ce0c2555f028ce415bac5a4b1a0e38bf782e730cbb24ddf52744` | ✔ |
| `quality/check-session-material.py` | `ffdc9d62c387050e…` | `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61` | ✔ |
| `quality/check-wave-done.py` | `10f4359ac0af755a…` | `10f4359ac0af755a4e7bcb1959233862fcde4d1bc895806409b7ea1b054f818c` | ✔ |
| `quality/check-state-cite.py` | (prototype) | `822912fc7b0d08b5ba19c4f825e14c54e4fbe7be40e0599927ab6a3e748afe8c` | ✔ (== w1 prototype) |
| `quality/check-deliverables.py` | (prototype) | `6fe0a4b4122762dc0ea456c9ad44b35d66458c0d9c60672727d7f2d7d042e88f` | ✔ (== w1 prototype) |
| `tools/mado-hostguard.py` | `fdaa5c2ec297ebfd…` | `fdaa5c2ec297ebfdddc1238d0dfe693ba0ae75ed2310939843cf14b024b7b47e` | ✔ |
| `.ufo/waves/round-50/receipts/binds-live-r50.txt` | `9f16e5a5ce7fe39f…` | `9f16e5a5ce7fe39fc30cd8a6041fcdf733f7b794f20310796bae09d01ae51590` | ✔ |
| `quality/counters/c1-r50-bind-entry.py` | `e162d6717915f558…` | `e162d6717915f5585c40853afa8223d0398e50f0de37da4fd02004d2b08a84c0` | ✔ |
| `quality/counters/c2-r50-session-gate.py` | `1d52a62cd969aba5…` | `1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298` | ✔ |

## Host-guard and safety notes

- Every counter/selftest ran with `HOME`/`XDG_*`/`TMPDIR` under the seat scratch; the C1 counter's own
  `live_binds()` additionally sandboxes `HOME`/`XDG_*` into a `mkdtemp` under `TMPDIR`
  (`quality/counters/c1-r50-bind-entry.py:1069-1110`) and keeps only `XDG_RUNTIME_DIR` and
  `HYPRLAND_INSTANCE_SIGNATURE`.
- No `pacman` transaction; no tool installed or upgraded (nothing in this seat needed a new tool).
- Compositor reads only: `hyprctl binds -j`, `hyprctl getoption input:resolve_binds_by_sym -j`
  (via the counter) and `hyprctl version` (via `make-receipt.py`). No dispatch, keyword, reload,
  setprop, switchxkblayout, batch, output, plugin or kill call. No GUI program launched, no input
  injected.
- Operator-owned host state re-measured read-only (digest+size+mtime of the four paths the lane's own
  receipt names) and **identical** to `receipts/operator-state-after.txt`; `~/.local/bin` entry count
  still 103. Receipt `20-`.
- No receipt in this seat dir carries an absolute home path or the account name; the home directory is
  written as `~`. The census tool's own stdout prints the absolute path, so receipts `12-` and `16-`
  are masked (`/home/<user>` → `~`) and each carries the **unmasked** sha256 in its header:
  `1141437f6952c7e078e09eff368a687507bfb2c41da4521bad7eb27dc6b9d068` for receipt `12-`, which is exactly
  the committed `receipts/census-after.txt` sha256 — byte-equality with the committed receipt stays
  checkable by hash. Verified with `grep -rn -e '/home/<user>' -e '<account>'` over the whole seat dir:
  0 hits.
- The lane tree was not mutated; `git status --porcelain` in the lane shows only the pre-existing
  untracked w2 files plus my seat directory. The fleet root is clean.
- The scratch directory `/fast/scratch/hyaku/mado-r50/ExecFreezeReplay/` was deleted at the end of the
  seat; every receipt quoted above was copied into the seat dir first.

## Deliverables (all present, `test -f` verified)

- `.ufo/waves/round-50/w2/ExecFreezeReplay.md` (this report)
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/01-c1-at-data.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/02-c2-at-data-nonce50117.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/03-c2-at-data-nonce778899.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/04-c2-at-data-nonce739214-fresh.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/05-c1-at-tip-rev.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/06-c2-at-tip-rev.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/07-selftests-gate-hostguard-wavedone.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/07b-selftests-abridged-vs-committed.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/08-wave-done-r50-at-tip.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/09-wave-done-r49-at-tip.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/10-wave-done-r50-at-receipted-rev.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/11-wave-done-r49-at-receipted-rev.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/12-census-validate-at-lane-tip.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/13-axis-base-repro.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/14-check100-r50-repro-FAIL.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/15-check101-w1-repro-exitcode-mismatch.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/16-census-validate-at-base-state.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/17-binds-live-r50-regen.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/18-controls-c1-rerun.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/19-controls-c2-rerun.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/20-operator-state-after-repro.txt`
- `.ufo/waves/round-50/w2/ExecFreezeReplay/receipts/21-FINDING-fetch-SHA256SUMS-self-entry-mismatch.txt`

## Risks / limits

- The C1 counter's clauses f and r read the live compositor socket. They reproduced the pinned digest
  exactly this run, but they are by design sensitive to a bind-table change between capture and score
  (a miss in that case, by the counter's own statement).
- The C2 red/green fixture counts are nonce-derived (F3); a replay at an unregistered nonce cannot be
  compared to the registered receipts by string equality.
- The census command reads the lane **working tree**, not a commit; the result here is tip-valid only
  because `corpus/SOURCES.md` is byte-identical in the worktree and at the tip blob.
- The control fixture revs in a fresh clone are new commits, so their hashes differ from the committed
  receipt's; comparison was made on the clause lines and verdicts, not on the rev token.
- `check101`'s 4 `ABSENT` rows are **correct** findings (F1) — the MutC1Tool seat declared
  seat-name-prefixed paths; they agree with the L1's M50-5. The receipt defect is the `exit=0` line
  and the abridgement (5 of 68 `DECLARATION` rows shown, the 4 `ABSENT` rows omitted), not the
  instrument's verdict.

## What the L1 should do

1. **Do not admit `receipts/check101-w1.txt` as-is**: its `exit=0` contradicts the instrument's exit 1
   (a piped-capture artefact, measured). The `absent=4` rows are **correct** — they are the MutC1Tool
   declaration defect already recorded as **M50-5** (`corpus/lessons/round-50.md:97`), so keep that
   finding; only the exit line and the abridgement need fixing: the receipt shows 5 of 68
   `DECLARATION` rows and none of the 4 `ABSENT` rows its summary counts. Re-capture the receipt
   unpiped, with the full output, so a reader can audit `absent=4` from the receipt itself.
2. **Do not admit `receipts/check100-r50.txt` as-is**: its command names an input (`claims-r50.txt`)
   that is not committed anywhere. Land the claims file (e.g. under
   `.ufo/waves/round-50/w1/ScrQualityR50/fixtures/`) and re-point the receipt's command at it.
3. **Restate the C2 kill rule** over the nonce-invariant tokens (`selftest=94/94 names=69/69
   scope=seen verdict=TARGET_MET`), or pin the `red=/green=` pair to each registered nonce (F3).
4. **Fix the pin manifest**: drop the self-entry line from `.ufo/waves/round-50/fetch/SHA256SUMS` (or
   exclude the manifest from its own check) so `sha256sum -c SHA256SUMS` exits 0 in the pin dir (F4).
5. **Land the four untracked receipts** (`check100-r50.txt`, `check101-w1.txt`,
   `operator-state-after.txt`, `selftests.txt`) so the freeze's own evidence is in the freeze (F6), and
   add the `exit=0` line to `census-after.txt` for shape parity with `census-before.txt` and with
   round-49 (F5).
6. **Remove the stray `.ufo/wakes` file** before committing round 50 (F9): it is a file at a
   misspelled path, created by another seat (RevN4Tip's draft), and would otherwise land tracked. This
   seat did not create it and did not delete it.
7. **No action needed** for C1 or C2 on the merits: the two counter data runs, all three selftests, both
   wave-done checks, the census, the axis check, both control sets and the live-receipt regeneration all
   reproduce exactly at the tip.

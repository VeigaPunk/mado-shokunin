# ExecWaveDone — round-50 w1 — `check-wave-done.py` (round-49 D2, mistake fix)

Lane `mado-shokunin`, base `8ae47b957034ae21012bbf09173cca2c48be345e`, claims at `13631f24050f22db92bf5bd33e0f4d014192992e`.
Seat scope: build the gate that makes round-49 defect D2 mechanical — a report filed with 7 w1 seats unsettled and no
WAVE-DONE (`corpus/lessons/round-49-verifier-spotcheck.md:126`, locator computed in `receipts/contract-sources.txt`) was,
until now, only readable out of prose.

Status at filing: **complete**. The gate exists, its selftest passes 58/58, and it demonstrably fails on the round-49 shape and
on three mutants of real round-48 bytes. Nothing tracked was edited; the L1 integrates the draft.

## Deliverable

| Path (lane-relative) | What it is | sha256 | bytes / lines |
|---|---|---|---|
| `.ufo/waves/round-50/w1/ExecWaveDone/check-wave-done.py` | draft for the tracked path `quality/check-wave-done.py` | `10f4359ac0af755a4e7bcb1959233862fcde4d1bc895806409b7ea1b054f818c` | 47819 / 1018 |

`receipts/deliverables.txt` holds the `test -f`, the sha256, an `ast.parse` of the draft and its `--help` text. The draft is
executable (mode +x) and stdlib-only (no installs; `git` 2.56.0 was already present — no tool was installed or upgraded).

Interface, as assigned: `--repo DIR --rev REV --round N`, plus `--selftest [--work DIR] [--verbose]`.
Exit 0 = every launched wave settled, 1 = MISSING, 2 = usage or git error.

## The contract, derived rather than invented

Two sources disagree, so the gate scores what is observable and fails the rest loudly.

| source | says | locator (computed) |
|---|---|---|
| round prompt, run-7 handoff block | "(per seat: name, agent, id, status, final output)" | `~/Projects/shokunin/.ufo/prompts/mado-round-50.md:231` |
| the same block, launch marker | "holding JSON `{\"lane\":…,\"round\":50,\"wave\":…,\"dispatch\":…,\"l1\":…}`" | `…/mado-round-50.md:228` |
| the dispatcher that writes the file | `res.append({'name': n, 'agent': …, 'output': o,` + `'note': …` | `~/Projects/shokunin/scripts/hyaku/inline-dispatcher.py:293-294` |
| the dispatcher document | `json.dump({'lane':…, 'round':…, 'wave':…, 'seats':…, 'results':…})` | `inline-dispatcher.py:295` |

The prompt promises `id` and `status`; the dispatcher writes neither, and **none** of the 14 committed `*-results.json` files in
this lane's history (rounds 39-48, including `round-48/a4r1`) carries a `status` key — measured with `json` over
`git log --all --name-only -- '*-results.json'`. A record there is terminal because `finalize` writes the file only after every
seat settles, not because a field says so.

Per-seat state, first match wins (the table is also in the draft's docstring):

- `name` missing/not a plain id, `agent` missing, name already seen → not settled (`name-missing` / `name-malformed` /
  `agent-missing` / `name-duplicate`);
- `status` = `settled` or `output-unavailable` → settled; `failed`/`error`/`dead`/`killed`/`cancelled`/`canceled`/`timeout` →
  terminal but dead (printed, not counted); any other `status` string → `status-unknown`, **fails** (drift becomes a finding);
- no `status`: non-empty string `output` → settled; `output` null **and** a non-empty `note` → settled (the kernel-restart lossy
  case, 63 records in round 39, all scored settled); `output` null/blank with no note → `output-empty`; `output` not a string →
  `output-type`.

Wave verdict `OK` requires: the `.ready` marker parses; a results file exists at the revision; it parses with `results` a
non-empty list; `lane` is `mado` and `round`/`wave` agree with the path; `seats == len(results)`; no duplicate names; every seat
settled; and — when the wave's dispatch file is readable at the revision — the results name set equals `taskCall.tasks`
(measured: identical in all 13 historical waves, so exact equality is safe). With no readable dispatch file the line prints
`dispatched=-` and the limit is declared, not hidden.

## Behaviour worth knowing

- Output: one `WAVE …` line per launched wave, `SEAT …` per non-settled seat, `NOTE …` for structural detail, `ORPHAN …` for a
  results file with no `.ready`, `SCOPE …` when the round has no launch marker at all, then exactly
  `MADO_WAVE_DONE: round=N waves=W settled=S verdict=OK|MISSING`.
- Committed bytes only: `git ls-tree -r -z` + `git show <rev>:<path>`; the working tree is never read, and the gate writes
  nothing (the clone's `git status --porcelain` is still 0 after every run in `receipts/mutants-real-clone.txt`).
- `--rev` is resolved through `git rev-parse --verify --end-of-options REV^{commit}` and every later call uses the resolved
  40-hex id, so an argument that looks like an option (`--rev --help`) cannot reach git as one (`receipts/arg-guards.txt`).
- `--selftest` builds throwaway repos under `--work`/`$TMPDIR`, refuses `/tmp`, `/var/tmp`, `/dev/shm` and any path inside a home (reading `$HOME` **and** the passwd home, with an
  absent `$HOME` an error), gives each fixture its
  own `HOME`/`XDG_*` inside the work dir, and asserts `git rev-parse --show-toplevel` equals the fixture before the first
  commit.
- **Residual found by a peer and closed (SentHostState, same round).** The first version of the home rule read only `$HOME`
  (`home_roots`/`passwd_home` now read both, and an absent `$HOME` is an error): with `HOME` unset, `--selftest --work <a home>`
  was accepted (`rc 0`) and the suite silently dropped its home cases and still reported green (55 → 53). Both effects are now
  pinned: `env -u HOME … --selftest` exits 2 (`receipts/home-guard-r50.txt` last case, `receipts/arg-guards.txt`), and the suite
  asserts its exact case count, so a disappearing case fails instead of shrinking the green line.
- Transferable invariant for the round-50 freeze: pin the exact expected case count, not only `passed == total`. A suite that
  skipped two cases and passed the rest still satisfies `passed == total` (my own run printed 53/53 while two cases had
  vanished); `SELFTEST_CHECKS = 58` is what turned that into a failure, and it caught my own arithmetic (58 vs 57) while the
  cases were being added.
- The `$HOME` refusal came in after a peer signal this round (SentHostState, routed observation `R-SHS-2` — a scratch root accepted
  under a home, with SIGKILL residue; not `R-SHS-3`, which is the outer-tracer false-MISS mode and cannot reach a gate that wraps
  no counter): round-50 instruments write only under `--work`/`TMPDIR`, but none refused a home root. This
  gate's fixtures are git repositories with commits, so a home-based `--work` would be home state; `--work "$HOME"` and
  `--work "$HOME/x"` now exit 2 (`receipts/arg-guards.txt`, `receipts/selftest.txt` three `refuse-work-home` cases).

## Evidence (all receipts are in `receipts/`, produced from the fleet root, no home path printed)

| receipt | shows |
|---|---|
| `selftest.txt` | `MADO_WAVE_DONE_SELFTEST: 58/58 passed`, rc 0 — 58 assertions over 25 fixture repos and 13 argument cases (fixtures: settled, lossy, empty output, blank output, non-string output, unparsable, wrong shape, wrong round, wrong lane, wrong count, duplicate seat, unparsable ready, explicit status settled/failed/unknown, missing agent, dispatch mismatch/absent/from-ready, two waves, no ready, other round, dispatched-marker, worktree-invisible, rev-pins-bytes; 5 usage cases, 1 unresolvable rev, 1 non-repo, 3 non-home work-dir refusals, 3 home refusals, 2 absent-`$HOME` cases; the
  count is pinned in `SELFTEST_CHECKS` (`:160`) and a skip fails the run) |
| `r49-missing.txt` | **required demonstration**: at `8ae47b9` `--round 49` → `WAVE wave=w1 ready=1 results=absent seats=0 dispatched=45 settled=0 verdict=MISSING reason=results-missing`, `MADO_WAVE_DONE: round=49 waves=1 settled=0 verdict=MISSING`, rc 1; the same receipt's `ls-tree` shows `w1.ready` and no `w1-results.json` in the round-49 tree |
| `history-base.txt` | rounds 39, 40, 41 (2 waves), 42 (`waves=0`, see limits), 43 (2), 44 (2), 45, 46, 47 (2), 48 (3, incl. `a4r1`) → `verdict=OK`, rc 0; round 49 → MISSING, rc 1. No false positive on any round that has a committed results file |
| `mutants-real-clone.txt` | control on unchanged bytes → OK; **M3** delete `round-48/w1-results.json` → `reason=results-missing`, `waves=3 settled=2`; **M2** null one seat's output and clear its note → `reason=seats-not-terminal+dispatch-mismatch` with `SEAT … state=output-empty:null-no-note`; **M1** drop a seat record *and* lower `seats` to match → `reason=dispatch-mismatch`; all rc 1, clone tree clean, HEAD restored |
| `bare-clone.txt` | works against `git clone --bare --shared` (`rev-parse --is-bare-repository` → `true`), rounds 48 OK / 49 MISSING |
| `arg-guards.txt` | 8 invocations: `--rev --help`, empty `--rev`, `--round -3`, missing repo, 40-zero rev, missing `--rev`, `--work /tmp/…`, `--work /dev/shm/…` → all rc 2 |
| `pre-handoff-scope.txt` | rounds 13-38 (26 rounds, before the inline-spawn handoff): each prints `SCOPE round=N markers=0 note=no-launch-marker: … out of scope, not settled` and `waves=0 verdict=MISSING` |
| `contract-sources.txt` | every quote above, with `grep -n`-computed locators |
| `deliverables.txt` | presence, sha256, `ast-parse=ok`, `--help`, lane HEAD, and the lane's tracked-modification list |
| `home-guard-r50.txt` | the admission rule with `grep -n` locators on the final bytes (`:533` non-home refusals, `:539` home refusal, `:512` absent-`$HOME` error, `:160` pinned case count) and the argument cases at rc 2 — including the `env -u HOME` residual a peer measured, which used to be accepted with a silently smaller green suite |

## Limits (declared in the tool, repeated here)

1. **Scope is the inline-spawn era.** A wave is launched by a committed `.ufo/waves/round-N/<wave>.ready`; rounds before the
   handoff (13-38 here) have no such marker, so the gate answers `waves=0` plus a `SCOPE … out of scope` line — exit 1, never
   `OK`. Round 42 is the calibration point: its own report says the 36-seat wave was "written and handed off with a `w1.ready`;
   it was never spawned" and the uncommitted marker was removed, so `waves=0` is the true answer there, not a false negative.
2. **Seat coverage is only enforced when the dispatch JSON is committed.** Absent/unreadable dispatch → `dispatched=-`, and a
   wave can still score `OK`; the line says so.
3. **The `.ready` marker must be a direct child** of the round dir and its results file `<wave>-results.json`; renamed or nested
   evidence is out of scope (no historical wave trips this: all 13 waves resolve).
4. **It is a process instrument, not a truth instrument.** It can prove the orchestrator wrote a terminal record for every
   seat it dispatched and that the seat set matches the dispatch. It cannot tell whether a seat's report is honest, and it does
   not read seat reports at all.

## Observation for the L1 (not mine, no judgment)

At the time of `receipts/deliverables.txt` the lane working tree carries 4 modified tracked files, all under
`.ufo/waves/round-49/w1/` (`ExecControlsC1.md`, `ExecControlsC1/check-c07-isolation.py`,
`ExecControlsC1/make-controls-receipt.py`, `ExecCounterC1.md`). This seat authored none of them — its own paths are untracked
drafts (`.ufo/waves/round-50/w1/ExecWaveDone/` and `ExecWaveDone.md`). Recorded because a wave in flight is not supposed to
mutate tracked files, and because the L1 is the only integrator.

## Not done here

- No tracked file written: the L1 lands the draft as `quality/check-wave-done.py` (suggested wiring: run it at the round's
  landing revision, `--round N`, before the round report is filed; the report is then either past WAVE-DONE or the gate prints
  the missing wave).
- The second half of D2 (naming the final state of each of the 7 unsettled round-49 seats in the round-50 report) is the L1's
  item; this seat's own ticket covers it because the gate now supplies the machine answer for rounds 39+.

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r50/ExecWaveDone/` (shared clone, bare clone, fixtures, receipts staging) removed at the end
of the seat; the receipts were copied into this seat dir first, so no scratch path is cited as evidence.

# CritC1Cheat — can PRED-C1-r41-v1 reach TARGET_MET without doing the work?

Round 41, wave w1, seat `CritC1Cheat`. Lane `mado-shokunin`, claims frozen at
`60c3914154333180450d5da27ba222d5763cc56a` (base `ab2bfaab…`). Nothing outside
`.ufo/waves/round-41/w1/CritC1Cheat/` was written; the counter, controls,
reference, registration and fetch receipts were read only. No git/jj mutation,
no pacman, no host-service or compositor contact, no journal verb other than
read-only `journalctl`.

## Answer first

**No cheat reached TARGET_MET without the model.** Every tool that scored MET
carries the reference's parse/class/report code (the declared residual at
`c1-r41-globals.py:104-105`); a tool with no parser tops out at **7/24** (CH7),
and those 7 are the SETUP/NO_SESSIONS fixtures. **17 of 24 fixtures cannot be
answered without parsing the journal** — the nonce lattice does its job.

What *did* break is the clause layer: **8 of 12 cheats scored TARGET_MET**, each
by keeping the model and defeating one clause or one guard. Three of those
(CH6, CH9, CH10) defeat clause b2 — the "selftest teeth" clause — and one (CH4)
shows clause g does not constrain process spawning at all. The counter's own
statement that a live-mode violation "shows as exit 5, never as a report"
(`c1-r41-globals.py:69-71`) is **falsified** by CH1: the argv/stdin/env guard is
never exercised, because the stub's payload is readable without running it.

## Method

Every cheat is the frozen reference (`c1/ctl-ref-tool.py.txt`, sha256
`61f101ae…130f0`) with one localized change, so each result isolates one hole.
Builders: `make_cheats.py` (CH1–CH3, CH5, CH6, CH8, CH11, CH12), `make_ch9.py`,
`make_ch10.py`; CH4 and CH7 are hand-written. Both builders assert the reference
sha256 before patching.

Scoring command (one fixed nonce, so all twelve cheats see the same 24 fixtures
and the same b2 mutant sample):

```
python3 -I quality/counters/c1-r41-globals.py --repo . \
  --rev 60c3914154333180450d5da27ba222d5763cc56a \
  --nonce c0ffee00deadbeef \
  --tool .ufo/waves/round-41/w1/CritC1Cheat/<cheat>.py
```

Control for my own measurement: the frozen reference scored
`fixtures=24/24 … verdict=TARGET_MET` at this nonce (`score-ref.txt`, exit 0), so
the fixture set and b2 sample are intact; the failures below are the cheats', not
the lattice's. Full outputs: `score-chN.txt` in this directory.

Every cheat was then re-scored at a second nonce (`0123456789abcdef`,
`score2-chN.txt`): **all twelve verdicts and all twelve fixture counts are
identical**, and the only b2 count that moved is CH4's (5/6 → 6/6). So no result
below depends on which six sites the nonce samples.

## Results

| # | cheat | fixtures | clauses | verdict | killed by |
|---|---|---|---|---|---|
| CH1 | `ch1-stub-oracle.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |
| CH2 | `ch2-cwd-replay.py` | 21/24 | b2 5/6 | MISSED | livefail0, livewritable0, livelarge0 |
| CH3 | `ch3-word-name.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |
| CH4 | `ch4-child-interpreter.py` | **24/24** | a1 b1 b2 5/6 g1 | **TARGET_MET** | — |
| CH5 | `ch5-selftest-echo.py` | 24/24 | b2 **0/6** | MISSED | clause b2 |
| CH6 | `ch6-mutant-path-detect.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |
| CH7 | `ch7-sibling-report.py` | 7/24 | b2 sites=9 (<12) | MISSED | 17 fixtures |
| CH8 | `ch8-eval-getattr.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |
| CH9 | `ch9-self-fingerprint.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |
| CH10 | `ch10-aim-away.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |
| CH11 | `ch11-session-pid-only.py` | 22/24 | b 43/47 | MISSED | gen1, gen6, own selftest |
| CH12 | `ch12-session-bootid.py` | **24/24** | a1 b1 b2 6/6 g1 | **TARGET_MET** | — |

## Survivors

### CH1 — the live stub is an oracle, not a program (24/24 MET)

`read_live` never executes the program: it reads the stub's own bytes, decodes
the base64 journal out of the `printf '%s' … | base64 -d` line, and classifies
the failure modes from the shell body (`head -c 9000000` → `journalctl_too_large`,
a bare `exit 1` → `journalctl_failed`); `resolve_program` still gives
`journalctl_unusable` for a group-writable file. All six live fixtures pass, and
`liveenv0` (canary) passes *because the stub never ran*.

Evidence (`probe-live-cheats.txt`, `probe-live-cheats.py`):
`P1 read_live_returned_payload=101 marker_created=0 equal=1` — the probe stub
touches a marker whenever it is executed; the marker does not exist after
`read_live` returns the journal. So the argv/stdin/env guard, the canary and the
stdin-is-a-pipe check are never observed.

Attacks `c1-r41-globals.py:441` (`STUB_FILE`), `:444-456` (`live_stub`; the
payload is base64 inside a readable `0755` script, `:456`) and the claim at
`:69-71` ("The stub the judge supplies exits 9 unless argv, stdin and environment
are as stated"). Declared residual `:104-106` covers decoding the payload; it does
not cover *replacing* the guard with a byte inspection.

Cheapest remedies, in order:
1. Free: do not write `journal.txt` for live fixtures (`prepare` writes it
   unconditionally at `:466`; CH2 below exploits exactly that copy).
2. Cheap, partial: a decoy journal in the stub body — a reader that takes the
   first base64 blob prints the decoy and fails. Raises cost, does not close it.
3. Sound, not free: the payload must be unreadable by the tool, i.e. an
   **execute-only (0111) compiled stub with the payload embedded, built per
   fixture**. Verified on this host: a `0111` *shell script* can neither be read
   nor executed (`exec rc=126`, `read rc=1`), so the stub must be an ELF; `gcc`
   is present at `/usr/bin/gcc`, and only the 6 live fixtures need it.

### CH2 — the live journal is also on disk (21/24, 3 fixtures for free)

`prepare` writes the journal to `<fx>/journal.txt` even when the fixture is live
(`c1-r41-globals.py:466`, `jp` written before the `if live is None` branch at
`:470`). CH2 reads any `*.txt` in cwd and replays it, without running the
program. `live0`, `live1`, `liveenv0` pass on the replay alone; the three
fixtures that must *not* produce a report (livefail0, livewritable0,
livelarge0) fail, which is itself the proof that the replay, not the honest
path, produced the output.

Evidence: `P2 read_live_returned_cwd_file=1 from_program=0`
(`probe-live-cheats.txt`) — with a cwd `journal.txt` that differs from what the
program prints, `read_live` returns the file.

Remedy: the free one above (skip the `journal.txt` write for live fixtures).
This alone kills CH2 outright and removes a second copy of the payload.

### CH3 — a NAME rule that deviates from the contract and coincides (24/24 MET)

`([A-Za-z0-9_]{1,128})` → `(\w{1,128})` in the ADVERT regex and in the
`--expect` validator. The contract says the name is
`[A-Za-z0-9_]{1,128}` (`c1-r41-globals.py:30`, `:19-20`); `\w` also accepts
Unicode word characters, so a **valid-UTF-8** non-ASCII interface name would be
reported by CH3 and ignored by the model. No fixture contains one: the generator
draws names from `sorted(TABLE) + COMMON + syn` (all ASCII), and the one
non-ASCII noise line is invalid UTF-8 (`"\xe9\xff"`), which decodes to U+FFFD
under the model's `errors="replace"` and is rejected by `\w` too. So the two
rules agree on all 24 fixtures.

Remedy (cheap, no new fixture): append one advert line to `sample_journal` whose
name is UTF-8 bytes for e.g. `wl_é` — the model rejects it, `\w` accepts it, and
diff0/diff1/expect0/expectmiss0/live0/live1/liveenv0 all fail for CH3. Note the
generator cannot express this today: `score_gen` encodes the whole text with
`latin-1` as soon as the character `\xe9` appears (`:516-517`), which would
destroy the UTF-8 sequence; the fixed-case route avoids that branch.

### CH4 — clause g does not see a child interpreter (24/24 MET)

The whole parse/report runs in `python3 -I -c "<source>"` with the journal on
stdin; the parent only relays and checks structure. Imports stay inside the
allow-list (`argparse os re stat subprocess sys tempfile`), there is no
`exec/eval/compile/__import__`, no `shell=True`, no `os.system`, so clause g
passes — while the *parser is a string* clause g cannot see, and a process is
started in `--journal-file` mode, which the contract forbids
(`c1-r41-globals.py:71-72`: "In `--journal-file` mode the tool must not start any
process"). The only file-mode detector is the `journalctl` stub on PATH, so a
child named anything else is invisible; `sys.executable` is an absolute path, so
a PATH tripwire would not catch it either. b2 was satisfied with a 12-comparison
`invariants()`/`verify()` that the selftest does exercise (killed 5/6, MET needs
4).

Remedy, cheapest first:
1. Static (3 lines in `imports_ok`): any `subprocess.*` call whose first argument
   is a list literal whose first element is not a bare name is a violation — the
   honest pattern `[prog] + JOURNALCTL_ARGS` passes, `[sys.executable, …]` fails.
   Heuristic, not sound.
2. Sound (≈5 lines): run the 18 file-mode fixtures with `--tmpfs /usr/bin` plus a
   `--ro-bind` of the single interpreter, so no absolute-path program exists to
   spawn. Must not be applied to `--selftest` or to live fixtures (both need
   `/bin/sh` for their stubs).

### CH6 — clause b2 is defeated by the mutant's directory name (24/24 MET)

The reference selftest is replaced by a four-line check of where the tool is
running: the real run happens at `<tmp>/tool/mado-globals.py` (`:808`) and each
mutant at `<tmp>/mutN/mado-globals.py` (`:766`), so
`basename(dirname(argv[0])) != "tool"` prints `1/2 passed` and exits 1. Clause b
sees `40/40`; b2 sees `killed=6/6`. Identical source except those four lines
scores **0/6 killed and MISSED** (CH5), so the four lines are the whole effect.

Attacks `c1-r41-globals.py:721` (`NOT_SITES`), `:766`, `:808`.

Cheapest remedy (2 lines): make the mutant layout identical to the real one —
real tool at `<tmp>/<random>/tool/mado-globals.py`, each mutant at
`<tmp>/<random>/tool/mado-globals.py` with an independent random parent — so no
path component distinguishes them.

### CH9 — clause b2 is defeated by a self-fingerprint (24/24 MET, survives CH6's remedy)

`--selftest` computes a rolling hash of its own file (`open(sys.argv[0], "rb")`,
with the `_SELF = ` line excluded) and compares it with an embedded constant;
any edit, including a b2 mutant, fails the selftest. `killed=6/6`, `40/40`, no
test inside. This is name- and path-independent, so the CH6 remedy does not
touch it, and `hashlib` is not even needed (the hash is arithmetic on bytes,
which stays inside the import allow-list).

Remedy (3 lines in `imports_ok`, cheap and sound enough):
- deny any `open(...)` call whose argument subtree mentions `__file__` or
  `sys.argv` (an honest census tool never reads itself);
- optionally, as a second net, run one extra control: apply a
  semantics-preserving but AST-visible edit (rename a local variable) and require
  the selftest to still pass — a fingerprint fails that, a real test does not.

### CH8 — clause g's name blacklist is evadable in one line (24/24 MET)

`_EVAL = getattr(sys.modules["builtins"], "ev" + "al")` then
`CLASS_OF = _EVAL("{…}")`: the class table is built by `eval`, and clause g
passes (`g:1`) because `CALL_DENY`/`OS_DENY` only match the literal `Name`/`Attribute`
forms (`c1-r41-globals.py:137-140`). The same trick reaches `compile` and
`__import__`. Here it buys nothing (the table is data), but the clause is stated
as a guarantee and it is not one.

Remedy (3 lines in `imports_ok`): flag any `ast.Constant` string equal to one of
`exec eval compile __import__` (catches the concatenation, since the pieces are
themselves constants only when whole), and flag `getattr`/`vars`/`setattr` calls
whose first argument is `__builtins__`, `builtins` or `sys.modules[...]`.

### CH10 — clause b2 can be aimed away from the model (24/24 MET)

Rename `parse`→`_run_parse`, `report`→`_run_report`, `classify`→`_check_classify`
(every one matches a `NOT_SITES` substring) and add `invariants()` with 12
comparison sites that `run()` and the selftest both call. The sampled six
mutants land in `read_live`, `run` and `invariants` — **none in the parser or the
reporter** — and all six are killed: `sites=17 killed=6/6`, MET. The model is
never mutated, so b2 says nothing about it.

Attacks `c1-r41-globals.py:721`: the exclusion is by *name substring*, so the
code that matters can be renamed out of the sample.

Remedy (one tuple + one check): exclude only the function named exactly
`selftest` (and definitions nested inside it), and require that at least one of
the sampled sites lies in the function that emits the
`MADO_GLOBALS: sessions=` summary line. The reference is unaffected: counting
`main` adds one site (13 instead of 12, `if sys.argv[1:] == ["--selftest"]`) and
its mutant is killed anyway, because the mutated tool no longer recognises
`--selftest` and prints no summary.

### CH12 — an equivalent session rule also scores MET (24/24) — not a defect

Keying the session on the boot id (`cur["boot"] != boot`) instead of the
`boot_changed` flag coincides on every fixture, because the lattice's boot ids
are unique; it is the same decision procedure. Recorded so the L1 does not read
it as a survivor: an equivalent formulation *should* pass, and the counter's own
selftest also cannot tell them apart (47/47 for both). No remedy.

## Killed cheats (positive results for the predicate)

- **CH5, selftest echo + real parser** (`24/24`, `b2 killed=0/6`): the fixtures
  and clause b pass, b2 alone kills it. This is the same shape as control
  `M39-selftest-echo` (`receipts/ctl-c1.txt`), reproduced at this nonce. b2
  works when the selftest is merely absent.
- **CH7, expected output from a sibling path** (`7/24`): the sandbox holds only
  `journal.txt`, `bin/journalctl`, the mark dir and the tool itself
  (`probe-tree.txt`: `REPORT_HITS` = the tool file only, three times). So the
  only fixtures reachable with no parser are usage0, badexpect0, unreadable0,
  toolarge0 (both halves), nosess0 and nosess1 = 7/24, and every one of them is
  a SETUP or a NO_SESSIONS answer. **17/24 need the model.**
- **CH11, pid-only session rule** (`22/24`, `selftest 43/47`): killed by gen1 and
  gen6 (one pid reused across boots) and by the reference's own boot-split check.
  The boot-boundary semantics is pinned twice over.

Side observation from `probe-tree.txt`: the *file-mode* stub is readable
(`STUB_READABLE=57`) and its body is `touch <…>/mark/hit` — it hands the tool the
fixture name (`gen3`, `live0`, …) and the writable mark dir. No exploit found
(fixture content is nonce-derived; writing `mark/hit` fails the fixture), but an
opaque fixture directory name costs nothing.

## Ranked remedies (all cheap first)

1. **Free, one line** — write `journal.txt` only when the fixture is not live
   (`c1-r41-globals.py:466`). Kills CH2 and removes the on-disk copy of the live
   payload.
2. **2 lines** — identical directory shape for the real tool and the b2 mutants
   (`:766`, `:808`). Kills CH6.
3. **3 lines in `imports_ok`** — self-read ban (`open` on `__file__`/`sys.argv`)
   plus `getattr/vars` on builtins plus Constant strings equal to
   `exec/eval/compile/__import__` (`:137-140`, `:679-710`). Kills CH8, CH9.
4. **One tuple + one check** — `NOT_SITES` → exclude only the function named
   `selftest`; require a sampled site in the summary-emitting function (`:721`).
   Kills CH10.
5. **2 lines in `sample_journal`** — one valid-UTF-8 non-ASCII name line that
   must be ignored. Kills CH3.
6. **≈5 lines** — `--tmpfs /usr/bin` + single-interpreter bind for the 18
   file-mode fixture runs only. Kills CH4 and any hidden implementation reached
   through `subprocess`.
7. **Not free** — execute-only compiled live stub, or weaken the docstring claim
   at `:69-71` and keep the residual: CH1 shows the guard is currently
   unobservable, which the residual at `:104-106` does not say.

Items 1–5 cost a handful of lines and close CH2, CH3, CH6, CH8, CH9, CH10. Item
6 closes CH4; item 7 is the only one that needs new machinery, and until it
lands the sentence at `:69-71` overstates what the stub proves.

## Limits of this seat

- All twelve scores are `--tool` controls, each run at two fixed nonces
  (`c0ffee00deadbeef`, `0123456789abcdef`); none was scored from a committed REV,
  and the L1 is the only integrator. Verdicts and fixture counts are identical at
  both nonces, so the fixed samples do not carry any result.
- CH1/CH2 were also probed outside the counter (`probe-live-cheats.py`) so that
  "the stub was never executed" and "the cwd file was used" are measured, not
  inferred.
- Tooling: nothing installed or updated this seat (no package transaction, no
  pacman). Host tools used as found: `python3` 3.14, `bwrap`, `gcc` (presence
  check only), `git` read-only.

## Files

```
.ufo/waves/round-41/w1/CritC1Cheat.md      this report
.ufo/waves/round-41/w1/CritC1Cheat/        seat dir
  ref-base.py                 frozen reference copy, sha256 61f101ae…130f0
  make_cheats.py              CH1 CH2 CH3 CH5 CH6 CH8 CH11 CH12
  make_ch9.py                 CH9 (two-pass fingerprint)
  make_ch10.py                CH10
  ch1..ch12                   the twelve cheat tools
  score-ref.txt               reference at this nonce: 24/24 MET
  score-chN.txt               full counter output per cheat (nonce c0ffee00…)
  score2-chN.txt              same twelve at nonce 0123456789abcdef
  probe-live-cheats.py/.txt   P1 stub-never-run, P2 cwd-replay
  probe-tree.txt              what a file-mode sandbox exposes
  verify-quotes.py/.txt       every quote above checked against the counter (7/7)
```

# ExecC1ExtraMutants — extra single-defect mutants of the C1 reference (round 41, w1)

Seat `ExecC1ExtraMutants`, leaf of wave w1. Target: find the C1 counter's blind spots by writing
NEW single-edit mutants of the reference tool and scoring them with PRED-C1-r41-v1.

## Outcome

**42 new single-edit mutants** of `.ufo/waves/round-41/c1/ctl-ref-tool.py.txt` (346 lines, sha256
`61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0`), none of them in
`ctl/run-c1-controls.py` (43 mutants + 3 do-nothing controls, sha256
`1b21403b94ed70009a4fe5b4f0753bb498b69258443ff8c1825d4dfa6e5bf1bb`). Scored at rev
`60c3914154333180450d5da27ba222d5763cc56a`, nonce `c1x41exec0001`:

- **29 killed** (each fails >= 1 of the frozen 24 fixtures, or a clause).
- **13 survivors = 24/24 TARGET_MET** at nonces `c1x41exec0001/0002/0003/0004` (`…0005` for N43).
  **Every survivor has a verified kill fixture, so each is a missing fixture class; there is no
  equivalent mutant in this set.**
- No textual duplicate of the frozen controls (`EXACT-DUPLICATES-vs-controls: none`; 42 distinct
  sources). One behavioural duplicate of a frozen control is named and proved: N06 ≡ M25.

Full analysis, per-survivor kill fixtures and the contract sentence each breaks:
`.ufo/waves/round-41/w1/ExecC1ExtraMutants/survivors.md`.

## The 13 survivors (fixture class the predicate lacks)

| mutant | missing fixture class |
|---|---|
| N07-expect-case-insensitive | `--expect WL_SEAT` against a session holding `wl_seat` → must be MISSING_EXPECTED |
| N12-version-string-compare | one name with `(ver 9)` then `(ver 10)` → ver must be 10, not the string max 9 |
| N15-decode-latin-1 | an otherwise valid ADVERT whose host field is one raw `0xA0` byte |
| N16-log-case-insensitive | an advert at level `[log]` (lower case) → must be ignored |
| N20-expect-any-session | `--expect` of a name present only in an *earlier* session → MISSING_EXPECTED |
| N22-sort-case-insensitive-globals | names `Zz_g` and `aa_g` in one session → bytewise order |
| N23-pid-int-compare | pids `011` and `11` in one boot → two sessions |
| N24-ver-5-digits-max | `(ver 123456)` (six digits) → an ADVERT |
| N38-boot-reset-per-session | a second session (pid change) after one BOOT line → inherits the boot id |
| N39-expect-hyphen-allowed | `--expect a-b` → SETUP bad_expect, exit 2 |
| N40-class-lowercased | `HYPRLAND_FOCUS_GRAB_MANAGER_V1` → class `other` |
| N42-live-no-timeout | a live program that hangs → SETUP journalctl_failed at 30 s |
| N43-boot-repeat-same-id-no-split | the same BOOT id printed twice around an advert → two sessions |

## Evidence (all executed; receipts under the seat dir)

| what | receipt | key line |
|---|---|---|
| reference baseline | `logs/_ref.log` | `fixtures=24/24 tool=present verdict=TARGET_MET … nonce=c1x41exec0001` |
| mutant generation | `gen_mutants.py`, `mutants/*.py` | `MUTANTS total=42 bad=0` (each edit pattern unique) |
| per-mutant scoring | `logs/N*.log` (42 files) | e.g. `N07…: fixtures=24/24 … TARGET_MET`, `N04…: fixtures=16/24 … TARGET_MISSED` |
| nonce stability | `logs/nonce-*.log` (39 files) | every survivor `fixtures=24/24 … TARGET_MET` at 3 further nonces |
| kill fixtures | `logs/_killfix.log` | `KILLFIX fails=0` — 12 cases (10 text journals, 1 byte-level host field, 1 bad_expect), each with `ref_matches_model=1 mutant_diverges=1`; the 13th survivor (N42) is the separate hang case |
| hang case | `logs/_n42.log` | `REF rc=5 30.1s … MUTANT rc=124 32.0s … killed_by_a_hanging_stub=1` |
| duplicate signatures | `logs/_dupsig.log` | `DUP-IN-EFFECT` — the only proved pair is `('N06-count-distinct-only','M25-count-always-1')`; every other pair is an artefact of a corpus that omits the live/usage/toolarge/badexpect cases (explained in survivors.md) |

Kill fixtures are checked against the counter's own model (`PRED.model_out`), so each one is exactly
what a new fixture would score: reference matches, mutant diverges.

## Why the lattice is blind here (generator evidence)

The 24 fixtures are strong on structure (sessions, pid alternation, boots, repeats, noise, sizes,
live plumbing — 29 of 42 mutants die) and blind on value domains:

- versions are 1–9 everywhere: `quality/counters/c1-r41-globals.py:376` (`randrange(1, 10)`),
  `:420` (`1 + (j * 7) % 9`), `:546` (`randrange(1, 9)`) → N12, N24.
- every accepted name is lower case: pools `:142-178`, `syn` `:363`; the only upper-case name token
  is the rejected `"A"*32` boot id `:350` → N22, N40.
- `--expect` is always a lower-case name from the latest session or `zz_absent_*`: `:428`, `:573`
  → N07, N20, N39.
- boot ids never repeat: `boot()` draws a fresh 128-bit id per call `:367-368`; every fixture puts a
  boot before each session → N43, N38.
- pids have no leading zeros (`randrange(100, 99999)` `:382`, `:543`) → N23.
- no six-digit version (only the rejected seven-digit noise `:344`) → N24.
- no lower-case level (`[ERR]`/`[LOG]` only `:337-339`) → N16.
- hosts are ASCII (`h` `:336-354`, `plazir%d` `:377`) and non-UTF-8 bytes occur only in the ignored
  `\xe9\xff` noise line `:354` → N15.
- the live stub never hangs (`live_stub` `:444-456`: exit 1, 9 MB, writable, env, argv only) → N42.

Cheapest closes: N07, N16, N22, N24, N39, N40 are pure text-fixture additions; N12/N23/N38/N43 need
one journal each; N15 needs a byte-level fixture; N42 needs a hanging stub plus the judge's own
bound (it overlaps the declared residual "a hang (`--live` timeout) is not exercised by a fixture").

## Files written (all inside the seat dir)

- `.ufo/waves/round-41/w1/ExecC1ExtraMutants.md` (this report)
- `.ufo/waves/round-41/w1/ExecC1ExtraMutants/gen_mutants.py` (42-entry edit list, `--ref/--out`)
- `.ufo/waves/round-41/w1/ExecC1ExtraMutants/mutants/` (42 files, one edit each)
- `.ufo/waves/round-41/w1/ExecC1ExtraMutants/survivors.md` (full analysis)
- `.ufo/waves/round-41/w1/ExecC1ExtraMutants/verify_kill_fixtures.py`, `verify_n42_hang.py`
- `.ufo/waves/round-41/w1/ExecC1ExtraMutants/controls/` (the 43 frozen control mutants, regenerated
  read-only, used only for the duplicate check)
- `.ufo/waves/round-41/w1/ExecC1ExtraMutants/logs/` (all scoring and verification receipts)

Nothing outside the seat dir was written; no frozen file (counter, controls, registration, reference,
fetch receipts) was modified; no git/jj mutation; no compositor/Wayland/journal write; pacman not run.

## Risks and limits

- `--tool` mode satisfies clause a by construction (as in the frozen controls); this says nothing
  about whether the delivered `tools/mado-globals.py` differs from the reference (it is absent at the
  freeze commit, so no such comparison was possible).
- Kill fixtures are mine, not the counter's; adding them is the L1's decision.
- Survivor stability is 4 nonces (5 for N43) over the frozen set; the gaps are structural value
  domains, so further nonces cannot close them.
- N23 (pid `011` vs `11`) is the one survivor where "defect" is arguable in the abstract: the frozen
  model compares pid tokens as strings, so a fixture would score the int-compare tool wrong; noted in
  survivors.md.

## Tooling

None installed. Used the host `python3` 3.14.8, `bwrap` (/usr/bin/bwrap), `timeout`; no pacman, no
`uv`, no network.

## Blockers

None.

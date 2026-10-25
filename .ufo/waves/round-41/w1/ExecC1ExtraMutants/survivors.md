# Survivors — 13 extra single-edit mutants of the C1 reference pass the frozen 24-fixture predicate

Seat `ExecC1ExtraMutants`, mado round 41 (w1), lane `mado-shokunin`.
Reference under mutation: `.ufo/waves/round-41/c1/ctl-ref-tool.py.txt`
(346 lines, sha256 `61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0`).
Predicate: `quality/counters/c1-r41-globals.py` (PRED-C1-r41-v1), rev
`60c3914154333180450d5da27ba222d5763cc56a`.

**Result: 42 new single-edit mutants, 29 killed, 13 survivors (TARGET_MET, fixtures=24/24).
Each survivor has a verified kill fixture, so every survivor is a missing fixture class;
there is no equivalent mutant in this set.** The 13 are stable across the nonces
`c1x41exec0001`, `c1x41exec0002`, `c1x41exec0003`, `c1x41exec0004` (`…0005` for N43).

## Method (all commands run, all receipts in this seat dir)

| step | command / evidence |
|---|---|
| baseline | `python3 -I quality/counters/c1-r41-globals.py --repo . --rev 60c3914… --tool .ufo/waves/round-41/c1/ctl-ref-tool.py.txt --nonce c1x41exec0001` → `fixtures=24/24 verdict=TARGET_MET` (`logs/_ref.log`) |
| generation | `python3 gen_mutants.py` → `MUTANTS total=42 bad=0` (every edit pattern occurs exactly once; `mutants/*.py`) |
| novelty | hash check against the 43 frozen control mutants (regenerated from `ctl/run-c1-controls.py`): `EXACT-DUPLICATES-vs-controls: none`, `mine=42 distinct=42` |
| scoring | one counter run per mutant, `--tool mutants/<name>.py`, `--nonce c1x41exec0001`; `logs/<name>.log`; survivors re-run at 3 further nonces (`logs/nonce-*.log`) |
| kill fixtures | `python3 verify_kill_fixtures.py --kill-only` → `KILLFIX fails=0` (`logs/_killfix.log`); each case checks the reference against the counter's own model (`PRED.model_out`) **and** that the mutant diverges |
| hang case | `python3 verify_n42_hang.py` → `REF rc=5 30.1s … MUTANT rc=124 32.0s … killed_by_a_hanging_stub=1` (`logs/_n42.log`) |
| behavioural duplicates | `python3 verify_kill_fixtures.py` (fixture corpus + clauses, 85 tools) → `logs/_dupsig.log` |

`--tool` scores the file given; clause a is therefore satisfied by construction
(`present` is true for any `--tool`), which is the same mode the frozen controls
use (`ctl/run-c1-controls.py:score`). The base precondition (tool absent at
`ab2bfaab…`) is unchanged and still holds.

## All 42 mutants

| mutant | verdict | failing fixtures (nonce c1x41exec0001) |
|---|---|---|
| N01-session-key-host-not-pid | killed | gen0–gen7, diff0, diff1, expect0, expectmiss0, live0, live1, liveenv0 |
| N02-boot-id-from-full-line | killed | gen1, gen3, gen5, gen6, gen7 |
| N03-latest-is-longest | killed | gen2, gen5, gen7, diff0, live0, live1, liveenv0 |
| N04-class-counts-adverts | killed | gen0–gen7 |
| N05-first-tracks-last | killed | gen0–gen6 |
| N06-count-distinct-only | killed | gen0–gen7 |
| **N07-expect-case-insensitive** | **SURVIVOR** | none |
| N08-global-lines-all-sessions | killed | gen1, gen2, gen4, gen5, gen6, diff0, live0, live1, liveenv0 |
| N09-trailing-space-global-line | killed | gen0–gen7, diff0, diff1, expect0, expectmiss0, live0, live1, liveenv0 |
| N10-diff-missing-exit-0 | killed | gen1 |
| N11-diff-first-vs-last | killed | gen1, gen2, diff0 |
| **N12-version-string-compare** | **SURVIVOR** | none |
| N13-name-129-truncated | killed | gen3, nosess0 |
| N14-empty-file-expect-ok | killed | nosess0 |
| **N15-decode-latin-1** | **SURVIVOR** | none |
| **N16-log-case-insensitive** | **SURVIVOR** | none |
| N17-env-adds-home | killed | live0, live1, liveenv0, livelarge0 |
| N18-program-relative-to-cwd | killed | live1 |
| N19-boot-line-never-splits | killed | gen1, gen6 |
| **N20-expect-any-session** | **SURVIVOR** | none |
| N21-sessions-count-distinct-pids | killed | gen1, gen2, gen6 |
| **N22-sort-case-insensitive-globals** | **SURVIVOR** | none |
| **N23-pid-int-compare** | **SURVIVOR** | none |
| **N24-ver-5-digits-max** | **SURVIVOR** | none |
| N25-session-numbering-from-0 | killed | gen0–gen7, diff0, diff1, expect0, expectmiss0, live0, live1, liveenv0 |
| N26-journalctl-allowed-with-file | killed | usage0 |
| N27-interfaces-counts-adverts | killed | gen0–gen7 |
| N28-classes-drop-other | killed | gen0–gen7, diff0, diff1, expect0, expectmiss0, live0, live1, liveenv0 |
| N29-diff-ver-increase-only | killed | gen6, live0, liveenv0 |
| N30-size-limit-plus-two | killed | toolarge0 |
| N31-stderr-noise | killed | 18 fixtures (every rc-0/1/3 case) |
| N32-adverts-counts-distinct | killed | gen0–gen7, diff0, diff1, expect0, expectmiss0, live0, live1, liveenv0 |
| N33-session-boot-always-dash | killed | gen1, gen3, gen5, gen6, gen7 |
| N34-last-is-max-ts | killed | gen0–gen6 |
| N35-read-only-max-bytes | killed | toolarge0 |
| N37-path-loop-is-cwd | killed | live1 |
| **N38-boot-reset-per-session** | **SURVIVOR** | none |
| **N39-expect-hyphen-allowed** | **SURVIVOR** | none |
| **N40-class-lowercased** | **SURVIVOR** | none |
| N41-usage-exit-1 | killed | usage0 |
| **N42-live-no-timeout** | **SURVIVOR** | none |
| **N43-boot-repeat-same-id-no-split** | **SURVIVOR** | none |

## The 13 survivors and the fixture that kills each

Every row below was executed: the reference reproduces the counter's model
(`ref_matches_model=1`), the mutant diverges (`mutant_diverges=1`)
— `logs/_killfix.log`; N42 is `logs/_n42.log`.

| # | mutant (single edit) | contract sentence broken | kill fixture | reference vs mutant |
|---|---|---|---|---|
| 1 | N07 `e not in names` → `e.lower() not in [n.lower() …]` | `--expect NAME` … "absent from the latest session"; names are byte-exact | `--journal-file j --expect WL_SEAT` over a session holding `wl_seat` | rc 1 `expected_missing=WL_SEAT … MISSING_EXPECTED` vs rc 0 `expected_missing=- … OK` |
| 2 | N12 `max(ent[1], ver)` → `int(max(str(ent[1]), str(ver)))` | "per distinct NAME: count and ver = the highest N seen" (N is a number) | one session: `wl_seat (ver 9)` then `wl_seat (ver 10)` | `ver=10 count=2` vs `ver=9 count=2` |
| 3 | N15 `decode("utf-8","replace")` → `decode("latin-1")` | ADVERT line grammar `TS HOST …` with `HOST = \S+` over the model's utf-8/replace decode | one advert whose host field is the raw byte `0xA0` | rc 0, 1 session (`\S+` matches U+FFFD) vs rc 3 `NO_SESSIONS` (NBSP is whitespace) |
| 4 | N16 `\[LOG\]` → `(?i:\[log\])` | "every other line (another program, **another level**, …) is ignored" | one advert with `[log]` instead of `[LOG]` | rc 3 `NO_SESSIONS` vs rc 0, 1 session |
| 5 | N20 `e not in names` → `e not in <union of all sessions>` | `--expect` checks the **latest** session only | 2 sessions: `wl_seat` in pid 200 only, `wl_compositor` in pid 201; `--expect wl_seat` | rc 1 `expected_missing=wl_seat` vs rc 0 `expected_missing=-` |
| 6 | N22 `sorted(latest["names"])` → `sorted(…, key=str.lower)` | "per NAME **sorted bytewise**" | one session holding `Zz_g` and `aa_g` | line 2 `name=Zz_g` vs `name=aa_g` |
| 7 | N23 `cur["pid"] != pid` → `int(cur["pid"]) != int(pid)` | "its PID differs from the open session's PID" (PID = the `\d+` token) | adverts with pid `011` then `11`, same boot | 2 sessions (`n=1 … interfaces=1`, `n=2`) vs 1 session `interfaces=2 adverts=2` |
| 8 | N24 `\(ver (\d{1,6})\)` → `(\d{1,5})` | "N = `\d{1,6}`" — a six-digit version is an ADVERT | one advert `wl_seat (ver 123456)` | rc 0, 1 session vs rc 3 `NO_SESSIONS` |
| 9 | N38 `boot_changed = False` → `… ; boot = "-"` | "boot = the id of the last BOOT line seen **before its first ADVERT**" | `-- Boot a…a --`, pid 300 advert, pid 301 advert (no second boot line) | `n=2 … boot=aaaa…aaaa` vs `n=2 … boot=-` |
| 10 | N39 `NAME = [A-Za-z0-9_]{1,128}` → `[A-Za-z0-9_-]{1,128}` | "a NAME must fully match `[A-Za-z0-9_]{1,128}`" | `--expect a-b` | rc 2 `MADO_GLOBALS: SETUP bad_expect` vs rc 1 `expected_missing=a-b … MISSING_EXPECTED` |
| 11 | N40 `CLASS_OF.get(name, "other")` → `CLASS_OF.get(name.lower(), "other")` | "Class decision table (name → class; **every other name** is `other`)" | one advert `HYPRLAND_FOCUS_GRAB_MANAGER_V1 (ver 1)` | `class=other` vs `class=focus-grab` |
| 12 | N42 `timeout=30` → `timeout=None` | "a … **timeout** is `SETUP journalctl_failed` (exit 5)" | `--live --journalctl <stub that sleeps 33 s>` | rc 5 `SETUP journalctl_failed` after 30.1 s vs still running at 32 s (rc 124) |
| 13 | N43 `boot = m.group(1); boot_changed = True` → `boot_changed = boot_changed or boot != m.group(1); boot = m.group(1)` | "a SESSION starts at an ADVERT when … **a BOOT line occurred since the previous ADVERT**" (even with the same id) | `-- Boot a…a --`, pid 300 advert, `-- Boot a…a --` again, pid 300 advert | 2 sessions vs 1 session `interfaces=2 adverts=2` |

N42 is also the residual the registration already declares ("a hang (`--live`
timeout) is not exercised by a fixture", `registration.md` §Residuals); the
difference is that the residual is about a *hanging* program while N42 shows the
bound itself is absent, so any live run can hang a caller indefinitely.

## Equivalent mutants

**None in this set.** N15 was the one candidate I expected to be equivalent
(latin-1 vs utf-8/replace can only differ on bytes ≥ 0x80, and every literal in
the accepted-line grammar is ASCII), and the hypothesis is false: `HOST` is
`\S+`, so a host byte that decodes to Unicode whitespace under latin-1
(`0xA0` NBSP, `0x85` NEL) rejects the line while the model's `U+FFFD` accepts it.
Measured, not argued: row 3 above.

## Behavioural duplicate of a frozen control

`N06-count-distinct-only` (`ent[0] += 1` → `ent[0] = 1 if not ent[0] else ent[0]`)
is behaviourally identical to the frozen control `M25-count-always-1`
(`ent[0] += 1` → `ent[0] = 1`): after the first advert both yield 1 and no later
advert changes it, so `count=` is 1 for every name on every input — equal
signature on all 24 fixtures (`logs/_dupsig.log`). It adds no new class and is
reported only for completeness. Every other pair in that log is an artefact of the
duplicate-check corpus: it holds the 8 gen fixtures, 3 sample journals, the kill
fixtures and the empty file, so mutants whose defect lives in the live, usage,
toolarge or badexpect cases behave like the reference *and* like any control that
also behaves like the reference there (e.g. N14 vs M07/M09/M10/…, N17 vs M10,
N18/N37 vs M26, N13 vs M28). Those mutants are all killed by the frozen fixtures
— the authoritative per-mutant failure sets are in the table above — so the
signature coincidence carries no equivalence claim. Only N06/M25 has a proof.

## What this says about the predicate

The 24-fixture lattice is strong on structure (sessions, boots, pid changes,
repeats, noise, sizes, live plumbing: 29 of 42 mutants die) and blind on eleven
**value-domain** classes, each traceable to the generator:

| blind class | generator evidence | survivor |
|---|---|---|
| versions never reach two digits (1–9 only) | `c1-r41-globals.py:376` `randrange(1, 10)`, `:420` `1 + (j * 7) % 9`, `:546` `randrange(1, 9)` | N12 |
| every accepted name is lower-case (bytewise vs case-insensitive sort and class lookup agree) | pools `TABLE`/`COMMON` (`:142-178`) and `syn` (`:363`) are lower-case; the only upper-case name token is the rejected `"A"*32` boot id (`:350`) | N22, N40 |
| `--expect` is always a lower-case name taken from the latest session, or `zz_absent_*` | `:428`, `:573` | N07, N20, N39 (no `-`/case variant, no cross-session name) |
| a repeated BOOT line never occurs (each `boot()` call draws a fresh 128-bit id) | `:367-368` | N43 |
| no session starts after a boot line without a fresh boot line in between | gen1/gen3/gen5/gen6/gen7 put a `boot()` before every session | N38 |
| pids have no leading zeros (`randrange(100, 99999)`) | `:382` (gen) and `:543` (sample journals) | N23 |
| the version field is never 6 digits (only the rejected 7-digit noise) | `:333-356` `noise_lines`, `(ver 1234567)` at `:344` | N24 |
| the log level is never lower-case (`[ERR]`, `[LOG]` only) | `noise_lines` `:337-339` | N16 |
| the host field is always ASCII | `noise_lines`/`session()` use `h` (`:336-354`) and `plazir%d` (`:377`) | N15 |
| a non-UTF-8 byte never sits in an otherwise valid ADVERT (only in the ignored `\xe9\xff` noise line) | `:354` | N15 |
| a live program never hangs (only exit 1 / 9 MB output / writable / env / argv stubs) | `live_stub` `:444-456` | N42 |

Two of these (N39 hyphen, N07 case) are also one-line additions to the existing
`badexpect0` / `expectmiss0` cases; the cheapest six (N07, N16, N22, N24, N39, N40)
are pure text-fixture changes needing no new live plumbing.

## Risks / limits of this evidence

- `--tool` mode satisfies clause a by construction, as in the frozen controls;
  these results say nothing about whether the *delivered* `tools/mado-globals.py`
  (absent at the freeze commit) differs from the reference.
- Kill fixtures are constructed by me and checked against the counter's own
  `model_out`, i.e. they show the model and the mutant disagree, which is exactly
  what a new fixture would score; they are not part of the frozen 24 and were not
  added to the counter (the L1 owns the counter).
- Survivor stability was checked on 4 nonces (5 for N43) of the *frozen* fixture
  set; the missing classes above are structural (value domains), not
  nonce-dependent, so more nonces cannot kill them.

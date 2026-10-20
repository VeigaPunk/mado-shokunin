# GateSwapReceipt — R18-V2 closed: criterion 26's red-before is now a header-bound receipt over a byte-pinned swapped fixture (383 passed / 6 failed, five OM9)

Seat: MadoR19.GateSwapReceipt. Date: 2026-10-20. Lane: `mado-shokunin`
(baseline `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, pre-registration
`17661e0fa83f978fb659f5bb8fef47f0969f6945`). No lane write other than the two
assigned files; no jj command; no live gate.

## §1 Files written

- `.ufo/waves/round-19/gate-swap.sh` (0755, 12151 bytes, sha256
  `c3bce9f30c870b51c8d2b5e78f32c365c96490a83013b35d4fda20fde6e836b4`) — builds
  the fixture, writes it, runs the landed selftest against a /tmp copy, prints
  the header-bound receipt.
- `.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh` (0644, 182300 bytes,
  3776 lines, sha256 `6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e`)
  — the fixture: landed gate with exactly one block exchanged.

## §2 The swap, located by content and pinned by digest

Both blocks were found by their exact start line
`    if ! have git || [ "$omtree" = 0 ] || ! have sha256sum || [ ! -f "$leaf" ]; then`,
required to occur exactly once in each file, with the block running to the first
following `    fi`:

| block | source | committed gate sha256 | lines | block sha256 | bytes |
|---|---|---|---|---|---|
| base (landed) | `17661e0:tools/mado-verify.sh` | `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5` | 3467-3489 | `c86f51b85c9b469409dec4896cf7088ff1fe5d3e3f887fac64b4149ebe939c4a` | 1538 |
| old (defect) | `d9a5a18:tools/mado-verify.sh` | `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` | 3402-3415 | `414bf6ed658c30c6ad3094127e1a85607af51068815268525e422766cdb4e315` | 850 |

Only the `else`-branch body differs; the fixture is byte-exact
`head(base) + old_block + tail(base)`. The decisive landed line, which the old
block lacks, is `tools/mado-verify.sh:3477` at `17661e0`:

```
blob=$(set -o pipefail; tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null \
  | sha256sum | cut -d' ' -f1); grc=$?
```

and its guard at `:3480` `if [ "$grc" != 0 ]; then` → UNKNOWN
(`:3481`). The old block (`d9a5a18:tools/mado-verify.sh:3405-3408`) is

```
local blob sw
blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)
sw=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1)
if [ -z "$blob" ]; then
```

so a failed `git show` hashes empty input (`e3b0c442…`) and the row falls to
`FAIL … local edit` — criterion 26's exact red.

The script refuses (exit 2) on: start marker count ≠ 1 in either file; no
closing `    fi`; identical blocks; any gate/block/fixture sha drift from the
pinned values; an empty-input digest; a committed fixture at REV whose bytes
differ from this run's; and an existing evidence file with different bytes
(never overwritten). Verified refusals:
`bash .ufo/waves/round-19/gate-swap.sh deadbeef` → rc 2,
`gate-swap.sh: REFUSED: cannot resolve 'deadbeef' to a lane commit`;
`--nope` → usage + rc 2.

## §3 Provisional receipt (fixture not yet committed)

Command (run from the lane root, exactly the `cmd=` recorded):

```
bash .ufo/waves/round-19/gate-swap.sh 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
```

stdout, lines 1-2 and last line (`/tmp/gate-swap-receipt.txt`; script rc 0):

```
RECEIPT tool=.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh tool_sha256=6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e measured_commit=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d utc=2026-10-20T17:10:37Z cmd=bash .ufo/waves/round-19/gate-swap.sh 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d
# blocks: base=17661e0fa83f978fb659f5bb8fef47f0969f6945:3467-3489 sha256=c86f51b85c9b469409dec4896cf7088ff1fe5d3e3f887fac64b4149ebe939c4a; old=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98:3402-3415 sha256=414bf6ed658c30c6ad3094127e1a85607af51068815268525e422766cdb4e315; fixture_bytes=182300; provisional=1
…
exit=2
```

`provisional=1` because `9c54c56:.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh`
does not exist yet. This receipt is **not credit under QUALITY 24 until L1
commits the fixture and re-cuts with the committing revision**; the script then
requires `sha256(git show REV:evidence/gate-swap-d9a5a18.sh) == tool_sha256`
and prints `provisional=0`.

Binding path validated in a throwaway `/tmp` clone of the lane (git writes only
in the clone): commit `3202de3d9af8feed133e107ff737045d1abfccee` carrying the
fixture → same header with `measured_commit=3202de3…`, `provisional=0`,
`exit=2`, script rc 0. A second clone commit `58e052a992a9cc6dd27598a8d2976e7eb6ef6b97`
with one byte appended to the committed fixture → rc 2, stdout empty, stderr
`REFUSED: fixture at 58e052a9… has sha256 3011e5c0…, this run builds
6e6782c3… — refusing to bind bytes REV does not carry`.

## §4 Observed tally and failing assertion names

Run of the fixture's own `--selftest` (a /tmp copy; hermetic
`/tmp/w5-mado-m52-selftest.*` roots, no substrate read):

```
MADO_SELFTEST: FAILED — 383 passed, 6 failed
  - R10: derived target equals the recorded gate revision (got '88286b3dfa1f39bde12d416c01d6d424c05989a00c315011daff98004ba65c51' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
  - OM9: no false local-edit claim (unexpected: local edit)
  - OM9: exactly one omarchy UNKNOWN (the failed read) (got '0' want '1')
  - OM9: exactly one omarchy FAIL — the unreproducible sha row (got '2' want '1')
fixtures kept: /tmp/w5-mado-m52-selftest.n4VSXc
exit=2
```

- `383 passed, 6 failed` = 389 assertions; the same suite on the pinned base
  gate (`git show 17661e0:tools/mado-verify.sh` → /tmp, sha `c9fb0cef…`)
  prints `MADO_SELFTEST: 389/389 assertions passed`, rc 0.
- The five **OM9** names are exactly the criterion-26 red set; OM9's source is
  `tools/mado-verify.sh:844-863` at `17661e0`. The sixth failure is **R10**, a
  fixture self-pin: `PIN_MADO` is the sha of the pristine gate's derived target
  (`:598` asserts equality whenever `DEFECT_ID` is unset), and any edit outside
  the marked R7/R8 regression blocks moves it — the gate's own comment says
  "selftest() asserts the derived target equals PIN_MADO on pristine runs, so a
  stale pin is visible" (`tools/mado-verify.sh:1798-1801`). It is therefore
  expected for any swapped fixture and is not a second behavioural defect.
- Round-18 recorded "383/389, five OM9 failures": the 383-passed figure
  reproduces exactly, but `383 + 5 ≠ 389`; the observed run has the same 383
  passes with R10 as the unlisted sixth failure. [INFERENCE] the round-18 prose
  omitted R10; only the count is recorded there, so this cannot be confirmed
  from that note.
- Determinism: two consecutive runs produced the identical fixture sha and an
  identical body except the `fixtures kept:` mktemp path (`…n4VSXc` vs
  `…o79suE`).

## §5 What QUALITY's criterion-26 red sentence should say

The receipt now names `tool_sha256` (the fixture) and `measured_commit`; after
L1's re-cut it satisfies criterion 24 (`git show <measured_commit>:<tool>`
hashes to `tool_sha256`). The red-before text should keep "five OM9 failures"
but state the fixture's total as `383 passed / 6 failed` and name R10 as the
fixture self-pin, so a later reader does not treat it as an unexplained sixth
defect. The fixture is `.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh`;
the receipt is `gate-swap.sh`'s stdout, intended to be captured by L1 into a
committed evidence file (out of this seat's write scope).

## Limits

- The fixture is synthetic gate bytes (`17661e0` + one `d9a5a18` block); it
  exercises the row's decision logic only. No checkout, host config tree or
  live gate was read or run.
- The provisional receipt (`measured_commit=9c54c56…`) is unbound: it cannot
  be credited under criterion 24 until L1 commits the fixture and re-cuts.
- The post-commit binding and tamper refusals were proven in a `/tmp` clone,
  not in the lane (no lane git/jj write, per contract).
- `--selftest` leaves its failing fixture tree at `/tmp/w5-mado-m52-selftest.*`
  by design (the gate prints `fixtures kept: …`); these are scratch, not
  evidence.
- Base/old line ranges are those of the two immutable commits; a future
  rewording of the vs_head block at any revision other than these refuses
  rather than silently swapping a different construct.

## Installs

none

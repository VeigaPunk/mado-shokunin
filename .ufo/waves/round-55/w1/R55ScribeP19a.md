# R55ScribeP19a — C3 correction block (draft, leaf seat)

Seat: R55ScribeP19a. Scope: draft the C3 append-only correction block per registration.md §C3. Base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`; freeze commit `54dacbd843d64ba744cd3f1bdc2ec622e5010039` (read via `git show`, never the working tree). No tracked-file edits, no git mutations, no subagents, no host reads, no hold-out access.

## Deliverables (all in `.ufo/waves/round-55/w1/R55ScribeP19a/`)

| File | What |
|---|---|
| `block.md` | The appended block: heading `## Correction (round 55): P23 supersedes P19`, P23 row (Supersedes `P19`, Source S371, Pin `Hyprland-ConfigActions.cpp:1554-1576`), Q01–Q13 table, "Not claimed" list |
| `after.md` | base bytes (3072) + `block.md` (3598) = 6670 bytes |
| `verify.txt` | output of `verify-block.py` |
| `gen-block.py` | generator: Q rows and the Quote cells come from `frozen-tables.json` `c3.q`, nothing retyped; writes `block.md` and `after.md` |
| `verify-block.py` | verifier: prefix, tail, pin sha, every Q row against `c3.q`, every Q quote against the stripped pin line, P23 tokens and Supersedes |

## Commands and decisive output

```
git -C <lane> cat-file -t 54dacbd8…   -> commit
git -C <lane> show 54dacbd8…:.ufo/waves/round-55/frozen-tables.json | cmp - <worktree copy>   -> FROZEN_MATCHES_WORKTREE
git -C <lane> cat-file -e 3b55b6e9…:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp     -> PIN_AT_BASE_OK
sha256 of pin (base blob) = a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  (= c3.pin_sha256)
base errata tail byte: "\n" (file ends with newline)

python3 -I gen-block.py   -> gen: base_bytes=3072 block_bytes=3598 after_bytes=6670 q_rows=13
python3 -I verify-block.py > verify.txt; rc=1
  PASS pin_sha256
  PASS prefix_identical base=3072 after=6670
  PASS tail_equals_block
  PASS heading count=1
  PASS rows:Q01 … rows:Q13 (13/13, line and quote equal to c3.q)
  PASS pin:Q01 … pin:Q13 (13/13, quote == stripped pin line at that line)
  PASS p23_row_count count=1
  PASS p23_supersedes cell=P19
  PASS p23_tokens missing=[] other=True
  PASS p23_pin_anchor cell=Hyprland-ConfigActions.cpp:1554-1576
  FAIL readme_at_base
  VERIFY: failed=1 names=readme_at_base
cmp <base> <(head -c 3072 after.md)                    -> PREFIX_CMP_OK
cmp after.md <(base + block.md)                         -> AFTER_IS_BASE_PLUS_BLOCK
sha256(after.md) = 36e27fc5da0ed1e85fcec37f278ada9c8718d0ccf20508f737cd05f9d9b46df7
```

verify.txt is the output of the final run (after the last regen; `prefix_identical after=6670`). Re-run `python3 -I verify-block.py` to reproduce; the only FAIL is the README leg above.

## Content decisions

- P23 proposition covers the three arms of `m_passPressed` (`== 1`, `== 0`, `otherwise`/`any other value`/`else`) and the `isMouse` split inside each arm. Source: lines 1556-1569 of the round-52 pin. Else arm: keyboard sends PRESSED then RELEASED (1568-1569); pointer sends PRESSED then RELEASED (1571-1572). It states that P19's "only when `m_passPressed == 1`" is false.
- Quote cell of the P23 row: `if (S.m_passPressed == 1) {` (the Q02 quote). The frozen tables do not specify this cell; I chose it.
- Q table is a separate 3-cell table (`| ID | Pin:line | Quote |`), rows in the frozen grammar `| Q01 | Hyprland-ConfigActions.cpp:<line> | `<quote>` |`.
- "Not claimed": where `m_passPressed` is set (no setter in lines 1554-1576); which values reach `else` at runtime; runtime/client/host delivery; non-author review still required.

## Defects and ambiguities

1. **`readme` leg fails (integration blocker, not in the block).** `corpus/README.md` line 81 names `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` but not `P23`. The registration requires one README line naming the file together with `P23`. The L1 must edit that row at integration; the block cannot satisfy it. `verify-block.py` reports this FAIL on purpose.
2. **P23 row shape is under-specified.** `registration.md` §C3 gives `| P23 | P19 | <proposition> | S371 | Hyprland-ConfigActions.cpp:1554-1576 | … |` with an ellipsis. I used the base table's 7 columns (ID, Supersedes, Proposition, Source row, Pin:anchor, Quote, Support), which the existing entry uses. Quote and Support contents are my choice.
3. **Registration §C3 `p23` leg wording.** It requires `== 1`, `== 0`, `PRESSED`, `RELEASED` and one of `otherwise`/`any other`/`else`. My proposition contains all of them, but the leg does not require the keyboard/pointer split, so that check is not testing the split. The split is in the text because the spec asks for it.
4. **Frozen anchor vs. base P19 anchor.** Base P19 cites `Hyprland-ConfigActions.cpp:1554-1558`; the frozen P23 anchor is `1554-1576`. The correction covers the wider range by design, but the two anchors are not the same span.
5. **`claims-frozen.md` line 60** says the `else` arm is at `ConfigActions.cpp:1566-1569`; the pin's `} else {` is at 1566 and the arm body at 1568-1569. Consistent, noted only.

## Not verified

- Counter `quality/counters/c3-r55-p19.py` and harness `quality/check-r55-controls.py` do not exist in this lane tree in my reads; I did not run them and did not check the C3-CTL controls. The `prefix`, `rows`, `pin` and `p23` legs were checked only by my own verifier, which is a draft and not the frozen counter.
- The `readme` leg was not satisfied (see defect 1).
- No runtime check of `m_passPressed` values; source-level only.
- No hold-out path was looked for or used.

## Tooling

No tools installed or upgraded. Scratch `/fast/scratch/hyaku/mado-r55/R55ScribeP19a/` was used for the base copy and removed before yield.

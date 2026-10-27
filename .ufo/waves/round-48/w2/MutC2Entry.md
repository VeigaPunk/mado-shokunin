# MutC2Entry - C2 row/entry claim evidence, mutation-tested (round 48, w2)

Seat: `MutC2Entry` (leaf). Target: `PRED-C2-r48`, the row/entry data of the C2 deliverable.
This seat scored mutants only; it did not score, re-score, edit or re-register the candidate.

## Identities

| item | value |
|---|---|
| base | `579f694b45c797a9c39761fdb4f9e0a1b71b3585` |
| freeze rev under attack | `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d` (round-48 freeze v1) |
| counter | `quality/counters/c2-r48-xkb-entry.py`, sha256 `4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1` (byte-equal to `l1-draft/c2-r48-xkb-entry.py`) |
| entry draft | sha256 `885a2e4187eeba2919c894e53b11d9a5975f2470e904572d58285e364806ec5a` |
| rows draft | sha256 `951b9f9371a85e456edd82d0edae905c109be758bd55c797c156c7a28de53891` |
| README row | sha256 `cd57260ef9215371742fd487a6334e7b7125ce4f8eb9af329419bcbe75037c45` |
| receipt | sha256 `ab5fa97169306877aeb7218290d99cd4a410639c2833063ca357cb173dfa53cc` |
| mirror baseline | `2f346d756ee9e15a80fd139d7a0341c8ae382118`, parent = base |

## Method

Every clone, commit, log and temp file lived under
`/fast/scratch/hyaku/mado-r48/MutC2Entry/` (1.4 MB total, removed on exit; largest scratch
file 115645 B, an object-store blob). Every writer shell began with `ulimit -f 2048`.

A checked-out clone is impossible under the file-size cap (the lane's round-20..23 fixture
blobs exceed it; `git checkout` aborts and the git index itself fails with "File too
large"), and the counter reads only revision objects, so the mirror was built
revision-addressed: `git clone --shared
--no-checkout`, then `git hash-object -w` per overlaid blob and `git mktree -z` trees from
`git ls-tree -r <base>`; commits have parent = base. The overlay is exactly the recipe of
`l1-draft/c2-mirror.sh`: entry, rows S340-S350 after S339, README index row after the r47
row, `fetch/*`, the receipt and `tools/make-xkb-receipt.sh`. Baseline scores
`clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1 verdict=TARGET_MET`
(`logs/v00-baseline.txt`).

Each mutant changes one source fact by a unique-string byte edit (`replace` anchors are
refused if non-unique). Score command, with `TMPDIR` inside the seat scratch:

```
python3 -I quality/counters/c2-r48-xkb-entry.py --repo <scratch>/clone --rev <variant>
```

Reproduction inputs are retained: `build.py`, `spec-*.json`, `diffs/<variant>.diff`.

## Scores

| # | mutation | class | verdict | killed by |
|---|---|---|---|---|
| v00 | none (draft) | baseline | **TARGET_MET** | all clauses 1 |
| v01 | `No index provided: match only if single layout` -> `... multiple layout` at the same locator | quote text | MISS | `clause=d quote_not_in_pin line=47 pin=xkbcommon-rules.c` |
| v02 | S342 `sha256:95b5d8...` -> S340's `04dfd934...` (valid hex, wrong file) | pin digest | MISS | `clause=c id=S342 pin_sha_mismatch=xkbcommon-include.c` (+ d) |
| v03 | entry table `--options nope:nope ... rc 0` -> `rc 1` | numeric rc (entry) | MISS | `clause=f entry_disagrees ... neg=[True, True, False]` |
| v04 | receipt unknown-option case `rc=0` -> `rc=1` | numeric rc (receipt) | MISS | `clause=f receipt_probe_bad=unknown option(rc_values=[0, 1])` |
| v05 | S346 anchor `xkeyboard-config-rules-evdev:570` -> `xkbcommon-rules.c:570` | rule-mapping locator | MISS | `clause=c id=S346 range_other_pin=xkbcommon-rules.c` |
| v06 | step 4 `+aliases(qwerty)` -> `+aliases(dvorak)` (same `:61-64` locator) | rule mapping prose | **TARGET_MET** | none |
| v07 | step 6 include order `XDG_CONFIG_HOME`, `$HOME/.xkb`, ... -> `$HOME/.xkb`, `XDG_CONFIG_HOME`, ... | include-path order | **TARGET_MET** | none |
| v08 | step 8 S319 claim `reset ... to layout us` -> `to layout br` | held S319 citation | **TARGET_MET** | none |
| v09 | S319 row text `reset to layout us` -> `reset to layout br` | held row bytes | MISS | `clause=h held_row_moved=S319` (+ `clause=d pin_not_cited_by_row=Hyprland-IKeyboard.cpp`) |
| v10 | step 7 `so an unknown model compiles` -> `fails the compile`, same rc/geometry sentence | non-literal outcome | **TARGET_MET** | none |
| v11 | receipt + entry `host.keymap` sha256 -> 64 zeros | positive digest | MISS | `clause=r positive_replay_failed rc=0 sha=efd487a39920` (f stayed 1) |
| v12 | entry table `--rules xfree98 ... rc 1` -> `rc 0` | numeric rc (entry) | **TARGET_MET** | none |
| v13 | entry live-run `73079 bytes` -> `73080 bytes` | non-literal numeric | **TARGET_MET** | none |
| v14 | v08's false claim re-expressed as `` `reset to layout br` at Hyprland-IKeyboard.cpp:101-116 `` | held S319 quote form | MISS | `clause=d quote_not_in_pin line=42 pin=Hyprland-IKeyboard.cpp` |
| v15 | quoted span's locator `xkbcommon-rules.c:1259` -> `:1297` | quote range | MISS | `clause=d quote_out_of_range at=[1259] range=1297-1297` |

Verdict/exit per mutant: MISS = counter exit 1, admitted 0/1; TARGET_MET = exit 0, admitted
1/1. Exact stdout+stderr for all 16 runs is in `logs/`.

## What the kills establish

- Quote **text** (v01) and quote **range** (v15) are bound to the pinned bytes at the stated
  locator; a span that does not occur, or occurs outside the stated range, is a miss.
- Row **pins** are digest-bound to the committed fetch copy (v02), and an anchor locator that
  resolves to a pin the row does not cite is refused (v05) - the rule mapping cannot be
  re-pointed to another file.
- Numeric **rc** is bound in both directions for the three labelled probes: entry text vs
  receipt (v03) and receipt vs the probe window union (v04).
- The receipt's positive **digest** is binding through replay, not through `clause f` alone:
  v11 passes `clause f` (`sha=000000000000 probes=3`) and is still a miss at `clause r`.
- Held **row bytes** are frozen (v09). v14 shows that a false held claim expressed in the
  quote+locator form *is* caught, which isolates the v08 failure to form, not topic.

## The semantic checker gap

### Mechanism

`PRED-C2-r48` validates *forms and bindings*, not the truth of prose:

- `QUOTE_RE` (counter:154-157) only matches a backticked/double-quoted span immediately
  followed by `, <locator>`, ` at <locator>`, `, (<locator>` or `(<locator>`. A backticked
  token with no adjacent locator is never read; `clause_d` (494) additionally skips spans of
  fewer than 2 words (515). v06/v07/v08 are exactly such spans (`+aliases(dvorak)`,
  `$HOME/.xkb`, `br`), so they are out of the checker's reach by construction.
- `clause_e` (543) counts `^N. ` steps and requires one in-range locator per step. It does
  not associate the step's sentence with the locator's content. v06/v07/v10 keep every
  locator in place and pass 9/9.
- `clause_f` (624) binds only three probe token classes - `PROBE_LAYOUT`/`PROBE_VARIANT`/
  `PROBE_OPTION` (166-168) - and the positive RMLVO. The entry's `--rules base`,
  `--rules xorg`, `--rules xfree98`, `--rules nope`, `--model nope`, multi-layout and
  byte/line-count sentences are not compared to the receipt or replay at all. `clause_r`
  (780) replays exactly one positive compile and the fixed three negatives with rc
  `(1,1,0)`.
- `clause_h` (745) compares the held row bytes at base and rev and the held pin digest. It
  never compares the entry's sentence about S319 with the S319 pin.

### Admitted false statements, with the pinned fact each contradicts

All four are one-fact edits inside the otherwise untouched draft; each scored
`clauses=a:1 ... r:1 admitted=1`. The counter cannot tell them from the draft.

1. **v06 - rule mapping inverted.** Step 4 now says any layout maps to
   `+aliases(dvorak)` at `:61-64`. In `fetch/xkeyboard-config-rules-evdev` the layout
   wildcard at line 64 is `* = +aliases(qwerty)` (line 69 likewise); `aliases(dvorak)` is
   not that mapping. `clause c` only checked the anchor's pin and range, `clause d` ignored
   the uncited span.
2. **v07 - include-path order inverted.** Step 6 now puts `$HOME/.xkb` before
   `$XDG_CONFIG_HOME/xkb`. In `fetch/xkbcommon-context.c` the append order is
   `%s/xkb` (XDG, line 259), `%s/.config/xkb` fallback (266), `%s/.xkb` (274), extra (280),
   then the root (318) and legacy root (336). The mutated order is false; the locator
   `xkbcommon-context.c:243-338` still validates.
3. **v08 - held S319 citation inverted.** Step 8 now says the failed-keymap reset uses
   layout `br`. In the held pin `round-46/fetch/Hyprland-IKeyboard.cpp` the reset is
   `m_currentRules.layout = "us";` (line 113) with the other names emptied (109-116). The
   **same false claim quoted with a locator** (v14) is a miss, proving the checker has the
   bytes and only the prose form determines whether they are consulted.
4. **v10 - outcome inverted.** Step 7 now says an unknown model "fails the compile" while
   retaining "`--model nope` returns keycodes `evdev` and geometry `pc(pc104)` ... and
   prints nothing". The receipt's `--model nope` case is rc 0 with `pc(pc104)` (receipt
   lines 165-174), i.e. the mutated sentence is internally contradictory and factually
   false, and still admitted.

Two numeric variants expose the same gap for values the probe list omits:

- **v12** - the entry's `--rules xfree98 ... rc 1` table row flipped to `rc 0` is admitted,
  although the receipt exits 1 for that probe (receipt lines 235-240) and `clause r` does
  not replay it. `clause f` has no `rules` token, so no window ever sees the contradiction.
- **v13** - the live-run byte count `73079` -> `73080` is admitted, although the receipt
  records 73079 bytes / 2090 lines (receipt lines 61-62); only the digest and the three
  probe rcs are bound.

### Position against the frozen instrument

These are not `TARGET_MISSED` results for the candidate: the candidate draft (v00) is
`TARGET_MET`, and each mutant satisfies every clause as written, so nothing here breaks or
narrows the frozen predicate. What is demonstrated is a gap between the predicate and the
claim it is used to license: "admitted=N/1" cannot distinguish the sourced entry from an
entry whose rule mapping, include-path order, held-compositor half and model outcome are
inverted, or whose unprobed rc and byte count are wrong.

Part of this is already declared in the counter's own residuals (script lines 103-112):
"clause c binds URL+digest+name, not the truth of the row's scope sentence"; "a true quote
at a true locator can stand beside a claim it does not support"; "clause d sees only spans
the author cites with a locator"; "clause e counts numbered steps and their pin locators,
not the truth of each step". This seat's contribution is the concrete demonstration that
the residual is load-bearing: **four single-fact inversions and two unattested numbers pass
TARGET_MET**, and the only reason v14 fails is that the author opted into the quotable form.

If the L1 wants the C2 claim's prose to be gated before the data commit, the leverage points
are: bind each numbered step's claim to a quoted pin span (the v14 form already fails on a
false quote), extend the probe-token set to every row of the entry's table (v12), and add
the receipt's byte/line count and the model case to the comparisons (v10, v13). This seat
did not change the predicate, counters, fixtures, claims or target, and did not re-register.

## Evidence retained

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w2/MutC2Entry/`

- `recipe.txt` - scratch layout, exact build and score commands, digests, ulimit/budget record.
- `scoring-table.txt` - the 16 verdicts with the clause line that decided each miss.
- `logs/v00..v15.txt` - exact counter stdout+stderr per run (2.0-3.3 KB each).
- `diffs/<variant>.diff` - the semantic diff of each mutant (byte lengths and hash prefixes).
- `pin-facts.txt` - pinned lines proving each admitted false statement is false.
- `build.py`, `spec-*.json` - reproduction of the revision-addressed mirror and mutants.

No lane file, registry, counter, entry, report, fleet repo, sibling lane or shokuknow was
edited; no lane Git/jj mutation, commit or push was made. No package transaction, GUI,
compositor or host-config change was made. No blocker.

# CritC2Forgery — attack on PRED-C2-r46 (round 46, wave w1, seat CritC2Forgery)

Scope: `quality/counters/c2-r46-input-device-entry.py` (frozen) at the freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`,
base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`. I built revisions that a reader would reject and asked the counter to admit
them. The lane is untouched; every tree below is a throwaway clone, and every artifact needed to re-check the work is in
`.ufo/waves/round-46/w1/CritC2Forgery/`.

## Verdict

12 crafted revisions. **10 were admitted** (`admitted=1/1 verdict=TARGET_MET`); 2 were rejected (both duplicate-URL shapes).

- **4 admitted forgeries are already declared residuals** (F1, F2, F3, F9): the declaration in the counter's docstring is
  accurate, and no clause edit can close them — only the non-author reading can.
- **6 admitted forgeries are NOT declared** (F4, F5d, F6, F7, F8, F10). These are holes in the predicate, not in the reading.
  The two sharpest:
  - **F7**: the revision writes its own live-run receipt under `.ufo/waves/round-46/receipts/` and cites it; clause i reads
    cited receipts "at REV" (counter:680), so the revision supplies the evidence its own claim rests on. The genuine
    `live-devices-host-l1.txt` sits at the same rev, uncited and unreferenced.
  - **F10**: the whole "chain, step by step" section is replaced by 28 `label: receipt:a-b keyword` bullets; the entry keeps
    every cited surface, every Gate quote, the census line and the README row, and PRED-C2-r46 still reports coverage of the
    input-device plane. Coverage becomes a citation index: the claim's substance is deleted, the predicate stays MET.
- **One defense held**: a duplicate-URL registry row carrying the *same* scope prose is rejected (F5, `e:0`). The guard is
  keyed on the scope cell, so the same duplicate passes once the scope prose differs (F5d, admitted).

Impacted axes: **C2 coverage/sourcing** (clauses b, e, f, i, j), and the **observation axis** that the entry's live-run
paragraph stands on (F7). **C1 is untouched** — no revision of mine wrote under `tools/`, and nothing here changes the
capability-acquisition predicate.

## Method

`forge.sh` (in the seat dir) does exactly the registration's positive-control recipe, then applies one patch per forgery:

1. clone the lane `--shared --no-checkout`, `rev-parse --show-toplevel` asserted equal to the clone, detach at the freeze;
2. `python3 -I .ufo/waves/round-46/l1-draft/build-pos.py "$D"` → commit `pos` (positive control: admitted 1/1);
3. `git checkout -f <pos> -- .`, `git apply patches/F<n>.patch`, commit, score with
   `python3 -I quality/counters/c2-r46-input-device-entry.py --repo "$D" --rev HEAD --base b22ea56…`;
4. run the tightening candidates A–G over `pos` and every forgery.

`forge.out` is the run I report. Commit hashes are ephemeral (the clone is deleted); a patch's identity is its sha256 in
`patches/SHA256SUMS`. The counter's own output line for each is in `forge.out`, e.g.

```
F7  ee613765b86348bc e235ca253043 PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=e235ca253043965a5aeffee4639531a47b1e68a6
F5  2a4a9c69eb16567b 827a82da851d PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=827a82da851d1660218c5f12298705860d0e2fba
```

## Findings

| id | what a reader rejects | counter | declared? |
|---|---|---|---|
| F1 | 3-row operator table naming no id whose rows contradict the sourced chain, plus a fabricated mechanism paragraph with a locator | admitted 1/1 | yes — "a decision table naming no id is not bound" (counter:71) |
| F2 | S316's Gate quote is the "did not change" debug log at `Hyprland-InputManager.cpp:1274`, true and unique, saying nothing about device-vs-global precedence | admitted 1/1 | yes — "a true quote at a true locator can stand beside a claim it does not support" (counter:70) |
| F3 | census contradicted in words: "twenty-nine values", defaults "`fr`", "clamped to 0..400", "four decimals" against `device_keys=47`, `default_layout=us`, `scroll_factor_max=100`, `json_scroll_decimals=2` | admitted 1/1 | yes — "a census value contradicted in words rather than tokens is not caught" (counter:71) |
| F4 | the entry's README index row is retargeted: "superseded — read `knowledge/hyprland-monitor-rule-r45.md` instead" (`patches/F4.patch:10`) | admitted 1/1 | **no** |
| F5 | duplicate-URL row, same scope prose as S318 | **rejected** `e:0` | — (defense) |
| F5c | the same row with only the tier cell changed (A→A2) | **rejected** | — (the guard reads the scope cell, not the tier) |
| F5d | duplicate-URL row with distinct scope prose **plus** S162's location rewritten to a different file than its own sha256 and line ranges describe (`patches/F5d.patch:10,18`) | admitted 1/1 | **no** |
| F6 | S316's anchor cell says `Hyprland-InputManager.cpp:1-20` while its claim is the 1213-1295 chain and its bound quote is line 1229 (`patches/F6.patch:10`) | admitted 1/1 | **no** (the anchor is read only for range shape, counter:610) |
| F7 | revision-authored live receipt (`patches/F7.patch:1-22`): "twelve keyboards AGREE on layout `us` … verdict OK" citing only its own file | admitted 1/1 | **no** |
| F8 | two 4-space-indented lines of invented C++ (`patches/F8.patch:13`) that occur in no pin | admitted 1/1 | **no** |
| F9 | OBS S319's gloss contradicts its own quote: the fallback at `Hyprland-IKeyboard.cpp:113` relabelled as "the layout the dump prints when a device block sets `kb_layout`" | admitted 1/1 | yes — claim-to-quote binding (counter:70) |
| F10 | chain replaced by a bare 28-line surface index, 0 numbered steps (`patches/F10.patch:10`) | admitted 1/1 | **no** |

### F4 — the README row can point anywhere

`patches/F4.patch:10` sets the row's second cell to `superseded — read \`knowledge/hyprland-monitor-rule-r45.md\` instead`.
Clause f reads the row prefix, the cell count and the S-token expansion (`cl["f"] = int(len(frows) == 1)`, counter:653), and
T2's supersede/replace/obsolete words are applied to registry rows only. So the corpus index can redirect a reader off the
entry while the entry itself is admitted. A reader following `corpus/README.md` is sent to the round-45 monitor note.

### F5 / F5d — the duplicate-URL guard is scope-keyed

`patches/F5.patch:9` adds an uncited S331 row on the same `ConfigValues.cpp` URL as S318 with the same scope prose →
`admitted=0/1`, `e:0`. The failing check is `same = [j for j, rr in reg_rev.items() for r in rr` … `and r[4] == cells[4]]`
(counter:585): the scope cell is index 4. Changing the *tier* cell instead (A→A2, `patches/F5c.patch`) does not help — also `admitted=0/1`; changing the *scope prose* does:
`patches/F5d.patch:18` and the same revision also rewrites S162's location to `src/config/ConfigManager.cpp`
(`patches/F5d.patch:10`). That URL does resolve — it is an 82-line, 2597-byte file with sha256 `c10dc1ce6602a854…`
(`pos-metrics.out`) — but the row still stores `9db68cf4…`, the legacy file's digest, and an anchor that cites lines up to
2093 in an 82-line file. S162 is never cited, and clause c/e only walk cited ids (`for i in ids`), so both moves are
invisible. Admitted 1/1. Note the positive control already carries 12 URL groups shared
between rows under different scopes (`tighten.out`, `dup_url_groups=12`), so URL sharing is lane practice; the undeclared part
is an *orphan* row and a *falsified* uncited row.

### F6 — the anchor cell names the right file and the wrong lines

`patches/F6.patch:10` rewrites S316's anchor to `Hyprland-InputManager.cpp:1-20 (receipt Hyprland-InputManager.cpp) @ commit
efb50993…`. T4 asks only that a `<receipt>:<a>[-<b>]` range parses and ends inside the receipt (`if not rng or any(int(b or a)
> nlines_`, counter:610). The row's claim is the per-device chain at 1213-1295, the bound quote sits at 1229, and the anchor
points at the file's includes. Provenance reads as "I checked these lines" while naming lines nobody read.

### F7 — the revision forges its own receipt

`patches/F7.patch:1` creates `.ufo/waves/round-46/receipts/live-devices-host-selfforge.txt` with `12 keyboards compared …
verdict=OK exit=0`, and `patches/F7.patch:22` rewrites the live-run paragraph to claim twelve keyboards AGREE on `us`, no
VIRTUAL device, verdict OK, citing that file and nothing else. Clause i's T4 requires the tokens of a verdict line to occur in
"the first cited receipt at REV" (counter:680) — the revision authored it at REV. The genuine `live-devices-host-l1.txt`
(9 AGREE, 1 VIRTUAL, OK) is still present at that rev and simply not cited; no clause requires a cited receipt to predate the
data commit. The trust root is the ten pins, and receipts outside `fetch/` are not pinned.

### F8 — indented code escapes T3

`patches/F8.patch:13` inserts

```
    const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout",
                                                       deviceFallback(devname));
    Config::mgr()->refreshKeyboard(devname);
```

Neither symbol occurs in any pinned source (`pin-greps.out`: 0 in all nine `.cpp`). Clause b's T3 walks fenced blocks only
(`def fences_ok`, counter:423; `blocks.append` is inside the fence branch, counter:430), so a 4-space-indented block is
unfenced, invisible to T3, and enters no other clause. The positive control has 0 indented code lines, so the hole is closed
only by luck until someone writes one.

### F10 — coverage without a chain

`patches/F10.patch:10` replaces everything between "## The chain, step by step" and "## Observations" with a `## Surface
index` of 28 bullets. Numbered steps drop 7 → 0, the entry is admitted, and all 28 clause-j surfaces are `cited=1`. Clause j
binds a locator and a keyword per surface (`cl["j"] = int(raw is not None and surfaces_ok(…))`, counter:686); nothing requires
the sentence the locator sits in, let alone a chain. C2 would then certify "the chain from config to `hyprctl devices -j`" from
a file that contains no chain.

## Smallest safe corrections (A–G)

`tighten.py` implements these against the counter's own helpers (it imports the frozen module, so parsing cannot drift). It
prints one line per rev; `tighten.out` is the run. **The positive control passes all seven; each undeclared forgery fails
exactly the intended one** (F5d fails two, F5 as well — it is an orphan).

| check | rule | kills | pos |
|---|---|---|---|
| A | each Gate quote's receipt line lies inside one of the ranges of that row's anchor cell | F6 | pass |
| B | the README index row's second cell is a status token (`draft`/`held`/`adopted`) and the row carries no supersede/replace/obsolete/instead/deprecate word | F4 | pass |
| C | every `.ufo/waves/round-N/receipts/<file>` path the entry cites exists at the **freeze** commit with identical bytes | F7 | pass |
| D | a 4-space-indented code run must occur verbatim in a pin, i.e. T3 applied to indented blocks as well as fences | F8 | pass |
| E | a registry row the entry never cites is byte-identical to its base row | F5d (S162) | pass |
| F | every registry row born at REV is cited by the entry (no orphan rows) | F5d, F5 (S331) | pass |
| G | every clause-j surface is cited on a line that is a numbered chain step (`^\d+\. `), and the entry has ≥ 5 such steps | F10 | pass |

Observed (verbatim from `tighten.out`, same revs as `forge.out`):

```
072da817379c A=1 B=1 C=1 D=1 E=1 F=1 G=1 PASS        <- positive control
7f797e985bd4 A=1 B=0 C=1 D=1 E=1 F=1 G=1 FAIL         <- F4
01d58ac5fc74 A=0 … FAIL                                <- F6
e235ca253043 … C=0 … FAIL                              <- F7
2df1d12828fa … D=0 … FAIL                              <- F8
ce832b6daae3 … E=0 F=0 … FAIL                          <- F5d
e6b35274af35 … G=0 FAIL                                <- F10
```

Each is a clause-sized edit, computed from git blobs with no typed locators. A is deliberately narrow: it does not catch F2
(quote at 1274 still inside 1213-1295), because a quote can be in range and still irrelevant — that stays the author's
reading. C is the one I would put first: it converts "the revision supplies its own evidence" into "evidence predates the
data", which is the property the whole sourced axis rests on. D and G are cheap and mechanical.

## Residuals confirmed, not closed

F1, F2, F3 and F9 are admitted and are exactly what the frozen docstring already declares: the claim-to-quote binding, the
unbound decision table, and the word-form census contradiction (counter:70-72). They are not defects of the predicate's
intent — they are the boundary of what a syntactic counter can do, and the lesson should keep them as the non-author
reading rather than as a clause to add. F1's fabrication is worth keeping as a fixture for that reading: "recompiles every
keyboard keymap on a hotplug and writes the compiled keymap back into the config store" (`patches/F1.patch`) appears in no
pinned file (`pin-greps.out`), and the claim that the global scroll factor "is clamped the same way" contradicts
`Hyprland-InputManager.cpp:1379-1380`, where the printed value is set only inside `deviceConfigExplicitlySet(devname,
"scroll_factor")`.

## Reproduction

```
sh /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/CritC2Forgery/forge.sh
```

Seat contents: `forge.sh`, `forge.out` (counter line per patch + A–G table), `patches/F*.patch` + `SHA256SUMS`,
`tighten.py`, `tighten.out` (A–G detail incl. `dup_url_groups`), `quote-check.py` + `quote-check.out` (every quote in this
report: whitespace-collapsed occurrence, ≤ 25 words, computed locator), `pin-greps.out` (pin evidence for F1, F2, F8, F9),
`pos-metrics.out` (indented-code and numbered-step counts for pos/F8/F10, and one network fetch of the F5d URL with its
size, digest and line count).

No host mutation, no compositor call, no package transaction, no write outside this lane's seat dir and the scratch tree
(`/fast/scratch/hyaku/mado-r46/CritC2Forgery`, deleted). Tools installed: none.

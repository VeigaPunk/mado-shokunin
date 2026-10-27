# ScoutEntryLocators — w2 falsification: C2 entry line/quote verification

Seat: ScoutEntryLocators (leaf, no subagents). Wave: mado round 48 w2 (FALSIFY, policy v1).
Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## Method

Built the replay tree the freeze will commit: lane at base + l1-draft overlay
(`xkb-keymap-compile-r48.md` → `corpus/knowledge/`, `rows-c2.md` spliced after the S339 row of
`corpus/SOURCES.md`, `readme-row.md` spliced after the `knowledge/xdg-terminal-selection-r47.md`
index row of `corpus/README.md`, 14 `fetch/` pins, the xkbcli receipt, the receipt generator),
composed with pure `git mktree` plumbing (working-tree checkout of the lane exceeds the 1 MiB
writer guard), committed as mirror `0e33a1fdb9965472a93b9d61093df91299a01010` in a `--shared -n`
clone. Every number below was recomputed from committed bytes (mirror tree + lane `fetch/` bytes)
with a fresh verifier (`verify_locators.py`, written for this seat), then cross-checked by running
the frozen counter `quality/counters/c2-r48-xkb-entry.py` on the same mirror, and by an
independent live replay of `xkbcli compile-keymap` (read-only verbs only; TMPDIR/HOME/
XDG_CONFIG_HOME isolated under the seat scratch).

No installs, no pacman, no host mutation. Scratch peak 860 KB, largest single file 251 KB
(overlay `SOURCES.md`); every writer shell ran under `ulimit -f 2048`.

## Results — all locator/quote/step/held/receipt checks pass

| check | result | evidence |
|---|---|---|
| row pin digests | all 14 round-48 fetch pins hash-match a `sha256:` digest their row records | `ScoutEntryLocators/verify-locators.txt`, `pin-sizes.txt` |
| pin byte/line counts | every size/line count stated in rows S340–S350 equals the committed pin (74868 B/2125 … 14270 B receipt) | `ScoutEntryLocators/pin-sizes.txt` |
| entry pin locators | 45 locators on unfenced entry lines; every one resolves to a fetch pin and stays inside its line count (e.g. `rules.c:520-527/2126 IN`, `context.c:243-338/593 IN`) | `ScoutEntryLocators/locator-table.txt` |
| entry quotes | 18 quotes (2–10 words, all ≤ 25); every one occurs verbatim (whitespace-collapsed, word-bounded) in its pin with an occurrence line inside the stated range | `ScoutEntryLocators/quote-table.txt` |
| continuation citations (invisible to the counter's `LOC_RE`) | manually verified: `messages-codes.h:150` = `XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,`; `rules-evdev:61-64` layout wildcard, `:109-175` symbols wildcard (`pc+%l%(v)` at 175); `Hyprland-IKeyboard.cpp:67-73` (five C-string names), `:75` (`XKB_CONTEXT_NO_FLAGS`) at the held r46 pin | `ScoutEntryLocators/verify-locators.txt` run log |
| row anchor ranges | every anchor range resolves to one of the row's own pins and is in range; S350 declares `whole file` | `ScoutEntryLocators/verify-locators.txt` |
| numbered steps | 9 steps (`^N. `); each cites ≥1 in-range locator on a row-cited pin | `ScoutEntryLocators/verify-locators.txt` |
| held reference | rows S318/S319 + `hyprland-input-devices-r46.md` byte-equal base↔mirror; held r46 pins exist with row-recorded digests; r46 `:69` ("The XKB compile itself is not reproduced") and `:33` (step 4, the `us` reset) still exact | `ScoutEntryLocators/verify-locators.txt` |
| receipt binding | receipt sha256 `ab5fa971…dfa53cc` = S350's recorded digest; `fetch/` copy byte-identical to `receipts/` copy; ≥512 B | `ScoutEntryLocators/receipt-sha.txt` |
| receipt content | version triple 1.13.2 (xkbcli + libxkbcommon 1.13.2-1 + xkeyboard-config 2.48-1); positive `br`+`compose:caps` rc 0, keymap sha256 `efd487a3…6fce81`, 73079 B / 2090 lines; negatives `--layout zz` rc 1, `--variant nope` rc 1, `nope:nope` rc 0 with XKB-595 | `ScoutEntryLocators/live-replay.txt` |
| independent live replay | positive digest reproduced exactly (`efd487a3…`), 2090 lines / 73079 B, empty stderr; negatives rc (1,1,0) with XKB-338/661/769/822 and XKB-661/769/822 and XKB-595; KcCGST `pc+br+inet(evdev)+compose(caps)`; include-path precedence probes reproduce (XDG→rc 0, `HOME/.xkb`→rc 0, byte-identical, neither→rc 1 XKB-338) | `ScoutEntryLocators/live-replay.txt`, `precedence-replay.txt` |
| URL pinning | all 10 upstream URLs ref-pinned to `xkbcommon-1.13.2` / `xkeyboard-config-2.48`; S350 own-work with digest+pin; no branch refs | `ScoutEntryLocators/url-pinning.txt` |
| README row | three index cells, covers S340–S350 (plus held S318/S319), no redirect words | `ScoutEntryLocators/url-readme-entry-values.txt` |
| entry-stated values | version beside `xkbcli`, digest, byte/line counts, and each probe rc stated on unfenced lines | `ScoutEntryLocators/url-readme-entry-values.txt` |
| frozen counter cross-check | `PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=0e33a1fd…` on the same mirror (its own clause-r replay also `ok sha=efd487a39920 neg=(1,1,0)`) | `ScoutEntryLocators/counter-mirror.txt` |
| content spot-checks | meson defaults `evdev/pc105/us` at `:32-59`; "More/Less layouts than variants" at `rules.c:520-535`; "Cannot load XKB rules" at `:1986-1992`; "No components returned" at `:2028-2036`; ids 661/769/822 registered; `br` has 11 `xkb_symbols` maps; host `input.conf` hashes match the entry (`3769c92a…`, `bee5aa68…`, `kb_layout = br`/`compose:caps` lines 10–11, omarchy default `us` at line 3) | run log in `live-replay.txt`, `host-input-conf-sha.txt` |

## Finding (1) — stale lane-document locator in the entry

- **What:** the entry's `ground:` line cites `` `corpus/README.md:112` `` with the parenthesized
  quote "Still open: the XKB compile itself". At base that citation is exact (README:112 is the
  round-46 Frontier bullet). The C2 data itself splices the README index row at line 76, shifting
  the Frontier section down one line: at the data commit (mirror `0e33a1fd…`) line 112 is **blank**
  and the bullet containing "Still open: the XKB compile itself …" sits at **line 113**.
- **Counter coverage:** none — the frozen counter refuses lane-document locators only for
  counter-quotes (`QUOTE_RE` needs a quote *followed by* a locator; here the locator precedes the
  parenthesized quote), and non-pin locators are skipped, so `admitted=1/1` stands with the
  defect in place. Verified against my mirror run.
- **Impact:** documentation accuracy only. The claim is true (the gap was held open at base, and
  base:112 proves it); a reader following the citation at the data tip lands on a blank line.
  No counter clause, pin, digest, range, quote, step, held row, or receipt value is affected.
- **Smallest safe correction (pre-data; entry edit only):** renumber the citation to
  `` `corpus/README.md:113` `` in `xkb-keymap-compile-r48.md`, or drop the line pin and keep the
  quoted text. No predicate, counter, fixture, row or claim change is needed; the counter will
  still admit.

## Notes

- Pin line counts are newline counts (`wc -l`-equivalent); the counter's `split("\n")` counts are
  one higher on newline-terminated pins — consistent with every range check, no boundary locator
  sits at the last line, so the convention is moot here.
- The `us:2` tokens in steps 5/8 are KcCGST group-index syntax picked up by the locator regex,
  not citations.
- The receipt's `taken: 2026-10-27T00:08:08Z` UTC equals 2026-10-26 local — consistent with the
  entry's "measured 2026-10-26".
- Tooling installs: none. Host guard: no compositor/service mutation, no input injection, no GUI
  launch; `xkbcli` used only as `compile-keymap`/`--test`/`--kccgst`/`--version` read verbs.

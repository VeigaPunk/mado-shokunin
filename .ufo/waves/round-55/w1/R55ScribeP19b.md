# Round 55 · w1 · seat R55ScribeP19b — C3 append-only correction (P19 → P23)

Scope: draft the C3 correction block per `registration.md` §C3 and `claims-frozen.md` C3, appended after the unchanged base bytes of `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` at base `3b55b6e91e40f455dd56b2985e4ffc087ada92d5`. Seat is a draft; the L1 integrates. No tracked file was edited, no git/jj mutation, no host read, no subagent, no tool installed.

## What I did

1. Read `registration.md` (§C3 grammar, legs, controls), `claims-frozen.md` (C3 predicate and kill rule), `frozen-tables.json` (`c3` block).
2. Pulled the base bytes with a read-only object read:
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 3b55b6e91e40f455dd56b2985e4ffc087ada92d5:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` → 3072 bytes, ends `…not the rest of that entry.\n`.
3. Checked the pin: `sha256sum .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` = `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`, equal to `c3.pin_sha256`. Read pin lines 1550–1580 and grepped `m_passPressed` in the pin `.cpp` and `.hpp`.
4. Wrote `gen.py` (generator): reads `c3.q` from `frozen-tables.json`, asserts pin sha, asserts every quote equals the stripped pin line at its line and contains no `|` or backtick, emits the 13 Q rows from the table (never retyped), and writes `block.md` and `after.md = base + block`.
5. Wrote `verify.py`: byte-prefix proof, after = base + block, pin sha, heading, 13 Q rows (id/line/quote byte-equal to frozen and to the stripped pin line), P23 row (Supersedes `P19`, `m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED`, an else-arm token, pin anchor). Writes `verify.txt`.
6. Ran both. Commands and decisive output:

```
$ python3 -I gen.py
base_bytes=3072 block_bytes=4987 after_bytes=8059

$ python3 -I verify.py
PASS base_sha256 764f48679447fd62858e9773607a3c0bee5395b6182bdf9f30f5d7c95f4d0b65 bytes=3072
PASS prefix_identical after_bytes=8059
PASS after_is_base_plus_block block_bytes=4987
PASS pin_sha256 a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637
PASS heading_correction_round55
PASS q_row_count found=13 unique=13
PASS rows:Q01 line=1554 … PASS rows:Q13 line=1576   (each with PASS pin_quote:Qnn)
PASS p23_row_present count=1
PASS p23_supersedes_P19 supersedes=P19
PASS p23_has:m_passPressed / == 1 / == 0 / PRESSED / RELEASED / p23_has:else_or_other / p23_pin_anchor
INFO readme_p23_line_in_corpus_README=False (integration surface; L1 edits it, seat does not)
VERDICT OK          (exit 0; re-run identical)
```

I did not run the C3 counter (`quality/counters/c3-r55-p19.py`, not present in the tree at this moment) or `quality/check-r55-controls.py --claim c3`. Those are L1 integration checks. My `verify.py` is the seat's own proof, not the frozen counter.

## Deliverables (absolute paths)

Directory `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ScribeP19b/`:

| file | sha256 | note |
|---|---|---|
| `block.md` | `fbe887ad8a4d39847b24f9f401662e382ff48d4497bcee85f01499c904449586` | 4987 bytes; the appended block (starts with a blank line) |
| `after.md` | `b3d1f1eb02ebcab9ed5251c13df71d600efaf41b2788f5e884eedda14c9f440e` | 8059 bytes = base (3072) + block |
| `verify.txt` | `b3288b35692c204436346dff85947f9b6f4f4c024cb7f0241ced3010a9d4f8c1` | output of `verify.py`, VERDICT OK |
| `gen.py` | `8caab0d29a88efae07556161accc2093d8f3be95cacd7a558d1a3ddaa4c6cbc6` | generator (Q rows from `frozen-tables.json` c3.q) |
| `verify.py` | `bb1d81d5cb1454574244e7bd998cd5aa3ce05eb5ae3659f1594f26b367a197d1` | verifier |

Report: this file. Scratch `/fast/scratch/hyaku/mado-r55/R55ScribeP19b/` was removed before yield (it held only a copy of the base bytes; `gen.py` and `verify.py` regenerate it from `git show`).

## The block (shape)

- Heading `## Correction (round 55): P23 supersedes P19`.
- Prose first: scope (P23 supersedes P19 only; source-level only); why the old P19 wording was false (cites only Q01–Q03, Q08–Q10, Q02, Q05); what stays unclaimed.
- P23 row in the seven-column base header: `| P23 | P19 | <proposition> | S371 | Hyprland-ConfigActions.cpp:1554-1576 | Q01 to Q13 below | direct: … runtime delivery not claimed. |`
- Branch table (`== 1` → keyboard PRESSED / pointer PRESSED, Q02–Q04; `== 0` → RELEASED, Q05–Q07; any other value / `else` → keyboard PRESSED then RELEASED, pointer PRESSED then RELEASED, Q08–Q12).
- Q table `| ID | Pin:line | Quote |` with Q01–Q13 generated from the frozen table.

## Defects, ambiguities and inputs that show them

1. **README leg is not met by this seat (integration item).** `corpus/README.md` line 81 names `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` but not `P23`; `verify.py` reports `readme_p23_line_in_corpus_README=False`. `registration.md` §C3 requires a README line naming the file together with `P23` (`readme=bad` otherwise). `claims-frozen.md` says C3 reads "`corpus/README.md` (its row)" yet the same file lists README rows as integration surfaces that are "not claim evidence". The contract does not say which of these binds the seat. The L1 must edit that row; I did not touch it.
2. **P23 quote cell is unspecified.** The §C3 template has `…` in the quote and support cells. I used `Q01 to Q13 below` (no backticked quote, so no quote-cell check can misfire) and a `direct:` support cell. The L1 should confirm this reading.
3. **Old P19 wording is false on the pin (Q-row evidence).** P19 says `Actions::pass` sends a PRESSED keyboard key only when `m_passPressed == 1`. Q09 sends a keyboard key PRESSED in the arm opened by Q08 (`} else {`), and Q10 sends the matching RELEASED; the else arm is therefore a second source of keyboard PRESSED. The old quote (Q01–Q03) covers only the `== 1` text.
4. **Possible runtime relevance of the default (observation, not claimed).** The pin's header `Hyprland-ConfigActions.hpp:114` declares `int m_passPressed = -1; // -1 = dynamic (press+release), 0 = released, 1 = pressed`. The pin's `sendKeyState` (lines 1603–1615) sets it to 1 or 0 around `pass` calls and restores it. Whether -1 or any other value reaches `pass` on a runtime path is not established by the pinned bytes I read; the block says so in its unclaimed paragraph. This is the open question the seat was asked to leave unclaimed.
5. **Other `m_passPressed` readers in the pin are outside P23.** Lines 1487/1492 (another function, same shape, `m_lastCode`/`m_lastMouseCode`) and 1634/1640 (global-shortcut event) read the same field. P23 is scoped to 1554–1576 as frozen; they are not claimed.
6. **Base entry's own limit still applies.** The base entry requires a non-author source-truth review before admission; the frozen `claims-frozen.md` says the independent sentence-to-pin audit is w2. The block's unclaimed paragraph repeats that.

## Not verified

- Did not run the frozen C3 counter or the C3 control harness; the counter file is not in the tree yet. The controls (C3-CTL-1..6) are not run by me. By construction: CTL-1 (block removed) fails `rows`/`p23`; CTL-2 (one byte of the P19 row) fails `prefix` because the block is appended after unchanged bytes; CTL-3 (Q09 quote altered) fails `rows:Q09`; CTL-4 (Q08–Q12 removed) fails `rows:Q08`; CTL-5 (P23 cell = P19 sentence) fails `p23` because it lacks `== 0`, `RELEASED`, and an else token; CTL-6 (README without P23) fails `readme`. These are reasoned, not observed.
- The S371 registry row and its pin mapping in `corpus/SOURCES.md` were not opened; the block reuses the base row's `S371` as written.
- Runtime delivery of any branch was not checked and is not claimed.
- The sealed hold-out was not looked for and not used (C2 only; not in my seat's inputs). I did not encounter any hold-out path.
- No host reads were made (`hyprctl` and `~/.config/hypr/input.conf` not touched; not needed for C3).

## Tooling

None installed. No pacman, uv, npm or binary channel used. `RULES.md` not needed because no tool was installed.

## Git state

No git mutation. Read-only `git show` of the base blob only. `git status` from the lane shows my seat directory as untracked (expected; the L1 integrates).

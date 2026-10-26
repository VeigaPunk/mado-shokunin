# ScrErrataR1 - R1 erratum for `corpus/knowledge/hyprland-input-devices-r46.md:57`

Round 47, w1, lane `mado-shokunin`. Status: complete.

## Behavior

Drafted the append-only erratum block for the round-46 entry, to be appended verbatim after line 73 (the entry is 73
lines; nothing else in it is edited). The block is `.ufo/waves/round-47/w1/ScrErrataR1/erratum.md` and starts
`## Erratum (2026-10-26, round 47)`. It corrects two things at :57 and leaves the observation itself standing:

1. **The two-config fact.** :57 says the host has "one `input` block in `~/.config/hypr/input.conf`". True of that
   file alone; false of the effective chain. `~/.config/hypr/hyprland.conf:11` sources
   `~/.local/share/omarchy/default/hypr/input.conf` (sha256 `bee5aa68...`, `input {` :2, `kb_layout = us` :3) and
   `:17` sources `~/.config/hypr/input.conf` (sha256 `3769c92a...`, `input {` :3, `kb_layout = br` :10). Two `input`
   blocks reach the compositor; the earlier names `us`. The last-wins explanation is grounded in the landed tool:
   `tools/mado-devices.py:418-419` (parse loop over config texts in order) and `:334`
   (`st.globals[key[len("input:"):]] = rhs`, a plain dict assignment).
2. **The citation.** :57 cites only `.ufo/waves/round-46/receipts/live-devices-host-l1.txt`, which is the *draft*
   tool's run: its header names `.ufo/waves/round-46/l1-draft/mado-devices.py` sha256 `b229efd0...`, 135 changed
   lines (30 removed, 105 added, 9 hunks) away from the landed tool. Corrected citation:
   `.ufo/waves/round-46/receipts/live-devices-host-r46.txt` (sha256 `0c749e1d...`), the run of
   `tools/mado-devices.py` (sha256 `3a803689...`) with both configs passed; its header records both config hashes and
   the chain (":5").

What stands: both receipts print the same fourteen device lines and the same verdict (`keyboards=10 agree=9 differ=0
fallback=0 virtual=1 mice=4 mice_differ=0 ... verdict=OK`); the "no `device` block" half holds in both files
(`device_blocks=0` each). The r46 receipt adds `MADO_DEVICES_SELFTEST: 59/59 passed`, absent from the L1 receipt. So
the entry's numbers (nine AGREE `br`, fcitx5 VIRTUAL, four pointers at -1.00) are unchanged and now rest on the
landed tool's receipt.

## Gates

- `verify.sh` re-ran every locator/hash/quote check: **48/48 passed**, rc=0 (`verify.out`). It recomputes locators
  with `grep -n`, re-hashes six files, and asserts both quotes are <= 25 words and present in the delivered block.
- Quotes: Q1 "one \`input\` block in \`~/.config/hypr/input.conf\`, no \`device\` block" at entry :57 (8 words);
  Q2 "# chain: ~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf"
  at r46 receipt :5 (12 words). Both locators computed, not typed.
- The entry is untouched: 73 lines, `git status --porcelain` empty for it (read-only git).

## Touched surfaces

- `.ufo/waves/round-47/w1/ScrErrataR1.md` (this report)
- `.ufo/waves/round-47/w1/ScrErrataR1/erratum.md` - the block for the L1 to append
- `.ufo/waves/round-47/w1/ScrErrataR1/verify.sh`, `verify.out` - the re-runnable check and its receipt

No tracked file, no host config, no git index, no scratch dir left behind (`/fast/scratch/hyaku/mado-r47/ScrErrataR1`
removed; `verify.sh` keeps its own `mktemp -d` under `TMPDIR` and deletes it on exit).

## Commands that produced the facts

- `sha256sum` over `tools/mado-devices.py`, both receipts, both configs, the draft tool.
- `grep -n '' corpus/knowledge/hyprland-input-devices-r46.md | sed -n '50,66p'` - locates :57; `grep -n` for
  `input.conf`, `one \`input\``, `device block` in the entry (only :57 carries the claim).
- `grep -n 'source' ~/.config/hypr/hyprland.conf` - lines 11 and 17.
- `grep -n ''` on both input configs; block counts via `grep -cE '^\s*(input|device)\s*\{'`.
- `diff -u` draft vs landed tool, counted by awk (30/105, 9 hunks); `grep -n` for the merge loop and assignment.
- `diff` of the two receipts' `MADO_` bodies - identical except the selftest line.

## Out of scope / limits

- I did not rerun the two-config join: the r46 receipt is the witness. Only config hashes, `source` lines, block
  counts and the tool's merge code were re-read on the host today.
- No SOURCES row was opened (R1 is an erratum, not new evidence); no other round-46/45 artifact touched.
- No tools installed or upgraded. No pacman. No compositor call, no process started, no socket opened.
- Only reads of `~/.config/hypr/*` and `~/.local/share/omarchy/default/hypr/input.conf`; no home listing committed.

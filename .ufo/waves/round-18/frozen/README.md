# Frozen tripwire replay (round 18)

Five byte-exact OMP incident transcript lines (SHA-256 pinned), replayed with
`python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`.

- `inputs/r15-libinput-events.jsonl` — R15-V1 anchor line 54 `call_38165` (`sudo pacman -S ... libinput`), plus 4 clean bash controls.
- `inputs/r13-global-capture.jsonl` — R13 host mutation line 19, plus 4 clean controls.
- `inputs/r14-review-source-bar.jsonl` — R14 `pacman -Sw` line 41, plus 4 clean controls.
- `inputs/r14-source-safety.jsonl` — the two R17-V4 variable-recipe known misses (152, 155), plus 4 clean controls.
- `inputs/r13-root.jsonl` — the R17-V4 helper-function known miss (470), plus 4 clean controls.

`provenance.json` binds each input to its absolute transcript path, source SHA-256 (equal to round-17
`evidence/session-index.json`) and `[snapshot_line, source_line]` pairs. Expected findings came from the
committed receipts (`tripwire-{r13,r14,r15,anchor-r15}.txt`, tool `962919ce...`) and were cross-checked
against `oracle-r13-r14.json` / `oracle-r15.json`, never by running the tool on this snapshot. Expected:
scan exit 1, label `findings`, 8 findings (2 R15 anchor, 4 R13, 2 R14), 3 known misses. `OutputSpec:65`
is skipped (792,861 bytes > 256 KiB per-line limit); the wlr-protocols install stays covered by R14.
Re-pin: copy lines byte-exactly, update digests in `expected.json` and `provenance.json`, re-derive
`expected_findings`/`known_misses` from a current-tool receipt; a `known_misses` finding means the miss
was fixed — remove it and re-pin. Never edit an input without updating both digests.

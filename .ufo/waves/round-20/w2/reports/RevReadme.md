# RevReadme — partly falsified: round-20 frontier and navigation pass, but the coverage row omits its Sources cell

## Findings

### Low — `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:46` has only two cells in a three-column coverage table

The header at `corpus/README.md:10` is `Note | Holds | Sources`. The new round-20 row at line 46 has only a note cell and a holds cell; `S099–S112` is appended to the holds text, and the Sources cell is absent. Neighboring rows, including line 45, have all three cells. This leaves the source/recheck column blank for the newly indexed note.

Evidence:
- Command `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --no-ext-diff --unified=8 9c54c56 a4046a8216080d4004de3f268c62cf142095ac07 -- corpus/README.md` output: `corpus/README.md | 22 ++++++++++++++++++++++`; the added row is at `README.md:46` above.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:10,45-46`; README sha256 `3b3ccdbca8cf6b67c961b15a890dc7f090a6863335468180ccebdcc0ce1026b2`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/tripwire-precision-r20.md:1` does list `source: S099 ... S112`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:111-124` contains the corresponding registry rows. `sources-census.sh validate` returned `file ok` and `exit=0` in the harm-watch run.

The navigation counter only extracts note paths from the first cell (`SCORECARD.md:76-88`), so its successful count does not validate the row's cell structure. No Markdown renderer was run; any renderer's treatment of the omitted cell is [INFERENCE], but the source row's missing third field is directly visible.

## Verification

- Ran the pinned harm-watch copy in the isolated clone, not from the lane worktree:
  `ROOT=/tmp/mado-r20w2-RevReadme OUTDIR=/tmp/mado-r20w2-RevReadme/out/harm bash /tmp/mado-r20w2-RevReadme/.ufo/waves/round-20/harm-watch.sh a4046a8216080d4004de3f268c62cf142095ac07`
  (copied from `git show a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-20/harm-watch.sh`; copied script sha256 `694e1f1afd615e846f10ead79bf94ef675a54524eea2c157d32cb652ef35a9b8`). Output: `HARM_WATCH: PASS`. Summary: `runs=21 ok=20 fail=0 skip=0 baseline=1 blocking=0`; summary sha256 `a4ad8ccd27b45050b8a79e66fff6f9c5026f8dc26b1372d21de0e80dd9bd89c0`.
- The navigation receipt `/tmp/mado-r20w2-RevReadme/out/harm/harm-nav-fleet-round-1.txt` reports `revision=a4046a8216080d4004de3f268c62cf142095ac07 indexed=35/35 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` and `exit=0`; sha256 `be4f9472a3a72243063d7850ed4318a5383543f31bb7b4933e81385cdc8b1ade`.
- The same run's precision command exited 0. The committed frontier text at `corpus/README.md:152-157` is consistent with `tripwire-precision-r20.md:18-20` (observed/lead and pure-data no-row meanings) and `QUALITY.md:232-249` (criterion 29 fail-closed harnesses). `SCORECARD.md:1329` records the 29/175 → 172/175 result. Relevant source hashes: tripwire note `199002895c14733a2da8b9da0c828f953ca66402dc4da564e21ab6b61a2058bf`, QUALITY `4da2cd62576ebea5a80028391e3a657ffa0505dd950f7ae563abb67cf47f4dd4`, SCORECARD `0b03337880a502b9984ae7b606000a398df536cdb71faced901fecdc9e647ed0`.

## Limits

- No LSP device is mounted: reading `xd://lsp` returned `No such tool: xd://lsp`. Therefore references/definition/diagnostics were unavailable. Grep was used only to locate text; the findings above are grounded in direct file reads, the committed diff, and command receipts.
- The harm-watch navigation check establishes admitted-note path reachability, not coverage-table column completeness; its counter's regex counts only the note-path cell.

## Installs

none
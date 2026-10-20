# ScribeMistakes — four round-19 mistake rows drafted; one red reproduced, three fixes pending their round-20 checks

Scope: drafted `.ufo/waves/round-20/w1/drafts/ScribeMistakes.md` (M1-M4 table). No lane file, fleet file or check was edited. No git/jj write was run in the lane. Nothing was executed except read-only git, `sha256sum`, and `python3 -I … --scan` on copied text fixtures.

## Findings

1. **M1 (precision traded for recall) is reproduced.** `/tmp/scribe/fx/data-only.jsonl` is the round-19 `py-lead-cross-cell-literal.jsonl` envelope with `code` replaced by `BLOCK=frozenset(['pacman','-Q','hyprland'])` (sha256 `769e25f2…`). Tool copies: `1f7f995` sha `367be947…`, `9c54c56` sha `c1ae45a7…` (both via `git show`). `--scan` at `1f7f995`: `MADO_TRIPWIRE: findings`, `findings=1`, `package_query` rule `pacman:-Q`, line 1, no evidence key. At `9c54c56`: `MADO_TRIPWIRE: clean`, `findings=[]`. The fixture code was never executed.
2. **M2 (fail-open isolation) is cited, not reproduced.** The harness lives at `/tmp/sgp/inns.sh` in the transcripts, not in the lane, and the host pause forbids running it. Evidence is `corpus/lessons/round-19-verifier-spotcheck.md:124`, `corpus/lessons/round-19.md:87,127-129,145`. The captured-by is self-report only.
3. **M3 (stale tallies) is checked for two of three items.**
   - 154 entries in `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` (parsed JSON `files` list; the receipt's sha256 is `9572d2a6…`). The lesson prose says 155.
   - Any-line S096 at `b435568` over the 13-file set is 8 with and 5 without, the five names matching the verifier's list. First-line 6/13 is not re-derived.
   - Conflict, not resolved: `.ufo/waves/round-19/w2/reports/RerunC2.md:98` says "8/13 credited files carry no S096 citation", the same number with the opposite polarity. The b435568 recount does not support that wording. [UNK] whether RerunC2:98 was true at its `01b8094` snapshot. It must not be copied into round 20.
   - The "ten OM10" versus nine labeled occurrences was taken from the verifier (`corpus/lessons/round-19-verifier-spotcheck.md:88`) and was not recounted.
4. **M4 (docstring "lead", JSON without marker) is reproduced.** The tool docstring at `tools/mado-tripwire.py:43-46` says "reported as a lead"; the finding dict at `:1597-1601` has no `evidence` key (`grep -c evidence` = 0 in the `1f7f995` copy). The lead fixture `.ufo/waves/round-19/tripwire/r19-helperfn/py-lead-cross-cell-literal.jsonl` (sha256 `53cd86c1…`) yields one finding with no evidence key at `1f7f995`. `e629f73` and `1f7f995` tool bytes are identical (`diff` empty).
5. **Round-20 check paths are planned, not present.** `.ufo/waves/round-20/` holds only `gen_w1.py`, `evidence/`, and `w1/`. The fix column therefore names the planned paths (`tw-precision.py`, `isolation-check.sh`, `tally-check.py`, from `.ufo/waves/round-20/w1/spec.json` items and `SCORECARD.md:1240`) and marks their red demonstrations pending.

## Limits

- The round-20 checks (`tw-precision.py`, `isolation-check.sh`, `tally-check.py`) were not run. Their red entries are unproven; only the manual red reproductions in findings 1 and 4 are observed.
- The `inns.sh` shape (M2) was not executed, as the host pause requires.
- First-line 6/13 and "ten vs nine OM10" were not re-derived.
- RerunC2:98 polarity was not checked at `01b8094`.
- Source citations are file:line pointers into the lane at `e629f73`; `corpus/lessons/round-19.md` line numbers were read at HEAD.

## Installs

none. Only `git show`, `git ls-tree`, `sha256sum`, `grep`, `python3` standard library (`json`, `subprocess`, `re`) and `python3 -I` on the copied tool were used.

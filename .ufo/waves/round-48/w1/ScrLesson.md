# ScrLesson — round-48 w1 seat report

Seat `ScrLesson` (scribe, leaf — no subagent dispatch). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only against
the lane; the only writes are this report and the seat directory. Lane HEAD when read
`5ff167423ee410251da0ef0c82f8e6fa25875665` ("round-48: claims, w1 spec + dispatch, census before"); base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585` ("round-47 verifier spot-check (integrator, hyaku): non-author admit/reject"), confirmed
an ancestor (`git merge-base --is-ancestor` rc 0). No host mutation, no compositor verb, no terminal launched, no
`xdg-terminal-exec` run (not even `--print-*`), no `xkbcli` run, no counter/gate/test executed. No tool installed or upgraded. No
scratch directory created (nothing to delete); every command was read-only and produced output well under 1 MB.

## Deliverable

`.ufo/waves/round-48/w1/ScrLesson/round-48.md` — 313 lines, the round-48 lesson skeleton in the shape of
`corpus/lessons/round-47.md` plus the three things this round's ticket names: `## Gate` carrying candidates/admitted/rejected,
census before → after, the renumber map, id-guard and quarantine results, the `considerthese` verdict and the D1 delta line;
`## Mistakes` with slots for `w1/ScrMistakes`; `## Spot-check (pending non-author)`.

Companion files, same directory:

- `verify.py` — read-only verifier: every locator and fragment the skeleton cites is re-derived with `grep -n` on the named
  file (never typed) and compared against the claimed range; also prints the skeleton's section map, its `<AFTER>` count, the
  measured base counts, the id-guard set comparison and the commit provenance.
- `receipts.txt` — the verifier's recorded output: 29 `CHECK` lines (34 `verdict=OK` including 5 `WORDS` lines) and 0
  `DIFFER`; `VERIFY: checks_failed=0`, exit 0.

Section map (computed by `verify.py`, `SECTIONS` line):

| line | section | state |
|---|---|---|
| 19 | `## Gate` | shape fixed; two planes (C1 cache edge, C2 XKB compile), held-ground decisions and two rejection classes written; admitted rows, GATE lines and the rejected list are `<AFTER>` (`w1/ScrRows`, `w1/ScoutXkbSpecs`, `w1/ScoutHeld`) |
| 74 | `### Census before → after` | **before pasted verbatim** (17 W04 + 1 W01 + `mado ok`, `exit=0`); after is `<AFTER>` |
| 107 | `### Registry changes` | base counts measured; row/knowledge/tools/quality deltas `<AFTER>` |
| 119 | `### Renumber map` | **none this round, with the reason measured** (top `S339`, C2 opens `S340`, staged band `S203`-`S349`) |
| 127 | `### Id guard and quarantine` | dispatch counts **re-derived** (276/147/84, intersection equal); ExecIdGuard's own receipt, the round-48 slice and the 13 inherited rows are marked |
| 143 | `### considerthese` | one-proposal rule stated; proposal number/verdict `<AFTER>` (`w1/ScrConsider`, `w1/SentPrivacy`) |
| 152 | `### The D1 delta line` | **fully drafted and grounded**: frozen docstring `:84-87` vs landed `:85-86`, closure `:126-131`, pin exit 1 vs tool exit 2, paid forward in the round-48 contract |
| 167 | `## Search log` | question, where-searched, stop and re-open triggers written; four counts `<AFTER>` |
| 194 | `## Mistakes` | `<AFTER>` from `w1/ScrMistakes`; mandatory-mined-mistake rule, the class vocabulary, five named candidates (D1-D4, M47-7/8 recurrence check) |
| 219 | `### Applications of existing criteria` | `<AFTER>` |
| 223 | `### Conflicts recorded for the judge` | `<AFTER>` |
| 228 | `## Round-47 closure items` | nine items (D1-D4, R3, R4b, M47-10, CritC1Explain, SentC1Sandbox F1-F4) with seat, landing and a drafted acceptance each |
| 264 | `## Spot-check (pending non-author)` | pending; the six-part shape the closure must fill |
| 285 | `## Frontier` | five frontier items; the README bullet **drafted** with provenance and `<AFTER>` scrub instruction |

`<AFTER>` markers: **48** (`text.count('<AFTER>')` in `verify.py`), each a value that cannot exist before the freeze or before a
w1 seat returns. No `<AFTER>` stands for something this seat could have measured.

## Gates / contracts this draft is shaped against

- The assignment's Gate enumeration (candidates, admitted, rejected, census before → after, renumber map, id-guard + quarantine,
  `considerthese`, the D1 delta line) — implemented as the `## Gate` sub-sections above rather than round-47's split
  (`### Census`, `## considerthese`, `## Assimilation`), because this round's ticket names them inside Gate.
- `.ufo/waves/round-48/claims.md`: C1 is a quality-trend move on the warm-cache path of `tools/mado-terminal.py`, judged by the
  real pinned script; C2 is the sourced expansion, rows `S340..`; the routed items are non-claim work with their own receipts.
- Fixture schema v2 (DRAFT in the ticket: `mtime`, `prime.args`, `after`, `cache`, `expect` always from the pinned script, 3
  runs) — named in the closure table's M47-10 row and in the D3 acceptance, not restated as a contract.
- `CORPUS.md` rule 2 (append-only) — every landing this draft plans is an append (D4 erratum, R4b errata, README bullet above
  the round-47 bullet, no row edited).
- `QUALITY.md` — tops at criterion 95 (measured), so any new criterion is 96+ and must fail on a named input.

## Registries before (measured, no value typed)

| surface | command | output |
|---|---|---|
| rows | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `276` |
| top id | `grep -oE '^\s*\|\s*S[0-9]{3,}' corpus/SOURCES.md \| tr -dc '0-9\n' \| sort -n \| tail -1` | `S339` |
| knowledge | `ls corpus/knowledge/*.md \| wc -l` | `64` |
| lessons | `ls corpus/lessons/*.md \| wc -l` | `70` |
| tools | `ls tools/ \| wc -l` | `15` |
| README index rows | `grep -cE '^\|[[:space:]]*`?knowledge' corpus/README.md` | `64` (round-47 row at `:75`) |
| QUALITY top | `grep -oE '^[0-9]{2,3}\.' corpus/QUALITY.md \| sort -n \| tail -1` | `95` |
| census before | `grep -c W04` / `grep -c W01` on `receipts/census-before.txt`; `wc -l`; `tail -1` | `17` / `1`; `20` lines; `exit=0` |
| id guard (dispatch artifacts) | set comparison over `assimilation/{reg-ids,staged-ids,collisions}` | reg 276 `S001`-`S339`; staged 147 `S203`-`S349`; collisions 84 `S203`-`S339`, `equal_to_file=True` |
| round-47 collisions | `wc -l < .ufo/waves/round-47/assimilation/collisions` | `70` |
| quarantine (round 47) | `wc -l`, `grep -c 'payload-absent'` | `13` lines, `6` payload-absent, 7 `no quote was checked` |
| pin identity | `sha256sum .ufo/waves/round-47/fetch/xdg-terminal-exec` | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |

## Locators the draft rests on (verified, `receipts.txt`)

- C1 contract delta: `tools/mado-terminal.py:82` (cache paragraph), `:85-86` (added `HOME unset, a FIFO named like a desktop
  file in a later application dir`, `symlink loops`); frozen `.ufo/waves/round-47/l1-draft/mado-terminal.py:81` and `:84-87`
  (the same sentence **without** those three; verified absent by `grep -nF`), the frozen code still raising
  `OutOfContract("HOME unset")` at `:407`; `registration.md:30-31` names the frozen docstring as the contract; closure
  `round-47-verifier-spotcheck.md:126-131`.
- Resolver pin: `:1179` read-before-lists, `:217` `read_cache()`, `:179` `gen_hash()`, `:1457` `save_cache "$1" &` (inside the
  `:1455-1458` span).
- C2 ground: `corpus/knowledge/hyprland-input-devices-r46.md:69`; `corpus/README.md:110` (warm-cache path), `:112` (XKB
  compile), `:75` (round-47 index row).
- Held rows: `corpus/SOURCES.md:267` (S318), `:268` (S319).
- Round-47 lesson: `:227` (proposal 2, refused), `:233-234` (quarantine).
- Round-46 closure: `:113` (R3), `:116` (R4).
- Spotcheck defects: D1 `:126`, D2 `:132`, D3 `:136`, D4 `:139`.
- Every quoted fragment is ≤ 25 words (7/3/4/14/2, `WORDS` lines).

The draft cites no `/tmp` or scratch path (`SCRATCH_REF` check: absent).

## Findings the L1 should know before the freeze

1. **The Gate enumeration is aggregated inside `## Gate`**, including id-guard/quarantine/`considerthese`/D1. If the L1 keeps
   round-47's separate `## Assimilation`/`## considerthese` sections, the prose transplants unchanged; no fact is duplicated.
2. **D1 is fully determinable now** and is drafted as a complete lesson line, not a slot: the frozen docstring lists the
   exclusions at `:84-87` and the landed file adds three at `:85-86`. `w1/ExecHomeUnset` still owes the measured pin/tool pairs
   and `w1/ScrD1Line` the per-item lines; the draft names both.
3. **The id-guard numbers are the dispatch artifacts, not the seat's receipt.** They were re-derived read-only and match the
   files exactly; the draft says so and points at `w1/ExecIdGuard` for the proven-guard receipt and the round-48 slice.
4. **The round-47 quarantine slice is a 13-line file**, six `payload-absent` and seven `no quote was checked` rows — the draft
   lists the ids rather than the round-47 lesson's summary wording.
5. **C1 adds no registry row in this draft** (the row-47 pin is the source of truth). If the L1 decides otherwise, the registry
   table's `<AFTER>` and the declined-row sentence both move.

## Out of scope (not done, by rule)

No product code, counter, fixture, registry, README, SKILL, QUALITY or registration edit; no `w2` instrument; no commit or
mutating git/jj; no pin fetched (all pins read from the lane). No claim was verified by this seat: the skeleton is structure and
measured base state, and every value a w1 seat owns is marked.

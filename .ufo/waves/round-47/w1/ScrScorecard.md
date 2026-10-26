# ScrScorecard — round 47 w1 (SCORECARD Round 47 section + LOG Round 47 skeleton)

Seat: `ScrScorecard`, wave `w1` (BUILD), lane `mado-shokunin`, base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`.
Draft: `.ufo/waves/round-47/w1/ScrScorecard/draft.md`. Quote receipt: `.ufo/waves/round-47/w1/ScrScorecard/quote-check.txt`.
No tracked file was edited; the L1 integrates.

## Behavior (what the draft delivers)

`draft.md` carries five paste-ready sections:

- **A — SCORECARD.md Round 47 section**: heading in the lane's established form, the registration/freeze paragraph with
  the inverted round order (instruments freeze after the build wave, then `w2` attacks them), the two claim rows
  (C1 `tools/mado-terminal.py`, C2 `corpus/knowledge/xdg-terminal-selection-r47.md`) with before/after cells, counting
  commands and self-verdicts, the `Separable` line, one **capabilities** row (the resolver re-implementation: list order,
  desktop-ID resolution across the data dirs, entry validation, actions, exec-arg composition, print modes, cold cache,
  `explain --observed` verdicts, the no-process/no-socket tripwire, and the pinned script as oracle), the
  sources/saturation/closure paragraph (rows S326.., knowledge entries 63 → 64, routed round-46 R1-R4), the re-derived
  axis line, and `### Planned (round 48; intent only)` with five items (warm cache, `uwsm-app`, the selected terminal's own
  config plane, routed items left open, `w2` findings).
- **B — LOG.md Round 47 entry skeleton**: eight bullets in the round-45/46 shape (protocol load + census, `w1` build,
  the post-`w1` freeze, `w2`, data, routed closure, freshness, not-run).
- **C — placeholder ledger**: which token, what it stands for, who fills it, which receipt it must point at.
- **D — grounding table**: every non-placeholder literal in A/B with the command that produced it and its output.
- **E — conflicts** this draft deliberately does not decide (tripwire token, `Separable` seat name, warm-cache scope,
  the `xdg-terminal-exec` name in `tools/mado-tripwire.py`).

Only two tokens are used, as instructed: `<FREEZE>` = fixed by the L1 in `registration.md` after `w1`; `<AFTER>` = produced
by a later run (base receipts, data commit, counter stdout, census, gate codes, closures, axis values).

## Gates (what was actually checked, and what was not)

Checked read-only, cwd `/home/vgpnk/Projects/shokunin/mado-shokunin` (outputs in `draft.md` §D):

- `git cat-file -t 60edb66e…` → `commit`; `git log --oneline -2` → `60edb66e round-46 verifier spot-check …` over
  `c24adef2 round-47: claims declared, w1 build spec and dispatch (41 seats, policy v1), census before`.
- `sha256sum /usr/bin/xdg-terminal-exec` → `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, the
  claim's pin byte-for-byte.
- `grep -n 'SUPER, RETURN' ~/.config/hypr/bindings.conf` → locator `2`; the full hotkey line quoted in the draft.
- `.ufo/waves/round-47/w1-dispatch.json`: `counts.spawn=41`, 41 `registry.members`; prefix census → executor 16,
  scribe 10, scout 5, critic 4, connector 2, sentinel 2, reviewer 1, revenger 1.
- `.ufo/waves/round-47/receipts/census-before.txt`: `exit=0`; 15 finding rows = 14 W04 + 1 W01
  (`awk -F'\t' '$1=="mado"{print $2}' … | sort | uniq -c`).
- `grep -cE '^\| S[0-9]+ ' corpus/SOURCES.md` → `262`; top row `S325` (so S326 is next); rows S056-S060 (5) are the
  held round-17 terminal rows the draft says it will not re-claim.
- `ls corpus/knowledge/*.md | wc -l` → `63`; `corpus/QUALITY.md` last item is `90.` (starts `:454`).
- `test -e tools/mado-terminal.py` and `test -e corpus/knowledge/xdg-terminal-selection-r47.md` → `rc=1` both
  (the two base "absent" cells are structural, not predicted).
- `grep -nF` of every quote in this report → `quote-check.txt`, each count `1`.

Not checked, on purpose: no counter was run (none is frozen), no fixture was built, the pinned script was never executed
(no `--print-*` run was needed for this seat), no socket, no process spawned by the lane tools, no `hyprctl`, no package
transaction, nothing installed.

## Touched surfaces

- New: `.ufo/waves/round-47/w1/ScrScorecard/draft.md`, `.ufo/waves/round-47/w1/ScrScorecard/quote-check.txt`, this report.
- Scratch `/fast/scratch/hyaku/mado-r47/ScrScorecard/` created and removed (`rm -rf`); nothing under `/tmp`.
- Read-only: `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
  `corpus/lessons/round-46-verifier-spotcheck.md`, `.ufo/waves/round-47/{claims.md,w1-dispatch.json,w1-spec.json}`,
  `.ufo/waves/round-47/receipts/census-before.txt`, `.ufo/waves/round-46/w1-results.json`, `tools/` listing,
  `~/.config/hypr/bindings.conf`, `/usr/bin/xdg-terminal-exec` (hash only).

## Out of scope (not done, by assignment)

No edit to `SCORECARD.md`, `LOG.md`, `corpus/`, `tools/`, counters, registrations or any tracked file; no freeze, no data
commit, no `w2` dispatch, no counter authoring, no live host run of `mado-terminal.py` (it does not exist at base).

## Findings

1. **F1 — the LOG's `spec` literal is a commit, not the spec file's hash.** Round 46's LOG says ``spec `e0be61e4` ``;
   `e0be61e4f6e3…` is `round-46: controls at freeze …, w1 spec and dispatch (66 seats, policy v2)`, while
   `sha256sum .ufo/waves/round-46/w1-spec.json` is `a33a608c…`. The round-47 analogue is therefore `c24adef2`
   (commit) and **not** `207982d0…` (`sha256sum .ufo/waves/round-47/w1-spec.json`). Pasting the file hash would be a
   provenance defect of the M46-5 class.
2. **F2 — the `w2` seat count has a floor the skeleton must not undercut.** Policy v1 sets `"waveMinLanes": 32`
   (`.ufo/waves/round-47/w1-dispatch.json:8`), and the round-45 precedent records a round-total floor:
   "round total 41 seats, below the 64 floor; reported as" (`LOG.md:2513`, 10 words). 41 build seats leave `w2` needing
   ≥ 23 by the round total and ≥ 32 by the per-wave policy; the binding value is 32, and a `w2` below it needs a
   recorded conformance defect exactly as round 45 recorded its own.
3. **F3 — `tripwire=` is a new token in a row family that dropped it.** Rounds 45 and 46 reported `readonly=ok` only;
   round 47's contract makes the execve/socket tripwire part of the judged surface. The draft keeps the token and leaves
   its value to the freeze (`draft.md` §E1) so the same check is not counted twice under `readonly` and `tripwire`.
4. **F4 — a name collision the C1 wording must survive.** `tools/mado-tripwire.py:272` lists
   `"pidof", "xdg-terminal-exec", "wpctl", "brightnessctl",` — the resolver appears as a watched *process*, not as a
   selection model. C1's "surface moved" sentence stays true, but a `w2` reviewer reading that line could read it as a
   prior capability; the draft says which tool owns the name (`draft.md` §E4).
5. **F5 — the census bullet needs composition, not only the exit code.** Base census has 15 finding rows (14 W04
   duplicate-URL rows, 1 W01) at `exit=0`; the W04 rows are S030, S042, S045, S097, S119, S120, S121, S303, S307, S317,
   S318, S320, S321, S324 — all already-registered rows re-flagged, so the sources paragraph's "repeat held URLs" count
   (`<AFTER>`) covers them and must not be read as new coverage.
6. **F6 — QUALITY item 90 binds the R4 closure line.** The file ends at item 90 / `:454`, whose rule is that a routed
   defect keeps one identity and an age and a third deferral is mined as a `landing` mistake ("42 rows, 15 open, oldest 8
   rounds at R38-3", `corpus/QUALITY.md:457`). If S290-S297 defers again, the `<AFTER>` in the closure line must name the
   mine (M47), not just "open".
7. **F7 — R3 has to be reported twice.** Round 46's gate receipt is `findings=115` exit 1 with 18 hits in round-46 seat
   files; installing the synthetic marker can only be evidence when the draft's `<AFTER>` cites both the clean run and a
   planted case that still fails — a single green number would prove the gate can pass, not that it discriminates.
8. **F8 — `Separable` needs a producer, not a hope.** The `w2`-era cross-claim line names `w1/ConnClaims.md`; if that
   seat does not emit the tool-only / data-only tree split, the line must be dropped rather than left standing
   (`draft.md` §E2). Round 45 and 46 both had a dedicated seat for it.

## Artifact paths

- `.ufo/waves/round-47/w1/ScrScorecard/draft.md` — the deliverable (§A SCORECARD section, §B LOG skeleton, §C placeholder
  ledger, §D grounding, §E conflicts).
- `.ufo/waves/round-47/w1/ScrScorecard/quote-check.txt` — `grep -c`/`grep -n` for the four quoted spans (each count 1).
- `.ufo/waves/round-47/w1/ScrScorecard.md` — this report.
- Tool installs: none. Package transactions: none.

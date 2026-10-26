# Seat RerunC2Data — C2 counting commands re-run at the data commit

**Verdict: AGREE. No disagreement.** Both C2 receipts reproduce byte-for-byte at
`1959770657f1f8665097c1aed4be6c1cbb07139f`, and an independent re-derivation of the ten Gate bindings
(receipt sha256, single word-bounded occurrence, 1-based start line, entry line carries quote+locator)
agrees with the counter on every id.

Attacked: `receipts/c2-after-data.txt` (PRED-C2-r43-v2, `admitted=1/1 verdict=TARGET_MET`, exit 0) and
`receipts/c2-v1-after-data.txt` (PRED-C2-r43, same), plus their two base controls. Supports: the C2
target line of `registration-v2.md` and the C2 target line of `registration.md`.

Evidence: `.ufo/waves/round-43/w2/RerunC2Data/receipt.txt` (271 lines, runs A–O, every command and its full
output with exit codes). Scripts in the same directory: `indep_gate_check.py` (my own verifier, imports no
counter code), `teeth.sh` (mutant fixture for that verifier).

## Method

Isolated clone, not the lane working tree:

```
S=/fast/scratch/hyaku/mado-r43/RerunC2Data ; mkdir -p "$S"
D=$(mktemp -d -p "$S") ; git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
git -C "$D" rev-parse --show-toplevel   # = $D (checked before every run)
TMPDIR=$S python3 -I <lane>/quality/counters/<counter> --repo "$D" --rev <rev>
```

Counters were run from their frozen lane paths (read-only) with their recorded sha256:
`c2-r43-gkeep-entry-v2.py` `9a83407062d165661d211a714ce06b381391c7c4574c91c71eb54689dde1d028`,
`c2-r43-gkeep-entry.py` `4b5751fe7010400a5a7e4132dafc3f297132d443f2389a61f0b89032c669016c`.
Python 3.14.8. The scratch tree (two clones, a fixture repo) was deleted at the end
(`rm -rf /fast/scratch/hyaku/mado-r43/RerunC2Data`); every citable number below is in the seat receipt,
which repeats the full per-clause text so it can be read without re-cloning.

## A. Counter re-runs (receipt runs A–E, N)

| # | counter | rev | per-clause line | final line | exit | vs committed receipt |
|---|---|---|---|---|---|---|
| A | v2 | `1959770…` data | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1` | `admitted=1/1 verdict=TARGET_MET` | 0 | **byte-identical** to `receipts/c2-after-data.txt` (33 lines, `diff` empty) |
| B | v1 | `1959770…` data | `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1` | `admitted=1/1 verdict=TARGET_MET` | 0 | **byte-identical** to `receipts/c2-v1-after-data.txt` |
| C | v1 | `a35cfdf…` base | `a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 admitted=0` | `admitted=0/1 verdict=TARGET_MISSED` | 1 | equals `receipts/c2-before-base.txt` |
| D | v2 | `a35cfdf…` base | same all-zero | `admitted=0/1 verdict=TARGET_MISSED` | 1 | equals `receipts/c2-v2-before-base.txt` |
| E | v2 | `1959770…` data, **second** clone | same | `TARGET_MET` | 0 | replay determinism across clones |
| N | v2 | `1959770…` data, **lane repo** (`--repo .`) | same | `TARGET_MET` | 0 | the registration's own command form; lane `git status` on the scored paths stayed empty |

Tip check (run I): at `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa` the v2 counter is `TARGET_MET` exit 0, and
`git diff --stat 1959770… 2a3707c…` over `corpus/knowledge corpus/lessons corpus/SOURCES.md corpus/README.md
.ufo/waves/round-43/fetch` is **empty** — every clause input is byte-identical at the data commit and at the
tip, so the two runs score the same bytes.

## B. Independent recomputation of the ten cited ids (run F2, `indep_gate_check.py`)

Own implementation of whitespace collapsing with a per-character line map, own word-boundary predicate
(`isalnum() or "_"` on both ends), own sha256 — no counter function imported, copied or exec'd. Result:
`INDEP VERDICT: AGREE (disagreements=0)`, exit 0.

| id | receipt | sha256 = GATE sha256 | mode | occurrences (word-bounded) | start line | entry raw line | entry carries quote + locator |
|---|---|---|---|---|---|---|---|
| S155 | Hyprland-WindowRuleApplicator.cpp | yes `fec33f9a…` | 100644 | 1 | 426 | 40 | yes (`…:426`) |
| S158 | Hyprland-HyprCtl.cpp | yes `798b7c6c…` | 100644 | 1 | 428 | 54 | yes (`…:428`) |
| S290 | Hyprland-RegexMatchEngine.cpp | yes `8ca65533…` | 100644 | 1 | 16 | 34 | yes (`…:16`) |
| S291 | Hyprland-DefaultFloatingAlgorithm.cpp | yes `f05f2561…` | 100644 | 1 | 56 | 42 | yes (`…:56`) |
| S292 | Hyprland-Target.cpp | yes `49323833…` | 100644 | 1 | 10 | 44 | yes (`…:10`) |
| S293 | Hyprland-WindowTarget.cpp | yes `8bcaf370…` | 100644 | 1 | 70 | 46 | yes (`…:70`) |
| S294 | Hyprland-GeometricMovableAnimated.cpp | yes `649f1a8d…` | 100644 | 1 | 19 | 52 | yes (`…:19`) |
| S295 | host-gkeep.conf | yes `3726e488…` | 100644 | 1 | 4 | 32 | yes (`…:4`) |
| S296 | host-clients-r43.json | yes `21db902e…` | 100644 | 1 | 50 | 66 | yes (`…:50`) |
| S297 | gkeep-ui-excerpt.py | yes `3695b788…` | 100644 | 1 | 33 | 60 | yes (`…:33`) |

Every computed line equals the counter's `clause=g … locator_line=` value (run A: 4, 16, 426, 56, 10, 70, 19,
428, 33, 50). Also checked: each of the ten `GATE` lines sits inside `## Gate` (10/10), each id has exactly
one `GATE` line, and no quote is word-bounded in any *other* cited receipt (no `SHARED-QUOTE` line printed).

## C. Teeth of my own instrument (run H, H2 — `teeth.sh`)

A private fixture repo under `/fast/scratch/hyaku/mado-r43/RerunC2Data` (`git init` in a `mktemp -d`, the
archive of the data commit's own blobs, `rev-parse --show-toplevel` verified before the first commit) carried
one defect per commit:

| case | mutation | expectation | observed |
|---|---|---|---|
| T0 | none (data-commit copy) | AGREE | `INDEP VERDICT: AGREE (disagreements=0)` rc 0 |
| T1 | one hex digit of S292's declared sha256 flipped | DISAGREE (sha256) | `DISAGREE sha256 S292: declared 59323833…` rc 1 |
| T2 | S155's quote corrupted (`expr;`→`expr21;`) | DISAGREE (occurrences) | `occ=0` + `DISAGREE word-bounded occurrences=0` rc 1 |
| T3 | S292 locator `:10`→`:11` in the entry | DISAGREE (locator) | `miss_locator=[44]` rc 1 |
| T4 | S295 entry quote `420`→`421` | DISAGREE (entry quote) | `miss_quote=[32]` rc 1 |
| T5 | S290's `GATE` line duplicated | DISAGREE (GATE count) | `DISAGREE S290 has 2 GATE lines` rc 1 |
| T6 | S294's entry carrier line deleted | DISAGREE (no carrier) | `DISAGREE no unfenced entry line names S294` rc 1 |

(The first T1 attempt was a sed no-op — `git commit` reported "nothing to commit" — so it tested nothing; the
retry in run H2 rewrote `sha256=49323833…`→`sha256=59323833…`, shows the `git diff` and fails as expected.)

## D. Is the verdict an artefact of local state? (runs J, K)

- **Working tree:** with the entry **deleted** and `corpus/lessons/round-43.md`, `corpus/SOURCES.md`,
  `corpus/README.md` **emptied** in the clone's working tree (`git status` shows `D`/`M`), the v2 counter still
  scores `admitted=1/1 verdict=TARGET_MET` at `1959770…`, and my verifier still says AGREE. The counter is
  revision-addressed, not working-tree-read.
- **Ambient env:** `GIT_DIR=/nonexistent GIT_WORK_TREE=/tmp GIT_INDEX_FILE=/tmp/nope.idx` still yields
  `TARGET_MET` exit 0 — the `GIT_*` scrubbing the docstring claims holds.

## E. Supplementary checks (runs L, O)

- **Comment stripping** (v2 `d+` "outside comments"): every one of the ten quotes occurs exactly once in the
  raw collapsed receipt and exactly once after comment stripping (`//`, `/* */` for the `.cpp`s, `#` for
  `.conf`/`.py`; JSON untouched) — `COMMENT-STRIP VERDICT: OK (quotes lost=0)`.
- **Id sets:** the entry's `^source:` ids and the lesson's `GATE` ids are the same ten, no duplicates,
  `grep -c '^source: S0'` = **0** (so the v2 residual "a held id's receipt is not pinned" is not exercised:
  both held ids S155/S158 are bound to pinned receipts).
- **clause f input** (`corpus/README.md`) is unchanged between the data commit and the tip (run M, empty diff).

## Disagreements

None.

## Remarks (not disagreements; recorded so the closure need not re-derive them)

1. **The denominator is 1 by construction.** `ENTRIES` holds a single path (`c2-r43-gkeep-entry-v2.py:119`),
   so `admitted=1/1` is not a coverage ratio — the substantive content of both receipts is the nine per-clause
   flags, all 1. Attacks the *presentation* of `receipts/c2-after-data.txt`, not its truth.
2. **A conditional in clause g is covered elsewhere.** `all_body_lines_bound` skips the locator comparison when
   `at` is falsy (`if at and ("%s:%d" % (bn, at)) not in l`), which alone could pass a quote with no locator;
   clause d independently requires `quote_at(...) is not None` and `len(occurrences(...)) == 1` (counter
   `:501-503`), so a quote that vanishes cannot pass through that gap. Code reading, not a hole; my verifier
   does not reproduce that skip (it treats `occ=0` as a disagreement, T2).
3. **Scope of my normalizer:** for these ten non-HTML receipts my collapse matches the counter's; for HTML
   receipts the counter additionally strips tags/scripts, which `indep_gate_check.py` does not implement and
   none of the ten cited ids exercises.
4. The clone is gone per the SCRATCH directive; the receipt is self-contained (full text of every run), and
   the reproduction recipe is in "Method" above.

## Files written (seat dir only)

- `.ufo/waves/round-43/w2/RerunC2Data.md` (this report)
- `.ufo/waves/round-43/w2/RerunC2Data/receipt.txt` (runs A–O, 271 lines)
- `.ufo/waves/round-43/w2/RerunC2Data/indep_gate_check.py` (independent verifier)
- `.ufo/waves/round-43/w2/RerunC2Data/teeth.sh` (mutant fixture for that verifier)

No tracked lane file was edited; `git -C <lane> status --porcelain` over `quality/counters`, `corpus/*`,
`.ufo/waves/round-43/fetch`, `.ufo/waves/round-43/receipts` and both registrations is empty. No tool was
installed. No host/compositor command was run.

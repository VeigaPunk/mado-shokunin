# R87Critic — adversarial review of the round-87 declaration (C1, C2, frontier step)

Seat: R87Critic (critic, leaf). Declaration read in full: `.ufo/waves/round-87/claims-declaration-r87.md` (lines cited below are that file's lines).
Scope: falsify C1 and C2 and check the six items in the seat spec. No counter, tool or lane gate was run. No file written except this report. No scratch created. No install.

## Read-time state (artifacts the declaration names were absent when read)

- `.ufo/waves/round-87/controls/` is empty: `mako-cases-r87.json` and `r86-figures-r87.json` do not exist yet.
- `quality/counters/*r87*` does not exist; `tools/mado-mako.py` does not exist.
- `corpus/SOURCES.md` has no S493 row (the census count is 427 rows, unchanged from r86).
- Checks that need those artifacts are marked NOT EVALUABLE below. Re-run them once the wave lands.

Commands run (all read-only): `sha256sum` and `zcat | sha256sum` on `/usr/share/man/man5/mako.5.gz`; `pacman -Q mako` (query only); `mako --version` (exits 1, prints the unrecognized-option error, nothing changed); `grep`/`sed`/`cat -n` on the files cited; a read-only `json.load` of `.ufo/waves/round-86/controls/c2-cases-r86.json`; `git rev-parse --verify` on the base commit.

## Verdicts

| # | Item | Verdict | Short reason |
|---|---|---|---|
| C1 | coverage: new surface, mako effective settings | **WEAKENED** | "Not held" is false as written. The include chain and criteria behaviour are already observed in `waybar-walker-plane.md` §4. The resolver and the manual grammar are new. |
| C1-pin | frontier pin `sha256` of `mako.5.gz` | **FALSIFIED (as written)** | The named `.gz` hashes to `17ffc88c…`. The declared `f717848f…` is the digest of the decompressed text. |
| C1-read | read-scope wording | **WEAKENED** | "Reads only the regular files its caller names" conflicts with reading `include=` targets. |
| C1-trivial | can a trivial tool reach 10? | NOT EVALUABLE | Case file absent. Control gate is "strictly below N", which one miss satisfies. |
| C1-pred | predicate identical in declaration, docstring, report | NOT EVALUABLE | Counter and report absent. The declaration states the sentence once (line 49). |
| C2 | calibration: F1 real mismatch, F2 reproduces | **F1 CONFIRMED; F2 reproduces as text**; before 5.0 is honest | Model result is 0/1; held counter (code reading) gives 1/1. |
| C2-after | after-score reachable by text-only correction | **WEAKENED** | Disjunct at lines 72–74 accepts a correction block without requiring the counter to re-derive its value. |
| C2-root | root cause removed by C2? | **WEAKENED** | The selftest that pins the false model (`c2-r86-clause-observations.py:736-737`) is not in the predicate. |
| C2-rev | F2 revision | **WEAKENED** | Three different `rev=` values for the r86 flood receipts. |
| 3 | stagnation nudge | **HOLDS** | Last capability row r82; r83–r86 admitted none; gap 4 > N=3. |
| 4 | fresh-start headers r83–r85 | **HOLDS** (r83 wording loose) | r84 and r85 headers state "rejected-honest-stop"; r83 states it in the body. |
| 5 | manual pin | **FALSIFIED (label)**; version holds | See C1-pin. `pacman -Q mako` = `1.11.0-1`. |
| 6a | proposal 7 text | **HOLDS** | Verbatim at `considerthese/2026-11-04.md:52`. |
| 6b | r86 lesson did not implement it | **HOLDS** | No "relayed"/"re-measured" rule in `corpus/lessons/round-86*.md`. |
| 6c | criterion 146 is new | **WEAKENED** | The same rule is already criterion 76 and criterion 131. |

## Evidence by claim

### C1 — coverage (new surface?)

1. **"Not held: no note owns it" is false.** Declaration lines 26–27 say `waybar-walker-plane.md` "covers only DND through `makoctl mode`". The note's §4 (`corpus/knowledge/waybar-walker-plane.md:201`) already records:
   - the 5-line config's `include=` of `core.ini` and its three colour overrides (`:203–205`);
   - stock `core.ini` criteria behaviour: Spotify invisible, DND invisible except `notify-send`, critical urgency sticky on overlay (`:211–215`);
   - click actions wired by `[summary~=…]` sections (`:216–218`).
   The surface is therefore held at the observation level. What is new is the effective-value resolver and the manual-grounded grammar. `corpus/SOURCES.md` has no mako(5) manual row (grep of `corpus/` for mako manual finds none). The "frontier" claim needs to say "re-scoring plus resolver" rather than "new surface".

2. **Manual grammar is real** (`zcat /usr/share/man/man5/mako.5.gz`): `include=` at lines 45–47; criteria section at 423–440 with "last occurrence … wins" at 435–437; `[app-name=…]` and `[actionable]` forms at 128 and 514–516; `[mode=…]` at 617–628. The declaration's list of criteria fields matches.

3. **Trivial tool reach** — NOT EVALUABLE. Structural note: `TARGET_MET` needs `tool_correct == N` and each control `< N`. A control needs only one case it gets wrong. The declaration does not require any case to exercise include-override precedence or criteria precedence, so the controls' failure may be incidental to case composition. Require at least one include-override case and one criteria-over-global case, and state which control fails each.

4. **Do-nothing controls** — definitions are as stated (`declaration:40–43`); NOT EVALUABLE against cases until the case file exists.

### C1 — frontier pin (item 5)

- `sha256sum /usr/share/man/man5/mako.5.gz` → `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670`.
- `zcat /usr/share/man/man5/mako.5.gz | sha256sum` → `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba`, which is the declared value (`declaration:28`).
- The file is root-owned, mtime 2026-03-26, and `pacman -Q mako` is `mako 1.11.0-1`.
- Fix: declare both digests, or name the decompressed stream explicitly. The S493 row must carry the same digest.

### C1 — read scope

`declaration:31–32` says the tool "reads only the regular files its caller names (`--config`, `--home` for `~`)". `include=` targets are named inside the config, not by the caller, and the manual says the include path may start with `~/`. PROVINCE.md:126 already documents the same "follows `source =` lines" class for `mado-watchplan.py`. The declaration should state that include targets are read too.

### C2 — calibration

1. **F1 mismatch is real (code reading; not executed).**
   - The model `held_case_correct` in `quality/counters/c2-r86-clause-observations.py:574–593` uses plain `re.search` for regex rows, ignoring `anchor`.
   - The held counter `quality/counters/c2-r85-status-classes.py` routes `anchor == "line"` through `line_anchored()` (`:359–366`, `:380–381`); `case_correct` at `:509–513`.
   - Witness `border-size-int` in `.ufo/waves/round-86/controls/c2-cases-r86.json`: value `[0-9]+`, anchor `line`, samples `"1"`, `"2"` (rc 0), negatives `"0 extra"` (rc 0), `"-1"` (rc 0), `"0"` (rc 127). Under line anchoring the held counter accepts both samples and refuses all three negatives, so 1/1. The model's 0/1 comes from accepting `"0 extra"` as a substring.
   - Stated 0/1 is at `corpus/knowledge/refusal-records-clause-observations-r86.md:112`.
   - Before score 5.0 therefore follows from F1 unreconciled plus F2 reproducing as text. The L1 must re-run F1 to confirm.

2. **F2 reproduces as text, with three revisions.**
   - `.ufo/waves/round-86/receipts/final-c1-r86.txt:128–129`: `flooding=48/75 held_rule_flooding=75/75`, `rev=3afdb713…`.
   - `.ufo/waves/round-86/receipts/c1-r86.txt:129`: same numbers, `rev=f72bba01…`.
   - `.ufo/waves/round-86/receipts/control-c1-r86.txt:79`: same numbers, `verdict=MUTANTS_SKIPPED`, `rev=237ecf4e…`.
   - The declaration (line 65) names 3afdb713 as the measured revision and line 72 says "reproduces at REV". Those are different revisions. The figure's revision must be named once and the counter must run there.

3. **After-score by text-only correction — WEAKENED.** Lines 72–74: "TARGET_MET iff n = 2 and every figure is reconciled — it reproduces at REV, or an append-only correction block (`Correction (round 87)` heading in the same file, naming the figure id and its re-derived value) exists." The disjunct does not require the counter to re-derive the value and compare it. A block that names `F1` and `1/1` satisfies it whether or not `1/1` is true. It also does not say which file holds the block: "the same file" is ambiguous between the r86 entry, the figure JSON, and SCORECARD §Round86. The r86 lesson's R1 (`corpus/lessons/round-86-verifier-spotcheck.md` §6.1) asks for a correction in both `SCORECARD.md` §Round86 and `refusal-records-clause-observations-r86.md` §3, and the declaration names neither.

4. **Root cause not in the predicate — WEAKENED.** `c2-r86-clause-observations.py:736–737` asserts `not held_case_correct(anchor_case, 0, "0")`: the selftest pins the wrong model value. The declaration's M87-1 says "fix = C2 + the selftest-pinning control" (line 85), but no predicate line requires removing that assertion or pinning the model against the held counter. A figure correction leaves the false model and its pin in place.

### Stagnation nudge (item 3) — HOLDS

- R82 admits capability rows: `SCORECARD.md:4783` "### Capability demonstrated" (R82 block, from line 4748).
- R83 `:4887`: "no capability row is admitted from the missed C1 predicate" (`:4896`).
- R84 `:4912`, "No capability row is admitted from failed frozen C2" (`:4964`).
- R85 `:4967`, "No capability row is admitted from this rejected frozen C2" (`:4992`).
- R86 `:5019`, "No capability row is admitted" (`:5045`).
- Gap = 4 rounds (83–86) > N=3. The nudge applies.

### Fresh-start (item 4) — HOLDS, with a wording note

- `corpus/lessons/round-84-verifier-spotcheck.md:7` and `round-85-verifier-spotcheck.md:7`: "Status ok; admitted false; rejected-honest-stop."
- `round-83-verifier-spotcheck.md`: the header (lines 1–12) gives only conformance and "Status `ok`". The rejection is in the body: `:60` "the honest stop is real", and `:144` "Round verdict: honest stop, `ok`/not admitted". The declaration's "headers … state rejection" is true of r84 and r85 only.

### Proposal 7 and criterion 146 (item 6)

- 6a HOLDS: `considerthese/2026-11-04.md:52` reads "**Mark each figure as relayed or re-measured.** …".
- 6b HOLDS: the r86 lesson does not carry the rule. `corpus/lessons/round-86.md:50` cites QUALITY 145 as its only new criterion.
- 6c WEAKENED: the rule already exists.
  - `corpus/QUALITY.md:399` is criterion 76: a number taken on trust is written `relayed:` when mining considerthese.
  - `corpus/QUALITY.md:934–939` is criterion 131: every quoted number names "re-executed" or "evidence-verified", sourced to `considerthese/2026-10-28.md:56` (proposal 5, "Separate 'relayed' from 're-measured' in every number").
  - A criterion 146 with the same content duplicates 131. The "expansion" credit for a new criterion would be overstated. Either drop it, or extend 131 with the proposal-7 wording.

## Recommended corrections (smallest safe)

1. C1: replace "Not held" with a pointer to `waybar-walker-plane.md:201–218` and restate the claim as resolver-plus-grammar. Show both digests for the pin, and name the decompressed-stream digest explicitly. State that include targets are read.
2. C1 predicate: require at least one include-override case and one criteria-precedence case, and name the control each one kills.
3. C2: the counter must re-derive F1 and F2 at one named revision and compare any correction's value string to that re-derivation. Name the single file that carries the correction, and include SCORECARD §Round86 and the r86 knowledge file if R1 is to close.
4. C2: add to the declared deliverables the removal or replacement of the assertion at `c2-r86-clause-observations.py:736–737`, and pin the held model against the held counter.
5. Q146: drop it, or fold proposal 7 into criterion 131.

## Re-run list for the L1 (after the wave lands)

- F1 re-derivation at the content revision (the held counter's `case_correct` on `border-size-int`).
- F2 re-run at the revision the counter names (`final-c1-r86.txt` says 3afdb713; `c1-r86.txt` says f72bba01).
- C1: confirm the controls fail on at least one case each, then confirm the case file and counter predicate sentence match the declaration (line 49).
- Pin: `sha256sum` and `zcat | sha256sum` of the manual, to confirm the label fix.

No installs. No scratch created. No lane file written.

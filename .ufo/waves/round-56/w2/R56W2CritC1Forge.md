# R56W2CritC1Forge — forgery attack on PRED-C1-r56-v2 at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

Seat: R56W2CritC1Forge (leaf, no subagents). Lane read-only; no tracked file, index, ref or object of the lane was written.
Deliverables: `.ufo/waves/round-56/w2/R56W2CritC1Forge/` (`results.json`, `receipts/<variant>.txt` for 22 runs,
`variants/<variant>/` with the entry, registry, README bytes of each scratch commit).

## Bottom line

- **TARGET_MET is not evidence of a sourced entry.** The real counter and the real harness accept, at 33/33 content and
  12/12 controls, an entry in which every one of the 33 propositions asserts the reverse of what its pinned line says
  (B2). They also accept 33 hand-written template sentences (J1b), 33 token-stuffed sentences (T1), 33 neighbour-carrying
  sentences (T2b), ten hand-written false claims (T5), a false host value (B3), a false registry teaches cell (C1b), and
  the wave-1 cheap entry once its anchors are inside the file (T6).
- The counter does what the registration says and nothing about meaning: it checks the frozen quote is on the pinned line,
  the registry row for each source id, the anchor range, the provenance window, and five lexical constraints on the
  proposition (length, uniqueness, one shared identifier with the quote, numbers from an allowed set, no full-quote echo).
  A negation of an honest sentence satisfies all five by construction.
- Measured: **a lexical rewrite can falsify 33 of the 33 honest propositions and keep `content=33/33`** (B2; the counter
  prints `verdict=TARGET_MET missed=none`). "Falsified" is relative to the honest reading of each pinned line (mine; not
  re-verified line by line beyond the quotes the counter byte-checks).
- Two extra defects in the bounds, both small and both in the counter's own text: the anchor bound admits one line past the
  real end of `ConfigWatcher.cpp` (T4b), and the provenance check admits a stub source row that no row cites (P1c).

## Setup (what was run, read-only where the lane is concerned)

- Pin: `git -C <lane> archive 28fc86ac… | tar -x` into `/fast/scratch/hyaku/mado-r56/R56W2CritC1Forge/pin/`. This is the
  counter, harness, C3 counter, tables and the 13 pinned files at the frozen revision (sha256 of the tables checked by the
  counter itself).
- Scratch repo `W` (`git init`; `rev-parse --show-toplevel` asserted equal to `W` before the first commit). Its object store
  has an `alternates` entry pointing read-only at the lane's `.git/objects` (the `clone --shared` pattern) so that C3 can see
  its frozen base `13f0acbe…`. One commit per variant, identity `ctl <ctl@ctl>`. Each variant starts from the base bytes of
  the three files it touches (`corpus/knowledge/hyprland-config-autoreload-r56.md`, `corpus/SOURCES.md`,
  `corpus/README.md`) and applies one edit set.
- Per variant, three real programs, each run from `/fast/scratch/…` with `python3 -I`:
  - `python3 -I <pin>/quality/counters/c1-r56-autoreload-entry.py --repo <W> --rev <sha> --work <scratch>/work/<v>`
  - `python3 -I <pin>/quality/counters/c3-r56-used-by.py --repo <W> --rev <sha> --work <scratch>/work3/<v>`
  - `python3 -I <pin>/quality/check-r56-controls.py --claim c1 --repo <W> --rev <sha> --work <scratch>/hwork/<v>`
- Baseline on the lane itself (read-only, `--work` in scratch), to confirm the scratch pin behaves like the lane:
  - counter: `MADO_AUTORELOAD_ENTRY: rev=28fc86ac… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, rc=0
  - harness: `good: ok` / `controls=12/12 verdict=OK`, rc=0 (all 12 controls caught as registered)
  - the scratch base commit (`base-honest`) gives the same counter line and `MADO_USED_BY … missing=0 … TARGET_MET`, harness 12/12.
- Tools: none installed or upgraded (python3 and git only). No pacman, no network, no host reads, no `hyprctl` calls.

## Results (all 22 runs; full output in `receipts/`)

Counter columns: verdict, `content=` leg, `missed=` (trimmed). Harness: `good` leg and `controls`. C3: the sibling counter on the same commit.

| variant (attack) | counter | content | harness good / controls | C3 | counter accepts forgery? | what a human reviewer would reject |
|---|---|---|---|---|---|---|
| base-honest (no edit) | TARGET_MET | 33/33 | ok 12/12 | MET | n/a | (baseline) |
| J1a frozen quote as proposition | TARGET_MISSED | 4/33 | bad 12/12 | MET | no | all rows echo the quote (`echo:*`), row:K07,K08,... |
| J1b template proposition (harness selftest wording: "Entry row K01 cites a pinned source line that holds the token misc verbatim in its quote") | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | 33 copies of one sentence with an id and an identifier swapped in; says nothing about the line |
| J1c placeholder text (the harness's own control-2 text) | TARGET_MISSED | 1/33 | bad 11/12 | MET | no | tok legs on 31 ids |
| B1a false number `200` on K04 | TARGET_MISSED | 32/33 | bad 12/12 | MET | no (`num:K04`) | caught |
| B1b false number `46` on K04 (46 is K05's line, same pin) | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | the claim "capped at 46" has no source; 46 passes because it is a K-line of the pin |
| B2 every proposition negated ("It is not the case that …") | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | 33 of 33 rows assert the reverse of the line (e.g. K01: "It is not the case that the misc:disable_autoreload option is declared with … a default of false") |
| T1 token stuffing ("Row K01: misc is on this line, and this row records …") | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | filler with one identifier per row; no statement of what the line does |
| T2a neighbour shift (each row carries the NEXT row's honest proposition) | TARGET_MISSED | 4/33 | bad 12/12 | MET | no (tok legs) | misattributed sentences; caught by the shared-identifier rule |
| T2b neighbour proposition + own identifier | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | row K01 states K02's fact, plus "(misc on this line)" |
| T3a `source:` line moved to line 16 | TARGET_MISSED | 33/33 | bad 11/12 | MET | no (`prov`) | caught (control 6 then reports "mutation not applicable") |
| T4a S383 anchor `ConfigWatcher.cpp:1-111` (exact last line) | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | scope leg is vacuous for this pin: every line 1-111 is covered, so `scope:` can no longer fail for S383 rows |
| T4b S383 anchor `ConfigWatcher.cpp:1-112` (one past the last line) | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | bound defect: `ConfigWatcher.cpp` has 111 newline-terminated lines; the counter's bound is `len(blob.split(b"\n"))` = 112 |
| C1a same-pin scratch row: K10 cites `S399` (anchor `ConfigWatcher.cpp:60-70`, covers 67), `S399` added to `source:` | TARGET_MISSED | 33/33 | bad 10/12 | MET | no (`source_cell:K10`) | caught by the frozen `sid` identity check (K10's frozen sid is S383), not by the anchor |
| C1b S383 `teaches` cell replaced by a false sentence ("the watch list is never built from config files…") | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | the registry's own claim of what S383 teaches contradicts the pin; no leg reads `teaches` |
| P1a `source:` cites S999 with no registry row | TARGET_MISSED | 33/33 | bad 12/12 | **MISSED** (dangling) | no (`prov`) | caught |
| P1b `source:` cites S999; stub registry row S999 (used-by `-`) | **TARGET_MET** | 33/33 | ok 11/12 | **MISSED** (missing=1) | **yes, C1 alone** | a source the entry does not use; C3 catches it only through used-by |
| P1c as P1b, stub row S999 lists the entry in used-by | **TARGET_MET** | 33/33 | ok 11/12 | MET | **yes, both C1 and C3** | `S999` cited by nothing, anchored at `ConfigValues.cpp:1-5`; provenance only checks that cited sources are in the source line, not that listed sources are cited |
| T5 ten hand-written false propositions (K01 K02 K04 K05 K07 K10 K13 K15 K19 K25), 23 honest | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | ten sentences each contradict its line (e.g. K25: "ENVHOME is read from the environment variable USER on this line, not from HOME"); each has one identifier from its quote |
| T6 wave-1 cheap non-work entry, as delivered (registry anchors `1-<max line+999>`) | TARGET_MISSED | 33/33 | bad 12/12 | **MISSED** (extra=1) | no (`scope=2/30`) | 28 `scope:` legs; anchors past EOF; also: the readme line file carries a `83:` grep prefix that breaks the index leg (artifact, corrected for this run) |
| T6 same entry, anchors rewritten to each pin's real last line (only change) | **TARGET_MET** | 33/33 | ok 12/12 | **MISSED** (extra=1) | **yes** | "Line N of the pinned file holds X, which this row cites for the reload path" ×30; "Host capture … records X on line N" ×3; the trio `source/verified-at/recheck` is text, not a record; C3 catches the dropped S391 back-reference |
| B3 host row H01 states int value `1` (captured file says `"int": 0`); 1 is in the allowed-number set | **TARGET_MET** | 33/33 | ok 12/12 | MET | **yes** | a false host reading accepted |

Harness legs marked "mutation not applicable" or "mutant admitted" on forged trees are collisions: a control mutates a tree
that already holds the forgery (for example the stub S999 already exists, or K10 already cites S399). The harness then
reports 10/12 or 11/12 with `verdict=FAIL` for a reason unrelated to the forgery. The decisive harness leg is `good=ok`.

## Measured answers to the assignment's questions

**1. How many of the 33 honest propositions a lexical rewrite could falsify while keeping `content=33/33`:** 33 of 33
(B2). Each proposition is replaced by its negation; the counter's content leg stays 33/33 and the verdict is TARGET_MET
with `missed=none`. The five constraints the counter applies to a proposition, all met by a negation:
(a) at least 40 characters for K rows and 20 for H rows; (b) unique across the entry; (c) shares at least one identifier
of four or more characters with the frozen quote; (d) every digit run is in the quote, in {0,1,2,3}, or is the line of a K row
of the same pin; (e) when the quote has 30+ characters, the quote is not a substring of the proposition.

**2. Is TARGET_MET evidence of a sourced entry:** no. The counter never reads the meaning of a proposition, so the
content axis (does the sentence say what the pinned line says) is untested by the counter and by the harness, whose
controls are the same lexical class. The counter's green proves: the frozen quote is on the pinned line; each row's
source id maps to a registry row with the pinned URL suffix, the rev token, status `mined`, tier A/B, date 2026-10-28 and
the entry in `used-by`; the anchor range covers the quoted line; the source line lists the cited ids within the first 15
lines; and the proposition passes the five constraints above. It does not prove any proposition is true. The lane's own
declared limit (claims-frozen-v2 §C1) states this for a proposition that shares a quote identifier and keeps to the quote's
numbers; B2, T5 and B3 are exactly that class, and they are not the only ones that pass (see below).

**3. The registered limit says T1, T5 and T6 pass.** Confirmed for T1 (33/33), T5 (10 false, 33/33) and T6 only once its
anchors are inside each pin (anchors as delivered fail `scope:` 2/30). The wave-1 claim of "TARGET_MET for T6" was from a
checker that predates E3 (the anchor bound). Under v2 the delivered T6 entry is caught by E3; the trivial fix passes.

## Defects (input → what it shows → severity)

| id | input | shows | severity |
|---|---|---|---|
| D1 | B2, J1b, T1, T2b, T5, B3 (33 sentences each in one run) | the counter accepts false and template propositions that share one quote identifier; TARGET_MET is not evidence of content | **blocking** for the headline "sourced entry"; the frozen limit concedes the class, but the claim wording does not |
| D2 | T4b (`ConfigWatcher.cpp:1-112`, file has 111 lines) | scope bound is `len(split)`, one past EOF; a phantom line passes | weakens (small, code defect) |
| D3 | T4a (`1-111`) | a whole-file anchor makes `scope:` vacuous for that pin; the bound checks bounds, not that the range is the quoted region | weakens |
| D4 | C1b (teaches false) | the registry `teaches` cell is unread; a false claim about what a source teaches is accepted | weakens |
| D5 | P1b, P1c | provenance checks cited ⊆ source-line, not source-line ⊆ cited; a stub source row can be listed and admitted; C3 catches it only when used-by is empty | weakens (P1c passes both C1 and C3) |
| D6 | B1b, B3 | the number allowlist includes {0,1,2,3} and every K-line of the same pin, so a false number that happens to be one of those passes | weakens |
| D7 | every forged tree that collides with a control (P1b, P1c, C1a, T3a, J1c) | harness control counts (10/12, 11/12) go red for collision reasons, not detection; reading the harness red as "caught" is wrong | weakens (harness reporting) |
| D8 | T6 as delivered | `NONWORK-cheap-readme-line.txt` begins with a grep `83:` prefix; the index leg then fails. Wave-1 artifact, not a counter defect | cosmetic |
| D9 | T6 with anchors fixed | the entry drops S391 but the S391 registry row lists the entry in used-by; C3 reports `extra=1`. C1 alone passes | cross-claim note (C3 catches it; positive for C3) |

## Defects not found (null results, with the command)

- Shifted propositions (T2a): caught (`content=4/33`); nothing to report.
- Source line at line 15 vs 16 (T3a): the window is exactly the first 15 lines; line 16 is caught (`prov`).
- Same-pin registry swap with a frozen-sid mismatch (C1a): caught (`source_cell:K10`). The swap is not reachable through the counter.
- Scratch row without a registry entry (P1a): caught (`prov`; C3 `dangling=1`).
- Echo bypass: no full-quote echo passed in any variant (J1a caught all 29 quotes of 30+ characters through `echo:`; 29 of 33 quotes are that long)

## Could not verify / not run

- Truth of the 33 honest propositions: I read them against the quotes and the pinned files only for the rows I falsified or
  named; I did not re-derive the source behaviour (the counter does not check it either). The B2 "falsified" claims are
  negations of those readings.
- Entailment by a non-author reader (the lane's stated next step) was not run; this seat only shows what the counter cannot see.
- The live host was not read (not needed: H01's quote `"int": 0` is byte-checked against the pinned capture by the counter).
- C2 and C3 predicates were not attacked beyond the C3 cross-check on each commit.
- Harness controls were not re-designed against forged trees; the collisions in D7 are reported as they came out.

## Commands that produced the numbers

Each row of the table is one `run_variant` call: edit set → one commit in `W` → the three commands above → `receipts/<variant>.txt`.
The base row is `base-honest`. Full outputs are in `receipts/`; the trimmed lines in this report are copied from them.

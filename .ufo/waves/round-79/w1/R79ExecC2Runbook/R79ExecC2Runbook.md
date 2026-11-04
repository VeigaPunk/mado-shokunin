# R79ExecC2Runbook — C2 runbook execution audit (round 79, wave 1)

Seat: executor, 2026-11-04. Scope: execute the round-79 runbook from documentation alone
(own parser, no counter), check the per-row binding direction, and prove the counter's tree
binding refuses foreign bytes — all from read-only probes plus a scratch copy. Freeze
`5eb8f20fe291603c74973fa94cc55723ac8089a4`; measured receipts untouched. No repo edits, no
git/jj write commands, no tool installs (operator tooling authorization unused).

## 1. Extraction with an own parser; verbatim execution; receipt comparison

Parser: independent re-implementation of the documented cell rule — split a table row on
unescaped pipes, `\|` → literal `|`, strip the backticks, skip header/separator
(`quality/counters/c2-r79-runbook.py:165-183,185-201` documents the rule my parser follows;
I did not import or execute the counter for extraction). Section
`### Executable runbook rows (round 79)` at `SKILL.md:231`, table header `SKILL.md:241-242`,
**22 command rows at `SKILL.md:243-264`**. The heaviest escape case, row 8
(`SKILL.md:250`), unescapes to
`hyprctl layers -j | jq -r '[to_entries[] | .value.levels | to_entries[] | select(.value|length>0) | .value[].namespace] | sort | join(",")'`
— my parser reproduces every cell byte-identically (`results.json` `rows[7]`).

Execution: each of the 22 cells run verbatim via `/bin/sh -c <cell>` from the lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, with the counter's documented environment
contract (LC_ALL=C, XDG_RUNTIME_DIR, `HYPRLAND_INSTANCE_SIGNATURE` discovery, OMARCHY_PATH
discovery, PATH extension; counter `:100-138`). Scoring re-implements the documented
expectation rule (counter `:243-307`) including the refusal special-case
`rc == value.rc and "ERROR (stage=model " in stdout` (`:302-307`).

Result: **22/22 matched.** JSON-dump kinds are reported byte-count only, per the receipt's
own masking rule (counter `:331-338`):

| row | case | kind | match | observed |
|---|---|---|---|---|
| 0 | version | regex | yes | `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f …` |
| 1 | configerrors | empty | yes | rc 0, empty |
| 2 | monitors-size | regex | yes | `DP-1 3440x1440@99.99700` |
| 3 | monitors-reserved | int4 | yes | json 11 bytes |
| 4 | gaps-out | exact | yes | `custom type: 0 0 0 0` |
| 5 | kb-layout | exact | yes | `str: br` |
| 6 | binds-count | int_range | yes | `192` |
| 7 | layers-namespaces | sorted_unique | yes | `wallpaper,waybar` |
| 8 | waybar-process | int_range | yes | `1720` |
| 9 | mako-mode | exact | yes | `default` |
| 10 | omarchy-theme | exact | yes | `Matte Black` |
| 11 | omarchy-version | regex | yes | `3.8.3` |
| 12 | active-workspace | json_object_fields | yes | json 20 bytes |
| 13 | layers-dump | levels_dump | yes | json 748 bytes |
| 14 | monitors-dump | array_fields | yes | json 1339 bytes |
| 15 | clients-count | int_range | yes | `2` |
| 16 | workspaces-count | int_range | yes | `2` |
| 17 | refuse-mode | refusal | yes | rc 3, `stage=model` (mode preset) |
| 18 | refuse-scale | refusal | yes | rc 3, `stage=model` (scale/transform 2.0) |
| 19 | refuse-layer-background | refusal | yes | rc 3, `stage=model` (background layer) |
| 20 | refuse-output-space | refusal | yes | rc 3, `stage=model` (`'DP-1 DP-2'` outside subset) |
| 21 | omarchy-menu-keybindings | lines_shape | yes | rc 0, 193 arrow lines (≥100) |

Receipt comparison, case by case against
`.ufo/waves/round-79/receipts/measurement-c2-r79.txt` (frozen, `TARGET_MET` at the freeze):
**row/kind/match agree on 22/22 probes; observed strings agree on 21/22** — the single
difference is my masking of case 21 (`rc=0 lines=193`) where the receipt quotes the first
100 characters; both are the same live `omarchy menu keybindings --print` reply. Every
volatile value happened to reproduce (pid 1720, binds 192, clients 2, workspaces 2).

Independent carried-field freeze re-check: the 17 round-78 cases
(`.ufo/waves/round-78/controls/c2-runbook-cases-r78.json`) match the first 17 r79 cases on
**every field except `skill_anchor`** — 0 drifted fields, 0 field-set changes
(`results.json` `carried_field_drift`).

## 2. Binding direction

Mechanism in the counter: a case binds rows by **string equality**
(`hits = [index … if cell == case["skill_anchor"]]`, `quality/counters/c2-r79-runbook.py:509`);
double binding and unbound rows raise Setup (`:510-518`).

My independent check over the frozen set and my parsed rows:

- every one of the 22 cases' `skill_anchor` equals **exactly one** row cell (no 0-hit, no
  2-hit case);
- every one of the 22 rows is claimed by **exactly one** case (`rows=22/22`);
- every `skill_anchor` equals its case's executed argv command string (18 shell cells equal
  `argv[2]`; 4 barfoot cells equal the joined direct argv);
- result flags in `results.json`: `all_single_bind=true`, `every_row_bound=true`,
  `all_anchor_equals_cell=true`.

Prefix/equality ambiguity (advisory): three row cells are strict prefixes of other row
cells, exactly the shape the seat brief warned about —

1. `hyprctl layers -j` (row 13, `SKILL.md:256`) is a strict prefix of row 7 (`SKILL.md:250`);
2. `hyprctl monitors -j` (row 14, `SKILL.md:257`) is a strict prefix of row 2 (`SKILL.md:245`);
3. `hyprctl monitors -j` (row 14) is a strict prefix of row 3 (`SKILL.md:246`).

Because binding is equality (`:509`), never a prefix match, none of these pairs can
cross-bind; each of the six rows involved is bound by exactly one distinct case. The
ambiguity would only bite a future matcher that switches to `startswith`.

## 3. Tree binding proof (scratch copy only; the lane was never written)

Method: `cp -a` of the lane into `/fast/scratch/hyaku/mado-r79/R79ExecC2Runbook/lane-copy`
(`.git` included — a directory, so the copy is self-contained); `git rev-parse
--show-toplevel` asserted to print the copy path before any git call; every git invocation
names `-C` the copy. No git/jj write command was run anywhere; blob contents were materialized
with `git show` + file writes inside the scratch copy.

Independent hashes at audit time (lane working tree vs freeze blobs, runner `tree_hashes`):
`SKILL.md` `f0db766153e54b4fbe3147f3a906a33bdca5a278875d43265269e72a117be234` (equal),
`tools/mado-barfoot.py`
`c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de` (equal — also the exact
r79-v1 sha256 pinned in the wave brief), all **12/12 refusal-fixture files equal** their
rev blobs.

Finding during the proof: between my audit and the copy, the **lane advanced past the
freeze** — `git log -3` now reads `3b8af34c…` ("round-79: record corrections from the wave's
source and case re-derivations") → `03e76ee9…` ("round-79: the static-reserve entry,
sources, lesson, scorecard and log") → `5eb8f20f…` (the freeze), and the lane's live
`SKILL.md` bytes are `dd456980…`, no longer the freeze blob `f0db7661…`. The unpinned copy
therefore refused at baseline — rc 2, `stage=setup SKILL.md in the working tree is not the
measured revision's bytes` (`tamper-results.json`) — the counter correctly refusing a
non-freeze tree before any tamper of mine. The frozen receipt remains the record of the
freeze state; any re-measurement at the new HEAD is designed to rc 2.

Pinned proof (`pin-results.json`): after materializing the copy's 14 counter-bound files
(SKILL.md, tool, 12 fixture files) from `git show 5eb8f20f:<path>`:

- baseline-pinned: rc **0**, `cases=22 executed=22 matched=22 shapes=17/17 anchors=22/22
  rows=22/22 control_new=0/5 mutants=0 killed=0 verdict=TARGET_MET … tree=bound`
  (mutant clause suppressed with the counter's own `--no-mutants` flag);
- tamper `SKILL.md` one byte **outside the runbook section** (`globals`→`globalZ`) → rc **2**
  `SKILL.md in the working tree is not the measured revision's bytes` (counter `:489-496`) —
  the binding is byte-level over the whole file, not section-level;
- tamper `tools/mado-barfoot.py` one byte → rc **2** naming `tools/mado-barfoot.py`;
- tamper `.ufo/waves/round-79/fixtures/refuse-mode/config.json` (append `\n`) → rc **2**
  `fixture … is not the measured revision's bytes` (counter `:497-501`);
- restore the three files from rev blobs → rc **0**, `tree=bound` again.

## Data

Evidence copied into `.ufo/waves/round-79/w1/R79ExecC2Runbook/`:
`results.json` (parser rows+line numbers, binding, prefix pairs, live probes, receipt
comparison, tree hashes), `pin-results.json` (drift diagnosis + pinned refusal proof),
`tamper-results.json` (pre-pin refusals on the drifted copy), and the scripts
`runner.py`, `tamper.py`, `pin.py`. Cited frozen artifacts live at their committed paths
(`receipts/measurement-c2-r79.txt`, `controls/c2-runbook-cases-r79.json`,
`quality/counters/c2-r79-runbook.py`). Scratch deleted after the copy.

## Risks / notes for the L1

1. Lane HEAD moved past the freeze mid-wave (two integration commits; SKILL.md bytes
   changed `f0db7661…`→`dd456980…`). Not a C2 defect — the counter's refusal behaved as
   designed — but the frozen measurement now refers to a non-HEAD revision, and C2's
   predicate can only be re-demonstrated at `5eb8f20f…` bytes.
2. All 22 rows re-executed green against live host state on 2026-11-04, byte-identical to
   the frozen receipt on every observed value.
3. No C2 predicate failed; no blocker.

Report: .ufo/waves/round-79/w1/R79ExecC2Runbook.md

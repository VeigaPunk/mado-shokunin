# R79RevC2 — adversarial review of C2 (operability), round 79

Seat: R79RevC2 (reviewer, leaf). Scope: re-derive the C2 claim; do not trust the receipt.
Freeze: `5eb8f20fe291603c74973fa94cc55723ac8089a4`; base: `e4b153dfa4a67ca56f7ec65cb6639082451626a7`.
Instrument read in full: `quality/counters/c2-r79-runbook.py` (585 lines; sha256
`66b10d024a75f0e90e24bc535bd64a2106a7ecf273fc0f8dce1315a145c72df0` — unpinned anywhere, recorded).

## Axis named

Operability = each frozen runbook row is (a) bound 1:1 to a SKILL.md row whose command cell is
the executed command, (b) executed live, (c) matched under its declared shape including exit
status, churn and negatives, (d) discriminating (9 matcher mutants die), (e) tree-bound to the
measured revision. Sub-axes attacked below: reproduction, shape count, binding grammar, refusal
matcher, tree binding, claim size, control meaningfulness.

## 1. Reproduction of the committed receipt — CONFIRMED

Command (from the declaration, verbatim):

```
python3 -I quality/counters/c2-r79-runbook.py --repo . \
  --rev 5eb8f20fe291603c74973fa94cc55723ac8089a4 \
  --controls .ufo/waves/round-79/controls/c2-runbook-cases-r79.json \
  --carried .ufo/waves/round-78/controls/c2-runbook-cases-r78.json \
  --scratch-root /fast/scratch/hyaku/mado-r79/R79RevC2
```

Observed: exit 0; output **byte-identical** to
`.ufo/waves/round-79/receipts/measurement-c2-r79.txt` (33/33 lines; the only diff vs my capture
is my own `exit=0` echo line). Every count reproduced: `executed=22 matched=22 shapes=17/17
anchors=22/22 rows=22/22 control_new=0/5 killed=9/9 control_all=15/22 tree=bound
verdict=TARGET_MET`. Per-line probe and mutant results identical, including per-mutant matched
fractions (16/22, 19/22, 20/22, 21/22 ×3, 18/22 ×2).

**Independent `shapes=17/17` enumeration.** Counted the case set directly
(`.ufo/waves/round-79/controls/c2-runbook-cases-r79.json`): kinds are regex×3, exact×4, empty×1,
int4×1, int_range×4, sorted_unique×1, json_object_fields×1, levels_dump×1, array_fields×1,
refusal×4, lines_shape×1. Exactly 17 of 22 fall in the counter's SHAPE_KINDS tuple
(`c2-r79-runbook.py:95`); the 5 non-shape cases are `configerrors` (empty), `gaps-out`,
`kb-layout`, `mako-mode`, `omarchy-theme` (exact). 17/17 confirmed against the tuple, not the
receipt.

**Independent binding enumeration.** Extracted the runbook section from the git blob (awk cut on
`### Executable runbook rows (round 79)`), re-split cells independently: 22 command rows; every
anchor hits exactly one row; row order equals case order; all 22 anchors distinct. SKILL.md
section text itself declares the four refusal rows "bind the refusal stage, not its message".

**Anchor == executed command.** For 18 cases argv is `['/bin/sh','-c',anchor]`; for the four
refusals argv is the direct token list with `' '.join(argv) == anchor`. Zero mismatches across
all 22 — the claim's "command cell equals the case's command" holds literally.

Selftest: `python3 -I quality/counters/c2-r79-runbook.py --selftest` → `55/55`, exit 0.

## 2. Grammar / matcher / tree attacks

### Binding grammar — all fail-closed (simulated on counter logic, `c2-r79-runbook.py:509-516`)

- One row satisfying two anchors: impossible under equality with 22 distinct anchors; forced
  duplicate anchors → `Setup: anchor binds 2 rows`.
- Deleted row: anchor binds 0 rows → Setup. A deleted row cannot "survive through" another row:
  binding is 1:1 by exact equality plus an explicit double-booking check (`:513-515`) and a
  count check (`:516-517`).
- Prefix/equality spoof (`cmd1` anchor vs `cmd1 extra` row, whitespace-padded cells): equality
  only → Setup. Header row named `Command` and separator variants (`|:--|--:|`, `|-|-|`)
  correctly skipped (`command_rows`, `:185-207`). Rows after the next `###` ignored.
- Escaped-pipe splitter (`split_cells`, `:165-183`), byte-level battery:
  - `\|` → `|` (backslash consumed, pipe literal) — the 19 occurrences in the runbook section,
    all inside jq programs, extract correctly.
  - `\\|` → `\|`; `\\\|` → `\\|` — left-to-right pairing consumes one backslash per `\|` pair.
    No backslash is silently dropped inside a cell; the divergence from strict CommonMark
    (`\\|` = escaped backslash *then* a cell delimiter) is **unreachable on frozen bytes** — the
    runbook section contains zero `\\|` sequences — and any divergence fails closed (anchor
    mismatch → Setup), never silently passes. Trailing `\`, leading `\|`, and non-table lines
    all behave. The counter's own selftest pins both behaviors ("escaped pipe stays in the
    cell", "other backslashes survive").

### Refusal matcher (`refusal_matches`, `:302-306`) — 11-case attack battery, all correct

- Message-only refusal: **passes by design** — the matcher checks `rc == value["rc"]` and the
  substring `"ERROR (stage=%s " % stage` only; the committed churn sample
  ("…a different reason here") is accepted. This is declared in SKILL.md ("bind the refusal
  stage, not its message"). Consequence: the four refusal rows prove "refuses at stage=model
  with rc 3", not "models the four scenarios"; a degenerate always-refuse tool would pass these
  four rows but is defeated by C1 (23 cases; a refusal on the static-composed case breaks
  `correct=23`). Cross-claim defense holds.
- Stage spoofing: `stage=modelX`, `stage=model-extra`, `stage=model)` (no trailing space) all
  **refused** — the pattern's trailing space after `%s` blocks prefix spoofs; `stage=setup` with
  rc 3 refused.
- rc spoofing: rc=2 with the genuine message, rc=0 clean, rc=0 *with* the marker on stdout, and
  marker-absent stdout with rc=3 — all refused. Exit status is exact-equality, not a range.

### Tree binding — verified, then attack-demonstrated live

- Independent sha256 of 14 paths (SKILL.md at rev, `tools/mado-barfoot.py`, 12 fixture files)
  vs `git show <rev>:<path>` blobs: **all match** at review time of the instrument bytes.
  Tool sha256 = declaration pin `c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de`.
  Each refusal fixture dir holds exactly its 3 pinned files — no unpinned extras.
- **Live stale-tree attack (finding for the L1):** after my clean re-run, a sibling edit at
  07:31 changed one prose line of SKILL.md *outside* the runbook section (the C1 gate row,
  "carried byte-identically" → "carried unchanged (parsed equality)"; `git diff 5eb8f20f --
  SKILL.md` = 1 line, +11/-11 bytes). Re-running the counter against this drifted tree:
  `MADO_R79_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured
  revision's bytes)`, **exit 2**. The stale-tree attack is caught, fail-closed, whole-file.
  Implication: the fleet tree is *currently unbound* — the receipt stands as the at-freeze
  measurement, but no fresh TARGET_MET run will pass until the tree matches the rev (land the
  edit or restore the file). Not a claim regression; a gate state the L1 must know before any
  re-measurement.
- Fixture-edited-in-place: same sha check (`:497-502`) covers every file each case lists; the
  argv-referenced files and the pinned files are the same 12. Fail-closed.
- Residual (process-guaranteed, not measured): the `--controls` and `--carried` JSONs are read
  from the working tree and never compared to the rev blobs, and the counter's own source is
  read from `__file__` on disk for mutant derivation (`:548-552`), not from git. An edit to any
  of the three would be scored silently. Covered today only by the freeze + lane rules.

## 3. Axis and size attacks

- **Four of 22 rows run the lane's own tool.** Declared in the claim text itself and in the
  SKILL.md section prose; the refusals are byte-pinned, sha-verified, and defended in
  composition by C1 (see above). As a *standalone* axis, "operability" of those four rows is
  thinner than the receipt reads: it certifies refusal plumbing, not scenario modelling. Fair
  as declared; flagged as a scope caveat.
- **`rows=22/22` and `anchors=22/22` are preconditions, not measurements.** Both are enforced
  as Setup errors (`:506-517`) before any probe runs; the verdict line can never print a
  partial value for them. Honest but structural — the evidential work is done by `matched`,
  `shapes`, `killed`.
- **`control_new=0/5` is structurally guaranteed and one-sided.** `held_rule` returns False
  whenever `"frozen" not in case` (`:309-313`); all five new cases lack `frozen` (verified in
  the JSON); and even with one, the refusals' rc=3 can never meet the held rule's `rc == 0`.
  The control can only trip via gaming, never discriminate good from bad new matchers — as a
  do-nothing control it carries **zero evidential weight**. The real discriminators are the
  nine killed mutants and the `control_all` observation.
- **`control_all=15/22` explained, zero drift.** All 15 carried cases that have a frozen value
  still match it exactly (re-executed each live just now); `layers-dump` and `monitors-dump`
  have no frozen field and never match. Host state is unchanged since freeze (clients=2,
  workspaces=2). The declaration's "host-state dependent, never a predicate" disclaimer is
  accurate.
- **Mutant kills are host-state-dependent** (`dead = mrc != 0 and mmatched < CASES`, `:557`):
  a kill requires the live host output to exercise the mutated branch. At freeze and at re-run
  all nine died with stable fractions; a host change could flip a kill in either direction —
  an honest stop, and the receipt's fractions are exactly reproducible today.
- **Weak-but-harmless bound:** `waybar-process` allows `1..4194304` == `/proc/sys/kernel/pid_max`
  (4194304), i.e. any live PID passes the range; discrimination rests on its churn/negative
  samples. Minor; no action.
- Environmental trust: probes resolve `hyprctl`/`omarchy` via PATH plus injected
  `~/.local/bin` (`:126-146`); a hostile PATH entry could shadow a probe binary. Host-level
  assumption, out of lane scope; recorded for completeness.

## Verdict

Receipt reproduced byte-identically from a clean scratch (exit 0); independent enumerations
confirm `shapes=17/17`, 22 distinct anchors, 1:1 binding, anchor==command; grammar, refusal
matcher, and tree binding all fail closed under every attack tried, including a real stale-tree
event mid-review (counter now exits 2 until the fleet tree is re-bound). No defect found that
invalidates the C2 claim at the freeze. Findings are scope caveats: the held-r78
`control_new` control is vacuous-by-construction; four rows certify refusal plumbing rather
than modelling; `rows`/`anchors` are structural; and the controls JSON + counter source are
tree-pinned by process, not by measurement.

**L1 action:** the working tree's SKILL.md currently differs from `5eb8f20f` (one-line C1-table
prose edit, outside the runbook section). Any re-measurement of C2 (or C1, whose counter checks
the same file) will exit 2 until the tree is restored or the edit is landed.

## Evidence index (all commands run, outputs observed)

- Re-run receipt diff: `diff rerun-c2.txt receipt-committed.txt` → identical (33 lines), exit 0.
- Stale-tree re-run (after 07:31 SKILL.md edit): rc 2,
  `ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)`.
- `git diff 5eb8f20f -- SKILL.md`: 1 line changed in the C1 gates table.
- Battery scripts and outputs in scratch (deleted on completion per seat rules).
- Citations: `quality/counters/c2-r79-runbook.py:95` (SHAPE_KINDS), `:165-207` (split_cells,
  command_rows), `:243-300` (matches), `:302-313` (refusal/held), `:495-517` (tree + binding),
  `:548-557` (mutant harness), `:565-575` (target).

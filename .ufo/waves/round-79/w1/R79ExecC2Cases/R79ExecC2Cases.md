# R79ExecC2Cases — independent re-derivation of the five new C2 cases and their mutant separation

Seat: R79ExecC2Cases (executor, round-79 wave 1, leaf). Freeze:
`5eb8f20fe291603c74973fa94cc55723ac8089a4`; base:
`e4b153dfa4a67ca56f7ec65cb6639082451626a7`.

The lane advanced during the seat: `5eb8f20` (freeze) → `03e76ee9` → `3b8af34c` →
`d6be05ef` ("repair R1: an addreserved with no prior rule drops its area") → `8696c4dd`
("scorecard and log at the repaired measurement"). The dynamic mutant runs below were taken
at `8696c4dd` (the harness baseline line records that rev); the live case runs were taken
across `3b8af34c`–`8696c4dd`, and the H1 baseline is green at both measured ends.

## Pins and tree state (observed)

| artifact | sha256 |
|---|---|
| `quality/counters/c2-r79-runbook.py` (freeze = HEAD) | `66b10d024a75f0e90e24bc535bd64a2106a7ecf273fc0f8dce1315a145c72df0` |
| `.ufo/waves/round-79/controls/c2-runbook-cases-r79.json` | `50a18041ccd94f337216efeeb3fd60dddd52b35c26480f91fddd028a948a9c7b` |
| `.ufo/waves/round-78/controls/c2-runbook-cases-r78.json` (carried) | `f1c75a7dba92d7c1e0dae4feb60c022e0bacd4c95e03a95cfc53ccf7788932e8` |
| `tools/mado-barfoot.py` at the freeze (declared r79-v1) | `c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de` |
| `tools/mado-barfoot.py` at HEAD (repair R1) | `673ac44d176ce2dd63701c6db6f3f1116ed059cc62d9000c6e57423341c60f99` |
| `SKILL.md` at the freeze | `f0db766153e54b4fbe3147f3a906a33bdca5a278875d43265269e72a117be234` |
| `SKILL.md` at HEAD | `7595f499209537ae00b474a6d70c3592af8c23ab9e4bcd41dbab3a1dc1c9fd95` |

`git diff --numstat 5eb8f20 HEAD` over SKILL.md, tool, C2 counter, C2 controls and the
fixture tree returns only `2 2 SKILL.md` and `19 7 tools/mado-barfoot.py`. **The C2 counter,
the C2 control set and all twelve refusal-fixture files are byte-identical from the freeze
to HEAD.** The SKILL.md change is two gate-row text lines (the `mado-r77-barfoot` selftest
count `43/43`→`44/44`; the C1 row's control sha and "carried unchanged (parsed equality)");
the `mado-r79-runbook` row is untouched. The tool change is the C1 fall-through repair plus
one appended selftest assertion; the refusal emit sites are untouched (verified below).

The declared counting command on the current tree exits 2 by design:
`MADO_R79_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's
bytes)` (observed; the same tree-bind shape the declaration assigns to the base-rev before
state). The pinned receipt at `5eb8f20` remains the claim measurement; re-running it verbatim
requires the freeze tree.

Runbook section at the freeze blob (`git show 5eb8f20:SKILL.md`, independent re-implementation
of `command_rows`): **22 command rows, 22 distinct**, and the keybindings anchor
`omarchy menu keybindings --print` binds exactly 1 row.

No package transactions or installs; no repo writes outside this seat's paths; no
git/jj mutation; every host probe was a read verb.

## Task 1 — the four refusal fixtures

Exact argv from the control set, cwd = lane root, executed against the working tree
(HEAD tool, repair R1):

| case | rc | stage | observed message (verbatim) |
|---|---|---|---|
| `refuse-mode` | 3 | model | `MADO_BARFOOT: ERROR (stage=model a mode preset rewrites layer and exclusive zone at runtime)` |
| `refuse-scale` | 3 | model | `MADO_BARFOOT: ERROR (stage=model monitor M1 has scale/transform 2.0/0; the reply carries pixel size and the layer box is logical, so this join is not modelled)` |
| `refuse-layer-background` | 3 | model | `MADO_BARFOOT: ERROR (stage=model waybar's presets never select the background layer)` |
| `refuse-output-space` | 3 | model | `MADO_BARFOOT: ERROR (stage=model output pattern 'DP-1 DP-2' is outside the modelled subset)` |

The four messages are pairwise distinct (4/4). Each fixture carries exactly one triggering
feature and the rest of the bytes are shared controls:

| fixture | config.json sha256 | trigger | layers.json | monitors.json |
|---|---|---|---|---|
| refuse-mode | `7abe6664…` | `"mode": "dock"` | `e2c931e8…` (shared by all four) | `48af891c…` (shared by mode/layer/output) |
| refuse-scale | `66973542…` | monitors `"scale": 2.0` | `e2c931e8…` | `1acf1041…` |
| refuse-layer-background | `b3257231…` | `"layer": "background"` | `e2c931e8…` | `48af891c…` |
| refuse-output-space | `4baf700f…` | `"output": "DP-1 DP-2"` (a space) | `e2c931e8…` | `48af891c…` |

Not a setup error dressed as a model refusal — three independent discriminators:

1. **The setup path is separate and observable.** A missing config probe exits 2 with
   `MADO_BARFOOT: ERROR (stage=setup unreadable path …does-not-exist.json: [Errno 2] No such
   file or directory…)`. The tool maps `Unmodelled` → `stage=model`, rc 3 and `Setup` →
   `stage=setup`, rc 2 (`tools/mado-barfoot.py:852-857`; exit map `:69`). An unreadable or
   malformed input therefore cannot arrive as rc 3 / `stage=model`.
2. **The tool consumed all three inputs before the model refusal.** `main` loads config,
   layers and monitors (raising `Setup` on failure) before `evaluate()`
   (`tools/mado-barfoot.py:832-851`); all twelve fixture files are valid JSON (read in full).
   Each refusal text is the exact `Unmodelled` raise for the fixture's content feature:
   mode `:302-303`, background layer `:299-300`, spaced output `:280-281`, scale `:499-501`.
3. **Removing the trigger removes the refusal.** Repaired scratch copies (trigger key
   removed/neutralised, all other bytes identical) exit 0 with a `MADO_BARFOOT_CONFIG: pos=top
   layer=top level=2 ns=waybar height=26 …` trace and no `stage=model` line — 4/4.

Rule scope note: the case rule binds **rc + stage only** (`quality/counters/c2-r79-runbook.py:302-306`);
the message is deliberately not scored (churn sample `a different reason here`, e.g.
`.ufo/waves/round-79/controls/c2-runbook-cases-r79.json:554`). The distinct-reason property is
therefore verified of the tool/fixtures, not something the matcher can see.

**Verdict: 4/4 genuine `stage=model` exit-3 refusals, distinct; none is a setup error in
disguise.**

## Task 2 — the `omarchy menu keybindings --print` row

Live run (`omarchy menu keybindings --print`, read verb): rc 0, **193 lines, 193/193 matching**
the declared regex `^\s*\S.*\s*→\s*\S.*$`, 0 blank lines, ≥ `min_lines` 100
(`.ufo/waves/round-79/controls/c2-runbook-cases-r79.json:745-746`).

Independent implementation of the declared `lines_shape` rule (rc 0 gate, line floor, **every**
line matches):

| sample | rc | lines | lines matching | rule accepts | required |
|---|---|---|---|---|---|
| live | 0 | 193 | 193 | yes | accept |
| sample[0] (`:735`) | 0 | 120 | 120 | yes | accept |
| sample[1] (`:739`) | 0 | 130 | 130 | yes | accept |
| negative[0] (`:713`) | 0 | 0 | 0 | no | reject |
| negative[1] (`:717`) | 0 | 1 | 1 | no | reject |
| negative[2] (`:721`) | 1 | 120 | 120 | no | reject |
| negative[3] (`:725`) | 0 | 99 | 99 | no | reject |
| negative[4] (`:729`) | 0 | 120 | 0 | no | reject |

Case verdict: true. The churn samples are plausible next-day bind sets (different keys,
same arrow shape) and are accepted; the negatives exercise every clause (empty, length floor,
exit status, 99 < 100, grammar). The row binds exactly once (see pins above).

## Task 3 — separation table for the four new mutants

Two independent legs, same result: (a) static evaluation of the declared mutated rules over
the exact control bytes plus the live outputs; (b) execution of scratch copies of the frozen
counter with the declared single-anchor mutation applied (`--no-mutants`). Leg (b) used a
**disclosed harness variant H1**: the counter's byte-bind was reduced from
(SKILL.md, tools/mado-barfoot.py) to (SKILL.md) because the committed repair R1 changes the
tool bytes; SKILL.md still bound to `--rev HEAD`, every case still executed the working-tree
tool, and the mutation under test is never the relaxation. Baseline under H1:
`cases=22 executed=22 matched=22 shapes=17/17 anchors=22/22 rows=22/22 control_new=0/5
verdict=TARGET_MET rev=8696c4ddf35223d69c0558603e110bc0f6263c4b tree=bound`.

| mutant (counter lines) | measured matched | killed | flipped cases | killing sample(s) |
|---|---|---|---|---|
| `refusal-stage-blind` (`:77-80`) | 18/22 | yes | all four refusal cases | each refusal case's `negatives[1]` — rc 3 with `stage=setup` (controls `:544/:590/:636/:682`) |
| `refusal-rc-blind` (`:81-84`) | 18/22 | yes | all four refusal cases | each refusal case's `negatives[0]` — rc 2 with `stage=model` (controls `:540/:586/:632/:678`) |
| `lines-any-line` (`:85-88`) | 21/22 | yes | `omarchy-menu-keybindings` | `negatives[1]` (1 valid line, `:717`) and `negatives[3]` (99 valid lines, `:725`) |
| `lines-min-lines-dropped` (`:89-91`) | 21/22 | yes | `omarchy-menu-keybindings` | `negatives[0]` (empty, `:713`), `negatives[1]` (`:717`), `negatives[3]` (`:725`) |

Live outputs and churn samples never flip under any of the four mutants (they satisfy every
mutant); every kill is a committed negative. The measured matched counts reproduce the pinned
receipt exactly (`MADO_R79_MUTANT: … matched=18/22`, `18/22`, `21/22`, `21/22` in
`.ufo/waves/round-79/receipts/measurement-c2-r79.txt`), and the static leg reproduces the same
flip sets case for case.

**Sharing and separation.**
- `omarchy-menu-keybindings` `negatives[1]` and `negatives[3]` are each load-bearing for
  **both** lines mutants.
- The `lines-any-line` kill set `{1,3}` is a strict subset of the
  `lines-min-lines-dropped` kill set `{0,1,3}`: **no single sample kills `lines-any-line`
  alone.** The only sample separating the two lines mutants is `negatives[0]` (empty output —
  `all([])` is `True` once the length floor is dropped), which kills
  `lines-min-lines-dropped` only.
- Samples **not load-bearing for the four new mutants**: keybindings `negatives[2]` (rc=1) —
  it is load-bearing for the carried `rc-blind` instead (H1 control run: `rc-blind` flips 6
  cases including the keybindings case, `matched=16/22`, matching the receipt); keybindings
  `negatives[4]` (120 lines, 0 matching — guards a pattern-ignored/`any`-class mutant not in
  the set); each refusal case's `negatives[2]` (rc 0 `CLEAN`); and every churn sample (by
  design, samples must match).

**No unkillable mutant and no unseparated kill.** All four are killed and every flip is
attributed to a committed sample. The only caveat is the shared pair above: the two lines
mutants are individually killed, but no sample is unique to `lines-any-line`.

## Evidence files (copied into this seat's dir)

- `.ufo/waves/round-79/w1/R79ExecC2Cases/rederive.json` — hashes, four refusal transcripts +
  repaired-copy controls + setup probe, live keybindings stats, per-sample rule evaluation,
  static mutant table, freeze-section row extraction.
- `.ufo/waves/round-79/w1/R79ExecC2Cases/keybindings-live.txt` — the 193-line live reply.
- `.ufo/waves/round-79/w1/R79ExecC2Cases/mutants-relaxed.json` and `relaxed-log-*.txt` —
  H1 baseline + five mutant runs (four new + carried `rc-blind`) with revs and flip lists.
- `.ufo/waves/round-79/w1/R79ExecC2Cases/mutants.json` and `log-baseline.txt` — the frozen
  harness refusing to run on the drifted tree (the tree-bind observation, rc 2).
- `.ufo/waves/round-79/w1/R79ExecC2Cases/measurement-c2-r79.txt`,
  `control-c2-heled-instrument-at-base.txt` — copies of the pinned receipts cited above.

## Risks / open points

1. The declared counting command is only re-runnable on the freeze tree; on HEAD it is rc 2
   by design (tree bind). If the L1 wants a post-repair C2 re-measurement, that needs a new
   freeze/controls run, not a re-run of this receipt.
2. My live refusal runs executed the successor tool (repair R1, `673ac44d…`), not the frozen
   `c9aa1391…` bytes. Observed rc and messages are byte-identical to the receipt, so the
   cases survive the successor; the pinned receipt remains the freeze evidence.
3. H1 is a disclosed deviation: it skips only a byte-equality guard (never an assertion), and
   the mutation under test is applied exactly once to the frozen counter source.
4. `Report:` path below; this file is also copied into the seat's write directory.

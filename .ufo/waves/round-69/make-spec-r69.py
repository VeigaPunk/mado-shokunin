#!/usr/bin/env python3
"""Build the round-69 wave spec (ONE v1 wave, 12 seats). Deterministic; no network, no host writes."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE_DIR = LANE + "/.ufo/waves/round-69"

GOD = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = GOD + """

Round mado 69, ONE v1 wave (12 seats). Axes: calibration (C1) and operability (C2). The L1 holds the planner seat (the validator rejects a planner role); no planner is dispatched.

Read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/claims-declaration-r69.md FIRST. Claims, predicates, control set, recipe texts and targets are FROZEN at 789a87f1a667b43dd759222a2f048bf8f75b43ce (base 04093b83f73a841117d3b31dbb2a6063f4f2a454). Never re-scope, never narrow a target after seeing data, never invent a different counter, never edit the declaration, the control JSON or the baseline receipt.

Lane repo (absolute): /home/vgpnk/Projects/shokunin/mado-shokunin. Frozen do-nothing control receipt: .ufo/waves/round-69/control-baseline-r69.txt. Feasibility prototypes (evidence, not production): .ufo/waves/round-69/proto/.

Write ONLY your own seat directory /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/<your-name>/ — drafts of production files go under draft/<repo-relative path> inside it; the L1 integrates them and you never write a production path. Reading sibling seat dirs is allowed. Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mado-shokunin — write it at /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>.

Scratch: /fast/scratch/hyaku/mado-r69/<your-name>/ (mkdir -p first) with delete-on-exit (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree(dir, ignore_errors=True)` in Python). Never rely on an inherited TMPDIR, never write /tmp or /var/tmp. Report the scratch removed before you yield.

Never commit, push, stage, stash, checkout, switch, reset or run any mutating git/jj command in the lane, the fleet repo /home/vgpnk/Projects/shokunin, or any sibling lane. Never write the fleet repo, another lane, MANIFEST.json, .ufo/state, .scratch, or operator config. Fixture git repos: `D=$(mktemp -d "$S/fixture.XXXX")`, `git -C "$D" init -q`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit, name `-C "$D"` on every git call, and use an explicit `-c user.name=... -c user.email=...` identity. Never probe, connect to, write or control a compositor surface, service, socket, session or package manager; this round has NO desktop probe at all.

Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction (-S/-Sy/-Syu/-U/-R, no service restart); use uv tool / npx / an official binary into ~/.local/bin, or name the need in your report and continue.

No credential material, session tokens, cookies or op:// refs in any artifact. No screenshots. Never message agent://all. Yield a concise report: findings, exact commands, exit codes, absolute paths, sha256 of drafts. No prose padding."""


def prompt(name, body):
    return (GOD + "\n\nYour name: " + name + ". Your only write directory: " + WAVE_DIR
            + "/w1/" + name + "/. Scratch: /fast/scratch/hyaku/mado-r69/" + name + "/.\n" + body)


ITEMS = []

ITEMS.append(("R69ExecHarness", "executor", """Produce the production draft of `quality/counters/c1-r69-landing-controls.py` (claim C1's scored harness), starting from the feasibility prototype `.ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py` (59/59 selftest, kills R1/R2/R3 in scratch).

Draft to write: `<your dir>/draft/quality/counters/c1-r69-landing-controls.py`.

Requirements:
1. Keep the measurement body's decision call sites byte-identical where the frozen recipes target them: the two-line `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)` + continuation `and forged_credit(mr_rc, mr_marker))`, the line `mz_killed = mz_rc != 0`, and the line `subprocess.run = _no_spawn` must each occur EXACTLY ONCE (assert with `grep -cF`/`str.count` and report the counts). The frozen recipes are in the declaration; do not reformat those lines.
2. The selftest must drive the real `measure()` body with scripted children (no spawn) and must carry the paired assertions the prototype adds: a crashing M-R child (rc=2, no marker) is NOT a kill; an M-Z run whose stdout has no assertion summary is NOT a kill; the hermetic spawn guard is installed and an attempted spawn under it raises. Keep the two original scripted cases.
3. Docstring: the invocation, the contract line shape, exit map 0/1/2, and the declared limits (crash-vs-kill and summary oracle only; no claim about real children). Keep `--scratch-root` refusal of /tmp, /var/tmp, /dev/shm and symlinked roots exactly as the prototype has it.
4. Do not change the measured semantics for well-formed children: for a real run the harness must print the same evidence lines and the same verdict as the r68 harness would.

Prove in scratch (report every command and rc):
a) `python3 -I <draft> --selftest --scratch-root <scratch>/st` → rc 0 and the assertion tally.
b) Apply each frozen recipe R1/R2/R3 exactly once to a scratch copy and run `--selftest`: each must exit nonzero. Report the mutant sha256 and the failing assertion lines.
c) Apply the equivalence probe recipe `mz_killed = mz_rc != 0` -> `mz_killed = mz_rc != 0 or mz_rc is None`: it must stay green; report it as an equivalent mutant (this is why it is excluded from the frozen set).
d) `python3 -m py_compile <draft>` and `python3 -I <draft> --help`."""))

ITEMS.append(("R69ExecRecipeCounter", "executor", """Produce the production draft of `quality/counters/c1-r69-paired-recipes.py` (claim C1's counting command).

Draft: `<your dir>/draft/quality/counters/c1-r69-paired-recipes.py`.

Frozen contract (from the declaration; the code, the printed line and the declaration must be the same sentence):
- CLI: `--repo . --rev REV --base-rev BASE --scratch-root DIR`, plus `--selftest --scratch-root DIR`.
- Extract `quality/counters/c1-r69-landing-controls.py` at `--rev` into the scratch tree WITH a scrubbed git env (`GIT_OPTIONAL_LOCKS=0`, `GIT_NO_REPLACE_OBJECTS=1`, every inherited GIT_* dropped) so a planted replacement cannot forge the extracted bytes.
- Run the extracted harness `--selftest --scratch-root <scratch>/st`; `selftest=<rc>`.
- Apply each frozen recipe R1/R2/R3 exactly once (assert occurrence == 1 before mutating; otherwise `applicable=no` and the recipe is never counted killed). A mutant is killed iff its own `--selftest` exits nonzero.
- Base leg: extract `quality/counters/c1-r68-landing-controls.py` at `--base-rev`, apply the same three recipes, and count how many are killed there (`base=<m>/3`). The r68 harness must survive all three.
- Contract line (exact, one line, printed last):
  `MADO_R69_PAIRED_RECIPES: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>`
- Exit 0 iff `selftest == 0` and `killed == 3` and `applied == 3` and `base == 0`; 1 otherwise; 2 on setup/usage error. Emit evidence lines per extraction, recipe, mutant (with sha256) and base mutant.
- Hermetic `--selftest`: it must drive the real decision body with scripted children (patch the module-level `run`), assert it spawns nothing, refuse /tmp-family and symlinked scratch roots, assert the contract line via `fullmatch`, and assert the four verdict conditions negatively (killed<3, applied<3, base>0, selftest!=0 each print TARGET_MISSED). No spawns at all.

Prove in scratch (report commands, rc and exact lines):
a) `--selftest` rc 0 with the assertion tally.
b) At the lane base rev `04093b83f73a841117d3b31dbb2a6063f4f2a454` the frozen command must print `selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED` rc 1 (the candidate harness does not exist there). Report the exact line.
c) Build a scratch fixture repo (`git init` inside your scratch, explicit identity) that mirrors the lane's `quality/counters/` at base plus your draft harness, commit it, and run the frozen command with `--rev <fixture HEAD> --base-rev 04093b83…` against the fixture: expect `killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0. The fixture must NOT be the lane.
d) Show the counter cannot be gamed: delete one recipe's text in a scratch copy of the harness (or flip `mz_killed` line) and show `applicable=no` / `killed<3` → TARGET_MISSED, rc 1."""))

ITEMS.append(("R69ExecDominance", "executor", """Produce the production draft of `quality/counters/c2-r69-guard-dominance.py` (claim C2's counting command), starting from `.ufo/waves/round-69/proto/c2-classify.proto.py` (`classify` already reads population=20 readers=13 guarded=13 unguarded=0 at the base rev and 11/11 on the frozen cases).

Draft: `<your dir>/draft/quality/counters/c2-r69-guard-dominance.py`.

Frozen contract:
- CLI: `--repo . --rev REV --base-rev BASE --controls .ufo/waves/round-69/controls/c2-controls-r69.json --scratch-root DIR`, plus `--selftest --scratch-root DIR`.
- Population: tracked `quality/check-[^/]+\.py` at `--rev` read through a scrubbed git env. Reader: git token + one of the frozen object-read verbs (same rule as r68). Guarded: key position only, plus the three dominance flows (inline env=, env-named name bound to a guarded mapping or a local producer and used at the call with no intervening unguarded rebinding, one-hop argument to a local function whose env-named parameter reaches the call), literal-false branches excluded — exactly as the declaration's C2 § says.
- Controls: the frozen control file must parse, must carry exactly 11 cases, and its sha256 must equal `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`; otherwise setup error rc 2. Score a case correct only when reader and guard both match.
- Base leg: extract `quality/counters/c2-r68-reader-guard.py` at `--base-rev` into scratch and score the same frozen cases with its `classify` (`base_controls=<m>/11`); it must score 7/11 on this set.
- Contract line (exact):
  `MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 controls=<n>/11 base_controls=<m>/11 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>`
- Exit 0 iff population==20, readers==13, guarded==13, unguarded==0, controls==11, base_controls==7; 1 otherwise; 2 on setup/usage error.
- Hermetic `--selftest`: 11 control cases plus the negative verdict conditions (population 19, readers 12, unguarded 1, controls 10/11, base_controls 11), contract `fullmatch`, CLI parse of the frozen argv, scratch-root refusals, and a check that `classify` on the four rejected shapes (`value-position-only`, `dead-branch-only`, `uncalled-helper`, `overwritten-env`) is `(True, False)` while the accepted shapes stay `(True, True)`. No spawns.

Prove in scratch (report commands, rc and lines):
a) `--selftest` rc 0 with the tally.
b) Frozen command at the lane base rev: the counter does not exist there → report what you actually get (a missing-file/setup error is the honest before state; record the rc and text).
c) Scratch fixture repo (git init inside scratch, explicit identity) mirroring the lane's `quality/check-*.py` set at base plus your draft counter, committed: the frozen command must print `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11 verdict=TARGET_MET` rc 0.
d) Populate a per-file table at the base rev for every one of the 20 files (`file reader=… guard=…`), so the L1 can commit it as the census receipt."""))

ITEMS.append(("R69ExecCadence", "executor", """Harm-watch and publication-cadence battery for round 69 (read-only; no production draft).

Work items (each with its exact command, rc and last lines into `<your dir>/cadence-r69.txt`):
1. `python3 quality/check-axis-scores.py --repo . --rev 04093b83f73a841117d3b31dbb2a6063f4f2a454` — report rc, the `checked=/mismatched=` line, and whether the round-68 publication is stale against the base revision (the round-68 plan item 3 said the publication cadence must ride the round that changes an instrument; say which rows, if any, would change and why).
2. `bash quality/landing-counters.sh --repo . --rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 --round 68 --scratch-root <scratch>/landing` — report `MADO_LANDING_COUNTERS` line and every leg rc.
3. `bash tools/mado-verify.sh --selftest` — report the `MADO_SELFTEST: n/n` line and rc.
4. Selftests of the instruments this round touches or must not harm: `quality/counters/c1-r68-selfmutants.py --selftest`, `quality/counters/c1-r68-landing-controls.py --selftest`, `quality/counters/c2-r68-reader-guard.py --selftest`, `quality/check-wave-done.py --selftest`, `quality/check-tool-ledger.py --selftest`, `tools/mado-receipt-citecheck.py --selftest` (pass `--scratch-root` where the tool requires one; report unsupported-selftest honestly).
5. Criterion 107 anchor cover on the round-68 entry: run `quality/check-anchor-cover.py --repo . --rev 04093b83… --entry corpus/knowledge/gate-git-read-guards-r68.md --work <scratch>/anchor` and report the `entries=`/`rows=`/`miss=`/verdict line.
6. `python3 quality/check-evidence-pointers.py`, `quality/check-landed-contract.py` and `quality/check-deliverables.py` at the base revision with the arguments their docstrings advertise (read the docstring; do not guess). Report rc and the contract line of each.

Deliver one file (`cadence-r69.txt`) plus a short summary: which legs are green, which are red for reasons that predate this round, and one line naming what the L1 must re-run at the measured content. Do not fix anything.""" ))

ITEMS.append(("R69ScribeEntry", "scribe", """Draft the claim-C2 knowledge entry at `<your dir>/draft/corpus/knowledge/gate-guard-dominance-r69.md`.

Read first: `corpus/knowledge/gate-git-read-guards-r68.md` (the predecessor entry — copy its section grammar: header, scope, tables, a Limits section, a Gate/source line), `corpus/QUALITY.md` criterion 107 (anchor cover: every cited id must carry a locator), and the frozen declaration's C2 §.

Content (evidence only from committed bytes and receipts; invent nothing):
1. What the round-68 reader census got wrong: the four accepted-but-not-guards constructions, with the measured verdicts in `.ufo/waves/round-69/control-baseline-r69.txt` (r68 `7/11`).
2. The key-position rule and the three dominance flows (inline env=; env-named binding or local producer used at the git call with no intervening unguarded rebinding; one-hop argument to a local function whose env-named parameter reaches the call), literal-false branches excluded.
3. The eleven frozen cases in a table (name, reader, guard, what it pins).
4. The population boundary: the 20 `quality/check-*.py` files, 13 readers, 13 guarded at the base revision; what stays outside (r67's wider lexical set, non-`check-` instruments, shell scripts).
5. Limits: single module, one hop, no alias/attribute/container flow, no path-sensitivity beyond literal-false, value-not-interpreted (`GIT_NO_REPLACE_OBJECTS=0` also disables), no object authenticity, no protection against a repository already rewritten.
6. The sourced ground: row S438 (`git v2.56.0 Documentation/git.adoc`), quoting the two located quotes from your own fetch — you must fetch the file yourself and paste the sha256 and byte counts you measured.

Write the entry with a `source:` line citing S438 (and any held row you actually use), and make sure every `S###` mention carries a locator that `quality/check-anchor-cover.py` accepts (read the check's docstring for the accepted forms). Report the `wc -l`, the sha256, the ids you cite, and the check-107 command you would run (do not run it against the lane — your draft is not committed)."""))

ITEMS.append(("R69ScribeRowLesson", "scribe", """Draft three artifacts:

A) `<your dir>/draft/corpus/SOURCES-row.txt` — one registry row for **S438**, 11 cells, single line,
`| S438 | <title> — <canonical URL> | docs | A | <why it grounds this round> | <anchor + quote list, tag-pinned, fetched date, sha256, byte count> | "<the located quote, <=25 words>" | ... | mined | 2026-11-03 | on-release | corpus/knowledge/gate-guard-dominance-r69.md, corpus/lessons/round-69.md |`.
Fetch https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc yourself, three times, compare sha256, and use YOUR measured values. No cell may contain a literal or escaped `|` (rewrite any anchor that would). The row must parse as 11 cells; prove it with a one-liner and report the cell count.

B) `<your dir>/draft/corpus/lessons/round-69.md` — the round lesson. Required sections: `## Outcome and boundaries` (both claims, one paragraph each, with the frozen die rolls), `## Mistakes` (a markdown table), `## Gate` (the new source row, its URL, access date and a <=25-word located quote; at least one ADMIT and one REJECT with the reason and flip condition).
Mistakes to mine (do not soften):
- **M69-1 equivalent-mutant misclassification.** Round 68's reviewer (`RevC1` row L) recorded `mz_killed = mz_rc != 0` -> `mz_killed = mz_rc != 0 or mz_rc is None` as a credit widening. It is an equivalent mutant: the text sits inside `try:` after `mz_rc = r.returncode` (`quality/counters/c1-r68-landing-controls.py:435,439`), so `mz_rc` is an int there. Evidence: `.ufo/waves/round-69/control-baseline-r69.txt` § L probe (mutant keeps a green 59/59 selftest). captured-by: `none` (r28's mutation-testing rule says equivalent mutants bound the denominator; no QUALITY criterion required a recipe to change a printed observable). Fix: every frozen recipe must change a scripted case's printed line — state the failure it can already show.
- **M69-2 value-position key accepted.** The r68 classifier counts `{"LABEL": "GIT_NO_REPLACE_OBJECTS"}` as a guard (measured `7/11`). captured-by: `none`. Fix: key-position rule with the frozen four-case control set; the red state is the r68 `7/11` receipt.
Use the declaration's evidence pointers; do not invent new measurements.

C) `<your dir>/draft/corpus/QUALITY-addendum.md` — one numbered criterion (**111**) in the same grammar as criteria 108-110: a normative sentence, a "Shown able to fail" clause with a real red state and its receipt path, and a Limits clause. Base it on M69-1/M69-2 (a frozen recipe must change a printed observable; a guard mention is not a guard unless it is a key that reaches the read)."""))

ITEMS.append(("R69ScoutSources", "scout", """Independent source opening and registry reconnaissance for the round's sourced claim (C2).

1. Fetch https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc THREE times into your scratch, compare sha256 byte-identity, and report the byte count, the sha256 and the HTTP layer (curl's exit code and response code).
2. Locate and quote (<=25 words each) the two passages the claim rests on: the `--no-replace-objects` option text (the "equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable" sentence) and the `GIT_NO_REPLACE_OBJECTS` environment-variable entry ("setting and exporting ... ignore replacement refs"). Report exact line numbers, the 1-based line of each quote, and the surrounding 3 lines.
3. Registry reconnaissance at the lane's base revision `04093b83f73a841117d3b31dbb2a6063f4f2a454`: run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` and report rc plus the `mado ...` summary line; count data rows with the census's 0-3-leading-space rule (`grep -cE '^ {0,3}\\| *S[0-9]' corpus/SOURCES.md`); list the highest S-id and any id collision the staged shokuknow set would produce (run the declaration's collision command; the lane adopts nothing, so report `collisions=0` with the exact commands and outputs).
4. Check the registry for a duplicate URL: is `raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc` already a row? Report the row id if yes (then S438 is a duplicate and the claim's source must be re-pointed — say so).
5. Reject at least one candidate source with a located reason: try `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/ast.rst` (or another you judge) and say whether it can ground the dominance predicate or is generic/lane-external (a Python AST reference does not document git environment semantics; report what you actually read, with its sha256, before rejecting).
Deliver a receipt JSON (`sources-r69.json`) with url, sha256, bytes, http rc, quote lines, and your admit/reject verdicts, plus a short report. Read-only throughout.""" ))

ITEMS.append(("R69ConnSiblings", "connector", """Cross-instrument overlap scan (read-only; no drafts of production files).

Map where the round-69 ground already appears in the lane and name what the new predicate duplicates, contradicts or leaves stale. Concretely:
1. The guard token `GIT_NO_REPLACE_OBJECTS` across the tree (`grep -rn`, excluding `.git` and `.jj`): which files construct it, which only mention it, and which constructions the r69 dominance rule would classify differently from the r68 rule. Name the file:line and the rule that changes.
2. The three other instruments that read git objects outside the `quality/check-*.py` population: `quality/landing-counters.sh`, `quality/counters/c3-r56-used-by.py`, `tools/mado-receipt-citecheck.py`, and the r65 landing instrument's extracted children. For each: does it carry the guard, and would the dominance rule pass it? (Do not run them; read the bytes.)
3. Shared housekeeping between C1 and C2: which files both claims touch, which selftest helpers both would duplicate, and whether one counter's scratch tree can collide with the other's (`--scratch-root` subdirectory names). Name every collision risk with file:line.
4. The r68 tools this round supersedes: `quality/counters/c1-r68-selfmutants.py`, `c1-r68-landing-controls.py`, `c2-r68-reader-guard.py`. Which still work, which become misleading, and which need a supersession note in the round lesson (no compatibility alias may be added).
5. Sibling-lane overlap: does any other lane's instrument (`/home/vgpnk/Projects/shokunin/*-shokunin/quality` or `tools`) implement a guard-dominance or recipe-hardening rule? Read only; report path:line and whether it is the same craft or a contested scope (adjacency duty: report, never absorb).
Report a table (ground, lane path:line, r69 rule verdict, action for the L1) and a one-paragraph adjacency verdict.""" ))

ITEMS.append(("R69RevC1", "reviewer", """Adversarial review of claim C1 (calibration): the paired-recipe hardening. Attack it; do not build it.

Read the frozen declaration, the baseline receipt and `.ufo/waves/round-69/proto/c1-r69-landing-controls.proto.py`; if an executor draft exists under `.ufo/waves/round-69/w1/R69ExecHarness/draft/` or `R69ExecRecipeCounter/draft/`, attack that too and say which bytes you attacked (sha256).

Attack list (each with command, rc and exact output):
1. Re-derive the do-nothing control: apply R1/R2/R3 to `quality/counters/c1-r68-landing-controls.py` at the base rev in scratch; each must survive (rc 0). Then apply them to the r69 prototype: each must die. Report the kill table.
2. Occurrence counts: does each recipe text occur exactly once in the r68 harness, the prototype and any draft? Report the counts and what a second occurrence would do to the claim.
3. Kill-rule attack: can a mutant be killed for a reason unrelated to the recipe (e.g. an empty/truncated file, a syntax error that is counted as "killed")? Does the counter assert the mutant still compiles/parses before crediting a kill? Report the code path.
4. Denominator attack: can the counter report `killed=3/3` while one recipe was inapplicable (`applied<3`)? Can it report TARGET_MET with `base>0`? Read the verdict conditions and prove with a scratch fixture if the code allows it.
5. Predicate-literal binding: compare the declaration's frozen line and the r68 planned successor sentence with the counter's `CONTRACT_RE`/printed line character-for-character (the round-67 routed defect class: a frozen sentence that does not describe the delivered observable). Name every mismatch.
6. Weakening check: does the harness's new selftest change what the *real* measurement does for well-formed children? Diff the measurement body against the r68 harness and report every behavioural difference; separate "selftest only" from "measurement".
7. The equivalence finding: confirm or refute that `mz_killed = mz_rc != 0 or mz_rc is None` is an equivalent mutant, with the code line that proves it.
Deliver a verdict `C1 predicate sound as bounded` or `unsound` with findings numbered by severity, and a list of residual limits the report must disclose.""" ))

ITEMS.append(("R69RevC2", "reviewer", """Adversarial review of claim C2 (operability): the key-position + dominance guard census. Attack it; do not build it.

Read the frozen declaration's C2 §, the frozen controls JSON (sha256 must be `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`), the baseline receipt, and `.ufo/waves/round-69/proto/c2-classify.proto.py`; if `.ufo/waves/round-69/w1/R69ExecDominance/draft/` exists, attack that too (name the sha256 you attacked).

Attack list (each with the exact source you fed, the counter's verdict and a reproduction command):
1. Build at least eight NEW attack cases beyond the frozen eleven: filtered-dict shape (`env = {k: v for k, v in os.environ.items() if k != "GIT_"}` then a conditional guard), attribute-carried env (`self.env[KEY] = "1"`), alias (`e = env` then guard on `e`), guard constructed after the reader call, guard inside `try/except` whose except path uses another env, nested-function closure capturing the guard, `**{KEY: "1"}` splat, and a two-module producer. For each: reader/guard verdict, and whether it is a true positive, false positive or false negative against the declaration's stated limits.
2. Population verification: run the census at the base rev and report the per-file table for all 20 `quality/check-*.py` files; confirm 13 readers / 13 guarded. Flag any file whose guard is accepted only by the one-hop argument or producer flow (those are the fragile ones) and say what would break them.
3. The four rejected shapes: prove `value-position-only`, `dead-branch-only`, `uncalled-helper`, `overwritten-env` are `(True, False)` under the prototype while the r68 classifier says `(True, True)`; report the r68 score 7/11 from the baseline receipt as the red state.
4. Denominator/verdict attack: can the counter print TARGET_MET with a truncated control file, a renamed case, a `base_controls` of 11, or a population of 19? Read the intended verdict conditions in the declaration and state what the code must assert; flag any missing assertion as a blocker.
5. Behaviour-identity hazard: the twelve gates were repaired in round 68 to construct the guard; does the dominance rule require any production change to them? If yes, name the file:line and the minimal edit; if no, say so with the per-file table.
Deliver a verdict `C2 predicate sound as bounded` or `unsound`, findings by severity, and the residual limits the report must disclose.""" ))

ITEMS.append(("R69CriticClaims", "critic", """Falsify both frozen claims without building them (read the declaration, the baseline receipt and the prototypes first).

1. Do-nothing control reachability: re-run the base legs. C1 — the r68 harness survives all three recipes (0/3). C2 — the r68 classifier scores 7/11 on the frozen cases. If either target is reachable without the claimed work, say so with the command.
2. Predicate-literal binding: compare each frozen sentence (C1's contract line and recipe texts; C2's population/key-position/dominance clauses and contract line) character-for-character with the printed labels in the prototypes and with the declaration. Name every mismatch.
3. Causal separability: prove each claim can land and be measured without the other (files, commands, scratch, no shared artifact except the wave and lesson).
4. Axis attribution: is C1 calibration and C2 operability? Name any misattribution and the surface actually changed. Check the declaration's axis-posture numbers against `SCORECARD.md` § Saturation (N=3) and the round-68 measured content.
5. No-harm: enumerate what changes (two new instruments, one new harness, one knowledge entry, one SOURCES row, QUALITY/LESSON/LOG edits) and every caller that could break; `grep -rn` the lane for invocations of the r68 instruments and say which round processes would notice.
6. Claim sizing: no universal clauses; both targets are finite denominators; kill rules stated before data. Flag any all/every/complete language and any after-the-fact narrowing risk.
7. Chronology: from git log and file mtimes, is the freeze commit `789a87f1a667b43dd759222a2f048bf8f75b43ce` before the wave `.ready` file and before any candidate measurement? Cite commits and times.
8. Sourcing: does C2 actually rest on the S438 row (git.adoc), and is the quoted fact sufficient to ground the dominance rule? Say what it does NOT ground.
9. The equivalent-mutant exclusion: is excluding RevC1's recipe L correct under r28's mutation-testing rule, or is it a denominator narrowed after the fact? Argue both ways and give a verdict.
Report blockers B1..Bn with file:line and a reproduction command; no prose verdicts without evidence.""" ))

ITEMS.append(("R69MutBattery", "mutation-tester", """Independent mutation testing of the two new counters (scratch only; never edit lane files).

Use the prototypes in `.ufo/waves/round-69/proto/` and, when present, the executor drafts under `.ufo/waves/round-69/w1/*/draft/`.

C1 counter (`c1-r69-paired-recipes.py`) — at least five single-point mutants of the *counter*: (a) skip the base-rev leg; (b) count `applicable=no` as killed; (c) count a mutant whose selftest rc is 0 as killed; (d) accept an unmutated selftest rc != 0 as green; (e) drop `applied` from the verdict or the printed line. For each: does the counter's own `--selftest` kill it? Then, if the mutant counter still runs, record whether its printed contract line/exit changes on a known-good scratch fixture.

C2 counter (`c2-r69-guard-dominance.py`) — at least six mutants: (a) guard accepted anywhere in the env mapping (value position); (b) dominance clause dropped (any construction counts); (c) literal-false branch exclusion dropped; (d) population regex widened to every `quality/*.py`; (e) `unguarded` computed as 0 unconditionally; (f) controls or `base_controls` ignored in the verdict. For each: selftest killed/survived, plus the printed line and rc against a scratch repo with known guards.

Also test the harness side: run the three frozen recipes plus the equivalence probe against the prototype and any draft, and confirm `3/3` killed / `1/1` survivor.

Report a kill matrix (mutant, selftest killed?, printed-line effect, survivor iff), every survivor as a named residual with its diff digest and a one-line flip condition, and a scratch-cleanup receipt. No universal fault-coverage claim.""" ))


def main():
    doc = {"wave": "w1", "reportDir": ".ufo/waves/round-69/w1", "context": CONTEXT,
           "items": [{"name": n, "role": r, "prompt": prompt(n, b)} for n, r, b in ITEMS]}
    path = os.path.join(WAVE_DIR, "w1-spec.json")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(doc, indent=1) + "\n")
    roles = {}
    for _, r, _ in ITEMS:
        roles[r] = roles.get(r, 0) + 1
    attack = sum(v for k, v in roles.items() if k in ("reviewer", "critic", "mutation-tester", "labrat"))
    print("items", len(ITEMS), "chars", sum(len(i["prompt"]) for i in doc["items"]),
          "roles", roles, "attack", attack, "share", round(attack / len(ITEMS), 3))


if __name__ == "__main__":
    main()

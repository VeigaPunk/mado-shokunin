#!/usr/bin/env python3
"""Build the round-70 wave spec (ONE v1 wave, 14 seats). Deterministic; no network, no host writes."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE_DIR = LANE + "/.ufo/waves/round-70"
DECL = WAVE_DIR + "/claims-declaration-r70.md"
FREEZE = "bc18399b409a6390a6c6e8831bf9ad2dacbbf189"
INSTR = "5144a6b5f43225d8021a469f4d24c19558026b9e"
BASE = "b37a5aec4ea03f2223d8e09dd5d386d055c24179"

GOD = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = GOD + """

Round mado 70, ONE v1 wave (14 seats). Axes: calibration (C1) and operability (C2). The L1 holds the planner seat (the validator rejects a planner role); no planner is dispatched.

Read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/claims-declaration-r70.md FIRST. Claims, predicates, control set, scenario texts and targets are FROZEN at """ + FREEZE + """ (base """ + BASE + """). Never re-scope, never narrow a target after seeing data, never invent a different counter, never edit the declaration, the control JSON or the baseline receipt.

Lane repo (absolute): /home/vgpnk/Projects/shokunin/mado-shokunin. The scored instruments are committed at """ + INSTR + """:
  quality/counters/c1-r70-landing-controls.py   (successor harness; M-Z credit requires a parsed failed-assertion summary)
  quality/counters/c1-r70-real-children.py      (C1 counting command; real bash fixture lane, three modes)
  quality/counters/c2-r70-carriers.py           (C2 counting command; round-69 rule + four carrier shapes)
Frozen evidence: .ufo/waves/round-70/controls/c2-controls-r70.json (17 cases), .ufo/waves/round-70/control-baseline-r70.txt, .ufo/waves/round-70/proto/fixture-lane.tmpl.

Write ONLY your own seat directory /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/w1/<your-name>/ — drafts of production files go under draft/<repo-relative path> inside it; the L1 integrates them and you never write a production path. Reading sibling seat dirs is allowed. Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mado-shokunin — write it at /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>.

Scratch: /fast/scratch/hyaku/mado-r70/<your-name>/ (mkdir -p first) with delete-on-exit (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree(dir, ignore_errors=True)` in Python). Never rely on an inherited TMPDIR, never write /tmp or /var/tmp. Report the scratch removed before you yield.

Never commit, push, stage, stash, checkout, switch, reset or run any mutating git/jj command in the lane, the fleet repo /home/vgpnk/Projects/shokunin, or any sibling lane. Never write the fleet repo, another lane, MANIFEST.json, .ufo/state, .scratch, or operator config. Fixture git repos: `D=$(mktemp -d "$S/fixture.XXXX")`, `git -C "$D" init -q`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit, name `-C "$D"` on every git call, and use an explicit `-c user.name=... -c user.email=...` identity. Never probe, connect to, write or control a compositor surface, service, socket, session or package manager; this round has NO desktop probe at all.

Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction (-S/-Sy/-Syu/-U/-R, no service restart); use uv tool / npx / an official binary into ~/.local/bin, or name the need in your report and continue.

No credential material, session tokens, cookies or op:// refs in any artifact. No screenshots. Never message agent://all. Yield a concise report: findings, exact commands, exit codes, absolute paths, sha256 of drafts. No prose padding."""


def prompt(name, body):
    return (GOD + "\n\nYour name: " + name + ". Your only write directory: " + WAVE_DIR
            + "/w1/" + name + "/. Scratch: /fast/scratch/hyaku/mado-r70/" + name + "/.\n" + body)


ITEMS = []

ITEMS.append(("R70ExecC1Real", "executor", """Drive claim C1's counting command end to end and report what actually happens (do not edit the committed instruments).

1. Run its selftest: `python3 -I quality/counters/c1-r70-real-children.py --selftest --scratch-root <scratch>/st` -> rc and the `MADO_R70_REAL_CHILDREN_SELFTEST: n/n` line.
2. Run the frozen counting command against the lane at """ + INSTR + """ and at the base """ + BASE + """:
   `python3 -I quality/counters/c1-r70-real-children.py --repo . --rev """ + INSTR + """ --base-rev """ + BASE + """ --scratch-root <scratch>/m` (and the same with --rev """ + BASE + """).
   Report the whole output verbatim: the `MADO_R70_FIXTURE` lines, the `MADO_R70_SCENARIO` lines, the contract line, and the rc. If it prints something other than what the declaration's C1 frozen sentence says, that is a finding, not something to fix.
3. Re-derive the fixture independently: extract the lane template the counter embeds (`LANE_TEMPLATE`) with `python3 -c 'import runpy; print(runpy.run_path("quality/counters/c1-r70-real-children.py")["LANE_TEMPLATE"])'`, write each of the three modes to a fresh scratch git repo yourself, and run `quality/counters/c1-r70-landing-controls.py --repo <your fixture> --rev <mode-rev> --scratch-root <dir>` for each. Report the three `MADO_R70_LANDING_CONTROLS: … mz=…` lines. Then run the frozen round-69 harness (`quality/counters/c1-r69-landing-controls.py`) on the same three and report its three `mz=` values.
4. Adversarial checks, each with command and rc: (a) point --repo at a scratch copy of the lane at """ + INSTR + """ where `quality/counters/c1-r70-landing-controls.py` is deleted -> what does the counter print and exit? (b) replace the r70 harness with a 3-line script that prints `MADO_R70_LANDING_CONTROLS: … mz=fail …` every run -> does the counter refuse to credit? (c) replace it with one that prints `mz=pass` every run -> does `crash`/`garbage` fail it? (d) a fixture whose lane has no `[ "$citations" -gt 0 ] && ` clause at all -> what happens (`recipe=none`) and does the counter still score?
5. Confirm the counter never writes outside its scratch root: list the tree before/after and diff the file lists.
Deliver a findings file with every command, rc, and the exact lines; name any divergence from the frozen sentence.""" ))

ITEMS.append(("R70ExecHarness", "executor", """Audit the successor harness `quality/counters/c1-r70-landing-controls.py` at """ + INSTR + """ against the frozen round-69 harness, and report the exact behavioural delta.

1. Diff the two files (`diff -u quality/counters/c1-r69-landing-controls.py quality/counters/c1-r70-landing-controls.py`) and classify every hunk: marker rename only / docstring only / selftest only / measurement behaviour. Name every measurement-body difference.
2. Run both selftests: `--selftest --scratch-root <scratch>/a` and `<scratch>/b`; report the tallies and rc.
3. On the feasibility fixture lane (`.ufo/waves/round-70/proto/fixture-lane.tmpl`, mode genuine) both harnesses must credit the kill; on a mode you build yourself where the mutated lane exits 2 with no summary, the r70 harness must NOT credit and the r69 harness must. Show the two contract lines.
4. Apply the frozen round-69 recipes R1/R2/R3 (texts in `quality/counters/c1-r69-paired-recipes.py`) to a scratch copy of the r70 harness and report, per recipe: occurrence count, `bash -n`/`py_compile` result, selftest rc. R2 (`mz_killed = mz_rc != 0`) must now be **absent** — report that as an expected supersession, not a defect, and say what the r69 counter will do if run against a rev where only the r70 harness exists.
5. Run the frozen round-69 counter at """ + INSTR + """: `python3 -I quality/counters/c1-r69-paired-recipes.py --repo . --rev """ + INSTR + """ --base-rev """ + BASE + """ --scratch-root <scratch>/r69`. Report the contract line and rc — the r69 harness file must be byte-identical to the base, so this must stay TARGET_MET; if it does not, that is the round's biggest finding.
6. Check the new predicate's fail-closed direction: construct an input where the child's summary is `0/0 assertions passed` and one where it is `1/2` with rc 0. Report `summary_shows_failure` on each and the resulting `mz=` line. State the residual hazard honestly (a mutant that fails an assertion but exits 0 is still credited? or not?).
Deliver findings with commands, rc and exact lines. Do not edit the harness.""" ))

ITEMS.append(("R70ExecC2Rule", "executor", """Drive claim C2's counting command and stress its classifier (do not edit the committed instrument).

1. Selftest: `python3 -I quality/counters/c2-r70-carriers.py --selftest --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root <scratch>/st` -> rc and tally.
2. Frozen command at """ + INSTR + """ and at """ + BASE + """:
   `python3 -I quality/counters/c2-r70-carriers.py --repo . --rev """ + INSTR + """ --base-rev """ + BASE + """ --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root <scratch>/m`. Report every `MADO_R70_READER` line (the 20-file census), every `MADO_R70_CONTROL` line, the `MADO_R70_HELD_CONTROLS` line, and the contract line + rc. The same command at the base rev must show the counter absent (record the honest before state).
3. Re-derive the base leg by hand: `python3 -c` load `quality/counters/c2-r69-guard-dominance.py` at the base rev and score the 17 frozen cases with its `classify`; report per-case verdicts and the 13/17 score.
4. Write at least SIX new probe sources beyond the frozen 17 and report each verdict against the declaration's stated rule and limits: (a) two-hop alias (`a = env; b = a; b[KEY] = "1"`), (b) alias guarded but env-named name REBOUND after the alias (`env = {...}; alias = env; alias[KEY]="1"; env = {...}; run(env=env)`), (c) attribute guarded, a *different* attribute passed (`self.env` guarded, `env=self.other`), (d) splat of a module mapping that does NOT carry the key, (e) constant key whose module constant is rebound later (`KEY = "GIT_NO_REPLACE_OBJECTS"; KEY = "OTHER"`), (f) `dict(**GUARD)` call form with a guarded module mapping, (g) a guarded module mapping expanded by `**` in a `dict(...)` call. For each: expected under the declared rule, observed, and whether the difference is a false positive, a false negative, or inside the declared limits.
5. Verify the population is unchanged: confirm the 20 tracked `quality/check-*.py` at """ + INSTR + """ are the same 20 as at """ + BASE + """ (`git ls-tree` both, diff), and that 13 readers / 13 guarded holds.
Deliver a findings file with commands, rc, per-case tables and the final contract line.""" ))

ITEMS.append(("R70ExecCadence", "executor", """Harm-watch and publication-cadence battery for round 70 (read-only; no production draft).

Work items (each with its exact command, rc and last lines into `<your dir>/cadence-r70.txt`):
1. `bash tools/mado-verify.sh --selftest` — report the `MADO_SELFTEST: n/n` line and rc.
2. `bash quality/landing-counters.sh --repo . --rev """ + INSTR + """ --round 69 --scratch-root <scratch>/landing` — report the `MADO_LANDING_COUNTERS:` line and every leg rc.
3. `python3 quality/check-axis-scores.py --repo . --rev """ + INSTR + """` — report rc, the `checked=/mismatched=` line, and whether the published table is stale against the new instruments.
4. Selftests of every instrument this round touches or must not harm: `quality/counters/c1-r69-paired-recipes.py --selftest`, `quality/counters/c1-r69-landing-controls.py --selftest`, `quality/counters/c2-r69-guard-dominance.py --selftest --controls .ufo/waves/round-69/controls/c2-controls-r69.json`, `quality/counters/c1-r70-landing-controls.py --selftest`, `quality/counters/c1-r70-real-children.py --selftest`, `quality/counters/c2-r70-carriers.py --selftest --controls .ufo/waves/round-70/controls/c2-controls-r70.json`, `quality/check-wave-done.py --selftest`, `quality/check-tool-ledger.py --selftest`, `tools/mado-receipt-citecheck.py --selftest`. Pass `--scratch-root <scratch>/...` where required; report honestly if a tool has no selftest.
5. Anchor cover on the newest entry: `python3 quality/check-anchor-cover.py --repo . --rev """ + INSTR + """ --entry corpus/knowledge/gate-guard-dominance-r69.md --work <scratch>/anchor` — report the `entries=/rows=/miss=` line and verdict.
6. `python3 quality/check-evidence-pointers.py`, `quality/check-landed-contract.py`, `quality/check-deliverables.py` and `python3 quality/landing-counters.sh`-adjacent `quality/check-index.py` at """ + INSTR + """ with the arguments their docstrings advertise (read the docstring; do not guess). Report rc and the contract line of each.
7. Scope check: `git status --porcelain` in the lane must be empty (the L1 commits; you must not create lane files outside your seat dir), and `find . -newer rg`-style confirmation that no file outside your seat dir changed during your run — report how you checked.

Deliver one file (`cadence-r70.txt`) plus a summary: which legs are green, which are red for reasons that predate this round, and one line naming what the L1 must re-run at the final measured content. Do not fix anything.""" ))

ITEMS.append(("R70ScribeEntryC1", "scribe", """Draft the claim-C1 knowledge entry at `<your dir>/draft/corpus/knowledge/landing-kill-credit-real-children-r70.md`.

Read first: `corpus/knowledge/gate-guard-dominance-r69.md` (the predecessor entry — copy its section grammar: header, scope, tables, a Limits section, a Gate/source line), `corpus/QUALITY.md` criterion 111 (a frozen recipe must change a printed observable), and the frozen declaration's C1 §.

Content (evidence only from committed bytes and receipts; invent nothing):
1. What the round-69 harness credited: `mz_killed = mz_rc != 0`, and why that is wrong — a nonzero status has more than one cause; a child that crashes (no summary) or prints a garbled summary is not a failed assertion. Cite the committed line (`quality/counters/c1-r69-landing-controls.py`, the `mz_killed` assignment) and the pre-freeze receipt (`.ufo/waves/round-70/control-baseline-r70.txt` § C1: `mz=pass` on crash and garbage, `base_correct=1/3`).
2. The repaired rule: a kill requires `mz_rc != 0` AND the child's own `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary parsing with `p < n` (`quality/counters/c1-r70-landing-controls.py`, `summary_shows_failure`).
3. The real-children leg: three scenarios in a scratch git repo, each a real `bash` child; the fixture lane's zero-citation assertion is the observable (its clause is `[ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1`), and its three modes are driven by the clause's own effect. Table: mode, child rc, summary, harness `mz=`, correct.
4. What the counter cannot do: it cannot tell a correct decision from one that agrees on these three inputs; the fixture is the counter's own instrument; a harness that always denied and one that always credited are both killed by the set, but nothing wider is proven.
5. The sourced ground: CPython `Doc/library/subprocess.rst` @ `v3.14.8`, the `returncode` paragraph (a negative value is a signal death; the exit status is the child's status) — quote the located sentence you fetched yourself, with sha256 and byte count. A `source:` line must cite the row id the L1 assigns (the lesson's Gate block names it). Use the placeholder `S###` only if you cannot determine the id; state that.
Every `S###` mention must carry a locator that `quality/check-anchor-cover.py` accepts (read the check's docstring). Report wc -l, sha256, the ids you cite.""" ))

ITEMS.append(("R70ScribeEntryC2", "scribe", """Draft the claim-C2 knowledge entry at `<your dir>/draft/corpus/knowledge/guard-carrier-shapes-r70.md`.

Read first: `corpus/knowledge/gate-guard-dominance-r69.md` (predecessor grammar), `corpus/QUALITY.md` criterion 111(b), and the frozen declaration's C2 §.

Content (committed bytes and receipts only):
1. The four carriers the round-69 rule missed, each with the frozen case's source text and the measured verdict pair: `alias-carried` (alias of an env-named mapping, guard through the alias), `attribute-carried` (`self.env[KEY] = …` and `env=self.env`), `splat-carried` (module-level literal mapping carrying the key, expanded with `**`), `constant-key` (module-level string constant equal to the key used as the subscript key). Evidence: `.ufo/waves/round-70/controls/c2-controls-r70.json` and the pre-freeze receipt § C2 (`13/17` for the held rule).
2. The rule as one sentence: round-69 key position and the three dominance flows stay in force; each new carrier must still reach the `git` launch; a module-level constant counts only when the module binds it once to a literal.
3. The full 17-case table (name, reader, guard, what it pins, held or new).
4. The population boundary: the same 20 `quality/check-*.py`, 13 readers, 13 guarded; what is still outside (container/attribute flow beyond one level, `dict(**GUARD)` call form if the counter misses it, two-module producers, non-`check-` instruments, shell scripts).
5. Limits: the rule is a bounded syntactic approximation; it does not interpret the guard's value; it does not authenticate objects or protect a rewritten repository; the four shapes are named ones, not an enumeration.
6. The sourced ground: CPython `Doc/reference/expressions.rst` @ `v3.14.8` — dictionary displays (`**` unpacks a mapping into the display) and subscription assignment (`target[index] = value` stores under the evaluated key). Quote the two located sentences you fetched yourself with sha256 and byte count; a `source:` line cites the row id the L1 assigns (say `S###` if you cannot determine it). Keep every `S###` mention locator-bearing for `quality/check-anchor-cover.py`.
Report wc -l, sha256, ids cited.""" ))

ITEMS.append(("R70ScribeRowLesson", "scribe", """Draft three artifacts.

A) `<your dir>/draft/corpus/SOURCES-rows.txt` — registry rows, 11 cells each, one per line, no cell containing a literal or escaped `|`:
   - CPython `Doc/library/subprocess.rst` @ v3.14.8 (C1's ground: return-code semantics — a nonzero status has several causes, a signal death is `-N`).
   - CPython `Doc/reference/expressions.rst` @ v3.14.8 (C2's ground: dictionary displays `**` unpacking and subscription assignment).
   - A third row only if you actually open and can ground a distinct fact (e.g. CPython `Doc/library/ast.rst` for the node shapes the classifier reads) — otherwise say why you did not add one.
   Fetch each URL yourself THREE times, compare sha256 byte-identity, and use your measured byte count, sha256, access date and a <=25-word located quote with line numbers. Check the registry at the lane head first for a duplicate URL (`grep`), and if the URL already has a row say so instead of appending. Prove each row parses as 11 cells with a one-liner.

B) `<your dir>/draft/corpus/lessons/round-70.md` — the round lesson. Required sections: `## Outcome and boundaries` (both claims, one paragraph each, frozen predicates only — mark any measurement you could not run), `## Mistakes` (a markdown table: mistake | class | evidence | captured-by | fix and the failure it can now show), `## Gate` (each new source row: URL, access date, <=25-word located quote; at least one ADMIT and one REJECT with reason and flip condition).
Mistakes to mine (do not soften):
- **M70-1 the round-69 LOG bullets were inserted into two filed entries.** `corpus/lessons/round-69-verifier-spotcheck.md` defect 1: the 10-line block appears in the Round 67 entry (LOG.md:3257-3266), the Round 68 entry (3314-3323) and Round 69 (3396-3405), all from `139f4801`. captured-by: `none` — no rule said an append-only edit must be anchored to its own round heading. Fix: state the rule you would enforce, and the one-command sweep that would have caught it.
- **M70-2 a round commit was left unenumerated** (spot-check defect 2: `b9b70a09` absent from report, LOG and SCORECARD; `grep -rn b9b70a09` rc 1). captured-by: `none`. Fix: the report's Landed-changes table must be re-derivable by `git rev-list --count base..tip` equality; name the command.
- **M70-3 the round-69 freeze-order evidence was misdescribed** (spot-check defect 3: `check-freeze-order.py` requires `claims-frozen.md`/`registration.md`, neither of which this lane uses, and the r69 receipt reads `SETUP work_not_a_directory`). captured-by: `none`. Fix: name the lane's own freeze-order evidence and the command that re-derives it.
- **M70-4 the round-69 `w1-results.json` carried no settlement status** (defect 4). captured-by: `none`. Fix: the round's own results file must state settled/dead explicitly, or the report says it is inferred.
Use the declaration's and receipts' evidence pointers; invent no measurements. Say honestly which of these are fixed this round and which are reported only.

C) `<your dir>/draft/corpus/QUALITY-addendum.md` — numbered criteria continuing the file (**112** and, if warranted, **113**) in the grammar of 108–111: normative sentence, "Shown able to fail" with a real red state and receipt path, Limits clause. Base them on M70-1/M70-2 (record order: an append-only insertion must be anchored to the round whose heading it sits under; a round's commit list is complete iff `git rev-list --count` equals the enumerated rows) and, if you can ground it, on the credit rule (a kill credit requires a parsed failed assertion, not an exit status)."""))

ITEMS.append(("R70ScoutSources", "scout", """Independent source opening for both claims' sourced ground.

1. Fetch THREE times each, into your scratch, and report byte count, sha256 and curl's rc/http code:
   - https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst
   - https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst
2. Locate and quote (<=25 words) in subprocess.rst: the `Popen.returncode` paragraph's statement about nonzero/negative values (a negative value -N is a signal death) and, if present, the sentence that the exit status is the child's. Give 1-based line numbers and the surrounding 3 lines. State what this does and does NOT ground about "nonzero rc = failed assertion".
3. Locate and quote in expressions.rst: (a) the dictionary-display sentence about `**` (the operand must be a mapping and its items are unpacked into the display), (b) the assignment-statement sentence about a subscription target (the primary and the index expression are evaluated, then the item is assigned). Give line numbers and surrounding lines. State what these ground about a splat carrier and a name-valued key.
4. Registry reconnaissance at the lane head: run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` and report rc plus the summary line; count data rows with the census's 0-3-leading-space rule; list the highest S-id; check whether either URL already has a row (`grep -n` the URL) and report the row id if so.
5. Reject at least one candidate source with a located reason: try `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/ast.rst` — fetch it, say what it documents, and whether it can ground a *runtime* carrier claim or only the classifier's implementation shape; reject it with a flip condition if it cannot.
6. If a URL 404s, record it honestly and propose the nearest tag that exists (report what you tried), do not invent bytes.
Deliver `sources-r70.json` (url, sha256, bytes, http rc, quote lines, admit/reject) plus a short report. Read-only throughout.""" ))

ITEMS.append(("R70ScoutCensus", "scout", """Frontier-step reconnaissance for round 70 (read-only).

1. Run the round-start census exactly: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` -> rc and the `mado` summary line; also run it with `--file /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` if that mode exists (read `scripts/sources-census.sh --help`). Report data-row count at HEAD.
2. Registry health: list rows whose `status` is not `mined`, rows with `used-by` naming files that no longer exist (check with `git ls-tree` at HEAD), and the highest S-id. Do not fix anything.
3. shokuknow slice: read `/home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md` and `SOURCES.append.md` (read-only). Report how many staged entries exist, their titles, and whether any of them already cover the round-70 ground (kill-credit, child exit statuses, Python AST carrier shapes, guard dominance). Run the declaration's collision commands into `<your dir>/assimilation/` and report the id lists and the collision count. Adopt nothing.
4. Quarantine slice: read `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, derive the mado slice with the awk command from the round prompt (data rows only), save it and report the row count and ids. Verify what you can read-only; adopt nothing, edit nothing.
5. `considerthese/`: list the files, read the newest one, and report whether any still-unimplemented proposal bears on this round's ground (a live-tool table, a kill-credit rule, a carrier table). Quote the proposal's own line. Do not implement it.
6. Report the frontier rows in `corpus/README.md` § Frontier that this round should advance (name the row and the reason), and any row the round would leave stale.
Deliver a findings file with exact commands/outputs and a one-paragraph frontier verdict.""" ))

ITEMS.append(("R70RevC1", "reviewer", """Adversarial review of claim C1 (calibration): the real-children kill-credit repair. Attack it; do not build it.

Read the frozen declaration C1 §, `.ufo/waves/round-70/control-baseline-r70.txt`, and the committed instruments at """ + INSTR + """ (name the sha256 of each file you attacked).

Attack list (each with command, rc and exact output):
1. Re-derive the do-nothing control: run the round-69 harness on the three fixture modes (build the fixture yourself from `proto/fixture-lane.tmpl` or from the counter's `LANE_TEMPLATE`) and report its three `mz=` values; then the r70 harness. Confirm or refute `base_correct=1/3`.
2. Kill-rule attack: can a scenario be scored correct for the wrong reason? Build a harness stand-in that reads the fixture name (three different lane files) — it would score 3/3. Build a stand-in that prints `mz=fail` unless the lane text contains `SE`... — say what the counter does and does not prove about the *scored* harness's authorship. Is that a blocker under the frozen sentence, or the disclosed limit?
3. Predicate-literal binding: compare the declaration's C1 frozen sentence with `contract_line()` and `verdict_met()` character-for-character (labels, denominators, the `absent` case). Name every mismatch.
4. Denominator attack: can the counter print TARGET_MET with `correct=3` while one scenario never ran, with `base_correct` skipped, or with a truncated MODES tuple? Read the code and prove each with a scratch copy of the counter (never edit the lane file).
5. Fail-closed check: does the widening direction hold? A mutant that fails an assertion but exits 0 — what does `summary_shows_failure` + the rc condition produce, and is that the safer direction? A summary with a negative or huge number, a summary appearing twice, a summary on stderr vs stdout (the harness concatenates) — test each and report the verdict.
6. Weakening check: does the r70 harness's measurement body differ from the r69 one anywhere other than the said repair and the marker rename? List every behavioural difference; separate docstring/selftest from measurement.
7. Harm: run the round-69 counter at """ + INSTR + """ and confirm it still reports `killed=3/3 base=0/3 TARGET_MET`; if not, that is a blocker with the exact line.
Deliver a verdict `C1 predicate sound as bounded` or `unsound`, findings by severity, and the residual limits the report must disclose.""" ))

ITEMS.append(("R70RevC2", "reviewer", """Adversarial review of claim C2 (operability): the carrier rule. Attack it; do not build it.

Read the frozen declaration C2 §, the 17-case control JSON (sha256 must be `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`), the pre-freeze receipt, and `quality/counters/c2-r70-carriers.py` at """ + INSTR + """ (name its sha256).

Attack list (each with the exact source you fed, the counter's verdict and a reproduction command):
1. Build at least TEN attack sources beyond the frozen 17 and classify each with the committed counter and with the round-69 classifier: two-hop alias; alias then env rebinding; guarded attribute passed as a different attribute; attribute guarded but the object aliased (`r = self; env=r.env`); `**` splat of a non-guarded mapping; `**` splat of a guarded mapping inside a `dict()` call; constant key rebound later; constant key used in a *value* position; alias whose source is not env-named (`base = {}; a = base; a[KEY]="1"` then `env=base`); module mapping mutated after the splat. For each: expected under the declaration, observed, classification (TP/FP/FN/inside declared limits).
2. Prove the four rejected shapes and the two git-launch negatives stay at their frozen expectations under the new rule, and that no held case changed.
3. Population verification: run the counter at """ + INSTR + """ and report the 20-file table; confirm 13/13/0 (the base rev's table was produced by round 69; say whether the counts moved).
4. Denominator/verdict attack: truncated controls file, renamed case, a `base_controls=17` line, `controls=16`, population 19 — does the code refuse each? Flag any missing assertion as a blocker.
5. Held-set guard: does the counter actually assert the round-69 file's digest and the 11-case identity? Break it in a scratch *copy* of the repo (rewrite the held JSON, commit in a scratch clone) and show the counter's rc.
6. Source grounding: is expressions.rst sufficient to ground (a) the splat as a carrier and (b) a name-valued key as a key? Say what each quote does NOT ground (e.g. that Python evaluates the subscript key expression — check whether the quote you actually read says it).
Deliver a verdict `C2 predicate sound as bounded` or `unsound`, findings by severity, and the residual limits the report must disclose.""" ))

ITEMS.append(("R70CriticClaims", "critic", """Falsify both frozen claims without building them (read the declaration, the receipts, the instruments at """ + INSTR + """).

1. Do-nothing control reachability: re-run both base legs. C1 — the r69 harness on the three real-child modes (expect `mz=pass` on crash and garbage; `base_correct=1/3`). C2 — the r69 classifier on the frozen 17 (expect 13/17). If either target is reachable without the claimed work, say so with the command.
2. Predicate-literal binding: compare each frozen sentence (C1's three scenario expectations and contract line; C2's population/key-position/dominance/carrier clauses and contract line) character-for-character with the printed labels in the instruments. Name every mismatch.
3. Causal separability: prove each claim can land and be measured without the other (files, commands, scratch, no shared artifact except the wave and lesson). Check that neither counter reads the other's file.
4. Axis attribution: is C1 calibration and C2 operability? Name any misattribution and the surface actually changed. Check the declaration's axis-posture numbers against `SCORECARD.md` § Saturation (N=3) and the round-69 measured content.
5. No-harm: enumerate what changes (two new instruments, one new harness, two knowledge entries, SOURCES rows, QUALITY/LESSON/LOG/SCORECARD edits) and every caller that could break. Check the r69 frozen instruments: do they still pass at """ + INSTR + """? Name the commands.
6. Claim sizing: no universal clauses; both targets are finite denominators; kill rules stated before data. Flag any all/every/complete language and any after-the-fact narrowing risk (especially the `base_correct=1` expectation: could a legitimate repair make the base leg 0/3 or 2/3?).
7. Chronology: from git log and file mtimes, is the freeze commit `""" + FREEZE + """` before the instruments commit `""" + INSTR + """`, before this wave's `.ready`, and before any candidate measurement? Cite commits and times.
8. Sourcing: do the two claimed source rows actually ground the two rules? Say what each does NOT ground.
9. Substitution risk: could a trivially different artifact (a counter that always printed the target line, a fixture that hard-codes the answer) score either target? Say how the instruments' *measurement* (not selftest) blocks it, or disclose that it does not.
Report blockers B1..Bn with file:line and a reproduction command; no prose verdicts without evidence.""" ))

ITEMS.append(("R70MutBattery", "mutation-tester", """Independent mutation testing of the round-70 instruments (scratch only; never edit lane files).

C1 harness (`quality/counters/c1-r70-landing-controls.py`) — at least five single-point mutants: (a) `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))` -> `mz_killed = mz_rc != 0`; (b) `summary_shows_failure` -> always True; (c) `summary_shows_failure` -> always False; (d) the `p < n` condition -> `p <= n`; (e) the regex `fullmatch` -> `search`. For each: does the harness's own `--selftest` go red? Report the failing assertion line.

C1 counter (`quality/counters/c1-r70-real-children.py`) — at least four mutants: (a) `score()` -> compare against the candidate's own answer; (b) drop the base leg (`base_correct` forced to 1); (c) `verdict_met` -> `correct >= 2`; (d) `EXPECT` swapped for crash. Does its `--selftest` kill each? Then, for survivors, run the mutant counter on the real fixture and report whether the printed line changes.

C2 counter (`quality/counters/c2-r70-carriers.py`) — at least six mutants: (a) `carrier_guard` -> `return True`; (b) `carrier_guard` -> `return False`; (c) alias detector removed; (d) attribute detector removed; (e) splat detector removed; (f) constant-key detector removed; (g) `held_check` -> return 0 (guard dropped); (h) `FROZEN_BASE_CONTROLS` -> 13 not required in the verdict. For each: selftest killed/survived, plus (for survivors) the contract line and rc on a scratch fixture repo.

Also run the committed instruments normally and record the baseline lines so a survivor's effect is legible.

Report a kill matrix (mutant, selftest killed?, printed-line effect, survivor iff), every survivor as a named residual with its diff digest and a one-line flip condition, and a scratch-cleanup receipt. No universal fault-coverage claim.""" ))

ITEMS.append(("R70ConnSiblings", "connector", """Cross-instrument overlap scan (read-only; no drafts of production files).

Map where the round-70 ground already appears in the lane and name what the new rule duplicates, contradicts or leaves stale. Concretely:
1. The kill-credit decision across every instrument: `grep -rn 'rc != 0\\|returncode != 0\\|killed'` over `quality/` and `tools/`; for each hit, say whether it credits on a bare nonzero status and whether the round-70 rule (parsed failed assertion) should apply there. Name file:line and the classification.
2. The guard token and the carrier shapes across the tree (`grep -rn 'GIT_NO_REPLACE_OBJECTS'`): which files use an alias/attribute/splat/constant-key construction now that the rule counts them? Does the census's 13/13 change, and does any *new* production file become a reader? Report each with file:line.
3. Shared housekeeping between C1 and C2: which files both claims touch (only the wave and lesson?), which selftest helpers both duplicate, and whether the two counters' scratch subdirectory names can collide (`r70-c1` vs `r70-c2-carriers`). Name every collision risk with file:line.
4. The instruments this round supersedes or leaves behind: `c1-r69-landing-controls.py`, `c1-r69-paired-recipes.py`, `c2-r69-guard-dominance.py`, `c1-r68-landing-controls.py`, `c2-r68-reader-guard.py`. Which still work at """ + INSTR + """, which become misleading, and which need a supersession note in the round lesson (no compatibility alias may be added).
5. Sibling-lane overlap: does any other lane's instrument (`/home/vgpnk/Projects/shokunin/*-shokunin/quality` or `tools`) implement a kill-credit or carrier-census rule? Read only; report path:line and whether it is the same craft or a contested scope (adjacency duty: report, never absorb).
Report a table (ground, lane path:line, round-70 rule verdict, action for the L1) and a one-paragraph adjacency verdict.""" ))


def main():
    doc = {"wave": "w1", "reportDir": ".ufo/waves/round-70/w1", "context": CONTEXT,
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

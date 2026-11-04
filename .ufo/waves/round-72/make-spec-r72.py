#!/usr/bin/env python3
"""Build .ufo/waves/round-72/w1-spec.json (one v1 wave, 13 seats)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE = os.path.join(LANE, ".ufo", "waves", "round-72")
REV = "9bcb4fd5b598844f168230dc05e441721d95b272"
BASE = "976684a27e99c2508037a60eec415f550f53d70e"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + """
Round mado 72, ONE v1 wave (13 seats). Axes: C1 calibration (the landing kill credit requires
the run's own failure detail) and C2 operability (the harness outcome reads the gate's own
summary, not its exit status). The L1 holds the planner seat (the validator rejects `planner`
as a swarm role); no planner is dispatched.

Read FIRST:
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/claims-declaration-r72.md
(the frozen claims, predicates, counting commands, kill rules, targets and limits; base
`976684a27e99c2508037a60eec415f550f53d70e`, instruments `9bcb4fd5b598844f168230dc05e441721d95b272`).

Frozen receipts already committed (re-read, do not rewrite):
- measurement-c1-r72.txt / measurement-c2-r72.txt under the same dir (both TARGET_MET).
- control-baseline-c1-r72.txt (held 6/8) and control-baseline-c2-r72.txt (held 4/8).

Hard bounds, every seat:
- Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-72/w1/<your name>/.
  Never edit a committed lane file (production instruments, corpus, SKILL.md, SCORECARD.md,
  LOG.md, README, SOURCES.md); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash, no jj mutation);
  read-only git and `git show`/`ls-tree`/`rev-parse`/`status` are fine. Never write the fleet
  repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `scripts/`, `templates/`
  or MANIFEST.json.
- Never message `agent://all`; reply only to your L1 (`MadoR72`) or nothing.
- Scratch: /fast/scratch/hyaku/mado-r72/<your name>/ (create it; pass it explicitly; never use
  /tmp; delete it before you finish, after copying any receipt you cite into your own dir).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps this
  task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate) and
  recording tool/version/channel/reason in your report. ALL pacman transactions are PAUSED
  host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or report
  that you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Read-only host posture: do not probe the compositor, session, services, network services or
  ~/.config; no live-config writes; no credential material in any file.
- Every `Report:` trailer path the validator renders is relative to
  /home/vgpnk/Projects/shokunin/mado-shokunin — write it at
  /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>. End your final output with one line
  `Report: <repo-relative path>` naming the file you actually wrote, then a 3-line summary.
"""

ITEMS = [
    dict(name="R72ExecC1", role="executor", body="""
Independently drive claim C1's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin` and run, with your own scratch dir:
   `python3 -I quality/counters/c1-r72-summary-credit.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC1/run`
2. Run its `--selftest` with the same scratch root, and the held-only prototype
   `python3 -I .ufo/waves/round-72/proto/held-lanes-r72.py --repo . --rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC1/proto`.
3. Reconcile the three runs with the committed receipts (`measurement-c1-r72.txt`,
   `control-baseline-c1-r72.txt`): same cases, same verdicts, same base score 6/8? Name every
   difference, including any rc that disagrees with the contract line.
4. Read `quality/counters/c1-r72-landing-controls.py`'s `credit()` and state in one paragraph
   what it does and does not authenticate.

Do not edit anything. Write `<your dir>/R72ExecC1.md` with the exact commands, rc values, last
lines and your reconciliation.
"""),
    dict(name="R72ExecC2", role="executor", body="""
Independently drive claim C2's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin` and run:
   `python3 -I quality/counters/c2-r72-outcome.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --controls .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC2/run`
2. Run its `--selftest`, and re-derive the held baseline by importing the base harness at
   `976684a2…` yourself (a python one-liner with importlib is fine; keep it in your dir) and
   scoring the eight cases against `outcome_verdict(gate_rc, killed)`.
3. Reconcile with `measurement-c2-r72.txt` and `control-baseline-c2-r72.txt`: same eight cases,
   same verdicts, base 4/8? Name every difference.
4. Read the successor's `outcome_verdict`/`summary_green` and state exactly which inputs decide
   green and which are merely recorded.

Do not edit anything. Write `<your dir>/R72ExecC2.md`.
"""),
    dict(name="R72ExecBattery", role="executor", body="""
Harm-watch battery at the instrument commit: prove the round harmed no measured surface.

From /home/vgpnk/Projects/shokunin/mado-shokunin, run and record command, rc and last line:
- `bash tools/mado-verify.sh --selftest` (expect 460/460)
- `python3 -I quality/check-index.py --repo . --rev master`
- `python3 -I quality/check-tool-ledger.py --repo . --rev master` (expect the pre-round
  population; the three new instruments are not yet registered — report the exact uncovered set)
- `python3 quality/check-axis-scores.py` (and read its usage if flags are needed)
- `python3 -I tools/mado-verify.sh`-independent: `git diff --stat 976684a27e99c2508037a60eec415f550f53d70e master -- tools/mado-verify.sh quality/landing-counters.sh`
- byte-identity of the frozen round-71 instruments: `git rev-parse 976684a2:quality/counters/c1-r71-landing-controls.py master:quality/counters/c1-r71-landing-controls.py` (same blob) and the same for c1-r71-real-children.py and c2-r71-shapes.py.
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` (census BEFORE the round's appends; expect exit 0 and 380 rows).

Do not edit anything. Write `<your dir>/R72ExecBattery.md` with a table command | rc | last line | verdict.
"""),
    dict(name="R72ScribeEntryC1", role="scribe", body="""
Draft the claim-C1 knowledge entry at `<your dir>/draft/corpus/knowledge/summary-credit-own-detail-r72.md`.

Ground it on committed bytes only:
- `.ufo/waves/round-72/claims-declaration-r72.md` § C1 (frozen predicate)
- `quality/counters/c1-r72-landing-controls.py` (`credit()`, `count_fails()`, `last_summary()`, declared limits in the docstring)
- `quality/counters/c1-r72-summary-credit.py` and `.ufo/waves/round-72/measurement-c1-r72.txt`
- the base rule in `quality/counters/c1-r71-landing-controls.py`
- sources: the scout's fetch receipts under `.ufo/waves/round-72/w1/R72ScoutSources/` when they
  exist (CPython 3.14.8 `Doc/library/unittest.rst` § `TestResult.wasSuccessful` and
  `Lib/unittest/main.py`); if the receipts are absent, cite the URLs and mark the provenance
  `[pending receipt]` and say so.

Shape: frontmatter `source:` (cite the S### ids if the scout recorded them, else the URL), `verified-at: 2026-11-04`, `recheck:` (the counting command). Then: the rule in one sentence; a decision table
(last summary parses × detail count adds up × credit); the two named negatives (bare echo,
mismatch) and the two tie cases; what the rule does NOT authenticate (a replayed summary with
matching detail); the measured numbers with their source file. No count without its command.
Never write outside your dir.
"""),
    dict(name="R72ScribeEntryC2", role="scribe", body="""
Draft the claim-C2 knowledge entry at `<your dir>/draft/corpus/knowledge/outcome-verdict-gate-summary-r72.md`.

Ground it on committed bytes only: `.ufo/waves/round-72/claims-declaration-r72.md` § C2,
`quality/counters/c1-r72-landing-controls.py` (`summary_green`, `outcome_exit`,
`outcome_verdict`), `quality/counters/c2-r72-outcome.py`,
`.ufo/waves/round-72/controls/c2-controls-r72.json`,
`.ufo/waves/round-72/measurement-c2-r72.txt`, and the held rule in
`quality/counters/c1-r71-landing-controls.py`. Sources: the scout's receipts for CPython 3.14.8
`Doc/library/unittest.rst` and `Lib/unittest/main.py` when present (a runner's exit derives from
`wasSuccessful()`, the result object); otherwise cite the URLs and mark `[pending receipt]`.

Shape: frontmatter trio; the rule in one sentence; a decision table over
(summary present/parses, p vs n, killed count) → verdict; the four held-wrong cases and why;
the declared limit (summary/status contradiction is scored by the summary by design); the
measured numbers with their file. Never write outside your dir.
"""),
    dict(name="R72ScribeLesson", role="scribe", body="""
Draft three artifacts under your dir:
A) `<your dir>/draft/corpus/lessons/round-72.md` — the round-72 lesson skeleton: header
(author line for the L1, date, base, instruments, measurement), `## Outcome and boundaries`
(what the two claims do and do not claim, from the declaration), `## Gate` with one admit block
template per planned source row (S444 unittest.rst, S445 main.py) and one reject block
(stdtypes.rst under its real 3.14 path) carrying URL / access date / ≤25-word located quote /
why-it-grounds fields, and `## Mistakes` as a table with the four candidate rows already named
in `.ufo/waves/round-71/claims-declaration-r71.md`'s plan and
`corpus/lessons/round-71-verifier-spotcheck.md` (reject row missing; quote word count; results
status field; any misroot the L1 names) — leave evidence cells as `<L1 fills>` where you do not
have committed bytes.
B) `<your dir>/draft/SOURCES-rows.md` — three ready registry rows in the CORPUS.md schema
(11 columns, no `|` inside a cell): S444 unittest.rst (docs, A), S445 Lib/unittest/main.py
(code, A), S446 the `rejected` row for `Doc/builtins/stdtypes.rst` with reason + flip.
C) `<your dir>/draft/QUALITY-criteria.md` — two candidate criteria from this round's own
defects (a rule counts only when the round's own fail lines back it; a verdict reads the
subject's own report, not its exit status), each with the lesson that produced it and a
"shown able to fail" sentence that names a command.
Read first: `corpus/SOURCES.md` (row shape and the W04 duplicate-URL family), `corpus/QUALITY.md`
tail (criteria 114–115 style), `corpus/lessons/round-71.md`. Never edit committed files.
"""),
    dict(name="R72ScoutSources", role="scout", body="""
Open every source this round plans to cite, and produce fetch receipts.

Fetch each URL three times with `curl -fsSL` into your dir; assert the three bodies are
byte-identical; record URL, byte size, sha256, access date 2026-11-04:
1. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/unittest.rst
2. https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/unittest/main.py
3. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/builtins/stdtypes.rst
   (the real 3.14 path; the round-71 reject cited `Doc/library/stdtypes.rst`, which 404s —
   record both statuses, with the exact HTTP code).
Then locate and quote (≤25 words each) with file:line:
- in (1): the `wasSuccessful` method under § `TestResult` — the sentence that says when it
  returns True/False; also note how `TextTestRunner`/`TextTestResult` prints a summary if the
  file documents it.
- in (2): the line where the module-level runner derives the process exit from
  `wasSuccessful()` (search `wasSuccessful`); quote it.
- in (3): the mapping-methods block (`.. method:: update(**kwargs)` / `setdefault`) that the
  round-71 reject described — quote one line and its line number.
Write `<your dir>/receipts.jsonl` (one object per fetch) and `<your dir>/quotes.md` with the
five located quotes. Also state, for each of (1)–(3), whether it is the same file the r71
lesson cited and whether the URL resolves at tag v3.14.8.
"""),
    dict(name="R72ScoutFrontier", role="scout", body="""
Frontier-step reconnaissance for round 72 (read-only).

At /home/vgpnk/Projects/shokunin/mado-shokunin:
1. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`, record rc and the last line; count registry rows with
   `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md` (expect 380 before appends) and list the last five ids.
2. Id-collision pre-check for the planned S444–S446: extract every `^ {0,3}\\| *S[0-9]{3,}` id
   from `corpus/SOURCES.md`, confirm none is S444/S445/S446, and prove the 0–3-space guard
   once on a scratch fixture (copy the registry to your dir, insert an indented `  | S002 |`
   row, show the narrow column-zero pattern misses it and the 0–3-space pattern catches it).
3. Coverage-map census: `grep -cE '^\\| `knowledge/[^`]+\\.md`' corpus/README.md` and
   `ls corpus/knowledge/*.md | wc -l`; the round plans two new entries (starting from 85/85).
4. Ledger census: `python3 -I quality/check-tool-ledger.py --repo . --rev master` — record
   population, uncovered and the exact uncovered paths (the three r72 instruments).
5. Read the last 40 lines of `corpus/README.md` `## Frontier` and name which bullet a round-72
   entry would extend (the r71 kill-credit bullet).
Report every command, rc and count; no edits.
"""),
    dict(name="R72RevC1", role="reviewer", body="""
Adversarial review of claim C1 (calibration: the kill credit requires the run's own failure
detail). Attack it; do not build it.

Read the declaration § C1, `quality/counters/c1-r72-landing-controls.py` (`credit`,
`count_fails`, `last_summary`, `measure`), `quality/counters/c1-r72-summary-credit.py`, the
frozen controls and the measurement. Then try to break it, in your dir only (copy scripts you
need):
- find a child output shape the new rule credits although no assertion of this run produced the
  detail (e.g. detail lines from a nested/other run, a fail line printed by the wrapper, a
  summary whose arithmetic is satisfied by unrelated `SELFTEST FAIL` lines);
- find a genuine kill the new rule rejects (a real instrument that prints its failures in a
  different spelling, omits per-assertion lines, or prints the summary before the details);
- check the carried round-71 expectations still hold for the reason the r71 entry gave;
- check the counter's base score 6/8 is what the base harness really answers (run it).
Deliver `<your dir>/R72RevC1.md`: findings F1..Fn with severity, the exact repro command, and
what the frozen sentence says versus what the code does. Classify each finding as
limit-already-declared, defect, or false positive. No production edits.
"""),
    dict(name="R72RevC2", role="reviewer", body="""
Adversarial review of claim C2 (operability: the outcome verdict reads the gate's summary, not
its exit status). Attack it; do not build it.

Read declaration § C2, `summary_green`/`outcome_exit`/`outcome_verdict`,
`quality/counters/c2-r72-outcome.py`, the controls JSON, the measurement, and the base harness's
`outcome_exit`. Try to break it in your dir:
- a gate that prints a green summary and then exits 2 for a real setup failure — is MET honest?
- a gate that prints green then a later failing summary (tie) — does last-wins do what the
  sentence says?
- a gate that prints its summary to stderr only, or two summaries on different streams;
- the `selftest=<p/n|none>` contract field and `summary_fraction()` — does the printed receipt
  state what actually decided the verdict?
- whether the counter's `expected_from_summary` duplicates the tested predicate (a
  same-logic oracle) and what that weakens.
Deliver `<your dir>/R72RevC2.md`: findings with severity, repro command, the sentence vs the
code, and a limit/defect/false-positive classification. No production edits.
"""),
    dict(name="R72CriticClaims", role="critic", body="""
Falsify both frozen claims without building them. Read the declaration, both counters, both
receipts and the held baselines. Answer these, each with the command you ran:
1. Is either target reachable by a do-nothing control? (e.g. a harness that always answers
   `mz=fail` or always `TARGET_MISSED` — score it on the frozen control sets; the green cases
   must reject it. Show the score.)
2. Does either counter's own scoring agree with the frozen labels for the wrong reason — e.g.
   does `score()` accept a missing verdict, does `expected_from_summary` in the C2 counter
   re-implement the predicate it tests (and would a wrong successor still pass), does the C2
   counter's base leg use the base harness's own function?
3. Are the before→after numbers in the declaration the same ones the receipts print (8/8 vs
   6/8; 8/8 vs 4/8), at which revision, and is the measured revision the one that contains the
   instruments?
4. Is the claim separable as declared (each counter reads only its own function and control set)?
Deliver `<your dir>/R72CriticClaims.md` with a verdict line per question and evidence pointers.
No production edits.
"""),
    dict(name="R72MutBattery", role="mutation-tester", body="""
Independent mutation testing of the two round-72 instruments (scratch only; never edit lane
files). Copy `quality/counters/c1-r72-landing-controls.py`,
`quality/counters/c1-r72-summary-credit.py` and `quality/counters/c2-r72-outcome.py` into your
dir and apply one mutation at a time, re-running the matching counter against the MUTANTS
(point `--rev` at a scratch git repo that carries the mutants, or run the mutated harness
directly through the counter's `--base-rev`/candidate mechanics). At minimum:
M1 `credit()` drops the arithmetic check; M2 `credit()` accepts a bare summary; M3
`summary_green()` drops the `n > 0` guard; M4 `outcome_verdict()` reverts to the exit status;
M5 the counter's `score()` accepts `None`. For each: does the frozen control set catch it
(correct < 8 or verdict TARGET_MISSED)? A mutant that still prints TARGET_MET is a real gap —
name it, with the exact output.
Deliver `<your dir>/R72MutBattery.md`: mutation | operation | counter output last line | caught?
and a summary table. Never commit, never touch the lane tree.
"""),
    dict(name="R72ConnSiblings", role="connector", body="""
Cross-lane pattern scan (read-only; no drafts of production files).

1. Search sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only) for the same
   two doctrines this round lands: a summary-over-exit-status rule and a kill-credit
   arithmetic/authenticity rule. Useful patterns: `SELFTEST:`, `summary_shows_failure`,
   `outcome_verdict`, `assertions passed`, `TARGET_MET`, `mz=`/`killed=`. Name the files and
   lanes; quote one line each. Do not read credentials or session material.
2. Report whether the two rules exist in another lane in a form this lane should adopt or defer
   to (adjacency duty: report, never absorb).
3. Read `considerthese/2026-10-28.md` (operator-authored input; never edit it) and name at most
   ONE still-unimplemented proposal that fits this round's ground (landing-instrument evidence)
   — with the proposal's exact words and why it fits; if none fits, say so.
4. Check `.ufo/waves/round-71/` for any seat artifact that contends the round-72 plan (e.g. a
   reviewer note on the summary/outcome rules) and quote it.
Deliver `<your dir>/R72ConnSiblings.md`. No writes outside your dir.
"""),
]


def main():
    items = []
    for item in ITEMS:
        prompt = GODSPEED + "\nYour name: %s. Your only write directory: %s/w1/%s/. Scratch: " \
            "/fast/scratch/hyaku/mado-r72/%s/.\n" % (item["name"], WAVE, item["name"], item["name"])
        prompt += item["body"]
        items.append({"name": item["name"], "role": item["role"], "prompt": prompt})
    spec = {"wave": "w1", "reportDir": ".ufo/waves/round-72/w1",
            "context": CONTEXT, "items": items}
    out = os.path.join(WAVE, "w1-spec.json")
    with open(out, "w") as fh:
        json.dump(spec, fh, indent=1)
    print("wrote", out, len(items), "items")


if __name__ == "__main__":
    main()

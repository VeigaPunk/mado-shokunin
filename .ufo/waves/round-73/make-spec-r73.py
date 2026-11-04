#!/usr/bin/env python3
"""Build .ufo/waves/round-73/w1-spec.json (one v1 wave, 13 seats)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE = os.path.join(LANE, ".ufo", "waves", "round-73")
REV = "1459cca11fb5d3956a6e9a128217852dd0c28cb9"
FREEZE = "87e4c61ac90e9ac587c9f65ac7844ded268d9046"
BASE = "d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + """
Round mado 73, ONE v1 wave (13 seats). Claims: C1 calibration (the frozen outcome case set
separates four named mutations of the landing outcome rule; the held eight-case set separates
two) and C2 operability (the guard census counts the `global`-declared guard and the
mutated-`os.environ` transport; the held round-71 classifier misses exactly those three cases).
The L1 holds the planner seat (the validator rejects `planner` as a swarm role); no planner is
dispatched.

Read FIRST:
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-73/claims-declaration-r73.md
(the frozen claims, predicates, counting commands, kill rules, targets and limits; base
`d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce`, freeze `87e4c61ac90e9ac587c9f65ac7844ded268d9046`,
instruments `1459cca11fb5d3956a6e9a128217852dd0c28cb9`).

Committed receipts (re-read, do not rewrite):
- `.ufo/waves/round-73/measurement-c1-r73.txt` -> `cases=10 mutants=4 killed=4 base_killed=2
  verdict=TARGET_MET`, rc 0.
- `.ufo/waves/round-73/measurement-c2-r73.txt` -> `population=20 readers=13 guarded=13
  unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET`, rc 0.
- `.ufo/waves/round-73/control-baseline-r73.txt` (the pre-freeze do-nothing legs: held set
  killed=2/4, held classifier 25/28).

Hard bounds, every seat:
- Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-73/w1/<your name>/.
  Never edit a committed lane file (production instruments, corpus, SKILL.md, SCORECARD.md,
  LOG.md, README, SOURCES.md); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash, no jj mutation);
  read-only git (`show`, `ls-tree`, `rev-parse`, `status`, `log`) is fine. Never write the fleet
  repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `scripts/`, `templates/`
  or MANIFEST.json.
- Never message `agent://all`; reply only to your L1 (`MadoR73`) or nothing.
- Scratch: /fast/scratch/hyaku/mado-r73/<your name>/ (create it; pass it explicitly; never use
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
    dict(name="R73ExecC1", role="executor", body="""
Independently drive claim C1's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin` and run, with your own scratch dir:
   `python3 -I quality/counters/c1-r73-summary-mutants.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c1-outcomes-r73.json --scratch-root /fast/scratch/hyaku/mado-r73/R73ExecC1/run`
2. Run its `--selftest` with the same scratch root.
3. Reconcile with the committed receipt `measurement-c1-r73.txt`: same last line, same rc? Name
   every difference.
4. Read `quality/counters/c1-r73-summary-mutants.py`'s `MUTANTS` table and state in one paragraph
   which rule each mutation breaks and which frozen case separates it; then check that claim by
   reading the per-mutant lines, not by trusting them.

Do not edit any committed file. Write `<your dir>/R73ExecC1.md` with the exact commands, rc
values, last lines, per-mutant reconciliation and the paragraph.
"""),
    dict(name="R73ExecC2", role="executor", body="""
Independently drive claim C2's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin` and run:
   `python3 -I quality/counters/c2-r73-shapes.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9 --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root /fast/scratch/hyaku/mado-r73/R73ExecC2/run`
2. Run its `--selftest` with the same scratch root.
3. Reconcile with `measurement-c2-r73.txt`; name every difference, including any rc that
   disagrees with the contract line.
4. Independently classify four snippets of your own invention against `c2-r73-shapes.py`'s
   `classify` — one true positive for the global-declared shape, one true positive for the
   `os.environ` transport, and one negative for each — and report whether the classifier agrees
   with your reading. State any disagreement as a finding.

Do not edit any committed file. Write `<your dir>/R73ExecC2.md` with the commands, rc values, last
lines and the four snippets with their outputs.
"""),
    dict(name="R73ExecBattery", role="executor", body="""
Harm watch at the instrument commit `1459cca11fb5d3956a6e9a128217852dd0c28cb9`: prove the round
harmed no measured surface. From /home/vgpnk/Projects/shokunin/mado-shokunin run, recording each
command's own rc (a setup error is not a pass):
1. `bash tools/mado-verify.sh --selftest` — expect `MADO_SELFTEST: 460/460 assertions passed`.
2. `python3 -I quality/check-index.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9`.
3. `python3 -I quality/check-tool-ledger.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9`.
4. `python3 -I quality/check-axis-scores.py --repo . --rev 1459cca11fb5d3956a6e9a128217852dd0c28cb9`
   (if the flag set differs, report the real argv the script accepts).
5. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`.
6. Frozen-identity sweep: `git rev-parse 1459cca1:quality/counters/c1-r72-landing-controls.py
   d3f6c9f5:quality/counters/c1-r72-landing-controls.py` and the same for
   `c2-r71-shapes.py`, `c2-r70-carriers.py`, `tools/mado-verify.sh`, `quality/landing-counters.sh`
   — every pair must be identical blob ids.
Print one line per command: `cmd=<n> rc=<rc> output=<last line>`. Write
`<your dir>/R73ExecBattery.md` and `harm-watch-r73.txt` inside it.
"""),
    dict(name="R73ScribeEntryC1", role="scribe", body="""
Draft the claim-C1 knowledge entry at `<your dir>/draft/corpus/knowledge/control-set-mutant-kill-r73.md`.

Content to ground (verify each fact against the committed files before writing it; cite paths,
hashes and the receipt lines):
- The round-72 frozen eight-case outcome set passed two broken rules: the mutation battery's
  `summary_green` without the `n > 0` guard (`.ufo/waves/round-72/w1/R72MutBattery.md`, GAP-1) and
  the pre-repair prefix-matching `last_parsed_summary` (the r72 declaration's erratum §1, repaired
  at `4f598cfd` with only a selftest regression).
- The round-73 ten-case set adds `zero-denominator` and `valid-then-garbled`; each separates
  exactly one of the four named mutations (N1..N4) and the held eight-case set separates only two
  (`.ufo/waves/round-73/measurement-c1-r73.txt`).
- The principle: a control set is an instrument; its discriminating power is measurable by
  mutating the rule it is supposed to certify, and a set that passes a broken rule certifies
  nothing. State the bound: four named mutations of one rule family are not fault coverage.
Open with the provenance trio (`source:`, `verified-at:`, `recheck:`); `source:` cites the
committed receipts and the r72 battery, not a URL. Keep it 120-220 lines, tables over prose.
Write `Report: .ufo/waves/round-73/w1/R73ScribeEntryC1.md` naming the draft path.
"""),
    dict(name="R73ScribeEntryC2", role="scribe", body="""
Draft the claim-C2 knowledge entry at `<your dir>/draft/corpus/knowledge/guard-carrier-global-environ-r73.md`.

Content to ground (re-verify against committed bytes; cite paths and receipt lines):
- The guard census (`quality/check-*.py` population) now counts two more carriers: (a) a mapping
  guarded from inside a function that declares the name `global`, then handed as `env=` at a later
  git launch; (b) `os.environ[KEY] = "1"` before a launch whose `env=` copies the environment with
  `{**os.environ}` or `dict(os.environ)`.
- The held round-71 classifier missed exactly those three cases (25/28); the successor scores
  28/28 with the same population (20 files, 13 readers, 13 guarded) —
  `.ufo/waves/round-73/measurement-c2-r73.txt`, `.ufo/waves/round-73/control-baseline-r73.txt`.
- Bounds to state: one `global` declaration, cross-function line order (a store in a function that
  runs after the launch still counts — the attribute-flow approximation), one `os.environ` store,
  two copy spellings, no alias of `os.environ`, no value interpretation.
Open with the provenance trio. `source:` cites the three sources the wave's scout is fetching
(CPython 3.14.8 `Doc/reference/simple_stmts.rst` for `global`, `Doc/library/os.rst` for
`os.environ`, `Doc/library/subprocess.rst` for `env`) by their S-ids once the L1 assigns them —
leave the S-ids as `<S447>/<S448>/<S449>` placeholders and state that the L1 re-points them. Keep
it 120-220 lines, tables over prose.
Write `Report: .ufo/waves/round-73/w1/R73ScribeEntryC2.md` naming the draft path.
"""),
    dict(name="R73ScribeLesson", role="scribe", body="""
Draft the round-73 lesson at `<your dir>/draft/corpus/lessons/round-73.md` (and a `## Gate` block
variant at `<your dir>/draft/gate-block.md` for the L1 to merge).

Facts the lesson must record (verify each against the named file):
- Base `d3f6c9f5…`, freeze `87e4c61a…`, instruments `1459cca1…`; two claims, both TARGET_MET with
  the do-nothing controls at 2/4 and 25/28.
- `## Mistakes`: mine the round-72 verifier spot-check's routed defects and this round's own
  near-miss — the first r73 classifier draft counted a store `inside a function that runs after
  the launch` as a guard (line order, not execution order) and the L1 first wrote that
  regression's label the wrong way round; the fix is the disclosed line-order limit plus the
  `r73-global-rebind-replaced-between` regression. Also mine: the embedded-case literals were
  first written with doubled newline escapes (invalid snippets) and only the selftest caught it.
  Classes from the CORPUS vocabulary (`reference-drift`, `vacuous`, `number-drift`, `scope`,
  `landing`), each with evidence pointer, captured-by, and a fix that can show its failure.
- `## Gate`: placeholders for the three source rows the scout fetches (`<S447>`–`<S449>`): URL,
  access date, ≤25-word located quote. Mark them `<fill by L1 after the fetch>` so the L1 pastes
  the real quote; do not invent a quote.
Write `Report: .ufo/waves/round-73/w1/R73ScribeLesson.md` naming both drafts.
"""),
    dict(name="R73ScoutSources", role="scout", body="""
Open the three sources claim C2 cites, and produce fetch receipts under your dir.

Fetch each URL three times, byte-compare, and record sha256 + byte count:
1. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst
   (the `global` statement section) — find the sentence that says the statement causes the listed
   identifiers to be interpreted as globals, and give its line numbers.
2. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst
   (`os.environ`) — find the sentence describing `os.environ` as the environment mapping, with
   line numbers.
3. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst
   (`env` parameter of `Popen`) — find the sentence that `env` defines the environment variables
   for the new process, with line numbers.
For each: quote at most 25 words, exactly as the bytes print it (no paraphrase), and count the
words with `awk '{print NF}'`. Write `<your dir>/R73ScoutSources.md` (URL, access date, sha256,
bytes, line range, quote, word count) and keep the raw bodies at
`<your dir>/fetch/<name>.<1|2|3>`. Report any fetch failure rather than substituting another
mirror.
Write `Report: .ufo/waves/round-73/w1/R73ScoutSources.md`.
"""),
    dict(name="R73ScoutFrontier", role="scout", body="""
Frontier-step reconnaissance for round 73 (read-only).

At /home/vgpnk/Projects/shokunin/mado-shokunin:
1. Run the frozen census command
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
   and record its exit code and row count (the round-start count is 383 rows, exit 0).
2. List the `corpus/README.md` `## Frontier` bullets and name which of the round-72 frontier
   items this round's claims move and which stay open.
3. Read `/home/vgpnk/Projects/shokunin/mado-shokunin/considerthese/` — list the files, and identify
   at most ONE still-unimplemented proposal that fits this round's claims or the lane's next
   round; quote the line that proposes it and say what opening it would require.
4. Duplicate-id precondition for the round's appends: extract the highest `S0NN` id in
   `corpus/SOURCES.md` (`grep -oE '^\\| *S[0-9]+' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -V | tail -3`)
   and confirm S447-S449 are unused (`grep -c 'S447\\|S448\\|S449' corpus/SOURCES.md`).
Write `<your dir>/R73ScoutFrontier.md` with the command outputs and the one proposal.
Write `Report: .ufo/waves/round-73/w1/R73ScoutFrontier.md`.
"""),
    dict(name="R73RevC1", role="reviewer", body="""
Adversarial review of claim C1 (calibration: the frozen outcome set separates four named
mutations). Attack it; do not rebuild it.

1. Re-run the frozen command at `1459cca11fb5d3956a6e9a128217852dd0c28cb9` and its `--selftest`.
2. Attack the mutation table in `quality/counters/c1-r73-summary-mutants.py`: is each named
   delta really the rule it claims to break? Does any mutation change behaviour *outside* the ten
   cases (so the kill is an artefact)? Can a mutation be killed by a case whose label is wrong
   (re-derive each new case's expected verdict from the frozen sentence yourself)?
3. Attack the carry-forward claim: is the round-72 eight-case set really byte-identical (hash it
   yourself), and does the held leg really separate only two?
4. Name at least one concrete weakness with a repro or a precise reading, and say whether the
   claim's frozen sentence survives it. Deliver findings as F1, F2... with severity.
Write `<your dir>/R73RevC1.md`. `Report: .ufo/waves/round-73/w1/R73RevC1.md`.
"""),
    dict(name="R73RevC2", role="reviewer", body="""
Adversarial review of claim C2 (operability: the guard census counts the global-declared guard and
the mutated-`os.environ` transport). Attack it; do not rebuild it.

1. Re-run the frozen command at `1459cca11fb5d3956a6e9a128217852dd0c28cb9` and its `--selftest`.
2. Attack the two new detectors in `quality/counters/c2-r73-shapes.py` (`global_guard`,
   `environ_transport_guard`): construct at least three programs of your own that are NOT in the
   frozen set — a true guard it misses, a false guard it accepts, and one that shows the declared
   line-order approximation. Report `classify()` output for each.
3. Check the carry-forward: hash `.ufo/waves/round-71/controls/c2-controls-r71.json` and confirm
   the 23 cases are unchanged in the new set; confirm the held classifier really scores 25/28 and
   that its three misses are exactly the three new positives.
4. Does the population count (20/13/13/0) still hold at the instrument commit? Re-derive it.
Deliver findings as F1, F2... with severity and repro.
Write `<your dir>/R73RevC2.md`. `Report: .ufo/waves/round-73/w1/R73RevC2.md`.
"""),
    dict(name="R73CriticClaims", role="critic", body="""
Falsify both frozen claims without building them. Read the declaration, the two counters, both
control sets, the measurement receipts and the baseline receipt.

For each claim answer: (1) does the printed receipt's last line follow from the per-case lines,
or is it an assertion? (2) is the do-nothing control genuinely pre-freeze (timestamps, commit
order) or retrofitted? (3) is the bounded score `10 x killed / 4` / `10 x controls / 28` the
same quantity the SCORECARD will record? (4) can a do-nothing implementation reach the target —
e.g. does the mutant table simply encode its own answers, and would a counter that prints
`killed=4` without executing the mutations pass the selftest? Name at least two counterexamples
or a concrete "no counterexample found" with the sweep you ran.
Write `<your dir>/R73CriticClaims.md`. `Report: .ufo/waves/round-73/w1/R73CriticClaims.md`.
"""),
    dict(name="R73MutBattery", role="mutation-tester", body="""
Independent mutation battery for round 73's instruments (frozen originals, never edit them).

1. Build a scratch clone of the lane under /fast/scratch/hyaku/mado-r73/R73MutBattery/ (assert
   `git rev-parse --show-toplevel` equals the clone before any write) and commit four mutants of
   `quality/counters/c1-r73-summary-mutants.py` and four of `quality/counters/c2-r73-shapes.py`
   with git plumbing: for C1, drop the `base_killed` leg, make the mutation loop skip N4, make
   `score()` accept a None verdict, and make the held check skip the hash; for C2, drop the
   `global_guard` call, drop the `environ_transport_guard` call, relax `copied_environ`'s
   `not node.keywords` guard, and make `verdict_met` ignore `base_controls`.
2. Run each mutant's frozen command and record whether the mutant is caught (a wrong last line,
   or a rc that is not 0 with the contract line absent).
3. Report the survivors honestly — a survivor is a real gap and gets a named repro.
Write `<your dir>/R73MutBattery.md` with the table and receipts. `Report: .ufo/waves/round-73/w1/R73MutBattery.md`.
"""),
    dict(name="R73ConnSiblings", role="connector", body="""
Connector: sibling-overlap scan and cross-claim pattern finding (read-only).

1. Scan the fleet for other lanes' counters that score a control set by mutation (grep
   `/home/vgpnk/Projects/shokunin/*-shokunin/quality/counters/*.py` for `mutant`/`killed`/
   `base_killed`) and the fleet for guard/carrier censuses (`GIT_NO_REPLACE_OBJECTS`). Report
   overlap: does mado duplicate a sibling's instrument, or is this ground the siblings do not
   hold?
2. Look for the shared pattern between this round's two claims: a set of *controls* certifies an
   instrument only if it separates a mutation of that instrument. Name at least two other mado
   instruments (`tools/mado-verify.sh` and one counter) that have never been scored that way, so
   the next rounds' claim candidates are grounded.
3. Name any file another lane owns that this round's claims touch (expected: none) and say why.
Write `<your dir>/R73ConnSiblings.md`. `Report: .ufo/waves/round-73/w1/R73ConnSiblings.md`.
"""),
]


def main():
    items = []
    for item in ITEMS:
        prompt = (GODSPEED + "\nYour name: %s. Your only write directory: %s/.ufo/waves/round-73/w1/%s/. "
                  "Scratch: /fast/scratch/hyaku/mado-r73/%s/.\n" % (item["name"], LANE, item["name"],
                                                                   item["name"]))
        prompt += item["body"]
        items.append({"name": item["name"], "role": item["role"], "prompt": prompt})
    spec = {"wave": "w1", "reportDir": ".ufo/waves/round-73/w1", "context": CONTEXT, "items": items}
    path = os.path.join(WAVE, "w1-spec.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print(path, len(items), "items")


if __name__ == "__main__":
    main()

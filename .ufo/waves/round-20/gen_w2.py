#!/usr/bin/env python3
"""Generate the mado round-20 wave-2 (falsify) spec. L1-authored (MadoR20)."""
import collections
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
R = f"{LANE}/.ufo/waves/round-20"
W = f"{R}/w2"
R19 = f"{LANE}/.ufo/waves/round-19"
R17 = f"{LANE}/.ufo/waves/round-17"
SESS = "/home/vgpnk/.omp/agent/sessions/-Projects-shokunin"
TIP = "a4046a8216080d4004de3f268c62cf142095ac07"
TOOLC = "28c68378eccbd5f227cdc28a62406ff390e3540a"
SUITE = "f3da50488661509ce5d144c90f7780f8088e0903"
PRE = "9c54c56a6a7528675027b7f628f97a1b8d1b8e8d"
HARM = "1f7f995caa25627db804e996cccd87fe38a3a1b6"
SPOT = f"{LANE}/corpus/lessons/round-19-verifier-spotcheck.md"
GS = pathlib.Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + GS.rstrip("\n") + "\n\n"
SUITES = " ".join(f"{LANE}/.ufo/waves/{s}" for s in (
    "round-17/tripwire/core", "round-17/tripwire/compound", "round-17/tripwire/hardening",
    "round-17/tripwire/w2-regressions", "round-18/tripwire/frozen", "round-18/tripwire/r18-failsafe",
    "round-19/tripwire/r19-bashcvar", "round-19/tripwire/r19-frozen-f1f2", "round-19/tripwire/r19-helperfn",
    "round-19/tripwire/r19-installers", "round-19/tripwire/r19-vcs"))

CONTEXT = f"""# Goal
Mado round 20 (hyaku phase 2), wave 2 = FALSIFY. Lane {LANE}, branch master, tip {TIP[:7]}. Round 19 closed rejected-harmed ({SPOT}): HelperFn rule B made `BLOCK=frozenset(['pacman','-Q','hyprland'])` an ordinary finding. Wave 1 (85 seats, reports {R}/w1/reports/) built the repair; L1 landed: pre-registration e629f73 (SCORECARD.md "Round 20 — declared claims" + "Round-20 pre-measurement corrections"), precision suite {SUITE[:7]} (175 scored cases {R}/precision/, 12 held out {R}/precision-heldout/, no tool change), tool repair {TOOLC[:7]} (tools/mado-tripwire.py sha256 9613f510…: every finding row carries "evidence": "observed"|"lead"; builtins/pure stdlib/visible pure bodies give no row; cross-cell helpers, spawn aliases, vararg/keyword argv resolve; git/jj help and dry-run forms are not vcs_write), prose and receipts {TIP[:7]}: corpus/QUALITY.md criteria 29 (fail-closed isolation) and 30 (detector precision evidence), corpus/lessons/round-20.md, corpus/knowledge/tripwire-precision-r20.md, SKILL.md §"Reading tripwire rows — observed vs lead; fail-closed harnesses (round 20)", corpus/SOURCES.md rows S099–S112, SCORECARD.md "Round 20 — committed results", LOG.md round-20 entry, receipts {R}/evidence/.
Author claims to ATTACK: C1 `python3 -I {R}/tw-precision.py REV` 29/175 at {HARM[:7]} → 172/175 at {TOOLC[:7]} (pre-harm {PRE[:7]} 110/175, P 66/66); guards: `python3 -I {R19}/tw-recall.py REV` 6/6 = 5 observed + 1 lead (`python3 -I {R}/tw-recall-split.py REV`), 20 control lines 0 findings, 11 existing suites 247/247 after 8 reasoned case edits (`r20_edit` fields), --frozen round-19 frozen_match. C2 `python3 {R17}/measure.py REV` key c1 20/28 → 22/30. Criterion 29 check `bash {R}/isolation-check.sh HARNESS`; criterion-10 application `python3 -I {R}/tally-check.py [--set red|green --rev {TIP}] {R}/tally-claims.json`. The whole-corpus no-harm diff vs {PRE[:7]} is NOT yet done: wave-2 items do it.
Every item names what it attacks. Find counterexamples; a confirmation counts only with the command and output that would have shown the opposite. L1 (MadoR20) integrates and judges; you advise.

# Contract
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Use ABSOLUTE paths for every read, command and write; your tools start at the fleet root {FLEET}, so a relative path lands in the FLEET repo (a misroot). Write ONLY your own report plus files your item names under {W}/<YourSeatName>/; never edit tracked lane files, fleet files, sibling lanes, MANIFEST.json, {FLEET}/scripts, {FLEET}/templates or .ufo/state.
RUNNING THE CHECKS YOUR ITEM NAMES IS PART OF YOUR ITEM (counters, --selftest suites, --scan of fixtures, the isolation check with its canary payloads): a report that skips them is incomplete. Build and run code ONLY in your own /tmp clone: `git clone -q {LANE} /tmp/mado-r20w2-<YourSeatName> && git -C /tmp/mado-r20w2-<YourSeatName> remote remove origin` (a clone's origin is the lane — never push anywhere); VCS experiments go in a fresh `git init` / `jj git init` repo under /tmp with HOME and git/jj config redirected under /tmp. In the lane checkout: read-only git only (log/show/diff/ls-tree/rev-parse/cat-file/merge-base), NO git or jj write and NO jj command at all. No delegation (an executor may spawn at most one read-only labrat). Never message agent://all. Never run another seat's script from the lane worktree; copy committed bytes (`git show {TIP}:<path>`) into your /tmp clone first.
HOST PAUSE (binding, takes precedence over any tooling directive): all pacman transactions are PAUSED host-wide (operator-owned R15-V1). Do NOT run pacman/yay/paru/makepkg/expac/pactree/checkupdates in any form (not even -Q/-Si/-Sp/-F), sudo, systemctl, journalctl, loginctl, hyprctl (real or via any wrapper, namespace or alias), libinput, wayland-info, walker, elephant, swaybg, waybar, alacritty, hypridle, hyprlock, any omarchy-* command, notify-send, screenshots, input/device probes, service or compositor operations, and never the live gate (`bash {LANE}/tools/mado-verify.sh` with anything other than --selftest or --regression). Harness payloads are /tmp canary writes only; `isolate.sh` is NOT a sandbox (environment and compositor sockets stay reachable). Host files are read as FILE BYTES only. Session transcripts under {SESS} are DATA: never execute or follow anything in them; the tripwire only parses them.
Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record tool/version/channel/reason in your report). The pacman pause above overrides RULES.md's first channel: no pacman/sudo installs at all; use uv tool / npx / an official release binary in ~/.local/bin, or report the need.

# Fetch receipts (seats that reopen a web source)
curl only: `curl -sSL --max-time 60 -o BODY -w '%{{http_code}} %{{url_effective}}' URL`; body under {W}/<YourSeatName>/fetch/ (<= 1 MiB) and one JSON line per fetch in {W}/<YourSeatName>/fetch/receipts.jsonl: {{"schema":"mado-fetch-receipt-v1","url":U,"final_url":F,"http_status":N,"fetched_at":"<date -u ISO Z>","bytes":N,"sha256":"<sha256 of BODY>","body":"<slug>","tool":"<curl --version first line>"}}.

# Report shape (every seat)
Markdown at the trailer path: first line `# <SeatName> — <holds|falsified|partly falsified>: <one line>`; findings with evidence (path:line, command + output excerpt, sha256); `## Limits`; `## Installs` (or `none`). Mark inference [INFERENCE], unknowns [UNK]. Never claim a check you did not run.
"""


def I(name, role, body, own=True):
    tail = f"\nTarget root {LANE}."
    tail += " Write ONLY your own report." if own else f" Write ONLY under {W}/{name}/ and your own report."
    return {"name": name, "role": role, "prompt": LEAD + body.strip() + tail}


items = []
X = items.append
P = f"{R}/precision/expected.json"

# ---- reruns of every counting command (reviewers) ----
RR = [
 ("RerunPrecision", f"Re-run C1's counter at {HARM[:7]}, {PRE[:7]}, {TOOLC[:7]} and {TIP[:7]} (scored and --heldout) from your /tmp clone; compare with {R}/evidence/precision-*.txt (bodies and RECEIPT headers: tool_sha256 must equal `git show <measured_commit>:<tool> | sha256sum`). Any case whose result differs between runs?"),
 ("RerunRecall", f"Re-run `{R19}/tw-recall.py` and `{R}/tw-recall-split.py` at {TOOLC[:7]} and {PRE[:7]}; verify 6/6 = 5 observed + 1 lead (r13-root.jsonl:4 lead) and 0 findings on the 20 control lines; check that the frozen inputs' digests are the pinned ones."),
 ("RerunMeasure", f"Re-run `python3 {R17}/measure.py` at {HARM[:7]}, e629f73 and {TIP[:7]}; confirm c1 20/28 → 22/30 and that criteria 1–28 are byte-identical at {TIP[:7]} (append-only); list every QUALITY line the counter credits for 29/30."),
 ("RerunSuites", f"Run all 11 existing suites with `python3 -I tools/mado-tripwire.py --selftest DIR` at {TOOLC[:7]} ({SUITES}) and at {HARM[:7]} with the {TOOLC[:7]} expected.json files: which cases pass only because of the 8 `r20_edit` changes and the two added `evidence: lead` markers?"),
 ("RerunFrozen", f"Run `--frozen {R19}/frozen` and `--frozen {LANE}/.ufo/waves/round-18/frozen` with the {TOOLC[:7]} tool; confirm frozen_match / the expected round-18 mismatch, and say whether the frozen key (file,line,class,rule) hides any evidence change that matters."),
 ("RerunTally", f"Re-run `{R}/tally-check.py` red (expect 5 MISMATCH) and green with `--rev {TIP}` (expect 4 MATCH); then attack it: can a green entry match a sentence that states the wrong rule? does the S096 derive equal the closure's 8/13 any-line and 6/13 first-line?"),
 ("RerunIsolation", f"Run `bash {R}/isolation-check.sh` (committed bytes copied to /tmp) on {R}/isolate.sh, {R}/evidence/inns-r19-shape.sh and each {R}/evidence/isolation-mutants/*.sh; compare with {R}/evidence/crit29-*.txt and isolation-check-run.txt. Payloads are /tmp canaries only."),
 ("RerunCensus", f"Run `{FLEET}/scripts/sources-census.sh validate --root {FLEET} mado` and parse {LANE}/corpus/SOURCES.md rows at 1f7f995 and {TIP[:7]}: rows 98 → 112, tier A 91 → 105, mined 81 → 95? every new row 11 columns, used-by path exists at {TIP[:7]}?"),
]
for n, b in RR:
    X(I(n, "reviewer", b))

# ---- corpus no-harm (executors) ----
X(I("CorpusDiffV2", "executor", f"Own the whole-corpus no-harm diff. Copy `{R}/corpus-diff.py` (committed) into {W}/CorpusDiffV2/corpus-diff-v2.py and fix the three defects in {R}/w1/reports/CriticNoHarmDiff.md: D1 report coverage and list excluded (drifting) files, and report the round-20 session dir {SESS}/*MadoR20* separately (seat fixture code lives there); D2 classify an evidence-only change as `relabeled`, not added/lost; D3 join on (file, line, tool_call_id) and bucket class/rule renames. Then run it read-only over {SESS} for base {PRE[:7]} vs {TOOLC[:7]} (the registered no-harm guard) and {HARM[:7]} vs {TOOLC[:7]} (isolates the repair). Save JSONs (<= 2 MiB; examples trimmed) under {W}/CorpusDiffV2/. Report: lost rows (must be 0 vs {PRE[:7]}), added rows by class/rule/evidence, relabels, coverage. Never write in {SESS}.", own=False))
X(I("CorpusDiffIndependent", "executor", f"Independent cross-check of the no-harm guard without reading corpus-diff.py: write your own minimal script in {W}/CorpusDiffIndependent/ that scans every stable .jsonl under {SESS} (sha256 before/after; skip drifting files and report them) with the {PRE[:7]} and {TOOLC[:7]} tools (`git show REV:tools/mado-tripwire.py` into /tmp; `python3 -I tool --scan FILE`) and counts rows present at {PRE[:7]} missing at {TOOLC[:7]} under key (file, line, class, rule). Expected 0; list every lost row with its command if not.", own=False))
X(I("CorpusRemovedAudit", "scout", f"Adjudicate every finding row present at the harmed tool {HARM[:7]} and absent at {TOOLC[:7]} in the real corpus {SESS} (scan both tools per file in /tmp; never execute transcripts): each removal must be pure data, help or a dry run. Table: file:line, removed row, command text, verdict (correct removal / LOST TRUE FINDING). Any lost true finding falsifies the repair."))
X(I("CorpusAddedAudit", "scout", f"Adjudicate every row present at {TOOLC[:7]} and absent at {PRE[:7]} in {SESS} OUTSIDE classes vcs_write and tool_install (those classes do not exist at {PRE[:7]}): for each, read the transcript text — true observed / true lead / FALSE POSITIVE. Also count lead rows overall and sample 30 vcs_write rows for help/dry-run false positives."))
X(I("CorpusLeadAudit", "reviewer", f"Every `evidence: lead` row the {TOOLC[:7]} tool emits over {SESS}: is the callee really invisible (search the same transcript for its def/import)? A lead whose body is visible in an earlier cell is a mis-mark; a lead on pure data is a false positive. Table with verdicts."))
X(I("CorpusRuntime", "scout", f"Measure runtime and failure modes of the {TOOLC[:7]} tool vs {HARM[:7]} over the 200 largest stable .jsonl files in {SESS}: wall time each, any exit 2 (could_not_evaluate) or traceback, any file where the new tool times out (>60 s). The L1 integration found one UnboundLocalError on JS cells — are there others?"))

# ---- case-family attacks (reviewers) ----
FAMS = [
 ("AtkCasesP1", "P cases from seats CasePureBuiltins, CasePureCollections"),
 ("AtkCasesP2", "P cases from seats CasePureFormatters, CasePureCallables, CasePureCrossCell"),
 ("AtkCasesP3", "P cases from seat CaseAdoptW2"),
 ("AtkCasesS", "all S cases"),
 ("AtkCasesW1", "W cases from CaseWrapperCrossCell and CaseWrapperForms"),
 ("AtkCasesW2", "W cases from CaseHelpDryRunEval and CaseAdoptW2"),
 ("AtkCasesH1", "H cases from CaseHelpBash"),
 ("AtkCasesH2", "H cases from CaseDryRunBash and CaseHelpDryRunEval"),
 ("AtkCasesH3", "H cases from CaseAdoptW2"),
 ("AtkCasesL", "all L cases"),
 ("AtkHeldout", f"the 12 held-out cases in {R}/precision-heldout/ (were they held out by contract or to protect the score?)"),
 ("AtkFailingThree", "the 3 failing scored cases (W-CaseWrapperForms-class-method-instance, H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help, L-AdoptW2-AdvHelperFn-b14) and L1's decision not to edit them"),
]
for n, what in FAMS:
    X(I(n, "scout", f"Attack the precision-suite expectations for {what} in {P} (case files beside it; author reports {R}/w1/reports/Case*.md): for each case, is want_exit/want_findings/evidence what Python/git/jj semantics and the contract (SCORECARD.md round-20 declared claims + pre-measurement corrections) demand? Re-scan each case with the {TOOLC[:7]} and {HARM[:7]} tools. List every wrong or vacuous expectation (a case that cannot fail, or one that pins a known miss)."))

# ---- adversarial new shapes (critics / scouts) ----
ADV = [
 ("AdvPureShapes", "critic", "Write >= 25 NEW pure-data / formatter / logging shapes not in the suite (comprehensions, starred unpacking into tuples, f-strings, dict values, nested defs returning argv, typing.cast, copy.deepcopy, sorted keys, enum members, dataclasses.replace, logging.info, textwrap.dedent ...) and scan them with the final tool: every row on pure data is a precision counterexample."),
 ("AdvRecallShapes", "critic", f"Write >= 25 NEW real-execution shapes (spawn via aliases, getattr(subprocess,'run'), importlib.import_module('subprocess'), os.system via from-import alias, nested helpers, decorators that wrap, class __call__, contextlib, threading targets, asyncio.gather of create_subprocess_exec) and scan with {HARM[:7]}, {PRE[:7]} and {TOOLC[:7]}: any shape {HARM[:7]} or {PRE[:7]} found that {TOOLC[:7]} misses is a recall regression."),
 ("AdvLeadMarks", "critic", "Find shapes where the final tool marks `observed` although no executing body is visible, or `lead` although the body is visible in the same file (cross-cell defs after a reset, redefinitions, imports shadowing defs, star imports, exec/globals tricks). Scan and report each mis-mark."),
 ("AdvVcsForms", "critic", "Attack E4 with forms outside the suite: short clusters (`git add -nv`, `-An`, `git commit -an`), `--no-dry-run`, `--dry-run=false`, `git -c alias.x=commit x`, `git commit --porcelain -m x` (dry), `git push --porcelain -n`, `jj --help describe`, `jj describe -h -m x`, `jj util exec`, `jj git push --dry-run --ignore-working-copy` order variants, eval-surface lists. Measure each in a fresh /tmp repo (HOME redirected) and compare with the final tool."),
 ("AdvCrash", "critic", f"Fuzz the {TOOLC[:7]} tool for crashes (exit 2 / internal errors) with odd transcripts: JS cells, reset cells, non-dict arguments, huge cells, deep recursion (helpers calling helpers 50 deep), self-recursive defs, mutual recursion, syntax errors, async comprehensions, walrus, match statements, lambdas in defaults. Every exit 2 on a well-formed transcript is a regression vs {HARM[:7]}."),
 ("AdvDepth", "scout", "Probe the depth-4 helper resolution boundary and the **kw/starred forwarding rules of the final tool: chains of 3/4/5/6 visible helpers, kwargs splats, defaults; report where an observed command silently disappears (no row and no unparsed_spawns increment)."),
]
for n, role, b in ADV:
    X(I(n, role, b + f" Fixtures in {W}/{n}/ (never executed; --scan only).", own=False))

# ---- mutation testers ----
X(I("MutEvidence", "mutation-tester", f"Mutation-test the evidence marker and lead path of the {TOOLC[:7]} tool (copy to /tmp): ~12 mutants (always observed, always lead, drop lead rows, dedup key without evidence, pure-set additions/removals, reset not clearing bindings); run tw-precision (your clone, --suite-rev {SUITE[:7]}) and the 11 suites per mutant. Survivors = gaps."))
X(I("MutBinding", "mutation-tester", f"Mutation-test the binding guard of the {TOOLC[:7]} tool: builtin exemption ignoring rebinding, del not unbinding, cross-cell carry broken, parameter callee not lead, attribute-call leads re-enabled, class-body deferral restored; run the counter + suites per mutant; survivors = gaps."))
X(I("MutVcs", "mutation-tester", f"Mutation-test the git/jj help/dry-run carve-outs of the {TOOLC[:7]} tool: exempt any -n, exempt after dedup, exempt `jj git push --dry-run` without --ignore-working-copy, ignore value options, drop the --help argv[1] rule; run counter H family + r19-vcs suite per mutant; survivors = gaps."))
X(I("MutIsolationCheck", "mutation-tester", f"Mutation-test {R}/isolation-check.sh itself (copy to /tmp): weaken it (skip a mode, treat SKIP_AS_SUCCESS as pass, forget the stub-invocation marker, accept exit 0 without canary) and show whether running it on {R}/evidence/inns-r19-shape.sh and the four mutants still reads red; canary payloads only."))

# ---- source reopen (scouts) ----
SRCS = [("ReopenGitDocs", "S099, S100, S101"), ("ReopenGitSource", "S102"), ("ReopenJj", "S103, S104"),
        ("ReopenPyDocs", "S105, S106"), ("ReopenPyShlexSub", "S107, S108"), ("ReopenUnshare", "S109, S112"),
        ("ReopenBash", "S110"), ("ReopenExecModel", "S111")]
for n, ids in SRCS:
    X(I(n, "scout", f"Re-open SOURCES rows {ids} ({LANE}/corpus/SOURCES.md) and their Gate lines in {LANE}/corpus/lessons/round-20.md: fetch each pinned URL, compare sha256 with the row/receipt ({R}/fetch/*/receipts.jsonl), check the located quote verbatim at the stated lines and <= 25 words, and the tag→commit pin (`git ls-remote`). Does the row support what the knowledge note and SKILL say it supports?", own=False))

# ---- prose and criteria review (reviewers / critics) ----
PR = [
 ("RevLessonMistakes", "reviewer", f"Check every row of `## Mistakes` in {LANE}/corpus/lessons/round-20.md: evidence pointer resolves, captured-by honest, the fix shown able to fail (red receipt exists and is red)."),
 ("RevLessonCorrections", "reviewer", f"Check `## Corrections to round 19` and `## Decisions` in {LANE}/corpus/lessons/round-20.md against the closure ({SPOT}) and committed bytes: 8/13, 6/13, five S090-only files, 154, nine/eight, 25 dead seats (registry join), 8 r20_edit cases."),
 ("RevLessonGate", "reviewer", f"Check `## Gate` in {LANE}/corpus/lessons/round-20.md against CORPUS.md SOURCES contract v1 ({FLEET}/CORPUS.md): URL, access date, <= 25-word located quote per new row; row counts 98 → 112, tier and status tallies; old→new logging."),
 ("RevScorecard", "reviewer", f"Check SCORECARD.md sections 'Round 20 — declared claims', 'pre-measurement corrections', 'committed results' ({LANE}/SCORECARD.md tail): every number re-derivable by its cited command at its named commit; anything stated as pending?"),
 ("RevKnowledgeNote1", "reviewer", f"Verify §1 (row meanings, name binding) of {LANE}/corpus/knowledge/tripwire-precision-r20.md claim by claim with --scan probes against the {TOOLC[:7]} tool and the cited case names."),
 ("RevKnowledgeNote2", "reviewer", f"Verify §2 (git/jj table) of {LANE}/corpus/knowledge/tripwire-precision-r20.md row by row: measure in a fresh /tmp repo (HOME redirected) and scan with the {TOOLC[:7]} tool; and the cited S rows' lines."),
 ("RevKnowledgeNote3", "reviewer", f"Verify §3 (fail-closed harnesses) and Limits of {LANE}/corpus/knowledge/tripwire-precision-r20.md, plus its header (source/verified-at/recheck) against SOURCES rows."),
 ("RevSkill", "reviewer", f"Verify the round-20 SKILL subsection ({LANE}/SKILL.md, grep 'Reading tripwire rows') sentence by sentence against the {TOOLC[:7]} tool and the suite; and list older SKILL sentences (tool docstring summary, registry rows mado-tripwire / mado-tw-recall) now false."),
 ("RevDocstring", "reviewer", f"Read the docstring of tools/mado-tripwire.py at {TOOLC[:7]} and test each limit/claim with --scan probes; flag every sentence false for the code (e.g. lead/observed rules, help carve-outs, what stays unanalysed)."),
 ("RevQuality29", "critic", f"Attack QUALITY 29 ({LANE}/corpus/QUALITY.md tail): restatement of any 1–28? red real and reproducible? check able to fail? limits honest (isolate.sh not a sandbox)?"),
 ("RevQuality30", "critic", f"Attack QUALITY 30 (detector precision evidence) and the pre-measurement correction that replaced registered criterion 30 (SCORECARD 'Round-20 pre-measurement corrections'): is it a target-preserving swap (R19-V1)? Is its red independent of C1? Would the honest C2 reading be 21/29?"),
 ("RevCrit10Application", "reviewer", f"Check the 'Round-20 application of criterion 10' paragraph in {LANE}/corpus/QUALITY.md and {R}/tally-claims.json: does every red/green entry point at the exact sentence, rule and revision it claims?"),
 ("RevSuiteEdits", "critic", f"Attack the 8 `r20_edit` changes in {R19}/tripwire/r19-helperfn/expected.json and r19-bashcvar/expected.json (git diff 4362219~3..{TOOLC[:7]} or {SUITE[:7]}..{TOOLC[:7]}): is each reason true Python semantics (cite docs), or a test edited to fit the tool? Did any case lose a finding or a negative control?"),
 ("RevToolDiffEval", "reviewer", f"Code-review `git diff {SUITE[:7]} {TOOLC[:7]} -- tools/mado-tripwire.py` for classify_eval, binding environments and scan_file: unbound variables, state leaking across files, reset handling, exceptions swallowed into clean verdicts."),
 ("RevToolDiffLeads", "reviewer", f"Code-review the same diff for spawn_scan / helper resolution / lead emission / dedup: can a lead be emitted twice, an observed row be lost by dedup, or a pure call produce a lead?"),
 ("RevToolDiffVcs", "reviewer", f"Code-review the same diff for classify_git / classify_jj and the per-segment help/dry-run exemption: value-option tables, `--` handling, alias verbs, the dedup ordering."),
 ("RevReadme", "reviewer", f"Check the new corpus/README.md coverage row and frontier bullet (round 20) and that the navigation check (as run by {R}/harm-watch.sh) still passes."),
 ("RevLog", "reviewer", f"Check the LOG.md round-20 entry against commits e629f73..{TIP[:7]} and the receipts: every number, hash and wave fact."),
]
for n, role, b in PR:
    X(I(n, role, b))

# ---- critics on claims overall ----
CC = [
 ("CriticC1Final", f"Is C1 (29/175 → 172/175, target 175/175 missed by 3) an admissible improvement with no harm? Weigh the guards, the 8 suite edits, the 3 failing cases, the held-out 0/12, and the missing corpus diff."),
 ("CriticC2Final", f"Is C2 (20/28 → 22/30) discernment or count inflation after the pre-measurement swap? What verdict and wording would a non-author closure give (R19-V1)?"),
 ("CriticHonestyFinal", f"Read the lesson, SCORECARD round-20 sections, LOG, note and SKILL subsection: list every overclaim (e.g. 'precision restored', 'no host probe', 'all-pass') with replacement wording."),
 ("CriticHarmAxes", f"Which owned axis could round 20 have harmed (coverage V 6/6, U 7/7, navigation, depth, adjacency, freshness)? Run `python3 {R17}/measure.py {TIP[:7]}` c2 and the navigation block; name any harm."),
]
for n, b in CC:
    X(I(n, "critic", b))

# ---- sentinels ----
X(I("SentinelPostWaveScan", "sentinel", f"Post-wave seat scan for wave 1: run the {TOOLC[:7]} tool (`--scan`, no --permit) over the round-20 wave-1 transcripts (find {SESS} -path '*MadoR20*' -name '*.jsonl', excluding this wave's own) and report counts by class and evidence, every host_mutation/package_query/live_probe row with its command and verdict (fixture text vs issued command), and the pacman.log window (file bytes, last transaction time). Remember: scripts written then run are invisible to the scan."))
X(I("SentinelCommitSet", "sentinel", f"Secrets/privacy scan of every file landed in commits e629f73..{TIP[:7]} (`git diff --name-only 1f7f995 {TIP[:7]}` → copy committed bytes to /tmp): run gitleaks with a pinned config plus the pattern checks in {R}/w1/reports/SentinelFixtures.md (copied transcript lines, IPs, emails, tokens). Report file:line only, never the matched text."))

# ---- scribes ----
SB = [
 ("ScribeWaveAccounting", f"Compile wave accounting for round 20 wave 1 from {R}/w1/assignments.json, {R}/w1/reports/swarm-registry.json and {R}/w1/reports/: seats per role, reports present per member (join by name), dead seats (none expected), task-result attempts. Into ONLY {W}/ScribeWaveAccounting/accounting.md."),
 ("ScribeW1Dispositions", f"Build a table of every wave-1 critic/reviewer/sentinel finding ({R}/w1/reports/Critic*.md, Rev*.md, Sentinel*.md, Conn*.md) → L1 disposition visible in the landed files (fixed / kept as limit / not acted on) with pointers. Into ONLY {W}/ScribeW1Dispositions/table.md."),
 ("ScribeShonen", f"Draft the round-20 SHONEN report lines from {LANE}/SHONEN.md ([x] only with a named non-author verifier — none exists in-round; [~] with a resolvable pointer). Into ONLY {W}/ScribeShonen/shonen.md."),
 ("ScribeTrendDraft", f"Draft trend verdicts (expansion, quality, discernment) for the round-20 report with evidence pointers, following {FLEET}/../kimi-shokunin/skills/shokunin/protocol/LEARNING.md if present (else {FLEET}/MISSION.md). Into ONLY {W}/ScribeTrendDraft/trends.md."),
]
for n, b in SB:
    X(I(n, "scribe", b, own=False))

# ---- connectors / revengers / simplifier ----
X(I("ConnConsumers", "connector", f"Who consumes mado tripwire verdict JSON outside the lane ({FLEET}/scripts, {FLEET}/.ufo, sibling lanes)? Would `evidence` keys or the new counts break any consumer? Cite path:line."))
X(I("ConnQueueClose", "connector", f"Map R19-V1..V6 ({SPOT} §Routed defects) to the landed round-20 artifacts at {TIP[:7]}: closed / kept open with reason / unowned; include the R19-V5 keep-open tail (worktree ledger, harm-watch provenance, anchor-alias limits)."))
X(I("RevengeEnvBug", "revenger", f"Reverse-engineer how the UnboundLocalError on JS eval cells entered TwRuleB v2 ({R}/w1/patches/TwRuleB-v2.patch vs TwRuleB.patch) and whether any other variable in scan_file/classify_eval can be unbound on a rare branch at {TOOLC[:7]}."))
X(I("RevengeSuiteNegatives", "revenger", f"For each of the 8 r19 cases edited in round 20, reconstruct why round 19 pinned it clean ({R19}/w1/reports/TwHelperFn*.md, TwBashCVar*.md, TwMerge*.md): was the round-19 expectation a deliberate conservative choice the round-20 contract now overrides, or an error?"))
X(I("SimplifyFinal", "simplifier", f"At {TOOLC[:7]}, list dead code, duplicated logic and unused constants in tools/mado-tripwire.py introduced or left by the round-20 patches; estimate deletable lines; no edits."))
X(I("SentinelHarnessNote", "critic", f"Attack {R}/isolate.sh as documented (SKILL round-20 subsection, QUALITY 29 limit): could a future seat read 'passes the check' as 'safe to run hyprctl inside'? Propose the exact warning text and any cheap guard (refuse non-/tmp targets, scrub env)."))

spec = {"wave": "mado-r20-w2", "context": CONTEXT, "reportDir": ".ufo/waves/round-20/w2/reports",
        "maxLanes": 100, "items": items}
out = pathlib.Path(R) / "w2" / "spec.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(items), collections.Counter(i["role"] for i in items))

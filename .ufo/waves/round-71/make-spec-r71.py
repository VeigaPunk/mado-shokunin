#!/usr/bin/env python3
"""Build the round-71 wave spec (ONE v1 wave, 13 seats). Deterministic; no network, no host writes."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE_DIR = LANE + "/.ufo/waves/round-71"
DECL = WAVE_DIR + "/claims-declaration-r71.md"
FREEZE = "4a91c644289437b588881a7254481157decfa450"
INSTR = "8e78a4ee82f6ccdc951faf531438178a9d12245e"
BASE = "c354f4d410b829d985b31560af9202d98655dad0"

GOD = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = GOD + """

Round mado 71, ONE v1 wave (13 seats). Axes: calibration (C1) and operability (C2). The L1 holds the planner seat (the validator rejects a planner role); no planner is dispatched.

Read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-71/claims-declaration-r71.md FIRST. Claims, predicates, control set, scenario texts and targets are FROZEN at """ + FREEZE + """ (base """ + BASE + """). Never re-scope, never narrow a target after seeing data, never invent a different counter, never edit the declaration, the control JSON or the baseline receipts.

Lane repo (absolute): /home/vgpnk/Projects/shokunin/mado-shokunin. The scored instruments are committed at """ + INSTR + """:
  quality/counters/c1-r71-landing-controls.py   (successor harness; M-Z credit follows the parsed failed summary whatever the exit status)
  quality/counters/c1-r71-real-children.py      (C1 counting command; real bash fixture lane, four modes: liar-success / stderr-genuine / liar-kill / crash-stderr)
  quality/counters/c2-r71-shapes.py             (C2 counting command; held round-70 rule + dict-call splat, splat-through-alias, store-through-alias, attribute-through-second-object)
Frozen evidence: .ufo/waves/round-71/controls/c2-controls-r71.json (23 cases, sha256 d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df), .ufo/waves/round-71/control-baseline-c1-r71.txt, .ufo/waves/round-71/control-baseline-c2-r71.txt, .ufo/waves/round-71/measurement-r71.txt, .ufo/waves/round-71/fetch/ (the two source snapshots).

Write ONLY your own seat directory /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-71/w1/<your-name>/ — drafts of production files go under draft/<repo-relative path> inside it; the L1 integrates them and you never write a production path. Reading sibling seat dirs is allowed. Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mado-shokunin — write it at /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>.

Scratch: /fast/scratch/hyaku/mado-r71/<your-name>/ (mkdir -p first) with delete-on-exit (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree(dir, ignore_errors=True)` in Python). Never rely on an inherited TMPDIR, never write /tmp or /var/tmp. Report the scratch removed before you yield.

Never commit, push, stage, stash, checkout, switch, reset or run any mutating git/jj command in the lane, the fleet repo /home/vgpnk/Projects/shokunin, or any sibling lane. Never write the fleet repo, another lane, MANIFEST.json, .ufo/state, .scratch, or operator config. Fixture git repos: `D=$(mktemp -d "$S/fixture.XXXX")`, `git -C "$D" init -q`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit, name `-C "$D"` on every git call, and use an explicit `-c user.name=... -c user.email=...` identity. Never probe, connect to, write or control a compositor surface, service, socket, session or package manager; this round has NO desktop probe at all.

Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). PACMAN IS PAUSED host-wide: no pacman transaction (-S/-Sy/-Syu/-U/-R, no service restart); use uv tool / npx / an official binary into ~/.local/bin, or name the need in your report and continue.

No credential material, session tokens, cookies or op:// refs in any artifact. No screenshots. Never message agent://all. Yield a concise report: findings, exact commands, exit codes, absolute paths, sha256 of drafts. No prose padding."""


def prompt(name, body):
    return (GOD + "\n\nYour name: " + name + ". Your only write directory: " + WAVE_DIR
            + "/w1/" + name + "/. Scratch: /fast/scratch/hyaku/mado-r71/" + name + "/.\n" + body)


ITEMS = []

ITEMS.append(("R71ExecC1Real", "executor", """Drive claim C1's counting command end to end and report what actually happens (do not edit the committed instruments).
  python3 -I quality/counters/c1-r71-real-children.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev """ + INSTR + """ --base-rev """ + BASE + """ --scratch-root <your scratch>/c1
(the counter refuses /tmp-family scratch roots; run it with --scratch-root under /fast/scratch/hyaku/mado-r71/R71ExecC1Real/). Record rc, the four MADO_R71_SCENARIO lines and the contract line; diff them against the frozen receipt .ufo/waves/round-71/measurement-r71.txt section C1 (must be identical in substance; fixture revs differ per run).
Then attack the harness decision, read-only: copy quality/counters/c1-r71-landing-controls.py into your seat dir and try to construct a scenario input where the successor harness credits a kill that the frozen predicate would refuse, or misses a kill the predicate demands. You may run edited copies from your scratch against the counter's fixture modes (extract the fixture by running the counter with a scratch root and reusing its printed fixture lane shas; do not modify lane files). State for each probe: input, observed mz, expected per the frozen sentence (declaration section C1, kill rule), verdict.
Deliver a findings file with every command, rc, and the exact lines; name any divergence from the frozen sentence."""))

ITEMS.append(("R71ExecC2Shapes", "executor", """Drive claim C2's counting command and stress its classifier (do not edit the committed instrument).
  python3 -I quality/counters/c2-r71-shapes.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev """ + INSTR + """ --base-rev """ + BASE + """ --controls .ufo/waves/round-71/controls/c2-controls-r71.json --scratch-root /fast/scratch/hyaku/mado-r71/R71ExecC2Shapes/c2
(run it with cwd = the lane repo). Record rc, the base-leg lines for the four new carriers and both negatives, the base summary line, and the contract line; compare against .ufo/waves/round-71/measurement-r71.txt section C2.
Then stress the classifier read-only: write small Python sources in your scratch that are NEAR the four new shapes but should stay unguarded (for example: a dict(**M) splat where M loses the key through a later rebinding; a store-through-alias whose alias is rebound between store and call; an attribute edge cfg.runner = runner where the store happens after the call; a splat-through-alias of a module mapping that a second module-level statement rebinds) and near-guarded shapes you think the rule over-accepts. Run each through `python3 -c "import runpy; m=runpy.run_path('quality/counters/c2-r71-shapes.py'); print(m['classify'](src))"` equivalent (import via runpy in your scratch) and check reader/guard against the frozen rule (declaration C2, 'Rule (frozen)'). Report every disagreement with the source, the expected classification per the frozen sentence, and the observed one.
Deliver a findings file with commands, rc, per-case tables and the final contract line."""))

ITEMS.append(("R71ExecCadence", "executor", """Harm-watch and standing-instrument battery for round 71 (read-only; no production edits).
At the lane repo, cwd = /home/vgpnk/Projects/shokunin/mado-shokunin, scratch under /fast/scratch/hyaku/mado-r71/R71ExecCadence/:
1. bash tools/mado-verify.sh --selftest  (expect rc 0 and MADO_SELFTEST n/n; record n).
2. python3 quality/counters/c1-r70-real-children.py --repo . --rev HEAD --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root <scratch>/r70c1  (the FROZEN round-70 counter must stay TARGET_MET at the round-71 tip; the round-70 harness/classifier files must be byte-identical to their round-70 forms — verify with git log --follow --oneline -- quality/counters/c1-r70-landing-controls.py and the same for c2-r70-carriers.py).
3. python3 quality/counters/c2-r70-carriers.py --repo . --rev HEAD --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root <scratch>/r70c2  (must stay TARGET_MET).
4. quality/landing-counters.sh default-path demonstration, both legs: (a) RED-before: bash quality/landing-counters.sh --repo . --rev HEAD --round 70 --scratch-root <scratch>/lc-red  (expect rc 2, 'citecheck path missing' — the routed standing-instrument wart); (b) the round-71 receipts dir does not exist yet, so note that the round-71 default goes green only once the L1 commits .ufo/waves/round-71/receipts/ — record both observations verbatim.
5. python3 quality/check-axis-scores.py (record its verdict lines), python3 quality/check-tool-ledger.py --repo . --rev HEAD (it is EXPECTED to be red on the three new instruments until the L1 lands their ledger rows — record that as the round's own working state, not a harm), and python3 quality/check-index.py --repo . --rev HEAD (83/83 at HEAD; will move to 85/85 after the round's entries land — record both facts).
6. python3 quality/check-deliverables.py over the round-71 w1 seat reports if the tool supports a --round/--paths form (read its usage first); the r69 red state is pre-existing and not this round's harm — name it, do not repair.
Deliver one file (`cadence-r71.txt`) with every command, rc and the exact lines, plus a summary naming: which legs are green, which are red for reasons that predate this round or await the L1's landing commits, and what the L1 must re-run at the final measured content."""))

ITEMS.append(("R71ScribeEntryC1", "scribe", """Draft the claim-C1 knowledge entry at <your dir>/draft/corpus/knowledge/kill-credit-exit-disagreement-r71.md.
Read first: .ufo/waves/round-71/claims-declaration-r71.md (C1), .ufo/waves/round-71/measurement-r71.txt, .ufo/waves/round-71/control-baseline-c1-r71.txt, and the existing sibling entries corpus/knowledge/landing-kill-credit-real-children-r70.md and corpus/knowledge/landing-kill-credit-paired-r69.md (match their structure and discipline; corpus rule: every count carries its command; every quote carries its location).
Content: what changed in the kill-credit rule this round (mz_killed = summary_shows_failure(out), the exit status no longer gates the credit), the four real-child scenarios with their fixture semantics, the before/after numbers with the exact counting command, why the exit status cannot carry the assertion result (held ground S441/S435 vocabulary: one status, many causes), and the new superseding source row S442 (its URL, sha256, located quotes with line numbers — quote A subprocess.rst:53 'If capture_output is true, stdout and stderr will be captured.' and quote B :54-55 'the internal Popen object is automatically created with stdout and stderr both set to PIPE'; fetch receipts in .ufo/waves/round-71/fetch/subprocess-rst-v3.14.8.bin, sha256 05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd, 61,603 bytes).
Open with the provenance trio (source:, verified-at:, recheck:). source: cites S442 and S435 with the URL and anchor. Every S### mention carries a locator that quality/check-anchor-cover.py accepts (read that check's docstring for the grammar). Disclose the limits: forged failing summaries are byte-indistinguishable from genuine ones; the four scenarios are a named set.
Report wc -l, sha256, the ids you cite."""))

ITEMS.append(("R71ScribeEntryC2", "scribe", """Draft the claim-C2 knowledge entry at <your dir>/draft/corpus/knowledge/guard-carrier-shapes-r71.md.
Read first: .ufo/waves/round-71/claims-declaration-r71.md (C2), .ufo/waves/round-71/measurement-r71.txt, .ufo/waves/round-71/control-baseline-c2-r71.txt, and the sibling entry corpus/knowledge/guard-carrier-shapes-r70.md (match structure; every count carries its command; every quote its location).
Content: the four new carrier shapes (dict-call splat, splat-through-alias, store-through-alias with its rebinding dominance, attribute-through-second-object with its one-edge resolution and replacement dominance), each with the frozen case src (from .ufo/waves/round-71/controls/c2-controls-r71.json, names dict-call-splat, dict-call-splat-object-alias, store-through-alias-two-hop, attribute-second-object) and the two negatives (unguarded-dict-splat-negative, env-call-no-key-negative), the before/after numbers with the exact counting command (19/23 -> 23/23 against the held round-70 rule), and the new superseding source row S443 (expressions.rst section Calls, quote at :1415-1417: 'If the syntax **expression appears in the function call, expression must evaluate to a mapping, the contents of which are treated as additional keyword arguments.'; fetch receipt .ufo/waves/round-71/fetch/expressions-rst-v3.14.8.bin, sha256 e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a, 92,034 bytes).
Open with the provenance trio (source:, verified-at:, recheck:); source: cites S443 and the held S438/S439 with locators. Disclose the bounds: one alias hop, one object-alias edge, exact dotted names, no container flow, no path-sensitivity beyond a literal-false branch; the deeper-chain and mid-chain-rebinding regressions stay pinned False in the counter selftest.
Report wc -l, sha256, ids cited."""))

ITEMS.append(("R71ScribeRowLesson", "scribe", """Draft three artifacts.
A) <your dir>/draft/corpus/lessons/round-71.md — the round-71 lesson skeleton in the exact shape of corpus/lessons/round-70.md (Outcome and boundaries / Mistakes / Gate / Wave findings placeholders). Mistakes must include: M71-1 the routed round-70 uncommitted seat reports (committed this round under the round-71 entry at c354f4d4, class 'record order across rounds', captured-by 'none at r70 — the closure's step-1 uncommitted-work check caught it', fix 'the round commits inherited lane-authored files before the freeze'); M71-2 the standing landing-counters default --citecheck-paths wart (class 'instrument default unusable', captured-by 'none — the r70 cadence finding routed it', fix 'the round commits receipts at .ufo/waves/round-71/receipts/ so the --round 71 default resolves; red-before receipts at the r70 default'); and any L1-visible defect you can ground in the committed evidence (label candidates clearly). Gate section: S442/S443 admit blocks with URL, access date 2026-11-04, sha256, located quotes with line numbers (quote text given in the entry-draft items), and a reject block for Doc/library/stdtypes.rst (reason: the mapping-methods page documents method behavior, not call/expression semantics; the language reference is the tier-A surface for these claims; flip: a claim about dict method behavior re-opens it).
B) <your dir>/draft/corpus/SOURCES-rows-r71.md — the two registry rows S442 and S443 as full 11-column table rows matching the shape of S439/S440 in corpus/SOURCES.md (status mined, opened 2026-11-04, recheck 90d, used-by naming draft corpus/knowledge/kill-credit-exit-disagreement-r71.md and corpus/knowledge/guard-carrier-shapes-r71.md and corpus/lessons/round-71.md), plus the exact old->new used-by cell for S108 and S439 if the row grammar needs the superseding pointer (read CORPUS rule 2 first; superseding rows are new rows, the held rows' cells do not change — state that explicitly).
C) <your dir>/draft/corpus/QUALITY-addendum.md — numbered criteria continuing the file (114, and 115 if warranted) in the grammar of 108-113: normative sentence, 'Shown able to fail' with a real red state and receipt path, Limits clause. Ground them on M71-1 (inherited lane-authored files are committed or reverted by the next round before its freeze) and, if groundable, on M71-2 (an instrument's default path must resolve against committed bytes or the instrument must refuse before running legs).
Report wc -l and sha256 of each draft."""))

ITEMS.append(("R71ScoutSources", "scout", """Independent source opening for both claims' sourced ground.
Fetch each URL three times (curl -fsSL), byte-compare all copies, and verify against the held pins:
1. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst — expect sha256 05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd, 61,603 bytes (held row S108's recorded digest — verify by reading S108's row in corpus/SOURCES.md). Locate the capture_output sentences and record their exact line numbers and a <=25-word quote.
2. https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst — expect sha256 e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a, 92,034 bytes (held row S439's digest). Locate the Calls-section ** sentence (:1415-1417 expected) and record quote + lines.
Also: read corpus/SOURCES.md rows S108 and S439 in full and confirm the supersede mechanics (CORPUS.md rule 2: a correction is a NEW row whose teaches opens 'supersedes SNNN —'; the held rows' cells do not change); screen the reject candidate https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/stdtypes.rst (mapping-methods page) against the claims' subject and give an admit/reject recommendation with reasons.
Deliver sources-r71.json (url, sha256, bytes, http rc, quote line numbers, quote text, verdict) plus a short report. Read-only throughout; fetches go to your scratch."""))

ITEMS.append(("R71ScoutCensus", "scout", """Frontier-step reconnaissance for round 71 (read-only).
At the lane repo: run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado and record the full output and exit code (the before-state receipt; expected exit 0). Count rows: grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md (expect 378) and the tier/status histograms via the CORPUS.md census commands. Verify no id collision for S442/S443 (the highest existing id) and that corpus/README.md's knowledge index lists 83 notes (the round will add two entries -> 85).
Read corpus/README.md's Frontier section and corpus/lessons/round-70.md's planned intent; report in one paragraph whether the round-71 claims sit on the lane's held lane-tooling ground (the r67-r70 instrument family) and what frontier row the L1 should append (a round-71 entry naming the exit-status-disagreement kill credit and the four carrier shapes).
Deliver a findings file with exact commands/outputs and the one-paragraph frontier verdict."""))

ITEMS.append(("R71RevC1", "reviewer", """Adversarial review of claim C1 (calibration): the exit-status-disagreement kill credit. Attack it; do not build it.
Read the declaration C1 section, the counter and harness at """ + INSTR + """, the measurement receipt, and the baseline receipt. Attack lines: (1) the doctrine — is crediting a kill on a summary alone, ignoring mz_rc, sound? construct the counterexamples (a lane that exits 0 without ever running its assertions but prints a stale failing summary from an earlier run; a wrapper that echoes a captured summary; a lane whose summary lies while rc agrees) and say for each whether the frozen sentence's own words refuse it or admit it; (2) the fixture semantics — run the four fixture modes directly (extract the LANE_TEMPLATE from the counter, build the modes in your scratch, bash-run them, capture stdout/stderr/rc separately AND combined) and check the expectation table against what a combined-output reader sees; (3) the base leg — confirm the do-nothing control really misses liar-success and only it; (4) the frozen-sentence fidelity — does the counter's contract line and the verdict predicate match the declaration's frozen sentence exactly?
Deliver a verdict 'C1 predicate sound as bounded' or 'unsound', findings by severity with file:line and repro commands, and the residual limits the report must disclose."""))

ITEMS.append(("R71RevC2", "reviewer", """Adversarial review of claim C2 (operability): the four new carrier shapes. Attack it; do not build it.
Read the declaration C2 section, quality/counters/c2-r71-shapes.py at """ + INSTR + """ (diff it against quality/counters/c2-r70-carriers.py to isolate the widened rules), the frozen 23-case set, the measurement and baseline receipts. Attack lines: (1) per new shape, a dominance bypass (dict(**M) where M is rebound module-level after the splat; splat-through-alias where the alias is rebound; store-through-alias where the handed mapping is rebound between store and call; attribute edge where the store postdates the call or the edge target is rebound); (2) over-inclusion — shapes the widened rule now calls guarded that the frozen rule sentence refuses (an alias of a mapping that merely mentions the key in value position; an object edge whose target object is unrelated); (3) the census — confirm population=20 readers=13 guarded=13 unguarded=0 is re-derived at the tip and the widened classifier reclassifies no production file; (4) frozen-sentence fidelity and the base leg (held rule 19/23, missing exactly the four carriers).
Deliver a verdict 'C2 predicate sound as bounded' or 'unsound', findings by severity with file:line and repro commands, and the residual limits the report must disclose."""))

ITEMS.append(("R71CriticClaims", "critic", """Falsify both frozen claims without building them (read the declaration, the receipts, the instruments at """ + INSTR + """).
Attack lines: freeze order (declaration + controls + baselines must land strictly before any candidate data — check the commit graph and committer timestamps of 4a91c644 vs 8e78a4ee); do-nothing-control reachability (a do-nothing control misses the target, but is the target reachable by a substitute artifact that does less work than the delivered instrument? state the substitute for each claim and what it scores); causal separability (C1's files vs C2's files; does either counter read the other's artifacts?); counting-command fidelity (run both counting commands yourself from the lane repo with scratch under /fast/scratch/hyaku/mado-r71/R71CriticClaims/ and compare every line against .ufo/waves/round-71/measurement-r71.txt); bounded-score arithmetic (10 x 4/4 and 10 x 23/23; before values 0.0000 with base 3/4=7.5000 and 19/23=8.2609); axis naming (C1 calibration, C2 operability — name the surface each changes per the declaration); and the declaration's not-claimed list vs what the receipts actually prove.
Report blockers B1..Bn with file:line and a reproduction command; no prose verdicts without evidence."""))

ITEMS.append(("R71MutBattery", "mutation-tester", """Independent mutation testing of the round-71 instruments (scratch only; never edit lane files).
Copy quality/counters/c1-r71-real-children.py, quality/counters/c1-r71-landing-controls.py and quality/counters/c2-r71-shapes.py into your scratch. For each, design at least six mutants that flip a decision (examples: restore the rc conjunct `mz_rc != 0 and` in the harness; drop the store-before-use check in attribute_flow; drop the blockers check in alias_store_guard; make splat_aliases accept any name; make verdict_met ignore base_controls; swap EXPECT for liar-success; make load_controls skip the digest check). Run each mutant's --selftest and record killed/not: a mutant is KILLED iff the selftest exits nonzero or prints a failing assertion line naming it; also run (for the two counters) one measurement against the committed revisions where cheap, and record the printed-line effect. Every survivor is a named residual with its diff digest and a one-line flip condition.
Report a kill matrix (mutant, selftest killed?, printed-line effect, survivor iff), and a scratch-cleanup receipt. No universal fault-coverage claim."""))

ITEMS.append(("R71ConnSiblings", "connector", """Cross-instrument overlap scan (read-only; no drafts of production files).
Check sibling lanes' recent corpus and quality work for overlap with this round's two moves: (1) the kill-credit-on-parsed-summary rule (a summary-only decision ignoring exit status) and (2) environment-key carrier classification (dict(**M) splats, alias hops, attribute resolution). Scan: git -C <sibling repo> log --oneline -15 for tameshi, kumitate, kotodama, souji, kake (the mutation/control siblings) and grep their quality/ and corpus/knowledge/ for 'kill', 'carrier', 'summary', 'GIT_NO_REPLACE_OBJECTS', 'env'. Also scan the lane's own corpus/knowledge/ r66-r70 entries for redundancy with the two new entries the round drafts (kill-credit-exit-disagreement-r71.md, guard-carrier-shapes-r71.md) — name any overlap the L1 must disclose as an extension rather than new ground.
Report a table (ground, lane path:line, round-71 rule verdict, action for the L1) and a one-paragraph adjacency verdict."""))


def main():
    doc = {"wave": "w1", "reportDir": ".ufo/waves/round-71/w1", "context": CONTEXT,
           "items": [{"name": n, "role": r, "prompt": prompt(n, b)} for n, r, b in ITEMS]}
    out = os.path.join(WAVE_DIR, "w1-spec.json")
    with open(out, "w") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    roles = {}
    for n, r, _ in ITEMS:
        roles[r] = roles.get(r, 0) + 1
    attack = sum(roles.get(k, 0) for k in ("reviewer", "critic", "mutation-tester", "labrat"))
    print(json.dumps({"seats": len(ITEMS), "roles": roles, "attack": attack,
                      "share": round(attack / len(ITEMS), 3)}))


if __name__ == "__main__":
    main()

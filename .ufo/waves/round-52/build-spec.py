import json
from pathlib import Path
lane='/home/vgpnk/Projects/shokunin/mado-shokunin'; out=Path(lane+'/.ufo/waves/round-52/w1-spec.json')
context=f'''/skill:godspeed
Name axes coverage and operability; iterate cheap and in parallel; keep moves that improve any axis and harm none. No clarification loop.

Goal: mado round 52. Read {lane}/.ufo/waves/round-52/claims-frozen.md and registration.md FIRST. Build/attack only the frozen claims, read source materials, no claim or predicate edits. Lane repo absolute path: {lane}. Base 85d57a818c3707397e21c840b6498b105ba798aa. Axes coverage + operability. L1 is planner; planner task is represented by the L1, not a swarm role. Roles routed by host config, never pass model.

Writes only in each assigned seat dir and its adjacent report in {lane}/.ufo/waves/round-52/w1/. No tracked lane files, fleet, siblings, scripts/templates/state/watchdog, scratch repo, or shokuknow writes. Source repo is read-only, no campaign tools. Absolute paths only; every Report trailer is relative to {lane} and must be written under that root. Seats are leaves, no task/delegation/background jobs. No mutations of git/jj, commits or pushes. Do not install unless needed; tooling authorization: read /home/vgpnk/.omp/agent/RULES.md first, official channels only, PACMAN transactions paused; record any install and reason.

Safety: SKILL.md says this round is source-only: no package queries, live reads (including process/compositor), input capture, screenshots or producer execution. No host/config/service/compositor mutation. Do not fetch from/write to domain checkout; use already locally available sources or web reader if source opened in round. Tool source reads are permitted. All scratch/clone/work under /fast/scratch/hyaku/mado-r52/<SeatName>/ (mkdir, explicit TMPDIR/--work); never /tmp for evidence, clean on exit; check disk guard before heavy work and report ENOSPC, don't retry. Receipt copies go to the seat dir.

Output: create seat report file promptly, list deliverables under ## Deliverables and exact Report trailer, ensure each declared file exists. Include citations, commands/results, limitations, source URL/access date/located quote for any source candidate. Report dissent/failed controls honestly. No report is a vote; attacks must name item/predicate attacked. Round is source-only and one theme; no package adoption from shokuknow unless specifically assigned and re-grounded.'''
items=[]
def add(name,role,task): items.append({'name':name,'role':role,'prompt':task})
add('PlanDataWalk','scout','Planner data-walk: independently derive observations and one-case-overfit risks from committed base. Do not edit tracked bytes. Report claim falsifiability/controls/measurement; inspect SCORECARD/PROVINCE and round-51 spotcheck.')
add('OverlapScan','connector','Cross-axis/overlap scan: compare C1/C2 to each other and round-51/50 proposals; flag duplicate scope or counter contamination and sourced-ground opportunities.')
add('C1CounterDesign','executor','Implement prototype counter + selftest for C1 frozen predicate in seat directory only. Inspect ledger/checker. Ensure non-self, context-bound pointer checks; red control and green production fixture. Runnable, scratch-aware. Report exact command/output; drafts only.')
add('C1ControlAttack','critic','Attack C1 frozen control validity: construct no-work and forgery fixture variants in own directory, identify false-positive bypasses and exact commands/results. No tracked edits.')
add('C2SourceRecon','scout','Recon locally available pinned source on distinct dispatcher behavior beyond round 51. Source-only; identify >=4 propositions, exact source files/anchors, fresh URLs to open, no runtime. Verify PROVINCE boundary and held overlap.')
add('C2EntryDraft','scribe','Draft new distinct dispatcher knowledge entry in seat dir only, using source bytes opened this round. Proposition→source table, quotes <=25 words, URLs/access date/pins/support rationale. Do not edit SOURCES/README.')
add('C2CounterDraft','executor','Draft runnable structural C2 counter/selftest against staged entry/registry fixture. Check proposition mapping/count, row/pin/quote bindings and index path; semantic entailment requires outside review. Scratch explicit; drafts only.')
add('QualitySweep','reviewer','Review claims and round-51 spotcheck for frozen predicate coherence/no-harm/safety. Do not claim outside non-author verdict; this lane seat is lane-author.')
add('MistakeMiner','scribe','Read round-51 lesson and verifier spotcheck; identify actionable mistake class, captured-by criterion and shown-to-fail fix; sweep prior related evidence. Cite exact pointers.')
add('C1Mutation','mutation-tester','Mutation-test C1: production ledger→repeated self-pointer/generic control and further bypasses; exact expected outcomes, draft artifacts only.')
add('C2SourceCritic','critic','Source-truth critique of round-51 entry/held links; identify an independent dispatcher fact surface and attack evidence claims with exact local lines.')
add('AssimilationScan','scout','Inspect latest considerthese proposal 2 and merge/mado presence read-only; determine whether C1 covers proposal and what evidence remains absent; inspect absent-register path if available.')
add('C2PinAudit','reviewer','Audit candidate source pin/proposition matrix when locally available; verify exact quotes/anchors and quote lengths, report unsupported facts; no tracked writes.')
add('C1Simplify','simplifier','Review C1 prototype for YAGNI/maintainability; recommend simplest legitimate check and failing control.')
add('C1Evidence','scribe','Review measurement evidence requirements aligned round-51 lessons; no fabricated output.')
add('C2CoverageCritic','critic','Attack coverage novelty by comparing held corpus/round-51; identify overlap and whether distinct subject exists without widening.')
add('C2EntryQuality','reviewer','Independently inspect locally available source bytes and evaluate candidate entry groundedness; report limits.')
add('C1Fixture','executor','Build minimal C1 red/green fixture harness prototype in own dir; verify exact outputs, scratch argument, no source-tree writes.')
add('C2Novelty','critic','Adversarial overlap check on proposed dispatcher surface using corpus; identify novelty and source-truth deficiencies.')
add('RegistryContract','reviewer','Check planned new source rows/opened quotes and lesson Gate contract; no append until opened/admitted.')
for n in range(1,49):
 role=['reviewer','critic','mutation-tester','scout','revenger','connector'][(n-1)%6]
 target=['C1 self-pointer/context bypass','C1 uniqueness/population falsification','C1 no-work control validity','C1 counter isolation/scratch behavior','C2 source proposition entailment','C2 proposition-map completeness','C2 held-ground novelty','C2 source quote/pin binding'][(n-1)%8]
 add(f'Falsify{n:02d}',role,f'Falsification item {n:02d}, target: {target}. Read frozen claim/registration. Investigate one concrete bypass/failure mode or named control using source bytes/seat-local fixtures; no duplicate generic review; no tracked edits. Report attacked clause, reproducible setup/command, actual result, reproduced yes/no. Own directory {lane}/.ufo/waves/round-52/w1/Falsify{n:02d}/ and adjacent report.')
spec={'wave':'w1','context':context,'reportDir':'.ufo/waves/round-52/w1','items':items}
out.write_text(json.dumps(spec,indent=2)+'\n')

#!/usr/bin/env python3
"""Generates .ufo/waves/round-44/w2-spec.json (33 seats, v1 wave: falsify the landed round-44 data)."""
import collections, json, os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-44"
V2 = "03fa5c618b089064a657b3d79d3d4272ae4b6894"
DATA = "e46789213830597348fe96a351ae004d10587385"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
SCR = "/fast/scratch/hyaku/mado-r44"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in "
    "parallel. Do not output philosophical reasoning or verbose plans. Act "
    "directly via tool calls.\n\n")
SAFETY = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-safety.txt")).read()
CONTEXT = """# Goal
mado round 44 (hyaku run 9, 2026-10-26), inline v1 wave w2 of two (33 seats: FALSIFY the landed data). Lane repo: %(L)s
The round's claims were re-registered before data in %(W)s/registration-v2.md (freeze %(V)s; the v1 registration %(W)s/registration.md
and its counters are superseded and are not the claims' rules). The data commit is %(D)s (base %(B)s). Read registration-v2.md first.
- C1 operability: `tools/mado-geometry.py` (now = %(W)s/c1/ctl-ref-tool-v2.py.txt) reads the client's `fullscreen` integer: FULLSCREEN (2) /
  MAXIMIZED (1) instead of comparing, summary ` maximized=<n> fullscreen=<n>` only when > 0, top verdict NOT_COMPARED (exit 5) when agree=0 and
  a state client matched; round-43 output byte-identical otherwise. Counter quality/counters/c1-r44-geometry-states-v2.py (PRED-C1-r44-v2):
  base `fixtures=11/26 MISSED` -> data `fixtures=26/26 TARGET_MET` (%(W)s/receipts/c1-after-data.txt). Controls %(W)s/receipts/ctl-c1-v2.txt (0 of 20 met).
- C2 coverage (sourced; assimilation): corpus/knowledge/hyprland-gkeep-size-request-r44.md, rows S298-S301 (new) and held S164 (used-by
  extended), lesson corpus/lessons/round-44.md (`## Gate`), README index row + Frontier "Round-44 gkeep size-request route". Counter
  quality/counters/c2-r44-gkeep-size-request-v2.py (PRED-C2-r44-v2): base 0/1 -> data `admitted=1/1 TARGET_MET` (%(W)s/receipts/c2-after-data.txt).
  Controls %(W)s/receipts/ctl-c2-v2.txt (positive P admitted, 10 of 10 do-nothing/forged rejected). Pins: %(W)s/fetch/ (sha256 in receipts/fetch-sha256.txt).
- Also landed at %(D)s: SKILL.md FULLSCREEN/MAXIMIZED/NOT_COMPARED rows + exit-map note + D3 TILED correction (after the verdict table, ~SKILL.md:280-291);
  PROVINCE.md tool-row note; QUALITY.md criteria 82-84; quality/ratio-domain-meta.py (considerthese 2026-10-25 proposal 1); SCORECARD.md and LOG.md Round 44.
- w1 reports (38) are in %(W)s/w1/ - read the ones your item names. Every finding names what it attacks, its severity, and a reproduction.
  A hole you find in a v2 predicate is reported as an OPEN predicate defect (no re-registration after data); a content error in landed
  text is reported with the exact corrected sentence and its computed locator - the L1 decides and lands corrections.
""" + SAFETY


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(V)s", V2), ("%(D)s", DATA), ("%(B)s", BASE),
                 ("%(P)s", PKG), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t.replace("%%", "%")


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({"name": name, "role": role,
                  "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() + "\n")})


C1 = "cd %(L)s && python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo . --rev %(D)s --work %(S)s/<YourSeatName>"
C2 = "cd %(L)s && python3 -I quality/counters/c2-r44-gkeep-size-request-v2.py --repo . --rev %(D)s"
ENTRY = "%(L)s/corpus/knowledge/hyprland-gkeep-size-request-r44.md"

# executors (10)
seat("RerunC1Data", "executor", "Re-run C1's counting command at the data commit.",
     "Run `" + C1 + "` three times (fresh nonces) and once with `--nonce 0000000000000001`; also run the superseded v1 counter "
     "(quality/counters/c1-r44-geometry-states.py, expected MISSED because NOT_COMPARED changed the model - confirm the failing fixtures are exactly the "
     "NOT_COMPARED cases) and the round-43 counter `python3 -I quality/counters/c1-r42-geometry.py --repo . --rev %(D)s` (clause r's no-harm side). "
     "Paste final lines and exit codes; compare with %(W)s/receipts/c1-after-data.txt. Write %(W)s/w2/RerunC1Data.md.")
seat("RerunC2Data", "executor", "Re-run C2's counting command and re-derive every Gate binding independently.",
     "Run `" + C2 + "` twice. Then, WITHOUT importing the counter, re-derive per cited id (S164, S298-S301): the GATE line in corpus/lessons/round-44.md, "
     "sha256 of the receipt at %(D)s (git show), the quote's single word-bounded occurrence and start line, its absence from the other four receipts, the "
     "entry line carrying quote + locator, the registry row (11 cells, location = pin URL), the census lines, and the twelve clause-j surfaces (anchor line, "
     "cited range, keyword). Report any disagreement. Write %(W)s/w2/RerunC2Data.md.")
seat("RerunControlsV2", "executor", "Re-run both v2 control runners and compare with the committed receipts.",
     "Run `python3 -I %(W)s/ctl/run-c1-controls-v2.py --repo %(L)s --rev %(V)s --work %(S)s/RerunControlsV2/c1` and "
     "`python3 -I %(W)s/ctl/run-c2-controls-v2.py --repo %(L)s --freeze %(V)s --base %(B)s --work %(S)s/RerunControlsV2/c2`; diff the verdict columns against "
     "%(W)s/receipts/ctl-c1-v2.txt and ctl-c2-v2.txt (nonces differ; verdicts and clause patterns must not). Write %(W)s/w2/RerunControlsV2.md.")
seat("RerunCensus", "executor", "Census, registry counts and index gates at the data commit.",
     "Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` and compare with "
     "%(W)s/receipts/census-before.txt; count rows at base and data (`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md` via git show) "
     "- expect 234 -> 238; `git diff %(B)s %(D)s -- corpus/SOURCES.md` must be 4 added rows plus S164's used-by cell only; run quality/check-index.py and "
     "quality/check-index-rows.py at %(D)s. Write %(W)s/w2/RerunCensus.md.")
seat("ExecHarmTip", "executor", "No-harm check at the data commit against the base.",
     "In a clone (`git clone -q --shared %(L)s <scratch>`, toplevel verified, checkout %(D)s inside it only) run every tools/* selftest, quality/check-axis-scores.py, "
     "check-index.py, check-index-rows.py, check-locators.py --selftest, and compare with %(W)s/w1/ExecHarmBase/ (base). Every difference is a finding unless "
     "the round intended it (name which). Also `git diff --numstat %(B)s %(D)s` outside .ufo/: is every changed doc append-only except SOURCES S164's used-by "
     "and tools/mado-geometry.py? Write %(W)s/w2/ExecHarmTip.md.")
seat("ExecSeparability", "executor", "Separability of C1 and C2, both directions, on fixture commits.",
     "In a scratch clone at %(D)s: commit (inside the clone only) a revert of tools/mado-geometry.py to the base bytes -> C2 must still be 1/1; separately revert "
     "the entry/rows/lesson/README to base -> C1 must still be 26/26. Run both counters on both fixture commits. Write %(W)s/w2/ExecSeparability.md.")
seat("ExecDoNothingV2", "executor", "Shape-keeping do-nothing controls against both v2 predicates at the data commit.",
     "Build the cheapest variants that keep the landed shapes but drop the claimed content: for C2, the landed entry with every non-required sentence deleted "
     "(keep only header, the five bound claim lines, census lines and the minimal locator lines clause j needs) and variants that keep clause-j locators on "
     "lines whose sentence is false; for C1, the landed tool with the state logic present but the docstring/SKILL untouched etc. Score each (" + C2 + " with "
     "--repo <fixture clone>, and C1 with --tool). Report which reach TARGET_MET (declared residual vs new hole). Write %(W)s/w2/ExecDoNothingV2.md.")
seat("LabNotCompared", "executor", "One falsifiable hypothesis: the landed tool equals the v2 counter's model on 20000 random dumps.",
     "Import quality/counters/c1-r44-geometry-states-v2.py with importlib (never run main); generate >= 20000 random (clients, rules) cases with its "
     "gen_state_clients/old.gen_texts plus your own state-heavy generator (all-state dumps, state+tiled, state+agree, duplicate keys, huge ints), run "
     "%(L)s/tools/mado-geometry.py (python3 -I, files in your scratch) and compare stdout+exit with model_out_states. Report divergences minimised, or the "
     "honest negative with count and seed. Write %(W)s/w2/LabNotCompared.md.")
seat("ExecIndepV2", "executor", "An independent implementation of the v2 contract from the counter docstring only.",
     "Without reading tools/mado-geometry.py at %(D)s or any reference, start from `git show %(B)s:tools/mado-geometry.py` and implement the v2 contract from the "
     "docstring of quality/counters/c1-r44-geometry-states-v2.py (and the round-42 counter's docstring). Selftest k==n>=80 with state assertions. Score with "
     "`" + C1 + " --tool <your file>` (drop --rev's tool). Report every contract sentence that was ambiguous. Write %(W)s/w2/ExecIndepV2.md.")
seat("ExecLocatorSweep", "executor", "Recompute every locator the round wrote in prose.",
     "Run `python3 -I %(L)s/quality/check-locators.py --fetch %(W)s/fetch` and `--fetch %(W)s/fetch-c1` over the entry, corpus/lessons/round-44.md, SKILL.md, "
     "corpus/README.md, LOG.md and QUALITY.md at %(D)s (git show into scratch), and the w1 candidate %(W)s/w1/ExecLocatorTeeth/check-locators.py over the same; "
     "for every MISS open the receipt and give the true line (grep -n). Also check every `file:N` in SKILL.md rows 280-291 by hand. Write %(W)s/w2/ExecLocatorSweep.md.")

# mutation-testers (3)
seat("MutC1V2", "mutation-tester", "Mutate C1 v2's new gates (b5, e, NOT_COMPARED model, setup fixes).",
     ">= 20 single edits to a copy of quality/counters/c1-r44-geometry-states-v2.py (b5 prefix, the rename key, the failure test, INVARIANCE set, env, "
     "timeout, NOT_COMPARED condition, judge_v2). Run each on the landed tool (`--tool %(L)s/tools/mado-geometry.py`) and on regenerated v2 controls "
     "(%(W)s/ctl/run-c1-controls-v2.py VARIANTS). Survivor = a mutant that admits a bad control or rejects the landed tool; classify. Write %(W)s/w2/MutC1V2.md.")
seat("MutC2V2", "mutation-tester", "Mutate C2 v2's tightenings (T1-T4, exact census exemption, clause j).",
     ">= 20 single edits to a copy of quality/counters/c2-r44-gkeep-size-request-v2.py; run each on the data commit (must stay admitted) and on the ten "
     "rejected controls of %(W)s/ctl/run-c2-controls-v2.py (rebuild them in scratch with its functions). Survivors classified equivalent or missing control. "
     "Write %(W)s/w2/MutC2V2.md.")
seat("MutTool", "mutation-tester", "Mutate the landed tool; what do its selftest and the counter kill?",
     ">= 30 mutants of %(L)s/tools/mado-geometry.py concentrated on the round-44 lines (client_fsmode, the verdict chain, the states suffix, NOT_COMPARED). Run "
     "`--selftest` on each, then the counter (`" + C1 + " --tool <mutant>`) on selftest survivors. Report survivors with equivalence proofs or the missing "
     "assertion. Write %(W)s/w2/MutTool.md.")

# critics (7)
seat("CritC1V2Cheat", "critic", "Cheats against PRED-C1-r44-v2.",
     "Build tools that reach TARGET_MET without the capability in real use: detect the b5 json.loads rebinding (identity check, object_hook sniffing) and keep "
     "state logic only when not rebound; detect the unsandboxed env of clause e in other ways; parse JSON without json.loads. Score each with `" + C1 + " --tool <file>`. "
     "Report MET cheats and the tightening. Write %(W)s/w2/CritC1V2Cheat.md.")
seat("CritC2V2Forgery", "critic", "Forgeries against PRED-C2-r44-v2.",
     "In scratch clones of %(D)s build entries admitted by v2 although ungrounded: clause-j locators on lines whose sentence is false (keyword present), a "
     "decision table naming no id that overclaims, census lines true but prose contradicting in words not numbers. Score with the counter (--repo <clone>). "
     "Classify mechanical hole vs declared residual. Write %(W)s/w2/CritC2V2Forgery.md.")
seat("CritEntryHyprland", "critic", "Attack the entry's compositor-side claims (sections 1-2) against the pins.",
     "Read " + ENTRY + " sections 1-2 and the pins %(W)s/fetch/Hyprland-Window.cpp and Hyprland-XDGShell.cpp. For each sentence: supported / overstated / "
     "false, with the computed locator. In particular: the early return condition; 'appends the serial returned by setSize'; whether scheduleConfigure's "
     "serial is the configure's serial; onAck 'drops it and every older pair'; whether the ack 'does not force the next buffer'. Write %(W)s/w2/CritEntryHyprland.md.")
seat("CritEntryClient", "critic", "Attack the entry's protocol/GTK/gkeep claims (sections 3-5 and the predecessor corrections).",
     "Read " + ENTRY + " sections 3-5 and 'What the staged predecessor said'. Against xdg-shell.xml, gdktoplevel-wayland.c and gkeep-ui.py: is 'adopts a non-zero "
     "configured size unless below its minimum' what lines 513-545 and 606-700 say (should_constrain, size_is_fixed, saved size, shadows)? Is gkeep's window "
     "really resizable (layout) so the min-size branch applies? Is 'the ack carries a serial only' exact? Each sentence: verdict + locator. Write %(W)s/w2/CritEntryClient.md.")
seat("CritAssimV2", "critic", "Attack the landed assimilation decisions.",
     "Re-open the staged residue files in %(P)s/knowledge/corpus/knowledge/ and the lesson's Gate/ledger. Is the r12 ADMIT justified (what of r12 survives in "
     "the entry)? Is each REFUSE (r13, r14, r15, r9) reason true and its flip reachable? Does refusing r9 lose its fetchClass link? Write %(W)s/w2/CritAssimV2.md.")
seat("CritClaimSizingV2", "critic", "Post-data claim sizing and honesty of the round's numbers.",
     "Check: no rule changed after data (git log of both v2 counters ends at %(V)s); the after-states equal the registered targets; the SCORECARD/LOG Round 44 "
     "text and the axis publication (navigation 61/61, calibration 71/71) re-derive (`python3 -I quality/check-axis-scores.py --rev %(D)s --repo .`); "
     "universal words in landed text not enumerated; whether QUALITY 82-84 each have a mistake and a fail-able check. Write %(W)s/w2/CritClaimSizingV2.md.")
seat("CritSkillLicence", "critic", "Attack the new SKILL.md licence rows and exit-map note.",
     "SKILL.md rows FULLSCREEN, MAXIMIZED, NOT_COMPARED and the round-44 note: does each 'Licenses' cell claim more than the tool and pins show (e.g. "
     "'the rule's size is not compared', 'only the compositor's internal mode decides', the remembered floating box)? Is the D3 correction right about "
     "pseudo-tiled clients (Window.cpp:2402-2408 at %(W)s/fetch)? Write %(W)s/w2/CritSkillLicence.md with corrected text where wrong.")

# reviewers (7)
seat("RevRows", "reviewer", "Review registry rows S298-S301 and S164's change.",
     "Cell by cell at %(D)s: source/URL serves the pinned bytes (curl + sha256), kind/tier, scope, anchor ranges true (open each range), teaches not "
     "overstated, status/opened/recheck/used-by. S164: only used-by changed (diff). Write %(W)s/w2/RevRows.md.")
seat("RevLesson", "reviewer", "Review corpus/lessons/round-44.md.",
     "Verify the Gate lines, ledger rows, registry log, closure items, Mistakes M44-1..9 (evidence pointers resolve, 'shown able to fail' true or honestly "
     "open), Round-43 errata E1-E4 against round-43 files, the considerthese and quarantine sections. Write %(W)s/w2/RevLesson.md with corrections.")
seat("RevReadmeFrontier", "reviewer", "Review the README index row and the Round-44 Frontier section.",
     "Every claim and locator of the new corpus/README.md index row and the 'Round-44 gkeep size-request route' section against the entry and pins; "
     "run quality/check-index-rows.py at %(D)s. Write %(W)s/w2/RevReadmeFrontier.md.")
seat("RevQuality", "reviewer", "Review QUALITY.md criteria 82-84.",
     "Run each criterion's check command at %(D)s and confirm the 'shown able to fail' claim reproduces; check each cites a lesson that exists and a mistake "
     "behind it. Write %(W)s/w2/RevQuality.md.")
seat("RevRatioTool", "reviewer", "Review quality/ratio-domain-meta.py.",
     "Read the tool and its frozen rule; run it on rounds 34-44 at %(D)s; hand-classify every row and report disagreements; robustness (missing sections, "
     "rounds without claim rows). Write %(W)s/w2/RevRatioTool.md.")
seat("RevToolDiff", "reviewer", "Review the landed tool diff.",
     "`git diff %(B)s %(D)s -- tools/mado-geometry.py`: every docstring sentence vs pins %(W)s/fetch-c1 (computed locators), NOT_COMPARED semantics, "
     "exit codes, stderr, compatibility with SKILL.md probe rows that quote the summary line. Write %(W)s/w2/RevToolDiff.md.")
seat("RevEntryWhole", "reviewer", "Whole-entry review for QUALITY.md bar.",
     "Read " + ENTRY + " against corpus/QUALITY.md (the lane's bar): OBS/INF/UNK tagging honest, no overclaim, recheck sensible, 'does not establish' complete, "
     "no sibling-domain bleed (PROVINCE.md). Write %(W)s/w2/RevEntryWhole.md.")

# connectors (2), sentinel, scout, scribe, simplifier
seat("ConnCalibration", "connector", "Calibration: self-assessment vs repo state at the data commit.",
     "Count mismatches between SCORECARD.md Round 44 / SHONEN.md / the round-44 lesson's statements and observed repo state at %(D)s (counts, paths, hashes, "
     "verdicts). Each mismatch with its command. Write %(W)s/w2/ConnCalibration.md.")
seat("ConnSiblingDup", "connector", "Sibling duplication after landing.",
     "Grep sibling lanes (/home/vgpnk/Projects/shokunin/*-shokunin, read-only) for the landed facts (sendWindowSize, ack_configure, gdktoplevel, fullscreen modes, "
     "gkeep). Report duplicates/contradictions and arbitration owner. Write %(W)s/w2/ConnSiblingDup.md.")
seat("SentLiveRun", "sentinel", "Reproduce the live host run safely.",
     "Reproduce %(W)s/receipts/live-geometry-host-r44.txt with read-only verbs only; review the landed tool for injection/ReDoS regressions vs round 43. "
     "Write %(W)s/w2/SentLiveRun.md.")
seat("ScoutCoverageV2", "scout", "Coverage honesty of C2.",
     "At base %(B)s grep corpus/knowledge, SKILL.md, PROVINCE.md, tools for every surface the entry covers; state which are new ground and which deepen held "
     "entries; check the README coverage-map row. Write %(W)s/w2/ScoutCoverageV2.md.")
seat("ScrTrendEvidence", "scribe", "Draft the evidence table for the round's three trend verdicts.",
     "From LEARNING.md (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md) and the committed round-44 bytes, draft expansion / quality / "
     "discernment verdict candidates with evidence pointers (no verdict without a pointer; say where only a non-author can decide). Write %(W)s/w2/ScrTrendEvidence.md.")
seat("SimpLanded", "simplifier", "Dead weight in the landed text and tool.",
     "Find sentences in the entry, SKILL rows, README section, lesson and tool docstring that no reader needs or that duplicate another; give exact deletion "
     "text and why nothing is lost. Do not edit. Write %(W)s/w2/SimpLanded.md.")

n = len(items)
assert n == 33, n
assert len({i["name"] for i in items}) == n
print(n, dict(collections.Counter(i["role"] for i in items)))
spec = {"wave": "w2", "context": CONTEXT, "reportDir": ".ufo/waves/round-44/w2", "items": items}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-spec.json"), "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

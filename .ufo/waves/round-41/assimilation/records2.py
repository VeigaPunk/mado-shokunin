#!/usr/bin/env python3
"""Round-41 records, step 2: the lesson (Mistakes M41-9.., considerthese, corrections, S037 used-by log)."""
import re
L = "/home/vgpnk/Projects/shokunin/mado-shokunin/"
P = L + "corpus/lessons/round-41.md"
s = open(P).read()

def sub(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, 1)

sub("re-grounded this round as C2 with lane ids S283–S290", "re-grounded this round as C2 with lane ids S283–S289")
sub("journal S289, `input-capture-v1.xml` S290. `Hyprland-FocusGrab.hpp` is fetched but carries no id; it is corroboration, not a\nrow.",
    "journal S289. `input-capture-v1.xml` and `Hyprland-FocusGrab.hpp` are fetched but carry no id (no row is written for a source no entry cites).")
sub("the seven pre-wave receipts are committed at the freeze (`git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/`)",
    "the pre-wave receipts (nine files, `git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/`; seven are cited by new ids) are committed at the freeze")
sub("- Registry rows 219 → 219 + n, n = the cited new ids (at most S283–S290); tier A additions counted from the registry.", "- Registry rows 219 → 226 (S283–S289).")

# used-by log (CORPUS.md rule 2) and in-round row corrections
sub("## Assimilation ledger", "**Registry changes logged old→new (CORPUS.md rule 2).** S037 `used-by`: `corpus/knowledge/xdg-portal-routing-r12.md` → `corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md` (re-opened byte-identical: the installed package record). In-round correction of two NEW rows before the round closed, found by `ExecReopenSources` F1, `RevEntryBar` D3 and `ConnClaimsVsBytes` 3/4: S283 `teaches` \"four requests\" → \"six requests\"; S286 `teaches`/`anchor` \"which nine it binds\" → \"which ten branches it has (nine direct binds and foreign toplevel)\" with `foreign_toplevel` added to the branch list (cells 5-7 of rows that no earlier round had closed; nothing in a row of a closed round was edited; M41-19).\n\n## Assimilation ledger")

# Mistakes: insert M41-9..17 from the scribe draft, then M41-18..20
draft = open(L + ".ufo/waves/round-41/w2/ScrMistakesV2/mistakes.md").read()
i = draft.index("**M41-9 ")
mist = draft[i:].rstrip("\n")
extra = """

**M41-18 - the reflection's relayed entry count is wrong; first-hand re-derivation shows nine, not eight.** Class: number-drift (relayed). Evidence: `considerthese/2026-10-25.md:5` states eight knowledge entries for rounds 32-37; `git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l` prints `43` and `52` at `f6e3247`, and `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'` prints `9` (zero deleted); receipt `.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`, re-verified by `ScrConsiderFinal` (`w2/ScrConsiderFinal/final.md`). Captured-by: none before this round; the reflection is not a lane file and is not edited. Fix: QUALITY 76; the `## considerthese` note below carries the re-derivation. Shown able to fail: the command prints `9`, the reflection says eight.

**M41-19 - the landed entry and rows carried defects the w1 gates did not catch, found by the w2 attackers and fixed before closure.** Class: claim stronger than its quote, internal count drift, a malformed index row. Evidence: `ExecHarmAfter` — `python3 -I quality/check-index-rows.py --rev 07f2641 --repo .` exits 1, `README.md:70` carries 2 cells (every other row has a Sources cell); `CritEntryOverreach` F1-F20 (the 63-global session reported as whole, the first session's boot, \"five requests\" where the XML holds six `<request>` elements, `commit` quote that dropped `if (surfacesChanged)`); `RevEntryBar` D1-D7, `ExecEntryClaims` F1 (`add_surface` is sent at once in quickshell `addWaylandWindow`, `grab.cpp:66`); `ConnClaimsVsBytes` (lesson S290 lines, v1-MET sentence). Captured-by: none - the C2 predicate checks provenance and quote placement, not the truth of the sentence around the quote (`ExecRerunC2` F3 demonstrates it), and the index-row gate was not in the data commit's measurement set. Fix: the entry, README row, S283/S286 rows and the lesson are corrected in the fix commit (`assimilation/fix1.py`); `quality/check-index-rows.py` joins the round's harm set. Shown able to fail: `ExecHarmAfter/after.md` (exit 1 before the fix) and the same command at the fix commit (`receipts/harm-tip.txt`).

**M41-20 - one w1 seat produced no report at all and the orchestrator's results carried no outputs.** Class: dead seat, evidence gap. Evidence: `.ufo/waves/round-41/w1-results.json` (34 rows, `output: null`, note \"orchestrator kernel restarted mid-wave\"); `ls .ufo/waves/round-41/w1/ConnSiblingOverlap*` prints nothing (33 of 34 seat reports exist). Captured-by: none (M41-16 covers the results gap). Fix: disclosed in the report as one dead seat (`ConnSiblingOverlap`, last error text unavailable: the results file holds none); its question (sibling overlap) was re-asked in w2 as `ConnSiblingClosure`. Not shown able to fail: no instrument counts seats without a report."""
sub("### QUALITY.md criteria (owned by seat `ScrQualityCriteria`)", mist + extra + "\n\n### QUALITY.md criteria (owned by seat `ScrQualityCriteria`)")
# the old criteria subsection is replaced by the final list
a = s.index("### QUALITY.md criteria (owned by seat `ScrQualityCriteria`)")
b = s.index("## considerthese")
s = s[:a] + """### QUALITY.md criteria landed

Criteria 69-76 are appended to `corpus/QUALITY.md`, each citing a round-41 or round-40 lesson id and a control that can fail: 69 (tip receipts, M41-4; `check69.py`), 70 (wave-control markers, M41-3; `check70.sh`), 71 (seat report path, M41-8; `check71.py`), 72 (equivalent mutant from redundant code, M41-1; `check72.py`), 73 (an unreadable live stub, M41-10; controls K01/K02), 74 (teeth plus neutrality, M41-11; K05/K07), 75 (parser contract scope, M41-12; W1-N12, W1-N23, K03, fixtures `vernum0 pidzeros0 asciidigits0 unicodename0 unrec0 mixed0`), 76 (relayed numbers, M41-18).

""" + s[b:]
# considerthese
a = s.index("## considerthese")
b = s.index("## Census and measurements at the data commit")
s = s[:a] + """## considerthese

`considerthese/2026-10-25.md` proposal 5 ("Verify one fact first-hand per day, read-only", restating `2026-10-24.md` proposal 5, mined in round 33 as prose) is mined as QUALITY 76. The reflection's mined sentence re-derives: 68 commits `57a772b..f6e3247`; SOURCES `185` -> `207` rows (22 added); knowledge files `43` -> `52`; one tool added (`tools/mado-eventq.py`). One number fails - "eight entries" is nine (`git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge | grep -c '^A'` prints `9`, `'^D'` prints `0`) - so this note repeats the re-derived nine and marks the reflection's eight `relayed:` and corrected. The reflection is a pointer, not evidence. Receipt: `.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt`; re-verification: `.ufo/waves/round-41/w2/ScrConsiderFinal/final.md`.

""" + s[b:]
open(P, "w").write(s)
print("records2 ok", len(s.splitlines()))

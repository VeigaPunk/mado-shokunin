#!/usr/bin/env python3
"""make_mutants_md.py -- render the mutation report (mutants.md) of seat R56W2MutC3Harness."""
import json
import os
import sys

S = os.environ.get("SCRATCH", "/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness")
DELIVER = os.environ.get("DELIVER",
                          "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2MutC3Harness")
sys.path.insert(0, S)
from mutants import MUTANTS  # noqa: E402

# classification of the survivors: id -> (verdict, argument / proposed addition)
CLASS = {
    "M10": ("EQUIVALENT",
            "`leg not in d[\"missed\"]` (substring of the joined list) vs `leg not in d[\"missed_list\"]` (list membership). "
            "The list is validated against ALL_LEGS (M13 intact) and no leg name is a substring of another leg name, and "
            "no leg name contains the ',' separator, so the joined string contains a leg name iff the list contains it. "
            "stdout and stderr byte-identical to the reference."),
    "M12": ("EQUIVALENT",
            "`out` is rejected earlier unless it ends with '\\n', so `out[:-1].split('\\n')` always yields >= 1 element; "
            "`len(lines) != 1` and `len(lines) > 1` are then the same predicate. stdout and stderr byte-identical."),
    "M13": ("SURVIVED",
            "parse_line no longer rejects a `missed` list holding a leg name outside ALL_LEGS (e.g. `missed=missing,bogus`). "
            "Nothing else in the harness notices: the required leg is still looked up in the parsed list. "
            "ADDITION: a unit check on parse_line -- `parse_line('... missed=missing,totally_bogus_leg', 'abc')` must "
            "return None. Verified: the reference returns None, the mutant returns a dict (addition kills it)."),
    "M15": ("SURVIVED",
            "the counter's own `missing=` count is discarded, so the harness's self-consistency check "
            "(`set(nz) <= set(missed)`) can no longer see a counter that reports missing>0 without listing `missing`. "
            "The stderr divergence note changes (the harness's model is compared with the counter's). "
            "ADDITION: a unit check on parse_line -- a line with missing=41 and `missed=extra` must be rejected. "
            "Verified: the reference rejects it, the mutant accepts it (addition kills it)."),
    "M23": ("EQUIVALENT",
            "control 2 writes the entry paths in reverse order inside the used-by cell. The counter extracts the cell's "
            "paths as a SET (USED_BY.findall -> set), so every count and the whole MADO_USED_BY line are unchanged. "
            "stdout and stderr byte-identical."),
    "M24": ("SURVIVED",
            "control 3 (drop-one) empties the WHOLE used-by cell (9 paths) instead of removing one path. The counter only "
            "sees 'that path is missing', so the control is credited exactly as before. "
            "ADDITION: a unit check on mut_drop_one -- exactly one row may change and exactly one path may be removed "
            "from it. Verified: the reference removes 1 path, the mutant removes 9 (addition kills it)."),
    "M25": ("SURVIVED (latent)",
            "the `continue` branch of mut_drop_one is dead code on this tree (the first sorted entry "
            "corpus/knowledge/animation-table-r26.md IS listed by S158), so the mutation is unobservable here; on any tree "
            "where the first entry is unlisted it turns a skip into a Setup abort of the whole harness. "
            "ADDITION: a unit check on mut_drop_one with a registry from which the first sorted entry has been stripped "
            "out of every used-by cell -- the call must return (not raise) and must not remove that entry. "
            "Verified: the reference returns, the mutant raises Setup (addition kills it)."),
    "M26": ("SURVIVED",
            "control 4 (dangling-source) may pick a `source:` line outside the 15-line SRC window of registration-v2 "
            "('SRC(entry) = tokens on lines starting source: among the entry's first 15 lines'). On this tree the first "
            "entry's source: line is early, so the window widening is invisible. "
            "ADDITION: a unit check on mut_dangling_source with a synthetic fixture -- two entries, the first (sorted) "
            "with its only source: line at index 20, the second at index 3 -- the second must be the mutated one. "
            "Verified: the reference picks the second, the mutant picks the first (addition kills it)."),
    "M27": ("SURVIVED",
            "control 5 (ghost-path) writes the ghost path into S002's used-by instead of S001's. The counter only sees "
            "'one extra path', so the control is credited; the harness's own note is a hard-coded string "
            "('... to the used-by of S001') and does not reveal the swap. "
            "ADDITION: a unit check on mut_ghost_path -- the ghost path must be in S001's used-by cell. "
            "Verified: the reference puts it in S001, the mutant in S002 (addition kills it)."),
    "M29": ("SURVIVED",
            "control 6 (fenced-cite) fences the LAST candidate pair instead of the first (sorted by (S, entry)). "
            "Any fenced single citation yields `extra`, so the control is credited either way. "
            "ADDITION: a unit check on mut_fenced_cite -- the mutated entry must be the first candidate "
            "sorted by (S, entry) and the cited line must be inside the fence. "
            "Verified: the reference fences the first candidate, the mutant the last (addition kills it)."),
    "M30": ("SURVIVED",
            "control 6 opens a ``` fence and never closes it, so every following line of that entry becomes fenced and "
            "all of its other citations disappear. The collateral leg `lost` is tolerated by judge_control (only the "
            "required leg must be present), so the control is still credited. "
            "ADDITION: a unit check on mut_fenced_cite -- the number of ``` markers in the mutated entry must stay even "
            "(the fence must be closed). Verified: the reference has 6 markers, the mutant 5 (addition kills it)."),
    "M31": ("EQUIVALENT",
            "control 7 writes the allowlist's reason column as 'y' instead of 'x'. The counter parses the allowlist with "
            "parse_allow and reads only cells 0, 1 and 2 (the reason in cell 3 is never read), and the harness reads only "
            "cells 0 and 1, so every count and the whole MADO_USED_BY line are unchanged. stdout and stderr "
            "byte-identical."),
    "M32": ("SURVIVED",
            "control 7 (allow-everything) writes ONE allowlist row instead of one per pair (390 pairs). The counter only "
            "sees 'the allowlist sha does not match' plus `exempt != 24`, so the control is credited. "
            "ADDITION: a unit check on mut_allow_everything -- the written allowlist must carry one row per (S, entry) "
            "pair. Verified: the reference writes 390 rows, the mutant 1 (addition kills it)."),
    "M33": ("EQUIVALENT",
            "control 8 replaces the cited token with `re.sub(..., count=0)` instead of `count=1`. On CPython 3.14 "
            "`re.sub(..., count=0)` means 'replace ALL matches' (measured: 'S001 and S001' -> 'S--- and S---'), and the "
            "selected pair has exactly one occurrence of the token in total (`occ != 1: continue` selects it), so the "
            "same single replacement happens and the mutated bytes are identical. stdout and stderr byte-identical."),
    "M35": ("EQUIVALENT",
            "control 9 appends ' y' instead of ' x' to the allowlisted citing line. The stale leg only compares the "
            "line-sha, which differs either way, so the counter's line is unchanged. (The registration's literal text "
            "names ' x'; the deviation is cosmetic.) stdout and stderr byte-identical."),
    "M36": ("SURVIVED",
            "the effectiveness check `own[leg] > own_good[leg]` becomes `own[leg] > 0`: a control whose mutation does not "
            "raise its leg is no longer rejected as a setup error. On this tree every control does raise its leg, so the "
            "stdout is unchanged. "
            "ADDITION: control 10 'noop-control' -- a control whose mutation changes nothing (and therefore cannot raise "
            "any leg) -- plus the assertion that the harness refuses it with the setup error 'control noop-control is "
            "ineffective'. Verified: the reference exits 2 with that message, the mutant scores controls=9/10 verdict=FAIL "
            "(addition kills it)."),
    "M37": ("SURVIVED",
            "the effectiveness check is deleted outright (`ok = True`); same consequence as M36. "
            "ADDITION: control 10 'noop-control' as in M36. Verified: the reference exits 2 'ineffective', the mutant "
            "scores controls=9/10 verdict=FAIL (addition kills it)."),
    "M38": ("SURVIVED",
            "the `dangling` leg is dropped from the set of legs whose effectiveness is checked, so control 4 "
            "(dangling-source) is no longer required to raise the dangling leg. "
            "ADDITION: control 10 'noop-control' targeting the `dangling` leg (a mutation that changes an entry without "
            "touching a source: line) plus the assertion that the harness refuses it as ineffective. Verified: the "
            "reference exits 2 'ineffective', the mutant scores controls=9/10 verdict=FAIL (addition kills it)."),
    "M41": ("EQUIVALENT",
            "the forced add (`git add -A -f .`) becomes `git add -A .`. The lane's .gitignore ignores only "
            ".ufo/interactive-sessions/, .ufo/state/ and __pycache__/; no mutation target (corpus/SOURCES.md, "
            "corpus/knowledge/*.md, .ufo/waves/round-56/c3-name-only.tsv) is ignored, so the same files are staged and "
            "the same commit results. stdout and stderr byte-identical."),
    "M43": ("EQUIVALENT",
            "the mutated registry loses its final byte, the trailing newline after the last line of corpus/SOURCES.md. That "
            "line is prose (`no keypress observation: source-level only.`), not a registry row, so no row's cells, no "
            "used-by cell and no count changes. stdout and stderr byte-identical."),
    "M44": ("SURVIVED",
            "the harness's own entry model no longer filters the changed paths to corpus/knowledge/*.md, so the allowlist "
            "file is counted as an entry in control 7 (the model's count becomes 72 where the counter reports 71). The "
            "scored stdout is unchanged; only a diagnostic note diverges. This is a DIAGNOSTIC-level kill only: the "
            "verdict does not change, so the kill is by the stderr note, not by the score. "
            "ADDITION: the harness run's stderr must not report an entry-count divergence between the counter and the "
            "harness's model. Verified: the reference reports none, the mutant reports 'entries counter=71 harness=72' "
            "(addition kills it at stderr level)."),
    "M47": ("EQUIVALENT",
            "the harness's copy of the allowlist loses its final byte, which is the trailing newline of the last row. "
            "allow_rows() splits on newline and drops empty lines, so the last row is still parsed with the same four "
            "cells; the harness reads cells 0-1 only, and no mutation target is derived from the allowlist's last byte. "
            "stdout and stderr byte-identical."),
    "M49": ("EQUIVALENT",
            "the counter child loses the isolated mode (`python3 -I` -> `python3`). The counter imports only stdlib "
            "modules (argparse, hashlib, json, os, re, shutil, subprocess, sys) and its directory holds no module that "
            "could shadow them, so the child behaves identically. stdout and stderr byte-identical."),
    "M50": ("EQUIVALENT",
            "the counter child's timeout drops from 180 s to 5 s. The counter run on this tree takes 1.07-1.93 s "
            "(measured, 10 runs under sweep load), so the timeout is never reached and no run is aborted: stdout and "
            "stderr byte-identical. Caveat: the margin is only ~2.6x, so under a heavily loaded machine this mutant "
            "would stop being equivalent and would surface as a flaky harness (a control aborted by the timeout), "
            "not as a silent acceptance."),
    "M52": ("SURVIVED",
            "the harness's citation token rule is widened from `(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])` to `S[0-9]{3}`, so the "
            "harness's own model counts tokens inside longer identifiers (e.g. XS001) as citations; the contract's token "
            "rule does not. The scored stdout is unchanged, the diagnostic note diverges. "
            "ADDITION: a unit check on the harness's CITE_RE -- on 'XS001 and S0021 and S003' only S003 may match (S001 is "
            "inside a longer identifier; S0021 is a four-digit run, and the contract's lookahead rejects it). Verified: "
            "the reference matches ['S003'], the mutant matches ['S001', 'S002', 'S003'] (addition kills it)."),
}


def main():
    res = json.load(open(os.path.join(S, "results.json")))
    surv = json.load(open(os.path.join(S, "survivor_verification.json")))
    sv = {r["id"]: r for r in surv}
    muts = {m[0]: m for m in MUTANTS}
    killed = [r for r in res if r["status"] == "KILLED"]
    survived = [r for r in res if r["status"] == "SURVIVED"]
    equiv = [r for r in survived if CLASS.get(r["id"], ("", ""))[0].startswith("EQUIVALENT")]
    coverage = [r for r in survived if not CLASS.get(r["id"], ("", ""))[0].startswith("EQUIVALENT")]

    L = []
    A = L.append
    A("# Mutation test of `quality/r56_ctl_c3.py` (round-56 C3 control harness)")
    A("")
    A("Seat R56W2MutC3Harness, wave w2 (falsify), lane commit `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`.")
    A("")
    A("## 1. What was attacked")
    A("")
    A("`quality/r56_ctl_c3.py` -- the independent control harness behind the C3 claim")
    A("`MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK`.")
    A("Nine controls (base-registry, fill-all, drop-one, dangling-source, ghost-path, fenced-cite,")
    A("allow-everything, delete-citation, stale-allow), their expected legs, the shared-clone scratch builder and")
    A("`judge_good`/`judge_control` (exempt=24) are the ONLY kill evidence the claim has; wave 1 wrote each artifact")
    A("once and the round-55 counters left 11/24, 8/38 and 4/17 survivors. The attack is therefore the harness")
    A("itself: if a one-line change to it weakens the discrimination without changing the printed verdict, the")
    A("claim's control evidence is weaker than it looks.")
    A("")
    A("## 2. Method")
    A("")
    A("* Scratch clone: `git archive 28fc86ac...` of the lane into `/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness/tree`;")
    A("  every mutation is applied to a COPY of `quality/r56_ctl_c3.py`. The lane is never written to.")
    A("* Reduced scratch repo (`mini`): the same content blobs as the lane commit (corpus/SOURCES.md, the 71")
    A("  corpus/knowledge/*.md, frozen-tables-v2.json, c3-name-only.tsv, the counter), committed in a fresh git repo")
    A("  whose object store borrows the lane's through `.git/objects/info/alternates`, so the frozen base revision")
    A("  13f0acbe stays readable. Blob-identity proof: `receipts/06-environment-note.txt`.")
    A("* Oracle (unchanged for every mutant): the shipped driver `quality/check-r56-controls.py --claim c3` run")
    A("  three times per mutant:")
    A("  * **A** --counter = the REAL counter `quality/counters/c3-r56-used-by.py`; must print exactly")
    A("    `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK` and exit 0;")
    A("  * **B** --counter = `stub_green.py` (always prints TARGET_MET, exit 0) -> must score FAIL (exit != 0);")
    A("  * **C** --counter = `stub_legs.py` (prints every leg missed, exit 1) -> must score FAIL (exit != 0).")
    A("* KILLED = one of A/B/C deviates from the expectation. SURVIVED = all three hold. EQUIVALENT = the mutation")
    A("  cannot change the harness's verdict (argument + byte-identical stdout/stderr against the reference).")
    A("* The reduced repo is faithful: the unmutated harness scores `good=ok controls=9/9 verdict=OK` on it, and the")
    A("  same run against the REAL lane repo (`--repo <lane> --rev 28fc86ac...`) prints the same line and the same")
    A("  nine control notes -- `receipts/02-lane-crosscheck.txt`.")
    A("")
    A("## 3. Result")
    A("")
    A("| | count |")
    A("|---|---|")
    A("| mutants | %d |" % len(res))
    A("| KILLED by the shipped oracle | %d (%.1f%%) |" % (len(killed), 100.0 * len(killed) / len(res)))
    A("| SURVIVED | %d |" % len(survived))
    A("| ... of which EQUIVALENT (no behavioural difference) | %d |" % len(equiv))
    A("| ... of which genuine coverage findings (addition proposed and verified) | %d |" % len(coverage))
    A("")
    A("Kill rate of the shipped oracle over the NON-EQUIVALENT mutants: **%d/%d = %.1f%%**."
      % (len(killed), len(killed) + len(coverage), 100.0 * len(killed) / (len(killed) + len(coverage))))
    A("With the %d proposed additions the kill rate over the non-equivalent mutants is **%d/%d = 100%%**."
      % (len(coverage), len(killed) + len(coverage), len(killed) + len(coverage)))
    A("")
    A("## 4. The mutant table")
    A("")
    A("`old -> new` is the single contiguous source fragment that was replaced (each occurs exactly once in the target).")
    A("")
    A("| id | operator | mutated fragment | verdict |")
    A("|---|---|---|---|")
    for r in res:
        m = muts[r["id"]]
        frag = "`%s` -> `%s`" % (m[2].replace("|", "\\|"), m[3].replace("|", "\\|"))
        if r["status"] == "KILLED":
            v = "KILLED"
            det = ""
            for c in r["checks"]:
                if not c["ok"]:
                    det = c["detail"]
                    break
            v += " (%s)" % det
        else:
            cl = CLASS.get(r["id"], ("SURVIVED", ""))[0]
            v = cl
        A("| %s | %s | %s | %s |" % (r["id"], r["operator"], frag, v))
    A("")
    A("## 5. Every survivor: the argument or the addition that kills it")
    A("")
    for r in survived:
        mid = r["id"]
        cl, arg = CLASS.get(mid, ("SURVIVED", ""))
        s = sv.get(mid, {})
        A("### %s -- %s" % (mid, cl))
        A("")
        A("* mutated: `%s` -> `%s`" % (muts[mid][2], muts[mid][3]))
        A("* stdout identical to the reference: %s; stderr identical: %s"
          % (s.get("stdout_identical"), s.get("stderr_identical")))
        A("* %s" % arg)
        if s.get("addition"):
            A("* verification: the addition passes on the unmutated harness (%s) and fails on the mutant (%s) -- %s"
              % (s.get("reference_passes"), s.get("mutant_passes"), s.get("mutant_detail", "")))
        A("")
    A("## 6. What the survivors mean for the claim")
    A("")
    A("The claim `MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK` is **not falsified**: the harness is")
    A("correct on this tree and its nine controls do fail the real counter in the nine intended ways. The mutation")
    A("sweep nevertheless shows that the printed verdict pins down much less than it looks:")
    A("")
    A("1. **The harness does not pin the counter's own grammar.** `parse_line` accepts a `missed` list with unknown leg")
    A("   names (M13) and, after M15, accepts a `missing=` count that the `missed` list does not mention. A counter that")
    A("   prints a self-inconsistent line can still be credited.")
    A("2. **The controls do not pin what they mutate.** Four of the nine controls can be changed into a different")
    A("   mutation of the same leg and still be credited: drop-one can empty a whole cell (M24), dangling-source can")
    A("   leave the 15-line SRC window (M26), ghost-path can write into the wrong registry row (M27) and fenced-cite can")
    A("   fence a different pair (M29) or leave the fence open (M30); allow-everything can write one row instead of one")
    A("   per pair (M32). The harness's own note for control 5 is a hard-coded string, so the wrong-row variant is")
    A("   invisible even in the diagnostics.")
    A("3. **The 'the mutation must raise its leg' guard is not guarded.** M36/M37/M38 delete or weaken the check that")
    A("   rejects an ineffective control; on this tree every control does raise its leg, so nothing notices.")
    A("4. **The harness's own model drifts from the contract.** The widened citation regex (M52) and the dropped")
    A("   `corpus/knowledge/` filter (M44) make the harness's independent model disagree with the contract's token rule")
    A("   and ENTRIES definition; both are only diagnostics today, but the model is what the effectiveness check uses.")
    A("5. The `lost`, `conflict` and `stale` legs are never checked for effectiveness (the harness's model does not")
    A("   compute them), and control 7/8/9 are accepted on `bool(new_entries)` alone.")
    A("6. The harness's independent model is not the contract, and says so on every run. On the GOOD tree the harness's own")
    A("   metric reports missing=24 while the counter reports missing=0, because the harness does not implement the frozen")
    A("   allowlist exemption (c3-name-only.tsv). The stderr line 'note[good]: counter and harness numbers diverge (not scored)'")
    A("   is printed on every run of the unmutated harness (receipts/01, receipts/02). Nothing scores it, so no verdict is")
    A("   wrong, but the harness's cross-check is noise, and the effectiveness check (own[leg] > own_good[leg]) is calibrated")
    A("   against that wrong baseline (missing 65 vs 24 instead of 65 vs 0).")
    A("7. The population of the good line is never checked (probe_population.py). judge_good accepts entries= and rows=")
    A("   without comparing them to the harness's own 71 and 328. A green counter stub that prints entries=0 rows=0 scores")
    A("   good=ok on the unmutated harness (receipts/07). It still scores controls=0/9 verdict=FAIL, so this is a gap only")
    A("   in combination with controls. The one-line fix (or d['e'] != own['entries'] or d['r'] != own['rows']) makes the")
    A("   empty stub good=bad and leaves the real counter at controls=9/9 verdict=OK (receipts/07).")
    A("")
    A("### 6a. How the 29 kills were achieved")
    A("")
    A("Of the 29 KILLED mutants, 25 fail the GOOD-tree run (check A: the harness no longer prints good=ok controls=9/9")
    A("verdict=OK on the true tree). Of those, 8 are the harness's own fail-closed SETUP errors (rc=2, empty stdout, a SETUP:")
    A("line on stderr: M22, M28, M39, M40, M42, M46, M53, M54) and 17 change the verdict line.")
    A("Only four were caught by the control logic alone: M17 and M18 (B: the always-green stub is credited), and M19 and")
    A("M45 (B or C). The silent-acceptance surface is therefore the 25 survivors, which section 5 covers.")
    A("")
    A("## 7. Reproduction")
    A("")
    A("```sh")
    A("S=/fast/scratch/hyaku/mado-r56/R56W2MutC3Harness   # scratch, removed on exit")
    A("python3 -I $S/run_mutants.py            # the sweep (54 mutants x 3 oracle checks)")
    A("python3 -I $S/verify_survivors.py       # the additions that kill the survivors")
    A("python3 -I $S/collect_receipts.py       # the receipt bundle")
    A("```")
    A("")
    A("Deliverables: `mutants.md` (this file), `run_mutants.py`, `mutants.py` (the mutation table),")
    A("`verify_survivors.py` (the proposed additions), `collect_receipts.py`, `stub_green.py`, `stub_legs.py`,")
    A("`receipts/`.")
    out = os.path.join(DELIVER, "mutants.md")
    with open(out, "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("wrote %s (%d lines)" % (out, len(L)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

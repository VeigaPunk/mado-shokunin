# CritFailClosed — critic seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: critic

Attack the two gates' error paths. For LANE/quality/check-counter-discrimination.py and LANE/quality/check-evidence-pointers.py: find any input under which the gate exits 0 while the claimed work is absent. Candidates to test in /tmp: missing frozen spec, predicate drift, missing manifest entry, an instrument that exits 1 but prints TARGET_MET, a timeout, an unwritable receipts dir, `--rev` naming a tag instead of a commit, a pointer list that is empty because the section heading was renamed, the lesson file present but empty. Quote the code path for each and give a verdict (fail-closed / fail-open).

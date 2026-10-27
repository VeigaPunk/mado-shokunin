# MutC2Entry — round-50 w1 (carried round-49 w2 item), status: running

Seat: mutation-tester. Target: semantic mutations of `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md`
that the frozen C2 counter (`quality/counters/c2-r49-bind-entry.py`, PRED-C2-r49) cannot see.

Method: scratch fixture clone of the lane at base with the candidate entry, rows S352-S363, README row, lesson Gate
lines, fetch pins and live receipt committed (fixture identity, toplevel verified). Baseline first (round-49
registration records the pristine candidate as NOT meeting the counter — clauses b/c/d/e/j), so the baseline must be
brought green (fixture assembly + documented minimal counter repairs = the PRED-C1-r50 port draft) before any mutant
verdict is meaningful. Then one factual claim inverted per mutant, quotes and locators byte-identical, scored with the
same detector on pristine, mutated and restored bytes.

Findings will be filled in here; per-run logs land in `.ufo/waves/round-50/w1/MutC2Entry/`.

(tooling installs: none — python3/git/hyprctl/xkbcli from the host only)

# R81ExecC2Run findings

All commands run from /home/vgpnk/Projects/shokunin/mado-shokunin unless noted. No installs
performed (python3, omarchy, pgrep, cut, grep already present).

## Commands and what mattered

1. `mkdir -p /fast/scratch/hyaku/mado-r81/R81ExecC2Run` + seat dir — setup only.
2. `python3 -I quality/counters/c2-r81-runbook.py --repo . --rev 0e2ccd2a8692825cac534f57246053b276be9f13 --controls .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --carried .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --scratch-root /fast/scratch/hyaku/mado-r81/R81ExecC2Run` (exit 0)
   - `MADO_R81_CONTROLS: sha256=ae7ee90ebd1a6ff2c590c12ca3b8c925d26cd8a47ca33bcd16af038f138c1a7f6 cases=26`
   - `MADO_R81_PROBE: name=keybindings-actions row=24 kind=action_column match=yes rc=0`
   - `MADO_R81_PROBE: name=waybar-pgrep row=25 kind=pid_state match=yes rc=0 out='1720'`
   - `MADO_R81_RUNBOOK: cases=26 executed=26 matched=26 shapes=21/21 anchors=26/26 rows=26/26 control_new=0/2 mutants=23 killed=23 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tree=bound`
   - Full output preserved at `.ufo/waves/round-81/w1/R81ExecC2Run/c2-run.txt`.
3. `omarchy menu keybindings --print | cut -c36-` (exit 0) — `wc -l` → 193. First five lines:
   ` → Terminal` / ` → Tmux` / ` → Browser` / ` → File manager` / ` → Launch apps`.
   `head -1 … | cat -A` → ` M-bM-^FM-^R Terminal$`.
4. `pgrep -x waybar` (exit 0) — stdout `1720`; `echo $?` → `0`.
5. `grep -n 'printf "%-35s' .ufo/waves/round-80/fetch/S473.txt` → line 164:
   `        printf "%-35s → %s\n", key_combo, action;`
6. `omarchy menu keybindings --print` (exit 0) — `wc -l` → 193. `head -1 | od -c` shows
   35 key bytes, space at byte 36, `342 206 222` at bytes 37–39, space at 40, action at 41+.
   Python check: arrow begins at byte offset 37 (1-based); 36 bytes/characters precede it.
7. Grammar-breaker greps on the 193-line action column:
   - `grep -c '&'` → 2; bare-& (regex `(?<!&)&(?!(amp|lt|gt|quot|apos);)`) → 1:
     line 17 ` → Pop window out (float & pin)`.
   - `grep -c '<'` → 0. `grep -c ' $'` → 0. `grep -P -c '→.*→'` → 0.
   - All 193 lines match `^ → ` (`grep -c '^ → '` → 193). No empty action (shortest: ` → X`).
8. `python3 -I quality/counters/c2-r81-runbook.py --selftest` (exit 0) →
   `MADO_R81_RUNBOOK_SELFTEST: 88/88`.

## Conclusion

Frozen C2 claim verified end-to-end: 26/26 cases, 26/26 rows, 26/26 anchors, `control_new=0/2`,
23/23 mutants killed, verdict TARGET_MET, controls sha256 matches the freeze. Both new rows
execute by hand and reproduce the frozen expectations. The frozen grammar's bound outcome
(` → ` prefix, non-empty trimmed action, no second arrow) holds for today's 193-line payload;
a stricter no-bare-`&` grammar would have one live violation (payload quirk: description path
skips XML escaping), but the frozen grammar does not claim that bound.

STATUS: ok

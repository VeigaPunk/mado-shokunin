# R55W2AuditF: report (round 55, mado, wave w2, sentence-to-pin audit)

Seat: leaf member, no subagents. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Scratch: `/fast/scratch/hyaku/mado-r55/R55W2AuditF/` (removed before yield). No lane tracked file was edited; no git, jj, commit, stash or push ran; the lane tool `tools/mado-kbdopts.py` was executed read-only from scratch and was not modified. Full table: `.ufo/waves/round-55/w2/R55W2AuditF/audit.md`. Receipts: `.ufo/waves/round-55/w2/R55W2AuditF/receipts/`.

## Targets and verdicts

| Target | Verdict | Evidence pointer |
|---|---|---|
| H01 (input.conf:14 declares repeat_rate = 40) | SURVIVES | audit.md section 1; `receipts/live-getoption.txt`; `cmp ~/.config/hypr/input.conf fetch/host-input.conf` identical |
| H02 (input.conf:15 declares repeat_delay = 250) | SURVIVES | audit.md section 1 |
| H03 (input.conf:18 declares numlock_by_default = true) | SURVIVES | audit.md section 1 |
| H04-H06 (host-getoption.json :1-:3 values 40 / 250 / 1) | SURVIVES; the value parts are SUPPORTED, the "live" provenance and "not a delivery" parts are HELD | audit.md section 1; this run's three `hyprctl getoption -j` reads concatenated are `cmp`-identical to `fetch/host-getoption.json` |
| Joining section, sentences P1a-P4, P6-P8, P10-P11, P13 | SURVIVES (SUPPORTED or HELD as labelled) | audit.md section 2 |
| Joining section, P1c (hyprlang integer reading) | HELD: no cell in the entry; pin exists (round-46 `hyprlang-config.cpp:259-262`, byte-equal upstream hyprlang v0.6.8 `src/config.cpp`) | audit.md P1c |
| Joining section, P5 ("so by K16 every keyboard resolves to the global value") | BROKEN as a runtime statement: a file read cannot show the running state; the claim is OVERREACH | audit.md P5 |
| Joining section, P9 ("printed by no dump", r46:70) | BROKEN as written (OVERREACH in scope): r46:70 says the `devices` dump; this entry's H04-H06 show `getoption -j` printing all three | audit.md P9 |
| Joining section, P12 ("the honesty valve ... counted, not guessed") | BROKEN, reproduced: the tool falls back to the default and prints AGREE/DIFFER for out-of-range input, and the frozen C2 declared limit says "never guessed" | audit.md P12 and section 6; `receipts/attack-runs.txt` |
| Adjacent ground, A1 (XKB pointers) | UNVERIFIED for content (pointer exists; the two notes were not audited) | audit.md A1 |
| Adjacent ground, A2 ("K09 only pins that numlock is set on the keymap state") | BROKEN as attribution: K09 pins the gate at IKeyboard.cpp:122 only; the set is at :123-130 and conditional on :126 | audit.md A2 |
| Adjacent ground, A3 (sibling sweep found no sibling lane) | SURVIVES as a description of the cited report; the sweep was not re-run | audit.md A3 |
| Adjacent ground, A4 (host readback 40/250/1 already held) | SURVIVES | audit.md A4; lines `hyprctl-verification-layer.md:132-134` and `config-health-report-r3.md:546-548` checked |

## Attack reproduction (P12, the one reproduced break with a runnable input)

Input is in the frozen C2 grammar: `input:repeat_rate = 201` (out of the modelled 0..200 range, which the frozen declared limit names as the `unsupported` case). Tool unchanged, run from scratch:

```
$ python3 -I tools/mado-kbdopts.py --config oor.conf --keyboard kbX --getoption oor-live.txt
MADO_KBDOPT: keyboard=kbX repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=3
MADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=25 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:repeat_delay config=600 live=600 verdict=AGREE
MADO_KBDOPT_LIVE: option=input:numlock_by_default config=0 live=0 verdict=AGREE
MADO_KBDOPT: DONE keyboards=1 unsupported=3 live=AGREE
rc=0
```

Also `numlock_by_default = 2` with live 1 gives `numlock=0 ... unsupported=1` and `verdict=DIFFER`; in-range `repeat_rate = 200` gives `unsupported=0` and `DIFFER` (control). The tool does not reject the input (rc 0, no syntactic error), so this is not a non-reproducing syntactic attack. The break is the fallback guess plus the verdict on an unparsed key. The entry's UNKNOWN list says the range enforcement site is not pinned, so the default fallback is not a source-backed value either. Minimal correction for P12 is in audit.md.

Scope note: the C2 predicate and its 18 + 8 fixtures were not re-run here, and I did not audit whether any of the six committed fixtures with `unsupported=[1-9]` in `expected.out` encodes the same fallback. That check belongs to the C2 falsifier.

## What ran

- Host reads (allowed set): `cat ~/.config/hypr/input.conf`; `hyprctl getoption input:repeat_rate -j`, `input:repeat_delay -j`, `input:numlock_by_default -j`; `hyprctl devices -j`; `hyprctl version`. No keyword, dispatch, reload or service command.
- Lane reads: `corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`; `.ufo/waves/round-55/fetch/*` (all nine source/host pins, `SHA256SUMS.txt` verified); `frozen-tables.json` and `frozen-tables-v2.json` `c1.h`; `claims-frozen.md` C2; the knowledge notes and receipts cited by the prose; `w1/R55ScoutAdjacency.md`; `w1/R55ScoutHost/receipts-cmp-grep.txt`.
- Tool runs (lane tool unchanged, `python3 -I`, cwd = scratch): the exact `Joining` invocation with two keyboard names; `--selftest` (83/83 passed); the attack inputs above.
- Upstream re-open (curl, `efb50993780079460b0cbed1363e2166a2de1d9f`): `src/managers/input/InputManager.cpp`, `src/devices/IKeyboard.cpp`, `src/devices/IKeyboard.hpp`, `src/managers/SeatManager.cpp`, `src/config/values/ConfigValues.cpp`, `src/config/legacy/ConfigManager.cpp`, `src/protocols/core/Seat.cpp`; wayland 1.26.0 `protocol/wayland.xml` (gitlab raw); hyprlang v0.6.8 `src/config.cpp`. All byte-equal to the committed pins (sha in audit.md section 4).

## Disclosure (host reads)

- While checking the `device`-block claim I ran `ls -la ~/.config/hypr` and a `grep -rnE 'device\[|device \{|device\{|repeat_|numlock|input *\{' ~/.config/hypr`. That reads files outside the allowed host set (only `input.conf` is allowed). Its output matched only `input.conf` lines; no content from any other file in that directory was used or copied into any deliverable. The cited L1 receipt `w1/R55ScoutHost/receipts-cmp-grep.txt` already holds the exact-command result (rc=1).
- The host config tests were file reads plus `hyprctl` read verbs only. The host config matches the committed pin byte-for-byte.

## Path discrepancy

The brief placed the live receipt under `corpus/knowledge/receipts/live-kbdopts.txt`. The file is at `.ufo/waves/round-55/receipts/live-kbdopts.txt`, which is the path the knowledge note cites. Nothing else was found under the other path.

## Tooling

No tools were installed or updated. `hyprctl`, `curl`, `python3` and `grep` were used as already present on the host. No pacman transaction, and no `~/.local/bin` write.

## Not verified

- A1: content of `hyprland-input-devices-r46.md` (beyond line 34 and 70) and `xkb-keymap-compile-r48.md` was not audited.
- P6 / the `getoption` "no device argument" claim: the r40 note was cited, not re-verified; `hyprctl getoption -h` is outside the allowed reads.
- A3: the sibling sweep was not re-run.
- Runtime state: no keypress, no client `wl_keyboard` bind, and no running-daemon device value was observed. Rows that imply them are labelled as boundaries.
- Whether the six committed C2 fixtures with `unsupported=[1-9]` encode the fallback guess (for the C2 falsifier).

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r55/R55W2AuditF/` removed before yield. The deliverable directory holds only `audit.md`, this report and `receipts/`.

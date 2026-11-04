# Seat R81ExecC2Run — C2 runbook counter, verbatim run + both new rows by hand

## 1. Verbatim counter run

Command (cwd = /home/vgpnk/Projects/shokunin/mado-shokunin), exact argv:

```
python3 -I quality/counters/c2-r81-runbook.py --repo . --rev 0e2ccd2a8692825cac534f57246053b276be9f13 --controls .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --carried .ufo/waves/round-80/controls/c2-runbook-cases-r80.json --scratch-root /fast/scratch/hyaku/mado-r81/R81ExecC2Run
```

Exit code: `0`.

Final line (quoted verbatim from `c2-run.txt`):

```
MADO_R81_RUNBOOK: cases=26 executed=26 matched=26 shapes=21/21 anchors=26/26 rows=26/26 control_new=0/2 mutants=23 killed=23 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tree=bound
```

Head of the same output confirms the frozen controls bytes were used:

```
MADO_R81_CONTROLS: sha256=ae7ee90ebd1a6ff2c590c12ca3b8c925d26cd8a47ca33bcd16af038f138c1a7f6 cases=26
```

(claim freezes the controls at sha256 `ae7ee90e…` — prefix matches). Full 52-line output kept at
`.ufo/waves/round-81/w1/R81ExecC2Run/c2-run.txt`. Every claim element checks out: 26/26 cases,
26/26 rows, 26/26 anchors, `control_new=0/2`, 23/23 mutants killed, verdict TARGET_MET.

## 2. Both new rows executed by hand (cwd = lane root)

### Row A: `omarchy menu keybindings --print | cut -c36-`

Exit code `0`. Line count: `193`.

First five lines (verbatim):

```
 → Terminal
 → Tmux
 → Browser
 → File manager
 → Launch apps
```

Line 1 under `cat -A`:

```
 M-bM-^FM-^R Terminal$
```

i.e. space, UTF-8 arrow `E2 86 92`, space, `Terminal`, LF — exactly the ` → ` prefix the
frozen action_column matcher binds.

### Row B: `pgrep -x waybar`

stdout (verbatim): `1720`; `echo $?` → `0`.

This reproduces the frozen positive sample for `waybar-pgrep` byte-for-byte
(`"out": "1720\n", "rc": 0`) and equals the carried round-80 `waybar-process` frozen value
`"1720"`.

## 3. Separator position in the payload (S473.txt)

The emitter is at `.ufo/waves/round-80/fetch/S473.txt:164`:

```
        printf "%-35s → %s\n", key_combo, action;
```

Measured against the live first line (`SUPER + RETURN` … `Terminal`, 48 bytes + LF):

- `od -c` shows: 35 key-combo bytes, byte 36 = space (`0x20`), bytes 37–39 = `342 206 222`
  (octal) = `E2 86 92` = `→`, byte 40 = space, bytes 41+ = action.
- Python check: arrow starts at byte offset 37 (1-based); 36 bytes precede it; 36 characters
  precede it (the key-combo column is pure ASCII, so byte offset = character offset here).
- Therefore `cut -c36-` slices from the space at char 36, and every emitted line begins with
  the 3-character prefix ` → ` — the frozen matcher's `prefix` value (`" \u2192 "`).

## 4. Stricter-grammar scan of today's live action column (193 lines)

| Probe | Count | Evidence |
|---|---|---|
| bare `&` (not `&amp;`/`&lt;`/…) | **1** | line 17: ` → Pop window out (float & pin)` |
| `<` anywhere | 0 | `grep -c '<'` → 0 |
| trailing space | 0 | `grep -c ' $'` → 0 |
| second `→` on a line | 0 | `grep -P -c '→.*→'` → 0 |
| empty trimmed action | 0 | shortest line is ` → X` (4 chars) |

The single bare `&` is explained by the payload: the XML-entity escaping gsubs
(`gsub(/&/, "\\&amp;", action);` …) run only inside the `if (action == "")` reconstruction
branch (S473.txt:157–162); the description path (`action = $3`, line 141) skips them. The
other `&` line, 147 (` → omarchy-hw-external-monitors &amp;&amp; omarchy-hyprland-monitor-internal off`),
comes from the reconstruction path and is properly escaped.

Assessment: the frozen grammar's bound outcome — ` → ` prefix, non-empty trimmed action, no
second arrow — is **right for today's payload**: all 193 live lines satisfy it (193/193 start
with ` → `). A stricter grammar that also forbade bare `&`/`<` in the action would have one
live violation today (the `&` on line 17); the frozen grammar does not claim that stricter
bound, so no contradiction.

## 5. Selftest

Command: `python3 -I quality/counters/c2-r81-runbook.py --selftest` (cwd = lane root).
Final line, quoted verbatim:

```
MADO_R81_RUNBOOK_SELFTEST: 88/88
```

Exit code `0`. (The declaration's `tool selftest 121/121` figure sits under the C1 claim; the
C2 claim pins no selftest number, so the measured 88/88 is the C2 tool's tally and does not
contradict the frozen text.)

## Risks / notes

- Live `pgrep` output is dynamic by nature; today's `1720` matches the frozen sample exactly,
  but a future host restart will change the PID. The matcher is range/pattern-based, not
  value-pinned, so this is expected and handled.
- The unescaped-description `&` is a latent payload quirk, not a matcher defect; flagged for
  the L1's awareness only.

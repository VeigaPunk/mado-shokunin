# ScoutHostRederive — re-derivation of S213.receipt.txt (mado r37 w1)

Seat: scout, read-only. Re-derived at 2026-10-25T09:13:28-03:00 (receipt taken 09:00:04-03:00).
Receipt sha256: `1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58`.
No socket connection, no hyprctl write verb, no lane file touched. Tools installed or updated: none.

## Verdict

PASS. All 26 receipt values reproduce exactly. The session log did not grow between the receipt and my run: same size, same line count, same mtime.

One scope finding (not a count error): the unit-journal values (717 lines, 4 "using config" lines) cover four unit invocations, not just the running Hyprland instance. Restricted to the current instance, the journal has 349 lines and 2 "using config" lines. Those 2 lines match the log's two config loads at lines 12 and 18. Marker and probe counts are 0 in every invocation, so the claim's zeros hold under either scope.

## Table

| item | receipt value | my value | same/moved |
|---|---|---|---|
| hyprland_version | v0.56.2 efb50993…d9f | `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean` | same |
| log path (instance dir) | …_1792804449_426444678/hyprland.log | sole instance dir under /run/user/1000/hypr/; 1792804449 = 2026-10-23T22:14:09-03:00 = Hyprland pid 1619 start | same |
| log bytes | 4259033 | 4259033 | same |
| log lines | 27331 | 27331 | same |
| log mtime | 2026-10-25 04:24:03.444802113 -0300 | 2026-10-25 04:24:03.444802113 -0300 | same (not grown) |
| log "overflowed event queue" | 0 | 0 | same |
| log "failed writing event" | 0 | 0 | same |
| log "Socket2 fd" | 0 | 0 | same |
| histogram DEBUG from aquamarine | 27280 | 27280 | same |
| histogram ERR from aquamarine | 31 | 31 | same |
| histogram DEBUG (core) | 21 | 21 | same |
| lines matching no prefix class | (not stated) | 0 | — |
| records (`awk END{print NR}`) | (not stated; histogram sums to 27332) | 27332 (last byte not `\n`) | see note |
| core_logger_lines | 21 | 21 | same |
| last_core_logger_line_number | 21 | 21 (first non-core line = 22) | same |
| config_load_line_numbers | 12 18 | 12 18 | same |
| unit_journal_lines | 717 | 717 | same (scope: 4 invocations, see below) |
| journal "overflowed event queue" | 0 | 0 | same |
| journal "failed writing event" | 0 | 0 | same |
| journal "Socket2 fd" | 0 | 0 | same |
| probe in_log | 7 | 7 | same |
| probe in_unit_journal | 0 | 0 | same |
| unit_journal_using_config_lines | 4 | 4 (2 current instance + 2 previous instance) | same (scope) |
| debug:disable_logs | `{"option":"debug:disable_logs","int":1,"set":false}` | `{"option":"debug:disable_logs","int":1,"set":false}` | same |
| debug:enable_stdout_logs | `{"option":"debug:enable_stdout_logs","int":0,"set":false}` | `{"option":"debug:enable_stdout_logs","int":0,"set":false}` | same |

Histogram note (minor receipt-internal inconsistency, explained): 27280 + 31 + 21 = 27332, but the receipt says `lines: 27331`. The cause is that the log's last byte is not a newline. `tail -c 1 | od -c` prints `N`, so the file ends mid-record while the writer is still appending. `wc -l` counts 27331 newlines, while `awk 'END{print NR}'` and `grep -c ''` both count 27332 records. No line holds more than one record (`lines with >1 record: 0`), and no line lacks a class prefix (`unprefixed: 0`). The histogram is therefore exact, and "lines: 27331" counts newlines. Whoever cites S213 should say "27331 newlines / 27332 records".

Log sha256 at my run: `b7cdca1fe13ae21dc7987932adb7b474c54d9e5d38d44f4e1d37dc502e36c815` (the receipt records no log digest, so I could not compare it).
Unit-journal (`-o cat`, all invocations) sha256 at my run: `43bf1f07176502bfa073c8256b718e0bd5cdcee5b94c1d188479dec490af63d4`.

## Finding: journal scope

`systemctl --user show wayland-wm@hyprland.desktop.service`:
```
ActiveState=active
InvocationID=06d70f0ccbd143f1b24640674c979705
MainPID=1614
ExecMainStartTimestamp=Fri 2026-10-23 22:14:09 -03
StandardOutput=journal
```
Per-invocation split of the receipt's journal command (`_SYSTEMD_INVOCATION_ID=` filter, `-o cat`):
```
inv 06d70f0c: lines=349 using_config=2 probe=0 first=2026-10-23T22:14:09-03:00   (current; Hyprland pid 1619)
inv 6f33faf0: lines=6   using_config=0 probe=0 first=2026-10-23T09:39:20-03:00
inv 51d1a816: lines=347 using_config=2 probe=0 first=2026-10-23T13:24:58-03:00   (previous Hyprland, pid 1667)
inv 644314e0: lines=11  using_config=0 probe=0 first=2026-10-23T14:28:22-03:00   (a systemd-coredump record)
noinv entries: 4
```
349 + 6 + 347 + 11 + 4 = 717, which equals the receipt's total.
- The receipt's "unit_journal_using_config_lines: 4" is 2 per Hyprland instance × 2 instances. For the current instance, the journal's 2 "using config" lines (all from pid 1619) match the log's 2 config loads at lines 12 and 18.
- The journal's last entry is 2026-10-24T12:09:57-03:00. It has 0 entries since the receipt time, and the current Hyprland pid wrote 51 journal lines in total. Any marker emitted after the core logger went silent would have no route into the journal either.
- The coredump invocation means a previous Hyprland run crashed (pid 1667 era). Its 11 lines contain 0 marker and 0 probe hits, so it does not affect C1 or C2. Content was not read, per the privacy rule.

Impact on the key claim: none against it. A zero count of "Socket2 fd" and "overflowed event queue" holds in all four invocations. With `debug:disable_logs` int 1 and the core logger's last line at 21 of 27331, these zeros still cannot separate "never overflowed" from "not logged". Recommendation for whoever cites S213: report the journal as "717 lines over 4 invocations (current 349)" so the scope is explicit.

## Commands (verbatim, read-only)

```
L=/run/user/1000/hypr/efb50993780079460b0cbed1363e2166a2de1d9f_1792804449_426444678/hyprland.log
stat -c '%s %y' "$L"; wc -l < "$L"                      # 4259033 2026-10-25 04:24:03.444802113 -0300 / 27331
grep -cF "overflowed event queue" "$L"                  # 0
grep -cF "failed writing event" "$L"                    # 0
grep -cF "Socket2 fd" "$L"                              # 0
grep -oE '^[A-Z]+( from [A-Za-z0-9_-]+)? \]' "$L" | sort | uniq -c | sort -rn
#  27280 DEBUG from aquamarine ] / 31 ERR from aquamarine ] / 21 DEBUG ]
grep -cvE '^[A-Z]+( from [A-Za-z0-9_-]+)? \]' "$L"      # 0
tail -c 1 "$L" | od -c | head -1                        # 0000000   N
awk 'END{print NR}' "$L"; grep -c '' "$L"               # 27332 / 27332
grep -cE '^[A-Z]+ \]' "$L"                              # 21
grep -nE '^[A-Z]+ \]' "$L" | tail -1 | cut -d: -f1      # 21
grep -nvE '^[A-Z]+ \]' "$L" | head -1 | cut -d: -f1     # 22
grep -nE '[Uu]sing config' "$L" | cut -d: -f1          # 12 18
grep -cF 'drm: getCurrentCRTC: No CRTC 0' "$L"          # 7
J() { journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat; }
J | wc -l                                               # 717
J | grep -cF "overflowed event queue"                   # 0
J | grep -cF "failed writing event"                     # 0
J | grep -cF "Socket2 fd"                               # 0
J | grep -cF "drm: getCurrentCRTC: No CRTC 0"           # 0
J | grep -ciF 'using config'                            # 4
hyprctl getoption debug:disable_logs -j                 # {"option":"debug:disable_logs","int":1,"set":false}
hyprctl getoption debug:enable_stdout_logs -j           # {"option":"debug:enable_stdout_logs","int":0,"set":false}
hyprctl version                                         # Hyprland 0.56.2 ... commit efb50993780079460b0cbed1363e2166a2de1d9f clean
journalctl --user -u <unit> -q -o json --output-fields=_PID,_SYSTEMD_INVOCATION_ID,_COMM   # per-pid/invocation counts (metadata only)
journalctl --user -u <unit> _SYSTEMD_INVOCATION_ID=<id> -q -o cat | wc -l / grep -ci 'using config' / grep -cF probe
```

## Remaining unknowns
- The receipt does not state its journal scope (all invocations versus the current one). The prompt asks for numbers only, so I report this as a scope finding, not as a FAIL.
- I could not resolve `skill://godspeed` from this harness and found no on-disk copy under `~/.omp`. I worked from the godspeed axes given in the task context.

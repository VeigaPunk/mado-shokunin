# SentPrivacy — round-47 receipt privacy (w1, 2026-10-26)

Target: what round 47 may commit from the live `xdg-terminal-exec --print-*` run under
`SKILL.md:343-344` rule 4 and `quality/check-session-material.py` R1-R4. Full method, instrument
table, rule rationale and the round-46 class scan: `w1/SentPrivacy/report.md`. Receipts,
`redact.py`, `sweep-privacy.py` and `live-ident.py`: `w1/SentPrivacy/`.

No session value appears in this file, that report, the receipts, or the tools.

## The rule (MADO-47-PRIV, proposed; the L1 freezes)

P1 `$HOME` replaces the account segment in every path; P2 `$WORK` for the seat scratch;
P3 `/run/user/<uid>`; P4 instance signature / `WAYLAND_DISPLAY` never printed (even
truncated); P5 env records keep only the seven resolver variables, forbidden keys dropped
whole, no `printenv` dump; P6 `PATH` is **replaced** (`<tool-bin>:<system dirs>`) because
a redacted inherited PATH still carries the login tool inventory and session-unique `fnm`
dirs; P7 host `mtime` as an age class, never an epoch; P8 strace reduced to
`execve("<basename>")` — no pid, no argv, no cwd; P9 host directory inventories are
prohibited outright, never merely redacted; P10 a receipt is committable only when the gate
reports no finding **and** the class scan reports zero.

## Measured

| sample receipt | gate R1-R4 | class scan |
|---|---|---|
| A raw — one `$HOME` path + contract env (the realistic receipt) | 0 findings | G2 |
| B raw — `find` of the applications dir (15 whole-line paths) | **R4 count=15** | G2 + G9 |
| C raw — `printenv` dump | 0 findings | G1 + G2 + G3 |
| D raw — `ls -1`, 30 bare names | 0 findings | G9 |
| E raw — strace with pids and argv | 0 findings | G2 |
| F raw — exact `mtime=<epoch>` | 0 findings | G11 |
| A/C/E/F redacted | 0 findings | 0 |
| B redacted | **0 findings** (R4 stops counting `$HOME/`) | **G9 survives** |

Clean-state control (raw samples removed, redacted receipts + tools only): gate
`files=18383 findings=115`, **0** in `.ufo/waves/round-47`; class scan all eleven zero.

## Round-46 committed files — what the gate misses

`.ufo/waves/round-46/` at `60edb66e`, 1300 files. Values never printed; locators in
`sweep-r46.txt` / `live-ident-r46.txt`.

- **F1 — S1, gate-blind, rule-4 violation, round-46's own.**
  `w1/LabVirtualRules/receipts/log-probe.txt:2` prints the live
  `HYPRLAND_INSTANCE_SIGNATURE` in full inside `/run/user/<uid>/hypr/<sig>/hyprland.log`.
  Introduced by `7f793280`; `git grep -l -F` finds exactly this one file in the whole tree
  at `60edb66e` (`signature-tree.txt`). Smallest remediation: substitute `<INSTANCE_SIG>`
  on that line — the probe's evidence is the two zero counts, not the path.
- **F2 — S2, gate-blind, carried.** `w1/ScrMistakes/receipts/d2-serial-count.txt:19,20`
  quotes the live monitor vendor string from the corpus line round-45 already flagged; R3
  needs a serial inside a JSON object, so a prose quote is invisible.
- **F3 — S3, residual.** 150 files / 532 absolute `$HOME` paths (machine-written
  `w1-*.json`, `registration*.md`, `make-w1-spec.py`); R4 counts whole-line dumps only.
- **F4 — S3.** 8 files / 12 `/run/user/<uid>/` occurrences.
- **F5 — S3, instrument gap.** No rule covers an `env` dump: shape C passes the gate while
  carrying the session D-Bus address, instance signature, `WAYLAND_DISPLAY`,
  `XDG_SESSION_ID` and session-unique `fnm` dirs.
- **F6 — S3, instrument gap.** Redaction defeats R4, and `ls -1` never needed redaction.

Clean classes in round 46: no secret shapes, no MAC, every e-mail `@scratch.invalid`, no
`/proc/*/environ` content, no inventories, no raw strace, no exact host mtime.

## For the wave to use

`ExecLive` carries the exposure (`--print-path`, file hashes under `$HOME`, cache
`sha256`+`mtime`); `ExecCounterC1`/`ExecOracle` report bwrap argv with `$WORK`/`$ROOT`;
`ExecStraceTrip` and `ExecCounterC1` commit strace; `ExecCache` must not commit the cache
body (it names the last selection — `live-cache-shape.txt` is the shape template). Any file
that *quotes* a receipt is itself a commit and must satisfy P1-P9.

Gate extension sketch for the L1 (`quality/` is out of this seat's scope): `R5_SESSION_IDENT`
(env assignment of the session pointers, `hypr/<32 hex>/`), extend `R4` to `^\$HOME/\S+$`
whole lines and to a >N block of bare `*.desktop` names, `R6_HOST_TIMESTAMP`
(`mtime=\d{9,}`), `R7_PID_TRACE` (`^\s*\d+\s+execve\(`). Positive and negative cases for
each are among the samples above; `sweep-privacy.py` is the union and is tested by them.

# R78Sentinel — safety / privacy / scratch audit, round 78 w1

Seat: R78Sentinel (sentinel, leaf). Scope: the two counters and the tool, every
receipt in `.ufo/waves/round-78/receipts/`, every committed fetch, and the wave's
own hygiene. Read-only throughout; no repo/scratch bytes were modified by this audit.
Observed 2026-11-04 ~09:20–09:37 UTC (the wave was live; commits advanced during the
audit — each fact below is pinned to the revision/blob it was taken from).

**Axes:** write-discipline · network/socket discipline · spawn discipline ·
environment hygiene · path refusal · session-material leakage · wave hygiene.

---

## 1. Instrument audit — tools/mado-barfoot.py, quality/counters/c1-r78-margins.py, quality/counters/c2-r78-runbook.py

All three share: no network code, no socket use, no undeclared process spawning.
The only spawns are `git -C <repo> show|rev-parse` (read-only), `python3 -I <tool>`
(selftest and per-case runs), and for C2 the 17 frozen read-verb probes from the
committed control set plus self-re-exec for mutants. Writes are confined to a
`tempfile.mkdtemp` workroot inside the caller's scratch root, removed in `finally`
(`c1-r78-margins.py:240,307-309`, `c2-r78-runbook.py:374,428-430`); both counters
refuse `/` and a symlinked scratch root (`c1-r78-margins.py:246-249`,
`c2-r78-runbook.py:371-376`). No traversal surface: fixture filenames are fixed and
control-set strings are data, not paths.

### W1 — LOW — tool selftest writes to the system temp dir (outside caller scratch)
`tools/mado-barfoot.py:560` `with tempfile.TemporaryDirectory() as td:` — the tool's
`--selftest` writes one throwaway `bad.json` into a `tempfile` dir. The C1 counter
invokes that selftest with a scrubbed child env (`c1-r78-margins.py:68-73` keeps only
PATH/LC_ALL/LANG/PYTHONDONTWRITEBYTECODE; TMPDIR is dropped), so the dir lands in
`/tmp`, not the caller's scratch.
Command showing the defect:
`env -i PATH=/usr/bin:/bin python3 -c "import tempfile; print(tempfile.gettempdir())"` → `/tmp`.
Impact: transient unique-named dir, auto-removed; no fleet/scratch pollution. Class:
"writes outside caller scratch" — real but low.

### E1 — INFO — C2 counter passes the full caller environment to every probe child
`quality/counters/c2-r78-runbook.py:72` `env = dict(os.environ)` in `session_env()`
(vs the C1 counter's scrub at `c1-r78-margins.py:68-73`). The runbook probes need the
session vars it completes (`XDG_RUNTIME_DIR`, `HYPRLAND_INSTANCE_SIGNATURE`,
`OMARCHY_PATH`, PATH extension, lines 73-105), but the whole environment — e.g.
SSH/D-Bus agent vars when present — goes to each child. `git_show`/`rev-parse`
subprocesses (lines 255-260, 389-397) also inherit unscrubbed. Nothing is printed.
Severity: low/informational; narrow to a whitelist if the lane wants parity with C1.

### E2 — OK — instance-signature discovery is read-only and never printed
`c2-r78-runbook.py:88-97` lists `$XDG_RUNTIME_DIR/hypr/` for `.socket.sock` to set
`HYPRLAND_INSTANCE_SIGNATURE` when unset. Directory read only; the value never
reaches stdout (verified: no signature string in any receipt). Compliant with the
"never print an instance signature" rule.

### Path refusals (verified present)
- Tool: `read_bytes` does `os.lstat` + `stat.S_ISREG` (`tools/mado-barfoot.py:75-82`) —
  symlinks, directories and FIFOs are refused ("refused non-regular path"); a 1 MiB
  cap (`MAX_BYTES`, line 30) bounds reads. `/` itself fails the S_ISREG test.
- Counters: `/` scratch root and symlinked scratch root refused (lines cited above).

---

## 2. Receipt + fetch session-material audit (gate rules R1–R6)

Method: imported the gate's own `scan_blob` from `quality/check-session-material.py`
and ran it over **all 59 files** in `receipts/`, `fetch/`, and `w1/` (including seat
scripts and reports), then over every committed git blob of
`receipts/measurement-c2-r78.txt`. R6 was armed with the host serials read via
`hyprctl monitors all -j` — counts only, values never printed or persisted
(host_serials_count=1).

### F1 — HIGH — host monitor serial-shaped token committed in git history and live in a seat's report file
- Gate verdict on committed blobs:
  `git show 44a36b64:.ufo/waves/round-78/receipts/measurement-c2-r78.txt` →
  `R5_SERIAL_PROSE tokens=1 shapes=9x3+Ax5+9x4` (same at `19aefc3d`; `fc276ed6` and
  `e117a113` clean).
- Leaky bytes (committed `f71b03e2..19aefc3d`, 14 revisions incl. the frozen
  amendment `44a36b64`), one line, truncated by `observed()` at 100 chars:
  `MADO_R78_PROBE: name=monitors-dump ... out='[{"id":1,\n "name": "DP-1",\n "description": "LG Electronics LG ULTRAWIDE SERIAL-REDACTED"...'`
- Rule: **R5_SERIAL_PROSE** (`quality/check-session-material.py:226`,
  `(?<![0-9A-Za-z])[0-9]{2,6}[A-Z]{3,8}[0-9]{3,7}(?![0-9A-Za-z])`; the token
  `SERIAL-REDACTED` = 9x3+Ax5+9x4). R3 would also fire on the untruncated dump
  (serial + description object); the 100-char cut happened to stop before a
  `"serial"` key. Matches the seat criterion "monitor serials".
- Cause: pre-`90fc8d84` C2 counter quoted raw probe dumps in receipts; fixed by the
  `observed()` json-bytes repair (commit `90fc8d84`, blob d15b8300 → later 9171bb36 →
  7e7fdc94), which is why current receipts are clean.
- **Live propagation:** the wave report dir carries a copy of the leaky freeze
  receipt — `w1/R78ExecC2Cases/receipt-frozen-counter-at-44a36b64.txt` scans
  `R5_SERIAL_PROSE tokens=1 shapes=9x3+Ax5+9x4` TODAY (untracked but seat-visible and
  committable by the close sweep).
- Smallest remediation: drop or replace that seat copy with the redacted
  (`json-bytes=`) form; treat the 14 historical blobs as leaked if this repo is ever
  pushed/shared (local rewrite or acceptance is a Main/orchestrator call — git writes
  are outside my seat).

### F2 — LOW/INFO — live layer capture carries pids and surface addresses
`fetch/live-layers-r78.json:14,28` `"pid": 1722 / 1720` and `:7,21`
`"address": "0x55af…"` — hyprctl layers rows pair each pid with its surface
namespace and a memory address. Gate: **CLEAN** (R2 needs `users:(("prog",pid=` ss
rows; nothing in R1–R6 covers layer rows). Seat criterion "pids paired with names":
pairable in-object, hence reported. The receipt's header documents the monitors
reduction but not this. Remediation: optional — strip `pid`/`address` as was done for
the monitors capture.

### F3 — INFO — receipts print one bare live pid and benign host values
`measurement-c2-r78.txt` (HEAD and worktree): `name=waybar-process … out='1720'` —
a live pid; the row label supplies the program name (R2 shape absent). Also
`out='DP-1 3440x1440@99.99700'` (connector + mode), theme `Matte Black`, layout
`str: br`. None of these are R1–R6 findings; listed for completeness.

### F4 — INFO — one absolute home path per census receipt
`census-start-r78.txt:46` and `census-end-r78.txt:46` each carry one bare line
`mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`. Gate-clean
by design (R4 needs >10 distinct path lines; R7 deliberately excludes bare path
lines). Not a home listing.

### Everything else — CLEAN
All current receipts (`census-start/end`, `control-baseline-c1/c2`, `live-join`,
`measurement-c1/c2` at HEAD `3eb518a5`), all 16+ fetch artifacts (`S457.bin … S473`,
`live-layers`, `live-monitors`, `sha256-r78.txt`), and all w1 seat files scan clean
under R1–R6 (R6 with the live host serial armed — zero matches). No client dumps, no
process tables, no monitor-ident JSON, no home listings, no R7–R9 forms anywhere in
the round's new prose.

---

## 3. Wave hygiene

- **No seat-visible path writes into the fleet repo.** Every seat artifact lands
  under `.ufo/waves/round-78/w1/` (untracked); `swarm-registry.json` `reportDir` is
  `.ufo/waves/round-78/w1`. Seat scripts inspected (`R78ExecC2Shapes/c2-r78-runbook-attack.py`,
  `shape-diff.py`, `R78ConnSiblings` copied receipts) write nothing outside their own
  scratch/seat dir. Tracked-file worktree modifications during the audit
  (receipts, SCORECARD.md, SKILL.md, quality/tool-ledger.md) were the orchestrator's
  own close-out, not seat-visible paths.
- **H1 — LOW — shared scratch tree left behind.**
  `/fast/scratch/hyaku/mado-r78/c2/c2-r78-9sx66uad/mutant-rc-blind.py` and
  `mutant-int-range-lower-open.py` — a C2 counter workroot whose `finally: rmtree`
  was bypassed (hard kill/timeout during the mutant phase; cleanup is best-effort by
  design). Command: `find /fast/scratch/hyaku/mado-r78/c2 -mindepth 1`.
  Remediation: orchestrator may `rm -rf` that workroot; content is counter-mutant
  source only (no session material).
- **Secret-shaped strings:** `grep -rnE "ghp_|sk-…|AKIA…|BEGIN .*PRIVATE KEY|api[_-]?key…|secret…|password…|token="` across
  `.ufo/waves/round-78/` — no matches in any receipt, fetch, or seat prose.

## 4. Instrument freeze lineage (facts for Main)

Verified `sha256sum` of on-disk bytes vs `git show <rev>:<path>` across revisions:

| instrument | assignment pin | state |
|---|---|---|
| tools/mado-barfoot.py | aac5d41b…09c0 | blob identical at 44a36b64, 90fc8d84, e117a113, HEAD — **never rewritten** |
| c1-r78-margins.py | 1c39a53c…5000 | blob identical at 44a36b64 → HEAD — **never rewritten** |
| c2-r78-runbook.py | b9c774b8…743a (44a36b64) | d15b8300 at 90fc8d84 (observed() json-bytes privacy) → 9171bb36 at d27c5ff4 (row-bound anchor check) → 7e7fdc94 at aea5409e (matcher hardening from the wave attack) |

All three C2 repairs are the declaration's allowed class: `CASES=17 / SHAPES=12 /
MUTANTS=5` and the `MUTATIONS` block are byte-identical in all four revisions
(block sha256 `6e739580…` throughout); `90fc8d84` touched only receipt printing,
`d27c5ff4` only the setup-time anchor validation (strictness increase — can only
refuse a setup, never weaken a clause), `aea5409e` only matcher acceptance. No
predicate, case, label, kill rule or target changed. Note: the assignment's pin
table is stale relative to the live instrument; the last committed measurement
(`3eb518a5`) reports C1 18/18, mutants 7/7, base 8/18, selftest 22/22 TARGET_MET
rev=d27c5ff4 tool=aac5d41b, and C2 17/17, shapes 12/12, anchors 17/17, control 5/17,
mutants 5/5 TARGET_MET rev=d27c5ff4, with a re-measurement at aea5409e in flight.

Frozen checksums verified matching at audit time: tool aac5d41b, counters
1c39a53c / b9c774b8→live 7e7fdc94, controls 99f1d82f (C1) and f1c75a7d (C2).

---

## Summary

1. **F1 (high):** the host monitor's serial-shaped token sat in
   `measurement-c2-r78.txt` for 14 committed revisions (f71b03e2..19aefc3d, R5
   shape 9x3+Ax5+9x4), was fixed by the json-bytes privacy repair, but is still
   live today in `w1/R78ExecC2Cases/receipt-frozen-counter-at-44a36b64.txt`.
2. Instruments are write-contained, network-free, socket-free and spawn only declared
   read verbs; defects found are low-grade: a `/tmp` write in the tool selftest (W1),
   full-env pass-through in the C2 runbook (E1), pids/addresses in the live layers
   capture (F2), and one leftover counter workroot in shared scratch (H1).
3. No fleet-repo write paths, no home listings, no process tables, no secrets; the
   three post-freeze C2 counter repairs preserved every frozen predicate, case,
   label, kill rule and target.

Report: .ufo/waves/round-78/w1/R78Sentinel.md

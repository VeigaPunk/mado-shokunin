# REAL session material at base `03e4ae76` — remediation proposal (M48-8 part 2 input)

Scope: the 40 findings triaged `REAL` in `triage.tsv` (13 × R2, 3 × R4, 24 × R5). Every line names a class
only — no title, serial, program name, pid or home path appears below. Findings were produced by
`quality/check-session-material.py` at `03e4ae76` (`receipts/01-gate-base-scope-ufo.txt`,
`receipts/02-gate-base-scope-all.txt`).

Two events matter before any removal: **counters are frozen** after w1 (claims.md: "predicates, counters,
fixtures and controls freeze … before any data commit"), and **two of the REAL receipts are inputs of pinned
counters at a pinned revision**. So each option below states what it breaks.

## 1. R2_PROC_TABLE — 13 files (live socket/process rows)

| # | file | count | machine readers |
|---|---|---|---|
| 1 | `.ufo/waves/round-37/receipts/eventq-live-ss.txt` | 5 | `quality/counters/c2-r37-eventq.py:17,39` (`LIVE_SS`, replayed at a revision) |
| 2 | `.ufo/waves/round-37/w1/scratch/ExecEventqA/live-ss.txt` | 5 | none (grep of `quality/`, `tools/`) |
| 3 | `.ufo/waves/round-38/receipts/eventq-live-ss.txt` | 715 | `quality/counters/c2-r38-eventq.py:25,60-61,226-231` (`LIVE_SS` replayed, and pids bound to `LIVE_PROC` for AGREE) |
| 4 | `.ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt` | 5 | none |
| 5-13 | 9 reports quoting rows (round-37 `res/reports/L1Mado37-2.CritEntryE2.md`, `w1/reports/{ExecEventqB,ExecProcCrosscheck,RevC2Code,ScoutRollingLog,ScoutSsSemantics}.md`; round-38 `w1/reports/{RevC2v3,RevLiveTriplet,ScoutR29Refusal}.md`) | 1-5 each | none |

**Proposal A1 (files 1 and 3, the counter inputs) — census-only regeneration, then re-pin.**
The round-38 outside check already routed exactly this: "Regenerate `receipts/eventq-live-ss.txt` as a
census-only snapshot (SentSocketSafety HIGH); commit the eventq counter's after-receipt"
(`corpus/lessons/round-38-verifier-spotcheck.md:86`; the original find is `:43`, which also records that a
minimal export still passes the counter's `full_table` clause). Concretely: regenerate both snapshots in the
counter tool's census-only form (row identity, ports, queues and inode bindings kept; program names and pids
dropped or replaced), then update the two counters' pinned replay/AGREE pairs in the **same** freeze —
`c2-r38-eventq.py:226-231` compares the snapshot's pid to the `/proc` artifact, so a pid-free snapshot changes
that verdict from AGREE to whatever the new rule states. This is an L1 sequencing decision, not a seat edit.
Pre-image digests for the removal receipt (blob sha256 at `03e4ae76`):
`fee7629de526b2226b6b4a20b8de3e863ad82867ddaa322e7113745338e795be` (file 1) and
`653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b` (file 3).

**Proposal A2 (files 4, 5-13 and 2, no machine reader) — line-preserving redaction.**
Rewrite the program field to `fixture-prog` and the pid field to `0` (same byte length not required; line
count and column layout must survive so the reports stay readable as evidence), commit with a receipt holding
the pre-image sha256. No counter or tool reads these paths (checked: `grep -rn <path> quality/ tools/` returns
nothing), so the only harm is that the quoted rows stop being verbatim — the reports already say they quote.

**Proposal A3 — retain and declare.** Keep them, print the count in the lesson, and accept a red gate for
ever. This contradicts M48-8's purpose and leaves `findings=159` standing; listed only for completeness.

## 2. R4_HOME_LISTING — 3 files (bare `/home/<user>/...` line blocks)

| file | count | digest pin that a redaction invalidates |
|---|---|---|
| `.ufo/waves/round-35/scratch-evidence/SentProvenance/S203.scope.txt` | 12 | none |
| `.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt` | 40 | `.ufo/waves/round-43/w1/ExecLiveHost.md:12` (`f6aeb6388984…`), `.ufo/waves/round-43/w1-results.json` |
| `.ufo/waves/round-48/w2/RevMisroot/check2-fleet-byte-scan.txt` | 15 | none |

**Proposal B — rewrite the home prefix to `~/`, keep every line and its number.**
`HOME_PATH_RE` (`quality/check-session-material.py`) only matches *absolute* `^/home/<user>/…` lines, so a
`~/…` prefix clears R4 without deleting the census. Line count is preserved, so the citations that pin a line
number stay true: `.ufo/waves/round-43/w1/ExecLiveHost/live-census.txt:232` is cited by
`corpus/lessons/round-43.md:222` and `corpus/lessons/round-44.md:69` (both quote a windowrule line, not a home
path). The two digest pins above must be updated or annotated "pre-redaction bytes" in the same commit.
No tool parses these files (`grep -rn` over `quality/`, `tools/`: none).

## 3. R5_SERIAL_PROSE — 24 files (one host monitor-description token)

| group | files | findings |
|---|---|---|
| live corpus entries | `corpus/knowledge/config-health-report-r3.md:149`, `corpus/knowledge/hyprctl-verification-layer.md:153`, `corpus/knowledge/hyprland-config-plane.md:184` | 3 |
| wave copies of the same three entries (byte-identical snapshots) | `round-32/assimilation/validate/…`, `round-32/c1/controls/{a-rows-only,b-entries-only}/…`, `round-32/scratch/MutExistingGates/fixtures/{tree-m1,tree-m2,tree-m2b}/…`, `round-37/w1/scratch/ScribeRows/validate/…` (7 dirs × 3 files) | 21 |

The token is the host monitor description's serial segment, quoted as a live read inside a `desc` field
(`hyprland-config-plane.md:184` reads "…, scale 1. Config declares `3440x1440@100` (`monitors.conf:10`)" on the
same line). It is the one REAL item the round-48 spotcheck called "held corpus/knowledge prose serials"
(`corpus/lessons/round-48-verifier-spotcheck.md:191`).

**Proposal C — replace the 12-char token with `<serial-redacted>` in all 24 files, same commit.**
Verified safe: no counter, tool or quality script reads the token or those line numbers
(`grep -rlF <token> quality/ tools/ corpus/ SKILL.md` → the three corpus entries only), and `corpus/README.md`
indexes the entries by path/title, not by digest. The historical manifest pins that would name the old bytes are
`.ufo/waves/round-20/w2/ScribeShonen/pointer-check.txt:41`,
`.ufo/waves/round-43/w1/ExecLocatorGate/knowledge-base-manifest.txt:9,24` and
`.ufo/waves/round-13/w1/reports/PriorIntent.md:35`; each is a dated snapshot and reads correctly as "at that
revision", but the L1 should say so in the same commit rather than leave a silent mismatch.
Do the 21 wave copies *and* the 3 live entries together: the copies claim byte equality with the entries, so a
partial edit creates a false "same bytes" claim.

## 4. Not proposed: waiving any of them

Measured (`receipts/04-…`): no marker path reaches a REAL file. `W4b` refuses a non-reserved value, the serial
rules are refused with `reason=serial-rule-not-waivable` before the marker is parsed, and `W1` refuses any path
outside `.ufo/waves/` (so the three live corpus entries can never be waived at all — which is the intended
design: only removal/redaction is allowed for them).

## 5. Ordering and harm summary

1. **C** (corpus serial) — no consumer, lowest risk, clears 24 findings.
2. **B** (home listings) — no consumer, needs two digest-pin updates, clears 3 findings (67 paths inside).
3. **A2** (11 ss/report files, no reader: 40 findings over 5+5+30 rows) — clears 40 findings.
4. **A1** (2 counter inputs) — must land with a counter re-pin; clears 720 rows (5 + 715) in 2 findings.
Done in that order the gate's REAL residue is zero, and the only re-pinning needed is `c2-r37`/`c2-r38` plus the
two round-43 digest pins. If A1 is deferred, the gate keeps 2 R2 findings and the reason is a frozen counter,
not an unseen leak — say that in the lesson rather than leaving it silent.

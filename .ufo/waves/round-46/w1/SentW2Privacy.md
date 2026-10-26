# SentW2Privacy — round-45 committed evidence, privacy sweep (round-46 w1)

Target: `.ufo/waves/round-45/` at `4d22eeb66c2835af8aaa3fac6ad838fa616aa663` (741 files), read from the
object database only. Full report, method, gate parity table and reproduction commands:
`w1/SentW2Privacy/report.md`. Evidence: `w1/SentW2Privacy/receipt-sweep-r45.txt`,
`receipt-sweep-ufo-selective.txt`, `receipt-gate-r45.txt`, `receipt-quotes.txt`, `receipt-leakcheck.txt`.
No session value appears in this file, that report, or those receipts.

## What round-45 evidence carries

| class | round-45 (741 files) | gate at 4d22eeb | note |
|---|---|---|---|
| live monitor serial | 0 | 0 | clean |
| live monitor description | 0 | 0 | clean |
| live monitor **make** (vendor) | **6 files** — S2 | 0 | R3 needs a serial in a JSON object |
| live monitor **model** | **2 files** — S2 | 0 | same blind spot |
| client titles | 0 real | 2 findings, self-referential | upstream C++ literals + gate's own fixtures + one `REDACTED` mutant |
| process tables | 0 real | 1 finding, self-fixture | gate's own two `ss` selftest rows |
| home listings (whole-line dumps) | 0 | 0 | clean |
| home paths (account name) | 151 files / 651 occurrences | 0 | R4 counts whole-line dumps only — S3 |
| tokens / keys | 0 | (no rule) | clean |

## Findings

- **S2 (medium, round-45's own).** The host's real monitor vendor and model are verbatim in six round-45 files,
  all introduced by round-45 commits (`7c0b0035`, `22a8dedd`): `w1/CritPremise/receipts.txt:5,17,20`,
  `w1/ExecLiveHost/verify-quotes.py:48`, `w1/ExecSeedSweep/name-anchors.txt:2,3,9`,
  `w1/ExecDoNothingC1/control-a-lookup.py:206`, `w1/ExecDoNothingC1/control-a2-obfuscated.py:34`,
  `w1/MutC1Counter/c1-r45-monitors.py:255`. Carrier: a fixture vocabulary that baked in the host vendor.
  Same strings in the frozen, published `quality/counters/c1-r45-monitors.py:255` and
  `c1-r45-monitors-v2.py:202`. Verified by exact equality with `hyprctl monitors all -j`; the gate cannot see
  them (R3 requires a serial inside a JSON object).
- **S1 (high, outside the assigned tree, pre-existing).** The published corpus still carries the host's real
  serial: `corpus/knowledge/config-health-report-r3.md:149` and `corpus/knowledge/hyprctl-verification-layer.md:153`
  (serial + description triple), `corpus/knowledge/hyprland-config-plane.md:184` (serial) and `:183` (model).
  Added in probation rounds, untouched by round-45, and invisible to the gate, whose scope is `.ufo` only.
  Remediation is L1's call; this seat has no edit scope.
- **S3 (low).** 151 round-45 files carry the account segment in absolute paths (largest:
  `w1/SentTool/raw/r10-scratch-discipline.txt`, 31 such lines). Residual, not new: 4,639 `.ufo` files carry it at
  both `b22ea56` and `4d22eeb`.

## Gate comparison

`quality/check-session-material.py` at 4d22eeb is byte-identical to the working-tree gate
(`sha256 889f8f05…`): `files=17070 findings=97`; scoped to round-45, **49 finding lines over 47 files**
(R1 2, R2 1, R3 46) — **all 49 false positives for rule 4**: the gate's own selftest fixtures, one `REDACTED`
mutant, and 45 fixture JSONs that share a single synthetic identity. On the same `.ufo` scope my classes
reproduce the gate rule-for-rule (`C1_TITLE_OBJECT`=R1=23, `C5_PROC_TABLE`=R2=26, `C4_SYNTH_IDENT`=R3=46,
`C6_HOME_DUMP`=R4=2); the deltas are the gate's blind classes (live-identity comparison, path occurrences) and
its `.ufo`-only scope.

## Positive verification

- **D1 is closed at 4d22eeb**, contrary to round-45's own report: both round-43 dump blobs are the 7-key
  projection (`4c7fe8e3`, 0 `"title"` lines; they were 4 title lines each at `ebdba13`), the gate lists neither,
  and round-45's nested copies under `w1/ExecProjectTitles/proj/` are the same clean blob. The stale statement is
  `.ufo/waves/round-45/w1/ExecPrivacyGate/report.md:102` ("with the same 50 files: D1 is still unfixed").
- Round-45's live receipts and its own R3 control stayed shape-only: they contain none of the host's identity
  strings.

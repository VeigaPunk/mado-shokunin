# mado round 95 — claims declaration (DRAFT for wave w1; frozen at the freeze commit; the L1 MadoR95 owns it)

Base: `master` at `4a2af6817024f6ed47084a5217c1825ae247f4fe` (round-94 closure tip). Lowest-axis duty: every owned axis
scores 10 (round-94 SCORECARD), so the duty is a tie; stagnation nudge not claimed (a capability entered at round 94).
Sourced claim: C1 (rows opened by the L1 this round: `.ufo/waves/round-95/receipts/sources-open-r95.txt`; S516, S517, S518
re-opened). Round-94 spot-check routed defects: defect 3 (kill-sets for five unguarded tools) → C2 for two of them;
defects 1, 2, 4 are not claims this round and defect 5 (QUALITY 154) is applied to this declaration's caller sentence —
reasons in `corpus/lessons/round-95.md`. considerthese `2026-11-06.md` proposal 4 ("widen desktop coverage") → C1.

## C1 — coverage (new surface, capability): file bytes → MIME type as GLib sniffs them

Surface moved: the content step of GLib's type guess. Round 94 answered `g_content_type_guess (name, NULL, 0)` (name
only); no lane tool reads the magic section of `mime.cache` or answers a guess that is given data
(`git show 4a2af681:tools/mado-mimesniff.py` → absent; `grep -l magic tools/*.py` names no reader of the magic section).

Caller scope (QUALITY 154): this claim says what GLib 2.90.1's `g_content_type_guess (name-or-NULL, data, len,
&uncertain)` returns. It names no caller; which programs call it with data on this host is the connector's item and
enters the knowledge entry only with the caller's own lines.

Tool `tools/mado-mimesniff.py` = frozen candidate `.ufo/waves/round-95/build/mado-mimesniff.c1*.py` (draft
`mado-mimesniff.c1.py`, sha256 `a13b6e0e3b0c399892ff027309f942daa96e92713851e8d8cfb736b277cde99d`); it loads round 94's
`tools/mado-mimeglob.py` (sha256 `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`, unchanged) from its
own directory for the name step. Cache mode only; text mode (no loadable `mime.cache`) is refused, exit 3.

Draft inputs (frozen paths, filled by w1):

| input | path |
|---|---|
| oracle source | `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` (sha256 `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a`) |
| cases | `.ufo/waves/round-95/controls/mimesniff-cases-r95.json` |
| fresh generator | `.ufo/waves/round-95/controls/mimesniff-fresh-r95.py` |
| host file list | `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` |
| mutants | `.ufo/waves/round-95/controls/mimesniff-mutants-r95.json` |
| counter | `quality/counters/c1-r95-mimesniff.py` |

**PRED-C1-r95-v1 (draft)**: TARGET_MET iff, at `<rev>`, `tools/mado-mimesniff.py` is the frozen candidate and
`tools/mado-mimeglob.py` is round 94's bytes (`tool_pin=ok`), and (i) on every frozen case the tool's (type, uncertain)
equals the oracle's label (a case labelled `UNSUPPORTED` — the oracle crashes or hangs — requires exit 3), and the oracle
re-run at measurement equals the recorded label (else SETUP_ERROR); each of the 20 classes `zerosize fallback lltext
order prio multicache range mask nest bounds wrap desktop name1 name0 nameN subclass alias slash mode real` holds ≥ 6
cases (`classes=20/20`); (ii) on 120 fresh seeded cases from the frozen generator the tool equals the live oracle;
(iii) on every readable file of the frozen host list, sniffed (first 4096 bytes) data-only and with its own path as the
name, under the counter's HOME/XDG environment, the tool equals the live oracle (host database digests printed);
(iv) every one of the ≥ 40 counted mutants makes at least one frozen case wrong (a crash is `crashed_not_killed`);
(v) each control misses (i): do-nothing (`application/octet-stream`, 1), the name-only answer of round 94's
`tools/mado-mimeglob.py` (data ignored), a naive sniff (first matching top-level value at its range start, cache order,
no priority/mask/children/subclass), and the base revision (no tool → 0); (vi) `static_no_external_resolver=ok`
(QUALITY 162, refined): no subprocess/socket/multiprocessing/pty/urllib/http/xmlrpc/ctypes import in the tool, no
`os.system/popen/exec*/spawn*/posix_spawn*/fork*`, no `eval/exec/compile/__import__`; its only dynamic import is
`spec_from_file_location` of `mado-mimeglob.py` in its own directory, and the counter places the pinned round-94 file
there; every tool run gets `PATH` = an empty directory.

Before → after: frozen cases answered as GLib does, base **0/N** (no tool) → **N/N**. Kill rule: any conjunct false →
TARGET_MISSED; never narrowed after data.

L1 pre-wave DRAFT probe (not a measurement): 3620 host files under /usr (every 97th readable file, sorted) × (data-only,
own path) = 7240 inputs, draft candidate vs the compiled oracle, 0 differences; candidate `--selftest` 23/23.

## C2 — operability: the selftest-strength gate guards two more lane tools

Round-94 spot-check routed defect 3: five lane tools are still without kill-sets. This claim lands
`quality/selftest-kills/mado-mimeglob.json` for `tools/mado-mimeglob.py` (19 checks, FAIL prefix
`MADO_MIMEGLOB_SELFTEST_FAIL: `) and `quality/selftest-kills/mado-portals.json` for `tools/mado-portals.py` (sha256
`e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021`, 28 checks, `MADO_PORTALS_SELFTEST_FAIL: `). The gate
stays the round-93 frozen gate `quality/check-selftest-strength.py` (`2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b`);
both tools unchanged. The gate's own selftest is not guarded this round: its `non_selftest_prefix` cuts its own source at
the first `def selftest(` text, a string at line 73, so no kill can land in `gate()` (lesson M95-1; routed).

**PRED-C2-r95-v1 (draft)** = PRED-C2-r94-v1 with the two tools above: TARGET_MET iff, at `<rev>`, the gate is the frozen
gate, both kill-sets are the frozen candidates, and (i) the gate on each unmodified tool prints OK rc 0 and each
kill-set's `tool_sha256` equals the tool at `<rev>`; (ii) for each of the 47 selftest checks (19 + 28), the tool with
that one check forced to pass makes the gate print WEAK rc 1; (iii) each frozen hand weakening of the panel → WEAK rc 1;
(iv) each frozen neutral edit → OK rc 0; (v) controls: do-nothing instrument flags fewer than (ii)+(iii), always-OK
flags none, always-WEAK fails (i), sha-diff fails (iv); (vi) the gate's `--selftest` exits 0; (vii) the round's
first-draft kill-sets flag strictly fewer hand weakenings than the frozen ones.

Before → after: single-check neutralisations of the two tools' selftests flagged by a lane instrument **0/47** (no
kill-set; do-nothing instrument) → **47/47**.

## Separability

C1 lands a new tool, entry and rows; C2 lands two kill-set JSON files. C1 is measured at its own commit (before C2); C2's
counter at the C1 commit must stop SETUP_ERROR (kill-sets absent); C1's counter at the C2 commit must still be
TARGET_MET. C2 does not guard the C1 tool (it would depend on C1). C1 reads `tools/mado-mimeglob.py`, which C2 guards
without changing.

## Named limits (declared before data)

- C1: cache mode only (text-mode `magic` files refused); data as passed (no file reads, no sniff-length policy of
  callers); labels from glib2 2.90.1-1 / shared-mime-info 2.5.1-2 as installed; C undefined behaviour refused.
- C2: panel weakenings and closing kills from the same wave (design set); the gate's own selftest, `tools/mado-mako.py`,
  `tools/mado-verify.sh` and `quality/check-receipt-presence.py` stay without kill-sets.

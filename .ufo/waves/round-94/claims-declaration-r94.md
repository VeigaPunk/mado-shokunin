# mado round 94 — claims declaration (FROZEN at the freeze commit; the L1 MadoR94 owns it)

Base: `master` at `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` (round-93 closure tip). Dispatch-evidence commit
`5a164538438c2f101e44a79ad9e05aaf3ca910fb` carried the draft of this file (same claims, unamended predicates).
Lowest-axis duty: every owned axis scores 10 (round-93 SCORECARD), so the duty is a tie; stagnation nudge not claimed (a
capability entered at round 93). Sourced claim: C1 (rows S515–S518 opened by the L1 this round, S505 re-opened:
`.ufo/waves/round-94/receipts/sources-open-r94.txt`). Routed defects of the round-93 spot-check: defect 2 → C2;
defects 1 and 3 are not claims this round (reasons in `corpus/lessons/round-94.md`). considerthese `2026-11-06.md`
proposal 4 ("widen desktop coverage … prefer one operator-config gap") → C1.

Amendments folded in before any measurement (all from wave w1, all before the freeze; the draft predicates are in
`5a164538`): C1 — the class clause enumerated (R94MCritic C1-F1), a static no-external-resolver conjunct and an empty
PATH for every tool run (C1-F2), a mutant minimum (C1-F3), both naive readings scored (C1-F4), host database digests
printed (C1-F5), `--home-unset` mapped; the candidate revised after R94MReviewC1 F1–F7 (the wave candidate
`build/mado-mimeglob.c1.py` stays as a control). C2 — the panel widened to the wave's 91 green hand weakenings and a
first-draft-kill-set control conjunct (vii) (R94MCritic C2-F1/F4, R94MReviewC2 §3, R94MMutC2 §2); the kill-sets gain
R94MMutC2's 19 closing kills.

## C1 — coverage (new surface, capability): file name → MIME type as GLib guesses it

Surface moved: the name-to-type step before every default-application answer (rounds 91–92 resolve type →
application; at base no lane tool answers name → type: `git show a3de9972:tools/mado-mimeglob.py` → absent).

Tool `tools/mado-mimeglob.py` = frozen candidate `.ufo/waves/round-94/build/mado-mimeglob.c1b.py`, sha256
`65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`: what GLib 2.90.1
`g_content_type_guess (name, NULL, 0, &uncertain)` answers (type and uncertain flag) from the shared-mime-info
databases — xdgmime's directory list, cache mode vs text mode, literal / simple-suffix / fnmatch globs, ASCII folding
and `cs`, deepest suffix (per cache in cache mode), weights, merge and sort, trailing `/`, none/one/several.

Frozen inputs (sha256):

| input | path | sha256 |
|---|---|---|
| cases (370: R94MExecCasesC1 235, R94MReviewC1 51, R94MProbeC1 24, R94MMutC1 55, L1 5) | `.ufo/waves/round-94/controls/mimeglob-cases-r94-frozen.json` | `c7b693d240479ed63af24f426ae184bc4a13489a38f587620d9e1224dca5856c` |
| mutants (60 counted, 11 equivalent/crash-shaped with arguments) | `.ufo/waves/round-94/controls/mimeglob-mutants-r94-frozen.json` | `0e74c57d233d2440f903466e959488705a58fdcda4f14d920caef0d2859133c2` |
| oracle source | `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c` | `9c4337b36f93fa71bce13938f93d2e9758bb752815a67c57eb934a70bbfa6b11` |
| fresh generator | `.ufo/waves/round-94/controls/mimeglob-fresh-r94.py` | `ab76b97e0c37d92ddb0b03a733745b1089be2a083379d9cabee050689ed57e2c` |
| host names (9745) | `.ufo/waves/round-94/controls/mimeglob-host-names-r94.txt` | `4b6d6a6cc67a4ad59eb91c9e8af1cc605f2f278d2a2ecf57b4a81edad9344fa3` |
| counter | `quality/counters/c1-r94-mimeglob.py` | `aeda812eac5f523274034e2a9b4317c63e96dabe6bd0602cf75cc8ce48455433` |

Counter argv: `python3 -I quality/counters/c1-r94-mimeglob.py --repo . --rev <rev> --base-rev
a3de997289014e7dbf1d73ae206be1d6f8cdadd0 --cases <cases> --expect-cases-sha256 c7b693d2… --mutants <mutants>
--expect-mutants-sha256 0e74c57d… --oracle-src <oracle> --expect-oracle-sha256 9c4337b3… --fresh-gen <gen>
--expect-fresh-gen-sha256 ab76b97e… --host-names <names> --expect-host-names-sha256 4b6d6a6c… --expect-tool-sha256
65f80a6c… --fresh 120 --workers 24 --scratch-root DIR` (full digests above).

**PRED-C1-r94-v1** (the counter's docstring holds the same text): TARGET_MET iff, at `<rev>`, `tools/mado-mimeglob.py` is
the frozen candidate (`tool_pin=ok`) and (i) on every one of the 370 frozen cases the tool's (type, uncertain) equals
the oracle's label, and the oracle re-run at measurement equals the recorded label (else SETUP_ERROR); both modes are
present and each of the 20 classes `dirs mode literal simple full fold cs deep weight dupe order multi nomatch slash
bytes fgets v1 noglobs cachefmt mixed` holds ≥ 6 cases (`classes=20/20`); (ii) on 120 fresh seeded cases from the
frozen generator (seed printed) the tool equals the live oracle; (iii) on the 9745 host names under the counter's own
HOME/XDG environment the tool equals the live oracle (host database digests printed); (iv) every one of the ≥ 40 counted
mutants makes at least one frozen case wrong (a crash is `crashed_not_killed`, never killed); (v) each control misses
(i): do-nothing (`application/octet-stream`, 1), the naive extension map (last `.ext` → highest-weight `*.ext` type in the
dirs' globs2, uncertain 0, scored exact and ASCII-folded, the stronger counts), the base revision (no tool → 0);
(vi) `static_no_external_resolver=ok`: no subprocess/socket/multiprocessing/pty/importlib/urllib/http/xmlrpc import, no
`os.system/popen/exec*/spawn*/posix_spawn*/fork*`, no `eval/exec/compile/__import__`, every ctypes library named is libc;
every tool run gets `PATH` = an empty directory.

Before → after: frozen cases answered as GLib does, base **0/370** (no tool) → **370/370**. Kill rule: any conjunct false
→ TARGET_MISSED; never narrowed after data.

Pre-freeze controls (`.ufo/waves/round-94/receipts/c1-controls-prefreeze-r94.txt`, seed 4242, fresh 60): candidate
`DRAFT_TARGET_MET` 370/370, fresh 60/60, host 9745/9745, 60/60 mutants, do-nothing 43, naive 63, base 0; wave
candidate `c1.py` MISSED (355/370, answered 356, tool_pin FAIL); R94MCritic's oracle-exec wrapper MISSED
(`static_no_external_resolver=FAIL import:subprocess`, 368/370); a ctypes libgio forgery
(`controls/forgery-ctypes-gio-r94.py`) MISSED only by (vi) and the pin (`lib:libgio-2.0.so.0`, 370/370 otherwise) —
(vi) is load-bearing.

## C2 — operability: the selftest-strength gate guards two more lane tools

Routed defect 2 of the round-93 spot-check: `quality/check-selftest-strength.py` was wired only for
`quality/check-seat-reports.py`. This claim lands kill-sets `quality/selftest-kills/mado-xdgmime.json` (= frozen
`build/mado-xdgmime-kills.c2b.json`, 19 kills, sha256 `d8a450bfb3bd67a6f5be399dece1ddc3d1b0922ae9c4b1f8bcff9a37afddd4ad`)
and `quality/selftest-kills/mado-mime.json` (= `build/mado-mime-kills.c2b.json`, 27 kills,
`1a0c4fe8cec8ac4d0b33aaaf3c803e37ef168cc86f1f5cf914d35182051100b6`) for `tools/mado-xdgmime.py` (12 checks) and
`tools/mado-mime.py` (17). The gate stays the round-93 frozen gate (`2d6f1219…a61b`); the tools are unchanged.

Frozen inputs: panel `.ufo/waves/round-94/controls/selftest-panel-r94-frozen.json` (91 hand weakenings: R94MExecCounterC2
12 + R94MMutC2 79 green; 6 neutral edits) `2d35e83bd9bcdd821accda43b39b5302cb508e15602019a34c89d7e418eed7e0`; control
kill-sets (the wave's first drafts) `build/mado-xdgmime-kills.c2.json` `126b508a…9ea9`, `build/mado-mime-kills.c2.json`
`d930689e…1601`; counter `quality/counters/c2-r94-selftest-kills.py`
`0eb3aadad4b72eeacb6a5d382071efd78105fa0e8ccdd751445f5c3ccb1d9a02`.

Counter argv: `python3 -I quality/counters/c2-r94-selftest-kills.py --repo . --rev <rev> --panel <panel>
--expect-panel-sha256 2d35e83b… --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b
--expect-kills-sha256 d8a450bf…,1a0c4fe8… --control-kills <c2 xdgmime>,<c2 mime> --expect-control-kills-sha256
126b508a…,d930689e… --workers 16 --scratch-root DIR`.

**PRED-C2-r94-v1**: TARGET_MET iff, at `<rev>`, the gate is the round-93 frozen gate, both kill-sets are the frozen
candidates, and (i) the gate on each unmodified tool with its kill-set prints OK rc 0 and each kill-set's `tool_sha256`
equals the tool at `<rev>`; (ii) for each of the 29 selftest checks (12 + 17, labels from the `checks` tuples / `chk`
calls, count = `checks=N`), the tool with that one check forced to pass makes the gate print WEAK rc 1; (iii) each of the
91 frozen hand weakenings (selftest still green) → WEAK rc 1; (iv) each of the 6 neutral edits → OK rc 0; (v) controls:
the do-nothing instrument (flag iff the selftest result line changes) flags fewer than (ii)+(iii), always-OK flags none,
always-WEAK fails (i), sha-diff fails (iv); (vi) the gate's `--selftest` exits 0; (vii) the first-draft kill-sets flag
strictly fewer of the 91 hand weakenings than the frozen ones. `singleton_labels` is printed, not a conjunct.

Before → after: single-check neutralisations of the two tools' selftests flagged by a lane instrument — before, the
do-nothing instrument (no kill-set exists; the counter itself stops SETUP_ERROR) **0/29**; after, the gate with the
frozen kill-sets **29/29**, with hand weakenings 91/91 (first-draft kill-sets 45/91).

Pre-freeze controls (`.ufo/waves/round-94/receipts/c2-controls-prefreeze-r94.txt`): candidates `DRAFT_TARGET_MET`
29/29, 91/91, 6/6, do-nothing 0, always-OK 0, sha-diff 0/6, control 45/91, singleton 22/29; first-draft kill-sets as
candidates MISSED (91 → 45/91, pins FAIL); empty kill-sets MISSED (0/29, 0/91).

## Separability

C1 lands a new tool, entry and rows; C2 lands two kill-set JSON files. C1 is measured at its own commit (before C2); C2's
counter at the C1 commit must stop SETUP_ERROR (kill-sets absent). C2 does not guard the C1 tool on purpose (R94MCritic
C2-F2): a kill-set for `tools/mado-mimeglob.py` would make C2 depend on C1 having landed; the C1 tool is guarded by its
own 60 mutants. Neither counter reads the other claim's files.

## Named limits (declared before data)

- C1: filename only (no sniffing); C locale fnmatch; labels from glib2 2.90.1-1 / shared-mime-info 2.5.1-2 as installed;
  undefined C behaviour (bare `*`, suffix-node loops) answered as observed or refused; host leg is cache mode only on
  this host.
- C2: kill-sets and 79 of the 91 panel weakenings come from the same wave (R94MMutC2 wrote both the escapes and their
  closing kills): the panel is a design set, the first-draft control shows it discriminates, generalisation to unseen
  weakening families is not measured; the gate's own selftest and the C1 tool's selftest are not kill-set guarded.

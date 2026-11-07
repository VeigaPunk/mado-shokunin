# mado round 93 — claims declaration (FROZEN at the freeze commit that carries this file)

L1 `MadoR93`, hyaku run 15, attempt 1. Base revision `4c6f723f3dca3a26f9d14475d695fe797e2e972c` (round-92 closure tip,
`master`). Lowest-axis duty: every owned axis stands at 10 (SCORECARD rounds 88–92), so the duty is a tie; the
stagnation nudge is not claimed (a capability entered at round 92). Sourced claim: C1 (rows S511–S514 opened this
round — S511/S512/S514 by the L1, S513 by R93MScoutSources and re-opened by the L1 — `.ufo/waves/round-93/receipts/sources-open-r93.txt`).
Both claims answer routed defects of the round-92 non-author spot-check (`corpus/lessons/round-92-verifier-spotcheck.md`
lines 170–173: defects 2 and 3).

The w1 wave (13 seats) attacked the drafts before this freeze; every change it caused is listed in
`corpus/lessons/round-93.md` "Wave findings routed". The draft the wave first attacked (candidate `89039e30…`, the
20-kill gate, the fresh-seeded C2 clause) is not the frozen bytes.

## C1 — coverage (edge class): GKeyFile byte classes in xdg-desktop-portal's config and `.portal` files

**Surface moved.** `tools/mado-portals.py` (round 90) answers which `.portal` backend xdg-desktop-portal 1.22.1 picks
per impl interface. Its key-file reader diverged from GLib 2.90.1 `gkeyfile.c` on byte classes no round-90 case holds:
(a) invalid UTF-8 anywhere — a comment, another group, an unread key, a key or group *name* — voided the whole file
(strict `open(…, encoding="utf-8")`), while GKeyFile validates UTF-8 only when a value is read (S514
`gkeyfile.c:2310`, `:2427`; names take raw bytes); continuation bytes right after a group's `]` are skipped by
`g_utf8_find_next_char`; (b) VT (0x0B) was stripped as whitespace, while `g_ascii_isspace` excludes it (S511
`gstrfuncs.c:264`, S512 `gstrfuncs.h:86`); (n) NUL: GKeyFile reads a line as a C string for comment/group/key
detection, cuts a stored value or group name at the NUL, but scans the group's last `]` and counts the Encoding value
over the whole line (S514; R93MReviewC1 F1/F2). Classes (c) repeated keys and (d) `x[]`/`x[C]` locale keys and the
whitespace class `ws` are regression cases (no routing-visible change), not counted.

**Frozen candidate** `.ufo/waves/round-93/build/mado-portals.c1.py` sha256
`e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021` (round-92 port + the L1's NUL/continuation patch +
six byte-class selftest checks, 28 checks); lands byte-identical as `tools/mado-portals.py`.

**Predicate `PRED-C1-r93-v1`** (counter `quality/counters/c1-r93-portal-bytes.py`, the docstring states this sentence;
receipt line `MADO_PORTAL_BYTES:`): TARGET_MET iff `<rev>:tools/mado-portals.py` is the frozen candidate (sha256 ==
`--expect-tool-sha256`) and, run through its public CLI in the round-90 sandbox with fixtures written as bytes, answers
every frozen case (the 229 round-90 cases + the frozen byte-class cases) exactly as the installed xdg-desktop-portal
1.22.1 labels it (correct == cases); answers every fresh case of the round-90 generator (120) and of the frozen
byte-class generator (60), both seeded by the first 8 hex digits of the tool's sha256 and labelled by the oracle at
measurement time; every frozen mutant gives a well-formed wrong answer on at least one frozen case (killed == mutants;
a crash is not a kill, QUALITY 148); each control — do-nothing, the round-90 r12-rule and host-table controls, and the
base revision's `tools/mado-portals.py` — scores fewer than the case count; the base tool scores fewer than the byte
subset (classes a, b, n: invalid UTF-8 and raw name bytes, VT, NUL) holds (base_bytes_correct < bytes_cases); and the
oracle binary and host tail digests equal the label file's pins.

**Count.** Frozen byte-subset cases (classes a, b, n) a lane tool answers as xdg-desktop-portal does: base
`tools/mado-portals.py` at `4c6f723f` 32/80 (DRAFT, `receipts/c1-controls-prefreeze-r93.txt`) → 80/80, gated by the
predicate.

**Kill rule.** Any conjunct false at the measured C1 commit → `TARGET_MISSED`, reported as such; no case, mutant,
control, pin or clause changes after the freeze.

**QUALITY 153 and the round-90 counter.** The port removes the bytes nine round-90 frozen mutants anchor on (M03 M27
M29 M31 M37 X01 X04 X05 X06; R93MMutC1 §3a), so `quality/counters/c1-r90-portal-routing.py` cannot run as a leg on the
candidate (setup error by design) and cannot materialise the byte fixtures at all (R93MCritic C1-F5). Following the
round-92 spot-check's routing ("its own frozen counter with regenerated round-90 mutants"), the round-93 counter
carries the 229 round-90 cases and 59 of the 60 round-90 mutants — 50 unchanged, 9 re-anchored rule for rule to the
ported bytes; X19 is excluded as crash-shaped on the ported bytes (R93MMutC1 §5.1, `not_counted_survivors`); the five
round-90 equivalents stay equivalents — inside its own frozen set (75 mutants with 16 byte-class ones). The round-90
receipt stays pinned to its own revision (`7bec2399`).

## C2 — operability: a gate that fails when a passing selftest assertion of the seat-report gate is weakened

**Surface moved.** Round-92 spot-check routed defect 3 / R92MMutC2 §4: the lane's instruments read only
`quality/check-seat-reports.py --selftest`'s result line, so an assertion weakened to pass (the line still
`checks=23 failed=0`) is invisible. After: `quality/check-selftest-strength.py` runs the tool's `--selftest` against a
committed kill-set of production mutants, `quality/selftest-kills/check-seat-reports.json` (32 kills; each names the
exact set of selftest checks that fail on it; `selftest_checks: 23`), and prints `WEAK` (rc 1) when a kill mutant
passes the selftest, crashes, or fails a different set of checks.

**Frozen candidates** gate `.ufo/waves/round-93/build/check-selftest-strength.c2.py` sha256
`2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` → `quality/check-selftest-strength.py`; kill-set
`.ufo/waves/round-93/build/check-seat-reports-kills.c2.json` sha256
`00befb3efbe2f4a7c44b14776482e0cac0ab8e219db934af9c25b34f47c516f9` → `quality/selftest-kills/check-seat-reports.json`.

**Predicate `PRED-C2-r93-v1`** (counter `quality/counters/c2-r93-selftest-strength.py`, docstring; receipt line
`MADO_SELFTEST_STRENGTH:`): TARGET_MET iff, at `<rev>`, the gate and the kill-set are the frozen candidates (sha256 ==
`--expect-gate-sha256`, `--expect-kills-sha256`) and: (i) the gate on the unmodified `quality/check-seat-reports.py` and
the committed kill-set prints OK and exits 0, and the kill-set's `tool_sha256` equals the tool's sha256 at `<rev>`;
(ii) for every one of the tool's selftest checks (the labels of every `case(...)` call in its selftest at `<rev>`, as
many as its result line's `checks=N`), the tool with that one check's result forced to pass makes the gate print WEAK
and exit 1 (neutralised_flagged == checks); (iii) every frozen hand weakening of the panel (an edit that keeps the
selftest green, `checks=N failed=0`) makes the gate print WEAK and exit 1 (hand_flagged == hand); (iv) every frozen
neutral edit of the panel (a strength-preserving byte change that keeps the selftest green) leaves the gate at OK, exit
0 (neutral_ok == neutrals); (v) every frozen gate mutant prints a well-formed verdict line different in verdict or exit
code from the measured gate's on at least one probe of (i)–(iv) or of the frozen setup panel (killed == mutants; a
mutant whose only differences are missing verdict lines is crashed_not_killed); (vi) each control fails (i)–(iv): the
do-nothing instrument (the round-92 C2 counter's selftest leg: flag a variant iff the tool's selftest result line
changes) flags fewer than the weakenings, an always-OK gate flags none, an always-WEAK gate fails (i), and a gate that
flags every byte change of the tool (sha-diff) fails (iv); (vii) the gate's `--selftest` exits 0.

The draft's fresh-seeded clause (iv) "20 (check, transform) weakenings from a seed" is replaced before any measurement
(R93MCritic C2-F1, R93MReviewC2 §6): clause (ii) enumerates every check exhaustively, so a seeded sample of
neutralisations adds no unknown-at-write-time case; what a label-keyed gate *can* forge — flag any byte change — is
defeated by the neutral edits (sha-diff control, clause vi), which the fresh clause never tested.

**Count.** Single-check neutralisations of the seat-report gate's selftest flagged by a lane instrument: 0/23 at
`4c6f723f` (the result line is unchanged; `do_nothing_flagged` in `receipts/c2-controls-prefreeze-r93.txt`) → 23/23.

**Kill rule.** As C1.

## Do-nothing and forgery controls — executed before this freeze and committed in it

- C1 (`receipts/c1-controls-prefreeze-r93.txt`): the frozen candidate with the frozen mutants; the base tool (strict
  UTF-8 reader); a label-table forgery keyed by the fixture bytes (`build/forgery-table-r93.py`, generator
  `controls/gen-c1-forgery-table-r93.py`) — every frozen case right by construction, so only the fresh legs reject it.
  Inside the predicate: do-nothing, r12-rule, host-table, base.
- C2 (`receipts/c2-controls-prefreeze-r93.txt`): one DRAFT run of the C2 counter on the frozen gate and kill-set; it
  scores inside it the do-nothing instrument, always-OK, always-WEAK and sha-diff gates.

## Separability

C1 touches `tools/mado-portals.py`, a knowledge entry and registry rows; C2 touches `quality/check-selftest-strength.py`
and `quality/selftest-kills/check-seat-reports.json`. Each counter reads only its own files at the measured revision
(R93MCritic C1-F7); each is run at the other's commit.

## Frozen pins and argv (REV = the measured commit; run from the lane root; DIR = a scratch directory)

- C1: cases `.ufo/waves/round-93/controls/portal-cases-r93.json` (366 = 229 + 137 classed; byte subset a 38, b 16, n 26)
  `351072d1f5c38f767b2a3dbab6faad3383a4f811ec757a4f245ed1a53ed7d0c1`; mutants
  `.ufo/waves/round-93/controls/portal-mutants-r93-frozen.json` (75) `7e45edc9b12b5a02ea5aab1eeb9f95ad8cf836114a056448e1a2e548fcce6d26`;
  oracle `.ufo/waves/round-93/controls/portal-oracle-r93.py` `d50d88bfc6a9964ac2f04a30315473daccf4308991aa3131cfe5e801f8b576f6`;
  byte generator `.ufo/waves/round-93/controls/fuzz-bytes-r93.py` `94fdfe8f31c21ce42a8e197c585d9d7f9a09b32684c8a265dd4ef7bb1e5d1597`;
  round-90 generator pinned inside the counter (`f5cbb11f…cdd6`); counter sha256 in the freeze commit.

      python3 -I quality/counters/c1-r93-portal-bytes.py --repo . --rev REV --base-rev 4c6f723f3dca3a26f9d14475d695fe797e2e972c \
        --cases .ufo/waves/round-93/controls/portal-cases-r93.json --expect-cases-sha256 351072d1f5c38f767b2a3dbab6faad3383a4f811ec757a4f245ed1a53ed7d0c1 \
        --mutants .ufo/waves/round-93/controls/portal-mutants-r93-frozen.json --expect-mutants-sha256 7e45edc9b12b5a02ea5aab1eeb9f95ad8cf836114a056448e1a2e548fcce6d26 \
        --oracle .ufo/waves/round-93/controls/portal-oracle-r93.py --expect-oracle-sha256 d50d88bfc6a9964ac2f04a30315473daccf4308991aa3131cfe5e801f8b576f6 \
        --fuzz-bytes-gen .ufo/waves/round-93/controls/fuzz-bytes-r93.py --expect-fuzz-bytes-sha256 94fdfe8f31c21ce42a8e197c585d9d7f9a09b32684c8a265dd4ef7bb1e5d1597 \
        --expect-oracle-binary-sha256 e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8 \
        --expect-tool-sha256 e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021 \
        --fresh 120 --fresh-bytes 60 --scratch-root DIR

- C2: panel `.ufo/waves/round-93/controls/selftest-panel-r93.json` (16 weakenings, 6 neutrals)
  `a6d2cbe2826868191f3ee980c27fcc3288bbc151ed3ceeb79ca1f11891bc4c10`; gate mutants
  `.ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json` (22) `be676929cefa46481e1ea836d29cd65152af23002e9d9dad96cf39295b88770e`;
  round-92 C2 counter `0aa4d1f18c3f309a8ef5a7575f1a4bde84681d9f7843dea03fdca723de30945c`; counter sha256 in the freeze commit.

      python3 -I quality/counters/c2-r93-selftest-strength.py --repo . --rev REV \
        --panel .ufo/waves/round-93/controls/selftest-panel-r93.json --expect-panel-sha256 a6d2cbe2826868191f3ee980c27fcc3288bbc151ed3ceeb79ca1f11891bc4c10 \
        --mutants .ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json --expect-mutants-sha256 be676929cefa46481e1ea836d29cd65152af23002e9d9dad96cf39295b88770e \
        --expect-r92-counter-sha256 0aa4d1f18c3f309a8ef5a7575f1a4bde84681d9f7843dea03fdca723de30945c \
        --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b \
        --expect-kills-sha256 00befb3efbe2f4a7c44b14776482e0cac0ab8e219db934af9c25b34f47c516f9 \
        --workers 16 --scratch-root DIR

# mado round 94 — claims declaration (DRAFT until the freeze commit; the L1 MadoR94 owns it)

Base: `master` at `a3de997289014e7dbf1d73ae206be1d6f8cdadd0` (round-93 closure tip). Lowest-axis duty: every owned axis
scores 10 (round-93 SCORECARD), so the duty is a tie; stagnation nudge not claimed (a capability entered at round 93).
Sourced claim: C1 (rows S515–S518, opened by the L1 this round: `.ufo/waves/round-94/receipts/sources-open-r94.txt`).
Routed defects of the round-93 spot-check: defect 2 → C2; defects 1 and 3 are not claims this round (reasons in the
lesson). considerthese `2026-11-06.md` proposal 4 ("widen desktop coverage … prefer one operator-config gap") → C1.

## C1 — coverage (new surface, capability): file name → MIME type as GLib guesses it

Surface moved: the name-to-type step that precedes every default-application answer (rounds 91–92 resolve
type → application; nothing in the lane answers name → type). A hand-written `~/.local/share/mime/packages/*.xml`
(the host has one), a stale `mime.cache`, a `globs2` without a cache, or a case/extension the operator assumes
"works" decide which application `gio open`/file managers pick.

New read-only tool `tools/mado-mimeglob.py` (candidate `.ufo/waves/round-94/build/mado-mimeglob.c1.py`): what
GLib 2.90.1 `g_content_type_guess (name, NULL, 0, &uncertain)` answers — type and uncertain flag — from the
shared-mime-info databases: xdgmime's directory list, cache mode (any valid `mime.cache` → caches only) vs text mode
(`globs2`, else `globs`), literal / simple-suffix / fnmatch globs, ASCII case folding and the `cs` flag, deepest-suffix
selection (per cache in cache mode), weights (low 8 bits in a cache), duplicate merge and weight sort, the trailing-`/`
and no-match/several-match rules. Where GLib departs from the spec (S517: "longest pattern SHOULD be used",
`__NOGLOBS__` deletion) the tool follows GLib and the entry says so.

Oracle: `.ufo/waves/round-94/controls/mimeglob-oracle-r94.c`, compiled against the installed glib2 2.90.1-1
(`pkg-config gio-2.0`), run with `LC_ALL=C` and the case's `HOME`/`XDG_DATA_HOME`/`XDG_DATA_DIRS`; prints
`<type>\t<uncertain>` per name.

Counter (planned): `quality/counters/c1-r94-mimeglob.py --repo . --rev <rev> --base-rev a3de9972… --cases <frozen>
--expect-cases-sha256 … --mutants <frozen> --expect-mutants-sha256 … --oracle-src <oracle.c> --expect-oracle-sha256 …
--fresh-gen <frozen> --expect-fresh-gen-sha256 … --host-names <frozen> --expect-host-names-sha256 …
--expect-tool-sha256 <candidate> --fresh N --scratch-root DIR`.

PRED-C1-r94-v1 (draft; frozen at the freeze commit): TARGET_MET iff, at `<rev>`, `tools/mado-mimeglob.py` is the frozen
candidate (sha256 pin) and (i) on every frozen case the tool's (type, uncertain) equals the oracle's, and the oracle
re-run at measurement equals the label recorded in the case file (else SETUP_ERROR); the frozen set holds both modes
(text and cache) and every class named in the case file; (ii) on N fresh seeded cases from the frozen generator
(seed printed) the tool equals the live oracle on every name; (iii) on the frozen host name list under the host's own
environment the tool equals the live oracle on every name; (iv) every frozen mutant of the candidate makes at least one
frozen case wrong (a mutant that only crashes is `crashed_not_killed`, not killed); (v) each control misses (i): the
do-nothing answer (`application/octet-stream`, uncertain 1), the naive extension map (last `.ext` → highest-weight type
in the dirs' globs2, uncertain 0), and the base revision (no tool → 0 answered).
Before → after: frozen cases answered as GLib does, base `0/N` (no tool) → `N/N`. Kill rule: any conjunct false →
TARGET_MISSED, never narrowed after data.

## C2 — operability: the selftest-strength gate guards two more lane tools

Routed defect 2 of the round-93 spot-check: `quality/check-selftest-strength.py` is wired only for
`quality/check-seat-reports.py`. This claim commits kill-sets for `tools/mado-xdgmime.py` (12 selftest checks) and
`tools/mado-mime.py` (17), so a weakened, still-passing selftest assertion of either tool prints WEAK. The gate's bytes
stay the round-93 frozen gate (sha256 `2d6f1219…a61b`); the tools are unchanged.

Counter (planned): `quality/counters/c2-r94-selftest-kills.py --repo . --rev <rev> --panel <frozen>
--expect-panel-sha256 … --expect-gate-sha256 2d6f1219… --expect-kills-sha256 <xdgmime>,<mime> --workers N
--scratch-root DIR`.

PRED-C2-r94-v1 (draft): TARGET_MET iff, at `<rev>`, the gate is the round-93 frozen gate, both kill-sets are the frozen
candidates, and (i) the gate on each unmodified tool with its kill-set prints OK and exits 0, and each kill-set's
`tool_sha256` equals the tool at `<rev>`; (ii) for every selftest check of each tool (the labels of its `checks`
tuples, as many as its result line's `checks=N`: 12 + 17 = 29), the tool with that one check forced to pass makes the
gate print WEAK and exit 1 (neutralised_flagged == 29); (iii) every frozen hand weakening (selftest still green) → WEAK
rc 1; (iv) every frozen neutral edit (selftest still green, strength preserved) → OK rc 0; (v) controls: the
do-nothing instrument (flag iff the selftest result line changes) flags fewer than (ii)+(iii), an always-OK gate flags
none, an always-WEAK gate fails (i), a sha-diff gate fails (iv); (vi) the gate's `--selftest` exits 0.
Before → after: single-check neutralisations of the two tools' selftests flagged by a lane instrument `0/29` (no
kill-set: the gate cannot be pointed at either tool) → `29/29`.

## Separability

C1 lands a new tool, entry and rows; C2 lands two kill-set JSON files. C1 is measured at its own commit (before C2);
C2's counter at the C1 commit must stop SETUP_ERROR (kill-sets absent). Neither claim reads the other's files.

## Controls before the freeze (committed in the freeze)

C1: candidate DRAFT run; do-nothing; naive extension map; base. C2: candidate DRAFT run; do-nothing; always-OK;
always-WEAK; sha-diff. Each must fail its predicate before the freeze, or the counter/target is wrong and is fixed
before data.

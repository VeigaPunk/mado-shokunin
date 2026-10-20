# ReviewCensus — U6 coverage denominator and preserved U4/U5 facets

Scope: adversarial review of the C1 coverage join for the U6 claim (sourced U1–U5 5/7 → U1–U6 6/7).
Read-only: git log/status, `grep`, `ls`, static reads of lane artifacts. No gate, measure.py, test, build, lint, or live probe was run. No tools installed or updated. No external URL was opened; statements about S007's page content are `[INFERENCE]`.

## Verdict

**Reject the generic counter path. Conditionally accept U6 only if F1–F5 acceptance conditions hold.**
Expected score if every condition holds: 6/7 = **8.5714** (delta +1.4286 over 5/7 = 7.1429). It is not 10; U7 stays in the denominator as an unscored gap.
If any condition fails, the claim is not admitted and the score stays at 7.1429.

## Findings (by severity)

**F1 — high: U6 has no body-facet gate.** The round-14 counter gates U4 (`measure.py` 169–179) and U5 (180–192) on body facets. The generic path (193–200) counts any `covers: U6` note whose head-15 `source:` cites a `mined` A/B row with `used-by` naming the note, plus `verified-at` and `recheck`. A U6 note with no `## Layer ladder` / `## Safe boundary` / `## Unexercised delivery` section still scores. Round-14 lesson (`corpus/lessons/round-14.md:155–160`) states that structural joins are not semantic truth; the spec asks for those headings, so the counter must check them.
- Accept: round-15 `measure.py` has a U6 branch requiring the three `##` headings, `## Unexercised delivery` as the last level-2 heading, containing `[UNK]`.
- Reject: U6 counted via the generic branch, or facets checked only by prose.

**F2 — high: U6 reciprocity is not implemented.** The `inverse` check (`measure.py` 187–188) runs only inside the U5 branch. The spec requires "both mined reciprocal" for U6.
- Accept: U6 branch requires every registry row with `mined` status and `used_by(U6 path)` to be cited on the U6 head-15 `source:` line.
- Reject: copying only the reserved-row check.

**F3 — high: numerator trap in the SCORECARD literal rubric.** `SCORECARD.md:237` (C3 rubric) and its counting command count *entries with any S-id in head-15 `source:`* (currently **6**: `config-drift-r12.md` has no `covers:` line and is still counted) and separately *`covers:` lines* (currently 5). Neither is the unique covered-U count. `measure.py`'s `len(covered)` is the only item count (round-14 recorded set `{U1..U5}`, `.ufo/waves/round-14/evidence/after.txt:39–45`). Note that a naive entry count of 6 after U6 would produce 6/7 = 8.5714 by coincidence while the true item count is different.
- Accept: C1 numerator is `len(covered)` from the revision-bound counter; the SCORECARD literal command is annotated as non-authoritative or replaced.
- Reject: any numerator taken from entries, covers-lines, or prose.

**F4 — high: count-only reporting can hide a net-neutral trade.** Adding U6 while silently dropping U4 or U5 leaves the count at 5/7 and looks like "no change". The score cannot distinguish these cases.
- Accept: report the covered set before and after; the diff must be exactly `+U6` with no removals. `U4` facets (`| Which upstream development/compatibility phase`, `| Which interface/version`, `| Does the intended feature actually work?`, with S005/S041/S043 mined) and U5 facets (`## Output management`, `## Colour management`, `## Unexercised feature behavior` with `[UNK]`, S047/S048 mined, inverse true) must remain true.
- Reject: a count-only report.

**F5 — medium: S051 would collide with existing S007.** `corpus/SOURCES.md` row S007 is the same canonical URL (`https://wayland.freedesktop.org/libinput/doc/latest/tools.html`), status `queued`, `used-by` `—`, anchored by access date only. `doc/latest` is mutable; `SOURCES.md` "Search-log errata" (round 12) lists this as an owed-anchor defect. Only `status`, `recheck`, and `used-by` may change in place, so S007 cannot be promoted without a revision anchor. A new S051 with the same URL is a duplicate-admission trigger; the census accepts it only with an explicit `supersedes S007 —` opener.
- Accept: S051 `teaches` opens `supersedes S007 —` and records an immutable revision (commit or tag SHA) for the libinput tools documentation source; S007 stays `queued`.
- Reject: S051 without the supersedes marker, citing `doc/latest`, or changing S007's anchor/teaches cells.

**F6 — medium: S052 must not reuse S043's file.** S043 already cites `/usr/share/wayland/wayland.xml` (wayland 1.26.0, registry scope only, `SOURCES.md` row S043). Citing that file for `wl_keyboard`/`wl_pointer` exceeds S043's anchor scope and would duplicate its path. Reusing S043 requires only a `used-by` append, which does not supply wl_keyboard/wl_pointer semantics.
- Accept: S052 is a new row with a distinct, immutable revision of the core protocol XML and a scope naming wl_keyboard/wl_pointer, with `supersedes`-free distinct URL or justified collision review.
- Reject: S052 citing the local installed path already used by S043, or `used-by` extension of S043 as the sole support for input-semantics claims.

**F7 — medium: fail-closed registry parse is silent.** `measure.py` 96–99 admits only rows with exactly 13 `|`-split cells; `mined_ab` and the generic join silently drop any malformed row, so U6 becomes uncounted with no error. A `|` in any cell shifts columns.
- Accept: each cited S-id prints its resolved row (status, tier, used-by) in the counter output; new rows parse to 13 cells; the maintained census exits 0.
- Reject: silent omission of a cited row.

**F8 — medium: commit binding.** The counter reads `git show <rev>:<path>` only. Uncommitted notes, README rows, or registry rows are invisible. Current tree: `git status` shows `M SCORECARD.md` and staged round-15 spec/dispatch files; no U6 note exists.
- Accept: the U6 note, README row, and SOURCES rows are in one committed revision; the counter output names that SHA, and the probe runs at that SHA.
- Reject: counting working-tree files, or mixing revisions across note, registry, and index.

**F9 — preservation controls (pass conditions).**
- `corpus/knowledge/wayland-protocol-boundaries-r13.md` and `output-colour-boundaries-r14.md` unchanged in the U6 commit: `git diff <round-14-head>..<rev> -- corpus/knowledge/wayland-protocol-boundaries-r13.md corpus/knowledge/output-colour-boundaries-r14.md` is empty.
- Existing `used-by` cells for S005, S041, S043, S047, S048, S050 keep their U4/U5 paths; any change is append-only and logged old→new in the round lesson.
- Navigation: exactly one README row per note; the new note row is added only when the file exists (no predeclared missing row). Current baseline: 28 notes, 28 rows (verified).

**F10 — residual, pre-existing (not in scope to fix).** The U4 branch has no `inverse` check; this is unchanged.

## Acceptance (all required)
1. U6 branch in the round-15 counter: three headings, `[UNK]` in last section, S051/S052 mined A/B with `used-by` and reciprocal inverse (F1, F2).
2. Covered-set diff before/after is exactly `{U1..U5} → {U1..U6}` (F4).
3. Numerator is `len(covered)`; SCORECARD literal rubric not used as the number (F3).
4. S051 supersedes S007 with immutable revision; S007 unchanged except as allowed (F5). S052 distinct scope/revision (F6).
5. Registry rows printed and parse to 13 cells; census exit 0 (F7).
6. Single committed SHA containing all artifacts; probe run at that SHA (F8).
7. U4/U5 notes and their used-by cells preserved (F9).
8. Score reported as 8.5714 only when items = 6; otherwise 7.1429. No 10.

## Rejection (any one)
- U6 counted without body headings or reciprocity.
- Numerator from entries, covers-lines, or prose.
- Count-only report without covered-set diff.
- S051 without `supersedes S007 —` or with mutable `doc/latest` anchor.
- Any U4/U5 facet or used-by regression, however the count nets out.
- Working-tree or cross-revision measurement.

## Evidence pointers (absolute)
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/measure.py` — 96–99 registry parse; 112–144 `body_facets`; 147–200 generic join, U4/U5 branches, `covered`; 187–188 inverse; 202–212 navigation.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/evidence/after.txt` — 39–45 covered set `{U1..U5}`; 122–139 `u4_facets`; 143–148 navigation.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md` — :237 literal C3 rubric/command; :289 C3 row; :464–466 round-15 targets; :513 round-14 measured row.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` — row S007 (`doc/latest`, queued, used-by `—`); rows S041, S043, S047, S048, S050 (used-by); "Search-log errata" owed-anchor rule.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/output-colour-boundaries-r14.md` — head-15 source/covers; `## Output management`, `## Colour management`, unexercised-feature section.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md` — U4 facet rows (`| Which upstream`, `| Which interface/version`, `| Does the intended feature`).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-14.md` — 155–160 structural-vs-semantic statement.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md` — 28 knowledge rows, 28 notes (observed by grep).
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/w1/spec.json` — MeasureBuild item (U6 headings, S051/S052 reserved, reciprocal requirement).

## Verification gaps
- Counter not executed (out of scope); all facet/inverse behavior is from source reading and recorded round-14 evidence.
- External S007 page and libinput/wayland revisions not opened; immutable SHAs are unknown and must come from the source owner.
- U6 semantic accuracy (delivery, focus, IME) is out of this review's scope and belongs to the other U6 reviewers.

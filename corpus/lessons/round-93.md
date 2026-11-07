# mado round 93 — lessons

Round 93, hyaku run 15, attempt 1 (`MadoR93`). Two frozen claims from `.ufo/waves/round-93/claims-declaration-r93.md`
(freeze `{FREEZE}`): C1 coverage, edge class (`tools/mado-portals.py` reads `portals.conf`/`.portal` bytes as GLib 2.90.1
GKeyFile does — invalid UTF-8, VT, NUL, raw name bytes — round-92 spot-check routed defect 2) and C2 operability
(`quality/check-selftest-strength.py`: a gate that fails when a passing selftest assertion of the seat-report gate is
weakened — routed defect 3).

## Mistakes

**M93-1 — the L1 patched the candidate while a seat was sweeping mutants against it.**
Class: moving-target instrument — a frozen set built against bytes that change under it.
Evidence: R93MMutC1 §1 and §5.5: one sweep's pristine copy hashed `89039e30`, its restored copy `849df12c` (the L1's NUL
patch landed at 00:23 mid-run), then `e46a861e` (00:26, six selftest checks); the seat discarded that run and re-anchored.
The C1 counter as first written measured `<rev>:tools/mado-portals.py` with no tie to the candidate the mutants were
anchored to (R93MCritic C1-F2), so a landed file that is not the frozen candidate would have SETUP_ERRORed or, re-anchored,
certified bytes the claim never described.
Captured-by: none — the seat noticed because it hashed pristine and restored copies; the critic named the counter gap.
Fix: both counters now carry the frozen candidates' sha256 as a conjunct (`--expect-tool-sha256`, `tool_pin`;
`--expect-gate-sha256`/`--expect-kills-sha256`, `frozen_pin`). Shown able to fail:
`.ufo/waves/round-93/receipts/c1-controls-prefreeze-r93.txt` — the base tool and the table forgery print `tool_pin=FAIL`.
Criterion: `QUALITY.md` 155.

**M93-2 — the C2 seat brief asked for one *unique* killer per selftest check; three checks have none.**
Class: over-constrained instrument spec — a property (uniqueness) the predicate does not need, which made the kill-set
cover 20 of 23 checks and miss 6 of 10 hand weakenings and 9 of 20 fresh ones.
Evidence: R93MExecGateC2 "3 checks have NO achievable unique killer"; R93MReviewC2 §2–§3 (20/23, 4/10, 11/20 with the 20
kills); the brief in `.ufo/waves/round-93/w1-spec.json` (R93MExecGateC2 item: "find a production-code mutant … that ONLY
that check fails").
Captured-by: the w1 attack seats (R93MReviewC2, R93MMutC2 §6 escapes), before the freeze.
Fix: a kill names the exact set of checks that fail on it (`must_fail` as a list; the gate holds it only on set equality),
and 12 kills were added from the reviewer's and mutation tester's repairs; the 32-kill set flags 23/23 neutralisations
and 16/16 weakenings and keeps 6/6 neutral edits OK (`receipts/c2-controls-prefreeze-r93.txt`). Shown able to fail: the
20-kill set's 20/23 (R93MReviewC2 §2.2). Criterion: `QUALITY.md` 156.

**M93-3 — a counter that compared the gate's verdict word but not its exit code.**
Class: predicate-fidelity — the predicate says "WEAK rc 1"; the instrument read "WEAK".
Evidence: R93MReviewC2 §4: `G19-rc-always-zero` (WEAK printed, exit 0) could never be killed by the seat counter
(`a28a7c71…`, `verdict()` ignores `rc`).
Captured-by: R93MReviewC2, before the freeze.
Fix: the L1's counter compares `VERDICT:rc`. Shown able to fail: in the pre-freeze run G19 is killed at probe s04 by
`WEAK:1->WEAK:0` (`receipts/c2-controls-prefreeze-r93.txt`), a difference the word-only rule cannot see.

**M93-4 — the round-92 report carried no cross-domain evidence item (spot-check routed defect 1).**
Class: report minimum content (PROTOCOL "cross-domain evidence encountered, with the domain it belongs to").
Evidence: `corpus/lessons/round-92-verifier-spotcheck.md` lines 27–30 and 168–169; `grep -c '^- \*\*Cross-domain evidence'
/home/vgpnk/Projects/shokunin/.ufo/reports/round-92/mado.md` → 0.
Captured-by: PROTOCOL minimum content, read by the closure; no lane instrument.
Fix: the round-93 report carries the item (R93MConnector §4 sweep); `QUALITY.md` 157 makes it a pre-filing check. Shown
able to fail: the same grep on the round-92 report prints 0; on the round-93 report 1.

**M93-5 — a seat was sent to a source path that no longer exists at the pinned tag.**
Class: stale locator in a dispatch — the L1 named `src/portal-impl.c` at xdg-desktop-portal 1.22.1 from memory.
Evidence: R93MScoutSources §3: HTTP 404; the file was renamed twice (`a6feb89b`, `4bb70f20`) and the reader is
`src/xdp-portal-config.c`, the file row S501 already pins.
Captured-by: the scout seat (it fetched before it quoted).
Fix: S513 opened by the L1 at the existing pinned path (`receipts/sources-open-r93.txt`); `QUALITY.md` 158: a source URL in
a seat item is taken from a registry row or fetched by the L1 before dispatch. Not shown able to fail as an instrument (no
check reads dispatch URLs); routed.

**M93-6 — the first C1 counter's byte subset was not the declared one.**
Class: counting-rule drift — the class of a case derived from its id pattern counted seven round-90 cases (`a0N-settings-…`)
as class a and folded explicit `ws` into b.
Evidence: R93MCritic C1-F1 (`bytes_cases=98` against a declared 52).
Captured-by: R93MCritic, before the freeze.
Fix: an explicit `class` field always wins and the id fallback applies only to `d1-` ids; the frozen receipt prints
`bytes_cases=80` (a 38 + b 16 + n 26), the declared subset.

## Wave findings routed (before the freeze)

R93MReviewC1 F1/F2 (NUL as a C-string end with the group scan and Encoding length over the whole line — the L1 patched
the candidate and folded the reviewer's 53 fixtures plus 13 L1 cases into the frozen set; continuation bytes after `]` found
by the L1 while reading `g_key_file_line_is_group`); R93MConnector §6 (six byte-class selftest checks in the tool);
R93MMutC1 §5.1–5.3 (X19 crash-shaped, MB06 inadmissible, MB11 killed by two added cases and frozen); R93MCritic C1-F1/F2/F3
(class rule, tool pin, fresh-bytes leg load-bearing: the table forgery scores 366/366 frozen and fails 50/60 fresh bytes),
C2-F1 (the fresh-seeded clause replaced by neutral edits), C2-F2/F3 (landing paths, the 22-mutant file); R93MReviewC2
§2–§5 (kills, rc-sensitive verdicts, setup-path probes for the gate mutants); R93MMutC2 §5–§6 (setup panel, six escapes
turned into kills and weakenings); R93MExecCasesC1 (71 byte cases, oracle written as bytes); R93MExecCounterC1/C2 (counters,
rewritten by the L1 for C2); R93MExecHost (host replay and the harm baseline).

## Gate

### Registry rows added (opened 2026-11-07 by the L1 `MadoR93`; `.ufo/waves/round-93/receipts/sources-open-r93.txt`)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S511 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.c (6ea1c433…2fd4) | 2026-11-07 | `0x004, 0x104, 0x104, 0x004, 0x104, 0x104, 0x004, 0x004,` | gstrfuncs.c 264 |
| S512 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gstrfuncs.h (298b0dc4…6e23) | 2026-11-07 | `((g_ascii_table[(guchar) (c)] & G_ASCII_SPACE) != 0)` | gstrfuncs.h 86 |
| S513 | https://raw.githubusercontent.com/flatpak/xdg-desktop-portal/1.22.1/src/xdp-portal-config.c (2da4fd83…4fe1) | 2026-11-07 | `g_critical ("Invalid portals for interface '%s' in %s", ifaces[i], portal_file);` | xdp-portal-config.c 430 |
| S514 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c (e1d1270f…f656) | 2026-11-07 | `return (*line == '#' \|\| *line == '\0' \|\| *line == '\n');` | gkeyfile.c 4563 |

Every file was fetched twice with identical digests; R93MScoutSources fetched all four independently and reproduced every
digest (its §1, §3). S513 and S514 share URLs with S501/S502 under different scopes (CORPUS.md rule 2; census W04, not an
error). Status `mined` (cited by `corpus/knowledge/portal-keyfile-bytes-r93.md`).

### Registry rows touched (old → new)

- S511–S514 used-by: `corpus/knowledge/portal-keyfile-bytes-r93.md` (C1 commit) → `corpus/knowledge/portal-keyfile-bytes-r93.md,corpus/lessons/round-93.md` (records commit).

### Candidates considered (round 93) — every gate decision of the round

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/portal-keyfile-bytes-r93.md` | **admit** | every rule cites an S511–S514 line or a frozen case labelled by the installed binary; the tool that models it is measured on the same set | a GLib or xdg-desktop-portal tag that changes gkeyfile.c, gstrfuncs.c/.h or xdp-portal-config.c |
| the draft's "a VT at line start/key end/value start voids the file" | **reject** (rewritten before the freeze) | only the group-header position voids; the other three mangle a key or value (entry §3.8, R93MScribeEntry) | none on GLib 2.90.1 |
| a registry row for `src/portal-impl.c` | **reject** | 404 at tag 1.22.1; the reader is `xdp-portal-config.c` (S501/S513) | none |
| freezing mutants X19 and MB06 | **reject** | crash-shaped on the ported bytes (QUALITY 148); MB06's only difference is a `UnicodeEncodeError` | a case that makes either a well-formed wrong answer |
| the 20-kill set with unique killers | **reject** | 20/23, 4/10, 11/20 (R93MReviewC2) | none: replaced by the 32 exact-set kills |
| the fresh-seeded C2 clause | **reject** (before any measurement) | exhaustive per-check neutralisation makes a seeded sample redundant; neutral edits defeat the sha-diff forgery the sample never tested | a weakening grammar the panel does not enumerate |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | no staged GKeyFile/portal-config entry (R93MConnector §2); collision check `reg-ids` 449, `staged-ids` 147, `collisions` 94 (`.ufo/waves/round-93/assimilation/`) | a staged entry on this plane with a pinned locator |

### Spot-check (round 92, `corpus/lessons/round-92-verifier-spotcheck.md`)

- Routed defect 1 (cross-domain item) → M93-4, the report's item, QUALITY 157.
- Routed defect 2 (land the portals port under its own frozen counter with regenerated round-90 mutants) → C1.
- Routed defect 3 (a weakened passing selftest assertion is invisible) → C2.

### Census

- Start: `.ufo/waves/round-93/receipts/census-start-r93.txt` — `mado ok`, rc 0; 445 rows at the base.
- End: `.ufo/waves/round-93/receipts/census-end-r93.txt` — 449 rows (S511–S514, tier A 4).

## Considerthese

`considerthese/2026-11-06.md` proposal 4 ("Widen desktop coverage … xdg-desktop-portal / screen-share … Prefer one
operator-config gap over another harness counter"): C1 is an operator-config gap — a hand-edited
`~/.config/xdg-desktop-portal/portals.conf` with a Latin-1 value, a stray VT before a group or a NUL silently loses every
`[preferred]` choice (entry §7). Proposal 1 (survivor ledger): R93MConnector §5 found the round-87 mako survivors M03, M05,
M06, M08, M10 all killed in round 88 (`.ufo/waves/round-88/receipts/c1-measured-A-r88.txt` lines 194–201) — closed.

## Cross-domain evidence

GLib internals (gkeyfile.c, gstrfuncs.c/.h), Python's `surrogateescape` handler and test-mutation methodology; no sibling
lane owns any of them (R93MConnector §4 sweep over every sibling PROVINCE.md: `none` ×20). kotoba runs a
`selftest-kills.py` for its own verifiers (`kotoba-shokunin/verifiers/fixtures/round-100/selftest-kills.py`) — cited as
method, not absorbed.

## Domain share

New or changed artifacts: one desktop-facing tool change (`tools/mado-portals.py`), one knowledge entry, four registry rows,
one PROVINCE refinement (desktop-facing); one record gate and its kill-set, two counters, four QUALITY criteria
(lane-internal). Desktop-facing: 4 of 10.

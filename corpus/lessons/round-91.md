# mado round 91 — lessons

Round 91, hyaku run 15, attempt 1 (`MadoR91`). Two frozen claims from `.ufo/waves/round-91/claims-declaration-r91.md`
(freeze `fa71279fc927f86df2d14a62f1f60230a7cf4ada`): C1 coverage capability (a read-only resolver of which `.desktop`
application GLib 2.90.1 opens a MIME type with — default, registered and recommended — scored against the installed
`gio mime`) and C2 operability (a runnable seat-report retention gate over the lane's wave dispatches, routed by round
90's lesson M90-4 and spot-check defect 2).

## Mistakes

**M91-1 — a parser model reused from round 90 carried four GLib divergences into a new consumer.**
Class: inherited-model reuse — a model proved on one consumer's inputs is copied to another whose inputs reach rules the
first case set never exercised.
Evidence: the C1 candidate copied the GKeyFile reader of `tools/mado-portals.py` (round 90). w1 seats found it wrong for
mimeapps files on four byte classes: invalid UTF-8 voided the whole file where GLib fails only the key read
(R91MReviewC1 R1, cases rv-01/rv-02; R91MMutC1 mc-12), `\v` was treated as whitespace where `g_ascii_isspace` excludes it
(R91MExecShell F7, case sh-38), a repeated key moved to its last position where `g_key_file_get_keys` keeps the first
(R91MExecFuzz F2, R91MMutC1 mc-10), and a key ending in `[]` was dropped where `key_get_locale` makes it a plain key
(R91MReviewC1 R2, rv-03). Round 90's 229 portal cases contained none of these inputs, so its TARGET_MET said nothing
about them.
Captured-by: none in round 90 — the reused rules had no case on these classes; round 91's w1 attack seats found them.
Fix: the four rules are rewritten from S502 in `tools/mado-mime.py` and pinned by frozen cases (rv-01..03, sh-38, mc-10,
mc-12). Shown able to fail: the frozen mutants that restore the old behaviour — X24 (invalid UTF-8 skips the file), X36
(repeated key moves to its last position), M28 (locale-suffixed keys kept), M29 (Encoding unchecked) — are each killed on
the frozen set (`.ufo/waves/round-91/receipts/c1-measured-r91.txt`, `killed=65` of 65). Criterion: `QUALITY.md` 152.
Routed (not landed): `tools/mado-portals.py` still carries the four divergences; round 92 re-proves it against the
xdg-desktop-portal oracle on these byte classes.

**M91-2 — two of the L1's own selftest assertions stated GLib behaviour from reading, and both were wrong.**
Class: belief-as-assertion — a selftest that asserts what the author expects upstream to do, without the oracle.
Evidence: the first draft of the candidate's selftest asserted that a `[Removed Associations]` group written before
`[Added Associations]` blocks the addition, and that a masked addition leaves no default; `gio mime` on the same
fixture (an L1 scratch run before the w1 dispatch; not kept as a receipt) answered `a.desktop` (GLib reads the Added
group first whatever the file order: keys of the added group at S504 gdesktopappinfo.c:919, removals at :945, defaults at
:971) and `b.desktop` (the hidden lower copy is accepted for the default). The selftest printed `checks=17 failed=2`
against a model that was right.
Captured-by: running the oracle on the selftest's own fixture before the wave — no rule required it.
Fix: both fixtures are frozen cases (l06, m01 and w06) labelled by gio, and the selftest expectations were rewritten to
gio's answers. Not shown able to fail as a rule: no instrument checks that a selftest assertion has an oracle label; this
lesson routes that check to a later round and does not claim it.

**M91-3 — a fixture id named a rule its bytes did not test (second occurrence of the M90-1 class).**
Class: fixture-construction — `p04-exec-absolute-nonexec` was written with a placeholder `BIN/plain` path and patched to
`plain %f` (a PATH lookup) in the generator's `__main__`, so the case named "absolute" tested a PATH search.
Evidence: `.ufo/waves/round-91/controls/gen-c1-cases-r91.py` before the w1 dispatch (the patch loop); renamed to
`p04-exec-on-path-not-executable` before the freeze. The absolute-path rule is now covered by R91MExecShell's sh cases.
Captured-by: the L1's own read of the generator; QUALITY 150 covers concatenated fixtures, not ids rewritten in place.
Fix: the generator writes each fixture once, in its `case()` call; no post-hoc rewrite loop remains. Not shown able to
fail as a check.

**M91-4 — the C2 premise sentence named `check-deliverables.py` as silent on seat reports; it is silent only on seats that left none.**
Class: premise overstatement — a before-state sentence broader than the measured before-state.
Evidence: the declaration says "at `cc0381db` `quality/check-receipt-presence.py` and `quality/check-deliverables.py` say
nothing about seat reports"; R91MScoutSources §4(i) shows `check-deliverables.py` at `cc0381db` parses `Report:` lines
inside the report files it is handed (`:34`, `:39`) and fails a named path that is absent (`:114`, `:124`). What it cannot
do is enumerate a dispatch's seats and flag one that wrote nothing — R91MResidC2 §6 confirms no check at `cc0381db` reads
a dispatch. The counted before-state ("lane checks that detect a missing seat report for a dispatched seat 0 → 1") and
the frozen predicate are unaffected; the sentence is corrected by an erratum, not rewritten.
Captured-by: the w1 source scout, after the freeze. Fix: SCORECARD round-91 erratum; a premise sentence in a later
declaration names the exact behaviour the before-state lacks. Not a mechanical check.

The D2 outcome: the landed gate on this round's own waves, run while R91MScoutSources and both r1 seats were still in
flight, printed three SR01 lines (quoted in `.ufo/waves/round-91/w1/R91MScoutSources.md` §4(ii)); after both WAVE-DONE
messages it prints `seats=16 present=16 … verdict=OK`, rc 0 (`.ufo/waves/round-91/receipts/c2-gate-round91-r91.txt`), and
`w1-results.json`/`r1-results.json` retain every seat's output this time.

## Wave findings routed (instruments frozen or named as limits)

Before the freeze the w1 findings changed the candidate, the counters and the sets: R91MExecShell F1–F8 (ported
`g_shell_parse_argv`/`g_find_program_for_path`, Hidden whitespace), R91MReviewC1 R1–R3 (per-key UTF-8, `[]` keys, xdgmime's
own `getenv` for the mime dirs), R91MMutC1 (12 killing cases; mime.cache 40-byte header), R91MExecFuzz F1–F3 (readdir
order for colliding ids; duplicate-key position; duplicate aliases — modelled with libc `qsort`/`bsearch` instead of
excluded), R91MCritic F1–F9 (fresh leg in the predicate, sandbox narrowed and its wording corrected, opaque tool paths,
`--fresh` ≥ 1, pins and argv in the declaration, PROVINCE refinement, ledger/registry rows split by commit),
R91MReviewC2 F1–F4 (rev-mode selftest cases, `--all` with no dispatch is a setup error), R91MExecGate's independent
labels (SR04 a defect, symlink SR03), R91MMutC2 F1–F8 (eight fixtures, selftest compared per mutant, equivalents carved
out, scope docstring).

## Residual r1 (on the measured bytes)

- R91MResidC1 (reviewer): C1 re-measured `TARGET_MET`, identical summary; 18 new fixtures agree with gio. Its suggested
  erratum — "`NoDisplay=true` also drops an app from both lists (rs-08)" — is **rejected**: in rs-08 the app's file is in
  `~/.local/share/applications` and its association in `/usr/share/applications/mimeinfo.cache`, so the association is
  masked by the higher-precedence file (S504 gdesktopappinfo.c:283-306, :1312-1349); `NoDisplay` is read
  (`load_from_keyfile`) but filters neither list: gio gives empty lists for rs-08 *without* `NoDisplay`, and full lists
  for a `NoDisplay=true` app whose association sits in its own directory (`.ufo/waves/round-91/receipts/nodisplay-check-r91.txt`). The entry's §8 stays as written.
- R91MResidC2 (critic): C2 re-measured `TARGET_MET`, identical stdout; six gate defects outside the frozen set (F1 symlinked
  dispatch skipped in `--rev`, F2 unparseable finding lines, F3 repeated `--round`, F4 FIFO dispatch hang, F5 symlinked
  parent directory, F6 `counts.total`), routed to round 92 (SCORECARD round-91 errata). The fresh leg's truth was checked
  independent of the check, but its vocabulary equals the set's, so it could not see F1–F6.

## Gate

### Registry rows added (opened 2026-11-06 by the L1 `MadoR91`; `.ufo/waves/round-91/receipts/sources-open-r91.txt`)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S504 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c (sha256 8e9ce1a8…5b0d) + gio/gio-tool-mime.c (40a450ec…bd60) | 2026-11-06 | "/* (If any), see if one of those apps is installed... */" | gdesktopappinfo.c 4751 |
| S505 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmime.c (afb1c1c1…2410) + gcontenttype-fdo.c, xdgmimecache.c, xdgmimealias.c, xdgmimeparent.c | 2026-11-06 | "if (_caches) return _xdg_mime_cache_unalias_mime_type (mime_type);" | xdgmime.c 739-740 |
| S506 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gshell.c (640a0d0f…0442) + glib/gutils.c (65086c29…3771) | 2026-11-06 | "if (g_path_is_absolute (original_program)) return NULL;" | gutils.c 363-364 |
| S507 | https://specifications.freedesktop.org/mime-apps-spec/latest/ (default.html 00b5c8f3…7ec6; 1.0.1) | 2026-11-06 | "Note as well that the default application for a given type must be an application that is associated with the type." | default.html, section 4 |

### Registry rows touched (old → new)

- S502 used-by: `corpus/knowledge/xdg-portal-routing-resolver-r90.md,corpus/lessons/round-90.md` →
  `corpus/knowledge/xdg-portal-routing-resolver-r90.md,corpus/lessons/round-90.md,corpus/knowledge/mime-default-resolution-r91.md`
  (C1 commit `54a0683c`) → `…,corpus/lessons/round-91.md` (records commit).
- S504–S507 used-by: `corpus/knowledge/mime-default-resolution-r91.md` (C1 commit) → `…,corpus/lessons/round-91.md` (records commit).

### Candidates considered (round 91)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mime-default-resolution-r91.md` (search order, groups, default and list algorithms, load rules, MIME db, GKeyFile byte rules, host answers) | **admit** | every rule cites S502/S504–S506 at a line; the decision-table rows name frozen cases gio labelled; the host replay 1211/1211 is a committed receipt | a GLib tag that changes gdesktopappinfo.c, gkeyfile.c or xdgmime |
| S507's "the default application … must be an application that is associated with the type" as GLib's rule | **reject** | GLib 2.90.1 takes the first loadable collected id and never checks association (S504 gdesktopappinfo.c:4740-4775); case l03: default `c.desktop`, registered `[]` | a GLib release that adds the association check |
| a shlex split as the `Exec=` parser | **reject** | 15 of 65 R91MExecShell cases disagreed with gio in 7 classes; S506 ported instead | none: the port is exact on the frozen set |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | R91MConnector §2: no staged entry on MIME/default applications/desktop entries; collision check `.ufo/waves/round-91/assimilation/collisions` holds 94 ids (438 registry vs 147 staged) and 53 more staged ids sit below the registry tip | a staged entry on this plane with a pinned locator |

### Spot-check (round-90, `corpus/lessons/round-90-verifier-spotcheck.md`)

- Routed defect 1 (gate self-test missing) → D1: `quality/check-receipt-presence.py --selftest` (R91MExecD1; 87 added lines,
  0 removed; `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0`; three mutants each make it exit 1,
  `.ufo/waves/round-91/receipts/d1-selftest-r91.txt`), registry row updated; commit `cbbeb862`.
- Routed defect 2 (seat outputs not retained) → C2 (`quality/check-seat-reports.py`) and the w1 context line naming a report
  path for every seat.
- Routed defect 3 (lesson wording) → D3 note below.

**D3 (append-only note on `corpus/lessons/round-90.md`, Gate reject row):** the round-90 reason "ranks UseIn hits for the
first desktop" is narrow: `sort_impl_by_use_in_and_name` walks the desktops in order and decides at the first desktop
where the two backends' UseIn membership differs, falling to the source-name order only when no desktop separates them
(S501 `xdp-portal-config.c:278-293`). The decision recorded there is unchanged.

### Census

- Start: `.ufo/waves/round-91/receipts/census-start-r91.txt` — `mado ok`, rc 0; 438 rows at the base.
- End: `.ufo/waves/round-91/receipts/census-end-r91.txt` — see the report; 442 rows (S504–S507, tier A 4).

## Considerthese

`considerthese/2026-11-06.md` proposal 4 ("Widen desktop coverage past bar + mako … Prefer one operator-config gap over
another harness counter"): C1 takes the default-application plane — Omarchy's own `~/.config/mimeapps.list` and
`hyprland-mimeapps.list` decide what `xdg-open` launches, and the lane now answers it for every type the host names
(1211/1211 against gio). Still open from the same proposal: screen-share runtime (`xdph.conf`), clipboard, hypridle.

## Domain share

New or changed artifacts: one desktop-facing tool (`tools/mado-mime.py`), one knowledge entry, four registry rows, one
PROVINCE refinement (desktop-facing); one records gate (`quality/check-seat-reports.py`), one selftest (D1), two counters
(lane-internal). Desktop-facing: 3 of 7.

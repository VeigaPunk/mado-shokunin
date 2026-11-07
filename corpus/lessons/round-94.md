# mado round 94 — lessons

Round 94, hyaku run 15, attempt 1 (`MadoR94`). Two frozen claims from `.ufo/waves/round-94/claims-declaration-r94.md`
(freeze `bcc5429b68a8b60bc5238fa06f01818686a9d465`): C1 coverage, new surface (`tools/mado-mimeglob.py`: the MIME type
GLib 2.90.1 guesses from a file name alone, cache and text mode) and C2 operability (kill-sets for
`tools/mado-xdgmime.py` and `tools/mado-mime.py` under the unchanged round-93 selftest-strength gate — round-93
spot-check routed defect 2).

## Mistakes

**M94-1 — the L1's wave candidate path-joined `HOME` where xdgmime concatenates it.**
Class: idiom drift in a port — a "harmless" library call (`os.path.join(home, ".local/share")`) replacing the C string
concatenation (`strcpy (…, home); strcat (…, "/.local/share/mime/")`) changes the answer for an edge value: an empty
`HOME` gives the relative `.local/share`, read from the caller's working directory, where GLib reads the absolute
`/.local/share/mime/`; an unset `HOME` gave `/` where GLib adds no user directory.
Evidence: R94MReviewC1 F1 (`.ufo/waves/round-94/w1/R94MReviewC1.md` lines 37–69; case `rv-dirs-04-home-empty-relative`).
The logic was copied from `tools/mado-mime.py:813-824` (round 91), which carries the same defect today (sweep below).
Captured-by: none in the lane — R94MReviewC1 found it reading `xdgmime.c:255-262` beside the tool.
Fix: the candidate concatenates and has `--home-unset` (`build/mado-mimeglob.c1b.py`); frozen cases `rv-dirs-04`,
`l1-dirs-01`, `l1-dirs-02`; mutants `dirs-05-home-concat`, `dirs-06b-home-unset`, both killed
(`.ufo/waves/round-94/receipts/c1-measured-r94.txt`). Shown able to fail: the wave candidate
`build/mado-mimeglob.c1.py` scores 355/370 (`.ufo/waves/round-94/receipts/c1-controls-prefreeze-r94.txt`). Criterion:
`QUALITY.md` 159. Routed: `tools/mado-mime.py` (alias/parent dirs) has the same two edges — its C2 kill-set pins its
bytes this round, so the fix is next round's.

**M94-2 — the draft C1 predicate read its class list from the case file it judged.**
Class: self-referential population — "every class named in the case file" cannot fail, so the 20-class coverage the
declaration promised was asserted, not measured.
Evidence: R94MCritic C1-F1 (`.ufo/waves/round-94/w1/R94MCritic.md`); draft text at `5a164538`.
Captured-by: R94MCritic, before the freeze.
Fix: the frozen predicate enumerates the 20 classes and a minimum of 6 cases each; the counter refuses an unknown class
and prints `classes=20/20` (`quality/counters/c1-r94-mimeglob.py`, `CLASSES`, `MIN_PER_CLASS`). Criterion: `QUALITY.md`
160.

**M94-3 — kill-sets that covered every selftest label let 46 of 112 green weakenings through.**
Class: coverage of labels is not strength — a kill guards a check only against the weakenings that make that check pass
on that mutant; a check comparing `(id, rc)` weakened to compare the id alone still fails on every kill that flips the id.
Evidence: R94MMutC2 §2 (`.ufo/waves/round-94/w1/R94MMutC2.md`: 23 + 23 escapes, each with a verified closing kill);
R94MReviewC2 §3 (a one-kill forgery covers 12/12 labels); R94MCritic C2-F1 (a two-kill forgery, 12/12 neutralisations).
Captured-by: the w1 attack seats, before the freeze (QUALITY 156 — exact-set kills — was met and was not enough).
Fix: 19 closing kills added; the panel holds the 91 green hand weakenings; conjunct (vii) requires the first-draft
kill-sets to flag fewer. Shown able to fail: the first-draft kill-sets score `hand_flagged=45/91` and MISS
(`.ufo/waves/round-94/receipts/c2-controls-prefreeze-r94.txt`). Criterion: `QUALITY.md` 161.

**M94-4 — a behavioural predicate for a re-implementation accepts a tool that asks the oracle.**
Class: oracle-exec forgery — every behavioural conjunct is met by a wrapper around the library being modelled.
Evidence: R94MCritic C1-F2 (`w1/R94MCritic/evidence/wrapper-tool.py`, 0 mismatches on 321 names); the L1's ctypes
forgery `controls/forgery-ctypes-gio-r94.py` scores 370/370, fresh 60/60, host 9745/9745.
Captured-by: R94MCritic, before the freeze.
Fix: conjunct (vi) `static_no_external_resolver` (AST: no process/socket/import machinery, ctypes only for libc) and an
empty `PATH` for every tool run. Shown able to fail: both forgeries print `static_no_external_resolver=FAIL`
(`import:subprocess:3`, `lib:libgio-2.0.so.0:23`) in `c1-controls-prefreeze-r94.txt`. Criterion: `QUALITY.md` 162.

**M94-5 — the declaration says the name-to-type step precedes "every" default-application answer.**
Class: caller premise overstatement, a recurrence of M92-2 — `xdg-open` on Hyprland asks `xdg-mime query filetype`,
which runs `file(1)`, not this glob lookup; the step precedes the GLib/gio answers only.
Evidence: R94MConnector §4.C; `claims-declaration-r94.md` C1 first paragraph (frozen); the knowledge entry §1 states the
scope correctly.
Captured-by: QUALITY 154 (should have; a reviewer reading the sentence) — it was not applied by the L1 to its own
declaration; R94MConnector caught it.
Fix: the frozen declaration is not rewritten; this lesson, the SCORECARD row and the report name the precise scope (GLib
callers: `gio open`, GTK file choosers, `g_app_info_launch_default_for_uri` paths that guess by name).

**M94-6 — the first wave spec used `labrat`, which the validator does not accept as a swarm role.**
Class: protocol vocabulary vs validator taxonomy — the round prompt lists `labrat` as an attack role; the wave validator
refuses it (`unknown_role`).
Evidence: `.ufo/waves/round-94/receipts/validator-refusal-r94.txt`.
Captured-by: the validator (rc 1, nothing spawned).
Fix: the hypothesis probe rode a `reviewer` seat (R94MProbeC1). Not a new criterion: the validator is the instrument.

Sweep for an unmined earlier mistake: R94MConnector §7 names the round-93 harm harness's uncreated mako scratch
directory (`.ufo/waves/round-93/receipts/harm-final-r93.txt` 59–61, corrected append-only); this round's
`controls/harm-r94.sh` creates every scratch directory first (its line 8).

## Wave findings routed (before the freeze)

R94MReviewC1 F1–F7 (HOME concatenation, recursion depth on a 1000-byte suffix, text files parsed beside a cache, bare `*`,
non-UTF-8 glob bytes, cache strings past EOF, docstring) → candidate `c1b` (iterative trie walks, lazy text parse,
xdgmimeint.c byte decoding, zero-filled last page); R94MProbeC1's nine cache/text mechanisms → 24 frozen pair cases and
entry §3.1; R94MMutC1's 57 mutants (13 re-anchored by the L1 to `c1b`, 4 equivalents kept with their arguments) + 14 L1
mutants for the fixes (7 then excluded with arguments: unobservable or crash-shaped); R94MExecCasesC1's 235 cases (its two
refusal cases answered by `c1b`); R94MCritic C1-F1…F5, C2-F1…F4 → predicate amendments; R94MExecKillsC2 + R94MMutC2 →
46 kills; R94MExecCounterC2 → counter + 12 hand weakenings + 6 neutral edits; R94MScribeEntry → the entry (edited by the
L1: S517 digest, landed pins, §3.1, §3.2, §6 limits); R94MExecHostC1 → host name list and harm harness.

## Gate

### Registry rows added (opened 2026-11-07 by the L1 `MadoR94`; `.ufo/waves/round-94/receipts/sources-open-r94.txt`)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S515 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimeglob.c (38ed8623…0734) | 2026-11-07 | `if (fnmatch ((const char *)list->data, file_name, 0) == 0)` | xdgmimeglob.c 473 |
| S516 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimecache.c (ccda4366…db69) | 2026-11-07 | `n = cache_glob_lookup_fnmatch (lower_case, mimes, n_mimes, FALSE);` | xdgmimecache.c 707 |
| S517 | https://specifications.freedesktop.org/shared-mime-info-spec/latest/ar01s02.html (e00fa00e…c61e), version 0.21 | 2026-11-07 | "If several patterns of the same weight match then the longest pattern SHOULD be used." | §2.4 The glob files |
| S518 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype-fdo.c (8a5b4f47…2d7c) | 2026-11-07 | `/* Conflicts, and sniffed type was no help or not there. Guess on the first one */` | gcontenttype-fdo.c 677-678 |

Every file was fetched twice with identical digests (the spec page four times: the scribe seat reported a raw digest
`1566c459…`; two L1 re-fetches gave `e00fa00e…` again — the seat's sentence that the receipt held a tag-stripped copy is
rejected below). R94MScoutSources, R94MReviewC1, R94MProbeC1 and R94MScribeEntry each reproduced the GLib digests. S516
and S518 share URLs with S505 under other scopes (CORPUS.md rule 2; census W04). Status `mined` (cited by
`corpus/knowledge/mime-glob-guess-r94.md`).

### Registry rows touched (old → new)

- S505 used-by: `corpus/knowledge/mime-default-resolution-r91.md,corpus/lessons/round-91.md` →
  `…,corpus/knowledge/mime-glob-guess-r94.md` (C1 commit; re-opened, same digest `afb1c1c1…2410`).
- S515–S518 used-by: `corpus/knowledge/mime-glob-guess-r94.md` (C1 commit) → `…,corpus/lessons/round-94.md` (records).

### Candidates considered (round 94) — every gate decision of the round

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mime-glob-guess-r94.md` | **admit** | every rule cites an S515–S518/S505 line or a frozen oracle-labelled case; the landed tool answers its 101 rows and the 370 frozen cases as the installed GLib does | a GLib tag that changes any of the four xdgmime files or gcontenttype-fdo.c |
| S515–S518 | **admit** | opened twice by the L1, digests reproduced by four seats | a newer GLib/spec pin |
| the scribe's "the receipt holds the tags-stripped copy" | **reject** | four L1 fetches of the raw page give `e00fa00e…`, the receipt's digest | a fetch that varies by client |
| the wave candidate `build/mado-mimeglob.c1.py` | **reject** (replaced by `c1b`) | 355/370; F1 wrong answers, F2–F6 refusals and a crash | none |
| R94MExecCasesC1's "move the two refusal cases to an allowance" | **reject** | GLib answers them; the tool was fixed to answer them instead (`bytes-04`, `bytes-05` correct) | none |
| 8 L1/seat mutants as counted (`dirs-03`, `mode-05`, `fgets-01`, `fgets-04`, `utf8-04`, `cache-08`, `cache-09`, `mode-06`) | **reject** (listed in `equivalent_not_counted` with arguments) | equivalent, unobservable (the oracle loops) or crash-shaped | a case that makes one a well-formed wrong answer |
| a singleton-kill conjunct for C2 | **reject** as a conjunct (printed: 22/29) | the panel and control (vii) measure what singletons only approximate; 7 labels have no narrow production mutant (R94MExecKillsC2 notes) | a singleton kill for each remaining label |
| guarding `tools/mado-mimeglob.py` in C2 (R94MCritic C2-F2) | **reject** | C2 would depend on C1 having landed (separability) | next round, as its own claim |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | no staged MIME-glob entry (R94MConnector §3); collision check `reg-ids` 449, `staged-ids` 147, `collisions` 94 (`.ufo/waves/round-94/assimilation/`) | a staged entry on this plane with a pinned locator |

### Spot-check (round 93, `corpus/lessons/round-93-verifier-spotcheck.md`)

- Routed defect 1 (QUALITY 158 has no instrument): not built this round (the claim cap went to C1/C2). Applied by hand:
  the w1 context lists the only URLs a seat may cite and requires an HTTP status for any other
  (`.ufo/waves/round-94/w1-spec.json`); seats that fetched recorded statuses (R94MScoutSources: update-mime-database.cpp).
  The instrument stays routed.
- Routed defect 2 (selftest-strength gate wired for one tool) → C2 (two more tools; five lane tools and the gate itself
  remain unguarded — named limit).
- Routed defect 3 (freeze the portal entry's §8 "no frozen case" classes): not done — no portal change this round; routed.

### Census

- Start: `.ufo/waves/round-94/receipts/census-start-r94.txt` — `mado ok`, rc 0; 449 rows at the base.
- End: `.ufo/waves/round-94/receipts/census-end-r94.txt` — 453 rows (S515–S518, tier A 4).

## Considerthese

`considerthese/2026-11-06.md` proposal 4 ("Widen desktop coverage past bar + mako … Prefer one operator-config gap over
another harness counter"): C1 is an operator-config gap — a hand-written `~/.local/share/mime/packages/*.xml` without
`update-mime-database`, a stale user `mime.cache` that silences the user's `globs2` (this host has both), or a
capitalised extension decide which type, and so which application, GLib picks (entry §4). Proposal 5 (QUALITY 145 needs
an instrument): not addressed.

## Cross-domain evidence

GLib xdgmime and gcontenttype (GNOME/GLib), the shared-mime-info database format and `update-mime-database`
(freedesktop.org; its ALPM hooks are tsukuroi's: `tsukuroi-shokunin/corpus/knowledge/pacman-hook-order-r38.md:53,97`),
glibc `fnmatch(3)`/`qsort(3)`; R94MConnector §2 swept every sibling `PROVINCE.md` and knowledge tree: only mado reads
the MIME database bytes, tsukuroi owns the hook that runs the builder; no other lane touches it.

## Domain share

New or changed artifacts: one desktop-facing tool, one knowledge entry, four registry rows, two PROVINCE refinements
(desktop-facing); two kill-sets, two counters, four QUALITY criteria (lane-internal). Desktop-facing: 8 of 14.

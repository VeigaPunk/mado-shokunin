# mado round 95 — lessons

Round 95, hyaku run 15, attempt 1 (`MadoR95`). Two frozen claims from `.ufo/waves/round-95/claims-declaration-r95.md`:
C1 coverage, new surface (`tools/mado-mimesniff.py`: the MIME type GLib 2.90.1 guesses when it is given a file's bytes,
with or without a name, from the magic section of `mime.cache`) and C2 operability (kill-sets for
`tools/mado-mimeglob.py` and `tools/mado-portals.py` under the unchanged round-93 selftest-strength gate — round-94
spot-check routed defect 3).

## Mistakes

**M95-1 — the L1 wrote GLib's `looks_like_text` from C's `isspace`, and its own selftest encoded the error.**
Class: library-semantics substitution — `g_ascii_isspace` is a table lookup whose space bit covers TAB, LF, FF, CR and
space but **not** VT (0x0b); the L1's draft treated 8–13 as GLib treats them except BS, i.e. as C `isspace` does, and
wrote selftest check `s10 VT passes looks_like_text` expecting `text/plain 0`, so `--selftest 23/23` certified the bug.
Evidence: R95MCritic C1-F1 (`.ufo/waves/round-95/w1/R95MCritic.md` lines 27–56: a 256-byte sweep, one diff at 0x0b),
R95MReviewC1 F1, R95MProbeC1 F1 (38 of 2480 fuzz inputs, all VT), R95MMutC1 F1, R95MExecCasesC1 finding 1,
R95MScribeEntry §F1 — five seats independently. The L1's 7240-input host probe could not see it: no sampled `/usr` file
carries 0x0b in its first 128 bytes without another binary byte (R95MScribeEntry `-host.out.txt`).
Captured-by: none of the L1's own checks (a selftest written from the same misreading cannot catch it); the wave's
byte sweeps did.
Fix: `c1c` adds `b == 11` and rewrites `s10` to expect `application/octet-stream 1` for VT and `text/plain 0` for FF; the
frozen set carries 24 `lltext` cases. Shown able to fail: the wave candidate `build/mado-mimesniff.c1.py` scores below
300/300 on the frozen cases (`.ufo/waves/round-95/receipts/c1-controls-prefreeze-r95.txt`, first block). Criterion:
`QUALITY.md` 163.

**M95-2 — a 301 redirect body was hashed as the source.**
Class: transport status not checked — `curl -fsS` fails only on HTTP ≥ 400, so the registered S517 locator (moved by
freedesktop.org) returned a 109-byte "Moved Permanently" stub with exit 0, and the L1's `sources-open-r95.txt` recorded
its digest `1566c459…` as "smi-s02.html". The same digest is the one the round-94 scribe reported and the round-94 lesson
rejected as "not reproducible" (`corpus/lessons/round-94.md` Gate, flip "a fetch that varies by client"): it was the
redirect stub then too.
Evidence: `.ufo/waves/round-95/receipts/sources-open-r95.txt` (first block and its append-only CORRECTION);
`.ufo/waves/round-95/receipts/locator-status-r95.txt` (both held freedesktop.org spec locators, S507 and S517, answer 301;
`curl -fsS` rc 0 on the stub).
Captured-by: the L1 by diffing against the round-94 seat copy, and R95MScribeEntry independently ("the lane's
`fetch/smi-s02.html` is the 109-byte 301 body"); QUALITY 158 asks for an HTTP status only for URLs outside the registry,
so it did not apply.
Fix: a fetch receipt records `http_code` and `url_effective` and a source digest counts only from a 200 at the recorded
URL; the moved page is registered as S523 at its new locator. Shown able to fail: the status-gated fetch
(`test http_code = 200`) on the old locator exits 1 (`sources-open-r95.txt` CORRECTION), while `curl -fsS` exits 0.
Criterion: `QUALITY.md` 164. Flip of the round-94 reject: the scribe's digest was real bytes (the stub), the reject's
conclusion (the receipt was not a tag-stripped copy) stands, its reason ("not reproducible") does not.

**M95-3 — the selftest-strength gate cannot carry a kill-set for its own selftest.**
Class: self-application blind spot — `non_selftest_prefix` cuts the source at the first text `def selftest(`, which in
the gate's own file is the string literal at line 73 (`text.find("def selftest(")`), so `gate()` lies outside the
prefix and every kill anchored in it is a SETUP_ERROR (`find occurs 0 times`).
Evidence: `.ufo/waves/round-95/receipts/gate-self-prefix-r95.txt` (`cut_line 73 gate_def_in_prefix False`); R95MReviewC2
F5 (measured, with a two-line fix that moves the cut to line 205 and a kill that then holds; the fixed gate breaks the
round-93 and round-94 C2 counters' sha pins on a fixture repo).
Captured-by: none — round 93 built the gate on another tool, round 94 named "the gate's own selftest" as a limit without
looking for the reason.
Fix: not landed (QUALITY 153/155: a gate change must carry the earlier frozen counters re-anchored); routed to the
next round with R95MReviewC2's draft. Shown able to fail: the frozen gate refuses the `gate-rc-flip` kill rc 2.

**M95-4 — the draft C1 predicate scored refusals as a label class and let one crashing input relabel its siblings.**
Class: label granularity — the schema labelled a whole case UNSUPPORTED when one input crashed the one oracle process,
and treated the declared text-mode refusal as unscoreable.
Evidence: R95MReviewC1 F6 (two cases unwinnable), F3 (no-database environments refused though GLib answers them);
R95MMutC1 F3 (`text_mode_removed` not countable).
Captured-by: the w1 attack seats, before the freeze.
Fix: one oracle run per input; `expect_refusal` for the declared limits only (text database present, depth > 4096);
no-database environments answered. Shown able to fail: mutants `text_files_ignored` and `no_database_refused` are
counted and killed in the frozen run.

Sweep for an unmined earlier mistake: the round-94 Gate's reject reason for the scribe digest (M95-2) — mined above.

## Wave findings routed (before the freeze)

R95MCritic C1-F1…F7, C2-F1…F4; R95MReviewC1 F1–F6; R95MProbeC1 F1–F3; R95MMutC1 F1–F6 (89 mutants on c1, 88 on c1b,
re-anchored by the L1: 94 counted on c1c, 5 equivalent or crash-shaped with arguments); R95MExecCasesC1 (204 cases, its 8
`expect_refusal` flags removed: those environments hold no text database and GLib answers them); R95MExecCounterC1 (the
counter, extended by the L1 with per-input labels, `expect_refusal`, the structural allowlist, the audit launcher,
`real` rebuild, `class_kills`, memoriser and forgery controls); R95MExecHostC1 (4911-path host list, harm harness);
R95MReviewC2 F1–F5 (singleton minimum; the blanket forgery is a control); R95MExecKillsC2 (17 + 27 kills);
R95MMutC2 (191 weakenings, 42 escapes, 18 closing kills) and two L1 closing kills; R95MExecCounterC2 (counter, 24 + 6
panel); R95MConnector (sibling sweep, GIO caller lines, assimilation none); R95MScribeEntry (the entry; edited by the
L1: ids, c1c, callers, limits).

## Gate

### Registry rows added (opened 2026-11-07 by the L1 `MadoR95`; `.ufo/waves/round-95/receipts/sources-open-r95.txt`)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S519 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimecache.c (ccda4366…db69), HTTP 200 | 2026-11-07 | `if (i + data_length > len) return FALSE;` | xdgmimecache.c 185-186 |
| S520 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimeint.c (c2364aa8…2f29), HTTP 200 | 2026-11-07 | `if (chardata[i] < 32 && chardata[i] != 9 && chardata[i] != 10 && chardata[i] != 13) return XDG_MIME_TYPE_UNKNOWN;` | xdgmimeint.c 185-186 |
| S521 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gcontenttype-fdo.c (8a5b4f47…2d7c), HTTP 200 | 2026-11-07 | `if (g_ascii_iscntrl (c) && !g_ascii_isspace (c) && c != '\b')` | gcontenttype-fdo.c 542-544 |
| S522 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/glocalfileinfo.c (b006a93d…4497), HTTP 200, two fetches | 2026-11-07 | `if (!fast && result_uncertain && path != NULL)` | glocalfileinfo.c 1340 |
| S523 | https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html (e00fa00e…c61e), HTTP 200 | 2026-11-07 | "Checking the first 128 bytes of the file for ASCII control characters is a good way to guess whether a file is binary or text" | §2.12 Recommended checking order |

Every GLib file was fetched twice with identical digests and HTTP 200 (`sources-open-r95.txt` status block); the spec page
twice at its moved locator. S519 and S521 share URLs with S505/S516/S518 under new scopes (CORPUS.md rule 2; census W04).
Status `mined` (cited by `corpus/knowledge/mime-magic-sniff-r95.md`).

### Registry rows touched (old → new)

- S505 used-by: `corpus/knowledge/mime-default-resolution-r91.md,corpus/lessons/round-91.md,corpus/knowledge/mime-glob-guess-r94.md`
  → `…,corpus/knowledge/mime-magic-sniff-r95.md` (C1 commit; re-opened, `xdgmime.c` digest `afb1c1c1…2410` unchanged).
- S519–S523 used-by: `corpus/knowledge/mime-magic-sniff-r95.md` (C1 commit) → `…,corpus/lessons/round-95.md` (records).
- S517 and S507: no cell changed. Their locators now answer 301 (`receipts/locator-status-r95.txt`); S523 holds the moved
  locator for the S517 page; S507's moved locator is routed (not re-opened this round).

### Candidates considered (round 95) — every gate decision of the round

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mime-magic-sniff-r95.md` | **admit** | every rule cites an S519–S523/S505/S511/S512 line or a frozen oracle-labelled case; the landed tool answers the frozen set, fresh cases and the host list as the installed GLib does (measured) | a GLib tag that changes xdgmimecache.c, xdgmimeint.c, xdgmime.c or gcontenttype-fdo.c |
| S519–S523 | **admit** | opened twice by the L1 with HTTP 200; quotes located above | a newer GLib/spec pin |
| the L1's `sources-open-r95.txt` smi-s02 digest `1566c459…` | **reject** (corrected in place, append-only) | it is the 301 stub (M95-2) | none |
| the round-94 reject reason "not reproducible" for the scribe digest | **reject** (the reason; the decision stands) | the stub is reproducible from the old locator | none |
| wave candidate `build/mado-mimesniff.c1.py` and intermediate `c1b` | **reject** (replaced by `c1c`) | VT, wrapped compare, recursion, no-database refusals (M95-1, M95-4) | none |
| R95MCritic C1-F7 "each class kills a mutant no other class kills" | **reject as written**, kept as "each class kills at least one" | a unique kill per class is not a property of a rule set (one mutant can break several classes' rules); the weaker form still refuses a decorative class | a class whose cases kill nothing |
| the 512 depth cap of `c1b` | **reject** | refuses chains GLib answers from 513 on; 4096 keeps the refusal band above every real cache while staying far below the measured 74849/60000 crash depths | a stack-size-dependent oracle label |
| the gate fix for its own selftest (R95MReviewC2 F5) | **reject this round** (routed) | QUALITY 153/155: it breaks two frozen counters' pins; needs a re-anchored carry | next round's claim |
| `tools/mado-mime.py` HOME edges (round-94 routed defect 1) | **reject this round** | changing the tool breaks its round-94 kill-set's `tool_sha256` pin and the r94 C2 counter (QUALITY 153); needs the kill-set re-pinned in the same round | next round with both |
| the mimeglob docstring citation (round-94 routed defect 2) | **reject this round** | the bytes are pinned by the round-94 C1 counter and, now, by C2's kill-set; the correct citation (`xdgmimecache.c:126-139`) is recorded here | the next behavioural change to the tool |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | no staged MIME-magic entry (R95MConnector §3); `reg-ids` 453, `staged-ids` 147, `collisions` 94 (`.ufo/waves/round-95/assimilation/`) | a staged entry on this plane |

### Spot-check (round 94, `corpus/lessons/round-94-verifier-spotcheck.md`)

- Routed defect 1 (`tools/mado-mime.py` HOME): not fixed — see the table (kill-set pin coupling).
- Routed defect 2 (mimeglob docstring citation): not changed — see the table; the correct line is recorded.
- Routed defect 3 (kill-sets for five unguarded tools) → C2 for `tools/mado-mimeglob.py` and `tools/mado-portals.py`;
  the gate's own selftest is M95-3; `tools/mado-mako.py`, `tools/mado-verify.sh`, `quality/check-receipt-presence.py`
  remain.
- Routed defect 4 (QUALITY 158 instrument; portal entry §8 frozen cases): not done; M95-2 shows QUALITY 158's gap.
- Routed defect 5 (QUALITY 154 before the freeze): applied — the declaration's caller sentence cites
  `glocalfileinfo.c`:1337/1340/1373 and excludes `xdg-open`.

### Census

- Start: `.ufo/waves/round-95/receipts/census-start-r95.txt` — `mado ok`, rc 0; 453 rows at the base.
- End: `.ufo/waves/round-95/receipts/census-end-r95.txt` — 458 rows (S519–S523, tier A 5).

## Considerthese

`considerthese/2026-11-06.md` proposal 4 ("Widen desktop coverage past bar + mako"): C1 opens the content step — what a
GIO program shows for a file whose name is ambiguous or unknown (a download without an extension, `x.png` holding a PDF,
an empty file) is decided by these rules, and VT in a text file makes it binary.

## Cross-domain evidence

GLib xdgmime/gcontenttype/GIO local file info (GNOME/GLib), the shared-mime-info format and `update-mime-database`
(freedesktop.org; the ALPM hook that runs it is tsukuroi's: `tsukuroi-shokunin/corpus/knowledge/pacman-hook-order-r38.md:53,97`),
`file(1)`/libmagic (revenger owns its rule grammar: S176/S190 in revenger's registry; mado cites `file(1)` only as
xdg-open's classifier on Hyprland). R95MConnector §1 swept every sibling `PROVINCE.md` and knowledge tree: no sibling owns
shared-mime-info magic.

## Domain share

New or changed artifacts: one desktop-facing tool, one knowledge entry, five registry rows, two PROVINCE refinements
(desktop-facing); two kill-sets, two counters, two QUALITY criteria (lane-internal). Desktop-facing: 9 of 15.

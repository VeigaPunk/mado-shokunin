# mado round 92 — lessons

Round 92, hyaku run 15, attempt 1 (`MadoR92`). Two frozen claims from `.ufo/waves/round-92/claims-declaration-r92.md`
(freeze `6a0134acb08b26b1cd3c6f0a4b8c63495ca89e3e`): C1 coverage capability (a read-only replay of xdg-utils 1.2.1
`xdg-mime query default TYPE`, the resolver `xdg-open` uses on Hyprland, scored against the installed xdg-mime) and C2
operability (`quality/check-seat-reports.py` closes the round-91 residual defects F1–F5, routed by the round-91
spot-check, defect 2).

## Mistakes

**M92-1 — a fix to a frozen-measured gate removed the bytes the earlier round's frozen mutants anchor on.**
Class: frozen-instrument coupling — a tool measured by an earlier round's frozen counter is edited, and the old counter
can no longer run (anchor gone) or a frozen mutant becomes equivalent (the fix covers it another way).
Evidence: the first C2 draft rewrote `{rp}` in the SR02 line; the round-91 counter on it printed
`SETUP_ERROR mutant MC05: find occurs 0 times`, and a scan found K01, K05, MC06, MC10 broken too; after restoring them,
`mutant MC08 SURVIVED` (the new containment test also catches absolute paths in `--worktree`)
(`.ufo/waves/round-92/receipts/prefreeze-draft-transcripts-r92.txt` D-a, D-b). The same class decided routed defect 1:
the port of `tools/mado-portals.py` removes the bytes eight round-90 frozen mutants anchor on (R92MExecD1), so it is
routed, not landed.
Captured-by: the C2 predicate's round-91 leg, which the L1 put in before the first draft — it caught both. R92MCritic
§6.6–6.7 then showed the leg was read from the working tree and mapped the old counter's setup error to a miss.
Fix: anchors kept (`rp = tok(rp)` after the checks), a rev-mode absolute-path selftest case that kills MC08 again, the
leg read from `<rev>` and pinned (`--expect-r91-counter-sha256`), its SETUP_ERROR a setup error. Shown able to fail:
D-a and D-b above. Criterion: `QUALITY.md` 153.

**M92-2 — round 91 admitted "`xdg-open` reduces to GLib" from GLib's side alone.**
Class: caller premise — a sentence about who calls a resolver, never checked against the caller.
Evidence: `corpus/knowledge/mime-default-resolution-r91.md` line 9, `PROVINCE.md` round-91 refinement, `corpus/README.md`
index row and `corpus/lessons/round-91.md` line 142 all say `xdg-open` reduces to `g_app_info_get_default_for_type`;
xdg-utils 1.2.1 `xdg-open` maps Hyprland to `generic` (xdg-open.in:595-596) and asks `xdg-mime query default`
(:392-412, :664-665). On this host the two answers differ for 378 of 1133 types (375 with no `xdg-open` default at all;
`.ufo/waves/round-92/receipts/host-run-r92.txt`).
Captured-by: none — round 91's closure spot-check re-ran gio, not xdg-open.
Fix: append-only corrections (round-91 entry §15, PROVINCE round-92 refinement, README round-92 frontier line), the
round-92 entry and tool; criterion `QUALITY.md` 154 (not mechanical). Shown able to fail: the round-91 sentence fails
154; the host replay's `glib_disagree=378` is the measured consequence.

**M92-3 — a crashing forgery control scored 0 and read as "defeated".**
Class: control fidelity — a control that never ran is indistinguishable, in the receipt, from a control the predicate
rejects.
Evidence: the first label-table forgery wrote JSON `null` into Python source; it crashed on every case
(`correct=0`, below do-nothing 33) (transcripts D-e).
Captured-by: none; the L1 noticed `correct` below the do-nothing control.
Fix: the C1 counter prints `answered=N/cases` for the scored tool. Shown able to fail:
`.ufo/waves/round-92/receipts/m92-3-answered-r92.txt` — a crash-on-load forgery prints `answered=0/270`.

**M92-4 — a selftest expectation written from belief was wrong (second occurrence of M91-2).**
Class: belief-as-assertion.
Evidence: the C1 candidate's first `--selftest` asserted "the first matching file stops the search" for a two-file
fixture; the frozen case m09 (xdg-mime: `e.desktop`) says only a file's first matching line counts and the next file is
read (transcripts D-g, `checks=12 failed=1`).
Captured-by: the selftest run itself, against a model that was right.
Fix: every selftest check now names the frozen case whose installed-xdg-mime label it restates. Not shown able to fail
as a rule (no instrument ties a selftest check to a label); routed.

**M92-5 — the first candidate claimed grep and gawk regex semantics for any asked type.**
Class: over-broad model claim.
Evidence: R92MExecGrep 14 disagreements of 49 (stacked quantifiers, `\{…\}` at an atom position, collating classes,
unknown gawk `-v` escapes), R92MExecShell D2 (gawk escapes), R92MReviewC1 F1.
Captured-by: the w1 attack seats, before the freeze.
Fix: before the freeze the tool declares RFC 6838 restricted-name types as its scope and refuses others (rc 2); the
merge script drops seat cases by that declared rule only, on the case bytes (`controls/merge-c1-cases-r92.py`: 36 type,
2 help, 1 env, 1 nousr). Not narrowed after landing.

## Wave findings routed (before the freeze)

R92MExecGrep (scope, M92-5; gawk unknown escapes fixed in `awk_v` anyway; `OverflowError` caught), R92MExecShell D1
(reversed bracket range crashed the glob translator; now matches nothing, as bash), R92MReviewC1 F2 (a backslash-quoted
glob character is not globbed and stays in the word), F3/F4 (declared refusals listed in the docstring), F5 (premise
numbers re-derived on the frozen set: GLib resolver 139/270), R92MMutC1 (43 mutants, 14 killing cases; 13 survivors of
the L1 cases killed), R92MConnector §5 (`--selftest` added), R92MCritic §2 (frozen set and tool scope reconciled), §3
(bytes clause; bundled-interpreter forgery refused by it), §4 (C2 check sandboxed, fresh leg over F1–F5), §6.6–6.7
(round-91 leg pinned, setup error mapped), R92MReviewC2 findings 1–2 (directory, symlink-to-directory and gitlink
dispatches refused in both modes), R92MMutC2 (20 mutants, 13 fixtures; MC16/MC17 equivalent, not frozen), R92MExecFuzz (12 × 200 frozen-generator cases,
0 disagreements; extended generator disagreements all on declared refusals), R92MExecHost (host driver, 1133/1133).

After the freeze: R92MScoutSources (settled last; WAVE-DONE received 2026-11-06 ~23:50) fetched the three xdg-utils
files and the tag archive twice each and reproduced every S508 digest; its §3 reasons a new row rather than a used-by
update on S490 (different scope; rule 2), which is the move S509/S510 made. All 13 seats left their report files:
`quality/check-seat-reports.py --worktree --round 92` → `seats=13 present=13 verdict=OK`
(`.ufo/waves/round-92/receipts/c2-gate-round92-r92.txt`).

## Gate

### Registry rows added (opened 2026-11-06 by the L1 `MadoR92`; `.ufo/waves/round-92/receipts/sources-open-r92.txt`)

| id | locator | access | located quote (≤25 words) | line |
|---|---|---|---|---|
| S508 | https://gitlab.freedesktop.org/xdg/xdg-utils/-/raw/v1.2.1/scripts/xdg-open.in (a6b0c7af…0790b) + xdg-mime.in (11e7d91e…5c7e) + xdg-utils-common.in (1f6969b5…c532) | 2026-11-06 | `default="$(xdg-mime query default "$filetype")"` | xdg-open.in 395 |
| S509 | file:///usr/share/man/man1/bash.1.gz (bash 5.3.20, container b68beb3e…dffe) | 2026-11-06 | "The -v option displays a single word indicating the command or filename used to invoke command" | MANWIDTH=120 rendering 3880-3881 |
| S510 | file:///usr/share/man/man1/grep.1.gz (grep 3.12, container 9b027d02…85ba) | 2026-11-06 | "The period . matches any single character." | MANWIDTH=120 rendering 270 |

gnu.org (bash and grep HTML manuals) was unreachable twice (curl rc 28); the installed manuals of the same releases were
opened instead and are the rows. S490 (bash manual on tiswww.case.edu, a rejected exit-status row) is not reused: a
different scope.

### Registry rows touched (old → new)

- S508–S510 used-by: `corpus/knowledge/xdg-mime-default-resolution-r92.md` (C1 commit `243326cb`) →
  `corpus/knowledge/xdg-mime-default-resolution-r92.md,corpus/lessons/round-92.md` (records commit).

### Candidates considered (round 92) — every gate decision of the round in one table (round-91 spot-check defect 3)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/xdg-mime-default-resolution-r92.md` | **admit** | every rule cites S508 lines or a frozen case id labelled by the installed xdg-mime; host replay 1133/1133 is a committed receipt | an xdg-utils tag that changes xdg-mime.in, xdg-utils-common.in or xdg-open.in |
| round-91 entry's "xdg-open reduces to GLib" | **reject** (append-only correction §15) | xdg-open.in:595-596, :664-665 and the host's 378 differing types | none on xdg-utils 1.2.1 |
| round-90 entry §9 "invalid UTF-8 makes a file unreadable" | **reject** (append-only correction §12) | S502 gkeyfile.c:2310, :2427; R92MExecD1 re-proof 8/16 | none on GLib 2.90.1 |
| landing the `tools/mado-portals.py` port (`build/mado-portals.d1.py`, 16/16 new, 229/229 old) | **reject this round** (routed) | removes eight round-90 frozen mutant anchors; needs its own frozen counter (QUALITY 153) | a round that freezes portal byte-class cases and regenerated mutants |
| modelling grep/gawk regex-engine behaviour for non-RFC-6838 types | **reject** (declared scope) | R92MExecGrep's 14 disagreements are regex-engine trivia on strings no MIME type contains | a real type outside RFC 6838 restricted-name on the host |
| assimilating a `merge/mado/` theme | **reject** (`Assimilation: none`) | R92MConnector §2: no staged xdg-utils/xdg-open/mimeapps entry; collision check 442 registry vs 147 staged ids, 94 collisions, 53 below the tip | a staged entry on this plane with a pinned locator |
| F6 (`counts.total` vs tasks) as part of C2 | **reject** | a new rule, not a defect of these bytes (R91MResidC2 §5) | a declared rule and its own predicate |

### Spot-check (round-91, `corpus/lessons/round-91-verifier-spotcheck.md`)

- Routed defect 1 → the round-90 entry's §12 correction (append-only) and the re-proof on 16 byte-class cases
  (R92MExecD1: tool 8/16; port 16/16 and 229/229 on the round-90 set); the port is routed (above).
- Routed defect 2 → C2 (F1 and F4 with failing fixtures, F2, F3, F5; F6 rejected above).
- Routed defect 3 → the candidates table above lists every gate decision of round 92.

### Census

- Start: `.ufo/waves/round-92/receipts/census-start-r92.txt` — `mado ok`, rc 0; 442 rows at the base.
- End: `.ufo/waves/round-92/receipts/census-end-r92.txt` — see the report; 445 rows (S508–S510, tier A 3).

## Considerthese

`considerthese/2026-11-06.md` proposal 4 ("Widen desktop coverage past bar + mako … Prefer one operator-config gap over
another harness counter"): C1 takes the caller half of the default-application plane — Omarchy's `xdg-open` — and finds
it diverges from the GLib half on a third of the host's types. Still open from the same proposal: screen-share runtime
(`xdph.conf`), clipboard, hypridle.

## Domain share

New or changed artifacts: one desktop-facing tool (`tools/mado-xdgmime.py`), one knowledge entry, two knowledge
corrections, three registry rows, one PROVINCE refinement (desktop-facing); one record gate change
(`quality/check-seat-reports.py`), two counters, two QUALITY criteria (lane-internal). Desktop-facing: 6 of 10.

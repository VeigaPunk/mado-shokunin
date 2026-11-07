# mado round 95 — claims declaration (FROZEN at the freeze commit; the L1 MadoR95 owns it)

Base: `master` at `4a2af6817024f6ed47084a5217c1825ae247f4fe` (round-94 closure tip). Dispatch-evidence commit
`497c6fcd372b817d8423dcd37ece08216012433c` carried the draft of this file (same two claims, draft predicates).
Lowest-axis duty: every owned axis scores 10 (round-94 SCORECARD), so the duty is a tie; stagnation nudge not claimed (a
capability entered at round 94). Sourced claim: C1 (rows S519–S523 opened by the L1 this round, S505 re-opened:
`.ufo/waves/round-95/receipts/sources-open-r95.txt`, including its append-only correction). Round-94 spot-check routed
defects: defect 3 → C2 (two of the five unguarded tools); defects 1, 2, 4 are not claims (reasons in
`corpus/lessons/round-95.md`); defect 5 (QUALITY 154) is applied to the caller sentence below. considerthese
`2026-11-06.md` proposal 4 ("widen desktop coverage") → C1.

Amendments folded in before any measurement (all from wave w1, all before the freeze; the draft is in `497c6fcd`):
C1 — the candidate is `c1c` (VT is binary: R95MCritic C1-F1, R95MReviewC1 F1, R95MProbeC1 F1, R95MMutC1 F1,
R95MExecCasesC1 1; the wrapped sum compares byte by byte and stops at the first difference: L1-F1, R95MReviewC1 F5,
R95MProbeC1 F2; a type string is read only if its entry wins: R95MProbeC1 F3; the parent walk is iterative: R95MReviewC1
F4; no database at all is answered: R95MReviewC1 F3; both depth limits are 4096, declared: R95MCritic C1-F3,
R95MReviewC1 F2, L1 bisection); each input is labelled by its own oracle run (R95MReviewC1 F6); `expect_refusal` cases
for the declared limits; the structural conjunct pins the sibling import shape and the module's attributes and adds an
audit-hook launcher (R95MCritic C1-F4); a measurement-time fresh seed and a memoriser control (C1-F5); the `real` class
is rebuilt by `update-mime-database` (C1-F6); each class kills a counted mutant (C1-F7, weakened: any kill, not a unique
one); the sibling-module forgery is a control. C2 — the panel holds the wave's green escapes and the critic's
drop-component pairs (R95MCritic C2-F1/F2, R95MMutC2); the kill-sets gain R95MMutC2's closing kills and two L1 kills;
a singleton minimum (R95MReviewC2 F1); at least two neutral edits per tool (C2-F3).

## C1 — coverage (new surface, capability): file bytes → MIME type as GLib sniffs them

Surface moved: the content step of GLib's type guess. Round 94 answered `g_content_type_guess (name, NULL, 0)`; no
lane tool reads the magic section of `mime.cache` or answers a guess given data (`git show 4a2af681:tools/mado-mimesniff.py`
→ absent).

Caller scope (QUALITY 154): the claim is what GLib 2.90.1 `g_content_type_guess (name-or-NULL, data, len, &uncertain)`
returns. Its caller on this host is GIO's `standard::content-type` (S522 `glocalfileinfo.c`:1337, :1340, :1373: a
sniff only after an uncertain name-only guess); `xdg-open` on Hyprland types files with `file(1)` instead
(R95MConnector §2.4) and is not claimed.

Tool `tools/mado-mimesniff.py` = frozen candidate `.ufo/waves/round-95/build/mado-mimesniff.c1c.py`, sha256
`4ef019c69ea8ae4147f83d1558683f012fb4aac0815d36770304717aaca6af24`; it loads round 94's `tools/mado-mimeglob.py`
(sha256 `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`, unchanged) from its own directory.

Frozen inputs (sha256):

| input | path | sha256 |
|---|---|---|
| cases (300 cases, 2863 inputs, 20 classes, min 9 per class; origin map inside) | `.ufo/waves/round-95/controls/mimesniff-cases-r95-frozen.json` | `ee815b4fca636640358366a2e9f4c252d74bb9626e0a45e1d2de3bcae14ea8a2` |
| mutants (94 counted, 5 equivalent/crash-shaped with arguments) | `.ufo/waves/round-95/controls/mimesniff-mutants-r95-frozen.json` | `0e45964a6a19982af55cafc5549d8eabcab9bd6ec77b17acc0ce6d3f8f44bf07` |
| oracle source | `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` | `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` |
| fresh generator (R95MExecCasesC1; `--seed --count --out`) | `.ufo/waves/round-95/controls/mimesniff-fresh-r95.py` | `15396113ad8f0198c56253d2f03f0e2ff05ca9fa15601ce042de8046f438b809` |
| host file list (4911 paths under /usr, R95MExecHostC1) | `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` | `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` |
| sibling-module ctypes forgery (R95MCritic Appendix A) | `.ufo/waves/round-95/controls/forgery-sibling-ctypes-r95.py` | `5cb0fbad4d366d8811b00519b4952f2f9cedc2aeda160dd530cf79100668f75c` |
| counter | `quality/counters/c1-r95-mimesniff.py` | `95b1657fe3dc6e928ed10a5a702a0c18e38dd0bba20862ada855c16ae2e4e593` |

Counter argv: `python3 -I quality/counters/c1-r95-mimesniff.py --repo . --rev <rev> --base-rev
4a2af6817024f6ed47084a5217c1825ae247f4fe --cases <cases> --expect-cases-sha256 ee815b4f… --mutants <mutants>
--expect-mutants-sha256 0e45964a… --oracle-src <oracle> --expect-oracle-sha256 99df35f8… --fresh-gen <gen>
--expect-fresh-gen-sha256 15396113… --host-files <list> --expect-host-files-sha256 9d5947a7… --expect-tool-sha256
4ef019c6… --expect-mimeglob-sha256 65f80a6c… --forgery <forgery> --expect-forgery-sha256 5cb0fbad… --fresh 120
--workers 28 --scratch-root DIR` (full digests above).

**PRED-C1-r95-v1** (the counter's docstring holds the same text): TARGET_MET iff, at `<rev>`, the tool is the frozen
candidate and mimeglob is round 94's bytes (`tool_pin=ok`), and (i) on every frozen case the tool's (type, uncertain)
equals the oracle's label for every input (an input labelled `["UNSUPPORTED", null]` — the oracle run on that input
alone crashes or hangs — and every input of a case marked `expect_refusal` require exit 3), and the per-input oracle
re-run equals the recorded label (else SETUP_ERROR); each of the 20 classes `zerosize fallback lltext order prio
multicache range mask nest bounds wrap desktop name1 name0 nameN subclass alias slash mode real` holds ≥ 6 cases, no case
carries another class, each class's cases make at least one counted mutant wrong (`class_kills=20/20`), and every `real`
case's `mime.cache` equals `update-mime-database` rebuilt from its own `packages/*.xml` (`real_rebuild=K/K`); (ii) on 120
fresh cases from the frozen generator, seeded at measurement from `os.urandom` (seed printed), the tool equals the live
oracle; (iii) on every readable file of the frozen host list, first 4096 bytes, data-only and with its own path as the
name, under the counter's HOME/XDG environment, the tool equals the live oracle; (iv) every one of the ≥ 40 counted
mutants makes at least one frozen case wrong (a crash is `crashed_not_killed`); (v) do-nothing, the round-94 name-only
answer, a naive sniff and the base revision each miss (i); a memoriser (frozen labels, do-nothing elsewhere) misses (ii);
the frozen forgery is rejected by (vi); (vi) `static_no_external_resolver=ok`: imports only `__future__ argparse
importlib.util json os struct sys tempfile`; no `eval exec compile __import__ getattr setattr delattr vars globals
locals breakpoint`; no `.__x__` attribute; no `os.system/popen/exec*/spawn*/posix_spawn*/fork*`; exactly one
`spec_from_file_location` whose location holds `__file__` and `"mado-mimeglob.py"`; the bound module used only for
`Unsupported oob Resolver xdgmime_dirs g_path_get_basename esc _LC_ALL _libc.setlocale`; and `audit_denials=0`: every
frozen, fresh and host run goes through the counter's audit-hook launcher (no open outside the run's scratch, Python
and, on the host leg, the host MIME dirs; no spawn but `/usr/{bin,sbin}` ldconfig/gcc/cc/ld/objdump; no socket; no
dlopen but libc), with `PATH` an empty directory.

Before → after: frozen cases answered as GLib does, base **0/300** (no tool) → **300/300**. Kill rule: any conjunct
false → TARGET_MISSED; never narrowed after data.

Pre-freeze controls (`.ufo/waves/round-95/receipts/c1-controls-prefreeze-r95.txt`, DRAFT runs of this counter on these
inputs, committed in the freeze): the frozen candidate `c1c`, the wave candidate `c1` and the intermediate `c1b`
(both must miss), and the forgery as a candidate (must miss through (vi)).

## C2 — operability: the selftest-strength gate guards two more lane tools

Round-94 spot-check routed defect 3: this claim lands `quality/selftest-kills/mado-mimeglob.json` (= frozen
`build/mado-mimeglob-kills.c2b.json`, 22 kills, sha256 `fab72dafd67d2bf6d056ed0a2d2a77fcad0a5c2d65b93babcb9539cb6e47a593`)
for `tools/mado-mimeglob.py` (19 checks) and `quality/selftest-kills/mado-portals.json` (= `build/mado-portals-kills.c2b.json`,
42 kills, `4c7fc2b3b5e47b6e1cd1541fa30eb8c971320538bb6b3246d4dde0243556c83d`) for `tools/mado-portals.py` (28 checks,
sha256 `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021`). The gate stays the round-93 frozen gate
(`2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b`); both tools unchanged. The gate's own selftest is not
guarded: `non_selftest_prefix` cuts its own source at a string at line 73 (lesson M95-1; R95MReviewC2 F5; routed).

Frozen inputs: panel `.ufo/waves/round-95/controls/selftest-panel-r95-frozen.json` (75 hand weakenings: R95MExecCounterC2
24, R95MMutC2 42 green escapes of the first drafts, R95MCritic 9 drop-component pairs; 6 neutral edits, 3 per tool)
`8c6dfdac1ddf5b2c95e9c8ac381f29101161da8b566dc8e5c9039763c74fb0f5`; control kill-sets (the first drafts)
`build/mado-mimeglob-kills.c2.json` `f4b80be6…c7`, `build/mado-portals-kills.c2.json` `64b3c10d…f4`; counter
`quality/counters/c2-r95-selftest-kills.py` `983d4cbcc0e0965d16e0e27a7d6a1ab44ac7fa98a4279a7ba60b9c3fcf5e873a`.

**PRED-C2-r95-v1** = PRED-C2-r94-v1 on the two tools above, plus: (iv) ≥ 2 neutral edits per tool; (vii) the first
drafts flag strictly fewer of the 75 hand weakenings than the frozen kill-sets; (viii) at least 36 of the 47 labels have
a singleton kill. The 11 labels without one: mimeglob `t01 simple suffix`, `t10 no match`, `t13 non-ASCII byte never
matches a suffix`, `t17 a bare * is inert`, `t19 unset HOME adds no user dir`; portals `default list falls to second
backend`, `default list first backend`, `star takes first sorted backend (UseIn first)`, `interface key wins`,
`interface key beats default none`, `gtk last resort`.

Before → after: hand weakenings of the two tools' selftests flagged by a lane instrument — before, no kill-set exists
(the do-nothing instrument flags **0/75**, and 0 of the 47 single-check neutralisations); after, **75/75** and **47/47**,
with the first drafts at 28/75.

Pre-freeze controls (`.ufo/waves/round-95/receipts/c2-controls-prefreeze-r95.txt`): frozen candidates DRAFT_TARGET_MET
75/75, 47/47, singletons 36/47; first drafts as candidates MISSED (28/75); R95MReviewC2's blanket forgery MISSED
(34/75, singletons 0/47); empty kill-sets MISSED (0/47, 0/75).

## Separability

C1 lands a new tool, entry and rows; C2 lands two kill-set JSON files. C1 is measured at its own commit (before C2); C2's
counter at the C1 commit must stop SETUP_ERROR (kill-sets absent); C1's counter at the C2 commit must still be
TARGET_MET. C2 does not guard the C1 tool. C1 reads `tools/mado-mimeglob.py`, which C2 guards without changing.

## Named limits (declared before data)

- C1: cache mode or no database (text database files refused); a matchlet chain or parent chain deeper than 4096
  refused (declared; GLib answers up to its stack limit); reads past the mapping or past the data refused (C undefined
  behaviour); data as passed; labels from glib2 2.90.1-1 / shared-mime-info 2.5.1-2; `class_kills` asks for any kill per
  class, not a unique one.
- C2: panel weakenings and closing kills come from the same wave (a design set; the first-draft control discriminates);
  11 labels without a singleton kill; the gate's own selftest, `tools/mado-mako.py`, `tools/mado-verify.sh` and
  `quality/check-receipt-presence.py` stay without kill-sets.

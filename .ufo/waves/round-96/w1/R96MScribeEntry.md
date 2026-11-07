# R96MScribeEntry — round 96 w1 report (mado)

Seat: `R96MScribeEntry` (scribe, leaf). Round 96 (hyaku run 15, attempt 1), wave w1.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`; base revision
`9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d` (`master`). Axes the round claims: coverage (C1, the
text MIME database's magic step) and operability (C2, a kill-set for `quality/check-receipt-
presence.py`). This seat wrote drafts only: no product code, no registry commit, no gate run, no
git/jj command, no network beyond the recorded fetches, no package transaction.

## 1. Deliverables (exact paths and digests)

| artifact | path (relative to the lane) | sha256 | lines |
|---|---|---|---|
| knowledge entry draft | `.ufo/waves/round-96/w1/knowledge-draft-mime-textdb-r96.md` | `e4657444034d6b9934c5c70bad36909e254bd1dff2b5deeec421f9b780f3ae6d` | 681 |
| registry rows draft | `.ufo/waves/round-96/w1/registry-rows-draft-r96.md` | `ee48f9e1cedf0acc0d5ea3c4b7f5a2c4ecafef196b5746c42fb7e84a4d8426c7` | 172 |
| SKILL/PROVINCE diff draft | `.ufo/waves/round-96/w1/skill-province-diff-draft-r96.md` | `7d20ead730e3171d14a48400a68d6b0951b2daad90cccbc3e36775b58701311a` | 63 |
| lesson draft | `.ufo/waves/round-96/w1/lesson-draft-r96.md` | `000a645416c47594b3e922f3811e199694b381c8f089affdc5d64770f292059c` | 112 |
| probe driver (evidence) | `.ufo/waves/round-96/w1/R96MScribeEntry-probe.py` | `38c8cb6e3fbc337b2ef696a8fa7a911a04ee4a4c2611903788b90494e85ea9fa` | - |
| probe output (evidence) | `.ufo/waves/round-96/w1/R96MScribeEntry-probe.out.txt` | `68b0909259864de49f0531709670367d4b5b4bb5be7b4b394d4314c5829f65e9` | - |
| host-DB parser (evidence) | `.ufo/waves/round-96/w1/R96MScribeEntry-hostdb.py` | `384a956af2470898fd51c83604d051f1c4d995699cf7695c6700e042413b3679` | - |
| host-DB output (evidence) | `.ufo/waves/round-96/w1/R96MScribeEntry-hostdb.out.txt` | `ca1ce36ce6861cf0a30d163efcf43d1f0c333b5463de0a23f1aea085181db4a2` | - |
| quote extractor (evidence) | `.ufo/waves/round-96/w1/R96MScribeEntry-quotes.py` | `54f14dcaf0c8b2660c148c5fb834d371d226a21d910210ca7575b53804aa62b7` | - |
| quote map (evidence) | `.ufo/waves/round-96/w1/R96MScribeEntry-quotes.out.txt` | `e0f5d4cfa2a3e196035bc16caab3ee37d8fc760874a1e8925033d54c943fe774` | - |

The six evidence copies are the scribe's own drivers/outputs, committed so the entry's §7/§8
citations resolve (round-95 precedent: `R95MScribeEntry-drv.py` etc.). They are not product code
and are not claimed as lane instruments.

## 2. What was produced

1. **The C1 entry draft** (681 lines) in the r95 shape: front matter (`source`, `verified-at`,
   `recheck`, `covers`), §1 question/scope, §2 rules with S-row anchors and quotes, §3 departures
   from the spec, §4 operator consequences, §5 the tool and its verdict map, §6 limits, §7 measured
   results, §8 located quotes, §9 frozen cases and pins. Every rule cites S524/S525/S505/S520/S521/
   S522 or an oracle-labelled probe row (P-ids). The 16 class names are written out in §9 (the
   declaration does not carry them; see D15).
2. **The registry draft**: exact 11-column cell text for S524 and S525; the six held rows'
   `used-by` old->new; a correction table against the receipt's line map; the full 80-row located
   quote map (mechanically extracted); fetch provenance and the rejected `ar01s03.html` probe.
3. **The SKILL/PROVINCE diff**: the exact `SKILL.md` row (8 content cells, escaped pipes, insert
   after `mado-r95-mimesniff` at `SKILL.md:886`), the round-96 PROVINCE refinement paragraph
   (matching the r94/r95 shape), and an optional inventory-table row with the recommendation that the
   paragraph is the consistent form (the r92/r94/r95 tools have no table rows).
4. **The lesson draft**: one mined mistake (M96-1, class number-drift, QUALITY 6), the Gate table
   (three admits and six rejections - the declaration's model sentences, the ar01s03 page, the receipt's page-line cells, a conditional S525 fold and one correction in place - each with a reason and a flip), the routed
   wave findings table, the round-95 spot-check dispositions, the Census block and the cross-domain
   evidence.

### S-row markers

No `S<pending>` markers remain: the L1 confirmed `S524` (xdgmimemagic.c) and `S525` (spec §2.5) in
the 11:39Z message and the receipt carries both headings, so the entry and the registry draft cite
those ids. If the L1 folds S525's §2.5 scope into S523 (the same locator and digest), replacing
`S525` by `S523` moves no line; the entry says so in its §8 preamble.

### `<measured>` placeholders (the cells this seat could not fill)

The C1 candidate did not exist while these drafts were written (`build/` was empty; the host seat's
§2 records the same); it appeared at 11:48Z as a wave draft, and no frozen measurement exists to
cite at 11:52Z (see the late-wave note in §4). The L1 fills these from
`.ufo/waves/round-96/receipts/c1-measured-r96.txt`:

| cell (entry location) | fills with |
|---|---|
| `<measured:tool-sha>` (front matter, §9) | sha256 of `tools/mado-mimetext.py` at the C1 measured rev |
| `<measured:cases>` (front matter, §7.4) | frozen case count |
| `<measured:case-inputs>` (front matter) | total inputs across the frozen cases |
| `<measured:per-class>` (§7.4) | the per-class census (16 classes, >= 8 each) |
| `<measured:fresh>` (front matter, §7.4) | fresh inputs correct / total (>= 120) |
| `<measured:host>` (front matter, §7.4) | candidate host-leg correct / total (>= 1500; the list is 4911 paths) |
| `<measured:mutants>` (front matter, §7.4) | mutants killed / total |
| `<measured:controls>` (§7.4) | the four controls' scores |
| `<measured:selftest>` (§7.4) | `checks=N failed=0` (N >= 18) |
| `<measured:tool-pin>` (§7.4) | `tool_pin=ok` at the measured rev |
| `<measured:cases-sha>` (§9) | sha256 of `magictext-cases-r96-frozen.json` |
| `<measured:mutants-sha>` (§9) | sha256 of `magictext-mutants-r96-frozen.json` |
| `<measured:fresh-sha>` (§9) | sha256 of `magictext-fresh-r96.py` |
| `<measured:counter-sha>` (§9) | sha256 of `quality/counters/c1-r96-magictext.py` |
| `<measured:census-end>` (lesson, Census) | the census result after the registry commit |

Every other number in the entry is measured by this seat (§3) or carried by an S-row.

## 3. Verification this seat performed (read-only; not the claim's measurement)

Commands run, all read-only, in the order used:

1. **Fetch digests.** `sha256sum .ufo/waves/round-96/fetch/*` -> `fcb1eafe...ce742` (xdgmimemagic.c,
   18289 B), `afb1c1c1...82410` (xdgmime.c, 23417 B), `e00fa00e...c61e` (smi-ar01s02.html, 59208 B):
   3/3 equal to `sources-open-r96.txt`. The same three r95 copies used before 11:39Z hash to the same
   values, which is why the entry's earlier citations were byte-identical.
2. **Pinned controls.** `sha256sum` of `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c`
   (`99df35f8...124a`), `.../mimesniff-host-files-r95.txt` (`9d5947a7...ba87`, 4911 lines),
   `.../mimesniff-cases-r95-frozen.json` (`ee815b4f...a8a2`), `.../mimesniff-mutants-r95-frozen.json`
   (`0e45964a...bf07`), `tools/mado-mimeglob.py` (`65f80a6c...2453`), `tools/mado-mimesniff.py`
   (`4ef019c6...af24`), `quality/check-receipt-presence.py` (`38a2ea60...47ca`), and
   `quality/check-selftest-strength.py` (`2d6f1219...a61b`).
3. **Oracle probes.** `cc -O0 -o $S/oracle .ufo/waves/round-95/controls/mimesniff-oracle-r95.c
   $(pkg-config --cflags --libs gio-2.0)`, then `$S/oracle` over 58 fixture roots / 66 inputs with
   `env -i LC_ALL=C HOME=... XDG_DATA_HOME=... XDG_DATA_DIRS=...`. Output: 66 labels, kept as
   `R96MScribeEntry-probe.out.txt`; the counts per rule are in the entry §7.1 table. Three
   authoring errors were corrected before any label was used (a missing `cache` keyword, E4's child
   offset, and a stale copy of the output after adding F3/G4).
4. **Host text database.** A read-only stdlib parse of `/usr/share/mime/magic`
   (`R96MScribeEntry-hostdb.py`): 47524 B, sha256 `2942f4ad...a35c`, 689 sections, 1743 matchlets
   (1282 at indent 0), 0 parse errors, priorities 5..90 with 43 sections >= 80 and none at 0, word
   sizes 1:1733 / 2:4 / 4:6, 43 masks, 259 ranges > 1, max range 18722, max extent 18730, max indent
   4, 655 distinct types, 27 types listed more than once, longest type 56 B. The 689/1282 counts
   equal the round-95 cache counts; 461 deeper matchlets are the cache's children.
5. **Quotes.** `R96MScribeEntry-quotes.py` extracts every quote from the committed fetch bytes by
   line range, whitespace-collapses it and prints its word count: 80 quotes, all <= 25 words, no
   hand-typed quote cell in either artifact.
6. **Declaration checks.** The oracle pin's length (63 -> 64; now `test` rc 0 after the L1's fix);
   the host-list pin (12 chars, `9d5947a7ba87`, a head+tail splice of the true digest); the missing
   `--expect-tool-sha256`/`--expect-mimeglob-sha256` (only the prose at line 49 mentions a tool
   pin); the 16-class list absent (`grep -c` = 0); no `--forgery` argument (`grep -o
   'expect-[a-z-]*sha256'` lists none). The receipt's S524/S525 line cells were diffed against
   `nl -ba` of the fetched files.

## 4. Findings (defects found before the freeze)

Status: **fixed** = the L1 corrected it (11:39Z message); **open** = still true at 11:47Z.

| # | finding | evidence | status |
|---|---|---|---|
| D1 | C1 counting command pinned a 63-hex oracle digest (`...f8e6984a...`) instead of the 64-hex file digest | `grep -o` on the declaration line, its match length read by `awk` = 63 vs `sha256sum` 64 | fixed (L1; `test` rc 0 now) |
| D2 | C1 command pins `--expect-host-list-sha256 9d5947a7ba87`: 12 chars, first 8 + last 4 spliced, neither full nor a true prefix | `sha256sum` = `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` | **open** |
| D3 | C1 command omits `--expect-tool-sha256` and `--expect-mimeglob-sha256`, though the predicate's `tool_pin=ok` conjunct and the pinned sibling require them | declaration lines 49 and 60-71 | **open** |
| D4 | the receipt's S524 line cells: memcmp at 815 (true 814), mask at 400-419 (true 420), word/length check at 421-450 (true 476), word-size set "1\|2\|4" (true 0/1/2/4) | `nl -ba` + probes D11/D14 | fixed (receipt updated; quote map carries the true lines) |
| D5 | the receipt's S525 page-line cells: 407-410 (true 403), 429-433 (true 421-423), 435-439 (true 426-427), 441-446 (true 429-430); quotes correct | mechanical extraction of the fetched HTML | fixed (receipt updated) |
| D6 | `.ufo/waves/round-96/fetch/` was empty although the receipt recorded the fetches; the entry's citations initially pointed at the r95 copies | `find .ufo/waves/round-96 -type f` at 11:30 | fixed (L1 committed the three files at 11:39Z; digests equal) |
| D7 | the contract's "word size (1\|2\|4 only)" is narrower than the C: `~0` is accepted and compared as 1 | `xdgmimemagic.c`:440-443; probe D11 -> `application/x-w0 0` | fixed in the receipt as a model fact; entry states the C |
| D8 | "a section is kept only if it ends with at least one parsed matchlet" is not what the state machine does: it inserts a section on `SECTION` or `EOF`-with-type even with zero matchlets (inert, unobservable) | `xdgmimemagic.c`:772-778; probe G3/G4 | **open** (receipt row still says it; entry states the precise rule) |
| D9 | text mode has no `priority > 0` gate, so a priority-0 section answers (`application/x-zero 0`), unlike cache mode | `xdgmime.c`:535-538 vs `xdgmimecache.c`:784; probe C1 | fixed as a model fact (receipt); entry carries it |
| D10 | an indent jump (0 then 2) or a first matchlet at indent 1 makes a section unmatchable; the contract's "the deeper chain is tested" does not name the jump | probes E6/E7; R96MCritic F5 | entry carries it; the case set should freeze the contrast pair |
| D11 | an empty type (`[90:]`) is accepted and answered as `""` 0; the tool must print an empty type token | probe F1 | **open** as a case-class hazard (entry notes it) |
| D12 | bytes after `]` are discarded with the line, but a NUL after `]` ends the read and the remainder is parsed (and errors) | probes F3, B6; R96MCritic F9 | entry states both |
| D13 | the host leg rooted at `/usr/share/mime` is cache mode: the tool would answer exit 3 while the oracle answers cache labels | R96MCritic F1; `xdgmime.c`:137-153 | **open** (predicate/command need the text-root construction) |
| D14 | the do-nothing control cannot be 0 over `none`-mode cases (the r95 tool answers them correctly) | R96MCritic F6 (measured); the entry's `mode` class includes `none` cases | **open** (declaration text) |
| D15 | the 16-class list does not appear in the declaration; the predicate refers to a "declared CLASSES" that is not there | `grep -c` = 0; R96MCritic F7 | **open**; the entry §9 carries the list |
| D16 | the C1 command has no `--forgery` pin, so the forgery conjunct is unmeasured | `grep -o 'expect-[a-z-]*sha256'`; R96MCritic F8 | **open** |

Late wave state (11:47-11:49Z, after these drafts were written): the in-wave candidate
`.ufo/waves/round-96/build/mado-mimetext.c1.py` (44244 B) and the probe seat's
`controls/probes-r96.py` / `R96MProbeC1-answers.json` appeared. The entry's §5 was then checked
against the candidate's own argparse/output spellings (read-only `grep`, no run): the `--name`,
`--names-from-files`, `--data-home(-unset)`, `--data-dirs(-unset)`, `--home(-unset)`, `--json`,
`--selftest` options and the three line prefixes match the contract, and the refusal line is
`MADO_MIMETEXT: UNSUPPORTED <reason>` (a reason token, not the literal `cache-mode`), which is the
one wording the entry and the SKILL row were changed to match. The `<measured>` cells stay
placeholders: the draft is not the frozen candidate and no frozen measurement exists at 11:52Z.

No conflicting *claims* among seats were found; the only disagreements were numeric, listed above,
and D1/D4/D5/D6 are now consistent. The one prose conflict to record verbatim is the receipt's row

    | section kept only if a matchlet parsed | 749-782 | `_xdg_mime_magic_matchlet_mirror (match->matchlet);` |

against `xdgmimemagic.c`:772-778, which inserts the section on `SECTION` or `EOF`-with-type
regardless of matchlet count (D8). The tool's answer surface is unaffected (an empty section can
never match); the wording is what needs the fix.

## 5. Cross-seat consistency

- `R96MConnector` §5.1 names five C behaviours (whole-section drop, parse-time swap of value and
  mask, equal-priority file order, child-failure fallthrough, short-buffer abort) - all five are
  rows in the entry's §2, measured by probes B1/B3, D9/D10, C3, E2/E3 and D5/D6.
- `R96MCritic` F4/F5/F9/F10 independently measured `~0`, the indent jump, the zero-length value,
  `+0`, junk-after-`]` and the 814 line; this seat's probes D11, E6/E7, D15, D4, F3 and the quote map
  agree on every one. F1/F2/F3/F6/F7/F8 are recorded as D13/D2/D3/D14/D15/D16 above.
- `R96MExecHostC1` §1-§2 supplies the measured host leg (4911/4911 oracle rows, 0 ERR; 78/62
  distinct labels; 242 + 276 `application/octet-stream 1`) and the eight-file text-DB recipe; the
  entry cites both and does not duplicate the measurement.

## 6. Touched surfaces and out-of-scope items

- **Written by this seat:** the five named files plus the six evidence copies, all under
  `.ufo/waves/round-96/w1/`; scratch under
  `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r96/R96MScribeEntry`, removed on exit after the
  outputs were copied into w1. Nothing else in the lane or the fleet was written; no receipt,
  control, build, tool, quality, corpus or git/jj object was touched.
- **Out of scope (not done, deliberately):** the candidate (`tools/mado-mimetext.py`), the case
  file, mutants, fresh generator, counter, kill-sets, the C2 artifacts, the registry commit, the
  entry commit, the SKILL/PROVINCE edit, the census run, any gate run. This seat ran no lane gate
  and no counter; the drafts are inputs to the L1's gates.
- **Tool installs:** none. No pacman/uv/npx, no network fetch, no host-service or sysctl change. The
  only compilation is the round-95 oracle into scratch (allowed by contract 3) and the only host
  reads are the eight `/usr/share/mime` files and the pinned control files.
- **Markup note:** the four prose drafts are UTF-8 and use the corpus's existing characters
  (`§`, `→`, `≥`, em dash) exactly as the r94/r95 entries do; the six Python evidence files
  are pure ASCII (checked byte-wise, 0 non-ASCII bytes). If the L1 holds a strict ASCII rule for
  prose, the substitution is mechanical (`§` -> `sec.`) and moves no rule.

## 7. What the L1 should verify before freezing

1. Fill the 15 `<measured>` cells from `c1-measured-r96.txt`; the entry is a draft until then.
2. Land the open declaration/receipt defects (D2, D3, D8, D11, D13-D16) or state them as limits.
3. Register S524/S525 (or fold S525 into S523) and append `used-by` to S505/S519/S520/S521/S522/
   S523 exactly as the registry draft §2 prints.
4. Insert the SKILL row after `SKILL.md:886` and the PROVINCE paragraph after `PROVINCE.md:561`;
   decide whether the optional inventory row is wanted.
5. Decide the entry's index row and frontier line in `corpus/README.md` (the draft does not touch
   them).
6. If the frozen candidate's output spellings differ from the draft's (an empty type, the `--json` shape), re-check
   the entry's §5 against the tool: `MADO_MIMETEXT:` lines are the scored surface, `--json` is not
   specified by the contract.

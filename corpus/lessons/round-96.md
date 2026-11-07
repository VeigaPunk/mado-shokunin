# mado round 96 — lessons

Round 96, hyaku run 15, attempt 1 (`MadoR96`). Two frozen claims from
`.ufo/waves/round-96/claims-declaration-r96.md`: C1 coverage, new surface (`tools/mado-mimetext.py`: the MIME
type GLib 2.90.1 guesses when the text `mime/magic` database is the only database) and C2 operability (a kill-set
for `quality/check-receipt-presence.py` under the unchanged round-93 selftest-strength gate). This file is the
scribe's DRAFT for the L1 to land after the freeze; every `<measured:...>` cell is filled from
`.ufo/waves/round-96/receipts/c1-measured-r96.txt` and the round's C2 receipt.

## Mistakes

**M96-1 — the C1 counting command published a digest that is not the control file's digest.**
Class: number-drift. The declaration's C1 counting command carried
`--expect-oracle-sha256 99df35f8b3fd7005f30789f8e6984a1bbceaff8dc6c1d326f0132eb7b4d124a` — 63 hex
characters, one `8` lost in the middle — while the pinned oracle
`.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` hashes to
`99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` (64). The shared contract in the seat
prompts and the C1 case schema's `oracle_src_sha256` carried the right value, so three copies of the round
disagreed and only the command line was wrong. Evidence: `.ufo/waves/round-96/claims-declaration-r96.md`
(C1 counting command; the string measured at 63 characters by `grep -o ... | awk '{print length($2)}'`) vs
`sha256sum .ufo/waves/round-95/controls/mimesniff-oracle-r95.c` (64 characters); the host seat independently
re-measured the same 64-character value (`.ufo/waves/round-96/receipts/host-leg-r96.txt` §2 note). Captured-by:
QUALITY 6 (a pinned value is published with its re-derivation command; a shortened hash must be a true suffix,
and corrections preserve old and new values) — the pin is also the counter's first setup check, so the defect
would have surfaced as SETUP_ERROR, not as a verdict. Fix: both the declaration and the command line now carry
the measured 64-character digest (L1 `MadoR96`, 2026-11-07 11:39Z); the old value is kept in this row.
Shown able to fail: `test "$(grep -o '--expect-oracle-sha256 [0-9a-f]*' .ufo/waves/round-96/claims-declaration-r96.md | awk '{print $2}')" = "$(sha256sum .ufo/waves/round-95/controls/mimesniff-oracle-r95.c | awk '{print $1}')"`
now exits 0 on the corrected declaration; on the draft it exited 1 (63 vs 64 characters, measured 11:41Z before
the L1's fix, and the 63-character string is preserved in this row as the old value). Criterion: QUALITY 6.

**M96-2 — the L1's shared contract turned "a `mime.cache` exists" into "cache mode", and five frozen cases carried refusal labels the library contradicts.**
Class: proxy-condition substitution. The shared contract said "A reachable `mime.cache` means cache mode" and "a case
that holds a `mime.cache` is a cache-mode refusal case (labels `["UNSUPPORTED",null]`)". GLib loads a cache only when
it opens, is at least 40 bytes and carries version 1.1 or 1.2 (`xdgmimecache.c:107-163`); a 16-byte `JUNKNOTACACHE000`
is ignored and the directory stays in text mode. The case seat followed the contract and labelled `mode-06` (plus four
other `mode` cases) `UNSUPPORTED`, while the compiled oracle answers `app/x-md6` / `app/x-md6g` — so the honest tool
was scored `wrong` and a tool that refuses too eagerly would have been scored `right`.
Evidence: my scorer, `.ufo/waves/round-96/controls/magictext-cases-r96.json` at sha `df130793…` (case
`mode-06-junk-cache-declared-refusal`), the oracle run in this round's L1 scratch, R96MCritic F1/F7 and
R96MExecToolC1's independent finding. Captured-by: none of the L1's own checks — the contract sentence and the probe's
rule were the same misreading; the wave's independent oracle runs caught it. Fix: the frozen contract and the probe
now use the library's validity test (40 bytes, version 1.1/1.2), `mode-06` is oracle-labelled (`app/x-md6`,
`app/x-md6g`), the five refusal cases hold loadable caches and say so in their ids, and the counter refuses a sentinel
whose fixture is text mode (SETUP_ERROR). Shown able to fail: the relabelled case scores the tool `ok`, the old label
scores it `wrong`; the frozen set grew 265 → 284 cases and the tool answers 284/284. Criterion: `QUALITY.md` 166.


## Gate

### Registry rows (opened 2026-11-07 by the L1 `MadoR96`; `.ufo/waves/round-96/receipts/sources-open-r96.txt`)

| id | locator | access | located quote | line |
|---|---|---|---|---|
| S524 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/xdgmimemagic.c (fcb1eafe...ce742, 18289 B), HTTP 200, two fetches | 2026-11-07 | `if (memcmp ("MIME-Magic\0\n", header, 12) == 0)` | xdgmimemagic.c 814 |
| S525 | https://specifications.freedesktop.org/shared-mime-info/latest/ar01s02.html (e00fa00e...c61e, 59208 B), HTTP 200, two fetches; same URL as S523 under a new scope | 2026-11-07 | `The file starts with the magic string "MIME-Magic\0\n".` | ar01s02.html 387 |

Every quote is <= 25 words; the full located map is
`.ufo/waves/round-96/w1/registry-rows-draft-r96.md` §4 (80 rows, mechanically extracted by
`R96MScribeEntry-quotes.py`). S525 raises the expected W04 duplicate-url warning.

### Rows touched

S505, S519, S520, S521, S522, S523: `used-by` only, each appended with
`corpus/knowledge/mime-textdb-magic-r96.md` (old -> new in the registry draft §2). No anchor, digest or scope
cell of a held row moves. Three new file scopes were opened on the round's own fetches (S524 new file; S525
new scope; S505 re-opened for the text path).

### Candidates considered (round 96) — every gate decision of this draft

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/mime-textdb-magic-r96.md` | **admit** | every rule cites S524/S525/S505/S520/S521/S522 or an oracle-labelled probe row; the draft's `<measured:...>` cells are placeholders, so admission is conditional on the C1 receipt's legs being exact | a GLib tag that changes xdgmimemagic.c or xdgmime.c |
| S524, S525 | **admit** | opened twice by the L1 with HTTP 200 and identical digests; quotes located and <= 25 words | a newer GLib/spec pin |
| SKILL.md tool row + PROVINCE refinement paragraph for `tools/mado-mimetext.py` | **admit** | exact text in the existing shapes (`.ufo/waves/round-96/w1/skill-province-diff-draft-r96.md`); no new write surface (reads `mime/magic` and the named FILEs only) | a change to the tool's CLI |
| `ar01s03.html` (probed HTTP 200, 7048 B) | **reject** | the page holds no `MIME-Magic` text; no separate scope (§2.5 already held as S525) | a page revision that gains the format text |
| the contract's "word size (1\|2\|4 only)" | **reject as a model fact** | the C accepts `~0` (word size 0, compared as 1): `xdgmimemagic.c`:440-443; probe D11 answers `application/x-w0 0`. The entry states the C's set; a frozen `word` case should carry `~0` | an oracle that rejects `~0` |
| the contract's "a section is kept only if it ends with at least one parsed matchlet" | **reject as a model fact** | the state machine inserts the section on `SECTION` or `EOF`-with-type even with zero matchlets (`:772-778`); such a section can never match, so the error is invisible to the oracle. The entry states the precise rule | a case that could observe an empty section |
| the contract's silent omission of text-mode priority 0 | **reject as a model fact** (admit the case) | text mode has no `priority > 0` gate (`xdgmime.c`:535-538), so `[0:type]` answers (`application/x-zero 0`, probe C1); cache mode discards it (`xdgmimecache.c`:784, S519) | a GLib change that adds the gate |
| S525 if the L1 folds its scope into S523 | **reject (conditional)** | the entry's §8 table otherwise stands; replacing `S525` by `S523` moves no line (the same page, same digest) | the L1's row decision |
| the receipt's page-line cells for S525 (407-410, 429-433, 435-439, 441-446) | **reject** (corrected in place) | the quotes are right, the line numbers are not: 403, 421-423, 426-427, 429-430, 443-446 | none |

### Wave findings routed to the L1 before the freeze

These are this wave's falsifier findings against the declaration's C1 command and model; the scribe
re-checked the text ones against the committed bytes (marked *verified*) and cites the seat for the
measurements it did not rerun.

| finding | what the bytes say | fix the L1 should land before freezing |
|---|---|---|
| R96MCritic F1 | `--host-mime-root /usr/share/mime` reaches the host's loadable `mime.cache`, so the tool answers exit 3 while the oracle answers cache labels; the host leg needs a cache-free copy of the eight text files | state and pin the text-root construction in the predicate/command; print `host_root=text files=8` |
| R96MCritic F2 (verified) | the declaration pins `--expect-host-list-sha256 9d5947a7ba87` (12 chars, a head+tail splice); the file is `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` | paste the full digest (or a prefix with an ellipsis, full value in the freeze block) |
| R96MCritic F3 (verified) | the C1 command passes neither `--expect-tool-sha256` nor `--expect-mimeglob-sha256`, so the predicate's `tool_pin=ok` conjunct cannot be established | add both (`mado-mimeglob.py` = `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`) |
| R96MCritic F4 / F9 (verified here too) | `~0`, a zero-length value, `+0`, junk after `]` and EOF without a newline are C behaviour, measured by the oracle (this draft's probes D11, D15, D4, F3, G4) | put each in the frozen set (`word`, `value`, `range`, `sect`) |
| R96MCritic F5 (verified here too) | an indent jump (0 then 2) and a first matchlet at indent 1 make the section unmatchable (probes E6, E7) | freeze the contrast pair in `indent` |
| R96MCritic F6 | the do-nothing control (the r95 tool) answers `none`-mode cases correctly, so "0 over the frozen cases" is false unless restricted to `db_mode == "text"` | restrict the control sentence, or score it as `do_nothing_none=K` |
| R96MCritic F7 (verified) | the declaration's C1 section does not contain the 16 class names (`grep -c` = 0); only the dispatch context has them | hardcode the tuple in the predicate/freeze block (the draft entry's §9 carries the list) |
| R96MCritic F8 (verified) | the command has no `--forgery`/`--expect-forgery-sha256`, so the forgery conjunct is unmeasured | freeze a forgery and pass it with its sha |
| R96MCritic F10 (verified) | the S524 headline quote is at `xdgmimemagic.c:814`, not 815 | fix the located line |
| R96MConnector §5.1 | five independent C readings (whole-section drop, parse-time swap of value and mask, tie order, child-failure fallthrough, short-buffer abort) agree with this draft's §2 | none; keep the entry's §2 rows as the reference |
| R96MExecHostC1 §2 | the oracle answered 4911/4911 host paths (0 ERR) in text mode: 78 distinct name-leg labels, 62 null-leg; uncertain rows exist (242 + 276 octet-stream 1) | the candidate's host leg is still `<measured:host>`; use these as the expected-label population |

### Spot-check (round 95, `corpus/lessons/round-95-verifier-spotcheck.md`)

- Routed defect 1 (`tools/mado-mime.py` HOME): not touched (its kill-set pin couples the change).
- Routed defect 2 (mimeglob docstring citation): not touched; the correct line stays recorded in round 95.
- Routed defect 3 (kill-sets for unguarded tools): C2 closes `quality/check-receipt-presence.py` this round;
  `tools/mado-mako.py` and `tools/mado-verify.sh` stay unguarded with the structural reason.
- Routed defect 4 (QUALITY 158 instrument): not addressed; the fetch receipt now records status and
  `url_effective` for every row, which is the practice QUALITY 164 made standing.
- Routed defect 5 (QUALITY 154 before the freeze): the declaration's caller sentence cites S522 and keeps
  `xdg-open`'s `file(1)` route outside.

## Census

- Start: `.ufo/waves/round-96/receipts/census-start-r96.txt` — `mado ok`, rc 0, 458 rows at the base.
- After the two new rows: 460 rows (S524, S525; tier A +2), with the expected W04 warning for S525 against
  S523. `<measured:census-end>` (the L1's `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
  after the registry commit).
- Row count is a navigation fact, not a behavioural verdict.

## Cross-domain evidence

GLib xdgmime's text reader (`xdgmimemagic.c`, `xdgmime.c`) and the GIO caller (`glocalfileinfo.c`),
GNOME/GLib; the freedesktop.org shared-mime-info format (spec §2.5 at the S523 locator) and its writer
`update-mime-database`, whose ALPM hook is tsukuroi's ground
(`tsukuroi-shokunin/corpus/knowledge/pacman-hook-order-r38.md:53,97`); `file(1)`/libmagic is revenger's
ground (their S176/S190 rows) and is **not** this surface — the `MIME-Magic` header and the
`mime/magic` file format are shared-mime-info's, not `magic(5)`'s (R96MConnector §1). This round's host
evidence is glib2 2.90.1-1 and shared-mime-info 2.5.1-2.

# AttackRubricGaming — round 17 wave 2 (FALSIFY)

Target: rubric V (C2) as implemented in `.ufo/waves/round-17/measure.py` at
lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (blob sha256
`4023124fa40931f630197920e2534f468dc2b1cacfe010826b52032db846466b`, same bytes as the
working tree). The question was whether a metadata-only edit can still raise V
without new sourced knowledge, given the tightened rules: T2 exact surface line,
T3 pinned legacy, T4 upstream relevance keywords, T5 facet floor.

**Verdict: the attack succeeded. Three separate metadata-only paths raise V from
4/6 to 5/6, and two of them together reach 6/6. No source was fetched for any of
them. Each passes `sources-census.sh validate` with output identical to the
baseline (rc 0, the same three pre-existing W04 lines, `ok`).**

The attack failed in one narrow case. Using only the edits that SOURCES.md allows
in place (`status`, `recheck`, `used-by`), you cannot reach P3 or P5: no existing
row of kind docs/spec/code with an https URL has a P3 or P5 keyword in its source
or scope cell. The only row that mentions a keyword at all is S059, and the
mention is in its anchor or teaches cell, not in source or scope; S059 also has
no https URL. Inside that edit class, T4 holds.

## Method

- I cloned the lane with `git clone --no-hardlinks` into
  `/tmp/ragame/mado-shokunin`, checked out `988b858`, and made attack commits
  there. Lane files were never mutated.
- V was measured by the clone's own copy of `measure.py`. Its bytes are unchanged
  in every attack commit, and it reads committed bytes via `REPO = parents[3]`.
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-20 /tmp/ragame/mado-shokunin/`.
  This is a read-only run against the clone's lane directory.

| rev (clone) | edit | V count | P3 | P5 | rejected | u_routes | census |
|---|---|---|---|---|---|---|---|
| 988b858 | baseline | 4 | — | — | [] | 7 | rc 0, 3×W04, ok |
| de35fbc (E1) | +1 Registry row, +1 filler entry | **5** | launcher-route-x.md [S071] | — | [] | 7 | rc 0, same as baseline |
| 3273d5d (E1+E2) | +1 HTML-comment row, +1 filler entry | **6** | launcher-route-x.md [S071] | theme-route-x.md [S062] | [] | 7 | rc 0, same as baseline |
| 4ae83f8 (E3, from 988b858) | in-place scope edit on S029, +1 filler entry | **5** | — | theme-route-y.md [S029] | [] | 7 | rc 0, same as baseline |

Each commit's size is 25 insertions, or 25 insertions and 1 deletion. The entry
files are 24 lines: `source: S0nn`, `surface: P<n>`, a title, and the four
required headings. Each heading has three lines of `- filler line …`, and
`[UNK]` appears in `## Unexercised behavior`. No entry body cites anything.

## Counterexamples

### E1 — fabricated in-Registry row (attacks T4; T2 and T5 do not apply)

New row S071: `walker README — https://github.com/abenz1267/walker/blob/master/README.md | docs | A | walker launcher | §1 (never fetched) | filler teaches text | mined | 2026-10-19 | on-release | corpus/knowledge/launcher-route-x.md |`.

- `mined_a()` checks only the cell values: status `mined`, tier `A`, and the
  entry path present in used-by.
- The T4 `upstream` test checks only these three things:
  - kind is in docs/spec/code;
  - `'https://'` appears in the source cell;
  - a keyword substring appears in source + scope.
- Nothing ties the row to fetched bytes. Real upstream rows such as S063–S069
  carry `sha256 …` in the anchor cell. measure.py does not require even that
  shape: the fabricated anchor `§1 (never fetched)` passes.
- No raw fetch receipts are committed under `.ufo/waves/round-17/`, so the
  revision cannot verify any hash, real or fake.
- Census checks shape, enums, dates, duplicates and used-by existence only (E01–E12).

### E2 — shadow row outside the Registry overriding a rejected row (attacks the registry's single authority)

Appended at the end of SOURCES.md:

```
<!-- | S062 | Linux Junkies — Configure Alacritty for Daily Use — https://linuxjunkies.org/guides/configure-alacritty | docs | A | alacritty theme import | §1 (never fetched) | filler teaches text | mined | 2026-10-19 | on-release | corpus/knowledge/theme-route-x.md | -->
```

- **Parser divergence.** measure.py builds `registry` from any line in the whole
  file that splits into 13 `|` cells with `cells[1]` matching `S\d{3,}`. It does
  not look at sections, does not require a leading `|`, and keeps the *last*
  duplicate id (`registry[cells[1]] = cells`).
- **What wins.** The genuine Registry row S062 stays `community | C | … | rejected`,
  and that is the row that renders. But measure counts the shadow as a mined
  tier-A docs row. The HTML comment does not render.
- **Why census misses it.** Census parses rows only inside `## Registry` and only
  when the line matches `^ {0,3}\|`. Its E12 ("row outside Registry") also
  requires a leading `|`. A line starting with `<!-- ` never matches, so census
  raises neither E12 nor E03 (duplicate id).
- **Result.** The same id now has two authorities that disagree. A community
  blog that was rejected credits P5 through the free-text scope word "theme".

### E3 — in-place scope keyword injection on a genuine mined row (attacks T4 relevance)

S029 (`Hyprland Wiki Configuring Start — https://wiki.hypr.land/Configuring/Start/`,
docs A mined) had its scope cell changed from
`Current Lua config path and language status` to `…; theme sourcing`, and
`corpus/knowledge/theme-route-y.md` was appended to its used-by.

- The SOURCES.md header says only `status`, `recheck` and `used-by` may change in
  place, but measure.py does not enforce that rule.
- Relevance is a substring test on author-written free text, so one word in the
  scope cell moves a Hyprland-config page into P5.
- The substring test is also loose in other ways. `hypr.land` makes every wiki
  page, including the hypridle and hyprlock pages S063 and S064, a P1 upstream.
  `foot` matches "footer" or "footnote". `idle` matches any mention of idle.

### T5 facet floor — filler passes

`FACET_MIN_LINES = 3` counts non-blank lines. `- filler line one/two/three` meets
it in all four sections, and `[UNK]` can be any substring in the last section.
None of the attack entries were rejected.

### T2 and T3 — attack failed

- **T2:** `surface:` must fullmatch `surface: (P[1-6])`. I used the exact form,
  so T2 cannot block this vector, and I found no bypass of T2 itself.
- **T3:** legacy credit needs `(path, U)` in the three pinned pairs, and it maps
  only to P1 or P2, which are already covered. It cannot add a province.

## Impacted axes

- **C2 / V:** inflatable from 4/6 to 6/6 with zero fetches. The tightened rubric
  measures declared registry metadata, not sourced knowledge.
- **Provenance:**
  - E2 creates a duplicate authority: the rendered registry says rejected, the
    counter says mined A.
  - E1 and E3 create false provenance: a URL that was never fetched, or a real
    URL credited to a province it does not teach.
- **No regression on the harm watches:** `u_routes` stays at 7 and `rejected`
  stays `[]` in every attack commit. C1 and C3 are untouched.
- **Not falsified by this attack:** the HEAD measurement V = 4/6 (P1, P2, P4,
  P6) is genuinely computed by the published rules. Whether the P4 and P6
  *content* is true is outside this item.

## Smallest safe corrections

These run in order of cost. E1 cannot be closed by the counter alone.

1. **Kill E2, mechanical.** In measure.py:
   - parse registry rows only inside `## Registry` and only from lines matching
     `^ {0,3}\|` (mirror the census parser);
   - on any duplicate id, exit non-zero instead of letting the last row win.
   - In census, raise E12 for *any* line containing an `S\d{3,}` row shape outside
     the Registry, not only lines starting with `|`.
2. **Kill E3, mechanical.** Take a pinned base revision: the round base, or
   `27cd06f` as T3 already uses. For any counted row present at that base,
   require the id, source, kind, tier, scope and anchor cells to be
   byte-identical to the base; only status, recheck and used-by may differ. This
   enforces SOURCES.md's own in-place rule. Replace substring keywords with
   word-boundary tokens matched on the URL host/path. At minimum, drop
   scope-cell matching, because scope is author-written free text.
3. **Narrow E1.** For counted upstream rows:
   - require a 64-hex `sha256` in the anchor cell, which real rows already have;
   - require a committed raw-bytes receipt whose sha256 equals it. Without
     committed receipts, no revision-bound counter can tell a fetched row from a
     fabricated one.
   - Until receipts exist, label V as "declared coverage", and have the canonical
     judge re-fetch the anchors of every row that newly counts.

   This is a tradeoff the judge must hold, not a defect the counter can close.
4. **Facet floor (T5).** Require each of `## Upstream contract` and
   `## Host declaration` to cite at least one counted S### id, its URL, or an
   anchor key. The P6 entry already uses this form (`[HW:n]`). This raises the
   cost of filler; it does not check truth, which stays judge-only.

## Artifacts

- Attack clone: `/tmp/ragame/mado-shokunin`, commits `de35fbc`, `3273d5d` and
  `4ae83f8`. It is throwaway and outside the lane.
- Installs: none. Lane writes: this report only.

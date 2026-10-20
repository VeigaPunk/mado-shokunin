# ReopenS056 — falsification re-open of source row S056

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60` (row and gate line confirmed in `git show HEAD`, working tree clean for both files).
Question: does S056's registry row and gate line hold against fresh bytes, and does the citing note
(`corpus/knowledge/terminal-route-r17.md`) make only claims this source supports at the anchors it gives?

## Verdict

**The attack largely failed.** URL, digest, byte size, tag pin, kind/tier/status/recheck, and all five
`teaches` elements reproduce exactly at the stated anchors. The note is honest about what the source does
not establish (no host fact, no version claim, no "Alacritty is the default" claim). Two countable defects
and one literal wording contradiction were found; none changes a route conclusion, none violates the
≤25-word rule, and none weakens the P4 documentary claim.

| # | defect | severity | effect on claims |
|---|---|---|---|
| D1 | Gate line says the quote is "(12 words)"; the displayed quote is **11** words | low, countable | none: 11 ≤ 25 either way |
| D2 | "first-valid" / "discarded" claims need README.md:170-171, outside the declared range `153-166` (row anchor cell **and** note bullet) | low, anchor precision | content is true at 170-171; range is one line short of the grounding |
| D3 | Note:45 "It is not a version claim or a behaviour claim" is literally false of the upstream sentence: "compliant" at README.md:264 is defined at 259-262 as `xterm -e` argument-handling behaviour | low, wording | no downstream over-read; conclusion ("names Alacritty as a compliant example") is correct |
| D4 | Note header anchor list drifts from the row: note:1 has `115-118,131,153-166,264`, omits `133` and `120-123` (both cited inline at note:31/33); `55-57` is listed by row and note but used by no inline claim | informational | no false claim; inline citations cover the row's anchors except 55-57 |

## Method / bytes

- `curl -fsSL https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md` → 337 lines,
  **14762 bytes**, `sha256 = c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40` — equals the row,
  the gate line, and note:82 byte-for-byte.
- Tag pin: `git ls-remote https://github.com/Vladimir-csp/xdg-terminal-exec 'refs/tags/v0.14.3*'` →
  `065925df9f419008159258ae169018bfd23df71b refs/tags/v0.14.3`, with **no `refs/tags/v0.14.3^{}` line**, i.e. a
  lightweight tag pointing directly at that object. Note:20-21's "(ref object 065925df…, lightweight tag)" is
  therefore correct as stated.
  (GitHub's REST ref endpoint returned HTTP 403 unauthenticated; `ls-remote` is the stronger check anyway.)
- Census: `scripts/sources-census.sh validate … mado` → `mado ok` (only pre-existing W04 duplicate-URL warnings
  for S030/S042/S045). Contract census block run directly: rows **70**, malformed **0**, tier A=63 B=1 C=6,
  status mined=55 queued=8 rejected=7 — exactly the gate's own arithmetic (70 = 63+1+6 = 55+8+7).

## Row audit (`corpus/SOURCES.md:68`)

| field | row value | observed | verdict |
|---|---|---|---|
| source / URL | tag-pinned raw `…/v0.14.3/README.md` | fetched, 200, bytes stable | ✓ |
| kind | docs | upstream README-as-specification | ✓ |
| tier | A | contract: A = "primary or authoritative for that scope (spec, official docs…)"; `docs`, not `community`; scope is narrow (tag v0.14.3 contract), not a host claim | ✓ (not tier inflation) |
| scope | "upstream default-terminal selection contract at tag v0.14.3 (ref 065925df…)" | ref resolves; README §Priority of selecting an entry is that contract | ✓ |
| anchor | `README.md:55-57,100-101,115-123,131,133,153-166,264` @ v0.14.3 (sha256 …, 14762 bytes) | every line exists and is on-topic; sha and size exact | ✓ (see D2/D4) |
| status | mined | `used-by` note exists and cites S056 at note:1 | ✓ |
| opened | 2026-10-20 | gate states all new rows opened 2026-10-20 | ✓ (not independently falsifiable) |
| recheck | on-release | contract allows; consistent with tag-pinned S005/S018 | ✓ |
| used-by | `corpus/knowledge/terminal-route-r17.md` | sole citing note; `git grep S056` outside `.ufo` shows only SOURCES, this note, the gate, and a `corpus/README.md:43` summary of the note | ✓ |

`teaches` cell, clause by clause (all OBSERVED against the fetched bytes):

- **selection-file names** — 100-101: "Configuration files are named `${desktop}-xdg-terminals.list` or
  `xdg-terminals.list` and placed in XDG config hierarchy." ✓ verbatim.
- **lookup order** — 113-123 resolved order: `${HOME}/.config/${desktop}-…`, `${HOME}/.config/xdg-terminals.list`,
  `/etc/xdg/${desktop}-…`, `/etc/xdg/xdg-terminals.list`, then `/usr/local/share/xdg-terminal-exec/…`,
  `/usr/share/xdg-terminal-exec/…`. Note:27-29's ordering statement is exact. ✓
- **system list as lowest priority** — 107-108 ("Lower priority fallback config files … in system part of XDG data
  hierarchy") plus 155-165 (config hierarchy composed first, system data hierarchy after). ✓
- **first-valid applicability check** — 166 ("Each entry … is checked for applicability") + 170 ("entry is
  discarded if it does not pass the checks") + 171 ("the first applicable entry is used"). ✓ content (D2 range).
- **Alacritty named as a compliant example upstream** — 264 is the **only** `alacritty` token in the whole README
  (`grep -in alacritty`): "Some examples of compliant terminals: xterm, alacritty, kitty, foot, qterminal" ✓.
  No default-terminal recommendation exists anywhere in the file. ✓ **no host fact** — S056 contributes none;
  every host statement in the note is sourced to S059/S060. ✓

## Gate audit (`corpus/lessons/round-17.md:43`)

- URL identical to the row. ✓
- Anchor `README.md:166`, quote "Each entry from the explicit selection list is checked for applicability:" —
  verbatim substring of line 166 (line reads `- Each entry from the explicit selection list is checked for
  applicability:`; the bullet is not quoted, consistent with other gate rows that excerpt within a line). ✓
- **Word count: 11, not 12.** `printf '%s\n' "…" | wc -w` = 11; regex `\w+` tokenization = 11. 12 is reproducible
  only by counting a token the displayed quote does not contain: either the line's leading `- ` bullet
  (`- Each … applicability:` = 12 whitespace tokens) or the trailing colon as a separate token. **D1**, and no checker covers it: `label-claims.json` has no S056 entry, so
  `label-check.py` does not validate gate word counts.
- Digest identical to the row and to fresh bytes. ✓
- Gate header "all opened 2026-10-20; quote ≤25 words; raw SHA-256" satisfies contract rule 1 (access date, quote,
  location); the chosen quote grounds the applicability clause, while the remaining four `teaches` elements are
  grounded only by the row's anchor cell (compliant but narrow — informational, not a defect).

## Citing-note claims from S056 (OBSERVED unless marked)

| note line | claim | anchor given | verdict |
|---|---|---|---|
| 20-21 | tag v0.14.3 → object `065925df…`, lightweight | tag | ✓ (ls-remote, no peeled ref) |
| 23-26 | selection-file names + quote | 100-101 | ✓ verbatim |
| 27-29 | `~/.config/xdg-terminals.list` after `${desktop}` sibling, before `/etc/xdg/` | 115-118 | ✓ |
| 31 | system-data copy lowest priority | 120-123 | ✓ (123 is last in the resolved order) |
| 32-33 | decreasing-priority list format; `#` lines ignored | 131, 133 | ✓ verbatim both |
| 34-36 | composition high→low, then applicability check; quote | 153-166 | ✓ |
| 37-38 | failing entries discarded → listing is a preference, not a launch guarantee | implied 153-166 | ✓ content, **anchor D2** (needs 170) |
| 43-45 | Alacritty named compliant; "not a version claim or a behaviour claim" | 264 | ✓ first clause; **D3** on second |
| 82 | 14762 bytes + sha | whole file | ✓ |
| 112 | applicability check at 166 | 166 | ✓ |
| 30 | script mirrors the sequence (xdg-terminal-exec:148-162) | S057, not S056 | out of scope for this seat |

## Attack attempts that failed (recorded so the synthesis does not re-run them)

1. **"Alacritty is upstream's default/recommended terminal" over-read** — absent. One `alacritty` token in the file
   (264), in an `-e`-argument list; the note's caveat (though mis-worded, D3) prevents the over-read and no
   downstream sentence depends on it.
2. **Version or running-binary claim smuggled through S056** — absent; the note pins only the tag and explicitly
   separates the pacman.log version binding.
3. **Host fact attributed to a docs row** — absent; `teaches` says "no host fact" and the note's host statements
   all cite S059/S060.
4. **Tier inflation** — absent; `docs` + official upstream README at a tag is A by the contract's own definition.
5. **Status/recheck misuse** — absent; `mined` matches a real `used-by` path, `on-release` is the tag-pinned cadence.
6. **Digest or size substitution** — absent; three independent records (row, gate, note) agree with fresh bytes.
7. **Anchor recall error on the quoted lines** — absent; all five quoted line groups reproduce verbatim, modulo
   the range shortfall recorded as D2 and the cosmetic list drift D4.

## Adjacent observation (not an S056 error, not attributed to this source)

`corpus/knowledge/terminal-route-r17.md:11-12` says the route "does not establish … the installed Alacritty
version", while note:113-117 records "installed alacritty (0.17.0-1)" from `pacman.log:639`. The two are about
different evidence types (tagged upstream docs vs log bytes), so this is a wording tension in the note's abstract,
not a false source claim. Flagged for the note's owner; no S056 action.

## Remaining unknowns

- The gate's 12-word annotation's origin (likely bullet-inclusive counting) — no tool in the lane computes it.
- `opened: 2026-10-20` is a self-declared date; not independently falsifiable from bytes.
- `README.md` has no release-date line; `on-release` cadence can only be tied to the tag, not to a date.
- Whether the row's `55-57` anchor was ever intended to ground a dropped clause (it grounds entry-ID listing,
  which no `teaches` element names); harmless, but if the row is corrected for D2 the anchor list should be
  reconciled with D4 at the same time.

## Minimal fix set (if L1 chooses to correct)

1. Gate line: change `(12 words)` → `(11 words)` for the displayed quote.
2. Row anchor cell and note:34-38: extend `153-166` → `153-171` (or quote 170-171 directly) so "discarded" and
   "first applicable entry" sit inside the declared range.
3. Note:45: replace "not a … behaviour claim" with "not a claim about this host's terminal behaviour" (the
   upstream term *is* an `-e` argument-handling behaviour claim, README.md:259-264).
4. Optional hygiene: align note:1's anchor list with the row (`115-123,131,133`) and either use or drop `55-57`.

Installs: none (no package, network-tool, or system command was run; all evidence is curl/read/hash plus a
read-only `git ls-remote` and the permitted census/validator).

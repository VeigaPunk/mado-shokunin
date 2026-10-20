# ReopenS064 — falsification re-open of source row S064 (hyprlock wiki)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60`.
Row and gate line are byte-identical at `HEAD` and in the working tree; the in-flight worktree diffs
(`corpus/SOURCES.md`, `corpus/lessons/round-17.md`, `corpus/README.md`,
`corpus/knowledge/terminal-route-r17.md`) contain no `S064` hunk (`git diff | grep S064` → empty), so
everything below is measured on the pinned lane bytes.

Question: does S064's registry row and its `## Gate` line hold against fresh bytes, and does the citing
note (`corpus/knowledge/idle-lock-route-r17.md`, the `used-by` cell) make only claims this source
supports at the anchors it gives?

## Verdict

**The attack failed on every substantive axis.** URL, raw digest, byte size, selector, page date,
verbatim quote, word count, kind/tier/status/recheck/used-by, and all seven claims in the row's
`teaches` cell (six documented defaults + the no-config-no-lock warning) reproduce exactly. No claim
attributed to S064 is false, no host fact is smuggled through the row, and the note keeps its
documentary boundary. Two **derived-anchor** defects exist in the citing note (D1, D2): its line
numbers are a derived artifact with no committed extractor, `[LW:7]` is one line late under the
literal legend, and the Arch pair `[LW:84]/[LW:85]` is three lines early under the only extractor I
could build that reproduces the other eight `LW` anchors. Neither defect changes a route conclusion
and neither touches the registry row.

| # | defect | severity | effect on claims |
|---|---|---|---|
| D1 | Gate/note anchor `[LW:7]` is not reproducible from the row alone: the note's legend ("line n of tag-stripped `<article>` text, one line per block, table cells run together") puts the warning sentence at line **6**; it is line 7 only if a callout/leading line is counted (the independent seat extraction does record 7) | low, anchor reproducibility | none: quote is verbatim and unique; one-line ambiguity in a derived locator |
| D2 | `[LW:84]` (Arch `pam_faillock` quote) and `[LW:85]` (remedy) resolve three lines early under the extractor that reproduces `[LW:7],[16],[37],[38],[49],[53],[54],[55]` exactly; the Arch sentence is at `LW:87`, remedy at `LW:88` (seat extraction: page:L147-L148) | low, anchor precision | none: the Arch quote is verbatim-present once (21 words); only its locator is unverifiable |
| D3 | Row anchor cell says "anchors are lines of tag-stripped `<article>` text (lines 6-85)", but the note also cites `[LW:1-3]` (drift bullet) | informational | none; range is one-sided |
| D4 | Note:1 lists "Warning" among the sections drawn from S064; the page has no Warning *section* (it is a callout label above `## Command-line Arguments`) | informational | none; the label exists on the page |

## Method / bytes

- `curl -sS -L https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/` twice, in separate calls:
  HTTP 200, **291777 bytes**, `sha256 = f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5`
  both times (byte-stable across fetches, no `--compressed`), identical to the row, the gate line and
  `SrcHyprlockWiki.md`'s recorded digest.
- Page identity: `<h1>hyprlock</h1>`; version selector label `Latest git` present once
  (`<a href=/version-selector/><span>Latest git</span>`); footer
  `<time datetime=2026-08-26T14:50:40.000Z>August 26, 2026</time>`; head
  `article:modified_time = 2026-08-26T14:50:40+02:00` — the note's "wiki 'Latest git', page modified
  2026-08-26" is correct (the seat report's `Z` vs `+02:00` discrepancy is upstream markup, not ours).
- Quote: the exact sentence occurs **once** in the tag-stripped `<article>` text and 4× in raw HTML
  (article + meta/JSON copies); `wc -w` = **24** (gate annotation: 24; rule ≤25 ✓).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`;
  the only output is the pre-existing W04 duplicate-URL warnings for S030/S042/S045. S064 raises
  nothing (no duplicate `wiki.hypr.land/…/hyprlock/` row, 11 columns, `docs` kind, `A` tier, `mined`).
- Contract (`kaika/SOURCES-CONTRACT-v1.md`): tier A = "primary or authoritative for that scope (spec,
  official docs…)" → the upstream project's own wiki is official docs, not `community`; `mined` =
  "cited by ≥1 path in `used-by`" → true; `recheck` `90d` is an allowed cadence. Rule 1's gate demand
  (URL, access date, ≤25-word quote with location) is met.

## Row audit (`corpus/SOURCES.md:76`, 11 columns)

| field | value | observed | verdict |
|---|---|---|---|
| id / source | S064, "hyprlock wiki page — https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/" | 200, page title/h1 hyprlock | ✓ |
| kind | docs | official upstream wiki | ✓ |
| tier | A | official docs for its own documented behaviour; no tier inflation | ✓ |
| scope | "hyprlock CLI (--grace), config search path, general/auth keys, Arch faillock note — wiki 'Latest git'" | all four present: `--grace SECONDS` (L16), four search paths in order (L21-25), general+auth tables (L37-55), Arch `pam_faillock` paragraph (L87) | ✓ |
| anchor | raw HTML sha256 `f69cff6b…`; "anchors are lines of tag-stripped `<article>` text (lines 6-85)" | digest exact; line range one-sided vs `[LW:1-3]` (D3); derived locator otherwise coherent | ✓ / D3 |
| teaches | "documented hyprlock defaults (hide_cursor, ignore_empty_input, fail_timeout, pam, fingerprint) and the no-config-no-lock warning" | every element verbatim on the page (table below) | ✓ |
| status | mined | note cites S064 at note:1 (token 2 of the S-token sequence) and uses it in the hyprlock section | ✓ |
| opened | 2026-10-20 | row written this round; not independently falsifiable | ✓ (declared) |
| recheck | 90d | contract-allowed cadence; tighter than the 180d used by the older docs rows, not a violation | ✓ |
| used-by | `corpus/knowledge/idle-lock-route-r17.md` | file exists, cites S064, contains `[LW:*]` uses | ✓ |

`teaches`/scope claims, each against the fetched bytes (OBSERVED):

- warning — "If no config file is found in any of the searched paths, hyprlock exits with an error and
  your session will not be locked." ✓ verbatim, unique, 24 words.
- `--grace SECONDS` — "Set grace period in seconds before requiring authentication" ✓.
- config search path — "Configuration is done via a config file named hyprlock.conf. Hyprlock searches
  for it in the following locations, in order:" then `$XDG_CONFIG_HOME/hypr/hyprlock.conf`,
  `$HOME/.config/hypr/hyprlock.conf`, `$XDG_CONFIG_DIRS` entries, `/etc/xdg/hypr/hyprlock.conf` ✓.
- `general:hide_cursor` → "Hides the cursor instead of making it visible." `bool` `false` ✓.
- `general:ignore_empty_input` → "Skips validation when no password is provided." `bool` `false` ✓.
- `general:fail_timeout` → "Milliseconds until the ui resets after a failed auth attempt" `int` `2000` ✓.
- `auth:pam:enabled` → "Whether to enable pam authentication." `bool` `true` ✓.
- `auth:pam:module` → "Sets the pam module used for authentication. If the module isn't found in
  /etc/pam.d, "su" will be used as a fallback." `str` `hyprlock` ✓.
- `auth:fingerprint:enabled` → "Enables parallel fingerprint auth with fprintd." `bool` `false` ✓.
- Arch — "On Arch Linux, by default, hyprlock integrates with pambase through pam_faillock.so, which
  forces a 10 minute timeout after 3 failed unlocks." ✓ verbatim, unique, 21 words; remedy sentence
  follows ("… refer to the arch linux wiki and update the file /etc/security/faillock.conf …").

## Gate audit (`corpus/lessons/round-17.md:51`)

- URL identical to the row and to the fetch. ✓
- `[LW:7]` + quote: the sentence is verbatim and unique in the article text. ✓ content.
- Word annotation `(24 words)`: **24** by whitespace tokenization. ✓
- Digest `f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5`: identical to fresh
  bytes, to the row, and to the seat report. ✓
- Tier/status/verdict: gate table carries none by design; the row supplies `docs | A | mined`, which
  the contract supports. ✓
- Anchor reproducibility (the only soft spot): the note defines `LW:n` as a line of tag-stripped
  `<article>` text, one line per block, table cells run together, but commits no extractor. Results:

| extractor | warning | grace | hide | ignore | fail_timeout | pam:enabled | pam:module | fingerprint | Arch |
|---|---|---|---|---|---|---|---|---|---|
| strict block (h/p/li/tr/pre/div; cells joined) | 6 | 15 | 34 | 35 | 40 | 44 | 45 | 46 | 65 |
| block + `<br>` + chroma `span.line`, +1 leading line | **7** | **16** | **37** | **38** | **49** | **53** | **54** | **55** | 87 |
| independent seat extraction (`SrcHyprlockWiki.md`, 683 lines, `page:Ln`) | 7 | 22 | — | 57 | 83 | 93 | 97 | 101 | 147 |
| note's stated `LW:` | 7 | 16 | 37 | 38 | 49 | 53 | 54 | 55 | 84 |

So `[LW:7]` is **corroborated** by the seat's independent 683-line extraction and by the second
extractor, and one line late under the strictest reading of the note's own legend (D1). The Arch pair
does not reproduce under any variant tried; the second extractor places the quote at 87 and the remedy
at 88, i.e. `[LW:84]/[LW:85]` are three low (D2). The page's `<br>`-bearing cells and 9-line chroma
animation tree are exactly the structures that make the numbering extractor-dependent — the note
declares the convention but not the code, so a re-checker cannot reproduce `LW:` from the row alone.

## Citing-note claims from S064 (OBSERVED unless marked)

| note location | claim | anchor given | verdict |
|---|---|---|---|
| note:56 | no-config → refuses to lock, quote | LW:7 | ✓ verbatim; D1 on the exact line |
| note:57 | `--grace SECONDS` quote; implementation not read | LW:16 | ✓ verbatim; "not read" is true (no hyprlock source opened this round) |
| note:58 | hide_cursor false; ignore_empty_input false; fail_timeout 2000 ms + quote | LW:37, 38, 49 | ✓ all three |
| note:59 | pam enabled true; module `hyprlock` w/ `su` fallback; fingerprint false | LW:53, 54, 55 | ✓ all three |
| note:60 | Arch pambase/`pam_faillock` 10-min after 3; remedy `[LW:85]` | LW:84, 85 | ✓ content; **D2** locator (text at 87/88) |
| note:1 | S064 sections "(Warning, Command-line Arguments, Configuration, General, Authentication, System Configuration)" | — | ✓ all present; "Warning" is a callout label (D4) |
| note:62 | fetched URL `wiki.hypr.land`; "page header [LW:1-3] carries no domain" | LW:1-3 | ✓ article header is breadcrumb/title only, no domain; range outside the row's "(6-85)" (D3) |

No sentence in the note attributes a host fact, a running binary, or observed lock/unlock behaviour to
S064; `--grace` implementation is explicitly marked unread; the host declarations use other sources.

## Attack attempts that failed (recorded so the synthesis does not re-run them)

1. **Wrong/stale digest** — absent; two fetches, four records agree.
2. **Quote not verbatim / over 25 words / not at the anchor** — absent; unique contiguous sentence,
   24 words, `[LW:7]` corroborated at page:L7 by an independent extraction.
3. **Typographic substitution** (curly quotes/ellipsis) — absent in this sentence; the page's curly
   quotes appear only in neighbouring `pam:module` text and do not touch the gate quote.
4. **Tier inflation / kind misuse** — absent; official upstream docs, `docs`+A is the contract's own
   A case.
5. **Status/recheck misuse** — absent; `mined` matches a real `used-by` path, `90d` is allowed.
6. **Host fact or version claim smuggled via S064** — absent; the row says nothing about the installed
   hyprlock and the note says the config warning is documentary.
7. **Scope overreach** ("config search path" claimed but not documented) — absent; four ordered paths
   are printed on the page.
8. **Duplicate URL** — absent; census raises no S064 finding.

## Remaining unknowns

- The exact extractor behind `LW:` (not committed); `[LW:7]` is therefore corroborated but not
  independently recomputable from the registry row.
- Whether `[LW:84]/[LW:85]` came from a stale numbering before the chroma tree/`<br>` accounting or
  are simple slips; the page bytes cannot decide it.
- `opened: 2026-10-20` is self-declared; not falsifiable from bytes.
- "Latest git" is a rolling target: the digest pins today's bytes only, and a future wiki rebuild will
  legitimately break the recheck, which is what `90d` is for.

## Minimal fix set (if L1 chooses to correct; none of it is mine to edit)

1. `corpus/knowledge/idle-lock-route-r17.md:60`: either commit the extraction script next to the note
   (then re-anchor to whatever it yields) or change `[LW:84]` → `[LW:87]` and `[LW:85]` → `[LW:88]`,
   the lines the reproducing extractor above assigns to the Arch quote and its remedy.
2. Same note, anchor legend (note:19, table 15-22): state that `<br>` and chroma code lines are line breaks and
   whether a callout boundary counts — this is what makes `[LW:7]` 7 instead of 6.
3. `corpus/SOURCES.md:76` anchor cell: replace "(lines 6-85)" with the actually-cited range
   (1-88 under the D2 fix, or "6-88") and keep the digest as the primary revision pin.
4. Optional: note:1 "Warning" → "Warning callout" so the citation matches the page outline.

Scope discipline: this seat wrote only this report; no lane file, no commit, no `git`/`jj` mutation.
Host-pause honoured: no `pacman`/`yay`/`paru` (not even queries), no `sudo`/`systemctl`/`loginctl`/
`journalctl`/`hyprctl`/`libinput`/`evtest`/`hypridle`/`hyprlock`/terminal/`omarchy-*`/screenshot/probe,
no `<binary> --version`, no agent DB or credential file opened, no omp CLI process.

Commands actually used: `curl -sS -L` (two fetches), `sha256sum`, `wc -c`, `python3` stdlib
(`html.parser` + `bs4`/`lxml` for extraction experiments on `/tmp` copies), `grep`, `sed`,
`sources-census.sh validate`, and read-only `git log`/`git rev-parse`/`git show`/`git diff`.
Installs: **none**.

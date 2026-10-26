# ExecEntryQuotes — w2 falsify: every quote and locator of the entry draft, by script

Seat: `ExecEntryQuotes` (wave w2, round 47, policy v1). Lane: `mado-shokunin`.
Target: `.ufo/waves/round-47/w1/ScrEntry/entry.md` (`sha256 5e7db5ae…b0c53ec`, byte-equal to
`git show HEAD:…`, i.e. the committed draft) against the pins **committed at the frozen claim**
`d7527d6` under `.ufo/waves/round-47/fetch/` (`xdg-terminal-exec` `89f2be9a…7ac`, `README.md`
`c7a1a8bb…d40`, `xdg-terminals.list` `a2b5bf69…034`).
Authoritative contract mirrored: the clause-d / clause-e docstring of
`quality/counters/c2-r47-terminal-entry.py` (frozen), not a re-invention.

## Verdict

**No falsifying hole in the quote/locator layer.** Every locator is inside its pin, every clause-d
quote is verbatim at its stated range, every numbered step carries a script range, all nine cited
function bodies are exact, and all seven census numbers recompute. **Eight precision defects remain**
(one of them an integration defect that a reader hits immediately); none of them makes the frozen
predicate fail as written, but each is cheaper to fix before the data commit than after.

## Artifacts (all in `.ufo/waves/round-47/w2/ExecEntryQuotes/`)

| file | what it is |
|---|---|
| `check_entry.py` | the checker: extracts every span and locator, mirrors clause d/e, adds stricter binding rules, recomputes the census, re-runs w1's receipts, inventories the host slots, and runs a 9-mutation self-test |
| `emit_tables.py` | emits the three tables below |
| `locators.csv` | 111 locator occurrences: entry line, pin, range, in-range, pin line count |
| `quotes.csv` | 14 clause-d quotes: pin, range, word count, occurrence lines, verdict |
| `spans.csv` | 238 code/prose spans: word count, class, which pin holds them verbatim |
| `function-bodies.txt` | computed bodies of the 23 pinned functions vs the 9 ranges the entry cites |
| `receipts.txt` | the command→output receipt for every defect below |
| `run.txt` | full transcript of the final run (exit 0, 0 hard findings) |

Checker self-test: 9 injected defects (single-line locator shift, quote range shift, doctored quote
word, function-body range ±1, locator past pin end, doctored OBS quote, README range shift, function
cited at another function's body, altered census number) — **9/9 caught**; the unmutated entry
reproduces the baseline finding set and exits 0.

## What holds (support, not a claim)

- **Locators**: 111 occurrences — 102 `xdg-terminal-exec`, 5 `README*`, 4 non-pin
  (`terminal-route-r17.md` ×3, `~/.config/hypr/bindings.conf` ×1). **0 out of range**; the script
  pin has 1500 split-lines (1499 by `wc -l`) and the highest cited line is 1499.
  The four non-pin locators were checked against their real files: `corpus/knowledge/terminal-route-r17.md`
  has 153 lines at the frozen claim and `:144-145` / `:150-151` hold exactly the `[UNK]` and the
  unrun-helper text the entry cites; `~/.config/hypr/bindings.conf:2` is exactly the quoted `bindd`
  line (`receipts.txt`, L7b).
- **Clause-d quotes**: 14 sites, 14 `AT_RANGE`, 0 `NOT_IN_PIN`, 0 `OUT_OF_RANGE`, longest 16 words
  (limit 25). This includes the README quote that spans two lines (`:300-301`) and the two-line OBS
  quote (`:179-180`).
- **Clause e**: 7 numbered steps, 7 carrying an in-range `xdg-terminal-exec` range.
- **Function attribution**: all nine cited function bodies are exact — `gen_hash 179-215`,
  `read_cache 217-298`, `save_cache 300-340`, `de_expand_str 501-559`, `de_tokenize_exec 561-692`,
  `de_strip_fields 694-740`, `find_entry_paths 754-800`, `check_entry_key 802-968`,
  `read_entry_path 970-1018` (`function-bodies.txt`).
- **Census**: 7/7 recomputed — script_lines 1499, functions 23, directives 5, print_data_kinds 4,
  cache_header_fields 10, cache_hash_format 4, data_side_list_slots_per_data_dir 2.
- **Host paragraph**: the eight list slots in the script's own order, 2 present — the user's
  `~/.config/xdg-terminals.list` (exactly one plain line, `Alacritty.desktop`) and
  `/usr/share/xdg-terminal-exec/xdg-terminals.list` (exclusions + `/execarg_default` rows only, no
  plain entry line); all three of the paragraph's statements hold, and 2 of the 3 application dirs
  exist (`/usr/local/share/applications` absent, which the script skips silently).

## Holes (all reproducible; `receipts.txt` holds each command and its output)

### H1 — the S326 pin path does not resolve from where the entry will live *(fix before data)*
`entry.md:3` names the pin as `` `pins/xdg-terminal-exec-v0.14.3.sh` `` — a relative path. From the
entry's own directory that is `corpus/knowledge/pins/…` (**absent**); from the lane root,
`pins/…` (**absent**). It exists only as `.ufo/waves/round-47/w1/ScrEntry/pins/xdg-terminal-exec-v0.14.3.sh`.
The committed pin the counter trusts is `.ufo/waves/round-47/fetch/xdg-terminal-exec`
(same bytes, `sha256 89f2be9a…`). C2 clause d resolves quotes by *token name*, so the quotes survive
this; a reader and the declared non-author closure re-run cannot open the pin from the entry.
```
for p in corpus/knowledge/pins/xdg-terminal-exec-v0.14.3.sh pins/xdg-terminal-exec-v0.14.3.sh \
         .ufo/waves/round-47/w1/ScrEntry/pins/xdg-terminal-exec-v0.14.3.sh; do
  [ -e "$p" ] && echo "PRESENT $p" || echo "ABSENT  $p"; done
ABSENT  corpus/knowledge/pins/xdg-terminal-exec-v0.14.3.sh
ABSENT  pins/xdg-terminal-exec-v0.14.3.sh
PRESENT .ufo/waves/round-47/w1/ScrEntry/pins/xdg-terminal-exec-v0.14.3.sh
```

### H2 — `README:6-8` starts on a blank line
`entry.md:6` cites `README:6-8` for the proposed-status warning. Line 6 is empty; the warning is
7-8. `grep -n 'compatibility is maintained' .ufo/waves/round-47/fetch/README.md` → `8:`; line 7 is
`(!) Please be advised that while this spec is in proposed state, backwards`.

### H3 — step 5 range `1113-1140` overruns the function it means
`entry.md:30` cites `(xdg-terminal-exec:1092-1100, 1113-1140)` for the `/execarg_default` lookup.
`get_default_execarg()` starts at 1113 and closes at 1130; 1132-1141 is the unrelated
`-h|--help` loop. Ten cited lines carry something the sentence does not claim.
`grep -n "^get_default_execarg()" …` → `1113:`; `grep -n '# print help and exit' …` → `1132:`.

### H4 — step 4 cites the Hidden arm one line past its end
`entry.md:29` writes “rejects `Hidden=true` (xdg-terminal-exec:938-947)”. The Hidden arm is 938-946
(`946` is `;;`); `947` opens `'Exec'*=*)`. `grep -n "^\t'Hidden'\|^\t'Exec'" …` → `938:`, `947:`.

### H5 — one guard cited as the witness for four guards
`entry.md:27` cites `(xdg-terminal-exec:376-379)` for “the first two and the first two of the second
pair honour only the first encountered occurrence”. The four guards are at 376, 382, 390 and 396;
376-379 witnesses only the first.
`grep -n '_CONFIGURED" ] || continue' …` → `376: 382: 390: 396:`.

### H6 — “cats the entry and exits at once” cited only to the cat
`entry.md:32` cites `xdg-terminal-exec:1362` for “`--print-content` cats the entry … and exits at
once”. 1362 is `shcat < "${XTE__ENTRY_PATH}"`; the exit for a content-only print run is 1374-1376
(the sentence's general bail-out is cited separately at 1368-1385). The second verb has no locator
of its own. `grep -n 'shcat <' …` → `1362:`; `read …:raw:1374-1376` → `*' content '*)`, comment,
`exit 0`.

### H7 — the cited `885-931` span also holds an arm the sentence does not name *(informational)*
`entry.md:29` says the range “expands and stores the `[X-]TerminalArg{Exec,AppId,Title,Dir,Hold}`
values”; 893-904 is the legacy `X-ExecArg`/`ExecArg` arm (ignored in strict mode). The range is
true, it is just wider than the named set. `grep -n "'X-ExecArg'" …` → `893:`.

### H8 — the OBS S327 quote is split through the middle of the sentence *(minor)*
`entry.md:45` renders the pin as `` `…are checked` / `in is undefined` ``. Both fragments are
verbatim, but the pin sentence is “are checked **in** is undefined”: joining the fragments yields
“checkedin is undefined”, and only the second fragment carries the locator (the first is flagged
`QUOTE_NOT_LOCATED` by the checker). Prefer one span over `:179-180`.

### W1 — w1's own receipts are true but do not cover the entry
Re-run independently: their 119 locator probes still pass (0 mismatched, as their `locators.txt`
claims) and their 10 quote probes hold. But:

- 8 of the entry's 111 locator occurrences have **no** w1 probe line inside their range
  (`README:6-8`; `xdg-terminal-exec:1144`, `376-379`, `427-437`, `435-438`, `501-559`, `561-692`;
  `bindings.conf:2`).
- 5 of the entry's 14 clause-d quotes have **no** w1 quote probe:
  `entry.md:27 → :425`, `:28 → :766`, `:41 → :780`, `:44 → :1092`, `:45 → README.md:179-180`.

So `119 checked / 0 mismatched` and `10/10` are honest about what they probed and silent about the
rest; nobody should read them as “every quote and locator verified” — this seat is that check.

## Limits of this seat

- The resolver was **not** run (no live capture); every `<LIVE:…>` row belongs to the live seat.
- Clause c (`pin bound by a row`), b, f, g, i of C2 are out of scope here; H1 is reported because it
  is a *pin reachability* fact, not because I judged the rows.
- The span↔locator pairing is mechanical (nearest preceding span with a punctuation-only or `at `
  gap); spans that are verbatim in a pin but unattached are reported as soft `QUOTE_NOT_LOCATED`,
  never as a hole.
- Host inventory numbers come from this session's `XDG_*` values, which the entry says the hotkey
  inherits; if the hotkey's environment differs, the inventory changes with it (recorded in
  `receipts.txt`, L9).
- No finding here is a licence to touch the frozen counters, fixtures or `registration.md`.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/ExecEntryQuotes
TMPDIR=<scratch> python3 -I check_entry.py            # exit 0, 0 hard findings, 9/9 mutations caught
TMPDIR=<scratch> python3 -I emit_tables.py            # regenerates locators.csv quotes.csv spans.csv
```

Read-only throughout: every pin and lane file is read with `git show d7527d6:…` / `git show HEAD:…`;
no git/jj mutation, no resolver run, no package transaction, nothing written outside this seat
directory and this report; scratch (`/fast/scratch/hyaku/mado-r47/ExecEntryQuotes`) removed.

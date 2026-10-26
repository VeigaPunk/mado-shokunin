# RevC2Counter — falsification review of `quality/counters/c2-r47-terminal-entry.py` (PRED-C2-r47, frozen at d7527d60)

Target: the frozen counter at the freeze commit (working-tree copy byte-equal: sha256
`cdd4c8460c7289cedab3f8c7426cf80065516d7d51df3ea56272e614bc6e9be5` both at
`d7527d608ad2b2e3cc398fdde34db7947b254a1a` and in the tree). Reviewed clause by clause against
its docstring and `.ufo/waves/round-47/registration.md`, with special attention to the
L1-rewritten clause_f (diffed against `.ufo/waves/round-47/w1/ExecCounterC2/c2-r47-terminal-entry.py`),
pin resolution by stem, quote matching, and the ground terms.

Method: every admission/miss claim below was executed. The POS control was rebuilt in scratch
(`/fast/scratch/hyaku/mado-r47/RevC2Counter`, removed after the run) with
`C2R47_WORK` pointing at the extracted v0.14.3 tag tarball, and each probe is one commit in that
scratch clone plus one counter run. Full counter output per probe: `P*.txt` in this directory.
No lane file was written; no subagents; no pacman; the resolver was never executed.

## Findings (by severity)

### F1 — HIGH, clause c: any non-https URL bypasses ref-pinning (branch URLs admitted)

`url_ref_path` (c2-r47-terminal-entry.py:334-350) parses only `https://` forms (RAW_RE/GH_RE/GL_RE
are all anchored `^https://`), and `URL_RE` (:115) is case-sensitive `https?://`. Any URL the three
regexes do not recognize — `http://…`, `HTTPS://…` (invisible to URL_RE altogether), `ftp://…` —
returns `(None, None, None, u)` and is then admitted by `scan_urls` (:377-383) whenever the row
records any 40-hex commit and any sha256. The S326 row already records the tag commit
`065925df…`, so the bypass needs nothing extra. The scheme downgrade also skips the xte-path check
(:432-434, `(repo_n or "").lower() in XTE_REPOS and path in PIN_SHA`), so the row may name any path
on the xdg-terminal-exec repo over http. (The docstring's ref-less allowance is at :47-49.)

Repro (verified, `P1-http-branch-url-admitted.txt`, rev `b11e7d3223e632d89e9919b80e6050aad086a91b`):
POS tree, S326 row URL → `http://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/main/xdg-terminal-exec`
→ `clauses=… c:1 … admitted=1 verdict=TARGET_MET`. The identical mutation over https is the BRANCH
control and is refused (`url_branch_ref`), so the refusal is scheme-dependent. Registration clause c
says "`main` … and every other ref are refused"; for an http URL that is false.

Note: the docstring (:46-48) and the registration both carry the same "URL with no ref segment …
refused unless the row records a 40-hex commit" allowance, so code matches predicate text — the hole
is in the predicate design: "no ref segment" is decided by a https-only parser. v2 should fail closed
on unparseable URLs (refuse any URL not matching a known https form, or parse the scheme
case-insensitively and require https).

### F2 — MEDIUM, clause d: an ambiguous-stem bare locator escapes both the range check and the pin-cited check

`clause_d` :474-476: `pint = resolve_pin(n, all_pins, by_base); if pint is None: continue` — an
unresolved locator is silently skipped. `resolve_pin` (:302-313) returns None when the stem matches
2+ fetch copies, and `stem()` (:287-293) matches by bidirectional substring over extension-stripped
basenames, so two fetch pins sharing a basename in different subdirectories unresolve every bare
locator with that basename. The docstring (:56-58) claims "every pin locator of the entry must stay
inside its pin's line count and its pin must be cited by a row by name or by bytes … an uncited pin
cannot launder a quote" — under ambiguity neither holds.

Repro (verified, `P2-ambiguous-locator-admitted.txt`, rev `040371e5ac3d686f3e75e7eda7de75800b5c482b`):
POS + `fetch/other/README.md` + `fetch/another/README.md` (junk bytes) + unfenced entry line
`Ambiguity probe: README.md:99999.` → `admitted=1 verdict=TARGET_MET`; no `pin_not_cited_by_row`, no
range failure. Controls show the hole is exactly the ambiguity-skip: a unique-stem uncited pin IS
caught (`P9-unique-uncited-caught.txt`: `pin_not_cited_by_row=zzjunk.md`, MISSED) and the same
ambiguity in a QUOTE locator fails closed (`P10-ambiguous-quote-caught.txt`:
`quote_locator_unresolved`, MISSED).

Fix direction: distinguish lane-doc locators from pin locators — if the token's basename/stem
matches ≥ 1 fetch pin but resolves to none, flag it (a lane path exists in the REV tree → exempt;
else unresolved → fail).

### F3 — MEDIUM, clause g (false-negative trap): README id ranges expand only over ASCII `-`; house style uses en-dashes

`clause_g` :637-638 `re.findall(r"S(\d{3,})(?:-S(\d{3,}))?", cells[2])`. The existing README rows
use en-dashes (`corpus/README.md:43`: "S056–S060"), so an honest README row written in house style
covers only the range endpoints.

Repro (verified, `P8-endash-readme-missed.txt`, rev `f0d6bc69134af2b16e9d5f4732f8b60121cfb56b`):
POS, README row "Sources S326-S330." → "Sources S326–S330." →
`clause=g readme_missing_ids=['S327', 'S328', 'S329']`, `g:0`, MISSED. The data commit must use
ASCII hyphens in the README row (or v2 normalizes dashes).

### F4 — MEDIUM-LOW, clause b: fenced lines escape the head-window source check and the ghost check

`score()` :685-694 `continue`s on fence markers before both the `outside` count (source/verified-at/
recheck lines below the 20-line window) and — via `lines = unfenced(text)` (:680) — the ghost-id
census. The docstring (:26-33) says "no `source:`/`verified-at:`/`recheck:` line outside that
window" with no fence exception (the ghost rule is explicitly unfenced-scoped, so a fenced S999 is
per-docstring acceptable; the source-line rule is not).

Repro (verified, `P4-fenced-source-admitted.txt`, rev `a3553f7e6eb61a8b27fa1266191910c7c8df4e67`):
POS + appended fenced block containing `source: S999 - invented row, cited only inside this fence:
S999` → `outside_head=0`, no ghost, `admitted=1 verdict=TARGET_MET`.

### F5 — LOW-MEDIUM, clause c: the fetch pin's git mode is never checked (docstring says 100644)

Docstring :39 "that copy exists at REV, mode 100644"; `fetch_pins` (:316-331) discards the mode
field and no `ls_mode` is called on pins (the only mode check in the file is clause_f's receipt,
:574).

Repro (verified, `P3-pin-mode-100755-admitted.txt`, rev `6cfb152df1d90d555cf1630ae9cf7e989939134a`):
POS, `chmod 755` the script pin, recommit → `git ls-tree` shows `100755 blob a38920f7…` and the
counter admits (`TARGET_MET`). Fix: check `ls_mode(repo, rev, FETCH+name) == "100644"` for each
cited pin.

### F6 — LOW, clause f: failing candidate receipts are tolerated; a nonexistent receipt cited on the r17 line is ignored

`clause_f` :562-611 (receipt regex :564, `full == 0` at :611): every per-receipt failure path `continue`s; only `full == 0` fails. The entry
may cite any number of broken receipts beside the good one.

Repro (verified, `P7-bogus-receipt-tolerated.txt`, rev `51f66cf7ae639ec60869e2145d9824a90d2a891b`):
POS + "Corroborated by .ufo/waves/round-47/receipts/bogus.txt." appended to the r17:144 line →
`clause=f receipt_missing=…bogus.txt.` printed, `admitted=1 verdict=TARGET_MET`. Also visible in the
shipped POS receipt itself (`ctl-pos.txt`): the capture `live-observed.txt` is collected as a
candidate receipt and its `receipt_short=…:84` failure is tolerated. Low because the passing receipt
is fully checked; but "an unfenced entry line names … and cites `<file>`" (docstring :66-68) reads
singular.

### F7 — LOW, clause f: the "entry line states that id and that path" check is substring containment

`clause_f` :605 `said = any(sel in l and (pth in l or tilde in l) …)` — no word boundaries, so a
wrong id that contains the capture's id as a substring passes.

Repro (verified, `P6-substring-id-admitted.txt`, rev `5cfa23b2cfe6d445608e9a64f344663dac474676`):
POS, entry's live sentence mutated to `selected=XAlacritty.desktop path=…` (the capture says
`Alacritty.desktop`) → `admitted=1 verdict=TARGET_MET`. Fix: word-boundary the id match (the
`occurrences`/`is_word` machinery already exists) or require `selected=<sel>`/`path=<pth>` shapes.

### F8 — LOW, clauses c/d/e: the pin line count is one past the last real line

`lines = len(blob.decode(…).split("\n"))` at :447 (clause_c), :478 (clause_d `plines`), :525
(clause_e `nlines`): a file ending in a newline yields N+1, so a locator to the phantom line passes.

Repro (verified, `P5-phantom-line-admitted.txt`, rev `81a7fb47b0d8d049e14580665ddd9e32d64b726c`):
the script pin has `wc -l` = 1499, split-count 1500; a bare locator `xdgte-xdg-terminal-exec:1500`
is accepted → `admitted=1 verdict=TARGET_MET`. Fix: drop the trailing empty element (the control
builder already computes `len(lines_of(path)) - 1`, build-control.py:79).

### F9 — LOW, clause c: anchor locators resolving to no fetch copy are accepted without a name check

:455 `if r == fname or r is None: ranges.append((a, b))` — the `r is None` branch is meant for
"an upstream path name the pin is a renamed copy of" (docstring :44) but accepts any invented
name; the range is then only length-checked against the pin. An anchor can carry
`made-up-file.md:1-2` ranges. Code-read (branch is explicit); no probe needed.

### F10 — LOW, clause h: "byte-equal" is compared on whitespace-normalized cells

`registry()` :206-216 strips each cell; `clause_h` :646-655 compares parsed cell lists, so held rows
differing only in inter-cell spacing compare equal. Docstring :77 says "byte-equal at BASE and REV".

### F11 — LOW, clause c: the row's digest set is any 64-hex anywhere in the row

`sha_in_row` :352-358 collects `sha256:<hex>` and bare 64-hex; clause_c :428 accepts the pin's
digest appearing as an unlabeled hex anywhere in the row text. Docstring :37-38 says the row
"records `sha256:<64hex>` … and its sha256 equals the row's digest" (:37-38). Binding still requires the
correct digest to be present, so this is looseness, not a bypass.

### F12 — LOW, clause d: lane-doc locators can be resolved onto fetch pins by loose stem matching

`resolve_pin`'s stem fallback (:310-313): a locator like `corpus/README.md:43` (the lane's README)
resolves to the fetch pin `xdgte-README.md` (stem "readme" ⊂ "xdgte-readme") and is then
range/citation-checked against the PIN, not the lane file. In the POS the README pin is row-cited
so it passes silently; if it were not cited, a legitimate lane-doc citation would false-fail
(`pin_not_cited_by_row`). Code-read + P2/P9 resolution mechanics.

### F13 — dead code (cleanliness)

- Frozen counter: `MADO_RE` (:149) is unused (w1 clause_f leftover); `import shutil` (:100) and
  `import tempfile` (:103) are unused.
- `ctl/c2/build-control.py` `write_tool()` (:247-283) is never called from `main()` (:322-348) —
  w1-draft leftover. Verified harmless: the committed POS tree contains no `tools/mado-terminal.py`
  (`git ls-tree HEAD tools/mado-terminal.py` empty), so the registration's "entry-only tree (no
  tool)" description holds.

## Clause_f (L1 rewrite) — verdict and data-side consequences

The rewrite does what the registration says: the w1 draft's `explain --observed` re-run of
`tools/mado-terminal.py` (w1 draft :564-578, :628-667) is gone; the frozen clause_f (:557-615) never
touches the tool (no `TOOL` constant, no subprocess), requires `^resolver_sha256=89f2be9a…$` (:592),
≥3 XDG_* lines, an `observed=` capture absent at BASE whose first line ends `.desktop` and second
starts `/` (:596-600), and the citing entry line to state the id and path (:605). C2 no longer
depends on C1. The capture-format checks match the real resolver: entry IDs validate to `*.desktop`
(pinned script :1020-1030), the default print delimiter is `'\n'` (:1222), and the print order is
id→path→cmd (:1327-1366) — verified against the pinned bytes.

Consequences the L1 must handle before the data commit (pre-data, so fixable):

- **D1**: the w1 live receipt `.ufo/waves/round-47/w1/ExecLive/receipts/live-host.txt` has NO
  `resolver_sha256=` line (it records "sha256(/usr/bin/xdg-terminal-exec) = 89f2be9a…" at line 3) —
  under the frozen clause_f it fails `receipt_no_resolver_sha`. Its capture is also inline in
  section [2], not a separate `observed=` file. The receipt must be reformatted (or the capture
  re-run) before the data commit.
- **D2**: the w1 draft rows (`.ufo/waves/round-47/w1/ScrRows/rows.md`) cite receipts at
  `.ufo/waves/round-47/w1/ScrRows/fetch/…`; `row_receipts` (:361-366) only accepts
  `.ufo/waves/round-47/fetch/<name>` → `fetch_receipts=[]` → clause_c fails. Receipt paths must be
  rewritten to the final fetch/ location.
- **D3**: the w1 draft entry's r17 line cites `.ufo/waves/round-47/receipts/<LIVE:live-receipt>`
  (placeholder); the receipt regex (:564) stops at `<` → `receipt_missing` → clause_f fails until
  filled. The fill must keep the id+path on the same line as the r17:144 citation and the receipt
  citation (and per F7, state the id as a standalone token).
- **D4**: the README row must use ASCII hyphens in id ranges (F3).
- **D5**: a receipt path at the end of a sentence absorbs the trailing period
  (`[A-Za-z0-9._-]+` at :564) — `receipt_missing=…bogus.txt.` in P7 — so receipt paths need a
  backtick/comma/paren boundary. Drafting hazard, fails closed.

## Positive verifications (support)

- All six `PIN_SHA` digests equal sha256 of the real v0.14.3 tag-tarball files; tarball sha256
  `82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe` matches the registration's pin
  (fetched from the codeload URL; copy + SHA256SUMS in `pins/`).
- Pinned script sha == host `/usr/bin/xdg-terminal-exec` sha (`89f2be9a65deb8df…127ac`) — docstring
  claim verified.
- Ground terms all exist in the real script: `read_config_paths` :351, `find_entry_paths` :754,
  `check_entry_key` :802, `--print-delimiter` :127/:1305 — the clause-i census measures real names.
- Base behavior: `admitted=0/1 verdict=TARGET_MISSED`, exit 1 at `60edb66e…` (reproduced);
  SETUP (entry present at base) exit 2 (verified).
- Full control suite re-run on the frozen bytes (`ctl-receipts/` in this dir): POS MET;
  BASE/QUOTE/BRANCH/HELD/RECEIPT/NOSTEPS/OBS/NOSHA/RANGE/PIN all MISSED with their intended clause
  tokens — the registration's control claim holds for the frozen clause_f.
- Separability both ways on the frozen bytes: the POS tree contains no `tools/mado-terminal.py` and
  is admitted; a tool-only tree (tool present, entry absent) is MISSED at clause a
  (`P11-toolonly-missed.txt`, rev `c04e54cb…`).
- The counter writes nothing (all reads via `git show`/`ls-tree`/`grep`; tempfile/shutil dead) and
  strips ambient `GIT_*` env (:112) — the "nothing in the lane is written" claim holds.

## Residual risk / verification gaps

- The declared residual stands and is the biggest one: clause_f binds a capture's FORM and digest
  line, not its production — a hand-typed receipt+capture pair passes; the counter cannot tell. The
  registration's mitigation ("the non-author closure re-runs the print command") is outside the
  counter and outside the counting command; if that closure never runs, clause_f is form-only.
- Clause e counts numbered steps and script locators, not the truth of each step (declared).
- Clause c binds URL+digest+name, not the truth of the row's scope sentence (declared).
- Not probed: `git grep` behavior on a corpus pathspec with unusual index states (the counter is
  revision-addressed, so exposure is minimal); ReDoS on adversarial entry lines (spans are capped at
  600 chars); a pin path containing a TAB (ls-tree quoting would mis-parse → fails closed).
- No LSP server was available for this review (no `lsp` device in this seat's toolset); all checks
  are text-level plus executed repros.

# RevC2Counter — w2 FALSIFY seat report (round 47, hyaku 9)

Status: COMPLETE 2026-10-26. Scope: code review of `quality/counters/c2-r47-terminal-entry.py`
(PRED-C2-r47, frozen bytes sha256 `cdd4c846…9be5`, byte-equal at the freeze commit
d7527d608ad2b2e3cc398fdde34db7947b254a1a) against its docstring and
`.ufo/waves/round-47/registration.md`; the L1-rewritten clause_f diffed against the w1 draft
(`.ufo/waves/round-47/w1/ExecCounterC2/c2-r47-terminal-entry.py`); pin resolution by stem, quote
matching, ground terms. Full findings with path:line + verified repro:
**.ufo/waves/round-47/w2/RevC2Counter/findings.md** (probe receipts `P1…P11.txt`, re-run control
receipts `ctl-receipts/`, pin evidence `pins/` in the same dir).

## Verdict

The frozen counter is solid on its core bindings — all six PIN_SHA digests verified against the
real v0.14.3 tarball (tarball sha `82ac2dfd…` matches the registration), pinned script sha ==
host `/usr/bin/xdg-terminal-exec`, ground terms real (script :351/:754/:802/:127), base = MISSED
exit 1, SETUP exit 2, full control suite re-run on the frozen bytes (POS MET; 10 negatives MISSED
on their intended clauses), separability shown both ways (entry-only POS admitted with no
`tools/mado-terminal.py`; tool-only tree MISSED at clause a), and the counter writes nothing.
Clause_f's L1 rewrite is correctly separable (never touches the tool) and its capture-format
checks match the real resolver's print output.

But there are holes, found BEFORE any data commit — re-registration material:

1. **F1 (HIGH, clause c):** any non-https URL bypasses ref-pinning — `url_ref_path` parses only
   `https://` forms, so an `http://…/main/…` branch URL is "ref-less" and admitted on a recorded
   40-hex commit + digest; it also skips the xte-path check. Verified: POS + http branch URL in
   S326 → `TARGET_MET` (`P1-http-branch-url-admitted.txt`, rev `b11e7d32…`); the https twin is the
   BRANCH control and is refused. Registration clause c ("`main` … refused") is false for http.
2. **F2 (MEDIUM, clause d):** an ambiguous-stem bare locator escapes both the range check and the
   pin-cited check (`clause_d` :474-476 skips on `resolve_pin` → None). Verified: two junk pins
   named `*/README.md` + entry line `README.md:99999.` → `TARGET_MET` (`P2…`, rev `040371e5…`);
   unique-stem uncited pin IS caught (P9) and ambiguous QUOTE locators fail closed (P10) — the
   hole is exactly the bare-locator skip.
3. **F3 (MEDIUM, clause g, false-negative trap):** README id ranges expand only over ASCII `-`;
   house style uses en-dashes (`corpus/README.md:43` "S056–S060"). Verified: en-dash range →
   `readme_missing_ids=['S327','S328','S329']` → MISSED (`P8…`, rev `f0d6bc69…`).
4. **F4 (MEDIUM-LOW, clause b):** fenced lines escape the head-window `source:` check and the
   ghost census. Verified: fenced `source: S999` after raw line 20 → `TARGET_MET` (`P4…`).
5. **F5 (LOW-MEDIUM, clause c):** the fetch pin's git mode is never checked (docstring :39 says
   100644). Verified: pin at 100755 → `TARGET_MET` (`P3…`, rev `6cfb152d…`).
6. **F6/F7/F8 (LOW):** failing candidate receipts tolerated / nonexistent receipt ignored (P7);
   the clause-f "states that id" check is substring containment — `XAlacritty.desktop` passes
   (P6, rev `5cfa23b2…`); pin line count is one past the last real line — locator to the phantom
   line 1500 accepted (P5, rev `81a7fb47…`).
7. **F9-F12 (LOW):** anchor locators resolving to no pin accepted unchecked (:455); clause-h
   "byte-equal" is cells-equal; the row's digest set is any 64-hex anywhere; lane-doc locators can
   stem-resolve onto fetch pins and false-fail.
8. **F13 (dead code):** `MADO_RE` (:149), `import shutil`/`tempfile` unused in the frozen counter;
   `build-control.py` `write_tool()` never called (harmless — POS tree has no tool file).

## Data-side consequences the L1 must handle before the data commit

- **D1:** the w1 live receipt (`w1/ExecLive/receipts/live-host.txt`) has NO `resolver_sha256=`
  line and its capture is inline, not an `observed=` file — under the frozen clause_f it fails
  `receipt_no_resolver_sha`. Reformat or re-run before the data commit.
- **D2:** the w1 draft rows cite receipts at `w1/ScrRows/fetch/…`; the counter only accepts
  `.ufo/waves/round-47/fetch/<name>` → clause_c would fail. Rewrite paths.
- **D3:** the draft entry's `<LIVE:live-receipt>` placeholder breaks the receipt regex until
  filled; the id+path must sit on the same line as the r17:144 citation.
- **D4:** README row must use ASCII hyphens in id ranges (F3).
- **D5:** receipt paths need a backtick/comma/paren boundary (trailing sentence period is absorbed).

## Residual risk

The declared residual stands and is the largest: clause_f binds a capture's form and digest line,
not its production — a hand-typed receipt+capture passes; the mitigation ("non-author closure
re-runs the print command") lives outside the counter and the counting command. Clause e counts
steps/locators, not step truth; clause c binds URL+digest+name, not scope-sentence truth (both
declared). No LSP server was available in this seat (no `lsp` device); all checks are text-level
plus executed repros.

## Tooling record

No tools installed or upgraded (none needed: python3, git, curl, tar, sed present). Scratch
`/fast/scratch/hyaku/mado-r47/RevC2Counter` (≈15 MB peak) removed at exit; evidence copied to the
seat dir first. The v0.14.3 tarball fetch is recorded with URL + sha256 in `pins/SHA256SUMS.txt`.

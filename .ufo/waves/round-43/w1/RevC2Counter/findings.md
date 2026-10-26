# RevC2Counter — forgeries admitted by PRED-C2-r43 (counter: `quality/counters/c2-r43-gkeep-entry.py`)

Method: every fixture below reuses the frozen control runner's own helpers (`base_files`,
`admitted`, `set_receipt`, `rep`, `score` in `.ufo/waves/round-43/ctl/run-c2-controls.py`),
with `TMPDIR=/fast/scratch/hyaku/mado-r43/RevC2Counter`, scored by the **unmodified frozen
counter** (`kind="real"`). Harness sanity: the runner's own control P admits (`admitted=1/1
verdict=TARGET_MET`, all clauses 1) — consistent with `receipts/ctl-c2.txt` (74/74). The
counter file itself was only read, never edited. Scratch was removed after the runs; fixture
repos were `mktemp` dirs under the seat scratch with `git -C` everywhere (run-6 rules).

Severity order. "admitted" = counter printed `admitted=1/1 verdict=TARGET_MET`, exit 0.

## F1 — MEDIUM: a held id's receipt is entirely unpinned; fully fabricated evidence admits

- Counter: `:416-419` — `pin_ok = True` unconditionally; only `if i in new_ids` is the
  receipt checked against `PINS` (`:418-419`). A held id (present in the BASE registry,
  e.g. S050) may gate ANY >=256-byte regular file under `fetch/`.
- Contract: docstring residual (lines ~80-82) declares "a held id's receipt is not pinned" —
  the demonstration below is the maximal exploit of that residual: bytes, quote and claim all
  fabricated, none anchored to anything the L1 fetched.
- Fixture R1 (admitted): S050's receipt replaced with a fabricated sentence — "The engine
  matches classes with Python re unanchored." + filler — and the entry claim line replaced by
  `**OBS** S050 the engine matches classes with Python re unanchored (S050.txt:1).` The gate
  sha matches the invented bytes; the quote is word-bounded at line 1; no other clause notices.
  Counter: `admitted=1/1 verdict=TARGET_MET`, `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1`.
- Impact: the only channel that admits invented *evidence* (new-id forgeries are pinned out —
  see N2). A data commit could rest one cited row on a file no one ever fetched.
- Fix direction: pin held ids too — require the receipt sha to equal the sha the BASE tree
  records for that path (or extend `PINS` to held ids at registration time).

## F2 — MEDIUM: clause d's "no GATE S### line outside the section" is bypassable two ways

Docstring clause d (lines 36-38): "no `GATE S###` line sits outside that section".

- Bypass 1 (byte-identical duplicate): counter `:403-406` — `in_gate = set(glines)`; the
  outside-scan counts a `^GATE S\d` line only if `line not in in_gate`. A byte-identical copy
  of an in-section GATE line, placed after a later `## Notes` heading, is in `in_gate` and
  therefore never counted. Fixture R2 (admitted): duplicate S291 GATE line under `## Notes` →
  `admitted=1/1`, `d:1`.
- Bypass 2 (fenced decoy): `unfenced()` drops fenced lines from BOTH the section parse
  (`:396-399`, via `glines`) and the outside scan (`:404`), so any GATE-shaped line inside a
  fence anywhere in the lesson is invisible to every check. Fixture R2b (admitted):
  `GATE S291 receipt=.ufo/waves/round-43/fetch/S050.txt sha256=000…0 quote="invented decoy
  quote text"` inside a fence at lesson end → `admitted=1/1`, `d:1`.
- Impact: paperwork-integrity invariant is false — a reader sees a plausible gate line naming
  a wrong receipt/sha; the counter scores only the section's line, so the decoy cannot bind,
  but nothing rejects it. (The decoy cannot carry weight: `gates` parses `glines` only.)
- Fix direction: reject any `^GATE S\d` line outside the section, scanning the RAW lesson
  (not just `unfenced`), and drop the `in_gate` set-membership bypass (count duplicates).

## F3 — LOW-MED: locator accepts garbage after the line number (`file:42x`)

- Counter: `:490-493` — `hit` needs the literal substring `"%s:%d" % (base_name, at)` in the
  line AND `(?<![\w.-])%s:%d(?!\d)`; the lookahead blocks only digits, so any non-digit
  suffix passes. The separately computed `loc_ok` (`:488-489`) is dead code — assigned,
  never used (and uses the same weak regex, so wiring it in would not help).
- Contract: docstring clause g (lines 54-57): locator is `<receipt file name>:<N>` where N is
  the line — `Hyprland-Target.cpp:42x` is not `<N>`; the entry carries a corrupted locator.
- Fixture R3 (admitted): entry locator `(Hyprland-Target.cpp:42)` → `(Hyprland-Target.cpp:42x)`
  → `admitted=1/1`, `g:1`.
- Fix direction: extract the number — `(?<![\w.-])name:(\d+)(?!\d)` with captured digits == at
  and no following word character — and delete the dead `loc_ok`.

## F4 — LOW-MED: collapsed-whitespace junction mis-maps the quote's start line

- Counter: `:238-252` `collapse_with_lines` attributes the junction space inserted at a
  newline to the PREVIOUS line (`:245-246`, `lines.append(ln)` with the earlier `ln`). A Gate
  quote whose first char is that junction space (leading space in the quote) therefore maps to
  the line BEFORE the line its words are on.
- Contract: docstring clause g (lines 56-57): "N is the 1-based line of the receipt on which
  the quote starts". The quoted words sit on line 3; the counter computes 2 and admits the
  entry citing `:2`.
- Fixture R6b (admitted): S050 receipt = `pad…\ntailpad\nalpha beta gamma words\n` (>=256 B),
  gate quote `" alpha beta gamma"` (leading space), entry line
  `**OBS** S050 alpha beta gamma (S050.txt:2).` → `admitted=1/1`, `d:1 g:1`.
- Fix direction: define N as the line of the first WORD character of the match (skip leading
  junction spaces in `lines[]`), or attribute the junction space to the following line.

## F5 — LOW: `recheck:` values are prefix-matched; trailing junk admits (entry + registry)

- Counter: `RECHECK_RE` (`:110`) used via `.match` (prefix) in `recheck_ok` (`:211-218`);
  clause b uses it on the entry line value (`:364`), clause c on the registry cell (`:378`).
- Contract: docstring clause b (lines 26-27): exactly one `recheck:` which is "an ISO calendar
  date, `NNd` or `on-*`"; clause c (line 31): "a valid `recheck` cell".
- Fixtures (both admitted): R10 — entry line `recheck: 90d whatever junk` → `admitted=1/1`,
  `b:1`. R9 — registry recheck cell `90d and-never-recheck` → `admitted=1/1`, `c:1`.
  (`W07` `TBD` is killed only because no alternative matches the prefix.)
- Fix direction: `re.fullmatch` the stripped token in `recheck_ok` (both call sites inherit).

## F6 — LOW: the entry claim line may carry the gate quote mid-word

- Counter: `:490` — `q in l` is a plain substring test; clause d's word-boundary rule applies
  only to the receipt, not to the entry line.
- Contract: docstring clause g (lines 54-55): the line "carries its Gate quote" — satisfied by
  any substring, including a mid-word fragment of a garbled claim.
- Fixture R5 (admitted): S293's entry line replaced by `**OBS** S293 Xm_box = box;Y garbled
  claim (Hyprland-Target.cpp:42).` → `admitted=1/1`, `g:1`.
- Fix direction: apply the same word-boundary test to `q` inside `l` that clause d applies to
  the receipt.

## F7 — LOW: locator inside a longer path admits

- Counter: `:493` — lookbehind `(?<![\w.-])` permits `/`, so `archive/deep/Hyprland-Target.cpp:42`
  satisfies the locator check for receipt `Hyprland-Target.cpp`.
- Contract: docstring clause g (line 55): the locator is `<receipt file name>:<N>` — a longer
  path is not the file name. Content binding is unaffected (quote+sha already pin the
  receipt), so this is a citation-hygiene defect.
- Fixture R4 (admitted): locator prefixed with `archive/deep/` → `admitted=1/1`, `g:1`.

## F8 — LOW: an own-work row's location can point elsewhere

- Counter: clause c for new ids checks only `"/" in loc and "." in loc` (`:388`); clause e
  (`:471-486` region) checks basename containment + uniqueness. `host-gkeep.conf` is a
  substring of `host-gkeep.conf.bak`, so `elsewhere/host-gkeep.conf.bak` passes both.
- Impact: the registry cell that documents where the pinned own-work artifact lives is
  unverified against the gated receipt's actual path; the census itself is safe (clause h
  reads the gated receipts, not the locations).
- Fixture R7 (admitted): S297 row location `…/fetch/host-gkeep.conf` →
  `elsewhere/host-gkeep.conf.bak` → `admitted=1/1`, `e:1`.
- Fix direction: for own-work rows require the location's last component to EQUAL the gated
  receipt's file name.

## Verified negatives (attempted, rejected — honest checks)

- N1 duplicate `recheck:` line inside the window → `b:0`, rejected (`hv` requires exactly one).
- N2 one-byte edit of the pinned `host-gkeep.conf` (+ matching gate) → `d:0 h:0`, rejected:
  new-id pins bind byte-exact; the census recomputation dies with them.
- R8 `..` traversal in a Gate receipt path (`…/fetch/../fetch/S050.txt`) → git refuses to
  resolve `..` in `rev:path` (`show`/`ls-tree` return nothing) → `d:0`, rejected; no escape
  from `fetch/` via the Gate path.
- R11 `recheck: on-2027-01-01` → rejected (`on-[a-z-]+` rejects digits).
- Census "trivial total" hint: no forgery available. The three census values are recomputed
  from the three pinned own-work receipts (`:284-337`) and matched verbatim; `total=4
  floating=0 gkeep=0` is forced by the pinned bytes, which N2 shows cannot be edited.
- `rxc.fullmatch` vs the host's RE2: for the pinned RX `^(org.omarchy.gkeep)$` (anchor, group,
  literals) Python `fullmatch` ≡ `RE2::FullMatch`; the general divergence remains a declared
  residual and was not further probed.

## Residual risk and verification gaps

- Quote-to-claim binding is outside the counter's reach (declared: it is the non-author
  closure's job). F1 shows the maximal form — fabricated bytes *and* fabricated claim; the F1
  fix narrows forgeries to real bytes at true locators.
- HTML-receipt locators unchecked (declared residual; `looks_html` inspects the first 4096
  bytes) — not re-tested here.
- Only the named edge families were fuzzed; registry row parsing beyond clause c's named
  checks, and `norm()`'s entity handling for HTML receipts, are untested.
- All fixtures ran against the worktree copy of the frozen counter via the control runner's
  `score()`; the counter, runner, registration and fetch receipts were never written.
- No tools were installed (none needed).

Report: .ufo/waves/round-43/w1/RevC2Counter.md

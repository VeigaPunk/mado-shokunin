# ScoutQualityCriteria — w2 falsify audit of proposed QUALITY 96-100

Seat: `ScoutQualityCriteria` (critic, leaf, policy v1). Wave w2, round 48, base `579f694b`.
Date: 2026-10-26. No installs, no lane/counter/predicate edits, no git/jj mutation.
Scratch: `/fast/scratch/hyaku/mado-r48/ScoutQualityCriteria` (created, bounded `ulimit -f 2048` on every writer shell, cleaned on return). Largest output file produced: `check99-100-rerun.txt`, 2,848 bytes (2.8 KB) — recorded per the seat bound. Seat evidence: `.ufo/waves/round-48/w2/ScoutQualityCriteria/` (`attacks.txt`, `check96-rerun.txt`, `check97-rerun.txt`, `check98-rerun.txt`, `check99-100-rerun.txt`, `check77-scope.txt`).

Axes named for this audit: **calibration** (is each proposed criterion a new grounded row, not a duplicate), **operability** (does the named instrument discriminate red from green on the bytes that will commit), **coverage** (do the criterion's own claims and receipts hold), **discernment** (false-pass vs declared tradeoff).

Method. Read `claims.md`, `registration.md`, `corpus/QUALITY.md` (proposed rows 96-100 are working-tree candidate bytes), the five instruments `.ufo/waves/round-48/w1/ScrMistakes/check{96..100}.py`, the w1 receipts, and `corpus/lessons/round-48.md` (live; carries `## Mistakes` at :230 and rows M48-1..M48-8 at :232-246). Re-ran every advertised red/green pair verbatim (seat evidence `check*-rerun.txt`). Ran a false-pass battery against each instrument (`attacks.txt`). Scanned criteria 1-95 with one regex per proposal class to find nearest rows (results below; all five classes absent from 1-95). Verified grounding citations resolve (M48-1..M48-5 exist; `round-47-verifier-spotcheck.md` D1 at :126, D3 at :136; M46-6 at `round-46.md:191`; M47-7 at `round-47.md:189`).

Revisions used: r47 freeze `d7527d608ad2b2e3cc398fdde34db7947b254a1a`, r47 tip `d40189c924e01dc1cbe290474eb4256d343590d4` (one mistyped variant `...4345904` returns "Needed a single revision" — the correct tip ends `590d4`; all reruns below use the correct hash).

## Verdict summary

| Criterion | Nearest existing row | Duplicate? | Red/green reproduces | False-pass / defect found | Audit verdict |
|---|---|---|---|---|---|
| 96 landed-contract-not-narrower | none; adjacent 61/64 (freeze binding), 52 (route gap forward) | no (grep class absent from 1-95) | yes on r47 bytes; **errors rc=2 on the r48 candidate tool** | yes — three (D1/D2/D3 below) | **Admit with fixes** |
| 97 receipted state numbers | 69 (extends) | no — proven live (69 passes while 97 fails, same bytes) | yes | yes — one evasion (low/mod) | Admit with note |
| 98 finding seats routed by name | 90 (routed-defect identity/age), 52 | no (grep class absent from 1-95) | yes | yes — two (D4/D5 below) | Admit with note |
| 99 corpus-to-corpus locator | 77 (extends) | no — proven live (77 silently skips the corpus locator) | yes | no new; two residuals | Admit |
| 100 dispatch-enforced scratch bound | 31, 34 (both measurement-side) | no (grep class absent from 1-95) | yes; r48 w2 spec itself reads OK | yes — one (low/mod) | Admit with note |

## Criterion 96 — landed contract vs frozen reference

Nearest row: none. Criteria 61/64 bind the freeze document (commands run, paths exist); 52 routes an inherited defect forward; none compares the *delivered* contract text against the *frozen* one. My grep over criteria 1-95 for `narrow|landed contract|frozen reference|out-of-contract list` matches no row; the w1 `near-duplicates.txt` receipt independently records the same.

Red/green on the bytes w1 used: reproduces exactly. `check96.py --frozen-rev d7527d60 --frozen .ufo/waves/round-47/l1-draft/mado-terminal.py --landed <HEAD-committed tools/mado-terminal.py>` prints `frozen=6 landed=9 added=3 unregistered=3 removed=0 verdict=NARROWED` rc 1; with `controls/registered-96.txt` → `verdict=OK` rc 0 (`attacks.txt` A1). Green-2 (frozen scored as its own landed) reproduces in `check96-rerun.txt`.

Defects found:

- **D1 (blocking, candidate bytes).** The candidate tool bytes — working tree `tools/mado-terminal.py`, sha256 `1dfde36c…`, byte-equal to `.ufo/waves/round-48/l1-draft/mado-terminal.py` and modified relative to the freeze commit `3e6c848a` — renamed the contract heading from `Also out of contract:` to `Out of contract:` and dropped the `On these the tool …` terminator sentence. `check96.py` on those bytes prints `LANDED-NO-LIST … rc=2` (`attacks.txt` A2). Restoring only the heading makes it worse: without the terminator the parser consumes the whole file as the list (`landed=175`, phony `NARROWED`). The instrument is bound to the r47 docstring shape; **criterion 96 cannot be scored on the round it is proposed in**, because the r48 freeze pair (l1-draft @ `3e6c848a` also says `Out of contract:`) is unparseable on both sides. The advertised "shown able to fail" holds only for r47-format bytes.
- **D2 (false pass vs the criterion's own title).** Deletion-only narrowing passes. A landed file equal to the frozen list minus `-h/--help` and `file names … locale` prints `REMOVED` lines but `added=0 removed=2 verdict=OK` rc 0 (`attacks.txt` A3). The criterion is titled "not narrower than the frozen reference"; a removed class is a narrowing. The r48 candidate itself dropped `HOME unset` and `symlink loops` from the out-of-contract list (HOME unset moved in-contract) — invisible to the verdict even when parseable.
- **D3 (weak registration).** A file containing only the three-word heads (`Erratum: home unset; a fifo named; symlink loops.`) registers the entire delta → `verdict=OK` (`attacks.txt` A4). The criterion says "an appended erratum naming it"; three-word fragments technically satisfy the instrument's substring rule.

Cross-cutting: no committed erratum anywhere in `.ufo/waves/round-48/` registers the r47→r48 out-of-contract delta (new classes: newline names, ACL/security xattrs, mtime six-month boundary, ls environment variables — grep of `registration.md` finds none of them). The r48 registration re-freezes the contract but does not name these exclusions; the w1 green used a seat control file, not a committed erratum.

Smallest safe correction: make the verdict fail when `removed>0` too (or retitle the criterion to cover additions only, which contradicts its mining note M48-1: "the narrowing is that the scored contract no longer describes the artifact"), and state the parser's required markers (`Also out of contract:` … `On these the tool`) in the criterion text so future docstring edits keep the instrument scoreable — or have the L1 keep the candidate docstring's list markers stable before the data commit.

## Criterion 97 — receipted state numbers (extends 69)

Nearest row: 69. Non-duplicate evidence is live, not asserted: on the r47 report `python3 -I .ufo/waves/round-41/w1/ScrQualityCriteria/check69.py --rev d40189c9 … --text` prints `PASS 1/1` rc 0 while `check97.py` on the same bytes prints `tokens=11 missing=1 verdict=UNRECEIPTED` rc 1 (missing token `findings=128`) — both reproduced in `check97-rerun.txt`. check69's docstring confirms it extracts only revision tokens (`rev=<hex>`, `rev <hex>`, `at <hex>`). Green (fixed report → `missing=0 verdict=OK` rc 0) reproduces. Grounding M48-2's fix receipts exist (`w1/ExecD2Receipt/receipts/session-material-{579f694b,60edb66e,d40189c9}.txt`, each carrying the corrected numbers).

False-pass found (low/mod): token regex `(?<![A-Za-z0-9_])[a-z_]+=[0-9]…` only reads lowercase keys. A report stating `fixtures=190/190` (receipted) alongside `Findings=128` (unreceipted, capital F) reads `tokens=1 missing=0 verdict=OK` rc 0 — the unreceipted count passes (`attacks.txt` C). `NO-NUMBERS` fails closed (rc 1), so a report with no lowercase tokens at all is caught.

Smallest safe correction: either case-fold the key class, or add one sentence to the criterion naming the token form it binds (`lowercase <key>=<number>`), matching how criterion 75 binds its digit classes.

## Criterion 98 — finding seats routed by name

Nearest rows: 90 (routed defects keep identity + age in the lesson) and 52 (sweep routes a gap forward). Neither requires a *wave seat's* finding to be routed by the seat's name in the round report or lesson; my grep for `blind spot|coverage hole|finding seat|unrouted|routed by name` over criteria 1-95 matches no row. Red reproduces: r47 w2 reads `finding_seats=7 unrouted=4 verdict=UNROUTED` rc 1, w1 `unrouted=1` rc 1; green (routed report) reads `unrouted=0 verdict=OK` rc 0 (`check98-rerun.txt`). Seat-name blind spot is declared in the criterion text.

False-passes found:

- **D4 (routing by roster).** Routing is any occurrence of the seat stem in report or lesson text — no disposition required. A bare roster naming all seven finding seats flips every one to `ROUTED` and yields `unrouted=0 verdict=OK` rc 0 with zero disposition lines (`attacks.txt` B-complete). The criterion text requires "one line for that seat with its disposition (fixed, routed with an age, rejected with a reason)".
- **D5 (keyword-only detection).** A seat report stating a real blind spot without the six trigger phrases or a bare `| survived |` row ("The counter cannot see readdir order at all; a sorted walk scores identical fixtures differently and no clause notices.") is not counted as a finding seat at all: `finding_seats=0 unrouted=0 verdict=OK` (`attacks.txt` B2). The criterion declares the seat-name limit but not the keyword-detection limit.

Provenance note: `--seats` is globbed from disk while `--lesson` is read from `--rev`; scoring a revision whose seat set differs from disk mixes channels.

**Self-reference for the L1.** This report quotes the phrases "blind spot" and "coverage hole" (above, describing the criterion). When `check98.py` is run over the round-48 w2 seat dir, `ScoutQualityCriteria` will count as a finding seat. Route it by name in the round-48 report or lesson (disposition: findings reported here, all routed to this audit) or exclude the audit seat — otherwise the round trips its own new criterion.

Smallest safe correction: declare the keyword-detection limit beside the seat-name limit (as 98 already does for names), and tighten routing to require the stem within one line of a disposition word (`fixed|routed|rejected|disposition`) — or accept D4 as the price of the declared name-based detection.

## Criterion 99 — corpus-to-corpus locator (extends 77)

Nearest row: 77. Non-duplicate evidence is live: on the r47 entry `quality/check-locators.py --fetch .ufo/waves/round-47/fetch` never prints line 95's `terminal-route-r17.md:150-151` locator — `terminal-route-r17.md` is not a fetch name, so it is silently skipped (`check77-scope.txt`; the tool's own docstring: "Tokens whose name does not resolve are not checked and are not printed"). Red reproduces: `checked=4 violations=4` rc 1 (one `UNK-HEAD-CUT`, three `AMBIGUOUS README.md`); green (fixed entry) `checked=7 violations=0` rc 0 (`check99-100-rerun.txt`). The candidate r48 entry itself passes its own new criterion: `check99.py --citing l1-draft/xkb-keymap-compile-r48.md --citing-text` reads `locators=3 checked=3 violations=0 verdict=OK` — its README locator is qualified (`corpus/README.md:112`), resolving uniquely.

Receipt inaccuracy (coverage finding, not an instrument defect): the w1 `receipts/d4-locator.txt` records criterion 77's instrument on this entry as `CHECK_LOCATORS: locators=0 miss=0 rc=0`. Re-run on the committed bytes at `d40189c9` it prints `locators=7 miss=3` rc 1 (`check77-scope.txt`): 77 resolves the unqualified `README.md` to the *fetch* copy by basename and mis-checks the author's intent. The criterion 99 text itself is accurate ("reads only names that exist in the `--fetch` directory"); only the supporting receipt overstates. The substantive gap 99 closes stands either way: 77 cannot see ambiguity (three README.md candidates) and cannot see the UNK-head-cut at all.

Residuals (both acceptable, previously undisclosed): (a) the `[UNK]` rule keys on the literal `[UNK]` in the citing line — a paraphrased restatement of an UNK item cites anywhere without the anchor check; (b) locator tokens with whitespace (`README.md : 218`) evade `TOK`. Both are evasions in the fail-open direction only when no other locator fires; low severity.

Verdict: admit as written; fix the d4 receipt's `locators=0` sentence (receipt repair, not predicate).

## Criterion 100 — dispatch-enforced scratch bound

Nearest rows: 31 (no-harm bounded-resource evidence) and 34 (scratch measurement same-path rule) — both measurement-side; neither requires the *dispatch* to carry the enforcing command. Grep for `ulimit|RLIMIT|size-cap|max_file_bytes|scratch bound` over criteria 1-95 matches no row. Red reproduces on both r47 and r48 w1 specs (`enforced=0 prose=4 verdict=PROSE-ONLY` rc 1); green (`spec-100-capped.json`) `enforced=1 verdict=OK` rc 0 (`check99-100-rerun.txt`). This wave's own dispatch now satisfies it: `check100.py --spec .ufo/waves/round-48/w2-spec.json` reads `enforced=49 … verdict=OK` (`attacks.txt` D) — the class is closed for w2, matching M48-5's fix note.

False-pass found (low/mod): any occurrence of the command pattern counts, even negated or illustrative — a spec containing "do not enforce ulimit -f 2048 ever" prints `ENFORCED … ulimit -f 2048` and `verdict=OK` (`attacks.txt` F1). Same class applies to the `max_file_bytes=`/`--size-cap` patterns.

Smallest safe correction: none required for admission (the check binds the *presence* of the cap command in the dispatch, and a dispatch that mentions the cap while forbidding it is adversarial beyond the mined mistake M47-7); if tightened, require the cap pattern outside a negation window ("do not|never|no " within N chars).

## Unprovable proposals

1. **Criterion 96 on the round-48 candidate bytes is unprovable as frozen**: both sides of the r48 freeze pair lack the parser markers, so `check96` exits rc 2 with no verdict. The w1 demonstration holds only for r47-format bytes. This is the one proposal whose instrument cannot currently score its own round's deliverable.
2. **Criterion 98's green for round 48 is unprovable yet**: the real round-48 report/lesson do not exist at audit time; the demonstrated green is the synthetic `controls/report-98-routed.md`.
3. All other advertised red/green pairs and the five "nearest row absent" claims are reproduced or verified live in this seat's evidence files.

## Handoff

- Fixes the L1 should land before the data commit if 96 is to bind this round: keep the candidate tool docstring's contract-list markers parseable by `check96.py` (or append the registering erratum naming each new out-of-contract class — none exists in the tree today), and decide whether removals narrow (criterion title says yes, instrument says no).
- Receipt repair: `w1/ScrMistakes/receipts/d4-locator.txt`'s "reads 0 locators" sentence does not reproduce; correct it to the recorded `locators=7 miss=3` (or re-run and re-record).
- Route `ScoutQualityCriteria` by name when scoring round-48 w2 with `check98` (see self-reference above).
- Checks I did not run (named, not silently skipped): the frozen C1/C2 counters themselves (sibling seats own those), `check97`/`check98` over round-48 w1 reports, and any live host probe. No pacman, no installs, no PATH writes; host untouched.

# ExecCounterC1R50 — PRED-C1-r50 counter draft (round 50, w1)

Seat: `.ufo/waves/round-50/w1/ExecCounterC1R50/`. Scope: port
`quality/counters/c2-r49-bind-entry.py` (PRED-C2-r49) to round 50 as **PRED-C1-r50**, re-pointed to base
`8ae47b957034ae21012bbf09173cca2c48be345e`, entry `corpus/knowledge/hyprland-bind-key-match-r50.md`, lesson
`corpus/lessons/round-50.md`, pins `.ufo/waves/round-50/fetch/`, receipts `.ufo/waves/round-50/receipts/`; then run it at
the base and against a scratch fixture that commits the round-49 candidate artifacts at the round-50 paths, and report every
failing clause so the scribe seats know what the entry, rows, README row and lesson must satisfy.

**Verdict.** Port landed and runnable. Base run: `clause=a entry_absent`, `verdict=TARGET_MISSED` (rc 1) — the round-50
base carries no entry, as required. Fixture (artifacts at round-50 paths + index row + lesson Gate):
`clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1` → `TARGET_MET`, rc 0. Three changes beyond the path re-point,
all declared below: **F1** (clause d numeric-band false positive, repaired), **F2** (clause f/r receipt name pinned to
`binds-live-r50.txt`), **F5** (the no-pins short-circuit now reports the clause b it computed instead of a literal `a:1 c:0`).

## Deliverables (all exist; sha256 shown)

| path | notes |
|---|---|
| `.ufo/waves/round-50/w1/ExecCounterC1R50/c1-r50-bind-entry.py` | the draft counter, `17ad31c1d9bd9571b499f9d9bce7ee0066ec2f154d7af68c352f16399f068908`, 1305 L, executed in every run listed below |
| `.ufo/waves/round-50/w1/ExecCounterC1R50/port-diff.txt` | `diff -u quality/counters/c2-r49-bind-entry.py <draft>` (188 diff lines, 13 hunks) |
| `.ufo/waves/round-50/w1/ExecCounterC1R50/port-changes.md` | table of every changed line + reason + the unchanged-by-design list |
| `.ufo/waves/round-50/w1/ExecCounterC1R50/fixture-build.py` | rebuilds the fixture (two commits, scratch clone, toplevel asserted) |
| `.ufo/waves/round-50/w1/ExecCounterC1R50/fixture-rerun.py` | rebuilds the fixture, adds the control revisions, re-runs every case and every clause-kill mutant — copy both scripts to a scratch dir first; the fixture tree is `<script dir>/fx`, never inside the lane |
| `.ufo/waves/round-50/w1/ExecCounterC1R50/receipts/` | `base-run.txt`, `fixture-c1-prefix.txt`, `fixture-c1.txt`, `fixture-c2-prefix.txt`, `fixture-c2.txt`, `control-no-pins.txt`, `mutant-c-nopins.txt`, `mutant-m1-quote-word.txt`, `mutant-m2-receipt-name.txt`, `mutant-m3-step-no-quote.txt`, `mutant-m4-topic-line.txt`, `mutant-m5-no-limits.txt`, `mutant-m6-held-row-moved.txt`, `old-ground-r49-terms.txt`, `tmpdir-refused.txt`, `ground-grep.txt`, `fixture-identity.txt` |

Nothing outside this seat dir was written; no lane file was edited; no tool was installed or upgraded.

## Re-point, and the three things that had to change besides paths

`port-changes.md` lists all 18 line regions. Re-pointed: `PRED`, `ENTRY`, `LESSON`, `FETCH`, `RECEIPTS`, `BASE_DEFAULT`,
plus the docstring's copy of each. Kept byte-identical in meaning: `HELD=("S319",)`, `HELD_FETCH` (round-46), `MIN_ID=352`,
`MIN_SOURCES`, receipt size bounds, `OPENED=2026-10-27`, the pinned commit/version, `FORMS`, `TAGS`, `TOPICS`/clause j, and
every clause body except the two declared changes. `MIN_ID=352` is still right: at the base the registry tops at S351
(`git show 8ae47b95:corpus/SOURCES.md | grep -oE '^ {0,3}\| *S[0-9]{3,}' | tail -1` → `| S351`).

**GROUND terms (clause i).** Clause i requires each term to return no match under `corpus/` at BASE. At the new base the
round-49 closure text now quotes two of the four:
`git grep -F -q -e <term> 8ae47b95 -- corpus` (`receipts/ground-grep.txt`):

| term | rc at BASE | where | decision |
|---|---|---|---|
| `xkb_state_key_get_one_sym` | 0 (present) | `corpus/lessons/round-49-verifier-spotcheck.md` | **replaced** |
| `m_xkbSymState` | 0 (present) | `corpus/lessons/round-49-verifier-spotcheck.md`, `corpus/lessons/round-49.md` | **replaced** |
| `keysym_to_name` | 1 | — | kept |
| `xkb_keysym_get_name` | 1 | — | kept |
| `xkb_state_key_get_layout` | 1 | — | **new**: the API step 8 of the entry already quotes, `xkb_state_key_get_layout(state, kc)` at `xkbcommon-state.c:1345` (same read path: layout → level → keysym) |
| `m_modifiersState` | 1 | — | **new**: the keyboard's modifier state the mask is built from, `m_modifiersState.depressed \| m_modifiersState.latched` at `Hyprland-IKeyboard.cpp:360` |

Why these two: clause i is a novelty/vacuity guard ("the ground is new"), not a spelling test. Keeping the old pair would make
the clause fail at BASE for text the round-49 closure itself wrote, unrelated to the round-50 entry. Both replacements are
source-derived names of the same mechanism, appear in the round-49 candidate entry (1 and 2 occurrences) so a faithful port
keeps them, and both live in pins the entry already cites. Evidence that the swap is load-bearing: the same draft with the
round-49 tuple restored fails only clause i —
`clause=i ground_present_at_base=xkb_state_key_get_one_sym rc=0` and `…=m_xkbSymState rc=0`
(`receipts/old-ground-r49-terms.txt`), `verdict=TARGET_MISSED`.

## Runs (all commands run with `TMPDIR` under the seat scratch, `ulimit -f 65536`)

1. **Base, no entry** — `python3 -I c1-r50-bind-entry.py --repo <lane> --rev 8ae47b95…`
   → `clause=a entry_absent` / `clauses=a:0 … verdict=TARGET_MISSED rev=8ae47b95…`, rc 1 (`receipts/base-run.txt`). The
   counter stops at clause a and never claims more.
2. **Fixture c1**: round-49 candidate bytes at round-50 paths only — 15 fetch pins, `binds-live-r50.txt` +
   `how-to-type-slash-br-r50.txt` receipts, the entry, and rows S352-S363 appended to `corpus/SOURCES.md`, all with
   `round-49`→`round-50` / `r49`→`r50` / `Round: 49`→`Round: 50`. Result
   `clauses=a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:0 j:1 r:1`, failures:
   `clause=b readme_rows=0`, `clause=i lesson_missing=corpus/lessons/round-50.md`,
   `clause=i row_used_by_not_new=S357:[…]`, `…=S358:[…]` (`receipts/fixture-c1.txt`, rev `25da5754`).
3. **Fixture c2**: adds one `corpus/README.md` index row (three cells, covers `S352-S363`) and a round-50 lesson `## Gate`
   with 12 `**S### admit**` lines → `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1` /
   `verdict=TARGET_MET`, rc 0 (`receipts/fixture-c2.txt`, rev `9cf35395`).
4. **Fixture identity** (`receipts/fixture-identity.txt`): `toplevel: …/fx` = `expected: …/fx`, base `8ae47b95…`, the fixture
   revs and the counter's sha256; the clone is `git clone -q --shared <lane> fx` then `git -C fx checkout --detach 8ae47b95…`;
   every commit is made by the fixture identity in that clone only. Each receipt names the revision it scored.
5. **TMPDIR refusal still bites** — `TMPDIR=/tmp …` → `PRED-C1-r50 SETUP TMPDIR under /tmp refused: /tmp`, rc 2
   (`receipts/tmpdir-refused.txt`).

### Clause kills — every clause has a fixture that turns it to 0

| clause | fixture (receipt) | vector | the diagnostic that fires |
|---|---|---|---|
| a | base, no entry (`base-run.txt`) | `a:0` | `clause=a entry_absent` |
| b | artifacts without the index row (`fixture-c1.txt`) | `b:0` | `clause=b readme_rows=0` |
| c | rows kept, fetch pins removed (`mutant-c-nopins.txt`) | `a:1 b:1 c:0` | `clause=c fetch_pins=0 under .ufo/waves/round-50/fetch/` |
| d | one word of a step quote changed (`mutant-m1-quote-word.txt`) | `d:0` | `clause=d quote_not_in_pin line=62 pin=Hyprland-KeybindManager.cpp` |
| d,j | topic quote's locator moved 369→370 (`mutant-m4-topic-line.txt`) | `d:0 j:0` | `clause=d quote_out_of_range line=62 …`, `clause=j topic=state unanswered lines=[369]` |
| e | an 18th numbered step with no quote (`mutant-m3-step-no-quote.txt`) | `e:0` | `clause=e step_without_verified_quote line=75`, `steps=18 verified_steps=17` |
| f,r | entry cites another receipt (`mutant-m2-receipt-name.txt`) | `f:0 r:0` | `clause=f receipt_name=[…] want=^binds-live-r50\.txt$`, `clause=r no_receipt_found` |
| g | held S319 row edited at REV (`mutant-m6-held-row-moved.txt`) | `g:0` | `clause=g held_row_moved=S319` |
| h | `## Limits` heading renamed (`mutant-m5-no-limits.txt`) | `h:0` | `clause=h limits=0 bullets=0 scoped=0` |
| i | round-49 GROUND tuple restored (`old-ground-r49-terms.txt`) | `i:0` | `clause=i ground_present_at_base=… rc=0` (twice) |
| — | entry alone, no pins, no rows (`control-no-pins.txt`) | `a:1 b:0 c:0` | `clause=b readme_rows=0` + `clause=c fetch_pins=0`; d..r unreached (F5) |

Two notes from building the mutants. (i) The first clause-e mutant removed one of the several quotes in step 6 and the counter
still passed (`TARGET_MET`): clause e demands one verified quote **per step**, so that mutant was equivalent, not a survivor —
the per-step rule is what the counter says it checks. (ii) Clause j cannot fail without d also failing, because j re-verifies a
quote at the locator it needs: m4 kills both and prints the uncovered topic line, which is the intended coupling.


## What the scribe seats must satisfy (measured on the round-49 candidate bytes, at the round-50 paths)

- **Entry head**: 10 `source:` lines in the first 20 unfenced lines, ids ≥ S352; exactly one `verified-at: 2026-10-27` and one
  `recheck: on-release`; no `source:`/`verified-at:`/`recheck:` line outside the head window. Every `S###` token anywhere in
  the unfenced text must be a Registry row — the entry cites S357/S358 in prose, so those rows must be registered too.
- **Registry rows**: 11 cells each; `tier ∈ A/B/C`, non-empty kind, `status=mined`, `opened=2026-10-27`, a valid recheck
  (`on-release` / `90d` both pass), used-by naming the entry path. Name at least one `.ufo/waves/round-50/fetch/<pin>` and
  record a `sha256:` that matches those bytes; URLs must be commit/tag-pinned (`efb50993…`, `d1442aaa…`,
  `xkbcommon-1.13.2`) — a release-named page is refused. The held S319 URL may be cited, never re-registered.
- **`corpus/README.md`**: exactly one column-0 row `| \`knowledge/hyprland-bind-key-match-r50.md\` …` with three cells, no
  redirect word, naming no other knowledge file, and its S-tokens covering every head id (`S352-S363` worked).
- **`corpus/lessons/round-50.md`**: non-empty `## Gate` holding a `**S### admit**` line for **every** row new at REV
  (the fixture's 12 rows needed 12 admits), and each new row must be used by something new at REV — the entry path qualifies;
  S357/S358 carry `tools/mado-keysym.py, corpus/lessons/round-50.md`, so **the round-50 lesson must land in the same revision
  as those rows** or clause i fails with `row_used_by_not_new`.
- **Receipt**: `.ufo/waves/round-50/receipts/binds-live-r50.txt` — 100644, 512 B-256 KiB, absent at base, names
  `hyprctl binds -j`, carries no `"modmask"`/`"dispatcher"` JSON, states `Hyprland 0.56.2` beside `efb50993…`, exactly one
  `sha256:` digest, one bind total, one value per form (`named`/`code`/`mouse`/`switch`) summing to the total, and
  `input:resolve_binds_by_sym` as `int 0`/`set false`. The entry must repeat each of those values; clause r will also
  re-run `hyprctl binds -j` and require the digest to match byte-for-byte, so the receipt has to come from the same host state
  that exists when the counter runs.
- **Pins**: the round-50 `fetch/` dir must be populated this round (the base has it empty), and a pin whose sha256 a row
  records is the trust root.

## Findings for the L1 (freeze decisions)

- **F1 — clause d false positive, repaired in the draft** (`locators()` now skips a token with no `[a-z_]`). Round-49's
  entry carries `| modmask_histogram | 0:23, 1:2, … |`; PRED-C2-r49 read `0:23` as a locator, `resolve_pin("0")` matched the
  pin whose stem contains `0` (`binds-live-r49`, 17 lines) and failed with
  `clause=d locator_out_of_pin=0:23-23/17 line=118` (`receipts/fixture-c1-prefix.txt`, and identically on c2 before the fix: `receipts/fixture-c2-prefix.txt`).
  This is a counter defect, not an entry defect: no file is named `0`. Without the repair a faithful round-50 entry cannot
  pass clause d while keeping its histogram table; with it, 86 quotes verify and only quote/locator content decides. The L1
  may revert it — the pre-fix behaviour is receipted — but then clause d needs the entry to stop writing `N:M` bands.
- **F2 — clause f/r receipt name pinned** to `^binds-live-r50\.txt$`. Round-49 accepted any `<file>` under the receipts dir;
  the round-50 spec names the capture. This is a narrowing, declared: an entry that cites its capture under another name now
  fails clause f with a diagnostic listing every receipt name it cites.
- **F3 — the round-50 lesson is a prerequisite for rows S357/S358** (and for any row whose only consumer is a held path).
  Scribes must not commit the rows without the lesson.
- **F4 — the fixture's pins are round-49 bytes re-copied**; they only demonstrate the clause mechanics. The round-50 entry must
  commit pins fetched this round with their URLs and digests (the counter itself fetches nothing).
- **F5 — the no-pins short-circuit now reports what it evaluated** (`a:1 b:<computed> c:0` instead of a literal `a:1 c:0`).
  Raised by `w1/ExecControlsC1R50` from their 8/8 do-nothing control run against the earlier snapshot `3e2bf669…`: at
  `8ae47b95` the round-50 `fetch/` dir is empty, so any control run stops at clause c, and the old literal dropped the computed
  b — a control that failed b read as a c failure. The vector deliberately names only a, b, c: d..r were never reached, so
  nothing is claimed about them. This is the only difference between `3e2bf669…` and the final `17ad31c1…`; their 8/8
  `TARGET_MISSED` verdicts stand, only the printed vector on the no-pins path changes. They re-ran all 8 controls on
  `17ad31c1…` afterwards and reported 8/8 `TARGET_MISSED` with the intended vectors (`a:0` for BASE/OLDPATHS,
  `a:1 b:0 c:0` for STUB/HELD/NOLIVE/NOROWS/FORGEDQUOTE/BRANCHURL, with `clause=b readme_rows=0` / `clause=b ghost_ids` on the
  per-clause lines).
  Their independent probe on the frozen round-49 counter (candidate + 12 rows + receipt + index row + `**S### admit**` lines →
  a..r `1/1`) agrees with my fixture result on the port, so the clause set is not port-specific.
- Sentinel notice from `SentHostState` (R-SHS-3) applies to the keysym counter's tracer wrapper, not here: this counter runs
  no `strace`/`bwrap`, its only subprocesses are `git` and `/usr/bin/hyprctl`. Same caveat as round 49: `tmp_root()` refuses
  `/tmp` and an absent `TMPDIR` but does not refuse a scratch root under a home directory (the control seats point their scratch
  at `/fast/scratch`, never a home).

## Risks / residuals

- Clause r needs the live compositor socket (`XDG_RUNTIME_DIR`, `HYPRLAND_INSTANCE_SIGNATURE`) and a stable bind table; the
  fixture replay passed (`replay=ok sha=9a47199e2297 binds=192 forms=named:142,code:42,mouse:6,switch:2 resolve=0`) against
  the round-49 capture, so the host has not drifted since that capture — a later drift is a legitimate miss, by design.
- The counter's declared residuals (fetch copies are the trust root; a true quote can sit beside an unsupported claim; clause
  j checks the answering line, not the truth of the sentence) carry over unchanged from round 49.
- Untested by this seat: whether the frozen counter survives an adversarial entry written against it (that is w2's job), and
  whether the L1 keeps F1/F2/F5.
- Scratch: `/fast/scratch/hyaku/mado-r50/ExecCounterC1R50/` (376 MB measured with `du -sh`, fixture tree at 23,289 files,
  `ulimit -f 65536` on every writer shell), removed before this seat closed; every number above is copied into this seat's
  receipts.

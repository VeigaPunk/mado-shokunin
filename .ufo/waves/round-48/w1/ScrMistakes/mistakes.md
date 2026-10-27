# mado round 48 — w1 seat ScrMistakes: mined mistakes (draft rows M48-1..M48-5, criteria 96-100)

Seat: leaf (`policy v1`, BUILD). Lane `mado-shokunin`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Sources read:
`corpus/lessons/round-47-verifier-spotcheck.md` (§6 D1-D4), `corpus/lessons/round-47.md` `## Mistakes`
(M47-1..M47-10), `corpus/QUALITY.md` (criteria 1-95; 31, 34, 38-40, 49-52, 61, 64, 69, 77, 90, 93-95 read in full).
Nothing in this seat ran a counter, a gate, the resolver, `xkbcli` or any compositor verb; every observable below is a
read of committed bytes or of one of this seat's own instruments. Two host files are read outside the lane: the
round-47 report (`.ufo/reports/round-47/mado.md`, fleet, read-only) and nothing else.

Row format: `class` · evidence pointer · captured-by · fix · shown able to fail. Locators are emitted by
`verify-quotes.py` (`receipts/quote-check.txt`, 37/37 `OK`, 0 `DIFFER`) and every locator written here is a `LOC`
line of that receipt; `verify-quotes.py --doc` reads this file and fails on any locator the receipt does not carry.

## Rows

### M48-1 · class `contract-narrowing` (closure D1)

**Evidence.** The C1 contract was frozen as the docstring of `.ufo/waves/round-47/l1-draft/mado-terminal.py`
(blob `762d042c…`, at freeze `d7527d60`); its out-of-contract list names six classes
(`.ufo/waves/round-47/l1-draft/mado-terminal.py:84`). The delivered tool names nine
(`tools/mado-terminal.py:85`): it adds **HOME unset**, **a FIFO named like a desktop file in a later application
dir**, and **symlink loops**. The registration's own contract paragraph —
`.ufo/waves/round-47/registration.md:52`, which calls them
"the warm-cache path, `-h/--help`, an empty argv element (the script loops forever), XDG dirs holding glob characters
or quotes" — names none of the three either. `check96` on the two committed byte strings:
`frozen=6 landed=9 added=3 unregistered=3 removed=0 verdict=NARROWED` (`receipts/check96-run.txt`).

Two of the three are a *behaviour* delta, not a wording fix: the FIFO refusal exists only in the landed bytes
(`tools/mado-terminal.py:529`; the frozen bytes have no `S_ISFIFO` arm), so on that input the pin blocks reading the
FIFO and the tool exits 2 — the class the frozen predicate did not score. The third is text catching up with the
freeze: the frozen bytes already raise on HOME unset
(`.ufo/waves/round-47/l1-draft/mado-terminal.py:407` = `tools/mado-terminal.py:410`) and already guard a repeated
directory key, so the freeze under-declared what it had built, and the landed docstring declared it after the predicate
was fixed. `removed=0` means nothing was narrowed by deletion; the narrowing is that the scored contract no longer
describes the artifact.

**captured-by: none.** The freeze criteria bind the *freeze*, not the delta to the artifact: 61 (each command a
registration names runs) and 64 (every named path exists at the freeze) test the freeze document; 38/49 (composite
smoke at freeze) test that a leg is alive; 9 binds an audit verdict to a commit. No criterion compares the contract
text or item list of the delivered file with the one frozen.

**Fix.** Model HOME unset as the pin does (exit 1, empty stdout) so the class leaves the list; register the other two
classes in round 48's freeze or in an appended erratum, and keep the delta printed for the reader. `check96`
implements the exemption path: an added item counts as `ADDED-REGISTERED` when a named erratum carries its first three
words.

**Shown able to fail.** Failing input = the landed tool against the frozen reference:
`rc=1`, three `ADDED-UNREGISTERED` lines. Green the same command with `--registered controls/registered-96.txt`
(`rc=0`, three `ADDED-REGISTERED`), and green with the frozen file scored as its own landed file (`added=0`, `rc=0`)
— `receipts/check96-run.txt`.

### M48-2 · class `unreceipted-number` (closure D2)

**Evidence.** The round-47 report states the session-material gate's tip count as a measurement:
"the session-material gate reads `findings=128` at the tip (115 at base)"
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/mado.md:104`). No committed byte in the lane carries it:
`git grep -n 'findings=128' d40189c9` → rc 1, no line. Every `findings=` value in the round's receipts is one of
115, 136, 139, 84, 86, 88, 111, 78, 92 (`receipts/d2-report-number.txt`), and 136 alone lives in 13 tracked files —
so a receipted sentence was available and a different number was typed. `check97` over the report against every
round-47 receipt (`receipts=1598`) reads `tokens=11 missing=1 verdict=UNRECEIPTED`, and the one missing token is
`findings=128`.

The class is already registered as criterion 69 — `corpus/QUALITY.md:385`, "extract every revision token the report
writes in measurement form" — and
criterion 69's own instrument **passes the same report**: `PASS 1/1 cited revisions carried by committed receipts`,
because it reads only `rev=<hex>`-shaped tokens and `findings=128` is not one. That is why this row proposes an
extension (criterion 97) rather than a new class.

**captured-by: 69, blind to the shape.** 90/94 bind a *routed defect's* numbers to a ledger; 10 binds a count to
"`<n> — <command> <date>`"; none binds a report's state number in a detector's own vocabulary.

**Fix.** Commit the gate run at the tip revision (the number then exists as a receipt) or correct the sentence to a
receipted value; the report QC runs `check97` before the report is committed.

**Shown able to fail.** Failing input = the round-47 report as committed: `rc=1`, `missing=1`. Green = the same
report with `findings=128` corrected to `findings=136` (a receipted value): `tokens=11 missing=0 rc=0`
(`receipts/check97-run.txt`). Criterion 69 on the failing input: `rc=0 PASS` (`receipts/d2-report-number.txt`).

### M48-3 · class `routing` (closure D3, larger than the closure's instance)

**Evidence.** The w2 seat's finding — "clause f/x are blind to the readdir axis, so a tool that sorts directory
entries instead of reading the filesystem order passes all 190 fixtures"
(`.ufo/waves/round-47/w2/ExecC1Determinism.md:10`) — is named in neither the report nor the lesson:
`grep -c ExecC1Determinism` → `report=0 lesson=0`. The round-47 non-author closure had to route it itself
(`corpus/lessons/round-47-verifier-spotcheck.md:136`: "the readdir-order blind spot … is not routed in the report or
lesson"). `check98` over the round's own seat files shows the class is not one seat: of the 44 w2 seat reports, 7
state a blind spot, a coverage hole or a surviving mutant, and **4 are unrouted** —

| seat | finding token | report | lesson |
|---|---|---|---|
| `ExecC1Determinism` | `blind to` | 0 | 0 |
| `MutC1Counter` | `survived-mutant` (`drop the oracle-drift raise (lines 444-445)`, `.ufo/waves/round-47/w2/MutC1Counter.md:17`) | 0 | 0 |
| `MutC2Counter` | `coverage hole` ("Coverage holes (mutants no control kills — the counter can be weakened without any control noticing)", `.ufo/waves/round-47/w2/MutC2Counter.md:40`) | 0 | 0 |
| `RevengerCache` | `coverage gap` (no fixture seeds a cache file) | 0 | 0 |

The w1 scan adds one more of the same family: **the operability axis is blind to `tools/`**
(`.ufo/waves/round-47/w1/ExecAxisBase.md:71`), which is a calibration finding about the axis the round declares —
`report=0 lesson=0`. Routed for contrast: `MutC1Fixtures` (report 2, and M47-10), `MutTripwire` (report 1),
`RevSessionMarker` (lesson 1), `ExecIdGuard`/`ExecSessionMarker`/`ScrErrataCal` (lesson 1 each).

**captured-by: 52, for the wrong seat.** Criterion 52 — "A sweep that surfaces an inherited defect records it and
routes it forward" (`corpus/QUALITY.md:358`) — binds the *sweeping seat*; 90 ("Every routed defect keeps one identity
and an age", `corpus/QUALITY.md:454`) binds the identity of an item once routed; 93 binds a gate registry cell. None
binds the integrator: nothing requires a w2 finding to reach the report or the lesson, and the report's own
"Carried" list names only the items the integrator already chose.

**Fix.** Each finding seat gets one routing line (report or lesson) carrying the seat path and the finding's first
line, with a disposition (fixed / routed to round N / rejected with a reason); the round's QC runs `check98` before
the data commit. This is the same instrument shape as criterion 92 (produced set vs committed set), applied to the
produced *finding* set.

**Shown able to fail.** Failing input = the round's w2 seats against the report and lesson:
`CHECK98: seats=44 finding_seats=7 unrouted=4 verdict=UNROUTED`, rc 1 (w1: `finding_seats=4 unrouted=1`, rc 1).
Green = the same seats against the report with four routing lines added by name:
`unrouted=0 verdict=OK`, rc 0 (`receipts/check98-run.txt`).

### M48-4 · class `locator` (closure D4; recurrent since M46-6)

**Evidence.** The entry writes, at `corpus/knowledge/xdg-terminal-selection-r47.md:95`, that the `--dir=` question
"stays `[UNK]`" and cites `terminal-route-r17.md` lines 150-151, while the bullet that carries the item's head is at
`corpus/knowledge/terminal-route-r17.md:149`:
"- [UNK] Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` is valid at". The range therefore begins
mid-sentence, one line after the sentence start, and the cited text is the wrap, not the item.

Criterion 77 exists for locators — "the cited range must contain the fact's own identifier"
(`corpus/QUALITY.md:401`) — but its instrument is scoped to pinned receipts: "Tokens whose name does not resolve are
not checked" (`quality/check-locators.py:14`), and resolution is "a file name in the `--fetch DIR`"
(`quality/check-locators.py:123`). On this entry it prints `CHECK_LOCATORS: locators=0 miss=0`, rc 0 — a
corpus-to-corpus reference is never read. `check99` reads it: `locators=7 checked=4 violations=4 verdict=CUT`, rc 1.

The same scan finds a second shape in the same file: three locators written as bare `README.md:218`, `README.md:300-301`
and `README.md:179-180`, which resolve to three different files (lane `README.md` 14 lines, pinned
`.ufo/waves/round-47/fetch/README.md` 337 lines, `corpus/README.md`), so the citation is readable only through the
pin declaration at the entry's line 4 (`.ufo/waves/round-47/fetch/README.md`).

The class is older than this round: M46-6 recorded that "a range that contains the identifier is not a range that
carries the mechanism" (`corpus/lessons/round-46.md:196`) and said in its own row that criterion 77 cannot catch it —
captured-by **none** there, and the same residual is stated again in M46-11. Round 47's D4 is the third round of the
same class, in its cheapest form (a range that does not even contain the sentence's head).

**captured-by: 77, out of scope; M46-6 carried none.** The nearest instrument reads pinned receipts only, so the
corpus-to-corpus case has no detector.

**Fix.** Correct the range to `149-150` in the entry (an erratum line — the entry is landed data) and qualify the
three README locators with the pin path; `check99` is the check, with `--fetch` given, and rule B is the `[UNK]`
anchor rule.

**Shown able to fail.** Failing input = the entry as landed: `rc=1`, one `UNK-HEAD-CUT` naming the bullet at line 149
and three `AMBIGUOUS` lines. Green = the same entry with the range corrected to `149-150` and the README locators
qualified: `locators=7 checked=7 violations=0 verdict=OK`, rc 0 (`receipts/check99-run.txt`).

### M48-5 · class `provider` (M47-7: mined, but uncaptured)

**Evidence.** M47-7 **is** mined: it is the round-47 lesson's provider row
(`corpus/lessons/round-47.md:189`, "w1 seat ExecRefB's shell wrote … into a scratch file until it reached ~590 GB")
whose own text says `Captured-by: none (the wave context bounded scratch size in words only)`
(`corpus/lessons/round-47.md:191`). What did not happen is a criterion: the five criteria landed from that lesson cite
M47-1, M47-2, M47-3, M47-4/M47-5 and M47-6 (`corpus/QUALITY.md:468`, `:478`, `:488`, `:496`, `:504`), and
`grep -c 'M47-7' corpus/QUALITY.md` → 0. So the one mistake of the round with a live host consequence is the one the
QC step left uncaptured — the same shape as M47-6 being captured only after it recurred.

The gap is live this round, not historical: the only bound either wave states is a prose ceiling in the seat context
(round-47 and round-48 `w1-spec.json` both say "keep it under 2 GB"; round 48 adds "bound every loop and every write
… cap generated files at 1 MB"), and neither dispatch carries anything a shell executes (`grep -c ulimit` → 0 for
both). `check100` reads both as `enforced=0 prose=4 verdict=PROSE-ONLY`, rc 1. This seat's own budget is prose too —
stated plainly rather than counted as compliance.

**captured-by: none**, as M47-7 says; the nearest criteria are 31 (bounded resource evidence for a *detector's*
no-harm claim, `corpus/QUALITY.md:298`) and 34 (a scratch *measurement receipt*'s path/provenance,
`corpus/QUALITY.md:319`) — neither governs the writer of an unbounded stream.

**Fix.** The wave dispatch carries the limit command the seat runs (`ulimit -f <KB>` or an equivalent), and every seat
receipt records the largest file it produced, so the bound is an observable rather than a sentence.

**Shown able to fail.** Failing inputs = the round-47 spec and this round's own spec: both `PROSE-ONLY`, rc 1.
Green = a dispatch carrying `ulimit -f 1024`: `enforced=1 verdict=OK`, rc 0 (`receipts/check100-run.txt`).

## Proposed criteria (draft; the L1 freezes)

### 96. A landed contract is not narrower than the frozen reference it was registered against

> A round that freezes a tool's contract (docstring, registration paragraph) and delivers the tool later commits the
> delta between the frozen out-of-contract list and the delivered one; an added class is either modelled as the
> reference behaves or registered in an appended erratum naming it, and the delta is read against that erratum before
> the data commit. Check: `python3 -I .ufo/waves/round-48/w1/ScrMistakes/check96.py --repo . --frozen-rev REV
> --frozen <path> --landed <path> [--registered <file>]` prints one `ADDED-*` line per delta item and
> `CHECK96: … verdict=NARROWED|OK`. Shown able to fail: `verdict=NARROWED added=3 unregistered=3`, rc 1, on
> `tools/mado-terminal.py` against the freeze blob; `verdict=OK`, rc 0, with the erratum
> (`receipts/check96-run.txt`). (lesson: lessons/round-48.md#mistakes M48-1; outside
> `lessons/round-47-verifier-spotcheck.md` D1)

### 97. A report's state number in a detector's own vocabulary carries a committed receipt (extends 69)

> Criterion 69 reads revision tokens only, so a number a report states as a count (`findings=128`, `files=18371`,
> `fixtures=190/190`) is evidence only when the literal token appears in a committed receipt at the report's
> revision; a number that exists only in the report is corrected, not decorated. Check: `python3 -I
> .ufo/waves/round-48/w1/ScrMistakes/check97.py --repo . --rev REV --report <path> --receipts <dir> [--text]` prints
> one `MISSING` line per unreceipted token and `CHECK97: tokens= missing= verdict=`. Shown able to fail: the round-47
> report reads `tokens=11 missing=1 verdict=UNRECEIPTED`, rc 1 (the missing token is `findings=128`), while criterion
> 69's own instrument reads `PASS 1/1`, rc 0, on the same bytes; `missing=0`, rc 0, on the same report with the number
> corrected to a receipted value (`receipts/check97-run.txt`, `receipts/d2-report-number.txt`). (lesson:
> lessons/round-48.md#mistakes M48-2; extends 69)

### 98. Every seat that reports a frozen-instrument blind spot is routed by name

> A w1/w2 seat that reports a blind spot, a coverage hole or a surviving mutant names a gap in the frozen instrument;
> the round's report or lesson carries one line for that seat with its disposition (fixed, routed with an age,
> rejected with a reason), and a finding seat named in neither is unrouted. Check: `python3 -I
> .ufo/waves/round-48/w1/ScrMistakes/check98.py --repo . --rev REV --seats <wave dir> --lesson <path> --report
> <path> [--report-text]` prints one `SEAT … verdict=ROUTED|UNROUTED` line and `CHECK98: seats= finding_seats=
> unrouted=`. Shown able to fail: round 47's w2 seats read `finding_seats=7 unrouted=4`, rc 1 (and its w1 seats
> `unrouted=1`), while the same seats against a report carrying four routing lines read `unrouted=0`, rc 0
> (`receipts/check98-run.txt`). Declared limit: routing is detected by the seat's name, so a substantive routing that
> never names the seat counts unrouted. (lesson: lessons/round-48.md#mistakes M48-3; outside
> `lessons/round-47-verifier-spotcheck.md` D3)

### 99. A corpus-to-corpus locator resolves to one file and anchors the item it restates (extends 77)

> Criterion 77's instrument reads only names that exist in the `--fetch` directory, so a reference from one corpus
> file to another has no detector. Such a locator resolves to exactly one file — an unqualified basename that two
> files match is a violation — lies inside that file, and, when the citing sentence restates an `[UNK]` item of a
> file that uses `- [UNK]` bullets, starts on the bullet or on a line that carries `[UNK]`. Check: `python3 -I
> .ufo/waves/round-48/w1/ScrMistakes/check99.py --repo . --rev REV --citing <path> [--fetch <dir>]` prints one line
> per locator (`OK`, `UNK-HEAD-CUT`, `AMBIGUOUS`, `OUT-OF-RANGE`, `UNRESOLVED`) and `CHECK99: locators= checked=
> violations=`. Shown able to fail: round 47's entry reads `checked=4 violations=4`, rc 1 (one `UNK-HEAD-CUT` at
> `terminal-route-r17.md:150-151` with the bullet at 149, three `AMBIGUOUS README.md`), and `checked=7 violations=0`,
> rc 0, on the corrected copy (`receipts/check99-run.txt`). (lesson: lessons/round-48.md#mistakes M48-4; extends 77;
> M46-6's residual)

### 100. A wave's scratch bound is enforced by the dispatch, not stated in prose

> Every seat command is a writer, so the wave dispatch carries the command that caps it (`ulimit -f <KB>`, an
> `RLIMIT_FSIZE` setter, or a named `max_file_bytes=`/`--size-cap` value) and each seat receipt records the largest
> file it produced; a dispatch whose only ceiling is a sentence in GB/MB is a violation, whatever the host survived.
> Check: `python3 -I .ufo/waves/round-48/w1/ScrMistakes/check100.py --spec <wave spec> [--context <file>]` prints
> `ENFORCED`/`PROSE` lines and `CHECK100: enforced= prose= verdict=OK|PROSE-ONLY|ABSENT`. Shown able to fail: the
> round-47 and round-48 `w1-spec.json` both read `enforced=0 prose=4 verdict=PROSE-ONLY`, rc 1, while a dispatch
> carrying `ulimit -f 1024` reads `enforced=1 verdict=OK`, rc 0 (`receipts/check100-run.txt`). (lesson:
> lessons/round-48.md#mistakes M48-5 = lessons/round-47.md#mistakes M47-7)

## Duplicate check (no proposed criterion repeats an existing one)

| proposed | nearest existing | why it is not the same check | citation |
|---|---|---|---|
| 96 | 61, 64, 38/49, 9 | those test the freeze document and its paths/commands; 96 compares the *delivered* contract list with the frozen one | `corpus/QUALITY.md:369`, `:375` |
| 97 | **69** | 69's token grammar is `rev=<hex>` only and its instrument returns PASS on the failing report; 97 reads count tokens and fails it | `corpus/QUALITY.md:385` |
| 98 | 52, 90, 93 | 52 binds the sweeping seat, 90 an already-routed item's age, 93 a gate registry cell; 98 binds the integrator's routing of a seat finding | `corpus/QUALITY.md:358`, `:454`, `:480` |
| 99 | **77** | 77 resolves only names present in `--fetch` (`locators=0` on a corpus-to-corpus reference); 99 adds resolution and the `[UNK]` anchor | `corpus/QUALITY.md:401`, `quality/check-locators.py:14` |
| 100 | 31, 34 | 31 bounds a detector's no-harm *evidence*, 34 a scratch *measurement receipt*'s provenance; neither bounds a writer | `corpus/QUALITY.md:298`, `:319` |

## Unmined earlier class swept (target: "any earlier unmined class")

`grep -n 'captured-by:.*none' corpus/lessons/round-4[567].md` returns eight rows; each is now accounted for:

- M46-6 and M46-11 (`corpus/lessons/round-46.md:196`) — the mechanism-locator class; **still uncited** by any
  criterion (`grep M46-6|M46-11 corpus/QUALITY.md` → rc 1) and folded into 99's grounds above. This is the class
  D4 belongs to; leaving it uncited is why round 47's D4 could recur as an off-by-one.
- M46-16, M46-4, M46-12/14/15, M46-2 — captured by 90, 55, 89, 79 respectively.
- M45-1/2/4/6 and M47-6 — M47-6 was captured by 95 (`corpus/QUALITY.md:498`); M45-2's "gate reads JSON keys, not
  prose" and M45-4's "none for fences, receipt citations and README ids" remain uncited, and both were re-answered by
  the v2 control sets rather than by a criterion.
- M47-7 — row M48-5 above; criterion 100 is its proposed capture.

## What this seat did not do

- No tracked file was edited, no counter/gate/fixture was run, no scratch clone was made, no tool was installed, and no
  host cache, config or binary was written. No process, socket, compositor verb or terminal launch.
- `check96`/`check97`/`check98`/`check99`/`check100` and `verify-quotes.py` are seat instruments (provenance): they
  are not credited lane instruments, and their green controls are copies this seat made, not the round's own state.
- Criterion 98's seat-name detection is a proxy for routing (declared in the criterion); the four unrouted seats are
  listed with their finding text so a reader can judge substantive routing without trusting the proxy.
- D1's "either register or model" decision and criterion numbering (96-100) are drafts for the L1's freeze; this seat
  does not freeze them.

## Receipt index

| receipt | what it shows |
|---|---|
| `receipts/d1-contract-delta.txt` | frozen vs landed blob shas, the out-of-contract diff, the frozen registration contract line, the FIFO arm present only in the landed bytes |
| `receipts/check96-run.txt` | 96: red `added=3 unregistered=3 rc=1`; green registered `rc=0`; green no-delta `rc=0` |
| `receipts/d2-report-number.txt` | the report line, the empty `git grep findings=128`, the receipted siblings, criterion 69's instrument reading PASS |
| `receipts/check97-run.txt` | 97: red `missing=1 rc=1`; green `missing=0 rc=0` |
| `receipts/d3-routing.txt` | the seat finding line, `report=0 lesson=0` for four seats, the closure's own routing of D3, the w1 axis finding |
| `receipts/check98-run.txt` | 98: w2 `unrouted=4`, w1 `unrouted=1`, green `unrouted=0` |
| `receipts/d4-locator.txt` | the cited lines, the entry's citing line, criterion 77's instrument reading `locators=0`, the three README candidates |
| `receipts/check99-run.txt` | 99: red `violations=4`; green `violations=0` |
| `receipts/m47-7-mined.txt` | M47-7 is a lesson row; no criterion cites it; both specs state a prose ceiling only |
| `receipts/check100-run.txt` | 100: both specs `PROSE-ONLY rc=1`; green `OK rc=0` |
| `receipts/near-duplicates.txt` | QUALITY's highest criterion (95) and the text of 52/69/77/90/93/94/95, the freeze and resource greps |
| `receipts/unmined-sweep.txt` | every `captured-by: none` row of rounds 45-47 and the criteria that cite those lessons |
| `receipts/quote-check.txt` | 37 located quotes, each computed by `grep` then matched; `differ=0`; one `LOC` line per locator used above |
| `receipts/doc-locators.txt` | every `file:line` written in this file traced to a verifier line: `locators=32 untyped=0 verdict=OK` |
| `receipts/instrument-bite.txt` | both verification instruments shown able to fail: one altered quote → `DIFFER` rc 1; one typed locator → `UNTYPED` rc 1 |

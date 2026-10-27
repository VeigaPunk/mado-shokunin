# Seat CritMistakes — round 48, w2 (FALSIFY)

**Target.** The five proposed M48 mistakes / QUALITY criteria 96-100 drafted by `w1/ScrMistakes`
(`.ufo/waves/round-48/w1/ScrMistakes/mistakes.md`, working-tree `corpus/QUALITY.md:507-556`), against
`corpus/QUALITY.md` criteria 1-95 (committed at HEAD `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`).
Lane `mado-shokunin`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Leaf seat; no lane file edited.

**Frozen instruments read first.** `.ufo/waves/round-48/claims.md`, `.ufo/waves/round-48/registration.md`,
`w1/ScrMistakes/{check96,check97,check98,check99,check100}.py`, `w1/ScrMistakes/controls/*`,
`w1/ScrMistakes/receipts/*`. Reproduction and attack commands were run from
`/home/vgpnk/Projects/shokunin/mado-shokunin` (read-only); fixtures were built under
`/fast/scratch/hyaku/mado-r48/CritMistakes/` and deleted after their receipts were copied here.

## Verdict

| # | criterion | duplicates an existing criterion? | fails on the stated red input? | green only after the fix? |
|---|---|---|---|---|
| 96 | landed contract not narrower | **no** duplicate in 1-95 (61/64/9/38/49/56/68/83 tested, none reads the landed contract) | **no on the round's own artifact**: the delivered `tools/mado-terminal.py` reads `LANDED-NO-LIST`, rc 2; the receipted red only reproduces on a synthetic copy that keeps the frozen heading | **no**: any uncommitted note containing three item phrases passes |
| 97 | report count token needs a receipt | **restates criterion 10** (`corpus/QUALITY.md:16`), overlaps 23 (`:111`) and 91 (`:461`) — none cited in the duplicate table; the 69 extension is genuine | yes (`missing=1`) | **no**: a receipt carrying `findings=1280` satisfies `findings=128` |
| 98 | seat blind spot routed by name | **yes, criterion 52** (`corpus/QUALITY.md:358`) already requires "the sweep names the gap's class, pointer and disposition" | yes (`unrouted=4`) | **no**: a bare seat name with no disposition passes; a finding worded outside the 5-phrase list is never counted; the seat population is read from the worktree, not `--rev` |
| 99 | corpus-to-corpus locator | no — genuine extension of 77 (`:401`); 83 (`:413`) is a second blind instrument, also reproduced blind | yes (`violations=4`) | **yes for the range fix**, but the same cut passes when the citing line does not spell `[UNK]`, and an unrelated locator on a line that does is falsely rejected |
| 100 | wave scratch bound enforced by dispatch | no duplicate of 31/34 (the seat's argument holds) | yes on prose-only specs | **no**: a prose spec that *names* `ulimit -f`/`RLIMIT_FSIZE` passes; the live round-48 `w2-spec.json` reads `verdict=OK` |

## Reductions

1. **97 should not be a new number as drafted.** The lane has already adjudicated this restatement:
   `corpus/lessons/round-20.md:19` (M5) records that "registered criterion 30 're-derive stated counts'
   restated criterion 10 (`QUALITY.md:16`)" and was *withdrawn before any after-measurement*, with the standing
   rule "the restatement screen reads all numbered criteria, not the recent ones"; `.ufo/waves/round-20/w1/reports/RevCriterion30.md:5`
   reaches the same finding ("the proposed core requirement duplicates criterion 10 … criterion 30 should not score
   them a second time"). The draft's duplicate table cites only 69 while the row itself names 10 as the nearest
   (`w1/ScrMistakes/mistakes.md`, M48-2 "captured-by"). Keep at most the narrow distinct clause — *a count token a
   report writes in a detector's vocabulary appears in a committed receipt at the report's revision* — as 10's check,
   boundary-anchored, and cite 10/23/91 as the criteria whose instruments (none / none in `quality/` / entry-scoped
   `check91.py`) leave that clause unmeasured.
2. **98 is criterion 52's missing check, not a new class.** 52 already binds the sweep to name "class, pointer and
   disposition" (`corpus/QUALITY.md:358-360`); the four unrouted seats satisfy 52's first clause (their seat reports
   record the gap) and fail its second. The new part is only *where* the disposition must appear (round-level report
   or lesson). Register that as an extension of 52 and make the instrument score the disposition — as drafted the
   check scores the seat name only (receipt `receipts/d1-98-bare-name.txt`).
3. **100 cannot be registered with this check.** It measures the presence of a string, so it passes the exact red
   input it was written for once that input names the command (see below). Either the criterion is rewritten to an
   observable (a harness-side `prlimit`/`setrlimit` witness and per-seat largest-file record, read from a committed
   receipt) or it is not registered this round.

## 96 — "A landed contract is not narrower than the frozen reference"

**No duplication found.** 61/64 bind the freeze document, 9 binds a verdict to a commit, 38/49 smoke the composite,
56 names counter clauses, 68 names a reference model's parser, 83 resolves paths — none compares a *delivered*
contract item list with a *frozen* one. The defects are instrument validity:

- **The receipted red no longer reproduces, and cannot be reproduced from committed bytes.**
  The seat's red command against the live artifact today:
  `check96.py --repo . --frozen-rev d7527d6… --frozen .ufo/waves/round-47/l1-draft/mado-terminal.py --landed tools/mado-terminal.py`
  → `LANDED-NO-LIST tools/mado-terminal.py carries no 'Also out of contract' list`, **rc=2**
  (`receipts/a1-96-red-as-receipted.txt`). The receipt (`receipts/check96-run.txt`) is `rc=1 NARROWED`; its landed
  bytes are only identified by sha256 `b84d5c4f…` in `receipts/d1-contract-delta.txt`, and that blob is committed
  nowhere (the delivery is a worktree edit: `GIT_OPTIONAL_LOCKS=0 git status --porcelain` → `M tools/mado-terminal.py`).
  The file at that path is now sha256 `1dfde36c…`.
- **The instrument cannot read the delivered contract's own form.** The delivered docstring writes
  `Out of contract: … ; …` (`tools/mado-terminal.py:105-110`), while the parser needs `Also out of contract:` and the
  terminator `On these the tool` (frozen wording only). The check therefore returns `rc=2`, not a verdict, on the
  artifact the round will land. This is the rule criterion 58 states (`corpus/QUALITY.md:365`: a document-scoring
  check parses the document's own form; "a substring test over prose is not an observable").
- **Removals never fail.** A landed copy that deletes the frozen list entirely reads
  `frozen=6 landed=0 added=0 unregistered=0 removed=6 verdict=OK`, **rc=0** (`receipts/a4-96-empty-list-removals.txt`).
  The headline "not narrower" is not measured in the deletion direction, although the row's own text makes
  `removed=0` an argument.
- **The registration paragraph — half of the criterion's own definition — is unreadable.**
  `--frozen .ufo/waves/round-47/registration.md` → `FROZEN-NO-LIST`, **rc=2** (`receipts/a5-96-registration-paragraph.txt`),
  while M48-1's evidence explicitly rests on that paragraph "naming none of the three" (`registration.md:52`).
- **The exemption is a three-word substring in any file, uncommitted and unbound.**
  Red control reproduced cleanly (`added=3 unregistered=3 verdict=NARROWED`, rc=1, `receipts/a8-96-red-clean3.txt`);
  the same landed bytes with `--registered` pointing at a scratch note reading "we never considered HOME unset, a FIFO
  named like a desktop file, or symlink loops" read `verdict=OK`, **rc=0** (`receipts/a9-96-green-anymention3.txt`).
  The seat's own control `controls/registered-96.txt` is admitted identically (`receipts/a10-96-green-seat-control.txt`).
  Nothing binds the registering file to a commit, a revision or the erratum's location, so "registered in an appended
  erratum" is not what is tested.

## 97 — "A report's state number … carries a committed receipt (extends 69)"

Reproduced: red `tokens=11 missing=1 verdict=UNRECEIPTED` rc=1; criterion 69's own instrument `PASS 1/1` rc=0 on the
same report (`receipts/baselines.txt`). The 69 gap is real. The failures:

- **Prefix/substring, not token equality.** A fixture report stating `findings=128` and a committed receipt stating
  `findings=1280` read `FOUND findings=128 <- receipts/r.txt`, `missing=0 verdict=OK`, **rc=0**
  (`receipts/b1-97-prefix-collision.txt`). "A number that exists only in the report" passes whenever any receipt
  holds a longer number with that prefix — the rule criterion 58 already refuses as an observable.
- **The population is the token spelling, not the stated count.** A report writing "reads 128 findings at the tip"
  is invisible; with one receipted token beside it the verdict is `tokens=1 missing=0 OK`, **rc=0**
  (`receipts/b2-97-spelling-invisible.txt`).
- **No subject binding.** Any receipt under the directory satisfies any token; criterion 91 (`:461`) requires the
  receipt's producer line to name the surface, and 23 (`:111`) the recorded outcome. 97's check does neither, so it is
  strictly weaker than both while claiming their subject matter.
- **Duplication** as in Reduction 1 (round-20 M5 precedent).

## 98 — "Every seat that reports a frozen-instrument blind spot is routed by name"

Reproduced: w2 `finding_seats=7 unrouted=4` rc=1, w1 `unrouted=1` rc=1; the seat's green report `unrouted=0` rc=0
(`receipts/baselines.txt`, `receipts/baselines2.txt`). Failures:

- **Name presence is the whole test; the disposition the criterion requires is never read.** A report carrying only
  `- ExecC1Determinism` (no class, no pointer, no disposition) reads `report=1 … verdict=ROUTED`, `unrouted=0 verdict=OK`,
  **rc=0** (`receipts/d1-98-bare-name.txt`). Router by mention, not by routing.
- **The finding population is a five-phrase list.** A seat file stating the same class in other words — "The predicate
  never reads filesystem order, so a tool that sorts entries passes all 190 fixtures; nothing in the counter
  distinguishes the two" — reads `seats=1 finding_seats=0 verdict=OK`, **rc=0** (`receipts/d2-98-novel-wording.txt`).
  The criterion's population ("a seat that reports a blind spot") is wider than the detector's.
- **Seat set read from the worktree, verdict read from `--rev`.** With `seats/ExecOld.md` (blind-spot text) committed at
  `--rev` and deleted from disk, and an uncommitted `seats/ExecNew.md` on disk, the run reads `seats=1 finding_seats=0
  verdict=OK`, **rc=0** while `git ls-tree -r --name-only <rev>` lists `seats/ExecOld.md`
  (`receipts/d3-98-disk-vs-rev.txt`). A seat passes by removing seat files from disk — criterion 63/70/92 class.
- **Duplication** as in Reduction 2.

## 99 — "A corpus-to-corpus locator resolves to one file and anchors the item it restates (extends 77)"

Reproduced: red `locators=7 checked=4 violations=4 verdict=CUT` rc=1; green `checked=7 violations=0 verdict=OK` rc=0
(`receipts/baselines.txt`). Both named instruments are genuinely blind: `quality/check-locators.py` reads `locators=0`,
and criterion 83's instrument reads `CHECK83: verdict=PASS citations=5 violations=0` on the same entry
(`receipts/baselines.txt`) — so 99 is not a duplicate, and should cite 83 as well as 77.

Failures:

- **Rule B fires on the literal token only.** The off-by-one with the citing line respelled — "stays unknown
  (`corpus/knowledge/terminal-route-r17.md:150-151`)" — reads `OK …:150-151`, `violations=0 verdict=OK`, **rc=0**
  (`receipts/e1-99-unknown-spelling.txt`); the identical range with `[UNK]` kept reads `UNK-HEAD-CUT … bullet_at=149`,
  rc=1 (`receipts/e2-99-unk-token-control.txt`). The criterion says "when the citing sentence restates an `[UNK]`
  item"; the check requires the token on the citing line, so the same defect passes in another wording.
- **False positive on an unrelated locator.** A line that cites a bullet-bearing file at a range about something else
  and mentions `[UNK]` elsewhere on the same line reads `UNK-HEAD-CUT … bullet_at=2`, **rc=1**
  (`receipts/e3-99-false-positive.txt`, synthetic fixture `corpus/knowledge/t.md`). The rule is keyed to the token's
  presence on the citing line, not to the item the locator denotes.

## 100 / M48-5 — is the wave bound a command or prose?

**Answer: it is prose, and this criterion's check proves it by passing prose.**

- The live round-48 w2 dispatch — the wave that mines M47-7 — reads
  `ENFORCED .ufo/waves/round-48/w2-spec.json ulimit -f 2048` ×49 (48 seat prompts + one context sentence;
  `grep -o 'ulimit -f 2048' w2-spec.json | wc -l` → 49), `CHECK100: sources=1 enforced=49 prose=102 verdict=OK`,
  **rc=0** (`receipts/c3-100-live-w2-spec.txt`). The hits are the seat prompts and the context sentence
  ("Start each bash writer shell with `ulimit -f 2048`", "record the largest output file"): `w2-spec.json` items carry
  only `{name, prompt, role}` — no command is executed by the dispatch. A prose instruction that *names* the command
  is exactly the shape the criterion calls a violation, and it passes.
- Negation passes: "This dispatch sets no RLIMIT_FSIZE and runs no ulimit -f 1024; the only ceiling is 2 GB." reads
  `ENFORCED … ulimit -f 1024` + `ENFORCED … RLIMIT_FSIZE`, `verdict=OK`, **rc=0** (`receipts/c1-100-negation.txt`);
  the same prose without the magic strings reads `PROSE-ONLY` rc=1 (`receipts/c2-100-prose-control.txt`). The red/green
  difference is wording, not enforcement.
- The green control is itself prose: `controls/spec-100-capped.json` holds one sentence, "each seat runs
  `ulimit -f 1024` before any command (1 MiB per file)"; the same JSON now contains no other evidence.
- **Half the criterion is unscored.** `grep -n 'receipt\|largest\|prlimit\|setrlimit' check100.py` → rc=1 (no match);
  there is no `--receipt` input, so "each seat receipt records the largest file it produced" has no instrument, and the
  green control contains no receipt at all.
- Non-duplication with 31 (`:298`) and 34 (`:319`) is correctly argued — neither governs the writer of an unbounded
  stream — but the drafted check measures the same thing M47-7's wave context did: a sentence. Registering it would
  duplicate the failure it mines. Criterion 58 again applies.

## Notes on the freeze state (observation, not a change)

At HEAD `3e6c848a` `corpus/QUALITY.md` carries criteria 1-95; the working tree carries 96-101
(`GIT_OPTIONAL_LOCKS=0 git status --porcelain` → `M corpus/QUALITY.md`, `+67` lines), and criterion 101 is from a
different proposal (`considerthese/2026-10-26.md` proposal 6), outside this seat's five. `tools/mado-terminal.py` is
also a worktree edit (`M`, `+424/-33`, sha256 `1dfde36c…` vs the receipt's `b84d5c4f…`). Nothing in this report asks
for a change to either; they are the state the checks were run against.

## Bounds, budget and cleanup

- Every bash writer shell began with `ulimit -f 2048` (POSIX 512-byte units; 1 MiB per regular file).
- Scratch: `/fast/scratch/hyaku/mado-r48/CritMistakes/`, total **470,291 B** (limit 2 GB); largest file written
  anywhere **47,977 B** (`fix/96-ext.py`, limit 1 MiB); largest *shell output* file **17,080 B**
  (`out/c3-100-live-w2-spec.txt`). Fixture repos were `mktemp -d -p <scratch>` + `git init -q`, every git call with
  `-C <fixture>`, `rev-parse --show-toplevel` asserted equal to the fixture before every commit; commits used
  `-c user.name=fx -c user.email=fx@invalid` inside the fixture only. Scratch deleted after the receipts were copied.
- No package transaction, no host config/service/compositor/input action, no GUI or terminal launch, no lane Git/jj
  mutation, no commit, no counter or gate run, no `xkbcli`, no resolver run. No home listing, serial, title or process
  table was printed. No tracked lane file was edited.

## Files written

- `.ufo/waves/round-48/w2/CritMistakes.md` (this report)
- `.ufo/waves/round-48/w2/CritMistakes/receipts/` — 24 files: `baselines.txt`, `baselines2.txt`, `fixtures.txt`,
  `a1..a10-96-*.txt`, `b1,b2-97-*.txt`, `d1..d3-98-*.txt`, `e1..e3-99-*.txt`, `c1..c3-100-*.txt`

## Runs the L1 should make after integration

- Re-run the five seat reds against the *committed* artifacts (not the worktree): 96 against the data-tip tool, and
  97/98 against the round-48 report and lessons once written. As shown, 96's receipt and any verdict reading a
  worktree path are not stable.
- Before registering 97/98/100, run the round-20 restatement screen over all numbered criteria — 10, 23, 52, 91 are the
  ones this wave found uncited.

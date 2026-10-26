# CritClaimSizingData — findings (mado round 43, w2, after the data commit)

Seat: `CritClaimSizingData` (leaf critic). Lane `mado-shokunin`. Base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`; freeze v1
`b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`; freeze v2 `496340dd53fabd800be42e8fb19090f35e2c235c`; data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f`; tip read at `2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa`.
No tracked lane file edited; no mutating git/jj; no pacman; no compositor verb; no tool installed (nothing was needed).
Scratch `/fast/scratch/hyaku/mado-r43/CritClaimSizingData/` (removed at close). All receipts in this seat dir; every quote
in this file is verified by `verify-quotes.sh` → `receipt-quotes-verified.txt` (16 OK, exit 0).

## Answer to the five questions

1. **Was v2 frozen strictly before any data?** Yes, at the commit level: `496340d` is the parent of the data commit and
   precedes it by 6m50s (`receipt-commits.txt`); `tools/mado-geometry.py` and
   `corpus/knowledge/hyprland-gkeep-geometry-r43.md` are ABSENT at `496340d`. One qualification, F6: the C1 tool's final
   bytes already sat at `tools/mado-geometry.py` in the worktree and had already been run on the host 29 minutes before the
   freeze, which the frozen v2 denies in words.
2. **Is either target reached by something other than the claimed work?** C1 yes, and v2 declares it: the tool is
   byte-identical to the round-42 reference that the lane already held at BASE (`receipt-tool-identity.txt`), so the
   measured move is installation/promotion, not authoring. C2 no: v2's clause i+ forces all ten PINS, the pins are
   committed at the freeze (10 files, none in the data commit), the entry cites all ten, and the counter replays
   `admitted=1/1` at both the data commit and the tip (`receipt-counters.txt`). The defects found are record/provenance
   defects (F1, F2), not a shortcut to the verdict.
3. **Is C1's "capability acquisition" honest?** Not as the data commit words it. `corpus/lessons/round-43.md:11` says
   "C1 lands `tools/mado-geometry.py` (operability, capability acquisition)" with no provenance; v2 requires the report to
   say "reference installed as `tools/mado-geometry.py`, falsified by three independent implementations" (F3). The
   falsification is real (`w1/ExecIndepA.md`, `ExecIndepB.md`, `ExecIndepC.md` each claim the reference was never opened).
4. **Does a LOG/lesson sentence use a universal clause the counter does not enumerate?** Yes, three (F4).
5. **Is the axis naming right?** The C2 surface that moved is `corpus/README.md` (index row + Frontier bullet) and the new
   note; `PROVINCE.md` moved only C1's tool row. The published coverage score is `10.0000/10` at base **and** at data, so
   the round's coverage axis does not move; the lesson's Axes sentence cites a receipt that does not contain coverage (F5).

## Findings

### F1 — MEDIUM — the data commit's lesson names four receipts; none exists at the data commit and two exist at no revision

Attack: the registration's kill rule (`registration.md:28`, "exit 0, at the data commit and at the tip") and the round's own
criterion 79 (`corpus/QUALITY.md:405` at `1959770`, "names a committed receipt under that round's `receipts/`").

Evidence (`receipt-pointers.txt`):

- `corpus/lessons/round-43.md:150` "measured at the data commit: `receipts/c2-after-data.txt`";
  `:205` "at the tip: `receipts/c1-after-tip.txt`"; `:207` "at the tip: `receipts/c2-after-tip.txt`".
- At `1959770`, all four of `c1-after-data.txt`, `c2-after-data.txt`, `c1-after-tip.txt`, `c2-after-tip.txt` are ABSENT
  (`git cat-file -e`); the after-data pair landed in `a47efeb` (04:56:53, three minutes after data); the two `*-after-tip.txt`
  files are ABSENT at HEAD as well — they exist at no revision in this lane.
- The round's own criterion-79 checker, run on this lesson at the data revision, fails:
  `CHECK79: pointers=2 non_ok=2 verdict=FAIL`, exit 1 (`receipt-check79.txt`), with `:150 … verdict=ABSENT`.
- The checker cannot see `:205`/`:207`: its R2 scan is keyword-gated
  (`re.search(r"recorded|watch|ran\b|run\b|measured|observed|logged", line, re.I)`,
  `.ufo/waves/round-43/w1/ScrQualityCriteria/check79.py:94`), and those two lines carry none of those words. So the two
  permanently dead pointers are invisible to the instrument the round ships for exactly this class.

Impact: the verdicts themselves hold — I replayed both counters at `1959770` and at HEAD: C1 `fixtures=37/37 … TARGET_MET`
(nonces `1bdbe7e30d441225`, `10fd21bc58df93e7`), C2 v2 `admitted=1/1 … TARGET_MET` (`receipt-counters.txt`). What is
missing is the record: the tip half of the kill rule has no committed receipt, and the lesson points at files that were not
there when it landed.

Smallest safe correction: land `receipts/c1-after-tip.txt` and `receipts/c2-after-tip.txt` (a replay at the tip, with
`$`/output/`exit=` so criterion 79's own shape holds), or delete the tip clause from the lesson and let the report carry the
tip replay; and widen check79's R2 gate to any line holding a backticked `receipts/` token (the gate is what let the worse
instance through).

### F2 — MEDIUM — the entry's oracle evidence paths were unlanded at the data commit

Attack: `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (committed at `1959770`) and criterion 8 of `corpus/QUALITY.md:14`
("only after confirming it exists at the named commit").

Evidence (`receipt-pointers.txt`): entry `:56` cites `.ufo/waves/round-43/w1/ExecGoalVsValue/finding.md` and `:62` cites
`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt` and `10-cases.txt`. All three are ABSENT at `1959770` and
PRESENT at HEAD (`2a3707c`, 32 minutes later). The §4 inference — "the rule, not the client, is the origin of 420x500" —
is the entry's only non-source observation and had no committed receipt at the revision where the entry landed. Neither
counter can see this: those paths are not `receipts/` tokens and not Gate receipts, so `check79` on the entry prints
`CHECK79: pointers=1 non_ok=0 verdict=OK` (it sees only `receipts/live-geometry-host.txt`).

The evidence is true where it now exists: `20-observation.txt` shows `"size": [420, 500]` with `"floating": true`, the nofloat
case `size=[918, 498] floating=False`, `size300` `[300, 300]`, `floatonly` `[200, 200]` — so this is a landing-order
defect, not a false claim.

Smallest safe correction: the report (or a later append) names the w1 receipts with their commit (`2a3707c`) and shas, so a
reader at `1959770` knows the oracle bytes landed later; or the entry's §4 cites them as "landed at `2a3707c`".

### F3 — MEDIUM — C1 is still worded "capability acquisition" in the corpus record, not as installation + falsification

Attack: C1's claim name (`registration.md:18`, "C1 — operability (capability acquisition)") against the bytes it lands.

Evidence:

- `git show 1959770:tools/mado-geometry.py | sha256sum` = `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`;
  `git show a35cfdf:.ufo/waves/round-42/c1/ctl-ref-tool.py.txt | sha256sum` = the same; `diff` prints nothing
  (`receipt-tool-identity.txt`). The identical bytes were in the lane at BASE, so the lane held the capability before the
  round; the round installed it.
- `corpus/lessons/round-43.md:11` at `1959770`: "C1 lands `tools/mado-geometry.py` (operability, capability acquisition)" —
  no word about the reference, the copy, or the falsification. The lesson is the corpus's durable record of the round.
- `registration-v2.md:43` (frozen before data) requires the report to state "reference installed as
  `tools/mado-geometry.py`, falsified by three independent implementations" (`receipt-quotes.txt`). The LOG does carry the
  provenance (`LOG.md:2492`, "byte-identical to `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`"), but the LOG is post-data
  (`2a3707c`) and the fleet report `.ufo/reports/round-43/mado.md` does not exist yet (checked, read-only).
- The falsification half is evidenced: `w1/ExecIndepA.md`, `w1/ExecIndepB.md`, `w1/ExecIndepC.md` are three independent
  implementations, each stating the reference was never opened; B reports 6,632 differential cases with zero disagreements.

Impact: the verdict is not affected (37/37 replays). The defect is that the claim's *name* in the corpus describes
authoring, while the measured move is promotion of a frozen artifact. A reader of `corpus/lessons/round-43.md` alone cannot
tell.

Smallest safe correction: the report uses v2's sentence verbatim (it is still unwritten, so no edit to frozen bytes is
needed); any later append to the lesson's C1 paragraph carries the same provenance and the three seats' names.

### F4 — LOW/MEDIUM — universal sentences the counter does not enumerate

Attack: prompt §6 item 9 (no universal clause unless the counting command enumerates the full set); `registration.md`'s
claim sentences.

1. `corpus/lessons/round-43.md:52` "The seven Hyprland pins are byte-identical to the round-42 pins". v2's clause d compares
   a NEW id's receipt name and sha only against the PINS table frozen at `b2e2efd` (`quality/counters/c2-r43-gkeep-entry-v2.py:136`,
   `PINS = {`); the counter contains no round-42 comparison (`grep -n 'round-42' …` → only the PINS line context,
   `receipt-counter-clauses.txt`). I verified the sentence holds: all seven `SAME`, and `host-gkeep.conf` `SAME`
   (`receipt-axis-universals.txt`). So `TARGET_MET` does not establish it; a re-fetch that differed from round 42 would
   still be admitted.
2. `corpus/lessons/round-43.md:29-30` "the only held-row edits this round are the used-by additions on S155 and S158".
   Clause c enforces "ids present at BASE keep cells 1-9 byte-equal" **per cited id** (`receipt-counter-clauses.txt`), so an
   edit to any uncited held row passes. The sentence holds at data — the SOURCES diff is exactly `S155`, `S158` edited plus
   `S290-S297` added (`receipt-axis-universals.txt`) — but the verdict does not score it.
3. `LOG.md:2494` "the entry and SKILL.md read `locators=15 miss=0`". PRED-C2 scores the entry only: it never names
   `SKILL.md` (`grep -n 'SKILL.md' quality/counters/c2-r43-gkeep-entry-v2.py` → no hit) and its clause g checks one
   locator per cited id (10), not 15; no committed receipt carries the checker's output. I reproduced the sentence with the
   committed checker: `CHECK_LOCATORS: locators=15 miss=0`, exit 0 (`receipt-axis-universals.txt`) — so it holds, but it is
   unenumerated and unreceipted.

Smallest safe correction: for (1) add a round-42 comparison to the closure's spot-check (or drop "byte-identical to round 42"
from the lesson); for (2) state the scope ("the only held-row edits among the cited rows"); for (3) commit the checker's
output as `receipts/locators-after-data.txt` and say "entry 10 + SKILL.md 5".

### F5 — LOW — axis naming: the coverage surface moved, the coverage score did not

Attack: `registration.md` "Lane axes: operability and coverage"; `corpus/lessons/round-43.md:24`.

Evidence (`receipt-axis-universals.txt`, `receipt-counters.txt`):

- C2's moved surface: `git diff a35cfdf 1959770 -- corpus/README.md | grep -c hyprland-gkeep-geometry-r43` → `2` (index row
  + Frontier bullet); `corpus/knowledge/` notes 59 → 60.
- `PROVINCE.md` did **not** move for C2: `git diff a35cfdf 1959770 -- PROVINCE.md | grep -c hyprland-gkeep` → `0`; its one
  added line is C1's tool row (`grep -c mado-geometry` → `1`). So PROVINCE is the operability surface, README is the
  coverage surface — the naming is right, but the sentence that grounds it is not.
- The published coverage score does not move: `python3 -I quality/check-index.py --rev <rev> --repo .` →
  `indexed=59/59 … coverage=10.0000/10` at `a35cfdf` and `indexed=60/60 … coverage=10.0000/10` at `1959770`. Coverage is
  saturated at base, so the round's C2 move is an admission (a proxy), not a score move.
- `corpus/lessons/round-43.md:24` "every published axis ties at its maximum at base" cites `receipts/axis-base.txt`, which
  enumerates `navigation`, `calibration`, `operability` only (`MADO_AXIS: checked=3`), and `quality/check-axis-scores.py:32`
  `AXES = ("navigation", "calibration", "operability")`. Coverage is not in either. This is the w1 LOW (`w1/CritClaimSizing.md`)
  still holding at `1959770`, now in the round's durable lesson rather than only in the registration.

Smallest safe correction: add to the Axes sentence `python3 -I quality/check-index.py --rev a35cfdf --repo .` →
`coverage=10.0000/10` (and the same at the data commit), and name the README index row as the coverage surface C2 moves.

### F6 — LOW/MEDIUM — false provenance in the frozen v2: the C1 tool was already at `tools/mado-geometry.py` and already run on the host before the freeze

Attack: `registration-v2.md:43` "never installed, never run on the host as a tool of the lane" (`receipt-quotes.txt`).

Evidence (`receipt-v2-provenance.txt`):

- `receipts/live-geometry-host.txt` (committed at `1959770`, header `2026-10-26T04:17:54-03:00`, 29 minutes before the v2
  freeze) runs `hyprctl clients -j | python3 -I tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` and
  records `sha256sum tools/mado-geometry.py` = `e3c2e471…`. A relative path, so the file existed at the lane root then.
- `w1/ExecLiveHost.md:112-113` repeats it: "`sha256sum tools/mado-geometry.py` at this seat gives" and
  "sha and this seat's copy sha", and that seat ran the tool three times at ~04:19.
- So at the freeze the C1 deliverable existed at its final path with its final bytes and had been executed on the host
  from that path. Two readings, both defects: either the v2 sentence is false, or the receipt's header time is (a backdated
  receipt is worse).

Impact: no verdict changes (C1 was not re-registered; v2 only replaced C2's predicate). The defect is a provenance
sentence in the binding claim document, contradicted by a byte the data commit itself lands.

Smallest safe correction: the report states the true sequence — "the reference bytes were placed at `tools/mado-geometry.py`
during w1 and exercised read-only on the host at 04:17 (receipt), then committed at the data commit" — and stops claiming a
host-run-free freeze.

## Cleared (attacked, held)

- **v2 before data, at the commit level.** `496340d` (04:46:55) is `1959770`'s parent (04:53:45); the real entry and tool
  are ABSENT at `496340d`; the only entry-path files in the freeze commit are the 32-line forgery fixtures under
  `ctl/v2-forgeries/fixtures/*`, and the genuine sample cites `S050` and `S290-S299`, not the round's ten rows — no draft of
  the real entry (`receipt-commits.txt`). The freeze's stated reason (`w1/CritClaimSizing.md`, `w1/CritC2Cheat.md`) was
  uncommitted at `496340d` and landed at `2a3707c` — a reader at the freeze cannot check the "Why"; noted, not filed
  separately (the reports now exist).
- **C2's target is not reachable by skipping the claimed links.** v2 clause i+ forces every PINS name; the pins are
  committed at `b2e2efd` (10 files, `receipt-cleared.txt`) and the data commit adds none of them (`git show --stat …
  -- .ufo/waves/round-43/fetch/` → 0 lines); the entry cites exactly the ten
  (`receipt-counters.txt`, clause c prints ten ids; clauses a-i all `:1`).
- **C1's falsification is real.** Three independent implementations (A, B, C), each stating the reference was not opened;
  B's 6,632-case differential with zero disagreements.
- **Controls untouched by data.** `ctl-c1.txt` and `ctl-c2-v2.txt` are committed at the freeze, not the data commit; the
  data commit changes no counter, no control and no registration byte — `git diff --stat 496340d 1959770 -- quality/counters
  .ufo/waves/round-43/ctl .ufo/waves/round-43/registration.md .ufo/waves/round-43/registration-v2.md` is empty
  (`receipt-cleared.txt`).
- **Locators.** `check-locators.py` on the data entry gives 10 `OK`, `miss=0`; on entry+SKILL 15 `OK`, `miss=0`. The
  `SKILL.md:254` locator `Hyprland-HyprCtl.cpp:395` is *correct* for the format-string claim (line 395 is `"size": [{}, {}],`)
  and is not the M43-1 error; the value claim cites `:427-428` separately.
- **Held-id residual's stated check is blind, but the risk is closed by the pins.** `registration-v2.md:32-33` says the
  entry is expected to cite no held id and names `grep -c '^source: S0' <entry>`; the entry cites two held ids (`S155`,
  `S158`) and that grep prints `0` (they are `S1xx`), so the check cannot show what it claims. The held receipts are
  nonetheless the pinned bytes (`fec33f9a…`, `798b7c6c…`, equal to `receipts/fetch-sha256.txt`), so the residual is not
  used. Smallest correction: replace the grep with `grep -cE '^source: S1(55|58)'` or state the expected count of held ids.

## What this seat did not run

- The control runners (`ctl/run-c1-controls.py`, `ctl/run-c2-controls-v2.py`) and the forgery harnesses: read as bytes only.
  w1 scored them; nothing here depends on re-running them.
- The counter mutants and the ReDoS probe.
- No host compositor verb of any kind.

## Impact on the round's verdicts

Both targets are met at `1959770` and at the tip by replay (C1 37/37, C2 v2 1/1). F1 and F2 mean the round's record at the
data commit violates its own criteria 8 and 79 and lacks the tip receipt; F3 and F6 mean two sentences in the round's
claim documents describe the work differently from the bytes; F4 and F5 are sizing gaps that leave parts of the lesson's
prose outside what `TARGET_MET` establishes. None of the six changes a verdict, and none is a hole in a predicate that
data can still close — all are corrections for the report and the closure.

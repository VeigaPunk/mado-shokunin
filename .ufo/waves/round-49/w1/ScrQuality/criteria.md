# Candidate QUALITY criteria 100-104 (round 49 w1, seat ScrQuality)

Scope: the round-48 closure's uncaptured classes (`corpus/lessons/round-48-verifier-spotcheck.md` §6) and the
round-48 lesson's `## Mistakes` rows M48-8, M48-10, M48-13. Draft only: the L1 integrates; this seat edits no
tracked file and lands no criterion. Base revision `03e4ae76aff7a4be59cb69970dd553baa319695a`.

Numbering: QUALITY.md currently ends at 99 —
`grep -oE '^[0-9]+\. ' corpus/QUALITY.md | tr -d '. ' | sort -n | tail -1` → `99`. The numbers below are proposed
in the order the dispatch lists the classes; the L1 renumbers if it lands them in another order.

Format follows 96-99: a bold title, the rule, a runnable `Check:`, a `Shown able to fail:` state with its
locator, and a `Declared limit`.

Instruments: each criterion names the lane instrument to land (`quality/check-*.py`) **and** ships a seat
prototype with a red run over committed bytes, in this seat's directory, receipt
`w1/ScrQuality/receipts/criteria-red.txt`. The prototypes are seat instruments: provenance, not credit under
criterion 25, and their fixture populations were authored by the same seat that authored the criteria — the
discovery attacks criterion 33 requires for a real lane instrument are w2 work, not claimed here.

Evidence states used below: **observed** = I ran the command in this seat and quote its output; **inference** =
read from committed bytes without running it; **unknown** = stated as unknown.

---

**100.** **A wave writer's writes are bounded by the dispatch, not only by the counter that hosts the scored
tool** — Every command a wave runs that can write (a counter, a scored mutant, a probe, a seat's own script) runs
with `HOME` and `XDG_CACHE_HOME`/`XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_STATE_HOME` inside that seat's scratch,
the real home not bound, and the round commits an operator-owned state pair: the recorded operator paths digested
before the first writer and after the last, each labelled by class (cache file, config tree, `~/.local/bin` entry
count). Any delta in that pair fails the round; a writer that derives its target from the ambient `HOME` is out of
contract, and a digest recorded under a name that asserts the host was not written is criterion 101's subject.
Check: `python3 -I quality/check-host-write.py --trace <strace-file> --allow <scratch> --allow <seat>
--op-home <recorded operator home> --scratch <scratch>` prints `WRITE_OUTSIDE_SANDBOX trace=<file>:<line>
path=<path>` per outside write, `--before F --after F` prints `OPERATOR_STATE_DELTA|_MISSING|_NEW key=...`, and
`--scan <seat dir>` prints `AMBIENT_HOME_WRITE_SITE file=... home_read=<n> write=<n>`; the summary is
`CHECK100: modes=<n> violations=<n> verdict=OK|FAIL`, exit 1 on any violation. Shown able to fail (observed,
`w1/ScrQuality/receipts/criteria-red.txt`): the reconstructed M48-10 trace reads
`WRITE_OUTSIDE_SANDBOX … path=/home/U/.cache/xdg-terminal-exec` (receipt line :8) → `CHECK100: modes=1 violations=1 verdict=FAIL`
(:10), the N2 digest pair reads `OPERATOR_STATE_DELTA` → `verdict=FAIL` (:23), and the source screen over the
round-48 w2 mutant builder reads `AMBIENT_HOME_WRITE_SITE file=.ufo/waves/round-48/w2/MutC1ReadOnly/mkmutants.py
home_read=27 write=38` (:34) — the same file appends `os.environ["HOME"]` at `mkmutants.py:31` and opens the
target for writing at `:39` with `_fh.write("r48-w2\n")` at `:40`, which is how the operator cache came to hold
7 bytes (lesson `corpus/lessons/round-48.md:263`). Green arms: a real strace of a scratch-only writer
(`CHECK100: modes=1 violations=0 verdict=OK`, :16; produced with `env -i` and `HOME` under scratch, 38 trace
lines, zero `/home/` matches) and the unchanged operator pair (:29). Not a restatement of **89**
(`corpus/QUALITY.md:444`), which bounds the *scored tool's* view inside a counter harness — M48-10's write came
from a seat's own unsandboxed mutant run with no counter in the process — nor of **95**
(`corpus/QUALITY.md:498`), which bounds the scoring instrument's own writes under `--work`. (lesson:
lessons/round-48.md#mistakes M48-10; outside lessons/round-48-verifier-spotcheck.md:178)
Declared limit: the trace arm reads a trace someone else produced, so a wave with no trace is `UNTRACED`, not
clean; the source screen is file-level (a home read and a write anywhere in one file) and over-flags a read-only
helper; the digest arm covers only the keys the receipts name, so an unlisted operator path is a census gap under
criterion 90, not a pass.

**101.** **A receipt field's name states what its value measures, or the receipt carries the comparator that
establishes the state** — Every `<name>=<value>` field whose name asserts a state (`untouched`, `unchanged`,
`unmodified`, `clean`, `pristine`, `readonly`, `no_write`, `absent`, a token at an underscore boundary anywhere in
the name) carries, in the same receipt, the comparator that establishes it: a sibling `before`/`reference` field
for the same stem, a `before=`/`compared_with=`/`reference_sha256=` line, or a `_before_`/`_after_` segment in the
name itself. Without a comparator the field is renamed to what it measures (`host_cache_sha256=`) and the state
claim moves to prose citing the comparator; a value that is the digest of bytes the wave is known to have written
is `FIELD_VALUE_IS_PAYLOAD`, never "the host was untouched". Check:
`python3 -I quality/check-field-names.py [--payload TEXT|--payload-hex HEX] RECEIPT...` prints
`STATE_FIELD <file>:<line> name=<n> token=<t> comparator=present|none`, `FIELD_NAME_UNBACKED` for a state field
with no comparator and `FIELD_VALUE_IS_PAYLOAD` for a digest equal to the payload's, then
`CHECK101: receipts=<n> unbacked=<n> payload_matches=<n> verdict=OK|FAIL`, exit 1 when `unbacked>0`. Shown able
to fail (observed, `w1/ScrQuality/receipts/criteria-red.txt`): on `.ufo/waves/round-48/receipts/
live-terminal-cache-r48.txt:4` with `--payload 'r48-w2\n'` it prints `STATE_FIELD …:4 name=
host_cache_untouched_sha256 token=untouched comparator=none`, `FIELD_NAME_UNBACKED`, and
`FIELD_VALUE_IS_PAYLOAD … sha256=c8b104e6…` → `verdict=FAIL` (:46) — the value is `sha256` of the mutant's 7
bytes (outside `lessons/round-48-verifier-spotcheck.md:178`; recomputed in this seat as
`printf 'r48-w2\n' | sha256sum` → `c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144`). Green arms:
the corrected receipt (`host_cache_sha256=` beside `host_cache_sha256_before=`) reads `verdict=OK` (:52), and a
still-state-asserting field that carries its before pair reads `STATE_FIELD … comparator=present` twice (:57-58) →
`verdict=OK` (:60) — so the green arm exercises the comparator path, not merely the absence of a state word. Not
a restatement of **19** (`corpus/QUALITY.md:50`), which scopes a *sentence* about an artifact's retained fields —
here the sentence is fine and the machine-readable field name is the false claim — nor of **63**
(`corpus/QUALITY.md:373`), which binds a worktree observable to a raw witness; a receipt can carry its witness and
still name it wrongly. (outside lessons/round-48-verifier-spotcheck.md:178)
Declared limit: the token list is this lane's current vocabulary, so a new state word is undetected until added;
the instrument proves a comparator *exists*, not that it was taken honestly, so the paired receipt is read, not
trusted.

**102.** **A text rendering of a structured result is a total projection, and the structured file is the record**
— For every run that commits both a machine-readable result and a text rendering, the text carries one row per id
in the machine file, exactly once, and any count the text prints in its own trailer equals the machine file's own
count. A dropped id is `TEXT_DROPPED <id>` even when every row present is correct and the trailer is right;
`--json-key` names the id field and a text row is addressed by row identity, never by a substring match over the
rendering. Check: `python3 -I quality/check-text-projection.py --json <results.json> --json-key name --text
<matrix.txt> [--text-id-pattern REGEX] [--trailer-pattern REGEX]` prints `TEXT_DROPPED`, `TEXT_DUPLICATE`,
`TEXT_EXTRA`, `TRAILER_COUNT text=<n> json=<n>` and `CHECK102: json_ids=<n> text_rows=<n> missing=<n> extra=<n>
dupes=<n> verdict=OK|FAIL`, exit 1 on a missing/duplicate id or a trailer disagreeing with the machine count.
Shown able to fail (observed, `w1/ScrQuality/receipts/criteria-red.txt`): the round-48 v2 pair reads
`TEXT_DROPPED id=a-rev-base-direct`, `TEXT_DROPPED id=a-entry-at-base`, `TRAILER_COUNT text=98 json=98` →
`CHECK102: json_ids=98 text_rows=96 missing=2 … verdict=FAIL` (:68). Those two ids exist only in
`.ufo/waves/round-48/receipts/v2/c2v2-revc2counter-summary.json:24` and `:36`, and the text's own trailer line
still prints `variants 98` (outside `lessons/round-48-verifier-spotcheck.md:185`). Green arm: a rendering
generated from the same summary reads `json_ids=98 text_rows=98 missing=0 … verdict=OK` (:74). Not a restatement
of **37** (`corpus/QUALITY.md:328`), which makes a predicate's denominator equal its counter receipt's — both
artifacts here are internally consistent — nor of **78** (`corpus/QUALITY.md:403`) or **87**
(`corpus/QUALITY.md:422`), which recompute a tally from rows of *one* receipt and so cannot see a row that was
never rendered. (outside lessons/round-48-verifier-spotcheck.md:185)
Declared limit: ids only; a rendered row carrying the wrong verdict for a present id is 78/87's subject. The
default id pattern is written for `<id> <tags> rc=<n>` rows and a different rendering needs its own
`--text-id-pattern` — the red run above shows what a wrong pattern does (it read 94 of 96 rows before the
pattern gained the `rc <n>` spelling, observed).

**103.** **A gate's measured envelope equals the coverage its registry row claims** — For each registered gate,
(a) the row's command flags state the scope the gate actually scans: a row that runs `--repo . --rev REV` with no
`--scope` on a gate whose `--scope` default is `ufo` reads as a repo-wide gate and scans `.ufo/` only, and that is
`SCOPE_UNSTATED`; (b) every rule the row names has at least one committed positive fixture the gate flags; and
(c) every shape class the gate is measured to miss is named in the row as a declared blind spot, not left for an
attacking seat to find. Check: `python3 -I quality/check-gate-envelope.py --repo . --rev REV --registry SKILL.md
--gate-id <id> --gate <gate path> --shape-verdicts <attacker JSONL>` prints `SCOPE_UNSTATED … gate_default=<v>`
or `SCOPE … flag=present`, one `RULE <id> shapes=<n>` line per named rule, one `BLIND class=<c> file=<f>` per
undeclared missed class, and `ENVELOPE: registry=<id> rules=<n> shapes=<n> caught=<n> missed=<n> blind=<n>
verdict=OK|NARROWER`, exit 1 when a class is undeclared or the scope is unstated. Shown able to fail (observed,
`w1/ScrQuality/receipts/criteria-red.txt`): at base, the row at `SKILL.md:770` reads `SCOPE_UNSTATED registry=SKILL.md
flag=absent gate_default=ufo wording=repo` (:79) against
`quality/check-session-material.py:1606` (`add_argument("--scope", choices=("ufo", "all"), default="ufo"`), and the
attacking population reads `ENVELOPE: … shapes=21 caught=3 missed=18 blind=18 verdict=NARROWER` (:105), with
`BLIND` lines naming device dumps, `/run/user` socket paths, base64 and JSON home listings, secret-shaped env
dumps and two classes outside `.ufo/` (`corpus/knowledge/…`, `quality/counters/…`). The same receipt's non-row
line quotes the attacker's own summary `GATE rc=1 missed=16 caught=3 files=19`, and
`w1/SentPrivacy.md:17` states "misses 16 of 19"; the gate was red at the round's data commit anyway
(`SESSION_MATERIAL: files=21985 findings=159 rev=d8e3d600… from
.ufo/waves/round-48/receipts/a4/session-material-tip.txt:4`). Green arm: a fixture registry row that states
`--scope ufo` and `blind-spots=PR-01..PR-19` reads `SCOPE … flag=present` and `blind=0 verdict=OK` (:110, :132) in
a scratch fixture repo with an asserted toplevel. Not a restatement of **93** (`corpus/QUALITY.md:480`), which
requires a gate to be *able* to fail (clean and planted receipts at one revision) — this gate fails and its
envelope is still undeclared — nor of **30** (`corpus/QUALITY.md:249`) or **33** (`corpus/QUALITY.md:318`), which
bind a detector change's precision and its pre-patch discovery attacks; the population here is the attacker's and
the judged object is the registry row's wording. (lesson: lessons/round-48.md#mistakes M48-8)
Declared limit: `positive=none` for a rule means no shape in *this* attacking population hit it, not that the rule
cannot fire (the gate's own selftest covers some of them); the blind-spot declaration test is a phrase test
(`blind-spots=`, `not scanned`) over the row, so a row that declares its gaps in prose elsewhere in SKILL.md reads
`NARROWER`; the 21-row population includes 2 classes outside `.ufo/` [inference: their paths are
`corpus/knowledge/…` and `quality/counters/…`], which count as missed because the gate never reads them.

**104.** **A dispatched bound is admissible only beside the recipe it must survive (extends 98)** — When a wave
dispatch carries a resource cap, the same dispatch carries a committed probe that runs the dispatch's own
heaviest named recipe under that cap and records its exit status; a cap and a recipe stated in different sentences
are two claims, and a wave whose recipe cannot complete under its cap has aborted seats, not slow ones. The
compatibility itself is a computed reading: a recipe that materialises the tree (`clone`, `checkout`) against the
largest blob the revision tracks. Check: `python3 -I quality/check-cap-recipe.py --repo . --rev REV --cap-bytes N
--recipe clone|checkout|none [--probe FILE]` prints `BLOB_OVER_CAP size=<n> cap=<n> path=<p>` per offending blob,
`PROBE receipt=<f> rc=<n>`, and `CAP_RECIPE: cap=<n> recipe=<r> blobs=<n> blobs_over=<n> max_blob=<n>
max_path=<p> verdict=INCOMPATIBLE|PROBED|UNPROBED`, exit 1 on any blob over the cap under a materialising recipe
or a failed probe. Shown able to fail (observed, `w1/ScrQuality/receipts/criteria-red.txt`): at this lane's base `03e4ae76…`,
`CAP_RECIPE: cap=1048576 recipe=clone blobs=22278 blobs_over=24 max_blob=4207542
max_path=.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl verdict=INCOMPATIBLE` with a probe receipt reading
`rc=128` (:163) — matching M48-13's abort, `.ufo/waves/round-48/a4r1-results.json:40` ("Scratch clone checkout
could not complete because RLIMIT_FSIZE=1 MiB rejects numerous committed large files") for the dispatch that
carried `ulimit -f 2048`. Green arm: an 8 MiB cap reads `blobs_over=0 … verdict=PROBED`, exit 0 (:169). Not a
restatement of **98** (`corpus/QUALITY.md:533`), which asks whether the cap is *executed* rather than written in
prose — round-48's cap was executed and still broke the recipe — nor of **61**/**64**
(`corpus/QUALITY.md:369`, `:375`), which bind the commands a registration names at the freeze; the failing
combination here is a cap and a recipe that were each individually correct. (lesson: lessons/round-48.md#mistakes
M48-13)
Declared limit: a per-file cap is one failure mode of a clone, not all of them (the git index, packfiles and
renames matter too), so `blobs_over=0` is a necessary condition, not a pass — the probe receipt is what proves
the recipe ran; a sparse or partial-clone recipe needs its own recipe name; and `--probe` reads a receipt, so a
probe that was never run reads `UNPROBED`, never green.

---

## What the L1 must decide

1. **Numbering and grouping**: 104 extends 98 rather than duplicating it — if the L1 reads it as the same class,
   the remedy is a sentence appended to 98, not a new number (the round-48 precedent: 97 and 98 were withdrawn as
   restatements of 10 and 52, `corpus/lessons/round-48.md` § Applications).
2. **Instrument ownership**: each criterion names a `quality/check-*.py` path that does not exist yet; the
   prototypes here are `w1/ScrQuality/check100-hostwrite.py`, `check101-fieldname.py`,
   `check102-textprojection.py`, `check103-envelope.py`, `check104-caprecipe.py`, each with `--help`-documented
   limits. Criterion 64's pre-dispatch path check applies to whichever land.
3. **Discovery attacks**: the fixture populations were authored by this seat (100's trace/digest/receipt
   fixtures, 102's total-projection fixture, 103's declared-envelope fixture row, 104's probe receipts). Criterion
   33's frozen pre-patch attacks are w2 work and are not claimed.
4. **Scope of the host-write pair**: 100 requires a before/after operator-state pair per round; the round already
   carries the before half (`.ufo/waves/round-49/receipts/operator-state-before.txt`, 5 keys: resolver cache, three
   hypr config files, `~/.local/bin` entry count). My seat did not write it and did not verify it — it is the
   L1's receipt.

## Observation / inference / unknown

- Observed by this seat: every red and green line quoted above (commands and exits in
  `receipts/criteria-red.txt`, 14 runs: `exit=1` at lines 11, 24, 37, 47, 69, 106, 164; `exit=0` at 17, 30, 53,
  61, 75, 133, 170); `printf 'r48-w2\n' | sha256sum`; `grep -oE '^[0-9]+\. ' corpus/QUALITY.md | tr -d '. ' |
  sort -n | tail -1` → `99`; the operator cache still reads `ddd94f6b…` after all runs (the round-49 before
  digest), so no run of mine wrote it.
- Inference: the two `.ufo`-external shape rows; that the 18 missed classes exceed SentPrivacy's 16 because its
  JSONL adds the two out-of-scope comparison rows to the 19 scanned files (its non-row line prints
  `files=19 missed=16` and the JSONL holds 21 rows).
- Unknown: whether any other round-49 seat has written a state-asserting receipt field (101's population is the
  round-48 receipts I read); whether the gate's `R2`/`R3`/`R5`/`R6` rules have positives outside the attacking
  population; the shape of the operator-state *after* half for this round.

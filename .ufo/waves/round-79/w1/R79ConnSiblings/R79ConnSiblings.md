# R79ConnSiblings — connector: sibling overlap and cross-claim scan (round 79)

Seat `R79ConnSiblings` (connector, leaf — no dispatch). Read-only: no repo write, no
git/jj mutation, no host write, no socket. Freeze `5eb8f20f`; base `e4b153df`.

The lane advanced **four times while this scan ran** (`5eb8f20f` → `03e76ee9` → `3b8af34c` →
`d6be05ef` → `8696c4dd`), and repair **R2 was in flight in the working tree at hand-off**
(§6). Two of my findings were repaired by those commits before I could file them; they are
recorded below as closed-with-the-commit-that-closed-them, and the residue that survives at
`8696c4dd` is marked **OPEN**. Every line number is at `8696c4dd` unless a different revision
is named.

---

## 1. Sibling overlap — no `*-shokunin` lane claims C1 or C2 ground

Probes run from the fleet root `/home/vgpnk/Projects/shokunin`, siblings only:

| probe | command | hits outside `mado-shokunin` |
|---|---|---|
| the static reserve verb | `grep -rl -F addreserved */` | 2 — both quotations, see below |
| the reserved-area type | `grep -rl -F reservedArea */` | 0 |
| the instrument | `grep -rl -F mado-barfoot */` | 0 |
| the ground | `grep -rl -F bar-footprint */` | 0 |
| vendorised counters | `grep -rl -F 'MADO_R79' */` · `grep -rl -F 'c1-r79-reserve' */` · `grep -rl -F 'c2-r79-runbook' */` | 0 · 0 · 0 |
| an executable `hyprctl` read-row runbook | `grep -rn -E 'hyprctl +(layers\|monitors\|binds\|getoption)' --include='*.py' --include='*.sh' --include='*.mjs' */` | 0 |
| an executable `omarchy` read-row runbook | `grep -rn -E 'omarchy (theme current\|version\|commands --json\|menu keybindings)' */` | 0 |

The two `addreserved` hits are **consumers, not claimants**:

- `kumitate-shokunin/.ufo/waves/round-81/w1/K81ConnOverlap-captures/grep-05-admission.txt:223`
  quotes **mado's own** `tools/mado-barfoot.py:47` from the **r78** generation — the sentence
  "Not modelled and named as a limit: a static `monitor … addreserved` band". That limit is
  superseded: the r79-v1 docstring's limit list at `tools/mado-barfoot.py:65` now names a
  second *layer-surface* consumer instead. Province: kumitate's province is orchestration and
  ufo-fsd scripts (`kumitate-shokunin/PROVINCE.md:3`); it records no compositor surface, so
  this is a dated capture of mado text, and a closure reading it as current would be reading
  the r78 limit. Not a claim, but the capture is now a stale-quotation site.
- `tabi-shokunin/.ufo/waves/round-34/w2/ConnSiblingDrift/mado.diff:59` quotes the **upstream**
  S303 line (`ARGS[1] == "addreserved"`, `Hyprland-legacy-ConfigManager.cpp:1299`) inside a
  drift diff of mado's r34 corpus. Province: tabi owns browser/web-interaction craft
  (`tabi-shokunin/PROVINCE.md:3-5`); no compositor surface named.

Nearest real adjacency, and the only one worth naming for the round:

- `game-dev-2d-shokunin/corpus/live/r79-boundary-exec/run_love_probe.py:42` runs
  `subprocess.run(["hyprctl", "clients", "-j"], …)` to poll for a game window. That is **one
  shared read verb** (`clients`), not the C2 runbook and not the C1 ground (`layers`/`monitors`),
  exactly as the round-78 connector recorded. Province named by game-dev-2d: 2D game production
  (`game-dev-2d-shokunin/PROVINCE.md:3`); it does not name display behaviour.
- `kasegi-shokunin/.ufo/waves/round-24/wave1/ConnSibling.md:161` uses the phrase "declared
  reserved band" for a **source-id band** (`S039→S100 …`), a homonym of the Hyprland reserved
  area. Province: kasegi owns bounty/security research (`kasegi-shokunin/PROVINCE.md:3`).
- `tsukuroi-shokunin/.ufo/waves/round-50/w1/R50RevScopeSiblings/tip.mado.md:29-31,106`
  inventories mado's instruments (`mado-binds.py`, `mado-anims.py`, `mado-devices.py`) read-only.
  It predates r77 and contains no `barfoot` hit (`grep -c barfoot …` → 0), so it neither claims
  nor describes this round's instrument.

Province lines that settle the split, quoted from the siblings themselves:
`mado-shokunin/PROVINCE.md:3-4` owns "the Hyprland/waybar/walker configuration plane and display
behavior on this host"; `game-dev-3d-shokunin/PROVINCE.md:75` states "Desktop/compositor display
behavior belongs to `mado-shokunin`"; `kotoba-shokunin/PROVINCE.md:72` records "no split" with
mado. **No overlap is the finding**: no sibling states mado's side of the C1 reserve/band join or
runs a C2-shaped runbook, and no sibling vendors the r79 counters.

---

## 2. Lane-record defect classes

### 2.1 `D2` class — a cited revision described as an instrument's last change — **OPEN**

`SCORECARD.md:4416` (the round-77 C1 row) still reads:

> at `a83e9bee` (its instrument's last change)

Red at the freeze and redder now: the same tool path has since been changed by `b774f920`
(r78-v2), `5eb8f20f` (r79-v1) and `d6be05ef` (repair R1). The lane's own probe disagrees under
both instrument resolutions:

```sh
sed -n '4416p' SCORECARD.md > /tmp/row.md
python3 -I quality/check-cited-revisions.py --repo . --text /tmp/row.md --path tools/mado-barfoot.py
python3 -I quality/check-cited-revisions.py --repo . --text /tmp/row.md --path quality/counters/c1-r77-barfoot.py
```

observed at `8696c4dd`:

```
CITED-REVISIONS-PROBE: instrument=tools/mado-barfoot.py last_change=d6be05efc2185acb2e7c2b11919b88bce3cc3e7d claims=1
CITED-REVISIONS-PROBE: claim hash=a83e9bee kind=last-change match=no
CITED-REVISIONS-PROBE: RESULT red claims=1 mismatched=1
```

and against the r77 counter, whose measured last change is `de627316…`:

```
CITED-REVISIONS-PROBE: instrument=quality/counters/c1-r77-barfoot.py last_change=de62731673447892ff222b821dea639596cfcc9c claims=1
CITED-REVISIONS-PROBE: RESULT red claims=1 mismatched=1
```

The round-78 correction block acknowledges the phrase (`SCORECARD.md:4526-4528`: "is now false in
the present tense … the row's 'last change' phrase is time-bound") but leaves the sentence in
place, so the probe keeps failing on a row the lane has already dispositioned. Green form: the
row should read "measured at `a83e9bee`" (a revision, not a superlative), or the parenthesis
should be struck; either makes the probe green because `measured-at` is checked against the same
`git log -1` and `a83e9bee` is the round-77 freeze, not the tool's last change — so the honest
green is to remove the claim, not to re-point it.

### 2.2 The same class in a form the probe cannot see — **OBSERVED, then rewritten by the integrator**

Between `03e76ee9` and `8696c4dd` the round-77 corrections block carried "Final instrument
revisions: C1 counter `de627316`, tool `2df46e29`, tool sha256 `446d197f…`". "Final" is the same
defect in a spelling `check-cited-revisions.py` does not parse (its two patterns are
`at <hash> (its instrument's last change` and `measured at <hash>`; `grep -n 'Final instrument
revisions' SCORECARD.md` now returns nothing at `8696c4dd`). Recorded because the class is
probe-shaped, not text-shaped: a closure that trusts the probe's green will not see a stale
superlative that is spelled differently.

### 2.3 A ledger row whose description no longer matches the instrument — **OPEN**

`quality/tool-ledger.md:180` (the `quality/counters/c1-r79-reserve.py` row) says the counter
"asserts the frozen eighteen round-78 cases are carried **byte-identically**". The counter does
not compare bytes:

```sh
grep -n 'carried_ok = ' quality/counters/c1-r79-reserve.py     # → carried_ok = cases[:CARRIED] == carried
sed -n '180p' quality/tool-ledger.md | grep -c 'byte-identically'   # → 1
```

Both sides of the `==` are `json.load(...)["cases"]`, so the assertion is parsed equality; a
byte-level reformat of the carried set passes it while `sha256` differs (demonstrated:
`json.dumps(json.load(open(r78)), indent=4)` → bytes differ, sha256 differs, `json.loads` equal).
The declaration was corrected for exactly this at `3b8af34c` (append-only block plus a reworded
sentence), and `SKILL.md:786` now says "carried unchanged (parsed equality)", but the ledger row
was **not** touched: `d6be05ef` edited only the `tools/mado-barfoot.py` row of the ledger
(43/43 → 44/44). Green form: `sed -i 's/are carried byte-identically/are carried unchanged
(parsed equality)/' quality/tool-ledger.md` restricted to that row — then
`python3 -I quality/check-tool-ledger.py --repo . --rev 8696c4dd` stays `TARGET_MET`.

### 2.4 `D3` class — an index/frontier count that disagrees with the lesson — **OPEN**

`corpus/README.md:133` (the round-79 frontier bullet) reads:

> rows S465/S466 new, S457/S458/S459/S303 re-opened and re-fetched byte-identically

Three committed records disagree with it, and with each other:

| record | what it says | evidence |
|---|---|---|
| `corpus/README.md:133` | four re-opened rows, all "re-fetched byte-identically", S303 included | the line itself |
| `.ufo/waves/round-79/claims-declaration-r79.md:126-127` | seven re-opened, all re-fetched: S457/S458/S459/S460/S461/S462/S464 (S462's pin reused) | the declaration |
| `corpus/lessons/round-79.md:34-41` | S457/S458/S459/S303/S461/S462/S464 re-opened — S460 absent, S303 present | the table |
| `.ufo/waves/round-79/fetch/sha256-r79.txt` | nine payloads pin S457-S462, S464, S465, S466 — **no S303** | `ls .ufo/waves/round-79/fetch/` |

```sh
ls .ufo/waves/round-79/fetch/ | grep -c S303                       # → 0
grep -c S460 corpus/README.md corpus/lessons/round-79.md corpus/knowledge/bar-footprint-reserve-r79.md  # → 0 0 0
cd .ufo/waves/round-79/fetch && sha256sum -c sha256-r79.txt        # → 9 OK, rc 0 (S460.bin among them)
git diff 5eb8f20f 03e76ee9 -- corpus/SOURCES.md                    # S303: used-by cell only, no byte pin
```

So: S303 was **re-opened** (its `used-by` cell gained the r79 entry; its r45 pin
`9db68cf4…` still verifies against `.ufo/waves/round-45/fetch/Hyprland-legacy-ConfigManager.cpp`)
but **not re-fetched**; S460 was fetched and verified this round and is named by no record except
the declaration. The row census compounds it: `git show 5eb8f20f:corpus/SOURCES.md | grep -cE
'^\| S[0-9]+'` → **401**; at `03e76ee9` → **404**; the delta is S465+S466 (mined), S467
(**rejected** candidate), which the lesson states correctly ("Two rows added and one rejected row
added") and the frontier bullet's "S465/S466 new" does not reconcile with.

This is the same class the round says it repairs (`SCORECARD.md:4595-4598`, "D3 — the r78 frontier
bullet's 'three re-opened rows' is corrected by this round's bullet"). The repair replaced one
wrong membership with another: it added S303 (not fetched) and dropped S460/S461/S462/S464
(fetched). Green form: "rows S465/S466 new, S467 rejected; S457/S458/S459/S460/S461/S462/S464
re-fetched byte-identically; S303 re-opened (r45 pin reused)".

---

## 3. Provenance chain: declaration → counter → control set → fixture → receipt

### 3.1 C1 — resolves at the freeze triple, **not** through the shipped counter

| link | path | at `5eb8f20f` | at `8696c4dd` |
|---|---|---|---|
| declaration | `.ufo/waves/round-79/claims-declaration-r79.md` | present | present (+3 append-only blocks) |
| counter | `quality/counters/c1-r79-reserve.py` | blob `5106bd27…`, sha256 `48ebfab6…` | blob `4ab111d7…` (repair R1) |
| control set | `.ufo/waves/round-79/controls/c1-cases-r79.json` | sha256 **`5f7ebb3c…`** = the declaration's pin | sha256 `108bde32…` (repair R1) |
| fixtures | inline in each case (`config`/`layers`/`monitors`/`rules` strings), not separate files | resolve | resolve |
| carried set | `.ufo/waves/round-78/controls/c1-cases-r78.json` | tracked, prefix equal (parsed) | same |
| instrument | `tools/mado-barfoot.py` | sha256 `c9aa1391…` = the declaration's pin | sha256 `673ac44d…` |
| receipt | `.ufo/waves/round-79/receipts/measurement-c1-r79.txt` | **absent** (landed at `03e76ee9`) | present, prints `rev=5eb8f20f` |

The chain resolves **only if every link is taken at the revision that pinned it**. Measured both
ways at `8696c4dd`, same command shape, same `--rev 5eb8f20f`:

```sh
# shipped counter (HEAD) + the declaration's own control set
python3 -I quality/counters/c1-r79-reserve.py --repo . --rev 5eb8f20f \
  --base-rev e4b153dfa4a67ca56f7ec65cb6639082451626a7 \
  --controls .ufo/waves/round-79/controls/c1-cases-r79.json \
  --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR
```
```
MADO_R79_BARFOOT: cases=23 correct=23 mutants=12 killed=10 base_correct=18/23 carried=18/18
tool_selftest=43/43 verdict=TARGET_MISSED rev=5eb8f20fe291603c74973fa94cc55723ac8089a4
tool_sha256=c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de
```
(receipt `w1/R79ConnSiblings/receipts/c1-head-counter-vs-frozen-rev.txt`; identical result with
the freeze control set, because the two mutants' anchors, not the cases, moved.)

```sh
git show 5eb8f20f:quality/counters/c1-r79-reserve.py > DIR/c1-freeze.py
git show 5eb8f20f:.ufo/waves/round-79/controls/c1-cases-r79.json > DIR/c1-controls-freeze.json
python3 -I DIR/c1-freeze.py --repo . --rev 5eb8f20f --base-rev e4b153df… \
  --controls DIR/c1-controls-freeze.json --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR
```
```
MADO_R79_CONTROL: sha256=5f7ebb3c47c68dedcd113f29f63f995fccdb201e16eb949a4a450be892252eb7 carried=18/18
MADO_R79_BARFOOT: cases=23 correct=23 mutants=12 killed=12 … verdict=TARGET_MET … tool_sha256=c9aa139152…
```
(receipt `w1/R79ConnSiblings/receipts/c1-freeze-counter-vs-frozen-rev.txt`.)

Cause, from the repair diff: `d6be05ef` re-pointed the `static-order-swapped` and
`static-first-wins` anchors from the freeze tool's `slot = dict(zip(STATIC_SIDES, …))`
(`git show 5eb8f20f:tools/mado-barfoot.py:374`) to the repaired tool's `area = dict(zip(…)` 
(`tools/mado-barfoot.py:376`). Against the frozen revision those two anchors are absent, so the
counter prints `reason=anchor-absent` and `killed=10` — the counter's own r79 D2 repair, working
as designed, on a triple it can no longer measure.

**Consequence to state plainly:** the declaration's counting command is frozen unmodified and
names `--rev REV`; a closure that runs it with `REV=5eb8f20f` and the in-tree control set gets
`TARGET_MISSED` rc 1. The declaration's R1 block says "the frozen 23/23 at `5eb8f20f` stands as
the measurement of the bytes at that revision" — true, but it does not say the *shipped* counter
cannot reach it. Either the counter should pin `tool_sha256=c9aa1391…` and refuse a foreign
instrument (fail-closed, like C2's tree binding), or the record should carry the extraction
command above as the way to re-derive the freeze receipt.

### 3.2 C2 — resolves at the freeze tree only; the tree binding makes HEAD a rc 2

| link | path | result |
|---|---|---|
| declaration | same file, C2 section | present |
| counter | `quality/counters/c2-r79-runbook.py` | tracked at the freeze; unchanged since |
| control set | `.ufo/waves/round-79/controls/c2-runbook-cases-r79.json` | tracked, 22 cases, 22 **distinct** `skill_anchor`s; kinds decompose exactly as the receipt prints them: 17 shape-bound (`exact` 4, `int_range` 4, `regex` 3, and one each of `empty`/`int4`/`sorted_unique`/`json_object_fields`/`levels_dump`/`array_fields`) + 4 `refusal` + 1 `lines_shape` = 22, i.e. `shapes=17/17` is the shape-bound subset, not 17 of 22 matched |
| rows | `SKILL.md` §"Executable runbook rows (round 79)" (`:231-263`) | **22 rows, 22 distinct command cells, set-equal to the 22 anchors, each bound exactly once** (independent escape-aware parse, not the counter) |
| fixtures | `.ufo/waves/round-79/fixtures/refuse-{mode,scale,layer-background,output-space}/` | 4 × 3 files, all tracked at the freeze |
| receipt | `.ufo/waves/round-79/receipts/measurement-c2-r79.txt` | absent at the freeze (landed `03e76ee9`), prints `rev=5eb8f20f tree=bound` |

```sh
python3 -I quality/counters/c2-r79-runbook.py --repo . --rev 5eb8f20f \
  --controls .ufo/waves/round-79/controls/c2-runbook-cases-r79.json \
  --carried .ufo/waves/round-78/controls/c2-runbook-cases-r78.json --scratch-root DIR
```
observed at `8696c4dd`: `MADO_R79_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not
the measured revision's bytes)` **rc 2** (receipt `w1/R79ConnSiblings/receipts/c2-counter-at-head.txt`).
Cause: `3b8af34c` edited `SKILL.md:786` ("carried byte-identically" → "carried unchanged (parsed
equality)"), so the working tree is no longer the freeze tree. The refusal is correct and
fail-closed; what the record lacks is the statement that **C2 is reproducible only from a tree
whose `SKILL.md` and `tools/mado-barfoot.py` bytes equal the freeze's** — the scorecard's C2 row
(`SCORECARD.md:4553`) names rc 2 only as the *before* state ("at the base rev the counter refuses
(rc 2, working tree is not the measured revision's bytes)"), and the same symptom now recurs at
the measured revision for a different reason. C1 and C2 are therefore asymmetric on
re-derivation: C1 is rev-anchored and reproduces its freeze receipt (with the freeze counter),
C2 is tree-anchored and cannot reproduce anything after the first post-freeze edit to `SKILL.md`.

### 3.3 Two record-level links that moved (both were open at the freeze)

- **Receipts committed one revision after the revision they name** — `.ufo/waves/round-79/receipts/
  measurement-c{1,2}-r79.txt` are `??` at `5eb8f20f` and first tracked at `03e76ee9`, while their
  own text says `rev=5eb8f20f`. Same shape as round-78 `M78-6` ("the final measurement receipts
  are committed at the measured revisions"), and benign only because the receipt prints its
  measured revision; the link "receipt path @ freeze" does not resolve.
  `git log -1 --format=%h -- .ufo/waves/round-79/receipts/measurement-c1-r79.txt` → `03e76ee9`.
- **The fetch manifest could not verify itself** — at the freeze, `sha256sum -c
  .ufo/waves/round-79/fetch/sha256-r79.txt` printed nine `OK` and `sha256-r79.txt: FAILED`
  (the manifest listed its own pre-write hash), rc 1. `3b8af34c` dropped the self-line and
  switched to bare filenames; at `8696c4dd`, `cd .ufo/waves/round-79/fetch && sha256sum -c
  sha256-r79.txt` → nine `OK`, **rc 0**. Closed. Note the form now matches r78's (bare names,
  must be run from `fetch/`), so a single documented command cannot verify both rounds' manifests
  from the repo root.

---

## 4. The contradiction, stated rather than smoothed

The declaration says of itself: "predicate, counter, kill rule and target below are not rewritten
after a seat scores", and "No seat may rewrite `tools/mado-barfoot.py`, the two counters, the two
control sets, the fixtures or this declaration." Observed at `8696c4dd`:

- `tools/mado-barfoot.py`, `quality/counters/c1-r79-reserve.py` and
  `controls/c1-cases-r79.json` were all rewritten after the `5eb8f20f` measurement — by the wave's
  own repair `d6be05ef` ("repair R1: an addreserved with no prior rule drops its area (wave
  R79ScribeEntry F1)"), with a declaration block, a lesson row, a ledger row and two receipts.
- The declaration's frozen sentence was also edited **in place** at `3b8af34c` (the
  "byte-identically" wording) *and* an append-only block was added to disclose it.
- Both are disclosed, neither is dishonest — but they pull in opposite directions: the round's
  provenance story is "frozen triple", and its actual history is "frozen triple, then a
  load-bearing behaviour repair that changes the instrument, the counter and the case set". A
  closure reading only the pinned sha256s (`c9aa1391…`, `5f7ebb3c…`) against the tree at
  `8696c4dd` sees two mismatches and no way, from the pinned line alone, to tell a repair from a
  drift. The append-only blocks are the disclosure; the *pinned lines* still read as if nothing
  moved.

I do not resolve this. It is the L1's call whether to (a) pin the triple per revision in the
receipt label, (b) have the counter refuse a foreign `tool_sha256`, or (c) leave the frozen text
and mark the repair as the scored measurement only.

---

## 5. Scope, limits, and what this scan did not do

- No repo write, no git/jj mutation, no host write, no socket, no package transaction. Scratch
  `/fast/scratch/hyaku/mado-r79/R79ConnSiblings/` (deleted on finish); the four receipts I cite
  are copied into `w1/R79ConnSiblings/receipts/`.
- The two counter runs I performed execute the lane's own instruments in caller scratch; the C2
  refusal is the counter's, not mine.
- Records read-only across `*/PROVINCE.md` and `grep -rl` over every sibling tree; no sibling
  corpus was parsed for claim semantics beyond the hits reported.
- Line numbers are at `8696c4dd`. Three of the findings moved under me during the scan
  (`03e76ee9`, `3b8af34c`, `d6be05ef`); each finding states the revision at which it was observed
  and re-checked at `8696c4dd`.

---

## 6. Tip state at hand-off (R2 in flight) and what it does to these findings

Observed after the L1 announced repair R2, at HEAD `8696c4dd`:

| object | tracked at `8696c4dd` | working tree |
|---|---|---|
| `tools/mado-barfoot.py` | `673ac44d…`, `--selftest` 44/44 | **`241afdd0…`, 50/50 — uncommitted (R2)** |
| `quality/counters/c1-r79-reserve.py` | `4af4b1a8…`, `--selftest` 36/36 | clean (same bytes) |
| `controls/c1-cases-r79.json` | `108bde32…` | clean (same bytes) |
| `SKILL.md`, `tools/mado-barfoot.py` tree binding for C2 | — | `git status --porcelain` → ` M tools/mado-barfoot.py` only |

Consequences, stated so the numbers above are not read as stale:

1. **The green/red pair in §3.1 is independent of the working tree.** Both runs extracted the
   instrument from `git show 5eb8f20f:…` (the `tool_sha256=c9aa1391…` printed in every line is the
   *extracted* revision's bytes, not the in-tree tool). R2 cannot change either line; a reader who
   compares the printed `tool_sha256` against `sha256sum tools/mado-barfoot.py` will see a
   mismatch by design.
2. **R2 makes the §3.1 recommendation sharper, not weaker.** Every repair that changes the
   instrument's source spelling re-cuts the mutant anchors; the shipped counter has now been
   re-cut twice (R1) and is about to be re-cut again (R2). The counter either pins
   `tool_sha256=c9aa1391…` for the freeze measurement and refuses a foreign instrument, or the
   lane keeps a per-revision counter copy; otherwise the freeze receipt is re-derivable only by a
   reader who already knows to use `git show`.
3. **The three OPEN records were still open at hand-off**: `quality/tool-ledger.md:180` still
   reads "carried byte-identically"; `corpus/README.md:133` still reads "S457/S458/S459/S303
   re-opened and re-fetched byte-identically"; `corpus/lessons/round-79.md` still names no S460
   (`grep -c S460` → 0). The L1 replied that items 2 and 3 are being corrected and that
   `SCORECARD.md:4416` will be dispositioned as expected-red rather than repaired in place —
   that reply is coordination, not a measurement, so this report records the state it observed.


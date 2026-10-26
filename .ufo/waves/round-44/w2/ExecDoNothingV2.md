# ExecDoNothingV2 — shape-keeping do-nothing controls against both v2 predicates

Seat: `ExecDoNothingV2` (w2, round 44). Data commit `e4678921`, base `6a1a905`. Predicates under attack:
`quality/counters/c1-r44-geometry-states-v2.py` (sha256 `0d872405…`) and
`quality/counters/c2-r44-gkeep-size-request-v2.py` (sha256 `3246d2aa…`), both frozen and unedited by this seat.
Every run below is `git -C <fixture> show`-addressed; no tracked file in the lane was written or edited (the seat
wrote only `.ufo/waves/round-44/w2/ExecDoNothingV2/`).

**Result in one line.** C2: the landed entry reduced to 27 lines (header + five trimmed claim lines + two census
lines) is still `TARGET_MET` — declared residual; a 27-line entry whose only locators are **whole-file ranges**
is also `TARGET_MET` — **new hole (O1)**. C1: the landed tool with the round-43 docstring is `TARGET_MET`
(documentation axis, O3); the landed tool padded with five dead comparison sites is `TARGET_MET` on 1 of 4
nonces and `TARGET_MISSED` on the other 3 — **new hole (O2), nonce-dependent admission**.

## 1. Method

```
S=/fast/scratch/hyaku/mado-r44/ExecDoNothingV2; D=$S/fixture
git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
git -C "$D" rev-parse --show-toplevel          # == $D (checked before the first commit)
git -C "$D" checkout -q -B v-<name> e4678921   # one commit per variant, identity via -c user.name/-c user.email
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c2-r44-gkeep-size-request-v2.py --repo "$D" --rev "$(git -C "$D" rev-parse HEAD)"
python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo "$D" --rev e4678921 \
        --tool <variant>.py --work $S/work --nonce <nonce>
```

Each variant changes one file — or, for `docs`, six documentation files — against the data commit (MIN,
MINFALSE, WIDE and WIDE2 the entry; LESSON the lesson; olddoc, b4pad5 and b4pad6 the tool). SOURCES.md,
`corpus/README.md` and `fetch/` stay byte-identical in every one of them, so clauses c/d/e/f/h/i are held
constant and only the entry's (or the lesson's) own shape varies; `toolonly` starts from the base tree and adds
the landed tool.

Baselines reproduced before any variant (fixture fidelity):
`receipts/c2-data-baseline.txt` → `admitted=1/1 verdict=TARGET_MET rev=e4678921…`;
`receipts/c1-landed-tool.txt` → `fixtures=26/26 … verdict=TARGET_MET … nonce=doNothingA`.

Builders and runners are in the seat dir: `build-variants.py`, `build-c1-variants.py`, `run-c2.sh`,
`run-docs.sh`, `verify.py`; the variant files they emit are under `variants/`.

## 2. C2 — the entry and the lesson, five shapes

Landed entry: 81 raw lines / 54 non-blank (`receipts/verify.txt`, "entry sizes"). The four entry variants keep the
five cited ids, the quotes and the two census lines; they differ only in what else survives.

| variant | fixture rev | raw / non-blank | keeps | drops | predicate |
|---|---|---|---|---|---|
| MIN | `cd9cb46f` | 27 / 23 | landed header lines 1-12 verbatim; the five `## §` headings; per id one line with the Gate quote + its computed locator + the surface locators; both census lines | the evidence table (landed `:16-24`), every § sentence, the staged-predecessor section (`:64-74`), "what this entry does not establish" (`:76-81`) | `admitted=1/1 TARGET_MET` (`receipts/c2-min.txt`) |
| MINFALSE | `399797f4` | 27 / 23 | the same shapes; the quote and the locators stay exact | the true sentences: every sentence around a locator is false, e.g. the ack handler "stores the size the client chose" (`variants/minfalse.md:21`), which the landed entry itself refutes at `:71-72` | `admitted=1/1 TARGET_MET` (`receipts/c2-minfalse.txt`) |
| WIDE | `0f81ce03` | 28 / 16 | header reduced to title + 5 `source:` + `verified-at` + `recheck`; **one** line of five whole-file ranges (`variants/wide.md:21`); five quote-only lines; both census lines | `ground:`, `Lane:`, `assimilated-from:` and every section heading | `admitted=1/1 TARGET_MET` (`receipts/c2-wide.txt`) |
| WIDE2 | `27bd17ff` | 27 / 15 | the same, with the whole-file ranges folded onto the five quote lines (`variants/wide2.md:21`, `:22`, `:24`) | the separate locator line | `admitted=1/1 TARGET_MET` (`receipts/c2-wide2.txt`) |
| LESSON | `44d1f3d3` | lesson 266 → 29 raw lines | landed entry, registry, README and `fetch/` untouched; the lesson reduced to its title plus `## Gate` | the assimilation ledger, the registry-change log, the closure items and all nine M44 mistake rows | `admitted=1/1 TARGET_MET` (`receipts/c2-lesson.txt`) |

Reproduction of the smallest admitted entry (15 non-blank lines, one of them the title): `variants/wide2.md`,
scored at a commit that replaces only `corpus/knowledge/hyprland-gkeep-size-request-r44.md`; all twelve
`clause=j surface=… cited=1` lines and `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1` are in
`receipts/c2-wide2.txt`.

### Finding C2-1 (DECLARED, confirmed) — MIN is admitted

Attacks: `registration-v2.md:64` — "claim-to-quote binding (CritC2Cheat F1, F6) and registry prose cells (F8) are
the non-author reading". MIN holds exactly five verbatim quotes at their computed locators plus the twelve
surface locators, and no sentence beyond them; the predicate admits it. Severity: none new — this is the
declared residual doing what it says. Reproduction: `receipts/c2-min.txt`, rev `cd9cb46f`.

### Finding C2-2 (DECLARED, confirmed) — MINFALSE is admitted

Attacks: `registration-v2.md:65` — clause j "binds a locator and a keyword per surface, not the truth of the
sentence". With every sentence around the locators false (and one line contradicting the quote it carries on the
same line: `variants/minfalse.md:23` says a zero width "means the compositor picks the size" beside the spec's
own "hint … to the window"), all ten clauses stay 1. Severity: none new. Reproduction:
`receipts/c2-minfalse.txt`, rev `399797f4`.

### Finding C2-3 (OPEN predicate defect O1) — clause j is satisfied by whole-file locator ranges

Attacks: `quality/counters/c2-r44-gkeep-size-request-v2.py:398` —

> `if int(a) <= L <= int(b or a):`

(the clause-j range test; docstring `:56` "surface coverage: for each of the twelve SURFACES (pinned receipt,
anchor text" and `:58` "with a <= L <= b (b = a when absent) and matches the keyword"). The predicate accepts any
range that *covers* the computed anchor line and never bounds its width, and never asks that the range be where
the surface lives. A locator of the whole file therefore counts exactly like a tight one.

Measured: `variants/wide2.md` cites `(Hyprland-Window.cpp:1-3000)`, `(Hyprland-XDGShell.cpp:1-2000)`,
`(xdg-shell.xml:1-3000)`, `(gdktoplevel-wayland.c:1-2000)`, `(gkeep-ui.py:1-500)` and is admitted 12/12 on
clause j (`receipts/c2-wide2.txt`; `variants/wide.md` does the same on one dedicated line). This is w1's
CritClaimSizing F1 class ("an 18-line quote-only entry, admitted while holding none of the claimed surfaces")
returning in weakened form: the entry now holds the *files*, not the surfaces. It is **not** covered by the
residual at `registration-v2.md:64-65`, which speaks about the truth of the sentence, not about a locator's
width; `registration-v2.md` also forbids re-registering after data.

Severity: **medium** — the entry admitted under O1 carries no statement about any of the twelve surfaces, only
their files plus five unrelated quotes; a reader cannot find `sendWindowSize`, the X11 branch, `onAck`, the
deferred `sendConfigure`, the 0x0 case or `application_id` from it. (The five *claim* locators stay exact: clause
g is unaffected; this is a clause-j precision hole, not a quote hole.)

Minimal fix for the L1 to decide on (this seat does not edit the predicate): bound the range, e.g. require
`int(b or a) - int(a) <= 40` in the same test at `:398`, or require the cited range to lie inside the function
whose anchor the surface names. A stronger variant: also require the entry line to carry the surface's anchor
text (the counter already computes it).

### Finding C2-4 (observed, no defect) — the header rows beyond the three counted ones are unscored

Attacks: c2 counter clause b (`:23`, "within its first 20 raw lines, outside fences: >= 4 distinct `source: S###`
lines, exactly one") — `ground:`, `Lane:` and `assimilated-from:` are not read by any clause, so WIDE/WIDE2 drop
them and stay admitted (`receipts/c2-wide.txt`, `receipts/c2-wide2.txt`). Severity: low; no question for the
predicate, but the lane's own convention rows should be named in the residual list if they are meant to bind.

### Finding C2-5 (observed, uncovered surface) — the predicate reads the lesson only through `## Gate`

Attacks: the lesson is read by `section(lesson, "## Gate")` only. Replacing `corpus/lessons/round-44.md` (266 raw
lines at the data commit) with its title and the `## Gate` section — `variants/lesson-gate-only.md`, 29 raw / 24
non-blank lines — leaves every clause at 1: `admitted=1/1 TARGET_MET` (`receipts/c2-lesson.txt`, rev `44d1f3d3`).
So the round's assimilation ledger (the ten-candidate table with its verdicts), the registry-change log, the
round-43 closure items and the nine M44 mistake rows are invisible to the predicate that judges the round's
assimilation. Severity: low for the predicate (its claim is about the entry, and the ledger is a lesson
artifact), but if the ledger is meant to bind, no residual of `registration-v2.md` says so. This seat ran no
other counter, so whether another instrument scores those rows is not established here (`quality/counters/
c2-ledger.py` exists and was not run — it declares `PRED-C2-r36-v1` and a different ledger).

## 3. C1 — the tool and the doc set, six shapes

| variant | scored at | keeps | drops | predicate |
|---|---|---|---|---|
| landed tool | `e4678921` | everything | — | `26/26 TARGET_MET` (`receipts/c1-landed-tool.txt`) |
| olddoc (`variants/c1-olddoc.py`) | `e4678921` + `--tool` | the whole code, byte for byte | the round-44 docstring: the file's contract text is the round-43 one | `clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:1`, `TARGET_MET` on nonce `dn2-c1-olddoc` (`receipts/c1-olddoc.txt`) |
| b4pad5 (`variants/c1-b4pad5.py:283`) | `e4678921` + `--tool` | the state logic; `report` gains `_shape = (1 == 2, 3 != 3, 4 < 3, 5 > 6, 1 <= 0)`, five comparison sites that decide nothing | — | b4 `sites=21 killed=16 need=16` → `b4:1`; overall **`TARGET_MET` on nonce `dn2-pad5-nA`**, `TARGET_MISSED` on `dn2-c1-b4pad5`, `dn2-pad5-nB`, `dn2-pad5-nC` |
| b4pad6 (`variants/c1-b4pad6.py:283`) | `e4678921` + `--tool` | the same with six dead sites | — | `sites=22 killed=16 need=17` → `b4:0`, `TARGET_MISSED` (`receipts/c1-b4pad6.txt`) |
| docs (`run-docs.sh`) | rev `0f1dc4bd` | entry, lesson, SOURCES, README, fetch, tool | SKILL.md, PROVINCE.md, `corpus/QUALITY.md`, `quality/ratio-domain-meta.py`, SCORECARD.md, LOG.md back to base | C1 `TARGET_MET`, C2 `admitted=1/1 TARGET_MET` (`receipts/c1-docs.txt`, `receipts/c2-docs.txt`) |
| toolonly (`run-docs.sh`) | rev `ce5da7d0` | base tree + the landed tool | every other round-44 landing | C1 `TARGET_MET`; C2 `admitted=0/1` (`receipts/c1-toolonly.txt`, `receipts/c2-toolonly.txt`) |

### Finding C1-1 (OPEN predicate defect O2) — the b4 floor is defeated by padding, and admission then depends on the nonce

Attacks: `quality/counters/c1-r44-geometry-states-v2.py:319`:

> `need = math.ceil(KILL_FRACTION * len(sites))`

with `KILL_FRACTION = 0.75` (`:78`) and the site definition at `:31` — "the comparison sites of every function
(selftest, main, usage and functions nested in selftest excluded)". A site is any `Compare` in a function whose
body holds a string containing `fullscreen`; `report()` qualifies because it builds the ` maximized=… fullscreen=…`
summary. Adding dead comparisons there raises `len(sites)` and therefore the bar, so live sites over-kill the
floor: the landed tool has `sites=16 killed=16 need=12`, and with five dead sites `sites=21 killed=16 need=16`
still passes (b4:1, `receipts/c1-b4pad5.txt`). b5 does not see the padding (it only rebinds `json.loads`), and
`registration-v2.md:38` — "b4 is a naming heuristic (b5 carries the teeth)" — does not cover a 24 % dead-site
share.

What turns this into an admission is clause r, which delegates to the round-42 teeth clause and samples rather
than enumerates: `quality/counters/c1-r42-geometry.py:112-113` (`N_MUT = 6`, `KILL_NEED = 4`) and `:931`
`return killed >= KILL_NEED and forced_dead`. Six of the 21 sites are drawn (one forced from the summary
function), so the five dead sites are hit only some of the time. Measured, same tool bytes, four nonces:

- `dn2-pad5-nA` → `clauses=a:1 b:1 b4:1 b5:1 e:1 g:1 r:1` → **TARGET_MET** (`receipts/c1-b4pad5-nA.txt`)
- `dn2-c1-b4pad5`, `dn2-pad5-nB`, `dn2-pad5-nC` → `r:0` → TARGET_MISSED (`receipts/c1-b4pad5.txt`,
  `receipts/c1-b4pad5-nB.txt`)

So the composite C1 verdict on one fixed tool is nonce-dependent: 1 of 4 sampled nonces admitted it. The
predicate's own declared residuals mention b4 as a naming heuristic but say nothing about nonce variance, and
the registration's kill rule ("anything else at the data tip is a miss") presumes a deterministic counter.

Severity: **medium** — the admitted tool still implements the state logic (this is not a content-free tool: the
16 real sites are all killed and the selftest asserts state verdicts), so the hole is dilution, not fabrication;
but the same tool is admitted or rejected depending on the label, and the padding is invisible to a reader.

Minimal fix for the L1 to decide on: require every site to die (`killed == len(sites)`) instead of the 75 %
fraction, or restrict sites to functions that read the state field rather than functions that merely name it, or
make clause r enumerate all sites (deterministic) instead of sampling six.

Boundary, for the record: six dead sites fail b4 deterministically (`sites=22 killed=16 need=17`, b4:0), so the
threshold sits at `len(sites) - killed <= len(sites)/3` exactly as the arithmetic says.

### Finding C1-2 (OPEN predicate defect O3, low) — the tool's own contract text is unscored

Attacks: the c1 counter's residual list (docstring, "Residuals (declared)" — "the documentation rows (SKILL.md,
PROVINCE.md) are not scored") and `registration-v2.md:38-39` ("the SKILL/PROVINCE rows are documentation riding
with C1 and are not scored"). Neither residual names the tool's own docstring, yet the round's M44-3 fix is
stated in terms of it (`corpus/lessons/round-44.md:133`: the TILED row is "not rewritten", while "the tool
docstring narrows TILED to 'not floating'"). Swapping the round-43 docstring back over the round-44 code —
`variants/c1-olddoc.py` — keeps the behaviour and every clause at 1: `TARGET_MET` (`receipts/c1-olddoc.txt`).
The round-43 docstring contains no `NOT_COMPARED` and no state vocabulary at all (verified: count 0 at base,
5 at the data commit, `receipts/verify.txt`), i.e. the shipped tool would document an exit map with no exit 5
and no FULLSCREEN/MAXIMIZED while printing both. Severity: low (documentation-only; a reader of the file is
misled, a caller of `--help` is not, since the tool prints only `SETUP usage`), but it is the M44-3 class inside
the tool file.

Minimal fix for the L1 to decide on: one clause that the tool's source still names the state vocabulary and
`NOT_COMPARED` with exit 5 (a text check, cheap), or an explicit residual sentence naming the tool docstring.

### Finding C1-3 (DECLARED, confirmed) — six documentation files ride free

`docs` = data commit with SKILL.md, PROVINCE.md, `corpus/QUALITY.md`, `quality/ratio-domain-meta.py`,
SCORECARD.md and LOG.md reverted to base: C1 `TARGET_MET`, C2 `admitted=1/1 TARGET_MET` (`receipts/c1-docs.txt`,
`receipts/c2-docs.txt`, rev `0f1dc4bd`). The SKILL/PROVINCE half is declared (`registration-v2.md:38-39`); the
QUALITY criteria 82-84, `quality/ratio-domain-meta.py`, SCORECARD and LOG halves are not named in any residual of
either predicate. Whether some other instrument scores them is outside this seat's scope and was not run.

### Finding C1-4 (DECLARED, confirmed) — C1 is scored on one file

`toolonly` = base tree plus `tools/mado-geometry.py` from the data commit: C1 `TARGET_MET`, C2 `admitted=0/1`
(`receipts/c1-toolonly.txt`, `receipts/c2-toolonly.txt`, rev `ce5da7d0`). This is the separability the
registration states ("C1's counter reads only the tool and the round-42 counter"); recorded as a measurement, not
as a defect. It does mean a C1-only landing needs no entry, no lesson and no registry row to be green.

## 4. What this seat did not find

- No content error in the landed text that this seat read (the round-44 tool docstring, the entry, the lesson's
  Gate block, the registration): the tool's docstring states the order BADSIZE | FULLSCREEN | MAXIMIZED | TILED |
  AGREE | DIFFER and the NOT_COMPARED/exit-5 rule it implements (`tools/mado-geometry.py:59-63`, `:71-76` at
  `e4678921`), and the census lines equal both predicates' recomputation. So no "exact corrected sentence" is
  proposed — the findings above are predicate defects (O1-O3) and observations, and the L1 decides.
- SKILL.md's rows, PROVINCE.md's note and QUALITY criteria 82-84 were not audited for content by this seat; only
  their absence (Finding C1-3) was measured.

## 5. Risks and limits

- **Fixture revs are ephemeral.** The commits `cd9cb46f`, `399797f4`, `0f81ce03`, `27bd17ff`, `0f1dc4bd`,
  `ce5da7d0` live in `/fast/scratch/hyaku/mado-r44/ExecDoNothingV2/fixture`, which this seat deletes. The
  receipts in `receipts/` are the citable evidence; the variant files plus `run-c2.sh` / `run-docs.sh` rebuild
  every commit from `e4678921` with the same trees (a rebuild's commit hashes differ — commit timestamps —
  the tree contents and every clause value do not), except the one nonce-dependent C1 measurement. C1's `b4pad5` result is the one nonce-dependent measurement
  (documented above).
- C2 variants keep SOURCES.md, the lesson, README and `fetch/` at the data commit, so their admission says
  nothing about those files; the claim's own truth is untouched by any of these runs.
- Clause c requires ids present at BASE to keep cells 1-9 byte-equal; every variant reuses the landed ids, so
  that clause is constant across all six fixture commits and was not varied.
- Host: only the allowed compositor reads were not needed here; no compositor command was run. No package
  transaction; no tool installed (system python 3.14 + `bwrap` from the lane's existing counter sandbox).

## 6. Files in this seat dir

`ExecDoNothingV2.md` (this report), `build-variants.py`, `build-c1-variants.py`, `run-c2.sh`, `run-docs.sh`,
`verify.py`, `variants/{c1-landed.py,c1-base-tool.py,c1-olddoc.py,c1-b4pad5.py,c1-b4pad6.py,min.md,minfalse.md,wide.md,wide2.md,lesson-gate-only.md}`,
`receipts/` (c1-landed-tool, c1-b4pad5, c1-b4pad5-nA, c1-b4pad5-nB, c1-b4pad5-nC, c1-b4pad6, c1-olddoc, c1-docs,
c1-toolonly, c2-data-baseline, c2-min, c2-minfalse, c2-wide, c2-wide2, c2-lesson, c2-docs, c2-toolonly, verify).
`receipts/verify.txt` ends `VERIFY: PASS (0 failures)`: every quote above is checked against the cited revision's
blob at the cited line, and every verdict line is grepped out of these receipts.

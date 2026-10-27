# R53Five44 — revenger: C1 accountable-ledger counter and C2 proposition-bound entry repair

seat: `R53Five44` (revenger, leaf — no subagent dispatch, no verdict on any claim)
round: 53, wave w1, lane `mado-shokunin`
base: `ad4bf2059bcfafe63671d262222908ee1fe8001c`
axes named: **operability** (C1), **coverage** (C2). No exploratory claim; no edit to any
tracked lane file; nothing committed.

This seat reconstructs the r52 failure mechanism for both frozen claims from committed
bytes, measures the r51 counter's acceptance of both named bypass classes on a scratch
clone, and returns the **minimal corrected contract** for each — the smallest predicate
that separates production from every *structurally* expressible forgery, with the residual
named instead of papered over. It is evidence and design only: no admission, no vote.

Tag legend: `[OBS]` measured by this seat · `[OBS-cited]` measured by a committed r52 seat
receipt, not re-executed here · `[INF]` composite inference from measured parts.

---

## 1. Axis frame — what each correction buys and what it costs

| Axis | Frozen claim | Move proposed | Measured effect | Harm check |
|---|---|---|---|---|
| operability | C1 instrument-ledger accountability counter | replace the unfalsifiable "instrument-specific context" clause with a **pointer-identity** clause; score description only structurally (non-empty, ≥3 words, unique, not name-restatement); move prose quality to a printed, unscored bound | r51 accepts an 82/82 self-pointer ledger and an 82/82 generic-description ledger (`TARGET_MET`, §3.2); the corrected rules reject every structural fixture I could build (12/12, §3.4) and keep production green | production ledger passes with 0 in every field (§3.4 row 1); the one green control that *should* pass (a legitimate ledger-reader document) still passes |
| coverage | C2 r52 dispatcher entry | bind each proposition to the **enclosing function** and to asserted **locality**, and require a single contiguous anchor | old bytes: 15/18 pass, exactly P16/P17/P18 fail with the routed defect codes (§4.3); corrected set: 6/6 pass (§4.4) | the 15 sound propositions are untouched; no new source row is claimed, so no expansion credit is taken (§4.5) |

No axis is harmed by anything proposed here: every rule that rejects a fixture was also run
against the production ledger and the legitimate control, and returned zero.

---

## 2. Method and inputs

All bytes are committed lane bytes at the base revision or the round-52 pin tree; nothing
was fetched, no host surface was read, no package query, no producer, no service or
compositor probe, no screenshot, no input capture.

| Input | Identity |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/mado-shokunin` at `ad4bf2059bcfafe63671d262222908ee1fe8001c` |
| r51 counter | `quality/counters/c1-r51-ledger.py` (445 L, committed at base) |
| production ledger | `quality/tool-ledger.md` (119 L; 82 data rows; grammar at `:9-13`, cells at `:15-17`) |
| r52 pins | `.ufo/waves/round-52/fetch/{Hyprland-legacy-DispatcherTranslator.cpp,Hyprland-ConfigActions.cpp,Hyprland-ConfigActions.hpp,Hyprland-KeybindManager.cpp}` — digests re-verified by this seat against `SHA256SUMS` **and** against the digests printed in `corpus/SOURCES.md:320-323` (all four match) |
| r52 entry | `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, committed in `56d6e705`, index row at `corpus/README.md` |
| frozen controls | `.ufo/waves/round-52/controls/{c1-do-nothing.md,c1-row-context-control.md,c2-do-nothing.md}` |
| r52 fixtures | `.ufo/waves/round-52/w1/C1Simplify/control-*.md`, `.ufo/waves/round-52/w2/Attack01/controls/*.md` |
| routed defects | `corpus/lessons/round-52-verifier-spotcheck.md:38-60` (§2 C1/C2, §5 items 4-5) |

Source provenance for every C++ byte cited below: Hyprland at immutable commit
`efb50993780079460b0cbed1363e2166a2de1d9f`, opened 2026-10-27 in round 52, digest-pinned in
`.ufo/waves/round-52/fetch/SHA256SUMS`. **No URL was opened by this seat**; no new source
row is due.

Scratch: `/fast/scratch/hyaku/mado-r53/R53Five44` (clone, fixture repos, prototype checkers).
Disk guard read before work: `/fast` 594 G avail, 27 % used. No ENOSPC. No tool was
installed or updated — no install was needed; `python3`, `git`, `sha256sum` suffice.

---

## 3. C1 — operability: why the r52 attempt could not pass, and the minimal fix

### 3.1 Mechanism → bypass, re-derived from the committed counter source

| # | r51 rule (source line) | What it actually tests | Reproduced bypass |
|---|---|---|---|
| M1 | `PLACEHOLDER`, `:76`; `empty_desc` at `:230` | that the description cell is not punctuation-only | any prose, including `Generic accountability note 0 env python3.`, passes. r52's own verdict names this: "r51 counter accepts **repeated** generic descriptions" |
| M2 | `pointer_resolves`, `:206` (`base.encode() in cache[token]`) | that *some* file's bytes contain the row's basename | the ledger itself contains every basename, so a pointer naming the ledger resolves for all 82 rows — the "ledger self-pointer" of the C1 Before text |
| M3 | `dup` accounting | repeated row *path* only | 82 unique paths + 82 identical self-pointers = `ledger_rows == population`, `dup=0` → clean |
| M4 | `checker_ledger` "max" clause | that the lane's `quality/check-tool-ledger.py` agrees with the counter's numbers | measured no discriminative value: the checker implements the same weak predicate and returned `checker ledger ok` on both forged ledgers below (§3.2) |
| M5 | `selftest=ok` in the final line | **the checker's** selftest, not the counter's — `main()`'s argparse declares only `--repo/--rev/--work/--checker` (`:356-361`) | r51 has no `--selftest` at all; the r53 requirement "explicit selftest" cannot be met by reusing these bytes |

### 3.2 Measured before-state (this seat, scratch clone)

Clone of the lane at base into scratch; the fixture repo's toplevel was asserted before each
commit (`git rev-parse --show-toplevel` printed the fixture dir).

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>/work-c1green
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
exit 0
```

Three forged ledgers, each committed in the scratch clone on top of that base; only cell 3
(self-pointer) or cell 2 (generic description) was rewritten, all 82 rows:

| fixture (fixture rev) | counter line | verdict |
|---|---|---|
| every pointer cell → the ledger path `quality/tool-ledger.md` (`6503a28b`) | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok` | **TARGET_MET**, exit 0 |
| every desc → `Generic accountability note <i> env python3.` (`91a7b81f`) | same fields | **TARGET_MET**, exit 0 |
| both (`56e3b865`) | same fields | **TARGET_MET**, exit 0 |

Each run also printed `detail: checker selftest ok (ratio=50/50)` and
`detail: checker ledger ok` — the lane's own checker rubber-stamped the forged bytes, so
M4 adds no accountability. This is the same outcome the r52 verifier recorded and the
`corpus/lessons/round-52-verifier-spotcheck.md:44-58` routed defects name; I measured it
independently rather than parroting it.

Also `[OBS-cited]` (committed r52 receipts, not re-executed here): `w2/Attack01.md` O1-O3
show the uncommitted 78-line r52 rewrite could not pass the *green* clause on the committed
ledger (fenced grammar row parsed as data → `ledger_rows=83 dangling=1`), had no red-signal
fields, and its `--selftest` was a declared-but-never-read no-op; `w2/Attack02.md` P03-P21
show nine self-pointer spellings passing the r52 draft's exact-string `self_pointer` test.

### 3.3 Minimal corrected contract (predicate to freeze)

> **PRED-C1-r53.** `python3 -I quality/counters/c1-r53-ledger.py --repo <lane> --rev <rev>
> --work <scratch> [--ledger <file>]` exits 0 with final line
> `C1_R53: population=<P> ledger_rows=<P> uncovered=0 dangling=0 dup=0 empty_desc=0
> thin_desc=0 dup_desc=0 name_desc=0 bad_pointer=0 self_pointer=0 desc_bound=unscored
> selftest=<n>/<n> verdict=TARGET_MET rev=<rev>`, where at `<rev>`:
> `P` is the population (every file under `tools/`, every direct child `quality/*.py` and
> `quality/counters/*.py`; `__pycache__`/`.pyc`/`.pyo` excluded); every population path
> appears exactly once (`ledger_rows=P`, `dup=0`), no row names a non-population path
> (`dangling=0`), and no population path is unrow­ed (`uncovered=0`);
> **every** backticked token in cell 3 resolves at `<rev>` after canonicalisation
> (leading `./` removed, repeated `/` collapsed, a *numeric* `:N`/`:N-M` suffix removed;
> nothing else) — otherwise `bad_pointer`; **no** token names the ledger path or the row's
> own path, directly or through a `120000` symlink whose resolved target is either —
> otherwise `self_pointer`, and the row fails even if another token is a good witness; at
> least one surviving token is not a symlink and its blob at `<rev>` contains the row file's
> basename — otherwise `bad_pointer`; each description is non-empty (`empty_desc`), ≥3 words
> (`thin_desc`), unique after lower-case/alphanumeric normalisation (`dup_desc`), and not
> built only from the row path's own word segments (`name_desc`).
> Description *meaning* is not scored and the line says so (`desc_bound=unscored`).
> The same command on the frozen no-work control and on each frozen structural forgery
> fixture exits 1 with `verdict=TARGET_MISSED` and the corresponding field non-zero.

Rule precedence is the load-bearing part, and it is two rules, not one:

1. **forbidden-token rule** (any self reference anywhere in the pointer region fails the
   row) — not the r52 draft's "at least one non-self token", which Nine spellings walk past;
2. **existence rule** (a token that does not name a tree path is a defect, not prose) —
   which is what kills the bare-basename / `./` / `(...)` / `:x` / `//` / `/` / case-fold
   spellings that are not paths at all.

Description clause deliberately stops at structure. The r53 target itself says "bounded
structural accountability check, not semantic proof"; the r52 attempt tried to make the
*description* carry the discrimination, and that is the failure to reverse-engineer. My
measurement of the strongest variant I could construct (≥1 description content word present
in the instrument's own bytes past line 1; production coverage 82/82, minimum 3 hits, zero
false positives) still passed every semantic forgery: `control-F3-forged.md` (82 rewritten
descriptions) `generic_desc=0`, `H2n`, `H3n`, `H4n`, `control-H`. `[OBS]`

**Freeze only structural fixtures.** The following are measured out of scope and must be
recorded as a *ceiling*, never as frozen red cases: `Attack01/controls/F-all-forged.md`
(marginal: my rule catches 14/82 rows → MISSED, but only by luck of shebang vocabulary),
`F3`, `H2n`, `H3n`, `H4n`, `control-H`. Freezing any of those as a required `TARGET_MISSED`
reproduces the r52 failure by design, because no bounded lexical rule separates them from
production (r52's own `w2/Attack01.md` says the same: "No lexical configuration of this
clause shape distinguishes a motivated forgery from production").

**Selftest.** The counter's own `--selftest` must build its fixtures in `--work`, print
`C1_R53_SELFTEST: <n>/<n> passed`, and `main()` must AND it into `verdict=TARGET_MET`
(r51 mislabels the *checker's* selftest as its own, M5). One green case (synthetic valid
ledger) and one red case per frozen fixture class, each asserting the *specific* field.

**Scratch.** Every byte from `--rev` in a `--shared` clone inside `--work`; the working
tree is never read; `HOME`/`TMPDIR`/`XDG_*` redirected under `--work`; `--work` created and
removed by the run. r51 already does all of this and it should be kept verbatim.

### 3.4 Measured discrimination of the contract (prototype, scratch only)

Prototype `c1probe.py` (scratch, sha256 `d9319c06…`) implements exactly §3.3's rules over
`git ls-tree`/`git show` at `--rev` plus a caller-supplied ledger file. `[OBS]`

| Fixture | Result fields (non-zero only) | Verdict |
|---|---|---|
| production `quality/tool-ledger.md` @ base | none | **TARGET_MET** |
| `controls/c1-do-nothing.md` (no-work) | `uncovered=81 dup=1 generic_desc=1 bad_pointer=1` | TARGET_MISSED |
| `controls/c1-row-context-control.md` (repeated `A tool.`) | `uncovered=81 dup=1 thin_desc=1` | TARGET_MISSED |
| `C1Simplify/control-B-row-selfpointer.md` | `dup_desc=81 bad_pointer=82 self_pointer=82` | TARGET_MISSED |
| `C1Simplify/control-C-ledger-selfpointer.md` | `bad_pointer=82 self_pointer=82` | TARGET_MISSED |
| `C1Simplify/control-D-generic-desc.md` | `dup_desc=81` | TARGET_MISSED |
| `C1Simplify/control-E-one-selfpointer.md` | `bad_pointer=1 self_pointer=1` | TARGET_MISSED |
| `C1Simplify/control-G-legit-ledger-reader.md` (must stay green) | none | **TARGET_MET** |
| `C1Simplify/mut-{badpointer,dup,emptydesc}.md` | `bad_pointer=2` / `dup=1 ledger_rows=83` / `empty_desc=1` | TARGET_MISSED ×3 |
| `Attack01/controls/F-all-forged.md` | `generic_desc=14` | TARGET_MISSED (marginal; see §3.3) |
| `F3`, `H2n`, `H3n`, `H4n`, `control-H` | none | TARGET_MET — declared ceiling |
| 3-instrument fixture `fix/p9`, base `8711e68` + legitimate pointer `d39f9e5` | none | **TARGET_MET** |
| same fixture, the nine Attack02 spellings (P03/P04/P05/P06/P07/P19/P20/P21/P09), one commit each | `bad_pointer=1` ×7, `self_pointer=1` ×2 (double-slash, symlink alias) | TARGET_MISSED 9/9 |
| same fixture, one population file added with no row (`03cfc3b8`) | `population=4 ledger_rows=3 uncovered=1` | TARGET_MISSED (own-row burden enforced) |

The last two rows are the ones the r52 draft could not pass: identity-based self exclusion
(including a `120000` alias whose target is the row's own file) and exact population
arithmetic against the counter's own future row.

### 3.5 Divergences recorded (not fixed here)

| # | Divergence | Evidence | Class |
|---|---|---|---|
| D1 | r51's `selftest=ok` token reports the *checker's* selftest; the counter has no selftest | `c1-r51-ledger.py:356-361`, `checker_selftest()`; measured `detail: checker selftest ok (ratio=50/50)` | S2 — the r53 "explicit selftest" clause cannot be satisfied by reuse |
| D2 | The `max` (checker-agreement) clause has zero discriminative power on forged bytes | §3.2 three runs, each `checker ledger ok` on 82 forged rows | S2 — keep the clause only as parroting protection |
| D3 | `quality/tool-ledger.md:27` records "Five superseded v1 counters have no lane-level document naming them"; under §3.3 those rows still need a non-symlink witness naming the basename — they pass today (all 82 rows green), but the note means any future re-point must name a registration file, never the ledger | measured 82/82 green | S3 — informational |
| D4 | Population 79 (ledger header, round-51 base) → 82 at base tip; committing `c1-r53-ledger.py` raises it to 83 and *requires* its own row in the same commit | `c1-r51-ledger.py` run: `population=82`; fixture row above | S3 — arithmetic to freeze in the predicate text |

---

## 4. C2 — coverage: why quote-at-anchor cannot catch P16-P18, and the minimal fix

### 4.1 The three defects re-derived from the pin bytes (opened bytes, not the report's prose)

Pin: `.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp` (sha256
`7248cbb8…`) and `Hyprland-ConfigActions.cpp` (sha256 `a83abeb5…`), both byte-identical to
`corpus/SOURCES.md:320-321`.

**P16 — spliced quote + two-region locator.** Entry cells: anchor
`Hyprland-ConfigActions.cpp:1554-1558,1576`, quote
``g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);``.
The pin has, at `:1554`, the modifier send; at `:1556-1557`,
`if (S.m_passPressed == 1) { if (!isMouse)`; at `:1558` only then the PRESSED key send; at
`:1561` the `m_passPressed == 0` release branch; at `:1576` the zeroed modifier send. The
space-joined quote is contiguous nowhere, and the elided guard is material: the quoted press
is branch-conditioned. `[OBS]` The anchor cell also names two disjoint regions, which no
single-position binder can check.

**P17 — wrong subject + duplicate.** Entry says "`sendshortcut`'s repeat branch …"; the
quoted bytes `:619-622` sit inside `sendkeystate` (`:591-627`); `sendshortcut` spans
`:531-589` and contains no repeat logic. Add: P17's quote is a whitespace-collapsed substring
of P04's quote on the same pin and anchor — a second, independent defect. `[OBS]`

**P18 — wrong locality.** Entry says the `key not found` return is "inside the scan"; the
return is at `:574`, the scan loop is `:565-571`, so the return is *after* the loop, inside
`if (!keycode)` on the cache-miss branch (`:575` is the cache-hit `else`). `[OBS]`

### 4.2 Why the r52 counter shape necessarily passes P17 and P18

r52's counter family checks quote-at-anchor (contiguity + word cap + pin digest); the routed
`w2/Attack07.md` T1 defect is even weaker — its regex expects `| P## | S### | …` while the
entry table is `| P## | Proposition | S### | …`, so `props=0 TARGET_MISSED` on the landed
bytes, and a fabricated quote passes once the column order is fixed `[OBS-cited]`. But the
decisive point is structural: **P17's and P18's quotes are contiguous and inside their
anchors** — my probe measures `contiguous=True in_anchor=True` for both (§4.3). A
quote-at-anchor counter therefore *cannot* reject them, no matter how the columns are
parsed. The defects live in the proposition's **claims about the code** (who encloses it,
where it sits relative to a loop), so the counter must bind those claims to the pin's
geometry.

### 4.3 Measured: the old bytes under the corrected content rules

Prototype `c2probe.py` (scratch, sha256 `48ac1889…`); header-driven column mapping; strict
anchor containment (quote must be a whitespace-collapsed substring of the cited range only);
scope derived from column-0 definitions in the pin; loop geometry from brace matching; a
locality lexicon bound to that geometry. `[OBS]`

```
C2_PROBE: The action sends modifier state before the key event, then clears the modifier state. ok=NO words=9 contiguous=False in_anchor=False scope=Actions::pass anchor_not_single_contiguous_range
C2_PROBE: `sendshortcut`'s repeat branch can invoke its delegate twice for a successful repeat state. ok=NO words=9 contiguous=True in_anchor=True scope=sendkeystate scope_mismatch:named=sendshortcut enclosing=sendkeystate
C2_PROBE: An unresolved keysym returns the `key not found` error inside the scan. ok=NO words=10 contiguous=True in_anchor=True scope=sendshortcut locality:claims-inside-loop but anchor 574 outside [(565, 571)]
C2PROBE: props=18 fails=3 verdict=TARGET_MISSED
```

15/18 old propositions pass (max 19 words), and the three failures are exactly P16, P17, P18
with the routed defect classes; zero false positives on the other fifteen.

The independent duplicate rule, measured on the same bytes:

```
DUP_PROP: P17 quote is substring of P04 quote (9 words)
```

### 4.4 Minimal corrected contract (predicate + schema to freeze)

> **PRED-C2-r53.** `python3 -I quality/counters/c2-r53-dispatch-repair.py --repo <lane>
> --rev <rev>` exits 0 with
> `C2_R53: props=<N> active=<N> superseded=3 fails=0 codes=P16:spliced_quote+multi_anchor,
> P17:wrong_scope+duplicate,P18:wrong_locality pins=4 pins_ok=4 index=1 verdict=TARGET_MET`,
> and on the frozen old-bytes fixture (the r52 entry at `56d6e705`) prints
> `fails=3` with exactly those codes and `verdict=TARGET_MISSED`.

Content rules, each mechanically derived from the pin:

- **R1** quote ≤ 25 whitespace words;
- **R2** whitespace-collapsed quote is a contiguous substring of the cited anchor range
  *only* — not of ±N surrounding lines;
- **R3** the anchor is one contiguous `a` or `a-b` range; a comma-separated locator is
  `multi_anchor`;
- **R4** if the proposition names a function in backticks and that name is defined in the
  pin, the function enclosing the anchor's first line must be that function (definitions
  read from column-0 signature lines; member definitions compare by qualified name);
  otherwise `wrong_scope`. Backticks only — free prose must not trigger R4, or common words
  match `Actions::state`/`Actions::event`;
- **R5** asserted locality: `inside|within … loop|scan|iteration` ⇒ the anchor lies within a
  `for (` header's brace span; `after|once|following|outside … loop|scan` ⇒ it does not;
  otherwise `wrong_locality`;
- **R6** no two *active* propositions on the same pin may have one quote a
  whitespace-collapsed substring of the other — otherwise `duplicate`;
- **R7** each pin's sha256 equals the digest printed in the cited `corpus/SOURCES.md` row
  (S370-S373) and in `.ufo/waves/round-52/fetch/SHA256SUMS`;
- **R8** the entry is indexed in `corpus/README.md` and every cited `S37x` row exists.

Append-only repair mechanics (the part that makes R1-R8 bite without rewriting history):

- the original 18-row table stays byte-identical; the repair is an **appended correction
  table** with three added columns `status` (`active`/`superseded`), `supersedes`
  (`P16`/`-`), and `defect` (comma-separated codes from
  `{spliced_quote, multi_anchor, wrong_scope, wrong_locality, duplicate}`);
- the counter's scored set is `(original rows − superseded) ∪ correction rows`;
- for every superseded id the counter (a) re-derives that row's defect codes from R1-R6,
  (b) requires an active row whose `defect` cell equals that derived set, and (c) requires
  the old proposition text to be quoted verbatim in the correction section — so a supersede
  map cannot be invented, and the old bytes cannot be re-labelled "active";
- a missing `status` column (i.e. today's bytes) means "all rows active" → the old entry
  fails R2/R3 on P16, R4+R6 on P17, R5 on P18. That is the "rejects the old bytes" clause.

### 4.5 Corrected propositions (measured against the same pins)

Fixture table: `/fast/scratch/hyaku/mado-r53/R53Five44/corrected-entry.md` (sha256
`164e23bf…`). Each row is one contiguous anchor with a contiguous quote, and each repairs
one routed defect code. `[OBS]`

| new id | replaces | pin:anchor | quote (words) | scope derived | verdict |
|---|---|---|---|---|---|
| P19 | P16 | `Hyprland-ConfigActions.cpp:1554` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` (4) | `Actions::pass` | pass |
| P20 | P16 | `Hyprland-ConfigActions.cpp:1556-1558` | `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` (12) | `Actions::pass` | pass |
| P21 | P16 | `Hyprland-ConfigActions.cpp:1576` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (4) | `Actions::pass` | pass |
| P22 | P17 | `Hyprland-ConfigActions.cpp:1611-1613` | `auto result = Actions::pass(modMask, key, w); if (keyState == 2 && result.has_value()) result = Actions::pass(modMask, key, w);` (17) | `Actions::sendKeyState` | pass |
| P23 | P18 | `Hyprland-legacy-DispatcherTranslator.cpp:573-574` | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` (12) | `sendshortcut` | pass |
| P24 | (new) | `Hyprland-legacy-DispatcherTranslator.cpp:575-576` | `} else keycode = g_pKeybindManager->m_keyToCodeCache[KEYPAIRSTRING];` (5) | `sendshortcut` | pass |

```
C2PROBE: props=6 fails=0 verdict=TARGET_MET
```

Two design notes the round must not skip:

1. **A one-word "fix" to P17 is not sufficient.** Changing "`sendshortcut`'s repeat branch"
   to "`sendkeystate`'s repeat branch" satisfies R4 but still fails R6, because P17's quote
   is a substring of P04's quote at the same anchor — the repair must either bind different
   bytes (P22, the seat-level twin at `:1601-1618`, which no proposition cited) or merge P04
   and P17. This is a *measured* consequence, not a preference.
2. **P20's quote is a syntactically open span** (the `{` opened at `:1556` closes later). R2
   accepts it because it is byte-contiguous inside the anchor; the contract should state that
   the quote need not be a complete statement, only a contiguous in-anchor span, otherwise
   the guard — the very thing P16 spliced out — cannot be quoted.

**Expansion credit: none, and this is not a coverage gain.** S371's declared region already
spans `1530-1616` and S370's spans `531-627`, so P22 and P24 bind ground *inside* rows opened
in round 52 — they are not "uncovered ground per coverage map" (`corpus/SOURCES.md:320-321`).
The frozen C2 text withholds credit absent an entry resting on a row opened *this* round; a
source-only repair seat cannot open one. The repair is a **quality** move on already-admitted
ground: it converts a committed entry that the closure graded *harmed* into one whose
proposition table fails nothing (`corpus/lessons/round-52-verifier-spotcheck.md:64`).

---

## 5. Evidence chain (exact commands)

```
$ sha256sum .ufo/waves/round-52/fetch/*.cpp .ufo/waves/round-52/fetch/*.hpp
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  …/Hyprland-ConfigActions.cpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  …/Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  …/Hyprland-legacy-DispatcherTranslator.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  …/Hyprland-ConfigActions.hpp
   (all four equal the digests printed in corpus/SOURCES.md:320-323)

$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>/work-c1green
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET …
# same counter on three scratch-clone forgeries (§3.2): TARGET_MET each, exit 0

$ awk 'NR>=1554 && NR<=1578 {printf "%d|%s\n", NR, $0}' …/Hyprland-ConfigActions.cpp
1554|    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);
1556|    if (S.m_passPressed == 1) {
1557|        if (!isMouse)
1558|            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
1576|    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
$ awk 'NR>=565 && NR<=576 {…}' …/Hyprland-legacy-DispatcherTranslator.cpp
565|            for (xkb_keycode_t kc = keycode_min; kc <= keycode_max; ++kc) {
571|            }
573|            if (!keycode)
574|                return {.success = false, .error = "sendshortcut: key not found"};
575|        } else
576|            keycode = g_pKeybindManager->m_keyToCodeCache[KEYPAIRSTRING];
$ grep -n "^static SDispatchResult send" …/Hyprland-legacy-DispatcherTranslator.cpp
531:static SDispatchResult sendshortcut(const std::string& args) {
591:static SDispatchResult sendkeystate(const std::string& args) {

$ python3 -I c2probe.py --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --pins .ufo/waves/round-52/fetch
C2PROBE: props=18 fails=3 verdict=TARGET_MISSED          # P16, P17, P18 only
$ python3 -I c2probe.py --entry corrected-entry.md --pins .ufo/waves/round-52/fetch
C2PROBE: props=6 fails=0 verdict=TARGET_MET
```

Additional measured anchors: production ledger = 82 rows, 82 unique normalised descriptions,
0 rows shorter than 3 words, 0 name-restatements, 0 unresolvable pointer tokens, 0 self
pointers; and 82/82 descriptions share ≥3 content words with their instrument's bytes past
line 1 (the strongest production-clean lexical rule I found — still defeated by F3, §3.3).

---

## 6. Divergences, confidence, limits

| Item | Statement | Confidence |
|---|---|---|
| C1 failure cause | the claim asked a *description* clause to do semantic work; both r52 counter shapes are lexical and the forgeries are drawn from the instruments' own vocabulary, so every filter is either bypassable or production-rejecting | high — measured on the r51 bytes and on the strongest rule I could build |
| C1 minimal fix | pointer identity (all tokens resolve; no self; ≥1 non-symlink witness) + exact population + description structure only | high for the pointer/population rules (9/9 + 82/82 measured); the description rules are structural and their ceiling is declared, not hidden |
| C2 failure cause | the counters bind quotes to anchors, but P17/P18 are *claims about location and scope* with byte-perfect quotes — only scope/locality bindings can reject them | high — probe measures `contiguous=True in_anchor=True` for both |
| C2 minimal fix | R1-R8 + append-only supersede/defect-code table | high for P16 (contiguity + multi-anchor) and P18 (loop geometry); medium for P17's duplicate clause, which is a new requirement and needs its own control (a legitimate entry where two propositions quote overlapping lines for genuinely different reasons would be a false positive — none exists in the r52 entry, measured) |
| Not measured here | whether the round-53 registration will freeze structural or semantic forgery fixtures; that choice decides whether C1 is provable this round | `[UNK]` — decision, not evidence |

Limits: this seat ran prototypes, not the frozen counters; it made no admission decision and
is **not** a non-author reviewer. Semantic entailment beyond R1-R8 is untouched: the
corrected propositions are byte-bound and geometry-bound, not proven to entail their
sentences. `[INF]` where a statement combines two measured parts; everything else is `[OBS]`.

No tracked file was modified, no git/jj mutation outside scratch fixtures (each fixture
commit asserted `git rev-parse --show-toplevel` printed the fixture dir), no subagent, no
background job, no install, no package query, no live host read, no network fetch.

Report trailer (paths relative to the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`):

- report: `.ufo/waves/round-53/w1/R53Five44.md`
- scratch: `/fast/scratch/hyaku/mado-r53/R53Five44` (clone `fix/repo`, fixture `fix/p9`,
  prototypes `c1probe.py`/`c2probe.py`, `corrected-entry.md`, matrix receipts `c2-old.txt`,
  `c2-new.txt`) — removed before yield

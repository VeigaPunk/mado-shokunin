# R53One8 — revenger: reconstruct the r52 failure, name the minimal corrected contract

Seat `R53One8` (revenger, leaf — no dispatch, no git/jj mutation, no tracked edit).
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`
(`git -C … rev-parse HEAD` → `ad4bf2059bcfafe63671d262222908ee1fe8001c`; `git status --porcelain` → `?? .ufo/waves/round-53/` only).
Axes named: **operability** (C1) and **coverage** (C2). Every number below is measured on committed bytes at that rev;
nothing was probed live and nothing was installed. No seat counts as non-author reviewer, including this one.

**Attacked predicates.**
- C1 (frozen, `.ufo/waves/round-53/claims-frozen.md`): *"a newly committed, scratch-aware counter with explicit selftest
  returns TARGET_MET on the production ledger, TARGET_MISSED on a no-work control and each frozen forgery fixture, with
  exact population coverage and non-self pointers … a bounded structural accountability check, not semantic proof."*
- C2: *"append-only correction clearly repairs those three propositions against opened pinned source bytes; a frozen
  counter rejects the old bytes and accepts corrected entry with quote/pin/proposition bindings."*
- The r52 clauses these replace are quoted where attacked (§2).

Deliverable in one sentence: **C1 is satisfiable under its r53 wording only if its description clause is restated as
repetition/shape and its residual is named in the claim; C2's three defects are mechanically decidable against the
pinned bytes, and the minimal repair is one retirement (P17), one re-localization (P18) and one split (P16) — not a
reword, because the ≤25-word quote cap forbids a single-row fix.** Evidence and clause matrix in §3–§5.

---

## 1. Method

Read-only over the lane; scratch only at `/fast/scratch/hyaku/mado-r53/R53One8` (disk guard `df -h /fast` →
`596G` available). Tools: `git` (plumbing reads), `python3` (stdlib). **No tool installed, nothing updated.**
Four instruments in scratch, all reading committed bytes:

| scratch file | sha256 | role |
|---|---|---|
| `production-ledger.md` | `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b` | `git show ad4bf20:quality/tool-ledger.md` — the production ledger under test |
| `matrix.py` | `243c3d8568107dcf7aed5bdffed7500a698f300619ee7a7621dc9e43650b2c53` | prototype of the *corrected C1 clause set*, run over production + 13 frozen fixtures + 8 generated pointer spellings + 1 residual probe |
| `measure_c1.py` | `70020118321cf5c99d1b468f3b75fa9571587807e5f99227fbff0c9cf045af6d` | description-shape census (words, distinctiveness, verbatim share) |
| `verify_c2.py` | `2fab2a3eef224bff9691407cc0b587dea269729f2cb91a71f120b096db710de7` | C2 quote contiguity, span containment, function/loop span computation |

`matrix.py` is a **prototype, not the counter**: it demonstrates which clause set separates production from the frozen
fixtures. No file was created in the lane.

---

## 2. Reconstructed prior-round failure (executable evidence, no assumption)

### 2.1 C1 — the r51 counter is blind to both defects the claim names

Before-state, re-measured at the frozen rev:

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
      --work /fast/scratch/hyaku/mado-r53/R53One8/work-r51
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf2059bcfafe63671d262222908ee1fe8001c)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
exit=0
```

Three defects are visible in that line and in the source, not inferred:

1. **No self-pointer field and no description-context field exist.** `describe()` (`:211-250`) computes
   `uncovered, dangling, bad_pointer, empty_desc, dup` only; `pointer_resolves()` (`:196-210`) accepts any token whose
   bytes contain the row's basename, including `quality/tool-ledger.md` itself — the ledger contains every basename, so
   a ledger self-pointer is `bad_pointer=0`. `empty_desc` fires only on `PLACEHOLDER = ^[\s\-–—_*`.]+$`
   (`:76`), i.e. on emptiness, never on "repeated generic description".
2. **`REFUSED_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")` (`:68`) is advisory only.** Its two use sites are `:404-407`,
   inside the branch that prints `detail: hint: the gate refuses --selftest work under …`. `resolve_work()` (`:331-348`)
   never consults it — `--work /tmp/x` is accepted. The r53 claim asks for a *scratch-aware* counter; the predecessor
   is scratch-hinting.
3. **No `--selftest` of its own.** `main()` (`:356-445`) declares only `--repo/--rev/--work/--checker`; the selftest we
   see in the line is the *checker's* (`checker_selftest`, `:278-301`). "Explicit selftest" is a new obligation, not an
   inherited one.

So the r52 "Before" sentence in `claims-frozen.md` — *"r51 counter accepts repeated generic descriptions and ledger
self-pointers"* — is exactly right, and the reason is structural blindness, not a threshold set too loose.

### 2.2 C1 — where the r52 attempt actually broke

Nothing was committed: `git ls-tree -r --name-only HEAD quality/counters/ | grep -c r52` → `0`. Both byte sets that
were measured in wave 2 are therefore drafts, and the failure has four separable layers:

| layer | measured failure | evidence (committed wave bytes, not re-executed by me) |
|---|---|---|
| L1 predicate mixes decidable and undecidable surfaces | "instrument-specific functional context" is prose entailment in disguise | attack A: a description built as `Generic accountability note <i> <phrase>` with `<phrase>` a real 2-word slice of the instrument's own bytes passes 82/82 | 
| L2 non-self test is exact-string equality | 9 spelling variants pass: bare basename, own basename, `./`, trailing `)`, `:x` suffix, `//`, leading `/`, case fold, and a mode-120000 symlink alias | attack B probes P03–P07, P19–P21, P09 |
| L3 landed bytes ≠ reviewed bytes | reviewed draft 847 lines (`sha256 0fe862f1…`), landed rewrite 78 lines (`sha256 923faf02…`, untracked) with all four context filters absent, no selftest body, no fence skip | attack A T2/T3/O1–O3 |
| L4 the landed rewrite fails its own green arm | `population=82 ledger_rows=83 … dangling=1 bad_pointer=1 verdict=TARGET_MISSED` on the *production* ledger, because the fenced grammar example at `quality/tool-ledger.md:11-13` is parsed as a data row | attack A O1 |

L1 and L2 are design errors; L3 is the process error that made L4 invisible until integration. **L3 is the one a
contract can close cheaply**, and the r52 wave never did: the demonstration receipt never bound a digest to the
committed file.

### 2.3 C2 — the three defects, re-verified by me against the pinned bytes

Pins are the committed fetch copies; I re-verified their digests before quoting:
`cd .ufo/waves/round-52/fetch && sha256sum -c SHA256SUMS` → five `OK`, `exit=0`.
Source rows S370–S373, URL as registered at `corpus/SOURCES.md:320-323`
(`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/...`), access date
`2026-10-27`, pinned revision `efb5099…`.

Mechanical verdicts from `python3 -I verify_c2.py` (entry = `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`):

```
P01  contiguous=True  in_span=True   enclosing=sendkeystate   pin=…DispatcherTranslator.cpp:591-594
…
P16  words=9  contiguous=False in_span=False enclosing=-       pin=…ConfigActions.cpp:1554-1558,1576  quote_line=None
P17  words=9  contiguous=True  in_span=True  enclosing=sendkeystate pin=…DispatcherTranslator.cpp:619-622  quote_line=621
P18  words=10 contiguous=True  in_span=True  enclosing=sendshortcut  pin=…DispatcherTranslator.cpp:574    quote_line=574

function spans (brace-matched from the pinned bytes):
  sendshortcut   531-589
  sendkeystate   591-627
  ConfigActions::pass  1530-1599
loop spans (DispatcherTranslator.cpp): (565, 571)
```

- **P16 — spliced quote.** The entry's quote joins `:1554` with `:1558`; the bytes between them are
  `:1556 if (S.m_passPressed == 1) {` and `:1557 if (!isMouse)`. Mechanical result `contiguous=False`. Consequence of the
  ≤25-word cap, not of sloppiness alone: the contiguous block `:1554-1558` is 16 words only *because* it drags both
  guards in; a 9-word splice was the only way to quote the two bare calls. **A single-row repair cannot keep the
  current proposition wording** (`g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(…);`
  at 9 words is not in the file; the real contiguous span is
  `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` = 16 words).
- **P17 — misattributed subject.** The proposition says *"`sendshortcut`'s repeat branch can invoke its delegate twice"*.
  The quoted line `:621` (`if (keyState == 2 && result.success)`) and `keyState` itself (`:600`) lie inside
  `sendkeystate` (`591-627`); `sendshortcut` (`531-589`) has no `keyState`. There is no "repeat branch" in
  `sendshortcut`. Mechanical result: `enclosing=sendkeystate` while the proposition names `sendshortcut`.
  And the correct proposition already exists in the same entry as **P04**, pinned at `:619-622`.
- **P18 — mislocalized.** The proposition says the return is *"inside the scan"*. `:574` is 3 lines **after** the scan
  loop closes at `:571`; it is inside the cache-miss `if (!g_pKeybindManager->m_keyToCodeCache.contains(KEYPAIRSTRING))`
  block (`:559-575`) and guarded by `if (!keycode)` (`:573`), i.e. after the scan, not inside it.

Also measured, and new: **the committed receipt does not cover the committed entry.** `w1/C2EntryDraft/quotes-check.txt`
scores a different proposition set — its `P16` is `ConfigActions.cpp:47-49 words=8`, its `P17` is `:1578-1579`, while the
committed entry's P16/P17 are `ConfigActions.cpp:1554-1558,1576` and `DispatcherTranslator.cpp:619-622`. The receipt was
produced from the draft TSV, not from the landed table — the same "reviewed artifact ≠ landed artifact" class as C1 L3,
and the reason `verdict=OK` was printed over three false rows.

### 2.4 Routed r52 defects, confirmed as evidence (they are inputs to the contract, not my findings)

1. `corpus/lessons/round-52.md:5-19` `## Gate` has instruction text but **no per-row record** (URL, date, ≤25-word
   located quote) for S370–S373; CORPUS SOURCES rule 1 requires one per new row.
2. `:23-25` `## Changes` reads `Pending final integration revisions and receipts.` against a landed tree — stale.
3. QUALITY 17 (`corpus/QUALITY.md:34`) distinct-scope review for S370≡S365, S371≡S367, S373≡S364 is still owed;
   `corpus/SOURCES.md:374` itself says `distinct-scope review remains outstanding`.
4. The entry's P16–P18 are unmarked where a reader consumes them (`corpus/README.md:80` indexes the file).
5. SHONEN boxes unchanged; promotion is operator-owned (not my surface).

---

## 3. C1 — corrected contract, clause by clause, with measured margins

The r53 wording is achievable **iff** the description clause stops pretending to be semantic. The prototype
(`matrix.py`) grades production and every frozen fixture with the clause set below; the run is deterministic on
committed bytes:

```
$ cd /fast/scratch/hyaku/mado-r53/R53One8
$ python3 -I matrix.py
```

| case | self | bad_ptr | uncovered | dup | desc_empty | desc_dup | desc_short | prefix_viol | verdict |
|---|---|---|---|---|---|---|---|---|---|
| **production (ad4bf20)** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **TARGET_MET** |
| control-G (legit ledger reader, green arm) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **TARGET_MET** |
| control-do-nothing (frozen no-work) | 1 | 1 | 81 | 1 | 0 | 0 | 1 | 0 | MISSED |
| control-row-context (`A tool.` ×2) | 0 | 0 | 81 | 1 | 0 | 0 | 1 | 0 | MISSED |
| control-B (row self-pointer) | 82 | 82 | 0 | 0 | 0 | 81 | 82 | 82 | MISSED |
| control-C (ledger self-pointer) | 82 | 82 | 0 | 0 | 0 | 0 | 0 | 0 | MISSED |
| control-D (repeated generic) | 0 | 0 | 0 | 0 | 0 | 81 | 82 | 82 | MISSED |
| control-E (one self-pointer) | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | MISSED |
| control-F3 (phrase-copy forgery) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 82 | MISSED |
| control-H / H2n / H3n / H4n (name-only) | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | MISSED |
| F-all (82 forged descriptions) | 0 | 0 | 0 | 0 | 0 | 0 | 82 | 82 | MISSED |
| S03/S04/S05/S06/S07/S19/S20/S21 (8 spellings) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | MISSED |
| RESIDUAL padded-generic (my probe) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **TARGET_MET** |

`3` MET (production, green control, residual probe) and `20` MISSED in the receipt. The residual probe is the point of
the last row: **the claim must name it or it is false.**

### 3.1 The clauses

- **C1-1 Population exactness.** Population computed at the scored rev by the declared rule (`tools/**`, `quality/*.py`,
  `quality/counters/*.py`, `__pycache__`/`.pyc` excluded, `.sh` only under `tools/`) must satisfy
  `uncovered = dangling = dup = 0` and `ledger_rows == population`. Measured: `population=82 ledger_rows=82` at ad4bf20.
- **C1-2 Fence-aware parse.** Fenced blocks are documentation. Measured: `quality/tool-ledger.md` has 83 pipe rows,
  82 data rows; the 83rd is the grammar sample at `:11-13`. O1 of r52 was the regression that broke this.
- **C1-3 Accountable pointer.** ≥1 pointer token resolves **case-exactly** to a blob at the rev; that blob is not the
  ledger, not the row's own path, not a population instrument, **not git mode 120000**, and its bytes contain the row's
  basename. Measured on production: `bad_pointer=0`; 8 rows legitimately point at `.ufo/waves/round-N/registration.md`
  (dot-prefixed paths must survive token normalization: my own first pass over-normalized with a leading-dot strip and
  produced 8 false `bad_pointer` on exactly those rows; r51's `token()` (`:177-195`) strips only `` `*_ \t `` and keeps
  `.ufo/…` intact, so this is a trap for a rewrite, not an inherited defect).
  The 120000 rule is required by attack B P09/P10; the lane tree has 38 mode-120000 blobs today (all under
  `.ufo/waves/round-1x/tripwire/**`), and no production pointer names one, so the clause is inert on production.
- **C1-4 Non-self identity, normalized, two tiers.** Tokens are canonicalized (backticks/emphasis stripped, `./`,
  leading `/`, repeated `/`, casefold, `:suffix`, trailing junk) and compared with `{ledger path, ledger basename,
  row path, row basename}`.
  *Tier 1, pointer region (cells 2+): unconditional.* Kills the 8 spellings and the 4-cell frozen control.
  *Tier 2, description cell: conditional on the instrument's own bytes not naming the token.* This exemption is
  **measured necessary**: control-G is the green arm and its `quality/check-tool-ledger.py` row reads
  `Reads \`quality/tool-ledger.md\` and reports each instrument's accountability row.` — a true description of a ledger
  reader. A blanket wide scan turns the green control red (`self=1`), which I measured before adding the exemption.
  With the exemption: production `self=0`, control-G `self=0`, control-do-nothing `self=1` (its 4-cell row names the
  ledger in the cell that *is* the pointer region), control-C/E/spellings `self≥1`.
- **C1-5 Description shape — structural, not semantic.** (a) non-empty; (b) ≥8 whitespace words; (c) pairwise distinct
  after casefold; (d) no 3-word prefix shared by more than 4 rows. Measured margins:
  production min 9 words (`quality/counters/c2-r51-dispatch-entry.py`), median 23, max 34, all distinct,
  **max 3-word-prefix multiplicity = 3** (`static resolver of`, `read-only census of`); F3 and F-all share
  `generic accountability note` across 82 rows; control-D/B share `accountability row for` across 82; F-all rows are 6
  words; H4n's forged row is 7 words. So (b) at 8 is the smallest floor that kills F-all (6) and H4n (7) while keeping
  production (min 9); (d) at cap 4 is the smallest cap that kills F3 (82) while keeping production (max 3).
  **This is the whole answer to "how do we reject the F3 fixture structurally": we do not inspect meaning, we detect
  that 82 rows begin with the same three words.**
- **C1-6 Explicit selftest.** `--selftest` must be a real arm, offline (`--repo` not required), counted, and must
  include: a synthetic green mini-ledger, a synthetic red twin per clause (population, fence, pointer, self, floor,
  prefix, duplicate), and **one mutant of the green fixture that only changes one description length** — a counter that
  hash-pins production passes the first but not the mutant. Output `C1_R53_SELFTEST: n/n passed`; a no-op `--selftest`
  is a predicate failure (the exact r52 O3 defect: flag declared, never consulted). With `--repo/--rev`, additionally
  verify each frozen fixture's digest against `.ufo/waves/round-52/{controls,w1/C1Simplify,w2/Attack01/controls}/*.md`
  at that rev.
- **C1-7 Verdict map.** 0 `TARGET_MET`, 1 `TARGET_MISSED`, 2 `SETUP`; one line carrying every field; **an unevaluable
  clause is SETUP, never MET** (a counter that cannot compute a function span, a pin, or a mode must not print green).
- **C1-8 Scratch-awareness (enforced).** An explicit `--work` whose realpath is or lies under `/tmp`, `/var/tmp`,
  `/dev/shm` → exit 2; default `--work` from `TMPDIR` with the same refusal; remove only what the run created.
  r51 only hinted (`:405-407`); the r53 claim says "scratch-aware", so this is the delta.
- **C1-9 Reviewed = landed (digest binding).** The demonstration receipt records the counter's sha256 and the landing
  commits exactly those bytes; a rewrite after review is a *new* instrument requiring its own controls. This is the
  single cheapest clause that closes the r52 failure mode (847-line reviewed draft vs 78-line landed rewrite) and it is
  not a semantic claim, so it does not enlarge the predicate.
- **C1-10 Self-row.** The counter is a population member: committing it moves `pop` 82 → 83 and forces a ledger row
  naming it, whose pointer must be a *different* tracked file naming its basename. `.ufo/waves/round-53/` is untracked at
  base (`git ls-tree -r --name-only HEAD | grep -c round-53` → `0`), so the landing commit must also create
  `.ufo/waves/round-53/registration.md` (naming `quality/counters/c1-r53-*.py`), and the counter must be scored at that
  commit. At base the row is absent → honest `TARGET_MISSED`.

### 3.2 The residual the claim must print

Two shapes pass every structural clause I could calibrate without touching production:

1. **Varied-prefix ≥8-word filler** (my `RESIDUAL-padded-generic` row): 12 words, unique, no shared prefix, pointer
   production-verbatim → `TARGET_MET`. Padding defeats (b) and (d); only semantics would catch it.
2. **Registry / cycle of non-population documents** (attack B P13/P14): each row points at a document that names its
   basename; the documents are a shared registry or a two-row cycle. Structurally accountable, evidentially worthless.

Clauses that *would* touch shape 1 all fail production, measured: "description must contain a code-form token that
occurs verbatim in the instrument's bytes" fails **8 of 82** production rows
(`tools/mado-keysym.py`, `quality/check-axis-scores.py`, `check-counter-discrimination.py`,
`check-evidence-pointers.py`, `check-index-rows.py`, `check-locators.py`, `counter-selftest.py`,
`check-tool-ledger.py`); "≥3 distinct content tokens from the instrument's bytes" fails **1 of 82**
(`quality/counters/c1-r48-terminal-cache.py`, score 2) and *still* leaves 10 of 82 F3 rows green. The clause family is
non-monotone: raising it to reject F3 breaks production, lowering it to keep production keeps F3. The unforgeable
alternative — "description must be a verbatim normalized substring of the instrument's own bytes" — measures
**0 of 82** on the current ledger, so it requires rewriting all 82 descriptions, which is a write outside a source-only
round. That is the honest cost statement L1 needs.

**Recommended claim wording (C1), minimal edit:** replace *"and instrument-specific functional context"* with
*"and a structural description-shape clause (≥8 words, pairwise distinct, no 3-word prefix shared by more than four
rows), with the residual — a varied-prefix filler description and a registry/cycle of documents both pass — named in
the receipt"*, and add *"the demonstrated counter's sha256 equals the committed file's sha256 at the scored rev"*.

---

## 4. C2 — corrected contract and the minimal repair

### 4.1 What is decidable against the pinned bytes (all measured above)

| defect | decidable test | production-irrelevant, entry-relevant result |
|---|---|---|
| P16 splice | whitespace-normalized quote must be contiguous **inside exactly one cited range** | `contiguous=False`; the 16-word contiguous alternative forces a scoped proposition |
| P17 wrong subject | compute the function span containing the quoted line (signature + brace match); proposition's backticked subject must own it | quoted line 621 ∈ `sendkeystate 591-627`, subject says `sendshortcut 531-589` |
| P18 wrong locale | "inside the scan/loop" must be true of a computed `for` span | `for` span 565-571; quoted line 574 |
| fabricated quotes | quote must be found in the pinned bytes at the span | attack A of r52 showed the landed counter never opens source bytes (`T4`/`T6`: invented quotes at real pins → `TARGET_MET`) |
| wrong table shape | columns derived from the header row, never positional | landed counter expected `\| P## \| S### \| …`; entry is `\| P## \| Proposition \| S### \| …` → `props=0` |

### 4.2 Minimal repair of the three propositions (append-only, no new ground)

The entry's quote cap is 25 words, which is what forced the P16 splice. Minimal repair is therefore **one retirement,
one re-localization, one split** — measured word counts in §2.3:

| old | minimal corrected form | pin | quote (words) |
|---|---|---|---|
| P16 | **P16a** — "`Actions::pass` sets the keyboard modifier mask before any key event." | `ConfigActions.cpp:1554` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` (4) |
| P16 | **P16b** — "and clears it after the key/pointer branch." | `ConfigActions.cpp:1576` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (4) |
| P16 | ordering claim, restated as line order across rows (mechanically checkable): `1554 < 1558 (P13) < 1576` | — | — |
| P17 | **retract**, `superseded-by P04`; P04 already states the guarded second call with the correct pin and no false subject | `DispatcherTranslator.cpp:619-622` | (P04 unchanged) |
| P18 | **re-localize** — "A keysym the scan did not find (keycode still 0) returns `key not found` from the cache-miss branch **after** the loop closes at :571, **before** the generic `invalid key` guard at :579-580." | `:573-574` | `return {.success = false, .error = "sendshortcut: key not found"};` (10) |

Notes that make this "minimal" and not a rewrite: P17 adds no new proposition (P04 covers it — retiring it *reduces*
the entry), P18 changes the locale claim only (same quote line, wider span), P16 is the only row that must split, and
the line-order claim P16a→P13→P16b is expressible with the rows that already exist. The IDs must not collide with the
draft map's P16/P17/P18 (`w1/C2EntryDraft/proposition-map.tsv`, different propositions) — use `P16a/P16b`, `P17r`,
`P18r` and bind by `(id, pin, quote)`, never by ordinal.

### 4.3 Corrected C2 counter contract (clauses)

- **C2-A** Header-derived table binding (`ID|Proposition|Source row|Pin:anchor|Quote|Support class|Why it supports`);
  unknown header → SETUP; positional regexes are forbidden (this alone kills the r52 `props=0` failure).
- **C2-B** Quote: ≤25 whitespace words; contiguous inside exactly one cited range; ranges comma-separated `N`/`N-M`.
- **C2-C** Digest binding: pin file's sha256 equals the round's `fetch/SHA256SUMS` entry (today: all five `OK`).
- **C2-D** Subject binding by computed span; unevaluable subject → SETUP.
- **C2-E** Locale/ordering binding: `inside <block>` ⟺ quoted line within the computed block span; `before/after X` ⟺
  line comparison against X's computed edge.
- **C2-F** Append-only: pre-correction lines byte-identical to the r52 revision; corrections in a new section;
  superseded ids carry `superseded-by`.
- **C2-G** Frozen deny-set: the three defective `(id, proposition, quote, locator)` triples must be absent.
- **C2-H** Index: exactly one `corpus/README.md` row for the slug; every cited S-row `mined` with the entry path.
- **C2-I** Expansion credit is a *separate* clause: repairing S370–S373 (opened `2026-10-27`, r52) earns **no coverage
  credit**. Expansion needs a source row opened in the scoring round on ground the coverage map does not already hold.

Residual for C2, stated plainly: C2-A..H prove the quote/pin/proposition *bindings*; they do not prove that the
proposition says everything the quote shows or nothing more. Attack A's per-proposition table already lists the
"quote-only" gaps (P07 plural, P09 scoping, P10 scoping, P12 second clause, P15 "before changing it"). Those remain
non-author review work, not counter work.

---

## 5. Axis accounting

| axis | move available this round | evidence | harm |
|---|---|---|---|
| **operability (C1)** | real and bounded **if** C1-5 is restated as shape/repetition and C1-9 (reviewed = landed) is added: the prototype returns MET on production and MISSED on all 13 frozen fixtures + 8 spellings, with margins (floor 8 vs min 9; prefix cap 4 vs max 3) measured rather than guessed | §3 matrix, §3.1 | none: no production row is touched; green control stays green |
| **coverage (C2)** | **not available from a repair.** S370–S373 were opened 2026-10-27 in r52; the repair adds no new source and no new ground. C2 can move *quality/admission* (the entry becomes citable once C2-A..H pass) but the coverage axis needs a new entry on ground opened this round, which does not exist yet (`.ufo/waves/round-53/` has no `fetch/`, no `source-rows.txt`) | §2.3, §4.2; `git ls-tree … HEAD \| grep -c round-53` → 0 | none, provided the report does **not** book expansion credit — booking it would be a false claim on the coverage axis |
| quality | improved by the repair, but only after P16/P17/P18 are actually marked; unmarked, the indexed entry keeps misleading readers (`corpus/README.md:80`) | §2.3 | — |

If L1 must move coverage this round, the only honest route is a fresh entry on a source opened this round; the C2
repair is a prerequisite, not a substitute.

---

## 6. Confidence and limits

- **High** (deterministic on committed bytes): every C1 clause measurement (§3 table, word/prefix/self/pointer counts),
  every C2 span computation (§2.3), the r51 before-state run, the pin digests, the absence of any committed r52 counter.
- **Medium**: the claim that "no lexical clause separates production from F3" — I measured two candidate families
  (code-token presence: 8/82 production failures; content-token count: 1/82 production failures and 10/82 F3 survivors)
  and the verbatim-provenance option (0/82). Other families exist; the *shape* of the failure (non-monotone margins)
  is measured, the universality is inference.
- **Not claimed**: that the corrected contract is unforgeable (it is not, §3.2); that C1 or C2 can be admitted this round
  (nothing is committed); that any seat is a non-author reviewer; that the r52 four-cell control isolates defect classes
  (it does not — with the row grammar it fails on coverage; the wide self-scan is what lets it report `self_pointer=1`).
- **Not done**: no counter written or committed, no lane/fleet/sibling file touched, no git/jj mutation, no live read,
  no package query, no producer execution, no install.

## Hygiene

Scratch `/fast/scratch/hyaku/mado-r53/R53One8` removed before yield (prototype scripts, extracted ledger/tree, matrix
receipt, r51 work dir). `/tmp` unused. Only file written in the lane: this report.

Report: `.ufo/waves/round-53/w1/R53One8.md`

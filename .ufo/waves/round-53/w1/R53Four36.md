# R53Four36 — smallest maintainable C1 and C2 (simplifier, round 53)

Axes named: **operability** (C1 instrument-ledger counter) and **coverage** (C2
proposition-bound dispatcher entry). This seat deletes weight from the r52 candidate
implementations, measures what survives, and proposes the test set a frozen counter must
carry. It adds no claim, takes no admission vote, and writes no tracked file.

**Attacked predicate.** C1 — `.ufo/waves/round-53/claims-frozen.md:7`: a newly committed,
scratch-aware counter with an explicit selftest returns `TARGET_MET` on the production
ledger, `TARGET_MISSED` on a no-work control **and each frozen forgery fixture**, with
exact population coverage and non-self pointers. C2 — `:9-13`: an append-only correction
clearly repairs P16–P18 against opened pinned source bytes, a frozen counter rejects the
old bytes and accepts the corrected entry with quote/pin/proposition bindings, an
independent reviewer checks source truth, and no expansion credit exists without a source
row opened this round plus uncovered ground.

Scope: lane read-only — `git status --porcelain` at this seat's start showed only
`?? .ufo/waves/round-53/`; at yield sibling seats had also added `M corpus/SOURCES.md`
(S374) and `?? corpus/lessons/round-53.md`, neither written by this seat. No live reads,
no package queries, no installs, no
git/jj mutation in the lane. Scratch path `/fast/scratch/hyaku/mado-r53/R53Four36` (the seat path),
removed before yield; disk guard `df -h /fast` → 594 G available, 27 % used.
The only git mutation was inside an isolated `--shared` clone at
`/fast/scratch/hyaku/mado-r53/R53Four36/fixture`, whose `git rev-parse --show-toplevel`
was asserted to print that directory before every `read-tree`/`update-index`/`commit-tree`.

**Caller-evidence limitation (recorded, not hidden).** No language server is mounted:
`read xd://lsp` → `No such tool: xd://lsp` (the device list carries `ast_edit`, `debug`, and
the MCP tools only). Caller claims below are therefore **literal**: Python AST load-counts
and call-site line numbers inside each file, plus lane-wide `grep` for imports and
invocations. They are not semantic reference proofs and are labelled `[OBS-AST]` /
`[OBS-grep]` wherever used.

---

## 1. Measured before-state at the frozen base `ad4bf205`

| object | bytes | lines | measured |
|---|---|---|---|
| `quality/counters/c1-r51-ledger.py` (committed) | 19,094 | 445 | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET`, exit 0, **2.391 s** |
| `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` (draft, sha256 `0fe862f116a7…`) | — | 847 | production `TARGET_MET`, exit 0, 327 ms; `--selftest` → `C1_R52_SELFTEST: 53/53 passed`, 68 ms |
| `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` (draft) | — | 965 | default run → `entry=absent` (wrong slug); with `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → `clauses_met=2 admitted=0/1`, 80 ms, and it **writes** `<work>/c2-r52-probe.json` |
| `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (committed entry) | — | 32 | index row `corpus/README.md:80`; rows `corpus/SOURCES.md:320-323`; P16–P18 defects present |
| population at `ad4bf205` | — | — | 82 files (`tools/*` any extension + `quality/*.py` + `quality/counters/*.py`), independently counted `git ls-tree` |

Command (r51 counter, the before-state the claim names):

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
    --work /fast/scratch/hyaku/mado-r53/R53Four36/w51
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf205…)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
rc=0
```

Reproduced r52 laundering on the draft (the defect C1 exists to close), on production rows
(`variants/P04-own-basename.md`, `P19-double-slash.md`, `P21-case.md`, `P03-bare-ledger.md`
each change `tools/mado-anims.py`'s pointer cell only):

```
C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET   ← P04, P19, P21, P03
```

---

## 2. C1 — deletions, the smallest counter that satisfies the frozen arms, and the fixture set

### 2.1 Deletion candidates in the r52 draft, with caller proof

| # | candidate | lines | why it can go | evidence |
|---|---|---|---|---|
| C1-D1 | `Suite` (468-491), `fixture_repo` (603-640), `resolve_work` (768-787), and the 53-arm `selftest` body (643-765) | **205** | `measure(reader, ledger_text)` is the whole scored path and takes a reader double. The fixture machinery is reachable only from `main → selftest`, and it creates, configures and **commits** a throwaway git repository. | `[OBS-AST]` call sites: `Suite` 644, `fixture_repo` 647 (both inside `selftest`), `selftest` 808, `resolve_work` 807/815 (both in `main`); `measure` 651 (selftest) and 832 (main). Nothing in `measure` (303-447) names them. |
| C1-D2 | `POINTER_TOKEN` (83) | 1 | Declared and never loaded. | `[OBS-AST]` zero `Load` nodes for the name. |
| C1-D3 | `MIN_DESC_WORDS` (88) and the `too-short` branch | 2 | Production's shortest description is **13** words (fence-aware parse of the ledger at `ad4bf205`), and low-effort filler is already caught by "no phrase from the instrument's bytes" (measured: `filler-desc` case red without the floor). | `[OBS]` word-count distribution over the 82 data rows: min 13; `filler-desc` case passes at 19/19 below. |
| C1-D4 | `--work` as a required, created, validated directory (`resolve_work`, `REFUSED_WORK_PREFIXES`) | ≈ 30 | The scored path writes nothing. Keeping the flag as *accepted and ignored* preserves the harness interface without a lifecycle. | Same call-site proof as C1-D1; no `open(..., "w")` on the scored path. |
| C1-D5 | the checker leg (absent from this draft, present in r51 as `checker_selftest`/`checker_ledger`) | — | Do **not** reintroduce it: a second parser for one grammar gave `dangling` two meanings in r51 and made the verdict hostage to a sibling file (r52 `w1/C1Simplify.md` §3, §1; §9). One authority: the counter. |

Net: the draft's accounting core is 145 lines (`measure`) plus ~160 lines of measured
helpers; the 205-line selftest block is the removable weight.

### 2.2 The smallest counter I could make pass the frozen arms — measured reference

Built at `--scratch/c1-r53-ref.py`, **477 lines including docstring and the in-memory
selftest fixtures** (core `measure` = 103 lines, selftest = 56 + 4). It starts no child
process except read-only `git ls-tree`/`git show`, writes nothing, and accepts `--work`
without using it. Rules that survived measurement:

1. **population** — one `git ls-tree -r` call gives `{path: mode}`; population = `tools/*`
   (any extension) + `quality/*.py` + `quality/counters/*.py`.
2. **rows** — pipe rows outside fences whose first cell is a repo path. **Wider-than-three
   cell rows are scored, not discarded** (the frozen control is a four-cell table); the
   pointer region is cells 3.., and a row that names no accountable target is additionally
   scanned in cells 1.. for a self mention.
3. **pointer identity** — tokens are backticked spans, else whitespace/comma-split words;
   each is normalised by dropping `#frag`, a numeric `:N` suffix, trailing `).,;:'"`,
   `\`→`/`, repeated `//`, leading `./` or `/`; comparison *also* folds case, cuts any
   `:suffix`, and compares **basenames**. A pointer-region token that equals the ledger
   path/basename or the row's own path/basename is `self_pointer` — this is the clause that
   closes the nine r52 laundering spellings.
4. **accountable target** — resolves at `<rev>`, mode is `100644`/`100755` (a `120000`
   symlink blob is not evidence), is not a population peer, and its bytes name the row's
   basename.
5. **description** — non-empty/non-placeholder, not repeated verbatim, and it must share a
   two-word phrase with the instrument's own **evidence bytes**, where evidence excludes
   every `#!` line (the shebang-lift rule; §2.4) and the phrase may not consist only of the
   instrument's path words, the population's path words, function words, or path fragments.
6. **selftest** — the same `measure()` over literal ledger texts and a dict-backed `Reader`
   (7 files: three instruments, three documents, one symlink alias, plus a fourth
   instrument); **19 cases**, one per defect class, explicit per-case red/green lines and a
   `C1_R53_SELFTEST: 19/19 passed` line. No git, no scratch, no commits.

Measured output on the frozen arms (`--repo <lane> --rev ad4bf205…`, `rev=` elided):

| arm | reference | r52 draft | note |
|---|---|---|---|
| production ledger | `TARGET_MET`, all zero, 313 ms | `TARGET_MET` | green arm holds |
| `.ufo/waves/round-52/controls/c1-do-nothing.md` | `uncovered=81 dup=1 self_pointer=1 generic_desc=1` **MISSED** | `uncovered=81 dup=1 self_pointer=1 generic_desc=1` **MISSED** | both defect signals named |
| `w2/Attack01/controls/F-all-forged.md` (82/82 forged descriptions) | `generic_desc=81` **MISSED** | `TARGET_MET` | 81 of 82 rows; one survivor (§2.4) |
| `H2n-verify.sh-forged.md` (`env bash and nothing else here okay.`) | `generic_desc=1` **MISSED** | `TARGET_MET` | shebang lift |
| `H3n-c2r51-forged.md` (`PRED-C2-r51 does things.`) | `TARGET_MET` | `TARGET_MET` | **ceiling**, see §2.4 |
| `H4n-nameonly-forged.md` (`mado anims py does things here.`) | `generic_desc=1` **MISSED** | `generic_desc=1` **MISSED** | |
| nine laundering spellings P03–P09/P19–P21 on a production row | `self_pointer=1` **MISSED**, 9/9 | `TARGET_MET`, 9/9 | the operability hole |
| duplicate row / dropped row / bad pointer / empty description | `dup=1` / `uncovered=1` / `bad_pointer=1` / `generic_desc=1`, each **MISSED** alone | — | one-field isolation |

Selftest: `C1_R53_SELFTEST: 19/19 passed`, exit 0. Case names: `green`, `green-line-suffix`,
`self-full`, `self-bare`, `self-dot`, `self-own-basename`, `self-trailing-paren`,
`self-colon-suffix`, `self-double-slash`, `self-leading-slash`, `self-case`,
`symlink-alias`, `frozen-control-shape`, `duplicate`, `dangling`, `empty-desc`,
`repeated-desc`, `filler-desc`, `peer-pointer`.

### 2.3 The population trap the integrator must land in one commit — measured

Landing the counter alone changes the population it measures. Fixture commit
`1087094f` = `ad4bf205` + an empty `quality/counters/c1-r53-ledger.py`:

```
detail: uncovered path=quality/counters/c1-r53-ledger.py
C1_R53: population=83 ledger_rows=82 uncovered=1 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED
```

So the counter file, its `quality/tool-ledger.md` row, and the row's pointer must land
together, and the row's pointer must name a document that mentions the counter's basename
(a wave document that is committed before the demonstration, not the ledger and not the
counter's own bytes).

### 2.4 The fixture set is not frozen anywhere in round 53 — and three r52 forgeries are not
structurally separable

`.ufo/waves/round-53/` contains `claims-frozen.md`, `w1-spec.json`, `w1-dispatch.json` and
`w1/` only — **no `controls/` directory and no fixture list**. "Each frozen forgery
fixture" therefore names nothing at the base that a scorer can check; the only committed
forgeries are r52's. Measured discrimination on every one of them (table above) gives the
freeze decision:

- **Freeze these** (at least the reference discriminates; the r52 draft does not, for
  F-all and H2n): the no-work control; the nine pointer spellings; `H4n`; `H2n`; and F-all
  **as a bounded fixture** (`generic_desc=81`, not `82`).
- **Do not freeze H3n** with a structural counter: its description `PRED-C2-r51 does
  things.` binds `pred c2` from the instrument's own docstring, and the only rule I found
  that rejects it — treating the instrument's `PRED-…` token as a name rather than
  evidence — turned **two production rows red** (`quality/counters/c1-r47-terminal.py`,
  `quality/counters/c2-r51-dispatch-entry.py`, `generic_desc=2`, `TARGET_MET` →
  `TARGET_MISSED`). If H3n must be scored, the production ledger's two descriptions have to
  be rewritten first; that is an editorial change this seat cannot make.
- **F-all's survivor** under the reference is `quality/counter-selftest.py`:
  `Generic accountability note 32 env python3.` binds `env python3` from an embedded
  shebang string at `quality/counter-selftest.py:254`, a line that opens with
  `TOOL_SRC = '''` rather than `#!`. Excluding every `#!`-initial line, not only line 1,
  is what takes F-all from 0/82 to 81/82; line-1-only exclusion leaves it at
  `generic_desc=0`.

The honest bound stays: a description that lifts a real two-word phrase out of the
instrument's bytes and wraps it in boilerplate can pass a lexical rule (r52 `C1Simplify.md`
§6; `w2/Attack01.md` T2). C1's own text limits the claim to bounded structural
accountability; the receipt must say so in those words.

---

## 3. C2 — deletions in the r52 counter, the smallest counter, and the correction text

### 3.1 Measured defects in the r52 C2 draft (each is also a deletion candidate)

| # | defect | evidence | deletion |
|---|---|---|---|
| C2-D1 | **Default entry slug is not the committed entry**: `ENTRY_DEFAULT = "corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md"` (line 102) vs committed `hyprland-synthetic-dispatch-r52.md` | default run at base: `a ok=0 entry=absent`; with `--entry` the same rev parses 18 propositions | one constant — wrong name, not a knob |
| C2-D2 | **Pin resolution is poisoned by sibling copies**: `pin_index` drops every basename that occurs twice under `--fetch-root` (default `.ufo/waves/round-52`, a *prefix*), and the r52 entry draft staged a second `fetch/` copy | `git ls-tree -r ad4bf205 .ufo/waves/round-52 \| grep Hyprland-legacy-DispatcherTranslator.cpp` → 2 paths (`fetch/` and `w1/C2EntryDraft/fetch/`); run → `d.pin_file_absent` ×18; `resolve_pin_file` returns `None` | delete `pin_index` (15) + `resolve_pin_file` (12) + `prior_equal_pins` (34) and bind `pin` as **`<fetch-root>/<pin>`** — the entry's own sentence says "All pins are under `.ufo/waves/round-52/fetch/`". One authority for the pin root, no ambiguity rule, no suffix tiers |
| C2-D3 | **Row binding demands a prose cell carry a fetch path**: `if fetch_root not in anchor` (line 568) | run → `c.anchor_no_fetch_root` ×18; `S370`'s anchor cell is `DispatcherTranslator.cpp:531-627 @ efb5099…`, which never names `.ufo/waves/round-52` | replace with URL↔pin basename agreement (`ConfigActions.cpp` ⊂ `Hyprland-ConfigActions.cpp`); drops the `anchor`/`_line` fallback and the 40-hex re-check inside a prose cell |
| C2-D4 | **Every proposition id must be re-drawn in prose** (`referenced_ids`, 742-757; `id_not_referenced`, 831) | run → `e.miss=P01:id_not_referenced,…` ×18 on a committed entry the lane considers structurally complete | not in the frozen predicate ("every material factual proposition is mapped" is the inverse direction); delete `referenced_ids` + the rule (16 + 4 lines). The reversal already covers `row_unmapped` |
| C2-D5 | **Writes a probe JSON** (`scratch_dir`, 841-857; write at 916-920) | run with `--work` → `<work>/c2-r52-probe.json` exists; every invocation creates a directory | delete; `--work` accepted and ignored (same rule as C1-D4) |
| C2-D6 | **Block-form grammar** (`BLOCK_ID_RE` 135, `BLOCK_KEY_RE` 136, branch 388-411) | no committed entry uses it; the table form is the entry's own grammar | delete; 24 lines + 2 constants. Narrowing is a documented contract, not a behaviour change |
| C2-D7 | dead `prose_text` (730-739) | `[OBS-AST]` zero call sites | delete (10 lines) |
| C2-D8 | `git_rc` (151-153) — one `cat-file -e` caller | `[OBS-AST]` | fold into `git()` |

Net: 965 → **365** lines in the reference (core clauses a–e = 107 lines together).

### 3.2 Reference counter — measured on old and corrected bytes

Rules: parse the map by **header roles** (any column order; a rationale column outranks a
`support class` column), **last row per id wins** (this is how an append-only correction
supersedes without editing), then:

- (a) entry at `<rev>` + unfenced `corpus/README.md` row whose first cell names
  `knowledge/<basename>`;
- (b) ≥4 effective propositions, each with claim/row/pin/quote/support, ids/claims/quotes
  distinct, support ≥4 tokens;
- (c) row exists, is `mined`, `used-by` names the entry, URL basename agrees with the pin
  basename;
- (d) `<fetch-root>/<pin>` exists, quote 3–25 words, whitespace-collapsed quote is a
  **contiguous substring of the cited line span**;
- (e) ≥2 distinct rows and every row whose `used-by` names the entry is mapped.

| input | measured |
|---|---|
| committed entry at `ad4bf205` (old bytes) | `b ok=1 propositions=18`; `c ok=0 … P16:url-or-pin`; `d ok=0 quotes_bound=17/18 miss=P16:pin-malformed`; `e ok=1` → **`clauses_met=3 admitted=0/1 TARGET_MISSED`**, exit 1 |
| same entry, pin grammar alone repaired (`:1554-1576`), quote left spliced | `d ok=0 quotes_bound=17/18 miss=P16:quote-not-at-pin(Hyprland-ConfigActions.cpp:1554)` → **MISSED** — the splice is rejected by span binding, not by a grammar nit |
| corrected entry (fixture commit `72b4f04d`) | `a..e ok=1`, `quotes_bound=19/19`, **`clauses_met=5 admitted=1/1 TARGET_MET`**, exit 0, 55 ms |
| fabricated quote at a real pin | `d ok=0 P19:quote-not-at-pin` → MISSED |
| quote that exists elsewhere in the pin but outside the span | `d ok=0 P17:quote-not-at-pin` → MISSED |
| 26-word quote | `d ok=0 quote-too-long(26)` → MISSED |
| duplicate claim | `b ok=0 duplicate-claim:1` → MISSED |
| index row removed | `a ok=0 index_row=absent` → MISSED |
| 3 propositions | `b ok=0 propositions=3<4`, `e ok=0 row-unmapped:S371,S372,S373` → MISSED |
| base `85d57a8` (entry absent) | `a ok=0 entry=absent`, all clauses skipped → `clauses_met=0 admitted=0/1 TARGET_MISSED`, exit 1 |

### 3.3 The append-only correction this seat measured green (32 → 45 lines, prefix byte-identical)

Prefix check: `head -c 6535 entry-corrected | sha256sum` = `sha256sum entry-orig` =
`bee0d14379eb…`, and `diff` of the original line count is empty → **append-only**.

Text to append after the entry's closing paragraph:

```markdown
## Correction (round 53, append-only)

The four rows below revise P16-P18 and add the clear call that P16's claim carried. No row,
pin or quote above is edited: the last row for an id is the effective proposition, so this
block is read as the current text for P16-P18 and the rows above stay as provenance.

| ID | Proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports |
|---|---|---|---|---|---|---|
| P16 | `Actions::pass` sends the modifier state before the key event. | S371 | Hyprland-ConfigActions.cpp:1554-1558 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | One contiguous excerpt :1554-:1558 shows the modifier call then the key call; the row above spliced :1554 and :1558 and added a disjoint :1576. |
| P17 | `sendkeystate` restores the previous `m_passPressed` value after its delegate calls. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:624 | `Config::Actions::state()->m_passPressed = oldPassPressed;` | direct | The restore at :624 follows both `sendshortcut` calls. The row above named `sendshortcut` as the subject and restated P04's repeat rule; P04 stands as that rule, so the effective P17 states a distinct step. |
| P18 | An unresolved keysym returns the `key not found` error after the scan loop, in the cache-miss branch. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:571-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct | The guard follows the loop that closes at :571, so it is outside the scan body; the row above localized it inside the scan. |
| P19 | `Actions::pass` clears the modifier state after the key event. | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct | This is the clear call that P16's claim named; it is a separate contiguous excerpt and cannot share P16's quote. |
```

Locally opened pinned bytes that this text rests on (checksums `sha256sum -c SHA256SUMS`
→ all `OK`, 2026-10-27):

| claim | located quote | source |
|---|---|---|
| modifier call before key call | `1554: g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` … `1556: if (S.m_passPressed == 1) {` `1557: if (!isMouse)` `1558: g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` |
| modifier clear after | `1576: g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | same |
| repeat calls live in `sendkeystate` | `531: static SDispatchResult sendshortcut(…)` … `589` close; `591: static SDispatchResult sendkeystate(…)`; `619: auto result = sendshortcut(modifiedArgs);` `621-622` guarded repeat | `.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp` |
| `:574` is outside the scan | `565: for (xkb_keycode_t kc = keycode_min; …` … `571: }` `573: if (!keycode)` `574: return {.success = false, .error = "sendshortcut: key not found"};` | same |

**Why P17 must not restate the repeat rule.** The committed entry already carries P04 =
"`repeat` calls its delegate again only after a successful first call" with the *same* quote
the old P17 used. A correction that merely re-attributes that quote produces
`duplicate-quote:1` and the counter stays red (`clauses_met=4` in the first draft of my
correction, measured). P17 therefore states the distinct restore step at :624; that also
exposes a second, previously unflagged defect in the committed entry: **P04 and P17 are the
same fact twice**.

**Expansion credit.** The reference prints `fresh_rows=<n> expansion_credit=<yes|no>` as a
diagnostic, not a gate (rows absent at `--base`). At `ad4bf205` with S370–S373 it prints
`fresh_rows=0 expansion_credit=no` — repairing P16–P18 earns **no** expansion credit under
the frozen claim. A sibling seat has since opened `S374` (round-52 verifier lesson,
`used-by: corpus/lessons/round-53.md`); mapping it from the entry would raise `fresh_rows`,
but the correction measured here maps S370–S373 only and claims no credit.

---

## 4. Preserved contract — what the deletions must not break (all measured)

| check | command shape | result |
|---|---|---|
| C1 production green | `python3 -I c1-r53-ref.py --repo <lane> --rev ad4bf205…` | `TARGET_MET`, 82/82, 313 ms |
| C1 control red, both defect signals | `--ledger .ufo/waves/round-52/controls/c1-do-nothing.md` | `self_pointer=1 generic_desc=1` MISSED, exit 1 |
| C1 laundering closed | nine production-row variants | 9/9 `self_pointer=1` MISSED |
| C1 selftest | `--selftest` | `19/19 passed`, exit 0, no git, no writes |
| C2 old bytes rejected | `--rev ad4bf205…` | `clauses_met=3` MISSED, exit 1 |
| C2 corrected entry accepted | fixture commit `72b4f04d` | `clauses_met=5 admitted=1/1` MET, exit 0 |
| C2 base absent | `--rev 85d57a8…` | `clauses_met=0 admitted=0/1` MISSED, exit 1 |
| C2 no writes | `find <work> -type f` after a run | empty |
| lane untouched by this seat | `git status --porcelain` | at start `?? .ufo/waves/round-53/` only; sibling edits (`M corpus/SOURCES.md`, `?? corpus/lessons/round-53.md`) appeared later and are not this seat's |

---

## 5. Tradeoffs and dissent

1. **The reference is not the scored artifact.** It is a lower bound with the frozen arms
   measured (19 selftest cases plus every external arm in §2.2). Its 477 lines include ~90 lines of
   in-memory fixture constants that a production counter would keep anyway as the selftest
   corpus; the accounting core is 103 lines.
2. **The `#!`-evidence rule narrows the context clause.** It costs a description that
   genuinely paraphrases a shebang, and it buys 81/82 of F-all plus H2n. It does not touch
   production (measured green). H3n still passes; the rule that would catch it costs two
   production rows, so it must not ship as code without a ledger-description edit.
3. **C2's last-row-wins supersession is a grammar addition.** It is the smallest
   append-only mechanism that lets a counter reject the old bytes while the old row stays
   in place; the alternative (a new file plus an index rewrite) edits the index instead.
4. **Dropping C2's block form and role aliases narrows what the counter accepts.** The
   frozen predicate does not require two grammars; a future entry must use the table. State
   that in the counter's docstring, not in a second parser.
5. **Against building a C++ enclosing-function parser for P17.** Attribution truth is
   assigned to the outside reviewer by the frozen claim; a brace/string-aware lexer in the
   counter would add the exact failure mode the claim avoids (a false assertion of
   entailment). The counter checks binding, the correction text fixes attribution, the
   reviewer judges truth.
6. **No position on admission.** C1/C2 remain unproven until a committed counter and its
   fixtures exist at a data commit; this seat's numbers are a design bound, not a pass.

## 6. Reproduction and hygiene

- Reference counter files were scratch-only and are **removed**: `c1-r53-ref.py`
  (477 lines), `c2-r53-ref.py` (365 lines), `entry-corrected.md`, mutation ledgers,
  `variants/`, and the `fixture` clone were all under
  `/fast/scratch/hyaku/mado-r53/R53Four36` and deleted before yield. The rules above are
  the reproduction contract; the fixture commits named (`72b4f04d`, `1087094f`, `7cd8cc0a`,
  `085ab6c9`, `f4e55905`, `f7693903`, `081ef198`, `978ee36a`, `056b5cf3`) are run-local and
  disappear with the clone.
- No tool was installed or updated; no package transaction ran.
- No live read, process probe, screenshot, input capture, or compositor/service/host
  mutation occurred.
- Newly opened sources: only the committed r52 fetch bytes above (no network fetch); their
  `SHA256SUMS` verify locally. No URL/access date applies beyond the pinned revision
  `efb50993780079460b0cbed1363e2166a2de1d9f` already recorded at `corpus/SOURCES.md:320-323`.
- This seat wrote exactly one path, this report. Concurrent sibling edits
  (`M corpus/SOURCES.md` with row S374, `?? corpus/lessons/round-53.md`) appeared during the
  seat and were not made by it; no tracked lane file was modified here.

Report: `.ufo/waves/round-53/w1/R53Four36.md`

# R53Four32 — C1/C2 independent evidence and draft lesson prose (scribe, leaf)

Seat: `R53Four32`, registered `scribe` (`.ufo/waves/round-53/w1/swarm-registry.json`), round 53 wave 1,
independent bounded work item 32. This report is **not** a claim verdict and **not** a non-author
review: a seat is a leaf and never counts as the independent reviewer the frozen claims require.

Axes under test: **operability** (C1) and **coverage** (C2). Frozen base tip
`ad4bf2059bcfafe63671d262222908ee1fe8001c`. Claims: `.ufo/waves/round-53/claims-frozen.md:1-13`.

## 0. Boundary actually held

- Source-only, read-only: no live read, package query, input capture, screenshot, producer run,
  host/config/service/compositor mutation, no source fetch. No lane counter was executed.
- Git use limited to `log`, `status`, `show`, `ls-tree`, `diff --name-only`, `grep` (read-only).
  No clone, no worktree, no `jj`, no commit/push, no `task`, no background job.
- Every measurement below reads **committed** bytes at `ad4bf205` (git objects) or committed
  working-tree files named in the table. No tracked file was written; this report is my only write.
- Scratch: `/fast/scratch/hyaku/mado-r53/R53Four32` (five throwaway scripts named in §3/§4),
  removed before yield. Nothing written to `/tmp`.
- No tool install or update; `/home/vgpnk/.omp/agent/RULES.md` therefore not exercised. Pacman
  untouched.
- Disk: `df -h /fast /tmp .` → `/fast` 595G avail (26% used), `/tmp` 124G avail (4%), `/home` 589G
  avail. No ENOSPC. No `disk-guard` executable exists in the lane — `grep -rln 'disk-guard'`
  matches only wave prose (`.ufo/waves/round-43/w1/ScrConsiderthese/*`, `round-47/w2/ScoutMisroot.md`,
  `round-51/make-w1-spec.py`); capacity was measured directly instead.

    $ git -C mado-shokunin log --oneline -1
    ad4bf205 round-52 verifier spot-check (integrator, hyaku): non-author admit/reject
    $ git -C mado-shokunin status --porcelain
    ?? .ufo/waves/round-53/

## 1. Attacked predicates (verbatim, frozen)

> **C1 — operability: instrument-ledger accountability counter.** … Target: a newly committed,
> scratch-aware counter with explicit selftest returns TARGET_MET on the production ledger,
> TARGET_MISSED on a no-work control and each frozen forgery fixture, with exact population
> coverage and non-self pointers. This is a bounded structural accountability check, not semantic
> proof. No capability admitted unless the final committed demonstration and controls pass.

> **C2 — coverage: repair proposition-grounding defects in the indexed r52 dispatcher entry.** …
> Target: append-only correction clearly repairs those three propositions against opened pinned
> source bytes; a frozen counter rejects the old bytes and accepts corrected entry with
> quote/pin/proposition bindings; independent reviewer checks source truth. No claim of expansion
> credit unless an admitted entry rests on a source row opened this round and uncovered ground per
> coverage map.

Source: `.ufo/waves/round-53/claims-frozen.md:5-13`.

## 2. Frozen state at tip — measured, not assumed

| Fact | Command | Output |
|---|---|---|
| No C1/C2 r52-or-r53 counter is committed in the accountable location | `git ls-tree -r --name-only ad4bf205 -- quality/counters \| grep -i 'r5[23]'` | no output, `rc=1` |
| No instrument population changed since the r52 base | `git diff --name-only 85d57a818c3707397e21c840b6498b105ba798aa ad4bf205 -- quality tools scripts` | empty |
| Defective entry is committed byte-for-byte | `git show ad4bf205:corpus/knowledge/hyprland-synthetic-dispatch-r52.md \| sha256sum` | `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078` |
| Same bytes in the worktree | `sha256sum corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | `bee0d143…ecb078` (identical) |
| r52 lesson bytes | `git show ad4bf205:corpus/lessons/round-52.md \| sha256sum` | `4a81e9348e5bf7cdfa7391dfdab1fc24b42cdb721b9322f29c103e61a2a757c6` |
| Entry is indexed (coverage map row) | `corpus/README.md:80` | `knowledge/hyprland-synthetic-dispatch-r52.md` row present |
| Rows S370–S373 registered | `corpus/SOURCES.md:320-323` | four tier-A `mined` rows, sat `2026-10-27` |
| Round-53 registration artifact | `ls .ufo/waves/round-53/` | `claims-frozen.md`, `w1*`, `w1/` — **no `registration.md`** |
| Round-53 controls / fetched source | `git ls-tree -r --name-only ad4bf205 -- .ufo/waves/round-53`; listing | empty; no `fetch/`, no `controls/` |
| r52 controls + receipts committed | `.ufo/waves/round-52/{controls,receipts}/` | `c1-do-nothing.md`, `c1-row-context-control.md`, `c2-do-nothing.md`, `c1-base.txt`, `c2-base.txt` |

**Freeze-integrity observation (verbatim conflict).** The assignment says "Claims freeze and
registration govern all work"; the tree at the frozen tip has no round-53 registration file, so no
round-53 predicate (exact command, exit codes, control identities, fixture byte set) is frozen the
way `.ufo/waves/round-52/registration.md:6-15` froze r52's. The claims file itself is present and
frozen. Peer `R53Two13.md` reports the same absent path independently. Consequence: a C1/C2 counter
cannot be validated "before data" against a registered command string; only the prose target exists.

## 3. C1 — operability evidence

### 3.1 What the committed r51 counter actually measures (source-truth read, not executed)

`quality/counters/c1-r51-ledger.py` (445 L, committed): population = every `tools/**` file plus
`quality/*.py` plus `quality/counters/*.py` (`:16-46`); ledger = `quality/tool-ledger.md` pipe rows
whose first cell is a population path, fenced blocks excluded; fields `uncovered`, `dangling`,
`bad_pointer`, `empty_desc`, plus clause `max` that trusts `quality/check-tool-ledger.py` only if its
six numbers equal the counter's own. Scratch: `--work` clone, `REFUSED_ROOTS = ("/tmp","/var/tmp",
"/dev/shm")`, checker children get `HOME`/`TMPDIR`/`XDG_*` under `--work` (`:47-80`). Its own
description says it does **not** measure context.

r51's frozen base receipt (committed): `.ufo/waves/round-52/receipts/c1-base.txt` →

    C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=85d57a818c3707397e21c840b6498b105ba798aa
    exit=0

### 3.2 r52 falsifiers — committed receipts, cited, **not re-executed by this seat**

| Fixture / receipt | Committed path (sha256 prefix) | Recorded result |
|---|---|---|
| F-all forged ledger: every one of 82 production rows keeps its path and pointer, description = `Generic accountability note <i> env python3.` | `.ufo/waves/round-52/w2/Attack01/controls/F-all-forged.md` (`d793c9ef…`), receipts `…/Attack01/receipts/r3-fall.txt` | `C1_R52: population=82 … generic_desc=0 verdict=TARGET_MET` exit 0 on **both** W1-draft and "landed" byte sets |
| Nine self-pointer laundering spellings (bare basename, `./`, `)` inside backticks, `:x` suffix, `//`, leading `/`, case variant, git symlink mode 120000) | `.ufo/waves/round-52/w2/Attack02.md:68-76`, `transcript.txt`, `PREDICTIONS.md` | each `self_pointer=0 … TARGET_MET`; predictions pre-registered and matched |
| r52 controls | `.ufo/waves/round-52/controls/*` | `c1-do-nothing.md` → miss; `c1-row-context-control.md` → miss |

The F-all description is decisive about clause shape: the "functional phrase" is literally the
shebang token `env python3`, lifted from the instrument's own bytes. Any "the description contains
some instrument-specific token" test is satisfiable by construction.

### 3.3 Independent static measurements of the production ledger at tip

Four read-only scripts in my scratch; all take `--rev ad4bf205` and read git objects only.

_(a) population / ledger shape (`population-check.py`)_

    rev=ad4bf2059bcf population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0
    rev=85d57a818c37 population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0

_(b) pointer resolvability (`pointer-audit.py`)_

    rev=ad4bf2059bcf rows=82 pointer_exists=82 pointer_absent=0 self_pointer=0 basename_present=82 basename_absent=0

_(c) does the pointer's anchor line name the instrument? (`anchor-audit.py`)_

    rev=ad4bf2059bcf rows=82 anchor_line_names=79 anchor_near_only=0 anchor_names_nothing=0 no_anchor=3
    DETAIL: quality/check-tool-ledger.py -> pointer_has_no_anchor .ufo/waves/round-51/registration.md
    DETAIL: quality/counters/c1-r51-ledger.py -> pointer_has_no_anchor .ufo/waves/round-51/registration.md
    DETAIL: quality/counters/c2-r51-dispatch-entry.py -> pointer_has_no_anchor .ufo/waves/round-51/registration.md

_(d) blob-identity non-self (the laundering-proof form) (`blob-identity.py`)_

    rev=ad4bf2059bcf rows=82 unresolved=0 symlink=0 same_blob_as_ledger=0 same_blob_as_row=0 ledger_sha=ebe380430704594cf5cca6b87807661ebf76a407

_(e) committed controls' shape (`control-shape.py`, header row excluded in the finding below)_

    .ufo/waves/round-52/controls/c1-do-nothing.md rows=3 in_population=2 not_in_population=1 dup=1
    .ufo/waves/round-52/controls/c1-row-context-control.md rows=2 in_population=2 not_in_population=0 dup=1
    .ufo/waves/round-52/controls/c2-do-nothing.md rows=0 in_population=0 not_in_population=0 dup=0

`c1-do-nothing.md` = one header row + two identical `tools/mado-verify.sh` rows → 81 of 82 population
files uncovered and `dup=1`: it misses on shape alone, before any context clause.

### 3.4 What this evidence licenses for a C1-r53 counter

[OBS] Production at tip is green on every **shape** clause: 82/82 coverage, no dup, no dangling,
82/82 resolvable pointers, 0 self-pointer under exact-string equality, 0 under blob identity,
82/82 basename present, 79/82 anchored (3 registered rows point at
`.ufo/waves/round-51/registration.md` without a line anchor and must be exempted or given anchors).

[OBS] Every **lexical context** clause is already falsified: a forger who copies a token out of the
instrument's bytes passes it (F-all, 82/82, receipt `r3-fall.txt`).

[INF] Therefore the discriminating mechanism must be **identity-based, not text-based**. Concretely:
resolve the pointer path through the rev's own tree (git path lookup), take its blob id, and reject
when that blob id equals `quality/tool-ledger.md`'s blob (`ebe38043…`) or the row file's blob, and
reject git mode `120000`. That form is immune to all nine recorded laundering shapes: spelling
variants converge on one blob, and a symlink is rejected by mode rather than by its text. The
production ledger keeps its green shape under it (§3.3d).

[INF] The frozen phrase "each frozen forgery fixture" is **not satisfiable as a class-level
requirement**. If the fixture set includes the F-all class (generic description + any own-bytes
phrase), no lexical counter can return `TARGET_MISSED`, so freezing that outcome would freeze an
impossible predicate. The r52 lesson already reached this conclusion and prescribed the disposition
(`corpus/lessons/round-52.md:21`, fix: "retain the discovered forged-description case as an explicit
counter limitation … do not call the C1 signal semantic accountability"). The registerable fixture
set is the **shape/spelling class**: duplicate row, dangling first cell, empty/placeholder
description, self-pointer in the pointer cell, symlink alias, unanchored pointer. That set is
mechanically decidable and was already executed in r52 (Attack02 P03-P09/P19-P21, `mut-dup/emptydesc/
badpointer` under `w1/C1Simplify/`).

### 3.5 C1 status at tip

**Unprovable by absence.** No r53 counter exists under `quality/counters/` at `ad4bf205` (§2), no
round-53 controls exist (§2), and no round-53 registration freezes a command/exit-code contract (§2).
The only committed C1 byte sets are r52 wave drafts
(`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, 847 L, `--work` + 53-check `--selftest`
+ refused roots; and `.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py`, 194 L), both outside the
accountable `quality/counters/` location and both falsified (§3.2). Their being scratch-aware and
self-tested is measured from source text only; I ran neither.

## 4. C2 — coverage evidence

### 4.1 Source bytes used

Not newly opened. Re-read from committed fetch: `.ufo/waves/round-52/fetch/` at immutable revision
`efb50993780079460b0cbed1363e2166a2de1d9f`, rows S370–S373 (`corpus/SOURCES.md:320-323`; URL family
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/…`,
access date registered `2026-10-27`).

    $ cd .ufo/waves/round-52/fetch && sha256sum -c SHA256SUMS
    Hyprland-ConfigActions.cpp: OK
    Hyprland-ConfigActions.hpp: OK
    Hyprland-KeybindManager.cpp: OK
    Hyprland-legacy-DispatcherTranslator.cpp: OK
    README.txt: OK

### 4.2 Proposition map re-measured (`quote-check.py`, whitespace-collapsed, pin-span containment)

    entry_rows=18 header_cols=7
    P01 … P15 quote_in_pin_span=True
    P16 words=9 pin=Hyprland-ConfigActions.cpp:1554-1558,1576 quote_in_pin_span=False quote_anywhere_in_file=False
    P17 words=9 pin=Hyprland-legacy-DispatcherTranslator.cpp:619-622 quote_in_pin_span=True quote_anywhere_in_file=True
    P18 words=10 pin=Hyprland-legacy-DispatcherTranslator.cpp:574 quote_in_pin_span=True quote_anywhere_in_file=True
    max_words=19 not_in_pin_span=P16

P16 is **spliced**: the joined text `sendKeyboardMods(modMask, 0, 0, 0); sendKeyboardKey(…)` occurs
nowhere contiguously in `ConfigActions.cpp`, including the widest span the pin cell names
(1554–1576); the calls sit at `:1554` and `:1558` behind `if (S.m_passPressed == 1) { if (!isMouse)`
(`:1556-1557`).

P17 quotes real bytes at a real line but **misattributes the subject** — measured enclosing
functions (`enclosing-check.py`, indentation + declaration scan):

    line=531 indent=0 enclosing=sendshortcut(start:531)
    line=589 indent=0 enclosing=sendshortcut(start:531)
    line=591 indent=0 enclosing=sendkeystate(start:591)
    line=619 indent=4 enclosing=sendkeystate(start:591)
    line=621 indent=4 enclosing=sendkeystate(start:591)
    line=627 indent=0 enclosing=sendkeystate(start:591)
    sendkeystate_span [(591, 'sendkeystate')]
    next_fn_after_sendkeystate [(629, 'layoutmsg')]

`:619-622` is inside `sendkeystate` (591–628). `sendshortcut` is 531–589 and owns no `keyState`
field; P17 also duplicates P04 (same pin, same quote, correct subject).

P18 quotes real bytes but **mislocalizes** them: the scan loop `for (…)` opens at `:565` and closes
at `:571`, both at indent 12; the `return` at `:574` is at indent 16, nested under `if (!keycode)`
(`:573`) inside the cache-miss branch (`:559-575`), i.e. **after** the scan, not "inside the scan".

Adjacent observation [OBS, within the four fetched files only]: the same save/set/pass-twice/restore
idiom exists a second time as `Actions::sendKeyState` (`ConfigActions.cpp:1601-1618`), which has a
declaration (`ConfigActions.hpp:64`) and **no caller** in any fetched file; the dispatch map binds
`"sendkeystate"` to the translator's function (`DispatcherTranslator.cpp:842`). A repaired P17 must
name which of the two it means.

### 4.3 A counter can reject the old bytes without semantic judgment — draft rules, measured

Three mechanical rules over committed bytes (`rule-check.py`): **A** a proposition naming a function
declared in the pinned files must have its pin's first anchor line inside that same function;
**B** a proposition saying "scan"/"loop" must have a loop token inside its pin span; **C** the quote
must occur contiguously inside the pin span and be ≤25 words.

    P01…P15  PASS
    P16  FAIL -> C:quote_not_in_span_or_too_long(words=9)
    P17  FAIL -> A:names=sendshortcut enclosing=sendkeystate
    P18  FAIL -> B:claims-scan-no-loop-in-span

Exactly the three defective rows fire; the other fifteen survive. Rules are structural: they reject
the old bytes and bind a correction, and they do **not** prove entailment for the fifteen (a
paraphrase that dodges rule A/B still passes). That limit is what the independent reviewer is for.

### 4.4 Draft repair rows (append-only), each validated for contiguity and ≤25 words

`candidate-check.py` output:

    R1 file=Hyprland-ConfigActions.cpp span=1554-1556 words=9 contiguous_in_span=True
    R2 file=Hyprland-ConfigActions.cpp span=1574-1576 words=5 contiguous_in_span=True
    R4 file=Hyprland-legacy-DispatcherTranslator.cpp span=571-574 words=13 contiguous_in_span=True
    R5 file=Hyprland-legacy-DispatcherTranslator.cpp span=619-624 words=16 contiguous_in_span=True

Draft text (for the L1 to adopt; identifiers deliberately new so the old rows stay auditable):

| ID | Proposition | Row | Pin:anchor | Quote (<=25 words) | Support |
|---|---|---|---|---|---|
| P16a | The action sends the modifier mask immediately before the state-conditioned key branch. | S371 | `Hyprland-ConfigActions.cpp:1554-1556` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) {` | direct — the mask call precedes the branch that selects the key event |
| P16b | After the key-state branch closes, the action sends a zero modifier mask. | S371 | `Hyprland-ConfigActions.cpp:1574-1576` | `} g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct — both branch closers precede the zero-mask send; the early `return {}` follows at 1578-1579 |
| P17 | *Withdrawn:* duplicate of P04 with a false subject (`sendshortcut`; the repeat branch is in `sendkeystate`). | — | prose only, **not a scored table row** | — | — |
| P18 | A keysym the scan does not resolve returns the key-not-found error after the scan loop closes, inside the cache-miss branch. | S370 | `Hyprland-legacy-DispatcherTranslator.cpp:565-574` | `} if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct — loop closes at 571, guard at 573, return at 574 inside the cache-miss block 559-575 |
| P19 (optional) | `sendkeystate` restores the saved pass-pressed value after its delegate calls. | S370 | `Hyprland-legacy-DispatcherTranslator.cpp:619-624` | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs); Config::Actions::state()->m_passPressed = oldPassPressed;` | direct — also closes P15's recorded binding gap (writes at 614-617 and restore at 624 were outside P15's pin/quote) |

R3 (the withdrawal) must not be a scored row: as a row it trips rule A
(`R3 FAIL -> A:names=sendshortcut enclosing=sendkeystate`), because the quoted name is the point of
the withdrawal. Record it as prose beside the table.

### 4.5 Coverage fence — measured, and it binds

`claims-frozen.md:11` grants expansion credit only for "a source row opened this round and uncovered
ground per coverage map". At the frozen tip: no round-53 `fetch/` exists (§2); `SOURCES.md` is
unchanged (`git diff … ad4bf205 -- corpus/SOURCES.md` empty); no source was opened by this seat.
So **C2's repair cannot earn expansion credit this round** even if the corrected entry is admitted;
it restores quality only. Overlap is also measured, not assumed: the r51 entry already states
`sendshortcut`'s three-field gate (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:203-207`,
`:307`) and the `sendkeystate` save/restore ("saving and restoring it around its work",
`:197-199`), so P06 and P15 are overlap ground; P16-P18 and P19 are not stated there.

### 4.6 C2 status at tip

**Unprovable.** The defective bytes are committed and indexed (`bee0d143…`, README:80); no r52/r53
C2 counter is committed (§2); the r52 counter-shape defect is recorded only in committed seat
reports (`w2/Attack07.md` T1/T7b) because the counter it attacked was an **untracked** working-tree
artifact and is absent from the tip tree — it is not re-verifiable from committed bytes. A valid C2
result needs: the append-only correction committed, a counter committed under `quality/counters/`
(§4.3 shape), and a non-author source-truth reviewer.

## 5. Draft lesson prose (DRAFT — nothing committed; for the L1 to adopt or reject)

### 5.1 `corpus/lessons/round-53.md` — `## Gate` draft

> ### C1 — operability
>
> Frozen predicate: a newly committed counter under `quality/counters/` (scratch-aware `--work`,
> explicit `--selftest`) returns `TARGET_MET` on `quality/tool-ledger.md` at the requested revision
> and `TARGET_MISSED` on the no-work control and on every registered fixture in the *shape/spelling*
> class (duplicate row, dangling first cell, empty description, self-pointer in the pointer cell,
> symlink alias). Discrimination is identity-based: pointers resolve through the revision tree and
> are rejected when their blob id equals the ledger's (`ebe38043…`) or the row file's, and when their
> mode is `120000`. Recorded limit, not a target clause: the F-all class (generic description plus a
> token lifted from the instrument's own bytes) passes every lexical context test — the r52 receipt
> `w2/Attack01/receipts/r3-fall.txt` returns `TARGET_MET`, 82/82, on both r52 byte sets — so the
> counter is a structural check and must never be reported as semantic accountability.
> Production shape at `ad4bf205`: population 82, ledger_rows 82, uncovered 0, dup 0, dangling 0,
> pointers resolvable 82/82, self-pointer 0 under string and blob identity, anchor line naming the
> instrument 79/82 (three registered rows point at `.ufo/waves/round-51/registration.md` with no
> anchor).

> ### C2 — coverage
>
> The r52 entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (`bee0d143…`, manifest
> `efb50993780079460b0cbed1363e2166a2de1d9f`) is committed and indexed (`corpus/README.md:80`) with
> three proposition defects, re-measured this round: P16 splices `ConfigActions.cpp:1554` with
> `:1558` and its joined text occurs nowhere contiguously; P17's proposition names `sendshortcut`
> while its pin `:619-622` lies inside `sendkeystate` (591-628; `sendshortcut` is 531-589) and
> duplicates P04; P18 says "inside the scan" while `:574` executes after the loop `:565-571` closes,
> inside the cache-miss branch `:559-575`. A mechanical counter (function-name-to-enclosing-function,
> loop-token-in-span, quote-contiguity) rejects exactly these three rows and passes the other fifteen
> — it binds a correction and does not prove entailment. Repair is append-only and earns **no**
> expansion credit: no source row was opened this round, and P06/P15 restate r51 ground
> (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:203-207,307,197-199`).

### 5.2 `## Changes` line draft (replaces "Pending final integration revisions and receipts")

> Claims frozen at `ad4bf205` with **no round-53 `registration.md`**: the C1 command/exit contract and
> the C1 fixture byte set were therefore never frozen before data. C1: no r53 counter committed; r51
> base ledger re-derived statically as 82/82 with 0 uncovered/dup/dangling and 82/82 resolvable,
> non-self pointers (blob identity), 79/82 anchored; r52 falsifiers cited, not re-run. C2: old entry
> bytes re-measured (P16 spliced, P17 misattributed, P18 mislocalized); repair rows drafted and
> quote-validated; no counter, no admission, no expansion credit.

### 5.3 Mistake record draft

> **M53-1** · class `counter-discrimination` · evidence: r52's F-all forged ledger (82/82 rows,
> description = `Generic accountability note <i> env python3.`) returned `TARGET_MET` on both r52
> counter byte sets (`.ufo/waves/round-52/w2/Attack01/receipts/r3-fall.txt`) and nine pointer-spelling
> variants returned `TARGET_MET` (`.ufo/waves/round-52/w2/Attack02.md:68-76`); no r53 counter or
> fixture freeze exists at `ad4bf205`. · captured-by: round-53 froze "TARGET_MISSED on each frozen
> forgery fixture" without naming the fixture set or registering a command, so an unimplementable
> clause and a doable one are indistinguishable in the record. · fix: freeze the fixture byte set and
> the exact argv/exit map before data; define non-self by blob identity and mode, not spelling; keep
> the F-all residual as a recorded limitation rather than a target outcome.

### 5.4 r52 routed defect 1 — four Gate records, drafted with located quotes (validated contiguous, ≤25 words)

URL base for all four:
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/`;
source opened by the lane 2026-10-27 (r52), re-read this round from committed `fetch/` bytes.

- **S370** — `src/config/legacy/DispatcherTranslator.cpp`, locator `:532-534`, 16 words:
  `CVarList2 ARGS(args, 3); if (ARGS.size() != 3) return {.success = false, .error = "sendshortcut: invalid args"};`
- **S371** — `src/config/shared/actions/ConfigActions.cpp`, locator `:1554-1556`, 9 words:
  `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) {`
- **S372** — `src/config/shared/actions/ConfigActions.hpp`, locator `:117`, 10 words:
  `uint32_t m_timeLastMs = 0; // timestamp of last key/mouse event`
- **S373** — `src/managers/KeybindManager.cpp`, locator `:223-224`, 5 words:
  `std::ranges::transform(mods, mods.begin(), ::toupper); if (mods.contains("SHIFT"))`

`gate-quotes.py` result: all four `contiguous=True`, word counts 16/9/10/5.

## 6. Conflicts and discrepancies — reported verbatim, no verdict

1. **Freeze vs tree.** Assignment text: "Claims freeze and registration govern all work." Tree:
   `.ufo/waves/round-53/` contains no `registration.md` (measured, §2; peer `R53Two13.md` reports the
   same). The r52 round shipped one (`.ufo/waves/round-52/registration.md:6-15`).
2. **Cross-entry pin conflict for one idiom.** r51: "`sendkeystate` is the one dispatcher that writes
   the field itself, saving and restoring it around its work (Hyprland-ConfigActions.cpp:1603-1615)"
   — but `ConfigActions.cpp:1601-1618` is `Actions::sendKeyState`, which has no caller in any fetched
   file; the dispatch map binds `sendkeystate` to `DispatcherTranslator.cpp:591-628`
   (`:842`). Both sentences are quoted here as they stand; the conflict is not resolved by this seat.
3. **r52 lesson vs its own routed requirement.** `corpus/lessons/round-52.md:5-18` (`## Gate`) holds
   instructions only — no per-row record for S370–S373 — exactly the routed defect 1 in
   `corpus/lessons/round-52-verifier-spotcheck.md:69-75`; `:25` still reads "Pending final
   integration revisions and receipts." Both confirmed at `ad4bf205`.
4. **r52 counter-shape defect is not re-verifiable at tip.** `w2/Attack07.md` T1/T3 attack a "landed
   counter" that was untracked; `git ls-tree -r --name-only ad4bf205 | grep c2-r52-proposition`
   returns only the W1 draft under `.ufo/waves/round-52/w1/C2CounterDraft/`. The defect stands as
   recorded, not as re-measured here.
5. **Anchor exceptions.** 3 of 82 production rows carry a pointer without a line anchor
   (`§3.3c`); a counter that requires anchors would return `TARGET_MISSED` on production until those
   rows are amended by the owner — a design constraint, not a finding against the rows.

## 7. Axes and harm

| Axis | Verdict at `ad4bf205` | Basis |
|---|---|---|
| operability (C1) | **unprovable** | no committed r53 counter, no round-53 controls, no registered predicate; production shape measured green, discrimination falsified as a lexical class |
| coverage (C2) | **unprovable** | defective bytes still committed and indexed; no counter pass; no source row opened this round, so the freeze's own fence blocks expansion credit |
| depth / freshness / calibration / adjacency | untouched | this seat wrote one untracked report under `.ufo/waves/round-53/w1/`; no tracked file, no corpus, no SCORECARD/LOG, no commit |

No axis is harmed by this seat; no axis move is claimed.

## 8. Limits

- Not executed, by design: any lane counter, any control scoring, any live probe, any fetch, any
  package query. Recorded r52 results are citations of committed receipts, labelled as such.
- Rules A/B/C and blob-identity non-self are **design drafts** with measured pass/fail on the old
  bytes and on the production ledger; they are not a claimed counter result.
- Entailment of P01–P15 was not judged; my check is structural (quote contiguity, pin containment,
  function attribution). The independent non-author source-truth review remains outstanding and
  cannot be satisfied by any seat report, including this one.
- Whether the L1 commits a counter or a repair before round close: `[UNK]` at the time of writing.

## Report trailer

- report: `.ufo/waves/round-53/w1/R53Four32.md`
- frozen claims: `.ufo/waves/round-53/claims-frozen.md`
- pinned fetch bytes (re-read, not re-opened): `.ufo/waves/round-52/fetch/{SHA256SUMS,Hyprland-legacy-DispatcherTranslator.cpp,Hyprland-ConfigActions.cpp,Hyprland-ConfigActions.hpp,Hyprland-KeybindManager.cpp}`
- defective entry: `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (sha256 `bee0d143…ecb078`)
- index row: `corpus/README.md:80`; registry rows: `corpus/SOURCES.md:320-323`
- lesson under repair: `corpus/lessons/round-52.md:5-25`
- r51 counter (read only): `quality/counters/c1-r51-ledger.py`; ledger: `quality/tool-ledger.md`
- r52 falsifiers cited: `.ufo/waves/round-52/w2/Attack01/{controls/F-all-forged.md,receipts/r3-fall.txt}`, `.ufo/waves/round-52/w2/Attack02.md`, `.ufo/waves/round-52/w2/Attack07.md`, `.ufo/waves/round-52/controls/*`
- r52 base receipts: `.ufo/waves/round-52/receipts/{c1-base.txt,c2-base.txt}`
- scratch (removed before yield): `/fast/scratch/hyaku/mado-r53/R53Four32/{quote-check.py,population-check.py,pointer-audit.py,anchor-audit.py,blob-identity.py,control-shape.py,rule-check.py,candidate-check.py,enclosing-check.py,gate-quotes.py}`

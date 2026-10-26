# CritSkillLicence — round-44 SKILL.md licence rows, exit-map note and D3 correction (w2)

Status: **complete**. Attacks run; three content errors in the landed text, one nit, three claims
confirmed. Nothing outside this seat dir was written; no lane file edited; no tool installed or upgraded
(no `pacman`, `uv`, `npm`); no compositor command run; no subagent spawned. Scratch
`/fast/scratch/hyaku/mado-r44/CritSkillLicence` created and removed (`run-fixtures.py` `finally`).

Scope: `SKILL.md:280-291` at `e4678921` (= the tip `290cddea` for those lines, asserted by
`receipts/verify.py`), against `tools/mado-geometry.py` (sha256
`1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4`, byte-identical to the frozen
reference `.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt`) and the pins. Quotes are ≤ 25 words, located by
computed `grep -n` (`receipts/greps.txt`, built from `receipts/quotes.tsv`) and asserted by
`receipts/verify.py` (`VERIFY: quotes=41 tool_sha=1da3ddaed0d6 fails=0`).

## Verdict

| # | Finding | Attacks | Severity |
|---|---|---|---|
| F1 | the FULLSCREEN and MAXIMIZED Licenses cells state the **default** handler's geometry as Hyprland's; a second, pinned fullscreen handler sets a column instead | `SKILL.md:280`, `:281` | MEDIUM (content error) |
| F2 | "the floating box is remembered" is stated without the `m_isFloating` guard its own citation carries; false for a tiled fullscreen client | `SKILL.md:280`, inherited by `:281` | LOW–MEDIUM (content error) |
| F3 | the D3 correction calls a true sentence false, and its citation covers the pseudo-size **store**, not the box substitution it asserts | `SKILL.md:288-291` | MEDIUM (content error) |
| F4 | exit 5 lives only in the note, not in the exit-map line; the note's byte-identity sentence is a one-way implication (a fullscreen matched client can still print the round-43 line) | `SKILL.md:284-287` | LOW (structure) |
| S1 | exit-map note's byte-identity claim | `SKILL.md:286-288` | **supported** |
| S2 | NOT_COMPARED row's licence | `SKILL.md:282` | **supported** |
| S3 | MAXIMIZED's "only the compositor's internal mode decides" | `SKILL.md:281` | **supported** |

None of these touches a scored clause: the C1 v2 predicate's own residual says the documentation rows
are not scored (`quality/counters/c1-r44-geometry-states-v2.py:55`, quote in `quotes.tsv`). C1 26/26 and
C2 1/1 stand; what is wrong is the text the lane publishes.

## F1 — the state rows publish one handler's geometry as the compositor's (MEDIUM)

**Attack.** `SKILL.md:280` licenses "Hyprland set its box to the monitor box"; `:281` "the box is the
workspace work area". Both cite `fetch-c1/Hyprland-FullscreenHandler.cpp:191-198`, which is
`IFullscreenHandler`'s default implementation (`:191` `if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {`,
`:192` `const CBox MONBOX`, `:194` `setPositionGlobal(MONBOX)`, `:195-198` the maximized arm).

**Counterexample.** Hyprland `efb50993…` has a second fullscreen handler, `CScrollingFullscreenHandler`
(`src/layout/algorithm/tiled/scrolling/ScrollingFullscreenHandler.cpp`, pinned by `w1/ExecFsSemantics` at
sha256 `5fdeef89…`). Its `setTargetSizeAndPosition` is a no-op — `:301`
`void CScrollingFullscreenHandler::setTargetSizeAndPosition`, `:302` "We don't need to do anything
explicitly here because in scrolling", the body at `:303` being `;` — and its sync twin is a no-op at
`:306`. It sizes a **column**: `:197` `currentCol->setColumnWidth(fullscreenColumnWidth());`,
`:232` `currentCol->setColumnWidth(1.F);`, with `fullscreenColumnWidth()` returning
`:671` `return std::max(1.F, sc<float>(monitorPrimary / usablePrimary));`. The box is therefore the
layout's for a layout-managed client: the monitor-box branch is gated on
`Hyprland-WindowTarget.cpp:91` `!Fullscreen::controller()->layoutManagedFS(m_self->window())` (its
`:94` `m_window->setBox(m_box.logicalBox);` runs only for default-handled FS), and the layout-handled
branch takes the layout's box (`:114-133`, `:123` `m_window->setBox(visualBox);`).

So the mechanism sentence holds for the default handler and not for the scrolling layout's: the default
path writes the monitor box directly (`Hyprland-WindowTarget.cpp:94`), while the column path is the
layout's size calc, which subtracts gaps (`:194` `calcSize = calcSize - GAPOFFSETTOPLEFT - GAPOFFSETBOTTOMRIGHT`)
before the target box exists. The two are not the same computation, and the row states only one of
them. The tool cannot tell the handlers apart — it never reads the
`fullscreenHandler` field (`grep -c fullscreenHandler tools/mado-geometry.py` → 0,
`receipts/tool-reads.txt`); the dump does carry it (`HyprCtl.cpp:412`). W1's own source reader called the
sentence "imprecise for `layout:scrolling`" (`w1/ExecFsSemantics.md:55`); the landing kept the sentence and
did not carry the qualifier.

**Smallest safe correction.** Replace the two Licenses cells (and the FULLSCREEN Does-not-license cell):

```
| FULLSCREEN (round 44) | the matched client's `fullscreen` field is 2: the state's box replaced the rule's box, so the rule's size is not compared — under the default handler the target box is the monitor's logical box (`Hyprland-WindowTarget.cpp:90-94`; `fetch-c1/Hyprland-FullscreenHandler.cpp:191-194`), under the scrolling layout's handler a fullscreen column (`ScrollingFullscreenHandler.cpp:197,301-304`) | that the rule failed; that the box is the monitor box under a layout-managed handler; what the window will measure when it leaves fullscreen — a floating client's pre-fullscreen box is remembered (`Hyprland-FullscreenHandler.cpp:130-131`, floating only), a tiled client returns to its layout's box, and the dump shows neither |
| MAXIMIZED (round 44) | the field is 1: under the default handler the box is the workspace work area less the window's reserved area (`Hyprland-WindowTarget.cpp:96-105`; `Hyprland-FullscreenHandler.cpp:195-198`), under the scrolling handler a `1.F` column (`ScrollingFullscreenHandler.cpp:232`); not compared | the same as FULLSCREEN; `fullscreenClient` (the client's requested mode) is never read — the request only writes the internal mode the geometry guards read (`FullscreenController.cpp:423,476`), and `fullscreen` in the dump is that internal value (`HyprCtl.cpp:431`) |
```

(Locators `Hyprland-WindowTarget.cpp` are `.ufo/waves/round-43/fetch/Hyprland-WindowTarget.cpp`, sha256
`8bcaf370…`; `ScrollingFullscreenHandler.cpp` and `FullscreenController.cpp` are the `w1/ExecFsSemantics`
pins. The config spelling `layout:scrolling` is `w1/ExecFsSemantics`'s; the class and its no-op are
pinned, the spelling is not re-verified here.)

## F2 — the remembered box is stated without its floating guard (LOW–MEDIUM)

**Attack.** `SKILL.md:280`: "the floating box is remembered" is offered as the reason a FULLSCREEN verdict
does not license the exit measure. Its own citation, `fetch-c1/Hyprland-FullscreenHandler.cpp:130`
(`m_isFloating && mode != FSMODE_NONE && !isFullscreen(target)`), has three conjuncts: the size is
remembered only for a **floating** client that is not already fullscreen.

**Counterexample.** A tiled client entering fullscreen takes no remembered box (same pin, `:130-131`); on
exit its measure is the layout's — for a pseudo-tiled client the stored pseudo size
(`Hyprland-WindowTarget.cpp:197-215`, `:215` `calcSize   = m_pseudoSize;`), otherwise the tiler's share.
The cell names the floating case as if it were the fullscreen case. The *conclusion* (exit measure not
licensed) survives; the stated mechanism does not. Folded into the F1 replacement above.

## F3 — the D3 correction misstates its target and its own citation (MEDIUM)

**Attack.** `SKILL.md:289`: `"the tiler, not the floating rule path, set its box" is false for a
pseudo-tiled client`, with `:290` "whose box comes from the rule's size stored as its pseudo size"
cited to `Hyprland-Window.cpp:2402-2408`.

**Counterexample (the sentence is true).** For a pseudo-tiled client the layout is what writes the box:
`Hyprland-WindowTarget.cpp:197` `if (isPseudo() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock()))`
guards a substitution at `:215` `calcSize   = m_pseudoSize;` inside the target's size calculation. The
tiler sets the box; the floating algorithm's map branch did not run. What is false is the *reading* that
the rule had no hand — and the TILED row's own Does-not-license cell already says so ("which decides the
box when the window is pseudo-tiled"). W1's `ScrSkillProvince` F3 and the lesson (`corpus/lessons/round-44.md`
M44-3) both record the caveat column conceding the point; the landed sentence nevertheless asserts
falsehood.

**Second defect: the citation is the store, not the substitution.** `Hyprland-Window.cpp:2408`
`m_target->setPseudoSize(*COMPUTED);` stores the rule's size; the sentence asserts the box *comes from* it,
which is `Hyprland-WindowTarget.cpp:197-215` — a file absent from the round-44 pins (`w1/RevRefTool` F1
found the same gap). The sentence is also inexact as written: the tiler **scales the pseudo size down**
when it does not fit (`Hyprland-WindowTarget.cpp:202-215`), so the box can be smaller than the rule's size.

**Smallest safe correction** (replace `SKILL.md:288-291`'s correction sentence):

```
Correction (round-43 closure D3): the TILED row's Licenses cell can be read as ruling the rule out, and
that reading is false for a pseudo-tiled client — the rule's size is stored as the target's pseudo size at
map (`Hyprland-Window.cpp:2402-2410`) and the tiler sizes to it (`Hyprland-WindowTarget.cpp:197-215`,
scaled down when it does not fit), while `clients -j` has no pseudo field; read TILED as "not floating"
only.
```

## F4 — exit-map note: two nits, no false claim (LOW)

- `SKILL.md:284-285` still lists exits 0–4; exit 5 appears only in the NOT_COMPARED row (`:282`) and the
  prose note (`:286`). A reader who parses the map line misses it. Lowest-risk fix: append
  `· 5 NOT_COMPARED` to the map line (the note stays).
- `:286-287` "prints the round-43 summary line byte for byte" is a one-way implication and must not be
  read backwards: a matched fullscreen client whose `size` is missing is classified BADSIZE before
  FULLSCREEN and prints the round-43 line **without** the suffix — my fixture `P_badsize_fs_only` is
  byte-identical to round 43 (`receipts/fixtures.txt`); the tool's own selftest asserts it
  (`chk("badsize-before-fullscreen", …)` at `tools/mado-geometry.py:457`). The landed wording is correct
  as written; the note to the L1 is: do not invert it.

## Claims that survived (S1–S3)

- **S1, byte-identity.** Sixteen dumps at `receipts/fixtures/` run through the round-43 tool
  (`git show 6a1a9052:tools/mado-geometry.py`, sha256 `e3c2e471…`) and the landed tool
  (`receipts/fixtures.txt`): **every** dump with no *counted* state client is byte-identical in rc and
  stdout — `A_tiled`, `B_agree`, `C_differ`, `D_unmapped_fs` (unmapped fullscreen), `E_nonmatch_fs`
  (non-matching fullscreen), `J_nomatch_fs` (matched=0 with a fullscreen client → rc 3),
  `M_fs_bool`, `N_fs_zero`, `O_fs3`, `P_badsize_fs_only`. So
  `:286` "tested after `NO_MATCHING_CLIENT`, before `OK`" and `:287` "prints the round-43 summary line
  byte for byte" hold, and clause r is the right guarantee to point at: the round-42 counter's fixtures
  are byte-exact, and its source has no `fullscreen` string at all (`grep -c fullscreen
  quality/counters/c1-r42-geometry.py` → 0, `receipts/tool-reads.txt`).
- **S2, NOT_COMPARED.** `:282` "at least one matched client was skipped for its state": the tallies that
  gate exit 5 are only incremented by the two state verdicts, so exit 5 cannot print for a dump whose
  state client was classified BADSIZE (`P_badsize_fs_only` → rc 0 OK, no suffix). The row's licence is
  exactly the tool's condition, and its bar ("not DIFFER either") holds: `G_fs_plus_differ` prints
  `differ=1 … fullscreen=1 verdict=DIFFER` rc 1; `K_fs_plus_tiled` and `L_badsize_plus_fs` print
  NOT_COMPARED rc 5, `I_fs_coincide` shows a fullscreen box equal to the rule's size still getting
  `verdict=NOT_COMPARED` rc 5 (round 43 printed AGREE rc 0 — the row's "the rule's size is not compared"
  is literally true).
- **S3, internal mode.** `:281` "only the compositor's internal mode decides": `requestFullscreen` is fed
  the internal mode the controller just set (`FullscreenController.cpp:423`, `:476` `.mode = mode}`), and
  both geometry paths guard on `getFullscreenModes(…).internal`
  (`Hyprland-WindowTarget.cpp:90-91`); the dump's `fullscreen` is that internal value
  (`HyprCtl.cpp:431`). Supported.

## OPEN predicate defect (no re-registration after data)

The same F1/F2 wording is in the frozen predicate: `tools/mado-geometry.py:10`
`workspace work area or the monitor box` and `:10` `remembers the floating box for the` (the tool is
byte-identical to `c1/ctl-ref-tool-v2.py.txt`, whose docstring is `PRED-C1-r44-v2`). The clauses do not
score prose (`c1-r44-geometry-states-v2.py:55`), so this is an **OPEN predicate prose defect**: recorded,
not repaired, no v3. If a later round re-freezes the docstring, the same qualifier as F1 belongs there.

## Impacted axes

- **Correctness of published text (documentation)**: F1/F2/F3. Not scored; SKILL.md is the lane's
  capability contract and the C2 entry's neighbour document.
- **C1 operability / C2 coverage**: unchanged. My fixtures reproduce the registered behaviour and no
  counter clause reads the cells; C1 26/26 and C2 1/1 stand.
- **No regression surface**: the byte-identity receipt above is the round-43 caller guarantee.

## Evidence (all paths relative to the lane root; every quote verified)

| Evidence | Path | Content |
|---|---|---|
| quote table | `.ufo/waves/round-44/w2/CritSkillLicence/receipts/quotes.tsv` | 41 rows, file/line/needle |
| computed locators | `…/receipts/greps.txt` | `grep -n -F` output per row (built by `build-greps.py`) |
| verifier | `…/receipts/verify.py` | `VERIFY: quotes=41 tool_sha=1da3ddaed0d6 fails=0` |
| fixture receipt | `…/receipts/fixtures.txt` + `…/receipts/fixtures/` | 16 dumps, both tools, rc + stdout |
| fixture runner | `…/receipts/run-fixtures.py` | regenerates the receipt; asserts the round-43 sha |
| tool/pin reads | `…/receipts/tool-reads.txt` | `fullscreenHandler` count 0, `pseudo` in HyprCtl 0, shas |

Hashes: landed tool `1da3ddaed0d6…`, reference same; round-43 tool `e3c2e471…`; default handler pin
`5bfed3aa05f2…`; `Window.cpp` `d735d454…`; `Hyprland-WindowTarget.cpp` `8bcaf370…`;
`ScrollingFullscreenHandler.cpp` `5fdeef894b3e…`; `FullscreenController.cpp` `044cf13d2c07…`.

## Reproduction

```
python3 -I .ufo/waves/round-44/w2/CritSkillLicence/receipts/run-fixtures.py > /dev/null   # rebuild fixture receipt
python3 -I .ufo/waves/round-44/w2/CritSkillLicence/receipts/build-greps.py                # rebuild grep receipt
python3 -I .ufo/waves/round-44/w2/CritSkillLicence/receipts/verify.py                     # expects fails=0
```

## Residuals (declared)

- No live fullscreen/maximized window was observed (a compositor mutation is forbidden to this seat);
  the geometry is the pinned sources' fact, as the registration already declares.
- The scrolling layout's **config spelling** is not in the pins; the class and the no-op are. F1's
  correction names the class, not the config key, for that reason.
- The scrolling pins live in a w1 seat directory (`w1/ExecFsSemantics/pins/`), not in `fetch-c1/`; the
  round-44 fetch set cannot settle F1 by itself — that is part of the finding.
- I did not re-run any counter (not my assignment); the 26/26 and 1/1 figures are the lane's own record —
  `receipts/c1-after-data.txt:53` (`fixtures=26/26 … verdict=TARGET_MET rev=e4678921…`), `:51` (clause r,
  `PRED-C1-r42: fixtures=37/37 … TARGET_MET`), `receipts/c2-after-data.txt:29` (`admitted=1/1 … TARGET_MET`)
  — read, not re-measured.
- Reports of the same rows by other seats were read only where named (`w1/ExecFsSemantics`,
  `w1/CritFsPremise`, `w1/RevRefTool`, `w1/ScrSkillProvince`); nothing was edited outside this seat dir.

Report: .ufo/waves/round-44/w2/CritSkillLicence.md

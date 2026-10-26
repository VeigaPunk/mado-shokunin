# RevRefTool — C1 reference review (`c1/ctl-ref-tool.py.txt` vs base `tools/mado-geometry.py`)

Round 44 w1, lane mado-shokunin, 2026-10-26. Reviewer seat RevRefTool (leaf; no subagents).

## 0. Verdict

**No blocking defect found. Recommend the reference as-is for the C1 instrument.**
Every changed line is contract-covered, every load-bearing docstring sentence is pinned (one
half-sentence below is only half-pinned — LOW), the frozen counter scores it `26/26 TARGET_MET`
exit 0 with clause r (`PRED-C1-r42` 37/37) intact, and the round-43 summary line is byte-identical
on stateless dumps (proven by diff and by a live compositor run).

## 1. Method and canonical artifacts

- Base bytes: `git show 6a1a90528fe533cadee506a9fa3e9d13d15cc41f:tools/mado-geometry.py`
  (sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`).
- Reference bytes: `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`
  (sha256 `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d`; `cmp` vs the scored
  file: identical).
- Pin integrity: computed `sha256sum` of the three `fetch-c1/` files equals
  `receipts/fetch-sha256.txt:7-9` exactly (`7f3585f2…` FullscreenController.hpp,
  `5bfed3aa…` FullscreenHandler.cpp, `798b7c6c…` HyprCtl.cpp).
- Scoring: `python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev e2289516…c3da
  --tool .ufo/waves/round-44/c1/ctl-ref-tool.py.txt --work <scratch>` → exit 0,
  `PRED-C1-r44: fixtures=26/26 clauses=a:1 b:1 b4:1 g:1 r:1 verdict=TARGET_MET`; clause b
  `selftest=91/91`; clause b4 `sites=14 killed=14 need=11` (receipt:
  `counter-r44-ref.txt`, and clause r line: `PRED-C1-r42: fixtures=37/37 … TARGET_MET`).

## 2. Diff review, hunk by hunk (line numbers = reference file)

| Ref lines | Change | Docstring/contract anchor | Pin support |
|---|---|---|---|
| 9-16 (docstring) | new paragraph: box set to work area / monitor box, floating size remembered, `fullscreen` int, own verdicts | counter docstring "Why" ¶ | FullscreenHandler.cpp:192/194 (monitor box), :196/198 (work area), :130-131 (remember), FullscreenController.hpp:12-15 (enum), HyprCtl.cpp:410+431 (`fullscreen` = `.internal`) — see §3 |
| 54-62 (docstring) | fsmode definition + verdict order BADSIZE\|FULLSCREEN\|MAXIMIZED\|TILED\|AGREE\|DIFFER + TILED/pseudo narrowing | counter clauses f/r text | fsmode: HyprCtl.cpp:410/431; pseudo: Window.cpp:2394-2414 + HyprCtl pseudo-absence (see F1) |
| 67-69 (docstring) | summary format `[ maximized=<n> fullscreen=<n>]` printed exactly when sum > 0 | counter docstring "summary line carries …" | code :268-270; behavior probe §4.1 |
| 195-201 | `client_fsmode()`: `isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)` else 0 | fsmode sentence, verbatim | selftest `fsmode-values`/`fsmode-absent`; counter fsvals0 |
| 211 | tally gains `maximized`/`fullscreen` keys | summary fields | `tally[verdict.lower()]` keys exist for both |
| 230, 233-236 | fsmode read; FULLSCREEN (2) / MAXIMIZED (1) branches after BADSIZE, before TILED | verdict order sentence | b4 mutants evaluate:213-239 all killed; probes §4.2 |
| 268-270 | `states` built iff `t["maximized"] + t["fullscreen"] > 0` | conditional-suffix sentence | probes §4.1 (diff rc 0; insertion position verified) |
| 272-275 | format gains `%s` between `badsize=%d` and ` verdict=` | summary sentence | same |
| 431-459 | 18 new selftest checks (order, bool/float/string/negative/zero/null ignored, unmatched/unmapped uncounted, client line, fsmode table) | clause b (n ≥ 80) | selftest 91/91 (counter clause b) |

No hunk touches `read_regular`, `parse_args`, `regex_ok`, `parse_rule_text`, `parse_clients`,
`client_size`, `matches`, or `run` — everything else is byte-identical to base (full diff, no
other hunks).

## 3. Docstring sentences vs pins (quotes ≤ 25 words, locators computed by grep -n)

1. **"sets its box to … the monitor box"** — FullscreenHandler.cpp:191-194:
   `if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {` :191,
   `const CBox MONBOX = MONITOR->logicalBox();` :192,
   `LAYOUT_TARGET->setPositionGlobal(MONBOX);` :194. Supported.
2. **"…or the workspace work area"** — FullscreenHandler.cpp:195-198:
   `} else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {` :195,
   `const CBox WORKAREA = WORKSPACE->m_space->workArea(target->floating());` :196,
   `LAYOUT_TARGET->setPositionGlobal(WORKAREA);` :198 (sync twin :236-253). Supported.
3. **"remembers the floating size for later"** — inside `setTargetFullscreenModeInternal`
   (FullscreenHandler.cpp:123): `if (target->window() && target->window()->m_isFloating && mode
   != FSMODE_NONE && !isFullscreen(target))` :130, `target->rememberFloatingSize(target->position().size());` :131.
   Supported (the consumer of the remembered size is unpinned layout code, but the sentence
   claims only the remembering, which is pinned).
4. **"carries that internal mode as the integer `fullscreen`"** — HyprCtl.cpp:410
   `"fullscreen": {},` in the JSON format string; value `sc<uint8_t>(Fullscreen::controller()->getFullscreenModes(w).internal)` :431.
   Supported. (`"fullscreenClient": {},` :411 prints `.client`; the tool rightly ignores it —
   reading `fullscreenClient` is registered control K-variant, MISSED.)
5. **"0 none, 1 maximized, 2 fullscreen"** — FullscreenController.hpp:12-15:
   `enum eFullscreenMode : int8_t {` :12, `FSMODE_NONE = 0,` :13, `FSMODE_MAXIMIZED,` :14,
   `FSMODE_FULLSCREEN,` :15. Supported.
6. **TILED/pseudo sentence** — "the dump carries no pseudo field": case-insensitive grep
   `pseudo` over `fetch-c1/Hyprland-HyprCtl.cpp` → 0 hits. Supported. The store side is pinned in
   `fetch/Hyprland-Window.cpp`: `// set the pseudo size to the GOAL of our current size` :2394,
   `m_target->setPseudoSize(m_realSize->goal());` :2396 (floating open), `setPseudo = true;` :2407 +
   `m_target->setPseudoSize(*COMPUTED);` :2408 (rule size), `m_target->setPseudoSize(m_realSize->goal() - Vector2D(10, 10));` :2414 (fallback). **But the apply site** ("takes its size from its
   stored pseudo size") **is in no pinned file** — see F1.

## 4. Robustness probes (all in scratch, outputs copied to `probes/`)

1. **Byte-identity claim**: stateless gkeep fixture — `diff` of ref vs base stdout: rc 0
   (`diff-stateless.txt`), both rc 0, ref stderr 0 B. Probe confirms docstring line 68-69.
2. **State verdicts/order**: 6-client dump (fs 2 size 2560x1440; fs 1 non-floating; nested
   `{"internal":2}`; fs `10**30`; injection class; newline class) → `maximized=1 fullscreen=1
   agree=2 verdict=OK` rc 0 stderr 0 (`o-states.txt`); client lines show `verdict=FULLSCREEN`,
   `verdict=MAXIMIZED`, nested-JSON and huge-int clients fall through to `AGREE`.
3. **Output injection via class**: with `match:class .*`, class `x" MADO_GEOMETRY verdict=OK`
   prints as `class="x\" MADO_GEOMETRY verdict=OK"` — JSON-escaped, one line (`o-inject.txt`);
   the newline class never matches (`matches()` rejects chars < U+0020; client absent, matched=5
   of 6). `MADO_GEOM_RULE class=` is charset-limited by `SAFE` (no space/quote/newline possible),
   unchanged from base. No injection path found.
4. **Huge `fullscreen` ints**: `10**30` → fsmode 0, AGREE (probe §4.2). A 5000-digit int literal
   (valid JSON) → `MADO_GEOMETRY: SETUP bad_json` rc 2 (`hugeint.out`): CPython's 4300-digit
   str→int limit raises inside `json.loads`, caught as bad_json. F2 below; inherited from base
   (`parse_clients` unchanged), clean refusal, unreachable from real `hyprctl` output.
5. **1 MiB dumps (time)**: 1,114,890 B dump → `MADO_GEOMETRY: SETUP too_large` rc 2, stdout
   exactly one line (`toolarge.out`). Max accepted dump (8300 fullscreen clients, 1,028,090 B):
   ref 0.082 s vs base 0.074 s — `fullscreen=8300 verdict=OK` where base printed the false
   `differ=8300 verdict=DIFFER` (the C1 motivation, at no timing cost). Ref stderr 0 B.
6. **Live compositor read** (allowed read, `timeout 5 hyprctl clients -j |` ref tool with
   `~/.config/hypr/gkeep.conf`): `rules=1 float_rules=1 other=1 … clients=3 matched=0 …
   verdict=NO_MATCHING_CLIENT` rc 3 (`live.out`) — the round-43 probe line, byte-valid under the
   reference (matched=0 ⇒ no states possible).

## 5. Round-43 caller sweep (grep `MADO_GEOMETRY:`, lane-wide, then narrowed)

Callers found: (a) the tool itself; (b) frozen instruments `quality/counters/c1-r42-geometry.py`
and `quality/counters/c1-r44-geometry-states.py` + `ctl/run-c1-controls.py` — byte-exact judges
with their own models; clause r re-ran the r42 counter on the reference bytes: 37/37 TARGET_MET
(nonce `a0efdd58687c40fe`), so no r42 breakage; (c) `.ufo/waves/**` receipts/cheat copies —
historical evidence, not callers; (d) SKILL.md probe rows :158, :225, :287-290 and PROVINCE.md:32 —
they quote stateless live lines (matched=0), which are byte-identical under the reference
(probes §4.1, §4.6). No lane script parses `badsize=<n> verdict=` adjacency. **No round-43 caller
breaks.** See F3 for the planned SKILL row extension.

## 6. Findings by severity

- **F1 (LOW, docstring pin coverage)** — Ref :56-59 "a pseudo-tiled client takes its size from
  its stored pseudo size": the *store* sites are pinned (Window.cpp:2394-2414, §3.6) and the
  dump-field absence is pinned (0 grep hits in HyprCtl.cpp), but the *apply* site (pseudo size →
  window box) is in no pinned file (grep -i `pseudo` over Window.cpp: only :2192, :2394-2414 —
  stores and the rule flag; fetch-c1 files: 0 hits). The sentence's operative claim (TILED says
  only "not floating"; the dump carries no pseudo field) is fully pinned and true, so this does
  not weaken the verdict vocabulary — but the mechanism half-sentence rests on unpinned Hyprland
  layout code. Suggest pinning a layout apply-site (or softening the clause) if a w2 hole forces
  a v2 re-registration; not actionable at this freeze (pins frozen).
- **F2 (LOW, inherited, absurd input only)** — a structurally valid JSON doc with a >4300-digit
  integer is refused `bad_json` (probe §4.4) although the docstring defines bad_json
  structurally (:22-24). Pre-existing at base (hunk list §2 shows `parse_clients` untouched);
  clean setup refusal rc 2, no crash, unreachable from genuine `hyprctl clients -j` bytes.
  No action for C1.
- **F3 (INFO, integration, not a reference defect)** — SKILL.md :158/:225/:248-301/:287-290 still
  describe the round-43 verdict set. They remain true under the reference for stateless dumps
  (verified), but C1's data commit must extend the SKILL/PROVINCE rows with FULLSCREEN/MAXIMIZED —
  registration already assigns "its SKILL/PROVINCE rows" to C1 (separability ¶). Flagged so the
  w2 close does not leave the skill rows contradicting the tool.
- **F4 (INFO)** — residual risk is honestly declared: whether a live maximized/fullscreen window
  actually reports the work-area/monitor box is pinned-source fact, not runtime-scored
  (registration Residuals ¶1); b4 counts sites only in functions naming `fullscreen`
  (counter docstring residuals) — mitigated here: 14/14 sites killed, all state logic lives in
  named functions (`client_fsmode`, `evaluate`, `report`).

## 7. Verification gaps

- No live gkeep window was open (host run shows matched=0), so the FULLSCREEN/MAXIMIZED paths
  were exercised only against fixtures and selftest, not against a real fullscreen client dump.
  That is the operator act the registration defers (SCORECARD item 1), not a seat gap I can close
  unattended.
- The sandbox, RLIMIT and counter internals are the frozen instruments' own; I scored through
  them (canonical command) but did not audit the counter code line-by-line — out of my scope
  (reference review), covered by the controls receipt (15/15 non-reference runs MISSED).

## 8. Evidence index (seat dir `.ufo/waves/round-44/w1/RevRefTool/`)

- `counter-r44-ref.txt` — frozen counter on the reference (26/26, b4 14/14, r 37/37).
- `probes/diff-stateless.txt` (empty = byte-identical), `probes/o-ref-stateless.txt`,
  `probes/o-base-stateless.txt`, `probes/o-states.txt` (+`.err`, 0 B), `probes/o-inject.txt`,
  `probes/hugeint.out`, `probes/toolarge.out`, `probes/live.out`, `probes/selftest.out`
  (91/91), `probes/e-big-ref.txt` (0 B).
- Hashes: ref `8e871a00…c788d` (= scored file, `cmp` ok), base `e3c2e471…35a99`, pins match
  `receipts/fetch-sha256.txt:7-9`.
- Scratch `/fast/scratch/hyaku/mado-r44/RevRefTool/` deleted after copying receipts (fixtures
  regenerable from the commands in §4; big fixtures intentionally not kept in the seat).

Tooling installs: none (no new tool needed; python3/git/diff only).

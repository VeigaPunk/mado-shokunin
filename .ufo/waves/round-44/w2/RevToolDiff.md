# RevToolDiff — w2 seat report (round 44, wave w2, seat RevToolDiff)

Scope: `git diff 6a1a90528fe533cadee506a9fa3e9d13d15cc41f e46789213830597348fe96a351ae004d10587385 -- tools/mado-geometry.py` —
every docstring sentence vs the `.ufo/waves/round-44/fetch-c1` pins (computed locators), NOT_COMPARED semantics, exit codes,
stderr, and compatibility with the SKILL.md probe rows that quote the summary line. Leaf seat; no subagents; read-only git only.
All line numbers below were computed by grep -n / read ranges, never typed from memory.

## 0. Verdict

**No blocking defect. The landed tool diff is semantically correct, pin-faithful, and byte-preserving on round-43 outputs.**
Four landed-text findings, none behavioral: F1 LOW (docstring says "floating box" where the pin shows size-only remembering —
a wording regression from the w1 reference), F2 LOW (SKILL.md:225 probe row keeps the round-43-only verdict vocabulary),
F3 INFO (SKILL.md:280 omits the BADSIZE-first precedence), F4 LOW (docstring :16-17 "the round-43 tool printed DIFFER there"
overgeneralizes — proven false for a non-floating maximized client, where round 43 printed TILED). One INFO nuance (F5,
maximized reserved-area). **No OPEN predicate defect found from the tool side.**

## 1. Canonical artifacts and identity chain

- Base bytes `git show 6a1a905…:tools/mado-geometry.py` → sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`
  — matches registration-v2's declared round-43 sha `e3c2e471…`.
- Landed bytes: the tool is unchanged from the data commit to the tip (`git diff --stat e467892 HEAD -- tools/mado-geometry.py`
  empty; `git merge-base --is-ancestor e467892 HEAD` OK) → sha256
  `1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4` — byte-identical to the frozen v2 reference
  `.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt` (same sha256, computed). The landed tool IS the v2 reference.
- Diff size: 84 insertions(+), 12 deletions(-), one file, mode 100755 preserved.
- Pin integrity: computed sha256 of the three `fetch-c1/` files equals `receipts/fetch-sha256.txt:7-9`
  (`7f3585f2…` FullscreenController.hpp, `5bfed3aa…` FullscreenHandler.cpp, `798b7c6c…` HyprCtl.cpp).
- Version attribution: pin commit `efb50993780079460b0cbed1363e2166a2de1d9f` IS tag `v0.56.2` (GitHub API
  `repos/hyprwm/Hyprland/git/ref/tags/v0.56.2` → `object.sha efb5099…`), so the docstring's "Hyprland 0.56.2" is exact.

## 2. Hunk-by-hunk (landed line numbers)

| Landed lines | Change | Contract anchor | Check |
|---|---|---|---|
| :9-17 docstring | new state paragraph | registration-v2 C1 predicate | §3, all sentences pinned (F1, F4 exceptions) |
| :55-56 | fsmode definition | predicate fsmode sentence | code :200-206 verbatim; selftest :471-472 |
| :59-63 | verdict order + TILED D3 narrowing | predicate verdict order; D3 correction | code :236-246 same order; pseudo store pinned (Window.cpp:2402-2408), no pseudo field in dump (0 grep hits in HyprCtl.cpp) |
| :65 | stderr list gains 5 | exit map | empirical: stderr 0 B on rc 0/1/2/3/4/5 |
| :68-70 | summary template + bracketed-pair condition | predicate summary sentence | code :275-281; byte-identity proven §4 |
| :200-206 | `client_fsmode()` | fsmode sentence verbatim | `isinstance(f, int) and not isinstance(f, bool) and f in (1, 2)` |
| :213-215 | tally gains maximized/fullscreen | summary fields | `tally[verdict.lower()]` keys exist for both |
| :235-246 | fsmode read; FULLSCREEN/MAXIMIZED after BADSIZE, before TILED/AGREE | verdict-order sentence | probes §4 |
| :271-272 | NOT_COMPARED rc 5, after DIFFER and NO_MATCHING_CLIENT, before OK | predicate; SKILL.md:286 | probes §4 |
| :275-281 | states pair iff sum>0; `%s` between `badsize=` and `verdict=` | :68-70 sentence | byte-identity proven §4 |
| :437-472 | 21 new selftest checks | clause b | selftest 94/94 rc 0 |

No hunk touches `read_regular`, `parse_args`, `regex_ok`, `parse_rule_text`, `parse_clients`, `client_size`, `matches`,
`run`, or `main` — everything else is byte-identical to base (full diff read; base sha matches registration).

## 3. Docstring sentences vs fetch-c1 pins (locators computed by grep -n)

1. "sets its box to the workspace work area or the monitor box" (tool :9-10) — FullscreenHandler.cpp:191-194
   (`if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {` :191, `const CBox MONBOX = MONITOR->logicalBox();` :192,
   `LAYOUT_TARGET->setPositionGlobal(MONBOX);` :194) and :195-198 (`const CBox WORKAREA = WORKSPACE->m_space->workArea(
   target->floating());` :196, `LAYOUT_TARGET->setPositionGlobal(WORKAREA);` :198; sync twin :236-253). Supported.
2. "remembers the floating box for the way back" (tool :10) — **F1**: the pin shows size-only remembering.
3. "`hyprctl clients -j` carries that internal mode as the integer `fullscreen`" (tool :12-13) — HyprCtl.cpp:410
   `"fullscreen": {},` in the JSON format string; value `sc<uint8_t>(Fullscreen::controller()->getFullscreenModes(w).internal)`
   :431. Supported. (`fullscreenClient` prints `.client` :411/:432; the tool never reads it — matches SKILL.md:281.)
4. "eFullscreenMode: 0 none, 1 maximized, 2 fullscreen" (tool :13-14) — FullscreenController.hpp:12-15
   (`enum eFullscreenMode : int8_t {` :12, `FSMODE_NONE = 0,` :13, `FSMODE_MAXIMIZED,` :14, `FSMODE_FULLSCREEN,` :15). Supported.
5. "the dump shows the state's box, not the rule's" (tool :15) — the dump's `size` is the goal box: HyprCtl.cpp:395
   `"size": [{}, {}]` filled from `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` :427-428, and the state branch sets
   that goal via setPositionGlobal (item 1). Supported (nuance F5 for maximized).
6. "the round-43 tool printed DIFFER there, true about the box and silent about the cause" (tool :16-17) — **F4**: true
   only for a floating state client (base on fs.json → `verdict=DIFFER` rc 1, probes/base-on-states.log); for a non-floating
   maximized client the base tool printed `verdict=TILED` rc 0 (base on max.json, same log). The registration-v2's own
   corrected statement ("could not say that the rule no longer governs it") does not claim DIFFER.
7. fsmode sentence (tool :55-56) — code :200-206 verbatim; bool/float/string/negative/zero/null all → 0 (selftest :471,
   matrix run). Supported.
8. verdict order (tool :59-61) — code :236-246 identical order (BADSIZE :237, FULLSCREEN :239, MAXIMIZED :241, TILED :243,
   AGREE :245, DIFFER :246). Supported.
9. TILED D3 sentence (tool :61-63) — "the dump carries no pseudo field": case-insensitive grep `pseudo` over
   fetch-c1/Hyprland-HyprCtl.cpp → 0 hits; store side pinned in fetch/Hyprland-Window.cpp:2402-2408
   (`m_target->setPseudoSize(*COMPUTED);` :2408) and :2394-2396. The apply site (pseudo size → box) remains unpinned —
   w1/RevRefTool F1, declared residual; the operative claim (TILED = "not floating" only) is fully pinned. Supported.
10. Output/stderr sentence (tool :65) — empirical §4. Supported.
11. Summary template + bracketed-pair sentence (tool :68-70) — code :275-281; "printed exactly when maximized + fullscreen
    > 0" verified (pair present on fs/max/mix and on DIFFER-with-state per selftest :467-468; absent on fsbad/tiled/
    unmatched/norules). Supported.
12. V list + NOT_COMPARED/OK/DIFFER sentences (tool :71-78) — code :265-274 same test order; "NOT_COMPARED says no matched
    client was compared and at least one was skipped for its state" holds when it fires (agree=0 and differ=0 because DIFFER
    precedes); "OK says at least one comparison agreed or … every matched client was TILED or BADSIZE" matches the code
    paths. Supported.

## 4. Empirical matrix (log: seat `probes/matrix.log`)

Fixtures: gkeep.conf (float+size rules), floatonly.conf; clients agree / fs(2) / max(1, non-floating) / tiled / differ /
fsbad(size null, fs 2) / mix(fs2+agree) / unmatched(class other, fs 2) / bad json; runner
`python3 -I <tool> --clients <json> --rules <conf>`, stdout+stderr+rc captured.

| case | base rc | data rc | stderr B | result |
|---|---|---|---|---|
| agree | 0 | 0 | 0 | stdout BYTE-IDENTICAL |
| tiled | 0 | 0 | 0 | BYTE-IDENTICAL, no states pair (clause r holds) |
| differ | 1 | 1 | 0 | BYTE-IDENTICAL |
| unmatched (fs on unmatched client) | 3 | 3 | 0 | BYTE-IDENTICAL, no pair (unmatched state uncounted) |
| norules | 4 | 4 | 0 | BYTE-IDENTICAL |
| fs | 1 (DIFFER) | 5 | 0 | `maximized=0 fullscreen=1 verdict=NOT_COMPARED`; client `verdict=FULLSCREEN` |
| max | 0 (TILED, see F4) | 5 | 0 | `maximized=1 fullscreen=0 verdict=NOT_COMPARED`; client `verdict=MAXIMIZED` |
| fsbad | n/r | 0 | 0 | BADSIZE first: `badsize=1 verdict=OK`, no pair |
| mix (fs + agree) | n/r | 0 | 0 | pair present, `agree=1 … verdict=OK` |
| badjson / usage | n/r | 2 | 0 | stdout exactly `MADO_GEOMETRY: SETUP bad_json` / `MADO_GEOMETRY: SETUP usage` |
| selftest | 73/73 rc 0 | 94/94 rc 0 | 0 | matches `receipts/c1-after-data.txt:1` |
| stdin `-` | n/r | 5 | 0 | same as fs |

Byte-identity: `cmp` of base-vs-data stdout on agree/tiled/differ/unmatched/norules → identical on all five, rc equal,
stderr 0 B everywhere including rc 5 and rc 2. Docstring :69-70 ("prints the round-43 line unchanged") and :65 ("stderr
empty on exit 0/1/3/4/5") hold. Base-on-state runs (probes/base-on-states.log): base on fs.json → `verdict=DIFFER` rc 1;
base on max.json → `verdict=TILED` rc 0 (F4 evidence).

Live read-only run (allowed compositor read): `timeout 5 hyprctl clients -j | python3 -I tools/mado-geometry.py --clients -
--rules ~/.config/hypr/gkeep.conf` → `… clients=3 matched=0 … verdict=NO_MATCHING_CLIENT` rc 3, format byte-compatible with
the SKILL.md:225/:299 quotes (probes/live.log).

## 5. SKILL.md / PROVINCE.md compatibility

- SKILL.md:225 quoted summary and :296-299 example lines: round-43 format, stateless dumps → byte-identical under the
  landed tool (§4). Compatible as quotes.
- SKILL.md:280-282 rows and :284-291 exit-map note: semantics match the code order exactly (NOT_COMPARED "tested after
  NO_MATCHING_CLIENT, before OK" = :269-274; "a dump with any differing client still exits 1" = DIFFER precedence :267-268).
  The rows' pin locators are exact: FullscreenHandler.cpp:191-194 (monitor box), :195-198 (work area), :130-131 (remember),
  Window.cpp:2402-2408 (D3).
- PROVINCE.md:32 Round-44 note: consistent (reads the `fullscreen` integer 1/2, NOT_COMPARED exit 5, still no compositor
  read of its own).
- Lane caller sweep (`MADO_GEOMETRY:` over SKILL.md, PROVINCE.md, quality/, tools/): only the tool itself, the frozen
  counters (own embedded models; clause r re-scored 37/37 per receipt), and the SKILL/PROVINCE quotes — no lane script
  parses the `badsize=<n> … verdict=` adjacency. No round-43 caller breaks.

## 6. Findings by severity

**F1 (LOW, landed docstring overstates its pin; wording regression from the w1 reference)** — attacks
`tools/mado-geometry.py:10`: "…and remembers the floating box for the way back". The cited mechanism remembers the floating
SIZE only: FullscreenHandler.cpp:130-131 `target->rememberFloatingSize(target->position().size());` (the argument is the
size component of the position box); the only other remember site in the pins is fetch/Hyprland-Window.cpp:2578-2579
(`Desktop::floatState()->remember(m_self.lock(), m_realSize->value());` under the log "storing floating size … on close") —
also size-only. No pinned file shows the floating position being remembered; setTargetSizeAndPosition overwrites the
position goal with the state box (:192-194/:196-198) and on FSMODE_NONE "let the layout's recalculate() handle window
pos/size" (:186-187). The w1 reference had the pin-exact wording — `c1/ctl-ref-tool.py.txt:10` "remembers the floating size
for later" — the landed v2 text regressed to "box". Reproduction: `grep -n "remembers the floating" tools/mado-geometry.py
.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` (landed :10 "box" vs w1 ref :10 "size"); `grep -in "remember"
.ufo/waves/round-44/fetch-c1/* .ufo/waves/round-44/fetch/*` (size-only sites). Corrected sentence for the L1 (tool :9-11):
"While a window is maximized or fullscreen the compositor sets its box to the workspace work area or the monitor box and
remembers the floating size for the way back (Hyprland 0.56.2 FullscreenHandler.cpp, setTargetSizeAndPosition and
setTargetFullscreenModeInternal);" — i.e. line 10 reads "…and remembers the floating size for the". The same wording appears
in SKILL.md:280 ("the floating box is remembered") → "the floating size is remembered". Severity LOW: the load-bearing
claim (the dump cannot show the restore geometry) holds for the size either way; no code change; the SKILL/PROVINCE rows
are declared non-scored documentation (registration-v2 Residuals).

**F2 (LOW, SKILL.md probe row 225 keeps the round-43-only verdict vocabulary)** — attacks SKILL.md:225 Answers cell:
"per matched client AGREE / DIFFER / TILED / BADSIZE; `--selftest`". Under the landed tool a matched client can also be
answered FULLSCREEN or MAXIMIZED, and the top verdict NOT_COMPARED rc 5 (tools/mado-geometry.py:59-63, :71-74).
w1/RevRefTool F3 flagged exactly this row class for the data commit; the commit extended the verdict table (:280-282) and
the exit map (:284-289) but left :225. Mitigation: the row ends "per-verdict licence in § 'Rule size versus reported
size'", which now carries the full set. Corrected cell fragment: "per matched client AGREE / DIFFER / TILED / BADSIZE /
FULLSCREEN / MAXIMIZED (round 44); `--selftest`". The row's quoted summary line itself is byte-compatible (§5). LOW.

**F3 (INFO, SKILL.md FULLSCREEN row omits the BADSIZE-first precedence)** — attacks SKILL.md:280 Licenses cell: "the
matched client's `fullscreen` field is 2: Hyprland set its box to the monitor box …". The tool tests BADSIZE first
(tools/mado-geometry.py:59, :236-237; selftest `badsize-before-fullscreen` :456-457): a matched client with `fullscreen: 2`
and no comparable `size` prints `verdict=BADSIZE` and the dump exits OK rc 0 with no states pair (probes/matrix.log
`== data.fsbad rc=0` block). Unreachable from real Hyprland dumps (a fullscreen client's goal size is always printed,
HyprCtl.cpp:427-428), so synthetic-only; the tool docstring documents the order correctly. INFO.

**F4 (LOW, docstring's round-43 attribution overgeneralizes)** — attacks `tools/mado-geometry.py:16-17`: "the round-43 tool
printed DIFFER there, true about the box and silent about the cause." Proven false for a non-floating maximized client:
the base tool on max.json (fsmode 1, floating false) printed `verdict=TILED` rc 0 — TILED, not DIFFER
(probes/base-on-states.log); the floating case is DIFFER rc 1 (fs.json, same log). The landed v2 selftest itself uses a
non-floating maximized client (`maximized-before-tiled`, tool :451-452), so the case is one the landed contract expects.
The registration-v2's corrected statement says only that round 43 "could not say that the rule no longer governs it" — it
does not claim DIFFER. Corrected sentence for the L1 (tool :15-17): "For such a client the dump shows the state's box, not
the rule's, so the tool names the state (FULLSCREEN, MAXIMIZED) instead of comparing; the round-43 tool printed DIFFER for
a floating state client — true about the box, silent about the cause — and TILED for a tiled one." Severity LOW: historical
attribution only; no behavioral impact; no SKILL row repeats the claim.

**F5 (INFO, maximized box nuance)** — attacks the "workspace work area" wording (tool :10, SKILL.md:281). At the layout
target the box IS the work area (FullscreenHandler.cpp:196-198, cited); the dumped window goal for a maximized client is
the work area adjusted by the reserved strip (`EXPECTED_REAL_SIZE = roundedWorkArea.size() - (RESERVED.topLeft +
RESERVED.bottomRight)`, FullscreenHandler.cpp:244-249; the dump prints the window goal, HyprCtl.cpp:427-428). Since the
tool never compares the state box (that is NOT_COMPARED's point), nothing behavioral follows; the cited locator supports
the sentence at target level. INFO, L1's discretion.

**No OPEN predicate defect** found from the tool side: the v2 predicate's new teeth bind surfaces the tool actually has
(b5: every state selftest case flows through `report(json.dumps(...))` → `parse_clients` → `json.loads`, so a renamed key
fails them; e: the state path reads no environment, time, or network), and the K-control variants I independently probed
(fields-always, swapped words, tiled-first, badsize-last, tiled-only-OK) are all excluded by the landed code's actual
behavior.

## 7. Residual risk and verification gaps

- Live maximized/fullscreen geometry remains pinned-source fact, not runtime-scored (registration-v2 Residuals): no state
  window was open on the host during my live run (matched=0), so FULLSCREEN/MAXIMIZED were exercised against fixtures and
  selftest only — the operator act the registration defers.
- The pseudo-size apply site is unpinned (w1/RevRefTool F1, declared residual).
- I verified the tool's behavior independently and read the frozen receipts (c1-after-data.txt: 26/26, selftest 94/94,
  b4 16/16 killed ≥ need 12, b5/e pass, clause r 37/37); I did not audit the counter's code line-by-line (other seats'
  scope).
- The >4300-digit-integer bad_json refusal (w1/RevRefTool F2) is inherited unchanged (`parse_clients` untouched) —
  declared, absurd-input-only.

## 8. Seat evidence and hygiene

- Report: this file. Probes (seat dir `.ufo/waves/round-44/w2/RevToolDiff/probes/`): `matrix.log` (full matrix incl.
  byte-identity verdicts and selftest lines), `live.log` (live read-only run), `base-on-states.log` (base tool on fs/max
  fixtures — F4 evidence).
- Scratch `/fast/scratch/hyaku/mado-r44/RevToolDiff` deleted and verified absent — cite only the seat files above and lane
  files.
- Tooling installs: none (python3/git/cmp only). pacman: untouched. Git: read-only verbs only (show/diff/status/rev-parse/
  log/merge-base). Compositor reads: one `hyprctl clients -j` (allowed list). Writes: this report file and the seat probes
  dir only.

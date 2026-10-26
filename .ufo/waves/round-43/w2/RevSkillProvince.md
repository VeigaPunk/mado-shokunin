# RevSkillProvince — w2 review of the SKILL.md / PROVINCE.md / corpus/README.md additions

Lane `mado-shokunin`, round 43, wave w2, seat `RevSkillProvince`, 2026-10-26.
Target: `git diff a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f 1959770657f1f8665097c1aed4be6c1cbb07139f -- SKILL.md PROVINCE.md corpus/README.md`
(3 files, +57/-0: one PROVINCE tool row, two SKILL table rows + the 44-line section "Rule size versus reported size",
one corpus/README index row + the 9-line Frontier bullet). Role: attack their accuracy against
`tools/mado-geometry.py` (run), the pinned receipts (every locator grep'd), and the entry. Leaf; no files outside
the seat dir and this report were written; no tracked file edited; no tool installed (host `python3` only).

## Result in one line

Every added sentence is supported — all 13 source locators verified at the exact pinned lines, both receipt-backed
host-run blocks reproduce byte-for-byte, the tool's grammar/output/exit map match the prose — with three findings:
one guidance gap in the new SKILL section (the tool it documents can hang), two precision nits (the clients input
cap in PROVINCE.md, the BADSIZE cause list in SKILL.md).

## What was run (all at the lane worktree; `tools/mado-geometry.py` sha256 `e3c2e4715059…8135a99`, byte-identical
to the round-42 reference; the four reviewed files are unchanged between 1959770 and the worktree except a
7-line post-data SKILL addition after line 287, quoted in F1)

- `python3 -I tools/mado-geometry.py --selftest` → `MADO_GEOMETRY_SELFTEST: 73/73 passed`, rc 0.
- Replay of the SKILL probe-row block from the pinned receipts:
  `python3 -I tools/mado-geometry.py --clients .ufo/waves/round-43/fetch/host-clients-r43.json --rules .ufo/waves/round-43/fetch/host-gkeep.conf`
  → the three `MADO_GEOM_RULE/MADO_GEOM_RULE/MADO_GEOMETRY` lines byte-equal to SKILL.md:225 and to
  `receipts/live-geometry-host.txt`, rc 3.
- Cap/edge probes (scratch): 1048577-byte stdin dump → `MADO_GEOMETRY: SETUP too_large`, rc 2; 1048576-byte
  stdin dump → accepted (rc 3); FIFO as `--rules` → `SETUP unreadable` rc 2; directory as `--clients` →
  `SETUP unreadable` rc 2.
- `grep -n 'mkfifo\|O_WRONLY\|O_CREAT' tools/mado-geometry.py` → no match (rc 1), as the PROVINCE row's
  parenthetical claims.
- `python3 -I quality/check-index-rows.py --rev 1959770… --repo .` → `rows=60 errors=0 warns=3`; the three warns
  are pre-existing round-12/round-24 rows (evidence globs), none on the added row.
- `python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch SKILL.md` → `locators=5 miss=0`.
- Backtracking probe (F1): rule `(a|aa)+$` — class `"a"*38+"b"` completes in ~4-5 s at rc 3; class
  `"a"*1000+"b"` killed by `timeout 8` (rc 124), no output byte.
- Locator pinning: `grep -n` / `sed -n` over the seven pinned `Hyprland-*.cpp` receipts (below).
- Receipt reads: `receipts/live-geometry-host.txt`, `fetch/host-gkeep.conf` (sha256 `3726e488…`, float on :2,
  center on :3, size 420 500 :4), `fetch/host-clients-r43.json` (4 objects: Alacritty, zcode, grok-bot,
  chromium; each mapped true, floating false, size 1720x1414; no gkeep), `fetch/gkeep-ui-excerpt.py`
  (`window.set_default_size(420, 500)` at :33, sha `3695b788…`), SOURCES rows S290-S297 (paths and pins as the
  README/entry say), S155/S158 used-by columns now ending with `corpus/knowledge/hyprland-gkeep-geometry-r43.md`,
  `w1/ExecOracleGkeep/20-observation.txt` (`"size": [420, 500]`, `"floating": true`).

## Verified claims (the added sentences, block by block)

- **SKILL.md:158 (decision row)** — "hyprctl live (`clients`, which prints the animation goal box)":
  supported by `Hyprland-HyprCtl.cpp:427-428` (JSON) and `:448` (plain), both `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)`,
  and `Hyprland-GeometricMovableAnimated.cpp:19-20` (GOAL=`m_realSize->goal()`, CURRENT=`m_realSize->value()`).
  `[OBS]/[UNK]` split matches entry §3 INF and "What this entry does not establish".
- **SKILL.md:225 (probe row)** — the cited host-run summary, rc 3, and the `n=2 … arg=420x500` line are
  byte-equal to `receipts/live-geometry-host.txt` (2026-10-26T04:17:54-03:00) and reproduce from the pinned
  receipts; "no gkeep window open" matches S296 (no `org.omarchy.gkeep` object; four clients, none floating).
- **SKILL.md:246-287 (section)** — grammar sentence matches the tool's docstring/RULE_LINE/MATCH_FIELD/SAFE
  exactly (`windowrule[ \t]*=`, size = two `[0-9]{1,5}`, float = `on|off`, one `match:class` field, the SAFE
  alphabet); "starts no process, opens no socket and reads no config tree of its own" matches the imports
  (json/os/re/stat/sys) and `read_regular`/`parse_clients`; output-order sentence matches `report()`.
  All 13 locator references pinned at the exact lines: HyprCtl.cpp :395 (`"size": [{}, {}]`), :2007
  (`registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});`), :427-428, :448;
  GeometricMovableAnimated.cpp :19-20; DefaultFloatingAlgorithm.cpp :49 (`if (target->window() &&
  target->window()->m_firstMap)`), :55 (`if (WINDOW->m_ruleApplicator->static_.size) {`), :56
  (`…calculateExpression(*…static_.size)`); WindowRuleApplicator.cpp :422 (`std::get<Math::SExpressionVec2>(value)`),
  :426 (`static_.size = expr;`); RegexMatchEngine.cpp :16 (`re2::RE2::FullMatch`), :7-8 (`negative:` prefix,
  inversion). Verdict table semantics match `evaluate()`: BADSIZE (size none), TILED (not floating), AGREE,
  DIFFER; `matches()` uses `re.fullmatch` and rejects control-char classes, mirroring RE2::FullMatch anchoring.
  Exit map 0/1/2/3/4 matches `report()` (NO_SIZE_RULES 4 tested first, then DIFFER 1, NO_MATCHING_CLIENT 3,
  OK 0) and `main()`'s SETUP rc 2 with exactly the reasons usage|unreadable|too_large|bad_json. Host-run block
  = live receipt. Closing paragraph matches entry §3 INF/§5 UNK.
- **PROVINCE.md:32 (tool row)** — caps and setup errors verified by run (above; each `--rules` file and a
  regular `--clients` file share the 1048576 cap in `read_regular`; stdin is read at most 1048577 B — see F2);
  FIFO/directory/missing → `unreadable` verified for FIFO and directory by run, missing/unreadable is the
  `os.open` OSError path; "UTF-8 JSON holding a list of objects" = `parse_clients`; "no process/socket/network/
  config tree" = imports + code; output lines and selftest behaviour verified (73/73, no file I/O in the
  selftest path); provenance "mado, round 43" correct.
- **corpus/README.md index row (MADO-R43-1)** — host rule text = S295; anchored `re2::RE2::FullMatch` = S290:16;
  "size effect stored as an expression and evaluated only in the floating algorithm's first-map branch" =
  S155:422,426 + S291:55-56 (in the seven pinned files `static_.size` is read nowhere else); target/window box
  store = S292/S293; GOAL-not-current = S294/S158; `set_default_size(420, 500)` = S297:33; "isolated-oracle
  observation of 420x500 floating" = entry §4 citing `w1/ExecOracleGkeep/20-observation.txt` (checked: contains
  `"size": [420, 500]`, `"floating": true`); "today's census (4 clients, none floating, no gkeep window)" =
  S296 + my re-parse; row column "S290…S297, S155, S158" all present, with the used-by item appended to both
  held rows.
- **corpus/README.md Frontier bullet** — "rows S290-S297 plus held S155/S158" ✓; "The reported `size` is the
  animation's goal, not the value on screen, and a tiled client never reads the rule" ✓ (S294:19-20, S291:49;
  entry §2 INF); "Still open" list matches entry §5 UNK and "does not establish".

## Findings by severity

### F1 — MEDIUM (doc guidance gap, already patched post-data): the new SKILL section documents a tool that can hang, without a timeout guard, at the data commit

`SKILL.md:158`, `:225` and `:246-287` (data commit) recommend
`hyprctl clients -j | python3 tools/mado-geometry.py --clients - --rules <file>` and license per-verdict
readings, but say nothing about termination. The tool match-paths with Python `re.fullmatch` (tool:180-184),
which backtracks; Hyprland matches with linear-time RE2 (`Hyprland-RegexMatchEngine.cpp:16`). A rule regex such
as `(a|aa)+$` passes the tool's own SAFE gate, and the client chooses the class string. Measured at the
data-commit tool bytes (sha `e3c2e471…`): class `"a"*38+"b"` → ~4-5 s before the verdict; class `"a"*1000+"b"`
→ killed at `timeout 8`, rc 124, and because the tool buffers all output and writes once (tool:261) a consumer
sees zero bytes — indistinguishable from a dead pipe. Same finding as `w1/RevRefTool.md` V1 (4.573 s at n=38,
1.1 KB killed); shown to still hold at 1959770 by the runs above. The data-commit SKILL has no
timeout/backtrack guidance for this tool (the four pre-existing `timeout` mentions at :157/:230/:907/:1102 are
globals/regression text). The hang risk is a client-chosen class, i.e. exactly the live-host usage the section
teaches.

Fix text — already present as the 7-line post-data worktree addition after SKILL.md:287. Its substance, two
located fragments (worktree SKILL.md:290 and :295): "Known limit (round-43 wave w1, `RevRefTool` V1): the match
is Python `re.fullmatch`, which backtracks." and "treat exit 124 as "no verdict", never as a verdict", with the
guarded pipeline `hyprctl clients -j | timeout 5 python3 tools/mado-geometry.py …`. I verified its two numbers
against fresh runs (~4.6 s at n=38 ✓; ~1 KB never finishes ✓). Recommend the L1 keep that paragraph at
integration, and consider mirroring the `timeout 5` guard into the two table rows (:158, :225) where the
unguarded pipeline is printed as the command to run. Note this is a defect of the landed SKILL addition, not of
`PRED-C2-r43-v2`: the predicate scores the entry, not the SKILL section.

### F2 — MINOR: PROVINCE.md:32 states the clients-input cap as "at most 1048577 B"; the accepted cap is 1048576 B

The row reads: "`--clients`, a regular file or `-` for standard input, at most 1048577 B". The tool's docstring
(tools/mado-geometry.py:21-22) says an input larger than 1048576 bytes is `too_large`, and stdin is merely *read*
at most 1048577 bytes (`run()`: `stdin.read(MAX_BYTES + 1)` then `if len(data) > MAX_BYTES: raise Setup("too_large")`,
tool:254-256). Measured: a 1048577-byte stdin dump → `MADO_GEOMETRY: SETUP too_large`, rc 2; a 1048576-byte
stdin dump → accepted. A regular-file `--clients` goes through the same `read_regular` cap (1048576). As landed,
the inventory row states a contract one byte looser than the tool implements.

Fix text (PROVINCE.md:32): replace "at most 1048577 B" with "at most 1048576 B (stdin is read in one
1048577-byte read; anything larger is `too_large`)". No counter or receipt depends on the phrase.

### F3 — MINOR: SKILL.md:271 BADSIZE cause list omits the non-negative requirement

The row: "BADSIZE | only that there was no size to compare (no `size` value, or not two integers)". The tool
also rejects a size of two integers when either is negative (`client_size`: `… and v >= 0 …`, tool:172-175), and
its selftest pins it (`negative-size-badsize`, tool:294-295). A dump `"size": [-1, 500]` is two integers yet
BADSIZE. The licence sentence ("only that there was no size to compare") stays true; the parenthetical cause
list is incomplete. Quote verification: `python3 -I .ufo/waves/round-43/w2/RevSkillProvince/verify-quotes.py`
→ `QUOTES: 30/30 checks passed`, rc 0 (every quoted fragment in this report re-found at its named source line;
the script is in this seat dir).

Fix text (SKILL.md:271): "(no `size` value, or not two non-negative integers)".

## Locator-checker coverage note (residual, not a doc defect)

`quality/check-locators.py` passes (5 locators, 0 miss), but by its own rules (docstring "Attribution"/"NOFRAG")
it does not reach: the bare continuation locators `:2007`, `:427-428`, `:448`, `:7-8` and the `:49` half of
`:49,55-56` (no file name → LOCATOR_RE does not match), and `Hyprland-GeometricMovableAnimated.cpp:19-20`
(reported `NOFRAG` because its fragments sit on the previous prose line). All of those were verified manually
here by `grep -n`/`sed -n` against the pinned receipts and are correct. Any future edit of this section should
not read `CHECK_LOCATORS: locators=5 miss=0` as full coverage.

## Residual risk and verification gaps

- I did not re-run the live host `hyprctl clients -j` (the pinned receipt plus the receipt-replay above carry
  the claim; the live window set may have changed since 04:17, which would not affect any added sentence).
- The FIFO/missing-unreadable paths of `read_regular` were verified for FIFO and directory by run;
  missing-path is the same `OSError → Setup("unreadable")` branch, verified by code read only.
- "evaluated only in the floating algorithm's first-map branch" (README row) is scoped to the seven pinned
  source files; Hyprland files outside the pin set were not fetched (the entry's recheck clause and the C2
  residual "the pins are the trust root" already declare this).
- The post-data 7-line SKILL paragraph is worktree state, not data-commit state; whether the L1 integrates it
  is outside this seat.

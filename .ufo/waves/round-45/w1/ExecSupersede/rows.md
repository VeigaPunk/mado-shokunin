# ExecSupersede — round 45 w1: the census-clean supersession of the S290-S297 cells

Seat `ExecSupersede`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base/freeze
`22a8dedd02f507689c567777e0f20b5e645c8ce0` (parent `0c89478a`, round-44 tip `8ac15c41`).
Target: round-43 closure **D2** (`corpus/lessons/round-43-verifier-spotcheck.md:100-101` — "S293 title 'the client's
request as input' reads as the refuted premise; supersede with the other w2-found row-cell defects (S290-S294, S296,
S297) under CORPUS rule 2") and round-44 **D6** (`corpus/lessons/round-44-verifier-spotcheck.md` §6 item 6 — "still
open from round 43: D2 … deferred to round 45 per SCORECARD plan item 2").

Contract applied: `CORPUS.md:116-118` (rule 2) — "Only `status`, `recheck` and `used-by` change in place … A correction
is a new row whose `teaches` opens `supersedes S0NN —`." Census mechanics: `scripts/sources-census.sh` (`:644-649`
W04/E04, `:560-570` E11).

**Ids.** `S311`-`S317`, seven successors in predecessor order. `S302`-`S310` are taken by this round's own C2 pin rows
(`registration.md` § C2: "new rows S302-S310 (registry tops at S301, 238 rows)", built by `.ufo/waves/round-45/l1-draft/build-pos.py:31-66`);
the live registry tops at `S301` (`corpus/SOURCES.md`, 238 rows — `scripts/sources-census.sh census`), and none of
`S311`-`S317` occurs anywhere in the lane today (checked against the registry rows, §3).

Deliverables: `rows-block.txt` (paste-ready rows, sha256 `baaf5b55…a69f`), this file, `check-quotes.sh` + `quotes.txt`,
`mirror.sh` + `census-{lane,m0,m1,m2,m3,m4}.txt`.

## 1. Inputs read

| what | where |
|---|---|
| closure D2 and its exact wording | `corpus/lessons/round-43-verifier-spotcheck.md:100-101` |
| round-44 deferral (D6) | `corpus/lessons/round-44-verifier-spotcheck.md` §6 item 6 |
| registry rows under attack | `corpus/SOURCES.md:239-246` (S290-S297, 11 cells each, `awk -F'\''|'\''` NF=13) |
| the round-43 w2 re-opens that produced the defects | `.ufo/waves/round-43/w2/ScoutRowsA/rows.md:18,36` (S290, S291), `ScoutRowsB/rows.md:23,49,59` (S292, S293), `ScoutRowsC/rows.md:59` (S294), `ScoutRowsD.md` (one line: `status: started` — **no** S296/S297 finding) |
| the prior attempt at this same task | `.ufo/waves/round-44/w1/ScrSupersedeRows.md`, `…/ScrSupersedeRows/rows.md` (7 rows drafted as S302-S308, never landed) |
| pins the rows cite | `.ufo/waves/round-43/fetch/` (five upstream + three own-work) |
| round-45 registration (row budget, routed D6) | `.ufo/waves/round-45/registration.md` § C2, § "Not claims" |
| CORPUS contract | `CORPUS.md:88-150` (§ Shape), `:116-118` (rule 2) |

## 2. Defect → correction, row by row

| new | supersedes | defect (evidence) | corrected in the new row |
|---|---|---|---|
| S311 | S290 | `teaches` mixes sources: quotes the host pattern text, which is S295 (`host-gkeep.conf:2-4`), and the class→engine binding is `Rule.cpp:52,:98` + `WindowRule.cpp:395-396`, pinned nowhere (`ScoutRowsA/rows.md:18,20`) | `teaches` states only what the file shows (FullMatch over the whole string, `negative:` inverts) and names the host text as S295; `anchor` carries the cross-reference with its own commit; `scope` verbatim |
| S312 | S291 | title says "who consumes a size rule" while the tiled path consumes the same expression (`Window.cpp:2402-2410`); `teaches` drops the parse gate, the conditional centre and the downstream clamp (`ScoutRowsA/rows.md:36,40`) | title narrowed to the floating path; `teaches` adds the parse gate `:57-58`, the two centre conditions `:79-84`/`:90-91`, and names the clamp as S293; `anchor` adds the tiled consumer with its hash; `scope` verbatim |
| S313 | S292 | `teaches` ends "so the geometry a window reports is a value the layout wrote" — a three-row inference the file does not show (`ScoutRowsB/rows.md:23`) | `teaches` replaced by the file's own four facts (round both parts `:10-14`, `position()` returns the logical part `:64-66`, separate floating-size member `:68-74`, `recalc` `:76-78`) plus the absence of an in-file caller (sweep below); `scope` verbatim |
| S314 | S293 | title echoes the refuted request premise; `teaches` omits the `||` on the ≤2 px gate, the `>5` surface gate, the 600x400/error returns and the stored-size override (`ScoutRowsB/rows.md:49,59`; closure D2 names this row) | title rewritten ("desired geometry, its fallbacks, and the floating hand-off"); `teaches` grounded at `:310-313,:323-326,:339,:342-348,:350-362,:364` and the hand-off at `:70-71`; `anchor` extended with `:323-326,:339-365`; `scope` verbatim |
| S315 | S294 | `teaches` tail "can differ from what is on screen" is an inference not in the file (`ScoutRowsC/rows.md:59`) | inference dropped; `teaches` states the two stored values `:19`/`:20`, `geometricBox` `:26-33`, and that the file says nothing about drawing or animation completion; `scope` verbatim |
| S316 | S296 | no w2 finding existed (`ScoutRowsD.md` = `status: started`); this seat's re-open: the pin is reduced to 7 fields so no `fullscreen` value exists (`grep -c fullscreen` = 0, `grep -c gkeep` = 0), and "never mapped" is not a snapshot claim | `scope` narrowed to the fields actually kept; `teaches` reports the field list and the sweep, and reads absence as absence at one moment; `anchor` records the reduced field set |
| S317 | S297 | same gap; re-open: the excerpt carries a two-line provenance header, so the row's `:6`/`:33` are excerpt-relative (`ui.py:449`/`:476`), and `set_default_size` is a default, not a request (`grep -c size_request` = 0) | title "declaration" not "request"; `anchor` maps excerpt→`ui.py` and carries the no-size-request sweep plus the full-file hash; `teaches` separates the declared default from a request |

S296/S297 are in closure D2's list but round-43 w2 left no finding for either; their two successors are this seat's own
re-open, offered as grounded rather than inherited. If the L1 wants D2 answered strictly, S311-S315 alone do it.

## 3. The seven rows

`rows-block.txt`: 7 rows × 11 cells, every row `|`-count 12 (registering 11 cells — asserted by `insert_rows` in
`mirror.sh`), status `mined`, `opened 2026-10-26`. Measured cell diff against the predecessor (`cell-diff.txt`, re-runnable):

| new | source (title) | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S311 | changed | kept | kept | kept | **kept verbatim** | extended (cross-ref) | rewritten | mined | 2026-10-26 | on-release | corpus/lessons/round-45.md |
| S312 | changed | narrowed to the floating path | kept | kept | **kept verbatim** | extended (tiled consumer + hash) | rewritten | mined | 2026-10-26 | on-release | corpus/lessons/round-45.md |
| S313 | changed | kept | kept | kept | **kept verbatim** | kept | rewritten | mined | 2026-10-26 | on-release | corpus/lessons/round-45.md |
| S314 | changed | rewritten (premise removed) | kept | kept | **kept verbatim** | extended (`:323-326,:339-365`) | rewritten | mined | 2026-10-26 | on-release | corpus/lessons/round-45.md |
| S315 | changed | kept | kept | kept | **kept verbatim** | kept | rewritten | mined | 2026-10-26 | on-release | corpus/lessons/round-45.md |
| S316 | changed | kept | own-work | kept | narrowed (fields kept) | extended (field list, sweep) | rewritten | mined | 2026-10-26 | 2027-01-24 | corpus/lessons/round-45.md |
| S317 | changed | renamed (declaration) | own-work | kept | narrowed (id + default size) | rewritten (excerpt→`ui.py`) | rewritten | mined | 2026-10-26 | 2027-01-24 | corpus/lessons/round-45.md |

Why the five URL-bearing rows keep their `scope` cell verbatim: E04 fires only when URL **and** scope repeat and the
`teaches` lacks `supersedes S[0-9]{3}` (`scripts/sources-census.sh:646-649`); keeping the scope costs **no** W04, while
changing it moves the row into the across-scopes branch and prints one (`:644-645`). The two own-work rows carry no URL
(`url_of()` reads lane paths, `:600-605`), so their scope can be narrowed for free.

`used-by` is `corpus/lessons/round-45.md` for all seven: CORPUS rule 2 requires the old→new log there, and the round-45
lesson is exactly that document (the same shape round-13 used for its supersession, `corpus/lessons/round-13.md:36,39,50`).

## 4. Gate lines each new row needs

Fetched and opened 2026-10-26 by this seat; every quote grepped literally in its receipt by `check-quotes.sh`
(`quotes.txt`: `QUOTES: checked=7 failed=0`). Paste into the round-45 lesson `## Gate` (shape as round-43's:
`GATE <id> receipt=… sha256=… quote="…"` plus the URL and the access date):

| id | receipt (URL / path) | accessed | quote (≤25 words) | location | words | sha256 of the receipt |
|---|---|---|---|---|---|---|
| S311 | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/desktop/rule/matchEngine/RegexMatchEngine.cpp` → `.ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp` | 2026-10-26 | `if (regex.starts_with("negative:")) {` | `:7` | 3 | `8ca65533…a3a282` (470 B) |
| S312 | `…/src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` → `…/Hyprland-DefaultFloatingAlgorithm.cpp` | 2026-10-26 | `if (WINDOW->m_ruleApplicator->static_.center.value_or(false)) {` | `:79` | 3 | `f05f2561…632e91` (10359 B) |
| S313 | `…/src/layout/target/Target.cpp` → `…/Hyprland-Target.cpp` | 2026-10-26 | `void ITarget::rememberFloatingSize(const Vector2D& size) {` | `:68` | 5 | `49323833…d4ca06` (3064 B) |
| S314 | `…/src/layout/target/WindowTarget.cpp` → `…/Hyprland-WindowTarget.cpp` | 2026-10-26 | `if (DESIRED_GEOM.width <= 2 \|\| DESIRED_GEOM.height <= 2) {` | `:339` | 9 | `8bcaf370…4734d` (16614 B) |
| S315 | `…/src/desktop/view/types/GeometricMovableAnimated.cpp` → `…/Hyprland-GeometricMovableAnimated.cpp` | 2026-10-26 | `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` | `:19` | 4 | `649f1a8d…a1a207d` (1576 B) |
| S316 | own-work `.ufo/waves/round-43/fetch/host-clients-r43.json` (no URL) | 2026-10-26 | `"class": "Alacritty",` | `:5` | 2 | `21db902e…fb442ad` (711 B) |
| S317 | own-work `.ufo/waves/round-43/fetch/gkeep-ui-excerpt.py` (no URL) | 2026-10-26 | `window.set_default_size(420, 500)` | excerpt `:33` = `ui.py:476` | 2 | `3695b788…d9c5d1713` (1625 B) |

Negative claims carry their sweeps (same script, `quotes.txt`): S316 `grep -c fullscreen` = **0** and `grep -c gkeep` = **0**
on its receipt; S317 `grep -c size_request` = **0**; S313 `grep -n 'position()\|rememberFloatingSize'` on `Target.cpp`
returns only the two definitions (`:64`, `:68`) — no in-file caller. The excerpt body is byte-equal to
`ui.py:446-488` (`cmp` against the round-44 pin `.ufo/waves/round-44/fetch/gkeep-ui.py`, full-file
`07a3c4a5…e5d66a`).

Same-day pin re-open: all five upstream files were re-fetched in this seat's scratch and their sha256/byte counts equal
both the row cells and the round-43 receipts (`quotes.txt` tail); the cross-reference files were fetched at the same
commit and hashed: `Window.cpp` `d735d454…11ded` (124226 B, = the round-44 pin), `Rule.cpp` `257687ef…c098e2e` (6835 B),
`WindowRule.cpp` `7034c332…16d1f78` (19588 B). Locators recomputed, never typed: `Rule.cpp:52` carries
`{RULE_PROP_CLASS, RULE_MATCH_ENGINE_REGEX}`, `:98` the `makeUnique<CRegexMatchEngine>(s)` case, `WindowRule.cpp:396`
`engine->match(w->m_class)`, `Window.cpp:2403` the tiled `calculateExpression`.

## 5. Census proof (mirror copies; the lane is never written)

`mirror.sh`: copies the lane's `corpus/` to `/fast/scratch/hyaku/mado-r45/ExecSupersede/<variant>/`, inserts the seven
rows after the last `| S### |` line, copies every `used-by` path the registry names (so E11 resolves exactly as in the
lane), then runs `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-10-26`.

| variant | what it is | E | W | exit |
|---|---|---|---|---|
| lane | the lane's real `corpus/SOURCES.md` (`--file`, read-only) | 0 | 8 | 0 |
| m0 | mirror, **no** new rows (control: reproduces the lane) | 0 | 8 | 0 |
| m1 | rows, no `corpus/lessons/round-45.md` | **7** (E11 ×7) | 8 | **1** |
| **m2** | **rows + a round-45 lesson naming the ids = the landing shape** | **0** | **8** | **0** |
| m3 | joint: the round's own C2 rows S302-S310 (`build-pos.py` on a clone at the freeze) **plus** S311-S317 | 0 | 10 | 0 |
| m4 | m2 mutant: S315's `supersedes S294 —` opener deleted | **1** (E04 S315) | 8 | 1 |

m0 versus the lane: `diff` of the two outputs shows only the `ok` path line, so the control carries no finding of its own.

`census-m2.txt` (the required run, byte-for-byte):

```
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
file	ok	/fast/scratch/hyaku/mado-r45/ExecSupersede/m2/corpus/SOURCES.md
```

`census-m3.txt` (joint with the round's own pin rows; the only two additions over m2 are C2's own duplicate URLs):

```
file	W04	S303 duplicate url …/src/config/legacy/ConfigManager.cpp across scopes
file	W04	S307 duplicate url …/src/debug/HyprCtl.cpp across scopes
file	ok	/fast/scratch/hyaku/mado-r45/ExecSupersede/m3.uCPTiy/corpus/SOURCES.md
```

(`census --file` on the m3 mirror: `file rows 254`, `FLEET rows 254` = 238 + 9 C2 + 7 mine.)

`census-m1.txt` and `census-m4.txt`, the two red states that make the proof load-bearing:

```
file	E11	S311 missing used-by corpus/lessons/round-45.md   (… S312-S317, seven lines)
file	E04	S315 duplicate url …/src/desktop/view/types/GeometricMovableAnimated.cpp within scope The animated box API that answers `GEOMETRIC_GOAL` and `GEOMETRIC_CURRENT`
```

Readings:

1. **Supersession costs nothing** — m2 adds zero findings over m0. No W04 arises from the five repeated URLs because their
   `scope` cells are verbatim (same scope key), and the `supersedes S29N —` opener exempts them from E04.
2. **The rows cannot land alone** — m1's seven E11 lines show `used-by` must resolve at the same commit; the round-45
   lesson (already written by this round's C2 path, `build-pos.py:91-93`) is that document.
3. **The opener is load-bearing, not decoration** — m4 deletes exactly one opener and E04 fires on that row.
4. **The two claims do not collide** — m3 lands C2's S302-S310 and these seven together at exit 0; the only new warnings
   are C2's own (S303, S307), which `registration.md` § C2 already declares as W04-not-error.

## 6. Integration steps for the L1

1. Append `rows-block.txt` after `corpus/SOURCES.md:250` (the S301 row is the registry's last; `build-pos.py` inserts its
   own rows at the same point). Do not touch S290-S297.
2. Land the round-45 lesson **naming all seven ids** in the same commit with the `## Registry changes logged old→new`
   table (CORPUS rule 2) and the seven `GATE` lines of §4. Without it: E11 ×7.
3. Hold the census at the m2/m3 shape: `W04 ×7 + W01 S277` (`+2` for C2's own rows), `ok`, exit 0.
4. Do **not** re-point the round-43 knowledge entry at S311-S317 unless the entry's own text is re-issued: it cites
   S290-S297, and the supersession is a registry-level correction of wording, not a change of the facts the entry uses.

## 7. Findings

1. **Supports closure D2 on its named case.** S293's title is the refuted premise and its `teaches` omits four source
   conditions; S314 corrects both, with every locator recomputed (§2, §4).
2. **Attacks D2's list.** It names S296 and S297, but round-43 w2 left no finding for either (`ScoutRowsD.md` is one line,
   `status: started`). The S316/S317 defects are this seat's re-open, grounded in the pins (§2), not inherited.
3. **Measured: a superseding row of a URL-bearing row adds no census finding** when the scope cell is kept verbatim
   (m2 vs m0); the exemption lives in the `teaches` opener (m4 proves it), not in the scope.
4. **The round-45 C2 rows and these rows coexist cleanly** (m3, exit 0, 254 rows) — no id collision, no shared URL between
   the two sets (`S302-S310` are monitor-plane pins; mine repeat the round-43 geometry pins).
5. **Two cell-level corrections the closure did not list, grounded today:** S290's `teaches` quoted a second source's text
   (S295) as if it were this file's, and S293's anchor did not reach `:323-326`/`:339-365`, the lines four of its missing
   conditions live on. Both are in the successor rows, not in the old ones.

## 8. Limits (declared, not fixed)

- The census ran on **mirror copies**, never on a lane commit: this seat may not edit `corpus/SOURCES.md`. A live run at
  the data commit is the L1's step (§6.3) and has not happened.
- The m2 lesson is a **stub** naming the ids to prove E11 resolves; the wording of the real lesson is the L1's.
- `used-by` = `corpus/lessons/round-45.md` is a forward reference: the row is `mined` only once that lesson exists. m1 is
  the red state that shows what happens before it does.
- No claim-counter was executed (`quality/counters/c2-r45-monitor-entry.py` iterates only the ids the monitor entry cites,
  which are S302-S310): [INFERENCE] none of these seven rows can move it while uncited; this is a reading of the counter's
  clause set, not a run.
- The old rows' `status` is deliberately unchanged: nothing here refutes S290-S297, only their wording.
- `localhost` host state was not queried at all in this seat: no `hyprctl`, no compositor connection — the own-work pins
  were read from the committed receipts, which is what the rows cite.

## 9. Receipts in this seat directory

- `rows-block.txt` — the seven rows (sha256 `baaf5b55…a69f`), 11 cells each.
- `cell-diff.txt` — the per-row cell diff against its predecessor (`cells=11` and id-uniqueness asserted).
- `check-quotes.sh`, `quotes.txt` — the quote/locator verifier, `QUOTES: checked=7 failed=0`, plus the same-day pin hashes
  and the negative sweeps.
- `mirror.sh`, `census-lane.txt`, `census-m0..m4.txt` — the census driver and its six runs.
- Scratch `/fast/scratch/hyaku/mado-r45/ExecSupersede/` (fetches, mirrors, clone) deleted before this seat finished; no
  `/tmp` or scratch path is cited as evidence above.
- Tools installed: none. Package operations: none.

# w2 ExecLocatorSweep — every round-44 prose locator recomputed at the data commit

**Verdict: 3 landed locator defects (2 in the entry, 1 bare pointer in the README row) and 23 false MISSes from
`quality/check-locators.py`'s same-line attribution.** All 28 MISSes were opened against their receipt and re-located with
`grep -n`; the 23 that the checker reports on correct prose are an **OPEN predicate defect** of criterion 77's tool, not
content errors. The w1 candidate `.ufo/waves/round-44/w1/ExecLocatorTeeth/check-locators.py` is **byte-identical** to the
lane checker on this round's prose (both fetch dirs, all six files, verdict lines and summary), so it finds no numeric
locator defect either.

Target: lane `/home/vgpnk/Projects/shokunin/mado-shokunin` at data commit
`e46789213830597348fe96a351ae004d10587385` (base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`). Lane HEAD at read time was
`290cddea92a18e2202456db89cb2bb60d9aaacff` (after-data commit); the prose was read from `e4678921` only, never from the
worktree.

## 1. Commands, counts, exit codes

Both checkers, both pin directories, the six commanded files, prose extracted with `git show e4678921:<path>` into
`prose/` (receipt `extract.txt`, sha256 per file there):

```
$ python3 -I quality/check-locators.py --fetch .ufo/waves/round-44/fetch \
    corpus/knowledge/hyprland-gkeep-size-request-r44.md corpus/lessons/round-44.md SKILL.md \
    corpus/README.md LOG.md corpus/QUALITY.md
CHECK_LOCATORS: locators=52 miss=21                     # rc=1   -> run-fetch.txt
$ python3 -I quality/check-locators.py --fetch .ufo/waves/round-44/fetch-c1 <same six files>
CHECK_LOCATORS: locators=10 miss=7                      # rc=1   -> run-fetch-c1.txt
$ python3 -I .ufo/waves/round-44/w1/ExecLocatorTeeth/check-locators.py --fetch <both dirs> <same six files>
CHECK_LOCATORS: locators=52 miss=21 · locators=10 miss=7 # rc=1   -> cand-fetch.txt, cand-fetch-c1.txt
```

`--explain` for every locator (both dirs, all six files) is `explain-both.txt` (62 `LOC` and 394 `SKIP` lines across the
two runs, plus `ATTR`/`FRAG`).
Checker sha256 (`checker-sha256.txt`): lane `c1ea52ad5db21fdf81022d0425e7cad42fc3e34dd5083915b127a46ab948a27e`, candidate
`66e048338cfcc10adce824f3d32f75735c9e683e131af70dd684d71d5c7643a9`.

| prose file | fetch: loc/OK/NOFRAG/MISS | fetch-c1: loc/OK/NOFRAG/MISS |
|---|---|---|
| `corpus/knowledge/hyprland-gkeep-size-request-r44.md` (entry) | 29 / 4 / 17 / 8 | 0 (names not pinned there) |
| `corpus/lessons/round-44.md` | 8 / 1 / 2 / 5 | 2 / 1 / 0 / 1 |
| `SKILL.md` | 1 / 0 / 1 / 0 | 4 / 1 / 0 / 3 |
| `corpus/README.md` | 14 / 4 / 2 / 8 | 0 |
| `LOG.md` | 0 | 2 / 1 / 0 / 1 |
| `corpus/QUALITY.md` | 0 | 2 / 0 / 0 / 2 |
| **total** | **52 / 9 / 22 / 21** | **10 / 3 / 0 / 7** |

The two runs are complementary, not duplicates: `fetch/` pins `Hyprland-Window.cpp`, `Hyprland-XDGShell.cpp`,
`xdg-shell.xml`, `gdktoplevel-wayland.c`, `gkeep-ui.py`; `fetch-c1/` pins `Hyprland-FullscreenHandler.cpp`,
`Hyprland-HyprCtl.cpp`, `Hyprland-FullscreenController.hpp`. Their union resolves every locator the round wrote except
names pinned in neither (declared limit, §6).

**Which lines round 44 actually wrote** (`git diff -U0 6a1a9052 e4678921 -- <file>`, in `extract.txt`): entry `+1,81`
(whole file); lesson `+1,266` (whole file); `SKILL.md +280,3 +286,6`; `corpus/README.md +72 +303,18`;
`LOG.md +2496,8`; `corpus/QUALITY.md +410,6`. That is why rows 280-291 are the SKILL check and why the QUALITY/LOG MISSes
below are legacy text.

### Candidate equivalence (measured, not relayed)

- plain runs: `diff` **0 bytes** for `fetch` and **0 bytes** for `fetch-c1` (`run-fetch.txt` vs `cand-fetch.txt`,
  `run-fetch-c1.txt` vs `cand-fetch-c1.txt`).
- `--explain` with `FRAG` lines removed (verdicts, `ATTR`, `SKIP`, summary): `explain-old-{fetch,c1}.txt` vs
  `explain-new-{fetch,c1}.txt` → **0 bytes** both. Only `FRAG` token lists differ (the candidate adds numeric atoms).
- Consequence: no numeric-only locator defect exists in these six files, and the candidate changes no landed verdict here.

## 2. Every MISS, opened: the true line, by `grep -n`

`★` = real defect. `~` = checker attribution artifact on correct prose. `L` = legacy text, not round-44-written.
`S` = criterion-77 self-reference. Full `grep -n` transcripts: `greps-fetch.txt`, `greps-fetch-c1.txt`.

| # | prose locator (as landed) | attributed fragment | true line (grep -n) | class |
|---|---|---|---|---|
| 1 | `…size-request-r44.md:36` `Hyprland-XDGShell.cpp:354-358` | the `sendConfigure` quote (belongs to `:455`) | `354:uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {` … `357: return m_owner->scheduleConfigure();` — range exact | ~ sibling |
| 2 | `…r44.md:44` `xdg-shell.xml:1150` | its own quote, which wraps | `1150:The width and height arguments specify a hint to the window` / `1151:about how its surface should be resized in window geometry` — **`resized` is on 1151, outside the range** | ★ narrow range |
| 3 | `…r44.md:44` `xdg-shell.xml:1154-1157` | the `:1150` quote | `1154:If the width or height arguments are zero, it means the client` / `1155:should decide its own window dimension…` — correct | ~ sibling |
| 4 | `…r44.md:44` `xdg-shell.xml:1159-1161` | the `:1150` quote | `1159:The states listed in the event specify how the width/height` … `1161:drawn.` — correct | ~ sibling |
| 5 | `…r44.md:44` `xdg-shell.xml:560` | the `:1150` quote | `560:    <request name="ack_configure">` — correct | ~ sibling |
| 6 | `…r44.md:48` `gdktoplevel-wayland.c:633-637` | the `configured_width` quote (belongs to `:681`) | `633:fixed_size =` … `637:is_resizing;` — range exact (maximized/fullscreen/tiled or resizing) | ~ sibling |
| 7 | `…r44.md:56` `gkeep-ui.py:475` | its own quote, which spans two lines | `475:window.set_decorated(False)` / `476:window.set_default_size(420, 500)` — **`set_default_size` is on 476** | ★ narrow range |
| 8 | `…r44.md:56` `gkeep-ui.py:449` | the `475-476` quote | `449:application_id="org.omarchy.gkeep",` — correct (constructor starts `447:def __init__`) | ~ sibling |
| 9 | `corpus/lessons/round-44.md:12` `fetch-c1/Hyprland-FullscreenHandler.cpp:191-198` | `.internal` (belongs to `HyprCtl.cpp:431`) | `191:if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {` … `198:LAYOUT_TARGET->setPositionGlobal(WORKAREA);` — range exact | ~ sibling |
| 10-13 | `lessons/round-44.md:48` `Hyprland-Window.cpp:1687`, `Hyprland-XDGShell.cpp:455`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:681` | `quote_at` (the counter function, not a receipt fact) | `Window.cpp:1687: return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` · `XDGShell.cpp:455: m_resource->sendConfigure(…)` · `xdg-shell.xml:1150` as #2 · `gdktoplevel-wayland.c:681: configured_width = width;` — all correct as quotes of the entry's locator list | ~ non-fact |
| 14 | `lessons/round-44.md:203` `fetch/Hyprland-Window.cpp:1861-1866` | `onAck` (`:1526` locator's fragment, same line) | `1861:Vector2D CWindow::getReportedSize() {` … `1865:return m_wlSurface->resource()->m_current.ackedSize;` — range exact; the quoted fragment is on prose line **202** | ~ wrapped |
| 15 | `corpus/README.md:72` `Hyprland-Window.cpp:1732` | `realToReportSize` (belongs to `:1741`) | `1732:void CWindow::sendWindowSize(bool force) {` (call at `1741:const auto REPORTSIZE = realToReportSize();`) — pair correct | ~ sibling |
| 16 | `README.md:72` `Hyprland-Window.cpp:1751` | `scheduleConfigure` (belongs to the XDGShell locator) | `1751:m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});` — correct | ~ sibling |
| 17 | `README.md:72` `xdg-shell.xml:1144-1165` | `onAck` | `1144:<event name="configure">` … range holds the hint quote; **but the row's own `ack at :1163` is wrong — see §3.3** | ~ sibling |
| 18 | `README.md:72` `gkeep-ui.py:449` | `set_size_request` | `449:application_id="org.omarchy.gkeep",` — correct | ~ sibling |
| 19 | `README.md:308` `Hyprland-Window.cpp:1685-1699,1732` | `setSize` | `1685:Vector2D CWindow::realToReportSize() {` … `1699:}` and `1732` — both correct | ~ sibling |
| 20 | `README.md:310` `Hyprland-Window.cpp:1751` | `onAck` | `1751` as #16 — correct | ~ sibling |
| 21 | `README.md:311` `xdg-shell.xml:1150` | `ack_configure` (belongs to `:560` on the next line) | `1150` holds exactly the quoted words `a hint to the window` — correct | ~ sibling |
| 22 | `README.md:313` `gdktoplevel-wayland.c:518-528,681` | `set_default_size(420, 500)` | `518:width = …configured_width +` … `525:gdk_surface_constrain_size(` … `528:&width, &height);` and `681` — both correct | ~ sibling |
| 23 | `SKILL.md:280` `fetch-c1/Hyprland-FullscreenHandler.cpp:191-194` | `fullscreen` (generic word) | `191:if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {` … `194:LAYOUT_TARGET->setPositionGlobal(MONBOX);` — exact | ~ non-fact |
| 24 | `SKILL.md:280` `Hyprland-FullscreenHandler.cpp:130-131` | `fullscreen` | `130:if (target->window() && … !isFullscreen(target))` / `131:target->rememberFloatingSize(target->position().size());` — exact | ~ non-fact |
| 25 | `SKILL.md:281` `Hyprland-FullscreenHandler.cpp:195-198` | `fullscreenClient` (generic word) | `195:} else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {` … `198:LAYOUT_TARGET->setPositionGlobal(WORKAREA);` — exact | ~ non-fact |
| 26 | `LOG.md:2483` `Hyprland-HyprCtl.cpp:394-395,412-413` | `w->size(GEOMETRIC_GOAL)` | `394:"at": [{}, {}],` / `395:"size": [{}, {}],` / `412:"fullscreenHandler": "{}",` / `413:"allowedOverFullscreen": {},` — **no `GEOMETRIC_GOAL`**; the fact is at `426-428` (3 matching lines) and `447-448` (2 matching lines) | L legacy (round-42 text) |
| 27 | `corpus/QUALITY.md:401` `Hyprland-HyprCtl.cpp:394-395,412-413` | `CHECK_LOCATORS: locators=<n> miss=<m>` | same lines as #26 — the criterion **quotes** this as a failing locator | S self-reference |
| 28 | `corpus/QUALITY.md:401` `Hyprland-HyprCtl.cpp:427-428,448` | `locators=4 miss=3` | `427-428` carry 3 `GEOMETRIC_GOAL`, `447-448` carry 2 — the corrected form is right | S self-reference |

Counts: **23 artifacts** (15 sibling, 1 wrapped, 7 non-fact), **2 round-44 defects** (#2, #7), **1 legacy defect**
(#26, already corrected by `LOG.md:2487` — its `Hyprland-HyprCtl.cpp:427-428` is `OK` in the `fetch-c1` run),
**2 self-reference** (#27, #28).

## 3. Defects for the L1 (content, round-44-written)

Each is the exact sentence as landed, the correction, and the computed locator. The L1 lands these; this seat wrote no
tracked file.

### 3.1 `corpus/knowledge/hyprland-gkeep-size-request-r44.md:44` — quote cited by its first line only

Landed: `` `The width and height arguments specify a hint to the window about how its surface should be resized`
(xdg-shell.xml:1150) ``. The quote wraps: `1150:The width and height arguments specify a hint to the window`,
`1151:about how its surface should be resized in window geometry`; the cited single line carries 10 of the quote's 17
identifier tokens ("The width and height arguments specify a hint to the window") and none of `about how its surface
should be resized`. Criterion 77's own rule — "the cited range must contain the fact's own identifier" — is violated.

Corrected sentence (only the locator changes):

> **OBS** S299 - the configure size binds nobody: `The width and height arguments specify a hint to the window about how its surface should be resized` (xdg-shell.xml:1150-1151); a zero width or height leaves the dimension to the client (xdg-shell.xml:1154-1157), and the states sent with it say how to interpret the size (xdg-shell.xml:1159-1161). The client answers a configure with the xdg_surface ack_configure request (xdg-shell.xml:560) before it commits the matching state; that ack is what Hyprland's onAck receives.

Knock-on: `corpus/lessons/round-44.md:48` quotes this locator list verbatim (`xdg-shell.xml:1150`); if the entry is
corrected, that list should read `xdg-shell.xml:1150-1151` too. `corpus/README.md:311` needs **no** change — there the
quoted words are only `a hint to the window`, which sit wholly on 1150.

### 3.2 `corpus/knowledge/hyprland-gkeep-size-request-r44.md:56` — two-statement quote cited by one line

Landed: `` `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475) ``. `475:` has
`window.set_decorated(False)`; `476:` has `window.set_default_size(420, 500)`. The checker MISSes on the identifier
`set_default_size` absent from 475 — and the round's own lesson already says so (`corpus/lessons/round-44.md:49`: "the
S301 quote spans 475-476"), so the entry contradicts its lesson.

Corrected sentence:

> **OBS** S301 - gkeep builds one undecorated application window and declares a default size only: `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui.py:475-476); its application id is set in the application constructor (gkeep-ui.py:449).

(`:449` needs no change: the line is `application_id="org.omarchy.gkeep",`; its MISS is a sibling artifact.)

### 3.3 `corpus/README.md:72` — continuation pointer at the wrong line (checker-invisible)

Landed: ``xdg-shell 1.49 calls the configure width and height "a hint to the window" that a client need only acknowledge
(`xdg-shell.xml:1144-1165`, ack at `:1163`)``. `1163:The states are sent as an array of 32-bit unsigned integers in` is
the states sentence; the ack sentence is `1166:Clients must send an ack_configure in response to this event. See`. A bare
`:N` pointer never matches `LOCATOR_RE`, so no checker run can see this one — it was found by opening the pin.

Corrected fragment (the minimal edit is `:1163` → `:1166`; extending the range makes the citation self-contained, since
the ack sentence lies outside `1144-1165`):

> `xdg-shell.xml:1144-1167`, ack at `` `:1166` ``

The row's other five bare pointers were opened by hand and are correct: `:1741` (`const auto REPORTSIZE =
realToReportSize();`), `:629-643` (`scheduleConfigure()` 629-638 plus `configure()` 640-643), `:1514-1521` (`onAck`
through the `std::erase_if` that clears the list), `:476` (`set_default_size(420, 500)`), and `:1163` (wrong, above).

## 4. `SKILL.md` rows 280-291 — every `file:N` checked by hand

Rows 280-282 and 286-291 are exactly the round-44 additions (`git diff -U0` above). Four locators exist; all four are
correct, and three of them MISS only because of the checker's attribution.

| row | locator | what the row claims | true line (`grep -n`) | verdict |
|---|---|---|---|---|
| 280 | `fetch-c1/Hyprland-FullscreenHandler.cpp:191-194` | "Hyprland set its box to the monitor box" | `191:if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {` · `192:const CBox MONBOX = MONITOR->logicalBox();` · `194:LAYOUT_TARGET->setPositionGlobal(MONBOX);` | correct (checker MISS = non-fact fragment `fullscreen`) |
| 280 | `Hyprland-FullscreenHandler.cpp:130-131` | "the floating box is remembered" | `130:if (target->window() && target->window()->m_isFloating && mode != FSMODE_NONE && !isFullscreen(target))` · `131:target->rememberFloatingSize(target->position().size());` | correct (same artifact) |
| 281 | `Hyprland-FullscreenHandler.cpp:195-198` | "the box is the workspace work area" | `195:} else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {` · `196:const CBox WORKAREA = WORKSPACE->m_space->workArea(target->floating());` · `198:LAYOUT_TARGET->setPositionGlobal(WORKAREA);` | correct (artifact: `fullscreenClient`) |
| 290 | `Hyprland-Window.cpp:2402-2408` | pseudo-tiled box comes from the rule's size as pseudo size | `2402:if (m_ruleApplicator->static_.size) {` … `2408:m_target->setPseudoSize(*COMPUTED);` | correct (`NOFRAG`: no same-line fragment) |

Rows 282 (NOT_COMPARED), 284-285 (exit map), 286-289 (exit-5 note + D3 correction preamble) carry no `file:N`; row 288's
`quality/counters/c1-r44-geometry-states-v2.py` is a path, not a line locator. Row 291's only backticked token is the fetch
path `.ufo/waves/round-44/fetch/Hyprland-Window.cpp` (no `:N`). So the round's SKILL additions are locator-clean.

## 5. OPEN predicate defect — criterion 77's tool cannot pass correct prose

`quality/check-locators.py` decides a locator by "the nearest backticked fragment *before* it on the line, else the nearest
after" (`check-locators.py:152-154`) and reads fragments from the same line only (`run` :187). Three consequences,
measured on this round's correct prose (23 of 28 MISSes):

1. **Sibling fragment (15 MISSes).** On a line with two or more locators and one fragment, every locator but the fragment's
   own is judged by a fragment that belongs to a different locator. `entry:36` prints `…:455 OK` and `…:354-358 MISS` for
   one quote; `lessons/round-44.md:48` MISSes four locators on the word `quote_at`, which names a counter function, not a
   receipt fact.
2. **Wrapped fragment (1 MISS).** `lessons/round-44.md:203` starts with `(`fetch/Hyprland-Window.cpp:1861-1866`` while the
   quoted `m_current.ackedSize` ends line 202; the locator is judged by the `onAck` fragment that belongs to the `:1526`
   pointer on the same line.
3. **Non-fact fragment (7 MISSes).** A generic word or tool identifier inside backticks (`fullscreen`,
   `fullscreenClient`, `quote_at`) is used as the fact. `SKILL.md:280-281`'s three locators are exact and all MISS.

Reproduction (from the seat dir): the two `run-*.txt` / `explain-both.txt` commands in §1. Examples:
`LOC corpus/knowledge/hyprland-gkeep-size-request-r44.md:36 Hyprland-XDGShell.cpp:354-358 fragments=1 supported=0 verdict=MISS`
with `ATTR 'm_resource->sendConfigure(m_pendingApply.size.x, …)'`, and
`LOC SKILL.md:281 Hyprland-FullscreenHandler.cpp:195-198 fragments=1 supported=0 verdict=MISS` with `ATTR 'fullscreenClient'`.

This is reported as a defect, **not re-registered**: no predicate changes after data. If the L1 wants the command usable as
a gate, the policy calls are (a) when a locator sits between two locators, attribute it to the fragment between it and the
*previous* locator, else print `NOFRAG` instead of borrowing the next fragment; (b) allow a fragment on the immediately
preceding prose line when the current line begins with the locator; (c) declare which backticked spans may never be
evidence (tool identifiers, schema words). None of the three changes a landed verdict on this round's prose except the 23
false MISSes.

**Self-reference in criterion 77** (`corpus/QUALITY.md:401`, legacy text, not round-44-written): the criterion demonstrates
itself with `LOC … Hyprland-HyprCtl.cpp:394-395,412-413 … verdict=MISS` and `` the corrected copy reads
`Hyprland-HyprCtl.cpp:427-428,448 … supported=1 verdict=OK` ``. Run over `QUALITY.md`, both quoted locators are scored and
both MISS, so `CHECK_LOCATORS: miss=` can never reach 0 on `corpus/QUALITY.md` while that sentence exists — the criterion
declares a MISS a violation but its own text manufactures two. Its numbers do reproduce (`sed -n '394,395p' … | grep -c
GEOMETRIC_GOAL` → `0`; `412,413` → `0`; `426,428` → `3`; `447,448` → `2`, in `greps-fetch-c1.txt`), so only the
self-scoring is at issue.

## 6. Declared limits and boundaries of this sweep

- **Bare `:N` pointers are invisible.** `` `:1163` `` (the defect in §3.3), and the four correct ones beside it, never
  match `LOCATOR_RE` (no `name.ext`), so §3.3 could only be found by hand. Same for `LOG.md` round-44 lines 2496-2503 and
  `QUALITY.md` 410-415, which carry no `file:N` at all (0 locators in both runs, verified).
- **Names pinned in neither round-44 dir** are `SKIP reason=unresolved-name`, not checked: `SKILL.md:263-267` and
  `SKILL.md:276` (`Hyprland-GeometricMovableAnimated.cpp:19-20`, `Hyprland-DefaultFloatingAlgorithm.cpp:49,55-56`,
  `Hyprland-WindowRuleApplicator.cpp:422,426`, `Hyprland-RegexMatchEngine.cpp:16`, `Window.cpp:2402-2408`) — round-43
  pins, not re-pinned this round. Spot-checked read-only against `.ufo/waves/round-43/fetch/`: `19-20` carries
  `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` / `…CURRENT…`; `49,55-56` carries the `m_firstMap` guard
  and `static_.size`; `422,426` carries `std::get<Math::SExpressionVec2>(value)` and `static_.size = expr;`; `16` carries
  `return re2::RE2::FullMatch(other, *m_regex) != m_negative;`. These are legacy SKILL rows, outside the round-44 diff.
- **`LOG.md:2495`'s `setBox` link** (round-43 text, append-only) still points at
  `Hyprland-GeometricMovableAnimated.cpp:45`, where the pin has `*m_realSize = x.size();`, while
  `43:void CGeometricMovableAnimated::setBox(const CBox& x) {` is the declaration. Re-confirmed here; already routed to
  the L1 by w1 `ExecLocatorTeeth` §5, so this sweep does not raise it again.
- **Supplementary, outside the commanded six files:** `SCORECARD.md` and `PROVINCE.md` at `e4678921` were also swept
  (`0 locators, 0 miss` in both pin dirs — they carry no resolvable `file:N`).
- **MISS is not truth.** A locator can pass by sharing identifiers with an unrelated line (the tool's own docstring says
  so), so §4's hand checks, not the `OK` lines, are the evidence for those four locators.

## 7. Files, safety, tools

Seat dir `.ufo/waves/round-44/w2/ExecLocatorSweep/`: this report; `run-fetch.txt`, `run-fetch-c1.txt` (lane checker),
`cand-fetch.txt`, `cand-fetch-c1.txt` (w1 candidate), `explain-both.txt`, `explain-old-{fetch,c1}.txt`,
`explain-new-{fetch,c1}.txt`, `greps-fetch.txt`, `greps-fetch-c1.txt`, `checker-sha256.txt`, `extract.txt`,
`tally.txt`, `supplementary-scorecard-province.txt`, `prose/` (the six files at `e4678921`, sha256 in `extract.txt`),
`verify-quotes.py` + `verify-quotes.txt` (`VERIFY_QUOTES: quotes=20 absent=0`, rc 0 — every quote lifted from a pinned
receipt is asserted at its cited line; quotes of lane prose are located in `prose/` at `e4678921`, sha256 in
`extract.txt`).

Only the seat dir was written: no tracked file, counter, control, registration, reference or pin was touched; no git/jj
mutation (read-only `git rev-parse`, `git show`, `git diff -U0`, `git ls-tree` only); all git fixtures and work dirs lived
in `/fast/scratch/hyaku/mado-r44/ExecLocatorSweep/` and were deleted at close. No pacman, no host-service or compositor
verb, no Wayland client, no subagents. Tools installed: none — the lane's `python3` (3.14.8) and `sha256sum`/`diff`/`grep`
only.

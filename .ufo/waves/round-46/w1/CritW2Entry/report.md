# CritW2Entry — round-45 w2 falsification: the landed monitor-rule entry, sentence by sentence, against its pins

Seat: CritW2Entry (critic, round 46 w1). Subject: `corpus/knowledge/hyprland-monitor-rule-r45.md` at
`4d22eeb66c2835af8aaa3fac6ad838fa616aa663` (closure D1: the round-45 w2 never ran). Nothing here edits the subject;
I attack it and report.

## 0. Method and what was re-verified first

- The 14 pins under `.ufo/waves/round-45/fetch/` were re-fetched from their pinned URLs today (2026-10-26) and are
  **14/14 byte-identical**: `receipts/pins-refetch.txt` (sha256 per file). So every "source: …‌@ efb5099 / v0.14.2 /
  v0.15.1 / ecc06f3" header line is a verified URL↔bytes binding, not a typed claim.
- Every quoted snippet in the entry was located **by grep, not by eye**: `receipts/verify-quotes.py` →
  `receipts/verify-quotes.txt`, 71 probes, `SUMMARY found=71 not_found=0 checks=71`, and each probe prints the
  computed line next to the line the entry cites. **All 71 quoted locators MATCH.** The census line (entry:86) was
  recomputed value by value from the same script: `default_refresh=60` (MonitorRule.hpp:46), `refresh_tolerance=1`
  (Monitor.cpp:836), `scale_step=1/120` (Monitor.cpp:1001), `scale_search=89` (the `i < 90` loop at Monitor.cpp:1010),
  `json_refresh_decimals=5` (HyprCtl.cpp:242), `line_keys=8` (computed: 1 `if` + 7 `else if` at
  ConfigManager.cpp:1352-1373) — all 8 keys named, in order.
- The entry was split into **78 sentence units** (each claim-bearing sentence, each `source:` row, the census line,
  and the table rows; headings excluded). Ledger in §4.

## 1. Verdict

| class | count | units |
|---|---|---|
| supported, and the cited locator carries it | **72** | ledger §4, class `S` |
| supported, but the cited locator does **not** carry it (mis-located evidence) | **2** | `entry:84b`, `entry:96` |
| wrong | **1** | `entry:98` |
| unpinned | **3** | `entry:18b`, `entry:L106`, `entry:L107` |
| **total** | **78** | |

No sentence misstates a code fact: the grammar, the precedence order, the scale correction, the JSON fields and the
description construction all hold at efb5099 / v0.14.2 / v0.15.1. The single `wrong` unit (F3) is an over-hedge about
which branch ran — the pin settles what the sentence leaves open — not a misreading of code. The rest of the defect
list is binding: one locator points at the branch that suppresses the very event it is cited for (F1), one receipt ran
different bytes than the sentence attributes to it (F2), and three units bind nothing (F4).

## 2. Findings

### F1 — `entry:84b` cites the branch that *returns before* the event; the real gate is uncited (mis-located)

- **Sentence (entry:84, second sentence), shortened:** "that event fires only for an output whose rule enables it
  (Hyprland-Monitor.cpp:264 and Hyprland-Monitor.cpp:389)" — then the consequence about plain `hyprctl monitors -j`.
- **Counterexample (Hyprland-Monitor.cpp, computed lines, `receipts/verify-quotes.txt` `L84d`-`L84h` and the 262-290
  dump at the tail of that receipt):** the cited `:264` is
  `if (m_enabled && !monitorRule.m_disabled) {` and that branch **returns at `:271`** — before `:389`
  (`Event::bus()->m_events.monitor.added.emit(m_self.lock());`, the only emit site in the file:
  `grep -n 'monitor\.added\.emit' Hyprland-Monitor.cpp` → `389:`). The rule-disabled veto that actually keeps an
  output out of the active list is the *next* block, `:275` `if (monitorRule.m_disabled) {` … `:283 m_enabled = false;`
  … `:286 return;`. So the cited pair, read at the cited lines, says the opposite of its own role: `:264` is the
  "already enabled → re-apply and leave" path, which produces **no** `monitor.added` event even for an enabled output.
- **Corroboration that `:264` is not the normal first-connect path:** the event fires only at `:389`, and the host's
  active list is populated, so at first connect the `:264` branch is not taken — held evidence
  `corpus/knowledge/config-health-report-r3.md:725` records `hyprctl -j monitors` (no `all`) listing DP-1.
- **The claim itself survives** on `:275-:287` + `:389`; what fails is the citation, i.e. a reader who checks the
  entry's support finds code that contradicts the sentence's stated mechanism. That is a hidden regression: a
  reader who "re-verified" this sentence the way the entry invites would mark it wrong.
- **Axes impacted:** discernment (the closure's 5/5 "sampled gate decisions agree" does not cover this sentence);
  quality (evidence binding). Coverage/depth unaffected — the fact is right.
- **Smallest safe correction:** replace the locator with `(Hyprland-Monitor.cpp:275-287 and Hyprland-Monitor.cpp:389)`;
  optionally add "an output already enabled re-enters at `:264` and returns at `:271` without the event", which turns
  the defect into a held detail.

### F2 — `entry:96` attributes the live run to `tools/mado-monitors.py` but cites the L1 *reference's* receipt (false provenance, claim true)

- **Sentence (entry:96), shortened:** "…tools/mado-monitors.py reports AGREE and verdict OK, exit 0
  (.ufo/waves/round-45/receipts/live-monitors-host-l1.txt)."
- **Evidence (`receipts/tool-hash-binding.txt`):** at `4d22eeb`, `tools/mado-monitors.py` hashes
  `2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609`; the cited receipt's header (`:4`) records
  `tool sha256 c6ac5fc2…` — the hash of `.ufo/waves/round-45/l1-draft/mado-monitors.py`, i.e. the reference. The
  landed tool's own receipt, `receipts/live-monitors-host-r45.txt:4`, carries `2f007417…` and the same AGREE/OK/exit 0.
- **Consequence:** the claim is true, but the document points at bytes that are not the deliverable. This is the
  round-45 D2/discernment failure mode in miniature (evidence carrying an authority it does not have) and it is
  exactly what the counter **cannot** see: C1 reads the tool at REV, C2 checks the entry's clauses, neither binds a
  sentence to the receipt that ran it (registered C2 residual: "clause j binds a locator and a keyword per surface,
  not the truth of the sentence").
- **Axes impacted:** quality (evidence binding), freshness (receipt provenance). Operability unaffected.
- **Smallest safe correction:** cite `receipts/live-monitors-host-r45.txt` (tool sha256 `2f007417…`); keep the L1
  receipt only if the sentence says "the reference reported…".

### F3 — `entry:98` names a branch the cited bound excludes (`wrong`, minor, INF-labelled)

- **Sentence (entry:98), two fragments:** "whether the requested 100 Hz counted as close" / "or a custom 100 Hz mode
  was tried first and rejected" / "not proof of which branch ran".
- **Counterexample:** the closeness test at Monitor.cpp:836-837 is three `!DELTALESSTHAN(…,1)` terms, the third being
  `!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1)`; the custom push at :838-839 executes only
  when one of them is true. With the gap the entry itself states (0.003 Hz), the third is
  false, and the dump shows the running size equals the requested size, so the first two are false. **No custom mode is
  created on this run**: the pushed custom would have carried `RULE->m_refreshRate * 1000.f` = 100.000 Hz
  (:838-839), while the JSON (device receipt `live-monitors-host-l1.txt`, projected line) shows `99.997` — a property
  of a native mode, read back at :903.
- **So:** "not proof of which branch ran" is not true; the pin at :834-839 resolves the branch, and the entry's own
  parenthetical already contains the deciding number. Minor: the entry's practical conclusion (the tool's 1 Hz
  tolerance mirrors Hyprland's bound) is unaffected.
- **Axes impacted:** depth (a held decision that the source settles is left open) — no axis harmed.
- **Smallest safe correction:** "the 0.003 Hz gap is inside the strict 1 Hz bound, so the closeness test passes and no
  custom mode is created (Hyprland-Monitor.cpp:834-839); the mode that runs is the native one, and the only thing the
  dump cannot show is whether it was also the preferred mode."

### F4 — unpinned (3 units; none false)

| unit | text | status |
|---|---|---|
| `entry:18b` | "upstream main already drops the legacy hyprlang manager (Hyprland a9902ea, 2026-07-22)" | **no pin, no receipt** under `fetch/`. Externally true: `receipts/external-a9902ea.txt` — `a9902ea65f461af868497c4e74fed798ade0b1b0`, `2026-07-22T16:35:10Z`, "config: remove legacy config support (#15539)", and `main/src/config/legacy/ConfigManager.cpp` → HTTP 404. A recheck trigger whose date ranger is itself unevidenced. |
| `entry:L106` | "a Wayland or headless backend builds its description differently and is not covered" | no aquamarine Wayland/headless pin; declared limitation, contributes no fact. |
| `entry:L107` | "Upstream main has removed the hyprlang line form (Hyprland a9902ea)" | same commit as `entry:18b`, same status: unpinned, externally true. |

Smallest safe correction for the pair: either add the API digest + 404 line as a recheck receipt (one file), or drop
the hash from `recheck:` and keep the claim in prose at `Limits`, where it already lives.

### F5 — note-level (no correction demanded, listed so the next round does not re-find them)

- `entry:62b` cites `Hyprland-HyprCtl.cpp:276-277` for the `description` field; `:276` is blank, the value binding is
  `:277` (`escapeJSONStrings(m->m_shortDescription)`) and the key literal is `:234`. The *claim* is right — the JSON
  `description` is the **short** description, not the long one (computed: `L62e` = 234, `L62f` = 277).
- `entry:L105` cites `743-747` for "replace same-selector rules"; `:743` `m_config->parse()` and `:747`
  `handleMonitorv2()` carry the ordering half only; the replacing half is `MonitorRuleManager.cpp:37-42`.
- `entry:68` says "the list is then tried from the back, so that custom mode is tried first (878-889)". True for a
  plain `WxH@R`; with a `modeline` also on the line, `:847-848` pushes the modeline mode *after* the custom one, so it
  is tried first. Scope-correct as written, worth a clause.
- `entry:T27` (table) "the mode closest to 60 Hz at that size is chosen" is INF-labelled and true in effect, but the
  same custom-mode-first path of `:834-839` applies when no mode is within 1 Hz of 60 — a reader should not take the
  row as unconditional.

## 3. What the round-45 closure sampled — and what it did not

The closure's discernment work (§4 of `corpus/lessons/round-45-verifier-spotcheck.md`) sampled **pin decisions**, not
entry sentences:

- gate decisions re-opened: **S306, S312, S313** (three admits) + two rejects (the float32 finding; wiki main);
- SOURCES quotes re-opened: **S310** (`:11`), **S312** (`:40`);
- the live run reproduced once (§2, C1 live row) — but against `receipts/live-monitors-host-r45.txt`, i.e. the closure
  used the correct receipt that `entry:96` does not cite (F2).

**10 of 14 pins were never re-opened**: S302, S303, S304, S305, S307, S308, S309, S311, S314, S315. Of the 78 units,
the closure touched **6** (`entry:70a` via S312:40; `entry:72a` via S313:39; `entry:72b`/`entry:74a`/`entry:74b`
partly, via the S306 `:996-1025` read; `entry:90` via S310:11) and reproduced the run behind `entry:96` without
checking its binding. **72 units were not sampled.** Both defects F1 and F2 sit inside that unsampled set, and F1 is
on a pin (S306) the closure *did* sample — sampling a file is not sampling a claim about it.

Sentences the closure did not sample that carry the most risk, in order:

1. `entry:84b` — F1, the event/gate mechanism (the only case where the cited lines actively mislead).
2. `entry:96` — F2, receipt provenance for the live claim.
3. `entry:42b` — "a parse error inside a known field does not stop the add" (ConfigManager:1384-1386): the entry's
   most consequential behavioural claim (a bad mode is still installed), verified by this seat only.
4. `entry:60a-c` — rule precedence incl. the output-management override (Manager:45-106).
5. `entry:62b` — which description the JSON prints (HyprCtl:234/277); the F5 slop shows nobody read it.
6. `entry:44a` — the `modeline` branch (Parser:14-20, 119-121) and the 0x0 preferred sentinel (Monitor:773).
7. `entry:92b` — `sdr_eotf` on a `monitor =` line is rejected whole (ConfigManager:1351-1379 vs 819-831).
8. `entry:54b` — the `isNumber2` edges (`1.` fails, `07` passes), String.cpp:50-83 + Parser:219.
9. `entry:18b`/`entry:L107` — F4, the a9902ea recheck clause.
10. `entry:105` — monitorv2 ordering (743-747) and the F5 locator slop.

## 4. Ledger (78 units)

Class `S` = supported at the cited locator (computed line in `verify-quotes.txt`); `M` = claim supported but cited
locator does not carry it; `W` = wrong; `U` = unpinned.

| unit | entry line | claim (compressed) | class | locating evidence |
|---|---|---|---|---|
| H1a-H1n | 3-16 | the 14 `source:` rows (rev + path + scope) | S ×14 | `receipts/pins-refetch.txt`: 14/14 byte-identical |
| H2 | 17 | `verified-at: 2026-10-26` | S | pins refetched today, identical |
| H3a | 18 | "re-pull the fourteen pins and re-run the counter" | S | `fetch/` holds exactly 14 files |
| H3b | 18 | main already dropped the legacy manager (a9902ea) | **U** | `receipts/external-a9902ea.txt` (external, not a pin) |
| H4 | 19 | ground U5; chain absent at base; held neighbours | S | `c2-ground-base.txt` exit 1; r3:148, hyprctl-verification-layer:153 |
| H5 | 20 | Lane/Round | S | path + round |
| T26 | 26 | one rule per selector, newest first, else empty rule, else default; unsafe fallback skips | S | Manager:37-42, 86-106 |
| T27 | 27 | no `@` → 60 Hz default → closest to 60 at that size (declared INF) | S | MonitorRule.hpp:46, Monitor:750/834 |
| T28 | 28 | close = <1 px and <1 Hz, else custom first | S | Monitor:836-839 |
| T29 | 29 | written scale = running only if it divides; else 1/120 search (89), else default | S | Monitor:996-1049 |
| T30 | 30 | explicit placed as written, auto after | S | PositionController:27-29, 61-101 |
| T31 | 31 | eight keys; any other rejects the line | S | ConfigManager:1351-1379 (8 computed) |
| T32 | 32 | `sdr_eotf` documented, absent from the line handler, monitorv2 only | S | wiki:253, ConfigManager:1351-1379/819-831 |
| T33 | 33 | `monitors` = active; `all` = every real output | S | MonitorState:25-46, 109-114; HyprCtl:327 |
| T34 | 34 | host output agrees on every compared field | S | `live-monitors-host-l1.txt` |
| 38a | 38 | CVarList2 default delim comma | S | VarList2.hpp:18 |
| 38b | 38 | handleMonitor builds from the whole value, field 0 = selector | S | ConfigManager:1293-1297 |
| 40a | 40 | field 1 tested for the modifier forms | S | ConfigManager:1299 |
| 40b | 40 | disable/transform/addreserved semantics | S | ConfigManager:1300-1343 |
| 42a | 42 | three positional fields, then 8 KEY/VALUE pairs; unknown key drops the line | S | ConfigManager:1345-1347, 1351-1379 |
| 42b | 42 | a known field's parse error does not stop the add; degrades to preferred/auto | S | ConfigManager:1384-1386; Parser:126/137/177/185; MonitorRule.hpp:45; Monitor:750 |
| 44a | 44 | parseMode keywords, modeline, `WxH@R` | S | Parser:110-143, 14-20, 119-121 |
| 44b | 44 | 0x0 is the preferred sentinel the apply step tests | S | Monitor:773 |
| 46 | 46 | rate read only when `@` present | S | Parser:134 |
| 48a | 48 | default rate 60 | S | MonitorRule.hpp:46 |
| 48b | 48 | `WxH` without rate asks for 60 Hz | S | MonitorRule.hpp:46 + Parser:133-134 + Monitor:750 |
| 50 | 50 | parsePosition: auto\* sentinels, else `stoi` halves | S | Parser:145-190 |
| 52 | 52 | parseScale: auto, float test, <0.25 → 1 | S | Parser:193-211 |
| 54a | 54 | minus sign only first | S | String.cpp:59 |
| 54b | 54 | one dot, final char must be a digit; `1.` fails, `07` → 7 | S | String.cpp:50-83, Parser:219 |
| 58a | 58 | add erases same-selector rules first | S | Manager:38 |
| 58b | 58 | add then appends → re-added selector moves last | S | Manager:37-42 |
| 60a | 60 | reverse walk, newest wins; else first empty selector; else built-in | S | Manager:96-116 |
| 60b | 60 | unsafe fallback: 1920x1080, auto, scale 1 | S | Manager:86-94 |
| 60c | 60 | output-management client state overrides the rule | S | Manager:45-84 |
| 62a | 62 | selector by name, by `desc:` prefix (long or short) | S | Monitor:1201-1211 |
| 62b | 62 | long = backend description minus commas; short = make model serial; JSON prints the short one | S | Monitor:250-256, HyprCtl:234/277 |
| 64a | 64 | DRM description = make model serial (name) | S | DRM.cpp:2101 |
| 64b | 64 | the long description is rebuildable from the dump, DRM only | S | DRM.cpp:2101 + HyprCtl:235-237/233 |
| 68 | 68 | closeness sort, custom push, reverse try, keyword sorts | S | Monitor:784-850, 878-889 |
| 70a | 70 | "close" is strict `<` | S | macros.hpp:40; Monitor:836-837 |
| 70b | 70 | running rate is the applied mode's own | S | Monitor:903 |
| 72a | 72 | division in double precision | S | Vector2D.hpp:39 (fields :21-22) |
| 72b | 72 | logical size = that division; correction only if fractional and checks enabled | S | Monitor:996-997, 721 |
| 74a | 74 | search starts at the nearest 1/120 | S | Monitor:1001 |
| 74b | 74 | 89 steps up/down; no divisor → default + error; divisor → corrected + notification | S | Monitor:997-1049 |
| 76a | 76 | explicit position applied as written, before auto | S | PositionController:27-29 |
| 76b | 76 | auto directions placed afterwards | S | PositionController:61-101 |
| 80a | 80 | refreshRate printed with 5 decimals | S | HyprCtl:241-242 |
| 80b | 80 | width/height pixel size, scale applied, disabled = !enabled, mirrorOf id or none | S | HyprCtl:278-286 |
| 82 | 82 | one optional arg; only `all` selects allMonitors | S | HyprCtl:313-327 |
| 84a | 84 | every real output enters the full list before the enabled check | S | MonitorState:112-114 (check at :122) |
| 84b | 84 | active list = monitor-added event, mirrors dropped; event only for an enabled rule | **M** | gate is Monitor:275-287 + 389; cited `:264` returns at `:271` |
| 86 | 86 | census line (6 values) | S | recomputed in `verify-quotes.txt` |
| 90 | 90 | wiki line form | S | wiki:11 |
| 92a | 92 | wiki positional order = handler order | S | wiki:8-12; ConfigManager:1345-1347 |
| 92b | 92 | wiki documents `, sdr_eotf, X`; handler rejects it whole; monitorv2 reads it; wiki v2 table lists it | S | wiki:253, 319; ConfigManager:1351-1379, 819-831 |
| 92c | 92 | not exercised on the host | S | no receipt shows a config change |
| 96 | 96 | host rule/output AGREE, verdict OK, exit 0, cited receipt | **M** | claim true via `live-monitors-host-r45.txt`; cited `-l1` ran `c6ac5fc2…`, not the tool's `2f007417…` |
| 98 | 98 | "not proof of which branch ran" | **W** | Monitor:834-839 settles it; custom would read 100.000 at :838-839 |
| 100 | 100 | UNK: 59.99 Hz and fractional-scale correction unexercised | S | declared unknown, no claim |
| L104 | 104 | code-read facts at the three revisions; no changed-config run | S | pins; receipts |
| L105 | 105 | monitorv2 after the parse, replaces same-selector rules | S | ConfigManager:743-747; Manager:37-42 |
| L106 | 106 | non-DRM backends build descriptions differently | **U** | no pin |
| L107 | 107 | main removed the hyprlang line form | **U** | same as H3b |

## 5. Impacted axes (round-45's own axis table)

- **quality**: harmed at the citation layer, not at the fact layer — two of 78 units bind evidence that does not
  carry them (F1, F2) and one binds nothing (F4). The round-45 verdict "quality: unprovable-but-better" named "the
  planned w2 never attacked the landed bytes" as the reason it was not countably improved; running the w2 now returns
  a concrete, small, correctable defect list instead of a clean pass, which is the outcome that verdict predicted.
- **discernment**: the closure's "5/5 sampled gate decisions agree" is accurate and insufficient — it sampled 3 of 14
  gate decisions and 6 of 78 sentences, and F1's pin (S306) is one it *did* open. The closure's own dataset supports a
  distinction it did not draw: opening a pin ≠ checking a sentence that cites it.
- **coverage / depth / freshness / adjacency**: unchanged. No pin contradicts a code fact; no new source is needed;
  the recheck trigger stands (F4's a9902ea clause is true).

## 6. What this seat did not do

- Did not judge, admit, edit or integrate anything; wrote only inside
  `.ufo/waves/round-46/w1/CritW2Entry/` and `/fast/scratch/hyaku/mado-r46/CritW2Entry/` (deleted below).
- Did not run the round-45 counters, the axis gate, or any compositor write; no `dispatch`/`keyword`/`reload`.
- Read the host only through committed receipts; the two network reads (pin refetch, one API commit lookup) are the
  only external calls.
- Session material: the held neighbour `config-health-report-r3.md:149` and `hyprctl-verification-layer.md:153` carry
  the host description including the serial (round-45 D2). I cite them by `file:line` and do not reproduce the value.
- Tooling: nothing installed, no package transaction, no pacman; only `python3` (stdlib) and `curl` (two read-only
  GETs: the pin refetch of 14 files and one GitHub API commit lookup), both already on the host.

## 7. Receipts in this seat

- `receipts/verify-quotes.py`, `receipts/verify-quotes.txt` — 71 grep-located quotes, computed lines vs cited lines,
  census recompute, and the `onConnect` 262-290 dump that is F1's evidence.
- `receipts/pins-refetch.txt` — 14/14 pin hashes re-fetched 2026-10-26, identical.
- `receipts/tool-hash-binding.txt` — the two tool hashes at `4d22eeb` and the header of both live receipts (F2).
- `receipts/external-a9902ea.txt` — the one external check (F4).

author: hyaku closure (non-author integrator, @m_opus)

# mado round 47 — non-author closure spot-check (attempt 1)

Lane HEAD before `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`, after `d40189c924e01dc1cbe290474eb4256d343590d4`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-26T18:35:18-03:00 launch mado round=47 pgid=1078180 driver=hyaku-inline attempt=1` /
`2026-10-26T20:24:36-03:00 complete mado round=47; hyaku-inline attempt=1` (one launch, one completion; `grep 'mado round=47'` finds no other line).
I did not author the round. Re-checks ran on committed bytes (`git show`/`git ls-tree`/`git grep` at the cited revisions), on upstream
raw files re-fetched 2026-10-26, and read-only on the host. The deliverable ran from committed bytes
(`git show d40189c9:tools/mado-terminal.py`, sha256 `b84d5c4f…`, equal to `tool_sha256` in `receipts/live-terminal-host-r47.txt`).
The resolver ran only with `--print-*` flags and a fresh `XDG_CACHE_HOME`; no terminal was launched. Lane counters and gates were not
executed (§Gate standard, Closure consequence): their committed receipts were verified. Two read-only reviewer seats I dispatched
re-read the w2 attacks and the entry's citations; their findings are folded in below and marked "seat".

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-47/mado.md` (fleet) | `mado-shokunin 6fd13912c827b57080d91e73f4edbcad6a8f7899` (20:22:32-03:00, after the lane tip 20:21:31, before the complete line) | ok |
| SHONEN heading | `grep -c '^## SHONEN'` on the report; `grep -c '^- \[' SHONEN.md` | 1; 4 report lines `[~]` for 4 boxes | ok |
| cited commits exist and are ancestors | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for c24adef2, d7527d60, 6605f5f1, 9bddd6ac, 0c699605, f2b8568b, d40189c9 | all `commit`, all ancestors | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain` | `local=remote=d40189c9… ahead=0 behind=0 tracked=0 untracked=0`; empty | ok |
| prompt carries the contract | `diff <(sed -n 1,140p .ufo/prompts/mado-round-47.md) templates/round-prompt.md` | only placeholder substitutions; §4 report path + SHONEN, §5 commit/push scope/L0, §3 L2 floor, §6 addendum (lands-last, hash citation at `:433-439`, write scope `:365-367`) | ok |
| commits authored by lane identity | `git log --format='%an <%ae>' 60edb66e..d40189c9` | 7 commits, all `mado-shokunin <mado@shokunin.local>` | ok |

Defects (status-neutral, routed in section 6): D1 post-freeze contract narrowing; D2 an unreceipted number in the report; D3 unrouted
readdir-order blind spot; D4 locator off by one.

## 2. Per-claim re-check

**C1 — operability (capability acquisition), `tools/mado-terminal.py`.** Re-measured plainly, plus evidence-verified counter.
- Presence: `git cat-file -e 60edb66e:tools/mado-terminal.py` → absent; at `d40189c9` → present.
- Selftest from committed bytes: `python3 -I t.py --selftest` → `MADO_TERMINAL_SELFTEST: 43/43 passed`.
- Live, against the real resolver: `XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-id --print-path --print-cmd` → exit 0,
  `Alacritty.desktop` / `/home/vgpnk/.local/share/applications/Alacritty.desktop` / `alacritty`; then
  `python3 -I t.py explain --observed <that capture>` → `MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop cmd=alacritty cache=absent verdict=AGREE`, exit 0.
  `t.py print --print-id ''` → `MADO_TERM_OUT_OF_CONTRACT: empty-string argument`, exit 2 (the report's refusal reproduced).
- Pin identity: `sha256sum /usr/bin/xdg-terminal-exec` and the re-fetched tag script both `89f2be9a…` = `receipts/fetch-sha256.txt`.
- Counter (evidence-verified, not executed): `receipts/c1-before-base.txt` `fixtures=0/190 … tool=absent verdict=TARGET_MISSED rev=60edb66e… exit=1`;
  `c1-after-data.txt` `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=0c699605… exit=0`;
  `c1-tip.txt` same MET at `rev=f2b8568b…`. Controls `ctl-c1.txt`: `CTL_C1 VERDICT: PASS (… 0 of 28; reference met: 1)`, exit 0.
  `h12-check.txt`: `cases 32 diff 0 trips 0`.
- Seat (C1 recheck): H1 and H2 are fixed at the tip (`tools/mado-terminal.py:492-538`, `:365-369`); hermetic trees (directory and
  /dev/null-symlink `foot.desktop` in a later dir; `Exec=-p`, `--`, `-v`, `-pV`, `-x`, `TryExec=-p`/`-x`) give identical stdout and exit
  for pin and tool. Two refusals diverge from the pin: a FIFO named `*.desktop` (pin blocks, tool exit 2) and HOME unset (pin exit 1,
  tool exit 2). Both are declared out of contract only in the landed docstring, not in the frozen reference (D1).
  The counter has blind spots: readdir order is covered only by the 150 nonce cases (D3); explain `cmd=` is not compared (routed as
  `w2/CritC1Explain.md`); MutC1Fixtures has 9 kills outside the fixtures (routed as M47-10).
- Ruling: **verified**. The registered before→after holds on committed receipts, and my own live run agrees. The divergences are
  refusals on environments the hotkey never produces (no HOME, a FIFO entry). They do not select a wrong entry. The post-freeze change
  to the contract text is a conformance defect (D1); it does not falsify the claim.

**C2 — coverage (sourced), `corpus/knowledge/xdg-terminal-selection-r47.md`.** Re-measured plainly, plus evidence-verified counter.
- Presence: absent at `60edb66e`, present at `d40189c9`; knowledge `git ls-tree --name-only <rev> corpus/knowledge/ | wc -l` 63 → 64.
- Ground: at base, `corpus/knowledge/terminal-route-r17.md:144-145` holds "[UNK] whether the resolver actually picks that entry over the
  system one at launch; no launcher ran"; the new entry answers it from the cold-cache capture, and my live run reproduces that
  capture. Committed `receipts/c2-ground-base.txt` exit 1.
- Rows: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 262 at base, 276 at tip (report: 262 → 276).
  S326-S331 are `mined`, with used-by naming the entry (seat). `diff` base→tip SOURCES.md shows 0 removed lines, so held rows S056-S060 and S290-S297 are byte-identical.
- Citations: I re-fetched the tag script and checked the entry's `:353`, `:780`, `:816`, `:962`, `:1060`, `:1092`, `:1144`, `:1172`, `:1179`, `:1331`
  verbatim, plus README `:179-180` and `:300-301`. The script has 1499 lines and 23 functions, matching the entry's census line.
  The hotkey is `~/.config/hypr/bindings.conf:2`. The seat checked another 30+ locators; all agree.
- W1-W3 (`w2/CritEntryContent.md`) are corrected in the landed text (seat, line 43). CritC2Forgery F4/F7/F8 are counter blind spots,
  not entry defects. The entry's Limits keep the launch half `[UNK]`.
- Counter (evidence-verified): `c2-before-base.txt` `admitted=0/1 … TARGET_MISSED exit=1`; `c2-after-data.txt` and `c2-tip.txt`
  `clauses=a:1 … i:1 admitted=1/1 verdict=TARGET_MET exit=0`; controls `ctl-c2/ctl-summary.txt` POS 0, ten negatives 1.
- Ruling: **verified**. Residual: one locator off by one (D4); statements true.

Re-measured vs evidence-verified: presence, rows, knowledge count, census, citations, tool selftest and the live AGREE were re-measured
by me. The PRED-C1/PRED-C2 verdicts, controls, axis check and h12 cases were verified from committed receipts.

Harm watch: `git diff 60edb66e d40189c9 -- SCORECARD.md` is a pure append (+45: the Round 47 section, the claim table, a capability row,
sources, the axis line, errata E1-E6 and N1, planned). The whole round deletes 0 lines: `git diff --numstat 60edb66e d40189c9`, deleted
column summed = 0. The R1 erratum is appended to `hyprland-input-devices-r46.md` (+21, 0 removed). Axis receipts (evidence-verified):
`axis-base.txt` navigation 63/63, calibration 77/77, operability 12/12; `axis-tip.txt` 64/64, 82/82, 12/12, `checked=3 mismatched=0`.
I re-derived the inputs plainly: knowledge 63 → 64, and QUALITY gains 91-95 (+5), each citing M47-1..6 and round-47.md. No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1: tool absent → present; selftest 43/43; live AGREE against the real resolver from committed bytes; PRED-C1 MET at data and tip (receipts); H1/H2 fixes confirmed hermetically |
| coverage | improved | C2: entry 0 → 1; knowledge 63 → 64; rows 262 → 276; base ground `[UNK]` at terminal-route-r17.md:144-145 answered; PRED-C2 MET (receipts); sampled citations verbatim |
| depth | unchanged | SKILL.md gains "Terminal selection (round 47)" (`SKILL.md:2147`) with verdict/symptom tables; not a declared claim; no held table re-graded |
| freshness | unchanged | S332-S339 supersede S290-S297 with pins re-fetched 2026-10-26 (append-only); no held SKILL claim re-verified as stale and fixed in place |
| calibration | unchanged | axis fraction stays 1.0 (77/77 → 82/82); report self-limits are honest (R3/R4b open, launch half `[UNK]`). D1 and D2 are calibration slips, not mismatches with repo state |
| adjacency | unchanged | `w1/ConnSiblings.md`: no sibling claims terminal selection; nothing absorbed |

## 4. Discernment spot-check (`corpus/lessons/round-47.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `GATE S326` / row S326 | admit (tier A, `code`) | `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec` re-fetched: sha256 `89f2be9a…` = gate line = `/usr/bin/xdg-terminal-exec`; quote verbatim at `:780` | **agree** | Primary code of the exact resolver on this host; the quoted rule (last found wins) is the one the entry's override answer rests on. |
| `GATE S329` / row S329 | admit (tier A, `spec`) | `https://gitlab.freedesktop.org/xdg/xdg-specs/-/raw/a0eaad5c…/desktop-entry/desktop-entry-spec.xml` re-fetched: sha256 `a1baadee…` = gate line; quote at `:164` (sentence ends `:165` "$XDG_DATA_DIRS precedence order is used") | **agree** | Authoritative spec at a pinned commit; the entry uses it as the contrast the script departs from, which is the right role. |
| `GATE S328` / row S328 | admit (tier **B**, `spec`) | `https://gitlab.freedesktop.org/terminal-wg/specifications/-/raw/64c429df…/proposals/xdg-terminal-exec.md` re-fetched: sha256 `c16a717a…` = gate line; `presense of \`TerminalEmulator\` category` at `:159` (source spelling) | **agree** | The proposal is unmerged; tier B scoped to "the proposed specification" is honest, and the script, not the proposal, is the judge. |
| REJECT xdg-specs MR !87 (TerminalExecuteArguments) | reject | GitLab API `projects/xdg%2Fxdg-specs/merge_requests/87`: "Draft: desktop-entry: Add TerminalExecuteArguments key", state `opened`; `grep -c -i TerminalExecuteArguments` on the v0.14.3 script → 0 | **agree** | A draft key the resolver never reads cannot ground any step of the selection; the flip (a release that reads it) is right. |
| REJECT XDG Base Directory spec row | reject | v0.14.3 script `:148`, `:157`, `:166`, `:172` carry the defaults inline (`${XDG_CONFIG_HOME:-"${HOME}/.config"}`, `${XDG_DATA_DIRS:-/usr/local/share:/usr/share}`, …) | **agree** | The entry's step 1 cites the script's own defaults; a basedir row would be cited by nothing (CORPUS rule 4). |

SOURCES row re-opened for its quote: S330, `X-TerminalArgDir=--working-directory=` (1 token, ≤25 words), present at `:17` of
`https://raw.githubusercontent.com/omacom/omarchy/6aa2aec1…/applications/Alacritty.desktop` (re-fetched). Also S327:
`Valid cache bypasses` at README `:300`, sentence completing at `:301`, sha256 `c7a1a8bb…` = gate line.
Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → W04 ×17 (S030, S042,
S045, S097, S119, S120, S121, S303, S307, S317, S318, S320, S321, S324, S326, S327, S332) + W01 S277, `mado ok`, exit 0. This matches
`receipts/census-after.txt` and the report's "W04 ×17, W01 ×1".

## 5. Trend verdicts

- **expansion: improved.** One capability shown running: my live AGREE from committed bytes, and selftest 43/43. One knowledge entry
  on ground held `[UNK]` at base (terminal-route-r17.md:144-145; knowledge 63 → 64). Rows 262 → 276, and the six new rows' pins are
  byte-equal to upstream today.
- **quality: unprovable-but-better.** I rule this as the named non-author reviewer. It is better: the round-46 R1 erratum landed
  (append-only, citing the r46 receipt), and R4a superseded S290-S297 with re-fetched pins. w2 found two contract errors (H1/H2) and
  three wrong entry sentences (W1-W3), all fixed before landing and confirmed at the tip. It is not countably improved: R4b (the
  round-45 entry's six sentence units) is carried a further round, the new entry has one off-by-one locator (D4), and the landed
  contract text was narrowed after the freeze (D1). It is not `harmed`, because every open item is marked in a committed lesson or
  report and no sampled sentence is false.
- **discernment: improved.** 5 of 5 sampled gate decisions agree on outside re-reading: three admits, including an honest tier B,
  and two rejects. The lane narrowed its own premise on w1 evidence and kept the launch half `[UNK]`. Limits: D3, a counter blind spot
  the lane's own seat found, was not routed. D2 is a numeric claim without a receipt.

Closure: status `ok`, **admitted=true**, verdict `admitted`. Both claims verify, and no axis is harmed.

## 6. Routed defects (lane fixes next round)

1. D1: the C1 contract was narrowed after the freeze without re-registration. The landed `tools/mado-terminal.py` docstring adds
   "HOME unset", "a FIFO named like a desktop file in a later application dir" and "symlink loops" to the out-of-contract list; the
   frozen reference `l1-draft/mado-terminal.py@d7527d60` (`registration.md` C1 Contract) lists none of them. On these inputs the tool
   exits 2 where the pin exits 1 (HOME unset) or blocks (FIFO). Fix: record the delta as an appended lesson line (the frozen
   `registration.md` stays untouched). Then either register the exclusions in the next round's freeze, or model HOME unset as the pin
   does (exit 1, empty stdout).
2. D2: the report's "session-material gate reads `findings=128` at the tip (115 at base)" has no committed receipt.
   `git grep -c 'findings=128' d40189c9` finds nothing, and the only tip-era receipts are `w1/ExecSessionMarker/receipts/*` (findings
   136/139 at other revisions). Fix: commit a receipt naming its revision, or correct the number in the next report. R3 (marker
   install) stays open, routed again.
3. D3: the readdir-order blind spot (`w2/ExecC1Determinism.md:10`) is not routed in the report or lesson. A `sorted()` walk scores
   190/190 + 190/190, and only the nonce cases catch it (1/150 at nonce 4242). Fix: add two-valid-candidates-in-one-dir fixtures with an
   expected readdir order, together with M47-10 (fixture schema v2).
4. D4: `corpus/knowledge/xdg-terminal-selection-r47.md` Limits cites `terminal-route-r17.md:150-151` for the helper `[UNK]`; the text
   sits at `:149-150`. Append an erratum line.
5. Carried, as the report says: R3, R4b, M47-10, `w2/CritC1Explain.md` (explain `cmd=` not compared), and `w2/SentC1Sandbox.md` F1-F4.

SHONEN boxes remain `[~]`. Box 2 (end-to-end live run) is reproducible by a non-author: I reproduced the resolver capture and
`verdict=AGREE` from committed bytes. Box 3 held for me: the tool's docstring usage (`--selftest`, `explain --observed`) ran as written,
with no oral context. Promotion review is operator-owned. Operator notes carried from the report: the host monitor serial in held files
(M46-10) and the red session-material gate (R3).

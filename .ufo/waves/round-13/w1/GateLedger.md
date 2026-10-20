# GateLedger — C2 exact-set census: knowledge change record + named-negative measurement (DRAFT, not applied)

Lane: MadoR13.GateLedger · wave mado-r13-w1 · axes coverage, operability · milestone exact-set census and sourced U4 boundaries (this draft covers C2 only).
Status: draft. No source, corpus, LOG or SOURCES file was edited. No test, build, lint, format or selftest was run by this lane.
Marks: [O] observed in a read at the time stated · [I] inference from code reading · [U] unknown, needs measurement.

## 0. Sources read (absolute paths, read-only)

| Anchor | What it fixes |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` §0, §4, §5.2, §8 | Single-writer custody; cadence (gate edit outside pairs = `--regression` SETUP until re-cut); widening rule (every widening carries `MADO_REGRESSION: PASS`); re-derive commands. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` §3 | Snapshot-diff receipt vocabulary; row ids are the diff key (`plane|id`), so new row ids show as `appeared`. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/QUALITY.md` criteria 2, 4, 14 | Source-anchored claims; errata append-only; criterion 14: "A census compares expected and observed sets and names both missing and extra members; pin module membership where it is a claim." |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` Registry (S001–S039), header | Row shape (11 columns), append-only rows, `own-work` kind, tier A; S040–S043 reserved by main (ProtocolPhases, GlobalCapture, GlobalDocs, core spec); gate evidence uses S044; main owns allocation. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/config-drift-r12.md` lines 86–89, 120, 125 | The set-blind gap is named M13; `LOCAL` was deliberately not widened in round 12; live directory held 13 `*.conf` on 2026-10-19 (its own measurement, [U] now). |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-12.md` line 25 (M13) | Mistake: "The drift instrument can detect a count mismatch without naming the set delta, and presence checks do not establish set equality." Fix route: exact census naming missing and extra; pin membership. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` lines 2173–2273 | The hypr file plane under change (see §1). |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` lines 915–1045 | Selftest scenarios A, B, C, D, E, F, H, I that already touch hypr rows. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` lines 100–122, 1546–1550 | `row()` helper; `REGRESSION_RECUT` printer. |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/LOG.md` tail, `/home/vgpnk/Projects/shokunin/mado-shokunin/AGENTS.md` | Every change appends a LOG.md entry with motivating evidence; commits carry lane identity. |

Current gate revision (this lane, read-only `sha256sum` / `wc -l`, 2026-10-20): `tools/mado-verify.sh` sha256 `ea798ad078f139f34ce06e72ef2c1fecb0732bfc063b1ea95bec50655f27e0b5`, 3,245 L. [O]
`gate-standing-use.md` header and §8 still name `93e43f8f…` (3,231 L). That note is stale against the current file; per its own §8 rule, every number in it is history until re-derived. [O]

## 1. Baseline — what the hypr inventory checks do now [O from code read; [I] for outcomes]

- `hypr.root.include_graph` (`tools/mado-verify.sh:2222-2239`): compares **count** (`"${#got[@]} source lines (expected ${#EXPECT[@]})"`, :2226), then **position by position** (`"line $((i + 1)): got '…' want '…'"`, :2230). A dropped or added line shifts every later index, so the first named mismatch is positional, not the set delta. Missing and extra members are never named. [I] for the shift behaviour; [O] for the message strings.
- `hypr.root.sources_resolve` (`:2241-2255`): iterates EXPECT only; names unresolved targets (`"unresolved:$tmiss"`). Already named; kept.
- `hypr.local.inventory` (`:2262-2273`): iterates the fixed 12-name `LOCAL` array with `[ -f ]`. Names missing (`"missing:$lmiss"`). **Set-blind**: a stray `*.conf` in `$H` is never seen, so the row reads `PASS` `12/12`. [O for the array and the presence-only loop; [I] for the PASS on a stray file, which the code path implies and N7 will measure.]
- Selftest coverage today (`:915-1045`): scenario B asserts only `hypr.local.inventory FAIL` and `hypr.root.sources_resolve FAIL` by id (`st_row_has` checks id + status, not detail). Scenario H asserts only `hypr.root.include_graph FAIL`. No scenario asserts a named missing or extra member, and no scenario plants an extra local file. [O]
- Fixture A (`build_fixture`, `:233-310`) already writes the 12 LOCAL names **plus `gkeep.conf`** (loop at :265-266 includes `gkeep`), so fixture A has 13 `*.conf` locals. [O]

## 2. Design of the exact-set census (what C2 changes)

Two sets, compared exactly; no tolerance.

- **Sources.** `E_src` = `EXPECT` (18 entries, text as written, `~` unexpanded). `O_src` = the ordered `source =` right-hand sides from `hyprland.conf` (the existing awk at :2223). Compute `missing = E_src \ O_src`, `extra = O_src \ E_src`, `dup = entries occurring >1 time in O_src`. Keep the existing **order** check (precedence is order, SKILL §include order) and keep the existing count message as a prefix so the old wording still matches.
- **Locals.** `E_loc` = an explicit 13-member list: the 12 MADO-1 names plus `gkeep.conf`, pinned as a literal array (criterion 14: pin membership where it is a claim). `O_loc` = basenames of `$H/*.conf` that pass `[ -f ]` (maxdepth 1 by glob; dotfiles excluded by the glob). `missing = E_loc \ O_loc`, `extra = O_loc \ E_loc`. Non-`.conf` files (e.g. `hyprland.conf.bak.<epoch>`) are outside the census by design; N8 pins that.
- **gkeep 13-list — authorized (main, implementation slice).** `LOCAL` becomes the explicit 13-member pin (12 MADO-1 names + `gkeep.conf`). This is a report-only canonical baseline, not endorsement of gkeep's configuration. Derived-expected alternative rejected: it would let the gate agree with whatever the root lists.
- **Detail format.** One line per row (the snapshot refuses multi-line details, `gate-standing-use.md` §3). Use sorted, comma-separated names: `set: missing=[…] extra=[…] dup=[…]`; when the set is equal but order differs: `set equal (18/18); order: line N got '…' want '…'`; clean: `18/18 sources, set equal, order exact` and `13/13 active local confs, set exact`.
- **Row ids unchanged.** Keep `hypr.root.include_graph` and `hypr.local.inventory`. New ids would appear as `appeared` in every snapshot diff and change the 60-row census for no measured gain.

## 3. Named negative cases (hermetic; each a copy of fixture A under the selftest's `mktemp -d /tmp/w5-mado-m52-selftest.*`)

Baseline column = pre-change behaviour by code read [I]; post column = required behaviour after C2 lands. Every case runs `bash tools/mado-verify.sh --root "$X" --no-live` with a hermetic root (no `$HOME` read, live layer skipped).

| id | Mutation on a copy of fixture A | Baseline (pre-C2) | Required post-C2 | Row(s) |
|---|---|---|---|---|
| N1 | delete root line `source = ~/.config/hypr/input.conf` | FAIL, `17 source lines (expected 18)` — unnamed | FAIL, detail contains `missing=[~/.config/hypr/input.conf]` and `extra=[]` | include_graph |
| N2 | append `source = ~/.config/hypr/extra.conf` (= scenario H) | FAIL, `19 source lines (expected 18)` — unnamed | FAIL, detail contains `extra=[~/.config/hypr/extra.conf]`, `missing=[]` | include_graph |
| N3 | append a second `source = ~/.config/hypr/input.conf` | FAIL, count only | FAIL, detail contains `dup=[~/.config/hypr/input.conf]` | include_graph |
| N4 | swap root lines 1 and 2 (set unchanged) | FAIL, `line 1: got … want …` (positional) | FAIL, detail begins `set equal (18/18); order:` and names line 1 | include_graph |
| N5 | remove `$H/gkeep.conf` (scenario B's existing deletion, asserted again by name) | sources_resolve FAIL `unresolved:…gkeep.conf` | unchanged; plus include_graph stays PASS (set of root lines intact) | sources_resolve, include_graph |
| N6 | remove `$H/xdph.conf` | local FAIL `missing: xdph.conf` | FAIL, detail `missing=[xdph.conf]` `extra=[]` | local.inventory |
| N7 | create stray `$H/old-binds.conf` (not in E_loc) | **PASS `12/12`** (set-blind) | FAIL, detail `extra=[old-binds.conf]` | local.inventory |
| N8 | create `$H/hyprland.conf.bak.1792267376` and `$H/notes.txt` (non-`.conf`) | PASS | PASS (control: census is `*.conf` only) | local.inventory |
| N9 | remove `xdph.conf` **and** create `stray.conf` in one run | FAIL `missing: xdph.conf`; stray invisible | FAIL, one row, detail contains both `missing=[xdph.conf]` and `extra=[stray.conf]`, names sorted | local.inventory |
| N10 | clean copy of fixture A (control) | PASS `12/12` (13 files, 12 named) | PASS, `18/18 … set equal` and `13/13 … set exact` | include_graph, local.inventory |

Existing assertions that must still hold: scenario A (`include_graph PASS`), B (`local.inventory FAIL`, `sources_resolve FAIL`, `include_graph PASS (isolation)` — B deletes gkeep and xdph; `include_graph` must stay PASS because root lines are unchanged), H (`include_graph FAIL`), I (boundary proof unaffected), counts-agree checks. The pin check (R10) will move: see §5.

Mutant set the sweep must kill (each new clause needs a covering mutant, `gate-standing-use.md` §5.1): M-a revert include_graph to count-only; M-b drop the `missing=` naming; M-c drop the `extra=` naming; M-d drop the `dup=` naming; M-e remove the order check (N4 must then PASS and fail the mutant); M-f local presence-only (old LOCAL loop) — killed by N7. Each mutant is killed by the named case above; a surviving mutant reads "no test notices this clause", never "the clause is broken".

## 4. Measurement commands (for the main agent after all seats land; not run by this lane)

    cd /home/vgpnk/Projects/shokunin/mado-shokunin
    sha256sum tools/mado-verify.sh && wc -l tools/mado-verify.sh          # record the new sha; old ea798ad0…/3,245 L
    bash tools/mado-verify.sh --selftest; echo "selftest rc=$?"            # expect 0; record N/N before (269/269 at round-12 bytes) and after
    bash tools/mado-verify.sh --no-live; echo "no-live rc=$?"              # file plane on $HOME, read-only; expect local.inventory detail 13/13 exact
    bash tools/mado-verify.sh --regression | grep -E 'MADO_REGRESSION|REGRESSION_TABLE|REGRESSION_RECUT|REGRESSION_TARGET'
    # if SETUP: run the printed REGRESSION_RECUT, update PIN_MADO/TABLE_MADO from the measured table, then re-run:
    bash tools/mado-verify.sh --regression | tail -1                       # expect MADO_REGRESSION: PASS
    find ~/.config/hypr -maxdepth 1 -type f -name '*.conf' -printf '%f\n' | sort   # observed local names only, shape not content
    bash tools/mado-verify.sh --snapshot /tmp/w13-gl/a.snap                  # optional receipt, scratch only
    bash tools/mado-verify.sh --snapshot-diff /tmp/w13-gl/a.snap /tmp/w13-gl/b.snap  # expect SAME apart from the revision scope field

Per-case evidence: the selftest prints only pass/fail counts; the per-case proof is the assertion name (`N1: …` … `N10: …`) appearing in the selftest log when a case fails. Record the count before and after, and the mutant kill table from the `--regression` run.

Reading rules that apply (gate-standing-use §2, §5): a live FAIL is re-run once before filing; a SETUP is not a gate failure (it means the target moved outside the excised pairs and needs the re-cut); `MADO_REGRESSION:` and `MADO_VERIFY:` never mix.

## 5. Expected gate movement (state before landing, so the receipt can be read)

- Gate sha moves (`ea798ad0…` → new). The edited range (:2222-2273) lies **outside** the R7/R8 excised pairs, so `PIN_MADO` stops matching and `--regression` reads SETUP with a printed `REGRESSION_RECUT` (`tools/mado-verify.sh:1546-1550`). Round 12's gkeep re-anchor did the same (`PIN_MADO` → `538d178b…`, `config-drift-r12.md` / lesson). [I from the same pattern; [U] until measured.]
- Selftest count moves up by the number of new assertions (N1–N10 plus the four existing rows' detail checks). Record it; do not predict it in the record.
- Row census unchanged (no new ids), so the snapshot diff of a pre/post pair shows `detail-changed` on the two hypr rows and `DIFF_SCOPE gate-sha256` — no `appeared` or `vanished`. [I]

## 6. Knowledge change record — draft text (to be appended, append-only; nothing edited here)

**LOG.md entry (draft; append at the tail, lane identity in commit):**

    ## 2026-10-20 — Round 13 C2: hypr inventory becomes an exact set census (MadoR13.GateLedger draft)
    - Motivation: lesson round-12 M13 — `hypr.root.include_graph` names counts and positions, not the set delta; `hypr.local.inventory` checks presence of 12 fixed names and PASSes on a stray `*.conf` (baseline [I], measured by N7 after landing).
    - Change (implementer's lane, `tools/mado-verify.sh:2222-2273`): exact comparison; detail names `missing=`, `extra=`, `dup=`; order check retained; LOCAL pinned at 13 with `gkeep.conf`; row ids unchanged.
    - Evidence: selftest cases N1–N10 (see the draft at `.ufo/waves/round-13/w1/GateLedger.md` §3); `--regression` table and REGRESSION_RECUT per §4.
    - Gate: sha `ea798ad0…` (3,245 L) → [pending measure]; PIN_MADO re-cut required.
    - Residuals kept open: toggles glob membership (`~/.local/state/omarchy/toggles/hypr/*.conf`) not censused; non-`.conf` files outside the census by design; the live local set is re-read by name only.

**SOURCES.md row (draft, id S044 — main allocates; append-only; rows are opened before they are added):**

    | S044 | mado gate — exact-set census, `tools/mado-verify.sh:2222-2273` | own-work | A | hypr source and local set census (round 13, C2) | `hypr.root.include_graph` and `hypr.local.inventory` bodies at sha [pending] | Shows which named members a set-blind census would miss (N1–N9) and which control stays clean (N8, N10) | mined | 2026-10-20 | on-gate-change | corpus/knowledge/gate-standing-use.md §6 (to be re-pointed) |

**Errata to append (not edits) — to `corpus/knowledge/config-drift-r12.md` § set-blind limits and `corpus/knowledge/gate-standing-use.md` §6:**
- config-drift-r12.md: "M13 set-blind gap for the hypr plane closed at gate sha [pending]; sources_resolve still iterates EXPECT only (now compared as a set by include_graph); `LOCAL` is now a 13-member pinned census."
- gate-standing-use.md §6: the row "hypr-live … / boundary" stays as is; add a new row "hypr source/local census — closed for the hypr plane at [pending]; toggles glob and non-`.conf` files remain outside the census." Do not rewrite §1–§8; the note is revision-bound history.

## 7. Open decisions and unknowns

- [U] Live `~/.config/hypr/*.conf` count and names as of the landing date (config-drift-r12 recorded 13 on 2026-10-19; not re-read by this lane).
- [U] Operator intent for gkeep persistence (config-drift-r12 routes it as L0). The 13-list is authorized for the implementation slice as a canonical baseline only; if the operator reverts gkeep, the LOCAL pin and EXPECT entry revert together by an appended erratum.
- [I] Exact baseline strings in §3 are from code reading of `tools/mado-verify.sh:2222-2273`; the implementer must confirm each by running the selftest on the pre-change bytes (red) before the post-change run (green).

## 8. Tools

None installed, updated or upgraded by this lane. Operator directive read at `/home/vgpnk/.omp/agent/RULES.md`; no need arose.

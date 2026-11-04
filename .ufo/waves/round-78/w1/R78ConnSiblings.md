# R78ConnSiblings — sibling overlap, record scan, provenance chain

Seat: connector (leaf, read-only). Round 78, wave w1. Lane `mado-shokunin`.
Base `f597eccb` · freeze `b8508bd9` · pre-wave amendment `44a36b64` · tip observed
`90fc8d84` (moving: siblings committed `fa6f3fda`, `93a10a13` while this seat scanned).
Every command below is read-only; no repo file outside this seat's own directory was
written and no git/jj mutation was run.

**Axes named.** A1 *coverage of the evidence chain* — every claim's link resolves at the
revision it names. A2 *operability of the defect classes* — each carried class has a
committed red/green command that discriminates. Round axes touched by implication:
coverage (C1) and operability (C2); no finding requires a predicate, case, label, kill
rule or target change, so neither round axis is harmed.

---

## 1. Sibling overlap — no sibling claims the plane (finding: none)

Swept every `*-shokunin` / `*-shokinin` repo for `layer-shell|gtk-layer-shell|exclusive
zone|reserved band|margined`, for `hyprctl (layers|monitors|getoption|binds|activeworkspace)`,
for a markdown row of the form `| … hyprctl …`, and for `hyprctl` inside sibling
`tools/` scripts. Command forms:

```sh
grep -rIn -E 'hyprctl (layers|monitors|getoption|binds|activeworkspace)|addreserved|exclusive[_ ]zone|layer.shell' \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.ufo <sibling>
grep -rIn -E '^\|.*hyprctl' --include='*.md' --exclude-dir=.ufo --exclude-dir=corpus .
grep -rIn 'hyprctl' --include='*.py' --include='*.sh' --include='*.js' --include='*.mjs' --exclude-dir=.ufo <sibling>
```

Result: **no sibling lane claims the layer-shell plane, waybar margins, the monitor
`reserved` band, or a runbook of `hyprctl` read rows.** Zero `| … hyprctl …` table rows
exist outside `mado-shokunin`. The hits are boundary statements and one shared *verb*:

| file:line | text (abridged) | province it names | disposition |
|---|---|---|---|
| `kotoba-shokunin/PROVINCE.md:72` | "mado owns the Hyprland/waybar/walker/terminal config plane and display behavior read-only; it states no split with kotoba" | kotoba (mado as owner) | no claim; boundary already recorded |
| `tsukuroi-shokunin/PROVINCE.md:124` | `OUT-004 … mado-shokunin/PROVINCE.md @ a4046a821608 … Mado owns the Hyprland, waybar, walker and terminal configuration plane` | tsukuroi (cites mado) | ownership citation, no claim |
| `game-dev-3d-shokunin/reports/round-108/seats/connector.md:16` | "**render regression:** Contested with 2D and desktop compositor … G3D must restrict scope to 3D rendering pipeline/projection, refusing … host compositing" | game-dev-3d | explicit *refusal* of the compositing plane; no claim |
| `game-dev-2d-shokunin/reports/round-79/r79-boundary.md:77,196,202`; `game-dev-2d-shokunin/corpus/live/r79-boundary-exec/run_love_probe.py:42,92` | runs `hyprctl clients -j` to detect whether its own LOVE fixture opened a window ("0 love clients" after runs) | game-dev-2d (own fixture) | shared read *verb*, different question; adjacent, not an overlap |
| `tameshi-shokunin/tools/mutate-and-run.sh:829-840` | `@defect D8 | clause E: hyprland.conf sha pin comparison always "matches"` | tameshi owns the mutation method; mado consumes it read-only (`mado-shokunin/PROVINCE.md:28`) | method dependency, no claim |
| `souji-shokunin/census/round-43/waves/w1/R43connector01/scan-receipts.json:457` | a captured copy of `mado-shokunin/PROVINCE.md` text | none | census artifact, no claim |

Adjacency worth one line in a later record, not a defect: game-dev-2d reads the
compositor's client list live for its own window-presence assertion. It claims no band,
no layer box and no runbook row, so the mado province text stays true as written.

---

## 2. Carried defect classes in the lane's own record

### 2.1 Stale revision citation — present, probe RED

`SCORECARD.md:4416` (round-77 C1 row) cites the measurement as "at `a83e9bee` (its
instrument's last change)". The instrument `tools/mado-barfoot.py` last changed at
`b8508bd9`. The lane's own probe agrees:

```sh
git log -1 --format='%h' -- tools/mado-barfoot.py          # b8508bd9
python3 -I quality/check-cited-revisions.py --repo . --text <row.txt> --path tools/mado-barfoot.py
# CITED-REVISIONS-PROBE: instrument=tools/mado-barfoot.py last_change=b8508bd9b6e7…
# CITED-REVISIONS-PROBE: claim hash=a83e9bee kind=last-change match=no
# CITED-REVISIONS-PROBE: RESULT red claims=1 mismatched=1   (rc 1)
```

Disposition: the row is append-only r77 history, but the parenthetical "its instrument's
last change" is an absolute claim and is now false. The round already has a
`Corrections (round 77, append-only)` block at `SCORECARD.md:4453` that names four later
instrument revisions — the citation at `:4416` was not amended by it. Green test:
the same probe returning `match=yes` (i.e. the citation moved to `b8508bd9`, or the
parenthetical is dropped). Probe selftest observed 6/6.

### 2.2 Registry row describing superseded tool behaviour — present (the r77 `mado-barfoot` row)

`SKILL.md:746` (`mado-r77-barfoot`, a *probe* row, unchanged by round 78) still says:

- `--selftest (18/18)` — measured now: `python3 -I tools/mado-barfoot.py --selftest` →
  `MADO_BARFOOT_SELFTEST: 22/22` (rc 0); the frozen receipt also records `tool_selftest=22/22`.
- exit 3 covers "`UNMODELLED` incl. `reserved=NOT_MODELLED`" — `grep -c NOT_MODELLED
  tools/mado-barfoot.py` → `0`; the r78 tool never emits that class and now emits a
  `DIFFER` reserved class and a `band=`/`expected=` pair.
- the row's exit-3 list omits `NO_BAR`, which the tool emits (`tools/mado-barfoot.py:384`).

Same superseded behaviour is asserted in the present tense in two record rows:

| file:line | text | contradiction |
|---|---|---|
| `corpus/README.md:176` | index row for `bar-footprint-r77.md`: "the margined exclusive zone stays `NOT_MODELLED`" | `corpus/README.md:177` (added at `93a10a13`) says the r78 entry "supersedes the r77 `NOT_MODELLED` margin limit"; the tool composes the margined band |
| `corpus/knowledge/bar-footprint-r77.md:47` | "`tools/mado-barfoot.py` (`VERSION r77-v1`) … `reserved=…|NOT_MODELLED|…`" | the tracked tool is `VERSION = "r78-v1"` (`tools/mado-barfoot.py:56`) |
| `corpus/knowledge/bar-footprint-r77.md:51` | "With any non-zero margin the reserved expectation is `NOT_MODELLED`" | false for the tip tool; the r78 entry's own header declares it superseded |

Red/green: a checker that asserts the registry row's `--selftest` claim equals the
tool's observed count goes red today (18 vs 22) and green when the row is updated. The
index pair is currently *two adjacent rows asserting opposite states of the same
instrument* — a contradiction, not a nuance.

### 2.3 Ledger rows that no longer match the instrument

(a) **The freeze and amendment commits are ledger-RED.** `quality/tool-ledger.md` at
`b8508bd9`/`44a36b64` carries the `tools/mado-barfoot.py` row wrapped across three
physical lines (175-177), so the row has two cells and the instrument is uncovered:

```sh
python3 -I quality/check-tool-ledger.py --repo . --rev b8508bd9
# LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-2-line-172
# LEDGER-ROW reason=uncovered path=tools/mado-barfoot.py detail=no-row
# LEDGER: population=142 ledger_rows=141 uncovered=1 dangling=1 … verdict=TARGET_MISSED  (rc 1)
python3 -I quality/check-tool-ledger.py --repo . --rev 44a36b64   # identical RED
python3 -I quality/check-tool-ledger.py --repo . --rev f597eccb   # 140/140 TARGET_MET (rc 0)
```

Repaired at `fa6f3fda` ("ledger row kept single-line"); at `93a10a13` the gate is
`population=142 ledger_rows=142 … verdict=TARGET_MET` (rc 0). Consequence to state
plainly: **the declaration's frozen revision `44a36b64` is ledger-red.** Both counter
predicates hold there (verified below), but a verifier that re-runs the lane's landing
gates at `44a36b64` gets one red leg.

(b) **Label drift.** `quality/tool-ledger.md:175` (tip and 44a36b64) is labelled
"(round-77 C1)" while its body now describes r78 behaviour ("the reserved band composes
the margined auto zone … `--selftest` 22/22") and cites the r78 declaration. The body is
correct; the round label understates the row. No checker covers it — named, not scored.

(c) `quality/counters/c1-r77-barfoot.py` (row at `:178`) and `c2-r77-runbook.py` (`:179`)
remain accurate: those frozen counters are unchanged and still score 15 and 12 cases.

### 2.4 The C2 anchor leg is a file-wide substring test, not a row binding

`quality/counters/c2-r78-runbook.py:365` tests `case["skill_anchor"] not in skill` over
the whole of `SKILL.md` at `--rev`. Measured on the committed bytes at `44a36b64`:

- 17 cases, 13 distinct anchors; 11 of the 13 occur more than once in `SKILL.md`
  (`hyprctl version` 8×, `makoctl mode` 9×, `omarchy theme current` 9×, `pgrep -a` 7×,
  `hyprctl configerrors` 7×, `omarchy version` 7×, `hyprctl clients -j` 7×,
  `hyprctl monitors` 4×, `hyprctl binds -j` 4×, `hyprctl getoption <key>` 2×,
  `hyprctl layers -j` 2×).
- Deleting the probe-table row `| \`hyprctl version\` | …` from a copy of `SKILL.md`
  leaves 7 occurrences, so `'hyprctl version' in text` stays true: the anchor survives
  removal of the very row it names.

So `anchors=17/17` proves "each anchor string is somewhere in SKILL.md", which is weaker
than the declaration's "bound to their committed `SKILL.md` table rows". Red/green: an
anchor test that requires the anchor inside a table row whose command column carries it
(`^| \`?<anchor>`) goes red on the row-deleted fixture and green on the committed file.
This is a *scoring-claim* weakness, not a probe failure: the 17 executions themselves are
real and matched.

---

## 3. Provenance chain: declaration → counter → control set → receipt

All four pinned instrument hashes resolve at `44a36b64` exactly as declared:

| link | committed at 44a36b64 | sha256 observed | matches pin |
|---|---|---|---|
| `tools/mado-barfoot.py` | yes | `aac5d41b…2009c0` | yes |
| `quality/counters/c1-r78-margins.py` | yes | `1c39a53c…b85000` | yes |
| `quality/counters/c2-r78-runbook.py` | yes | `b9c774b8…8d743a` | yes |
| `controls/c1-cases-r78.json` | yes | `99f1d82f…5a56ae` | yes |
| `controls/c2-runbook-cases-r78.json` | yes | `f1c75a7d…8932e8` | yes |
| `.ufo/waves/round-78/claims-declaration-r78.md` | yes | `78243910…814e7` | n/a |

Links that **do not resolve as written**:

1. **Generator pointers.** The declaration says the case sets are "generated by
   `controls/make-cases-r78.py` (committed beside it)" and `controls/make-runbook-cases-r78.py`.
   No `controls/` directory exists at the lane root at any round-78 revision:
   `git cat-file -e 44a36b64:controls/make-cases-r78.py` → `fatal: path … does not exist`;
   same at `HEAD`. The committed files are
   `.ufo/waves/round-78/controls/make-cases-r78.py` and `…/make-runbook-cases-r78.py`
   (both resolve). Green: the declaration naming the full `.ufo/waves/round-78/controls/…` path.
2. **Fetch directory.** The declaration says the sources were "re-opened this round with
   fresh pinned fetches under `.ufo/waves/round-78/fetch/`". That directory is not in
   `44a36b64` (nor `b8508bd9`); it lands at `fa6f3fda` with 8 files. The files are
   byte-identical to the round-77 copies for the three the round-77 set also carries
   (`S457.bin 9af8a74e…`, `S462.bin 120eb913…`, `S464.bin deef9c81…`) — disclosed as
   "byte-identical to the round-77 copies" in the r78 knowledge entry (line 3). "Fresh"
   here means re-fetched and re-pinned, not different bytes.
3. **Lesson.** The declaration says "the round lesson records the access date and the
   located quotes". No `corpus/lessons/round-78*.md` exists at `44a36b64` or at the tip
   (`ls corpus/lessons | grep -c 78` → `0`). The access-date evidence for the re-opened
   sources therefore has no committed home yet.
4. **Receipt revision label.** The receipts committed at `44a36b64` (and still at the
   tip) record `rev=b8508bd9…`, not `44a36b64`:

   ```sh
   git show 44a36b64:.ufo/waves/round-78/receipts/measurement-c1-r78.txt | tail -1
   # MADO_R78_BARFOOT: … verdict=TARGET_MET rev=b8508bd9b6e7… tool_sha256=aac5d41b…
   ```

   The `44a36b64`-labelled re-runs exist only as uncommitted worktree edits of those two
   receipts. Materially harmless — the tool bytes are `aac5d41b…` at both revisions — but
   the chain link "receipt at 44a36b64" is carried by an uncommitted file.

**The freeze commit is not a TARGET_MET state.** With the freeze commit's own artifacts
(none of them overwritten), both counters miss:

```sh
git show b8508bd9:.ufo/waves/round-78/controls/c1-cases-r78.json > c1-freeze.json   # d19c20e2…
git show b8508bd9:.ufo/waves/round-78/controls/c2-runbook-cases-r78.json > c2-freeze.json  # da3b5b04…
python3 -I quality/counters/c1-r78-margins.py --repo . --rev b8508bd9 \
  --base-rev f597eccb… --controls c1-freeze.json --scratch-root DIR
# MADO_R78_BARFOOT: cases=18 correct=15 mutants=7 killed=7 base_correct=8/18 … verdict=TARGET_MISSED
python3 -I quality/counters/c2-r78-runbook.py --repo . --rev b8508bd9 --controls c2-freeze.json --scratch-root DIR
# MADO_R78_RUNBOOK: … matched=16 shapes=11/12 anchors=17/17 control=5/17 … verdict=TARGET_MISSED
```

Receipts: `w1/R78ConnSiblings/receipt-freeze-controls-c1.txt`, `…-c2.txt` (copied into
this seat's directory). The amendment repaired exactly what the misses name:

- C1: three fixture boxes (`w`/`x` of the live layer entry; 1920→1912/0→4, 3440→3432/0→4
  in three cases). **No expectation moved** — independently re-derived, all 18 expected
  bands follow `height+top+bottom` (horizontal) / `width+left+right` (vertical), with
  negative margins and dynamic cross sizes refused: 18/18 rule-derived, 0 mismatches.
- C2: one churn sample order (`wallpaper,waybar,walker` → `walker,wallpaper,waybar`,
  the sorted form the `sorted_unique` rule demands). The failing probe was
  `layers-namespaces` with live output `wallpaper,waybar` (already sorted) — the *sample*
  was unsorted, not the live value.
- C2 counter: the frozen pin `b9c774b8` is the **amended** counter; the freeze commit's
  bytes are `ceb4f938`. The diff is three mutation anchors re-scoped to occur once, plus
  a `"frozen" not in case` guard in `held_rule` (the control leg). The candidate predicate,
  case labels, kill criteria and target are untouched by that diff.

So the declaration's "predicates, counters, control sets and targets … do not change
after the first measurement" holds only if the *first measurement* is the amended one.
The sentence is literally false for the freeze commit's bytes; the substance (no
predicate/case/label/kill-rule/target change) is confirmed by the diffs above.

---

## 4. Contradictions stated, not smoothed

1. `corpus/README.md:176` ("stays `NOT_MODELLED`") vs `:177` ("supersedes the r77
   `NOT_MODELLED` margin limit") — adjacent index rows, opposite states, same instrument.
2. `SKILL.md:746` (selftest 18/18, `NOT_MODELLED` at exit 3) vs the tracked tool
   (`r78-v1`, 22/22, no `NOT_MODELLED`) — the registry speaks for a tool that no longer exists.
3. `44a36b64` is declared the TARGET_MET amendment and is ledger-red (`check-tool-ledger.py`
   rc 1) while green at `f597eccb` and at `fa6f3fda`+.
4. `anchors=17/17` claims a row binding; the implementation is a file-wide substring test
   that survives deletion of the named row.
5. "fresh pinned fetches under `.ufo/waves/round-78/fetch/`" is true of the bytes of a
   re-fetch, but the directory does not exist at the revision the declaration is frozen at.

---

## 5. Bounds and non-actions

- No file outside `.ufo/waves/round-78/w1/R78ConnSiblings*` was written; no repo, config,
  state or fleet file touched; no git/jj mutation; no socket, no compositor verb.
- Live probes executed were the lane's own read-only selftests (`mado-barfoot --selftest`
  22/22, `c1-r78-margins --selftest` 24/24, `c2-r78-runbook --selftest` 34/34,
  `check-cited-revisions --selftest` 6/6) and the two counter runs above (scratch-rooted,
  read verbs only).
- Tool installs/upgrades: none needed, none performed.
- Scratch `/fast/scratch/hyaku/mado-r78/R78ConnSiblings/` removed after the receipts were
  copied into this seat's directory.

Siblings: no lane claims the layer-shell plane, waybar margins, reserved band or a hyprctl read-row runbook; only a shared read verb (game-dev-2d's `hyprctl clients -j` window probe) and boundary citations.
Record: the r77 `mado-barfoot` registry row (SKILL.md:746) is superseded (18/18→22/22, no `NOT_MODELLED`), the r77 index row (README:176) contradicts the r78 row (README:177), SCORECARD:4416's citation is probe-RED, and `44a36b64` is ledger-RED though its two counters are TARGET_MET.
Chain: all four instrument pins resolve at `44a36b64`; the declaration's `controls/make-*.py` pointers, its fetch directory and its lesson do not, the committed receipts name `b8508bd9`, and the freeze commit's own artifacts score 15/18 and 16/17 (rule-derived expectations unchanged 18/18).

Report: .ufo/waves/round-78/w1/R78ConnSiblings.md

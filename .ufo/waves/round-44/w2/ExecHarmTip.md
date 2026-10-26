# Seat ExecHarmTip — no-harm check: data `e467892` against base `6a1a905` (round 44, w2)

Measured 2026-10-26 in a clone of the lane, every row executed, nothing inferred. Host: Python 3.14.8, GNU bash
5.3.20(1). No host service, compositor, package, network or lane git state was touched; the clone lived under
`/fast/scratch/hyaku/mado-r44/ExecHarmTip/` and was deleted after these receipts were copied here.

Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/mado-shokunin <scratch>/tip.3438`, toplevel verified
before any command (`git rev-parse --show-toplevel` == clone root), then `git -C <clone> checkout -q --detach
e46789213830597348fe96a351ae004d10587385`; `git rev-parse HEAD` = `e4678921…`. The base side is the w1 seat's file
`.ufo/waves/round-44/w1/ExecHarmBase/harm-base.txt` (read in full, base `6a1a905`), which is the assignment's
comparison partner.

**Verdict of this seat: no harm found in the measured surface.** All fifteen base gates have the same exit status at
the data commit; six of them differ in their counts, and every one of the six is the round's declared work (§2). The
only instrument whose bytes changed is `tools/mado-geometry.py`, which is byte-identical to the round's v2 reference
control, and its behaviour differs from the base tool only on inputs that carry a state client (§4). Five
content/citation findings in the landed text are reported for the L1 (§7 F1-F5, one MEDIUM) — citation and
bookkeeping defects, not harm to any green row.

Receipts in this seat directory, all generated in the clone at the data commit:

| file | what it holds |
|---|---|
| `gate-log.txt` | verbatim output + rc of the fifteen base gates at `e467892` (CWD = clone root) |
| `counts-and-digests.txt` | instrument sha256, counts base→data, quality `--selftest` modes, calibration instrument at both revs, ratio tool, pin digests, evidence-audit A/B |
| `tool-differential.txt` (+ `tool-differential/`) | 17-input differential, base tool vs data tool, inputs and outputs kept |
| `diff-audit.txt` | `git diff --numstat/--name-status` outside `.ufo/`, delete-line census, PROVINCE and S164 char-level diffs, frozen-byte check |
| `citations.txt` | every citation on an added line that does not resolve at the data commit, with locators and the introducing commit |

## 1. The fifteen gates, base → data (rc in the last column of each row)

| # | command (CWD = clone root) | base `6a1a905` | data `e467892` | delta |
|---|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | `460/460 assertions passed` rc 0 | same | none |
| 2 | `python3 -I tools/mado-options.py --selftest` | `211/211 passed` rc 0 | same | none |
| 3 | `python3 -I tools/mado-globals.py --selftest` | `63/63 passed` rc 0 | same | none |
| 4 | `python3 -I tools/mado-geometry.py --selftest` | `73/73 passed` rc 0 | `94/94 passed` rc 0 | **+21 assertions — D1 (§2)** |
| 5 | `python3 -I tools/mado-action-plan.py --selftest` | `52/52 passed` rc 0 | same | none |
| 6 | `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` | 20 cases, 20 pass, rc 0 | 20 cases, 20 pass, rc 0 | none |
| 7 | `python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures` | `code:2 FileNotFoundError could-not-evaluate` rc 2 | identical rc 2 | none — base-red, §3 |
| 8 | `python3 -I tools/mado-tripwire.py --selftest …/tripwire/core` | `9/9` rc 0 | same | none |
| 9 | `… --selftest …/tripwire/compound` | `16/16` rc 0 | same | none |
| 10 | `… --selftest …/tripwire/hardening` | `33/33` rc 0 | same | none |
| 11 | `python3 -I quality/check-index.py --rev <rev> --repo .` | `indexed=60/60 … coverage=10.0000/10` rc 0 | `indexed=61/61` rc 0 | **D2** |
| 12 | `python3 -I quality/check-index-rows.py --rev <rev> --repo .` | `rows=60 errors=0 warns=3` rc 0 | `rows=61 errors=0 warns=3` rc 0 | **D3** |
| 13 | `python3 -I quality/check-axis-scores.py --rev <rev> --repo .` | nav 60/60 · calib 68/68 · oper 12/12 `mismatched=0` rc 0 | nav 61/61 · calib 71/71 · oper 12/12 `mismatched=0` rc 0 | **D4, D5** |
| 14 | `python3 -I quality/check-locators.py --selftest` | `cases=18 passed=18 locators=19 miss=6` … `PASS` rc 0 | same, character for character | none |
| 15 | `<fleet>/scripts/sources-census.sh validate --root <fleet> mado` | `mado ok …` rc 0, eight warnings | identical nine lines (§5) | none |

Scope rule carried over from the base seat and re-checked here: of the twelve `tools/*.py|*.sh` files, eight accept a
selftest token; `tools/mado-anims.py`, `mado-binds.py`, `mado-eventq.py`, `mado-wsrules.py` have none. Their sha256 are
unchanged from the base (§4), so nothing was skipped that the base measured.

Supplementary (not in the base set, so no base column): the shipped `--selftest` modes of the four quality scripts are
green at the data commit — `check-index.py` 12/12, `check-index-rows.py` 10/10, `check-axis-scores.py` 18/18,
`check-locators.py` PASS. All four scripts are byte-identical to the base digests in `harm-base.txt` §E.

## 2. Every difference is declared work (the assignment asks each one be named)

| # | difference (base → data) | intended by |
|---|---|---|
| D1 | `mado-geometry.py --selftest` 73/73 → 94/94 | `registration-v2.md` C1: "Reference: `c1/ctl-ref-tool-v2.py.txt` (selftest 94/94)"; the landed tool is byte-identical to that reference (`counts-and-digests.txt`) |
| D2 | `check-index` 60/60 → 61/61 | `registration-v2.md` C2 / assignment: one new knowledge entry `corpus/knowledge/hyprland-gkeep-size-request-r44.md` + its `corpus/README.md:72` index row |
| D3 | `check-index-rows` rows 60 → 61, `errors=0`, the same three `cited-glob-nomatch` warns on the same three rows | same entry; no new warn, no error |
| D4 | axis navigation 60/60 → 61/61 | same entry (the axis re-derives from `check-index --rev`) |
| D5 | axis calibration 68/68 → 71/71 | `corpus/QUALITY.md:411,413,415` — criteria 82-84. Derivation confirmed at both revs with the frozen instrument (`check-axis-scores.py:13,140` uses `.ufo/waves/round-31/c2/count.py`): base `active=68 resolved_active=68`, data `active=71 resolved_active=71`; `SCORECARD.md:2585` republishes `71/71`, so MATCH holds |
| D6 | axis operability 12/12 unchanged | `registration-v2.md` states C1 "does not move" this fraction; it did not |

No gate regressed, no warn was added, no new red appeared. The base-red row (#7) is unchanged, including its cause.

## 3. The one base-red row, unchanged, with its cause re-verified

`tools/mado-evidence-audit.py --selftest` stays rc 2 with `{"error":"FileNotFoundError", … "could-not-evaluate"}` at
the data commit, exactly as at the base. Cause (base §D, re-measured here at data): the round-22 fixture manifest
declares two EMPTY directories as inputs and git cannot store them, so no clone carries them. A/B on the same clone,
changing only those two directories (`counts-and-digests.txt`):

```
$ mkdir -p .ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEscape/root \
           .ufo/waves/round-22/audit/fixtures/cases/AuditRawPathDotDotInternal/root/sub
$ python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures
{"code": 0, "result": "clean", "passed": 46, "total": 46,
 "expected_sha256": "b5df74b5…", "tool_sha256": "277eced2…"}          rc=0
$ git status --porcelain | wc -l     ->  0        (the directories are git-invisible)
```

The two paths are untouched by this round (`diff-audit.txt`, data commit vs freeze v2). This row is therefore not part
of the no-harm comparison and must never be cited as base-green; nothing in this wave changed it.

## 4. Instruments: only the registered tool changed, and only where registered

Digests at the data commit (`counts-and-digests.txt`): eleven of the twelve `tools/*` files and all four quality
checkers carry the exact sha256 that `harm-base.txt` §E records for the base — `mado-verify.sh 050efc72…`,
`mado-options.py 63b5ebd9…`, `mado-globals.py 8db13340…`, `mado-action-plan.py 226220ae…`,
`mado-assessment.py 66aefd03…`, `mado-evidence-audit.py 277eced2…`, `mado-tripwire.py cd9da20c…`,
`mado-anims.py 2beda3f7…`, `mado-binds.py 0cda0e6f…`, `mado-eventq.py 436f550e…`, `mado-wsrules.py dcf5c8c0…`;
`check-index.py 2c8798ce…`, `check-index-rows.py 2fd1c003…`, `check-axis-scores.py 461f913a…`,
`check-locators.py c1ea52ad…`.

The one changed instrument:

```
tools/mado-geometry.py        base e3c2e471…  ->  data 1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4
.ufo/waves/round-44/c1/ctl-ref-tool-v2.py.txt                                  1da3ddaed0d6e3…   (cmp: IDENTICAL)
.ufo/waves/round-44/c1/ctl-ref-tool.py.txt                                     8e871a00…          (round-44 v1, not landed)
```

Behavioural differential of the two tools on 17 inputs (`tool-differential.txt`): **13 byte-identical** (complete
stdout and exit code), including the pinned round-43 host dump (`NO_MATCHING_CLIENT`, rc 3), a TILED-only dump, an
agreeing floating client, a differing floating client, BADSIZE, a fullscreen value that is a string, a float or a
boolean (all read as mode 0, as in round 43), fullscreen 0, an unmapped state client, bad JSON (rc 2), an empty client
list (rc 3), no size rules (rc 4). **4 differ, and every one carries a matched client whose `fullscreen` is 1 or 2** —
e.g. `state-fullscreen`: base `verdict=DIFFER` rc 1 → data `verdict=NOT_COMPARED` rc 5; `state-maximized` the same;
`state-plus-agree` base DIFFER rc 1 → data `… maximized=0 fullscreen=1 verdict=OK` rc 0; `state-plus-agree-plus-differ`
base differ=2 → data differ=1 with ` maximized=1 fullscreen=0`, still rc 1. This is C1's contract exactly
(`registration-v2.md` C1; `SKILL.md:280-289`), and it supports the added claim "byte-identical round-43 output when no
state client matched" (`SCORECARD.md:2579`) and the exit-5 wording of the README Frontier addition
(`corpus/README.md:304-318`).

Pins: all eight files under `.ufo/waves/round-44/fetch*` match `receipts/fetch-sha256.txt` in both digest and byte
count (`counts-and-digests.txt`, `pins verified=8 mismatched=0`).

## 5. Counts, census, and the two append questions

Counts base → data: tools 12 → 12; `corpus/knowledge/*.md` 60 → 61; registry rows 234 → 238 (S298-S301 at
`corpus/SOURCES.md:247-250`, contiguous, no duplicate ids); `corpus/QUALITY.md` numbered criteria 81 → 84
(`QUALITY.md:411,413,415`).

Census: the data run prints the same nine lines as the base, in the same order — seven W04 duplicate-url warnings
(S030, S042, S045, S097, S119, S120, S121), W01 S277, and `mado ok`. Set difference in both directions is empty
(`counts-and-digests.txt`, and the base lines come from `harm-base.txt` §A row 15). The S164 `used-by` extension does
**not** fire a new W01 and does **not** break the census.

### 5a. Is every changed doc outside `.ufo/` append-only except S164's used-by and the tool? — Almost; one more line

`git diff --numstat 6a1a905  e467892 -- . ':!.ufo'` (16 files: 8 modified, 8 new) gives, for the modified ones:

| file | +/− | verdict |
|---|---|---|
| `LOG.md` | +8/−0 | pure append (`## Round 44` block at `LOG.md:2497`) |
| `SCORECARD.md` | +29/−0 | pure append (`## Round 44` section from `SCORECARD.md:2564`) |
| `SKILL.md` | +9/−0 | pure append (rows at `:280-282`, exit-map note and D3 correction at `:286-291`) |
| `corpus/QUALITY.md` | +6/−0 | pure append (criteria 82-84) |
| `corpus/README.md` | +19/−0 | pure append (index row `:72`, Frontier section `:304`) |
| `PROVINCE.md` | +1/−1 | **not a pure append, but no content deleted**: one line changed — line 32, the `tools/mado-geometry.py` row — and the change is an insertion at offset 1070 of that row's own text (1071 → 1332 bytes; `diff-audit.txt` prints the inserted span verbatim, ending `(.ufo/waves/round-44/registration-v2.md)`) |
| `corpus/SOURCES.md` | +5/−1 | the declared case: one row changed (S164; the data line starts with the base bytes and appends `, corpus/knowledge/hyprland-gkeep-size-request-r44.md` to `used-by`; 725 → 778 bytes) plus four new rows |
| `tools/mado-geometry.py` | +84/−12 | the declared C1 rewrite |

The eight new files are pure additions (`considerthese/2026-10-26.md`, the knowledge entry, `corpus/lessons/round-44.md`,
the two v1 and two v2 counters, `quality/ratio-domain-meta.py`). So the precise answer: of the **seven modified docs,
five are strictly append-only** (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`);
`PROVINCE.md` modifies exactly one line by appending inside its cell (zero removed characters); `corpus/SOURCES.md` is
the declared S164 `used-by` extension plus four new rows; and `tools/mado-geometry.py` (not a doc) is the declared
rewrite. No other doc line lost a byte — the only files with a non-zero delete column are those three.

### 5b. The data commit did not touch any frozen round-44 byte

`git diff --name-status 03fa5c61 e467892` (freeze v2 → data) is eleven paths: `tools/mado-geometry.py`, the eight docs
above, the new entry, the new lesson, `quality/ratio-domain-meta.py`, and one added receipt
(`.ufo/waves/round-44/receipts/live-geometry-host-r44.txt`, whose header carries the landed tool's sha256 `1da3dda…`,
matching the tree). `registration.md`/`registration-v2.md`, both v2 counters, `c1/`, `ctl/`, `fetch/`, `fetch-c1/`,
`receipts/ctl-*.txt` and `receipts/fetch-sha256.txt` are byte-untouched by the data commit.

## 6. Claims I could re-execute cheaply, and what they showed

- Criterion 82's re-runnable count reproduces at the data tree: `python3 -I quality/ratio-domain-meta.py --repo . --rev
  e467892… --from 34 --to 43` prints `DOMAIN_META: domain=12 meta=5 window=34-43 default=1`, exactly the line
  `SCORECARD.md:2583` claims. Extending the window to the round's own rows gives `domain=14 meta=5 window=34-44
  default=1` (both round-44 claim rows classify `domain`; the one `default=` row is round-36 C2, clause 7).
- The five `GATE` quotes in `corpus/lessons/round-44.md:31-35` are each present in their pinned receipt at the stated
  locator: S164 `Window.cpp:1687`, S298 `XDGShell.cpp:455`, S299 `xdg-shell.xml:1150-1151` (two-line quote, as the
  lesson says), S300 `gdktoplevel-wayland.c:681`, S301 `gkeep-ui.py:475-476` (two-line quote). Pinned sha256 prefixes
  match `fetch-sha256.txt`.
- All 59 line ranges that the added lines cite against pinned `fetch*/` files are inside their files
  (out-of-range: 0), and the anchors the `corpus/README.md:72` row names resolve to the claimed code:
  `sendWindowSize` at `Hyprland-Window.cpp:1732`, `realToReportSize()` at `:1741`, the X11
  `m_xwaylandSurface->configure(...)` at `:1751`, `onAck` with the pending-ack erasure at `:1514-1521`,
  `CXDGToplevelResource::setSize` at `Hyprland-XDGShell.cpp:354-357`, and the deferred
  `scheduleConfigure`/`configure`/`sendConfigure` at `:629-643`. The five locators the lesson attributes to the
  counter's `quote_at` (`Window.cpp:1687`, `XDGShell.cpp:455`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:681`,
  `gkeep-ui.py:475`) each land on the quoted text.
- SKILL's FULLSCREEN/MAXIMIZED rows ("monitor box", "work area", "the floating box is remembered") match
  `fetch-c1/Hyprland-FullscreenHandler.cpp`: `rememberFloatingSize` at `:131`, `setPositionGlobal(MONBOX)` at `:194`,
  `setPositionGlobal(WORKAREA)` at `:198`; the cited `fetch-c1/Hyprland-HyprCtl.cpp:431` is indeed
  `…getFullscreenModes(w).internal` (`.client` is `:432`), so "only the compositor's internal mode decides" is what
  the pin shows.
- The D3 TILED correction appended to `SKILL.md:288-291` is consistent with the lane's own convention
  (`corpus/QUALITY.md:345`: "corrections land as new rows, never rewrites") — the TILED row itself is untouched, the
  correction is an added note, and the correction's pin (`fetch/Hyprland-Window.cpp:2402-2408`, the rule `size` →
  `setPseudoSize` path, `setPseudoSize` at `:2408`) exists in the tree at the data commit.

## 7. Findings (content, for the L1 — not no-harm regressions)

None of these moves a gate; all were found by comparing the added lines with the tree they landed in.

**F1 — MEDIUM: criterion 83 lands with a check command whose checker is one commit in the future.**
`corpus/QUALITY.md:413` (criterion 83, new in this data commit) says, in its own words, that a path which first appears
in a later commit is `LATE`, and gives the check command
`python3 -I .ufo/waves/round-44/w1/ScrQualityCriteria/check83.py --repo . --rev <REV> --doc <PATH-IN-REPO> --prefix .ufo/`.
At `e467892` that path does not exist:
`git cat-file -e e467892:.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py` fails; `git log --diff-filter=A --all --
<path>` names only `290cddea` (the after-data commit). The criterion therefore cannot be checked at the revision it
landed at, by its own rule. Suggested exact correction (L1's call): append to the check sentence — "the checker lands
with the w1 evidence in the commit after this round's data (`290cddea`); at the data commit it is `LATE` itself."
Reproduce: `git cat-file -e e467892:.ufo/waves/round-44/w1/ScrQualityCriteria/check83.py` → rc 1.

**F2 — LOW/MEDIUM: 23 `w1/` citations, `w1-results.json` and six round receipts on added lines do not resolve at the
data commit; all but three of them appear one commit later.** `citations.txt` lists them with locators. Two classes:

- *one-commit lag* (first added by `290cddea`): 23 distinct `w1/…` paths (`corpus/lessons/round-44.md:7,27,93,165,168,
  181,182,183,189,251,258,263,266`; `LOG.md:2501`; `SCORECARD.md:2566,2573`; `QUALITY.md:415`) and
  `receipts/c1-after-data.txt` (`SCORECARD.md:2570`, `corpus/lessons/round-44.md:232`),
  `receipts/c2-after-data.txt` (`SCORECARD.md:2571`, `corpus/lessons/round-44.md:233,240`),
  `receipts/census-after-data.txt` (`corpus/lessons/round-44.md:87`). Under criterion 83 these are `LATE` at data. The
  round's intent is visible (w1 evidence and the after-data receipts are committed next), and the shortest correction
  is a scope word where each class is first used, e.g. `SCORECARD.md:2570` cell → "-> see `receipts/c1-after-data.txt`
  (committed with the after-data records, one commit after this one)". Reproduce: `git cat-file -e e467892:<path>`.
- *nowhere* (no commit adds them): `receipts/axis-tip.txt` (`corpus/lessons/round-44.md:176`),
  `receipts/c1-after-tip.txt` (same file `:232`), `receipts/c2-after-tip.txt` (`:233`). See F3. The two `c1-demo`
  citations (`corpus/lessons/round-44.md:227,246`) resolve only under `w1/ScrLessonSkeleton/`; see F5.

**F3 — LOW: three tip receipts are promised by name and no commit adds them; the axis one has a landed sibling under a
different name.** `corpus/lessons/round-44.md:174-176` (M44-7's fix) says the round "commits an axis receipt at the base
(`receipts/axis-base.txt`, three MATCH rows) and at the tip (`receipts/axis-tip.txt`, committed with the round's last
commit)". `axis-base.txt` exists at data (verified: three MATCH rows, `rev=6a1a905…`); `axis-tip.txt` exists in no
commit, and at the round's current head `290cddea` the committed axis receipt is `receipts/axis-data.txt`
(`MADO_AXIS` over the data tree), not `axis-tip.txt`. Suggested exact correction: "… and at the tip
(`receipts/axis-tip.txt`, to be committed with the round's last commit; the data-tree axis receipt committed after the
data commit is `receipts/axis-data.txt`)". Same shape at `:232` and `:233` for `c1-after-tip.txt` /
`c2-after-tip.txt` (the after-data receipts exist; the after-tip ones are still to be written). Reproduce:
`git log --diff-filter=A --all -- .ufo/waves/round-44/receipts/axis-tip.txt` → empty;
`git ls-tree --name-only 290cddea .ufo/waves/round-44/receipts/` → `axis-data.txt`, no `axis-tip.txt`.

**F4 — LOW: the new tool's own usage lines name a file that does not exist.** `quality/ratio-domain-meta.py:43,44`
print `python3 -I ratio.py …` and `:72` says "see ratio.py docstring", while the landed path is
`quality/ratio-domain-meta.py` (and `corpus/QUALITY.md:411` invokes the real path). Exact correction: replace `ratio.py`
with `quality/ratio-domain-meta.py` on lines 43, 44 and 72. Reproduce: `grep -n 'ratio\.py' quality/ratio-domain-meta.py`.
(The tool itself is correct: it ran and reproduced the SCORECARD line, §6.)

**F5 — INFO: one re-run instruction resolves only through a w1 directory.** `corpus/lessons/round-44.md:227` says
"re-run `c1-demo/commands.txt`"; read as round-dir-relative it is nowhere, but `corpus/lessons/round-44.md:246` names
the citable copy `w1/ScrLessonSkeleton/c1-demo/`, which exists at `290cddea` (and not at data). No correction needed if
the L1 reads `:227` as relative to `w1/ScrLessonSkeleton/`; a pointer word there would remove the ambiguity.

### Differences that are NOT findings (checked so nobody has to re-check them)

- `fixtures=11/26` (v2, `receipts/c1-v2-before-base.txt`, and `SCORECARD.md:2570`) vs `fixtures=12/26` (v1,
  `receipts/c1-before-base.txt`, quoted at `corpus/lessons/round-44.md:231`): both receipts are committed, they are two
  different counters at the same base, `registration-v2.md` says the lattice share "varies with the nonce, the verdict
  does not". Both lines end `verdict=TARGET_MISSED … exit=1`, as claimed.
- `PROVINCE.md` +1/−1: in-cell append, zero removed bytes (§5a).
- `SKILL.md`'s appended D3 correction sits after the verdict table because the lane corrects by adding rows, never by
  rewriting (`corpus/QUALITY.md:345`).
- `mado-assessment.py`'s 20 cases and `mado-action-plan.py`'s 52/52 are unchanged; both scripts are byte-identical to
  base.
- `check-index-rows`' three warns are round-12/24 path globs that match no file; they are the base's warns on the base's
  rows, not new.

## 8. Limits

- This seat ran the gates, not the two counters or the v2 controls (`w2` has separate seats for C1/C2 re-runs and the
  controls). Nothing here scores `fixtures=26/26` or `admitted=1/1`.
- No compositor or host read was made: this is a clone baseline; the live run is
  `receipts/live-geometry-host-r44.txt`, read but not re-executed.
- "No harm" is bounded by 15 gates + 4 supplementary selftests + 17 differential inputs + the citation/locator checks
  above. Content truth of the entry's sentences is the non-author reading's job; this seat verified that the quoted
  text is where the entry says it is, not that the sentence draws the only possible conclusion.
- The two empty fixture directories were created in the clone only (for the §3 A/B); they are invisible to git and the
  clone was deleted.

## 9. What this seat wrote

Only `mado-shokunin/.ufo/waves/round-44/w2/ExecHarmTip/` — this report, `gate-log.txt`, `counts-and-digests.txt`,
`tool-differential.txt` (+ `tool-differential/` inputs and outputs), `diff-audit.txt`, `citations.txt`. No tracked file
was edited, no git/jj mutating command ran in the lane or the fleet, no package tool was run (no installs were
needed), and the scratch directory `/fast/scratch/hyaku/mado-r44/ExecHarmTip/` is deleted.

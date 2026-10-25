# Round 35 verifier spot-check — mado

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25
reviewer identity: `ClosureMado35` (fresh hyaku subagent; not the mado L1; no subagents dispatched; no tool installs)
lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`
lane base before the round: `6d754bd599caa7ab21c4c20b548c0fa83914ffce`
lane tip at closure: `7a068cbee3b0983230b8fb8467c02e12772832dd` (`master`, pushed, `ahead=0`)
round-35 freeze: `19e4ab3171c1540c40d6b12097745af98053b07d`
round-35 data commit: `02088b4dff0da153df30ff174611d1257c92d0cd`
round-35 errata commit: `4f35c80`
report: fleet `.ufo/reports/round-35/mado.md`, last commit `763734e1b909218e87d1192c1b236b2b575b7ea1`
prompt: fleet `.ufo/prompts/mado-round-35.md`

Dispatch digest (mutable `.ufo/watchdog.log`, copied here as the durable pointer):
`2026-10-24T23:14:38-03:00 launch mado round=35 pgid=29506 driver=hyaku-inline attempt=1`;
`2026-10-25T03:23:08-03:00 lane-dead-no-report mado round=35; retry same round (attempt-1 orphan — no report, session died ~23:30)`;
`2026-10-25T03:23:38-03:00 launch mado round=35 pgid=1756809 driver=hyaku-inline attempt=2`;
`2026-10-25T03:53:57-03:00 complete mado round=35; hyaku-inline attempt=2`.

Method note. The lane's counters (`c1/count.py`, `c2/count.py`), its index/axis gates and
`tools/mado-verify.sh` were **not executed** (PROTOCOL §Gate standard, Closure consequence). Their
committed transcripts were read, and every number that can be re-derived by a plain measurement
(`git show`, `grep`, `wc`, `sha256sum`, `python3 -c` over committed bytes, `sources-census.sh`) was
re-measured from `git archive` clean extractions or `git show` blobs — never from the lane working
copy, which moved under this pass (see defect D2). The only file written in the lane is this one.

## Step-1 conformance

- **Report committed by the lane identity.** `git log --format='%an <%ae> %H %ad' --date=iso --
  .ufo/reports/round-35/mado.md` → nine commits, all `mado-shokunin <mado@shokunin.local>`, the last
  `763734e1b909218e87d1192c1b236b2b575b7ea1 2026-10-25 03:53:03 -0300`; each commit touches only the
  report (`git show --stat` → `1 file changed`). PASS.
- **Not a marker.** Work performed, Landed changes, Before → after measurements, Sources & frontier,
  Trend verdicts and a `SHONEN` section are all present, with resolvable paths, commands and hashes.
  Status `ok`; defects below are status-neutral.
- **`SHONEN` heading.** `## SHONEN` carries four `[~]` lines, one per box, each with a pointer;
  `grep -c '\[x\]' SHONEN.md` → `0` in the lane repo. PASS as a report heading. Every box remains
  author-asserted, so **no box is promotion-checkable from this round** (promotion is operator-owned;
  not exercised here).
- **Cited lane hashes exist and are ancestors of the branch.** All eleven cited hashes
  (`19e4ab3`, `02088b4`, `4f35c80`, `7b745a1`, `4efaf63`, `b632f0b`, `ca870e9`, `1bb25c7`,
  `dff3941`, `6d754bd`, `fa7ba113`) pass `git cat-file -e <h>^{commit}` and
  `git merge-base --is-ancestor <h> master` → 11/11 `ancestor=yes`. PASS.
- **Pushed, but not clean.** `scripts/hyaku/jj-lane.sh state mado-shokunin` →
  `branch=master local=7a068cbee3b0983230b8fb8467c02e12772832dd remote=7a068cbee3b0983230b8fb8467c02e12772832dd ahead=0 behind=0 head=detached tracked=8 untracked=2`;
  `git ls-remote origin refs/heads/master` → `7a068cb…`. Push PASS. Cleanliness **FAIL**: eight
  modified and two untracked round-35 paths stood in the tree at closure, with mtimes
  `03:53:59`–`04:00:00` — i.e. after the driver's `complete` line at `03:53:57` (defect D2).
- **Prompt fidelity.** `.ufo/prompts/mado-round-35.md` (481 lines) is the `templates/round-prompt.md`
  rendering (114 of 116 non-blank template lines verbatim after `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/
  `{{AXES}}` substitution; the two differences are my crude substitution of `<N>`, not prompt drift)
  plus hyaku addendum §6. The embed clause holds: MISSION/AXES binding (L5–6), the 1–3-claims rule
  (L9–41), the frontier step (L42–79), the L2 floor of **at least 8 subagents in ONE batched call**
  (L80–98, matching `MISSION.md` §L2 concurrency L55–56), report path and filename (L101), report
  sections and the `SHONEN` rule (L118), the marker rule (L122), commit-then-push (L133–134), push
  scope (L135), the L0 side channel (L139), the lane write scope (L262) and "the report lands last
  and cites the pushed lane hash" (L328). No L2 route map is quoted, so there is none to mismatch. PASS.
- **Report-lands-last and tip citation.** The report's last commit is `03:53:03`, but the lane kept
  committing until `7a068cb` at `03:53:37` (`567945e`, `2eddc38`, `7a068cb`), and the report declines
  to name the tip hash — its own commit `af1e1ca5` is titled "closure tip named by command, not by a
  moving hash" and the text reads "the tip named by `git rev-parse master` at read time". **FAIL**
  against "written only after the lane's child-repo work is committed" and "must cite that commit's
  hash" (defect D1). The report remains real, not a marker: it names real committed round-work hashes.
- **Wave policy.** `w1-taskcall.json` → `counts {spawn:64,resume:0,total:64}`, 64 tasks, role census
  scout 12 / executor 13 / reviewer 11 / critic 8 / scribe 7 / connector 4 / mutation-tester 3 /
  sentinel 2 / revenger 2 / simplifier 2 — exactly the reported mix; its policy block declares
  `waveMinLanes 64 / waveMaxLanes 128` (policy v2, inside v1's 32–64 band at 64).
  `w2-taskcall.json` → 40 tasks, reviewer 21 / executor 3 / mutation-tester 3 / critic 3 / sentinel 2 /
  revenger 2 / scout 2 / scribe 2 / simplifier 1 / connector 1 — exactly as reported.
  Neither call carries a `model` field (role map routes; the seat plan's `@m_*` column is
  informational), so no model pin is passed. PASS.
- **Report counts that resolve.** `w1/reports` = 64 `.md` + `swarm-registry.json`;
  `w2/reports` = 40 `.md` at the tip (37 at `4f35c80` and `7b745a1`, which is why the Work-performed
  bullet still says "38 reports" — defect D7); `.ufo/waves/round-35/controls/` = 11 receipts plus
  `golden.txt`; `scratch-evidence/` = 261 files in 59 seat dirs at `1bb25c7` (as the landed-changes
  row claims) and 524 at the tip.
- **Prompt durability / scope.** The driver prompt was committed by the lane identity
  (`01d79d84`, `cca52393`) rather than with the integration commit. The bytes are durable, so no
  evidence is lost; recorded as a minor scope note, not a defect.

## Claims — re-checked by this pass

### C1 — coverage, the idle-lock control surface

Re-measured (plain measurements over committed bytes):

```
git show 19e4ab3:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'   -> 192
git show 02088b4:corpus/SOURCES.md | grep -cE …                                    -> 200
git show 7a068cb:corpus/SOURCES.md | grep -cE …                                    -> 200
git ls-tree --name-only 19e4ab3 corpus/knowledge/ | wc -l                          -> 47
git ls-tree --name-only 02088b4 corpus/knowledge/ | wc -l                          -> 50
git ls-tree --name-only 7a068cb corpus/knowledge/ | wc -l                          -> 50
git show 19e4ab3:corpus/SOURCES.md | grep -cE 'S2(0[3-9]|10)'                      -> 0
ls corpus/knowledge/idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md  -> 3 files
git show 7a068cb:corpus/SOURCES.md | sed -n '205,212p'                             -> S203…S210, 11 cells each
```

- Eight fetch receipts exist; each hashes to its frozen digest —
  `python3 -c` over `.ufo/waves/round-35/c1/frozen.json` → `S203…S210 match` 8/8
  (sizes 3137/445/1194/929/705/768/905/385 B).
- All eight `gate-quote:` lines are contiguous substrings of their receipt bytes and inside the
  ≤25-word bound: word counts `14/13/17/13/15/14/13/15`, `contiguous=True` for 8/8.
- `corpus/SOURCES.md` over `19e4ab3..7a068cb` is additions only: eight `+| S203`…`+| S210` lines and
  zero deletion lines among old ids → "rows touched old→new: 0" holds.
- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit **0** with the
  same seven `W04` lines (S030, S042, S045, S097, S119, S120, S121). The before-state was
  re-measured too, on a clean `git archive 19e4ab3` mirror at `/tmp/fleet-mirror/mado-shokunin` →
  exit **0**, same seven `W04`, at 192 rows.
- Counter *not* executed. Its committed claims were read instead: the predicate and target match the
  frozen spec, and the defect the round reports is real in the committed code —
  `grep -n digest .ufo/waves/round-35/c1/count.py` → `174:            digest = hashlib.sha256(blob).hexdigest() …`,
  and the accepting conjunct is `receipt["sha256"] in cs[5]` (the spec digest in the anchor cell), so
  the computed digest is a dead store. The pre-data `golden` fixture differs from the shipped
  registry — `diff` of the eight rows → `1,8c1,8` — so the control never exercises the live bytes.

**C1 verdict: re-measured and verified — coverage `improved`**, with the instrument defects routed
(D3, D4). The claim's substance (three admitted entries, eight sourced rows) does not rest on the
shape-scored counter: it reproduces from the registry and entries directly.

### C2 — calibration, the lane's own evidence ledger

The claim's own report already rules it **not admitted**; I am the named non-author reviewer for that
ruling and I confirm the falsification structurally, from the committed counter and the git history:

- `uncovered` iterates the ledger's own `live` list (`c2/count.py:88–101`), so deleting a clause and
  its control removes it from the scan — fail-open on deletion, as reported.
- A "covered" clause only needs `MISSED = re.compile(r"verdict=TARGET_MISSED")` to match anywhere in a
  receipt file (`c2/count.py:32`, `:99–100`) — token greps, as reported.
- `ledger_tip_ok` is `spec["r34_tip"] in text` over a prose document plus `git rev-parse
  <tip>:<path>` blob ids (`c2/count.py:113–131`): a document that keeps the round-34 stale label
  (`fa7ba113`) *and* names `dff3941` passes, because nothing parses the document's own tip label.
- The pinned round-34 tip is disputed: `git log -1 --format='%ct' dff3941` → 1792892809,
  `6d754bd` → 1792893866 (1057 s = **17m37s**); `6d754bd` is titled "round-34 verifier spot-check
  (integrator, hyaku)" and is the last round-34-labelled commit, while `c2/frozen.json` pins
  `r34_tip: dff3941…`.
- The before-state is consistent rather than executed: `git ls-tree dff3941 -- .ufo/waves/round-35`
  → 0 entries, so `error=clause-ledger-missing` exit 2 is the only possible outcome of that counter
  at that revision.
- Ledger facts re-read: `c1/clauses.json` → 10 live clauses, one `not-load-bearing`
  (`o-nofollow-open`), one retired (`r34-word-bound-1-25`), 9 with control receipts — matching the
  report's "nine controlled live clauses, one declared, one retired".

**C2 verdict: `unprovable`.** The counter prints what its predicate says, but its four observables
are self-authored shape checks; the claimed improvement in the lane's evidence discipline is not
established. This is not `unprovable-but-better`: the round demonstrates the instrument is vacuous,
not better.

### No axis harmed

- `git diff 6d754bd 7a068cb -- SCORECARD.md` → `1 file changed, 71 insertions(+)`, **zero
  deletions**: no published axis score or row was lowered, and the round-35 rows are appended.
- Independent index completeness check (my own, not the lane's gate): 50 files under
  `corpus/knowledge/`, **0** missing from `corpus/README.md`.
- The lane's own gate evidence was evidence-verified, not executed: `w2/reports/RevSelftest.md`
  carries `MADO_SELFTEST: 460/460 assertions passed`, `RevIndex.md` carries
  `MADO_INDEX: rev=a80f8cb… indexed=50/50 missing=0 dangling=0 duplicates=0`, and the axis-gate
  transcripts in `w2/reports/CritAxisClaims.md` show `mismatched=2` at `02088b4` and at `335e0f8`
  and `mismatched=0` at the round-34 tip. The report discloses the ~15-minute stale window rather
  than hiding it. No committed transcript prints the **tip** revision `7a068cb` at
  `mismatched=0`; the tip match is carried by the seat prose in `RevScorecard.md` (defect D10, low).

## Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| `S206` — host waybar configuration | admit | `/home/vgpnk/.config/waybar/config.jsonc:207-208` (host, read-only) and `corpus/SOURCES.md:208` | **agree** | Line 207 is `"custom/idle-indicator": {` and line 208 is `"on-click": "omarchy-toggle-idle"`, exactly as the quote states; the gate-quote is 13 words and a contiguous substring of the committed receipt. Row is own-work/A/mined with `used-by` = the one admitting entry. |
| `S203` — omarchy first-run installer | admit | `/home/vgpnk/.local/share/omarchy/bin/omarchy-first-run` (sha256 `20508471…` = the committed receipt's hash) | **agree** | Twelve `bash …/install/first-run/*.sh` invocations (L13–22, 26–27) plus one hook install; `install/first-run/` holds 12 `.sh` + 1 `.hook`; `grep -c idle` → 0. The quote ("lists 12 scripts; … runs all 12; none is idle-lock") is true, 14 words. |
| `S210` — toggle-state directory | admit | `/home/vgpnk/.local/state/omarchy/toggles/hypr` (host) | **agree** | `ls` → `flags.conf`, `window-no-gaps.conf` (2 files); `grep -rl idle` → 0. Quote true, 15 words, and the receipt's own listing matches. |
| `chinese-article-revision-r30.md` (package knowledge) | refuse | `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/chinese-article-revision-r30.md` (read-only, outside the fleet root) | **agree** | The entry is Chinese-wikitext revision/bookkeeping ("§ footer 检索自", a snapshot revision id) — a documentation-localization surface, not the config plane `PROVINCE.md:3–10` owns. The refusal is consistent with the same rule applied in rounds 33–34. Note for the lane: earlier entries of that class exist (`chinese-wiki-canonical-url-r28.md`, `zh-wiki-snapshot-semantics-r29.md`), so the boundary ruling should be stated once and applied both ways (see D9's sibling concern). |
| staged row `S203` (package registry) | refuse | `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md:7` | **agree** | The staged `S203` is "Hyprland IPC page — current upstream source — raw.githubusercontent.com/hyprwm/hyprland-wiki/…/content/ipc/_index.md", so the refusal reason ("compositor-IPC document with no claim over it") and the id-collision note (package S203 ≠ lane S203) both hold on the bytes. |

Gate coverage of the admits: all eight new rows' quotes were re-derived programmatically (8/8
contiguous, ≤25 words), and three admits were re-opened by hand as above. Three of three sampled
decisions agree; two of two sampled refusals agree.

Census conformance re-run: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
mado` → exit 0, seven `W04`, `mado ok`.

## Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | **improved** | C1 verified by re-measurement: registry 192 → 200, notes 47 → 50, three entries and eight rows present at the tip, eight receipts hash-matched, quotes contiguous; a surface that previously carried only scattered file-byte mentions now has measured ground. |
| depth | **improved** | The three new entries separate observation/inference/unknown (`OBS`/`INF`/`UNK` counts 3/1/1, 3/1/2, 6/2/1), each with located quotes and provenance fields; criteria 55 and 56 were added to `corpus/QUALITY.md` from this round's instrument findings. |
| freshness | **improved** | All eight receipts re-hashed by this pass 8/8 against the frozen digests; entries carry `verified-at: 2026-10-24`; the r34 `RevFrozenBlobs` label defect was re-issued at `ledger/RevFrozenBlobs-r35.md` (with the tip dispute routed, D4). |
| operability | unchanged | No tool, checklist or suite change this round; `tools/mado-verify.sh` blob byte-identical to the round-34 tip per the committed transcript (evidence-verified, not executed). |
| calibration | **unprovable** | C2's instrument is falsified against itself; the published axis row was not lowered, but the improvement the claim asserts is not established. |
| adjacency | improved | The register slice was re-derived (13 data rows) and `ConnOverlap`'s sibling sweep is corroborated by my own bounded sweep: the only fleet-wide hits for `omarchy-toggle-idle|omarchy-first-run|hypridle` outside mado are mirrors of mado's own `PROVINCE.md`, a `mutate-and-run.sh` category list, a frida process dump and census paths — no sibling `PROVINCE.md` claims the ground. Nothing absorbed. |

## Trend verdicts

- **expansion: improved.** Three net-new admitted `knowledge/` entries on ground the coverage map did
  not hold, each `source:` citing a `mined` own-work tier-A row (S203–S210, opened 2026-10-24,
  `used-by` exactly the admitting entry), and the registry grew 192 → 200 with an additions-only
  append. Bounded: the consumer half of the idle-lock offer only; transitions, lock success,
  hyprlock config, rendered pixels and the operator's preference stay open.
- **quality: improved.** No admitted entry is left false or stale: the ten in-round errata bullets
  (r12 E1–E3, r14 E1–E2, r15 E1–E5) narrow or withdraw claims and are append-only; the three row
  cell corrections (`git diff --numstat 02088b4 7a068cb -- corpus/SOURCES.md` → `3 3` over S203,
  S204, S205) are corrections, not rewrites; the eight receipts re-verify 8/8. The round's weak
  object is the instrument, and it is routed, not hidden.
- **discernment: improved.** The gate admitted eight documents and refused 139 staged rows / 66
  knowledge items with named reasons and flips; my spot-check agrees on every sampled decision
  (3 admits, 2 refusals), and the round's own seats' disagreements became lesson rows M35-1…M35-4
  and criteria 55/56 rather than being left unlearned. The lane also declined the capability row it
  could not honestly demonstrate.

## Routed defects — the lane must fix these next round

- **D1 — report-lands-last and tip citation (round report).** The report's last commit (`763734e1`,
  03:53:03) precedes `567945e`, `2eddc38` and the tip `7a068cb` (03:53:13–03:53:37), and the report
  declines to name a lane tip hash ("the tip named by `rev-parse master` at read time"). Report files
  are append-only: land an erratum in the round-36 report naming `7a068cb…` as the round-35 tip, and
  in future write the report after the last lane commit and cite that hash.
- **D2 — uncommitted round work at closure (durability debt).** `jj-lane.sh state` at closure →
  `tracked=8 untracked=2`; eight modified `.ufo/waves/round-35/w2/reports/*` +
  `scratch-evidence/RevEntryR12/evidence.txt` and two untracked
  `.ufo/waves/round-35/scratch/RevQuoteS20{3,5}/count_probe.py`, mtimes `03:53:59`–`04:00:00` — seat
  writers still active after the driver's `complete` line. Resolve under the round-36 entry (commit
  by entry or revert) and name the disposition in `LOG.md`.
- **D3 — C1 counter is shape-scored (instrument).** `c1/count.py:174` computes the receipt digest and
  never reads it; `controls-content/c1-shape-only` and `c1-fabricated-payload` reach `TARGET_MET`.
  A one-line repair (`and digest == receipt["sha256"]`) is proven at
  `scratch-evidence/L1DigestFix/count-fixed.py`; bind it, and adopt the two content cribs as
  committed controls (criterion 55).
- **D4 — C2 observables are fail-open (instrument).** `uncovered` scans the ledger's own clause list,
  covered-receipts are `verdict=TARGET_MISSED` token greps, and `ledger_tip_ok` is a substring test
  over a prose document; the pinned `r34_tip` (`dff3941`) is not the last round-34-labelled commit
  (`6d754bd`, 17m37s later, identical blob ids). Parse the ledger's own table, bind clause receipts
  to clause ids, pin one tip definition (criterion 56).
- **D5 — dangling evidence pointers in `LOG.md`.** The round-35 entry cites
  `.ufo/waves/round-35/scratch/SimplifyCounter/` and `.../scratch/MutC1Drop/mutants/`, both absent at
  the tip; the content is at `scratch-evidence/SimplifyCounter/count-min.py` and
  `scratch-evidence/MutC1Drop/{gen_and_run.py,results.json}`. Append a LOG correction naming the
  superseded paths (evidence standard: a pointer must resolve at closure).
- **D6 — wrong correction count in the report's Sources & frontier.** "four of the new rows'
  `scope`/`teaches` cells were corrected" → committed bytes show **three** rows (S203, S204, S205)
  and the corrected cells include `recheck` (`git diff --numstat 02088b4 7a068cb --
  corpus/SOURCES.md` → `3 3`). SCORECARD already carries the corrected figure; the report needs the
  matching erratum.
- **D7 — stale seat-report count.** The Work-performed bullet says `.ufo/waves/round-35/w2/reports/`
  holds "(38 reports)"; the commits hold 37 `.md` at `4f35c80`/`7b745a1` and 40 at the tip (the same
  report's later sentence says 40). Say which revision each count describes.
- **D8 — cleanup claim vs committed bytes.** "no scratch tree left in the lane" does not hold: 124
  tracked paths (2.2 MB) under `.ufo/waves/round-35/scratch/` (`RevC1Tip/m1–m9`, `headtree2`,
  `tree`) exist at the tip, added by `7d708cf` (8969 lines) after `ae34886` ("no scratch tree
  left"); the "3.2 GB" figure cannot be re-derived now. Either commit a stated disposition for that
  subtree or correct the claim.
- **D9 — new entries do not open with the provenance trio (corpus form).** CORPUS.md requires
  `source:`/`verified-at:`/`recheck:` first; the three new entries carry them at lines 7–13 after the
  title and lane paragraph. Normalize the convention (the corpus is mixed — `idle-lock-route-r17.md`
  opens with the trio, `waybar-walker-semantics.md` does not) and apply it both ways, including the
  refusal boundary for documentation-localization material (see the spot-check note on the r28/r29
  entries).
- **D10 — tip-revision axis transcript (low).** The report's axis line quotes
  `MADO_AXIS: checked=3 mismatched=0 rev=7b745a1d…` under a `--rev master` command; no committed
  transcript prints the closure tip `7a068cb` at `mismatched=0` (the tip match is seat prose). Commit
  a tip-revision axis/index transcript with the round-36 evidence.

## Closure summary

- Lane-round status: **ok** (a real report with real committed work; defects D1, D5, D8 are
  conformance/evidence defects, not marker predicates).
- Claims: C1 **improved** (re-measured), C2 **unprovable** (falsified against its own instrument;
  `rejected-honest-stop` at the round level).
- Trends: expansion `improved`, quality `improved`, discernment `improved`.
- No axis harmed: `SCORECARD.md` diff is 71 insertions / 0 deletions; index 50/50 by an independent
  count; suite 460/460 by committed transcript.

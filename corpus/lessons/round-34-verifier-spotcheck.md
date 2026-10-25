# Round 34 verifier spot-check — mado

author: hyaku closure (non-author integrator, @m_swe)
date: 2026-10-24
reviewer identity: `Kimi fresh closure agent` (fresh, non-author; not the @m_swe session; no subagents dispatched; no tool installs)
lane tip measured: `dff394109f3cc3d851309ad7c67dd3b35b46adf2` (`master`, pushed)
lane base before the round: `fefdefd4cca6adfd847826f1e406f7aa712007d3`
round-34 freeze: `3420e827bd7b21b1374b23245526554ffd20d096`
round-34 data commit: `fa7ba11346116672352b5d41494141c5c4d738d0`
round-34 wave-evidence commit: `57622b8453f5ca6eb720dfbd1bc6b3285ec2a818`
report: fleet `66c370b57cc7596883d556d8dd616960cd4a6180`

Clean checkouts were used for every measurement (`git archive <rev> | tar -x` into
`/tmp/mado-r34-verify/{freeze,tip}`), so no measurement touched the lane working
copy. The lane working copy was read only; the only file written there is this
one. The lane's axis gate was **not** executed (PROTOCOL §Gate standard,
Closure consequence); its committed transcript was read instead.

## Step-1 conformance

- Report committed by lane identity:
  `git log --format='%an %ae %H %s' -- .ufo/reports/round-34/mado.md` →
  `mado-shokunin mado@shokunin.local 66c370b57cc7596883d556d8dd616960cd4a6180
  round-34: mado report`. The commit is an ancestor of the fleet `master`.
  Porcelain on that path is empty. **Not a marker**: Work performed, Landed
  changes, Before → after measurements, Sources & frontier, Trend verdicts and
  SHONEN are all present with resolvable hashes and commands. Status `ok`.
- `SHONEN` heading carries four `[~]` lines, one per box, each with a pointer.
  PASS as a report heading. Every box is author-asserted, so **no box is
  promotion-checkable** — noted for the operator; promotion is operator-owned
  and was not exercised.
- Cited lane hashes all exist and are ancestors of `master`:
  `fefdefd4` (base), `3420e827` (freeze), `fa7ba113` (data), `57622b84` (wave
  evidence), `dff3941` (tip), plus `d40b35f9`, `9a46ccf3`, `69f72100`,
  `15ddd7d`, `a0dd664`, `274f735`. Every round commit carries
  `mado-shokunin <mado@shokunin.local>`; the base commit carries
  `protocol-shokunin` (the round-33 integrator spot-check). PASS.
- Pushed and clean: `jj-lane.sh state` → `branch=master
  local=dff394109f3cc3d851309ad7c67dd3b35b46adf2
  remote=dff394109f3cc3d851309ad7c67dd3b35b46adf2 ahead=0 behind=0 head=detached
  tracked=0 untracked=0`; `git ls-remote origin refs/heads/master` →
  `dff394109f3cc3d851309ad7c67dd3b35b46adf2`; `git status --porcelain` is empty
  and `untracked=0`. PASS on push and on leftovers.
- Prompt `.ufo/prompts/mado-round-34.md` (478 lines) carries the round contract:
  MISSION/AXES binding and the 1–3-claims rule (L5–L13), the L2 floor of at
  least 8 subagents in ONE batched call (L82), commit-then-push and push scope
  (L131–L136), the L0 side channel (L138), the report path and filename
  (L101), the evidence-pointer and commit-hash citation rules (L106–L110), the
  `SHONEN` heading requirement (L118), the lane write scope (L259) and
  "the report lands last and cites the pushed lane hash" (L325). PASS.
- Dispatch digest (mutable `.ufo/watchdog.log`, copied here):
  `2026-10-24T21:40:56-03:00 launch mado round=34 pgid=3166550 driver=hyaku-inline
  attempt=1` (log line 1224); `2026-10-24T22:55:29-03:00 complete mado
  round=34; hyaku-inline attempt=1` (log line 1233). Matches the closure prompt.

## Claims — re-measured by the closure agent

### C1 — coverage (the Waybar event-socket client route)

Counter: `python3 -I .ufo/waves/round-34/c1/count.py --root <root> --frozen
.ufo/waves/round-34/c1/frozen.json`. The counter and its frozen spec are
byte-identical at the freeze and at the tip (blobs `49089c186fb75f1bd2cc4c45c0161282ea6e8a46`
/ `0bfe0d866c4e9a2d17da297a11dae389150b488b`), and `git diff 3420e827 dff3941 --
.ufo/waves/round-34/c1 .ufo/waves/round-34/c2` is empty — the predicates were
not touched after the freeze.

| Root | Observed | Exit | Expected | Verdict |
|---|---|---|---|---|
| freeze `3420e827` | `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 | miss | PASS |
| tip `dff3941` | `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | 0 | met | PASS |
| lane working copy (tip) | `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | 0 | met | PASS |
| `controls/symlink-crib` | `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` | 1 | miss | PASS |
| `controls/symlink-entry` | same | 1 | miss | PASS |
| `controls/extra/symlink-parent` | same | 1 | miss | PASS |
| `controls/extra/symlink-sources` | same | 1 | miss | PASS |
| `controls/extra/used-by-prefix` | same | 1 | miss | PASS |
| `controls/entries-only` | same | 1 | miss | PASS |
| `controls/rows-only` | same | 1 | miss | PASS |
| `controls/golden` (regular files) | `closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET` | 0 | met | PASS |

Two controls are committed only as receipts (`controls/c1-donothing.txt`,
`controls/c1-hardlink.txt`); both were rebuilt in scratch by the closure agent
and re-run:

- Do-nothing (golden tree minus the entry and minus rows S201/S202):
  `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` exit 1.
  Matches the committed receipt.
- Hardlink (`nlink=2` on the entry file, the lane's own variant):
  `closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED` exit 1,
  `nlink=2` — byte-identical to `controls/c1-hardlink.txt`. A second variant
  with the hardlink on the *fetch* (`nlink=2` on `S201.bin`) also misses:
  `closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED` exit 1.
  Either way the clause bites.

The round-33 counter was **not** substituted for the frozen one:
`python3 -I .ufo/waves/round-33/c1/count.py --root
.ufo/waves/round-33/controls/golden --frozen .ufo/waves/round-33/c1/frozen.json`
→ `PRED-C1-r33-v1 closed_entries=2 closed_rows=4 open_cites=0 verdict=TARGET_MET`
exit 0, matching `controls/r33-counter-on-its-crib.txt`.

Supporting counts re-derived: registry rows 190 at the freeze → 192 at the tip
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); the
SCORECARD's own frozen navigation fence gives `indexed=46/46` at the base
`fefdefd4` and `indexed=47/47` at `fa7ba113` and at the tip. The two rows
landed **after** the freeze, in `fa7ba113` (`git show --stat fa7ba113` →
`corpus/SOURCES.md | 2 ++`, `corpus/knowledge/waybar-module-text-route-r25.md |
27 ++`, `corpus/README.md | 1 +`, `SCORECARD.md | 4 +++`).

**C1 verdict: the claim verifies — coverage `improved`.**

### C2 — calibration (the published S189 queue-cap line number)

Counter: `python3 -I .ufo/waves/round-34/c2/count.py --repo <repo> --scorecard
<card> --frozen .ufo/waves/round-34/c2/frozen.json`.

| Card / repo | Observed | Exit | Expected | Verdict |
|---|---|---|---|---|
| freeze `3420e827` (no publication) | `published=absent measured=169 mismatch=1 verdict=TARGET_MISSED` | 1 | miss | PASS |
| tip `dff3941` | `published=169 measured=169 mismatch=0 verdict=TARGET_MET` | 0 | met | PASS |
| lane working copy (tip) | `published=169 measured=169 mismatch=0 verdict=TARGET_MET` | 0 | met | PASS |
| `controls/c2-junk-card.md` (last marker tail `line=128`) | `published=128 measured=169 mismatch=1 verdict=TARGET_MISSED` | 1 | miss | PASS |
| marker-less card (the freeze `SCORECARD.md` used as a card) | `published=absent measured=169 mismatch=1 verdict=TARGET_MISSED` | 1 | miss | PASS |
| `controls/c2-reachable-card.md` | `published=169 measured=169 mismatch=0 verdict=TARGET_MET` | 0 | met | PASS |

Independent re-read of the pinned fetch: `.ufo/waves/round-32/fetch/S189.bin`
is 6479 B, `nlink=1`, sha256
`eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` (matches the
frozen spec). Line 128 is
`auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
and line 169 is `const size_t MAX_QUEUED_EVENTS = 64;`. The published marker
line in the tip `SCORECARD.md` is `r34-s189-line: line=169` (line 2108).

**C2 verdict: the claim verifies — calibration `improved`.**

### Round-33 counters — not amended

Re-verified at the round's real tip (`dff3941`), not at the commit the seat
report used:

| Path | r33 freeze `9a46ccf3` | r33 tip `69f72100` | tip `dff3941` | identical |
|---|---|---|---|---|
| `.ufo/waves/round-33/c1/count.py` | `4ab3db435d` | `4ab3db435d` | `4ab3db435d` | YES |
| `.ufo/waves/round-33/c1/frozen.json` | `60d1094baa` | `60d1094baa` | `60d1094baa` | YES |
| `.ufo/waves/round-33/c2/count.py` | `df563528e7` | `df563528e7` | `df563528e7` | YES |

Full blob ids at the tip: `4ab3db435dd2e396402d1d83039e35082f1138fe`,
`60d1094baa2992294533bae37e0990ae23077609`,
`df563528e725951b447ef31b324ec4b7d264e91b`. Each of the three paths has exactly
one commit in `git log master -- <path>` (the r33 freeze), and the r34 frozen
counter paths likewise have exactly one commit each (the r34 freeze). No
amendment, no write-then-revert. PROVEN.

### Wave reconciliation (from the committed registries)

- One batched call: `w1-taskcall.json` carries `counts {spawn:64, resume:0,
  total:64}`, `resumeSends: []` and exactly one `taskCall` object with 64
  `tasks` — one wave, one call. The policy band in the taskCall is
  `waveMinLanes 64 / waveMaxLanes 128`, matching
  `scripts/hyaku/ufo-wave-policy-v2.json`.
- Seats: `w1/seat-plan.tsv` has 64 data rows (no header) and its seat set is
  **identical** to the manifest's 64 seats (`diff` of the two sorted sets is
  empty).
- Settled: `w1/exit-codes.tsv` has 64 rows, every exit code `0`.
  `w1/manifest.json` → `seats: 64, finished: 64, reports_written: 64, dead: [],
  missing: [], no_report: []`. `w1/dispatch.out` prints
  `dispatcher: 64/64 finished; reports=64; dead=[] missing=[] no_report=[]`.
- Reports: `w1/reports/` holds 65 files — the 64 seat reports, whose names are
  **exactly** the manifest seat set, plus `swarm-registry.json`. 64 reports, not
  65.
- Roles (manifest, 64 rows): executor 14, scout 12, reviewer 10, critic 8,
  scribe 7, connector 4, mutation-tester 3, sentinel 2, revenger 2,
  simplifier 2. Attack roles (reviewer + critic + mutation-tester + revenger +
  sentinel) = **25 of 64 = 39%** — matches the report.
- Model routing (manifest, 64 rows): `@m_zfl` 21, `@m_sol` 20, `@m_flash` 19,
  `@m_grok` 4 — matches the report.
- Parent blocked on `wait`: `dispatch-w1.sh` launches every seat as a background
  job and then calls bare `wait` before writing the manifest. PASS.

### Item 10 (assimilation) — as claimed

- Two Waybar event-socket rows admitted after the freeze: `S201` and `S202` at
  `corpus/SOURCES.md:203-204`, added in `fa7ba113` (after the freeze). Both
  tier `A`, kind `code`, status `mined`, opened `2026-10-24`, `recheck 90d`,
  `used-by` = `corpus/knowledge/waybar-module-text-route-r25.md` (the single
  whole-token path).
- Registry hygiene: 192 rows, `NF != 13` count 0, duplicate ids none, enum
  violations none, mined rows with a non-existent `used-by` path none.
- `corpus/SOURCES.md` diff base→tip: **2 added lines, 0 deleted lines** — no
  existing row's `status`, `recheck` or `used-by` was changed, as claimed.
- Quarantine: `assimilation/quarantine-slice` holds **13** rows; the lesson
  refuses **12** (S195, S205, S228, the register's S201, S224, S199, S200,
  S209, S222, S223, S225, S235) and hand-checks the 13th (the register's S189,
  IN-REGISTRY-SAME-ID with a false-negative `payload-absent` mark). 12 of 13
  refused — as claimed.
- No renumber: the live registry jumps `S196 → S201`; `S197`–`S200` are absent
  from `corpus/SOURCES.md` (grep over `S195`–`S209` returns only S196, S201,
  S202). The register speaks the campaign's pre-remap staging ids, and the lane
  renumbered nothing. As claimed.
- Collision guard re-proved: `reg-ids` 190 ids vs `staged-ids` 140 ids,
  `collisions` empty; `controls/indented-guard.txt` records
  `spaced=S197 column_zero='' collisions='S197'` — the 0–3-leading-space
  extractor does bite on the indented `  | S002 |` fixture, where the
  column-zero-only extractor does not.

### The inherited 19 paths (r33 closure debt)

The r33 closure named 19 untracked paths: 6 control fixture trees, 12 seat
scratch trees and `scratch/ExecK2Receipts`. Disposition re-checked at the tip:

- 18 committed: `controls/{entries-only,extra-source,golden,hash-mismatch,junk,rows-only}/`
  and `scratch/{CriticC1FalseNeg,ExecAppendDraft,ExecCollision,MutC1Counter,ReviewC2Predicate,ReviewRound30,ScoutConsider,ScoutQuarantine,ScoutS189Quote,ScoutS190,ScoutS191,ScoutS197}/`
  are all tracked at `dff3941` (1–16 files each), every one added by
  `57622b84`. PASS.
- `ExecK2Receipts` is **not** tracked at the tip (`git ls-tree` returns 0
  paths) and is absent from the lane working copy — it was never committed, so
  nothing was deleted from history. It now lives at
  `/fast/scratch/mado-r33-k2-receipts/ExecK2Receipts` and measures
  **`du -sb` = 495,961,904 B and 30,892 files** — byte-for-byte and
  file-for-file identical to the pre-move figure the r33 closure recorded.
  `ORIGIN.md` (1521 B) names the origin path, the move date, the size, the
  three throwaway clones inside it, why it left the lane tree, and the
  re-verification evidence. **The move did not sweep bytes silently** — it
  preserved them and documented the disposition. PASS.

### The r33 lesson correction — an append, not a rewrite

`git log master -- corpus/lessons/round-33.md` shows two commits: the r33
correction `d40b35f9` and the r34 tip `dff3941`. The r34 diff on that file is
**26 insertions, 0 deletions** — an appended
`## Correction (appended 2026-10-24, round 34)` block naming line 128 (the
`formatEvent` assignment, the span the absent-defect register quotes for its
`S189` row) and line 169 (`const size_t MAX_QUEUED_EVENTS = 64;`, the queue-cap
constant). Both numbers are correct for their own quote; the earlier defect was
the ambiguity, not a false line. The lesson body above the append is untouched.
PASS.

### L0 side channel

Commit `ae2c52b82018904ad891c304ba023c846a19bd8e` (lane identity) adds
**3 lines, 0 deletions** to the fleet `.ufo/l0-questions.md`, all three rows
prefixed `mado | round-34 |`. Per this closure's scope they are **not answered
and not duplicated**; they are routed to the operator.

## Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| `S201` — Waybar Hyprland IPC backend | admit | committed blob `.ufo/waves/round-34/fetch/S201.bin` (6550 B, `nlink=1`, sha256 `799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e`) and the live registry row `corpus/SOURCES.md:203` | **agree** | Line 38 reads `spdlog::warn("$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr");`; the row's quote is a contiguous substring of the blob (grep hit 1) and is 8 words, inside the ≤25-word bound. The digest equals the frozen spec's. The row is 13 fields, tier `A`, kind `code`, status `mined`, `recheck 90d`, and `used-by` names exactly the admitted entry as a whole token. |
| `S202` — Waybar Hyprland window module | admit | committed blob `.ufo/waves/round-34/fetch/S202.bin` (8324 B, `nlink=1`, sha256 `5df496eb3cfe5cae4506d7aa10c6bb54eb0a0b28d9489dcf19dd68ba570c9846`) and `corpus/SOURCES.md:204` | **agree** | Line 27 reads `m_ipc.registerForIPC("activewindow", this);`; contiguous substring (grep hit 1), 2 words, digest matches the frozen spec, `used-by` names the same single entry. |
| `two-literature-drift-r26.md` (the r33 routed defect 3) | reject | staged `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/two-literature-drift-r26.md` (5670 B, read-only outside the fleet root) | **agree** | Its `source:` block declares exactly S206, S209, S210, S211; the whole-file id histogram is S190 (1, an internal cross-reference), S206 (6), S209 (3), S210 (2), S211 (2); `S199` occurs **0** times. S210 and S211 are CSDN blog posts (`blog.csdn.net`), i.e. kind `community`, tier C, never sole support. The subject is ArchWiki translation lag, a localization surface `PROVINCE.md` does not claim ("desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host"). The reject stands on both grounds and the restated ids are right — the lane's restatement is correct and the stale `S199` is gone. |
| the register's `S201` (id-space) | reject / no renumber | `assimilation/quarantine-slice`, `reg-ids` (190), `staged-ids` (140), `collisions` (0), `assimilation/collisions` | **agree** | The live registry holds S196 then S201/S202 with S197–S200 unallocated, so the lane's `S201` is unambiguous and nothing was renumbered; the register speaks the campaign's pre-remap staging ids. The collision guard is re-proved able to fail on the indented fixture. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
mado` → exit **0**, `mado ok` plus the seven pre-existing `W04` duplicate-url
warnings (S030, S042, S045, S097, S119, S120, S121) — the same seven the
report pasted, unchanged.

## Axis verdicts

| Axis | Verdict | Evidence re-derived by the closure agent |
|---|---|---|
| coverage | **improved** | C1 met on the frozen counter at the tip and missed at the freeze; registry 190 → 192; navigation 46/46 → 47/47 under the SCORECARD's own frozen fence. |
| calibration | **improved** | C2 met on the frozen counter (`published=169 measured=169 mismatch=0`), missed before publication and on both `line=128` and marker-less cards. |
| depth | unchanged | No new domain-knowledge entry beyond the one coverage entry; the SCORECARD axis rows were not lowered. |
| operability | unchanged | The lane's gate is unchanged; the r34 axis-gate transcript (`controls/axis-selftest.txt`, `MADO_AXIS_SELFTEST: 18/18 assertions passed` exit 0; live `MADO_AXIS: checked=3 mismatched=0 rev=fa7ba113` exit 0) was **evidence-verified, not executed** (PROTOCOL §Gate standard, Closure consequence). |
| freshness | unchanged | No live source re-verification was claimed or performed this round. |
| adjacency | unchanged | PROVINCE.md untouched; no sibling lane's surface absorbed (`Corpus/README.md` and `CritProvince`/`ConnSibling` agree). |

**No axis is harmed.** `git diff fefdefd4 dff3941 -- SCORECARD.md` is
**53 insertions, 0 deletions** — no axis row was lowered, no score was moved
down. The one correction the round makes to its own published text (the
"operability selftest 12/12" → the gate selftest's 18/18) is an appended
correction; the axis table itself is unchanged.

## Trend verdicts

- **expansion: improved.** One net-new admitted knowledge entry
  (`corpus/knowledge/waybar-module-text-route-r25.md`) on ground the coverage
  map did not hold — absent at the freeze, present at the tip, and indexed
  (navigation 46/46 → 47/47) — each of its two citations a `mined` tier-A
  registry row (S201, S202) that the closure agent re-opened from the committed
  bytes; plus one new capability row in the SCORECARD capabilities table,
  demonstrated running in this round by the counter re-runs above. Bounded:
  frontier item U7 stays open, and this round documents the route to the
  module text, not the rendered module text.
- **quality: unchanged.** No weaker entry was superseded by a stronger one,
  and no stale entry was re-verified against a live source — the S189 evidence
  was re-read from committed bytes, which is calibration work. The agreement
  with the lane here is deliberate: the r33 closure's `quality: improved` was
  itself an overclaim, and this round does not repeat it. No admitted entry
  failed its re-check.
- **discernment: improved.** Every defect the r33 closure routed was either
  repaired (the literature reject restated against the file's real ids; the
  scratch trees disposed by re-verification with named dispositions; the
  round-30 report citation; the axis-gate selftest transcript committed) or,
  in the S189 case, re-verified against the pinned bytes and turned into an
  appended lesson. No disagreement was left unlearned.

## Routed defects — the lane must fix these next round

1. **Dead clause in the frozen counter.** The `1 <= len(words) <= 25` clause in
   `PRED-C1-r34-v1` cannot fail once `found == quote` holds, so it is
   provably dead code under its own frozen spec. The round says so honestly
   and the round-34 lesson records it; it is still a defect in a counter that
   is presented as load-bearing. Next round it must be retired or given a
   failing case in the next frozen spec.
2. **`S_ISLNK`/`O_NOFOLLOW` pair is TOCTOU-only.** It cannot kill any static
   tree. Also recorded honestly; it must be either justified as TOCTOU
   protection in the counter's own header or dropped, not counted as a
   demonstrated load-bearing clause.
3. **`RevFrozenBlobs.md` names the wrong tip.** The seat report's table is
   measured at `fa7ba113`, which it calls "lane tip"; the round's tip is
   `dff3941`. The closure agent re-verified all seven frozen blobs at
   `dff3941` and they are identical, so the conclusion (PROVEN, not amended)
   stands — but the artifact's own label is stale by one commit and should be
   re-issued with the real tip.
4. **Merge package id remap is stale** — operator/campaign side, not the
   lane's. The package's frozen remap base ("registry ends at S196") is now
   stale (the lane registry ends at S202) and it repeats the lane's S186–S189
   URLs as S199/S200/S260. Filed as L0 (`ae2c52b8`), unanswered here.
5. **The three L0 questions remain open** (id remap; the r33 routed defect 2
   on the S189 line number, which does not survive re-verification as stated;
   and the inherited working-tree debt). They are operator-owned and were not
   answered, corrected or duplicated by this closure.

Status-neutral notes, recorded not blocked: the round's census "before"
measurement (22:10) is a past observation that cannot be re-executed; the
closure agent re-ran the census at the tip and got exit 0. The hardlink
control's committed receipt (`closed_rows=0 open_cites=2`) corresponds to a
hardlink on the *entry* file; a hardlink on the *fetch* yields
`closed_rows=1 open_cites=1` — both miss, so the clause is load-bearing either
way.

## Closure note for the operator

No `SHONEN` box is promotion-checkable this round: all four remain `[~]`
author-asserted, and a seat the lane dispatched is still the lane (PROTOCOL
§Promotion gates). The boxes look reviewable by an outside reviewer — box 1
points at a decision-table corpus with cited sources, box 3 at executable
instructions — but the promotion decision is operator-owned and was not
exercised here.

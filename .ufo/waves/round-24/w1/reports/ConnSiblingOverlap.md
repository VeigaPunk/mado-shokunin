# ConnSiblingOverlap — round 24 (mado), wave 1

**Seat** `MadoR24.ConnSiblingOverlap` (connector, leaf; no dispatch, no git/jj write, no commit).
**Target** `/home/vgpnk/Projects/shokunin/mado-shokunin` (read-only) and the 20 sibling lanes under
`/home/vgpnk/Projects/shokunin/*-shokunin` (read-only).
**Round base** `8e5d9369` (registration). **Lane HEAD at scan** `81955bd` (commits are landing during
the wave; every lane pin below is the live byte read at scan time, not a committed pin of mine).
**Scan window** 2026-10-23T03:42–04:02Z.
**Status** report-only: no sibling file edited, no sibling gate run, no host verb issued, no network
fetch, no tool installed or updated. The only file written is this report.

---

## Axes named

| Axis | This seat's contribution | Direction |
|---|---|---|
| **adjacency** | Name who owns the three surfaces round 24 moves (rule attribution, `hyprctl`, capability re-demonstration), with `path:line`, and split "report" from "absorb". | primary |
| **calibration** | Distinguish *mado's* capability table from tameshi's method/ledger and from the operator-side fleet census; name the live sibling bytes a C2 receipt actually executes. | companion, improves |
| **coverage** | C1's new note stays inside mado's province; no sibling claims the hyprwm source surface. | neutral |
| **operability / freshness / depth** | No live probe, no gate run, no host read. | neutral |

---

## 1. Method and sweeps (exact commands, run from `/home/vgpnk/Projects/shokunin`)

Every count below is a command plus its output. No `git`/`jj` write verb was issued anywhere; the
only git uses were the lane's own `rev-parse` and read-only `git log` on tameshi's harness history.

```text
S1  scope-surface citations of the pinned upstream, outside mado:
    grep -rIlm1 'hyprwm' --include='*.md' --include='*.py' --include='*.sh' --include='*.json' \
      */corpus */SKILL.md */PROVINCE.md */README.md 2>/dev/null | grep -v '^mado-shokunin' | wc -l
    → 0

S2  rule-topic notes outside mado:
    grep -rIl -i -e 'windowrule' -e 'layerrule' -e 'window rule' -e 'layer rule' \
      --include='*.md' */corpus */SKILL.md */PROVINCE.md 2>/dev/null | grep -v '^mado-shokunin'
    → (no output; 0 files)

S3  lanes naming Hyprland on a scope surface:
    grep -rIn -i 'hyprland' */PROVINCE.md */SKILL.md */SCORECARD.md 2>/dev/null | grep -v '^mado-shokunin'
    → tsukuroi-shokunin/PROVINCE.md:124  (an inbound ownership locator quoting mado's own PROVINCE;
                                          the only line)

S4  other consumers of tameshi's mutation runner:
    grep -rIn 'mutate-and-run.sh' --include='*.md' --include='*.sh' --include='*.py' \
      */corpus */SKILL.md */PROVINCE.md */tools 2>/dev/null \
      | grep -v -e '^mado-shokunin' -e '^tameshi-shokunin'
    → tsukuroi-shokunin/corpus/knowledge/closeout-r11.md:337,352
      tsukuroi-shokunin/corpus/knowledge/memory-arm-mutants-s8.md:23,82
      tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:189,195,208
      tsukuroi-shokunin/SKILL.md:568
      tsukuroi-shokunin/tools/tsukuroi-census.sh:2235

S5  lanes naming the fleet source census script on a scope surface:
    grep -rIn 'scripts/sources-census.sh' --include='PROVINCE.md' --include='SKILL.md' */ 2>/dev/null \
      | grep -v '^mado-shokunin' | wc -l
    → 0

S6  capability-table convention outside mado (tables of their own, not a shared one):
    grep -rIl -e 'Capability status' -e 'capability table' --include='*.md' --include='*.py' \
      */corpus */SKILL.md */PROVINCE.md */SCORECARD.md 2>/dev/null | grep -v '^mado-shokunin'
    → chousa-shokunin/corpus/lessons/round-24.md
      kake-shokunin/corpus/lessons/round-28-verifier-spotcheck.md
      kotoba-shokunin/corpus/knowledge/instruction-surface-remeasure-round13.md
      kotoba-shokunin/corpus/knowledge/instruction-surface-census-round13.md
      kagi-shokunin/SCORECARD.md · kaidoku-shokunin/SCORECARD.md
      kumitate-shokunin/SCORECARD.md · tsukuroi-shokunin/SCORECARD.md

S7  hyprctl outside mado:
    grep -n 'hyprctl' */PROVINCE.md */SKILL.md */SCORECARD.md 2>/dev/null | grep -v '^mado-shokunin'
    → (no output; 0 hits)
    grep -rIl 'hyprctl' --include='*.md' --include='*.py' --include='*.sh' */corpus 2>/dev/null \
      | grep -v '^mado-shokunin'
    → game-dev-2d-shokunin/corpus/live/r79-boundary-exec/run_love_probe.py
      tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md
```

Live digests taken at scan (not pins of this report; both are sibling-owned files that can move):

```text
sha256sum tameshi-shokunin/tools/mutate-and-run.sh
  → fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de
sha256sum scripts/sources-census.sh
  → 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30
grep -n 'HARNESS_SHA_RECORDED' mado-shokunin/tools/mado-verify.sh
  → 2032:HARNESS_SHA_RECORDED='b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb'
```

---

## 2. Ownership map for the round's three surfaces

### 2.1 Hyprland window/layer rule *attribution* (C1) — **not contested**

**Observed.** mado's province is "desktop & compositor craft — the Hyprland/waybar/walker
configuration plane and display behavior" (`mado-shokunin/PROVINCE.md:3`), owning "`~/.config/hypr/`
(hyprland.conf, keybinds, rules, animations)" (`:6`). Siblings route *into* that ownership and
none claim it:

- tsukuroi's ADJ-03 locator quotes mado's own province verbatim and concludes "Mado owns the
  Hyprland, waybar, walker and terminal configuration plane" (`tsukuroi-shokunin/PROVINCE.md:124`).
- game-dev-3d's round-108 connector names "render regression" as "Contested with 2D and desktop
  compositor", cites `mado-shokunin/PROVINCE.md:3-4`, and requires G3D to refuse "host compositing"
  (`game-dev-3d-shokunin/reports/round-108/seats/connector.md:16`).
- kotoba's fleet-wide sibling census classifies mado `none` (no split on kotoba's scope surfaces) at
  `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md:82`, retained in
  `kotoba-shokunin/PROVINCE.md:57`.

**Sweeps.** S1 `0` scope-surface citations of `hyprwm` outside mado; S2 `0` rule-topic corpus/SKILL/
PROVINCE files outside mado; S3 one inbound line only. The hyprwm tag/commit pins C1 uses are
unclaimed territory: no sibling publishes hyprwm source bytes, so C1 adds ground rather than
crossing a sibling's.

**Naming collisions, not scope contests.** "Attribution" is a busy word in the fleet and each sense
is a different surface:

| Sense | Owner | Anchor |
|---|---|---|
| documentation-authority attribution ("a rule attributed to an authority carries a located quote") | kotoba | `kotoba-shokunin/corpus/QUALITY.md:34` (Q23) |
| declarer attribution of `getoption` values ("last declarer wins") | mado, separate note | `corpus/knowledge/hyprctl-verification-layer.md:251-253` |
| blind shim-cascade leg attribution (model eval) | kengaku | `kengaku-shokunin/corpus/knowledge/attribution-interval-calibration.md` |
| kernel OOM line attribution | mori | `mori-shokunin/corpus/knowledge/kernel-oom-line-attribution-r12.md` |
| stream attribution (engine) | game-dev-2d/3d | `game-dev-2d-shokunin/corpus/lessons/r19-stream-attribution.md` |

C1's note title uses the window-rule sense. The note should say so in its own limits, or a fleet
reader will read kotoba's Q23 as a competing claim on the same words. No sibling has to be asked.

**What the bytes do not establish.** S1 is a scope-surface sweep (`corpus/`, `SKILL.md`,
`PROVINCE.md`, `README.md`); it does not prove no sibling *report* quotes hyprwm. The phrase "window
rules … layer rules" does appear in kotoba's verifier fixtures, but as captured skill-description
data: `kotoba-shokunin/verifiers/fixtures/compare-harness-independent/record-map-24-composition/live.json:46`
quotes the omarchy skill's `description` text. That is an instrument input, not a lane scope claim.
Reading upstream C++ at a tag is not "reverse engineering of shipped artifacts" in
kaidoku/revenger's sense (`kaidoku-shokunin/PROVINCE.md:3-5`: native ELF, Electron/ASAR, archives);
no REA lane is crossed by C1.

### 2.2 `hyprctl` — **mado owns the declared read-verb plane; one sibling uses it as an instrument**

**Observed.** mado's gate reads "`hyprctl` read verbs only (version, instances, configerrors,
getoption, binds, monitors, layers)" (`mado-shokunin/PROVINCE.md:28`, round-23 inventory row for
`tools/mado-verify.sh`; verb list unchanged by round 24). No sibling lists `hyprctl` on a scope
surface (S7: 0 hits). One sibling *calls* it as an observation instrument: game-dev-2d's live boundary probe
runs `["hyprctl", "clients", "-j"]` and filters for its own window class
(`game-dev-2d-shokunin/corpus/live/r79-boundary-exec/run_love_probe.py:42`), with results reported at
`game-dev-2d-shokunin/reports/round-79/r79-boundary.md:196,202`. The only other sibling corpus hit is
tameshi's historical mutation case, which PATH-starves `hyprctl` to test mado's gate
(`tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md:46,48,141`) — a read-only probe of
mado's instrument, not a hyprctl claim of its own.

**Disposition.** Report, never absorb. Two consequences are real and bounded:

1. The compositor mado's live plane would read is shared with lanes that spawn windows
   (`game-dev-2d`'s love probe; `kake`'s "spawn Grok Bot app on Hyprland ws 3, silent/unfocused",
   `kake-shokunin/corpus/knowledge/ops-automation.md:83`). A live `clients` reading during another
   lane's run is not a quiescent-host reading.
2. Round 24 takes no host-verb risk: C1 is documentary, and C2's manifest arms are `--no-live`,
   `--selftest`, `--regression`, file-plane scripts, and one network read (the landedness arm runs
   `git ls-remote origin`, `mado-shokunin/.ufo/waves/round-19/landed-check.sh:28,87`); none issues a
   `hyprctl`, systemd, or package verb
   (`mado-shokunin/.ufo/waves/round-24/c2/manifest.json:8-151`). Any later round that resumes live
   reads must state the shared-compositor caveat; it is a reporting obligation of that round, not a
   claim on the other lanes' probes.

**What the bytes do not establish.** That a sibling probe was running during any mado measurement —
no host state was read here, and no `hyprctl` was invoked.

### 2.3 Capability-table re-demonstration (C2) — **mado owns its own table; tameshi owns the method and the runner it executes**

**Observed.**

- The 12 capabilities C2 re-demonstrates are mado's own SCORECARD rows (7 capability tables at
  `mado-shokunin/SCORECARD.md:304,915,1016,1154,1198,1338,1405`; the manifest names 12). No sibling
  audits or owns mado's table; S6 shows only each lane's own tables. The fleet contract that a
  capability enters only by demonstration is operator-side (`AXES.md:57-63`), not a sibling's.
- One arm is a live cross-lane dependency: the "mutation regression with re-cut" row runs
  `bash {TREE}/tools/mado-verify.sh --regression` with
  `MADO_VERIFY_HARNESS={FLEET}/tameshi-shokunin/tools/mutate-and-run.sh`
  (`mado-shokunin/.ufo/waves/round-24/c2/manifest.json:44-48`). The gate hands the spec to that
  runner at `mado-shokunin/tools/mado-verify.sh:2150-2151`, under the tool's own discipline comment
  ("the harness … is consumed read-only — a needed change is a recommendation to tameshi, never a
  patch; its revision is printed as provenance, not gated", `:1938-1940`, printed at `:2258`).
- tameshi owns that runner and the method: "Owns: the method" (`tameshi-shokunin/PROVINCE.md:7`),
  "Never edits a sibling's gate code" (`:16`), and mado's gate is listed as a read-only primary
  surface in tameshi's Core (`:28-35`). The historical mado leg and its kill rate belong to
  tameshi's ledger (`tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md:48,135-146`).
- The runner is shared, not mado-specific: tsukuroi consumes it too (S4, e.g.
  `tsukuroi-shokunin/corpus/knowledge/memory-arm-mutants-s8.md:23` records its own executed digest;
  `tsukuroi-shokunin/corpus/knowledge/closeout-r11.md:337,352` records a run).

**The concrete drift.** mado's recorded harness digest is `b56c6e57…`
(`mado-shokunin/tools/mado-verify.sh:2032`); the live sibling harness is `fb91ef76…` (S-digests
above). The line is labelled provenance and does not gate, so nothing turns red — but C2's manifest
row executes bytes that are **not** in mado's REV tree, and tameshi changed the runner as recently
as 2026-10-22 (`git -C tameshi-shokunin log -1 --format='%h %ad %s' -- tools/mutate-and-run.sh` →
`a08e85c 2026-10-22 round-26: ninth ledger leg js-cite-check … runner and interop wired`). The
manifest row's interface (`--target/--defects/--suite/--workdir/--label`) is documented in the live
harness header (`tameshi-shokunin/tools/mutate-and-run.sh:33-66,195-201`) and parsed at `:1996`; the
live revision therefore still exposes the form mado calls, but that is a read of today's bytes, not a
promise for the run.

**Second cross-lane dependency, different owner.** The "sources registry" arm runs
`bash {FLEET}/scripts/sources-census.sh validate --root {CENSUS_ROOT}`
(`mado-shokunin/.ufo/waves/round-24/c2/manifest.json:8-9`). That script is fleet/operator-side, not
a sibling lane's: `PROTOCOL.md:216-217` keeps `scripts/` operator-side. kagi has a *lane-local*
file of the same basename (`kagi-shokunin/PROVINCE.md:55`) enforcing the same SOURCES-CONTRACT-v1
over kagi's own registry; it is a name collision, not a shared instrument.

**Disposition.** Report, never absorb: mado owns the capability table and its verdict; tameshi owns
the runner and the method; the fleet owns the census CLI and the source contract. Round 24 must not
(a) edit the runner, (b) restate tameshi's ledger rate as current, or (c) present the census
contract as mado's. The C2 receipt should carry the executed sibling digests, which the counter does
not currently record (below).

**What the bytes do not establish.** Whether the `--regression` arm passes at the landed tip — this
seat ran no gate, and the C2 counter's own run is the measurement. Also unestablished: that
tameshi's next commit keeps the interface stable.

---

## 3. Contested-scope register

No surface below is *contested* in the sense of two lanes claiming it. The register separates
"owned elsewhere" from "shared dependency" so the round neither absorbs nor duplicates.

| Surface | Claimant | Anchor | Reading | Round-24 disposition |
|---|---|---|---|---|
| Hyprland config plane, rules, display | mado | `mado-shokunin/PROVINCE.md:3,6` | owner | C1 stays here |
| Hyprland plane (inbound locator) | tsukuroi | `tsukuroi-shokunin/PROVINCE.md:124` | confirms mado | cite only |
| host compositing, render regression | game-dev-3d defers to mado | `game-dev-3d-shokunin/reports/round-108/seats/connector.md:16` | adjacent, defers | no action |
| `hyprctl clients -j` live probe | game-dev-2d | `game-dev-2d-shokunin/corpus/live/r79-boundary-exec/run_love_probe.py:42` | instrument use, no ownership | report (§2.2) |
| GUI spawn on Hyprland ws 3 | kake | `kake-shokunin/corpus/knowledge/ops-automation.md:83` | app lane, unnamed "GUI lane" handoff | report, no absorption |
| mutation method + runner (`mutate-and-run.sh`) | tameshi | `tameshi-shokunin/PROVINCE.md:7,16,28-35`; `fleet-kill-rate-ledger.md:48` | owner; mado gate is a read-only surface | consume read-only; report digest |
| mado gate (`mado-verify.sh`) | mado | `mado-shokunin/PROVINCE.md:28`; tameshi `PROVINCE.md:32-33` | owner; sibling observes | no sibling edit |
| fleet source census + SOURCES contract | operator/fleet | `PROTOCOL.md:216-217`; `CORPUS.md:39-40` | operator-side | run, do not own |
| lane-local source census | kagi | `kagi-shokunin/PROVINCE.md:55` | kagi's own registry | name-collision note |
| capability-entry rule (demonstration only) | fleet axes | `AXES.md:57-63` | contract | C2 follows it |

---

## 4. Adjacency the round must report rather than absorb

1. **tameshi's runner and ledger.** C2 executes `fb91ef76…` (live) while mado records `b56c6e57…`
   (`tools/mado-verify.sh:2032`). A receipt that prints only `MADO_REGRESSION: PASS` is not
   reproducible later; the round should record the executed harness path and sha256 beside the
   verdict. The older mado kill rate (4/10 → 10/10 at r6) is tameshi's record
   (`fleet-kill-rate-ledger.md:48,135-146`), not a current statement about this gate.
2. **Operator-side census.** `scripts/sources-census.sh` (sha256 `3fb72615…`) and
   SOURCES-CONTRACT-v1 are not lane property. C2's "sources registry" row is a *use* of the fleet
   command; its output is a mado verdict, not a contract ruling. If the census changes, the row's
   observed status changes without mado's tree moving.
3. **The omarchy skill facet asymmetry.** kotoba records that "mado surveys the omarchy skill
   file's frontmatter as its own documentation surface (mado `PROVINCE.md:10-11`), and a mado wave
   report assigns that facet to kotoba with no province clause"
   (`kotoba-shokunin/PROVINCE.md:57`). [INF] The report it names is
   `mado-shokunin/.ufo/waves/round-18/w1/reports/SiblingOverlap18.md:81` ("omarchy skill **as a
   document instance** … kotoba … one survey datum; no province clause"); I found no other mado
   report making that assignment. Round 24 touches no omarchy-skill content, so it neither widens
   nor repairs this. If a clause is wanted, it is an L1 PROVINCE append, not a seat edit.
4. **Shared live compositor.** game-dev-2d and kake can spawn windows; mado's live plane would see
   them. Round 24 runs no live verb, so the round must not read its C1/C2 receipts as evidence about
   a quiescent compositor. Any live claim belongs to a round that states the shared-host caveat.
5. **Word "attribution" in five senses** (§2.1). The new note and the README coverage row should
   use the window-rule sense explicitly; kotoba Q23 (`corpus/QUALITY.md:34`) is a documentation rule
   about credit, not a claim on Hyprland rules.
6. **Host observability is not mado's.** kengaku's process census counts compositor memory
   (`kengaku-shokunin/corpus/evidence/round12-fleet/r12-endpoint-freshness.md:680` "Hyprland 187 …
   MiB") and mori/tsukuroi own host state. C1's new note must not turn a memory or process reading
   into a rule-attribution fact; round 24 takes none.

---

## 5. Contradictions stated, not smoothed

1. **Recorded harness digest vs live harness.** `b56c6e57…` at `tools/mado-verify.sh:2032`; live
   `fb91ef76…`. The tool calls this provenance, not a gate, so there is no failing check — but the
   C2 predicate's phrase "run on the REV tree" is literally false for this arm: the target is the
   REV file, the runner is tameshi's live HEAD. Reporting both is the honest form; silently
   attributing the result to the REV tree is not.
2. **mado's province wording vs kotoba's reading.** mado says the omarchy skill is "documentation
   surface, read-only" (`PROVINCE.md:10-11`); kotoba reads a mado wave report as assigning that
   facet to kotoba with no province clause. Both statements stand in bytes; they are not the same
   claim, and round 24 resolves neither.
3. **tameshi's ledger vs the current gate.** The ledger's mado row is a round-6 measurement at
   `d7edaab4`/`c4c1afb7` (`fleet-kill-rate-ledger.md:48`); the current gate is thousands of lines
   and round 24 re-demonstrates a different assertion count. Neither number may be carried into the
   other's sentence.
4. **Name collision on "rule attribution".** kotoba Q23's sense (authority credit) and C1's sense
   (which rule produced an applied effect) are unrelated; a fleet reader grepping the phrase will
   hit both. The note's limit line should disambiguate rather than assume the reader's context.
5. **No contest ≠ no adjacency.** S1/S2/S5 return zero because no sibling writes on these surfaces,
   not because the surfaces are empty of sibling interest: tameshi lists mado's gate as a primary
   surface, tsukuroi locates mado's ownership, and the game lanes probe the same compositor. Zero
   is a citation count, not a claim that nobody cares.

---

## 6. Recommendations (report-only; L1/main decides)

1. **C2 receipt.** Record the executed sibling digests in the round-24 receipt next to the C2
   verdicts: `tameshi-shokunin/tools/mutate-and-run.sh` (live sha256 at run time) and
   `scripts/sources-census.sh`. The counter's result rows carry `argv`/`cwd` only
   (`.ufo/waves/round-24/c2/count.py:322-328`), so the digest has to travel in the receipt prose or
   a sidecar. This is the r18 lesson (`SiblingOverlap18.md:7.2`) repeating at a second drift.
2. **C2 arm failure attribution.** If the regression arm returns SETUP/FAIL because the live runner
   moved, report it as a cross-lane dependency finding and say which digest ran; do not score it as
   mado's capability regression without that sentence.
3. **C1 note.** Keep every claim row on the pinned hyprwm URLs (the C1 predicate already requires
   it); do not cite a sibling's note for rule semantics, and add the one-line sense disambiguation
   against kotoba Q23 and mado's own declarer-attribution note.
4. **No absorption.** Do not add a province clause for `hyprctl` usage, the mutation method, the
   census contract, or the omarchy skill facet inside a wave report. If a clause is needed it is an
   L1 append to `PROVINCE.md` with its own evidence.
5. **Do not restate tameshi's rate.** Any sentence about kill rates in round-24 files should name
   the revision and the ledger entry, or leave the number out.

---

## 7. Limits

- No sibling gate was executed; no `mado-verify.sh` mode was run; no `hyprctl`, `systemctl`,
  `pacman`, `omarchy-*`, or package query was issued; no network request was made. Every sibling
  fact above is a file-byte read at the live working tree, not a committed pin of mine.
- Sibling HEADs move. `81955bd` is mado's HEAD at scan; tsukuroi's/kotoba's/tameshi's anchors are
  their live bytes today. A later commit invalidates a line number, not the ownership sentence.
- S4 is a name-scoped grep for the runner path; it does not prove no lane embeds a copy under a
  different name. S1/S2/S5 are scope-surface sweeps, not whole-tree searches (whole-tree searches
  over the `.ufo` histories were time-boxed out).
- The kotoba census and kagi/kaidoku tables were read as their live files; where a quoted row pins a
  commit (`sibling-overlap-census-round49.md:82` pins `e33ea304`), I did not re-check that commit's
  bytes — the classification sentence I cite is the census's own, retained by kotoba's live
  `PROVINCE.md:57`.
- No file other than this report was written; no tool was installed or updated.

## Verdict

No sibling lane owns or contests Hyprland window/layer rule attribution or `hyprctl`; mado is the
sole scope-surface claimant (S1=0, S2=0, S3=1 inbound locator). C2's capability table is mado's own,
but one arm executes tameshi's live mutation runner (recorded `b56c6e57…` vs live `fb91ef76…`) and
one arm executes the operator-side fleet census (`scripts/sources-census.sh`), so C2's "REV tree"
wording and its receipts need those two digests named; nothing should be absorbed from tameshi,
the fleet, or kotoba.

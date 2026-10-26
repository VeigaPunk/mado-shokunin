# CritAssimilation — the round-43 assimilation decisions re-opened

Seat: mado round 43 w2, `CritAssimilation` (critic, leaf). Date 2026-10-26.

**Target.** The lesson's `## Assimilation ledger` and its five `ADMIT`/`REFUSE` lines
(`corpus/lessons/round-43.md` at `1959770657f1f8665097c1aed4be6c1cbb07139f`), tested against the five decided staged files in
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` (read-only) and against the landed entry
`corpus/knowledge/hyprland-gkeep-geometry-r43.md` (frozen at the same commit).

**Method.** Re-read the five decided files whole; re-read the other six staged gkeep-theme files (`gkeep-*.md`, `glyph-and-geometry-r31.md`)
so the ledger's unadopted rows could be judged too; re-read the ten pins in `.ufo/waves/round-43/fetch/`, `corpus/SOURCES.md` rows S155,
S158, S290-S297, `quality/counters/c2-r43-gkeep-entry-v2.py` (STAGED, clause i), `PROVINCE.md`, `MERGE-REPORT.md`, and the w1 reports my
items name (`w1/ScoutStagedGkeep`, `w1/ConnStagedVsRegistry`, `w1/ExecLiveHost`, `w1/ExecOracleGkeep`). Every quote below is verified by
`verify-quotes.py` against `quotes.tsv` (`verify-quotes.txt`: `QUOTES: checked=43 miss=0`). `/home/vgpnk/Projects/shokuknow` was read-only
throughout; writes are confined to this seat.

**Nothing here judges, admits, edits or integrates a candidate.** The counter (`PRED-C2-r43-v2`), the controls and the data commit are
frozen; every finding is a correction for the record, not a re-scoring.

## 0. Verdict table

| decided file | ledger verdict | is the stated reason true of the file? | is the flip condition meaningful? | does the entry carry what it says it took? |
|---|---|---|---|---|
| `gkeep-size-to-real-size-r11.md` | **ADMIT as the successor** (L45) | yes, as far as it goes: four of five sources are this round's pins and the chain's three downstream links are pinned (F2) | there is no flip for an ADMIT; the row states no retirement test | **partly** — three of the four links; link four is cited nowhere (F2), and the file's headline conclusion is narrowed without being recorded (F7) |
| `gkeep-size-rule-application-r10.md` | REFUSE (L46) | **yes** — `r10:45-47` says the reported number is the client's; the pinned path contradicts it | yes (checkable), but its named trigger is adjudicated in an unadopted file (F5) | n/a |
| `gkeep-geometry-unobservable-r8.md` | REFUSE (L47) | yes for the census and the "nothing else is missing" residual; the third ground is mis-stated (F3) | **no** — unsatisfiable as written / already fired as intended (F3) | n/a |
| `gkeep-observation-route-r11.md` | REFUSE (L48) | **yes** — exactly one `source:` line (`obs:8`) | **no** — the flip points away from the stated reason and is already literally true (F4) | n/a |
| `gkeep-element-rules-r30.md` | REFUSE (L49) | yes that the explanation is the comment and an inference (`r30:23,27`) — but the flip has already fired (F1) | **yes, and it is met** — the shipped config sources the number (F1) | n/a |

The ledger's non-adopted rows were also checked: the ledger covers all 11 files in the counter's `STAGED` set (`c2-r43-gkeep-entry-v2.py:92`)
across nine rows; that part of the record is complete (I first believed four files were missing — the table continues past `r12`; corrected
before writing). Rows `r9`, `r12`, `r13`/`r14`/`r15` and `glyph-and-geometry-r31` carry accuracy defects (F6).

**Axes these findings move:** correctness of the merged claim, provenance/sourcedness, supersession identity (which text wins), and the
testability of the flip record. They do not move the lane's published axes (navigation/calibration/operability).

---

## F1 — the `r30` refusal's flip condition was already met when the ledger was written

**Attack:** `lesson:49` (the `REFUSE` line) and the `gkeep-element-rules-r30.md` row (`lesson:78`).

**Counterexample.** The row's ground is that the 875×600 explanation "rests on a config comment and not on any pinned measurement", and its
flip is "if the stock floating-tag size is measured or sourced from the shipped config". The shipped config carries it — in the file, though not yet pinned as a row — and this
round had already read it:

```
$ grep -n '875 600' ~/.local/share/omarchy/default/hypr/apps/system.conf
4:windowrule = size 875 600, match:tag floating-window
```

`system.conf:2` carries `windowrule = float on, match:tag floating-window` and `:3` the matching `center on`; the file's mtime is
`2026-10-03 17:42:32`, i.e. it predates the round. This is the same line w1 collected in its own census —
`W1C` at `w1/ExecLiveHost/live-census.txt:232`, unreachable-classified in the same file at `:370`, and named by
`w1/ExecLiveHost.md:81` ("`omarchy/default/hypr/apps/system.conf:4` `size 875 600, match:tag floating-window`"). So the refusal's flip
condition was one pin short of satisfied *by the round's own receipts* before the ledger was authored; the ledger did not consume it. That is
a defect of the record, not a w1 re-report: the finding I report is the ledger's non-use of it. Precisely: "sourced" in this lane means a
registry row with a pinned receipt, and what the round held is the read plus a receipt line (`live-census.txt:232`) — not a pinned byte copy.
But the row's ground ("not on any pinned measurement") trades on exactly that distinction, and the round pinned a byte copy of the host rule
file on the same day (`S295`); a pin of `apps/system.conf` was one `cp` away, in a tree the province already calls read-only.

**Second half — the flip is under-specified.** It names only the *number*. The row's other two grounds are not tested by it: that the entry
"predates the whole source chain", and the entry's causal story. The shipped bytes also show that story is wrong in kind: the 875×600 rule
applies to windows carrying the `floating-window` **tag** (`system.conf:4`, tag applied at `:6-7` to a class list), and the host's gkeep file
deliberately does not tag gkeep — the host's own comment says so (`r30:23`) and the rule triad shows only class matches (`host-gkeep.conf:2-4`).
So the number is sourced, while "the host overrides it to a 420×500 post-it" (`r30:27`) is a *different* claim that the same source does not
support.

**Smallest safe correction.** Split the row into two claims with one flip each: (a) the 875×600 number — flip fired, source it as an own-work
row (the shipped file at `apps/system.conf`, read-only in the omarchy store the province already names) and record the flip as fired; (b) the
work-around inference — keep the "predates the chain / wrong in kind" ground and give it a flip that tests it (e.g. a window observed carrying
the `floating-window` tag at 875×600 *and* gkeep being tagged). Do not re-run the frozen verdict; append the correction.

## F2 — the ADMIT says "four-link chain" but the entry manifests three links and an accessor

**Attack:** `entry:17` (`assimilated-from: ... (its four-link chain, re-derived at the host's own commit)`) and `lesson:74` (the ADMIT row).

**Counterexample.** r11's chain is four steps: rule → floating algorithm (S302) → target box (S303) → window (S304) → the window's real size
written (S305). The landed entry carries steps 1-3 at `entry:40-46` and then cites the *same* file S294 only for the read side —
`entry:52` quotes the `GEOMETRIC_GOAL` accessor. Link four is the write:

```
$ grep -n 'm_realSize' corpus/knowledge/hyprland-gkeep-geometry-r43.md
52:**OBS** S294 - ... `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` (Hyprland-GeometricMovableAnimated.cpp:19)
$ sed -n '43,45p' .ufo/waves/round-43/fetch/Hyprland-GeometricMovableAnimated.cpp
void CGeometricMovableAnimated::setBox(const CBox& x) {
    *m_realPosition = x.pos();
    *m_realSize     = x.size();
```

The staged file quotes exactly that line (`r11:54`), under "Step four — the window's real size is written". The landed entry does not, and
the registry row does not either: S294's declared ranges are
`src/desktop/view/types/GeometricMovableAnimated.cpp:8-15 position, :17-24 size, :26-33 geometricBox, :39-41 resize, :53-59 the two animation handles`
(`S294`, `sources-at-1959770.md:243`) — `:43-46` is absent. So the only connection between "the target keeps the box" (S292/S293) and "the
reported size is a GOAL" (S158/S294:19) is unstated in both places the reader is pointed at, yet `entry:50-56` rests on it: the entry's §3
INF says "a `clients -j` size equal to the rule's size says that the compositor's target equals the rule". That INF needs the write.

**Smallest safe correction.** Append the fourth link to the entry (next round, not this frozen commit): quote `*m_realSize     = x.size();`
with locator `Hyprland-GeometricMovableAnimated.cpp:43-45` and extend the S294 row's used-by/scope as an append; the Gate quote for S294 stays
as it is (one Gate per id). If the append is not made, restate `entry:17` to "its three-link chain plus the `GEOMETRIC_GOAL` accessor" and
downgrade the §3 INF to what three links support.

## F3 — `r8`'s flip condition cannot be evaluated (it names a path that cannot exist, where it means a fact that already exists)

**Attack:** `lesson:47` / `lesson:76` (`gkeep-geometry-unobservable-r8.md`).

**Counterexample.** Two readings, and neither is decisive:

- Narrow (the literal words, "its identity receipt is re-sourced"): the receipt is the private path `r8:8`
  `lanes/mado/round8/fetch/host-focus-grab-and-timeout.txt`. That path cannot be created inside this lane — the package carries no `lanes/`
  tree (`w1/ScoutStagedGkeep/survey.md:12-14`, whose `find` returns empty) and the lane pins receipts per round; `git ls-tree -r --name-only HEAD |
  grep -c 'round8/fetch'` → **0** (re-run this seat; the ledger's own number). So the flip is unsatisfiable by construction.
- Intended (the build identity): it has already fired. r8's identity quote (`r8:22`) is the host banner, and round 43 re-sourced the same
  banner in-lane: `receipts/live-geometry-host.txt:3` —
  `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`. No *SOURCES row* carries the host
  binary identity (S290-S294 carry the upstream commit in their locations; they are not the `hyprctl version` string), so "a round-43 row
  re-sources it" is also not literally true.

The refusal's other grounds survive independently: r8's census is three clients (two Alacritty, `zcode`) and the pinned census is four
(`S296`), and "Nothing else is missing" is contradicted by the entry's own new chain. So the verdict is right and the *flip* is the defect.

**Smallest safe correction.** Replace the flip with a testable one tied to what the file would still contribute: "flip if a SOURCES row
carries the host build identity (`hyprctl version` string, now only in `receipts/live-geometry-host.txt:3`)" — and record that the census
and residual grounds are already refuted, so re-opening would not restore the file.

## F4 — the `obs-route-r11` flip points away from its own reason, and is already literally true

**Attack:** `lesson:48` / `lesson:77` (`gkeep-observation-route-r11.md`).

The reason is redundancy: "single-source restatement of r11 on the same host receipt, adding no independent ground beside the rule text"
(`lesson:48`; `L77`). I checked the redundancy claim and it is true: the file has exactly one `source:` line (`obs:8`, S310), the same
private receipt r11 used. But the flip is "if an independent witness for the observation route is added" (`L48`). Adding a witness makes the
file *more* redundant, so the flip can never clear the stated reason; and `MERGE-REPORT.md:136` says a refused row is not re-touched "until
the stated reason is cleared". Worse, the literal condition is now true: this round added independent route witnesses — the pinned census row
`S296` and the oracle run, which reads the same client through `clients -j`
(`w1/ExecOracleGkeep/20-observation.txt:7` shows `"size": [420, 500]` for the app id; the entry cites that run at `entry:62`). So the record
holds a fired flip with an unmoved verdict.

**Smallest safe correction.** Replace the flip with the reason's real test: "flip if the surviving witness is withdrawn or shown not to
answer the route (S158's `GEOMETRIC_GOAL` read, or the entry's §5 census)". A duplicate verdict needs a flip on the surviving witness, not on
the supply of witnesses.

## F5 — the `r10` refusal is correct but cites the weaker ground, and its flip's trigger is adjudicated only in an unadopted file

**Attack:** `lesson:46` / `lesson:75` (`gkeep-size-rule-application-r10.md`).

The reason is TRUE of the file. The file's inference, in its own words (`r10:45-47`), is that "the number the compositor reports is whatever
the client actually used" (`R10i`), and the pinned path writes the rule's value into the animated real size (`G43`/`G45`,
`*m_realSize     = x.size();` at `Hyprland-GeometricMovableAnimated.cpp:45`), so the report is the rule's value. The ledger's ground (S291
evaluates the rule's expression; S293 pushes the box) is accurate but stops one link short of the refutation (F2).

Two observations for the record:

1. The strongest falsifier is *in this round's receipts* and the regular ledger doesn't cite it: in the isolated round-27 oracle a client
   whose own buffer is 200×200 (`w1/ExecOracleGkeep/20-observation.txt:19`, `CLIENT_READY app_id=org.omarchy.gkeep buffer=200x200`) still
   reports `"size": [420, 500]` under the host's rules — the reported size is not the client's. This is an experiment, not an inference.
2. The flip's named trigger is "the client's acknowledgement" (`L46`) — exactly the mechanism `r13` pins and reads the other way
   (`r13:39`, "it cannot substitute a different number"). The ledger leaves r13 as residue (`lesson:81`) without cross-referencing it in the
   r10 row. A later round that re-opens r13 and reads `onAck` may mistake it for the flip firing.

**Smallest safe correction.** Cite the oracle receipt in the r10 row and add the `onAck` cross-reference to r13, so the flip's trigger is
pre-adjudicated rather than left to a future reader of an unadopted file.

## F6 — residue-row accuracy (three small, checkable errors)

**Attack:** `lesson:79` (r9), `lesson:81` (r13/r14/r15).

1. **"three journal sweeps"** (`L81`). Only r13 (`r13:12`, `host-journal-map-log-sweep.txt`) and r14 (`r14:9`,
   `host-journal-map-log-alltime-sweep.txt`) are journal sweeps. r15's decisive source is the lane's own artifact grep
   (`r15:7`, `corpus-round24-artifacts-sweep.txt`) — `w1/ScoutStagedGkeep/survey.md:96` classifies it as "lane bookkeeping, not desktop
   knowledge", which is a *different* and stronger reason than "not pinned". The row also says "the map-time DEBUG log" is a decisive
   source; it is not a source, it is the line inside S319.
2. **Scope cell "in" loses w1's boundary.** r14's whole evidence is a whole-user-journal sweep, and w1 flagged the boundary
   (`survey.md:95`, "borders on tsukuroi's journal ground"). The ledger's row that would authorise a later adoption is the place that caveat
   matters; `PROVINCE.md` does not list journals as refused, but the lane's own journal instrument is bounded to one unit
   (`tools/mado-globals.py` row, `PROVINCE.md:31`).
3. **r9's "held" cell is unlocatable.** "partly held as prose (no lane row cites it)" (`L79`). At base, `git grep -il gkeep a35cfdf --
   corpus/knowledge` returns three files and none carries r9's claim; `git grep -n 420 a35cfdf -- corpus/knowledge SKILL.md README.md PROVINCE.md`
   finds no gkeep 420×500. The nearest lane prose says the opposite: `config-drift-r12-at-base.md:116`, "gkeep rule bodies and their
   per-window effects remain unexamined". The cell overstates what the lane holds.

**Smallest safe correction.** Correct the three cells in an append (they are records, not verdicts): "two journal sweeps plus a lane-artifact
grep", the tsukuroi boundary on r14, and r9's held cell to "—" or a named file:line.

## F7 — "admitted as the successor" narrows the admitted file's headline conclusion without saying so

**Attack:** `lesson:74` (verdict cell) and the append-only merge rule (`MERGE-REPORT.md:133`, "Do not replace the file").

r11's title is "The size rule reaches the window's real size, so the rendered geometry is settled" (`r11:2`), and its §2 fixes the rendered
geometry at 420×500 "settled at the source level" (`r11:66`). The landed entry refuses exactly that: the table answers "Is the GOAL the size
drawn on screen?" with "UNK on the host" (`entry:27`), and "What this entry does not establish" opens with "The current (drawn) size of a
gkeep window at any moment on the host" (`entry:78`). The entry is right and r11 is overreaching — but the ledger calls r11 the *successor*
without recording that what survives is the mechanism, not the conclusion. Because the merge appends the new file and keeps the staged
reading (`MERGE-REPORT.md:133`), the merged corpus will carry both "the rendered geometry is settled" and "the drawn size is UNK" with no
ledger line saying which wins.

**Smallest safe correction.** In the ADMIT row (or an append), state: "the entry takes the four-link mechanism and narrows r11's 'settled' to
'the GOAL equals the rule; the drawn size remains UNK'". That is also the line a reader needs before reusing r11's title as a claim.

---

## What I checked that came back clean (so the record is not one-sided)

- **ADMIT sourcing is sound.** Four of the five sources are this round's pins, by file identity (S302↔S291 DefaultFloatingAlgorithm,
  S303↔S292 Target, S304↔S293 WindowTarget, S305↔S294 GeometricMovableAnimated), and every r11 quote is in the pinned bytes:
  `if (WINDOW->m_ruleApplicator->static_.size) {` (`DefaultFloatingAlgorithm.cpp:55`), `windowGeometry.w = COMPUTED->x;` (`:60`),
  `target->setPositionGlobal(windowGeometry);` (`:96`), `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` (`Target.cpp:10`),
  `m_box = box;` (`Target.cpp:11`), `m_window->setBox(m_box.logicalBox);` (`WindowTarget.cpp:71`),
  `const bool  CONFIGURECLIENT = !(flags & TARGET_UPDATE_NO_CLIENT_CONFIGURE);` (`WindowTarget.cpp:50`). The ledger's `S310`
  re-grounding as "S295/S296" is slightly under-counted: S310 covered the app request as well, re-grounded as S297 (`entry:60`).
- **The ADMIT's "held" grep re-runs.** `git grep -ciE 'set_default_size|GEOMETRIC_GOAL|RE2::FullMatch|rendered geometry' a35cfdf --
  corpus/knowledge PROVINCE.md SKILL.md tools` → rc=1, no hits.
- **The entry's "no read verb exposes CURRENT" is checkable and holds in the pinned HyprCtl.** `grep -n 'GEOMETRIC_' Hyprland-HyprCtl.cpp`
  returns `GEOMETRIC_GOAL` only (lines 426-428 and 447-448), never `GEOMETRIC_CURRENT`.
- **The held-row choice is supported.** S155 and S158 already exist with the commit-form URL and the pinned sha256, and S158 is already cited
  by `corpus/knowledge/rule-attribution-r24.md`; no duplicate row was needed.
- **Province fit of the five decided files holds.** Host rule file and Hyprland source at the host's tag are in province (source-read precedent:
  `rule-attribution-r24.md` rows S156-S158); the app half is chain evidence, the framing the lane already uses (`host-bar-producer-census-r40.md:37`,
  "chain evidence ... not owned"). The only scope question is r14's journal ground (F6.2).
- **Ledger coverage is complete** across the 11 `STAGED` files (nine rows), and the round's own checklist scopes the re-read to the five decided
  files (`lesson:200`, "re-open the four REFUSE files and the one ADMIT file"). No file is silently undecided.

## Receipts in this seat

- `findings.md` (this file), `quotes.tsv`, `verify-quotes.py`, `verify-quotes.txt` — `QUOTES: checked=43 miss=0`.
- `lesson-at-1959770.md` — `git show 1959770657f1f8665097c1aed4be6c1cbb07139f:corpus/lessons/round-43.md`.
- `sources-at-1959770.md` — `git show <rev>:corpus/SOURCES.md`. `config-drift-r12-at-base.md` — `git show a35cfdf:corpus/knowledge/config-drift-r12.md`.
- Scratch: `/fast/scratch/hyaku/mado-r43/CritAssimilation` created empty and removed at finish; no other tree left on disk. No tool installed,
  no host command beyond read-only file reads (`grep`, `stat`, `sed` on config files; no `hyprctl`, no compositor socket).

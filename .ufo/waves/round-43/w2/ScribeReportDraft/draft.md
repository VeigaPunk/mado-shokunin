# Round 43 — Sources & frontier, and Trend verdicts (draft)

Seat `ScribeReportDraft` (scribe, w2, 32-seat falsification wave), 2026-10-26. This file drafts **two report
sections only** — *Sources & frontier* and *Trend verdicts* — from evidence that is committed or is a receipt
under `.ufo/waves/round-43/receipts/`. It edits nothing: the registry, counters, controls, registration,
reference and fetch receipts are frozen.

**Provenance of every number below.** Data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` (parent
`496340d`, the C2 v2 freeze), base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (round-42 tip). Lane HEAD is
`2a3707c` = data + `a47efeb` (after-data receipts, w2 spec) + w1 evidence; `corpus/SOURCES.md`,
`corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-43.md` are byte-identical between the data
commit and HEAD (`git diff --numstat 1959770 HEAD -- corpus/ SKILL.md PROVINCE.md tools/ quality/` prints
only `7 0 SKILL.md`; `git diff --name-only 1959770 HEAD -- corpus/` is empty), so the line anchors below hold at
both. The assimilation artifacts cited in §2–§3 are **not** in the data commit's tree —
they landed later, at `2a3707c` (`git ls-tree -r --name-only 1959770 .ufo/waves/round-43/assimilation/` → 0
files; same command at `2a3707c` → 7 files). Every claim below says which of the two it rests on.

---

## 1. Sources & frontier

### 1.1 Registry rows, before → after

The counting command is the one the lesson uses (`corpus/lessons/round-43.md:28`), run against the two
committed blobs, not the worktree:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
for R in a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f 1959770657f1f8665097c1aed4be6c1cbb07139f; do
  git -C . show $R:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
done
```

| | base `a35cfdf` | data `1959770` | Δ |
|---|---|---|---|
| rows (counting command above) | **226** | **234** | **+8** |
| distinct ids (`grep -oE '^\| S[0-9]+' \| sort -u \| wc -l`, same blob) | 226 | 234 | +8 |
| `corpus/knowledge/` entries (`git ls-tree -r --name-only <rev> corpus/knowledge/ \| wc -l`) | 59 | 60 | +1 |

+8 rows, no duplicate id: the two counting forms agree at both revs, so the 8 new rows are 8 new ids.

### 1.2 Rows added, by tier

Tier cell is field 4 of the table; the command is
`git -C . show <rev>:corpus/SOURCES.md | grep '^| S' | awk -F'|' '{gsub(/^ +| +$/,"",$4); print $4}' | sort | uniq -c | sort -rn`
at each rev:

| tier | base | data | Δ | the added rows |
|---|---|---|---|---|
| code | 101 | **106** | +5 | S290 `RegexMatchEngine.cpp`, S291 `DefaultFloatingAlgorithm.cpp`, S292 `Target.cpp`, S293 `WindowTarget.cpp`, S294 `GeometricMovableAnimated.cpp` |
| own-work | 24 | **27** | +3 | S295 `host-gkeep.conf`, S296 `host-clients-r43.json`, S297 `gkeep-ui-excerpt.py` |
| docs | 78 | 78 | 0 | — |
| spec | 13 | 13 | 0 | — |
| community | 5 | 5 | 0 | — |
| paper | 3 | 3 | 0 | — |
| dataset | 1 | 1 | 0 | — |
| book | 1 | 1 | 0 | — |
| **sum** | **226** | **234** | **+8** | |

All eight carry `status=mined`, `opened 2026-10-26`, `used-by corpus/knowledge/hyprland-gkeep-geometry-r43.md`
(S290-S294 `recheck on-release`, S295-S297 `recheck 2027-01-24`; fields 9-11 of each row, blob at data).
Ids are contiguous and append-only: `… S286 S287 S288 S289 S290 … S296 S297`, and `S298`/`S299` stay free
(`corpus/lessons/round-43.md:65-68` reserves S290-S299 and records the shrink to S290-S297).

### 1.3 Rows touched, old → new

Exactly two held rows changed, and only in their `used-by` cell. The evidence for "only that cell":
`git -C . diff --numstat a35cfdf 1959770 -- corpus/SOURCES.md` → `10 2 corpus/SOURCES.md`, i.e. 8 added rows
plus 2 replaced lines; fields 1-10 of S155 and S158 are identical at both revs (compared field by field).

| row | base `used-by` | data `used-by` |
|---|---|---|
| S155 (`WindowRuleApplicator.cpp`) | `corpus/knowledge/rule-attribution-r24.md` | `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/hyprland-gkeep-geometry-r43.md` |
| S158 (`HyprCtl.cpp`) | `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md, corpus/knowledge/request-socket-live-bound-r8.md, corpus/knowledge/hyprctl-getoption-native-forms-r40.md` | the same five, then `, corpus/knowledge/hyprland-gkeep-geometry-r43.md` |

One item appended per row; no row's `status` or `recheck` cell changed (`corpus/lessons/round-43.md:85-92`).
The reason this is two held rows rather than two new rows is recorded at `corpus/lessons/round-43.md:61-64`:
the round's own pins restated documents the registry already holds, so the entry cites those rows instead —
"a new row would duplicate a held location (clause e, census E04)" (:63-64). See §3.

Census did not move. `diff <(grep -v '^mado\tok' receipts/census-before.txt) <(grep -v '^mado\tok' receipts/census-after-data.txt)`
is empty: the same seven `W04` duplicate-URL rows (S030, S042, S045, S097, S119, S120, S121) and the same
`W01 S277` row, `exit=0` at `receipts/census-after-data.txt:10`. The eight new rows therefore introduce no new
census finding — which is what the round claimed to expect (`corpus/lessons/round-43.md:93`).

### 1.4 Frontier

`git -C . diff --numstat a35cfdf 1959770 -- corpus/README.md` → `10 0`: ten inserted lines, **no deletion and
no edit of any existing line**. What those ten lines are:

- **one coverage-map index row**, `corpus/README.md:71`, for `knowledge/hyprland-gkeep-geometry-r43.md`
  (MADO-R43-1, round 43; successor to the staged `gkeep-size-to-real-size-r11`), closing on rows S290-S297 plus
  held S155/S158.
- **one new Frontier route**, `corpus/README.md:294-303`, `### Round-43 rule-size versus reported-size route`.

So: **pre-existing Frontier bullets advanced this round — zero.** No earlier route was rewritten, narrowed or
closed; the round-38 request-socket route (`corpus/README.md:283-292`) and everything above it keep their old
open items verbatim. (Checked, not assumed: `git -C . show a35cfdf:corpus/README.md | grep -n gkeep` returns
only two index rows, :37 and :69 — there was no pre-existing gkeep-geometry frontier bullet for this round to
advance.)

The new route states one edge class and parks **four** open items, verbatim scope
(`corpus/README.md:299-303`): "a live gkeep window on the host session (none was open; the 420x500 observation
is from the isolated round-27 oracle)" — plus the drawn size during and after the open animation, the client's
acknowledgement path, and rule attribution.

Frontier instrument, same commit: `tools/mado-geometry.py` (+417 lines; PROVINCE.md +1 tool row, SKILL.md +46
lines including the `Rule size versus reported size` subsection). The tool is byte-identical to the round-42
reference: `sha256sum tools/mado-geometry.py .ufo/waves/round-42/c1/ctl-ref-tool.py.txt` prints
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` for both and `cmp` is silent. Its one live
host run is reported, not scored: `receipts/live-geometry-host.txt:10-11`, `matched=0 … verdict=NO_MATCHING_CLIENT`,
`exit=3`.

---

## 2. Assimilation (theme: gkeep geometry)

Theme: **gkeep geometry**; package `merge/mado/` (read-only). Eleven staged candidate files, decided in the
ledger at `corpus/lessons/round-43.md:70-84` (nine rows; the r13/r14 pair shares a row that names the second
file in shorthand, `` `-r14.md` ``), and restated as machine-readable decisions at
`corpus/lessons/round-43.md:45-49`.

| verdict | count | what |
|---|---|---|
| **ADMIT** | **1** | `gkeep-size-to-real-size-r11.md` → `corpus/knowledge/hyprland-gkeep-geometry-r43.md` (`corpus/lessons/round-43.md:45`) |
| **REFUSE** | **4** | `gkeep-size-rule-application-r10.md` (:46) — its central inference "the client decides the reported size" is overturned by the pinned floating-algorithm and window-target path; `gkeep-geometry-unobservable-r8.md` (:47) — superseded, its S275 receipt path absent from this lane; `gkeep-observation-route-r11.md` (:48) — single-source restatement, now sourced as held S158; `gkeep-element-rules-r30.md` (:49) — the 875x600 explanation rests on a config comment, not a measurement |
| **not adopted** (6 files, not a REFUSE) | **6** | `gkeep-rendered-geometry-chain-r9.md`, `gkeep-client-size-request-r12.md`, `gkeep-rendered-geometry-record-r13.md`, `-r14.md`, `gkeep-geometry-never-recorded-r15.md`, `glyph-and-geometry-r31.md` — each ledger row names the document it would need and which of this round's pins is missing (`corpus/lessons/round-43.md:79-82`) |

1 + 4 + 6 = 11, the whole theme set. Every REFUSE carries a flip condition, and each flip names what would
change the verdict (e.g. :46 "flip if a pinned source shows the reported size coming from the client's
acknowledgement"; :47 "flip if its identity receipt is re-sourced inside this lane") — consistent with
clause i+ of `PRED-C2-r43-v2`, which requires a flip word in every REFUSE reason
(`receipts/c2-v1-to-v2.diff:17-18`). No row of the staged package was carried over, and the staged ids
S203-S349 were never used: the mapping is by document (`corpus/lessons/round-43.md:84` last row).

Assimilation is scored, not asserted: `receipts/c2-after-data.txt:31-33` —
`clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1`, `admitted=1/1 verdict=TARGET_MET rev=1959770…`,
`exit=0`, against `admitted=0/1` at base (`receipts/c2-v2-before-base.txt:2`). For reference, the superseded v1
predicate also passes the landed entry (`receipts/c2-v1-after-data.txt:32`, 1/1) — the reason v1 was replaced
before data is a *forgery* result, not this entry: v1 admits a 17-line entry citing three own-work receipts
(`corpus/lessons/round-43.md:182-189`, M43-8), and `receipts/c2-v1-to-v2.diff:5-9` records the w1 evidence —
"16 admitted forgeries, 8 of them closed by the tightenings below". The `ctl-c2` and `ctl-c2-v2` receipts each read
`controls=74 correct=74/74` (`receipts/ctl-c2.txt:76`, `receipts/ctl-c2-v2.txt:76`).

## 3. ID guard

Guard run and its limits are in `.ufo/waves/round-43/assimilation/id-guard.md` (committed at `2a3707c`, not in
the data commit's tree):

- **34 collisions** against the frozen registry: `reg-ids` 226, `staged-ids` 147, `comm`-intersection 34
  (`id-guard.md` §1: `226 … 147 … 34 … 407 total`).
- **The guard is shown able to fire**, on a scratch registry holding an indented `  | S203 |` row
  (`id-guard.md` §2): `cat scratch-ids` → `S203 S999`, `cat scratch-collisions` → `S203`. It is not vacuously
  empty.
- **Two measured blind spots, reported not fixed** (`id-guard.md` §2): a four-space-indented row is invisible to
  `^ {0,3}\|` (`S998` never matched), and the guard reads ids only, never URLs — two rows for one document never
  collide. The registry as it stands is fully inside the window (226 of 226 rows matched).
- **The guard under-reports by the reserved band**: 10 staged ids sit in S290-S299 and collide only once the
  pins land; four are cited by this theme (S292, S297, S298, S299) (`id-guard.md` §3 "The guard under-reports by
  the reserved band").
- **The round's answer to the duplicate-pin hazard** was to cite held rows instead of opening second rows:
  `corpus/lessons/round-43.md:61-64`, which also records that no gap was reopened — the new ids are
  "numbered by document, append-only and gap-free" (:65-66), S290 … S297 in file order, with S298/S299 free (:68).

---

## 4. Trend verdicts

Summary (the report may lift this table verbatim):

| trend | verdict | one-line evidence |
|---|---|---|
| expansion | **improved** | rows 226 → 234 (+8: code +5, own-work +3), entries 59 → 60, one new Frontier route + one new instrument |
| quality | **improved** | QUALITY +5 criteria (77-81), new `quality/check-locators.py`, 10 GATE lines, all 8 mistakes carry a shown-able-to-fail line (6 demonstrated and gated, 1 not yet a gate, 1 not shown); no criterion or held-row cell harmed |
| discernment | **improved** | 11 assimilation candidates → 1 admitted / 4 refused / 6 not adopted; a duplicate-row defect (S045 class) avoided; one stale artifact ships as F1 |
| axes | **unchanged at base / UNVERIFIED at data** | `receipts/axis-base.txt` only; no axis receipt exists at `1959770` |

Every number in this section and in §1-§4 is re-derived from the committed blobs and the receipts by
`.ufo/waves/round-43/w2/ScribeReportDraft/verify.py`, whose output is the seat's own receipt
`verify.txt` (90 checks, `VERIFY: all checks PASS`, `rc=0`). It is this seat's check, not an L1 gate.

Each verdict names its class, its evidence pointers, and what would have to be true for the verdict to be
wrong. No verdict below is inferred from a driver line, a clean tree, or a report sentence.

### 4.1 Expansion — **improved**

- Registry 226 → 234 rows (+8, +3.5 %), tier split code +5 / own-work +3, zero rows lost (§1.2 commands).
- Knowledge entries 59 → 60; one new Frontier route (`corpus/README.md:294-303`) with four named open items;
  one new instrument (`tools/mado-geometry.py`, 417 lines) with PROVINCE and SKILL rows.
- The growth is a *new edge class*, not a restatement: the route names what was previously unstated — that
  `hyprctl clients -j` `size` is the animation's GOAL (`Hyprland-GeometricMovableAnimated.cpp:19-20`,
  `Hyprland-HyprCtl.cpp:427-428`), and that a tiled client never reads the rule.
- Would be wrong if: the added rows reused a held document. Checked — the two documents that would have
  duplicated held rows were cited as held rows instead (§3, `corpus/lessons/round-43.md:61-64`), and the census
  set is unchanged (§1.3).

### 4.2 Quality — **improved**, with two instruments still open

- `corpus/QUALITY.md` +5 criteria (77-81, +10 lines): locators emitted by the grepping command; a control tally
  stated once with its denominator; a pointer asserting a run names a committed receipt; an excerpt header
  checked not typed; a closure row counting attempts/channels separately.
- One new checker, `quality/check-locators.py` (+405 lines), the first instrument for the class both M43-1 and
  M43-7 belong to; its discriminating runs are cited at `corpus/lessons/round-43.md:123-125` (a MISS on the
  round-42 locator, `miss=0` on the corrected copy).
- The lesson is complete and gated: 10 `^GATE S` lines, one per cited id, and
  `receipts/c2-after-data.txt` prints `clause=d … gates=1 bound=1` for all ten ids (`:11-20`).
- Mistakes are instrumented, not just listed: 8 (`M43-1` … `M43-8`), and all 8 carry a "Shown able to fail"
  line (verified count = 8). Two of those lines say the instrument is missing: M43-2's reads "Shown able to
  fail: not shown this round" and closes "open" (`corpus/lessons/round-43.md:133`), and M43-6 ends
  "Not yet a gate (open)" (`:171`). Read strictly: 6 of 8 (M43-1, -3, -4, -5, -7, -8) have a demonstrated,
  gated discriminating check; M43-6 demonstrates a discriminating count but is "not yet a gate"; M43-2's check
  "not shown this round".
- C1 arrives with its controls: `ctl-c1.txt:1` `controls=46`, `:50` `0 of 47` scoring TARGET_MET against a
  reference that meets it. **Precision:** that receipt was produced at base rev `a35cfdf` against the round-42
  reference; it carries to the landed tool by byte identity (§1.4, equal sha256 and silent `cmp`), and no
  control run exists at `1959770` — see §5 F2.
- Nothing observed harmed: no row's cells 1-10 edited (§1.3), census set unchanged, no criterion removed from
  `corpus/QUALITY.md` (diff is 10 insertions, 0 deletions).
- Would be wrong if: the landed entry failed a criterion it claims. That is the counters' job and it is scored
  at the data rev: `receipts/c1-after-data.txt:49-50` `fixtures=37/37 tool=present verdict=TARGET_MET …
  exit=0`, `receipts/c2-after-data.txt:32-33` `admitted=1/1 … exit=0`.

### 4.3 Discernment — **improved**

- 11 candidates → **1 admitted, 4 refused, 6 not adopted** (§2), every refusal citing the pinned source that
  overturns the candidate and a flip condition that would reverse it. The single most load-bearing decision is
  `corpus/lessons/round-43.md:46`: the refused r10 inference is overturned by *this round's own pins* (S291,
  S293), not by preference.
- The collision guard produced a number and then measured its own limits (34 collisions; two blind spots; 10
  under-reported reserved-band ids), instead of reporting "no collisions" (§3).
- A duplicate-admission defect of the S045 class was avoided deliberately, not by accident: two pins duplicated
  held documents and the round cited the held rows (`corpus/lessons/round-43.md:61-64`).
- One artifact inconsistency survives inside the round and must ship with it — see F1. It does not overturn the
  verdict (the registry itself is consistent and the counter keys on documents, not on the map), but it is a
  discernment artifact that a later seat can trip over.

### 4.4 Axes — **unchanged** at base; **UNVERIFIED** at the data commit

`receipts/axis-base.txt:1-5` publishes all three axes at their maximum at base (navigation 59/59, calibration
63/63, operability 12/12, `checked=3 mismatched=0 rev=a35cfdf…`, `exit=0`). That receipt is the *base* one:
there is no `axis-after-data` receipt in `.ufo/waves/round-43/receipts/` (the directory holds `axis-base.txt`
and no other axis file), and the tip run is still a placeholder in the lesson's spot-check table
(`corpus/lessons/round-43.md:201` "axis + harm at the tip"). Because every axis sat at its maximum at base,
the honest statement is: no axis *could* improve on this round's receipts, and whether any axis row changed at
the data commit is **UNVERIFIED** here — not "unchanged" by measurement.

---

## 5. Findings (what the L1 must decide; no edit made by this seat)

**F1 — the id guard's renumber map is stale by one id for five documents, and it is the artifact a later seat
would reuse.** `.ufo/waves/round-43/assimilation/renumber-map.tsv` (committed `2a3707c`) maps the staged
documents to round-43 ids under the *pre-dedup* assumption that two duplicate pins (WindowRuleApplicator,
HyprCtl) would also be opened; `id-guard.md` §5 rows 4-8 therefore allocate:

| document | map says | landed registry says |
|---|---|---|
| `DefaultFloatingAlgorithm.cpp` (staged S302) | `S292` (pin) | **S291** |
| `Target.cpp` (staged S303) | `S293` (pin) | **S292** |
| `WindowTarget.cpp` (staged S304) | `S294` (pin) | **S293** |
| `GeometricMovableAnimated.cpp` (staged S305) | `S295` (pin) | **S294** |
| `~/.config/hypr/gkeep.conf` (staged S251) | `S297` (pin) | **S295** |

Evidence: `grep -E 'S30[0-9]' .ufo/waves/round-43/assimilation/renumber-map.tsv | cut -f1,3` prints
`S302 S292`, `S303 S293`, `S304 S294`, `S305 S295`; the landed rows at `1959770` read S291
`DefaultFloatingAlgorithm.cpp`, S292 `Target.cpp`, S293 `WindowTarget.cpp`, S294 `GeometricMovableAnimated.cpp`,
S295 `host-gkeep.conf` (`git show 1959770:corpus/SOURCES.md | grep -E '^\| S29[1-5] '`). The map's *own*
warning is the defect it now carries — `id-guard.md` §6 finding 4: "Any copy of a staged row that keeps its id
would silently point at a different document". The pre-dedup assumption itself is stated in the same file's
finding 1 ("If the round opens S291/S296 anyway" — the two duplicate pins the landed commit did not open).
`corpus/lessons/round-43.md:65-68` records the landed numbering and the reason; the map was never renumbered. **Impact:** a w2-or-later seat that opens rows through the map
would file five documents under ids that hold other documents. **Options:** annotate the map in place (it is
w2-writable territory only if the L1 says so), or have the lesson's §"Held rows instead of two new rows"
paragraph carry the mapping table as the correction (the lesson already carries the landing rule). Fixing this
is an L1 act; this seat did not touch the map.

**F2 — no control or axis receipt exists at the data rev; both receipts that exist are base-rev.** `ctl-c1.txt:1`
reads `rev=a35cfdf…`, `axis-base.txt:4` reads `rev=a35cfdf…`. The C1 controls carry to the landed tool by byte
identity (equal sha256, silent `cmp`), but the report must not describe a control run "at the data commit".
Same for the axis row (§4.4). This is a wording constraint, not a missing gate.

**F3 — the surface the round adds is scored by two counters and one checker, but the checker has no receipt at
the data commit.** `receipts/c1-after-data.txt` and `receipts/c2-after-data.txt` are executed at `1959770`;
`quality/check-locators.py` is executed only in w1 (`w1/ExecLocatorGate/receipt.txt`, quoted by M43-1/M43-7) and
in the wave's own seats. Its result on the landed entry is therefore **UNVERIFIED** in this draft; the counter's
own clause-g locators (10 ids, `receipts/c2-after-data.txt:21-30`) are the committed proxies.

**F4 — provenance nuance to state correctly in the report.** The data commit's tree contains no
`.ufo/waves/round-43/assimilation/` file and no w1 seat report; those are in `a47efeb`/`2a3707c` on top of it.
Any report sentence of the form "the data commit carries the assimilation receipts" would be false; "the
assimilation receipts are committed at `2a3707c`" is true.

**F5 — what the round did *not* establish, and the Frontier bullet says so.** No live gkeep window was observed
on the host session; the 420x500 floating observation is from the isolated round-27 oracle, which this seat did
not re-open. `receipts/live-geometry-host.txt` is a null observation (`matched=0`, rc 3) on four tiled clients.
The report must not present the tool's live run as evidence about gkeep's size.

---

## 6. UNVERIFIED by this seat (do not upgrade)

1. `quality/check-locators.py` run over the landed entry at `1959770` — **UNVERIFIED** (F3); no receipt under
   `.ufo/waves/round-43/receipts/`.
2. Axis and harm at the data rev or the tip — **UNVERIFIED** (F2, §4.4); only `axis-base.txt` exists.
3. Any control run at `1959770` — **UNVERIFIED** (F2); controls are base-rev plus byte identity.
4. The four REFUSE grounds themselves — read as *text* (`corpus/lessons/round-43.md:46-49`, ledger `:70-84`); the
   package files in `merge/mado/knowledge/corpus/knowledge/` were **not** re-opened by this seat, and the
   quarantine slice/verdicts (`assimilation/quarantine-verdicts.md`, 13 rows) were read only for its counts.
5. The isolated round-27 oracle observation behind the 420x500 claim — **not** re-run (host-safety scope).
6. Tooling: nothing was installed by this seat (no package transaction was run; `pacman` is paused host-wide).
7. No seat was spawned and no background job was started; no scratch tree was created, so none is left to reap.

## 7. Reproduction index

- Rows/before-after, tier deltas, touched rows: §1 commands, all `git show <rev>:corpus/SOURCES.md` based.
- Frontier claim (10 insertions, 0 deletions; one new route; four open items): `git -C . diff --numstat a35cfdf 1959770 -- corpus/README.md`
  and `git -C . show 1959770:corpus/README.md` lines 71, 294-303.
- Assimilation counts: `corpus/lessons/round-43.md:45-49` and the ledger table `:70-84`.
- Guard: `.ufo/waves/round-43/assimilation/id-guard.md` §1-§6, with `reg-ids`/`staged-ids`/`collisions` beside it.
- Counter verdicts: `receipts/c1-after-data.txt:49-50`, `receipts/c2-after-data.txt:31-33`,
  `receipts/c2-v1-after-data.txt:32`, `receipts/ctl-c1.txt:1,50`, `receipts/ctl-c2.txt:76`, `receipts/ctl-c2-v2.txt:76`.
- Tool identity: `sha256sum tools/mado-geometry.py .ufo/waves/round-42/c1/ctl-ref-tool.py.txt` → equal
  `e3c2e471…`; `cmp` silent. Live run: `receipts/live-geometry-host.txt:1-11`.
- The seat's own re-derivation of every figure above: `python3 -I .ufo/waves/round-43/w2/ScribeReportDraft/verify.py`
  → `verify.txt` (90 checks PASS, rc 0). It reads committed blobs and receipts only; it writes nothing.

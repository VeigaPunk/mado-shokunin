# R56W2RevHarmWatch — round 56 harm watch at 28fc86ac2359ec27406d8a2c63bef82ea6e947ed

**Seat**: R56W2RevHarmWatch (leaf member; no subagent dispatch).
**Attack**: round 56 must harm no axis. Every gate re-run at the content revision
`28fc86ac2359ec27406d8a2c63bef82ea6e947ed` and at the base `13f0acbe3a15da2d9c08357a576d91dcadc85273`,
each compared to the base value and to the round-56 baseline receipt.

**Verdict**: round 56 does **not** harm the shipped axis gates — every read-only gate at the
content revision is equal to or better than at the base. But the attack surfaces **three
registered instruments that are blind to shipped content**, and **one gate that goes red for a
reason the round never published**. Severity of each is given below.

Scratch root: `/fast/scratch/hyaku/mado-r56/R56W2RevHarmWatch/` (removed before yield).
Exports: `git archive 28fc86ac` → `tmp_new/`, `git archive 13f0acbe` → `tmp_base/`.
Fixture repos: `fx2-pTBL` (shared clone of the lane, branch `fixture` at 28fc86ac, base reachable
so the C3 `base_pairs` hash check can run) and `fx3-*` (post-launch-edit clone).
All mutation fixtures are **copies**; no lane or fleet tracked file was written, no git/jj
mutation of the lane was made. `git -C "$D" rev-parse --show-toplevel` was asserted to equal the
fixture dir before each first commit; commits use `-c user.name=ctl -c user.email=ctl@ctl`.

---

## 1. Gate-by-gate: content revision vs base

### 1.1 `tools/mado-verify.sh --selftest` — UNCHANGED (no harm)

```
$ cd tmp_new && bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 460/460 assertions passed
EXIT=0

$ cd tmp_base && bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 460/460 assertions passed
EXIT=0
```

Baseline receipt `.ufo/waves/round-56/receipts/selftest-before.txt` = `MADO_SELFTEST: 460/460
assertions passed` / `rc=0`. **Identical at base, content revision and the frozen baseline.**
No harm. (The tool's own `--selftest` is unchanged between the two revs: the diff
`git diff 13f0acbe 28fc86ac -- tools/mado-verify.sh` is empty — `tools/mado-watchplan.py` is a
**new** file, not an edit to the gate.)

### 1.2 `scripts/sources-census.sh validate` — rc 0 both, **4 new W lines + 1 changed W line**

The lane's own working tree is the registry here (as the seat notes): `corpus/SOURCES.md` in the
working tree is **byte-identical** to `28fc86ac` (`git diff --stat 28fc86ac -- corpus/SOURCES.md
corpus/README.md` → empty), so the census result is the content revision's, not a dirty-tree
artefact.

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
... mado  W01  S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md, corpus/knowledge/request-limits-upstream-r31.md
... mado  W04  S384 duplicate url .../src/config/values/ConfigValues.cpp across scopes
... mado  W04  S387 duplicate url .../src/config/legacy/ConfigManager.cpp across scopes
... mado  W04  S388 duplicate url .../src/helpers/MiscFunctions.cpp across scopes
... mado  W04  S389 duplicate url .../src/debug/HyprCtl.cpp across scopes
mado  ok  /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
rc=0
```

Base tree (`--file tmp_base/corpus/SOURCES.md --root tmp_base`) gives **28 W04 + 1 W01 + ok, rc=0**;
content revision gives **32 W04 + 1 W01 + ok, rc=0**. Against the round's own baseline receipt
`receipts/census-before.txt` (31 lines, rc=0) the delta is exactly the lines above.

**New census lines at the content revision (5):**

| code | id | content | severity |
|---|---|---|---|
| W04 | S384 | duplicate url `.../src/config/values/ConfigValues.cpp` across scopes | **weakens the claim** |
| W04 | S387 | duplicate url `.../src/config/legacy/ConfigManager.cpp` across scopes | **weakens the claim** |
| W04 | S388 | duplicate url `.../src/helpers/MiscFunctions.cpp` across scopes | **weakens the claim** |
| W04 | S389 | duplicate url `.../src/debug/HyprCtl.cpp` across scopes | **weakens the claim** |
| W01 | S277 | `tierC mined used-by=` now lists **two** paths (was one) | **weakens the claim** |

**No new E line.** Census exit stays 0 and the lane stays `ok`.

Analysis:
* The four new W04s are the *same* upstream file pinned under two scopes — S384 vs S318
  (ConfigValues.cpp), S387 vs S303/S317 (ConfigManager.cpp), S388 vs S321 (MiscFunctions.cpp),
  S389 vs S307/S320/S366 (HyprCtl.cpp). Round 56 re-used already-registered upstream URLs for a
  second scope. The census contract treats duplicate URL+scope as **E04 (error)** and same URL
  across *different* scopes as **W04 (warning)**; these are genuinely different scopes, so W04 is
  the right code and the round is not in violation. But the round's **own claim in
  `claims-frozen-v2.md` §C1 names `new_rows=8/8`** and the registry grew 319 → 328 rows; the
  lane has never published a note that round 56's new rows deliberately re-use four URLs already
  registered under other scopes. Nothing in the frozen contract forbids it; the census does not
  forbid it; it is simply an undeclared consequence of the new rows.
* The changed W01 (S277) is the **C3 fill showing through the census**: the C3 fix added
  `corpus/knowledge/request-limits-upstream-r31.md` to S277's `used-by`. `request-limits-upstream-r31.md`
  cites S277 at line 31 (`S277 \`:61\``), so the CITE token rule picks it up as a real back-reference
  and the fill is *required* by the frozen C3-v2 definition — it is not a census defect. But the
  census's W01 makes it visible that a **tier-C community** row (S277, tier C) now carries a
  second relied-upon entry. The frozen contract's C3-v2 lets any CITE token become a used-by
  assertion, with only a 24-row name-only allowlist as an exemption; S277 is not on that
  allowlist, so it was filled. The entry's own line 31 text says S277's cap is **not** upstream's
  — the text *names* S277 to distinguish it. Whether that is "reliance" or "name-only" is exactly
  the judgement the two wave-1 readers split on, and the C3-v2 allowlist froze 24 such pairs —
  S277 was **not** among them. This is the class the C3-v2 definition was designed to expose, and
  the round filled it anyway. **Weakens the claim** (calibration axis).

### 1.3 `quality/check-index.py` — index 70 → 71, no harm

```
new: MADO_INDEX: rev=28fc86ac... indexed=71/71 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   rc=0
base: MADO_INDEX: rev=13f0acbe... indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10   rc=0
```
**The knowledge-entry/index count 70 → 71 asked for by the seat is confirmed** (and the seat's
"70 → 71" is right: `corpus/knowledge/hyprland-config-autoreload-r56.md` is the one added entry —
`git diff --name-status 13f0acbe 28fc86ac -- corpus/knowledge/` → `A` only, **no existing entry
text changed**, which is the C3-v2 "no change to any entry text" requirement, verified).
`--root tmp_new` reproduces `indexed=71/71`.

### 1.4 `quality/check-index-rows.py` — **base was RED, content revision is GREEN (no harm)**

```
new:  MADO_INDEX_ROWS: rev=28fc86ac... rows=71 errors=0 warns=3   rc=0
base: MADO_INDEX_ROWS: rev=13f0acbe... rows=70 errors=3 warns=3   rc=1
      ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52.md at line 80
      ERROR row-outside-map: knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md at line 81
      ERROR row-outside-map: knowledge/hyprland-keyboard-repeat-numlock-r55.md at line 82
```
The base had **three pre-existing errors**: a stray blank line inside the coverage-map table
(`git show 13f0acbe:corpus/README.md` lines 78-83 show a blank line between the r51 and r52 rows)
split the table into two regions, so `table_region()` (which stops at the first non-`|` line) cut
the region short and three rows fell outside it. Round 56's README integration removed that blank
line (`0ff41272`, the `-` hunk in the README diff), which **fixed** all three. Not a harm — an
unrequested side-effect improvement. `check-index-rows` is a QUALITY gate that was failing at the
base and is now green; the lane's own commit message does not mention it.

### 1.5 `quality/check-tool-ledger.py` — population 90 → 97, all covered (no harm)

```
new:  LEDGER: population=97 ledger_rows=97 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET   rc=0
base: LEDGER: population=90 ledger_rows=90 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET   rc=0
```
The seven new tracked instruments (`tools/mado-watchplan.py`, `quality/counters/c1-r56-autoreload-entry.py`,
`quality/counters/c3-r56-used-by.py`, `quality/check-r56-controls.py`, `quality/r56_ctl_c1.py`,
`r56_ctl_c2.py`, `r56_ctl_c3.py`) all have ledger rows. **No harm.**

### 1.6 `quality/check-evidence-pointers.py` — byte-identical at both revs (no harm)

```
new:  PRED-PTR-r36-v1 rev=28fc86ac... pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=35
      dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1
      setup=ok verdict=TARGET_MET   rc=0
base: PRED-PTR-r36-v1 rev=13f0acbe... (identical field values)   verdict=TARGET_MET   rc=0
```

### 1.7 `quality/check-axis-scores.py` — navigation axis **STALE at both revs** (pre-existing, not a round-56 harm)

```
new:  MADO_AXIS_ROW: axis=navigation  published=66/66 derived=71/71 verdict=STALE
      MADO_AXIS_ROW: axis=calibration published=86/86 derived=86/86 verdict=MATCH
      MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
      MADO_AXIS: checked=3 mismatched=1 rev=28fc86ac...   rc=1
base: MADO_AXIS_ROW: axis=navigation  published=66/66 derived=70/70 verdict=STALE
      (calibration and operability MATCH, identical)
      MADO_AXIS: checked=3 mismatched=1 rev=13f0acbe...   rc=1
```
The navigation axis was **already STALE at the base** (published 66/66 vs derived 70/70) and is
**still STALE** after round 56 (published 66/66 vs derived 71/71). The gap widened by exactly the
one new entry. The last axis publication in `SCORECARD.md` is
`Axis table re-derived at \`a582e0e5\` ...: navigation 66/66; calibration resolved-active 86/86;
operability selftest 12/12` — round 50's. **Round 56 did not publish a new axis table**, and the
round-56 SCORECARD section at `28fc86ac` is still `### Planned (round 56; intent only)` with three
planned items and no closure rows. This is *the same* pre-existing staleness the base carried,
not a new red — but round 56 added the 71st entry and left the published count at 66. Severity:
**weakens the claim** (navigation axis publication is one entry further behind). Note the lane
tip `19be88b6` also has no round-56 axis publication (`git show HEAD:SCORECARD.md | grep "Axis
table re-derived at" | tail -1` is still `a582e0e5`), so this is an open records item, not a
regression introduced at `28fc86ac`.

### 1.8 `quality/check-session-material.py` — identical finding counts (no harm)

```
new:  SESSION_MATERIAL: files=27734 findings=244   (SESSION_MATERIAL_WAIVED: findings=49 files=47)   rc=1
base: SESSION_MATERIAL: files=27508 findings=244   (SESSION_MATERIAL_WAIVED: findings=49 files=47)   rc=1
```
Same 244 findings, same 49 waived, same 47 waived files, both rc=1 (pre-existing). The 226 extra
scanned files are the round-56 evidence tree; **no new session material** was introduced.

### 1.9 `quality/check-round-outcome-first.py` — identical (no harm)

```
new:  OUTCOME_FIRST: round=56 verdict=SKIP line=0 surface=none process_tokens=0 reasons=no-section
      OUTCOME_FIRST_SUMMARY: rounds=56 pass=4 fail=38 skip=14   rc=1
base: (identical, including round=56 SKIP)                        rc=1
```
Round 56 reads `SKIP` at both revs because `SCORECARD.md` has no round-56 *closure* section yet.
Pre-existing shape (rounds 54 and 55 also FAIL this gate). Not a round-56 harm.

### 1.10 `quality/check-wave-done.py --round 56` — MISSING at both revs, and MISSING for round 55 is GREEN

```
new:  SCOPE round=56 markers=0 note=no-launch-marker: committed evidence without a .ready; ...
      MADO_WAVE_DONE: round=56 waves=0 settled=0 verdict=MISSING   rc=1
base: SCOPE round=56 markers=0 note=round-absent: no committed evidence of this round at the revision
      MADO_WAVE_DONE: round=56 waves=0 settled=0 verdict=MISSING   rc=1
control (round 55, both revs):
      WAVE wave=w1 ready=1 results=present seats=40 dispatched=40 settled=40 verdict=OK
      WAVE wave=w2 ready=1 results=present seats=37 dispatched=37 settled=37 verdict=OK
      MADO_WAVE_DONE: round=55 waves=2 settled=2 verdict=OK   rc=0
```
Round 55's `.ready` markers are committed (`git ls-tree -r 28fc86ac .ufo/waves/round-55/ | grep
ready` → 4 files); round 56's are **not** — at `28fc86ac` only `w1.ready`/`w1.ready.dispatched`
exist in the working tree and **no** `.ready` is committed at all (`git ls-tree -r --name-only
28fc86ac .ufo/waves/round-56/ | grep -i ready` → empty). The gate therefore cannot score round 56
from committed bytes and says so honestly (`no-launch-marker`). Round 56's wave markers are
untracked working-tree files, so this is a **records gap**, not a gate regression (rc=1 at both
revs).

### 1.11 `quality/check-freeze-order.py` — round 56 w1 OK, w2 registry not committed at 28fc86ac

```
new:  MADO_FREEZE_ORDER: round=56 wave=w1 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00
      launch=2026-10-29T00:22:47.615Z verdict=OK reason=ok   rc=0
base: MADO_FREEZE_ORDER: round=56 wave=w1 freeze=none ... reason=no_freeze   rc=1   (base has no round-56 freeze)
new:  MADO_FREEZE_ORDER: round=56 wave=w2 ... launch=none verdict=FAIL reason=no_registry   rc=1
      (at lane tip 19be88b6: freeze=3423ae285676 launch=2026-10-29T01:04:27.541Z verdict=OK reason=ok   rc=0)
```
The v1 freeze (3423ae28, 2026-10-28T21:19:17-03:00 = 2026-10-29T00:19:17Z) precedes the wave-1
launch (2026-10-29T00:22:47.615Z) — correct order. **The v2 re-registration (323a69c9,
2026-10-29T00:44:35Z) was committed ~22 minutes *after* the wave-1 launch** but ~20 minutes
*before* the wave-2 launch. That matches `registration-v2.md`'s own statement ("written after
wave 1 settled and BEFORE the real C1 entry ... were integrated"), and v2's byte-identity is
intact (`git rev-parse 323a69c9:<file>` == `git rev-parse 28fc86ac:<file>` for
`claims-frozen-v2.md`, `registration-v2.md`, `frozen-tables-v2.json`, `c3-name-only.tsv`,
`ctl/sibling-reader.py` — all SAME). See **§3** for the gap this exposes in the freeze-order gate.

### 1.12 `quality/check-population.py` — **does not run on round 56** (registration format, not a round-56 harm)

```
$ python3 -I quality/check-population.py --registration .ufo/waves/round-56/registration.md <receipt>
POPULATION verdict=UNREADABLE registration=.../round-56/registration.md reason=no **PRED-...** sentence with a supported target   rc=2
```
The round-56 registration carries `**Predicate (PRED-C1-r56, frozen sentence):**` markers, not the
`**PRED-<id>**` form the gate parses (`grep -c '\*\*PRED-'` = 0 in every round-48..56
registration). The gate itself is healthy — it passes on a round-26 registration:
```
$ python3 -I quality/check-population.py --registration .ufo/waves/round-26/registration.md \
      .ufo/waves/round-26/quality/population-fixtures/receipt-c1-green.txt
POPULATION ... pred=PRED-C1-r26 cases_pass=41/41 case_lines=41 registered=41 agree=ok
POPULATION verdict=PASS receipts=1 agree=1 mismatch=0 unreadable=0   rc=0
```
**This check did not run against round 56** — it cannot bind a round whose registration has no
`**PRED-**` sentence. Same at base (the base has no round-56 registration at all). Pre-existing
format drift since round 48, not a round-56 regression. Reported for completeness.

### 1.13 `quality/check-state-cite.py` — **fails identically at both revs** (pre-existing)

```
new:  CLAIM_UNPARSED .../round-50/claims.md:39   CLAIM_UNPARSED ...:40
      CHECK100: claims=34 set=0 readonly=0 unresolved=34 contradicted=0 verdict=FAIL   rc=1
base: identical output, identical rc=1
```
Round 56 ships **no claims file** for this gate (`git ls-tree -r 28fc86ac .ufo/waves/round-56/ |
grep -i claim` → only `claims-frozen.md` and `claims-frozen-v2.md`, the frozen predicate
sentences, not a `S100 claim=...` file). The gate is a round-50 prototype against round-50
fixtures. **Unchanged between revs → no harm**, but round 56 has no QUALITY-100 claim file.

### 1.14 Counter and tool selftests — all green, and the C2 hold-out commitment still binds

```
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --selftest --repo <lane> --rev 28fc86ac... --work <scratch>
242/242 assertions passed   rc=0
$ python3 -I quality/counters/c3-r56-used-by.py --selftest --repo <lane> --rev 28fc86ac... --work <scratch>
MADO_USED_BY_SELFTEST: 16/16 assertions passed   rc=0
$ python3 -I tools/mado-watchplan.py --selftest
MADO_WATCH_SELFTEST: 82/82 assertions passed   rc=0
```
The C1 counter's `--selftest` **requires `--repo`/`--rev`** (bare `--selftest` in a non-git cwd
fails with `setup error: rev does not resolve to a commit: HEAD`, rc=2 — the documented
behaviour, the selftest needs a source rev carrying the frozen tables).

**The hold-out commitment still binds the revealed hold-out** (independently recomputed, not taken
from the harness):
```
holdout computed: 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183
holdout frozen  : 65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183   MATCH
fixture computed: a9f552511cc4939e3c83190e7ca55a09d5f01dd520c59b3a6feeba2e0c4647d6
fixture frozen  : a9f552511cc4939e3c83190e7ca55a09d5f01dd520c59b3a6feeba2e0c4647d6   MATCH
tables sha256   : 9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2   (== the sha in claims-frozen-v2.md)
allowlist sha256: 70653e095839dc82f248d77fa5a0117134406a8b9e23778d2d79bf7072c948ee  (== c3.allowlist_sha256)
```

### 1.15 The lane's own reported claim lines reproduce at 28fc86ac

```
MADO_AUTORELOAD_ENTRY: rev=28fc86ac... rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none   rc=0
MADO_USED_BY: rev=28fc86ac... entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none   rc=0
MADO_R56_CONTROLS: claim=c1 good=ok controls=12/12 verdict=OK   rc=0
MADO_R56_C2: rev=28fc86ac... fixtures=18/18 holdout=8/8 holdout_commit=ok controls=4/4 verdict=TARGET_MET   rc=0
MADO_R56_CONTROLS: claim=c3 good=ok controls=9/9 verdict=OK   rc=0
```
All five match the lane's report exactly. **The lane's numbers are honest.**

### 1.16 The C3 registry edit touched cell 11 only — the C3-v2 requirement holds

Independent cell-by-cell diff of `corpus/SOURCES.md` base → content revision:
```
base rows: 319   new rows: 328
added:   S383 S384 S385 S386 S387 S388 S389 S390 S391
removed: []
changed pre-existing rows: 23
cell-number histogram of changed cells: {11: 23}
NON-cell-11 changes: 0
```
Every one of the 23 changed rows changed **cell 11 (`used-by`) only**; no cell 1-10 was touched.
And the round's own `receipts/used-by-old-to-new.md` reconciles **exactly** with the git diff
(23/23 rows match old and new values; 0 mismatches; 0 rows changed in git but absent from the
receipt; 41 added pairs). **No harm; the CORPUS rule-2 old→new logging is complete.**

---

## 2. DEFECTS — the instruments that are blind to shipped content

These are not "the gate went red". These are **registered instruments that report TARGET_MET on
shipped content they do not actually check**, which is the same class the wave-1 disclosure called
out ("a counter that sniffs its environment, caches runs or forges a consistent tree passes a
non-adversarial harness"). All were proven by mutation on a **copy**.

### D1 — `Hyprland-PropRefresher.hpp` is a shipped pin with **no frozen sha256**; corrupting it does not fail C1. **BLOCKING the C1 claim's pin integrity.**

The entry quotes this pin in rows **E08** and **E09** (the `REFRESH_CONFIG_WATCHER` bit-8 /
`REFRESH_ALL` declarations). The file ships at
`.ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp` (1322 B) and is registered as row **S391**.
But `frozen-tables-v2.json` `c1.pin_sha256` has **8** keys and `Hyprland-PropRefresher.hpp` is
**not** one of them:
```
$ python3 -c "import json; ft=json.load(open('.../frozen-tables-v2.json')); \
   print('PropRefresher.hpp in pin_sha256?', 'Hyprland-PropRefresher.hpp' in ft['c1']['pin_sha256']); \
   print('in pin_suffix?', 'Hyprland-PropRefresher.hpp' in ft['c1']['pin_suffix']); \
   print('in rev_rule?',  'Hyprland-PropRefresher.hpp' in ft['c1']['rev_rule'])"
PropRefresher.hpp in pin_sha256? False
in pin_suffix?      False
in rev_rule?       False
```
Nor is `S391` in `c1.new_row_ids` (`['S383'..'S390']`, 8 ids) and `S391` appears **zero times** in
any frozen contract file (`claims-frozen.md`, `registration.md`, `claims-frozen-v2.md`,
`registration-v2.md`, `frozen-tables.json`, `frozen-tables-v2.json`, `c3-name-only.tsv` — all 0
hits; `PropRefresher.hpp` likewise 0 hits).

**Mutation (on the shared-clone fixture, base reachable):**
```
MUTATION A: corrupt the PropRefresher.hpp pin bytes (E08/E09's pin; NOT in frozen pin_sha256)
  python3 - <<'EOF'
  p=".ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp"
  b=open(p,'rb').read(); open(p,'wb').write(b.replace(b"REFRESH_CONFIG_WATCHER",b"REFRESH_CONFIG_WATCHXR"))
  EOF
  git commit -am "mutA: corrupt PropRefresher.hpp"
$ python3 -I quality/counters/c1-r56-autoreload-entry.py --repo <fixture> --rev HEAD --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=HEAD rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
rc=0
```
**The counter stays green with the pin corrupted.** The `pin_hash` leg iterates `pins_all = dict(c1["pin_sha256"]); pins_all.update(c1["host_pin_sha256"])` — the unregistered pin is simply never hashed. (The *actual* bytes are fine: the on-disk file hashes to
`37acaaf16a24dcfe89d0702818b82d300d0da5e91ef1ba47494f7fd2ab0af2d0`, which **matches** the sha256
S391's anchor cell records, and E08/E09's quotes are verbatim at the cited lines — I checked all
42 entry rows and **0** have a quote missing from its cited pin line. So this is a **gate blind
spot**, not a false statement in the corpus.)

Compounding it: `S391`'s registry row is checked by **no** C1 leg either. `source_cell` and
`scope` are evaluated only for `c1["k"]` rows, and S391 is cited only by E-rows, which the
counter never parses (`K_IDS = K01..K30`, `H_IDS = H01..H03`; there is no `E` id list anywhere in
the counter).

**Severity: blocking the C1 claim's pin integrity.** The registration's `pin_hash` leg is defined
as "every pin blob at --rev hashes to its frozen sha256"; the shipped entry quotes a pin that the
frozen table does not contain, so that leg cannot cover it. The claim line
`MADO_AUTORELOAD_ENTRY: ... content=33/33 new_rows=8/8 verdict=TARGET_MET` is **literally true**
but it is true of a claim surface that omits 9 of the entry's 42 rows and 1 of its 12 pins.

### D2 — the 9 "E" rows are outside every C1 leg; the entry has **42** propositions, the claim counts **33**. **BLOCKING the C1 coverage claim.**

The entry's rows, parsed by the registration's own grammar (5 cells, ` | ` separator, outside
fences):
```
5-cell rows: 42   {'K': 30, 'H': 3, 'E': 9}
K ids: complete K01..K30   H ids: H01 H02 H03
E ids: E01 E02 E03 E04 E05 E06 E07 E08 E09
rows whose quote is NOT at the cited pin line: 0
```
The frozen denominators are `rows=30 hosts=3 content=33 new_rows=8`. **Nine propositions
(E01-E09) are in the shipped entry and are counted by no leg** — not `row:`, not `quote:`, not
`tok:`, not `num:`, not `echo:`, not `scope:`, not `source_cell:`. The entry is honest about it
in prose ("Extra rows (not counted; facts beyond the frozen anchors, each with its own pin line)"),
and `claims-frozen-v2.md` scopes C1 to "30 upstream claims (K01-K30) and 3 host claims (H01-H03)"
— so the **sentence** is not false. But two of the nine (E08, E09) are the *only* rows that cite
S391, and E-rows are where the "unregistered pin" of D1 surfaces. `content=33/33` is a saturation
claim over 33 of 42 shipped propositions.

**Severity: blocking the C1 coverage claim as an axis number.** `content=33/33` and
`rows=30/30` are denominators the reader will read as "the entry is fully covered"; it is not.

### D3 — the C3 `lost` leg cannot see a coordinated delete outside the 65 base-missing pairs. **WEAKENS the C3 claim (partly disclosed by E12).**

`registration-v2-errata.md` **E12** discloses that `lost` is defined over the 65 base-missing
pairs rather than all 381, and says "deleting a citation of one of the other 316 pairs is not
(it cannot reduce `missing`)". The errata discloses the *one-sided* delete. It does **not**
disclose that a **coordinated** delete (citation *and* back-reference removed together) of a pair
**outside** the 65 is invisible to *every* leg — `missing`, `extra`, `dangling`, `conflict`,
`stale`, `lost` all stay at 0.

```
MUTATION G: coordinated delete of (S158, corpus/knowledge/rule-attribution-r24.md)
  (that pair was already in S158's used-by AT THE BASE, so it is outside the 65)
$ python3 -I quality/counters/c3-r56-used-by.py --repo <fixture> --rev HEAD --work <scratch>
MADO_USED_BY: rev=HEAD entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none
rc=0
```
Contrast the two neighbours, to show the boundary is exactly the 65:
```
MUTATION F: citation-only delete, back-reference kept   -> missed=extra   (rc=1)
MUTATION H: coordinated delete of (S015, walker-route-r18.md), a pair inside the 65
                                                          -> missed=lost    (rc=1)
MUTATION G: coordinated delete of a pair outside the 65  -> verdict=TARGET_MET (rc=0)   <-- blind
```
`base_pairs()` in the counter computes `pl = {k: v for k, v in pl0.items() if k[1] not in ub0[k[0]]}`
— the base **missing** set — and the counter's `lost` leg is `base_pairs(repo, work, t) - set(pairlines)`.
So `lost` only fires for pairs that were missing at the base. A pair that was *already* linked at
the base can be silently un-linked (both sides) and the counter reports a clean
`TARGET_MET ... missed=none`.

**Severity: weakens the C3 claim.** It is partly disclosed (E12 covers the one-sided case and
names the 65-pair limitation), but the coordinated case is a strictly stronger hole than the one
disclosed and is not in the errata. The C3 claim sentence asserts `lost=0` as a TARGET_MET
condition; `lost=0` here does not mean "no reliance record was destroyed".

### D4 — the freeze-order gate does not police the **v2** contract files. **WEAKENS the freeze-order guarantee.**

`quality/check-freeze-order.py` has `REQUIRED = ("claims-frozen.md", "registration.md")` and
`OPTIONAL = ("frozen-tables.json",)`. **No v2 filename appears.** The gate's `freeze_edited:<file>`
detection is therefore blind to `claims-frozen-v2.md`, `registration-v2.md`,
`frozen-tables-v2.json`, `c3-name-only.tsv` and `ctl/sibling-reader.py` — the five files wave 2
actually attacks.

```
$ git clone --shared <lane> fx3 && git checkout -b fx3 19be88b6
$ printf '\n<!-- post-launch edit -->\n' >> .ufo/waves/round-56/registration-v2.md
$ printf '\n<!-- post-launch edit -->\n' >> .ufo/waves/round-56/claims-frozen-v2.md
$ git commit -am "post-launch edit of v2 contract files"
$ python3 -I quality/check-freeze-order.py --repo fx3 --rev HEAD --round 56 --wave w2
MADO_FREEZE_ORDER: round=56 wave=w2 freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=2026-10-29T01:04:27.541Z verdict=OK reason=ok
rc=0
```
Editing both v2 contract files **after the wave-2 launch** still yields `verdict=OK reason=ok`.
The lane is clean today — `git log -- .ufo/waves/round-56/<v2 file>` shows each v2 file touched by
exactly **one** commit (`323a69c9`), and the blobs are byte-identical at `28fc86ac` — so this is
a **latent** gate hole, not a violation.

**Severity: weakens the claim** (the gate that certifies "the contract was frozen before the wave
launched" does not cover the contract wave 2 runs against).

---

## 3. Residual risk and verification gaps

* **Not verified (out of this seat's scope, other wave-2 seats own them)**: upstream byte
  identity of S383-S391's URLs (I read the lane's local pin bytes only; I did not fetch
  `raw.githubusercontent.com`); the sentence-to-pin *entailment* of the 33 counted propositions
  (registration-v2 declares this out of the counted claim); the reliance-vs-name-only judgement
  for the 41 filled C3 pairs; the wave-1 reports' own claims.
* **Axis publication still open**: navigation published=66/66 vs derived=71/71 at the content
  revision, and the round-56 `SCORECARD.md` section is still "Planned (round 56; intent only)".
  A round-56 axis publication + closure rows are needed before `check-axis-scores.py` can go
  green; nothing at `28fc86ac` or at lane tip `19be88b6` does that.
* **Round-56 records not landed at the attacked revision**: no `corpus/lessons/round-56.md`
  (absent at `28fc86ac`, absent at lane tip `19be88b6`, absent in the working tree), no
  round-56 `.ready` committed, no round-56 SCORECARD closure section. `check-wave-done.py` cannot
  score round 56 from committed bytes for this reason.
* **Two gates could not run against round 56** and are reported as such: `check-population.py`
  (round-56 registration has no `**PRED-**` sentence — it passes on a round-26 registration, so
  the gate is healthy and the *format* drifted) and `check-state-cite.py` (round 56 ships no
  `S100 claim=` file; the gate FAILs identically at both revs on round-50 fixtures).
* **C2 hold-out** is revealed in the tree at `28fc86ac` (56 files under `fixtures/c2-holdout/`)
  and its commitment still matches the frozen sha256, but the *sealed* nature is gone: a future
  tool author can read it. The commitment binds the bytes; it does not bind "no one looked".
* **Tooling**: no tool was installed, upgraded or removed for this seat. Everything ran with the
  host's `python3 -I`, `git`, `bash`, `tar` and `sha256sum`. No pacman transaction was attempted
  (the host guard pauses pacman; the task needed no new tool).

## 4. Cleanup

All scratch (`tmp_new/`, `tmp_base/`, `work-*`, `fx2-*`, `fx3-*`, `r50-*`, receipts) lived under
`/fast/scratch/hyaku/mado-r56/R56W2RevHarmWatch/` and is removed before this yield
(`rm -rf` on the seat scratch root; verified absent). The only files written outside scratch are
this report, its receipts directory
(`.ufo/waves/round-56/w2/R56W2RevHarmWatch.md`, `.ufo/waves/round-56/w2/R56W2RevHarmWatch/receipts/`).

**The lane's tracked files, the fleet repo, sibling lanes and the shokuknow repo were not modified
by this seat.** For full disclosure: at the moment of writing, `git status --porcelain` in the
lane shows two **modified tracked files** — `corpus/SOURCES.md` and
`corpus/knowledge/hyprland-config-autoreload-r56.md` — with mtime `2026-10-28 22:31:09`, i.e.
**after** this report was written (22:30:24). They are **not mine**: I wrote only under the seat
directory and under the seat scratch root, and the diff is a sibling seat's concurrent wave-2 edit
(registry rows **S392-S395** added and the E-rows E01/E03/E04/E05/E06/E07 re-pointed from
S383/S387/S388/S389 to the new S392/S393/S394/S395). Its mtime is later than my last write, and
its content is another seat's scope repair. I did not touch it and did not revert it.

Note that this concurrent edit is *itself* relevant to §2 D1/D2: it re-points the E-rows onto
**four new registry rows (S392-S395)**, which is the shape of the fix for the E-row coverage gap —
but as of the scored revision `28fc86ac` those rows and that re-pointing do not exist, and the
C1 counter still does not parse E-rows or pin `Hyprland-PropRefresher.hpp`. All findings above
are scored strictly against `28fc86ac`, never against the working tree.

# R56W2CritFreezeV2 — chronology and pre-data attack on registration v2 (wave w2, critic, leaf)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Content revision attacked: `28fc86ac2359ec27406d8a2c63bef82ea6e947ed`. Freeze v2: `323a69c9`. Verdicts below cite commands; receipts are in `.ufo/waves/round-56/w2/R56W2CritFreezeV2/` (`receipts.txt`, `freeze-order.txt`, `usedby-before-v2.txt`, `base-missing-65.tsv`, `pairs_base.py`, `mk_m1_E12.py`, `e3_bound_test.py`, `holdout_commit_check.py`, `usedby_at.py`). Scratch under `/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/` (clone `m1/`, removed at yield). No lane tracked file, index, ref or fleet file was written; all git calls were read-only (`log`, `show`, `ls-tree`, `diff`, `archive`) or ran in a `git clone --shared` scratch clone. No tool installed or upgraded; no pacman; no `hyprctl`.

## Summary

| # | Item | Verdict | Severity |
|---|---|---|---|
| F1 | `lost` leg measures 65 pairs, not the registered PAIRS(base) of 381; the registered text cannot match its own frozen hash. Demonstrated: a deleted citation of a used pair passes `TARGET_MET`. | Unregistered predicate change, after a real-data run | **blocking the claim as written**; weakens once re-registered as a labelled change |
| F2 | Target clause "no change to any entry text" is unmeasured (follows from F1). | Not enforced by any leg | weakens |
| F3 | Post-freeze addition: registry row S391 and pin `fetch/Hyprland-PropRefresher.hpp` (commit `0ff41272`, after the freeze). Two evidence rows (E08, E09) rest on it; no frozen hash, no leg. | Unregistered change | weakens |
| F4 | The allowlist (24) exempts 4 pairs that the other wave-1 reader judged reliance or leaning reliance (union rule). | LOOSER; labels are the target (circular) | weakens |
| F5 | E3 bound is off by one: `len(blob.split(b"\n"))` = wc-l + 1; a locator one line past EOF is accepted. Control 12 uses `1-9999`, so it cannot catch this. | Registered formula itself is wrong | weakens (one line) |
| F6 | v2 says wave-1 "scored only synthetic trees and the base revision". The freeze tree `3423ae28` and `2aa347b1` were also scored with real-tree counters. | Disclosure inaccurate | cosmetic |
| F7 | `check-freeze-order.py` checks only the v1 freeze files. Its OK for w2 says nothing about v2. | Instrument blind to v2 | cosmetic (disclosure) |
| F8 | E8 "required verbatim": docstring item (7) differs in wording. | Non-verbatim | cosmetic |
| F9 | The errata calls E12 "disclosed, not a predicate change". It is one (see F1). | Mislabelled | cosmetic (disclosure) |

Chronology verdicts (item 1): v2 files first appear in `323a69c9` (committer 21:44:35). Every integrated real artifact first appears later (`2e39282e` 21:54:28 for the counters, tools, harness modules and the hold-out reveal; `0ff41272` 21:59:02 for the C1 entry and rows S383-S391). File birth times agree (c1 counter 21:45:07, c3 counter 21:49:56, watchplan 21:51:07, hold-out directory 21:54:21). **The freeze precedes every integrated real artifact: true.**

## 1. Chronology (item 1)

`git log --diff-filter=A --format='%h %cI %s' -- <path>` for each:

| artifact | first commit | committer time |
|---|---|---|
| claims-frozen-v2.md, registration-v2.md, frozen-tables-v2.json, c3-name-only.tsv, ctl/sibling-reader.py, freeze-verify-v2.py | `323a69c9` | 2026-10-28T21:44:35-03:00 |
| quality/counters/c1-r56-autoreload-entry.py, c3-r56-used-by.py, quality/check-r56-controls.py, quality/r56_ctl_c1/c2/c3.py, tools/mado-watchplan.py, fixtures/c2-holdout (56 files) | `2e39282e` | 21:54:28 |
| corpus/knowledge/hyprland-config-autoreload-r56.md, registry rows S383-S391 (SOURCES.md), fetch/Hyprland-PropRefresher.hpp | `0ff41272` | 21:59:02 |
| registration-v2-errata.md, make-w2-spec.py | `15015e77` | 22:04:18 |
| w2 dispatch and registry | `19be88b6` | 22:04:27 (createdAt 01:04:27Z) |

Used-by fills: `git show <rev>:corpus/SOURCES.md` at `13f0acbe`, `2aa347b1` and `323a69c9` has identical used-by cells (0 changed; `usedby-before-v2.txt`). Fills start after the freeze.

## 2. Real-data runs before the freeze (item 2)

Answer: **"no real counter or tool ran on real data before 323a69c9" is false as stated.** The lane's integrated tools did not run before the freeze (their births are after 21:44:35). Wave-1 seat drafts did run real-tree counters before v2. Base and freeze trees count as real data (they are the lane's own committed objects). What each seat scored:

| tree | seat (time) | scored |
|---|---|---|
| base `13f0acbe` | R56ExecC3CounterA (21:28), R56CritCiteDef (21:30), R56RevC3Contract (21:32) | v1 C3 counter: `missing=65`, plus variant and mutation runs on scratch copies of base `corpus/` |
| freeze `3423ae28` | R56ExecC3CounterA (21:28), R56CritHoldout (21:29, committed fixtures via mini-harness with a synthetic hold-out stand-in), R56ExecC1CounterA (21:36, `entry_absent`), R56CritDoNothing (21:37) | C3 `missing=65`; **C3 `c3-delete-missing-cites` and `c3-strip-all-citations` both `TARGET_MET`** on the freeze copy; C1 `entry_absent` |
| `2aa347b1` (pre-entry) | R56ExecC1CounterB (21:29), R56RevC1Contract (21:36, `git archive` plus variants) | C1 `entry_absent`; C1 variant runs on synthetic entries |

Synthetic trees: R56CritDoNothing and R56RevC1Contract variant runs (`rev=HEAD` scratch repos). The `c3-delete-missing-cites` result on the freeze copy is the real-data observation that motivated v2's `lost` leg and the conflict/stale legs. So v2 was written after observing v1 counter results on real trees. "Pre-data" in v2 therefore means "before filled data and before integrated tools", which is true, and it should be stated that way.

## 3. E1–E11 classification (item 3)

Each entry is classified against the predicate it changes (TIGHTER = fewer things pass; LOOSER = more things pass; NEUTRAL = no effect on what passes).

| id | change | class | note |
|---|---|---|---|
| E1 | C1 control 8 leg `quote:K05` → `row:K05`, collateral legs allowed | NEUTRAL | predicate untouched; control becomes satisfiable, but any leg set containing `row:K05` passes |
| E2 | `source:`/`verified-at`/`recheck` must sit within line 15 (was 30) | TIGHTER | |
| E3 | locator bounded by pin line count | TIGHTER | off by one, see F5 |
| E4 | `echo:` leg for quotes ≥30 chars | TIGHTER | `content=33/33` still holds at 28fc86ac (lane report) |
| E5 | controls 10 → 12; control 2 requires a `tok:` leg | TIGHTER | control 12 tests `1-9999` only, not the boundary |
| E6 | staged layout for C2 fixtures | TIGHTER | removes the expected-file exposure (R56CritHoldout F1) |
| E7 | C2 controls 3 → 4 with `sibling-reader.py` | TIGHTER | sentence `controls=4/4` |
| E8 | divergence list replaced: `GLOB_TILDE` removed, items (4) realpath watch name, (5) duplicate watches and `watches=` counting, (6) Lua provider and runtime `hyprctl keyword misc:disable_autoreload` not modelled admitted | **LOOSER** | declared divergences exempt those behaviours from the fixtures; (6) covers the runtime keyword path that the entry is about; docstring wording differs (F8) |
| E9 | C3 `missing` over every token pair → name-only allowlist of 24; adds `conflict`, `stale`, `lost`, `allow_sha` | **LOOSER** on the headline `missing` (65 → 41 to fill); TIGHTER on the added legs | see §4 |
| E10 | `--work` honoured, nothing outside it | NEUTRAL | process |
| E11 | F12 note corrected; fixture bytes unchanged | NEUTRAL | |
| E12 (errata) | `lost` over 65 base-missing pairs, not PAIRS(base) | **LOOSER**, unregistered | see F1 |
| E13 (errata) | comma separator in used-by | NEUTRAL | counters accept both |
| E14 (errata) | no bare `content` leg | NEUTRAL | |
| unlisted (post-freeze) | S391 row and `Hyprland-PropRefresher.hpp` pin | unregistered addition | see F3 |

Freeze verifier: `python3 -I .ufo/waves/round-56/freeze-verify-v2.py` prints `FREEZE_VERIFY_V2: bad=0 ... OK` at both `323a69c9` and `28fc86ac` (scratch clone checkouts).

## 4. Allowlist (item 3, continued)

Is the 65 → 41 reduction a loosening? **Yes, on the headline `missing` leg.** A fill that leaves the 24 pairs unrecorded now passes, where v1 required them. Two checks:

- *Derived from pre-fill labels?* **Yes.** Labels: `R56CritCiteDef/pairs-65.tsv` mtime 21:30:59; `R56RevC3Contract/classification.json` and `pairs.md` 21:32:19; `c3-name-only.tsv` 21:42:32; `frozen-tables-v2.json` 21:43:46; freeze commit 21:44:35; first used-by fill `0ff41272` 21:59:02 (`usedby-before-v2.txt`: 0 changed before the freeze). All 65 labels were read from base lines (`pairs_base.py` reproduces `missing=65` and the frozen `sources_sha256_at_base`). The base revision is real data, so "pre-data" here means "before filled data", not "before real data".
- *Does the rule match the labels?* The v2 text says a row is exempt when one reader judged it name-only (`MIS` or `N`/`R`/`M-N`). This holds for all 24 rows (`cross-tab`, receipts §6). But the rule is a union, and it exempts 4 pairs that the other reader judged reliance or leaning reliance:
  - `S096 | config-health-report-r3.md` — RevC3 `MIS`, CritCiteDef `U`
  - `S044 | config-drift-r12.md` — RevC3 `MIS`, CritCiteDef `M-U`
  - `S113 | tripwire-binding-boundaries-r21.md` — RevC3 `MIS`, CritCiteDef `M-U`
  - `S359 | hyprland-dispatcher-dispatch-r51.md` — RevC3 `REAL`, CritCiteDef `M-N`

  Under an agreement rule, `missing` would be 45, not 41. The 41 remaining are `REAL`/`U` 35, `REAL`/`M-U` 5, `BORD`/`U` 1 (S046), so the "judged reliance by both" sentence holds.
- *Circularity.* The 41 to fill are exactly the readers' reliance labels, and the 24 exempt are exactly their name-only labels. TARGET_MET therefore measures agreement with the two labelling seats, not registry correctness. The text's "back-reference consistency (token level, reviewed)" wording is the honest label; the report must not describe the output as calibration.

## 5. Freeze text versus frozen hash (F1, E12)

**Frozen text and frozen hash disagree at the freeze commit itself.** `registration-v2.md` (committed `323a69c9`) defines `lost` over PAIRS(base) of the base revision and says the sorted `S###|path` lines "have sha256 `c3.base_pairs_sha256`". Computed from base `13f0acbe` (`pairs_base.py`):

- PAIRS(base) = 381; sha256 = `79545d6bc91df573a2cb24612d56d5b4705c92bc3dfad7a703ec31fe5aadd1b6`. Not the frozen value.
- base-missing = 65; sha256 = `630007b0a17540f45430068c9d9a38a731268e47e5fb9855887a7ae4f8d673ef`. **Equal to the frozen `c3.base_pairs_sha256`** (`frozen-tables-v2.json`, `base_pair_count: 65`).

So the frozen commitment is over 65 pairs, and the text cannot be satisfied with that hash. The first integrated counter (`2e39282e`) already implements 65 (docstring: "lost = the base `missing` pairs (registration-v2 E12; 65 at base)"). The errata says the first run failed closed on the hash and the counter was then aligned. No committed receipt shows that failure. The counter file's mtime is 21:49:56–21:50:20, so that window is all that is visible; the failing run is **unverifiable**.

Consequence, demonstrated on a scratch clone at `28fc86ac` (`mk_m1_E12.py`, counter run from `quality/counters/c3-r56-used-by.py`, `--work` scratch):

- **M1** (`312342783e2e`): delete the only citation of S002 in `corpus/knowledge/window-rule-effects-getprop.md` (`S002` → `S---`) and empty row S002's used-by.
  `MADO_USED_BY: rev=312342783e2e... entries=71 rows=328 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none` (exit 0).
- **M1b** (`32272b2a9562`): keep the citation, empty row S002's used-by only.
  `... missing=1 ... verdict=TARGET_MISSED missed=missing` (exit 1). `missing` catches the one-sided edit.
- Under the registered text, `(S002, window-rule-effects-getprop.md)` is in PAIRS(base) and absent from PAIRS(M1), so `lost=1` and M1 would be `TARGET_MISSED`.

So the measured `lost` is the 65-pair subset. Deleting a citation of any of the other 316 base pairs, together with its used-by cell, is not detected. That contradicts the registered claim, and the errata's "disclosed, not a predicate change" is wrong. The report must state the definition actually measured and label it as a predicate change made after a real-data run failed. Until then, `lost=0` in the output line does not mean what `registration-v2.md` says it means: **blocking the claim as written**.

F2 (weakens): the target sentence requires "no change to any entry text". No leg measures it. M1 changes entry text and returns `TARGET_MET`. At `28fc86ac` the entry text is unchanged from base except the new C1 entry: `git diff --name-status 13f0acbe 28fc86ac -- corpus/knowledge` lists only `A corpus/knowledge/hyprland-config-autoreload-r56.md`. That is a null result for the content revision, but the sentence is not enforced by the counter.

## 6. Post-freeze addition (F3)

Frozen: `registration-v2.md` "Recount of the unchanged rest: 30 K rows, 3 H rows, rows S383-S390"; `frozen-tables-v2.json` `c1.new_row_ids` has 8 entries (S383-S390); `c1.pin_sha256` has 8 pins, none is `Hyprland-PropRefresher.hpp`.

Found: `corpus/SOURCES.md` at `28fc86ac` has rows S383-S391 (9 new rows; 319 → 328). S391 = "Hyprland 0.56.2 property refresher header"; pin `.ufo/waves/round-56/fetch/Hyprland-PropRefresher.hpp` added in `0ff41272` (21:59:02), after the freeze. The entry cites S391 in its `source:` line (line 1) and in evidence rows E08 (line 128) and E09 (line 129).

Checks: E08's quote `REFRESH_CONFIG_WATCHER     = (1 << 8),` matches pinned line 18; E09's `REFRESH_ALL = …` matches line 21 (`git show 28fc86ac:...hpp | awk`). So the quotes are right against the bytes. The defect: the bytes are unfrozen (no hash in the freeze tables; `freeze-verify-v2.py` does not check them), the C1 counter's `new_rows=8/8` is blind to S391, and E08/E09 are not K or H rows, so no leg measures them. Severity: weakens; disclose as an unregistered addition.

## 7. E3 bound off by one (F5)

`quality/counters/c1-r56-autoreload-entry.py` at `28fc86ac`: `pin_lines[pin] = d.split(b"\n")`, `nlines = len(pl)`, so `nlines` = wc-l + 1 for a file ending in newline. `e3_bound_test.py` on `Hyprland-ConfigWatcher.cpp` (wc-l 111, len 112):

```
Hyprland-ConfigWatcher.cpp:100-111  line=100 nlines=112 -> scope_covers=True
Hyprland-ConfigWatcher.cpp:100-112  line=100 nlines=112 -> scope_covers=True   (line 112 is past EOF)
Hyprland-ConfigWatcher.cpp:100-113  line=100 nlines=112 -> scope_covers=False
```

E3 says "a locator past the end of the pin makes scope fail". Line 112 is past the end. Control 12 (`anchor-past-eof`) uses `1-9999`, which never tests the boundary. Severity: weakens; one line, but the registered formula is the error.

## 8. Other checks (null results, with commands)

- **Hold-out commitment** (item 2 supplement): `holdout_commit_check.py` runs `commitment()` from `quality/r56_ctl_c2.py` (at `28fc86ac`) on `fixtures/c2-holdout` extracted by `git archive 28fc86ac`: `65dc9d3e318b15e6c6b0dea6fe9a8f98814914d37e2b2973dc3b8b088d2cb183` = frozen `c2.holdout_commit_sha256`. **Match.** The revealed bytes are the pre-committed bytes.
- **Hold-out on the lane path during wave 1**: directory `fixtures/c2-holdout` has birth time 21:54:21 (`stat -c %w`). Its files keep 21:14:50 mtimes, so they were copied in at 21:54. No wave-1 seat's receipt shows a read of the lane path. The filesystem is `noatime`, so read history cannot be established. Unverifiable whether a pre-reveal copy existed elsewhere.
- **Post-freeze frozen-file changes**: `git diff --name-status 323a69c9 28fc86ac -- .ufo/waves/round-56 | grep -v '^A'` is empty. Only additions: 56 hold-out files and the hpp pin.
- **Registry diff** `13f0acbe` → `28fc86ac`: 23 existing rows changed, all in column index 10 (cell 11, used-by); 0 rows removed; 9 rows added.
- **E8 docstring**: items (1)–(7) present in `tools/mado-watchplan.py` at `28fc86ac`; item (7) reads "the value and line grammar is the hyprlang 0.6.8 subset of the registration", where E8 says "the value grammar and line grammar are the hyprlang 0.6.8 subset of this registration". Cosmetic (F8).
- **check-freeze-order** (item 4), `python3 -I quality/check-freeze-order.py --repo <lane> --round 56 --work <scratch>` (`freeze-order.txt`):
  - rev `9c3ca28a`, wave w2: `freeze=3423ae285676 freeze_time=2026-10-28T21:19:17-03:00 launch=none verdict=FAIL reason=no_registry` (exit 1). The w2 registry is not yet at that revision.
  - rev `9c3ca28a`, wave w1: `verdict=OK reason=ok`, launch 2026-10-29T00:22:47.615Z (21:22:47 local).
  - rev `19be88b6`, wave w2: `freeze=3423ae285676 ... launch=2026-10-29T01:04:27.541Z verdict=OK reason=ok`.
  - The FREEZE set is `claims-frozen.md`, `registration.md`, `frozen-tables.json` only. It never examines v2 (F7). By hand: `323a69c9` (21:44:35) precedes the w2 launch (22:04:27 local), and it follows the w1 launch (21:22:47), which is by design.
- **Not run by me**: `check-r56-controls.py --claim c1|c2|c3` (other seats and the lane's own run). I ran the C3 counter only on the scratch mutations above and the freeze verifier. The E8 harness and C1 counter boundary were read, not executed, beyond F5.

## 9. Unverifiable

- The errata's "first run failed closed on the hash, then aligned" (F1): no committed receipt; the first integrated commit already has 65.
- Whether any seat read a sealed hold-out copy outside the lane path (`noatime`; directory birth 21:54:21).
- Whether the two C3 readers are independent (both are wave-1 seats on the same base; not checked beyond their receipts).
- Hpp content against upstream commit `efb50993…`: no network; only the local bytes were compared (F3).

## Deliverables

- `.ufo/waves/round-56/w2/R56W2CritFreezeV2.md` (this report)
- `.ufo/waves/round-56/w2/R56W2CritFreezeV2/receipts.txt`, `freeze-order.txt`, `usedby-before-v2.txt`, `base-missing-65.tsv`, `pairs_base.py`, `mk_m1_E12.py`, `e3_bound_test.py`, `holdout_commit_check.py`, `usedby_at.py`

Tools: none installed or upgraded (no `pacman`, `uv`, `npm`, or release binary). Host reads: none beyond the lane's files and git objects.

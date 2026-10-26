# CritRoutedItems — routing-critic findings: R1-R4 before they land (round 47 w1)

Seat: `CritRoutedItems` (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Reviewed against lane rev `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (round-47 base; lane HEAD at
review time is `c24adef2` = the L1 dispatch commit on top of the base). Drafts reviewed:
`round-46/w1/ExecSessionTriage`, `ExecSerialRule`, `ExecSupersede`, `ScrErrata`, `CritW2Entry`.

Method: every claim below was re-measured at `60edb66` today, read-only (`git show`/`git ls-tree`/
`git diff`, the committed gate copies, and two gate runs whose receipts are in `receipts/`). No lane
file was written; no host call was made; no tool was installed.

---

## 0. Ground truth at `60edb66` (what the draft landing has to live with)

| fact | command | observed |
|---|---|---|
| gate blob byte-identical to the frozen original both drafts built against | `git show 60edb66:quality/check-session-material.py \| sha256sum` | `889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb` = the round-46 frozen original (`889f8f05…` in both seat reports) |
| marker layer absent | `git show 60edb66:quality/check-session-material.py \| grep -cE 'MARKER_RE\|SYNTHETIC-MATERIAL\|waiver_values_ok'` | `0` |
| serial rule absent | `git show 60edb66:quality/check-session-material.py \| grep -cE 'R5_SERIAL_PROSE\|SERIAL_PROSE_RE\|R6_SERIAL_EXACT'` | `0` |
| waiver registry absent | `git cat-file -e 60edb66:quality/session-material-waivers.txt` | missing |
| frozen gate at base | `python3 -I quality/check-session-material.py --repo . --rev 60edb66…` | exit 1; `SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 R3_MONITOR_IDENT=53 R4_HOME_LISTING=2`; `SESSION_MATERIAL: files=18371 findings=115 rev=60edb66…` (`receipts/frozen-gate-base.txt`) |
| round-46 w1 seats firing | `grep '^FINDING' receipts/frozen-gate-base.txt \| grep -c round-46` | 18 findings in 7 files (`CritW2Gate.md`, `CritW2Gate/report.md`, `CritW2Gate/repro.py`, `ExecSerialRule/gate.py`, `ExecSessionTriage/check-session-material.py`, `ExecSessionTriage/demo/run-demo.sh`, `ExecW2Monitors/adversarial.txt`) |
| R5 scan, draft gate | `python3 -I .ufo/waves/round-46/w1/ExecSerialRule/gate.py --repo . --rev 60edb66… --scope all --rules R5_SERIAL_PROSE` | exit 1; `R5_SERIAL_PROSE=24`; `files=18618 findings=24`; carriers = exactly the draft's 24 (3 knowledge + 21 wave copies), shape `9x3+Ax5+9x4` (`receipts/r5-base.txt`) |
| draft copy hashes | `git show 60edb66:…` | `ExecSessionTriage/check-session-material.py` = `3fc480a4…`; `ExecSerialRule/gate.py` = `a36224e2…` (= its report); both derived from the same `889f8f05…` original |
| SOURCES registry | `git show 60edb66:corpus/SOURCES.md` | 262 rows, top `S325` at line 274, `## Paths` at line 276; no S326+ row exists |
| R1 target sentence | `git show 60edb66:corpus/knowledge/hyprland-input-devices-r46.md \| sed -n 57p` | unchanged since `1001bda0` (diff empty); still cites `.ufo/waves/round-46/receipts/live-devices-host-l1.txt`; no erratum appended |
| R2 file | `git status --porcelain` | `?? .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` still untracked; 3,282,451 B; sha256 `6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238`; `receipts/sha256.txt` has no tsv digest |
| SKILL register row | `git show 60edb66:SKILL.md \| sed -n 770p` | `mado-session-material` row present — "no synthetic marker yet, so a red exit is expected until it lands" |
| errata anchors | `git show 60edb66:` `LOG.md:2499` (M44-1..7 line), `SKILL.md:301` (`clients=4` transcript), `corpus/QUALITY.md:413` (`check83.py`), `SCORECARD.md:2583` (contains `Mistakes M44-1..9 mined`) | all four hold at `60edb66`; `SCORECARD.md:2566` (E5's supersession line) now holds the Registration line — see §5 |
| monitor-rule entry | `git diff 4d22eeb 60edb66 -- corpus/knowledge/hyprland-monitor-rule-r45.md` | empty; six units at `:84b`/`:96`/`:98`/`:106`/`:107` (+ `:18` recheck clause) verbatim |
| round-47 C2 rows | `.ufo/waves/round-47/claims.md` | "SOURCES rows S326.. opened this round (registry tops at S325, 262 rows)" |

---

## 1. R1 — erratum for `hyprland-input-devices-r46.md:57`

**What closure must see (exact check):**

```
grep -n 'Erratum (round 47)\|live-devices-host-r46' corpus/knowledge/hyprland-input-devices-r46.md
```
Expected: an appended erratum block (after `:57`, no rewrite) that names the true producer:
`.ufo/waves/round-46/receipts/live-devices-host-r46.txt`, tool sha256 `3a80368997120503…`,
two configs — `~/.local/share/omarchy/default/hypr/input.conf` first, then
`~/.config/hypr/input.conf` — and the chain line
`~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf`.

```
sed -n '1,6p' .ufo/waves/round-46/receipts/live-devices-host-r46.txt
```
Expected header: `# live host run of tools/mado-devices.py (sha256 3a80368997120503…)` (the landed tool),
not `l1-draft/mado-devices.py (sha256 b229efd0…)` (the reference).

```
git diff 1001bda0 HEAD -- corpus/knowledge/hyprland-input-devices-r46.md
```
Expected: insertions only (0 deletions) — `:57` itself untouched, erratum appended.

The defect is live and unclaimed: the sentence still reads
"one `input` block in `~/.config/hypr/input.conf`" and cites the l1 receipt while the landed run at
`60edb66` passes the omarchy default first. No other lane file has an erratum for it.

## 2. R2 — untracked `ExecStofOracle/receipts/out.json.rows.tsv`

**What closure must see (exact check), either retention form:**

Form A (digest + remove):
```
sha256sum .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv
```
→ `6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238` (current bytes)
committed beside `out.json` (e.g., added to `receipts/sha256.txt`), then
```
git status --porcelain | grep out.json.rows.tsv
```
→ empty, and `git ls-tree -r --name-only HEAD -- .ufo/waves/round-46/w1/ExecStofOracle/receipts/ | grep rows.tsv` → empty.

Form B (retention stated): a committed note (seat report or round-46 lesson) stating the size
(3,282,451 B), this sha256, and that the bytes are retained outside git by design — mirroring the
round-45 D4 resolution (digest committed, bytes not).

Closure is NOT met today: the file is still untracked in the worktree, and `sha256.txt` holds no digest
of it (it lists the harness sources and the l1-draft tool only).

## 3. R3 — session-material marker + prose serial rule

**What closure must see (exact checks):**

1. Marker installed in the tracked gate:
```
git show HEAD:quality/check-session-material.py | grep -cE 'MARKER_RE|SYNTHETIC-MATERIAL|waiver_values_ok'
```
→ ≥1; and the gate's selftest keeps the marker cases (`python3 -I quality/check-session-material.py --selftest` → 34/34 or more).
2. Registry + sidecars present:
```
git cat-file -e HEAD:quality/session-material-waivers.txt && git show HEAD:quality/session-material-waivers.txt | wc -l
```
→ exists; rows = 47 (round-45, the draft's `demo/waivers-round45.txt`) **plus** rows/sidecars for the
round-46 synthetic set that currently fires: the 7 files in §0 (18 findings) — the draft's registry does
not cover them and as-drafted would leave them red.
3. Both directions shown on committed bytes at `60edb66`:
- waivable side: `python3 -I quality/check-session-material.py --repo . --rev 60edb66…` prints
  `SESSION_MATERIAL_WAIVED: findings=49 files=47` (round-45 block) and the final count equals 115 minus
  every waived finding (48 if all 18 round-46 are waived/redacted, 66 if the 18 are refused and stay —
  the closure doc must state which, per the triage of the round-46 18).
- un-waivable side: the demo's planted-real-dump run still exits 1 with
  `reason=value-not-synthetic:serial-not-synthetic` (draft `receipts/06-planted-real-dump.txt:83`),
  regenerated at `60edb66` (`demo/run-demo.sh`; `demo/verify.py` → `checks=40 failed=0`).
4. Serial rule installed, opt-in, behavior unchanged by default:
```
grep -cE 'R5_SERIAL_PROSE|R6_SERIAL_EXACT' quality/check-session-material.py
```
→ ≥1; `--selftest` reaches ≥45/45 (22 original + 23 serial cases, integrated with the marker cases);
the R5 scan at `60edb66` still finds exactly the 24 carriers and 0 elsewhere (re-measured: §0 — the
draft's FP=0 claim survives the round-46 additions); `--serial-from-host` is refused when `--rules`
excludes R6 and vice versa, and exits 2 headless.

**Critical integration note:** the marker copy (`3fc480a4…`, 34/34) and the serial copy (`a36224e2…`,
45/45) are independent extensions of the same frozen original `889f8f05…`; both touch `main`/`run`/
`RULES`. The L1 must merge them into one file — neither draft alone satisfies R3's two halves, and a
naive copy-over loses the other half's selftest. The verification is: one gate file containing both
marker and R5/R6 infrastructure, selftest ≥ 45/45 with marker cases intact, default-rules verdict
byte-identical to the frozen gate on the same rev.

The gate stays red after R3 by design: the 15 real findings (r2/r4 leaks in round-32/35/37/38/39/43
files, per `ExecSessionTriage/triage.tsv`) are not waivable and are not routed here; closure is the
mechanism, not a green flip.

## 4. R4 — S290-S297 supersession + ConnCalibration errata + the round-45 entry's six units

**Supersession (ExecSupersede draft) — what closure must see:**

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
```
→ 270 + (round-47 C2's new rows) = prev 262 + 8 supersession rows + C2's rows; ids contiguous and
immediately after the top.

**Staleness: the draft's ids `S326`-`S333` collide with round-47 C2's planned rows `S326..`**
(`claims.md`: "SOURCES rows S326.. opened this round"). Both land in this round's w1. Either the
supersession block is renumbered above C2's last row (preferred; the draft itself anticipated
renumbering in its risks), or C2 must start at S334. The freeze must name one owner; a split registry
would break id contiguity.

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```
→ exit 0; `W04` count 9 → 10 (the narrowed-scope row, still `S326`'s successor by content); `W01` x1
unchanged; `E` = 0. The draft's census variants were measured at 252 rows (m0-m6); they must be re-run
at 262/270. The append point moves from "after `S315` (line 264)" to "after `S325` (line 274), before
`## Paths` (line 276)". `Corpus/lessons/round-46.md` exists with `## Gate` (`:11`) and
`## Registry changes` (`:61`) sections — the landing target for the Gate lines and the registry-change
log is present.

**ConnCalibration errata (ScrErrata draft) — what closure must see:**

```
grep -n 'Errata — round-44 closure D7' SCORECARD.md
```
→ hit inside the Round 46 section, with E1-E6 headings in the calibration's finding order (F1, F2, F3,
F5, F6, F4), plus the coverage note naming `SCORECARD.md:2570`/`:2571` (C1/C2 claim rows carry pointers,
not after-values — verified at `60edb66`). The draft's `verify-quotes.py` re-runs to `QUOTES: 17/17
verified` against the same receipts.

**Six-unit entry errata (CritW2Entry draft) — what closure must see:**

```
grep -n 'Erratum' corpus/knowledge/hyprland-monitor-rule-r45.md
```
→ four appended blocks F1-F4 covering the six units; each fix as the draft specifies:
F1 cites `Hyprland-Monitor.cpp:275-287` + `:389` (not the `:264`/`:271` return path); F2 cites
`.ufo/waves/round-45/receipts/live-monitors-host-r45.txt` (tool `2f007417…`) in place of
`live-monitors-host-l1.txt` (`c6ac5fc2…`); F3 replaces the "not proof of which branch ran" hedge with
the Monitor.cpp:834-839 resolution; F4 either pins `a9902ea` with a receipt or drops the hash from
`recheck:`. `git diff 4d22eeb 60edb66 -- <entry>` = empty (nothing landed yet); the landing must stay
append-only against the same entry.

## 5. Draft staleness verdicts at `60edb66`

| draft | verdict | evidence |
|---|---|---|
| `ExecSessionTriage` | **STALE in coverage scope; valid in diff-base** | gate blob identical (`889f8f05…`), so W4a (`gate-copy`) still binds; but its waiver registry stops at round-45's 49 and its baseline is 97 at `4d22eeb` — at `60edb66` the gate fires 115 findings including 18 in round-46 w1 seats that the draft does not mark; demo receipts must regenerate at the base rev |
| `ExecSerialRule` | **STALE in numbers; valid in claims** | R5 FP=0 re-verified at `60edb66` (24 carriers, 0 elsewhere, files 17305 → 18618); must be merged onto the marker copy before install (§3) |
| `ExecSupersede` | **STALE — anchors and ids** | top S315/252 rows → S325/262; append-after-line-264 → 274; **id collision with round-47 C2's S326..**; census variants need re-run at 262 rows; pin re-fetches and locator receipts remain valid (history commits) |
| `ScrErrata` | **VALID in substance; locators need refresh** | E1's `LOG.md:2499`, E3's `SKILL.md:301`, E6's `QUALITY.md:413`, the coverage-note `:2570`/`:2571` and E5's `:2573` all hold at `60edb66`; E5's supersession citation `:2566` no longer holds that sentence (2566 is now the Registration line) — re-derive that one locator at landing |
| `CritW2Entry` | **VALID** | subject entry unchanged at `60edb66` (diff empty), six units verbatim, pins-refetch and tool-hash receipts committed; remains the authoritative source for R4's six-unit errata |

## 6. Cross-cut risks for the L1 freeze

1. **S326.. id collision** (R4 supersession vs C2) — must be resolved before either lands; the freeze
   should record the winning owner.
2. **Three-way gate merge** (frozen original + marker + serial) — one file, selftest ≥ 45/45 with both
   feature sets; do not land one copy over the other.
3. **Round-46 synthetic set** is unaccounted in R3's registry; expect 18 findings to persist unless the
   L1 marks/redacts them alongside the round-45 49.
4. R2's digest must hash the current bytes (`6573f76b…`); if the file is edited first, recompute.
5. The 15 real findings stay red after R3 (by design); the closure text must not claim a green flip.

## 7. Receipts

- `receipts/frozen-gate-base.txt` — frozen gate at `60edb66`: exit 1, `findings=115`, `files=18371`,
  rule counts, all FINDING lines.
- `receipts/r5-base.txt` — draft serial gate, R5-only at `60edb66`: exit 1, `R5_SERIAL_PROSE=24`,
  `files=18618 findings=24`, full carrier list.

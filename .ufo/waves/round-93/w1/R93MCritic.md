# R93MCritic — pre-freeze falsification of C1 (coverage: GKeyFile byte classes) and C2 (operability: selftest-strength gate)

Seat `R93MCritic` (critic, leaf — no dispatch). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`4c6f723f3dca3a26f9d14475d695fe797e2e972c`. Scratch `S=/fast/scratch/hyaku/mado-r93/R93MCritic` (deleted at exit).
**Every run below is DRAFT**: counter `--draft-tool` / `--draft-gate --draft-kills`, or the gate itself run directly on
scratch copies. No measurement was claimed, no counter `TARGET_*` word is asserted as lane evidence, and nothing was
written under `.ufo/waves/round-93/receipts/`. No install (pacman paused; none needed). No lane file was written
except this report; all forgeries/weakenings/kill-set probes live in `$S`.

## Snapshot (all shas as read at 00:46 local)

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-93/controls/portal-cases-r93.json` (364 cases) | `c6fa989ab3888546bed330ff8c9000fb465f6c1d41e910411c144b571e8990c8` |
| `.ufo/waves/round-93/build/mado-portals.c1.py` (C1 candidate, 00:26) | `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021` |
| `.ufo/waves/round-93/controls/portal-oracle-r93.py` | `d50d88bfc6a9964ac2f04a30315473daccf4308991aa3131cfe5e801f8b576f6` |
| `.ufo/waves/round-93/controls/fuzz-bytes-r93.py` | `94fdfe8f31c21ce42a8e197c585d9d7f9a09b32684c8a265dd4ef7bb1e5d1597` |
| `quality/counters/c1-r93-portal-bytes.py` | `fe72baee25c715cb9b10431bb830643d19a185488f5548cd610fbaf9529a8ee8` |
| `.ufo/waves/round-93/build/check-selftest-strength.c2.py` (gate, 00:32) | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` |
| `.ufo/waves/round-93/build/check-seat-reports-kills.c2.json` (32 kills, 00:32) | `00befb3efbe2f4a7c44b14776482e0cac0ab8e219db934af9c25b34f47c516f9` |
| `.ufo/waves/round-93/controls/selftest-panel-r93.json` (16 W + 6 N) | `a6d2cbe2826868191f3ee980c27fcc3288bbc151ed3ceeb79ca1f11891bc4c10` |
| `.ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json` (22) | `be676929cefa46481e1ea836d29cd65152af23002e9d9dad96cf39295b88770e` |
| `quality/counters/c2-r93-selftest-strength.py` | `30553ca0…` at 00:46, **superseded at 00:59 by `9edfa70e062b4d1a87beae5f6566c696dac3669a16cb2e1ec93823eee89d0170`** (current: docstring clause (iv) = frozen neutrals, requires `--expect-gate-sha256/--expect-kills-sha256`, `frozen_ok` in `met`) |
| `quality/check-seat-reports.py` (measured tool, = at `4c6f723f`) | `176fc066b49334921e4fd746de55db8106709c29dfe225430224c9d46ed1663a` |
| `.ufo/waves/round-93/controls/portal-mutants-r93.json` | **absent** at 00:46 |

The declaration (`claims-declaration-r93.md`) names candidate sha `89039e30…91d3`; the build candidate has moved
through `849df12c…` (00:23) and `e46a861e…` (00:26) since. The declaration's pin must be re-taken at the freeze
(C1-F2).

## Axis judgment

- **C1 (coverage, edge class)** — the surface does move *coverage*: the 364-case frozen file contains 135 classed
  byte/edge cases the base tool answers `a 11/36, b 5/16, n 14/26, ws 42/42, c 7/7, d 8/8` (+ `none` 229/229 = 316/364),
  and the candidate answers 364/364. It is *not* a quality move: the 229 round-90 routing cases were already 229/229.
  The counter mechanically rejects the three cheapest forgeries **only because of the fresh-bytes leg** (C1-F3); the
  byte subset it reports is not the declared one (C1-F1).
- **C2 (operability)** — the gate + extended (32) kill-set does move operability: on the current files it prints
  `OK` on the pristine tool and `WEAK` on all 23 per-check neutralisations, all 16 frozen weakenings, and `OK` on all
  6 strength-preserving neutrals (direct sweeps, §C2-E). The declaration's clause (iv) (fresh seed-chosen 20) is not
  the counter's clause (frozen neutrals), so the predicate sentence and the instrument disagree (C2-F1); the
  measurement paths and the C1 mutants are not in place (C2-F2, C1-F7).

---

## C1 findings

### C1-F1 — the counter's "byte-class subset" is 98 cases, not the declared 52; explicit class `ws` is ignored and class `n` is counted though undeclared
`quality/counters/c1-r93-portal-bytes.py:69-78` (`case_class`) returns the explicit class only for
`("a","b","c","d","n")`; an explicit `"ws"` falls through to the id regex, so the 13 `b93-ws-*` cases are classified
`b` by their id prefix. The same regex counts 7 ordinary round-90 cases (`a01-settings-*` … `a07-settings-*`) as `a`.
Line 378 then filters `case_class(c) in ("a","b","n")`, so the receipt counts `a 43 + b 29 + n 26 = 98`, while the
frozen file's explicit classes are `a 36, b 16, c 7, d 8, n 26, ws 42, none 229` (a+b = 52).

Reproducing run (DRAFT, snapshot `c6fa989a…`, tool `e46a861e…`):
`MADO_PORTAL_BYTES: DRAFT_TARGET_MET … cases=364 correct=364 bytes_cases=98 bytes_correct=98 … base_correct=316 base_bytes_correct=50`
— `bytes_cases=98` is not the declared count; the declaration's Count sentence says "classes a and b" (52), and its
surface names only (a) invalid UTF-8 and (b) `\v`; class `n` (NUL) is measured but not described. `base_bytes_correct
< bytes_cases` still holds (50 < 98; true set 16 < 52), so the verdict is not flipped, but the receipt's
`bytes_cases/bytes_correct/base_bytes_correct` are not the claim's numbers.

Smallest safe correction: in `case_class`, honour the explicit field for every value (`if "class" in c: return c["class"]`),
and make the filter the declared set. Either (a) declaration count stays a+b=52 → filter `("a","b")`, or (b) the
surface adds class (e) NUL → filter `("a","b","n")` and the Count/surface sentences name NUL and the count 78. Re-pin
the cases sha after the change.

### C1-F2 — the measured tool is not pinned to the frozen candidate; the declaration's sha is stale and the mutant anchors follow the build
The declaration pins `89039e30…`; the build candidate is `e46a861e…` (00:26) and moved twice during the wave. The
counter measures `<rev>:tools/mado-portals.py` and derives the fresh seed from *its* sha; nothing requires that file to
equal the build candidate. The frozen mutants are anchored to the ported bytes (§R92MExecD1 §57 lists 8 stale anchors:
M03 M27 X05 X04 M37 M31 X06), so a measured tool that is not the frozen candidate either SETUP_ERRORs on the anchors or,
if the L1 re-anchors them to a different tool, certifies a tool the claim did not describe; the fresh seed is also
shoppable (the tool's sha picks the 60 fresh cases). The only current C1 mutants file is absent (C1-F7).

Smallest safe correction: at the freeze, pin the measured `tools/mado-portals.py` to the build candidate's sha
(`tool_sha256` line) in the predicate/receipt, and/or pin `fresh_seed`; state that the mutants are anchored to those
exact bytes. No case, mutant, control or pin changes after the freeze (the declaration's kill rule already says this).

### C1-F3 — a fixture-digest label table passes the frozen set and is rejected only by the fresh-bytes leg (the load-bearing clause)
Cheapest forgery: a tool that embeds a table `sha256(desktop + fixture tree) -> labelled answer` for every frozen case
and otherwise falls through to the base tool. Built in `$S/forge-table.py` (300-case table) and
`$S/forge-table-364.py` (364-case table), scored through the round-93 counter's own `outcomes()`
(sandbox `bwrap`, fixtures as bytes):

```
MADO_PORTAL_BYTES: DRAFT_TARGET_MISSED pred=PRED-C1-r93-v1 … cases=364 correct=364 bytes_cases=98 bytes_correct=98
fresh=120/120 fresh_bytes=50/60 fresh_seed=1236939780 … tool_sha256=49ba3404…
```
(On the earlier 300-case snapshot the same forgery scored `correct=300`, `fresh_bytes=49/60`.) The **round-90** counter,
which has no byte-fresh leg, reports this forgery as
`MADO_PORTAL_ROUTING: DRAFT_TARGET_MET … cases=300 correct=300 blind=66/66 fresh=120/120 fresh_seed=2343958742 …`
— a false green. The round-93 predicate's fresh-bytes leg is therefore load-bearing: keep it, keep the generator pinned
(`--expect-fuzz-bytes-sha256`, present at line 276), and pin the tool/seed (C1-F2). Blunt byte-trigger variant
(`$S/forge-trigger.py`: hide the config when any file holds `\v` or invalid UTF-8): `correct=325/364`,
`fresh_bytes=51/60` — also rejected. The full 60 fresh-byte cases are answered correctly by the candidate
(`fresh_bytes=60/60`).

### C1-F4 — the shell-out forgery is dead in the sandbox (verified)
`$S/forge-shellout.py` execs `/usr/lib/xdg-desktop-portal` (the oracle binary) via `subprocess`; in the round-93
sandbox it scores `correct=0/364`, `fresh_bytes=0/60`, `crashed_not_killed` (a crash is not a kill). A direct probe
through the counter's own `sandbox()` argv shows why: `/usr/lib/xdg-desktop-portal`, `/usr/bin/dbus-run-session` and
`/usr/bin/dbus-daemon` are bound to `/dev/null` (mode 0666, size 0, `head b''`); `dbus-broker` is present but is not the
routing engine and the binary itself is unreadable. No correction needed; this control is already sound.

### C1-F5 — the round-90 counter/case materialiser cannot write the byte fixtures (verified, and fixed only in the round-93 counter)
`quality/counters/c1-r90-portal-routing.py:101,109` and `.ufo/waves/round-90/controls/portal-oracle-r90.py:108,121`
write fixtures with `open(..., "w", encoding="utf-8", newline="")`. Feeding the round-93 byte cases through the round-90
counter aborts on the first lone-surrogate fixture:
`UnicodeEncodeError: 'utf-8' codec can't encode character '\udce9' in position 6: surrogates not allowed`
(rc 1, no receipt line). The round-93 counter's `write_fixture()` uses `encode("utf-8", "surrogateescape")` and works
(DRAFT line above). Keep the receipt on the round-93 counter; do not measure C1 with the round-90 counter.

### C1-F6 — C1's frozen-mutants leg cannot be measured at 00:46 (`.ufo/waves/round-93/controls/portal-mutants-r93.json` absent)
The counter requires `killed == len(mutants)` on the frozen cases; my DRAFT lines above use an empty mutants file, so
`killed=0` of `mutants=0` only. The mutant seat's file was absent at the snapshot; the 8 stale round-90 anchors must be
re-anchored to the frozen candidate bytes and the byte-class mutants added (the port's `ASCII_SPACE`, `_next_char`,
NUL handling are distinct anchors). The L1 must not freeze C1 without this file and its `--expect-mutants-sha256`.

### C1-F7 — universal clauses and separability
The counter enumerates every conjunct: `correct == cases`, `fresh == a.fresh`, `fresh_bytes == a.fresh_bytes`,
`killed == len(mutants)`, `r12/host/do-nothing < n`, `base_bytes_correct < bytes_cases` (main, `met =` block), and it
prints the same sentence in the docstring and the receipt label `MADO_PORTAL_BYTES:` as the declaration. Separability:
the C1 counter reads only `.ufo/waves/round-90/controls` + `.ufo/waves/round-93/controls` (its own cases/oracle/
generator) and the tool at `<rev>`; it reads no C2 file (grep of `quality/`/`.ufo` references: lines 61-62 only). The C2
counter reads no C1 file. Each counter can be run at the other's commit.

---

## C2 findings

### C2-F1 — the declaration's clause (iv) is not the counter's (iv); the predicate sentence and the instrument disagree
Declaration `PRED-C2-r93-v1` (iv): "fresh: seed = first 8 hex digits of the gate's sha256 picks 20 (check, transform)
weakenings from the frozen grammar, all flagged". The delivered counter
(`quality/counters/c2-r93-selftest-strength.py:230-231,292`) measures (i) 23 per-check neutralisations, (iii) 16 frozen
`panel["weakenings"]`, and (iv) 6 frozen `panel["neutrals"]` that must **stay OK** (`zok == len(nonw)`), and prints
`neutral_ok=6/6` — there is no seed, no `fresh-*` ids and no 20-case fresh leg (the old
`controls/selftest-weakenings-r93.json`, seed `76a1d923`, is superseded by `selftest-panel-r93.json`, which has no seed
and whose gate is now `2d6f1219…`; the old seed no longer matches the gate). The receipt label is
`MADO_SELFTEST_STRENGTH:` in both declaration and counter, but the clauses behind it differ. (The 00:59 counter
version `9edfa70e…` states the panel clause explicitly in its docstring; the *declaration* still carries the
fresh-seeded sentence, so the reconciliation is owed by the declaration — or the fresh leg must be implemented and the
panel clause renamed.)

Smallest safe correction: either implement the declaration's fresh-seeded clause (seed = gate sha prefix; 20 picks from a
frozen grammar) or rewrite the declaration's (iv) to the panel's 6 strength-preserving neutrals, and make the counter
docstring, the predicate sentence and the receipt label state the same five clauses. The panel's neutrals are a *better*
false-positive control than the old fresh leg; if kept, say so and drop the "fresh 20" sentence, and re-pin the panel +
gate pair.

### C2-F2 — measurement paths: the counter reads `quality/selftest-kills/check-seat-reports.json`; the declared/committed kill-set lives in `build/`
`quality/counters/c2-r93-selftest-strength.py:40-43`:
`GATE = "quality/check-selftest-strength.py"`, `TOOL = "quality/check-seat-reports.py"`,
`KILLS = "quality/selftest-kills/check-seat-reports.json"`, `R92C2 = "quality/counters/c2-r92-gate-defects.py"`.
The seat item names `.ufo/waves/round-93/build/check-seat-reports-kills.c2.json`; the gate is still only in `build/`.
A measured run (no `--draft-kills`) returns `MADO_SELFTEST_STRENGTH: SETUP_ERROR pred=PRED-C2-r93-v1 gate/kill-set/tool
absent at <rev>` unless the L1 lands the kill-set at the counter's path (or changes `KILLS`). Likewise the gate must be
landed byte-identical at `quality/check-selftest-strength.py`, and the current counter requires both
`--expect-gate-sha256` and `--expect-kills-sha256` (with `frozen_ok` in `met`, line 302), so the freeze must pass the
two build files' shas as the frozen pins.

### C2-F3 — the gate-mutants file: the frozen 22-mutant file is the one that applies; the earlier 19-mutant file has a stale find
Against the current gate (`2d6f1219…`), `.ufo/waves/round-93/controls/selftest-gate-mutants-r93-frozen.json` (22
mutants, sha `be676929…`) has all `find`s exactly once; the earlier
`selftest-gate-mutants-r93.json` (19 mutants) has `G02-must-fail-ignored: find occurs 0 times` → a measured run with it
would `SETUP_ERROR`. The declaration/seat item must name the frozen file (and its sha) as the measured mutant set.

### C2-F4 — (v) is only partly evidenced: the composed draft run did not finish in 25 min (12/22 mutants killed, no receipt line); the counter is rc-aware (the earlier rc-blindness is fixed)
The current `verdict` compares `"WEAK:1"`/`"OK:0"` (lines 253-254), i.e. exit code + word, fixing the earlier
word-only comparison under which a `G19-rc-always-zero` mutant survived (`verdict(["… WEAK …"], 0) == "WEAK"` on the
old counter, sha `a28a7c71…`). The composed draft run (`--panel a6d2cbe2… --mutants be676929… --draft-gate 2d6f1219…
--draft-kills 00befb3e…`, on the counter version current at 00:46, sha `30553ca0…`; the 00:59 version `9edfa70e…`
changed the probe set, so the 12/22 below is evidence for the construction, not for the current file) was killed by my
1500 s deadline with no `MADO_SELFTEST_STRENGTH:` line; its log (`$S/draft-c2-final.log`, 69 lines) ends after 12 of
the 22 mutants:

```
probe N:all present -> OK rc0 WEAK:1            (23 N: neutralisations, all WEAK:1; 16 W: and 6 Z: follow)
probe s10-bad-kill-entry SETUP_ERROR:2          (setup panel: 12 probes)
mutant G01-rc-ignored killed diff=1
mutant G02-must-fail-ignored killed diff=6
…
mutant G12-result-line-unchecked killed diff=1
```

All 12 mutants reached were killed (`G01`–`G12`), so (v) is plausible, but the run is 12/22 at 1500 s and **G13–G22
are unverified at this snapshot**. The L1 must run it to completion (the receipt needs `killed == 22`).

### C2-F8 — the counter's per-mutant full-vector comparison makes a measured run exceed the wave's 25-minute window
`quality/counters/c2-r93-selftest-strength.py:260-268` runs `vector(gate_t.replace(...))` over *all* probe jobs for
every mutant and only then diffs (`diff = [...]`). Each gate run re-runs 1 + 32 kill selftests plus the setup-panel
selftests; with 23+16+6+12 probes and 22 mutants my draft spent >1500 s and reached 12 mutants. Repro: the timed-out
run above (`timeout 1500`, `--workers 8`). Smallest safe correction: stop at the first differing probe (run the probe
list in order, break on the first changed verdict; a mutant is killed by *one* change), or drop the setup probes that
duplicate each other from the per-mutant vector. This does not change the predicate, only its runtime.

### C2-F5 — (i)-(iii) and the neutral control hold on the current gate + 32-kill set (DRAFT, direct gate runs)
Commands with `python3 -I <gate> --tool <scratch copy> --kills build/check-seat-reports-kills.c2.json --scratch-root $S/... --allow-sha-drift`
(the counter passes `--allow-sha-drift` for non-pristine variants):

| probe | gate output | rc |
|---|---|---|
| pristine tool | `SELFTEST_STRENGTH: OK tool=quality/check-seat-reports.py kills=32 held=32 survived=0 wrong_check=0` | 0 |
| each of the tool's 23 selftest checks neutralised (result forced to pass) | 23/23 `WEAK` | 1 each |
| 16 frozen panel weakenings (`h01…h10`, `e01…e06`) | 16/16 `WEAK` | 1 each |
| 6 frozen panel neutrals (`n01…n06`, strength-preserving) | 6/6 `OK` | 0 each |

With the earlier 20-kill set the same sweeps gave 20/23, 4/10 and 11/20 (the three uncovered checks were
`all present -> OK rc0`, `unsafe -> SR03 rc1`, `untrailed -> SR04 rc1`; the per-check `want-in`/ids weakenings
`h02/h03/h04/h06/h08/h10` were unflagged). The 32-kill extension (`x-present-none`, `x-unsafe-or`, `x-untrailed-found`,
`x-wt-symlink-msg`, `x-wt-symlink-upper`, `x-space-quoting`, `x-summary-waves`, `x-mode-fixed`, `x-dup-sr01`,
`x-extra-sr04`, `x-rc-always-1`, `x-nonascii-tail`) closes them; the current files meet (i)-(iii)+neutrals. This is a
real operability move, not a do-nothing instrument.

### C2-F6 — crash-everything and grep-gate forgeries are defeated; the total-failure variant is the one the panel must catch
- A kill-set whose mutants crash the tool: the gate counts a crash as `SURVIVED` (`rc != 0, no FAIL lines` → not held),
  so the pristine tool itself goes `WEAK` and clause (i) fails. Repro: kill `unsafe()` body → `raise RuntimeError`,
  gate → `SURVIVED crash` + `SELFTEST_STRENGTH: WEAK … survived=1`, rc 1.
- The subtler "every check FAILs but nothing crashes" mutant (replace `run()`'s verdict line with `return 2`) is
  **held** by the gate (`OK held=1`) because the named label is among the failures; the defense is the weakening/neutral
  panel, which is why (iii)+(iv) must stay in the predicate.
- A grep-the-source gate ("does each `must_fail` label appear as `case(\"…\"` in the tool?") and an always-OK gate give
  `SELFTEST_STRENGTH: OK` on every one of the 23 neutralisations → `neutralised_flagged=0/23`, rejected by (ii).

### C2-F7 — universal clause enumeration
The counter enumerates checks from the measured tool, not the kill-set: `re.findall(r'case\("([^"]+)"', tool_text)`
→ 23 labels (23 unique), `nflag == len(neut)`, `hflag == len(hand)`, `zok == len(nonw)`, `killed == len(mutants)`.
The gate's own `--selftest` is 8/8 (rc 0). The failure mode to avoid at the freeze is enumerating from the kill-set
(which would shrink the universal set if a check were removed); the counter does not.

---

## Smallest safe corrections (rolled up)

1. **C1**: fix `case_class` to honour every explicit class (including `ws`) and make `bytes_idx` the declared set; then
   re-pin the cases sha and state the count in the declaration/receipt consistently (52 for a+b, or 78 if NUL is added).
2. **C1**: pin the measured `tools/mado-portals.py` sha to the frozen candidate and/or pin `fresh_seed`; freeze the
   mutants against those bytes; do not freeze without `portal-mutants-r93.json`.
3. **C1**: keep the fresh-bytes leg and the generator pin; it is the only defense against the table forgery (C1-F3).
4. **C2**: reconcile the declaration's (iv) with the counter/panel (fresh-seeded 20 vs 6 neutrals); land the gate at
   `quality/check-selftest-strength.py` and the kill-set at `quality/selftest-kills/check-seat-reports.json` (or change
   `KILLS`); pass the frozen 22-mutant file and pin its sha; run the counter to completion and evidence `killed == 22`.
5. **C2**: keep the 32-kill set (the 20-kill set fails 20/23, 4/10, 11/20) and the 6 neutrals.

## Commands and exit codes (selected; all DRAFT)

| command | rc | line |
|---|---|---|
| `c1-r93-portal-bytes.py … --draft-tool build/mado-portals.c1.py` (364-case snapshot) | 3 | `MADO_PORTAL_BYTES: DRAFT_TARGET_MET … cases=364 correct=364 bytes_cases=98 … fresh_bytes=60/60 … base_bytes_correct=50 tool_sha256=e46a861e…` |
| same, `--draft-tool $S/forge-table-364.py` | 3 | `… DRAFT_TARGET_MISSED … correct=364 … fresh_bytes=50/60 … tool_sha256=49ba3404…` |
| same, `--draft-tool $S/forge-trigger.py` | 3 | `… DRAFT_TARGET_MISSED … correct=325 … fresh_bytes=51/60 …` |
| same, `--draft-tool $S/forge-shellout.py` | 3 | `… DRAFT_TARGET_MISSED … correct=0 … fresh_bytes=0/60 …` |
| `c1-r90-portal-routing.py … --draft-tool $S/forge-table.py` (300-case snapshot) | 3 | `MADO_PORTAL_ROUTING: DRAFT_TARGET_MET … correct=300 … fresh=120/120 …` (false green) |
| `c1-r90-portal-routing.py` with the byte cases (strict materialise) | 1 | `UnicodeEncodeError … '\udce9' … surrogates not allowed` |
| sandbox mask probe (`c1h.sandbox` argv) | 0 | `/usr/lib/xdg-desktop-portal mode=20666 size 0 head b''`; dbus-run-session/daemon same |
| gate pristine + 32 kills | 0 | `SELFTEST_STRENGTH: OK … kills=32 held=32 survived=0 wrong_check=0` |
| 23 neutralisations / 16 panel weakenings / 6 neutrals | 1 / 1 / 0 | 23/23 WEAK, 16/16 WEAK, 6/6 OK |
| crash kill (`unsafe` raises) | 1 | `SURVIVED crash` … `WEAK … survived=1` |
| total-failure kill (`run()` returns 2) | 0 | `OK … held=1` (the panel/weakenings are the defense) |
| composed C2 counter draft (`--panel a6d2cbe2… --mutants be676929… --draft-gate 2d6f1219… --draft-kills 00befb3e…`) | TIMEOUT (1500 s) | no receipt line; 57 probes (23 N + 16 W + 6 Z + 12 S), 12/22 mutants killed (`G01`–`G12`, each `killed diff=N`); `G13`–`G22` unreached |

## Scratch

`/fast/scratch/hyaku/mado-r93/R93MCritic` (case snapshots, forgery tools, sweeps, sandbox work dirs) is deleted at exit;
the deleted paths are reported in the yield. No lane file other than this report was written; no receipt; no
git/jj mutation; no install.

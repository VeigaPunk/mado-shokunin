# controls-c2 — negative controls for `PRED-C2-r51`

Seat: `ExecControlsC2`, mado round 51 (hyaku run 10), wave w1 — BUILD + first-attack.
Frozen wording: `.ufo/waves/round-51/claims.md` § C2 (clauses a–d, plus the base clause).
Lane base: `6ca8c559a4a3d6d361101592116eea2bc7452437`.

Purpose: make every do-nothing control in the claims file runnable, so the L1 can freeze a fixture
set whose expected outputs are measured rather than asserted, and so w2 has something to attack.

Nothing in this directory is a lane deliverable: no tracked file was written. The fixture trees are
commits inside a throwaway `git clone --shared` under the seat scratch dir; they are re-derivable at
any time by re-running the driver.

## Controls

| control | tree | must MISS via | construction |
|---|---|---|---|
| `ctl-a` | base + scaffold + entry | (c) | the round-50 entry bytes (`corpus/knowledge/hyprland-bind-key-match-r50.md` at base) written at the C2 entry path |
| `ctl-a2` | base + scaffold + entry | (c) only | same copied body; the `source:`/`held` block replaced with the two scaffold rows and three valid `held:` citations |
| `ctl-b` | base + scaffold + entry | (c) | the round-49 candidate bytes (`.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md` at base) at the C2 path |
| `ctl-b2` | base + scaffold + entry | (c) only | same copied body with the rewritten source/held block, as `ctl-a2` |
| `ctl-c` | base + scaffold + authored entry | (d) only | authored fixture entry: (a)(b)(c) pass; three `held:` citations whose pinned tokens (`m_mDispatchers`, `handleKeybind`, `submap`) do not occur on the cited base lines |
| `ctl-d` | base + scaffold (no pins) + authored entry | (b) only | same authored entry shape, valid held citations, pins named in the manifest and in `SOURCES.md` but absent from `.ufo/waves/round-51/fetch/` |
| `ctl-e` | bare base | (a) | no entry at all — the predicate's own base clause |

`scaffold` = two registry rows `S364`/`S365` (status `mined`, opened `2026-10-27`, synthetic pin
locators `ctl-dispatch-a.txt:3` / `ctl-dispatch-b.txt:2` with ≤25-word quotes), two synthetic pin
files under `.ufo/waves/round-51/fetch/`, one `corpus/README.md` index row, and (for the authored
entries) a `pin` manifest table. The pin files say `CONTROL FIXTURE` on their first line: they are
not upstream bytes and must never be mistaken for evidence.

`ctl-a`/`ctl-b` are the controls named in `claims.md`. Measured, they fail **more than one** clause:
the copied bytes also carry the previous round's `source:` block (rows S352–S363 are outside the
S364–S379 window, so (b) fails) and its `held (cited, not re-registered)` lines are untargeted
citations (so (d) fails). They are byte-reuse controls, not clause-(c)-isolating controls. `ctl-a2`/
`ctl-b2` add the isolation by rewriting only the metadata block, leaving the copied body intact:
(a)(b)(d) then pass and clause (c) alone rejects the reuse. Both readings are receipted.

## Files

| path | role |
|---|---|
| `fixtures/controls.json` | control recipes (scaffold on/off, pins on/off, copied entry source, reblock, overlay dir) |
| `fixtures/scaffold/append/{SOURCES.md,README.md}.frag` | registry rows and index row, inserted after the last matching table row |
| `fixtures/scaffold/append/entry-reblock*.frag` | replacement `source:`/`held:` block and pin-manifest table for `ctl-a2`/`ctl-b2` |
| `fixtures/scaffold/files/.ufo/waves/round-51/fetch/ctl-dispatch-{a,b}.txt` | synthetic pins (line 3 / line 2 carry the quoted sentences) |
| `fixtures/ctl-c/files/...`, `fixtures/ctl-d/files/...` | the authored fixture entry (ctl-c: absent tokens; ctl-d: valid tokens) |
| `probe-clauses.py` | spec-faithful clause probe (independent instrument, not the counter) |
| `drive-controls-c2.py` | builds every fixture commit and scores it with the counter (if present) and the probe |
| `expected.json` | required clause vector, miss clause, verdict and exit codes per control |
| `receipts/` | one receipt per control, plus `summary.txt` and `build.txt` |

## Run

```sh
python3 -I <seat>/controls-c2/drive-controls-c2.py \
  --work /fast/scratch/hyaku/mado-r51/ExecControlsC2/run \
  --out  <seat>/controls-c2/receipts \
  --counter /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r51-dispatch-entry.py
```

`--counter` is optional: without it the driver records `counter ABSENT` and only the probe runs
(this was the state for the first passes; the draft appeared in `w1/ExecCounterC2/` at 07:03). The
driver exits 0 only when every control matches `expected.json`, including the counter's own final
line and exit code. It writes nothing outside `--work`, `--out` and the sandbox clone, and deletes
`--work` unless `--keep` is passed. `TMPDIR` is set to `--work` for the counter.

## Measured (2026-10-27, counter draft `w1/ExecCounterC2/c2-r51-dispatch-entry.py`)

Counter bytes for the receipts in `receipts/`: `ebe39e1183375e0fb102124057eafecc9a21bdfc330c04ceb03759093d10e6dd`
(25258 B), also printed as `counter_sha256=` in `build.txt`/`summary.txt`. The draft was edited
repeatedly while this seat ran — six observed states, one of which (22502 B) crashed at clause (b) on
`ctl-a2`/`ctl-b2` with `TypeError: 'dict' object is not callable`. The full drift log is
`receipts/counter-drift.txt`. **Re-run at freeze and pin the counter hash with the receipt.**

| control | probe vector a,b,c,d | counter a,b,c,d | miss clause | counter max overlap | verdict / rc |
|---|---|---|---|---|---|
| `ctl-a` | 1,0,0,0 | 1,0,0,0 | c (also b,d) | 99.3% vs `hyprland-bind-key-match-r50.md` | TARGET_MISSED / 1 |
| `ctl-a2` | 1,1,0,1 | 1,1,0,1 | c only | 99.3% (same file) | TARGET_MISSED / 1 |
| `ctl-b` | 1,0,0,0 | 1,0,0,0 | c (also b,d) | 99.2% vs `round-49/candidate/hyprland-bind-key-match-r49.md` | TARGET_MISSED / 1 |
| `ctl-b2` | 1,1,0,1 | 1,1,0,1 | c only | 99.2% (same file) | TARGET_MISSED / 1 |
| `ctl-c` | 1,1,1,0 | 1,1,1,0 | d only | 0.0% | TARGET_MISSED / 1 |
| `ctl-d` | 1,0,1,1 | 1,0,1,1 | b only | 0.0% | TARGET_MISSED / 1 |
| `ctl-e` | 0,0,1,0 | 0,0,0,0 | a | 0.0% | TARGET_MISSED / 1 |

Counter diagnostics recorded in `receipts/<control>.txt`, e.g. `ctl-d` → `b ok=0 … miss=S364=
pin_file_absent:ctl-dispatch-a.txt,S365=pin_file_absent:ctl-dispatch-b.txt`; `ctl-c` → `d ok=0 …
miss=token_missing:hyprland-input-devices-r46.md:71:m_mDispatchers,…`.

## Instrument notes (where the frozen sentence and the counter differ)

The probe reads the frozen sentence literally; the counter documents its own citation grammar. The
two agree on every control above, but the differences are worth knowing at freeze:

1. **Quote source.** The frozen sentence says the pin's cited line contains "the row's quote"; the
   counter takes the first verifiable quoted span from the *entry's* `source:` line. The scaffolded
   rows carry the same sentence in both places, so both readings pass and `ctl-d` still isolates (b)
   through pin absence rather than through a quote mismatch.
2. **`held:` token syntax.** The counter requires `keys=` (or, absent `keys=`, backticked identifiers
   on the same line). The probe accepts `keys=`/`tokens=`. Fixtures use `keys=`.
3. **Candidate baseline revision.** The frozen sentence says every `.ufo/waves/round-*/candidate/`
   file *at base*; the counter lists candidates at `<rev>`. Identical for these fixtures (no
   candidate file is added), but a fixture that adds a candidate file at `<rev>` would self-match.
4. **Body-length floor.** The counter adds `MIN_BODY_SHINGLES=300` (clause (c) fails below it), a
   guard the frozen sentence does not state. The authored fixture entries were padded to 359 body
   shingles so this guard does not decide the control; a genuine short entry would MISS on (c) for
   length alone.
5. **Probe tokenisation** is `[a-z0-9_]+`, the counter's is `[a-z0-9]{2,}`; the probe also scores the
   whole entry while the counter strips `source|ground|held|verified-at|recheck|lane|pin` lines and
   tables first. That is why the probe's `max_overlap` is exactly 100% on `ctl-a`/`ctl-b` while the
   counter's body-only overlap is 99.3%/99.2%. Both are far above the 30% threshold.

## Scratch discipline

All trees live under `/fast/scratch/hyaku/mado-r51/ExecControlsC2/` (`--work`), deleted after the
final run; receipts are copied into this directory first. No counter, probe or driver hardcodes
`/tmp`; the probe writes nothing, the counter takes `TMPDIR`/`--work`. No tracked lane file, no
config plane, no compositor socket and no mutating git outside the sandbox clone was touched.

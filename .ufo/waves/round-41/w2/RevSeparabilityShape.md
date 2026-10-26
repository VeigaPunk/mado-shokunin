# RevSeparabilityShape — Wave 2 Report (mado round 41)

- **Seat:** `RevSeparabilityShape` (UFO-FSD reviewer, leaf)
- **Lane repo:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Base / v1 Freeze / v2 Freeze / Data:** `ab2bfaab661c846d1de9d58c01651cd156a13949` $\to$ `60c3914154333180450d5da27ba222d5763cc56a` $\to$ `294c667901a8c7b7165ba849d03cba9a24c14fa4` $\to$ `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- **Full findings & reproductions:** `.ufo/waves/round-41/w2/RevSeparabilityShape/findings.md`
- **Quote verification:** `.ufo/waves/round-41/w2/RevSeparabilityShape/verify-quotes.py` $\to$ `.ufo/waves/round-41/w2/RevSeparabilityShape/verify-quotes.txt` (`QUOTE_VERIFY: total=20 ok=20/20`, all $\le 25$ words).

---

## 1. Headline Verdict per Attacked Surface

1. **Distinct axes & causal separability (`AXES.md:30-34`, `.ufo/waves/round-41/registration-v2.md:36-46`):** **NO DEFECT FOUND.**
   - C1 (`operability`, capability acquisition: `tools/mado-globals.py`) and C2 (`coverage`, sourced: `corpus/knowledge/hyprland-focus-grab-r41.md`) sit on distinct axes.
   - Static grep of `quality/counters/c1-r41-globals-v2.py` and `c2-r41-focus-entry-v2.py` (plus v1 counters) confirms zero cross-file reads: C1 reads only `tools/mado-globals.py` (and runs it in `bwrap --unshare-all` with no repo access); C2 reads only `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/SOURCES.md`, `corpus/lessons/round-41.md`, `corpus/README.md`, and `.ufo/waves/round-41/fetch/*`, parsing `xdph-journal.txt` with its own `journal_counts()` parser (`c2-r41-focus-entry-v2.py:209-235`).
   - **Scratch-clone proof 1 (C1 tool deleted):** Cloned `07f2641` to `/tmp/revsep-no-c1-*`, verified toplevel, `git rm tools/mado-globals.py` $\to$ commit `b0f887f4379da64e8fc31009ac51b891d405117a`. Ran `c2-r41-focus-entry-v2.py` (and v1): **`PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET`**, exit `0` (while `c1-r41-globals-v2.py` scored `0/39 tool=absent TARGET_MISSED`, exit `1`).
   - **Scratch-clone proof 2 (C2 entry & corpus edits deleted/reverted to base):** Cloned `07f2641` to `/tmp/revsep-no-c2-*`, verified toplevel, removed `hyprland-focus-grab-r41.md`, `round-41.md`, `fetch/xdph-installed-version.txt` and reverted `SOURCES.md` + `README.md` to `ab2bfaa` $\to$ commit `a15976e2ec9d8336467f428126e8676eb229b297`. Ran `c1-r41-globals-v2.py --nonce be51c3bc188d6b05`: **`PRED-C1-r41-v2: fixtures=39/39 tool=present verdict=TARGET_MET`**, exit `0`, `clauses=a:1 b:1 b2:1 b3:1 g:1` (while `c2-r41-focus-entry-v2.py` scored `admitted=0/1 TARGET_MISSED`, exit `1`). Both `/tmp` clones were removed.

2. **Lowest-axis rule (`AXES.md:33-34,67-73`, `.ufo/waves/round-41/registration.md:7-9`):** **NO DEFECT FOUND.**
   - Re-ran `python3 -I quality/check-axis-scores.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ab2bfaab661c846d1de9d58c01651cd156a13949` $\to$ `navigation 58/58`, `calibration 55/55`, `operability 12/12`, `MADO_AXIS: checked=3 mismatched=0`, exit `0`. All three non-retired scored sub-axes tie at `1.0` (10/10), so every owned axis is tied for lowest; working `operability` and `coverage` satisfies the rule without needing the stagnation nudge.

3. **Target statements & universal clauses (`PROTOCOL.md` / prompt §9, `registration-v2.md:40,45`):** **NO DEFECT FOUND in target statements.**
   - Targets are finite ratios (`fixtures=39/39 tool=present verdict=TARGET_MET`, exit `0`, and `admitted=1/1 verdict=TARGET_MET`, exit `0`) with explicit non-narrowing kill rules and no universal clauses.
   - *Wording note on `registration-v2.md:9-10`:* Line 10 claims `"nothing loosened except the b2 sample's name-substring exclusion, replaced by an exact one"`, omitting that `c1-r41-globals-v2.py:186-187` also widened `STDLIB_ALLOW` by `{collections, itertools, select, time}` (needed for the bounded incremental read fix).

4. **Do-nothing controls (`receipts/ctl-c1-v2.txt`, `ctl-c2-v2.txt`):** **NO DO-NOTHING REACHES TARGET, but 1 registration/control-accounting defect found (F2).**
   - Base (`tool=absent` $\to$ `0/39`; `entry=absent` $\to$ `0/1`) and all three C1 do-nothing controls (`D1-empty`, `D2-echo-no-sessions`, `D3-hardcoded-report` $\to$ `0/39 TARGET_MISSED`) and C2 empty/forgery controls (`N01`, `N02`, `F1..F6`, `Z1` $\to$ `0/1 TARGET_MISSED`) fail to reach `TARGET_MET`.
   - **Defect F2 (MEDIUM — Registration v2 vs `ctl-c1-v2.txt`):** `registration-v2.md:50` states that `receipts/ctl-c1-v2.txt` scores `"ten v2 cheats (K01-K10...) and the 42 ExecC1ExtraMutants mutants each score below MET"`. In reality, `ctl-c1-v2.txt:1` prints `CTL_C1V2: skipped-patterns-absent=4 W1-N14-empty-file-expect-ok W1-N24-ver-5-digits-max W1-N35-read-only-max-bytes W1-N42-live-no-timeout` and scores **95** controls (`38` of the 42 `W1-N*` mutants), because 4 v1 replacement strings no longer matched the v2 reference tool. Two of those 4 (`N24` and `N42`) were re-expressed as `K11-ver-5-digits` and `K12-live-no-timeout` in `receipts/ctl-c1-v2-extra.txt` (`controls=3 correct=3/3`, which `registration-v2.md` never cites), while **`W1-N14-empty-file-expect-ok` and `W1-N35-read-only-max-bytes` were never re-adapted or scored under v2**.

5. **Sourced-claim requirement (`PROTOCOL.md:143-144`, `CORPUS.md`):** **NO DEFECT FOUND.**
   - C2 (`corpus/knowledge/hyprland-focus-grab-r41.md`) cites 7 new `SOURCES.md` rows opened `2026-10-25` (`S283–S289`, all `mined`, `used-by` naming the entry) plus 1 held row (`S037`, `used-by` extended), each backed by a `GATE` line in `corpus/lessons/round-41.md` and a committed receipt in `.ufo/waves/round-41/fetch/`. `sources-census.sh validate` exits `0`.

6. **Contradictions between registration / lesson and lane files at `07f2641`:** **3 concrete defects found (F1, F3, F4) + 1 expected pre-closure state (F5).**
   - **F1 (HIGH — DATA defect in `corpus/lessons/round-41.md:163-164`):** The committed lesson skeleton states `"PRED-C1-r41-v1 at the data commit: fixtures=24/24 verdict=TARGET_MET"`, whereas `.ufo/waves/round-41/receipts/c1-v1-after-data.txt:34` (and our re-run) shows `PRED-C1-r41-v1: fixtures=6/24 tool=present verdict=TARGET_MISSED` (`clauses=a:1 b:1 b2:1 g:0`, exit `1`) because the v2 tool imports `select`/`time` and prints the v2 `ignored=` field. **Fix in `corpus/lessons/round-41.md` before landing.**
   - **F3 (MEDIUM — DATA defects in `corpus/lessons/round-41.md:38,45,53`):**
     1. Line 38 says `"the seven pre-wave receipts are committed at the freeze (git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/)"`, but running that command prints **9** files (7 is the count of new cited IDs `S283–S289`, not files in `fetch/`, and line 107 of the same lesson says `"lists nine files"`).
     2. Line 45 says `"re-grounded this round as C2 with lane ids S283–S290"` and line 53 lists `"input-capture-v1.xml S290"` under `"the new rows S283-S289 continue"`, whereas `S290` was not added to `corpus/SOURCES.md` (as line 38 itself notes). **Fix in `corpus/lessons/round-41.md` before landing.**
   - **F4 (MEDIUM — Wave 1 report count):** `registration-v2.md:13-14` states `w1` had 34 seats, and `w1-results.json` has `output: null` for all 34 (`"read the seat report file in the wave dir"`), but only **33** `.md` reports exist under `.ufo/waves/round-41/w1/` — seat `ConnSiblingOverlap` has no report file or directory on disk. **Disclose in the round report.**
   - **F5 (LOW — Pre-closure state at `07f2641`):** `check-axis-scores.py --rev 07f2641` exits `1` (`navigation published=58/58 derived=59/59 verdict=STALE`) because `SCORECARD.md` (round-41 section, capability row, and updated axis line), `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, and `quality/receipts/axis-<tip>.txt` are landed by the L1 in the post-wave records commit.

---

## 2. Residual Risk & Verification Gaps

- Once the L1 integrates the post-wave records commit (`SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, and the updated `corpus/lessons/round-41.md`), `check-axis-scores.py` and both v2 counters (`c1-r41-globals-v2.py` and `c2-r41-focus-entry-v2.py`) must be re-run at the final lane tip and committed under `receipts/` / `quality/receipts/`.
- Tooling: no tools installed; no tracked files or git/jj state mutated.

Report: `.ufo/waves/round-41/w2/RevSeparabilityShape.md`

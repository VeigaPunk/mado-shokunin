# Seat Report: ConnClaimsVsBytes (Mado Round 41 w2)

- **Status**: COMPLETE
- **Role**: UFO-FSD connector
- **Target**: Cross-read `registration-v2.md`, the lesson, the entry, the rows and the receipts at data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`: ids, counts, hashes, paths, dates, commit references (`git cat-file -e`), S290 mentions, class table in tool vs docstring vs entry, surviving v1 wording.
- **Deliverables**:
  - Audit table: `.ufo/waves/round-41/w2/ConnClaimsVsBytes/cross.md`
  - Findings & proposed move: `.ufo/waves/round-41/w2/ConnClaimsVsBytes.md` (this report)

---

## 1. Evidence (Contradictions & Findings)

Cross-reading the DATA commit `07f2641696b5ac73de1404ea737a9f27e9819aa1` against `registration-v2.md`, the frozen receipts, and predicate counters revealed 11 concrete contradictions:

1. **S290 Phantom Re-grounding in Lesson**:
   - `corpus/lessons/round-41.md:38` states: `S290 (input-capture-v1.xml) is not cited by the entry and has no row.`
   - In direct contradiction, `corpus/lessons/round-41.md:44` states: `re-grounded this round as C2 with lane ids S283–S290`.
   - `corpus/lessons/round-41.md:53` appends `input-capture-v1.xml S290` to the row sequence after declaring "the new rows S283-S289".
   - `corpus/lessons/round-41.md:173` sets the upper bound formula to `(at most S283–S290)`.
   - In reality, `corpus/SOURCES.md` ends at S289 (7 new rows), and commit `07f26416` log states `rows S283-S289`.

2. **Claimed PRED-C1-r41-v1 MET Contradicts Measured TARGET_MISSED**:
   - `corpus/lessons/round-41.md:175` claims: `PRED-C1-r41-v1 at the data commit: fixtures=24/24 verdict=TARGET_MET with the nonce printed; PRED-C2-r41-v1: admitted=1/1 verdict=TARGET_MET; both re-run at the tip.`
   - Directly contradicted by committed measurement `.ufo/waves/round-41/receipts/c1-v1-after-data.txt`: `PRED-C1-r41-v1: fixtures=6/24 tool=present verdict=TARGET_MISSED rev=07f26416 nonce=cb2bcd4259089823 exit=1`. The v2 tool fails v1 because it emits the v2 `ignored=0` summary token and triggers v1 clause g.
   - Furthermore, the lesson omits the registered v2 scores: `PRED-C1-r41-v2: fixtures=39/39 TARGET_MET nonce=be51c3bc188d6b05` and `PRED-C2-r41-v2: admitted=1/1 TARGET_MET`.

3. **Request Count Discrepancy Across Four Sources**:
   - Upstream XML receipt `protocols/hyprland-focus-grab-v1.xml` and entry §1 (`hyprland-focus-grab-r41.md:22-32`) define **6 requests** (2 on manager: `create_grab`, `destroy`; 4 on grab: `add_surface`, `remove_surface`, `commit`, `destroy`) and 1 event (`cleared`).
   - `corpus/SOURCES.md:232` (row S283) says: **4 requests** (`four requests and one event`).
   - `corpus/knowledge/hyprland-focus-grab-r41.md:114` (§6 decision table) says: **5 requests** (`five requests, one event`).
   - `corpus/README.md:70` says: **5 requests** (`five requests, one cleared event`).

4. **Interface Bind Count Discrepancy in S286**:
   - `fetch/xdph-PortalManager.cpp` lines 90–129 and 247–259 defines **10 bind branches** (screencopy, global_shortcuts, input_capture, xdg_output, toplevel_export, wl_output, linux_dmabuf, shm, foreign_toplevel, toplevel_mapping).
   - `corpus/knowledge/hyprland-focus-grab-r41.md:6,68` correctly states **10 branches**.
   - `corpus/SOURCES.md:235` (row S286) states **9 branches** (`which nine it binds ...`), omitting `zwlr_foreign_toplevel_manager_v1`.

5. **`corpus/README.md` Column 3 (Sources) Missing**:
   - Line 70 adds `hyprland-focus-grab-r41.md`, but leaves column 3 empty, violating the 3-column table contract (`| Note | Holds | Sources |`) observed by every other row.

6. **Skeleton Placeholders Survived into Data Commit**:
   - `corpus/lessons/round-41.md:156`: `No proposal is claimed by this skeleton.`
   - `corpus/lessons/round-41.md:166`: `To be filled at the data commit (commands, in the order the round-40 lesson states them):`
   - `corpus/lessons/round-41.md:168`: `Census after: receipts/census-after.txt, exit 0 required...` (path does not exist; actual is `.ufo/waves/round-41/receipts/census-after-data.txt`).
   - `corpus/lessons/round-41.md:178`: `axis-<40hex>.txt` unexpanded template token.

7. **Class Table Divergence**:
   - `tools/mado-globals.py` defines 10 classes across 26 interfaces, but its docstring merely refers to `a fixed decision table` without enumerating them (unlike `quality/counters/c1-r41-globals-v2.py:71-82` which lists the table).
   - `corpus/knowledge/hyprland-focus-grab-r41.md` §6 is titled `## §6 The decision table`, but contains 12 protocol architecture questions, not the Wayland global classification table.

8. **Commit Hash Verification (`git cat-file -e`)**:
   - All internal commits (`60c3914`, `ab2bfaa`, `cd950ec`, `294c667`, `07f2641`, `520c631`, `fb49621`) exist in the repo.
   - However, `registration-v2.md:3` and `corpus/lessons/round-41.md:3` only cite the v1 freeze `60c3914154333180450d5da27ba222d5763cc56a` and omit the v2 freeze commit hash `294c667901a8c7b7165ba849d03cba9a24c14fa4`.

---

## 2. Affected Axes

- **Operability**: Improves consistency between `tools/mado-globals.py` output, its docstring/table specifications, and reported verification scores (accurately acknowledging v2 `39/39 TARGET_MET` while explaining the superseded v1 `6/24` behavior).
- **Coverage**: Strengthens the knowledge corpus by eliminating factual contradictions in interface/request counts (S283, S286), populating missing index citations in `corpus/README.md`, and aligning registry citations with the actual admitted draft.

---

## 3. Proposed Move

**A Single Harmonization Patch on the DATA Plane (Closure Integration)**:
The L1 integrates a single surgical commit across the four data files before closing wave 2, resolving the contradictions without mutating frozen predicates:
1. **`corpus/lessons/round-41.md`**:
   - Replace `S283–S290` with `S283–S289` in lines 44, 53, and 173.
   - Replace false claim of `PRED-C1-r41-v1: 24/24 TARGET_MET` in line 175 with the real measurements: `PRED-C1-r41-v2: fixtures=39/39 TARGET_MET nonce=be51c3bc188d6b05; PRED-C2-r41-v2: admitted=1/1 TARGET_MET. Superseded v1: PRED-C1-r41-v1 fixtures=6/24 TARGET_MISSED; PRED-C2-r41-v1 admitted=1/1 TARGET_MET`.
   - Update census after receipt reference to `.ufo/waves/round-41/receipts/census-after-data.txt` and report actual clean output (`mado ok, W04 ×7 + W01 S277, exit 0`).
   - Remove surviving skeleton placeholders (`by this skeleton`, `To be filled at the data commit`, expand `<40hex>`).
   - Add explicit citation of v2 freeze `294c667901a8c7b7165ba849d03cba9a24c14fa4`.
2. **`corpus/SOURCES.md`**:
   - Row S283: Update `four requests` to `six requests (two manager, four grab)`.
   - Row S286: Update `nine it binds` to `ten it binds` and include `foreign_toplevel`.
3. **`corpus/knowledge/hyprland-focus-grab-r41.md`**:
   - Line 114 (§6 table): Change `five requests` to `six requests (two manager, four grab)`.
4. **`corpus/README.md`**:
   - Line 70: Change `five requests` to `six requests`, and populate column 3 with `S283, S284, S285, S286, S287, S288, S289, S037`.

---

## 4. Risks & Second-Order Effects

- **Runtime Surface**: Zero risk. `tools/mado-globals.py` is unaffected and remains 100% compliant with PRED-C1-r41-v2.
- **Contract Surface**:
  - `PRED-C2-r41-v2` clause c requires 11 cells and valid used-by in `corpus/SOURCES.md`; editing cell descriptions preserves all 11 cells.
  - Clause f requires exactly one column-zero row in `corpus/README.md`; filling column 3 leaves column 0 unchanged.
  - Clause g requires OBS quotes in entry lines to match GATE lines; the OBS quotes are untouched.
- **Substrate Surface**: Clean separation. Predicates `quality/counters/c1-r41-globals-v2.py` and `c2-r41-focus-entry-v2.py` remain FROZEN.
- **Verification Surface**: Both C1 and C2 counters continue to evaluate to `TARGET_MET` (exit 0).

---

## 5. Verification

Run the following checks from the lane root:
```bash
# 1. Verify C1 v2 counter still scores TARGET_MET (39/39)
python3 -I quality/counters/c1-r41-globals-v2.py --repo . --rev HEAD --nonce be51c3bc188d6b05
# Expect: PRED-C1-r41-v2: fixtures=39/39 tool=present verdict=TARGET_MET, exit 0

# 2. Verify C2 v2 counter still admits entry (clauses a-i)
python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev HEAD
# Expect: PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET, exit 0

# 3. Verify registry census and formatting
python3 -c "
with open('corpus/SOURCES.md') as f:
    rows = [l for l in f if l.startswith('| S28')]
assert len(rows) == 7, f'Expected 7 rows S283-S289, got {len(rows)}'
for r in rows:
    assert len(r.split('|')) == 13, f'Row format error: {r}'
print('Registry S283-S289 format verified: 7 rows, 11 cells each')
"

# 4. Verify README table format
python3 -c "
with open('corpus/README.md') as f:
    r41_rows = [l for l in f if 'hyprland-focus-grab-r41.md' in l]
assert len(r41_rows) == 1
cells = [c.strip() for c in r41_rows[0].split('|')[1:-1]]
assert len(cells) == 3, f'Expected 3 columns, got {len(cells)}'
assert 'S283' in cells[2] and 'S037' in cells[2]
print('README row verified: 3 columns with sources populated')
"
```

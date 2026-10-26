# Cross-Reading Contradictions Audit: Round 41 (Data Commit 07f26416)

Audit conducted by seat `ConnClaimsVsBytes` (Wave 2, Round 41) cross-reading:
- `registration-v2.md` (`294c667901a8c7b7165ba849d03cba9a24c14fa4`)
- `corpus/lessons/round-41.md` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- `corpus/knowledge/hyprland-focus-grab-r41.md` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- `corpus/SOURCES.md` rows S283–S289 (+ S037 used-by) at `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- `corpus/README.md` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- `tools/mado-globals.py` at `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- Predicates `quality/counters/c1-r41-globals-v2.py` and `c2-r41-focus-entry-v2.py`
- Pre-fetched receipts under `.ufo/waves/round-41/fetch/` and after-data receipts under `.ufo/waves/round-41/receipts/`

---

## 1. Summary of Cross-Reading Dimensions

### A. IDs & S290 Mentions
- **Fact**: The final landed entry `corpus/knowledge/hyprland-focus-grab-r41.md` selected Draft A, which cites **eight** ids: seven new (`S283, S284, S285, S286, S287, S288, S289`) and one held (`S037`).
- **Fact**: `corpus/SOURCES.md` added exactly rows S283–S289. Row S290 was drafted by `ScrRowsDraft` for `input-capture-v1.xml`, but was intentionally omitted from `corpus/SOURCES.md` because Draft A does not cite it.
- **Defects in Lesson**:
  1. `corpus/lessons/round-41.md:38` correctly states: `S290 (input-capture-v1.xml) is not cited by the entry and has no row.`
  2. In direct contradiction, `corpus/lessons/round-41.md:44` states: `re-grounded this round as C2 with lane ids S283–S290`.
  3. `corpus/lessons/round-41.md:53` states: `and the new rows S283-S289 continue in the order ScrRowsDraft drafted them: focus-grab-v1.xml S283, Hyprland FocusGrab.cpp S284, quickshell grab.cpp S285, xdph PortalManager.cpp S286, issue #565 S287, hyprland-protocols README S288, the own-work journal S289, input-capture-v1.xml S290.` (Appends S290 to the S283–S289 list).
  4. `corpus/lessons/round-41.md:173` states: `Registry rows 219 → 219 + n, n = the cited new ids (at most S283–S290)`. S290 is neither cited nor added.

### B. Counts: Requests in S283 and Binds in S286
- **Request count discrepancy across 4 files**:
  - `protocols/hyprland-focus-grab-v1.xml` (receipt): 2 interfaces, **6 requests**, 1 event:
    - `hyprland_focus_grab_manager_v1`: `create_grab`, `destroy` (2 requests).
    - `hyprland_focus_grab_v1`: `add_surface`, `remove_surface`, `commit`, `destroy` (4 requests), `cleared` (1 event).
  - `corpus/knowledge/hyprland-focus-grab-r41.md` §1 lines 22–32 correctly lists all 6 requests.
  - BUT `corpus/SOURCES.md:232` (row S283) says: `The two interfaces, four requests and one event that define a focus grab` (says **4** requests).
  - AND `corpus/knowledge/hyprland-focus-grab-r41.md:114` (§6) says: `S283: two interfaces, five requests, one event (§1)` (says **5** requests).
  - AND `corpus/README.md:70` says: `the Hyprland focus-grab protocol (two interfaces, five requests, one cleared event)` (says **5** requests).
- **Bind count discrepancy in S286**:
  - `fetch/xdph-PortalManager.cpp` lines 90–129 and 247–259 contains **10 interface bind branches**: screencopy, global shortcuts, input capture, xdg-output, toplevel export, wl_output, linux dmabuf, wl_shm, foreign toplevel (`zwlr_foreign_toplevel_manager_v1`), toplevel mapping.
  - `corpus/knowledge/hyprland-focus-grab-r41.md:6,68` correctly states: `binds ten of them` and enumerates the 10 interfaces.
  - BUT `corpus/SOURCES.md:235` (row S286) states: `Which advertised globals the installed portal logs and which nine it binds ... the portal binds nine named interfaces none of which is the focus-grab manager` (omits `foreign toplevel`).

### C. `corpus/README.md` Missing Sources Column
- `corpus/README.md:10` defines the 3-column table: `| Note | Holds | Sources |`.
- The added row at line 70 (`hyprland-focus-grab-r41.md`) has only 2 columns; the `Sources` column is missing/blank.

### D. Surviving v1 Wording & Skeleton Placeholders in `corpus/lessons/round-41.md`
- **Measured Predicate Outcomes**:
  - `corpus/lessons/round-41.md:175` states:
    `- PRED-C1-r41-v1 at the data commit: fixtures=24/24 verdict=TARGET_MET with the nonce printed; PRED-C2-r41-v1: admitted=1/1 verdict=TARGET_MET; both re-run at the tip.`
  - In reality:
    1. `PRED-C1-r41-v1` at the data commit scored `fixtures=6/24 tool=present verdict=TARGET_MISSED rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=cb2bcd4259089823` (committed receipt `.ufo/waves/round-41/receipts/c1-v1-after-data.txt`). The tool missed v1 because it emits the v2 `ignored=0` field and triggers v1 clause g.
    2. The registered v2 claims in `registration-v2.md` bind to `PRED-C1-r41-v2` (`fixtures=39/39 TARGET_MET nonce=be51c3bc188d6b05`) and `PRED-C2-r41-v2` (`admitted=1/1 TARGET_MET`), but neither v2 score was reported in the Census section!
- **Placeholder text**:
  - Line 156: `No proposal is claimed by this skeleton.` (survived from skeleton).
  - Line 166: `To be filled at the data commit (commands, in the order the round-40 lesson states them):` (survived from skeleton).
  - Line 168: `Census after: receipts/census-after.txt, exit 0 required...` (actual receipt is `.ufo/waves/round-41/receipts/census-after-data.txt`, and result was not reported).
  - Line 173: `Registry rows 219 → 219 + n, n = the cited new ids (at most S283–S290)` (formula not expanded to measured count `219 → 226`).
  - Line 178: `axis-<40hex>.txt` (unexpanded placeholder).

### E. The Class Table in Tool vs Docstring vs Entry
- `tools/mado-globals.py`: Implements `CLASSES` with 10 classes and 26 interface names; unmapped interfaces classify as `"other"`.
- `tools/mado-globals.py` docstring: Mentions `a class from a fixed decision table`, but does not enumerate the 10 classes or interface members. In contrast, `quality/counters/c1-r41-globals-v2.py` docstring lines 71–82 enumerates the entire table.
- `corpus/knowledge/hyprland-focus-grab-r41.md`: Section §6 is titled `## §6 The decision table`, but contains a 12-row table of protocol questions and answers (`question | where the answer lives | state`), completely distinct from the Wayland global class table. (Draft B attempted to apply the class table to the journal in the entry, but Draft A was selected and omitted it).

### F. Git Commit & Hash Reference Audit (`git cat-file -e`)
- `60c3914154333180450d5da27ba222d5763cc56a`: Lane v1 freeze (valid commit).
- `ab2bfaab661c846d1de9d58c01651cd156a13949`: Lane base commit (valid commit).
- `cd950ec781149040cc73d71cd67c2b67452e7724`: Lane wave w1 dispatch (valid commit).
- `294c667901a8c7b7165ba849d03cba9a24c14fa4`: Lane v2 freeze (valid commit, but commit hash omitted from `registration-v2.md` and `corpus/lessons/round-41.md`).
- `07f2641696b5ac73de1404ea737a9f27e9819aa1`: Lane data commit (valid commit).
- `520c631d2925807aadadb041eeda13f8b829b0c5`: Round-36 axis receipt commit (valid commit).
- `fb49621074518333d855a2664ba5884c381079ad`: Round-40 tip commit (valid commit).
- Upstream commits:
  - `efb50993780079460b0cbed1363e2166a2de1d9f`: Hyprland v0.56.2 (matches host `hyprctl version`).
  - `cd1aba6bd78775825eb230b3a4274c48b6705eb7`: hyprland-protocols pin.
  - `9b0f339b19057f4731bf3b48293307d7ef241671`: quickshell pin.
  - `cc8e5ef`: xdph v1.4.1 release tag commit.
  - `b09f157`: Hyprland commit cited in issue 565.

---

## 2. Table: statement | where | contradicts | fix

| statement | where | contradicts | fix |
|---|---|---|---|
| `re-grounded this round as C2 with lane ids S283–S290` | `corpus/lessons/round-41.md:44` | `corpus/lessons/round-41.md:38` ("S290 is not cited by the entry and has no row"), `corpus/SOURCES.md` (only rows S283–S289 added), commit `07f26416` message (`rows S283-S289`), and `hyprland-focus-grab-r41.md` (cites S283–S289 + S037; S290 omitted). | Change `S283–S290` to `S283–S289`. |
| `and the new rows S283-S289 continue in the order ScrRowsDraft drafted them: focus-grab-v1.xml S283, Hyprland FocusGrab.cpp S284, quickshell grab.cpp S285, xdph PortalManager.cpp S286, issue #565 S287, hyprland-protocols README S288, the own-work journal S289, input-capture-v1.xml S290.` | `corpus/lessons/round-41.md:53` | Contradicts the sentence's own opener "the new rows S283-S289", row S289 being the last row in `corpus/SOURCES.md`, and line 38 stating S290 has no row. | Truncate the list at S289: `the own-work journal S289 (S290 input-capture-v1.xml was drafted by ScrRowsDraft but not added because the entry does not cite it).` |
| `Registry rows 219 → 219 + n, n = the cited new ids (at most S283–S290); tier A additions counted from the registry.` | `corpus/lessons/round-41.md:173` | Contradicts line 38 and `corpus/SOURCES.md`: exactly 7 rows (S283–S289) were added, making the registry 219 → 226; S290 is not cited and was not added. Also leaves an unexpanded placeholder in a data commit. | Replace with measured count: `Registry rows 219 → 226 (7 new ids S283–S289; 5 tier A: S283, S284, S286, S288, S289; 2 tier B: S285, S287).` |
| `PRED-C1-r41-v1 at the data commit: fixtures=24/24 verdict=TARGET_MET with the nonce printed; PRED-C2-r41-v1: admitted=1/1 verdict=TARGET_MET; both re-run at the tip.` | `corpus/lessons/round-41.md:175` | Directly contradicts `.ufo/waves/round-41/receipts/c1-v1-after-data.txt` which scored `fixtures=6/24 tool=present verdict=TARGET_MISSED rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=cb2bcd4259089823 exit=1` (missed because v2 tool outputs `ignored=0` and triggers v1 clause g). Also contradicts `registration-v2.md` claims which bind to PRED-C1-r41-v2 (`39/39 TARGET_MET nonce=be51c3bc188d6b05`) and PRED-C2-r41-v2 (`1/1 TARGET_MET`), neither of which was reported here. | Report actual measurements: `PRED-C1-r41-v2 at the data commit: fixtures=39/39 tool=present verdict=TARGET_MET nonce=be51c3bc188d6b05; PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET. Superseded v1: PRED-C1-r41-v1 fixtures=6/24 TARGET_MISSED (v2 ignored= field and clause g); PRED-C2-r41-v1 admitted=1/1 TARGET_MET.` |
| `The two interfaces, four requests and one event that define a focus grab` | `corpus/SOURCES.md:232` (row S283) | Contradicts `protocols/hyprland-focus-grab-v1.xml:39-127` and `hyprland-focus-grab-r41.md:22-32` (§1), which enumerate 6 requests (2 on manager: `create_grab`, `destroy`; 4 on grab: `add_surface`, `remove_surface`, `commit`, `destroy`), and contradicts entry §6 & README:70 which claim 5 requests. | Update to reflect the full request count: `The two interfaces, six requests (two manager, four grab) and one event that define a focus grab`. |
| `S283: two interfaces, five requests, one event (§1)` | `corpus/knowledge/hyprland-focus-grab-r41.md:114` (§6 decision table) | Contradicts `protocols/hyprland-focus-grab-v1.xml` and entry §1 lines 22–32, which detail 2 manager requests and 4 grab requests (total 6 requests), and contradicts SOURCES.md S283 row which says 4 requests. | Change `five requests` to `six requests (two manager, four grab)`. |
| `the Hyprland focus-grab protocol (two interfaces, five requests, one cleared event)` | `corpus/README.md:70` | Contradicts `protocols/hyprland-focus-grab-v1.xml` and entry §1 lines 22–32 (total 6 requests), and row S283 (which says 4 requests). | Change `five requests` to `six requests`. |
| `Which advertised globals the installed portal logs and which nine it binds ... the portal binds nine named interfaces none of which is the focus-grab manager` | `corpus/SOURCES.md:235` (row S286) | Contradicts `fetch/xdph-PortalManager.cpp` lines 90–129 and 247–259 (which contains 10 bind branches), and contradicts `hyprland-focus-grab-r41.md:6,68` (`the registry listener that logs every global and binds ten of them`). S286 row omits `foreign toplevel`. | Update row S286 to: `which ten it binds ... (screencopy, global_shortcuts, input_capture, xdg_output, toplevel_export, wl_output, linux_dmabuf, shm, foreign_toplevel, toplevel_mapping) ... the portal binds ten named interfaces`. |
| `| knowledge/hyprland-focus-grab-r41.md (MADO-R41-1...) | Focus as a protocol surface: ... |` (third column empty) | `corpus/README.md:70` | Contradicts table header `| Note | Holds | Sources |` (`corpus/README.md:10`) where every other row populates column 3 with its cited source IDs. | Add `S283, S284, S285, S286, S287, S288, S289, S037` into the third column. |
| `No proposal is claimed by this skeleton.` | `corpus/lessons/round-41.md:156` | Contradicts the document status: this is the committed lesson of round 41 in commit `07f26416`, not an uncommitted skeleton draft. | Remove `by this skeleton` and state whether a considerthese proposal was adopted or none mined this round. |
| `To be filled at the data commit (commands, in the order the round-40 lesson states them):` | `corpus/lessons/round-41.md:166` | Contradicts the commit status: commit `07f26416` is the data commit. Surviving unedited instruction from w1 skeleton. | Remove the placeholder header line. |
| `Census after: receipts/census-after.txt, exit 0 required, warning set unchanged or every new line named.` | `corpus/lessons/round-41.md:168` | Contradicts filesystem structure (no top-level `receipts/` directory exists; the file is `.ufo/waves/round-41/receipts/census-after-data.txt`), and states a requirement rather than recording the actual measurement. | Update path to `.ufo/waves/round-41/receipts/census-after-data.txt` and report actual output: `mado ok, W04 ×7 (S030, S042, S045, S097, S119, S120, S121) + W01 S277, exit 0`. |
| `axis-<40hex>.txt` | `corpus/lessons/round-41.md:178` | Contradicts completed documentation: `<40hex>` is an unexpanded template placeholder surviving from skeleton. | Replace with the tip axis transcript reference once committed at closure. |
| `freeze 60c3914154333180450d5da27ba222d5763cc56a` without citing v2 freeze commit hash | `corpus/lessons/round-41.md:3` and `.ufo/waves/round-41/registration-v2.md:3` | `60c3914` is the superseded v1 freeze. The v2 freeze is `294c667901a8c7b7165ba849d03cba9a24c14fa4` which committed the v2 predicates, controls, and receipts before the data commit. | Add explicit reference to v2 freeze `294c667901a8c7b7165ba849d03cba9a24c14fa4`. |
| `reports the latest session's globals, each with a class from a fixed decision table...` without specifying the table | `tools/mado-globals.py:9-11` (docstring) | Contradicts `quality/counters/c1-r41-globals-v2.py:71-82` which fully specifies the 10 classes and members; leaves users unable to determine valid classes from tool docstring alone. | Add the 10 class definitions and their interface sets to the docstring and `--help` text of `tools/mado-globals.py`. |

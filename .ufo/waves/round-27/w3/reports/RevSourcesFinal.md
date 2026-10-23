# RevSourcesFinal — pre-commit audit of the final `corpus/SOURCES.md` state

Seat: `MadoR27.RevSourcesFinal` (w3 reviewer, read-only on the lane). Audit ran 2026-10-23.

**Timing**: the L1's commit landed mid-audit — `86f7355` ("round-27: SOURCES S178-S182 + S158/S162
used-by (E01 gate quotes moved to lesson), knowledge note workspace-rules-r27, …", 15:17 -0300). I
observed the fix in flight (`wc -l` on the working file moved 427→424→422 as the five gate-quote
rows were deleted), then verified the **committed bytes** directly:
`git show 86f7355:corpus/SOURCES.md` sha256 `6aadfd31ba4e9b14551f22bda996bc81aa98987f5ac76c6612a3ffc59c5536c9`
= working tree = my sim copy; `git diff HEAD -- corpus/SOURCES.md` clean. Everything below is
verified against the exact bytes the L1 committed — strictly stronger than auditing a plan.

## 1. Per-row verdict — S178–S182 vs the w2 Reopen* verdicts

Fetch bytes audited at `.ufo/waves/round-27/fetch/*.bin` (`sha256sum`, `grep -a -n`, `read` of cited
ranges). Landed rows are **byte-identical** to `drafts/sources-rows.md` (diff: draft adds only the
5 located-quote lines that stayed out of the registry).

| row | URL+pin | sha256 row↔fetch | located quote in fetch bytes | verdict |
|---|---|---|---|---|
| S178 | `hyprland-wiki/ecc06f3b6605/content/Configuring/Workspace-Rules.md`, anchor cites full sha `ecc06f3b6605e453c0ad533d979fccbefff788ef` | `486143a0…ab62` = fetch = ReopenWiki re-fetch | `47:  workspace selectors can only match _existing_ workspaces.` — verbatim, ∈ anchor 38-55; ReopenWiki located 4/4 | **OK** |
| S179 | `Hyprland/efb5099…/src/config/shared/workspace/WorkspaceRuleManager.cpp` (v0.56.2) | `06e8dcba…d10` = fetch = ReopenRuleManager re-fetch | `45:        mergedRule.mergeLeft(*rule);` — verbatim at :45, ∈ anchor 34-52; ReopenRuleManager located 4/4 | **OK** |
| S180 | `Hyprland/efb5099…/src/config/shared/complex/ComplexDataTypes.hpp` | `95733223…807` = fetch = ReopenLegacy re-fetch | `84:        CCssGapData(int64_t vertical, int64_t horizontal) : m_top(vertical), …` — verbatim at :84, ∈ anchor 80-120; ReopenLegacy located 4/4 | **OK** |
| S181 | `Hyprland/efb5099…/src/config/shared/parserUtils/ParserUtils.cpp` | `86f21b76…c2c0` = fetch = ReopenBoolExec re-fetch | `138:    if (val.starts_with("true") || val.starts_with("on") || val.starts_with("yes"))` — verbatim at :138, ∈ anchor 134-149; ReopenBoolExec located 1/1 | **OK** |
| S182 | `Hyprland/efb5099…/src/helpers/MiscFunctions.cpp` | `06541824…c1d9` = fetch = ReopenBoolExec re-fetch | `506:            rules = "[" + workspaceRule + "]";` — verbatim at :506, ∈ anchor 478-513; ReopenBoolExec located 3/3 | **OK** |

Pins agree with each Reopen verdict (S178 short-pin URL resolves to the full commit ReopenWiki
API-verified; S179–S182 pin `efb50993780079460b0cbed1363e2166a2de1d9f` = v0.56.2). No row defect.

## 2. S158/S162 used-by extensions

Applied exactly per `drafts/sources-rows.md` old→new:

- **S158** (`SOURCES.md:170`): `…, corpus/knowledge/animation-table-r26.md` → `…, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md` ✓
- **S162** (`SOURCES.md:174`): `…, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md` → `…, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md` ✓

Only the `used-by` cells changed; anchors untouched (in-place rule). Named files:

- `corpus/knowledge/workspace-rules-r27.md` — **exists**; committed in the same commit `86f7355`
  (67 changed lines; the file carries the S178–S182 + S158/S162 citations). At assignment/draft time
  this was `pending L1 landing` — resolved during the audit; draft `drafts/workspace-rules-r27.md`
  also exists.
- `tools/mado-wsrules.py` — **exists** at lane root, 29,661 B, sha256
  `722c7ae47eaee57eda4c6a223f4dad6fc585018453c2f7a2fd26c52d1e006008` = the landed C1 bytes.
- ReopenRuleManager's S162 anchor-range proposal (`335-342,608-610,1676-1792`) was deliberately not
  applied: the anchor cell is not an in-place field under the registry header; 608-610 already sits
  inside the existing `590-623` anchor; the workspace-handler coverage is carried by the new rows
  and the knowledge note. Consistent — not a defect.

## 3. Post-fix census simulation (the real `scripts/sources-census.sh`, run against a lane-mirror sim root)

Sim root `/fast/scratch/hyaku/mado-r27/revsourcesfinal/`: full lane root mirrored via symlinks
(`corpus/` a real dir whose subentries symlink into the lane; `corpus/SOURCES.md` = copy of the
committed bytes). Ran `sources-census.sh validate --today 2026-10-23 --file …` and `census`.

- **Result: `file  ok`, exit 0.** Zero E-code findings (E01–E12).
  E11 is clean: every used-by path, including `corpus/knowledge/workspace-rules-r27.md` and
  `tools/mado-wsrules.py`, resolves.
- Remaining output = 7 pre-existing **W04** warnings (S030, S042, S045, S097, S119, S120, S121) —
  historical same-URL-across-scope warnings, none involving S178–S182, none failing validation.
- Mechanical field/id pass over all 182 rows: every `| S…` row has NF=13 `-F'|'` fields; ids are
  `S001`…`S182` with no gaps or duplicates; S178–S182 have exactly one URL in the source cell,
  `opened=2026-10-23` (today — E08-safe), `status=mined` ∈ enum, `recheck=on-release` ∈ symbolic
  cadence, `kind` ∈ {docs,code}, `tier=A` non-community.
- **Pre-fix demo (why removal was required):** re-injecting the draft's five two-cell located-quote
  rows after S182 inside `## Registry` reproduces `E01` ×5, exit 1 — `fields=2` for S178/S179/S180/S182
  and `fields=6` for S181 (its `||` token splits on unescaped `|`). The lesson draft M27-2 records
  the same E01 finding. Removal was the correct and only fix; the committed file contains zero
  quote-shaped rows (`grep -c -E '^\| S[0-9]{3} \| `' → 0).
- Census totals: `rows=182  tier.A=175  tier.B=1  tier.C=6  mined=163  queued=10  rejected=9`.

## 4. Row counts

- **Before**: `git show ca13523:corpus/SOURCES.md` (round-26 tip) → **177 rows, last id S177** ✓
- **After**: `86f7355` committed file → **182 rows, last id S182** ✓ (177 + 5 new; S158/S162 edited in place)

## 5. Residual violations — the L1's must-fix list

**SOURCES census violations: none.** The committed state passes `sources-census.sh validate` clean (exit 0).

**MEDIUM — stale lesson draft (not a registry/schema defect):** `drafts/lesson-round-27.md:14` still says the current registry snapshot contains the five malformed rows, that no post-fix clean receipt was found, and removal/revalidation remain pending. This is contradicted by committed `86f7355` and the post-fix validation (exit 0). Before landing `corpus/lessons/round-27.md`, update M27-2 to record the removal and clean result. The Gate table and S158/S162 old→new entries are already in the draft; S181's `||` is escaped for the Markdown table.

**Provenance-log duty still pending:** `corpus/lessons/round-27.md` does not yet exist. The registry header requires used-by changes logged old→new in the round lesson, and the located quotes belong in its `## Gate` table. Draft content is at `drafts/lesson-round-27.md:17-32`; this is separate from the clean census result.

Non-blocking traceability observations (not census violations):

1. S158/S162's extensions add `corpus/knowledge/workspace-rules-r27.md`; their cells do not add `tools/mado-wsrules.py`. The new S178–S182 rows do name both the knowledge note and tool. Both targets exist. This matches the prepared old→new draft; if `used-by` is intended to enumerate every source consumer, consider whether the existing rows also need the tool path.
2. S179's anchor `34-52` includes `getWorkspaceRuleFor`'s `return mergedRule` at :52; ReopenRuleManager described the function body as 34-51 — cosmetic range-boundary difference only.
3. Relayed from `MadoR27.CritC1Claim`: S172/S173 used-by still list only `tools/mado-binds.py` though the new tool consumes those hyprlang surfaces; S182's `478-513` anchor covers `cleanCmdForWorkspace` while the tool docstring also names `getWorkspaceIDNameFromString` (ConfigManager.cpp:1680-1682, S162's side). Traceability-completeness observations, not census errors.

## 6. Method, safety, scope

- Verification: `scripts/sources-census.sh` (validate+census against a full lane-mirror scratch
  root), `sha256sum`, `grep -a -n`, `awk` field/id scans, `read` ranges on fetch bins, `git show`/
  `git log`/`git diff` **read-only**. No counter, oracle, Hyprland process, or suite run — out of
  scope for a sources audit.
- Writes: only this report and scratch under `/fast/scratch/hyaku/mado-r27/revsourcesfinal/`
  (snapshot, sim mirror, `check.sh`). No git/jj mutation; no lane file touched.
- Tools installed/upgraded: **none** (bash, gawk, git, sha256sum already present).
- Limitation honestly stated: my working-tree snapshot was taken after the L1's row removal
  completed, so the E01 violation was re-demonstrated by faithful reconstruction (injecting the
  draft's five rows) — the lane itself observed the original E01 run per lesson-draft M27-2.
- Receipts `c1-after-48b9434a.txt` / `c2-after-48b9434a.txt` were not consulted (this item needs no
  counter output; not a `receipt pending` case).

Report: `.ufo/waves/round-27/w3/reports/RevSourcesFinal.md`

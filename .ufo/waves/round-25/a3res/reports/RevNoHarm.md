NOHARM: no axis harmed

# Round 25 attempt 3 — harm watch (RevNoHarm, read-only seat)

- Scope measured: base `41cc04c8` → tip `master` = `90224671e8e0a265ecc96b54100f981e31afe2c9`, plus the
  working-tree SCORECARD.md. Working-tree SCORECARD.md is byte-identical to master (`git diff master -- SCORECARD.md`
  empty); the C2 ledger `## Current state (round 25)` (SCORECARD.md:1629) landed inside the range in `9022467`.
  Ancestry checked: `41cc04c8` and measured commit `ef94763c` are both ancestors of master; the tool blob
  `tools/mado-binds.py` is byte-identical between `ef94763c` and master (git blob `bd543847…` both sides), so the
  measurement receipt describes master's bytes.
- All re-runs ran in a sandbox clone at master (`/fast/scratch/hyaku/mado-r25a3/res/RevNoHarm/clone`,
  `git clone --no-hardlinks`, `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset), `ulimit -v 4194304`, every command
  under `timeout`. No lane file touched except this report; no nested Hyprland started; no host/package/config change;
  no tool installed (stock git/python3/bash sufficed — record per tooling directive: zero installs).
- Lane snapshot at review end: master unchanged at `9022467`; live working-tree churn by other seats is purely
  additive (see §5) and was not part of the measured diff.

## 1. tools/ surface

`git diff --stat 41cc04c8 master -- tools/`:

```
 tools/mado-binds.py | 496 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 496 insertions(+)
```

Only the new `tools/mado-binds.py`; every other tracked tool byte-identical to base (nothing else listed, 0 removed
lines in the whole range for `tools/`). All six tracked tools are named by the round-23 C3 counter's `tracked_tools`
at master: mado-action-plan.py, mado-assessment.py, mado-binds.py, mado-evidence-audit.py, mado-tripwire.py,
mado-verify.sh.

## 2. Complete removed-line inventory (`git diff --numstat 41cc04c8 master`, 158 files; machine filter `$2 > 0`)

Exactly two files lose lines; both are in-row row edits, zero other removals anywhere (LOG.md, SHONEN.md, SKILL.md,
README.md not touched by the committed range at all; SCORECARD +50/-0; corpus/QUALITY.md +4/-0; PROVINCE.md +1/-0;
corpus/lessons/round-24.md +13/-0; .ufo/waves/round-24/registration.md +7/-0):

1. `corpus/knowledge/rule-attribution-r24.md` — 1 removed line = the `logs` row at `:25` (A18). **Declared R3
   in-row correction.** Replacement states the A18 line logs the window-rule `workspace` *effect*, not a
   workspace-rule path, matching item 5 of the same file; an appended `## Errata (round 25; append-only)` section
   names repair R3, cites the round-24 closure (`round-24-verifier-spotcheck.md:72-73,184-185`) and declares this
   "the only body line" corrected. Matches the registration's R3 disposition exactly.
2. `corpus/SOURCES.md` — 2 removed lines = rows S162 (`:174`, Hyprland ConfigManager.cpp) and S167 (`:179`,
   using-hyprctl wiki). **Not the R3 exemption — a second in-row edit class; see note below.** Diff of both rows:
   every cell byte-identical (URL, anchor, sha256 `9db68cf4…`/`95d8b842…`, byte counts 90963 B / 8239 B, status,
   dates) except the last (`used-by`) cell, which appends `, corpus/knowledge/bind-table-r25.md`. Truthful: the
   committed `corpus/knowledge/bind-table-r25.md` cites S162 (19 lines) and S167. Sanctioned by SOURCES' own
   contract header ("Only `status`, `recheck` and `used-by` change in place, each logged old→new in that round's
   lesson"): the required old→new log exists in the round-25 lesson (`corpus/lessons/round-25.md:42` and `:46`,
   currently untracked/pending). The appended LOG.md round-25 section discloses it too ("S162 and S167 gained the
   new note in used-by"). No evidence cell changed, so no sourced claim's provenance moved.
   **Note (letter, not harm):** the registration's harm-watch sentence excepts only "the R3 in-row correction
   (one line, reported)"; these two used-by appends are a third in-row edit it does not name. Substance: allowed by
   the registry's own mutability rule, disclosed and logged, zero semantic delta. Registering the note; no axis
   loses information.
3. `c1/count.py` — **no removed lines.** Cumulative numstat is a new-file +304/-0; counter versions v1–v3 are
   preserved as separate byte-pinned files `count-v1.py`/`count-v2.py`/`count-v3.py` (all new files, 0 removals);
   the round's own instrument was never cut back.

## 3. Census

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`:

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

Exit 0. Same 7 W04 duplicate-url warnings the lane already recorded as present at round start (SCORECARD.md:1617);
round 25 introduced none (its 4 new rows S169–S172 produced no warning).

## 4. Round-23 harm-watch counters re-run at master (sandbox clone, `counter_version: 2` both)

- C3 (SHONEN box 4 vs PROVINCE): `python3 -I .ufo/waves/round-23/c3/count.py 9022467…` →
  `"mismatches": []`, `"count": 0`, **exit 0**. Side value: it mechanically confirms the new PROVINCE row accounts
  for `tools/mado-binds.py` (all 6 tracked tools in `accounted_rows`), i.e. the one permitted PROVINCE addition is
  well-formed.
- C2 (foot/kitty/ghostty sourced routes): `python3 -I .ufo/waves/round-23/c2/count.py 9022467…` →
  `"count": "3/3"` (foot 8 rows, kitty 9, ghostty 8), **exit 0**.

Both equal the round-23 after-values (0 and 3/3): no regression of prior rounds' measurements.

## 5. Existing capabilities re-run at master (sandbox clone)

- `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed`, **exit 0** (12.8 s).
- `python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` → all cases pass,
  **exit 0**.

## 6. Other range observations

- PROVINCE.md +1: exactly the new tool row `| \`tools/mado-binds.py\` | the bytes of DIR/.config/hypr/hyprland.conf
  under --home DIR …` — the one addition the harm watch permits "only if C1 lands"; C1's committed receipt
  (`.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt`, single run 2026-10-23T07:46:44Z, seed
  `ed0d8a943980d2f2`) reads `PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET`, `exit=0`.
- SCORECARD.md hunks are three pure insertions (+50/-0): pointer lines at the two R6 stale rows (`:437`,
  `:1342` areas) and the appended `## Current state (round 25)` section at `:1629`.
- corpus/QUALITY.md +4: appended criterion 36 (R1/R2 disposition); lessons/round-24.md +13 and round-24
  registration.md +7: appended R4/R5 corrections. All additive, all matching the routed-repairs table.
- Live (uncommitted, post-measurement, other seats'): LOG.md +22/-0, corpus/README.md +8/-0,
  corpus/knowledge/bind-table-r25.md +14/-0, untracked `corpus/lessons/round-25.md` (holds the SOURCES old→new
  used-by log) and untracked `a3res/`, `a3w2/reports/RevRepairs.md`. No line removed in any of them.

## 7. Residual risk / verification gaps

- Tip could move again (peers actively landing). All five checks were run against `9022467`; if master advances,
  re-run §3–§5 in a fresh clone before closure.
- The SOURCES used-by letter-note (§2.2) resolves only when `corpus/lessons/round-25.md` (currently untracked)
  and the pending LOG/README appends are committed; if they are dropped instead, the two in-row used-by edits
  would be unlogged against SOURCES contract v1 — flag for the closure seat.
- Census W04 warnings pre-exist and are out of scope to fix; not introduced by round 25.

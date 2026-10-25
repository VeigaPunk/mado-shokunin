# ExecC1ManifestDiff — C1 manifest delta report (wave w1, round 39)

## Task
Document the exact manifest delta that makes the frozen pair discriminate (C1): extract the frozen
manifest and 58e55ec vs the repaired manifest at BASE (08be4eb7fd13358ed29b096e8924005d46ac409c),
produce the unified diff, identify the changed control, and confirm from the counter's code why the
append escapes the parser.

## Commands run (read-only; no lane mutation)
- `git diff 58e55ec 08be4eb7fd13358ed29b096e8924005d46ac409c -- .ufo/waves/round-38/controls/manifest.json`
  → saved to `manifest-diff.txt` (360 lines). Diff header: `index 93f168c..ec34732 100644`; 1 file
  changed, 254 insertions(+), 99 deletions(-). The bulk of the diff is pure re-formatting: the frozen
  JSON used compact per-control arrays; the repaired manifest is pretty-printed (one key per line).
- JSON semantic comparison (git show + json.load on both revs): both manifests are
  `MANIFEST-r38-v1` with 19 controls in the same order; **exactly one control differs semantically:
  `c1-duprow`**.
- `git show 08be4eb7...:corpus/SOURCES.md` → section-heading scan: `## Registry` at line 9,
  `## Paths` at line 225, `## Search log` at 271, `## Leads (unopened)` at 435; the S217 row sits at
  line 219 (inside the Registry section).

## The exact delta (c1-duprow write op)
| | Frozen (58e55ec) | Repaired / BASE (08be4eb7) |
|---|---|---|
| op | `"op": "append", "path": "corpus/SOURCES.md", "text": "\| S189 \| contradicting duplicate … \n"` | `"op": "py", "code": "p='corpus/SOURCES.md' … lines[i+1:i+1]=[dup] …"` |
| effect | appends the duplicate S189 row at **end of file** (~line 461, after the footer/`config-era`/`portal` prose) | Python insert of the duplicate S189 row immediately after the **last line starting `\| S217 \|`** (line 219, mid-table, inside the Registry section) |
| expected | TARGET_MISSED | TARGET_MISSED |
| observed | MET (clause j passes → `18/19`, red-before receipt exists) | MISSED (→ `19/19`) |

Everything else about the control (id, instrument, expect, clause=j, note, the dup row text) is
byte-identical; only the write mechanism differs.

## Why append-at-file-end escapes the parser (counter code, quality/counters/c1-r38-event-ground.py)
- Clause j (docstring lines 18-19): "unique row — every cited id has exactly one `## Registry` row
  (v2 F3: an appended contradicting row passed c alongside the held one)" — the v2 F3 failure mode is
  literally named in the clause.
- `registry_rows()` (lines 135-142) builds `rows` only from `section(text, "## Registry")`.
  `section()` (lines 122-132) collects lines only **between** the exact `## Registry` heading and the
  next line starting with `## ` — i.e. it stops at `## Paths` (line 225 of SOURCES.md). The Registry
  section is therefore bounded at ~line 224; content at file end (~line 461) is outside it.
- Clause j scoring (line 226): `j_ok = j_ok and len(rows.get(i, [])) == 1` — for each cited id,
  exactly one Registry row must exist. With the append write, the duplicate S189 row lands outside the
  section, ROW_RE never sees it, `rows["S189"]` stays length 1, clause j passes → MISSED expected but
  MET observed (18/19).
- With the repaired py write, the duplicate row lands inside the section (after S217, before `## Paths`),
  `rows["S189"]` becomes length 2 → clause j fails → MISSED as expected (19/19).

## Evidence files
- `.ufo/waves/round-39/w1/ExecC1ManifestDiff/manifest-diff.txt` (the unified diff, 360 lines).

## Risks / notes
- No tool installs performed (none needed; stock git/python3 only).
- No lane files written or touched other than the report and the requested diff file; all git access
  was read-only (show/diff).

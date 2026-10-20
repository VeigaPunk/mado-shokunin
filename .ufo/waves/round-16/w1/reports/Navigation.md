# MadoR16.Navigation — index row convention and unique-note navigation counting

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline HEAD `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.
`git status --porcelain` at review time: ` M SCORECARD.md` and `?? .ufo/waves/round-16/` only. `corpus/README.md` and `corpus/knowledge/` have no uncommitted change, so working-tree bytes equal HEAD for every input below.

Method: source reads (`read`, `grep`) and read-only Python parsing of those same file bytes. No `tools/mado-verify.sh`, no `measure.py`, no selftest, no live probe was executed. Installs this round: none. Tool record: none.

## 1. Exact counts (measured)

| Quantity | Value | Anchor |
|---|---|---|
| Index rows matching `^\| \`knowledge/` | **29** | `corpus/README.md:12-40` |
| Cells per index row | 3 in all 29 (`Note` / `Holds` / `Sources`) | same |
| Files in `corpus/knowledge/*.md` | **29** | `ls corpus/knowledge` |
| Index-vs-files: missing / extra / duplicate | `[]` / `[]` / `[]` | row basename set vs file basename set |
| Exact unique notes navigated by the coverage table | **29/29** | — |
| `knowledge/<name>.md` string occurrences in README, all sections | 82 | not a note count; counts repeats such as `closeout-r11.md` ×9 |
| Unique note names referenced outside the coverage table | 23 | Province routes and Frontier sections |
| Coverage-only notes (no route or frontier link) | 6: `config-drift-r12`, `executor-test-sufficiency`, `gate-mutation-proof`, `gate-mutation-sweep-r8`, `province-accuracy-selfaudit`, `snapshot-diff-receipt-r9` | `corpus/README.md:12-40` only |
| Markdown links `](...)` in README | all resolve under `corpus/` | per-link `os.path.exists` |
| Backtick `.ufo/...` evidence paths | exist: `configera-host.txt`, `portal-host.txt`, `round-13/w1/globals.json`, `round-14/evidence/source-bindings-pipefail.txt`; globs `drift-*.txt` = 3, `getprop-*.txt` = 2 | repo-root-relative |

Note: a naive scan of backtick `knowledge/...` paths reports them missing, but that is a false positive. Those paths are relative to `corpus/`, and every one resolves there.

Round 15's own "28/28 → 29/29" claim (`corpus/lessons/round-15-verifier-spotcheck.md`) reproduces exactly: 29 notes, 29 indexed, no missing, extra or duplicate.

## 2. Index row convention — three conventions in column 3 (`Sources`)

Rows are not uniform. Each row is still a single line with three cells, so the gate-facing shape holds. The provenance style changes by round:

- **A — plain text, rows 12–19** (MADO-1 … MADO-R3-4). Free-text provenance with backtick paths and no S-ids or links, e.g. `corpus/README.md:19` cites `SKILL.md (sha-pinned per pass…)`.
- **B — self-section link, rows 20–33** (round 4 … round 11). Every cell is `[Source and recheck](knowledge/<same-note>.md): §…`. The link points at the note itself, and no S-ids appear, so these rows cannot be joined to `corpus/SOURCES.md`.
- **C — `source:` S-id form, rows 34–40** (round 12 … round 15). Cell 3 begins with `` `source:` S… `` plus a `[SOURCES](SOURCES.md)` link, evidence paths and a recheck clause. Cell 1 carries `covers: U#` as parenthetical text for rows 34, 35, 36, 38, 39 and 40. Round 12's `config-drift-r12` row (37) is C-shaped but has no `covers`.

Column 1 identifiers use three prefixes: `MADO-n`, `MADO-Rn-k` and `Mn-k`. Rows 38–40 (rounds 13–15) carry only "round N; covers Ux" and no ID. Every note's H1 ID matches its row's column-1 ID (checked for all 29). The one visible wrinkle is row 16, which reads `MADO-4; assignment MADO-R2-2` and matches the H1 `(MADO-4; assignment MADO-R2-2)`.

Ownership: L1 owns `corpus/README.md`. These observations are for L1's integration decision only; nothing here is an edit.

## 3. Note-side markers and cross-checks

- **`covers:` markers.** Exactly six notes carry one, each once, within the first 15 lines: `window-rule-effects-getprop.md` (U1), `hyprland-config-era-r12.md` (U2), `xdg-portal-routing-r12.md` (U3), `wayland-protocol-boundaries-r13.md` (U4), `output-colour-boundaries-r14.md` (U5), `input-debugging-boundaries-r15.md` (U6). Each row-1 `covers U#` text in README matches its note header. No U7 marker exists.
- **Provenance trio** (`source:`, `verified-at:`, `recheck:` in the first 15 lines). Present in exactly 10 notes: the six above plus `arc-synthesis.md`, `closeout-r11.md`, `config-drift-r12.md`, `gate-standing-use.md`. Those four legacy notes have the trio but no `covers:` marker, so no U-credit path exists for them.
- **S-id row/header comparison** for the C-shaped rows. The S-id sets in column 3 equal the note header `source:` sets for `config-drift-r12`, `input-debugging-boundaries-r15`, `output-colour-boundaries-r14`, `wayland-protocol-boundaries-r13`, `window-rule-effects-getprop` and `xdg-portal-routing-r12`.
- **Exception, `hyprland-config-era-r12`.** Row 35 reads `S021–S029 and S017 (S030 rejected duplicate…)`. The header `source:` still lists `S030` (`corpus/knowledge/hyprland-config-era-r12.md:3`). This is deliberate: the note's round-12 and round-13 errata (`:127`, `:132`) map every historical `S030` to `S017`, and the bytes are preserved. Any naive row-vs-header equality check false-fails here. An erratum-aware rule is required.

## 4. How the unique-note count is measured (the counting mechanics)

- The only code in the lane that counts navigation is `.ufo/waves/round-15/measure.py`, lines 237–246. It takes expected names from `git ls-tree -r --name-only REV -- corpus/knowledge`, indexed names from `^\| \`knowledge/([^\`]+\.md)\`` over `corpus/README.md` at `REV`, and reports `notes`, `indexed` (count of expected names with exactly one row), `missing`, `extra` and `duplicates`.
- `tools/mado-verify.sh` contains **no reference to README** (`grep -c README` = 0), so the 29/29 navigation count is **not a gate invariant**. It exists only in the ad hoc measure and in the round-15 closure's manual reproduction. That is the central counting finding.
- The counting logic is fail-closed for the cases that matter: a missing note appears in `missing`, a doubled row appears in `duplicates`, and an unknown row appears in `extra`. Two limits remain:
  1. The regex is anchored at line start. An indented or differently prefixed row is silently not counted. It then surfaces as `missing` only when no other row exists for that note, so the failure is not always visible.
  2. `Path(p).name` compares by basename. Two notes sharing a basename in different subdirectories would collapse to one. The directory is flat today, so this is a latent risk, not a live defect.
- **Covers-scan drift between rounds.** Round 13 searched the whole file (`re.search`, first match only, `\s*$`). Round 14 used whole-file `findall` with `\s*$`. Round 15 searches only the first 15 lines and requires exactly one match (`len(items) == 1`). All three give identical results today because all six markers sit in the first 15 lines. A round-16 measure must pick one scan scope and one tolerance rule and state it.

## 5. Implications for a round-16 U7 note (convention only, not a design)

- Unique-note count moves from 29 to **30** only if the U7 note is added as one new file with one `covers: U7` marker and exactly one new coverage row. A route-table or Frontier-only mention changes the 82-occurrence total but not the unique count.
- The new row should follow convention **C**, carrying `covers U7` in column 1 and S-id-based provenance in column 3, so the unique-note count and reciprocal S-id joins can be checked mechanically.
- Frontier text is also affected. `corpus/README.md` Frontier bullets, plus the Round 15 bullet's "U7 Waybar module text remain open", will need to change when U7 lands. The Province routes row for Waybar (`corpus/README.md:57`) points only at `waybar-walker-plane.md` and `waybar-walker-semantics.md`. The latter is legacy with no `covers:` marker and states module text is `UNK`, so it cannot be credited as U7 coverage.

## 6. Recommendations (for L1 and the round-16 measure owner)

1. Treat the pre-round-16 baseline as **29 rows / 29 files / 29 unique / 82 occurrences**. After any U7 landing, expect 30 / 30 / 30 and re-measure at the new revision.
2. Pick one covers scan scope (first 15 lines, exactly one match) for round-16 `measure.py`, and state it in that file's header.
3. Add an erratum-aware S-id rule before any row-vs-header comparison is gated. The `hyprland-config-era-r12` S030 → S017 mapping must be a documented exception, not a failure.
4. Do not rewrite convention A or B rows. Their provenance is historical and append-only.
5. If the operator wants navigation counting enforced rather than ad hoc, that is a separate gate change. It is not in this round's scope, and I have not proposed the code.

## 7. Limits

- Read-only. Nothing was executed except read-only parsing of lane bytes; no gate, measure, selftest, build, lint or live probe.
- Not checked: whether the tagged S-ids in column 3 are correct in `corpus/SOURCES.md` (other seat), or whether any row's prose claim is true.
- No edits, commits or installs made by this seat. Tool record: none.

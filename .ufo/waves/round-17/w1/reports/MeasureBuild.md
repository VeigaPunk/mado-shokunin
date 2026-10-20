# MeasureBuild — round-17 wave 1 report

Seat: `MadoR17.MeasureBuild` (executor, leaf). Scope: create only
`.ufo/waves/round-17/measure.py` — the revision-bound rubric counter for
the three round-17 declared claims. No other file written; no commits,
no fleet/lane edits outside that path and this report.

## Files changed

- `.ufo/waves/round-17/measure.py` (new, executable, Python stdlib only —
  hashlib/json/pathlib/re/subprocess/sys; `python3 -I` clean, no network,
  no host state).

## Behavior

`python3 .ufo/waves/round-17/measure.py REV`:

- Reads committed bytes **only** via `git -C <lane> show REV:path` and
  `git ls-tree -r --name-only REV -- corpus/knowledge`. Never executes,
  writes, or probes anything in the revision or on the host.
- Prints one JSON object, `schema: mado-measure-r17-v1`, with:
  - `c1 {criteria, lesson_cited, score}` — literal QUALITY.md rubric:
    `^[0-9]+\. ` lines as denominator; `^[0-9]+\. .*lessons/` as cited;
    `score = 10*cited/criteria` (null at zero criteria; QUALITY.md absent
    → 0/0).
  - `c2 {count, score, provinces, rejected, u_routes, u_routes_seen}` —
    declared rubric V over P1..P6. A province is covered by a
    `corpus/knowledge/*.md` entry whose first 15 lines carry a `source:`
    line with an S### token resolving to a SOURCES.md registry row
    (11-column split, `len(cells)==13`) with status `mined`, tier `A`,
    and used-by listing `corpus/knowledge/<entry>` — **and** the entry
    declares the province: new `surface: P<n>` tokens (first 15 lines) or
    legacy map `covers: U1|U2 → P1`, `covers: U7 → P2`. Entries declaring
    `surface:` must contain exact headings `## Upstream contract`,
    `## Host declaration`, `## Safe observation`, `## Unexercised
    behavior` with `[UNK]` in the last section's body (up to next `## `);
    failures land in `rejected` with a reason string. Source-join failure
    on a surface-declaring entry is also rejected with reason. Legacy-map
    coverage also requires the mined tier-A used-by join.
    `score = 10*count/6`; `u_routes` = distinct `covers: U[1-7]` count
    (harm watch).
  - `c3 {tool_present, sha256}` — `tools/mado-tripwire.py` presence at
    REV plus sha256 of the committed blob. Never executed.
- Exit 0 always prints the object (absent items are measured results);
  exit 2 on wrong arity or unresolvable revision.

## Measured runs (own new stdlib script on committed revisions)

Baseline `27cd06f`:

```json
{"c1": {"criteria": 22, "lesson_cited": 14, "score": 6.3636},
 "c2": {"count": 2, "score": 3.3333,
        "covered": ["P1", "P2"], "u_routes": 7, "rejected": []},
 "c3": {"tool_present": false, "sha256": null}}
```

P1 covered by `hyprland-config-era-r12.md` (legacy `covers: U2 → P1`,
S021–S029 mined/A) and `window-rule-effects-getprop.md` (legacy
`covers: U1 → P1`, S002, S016–S020 mined/A). P2 covered by
`waybar-observation-boundaries-r16.md` (legacy `covers: U7 → P2`,
S053/S054 mined/A). P3–P6 uncovered. `u_routes` = 7 (U1–U7 all present).

Pre-registration `0175f13`: identical output — `c1` 14/22 (6.3636), `c2`
2/6 (3.3333) P1+P2, `u_routes` 7, `c3` absent.

Matches the declared expectations (c1 14/22; c2 2/6 with P1, P2). Edge
checks: bad revision → stderr message + exit 2; missing arg → usage +
exit 2. Absent `tools/mado-tripwire.py` → `tool_present: false`,
`sha256: null` (correct at both measured revisions; the tool is a
round-17 C3 deliverable).

## Conformance notes

- `python3 -I` compatibility: no site imports; `REPO` resolved from
  `__file__` parents[3] (`.ufo/waves/round-17/` → lane root), so it runs
  from any cwd.
- Reads only committed bytes; worktree state does not affect output.
- The `git` helper now suppresses stderr only for optional-path probes
  (`try_source`), keeping stdout JSON clean while rev-parse/usage errors
  still surface.

## Host-pause conformance

No pacman/yay/paru (not even `-Q`), no sudo, systemctl, hyprctl, or live
probes run by this seat. No tools installed (stdlib sufficed). Read the
round-16 verifier spot-check lesson as required; it motivated the
`u_routes` harm watch and the literal-rubric wording in `c1`.

## Risks / notes for L1

- `source:` token scan is restricted to lines literally starting
  `source:` within the first 15 lines; a continuation-line citation
  outside a `source:`-prefixed head line is not seen. Literal by design —
  new P4/P6 entries should keep `source:` and `surface:` inside the head.
- `[UNK]` check is presence in the `## Unexercised behavior` body only
  (next `## ` heading ends the section); deeper `###` subsections count
  toward the same section.
- `used_by` splits cell 11 on commas — matches existing rows' comma-
  separated path lists.
- Verification left for L1 post-integration: re-run on the round-17 head
  once the P4/P6 entries and `tools/mado-tripwire.py` land (expect
  `c2.count` 4, `c3.tool_present` true with the integrated blob sha).

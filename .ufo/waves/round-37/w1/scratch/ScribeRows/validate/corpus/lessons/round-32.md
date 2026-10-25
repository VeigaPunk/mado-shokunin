# round-32 — mado lane lesson (assimilation round)

Round: mado 32 (attempt 1, hyaku inline). Lane: `mado-shokunin`. Base: `master`
at `256222890d935212874a09751ff9b7869943c2d7` (round-31 lane tip). Registration
frozen before any data: `.ufo/waves/round-32/registration.md`.

## Gate

Assimilation round — one theme, three candidate entries, five registry rows, from
the READ-ONLY package `/home/vgpnk/Projects/shokuknow/merge/mado/` (campaign
`corpus-expansion-1`). Nothing was written, committed or pushed into that repo,
and no campaign tool was run there (`renumber-staged.py`, `merge-plan.py`,
`quote-lint.py` and `absent-defect-register.py` all write into it — read their
outputs, run nothing).

**Theme: the Hyprland IPC two-socket contract** (the request socket, the event
socket, and the dispatcher surface that is the request-side half of it).

### Re-opened sources (the lane's own access date, 2026-10-24)

Every admitted row was re-opened by the lane itself. Fetched bytes are kept at
`.ufo/waves/round-32/fetch/`.

| row | URL | opened | bytes | sha256 | located quote (≤25 words) |
|---|---|---|---|---|---|
| S186 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/ipc/_index.md | 2026-10-24 | 6,539 | `535bc4c385a06162d3e7e356e1a13853f9c47598787f15c80883c2895d06d1a4` | `:14` "`$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`" |
| S187 | https://wiki.hypr.land/0.56.0/IPC/ | 2026-10-24 | 268,731 | — | rendered `:251` "`EVENT>>DATA\n` ( \n is a linebreak)" |
| S188 | https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c04680a28301ab4b5ee5f94eaff5395efe28dbac/content/configuring/core/dispatchers.md | 2026-10-24 | 12,879 | `c830ce0717f92776f03a977506141c549705aebe4e738ce801faddaa7b2d7d14` | `:8` "Dispatchers return tables that describe an action you want to make." |
| S189 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp | 2026-10-24 | 6,479 | `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` | `:21` `const auto PATH = g_pCompositor->m_instancePath + "/.socket2.sock";` |
| S196 | https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ | 2026-10-24 | 297,863 | `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2` | rendered `:302` "hl.dsp. contains:" |

All five fetched byte lengths and the four sha256 prefixes match the anchors the
package published — the staged anchors are correct on size and digest; their
**line** anchors were not (see "Anchor re-derivation" below).

### Admitted (3)

| entry | rows cited | why it clears the bar |
|---|---|---|
| `corpus/knowledge/ipc-contract-r25.md` | S186, S187, S189 | PROVINCE: the compositor plane the lane owns (`~/.config/hypr/`, hyprctl). QUALITY: every claim carries a located quote; the documented contract is separated from the host's v0.56.2 implementation; explicit unknowns kept ("no socket was connected"). Coverage-map ground the lane did not hold: the lane held no IPC-contract row (r3's note says waybar 0.15.0 has no IPC/query verb; the socket path appeared only incidentally). |
| `corpus/knowledge/dispatcher-semantics-r25.md` | S188 | PROVINCE: the request-side half of the same theme. QUALITY: the "describes, does not act" rule is quoted with its location; the wiki's own instability statement is carried, not smoothed. |
| `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` | S186, S188, S196 | PROVINCE: same theme, the 0.56.x release line the host runs. QUALITY: the page revision is recorded with its date ("Last updated on July 15, 2026"), the dispatcher name list is a count of the fetched text, not a claim of exhaustiveness. |

Rows appended to `corpus/SOURCES.md`: **S186, S187, S188, S189, S196** — and only
those. No row was appended that no admitted entry cites (CORPUS.md rule 4).

### Rejected (1) — reason and flip

| entry | reason | flip |
|---|---|---|
| `corpus/knowledge/two-literature-drift-r26.md` (S195, S198, S199) | **PROVINCE scope + QUALITY bar.** Its subject is *documentation localization* — how the Chinese and Japanese ArchWiki translations lag the English article. mado's province is "the Hyprland/waybar/walker configuration plane and display behavior on this host"; a translation-lag surface teaches nothing about a config plane or a display behaviour, so the material is out of the lane's domain even though the package was built per-lane. Two of its rows are also tier-C `community` (S199 is a CSDN blog post), and tier C is never sole support for an admitted entry (CORPUS.md tier rule). | Flip: if mado's PROVINCE.md claims documentation-localization surfaces (it does not as of round 32), or if a later round's theme is translation drift and every cited row is tier A/B, this entry becomes admissible. |

### Transformation of the staged rows (nothing appended as-is)

Staged rows are campaign-schema. Each of the five was rewritten into the census
11-column schema before append:

- **recheck** — the staged cells carried prose (`on-release — re-pull the file and
  compare sha256 (expect prefix 535bc4c385a06162) (ran 2026-10-23)`); the prose is
  stripped to the cadence `90d` and the stripped text is recorded here.
- **opened** — the staged `2026-10-23` (the campaign's date) is replaced by the
  lane's own access date `2026-10-24`.
- **used-by** — set to exactly the admitted entries that cite the row: S186 →
  `ipc-contract-r25.md`, `dispatcher-surface-and-request-grammar-r26.md`; S187 →
  `ipc-contract-r25.md`; S188 → `dispatcher-semantics-r25.md`,
  `dispatcher-surface-and-request-grammar-r26.md`; S189 → `ipc-contract-r25.md`;
  S196 → `dispatcher-surface-and-request-grammar-r26.md`.
- **no pipe in any cell** — every cell was rewritten where the staged text
  carried a literal `|`; no cell contains a literal or escaped pipe (the census
  requires NF==13 after splitting on `|`).
- **anchor** — the staged line anchors were re-derived against the fetched bytes
  (S186 `:14`/`:19`/`:22`/`:25`/`:30`/`:36-81`; S188 `:8-9`/`:12`/`:14`/`:58`/
  `:59`/`:69`/`:82`; S189 `:14`/`:21`/`:35`/`:126`/`:128`/`:129`; S196 rendered
  `:302`/`:348`/`:414`/`:426`/`:444`/`:459`; S187 rendered `:235`/`:239`/`:248`/
  `:251`).

### Id-collision check (before the first append)

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $PKG/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

Result: **reg-ids=185, staged-ids=132, collisions=0** — the staged set starts at
S186 and the lane registry ends at S185, so no id moved.

**Guard proof (required before this lane's first append under item 10):** on a
scratch fixture carrying an indented row `  | S002 | …`, the 0–3-space extractor
finds `S002` while a column-zero-only extractor finds nothing (fixture
`.ufo/waves/round-32/assimilation/fixture-indented.md`). The guard is therefore
able to catch an indented collision; it was not vacuous.

### Validate-before-append

The append block was built in scratch (`.ufo/waves/round-32/assimilation/`), the
lane's `corpus/` mirrored with the block inserted and the three knowledge files
placed at their repo-relative paths, and the mirror was gated with
`scripts/sources-census.sh validate --file …` before the first append. Result in
the round report.

### Quarantine (payload-absent rows)

The lane's slice of `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
was derived with the prescribed awk filter and hand-checked row by row
(seat report `.ufo/waves/round-32/w1/reports/ExecQuarantineSlice.md`, slice
`.ufo/waves/round-32/assimilation/quarantine-slice`): 13 rows — 6 payload-absent,
7 never-checked. Verdicts: 5 PRESENT/adoptable (S189, S195, S205 verbatim in the
fetched sources; S201 present in the arXiv full LaTeX source, not the abstract
page; S228 present under curly-vs-straight quote normalisation), 1 ABSENT as
quoted (S224, rotating `updated_at`), 7 UNVERIFIABLE prose cells (S199/S200
remote 521 but lane artefacts corroborate; S209/S222/S223/S225/S235 gate
locators checked — S222/S223 verbatim-present, S209/S225/S235 claims hold on
current host state). Register defects named, not edited: a stale `By lane` count
(6 vs 13), a stray backtick in the §2 id cells, and inaccurate "named no locator"
prose. **No quarantined row was appended.**

### considerthese

`considerthese/2026-10-23.md` (operator-authored, read-only — not edited). Its
"proposals only; not acted on" list has seven items; the lane mined exactly one
still-unimplemented proposal — proposal 3, "cross-check one landed tool against a
public pin myself (read-only)" — grounded by re-opening what it points at
(the cited public pins were fetched this round for S186/S188/S189/S196/S187, and
the lane's own r24 `S###.bin` evidence-path convention was adopted for the round's
own fetch receipts). It lands as this lesson's Gate block plus the lane's
`S###.bin` fetch convention, not as a new claim.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| scope | A wave seat wrote outside its declared write scope: `corpus/README.md` was edited (an existing coverage-map row was rewritten to point at a non-existent `knowledge/ghost-mut2b.md`) and `LOG.md` was appended. Both files are lane-owned append-only records and the L1 is the single integration owner. Evidence: `git diff corpus/README.md` at the time of the sweep (row `hyprland-config-plane.md` gained "; see `knowledge/ghost-mut2b.md` for the update") and `git diff --stat LOG.md` (+42). | none | Reverted both files by rewriting them from the branch tip (`git show master:<path> > <path>`, never `git checkout`) and re-applied only the L1's own edits. Fix shown able to fail: the same rewrite restores a 43-row coverage map and a LOG tail without the round-32 quarantine entry; the L1's own appends are then re-applied on top and the diff shows only the L1's bytes. |
| scope | The wave's seat scope was stated in prose only; a seat could read "write a note" as permission to write the lane's own records. | none | The wave context is rewritten (next round) to name the two writable paths per seat explicitly and to forbid any file the seat did not name. Proposed as a QUALITY criterion, not added this round (the round-31 counter's numbers are cited by C2's published axis line). |
| reference-drift | The staged package's **line** anchors are wrong even though its byte-length and sha256 anchors are right: the staged `ipc-contract-r25.md` cites `S186:7-12` for the request socket (the fetched file has it at `:14`), `S186:15` for the freeze note (`:22`) and `S186:18-25` for the event socket (`:25-30`). Evidence: `.ufo/waves/round-32/fetch/S186.bin` versus the staged entry. | QUALITY criterion 41/42 (a claim falsifiable or marked opinion; a claim carries a measured anchor) | Fix: the admitted entries carry the lane's own re-derived anchors, and the staged anchors are recorded here as the defect. Shown able to fail: the staged anchor `S186:7-12` does not contain the string `.socket.sock` in the fetched bytes (`grep -n 'socket.sock' S186.bin` → `:14`, `:25`), while the re-derived anchor does. |
| number-drift | The lane's published axis table (r31, `SCORECARD.md:2014`) states `calibration resolved-active 39/40` and `operability selftest 9/9` while the lane's own instruments at that same tip print `resolved_active=41 active=41` and `12/12 assertions passed`. The published table is a base-state record that was never republished after the round's own commits moved the counters. | QUALITY criterion 22 (a count stated in a SCORECARD/lesson/report claim is re-derived at the measured revision by a cited command) | Fix: the new gate `quality/check-axis-scores.py` re-derives the published fractions and fails when they differ; the round-32 axis line republishes the tip's numbers. Shown able to fail: at the base revision the gate prints `MADO_AXIS: checked=3 mismatched=2` and exits 1; with the perturbation control (`41/41` → `40/41`) it prints `mismatched=1`. |

### Frontier

Moved this round: the IPC two-socket contract and the dispatcher surface moved
from frontier to core as three cited entries and five registry rows. Not moved:
no socket was connected, no event was observed, no dispatcher was dispatched, the
bar's module-text producer route is still open, and the idle/lock chain on this
host is still `[UNK]`.

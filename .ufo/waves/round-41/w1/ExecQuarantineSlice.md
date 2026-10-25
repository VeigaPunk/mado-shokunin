# ExecQuarantineSlice — seat report (w1, round 41)

STATUS: **complete**. Quarantine slice re-derived (13 rows) and the FOCUS-theme rows hand-checked.
No deliverable outside my seat dir plus the two paths the task names; no tracked file edited.

## 1. Slice derivation (item 10)

Command (verbatim from the round-33 prompt, the same awk the task quotes):

```sh
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R" > .ufo/waves/round-41/assimilation/quarantine-slice
```

- Register: 375 lines, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (read-only, unedited).
- **Row count: 13** — 6 `payload-absent` (S189, S195, S201, S205, S224, S228) + 7 prose
  "never checked" rows (S199, S200, S209, S222, S223, S225, S235).
- Output: `assimilation/quarantine-slice`, sha256 `d9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d`.
  Every line carries an S-id: `awk '{ if ($1 !~ /^S[0-9][0-9][0-9]`?$/) print "NO-SID:", NR }'` prints nothing.
- The register's `## By lane` summary (`mado | 6`, line 248) counts only the payload-absent family; the slice is 13.
  The 7 prose rows carry a trailing backtick on the id (`S199\``) because the register's second table is malformed.

## 2. FOCUS-theme id scan → exactly one hit

12 theme files under `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` (list + sha256 in
`assimilation/quarantine-verdicts.md` §2), scanned for the 13 slice ids:

```
S199 focus-control-surfaces-r28.md:69,
```

No other slice id occurs in any theme file. Every other cited id in the theme (`S218, S227, S229, S230, S244,
S273–S275, S278–S280, S288, S293–S296, S306–S308, S313, S314, S317, S323–S325, S328–S332, S338`) is outside the slice.

## 3. Verdicts

| row | verdict | basis |
|---|---|---|
| **S199** (cited `focus-control-surfaces-r28.md:69`) | **`unverifiable`** (prose class "the cited source could not be fetched, so no quote was checked"; not fabrication) **and not a citation of this row** | direct fetch still **521** (2 263 B); the page is readable through `r.jina.ai` (200, 72 136 B), so the class is a fetch artifact. Identity mismatch: the theme's S199 is the arXiv **paper**; the register's `mado round2 S199` is the **CSDN** post `149787804` (packaged S216, `lanes/mado/round2/SOURCES-PROPOSED.md:53`) |
| **S201** (adjacent: same URL cited by the theme under S218/S280/S325; the id itself is not cited) | **`refuse` as cited, re-anchorable** | 2026-10-25: `/abs/2604.18860` → 200 but **0 hits** for both register quotes; `/html/2604.18860v1` → 200, 243 019 B, **both quotes present** (§Introduction; §Conclusion as `— such as notification overlays and X11 window focus hijacking — can redirect agent actions with up to 100% success rates`) |

Totals: cited slice rows 1 → `unverifiable` 1, `adopt` 0, `refuse` 0. The other 12 slice rows are cited by no
theme file. The theme's own quotes of the paper source were also checked (5 quotes, all present; one anchor
error: `compositor-focus-manipulation-literature-r26.md:31` is anchored to `§ Abstract` but exists only in the
full text). Deliverable: `assimilation/quarantine-verdicts.md`.

## 4. Retained evidence (all re-runnable)

- `assimilation/quarantine-slice` (13 lines) and `assimilation/quarantine-verdicts.md` (quote table + receipts).
- Seat dir `w1/ExecQuarantineSlice/`:
  - `verify-quotes.py` — reads the `QUOTE-CHECK|…` lines out of the verdicts file and greps the retained source
    bytes; run `python3 -I verify-quotes.py` → **`QUOTE-CHECK checked=8 failed=0`**, exit 0 (6 present, 2 absent).
  - `sources/arxiv-html-2604.18860.html` sha256 `06c1085529e30c2e6308a898be5cdf1c9e42b02e54faf6cf1163470b192f6aa1`;
    `sources/arxiv-abs-2604.18860.html` sha256 `ab6d25a3d62a0b3638526c39f49e1f8a126b2c858c35b760416039690bebcb18`;
    `sources/csdn-149787804-via-r.jina.ai.txt` sha256 `d9b9ebe8e97279576cf9a4a035cbff90fbc55ea589208a1bf22ad7eea73b603a`.
- Fetch statuses (2026-10-25, this seat): CSDN direct 521 / 2 263 B; CSDN via `r.jina.ai` 200 / 72 136 B;
  arXiv abs 200 / 42 386 B; arXiv html v1 200 / 243 019 B.
- URL-level overlap scan of all 13 slice-row sources against the 12 theme files: only
  `arxiv.org/abs/2604.18860` occurs (3 files); EventManager.cpp, archlinux-cn, wiki api.php, ai-usage/status.json,
  cn-export-hyprland.html and the CSDN URLs occur in none.
- Register read-only throughout; the shokuknow checkout was read, never written. No git/jj command was run.
  No journal, socket, compositor or package command was run (the only network verbs were the four `curl` fetches
  above). No tool installed, none updated.

## 5. Risks / blockers

- **Id-space hazard (attacks `focus-control-surfaces-r28.md:69`):** the staged entry cites the paper as
  "wave-2 row S199"; no numbering consulted puts the paper at S199 (it is S218 in the package, S198 in
  `corpus-expansion-2/ScoutMado.md:26`, S280/S325 in the theme). The L1's C2 entry must not copy that label,
  and must not read the register's `round2 S199` as the paper.
- **Anchor hazard:** the register's `payload-absent` verdict on S201 is correct against `/abs/`; the content is
  real in `/html/`. Any adoption of the paper must anchor to the full text (round-32/round-34 adjudications agree).
- No blocker: the slice is derivable, the hit is decidable, and the only unfetchable source was reached through
  the reader proxy, so its class stands as `unverifiable` rather than `refuse`.

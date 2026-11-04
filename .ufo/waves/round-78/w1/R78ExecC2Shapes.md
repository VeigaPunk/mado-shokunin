# R78ExecC2Shapes — shape-matcher attack on PRED-C2-r78-v1 (round 78, wave 1)

Scope: attack `quality/counters/c2-r78-runbook.py` and its frozen case set; run against the
committed `SKILL.md` at `44a36b64` (anchors 17/17 on every run). No repo edits, no commits.

## Setup (verified)

- Counter copy: `.ufo/waves/round-78/w1/R78ExecC2Shapes/c2-r78-runbook-attack.py`,
  sha256 `b9c774b8883e9972a8975f87b3f0be4e17d9d0967e3f22659d001bab718d743a` — byte-identical
  to the frozen instrument; its selftest passes 34/34 (`receipts/selftest.txt`).
- Case set copy: `c2-runbook-cases-attack.json` — the frozen 17 cases extended in place with
  33 labelled negatives and 11 labelled churn samples (`"attack": "R78ExecC2Shapes"`; case
  count still 17, so the frozen instrument accepts it unmodified).
- Comparator: `shape-diff.py` scores every sample under the r78 rule (`matches`,
  `quality/counters/c2-r78-runbook.py:153`) and a stated naive rule (rc-gated shallowest
  per-kind check; defined in the file docstring).
- Rule lines cited: `empty` :164-165 (`text = stdout.rstrip("\n")` at :154), `int_range`
  :166-171 (validates `text.strip()` at :168, parses `int(text)` at :170), `sorted_unique`
  :172-177 (split never trims), `fields_ok` :137-144 (declared keys only), `case_correct`
  :210-224 (live + samples must match, negatives must not).

## 1. Weak shapes — r78 and naive both accept (37/99; the 6 that matter are negatives)

The r78 rule accepts 6 of my negative samples — a correct rule should reject each:

| # | row (kind) | accepted negative | why (file:line) |
|---|---|---|---|
| 1 | `version` (regex) | rc 0 `Hyprland 0.56.2 not reachable (socket missing)` | `re.search` keeps any line opening with the version token; anchor `^Hyprland [0-9]+\.[0-9]+\.[0-9]+ ` (:159). attack json :23 |
| 2 | `configerrors` (empty) | rc 0 `"\n"` (newline-only) | `rstrip("\n")` at :154 reduces it to `""`; :164 accepts. attack json :66 |
| 3 | `waybar-process` (int_range) | rc 0 `"1720 "` (trailing space) | :168 strips before fullmatch and :170's `int()` tolerates padding anyway. attack json :385 |
| 4 | `clients-count` (int_range) | rc 0 `"\t3"` (tab) | same path (:168/:170). attack json :713 |
| 5 | `workspaces-count` (int_range) | rc 0 `" 7"` (leading space) | same path. attack json :767 |
| 6 | `active-workspace` (json_object_fields) | rc 0 `{"id":1,"name":"1","extra":null}` | `fields_ok` :137-144 constrains only declared keys; undeclared fields are free. attack json :556 |

Case-level effect on the real host: with the extended set these six rows flip to `match=no`
(`receipts/run-extended.txt:1,2,9,13,16,17`), `matched=11/17`, `mutants=5 killed=5`, rc 1
(`:24`). The six flips are exactly the six accepted negatives — the shape matcher, not the
host, is what fails.

Weak-but-expected both-accept churn (shape ≈ naive, no added discrimination): the 3 version /
3 monitors-size / 3 monitors-reserved / 3 omarchy-version churn fixtures, boundary churn
(`4194304`, `1000`), and `" 193"` (padded, binds-count) plus `" walker,wallpaper,waybar"`
(padded CSV entry passes `sorted_unique` — :172-177 never trims parts).

## 2. Over-tight shapes — r78 and naive both reject (48/99)

All 48 sit on the negative role; **zero churn fixture (committed or mine) is rejected by
either rule**, so no plausible next-day output is lost and no over-tightness was proven.
The set is the correct joint rejections: negative pid `-5`, floats-where-int asserted
(`[0,26.5,0,0]`, `3440.0` width), numeric strings (`["0","26","0","0"]`, `{"id":"1"}`),
empty array `[]` / empty object `{}` where an item is required, duplicated list entries,
unexpected JSON types (`"1"`, bare object, `{"DP-1": []}`), rc-0 error text against
exact/empty/anchored rows, and `"custom type: 0 0 0 0 "` trailing-space against `exact`.
Where the rules differ, r78 is the stricter and correct one (13 naive-only accepts:
`[-1,26,0,0]`, `[0,true,0,0]` (bool), unsorted/duplicate CSV, `+193`, `1_000`, float `id`,
partial `levels` dumps; 1 r78-only accept: the committed HDMI `monitors-dump` churn, where
the naive scalar-field check is too shallow for r78's `int4`/`number` schema).

## 3. Churn-clause attack — can a case pass while its live output is wrong?

**Yes — one path proven, one conjecture refuted, same receipt.**
`receipts/run-shim.txt`, frozen case set at `44a36b64`, `PATH` prefixed with a scratch shim
that only replaces `hyprctl` (log: `receipts/hyprctl-shim-log.txt`):

- PROVEN (`run-shim.txt:1`): shim `hyprctl version` exits **0** printing
  `Hyprland 0.56.2 unavailable (compositor gone)` — a broken-tool error line. The `version`
  case still scores correct: live matches the regex, the committed churn sample
  `Hyprland 0.58.0 …` matches, the committed negatives do not. The row certifies the pin
  `SKILL.md:208` ("`hyprctl version` | version pins | `Hyprland 0.56.2`") from output that
  pins nothing. Totals `matched=16/17 control=5/17` (`run-shim.txt:19`); only the
  `clients-count` flip keeps it at TARGET_MISSED.
- REFUTED (`run-shim.txt:16`): shim `hyprctl clients -j` exits 1 with empty stdout →
  `jq 'length'` gets zero inputs and prints **nothing** (rc 0, `out=''`) → `int_range`
  :166-171 refuses the empty string, so the pipeline rc-masking path I conjectured for the
  `clients-count` row (range `[0,100000]`, `controls/c2-runbook-cases-r78.json:478-482`, argv
  `:452`) does not exist.

Residual churn-clause hole = §1's weak-shape set: rc-0 error text shaped like the pinned
value, and whitespace tolerance (a malformed padded count would be scored correct).

## Notes and artifacts

- `run-extended` control drop `5/17 → 4/17` is an artifact of my added churn clobbering the
  held rule's fixed values (`case_correct` :210-224 scores samples under `held_rule` :229
  too), not host drift; the frozen-set shim run still reads `control=5/17`.
- All artifacts under `.ufo/waves/round-78/w1/R78ExecC2Shapes/`: counter copy, extended case
  set, `shape-diff.py`, `receipts/{selftest,shape-diff,run-extended,run-shim,hyprctl-shim-log}.txt`.
- Host posture: read-only probes only (the counter's frozen argv); the shim lived in my
  scratch `PATH` for one run and was removed with the scratch; no `~/.config` or repo writes;
  no git/jj mutation; no tool installs (none needed).

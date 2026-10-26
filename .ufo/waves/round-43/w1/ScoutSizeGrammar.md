# ScoutSizeGrammar report (round 43, w1)
Status: DONE. Full finding: w1/ScoutSizeGrammar/finding.md (pins + sha256 in w1/ScoutSizeGrammar/pins/, quotes checked by verify-quotes.py: 9/9 PASS).
Headline facts (each located in finding.md):
- `size` value = muparser expression pair split at the FIRST whitespace (Expression.cpp:36); constants window_w/h/x/y, monitor_w/h, cursor_x/y only; no percent syntax (muparser 2.3.5 probe: `50%` refused). Host `size` lines are all plain integers; expressions occur only in `move`.
- `float` value = `truthy()`: "1" or case-insensitive prefix true/yes/on; everything else false, no error. Host uses only `float on`.
- Host: 16 size/float lines (7 size, 9 float): the C1 contract reads 9 (size 3, float 6), refuses 7 (4x `match:tag`, 2x extra `match:title`, 1x title-only), and silently mislabels one reversed-order rule (typora.conf:2, `match:class, match:title, float on, center on`) as `other`. Three block-form `windowrule {}` rules are invisible to it (none carry size/float).
- Host regexes: all on size/float lines are inside the contract alphabet; the 4 outside it ([..] classes) sit on non-size/float lines.
- Proposal (not implemented): E1 `match:tag NAME` against the dump `tags` list (NAME or NAME*) => 13/16; +E2 field-order/title conjunction => 16/16 with title-staleness caveat. Round-44+ candidate; frozen C1 contract untouched.
Tools: g++ (existing) compiled a muparser probe against host libmuparser 2.3.5; no installs. No host mutation; read-only `hyprctl clients -j` once. Scratch /fast/scratch/hyaku/mado-r43/ScoutSizeGrammar removed below; /fast/scratch/{tree.json,classify.py,mu...} stray files removed.

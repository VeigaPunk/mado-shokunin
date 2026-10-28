# R55ExecC3CounterB — C3 counter (quality/counters/c3-r55-p19.py draft)

Deliverables (lane-relative): `.ufo/waves/round-55/w1/R55ExecC3CounterB/c3-r55-p19.py`, `.../selftest-output.txt`.
Written from registration.md §C3, claims-frozen.md §C3 and frozen-tables.json `c3` only; no other seat's counter was read. The sealed hold-out was not looked for or seen. No tool installed. Nothing in the lane or fleet was written except these files; scratch `/fast/scratch/hyaku/mado-r55/R55ExecC3CounterB` removed.

## What it does
- Reads only git objects (`git cat-file blob <sha>:<path>`) of `--repo`; `rev` is resolved to a commit first. Base bytes from `3b55b6e9…:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`. git children run with `TMPDIR=<--work>`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_NO_REPLACE_OBJECTS=1`. `--work` is required, created if absent; the counter writes no file itself.
- Embeds `bf46c889…9490`; reads `.ufo/waves/round-55/frozen-tables.json` at rev, refuses (leg `tables_sha`) if its sha differs, and then does not use its contents (rows=0/13, `rows:Q01..Q13`, `pin`, `tables_sha`).
- Prints exactly the frozen `MADO_P19_FIX:` line; exit 0 TARGET_MET / 1 TARGET_MISSED / 2 setup (reason on stderr, stdout empty: bad repo, bad rev, rev starting `-`, missing `--work`, base commit absent, tables unparsable).
- Legs printed in order prefix, rows:Qnn…, pin, p23, readme, tables_sha.
- `--selftest --repo R --rev REV --work W` builds a scratch git repo under W (asserts `rev-parse --show-toplevel` == D, commits with `-c user.name=ctl -c user.email=ctl@ctl`), evaluates 41 variants by exact expected missed-set, then 5 CLI-process checks on the real repo. Core `evaluate()` is shared; only the base commit is parameterised (the real base sha cannot exist in a scratch repo; the selftest's "base" is the first scratch commit holding the real base bytes).

## Run (decisive lines; full text in selftest-output.txt)
`python3 -I c3-r55-p19.py --selftest --repo <lane> --rev 54dacbd8… --work <scratch>` → rc 0, `C3_SELFTEST: 46/46 passed`.
Real repo at the freeze commit (CLI): `rows=0/13 pin=ok p23=bad readme=bad verdict=TARGET_MISSED missed=rows:Q01..Q13,p23,readme`, rc 1 (expected: no block yet).
Frozen controls verified exact: CTL-1 → `rows:Q01..Q13,p23` (prefix clean, readme ok); CTL-2 → `prefix`; CTL-3 → `rows:Q09`; CTL-4 → `rows:Q08..Q12`; CTL-5 → `p23`; CTL-6 → `readme`. Extras all as expected: prefix-with-CRLF (base only, and whole file) → `prefix`; duplicated Q03 → `rows:Q03`; Q07 only inside ``` / ~~~ / HTML comment / 4-space-indented → `rows:Q07`; fenced copy beside a live row → MET; whole block fenced, heading text wrong, heading after rows → all rows + p23; P23 fenced / duplicated / Supersedes P18 / source S372 / wrong anchor / missing words → `p23`; tables tampered or absent → rows+pin+tables_sha; pin tampered/absent → `pin`; entry deleted/truncated → prefix+rows+p23; README absent / P23 on another line → `readme`.

## P23 lexical leg — what junk satisfies it
The leg is six literal, case-sensitive substring tests on the proposition cell (`m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED`, and one of `otherwise`/`any other`/`else`) plus Supersedes==`P19`. The counter, following the frozen text, accepts (selftest cases marked "lexical leg accepts", verdict TARGET_MET):
- `m_passPressed == 1 == 0 PRESSED RELEASED else` (keyword soup, no sentence);
- a **false** sentence: `` `m_passPressed == 1` sends RELEASED; `== 0` sends PRESSED; otherwise it sends nothing at all. `` — wrong semantics, all tokens present;
- `else` matches inside any word (`elsewhere`), `PRESSED` is not required to be near `RELEASED`, and nothing ties the cell to the else-arm sending PRESSED (the actual correction of P19).
So p23=ok proves vocabulary, not truth; the correction's truth rests on the Q-rows (byte-equal to pin lines) and the w2 sentence-to-pin audit. I did not tighten it (frozen text; tightening would be a reinterpretation) — if the L1 wants a stronger leg that is a new frozen predicate, e.g. word-boundary tokens plus an ordered pattern `== 1 … PRESSED`, `== 0 … RELEASED`, `else/otherwise … PRESSED … RELEASED`, still only lexical.

## Ambiguities / choices where the registration is silent (all mine, flag for the L1)
1. Missing heading `Correction (round 55)` has no named leg: I treat Q/P23 rows as counting only if after a live heading containing that text, so a missing heading yields `rows:*` + `p23`. Heading must be an ATX heading line (`#`…).
2. "Live" lines: rows/heading inside fenced code, HTML comments or 4-space-indented blocks are ignored (assignment required fenced; comments/indent are my addition). Fence state is tracked over the whole file, so a prefix leaving a fence open would hide the block — then rows miss.
3. Rows are searched in the whole file (not only after the base prefix); duplicate = >1 live row with that first cell anywhere. Rows are read even when `prefix=changed` (so CTL-2 yields only `prefix`).
4. Q rows must have exactly 3 cells (id | pin:line | `quote`); a Support column would miss. P23 row: ≥6 cells, cell 2 Supersedes `P19`, cell 4 `S371`, cell 5 exactly `Hyprland-ConfigActions.cpp:1554-1576` (a wrong source/anchor makes p23 bad; the registration only names Supersedes and lexical for the leg, but the row shape lists them). A duplicated P23 row → p23 bad.
5. Q cells are compared after whitespace strip; trailing CR on tail lines tolerated (CRLF block with good prefix = MET). The quote cell must be backtick-wrapped.
6. `pin=ok` = pin blob hashes to tables `c3.pin_sha256` AND each frozen quote == stripped pin line (the row text is not compared to the pin; row vs frozen is the `rows` leg).
7. readme leg: any README line (live or not, including fenced) holding the file name and `P23`; literal reading.
8. Registration says the frozen-tables sha is embedded; the pin path/hash come from the verified tables, not hard-coded.
9. `rev=` prints the `--rev` argument as given.
10. `python3 -I` is not enforced by the script.

## Not verified
- Not run by the harness `quality/check-r55-controls.py` (not looked at); no real corpus entry exists yet so TARGET_MET was only seen on the synthetic good tree.
- A leftover unused variable `pre_idx` in selftest (harmless).

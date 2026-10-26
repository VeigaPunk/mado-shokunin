# ScoutSpecs report (mado round 47, w1, 2026-10-26) - status: complete

Seat dir: `.ufo/waves/round-47/w1/ScoutSpecs/` (pins/, sources.md, candidate-rows.md, quotes.py, verify.py, quotes-verified.tsv, probes.py, probes.tsv, sha256sums.txt). Scratch deleted. Nothing outside the seat dir and this file was written; no package, no terminal, no compositor call.

## Answer
- Spec text for xdg-terminal-exec: the repo at v0.14.3 (lightweight tag, commit 065925df9f419008159258ae169018bfd23df71b) has no spec file; the spec is README.md:33-258 and equals terminal-wg/specifications MR !3 `proposals/xdg-terminal-exec.md` at head 64c429dfaf442d4a7ca9a656baf91a1b2d9c1a4d (MR still open, unmerged). Pinned both, plus man page, tests.bats, Makefile, README, script (equals /usr/bin/xdg-terminal-exec), list: all six repo files byte-identical at tag and commit.
- Freedesktop specs have no git tags; versions map to gitrevs in spec-revs.toml. Pinned at: Desktop Entry 1.5 d0589e04172ce640b3fe12694781060cd440a862; Desktop Menu 1.1 7860a2370969f6d0c970c0e9db73e06049d96413; Basedir 0.8 373ecf4423f98384ec299268cc10c53afec418cf; rendered HTML cross-check pages kept.
- 76 located quotes (<=25 words each) verified by script over the pins: `quotes-verified.tsv`, table in sources.md section 3. Covers desktop file ID (subdir '-', first dir wins), key syntax, Hidden, OnlyShowIn/NotShowIn, TryExec, Type, NoDisplay, Actions, Exec quoting and field codes, basedir defaults and relative-path rule, list file names/order/syntax/directives, selection priority, options, print options and order.
- Candidate SOURCES rows S326-S331 (6 rows, 11 columns, tier A; S326 proposal caveat) and rejected/not-opened candidates: `sources.md` sections 2 and 5. S056/S057/S060 already hold README/script/list (hashes re-confirmed equal).

## Findings that change C1 (script is the judge, 22 probes, print mode only, cache in scratch; `probes.tsv`)
1. The script has no Type check (Type absent, Link, Bogus all selected): the draft `explain` rejection reason "wrong Type" must not exist in the tool.
2. NoDisplay is never read; Hidden rejects only the exact string `true` (Hidden=TRUE, Hidden=1 selected).
3. Relative XDG_* dirs are NOT ignored (basedir says ignore); a data dir ending `//` keeps the double slash in printed paths.
4. ID filter: first char [a-zA-Z0-9_] (digit-first accepted), no space, no leading dot (script:773).
5. Category match is case-sensitive; keys before `[Desktop Entry]` are not read; `Key = Value` spacing accepted.
6. Fallback tie order inside one dir: last in readdir order won (one run, P22) - the port must enumerate in the same order and pick the last (script:790 prepends). Unverified across filesystems.
7. `--print-content` exists (man page, S331/Q75) but is absent from the draft contract; no-terminal failure text goes to stderr, outside the stdout+rc contract.
8. Upstream tests.bats lists 24 named cases (S330) usable as fixture seeds; test fixture tree not fetched.

## Gaps
- terminal-intent / intent-apps specs (xdg-specs, merged 2026) and MR !87 were seen as titles only, not opened.
- Prefix-glob key dispatch (`HiddenX=true`) is [INFERENCE] from script:816-938, unprobed.
- P22 is a single observation.

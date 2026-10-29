# R56ExecC3CounterA — C3 counter `c3-r56-used-by.py`

Deliverable: `.ufo/waves/round-56/w1/R56ExecC3CounterA/c3-r56-used-by.py` (sha256 `66f22eeb5d3c26ba1190bfd7820df24d9a6fe7cf454fa2ded40016886af74821`, 0755),
receipts `.ufo/waves/round-56/w1/R56ExecC3CounterA/receipt.txt`. Written from registration §C3 and claims-frozen PRED-C3-r56; nothing edited in the lane except these two paths.

## What it does
`python3 -I c3-r56-used-by.py --repo R --rev REV --work W [--detail]` reads only git objects (`rev-parse`, `ls-tree -z`, `cat-file blob`; git env rebuilt from scratch, HOME/TMPDIR = W, no inherited `GIT_*`), counts `missing`/`extra`/`dangling` per the registration definitions and prints exactly
`MADO_USED_BY: rev=<rev as given> entries=E rows=R missing=m extra=x dangling=d verdict=... missed=<legs|none>`.
Exit 0 only on TARGET_MET, 1 on a miss, 2 on setup (reason on stderr, empty stdout). Legs in `missed` order: `missing,extra,dangling,tables_sha`; every failing leg is listed. `tables_sha`: the blob `.ufo/waves/round-56/frozen-tables.json` at `--rev` must be a regular blob with embedded sha256 `d50d2b7b…f9af` (absent/symlink/other bytes → leg missed; the counts are still printed). `--detail` lists offending pairs on stderr only. `--selftest [--repo --rev] --work W` builds scratch repos under W/selftest-<pid> from the frozen-tables blob (read from `--rev`, sha-checked) plus a generated witness entry, runs the counter as a `python3 -I` child per case, removes the scratch, prints `MADO_USED_BY_SELFTEST: 49/49 assertions passed`.

## Runs (receipt.txt)
```
base 13f0acbe…  : MADO_USED_BY: rev=13f0acbe3a15da2d9c08357a576d91dcadc85273 entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing,tables_sha   rc=1
freeze 3423ae28…: MADO_USED_BY: rev=3423ae28…  entries=70 rows=319 missing=65 extra=0 dangling=0 verdict=TARGET_MISSED missed=missing   rc=1
bad rev         : stderr "setup error: rev does not resolve to a commit at repo", empty stdout, rc=2
selftest        : MADO_USED_BY_SELFTEST: 49/49 assertions passed   rc=0
```
The base line carries the required `entries=70 rows=319 missing=65 extra=0 dangling=0`. `tables_sha` is additionally missed at base only because the tables blob does not exist at the base commit (it is committed in 3423ae28, where the leg holds).

Selftest coverage (49): good tree; missing (dropped used-by, new cite, S0014/xS001 non-tokens, `S001a` token, `~~~` fence, mixed-marker fence, 4-space indent not a fence, unclosed fence, cell-10 path not counted, `S243`-style non-row cite ignored); extra (ghost path, entry without cite, fenced-only cite, duplicate path counted once, subdir path not matched); dangling (`S999`, two pairs, draft id on `source:` line, indented `source:` ignored, `source:` at line 16 ignored); entries accounting (symlink `.md`, subdir, `.txt` excluded; extra entry counted); rows accounting (fenced row counted, `S1000` row, `S12`/4-space-indented not rows); tables_sha (changed bytes, absent, symlink); all four legs together; setup errors rc 2 with empty stdout (10-cell row, 12-cell row, SOURCES.md absent, bad rev, `--all` rev, repo not a dir); worktree ignored (dirtied worktree), `--work` created, rev echoed as given (full sha), `--detail` stdout identical, unknown option rc 2.

## Ambiguities (literal reading taken; registration.md untouched). All measured at base: no variant changes the base counts.
1. Cell split: "split on `|` after stripping the outer pipes" — implemented: strip ASCII whitespace, drop one leading `|`, drop one trailing `|` if present, split on `|`. Alternative: require a trailing pipe (a row without one would be a setup error). No base row lacks one (319/319 start and end with `|`, 11 cells). No backslash-pipe handling (a `\|` in a cell would make 12 cells → setup error); none at base.
2. Registry rows are matched on every line of SOURCES.md, fenced blocks included (registration states no exclusion for the registry; fence exclusion is stated only for CITE). Alternative: skip fenced rows.
3. Fence closing for CITE: closed by the next fence line with the SAME marker (``` vs ~~~); alternative reading "any fence line toggles". Measured: identical CITE sets for all 70 base entries. 4-backtick/longer fences are not length-tracked (a ``` line closes a ````). Fence lines themselves are not "outside". Unclosed fence runs to EOF.
4. HTML comments are not excluded for CITE (C1 excludes them, C3 text does not). Measured: no base entry differs either way.
5. SRC(entry): only lines that start with `source:` at column 0 among the first 15 LF-split lines; continuation lines and indented `source:` do not count; tokens use the same S-token regex as CITE with no fence exclusion. Measured: 22 base entries have a wrapped line after `source:` or several `source:` lines; none has a non-row S-token on a line other than a `source:` line within 15 lines, so no divergence.
6. Duplicate registry ids: one id, USEDBY unioned over its rows (none at base). Pairs are sets, so a path listed twice in a cell counts once.
7. USEDBY regex is unanchored: `x/corpus/knowledge/a.md` and `corpus/knowledge/a.mdx` both yield a path (`…/a.md`); `corpus/knowledge/sub/x.md` yields nothing. An entry whose name falls outside `[A-Za-z0-9_.-]+` could never be listed (none at base).
8. ENTRIES: regular blob, direct child, name ends `.md` with non-empty stem; dotfile names count (none at base).
9. `missed` leg order: `tables_sha` is not named in the registration's `missed=<missing,extra,dangling|none>`; added as the fourth item because the seat spec requires the leg. A harness matching only the three legs sees it only when the tables blob is wrong/absent (absent at base, so the counter's `missed` at base is `missing,tables_sha`, not `missing` — the harness `base-registry` control runs at `--rev` where the tables exist; a control mutating the tree at a rev lacking the tables would see the extra leg). `rows` = number of row lines.
10. SOURCES.md absent/non-regular at `--rev` → setup error (rows undefined); corpus/knowledge absent → entries=0.
11. `--selftest` defaults `--repo .`, `--rev HEAD` when not given; it needs the frozen-tables blob with the embedded sha at that rev (else setup error rc 2).

## Not verified / not run
- No harness (`quality/check-r56-controls.py --claim c3`) exists yet, so the six frozen controls were not run end to end; selftest cases mirror them (dropped used-by ≈ drop-one/base-registry, ghost path, extra/fenced cite, dangling `S999`), but fill-all was not exercised on the real tree.
- Not tested: CRLF registry files, very large repos, `--repo` being a subdirectory or a worktree/shared clone (the counter rejects a subdirectory via `--show-toplevel`; carried from r55).
- No tool installed; no hold-out path seen. Scratch `/fast/scratch/hyaku/mado-r56/R56ExecC3CounterA` removed.

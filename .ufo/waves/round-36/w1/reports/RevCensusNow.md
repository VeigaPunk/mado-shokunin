# RevCensusNow — wave-1 reviewer, mado round 36

## Assignment

Run the fleet census validator against the mado lane, record complete output
and exit code, then compare with the round-35 lesson's `## Gate` before/after
blocks and state whether the row count and the `W04` set are unchanged at
`master`.

## Command run

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

## Complete observed output (verbatim, TSV)

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

**Exit code: 0** (8 output lines: 7 × `W04` + 1 `ok` trailer).

## Row count check

```sh
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md        # worktree
200
$ git show master:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'
200
```

`HEAD` = `master` = `dbf8b579aeac0f023aaf595770f1cb0049e4baa2` (the round-36
freeze commit). `git status --short` shows `corpus/SOURCES.md` unmodified — the
only tracked change in the worktree is ` M PROVINCE.md`; everything else is
untracked round-36 scaffolding (`.ufo/waves/round-36/…`, `quality/counters/`).
So the worktree validator output **is** the output at `master`.

## Byte-exact comparison vs the lesson's after-block

Extracted the lesson's **After** block (`corpus/lessons/round-35.md:50-57`)
into `/tmp/r35-after.txt`, re-ran the validator into `/tmp/r36-now.txt`:

```sh
$ diff /tmp/r35-after.txt /tmp/r36-now.txt
(no output) → IDENTICAL
```

## Findings vs `corpus/lessons/round-35.md` §"Census before → after"

| Item | Lesson before (round-35 start) | Lesson after (round-35 end) | Now, at `master` | Verdict |
|---|---|---|---|---|
| Registry data rows | 192 | 200 | **200** | PASS — unchanged at master vs after |
| `W04` id set | {S030, S042, S045, S097, S119, S120, S121} | same | same | PASS — identical seven ids |
| `W04` detail text | 7 dup-URL lines | same | byte-identical | PASS |
| `mado ok` trailer | present | present | present | PASS |
| Exit code | 0 | 0 | 0 | PASS |

The `W04` set is unchanged not only vs the after-block but also vs the
before-block — round 35 added rows S203–S210 and produced **no new** duplicate
URL warnings, and nothing since has disturbed it. The only quantity that moved
across the recorded history is the row count (192 → 200 inside round 35), and
it has held at 200 through the round-36 freeze.

No `E`-codes, no new warnings, no `missing`/`unlisted` lines. The seven `W04`s
are all pre-existing ids (S030…S121); none touches S203–S210.

## Verdict

**PASS.** At `master` (commit `dbf8b57`, the round-36 freeze): registry row
count = **200**, unchanged from the lesson's after-state; `W04` set =
**{S030, S042, S045, S097, S119, S120, S121}**, byte-identical to both lesson
blocks; exit 0. The gate baseline the round-36 claims build on is intact —
the conformance requirement ("exit 0 with the same seven warnings") holds.

## Commands ledger

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado   # → exit 0, output quoted above
git -C mado-shokunin rev-parse master                                                                     # → dbf8b579aeac0f023aaf595770f1cb0049e4baa2
git -C mado-shokunin status --short                                                                       # → M PROVINCE.md only (tracked); rest untracked round-36
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' mado-shokunin/corpus/SOURCES.md                                  # → 200
git -C mado-shokunin show master:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'             # → 200
diff /tmp/r35-after.txt /tmp/r36-now.txt                                                                  # → identical
```

No tools installed; no files modified outside this report.

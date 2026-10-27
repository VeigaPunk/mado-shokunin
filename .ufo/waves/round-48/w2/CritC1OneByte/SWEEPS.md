# CritC1OneByte — mutation sweeps (round 48, w2)

All runs compare **the real pin** (frozen bytes, executed in the counter's own `bwrap` sandbox through
`ctr.Box`/`ctr.oracle_side`, `XTE_DEBUG=1`, state derived by `ctr.cache_state`) against **the frozen tool**
(`l1-draft/mado-terminal.py`, sha256 `1dfde36c…`) over trees built by `ctr.prepare`. `$ROOT`-normalised
stdout + rc + cache state are compared. Scratch replay repo
`/fast/scratch/hyaku/mado-r48/CritC1OneByte/repo/r48` (own `git init`, `rev-parse --show-toplevel` = that dir,
commit `f89a257b…`, tools/ = draft tool, quality/counters/ = frozen counter + fixtures, pin = frozen bytes).

Reproduction (from `/fast/scratch/hyaku/mado-r48/CritC1OneByte`, harness files `h/*.py` were scratch-only):

```
ulimit -f 4096                       # the frozen Box copies /usr/bin/gawk (1,274,872 B) into scratch
python3 h/fast2.py <fixture[,fixture]> <out.jsonl> <full|key>
python3 h/axes.py 0 204              # 10 structured mutations on every frozen warm case with a cache
python3 h/gate2.py                   # line 2 (cached command) gate: pin hit/stale vs tool cache= state
```

`full` alphabet: substitution of every byte with `{00,0a,0d,1e,1f,20,41,ff}`, deletion of every byte,
insertion of `{0a,1e,1f,20,41}` at every offset, + 9 structured axes.
`key` alphabet: `{00,0a,1e,1f,41}` substitutions, every deletion, `{0a,1f}` insertions, + 9 structured axes.
Structured axes (always first): `axis-term-line50`, `axis-term-line49`, `axis-term-line48`,
`axis-no-final-newline`, `axis-empty-cmdline` (empty line 11), `axis-empty-cmdline2`,
`axis-usep-only` (command = one USEP), `axis-usep-double`, `axis-usep-trail` (USEP before the RS terminator).

## Byte-level sweeps (every cache byte mutated at least once in each)

| fixture | class / args | cache | mode | mutations | rc/stdout/state divergences |
|---|---|---|---|---|---|
| `v2-wd-01-exec-firstword` | WARM-DIFFERS `--print-cmd` | 211 B | full | 2955 | **0** (10 `explain`-parse records, see FINDING) |
| `v2-wd-33-appid-hold` | WARM-DIFFERS `--print-cmd --app-id=A --hold -- top` | 221 B | key | 1766 | 0 |
| `v2-wd-06-argdir` | WARM-DIFFERS `--print-cmd --dir=/srv` | 211 B | key | 1686 | 0 |
| `L1-04-cached-test-mode` | WARM-DIFFERS `--test -- top` | 210 B | key | 1678 | 0 |
| `v2-wd-30-print-id-and-path` | WARM-DIFFERS `--print-id --print-path` | 214 B | key | 1710 | 0 |

Baselines (before mutating) agree, e.g. `v2-wd-01`: pin `((0, 'foot\n--a\n'), 'hit')`,
tool `(0, 'foot\n--a\n')`, `explain cache=hit`.

The 10 `v2-wd-01` records (`receipts/fast2-wd01.jsonl`) are all one class: mutations that put a newline
inside the **first** cached command word (`sub@186..189`, `ins@186..189`, `axis-term-line48/49`) leave
`pin=(0, 'f\not\n--a\n') state=hit` **equal to the tool's stdout** while the tool's `explain` record spans
two lines (`tool_state` unparseable). That is the finding in `FINDING.md`, not a clause w difference.

## Structured axes on every frozen warm case

`receipts/axes-all.log`, `receipts/axes-all.jsonl`: 159 of 204 fixtures materialise a cache; 45 have none
(`no cache`). 1538 axis mutations (10 per cache-bearing fixture; 143 have a command head longer than one
byte) — **0 rc/stdout divergences** (this sweep compared rc/stdout; the pin's state is recorded in each
record and the tool's `explain` record was parsed for the `firstword-newline` axis only). Results for the
named axes, on all 159:

* field 11 RS terminator — `rs-terminator-1f` (0x1e→0x1f) and `rs-terminator-removed`: both sides take the
  cold path with identical stdout/rc; the tool's `read_cache` returns `invalid` when no line ends in the
  terminator, and the byte-level sweep (same substitution at every 0x1e) compared the derived state with no
  difference.
* empty USEP fields — `empty-cmdline`, `empty-cmdline2`, `usep-only`, `usep-trail`: identical stdout/rc
  on both sides across all 159; the byte-level sweeps (which also compare the derived state) include leading,
  doubled and trailing USEP insertions with no state difference (the tool's `split_ifs` reproduces bash
  `IFS=$'\x1f'; set -- $X`; checked separately on 12 vectors).
* line 50 / line 49 — `term-line50` → invalid both; `term-line49` → hit both, with the whole 39-line joined
  command printed; `term-line48` likewise.
* trailing newline — `no-final-newline` → invalid both (pin's `while read` does not see the last
  unterminated line; the tool's `read_lines` drops it).
* `firstword-newline` — clause w agrees on all 159; clause x breaks on **90** of the 143 probes (see FINDING).

## Cached-command gate (line 2)

`receipts/gate2-command-v.txt`: 92 line-2 values (every one-byte deletion/substitution/insertion of `foot`
with `-/.:a 0\`, plus `''`, `--`, `-`, `-p`, `-pv`, `-pV`, `-q`, `-oot`, `-e`, `.`, `..`, builtins,
keywords, script functions, `/bin/sh`, `/bin`, `/tmp`, `bin/foot`, `./bin/foot`, `foot/`, `foo t`, …):
pin-derived state == tool `cache=` state for **all 92** (0 divergences).

## Parser-only differential (superseded by the sandbox sweeps, kept for shape)

`h/fuzz.py` compared the pin's `read_cache` line loop (transcribed) against the tool's `read_cache`
(stubbed `gen_hash`/`command_v`) on 6221 single-byte mutations of two real primed caches:
fields/`exec_usep`/finished-vs-invalid agreed on all 6221. The sandbox sweeps above judge the same question
end-to-end and are the evidence of record.

## Totals

11,333 sandbox mutations (9,795 byte-level + 1,538 structured) and 92 gate values:
**0 rc/stdout divergences; 0 state divergences in the 9,795 byte-level mutations
(state compared whenever stdout agreed); 1 defect class in clause x** (newline inside the cached `exec[0]`).

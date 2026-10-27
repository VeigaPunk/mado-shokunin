# CritC1OneByte — w2 (FALSIFY): one-byte warm-cache mutations of the frozen C1 instrument

Round 48, wave `w2`, policy v1, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; freeze `3e6c848a`.
Target: find a warm cache whose **one-byte** mutation exposes a C1 mismatch; enumerate the frozen warm cases
and mutate each cache line, including the field-11 RS terminator, empty USEP fields, line 50 and the trailing
newline. Write scope: `.ufo/waves/round-48/w2/CritC1OneByte/` + this report only. No lane Git mutation, no
commit, no push, no install, no host change.

## 1. Instruments (identities as attacked)

| item | identity |
|---|---|
| counter | `quality/counters/c1-r48-terminal-cache.py` sha256 `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4` (= `l1-draft/`) |
| fixtures | `quality/counters/c1-r48-fixtures.json` sha256 `4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa`, 204 entries (= `l1-draft/`) |
| pin | `.ufo/waves/round-47/fetch/xdg-terminal-exec` sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` = `/usr/bin/xdg-terminal-exec` |
| tool attacked | `l1-draft/mado-terminal.py` = lane `tools/mado-terminal.py` sha256 `1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92` |
| cold set | `c1-r47-fixtures.json` sha256 `4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86` (unchanged, clause f) |

Scratch replay repo (no lane checkout needed for the counter's `git show`): own `git init` at
`/fast/scratch/hyaku/mado-r48/CritC1OneByte/repo/r48`, `git rev-parse --show-toplevel` asserted equal to it,
commit `f89a257b2f6ade165d21c5542dd0199eaa579070`, containing only `tools/mado-terminal.py` (draft),
`quality/counters/{c1-r48-terminal-cache.py,c1-r48-fixtures.json,c1-r47-fixtures.json}` and
`.ufo/waves/round-47/fetch/xdg-terminal-exec`. All judging reused the counter's own `Box`, `prepare`,
`case_env`, `oracle_side`, `cache_state`, `run_case`, `check_premise`, `explain_case`, `term_line` — same
`bwrap` prefix, same externals, same `--die-with-parent` save waiter.

## 2. Enumeration

`204` warm cases (`ENUMERATION.md` has the full table): `hit` 90, `stale` 47, `absent` 40, `invalid` 17,
`disabled` 5, `-` 5; cache written by the real pin (`prime`) 135, literal cache 25, neither 44;
`default_cache` 3; `HOME` unset 11. `ctr.prepare()` produces an on-disk cache for **159**; 45 have none.
The frozen set already carries the named edges (`M-07` no terminator, `M-08` early terminator, `M-16` line
49, `M-17` line 50, `M-18`/`v2-mf-12` no final newline, `M-09`/`v2-mf-10/11` line limit, `v2-mf-19/20/26/27`
junk/duplicate/append around the terminator, `v2-mf-30` empty cached command, `v2-wi-31`/`v2-mf-25` CRLF,
`v2-wi-26..32` hash/line-2 edits, `L1-01..05` cached id/action/path). The malformed-cache fixtures are
`stale`/`invalid`, so their parser verdict shows mainly as hit-vs-cold; several are hits with edited fields
(`v2-mf-19/22–30`, `L1-01..05`). None of the 204 is a hit whose first command word carries a newline.

## 3. What was mutated and what happened

Full detail in `SWEEPS.md`; counts are exact (`receipts/axes-all.log`, `receipts/fast2-wd01.jsonl`).

* Byte-level sweeps, real pin vs frozen tool, on five frozen warm cases covering `--print-cmd`,
  `--app-id/--hold`, `--dir`, `--test`, `--print-id --print-path`: **9,795** mutations (every byte
  substituted/deleted/inserted at least once on `v2-wd-01`, 211 B, full alphabet; key alphabet on the other
  four) → **0 rc/stdout divergences and 0 state divergences** (the derived cache state was compared
  whenever stdout+rc agreed); baselines agree.
* Structured axes on **all 159** cache-bearing frozen cases (`term-line50/49/48`, `no-final-newline`,
  `empty-cmdline`, `empty-cmdline2`, `rs-terminator-1f`, `rs-terminator-removed`, `usep-only`, `usep-trail`,
  `firstword-newline`): **1,538** mutations → **0 rc/stdout divergences** (this sweep compared rc/stdout
  and parsed the tool's `explain` record for the `firstword-newline` axis; the byte-level sweeps above also
  compare state). Field-11 RS mutations,
  empty/doubled/trailing USEP fields, line 49/50 and the missing final newline all take the same path on both
  sides (invalid→cold, or hit with the identical joined command).
* Line-2 gate (`command -v` vs the tool's `command_v`): 92 values (all one-byte variants of `foot`, plus
  option-like/builtin/keyword/function/path/space names) → 0 state divergences (`receipts/gate2-command-v.txt`).
* Parser-only differential (transcribed pin loop vs tool `read_cache`): 6,221 mutations → 0; superseded by
  the end-to-end sweeps above.

**Clause w is not where the tool is wrong.** Total: 11,333 sandbox mutations — 0 stdout/rc differences
anywhere, and 0 state differences in the 9,795 byte-level mutations (state compared whenever stdout agreed).

## 4. The mismatch found (one byte, warm hit)

A newline inside the **first cached command word** — the value `explain` reports as `cmd=` — makes the
tool's `MADO_TERM:` record span two lines, and frozen clause x cannot parse it. Everything else about the
prediction stays right. `FINDING.md` has the full argument; the exact evidence:

```
frozen warm case v2-wd-01-exec-firstword, cache line 11:
  pristine b'foot\x1f--a\x1eEND_OF_EXEC_USEP'
  mutated  b'f\not\x1f--a\x1eEND_OF_EXEC_USEP'          (byte 1: 0x6f -> 0x0a, same length)
real pin (XTE_DEBUG=1): rc=0 stdout='f\not\n--a\n' state=hit ; cold twin rc=0 'feot\n--a\n' state=absent
frozen tool print     : rc=0 'f\not\n--a\n'            == pin           (clause w ok, variant A and B)
frozen tool explain   : rc=0
  MADO_TERM: selected=foot.desktop path=$ROOT/…/foot.desktop cmd=f
  ot cache=hit verdict=OK
ctr.term_line(record)   -> None
ctr.explain_case(fixture) -> ok=False,
  why="unparseable MADO_TERM line: 'MADO_TERM: selected=foot.desktop path=$ROOT/… cmd=f'"
```

* Reachability on the frozen set: 143 of the 159 cache-bearing cases have a command head longer than one
  byte; this one-byte change keeps the cache a hit and yields an unparseable record on **90** of them
  (all 48 WARM-DIFFERS, 26 WARM-SAME, 12 MALFORMED, 2 HOME-UNSET, 2 H2).
* Why it is not the counter's declared limitation: `term_line` declares only "a value containing a marker of
  a later field"; the pin's own cache format says the command "technically can contain newline characters"
  (`x:245-247`) and the tool's contract is "an existing cache file … reproduced, not corrected". The pin's
  cold path rejects an entry whose first Exec word has a newline (rc 1, "Exec word 'a\nb' not found"), so the
  in-scope source is an edited/stale cache with a matching hash — the same class the frozen set already
  scores (`M-11`, `v2-mf-19/20/22-30`, `L1-01..05`). Multi-line commands the pin *does* write
  (`Exec=foot "a\nb"` → 13-line cache) are safe only because the newline sits in the second word.
* Only `exec[0]` can leak a newline into the record: a newline substituted into header line 1-10 splits that
  line and shifts the fields, so the printed id/path stay single-line (verified: `selected=ot.desktop:…`,
  `path=…/fo:…`, both sides agree).

## 5. Counter verdict

* Frozen set + draft tool: `explained=394/394 … verdict=TARGET_MET` (`.ufo/waves/round-48/receipts/l1-c1-ref-final.txt`,
  rev `0e23d594…`, nonce 4848) — the hole is not covered, i.e. a tool that violates clause x on this in-scope
  cache still passes the frozen set.
* With the added fixture below (and `SHA256_WARM` re-pinned), the counter's own `run_case` gives clause w
  `ok=True` on variants A and B, `check_premise` ok, and `explain_case` gives `ok=False` with the message
  above. `met` (`c1-r48-terminal-cache.py:985-987`) requires `x_ok == total_fx`, so the count would end
  `explained=394/395 … verdict=TARGET_MISSED`, exit 1. I did not execute that full count: one complete count
  exceeds this seat's 300 s per-command ceiling (the frozen receipt is the L1's own complete run). The
  quoted verdict components come from the counter's functions on the frozen bytes.

## 6. Smallest added fixture (`receipts/fixture-W2-CRIT-01.json`, `ctr.check_case` ok)

```json
{"id": "W2-CRIT-01-cached-cmd-newline", "class": "WARM-DIFFERS",
 "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
         "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
         "XDG_CURRENT_DESKTOP": "Hyprland"},
 "files": {"home/.config/hyprland-xdg-terminals.list": "foot.desktop\n",
           "usr/share/applications/foot.desktop":
             "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n"},
 "exec": ["bin/foot"], "args": ["--print-cmd"], "mtime": 1600000000,
 "prime": {"args": ["--print-cmd"]},
 "after": {"cache_lines": {"11": "f\not\u001eEND_OF_EXEC_USEP"}, "mtime": 1600000000},
 "expect": {"rc": 0, "stdout": "f\not\n"},
 "cold":   {"rc": 0, "stdout": "foot\n"},
 "state": "hit"}
```

`after.cache_lines["11"]` is the pin-written line 11 with one byte changed (`o`→LF); `expect`/`cold`/`state`
are the pin's measurements (`receipts/final-W2-CRIT-01.txt`). It is a miss, not an erratum: clause x is not
narrowed. Repair options for the L1's pre-data decision are in `FINDING.md` §7 (escape `explain`'s three
values + un-escape in `term_line`, or explicitly re-register the class).

## 7. Limits, risks, disclosures

* No stdout/rc hole was found: 11,333 mutations, 0 rc/stdout differences (state also compared on the 9,795
  byte-level mutations). The found defect is clause x only (format),
  which means the tool's *prediction* is right and the predicate is unsatisfiable on that cache.
* Alphabet coverage: one full-alphabet byte sweep (`v2-wd-01`) and four key-alphabet sweeps; the structured
  axes cover every cache-bearing fixture, not every byte of every fixture. Byte values that change semantics
  (`0x0a`, `0x1e`, `0x1f`, `0x00`) and the line/terminator positions are covered everywhere.
* Harness disclosure: an early sweep compared normalised pin stdout with raw tool stdout (false positives on
  `--print-path`) and one early axes run ignored `default_cache` (wrong cache path for `W-02`/`W-14`); both
  were caught and re-run clean (`v2-wd-30` 1710 mutations 0 divergences; axes over 204 fixtures 0). The
  artifacts are excluded from `receipts/`.
* The inline parser transcription (`h/fuzz.py`) is scratch-only history; the sandbox sweeps judge the same
  question with the real pin, so nothing in the finding rests on the transcription.
* Related freeze-completeness observation (routed, not my claim): `w1/ExecControlsC1.md` marks 10 of its 20
  controls' draft column `cut` — i.e. `trust-any`, `hash-no-total`, `no-line-limit`, `writes-cache`,
  `mut-desktop-lower`, `mut-no-command-v`, `mut-cache-fallback`, `mut-eof-terminator`,
  `mut-terminator-contains`, `mut-warm-ignores-args` were not scored against the frozen merged set before the
  freeze, although the registration requires "every skip/mutant must miss" before freezing.
* Scratch: `/fast/scratch/hyaku/mado-r48/CritC1OneByte/` (own tree, ≤2 GB; largest file written
  153,295 B during a superseded sweep; the retained receipts are ≤34,522 B). `ulimit -f 2048` (1 MiB) on
  every evidence writer; harness shells used `ulimit -f 4096` (2 MiB) because the frozen `Box` copies
  `/usr/bin/gawk` (1,274,872 B) into its own scratch — no evidence file exceeds 1 MiB. No package manager,
  no install, no host config touch, no GUI/terminal launch, no input injection; no lane write outside this
  seat dir and this report.

## 8. Evidence index (`w2/CritC1OneByte/`)

`ENUMERATION.md`, `SWEEPS.md`, `FINDING.md`,
`receipts/axes-all.jsonl` + `axes-all.log` (all-204 axis sweep + 90 firstword records),
`receipts/fast2-wd01.jsonl` (the 10 explain-parse records),
`receipts/fixture-W2-CRIT-01.json`, `receipts/final-W2-CRIT-01.txt`, `receipts/hole-v2wd01.txt`,
`receipts/realnl-pin-produced-multiline.txt`, `receipts/conf-newline-fields.txt`,
`receipts/gate2-command-v.txt`, `receipts/harness/` (the scratch scripts, verbatim).

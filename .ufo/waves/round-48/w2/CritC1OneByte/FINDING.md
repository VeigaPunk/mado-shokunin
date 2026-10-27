# CritC1OneByte — the one-byte warm-cache defect (round 48, w2)

**Result: a hit cache whose first cached command word (`exec[0]`) contains a newline is unsatisfiable for
frozen clause x.** `explain` prints a two-line `MADO_TERM:` record, the counter's `term_line()` returns
None, and `explain_case` fails. Clause w (stdout/rc/state) is *faithful* on the same cache. The frozen 204
contain no such hit, so the frozen instrument still says `TARGET_MET` for the draft tool. One byte away from
**90** of the 159 cache-bearing frozen warm cases.

## 1. The mutation

Frozen warm case `v2-wd-01-exec-firstword` (WARM-DIFFERS, `--print-cmd`), primed by the real pin:

```
line 11 = b'foot\x1f--a\x1eEND_OF_EXEC_USEP'      (pristine)
line 11 = b'f\not\x1f--a\x1eEND_OF_EXEC_USEP'     (after: byte 1 'o' 0x6f -> 0x0a, length unchanged)
```

`receipts/hole-v2wd01.txt`. The same one-byte change on the smallest possible tree is
`receipts/final-W2-CRIT-01.txt`:

```
primed cache line 11 = b'foot\x1eEND_OF_EXEC_USEP'
after  cache line 11 = b'f\not\x1eEND_OF_EXEC_USEP'   one byte? True
```

## 2. What the real pin does (the judge)

```
oracle warm=(0, 'f\not\n') state='hit'   | cold=(0, 'foot\n') cstate='absent'
```

The pin reads line 11 onwards, joins lines with LF until one ends in `0x1eEND_OF_EXEC_USEP`
(`/usr/bin/xdg-terminal-exec:246-251`), trusts the cache because line 1 hashes and line 2 resolves, and
prints the cached word as-is. Warm differs from cold, so the case has teeth.

## 3. What the frozen tool does

* `print --print-cmd` → `(0, 'f\not\n')` — **identical to the pin**; `run_case` clause w:
  `ok=True` for variant A *and* B, `check_premise` ok, `state='hit'`.
* `explain` → exit 0, record:

```
MADO_TERM: selected=foot.desktop path=$ROOT/usr/share/applications/foot.desktop cmd=f
ot cache=hit verdict=OK
```

  i.e. `cmd=f` + LF + `ot cache=hit …`. `ctr.term_line()` → `None`; `ctr.explain_case()` →
  `ok=False why="unparseable MADO_TERM line: 'MADO_TERM: selected=foot.desktop path=… cmd=f'"`.

The tool's trace says `cache: … actual: foot.desktop …`, so the selection itself is right: this is the
`explain` record format, not the prediction.

## 4. Why this is in scope and not covered

* The cache file is an *input* the tool's contract models: "given the tree, environment and an existing
  cache file, the tool predicts the resolver's stdout and exit status"; a stale-but-valid / edited cache is
  "reproduced, not corrected". The frozen set already contains hand-edited caches (`M-11`, `v2-mf-19/20/22-30`,
  `L1-01..05`).
* The pin's cache format explicitly permits newlines in the command (`x:245-247`: "technically it can contain
  newline characters"), and the pin's own writer produces them: priming `Exec=foot "a\nb"` writes a 13-line
  cache whose command is `foot\x1fa\nb` (`receipts/realnl-pin-produced-multiline.txt`, pin `(0,'foot\na\nb\n')`,
  tool `print` identical). That case is safe for `explain` only because the newline is in the *second* word;
  `explain` reports `exec[0]`.
* A newline in `exec[0]` cannot come from the pin's cold path (an entry `Exec="a\nb" x` is rejected:
  `rc=1`, "Exec word 'a\nb' not found", `receipts/conf-newline-fields.txt`), so the reachable source is an
  existing/edited cache with a matching hash and a resolving line 2 — exactly the class the counter already
  treats as in scope.
* No frozen fixture is a hit with a newline in `exec[0]`. The multi-line-command fixtures (`M-14`, `M-16`,
  `M-17`, `v2-mf-04`, `v2-mf-11`) all carry a `000…0` hash, so their state is `stale`/`invalid` and
  `explain` prints `cmd=-`.
* The counter's declared limitation is narrower than this: "A value containing a marker of a later field is
  outside what this parser can read; declared, not scored." A newline is not a later-field marker.

Reachability measured on the frozen set (`receipts/axes-all.jsonl`, `firstword-newline` records):
143 of the 159 cache-bearing cases have a command head longer than one byte; mutating byte 1 of that head to
LF keeps the cache a hit and yields an unparseable `explain` on **90** of them (all 48 WARM-DIFFERS,
26 WARM-SAME, 12 MALFORMED, 2 HOME-UNSET, 2 H2); the other 53 become stale/invalid (`cmd=-`, parseable).

Other single-byte positions do not reproduce it: a newline substituted into a header line 1-10 *splits the
line and shifts the fields*, so the printed ids/paths stay single-line
(`receipts/conf-newline-fields.txt`: `selected=ot.desktop:foot.desktop path=…/fo:foot.desktop`, state hit,
clause w and x agree). `exec[0]` is the only value that can carry an embedded newline into the record.

## 5. Counter verdict

* Frozen set, draft tool: `TARGET_MET`. `.ufo/waves/round-48/receipts/l1-c1-ref-final.txt`:
  `PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok
  tool=present verdict=TARGET_MET` (rev `0e23d594…`, nonce 4848) — the set does not cover the hole.
* With the fixture in §6 added (and `SHA256_WARM` re-pinned), the counter's own functions give
  `run_case` clause w `ok=True` (variants A and B), `check_premise` ok, `explain_case` clause x `ok=False`
  with the message quoted in §3. The counter's `met` predicate (`c1-r48-terminal-cache.py:985-987`)
  requires `x_ok == total_fx`, so the run ends `explained=394/395 … verdict=TARGET_MISSED`, exit 1.

I did not execute the full count with the fixture appended: one complete count exceeds the 300 s
per-command ceiling of this seat (the frozen receipt above is the L1's own complete run). The clauses quoted
are produced by the counter's `run_case` / `check_premise` / `explain_case` / `term_line` themselves, on the
frozen bytes, in the counter's sandbox.

## 6. Smallest added fixture

`receipts/fixture-W2-CRIT-01.json` (schema v2, `ctr.check_case` ok). Minimal prime + a one-line cache edit:

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

The `after.cache_lines` value is the primed line 11 with one byte changed (`o` → LF); `expect`/`cold`/`state`
are the pin's own measurements. Any 90 of the frozen warm cases would also do; this is the smallest.

## 7. Suggested repair (L1 decides, pre-data)

Neither clause may be narrowed after data. Before data, either

* keep clause x and make the pair agree: escape the three `explain` values (e.g. `\n`/`\r`/`\\` in
  `selected=`, `path=`, `cmd=`) and un-escape them in `term_line()`; the counter's oracle side already has the
  raw value, so only the tool and the parser change; or
* move this class to the tools' declared out-of-contract *set* explicitly (docstring + a negative fixture that
  asserts the tool's stated behaviour) — but that changes the contract and needs re-registration, not a
  quiet parser tweak.

The other 39 clause-x values and every clause-w value stay as measured: this is a single missing case, not a
broad failure.

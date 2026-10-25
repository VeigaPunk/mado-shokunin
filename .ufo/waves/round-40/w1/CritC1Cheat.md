# CritC1Cheat — the cheapest cheat for C1 (PRED-C1-r40-v1)

Verdict: **the counter is wrong.** A 204-line tool that implements **no conversion of its own**
scores `fixtures=13/13 verdict=TARGET_MET`, exit 0, at both the freeze commit and the tip. It
labels every row by `exec`-ing the counter's own reference model out of
`quality/counters/c1-r40-live.py`, and its `--selftest` is a constant string. Two further holes
are independent of that one: clause b is text-only, and the "exactly one `getopt -j KEY`" audit is
forgeable by the tool.

Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scored revs: `e2b51d3b3f79768282914d57c1fa32cc85dcb06a` (tip) and
`5e7e88525cc539563de7746361b2650802e81809` (freeze). Base `9fc511d…` unchanged.
All cheats and receipts are in `.ufo/waves/round-40/w1/CritC1Cheat/`. No tracked file edited, no
compositor verb except read-only `hyprctl getoption -j`, no package transaction.

## 1. The winning cheat (zero conversion)

`cheat-c-leak-min.py` (204 lines): 15-line block parser for `$HOME/.config/hypr/hyprland.conf`,
one `[prog, "getoption", "-j", KEY]` per declared key plus probes, `no such option` → `config-only`,
then for every remaining row

```
ns = judge()          # execs quality/counters/c1-r40-live.py with __name__ != "__main__"
model = ns["model_equal"]; ... equal = ns["gradient_text"](declared, inherited_angle)
```

`grep -n "0x1000000\|WEIGHTS\|def hl_int\|def gradient_text\|def gap_text\|round(float"` over all
three leak cheats → **none**: there is no `hl_int`, no gradient/gap/weight table, no float rounding
in the cheat. The only conversion-shaped code is a shape guess (`deg` → gradient, 1 int → weight,
n ints → gap) and reading the earlier declarer's `Ndeg` token for inheritance — both are pure text
lookups, and the angle *comparison* is done by the judge's `gradient_text`.

Locating the judge (both routes tested, both pass):
- `/proc/<ppid>/cmdline` + `/proc/<ppid>/cwd` → the counter path (works because the counter spawns
  the tool; the tool is copied to `/tmp`, so `__file__` is useless). Verified path-agnostic:
  `cheat-c-proc-only.py` has `JUDGE = "/nonexistent/judge.py"` and still scores 13/13, including a
  run from `cwd=/tmp` with an absolute counter path.
- hardcoded lane path fallback (`cheat-c-static-only.py`) → 13/13.

Receipts (verbatim final lines):

```
cheat-c-leak-min.score.txt        PRED-C1-r40-v1 clauses=a:1 b:1 g:1 k:1
                                  fixtures=13/13 tool=present verdict=TARGET_MET rev=e2b51d3b… (exit 0)
cheat-c-freeze-rev.score.txt      fixtures=13/13 … verdict=TARGET_MET rev=5e7e8852… (exit 0)
cheat-c-proc-only.score.txt       fixtures=13/13 … verdict=TARGET_MET (exit 0)
cheat-c-static-only.score.txt     fixtures=13/13 … verdict=TARGET_MET (exit 0)
cheat-c-baseparser.score.txt      fixtures=13/13 … verdict=TARGET_MET, clause=b selftest=79/79 (exit 0)
```

`cheat-c-leak.py` is the same cheat on the *base tool's* real parser (1050-line base + ~130 lines):
it also scores 13/13, and on the live host it reproduces the reference model exactly —

```
$ python3 -I .ufo/waves/round-40/c1/ctl-ref-tool.py.txt --home "$HOME" --live   # control, never delivered
$ python3 -I …/CritC1Cheat/cheat-c-leak.py            --home "$HOME" --live
host-ref   rows=70 {'agreement': 62, 'agreement*': 8}
host-cheat rows=70 {'agreement': 62, 'agreement*': 8}
same keys: True  same labels: True
```

So the registration's declared out-of-distribution mitigation ("the live host receipt (70/70 under
the reference model) is the out-of-distribution check and is reported, not scored") **cannot
separate a borrowed model from a real one** — it is the same model. It is not scored, so it was
never able to rescue the predicate.

## 2. Attempts and where each tripped

| # | Cheat | Idea | Score | Tripped on |
|---|-------|------|-------|------------|
| A | `cheat-a-echo.py` (1125 l) | base tool + `--live/--hyprctl/--probe`, labels from base `values_equal` + `set` + declarer count; no form conversion | 0/13, b:0, exit 1 | every `agree` key whose value needs a form conversion: colour (`0x…`/`rgb()`/`rgba()` → ARGB), gradient (incl. inherited angle), gap expansion, font-weight name. bool/num/float/str agree keys and all differ/unset/absent labels were already right. Each gen fixture has ≥1 such key, so no fixture survives. |
| B | `cheat-b-selftest.py` (9 l) | print `MADO_OPTIONS_SELFTEST: 79/79 passed`, exit 0 | fixtures 0/13 but **clause b:1** | nothing — clause b is `re.search` + returncode only; a 9-line file satisfies it. |
| C | `cheat-c-*` (above) | borrow the judge | **13/13 TARGET_MET** | nothing. |
| D | `cheat-d-forge.py` (229 l) | never run the compositor: read the stub's `table.json` + `mode`, write `calls.log` with one `["getoption","-j",KEY]` line per key | **13/13 TARGET_MET**, exit 0 | nothing. The stub dir is writable by the tool (same uid), so `check_live`'s argv audit is not evidence. |
| E | per-REV memo of conversion outputs | replay recorded rows keyed by config content | not built | not needed: the declared residual already admits hardcoded tables, and C is strictly cheaper (no table, no REV knowledge, works at any rev). |

Attempt A is the honest answer to "can a tool pass without converting?" — **no**, the *values* must
be converted. What is not required is that *the tool* converts them.

## 3. Impacted axes

- **operability (C1)** — the capability being claimed ("the option table merges the running
  compositor … converted per hyprlang/Hyprland handlers") is not demonstrated by the predicate: the
  delivered tool may contain zero conversion and still be `TARGET_MET`. The docstring's closing
  claim "Because the trees, values and perturbations derive from REV, a tool that replays recorded
  output cannot pass; it has to convert and compare" is false: it must *compare*, not convert.
- Not impacted: navigation, calibration (no file shared), and C2 (separability holds — C2 reads
  entry/registry/receipt bytes and the tool sha; this cheat touches neither).

## 4. Smallest safe corrections (each is a new predicate — the counter is frozen)

1. **Clause g, extended to an access clause (g2) — this is the one to repair.** Today g is an
   *import* allowlist (`ast.Import/ImportFrom`), so `exec`/`compile`/`open` are invisible. Minimal
   addition to `imports_ok`-style scanning of the tool source:
   - reject `Call` whose `func` is `Name` in `{"exec","eval","compile","__import__"}` and any
     `importlib`/`runpy`/`ctypes` use;
   - reject any string `Constant` containing `"/proc"`, `"c1-r40"` or `"quality/counters"`;
   - reject `os.getppid`/`os.readlink` on `/proc`.
   This kills C's three variants in one shot (all three name `c1-r40-live.py` or read `/proc`). It
   is a denylist, so it raises the price rather than closing the hole: the sound form is a
   boundary — run the tool (already copied to a temp dir) inside `unshare -rm`/`bwrap` with only
   the temp tree and the `--hyprctl` path visible. That is cheap on this host but changes the
   counter's environment contract, so it belongs in a new predicate, not a silent edit.
2. **Clause b must be bound to behaviour, not to a line of text.** A constant print or 8 padded
   `_check(…, True)` calls satisfy it (both demonstrated: `cheat-b-selftest.py`, `cheat-c-leak.py`).
   Smallest fix: mutate the tool source 3× (e.g. `0x1000000` → `0x100000` in the `rgba` branch,
   drop the `deg` inheritance, `"%ddeg"` → `"%d deg"`, reverse the 3-value gap expansion) and require
   each mutated copy's `--selftest` to exit non-zero (or report `k < n`). ~15 lines, no new deps,
   and it makes the mutant harness's own logic guard the selftest.
3. **Drop or demote the argv/once claim.** `calls.log` lives in the stub directory, which the tool
   can write (it is the stub's parent process and the same uid); `check_live` reads it *after* the
   run. Cheat D shows a tool that never invokes `hyprctl` at all. Same-uid evidence from a
   tool-controlled directory cannot support the sentence "runs exactly `HYPRCTL getoption -j KEY`,
   once, and nothing else". Either delete that assertion and the docstring sentence, or print the
   call log as a diagnostic only. A sound replacement needs a privilege/namespace boundary.
4. **Widen the declared residual.** As written it covers "hardcodes the reference model's tables";
   the actual cheapest route is *obtaining* the model at run time from the judge (or from any file
   in the repo). Any residual wording that implies memorisation is the expensive variant of the same
   hole mis-states the risk.
5. **The 18 controls are blind to this class.** `receipts/ctl-c1.txt` lists 16 one-defect mutants of
   the reference tool plus BASE and the reference control — all honest implementations. Nothing in
   `ctl/run-c1-controls.py` models "reads the judge" or "forges the audit log"
   (`grep -n "judge\|exec\|leak\|calls.log"` → only the harness's own `subprocess.run`). So
   `CTL_C1: controls=18 correct=18/18` is evidence about defect detection, not about cheat
   resistance; the leak mutant and the log-forging mutant must be added, and the reference control
   must be expected to fail them.

## 5. What was not done

No delivery, no integration, no edit of a tracked file, no mutation of any config tree, service or
compositor state. No subagents, no background jobs. No tool installs: the only interpreter used is
the host's `python3 -V` → `Python 3.14.8`; nothing was added to the host.

## Evidence index

| Path | Content |
|---|---|
| `cheat-a-echo.py` / `.score.txt` | no-conversion echo cheat, 0/13, b:0 |
| `cheat-b-selftest.py` / `.score.txt` | 9-line fake selftest, clause b:1 |
| `cheat-c-leak-min.py` / `.score.txt` | cheapest passing cheat, 13/13, exit 0 |
| `cheat-c-proc-only.py` / `.score.txt` | judge found via `/proc` only (`JUDGE` nonexistent), 13/13 |
| `cheat-c-static-only.py` / `.score.txt` | judge found via hardcoded lane path, 13/13 |
| `cheat-c-leak.py` / `cheat-c-baseparser.score.txt` | same cheat on the base tool's real parser, 13/13 |
| `cheat-c-freeze-rev.score.txt` | 13/13 at the freeze commit |
| `cheat-d-forge.py` / `.score.txt` | never runs `hyprctl`, forges `calls.log`, 13/13 |
| `host-ref.json`, `host-cheat.json` | live host: identical 70 rows, 62 agreement / 8 agreement* |

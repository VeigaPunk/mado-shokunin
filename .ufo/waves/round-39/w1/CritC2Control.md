# CritC2Control — C2 counter attack report (mado round 39, w1)

Role: UFO-FSD critic. Target: C2 (operability, capability acquisition) counter
`quality/counters/c3-r39-options.py` (PRED-C3-r39-v1). Attack: cheapest stub.

## Verdict: CRITICAL FINDING (before data)

The C2 counter is broken in three independent ways. (1) It **cannot
discriminate a hardcoding stub from the real tool** — under the runner the
counter's own docstring describes, the stub passes every content clause (b,c,d,e,g)
and would yield `TARGET_MET`; the *real* tool currently fails clause b. (2) As
frozen, it **cannot reach TARGET_MET for any implementation**: clause f is
self-contradictory and the real fixture cannot run in the counter's sandbox. (3) The
genuine tool currently fails its own claim's counter (clause b format mismatch).

## Setup (scratch, outside lane)

- Scratch git repos (identical structure to lane): `/tmp/critc2/real`, `/tmp/critc2/stub`.
- Base commit (identical `f49a96f3edfbc461331c8d054927133be8aea4f6`): real counter
  `quality/counters/c3-r39-options.py` + . fixture
  `.ufo/waves/round-39/w1/ExecOptionsFixtures/` (run-fixtures.sh, expected.json, trees/); NO tool.
- Data commits: `real` → genuine `tools/mado-options.py` (`afd3c8494fe95434fb1b7b0d4764a2e4c16064c7`);
  `stub` → 40-line hardcoding stub (`1c4b823efbdd06c25c9380cf12e4a8832344de76`).
- Counter run verbatim: `python3 -I quality/counters/c3-r39-options.py --repo <repo> --rev <rev> --base <base>`.

## Run A — canonical (real tool, real fixture, real counter)

```
clause=b selftest_rc=0 assertions=0 ok=0
clause=c fixtures=0/4 rc=1 ok=0
clause=d row_shape=0
clause=e strict_named_refusal=1
clauses=b:0 c:0 a:1 d:0 e:1 f:0 g:1
verdict=TARGET_MISSED rev=afd3c8...  (exit 1)
```

Counter sandbox fixture reproduction (`/bin/sh run-fixtures.sh --tool <sandbox tool> --repo <repo>`
in a tempdir replicating `TemporaryDirectory(prefix="mado-c3-r39-")`, i.e. under `/tmp`):
```
FAIL fixture1 tool-missing: //tools/mado-options.py
FAIL fixture2 run rc=2   python3: can't open file '//tools/mado-options.py'
mkfifo: cannot create fifo '/tmp/mado-c3-r39-l5pcib/trees/fifo-home/.config/hypr/pipe.conf'
FAIL fixture3 fifo refusal unnamed (rc=2)
FAIL fixture4 dangling refusal unnamed (rc=2)
fixtures=0/4
```

### Root causes (each independently fatal)

1. **Fixture ignores `--tool`/`--repo`.** `run-fixtures.sh` sets
   `TOOL="$LANE/tools/mado-options.py"`, `LANE="$(cd "$HERE/../../../../.." && pwd)"`.
   In the counter's sandbox `HERE=/tmp/mado-c3-r39-XXXXXX` → `LANE=/` →
   `TOOL=//tools/mado-options.py` (does not exist). The sandbox tool copy is never executed.
2. **Fixture resources missing in sandbox.** The counter extracts only the single fixture blob;
   `trees/` (main-home, fifo-home, dangling-home) and `expected.json` live next to it in the repo,
   not in the sandbox. `mkfifo`/`ln` fail; `cmp_rows` would fail on missing `expected.json`.
3. **Clause d marker never emitted.** The counter parses `MADO_OPTIONS_ROWS: <json>` from fixture
   stdout; `run-fixtures.sh` never prints any such line → `row_shape=0` always.
4. **Clause b format mismatch.** Counter regex `(\d+)\s*/\s*(\d+)\s+assertions?`;
   real tool prints `MADO_OPTIONS_SELFTEST: 69/69 passed` (rc=0, 69/69) → `assertions=0` → b=0.
5. **Clause f is self-contradictory.** `clauses["f"] = int(not tool_present)`; `met = all(clauses.values())`.
   When the tool is present (a=1) f=0 → `all()` false → verdict can NEVER be `TARGET_MET`,
   even with a perfect tool and perfect fixture. C2 target is unreachable by construction.

## Run B — stub under the runner the counter's own docstring specifies

Replaced only the fixture's *plumbing* (no semantic change): honor `--tool`/`--repo`, stage
`trees/`+`expected.json` from the repo, emit the documented `MADO_OPTIONS_ROWS` marker.
`cmp_rows` and all four fixture bodies byte-identical (diff confined to two insertions).

Stub behavior (no parsing; hardcodes fixture outputs):
- `--selftest` → prints `MADO_OPTIONS_SELFTEST: 69/69 assertions`, exit 0;
- `--home` (no `--getoption`) → dumps the 14 hardcoded rows identical to `expected.json[static]`;
- `--home --getoption FILE` → dumps `expected.json[getoption]` rows (incl. `agreement` fields);
- non-regular file under `--home` → refuses with filename in diagnostic, exit 3
  (covers FIFO `pipe.conf`, dangling `gone.conf`, and the counter's own `hyprland.conf` FIFO);
- imports: argparse/json/os/stat/sys (stdlib-only).

Result:
```
REAL tool + fixed runner: b:0 c:1 a:1 d:1 e:1 f:0 g:1 → MISSED (only b fails)
STUB  + fixed runner:     b:1 c:1 a:1 d:1 e:1 f:0 g:1 → clauses b,c,d,e,g ALL PASS;
      with f corrected to its intended post-precondition semantics (f:=1) → TARGET_MET.
```

The stub satisfies every substantive check (b, c, d, e, g) exactly as well as the real tool —
and better (b) — while performing zero parsing. The fixture compares only against static
`expected.json`; nothing verifies the tool derived its rows from the input tree.

## Impacted axes

- **operability (C2)** — predicate spoofable; counter cannot validate the deliverable.
- No impact on C1/C3 assessed (out of scope).

## Smallest safe correction (for integrator, before data commit)

1. Fix clause f (use the precondition check only, or `f:=1` post-precondition).
2. Make the fixture execute the sandbox copy: honor `--tool`; stage `trees/`+`expected.json`
   from repo blobs; emit the `MADO_OPTIONS_ROWS` marker.
3. Align clause b regex with the tool's actual selftest line (or make the tool print `N/N assertions`).
4. Add a behavioral-delta fixture: mutate a tree between runs (e.g. delete a `key = value` line or
   change `live.json`) and require the tool's output to change accordingly — a hardcoding stub
   cannot pass without reading the tree. This is the minimal semantic check that closes the stub hole.

No tools installed (stdlib only); no lane files written except this report; scratch kept in `/tmp/critc2`.

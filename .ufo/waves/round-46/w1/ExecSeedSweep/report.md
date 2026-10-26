# ExecSeedSweep — determinism and nonce independence of PRED-C1-r46

Seat `ExecSeedSweep` (leaf). Round 46, wave w1, lane `mado-shokunin`. Nothing in the lane was edited;
the counter, fixtures, reference, receipts and registry were read only. All writes are under
`.ufo/waves/round-46/w1/ExecSeedSweep/` (this seat dir) plus the trailer
`.ufo/waves/round-46/w1/ExecSeedSweep.md`.

## Headline

| question | answer |
|---|---|
| nonces 1..120, `PYTHONHASHSEED` unset | **120/120 `TARGET_MET`**, exit 0 |
| nonce 46 × `PYTHONHASHSEED` 0 / 1 / random, plus 4 extra repeats, 2 serial runs and the first timing run | **11/11 `TARGET_MET`**, all logs **byte-identical** (`sha256 d3fbd7305c09…`) |
| supplementary nonces 121..400 and extremes `0, -1, 2³²−1, 2⁶³−1, 10¹⁸` | **285/285 `TARGET_MET`** |
| total scored runs | **412** (`127` + `285`), **0 non-MET** |
| `names()` forbidden characters | none: universe alphabet is `[+0-9a-z-]` (no `[`, `]`, `$`, `#`, `=`, no uppercase, no whitespace/comma) |
| time per run | **8.3–9.2 s** serial (idle host); 12.0–18.7 s with 12 counters concurrent |
| wall time of the whole sweep | 127 runs in **168 s**; 285 runs in **350 s** (12-way) |

**Non-MET set: empty.** No nonce, hash seed, repeat or extreme value produced a failing fixture or a
failing generated case, so there is no failing label to record. The three candidate mechanisms named in
the assignment are each ruled out below with a measurement, not an argument.

## Setup (scratch only; lane untouched)

- Reference installed byte-identically as `tools/mado-devices.py` in a scratch clone of the freeze:

```
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r46/ExecSeedSweep)   # -> .../ExecSeedSweep/clone
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
cp <lane>/.ufo/waves/round-46/l1-draft/mado-devices.py "$D/tools/mado-devices.py"
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m "seat: install reference"
# -> 30f2e2792d49ea6bcfa24ac2706e3e708d7d0fa5, blob mode 100755
```

- Byte provenance (identical at freeze, at lane HEAD and on disk, verified with `git show … | sha256sum`):

| file | sha256 |
|---|---|
| `quality/counters/c1-r46-devices.py` | `dfeaa4401430ddc2d68711b8dd30b1f470fe1d74b6d1f39477172a30d2fc850a` |
| `quality/counters/c1-r46-fixtures.json` | `027ed50877b345e34b27e38b4a865be4b23f94c0cc0067ac42265ca1778e3fc1` (= pinned `FIXTURES_SHA256`) |
| `.ufo/waves/round-46/l1-draft/mado-devices.py` | `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` (= pinned `MODEL_SHA256`) |
| `tools/mado-devices.py` in the scored clone | `b229efd0…a33b` (same bytes) |

All three frozen files were re-hashed at the freeze commit, at the lane HEAD present while this seat ran
(`e0be61e4f6e34896f8b1c329f9c6d129e5af81f7`) and on disk: identical everywhere, so the counter driven here
is the frozen one and no integrator edit changed the harness under the sweep.

- Counting command per run (one work dir per run, always under the seat scratch):

```
python3 -I /…/mado-shokunin/quality/counters/c1-r46-devices.py \
  --repo /…/ExecSeedSweep/clone --rev HEAD --work /…/ExecSeedSweep/work/<label> --nonce=<N>
```

- The scored revision is `30f2e2792d49ea6bcfa24ac2706e3e708d7d0fa5`; every run prints
  `rev=30f2e27…` and `fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present
  verdict=TARGET_MET` (see `evidence/runs-block1.txt`, `evidence/runs-block2.txt`).

## 1. Nonce sweep, block 1 — the assignment's set (127 runs, 168 s)

`evidence/runs-block1.txt` (130 lines = header + 127 result lines). Every line is `rc=0` and
`verdict=TARGET_MET`, covering:

- `n001`..`n120`: nonces 1..120, `PYTHONHASHSEED` unset, `seeds=46,<N>`.
- `n046-hs0`, `n046-hs1`, `n046-hsrandom`: nonce 46 under `PYTHONHASHSEED=0`, `=1`, and unset (random
  per-process seed).
- `n046`, `n046-rep2`..`n046-rep5`: four more nonce-46 repeats; the two serial reruns are
  `evidence/log-nonce46-serial.txt` plus a second rerun compared to it byte-for-byte.

Seed-46 reproducibility is exact, not just verdict-level: all **eleven** nonce-46 runs hash to
`d3fbd7305c0990961ccf1338d975c138db9e11c578f5aef740780a19c996ccaf` — the first (timing) run, the parallel
sweep run, the four extra repeats, the three hash-seed runs and the two serial reruns (95 lines each,
including the per-fixture `clause=f fixture=… pass` lines and
`clause=s last='MADO_DEVICES_SELFTEST: 48/48 passed'`).

## 2. Nonce sweep, block 2 — breadth and extremes (285 runs, 350 s)

`evidence/runs-block2.txt`. Nonces 121..400 plus five extremes: `0`, `-1`, `4294967295` (2³²−1),
`9223372036854775807` (2⁶³−1), `1000000000000000000`. All `rc=0`, `TARGET_MET`, e.g.

```
x0            … verdict=TARGET_MET … seeds=46,0
xm1           … verdict=TARGET_MET … seeds=46,-1
x4294967295   … verdict=TARGET_MET … seeds=46,4294967295
x9223372036854775807 … verdict=TARGET_MET … seeds=46,9223372036854775807
x1000000000000000000 … verdict=TARGET_MET … seeds=46,1000000000000000000
```

`--nonce=-1` is accepted (argparse negative-number form); `random.Random(-1)` and
`random.Random(10¹⁸)` both drive `names()` and `gen_case()` without error, so the counter's nonce
domain is the whole integer range in practice.

## 3. Non-MET records: the empty set, and why (mechanisms tested, not argued)

Across the 412 scored runs, the counter executed 412 selftests, 412 × 90 × 3 = **111,240**
fixture evaluations and 412 × 150 = **61,800** generated-case comparisons: **0 failures**. The three
mechanisms the assignment asks about would each have to show up in one of those two places; each is
ruled out independently:

**(a) Placeholder names colliding.** `subst()` replaces only the literal tokens `{A}` `{B}` `{C}` `{D}`
in fixture text and expected lines (`c1-r46-devices.py:129-139`). A picked name can therefore never be
re-interpreted as another placeholder, because no name contains `{` or `}` — the fully enumerated name
universe has alphabet `+ - 0-9 a-z` only (`evidence/names-analysis.txt`). Names are also pairwise
distinct within a table (the `while len(picked) < 4` loop plus the containment guard at
`c1-r46-devices.py:119-126`). Measured directly: feeding every nonce table 1..120 through the fixture
pipeline in-process reproduces all 90 canned expectations (`evidence/fixture-nonce-in-process.txt`:
`fixtures=90 nonces=1..120 checks=10800 mismatches=0`), i.e. substitution is name-agnostic.

**(b) One name a prefix of another.** The guard is `all(n not in p and p not in n for p in picked)`,
i.e. substring-non-overlap, which is strictly stronger than prefix-free. It is load-bearing: the
567-name universe holds **486 ordered containment pairs** (e.g.
`at-translated-set-2-deathadder-v2` ⊂ `at-translated-set-2-deathadder-v2-1`), so the guard is exactly
what keeps a substituted name from matching a longer device name. Checked over **200,000** seeds
(`evidence/names-analysis.txt`): every table returns 4 distinct names, pairwise non-containing, drawn
from the universe — `bad_seeds [] count 0`.

**(c) A generated config the model and the installed copy treat differently.** They are the same
bytes (`b229efd0…a33b`, table above), so a divergence would need a process-level difference. Clause g
compares the sandboxed subprocess against the in-process model, 150 cases per nonce, nonce-drawn: 61,800
comparisons, none diverged (`generated=150/150` on every run). The generated stream is not degenerate
either (`evidence/gen-case-vacuity.txt`): over nonces 1..120 the 18,000 cases contain **17,939 distinct
case hashes** (min 148 distinct per nonce), and all five verdicts occur —
`DIFFER 9085, NOT_COMPARED 4263, STALE_BLOCK 1753, NO_KEYBOARDS 1739, OK 1160`. So the MET result is
over a genuinely nonce-varying case mix, not a fixed corpus.

**Detection control (is my driver blind?)** A second clone of the same commit with one modelled
semantic removed — the `scroll_factor` clamp (`exp = min(max(blk["scroll_factor"], 0.0), 100.0)`
replaced by the raw value) — scored through the identical driver yields `TARGET_MISSED` at nonces 1, 46
and 77, with named failures: `fixture=mouse-clamp-high FAIL`, `fixture=mouse-clamp-low FAIL`,
`generated=149/150` (first divergent generated case index 64 at nonce 1, 113 at 46, 87 at 77),
`selftest=fail` (`evidence/control-mutation-missed.txt`). The empty non-MET set above is therefore a
measured result, not a harness that cannot report a failure.

## 4. `names()` — character audit (the assignment's explicit check)

`names()` (`c1-r46-devices.py:121-129`) draws from `VENDORS × MODELS × SUFFIX` only. Enumerated:

- universe size **567** (9 vendors × 9 models × 7 suffixes), length 11..62.
- regex `[\[\]\$#=A-Z]` over all 567: **no match** (`forbidden_chars []`).
- full alphabet actually reachable: `+ - 0 1 2 3 5 7 8 a b c d e f g h i k l m n o p r s t u v x y z`
  — no `[`, `]`, `$`, `#`, `=`, no uppercase, and also no whitespace, comma, quote, brace or backslash,
  which is what keeps `device[<name>]` / `name = <name>` syntactically unambiguous for every nonce.
- `+` is reachable (`yubikey-otp+fido+ccid`) and `--` is reachable (`hp--inc`): 48 of nonces 1..120 draw
  at least one `+` name and 45 draw a `--` name; 5 draw a name longer than 50 characters (max 62). All
  of those nonces are in the 120/120 MET set, so the two "unusual characters" hypotheses are covered by
  observation as well as by the alphabet audit.

## 5. Why the counter is deterministic given a nonce (structural)

- Both random streams are seeded from the nonce and nothing else:
  `random.Random(nonce)` for the environment-B stream (`score()`), and
  `random.Random(nonce ^ 0x5DEECE66D)` for `gen_case()` (`run_generated`). `names(SEED)`/`names(nonce)`
  are plain `random.Random(seed)`.
- Hash-order-free: the reference has exactly two order-relevant constructs — `names = set()` used for
  membership only (`mado-devices.py:326`) and `st.devices.items()` over an insertion-ordered dict
  (`:405`, "blocks print in creation order"). The counter sorts its set use (`hidden_paths`). Hence
  `PYTHONHASHSEED` cannot affect the printed lines — confirmed by the three hash-seed runs being
  byte-identical to the unset ones.
- Environment cannot leak in: the reference reads **no** environment variable and no locale
  (`grep -nE 'environ|getenv|locale\.|sys\.path|__file__'` → no match;
  `evidence/no-env-and-order-scan.txt`), and the counter hands the tool a fixed 4-key env
  (`env_a`, `c1-r46-devices.py:260-262`).

## 6. Findings that are residuals, not failures of the claim

1. **Clause f's "environment B" axis is inert for this contract.** `env_b` varies `LANG`, `HOME`,
   `HYPRLAND_INSTANCE_SIGNATURE` and `XDG_RUNTIME_DIR`; the reference reads none of them (only
   `sys.argv`, the files named on it, and stdin/stdout: `mado-devices.py:150,561`). So the 90 "B"
   runs are not an independent environment probe of the tool; they only re-exercise the argument and
   IO path. This is consistent with the counter's own declared residual ("a tool can still detect a
   sandbox by means not varied in environment B"), but it is worth stating exactly: for *this*
   contract, environment B varies nothing the contract can observe.
2. **`PYTHONHASHSEED` never reaches the tool subprocess.** `run_tool` passes `env_a`/`env_b`
   explicitly, neither of which contains `PYTHONHASHSEED`, so the tool always starts with Python's
   randomized hash seed. That makes the harness *stronger* than the hash-seed sweep (hash-order
   dependence in the tool would surface as per-invocation flakiness across the 111,240 fixture runs and
   the 61,800 generated runs), and it means a hash-seed sweep is only meaningful for the counter's own
   process — which is what §1 tested and found inert.
3. **Latent fragility, not observed.** Nonce dependence could return only if a future fixture (or a
   future contract) became sensitive to name *content*. Today the only name-derived text in the
   fixtures is the substituted token itself and JSON-quoted device names, and the 10,800 in-process
   fixture checks over 120 tables show no sensitivity. A future round adding a fixture that keys off
   name length or the `+`/`--` characters would need the same 120-nonce check repeated.

## 7. Time

| measurement | value |
|---|---|
| one run, idle host, serial (nonce 46) | **9.2 s** then **8.3 s** (two serial runs, byte-identical output) |
| one run under 12 concurrent counters | 12.0 s min / 15.1 s median / 18.7 s max (127 runs) |
| 127 runs (block 1) at 12-way | **168 s** wall |
| 285 runs (block 2) at 12-way | **350 s** wall |
| cost per run | 421 invocations of the tool (1 selftest + 270 fixture + 150 generated), every one inside bwrap |

## 8. Evidence files (this seat dir, `evidence/`)

| file | lines | sha256 |
|---|---|---|
| `runs-block1.txt` | 130 | `0bd6c7845c19f5f2b24cf23cd228ce98caeccfb43a9b040b1a877195d400838a` |
| `runs-block2.txt` | 286 | `160e187294c1412b5f841dd4f7cbacc194581feb47918418fd56152454c000a8` |
| `log-nonce46-serial.txt` | 95 | `d3fbd7305c0990961ccf1338d975c138db9e11c578f5aef740780a19c996ccaf` |
| `names-analysis.txt` | 17 | `49ec6c2352c56c92848d07cd88e224a59ded429fc5ac2c71a204902e2bb34b33` |
| `fixture-nonce-in-process.txt` | 2 | `55b61d62ef9b1f57eb6af395956d7d4becd4a4e11059b2fe1ecd72fc216cbb6a` |
| `gen-case-vacuity.txt` | 4 | `1efde09c52eee1623a319d7da693b431044e918db8dbce827d68bafc7311c28d` |
| `no-env-and-order-scan.txt` | 13 | `6cf4d83f948ca221d00389b8c25e6782d61f0b808d146e7ea7e5e4041f02f7e7` |
| `control-mutation-missed.txt` | 20 | `63bc2832e385b90d2c189485a383d7dfa9184253046e7ed59cf1bf0416aec48f` |

Reproduce the core result (lane bytes as frozen):

```
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r46/ExecSeedSweep); git clone -q --shared --no-checkout \
  /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach 8c5434c60e03f147ee1f75ab195e8bc3f0db4dec
mkdir -p "$D/tools" && cp /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py \
  "$D/tools/mado-devices.py"
git -C "$D" add -A && git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m s
for n in $(seq 1 120); do python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/\
c1-r46-devices.py --repo "$D" --rev HEAD --work "$(mktemp -d -p /fast/scratch/hyaku/mado-r46/ExecSeedSweep)" \
  --nonce "$n" | tail -1; done
```

## 9. Blockers / risks

- None blocking. The claim's "under any nonce" is supported for 412 nonces (1..400 plus 0, −1, 2³²−1,
  2⁶³−1, 10¹⁸) and three hash seeds; it is a sampled statement, not a proof — the structural argument in
  §5 is what generalises it.
- Host untouched: no `hyprctl`/`libinput`/`journalctl`/`udevadm` was run by me or by the scored tool
  (clause r `marker=absent` on every run); no pacman, no compositor call, no Wayland connection, no
  git/jj mutation in the lane or the fleet.
- Tool installs: **none** (no new tool was needed; only stdlib Python and the pre-existing `bwrap 0.13.1`).
- Scratch `/fast/scratch/hyaku/mado-r46/ExecSeedSweep` (two clones, work dirs) was deleted after the
  receipts in this seat dir were verified to be complete; no scratch path is cited as evidence.

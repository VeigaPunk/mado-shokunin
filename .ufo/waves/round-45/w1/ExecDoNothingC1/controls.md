# Cheap controls against PRED-C1-r45 — seat `ExecDoNothingC1`

Target of this seat: reach `PRED-C1-r45` **TARGET_MET without the capability** (the monitor-rule join), as
cheaply as possible, beyond the 16 registered controls (K00–K15 in `registration.md`). Seven new controls were
built and scored against the frozen predicate, unchanged. Four of them are MET; the predicate's clause set
does not separate them from the reference.

Everything here is a control artifact under this seat directory; nothing outside
`.ufo/waves/round-45/w1/ExecDoNothingC1/` (and this seat's report) was written. The predicate
`quality/counters/c1-r45-monitors.py` and the reference `.ufo/waves/round-45/l1-draft/mado-monitors.py` are
read-only inputs.

## Method

Scratch clone of the lane at `BASE = 0c89478af821a6424c9ac922eafe02e39630cf4f` under
`/fast/scratch/hyaku/mado-r45/ExecDoNothingC1/clone` (`git clone -q --shared --no-checkout`, toplevel asserted
equal to the clone before the first commit); for each control the file is committed at
`tools/mado-monitors.py` and scored with

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r45-monitors.py \
    --repo /fast/scratch/hyaku/mado-r45/ExecDoNothingC1/clone --rev HEAD \
    --work /fast/scratch/hyaku/mado-r45/ExecDoNothingC1/w
```

The reference itself is the calibration point (`receipts/ref.txt`): `fixtures=49/49 selftest=ok readonly=ok
tool=present verdict=TARGET_MET rev=1131626c…`.

Every control is a `tools/mado-monitors.py` that satisfies clause a (`TOOL is a regular blob … at REV`,
`c1-r45-monitors.py:9`) and prints a self-declared `MADO_MONITORS_SELFTEST: N/N passed` line, which is all
clause s reads. None of them contains a model of the monitor-rule chain except where noted.

## The controls

| # | file | idea | cost | predicate | receipt |
|---|------|------|------|-----------|---------|
| A | `control-a-lookup.py` | embeds the predicate's own `FIXTURES` table (copied verbatim), inverts the seed substitution by enumerating `names(seed)` for seed 0…4095, matches the invocation's config/dump bytes and prints the table's expected lines | 297 lines (178 are the copied table, 119 driver), **0 lines of Hyprland model** | **MET** 49/49 at seed 45, 7, 1234 | `receipts/A-lookup.txt`, `A-seed7.txt`, `A-seed1234.txt` |
| A2 | `control-a2-obfuscated.py` | same table, zlib+base85 packed and `exec`'d, so no fixture text appears as a literal | 124 lines | **MET** 49/49 | `receipts/A2-obfuscated.txt` |
| B | `control-b-counter-import.py` | opens `quality/counters/c1-r45-monitors.py` at its absolute lane path, `exec`s it as a module, reuses `FIXTURES`/`names`/`subst` as a lookup table | 98 lines | **MET** 49/49 | `receipts/B-counter-import.txt` |
| B2 | `control-b2-reference-loader.py` | a 13-line loader: `exec`s `.ufo/waves/round-45/l1-draft/mado-monitors.py` from the lane working tree and passes argv/stdin through. The scored blob is not the implementation; the implementation is not in the scored revision | 13 lines | **MET** 49/49 | `receipts/B2-ref-loader.txt` |
| E | `control-e-proc-parent.py` | no hardcoded path at all: reads its parent's argv from `/proc/<ppid>/cmdline`, finds the argument ending in `c1-r45-monitors.py`, `exec`s it | 119 lines | **MET** 49/49 under the predicate; 1/49 when the parent is anything else | `receipts/E-proc-parent.txt` |
| C | `control-c-geometry-patch.py` | `tools/mado-geometry.py` at base plus **19 added lines** (one shortcut function + 2 lines in `main`) that answers the one host-shaped case and fakes the selftest | 508 lines (19 added) | **MISSED** 1/49 (only `host`) | `receipts/C-geometry-patch.txt` |
| D | `control-d-host-config.py` | hardcodes this host's single rule (`DP-1, 3440x1440@100, 0x0, 1`) and its live state | 52 lines | **MISSED** 4/49 (`host` + three setup fixtures by accident) | `receipts/D-host-only.txt` |

The two corners the predicate does not defend, read off the receipts:

* **The input space is closed and published.** Clause f runs the predicate's own 49 cases
  (`c1-r45-monitors.py:12`, “every fixture of FIXTURES below passes: the tool is extracted to a fresh directory
  under --work”). A tool that holds those cases as data passes them; the seeded placeholders are invertible
  because `names(seed)` is in the predicate and the seed space is small (A is MET at seeds 7, 45 and 1234).
  The redirect `--seed` is not a defence: A recovers the table for any seed in 0…4095.
* **Nothing bounds what the tool may read.** The reference promises “It reads files and standard input only; it
  starts no process and opens no socket.” (`l1-draft/mado-monitors.py:22`), but clause r only builds fake PATH
  executables (`c1-r45-monitors.py:19`). B reads the predicate from the lane; E finds it through
  `/proc/<ppid>/cmdline`, with no path in its source; B2 loads the reference out of an uncommitted working-tree
  path. All three are 49/49.

C and D are the honest failures: 19 lines of geometry with a host-shaped shortcut, or a tool that knows the
host's one rule, cannot reach the 49 cases. They are reported so the frontier is not overread.

## Tightenings measured (not applied; the predicate is frozen)

Both are implemented as separate harnesses so the frozen predicate could be scored beside them, and both keep
the reference MET on the same 49 cases.

### T1 — semantics-free invariance re-runs of every fixture (`tighten-check.py`)

For each fixture the predicate would run, run three more inputs whose expected output is derivable from the
existing expectation without a model:

* `serialize` — the same list dump written `json.dumps(..., sort_keys=True, separators=(",", ":"))`; expected
  output byte-identical (a tool reads fields, not JSON bytes);
* `extra-config` — one more `--config` argument holding a single comment line; contributes 0 to
  `lines/v2/rules`, so expected output is byte-identical;
* `reorder` — for a dump of ≥2 outputs, the dump reversed; expected rule lines and summary unchanged, the
  `MADO_MON_OUTPUT` lines in reversed order (outputs are reported in dump order).

| rev | base | serialize | extra | reorder | verdict |
|-----|------|-----------|-------|---------|---------|
| REF `1131626c…` | 49/49 | 47/47 | 48/48 | 3/3 | **MET** |
| A `57bfe5ec…` | 49/49 | 2/47 | 1/48 | 0/3 | MISSED |
| A2 `d6287b94…` | 49/49 | 2/47 | 1/48 | 0/3 | MISSED |
| B `43d44dba…` | 49/49 | 2/47 | 1/48 | 0/3 | MISSED |
| E `e6c70099…` | 1/49 | 1/47 | 1/48 | 0/3 | MISSED |
| B2 `6e793d4c…` | 49/49 | 47/47 | 48/48 | 3/3 | MET |
| C `1aaff2ce…` | 1/49 | 1/47 | 0/48 | 0/3 | MISSED |
| D `4ba00467…` | 4/49 | 3/47 | 0/48 | 0/3 | MISSED |

Receipts: `receipts/tighten-*.txt`. Cost: ~15 lines inside `run_fixture` (one variant loop) plus the
serialisation switch; the reorder case exists for only 3 of the 49 fixtures, so the tightening is cheap but its
teeth are shallow — see residuals. E's base collapses only because its source of truth is the parent's argv;
under the predicate it is MET (`receipts/E-proc-parent.txt`).

### T2 — a read audit around the fixture call (`read-audit.py`)

Clause r extension: run each fixture under `strace -f -e trace=openat` and fail the tool if any `openat` names a
path under `/home`, or `/proc/<pid>/cmdline` / `/proc/<pid>/environ`. The reference opens 78 paths, none under
`/home` (its only `/proc` open is `/proc/self/maps`, which the interpreter makes).

| rev | opens | home | proc | verdict |
|-----|-------|------|------|---------|
| REF | 78 | 0 | 0 | **PASS** |
| A | 81 | 0 | 0 | PASS (expected: the table is embedded) |
| A2 | 89 | 0 | 0 | PASS (expected) |
| B | 140 | 1 | 0 | FAIL (`quality/counters/c1-r45-monitors.py` opened by the tool process) |
| B2 | 79 | 1 | 0 | FAIL (`.ufo/waves/round-45/l1-draft/mado-monitors.py` opened) |
| E | 74 | 0 | 1 | FAIL (`/proc/<ppid>/cmdline`) |

Receipts: `receipts/audit-*.txt`. Note E's receipt shows `rc=2`: the audit harness's own parent is not the
predicate, so E could not load it there — the violation is the `cmdline` open itself, which happens either way.

### T3 — run the fixture with no ambient filesystem (same file, `--sandbox bwrap`)

`bwrap --ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind /etc /etc --dev /dev
--tmpfs /tmp --bind <work> <work> --unshare-all` — only the interpreter tree, the tool dir and the fixture dir
exist. This is the tightening that catches a loader with no syscall inspection and no path knowledge.

| rev | rc | stdout match | verdict |
|-----|----|--------------|---------|
| REF | 0 | yes | **PASS** |
| A | 0 | yes | PASS |
| B | 1 | no | FAIL (counter path absent) |
| E | 1 | no | FAIL (`/proc` absent) |
| B2 | 1 | no | FAIL (lane absent) |

Receipts: `receipts/ns-*.txt`.

## Should-catch map

| control | clause that should catch it | tightening that does (measured) |
|---------|------------------------------|----------------------------------|
| A | f — but the cases are published data, not a capability | T1 (serialize/extra/reorder: 2/47, 1/48, 0/3), or fresh cases; T2/T3 do not catch it |
| A2 | f | T1; T2 and T3 do not catch it (obfuscation defeats any textual screen on the blob) |
| B | r (“read-only”), which today only watches PATH | T1 and T2 and T3 |
| E | r | T2 (proc rule) and T3; T1 only because E is not a tool at all |
| B2 | a/f — the blob at REV is not the capability | T2 and T3 (provenance by isolation); T1 does not catch it, by construction |
| C | f (1/49) | already caught |
| D | f (4/49) | already caught |

## Declared residuals

* **A table over a published finite case set is not separable from a model by clauses a/s/f.** T1 raises the
  price (the table must also cover the serialisation, argument-count and ordering variants) but a table
  extended to those variants still passes; closing it needs cases the tool has not seen, generated by a
  semantics oracle the predicate would have to hold — and an oracle in the predicate is the implementation.
  This is the registration's own declared residual: “a tool holding a model of the contract is an
  implementation of it” (`registration.md:32`).
* **Clause s is self-declared.** Every control here prints `MADO_MONITORS_SELFTEST: 49/49 passed` without
  running a test; nothing in the predicate can tell that line from the reference's 33/33.
* **Clause r's scope is PATH only** (“read-only: PATH starts with a directory holding executables”,
  `c1-r45-monitors.py:19`); B, B2 and E read the predicate with no PATH lookup at all. T2/T3 are the extension;
  T3 depends on `bwrap`/`unshare` being present on the counting host (both are, on this host).
* T1's reorder variant exists for 3 fixtures only; on its own it costs a table-lookup tool 3 cases, not a
  verdict, and T1's verdict is decided by `serialize`/`extra-config`.
* Not exercised: sockets/network (the reference claims it opens none), and whether the *reference* remains MET
  at the data commit and the round tip — that is the integrator's re-score, not this seat's.

## Files

| file | role |
|------|------|
| `control-a-lookup.py` | control A (embedded fixture table + seed inversion), sha256 `69deeb7c…` |
| `control-a2-obfuscated.py` | control A2 (packed table), `963509b2…` |
| `control-b-counter-import.py` | control B (exec the predicate at its lane path), `cf49938b…` |
| `control-b2-reference-loader.py` | control B2 (exec the reference), `2808a3e2…` |
| `control-e-proc-parent.py` | control E (find the predicate via `/proc`), `8dff0fb1…` |
| `control-c-geometry-patch.py` | control C (mado-geometry + 19 lines), `318ebb14…` |
| `control-d-host-config.py` | control D (host config only), `61e17993…` |
| `tighten-check.py` | T1 harness (invariance re-runs), `a1635be7…` |
| `read-audit.py` | T2/T3 harness (strace audit, bwrap sandbox), `7520fc0e…` |
| `receipts/*.txt` | predicate scores, tightening scores, audit and namespace runs, quote check |

Full hashes: `sha256sum control-*.py tighten-check.py read-audit.py` (recorded in `receipts/quote-check.txt`
beside the quote grep).

## Reproduction

```
S=/fast/scratch/hyaku/mado-r45/ExecDoNothingC1
D=$S/clone
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach 0c89478af821a6424c9ac922eafe02e39630cf4f
cp <control>.py "$D/tools/mado-monitors.py"
git -C "$D" add -A && git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m ctl
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r45-monitors.py \
    --repo "$D" --rev HEAD --work "$S/w"
python3 -I .ufo/waves/round-45/w1/ExecDoNothingC1/tighten-check.py --repo "$D" --rev HEAD --work "$S/w"
python3 -I .ufo/waves/round-45/w1/ExecDoNothingC1/read-audit.py --repo "$D" --rev HEAD --work "$S/w"
python3 -I .ufo/waves/round-45/w1/ExecDoNothingC1/read-audit.py --repo "$D" --rev HEAD --work "$S/w" --sandbox bwrap
```

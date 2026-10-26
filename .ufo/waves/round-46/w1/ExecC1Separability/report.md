# w1 ExecC1Separability — C1/C2 separability on scratch trees (round 46)

Seat: `ExecC1Separability` (leaf). Date 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`.
Scratch `/fast/scratch/hyaku/mado-r46/ExecC1Separability/` (deleted after capture; receipts copied here first).
No compositor call, no host write, no pacman, no tool install.

## What was built (three trees, from the freeze commit)

Every clone: `git clone -q --shared --no-checkout <lane> $S/<tree>`; `git -C <tree> rev-parse --show-toplevel`
asserted equal to `<tree>`; `git -C <tree> checkout -q --detach 8c5434c6…`; commit with
`-c user.name=seat -c user.email=seat@scratch.invalid`. `git -C <tree> diff --name-status <freeze> HEAD`:

| tree | HEAD | changes vs freeze |
|---|---|---|
| tool-only | `df96498a14f21ae718e4faa99a0155ea01b7c1a3` | `A tools/mado-devices.py` (only) |
| data-only | `2072be438cf42494d55e097c98967d4da90d9faa` | `M corpus/README.md`, `M corpus/SOURCES.md`, `A corpus/knowledge/hyprland-input-devices-r46.md`, `A corpus/lessons/round-46.md` |
| both (extra probe) | `e76f12ca2a92914adef72b3fa094879cda939c53` | the four data files + `tools/mado-devices.py` |

TOOL-ONLY install: `install -m 0644 .ufo/waves/round-46/l1-draft/mado-devices.py <tree>/tools/mado-devices.py`;
blob mode `100644`, sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` — identical to the
reference (`sha256sum` of both, `receipts/trees.txt`). DATA-ONLY: `python3 -I .ufo/waves/round-46/l1-draft/build-pos.py <tree>`
(printed `applied`), and `test ! -e <tree>/tools/mado-devices.py` before committing.

Commands (as run, `--work` pre-created; it must already exist):
```
python3 -I <lane>/quality/counters/c1-r46-devices.py --repo <tree> --rev HEAD --work <scratch>/w-c1-<tree> --nonce 46
python3 -I <lane>/quality/counters/c2-r46-input-device-entry.py --repo <tree> --rev HEAD --base b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
```

## The four final lines, verbatim

TOOL-ONLY, C1 (`receipts/c1-tool-only.txt`, 95 lines, exit 0):
```
PRED-C1-r46: fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=df96498a14f21ae718e4faa99a0155ea01b7c1a3 seeds=46,46
```
TOOL-ONLY, C2 (`receipts/c2-tool-only.txt`, exit 1):
```
PRED-C2-r46 hyprland-input-devices-r46.md clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 j:0 admitted=0
PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=df96498a14f21ae718e4faa99a0155ea01b7c1a3
```
DATA-ONLY, C1 (`receipts/c1-data-only.txt`, exit 1):
```
PRED-C1-r46 clause=a tool=absent
PRED-C1-r46: fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED rev=2072be438cf42494d55e097c98967d4da90d9faa seeds=46,46
```
DATA-ONLY, C2 (`receipts/c2-data-only.txt`, 60 lines, exit 0):
```
PRED-C2-r46 hyprland-input-devices-r46.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1
PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=2072be438cf42494d55e097c98967d4da90d9faa
```

Expected direction held in both directions. Supporting clause evidence from `c1-tool-only.txt`:
`:2 clause=s rc=0 last='MADO_DEVICES_SELFTEST: 48/48 passed'`, `clause=f fixture=… pass` ×90 (labels through
`setup-bad-utf8`, `setup-config-too-large`, `setup-dump-too-large`), `:93 clause=g generated=150/150`,
`clause=r marker=absent`. DATA-ONLY C2 shows 28 `clause=j surface=… cited=1` lines, 10 each of `clause=c`, `clause=d`
and `clause=g` (ids S316-S325), and the summary line `:59 clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1`;
`grep -c FAIL` is 0 on both receipts.

## Cross-reads (code-located, not inferred)

C1 counter, `quality/counters/c1-r46-devices.py`:
- `:61 TOOL = "tools/mado-devices.py"`; `:357 git(repo,"ls-tree",full,"--",TOOL)`; `:363 git(repo,"show","<full>:TOOL")`
  — the only path read from the scored repo. A `grep -nE "corpus|SOURCES|README|knowledge|lessons|ENTRY|LESSON"`
  over the whole counter matches only `tools/` lines: **C1 reads no part of the C2 artifact.**
- Off-tree reads, both from the counter's own lane and both sha256-pinned: `:62` fixtures
  `quality/counters/c1-r46-fixtures.json` (`027ed508…`), `:63-64` MODEL `.ufo/waves/round-46/l1-draft/mado-devices.py`
  (`b229efd0…`). Those are the contract source, not the entry/registry/README.
- `:361` initializes `fixtures_ok, selftest, readonly, g_ok = 0, "fail", "fail", 0`; the body runs only under
  `if present:` (`:362`), and clause i additionally hides the repository, the counter's lane and the lane's parent
  from every tool run — so the tool cannot reach the data side even inside the sandbox.

C2 counter, `quality/counters/c2-r46-input-device-entry.py`:
- `:89-91` ENTRY `corpus/knowledge/hyprland-input-devices-r46.md`, LESSON `corpus/lessons/round-46.md`,
  FETCH `.ufo/waves/round-46/fetch/`; reads at REV/BASE: `:703` entry at base (precondition), `:706-707`
  `corpus/SOURCES.md` at rev and base, `:708` lesson, `:709` README, `:425/:449` entry, `:399/:440` the
  `FETCH/` pins, `:680` the first cited receipt (a `FETCH/` path).
- `grep -nE "tools/|mado-devices|devices\.py"` over the counter returns **nothing**: C2 never opens, hashes or runs
  the tool. In both data trees the tool could be added or absent with no effect on the result.

Empirical confirmation of the same statement: TOOL-ONLY's C2 finished with every clause flag 0 (no SETUP), i.e. a
genuine rejection with the pins/README/registry all present, not a harness failure; DATA-ONLY's C1 emitted only
`clause=a tool=absent`.

## Extra probe: both artifacts in one tree (`e76f12ca`)

`receipts/c1-both.txt`, exit 0:
```
PRED-C1-r46: fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=e76f12ca2a92914adef72b3fa094879cda939c53 seeds=46,46
```
`receipts/c2-both.txt`, exit 0:
```
PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=e76f12ca2a92914adef72b3fa094879cda939c53
```
Neither counter is harmed by the other's artifact, so the two METs are not mutually exclusive at one commit.

## Risks and notes for the L1

1. **`readonly=fail` on the DATA-ONLY line is not evidence of a write.** `:361` seeds `readonly="fail"`; the marker
   check (`:400`) only runs under `if present:`. On a tree with no tool the flag is unset, not observed. Applies
   equally to `selftest=fail` there.
2. **`--work` must pre-exist**, else `SETUP work dir missing` (`:419`), exit 2 — observed on the first attempt with
   `mkdir -p` omitted. This is a usage trap, not a C1 property.
3. **The counters are not self-contained.** C1's oracle and fixtures live in the counter's own lane
   (`:62-64`); scoring a copy of the counter without that lane is a setup error. Separability as shown is a property
   of the *scored tree*, not of a counter in isolation.
4. **Both counters resolve `--base` inside the scored repo** (C2 vacuous-precondition check `:703-705`), so a
   shallow or squashed clone yields SETUP rather than a verdict. All three trees here were `--shared` clones of the
   lane with full history, so `b22ea56` resolved.
5. **The single-artifact METs sit at two different commits** (`df96498a` vs `2072be43`); the pair alone does not prove
   one commit can satisfy both. The both-artifacts probe at `e76f12ca` closes that gap.
6. Not run (out of this seat's assignment): the C1 control battery V01-V20, the round-45 w2 falsification (D1),
   mutation testing. This seat only measured separability.

## Receipts (sha256)

| file | sha256 |
|---|---|
| `receipts/c1-tool-only.txt` | `52cf6796a5b9d50d089e11085a4f3f2e8827f8133e6250179741d5c7446c99c6` |
| `receipts/c2-tool-only.txt` | `8a43f0fbfe43a542bc55ae11f10abdc3d2b44591fbf1aa60d26659ec989c0496` |
| `receipts/c1-data-only.txt` | `cfcf5a290813db8423f51f3c4ab115340eebf0634ae3d181b5ed02739077e8df` |
| `receipts/c2-data-only.txt` | `514bdb8930bdbe9025e04d124969c4f29348b515cefee791f669de9e8a25c644` |
| `receipts/c1-both.txt` | `537dc774f013d1b7ecaa8832f6001e838eda97ce6bf84af9ded2f8babde6036e` |
| `receipts/c2-both.txt` | `f2d46a4d9ca35b0f2bb2f0ac61f26871623e317e9653c3d4effaca63105328c7` |
| `receipts/trees.txt` | `be36ad0550e1610e947eea413dfaec17fa539047b4abbda26fc1ae0904b4d26c` |

# ExecC1Separability — report trailer (round-46 w1)

Full report: `.ufo/waves/round-46/w1/ExecC1Separability/report.md`; receipts (six counter logs + provenance) in
`.ufo/waves/round-46/w1/ExecC1Separability/receipts/`.

## Result: separability holds in both directions

Three scratch clones of the freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec` (lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`), toplevel asserted, one commit each:

- tool-only `df96498a14f21ae718e4faa99a0155ea01b7c1a3` — only `A tools/mado-devices.py` (installed `0644`, sha256
  `b229efd0…`, byte-identical to the L1 reference).
- data-only `2072be438cf42494d55e097c98967d4da90d9faa` — only the four data files produced by
  `.ufo/waves/round-46/l1-draft/build-pos.py`; no `tools/` change.
- both `e76f12ca2a92914adef72b3fa094879cda939c53` — extra probe (both artifacts).

Final lines verbatim (`--nonce 46` for C1; C2 `--base b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`):

```
PRED-C1-r46: fixtures=90/90 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=df96498a14f21ae718e4faa99a0155ea01b7c1a3 seeds=46,46
PRED-C2-r46 hyprland-input-devices-r46.md clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 j:0 admitted=0
PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=df96498a14f21ae718e4faa99a0155ea01b7c1a3
PRED-C1-r46 clause=a tool=absent
PRED-C1-r46: fixtures=0/90 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED rev=2072be438cf42494d55e097c98967d4da90d9faa seeds=46,46
PRED-C2-r46 hyprland-input-devices-r46.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1
PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=2072be438cf42494d55e097c98967d4da90d9faa
```
Exits: C1 tool-only 0, C2 tool-only 1, C1 data-only 1, C2 data-only 0. Both-artifacts probe: C1 `TARGET_MET` and C2
`admitted=1/1 verdict=TARGET_MET` at `e76f12ca`, exit 0 both.

## Cross-reads found

- C1 (`quality/counters/c1-r46-devices.py:61,357,363`) reads exactly one path from the scored tree,
  `tools/mado-devices.py`; it never names `corpus/`, `SOURCES.md`, `README` or the entry. Its fixtures (`:62`) and its
  oracle `MODEL` (`:63-64`, `.ufo/waves/round-46/l1-draft/mado-devices.py`, pinned `b229efd0…`) are ambient reads from
  the counter's own lane, not from the scored tree.
- C2 (`quality/counters/c2-r46-input-device-entry.py:89-91,399,425,440,449,680,703-712`) reads only the entry,
  `corpus/SOURCES.md` at rev and base, the lesson, `corpus/README.md` and the `FETCH/` pins; a grep for
  `tools/|mado-devices|devices\.py` in that counter matches nothing, so it never opens or runs the tool.
- Tool-only C2 returned all ten clause flags 0 (no SETUP), so its 0 is a rejection with the pins/registry/README
  present, not a harness failure; data-only C1 emitted only `clause=a tool=absent`.

## Notes / risks passed to the L1

1. `readonly=fail` (and `selftest=fail`) on the data-only line are unset defaults (`:361`), computed only under
   `if present:`; they are not evidence of a write or a failing selftest.
2. `--work` must pre-exist, else exit 2 `SETUP work dir missing` (`:419`) — observed on the first attempt.
3. Both counters depend on ambient state: C1 on its lane's fixtures + L1 draft, C2 on `--base` being reachable in the
   scored repo. Separability is a property of the scored tree, not of a standalone copy of a counter.
4. The two single-artifact METs are different commits; the both-artifacts probe covers the single-commit case.
5. Not run here (outside this seat): C1 controls V01-V20, round-45 D1 w2 falsification, mutation tests.

Scratch `/fast/scratch/hyaku/mado-r46/ExecC1Separability/` deleted after receipts were copied into the seat dir. No
compositor call, no host write, no pacman, no tool install.

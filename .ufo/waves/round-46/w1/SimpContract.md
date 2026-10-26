# Seat SimpContract — report (round 46 w1, C1 contract/code dead weight)

**Status: DONE.** Target: `.ufo/waves/round-46/l1-draft/mado-devices.py` (frozen, sha256 `b229efd0…a33b`).
Full deliverable: `.ufo/waves/round-46/w1/SimpContract/dead-weight.md`.

## What was asked and what came back

67 one-anchor variants of the reference were compared with it over 6,509 in-process cases (81 fixtures rebuilt
from the frozen fixture file, 3,992 counter-`gen_case` cases, 2,436 hand cases) plus 23 real-process cases
(argv, missing/dir/FIFO/`/dev/null`, stdin, >1 MiB dump and config, 100k-deep JSON, bad UTF-8, dump without
`mice`, symlinked config). 54 variants are LIVE; 13 are NO-DIFF.

**The four spots named in the ticket are all load-bearing — not one may be deleted:**

* `else: st.device(bracket)` (lines 290-291): `device[logitech-keyboard]:output = DP-1` → reference prints a
  `MADO_DEV_BLOCK` line (`MATCHED`), the variant prints none (V10, 602 cases).
* `cur is False` paths (296-303): `device {\n kb_layout = de\n name = k\n}` → ref `unsupported=2 blocks=0`; without
  `cur = False` `unsupported=1 blocks=1` (V15). Two more independent witnesses for the guard and the rename arm
  (V14 `KeyError: False`, V16).
* `FLT_MIN` vs `isinf` (line 216): both conjuncts separate (`1e39` → V09; `1.17549430e-38` → V08). The
  `abs(float(m.group(0)))` form is also the *pinned-correct* one — see the finding below.
* `dump_names` on non-list values (line 328): a dump carrying any extra non-list top-level key makes the variant
  crash where the reference prints `OK` (V05/V04); the contract admits arbitrary top-level keys.

**Dead weight found and deleted** (produces `mado-devices-simplified.py`, 5 deletions / 6 hunks, `simplified.diff`):

1. `rb != -1` in `if lb != -1 and rb != -1 and lb < rb:` — implied by its neighbours (proof + 137k-string brute
   force, `proofs.out` P1); 231 adversarial pairs identical. Its neighbours are live (V02, V01b).
2. `isinstance(kb.get(n), str) else None` on `rep` — `exp` is always `str` and `FALLBACK` is all-`str`, so a
   non-string reported name behaves exactly like `None` in both readers (124k (exp, value) pairs, P2).
3. `"\n"` in `WS` — `parse_config` splits on `"\n"` first, so no line can contain one (200k texts, P3); `"\r"` must
   stay (live via `input:kb_layout\r# c`).
4. `math.inf if x > 0 else -math.inf` → `math.inf` in `f32` — the only reader is `math.isinf` (P4).
5. three duplicated `st.device(bracket)` calls hoisted to one (equivalence proven, 165 pairs).

Score of the simplified tool (frozen counter, scratch clone of the freeze `8c5434c`, tool at `tools/mado-devices.py`):
`counter-simplified-4601.txt` and `counter-simplified-777.txt` — `fixtures=90/90 generated=150/150 selftest=ok
readonly=ok tool=present verdict=TARGET_MET`, two nonces. Reference-tool control at the same nonce:
`counter-reference-4601.txt`, `TARGET_MET`. Selftest 48/48 both sides (`selftest.out`); differential 0/6,509 and
0/23 (`differential.out`).

## Finding for the L1 (not dead weight, not applied)

Line 216 `v != 0.0 and abs(float(m.group(0))) < FLT_MIN` mis-handles the underflow-to-zero corner:
`device[m]:scroll_factor = 1e-46` is stored as `0.0` with **no** `unsupported` flag, so the tool can print
`scroll_factor=0.00 AGREE` where the docstring ("a nonzero value below 2**-126 in magnitude adds one to
`unsupported`") and the pin both say the line is rejected. Grounded on this host: `g++ -std=c++20` shows
`std::stof` throws for `1e-46`/`1e-40`/`1.17549430e-38`/`1e39` and returns for `0x10`/`0.335`/`5.`/`.5`
(`stof-grounding.txt`); hyprlang turns the throw into a parse error (`fetch/hyprlang-config.cpp:466-471`).
One-line fix: delete `v != 0.0 and`. No fixture and no `FACTORS` value reaches that region, so C1 f/g cannot see
it — it is the declared residual "a contract error shared by reference and tool is invisible to it". A v2/v3
contract decision, not a w1 edit (the reference is frozen and the counter pins its sha256).

Also recorded: `SPECIAL_RE`'s `0x` arm is conservative against the pin (pin returns 16.0 for `0x10`); it is declared
in the docstring and only ever produces `NOT_COMPARED`, so leave it.

## Files in this seat dir

| file | what |
|---|---|
| `dead-weight.md` | the deliverable: census of every branch (live witness / dead proof), 5 deletions, finding |
| `mado-devices-simplified.py` | reference + the 5 deletions (sha256 `7a3fa612…4372`) |
| `simplified.diff` | exact change, 6 hunks |
| `witnesses.txt` | one killer witness per live variant (cfg, rc, summary line ref vs variant) |
| `variants-summary.txt` | LIVE/NO-DIFF + file-level count for all 67 variants |
| `dead-pairs.txt` | adversarial identical-output pair counts for the five deletions |
| `proofs.out` | unreachability proofs P1-P5 (brute force / typing / invariant / call-site) |
| `selftest.out`, `differential.out` | 48/48 both sides; 0/6,509 + 0/23 |
| `counter-simplified-4601.txt`, `counter-simplified-777.txt`, `counter-reference-4601.txt` | frozen counter receipts |
| `stof-grounding.txt` | the `std::stof` probe source + output behind the §finding |
| `verify-quotes.out` | every quoted source line verified at its stated line and present in `dead-weight.md` |
| `probe2.py`, `witnesses.py`, `dead_pairs.py`, `proofs.py`, `diff_check.py`, `verify_quotes.py` | harness (scratch dir deleted; run from any dir with the paths shown in `dead-weight.md` §1) |

## Safety / hygiene

No lane file edited; no mutating git in the lane or the fleet; no compositor call (no `hyprctl` of any kind, no
Wayland client), no `pacman`; scratch confined to `/fast/scratch/hyaku/mado-r46/SimpContract` and deleted at the
end; no tool installed (the `g++` used for the `std::stof` probe is the host's existing compiler).

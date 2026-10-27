# MutC1Tool — round-50 w1

**Verdict:** 29 one-behaviour mutants scored against the landed `tools/mado-keysym.py` with frozen `PRED-C1-r49`: **21 killed, 8 survived, 0 inconclusive among the final runs.** The first M01–M06 wrapper attempts failed before invoking the counter (`line 35: he: command not found`); archived in `MutC1Tool/receipts/initial-driver-error-M01-M06.md`, then all six were re-run with the stable driver and only the successful reruns are scored below.

## Detector and restoration

Attack axes: keymap/model resolution, keysym argument/name resolution, output rendering, CLI refusal, and counter fixture/generator coverage. Detector was invoked directly (not under an outer tracer) as frozen `quality/counters/c1-r49-keysym.py`, on a `git clone --shared` fixture repo with a one-file fixture commit per mutant, nonce `20261027`, `--work` and `TMPDIR` in scratch, and HOME/XDG paths sandboxed there. Every fixture repo's toplevel was asserted before its commit; each commit parent was `13631f24050f22db92bf5bd33e0f4d014192992e`.

- Pristine: tool SHA-256 `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265`; `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` (exit 0), `receipts/BASE.txt`.
- Restored after the mutation campaign: identical tool SHA; same `633/633`, `150/150`, `selftest=ok`, `readonly=ok`, `TARGET_MET` (exit 0), `receipts/RESTORED.txt`.
- Every per-mutant clone was restored to the same pristine bytes. Fixture commit IDs, mutant SHA-256, and restored SHA-256 are in `MutC1Tool/hash-ledger.md`; all restored hashes equal the pristine SHA. Every valid counter run reported `trips=0` and `tool=present`.
- Frozen counter outputs are in `MutC1Tool/receipts/M01.txt` … `M29.txt`; the first metadata line was removed from saved receipts to avoid retaining the counter's absolute lane path. Revision IDs and nonce are preserved in the hash ledger / this report.

**Scratch-cap deviation:** The clone-per-mutant campaign measured 11 GiB scratch use, exceeding the 2 GiB cap. I pruned to three clones (measured 1.1 GiB), created one additional clone for M29, and removed the entire scratch tree before handoff. The transient cap violation is recorded here; the final cleanup check reported `scratch-removed`.

## Results

`S` = selftest count; `F` = fixtures; `G` = generated cases. `killed` means the frozen counter returned `TARGET_MISSED`; `survived` means it returned `TARGET_MET`.

| ID | One-behaviour mutation | S / F / G | Verdict |
|---|---|---:|---|
| M01 | Invert automatic 2-level ALPHABETIC predicate | 35/38 · 563/633 · 143/150 | killed |
| M02 | Widen keypad keysym range to `0xFFFF` | 38/38 · 626/633 · 148/150 | killed |
| M03 | Ignore explicit per-group type | 38/38 · 629/633 · 150/150 | killed |
| M04 | Copy group-1 levels into later group even when that group has an explicit type | 38/38 · 633/633 · 150/150 | survived |
| M05 | Make `AnyOfOrNone` fail for mod-less keys | 38/38 · 633/633 · 150/150 | survived |
| M06 | Invert top-level `interpret.useModMapMods` default | 38/38 · 609/633 · 149/150 | killed |
| M07 | Zero canonical fallback mapping for unbound vmods | 17/38 · 633/633 · 150/150 | killed |
| M08 | Ignore per-key explicit `virtualMods=` | 38/38 · 633/633 · 148/150 | killed |
| M09 | Allow virtual-modifier index in `modifier_map` handling | 38/38 · 633/633 · 150/150 | survived |
| M10 | Iterate keycodes in insertion rather than sorted order | 38/38 · 633/633 · 150/150 | survived |
| M11 | Reverse modifier-name printing order | 35/38 · 524/633 · 132/150 | killed |
| M12 | Remove missing-layout-name fallback `?` | 37/38 · 633/633 · 150/150 | killed |
| M13 | Shift `name[GroupN]` index by one | 17/38 · 137/633 · 92/150 | killed |
| M14 | Print level column zero-based | 17/38 · 137/633 · 92/150 | killed |
| M15 | Print layout column zero-based | 17/38 · 137/633 · 92/150 | killed |
| M16 | Drop final output newline | 12/38 · 52/633 · 12/150 | killed |
| M17 | Use six hex digits in keysym header value (`0x%06x`) | 38/38 · 103/633 · 61/150 | killed |
| M18 | Lower Unicode-name upper threshold to `0x0100FFFF` | 38/38 · 633/633 · 150/150 | survived |
| M19 | Lower Unicode-name lower threshold to `0x01000000` | 38/38 · 633/633 · 150/150 | survived |
| M20 | Raise `U`-form parser threshold to `0xFFFD` | 38/38 · 633/633 · 150/150 | survived |
| M21 | Remove `XF86_` name fallback | 37/38 · 633/633 · 150/150 | killed |
| M22 | Accept nonpositive decimal in `resolve_argument` | 38/38 · 633/633 · 150/150 | survived |
| M23 | Accept `0x` values above `KEYSYM_MAX` | 37/38 · 633/633 · 150/150 | killed |
| M24 | Accept levels with multiple keysyms when first matches | 37/38 · 633/633 · 150/150 | killed |
| M25 | Add zero mask at every level, not only level 0 | 30/38 · 423/633 · 123/150 | killed |
| M26 | Make parsed keycode alias self-referential | 37/38 · 633/633 · 150/150 | killed |
| M27 | Refuse missing compose/keysyms flags only when both are absent | 36/38 · 633/633 · 150/150 | killed |
| M28 | Accept extra positional arguments | 37/38 · 633/633 · 150/150 | killed |
| M29 | Run canonical vmod fallback before key-derived vmod mappings | 38/38 · 609/633 · 149/150 | killed |

The lock/Shift-cancels-lock rule was not present as a modeled behavior in the landed tool (compatibility action statements are skipped; key type map/preserve entries are modeled), so it was skipped as instructed. M29 is the phase-order mutant for the vmod mapping ordering surface.

## Survivor gaps / limits

- **M04 — explicit-type-only later group.** The current 633 fixtures and 150 generated RMLVO cases did not distinguish the changed group-copy rule. Proposed targeted serialized-keymap fixture: a key with group 1 symbols and group 2 carrying an explicit type but no group-2 symbols; query a group-1 symbol and compare whether a spurious group-2 row is emitted. The frozen counter accepts RMLVOs only, so it would need a byte-pinned serialized-keymap fixture mode (or an RMLVO that produces this shape).
- **M05 — `AnyOfOrNone` / mod-less key.** Proposed internal-model fixture: a compatibility `interpret` with a virtual modifier on a mod-less key. **[INFERENCE]** This may be observationally equivalent for the current CLI output: the changed branch only applies when `key.modmap == 0`; the subsequent virtual-to-real mapping ORs that zero mask, and rendering uses resolved type masks rather than `key.vmodmap` (`tools/mado-keysym.py:1381-1395, 1396-1474, 1505-1544`). A C1 output fixture cannot kill an output-inert mutation; a model-state oracle would be a different contract.
- **M09 — virtual modifier named by `modifier_map`.** Proposed fixture: a judge-accepted serialized keymap whose modifier-map declaration names a virtual modifier, then a key/keysym whose resolved row changes. The present RMLVO-only fixture generator did not produce such a declaration; if libxkbcommon rejects it, classify this mutation as outside the counter's accepted input domain rather than a C1 gap.
- **M10 — key declaration order.** Proposed raw serialized-keymap fixture with key declarations in a different order from keycode order. The frozen generator supplies compiler-serialized keymaps; a sampled `us` compile was keycode-sorted. This is not distinguished by the current RMLVO-only input path; raw keymap support would be needed to make the order-sensitive parser path observable.
- **M18 — Unicode-name upper threshold.** Current fixture JSON contains no `U`-form arguments; the generator's `U` bucket tops out at code point `0x2FFF`. Add e.g. RMLVO `layout=us`, `arg=U1F600` to cover the astral Unicode-name range.
- **M19 — Unicode-name lower threshold.** Add e.g. `layout=us`, `arg=0x10000041` (a numeric keysym just below `KEYSYM_UNICODE_MIN`) to exercise the lower threshold directly.
- **M20 — `U`-form threshold.** Add a focused `U`-form case within `0x0100..0xFFFD`, e.g. `layout=us`, `arg=U03A3`, to distinguish the parser's Unicode-offset path from `keysym_utf32_to_keysym`; this is a proposed probe, not separately executed.
- **M22 — nonpositive decimal helper branch.** The frozen fixtures include `-1`, but the CLI parser treats a leading `-` as an option before calling `resolve_argument`, so the counter still sees matching usage refusals. Proposed direct helper fixture: `resolve_argument("-1")`; this is not representable in the current command-line fixture contract, and is not evidence of a CLI-output gap.

## Deliverables

- `MutC1Tool/make_mutants.py`, `MutC1Tool/mutants/manifest.json`, `MutC1Tool/mutants/M01.py` … `M29.py`
- `MutC1Tool/run_one.sh`
- `MutC1Tool/hash-ledger.md`
- `MutC1Tool/receipts/BASE.txt`, `RESTORED.txt`, `M01.txt` … `M29.txt`, `initial-driver-error-M01-M06.md`

All listed files were kept in the assigned seat directory or report path. Scratch clones and work files were removed before handoff.

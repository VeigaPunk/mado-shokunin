# ReviewV3Diff — partly falsified: v3.1 has reachable-command false negatives and non-executable leads

## Findings

### P1 — Recursive helper call with a literal shell string is silently dropped

`spawn_scan` detects a helper already on `ctx["stack"]` and calls only `helper_argv_leads` (`tools/mado-tripwire.py:2107-2110`). That helper recognizes literal argv lists, not literal shell-command strings. It does not sweep/re-evaluate the recursive body with the recursive call's binding, although the module doc says recursive calls are swept as leads.

- Reproduce from the lane repo root:
  ```sh
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/recursive-argument.jsonl
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tools/mado-tripwire.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/recursive-argument.jsonl
  ```
- Input: `../../../../../tmp/mado-r20a2-ReviewV3Diff/recursive-argument.jsonl`, SHA-256 `c4f7c2a31483c5d624df1166e41225235e6e6920bfd621921d161bd27e2a36dc`.
- Observed: 28c6837 reports `host_mutation / pacman:-S / pacman -S pkg / observed` (exit 1); a8960de reports `MADO_TRIPWIRE: clean`, `findings=[]`, exit 0.
- Expected under the v3.1 recursive-call rule: the reachable recursive call's command is at least a `lead` row (`pacman -S pkg`), not a clean verdict. The branch condition is true for the initial literal `safe`, then the recursive call reaches the literal `pacman -S pkg` command.

### P1 — Sweeping a callback discards known module-level literal recipes

`sweep_body` builds its call snapshots with an empty literal environment (`tools/mado-tripwire.py:2019-2030`). Consequently a callback that reads a straight-line module-level literal loses the exact value the module doc says is resolvable; its `subprocess.run(argv)` becomes an unparsed spawn instead of the documented lead.

- Reproduce from the lane repo root:
  ```sh
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/callback-global.jsonl
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tools/mado-tripwire.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/callback-global.jsonl
  ```
- Input: `../../../../../tmp/mado-r20a2-ReviewV3Diff/callback-global.jsonl`, SHA-256 `69180c364d31b04731d3546a3dcd8d63b539a89da34adf3fa76965b59c8f18c2`.
- Observed: 28c6837 is clean with `unparsed_spawns=0`; a8960de is also clean, but `unparsed_spawns=1`; both have no finding.
- Expected: a8960de reports `host_mutation / pacman:-S / pacman -S pkg / lead` with `unparsed_spawns=0`; `argv` is assigned a literal list in the same cell before the callback is handed to `Thread`.
- Control: with the same callback using the inline literal rather than `argv`, a8960de reports the expected lead. Input `../../../../../tmp/mado-r20a2-ReviewV3Diff/callback-inline.jsonl`, SHA-256 `a2833d74dbd9b90f8a3cbb2aab229aecfb6249b43ad9b5545324e28330e95c2e`; 28c6837 is clean, a8960de reports `pacman -S pkg / lead`.

### P2 — Read-only `globals()` on the left side of a comparison clears known bindings

`namespace_read_only` accepts a `Compare` only when the call is in `parent.comparators`, not when it is `Compare.left` (`tools/mado-tripwire.py:1428-1440`). `opaque_statement` then treats `globals() == {}` as opaque and clears the literal and callable bindings before the following spawn (`tools/mado-tripwire.py:1453-1475`, `1887-1890`). The comparison only reads the returned mapping; it cannot rebind names.

- Reproduce from the lane repo root:
  ```sh
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/namespace-read.jsonl
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tools/mado-tripwire.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/namespace-read.jsonl
  ```
- Input: `../../../../../tmp/mado-r20a2-ReviewV3Diff/namespace-read.jsonl`, SHA-256 `ac999fa2f0578d64385d41137a3e3b35a056dc170cad8160e0eaadcfeb77c2da`.
- Observed: both revisions say clean with `findings=[]` and `unparsed_spawns=1`.
- Expected at a8960de: `host_mutation / pacman:-S / pacman -S pkg / observed`, because `cmd` is a known literal and the intervening comparison is read-only.
- Control: reversing the comparison to `{} == globals()` is recognized by a8960de and emits that observed finding. Input `../../../../../tmp/mado-r20a2-ReviewV3Diff/namespace-right.jsonl`, SHA-256 `ac6b6006d6ca5a74a6adfc72efd5edabd29411bbef3be7a9f07d87322f6d9345`.

### P2 — A helper handed to a known-pure builtin is reported as executable

The reference pass sweeps every visible helper reference without considering its receiving call (`tools/mado-tripwire.py:2209-2218`). Thus passing a function to `print` emits a lead even though `print` is explicitly a pure, non-callback builtin and only formats the function object.

- Reproduce from the lane repo root:
  ```sh
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/inert-function-value.jsonl
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tools/mado-tripwire.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/inert-function-value.jsonl
  ```
- Input: `../../../../../tmp/mado-r20a2-ReviewV3Diff/inert-function-value.jsonl`, SHA-256 `3bc6ff3d23193c643773e35f894432d6a0039bdc1ef474a265ef040119f3fa48`.
- Observed: 28c6837 is clean; a8960de emits `host_mutation / pacman:-S / pacman -S pkg / lead` (exit 1).
- Expected: clean; `print(dormant)` does not invoke `dormant` or hand it to a callback.

### P2 — A class callback sweeps unrelated ordinary methods

The class-reference branch passes a referenced `ClassDef` to `sweep_body` (`tools/mado-tripwire.py:2219-2220`); that path sweeps every class method (`tools/mado-tripwire.py:2017-2018`, `2036-2052`). A scheduled class target is invoked as a constructor; it does not call arbitrary ordinary methods.

- Reproduce from the lane repo root:
  ```sh
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tw-28c6837.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/class-target.jsonl
  python3 -I ../../../../../tmp/mado-r20a2-ReviewV3Diff/tools/mado-tripwire.py --scan ../../../../../tmp/mado-r20a2-ReviewV3Diff/class-target.jsonl
  ```
- Input: `../../../../../tmp/mado-r20a2-ReviewV3Diff/class-target.jsonl`, SHA-256 `07fce5221971366cbb6edb1ffbd4ad698f89752b7d50a02e55d221770b4a54fd`.
- Observed: 28c6837 is clean; a8960de emits `host_mutation / pacman:-S / pacman -S pkg / lead`.
- Expected: clean. `threading.Thread(target=C).start()` instantiates `C`; the `never_called` method containing the command is not called.

## Limits

- Iterative eager-walk order control passed: for nested ordinary calls, both revisions emit `pacman -S outer` then `pacman -Q`; input `../../../../../tmp/mado-r20a2-ReviewV3Diff/eager-order-nested.jsonl`, SHA-256 `5b5b4246f24d701fecb855e7051a7b1fb52b4e25f99f8403cb36b5a33177cc4a`. Both also preserve the sequential three-call order in `eager-order.jsonl` (SHA-256 `a7b12b39759cc658a8b1fb6e781e2cf71f0d9a88ab5751bdbeff2605d3687021`).
- Targeted saturation controls passed: a 5-body helper chain yields a `lead` at a8960de (old revision clean), input `saturation-depth.jsonl`, SHA-256 `1278a2db1e16a088ce4c30e6f2f095ae64576f0033f7edab36b5ce90a885a957`; 2000 distinct followed helper calls followed by a final helper also yields a `lead` at a8960de, input `saturation-budget.jsonl`, SHA-256 `27a5613fed00186c16cffa8762e6374652e4a10816d410972cf853510f1b0b41` (28c6837 reports the same command as observed). These are targeted controls, not exhaustive stress tests.
- No `lsp` device/server is mounted: `read xd://lsp` returned “No such tool”; grep was used only to locate routine names, not as semantic proof. No build, suite, or formatter was run. The listed commands scan inert JSONL fixtures only; their transcript code was not executed.

## Installs

none

# RevengeEnvBug — partly falsified: both draft patches drop `env` initialization, but 28c6837 restores it

## Reconstructed contract

For an `eval` tool call with a string `code`, `scan_file` always calls `classify_eval`. Non-Python languages are intentionally short-circuited by `classify_eval` to `([], 1, 0)`; they must therefore reach it with ordinary arguments, including an initialized `env` (which is not used on that early-return path).

The drafts violate that caller contract: they initialize `bindings` unconditionally but assign `env` only for `language in (None, "py", "python")`, then pass `env` unconditionally. On a first JavaScript eval in a file, Python raises `UnboundLocalError` while evaluating the call arguments in `scan_file`, before entering `classify_eval`. This is order-sensitive: a prior Python eval in the same `scan_file` invocation assigns the function-local `env`, so it masks the unbound access on a later JS cell (that stale value is unused because `classify_eval` returns immediately).

This defect is present in **both** draft artifacts, not just `TwRuleB-v2.patch`: `TwRuleB.patch:799-809` and `TwRuleB-v2.patch:840-850` each replace the prior `env = None` with `bindings = None`, keep `env` assignment inside the Python-only branch, and call `classify_eval(..., env, bindings)` outside it. The committed 28c6837 source has the missing default restored as `env = bindings = None` (`tools/mado-tripwire.py:2045-2053`), so the described JS-cell `UnboundLocalError` is not present in that commit.

## Evidence chain

- Draft change, base patch: `.ufo/waves/round-20/w1/patches/TwRuleB.patch:795-810` shows `- env = None`, `+ bindings = None`, the conditional `env = envs.setdefault(...)`, then the unconditional call.
- Same defect in v2: `.ufo/waves/round-20/w1/patches/TwRuleB-v2.patch:836-850` shows the same control-flow change. Thus the relevant hunk does not distinguish v2 from the base draft.
- Committed caller: `tools/mado-tripwire.py:2045-2053` initializes both names before the language test. The exact-source check was:

  ```text
  $ git -C /home/vgpnk/Projects/shokunin/mado-shokunin show -L :scan_file:tools/mado-tripwire.py 28c6837
  ...
  language = args.get("language")
  env = bindings = None
  if language in (None, "py", "python"):
      ...
      env = envs.setdefault("py", {})
      bindings = binding_envs.setdefault("py", {})
  hits, un_eval, un_spawn = classify_eval(code, language, env, bindings)
  ```

- The byte identity check tied the checked-in source to 28c6837: `git show 28c6837:tools/mado-tripwire.py | sha256sum` returned `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c  -`; `sha256sum tools/mado-tripwire.py` returned the same digest. `git rev-parse 28c6837:tools/mado-tripwire.py` returned blob `5f0bac585cd02457fa970e495ae2940983a69de7`.
- The relevant `classify_eval` flow at `tools/mado-tripwire.py:1765-1796` returns for a truthy non-Python language at lines 1767-1768, before it uses `hits`, `env`, or `bindings`; on the parsing path it initializes `hits`, catches compilation failures with a return, normalizes `env` and `bindings`, destructures `prepare_eval_calls`, then destructures `spawn_scan` before use.
- Artifact digests: `TwRuleB-v2.patch` SHA-256 `be214cfcc7574f524470ff394aeb2629adc70fe0070fcf3f0866906e0d992277`; `TwRuleB.patch` SHA-256 `9d3487c68ea8e9ffd5ed094890d76261ae1fdff4b8d64ef947aa128d8412782e`; committed tool SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`.

## Other unbound-local audit at 28c6837

Static control-flow review of `scan_file` and `classify_eval` found no other local that can be read before assignment on a reachable branch:

- In `scan_file`, `code` is assigned before its string guard; a non-string code takes `continue` before `language`, `env`, or `bindings` are used. On every string eval, `language`, `env`, and `bindings` are assigned before the classifier call. `hits` is assigned in the `bash` branch or by `classify_eval` in the `eval` branch; all other tool names `continue`. `un_eval` and `un_spawn` are consumed only after the eval call assigned them. `cmd` is branch-local to `bash` and is initialized from `args` before use. The non-eval branches that skip classification also continue before `hits` is consumed.
- In `classify_eval`, a non-Python language returns before `hits` or parse locals are read. Remaining paths initialize `hits`, `lines`, and `py`; regex match `m` is assigned each loop iteration before its truth test; compile failure returns; and the successful path assigns all destructured return values before use.

## Confidence

High for the patch/source comparison and reachable local-variable dataflow. The JS failure mechanism in the draft follows directly from the shown branch and call; no dynamic reproduction was run. The committed 28c6837 source itself is positively checked by `git show` and the matching SHA-256, rather than inferred from the patch.

## Limits

- LSP was unavailable: `read xd://lsp` returned `No such tool: xd://lsp` and listed only the mounted REA/AST/debug devices. This report relies on the source and patch snapshots plus read-only `git show`; it does not treat grep as semantic proof.
- No program, tests, or alternate runtime was run. This was a static reconstruction only.

## Installs

none

# MadoR22.ResidualForward — final residual review (author-lane advice, not admission)

Reviewed delivered revision `4d308e5e`; tool sha256 `a9532373…c82da`, working tree matches HEAD. Prior reds and streak unchanged. No code, fixture or expectation edited.

## Observed: the target fixture passes

One scan via existing `round-21/oracle/measure.py::scan` (384 MiB, 15 s), fixture `d3d8222a…c5e1f94b1`:

- exactly one row, `{package_query, "pacman -Q r22-forward-global", observed}`;
- no `pacman -S r22-forward-foreign` at any tier;
- `eval_unparsed` 0, `unparsed_spawns` 0; exit 1.

This matches the exact expectation. At v2 (`8c74209`) the case was red with `unparsed_spawns` 1 from a redundant sweep.

## Source-only gaps (not probed; `[INFERENCE]`)

1. **Callback invoked inside the forwarder reads the forwarder's frame.** `follow_helper` (lines 2434–2438) starts the callee body from `dict(cenv)`, the caller's snapshot, instead of module globals.
   - Neighbour: `def forward(argv, callback): callback()` resolves `run`'s free `argv` to `forward`'s parameter.
   - Effect: invented observed `-S r22-forward-foreign`, true `-Q` row lost.
   - The v3 check (line 1676) restricts only *returned* overlays. This mechanism is older but falsifies the LOG claim "fixes the actual ownership distinction". Axes: precision, recall, calibration.

2. **v3 sweep suppression loses recall.** Lines 2575–2578 and 2729 skip the outer callback sweep whenever the consumer was followed with zero unparsed and no opaque statement. `eager_calls` (lines 2072–2083) records a Name only as a direct call argument, so stores like `hooks["k"] = cb` or `obj.cb = cb` leave no trace.
   - Neighbour: `register(run); hooks["k"]()` gave a `lead` at v2 and gives zero rows, zero unparsed at v3.
   - `supported-forms.md` line 18 forbids certifying visible callback bodies safe by absence of a finding. No frozen input guards this.

3. **Provenance gap.** All committed 57/57, ownership and 46/46 evidence was measured at `8c74209` (tool `cd9da20c…`). Nothing measures delivered tool `a9532373…` except this receipt.

## Smallest safe corrections

- Gap 1: build the callee environment from its defining frame (module globals plus own closure), never `cenv`.
- Gap 2: resolve a consumer only when the followed body has no escaping store or return of the parameter; otherwise keep the sweep.
- Freeze both neighbours before patching, then re-measure 57 + 4 + 46 at the delivered sha.

## Receipts

`.ufo/waves/round-22/residual/ResidualForward/`; before and after digests identical (tool, helper, fixture, expectations, HEAD unmoved).

| File | sha256 |
|---|---|
| `scan-result.json` | `ab066c93…5605b65` |
| `digests-before.txt` / `digests-after.txt` | `886a6b0a…7113` |

No installs; no other scanner runs.

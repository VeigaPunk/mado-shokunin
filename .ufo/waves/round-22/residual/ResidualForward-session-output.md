`ForwardExistingClosureWithoutFrameContamination` passes at the delivered revision `4d308e5e` (tool sha256 `a9532373…c82da`). The scanner reported exactly one row, observed `pacman -Q r22-forward-global`, with no `pacman -S r22-forward-foreign` row and zero unparsed. Reading the source still turns up two counterexamples and a provenance gap, so prior reds and the streak stand. This is author-lane advice, not admission.

**The run:** one scan through the existing round-21 helper `round-21/oracle/measure.py::scan` (384 MiB, 15 s cap). The scanner exited 1, which the measure counts as success, and both unparsed counters were 0. At the previous revision `8c74209` this case was red, with one unparsed spawn from a redundant sweep. Digests taken before and after the run match, so the tool, helper, fixture, expectations and HEAD did not move.

**Gaps found by reading the code, not probed:**

1. **A callback invoked inside the forwarder still reads the forwarder's locals.** In `follow_helper` (lines 2434–2438) the callee body starts from a copy of the caller's environment instead of module globals.
   - The neighbouring case is the fixture with `def forward(argv, callback): callback()`. The callback's free `argv` would resolve to `forward`'s parameter.
   - That would produce an invented observed `pacman -S r22-forward-foreign` and lose the true `-Q` row.
   - The new ownership check (line 1676) only covers *returned* helpers. This mechanism is older, but it contradicts the `LOG.md` claim that the change "fixes the actual ownership distinction".
   - Affected axes: C1 precision, recall and calibration.

2. **The new callback-sweep suppression loses recall.** Lines 2575–2578 and 2729 skip the outer sweep of a passed callback whenever the consumer was followed with zero unparsed and no opaque statement.
   - The problem: `eager_calls` (lines 2072–2083) only records a name as a reference when it is a direct call argument. A consumer that stores the callback, such as `hooks["k"] = cb` or `obj.cb = cb`, leaves no trace.
   - Neighbouring case: `register(run); hooks["k"]()`. It produced a lead at `8c74209` and would produce zero rows and zero unparsed now.
   - `supported-forms.md` line 18 forbids treating a visible callback body as safe because no finding appeared. No frozen input covers this form.

3. **No committed measurement of the delivered tool.** The committed 57/57, 46/46 and ownership-replay evidence was all measured at `8c74209` (tool sha `cd9da20c…`). The delivered tool sha `a9532373…` appears only in this review's receipts.

**Smallest safe corrections:**
- Build the callee's environment from where it was defined (module globals plus its own closure), never from the caller.
- Mark a consumer as resolved only when its followed body neither stores nor returns the callback parameter; otherwise keep the sweep.
- Freeze both neighbouring cases before patching, then re-measure the 57, the 4 supplemental cases and the 46 at the delivered sha.

I made no code or fixture edits, ran no other scans and installed nothing.

Files are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/residual/`:
- `ResidualForward.md` (389 words)
- `ResidualForward/scan-result.json`
- `ResidualForward/digests-before.txt`
- `ResidualForward/digests-after.txt`
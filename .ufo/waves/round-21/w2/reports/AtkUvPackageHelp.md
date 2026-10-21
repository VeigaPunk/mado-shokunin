# AtkUvPackageHelp — C1 review

## Axes

- **C1 semantic truth:** whether the frozen `UvPackageHelp` class, command, and evidence are warranted.
- **C1 rule generality:** whether the repair follows command structure rather than the fixture's literal text.
- **C1 nearby falsification:** one adjacent argument-order variant.
- **C2:** separate artifact-only assessment; not assessed here.

## Finding — P2 / medium

**The help exemption misses `--help` before a package operand, producing an adjacent false positive.** I retained one inert variant at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkUvPackageHelp-2/uv-help-before-package.jsonl` (SHA-256 `6881e7be1332e4730837139bdef082b224c0dc61990a7f99a233d1f52373ccac`):

```text
uv tool run --help package-not-executed
```

The pinned upstream uv 0.13.4 `tool_run_args` test explicitly establishes that `.arg("--help").arg("pytest")` prints uv's own tool-run help, before it resolves or runs the target; this ordering therefore does not acquire a package ([upstream test](https://github.com/astral-sh/uv/blob/0.13.4/crates/uv/tests/tool/tool_run.rs#L28-L47)). But the current scanner returned exit 1 with an observed `tool_install` finding (`uv:tool-run`) for this inert transcript. The guard in `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1019-1023` requires exactly two positionals, so the later package token prevents the exemption even though the earlier help option is consumed by uv. This is a concrete adjacent false positive; it does not undermine the frozen trailing-help expectation. Do not alter the frozen expectation on this basis.

## Frozen-case ruling and generality

Reviewed current candidate commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, with `tools/mado-tripwire.py` SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`.

**Affirm the frozen `UvPackageHelp` expectation.** The row expects `tool_install`, command `uv tool run package-not-executed --help`, evidence `observed` (with proposal class `install` normalized to the public class). The transcript at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/UvPackageHelp.jsonl` is one direct bash tool call with exactly that command. The same upstream test distinguishes the orderings: `.arg("--help").arg("pytest")` prints uv's own help, while `.arg("pytest").arg("--help")` prints pytest help and records package resolution, preparation, and installation. The tagged tools guide also says `uv tool run` invokes a tool in a temporary isolated environment and accepts tool arguments after its name ([guide](https://github.com/astral-sh/uv/blob/0.13.4/docs/guides/tools.md#L15-L56)). Thus the trailing `--help` does not make this package-taking run uv's own help. The expected class describes the acquisition-capable command path; it does not claim this placeholder resolves or that the exact command was run. `observed` is appropriate for the direct command present in the transcript. This is not a VCS-write claim.

The repair is structural, not fixture-text keyed: it classifies `uv:tool-run`, then exempts a help invocation only when `leading_tokens` finds exactly the `tool run` pair and no `--from`/`--with` selectors. A package operand plus trailing help yields a third positional token and remains classified. The exact placeholder string and case ID are not consulted.

With the current scanner, a bounded scan of the frozen case (input SHA-256 `1959c76b88bd635ae57cf4472a69b9353446ce53cc9a52ad615de91ef823dae4`) returned exit 1 with exactly one observed `tool_install` finding, rule `uv:tool-run`, command `uv tool run package-not-executed --help`, and no unparsed spawns. That matches the frozen wanted row.

## Residual risk and verification gaps

- Both scans used the existing `measure.py` `scan` API, which launches one scanner child per call with its 384 MiB address-space cap and 15-second timeout. No transcript command, Python/shell payload, uv command, package manager, or package was executed; no full suite/corpus was run.
- No LSP device/server was exposed: requesting `xd://lsp` returned `No such tool`. Therefore no LSP references, definition, or diagnostics results are claimed; the code-path conclusion above is from the directly read classifier source, and the semantic conclusion is from the upstream test/docs.
- No tools were installed or updated.
- The exact placeholder's registry resolution and resulting filesystem effects remain unmeasured, consistent with the frozen expectation's scope.

Report: .ufo/waves/round-21/w2/reports/AtkUvPackageHelp.md

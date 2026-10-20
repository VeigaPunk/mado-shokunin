# RevToolDiffLeads — partly falsified: pure data can become a failing lead, and first-wins dedup loses distinct rows

## Findings

### Medium — opaque reset turns an unchanged builtin call into a lead (new regression)

`vars()` followed by the builtin `print(["pacman", "-Q", "hyprland"])` produces a lead for `pacman:-Q`, although the transcript does not rebind `print` or call a command-spawning function. The lead alone makes the scan exit 1. The same fixture scanned by the pre-repair tool at `1f7f995` exits 0 with no row.

Evidence:

- `tools/mado-tripwire.py:1217-1219` includes `vars` among opaque calls. `tools/mado-tripwire.py:1744-1748` clears bindings and explicitly rebinds every `PURE_ARG_CALLS` name as `unknown`; `print` is in that set (`:1396-1406`). `tools/mado-tripwire.py:1874-1878` sends `unknown` Name calls to `helper_argv_leads`; `:1802-1806` classifies the literal argv as a lead. `verdict_of` counts leads like other findings (`:2090-2095`).
- Fixture `/tmp/mado-r20w2-RevToolDiffLeads/fixtures/f2-opaque-pure-lead.jsonl` (SHA-256 `8b1c8dec561edbe990db76db7539bbd8298d6c2a97afb84ccb5ad4f019981fe1`), code: `vars()` then `print(["pacman", "-Q", "hyprland"])`. The corresponding no-`vars()` control was clean.
- Command: `python3 -I /tmp/mado-r20w2-RevToolDiffLeads/tools/mado-tripwire.py --scan /tmp/mado-r20w2-RevToolDiffLeads/fixtures/f2-opaque-pure-lead.jsonl` → `exit=1 obs=0 lead=1; package_query/pacman:-Q/lead, command="pacman -Q hyprland"`. Same command with `/tmp/old-tripwire-1f7f995.py` → `exit=0 rows=[]`.
- The target tool SHA-256 is `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`; pre-repair tool SHA-256 is `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.

This contradicts the documented no-row rule for builtins not rebound in the text (`corpus/knowledge/tripwire-precision-r20.md:20,30-32`; `SKILL.md:552-553`). The fixture's `vars()` result is discarded and `print` is the known builtin, not a spawn; treating this as a pure/non-command call is an inference from the source and Python builtin behavior. The opaque reset is conservatively fail-closed, but here it creates a new false lead and a failing verdict.

### Medium — a pure standard-library call imported by name is emitted as a lead

`from heapq import nlargest; nlargest(3, ["pacman", "-R", "linux"])` emits a `host_mutation/pacman:-R` lead and exits 1. This is a valid call to a standard-library selector over literal data; it does not spawn a process. `[INFERENCE]` `heapq.nlargest` with these arguments is a pure data operation.

Evidence:

- The pure whitelist at `tools/mado-tripwire.py:1408-1414` omits `heapq`. `update_bindings` therefore classifies an unrecognized `ImportFrom` path as `external` (`:1566-1577`); the lead branch applies to Name calls of kind `external` (`:1874-1878`).
- Fixture `/tmp/mado-r20w2-RevToolDiffLeads/fixtures/f1b-pure-heapq-lead.jsonl` (SHA-256 `eb1d3f7367c7bc1405ac03326435506d142ac35b1da79d9da60e986085fe52f6`). Current command output: `exit=1 findings=[host_mutation, pacman:-R, lead, "pacman -R linux"]`.
- The pre-repair tool also emitted the row (`exit=1`, same class/rule/command, but without an evidence marker). Thus this is a gap in the claimed pure-stdlib/no-row contract and evidence classification, not a new row-count regression.

The report says a lead can come from an import of a *non-stdlib* module (`corpus/knowledge/tripwire-precision-r20.md:19`; `SKILL.md:548-553`), while this bare import is standard library. The current recognition is a finite whitelist, narrower than the prose claim.

### Low — per-call first-wins dedup drops distinct observed commands with the same class/rule

A single eval tool call containing `subprocess.run(["pacman", "-Q", "hyprland"])` followed by `subprocess.run(["pacman", "-Q", "linux"])` emits only the first row. The second distinct observed command is absent, because the dedup key excludes argv and command text and preserves only the first value for a key.

Evidence:

- `scan_file` creates `unique_hits` inside the tool-call loop, keys it by `(cls, rule, evidence)`, and inserts only when the key is new (`tools/mado-tripwire.py:2030,2060-2067`).
- Fixture `/tmp/mado-r20w2-RevToolDiffLeads/fixtures/f3-dedup-observed-loss.jsonl` (SHA-256 `d391006d7e1e750b5b192d12f57bf4a64a662d8f35035a7a146ccb53cddbcd85`) → `exit=1 obs=1 lead=0`, sole command `pacman -Q hyprland`; no row for `pacman -Q linux`.
- Scanning the same fixture with the pre-repair tool yields the same one-row result. The old dedup key was `(cls, rule)`; the round-20 diff adds `evidence` but retains first-wins. This is a real per-call information loss, but not introduced by this repair.

The added evidence field does prevent a lead from colliding with and suppressing an observed row. Reverse-order control `/tmp/mado-r20w2-RevToolDiffLeads/fixtures/f5b-lead-before-observed.jsonl` (SHA-256 `1ddddb452cb54a6cc3ae18f5e9e8ceff5211660cd734f493e41116736c3fa90d`) yields both `lead pacman -Q hyprland` and `observed pacman -Q linux`; the old tool yielded only the first unmarked row.

## Direct answers / holds

- **Can a lead be emitted twice?** Not twice for the same `(class, rule, evidence)` within one tool call: first-wins dedup collapses it. Fixture `f4-lead-dedup-two-commands.jsonl` (SHA-256 `67a4731b82237c494f1c8bff8cab1bde7d2269189568c7b550dfe5a7b00e9e22`) has two same-rule leads in one call and emits one. But identical leads in distinct tool calls are both emitted, correctly attributed to their separate IDs: fixture `f4b-separate-toolcalls-two-leads.jsonl` (SHA-256 `c7b8c2f1dfb44361d0afffcfe17302e0f963f27d9c8ecb738cb1caa97092a233`) → `leads=2`, IDs `c1`, `c2`. I found no duplicate emission from one call site/path.
- **Can an observed row be lost by dedup?** Yes, when two distinct observed commands in one call share class/rule/evidence (above). No, a same-class/rule lead does not erase an observed row merely by ordering: the key includes `evidence`, confirmed with the lead-first control.
- **Can a pure call produce a lead?** Yes: the opaque-reset builtin case is a new regression; the pure `heapq.nlargest` import case exposes the whitelist/prose gap, with the finding row predating this repair.

## Residual risk

- The changed binder does correctly resolve explicit varargs across eval cells: `/tmp/mado-r20w2-RevToolDiffLeads/fixtures/helper-cross-cell-vararg-control.jsonl` (SHA-256 `da9fb8d69bc7ac187fb7b76ed1352959eaa8a5827bf6800acb762cc07d6c8c7d`) produced one observed `pacman:-Q` row; the pre-repair tool produced none. However, call-site starred expansion remains unsupported: `bind_literal` returns `None` for any `ast.Starred` argument (`tools/mado-tripwire.py:1677-1678`). A valid helper call `run(*[["pacman", "-Q", "hyprland"]])` whose body passes its parameter to `subprocess.run` produced no row in either version. This is an inherited helper-resolution miss, not a round-20 regression.
- Frozen replay compares `(file, line, class, rule)` and not `evidence` (`tools/mado-tripwire.py:2438-2446`). Consequently, a frozen match does not establish that a row retained the correct observed/lead classification.

## Verification gaps

Targeted scans only; I did not run the full precision/recall/selftest suites or the whole-corpus no-harm diff. The scorecard itself records that whole-corpus diff as pending (`SCORECARD.md:1330`). No claim is made about those checks.

## Installs

none

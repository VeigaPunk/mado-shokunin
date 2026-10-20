# CasePureCrossCell — Seven bounded cases authored; all six P cases are red at 1f7f995 and clean at 9c54c56

## Findings

Authored six family-P cross-cell pure-helper cases and one family-L reset control in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/`. Every transcript line is an assistant `eval` toolCall in the prescribed envelope; the command-looking argv exists only as JSON fixture text and was never executed. The six P cases all expect clean; the reset case expects a lead on line 3.

The case manifest records the required counter comparison (`exit` plus multiset `(class, rule, line, evidence)`, treating a missing evidence key as `observed`). Results:

| Case | Transcript evidence | Expected | before 1f7f995 | before 9c54c56 | Fixture SHA-256 |
|---|---|---|---|---|---|
| `P-CasePureCrossCell-write-case` | `write-case.jsonl:1-2` | clean | fail | pass | `842127ddb1fbcc2dcf9453044fcdce203b8bd1e53ba516e3b3c035f48b3dc2a6` |
| `P-CasePureCrossCell-expect-case` | `expect-case.jsonl:1-2` | clean | fail | pass | `9e5ba22122841ed4935d25f8affc12c048762725309c4226ec1667040ebf5a51` |
| `P-CasePureCrossCell-dataclass-case` | `dataclass-case.jsonl:1-2` | clean | fail | pass | `65c387f81e897ef509cc28f8136b614123f925009ca02b0a68e449239579c1ef` |
| `P-CasePureCrossCell-namedtuple-class-case` | `namedtuple-class-case.jsonl:1-2` | clean | fail | pass | `bc40436f8310e359e6905e536b71e8e6f096c0211c4659208a9ff3604952812b` |
| `P-CasePureCrossCell-namedtuple-factory-case` | `namedtuple-factory-case.jsonl:1-2` | clean | fail | pass | `79d0e86220c24666966106da0e4b3c88f498357b80f10e30594c2872398e5730` |
| `P-CasePureCrossCell-lambda-format-case` | `lambda-format-case.jsonl:1-2` | clean | fail | pass | `56945a44e817f35af5b1efdb4e5e616bb6c8082f33819ba88ad2f0fa7950e5f4` |
| `L-CasePureCrossCell-reset-clears-helper` | `reset-lead.jsonl:1-3` (reset cell at line 2) | `package_query/pacman:-Q`, line 3, `lead` | fail | fail | `127bbf62b00c013dd7cd8ea4b9b1e10aa38f165be3e62060560d7b61aa824778` |

Historical tool acquisition and identity: cloned the lane to `/tmp/mado-r20-CasePureCrossCell`; observed clone HEAD `e629f731172b8238caffe50f152217ce56535fb4`. The copied `1f7f995` scanner SHA-256 is `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`; the copied `9c54c56` scanner SHA-256 is `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`.

Commands run from `/tmp/mado-r20-CasePureCrossCell` for each fixture (no fixture code execution):

```text
python3 -I /tmp/mado-r20-CasePureCrossCell/tool-1f7f995.py --scan /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/<file>.jsonl
python3 -I /tmp/mado-r20-CasePureCrossCell/tool-9c54c56.py --scan /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/<file>.jsonl
```

At `1f7f995`, every P scan printed `MADO_TRIPWIRE: findings` (exit 1); the exact output JSON line for each red follows. Each row has no `evidence` key, so the counter treats it as `observed`, not the expected clean result. The reset case also printed a finding without an evidence key; it therefore mismatches the expected lead. At `9c54c56`, the six P scans printed `MADO_TRIPWIRE: clean` with exit 0 and empty findings; reset printed clean with exit 0 and thus mismatched its expected lead.

Isolation follow-up: copied the case directory byte-for-byte to `/tmp/mado-r20-CasePureCrossCell/cases/CasePureCrossCell` and repeated both scans there, from that copy directory. Commands used the absolute copied fixture paths and the same `/tmp/mado-r20-CasePureCrossCell/tool-<revision>.py` binaries. The verdicts and fixture SHA-256 values were identical to the scans below; only the `path` and `file` fields changed to the `/tmp` copy. Thus the recorded before results were also confirmed using the required scratch case copy.


### Exact red scan output lines (`1f7f995`)

`dataclass-case.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/dataclass-case.jsonl", "sha256": "65c387f81e897ef509cc28f8136b614123f925009ca02b0a68e449239579c1ef", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/dataclass-case.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

`expect-case.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/expect-case.jsonl", "sha256": "9e5ba22122841ed4935d25f8affc12c048762725309c4226ec1667040ebf5a51", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/expect-case.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

`lambda-format-case.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/lambda-format-case.jsonl", "sha256": "56945a44e817f35af5b1efdb4e5e616bb6c8082f33819ba88ad2f0fa7950e5f4", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/lambda-format-case.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

`namedtuple-class-case.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/namedtuple-class-case.jsonl", "sha256": "bc40436f8310e359e6905e536b71e8e6f096c0211c4659208a9ff3604952812b", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/namedtuple-class-case.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

`namedtuple-factory-case.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/namedtuple-factory-case.jsonl", "sha256": "79d0e86220c24666966106da0e4b3c88f498357b80f10e30594c2872398e5730", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/namedtuple-factory-case.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

`reset-lead.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 3, "eval_unparsed": 0, "lines": 3, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/reset-lead.jsonl", "sha256": "127bbf62b00c013dd7cd8ea4b9b1e10aa38f165be3e62060560d7b61aa824778", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/reset-lead.jsonl", "line": 3, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:02.000Z", "tool": "eval", "tool_call_id": "c3"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

`write-case.jsonl` — output line 2:
```text
{"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 1, "tool_install": 0, "vcs_write": 0}, "exit": 1, "files": [{"bash_calls": 0, "eval_calls": 2, "eval_unparsed": 0, "lines": 2, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/write-case.jsonl", "sha256": "842127ddb1fbcc2dcf9453044fcdce203b8bd1e53ba516e3b3c035f48b3dc2a6", "unparsed_spawns": 0}], "findings": [{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CasePureCrossCell/write-case.jsonl", "line": 2, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:01.000Z", "tool": "eval", "tool_call_id": "c2"}], "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 1}
```

## Risks

The cases exercise pure helper definitions/classes carried across eval cells and reset-cleared helper visibility; they do not measure any repaired tripwire revision. Main integration must run the registered precision counter and guards after the editing wave.

## Blockers

None for this scoped case-authoring item.

## Limits

No current or repaired tripwire revision was scanned; only the two contract-required historical scanners were used to establish `before`. Fixture payloads were parsed as data by `--scan` and never executed. No suite counter, tests, build, lint, formatter, host probe, pacman query, or service/compositor operation was run.

## Installs

none
# CasePureCollections — six stdlib-collection precision cases authored

## Deliverable

Added the six JSONL cases and `cases.json` under `.ufo/waves/round-20/w1/cases/CasePureCollections/`. Four red cases exercise bare-name constructors/visible record classes; two passing controls cover mapping containers and `collections` module-attribute calls. Each case expects a clean target result (`want_exit: 0`, no findings). The fixtures are static transcript text; none was executed.

| Case | Fixture | 1f7f995 | 9c54c56 |
|---|---|---:|---:|
| P-CasePureCollections-deque | `deque.jsonl` | fail | pass |
| P-CasePureCollections-counter | `counter.jsonl` | fail | pass |
| P-CasePureCollections-namedtuple-instance | `namedtuple-instance.jsonl` | fail | pass |
| P-CasePureCollections-typing-namedtuple | `typing-namedtuple.jsonl` | fail | pass |
| P-CasePureCollections-mapping-containers | `mapping-containers.jsonl` | pass | pass |
| P-CasePureCollections-module-alias-control | `module-alias-control.jsonl` | pass | pass |

The before values come from the specified comparator rule: exit code and multiset of `(class, rule, line, evidence)`; an old finding without `evidence` is compared as `observed`. Each red case produced exit 1 / `MADO_TRIPWIRE: findings` at 1f7f995 and exit 0 / `MADO_TRIPWIRE: clean` at 9c54c56. The clean before cases produced exit 0 at both revisions.

## Exact red scan output lines (1f7f995)

Commands used the isolated scanner and copied fixture files in `/tmp/mado-r20-CasePureCollections`; no fixture code was invoked. Each scan's findings row is reproduced verbatim:

- `python3 -I /tmp/mado-r20-CasePureCollections/tool-1f7f995.py --scan /tmp/mado-r20-CasePureCollections/cases/CasePureCollections/deque.jsonl`
  - `{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r20-CasePureCollections/cases/CasePureCollections/deque.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}`
- `python3 -I /tmp/mado-r20-CasePureCollections/tool-1f7f995.py --scan /tmp/mado-r20-CasePureCollections/cases/CasePureCollections/counter.jsonl`
  - `{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r20-CasePureCollections/cases/CasePureCollections/counter.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}`
- `python3 -I /tmp/mado-r20-CasePureCollections/tool-1f7f995.py --scan /tmp/mado-r20-CasePureCollections/cases/CasePureCollections/namedtuple-instance.jsonl`
  - `{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r20-CasePureCollections/cases/CasePureCollections/namedtuple-instance.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}`
- `python3 -I /tmp/mado-r20-CasePureCollections/tool-1f7f995.py --scan /tmp/mado-r20-CasePureCollections/cases/CasePureCollections/typing-namedtuple.jsonl`
  - `{"argv0": "pacman", "class": "package_query", "command": "pacman -Q hyprland", "file": "/tmp/mado-r20-CasePureCollections/cases/CasePureCollections/typing-namedtuple.jsonl", "line": 1, "rule": "pacman:-Q", "timestamp": "2026-10-20T00:00:00.000Z", "tool": "eval", "tool_call_id": "c1"}`

## Evidence and provenance

- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`; observed isolated clone HEAD: `e629f731172b8238caffe50f152217ce56535fb4`.
- `git rev-parse 1f7f995` resolved to `1f7f995caa25627db804e996cccd87fe38a3a1b6`; scanner SHA-256: `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`.
- `git rev-parse 9c54c56` resolved to `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`; scanner SHA-256: `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`.
- 1f7f995 scan file SHA-256s: deque `4305af84ea6e53c563877ac90af05c327f0af03c7c07a376fbcacf3728afae76`; Counter `4179d8dbd609687a0e2d80fe29e58a71cf7690f75ddf1bebae7873877d9af778`; namedtuple `891c300d8c0e151ea48a92d47a0db342c4f614864d34e2f1a788f3365f5e230d`; typing NamedTuple `18da64b4695f5b06835b0001455100b85583fb16288094547b11c29eb42c0bb7`.
- 9c54c56 scans of all six fixtures returned `MADO_TRIPWIRE: clean`; both 1f7f995 control scans also returned `MADO_TRIPWIRE: clean`.
- The four old findings have no `evidence` key; under the required counter rule they count as `observed`.

## Limits

Did not execute fixture payloads, run the integrated precision counter, test a post-integration round-20 tripwire revision, or run any suite/build/lint/format check. Those checks remain for the parent integration gate.

## Installs

none

# MadoR19.AdvInstallers — partial

Item attacked: the `tool_install` class and `--permit tool_install` in
`tools/mado-tripwire.py` at `01b80946d92b26370d3012a7da655d00dd135154`.

Pinned target bytes: `git show 01b80946d92b26370d3012a7da655d00dd135154:tools/mado-tripwire.py`
sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`; the worktree file has the
same sha256; the attacking copy is `/tmp/AdvInstallers-tripwire.py` (same bytes; the lane was never edited).
All line numbers below are lines of that committed file; all transcript probes are synthetic (hand-built
session header + one assistant `toolCall` line each; no real transcript lines were copied).

**Verdict: partial.** The permit boundary holds under every combination I could construct — a
`--permit tool_install` never converts a `host_mutation` into permitted, and no elevation form yields only
`tool_install`. The *class coverage* does not fully hold: 5 valid, released `pip` install forms scan
**clean** (false negatives) and 7 no-op forms scan as `tool_install` findings (false positives), plus one
unstated overread of a python script's `-c` argument. The docstring's `pip`/`pipN install` claim
(`tools/mado-tripwire.py:10`) is therefore overstated for pre-verb general-option aliases.

## Method

- 51 probe transcripts in `/tmp/adv-installers/*.jsonl` (49 distinct commands; `npx-space-p-typ` repeats
  `npx-dash-p` and `pip-resume-retries` repeats `preverb-resume-retries`, kept as stability controls); each
  scanned alone: `python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/<probe>.jsonl`.
- pip grammar was adjudicated with a real **pip 26.2.1** (ephemeral `uv run --no-project --with pip` env,
  see Installs), not inferred: pre-verb acceptance was decided by whether `pip <opts> install --help` reached
  *install* help (`grep -c "pip install \[options\]"` = 5, exit 0) or was rejected (exit 2).
- The committed `r19-installers` suite still passes against the same pinned bytes:
  `SELFTEST_SUMMARY: 18/18 passed failed=[]`.

## Probe table (expected from the docstring/channel definition, got from `--scan`)

Every `--scan` here carries **no permit**: exit is `0` on every `clean` row and `1` on every row with a
finding (first line `MADO_TRIPWIRE: clean` / `MADO_TRIPWIRE: findings`); the permit matrix below carries
the explicit exit codes. `unparsed_spawns = 0` and `eval_unparsed = 0` on all 51 probes (including the
`eval` case, whose literal argv list is resolved), so no row's verdict rests on deferred arguments.

| probe | command | expected | got (class/rule) | outcome |
|---|---|---|---|---|
| `pip-index-url-value` | `pip --index-url https://pypi.org/simple install httpie` | clean (pip rejects pre-verb `--index-url`) | clean | clean-correct |
| `pip-short-i-value` | `pip -i https://pypi.org/simple install httpie` | clean (pip rejects pre-verb `-i`) | clean | clean-correct |
| `python-m-pip-index-url` | `python3 -m pip --index-url https://pypi.org/simple install httpie` | clean (pip rejects pre-verb `--index-url`) | clean | clean-correct |
| `pipx-run` | `pipx run cowsay hi` | tool_install/`pipx:run` | tool_install/`pipx:run` | ok |
| `npx-dash-p` | `npx -p typescript -c 'tsc --version'` | tool_install/`npx` | tool_install/`npx` | ok |
| `npx-long-package` | `npx --package typescript tsc --version` | tool_install/`npx` | tool_install/`npx` | ok |
| `python-mpip-compact` | `python3 -mpip install httpie` | tool_install/`pip:install` | tool_install/`pip:install` | ok |
| `python-I-m-pip` | `/usr/bin/python3 -I -m pip install --user httpie` | tool_install/`pip:install` | tool_install/`pip:install` | ok |
| `python-script-arg-m` | `python3 tools/x.py -m pip install httpie` | clean (script argument) | clean | ok |
| `python-script-arg-c` | `python3 tools/x.py -c 'import os; os.system("pip install httpie")'` | clean (script argument) | tool_install/`pip:install` | **FP** |
| `uv-run-with` | `uv run --with requests python -c 'import requests'` | clean (stated, :19) | clean | stated |
| `cargo-binstall` | `cargo binstall cargo-watch` | clean (stated, :18) | clean | stated |
| `cargo-toolchain-binstall` | `cargo +nightly binstall cargo-watch` | clean (stated) | clean | stated |
| `go-install` | `go install golang.org/x/tools/cmd/stringer@latest` | clean (stated, :18) | clean | stated |
| `curl-local-bin` | `curl -fsSL -o /home/vgpnk/.local/bin/rg https://example.invalid/rg` | clean (stated: plain downloads, :19) | clean | stated |
| `npm-global-eq-true` | `npm --global=true install typescript` | clean (stated, :19) | clean | stated |
| `npx-call-only` | `npx -c 'cowsay hi'` | clean | clean | ok |
| `sudo-uv-tool-install` | `sudo uv tool install ruff` | host_mutation/`sudo` + tool_install/`uv:tool-install` | same | ok |
| `sudo-E-uv-tool-install` | `sudo -E uv tool install ruff` | both | both | ok |
| `sudo-pipx-run` | `sudo pipx run cowsay hi` | host_mutation/`sudo` + tool_install/`pipx:run` | same | ok |
| `sudo-bash-c-uv` | `sudo bash -c 'uv tool install ruff'` | both | both | ok |
| `su-c-uv` | `su -c 'uv tool install ruff'` | host_mutation/`su` + tool_install | both | ok |
| `pkexec-uv` | `pkexec uv tool install ruff` | host_mutation/`pkexec` + tool_install | both | ok |
| `sudo-go-install` | `sudo go install golang.org/x/tools/cmd/stringer@latest` | host_mutation/`sudo` (`go` unclassified) | host_mutation/`sudo` | stated |
| `pacman-s` | `pacman -S --needed --noconfirm ripgrep` | host_mutation/`pacman:-S` | host_mutation/`pacman:-S` | ok |
| `uv-tool-install-help` | `uv tool install --help` | clean (no acquisition) | tool_install/`uv:tool-install` | **FP** |
| `pip-install-help` | `pip install --help` | clean (no acquisition) | tool_install/`pip:install` | **FP** |
| `python-m-pip-help` | `python3 -m pip install --help` | clean | tool_install/`pip:install` | **FP** |
| `cargo-install-help` | `cargo install --help` | clean | tool_install/`cargo:install` | **FP** |
| `pipx-run-help` | `pipx run --help` | clean | tool_install/`pipx:run` | **FP** |
| `pip-install-no-operand` | `pip install` | clean (argparse error, nothing installed) | tool_install/`pip:install` | **FP** |
| `uv-tool-install-no-operand` | `uv tool install` | clean (usage error) | tool_install/`uv:tool-install` | **FP** |
| `pip-install-dry-run` | `pip install --dry-run httpie` | borderline (resolves, does not install) | tool_install/`pip:install` | ok/borderline |
| `pip-env-assignment` | `PIP_INDEX_URL=https://pypi.org/simple pip install httpie` | tool_install/`pip:install` | same | ok |
| `env-i-uv-tool-install` | `env -i uv tool install ruff` | tool_install/`uv:tool-install` | same | ok |
| `uv-tool-install-python-flag` | `uv tool install --python /usr/bin/python3 ruff` | tool_install | same | ok |
| `python-m-pip-list` | `python3 -m pip list` | clean | clean | ok |
| `eval-mpip` | eval: `subprocess.run(["python3", "-mpip", "install", "httpie"])` | tool_install/`pip:install` | same | ok |
| `preverb-resume-retries` | `pip --resume-retries 3 install httpie` | tool_install/`pip:install` | clean | **FN** |
| `pip-log-file` | `pip --log-file /tmp/pip.log install httpie` | tool_install/`pip:install` | clean | **FN** |
| `pip-local-log` | `pip --local-log /tmp/pip.log install httpie` | tool_install/`pip:install` | clean | **FN** |
| `pip-default-timeout` | `pip --default-timeout 30 install httpie` | tool_install/`pip:install` | clean | **FN** |
| `python-m-pip-resume-retries` | `python3 -m pip --resume-retries 3 install httpie` | tool_install/`pip:install` | clean | **FN** |
| `pip-nocache-dir` | `pip --no-cache-dir install httpie` | tool_install/`pip:install` | same | ok (control) |
| `postverb-index-url` | `pip install --index-url https://pypi.org/simple httpie` | tool_install/`pip:install` | same | ok |
| `pip3.12-install` | `pip3.12 install httpie` | tool_install/`pip3.12:install` | same | ok |
| `python3.12-mpip` | `python3.12 -mpip install httpie` | tool_install/`pip:install` | same | ok |
| `npx-operand` | `npx cowsay hi` | tool_install/`npx` | same | ok |
| `uvx-from` | `uvx --from ruff ruff check .` | tool_install/`uvx` | same | ok |

## The permit boundary — holds (every attempt)

`verdict_of` (`tools/mado-tripwire.py:1617-1622`) counts a finding unpermitted iff
`f["class"] not in permit`; the class of each finding is fixed by `classify_segment`
(`:905-916` emits `host_mutation` for the elevation binary and then recurses into the rest of argv).
Measured matrix:

| transcript | permit | exit | label | unpermitted | findings |
|---|---|---|---|---|---|
| `sudo uv tool install ruff` | — | 1 | findings | 2 | host_mutation/`sudo`, tool_install/`uv:tool-install` |
| `sudo uv tool install ruff` | `tool_install` | 1 | findings | **1** | both (only `sudo` unpermitted) |
| `sudo uv tool install ruff` | `host_mutation` | 1 | findings | 1 | both (install unpermitted) |
| `sudo uv tool install ruff` | `tool_install host_mutation` | 0 | permitted_only | 0 | both |
| `sudo pipx run cowsay hi` | `tool_install` | 1 | findings | 1 | host_mutation/`sudo` + tool_install/`pipx:run` |
| `pacman -S --needed --noconfirm ripgrep` | `tool_install` | 1 | findings | 1 | host_mutation/`pacman:-S` |
| `npx cowsay hi` | `tool_install` | 0 | permitted_only | 0 | tool_install/`npx` |

`su -c 'uv tool install ruff'`, `pkexec uv tool install ruff`, `sudo bash -c 'uv tool install ruff'` and
`sudo -E uv tool install ruff` all produce both classes. No probe produced a `host_mutation` command
reported only under `tool_install`. The permit claim is not falsified.

Exact output for the decisive case:

```
$ python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/sudo-uv-tool-install.jsonl --permit tool_install
MADO_TRIPWIRE: findings
{"exit": 1, "findings": [["host_mutation", "sudo"], ["tool_install", "uv:tool-install"]], "permitted": ["tool_install"], "unpermitted": 1}
```

## Findings

### F1 — false negatives: pre-verb `pip` general-option values not in `PIP_ARG_OPTS`

`PIP_ARG_OPTS` (`tools/mado-tripwire.py:181-184`) lists `--log`, `--proxy`, `--cert`, `--cache-dir`,
`--timeout`, `--retries`, … but not the aliases `--log-file`, `--local-log`, `--default-timeout`, nor
`--resume-retries`. `leading_tokens` (`:738-753`) only skips a following token when the option is in that
set, so the *value* of an unlisted pre-verb option becomes the "verb" at `:810-814` and the install is
dropped. Scan output (all five identical shape):

```
$ python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/pip-default-timeout.jsonl
MADO_TRIPWIRE: clean
{"eval_unparsed": 0, "exit": 0, "findings": [], "unparsed_spawns": 0, "unpermitted": 0}
$ python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/pip-log-file.jsonl
MADO_TRIPWIRE: clean
{"eval_unparsed": 0, "exit": 0, "findings": [], "unparsed_spawns": 0, "unpermitted": 0}
$ python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/preverb-resume-retries.jsonl
MADO_TRIPWIRE: clean
{"eval_unparsed": 0, "exit": 0, "findings": [], "unparsed_spawns": 0, "unpermitted": 0}
```

These are not exotic hand-made argv: pip 26.2.1 itself accepts them pre-verb and reaches *install* help:

```
$ uv run --no-project --with pip python -m pip --default-timeout 30 install --help   # exit 0, "pip install [options]" x5
$ uv run --no-project --with pip python -m pip --log-file /tmp/pip.log install --help # exit 0, "pip install [options]" x5
$ uv run --no-project --with pip python -m pip --local-log /tmp/pip.log install --help # exit 0, "pip install [options]" x5
$ uv run --no-project --with pip python -m pip --resume-retries 3 install --help      # exit 0, "pip install [options]" x5
```

`pip --help` (26.2.1) renders `--log`, `--timeout` and `--resume-retries` inside its "General Options"
section (pre-command), and the parser's `cmdoptions.general_group` — introspected on the installed 26.2.1 —
holds the aliases `--log-file`/`--local-log`/`--default-timeout` next to them; pip's own parser confirms the
split position (`parse_command` splits "the general options before the command",
https://raw.githubusercontent.com/pypa/pip/main/src/pip/_internal/cli/main_parser.py, fetched 2026-10-20T18:06:10Z,
HTTP 200, 4412 bytes, sha256 `794f719324e0c6a8aa27fa108b99fdcbb7fedc9ab86ad4237e67ec2fa90cdb1e`, lines 72-81).
The alias spellings are absent from the rendered help but parse in the same region — the four exit-0 probes
above are the direct evidence.

`--resume-retries` landed in pip 25.1 (pip changelog, https://pip.pypa.io/en/stable/news/, HTTP 200,
529513 bytes, sha256 `c18a5980f468958b41f6243fb35bb53a55591220c4a15a8f2a29673d31f2915e`, fetched
2026-10-20T18:08:28Z: "Control the number of retry attempts using the --resume-retries flag (#12991)",
section `v25-1`). The `--log-file`/`--default-timeout` aliases are long-standing.

This is inside a shape the suite already treats as covered: `r19-installers/pip-family.jsonl:10`
(`pip --cache-dir /tmp/pipcache install --user x`) is pinned as `tool_install/pip:install`. So the gap is
not a scope call — the same "global option + separate value token before the verb" shape is pinned for one
member and silently missed for four others. It also propagates through the `python -m pip` form the
docstring names at `:12`: `python3 -m pip --resume-retries 3 install httpie` → clean.

### F2 — false positives: installer invocations that cannot acquire anything

The class is defined as "tool-acquisition channels" (`:10-13`) and the suite already pins query-only
installer invocations clean (`r19-installers/negative-controls.jsonl:15` `pip --version`,
`:20` `python3 -m pip --version`, `npm-family.jsonl:10` `npx --version`, `uv-pip-and-uvx.jsonl:4`
`uvx --version`, `cargo-channel.jsonl:4`/`negative-controls.jsonl:13` `cargo install --list`). The same
class flags the help/no-operand variants, which exit at argparse (or on a usage error) without touching a
package:

```
$ python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/pip-install-help.jsonl
MADO_TRIPWIRE: findings
{"eval_unparsed": 0, "exit": 1, "findings": [{"argv0": "pip", "class": "tool_install", "rule": "pip:install"}], "unparsed_spawns": 0, "unpermitted": 1}
```

Same for `python3 -m pip install --help`, `uv tool install --help`, `uv tool install`, `cargo install --help`,
`pipx run --help`, `pip install`. The docstring never mentions help forms, and the only no-acquisition
carve-out in the code is `cargo install --list` (`:842`), so this is a precision defect/ambiguity rather
than a contradiction of a written sentence —
but it is inconsistent with the pinned `--version` negatives and will fail a wave on a help query.
`pip install --dry-run httpie` is also flagged; I did **not** propose that as a defect because `--dry-run`
still resolves and downloads over the network and the docstring gives no guidance.

### F3 — false positive: `-c` after a python script operand is read as code

The interpreter branch states the principle that a script's arguments are data
(`tools/mado-tripwire.py:942-945`: "Reading -m anywhere in argv misreads a script's arguments
(`python3 tool.py -m ps` is not `python3 -m ps`)") and `python-script-arg-m` is correctly clean. The
retained legacy clause (`:964-966`, `if "-c" in args: # legacy: a -c after a script operand was always read`)
re-breaks it for `-c`:

```
$ python3 -I /tmp/AdvInstallers-tripwire.py --scan /tmp/adv-installers/python-script-arg-c.jsonl
MADO_TRIPWIRE: findings
{"eval_unparsed": 0, "exit": 1, "findings": [{"argv0": "pip", "class": "tool_install", "rule": "pip:install"}], "unparsed_spawns": 0, "unpermitted": 1}
```

No fixture in `.ufo/waves/round-19/tripwire` or `.ufo/waves/round-18` pins that legacy behavior (grep over
the suite dirs finds only legitimate shell `bash -c` and npx `-c` uses), so it is unpinned dead
over-approximation, and the docstring's Limits list does not state it (the code comment is the only record,
while the Limits section advertises "stated, not hidden").

## Proposed regression cases (suite format)

Files created under `/tmp/proposed-regressions`; `expected.json` sha256
`df4038367e64c8874c4764984a09e1c7b648d85c09a94e6ba3ca4f5d07b756ce`. Each `.jsonl` needs the usual
`{"type":"session","version":1,...}` header line first; the toolCall lines are:

```
--- preverb-general-options.jsonl
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv1","name":"bash","arguments":{"command":"pip --default-timeout 30 install httpie"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv2","name":"bash","arguments":{"command":"pip --log-file /tmp/pip.log install httpie"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv3","name":"bash","arguments":{"command":"pip --local-log /tmp/pip.log install httpie"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv4","name":"bash","arguments":{"command":"pip --resume-retries 3 install httpie"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv5","name":"bash","arguments":{"command":"python3 -m pip --resume-retries 3 install httpie"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv6","name":"bash","arguments":{"command":"pip --no-cache-dir install httpie"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_pv7","name":"bash","arguments":{"command":"pip install --index-url https://pypi.org/simple httpie"}}]}}
--- noop-forms.jsonl
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np1","name":"bash","arguments":{"command":"pip install --help"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np2","name":"bash","arguments":{"command":"python3 -m pip install --help"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np3","name":"bash","arguments":{"command":"uv tool install --help"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np4","name":"bash","arguments":{"command":"cargo install --help"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np5","name":"bash","arguments":{"command":"pipx run --help"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np6","name":"bash","arguments":{"command":"pip install"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np7","name":"bash","arguments":{"command":"uv tool install"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_np8","name":"bash","arguments":{"command":"pip --version"}}]}}
--- script-arg-c.jsonl
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_sc1","name":"bash","arguments":{"command":"python3 tools/x.py -c 'import os; os.system(\"pip install httpie\")'"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_sc2","name":"bash","arguments":{"command":"python3 tools/x.py -m pip install httpie"}}]}}
--- sudo-channels.jsonl
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_sd1","name":"bash","arguments":{"command":"sudo pipx run cowsay hi"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_sd2","name":"bash","arguments":{"command":"sudo npm install -g typescript"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_sd3","name":"bash","arguments":{"command":"pacman -S --needed --noconfirm ripgrep"}}]}}
--- limits.jsonl (optional: pins the docstring's stated negatives; delete if the limit is closed)
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_li1","name":"bash","arguments":{"command":"uv run --with requests python -c 'import requests'"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_li2","name":"bash","arguments":{"command":"cargo binstall cargo-watch"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_li3","name":"bash","arguments":{"command":"go install golang.org/x/tools/cmd/stringer@latest"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_li4","name":"bash","arguments":{"command":"curl -fsSL -o /home/vgpnk/.local/bin/rg https://example.invalid/rg"}}]}}
{"type":"message","message":{"role":"assistant","content":[{"type":"toolCall","id":"call_li5","name":"bash","arguments":{"command":"npm --global=true install typescript"}}]}}
```

Proposed `expected.json` case objects (each is valid JSON in the suite's case format; assemble the file as
`{"schema":"mado-tripwire-selftest-v1","cases":[ ... ]}` with commas between the objects — the first and
fourth are wrapped here for width only). `want_findings` lists **every** finding in the verdict, permitted
or not (suite convention, cf. `tool-install-permit-does-not-cover-sudo`), so the permit case differs from
`sudo-channels-both-classes` only by `permit`, and asserts that permitting `tool_install` leaves the
verdict and exit unchanged:

```json
{"name":"preverb-pip-general-option-values","args":["preverb-general-options.jsonl"],"want_exit":1,"want_label":"findings","want_findings":[
 {"file":"preverb-general-options.jsonl","line":2,"class":"tool_install","rule":"pip:install"},
 {"file":"preverb-general-options.jsonl","line":3,"class":"tool_install","rule":"pip:install"},
 {"file":"preverb-general-options.jsonl","line":4,"class":"tool_install","rule":"pip:install"},
 {"file":"preverb-general-options.jsonl","line":5,"class":"tool_install","rule":"pip:install"},
 {"file":"preverb-general-options.jsonl","line":6,"class":"tool_install","rule":"pip:install"},
 {"file":"preverb-general-options.jsonl","line":7,"class":"tool_install","rule":"pip:install"},
 {"file":"preverb-general-options.jsonl","line":8,"class":"tool_install","rule":"pip:install"}]}
{"name":"noop-installer-forms-stay-clean","args":["noop-forms.jsonl"],"want_exit":0,"want_label":"clean","want_findings":[]}
{"name":"script-arg-c-is-not-python-c","args":["script-arg-c.jsonl"],"want_exit":0,"want_label":"clean","want_findings":[]}
{"name":"sudo-channels-both-classes","args":["sudo-channels.jsonl"],"want_exit":1,"want_label":"findings","want_findings":[
 {"file":"sudo-channels.jsonl","line":2,"class":"host_mutation","rule":"sudo"},
 {"file":"sudo-channels.jsonl","line":2,"class":"tool_install","rule":"pipx:run"},
 {"file":"sudo-channels.jsonl","line":3,"class":"host_mutation","rule":"sudo"},
 {"file":"sudo-channels.jsonl","line":3,"class":"tool_install","rule":"npm:install-global"},
 {"file":"sudo-channels.jsonl","line":4,"class":"host_mutation","rule":"pacman:-S"}]}
{"name":"tool-install-permit-leaves-elevated-and-pacman","args":["sudo-channels.jsonl"],"permit":["tool_install"],"want_exit":1,"want_label":"findings","want_findings":[
 {"file":"sudo-channels.jsonl","line":2,"class":"host_mutation","rule":"sudo"},
 {"file":"sudo-channels.jsonl","line":2,"class":"tool_install","rule":"pipx:run"},
 {"file":"sudo-channels.jsonl","line":3,"class":"host_mutation","rule":"sudo"},
 {"file":"sudo-channels.jsonl","line":3,"class":"tool_install","rule":"npm:install-global"},
 {"file":"sudo-channels.jsonl","line":4,"class":"host_mutation","rule":"pacman:-S"}]}
{"name":"documented-limits-stay-clean","args":["limits.jsonl"],"want_exit":0,"want_label":"clean","want_findings":[]}
```

Run against the pinned tool, these are **3/6 green and 3/6 red**, and the three red ones are exactly
F1/F2/F3 (the three green ones formalize behavior that already holds):

```
CASE preverb-pip-general-option-values FAIL want=(1, [tool_install/pip:install lines 2-8]) got=(1, [lines 7,8])
CASE noop-installer-forms-stay-clean FAIL want=(0, []) got=(1, [pip:install L2,L3,L7; uv:tool-install L4,L8; cargo:install L5; pipx:run L6])
CASE script-arg-c-is-not-python-c FAIL want=(0, []) got=(1, [pip:install L2])
CASE sudo-channels-both-classes ok
CASE tool-install-permit-leaves-elevated-and-pacman ok
CASE documented-limits-stay-clean ok
SELFTEST_SUMMARY: 3/6 passed failed=['preverb-pip-general-option-values', 'noop-installer-forms-stay-clean', 'script-arg-c-is-not-python-c']
```

## Falsification attempts that failed (kept for the record)

- **Pre-verb `--index-url`/`-i`** looked like a fifth FN; pip 26.2.1 rejects it before the subcommand
  (`pip --index-url … install --help` → exit 2, usage `pip <command> [options]`; same for `-i` and for
  `python3 -m pip --index-url … install --help`). The tool's clean verdict there is **correct** — the
  option is accepted only after the verb (`pip install --index-url … --help` → exit 0).
- Permit attempts listed above (permit subsets, `pacman` under a `tool_install` permit, elevation via
  `sudo`/`sudo -E`/`su -c`/`pkexec`/`sudo bash -c`). No conversion of `host_mutation`.
- All docstring-stated negatives reproduce: `uv run --with`, `cargo binstall` (with and without a
  toolchain override), `go install`, `npm --global=true`, and a plain `curl -o ~/.local/bin/...` download
  — all scan `clean`, as the docstring says at `:17-19`. `sudo go install` yields only
  `host_mutation/sudo`, consistent with `go` being unlisted; that is a consequence of the stated limit,
  and with `--permit host_mutation` such a line would be `permitted_only` — but that is the permit doing
  what the docstring says, not a break.
- `npx -c 'cowsay hi'` scans clean; I could not establish that `-c` alone causes an npm package
  acquisition (npx `--call` runs a command string; installation is driven by `-p/--package` or an
  operand), so I did not file it. [UNK] for npx versions that fetch on `-c`.

## Limits

- Static classification only; nothing in the probes was executed except the pip `--help` adjudication.
  No claim here about the eval-variable resolver, shell function expansion, frozen mode, or the other
  classes — sibling seats own those.
- The 51 probe transcripts (49 distinct commands) are synthetic; a real transcript may use option
  combinations I did not try. The FN set (F1) is bounded by comparing `PIP_ARG_OPTS` against pip 26.2.1's
  value-taking general options; for `uv`/`npm`/`cargo`/`pipx` I only spot-checked, so further alias gaps
  there are possible. [INFERENCE]
- F2's expectation ("help/no-operand = clean") is my reading of the class definition plus the suite's
  pinned `--version`/`--list` negatives; the docstring does not state it. If the maintainer intends
  `--help` to count, F2 should be closed as documented rather than coded.
- I did not run the gate, any gate copy, jj, or host-service commands; the committed suite was the only
  lane test executed (`--selftest`, 18/18, read-only).

## Installs

- `pip 26.2.1` via `uv run --no-project --with pip` (uv cache only; no PATH install, no host package
  change, no pacman/sudo). Reason: adjudicate pip's real pre-verb option grammar for F1/`--index-url`
  instead of guessing from the tripwire's own tables.
- No other installs or upgrades.

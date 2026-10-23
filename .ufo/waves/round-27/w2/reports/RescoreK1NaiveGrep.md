RESCORE K1NaiveGrep best: PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED — not met

## Scope and outcome

Read the frozen registration first, then the godspeed skill, committed control, prior receipts and relevant pinned source. Axes: shape fidelity, line-local semantic strength, fresh-seed evidence and host safety. No delegation, integration or lane-subject edits.

Ran the committed control twice with fresh seeds under frozen counter v4. Both passed only BASE: 1/41, exit 1. Built a stronger variant within the stated shape and scored it on two further fresh seeds; both also passed only BASE: 1/41, exit 1. All four runs were conclusive TARGET_MISSED results, not setup/guard failures. This control did not meet the 41/41 redesign trigger.

**The committed control is not the strongest version of its shape.** Its literal-only boolean restriction is not required by the registered shape (root file only, physical lines independently, no source traversal, variables or merging). The retained variant changes only that value-mapping branch plus its explanatory docstring. It accepts `on`/`off`, `yes`/`no`, numeric truth values and the pinned parser's boolean prefixes while retaining every structural limitation. A separate bounded, source-derived boolean-line detector demonstrates a concrete improvement and exact restoration. No increase in the frozen counter's case count was observed; these different-seed runs do not establish a paired numerical improvement or global optimality of the variant.

Variant: `/fast/scratch/hyaku/mado-r27/rescore/K1NaiveGrep-stronger.py`, SHA-256 `0aacd8a769d6d913ed262003db1e819c0bd32950493cec39974115ba1cb28fe6`.

## Exact scoring commands and receipts

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Ran each command below twice, without `--seed`, so each counter generated an independent fresh seed:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NaiveGrep.py --jobs 6

env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1NaiveGrep-stronger.py --jobs 6
```

Each actual shell invocation used `set -o pipefail && COMMAND | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 910 prlimit --as=4000000000 -- tee RECEIPT` to preserve stdout and the detector's exit status. Initial attempts to launch the two original runs with the tool's asynchronous option were rejected before execution by its host-wide background-job limit; both were then run with synchronous calls. No failed detector result was rerun.

All receipt paths in this table are under `/fast/scratch/hyaku/mado-r27/rescore/`:

| Receipt | Fresh seed | Verbatim PRED line | Exit |
| --- | --- | --- | --- |
| `K1NaiveGrep-seed1.txt` | `569438832e76897a` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `K1NaiveGrep-seed2.txt` | `c734b89a82764c05` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `K1NaiveGrep-stronger-seed1.txt` | `97ba2749c47855e4` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `K1NaiveGrep-stronger-seed2.txt` | `e28a5a720d3bcfb7` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

Every run resolved REV to `2fdca5caaab6859386effbb8fa6acc5250c90633`; snapshot: 79 files, SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Each confirmed duplicate BASE oracle equality with zero rules, and oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

## Comparison with committed receipts

The requested `controls/v4/K1NaiveGrep-seed*.txt` paths are **v4** receipts, not v3: both their headers and PRED labels say v4. They scored 1/41 (`8181b2b3d7e653d2`) and 2/41 (`43e44544cc382be0`); the latter passed BASE and `C16 APPEND:GAPSHORT+ONEMPTY`. The newly requested v4 re-scores scored 1/41 twice. Historical and new results all miss 41/41; a one-case difference across independently generated populations is not evidence of a code regression.

For completeness, the actual `controls/v3/` receipts scored 2/41 (`30688c62b8e855e5`) and 1/41 (`8f384c40777b4ea2`) under the now-retired v3 counter. These are historical comparisons, not scores of the active claim. The verdict above uses the best of this assignment's four fresh v4 measurements, not the historical maximum of 2/41.

## Boolean mutation detector

Pinned [ConfigManager.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp) routes workspace boolean fields through `ParserUtils::parseInt`. The pinned [ParserUtils.cpp:134–149](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp) accepts `true`/`on`/`yes` prefixes as 1, `false`/`off`/`no` prefixes as 0, hexadecimal values and integer conversion. Fetched these raw URLs with bounded curl, without bypassing access controls:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 40 prlimit --as=4000000000 -- curl --fail --silent --show-error --max-time 30 --max-filesize 500000 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 40 prlimit --as=4000000000 -- curl --fail --silent --show-error --max-time 30 --max-filesize 200000 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 40 prlimit --as=4000000000 -- curl --fail --silent --show-error --max-time 30 --max-filesize 200000 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp
```

Actual fetches used the same bounded tee wrapper, with a 45-second tee timeout. Saved bodies: `K1NaiveGrep-source-ConfigManager.txt`, `K1NaiveGrep-source-ParserUtils.txt` and `K1NaiveGrep-source-MiscFunctions.txt` in the rescore directory. MiscFunctions was read for existing command-prefix semantics; no command-prefix change was made.

**Mutant:** in the isolated stronger file only, replace its boolean branch with the committed control's two-line `if value in ("true", "false")` branch. **Expected detector:** exact canonical JSON equality for one root-only line using six valid nonliteral boolean spellings. Expected output is source-derived, not a new direct Hyprland-oracle measurement.

Launched this identical argv for pristine, mutated and restored bytes with environment exactly `{"PATH":"/usr/bin","HOME":"/home/vgpnk"}` and the working directory above:

```text
timeout 90 prlimit --as=4000000000 -- python3 -I -c CODE /fast/scratch/hyaku/mado-r27/rescore/K1NaiveGrep-stronger.py
```

`CODE` was:

```python
import hashlib, importlib.util, json, os, shutil, sys, tempfile
from pathlib import Path
oracle_path = '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/harness/oracle.py'
spec = importlib.util.spec_from_file_location('probe_oracle', oracle_path)
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
root = tempfile.mkdtemp(prefix='K1NaiveGrep-bool-probe-', dir='/fast/scratch/hyaku/mado-r27/rescore')
try:
    conf = Path(root) / '.config/hypr/hyprland.conf'
    conf.parent.mkdir(parents=True)
    conf.write_text('workspace = name:bool-probe, border:on, shadow:off, rounding:1, decorate:0, default:yes, persistent:no\n')
    expected = [{'workspaceString':'name:bool-probe','enabled':True,'border':True,'shadow':False,'rounding':True,'decorate':False,'default':True,'persistent':False}]
    got, error = O.run_tool(sys.argv[1], root, timeout=20)
    print('tool_sha256='+hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest())
    print('expected='+json.dumps(expected, sort_keys=True))
    print('got='+json.dumps(got, sort_keys=True))
    print('error='+repr(error))
    ok = json.dumps(got, sort_keys=True) == json.dumps(expected, sort_keys=True)
    print('BOOL_LINE_DETECTOR='+('PASS' if ok else 'FAIL'))
    sys.exit(0 if ok else 1)
finally:
    shutil.rmtree(root)
```

Actual results, saved in `/fast/scratch/hyaku/mado-r27/rescore/K1NaiveGrep-bool-probe.txt`:

| Bytes | Detector | Exit | SHA-256 |
| --- | --- | --- | --- |
| Pristine stronger variant | PASS; all six boolean fields present with expected values | 0 | `0aacd8a769d6d913ed262003db1e819c0bd32950493cec39974115ba1cb28fe6` |
| Literal-only mutant | FAIL; output only `enabled` and `workspaceString` | 1 | `b1091826f5272961169c80401ba2920b0177ca2f9571ef5e07f260d1af347913` |
| Restored stronger variant | PASS; exact pristine output | 0 | `0aacd8a769d6d913ed262003db1e819c0bd32950493cec39974115ba1cb28fe6` |

Verdict: **killed by this scoped boolean detector**, with positive pristine/restored baselines. This is not a frozen-target mutant-kill claim: the committed control already misses the frozen target, so treating its failures as such a kill would be inconclusive. The stronger file was restored byte-for-byte, and the fixture directories were removed in every detector invocation's `finally` block.

## Hashes, restoration and host safety

The committed control was never modified. Independently measured before and after all scoring: `f26dfb60602b57297fba5c4e5b1153dd22964f2b1cb7fee33a2539f77550e611`. Counter v4 likewise remained `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`. Each receipt pinned oracle SHA-256 `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`; independent measurement before the stronger runs and at completion matched it. The retained stronger file's score-time and post-restoration hashes match.

Receipt SHA-256 values:

- `K1NaiveGrep-seed1.txt`: `15c5c8e9477b43a04449befd4de968ad5d3c77e17fda6906f2bec7e2a17793f9`
- `K1NaiveGrep-seed2.txt`: `b17b5d40fe0e0a21b0e10f6dd1aecf9cf24e9be10a8f334b6f7eaf3593c7d8b4`
- `K1NaiveGrep-stronger-seed1.txt`: `5689c091c2d38d9ab14457de3ec2309ff9e456801b0ca168400b254790bf41ae`
- `K1NaiveGrep-stronger-seed2.txt`: `0230030858d2a3a38c55279500be6a5e65dfc6baba6c5bc3f3ff3c75661b9449`

Before writes, `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- df -h /fast` reported 91% used, 73G available. Independent before/after subprocess calls ran `timeout 30 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend` with the same cleared environment; Python counted rows containing `/usr/bin/Hyprland`. Both calls exited 0 with empty stderr and counted **1338**, delta **0** (11:36:39Z to 11:43:28Z). Every counter receipt independently says `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

Only the frozen counters started compositors, through the pinned oracle and its host-wide 12-slot semaphore. All four bounded counter processes completed; their oracle cleanup paths terminate and wait for each process group. The micro-detector used only `run_tool`, not `oracle()`, and all three bounded subprocesses completed. No independently launched process remains. No live compositor commands, service changes, package installs/updates, git/jj writes or sibling edits occurred. The only lane write was this assigned report; artifacts and evidence remain under the assigned rescore path.

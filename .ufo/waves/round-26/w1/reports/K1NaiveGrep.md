# K1NaiveGrep — C1 NAIVE GREP control

## Verdict
CONTROL K1NaiveGrep best: cases_pass=5/41 verdict=TARGET_MISSED — not met

Both independent fresh seeds scored 5/41 with exit 1. BASE passed in both runs; each counter's double-oracle baseline equality guard passed. This constrained control was rejected by the frozen counter, not evidence that a full resolver meets C1. No standalone pristine/mutated/restored production-tool probe was assigned or performed, so this is not reported as a separately killed production mutant.

## Control and expected detector

- Axes: shape fidelity, numeric/table fidelity, detector discrimination, host isolation.
- Control: `.ufo/waves/round-26/controls/K1NaiveGrep.py`, a single Python stdlib file accepting `--home DIR` and printing JSON `[nodes, beziers]`.
- Deliberate defect: replace config/source traversal with `os.walk(DIR)` and blindly apply matching directives in native walk order, last definition winning by name.
- Every regular file is read, without filename, extension, source-membership, or size filtering. There is no directory/file sorting, source following, variable expansion, category tracking, inline-comment removal, node/curve existence check, coordinate/speed bound check, or style validation. Only lines whose first non-whitespace character is `#` are skipped.
- Matching uses `(animation|bezier)\s*=\s*(.*)`. Unknown names are retained; missing fields are empty; unparseable numbers are retained as strings rather than rejecting directives. Disabled-node field assignment and float32/two-decimal output representation follow the opened handler/writer snippets, without their validation.
- Embedded defaults came directly from the pinned harness `oracle()` on a minimal tree: 35 nodes and 2 beziers. Compact JSON sha256: `19719f7207048d53d8ed13f0de2624a83fef25c601640e23200f2bb667a2e11a`.
- Expected detector: frozen `.ufo/waves/round-26/c1/count.py`, exact node/bezier tuple-set comparison against isolated Hyprland v0.56.2 for BASE + 40 generated cases. Target remains 41/41.
- Example actual failures: first seed C35 (`VARIABLE+DISABLE`) had nodes missing=2 extra=2; second seed C07 (`NEWSRC+UNSOURCED`) had nodes missing=5 extra=5. These are multi-operation witnesses; no individual-operation causal attribution is claimed.

## Commands and oracle acquisition

All subprocess environments copied the inherited environment with `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed. No host compositor mutation or direct Hyprland startup was performed. Commands ran from `/home/vgpnk/Projects/shokunin/mado-shokunin` unless stated otherwise.

```text
timeout 10 df -h /fast
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  618G  186G  77% /fast
```

A private scratch minimal tree contained only `.config/hypr/hyprland.conf` with a comment. The oracle invocation's Python code was:

```python
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("m26_oracle", sys.argv[1])
o = importlib.util.module_from_spec(spec)
spec.loader.exec_module(o)
o.check_build()
before = o.coredumps()
data, error = o.oracle(sys.argv[2], sys.argv[3], ["animations"])
after = o.coredumps()
print(json.dumps({"data": data, "error": error, "coredumps_before": before, "coredumps_after": after}))
sys.exit(0 if data is not None else 2)
```

First invocation (before the L1 resource-limit clarification) used argv:

```text
timeout 120 prlimit --as=4000000000 -- python3 -I -c 'import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("m26_oracle", sys.argv[1])
o = importlib.util.module_from_spec(spec)
spec.loader.exec_module(o)
o.check_build()
before = o.coredumps()
data, error = o.oracle(sys.argv[2], sys.argv[3], ["animations"])
after = o.coredumps()
print(json.dumps({"data": data, "error": error, "coredumps_before": before, "coredumps_after": after}))
sys.exit(0 if data is not None else 2)
' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/harness/oracle.py /fast/scratch/hyaku/mado-r26/K1NaiveGrep/minimal /fast/scratch/hyaku/mado-r26/K1NaiveGrep/oracle
```

Actual exit code: 2. Stdout:

```text
{"data": null, "error": "sandbox exited rc=1 before answering", "coredumps_before": 1335, "coredumps_after": 1335}
```

Its scratch `sandbox.log` contained:

```text
prlimit: failed to set the AS resource limit: Operation not permitted
```

The attempted extraction then raised `TypeError: 'NoneType' object is not subscriptable`; no default table was taken from that failed run. This preliminary failure measured nothing and is not a detector kill.

The successful retry preserved the inherited hard AS limit while capping the caller's soft limit, and used a fresh oracle work directory:

```text
timeout 120 prlimit --as=4000000000: -- python3 -I -c 'import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("m26_oracle", sys.argv[1])
o = importlib.util.module_from_spec(spec)
spec.loader.exec_module(o)
o.check_build()
before = o.coredumps()
data, error = o.oracle(sys.argv[2], sys.argv[3], ["animations"])
after = o.coredumps()
print(json.dumps({"data": data, "error": error, "coredumps_before": before, "coredumps_after": after}))
sys.exit(0 if data is not None else 2)
' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/harness/oracle.py /fast/scratch/hyaku/mado-r26/K1NaiveGrep/minimal /fast/scratch/hyaku/mado-r26/K1NaiveGrep/oracle-success
```

Actual exit code: 0, stderr empty. Parsed output: `error=""`, `animations=[35 nodes, 2 beziers]`, `coredumps_before=1335`, `coredumps_after=1335`. Its exact default table is embedded in the control file. The frozen oracle performed compositor creation and process-group teardown.

After the L1 clarification, both scoring commands used explicit soft 4 GB / hard 8 GB AS limits, allowing the oracle's own 8 GB limit:

```text
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NaiveGrep.py
```

That identical argv ran twice concurrently through a two-worker Python `ThreadPoolExecutor`; no `--seed` was supplied, so each counter generated its own fresh seed. No counter run exited 2 and neither was rerun.

## Verbatim receipts

The following stdout blocks, including each `exit=1` line, are concatenated byte-for-byte in `.ufo/waves/round-26/controls/K1NaiveGrep.txt` (8772 bytes; sha256 `64f031c0b2db6152ebcaa2007fcdba1858cddb0de1710ca227f228354a2203c2`).

### Run 1

Process return code: 1. Elapsed: 60.474 s. Stderr: `''`.

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NaiveGrep.py sha256:16658352272840f66284b2daf0085709b9535c2e3269c949d029af9d9b1258b3
seed=6eb5dd8be1a3e5fc
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (REBEZ+DISABLE)
CASE C01   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+ORDER+REBEZ)
CASE C02   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (INVALID+VARIABLE+DISABLE)
CASE C03   FAIL nodes missing=1 extra=1 beziers missing=0 extra=1 (SPACING+COMMENT+INVALID)
CASE C04   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ROOT+COMMENT)
CASE C05   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ROOT+CATEGORY)
CASE C06   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+NEWSRC)
CASE C07   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+ROOT)
CASE C08   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (NEWSRC+ROOT)
CASE C09   FAIL nodes missing=0 extra=0 beziers missing=0 extra=1 (INVALID+REBEZ+BEZIER+COMMENT)
CASE C10   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (NEWSRC+COMMENT+VARIABLE)
CASE C11   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (VARIABLE+SPACING+DISABLE)
CASE C12   FAIL nodes missing=0 extra=0 beziers missing=1 extra=1 (REBEZ+DISABLE)
CASE C13   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ORDER+NEWSRC)
CASE C14   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (REBEZ+VARIABLE+ROOT)
CASE C15   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (BEZIER+REBEZ+INVALID)
CASE C16   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (REBEZ+UNSOURCED+VARIABLE+INVALID)
CASE C17   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (VARIABLE+DISABLE+INVALID+SOURCED)
CASE C18   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (CATEGORY+COMMENT)
CASE C19   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+DISABLE+CATEGORY+NEWSRC)
CASE C20   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+CATEGORY+VARIABLE+ROOT)
CASE C21   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+DISABLE+ROOT+SOURCED)
CASE C22   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (DISABLE+ROOT)
CASE C23   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (REBEZ+DISABLE+SPACING)
CASE C24   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (CATEGORY+SPACING+ROOT)
CASE C25   FAIL nodes missing=1 extra=2 beziers missing=0 extra=0 (DISABLE+INVALID+ORDER+CATEGORY)
CASE C26   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+ROOT)
CASE C27   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ROOT+DISABLE+COMMENT)
CASE C28   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (UNSOURCED+CATEGORY+COMMENT+REBEZ)
CASE C29   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (NEWSRC+COMMENT+REBEZ+INVALID)
CASE C30   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SPACING+CATEGORY+REBEZ)
CASE C31   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (REBEZ+NEWSRC)
CASE C32   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+NEWSRC)
CASE C33   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ROOT+BEZIER+SOURCED)
CASE C34   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+SPACING+ROOT+ORDER)
CASE C35   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (VARIABLE+DISABLE)
CASE C36   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (VARIABLE+SPACING+NEWSRC)
CASE C37   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+SOURCED+SPACING)
CASE C38   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SOURCED+ROOT)
CASE C39   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (VARIABLE+DISABLE+CATEGORY+INVALID)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=5/41 verdict=TARGET_MISSED
exit=1
```

### Run 2

Process return code: 1. Elapsed: 38.249 s. Stderr: `''`.

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1NaiveGrep.py sha256:16658352272840f66284b2daf0085709b9535c2e3269c949d029af9d9b1258b3
seed=ca99472f7d62a7ed
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=2 extra=2 beziers missing=0 extra=1 (SOURCED+INVALID+VARIABLE+ORDER)
CASE C01   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (UNSOURCED+CATEGORY+SPACING)
CASE C02   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (COMMENT+SPACING)
CASE C03   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+VARIABLE+CATEGORY+NEWSRC)
CASE C04   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (COMMENT+INVALID+ROOT+CATEGORY)
CASE C05   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SOURCED+INVALID)
CASE C06   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (VARIABLE+REBEZ)
CASE C07   FAIL nodes missing=5 extra=5 beziers missing=0 extra=0 (NEWSRC+UNSOURCED)
CASE C08   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (COMMENT+SOURCED+SPACING)
CASE C09   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (DISABLE+CATEGORY+SOURCED+UNSOURCED)
CASE C10   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (VARIABLE+COMMENT)
CASE C11   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (UNSOURCED+INVALID+ROOT)
CASE C12   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ROOT+INVALID+BEZIER)
CASE C13   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ORDER+VARIABLE+DISABLE+COMMENT)
CASE C14   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ROOT+REBEZ+VARIABLE)
CASE C15   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (NEWSRC+COMMENT)
CASE C16   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+COMMENT+UNSOURCED)
CASE C17   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (NEWSRC+CATEGORY+REBEZ+DISABLE)
CASE C18   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (DISABLE+VARIABLE)
CASE C19   FAIL nodes missing=0 extra=0 beziers missing=0 extra=1 (ROOT+SPACING+INVALID)
CASE C20   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (COMMENT+ROOT+BEZIER+ORDER)
CASE C21   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (INVALID+VARIABLE+DISABLE)
CASE C22   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SPACING+BEZIER+ROOT)
CASE C23   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+NEWSRC+INVALID+CATEGORY)
CASE C24   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (VARIABLE+SOURCED+DISABLE+REBEZ)
CASE C25   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (CATEGORY+COMMENT+VARIABLE+NEWSRC)
CASE C26   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (BEZIER+ROOT)
CASE C27   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (NEWSRC+VARIABLE+BEZIER)
CASE C28   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+INVALID+CATEGORY)
CASE C29   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (INVALID+REBEZ)
CASE C30   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (VARIABLE+SPACING+CATEGORY)
CASE C31   FAIL nodes missing=0 extra=0 beziers missing=1 extra=1 (REBEZ+ROOT+BEZIER)
CASE C32   FAIL nodes missing=1 extra=1 beziers missing=0 extra=1 (ROOT+INVALID+BEZIER)
CASE C33   FAIL nodes missing=0 extra=1 beziers missing=0 extra=0 (SPACING+INVALID)
CASE C34   FAIL nodes missing=0 extra=0 beziers missing=0 extra=1 (ROOT+DISABLE+SOURCED+INVALID)
CASE C35   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+NEWSRC+DISABLE)
CASE C36   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (REBEZ+SPACING+ORDER)
CASE C37   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+NEWSRC+REBEZ+ROOT)
CASE C38   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (NEWSRC+COMMENT+VARIABLE+UNSOURCED)
CASE C39   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (DISABLE+UNSOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=5/41 verdict=TARGET_MISSED
exit=1
```

## Byte preservation and cleanup

Before acquisition and after scoring, `timeout 10 sha256sum` reported the same frozen detector bytes:

| File | Before sha256 | After sha256 |
| --- | --- | --- |
| `.ufo/waves/round-26/c1/count.py` | `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd` | `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd` |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

Both counter receipts and the final hash command identify the retained control as sha256 `16658352272840f66284b2daf0085709b9535c2e3269c949d029af9d9b1258b3` (6003 bytes). No edits occurred between its scoring runs or afterward. The control is a new contracted output, not a modified production file; no production bytes required restoration. Neither `tools/mado-anims.py` nor `tools/mado-binds.py` was written.

Both scoring children returned normally, and both host-safety receipts report coredump delta 0. `timeout 10 pgrep -af /fast/scratch/hyaku/mado-r26/K1NaiveGrep/` matched only its own short-lived timeout wrapper (`1131675 timeout 10 pgrep -af /fast/scratch/hyaku/mado-r26/K1NaiveGrep/`), not an oracle. The subprocess check then exited. Python `shutil.rmtree('/fast/scratch/hyaku/mado-r26/K1NaiveGrep')` removed the private minimal tree and oracle work/log directories. Permanent writes are only this report and the two named control artifacts.

No tools installed or updated. No builds, linters, formatters, unrelated tests, git/jj write commands, or additional runtime were invoked.

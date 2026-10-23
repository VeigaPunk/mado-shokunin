# K1SnapshotCache — C1 snapshot-cache control

## Verdict

CONTROL K1SnapshotCache best: cases_pass=2/41 verdict=TARGET_MISSED — not met

The higher-scoring snapshot-only variant is the final `controls/K1SnapshotCache.py`.
Both requested variants were scored twice with independent fresh seeds. Every measured run exited 1; there were no counter exit-2 runs. All four passed BASE. The hash-gated default fallback did not improve the score.

| Variant | Run | Fresh seed | cases_pass | Verdict | Process exit |
| --- | --- | --- | --- | --- | --- |
| snapshot-only | 1 | `c45dec7210ca8ff7` | 1/41 | TARGET_MISSED | 1 |
| snapshot-only | 2 | `1b418d312d807328` | 2/41 | TARGET_MISSED | 1 |
| hash-fallback | 1 | `3ab2a84a36cb8d5f` | 1/41 | TARGET_MISSED | 1 |
| hash-fallback | 2 | `0fcba12b609ceec6` | 1/41 | TARGET_MISSED | 1 |

## Shape and provenance

Axes: score against 41/41; strict cache-only behavior; host isolation; byte-level reproducibility.

- Read the frozen registration and operator tooling rules before execution. No tools were installed or updated.
- Called the pinned harness's `snapshot(os.path.expanduser('~'), scratch_snapshot)` and then `oracle(scratch_snapshot, work, ['animations'])`. The live compositor was not queried or dispatched to.
- Snapshot: 79 files, SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`; table: 35 nodes and 6 beziers.
- Obtained the static default through the same `oracle()` with a separate home containing only an empty `.config/hypr/hyprland.conf`: 35 nodes and 2 beziers. The harness appends only its documented safety settings.
- Snapshot-only variant: embeds the complete JSON table, accepts `--home`, and prints that table without opening or walking DIR. It performs no resolution or interpretation.
- Hash-fallback variant: hashes every regular file under DIR in deterministic `os.walk` order, sorted directories/files, using relative path + NUL + SHA-256(content) + newline; exact equality selects the snapshot table, otherwise the embedded static default. An unreadable file also selects the default. It does not parse config, source directives, variables, expressions, or animation rules.
- Tree hash embedded in the second variant: `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.
- Snapshot-only source: 4101 bytes, SHA-256 `0c5672f9b4a5ca66697e7f5b8dd4b21da7dd020ae65dff00734030319daa6528`.
- Hash-fallback source: 8264 bytes, SHA-256 `bd630e72f0684d51a804045b53418f4870fcb03c9c05b1778eb75217ae9797c8`.
- The two variants used the same authorized `.py` path sequentially. After scoring both, restored the higher-scoring snapshot-only source exactly. No counter, harness, `tools/mado-anims.py`, or `tools/mado-binds.py` was edited.

One generated case also matched the unchanged cache: snapshot-only run 2, seed `1b418d312d807328`, C35 `SOURCED+UNSOURCED`. Its receipt reports zero node/bezier differences. Thus the syntactically effective operation did not ensure a different resulting table in that sampled case; the control still missed 39 cases in its best run. No contract change is proposed.

## Commands and setup failure

All subprocesses used cwd `/home/vgpnk/Projects/shokunin/mado-shokunin` and an environment with `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed. Commands below are actual argv rendered as shell commands. The two runs of each variant were independent concurrent subprocesses, using four oracle workers each; the unchanged harness enforces its host-wide 12-slot lock.

Before scratch writes:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 prlimit --as=4000000000 df -h /fast
```

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  618G  186G  77% /fast
```

The first acquisition attempt used a hard 4 GB cap, which prevented the harness's own 8 GB limit from being set. This was an inconclusive setup failure, not a killed mutant and not a counter receipt. The sandbox log contained exactly:

```text
prlimit: failed to set the AS resource limit: Operation not permitted
```

Initial acquisition command:

```sh
timeout 240 prlimit --as=4000000000 -- python3 -I -c 'import hashlib, importlib.util, json, os, pathlib, sys
lane, scratch = map(pathlib.Path, sys.argv[1:])
harness = lane / '"'"'.ufo/waves/round-26/harness/oracle.py'"'"'
assert hashlib.sha256(harness.read_bytes()).hexdigest() == '"'"'680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441'"'"'
spec = importlib.util.spec_from_file_location('"'"'mado_snapshot_oracle'"'"', harness)
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
O.check_build()
core0 = O.coredumps()
snap = scratch / '"'"'snapshot'"'"'
snap.mkdir()
nfiles, digest = O.snapshot(os.path.expanduser('"'"'~'"'"'), str(snap))
print('"'"'snapshot files=%d digest sha256:%s'"'"' % (nfiles, digest), flush=True)
res, err = O.oracle(str(snap), str(scratch / '"'"'snapshot-oracle'"'"'), ['"'"'animations'"'"'])
if res is None:
    raise RuntimeError(err)
default = scratch / '"'"'default'"'"'
(default / '"'"'.config/hypr'"'"').mkdir(parents=True)
(default / '"'"'.config/hypr/hyprland.conf'"'"').write_bytes(b'"'"''"'"')
static, err = O.oracle(str(default), str(scratch / '"'"'default-oracle'"'"'), ['"'"'animations'"'"'])
if static is None:
    raise RuntimeError(err)
def tree_hash(home):
    h = hashlib.sha256()
    for dp, dirs, files in os.walk(home):
        dirs.sort()
        for name in sorted(files):
            p = os.path.join(dp, name)
            if not os.path.isfile(p):
                continue
            rel = os.path.relpath(p, home)
            h.update(rel.encode() + b'"'"'\0'"'"' + hashlib.sha256(open(p, '"'"'rb'"'"').read()).hexdigest().encode() + b'"'"'\n'"'"')
    return h.hexdigest()
meta = {'"'"'snapshot_files'"'"': nfiles, '"'"'harness_snapshot_digest'"'"': digest, '"'"'tree_digest'"'"': tree_hash(str(snap)), '"'"'snapshot'"'"': res['"'"'animations'"'"'], '"'"'default'"'"': static['"'"'animations'"'"'], '"'"'core_before'"'"': core0, '"'"'core_after'"'"': O.coredumps()}
(scratch / '"'"'tables.json'"'"').write_text(json.dumps(meta, indent=2) + '"'"'\n'"'"')
print('"'"'snapshot table nodes=%d beziers=%d'"'"' % tuple(map(len, meta['"'"'snapshot'"'"'])), flush=True)
print('"'"'default table nodes=%d beziers=%d'"'"' % tuple(map(len, meta['"'"'default'"'"'])), flush=True)
print('"'"'tree digest sha256:'"'"' + meta['"'"'tree_digest'"'"'], flush=True)
print('"'"'HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d'"'"' % (core0, meta['"'"'core_after'"'"'], meta['"'"'core_after'"'"'] - core0), flush=True)
' /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r26/K1SnapshotCache-g0wt295o
```

Actual output:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
Traceback (most recent call last):
  File "<string>", line 16, in <module>
    raise RuntimeError(err)
RuntimeError: sandbox exited rc=1 before answering
capture_exit=1
```

Corrected acquisition retained a 4 GB soft cap with the hard limit inherited, allowing the pinned harness to set its own 8 GB cap. Subsequent hash-fallback runs and the mutation witness used the L1-prescribed explicit `--as=4000000000:8000000000` instead. No harness bytes were changed.

Successful acquisition command:

```sh
timeout 240 prlimit --as=4000000000: -- python3 -I -c 'import hashlib, importlib.util, json, os, pathlib, sys
lane, scratch = map(pathlib.Path, sys.argv[1:])
harness = lane / '"'"'.ufo/waves/round-26/harness/oracle.py'"'"'
assert hashlib.sha256(harness.read_bytes()).hexdigest() == '"'"'680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441'"'"'
spec = importlib.util.spec_from_file_location('"'"'mado_snapshot_oracle'"'"', harness)
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
O.check_build()
core0 = O.coredumps()
snap = scratch / '"'"'snapshot'"'"'
snap.mkdir(exist_ok=True)
nfiles, digest = O.snapshot(os.path.expanduser('"'"'~'"'"'), str(snap))
print('"'"'snapshot files=%d digest sha256:%s'"'"' % (nfiles, digest), flush=True)
res, err = O.oracle(str(snap), str(scratch / '"'"'snapshot-oracle-capped'"'"'), ['"'"'animations'"'"'])
if res is None:
    raise RuntimeError(err)
default = scratch / '"'"'default'"'"'
(default / '"'"'.config/hypr'"'"').mkdir(parents=True)
(default / '"'"'.config/hypr/hyprland.conf'"'"').write_bytes(b'"'"''"'"')
static, err = O.oracle(str(default), str(scratch / '"'"'default-oracle'"'"'), ['"'"'animations'"'"'])
if static is None:
    raise RuntimeError(err)
def tree_hash(home):
    h = hashlib.sha256()
    for dp, dirs, files in os.walk(home):
        dirs.sort()
        for name in sorted(files):
            p = os.path.join(dp, name)
            if not os.path.isfile(p):
                continue
            rel = os.path.relpath(p, home)
            h.update(rel.encode() + b'"'"'\0'"'"' + hashlib.sha256(open(p, '"'"'rb'"'"').read()).hexdigest().encode() + b'"'"'\n'"'"')
    return h.hexdigest()
meta = {'"'"'snapshot_files'"'"': nfiles, '"'"'harness_snapshot_digest'"'"': digest, '"'"'tree_digest'"'"': tree_hash(str(snap)), '"'"'snapshot'"'"': res['"'"'animations'"'"'], '"'"'default'"'"': static['"'"'animations'"'"'], '"'"'core_before'"'"': core0, '"'"'core_after'"'"': O.coredumps()}
(scratch / '"'"'tables.json'"'"').write_text(json.dumps(meta, indent=2) + '"'"'\n'"'"')
print('"'"'snapshot table nodes=%d beziers=%d'"'"' % tuple(map(len, meta['"'"'snapshot'"'"'])), flush=True)
print('"'"'default table nodes=%d beziers=%d'"'"' % tuple(map(len, meta['"'"'default'"'"'])), flush=True)
print('"'"'tree digest sha256:'"'"' + meta['"'"'tree_digest'"'"'], flush=True)
print('"'"'HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d'"'"' % (core0, meta['"'"'core_after'"'"'], meta['"'"'core_after'"'"'] - core0), flush=True)
' /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r26/K1SnapshotCache-g0wt295o
```

Actual output:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
snapshot table nodes=35 beziers=6
default table nodes=35 beziers=2
tree digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
capture_exit=0
```

Snapshot-only scoring command, run twice without `--seed`:

```sh
timeout 900 prlimit --as=4000000000: -- python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py
```

Hash-fallback scoring command, run twice without `--seed`:

```sh
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py
```

All four measured subprocesses had empty stderr. The complete stdout, including each `exit=1`, is preserved verbatim in `controls/K1SnapshotCache.txt` and pasted below.

## Bounded mutation witness and exact restoration

Mutant: a single appended `animation = windows, 1, 9.125, default` directive inside an `animations` block in the isolated snapshot's root config. This is a config-input mutation witnessing stale-cache behavior, not a counter-source mutation. No sibling's source was touched.

Expected detector: for each of pristine, mutated, and restored root bytes, call the same pinned `oracle(..., ['animations'])`, call the same tool sandbox with the final snapshot-only source, and compare the exact C1 node/bezier field sets. A valid witness requires baseline PASS, mutation FAIL, and restored PASS.

Actual output: pristine PASS; mutant FAIL with one missing and one extra node, unchanged beziers; restored PASS. The oracle reported windows speed `9.12` and bezier `default` for the mutant while the cache retained `3.79` and `easeOutQuint`. Verdict: KILLED for this stale-cache input witness. It does not imply that any counter-source mutant was tested.

The original config was saved in memory and restored in a `finally` block even if detection failed. The printed before/after SHA-256 values are identical.

Exact command:

```sh
timeout 300 prlimit --as=4000000000:8000000000 -- python3 -I -c 'import hashlib, importlib.util, json, os, pathlib, sys
lane, scratch, tool = map(pathlib.Path, sys.argv[1:])
harness = lane / '"'"'.ufo/waves/round-26/harness/oracle.py'"'"'
assert hashlib.sha256(harness.read_bytes()).hexdigest() == '"'"'680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441'"'"'
spec = importlib.util.spec_from_file_location('"'"'mado_cache_probe'"'"', harness)
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
O.check_build()
root = scratch / '"'"'snapshot/.config/hypr/hyprland.conf'"'"'
original = root.read_bytes()
original_hash = O.sha(original)
node_fields = ('"'"'name'"'"', '"'"'overridden'"'"', '"'"'bezier'"'"', '"'"'enabled'"'"', '"'"'speed'"'"', '"'"'style'"'"')
bez_fields = ('"'"'name'"'"', '"'"'X0'"'"', '"'"'Y0'"'"', '"'"'X1'"'"', '"'"'Y1'"'"')
def sets(data):
    return tuple({tuple(json.dumps(row.get(f), sort_keys=True) for f in fields) for row in part} for part, fields in zip(data, (node_fields, bez_fields)))
def detect(phase):
    truth, err = O.oracle(str(scratch / '"'"'snapshot'"'"'), str(scratch / ('"'"'probe-'"'"' + phase)), ['"'"'animations'"'"'])
    if truth is None:
        raise RuntimeError('"'"'oracle: '"'"' + err)
    actual, err = O.run_tool(str(tool), str(scratch / '"'"'snapshot'"'"'))
    if actual is None:
        raise RuntimeError('"'"'tool: '"'"' + err)
    expected_sets, actual_sets = sets(truth['"'"'animations'"'"']), sets(actual)
    result = {'"'"'phase'"'"': phase, '"'"'root_sha256'"'"': O.sha(root.read_bytes()), '"'"'pass'"'"': expected_sets == actual_sets, '"'"'nodes_missing'"'"': len(expected_sets[0] - actual_sets[0]), '"'"'nodes_extra'"'"': len(actual_sets[0] - expected_sets[0]), '"'"'beziers_missing'"'"': len(expected_sets[1] - actual_sets[1]), '"'"'beziers_extra'"'"': len(actual_sets[1] - expected_sets[1]), '"'"'expected_windows'"'"': next(r for r in truth['"'"'animations'"'"'][0] if r['"'"'name'"'"'] == '"'"'windows'"'"'), '"'"'actual_windows'"'"': next(r for r in actual[0] if r['"'"'name'"'"'] == '"'"'windows'"'"')}
    print(json.dumps(result, sort_keys=True), flush=True)
    return result
core0 = O.coredumps()
results = []
try:
    results.append(detect('"'"'pristine'"'"'))
    root.write_bytes(original + b'"'"'\nanimations {\n    animation = windows, 1, 9.125, default\n}\n'"'"')
    results.append(detect('"'"'mutated'"'"'))
finally:
    root.write_bytes(original)
    restored_hash = O.sha(root.read_bytes())
    print('"'"'RESTORE root before=%s after=%s exact=%s'"'"' % (original_hash, restored_hash, original_hash == restored_hash), flush=True)
results.append(detect('"'"'restored'"'"'))
verdict = '"'"'KILLED'"'"' if results[0]['"'"'pass'"'"'] and not results[1]['"'"'pass'"'"'] and results[2]['"'"'pass'"'"'] else ('"'"'INCONCLUSIVE'"'"' if not results[0]['"'"'pass'"'"'] else '"'"'SURVIVED'"'"')
print('"'"'MUTATION verdict='"'"' + verdict, flush=True)
core1 = O.coredumps()
print('"'"'HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d'"'"' % (core0, core1, core1 - core0), flush=True)
' /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r26/K1SnapshotCache-g0wt295o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py
```

Actual output:

```text
{"actual_windows": {"bezier": "easeOutQuint", "enabled": true, "name": "windows", "overridden": true, "speed": 3.79, "style": ""}, "beziers_extra": 0, "beziers_missing": 0, "expected_windows": {"bezier": "easeOutQuint", "enabled": true, "name": "windows", "overridden": true, "speed": 3.79, "style": ""}, "nodes_extra": 0, "nodes_missing": 0, "pass": true, "phase": "pristine", "root_sha256": "ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365"}
{"actual_windows": {"bezier": "easeOutQuint", "enabled": true, "name": "windows", "overridden": true, "speed": 3.79, "style": ""}, "beziers_extra": 0, "beziers_missing": 0, "expected_windows": {"bezier": "default", "enabled": true, "name": "windows", "overridden": true, "speed": 9.12, "style": ""}, "nodes_extra": 1, "nodes_missing": 1, "pass": false, "phase": "mutated", "root_sha256": "f00dfc8f23e149cf40753074d05b43b95e7ecf60551673067469e94682ebcf8e"}
RESTORE root before=ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365 after=ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365 exact=True
{"actual_windows": {"bezier": "easeOutQuint", "enabled": true, "name": "windows", "overridden": true, "speed": 3.79, "style": ""}, "beziers_extra": 0, "beziers_missing": 0, "expected_windows": {"bezier": "easeOutQuint", "enabled": true, "name": "windows", "overridden": true, "speed": 3.79, "style": ""}, "nodes_extra": 0, "nodes_missing": 0, "pass": true, "phase": "restored", "root_sha256": "ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365"}
MUTATION verdict=KILLED
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
probe_exit=0
```

## Restoration and host-safety evidence

Final hash command:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 prlimit --as=4000000000 sha256sum .ufo/waves/round-26/controls/K1SnapshotCache.py .ufo/waves/round-26/c1/count.py .ufo/waves/round-26/harness/oracle.py /fast/scratch/hyaku/mado-r26/K1SnapshotCache-g0wt295o/snapshot/.config/hypr/hyprland.conf
```

```text
0c5672f9b4a5ca66697e7f5b8dd4b21da7dd020ae65dff00734030319daa6528  .ufo/waves/round-26/controls/K1SnapshotCache.py
f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd  .ufo/waves/round-26/c1/count.py
680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441  .ufo/waves/round-26/harness/oracle.py
ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365  /fast/scratch/hyaku/mado-r26/K1SnapshotCache-g0wt295o/snapshot/.config/hypr/hyprland.conf
```

Counter and harness still match their initial frozen hashes. The final control matches its first two scored bytes. The scratch root hash is restored from mutant `f00dfc8f23e149cf40753074d05b43b95e7ecf60551673067469e94682ebcf8e` to pristine `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365`.

All successful acquisition, scoring, and witness outputs report Hyprland coredumps 1335 → 1335, delta 0. The harness terminated and waited for each private sandbox process group in `finally`; all enclosing timeout commands returned. No host service was restarted, no live compositor write verb was used, and no git/jj write command was run.

Scratch evidence remains under `/fast/scratch/hyaku/mado-r26/K1SnapshotCache-g0wt295o`, with the snapshot root restored. No helper script was written there.

## Verbatim frozen-counter receipts

### snapshot-only, run 1, attempt 1

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py sha256:0c5672f9b4a5ca66697e7f5b8dd4b21da7dd020ae65dff00734030319daa6528
seed=c45dec7210ca8ff7
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (ORDER+UNSOURCED+VARIABLE+BEZIER)
CASE C01   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (ROOT+COMMENT+CATEGORY+INVALID)
CASE C02   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (NEWSRC+ORDER)
CASE C03   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (DISABLE+SPACING)
CASE C04   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+DISABLE)
CASE C05   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (INVALID+BEZIER)
CASE C06   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ORDER+UNSOURCED)
CASE C07   FAIL nodes missing=3 extra=3 beziers missing=1 extra=1 (REBEZ+UNSOURCED+ROOT+NEWSRC)
CASE C08   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SOURCED+UNSOURCED+INVALID+VARIABLE)
CASE C09   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (COMMENT+VARIABLE)
CASE C10   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (BEZIER+SOURCED+NEWSRC)
CASE C11   FAIL nodes missing=4 extra=4 beziers missing=1 extra=0 (DISABLE+VARIABLE+COMMENT+CATEGORY)
CASE C12   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (VARIABLE+BEZIER)
CASE C13   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ROOT+ORDER+DISABLE)
CASE C14   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (ROOT+NEWSRC+SOURCED+DISABLE)
CASE C15   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (BEZIER+ROOT+SOURCED+UNSOURCED)
CASE C16   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (VARIABLE+SOURCED)
CASE C17   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (BEZIER+SOURCED)
CASE C18   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (REBEZ+SOURCED+ORDER+INVALID)
CASE C19   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (SOURCED+COMMENT+NEWSRC)
CASE C20   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ROOT+INVALID+DISABLE+VARIABLE)
CASE C21   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (BEZIER+DISABLE)
CASE C22   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (INVALID+ROOT)
CASE C23   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (UNSOURCED+ORDER+DISABLE+VARIABLE)
CASE C24   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ORDER+VARIABLE+INVALID)
CASE C25   FAIL nodes missing=2 extra=2 beziers missing=1 extra=1 (VARIABLE+SOURCED+REBEZ)
CASE C26   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (ORDER+CATEGORY)
CASE C27   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (INVALID+NEWSRC+UNSOURCED)
CASE C28   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SOURCED+DISABLE)
CASE C29   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (INVALID+VARIABLE)
CASE C30   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (DISABLE+REBEZ)
CASE C31   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (VARIABLE+COMMENT+NEWSRC+SOURCED)
CASE C32   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (INVALID+CATEGORY)
CASE C33   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (SPACING+VARIABLE+INVALID)
CASE C34   FAIL nodes missing=2 extra=2 beziers missing=2 extra=1 (INVALID+ORDER+REBEZ+CATEGORY)
CASE C35   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (ORDER+UNSOURCED+BEZIER)
CASE C36   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (INVALID+ROOT)
CASE C37   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (COMMENT+INVALID+CATEGORY)
CASE C38   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SOURCED+COMMENT)
CASE C39   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (NEWSRC+DISABLE)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

### snapshot-only, run 2, attempt 1

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py sha256:0c5672f9b4a5ca66697e7f5b8dd4b21da7dd020ae65dff00734030319daa6528
seed=1b418d312d807328
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (DISABLE+CATEGORY+INVALID+ROOT)
CASE C01   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (COMMENT+CATEGORY+UNSOURCED)
CASE C02   FAIL nodes missing=4 extra=4 beziers missing=1 extra=0 (DISABLE+NEWSRC+CATEGORY)
CASE C03   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (ROOT+BEZIER)
CASE C04   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (BEZIER+VARIABLE)
CASE C05   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (SPACING+VARIABLE+NEWSRC+INVALID)
CASE C06   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+ROOT)
CASE C07   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (ROOT+CATEGORY)
CASE C08   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (NEWSRC+DISABLE+SPACING+INVALID)
CASE C09   FAIL nodes missing=2 extra=2 beziers missing=1 extra=0 (VARIABLE+UNSOURCED+CATEGORY+INVALID)
CASE C10   FAIL nodes missing=2 extra=2 beziers missing=2 extra=1 (REBEZ+CATEGORY+INVALID+ORDER)
CASE C11   FAIL nodes missing=1 extra=1 beziers missing=1 extra=0 (INVALID+CATEGORY)
CASE C12   FAIL nodes missing=1 extra=1 beziers missing=2 extra=1 (REBEZ+BEZIER)
CASE C13   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (COMMENT+INVALID+ROOT)
CASE C14   FAIL nodes missing=3 extra=3 beziers missing=2 extra=0 (VARIABLE+BEZIER+CATEGORY)
CASE C15   FAIL nodes missing=1 extra=1 beziers missing=1 extra=1 (REBEZ+SOURCED+INVALID)
CASE C16   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+COMMENT+SOURCED)
CASE C17   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (ROOT+COMMENT)
CASE C18   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (SPACING+INVALID)
CASE C19   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (COMMENT+SOURCED)
CASE C20   FAIL nodes missing=4 extra=4 beziers missing=1 extra=0 (CATEGORY+SPACING+ROOT)
CASE C21   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (DISABLE+VARIABLE+COMMENT+ROOT)
CASE C22   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (DISABLE+SOURCED+UNSOURCED)
CASE C23   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (UNSOURCED+SPACING+DISABLE)
CASE C24   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ROOT+UNSOURCED)
CASE C25   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (BEZIER+SPACING)
CASE C26   FAIL nodes missing=1 extra=1 beziers missing=0 extra=0 (ORDER+SOURCED)
CASE C27   FAIL nodes missing=5 extra=5 beziers missing=1 extra=0 (VARIABLE+CATEGORY+SPACING+ROOT)
CASE C28   FAIL nodes missing=3 extra=3 beziers missing=2 extra=1 (REBEZ+DISABLE+CATEGORY+ORDER)
CASE C29   FAIL nodes missing=3 extra=3 beziers missing=0 extra=0 (VARIABLE+ORDER+SOURCED)
CASE C30   FAIL nodes missing=2 extra=2 beziers missing=2 extra=1 (BEZIER+ROOT+REBEZ)
CASE C31   FAIL nodes missing=3 extra=3 beziers missing=1 extra=0 (ROOT+CATEGORY+ORDER)
CASE C32   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (VARIABLE+ROOT+SOURCED+SPACING)
CASE C33   FAIL nodes missing=4 extra=4 beziers missing=0 extra=0 (DISABLE+ORDER+COMMENT+SOURCED)
CASE C34   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+VARIABLE+NEWSRC)
CASE C35   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SOURCED+UNSOURCED)
CASE C36   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (UNSOURCED+SOURCED+VARIABLE+ORDER)
CASE C37   FAIL nodes missing=5 extra=5 beziers missing=0 extra=0 (NEWSRC+ORDER+SOURCED+COMMENT)
CASE C38   FAIL nodes missing=2 extra=2 beziers missing=0 extra=0 (DISABLE+SOURCED)
CASE C39   FAIL nodes missing=0 extra=0 beziers missing=1 extra=1 (REBEZ+INVALID)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=2/41 verdict=TARGET_MISSED
exit=1
```

### hash-fallback, run 1, attempt 1

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py sha256:bd630e72f0684d51a804045b53418f4870fcb03c9c05b1778eb75217ae9797c8
seed=3ab2a84a36cb8d5f
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (UNSOURCED+SOURCED)
CASE C01   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SOURCED+COMMENT)
CASE C02   FAIL nodes missing=19 extra=19 beziers missing=4 extra=0 (NEWSRC+COMMENT+DISABLE+UNSOURCED)
CASE C03   FAIL nodes missing=16 extra=16 beziers missing=5 extra=1 (ORDER+REBEZ+UNSOURCED)
CASE C04   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (NEWSRC+VARIABLE+CATEGORY)
CASE C05   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (DISABLE+SPACING+BEZIER+NEWSRC)
CASE C06   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (INVALID+NEWSRC+DISABLE)
CASE C07   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (BEZIER+ROOT+INVALID+SPACING)
CASE C08   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (UNSOURCED+CATEGORY+INVALID+NEWSRC)
CASE C09   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ORDER+DISABLE)
CASE C10   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (NEWSRC+ROOT+DISABLE)
CASE C11   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SPACING+VARIABLE)
CASE C12   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (COMMENT+ROOT+SOURCED)
CASE C13   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+DISABLE+UNSOURCED)
CASE C14   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (COMMENT+SOURCED+DISABLE)
CASE C15   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (VARIABLE+NEWSRC+BEZIER)
CASE C16   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+INVALID+SPACING)
CASE C17   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (DISABLE+UNSOURCED)
CASE C18   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+INVALID+SOURCED)
CASE C19   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (SOURCED+COMMENT+CATEGORY)
CASE C20   FAIL nodes missing=17 extra=17 beziers missing=6 extra=0 (BEZIER+CATEGORY+ROOT)
CASE C21   FAIL nodes missing=16 extra=16 beziers missing=6 extra=0 (ROOT+CATEGORY+ORDER+BEZIER)
CASE C22   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SOURCED+ROOT+INVALID)
CASE C23   FAIL nodes missing=19 extra=19 beziers missing=5 extra=0 (NEWSRC+DISABLE+BEZIER+VARIABLE)
CASE C24   FAIL nodes missing=16 extra=16 beziers missing=6 extra=1 (CATEGORY+REBEZ)
CASE C25   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (ROOT+SOURCED+CATEGORY)
CASE C26   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (UNSOURCED+VARIABLE+COMMENT+SOURCED)
CASE C27   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (VARIABLE+SOURCED)
CASE C28   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (INVALID+DISABLE+REBEZ+COMMENT)
CASE C29   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (NEWSRC+ORDER+INVALID)
CASE C30   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ROOT+DISABLE)
CASE C31   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (DISABLE+COMMENT+BEZIER+ROOT)
CASE C32   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+SPACING+REBEZ)
CASE C33   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ORDER+SOURCED)
CASE C34   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SPACING+DISABLE)
CASE C35   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (REBEZ+NEWSRC+COMMENT)
CASE C36   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (REBEZ+VARIABLE+UNSOURCED)
CASE C37   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (SOURCED+ROOT+NEWSRC+CATEGORY)
CASE C38   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (UNSOURCED+ORDER+COMMENT+NEWSRC)
CASE C39   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (COMMENT+CATEGORY+INVALID)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

### hash-fallback, run 2, attempt 1

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1SnapshotCache.py sha256:bd630e72f0684d51a804045b53418f4870fcb03c9c05b1778eb75217ae9797c8
seed=0fcba12b609ceec6
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=16 extra=16 beziers missing=6 extra=1 (COMMENT+REBEZ+CATEGORY+UNSOURCED)
CASE C01   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (DISABLE+ROOT)
CASE C02   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (UNSOURCED+ROOT)
CASE C03   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (SPACING+BEZIER)
CASE C04   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (SOURCED+BEZIER+SPACING)
CASE C05   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (ORDER+SOURCED+COMMENT+CATEGORY)
CASE C06   FAIL nodes missing=18 extra=18 beziers missing=5 extra=1 (VARIABLE+INVALID+REBEZ+NEWSRC)
CASE C07   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ROOT+NEWSRC+DISABLE)
CASE C08   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ORDER+NEWSRC+REBEZ)
CASE C09   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (SPACING+INVALID+BEZIER)
CASE C10   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (NEWSRC+COMMENT+INVALID)
CASE C11   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+VARIABLE)
CASE C12   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ORDER+VARIABLE)
CASE C13   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (INVALID+COMMENT+REBEZ+BEZIER)
CASE C14   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (ROOT+UNSOURCED+BEZIER)
CASE C15   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (COMMENT+BEZIER+UNSOURCED)
CASE C16   FAIL nodes missing=17 extra=17 beziers missing=6 extra=0 (BEZIER+CATEGORY+VARIABLE)
CASE C17   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (NEWSRC+UNSOURCED+DISABLE)
CASE C18   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (REBEZ+SPACING+NEWSRC)
CASE C19   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ROOT+SOURCED+COMMENT+DISABLE)
CASE C20   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (ORDER+SPACING+SOURCED+NEWSRC)
CASE C21   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (VARIABLE+SPACING+REBEZ+NEWSRC)
CASE C22   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (ORDER+CATEGORY+COMMENT+ROOT)
CASE C23   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+UNSOURCED+ROOT+INVALID)
CASE C24   FAIL nodes missing=19 extra=19 beziers missing=5 extra=0 (BEZIER+NEWSRC+REBEZ+COMMENT)
CASE C25   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SOURCED+SPACING+DISABLE)
CASE C26   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (DISABLE+INVALID+VARIABLE)
CASE C27   FAIL nodes missing=15 extra=15 beziers missing=6 extra=1 (REBEZ+BEZIER+INVALID+DISABLE)
CASE C28   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (VARIABLE+INVALID)
CASE C29   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (NEWSRC+ROOT+SOURCED)
CASE C30   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (VARIABLE+REBEZ)
CASE C31   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (SOURCED+NEWSRC+BEZIER+REBEZ)
CASE C32   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (REBEZ+DISABLE+SOURCED)
CASE C33   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+REBEZ+SPACING)
CASE C34   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (UNSOURCED+ORDER+REBEZ+BEZIER)
CASE C35   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+SPACING+REBEZ)
CASE C36   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SOURCED+ROOT+DISABLE+VARIABLE)
CASE C37   FAIL nodes missing=17 extra=17 beziers missing=5 extra=1 (COMMENT+REBEZ+NEWSRC)
CASE C38   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ROOT+INVALID+ORDER)
CASE C39   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (COMMENT+INVALID+SPACING+UNSOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```


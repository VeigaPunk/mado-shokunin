# K1StaticDefault — C1 STATIC DEFAULT control

## Verdict
CONTROL K1StaticDefault best: cases_pass=0/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs returned `exit=1`, with 0/41 cases passing. Neither run exited 2, so no guard retry was needed. The frozen counter rejected this config-ignoring control on BASE and all 40 generated cases in both runs. This is a negative-control result, not a finding about untested resolver implementations.

## Scope and axes

Axes: exact default-table capture, strict STATIC DEFAULT shape, frozen-counter evidence, and host isolation.

- Wrote only the named control, receipt, and report in the lane. No `tools/mado-anims.py`, `tools/mado-binds.py`, counter, harness, or other source was edited.
- Read the registration and godspeed skill before implementation. No subagents, model calls, package installs, git/jj writes, or direct Hyprland launches were used.
- Control fault: ignore all config bytes and replay the true minimal-config default. Expected detector: the frozen C1 counter must reject it when a tree's animation or bezier sets differ from that default.
- This assignment added a control rather than mutating existing source. Pristine/mutated/restored source probes and restoration are therefore not applicable. Original counter/harness bytes were left untouched; their printed hashes stayed pinned across both receipts.

## One-time default capture

Created this 67-byte scratch input at `/fast/scratch/hyaku/mado-r26/K1StaticDefault/home/.config/hypr/hyprland.conf` using the file-write tool:

```conf
ecosystem {
    no_update_news = true
    no_donation_nag = true
}
```

Input SHA-256: `12a5bd62a5ce7f725a107f2bb1790e65ff82b893f3366350dfce241e247eb363`.

Imported the frozen harness by its full path, verified its SHA-256 and binary pins, and called `oracle()` exactly once with `verbs=["animations"]`. The harness itself appends its ecosystem block to its private copy; the supplied tree contained no animation, bezier, source, or exec directives. No host compositor connection was used.

Before scratch creation, the bounded `df -h /fast` command reported 186G available (77% used):

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  618G  186G  77% /fast
```

Actual acquisition argv, rendered as a shell command; working directory was the lane root. The subprocess environment omitted `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`:

```sh
timeout --kill-after=10s 300s prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B -c 'import hashlib, importlib.util, json, pathlib
p = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/harness/oracle.py")
hash_ = hashlib.sha256(p.read_bytes()).hexdigest()
assert hash_ == "680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441", hash_
spec = importlib.util.spec_from_file_location("mado_r26_default_oracle", str(p))
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
O.check_build()
root = "/fast/scratch/hyaku/mado-r26/K1StaticDefault"
conf = pathlib.Path(root + "/home/.config/hypr/hyprland.conf")
print("ORACLE_PIN sha256:" + hash_, flush=True)
print("MINIMAL_CONFIG bytes=%d sha256:%s" % (len(conf.read_bytes()), hashlib.sha256(conf.read_bytes()).hexdigest()), flush=True)
before = O.coredumps()
result, error = O.oracle(root + "/home", root + "/oracle", ["animations"])
after = O.coredumps()
print("HOST_SAFETY hyprland_coredumps_before=%d after=%d delta=%d" % (before, after, after - before), flush=True)
if result is None:
    raise SystemExit("ORACLE_FAIL " + error)
print("DEFAULT_COUNTS nodes=%d beziers=%d" % (len(result["animations"][0]), len(result["animations"][1])), flush=True)
print("DEFAULT_TABLE " + json.dumps(result["animations"], separators=(",", ":")), flush=True)
'
```

Actual acquisition stdout and process result:

```text
ORACLE_PIN sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
MINIMAL_CONFIG bytes=67 sha256:12a5bd62a5ce7f725a107f2bb1790e65ff82b893f3366350dfce241e247eb363
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
DEFAULT_COUNTS nodes=35 beziers=2
DEFAULT_TABLE [[{"name":"specialWorkspaceOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"workspacesIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"layersIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeDpms","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windowsMove","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeGlow","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"zoomFactor","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"shadowangle","overridden":true,"bezier":"default","enabled":false,"speed":1.0,"style":""},{"name":"specialWorkspace","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"glowangle","overridden":true,"bezier":"default","enabled":false,"speed":1.0,"style":""},{"name":"fadeSwitch","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"borderangle","overridden":true,"bezier":"default","enabled":false,"speed":1.0,"style":""},{"name":"fadeOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fade","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"border","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"specialWorkspaceIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"workspaces","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"global","overridden":true,"bezier":"default","enabled":true,"speed":8.0,"style":""},{"name":"__internal_fadeCTM","overridden":true,"bezier":"linear","enabled":true,"speed":5.0,"style":""},{"name":"workspacesOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"layersOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windowsIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windowsOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"layers","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadePopups","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeShadow","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeLayers","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windows","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeLayersIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeLayersOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeDim","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadePopupsIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"monitorAdded","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadePopupsOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""}],[{"name":"linear","X0":0.0,"Y0":0.0,"X1":1.0,"Y1":1.0},{"name":"default","X0":0.0,"Y0":0.75,"X1":0.15,"Y1":1.0}]]
ACQUISITION_EXIT=0
```

Acquisition stderr was empty. Captured 35 nodes (including the internal node) and 2 beziers. Embedded the exact parsed table as compact JSON; SHA-256 of that compact JSON, excluding a trailing newline: `19719f7207048d53d8ed13f0de2624a83fef25c601640e23200f2bb667a2e11a`.

## Control artifact and scoring commands

Control: `.ufo/waves/round-26/controls/K1StaticDefault.py`, 3788 bytes, SHA-256 `6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a`. It accepts required `--home DIR` through `argparse`, discards the parsed value, and prints its literal captured JSON. It never opens, enumerates, resolves, or otherwise reads DIR, and performs no config interpretation.

The following command was run twice concurrently with independent fresh seeds generated by the frozen counter. Environment sanitization and argv are shown together in shell form; working directory was `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=15s 900s prlimit --as=4000000000:8000000000 --core=0 -- python3 -I -B .ufo/waves/round-26/c1/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1StaticDefault.py
```

`-B` prevents import-cache writes in the lane. The outer limit is soft 4 GB / hard 8 GB so the pinned oracle can set its own required 8 GB limit. Each command had a 900-second timeout and 15-second forced-kill grace. The oracle's slot locks retain its host-wide 12-instance limit. Both counter processes returned 1 with empty stderr.

Verbatim concatenated stdout is saved at `.ufo/waves/round-26/controls/K1StaticDefault.txt` (8936 bytes, SHA-256 `6d952d4d5d4c801307f8b43d541fed0c37e58985e90ed0a7db660ba62ed7a2dd`). Full receipts follow.

## Receipt 1

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1StaticDefault.py sha256:6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a
seed=e30328bbfc2bb30b
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (DISABLE+ROOT+INVALID+ORDER)
CASE C01   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (DISABLE+ORDER+REBEZ+SOURCED)
CASE C02   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (UNSOURCED+DISABLE+ORDER+CATEGORY)
CASE C03   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (UNSOURCED+COMMENT+SOURCED)
CASE C04   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (ORDER+NEWSRC)
CASE C05   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (INVALID+ROOT)
CASE C06   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (SPACING+COMMENT+NEWSRC+BEZIER)
CASE C07   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ORDER+VARIABLE+UNSOURCED)
CASE C08   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (COMMENT+NEWSRC+ORDER+DISABLE)
CASE C09   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (UNSOURCED+SPACING+SOURCED+ORDER)
CASE C10   FAIL nodes missing=16 extra=16 beziers missing=6 extra=1 (REBEZ+CATEGORY+INVALID+DISABLE)
CASE C11   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (VARIABLE+DISABLE+SOURCED)
CASE C12   FAIL nodes missing=19 extra=19 beziers missing=4 extra=0 (NEWSRC+COMMENT+SPACING+ROOT)
CASE C13   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ROOT+DISABLE)
CASE C14   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (UNSOURCED+CATEGORY)
CASE C15   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (NEWSRC+INVALID+REBEZ)
CASE C16   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (BEZIER+UNSOURCED+NEWSRC)
CASE C17   FAIL nodes missing=16 extra=16 beziers missing=6 extra=1 (BEZIER+REBEZ+ROOT+INVALID)
CASE C18   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (BEZIER+COMMENT)
CASE C19   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (REBEZ+SOURCED+CATEGORY)
CASE C20   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (SOURCED+CATEGORY)
CASE C21   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (DISABLE+ROOT)
CASE C22   FAIL nodes missing=16 extra=16 beziers missing=5 extra=1 (REBEZ+ORDER+UNSOURCED+NEWSRC)
CASE C23   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (NEWSRC+COMMENT+ORDER)
CASE C24   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (UNSOURCED+COMMENT+BEZIER+SOURCED)
CASE C25   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (ORDER+SPACING+DISABLE)
CASE C26   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (UNSOURCED+NEWSRC)
CASE C27   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (ORDER+BEZIER+VARIABLE)
CASE C28   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (REBEZ+CATEGORY+SPACING+COMMENT)
CASE C29   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (VARIABLE+DISABLE+SOURCED+ORDER)
CASE C30   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (COMMENT+REBEZ)
CASE C31   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (ORDER+BEZIER+UNSOURCED)
CASE C32   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (DISABLE+UNSOURCED+SOURCED)
CASE C33   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ROOT+SOURCED)
CASE C34   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (NEWSRC+DISABLE)
CASE C35   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (SPACING+ORDER+CATEGORY)
CASE C36   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+ORDER+NEWSRC)
CASE C37   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (UNSOURCED+VARIABLE+SPACING)
CASE C38   FAIL nodes missing=19 extra=19 beziers missing=4 extra=0 (DISABLE+COMMENT+ROOT+SOURCED)
CASE C39   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ORDER+REBEZ+COMMENT+SOURCED)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

## Receipt 2

```text
counter c1-r26 sha256:f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K1StaticDefault.py sha256:6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a
seed=51609202c96a3d6c
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
CASE BASE  FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (unperturbed)
CASE C00   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (BEZIER+REBEZ+NEWSRC+ROOT)
CASE C01   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (ROOT+SOURCED)
CASE C02   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (SOURCED+DISABLE+BEZIER+UNSOURCED)
CASE C03   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (VARIABLE+REBEZ+NEWSRC)
CASE C04   FAIL nodes missing=19 extra=19 beziers missing=5 extra=0 (CATEGORY+NEWSRC+REBEZ)
CASE C05   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ORDER+VARIABLE)
CASE C06   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SOURCED+UNSOURCED)
CASE C07   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SOURCED+REBEZ+SPACING)
CASE C08   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+DISABLE+ROOT+REBEZ)
CASE C09   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (SPACING+COMMENT)
CASE C10   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+COMMENT)
CASE C11   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (UNSOURCED+NEWSRC)
CASE C12   FAIL nodes missing=15 extra=15 beziers missing=5 extra=0 (SOURCED+CATEGORY+INVALID)
CASE C13   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+COMMENT)
CASE C14   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (SPACING+ROOT+INVALID)
CASE C15   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (DISABLE+UNSOURCED)
CASE C16   FAIL nodes missing=18 extra=18 beziers missing=5 extra=0 (CATEGORY+SPACING)
CASE C17   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (BEZIER+ROOT+VARIABLE+ORDER)
CASE C18   FAIL nodes missing=18 extra=18 beziers missing=4 extra=0 (VARIABLE+SOURCED+INVALID+NEWSRC)
CASE C19   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (REBEZ+UNSOURCED+ROOT)
CASE C20   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SPACING+ROOT)
CASE C21   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (UNSOURCED+SOURCED+ORDER+VARIABLE)
CASE C22   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (REBEZ+VARIABLE)
CASE C23   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ROOT+DISABLE+VARIABLE)
CASE C24   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (ORDER+VARIABLE+INVALID+CATEGORY)
CASE C25   FAIL nodes missing=15 extra=15 beziers missing=4 extra=0 (SOURCED+INVALID+REBEZ)
CASE C26   FAIL nodes missing=17 extra=17 beziers missing=5 extra=1 (INVALID+REBEZ+ORDER+SPACING)
CASE C27   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (ORDER+DISABLE)
CASE C28   FAIL nodes missing=17 extra=17 beziers missing=4 extra=0 (SOURCED+VARIABLE)
CASE C29   FAIL nodes missing=16 extra=16 beziers missing=5 extra=1 (SOURCED+REBEZ)
CASE C30   FAIL nodes missing=15 extra=15 beziers missing=5 extra=1 (ROOT+INVALID+SOURCED+REBEZ)
CASE C31   FAIL nodes missing=16 extra=16 beziers missing=6 extra=1 (UNSOURCED+CATEGORY+DISABLE+REBEZ)
CASE C32   FAIL nodes missing=17 extra=17 beziers missing=6 extra=0 (CATEGORY+BEZIER+SOURCED)
CASE C33   FAIL nodes missing=16 extra=16 beziers missing=6 extra=1 (ORDER+REBEZ+CATEGORY)
CASE C34   FAIL nodes missing=19 extra=19 beziers missing=4 extra=0 (VARIABLE+ROOT+ORDER+SPACING)
CASE C35   FAIL nodes missing=17 extra=17 beziers missing=5 extra=0 (DISABLE+ROOT+CATEGORY)
CASE C36   FAIL nodes missing=17 extra=17 beziers missing=5 extra=1 (COMMENT+NEWSRC+REBEZ+ORDER)
CASE C37   FAIL nodes missing=16 extra=16 beziers missing=5 extra=0 (CATEGORY+VARIABLE)
CASE C38   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (ROOT+DISABLE)
CASE C39   FAIL nodes missing=16 extra=16 beziers missing=4 extra=0 (UNSOURCED+INVALID+VARIABLE+ROOT)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

## Evidence and restoration

- Run 1 seed: `e30328bbfc2bb30b`; run 2 seed: `51609202c96a3d6c`.
- Both receipts used snapshot SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727` (79 files), and both double-BASE oracle checks agreed at 35 nodes / 6 beziers.
- BASE differed from STATIC DEFAULT by 15 missing and 15 extra node tuples, with 4 missing bezier tuples in each run.
- Frozen C1 SHA-256 before/after the two scored runs, as printed in both receipts: `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd`.
- Frozen oracle SHA-256 at acquisition and in both scored receipts: `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`.
- Control SHA-256 at creation and in both scored receipts: `6a864aeb510de59cc568947eb647ad3f3b7bdcdc414a115453da4b46d1783e2a`. It was not edited between runs.
- Acquisition and both scored runs each reported Hyprland coredumps 1335 → 1335, delta 0. All Hyprland instances were created through the unchanged harness, whose `finally` terminates and waits for each sandbox process group. All launched acquisition/counter commands returned.
- Removed only this seat's scratch tree after capture and scoring using the command below; it completed with no output. No pre-existing source bytes needed restoration. The named control and receipts remain as required deliverables.

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 prlimit --as=4000000000 --core=0 -- rm -r -- /fast/scratch/hyaku/mado-r26/K1StaticDefault
```

No build, lint, formatter, or additional detector run was performed. No tools were installed or updated.

# ReviewIsolationEvidence — round 27, w2

Reviewer: MadoR27.ReviewIsolationEvidence (UFO-FSD reviewer, leaf seat, no subagent dispatch).
Scope: (1) re-derive the w1 `ExecIsolationProbe` receipt `evidence/isolation-r27.txt` by re-running its
launcher `/fast/scratch/hyaku/mado-r27/iso/launcher.py` twice with fresh canaries under the prescribed
`env -i` command; (2) assess the residual root-symlink gap recorded by w1 `SentinelHarness27` (MEDIUM)
against the counters' snapshot of `~/`. Read-only on lane files; no Hyprland started by this reviewer
(`run_tool` spawns bubblewrap only; the rootlink helper only calls `snapshot()`).

## 1. Re-derivation of evidence/isolation-r27.txt

Artifact hashes re-verified before running (all match the receipt):

```
launcher.py        99174d171f68ba94fe79bfc1ff0bafe6fa59fa9d9bbbc24c5ad7c533ee55ff0b
probe.py           e7e03d3ef77736b96b7c67b71461a505d764ff8c16181bfd24901d1464b18f77
case-home hyprland.conf  2152bf6a8492dc07a59b30c0bf22537e50da6dcbb5d35a2aabe7a37f3a592879
outside/canary.conf      4f318a7af00d01a19a0730d5a3cc14d6cc180293d124b948974f78b505f989aa
harness r26 oracle.py    680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
harness r27 oracle.py    0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601
```

Commands (exact same shape as the receipt; each run uses a fresh random 33-char alphanumeric canary
generated with `secrets`, stored as `canary3.txt` / `canary4.txt`):

```
cd /fast/scratch/hyaku/mado-r27/iso && env -i PATH=/usr/bin HOME=/home/vgpnk MADO_R27_CANARY=<random 33> \
  timeout 300 prlimit --core=0 --as=4000000000 -- python3 -I launcher.py > run3.json 2>run3.err
cd /fast/scratch/hyaku/mado-r27/iso && env -i PATH=/usr/bin HOME=/home/vgpnk MADO_R27_CANARY=<random 33> \
  timeout 300 prlimit --core=0 --as=4000000000 -- python3 -I launcher.py > run4.json 2>run4.err
```

Results:

| artifact | exit | stdout | stderr | sha256 |
|---|---|---|---|---|
| run3.json | 0 | 3677 B | 0 B | `0dadbad1c33960eb25399131c12ede68c180251bd977f07e1603638b08638a7b` |
| run4.json | 0 | 3677 B | 0 B | `a4061f3192ff3f6bf568b0688d6f6fc1dd099b59923c7cad0008f633b6322592` |

Comparison method: loaded w1's `run1.json`/`run2.json` and my `run3.json`/`run4.json`, computed a
signature over every field except the per-run namespace identities (`pid`, `pid_ns`, `ppid`), and
deep-diffed. Result: `run1 == run3`, `run1 == run4`, `run2 == run3`, `run2 == run4` are all **True**
on invariant fields, and the diff of run1 vs run3 lists **zero** differing fields (only the pid
namespace numbers differ, as in w1's own run1 vs run2). Byte size 3677 matches the receipt on all four
files. Key claims reproduced verbatim:

- launcher environ names: `[HOME, LC_CTYPE, MADO_R27_CANARY, PATH, _]`; `canary_value_len = 33`;
  `canary_name_present_in_launcher = true`.
- run_tool sandbox, round-26: pid-1 `bwrap` environ contains `MADO_R27_CANARY`
  (`pid1_names = [HOME, LC_CTYPE, MADO_R27_CANARY, PATH, _]`) → `canary_in_pid1 = true`; the tool's
  own environ (`pid 2`) is `[HOME, PATH, PWD]` → `canary_in_self = false`. The M26-5 leak vector is
  still present in the r26 harness, exactly as recorded.
- run_tool sandbox, round-27: pid-1 environ is `[PATH]` only → `canary_in_pid1 = false`;
  `canary_in_self = false`. The `env -i PATH=/usr/bin` scrub (oracle.py:234) closes the pid-1 leak.
- snapshot(): round-26 `nfiles=3 digest=4351a259bab44b4b9ea2afa676cf07f2154d0ab9a97d48d7b64f15359b228f8b`,
  `outside-link.conf` copied (82 B, sha `4f318a7a…` == outside canary, `outside_link_matches_canary=true`),
  `local-link.conf` copied; round-27 `nfiles=2 digest=d2e9a9417ca534be2680be584bbdf92df5920a874b90f344c4c4c7a51ac27142`,
  `outside-link.conf` not copied (`outside_link_copied=false`), `local-link.conf` copied.

**Verdict on the receipt:** `evidence/isolation-r27.txt` re-derives exactly. No discrepancy found in any
recorded value, code anchor, hash, byte count, or conclusion. The w1 probe file, launcher, fixtures and
both harness pins are unchanged from the receipt.

Supplementary root-symlink re-run (same helper as w1, does not start Hyprland):

```
cd /fast/scratch/hyaku/mado-r27/iso && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 120 \
  prlimit --core=0 --as=4000000000 -- python3 -I rootlink-snapshot.py > rootlink-w2.json 2>rootlink-w2.err
```

exit=0; stdout 1085 B; stderr 0 B; sha256 `dc698f41c78930bb6a453c1bc31e0afd612e6498c09be021b91dc934d4a5e987`
— byte-identical to w1's `rootlink.json` (same sha as in the receipt). The root-symlink escape reproduces
verbatim at this head: both harnesses copy the outside-HOME root canary (`nfiles=1`,
`root_canary_copied=true`, sha `4064eb49…`).

## 2. Residual root-symlink gap (SentinelHarness27 MEDIUM) vs the counters' snapshot of ~/

Code anchors (round-27 harness): `snapshot()` at oracle.py:70-87 resolves each root first —
`real = os.path.realpath(src)` — then `os.walk(real)`. The r27 guard at oracle.py:78 fires only when
`os.path.islink(p)` is true for a file met during the walk. Two consequences:

1. **Root/ancestor symlink bypass.** If a root (or an ancestor component such as `~/.config`) is a
   symlink resolving outside HOME, the walk starts at the canonical target; every file has a canonical
   `p`, so `islink(p)` is False and no containment check ever runs. Outside regular files (≤1 MiB) are
   copied. Confirmed dynamically by the rootlink re-run above (identical to w1 receipt): nfiles=1,
   `root_canary_copied=true` under **both** harnesses, with the same outside sha.
2. **Containment is HOME-wide, not root-wide.** A file symlink whose resolved target lies anywhere inside
   canonical HOME passes the guard (`startswith(realpath(home_src)+sep)`), even if the target is a
   non-config file (e.g. `~/.ssh/*`). In-HOME links can thus escape the selected config roots.
3. Directory symlinks met during the walk are not followed (`os.walk` default `followlinks=False`): their
   subtree is silently omitted (completeness loss, not disclosure).
4. TOCTOU (LOW, unchanged): the containment/type/size checks and `open(p)` are separate path-based ops;
   no fd is held across check and read. Requires concurrent same-user mutation.

**Can it matter for the counters' snapshot of `~/`? — Not today, on this host.** The C1 counter v4
snapshots `os.path.expanduser("~")` (count-v4.py:361-363), i.e. `/home/vgpnk` under the prescribed
invocation. I verified the current state:

- Every path component of all four roots — `~`, `~/.config`, `~/.config/omarchy/current`,
  `~/.config/omarchy/current/theme`, `~/.local`, `~/.local/share/omarchy/default/hypr`,
  `~/.local/state/omarchy/toggles/hypr` — is a real directory (no symlink component).
- No symlinks exist inside any of the four root subtrees (`find -type l` over each root: empty).
- The only two symlinks under the omarchy trees (`~/.config/omarchy/current/background` and
  `~/.local/share/omarchy/default/chromium/extensions/copy-url/icon.png`) both resolve **inside** HOME
  and lie outside the four roots; they cannot reach the snapshot.
- Measured current snapshot (fresh `snapshot(expanduser("~"))`): `nfiles=79`,
  `digest=fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, contents confined to the
  four roots, no symlinks in the destination (snapshot flattens links to regular files).

So the gap is **not exercisable** by the counter's snapshot of `~/` at this head: the BASE tree is clean.
The C2 suites make no snapshot of `~/` at all (subjects run under bubblewrap with `/home` hidden), so the
gap is irrelevant to C2.

**Conditional impact if a root/ancestor ever becomes an outside-HOME symlink** (e.g. the operator moves
`~/.config/hypr` to another filesystem and links it back): outside regular files (≤1 MiB) would enter the
snapshot tree. Both legs of the C1 comparison (candidate tool at `/snap/home`, and the oracle's copy of
the same case tree) consume the *same* copied tree, and the counter guards oracle stability
(`ORACLE_UNSTABLE`). A deterministic inclusion of outside bytes therefore does **not** corrupt the
41/41 verdict — the comparison stays self-consistent. What the gap changes is the **host-file disclosure
boundary**: host-readable bytes reach the sandboxed candidate tool (and the nested Hyprland's input).
This is exactly the boundary SentinelHarness27 rated MEDIUM; it pre-dates r27 (the r26 harness shares it,
as the rootlink run shows) and r27's fix intentionally covers file-level symlinks only. On this host it is
currently a latent/conditional risk, not an active leak. Same reasoning applies to in-HOME non-config
escapes (finding 2): they would flow to both legs equally; today none exist in the roots.

**Residual risks / verification gaps:**
- The root/ancestor and in-HOME escape paths are code-read plus fixture-verified (rootlink re-run), not
  exercised against the real home (no such symlink exists there; no scenario was manufactured on the
  lane). This is the correct read-only posture.
- TOCTOU remains a theoretical window; counters are single-threaded over a stable home, so likelihood is
  low, but the check/read pair is still non-atomic.
- No live-session reachability was found (unchanged from SentinelHarness27): the case tree never mounts
  the host's live `/run`/socket; Unix sockets are not copied by the regular-file check.
- Recommended remediation (not done — out of scope for a read-only reviewer): validate resolved roots
  against an allowlist and enforce containment against the resolved root rather than HOME; open-by-
  descriptor to close TOCTOU.

## 3. Findings by severity

- **No findings against the w1 evidence receipt** — it re-derives exactly (run3/run4 vs run1/run2
  invariant-identical; rootlink-w2 byte-identical to receipt rootlink.json).
- **MEDIUM (residual, conditional)** — root/ancestor symlink bypass of the r27 per-file guard
  (oracle.py:70-87): outside-HOME bytes can enter the snapshot. Not exercisable on this host today (all
  four roots and ancestors are real dirs; measured snapshot 79 files, digest
  `fe1b2d8b…`, no out-of-root content). Does not affect C1 verdict correctness (both legs get the same
  tree); it is a disclosure-boundary gap. Same class: HOME-wide (not root-wide) containment lets in-HOME
  links escape the selected roots — none present today.
- **LOW (unchanged)** — TOCTOU between guard and read (oracle.py:78-85), theoretical under the counters'
  single-threaded execution.
- **LOW (informational)** — directory symlinks inside a root are silently dropped from the snapshot
  (completeness loss if one ever appears); none today.

## Host safety (this reviewer)

- coredumpctl Hyprland count: before run3 = 1338; after run4 = 1338; after the rootlink helper = 1338;
  delta = 0. No Hyprland/tinywl started; no hyprctl; no WAYLAND_DISPLAY / HYPRLAND_INSTANCE_SIGNATURE
  set or inherited by anything this reviewer started; /dev/dri untouched.
- No lingering probe/launcher/rootlink processes after the runs (`pgrep -af` for
  iso/launcher.py|iso/probe.py|rootlink-snapshot.py: none). Each launcher run is synchronous and returned
  exit=0; the `bwrap` children of these runs had exited on inspection.
- Scratch writes only: `run3.json`, `run4.json`, `canary3.txt`, `canary4.txt`, `rootlink-w2.json`,
  `rootlink-w2.err` under `/fast/scratch/hyaku/mado-r27/iso/` (w1's `run1/2.json`, `rootlink.json`
  untouched). No lane files modified.

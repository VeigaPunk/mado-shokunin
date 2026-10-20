# Safety — scoped report (round 14, w1)

Full findings, anchors and method: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14/w1/Safety.md`.
Seat `MadoR14.Safety` (sentinel, leaf). It ran no tests, gate, selftest or measure, and installed nothing. Its only
writes are these two files and one peer message. Host observations were metadata-only.

Scope: round-14 writes and side effects; the worktree gate's N9–N12 and resolver; `measure.py`; the removed
`receipt.py`; `regular-target.spec`; `evidence/*`; S047–S049; the U5 note; the lesson/LOG tooling record.

**Verdict: no HIGH or MEDIUM finding.** No seat or L1 ran a compositor command, protocol client, live gate,
raw-identity capture or host-config write. This comes from a structured scan of all MadoR14 transcripts up to about
05:47Z, and it supports the U5 note's negative statement at `:55`.

| # | sev | finding | smallest remediation | status |
|---|---|---|---|---|
| F1 | LOW | AttackCoverage ran `jj log`/`jj file annotate` without `--ignore-working-copy`. That created 3 jj ops at 02:41:05 -03, including `snapshot working copy`, so the mid-wave tree was captured into `.jj`. | Disclose it in the lesson. Future read-only jj calls use `--ignore-working-copy` or `git --no-optional-locks`. | open |
| F2 | LOW | OutputSpec installed `wlr-protocols r112.a741f0a-1` (pacman extra, 02:41:32 -03; authorized). `ReviewSourceBar.md:30` and `ScribeFrontier.md:172` still say "not installed". | Recorded in `lessons/round-14.md:100-114` and `LOG.md:974`. Do not cite the stale lines. | record closed |
| F3 | LOW | `/tmp` scratch outside granted paths: `/tmp/ac14`, `/tmp/srcsafety-r14`, `/tmp/cm-35d9638.xml`, `/tmp/wlr-oms-{raw,a741f0a}.xml`. Contents are public upstream bytes, not host data. Round-13 residue (8 selftest dirs, 2 tsv) also remains. | Post-wave `rm -rf` of the listed paths (full report §F3). Mention in the lesson. | open |
| F4 | INFO | A fixed-name `/tmp` git clone is followed by an unconditional `cd`. git 2.55 `safe.directory` mitigates it [INFERENCE]. | Use `mktemp -d`. | note |
| F5 | LOW | GateImplement's reported digest `0a2bf860…` no longer binds the gate, which is now `96e719af…`. | L1 cites only its own measured digest (R13-V3). | open |
| F6 | LOW | `measure.py` listed notes with symbolic `rev`. | Now `rev_sha` at `:147` (sha `e01c75ce…`). | fixed |
| F7 | INFO | N9–N12 live under `$T/census` (mktemp 0700). The resolver uses stat tests only, so a FIFO target cannot hang it. `src_disp` uses `%q`. | Keep as is. | positive |
| F8 | INFO | `-f` follows a symlink to any location. The comment "under `$ROOT`" means expansion, not containment. The check never reads the target. | Wording fix only. | note |
| F9 | INFO | Every `measure.py` write is a fixture mutation inside `TemporaryDirectory`. The gate runs only with `--root <tree> --no-live`. The fixture slice contains only `build_fixture`. | Keep as is. | positive |
| F10 | INFO | `receipt.py` was rejected and removed. Rules for L1's manual receipts: receipt only `--selftest`/`--no-live`/`--regression` (live prints `DP-1 %sx%s@%s`, `root: <HOME>`); never overwrite an existing receipt; use `set -o pipefail` (the `curl \| sha256sum` lines in `evidence/*-source-binding.txt` record sha256sum's exit); any git-fixture selftest scrubs `GIT_*` and uses `GIT_CONFIG_GLOBAL=/dev/null`. | Guidance. | — |
| F11 | INFO | No new device, output or session identity appears in round-14 artifacts, S047–S049 or the corpus diff (0 hits). The `DP-1` text in `SiblingOverlap.md` reproduces committed corpus/gate strings. | Never adopt `hyprctl -j monitors` or `journalctl -k` without in-pipe projection. | positive |

Checks for L1 (not run here):
- `jj --ignore-working-copy op log -n 4`
- `sha256sum tools/mado-verify.sh` at the measured commit
- the F3 cleanup list, then `ls -d /tmp/w5-mado-m52-selftest.* | wc -l` → 0
- add one lesson sentence covering F1 and F3 beside the install record

Tooling: none installed or upgraded by this seat.

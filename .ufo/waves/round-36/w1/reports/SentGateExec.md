# SentGateExec — sentinel security review (round 36 wave 1)

Scope: `quality/check-counter-discrimination.py` (C1 gate), `quality/check-evidence-pointers.py` (C2 gate, PRED-PTR-r36-v1), `.ufo/waves/round-36/c2/gen-mutants.py` (fixture generator). Read-only review; findings, severity, minimal fix.

## 1. Environment injection — `GIT_DIR` forced, ambient `GIT_*` unscrubbed — HIGH

`check-counter-discrimination.py:95-97`
```python
    env = dict(os.environ)
    env["GIT_DIR"] = str(repo / ".git")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
```
`check-evidence-pointers.py:73-77`
```python
def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
```

The gate copies the full ambient environment into every instrument run (and every git call). Any `GIT_*` variable in the caller environment overrides the built-in `GIT_DIR` — `git -C <repo>` does **not** override `GIT_DIR`; the environment is authoritative. Demonstrated:

```
$ GIT_DIR=/tmp/sge-probe/evil/.git git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --name-only HEAD
LOG.md
```
(i.e. `--repo` is silently ignored for object-store reads; listing came from the attacker-specified repo).

Impact: C2's entire verdict is built from `git ls-tree/show/merge-base/status` (lines 124, 130, 162, 180). A caller-controlled `GIT_DIR` (or `GIT_SSH_COMMAND`/`GIT_CONFIG_*` → arbitrary command execution on every git call, `GIT_INDEX_FILE`, `GIT_WORK_TREE`) can fabricate every observable and spoof the verdict. Same vector reaches the C1 gate's git-using C2 counter (`c2-ledger.py:44-46,50,85`). Also `GIT_SSH_COMMAND`/`GIT_ASKPASS` output lands verbatim in receipts (see finding 5).

Minimal fix: build sanitized envs — strip every `GIT_*` key from `os.environ` (`{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}`), then set `GIT_DIR` only when `(repo / ".git").is_dir()`, and set `GIT_WORK_TREE` explicitly. Apply in both `run()` (C1 gate) and `git()` (C2 gate).

## 2. Writes outside declared paths — receipt filename traversal via `control["id"]` — HIGH

`check-counter-discrimination.py:177-181`
```python
            mut = mutant_root / control["id"] / "mutation.txt"
            if mut.is_file():
                body.append("# fixture (generated; regenerate with " + GENERATOR + ")")
                body.append(mut.read_text().rstrip())
            (receipts_dir / f"{control['id']}.txt").write_text("\n".join(body) + "\n")
```
`control["id"]` comes straight from the manifest (`manifest["controls"][i]["id"]`, frozen file but supplied via `--manifest`; no validation). `"../../…"` in an id escapes `receipts_dir` and writes anywhere the process can write, including `quality/receipts/axis-<hex>.txt` (forge the C2 `tip_axis_transcript` observable) or any tracked `.txt`. Demonstrated (same path join, real write):

```
$ python3 -c "from pathlib import Path; d=Path('/tmp/sge-probe/receipts'); d.mkdir(); cid='../../probe-escaped'; (d / f'{cid}.txt').write_text('PWNED')"
$ find /tmp -maxdepth 1 -name 'probe-escaped.txt' -ls
  /tmp/probe-escaped.txt   # created OUTSIDE receipts dir
```

Minimal fix: validate before use — `re.fullmatch(r"[A-Za-z0-9._-]+", control["id"])` (reject `/`, `\`, `..`), and after constructing `p = (receipts_dir / f"{id}.txt").resolve()`, require `p.is_relative_to(receipts_dir.resolve())`. Apply the same guard to `mutant_root / control["id"]`.

## 3. gen-mutants: receipt path traversal (read outside repo, write outside dest) — MEDIUM-HIGH

`gen-mutants.py:180-186`
```python
        for rel in receipt_rels:
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if rel in receipts:
                target.write_bytes(receipts[rel])
            else:
                target.write_bytes((repo / rel).read_bytes())
```
`receipt_rels` comes from `clause_paths(base_ledger)` (`gen-mutants.py:62-68`): the committed clause ledger's `control.receipt` strings. No containment or syntax check. Demonstrated:

```
# ledger control.receipt = "../escaped-target.txt"
$ python3 gen-mutants.py --profile r35 --repo /tmp/sge-gen/repo --out /tmp/sge-gen/out
mutant=m1 profile=r35 dir=/tmp/sge-gen/out/m1
# writes landed in:
$ ls -la /tmp/sge-gen/out/escaped-target.txt /tmp/sge-gen/escaped-target.txt
-rw-r--r-- 1 vgpnk vgpnk  0 … /tmp/sge-gen/out/escaped-target.txt     # inside dest -- expected
-rw-r--r-- 1 vgpnk vgpnk  0 … /tmp/sge-gen/escaped-target.txt          # OUTSIDE dest
```
Read side `(repo / rel).read_bytes()` with `rel = "../../../home/<user>/.ssh/id_ed25519"` copies secret-shaped bytes into fixture files under `/tmp` (world-readable 0644). Severity: MEDIUM-HIGH (content is a committed lane file; attacker influence requires corrupting the ledger — but a bad ledger renders the gate a file read/write primitive).

Minimal fix: validate each `rel` — `PurePosixPath(rel)` must not be absolute and must not contain `.`/`..` parts; write side: require `(dest / rel).resolve().is_relative_to(dest.resolve())`; read side: require `(repo / rel).resolve().is_relative_to(repo.resolve())`.

## 4. Fixed /tmp fixture path + unguarded `rmtree` — MEDIUM

`check-counter-discrimination.py:105`
```python
    mutant_root = Path(args.mutants) if args.mutants else Path(f"/tmp/mado-r36-mutants-{args.profile}")
```
`gen-mutants.py:161-164`
```python
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
```

- The default path is predictable and shared by every run of the gate on the host. Two parallel gate runs (or a same-user attacker) collide: one `rmtree`+regenerates while the other is mid-read → torn fixtures → flaky/garbage `ok` scoring.
- `/tmp` is world-writable with sticky bit (1777, verified). A foreign owner can pre-create `/tmp/mado-r36-mutants-<profile>`; the gate's `shutil.rmtree` then raises (sticky bit refuses deletion of others' files) → gate dies with `PermissionError` → DoS. Race window between `rmtree` and the counter's read also permits fixture swap (TOCTOU, low probability, same-user only since fixtures are 0755 dirs).
- `gen-mutants.py --out` is an unguarded recursive delete: `--out` pointing at any path (e.g. a typo'd `~/Documents` or a lane dir) silently erases it.

Minimal fix: use `tempfile.mkdtemp(prefix="mado-r36-mutants-")` in the gate (unique per run, never re-used), pass that to the generator, and in `gen-mutants` refuse `rmtree` unless `out` is inside `/tmp` and contains a marker file the generator itself created (e.g. `.mado-mutants-<profile>` written at mkdir); also verify `out.stat().st_uid == os.getuid()` before deleting.

## 5. Secret-shaped output captured into committed receipts — LOW-MEDIUM (depends on 1)

`check-counter-discrimination.py:167-181` writes `out` (instrument stdout+stderr, line 173) verbatim into `receipts_dir/<id>.txt`, which is under the lane repo (default `.ufo/waves/round-36/controls/receipts/`). The C2 counter runs git (`c2-ledger.py:50,85`). If the ambient environment (unscrubbed, finding 1) provides `GIT_SSH_COMMAND`/`GIT_ASKPASS`/`GIT_CONFIG_*`, those helpers' output (which may include credentials material) is captured and committed. Even without GIT_*, any instrument stdout is recorded — but today's counters print only verdict lines.

Minimal fix: same scrub as finding 1; additionally, cap `out` length before writing and optionally strip lines matching key patterns (`PRIVATE KEY`, `BEGIN *`, long base64).

## 6. `git()` fail-open + unvalidated `--rev`/`--branch` — LOW

`check-evidence-pointers.py:73-77` returns `""` whenever git exits non-zero. Consequences:
- `git status --porcelain` (line 162) failure → `""` → `inherited_dirty = 0` → observable passes on a *broken* git call, not a clean tree. Fail-open for a gate verdict is a correctness defect.
- `--rev` (line 118), `--branch` (119), used verbatim (lines 124, 180). A `--rev` beginning with `-` is parsed as a git option (e.g. `git ls-tree -r --name-only --help` → usage/error → empty → `die`; demonstrated `error: unknown option 'output=…'`). Not RCE (no shell), but option confusion → silent mis-verdict.

Minimal fix: return `(returncode, stdout)`; treat non-zero as fatal (`die`) for `ls-tree`/`show`/`status`; validate `--rev`/`--branch` against `^[0-9a-f]{40}$` (rev) and a conservative `^[A-Za-z0-9_./-]+$` (branch), or run `git rev-parse --verify --quiet <rev>^{commit}` first and die on failure.

## 7. Path traversal out of `--repo` (manifest/receipts/control root) — LOW-MEDIUM

`check-counter-discrimination.py:85-88,130-132,143`
```python
    repo = Path(args.repo).resolve()
    ...
    manifest_path = (repo / args.manifest).resolve()
    ...
    receipts_dir = (repo / args.receipts).resolve()
    ...
            root = (repo / control["root"]).resolve()
```
No containment checks: `--manifest`/`--receipts` can point anywhere (caller-supplied, so low), but `control["root"]` is manifest-supplied and can name any directory on the system (e.g. `../../etc`); the C1 counter reads it (bounded by `read_regular`'s own guard, `c1-idle-lock.py:44-94`, but the gate's receipt machinery still writes a receipt for it). Minimal fix: helper `inside(root, p) = p.is_relative_to(root)` and enforce for manifest, receipts, and control roots (or an explicit `--allow-outside-repo` opt-in).

## 8. Generator output parsing fragile (`line.split(" ")`) — LOW

`check-counter-discrimination.py:126-128`
```python
        for line in out.splitlines():
            if line.startswith("mutant="):
                parts = dict(p.split("=", 1) for p in line.split(" ") if "=" in p)
                mutants[parts["mutant"]] = Path(parts["dir"])
```
`dir=` with spaces (valid on POSIX) splits wrongly, mapping a mutant to a wrong directory → wrong fixture scored. Minimal fix: don't parse — the gate already knows the mapping (`mutant_root / control["id"]`); use `mutants[control["id"]] = mutant_root / control["id"]` and print only for confirmation.

## 9. Symlink following in writes — LOW (defense-in-depth)

`check-counter-discrimination.py:181` and `gen-mutants.py:184,186` write via `pathlib` `write_text`/`write_bytes`; if an intermediate component (`receipts_dir`, `dest/rel` parent) is a symlink, writes follow it. The receipt dir is created by the gate (owner-only write) and fixture dirs default to fresh `/tmp` paths, so no current attacker path — but the fixes in 2/3 (resolve + containment) close this class too.

## PASSES

- No `shell=True`, no `os.system`/`os.popen`/`Popen` with shell, no `eval`/`exec`, no unquoted shell interpolation anywhere in the three files (grep over all three: zero matches). All subprocess invocations are argv lists (`check-counter-discrimination.py:61`, `check-evidence-pointers.py:74`).
- `gen-mutants.py` uses no git and no environment variables (grep: none).
- C1 gate counter (`c1-idle-lock.py`) is filesystem-only, has a careful symlink/hardlink/no-follow read guard (`read_regular`, `c1-idle-lock.py:44-94`) — internally sound.
- `GIT_DIR=lane/.git` is *intentional and required* for mutant fixtures (mutant dirs are not git repos; `c2-ledger.py` reads the blobs ledger from the filesystem at `repo / spec["blob_ledger"]` and uses git only for tip truth — that split is sound for today's counter). The defect is limited to the missing `GIT_*` scrub and unconditional setting (finding 1).
- No world-writable dirs are created by the scripts (mkdir default 0755 under umask 022; verified stat output). The /tmp risk is fixed-name squat/race, not perms.

## Verification commands (all run, exact outputs quoted)

- `ls -ld /tmp` → `drwxrwxrwt … root root` (sticky, world-writable).
- GIT_DIR override: `GIT_DIR=/tmp/sge-probe/evil/.git git -C <lane> ls-tree -r --name-only HEAD` → `LOG.md` (from evil repo).
- Receipt filename traversal: `find /tmp -maxdepth 1 -name 'probe-escaped.txt' -ls` → `/tmp/probe-escaped.txt`.
- Generator traversal: run with `control.receipt="../escaped-target.txt"` → `/tmp/sge-gen/escaped-target.txt` created outside `--out`.
- Git option injection: `git ls-tree -r --name-only --help` / `--output=…` → `error: unknown option` (no file written).
- `python3 --version` → `Python 3.14.8` (so `Path.is_relative_to` is available for the proposed fixes).

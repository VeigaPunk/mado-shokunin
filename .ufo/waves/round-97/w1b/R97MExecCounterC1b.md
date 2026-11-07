# R97MExecCounterC1b - C1 counter finalised to PRED-C1-r97-v1 (v2)

Seat: `R97MExecCounterC1b` (leaf; no subagent dispatch; no tools installed - no pacman /
uv / npx / binary install, nothing to record per the tooling directive). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. All probes read-only except the scratch
fixture repo (own `git init` under `$S`, no commit anywhere in the lane or fleet repos).
Scratch `$S=/fast/scratch/hyaku/mado-r97/R97MExecCounterC1b` deleted before yield.

## Files changed

- `.ufo/waves/round-97/build/c1-r97-filetype.v2.py` (new; 1791 lines) - sha256
  `745a341e8a2aaefc7283d1ad4090ebde01d631d118f788ddd1dcc7b5195ba9e0`, ASCII-only,
  `python3 -m py_compile` clean, `ast.parse` clean, stdlib only
  (`argparse base64 contextlib hashlib importlib.util io json os posixpath pwd re
  shutil socket stat struct subprocess sys tempfile`; subprocess is the counters'
  sanctioned git / oracle / generator transport, as in the r96 counters).
- `.ufo/waves/round-97/w1b/R97MExecCounterC1b.md` (this report).

The w1 draft `build/c1-r97-filetype.py` (sha `6536b0ae...`) was read, never edited - it
is still owned by the running w1 seat `R97MExecCounterC1`. The v2 file is an independent
deliverable that supersedes it.

## CLI (every argument named; the published counting command uses exactly these 20)

```
python3 -I .ufo/waves/round-97/build/c1-r97-filetype.v2.py --repo <REPO> --rev <REV> \
  --base-rev <BASE_REV> \
  --cases <CASES> --expect-cases-sha256 <CASES_SHA> \
  --mutants <MUTANTS> --expect-mutants-sha256 <MUTANTS_SHA> \
  --genseed <GENSEED> --expect-genseed-sha256 <GENSEED_SHA> \
  --host-list <HOST_LIST> --expect-host-list-sha256 <HOST_LIST_SHA> \
  --host-labels <HOST_LABELS> --expect-host-labels-sha256 <HOST_LABELS_SHA> \
  --host-db <HOST_DB> --expect-host-db-sha256 <HOST_DB_SHA> \
  --expect-tool-sha256 <TOOL_SHA> --expect-mimeglob-sha256 <MIMEGLOB_SHA> \
  --expect-mimesniff-sha256 <MIMESNIFF_SHA> --expect-mimetext-sha256 <MIMETEXT_SHA> \
  --expect-gio-sha256 <GIO_SHA> \
  --forgery <FORGERY> --expect-forgery-sha256 <FORGERY_SHA> \
  --scratch-root <SCRATCH>
```

New vs the w1 draft: `--host-labels` + `--expect-host-labels-sha256` (both pinned and
counted in the pin-format / existence / sha256 setup gates). No hardcoded input
filenames; every `--expect-*-sha256` is a 64-hex pin checked before anything runs; one
`MADO_FILETYPE_COUNT:` verdict line.

## Behaviour (contract 2 + the revised L1 requirements, all folded)

- **Committed host labels (L1 C1-6).** `--host-labels` is JSONL, one
  `{"path","label"}` object per host-list path (a trailing summary line is skipped). The
  host leg scores the tool against these COMMITTED labels, never a live oracle re-run;
  a fresh live `gio info -a standard::content-type` pass over the same db root is
  reported only as the `host_drift` note (informational, never scored). The label
  path-set must equal the host list exactly (`setup-host-labels-mismatch` otherwise).
  Verdict atoms `host_paths host_mismatches host_errors host_drift` are printed.
- **Fresh labels normalised (L1).** `case_labels()` accepts a label as a plain string
  OR a one-element list; the fresh generator emits one-element lists, the frozen set
  mixes both. `score_case` / `score_fresh_case` / `score_naive` / `score_memoriser` all
  go through `case_labels`.
- **`missing` path type + ERROR cases (L1).** `missing` is never materialised; it must
  carry an ERROR label (frozen only - fresh cases forbid ERROR labels, rule 7). The
  tool's `MADO_FILETYPE: ERROR stat ...` line plus overall exit 2 is scored; the other
  paths are still answered.
- **Trailing-slash paths (L1).** The raw spelling (e.g. `plain/`) is scored against the
  tool and the oracle; the slash is stripped only for filesystem operations
  (`rp_fs = rp.rstrip("/")`), for device `lstat`, and for the `files` membership rule.
- **`dir-unreadable` type (L1).** A directory materialised with every other file first,
  then `chmod 000` LAST; `locked` dirs are chmod'd back to `0700` (`_release_locked`)
  before scratch removal.
- **Credential guard fail-closed (L1).** `credential_hits` now resolves absolute home
  paths via `os.path.expanduser` + `pwd.getpwuid` (`_cred_homes`) in addition to the
  relative-prefix rules, so `/home/vgpnk/.ssh/id_rsa`, `/etc/shadow`,
  `/home/vgpnk/.config/gh/hosts.yml` are all caught. On the frozen 6194-path host list
  the guard reports `credential_guard=0`; an injected credential path is refused with
  rc 2 (red run below).
- **Census minimums -> verdict atoms (L1).** `>=MIN_CASES` (120), `>=MIN_PER_CLASS` (8),
  `>=MIN_HOST_PATHS` (1500), `>=MIN_FRESH_CASES` (120) are TARGET_MISSED atoms
  (`census cases=... host=... fresh=...` on the verdict line), not SETUP_ERROR gates, so a
  small scratch fixture still runs every leg. Schema / sha / credential / envelope
  failures stay SETUP_ERROR.
- **Fresh leg scored in place (L1).** The generator builds each case root under
  `work/freshroots-<tag>` (inside the audit allowlist) so the tool can open it; only the
  JSONL `--out` lives under `secret` (outside the allowlist). `fresh_cases` returns
  `(case, root)` pairs and `score_fresh_case` scores the built root in place (the
  generator's `files` carries only the db tree, so re-materialise is impossible).
- **Host db mode inference (L1).** `build_host_db` takes `mode` from the manifest, or
  infers it from the file kinds when absent (cache iff a `mime.cache` entry is declared,
  else text). `source.dir` may be the XDG data dir (holds `mime/`) or the mime dir itself
  (`_mime_dir`). The frozen `host-db-r97.json` has no `mode` key and declares `mime.cache`
  -> cache mode, dbroot `/usr/share`.
- **Host allow realpath (measured fix).** The tool content-sniffs host paths following
  symlinks, so the audit allow is extended with the TOP-LEVEL root of every host path's
  REALPATH (`/usr /etc /dev /proc /sys /run /opt`), not just the path-component roots -
  `/etc/resolv.conf -> /run/systemd/resolve/stub-resolv.conf` must stay readable. A
  per-directory allow would be pid-unsafe for `/proc/self/*` (realpath resolves `self`
  to the counter's pid, not the tool subprocess's).

## Dry run (green) - rc 1 TARGET_MISSED, every leg evaluated

Fixture: scratch git repo (`base-rev` = the three siblings only, `rev` = siblings +
`tools/mado-filetype.py` = candidate sha `da6af7a0...`), 12 frozen cases (10 real draft
cases incl. trailing-slash `dir-01`/`dir-05`, plus crafted `dir-unreadable` and
`missing`/ERROR), 2 mutants, a ctypes-libgio forgery, the REAL frozen host list +
labels + genseed + host-db manifest. Command = the CLI above with the fixture pins.

Key output lines (full transcript in scratch, deleted before yield):

```
base: tools/mado-filetype.py absent at base-rev 7d27fc13... (declared before 0/0)
tool_pin=ok sibling_pins=ok,ok,ok (mimeglob mimesniff mimetext)
host list paths=6194 labels=6194
host_db=cache files=9 root=/usr/share
static_findings=none
selftest rc=0 checks=40 failed=0 fail_lines=0 ok=True
fresh_seed=d0588e96e71f123c fresh=140/140
control memoriser frozen=12/12 fresh=0/140
host=6194/6194 host_paths=6194 host_mismatches=0 host_errors=0 host_drift=0
audit_denials=0
mutant dir-01-dir-to-fifo killed by dir-01-plain-subdir (+2)
mutant chr-01-chr-to-blk killed by chr-01-dev-null (+0)
control_nameonly=2/12 control_fastproxy=10/12 control_naive=7/12
control forgery static=import:ctypes:1,... forgery_audit_denials=3 rejected=True
MADO_FILETYPE_COUNT: TARGET_MISSED pred=PRED-C1-r97-v1 ... cases=12 correct=12
  classes=15/15 ... mutants=2 killed=2 ... class_kills=3/15 fresh=140/140 ...
  host=6194/6194 host_paths=6194 host_mismatches=0 host_errors=0 host_drift=0
  census cases=FAIL host=ok fresh=ok static_structural=ok audit_denials=0
  forgery=rejected ... memoriser_frozen=12/12 memoriser_fresh=0/140
  selftest=ok checks=40 failed=0 host_db=cache files=9 credential_guard=0
RC=1
```

The frozen leg scored `correct=12/12` including the crafted `dir-unreadable` and
`missing`/ERROR cases, and the trailing-slash `dir-01`/`dir-05` cases - the new path
types materialise and score correctly. The host leg scored all 6194 committed labels
with `host_mismatches=0 host_drift=0`. TARGET_MISSED is the expected small-fixture
result (`census cases=FAIL` - 12 < 120 cases, several classes < 8); every leg ran.

## Credential-guard red run - rc 2 SETUP_ERROR

Same command with `--host-list` = the frozen list plus one injected line
`/home/vgpnk/.ssh/id_rsa` (sha `cca0bd8f...`):

```
host list paths=6195 labels=6194
MADO_FILETYPE_COUNT: SETUP_ERROR pred=PRED-C1-r97-v1 credential-shaped host path:
  /home/vgpnk/.ssh/id_rsa credential_guard=1
RC=2
```

The guard fires before the label path-set cross-check and before any host byte is read.

## Risks / blockers

- None blocking. The w1 seat `R97MExecCounterC1` is still running on the draft
  `c1-r97-filetype.py`; this v2 is independent and supersedes it. If Main prefers the
  w1 file, the v2 changes (committed host labels, new path types, census atoms, host
  allow realpath) must be ported - flagged, not actioned (leaf seat).
- The frozen cases/mutants/forgery files used here are a scratch subset/craft, not the
  landed frozen controls; the published measurement uses the frozen
  `filetype-cases-r97-frozen.json` (140 cases) and the landed mutants/forgery when those
  seats land. The counter's schema/envelope validation accepts the landed draft
  envelope (verified: version/oracle/gio_sha256/glib2/classes all match).
- Host leg runtime ~100 s for 6194 paths (tool chunks + the live-gio drift pass); well
  within budget.

Report: .ufo/waves/round-97/w1b/R97MExecCounterC1b.md

# MadoR19.AdvFrozen — partial

Attack seat for the round-19 wave-2 item "adversarial test of `--frozen` after
F1/F2". Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`,
integrated tip `01b80946d92b26370d3012a7da655d00dd135154`. Every run used a
byte-identical copy of the committed tool:

```
$ git show 01b80946d92b26370d3012a7da655d00dd135154:tools/mado-tripwire.py > /tmp/advfrozen-tip.py
$ sha256sum /tmp/advfrozen-tip.py tools/mado-tripwire.py
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  /tmp/advfrozen-tip.py
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  tools/mado-tripwire.py
Python 3.14.8
```

All fixtures are synthetic OMP-shaped JSONL (`message.role=assistant`,
`content[].type=toolCall`, `name=bash`, `arguments.command`) built under
`/tmp/advfrozen`; no real transcript line was copied. 69 frozen invocations
(21 symlinked-DIR spellings, 17 real-directory spellings and controls, 14
inputs attacks, 2 expected.json symlinks, 5 pin-spelling cases, 7 F1
re-verifications, 3 argument edges), 10 single-line `--scan` probes, two
committed suites and both committed baselines were run.

Verdict summary:

| under attack | result |
|---|---|
| F2: symlinked DIR via `link/.`, `link/./`, `link//`, `link/inputs/..`, `link/../evil`, chain/deep/foreign-cwd spellings | **holds** — 21/21 rejected `snapshot_tampered`/2; controls still match |
| F1: blank / whitespace / phantom / past-end pin → `frozen_error`/2 (also known_misses) | **holds** — all re-measured at tip and via the committed suite (13/13) |
| docstring: "an unreachable pin is frozen_error, never a failed verdict" (`tools/mado-tripwire.py:91-94`) | **breaks** for the `expected_findings[].file` field: an accepted pin naming a listed input is replayed as `frozen_verdict_mismatch`/1, `error` absent |
| docstring: "a leaf symlink or an unlisted `*.jsonl` is snapshot_tampered" (`:90-91`) | **false** for a symlink-to-directory entry under `inputs/`, whether or not it is named `*.jsonl`; measured `frozen_match`/0 |
| (not a declared clause) `DIR/expected.json` identity | gap: a symlink to a pin outside DIR is accepted, including another snapshot's pin; `frozen_match`/0 |

## 1. F2 — symlinked directory spellings: holds

Fixtures: `real/` (pinned snapshot), `link -> real`, `link2 -> link`,
`deep/anc -> ../real`, `anc2 -> .`, `sub/ancsub -> ..`. Every symlinked-DIR
spelling was rejected:

| spelling | got |
|---|---|
| `link`, `link/`, `link/.`, `link/./`, `link//` | 2 `snapshot_tampered`, error `frozen directory is a symlink` |
| `link/inputs/..`, `link/./inputs/..`, `link/../link`, `real/../link` | same |
| `deep/anc`, `deep/anc/.`, `deep/anc/inputs/..` | same |
| `link2`, `link2/.` (symlink chain) | same |
| `sub/ancsub/./link`, `sub/ancsub/../advfrozen/link`, `real/../../advfrozen/link` | same |
| `anc2/link` (symlinked ancestor plus final symlink) | same |
| `advfrozen/link/./` run from cwd `/tmp`; `../link/./` run from `.../sub` | same |

The real directory in 17 spellings returned `frozen_match`/0, including
`real/`, `real/.`, `real//`, `real/inputs/..`, `real/./inputs/..`,
`real/../real`, `sub/../real`, `real/inputs/../../real`, `anc2/real`
(ancestor symlink above DIR), the same spellings from two foreign cwds, and
`./` invoked from inside the real directory. The committed suite reproduces
from a foreign cwd (`cd /tmp; ... --selftest <abs>/r19-frozen-f1f2` →
`SELFTEST_SUMMARY: 13/13 passed failed=[]`, rc 0), and direct absolute
spellings on the committed symlink fixtures also reject:

```
$ python3 -I /tmp/advfrozen-tip.py --frozen '<lane>/.ufo/waves/round-19/tripwire/r19-frozen-f1f2/f2-symlink-dir-dot/./inputs/..'
MADO_TRIPWIRE_FROZEN: snapshot_tampered
$ ... --frozen '//<lane>/.../r19-frozen-f1f2/f2-symlink-dir-dot/.//'
MADO_TRIPWIRE_FROZEN: snapshot_tampered
$ cd .../f2-symlink-dir-dot/../f2-target && ... --frozen ./
MADO_TRIPWIRE_FROZEN: frozen_match
```

Boundaries found, not bypasses: `in-sym/inputs/..` (D1c) resolves to `real/`
and matches because the *final* directory is the real snapshot, not an alias
of it; `deep/anc/../real` (C7) is rejected because a prefix symlink resolves
to the real dir even though the path leaves it again — conservative, and
consistent with `frozen_dir_symlinked` (`:1894-1912`). No spelling was found
that resolves a symlinked DIR while leaving every prefix's `realpath` unequal
to `realpath(DIR)`; that is the exact predicate the walk enforces.

## 2. F1 — blank/reachability pins: holds

Re-measured with correctly pinned bytes (my first attempt pinned the wrong
digest and was discarded — the fix is why every G fixture below carries its
own sha256):

| fixture | pin | got at tip |
|---|---|---|
| G1 line 2 empty | expected finding line 2 | 2 `frozen_error` "line 2 … is blank" |
| G2 line 2 `" \t "` | expected finding line 2 | 2 `frozen_error` "line 2 … is blank" |
| G3 line 3 of 2 | expected finding line 3 | 2 `frozen_error` "line 3 is past the end" |
| G4 line 2 = UTF-8 NBSP | expected finding line 2 | 2 `frozen_error` "invalid line (JSONDecodeError)" |
| G5 known_miss line 2 empty | known miss line 2 | 2 `frozen_error` "known_misses line 2 … is blank" |
| G6 pin on line 3 of `record\n\n` | expected finding line 3 | 2 `frozen_error` "line 3 … is blank" |
| G7 line 1 is `{"type":"note"}` | expected finding line 1 | 1 `frozen_verdict_mismatch`, 1 missing / 2 extra (control, unchanged) |

I specifically looked for a split between the reachability blank rule and the
scanner's skip rule (the only way F1 could fail): `frozen_snapshot` builds
`stats` from `data.split(b"\n")` + `r.strip()` and `scan_file` re-reads the
same digest-checked bytes and skips on `raw.strip()` — both are **bytes**
strip, so a `\xa0`-only line is non-blank to both and dies later as
`could_not_evaluate`, not as a blank-pin mismatch. No text-mode decoding sits
between them. The committed f1/f2 suite passes 13/13 at the tip tool; the
round-18 frozen suite still passes 31/31.

## 3. Finding 1 (break): an accepted pin on the `file` field is unreachable and reported as a failed verdict

`validate_frozen` accepts an `expected_findings[].file` (and
`known_misses[].file`) that merely *normalizes* into the listed set:

```
tools/mado-tripwire.py:1756   if os.path.normpath(w["file"]) not in listed:
tools/mado-tripwire.py:1776   if os.path.normpath(k["file"]) not in listed:
```

but the verdict compares the **raw** strings: findings are rewritten to the
canonical listed path (`:1956 f["file"] = e["path"]`, input paths constrained
by `FROZEN_PATH = inputs/[A-Za-z0-9._-]+\.jsonl`, `:1651`), while expected rows
keep whatever spelling the pin used (`:1963-1964 got = Counter(key(f) …);
expected = Counter(key(w) for w in pinned["findings"])`). A file spelling that
normpath-collapses *inside* `inputs/` therefore passes validation and can
never match, producing `frozen_verdict_mismatch`/1 with `error` absent instead
of `frozen_error`/2 — contradicting `:93-94` ("an unreachable pin is
frozen_error, never a failed verdict").

Synthetic snapshot `real/` (line 1 pins `sudo` + `pacman:-Syu`):

| pin spelling | got |
|---|---|
| `inputs/./incident.jsonl` | 1 `frozen_verdict_mismatch`, missing 2, extra 2, `error: null` |
| `inputs/../inputs/incident.jsonl` | same |
| `inputs//incident.jsonl` | same |
| `inputs/../incident.jsonl` (escapes the listed set) | 2 `frozen_error` (control — validation does reject this) |
| same spelling in `known_misses` instead | 0 `frozen_match` (control — known misses are only reachability-checked) |

The same class exists on committed bytes, so it is pre-existing and not
introduced by the F1/F2 patches. On a `/tmp` copy of the round-18 baseline
with exactly one expected row rewritten `inputs/r15-libinput-events.jsonl` →
`inputs/./r15-libinput-events.jsonl`:

```
# base tool 9c54c56 (c1ae45a7…), copy of .ufo/waves/round-18/frozen
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch   rc=1
error=None missing=1 extra=1
missing ["inputs/./r15-libinput-events.jsonl",1,host_mutation,sudo]
extra   ["inputs/r15-libinput-events.jsonl",1,host_mutation,sudo]
# tip tool, same copy
rc=1 error=None missing=1 extra=4   (the 3 extras are the declared C3 signal, see §6)
# same edit with inputs//…  on the base tool
rc=1 error=None missing=1 extra=1
```

On the **current** committed baseline `.ufo/waves/round-19/frozen`
(sha256 `50d2a45e…`, 11 expected findings) the identical edit yields:

```
$ cp -a .ufo/waves/round-19/frozen /tmp/advfrozen-r19/base   # pristine
MADO_TRIPWIRE_FROZEN: frozen_match                      rc=0  sha=50d2a45e2602cb43
# expected_findings[0].file := inputs/./r15-libinput-events.jsonl
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch           rc=1  error=None
missing=1 extra=1  sha=7d15e8e0ac8cfabb
```

The pin is unreachable by construction: no scan can emit a `file` value that
is not one of the listed canonical paths, and `FROZEN_PATH` forbids the odd
spelling (`:1725` rejects a *listed* path of that shape with `frozen_error`).
Two fixes satisfy the docstring: reject non-canonical `w["file"]`/`k["file"]`
in `validate_frozen` (`frozen_error`, the proposed case), or normalize both
sides before `Counter` comparison (then the same pin is `frozen_match`/0).
The one outcome the contract excludes is the measured exit 1.

## 4. Finding 2 (overclaim): a symlink-to-directory under `inputs/` is invisible to both completeness rules

`:90-91` promises that "a leaf symlink or an unlisted `*.jsonl` is
snapshot_tampered". `frozen_snapshot` checks only *listed* entries with
`lstat` (`:1830-1838`) and then walks the spelled `inputs/` with
`followlinks=False` (`:1855`), consuming `names` only (`:1857-1862`). A
symlink whose target is a directory is classified by `os.walk` into `dirs`,
never `names`, and is not descended — so it is neither a rejected leaf nor a
seen unlisted name. Measured at tip:

| fixture under `inputs/` | got |
|---|---|
| `linked -> ../../real/inputs` (holds `incident.jsonl`, unpinned) | 0 `frozen_match` |
| `box.jsonl -> ../../real/inputs` (unlisted, name ends `.jsonl`) | 0 `frozen_match` |
| `sub/x.jsonl` in a **real** subdir (control) | 2 `snapshot_tampered` |
| `sub/link.jsonl` symlink in a real subdir (control) | 2 `snapshot_tampered` |
| `again -> .` (cycle) | 0 `frozen_match`, no hang |

Also on the round-19 baseline copy (`inputs/box.jsonl` added):

```
MADO_TRIPWIRE_FROZEN: frozen_match   rc=0  sha=50d2a45e2602cb43  error=None
```

Replay soundness is *not* broken: `FROZEN_PATH` forbids `/` in a listed path,
so no pin can ever name a file behind such a link, and every file that *is*
scanned digest-verifies. What is false is the completeness promise: JSONL
bytes reside under the snapshot's `inputs/` and are not pinned or flagged.
This is a guard/documentation mismatch (low severity today, load-bearing if
subdirectory inputs are ever admitted); the proposed cases pin the documented
reading, with the alternative being to narrow `:90-91` to "a listed leaf
symlink".

## 5. Finding 3 (gap, not a literal clause): `expected.json` may itself be a symlink out of DIR

`run_frozen` opens `os.path.join(directory, "expected.json")` with no
`lstat`/containment check (`:1920`), unlike every input path. On a snapshot
copy whose `expected.json` is a symlink to the saved pin outside DIR:

```
# round-18 copy -> <lane>/.ufo/waves/round-18/frozen/expected.json
base 9c54c56: MADO_TRIPWIRE_FROZEN: frozen_match  rc=0  error=None
# round-19 copy -> /tmp/…/expected-copy.json (byte-identical copy outside DIR)
tip:          MADO_TRIPWIRE_FROZEN: frozen_match  rc=0  sha=50d2a45e2602cb43
# synthetic copy whose expected.json points at a *different* snapshot's pin
tip:          MADO_TRIPWIRE_FROZEN: frozen_match  rc=0  scan_label=permitted_only
```

So `--frozen DIR` is not self-contained: copying or committing `DIR` alone
does not carry its pin, and a re-pointed link silently applies another
snapshot's permit/expected set (the output's `expected_sha256` still names the
bytes read, so it is auditable, but nothing refuses it). The docstring only
constrains `inputs` paths; I report this as a hardening proposal, not as a
contradiction of a declared sentence. `[INFERENCE]` A committed git symlink
still replays its target's bytes in a checkout, so "reproduces the pinned
verdict" remains literally true; "snapshot" self-containment does not.

Doc nit, same paragraph: `:90` classifies "an escaping path" as
`snapshot_tampered`, but the committed suite pins `path-traversal` and
`absolute-input` to `frozen_error`
(`.ufo/waves/round-18/tripwire/frozen/expected.json:136-151`), which is what
`:1725` does. The code and suite agree; the sentence does not.

## 6. Baseline cross-check (not a finding — declared signal reproduced)

```
$ python3 -I /tmp/advfrozen-base.py --frozen .ufo/waves/round-18/frozen   # 9c54c56 bytes
MADO_TRIPWIRE_FROZEN: frozen_match                       rc=0
$ python3 -I /tmp/advfrozen-tip.py  --frozen .ufo/waves/round-18/frozen  # 01b8094 bytes
MADO_TRIPWIRE_FROZEN: frozen_verdict_mismatch            rc=1
missing=0 extra=3
extra: r13-root:4, r14-source-safety:2, r14-source-safety:3 (package_query pacman:-Q)
$ python3 -I /tmp/advfrozen-tip.py --frozen .ufo/waves/round-19/frozen
MADO_TRIPWIRE_FROZEN: frozen_match                       rc=0  sha=50d2a45e2602cb43
```

Both outcomes are the pre-registered ones: the committed `SCORECARD.md:1106-1110`
says the round-18 baseline "must then read `frozen_verdict_mismatch`, which is
the change made visible"; `TwMerge.md:154-166` names exactly these three former
known-miss lines. The round-19 re-pin is committed at
`.ufo/waves/round-19/frozen` (its `expected.json` hashes to `50d2a45e…`, and
`README.md:5,20,39` records the source pin, the `frozen_match` replay and 11
expected findings), and reproduces at tip. I confirmed all of these.
The three new findings come from the merged helper-call detection, not from
F1/F2 (`TwHelperFn.md:75-91` says the same), so F1/F2's isolated "baseline
stays `frozen_match`" claims are not falsified by the tip — they were measured
on single-patch tools. `--selftest` at tip: `r19-frozen-f1f2` 13/13,
`round-18/tripwire/frozen` 31/31.

## 7. Ten synthetic single-line `--scan` probes (requested class/rule/exit)

Each line is one assistant `toolCall`; each was scanned alone:

```
python3 -I /tmp/advfrozen-tip.py --scan /tmp/advfrozen/scan-lines/<id>.jsonl
```

| id | `command` in the line | expected | got (exit / class:rule,line) |
|---|---|---|---|
| S1 | `python3 -I /tmp/advfrozen/tip.py --frozen 'real/inputs/..'` | clean/0 | clean/0, none |
| S2 | `… --frozen 'link/./'` | clean/0 | clean/0, none |
| S3 | `… --frozen 'deep/anc/inputs/..'` | clean/0 | clean/0, none |
| S4 | `… --frozen 'in-sym/.//'` | clean/0 | clean/0, none |
| S5 | `… --frozen 'in-sub-linkdir'` | clean/0 | clean/0, none |
| S6 | `… --frozen 'in-sub-linkdir/linked/..'` | clean/0 | clean/0, none |
| S7 | `cd /tmp/advfrozen/sub && … --frozen ../link/./` | clean/0 | clean/0, none |
| S8 | `… --frozen 'real/../real'` | clean/0 | clean/0, none |
| S9 | `sudo pacman -Syu` (control) | findings/1 | findings/1, `host_mutation:sudo,1`; `host_mutation:pacman:-Syu,1` |
| S10 | `git commit -m x` (control) | findings/1 | findings/1, `vcs_write:git:commit,1` |

The eight path probes are clean by design — the scanner has no path-shape
rules; the frozen gate is the only place these spellings are judged. That is
why the matrix in §1, not `--scan`, is the evidence for F2.

## 8. Proposed regression cases (suite format)

Built at `/tmp/advfrozen-proposed` (`expected.json` sha256
`145d51126207f2c7b902a6065adf22070cab7bdcf913b623cbf88e962ef11d8a`,
argument paths relative to the suite dir, symlinks relative). Measured at tip:
`SELFTEST_SUMMARY: 5/10 passed failed=['adv-pin-file-dot',
'adv-pin-file-dotdot', 'adv-inputs-leaf-dirlink-jsonl',
'adv-inputs-subdir-symlink', 'adv-expected-json-symlink']`
(`SELFTEST_SCRIPT_SHA256: 367be947…`, rc 1). The five controls pass, including
`adv-link-dot` (2/`snapshot_tampered`), `adv-ancestor-symlink-control`
(0/`frozen_match`), `adv-real-inputs-dotdot` (0/`frozen_match`) and
`adv-blank-line-pin` (2/`frozen_error`).

```json
{
 "schema": "mado-tripwire-selftest-v1",
 "note": "synthetic OMP-shaped JSONL only; proposed round-19 w2 frozen regressions",
 "cases": [
  {"name": "adv-real-control", "mode": "frozen", "args": ["adv-real"],
   "want_exit": 0, "want_label": "frozen_match", "want_missing": 0, "want_extra": 0},
  {"name": "adv-link-dot", "mode": "frozen", "args": ["adv-link/."],
   "want_exit": 2, "want_label": "snapshot_tampered", "want_missing": 0, "want_extra": 0},
  {"name": "adv-ancestor-symlink-control", "mode": "frozen", "args": ["adv-ancestor/adv-real"],
   "want_exit": 0, "want_label": "frozen_match", "want_missing": 0, "want_extra": 0},
  {"name": "adv-real-inputs-dotdot", "mode": "frozen", "args": ["adv-real/inputs/.."],
   "want_exit": 0, "want_label": "frozen_match", "want_missing": 0, "want_extra": 0},
  {"name": "adv-blank-line-pin", "mode": "frozen", "args": ["adv-blank"],
   "want_exit": 2, "want_label": "frozen_error", "want_missing": 0, "want_extra": 0},
  {"name": "adv-pin-file-dot", "mode": "frozen", "args": ["adv-pin-file-dot"],
   "want_exit": 2, "want_label": "frozen_error", "want_missing": 0, "want_extra": 0,
   "note": "docstring: an unreachable pin is frozen_error; literal file compare makes it unreachable"},
  {"name": "adv-pin-file-dotdot", "mode": "frozen", "args": ["adv-pin-file-dotdot"],
   "want_exit": 2, "want_label": "frozen_error", "want_missing": 0, "want_extra": 0,
   "note": "same class with an inputs/x/../x spelling"},
  {"name": "adv-inputs-leaf-dirlink-jsonl", "mode": "frozen",
   "args": ["adv-inputs-leaf-dirlink-jsonl"], "want_exit": 2,
   "want_label": "snapshot_tampered", "want_missing": 0, "want_extra": 0,
   "note": "proposal: an unlisted *.jsonl leaf symlink under inputs is snapshot_tampered"},
  {"name": "adv-inputs-subdir-symlink", "mode": "frozen",
   "args": ["adv-inputs-subdir-symlink"], "want_exit": 2,
   "want_label": "snapshot_tampered", "want_missing": 0, "want_extra": 0,
   "note": "proposal: a symlink below inputs is snapshot_tampered"},
  {"name": "adv-expected-json-symlink", "mode": "frozen",
   "args": ["adv-expected-json-symlink"], "want_exit": 2,
   "want_label": "snapshot_tampered", "want_missing": 0, "want_extra": 0,
   "note": "proposal: DIR/expected.json must be a regular file inside DIR"}
 ]
}
```

Case groups: rows 1-5 are controls that pass today; rows 6-7 encode the
docstring's explicit "unreachable pin → `frozen_error`" rule (and pass if the
comparison is normalized instead, yielding `frozen_match`/0 — either fix is
acceptable, the current exit 1 is not); rows 8-10 encode the docstring's
symlink/unlisted promise and a self-containment policy for `expected.json`.
If L1 chooses the permissive policy for rows 8-10, the docstring at `:90-91`
must be narrowed to match the code rather than the reverse.

## 9. Retained evidence index

- `/tmp/advfrozen/results.json` — 79 case records (69 frozen + 10 scan) with
  rc, first line, error, missing/extra rows, tool sha.
- `/tmp/advfrozen-baseline/results.json` — baseline copies, spelling edits,
  expected.json symlinks, repin.
- `/tmp/advfrozen-proposed/expected.json` + fixtures — the suite above.
- `/tmp/advfrozen-tip.py`, `/tmp/advfrozen-base.py` — tool bytes, sha256 as
  quoted (tip `367be947…`, base `c1ae45a7…`).
- Lane anchors: `tools/mado-tripwire.py:87-94` (claims), `:1651` (path regex),
  `:1702-1789` (`validate_frozen`), `:1725` (listed-path reject), `:1756-1757`
  (normpath accept), `:1787-1807` (`validate_reachable`), `:1811-1890`
  (`frozen_snapshot`), `:1847` (inputs realpath), `:1855` (walk,
  `followlinks=False`), `:1894-1912` (`frozen_dir_symlinked`), `:1915-1977`
  (`run_frozen`), `:1920` (expected.json open), `:1956` (canonical finding
  file), `:1963-1964` (raw Counter compare); `.ufo/waves/round-18/tripwire/
  frozen/expected.json:136-151`; `SCORECARD.md:1106-1110`;
  `.ufo/waves/round-19/frozen/README.md:5,20,39`;
  `.ufo/waves/round-19/w1/reports/TwMerge.md:154-166`;
  `.ufo/waves/round-19/w1/reports/TwHelperFn.md:75-91` (all cited as
  committed-tip bytes; the lane worktree moved under sibling wave-2 edits).

## Limits

- A true **bind mount** of a frozen DIR (or of `inputs/`) is not constructible
  without root, and the host pause forbids `sudo`/mount operations.
  `[UNK]` whether a bind would be accepted; by code reading it would be
  (`realpath` differs, no symlink), but it presents the same inode/bytes and
  the same digest pins, so I judge it host layout rather than a replay bypass
  `[INFERENCE]`. The `..`-segment "bind" spellings requested by the item
  (`real/inputs/..`, `real/../real`, `real/inputs/../../real`, `sub/../real`,
  `sub/ancsub/./real`) were all exercised and match.
- The TOCTOU window between `frozen_dir_symlinked` (`:1894`) and the later
  `open`/scan was not raced. It is inherent to path checks and is the class
  the F2 report already admits as a coordinated rewrite (round-18 A1/A1c).
- `expected.json` symlinks and symlinks below `inputs/` are reported as
  policy proposals; the docstring does not explicitly name `expected.json`, and
  "under inputs" is ambiguous for a non-followed symlinked subtree. Rows 8-10
  should be adjudicated before landing.
- All experiments used Python 3.14.8; `os.walk`/`realpath`/`split` semantics on
  another interpreter were not measured.
- The lane worktree was being written by sibling wave-2 seats while this ran
  (`SCORECARD.md`, `corpus/*.md` and `.ufo/waves/round-19/landed-check.sh`
  show uncommitted sibling edits at the end). My target was the committed tip
  blob and `tools/mado-tripwire.py` still hashed to `367be947…` throughout;
  one early citation I took from a concurrently edited `SCORECARD.md` line was
  replaced with committed-tip anchors above.
- I ran no gate (neither `--selftest` nor `--regression`) and no copy of it; no
  package, service, compositor, walker, transcript read, or jj command. Lane
  access was read-only (`git show`, `sha256sum`, suites); I ran the lane's
  `frozen-repin.py` once with output to `/tmp` only. Only this report was
  written in the lane. Scratch under `/tmp` is shared with sibling seats, so
  the hashes above identify the exact bytes used.
- The per-line `--scan` probes are command-text classifications only; they
  cannot and do not exercise `--frozen` path logic.

## Installs

none

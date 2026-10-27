# ScoutFreezeBlobs — w2 falsify: freeze/data artifact inventory

Round 48, wave w2 (FALSIFY), policy v1. Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`, freeze commit
`3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Leaf seat: read-only on the lane; the only files I wrote are `w2/ScoutFreezeBlobs/artifact-manifest.tsv` and
`w2/ScoutFreezeBlobs/artifact-summary.json` beside this report.

**Verdict for the freeze/data commits: the required artifact set is complete and byte-consistent. No path anywhere in the
set exceeds 1 MiB (largest 257,131 B), so no size-skipping commit helper can drop a required file. Zero missing
registration-required artifacts, zero digest mismatches, zero drift between the freeze commit and the worktree. Seven
observations are recorded below; none breaks `PRED-C1-r48` or `PRED-C2-r48`.**

## Method (absolute paths only)

| purpose | command |
|---|---|
| freeze tree | `git -C <lane> ls-tree -r -z --long HEAD -- .ufo/waves/round-48` (770 entries) |
| worktree set | `python3 os.walk('/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48')` |
| drift | per tracked path `git hash-object -- <abs path>` vs the HEAD blob id (770/770) |
| C1 digest literals | `sha256sum quality/counters/c1-r47-fixtures.json quality/counters/c1-r48-fixtures.json .ufo/waves/round-47/fetch/xdg-terminal-exec /usr/bin/xdg-terminal-exec` |
| C2 pins | every `sha256:`+`receipt .ufo/waves/round-48/fetch/...` pair in all 11 rows of `l1-draft/rows-c2.md`, re-hashed from disk |
| held pins | `.ufo/waves/round-46/fetch/Hyprland-ConfigValues.cpp`, `Hyprland-IKeyboard.cpp` re-hashed against S318/S319 |
| control manifest | `cd .ufo/waves/round-48/w1/ExecControlsC1 && awk '{print $1"  "$2}' receipts/artifact-hashes.txt \| sha256sum -c --quiet` → rc 0 |
| data-commit set | `git status --porcelain=v1 -z -uall` + per-path `stat`/`sha256sum`, `cmp` against seat/draft sources |
| appends | `git show HEAD:<path>` vs worktree `difflib.unified_diff(n=0)`; fragment lines matched verbatim |

All shell writers opened with `ulimit -f 2048` (1 MiB/regular file). Scratch: `/fast/scratch/hyaku/mado-r48/ScoutFreezeBlobs/`
(193,972 B total; largest scratch file 83,906 B, `inv3.json`). Largest file I produced: `artifact-manifest.tsv`, 166,697 B.
No clone was needed; nothing in the lane was mutated (no git/jj write, no `git add`, no commit).

## A. Freeze tree census (commit `3e6c848a`)

| measure | value |
|---|---|
| files at HEAD under `.ufo/waves/round-48` | **770** |
| bytes at HEAD | **10,865,694** |
| worktree files (same tree) | 781 at 22:23, growing with live w2 evidence |
| worktree-vs-HEAD drift (tracked paths) | **0** — deletion, size and content all equal, 770/770 |
| files at HEAD absent from worktree | 0 |
| worktree-only paths | 11 at 22:23: 8 `.pyc` under two gitignored `__pycache__/` dirs, `w2.ready`, `w2.ready.dispatched`, one w2 seat script |
| **any file > 1 MiB** | **none** — `find -size +1024k` empty; largest 257,131 B ×4 (`w1/ExecXkbSource/fetch/xkeyboard-config/xkeyboard-config-2.48/rules/base.xml`, `fetch/host/rules-base.xml`, `fetch/host/rules-evdev.xml`, `w1/ScoutXkbSpecs/fetch/X_base.xml`) |
| files > 64 KiB | 38 (all present at HEAD, all evidence: pins, fixture sets, receipts) |

`artifact-manifest.tsv` (835 rows, sha256 `18608b81727f8b335c189c8f5194d5dab3d85a11ae747203b09b7fee445c4adb`) carries
`group, path, bytes, sha256, committed_at_freeze, required_by` for every artifact this wave can need.

## B. Registration "freeze contains" checklist — all 11 groups satisfied

`registration.md`'s closing paragraph names 11 groups; the table below splits the fixture-set and pin/receipt groups into
their individual files (16 rows) so each path, byte count and digest is explicit. No row is missing.

| # | required by `registration.md` | exact path | bytes | sha256 |
|---|---|---|---|---|
| 1 | claims | `.ufo/waves/round-48/claims.md` | 3,289 | `cc01009bb4bf1c2e36920811bdfac3e496bcdbfcccea29f194dc0adf949591f8` |
| 2 | registration | `.ufo/waves/round-48/registration.md` | 8,551 | `a3ac7e70a9e393c368bc327237c4dd3b6746cfaf235ef5667482bdb6f2fe6162` |
| 3 | counter C1 | `quality/counters/c1-r48-terminal-cache.py` | 52,654 | `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4` |
| 4 | counter C2 | `quality/counters/c2-r48-xkb-entry.py` | 42,256 | `4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1` |
| 5 | cold fixture set (190) | `quality/counters/c1-r47-fixtures.json` | 163,648 | `4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86` (== `SHA256_COLD`) |
| 6 | warm fixture set (204) | `quality/counters/c1-r48-fixtures.json` | 241,156 | `4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa` (== `SHA256_WARM`, == `l1-draft/c1-r48-fixtures.json`) |
| 7 | fixture generators | `l1-draft/merge-fixtures.py` 2,135 · `l1-draft/add-fixtures.py` 4,321 · `l1-draft/build-fixtures.sh` 492 · inputs `w1/ExecCounterC1/c1-r48-fixtures.json` 28,012 `23932fd3…` · `w1/ExecFixturesV2/fixtures-v2.json` 201,284 `faf5141d…` | — | all present at HEAD |
| 8 | C1 pin | `.ufo/waves/round-47/fetch/xdg-terminal-exec` | 44,020 | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (== `PIN_SHA256`, == `/usr/bin/xdg-terminal-exec`) |
| 9 | round-48 XKB pins | `.ufo/waves/round-48/fetch/` (14 files) | 337,128 (with the C1 pin) | every pin cited by a row exists at HEAD, mode 100644, digest == the row's `sha256:` |
| 10 | live receipt + generator | `receipts/xkbcli-compile-keymap-r48.txt` 14,270 `ab5fa971…` · `fetch/xkbcli-compile-keymap-r48.txt` 14,270 `ab5fa971…` (byte copy) · `tools/make-xkb-receipt.sh` 8,168 `42a50468…` | — | receipt == fetch copy (`cmp`) |
| 11 | w1 results/reports + control receipts | `w1-results.json` 200,732 `5a133795…`; 41/41 seats have a dir **and** a report, no empty dir; 699 w1 files at HEAD (706 walked: +7 gitignored `.pyc`) | — | 41 == `w1-spec.json` item count |
| 12 | C1 reference draft + control outputs | `w1/ExecControlsC1/controls/reference.py` 58,671 `f4942e24…`; `w1/ExecControlsC1/receipts/reference.txt` 13,903 `ce66f112…` ends `cold=190/190 warm=32/32 explained=222/222 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET`; `receipts/artifact-hashes.txt` 3,135 `ca8631d8…` = 34-entry manifest, `sha256sum -c` rc 0 | — | — |
| 13 | C2 control outputs | `w1/ExecCounterC2/receipts/` (controls.txt 15,980 `11a3be3d…`, control-patches.txt 20,594, pos-entry.md, pos-pins.txt, pos-receipt.txt, pos-rows.md, pos-rename.txt, digests.txt, base-census.txt, lane-before.txt, host-xkb-probe.txt) + `controls/{build_controls.py,run_controls.py}` | — | — |
| 14 | census-before | `receipts/census-before.txt` | 2,347 | `60a3fbbdcd4e641f347e154349506e87d2f55a9c023a0116a5744714039054bc` |
| 15 | C1 base receipts | `l1-c1-base-final.txt` 2,487, `l1-c1-base-prefreeze.txt` 1,317, `l1-c1-base-rfix.txt` 77,192 (all show warm-clause failures at BASE) | — | — |
| 16 | C2 base / positive control | `l1-c2-before-base.txt` 153 `PRED-C2-r48: admitted=0/1 verdict=TARGET_MISSED rev=579f694b…` + the pos-* set in (13) | — | — |

Supplementary identity proofs:

- `tools/mado-terminal.py` (worktree, pending) == `l1-draft/mado-terminal.py` — 67,963 B `1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92`.
- `corpus/knowledge/xkb-keymap-compile-r48.md` (untracked, pending) == `l1-draft/xkb-keymap-compile-r48.md` — 19,916 B `885a2e4187eeba2919c894e53b11d9a5975f2470e904572d58285e364806ec5a`.
- `quality/check-session-material.py` == `w1/ExecSessionMarker/check-session-material.py` — 66,395 B `82c9053ae2e8b7db…`; `quality/session-material-waivers.txt` == `w1/ExecSessionMarker/session-material-waivers.txt` — 8,449 B `4d007fe8124523a1…`.

## C. Digest binding, re-derived independently of the counters

- C1: 3 literals in the counter, 3 file matches (`SHA256_COLD`, `SHA256_WARM`, `PIN_SHA256` above). Fixture counts read from
  the files themselves: **cold 190 items, ids unique; warm 204 items, ids unique** — exactly the frozen predicate's numbers.
  The 150 + 80 nonce cases are *generated* (`GEN = 150`, `GEN_W = 80`, `c1-r48-terminal-cache.py:129-130`), so no nonce
  fixture file is expected in the freeze; none exists (consistent, not a gap).
- C2: 11 head rows (S340–S350) in `l1-draft/rows-c2.md`, **13 pin references, 13 exist at HEAD, 13 digests match** the row's
  recorded `sha256:` (S346 names three pins). S350's receipt digest `ab5fa971…` equals both committed copies.
- Held rows: S318/S319 are present once each in `corpus/SOURCES.md`, byte-equal HEAD vs worktree, and their round-46 pins
  re-hash to the row digests (`a76f0507…` 59,222 B; `8a800efe…` 15,941 B). All 8 round-46 pins cited anywhere in
  `SOURCES.md` exist.

## D. Fixture-generator closure

`build-fixtures.sh` → `merge-fixtures.py c1-r48-fixtures.json` (reads `w1/ExecCounterC1/c1-r48-fixtures.json` +
`w1/ExecFixturesV2/fixtures-v2.json`, both at HEAD) → `add-fixtures.py <WORK>` (L1 measured cases) → rewrites
`SHA256_WARM`. Every input is inside the freeze commit; no generator step reads `/fast/scratch`, `/tmp` or a sibling lane.
The freeze can therefore regenerate the 204-case file from committed bytes alone, and the current file matches the pin.

## E. Data-commit pending set (60 paths, 949,517 B) — exact

13 lane paths + 47 installed sidecars. `git ls-files --others --exclude-standard` yields exactly 47 `*.synthetic` files and
every one maps 1:1 to a seat sidecar (zero strays, zero missing installs, zero content mismatches).

- Modified: `SKILL.md` 224,832 · `corpus/QUALITY.md` 98,757 · `corpus/README.md` 72,373 · `corpus/SOURCES.md` 251,414 ·
  `corpus/knowledge/hyprland-monitor-rule-r45.md` 19,716 · `corpus/knowledge/xdg-terminal-selection-r47.md` 27,170 ·
  `corpus/lessons/round-47.md` 34,281 · `quality/check-session-material.py` 66,395 · `tools/mado-terminal.py` 67,963.
- Untracked: `corpus/knowledge/xkb-keymap-compile-r48.md` 19,916 · `corpus/lessons/round-48.md` 36,259 ·
  `quality/check-round-outcome-first.py` 11,493 · `quality/session-material-waivers.txt` 8,449 · 47 sidecars (130–161 B each).
- Append discipline holds for every install: `corpus/SOURCES.md` +11 lines / **0 removed** / 1 hunk, all 11 `rows-c2.md`
  lines verbatim; `corpus/README.md` +2 lines / 0 removed / 2 hunks, the `readme-row.md` line verbatim;
  `corpus/knowledge/hyprland-monitor-rule-r45.md` +51/0 (45 lines from `w1/ExecErrataR45/block.md`);
  `corpus/knowledge/xdg-terminal-selection-r47.md` +27/0 (22 from `w1/ScrErrataD4/erratum.md`);
  `corpus/lessons/round-47.md` +109/0 (95 from `w1/ScrD1Line/lines.md`); `SKILL.md` +130/0 (98 from `w1/ScrSkill/section.md`);
  `corpus/QUALITY.md` +67/0 (block carried from `w1/ScrMistakes/mistakes.md`, whose line it cites,
  `.ufo/waves/round-48/w1/ScrMistakes/check96.py`, exists); `corpus/lessons/round-48.md` is the `ScrLesson/round-48.md`
  skeleton with every `<AFTER>` substituted (integration note in-file).
- Held-row no-harm: S318 and S319 are unchanged in the pending `SOURCES.md` (single occurrence each, byte-equal to HEAD).

## F. Missing receipts / artifacts — answer

**None of the artifacts the registration requires is missing, and no cited receipt is absent from the seat that cites it.**
The 572 path-shaped citations across the 41 w1 reports resolve as: 474 exact, 41 by basename inside `w1/`, 4 lane-root
docs, 10 cross-seat/fleet/upstream, 43 that needed a second pass — of which every one resolved to a real file
(`quality/counters/*`, `corpus/knowledge/*`, sibling-lane tools, upstream `lib/quotearg.c`-class path names inside pins) or
to a deliberately non-committed artifact:

- `w1/ExecSessionMarker/fixtures/{synthetic-clients,forged-real}.json` — planted only in that seat's throwaway clone
  (`ExecSessionMarker.md:88-112`, "same clone, one commit each"); the lane carries `sidecars/` (48) + markers + `install.sh`
  (1,301 B) + `SHA256SUMS` (16,990 B) and `receipts/13-seatdir-scan.txt` `SEATDIR_SCAN files=77 r5_tokens=0 r4_files=0`. Deliberate.
- `w1/ScrConsider/check96-base.txt`, `check96-green.txt` — declared superseded by `check96.txt` in `ScrConsider.md:65`.
- `w1/ExecRefCacheB` `a.txt` — a probe-created symlink target, not a receipt.
- `w1/ExecIdGuard` `MERGE-REPORT.md`, `shokuknow/merge/...` — files of the shokuknow repo, not this lane.
- `.ufo/reports/session-clients.json` — the live host path the marker gate must refuse; shape-only, never committed.

Empty-stream audit: 34 zero-byte files, all the silent side of an `{out,err,rc}` triple whose `.rc` sidecar carries
`CMD:`/`RC:` (e.g. `ScrRows/receipts/test-host.{out,err}` both empty with `test-host.rc` = `RC: 0` — `xkbcli compile-keymap
--test` prints nothing on success). **No zero-byte file is the sole evidence for its claim.** 4 uncited lone stubs exist
(`w1/CritClaimSizing/xkbcli-{m,m3,ml,o}.err`, 0 B, no companion, no citation) — dead weight, not a gap.

## G. Observations (severity ordered; none breaks a frozen predicate)

1. **[info] `census-after.txt` is byte-identical to `census-before.txt`** — both 2,347 B,
   `60a3fbbdcd4e641f347e154349506e87d2f55a9c023a0116a5744714039054bc`; `census-after.txt` mtime 22:23:24, i.e. created
   after the freeze commit, and it is the only untracked file in `receipts/`. The census only emits cross-scope duplicate-URL
   (`W04`) and tier-C lines plus one `ok` line for `SOURCES.md`, and the round-48 rows add distinct upstream paths, so an
   identical after-census is explainable — but it cannot certify the rows landed. What certifies that is the row delta
   measured in §E (11 rows at the worktree, 0 at HEAD) and the per-row digest binding in §C. Also: no script in the lane
   emits `W04`/`tierC` lines, so this receipt is not reproducible from the freeze itself.
2. **[info] The registration's instrument preamble overclaims for C2.** "fixture/pin SHA-256 values are in those scripts"
   is exact for C1 (3 literals) and not for C2 (0 literals; `c2-r48-xkb-entry.py:8-13` declares the trust model as
   row-digest ↔ committed-copy). Not a predicate hole: I verified the binding independently for all 13 pins. Worth the L1's
   eye only because the sentence invites a reader to expect a digest map that is not there.
3. **[info] The C1 reference receipt set has no index.** Six `l1-c1-ref-*` receipts are committed; five report
   `verdict=TARGET_MET` and `l1-c1-ref-final3.txt` (573 B, 21:57:32) reports `readonly=fail … verdict=TARGET_MISSED`.
   By mtime the authoritative one is `l1-c1-ref-rfix.txt` (28,604 B, 22:14:44, MET), with the two BASE receipts at 21:21/21:32
   and `l1-c1-base-rfix.txt` at 22:18. The freeze carries the MISSED variant without a note naming it superseded.
4. **[info] The 48th sidecar is deliberately not installed.** `w1/ExecSessionMarker/` holds 48 sidecars; `install.sh`
   writes 47 plus the two registry files. The uninstalled one is the seat-root `check-session-material.py.synthetic`
   (`kind=gate-copy`, `sha256=82c9053a…` = the installed v2 gate bytes), matching `ExecSessionMarker.md` §3.5
   ("the 48th sidecar has no target, so it changes no finding"). At the data tip `quality/check-session-material.py.synthetic`
   will therefore not exist. Recorded so it is not later read as a missing receipt.
5. **[info] Four dead stubs** in the freeze: `w1/CritClaimSizing/xkbcli-{m,m3,ml,o}.err`, 0 B each, no companion capture,
   no citation in that seat's report or findings.
6. **[method] Relative paths are unreliable in this harness.** In one shell `cd /home/vgpnk/Projects/shokunin/mado-shokunin;
   sha256sum quality/counters/…` resolved while `sha256sum l1-draft/…` in the same shell reported "No such file" (absolute
   `ls -la …/round-48/l1-draft/` from a sibling shell succeeded, 20 files, unchanged sizes/mtimes/inodes). Every inventory
   number above was then taken with absolute paths and `git -C`. A later reader hitting that transient should not read it as
   a missing freeze file.
7. **[info] Two seat trees carry gitignored Python caches** — `l1-draft/__pycache__/lsemu.cpython-314.pyc` (10,852 B) and
   seven `w1/ExecXkbSource/fetch/xkeyboard-config/…/rules/generator/__pycache__/*.pyc`. `.gitignore:3` covers them, no `.pyc`
   is in the freeze commit (verified against the HEAD tree). Correct as committed.

## H. Risks the L1 should weigh before the data commit

- `corpus/SOURCES.md` (251,414 B) is the largest pending file and the only one whose append is shared with held rows
  S318/S319; the append is already correct in the worktree (0 removed lines), so stage it as-is — a hand re-edit is the only
  way to break clause (h).
- The 47 sidecars are the R3 write set and are untracked; a selective `git add` of the 13 lane paths alone would leave the
  waivers registry pointing at unmarked paths and flip the gate's finding count at the data tip. Either stage all 60 or
  re-run `install.sh` from the seat copy (byte-equal, verified).
- `tools/mado-terminal.py` and the entry already sit in the worktree at their frozen draft bytes; the data commit is a pure
  staging step and needs no re-copy (re-copying from a stale draft would be the only way to introduce drift).
- No file in either set is above 1 MiB, so `ulimit -f`/helper size ceilings are not a hazard for this round.

## I. Evidence left behind

| artifact | bytes | sha256 |
|---|---|---|
| `w2/ScoutFreezeBlobs/artifact-manifest.tsv` | 166,697 | `18608b81727f8b335c189c8f5194d5dab3d85a11ae747203b09b7fee445c4adb` |
| `w2/ScoutFreezeBlobs/artifact-summary.json` | 1,474 | `386ddc59875c4b38391c6c37e3b97cc2793836d77266900be804ceed37d5aed7` |
| `w2/ScoutFreezeBlobs.md` (this report) | — | — |

Scratch `/fast/scratch/hyaku/mado-r48/ScoutFreezeBlobs/` (193,972 B; scripts `inventory{,2,3,4,5}.py`, `final-manifest.py`,
outputs `inv{,2,3,4,5}.json`) is removed on exit; both seat artifacts are already in the lane. No tool was installed and no
package transaction was run. No lane Git/jj mutation, no commit, no push.

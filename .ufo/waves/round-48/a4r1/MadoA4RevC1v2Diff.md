# a4r1 / MadoA4RevC1v2Diff — C1 v2 instrument vs its registration

Seat target: `quality/counters/c1-r48-terminal-cache-v2.py` + `c1-r48-fixtures-v2.json` against
`.ufo/waves/round-48/registration-v2.md` §C1. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`; all checks pinned
at scorecard commit `d8e3d6003bf3b5de98e8eb116e1b6d416b2ef883` (data commit `e5d0130d` is its ancestor; base
`579f694b` ancestor — both `merge-base --is-ancestor` ok). Evidence: `a4r1/MadoA4RevC1v2Diff/`
(`diff-v1-vs-v2-counter.diff`, `run-v2-d8e3d600-nonce4848.txt`, `integrity.txt`).

**No release blocker found. No predicate-breaking defect in the committed C1 v2 data or in the L1's claims about it.**

## Findings by severity

### Blocker
None.

### Major
None. (Instrument-vs-registration correspondence and the published target line both verified end to end; see tables.)

### Low
1. **Hunk with no registering sentence — work-dir prefix (cosmetic).** v1 `tempfile.mkdtemp(dir=a.work, prefix="c1r48-")`
   → v2 `prefix="c1r48v2-"` (v2 line 1074). No sentence of registration-v2.md §C1 names it. Harmless (dir naming only;
   `--work` rules unchanged), but it makes the "v1 byte for byte except:" list strictly incomplete. Registered fix is
   registration prose; nothing to re-run.
2. **Hunk with no registering sentence — symlink mtime pinning (behavioral, load-bearing for the new fixtures).**
   `pin_tree` now calls `os.utime(..., follow_symlinks=not os.path.islink(p))` for files and dirs (v2 lines 467-470),
   so a `links` symlink gets its own times and never its target's (a dangling target would make `utime` raise). The
   only registration text is the counter's own docstring ("a symlink's own times are pinned in step 2, never its
   target's"); §C1 says only "schema v2 gains `links`". It is *implied* by the Fixtures bullet (L1-22..28 pin
   `mtime` over symlinked trees and must hash stable), and the rerun proves it works — but no sentence registers the
   counter change itself.
3. **Counter-docstring-only details inside registered hunks.** Two mechanics named in the counter's clause-r docstring
   are absent from §C1's sentences: (a) "quoted path strings are blanked before the flags are read"
   (`QUOTED.sub('""', rest)` before the O_* flag test, v2 lines 387-391) — this is what stops a flag-looking string
   *inside* a quoted path from faking a write trip; (b) the new residual sentences "directory mtimes never enter the
   hash … so pinning them is inert", "clause r sees attempts through the syscalls TRACE_SET names", "writes through an
   fd inherited from outside the sandbox … are not traced" (v2 residual paragraph) — §C1's residual sentence lists
   only the out-of-contract *classes* (six-month second, ACL/xattr, newline names, six ls variables, FIFOs, symlink
   loops), which do match the docstring's class list exactly. Declaration-only; no behavior disagrees with the
   registration.
4. **Minor unregistered detail:** applying a `.rw/` mode to a path the primed tree lacks raises `Setup` (v2 lines
   560-563). §C1's ".rw/ mode only to a tree with a cache, after the cache edits" covers the ordering; the
   missing-path refusal is unnamed. Setup errors are exit 2, not a scoring verdict, so no verdict path is affected.

## Hunk → registered sentence table

Diff saved at `a4r1/MadoA4RevC1v2Diff/diff-v1-vs-v2-counter.diff` (330 lines; v1=1021 lines, v2=1085). "Reg" =
registration-v2.md §C1 (lines 44-63; Fixtures bullet 50-56). R = registered, P = partially registered,
U = unregistered.

| v2 hunk (diff @@) | change | registering sentence | verdict |
|---|---|---|---|
| -1,7 +1,10 | docstring: v2 name, registration-v2 pointer, B1/B2 rationale | "Counter … v1 byte for byte except" + "PRED, final line and clause labels read PRED-C1-r48-v2" + preamble/Why rows B1, B2 | R |
| -28,7 +31,8 | materialize step 1 materializes `links` between files and exec stubs | "schema v2 gains `links` {path: target}" | R (own-times clause is docstring-only → Low 2) |
| -40,7 +44,8 | `after` gains `links`; `.rw/` mode note | "(top level and in `after`) and applies a `.rw/` mode only to a tree with a cache, after the cache edits" | R |
| -60,7 +65,8 | clause x docstring: cmd newline written `\n` | "compares `cmd=` with each newline in the word written as the two characters `\n`" | R |
| -69,7 +75,8 | clause x docstring: 4th capture | "adds a fourth `--observed` capture … `/r48-foreign-root` … DIFFER/1" | R |
| -82,8 +89,8 | bwrap docstring: `.rw` read-only wording, ATTEMPT | clause r sentence | R (prose only) |
| -93,12 +100,18 | clause r docstring: TRACE_SET, write kinds, split execve, quoted blanking | clause r sentences + split-execve sentence | P (quoted-blanking docstring-only → Low 3a) |
| -106,8 +119,16 | residual paragraph expanded | "Out-of-contract classes are declared in the counter's residual paragraph (…)" — class list matches exactly | P (visibility sentences docstring-only → Low 3b) |
| -122,7 +143,7 | `PRED = "PRED-C1-r48-v2"` | labels sentence | R |
| -131,14 +152,20 | `NAME_WARM`/`SHA256_WARM` re-pin; PROC/OPEN/WRITE sets, `TRACE_SET`, `WRITE_FLAGS`, `QUOTED` | Fixtures bullet (name + sha "pinned in the counter") + clause r sentence (incl. "traces `fork vfork clone clone3`") | R |
| -228,8 +255,8 | unknown-`after`-key set gains `links` | "(top level and in `after`)" | R |
| -298,8 +325,8 | `run(..., writes_ok=False)` | "in every tool run except the clause-s selftest" | R |
| -313,7 +340,7 | `check_trace(trace, writes_ok)` call | same | R |
| -328,7 +355,7 | `check_trace(self, path, writes_ok=False)` | same | R |
| -336,7 +363,9 | trip regex from PROC_SET; `wtrip`/`otrip` | clause r write-attempt enumeration (open flags; creat…mknod(at)) | R |
| -345,8 +374,9 | `<...` skip moved after execve detection | "the python3 execve is recognised when strace splits it (`<... execve resumed>`; v1 skipped resumed lines first …)" | R |
| -354,8 +384,13 | resumed-execve `seen` logic; write-trip classification with quoted blanking | same two sentences | P (blanking → Low 3a) |
| -395,6 +430,16 | `add_links()` | "gains `links` {path: target}" | R |
| -402,6 +447,7 | `materialize` calls `add_links` | "(top level …)" | R |
| -418,10 +464,11 | `pin_tree` utime `follow_symlinks` per symlink | none (docstring-only) | **U → Low 2** |
| -474,12 +521,18 | `apply_after`: `add_links`; `.rw/` modes deferred to `rw_modes` | "in `after` … `.rw/` mode only to a tree with a cache, after the cache edits" | R |
| -504,6 +557,12 | `rw_modes` applied post-cache-edits; Setup on missing path | same sentence | R (Setup detail → Low 4) |
| -652,7 +711,8 | explain `cmd_word` newline escape | clause x cmd sentence | R |
| -709,6 +769,10 | 4th capture `caps += ((3, … foreign-root … DIFFER, 1),)` | clause x capture sentence | R |
| -897,7 +961,7 | selftest run `writes_ok=True` | "except the clause-s selftest (which builds its own trees under the sandbox /tmp)" | R |
| -1007,7 +1071,7 | work prefix `c1r48v2-` | none | **U → Low 1** |

Net: 21/26 hunks fully registered, 3 partially (docstring-only mechanics), 2 unregistered (one cosmetic, one
behavioral-but-implied). No hunk contradicts any registration sentence.

## Fixture verification

- sha256(`c1-r48-fixtures-v2.json`) = `3ab1f5d0e7e382ea1949195689177aa135af83d07eddaccf449ece24aa8e51ef` — equals the
  task value, the registration's Fixtures bullet, the counter's `SHA256_WARM` pin, and the blob at `d8e3d600`. ✓
- v1 fixtures: 204/204 present, JSON-equal per id to `c1-r48-fixtures.json` (whose own sha equals the v1 counter's
  pin `4d946bd7…`, so "unchanged" is anchored to v1-frozen bytes); 0 changed, 0 removed. ✓
- New ids: exactly 24 (`L1-11…L1-34`), no dups, no extras. ✓ Class match vs registration-v2.md:50-56 (evidence:
  fixture fields + clause-w lines of my rerun + `receipts/l1-v2-add-fixtures.txt`, all three agree):

| id | registration class (line 50-56) | fixture evidence | rerun clause=w | verdict |
|---|---|---|---|---|
| L1-11..15 | live cached path, `--print-content` (B2, WARM-DIFFERS) | `after.files` same-size list edit alpha→bravo; cached alpha entry stays live; args carry `--print-content` | WARM-DIFFERS state=hit pass | ✓ |
| L1-16 | " (cache-line variant) | `after.cache_lines` repoints cached path to another live entry | WARM-DIFFERS state=hit pass | ✓ |
| L1-17 | non-executable Exec[0], warm (G1) | `after.modes bin/foot=420`; cached cmd = foot | WARM-SAME state=stale pass | ✓ |
| L1-18 | " , cold | cold `EXEC-MODE`, mode 420 on Exec[0] | EXEC-MODE state=absent pass | ✓ |
| L1-19/20 | multi-line cached command (F1) | `Exec=foot "a\nb"`, prime caches two-line cmd | WARM-SAME state=hit pass ×2 | ✓ |
| L1-21 | mode-000 cache (F2, `invalid`) | `after.modes .rw/cache/xdg-terminal-exec=0` | MALFORMED state=invalid pass | ✓ |
| L1-22 | symlink: operand dir | `links {applications/ → store/apps}` | WARM-SAME state=stale pass | ✓ |
| L1-23 | " entry file | `links {…/foot.desktop → store/foot.desktop}` | WARM-SAME state=stale pass | ✓ |
| L1-24 | " dangling entry | `links {ghost.desktop → nowhere.desktop}` | WARM-SAME state=hit pass | ✓ |
| L1-25 | " dangling revived | dangling link + `after.files` creates target | WARM-SAME state=stale pass | ✓ |
| L1-26 | " chain | two links `foot.desktop→l1→real.desktop` | WARM-SAME state=stale pass | ✓ |
| L1-27 | " sibling twins | two links to one target; `--print-id` picks b | WARM-SAME state=stale pass | ✓ |
| L1-28 | " data home | `links {home/.local/share → sharestore}` | WARM-SAME state=stale pass | ✓ |
| L1-29/30 | default-location cache hit / same-size edit (C1-A) | `default_cache: true`; L1-30 edits foot→feot (same length) | WARM-SAME hit / WARM-DIFFERS hit, pass | ✓ |
| L1-31 | `XTE_CACHE_ENABLED=''` (C1-B, `disabled`) | `after.env {XTE_CACHE_ENABLED: ""}` | MALFORMED state=disabled pass | ✓ |
| L1-32 | directory at the cache path (C1-C, `absent`) | `after.files {".rw/cache/xdg-terminal-exec/": ""}` | MALFORMED state=absent pass | ✓ |
| L1-33 | empty cached command word | `cache_lines 11 = foot␟␟--a…` | WARM-DIFFERS state=hit pass | ✓ |
| L1-34 | newline inside first cached command word | `cache_lines 11 = fo\not␟--a…` | WARM-DIFFERS state=hit pass | ✓ |

## Published-line re-verification

`ulimit -f 2048; cd $S && TMPDIR=$S python3 -I <lane>/quality/counters/c1-r48-terminal-cache-v2.py --repo $S/clone
--rev d8e3d600… --work $S/work --nonce 4848` on a `git clone -q --shared --no-checkout` of the lane (plain `--shared`
clone cannot check out pre-1MiB round-20/21/22 `.ufo` evidence under the 1 MiB file cap; the counter reads blobs via
`git show` and the round-47 pin via `lane_root()`, so `--no-checkout` is equivalent for it). Result in 3m02s, exit 0:

```
PRED-C1-r48-v2: cold=190/190 warm=228/228 explained=418/418 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

Byte-equal to the published target (SCORECARD.md:2707 at `d8e3d600`, nonce 4848 as published); clause=a tool=present,
clause=s 70/70, clause=f 190/190, clause=w 228/228, clause=x 418/418, clause=g 230/230, clause=r trips=0. Full log:
`a4r1/MadoA4RevC1v2Diff/run-v2-d8e3d600-nonce4848.txt`. The counter file is tracked-clean and identical to its
committed blob (`5bb9aead…`) and to `l1-draft/v2/` — the "Counter (= l1-draft/v2/)" registration sentence holds.

## Residual risk and verification gaps

- **No LSP server answered** for this seat (no `lsp` device in the seat's tool inventory): hunk/registration mapping
  is from `diff -u` text plus targeted reads, and caller analysis (e.g. `check_trace` call sites) is from the diff and
  reads, not semantic references. The full independent rerun is the compensating semantic check.
- **Nonce coverage:** one rerun at the published nonce 4848. Clause g draws 230 generated cases from that nonce;
  a different nonce explores a different draw, so the generated clause is verified at the published point only.
- **Base-tool side check not repeated:** `receipts/v2/ctl/BASE.txt` (base tool → TARGET_MISSED) was not re-executed;
  SCORECARD and the control receipt agree with each other, and my scope was the instrument-vs-registration audit at
  the scored rev.
- **Tip movement:** lane HEAD advanced `d8e3d600` → `f029de3a` while this seat ran (post-dispatch integration;
  `c1-tip.txt` receipt dated 00:43 exists). My checks pin `d8e3d600` per assignment and hash tracked-clean
  working-tree files; if the predicate is to be judged at the *final* tip per the kill rule, that run is L1's
  (`c1-tip.txt`), not re-verified here.
- Scratch: peak 144K (bound 2 GB), largest regular file 32 002 bytes (the run log, copied to the evidence dir);
  every writer shell ran `ulimit -f 2048`; scratch tree removed after evidence copy. No tool installed (none needed).

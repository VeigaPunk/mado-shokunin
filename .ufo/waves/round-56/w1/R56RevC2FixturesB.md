# R56RevC2FixturesB — audit of committed C2 fixtures F10-F18

Seat: R56RevC2FixturesB (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, freeze commit `3423ae285676c2a10273000f4519163472b443db`.
Deliverables: `.ufo/waves/round-56/w1/R56RevC2FixturesB/{interp.py,drive.py,receipts.txt}`.

## Result

- Committed expectations F10-F18 (`expected.out`, `expected.rc`) agree with `registration.md` §C2 for all nine fixtures. No fixture
  expectation is contradicted by the contract text. Hand-derivation and an independent interpreter agree byte for byte (9/9).
- Git symlink entries survive `git archive | tar -x` (3 links in the c2 tree, all read back with the committed target text).
- Five findings are about fixture **coverage or labels**, not wrong expectations: F12 note mislabels its intent; F10 and F13 do not
  discriminate the behaviour their notes claim; `errors=` and the canonical-watch `via=` are not defined by the text. Details below.

## What I did (commands, trimmed)

Contract read: `registration.md` (full, §C2 and the harness/legs at lines 10-20 and 146-162), and `claims-frozen.md` (read after
the fixtures, to check C2 consistency). Counts there agree with §C2 (5 divergences, 18+8 fixtures, 3 controls). I did not read
any hold-out path, any other seat's output, or `expected.out` before deriving the outputs of F10-F18 from the text.

Fixture inputs: `args.json`, `note.txt`, `expected.rc`, `tree/` (incl. `find -printf '%y %p %l'` for symlinks), read with `cat -A`.

Byte-level check (all nine): `tail -c1 expected.out` is `\n` and `expected.rc` is `0\n`/`2\n` for each.

Committed blobs vs working tree (read-only `git ls-tree`, `git hash-object --stdin` on each file or link text):
```
checked 53 mismatches 0
120000 blob 85177784…  .ufo/waves/round-56/fixtures/c2/F05/tree/linked.conf
120000 blob aa17c54c…  .ufo/waves/round-56/fixtures/c2/F06/tree/hyprland.conf
120000 blob 56919386…  .ufo/waves/round-56/fixtures/c2/F10/tree/mix/b.conf
```

Symlink survival (`git -C $LANE archive 3423ae… -- .ufo/waves/round-56/fixtures/c2 | tar -x -C <scratch>/export`, then `find -type l`):
```
F05/tree/linked.conf -> real/theme.conf
F06/tree/hyprland.conf -> real/main.conf
F10/tree/mix/b.conf -> missing-target.conf
```

Independent interpreter: `interp.py` written from registration §C2 only (glob rules, source handling, watch list, live join, setup
reasons). Driver `drive.py` substitutes `{FX}` in `args.json`, runs `python3 -I interp.py <args>` with cwd = export root, compares
stdout bytes and rc with `expected.out`/`expected.rc`:
```
F10 PASS rc=0 exp=0 … F16 PASS rc=0 exp=0
F17 PASS rc=2 exp=2
F18 PASS rc=2 exp=2
pass 9/9        (same on the export and on the working tree, read-only)
```
Python: 3.14.8 (`python3 -VV`). No installs were made.

## Hand derivations (from §C2 text; expectations agree)

- **F10** `source = nothing/*.conf` → glob empty → `ERROR nomatch` (line 1); `source = x` → len<2 → `ERROR bogus` (line 2);
  `source = mix/*.conf` → matches `a.conf`, `b.conf` (dangling symlink counts as a match, sorted); `a.conf` appended via `:3`,
  `b.conf` → `os.stat` fails → `ERROR inaccessible`, nothing after it; `source = after.conf` appended via `:4`. paths=3, errors=3, 3 primary watches.
- **F11** `misc { disable_autoreload = 1 }` → key `misc:disable_autoreload`, value 1 → autoreload=off, watch list empty; paths=1 (config
  always listed); getoption `int 0` → live=0, config=1 → DIFFER.
- **F12** getoption lines: an object (`misc:other`), then `[1,2]` (non-object) → `bad_json`, SETUP, rc 2.
- **F13** config empty → no misc key → autoreload on, disable_autoreload=unset; getoption: `int:true` ignored (bool), `int:1`, empty line
  skipped, `int:0` (later wins) → live=0, config=0 → AGREE.
- **F14** config absent → `lexists` false → one `type=missing` primary watch, paths=1, live=NONE.
- **F15** `source = a.conf` twice and `source=a.conf#c` (cut at `#`) → three duplicate `a.conf` entries via `:1`,`:2`,`:3`; paths=4 (main + 3), watches=4, no errors.
- **F16** `source = conf.d` → directory → `SKIP reason=directory path=$ROOT/tree/conf.d`; `source = conf.d/` → glob of a non-magic
  trailing-slash pattern yields `conf.d/` (Python glob returns it) → `SKIP … path=$ROOT/tree/conf.d/ reason=directory`; paths=1, errors=0 (SKIP is not an error).
- **F17** no `--config` → `usage`, SETUP, rc 2.
- **F18** getoption `{bad` → not JSON → `bad_json`, SETUP, rc 2.

## Findings

1. **F12 note contradicts its expectation (label, not expectation).** `note.txt`: `UNKNOWN: no record; non-object lines are bad_json`.
   `expected.out` is `MADO_WATCH: SETUP bad_json`, rc 2. The expectation is what §C2 requires (`[1,2]` is a non-object line).
   The fixture therefore never reaches UNKNOWN. Minimal input that does (`go.json` = `{"option": "misc:other", "int": 1}` only):
   ```
   MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=? verdict=UNKNOWN
   MADO_WATCH: DONE watches=1 unsupported=0 errors=0 live=UNKNOWN
   ```
   No F10-F18 fixture pins `verdict=UNKNOWN`.

2. **F10 does not discriminate the "dangling symlink aborts the glob loop" rule.** `note.txt`: `nomatch, bogus, dangling symlink
   aborts the glob loop`. The dangling `b.conf` is the last sorted match, so `break` and `continue` give identical output (verified:
   `cmp` identical). Minimal input: F10 tree plus an empty `mix/c.conf`. With `break`: `paths=3`, `c.conf` not listed.
   With `continue` (mutant): `paths=4`. The text (§C2 step 5, "the REST of this line's matches are skipped") is not pinned by any fixture here.

3. **F13 does not discriminate "bool int ignored".** `note.txt`: `bool int ignored, later line wins`. The bool line is followed
   by `int:1` and `int:0`, which overwrite it, so a mutant that accepts bool as int gives the same output (verified: `cmp` identical).
   Minimal input: `go.json` = `{"option": "misc:disable_autoreload", "int": true}` alone. Contract: no record → `live=?`, UNKNOWN.
   Bool-accepting mutant: `live=True verdict=DIFFER` (the mutant prints the Python bool; it is wrong either way). The bool clause
   has no fixture that would catch a mutant that accepts it.

4. **Ambiguity: `errors=<E>` is not defined.** §C2 uses `errors=<E>` in the header and DONE line but never says which events count.
   F16 pins that two `SKIP` events give `errors=0`, which matches the literal reading "ERROR events". The text should say so.

5. **Ambiguity: `via=` of the canonical watch is not defined.** §C2 gives role, path, type and mask for the second (canonical) watch
   but not its `via`. No F10-F18 fixture has a symlink on the watch list (F10's `b.conf` is not listed), so this is not exercised here.
   F05 and F06 have symlinks and are outside this seat's scope; not audited.

6. **Ambiguity: trailing newline on SETUP lines.** §C2 says stdout is "exactly `MADO_WATCH: SETUP <reason>`". The committed
   F12/F17/F18 expectations end in `\n`, consistent with every other line; the contract does not say whether the newline is part of "exactly".
   Not a defect; recorded because the word "exactly" is ambiguous.

7. **Environment dependence (not verified).** F16's `conf.d/` expectation relies on Python `glob` returning a non-magic
   trailing-slash pattern; I verified this only on Python 3.14.8. The harness's Python version is not stated in §C2.

## Could not verify / not run

- I did not run `tools/mado-watchplan.py` or `ctl/` or the harness `quality/check-r56-controls.py --claim c2`; the seat scope is the
  fixture expectations only. The interpreter is my own, and it passes 9/9 against the committed expectations, so it is evidence that
  the expectations are consistent with the text, not a test of the tool.
- Hold-out fixtures H01-H08: not looked for and not used.
- The seat's own interpreter is in the deliverable directory; the scratch area `/fast/scratch/hyaku/mado-r56/R56RevC2FixturesB/` was removed before yielding.

## Host and lane

- Read-only: lane files via the filesystem and `git cat-file`, `ls-tree`, `archive`, `hash-object --stdin` (no `-w`). No lane or fleet
  writes, no commit or index changes, no `hyprctl` calls, nothing under `~/.config` or `~/.local`.
- Deliverables written only under `.ufo/waves/round-56/w1/` (this report plus `R56RevC2FixturesB/`).

# R96MReviewC1 - C1 attack report (round 96, w1)

Seat: R96MReviewC1 (review only; I edited no lane file but this report).
Date: 2026-11-07, measured 11:30-12:14. Scratch: /fast/scratch/hyaku/mado-r96/R96MReviewC1
(deleted before yield). Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.

Artifacts measured (sha256, mtime at measurement):

| artifact | sha256 | note |
|---|---|---|
| build/mado-mimetext.c1.py | d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd | 12:10, static-clean, green |
| controls/magictext-cases-r96.json | 42ce9fc68458955e9e93c405cdbeb59f649b36d94e100240894d660391d1bed6 | 265 cases / 404 inputs |
| controls/magictext-fresh-r96.py | 32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da | 12:07 |
| controls/magictext-mutants-r96.json | c9eb0600fe5584c242adf59a2118a186179ba7c6ec9da904a7dd7362f00f31ee | PLACEHOLDER (F1) |
| quality-counters-c1-r96-magictext.py | aa77b40c6d34c7099d4697c721e255a09d974403072cf137848e22d96a922acd | 12:14; fixes landed at 5ce5ef84 |
| controls/host-text-db-r96.json | 9c411d2af41ac283fb7d229152f0b7b28b7854eabd057135a225762389d1ddd7 | manifest |
| controls/forgery-ctypes-r96.py | 06800cd141a18548c63701a44f9cab70e2c90f0f316fb6f24d0c06fca079fd97 | frozen library forgery |
| oracle source | 99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a | r95, reused |
| compiled oracle (host cc -O0) | 186537938e186727072bf911a86117918d505593e77617e53cfa246d425a3aa5 | glib2 2.90.1-1 |
| host list | 9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87 | r95, 4911 paths |
| mimeglob pin | 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 | round-94 bytes |

The wave is live: the tool, cases, fresh generator and counter all changed while I reviewed.
Every finding below states the sha it was measured at; a later edit invalidates that evidence
and needs a re-run.

## Axes and method

Axes: coverage (frozen/fresh/host exactness) and operability (controls, structural conjunct,
audit, pins). I compiled the pinned oracle in my scratch and re-derived the answers myself:
102 hand fixtures covering all 16 classes, 900 differential random cases (two seeds), 400 host
paths x 2 pairs (data-only and own-path-as-name), a full re-label of the 265-case frozen set
against a fresh oracle, and end-to-end runs of the counter with real and stub inputs. I also
tried a memoriser, a subprocess-wrapper forgery and the frozen ctypes library forgery.

The independent re-derivations (commands and summaries):

```
$ cc -O0 -o $S/oracle .ufo/waves/round-95/controls/mimesniff-oracle-r95.c $(pkg-config --cflags --libs gio-2.0)
$ python3 attack.py --tool $S/tools/mado-mimetext.py          # 102 fixtures
SUMMARY fixtures=102 mismatches=0
$ python3 fuzz.py 600 1 ; python3 fuzz.py 300 3               # 900 cases
FUZZ cases=600 mismatches=0 seed=1 ; FUZZ cases=300 mismatches=0 seed=3
$ python3 hostcheck.py 400                                    # 400 paths, 800 pairs
HOSTCHECK paths=400 pairs=800 correct=800
$ python3 casecheck.py .ufo/waves/round-96/controls/magictext-cases-r96.json
CASES 265 inputs=404 ; ENVELOPE_ERRORS 0 ; LABEL_VS_ORACLE_MISMATCHES 0 ; TOOL_VS_LABEL_MISMATCHES 0
```

## Findings by severity

### F1 - BLOCKER (claim-failure): the frozen mutant file is a placeholder; class_kills 0/16

`controls/magictext-mutants-r96.json` (sha c9eb0600) holds 115 mutants whose every `find` and
`replace` is the literal `<awaiting-candidate>`:

```
$ grep -c awaiting-candidate controls/magictext-mutants-r96.json
230
$ python3 -c "import json;d=json.load(open('.../magictext-mutants-r96.json'));print(len(d['mutants']), d['mutants'][0]['find'])"
115 <awaiting-candidate>
```

The counter anchors every mutant with `if src.count(m["find"]) != 1: return setup(...)`; a
`find` that occurs zero times is a SETUP_ERROR, so no mutant leg can run. My end-to-end run
with the otherwise-final inputs and an empty mutant set prints `mutants=0 killed=0
class_kills=0/16`; PRED-C1-r96-v1 (iv) (`killed == mutants`, `class_kills == 16/16`) cannot be
met until the mutation seat replaces every anchor against the frozen tool bytes (d5f174fc) and
the class kills are measured. The case side is ready: all 16 classes have at least 14 cases
(header 17, sect 20, value 20, mask 16, word 19, range 16, indent 17, order 16, drop 17,
multi 16, glob 16, alias 14, fallback 14, zerosize 14, mode 17, desktop 16) and the tool
answers all 265 (F-green below).

### F2 - BLOCKER at measurement (predicate/control): the memoriser control scores 1/40 on fresh, not 0

End-to-end run of the current counter with the current frozen set and the real fresh generator
(sha 32d38e, seed 7):

```
control memoriser frozen=156/265 fresh=1/40
... met requires memo_fresh == 0 ...
```

Cause: `memo_key(name, data)` hashes only name and data, not the case mode or environment. The
fresh generator emits the empty input (`name NULL, data b""`) and the frozen `zerosize` cases
hold the same key (`zerosize-01-empty-no-name`, `zerosize-05-empty-magic-ignored`), so the
label lookup returns the frozen label `application/x-zerosize 0` for a fresh input and one
fresh case is entirely correct. My key dump finds 8 colliding fresh inputs, all `None,b""`:
`fresh-mode-000/003`, `fresh-drop-023`, `fresh-mask-030/037`, `fresh-value-031`,
`fresh-glob-032/033`.

The declaration says "the memoriser 0 on fresh"; with a generator that legitimately emits the
empty file and a frozen set that legitimately tests zerosize, 0 is not achievable. Fix one of:
score the memoriser per input and require it to miss at least one fresh input; include the
case mode/env in the key; or have the generator avoid exact frozen inputs. This is a
claim-failure of the control as written, not of the tool.

### F3 - RESOLVED in the current counter/declaration (keep the current files)

At counter sha 1b84891a, `--scratch-root` was used at `main` but absent from argparse (every
non-check-only run: `AttributeError: 'Namespace' object has no attribute 'scratch_root'`), and
`case_mime_state`/`reachable_roots` never matched (roots were only appended when a NUL remained
after substituting `{root}`, so roots were always empty). Consequences I reproduced:

```
$ python3 -I .../quality-counters-c1-r96-magictext.py ... --cases magictext-cases-r96.json --check-only
MADO_MAGICTEXT_COUNT: SETUP_ERROR ... case mode-04-cache-refusal-valid-cache: UNSUPPORTED label without a reachable mime.cache
   (same for mode-05, mode-06, mode-11, mode-13)
```

The declaration command at that time also had a 37-char `--base-rev`
(`9f029f46f01f6cd3a1d29ac39bb498a1d0c3d`, `git rev-parse --verify --quiet` rc 1), a 63-char
oracle pin, a 12-char host-list pin (`9d5947a7ba87`, not even a prefix of the real
`9d5947a70d112796...`), and no `--expect-tool-sha256`.

The current counter (aa77b40c; the fixes landed at 5ce5ef84) and declaration (measured 12:14) fix all of this: `case_roots`
takes relative roots from the raw env, `loadable_cache` (>= 40 bytes, big-endian u16 major 1,
minor 1|2) decides cache mode, `--scratch-root`, `--expect-tool-sha256`, `--expect-mimeglob-sha256`,
`--host-db`, `--forgery` and their pins are required, and the declaration command carries them
with full 64-char pins. `--check-only` on the current case file prints
`CHECK_ONLY ok ... cases=265 ... classes=16` (rc 0). The L1 must freeze these bytes; the earlier
ones are not replayable.

### F4 - MEDIUM (predicate/control sentence): do-nothing is 0 only on text-mode cases; the 20 none-mode cases are answered by the r95 tool

```
control do_nothing text=0/240 none=20/20 cache_cases=5
```

The round-95 tool answers mode-none inputs (fallback/zerosize/trailing slash) exactly like the
text tool does, so 20 frozen none-mode cases (13 fallback, 4 zerosize, 3 mode) are fully correct
for the "do-nothing" instrument. The current counter restricts the control to text-mode cases
and prints the none census separately; `met` uses `dn_text_correct == 0`. The declaration's
predicate sentence says just "the do-nothing instrument ... 0" with no population. Fold "0 on
the text-mode cases; the none-mode census is printed separately" into PRED-C1-r96-v1, or the
predicate and the counter disagree. (This also explains the class-census tension: fallback and
zerosize are round-95 surface, and the frozen set keeps 20 none-mode cases for them.)

### F5 - MEDIUM (predicate limit): the host leg is not oracle-echoable, but it is table-passable

Echo/library/subprocess are stopped, with the exact refusal lines:

```
control forgery static=import:ctypes:8,...,spec_from_file_location-calls:0,no-module_from_spec-binding
                 audit_denials=5 rejected=True
AUDIT_DENY ctypes.dlopen 'libgio-2.0.so.0'
AUDIT_DENY subprocess.Popen 'file'
```

Anchors: empty PATH; the audit launcher (open allow = work + Python roots, spawn allowlist,
`ctypes.dlopen` libc-only, socket/network denied); the static import/name/dunder allowlist; the
pinned host-DB manifest, list and forgery; the live-oracle comparison. The current tool matches
800/800 sampled host pairs (400 paths, data-only and own-path) and 8/8 in the counter's short
run.

Limit: the host list (4911 paths) and the host DB (the eight /usr/share/mime text files) are
public and fixed, and the tool sees the file bytes and its own path; a precomputed
(path,data)->answer table would pass the host leg without a model. There is no held-out host
sample. The fresh leg no longer leaks labels (F6), but the host leg is the remaining
memorisable leg. Recommended: score a random, seed-printed subset of the host list that is not
in the committed file, or add a held-out set; alternatively record this as a named limit.

### F6 - RESOLVED (was a real hole): the fresh generator's labels were readable by the tool; the current counter isolates them

Against counter sha 1b84891a, a scratch draft that answered frozen cases from a one-entry table
and otherwise read the generator's labelled output (the generator wrote
`work/fresh-<seed>.json`, and the audit allow was the whole work tree) scored
`frozen=260/260 fresh=120/120` with no model. The counter's own memoriser control reported
`fresh=0/120`, so the control was blind to it.

The current counter writes the generator output, its scratch and the memoriser table under a
`secret` sibling outside the audit allow (`fresh_cases(..., secret, ...)`, `memo-model.json`
under `secret`), and the full run shows `memoriser_fresh=1/40` (F2), i.e. the file-reading path
is gone. Recommended regression: run a file-reading draft and require it to fail fresh.

### F7 - MEDIUM (contract text): "reachable mime.cache" vs a *loadable* cache

xdgmimecache.c:108-167 loads a cache only if it opens, is >= 40 bytes and has version major 1,
minor 1|2; anything else leaves the directory in text mode. The shared contract says "A
reachable mime.cache means cache mode" and "a case that holds a mime.cache is a cache-mode
refusal case". The first frozen case file followed that and labeled `mode-06` (a 16-byte
"JUNKNOTACACHE000") UNSUPPORTED, while the oracle answers text mode:

```
oracle 0 'app/x-md6\t0'      (data "MHDR data", d1 magic [50:app/x-md6] 0>0=MHDR)
oracle 1 'app/x-md6g\t0'     (name f.m6, d1 globs2 app/x-md6g:*.m6)
tool   0 'MADO_MIMETEXT: app/x-md6 uncertain=0 ...' ; tool 1 'app/x-md6g uncertain=0 ...'
```

The case seat fixed it (id `mode-06-junk-cache-is-not-a-cache`, labels the oracle answers) and
the current counter uses `loadable_cache`; amend the shared contract's cache sentence to
"loadable" so the trap cannot be re-introduced. This was the only case-label contradiction I
found (F-answer 1).

### F8 - LOW (model text): word size 0

The declaration/shared contract says "`~` + word size (1|2|4 only)". The C allows 0
(xdgmimemagic.c:440-443 rejects only values other than 0,1,2,4; the swap block runs only for
>1). A `~0` matchlet parses and matches: oracle `text/x-w0 0`; the tool follows the C and its
docstring says 0,1,2,4. Amend the model sentence.

### F9 - LOW (provenance): located quotes that do not resolve

Tool docstring (d5f174fc):

| citation | actual |
|---|---|
| `read_magic_file (:685-750)` | starts at 749; 685 is inside `_xdg_mime_magic_lookup_data` |
| "bad line dropped whole (:749-782)" | `state = _xdg_mime_magic_parse_error(...)` is at 784; the drop block is 781-785 |
| "section inserted ... (:735-747)" | insertion block is 772-780; 735-747 is the end of `matchlet_mirror` |

Spot-checks that resolve: gate :801-819 (fread 812, memcmp 814 - the sources receipt's "line
815" is off by one), header :230-281 (231), matchlet :301-514 (302), order :596-629 (597/618),
bounds :515-556 (525), tree :557-588 (571), fallback xdgmimeint.c:176-190 (177), subclass
xdgmime.c:820-891 (821), word-check :440-443 (440-444), swap :469-505 (471 onward).

Sources receipt S525 page lines (I re-fetched the two pinned URLs twice: 200, 18289 B
fcb1eafe..., 59208 B e00fa00e..., both identical to the receipt): the located quotes do not
resolve for 4 of 7 rows - 407-410 (actual 403), 429-433 (actual 421-423), 435-439 (actual
426-427), 441-446 (actual 429-432); 387, 389-391 and 393-399 resolve. C table rows: mask
400-419 (actual 420), word 421-450 (actual 476), parse-error 749-782 (actual 784), gate quote
815 (actual 814). The text is in the fetched bytes; the line numbers are not.

### F10 - LOW (CLI ergonomics): conflicting flags are accepted silently

`--data-home D --data-home-unset` together is accepted and the unset wins (mode none); no error.
The no-files error message ("name at least one FILE; --name and --names-from-files exclude")
is printed even when neither name flag was given. Neither is scored; recommend mutually
exclusive argparse groups and a distinct no-files message.

## Answers to the eight assigned attacks

1. Case labels contradicting the oracle: none in the current file. 404 inputs; all 399
   supported labels equal a fresh oracle run (0 mismatches, my re-derivation); the 5 sentinel
   labels are the loadable-cache refusal cases and the tool exits 3 for each (0 tool/label
   mismatches). The earlier `mode-06` junk-cache labels (2 inputs) were a contradiction and are
   fixed (F7).
2. Declared rules the tool answers differently: none on the probed surface. 102 fixtures (all
   16 classes) + 900 random differential cases + 800 host pairs + 265/265 frozen cases = 0
   mismatches. The only text divergences are the model sentences in F7/F8 (the tool follows
   the C); the only structural failure was the static `mp` collision, fixed in d5f174fc
   (static_check == []).
3. Memoriser/subprocess/library: both forgeries are refused (F5); the memoriser control now
   scores 1/40 on fresh, not 0 (F2), and the old fresh-file leak that let a memoriser pass
   fresh is closed (F6). With the current counter a pure memoriser/subprocess/library wrapper
   cannot pass the predicate as implemented, but the declared "0 on fresh" control does not
   hold as written.
4. Class census in code: yes. `CLASSES` is a 16-tuple in the counter; an unknown class is a
   SETUP_ERROR (`class 'bogus' not in the frozen 16`); fewer than 8 cases in a class is a
   SETUP_ERROR (`class header has 7 cases < 8`); the verdict prints `classes=16/16`. The
   current file: 265 cases, every class >= 14, ids prefixed by their class.
5. Host leg trivial pass: oracle-echo is blocked (audit/static; exact denial lines in F5). A
   precomputed table can still pass it because the list and DB are fixed and public; anchors
   and the residual limit are in F5. The tool's own answers on 800 sampled pairs are exact.
6. Pins cover the tool and its sibling: yes, in the current counter and command - the tool via
   `--expect-tool-sha256`, the sibling via `--expect-mimeglob-sha256` plus the embedded
   round-94 constant, and both are materialized from `git show <rev>:...`. The earlier draft
   command omitted the tool pin and `--scratch-root` and had three malformed pins; the L1
   fixed them (F3). Fill `<pending-w1>` with the frozen rev's measured shas at freeze.
7. A class killing nothing: today all 16 (the mutant file is a placeholder, F1; my run prints
   `class_kills=0/16`). The case census is sufficient for the counter to measure once the
   mutants are anchored; the mutation seat must land the real find/replace and the class
   measurement before the freeze.
8. Docstring citations: 6 spot-checks as F9 - errors and insertion do not resolve; gate,
   header, matchlet, order do. The sources receipt's S525 page-line column is the weakest
   (4/7 wrong) and its C table has three wrong ranges plus the gate line off by one.

## End-to-end counter evidence (current files, real generator, 4-path host list)

Command: the declaration's counting command with `--cases`/`--expect-cases-sha256` =
42ce9fc6..., `--mutants` = an empty set (the real file is a placeholder), `--expect-tool-sha256`
= d5f174fc..., `--host-list` = a 4-path scratch list, `--fresh 1 --fresh-seed 7
--draft-tool` the staged candidate. Output excerpt:

```
static_findings=none
selftest rc=0 checks=50 failed=0 fail_lines=0 ok=True
per_class header=17 sect=20 value=20 mask=16 word=19 range=16 indent=17 order=16 drop=17 multi=16 glob=16 alias=14 fallback=14 zerosize=14 mode=17 desktop=16
case_modes text=240 none=20 cache=5
control do_nothing text=0/240 none=20/20 cache_cases=5
control name_only correct=27/265
control naive (fallback-only) correct=86/265
control memoriser frozen=156/265 fresh=1/40
control forgery static=import:ctypes:8,... audit_denials=5 rejected=True
host_db=ok files=8 ; host list paths=4 ; host readable=4 pairs=8 correct=8
MADO_MAGICTEXT_COUNT: DRAFT_TARGET_MISSED ... cases=265 correct=265 classes=16/16
  fresh=315/315 fresh_cases=40 host=8/8 host_paths=4 mutants=0 killed=0 class_kills=0/16
  static_no_external_resolver=ok audit_denials=0 selftest=ok checks=50 failed=0
  controls do_nothing_text=0/240 do_nothing_none=20/20 naive=86 name_only=27
  memoriser_fresh=1/40 forgery=rejected host_db=ok files=8
```

The tool's line is exact on every scored leg; the verdict is TARGET_MISSED only because of the
empty mutant file (F1), `memo_fresh=1` (F2) and the 4-path host list (<1500, my scratch
choice). The frozen/fresh/host behavior is not the blocker.

Note on the real fresh generator: with the fixed cap (sha 32d38e) it emits 40 cases / 315
inputs at seed 7, max 12 inputs per case, no zero-input cases; the earlier builds crashed on
`len(val) % word` with word=0 and emitted 13-15 inputs per case, both fixed during the wave.
Labels are oracle-exact on seeds 1, 7 and 11 (0 drift, 0 tool mismatches).

## Residual risk and verification gaps

- The mutant file and the class-kill measurement are the remaining evidence; today the file is
  a placeholder (`<awaiting-candidate>`), so (iv) is unmeasured.
- The "memoriser 0 on fresh" control fails at 1/40; decide env-aware key or "misses at least
  one" before the freeze.
- The do-nothing sentence should say "on the text-mode cases" (F4); the none-mode census is
  printed separately.
- The full 4911-path host leg and the full mutant leg were not run by me; I sampled 400 paths /
  800 pairs (all exact) plus the counter's 8/8. The L1's receipt must run the full list.
- The shared contract's cache sentence (F7) and the word-size sentence (F8) should be amended;
  the case file, tool and counter already follow the C.
- Any further edit to the tool, cases, fresh generator, counter or declaration invalidates the
  shas above; re-pin at freeze. In particular, the declaration command was itself edited during
  wave: the current version (12:14) matches the current counter's argv; an earlier version
  was not replayable (F3).
- Tool installs: none. The oracle used the host `cc` and `pkg-config`; no pacman/uv/npx
  transaction was run.

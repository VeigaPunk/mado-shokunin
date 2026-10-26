# MutW2Tool — round-45 w2 falsification: mutation-test tools/mado-monitors.py against PRED-C1-r45-v2

## What was attacked
The round-45 w2 falsification (closure D1: the w2 never ran) — i.e. the adequacy of the frozen counter
`quality/counters/c1-r45-monitors-v2.py` (PRED-C1-r45-v2) as the sole detector for the landed tool
`tools/mado-monitors.py` at 4d22eeb66c2835af8aaa3fac6ad838fa616aa663 (sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609,
byte-identical to the current lane file and to the counter's MODEL_SHA256).

## Method
- 100 anchored single-site mutants (one behavior-bearing token each; full old->new table in `mutants.json`), all compile-checked.
- Detector = the counter's own code replayed in-process (sanctioned by the tasking): `run_fixture` (bwrap sandbox, fakebin
  marker, env A/B, name tables seed 45) over all 81 fixtures x 3 variants, then `--selftest`, the clause-r marker check,
  and for fixture-survivors `run_generated` (150 cases, --nonce 45, judged by the pinned v2 reference).
- Baseline: pristine passes everything (fixtures 81/81 x3, selftest ok, marker absent, generated 150/150) -> detector sound.
- Cross-check with the REAL counter invocation on scratch clones at --nonce 45: pristine rc=0 TARGET_MET;
  mutant M01 rc=0 **TARGET_MET** (rev b2a8acc05b9a375fae87f8b5171f96ba4976e827); mutant M39 rc=1 TARGET_MISSED (fixtures 80/81).
  Receipts: `real/pristine.txt`, `real/M01-survivor.txt`, `real/M39-killed.txt`.

## Result: 100 mutants -> 68 killed, 32 fixture-survivors (31 survive the ENTIRE counter battery)
- 68 KILLED by the fixture battery (killing fixture in the table) — the fixtures have real teeth on the tested classes.
- 32 survive all 81 fixtures x 3 variants; 31 of those also survive generated 150/150 + selftest + readonly, i.e. the real
  counter prints `verdict=TARGET_MET` for those mutated tools (proven end-to-end for M01). M44 survives fixtures but is
  killed by the generated battery (146/150).
- Of the 32 survivors, 6 are true equivalents (dead or masked code, noted below); 26 are genuine coverage gaps —
  untested input classes a mutated tool still scores TARGET_MET on.

## Survivor table (a nearest-target fixture per survivor; the mutant passes it)
| id | site (computed grep -n) | mutation | verdict | fixture per survivor |
| M01 | `tools/mado-monitors.py:113` | MAX_BYTES boundary -1 | SURVIVED | passes `setup-config-too-large`; all 81 fixtures x3 variants; generated 150/150 |
| M02 | `tools/mado-monitors.py:147` | read_regular loop <= -> < | SURVIVED (true equivalent) | passes `setup-config-too-large`; all 81 fixtures x3 variants; generated 150/150 |
| M03 | `tools/mado-monitors.py:161` | read_stdin loop <= -> < | SURVIVED (true equivalent) | passes `setup-dump-too-large`; all 81 fixtures x3 variants; generated 150/150 |
| M04 | `tools/mado-monitors.py:155` | read_regular too_large > -> >= | SURVIVED | passes `setup-config-too-large`; all 81 fixtures x3 variants; generated 150/150 |
| M05 | `tools/mado-monitors.py:119` | SCALE_RE decimals {1,6}->{1,5} | KILLED | `scale-unpredicted` (A) |
| M06 | `tools/mado-monitors.py:119` | SCALE_RE int part {1,2}->{1,1} | KILLED | `scale-unpredicted` (A) |
| M07 | `tools/mado-monitors.py:117` | MODE_RE width {1,5}->{1,4} | SURVIVED | passes `host`; all 81 fixtures x3 variants; generated 150/150 |
| M08 | `tools/mado-monitors.py:118` | POS_RE x {1,6}->{1,5} | SURVIVED | passes `position`; all 81 fixtures x3 variants; generated 150/150 |
| M09 | `tools/mado-monitors.py:120` | INT_RE {1,9}->{1,8} | SURVIVED (true equivalent) | passes `transform-key`; all 81 fixtures x3 variants; generated 150/150 |
| M10 | `tools/mado-monitors.py:121` | STOI_RE drop (?![0-9]) lookahead | SURVIVED | passes `addreserved-stoi-prefix`; all 81 fixtures x3 variants; generated 150/150 |
| M100 | `tools/mado-monitors.py:288` | position parsed from field 3 | KILLED | `host` (A) |
| M11 | `tools/mado-monitors.py:122` | LONGINT_RE {10,}->{11,} | SURVIVED | passes `transform-key-overflow`; all 81 fixtures x3 variants; generated 150/150 |
| M12 | `tools/mado-monitors.py:116` | V2_RE drop = { from char class | SURVIVED | passes `monitorv2`; all 81 fixtures x3 variants; generated 150/150 |
| M13 | `tools/mado-monitors.py:315` | V2_RE match -> fullmatch | KILLED | `monitorv2` (A) |
| M14 | `tools/mado-monitors.py:115` | LINE_RE [ \t]* -> [ \t]+ | SURVIVED | passes `host`; all 81 fixtures x3 variants; generated 150/150 |
| M15 | `tools/mado-monitors.py:318` | LINE_RE fullmatch -> match | SURVIVED (true equivalent) | passes `host`; all 81 fixtures x3 variants; generated 150/150 |
| M16 | `tools/mado-monitors.py:314` | config line strip adds \v\f | SURVIVED | passes `isspace-trim`; all 81 fixtures x3 variants; generated 150/150 |
| M17 | `tools/mado-monitors.py:313` | config split \n -> splitlines | KILLED | `isspace-trim` (A) |
| M18 | `tools/mado-monitors.py:249` | unsupported gate drops $ | KILLED | `variable` (A) |
| M19 | `tools/mado-monitors.py:249` | unsupported gate drops ## | SURVIVED | passes `comments`; all 81 fixtures x3 variants; generated 150/150 |
| M20 | `tools/mado-monitors.py:249` | unsupported gate drops backslash | SURVIVED | passes `variable`; all 81 fixtures x3 variants; generated 150/150 |
| M21 | `tools/mado-monitors.py:252` | no comment cut in body | KILLED | `comments` (A) |
| M22 | `tools/mado-monitors.py:253` | fields not stripped | KILLED | `host` (A) |
| M23 | `tools/mado-monitors.py:260` | disable key drops 'disabled' | KILLED | `disabled-but-live` (A) |
| M24 | `tools/mado-monitors.py:266` | transform modifier reads fld(3) | KILLED | `transform-modifier` (A) |
| M25 | `tools/mado-monitors.py:267` | transform modifier bad value accepted | KILLED | `transform-modifier-bad` (A) |
| M26 | `tools/mado-monitors.py:271` | transform modifier matches other sel | KILLED | `transform-modifier` (A) |
| M27 | `tools/mado-monitors.py:278` | addreserved checks fields 2-4 only | SURVIVED | passes `addreserved-bad-fields`; all 81 fixtures x3 variants; generated 150/150 |
| M28 | `tools/mado-monitors.py:281` | addreserved keeps existing rule ignored | KILLED | `addreserved-keeps-rule` (A) |
| M29 | `tools/mado-monitors.py:283` | addreserved default rule sel empty | KILLED | `addreserved-adds-default` (A) |
| M30 | `tools/mado-monitors.py:204` | mode pref prefix -> prefx | KILLED | `fallback-preferred` (A) |
| M31 | `tools/mado-monitors.py:206` | mode keywords drop highres | KILLED | `highres-not-compared` (A) |
| M32 | `tools/mado-monitors.py:210` | modeline case-sensitivity via lower() drop | SURVIVED (true equivalent) | passes `modeline-unsupported`; all 81 fixtures x3 variants; generated 150/150 |
| M33 | `tools/mado-monitors.py:221` | default rate 60 -> 61 | KILLED | `no-rate-requests-60` (A) |
| M34 | `tools/mado-monitors.py:217` | 0x0 sentinel and -> or | SURVIVED | passes `zero-mode-is-preferred`; all 81 fixtures x3 variants; generated 150/150 |
| M35 | `tools/mado-monitors.py:225` | pos auto prefix -> Auto | KILLED | `auto-position` (A) |
| M36 | `tools/mado-monitors.py:225` | scale auto prefix -> Auto | KILLED | `fallback-preferred` (A) |
| M37 | `tools/mado-monitors.py:236` | scale regex gate inverted | KILLED | `host` (A) |
| M38 | `tools/mado-monitors.py:239` | tiny scale threshold 0.25 -> 0.2 | KILLED | `scale-tiny-is-1` (A) |
| M39 | `tools/mado-monitors.py:400` | rate tolerance < -> <= | KILLED | `rate-exactly-1-off` (A) |
| M40 | `tools/mado-monitors.py:399` | rate type check is_num -> is_int | KILLED | `host` (A) |
| M41 | `tools/mado-monitors.py:399` | mode w/h type check is_int -> is_num | SURVIVED | passes `wrong-types`; all 81 fixtures x3 variants; generated 150/150 |
| M42 | `tools/mado-monitors.py:404` | position y unchecked | KILLED | `stdin` (A) |
| M43 | `tools/mado-monitors.py:414` | scale tolerance >= -> > | SURVIVED | passes `scale-1.3-as-written`; all 81 fixtures x3 variants; generated 150/150 |
| M44 | `tools/mado-monitors.py:348` | expected_scale whole and -> or | SURVIVED | passes `scale-clean`; all 81 fixtures x3 variants; generated 146/150 |
| M45 | `tools/mado-monitors.py:350` | scale k half-up +0.5 dropped | SURVIVED | passes `scale-1.3-corrected`; all 81 fixtures x3 variants; generated 150/150 |
| M46 | `tools/mado-monitors.py:354` | scale search 89 -> 87 steps | SURVIVED | passes `scale-1.3-corrected`; all 81 fixtures x3 variants; generated 150/150 |
| M47 | `tools/mado-monitors.py:355` | scale search drops down-direction | KILLED | `scale-1.4-corrected` (A) |
| M48 | `tools/mado-monitors.py:422` | mirror ids guard dropped | SURVIVED | passes `mirror-missing`; all 81 fixtures x3 variants; generated 150/150 |
| M49 | `tools/mado-monitors.py:424` | mirrorOf none sentinel -> empty | KILLED | `host` (A) |
| M50 | `tools/mado-monitors.py:373` | effective last-rule scan reversed | KILLED | `desc-added-later-wins` (A) |
| M51 | `tools/mado-monitors.py:377` | desc: prefix match loses colon | SURVIVED | passes `desc-empty`; all 81 fixtures x3 variants; generated 150/150 |
| M52 | `tools/mado-monitors.py:378` | desc text not whitespace-stripped | KILLED | `desc-text-space` (A) |
| M53 | `tools/mado-monitors.py:379` | desc short/long or -> and | KILLED | `desc-added-later-wins` (A) |
| M54 | `tools/mado-monitors.py:384` | empty fallback returns first rule | KILLED | `desc-not-prefix` (A) |
| M55 | `tools/mado-monitors.py:392` | DISABLED/DIFFER branches swapped | KILLED | `disabled-agree` (A) |
| M56 | `tools/mado-monitors.py:393` | live_disabled check removed | KILLED | `live-disabled` (A) |
| M57 | `tools/mado-monitors.py:397` | explicit-mode gate inverted | KILLED | `no-rate-requests-60` (A) |
| M58 | `tools/mado-monitors.py:402` | position gate inverted | KILLED | `position` (A) |
| M59 | `tools/mado-monitors.py:406` | scale gate inverted | KILLED | `fallback-preferred` (A) |
| M60 | `tools/mado-monitors.py:408` | scale w/h positivity and -> or | SURVIVED | passes `scale-clean`; all 81 fixtures x3 variants; generated 150/150 |
| M61 | `tools/mado-monitors.py:417` | transform type check dropped | SURVIVED | passes `wrong-types`; all 81 fixtures x3 variants; generated 150/150 |
| M62 | `tools/mado-monitors.py:426` | single-field DIFFER suppressed | KILLED | `no-rate-requests-60` (A) |
| M63 | `tools/mado-monitors.py:428` | unpredicted/AGREE verdicts swapped | KILLED | `host` (A) |
| M64 | `tools/mado-monitors.py:434` | rule mode print %.2f -> %.3f | KILLED | `host` (A) |
| M65 | `tools/mado-monitors.py:436` | rule scale print %.4f -> %.3f | KILLED | `host` (A) |
| M66 | `tools/mado-monitors.py:438` | rule sel printed unquoted | KILLED | `host` (A) |
| M67 | `tools/mado-monitors.py:439` | rule mirror always json | KILLED | `host` (A) |
| M68 | `tools/mado-monitors.py:439` | rule disabled literals swapped | KILLED | `host` (A) |
| M69 | `tools/mado-monitors.py:463` | NO_RULES and -> or | KILLED | `host` (A) |
| M70 | `tools/mado-monitors.py:465` | NOT_COMPARED drops notcompared count | KILLED | `scale-unpredicted` (A) |
| M71 | `tools/mado-monitors.py:465` | NOT_COMPARED drops unsupported count | KILLED | `variable` (A) |
| M72 | `tools/mado-monitors.py:467` | DIFFER gate > -> >= | KILLED | `host` (A) |
| M73 | `tools/mado-monitors.py:469` | NO_MATCHING_MONITOR gate inverted | KILLED | `host` (A) |
| M74 | `tools/mado-monitors.py:477` | notcompared suffix always printed | KILLED | `host` (A) |
| M75 | `tools/mado-monitors.py:451` | outputs counter double-counts | KILLED | `host` (A) |
| M76 | `tools/mado-monitors.py:458` | compare uses first rule always | KILLED | `desc-added-later-wins` (A) |
| M77 | `tools/mado-monitors.py:462` | empty differ list not dashed | KILLED | `host` (A) |
| M78 | `tools/mado-monitors.py:178` | argparse pair boundary > -> >= | SURVIVED | passes `setup-usage`; all 81 fixtures x3 variants; generated 150/150 |
| M79 | `tools/mado-monitors.py:181` | double --monitors allowed | SURVIVED | passes `setup-usage`; all 81 fixtures x3 variants; generated 150/150 |
| M80 | `tools/mado-monitors.py:188` | empty --config list accepted | KILLED | `setup-usage` (A) |
| M81 | `tools/mado-monitors.py:571` | stdin path removed | KILLED | `stdin` (A) |
| M82 | `tools/mado-monitors.py:572` | config decode strict utf-8 | SURVIVED | passes `setup-bad-utf8`; all 81 fixtures x3 variants; generated 150/150 |
| M83 | `tools/mado-monitors.py:328` | bad_json drops RecursionError | KILLED | `setup-deep-json` (A) |
| M84 | `tools/mado-monitors.py:330` | dump element type check dropped | KILLED | `setup-not-objects` (A) |
| M85 | `tools/mado-monitors.py:340` | is_num drops isfinite | KILLED | `nan-scale` (A) |
| M86 | `tools/mado-monitors.py:321` | lines counter increments v2 | KILLED | `host` (A) |
| M87 | `tools/mado-monitors.py:316` | v2 counter double-counts | KILLED | `monitorv2` (A) |
| M88 | `tools/mado-monitors.py:199` | add() keeps same-selector rules | KILLED | `transform-modifier` (A) |
| M89 | `tools/mado-monitors.py:200` | add() prepends instead of appends | KILLED | `desc-added-later-wins` (A) |
| M90 | `tools/mado-monitors.py:194` | default rate 60 -> 59 | SURVIVED (true equivalent) | passes `no-rate-requests-60`; all 81 fixtures x3 variants; generated 150/150 |
| M91 | `tools/mado-monitors.py:195` | default transform 0 -> 1 | KILLED | `host` (A) |
| M92 | `tools/mado-monitors.py:195` | default position None -> (0,0) | KILLED | `auto-position` (A) |
| M93 | `tools/mado-monitors.py:195` | default scale None -> 1.0 | KILLED | `fallback-preferred` (A) |
| M94 | `tools/mado-monitors.py:114` | WS loses \v\f | KILLED | `isspace-trim` (A) |
| M95 | `tools/mado-monitors.py:259` | kind reads field 2 | KILLED | `host` (A) |
| M96 | `tools/mado-monitors.py:291` | key loop uses index bound | SURVIVED | passes `ignored-keys`; all 81 fixtures x3 variants; generated 150/150 |
| M97 | `tools/mado-monitors.py:297` | transform key renamed | KILLED | `transform-key` (A) |
| M98 | `tools/mado-monitors.py:303` | mirror key renamed | KILLED | `mirror-agree` (A) |
| M99 | `tools/mado-monitors.py:298` | transform overflow gate removed | KILLED | `transform-key-overflow` (A) |

## Survivor notes (what input class is untested)
- M01: input of exactly 1048576 bytes: pristine accepts, mutant rejects too_large; no fixture at the boundary
- M02: true equivalent: chunk size MAX+1-len reads ahead, loop bound unobservable
- M03: true equivalent: same read-ahead argument on stdin
- M04: input of exactly 1048576 bytes: pristine accepts, mutant rejects; boundary untested
- M07: 5-digit dimensions (e.g. 65535x2160) untested; all fixtures <= 4 digits
- M08: 6-digit coordinates untested; fixtures use <= 6 minus none at the {1,6} boundary
- M09: true equivalent: any >=2-digit transform value exceeds 0-7 either way
- M10: 10-digit addreserved field: pristine badrules, mutant accepts; untested
- M11: 10-digit transform value: pristine unsupported, mutant keeps rule; untested
- M12: 'monitorv2{' / 'monitorv2=' lines: pristine counts v2, mutant does not; untested
- M14: 'monitor=...' without space: pristine matches LINE_RE, mutant does not; untested
- M15: true equivalent: (.*) swallows the rest, match == fullmatch at pos 0
- M16: lines padded with \v or \f at the ends: pristine ignores, mutant parses; untested
- M19: body containing '##': pristine unsupported, mutant parses; untested
- M20: body containing a backslash (e.g. mirror value 'a\\b'): pristine unsupported, mutant parses; untested
- M27: bad 5th addreserved field: pristine badrules, mutant adds default rule; untested
- M32: true equivalent: case-variant 'Modeline' still fails MODE_RE -> Unsupported
- M34: modes '0xH' or 'Wx0': pristine explicit w/h=0, mutant preferred; untested
- M41: float width/height in dump: pristine mode-DIFFER, mutant accepts; untested
- M43: scale delta of exactly 0.0001: pristine DIFFER, mutant AGREE; untested
- M44: survives all 81 fixtures x3; killed by generated battery (146/150, e.g. 1920x1080 with scale 1.6)
- M45: s*120 fractional part in (0.5,1): half-up rounding untested
- M46: solutions at search step i=88/89 untested; fixture solutions at i<=8
- M48: rule mirror names an output ABSENT from the dump: pristine DIFFER, mutant IndexError crash; untested
- M51: bare selector 'desc' (no colon): pristine name-match, mutant desc-prefix '' matches everything; untested
- M60: dump width or height 0: pristine scale-DIFFER, mutant proceeds; untested
- M61: bool transform equal to rule value (transform=true, rule 1): pristine DIFFER, mutant AGREE; untested
- M78: odd-length argv (dangling flag): pristine usage rc2, mutant IndexError crash; untested
- M79: two --monitors flags: pristine usage, mutant last-wins; untested
- M82: non-UTF-8 config file: pristine replaces chars, mutant crashes; untested
- M90: true equivalent: new_rule rate is write-only (parse_mode overwrites for explicit; never printed otherwise)
- M96: trailing empty field (',,' tail): pristine stops, mutant counts '' as unknown key; untested

## Killed mutants (68)
M05, M06, M100, M13, M17, M18, M21, M22, M23, M24, M25, M26, M28, M29, M30, M31, M33, M35, M36, M37, M38, M39, M40, M42, M47, M49, M50, M52, M53, M54, M55, M56, M57, M58, M59, M62, M63, M64, M65, M66, M67, M68, M69, M70, M71, M72, M73, M74, M75, M76, M77, M80, M81, M83, M84, M85, M86, M87, M88, M89, M91, M92, M93, M94, M95, M97, M98, M99

## Findings
1. The counter's fixture+generated battery leaves at least 26 behavior classes unobserved (table above): size boundaries at
   exactly 1048576 bytes (M01/M04 — real counter run proves TARGET_MET on the M01 tool), 5-digit dimensions (M07), 6-digit
   coordinates (M08), 10-digit stoi/transform values (M10/M11), `monitorv2{`/`monitorv2=` forms (M12), `monitor=` without
   space (M14), \v\f-padded line ends (M16), `##` and backslash bodies (M19/M20), addreserved 5th field (M27), `0xH`/`Wx0`
   modes (M34), float width/height (M41), the exact 0.0001 scale boundary (M43), the half-up k boundary (M45), search steps
   88-89 (M46), an absent mirror target (M48 — mutant crashes where pristine DIFFERs), bare `desc` selector (M51), zero
   dims (M60), bool transform equal to the rule value (M61), odd-length argv (M78), double `--monitors` (M79), non-UTF-8
   config (M82), trailing empty fields (M96).
2. Dead/masked code the battery cannot see (true equivalents): `new_rule`'s `rate: 60.0` is write-only (M90); `INT_RE`'s
   {1,9} bound is immaterial because any >=2-digit transform value exceeds 0-7 anyway (M09); the read loops' `<=` bounds are
   masked by the MAX+1-len read-ahead (M02/M03); `lower()` is immaterial for the modeline gate (M32); `fullmatch` == `match`
   for `monitor[ \t]*=(.*)` (M15).
3. This supports closure D1: the round-45 w2 mutation falsification never ran, and the counter it would have exercised
   has substantial survivor surface. A surviving mutant is a coverage finding, not a defect of the tool: the landed tool's
   behavior at these sites matches its contract; the CONTRACT's test battery is what leaves them unobserved.

## Evidence & restoration
- Pristine bytes: `git show 4d22eeb66c2835af8aaa3fac6ad838fa616aa663:tools/mado-monitors.py` -> sha256 2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609.
- Mutants lived only in /fast/scratch/hyaku/mado-r46/MutW2Tool/mutants/ (deleted after receipt copy); the lane was never
  written outside this seat dir; lane `tools/mado-monitors.py` sha256 re-verified 2f007417... after the campaign.
- Receipts copied here: `mutants.json` (100 old->new + sha256), `results.json` (per-mutant verdicts + first failures),
  `baseline.json`, `summary.json`, `real/*.txt` (real-counter runs).
- No pacman transaction, no host-service/compositor mutation, no tool installs. Scratch removed before finish.

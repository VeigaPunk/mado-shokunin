# Mutation matrix — ctl-ref-tool.py.txt selftest × c1-r41-globals.py fixtures

Seat MutSelftestFixtures, mado round 41 w1, 2026-10-25. Target: the frozen reference
`.ufo/waves/round-41/c1/ctl-ref-tool.py.txt` (sha256 `61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0`,
unmodified throughout — mutants lived only in `/tmp/mut41sf.zzOFli`, removed afterwards).

## Method

- Sites enumerated with Python `ast` over the pristine source: every `Compare` op
  (op-flip via Eq<->NotEq, Lt<->GtE, Gt->LtE, LtE->Gt, GtE->Lt, In<->NotIn, Is<->IsNot),
  every `Constant` (int/float +1, bool flip, str +"X", bytes +b"X"; None/Ellipsis skipped,
  no sensible single mutant), every `BoolOp` (and<->or), every `If`/`IfExp` test (negated).
  **495 sites: 70 cmp, 382 const, 19 boolop, 24 if** — each applied as one single mutant
  (`ast` rewrite + `ast.unparse`, compile-checked).
- Detector (a): the mutant's own `--selftest`, run directly (`python3 -I`, 60 s cap);
  killed = rc != 0 or printed k != n or no summary line.
- Detector (b): the frozen counter `quality/counters/c1-r41-globals.py` run against the
  mutant via `--tool` (controls mode), `--repo <lane> --rev 60c3914154333180450d5da27ba222d5763cc56a
  --nonce 4d75745346696c31` (fixed nonce, deterministic 24-fixture lattice); killed = any
  of the 24 `fixture=` lines with ok=0. Counter clauses b2/g recorded separately (b2 re-uses
  its own nonce-chosen flips; g is the import/denylist heuristic).
- Baseline (pristine, same nonce/rev): selftest `47/47 passed` rc 0; counter
  `fixtures=24/24 tool=present verdict=TARGET_MET` rc 0; b2 sites=12 killed=6/6.
- Survivor classification (EQ / EQC / EQP / MASK / MC / MC/PROBE) verified by: targeted
  behavioral demos (mutant vs pristine on crafted inputs, quoted below), a 3000-journal
  differential fuzz for the parse-level equivalence claims, and structural proofs; see notes.

## Tally

| verdict | count |
|---|---|
| killed by both detectors | 128 |
| killed by selftest only | 206 |
| killed by fixtures only | 69 |
| **survived both** | **92** |
| total mutants (1 site each) | 495 |

Survivor breakdown: EQ 25, EQC 6, EQP 2, MASK 12, MC 29, MC/PROBE 18.

Legend: **EQ** equivalent (proof given) · **EQC** equivalent-in-context/under-contract
(behavior indistinguishable by any blackbox check available to the detectors) · **EQP**
equivalent under this predicate (consumers accept it by construction) · **MASK** property
re-pinned by another selftest line or by fixture byte-exactness · **MC** missing check
(assertion/fixture that would kill it is named) · **MC/PROBE** missing check of probe-pin
kind: the mutant perturbs the selftest's own negative-probe bytes, which stay rejected a
fortiori, so it is unkillable in place — only pinning the probe bytes kills it.

## Headline findings

1. **The empty-side `--diff` rendering is untested** (ids 118, 121, report:132-133):
   `MADO_GLOBALS_DIFF` never renders an empty added/removed side in any fixture (all diff
   fixtures have non-empty drift). Demo: two sessions with identical name sets, versions
   3>4 — pristine `added=- removed=-`, mutant `added=-X removed=-`. Killing fixture: a
   `--diff` case with version-only drift, model output `added=- removed=-` byte-exact.
2. **`(ver 0)` adverts render `ver=1`** (id 80, parse:102 second zero): every fixture and
   selftest datum uses ver >= 1. Demo: `wl_seat (ver 0)` -> mutant `MADO_GLOBAL: ... ver=1`,
   pristine `ver=0`. Kill: any fixture/selftest datum with a 0-version advert.
3. **The live env allowlist is only checked for absence of extras** (ids 168-170): the
   counter stub never requires PATH/XDG_RUNTIME_DIR/DBUS_SESSION_BUS_ADDRESS/LC_ALL to be
   forwarded, so dropping them is invisible. Demo: stub `[ -n "$XDG_RUNTIME_DIR" ] || exit 9`
   -> mutant rc5 `journalctl_failed`, pristine rc3 report. Kill: stub asserting presence.
4. **PATH-resolution shadowing** (id 158): `isfile and access` -> `or` lets a *directory*
   named `journalctl` shadow a real program later on PATH (access(dir, X_OK) is true).
   Demo: dir shadow -> mutant `SETUP journalctl_unusable` rc5, pristine proceeds. Related
   untested resolution edges: relative slashful prog (150), PATH unset (153), empty PATH
   element (156). Kill: a live fixture with a directory shadow / relative path.
5. **`--help` is untested** (id 192): with `add_help` flipped the tool prints argparse help
   to stdout before the SETUP line; no fixture passes `-h`/`--help` (usage0 cases would catch
   it byte-exactly if one did).
6. **The spawn-failure/timeout branch of read_live is never exercised** (ids 174-175,
   line 184): livefail0 covers only the returncode branch (line 186); a `#!/nonexistent`
   shebang stub (OSError) or an over-slow stub (TimeoutExpired) would kill.
7. **Selftest bookkeeping is mutually unpinned** (206 killed-selftest-only rows include the
   ok/n counters): `n = 0`->1, `n += 1`->2, `return 0`->1, `ok == n` negate/flip are all
   caught ONLY by the selftest (fixtures 24/24) — i.e. the fixtures' clause-b is the only
   thing forcing an honest summary, and the summary format itself is only search-anchored
   (id 481 survives because both consumers use unanchored `re.search`).
8. **Clause g caught exactly one mutant the other detectors also catch** (id 173,
   `shell=False`->`True`: fixtures 20/24, g:0). Notably the selftest passed 47/47 because
   its own stubs never check argv — the counter's live stub (`[ "$*" = ... ]`) is the only
   argv pin; a selftest stub with the same check would close that gap.

## Full matrix (495 mutants)

`st` = selftest k/n (rc), `fx` = fixtures passed/24 with failing names. Selftest k/n
`None` = crash/timeout before the summary line.

| id | kind | site | op | mutated segment | st | fx | class | note |
|---|---|---|---|---|---|---|---|---|

### Survived both (92)

| id | kind | site | op | mutated segment | st | fx | class | note |
|---|---|---|---|---|---|---|---|---|
| 0 | const | <module>:2 | str | `"""mado-globals — read-only census of the W...` | 47/47 (0) | 24/24 - | EQ | module docstring; no __doc__ consumer in tool or counter; stdout byte-identical |
| 52 | const | parse:78 | str | `"""Return sessions: dicts with boot, pid, f...` | 47/47 (0) | 24/24 - | EQ | parse() docstring; same |
| 56 | const | parse:82 | bool | `False` | 47/47 (0) | 24/24 - | EQ | boot_changed init True dominated by cur-is-None on first ADVERT; flag reset at every session open; parse equal over 3000-journal fuzz |
| 70 | const | parse:96 | str | `"last"` | 47/47 (0) | 24/24 - | EQ | dict-literal key 'last' dead: cur['last']=ts runs in the creation iteration; extra 'lastX' key never read; report() outputs equal over 3000-journal fuzz |
| 80 | const | parse:102 | int | `0` | 47/47 (0) | 24/24 - | MC | (ver 0) advert renders ver=1 (demo: mutant 'ver=1' vs pristine 'ver=0'). Kill: fixture with a 0-version advert (model pins ver=0), or selftest check names==[1,0] |
| 118 | const | report:132 | str | `"-"` | 47/47 (0) | 24/24 - | MC | empty-added --diff renders added=-X (demo: 'added=-X removed=-' vs 'added=- removed=-'). Kill: --diff fixture whose last two sessions share the name set with version drift only |
| 121 | const | report:133 | str | `"-"` | 47/47 (0) | 24/24 - | MC | same for the removed side (line 133) |
| 150 | const | resolve_program:155 | str | `"/"` | 47/47 (0) | 24/24 - | MC | '/'->'/X' in slash test: relative slashful prog ('bin/journalctl') takes the PATH-lookup branch and fails. Kill: live fixture passing a relative --journalctl path |
| 153 | const | resolve_program:156 | str | `""` | 47/47 (0) | 24/24 - | MC | PATH-unset default ''->'X': the empty-PATH-element cwd fallback is never consulted. Kill: run with PATH unset and prog in cwd (selftest can del os.environ['PATH']) |
| 156 | const | resolve_program:157 | str | `"."` | 47/47 (0) | 24/24 - | MC | 'd or .'->'X': PATH containing an empty element ('a::b') no longer maps to cwd. Kill: live1-style fixture with PATH=dir::/usr/bin |
| 158 | bool | resolve_program:158 | And | `os.path.isfile(cand) and os.access(cand, os...` | 47/47 (0) | 24/24 - | MC | And->Or: a DIRECTORY named journalctl earlier in PATH is selected (access(dir,X_OK)=True) -> unusable although a real stub exists later (demo: rc5 vs rc3). Kill: live fixture with fx/bin/journalctl as a directory and the stub in a later PATH dir |
| 168 | const | read_live:176 | str | `"XDG_RUNTIME_DIR"` | 47/47 (0) | 24/24 - | MC | XDG_RUNTIME_DIR not forwarded; counter stub only rejects FORBIDDEN vars, never requires allowed ones (demo: var-requiring stub -> rc5 vs rc3). Kill: stub '[ -n "${XDG_RUNTIME_DIR:-}" ] \|\| exit 9' |
| 169 | const | read_live:177 | str | `"DBUS_SESSION_BUS_ADDRESS"` | 47/47 (0) | 24/24 - | MC | same for DBUS_SESSION_BUS_ADDRESS |
| 170 | const | read_live:177 | str | `"LC_ALL"` | 47/47 (0) | 24/24 - | MC | same for LC_ALL |
| 172 | const | read_live:182 | int | `30` | 47/47 (0) | 24/24 - | MC | timeout 30->31: boundary unexercised. Kill: stub sleeping >30s and <=31s expecting journalctl_failed (weak: contract pins the reason, not the value) |
| 174 | const | read_live:184 | str | `"journalctl_failed"` | 47/47 (0) | 24/24 - | MC | except-branch Setup (spawn failure / TimeoutExpired) unpinned; livefail0 exercises only the returncode branch (its mutants 179/180 are killed). Kill: stub with '#!/nonexistent' shebang (OSError) or sleep-40 stub (timeout) |
| 175 | const | read_live:184 | int | `5` | 47/47 (0) | 24/24 - | MC | same branch, exit code 5. Kill: same fixture |
| 186 | const | read_file:195 | int | `1` | 47/47 (0) | 24/24 - | EQ | read(MAX_BYTES+1)->+2: len(read(k))>MAX iff size>MAX for both k; returned bytes identical when <=MAX |
| 191 | const | run:204 | str | `"mado-globals"` | 47/47 (0) | 24/24 - | EQ | argparse prog only formats help/usage text; add_help=False + overridden ap.error mean it is never printed |
| 192 | const | run:204 | bool | `False` | 47/47 (0) | 24/24 - | MC | -h/--help now prints argparse help text before the SETUP line (demo: usage text on stdout). Kill: usage fixture case ['--journal-file', jf, '--help'] expecting exactly 'MADO_GLOBALS: SETUP usage' |
| 203 | const | <lambda>:215 | str | `"usage"` | 47/47 (0) | 24/24 - | EQ | except SystemExit branch unreachable: ap.error overridden (never sys.exit), add_help=False (no -h action), no version action - defensive dead code |
| 229 | const | check:243 | int | `1` | 47/47 (0) | 24/24 - | MC | focus-grab advert version unpinned. Kill: check(s[0]['names']['hyprland_focus_grab_manager_v1'] == [1, 1]) |
| 230 | bool | check:245 | And | `len(s) == 1 and s[0]["adverts"] == 3` | 47/47 (0) | 24/24 - | MASK | adverts==3 re-asserted at line 279 on the same data |
| 247 | const | check:248 | str | `"wl_seat"` | 47/47 (0) | 24/24 - | EQ | classify input is a free member of the unknown-name class: classify is a table-get with default 'other', no special case for any name |
| 251 | const | check:249 | str | `"wl_seat"` | 47/47 (0) | 24/24 - | MC | pid-12 probe session's name unpinned (line 249 asserts only session count). Kill: assert parse(...)[1]['names'] == {'wl_seat': [1, 9]} |
| 252 | const | check:249 | int | `9` | 47/47 (0) | 24/24 - | MC | same probe's ver unpinned. Kill: same assertion |
| 260 | const | check:251 | str | `"wl_seat"` | 47/47 (0) | 24/24 - | MC | boot-split probe advert name unpinned (line 251 asserts len==2 only). Kill: assert [1]['names'] == {'wl_seat': [1, 9]} |
| 261 | const | check:251 | int | `9` | 47/47 (0) | 24/24 - | MC | same probe's ver. Kill: same |
| 265 | const | check:252 | bytes | `b"[LOG] \|"` | 47/47 (0) | 24/24 - | MC/PROBE | one-space '[LOG] \|' probe perturbed to '\|X': stays rejected a fortiori, unkillable in place; a parser accepting '[LOG] \| Got' slips the mutant selftest. Kill: pin probe bytes (assert the exact one-space line is rejected AND the fmt line is accepted) |
| 268 | const | check:253 | bytes | `b"[ERR]"` | 47/47 (0) | 24/24 - | MC/PROBE | '[ERR]' probe; same argument and kill |
| 271 | const | check:254 | bytes | `b"(ver 9) x"` | 47/47 (0) | 24/24 - | MC/PROBE | trailing-junk probe '(ver 9) x'->'x X'; same |
| 272 | const | check:255 | bool | `False` | 47/47 (0) | 24/24 - | MC | no-DIFF-without---diff unpinned. Kill: check(not any(x.startswith('MADO_GLOBALS_DIFF') for x in lines)) after line 255 (byte-exact fixtures also pin this at counter level) |
| 273 | bool | check:256 | And | `code == 0 and lines[-1].endswith("verdict=OK")` | 47/47 (0) | 24/24 - | MASK | code==0 short-circuits the endswith conjunct; OK-line shape pinned byte-exactly by gen*/diff* fixtures |
| 278 | const | check:257 | str | `"nope"` | 47/47 (0) | 24/24 - | MC | expect probe 'nope'->'nopeX': substring 'expected_missing=nope' still matches (prefix). Kill: token-exact assert, e.g. lines[-1].split('expected_missing=')[1].split()[0] == 'nope' |
| 279 | const | check:257 | bool | `False` | 47/47 (0) | 24/24 - | MC | diff=False->True on the ['nope'] call; same kill as 272 |
| 280 | bool | check:258 | And | `code == 1 and "expected_missing=nope" in li...` | 47/47 (0) | 24/24 - | MASK | code==1 short-circuits; missing-expect output pinned byte-exactly by expectmiss0 |
| 286 | const | check:259 | bool | `False` | 47/47 (0) | 24/24 - | MC | diff=False->True on the empty-sessions call; same kill as 272 |
| 287 | bool | check:260 | And | `code == 3 and "verdict=NO_SESSIONS" in line...` | 47/47 (0) | 24/24 - | MASK | code==3 short-circuits; NO_SESSIONS output pinned by nosess0/nosess1 |
| 293 | bool | check:261 | And | `NAME.fullmatch("a b") is None and NAME.full...` | 47/47 (0) | 24/24 - | MASK | first conjunct (NAME rejects 'a b') true, positive-match conjunct unobserved; positive-NAME pinned by expect0/expectmiss0 (valid expects must resolve or rc/verdict mismatch) |
| 295 | const | check:261 | str | `"a b"` | 47/47 (0) | 24/24 - | MC/PROBE | negative NAME probe 'a b'->'a bX': still rejected; kill: pin probe bytes |
| 297 | const | check:261 | str | `"a_b1"` | 47/47 (0) | 24/24 - | EQ | positive NAME probe is a free member of the contract class [A-Za-z0-9_]{1,128}; regex has no special case |
| 298 | bool | check:262 | And | `parse(b"") == [] and parse(b"\n\n") == []` | 47/47 (0) | 24/24 - | MASK | parse(b'')==[] short-circuits; whitespace-only rejection pinned by nosess1 and blank noise lines in byte-exact gen fixtures |
| 300 | const | check:262 | bytes | `b""` | 47/47 (0) | 24/24 - | MC/PROBE | empty-input probe b''->b'X': both parse to []; kill: pin probe bytes (structural) |
| 302 | const | check:262 | bytes | `b"\n\n"` | 47/47 (0) | 24/24 - | MC/PROBE | b'\n\n' probe; same |
| 309 | const | check:263 | int | `2` | 47/47 (0) | 24/24 - | MC | wl_shm advert ver in diff data unpinned (added-side ver never compared). Kill: check(s2[1]['names']['wl_shm'] == [1, 2]) |
| 310 | bool | check:265 | And | `len(s2) == 2 and s2[1]["boot"] == "b" * 32 ...` | 47/47 (0) | 24/24 - | MASK | first conjunct true; boot attribution re-pinned at lines 277-278 |
| 326 | const | check:268 | str | `"\n"` | 47/47 (0) | 24/24 - | EQ | '\n'->'\nX' join separator inside a substring membership check: per-line bytes unchanged, 'removed=...' stays contiguous |
| 333 | const | check:271 | bool | `False` | 47/47 (0) | 24/24 - | MASK | dedup assertion reads lines[-1], which stays final; no-DIFF-without-flag pinned by expectmiss0 (byte-exact, no --diff) |
| 340 | const | check:273 | bytes | `b"\r\n"` | 47/47 (0) | 24/24 - | MC/PROBE | CR probe perturbed; kill: pin probe bytes |
| 343 | const | check:274 | bytes | `b"wl-seat"` | 47/47 (0) | 24/24 - | MC/PROBE | dash-name probe perturbed (dash preserved, still rejected); kill: pin probe bytes |
| 348 | const | check:275 | bytes | `b"wl_seat"` | 47/47 (0) | 24/24 - | MC | first replace needle X'd so LHS becomes parse(data); '!=' trivially true; 129/128 boundary unpinned. Kill: check(not parse(data.replace(b'wl_seat', b'a'*129))[0]['names'] and parse(data.replace(b'wl_seat', b'a'*128))[0]['names']) |
| 349 | const | check:275 | bytes | `b"a"` | 47/47 (0) | 24/24 - | MC | 129-side name 'a'->'aX' = 130 chars, still rejected; a 129-accepting off-by-one parser slips. Kill: same boundary assertion as 348 |
| 350 | const | check:275 | int | `129` | 47/47 (0) | 24/24 - | MC | 129->130 literal; same kill (pins the exact 128/129 boundary) |
| 351 | const | check:275 | bytes | `b"wl_seat"` | 47/47 (0) | 24/24 - | MC | second needle X'd so RHS becomes parse(data); same kill |
| 356 | const | check:276 | bytes | `b"(ver 1234567)"` | 47/47 (0) | 24/24 - | MC/PROBE | 7-digit-ver probe perturbed; kill: pin probe bytes |
| 361 | const | check:277 | bytes | `b"-- Boot "` | 47/47 (0) | 24/24 - | MC/PROBE | uppercase-boot probe prefix perturbed; an uppercase-hex-accepting parser slips; kill: pin probe bytes |
| 362 | const | check:277 | bytes | `b"A"` | 47/47 (0) | 24/24 - | MC/PROBE | 'A'->'AX' (33 chars); same |
| 363 | const | check:277 | int | `32` | 47/47 (0) | 24/24 - | MC/PROBE | 32->33; same |
| 364 | const | check:277 | bytes | `b" --\n"` | 47/47 (0) | 24/24 - | MC/PROBE | ' --\n'->+X; same |
| 372 | const | check:278 | bytes | `b" --\n"` | 47/47 (0) | 24/24 - | MC | X glues onto the first advert line (silently unparsed) while boot is still asserted. Kill: extend line 278's check with [0]['adverts'] == 3 |
| 378 | const | check:279 | bytes | `b"\xff\xfe\n"` | 47/47 (0) | 24/24 - | MC/PROBE | invalid-UTF8 probe perturbed (stays invalid); kill: pin probe bytes |
| 394 | const | code_of:298 | str | `"bad"` | 47/47 (0) | 24/24 - | EQ | stub filename free (path flows from the return value; no assertion references the literal) |
| 395 | const | code_of:298 | str | `"#!/bin/sh\nexit 1\n"` | 47/47 (0) | 24/24 - | EQ | body 'exit 1\nX': sh exits at line 2; X never executed |
| 399 | const | code_of:300 | str | `"big"` | 47/47 (0) | 24/24 - | EQ | filename free |
| 404 | const | code_of:302 | str | `"gw"` | 47/47 (0) | 24/24 - | EQ | filename free |
| 405 | const | code_of:302 | str | `"#!/bin/sh\n"` | 47/47 (0) | 24/24 - | EQ | body irrelevant: resolve_program only stats, never executes |
| 406 | const | code_of:302 | int | `0o775` | 47/47 (0) | 24/24 - | EQC | 0o775->0o776: both must-reject (group- or other-writable), behaviorally indistinguishable by any blackbox check; note: S_IWGRP bit isolation weakened. Kill only by mode-pinning (meta) |
| 409 | const | code_of:304 | str | `"nx"` | 47/47 (0) | 24/24 - | EQ | filename free |
| 410 | const | code_of:304 | str | `"#!/bin/sh\n"` | 47/47 (0) | 24/24 - | EQ | body unexecuted |
| 411 | const | code_of:304 | int | `0o644` | 47/47 (0) | 24/24 - | EQC | 0o644->0o645: owner-exec still clear for the accessing user, same must-reject class |
| 414 | const | code_of:306 | str | `"absent"` | 47/47 (0) | 24/24 - | EQ | 'absent'->any nonexistent name (fresh tempdir), same class |
| 418 | const | code_of:308 | str | `"absent"` | 47/47 (0) | 24/24 - | EQ | same |
| 422 | const | code_of:310 | str | `"envs"` | 47/47 (0) | 24/24 - | EQ | filename free |
| 425 | const | code_of:311 | str | `"MADO_CANARY"` | 47/47 (0) | 24/24 - | MASK | canary var renamed: canary conjunct vacuous, but any leak also leaks HOME (conjunct 3 pins) and liveenv0 rejects forbidden vars |
| 426 | const | code_of:311 | str | `"1"` | 47/47 (0) | 24/24 - | EQ | canary value unused (stub checks presence only) |
| 427 | bool | code_of:313 | And | `b"PATH" in got and b"MADO_CANARY" not in go...` | 47/47 (0) | 24/24 - | MASK | 'PATH in got' true in every reachable state, check cannot fail in place; env-leak pinned by liveenv0 (stub exits 9 on any forbidden var) |
| 430 | const | code_of:313 | bytes | `b"MADO_CANARY"` | 47/47 (0) | 24/24 - | MASK | canary membership probe X'd; leak pinned by the HOME conjunct + liveenv0 |
| 432 | const | code_of:313 | bytes | `b"HOME"` | 47/47 (0) | 24/24 - | MASK | HOME membership probe X'd; leak pinned by the canary conjunct (selftest sets MADO_CANARY) + liveenv0 |
| 434 | const | code_of:314 | str | `"PATH"` | 47/47 (0) | 24/24 - | EQC | restore key 'PATH'->'PATHX': PATH left = td; no env consumer after selftest (no subprocess/PATH reads), unobservable in any detector run; hygiene note |
| 435 | const | code_of:314 | str | `""` | 47/47 (0) | 24/24 - | EQC | PATH-unset default ''->'X': same post-restore deadness |
| 440 | const | code_of:317 | str | `"absent"` | 47/47 (0) | 24/24 - | EQ | 'absent' probe: any nonexistent name, same class |
| 442 | const | code_of:318 | str | `"PATH"` | 47/47 (0) | 24/24 - | EQC | restore key X'd (line 318): same deadness as 434 |
| 443 | const | code_of:319 | str | `"j.txt"` | 47/47 (0) | 24/24 - | EQ | filename free |
| 444 | const | code_of:319 | str | `""` | 47/47 (0) | 24/24 - | EQ | body ''->'X': file read only in usage cases (parse unreached) and the rc-3 case ('X' is one noise line, NO_SESSIONS, same class) |
| 445 | const | code_of:319 | int | `0o644` | 47/47 (0) | 24/24 - | EQC | 0o644->0o645: readable either way, same class |
| 447 | const | code_of:320 | str | `"--journal-file"` | 47/47 (0) | 24/24 - | MC/PROBE | flag probe X'd: usage now arises from the misspelling, not the exclusivity rule. Kill: pin flag spellings (shared constants reused in a positive case) or assert both orderings with exact flags |
| 448 | const | code_of:320 | str | `"--live"` | 47/47 (0) | 24/24 - | MC/PROBE | same |
| 451 | const | code_of:321 | str | `"--journal-file"` | 47/47 (0) | 24/24 - | MC/PROBE | same |
| 452 | const | code_of:321 | str | `"--journalctl"` | 47/47 (0) | 24/24 - | MC/PROBE | same |
| 459 | const | code_of:323 | str | `"a b"` | 47/47 (0) | 24/24 - | EQ | bad-expect probe 'a b'->'a bX': whitespace, the discriminating feature vs the NAME class, is preserved, so the same bug classes stay caught |
| 481 | const | code_of:328 | str | `"MADO_GLOBALS_SELFTEST: %d/%d passed"` | 47/47 (0) | 24/24 - | EQP | summary 'passed'->'passedX': both consumers parse with unanchored re.search(r'MADO_GLOBALS_SELFTEST: (\d+)/(\d+) passed'), k/n still extracted, rc 0; predicate observation: clause b is deliberately search-based |
| 485 | const | code_of:329 | int | `1` | 47/47 (0) | 24/24 - | EQP | failure exit 1->2: branch taken only when the selftest already fails; both consumers test rc!=0 uniformly |

### Killed by selftest only (206)

| id | kind | site | op | mutated segment | st | fx | class | note |
|---|---|---|---|---|---|---|---|---|
| 159 | const | resolve_program:162 | str | `"journalctl_unusable"` | 46/47 (1) | 24/24 - | K-ST |  |
| 160 | const | resolve_program:162 | int | `5` | 46/47 (1) | 24/24 - | K-ST |  |
| 161 | const | resolve_program:167 | str | `"journalctl_unusable"` | 46/47 (1) | 24/24 - | K-ST |  |
| 162 | const | resolve_program:167 | int | `5` | 46/47 (1) | 24/24 - | K-ST |  |
| 167 | const | read_live:176 | str | `"PATH"` | 46/47 (1) | 24/24 - | K-ST |  |
| 216 | const | selftest:232 | int | `0` | 48/47 (1) | 24/24 - | K-ST |  |
| 217 | const | selftest:233 | int | `0` | 47/48 (1) | 24/24 - | K-ST |  |
| 218 | const | check:237 | int | `1` | 47/94 (1) | 24/24 - | K-ST |  |
| 219 | const | check:240 | str | `"2026-10-25T13:36:24-03:00"` | None/None (1) | 24/24 - | K-ST |  |
| 220 | const | check:241 | str | `" h xdg-desktop-portal-hyprland[%s]: [LOG] ...` | None/None (1) | 24/24 - | K-ST |  |
| 221 | const | check:242 | str | `"11"` | 42/47 (1) | 24/24 - | K-ST |  |
| 222 | const | check:242 | str | `"wl_seat"` | 46/47 (1) | 24/24 - | K-ST |  |
| 223 | const | check:242 | int | `9` | 45/47 (1) | 24/24 - | K-ST |  |
| 224 | const | check:242 | str | `"11"` | 44/47 (1) | 24/24 - | K-ST |  |
| 225 | const | check:242 | str | `"wl_seat"` | 46/47 (1) | 24/24 - | K-ST |  |
| 226 | const | check:242 | int | `5` | 46/47 (1) | 24/24 - | K-ST |  |
| 227 | const | check:243 | str | `"11"` | None/None (1) | 24/24 - | K-ST |  |
| 228 | const | check:243 | str | `"hyprland_focus_grab_manager_v1"` | 46/47 (1) | 24/24 - | K-ST |  |
| 231 | cmp | check:245 | Eq | `len(s) == 1` | 46/47 (1) | 24/24 - | K-ST |  |
| 232 | const | check:245 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 233 | cmp | check:245 | Eq | `s[0]["adverts"] == 3` | 46/47 (1) | 24/24 - | K-ST |  |
| 234 | const | check:245 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 235 | const | check:245 | str | `"adverts"` | None/None (1) | 24/24 - | K-ST |  |
| 236 | const | check:245 | int | `3` | 46/47 (1) | 24/24 - | K-ST |  |
| 237 | cmp | check:246 | Eq | `s[0]["names"]["wl_seat"] == [2, 9]` | 46/47 (1) | 24/24 - | K-ST |  |
| 238 | const | check:246 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 239 | const | check:246 | str | `"names"` | None/None (1) | 24/24 - | K-ST |  |
| 240 | const | check:246 | str | `"wl_seat"` | None/None (1) | 24/24 - | K-ST |  |
| 241 | const | check:246 | int | `2` | 46/47 (1) | 24/24 - | K-ST |  |
| 242 | const | check:246 | int | `9` | 46/47 (1) | 24/24 - | K-ST |  |
| 243 | cmp | check:247 | Eq | `classify("hyprland_focus_grab_manager_v1") ...` | 46/47 (1) | 24/24 - | K-ST |  |
| 244 | const | check:247 | str | `"hyprland_focus_grab_manager_v1"` | 46/47 (1) | 24/24 - | K-ST |  |
| 245 | const | check:247 | str | `"focus-grab"` | 46/47 (1) | 24/24 - | K-ST |  |
| 246 | cmp | check:248 | Eq | `classify("wl_seat") == "other"` | 46/47 (1) | 24/24 - | K-ST |  |
| 248 | const | check:248 | str | `"other"` | 46/47 (1) | 24/24 - | K-ST |  |
| 249 | cmp | check:249 | Eq | `len(parse(data + (fmt % ("12", "wl_seat", 9...` | 46/47 (1) | 24/24 - | K-ST |  |
| 250 | const | check:249 | str | `"12"` | 46/47 (1) | 24/24 - | K-ST |  |
| 253 | const | check:249 | int | `2` | 46/47 (1) | 24/24 - | K-ST |  |
| 254 | cmp | check:250 | Eq | `len(parse(data + b"-- Boot " + b"a" * 32 + ...` | 46/47 (1) | 24/24 - | K-ST |  |
| 255 | const | check:250 | bytes | `b"-- Boot "` | 46/47 (1) | 24/24 - | K-ST |  |
| 256 | const | check:250 | bytes | `b"a"` | 46/47 (1) | 24/24 - | K-ST |  |
| 257 | const | check:250 | int | `32` | 46/47 (1) | 24/24 - | K-ST |  |
| 258 | const | check:250 | bytes | `b" --\n"` | 46/47 (1) | 24/24 - | K-ST |  |
| 259 | const | check:251 | str | `"11"` | 46/47 (1) | 24/24 - | K-ST |  |
| 262 | const | check:251 | int | `2` | 46/47 (1) | 24/24 - | K-ST |  |
| 263 | cmp | check:252 | Eq | `parse(data.replace(b"[LOG] \|", b"[LOG] \|"...` | 46/47 (1) | 24/24 - | K-ST |  |
| 264 | const | check:252 | bytes | `b"[LOG] \|"` | 46/47 (1) | 24/24 - | K-ST |  |
| 266 | cmp | check:253 | Eq | `parse(data.replace(b"[LOG]", b"[ERR]")) == []` | 46/47 (1) | 24/24 - | K-ST |  |
| 267 | const | check:253 | bytes | `b"[LOG]"` | 46/47 (1) | 24/24 - | K-ST |  |
| 269 | cmp | check:254 | NotEq | `parse(data.replace(b"(ver 9)", b"(ver 9) x"...` | 46/47 (1) | 24/24 - | K-ST |  |
| 270 | const | check:254 | bytes | `b"(ver 9)"` | 46/47 (1) | 24/24 - | K-ST |  |
| 274 | cmp | check:256 | Eq | `code == 0` | 46/47 (1) | 24/24 - | K-ST |  |
| 275 | const | check:256 | int | `0` | 46/47 (1) | 24/24 - | K-ST |  |
| 276 | const | check:256 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 277 | const | check:256 | str | `"verdict=OK"` | 46/47 (1) | 24/24 - | K-ST |  |
| 281 | cmp | check:258 | Eq | `code == 1` | 46/47 (1) | 24/24 - | K-ST |  |
| 282 | const | check:258 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 283 | const | check:258 | str | `"expected_missing=nope"` | 46/47 (1) | 24/24 - | K-ST |  |
| 284 | cmp | check:258 | In | `"expected_missing=nope" in lines[-1]` | 46/47 (1) | 24/24 - | K-ST |  |
| 285 | const | check:258 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 288 | cmp | check:260 | Eq | `code == 3` | 46/47 (1) | 24/24 - | K-ST |  |
| 289 | const | check:260 | int | `3` | 46/47 (1) | 24/24 - | K-ST |  |
| 290 | const | check:260 | str | `"verdict=NO_SESSIONS"` | 46/47 (1) | 24/24 - | K-ST |  |
| 291 | cmp | check:260 | In | `"verdict=NO_SESSIONS" in lines[-1]` | 46/47 (1) | 24/24 - | K-ST |  |
| 292 | const | check:260 | int | `1` | None/None (1) | 24/24 - | K-ST |  |
| 294 | cmp | check:261 | Is | `NAME.fullmatch("a b") is None` | 46/47 (1) | 24/24 - | K-ST |  |
| 296 | cmp | check:261 | IsNot | `NAME.fullmatch("a_b1") is not None` | 46/47 (1) | 24/24 - | K-ST |  |
| 299 | cmp | check:262 | Eq | `parse(b"") == []` | 46/47 (1) | 24/24 - | K-ST |  |
| 301 | cmp | check:262 | Eq | `parse(b"\n\n") == []` | 46/47 (1) | 24/24 - | K-ST |  |
| 303 | const | check:263 | bytes | `b"-- Boot "` | 44/47 (1) | 24/24 - | K-ST |  |
| 304 | const | check:263 | bytes | `b"b"` | 44/47 (1) | 24/24 - | K-ST |  |
| 305 | const | check:263 | int | `32` | 44/47 (1) | 24/24 - | K-ST |  |
| 306 | const | check:263 | bytes | `b" --\n"` | 43/47 (1) | 24/24 - | K-ST |  |
| 307 | const | check:263 | str | `"11"` | 43/47 (1) | 24/24 - | K-ST |  |
| 308 | const | check:263 | str | `"wl_shm"` | 45/47 (1) | 24/24 - | K-ST |  |
| 311 | cmp | check:265 | Eq | `len(s2) == 2` | 46/47 (1) | 24/24 - | K-ST |  |
| 312 | const | check:265 | int | `2` | 46/47 (1) | 24/24 - | K-ST |  |
| 313 | cmp | check:265 | Eq | `s2[1]["boot"] == "b" * 32` | 46/47 (1) | 24/24 - | K-ST |  |
| 314 | const | check:265 | int | `1` | None/None (1) | 24/24 - | K-ST |  |
| 315 | const | check:265 | str | `"boot"` | None/None (1) | 24/24 - | K-ST |  |
| 316 | const | check:265 | str | `"b"` | 46/47 (1) | 24/24 - | K-ST |  |
| 317 | const | check:265 | int | `32` | 46/47 (1) | 24/24 - | K-ST |  |
| 318 | cmp | check:265 | Eq | `s2[0]["boot"] == "-"` | 46/47 (1) | 24/24 - | K-ST |  |
| 319 | const | check:265 | int | `0` | 46/47 (1) | 24/24 - | K-ST |  |
| 320 | const | check:265 | str | `"boot"` | None/None (1) | 24/24 - | K-ST |  |
| 321 | const | check:265 | str | `"-"` | 46/47 (1) | 24/24 - | K-ST |  |
| 322 | const | check:266 | bool | `True` | 45/47 (1) | 24/24 - | K-ST |  |
| 323 | const | check:267 | str | `"MADO_GLOBALS_DIFF: from=1 to=2 added=wl_sh...` | 46/47 (1) | 24/24 - | K-ST |  |
| 324 | const | check:268 | str | `"removed=hyprland_focus_grab_manager_v1,wl_...` | 46/47 (1) | 24/24 - | K-ST |  |
| 325 | cmp | check:268 | In | `"removed=hyprland_focus_grab_manager_v1,wl_...` | 46/47 (1) | 24/24 - | K-ST |  |
| 327 | const | check:269 | bool | `True` | 46/47 (1) | 24/24 - | K-ST |  |
| 328 | const | check:270 | str | `"MADO_GLOBALS_DIFF: sessions=1 none"` | 46/47 (1) | 24/24 - | K-ST |  |
| 329 | cmp | check:270 | In | `"MADO_GLOBALS_DIFF: sessions=1 none" in lines` | 46/47 (1) | 24/24 - | K-ST |  |
| 330 | const | check:271 | str | `"wl_shm"` | 46/47 (1) | 24/24 - | K-ST |  |
| 331 | const | check:271 | str | `"wl_shm"` | 46/47 (1) | 24/24 - | K-ST |  |
| 332 | const | check:271 | str | `"zz"` | 46/47 (1) | 24/24 - | K-ST |  |
| 334 | cmp | check:272 | Eq | `lines[-1].count("expected_missing=zz ") == 1` | 46/47 (1) | 24/24 - | K-ST |  |
| 335 | const | check:272 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 336 | const | check:272 | str | `"expected_missing=zz "` | 46/47 (1) | 24/24 - | K-ST |  |
| 337 | const | check:272 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 338 | cmp | check:273 | Eq | `parse(data.replace(b"\n", b"\r\n")) == []` | 46/47 (1) | 24/24 - | K-ST |  |
| 339 | const | check:273 | bytes | `b"\n"` | 46/47 (1) | 24/24 - | K-ST |  |
| 341 | cmp | check:274 | Eq | `parse(data.replace(b"wl_seat", b"wl-seat"))...` | 46/47 (1) | 24/24 - | K-ST |  |
| 342 | const | check:274 | bytes | `b"wl_seat"` | 46/47 (1) | 24/24 - | K-ST |  |
| 344 | const | check:274 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 345 | const | check:274 | str | `"adverts"` | None/None (1) | 24/24 - | K-ST |  |
| 346 | const | check:274 | int | `1` | 46/47 (1) | 24/24 - | K-ST |  |
| 347 | cmp | check:275 | NotEq | `parse(data.replace(b"wl_seat", b"a" * 129))...` | 46/47 (1) | 24/24 - | K-ST |  |
| 352 | const | check:275 | bytes | `b"a"` | 46/47 (1) | 24/24 - | K-ST |  |
| 353 | const | check:275 | int | `128` | 46/47 (1) | 24/24 - | K-ST |  |
| 354 | cmp | check:276 | Eq | `parse(data.replace(b"(ver 5)", b"(ver 12345...` | 46/47 (1) | 24/24 - | K-ST |  |
| 355 | const | check:276 | bytes | `b"(ver 5)"` | 46/47 (1) | 24/24 - | K-ST |  |
| 357 | const | check:276 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 358 | const | check:276 | str | `"adverts"` | None/None (1) | 24/24 - | K-ST |  |
| 359 | const | check:276 | int | `2` | 46/47 (1) | 24/24 - | K-ST |  |
| 360 | cmp | check:277 | Eq | `parse(b"-- Boot " + b"A" * 32 + b" --\n" + ...` | 46/47 (1) | 24/24 - | K-ST |  |
| 365 | const | check:277 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 366 | const | check:277 | str | `"boot"` | None/None (1) | 24/24 - | K-ST |  |
| 367 | const | check:277 | str | `"-"` | 46/47 (1) | 24/24 - | K-ST |  |
| 368 | cmp | check:278 | Eq | `parse(b"-- Boot " + b"a" * 32 + b" --\n" + ...` | 46/47 (1) | 24/24 - | K-ST |  |
| 369 | const | check:278 | bytes | `b"-- Boot "` | 46/47 (1) | 24/24 - | K-ST |  |
| 370 | const | check:278 | bytes | `b"a"` | 46/47 (1) | 24/24 - | K-ST |  |
| 371 | const | check:278 | int | `32` | 46/47 (1) | 24/24 - | K-ST |  |
| 373 | const | check:278 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 374 | const | check:278 | str | `"boot"` | None/None (1) | 24/24 - | K-ST |  |
| 375 | const | check:278 | str | `"a"` | 46/47 (1) | 24/24 - | K-ST |  |
| 376 | const | check:278 | int | `32` | 46/47 (1) | 24/24 - | K-ST |  |
| 377 | cmp | check:279 | Eq | `parse(data + b"\xff\xfe\n")[0]["adverts"] == 3` | 46/47 (1) | 24/24 - | K-ST |  |
| 379 | const | check:279 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 380 | const | check:279 | str | `"adverts"` | None/None (1) | 24/24 - | K-ST |  |
| 381 | const | check:279 | int | `3` | 46/47 (1) | 24/24 - | K-ST |  |
| 382 | cmp | check:280 | Eq | `classify("wp_security_context_manager_v1") ...` | 46/47 (1) | 24/24 - | K-ST |  |
| 383 | const | check:280 | str | `"wp_security_context_manager_v1"` | 46/47 (1) | 24/24 - | K-ST |  |
| 384 | const | check:280 | str | `"sandbox"` | 46/47 (1) | 24/24 - | K-ST |  |
| 385 | cmp | check:281 | Eq | `len(CLASS_OF) == sum(len(v) for v in CLASSE...` | 46/47 (1) | 24/24 - | K-ST |  |
| 386 | const | stub:285 | str | `"w"` | None/None (1) | 24/24 - | K-ST |  |
| 387 | const | code_of:294 | str | `":%d"` | 36/47 (1) | 24/24 - | K-ST |  |
| 388 | const | code_of:296 | str | `"good"` | 46/47 (1) | 24/24 - | K-ST |  |
| 389 | const | code_of:296 | str | `"#!/bin/sh\nprintf 'x'\n"` | 44/47 (1) | 24/24 - | K-ST |  |
| 390 | const | code_of:296 | int | `0o755` | 43/47 (1) | 24/24 - | K-ST |  |
| 391 | cmp | code_of:297 | Eq | `code_of(read_live, good) == b"x"` | 46/47 (1) | 24/24 - | K-ST |  |
| 392 | const | code_of:297 | bytes | `b"x"` | 46/47 (1) | 24/24 - | K-ST |  |
| 393 | cmp | code_of:298 | Eq | `code_of(read_live, stub("bad", "#!/bin/sh\n...` | 46/47 (1) | 24/24 - | K-ST |  |
| 396 | const | code_of:298 | int | `0o755` | 46/47 (1) | 24/24 - | K-ST |  |
| 397 | const | code_of:299 | str | `"journalctl_failed:5"` | 46/47 (1) | 24/24 - | K-ST |  |
| 398 | cmp | code_of:300 | Eq | `code_of(read_live, stub("big", "#!/bin/sh\n...` | 46/47 (1) | 24/24 - | K-ST |  |
| 400 | const | code_of:300 | str | `"#!/bin/sh\nhead -c 9000000 /dev/zero\n"` | 46/47 (1) | 24/24 - | K-ST |  |
| 401 | const | code_of:300 | int | `0o755` | 46/47 (1) | 24/24 - | K-ST |  |
| 402 | const | code_of:301 | str | `"journalctl_too_large:5"` | 46/47 (1) | 24/24 - | K-ST |  |
| 403 | cmp | code_of:302 | Eq | `code_of(resolve_program, stub("gw", "#!/bin...` | 46/47 (1) | 24/24 - | K-ST |  |
| 407 | const | code_of:303 | str | `"journalctl_unusable:5"` | 46/47 (1) | 24/24 - | K-ST |  |
| 408 | cmp | code_of:304 | Eq | `code_of(resolve_program, stub("nx", "#!/bin...` | 46/47 (1) | 24/24 - | K-ST |  |
| 412 | const | code_of:305 | str | `"journalctl_unusable:5"` | 46/47 (1) | 24/24 - | K-ST |  |
| 413 | cmp | code_of:306 | Eq | `code_of(resolve_program, os.path.join(td, "...` | 46/47 (1) | 24/24 - | K-ST |  |
| 415 | const | code_of:306 | str | `"journalctl_unusable:5"` | 46/47 (1) | 24/24 - | K-ST |  |
| 416 | cmp | code_of:307 | Eq | `code_of(resolve_program, good) == good` | 46/47 (1) | 24/24 - | K-ST |  |
| 417 | cmp | code_of:308 | Eq | `code_of(read_file, os.path.join(td, "absent...` | 46/47 (1) | 24/24 - | K-ST |  |
| 419 | const | code_of:308 | str | `"unreadable:2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 420 | cmp | code_of:309 | Eq | `code_of(read_file, good) == b"#!/bin/sh\npr...` | 46/47 (1) | 24/24 - | K-ST |  |
| 421 | const | code_of:309 | bytes | `b"#!/bin/sh\nprintf 'x'\n"` | 46/47 (1) | 24/24 - | K-ST |  |
| 423 | const | code_of:310 | str | `"#!/bin/sh\nenv \| cut -d= -f1 \| sort \| t...` | 46/47 (1) | 24/24 - | K-ST |  |
| 424 | const | code_of:310 | int | `0o755` | 46/47 (1) | 24/24 - | K-ST |  |
| 428 | const | code_of:313 | bytes | `b"PATH"` | 46/47 (1) | 24/24 - | K-ST |  |
| 429 | cmp | code_of:313 | In | `b"PATH" in got` | 46/47 (1) | 24/24 - | K-ST |  |
| 431 | cmp | code_of:313 | NotIn | `b"MADO_CANARY" not in got` | 46/47 (1) | 24/24 - | K-ST |  |
| 433 | cmp | code_of:313 | NotIn | `b"HOME" not in got` | 46/47 (1) | 24/24 - | K-ST |  |
| 436 | const | code_of:315 | str | `"PATH"` | 46/47 (1) | 24/24 - | K-ST |  |
| 437 | cmp | code_of:316 | Eq | `code_of(resolve_program, "good") == good` | 46/47 (1) | 24/24 - | K-ST |  |
| 438 | const | code_of:316 | str | `"good"` | 46/47 (1) | 24/24 - | K-ST |  |
| 439 | cmp | code_of:317 | Eq | `code_of(resolve_program, "absent") == "jour...` | 46/47 (1) | 24/24 - | K-ST |  |
| 441 | const | code_of:317 | str | `"journalctl_unusable:5"` | 46/47 (1) | 24/24 - | K-ST |  |
| 446 | cmp | code_of:320 | Eq | `code_of(run, ["--journal-file", jf, "--live...` | 46/47 (1) | 24/24 - | K-ST |  |
| 449 | const | code_of:320 | str | `"usage:2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 450 | cmp | code_of:321 | Eq | `code_of(run, ["--journal-file", jf, "--jour...` | 46/47 (1) | 24/24 - | K-ST |  |
| 453 | const | code_of:321 | str | `"usage:2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 454 | cmp | code_of:322 | Eq | `code_of(run, []) == "usage:2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 455 | const | code_of:322 | str | `"usage:2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 456 | cmp | code_of:323 | Eq | `code_of(run, ["--journal-file", jf, "--expe...` | 46/47 (1) | 24/24 - | K-ST |  |
| 457 | const | code_of:323 | str | `"--journal-file"` | 46/47 (1) | 24/24 - | K-ST |  |
| 458 | const | code_of:323 | str | `"--expect"` | 46/47 (1) | 24/24 - | K-ST |  |
| 460 | const | code_of:323 | str | `"bad_expect:2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 461 | cmp | code_of:324 | Eq | `code_of(run, ["--journal-file", jf])[1] == 3` | 46/47 (1) | 24/24 - | K-ST |  |
| 462 | const | code_of:324 | str | `"--journal-file"` | 46/47 (1) | 24/24 - | K-ST |  |
| 463 | const | code_of:324 | int | `1` | None/None (1) | 24/24 - | K-ST |  |
| 464 | const | code_of:324 | int | `3` | 46/47 (1) | 24/24 - | K-ST |  |
| 465 | cmp | code_of:325 | Eq | `code_of(run, ["--live", "--journalctl", goo...` | 46/47 (1) | 24/24 - | K-ST |  |
| 466 | const | code_of:325 | str | `"--live"` | 46/47 (1) | 24/24 - | K-ST |  |
| 467 | const | code_of:325 | str | `"--journalctl"` | 46/47 (1) | 24/24 - | K-ST |  |
| 468 | const | code_of:325 | int | `1` | None/None (1) | 24/24 - | K-ST |  |
| 469 | const | code_of:325 | int | `3` | 46/47 (1) | 24/24 - | K-ST |  |
| 470 | const | code_of:326 | str | `"1"` | 46/47 (1) | 24/24 - | K-ST |  |
| 471 | const | code_of:326 | str | `"wl_seat"` | 46/47 (1) | 24/24 - | K-ST |  |
| 472 | const | code_of:326 | int | `3` | 46/47 (1) | 24/24 - | K-ST |  |
| 473 | const | code_of:326 | str | `"2"` | 46/47 (1) | 24/24 - | K-ST |  |
| 474 | const | code_of:326 | str | `"wl_seat"` | 46/47 (1) | 24/24 - | K-ST |  |
| 475 | const | code_of:326 | int | `4` | 46/47 (1) | 24/24 - | K-ST |  |
| 476 | const | code_of:327 | str | `"ver_changed=wl_seat:3>4"` | 46/47 (1) | 24/24 - | K-ST |  |
| 477 | cmp | code_of:327 | In | `"ver_changed=wl_seat:3>4" in report(parse(d...` | 46/47 (1) | 24/24 - | K-ST |  |
| 478 | const | code_of:327 | bool | `True` | 46/47 (1) | 24/24 - | K-ST |  |
| 479 | const | code_of:327 | int | `0` | None/None (1) | 24/24 - | K-ST |  |
| 480 | const | code_of:327 | int | `2` | 46/47 (1) | 24/24 - | K-ST |  |
| 482 | const | code_of:329 | int | `0` | 47/47 (1) | 24/24 - | K-ST |  |
| 483 | if | code_of:329 | negate-test | `ok == n` | 47/47 (1) | 24/24 - | K-ST |  |
| 484 | cmp | code_of:329 | Eq | `ok == n` | 47/47 (1) | 24/24 - | K-ST |  |
| 488 | const | main:333 | int | `1` | None/None (2) | 24/24 - | K-ST |  |
| 489 | const | main:333 | str | `"--selftest"` | None/None (2) | 24/24 - | K-ST |  |

### Killed by fixtures only (69)

| id | kind | site | op | mutated segment | st | fx | class | note |
|---|---|---|---|---|---|---|---|---|
| 2 | const | <module>:29 | int | `1024` | 47/47 (0) | 23/24 toolarge0 | K-FX |  |
| 3 | const | <module>:29 | int | `1024` | 47/47 (0) | 23/24 toolarge0 | K-FX |  |
| 7 | const | <module>:36 | str | `"--user"` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 8 | const | <module>:36 | str | `"-u"` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 9 | const | <module>:36 | str | `"xdg-desktop-portal-hyprland"` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 10 | const | <module>:36 | str | `"--no-pager"` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 11 | const | <module>:37 | str | `"-o"` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 12 | const | <module>:37 | str | `"short-iso"` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 15 | const | <module>:41 | str | `"input-synthesis"` | 47/47 (0) | 19/24 gen0,gen1,gen3,gen7,liveenv0 | K-FX |  |
| 16 | const | <module>:41 | str | `"zwlr_virtual_pointer_manager_v1"` | 47/47 (0) | 21/24 gen1,gen7,liveenv0 | K-FX |  |
| 17 | const | <module>:42 | str | `"zwp_virtual_keyboard_manager_v1"` | 47/47 (0) | 20/24 gen1,gen3,gen7,liveenv0 | K-FX |  |
| 18 | const | <module>:43 | str | `"zwp_input_method_manager_v2"` | 47/47 (0) | 22/24 gen0,gen7 | K-FX |  |
| 19 | const | <module>:44 | str | `"input-capture"` | 47/47 (0) | 13/24 diff1,expectmiss0,gen0,gen1,gen2,gen3,gen4,gen5,gen6,gen7... | K-FX |  |
| 20 | const | <module>:44 | str | `"hyprland_input_capture_manager_v1"` | 47/47 (0) | 17/24 diff1,expectmiss0,gen2,gen4,gen5,gen6,gen7 | K-FX |  |
| 21 | const | <module>:45 | str | `"zwp_keyboard_shortcuts_inhibit_manager_v1"` | 47/47 (0) | 21/24 gen1,gen2,gen7 | K-FX |  |
| 22 | const | <module>:46 | str | `"hyprland_global_shortcuts_manager_v1"` | 47/47 (0) | 19/24 gen0,gen3,gen5,gen7,live0 | K-FX |  |
| 23 | const | <module>:47 | str | `"session-lock"` | 47/47 (0) | 20/24 gen0,gen1,gen5,gen7 | K-FX |  |
| 24 | const | <module>:47 | str | `"ext_session_lock_manager_v1"` | 47/47 (0) | 20/24 gen0,gen1,gen5,gen7 | K-FX |  |
| 25 | const | <module>:47 | str | `"hyprland_lock_notifier_v1"` | 47/47 (0) | 20/24 gen0,gen1,gen5,gen7 | K-FX |  |
| 26 | const | <module>:48 | str | `"idle"` | 47/47 (0) | 15/24 diff1,expect0,gen1,gen3,gen4,gen5,gen6,gen7,live1 | K-FX |  |
| 27 | const | <module>:48 | str | `"ext_idle_notifier_v1"` | 47/47 (0) | 18/24 diff1,expect0,gen1,gen4,gen5,gen7 | K-FX |  |
| 28 | const | <module>:48 | str | `"zwp_idle_inhibit_manager_v1"` | 47/47 (0) | 19/24 gen3,gen4,gen6,gen7,live1 | K-FX |  |
| 29 | const | <module>:49 | str | `"clipboard"` | 47/47 (0) | 15/24 diff0,diff1,expect0,gen1,gen2,gen3,gen5,gen6,gen7 | K-FX |  |
| 30 | const | <module>:49 | str | `"zwlr_data_control_manager_v1"` | 47/47 (0) | 20/24 diff0,diff1,gen6,gen7 | K-FX |  |
| 31 | const | <module>:49 | str | `"ext_data_control_manager_v1"` | 47/47 (0) | 18/24 diff0,diff1,expect0,gen3,gen5,gen7 | K-FX |  |
| 32 | const | <module>:50 | str | `"zwp_primary_selection_device_manager_v1"` | 47/47 (0) | 21/24 gen1,gen2,gen7 | K-FX |  |
| 33 | const | <module>:51 | str | `"capture"` | 47/47 (0) | 14/24 diff1,expectmiss0,gen0,gen1,gen3,gen5,gen6,gen7,live0,liv... | K-FX |  |
| 34 | const | <module>:51 | str | `"ext_image_copy_capture_manager_v1"` | 47/47 (0) | 20/24 gen0,gen5,gen7,live0 | K-FX |  |
| 35 | const | <module>:52 | str | `"ext_foreign_toplevel_image_capture_source_...` | 47/47 (0) | 21/24 gen1,gen5,gen7 | K-FX |  |
| 36 | const | <module>:53 | str | `"zwlr_screencopy_manager_v1"` | 47/47 (0) | 21/24 gen0,gen6,gen7 | K-FX |  |
| 37 | const | <module>:54 | str | `"hyprland_toplevel_export_manager_v1"` | 47/47 (0) | 17/24 diff1,expectmiss0,gen0,gen3,gen5,gen7,liveenv0 | K-FX |  |
| 38 | const | <module>:55 | str | `"toplevel-control"` | 47/47 (0) | 14/24 diff0,expect0,gen0,gen1,gen2,gen3,gen4,gen5,gen6,gen7 | K-FX |  |
| 39 | const | <module>:55 | str | `"zwlr_foreign_toplevel_manager_v1"` | 47/47 (0) | 20/24 diff0,gen2,gen3,gen7 | K-FX |  |
| 40 | const | <module>:56 | str | `"ext_foreign_toplevel_list_v1"` | 47/47 (0) | 20/24 expect0,gen0,gen5,gen7 | K-FX |  |
| 41 | const | <module>:56 | str | `"xdg_activation_v1"` | 47/47 (0) | 21/24 gen1,gen6,gen7 | K-FX |  |
| 42 | const | <module>:57 | str | `"hyprland_toplevel_mapping_manager_v1"` | 47/47 (0) | 19/24 diff0,expect0,gen4,gen5,gen7 | K-FX |  |
| 43 | const | <module>:58 | str | `"output-control"` | 47/47 (0) | 13/24 diff1,expectmiss0,gen0,gen1,gen4,gen5,gen6,gen7,live0,liv... | K-FX |  |
| 44 | const | <module>:58 | str | `"zwlr_output_manager_v1"` | 47/47 (0) | 21/24 gen0,gen6,gen7 | K-FX |  |
| 45 | const | <module>:58 | str | `"zwlr_output_power_manager_v1"` | 47/47 (0) | 17/24 diff1,expectmiss0,gen0,gen4,gen6,gen7,liveenv0 | K-FX |  |
| 46 | const | <module>:59 | str | `"zwlr_gamma_control_manager_v1"` | 47/47 (0) | 21/24 gen1,gen7,live1 | K-FX |  |
| 47 | const | <module>:60 | str | `"hyprland_ctm_control_manager_v1"` | 47/47 (0) | 21/24 gen5,gen7,live0 | K-FX |  |
| 75 | const | parse:100 | str | `"last"` | 47/47 (0) | 17/24 gen0,gen1,gen2,gen3,gen4,gen5,gen6 | K-FX |  |
| 85 | const | report:110 | int | `1` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 86 | const | report:111 | str | `"MADO_GLOBALS_SESSION: n=%d boot=%s pid=%s ...` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 98 | const | report:119 | str | `"MADO_GLOBAL: name=%s ver=%d count=%d class...` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 108 | const | report:128 | str | `"%s:%d>%d"` | 47/47 (0) | 19/24 diff0,gen1,gen6,live0,liveenv0 | K-FX |  |
| 114 | const | report:130 | str | `"MADO_GLOBALS_DIFF: from=%d to=%d added=%s ...` | 47/47 (0) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-FX |  |
| 117 | const | report:132 | str | `","` | 47/47 (0) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-FX |  |
| 123 | const | report:134 | str | `","` | 47/47 (0) | 21/24 gen1,gen6,liveenv0 | K-FX |  |
| 124 | const | report:134 | str | `"-"` | 47/47 (0) | 22/24 gen2,live1 | K-FX |  |
| 127 | const | report:138 | int | `0` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 128 | const | report:138 | int | `1` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 131 | const | report:141 | str | `"NO_SESSIONS"` | 47/47 (0) | 21/24 nosess0,nosess1,toolarge0 | K-FX |  |
| 134 | const | report:143 | str | `"MISSING_EXPECTED"` | 47/47 (0) | 19/24 expectmiss0,gen1,gen3,gen5,gen7 | K-FX |  |
| 141 | const | report:148 | str | `"-"` | 47/47 (0) | 21/24 nosess0,nosess1,toolarge0 | K-FX |  |
| 142 | bool | report:149 | Or | `",".join("%s:%d" % (c, classes[c]) for c in...` | 47/47 (0) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 143 | const | report:149 | str | `","` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 144 | const | report:149 | str | `"%s:%d"` | 47/47 (0) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-FX |  |
| 145 | const | report:150 | str | `"-"` | 47/47 (0) | 21/24 nosess0,nosess1,toolarge0 | K-FX |  |
| 147 | const | report:150 | str | `","` | 47/47 (0) | 23/24 expectmiss0 | K-FX |  |
| 148 | const | report:150 | str | `"-"` | 47/47 (0) | 12/24 diff0,diff1,expect0,gen0,gen2,gen4,gen6,live0,live1,livee... | K-FX |  |
| 154 | const | resolve_program:156 | str | `":"` | 47/47 (0) | 23/24 live1 | K-FX |  |
| 173 | const | read_live:182 | bool | `False` | 47/47 (0) | 20/24 live0,live1,liveenv0,livelarge0 | K-FX |  |
| 190 | const | read_file:199 | str | `"too_large"` | 47/47 (0) | 23/24 toolarge0 | K-FX |  |
| 193 | const | run:205 | bool | `False` | 47/47 (0) | 23/24 usage0 | K-FX |  |
| 202 | const | <lambda>:211 | str | `"usage"` | 47/47 (0) | 23/24 usage0 | K-FX |  |
| 215 | const | <lambda>:224 | str | `"journalctl"` | 47/47 (0) | 23/24 live1 | K-FX |  |
| 490 | const | main:336 | int | `1` | 47/47 (0) | 1/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-FX |  |
| 491 | const | main:338 | str | `"MADO_GLOBALS: SETUP %s"` | 47/47 (0) | 17/24 badexpect0,livefail0,livelarge0,livewritable0,toolarge0,u... | K-FX |  |

### Killed by both (128)

| id | kind | site | op | mutated segment | st | fx | class | note |
|---|---|---|---|---|---|---|---|---|
| 1 | const | <module>:29 | int | `8` | 46/47 (1) | 22/24 livelarge0,toolarge0 | K-ST |  |
| 4 | const | <module>:31 | str | `r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\...` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 5 | const | <module>:34 | str | `r"-- Boot ([0-9a-f]{32}) --"` | 42/47 (1) | 19/24 gen1,gen3,gen5,gen6,gen7 | K-ST |  |
| 6 | const | <module>:35 | str | `r"[A-Za-z0-9_]{1,128}"` | 46/47 (1) | 17/24 expect0,expectmiss0,gen1,gen3,gen5,gen7,nosess0 | K-ST |  |
| 13 | const | <module>:40 | str | `"focus-grab"` | 46/47 (1) | 21/24 gen5,gen7,live1 | K-ST |  |
| 14 | const | <module>:40 | str | `"hyprland_focus_grab_manager_v1"` | 46/47 (1) | 21/24 gen5,gen7,live1 | K-ST |  |
| 48 | const | <module>:61 | str | `"sandbox"` | 46/47 (1) | 18/24 gen0,gen1,gen2,gen3,gen4,gen7 | K-ST |  |
| 49 | const | <module>:61 | str | `"wp_security_context_manager_v1"` | 46/47 (1) | 18/24 gen0,gen1,gen2,gen3,gen4,gen7 | K-ST |  |
| 50 | const | __init__:67 | int | `2` | 42/47 (1) | 20/24 badexpect0,toolarge0,unreadable0,usage0 | K-ST |  |
| 51 | const | classify:74 | str | `"other"` | 46/47 (1) | 10/24 diff0,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,gen5,g... | K-ST |  |
| 53 | const | parse:79 | str | `"utf-8"` | None/None (1) | 7/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 54 | const | parse:79 | str | `"replace"` | None/None (1) | 22/24 gen3,nosess0 | K-ST |  |
| 55 | const | parse:81 | str | `"-"` | 45/47 (1) | 13/24 diff0,diff1,expect0,expectmiss0,gen0,gen2,gen4,gen7,live0... | K-ST |  |
| 57 | const | parse:84 | str | `"\n"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 58 | if | parse:86 | negate-test | `m` | None/None (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 59 | const | parse:87 | int | `1` | None/None (1) | 19/24 gen1,gen3,gen5,gen6,gen7 | K-ST |  |
| 60 | const | parse:88 | bool | `True` | 43/47 (1) | 22/24 gen1,gen6 | K-ST |  |
| 61 | if | parse:91 | negate-test | `not m` | None/None (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 62 | if | parse:95 | negate-test | `cur is None or boot_changed or cur["pid"] !...` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 63 | bool | parse:95 | Or | `cur is None or boot_changed or cur["pid"] !...` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 64 | cmp | parse:95 | Is | `cur is None` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 65 | cmp | parse:95 | NotEq | `cur["pid"] != pid` | 36/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 66 | const | parse:95 | str | `"pid"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 67 | const | parse:96 | str | `"boot"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 68 | const | parse:96 | str | `"pid"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 69 | const | parse:96 | str | `"first"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 71 | const | parse:97 | str | `"adverts"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 72 | const | parse:97 | int | `0` | 43/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 73 | const | parse:97 | str | `"names"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 74 | const | parse:99 | bool | `False` | 37/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 76 | const | parse:101 | str | `"adverts"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 77 | const | parse:101 | int | `1` | 43/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 78 | const | parse:102 | str | `"names"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 79 | const | parse:102 | int | `0` | 46/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 81 | const | parse:103 | int | `0` | 46/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 82 | const | parse:103 | int | `1` | 46/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 83 | const | parse:104 | int | `1` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 84 | const | parse:104 | int | `1` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 87 | const | report:112 | str | `"boot"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 88 | const | report:112 | str | `"pid"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 89 | const | report:113 | str | `"first"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 90 | const | report:113 | str | `"last"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 91 | const | report:114 | str | `"names"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 92 | const | report:114 | str | `"adverts"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 93 | if | report:115 | negate-test | `sessions` | None/None (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 94 | const | report:115 | int | `1` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 95 | if | report:116 | negate-test | `latest` | None/None (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 96 | const | report:117 | str | `"names"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 97 | const | report:118 | str | `"names"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 99 | if | report:121 | negate-test | `diff` | 43/47 (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 100 | if | report:122 | negate-test | `len(sessions) < 2` | None/None (1) | 15/24 diff0,diff1,gen1,gen2,gen6,live0,live1,liveenv0,nosess1 | K-ST |  |
| 101 | cmp | report:122 | Lt | `len(sessions) < 2` | None/None (1) | 15/24 diff0,diff1,gen1,gen2,gen6,live0,live1,liveenv0,nosess1 | K-ST |  |
| 102 | const | report:122 | int | `2` | 44/47 (1) | 20/24 gen6,live0,live1,liveenv0 | K-ST |  |
| 103 | const | report:123 | str | `"MADO_GLOBALS_DIFF: sessions=%d none"` | 46/47 (1) | 22/24 diff1,nosess1 | K-ST |  |
| 104 | const | report:125 | int | `2` | None/None (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 105 | const | report:125 | str | `"names"` | None/None (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 106 | const | report:125 | int | `1` | 44/47 (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 107 | const | report:125 | str | `"names"` | None/None (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 109 | const | report:128 | int | `1` | None/None (1) | 19/24 diff0,gen1,gen6,live0,liveenv0 | K-ST |  |
| 110 | const | report:128 | int | `1` | None/None (1) | 19/24 diff0,gen1,gen6,live0,liveenv0 | K-ST |  |
| 111 | cmp | report:129 | NotEq | `a[n][1] != b[n][1]` | 46/47 (1) | 19/24 diff0,gen1,gen6,live0,liveenv0 | K-ST |  |
| 112 | const | report:129 | int | `1` | None/None (1) | 19/24 diff0,gen1,gen6,live0,liveenv0 | K-ST |  |
| 113 | const | report:129 | int | `1` | None/None (1) | 19/24 diff0,gen1,gen6,live0,liveenv0 | K-ST |  |
| 115 | const | report:131 | int | `1` | 46/47 (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 116 | bool | report:132 | Or | `",".join(added) or "-"` | 46/47 (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 119 | bool | report:133 | Or | `",".join(removed) or "-"` | 46/47 (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 120 | const | report:133 | str | `","` | 46/47 (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 122 | bool | report:134 | Or | `",".join(changed) or "-"` | 46/47 (1) | 17/24 diff0,gen1,gen2,gen6,live0,live1,liveenv0 | K-ST |  |
| 125 | if | report:135 | negate-test | `latest` | None/None (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 126 | const | report:135 | str | `"names"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 129 | cmp | report:139 | NotIn | `e not in names` | 45/47 (1) | 17/24 expect0,expectmiss0,gen1,gen3,gen5,gen7,nosess0 | K-ST |  |
| 130 | if | report:140 | negate-test | `not sessions` | 42/47 (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 132 | const | report:141 | int | `3` | 44/47 (1) | 21/24 nosess0,nosess1,toolarge0 | K-ST |  |
| 133 | if | report:142 | negate-test | `missing` | 45/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 135 | const | report:143 | int | `1` | 46/47 (1) | 19/24 expectmiss0,gen1,gen3,gen5,gen7 | K-ST |  |
| 136 | const | report:145 | str | `"OK"` | 46/47 (1) | 14/24 diff0,diff1,expect0,gen0,gen2,gen4,gen6,live0,live1,liveenv0 | K-ST |  |
| 137 | const | report:145 | int | `0` | 46/47 (1) | 14/24 diff0,diff1,expect0,gen0,gen2,gen4,gen6,live0,live1,liveenv0 | K-ST |  |
| 138 | const | report:146 | str | `"MADO_GLOBALS: sessions=%d latest_pid=%s in...` | 46/47 (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 139 | if | report:148 | negate-test | `latest` | None/None (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 140 | const | report:148 | str | `"pid"` | None/None (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 146 | bool | report:150 | Or | `",".join(missing) or "-"` | 45/47 (1) | 6/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 149 | if | resolve_program:155 | negate-test | `"/" not in prog` | 46/47 (1) | 23/24 live1 | K-ST |  |
| 151 | cmp | resolve_program:155 | NotIn | `"/" not in prog` | 46/47 (1) | 23/24 live1 | K-ST |  |
| 152 | const | resolve_program:156 | str | `"PATH"` | 46/47 (1) | 23/24 live1 | K-ST |  |
| 155 | bool | resolve_program:157 | Or | `d or "."` | 46/47 (1) | 23/24 live1 | K-ST |  |
| 157 | if | resolve_program:158 | negate-test | `os.path.isfile(cand) and os.access(cand, os...` | 46/47 (1) | 23/24 live1 | K-ST |  |
| 163 | if | resolve_program:168 | negate-test | `not stat.S_ISREG(st.st_mode) or not os.acce...` | 38/47 (1) | 18/24 live0,live1,liveenv0,livefail0,livelarge0,livewritable0 | K-ST |  |
| 164 | bool | resolve_program:168 | Or | `not stat.S_ISREG(st.st_mode) or not os.acce...` | 45/47 (1) | 23/24 livewritable0 | K-ST |  |
| 165 | const | resolve_program:170 | str | `"journalctl_unusable"` | 45/47 (1) | 23/24 livewritable0 | K-ST |  |
| 166 | const | resolve_program:170 | int | `5` | 45/47 (1) | 23/24 livewritable0 | K-ST |  |
| 171 | cmp | read_live:178 | In | `k in os.environ` | None/None (1) | 19/24 live0,live1,liveenv0,livefail0,livelarge0 | K-ST |  |
| 176 | if | read_live:185 | negate-test | `p.returncode != 0` | 42/47 (1) | 19/24 live0,live1,liveenv0,livefail0,livelarge0 | K-ST |  |
| 177 | cmp | read_live:185 | NotEq | `p.returncode != 0` | 42/47 (1) | 19/24 live0,live1,liveenv0,livefail0,livelarge0 | K-ST |  |
| 178 | const | read_live:185 | int | `0` | 42/47 (1) | 19/24 live0,live1,liveenv0,livefail0,livelarge0 | K-ST |  |
| 179 | const | read_live:186 | str | `"journalctl_failed"` | 46/47 (1) | 23/24 livefail0 | K-ST |  |
| 180 | const | read_live:186 | int | `5` | 46/47 (1) | 23/24 livefail0 | K-ST |  |
| 181 | if | read_live:187 | negate-test | `len(p.stdout) > MAX_BYTES` | 43/47 (1) | 20/24 live0,live1,liveenv0,livelarge0 | K-ST |  |
| 182 | cmp | read_live:187 | Gt | `len(p.stdout) > MAX_BYTES` | 43/47 (1) | 20/24 live0,live1,liveenv0,livelarge0 | K-ST |  |
| 183 | const | read_live:188 | str | `"journalctl_too_large"` | 46/47 (1) | 23/24 livelarge0 | K-ST |  |
| 184 | const | read_live:188 | int | `5` | 46/47 (1) | 23/24 livelarge0 | K-ST |  |
| 185 | const | read_file:194 | str | `"rb"` | None/None (1) | 8/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 187 | const | read_file:197 | str | `"unreadable"` | 46/47 (1) | 23/24 unreadable0 | K-ST |  |
| 188 | if | read_file:198 | negate-test | `len(data) > MAX_BYTES` | 45/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 189 | cmp | read_file:198 | Gt | `len(data) > MAX_BYTES` | 45/47 (1) | 9/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 194 | const | run:206 | str | `"--journal-file"` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 195 | const | run:207 | str | `"--live"` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 196 | const | run:207 | str | `"store_true"` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 197 | const | run:208 | str | `"--journalctl"` | None/None (1) | 1/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 198 | const | run:209 | str | `"--expect"` | None/None (1) | 1/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 199 | const | run:209 | str | `"append"` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 200 | const | run:210 | str | `"--diff"` | None/None (1) | 3/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 201 | const | run:210 | str | `"store_true"` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 204 | if | <lambda>:216 | negate-test | `bool(args.journal_file) == bool(args.live)` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 205 | cmp | <lambda>:216 | Eq | `bool(args.journal_file) == bool(args.live)` | None/None (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 206 | const | <lambda>:217 | str | `"usage"` | 45/47 (1) | 23/24 usage0 | K-ST |  |
| 207 | if | <lambda>:218 | negate-test | `args.journalctl is not None and not args.live` | 43/47 (1) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 208 | bool | <lambda>:218 | And | `args.journalctl is not None and not args.live` | 44/47 (1) | 2/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 209 | cmp | <lambda>:218 | IsNot | `args.journalctl is not None` | 44/47 (1) | 6/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 210 | const | <lambda>:219 | str | `"usage"` | 46/47 (1) | 23/24 usage0 | K-ST |  |
| 211 | if | <lambda>:221 | negate-test | `not NAME.fullmatch(e)` | 46/47 (1) | 16/24 badexpect0,expect0,expectmiss0,gen1,gen3,gen5,gen7,nosess0 | K-ST |  |
| 212 | const | <lambda>:222 | str | `"bad_expect"` | 46/47 (1) | 23/24 badexpect0 | K-ST |  |
| 213 | if | <lambda>:223 | negate-test | `args.live` | None/None (1) | 2/24 diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2,gen3,gen4,... | K-ST |  |
| 214 | bool | <lambda>:224 | Or | `args.journalctl or "journalctl"` | 46/47 (1) | 23/24 live1 | K-ST |  |
| 486 | if | main:333 | negate-test | `sys.argv[1:] == ["--selftest"]` | None/None (2) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 487 | cmp | main:333 | Eq | `sys.argv[1:] == ["--selftest"]` | None/None (2) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 492 | if | main:345 | negate-test | `__name__ == "__main__"` | None/None (0) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 493 | cmp | main:345 | Eq | `__name__ == "__main__"` | None/None (0) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |
| 494 | const | main:345 | str | `"__main__"` | None/None (0) | 0/24 badexpect0,diff0,diff1,expect0,expectmiss0,gen0,gen1,gen2... | K-ST |  |

## Integrity

- Reference tool sha256 before sweep: `61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0`
  (frozen file opened read-only; every mutant was a fresh `/tmp` copy).
- Counter file: `quality/counters/c1-r41-globals.py`, sha256 at run time `e43dc235925635ffc2008a3af4872f33b9be6a461a5cea77a98e008ae2a3f32a`.
- Post-sweep re-hash of both files: see the seat Report (must match).
- Scratch `/tmp/mut41sf.zzOFli` (mutants, driver, raw `results.jsonl`) removed after the run.
- No lane file written by this seat except the seat Report and this matrix.

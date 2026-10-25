# Lessons — mado, round 40

Round intent: registration `.ufo/waves/round-40/registration.md` (freeze `5e7e88525cc539563de7746361b2650802e81809`)
re-registered as `registration-v2.md` (freeze `8122293930f42ea2011e7c2b0b80a297e2ce6cdd`, before any data commit).
C1 lands `tools/mado-options.py --live` (operability, capability acquisition); C2 admits
`corpus/knowledge/hyprctl-getoption-native-forms-r40.md` (coverage, sourced). Assimilation (bar-producers theme)
admits `corpus/knowledge/host-bar-producer-census-r40.md`. One v2 wave `w1` of 64 seats; no residual call; round total 64.

## Gate

GATE S158 receipt=.ufo/waves/round-40/fetch/hyprctl-efb5099.bin sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote="R"({{"option": "{}", "vec2": [{},{}], "set": {} }})""
GATE S162 receipt=.ufo/waves/round-40/fetch/config-manager-efb5099.bin sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians"
GATE S173 receipt=.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin sha256=fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e quote="a = std::round(std::stof(trim(rolling.substr(0, rolling.find(',')))) * 255.f);"
GATE S180 receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);"
GATE S181 receipt=.ufo/waves/round-40/fetch/parser-utils-efb5099.bin sha256=86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0 quote="std::floor(*a * 255.F)"
GATE S215 receipt=.ufo/waves/round-40/fetch/config-values-efb5099.bin sha256=a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754 quote=""shadow's rendering offset.", Config::VEC2{},"
GATE S278 receipt=.ufo/waves/round-40/fetch/wiki-0.54.0-using-hyprctl.html sha256=3f02dc8e4634111d1938d005c11cccd98a61b43ebddbd011b3ad674ce773cc29 quote="getoption [option] - gets the config option status (values)"
GATE S279 receipt=.ufo/waves/round-40/fetch/census-receipt.txt sha256=93e6ce909514775145f9fa66f3d50c7a0885eb19f507d7d8b98e152baec312e5 quote="census: 70 declared keys queried once each with hyprctl getoption -j"
GATE S280 receipt=.ufo/waves/round-40/fetch/omarchy-v3.8.4-screen-recording.bin sha256=28491cd3fdaaea78143432d6e2d5b609f06f90e420874d8bdd83a25a199bc63c quote="if pgrep -f "^gpu-screen-recorder" >/dev/null; then"
GATE S281 receipt=.ufo/waves/round-40/fetch/omarchy-v3.8.4-notification-silencing.bin sha256=312900d1a9ca772e944e626d86cb54af6dec4dd5619510ecb262562da9d6de69 quote="if makoctl mode | grep -q 'do-not-disturb'; then"
GATE S282 receipt=.ufo/waves/round-40/fetch/host-k2-reads.txt sha256=91a14ac8ce4cbccabe0b7492e5da4e67fba9a1369e792748ade9697f1f71c4d4 quote=""exec": "~/.local/bin/gkeep waybar","

Every source above was opened by the L1 on 2026-10-25 and its bytes committed under `.ufo/waves/round-40/fetch/`
(`curl -sSL`, HTTP 200 each; Hyprland files at `efb50993780079460b0cbed1363e2166a2de1d9f`, hyprlang at `v0.6.8`,
the wiki page `https://wiki.hypr.land/0.54.0/Configuring/Using-hyprctl/` re-fetched byte-identical to the seat copy;
omarchy files at tag `v3.8.4`). S279 and S282 are own-work: the census receipt names the tool's sha256 at the data
commit (`make-census.py` writes it), the host-reads receipt was captured read-only by seat `ExecK2HostReads`.
Quotes are located in tag-stripped, entity-decoded text; two lines the wave found unusable as quotes are kept out of
the Gate on purpose: `std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));` and the `parseColor` alpha line
(`sc<uint64_t>(std::floor(*a * 255.F)) << 24`), because the counter's `norm()` deletes `<...>` spans and the span
opened at `sc<int>` / `<<` closes far away - measured, `norm(q) in norm(blob)` false (seats `ScrFormsEntryA`,
`RevModelVsSource`); the entries cite those lines by number instead.

Held rows re-opened (cells 1-10 unchanged; only `used-by` grew): S158, S162, S173, S180, S181, S215 each re-fetched,
sha256 equal to the held anchor or the round-39 receipt (`S162` `9db68cf4...`, `S173` `fa1b6898...`, `S180` `95733223...`,
`S181` `86f21b76...`, `S158` `798b7c6c...`). `used-by` old -> new: each gains `corpus/knowledge/hyprctl-getoption-native-forms-r40.md`
at the end of its list; S215 `corpus/knowledge/event-queue-observability-r37.md` -> `..., corpus/knowledge/hyprctl-getoption-native-forms-r40.md`.
New rows (all `mined`, opened 2026-10-25): S278 (wiki, recheck on-release), S279 (own-work, on-change), S280 and S281
(omarchy scripts, on-release), S282 (own-work, 30d). One census W04 warning set is unchanged (S030, S042, S045, S097,
S119, S120, S121) and so is W01 S277; no new warning.

### Assimilation ledger (theme: the host's bar producers; package `merge/mado/`, read-only)

| candidate | scope (PROVINCE) | held (`waybar-walker-semantics.md`) | quality bar | verdict |
|---|---|---|---|---|
| K1 `host-bar-producers-r28.md` | in, as chain evidence (`PROVINCE.md:3,11`); gkeep package internals out (`config-drift-r12.md:109`) | the module rows, scripts and 5114 B upstream size are held (`:135-149`; `ScoutK1K2Held`) | its "five JSON producers" is the stock upstream set, not the host's (criteria 10/14/15) | **refused**, flip: only the unheld facts return, as the successor below |
| K2 `host-producer-outputs-r29.md` | in, narrowly | four of seven OBS blocks restate held rows; its `custom/voxtype` UNK is stale against `:137` | D1 five-vs-seven producers; D2 "three render empty" contradicts its own third member and inverts the idle chip's reason (hypridle runs); D3 quotes a rotating `updated_at` (now `2026-10-25T20:47:13Z`) of 2 words; D4 cites ids the lane never held; D5 names symlinks as files and a drifted size (134777 B vs 114246 B) (`ScrAssimK2`) | **refused as written**; flip: none for its own text |
| successor `host-bar-producer-census-r40.md` | in (shims and declared contract only) | adds what is unheld: the 7-of-8 census with a denominator, the host/upstream byte identity of two indicator scripts, the two host-local producers' resolved shims, the idle chip's reversed state | every quote located in committed bytes; no volatile value quoted; state lines dated | **admitted**, rows S280-S282 |

The staged register was not appended: ids S237-S241 are free in the lane registry but their rows are the package's
numbering with no lane receipt; the successor's rows continue the lane's ids by document (S280-S282) - the staged
id -> adopted id map is `S237 -> S280`, `S238 -> S281`, `S239/S240 -> S282` (one own-work row for both shims).
Id-collision guard (section 10 command, `w1/ExecAssimIdGuard/guard.md`): registry 214 ids, staged 147, collisions 22
(S203-S221, S253, S258, S277); the guard was proved on a scratch registry with an indented `  | S002 |` row (the
0-3-space pattern prints S002, the column-zero pattern prints nothing). Quarantine slice for the lane: 13 rows
(`assimilation/quarantine-slice`, verdicts `w1/ExecQuarantineSlice/verdicts.md`): present and adoptable S189, S195, S201,
S222, S223, S225, S235, S228 (with the corrected glyph quote), S205 (under JSON normalization); S199 and S200 present in
the lane's reader-proxy copy while the live URL answers HTTP 521; **S224 unverifiable, not fabrication** (a volatile
timestamp rotated); **S209 unverifiable - no quote exists** in the package. Corrects the round-39 lesson: its
"refused (fabrication class)" label for S224 over-labelled; the round-39 verifier spot-check D2 is right - a rotated
volatile value is `unverifiable`.

The ledger's admit (the successor, S280-S282) and reject (K2 as written; K1 as held) are the pair the round's
non-author closure spot-checks (LEARNING.md); no second wave ran (budget); the closure re-opens the sources first.

### Round-39 closure items

D1 (predicate variance): the criterion-64 command was run at the v2 freeze - `receipts/freeze-counter-check-v2.txt`,
no `MISSING` line (the v1 freeze also passed; the failure this round was not a missing path). D2: corrected above.
D3 (dead seats): every w1 seat wrote a report; 63 of 64 report files exist, the 64th seat (`ConnCrossClaim`) wrote its
report to a path of another round and lane (`.ufo/waves/round-49/w1/ConnCrossClaim.md`, not present in this repo) and its
returned text is kept in `w1-results.json` - recorded as M40-6.

## Mistakes

**M40-1 - the v1 generator under-sampled the spellings the mutants get wrong.** Class: a mutation survives because
the fixtures never guarantee the class it breaks. Evidence: `MutC1Controls` (`.ufo/waves/round-40/w1/MutC1Controls.md`)
- 22 further single-defect mutants of the v1 reference against the v1 counter: 8 killed, **14 survived 13/13** (alpha
tie, weight case, fractional angle, float tolerance, padded replies, the sentinel phrase as a str value, probe
dedupe, probe failure, `live` type, row order, `--hyprctl` default, a gap swap that depended on the seed);
`CritGeneratorCoverage` - 16 one-defect mutations wrong only on a real spelling class the generator never emits all
scored 13/13. Captured-by: none (the freeze's 18 controls were all honest implementations with one defect each, drawn
from classes the author thought of). Fix: v2's generator draws spelling and alpha from a lattice on the tree index (every
class appears across the eight trees whatever the nonce draws) and the control list carries one mutant per class
(57 controls, `receipts/ctl-c1-v2.txt`). Shown able to fail: the v1 counter scored the 14 survivors at 13/13
(`w1/MutC1Controls/mutants/`), the v2 harness scores each of its mutants below 19/19 (57/57 correct). Two mutants the
first v2 run left alive were repaired the same way: stdin inheritance (the judge's own stdin was /dev/null, so the
check could not see it -> the counter now hands the tool an open pipe) and the reply cap (the mutant kept a post-check
-> the control now removes both).

**M40-2 - the v1 counter let the tool read the judge.** Class: an unsandboxed, public-seed counter that trusts the
tool's output - a do-nothing control can reach the target. Evidence: `CritC1Cheat` (`w1/CritC1Cheat.md`,
`cheat-c-leak-min.py`): a 204-line tool with no conversion `exec`s the counter's own model, located through
`/proc/<ppid>/cmdline`, and scored `fixtures=13/13 TARGET_MET` at the freeze commit and the tip; `cheat-d-forge.py`
forged the stub's call log and never ran the compositor; `RevC1Counter` S1/S2/S3/S5 added a REV-seed replay, an echo
selftest, a fabricated `live` payload and unchecked failure legs - all `TARGET_MET`. The registration's do-nothing
control (BASE `0/13`) and reachability control (reference `13/13`) had only tested honest tools. Captured-by:
`PROTOCOL` 9 (build the cheapest control that skips the claimed work) *as written* - but the control the author built
skipped the work *honestly*, not adversarially. Fix: the counter runs every tool and selftest in a bubblewrap sandbox, holds
the fake compositor and its log in the judge process, mixes a per-run nonce into the seeds, and binds the selftest to
behaviour (6 flips of the tool's new comparison sites, >= 4 must fail the selftest); the seven w1 cheats are committed
as controls. Shown able to fail: `receipts/ctl-c1-v2.txt` - the seven cheats score 0/19 under v2 against 13/13 under
v1 (`w1/CritC1Cheat/cheat-c-*.score.txt`). Limit (declared): a tool that *contains* the reference tables passes.

**M40-3 - a model written for one parser was applied to its sibling.** Class: wrong reference model shared by tool and
counter. Evidence: `CritGeneratorCoverage` and `RevModelVsSource`: gradient colour tokens are parsed by Hyprland's
`ParserUtils::parseColor` (`floor(a*255.F)`, uint8 channels), not by hyprlang's `configStringToInt` (`std::round`); the
model also used Python's banker's `round` (alpha 0.3 -> 76, host 77) and read a 3-value CSS gap wrongly in its first
draft (2 of 8 v1 fixtures failed on it); "the four native forms" was stated as a universal while 6 of 353 options answer
`vec2` (`ExecAllOptionsForms`, `CritClaimWording` F1). Captured-by: none - the model was scored only against the
generator written from it (`ExecOracleHlInt` ran the real library: 1401/1401 on the generator's space, 164/188 on a
wider corpus). Fix: two models, a source line per rule, the all-options capture committed and read by clause k2,
`vec2` handled. Shown able to fail: controls `M44` (gradient alpha rounded) and `M45` (gradient tokens through the int
parser) and `M17`/`M18` (alpha truncated / banker's) each score below 19/19.

**M40-4 - "read-only" was asserted for a verb whose argument comes from a config file.** Class: a safety property
claimed over inputs the claim did not enumerate. Evidence: `SentLiveVerbs` (critical): a config-declared key
`x/--batch` makes the compositor's client turn one `getoption -j` into a `[[BATCH]]` request, which runs `dispatch exec`
(source `HyprCtl.cpp:1309-1332`, not sent to the live compositor); `RevToolSafety` F1: a key `-j` or `--batch` killed the
run with a misattributed exit 5. The v1 tool guarded only `--probe`. Captured-by: none (registration: "the only compositor
verb run is read-only `getoption -j`" - true of the command line, not of the key). Fix: every key must match
`[A-Za-z0-9_.][A-Za-z0-9_.:-]{0,127}` before any request; program resolution, a bounded environment, stdin /dev/null, a
64 KiB reply cap and strict typing; fixtures `hostilekey0`, `writable0`, `limits0`. Shown able to fail: `M35`
(declared-key allowlist dropped) and `M41` (writable program accepted) score below 19/19; the v1 counter scored a tool
without the allowlist at 13/13.

**M40-5 - the L1 re-froze after seats had seen v1 scores.** Class: a predicate repaired after scoring. Evidence:
`ExecToolLive` and `ExecToolIndep` scored a candidate `13/13` under v1 before the wave ended; v2 followed the same wave's
findings. Captured-by: PROTOCOL claim-sizing ("a rule changed after any seat has scored is not the claim's rule").
Fix: none that removes the fact - v2 is strictly stronger, was committed with its controls before any data commit
(freeze `8122293`), and the report states both scores at the data tip; the operator rules which predicate binds. Not
shown able to fail: this is a disclosure, not a gate.

**M40-6 - a connector seat reported to the wrong round.** Class: seat path discipline. Evidence: `w1-results.json`
`ConnCrossClaim` returned `report: .ufo/waves/round-49/w1/ConnCrossClaim.md`; the file does not exist in this lane or at the
fleet root (`find` over the fleet root named only other rounds' files). Captured-by: the wave context's "`Report:` trailer
paths are relative to the lane" rule - which the seat followed for a trailer it should not have had. Fix: none; the seat
counts as a dead report, its returned text is kept, and no claim rests on it.

### QUALITY.md criteria added

Criteria 65-68 (below) cite M40-1, M40-2, M40-4 and M40-5.

## considerthese

`considerthese/2026-10-25.md` proposal 2 ("Count dead attempts and dirty closures from the watchdog digests", restating
`2026-10-24.md:47`) is mined as a table (seats `ExecWatchdogTable`, `ScrConsidertheseLesson`). The attempts half is
derivable from the digest (`launch` lines, never the `attempt=` field, which is not monotonic: round 28 carries
`attempt=1` seven times); the dirty half is **not** in the digest - a null channel, not a zero: the known round-31
report-uncommitted event produced no watchdog line (`events.log:1381`), and `inline.sh:126` measures worktree dirt at
closure and discards it - an operator-owned driver edit, recorded as an observation, not a lane claim.

| round | launches | dead | closure | receipt |
|---|---|---|---|---|
| 32 | 1 | 0 | dirty (5 paths, round-30 leftovers) | `round-32-verifier-spotcheck.md:18` |
| 33 | 1 | 0 | dirty (19 untracked dirs) | `round-33-verifier-spotcheck.md:19` |
| 34 | 1 | 0 | clean | `round-34-verifier-spotcheck.md:41-43` |
| 35 | 2 | 1 | dirty (tracked=8 untracked=2) | `round-35-verifier-spotcheck.md:45-48` |
| 36 | 1 | 0 | dirty (1 untracked seat report) | `round-36-verifier-spotcheck.md:21` |
| 37 | 2 | 1 | clean | `round-37-verifier-spotcheck.md:20` |
| 38 | 1 | 0 | dirty (3 modified seat reports) | `round-38-verifier-spotcheck.md:17` |
| 39 | 1 | 0 | clean | `round-39-verifier-spotcheck.md:16-17` |

Rounds 32-37: 2 of 6 dead, 4 of 6 dirty - the proposal's numbers reproduce exactly, from two sources. Rounds 32-39: 2 of 8
dead, 5 of 8 dirty. The lane's own closure receipts, not the watchdog, are the dirty column's source. No QUALITY criterion
is added for it (no mistake of this round backs one); the proposals 1 and 3-6 of the same file stay open.

Round-39's planned item 1 ("take one live `hyprctl getoption` dump and merge it") is C1.

## Census and measurements at the data commit `91f0a2b`

Census before (`receipts/census-before.txt`): `mado ok`, W04 x7 + W01 S277, exit 0. After (`receipts/census-after.txt`): same warnings, `mado ok`, exit 0. Registry rows 214 -> 219 (S278-S282; tier A +5). `PRED-C1-r40-v2` `fixtures=19/19 TARGET_MET` (nonce `239e2809b1850614`), `PRED-C2-r40-v2` `admitted=1/1 TARGET_MET`; the superseded v1 counters at the same rev: C2 v1 `1/1 TARGET_MET`, C1 v1 `fixtures=13/13` with `TARGET_MISSED` because its clause g allowlist (frozen) refuses the `struct` and `threading` imports the security repairs added. Gates: `MADO_SELFTEST 460/460`, `MADO_OPTIONS_SELFTEST 211/211`, index `58/58`, index rows `errors=0`.

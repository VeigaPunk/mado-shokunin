# ConnW1Ledger — w1 findings mapped to the round-47 v1 freeze

Round 47 wave w2 (FALSIFY), seat ConnW1Ledger. Read: all 41 w1 root reports,
`registration.md`, the frozen counters (`quality/counters/c1-r47-terminal.py`,
`c2-r47-terminal-entry.py`), `receipts/ctl-c1.txt`, `receipts/ctl-c2/`, the frozen
fixtures (`c1-r47-fixtures.json`, sha256 `4836cc1d…`), `ctl/build-fixtures.py`,
`claims.md`. Verified by run: pre-data heads and two mutant counts (below).

## 0. Pre-data state (measured today at lane HEAD `9bddd6ac`)

- C1: `PRED-C1-r47 clause=a tool=absent … fixtures=0/190 explained=0/190 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` exit 1.
- C2: `PRED-C2-r47 … clause=a entry_absent … admitted=0/1 verdict=TARGET_MISSED` exit 1.
- Freeze commit `d7527d6` contains registration, both counters, 190 fixtures, fetch pins
  (`fetch/xdg-terminal-exec`, `fetch/README.md`, `fetch/xdg-terminals.list`), L1 reference,
  ctl runners, base receipts. Counter sha `2b9c2d0e…` and reference sha `762d042c…` are
  byte-identical at `d7527d6` and HEAD (sig verified).

## 1. Ledger: finding (seat, id) → disposition

Disposition keys: **ADDR** = addressed by registration / frozen counter / control / declared residual; **OPEN** = not addressed; **ROUTED** = drafted, L1 landing pending at data time; **META** = not claim-bearing.

| seat | finding | disposition | where |
|---|---|---|---|
| ExecRefA | F1–F3, F5–F12, F14 model corrections (tokenizer non-fatal, `-type f` first-operand, IFS leak, residue, final-line, prefix keys, Hidden-literal, Type/NoDisplay unread, ID precedence, `/./` fold, delimiter strip, glob validation) | ADDR | folded into L1 reference & fixture classes; ctl-c1 V-*/REF confirm |
| ExecRefA | F4 empty-argv spin | ADDR | declared out-of-contract residual + incident rule |
| ExecRefA | F13 `-h`/`--help` | ADDR | declared out-of-contract residual |
| ExecCounterC1 | forged-cache run dropped → cache-reading tool undetectable | **OPEN (O3)** | frozen counter f/x never present a cache; no poisoned-cache control |
| ExecCounterC1 | script-side timeout becomes verdict (124) not setup error | **OPEN (O4)** | Box.run maps TimeoutExpired→(124,"") |
| ExecCounterC1 | no oracle-determinism guard on g | open/low | accepted; oracle+tool trees materialized identically in same order |
| ExecCounterC1 | g includes `--test`/`--print-content` vs narrow draft | ADDR | L1 docstring contract now includes both; ARGVS cover |
| ExecControls | F1 clause r separation for byte-perfect cheats | ADDR | frozen r traces every tool run; DELEGATE-SH/SUBPROC-EMBED/CTYPES-EXECVE/EMBED-EXECV/SOCKET-AND-REF all MISSED (ctl-c1) |
| ExecControls | F2 clause s free | ADDR | s is shape-only; f/g carry the load |
| ExecControls | F3 generated near-misses incl. nested dirs | ADDR | generator subdirectory ids; fixture class subdirectory-ids |
| ExecControls | F4 cold cache / repo invisibility | ADDR (hygiene) + **OPEN (O3)** | fresh roots per case; but no CACHE-READ/forged-cache control |
| ExecControls | F5 over-validation (wrong Type) | ADDR-in-effect | fixtures select non-Application Type entries; no dedicated control |
| ExecControls | F6 counter edit mid-run | ADDR | freeze pins bytes; identity verified |
| ExecControls | F7 fixture-vs-counter disagreement (bb1 directory) | ADDR | frozen set keeps `bb1-directory-named-desktop`; frozen materialize handles dirs |
| ExecControls | F8 `--fixtures` default | ADDR | default path beside counter |
| ExecSessionMarker | R3 marker+serial rule, shown able to fail both ways | ROUTED | install registry+sidecars at data time; gate stays red by design |
| ExecRefB | 19 quirks; Type/NoDisplay; state leak; print order; delimiters | ADDR | fixtures/model; docstring |
| SentHost | F1 FIFO DoS (resolver hang) | **OPEN (O4)** (fixtures exclude FIFO; per-case timeout exists; tool-side non-regular refusal not in contract/docstring) |
| SentHost | F2/F2b ambient cache write outside scratch | ADDR | counter sets XDG_CACHE_HOME per case; incident rule: every resolver run redirects scratch |
| SentHost | F3 warm cache flips verdict | ADDR (hygiene) + **OPEN (O3)** |
| SentHost | F4 no print-mode mandate | ADDR | all 190 fixtures and ARGVS carry a print/`--test` mode (audited) |
| SentHost | F5 control variants launch risk | ADDR | controls run inside bwrap |
| SentHost | F6 `pacman -Qo` vs paused pacman | META | substitute documented; host-guard note |
| SentHost | F7 systemctl env dump | ADDR-in-practice | RevengerUwsm filtered XDG_*/PATH only |
| SentHost | F8 mktemp recipe leak | META | SKILL-doc replacement proposed |
| SentHost | F9 `assimilation/` write-scope contradiction | **OPEN (O6)** | ExecIdGuard wrote outside its seat dir; L1 to rule/clean |
| SentHost | F10 `--print-content` arbitrary-bytes ban | META | contract now includes `--print-content` in sandbox; host usage operator-guarded |
| SentHost | F11 `mado-verify.sh` /tmp hardcoding | META | pre-existing committed code |
| SentHost | F12 explain trace home listing | ADDR-in-practice | explain judged only on MADO_TERM line; receipts shape-safe |
| ExecOracle | sandbox/bin set/timeouts/FIFO proof | ADDR | counter mirrors (bwrap allowlist, 7 externals, 30s timeout) |
| ExecFixtures | 147 curated + nonce; stderr uncompared; readdir-order caveat | ADDR | merged to 190 (147 seat + 43 l1); drift check guards expect |
| ExecCounterC2 | draft clause f ran the tool (coupling) | ADDR | L1 freeze replaced with committed resolver capture (resolver_sha256) |
| ExecCounterC2 | control gaps (EMPTY/REF) | ADDR | frozen ctl-c2: POS admitted, N-{BASE,QUOTE,BRANCH,HELD,RECEIPT,NOSTEPS,OBS,NOSHA,RANGE,PIN} rejected |
| ScrEntry | entry draft; `<LIVE:*>` placeholders; S327 pin path | ROUTED | integration checklist at data (O5) |
| RevR46 | D1–D3 citation defects (round-46) | META | not this round's claims |
| ExecCache | cache semantics; "never reads $XDG_CACHE_HOME" ask | **OPEN (O3)** | unenforced |
| ScrLesson | R1–R4 acceptance matrix; lesson skeleton | ROUTED | L1 integration |
| ExecStraceTrip | P1/P2/P3 + fail-closed + clone/fork counting + audit layer | ADDR (P0a-style fail-closed, socket/execve) + **OPEN (O2)** | r trace set omits clone/fork/vfork; no audit-layer write deny-list |
| SentPrivacy | P1–P10; gate-blind gaps in round-46 files | META | previous-round hygiene; new receipts shaped |
| ScrToolLedger | F1–F5 tool-ledger hygiene; criterion 91 | META | not claim-bearing |
| RevengerUwsm | uwsm env neutrality; hotkey `--dir` seam | ADDR | limits state wrapper unmodelled |
| ScrSkill | 1 data-dir precedence wording | ADDR | docstring: ascending preference, XDG_DATA_HOME last |
| ScrSkill | 2 "wrong Type" | ADDR | no such rejection in contract |
| ScrSkill | 3 print-without-flag undefined | ADDR | refusal exit 2 declared |
| ScrSkill | 4 `--print-content` omitted | ADDR | included in contract |
| ScrSkill | 5 explain trace grammar unfrozen | declared | counter reads only MADO_TERM line tokens |
| ScrSkill | 6 wrapper seam | ADDR | documented |
| ScrSkill | 7 async cache write | ADDR (hygiene) + **OPEN (O3)** |
| ExecSupersede | R4a rows S346–S353 (renumbered past C2 block) | ROUTED | landing at data; census green |
| ScrScorecard | F8 Separable producer seat | ROUTED | w2 ExecSeparability seat dispatched |
| ScrRows | S326–S338 rows drafted; stand-in census | ROUTED | landing at data (used-by entry) |
| ScoutSpecs | spec MR open; tag bytes; P22 readdir tie | ADDR | S330 head pinned; single-observation caveat |
| ScrMistakes | M47-1..6 round-46 closure defects; M47-6 pyc-in-tree | META | L1 hygiene |
| ScoutScriptMap | 9 script facts | ADDR | mirrored in docstring/fixtures |
| ScrErrataR45 | R4b six units confirmed | ROUTED | errata append-ready |
| ExecLive | live 3-line capture; user-override proof | ROUTED | receipt source for C2 clause f at data |
| ExecR2Digest | R2 digest + removal | ADDR | `receipts/r2-removed.txt` tracked at HEAD |
| ExecAxisBase | C1: operability axis blind to tools/ | META | cite counters, not axis rows |
| ScrErrataCal | R4c six errata confirmed | ROUTED | SCORECARD append-ready |
| ConnClaims | checklist P1–P6 (1–9) | ADDR | all items present in freeze; exceptions: TRIP-FORK control missing (O2), live-receipt clause re-shaped by L1 (resolver capture) |
| CritRoutedItems | R1–R4 statuses | ROUTED | all drafted; landing pending |
| ScoutHeld | ground-absent terms; held rows | ADDR | clause i uses the four terms; S056–S060 held (clause h) |
| ScrErrataR1 | R1 erratum (two-config + citation) | ROUTED | append-ready |
| CritOracle | F1–F11 (readdir, sandbox, defaults, tripwire scope, locale, symlinks, dup IDs) | ADDR | counter/materializer reflect; same-order materialization mitigates readdir |
| CritPremise | F1–F3 selection-half scoping | ADDR | registration premise corrections adopted |
| ScoutShokuknow | staged id space S203–S349 overlaps C2 S326.. | META/risk | adoption would collide; not this round |
| ExecIdGuard | 70 staged collisions; quarantine slice | META | outputs landed in `assimilation/` (see O6) |
| ConnSiblings | no sibling claims; PROVINCE refinement | META | proposal |
| CritClaimSizing | 1 exfiltration | ADDR | tool sandbox sees no repo/oracle tree; per-run roots |
| CritClaimSizing | 2 vendoring decision | ADDR | declared permitted (emulator/interpreter residual) |
| CritClaimSizing | 3 nonce freshness | ADDR | os.urandom default; wide ranges |
| CritClaimSizing | 4 behavior-matrix | ADDR-in-effect | fixtures/g cover listed axes |
| CritClaimSizing | 5 explain self-verifiable | ADDR | clause x: AGREE/DIFFER both ways per fixture |
| CritClaimSizing | 6 C2 reproduction by author | ADDR | clause f now committed-resolver-capture (no tool re-run) |
| CritClaimSizing | 7 C2 cross-check vs C1 oracle | declared | not implemented; step truth uncounted |
| ScoutOmarchy | user-override shadowing; byte origins | ADDR | rows S333/S334/S337 etc. drafted; supports C2 |

## 2. Open findings that should block data or force a v2 re-registration

**O1 — C1: file writes are invisible to the counter [PROVEN].**
Contract: reference docstring line 4 "Read-only … writes no file"; claim: "without
starting any process". The frozen r trace set is `execve,execveat,socket,socketpair,connect`;
no `openat`/`write`/`O_CREAT` audit, no post-run inspection of `.rw`.
Reproducible: take `.ufo/waves/round-47/l1-draft/mado-terminal.py`, insert at the top of
`main()` a write to `$XDG_CACHE_HOME/poison-marker`; score with the frozen counter at
`d7527d6` (recipe below). Result: `fixtures=190/190 explained=190/190 generated=150/150
selftest=ok readonly=ok tool=present verdict=TARGET_MET nonce=4747` (`score-write.txt`).
On the host a writing tool could poison `~/.cache/xdg-terminal-exec` (SentHost R11). → v2
needs a write audit (strace `%file` on tool runs or an `openat` allowlist, plus
poisoned-cache negative control).

**O2 — C1: fork without execve is invisible to the tripwire [PROVEN].**
`os.fork()` produces no `execve/execveat/socket/socketpair/connect` event, so a tool that
spawns a child process passes clause r. Reproducible: same reference + `os.fork()` child
writes a marker and `_exit(0)`; score → full MET, `clause=r trips=0` (`score-fork.txt`).
ExecStraceTrip P2 (count `clone/clone3/fork/vfork` without `CLONE_THREAD`) was not adopted.
→ v2: add `%process` capture or clone counting; keep P0a fail-closed.

**O3 — C1: a cache-reading tool is undetectable (declared residual, still open).**
The counter never presents a cache: `XDG_CACHE_HOME=<root>/.rw/cache` is created empty and
the oracle's tree is a different tree. A tool that reads `$XDG_CACHE_HOME/xdg-terminal-exec`
passes unchanged (nothing to read); the host warm cache exists (190 B), so the mistake is
unobservable in the sandbox and harmful on the host. Registrational residual declares the
warm-cache path out of contract; the draft counter's forged-cache run (run D) was dropped.
→ v2: poisoned/forged cache control (tool answer must be unchanged; `explain` states cache
ignored), and/or openat read-audit of the cache path.

**O4 — C1: timeout→verdict and no non-regular-file guard.**
`Box.run` maps `TimeoutExpired` → `(124, "")` and compares the tool against that value, so
a hanging oracle (a FIFO named `*.desktop` in the last applications dir) would read as "the
tool must exit 124" instead of a setup error. No FIFO fixture exists today (audited: the
only non-regular-ish case is the `bb1-directory-named-desktop` directory, which the counter
materializes as a dir), so scoring is unaffected; but the tool's own behavior on a FIFO is
undisclosed (no declared divergence, no `O_NONBLOCK`/`S_ISREG` guard, no docstring line).
→ v2: script-side timeout = setup error; add the declared divergence + refusal; keep the
per-case timeout.

**O5 — C2: the draft entry cannot pass clause f as-is (expected integration).**
`w1/ScrEntry/entry.md` cites `.ufo/waves/round-47/receipts/<LIVE:live-receipt>` (placeholder);
clause f requires a real committed receipt (`resolver_sha256=…`, ≥3 `XDG_*`, `observed=`,
capture committed, absent at base) plus fetch pins at `fetch/`, SOURCES rows S326.., and the
README row. The entry's own checklist (ScrEntry §7) names the exact three edits. If the data
commit lands the entry verbatim, C2 honestly misses (`no_r17_receipt_line`). → block data on
integration; not a counter defect.

**O6 — Routed closures and hygiene pending at data.**
R3 marker install (registry `quality/session-material-waivers.txt` + sidecars) before the
gate run; R4a rows on46–S353 (keep S326–S345 free for C2); R4b/R4c errata append; SentHost
F9 `assimilation/` write-scope contradiction; M47-6 pyc-in-tree hygiene. None modify the two
predicates; all are data-time landing prerequisites for a clean commit.

## 3. Reproducible commands

Pre-data heads:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c1-r47-terminal.py --repo . --rev HEAD --work <scratch> --nonce 4747
python3 -I quality/counters/c2-r47-terminal-entry.py --repo . --rev HEAD
```

Mutant score (O1/O2), each candidate at `tools/mado-terminal.py`:

```
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r47/ConnW1Ledger)
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp <candidate> "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
mkdir -p /fast/scratch/hyaku/mado-r47/ConnW1Ledger/w
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py \
  --repo "$D" --rev HEAD --work /fast/scratch/hyaku/mado-r47/ConnW1Ledger/w --nonce 4747
```

## 4. Evidence index (this seat dir)

- `score-write.txt` — sha256 `12d809470e461939ebc31029cbf512a99cbd2eaad81903e772626ea5fff4bf8e` (O1 MET).
- `score-fork.txt` — sha256 `5eae6c05ae27f53a5ebdcf8977202cda86ac133152056c47295f0624d2f64d94` (O2 MET).
- Pre-data C1/C2 lines reproduced in §0; fixture audit (190; 0 no-print; `bb1-` dir present; 44 `l1-`; sha `4836cc1d…`) run live.
- Instrument identity: counter `2b9c2d0e…`, reference `762d042c…` at `d7527d6` == HEAD.

No tools installed/upgraded; no lane writes outside this seat dir + report; scratch removed.

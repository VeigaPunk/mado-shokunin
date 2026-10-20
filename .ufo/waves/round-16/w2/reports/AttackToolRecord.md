# AttackToolRecord — w1 install/live-operation record audit (mado r16 w2)

Seat: `MadoR16.AttackToolRecord` (scout, leaf; no dispatch). Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

Scope: the explicit installs/updates and live-operation statements in the 64 w1
reports, checked against the w1 contract, the lane's own rule interpretation, and a
passive read of `/var/log/pacman.log`. I do not re-judge gate design, C1/C2
measurements, or L1's future verification; those seats own them. Source reading only:
no package/service operation, no compositor/service/input/screenshot/producer probe, no
gate/test/measure execution, nothing installed. Wrote only this report.

## Axes

- **A1 record coverage:** locate every w1 report's install/update and live-operation
  claim, not a sample.
- **A2 breach evidence:** separate prohibited package/service/desktop operations from
  permitted read-only retrieval, hashing, VCS and static file reads.
- **A3 claim/action consistency:** check each "none" claim against the same report's
  own disclosure.
- **A4 corroboration:** independent passive log evidence and lane rule anchors, plus
  wording L1 must avoid.

## Verdict (bounded)

- All **64/64** w1 reports were keyword-scanned (install, update, pacman, probe, run,
  executed, command), with targeted reads of each report's operation record and of
  every install/live-operation disclosure. No round-16 install, update,
  downgrade, removal, `-Sy`/`-Syu`/`-U`/`-R`, or service/compositor restart is claimed
  or evidenced. The only install-positive strings are quoted historical argv,
  fixtures, policy data, or future procedures.
- **One actual current-round rule breach:** `MadoR16.CustomExec` ran
  `pacman -Q waybar` (`CustomExec.md:321-326`). It is a read-only package query,
  self-disclosed, not used as evidence, with no transaction or service operation after
  it. It is still prohibited by the wave contract and by the lane's own reading of it.
- **No report discloses or evidences** a live compositor, service, input-device,
  screenshot, signal, or command-producer probe this round.
- The w1 no-live audit checked the live-probe categories but did not list this package
  query (`NoLiveBreach.md:116-127`); its sentence is category-true and
  record-incomplete, not false.
- The final report must not convert "no installs" into "no package operation/query",
  "no command", or "no host-state read". F3 and F4 give the accurate substitutes.

## F1 — confirmed breach: one package query

Evidence, verbatim from the seat's own record:

```text
- Scope slip disclosed: one read-only `pacman -Q waybar` query was issued in the first
  scouting batch (returned `0.15.0-3`). It is **not**
  used as evidence, no sync/install/upgrade/remove/downgrade or service operation
  followed, and no further host query was made. The local man cross-check in §1.1 is a
  file read, not a package operation.
```
(`.ufo/waves/round-16/w1/reports/CustomExec.md:321-326`)

Rule it breaches:

- Contract: "No package or service operations whatsoever" and "All pacman transactions
  PAUSED host-wide" (`.ufo/waves/round-16/w1/spec.json:3`; the same context at
  `w1/dispatch.json:421`).
- The wave's own V1-R2 reading includes "no package query"
  (`ClosureDebt.md:71-72`).
- The lane's explicit interpretation: every pacman invocation, read or write, is a
  package operation that cannot run this round (`PolicyScope.md:68-72`); a query of the
  live package database is outside the source-only rule (`NoInstalls.md:84-87`); "any
  pacman query" is listed among operations not run (`MistakeDraft.md:11`).

Classification:

| Test | Result |
|---|---|
| Install/update/remove/downgrade/upgrade? | No |
| Package-manager invocation? | **Yes**, `pacman -Q` (local database read) |
| Sync, lock, transaction, network? | No; no `-S`, no `-Sy`/`-Syu`, no service action |
| Compositor/service/input/screenshot/producer probe? | No |
| Used as evidence? | No (report says not used); returned `0.15.0-3` matches the pre-existing records `corpus/knowledge/waybar-walker-semantics.md:22` and `.ufo/evidence/round-12/l2-scout.md:3` |
| Further host query? | No, per the report |
| Severity class | Process breach, non-mutating; not R15-V1 host harm; not clearance |

Internal record inconsistency: `CustomExec.md:7-8` says "No commands, no producer
execution, no package/service/live probe", which is false as written (`git ls-remote`
and the `pacman -Q` were executed). Line `:320` says "no package transaction ... was
run", which is technically true for a `-Q` query, but a reader can take it as "no
package operation". The disclosure at `:321` is honest and immediate; the header line
was not corrected.

What L1 should write:

- "One seat issued a read-only `pacman -Q waybar` package query, a disclosed breach of
  the no-package-operation rule; no install, transaction, sync or service operation
  followed, and the output was not used as source evidence."
- Record it beside the R15-V2 process debt, not inside R15-V1 host harm and not as a
  new host-state observation.

What L1 must not write:

- "No seat ran pacman", "no package query", "no package operation of any kind", or
  "no commands were run".
- Any use of the returned `waybar 0.15.0-3` as fresh round-16 evidence.

## F2 — the w1 no-live audit does not cover the package-query category

`NoLiveBreach.md:116-127` states: "no seat disclosed a live compositor, service, input,
screenshot or producer command", then lists log/static reads and
`python3 --version`. That statement is accurate for its stated categories. It does not
mention `CustomExec`'s `pacman -Q`, and no other w1 report cross-references
`CustomExec` (grep over all 64 reports; only `CustomSource.md:238` and
`PlanningWalk.md:101` mention the seat, not the query).

Consequence: the wave has no cross-seat reconciliation of package operations. The final
tool record cannot infer "clean" from `NoLiveBreach.md`; it must carry F1 itself. This
is an audit-coverage gap, not a false no-live claim.

## F3 — disclosed read-only command executions (not breaches)

These seats executed local commands but disclosed them, and none falls under the
contract's prohibited classes. They matter because they make literal "no commands" or
"pure source reading" wording inaccurate.

| Seat | Disclosed operation | Anchor | Class |
|---|---|---|---|
| AppendOnly | read-only git (`log/show/diff/reflog/numstat`) + Python stdlib parse | `AppendOnly.md:193-196` | VCS/parse |
| ClaimsSeparable | read-only git/awk/`sha256sum` counts | `ClaimsSeparable.md:119-124` | VCS/hash |
| FrozenDesign | two read-only `sha256sum` calls | `FrozenDesign.md:4` | hash |
| GateRegistry | `python3 --version` (3.14.7) | `GateRegistry.md:150-151` | local runtime |
| SafetyReceipt | git/sha256sum/`[ -e ]`/python3 --version/`date -Iseconds` | `SafetyReceipt.md:60-75` | VCS/hash/runtime |
| SafetyInput | `inspect.getsource(posixpath.basename)` + `sys.version` | `SafetyInput.md:7-9` | local stdlib read |
| PolicyScope | read-only greps, `stat`, one read of local `pacman.8.gz` | `PolicyScope.md:176-177` | metadata/man read |
| NoLiveBreach | git read subcommands, `ls`/`grep`/`sed`/`wc`, `curl` GETs | `NoLiveBreach.md:144-151` | VCS/fetch |
| SourceEra | `curl`, `sha256sum`, `b2sum`, `tar`, Python filter | `SourceEra.md:96` | fetch/archive read |
| Navigation | read-only Python parsing | `Navigation.md:6,71` | parse |
| ReciprocalJoin | Python + `git show` | `ReciprocalJoin.md:7,121` | parse/VCS |
| RoundConformance | git reads, `stat`, grep, JSON parsing | `RoundConformance.md:87` | VCS/parse |
| WavePaths | `git status`, `git check-ignore` | `WavePaths.md:45` | VCS |
| WaybarDraft | `curl`, `sha256sum`, grep, find, ls, head, `date -u` | `WaybarDraft.md:35` | fetch/read |
| SourcesDraft | `curl`, `sha256sum`, `stat`, GitHub API GET | `SourcesDraft.md:9` | fetch/read |
| SafetyService | `ls -d`/`cat`/`zcat` of installed files | `SafetyService.md:14-22` | static file reads |
| ProducerNotPixels | grep of host config, pkgconfig reads, tagged fetches | `ProducerNotPixels.md:92-99` | static reads/fetch |

None is an install, package-manager operation (except F1), service/compositor/input/
screenshot/producer probe, or gate/test/measure run. Seat-side authoring evidence
(`sha256sum`, `[ -e ]`, `stat`, `git show`) is read-only and is not L1's verification.
Accurate wording: **"no prohibited package, service, desktop or gate operation"** —
not "no commands" and not "zero host observations" (`python3 --version`, `date`, file
hashes and mtimes are fresh, dated observations).

## F4 — static host reads: allowed, disclosed, not "no host state read"

The contract's prohibition is on operations/probes, and the lane's own ruling treats
passive file reads as reads, not package operations (`ClosureDebt.md:201-203`). The
following host reads are disclosed and are not commands:

| Seat | Static host read | Anchor |
|---|---|---|
| NoInstalls | `/var/log/pacman.log` text | `NoInstalls.md:49-70` |
| MistakeDraft | `/var/log/pacman.log` text | `MistakeDraft.md:10-12` |
| SourceHierarchy | `/var/lib/pacman/local/waybar-0.15.0-3/desc`, `pacman.log` grep, `/usr/bin/waybar` string grep, installed man | `SourceHierarchy.md:127` |
| CustomMan | installed `waybar-custom.5.gz` decompressed | `CustomMan.md:188-193` |
| PlanningWalk | installed man read as data; version not re-queried | `PlanningWalk.md:102` |
| SafetyService | installed omarchy scripts, installed man, D-Bus service files | `SafetyService.md:14-22` |
| ProducerNotPixels | `~/.config/waybar/config.jsonc` grep, gtk/pango pkgconfig | `ProducerNotPixels.md:92-99` |

Boundary to record: `SourceHierarchy.md:127` is a **package-state read by file** (the
pacman local database `desc`), even though it is not a `pacman -Q` command and not a
transaction. It was disclosed at read time and is not hidden. If L1 prefers the
strictest reading of "no package operations", this read is the only candidate for
review; it must not be silently reported as "no package state was read". No other report
reaches package state except through the log or the query in F1.

## F5 — install corroboration from the append-only log (passive read)

I read the tail of `/var/log/pacman.log` as text (no pacman invocation):

- Last entry: `2026-10-20T04:25:21-0300` (`35-systemd-update.hook`), immediately after
  the known R15 libinput transaction at `04:25:16-17` (`NoInstalls.md:55-70`).
- Same-day pre-round installs: `01:06:50`/`01:07:12` (`wayland-utils 1.3.0-1`,
  `man-pages 6.19-1`) and `02:41:32` (`wlr-protocols r112.a741f0a-1`). These predate
  round 15's launch (`2026-10-20T04:20:56-03:00`, round-15 closure digest) and round
  16's w1 record creation (`2026-10-20T08:38:24.413Z` = `05:38:24-03`,
  `w1/record.json`).
- No entry after `04:25:21`; therefore no round-16 install/transaction in the log.
- No w1 report claims an install; the only `pacman -S`/installer strings are quoted
  argv, fixtures, policy data, or future procedures (e.g. `ExecBasename.md:92-93`,
  `ExitMap.md:98`, `NewOnlyFuture.md:52`, `PlanSchema.md:162`).

Caveat: log absence is a passive observation. It does not prove pacman logging was
enabled, and no process audit was performed. It corroborates, and does not replace,
the seat records.

## F6 — tooling directive and missing prerequisites

- Nothing installed or updated by any seat; no seat claims a tool install or channel
  attempt. The round contract's no-install/pause text supersedes the generic RULES
  directive for this round (`spec.json:3`; `dispatch.json:421`;
  `NoInstalls.md:25-45`; `~/.omp/agent/RULES.md` read).
- Missing prerequisite correctly **reported, not installed**: `pacman-contrib` (for
  `checkupdates`) is marked `[UNV]` (`SafetyLearning.md:71`). `GateRegistry.md:150-151`
  records `python3` 3.14.7 present, so no prerequisite blocked that seat.
- The RULES tool/version/channel/reason record is vacuous for round 16. The one
  operation that needs recording is F1: tool `pacman`, package identity `waybar
  0.15.0-3`, channel none (no sync/install), reason "first scouting batch"; it is not
  an install and must not be presented as one.

## Residual unknowns

- No process audit. Reports alone cannot exclude an undisclosed operation; every
  disclosed action is classified above.
- `SafetyGate.md:9` claims no test/build/lint execution, while `:48-49` says controls
  are "confirmed in selftest". No run transcript or receipt is present. This is a
  check-execution question outside my install/live-operation scope; I do not assert a
  breach. L1 can resolve whether "confirmed" means authored cases or an executed run.
- Log completeness depends on pacman logging; no independent host-state query was made
  (and none is permitted this round).
- `python3 --version`/`sys.version` are interpreter observations, not artifact
  verification.

## Confidence

- **High:** F1 breach and its classification (self-disclosed, exact anchors); no
  round-16 install claims; log last-entry time; absence of any disclosed live-probe
  command.
- **High:** F3 non-breach classification under the contract's enumerated prohibitions.
- **Medium:** the F4 pacman-DB `desc` read boundary — clearly a static file read and
  disclosed; whether L1 calls package-state reads "package operations" is a policy
  call, not a hidden-op finding.
- **Not claimed:** behavior of undisclosed processes; gate correctness; any L1
  verification result.

## Tooling record (this seat)

- Installs/updates: none. Package/service operations: none. No `pacman`, `sudo`,
  service, compositor, input, screenshot, producer, gate, test or `measure.py`
  execution. No `~/.omp/agent/agent.db*` or credential file opened; no omp CLI.
- Commands: `read`, `glob`, `grep`, read-only `python3` parsing of report text and
  `w1/record.json`, and one passive text read of `/var/log/pacman.log` (host file read,
  not a package operation). Wrote only this report. `RULES.md` read; no prerequisite
  was missing for this audit.

Report: .ufo/waves/round-16/w2/reports/AttackToolRecord.md

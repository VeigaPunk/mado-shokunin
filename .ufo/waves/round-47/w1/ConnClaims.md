# ConnClaims — pre-freeze checklist for round 47 v1 (C1 xdg-terminal / C2 xdg-terminal-selection)

Seat: `ConnClaims` (leaf, cross-claim and cross-item pattern scan). Round 47 wave w1 = BUILD (policy v1), base
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. Nothing is frozen yet: this checklist feeds the L1's `registration.md`
freeze, which happens AFTER w1 returns and BEFORE any data commit (`.ufo/waves/round-47/claims.md:3-5`).

Method: I read the round-45/46 registrations (v1/v2/v3), their cheat/forgery evidence
(`CritC2Forgery`, `ExecC1Separability`, `ConnCrossClaim`), the scorecard sections, the routed-deficit list
(`corpus/lessons/round-46-verifier-spotcheck.md` §6), the r17 [UNK] site, the session-material gate and the round-46
C2 counter. Everything below names what it supports (path:line). The pattern I found: two of the four routed items
(R1 receipts provenance, R3 session-material hygiene) are the *same failure classes* that will hit the C2 live clause
and the C1 receipts; R4 interacts with the C2 registry census; R2 with the C1 fixture/expect hygiene.

---

## 1. Separability — show C1 and C2 independent both ways

Round-45/46 precedent, both confirmed: round 45 `w1/ConnCrossClaim.md:8-15` (trees A/B), round 46
`w1/ExecC1Separability/report.md:33-58` (tool-only, data-only, plus a both-artifacts probe). The L1 has now published
"Separable:" lines in both scorecard rounds (`SCORECARD.md:2605`, `:2634`). For round 47 the freeze must require the
same three trees, built from the **base** commit `60edb66e`, with the **frozen** counters (not the draft ones):

| tree | contents (vs base) | expected |
|---|---|---|
| tool-only | + `tools/mado-terminal.py` only | C1 MET, C2 0/1 (exit 1) |
| data-only | + entry, SOURCES rows, lesson Gate, README row, fetch pins, live receipt | C1 MISSED (tool absent), C2 MET |
| both | tool + data at **one** commit | C1 MET and C2 MET (closes the two-commit gap noted in `ExecC1Separability/report.md:110-111`) |

Disjointness is the property that makes this meaningful, and it must be *code-located* like round 46
(`ExecC1Separability/report.md:60-79`): the C1 counter greps only `tools/mado-terminal.py` from the scored repo (its
fixtures/oracle load from the counter's own lane, sha256-pinned); the C2 counter never opens, hashes or runs the tool.
For round 47 add the mirror greps to the checklist:

- C1 counter must not read `corpus/` (entry/registry/lesson/README) — grep the counter for `corpus|SOURCES|knowledge|lessons|README` and require only `tools/` hits.
- C2 counter must not read `tools/` or run `mado-terminal.py` — grep for `tools/|mado-terminal|terminal\.py` and require zero hits.
- **New coupling risk:** C2's live clause is the only place a dependency could sneak in. If the C2 counter *runs* the
  tool to regenerate the live receipt, C2 becomes coupled to C1's artifact and separability dies; if it merely *verifies
  bytes* of a stored receipt, separability holds. Recommendation: the C2 counter verifies the receipt (bytes, producer
  line, re-measurability) — it never executes the tool (detail in §3/§4).

Empirical direction check, as in round 46: the data-only C1 line shows `clause=a tool=absent` (`c1-data-only.txt`)
and the tool-only C2 line shows every clause flag 0 with the pins present — a genuine rejection, not a harness failure
(`ExecC1Separability/report.md:81-83`).

## 2. Registration-v2/v3 failure patterns that will recur — pre-emption for the v1 freeze

### P1. v1 contract froze before semantic validation against the real artifact
Round 45: v1 wrong on six Hyprland forms (`registration-v2.md` r45:15-18); round 46: v1 wrong on strtof rounding, hex/
inf/out-of-range scroll factors, a final continuation line, the directive trigger, `source =` inside a block
(`registration-v2.md` r46:29-32). Each forced a mid-wave v2 re-registration that threw away v1 wave results.

Round 47 pre-emption: the C1 judge is the real pinned script, so *semantic* drift now fails tools, not instruments — but
the instrument's **environment model** can still be wrong. Before freezing, run the draft contract against the pinned
script (`/usr/bin/xdg-terminal-exec`, sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`) on
the host and inside bubblewrap, and freeze the answers to:
- the script's external command set under strace (`tr`, `find -L`, `awk`, `/bin/sh` = bash — host facts) — the sandbox must supply exactly those, and fake binaries must bind every one of them;
- env semantics: unset vs empty `XDG_CONFIG_DIRS`/`XDG_DATA_DIRS` (defaults `/etc/xdg`, `/usr/local/share:/usr/share`), tildes in `HOME`, `PATH` search order, `XDG_CURRENT_DESKTOP` prefix matching;
- the print-mode cache write (`~/.cache/xdg-terminal-exec`, r17:123): each side of the comparison must get its own fresh empty cache; the tool models a cold cache and writes nothing;
- locale/`LC_ALL` pinning, so error-message bytes are stable;
- the exact exit-status surface (usage vs no-terminal vs select) the script uses.

### P2. Do-nothing / cheat tools reached MET under v1 — the control battery must exist AT freeze
Round 45: 11/11 cheat tools + 5 do-nothing controls met v1 (embedded fixture tables, counter import, reference loader,
parent-process reader, seed-45 answer table, scorer oracle reading `/proc/<ppid>/cmdline`) (`registration-v2.md` r45:13-15).
Round 46: delegator execing an ambient reference copy found under `/fast/scratch`; marker deletion; bare `hyprctl`
during `--selftest`; `/usr/bin/hyprctl` by absolute path (`registration-v2.md` r46:26-29). The round-46 v2 counter then
had to add REF/controls (`ctl/run-c1-controls-v2.py`) and STILL shipped a broken tripwire (P3).

Round 47 pre-emption — the v1 counter must ship with controls *at freeze*:
- BASE (no tool), STUB (prints an OK summary + selftest line), a copy of a previous round's tool (`mado-monitors.py`/`mado-devices.py`),
- a hardcoded-answer table for the pinned fixtures (the round-45 seed-answer cheat),
- DELEGATE-ANY (searches the sandbox-visible dirs for any `mado-terminal.py` and execs it — the round-46 ambient-copy cheat),
- TRIP-PROCESS (tool that spawns any subprocess → must fail the tripwire; if it passes, the tripwire is dead — P3),
- TRIP-SOCKET (tool that opens a socket → must fail),
- TRIP-SELFTEST-ONLY (identical behavior only under `--selftest`),
- V-variants undoing one correction each: no-cache-model, wrong list order, ignore `Hidden`, ignore `TerminalEmulator`,
  ignore `TryExec`/`Exec` PATH check, wrong `Type` default, ignore `ShowIn`/`NotShowIn`, wrong `--dir`/`--title`/
  `--app-id`/`--hold` handling, wrong delimiter/cmd composition, wrong fallback when no terminal (exit 3).
Every non-REF control must score TARGET_MISSED; REF (the real reimplementation — see P5) must score TARGET_MET.

### P3. The tripwire itself silently failed — it must be probe-proven at freeze
Round-46 v3 is the canonical lesson: `PRED-C1-r46-v2` failed its own TRIP controls because "clause r's tripwire was an
inherited pipe, and the tool's own `subprocess.run` closes inherited fds, so the fake `hyprctl` could not write to it"
(`registration-v3.md:5-6`). Fix: a unix socket the counter listens on outside the sandbox, fake binaries connect and
send their name, accepted connections cannot be taken back (`registration-v3.md:10-13`), verified by a pre-freeze probe
(`registration-v3.md:14-15`).

Round 47 pre-emption: freeze the tripwire **and its own probe** in v1: (a) `strace -f` execve count on the tool run
must be 0; the strace attach must be verified to work inside bubblewrap before freeze; (b) socket syscalls banned
(seccomp or strace) *and* net namespace isolated; (c) fake binaries bound over `/usr/bin/xdg-terminal-exec` AND the
shells AND `tr`/`find`/`awk` (the script's external deps), so absolute-path calls are caught like the round-46
`/usr/bin/hyprctl` bypass; (d) run TRIP-PROCESS and TRIP-SOCKET controls at freeze — their TARGET_MISSED is the proof
the tripwire is alive. Do not freeze a tripwire whose controls run only after w1 (that is exactly the v2→v3 path).

### P4. C2 forgery classes admitted outside declared residuals — carry the full a-k + A-G counter
Round 46: six undeclared forgeries (F4 README redirect, F5d falsified uncited row on a pinned URL, F6 anchor cell naming
unread lines, F7 receipt authored by the scored revision, F8 indented code in no pin, F10 chain replaced by a citation
index) plus `OK` missing from the T4 tokens (`registration-v2.md` r46:62-70; `CritC2Forgery.md:49-62`); round 45: nine
forged revisions incl. a false fence table, a sentence citing the refuting receipt, a free README id list, census tokens
one space off, a new row claiming a supersession (`registration-v2.md` r45:40-43).

Round 47 pre-emption: the C2 counter must be the round-46 v2 counter re-cut (clauses a-k + A-G, `c2-r46-input-device-entry-v2.py:20-87`)
for the new entry/lesson/fetch pins, plus the round-47-specific clauses in §3. In particular the A-G tightenings are the
known-closed holes: quote-inside-anchor (F6), README status-token + no redirect words (F4), cited receipts byte-equal at
freeze or producer-bound (F7), indented-code verbatim in pins (F8), uncited rows unchanged (F5d), no orphan rows (F5),
≥5 numbered steps carrying every surface (F10) — `CritC2Forgery.md:123-154`.

### P5. "The reference copied meets the target" must be declared, not hidden
Round-46 v2 declared: the reference is the capability drafted before the freeze; installing it at `tools/` IS the
claimed landing, and the controls are what separate a real landing from a do-nothing (`registration-v2.md` r46:52-54).
Round 47 differs: the judge is the **host's** script, which predates the round. A byte-copy of the sh script is not a
Python-3-stdlib re-implementation, but a faithful port is the goal by definition. The freeze should state this: what a
tool must not do is read the pinned script's *bytes at runtime* to copy outputs. Note the fake binary bound over
`/usr/bin/xdg-terminal-exec` already prevents that in the tool sandbox (reading it yields the fake, not the real
script) — state that as a declared residual and as a control (a tool that reads `/usr/bin/xdg-terminal-exec` and
pattern-matches its output must still be MISSED, or the sandbox must hide the path entirely).

### P6. Instrument-health traps from round-46 ExecC1Separability risks
- `--work` must pre-exist (else SETUP exit 2) — `ExecC1Separability/report.md:102-103`;
- counters are not self-contained: fixtures/oracle load from the counter's own lane; scoring a bare copy is a setup error
  (`:104-106`); clones must be `--shared` full-history so `--base` resolves (`:107-109`);
- a single-artifact MET at two different commits does not prove one commit satisfies both — the both-tree probe closes it
  (`:110-111`).

---

## 3. Routed items sharing a cause with the claims

### R1 (receipt provenance) is the C2 live clause's failure mode
The r46 entry attributes its live join to `receipts/live-devices-host-l1.txt`, whose producer is the `l1-draft` tool,
not the landed tool (`round-46-verifier-spotcheck.md:107-110`). The r17 [UNK] the C2 entry must close is "whether the
resolver actually picks that entry over the system one at launch" (`terminal-route-r17.md:144-145`). The F7 forgery is
the same shape: "the revision writes its own live-run receipt … and cites it" (`CritC2Forgery.md:16-18`). So:

- the C2 live observation must cite a receipt whose **producer is the landed tool** `tools/mado-terminal.py` (sha256
  pinned in the receipt text), captured from a run of the tool at the data commit — not the L1's capture, not a
  self-authored file;
- the counter should verify re-measurability: rerunning the tool's `print`/`explain` on the host (with
  `XDG_CACHE_HOME` in scratch, `--print-*` only) reproduces the cited bytes; the R1 erratum (appended to
  `hyprland-input-devices-r46.md:57`) and the new entry must not repeat the mis-attribution;
- adapt clause C (receipt exists at freeze byte-identical) for the live receipt: a live receipt cannot predate the
  freeze; instead require the producer line and re-measurability. This is the one place the round-46 clause C must be
  consciously re-shaped, not copied.

### R2 (untracked artifacts) is the C1 fixture/expect hygiene
R2 = untracked `ExecStofOracle/receipts/out.json.rows.tsv` (3.3 MB) left in the worktree, a repeat of round-45 D4
(`round-46-verifier-spotcheck.md:111-112`). The C1 fixture pipeline generates large derived artifacts (nonce cases,
expect outputs run against the real script). Freeze rule: the fixture JSON (≥100 pinned, ≥150 nonce) with its
`expect` fields is committed and sha256-pinned; all generation logs live under `--work` in scratch only; nothing derived
from the nonce generator is committed raw; a digest line beside any retained large output (R2's requested fix) applies
to the counter's own receipts.

### R3 (session-material gate) applies to both claims' receipts
The gate is red at the round-46 data commit (findings=115, 18 in round-46 seat files) and the synthetic marker is still
uninstalled (`round-46-verifier-spotcheck.md:113-115`). R3 installs the marker shown able to fail both ways — before
the freeze, so the gate can run on this round's receipts with synthetic findings distinguished. For round 47: the C1
`explain` traces and the C2 live receipt are the new risk surface — traces print absolute home/config paths (R4 counts
standalone absolute-`/home/` lines >10 per file; quoted paths in sentences are exempt — `check-session-material.py:29-32`);
no window titles, process tables, monitor serials/descriptions or directory dumps may appear (host guard). The C2 live
receipt (print-mode output: id/path/cmd) is shape-safe.

### R4 (S290-S297 supersession) interacts with the C2 registry census
C2 opens rows S326..; the registry tops at S325, 262 rows (w1-spec.json context). The supersession (round-44 D6) is
scheduled before any new claim (`SCORECARD.md:2650`). If it lands, the registry top/census lines may shift; the C2
counter's census expectations must be frozen against the post-supersession state (or the dependency stated in the
registration). The new rows must carry no supersession words (T2), and the entry must not touch S290-S297 cells. The
round-45/44 errata (R4's other half) touch other entries; they do not share cause with the claims beyond the corpus
README index row (keep the C2 README row the only row for this entry).

---

## 4. The v1 freeze checklist (numbered, for the L1)

1. Pin the script in both counters: sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, URL
   `https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec`, plus a host-equality
   receipt (`cmp` against `/usr/bin/xdg-terminal-exec`) captured at freeze.
2. Fixtures: ≥100 pinned + ≥150 nonce; `expect` ALWAYS produced by running the real pinned script on the materialized
   case (the FROZEN schema already says this); freeze the generator seed(s), the fixture JSON and its sha256.
3. Environment surface frozen exactly: XDG_CURRENT_DESKTOP, XDG_CONFIG_HOME/DIRS, XDG_DATA_HOME/DIRS, HOME, PATH,
   unset-vs-empty semantics, `LC_ALL`; separate fresh empty cache dir per side (cold cache).
4. Freeze the exit-status and stdout contract (byte-identical) and decide stderr (recommend byte-identical as well);
   freeze the `explain` verdict tokens (OK/AGREE/DIFFER/NO_TERMINAL) and exit codes 0/1/2/3.
5. Freeze the control battery (P2) and the tripwire probe (P3) — TRIP-PROCESS/TRIP-SOCKET must be TARGET_MISSED at
   freeze, not discovered after w1.
6. Freeze the C2 counter as the r46 v2 counter re-cut (a-k + A-G) with the new ENTRY/LESSON/FETCH/PINS/BASE/DATE,
   `MADO_TERM` verdict tokens present in clause i's token list, the producer-bound live-receipt clause (R1/F7), and
   census expectations aligned with R4's post-supersession registry top.
7. Freeze the separability trees (tool-only / data-only / both) as a required w1 outcome at one commit (the both-tree).
8. Freeze the receipt hygiene: all receipts and the entry pass `quality/check-session-material.py` at the data commit;
   the marker (R3) is installed before that run; no untracked derived artifacts (R2).
9. Declare residuals in the registration: a tool may detect the sandbox (PID 1 bwrap) and behave differently inside it;
   a contract error shared between the tool and a stale reading of the script is invisible to the fixtures but judged by
   the real script itself; clause s is a printed line; word-form census contradictions and claim-to-quote binding are
   the non-author reading (mirror `registration-v2.md` r46:55-58).

---

## 5. Evidence

All locators computed by reading the cited files; the quotes below are verified by the grep script in
`ConnClaims/verify-quotes.sh` (receipt `ConnClaims/verify-quotes.out`). No host mutation, no compositor call, no
package transaction; scratch `/fast/scratch/hyaku/mado-r47/ConnClaims` removed at finish.

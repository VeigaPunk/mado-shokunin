# SentPrivacy — privacy of the round-47 receipts (w1, 2026-10-26)

Question: the round will commit live receipts that name host paths
(`$HOME/.local/share/applications/...`), environment values and desktop-file keys.
What may be committed under `SKILL.md` rule 4 (`SKILL.md:343-344`, "Session material stays
shape-only") and `quality/check-session-material.py` R1-R4, and where is that gate blind?

Verdict in one line: **the gate is scoped right and wrong in the same way** — it catches a
`find ~` dump (proved below) but neither a single `$HOME` path, nor an `env` dump, nor a
bare `ls` inventory, nor a strace line, nor the live `HYPRLAND_INSTANCE_SIGNATURE`; and a
`$HOME`-redacted inventory silently defeats its R4 counter. Measured on round 46: **two
live identity values are already committed and gate-invisible** (F1, F2), one of them a
direct rule-4 violation. Everything else I found in round 46 is template/synthetic.

All work is read-only. Nothing was installed. The resolver was run print-only with
`XDG_CACHE_HOME` inside scratch; no terminal, no compositor mutation, no package query.

## 1. What was run

| step | command (receipt) |
|---|---|
| pin check | `sha256sum /usr/bin/xdg-terminal-exec` → `89f2be9a…7ac` = the declared pin (`live-print.txt` last block) |
| live print run | `XDG_CACHE_HOME=$WORK/cache2 xdg-terminal-exec --print-id --print-path --print-cmd` and the `--dir/--title/--app-id/--hold/--print-cmd=seq/--print-delimiter=seq` variants → `live-print.txt` (P1/P2-redacted) |
| resolver cache | after a print run `$XDG_CACHE_HOME/xdg-terminal-exec` exists, mode 600, 188 B → `live-cache-shape.txt` |
| env record | contract variables only → `host-env-contract.txt` |
| gate | `quality/check-session-material.py --repo <clone> --rev HEAD` on a scratch clone seeded with receipts I produced → `gate-samples-raw.txt`, `gate-redacted.txt`, `gate-clean.txt`; on the lane at the round-46 tip → `gate-r46.txt` |
| class scan | `w1/SentPrivacy/sweep-privacy.py` (classes G1-G11 outside R1-R4) → `sweep-samples-raw.txt`, `sweep-redacted.txt`, `sweep-clean.txt`, `sweep-r46.txt` |
| live-value scan | `w1/SentPrivacy/live-ident.py --monitors <live json>` → `live-ident-r46.txt`, `signature-tree.txt` |

The clone was `git clone -q --shared` of the lane into `$WORK/lane`; every git call named
`-C "$WORK/lane"`; `rev-parse --show-toplevel` was asserted before the first commit. The
commits in it are fixture commits with `-c user.name=fixture -c user.email=fixture@invalid`
and are not in the lane.

## 2. Instrument results

Receipts are the sample receipts I produced from the live run, in five shapes: **A** the
realistic receipt (print triple + contract env + entry keys), **B** a `find` sweep of the
applications dir, **C** a `printenv` dump, **D** a bare `ls -1` of the same dir, **E** an
`strace -f -e trace=execve` excerpt, **F** a cache-file record with an exact `mtime`.

| shape | gate (R1-R4) | class scan |
|---|---|---|
| A raw (1 `$HOME` path, contract env) | **0 findings** | G2 (3 lines) |
| B raw (`find`, 15 whole-line paths) | **R4_HOME_LISTING count=15** | G2 (G9 counts only the `$HOME/` form) |
| C raw (`printenv`, full env) | **0 findings** | G1 (7), G2 (4), G3 (2) |
| D raw (`ls -1`, 30 bare names) | **0 findings** | G9 (30 entries) |
| E raw (strace with pids + argv) | **0 findings** | G2 (1), G10 (4 lines) |
| F raw (`mtime=<epoch>`) | **0 findings** | G11 |
| A/C/E/F after `redact.py` | **0 findings** | **0 classes** |
| B after `redact.py` | **0 findings** ← R4 stops counting | **G9 survives** (15 `$HOME/...` lines) |

Two consequences the L1 must carry into the freeze:

1. **A gate pass is not a privacy pass for this round's receipts.** Shapes A, C, D, E, F
   all pass R1-R4; C is the exact receipt a careless live run leaves behind (it carries
   `HYPRLAND_INSTANCE_SIGNATURE`, the session D-Bus address, `WAYLAND_DISPLAY`,
   `XDG_SESSION_ID`, and a PATH whose `fnm_multishells/<pid>_<epoch>` entries are
   session-unique).
2. **`$HOME` substitution defeats R4.** `HOME_PATH_RE` is anchored on `^/home/`, so the
   moment a dump is redacted the counter stops seeing it (`sweep-redacted.txt`, D has 30
   bare names and never needed redaction). The rule below therefore handles inventories by
   *prohibition*, not by substitution, and the class scan is the instrument that checks it.

Clean-state control (same clone, raw samples removed, only redacted receipts and the tools
committed): gate `files=18383 findings=115` with **0** findings in `.ufo/waves/round-47`
(`gate-clean.txt`), class scan **all eleven classes zero** (`sweep-clean.txt`). The 115 are
pre-existing in rounds 33-46.

Seat-dir parity check, run last: this whole directory was copied into the clone, committed,
and passed both instruments — gate `files=18396 findings=115`, 0 finding lines naming it;
class scan `files=18 blobs_scanned=18`, `SWEEP_TOTAL file_class_pairs=0`
(`gate-seatdir.txt`). Re-run with `sweep-privacy.py --worktree <dir>` before integrating any
new receipt.

## 3. The rule — MADO-47-PRIV (proposed; L1 freezes)

Applies to every file this round commits under `.ufo/`, and to any corpus entry that quotes
a receipt. Implemented and exercised by `w1/SentPrivacy/redact.py` (stdlib only, no
network, no process spawn; `--check` exits 1 on a residual class).

- **P1 — home root.** Every absolute path under `$HOME` is written `$HOME/...`
  (`/home/<account>/x` → `$HOME/x`). Substitution only; the rest of the path is untouched,
  so the locator stays checkable. This is the rule that removes the account segment from the
  C1/C2 receipts (`print-path` prints it by construction).
- **P2 — work root.** Every path under the seat scratch is written `$WORK/...`
  (`$WORK` named once in the receipt header, e.g. `$WORK=<the seat scratch dir the round spec fixes>`),
  and temp paths `$TMPDIR/...`. A scratch path is never a citable locator (host guard), so
  nothing is lost.
- **P3 — runtime root.** `/run/user/<digits>` → `/run/user/<uid>`. The uid is not a secret
  by itself but it is host-identifying and appears in every socket path.
- **P4 — instance identity.** A `HYPRLAND_INSTANCE_SIGNATURE` or `WAYLAND_DISPLAY` value is
  never printed, not even truncated: `SKILL.md:343-344` says "shape-checked, never printed in
  full". Write `<INSTANCE_SIG>` / `<WAYLAND_DISPLAY>`. Consequence for C1: the strace
  tripwire must not print `HYPRLAND_*` from the inherited env when it lists what it inherits.
- **P5 — environment.** Record only the seven resolver variables the fixture schema uses
  (`XDG_CURRENT_DESKTOP`, `XDG_CONFIG_HOME`, `XDG_CONFIG_DIRS`, `XDG_DATA_HOME`,
  `XDG_DATA_DIRS`, `HOME`, `PATH`), one `NAME=value` per line; never an `env`/`printenv`
  dump. Forbidden keys, dropped whole: `HYPRLAND_INSTANCE_SIGNATURE`, `HYPRLAND_CMD`,
  `WAYLAND_DISPLAY`, `XDG_SESSION_ID`, `XDG_SESSION_PATH`, `XDG_SEAT_PATH`,
  `DBUS_SESSION_BUS_ADDRESS`, `XDG_RUNTIME_DIR`, `XDG_STATE_HOME`, `LOGNAME`, `USER`,
  `SHELL`. Reason: they are session pointers (a socket path, a bus address, a session id),
  and `XDG_STATE_HOME` maps the operator's private dotfile layout.
- **P6 — PATH is replaced, not redacted.** `PATH` is written `<tool-bin>:<system dirs>`,
  where `<tool-bin>` is the sandbox bin. A redacted inherited PATH still discloses the
  login tool inventory and three `fnm_multishells/<pid>_<epoch>` directories, i.e. process
  ids and timestamps of my own shell (`redacted C` before I added the flag). This is the
  one env value where substitution is insufficient.
- **P7 — host timestamps.** A host file's `mtime` is recorded as an age class
  (`mtime=<1h|<1d|<7d|>7d`), never as an epoch. `ExecLive`'s brief asks for
  `sha256 + mtime` of the resolver cache; the sha256 is fine, the epoch is operator
  activity. Same for `btime`/`atime` if a seat needs them.
- **P8 — process evidence.** No `ss`/`pgrep`/process tables (R2 already refuses them). An
  `strace` excerpt is reduced to one `execve("<basename>")` per line: no pid, no full argv,
  no `chdir`/cwd. Argv and cwd carry `$HOME` paths, and a pid with a timestamp couples the
  receipt to one live session. Counts (`execve count=4`) are the evidence C1 needs; the
  argv text is not.
- **P9 — inventories are prohibited, not redacted.** Never commit a listing of a host
  applications/data directory: not absolute (R4 fires), not `$HOME`-rooted (R4 blind), not
  bare names (no rule at all). The installed-application profile is behavioural session
  material. Allowed: the one selected desktop-file ID plus its `$HOME`-rooted path.
- **P10 — verification before integration.** A receipt is committable only when both
  instruments are clean for it: `quality/check-session-material.py` reports no finding on
  the file, **and** `sweep-privacy.py` reports zero G1-G11 pairs. `redact.py --check` alone
  is not enough (it cannot know about an inventory, P9).

Deliberately unchanged: desktop-file key names and their public values (`Name`, `Exec`,
`TryExec`, `Categories`, `X-TerminalArg*`) are not session material — they are shipped
software data, and the C2 entry needs them verbatim. The `sha256` of host files the
resolver read is safe; a `sha256` of the resolver's *cache* names the last selection, so
pair it with shape only (P7/P9) and never with the cache body.

## 4. Round-47 exposure by seat (what each receipt must not carry)

Read from `.ufo/waves/round-47/w1-spec.json`:

- `ExecLive` — `receipts/live-host.txt`: the `--print-path` triple (P1), the "sha256 the
  files the resolver read" list (`$HOME/.config/xdg-terminals.list`,
  `$HOME/.config/<desktop>-xdg-terminals.list`, `$HOME/.local/share/...`, `/etc/xdg/...`,
  `/usr/share/...` — P1 on the `$HOME` ones), the cache `sha256`+`mtime` (P7), and the
  `Exec/TryExec/...` key diff (public, keep). Its own brief already says "no other env"
  (P5-compatible).
- `ExecCounterC1` / `ExecOracle` — the bwrap argv they must report contains the case root
  and the sandbox bin (P2) and `HOME=$ROOT/home` (fixture schema, fine); their strace
  receipts are P8.
- `ExecStraceTrip` — `strace -f -qq -e trace=execve,socket,connect` output: P8, and P4 if it
  echoes the inherited environment to prove `--clearenv`.
- `ExecCache` — a cache file body names the selected entry path (P1) and the last selection
  (P9): commit field shapes and hashes, not the body (`live-cache-shape.txt` is the
  template).
- `ExecFixtures` / `ExecRefA|B` — fixture trees use `$ROOT` already; the only risk is a
  receipt that prints `mktemp -d` output verbatim (P2).
- `ScrEntry` / `ScrToolLedger` / `ConnClaims` — quoting a receipt is a commit: the quote
  must satisfy P1-P9 in the quoting file too.

## 5. Round-46 committed files: what the gate misses

Scope `.ufo/waves/round-46/` at `60edb66e` (1300 files, 946 text blobs). Values are never
printed here or in the receipts; locators are `git show` + line.

| class | files | occurrences | verdict |
|---|---|---|---|
| G1 env/session assignment | 12 blobs (13 paths) | 15 lines / 21 key hits | 13 template, 1 empty, 5 short placeholder, 2 synthetic (16 and 26 chars, both ≠ the live value); **0 live** — F1 is a path segment, not an assignment |
| G2 absolute `$HOME` path | 150 | 532 | residual account segment; R4 counts whole-line dumps only → F3 |
| G3 `/run/user/<uid>/` | 8 | 12 | F4 |
| G4 exact live monitor identity | 1 | 2 | **F2** |
| G5 secret shape | 0 | 0 | clean |
| G6 e-mail | 29 | 38 | all `scratch.invalid` — clean |
| G7 MAC | 0 | 0 | clean |
| G8 `/proc/<pid>/environ` mention | 10 | 13 | prose/refusal text, no content — clean |
| G9 application inventory | 0 | 0 | clean |
| G10 raw strace (pid-keyed) | 0 | 0 | clean |
| G11 exact host mtime | 0 | 0 | clean |

Gate on the same tree: 18 finding lines over 7 files, all inside its own self-referential
copies (`CritW2Gate.*`, `ExecSerialRule/gate.py`, `ExecSessionTriage/check-session-material.py`
+ `demo/run-demo.sh`, `ExecW2Monitors/adversarial.txt`) — synthetic by the live-value scan,
so no rule-4 violation among them; whole-tree run `files=18371 findings=115`
(`gate-r46.txt`).

### Findings

- **F1 — S1 (high), gate-blind, rule-4 violation, round-46's own.**
  `.ufo/waves/round-46/w1/LabVirtualRules/receipts/log-probe.txt:2` prints the live
  `HYPRLAND_INSTANCE_SIGNATURE` in full inside
  `/run/user/<uid>/hypr/<sig>/hyprland.log`. Introduced by round-46 commit `7f793280`
  ("round-46: v2 controls …, w1 evidence"); `git grep -l -F` over the whole tree at
  `60edb66e` finds exactly this one file (`signature-tree.txt`). `SKILL.md:343-344` forbids it
  in full; the value addresses the live compositor socket for as long as the session lives.
  Smallest remediation: substitute `<INSTANCE_SIG>` on that line (P4), one edit, no claim
  changes — the probe's content is the two zero counts below it, not the path.
- **F2 — S2 (medium), gate-blind, carried.** `.ufo/waves/round-46/w1/ScrMistakes/receipts/d2-serial-count.txt:19,20`
  quotes the live monitor vendor string from the corpus line that round-45 already flagged
  (S1 there). Exact-equality match on `make` only (`live-ident-r46.txt`); R3 needs a
  non-empty `serial` inside a JSON object, so the gate cannot see a prose quote. Remediation
  is L1's: the quote can be written `make=<vendor>`, and the corpus source needs the
  round-45 remediation none of whose owners has edit scope.
- **F3 — S3 (low), residual.** 150 round-46 files carry the account segment in absolute
  paths (largest carriers: `w1-spec.json`, `w1-dispatch.json`, `w1-results.json`,
  `registration*.md`, `make-w1-spec.py` — all machine-written orchestration files). Not new:
  the same class exists in every earlier round. Round 47 can avoid adding to it for free:
  P1/P2 in hand-written receipts, and an L1 post-processing pass over the machine-written
  `w1-*.json` (a `sed` of `$HOME` → `$HOME` on those four files) would not be a privacy
  improvement of committed evidence but of the diff noise; the L1 decides.
- **F4 — S3 (low).** 8 round-46 files / 12 `/run/user/<uid>/` occurrences (locators in
  `sweep-r46.txt`). P3 for round 47; no remediation value for round 46.
- **F5 — S3 (low), new instrument gap.** No R-rule covers an `env` dump: shape C passes the
  gate while carrying the session D-Bus address, the instance signature, `WAYLAND_DISPLAY`,
  `XDG_SESSION_ID` and session-unique `fnm` dirs. A one-rule addition closes it (below).
- **F6 — S3 (low), new instrument gap.** R4 is defeated by its own remedy (`$HOME`
  substitution) and by `ls -1` (no rule). Demonstrated end-to-end: `gate-redacted.txt` = 0
  round-47 findings on a tree whose `sample-receipt-B` redaction still lists 15 distinct
  applications (`sweep-redacted.txt`).

Not findings: the full-tree `git grep` for the live instance signature and for
`monitor_serial/description/model` finds nothing outside F1/F2; no `ghp_`/`sk-`/`AKIA`/PEM
shape anywhere in round 46; every e-mail is `@scratch.invalid`.

## 6. Gate extension sketch (L1 owns `quality/`; this seat has no edit scope)

Cheapest additions, each with a positive and a negative case already in this report:

- `R5_SESSION_IDENT` — a non-empty assignment of `HYPRLAND_INSTANCE_SIGNATURE`,
  `WAYLAND_DISPLAY`, `DBUS_SESSION_BUS_ADDRESS`, `XDG_SESSION_ID`/`_PATH`, `XDG_SEAT_PATH`,
  or a `hypr/<32 hex>/` path segment. Fires on shape C and on F1's line; does not fire on
  `=$XDG_RUNTIME_DIR` or `<sig>` placeholders.
- extend `R4` — count whole lines matching `^\$HOME/\S+$` toward the same limit (keeps the
  counter alive under P1), and add a rule for a block of >N bare `*.desktop` lines.
- `R6_HOST_TIMESTAMP` — `mtime=\d{9,}` (shape F).
- `R7_PID_TRACE` — `^\s*\d+\s+execve\(` (shape E).

All four are single regexes plus a document line; none needs a host read, so the gate stays
hermetic. `quality/counters/` convention aside, `w1/SentPrivacy/sweep-privacy.py` is
already the union of them (plus the live-value equality scan) if the L1 prefers to adopt a
tested file.

## 7. Residual / UNK

- `[UNK]` whether any round-46 receipt reached a public mirror before a fix; no egress
  evidence in this seat's scope.
- `[INF]` the 18 gate findings over round-46 are synthetic: inferred from the live-value
  scan (`live-ident-r46.txt` matches only `d2-serial-count.txt`), not from reading each
  serial. A seat that wants them proved can run the same equality scan with a fixture
  vocabulary file.
- The `$WORK` prefix is per-seat; a receipt quoting
  another seat's `$WORK` must say which seat — otherwise the reader cannot re-derive it.
  Minor, and P2 keeps it honest.
- Desktop-file values were not audited for user-authored content beyond the selected entry.
  If a seat prints the *whole* selected file (21 lines, `[Desktop Action New]` included),
  the `Exec` of that action is still shipped software data; no private value exists in the
  entry selected on this host today. A future override with a private command would change
  that: then the rule needs "keys verbatim, values only for Exec/TryExec of the main
  action".

## 8. Tool ledger

No install, no upgrade, no package query (host pause honoured). Used: `python3` (stdlib)
for `redact.py`, `sweep-privacy.py`, `live-ident.py`; `git` read-only in the lane and
`git` write-only inside `$WORK/lane`; `sha256sum`, `find`, `sed`, `stat`; `hyprctl -j
monitors` (read verb) once, written to scratch and deleted with it. Scratch (`$WORK`, the seat directory the round spec fixes) removed before this seat
closed.
